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
            candidate = Path(directory) / "moda"
            shutil.copytree(ROOT, candidate, ignore=shutil.ignore_patterns("__pycache__"))
            manifest = candidate / "moda.yaml"
            manifest.write_text(
                manifest.read_text(encoding="utf-8").replace('  kind: "framework"', '  kind: "project"'),
                encoding="utf-8",
            )
            findings = validate_repository(candidate)
        self.assertTrue(any(item.code == "schema-enum" for item in findings))

    def test_skill_manifest_pins_framework_and_knowledge(self) -> None:
        manifest = yaml.safe_load((ROOT / "skill" / "manifest.yaml").read_text(encoding="utf-8"))
        self.assertEqual("1.0.0", manifest["skill"]["version"])
        self.assertEqual("^1.0.0", manifest["framework"]["compatibility"])
        self.assertRegex(manifest["knowledge"]["snapshot"], r"^[0-9a-f]{40}$")
        self.assertFalse(manifest["installation"]["automatic_migration"])


if __name__ == "__main__":
    unittest.main()
