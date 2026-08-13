#!/usr/bin/env python3
"""Validate MODA Change Sets against a Git diff."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Iterable

import yaml


SURFACES = (
    "specification", "decisions", "documentation", "entrypoints", "manifests",
    "skill", "schemas", "validators", "tests", "ci", "templates", "examples",
    "changelog", "upgrade", "migrations", "roadmap", "conformance",
)
STATUSES = {"updated", "reviewed", "not-applicable"}
CLASSES = {"editorial", "operational", "normative"}
SEMVER = {"none", "patch", "minor", "major"}
CHANGE_STATUSES = {"proposed", "accepted", "implemented", "superseded"}
TRIGGERS = {"normative_rule", "public_path", "package_contract", "security_behavior", "release"}

SURFACE_PREFIXES: dict[str, tuple[str, ...]] = {
    "specification": ("SPEC.md",),
    "decisions": ("decisions/",),
    "documentation": ("docs/",),
    "entrypoints": ("README.md", "AGENTS.md", "CLAUDE.md", "GETTING-STARTED.md"),
    "manifests": ("moda.yaml", "skill/manifest.yaml"),
    "skill": ("skill/",),
    "schemas": ("schemas/",),
    "validators": ("scripts/",),
    "tests": ("tests/",),
    "ci": (".github/",),
    "templates": ("templates/",),
    "examples": ("examples/",),
    "changelog": ("CHANGELOG.md",),
    "upgrade": ("UPGRADE.md",),
    "migrations": ("MIGRATIONS.md",),
    "roadmap": ("ROADMAP.md",),
    "conformance": ("conformance/", "audits/"),
}

TRIGGER_SURFACES: dict[str, set[str]] = {
    "normative_rule": {"specification", "skill", "manifests", "schemas", "validators", "templates", "examples", "changelog", "upgrade", "migrations", "conformance"},
    "public_path": {"entrypoints", "manifests", "skill", "templates", "examples", "validators", "conformance"},
    "package_contract": {"manifests", "skill", "schemas", "templates", "examples", "changelog"},
    "security_behavior": {"specification", "skill", "manifests", "validators", "tests", "changelog", "upgrade"},
    "release": {"changelog", "upgrade", "migrations", "conformance"},
}

PROTECTED_PREFIXES = tuple(
    sorted({prefix for values in SURFACE_PREFIXES.values() for prefix in values})
)


@dataclass
class Finding:
    severity: str
    code: str
    message: str
    path: str | None = None


def path_matches(path: str, prefix: str) -> bool:
    return path == prefix or (prefix.endswith("/") and path.startswith(prefix))


def parse_name_status(text: str) -> set[str]:
    """Return all current and previous paths from git --name-status output."""
    paths: set[str] = set()
    for raw in text.splitlines():
        line = raw.strip()
        if not line:
            continue
        parts = line.split("\t")
        if len(parts) == 1:
            paths.add(parts[0])
            continue
        status = parts[0]
        if status.startswith(("R", "C")) and len(parts) >= 3:
            paths.update((parts[1], parts[2]))
        elif len(parts) >= 2:
            paths.add(parts[1])
    return paths


def git_changed_files(root: Path, base: str, head: str) -> set[str]:
    result = subprocess.run(
        ["git", "diff", "--name-status", "--find-renames", base, head],
        cwd=root,
        check=False,
        capture_output=True,
        text=True,
    )
    if result.returncode:
        raise RuntimeError(result.stderr.strip() or "git diff failed")
    return parse_name_status(result.stdout)


def git_commit_distance(root: Path, base: str, head: str) -> int | None:
    """Return the number of commits from an ancestor base to head."""
    ancestor = subprocess.run(
        ["git", "merge-base", "--is-ancestor", base, head],
        cwd=root,
        check=False,
        capture_output=True,
        text=True,
    )
    if ancestor.returncode:
        return None
    result = subprocess.run(
        ["git", "rev-list", "--count", f"{base}..{head}"],
        cwd=root,
        check=False,
        capture_output=True,
        text=True,
    )
    if result.returncode:
        return None
    try:
        return int(result.stdout.strip())
    except ValueError:
        return None


def select_nearest_impact(impact_distances: list[tuple[Path, int]]) -> tuple[Path | None, list[Finding]]:
    """Select the active Change Set whose declared base is nearest to HEAD."""
    if not impact_distances:
        return None, []
    nearest_distance = min(distance for _, distance in impact_distances)
    nearest = [path for path, distance in impact_distances if distance == nearest_distance]
    if len(nearest) != 1:
        labels = ", ".join(path.as_posix() for path in nearest)
        return None, [Finding(
            "error",
            "ambiguous-active-change-set",
            f"Multiple Change Sets have the nearest declared base ({labels}); select one explicitly with --impact.",
            "changes/",
        )]
    return nearest[0], []


def discover_active_impact(root: Path, impact_paths: list[Path], head: str) -> tuple[Path | None, list[Finding]]:
    """Resolve current linear work without applying it to historical Change Sets."""
    findings: list[Finding] = []
    distances: list[tuple[Path, int]] = []
    for impact_path in impact_paths:
        data = load_yaml(impact_path, findings)
        declared_git = data.get("git", {}) if isinstance(data, dict) else {}
        declared_base = declared_git.get("base_ref") if isinstance(declared_git, dict) else None
        relative = impact_path.relative_to(root).as_posix()
        if not isinstance(declared_base, str) or not declared_base:
            findings.append(Finding("error", "invalid-declared-base", "Change Set must declare a non-empty git.base_ref.", relative))
            continue
        distance = git_commit_distance(root, declared_base, head)
        if distance is None:
            findings.append(Finding("error", "invalid-declared-base", f"Declared base '{declared_base}' is not an available ancestor of HEAD.", relative))
            continue
        distances.append((impact_path, distance))
    selected, selection_findings = select_nearest_impact(distances)
    findings.extend(selection_findings)
    return selected, findings


def load_yaml(path: Path, findings: list[Finding]) -> dict[str, Any]:
    try:
        value = yaml.safe_load(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        findings.append(Finding("error", "missing-impact", "Change impact file is missing.", str(path)))
        return {}
    except yaml.YAMLError as exc:
        findings.append(Finding("error", "invalid-impact-yaml", f"Invalid YAML: {exc}", str(path)))
        return {}
    if not isinstance(value, dict):
        findings.append(Finding("error", "invalid-impact-root", "Impact root must be a mapping.", str(path)))
        return {}
    return value


def require_mapping(parent: dict[str, Any], key: str, path: str, findings: list[Finding]) -> dict[str, Any]:
    value = parent.get(key)
    if not isinstance(value, dict):
        findings.append(Finding("error", "missing-impact-section", f"Required mapping '{key}' is missing.", path))
        return {}
    return value


def validate_declared_path(root: Path, relative: str, impact_path: str, findings: list[Finding]) -> None:
    if relative.endswith("/"):
        exists = (root / relative.rstrip("/")).is_dir()
    else:
        exists = (root / relative).exists()
    if not exists:
        findings.append(Finding("error", "missing-declared-path", f"Declared path '{relative}' does not exist.", impact_path))


def validate_impact(root: Path, impact_path: Path, changed_files: set[str]) -> list[Finding]:
    findings: list[Finding] = []
    relative_impact = impact_path.relative_to(root).as_posix()
    data = load_yaml(impact_path, findings)
    if not data:
        return findings

    proposal_path = impact_path.parent / "proposal.md"
    if not proposal_path.is_file():
        findings.append(Finding("error", "missing-change-proposal", "Change Set impact must have a sibling proposal.md.", relative_impact))

    expected_top_level = {"change", "git", "triggers", "affected", "validation"}
    if set(data) != expected_top_level:
        findings.append(Finding("error", "invalid-impact-sections", f"Impact sections must be exactly {sorted(expected_top_level)}.", relative_impact))

    change = require_mapping(data, "change", relative_impact, findings)
    git = require_mapping(data, "git", relative_impact, findings)
    triggers = require_mapping(data, "triggers", relative_impact, findings)
    affected = require_mapping(data, "affected", relative_impact, findings)
    validation = require_mapping(data, "validation", relative_impact, findings)

    required_change = {"id", "title", "class", "semver", "status", "structural", "summary"}
    missing = sorted(required_change - change.keys())
    for key in missing:
        findings.append(Finding("error", "missing-change-field", f"Required change field '{key}' is missing.", relative_impact))
    if set(change) - required_change:
        findings.append(Finding("error", "unexpected-change-field", f"Unexpected change fields: {sorted(set(change) - required_change)}.", relative_impact))
    if not isinstance(change.get("id"), str) or re.fullmatch(r"[a-z0-9][a-z0-9-]*", change.get("id", "")) is None:
        findings.append(Finding("error", "invalid-change-id", "Change id must use lowercase letters, digits, and hyphens.", relative_impact))
    elif impact_path.parent.name != change.get("id"):
        findings.append(Finding("error", "change-id-path-mismatch", "Change id must match its changes/<change-id>/ directory.", relative_impact))
    for key in ("title", "summary"):
        if not isinstance(change.get(key), str) or not change[key].strip():
            findings.append(Finding("error", "invalid-change-text", f"Change field '{key}' must be a non-empty string.", relative_impact))
    if change.get("class") not in CLASSES:
        findings.append(Finding("error", "invalid-change-class", "Change class is invalid.", relative_impact))
    if change.get("semver") not in SEMVER:
        findings.append(Finding("error", "invalid-semver-impact", "SemVer impact is invalid.", relative_impact))
    if change.get("status") not in CHANGE_STATUSES:
        findings.append(Finding("error", "invalid-change-status", "Change status is invalid.", relative_impact))
    if not isinstance(change.get("structural"), bool):
        findings.append(Finding("error", "invalid-structural-flag", "structural must be boolean.", relative_impact))
    if change.get("class") != "editorial" and change.get("semver") == "none":
        findings.append(Finding("error", "missing-semver-impact", "Operational and normative changes require patch, minor, or major impact.", relative_impact))
    if change.get("class") == "editorial" and change.get("semver") not in {"none", "patch"}:
        findings.append(Finding("error", "excessive-editorial-impact", "Editorial changes may declare only none or patch impact.", relative_impact))

    for key in ("base_ref", "target_branch"):
        if not isinstance(git.get(key), str) or not git[key].strip():
            findings.append(Finding("error", "missing-git-field", f"Required git field '{key}' is missing.", relative_impact))
    if set(git) - {"base_ref", "target_branch"}:
        findings.append(Finding("error", "unexpected-git-field", f"Unexpected git fields: {sorted(set(git) - {'base_ref', 'target_branch'})}.", relative_impact))

    if set(triggers) != TRIGGERS:
        findings.append(Finding("error", "invalid-trigger-set", f"Triggers must be exactly {sorted(TRIGGERS)}.", relative_impact))
    for name, enabled in triggers.items():
        if not isinstance(enabled, bool):
            findings.append(Finding("error", "invalid-trigger", f"Trigger '{name}' must be boolean.", relative_impact))

    if change.get("class") == "normative" and triggers.get("normative_rule") is not True:
        findings.append(Finding("error", "missing-normative-trigger", "Normative changes must set normative_rule.", relative_impact))
    if triggers.get("normative_rule") and change.get("class") != "normative":
        findings.append(Finding("error", "trigger-class-mismatch", "normative_rule requires normative class.", relative_impact))
    if change.get("structural") is True and affected.get("decisions", {}).get("status") != "updated":
        findings.append(Finding("error", "missing-structural-decision", "Structural changes must update a Decision Record.", relative_impact))

    surface_data: dict[str, dict[str, Any]] = {}
    if set(affected) != set(SURFACES):
        findings.append(Finding("error", "invalid-surface-set", f"Affected surfaces must be exactly {sorted(SURFACES)}.", relative_impact))
    for surface in SURFACES:
        item = affected.get(surface)
        if not isinstance(item, dict):
            findings.append(Finding("error", "missing-surface", f"Affected surface '{surface}' is missing.", relative_impact))
            continue
        surface_data[surface] = item
        status = item.get("status")
        paths = item.get("paths")
        rationale = item.get("rationale")
        unexpected_surface_fields = set(item) - {"status", "paths", "rationale"}
        if unexpected_surface_fields:
            findings.append(Finding("error", "unexpected-surface-field", f"Surface '{surface}' has unexpected fields: {sorted(unexpected_surface_fields)}.", relative_impact))
        if status not in STATUSES:
            findings.append(Finding("error", "invalid-surface-status", f"Surface '{surface}' has invalid status.", relative_impact))
            continue
        if not isinstance(paths, list) or any(not isinstance(value, str) or not value for value in paths):
            findings.append(Finding("error", "invalid-surface-paths", f"Surface '{surface}' paths must be an array of non-empty strings.", relative_impact))
            continue
        if status == "updated" and not paths:
            findings.append(Finding("error", "missing-updated-path", f"Updated surface '{surface}' must declare paths.", relative_impact))
        if status in {"reviewed", "not-applicable"} and (not isinstance(rationale, str) or not rationale.strip()):
            findings.append(Finding("error", "missing-surface-rationale", f"Surface '{surface}' with status '{status}' requires rationale.", relative_impact))
        for relative in paths:
            validate_declared_path(root, relative, relative_impact, findings)
        if status == "updated" and paths and not any(
            any(path_matches(changed, declared) for changed in changed_files) for declared in paths
        ):
            findings.append(Finding("error", "updated-path-not-changed", f"Surface '{surface}' declares updated paths absent from the diff.", relative_impact))

    for surface, prefixes in SURFACE_PREFIXES.items():
        if any(any(path_matches(changed, prefix) for prefix in prefixes) for changed in changed_files):
            if surface_data.get(surface, {}).get("status") != "updated":
                findings.append(Finding("error", "changed-surface-not-updated", f"Changed surface '{surface}' must be declared updated.", relative_impact))

    declared_updated_paths = {
        declared
        for item in surface_data.values()
        if item.get("status") == "updated"
        for declared in item.get("paths", [])
        if isinstance(declared, str)
    }
    for changed in sorted(changed_files):
        if changed.startswith("changes/"):
            continue
        if any(path_matches(changed, prefix) for prefix in PROTECTED_PREFIXES) and not any(
            path_matches(changed, declared) for declared in declared_updated_paths
        ):
            findings.append(Finding("error", "uncovered-changed-path", f"Protected changed path '{changed}' is not covered by an updated declaration.", relative_impact))

    for trigger, required_surfaces in TRIGGER_SURFACES.items():
        if triggers.get(trigger) is True:
            for surface in sorted(required_surfaces):
                if surface_data.get(surface, {}).get("status") not in STATUSES:
                    findings.append(Finding("error", "unreviewed-trigger-surface", f"Trigger '{trigger}' requires surface '{surface}' to be considered.", relative_impact))

    if triggers.get("normative_rule") and surface_data.get("specification", {}).get("status") != "updated":
        findings.append(Finding("error", "normative-spec-not-updated", "A normative rule change must update the specification.", relative_impact))
    if triggers.get("security_behavior") and surface_data.get("skill", {}).get("status") != "updated":
        findings.append(Finding("error", "security-skill-not-updated", "Security behavior changes must update the operational skill.", relative_impact))
    if triggers.get("release") and surface_data.get("changelog", {}).get("status") != "updated":
        findings.append(Finding("error", "release-changelog-not-updated", "Release changes must update the changelog.", relative_impact))

    commands = validation.get("commands")
    evidence = validation.get("evidence")
    if set(validation) - {"commands", "evidence"}:
        findings.append(Finding("error", "unexpected-validation-field", f"Unexpected validation fields: {sorted(set(validation) - {'commands', 'evidence'})}.", relative_impact))
    if not isinstance(commands, list) or not commands or any(not isinstance(value, str) or not value for value in commands):
        findings.append(Finding("error", "invalid-validation-commands", "Validation commands must be a non-empty string array.", relative_impact))
    if not isinstance(evidence, list) or any(not isinstance(value, str) or not value for value in evidence):
        findings.append(Finding("error", "invalid-validation-evidence", "Validation evidence must be a string array.", relative_impact))
    elif isinstance(evidence, list):
        for relative in evidence:
            validate_declared_path(root, relative, relative_impact, findings)

    return findings


def discover_impacts(root: Path, changed_files: set[str]) -> list[Path]:
    return sorted(
        root / path for path in changed_files
        if path.startswith("changes/") and path.endswith("/impact.yaml") and (root / path).is_file()
    )


def change_set_required(changed_files: Iterable[str]) -> bool:
    return any(
        not path.startswith("changes/") and any(path_matches(path, prefix) for prefix in PROTECTED_PREFIXES)
        for path in changed_files
    )


def validate_changes(root: Path, changed_files: set[str], impact_paths: list[Path] | None = None) -> list[Finding]:
    findings: list[Finding] = []
    impacts = impact_paths if impact_paths is not None else discover_impacts(root, changed_files)
    if change_set_required(changed_files) and not impacts:
        findings.append(Finding("error", "missing-change-set", "Protected contract surfaces changed without a MODA Change Set.", "changes/"))
        return findings
    for impact in impacts:
        findings.extend(validate_impact(root, impact, changed_files))
    return findings


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate MODA Change Sets against a Git diff.")
    parser.add_argument("--root", type=Path, default=Path("."), help="Repository root.")
    parser.add_argument("--base", help="Base branch, tag, or commit for git diff.")
    parser.add_argument("--head", default="HEAD", help="Head branch, tag, or commit for git diff.")
    parser.add_argument("--name-status-file", type=Path, help="Read git --name-status compatible input from a file.")
    parser.add_argument("--impact", type=Path, action="append", help="Explicit impact file; may be repeated.")
    parser.add_argument("--json", action="store_true", dest="json_output", help="Emit machine-readable findings.")
    args = parser.parse_args()

    root = args.root.resolve()
    try:
        if args.name_status_file:
            changed = parse_name_status(args.name_status_file.read_text(encoding="utf-8"))
        elif args.base:
            changed = git_changed_files(root, args.base, args.head)
        else:
            parser.error("provide --base or --name-status-file")
    except (OSError, RuntimeError) as exc:
        print(f"ERROR change-diff: {exc}", file=sys.stderr)
        return 2

    explicit_impacts = args.impact is not None
    impact_paths = [path.resolve() for path in args.impact] if explicit_impacts else discover_impacts(root, changed)
    if change_set_required(changed) and not impact_paths:
        findings = [Finding("error", "missing-change-set", "Protected contract surfaces changed without a MODA Change Set.", "changes/")]
    elif args.base and impact_paths:
        findings = []
        if not explicit_impacts:
            active_impact, selection_findings = discover_active_impact(root, impact_paths, args.head)
            findings.extend(selection_findings)
            impact_paths = [active_impact] if active_impact is not None else []
        for impact_path in impact_paths:
            impact_data = load_yaml(impact_path, findings)
            declared_git = impact_data.get("git", {}) if isinstance(impact_data, dict) else {}
            declared_base = declared_git.get("base_ref") if isinstance(declared_git, dict) else None
            if not isinstance(declared_base, str) or not declared_base:
                findings.extend(validate_impact(root, impact_path, changed))
                continue
            try:
                impact_changed = git_changed_files(root, declared_base, args.head)
            except RuntimeError as exc:
                findings.append(Finding("error", "invalid-declared-base", f"Cannot diff declared base '{declared_base}': {exc}", impact_path.relative_to(root).as_posix()))
                continue
            findings.extend(validate_impact(root, impact_path, impact_changed))
    else:
        findings = validate_changes(root, changed, impact_paths)
    if args.json_output:
        print(json.dumps([asdict(item) for item in findings], indent=2))
    elif findings:
        for item in findings:
            location = f" [{item.path}]" if item.path else ""
            print(f"{item.severity.upper()} {item.code}{location}: {item.message}")
    else:
        print("MODA change validation passed.")
    return 1 if any(item.severity == "error" for item in findings) else 0


if __name__ == "__main__":
    sys.exit(main())
