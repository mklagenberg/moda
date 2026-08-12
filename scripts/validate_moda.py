#!/usr/bin/env python3
"""Validate deterministic MODA repository requirements."""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

import yaml


SEMVER = re.compile(r"^[0-9]+\.[0-9]+\.[0-9]+$")
COMMIT = re.compile(r"^[0-9a-f]{40}$")
OFFICIAL_REPOSITORY = "https://github.com/mklagenberg/moda"
DISCLOSURE_START = "<!-- moda:disclosure:start -->"
DISCLOSURE_END = "<!-- moda:disclosure:end -->"
CANONICAL_SCHEMA = Path(__file__).resolve().parents[1] / "schemas" / "moda.schema.json"


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
        findings.append(Finding("error", "missing-file", "Required YAML file is missing.", str(path)))
        return {}
    except yaml.YAMLError as exc:
        findings.append(Finding("error", "invalid-yaml", f"Invalid YAML: {exc}", str(path)))
        return {}
    if not isinstance(value, dict):
        findings.append(Finding("error", "invalid-root", "YAML root must be a mapping.", str(path)))
        return {}
    return value


def local_target(value: str) -> str:
    return value.split("#", 1)[0].rstrip("/")


def require_mapping(parent: dict[str, Any], key: str, path: str, findings: list[Finding]) -> dict[str, Any]:
    value = parent.get(key)
    if not isinstance(value, dict):
        findings.append(Finding("error", "missing-section", f"Required mapping '{key}' is missing.", path))
        return {}
    return value


def require_keys(mapping: dict[str, Any], keys: list[str], path: str, findings: list[Finding]) -> None:
    for key in keys:
        if key not in mapping or mapping[key] in (None, ""):
            findings.append(Finding("error", "missing-key", f"Required key '{key}' is missing.", path))


def type_matches(value: Any, expected: str) -> bool:
    """Return whether a value matches the JSON Schema type used by MODA."""
    checks = {
        "object": lambda item: isinstance(item, dict),
        "array": lambda item: isinstance(item, list),
        "string": lambda item: isinstance(item, str),
        "integer": lambda item: isinstance(item, int) and not isinstance(item, bool),
        "number": lambda item: isinstance(item, (int, float)) and not isinstance(item, bool),
        "boolean": lambda item: isinstance(item, bool),
        "null": lambda item: item is None,
    }
    return checks.get(expected, lambda _item: True)(value)


def validate_schema_value(value: Any, schema: dict[str, Any], location: str, findings: list[Finding]) -> None:
    """Validate the deterministic JSON Schema subset used by moda.schema.json."""
    expected_type = schema.get("type")
    if isinstance(expected_type, str) and not type_matches(value, expected_type):
        findings.append(Finding("error", "schema-type", f"Expected {expected_type} at {location}.", "moda.yaml"))
        return

    if "const" in schema and value != schema["const"]:
        findings.append(Finding("error", "schema-const", f"Value at {location} must equal {schema['const']!r}.", "moda.yaml"))

    allowed = schema.get("enum")
    if isinstance(allowed, list) and value not in allowed:
        findings.append(Finding("error", "schema-enum", f"Value at {location} is not one of {allowed!r}.", "moda.yaml"))

    if isinstance(value, str):
        minimum = schema.get("minLength")
        if isinstance(minimum, int) and len(value) < minimum:
            findings.append(Finding("error", "schema-min-length", f"Value at {location} is too short.", "moda.yaml"))
        pattern = schema.get("pattern")
        if isinstance(pattern, str) and re.fullmatch(pattern, value) is None:
            findings.append(Finding("error", "schema-pattern", f"Value at {location} does not match {pattern!r}.", "moda.yaml"))
        if schema.get("format") == "uri":
            parsed = urlparse(value)
            if not parsed.scheme or (parsed.scheme in {"http", "https"} and not parsed.netloc):
                findings.append(Finding("error", "schema-uri", f"Value at {location} is not an absolute URI.", "moda.yaml"))

    if isinstance(value, dict):
        required = schema.get("required", [])
        for key in required if isinstance(required, list) else []:
            if key not in value:
                findings.append(Finding("error", "schema-required", f"Required property {location}.{key} is missing.", "moda.yaml"))

        properties = schema.get("properties", {})
        properties = properties if isinstance(properties, dict) else {}
        additional = schema.get("additionalProperties", True)
        for key, child in value.items():
            child_location = f"{location}.{key}"
            if key in properties and isinstance(properties[key], dict):
                validate_schema_value(child, properties[key], child_location, findings)
            elif additional is False:
                findings.append(Finding("error", "schema-additional-property", f"Unexpected property {child_location}.", "moda.yaml"))
            elif isinstance(additional, dict):
                validate_schema_value(child, additional, child_location, findings)

        minimum = schema.get("minProperties")
        if isinstance(minimum, int) and len(value) < minimum:
            findings.append(Finding("error", "schema-min-properties", f"Object at {location} has too few properties.", "moda.yaml"))

    if isinstance(value, list):
        item_schema = schema.get("items")
        if isinstance(item_schema, dict):
            for index, item in enumerate(value):
                validate_schema_value(item, item_schema, f"{location}[{index}]", findings)


def validate_disclosure(
    root: Path,
    relative: str,
    artifact: dict[str, Any],
    moda: dict[str, Any],
    agent_entrypoint: bool,
    findings: list[Finding],
) -> None:
    path = root / relative
    if not path.is_file():
        findings.append(Finding("error", "missing-entrypoint", "Required disclosure file is missing.", relative))
        return
    text = path.read_text(encoding="utf-8")
    if DISCLOSURE_START not in text or DISCLOSURE_END not in text:
        findings.append(Finding("error", "missing-disclosure", "MODA disclosure markers are missing.", relative))
    if OFFICIAL_REPOSITORY not in text:
        findings.append(Finding("error", "missing-official-link", "MODA official repository link is missing.", relative))
    if "moda.yaml" not in text:
        findings.append(Finding("error", "missing-manifest-link", "MODA manifest is not referenced.", relative))
    if "conformance/moda.yaml" not in text:
        findings.append(Finding("error", "missing-conformance-link", "MODA conformance profile is not referenced.", relative))
    if not agent_entrypoint:
        kind = artifact.get("kind")
        compatibility = moda.get("compatibility")
        if isinstance(kind, str) and kind not in text:
            findings.append(Finding("error", "missing-profile-disclosure", f"Artifact profile '{kind}' is not disclosed.", relative))
        if isinstance(compatibility, str) and compatibility not in text:
            findings.append(Finding("error", "missing-compatibility-disclosure", f"MODA compatibility '{compatibility}' is not disclosed.", relative))


def validate_repository(root: Path, schema_path: Path | None = None) -> list[Finding]:
    findings: list[Finding] = []
    manifest_path = root / "moda.yaml"
    manifest = load_yaml(manifest_path, findings)
    if not manifest:
        return findings

    require_keys(
        manifest,
        ["moda", "artifact", "adoption", "documentation", "components", "packages", "conformance", "synchronization"],
        "moda.yaml",
        findings,
    )

    moda = require_mapping(manifest, "moda", "moda.yaml", findings)
    artifact = require_mapping(manifest, "artifact", "moda.yaml", findings)
    adoption = require_mapping(manifest, "adoption", "moda.yaml", findings)
    documentation = require_mapping(manifest, "documentation", "moda.yaml", findings)
    packages = require_mapping(manifest, "packages", "moda.yaml", findings)
    conformance = require_mapping(manifest, "conformance", "moda.yaml", findings)
    synchronization = require_mapping(manifest, "synchronization", "moda.yaml", findings)

    require_keys(moda, ["manifest_version", "repository", "compatibility", "verified_against", "verified_commit"], "moda.yaml:moda", findings)
    require_keys(artifact, ["id", "name", "kind", "version", "status", "language", "repository", "license"], "moda.yaml:artifact", findings)
    require_keys(adoption, ["relationship", "mode", "claim_stage", "conformance_result"], "moda.yaml:adoption", findings)
    require_keys(documentation, ["human_entrypoint", "agent_entrypoint", "specification", "getting_started", "invariants", "changelog", "upgrade", "migrations", "decisions"], "moda.yaml:documentation", findings)
    require_keys(conformance, ["profile", "latest_audit", "audit_mode"], "moda.yaml:conformance", findings)
    require_keys(synchronization, ["policy", "state", "reason"], "moda.yaml:synchronization", findings)

    if artifact.get("kind") not in {"methodology", "framework"}:
        findings.append(Finding("error", "invalid-kind", "Artifact kind must be 'methodology' or 'framework'.", "moda.yaml"))
    for label, value in (("artifact.version", artifact.get("version")), ("moda.verified_against", moda.get("verified_against"))):
        if not isinstance(value, str) or not SEMVER.fullmatch(value):
            findings.append(Finding("error", "invalid-semver", f"{label} must be a three-part semantic version.", "moda.yaml"))
    commit = moda.get("verified_commit")
    if not isinstance(commit, str) or not COMMIT.fullmatch(commit):
        findings.append(Finding("error", "invalid-commit", "verified_commit must be a full lowercase Git commit SHA.", "moda.yaml"))

    for label, relative in documentation.items():
        if not isinstance(relative, str):
            findings.append(Finding("error", "invalid-path", f"Documentation path '{label}' must be a string.", "moda.yaml"))
            continue
        target = local_target(relative)
        if target and not (root / target).exists():
            findings.append(Finding("error", "broken-documentation-path", f"Documentation target '{relative}' does not exist.", "moda.yaml"))

    for label, package in packages.items():
        if not isinstance(package, dict):
            findings.append(Finding("error", "invalid-package", f"Package '{label}' must be a mapping.", "moda.yaml"))
            continue
        require_keys(package, ["version", "source"], f"moda.yaml:packages.{label}", findings)
        version = package.get("version")
        if isinstance(version, str) and not SEMVER.fullmatch(version):
            findings.append(Finding("error", "invalid-package-version", f"Package '{label}' has an invalid version.", "moda.yaml"))
        source = package.get("source")
        if isinstance(source, str) and not (root / local_target(source)).exists():
            findings.append(Finding("error", "broken-package-source", f"Package source '{source}' does not exist.", "moda.yaml"))

    profile = conformance.get("profile")
    audit = conformance.get("latest_audit")
    profile_data: dict[str, Any] = {}
    audit_data: dict[str, Any] = {}
    if isinstance(profile, str):
        profile_data = load_yaml(root / profile, findings)
    if isinstance(audit, str):
        audit_data = load_yaml(root / audit, findings)
        if audit_data:
            require_mapping(audit_data, "audit", audit, findings)
            require_mapping(audit_data, "auditor", audit, findings)
            require_mapping(audit_data, "subject", audit, findings)
            require_mapping(audit_data, "framework", audit, findings)
            require_mapping(audit_data, "result", audit, findings)

    if profile_data:
        framework = require_mapping(profile_data, "framework", str(profile), findings)
        subject = require_mapping(profile_data, "subject", str(profile), findings)
        assessment = require_mapping(profile_data, "assessment", str(profile), findings)
        controls = require_mapping(profile_data, "controls", str(profile), findings)
        expected = {
            "framework.verified_against": (framework.get("verified_against"), moda.get("verified_against")),
            "framework.verified_commit": (framework.get("verified_commit"), moda.get("verified_commit")),
            "subject.id": (subject.get("id"), artifact.get("id")),
            "subject.kind": (subject.get("kind"), artifact.get("kind")),
            "subject.version": (subject.get("version"), artifact.get("version")),
            "assessment.claim_stage": (assessment.get("claim_stage"), adoption.get("claim_stage")),
            "assessment.result": (assessment.get("result"), adoption.get("conformance_result")),
        }
        for label, (actual, wanted) in expected.items():
            if actual != wanted:
                findings.append(Finding("error", "conformance-mismatch", f"{label} is {actual!r}; expected {wanted!r} from moda.yaml.", str(profile)))
        if assessment.get("claim_stage") in {"mapped", "verified", "certified"} and not controls:
            findings.append(Finding("error", "empty-controls", "Conformance profile must map at least one control.", str(profile)))

    if audit_data:
        audit_subject = require_mapping(audit_data, "subject", str(audit), findings)
        audit_framework = require_mapping(audit_data, "framework", str(audit), findings)
        audit_result = require_mapping(audit_data, "result", str(audit), findings)
        for label, value in (("subject.commit", audit_subject.get("commit")), ("framework.commit", audit_framework.get("commit"))):
            if not isinstance(value, str) or not COMMIT.fullmatch(value):
                findings.append(Finding("error", "invalid-audit-commit", f"Audit {label} must be a full lowercase Git commit SHA.", str(audit)))
        expected = {
            "subject.id": (audit_subject.get("id"), artifact.get("id")),
            "subject.kind": (audit_subject.get("kind"), artifact.get("kind")),
            "subject.version": (audit_subject.get("version"), artifact.get("version")),
            "framework.version": (audit_framework.get("version"), moda.get("verified_against")),
            "result.profile": (audit_result.get("profile"), artifact.get("kind")),
            "result.conformance": (audit_result.get("conformance"), adoption.get("conformance_result")),
        }
        for label, (actual, wanted) in expected.items():
            if actual != wanted:
                findings.append(Finding("error", "audit-mismatch", f"{label} is {actual!r}; expected {wanted!r} from moda.yaml.", str(audit)))

    validate_disclosure(
        root,
        str(documentation.get("human_entrypoint", "README.md")),
        artifact,
        moda,
        False,
        findings,
    )
    validate_disclosure(
        root,
        str(documentation.get("agent_entrypoint", "AGENTS.md")),
        artifact,
        moda,
        True,
        findings,
    )

    schema_path = schema_path or CANONICAL_SCHEMA
    try:
        schema = json.loads(schema_path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        findings.append(Finding("error", "missing-schema", "MODA JSON Schema is missing.", str(schema_path)))
    except json.JSONDecodeError as exc:
        findings.append(Finding("error", "invalid-schema", f"MODA JSON Schema is invalid JSON: {exc}", str(schema_path)))
    else:
        if isinstance(schema, dict):
            validate_schema_value(manifest, schema, "$", findings)
        else:
            findings.append(Finding("error", "invalid-schema-root", "MODA JSON Schema root must be an object.", str(schema_path)))

    return findings


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate deterministic MODA repository requirements.")
    parser.add_argument("root", nargs="?", default=".", help="Repository root to validate.")
    parser.add_argument("--schema", type=Path, help="Path to the MODA manifest JSON Schema.")
    parser.add_argument("--json", action="store_true", dest="json_output", help="Emit machine-readable findings.")
    args = parser.parse_args()

    root = Path(args.root).resolve()
    findings = validate_repository(root, args.schema.resolve() if args.schema else None)
    if args.json_output:
        print(json.dumps([asdict(item) for item in findings], indent=2))
    elif findings:
        for item in findings:
            location = f" [{item.path}]" if item.path else ""
            print(f"{item.severity.upper()} {item.code}{location}: {item.message}")
    else:
        print("MODA validation passed.")
    return 1 if any(item.severity == "error" for item in findings) else 0


if __name__ == "__main__":
    sys.exit(main())
