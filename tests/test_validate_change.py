from __future__ import annotations

import shutil
import tempfile
import unittest
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]

from scripts.validate_change import parse_name_status, validate_changes, validate_impact  # noqa: E402


IMPACT = Path("changes/0011-specification-driven-change-control/impact.yaml")
AGENT_IMPACT = Path("changes/0013-agent-validation-and-release-gates/impact.yaml")


class ValidateChangeTests(unittest.TestCase):
    def copy_repository(self, directory: str) -> Path:
        candidate = Path(directory) / "moda"
        shutil.copytree(ROOT, candidate, ignore=shutil.ignore_patterns("__pycache__"))
        return candidate

    def current_changed_files(self, root: Path) -> set[str]:
        impact = yaml.safe_load((root / IMPACT).read_text(encoding="utf-8"))
        changed = {IMPACT.as_posix(), "changes/0011-specification-driven-change-control/proposal.md"}
        for surface in impact["affected"].values():
            if surface["status"] == "updated":
                changed.update(surface["paths"])
        return changed

    def declared_changed_files(self, root: Path, impact_path: Path) -> set[str]:
        impact = yaml.safe_load((root / impact_path).read_text(encoding="utf-8"))
        changed = {impact_path.as_posix(), (impact_path.parent / "proposal.md").as_posix()}
        for surface in impact["affected"].values():
            if surface["status"] == "updated":
                changed.update(surface["paths"])
        return changed

    def test_current_change_set_is_valid(self) -> None:
        changed = self.current_changed_files(ROOT)
        errors = [finding for finding in validate_impact(ROOT, ROOT / IMPACT, changed) if finding.severity == "error"]
        self.assertEqual([], errors, "\n".join(f"{item.code}: {item.message}" for item in errors))

    def test_agent_release_change_set_is_valid(self) -> None:
        changed = self.declared_changed_files(ROOT, AGENT_IMPACT)
        errors = [finding for finding in validate_impact(ROOT, ROOT / AGENT_IMPACT, changed) if finding.severity == "error"]
        self.assertEqual([], errors, "\n".join(f"{item.code}: {item.message}" for item in errors))

    def test_claude_entrypoint_is_a_protected_surface(self) -> None:
        findings = validate_changes(ROOT, {"CLAUDE.md"})
        self.assertTrue(any(item.code == "missing-change-set" for item in findings))

    def test_protected_change_without_change_set_is_rejected(self) -> None:
        findings = validate_changes(ROOT, {"SPEC.md"})
        self.assertTrue(any(item.code == "missing-change-set" for item in findings))

    def test_impact_without_proposal_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            candidate = self.copy_repository(directory)
            (candidate / IMPACT).with_name("proposal.md").unlink()
            findings = validate_impact(candidate, candidate / IMPACT, self.current_changed_files(candidate))
        self.assertTrue(any(item.code == "missing-change-proposal" for item in findings))

    def test_changed_specification_cannot_be_declared_reviewed(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            candidate = self.copy_repository(directory)
            impact_path = candidate / IMPACT
            data = yaml.safe_load(impact_path.read_text(encoding="utf-8"))
            data["affected"]["specification"] = {
                "status": "reviewed",
                "paths": ["SPEC.md"],
                "rationale": "Claimed unchanged despite the diff.",
            }
            impact_path.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")
            findings = validate_impact(candidate, impact_path, self.current_changed_files(candidate) | {"SPEC.md"})
        codes = {item.code for item in findings}
        self.assertIn("changed-surface-not-updated", codes)
        self.assertIn("normative-spec-not-updated", codes)

    def test_updated_path_absent_from_diff_is_rejected(self) -> None:
        changed = self.current_changed_files(ROOT) - {"skill/SKILL.md", "skill/references/change-workflow.md"}
        findings = validate_impact(ROOT, ROOT / IMPACT, changed)
        self.assertTrue(any(item.code == "updated-path-not-changed" and "skill" in item.message.lower() for item in findings))

    def test_protected_path_not_listed_by_updated_surface_is_rejected(self) -> None:
        changed = self.current_changed_files(ROOT) | {"skill/references/unlisted-workflow.md"}
        findings = validate_impact(ROOT, ROOT / IMPACT, changed)
        self.assertTrue(any(item.code == "uncovered-changed-path" for item in findings))

    def test_reviewed_surface_requires_rationale(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            candidate = self.copy_repository(directory)
            impact_path = candidate / IMPACT
            data = yaml.safe_load(impact_path.read_text(encoding="utf-8"))
            del data["affected"]["upgrade"]["rationale"]
            impact_path.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")
            findings = validate_impact(candidate, impact_path, self.current_changed_files(candidate))
        self.assertTrue(any(item.code == "missing-surface-rationale" for item in findings))

    def test_structural_change_requires_decision_update(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            candidate = self.copy_repository(directory)
            impact_path = candidate / IMPACT
            data = yaml.safe_load(impact_path.read_text(encoding="utf-8"))
            data["affected"]["decisions"] = {
                "status": "reviewed",
                "paths": ["decisions/"],
                "rationale": "Incorrectly claimed no decision change.",
            }
            impact_path.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")
            findings = validate_impact(candidate, impact_path, self.current_changed_files(candidate))
        self.assertTrue(any(item.code == "missing-structural-decision" for item in findings))

    def test_security_behavior_requires_skill_update(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            candidate = self.copy_repository(directory)
            impact_path = candidate / IMPACT
            data = yaml.safe_load(impact_path.read_text(encoding="utf-8"))
            data["triggers"]["security_behavior"] = True
            data["affected"]["skill"] = {
                "status": "reviewed",
                "paths": ["skill/"],
                "rationale": "Incorrectly claimed no operational effect.",
            }
            impact_path.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")
            changed = self.current_changed_files(candidate) - {"skill/SKILL.md", "skill/references/change-workflow.md"}
            findings = validate_impact(candidate, impact_path, changed)
        self.assertTrue(any(item.code == "security-skill-not-updated" for item in findings))

    def test_rename_parser_includes_old_and_new_paths(self) -> None:
        changed = parse_name_status("R100\tdocs/old.md\tdocs/new.md\nM\tSPEC.md\n")
        self.assertEqual({"docs/old.md", "docs/new.md", "SPEC.md"}, changed)

    def test_unknown_change_field_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            candidate = self.copy_repository(directory)
            impact_path = candidate / IMPACT
            data = yaml.safe_load(impact_path.read_text(encoding="utf-8"))
            data["change"]["invented"] = True
            impact_path.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")
            findings = validate_impact(candidate, impact_path, self.current_changed_files(candidate))
        self.assertTrue(any(item.code == "unexpected-change-field" for item in findings))


if __name__ == "__main__":
    unittest.main()
