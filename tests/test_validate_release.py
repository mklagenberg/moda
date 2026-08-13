from __future__ import annotations

import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scripts.validate_release import (  # noqa: E402
    render_handoff,
    validate_bump,
    validate_evidence_paths,
    validate_release,
)


CONTENT_COMMIT = "c" * 40
RELEASE_COMMIT = "d" * 40


class ValidateReleaseTests(unittest.TestCase):
    def copy_repository(self, directory: str) -> Path:
        candidate = Path(directory) / "moda"
        shutil.copytree(ROOT, candidate, ignore=shutil.ignore_patterns("__pycache__"))
        return candidate

    def write_yaml(self, path: Path, value: dict) -> None:
        path.write_text(yaml.safe_dump(value, sort_keys=False), encoding="utf-8")

    def make_release_ready_fixture(self, candidate: Path) -> None:
        manifest_path = candidate / "moda.yaml"
        manifest = yaml.safe_load(manifest_path.read_text(encoding="utf-8"))
        manifest["adoption"]["claim_stage"] = "verified"
        manifest["adoption"]["conformance_result"] = "conformant"
        manifest["synchronization"]["state"] = "current"
        manifest["synchronization"]["reason"] = "Release evidence is synchronized."
        self.write_yaml(manifest_path, manifest)

        profile_path = candidate / manifest["conformance"]["profile"]
        profile = yaml.safe_load(profile_path.read_text(encoding="utf-8"))
        profile["assessment"]["claim_stage"] = "verified"
        profile["assessment"]["result"] = "conformant"
        self.write_yaml(profile_path, profile)

        audit_path = candidate / manifest["conformance"]["latest_audit"]
        audit = yaml.safe_load(audit_path.read_text(encoding="utf-8"))
        audit["subject"]["commit"] = CONTENT_COMMIT
        audit["result"].update({
            "claim_stage": "verified",
            "conformance": "conformant",
            "critical_findings": 0,
            "major_findings": 0,
            "minor_findings": 0,
            "observations": 0,
        })
        audit["findings"] = []
        self.write_yaml(audit_path, audit)

        changelog_path = candidate / "CHANGELOG.md"
        changelog_path.write_text(
            changelog_path.read_text(encoding="utf-8").replace(
                "## [1.0.0] - Unreleased", "## [1.0.0] - 2026-08-12", 1
            ),
            encoding="utf-8",
        )

    def test_current_repository_is_not_release_ready(self) -> None:
        findings, _ = validate_release(
            ROOT, "1.0.0", "initial", CONTENT_COMMIT, RELEASE_COMMIT, check_git=False
        )
        codes = {item.code for item in findings}
        self.assertIn("release-sync-not-current", codes)
        self.assertIn("audit-content-mismatch", codes)
        self.assertIn("release-blocking-findings", codes)
        self.assertNotIn("undated-changelog-version", codes)
        self.assertIn("release-not-conformant", codes)

    def test_complete_repository_controlled_gates_pass(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            candidate = self.copy_repository(directory)
            self.make_release_ready_fixture(candidate)
            findings, description = validate_release(
                candidate,
                "1.0.0",
                "initial",
                CONTENT_COMMIT,
                RELEASE_COMMIT,
                check_git=False,
            )
        self.assertEqual([], findings, "\n".join(f"{item.code}: {item.message}" for item in findings))
        self.assertIn("First public contract", description or "")

    def test_semver_class_must_match_previous_release(self) -> None:
        self.assertEqual([], validate_bump("2.0.0", "major", "1.7.3"))
        findings = validate_bump("1.8.1", "minor", "1.7.3")
        self.assertTrue(any(item.code == "version-bump-mismatch" for item in findings))

    def test_release_commit_rejects_non_evidence_paths(self) -> None:
        findings = validate_evidence_paths([
            "audits/moda/release.yaml",
            "conformance/moda.yaml",
            "moda.yaml",
            "skill/manifest.yaml",
            "SPEC.md",
        ])
        self.assertEqual(["SPEC.md"], [item.path for item in findings])

    def test_handoff_contains_exact_human_creation_fields(self) -> None:
        handoff = render_handoff("MODA", "1.1.0", "main", RELEASE_COMMIT, "Compatible capability release.")
        for expected in ("v1.1.0", "`main`", RELEASE_COMMIT, "MODA v1.1.0", "Compatible capability release."):
            self.assertIn(expected, handoff)

    def test_cli_withholds_handoff_without_remote_gate_confirmation(self) -> None:
        result = subprocess.run(
            [
                sys.executable,
                str(ROOT / "scripts" / "validate_release.py"),
                "--root", str(ROOT),
                "--version", "1.0.0",
                "--bump", "initial",
                "--content-commit", CONTENT_COMMIT,
                "--release-commit", RELEASE_COMMIT,
                "--skip-git",
                "--handoff",
                "--json",
            ],
            check=False,
            capture_output=True,
            text=True,
        )
        self.assertNotEqual(0, result.returncode)
        self.assertIn("remote-gates-not-confirmed", result.stdout)


if __name__ == "__main__":
    unittest.main()
