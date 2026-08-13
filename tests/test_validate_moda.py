from __future__ import annotations

import sys
import shutil
import tempfile
import unittest
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scripts.validate_moda import validate_repository  # noqa: E402


class ValidateModaTests(unittest.TestCase):
    def copy_repository(self, directory: str) -> Path:
        candidate = Path(directory) / "moda"
        shutil.copytree(ROOT, candidate, ignore=shutil.ignore_patterns("__pycache__"))
        return candidate

    def latest_audit_path(self, candidate: Path) -> Path:
        manifest = yaml.safe_load((candidate / "moda.yaml").read_text(encoding="utf-8"))
        return candidate / manifest["conformance"]["latest_audit"]

    def test_repository_is_structurally_valid(self) -> None:
        errors = [finding for finding in validate_repository(ROOT) if finding.severity == "error"]
        self.assertEqual([], errors, "\n".join(f"{item.code}: {item.message}" for item in errors))

    def test_minimal_example_is_structurally_valid(self) -> None:
        example = ROOT / "examples" / "minimal-methodology"
        errors = [finding for finding in validate_repository(example) if finding.severity == "error"]
        self.assertEqual([], errors, "\n".join(f"{item.code}: {item.message}" for item in errors))

    def test_missing_manifest_is_reported(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            findings = validate_repository(Path(directory))
        self.assertTrue(any(item.code == "missing-file" for item in findings))

    def test_manifest_schema_violation_is_reported(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            candidate = self.copy_repository(directory)
            manifest = candidate / "moda.yaml"
            manifest.write_text(
                manifest.read_text(encoding="utf-8").replace('  kind: "framework"', '  kind: "project"'),
                encoding="utf-8",
            )
            findings = validate_repository(candidate)
        self.assertTrue(any(item.code == "schema-enum" for item in findings))

    def test_prerelease_and_build_semver_are_accepted(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            candidate = self.copy_repository(directory)
            manifest = candidate / "moda.yaml"
            manifest.write_text(
                manifest.read_text(encoding="utf-8")
                .replace('  version: "1.0.0"', '  version: "1.0.0-rc.1+fixture"', 1)
                .replace('    version: "1.0.0"', '    version: "1.0.0-rc.1+fixture"'),
                encoding="utf-8",
            )
            conformance = candidate / "conformance" / "moda.yaml"
            conformance.write_text(
                conformance.read_text(encoding="utf-8").replace(
                    '  version: "1.0.0"', '  version: "1.0.0-rc.1+fixture"'
                ),
                encoding="utf-8",
            )
            audit = self.latest_audit_path(candidate)
            audit.write_text(
                audit.read_text(encoding="utf-8").replace(
                    '  version: "1.0.0"', '  version: "1.0.0-rc.1+fixture"', 1
                ),
                encoding="utf-8",
            )
            errors = [finding for finding in validate_repository(candidate) if finding.severity == "error"]
        self.assertFalse(any(item.code in {"invalid-semver", "invalid-package-version", "schema-pattern"} for item in errors))

    def test_placeholder_commit_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            candidate = self.copy_repository(directory)
            manifest = candidate / "moda.yaml"
            value = yaml.safe_load(manifest.read_text(encoding="utf-8"))
            value["moda"]["verified_commit"] = "0" * 40
            manifest.write_text(yaml.safe_dump(value, sort_keys=False), encoding="utf-8")
            findings = validate_repository(candidate)
        self.assertTrue(any(item.code == "invalid-commit" for item in findings))

    def test_missing_literal_changelog_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            candidate = self.copy_repository(directory)
            (candidate / "CHANGELOG.md").unlink()
            findings = validate_repository(candidate)
        self.assertTrue(any(item.code == "missing-literal-artifact" and item.path == "CHANGELOG.md" for item in findings))

    def test_missing_change_management_documentation_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            candidate = self.copy_repository(directory)
            manifest = candidate / "moda.yaml"
            manifest.write_text(
                manifest.read_text(encoding="utf-8").replace(
                    '  change_management: "docs/change-management.md"\n', "", 1
                ),
                encoding="utf-8",
            )
            findings = validate_repository(candidate)
        self.assertTrue(any(item.code in {"missing-key", "schema-required"} for item in findings))

    def test_missing_validation_policy_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            candidate = self.copy_repository(directory)
            manifest = candidate / "moda.yaml"
            manifest.write_text(
                manifest.read_text(encoding="utf-8").replace(
                    '  validation: "docs/validation-and-repair.md"\n', "", 1
                ),
                encoding="utf-8",
            )
            findings = validate_repository(candidate)
        self.assertTrue(any(item.code in {"missing-key", "schema-required"} for item in findings))

    def test_claude_entrypoint_must_point_to_canonical_agents_file(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            candidate = self.copy_repository(directory)
            (candidate / "CLAUDE.md").write_text("# Independent instructions\n", encoding="utf-8")
            findings = validate_repository(candidate)
        self.assertTrue(any(item.code == "invalid-host-shim" for item in findings))

    def test_broken_markdown_evidence_anchor_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            candidate = self.copy_repository(directory)
            conformance = candidate / "conformance" / "moda.yaml"
            conformance.write_text(
                conformance.read_text(encoding="utf-8").replace(
                    '"SPEC.md#1-purpose"', '"SPEC.md#missing-anchor"', 1
                ),
                encoding="utf-8",
            )
            findings = validate_repository(candidate)
        self.assertTrue(any(item.code == "broken-evidence-anchor" for item in findings))

    def test_invalid_control_status_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            candidate = self.copy_repository(directory)
            conformance = candidate / "conformance" / "moda.yaml"
            conformance.write_text(
                conformance.read_text(encoding="utf-8").replace('status: "satisfied"', 'status: "optimistic"', 1),
                encoding="utf-8",
            )
            findings = validate_repository(candidate)
        self.assertTrue(any(item.code == "invalid-control-status" for item in findings))

    def test_audit_finding_count_mismatch_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            candidate = self.copy_repository(directory)
            audit = self.latest_audit_path(candidate)
            value = yaml.safe_load(audit.read_text(encoding="utf-8"))
            value["result"]["major_findings"] = 1
            audit.write_text(yaml.safe_dump(value, sort_keys=False), encoding="utf-8")
            findings = validate_repository(candidate)
        self.assertTrue(any(item.code == "audit-count-mismatch" for item in findings))

    def test_git_package_with_pinned_provenance_is_accepted(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            candidate = self.copy_repository(directory)
            manifest = candidate / "moda.yaml"
            manifest.write_text(
                manifest.read_text(encoding="utf-8").replace(
                    "installations: []",
                    """  remote-adapter:\n    role: \"host-adapter\"\n    version: \"1.0.0\"\n    source_kind: \"git\"\n    source:\n      repository: \"https://example.invalid/moda-adapter\"\n      ref: \"v1.0.0\"\n      commit: \"909c83cd5b82d5840b40eb87f6b2ed4885a71c94\"\n\ninstallations: []""",
                    1,
                ),
                encoding="utf-8",
            )
            findings = validate_repository(candidate)
        self.assertFalse(any(item.code in {"invalid-remote-source", "invalid-remote-commit", "broken-package-source"} for item in findings))

    def test_skill_manifest_pins_framework_and_knowledge(self) -> None:
        manifest = yaml.safe_load((ROOT / "skill" / "manifest.yaml").read_text(encoding="utf-8"))
        self.assertEqual("1.0.0", manifest["skill"]["version"])
        self.assertEqual("^1.0.0", manifest["framework"]["compatibility"])
        self.assertRegex(manifest["knowledge"]["snapshot"], r"^[0-9a-f]{40}$")
        self.assertFalse(manifest["installation"]["automatic_migration"])


if __name__ == "__main__":
    unittest.main()
