#!/usr/bin/env python3
"""Validate repository-controlled MODA release gates and render a human handoff."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

import yaml


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scripts.validate_moda import validate_repository  # noqa: E402


SEMVER = re.compile(
    r"^(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)"
    r"(?:-[0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*)?"
    r"(?:\+[0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*)?$"
)
STABLE_SEMVER = re.compile(r"^(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)$")
COMMIT = re.compile(r"^[0-9a-f]{40}$")
ZERO_COMMIT = "0" * 40
EVIDENCE_ONLY_PREFIXES = ("audits/", "conformance/", "releases/", "moda.yaml")


@dataclass
class Finding:
    severity: str
    code: str
    message: str
    path: str | None = None


def load_yaml(path: Path, findings: list[Finding]) -> dict[str, Any]:
    try:
        value = yaml.safe_load(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        findings.append(Finding("error", "missing-release-file", "Required release file is missing.", str(path)))
        return {}
    except yaml.YAMLError as exc:
        findings.append(Finding("error", "invalid-release-yaml", f"Invalid YAML: {exc}", str(path)))
        return {}
    if not isinstance(value, dict):
        findings.append(Finding("error", "invalid-release-root", "Release YAML root must be a mapping.", str(path)))
        return {}
    return value


def valid_commit(value: str | None) -> bool:
    return isinstance(value, str) and COMMIT.fullmatch(value) is not None and value != ZERO_COMMIT


def version_tuple(value: str) -> tuple[int, int, int] | None:
    match = STABLE_SEMVER.fullmatch(value)
    return tuple(map(int, match.groups())) if match else None


def validate_bump(version: str, bump: str, previous_version: str | None) -> list[Finding]:
    findings: list[Finding] = []
    current = version_tuple(version)
    if current is None:
        return [Finding("error", "unstable-release-version", "Stable release gates require an exact MAJOR.MINOR.PATCH version.")]
    if previous_version is None:
        if bump != "initial":
            findings.append(Finding("error", "invalid-initial-bump", "A repository without a previous stable tag must use bump 'initial'."))
        return findings
    previous = version_tuple(previous_version)
    if previous is None:
        return [Finding("error", "invalid-previous-version", "Previous stable version must be MAJOR.MINOR.PATCH.")]
    expected = {
        "major": (previous[0] + 1, 0, 0),
        "minor": (previous[0], previous[1] + 1, 0),
        "patch": (previous[0], previous[1], previous[2] + 1),
    }.get(bump)
    if expected is None:
        findings.append(Finding("error", "invalid-bump", "Existing releases require bump major, minor, or patch."))
    elif current != expected:
        findings.append(Finding("error", "version-bump-mismatch", f"Bump '{bump}' from {previous_version} requires {'.'.join(map(str, expected))}, not {version}."))
    return findings


def extract_changelog_section(text: str, version: str) -> tuple[str | None, str | None]:
    pattern = re.compile(
        rf"^## \[{re.escape(version)}\] - ([^\n]+)\n(.*?)(?=^## |\Z)",
        re.MULTILINE | re.DOTALL,
    )
    match = pattern.search(text)
    if not match:
        return None, None
    return match.group(1).strip(), match.group(2).strip()


def validate_evidence_paths(paths: list[str]) -> list[Finding]:
    return [
        Finding("error", "non-evidence-release-change", f"Release commit contains non-evidence path '{path}'.", path)
        for path in paths
        if not any(path == prefix or (prefix.endswith("/") and path.startswith(prefix)) for prefix in EVIDENCE_ONLY_PREFIXES)
    ]


def git_output(root: Path, args: list[str]) -> tuple[int, str]:
    result = subprocess.run(["git", *args], cwd=root, check=False, capture_output=True, text=True)
    return result.returncode, (result.stdout.strip() or result.stderr.strip())


def latest_stable_tag(root: Path, target_version: str) -> str | None:
    code, output = git_output(root, ["tag", "--list", "v*", "--sort=-v:refname"])
    if code:
        return None
    for tag in output.splitlines():
        value = tag.removeprefix("v")
        if value != target_version and STABLE_SEMVER.fullmatch(value):
            return value
    return None


def validate_git_release(root: Path, version: str, content_commit: str, release_commit: str) -> list[Finding]:
    findings: list[Finding] = []
    for label, commit in (("content", content_commit), ("release", release_commit)):
        code, _ = git_output(root, ["cat-file", "-e", f"{commit}^{{commit}}"])
        if code:
            findings.append(Finding("error", "missing-git-commit", f"Declared {label}_commit is not available in the checkout.", commit))
    if findings:
        return findings
    code, _ = git_output(root, ["merge-base", "--is-ancestor", content_commit, release_commit])
    if code:
        findings.append(Finding("error", "release-not-descendant", "release_commit must descend from content_commit."))
    code, output = git_output(root, ["diff", "--name-only", content_commit, release_commit])
    if code:
        findings.append(Finding("error", "release-diff-failed", "Could not inspect the content-to-release diff."))
    else:
        findings.extend(validate_evidence_paths([path for path in output.splitlines() if path]))
    code, head = git_output(root, ["rev-parse", "HEAD"])
    if code == 0 and head != release_commit:
        findings.append(Finding("error", "release-head-mismatch", "Checkout HEAD must equal release_commit for final tag readiness."))
    code, _ = git_output(root, ["show-ref", "--verify", "--quiet", f"refs/tags/v{version}"])
    if code == 0:
        findings.append(Finding("error", "tag-already-exists", f"Tag v{version} already exists and must not be moved or reused."))
    return findings


def validate_release(
    root: Path,
    version: str,
    bump: str,
    content_commit: str,
    release_commit: str,
    previous_version: str | None = None,
    require_conformant: bool = True,
    check_git: bool = False,
) -> tuple[list[Finding], str | None]:
    findings: list[Finding] = []
    root = root.resolve()

    for repository_finding in validate_repository(root):
        if repository_finding.severity == "error":
            findings.append(Finding("error", f"repository-{repository_finding.code}", repository_finding.message, repository_finding.path))

    if not SEMVER.fullmatch(version):
        findings.append(Finding("error", "invalid-release-version", "Release version must be valid SemVer."))
    findings.extend(validate_bump(version, bump, previous_version))
    if not valid_commit(content_commit):
        findings.append(Finding("error", "invalid-content-commit", "content_commit must be a non-placeholder full lowercase Git SHA."))
    if not valid_commit(release_commit):
        findings.append(Finding("error", "invalid-release-commit", "release_commit must be a non-placeholder full lowercase Git SHA."))
    if content_commit == release_commit:
        findings.append(Finding("error", "release-equals-content", "release_commit must be an evidence-only descendant of content_commit."))

    manifest = load_yaml(root / "moda.yaml", findings)
    artifact = manifest.get("artifact", {}) if isinstance(manifest, dict) else {}
    adoption = manifest.get("adoption", {}) if isinstance(manifest, dict) else {}
    synchronization = manifest.get("synchronization", {}) if isinstance(manifest, dict) else {}
    conformance_map = manifest.get("conformance", {}) if isinstance(manifest, dict) else {}
    if artifact.get("version") != version:
        findings.append(Finding("error", "manifest-version-mismatch", f"moda.yaml artifact.version must equal {version}.", "moda.yaml"))
    if synchronization.get("state") != "current":
        findings.append(Finding("error", "release-sync-not-current", "Release synchronization state must be current.", "moda.yaml"))

    changelog_path = root / "CHANGELOG.md"
    try:
        changelog = changelog_path.read_text(encoding="utf-8")
    except FileNotFoundError:
        findings.append(Finding("error", "missing-release-changelog", "CHANGELOG.md is missing.", "CHANGELOG.md"))
        changelog = ""
    date, description = extract_changelog_section(changelog, version)
    if date is None:
        findings.append(Finding("error", "missing-changelog-version", f"CHANGELOG.md has no section for {version}.", "CHANGELOG.md"))
    elif re.fullmatch(r"\d{4}-\d{2}-\d{2}", date) is None:
        findings.append(Finding("error", "undated-changelog-version", f"Release {version} must have a YYYY-MM-DD changelog date, not '{date}'.", "CHANGELOG.md"))
    if not description:
        findings.append(Finding("error", "empty-release-description", "The matching changelog section must contain the release description.", "CHANGELOG.md"))

    for impact_path in sorted((root / "changes").glob("*/impact.yaml")):
        impact = load_yaml(impact_path, findings)
        status = impact.get("change", {}).get("status") if isinstance(impact.get("change"), dict) else None
        if status not in {"implemented", "superseded"}:
            findings.append(Finding("error", "incomplete-change-set", f"Change Set status is '{status}', not implemented or superseded.", impact_path.relative_to(root).as_posix()))

    profile_path = conformance_map.get("profile")
    audit_path = conformance_map.get("latest_audit")
    profile = load_yaml(root / profile_path, findings) if isinstance(profile_path, str) else {}
    audit = load_yaml(root / audit_path, findings) if isinstance(audit_path, str) else {}
    assessment = profile.get("assessment", {}) if isinstance(profile, dict) else {}
    audit_subject = audit.get("subject", {}) if isinstance(audit, dict) else {}
    audit_result = audit.get("result", {}) if isinstance(audit, dict) else {}

    if audit_subject.get("commit") != content_commit:
        findings.append(Finding("error", "audit-content-mismatch", "Latest accepted audit subject.commit must equal content_commit.", str(audit_path)))
    if audit_result.get("critical_findings") != 0 or audit_result.get("major_findings") != 0:
        findings.append(Finding("error", "release-blocking-findings", "Latest audit must have zero critical and major findings.", str(audit_path)))
    if require_conformant:
        if adoption.get("claim_stage") not in {"verified", "certified"} or adoption.get("conformance_result") != "conformant":
            findings.append(Finding("error", "release-not-conformant", "This release policy requires verified or certified conformant adoption.", "moda.yaml"))
        if assessment.get("claim_stage") not in {"verified", "certified"} or assessment.get("result") != "conformant":
            findings.append(Finding("error", "profile-not-conformant", "Conformance profile must be verified or certified and conformant.", str(profile_path)))
        if audit_result.get("claim_stage") not in {"verified", "certified"} or audit_result.get("conformance") != "conformant":
            findings.append(Finding("error", "audit-not-conformant", "Latest audit result must be verified or certified and conformant.", str(audit_path)))

    if check_git:
        findings.extend(validate_git_release(root, version, content_commit, release_commit))
    return findings, description


def render_handoff(
    artifact_name: str,
    version: str,
    target_branch: str,
    release_commit: str,
    description: str,
    approval_remaining: str = "explicit human approval and any required tag signing",
) -> str:
    classification = "prerelease" if "-" in version else "latest"
    return f"""# Release creation handoff

Status: **ready for explicit human creation**

- Tag: `v{version}`
- Target branch: `{target_branch}`
- Target commit: `{release_commit}`
- Release title: `{artifact_name} v{version}`
- Release classification: `{classification}`
- Signing or approval remaining: {approval_remaining}

## Release description

{description}

## GitHub creation steps

1. Open **Releases** and choose **Draft a new release**.
2. Create tag `v{version}` targeting `{release_commit}` on `{target_branch}`.
3. Use `{artifact_name} v{version}` as the release title.
4. Paste the release description above.
5. Select **{classification}** as declared.
6. Publish only after the remaining approval or signing step is complete.
"""


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate repository-controlled MODA release gates.")
    parser.add_argument("--root", type=Path, default=Path("."))
    parser.add_argument("--version", required=True)
    parser.add_argument("--bump", required=True, choices=["initial", "major", "minor", "patch"])
    parser.add_argument("--previous-version")
    parser.add_argument("--content-commit", required=True)
    parser.add_argument("--release-commit", required=True)
    parser.add_argument("--target-branch", default="main")
    parser.add_argument("--allow-partial", action="store_true", help="Do not require a verified conformant claim.")
    parser.add_argument("--skip-git", action="store_true", help="Skip checkout-specific ancestry, diff, HEAD, and tag checks.")
    parser.add_argument(
        "--remote-gates-passed",
        action="store_true",
        help="Confirm that required remote branch, pull-request, CI, review, and tag-absence gates were independently verified.",
    )
    parser.add_argument("--handoff", action="store_true", help="Render the exact human creation handoff after validation passes.")
    parser.add_argument("--json", action="store_true", dest="json_output")
    args = parser.parse_args()

    root = args.root.resolve()
    previous = args.previous_version
    if previous is None and (root / ".git").exists():
        previous = latest_stable_tag(root, args.version)
    findings, description = validate_release(
        root,
        args.version,
        args.bump,
        args.content_commit,
        args.release_commit,
        previous,
        not args.allow_partial,
        (root / ".git").exists() and not args.skip_git,
    )
    if args.handoff and not args.remote_gates_passed:
        findings.append(Finding(
            "error",
            "remote-gates-not-confirmed",
            "A ready release handoff requires independent confirmation of the remote branch, pull request, CI, review, and tag-absence gates.",
        ))
    if args.json_output:
        print(json.dumps([asdict(item) for item in findings], indent=2))
    elif findings:
        for item in findings:
            location = f" [{item.path}]" if item.path else ""
            print(f"{item.severity.upper()} {item.code}{location}: {item.message}")
    elif args.handoff and description is not None:
        manifest = yaml.safe_load((root / "moda.yaml").read_text(encoding="utf-8"))
        print(render_handoff(manifest["artifact"]["name"], args.version, args.target_branch, args.release_commit, description))
    else:
        print("Repository-controlled release gates passed. Remote checks, signing, and explicit human approval remain required.")
    return 1 if any(item.severity == "error" for item in findings) else 0


if __name__ == "__main__":
    sys.exit(main())
