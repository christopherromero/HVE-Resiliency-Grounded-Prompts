"""Regression tests for conditional review, promotion, report coverage, and preflight."""

from __future__ import annotations

import copy
import io
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import yaml

from validate_assessment_report import BLOCKER_FIELDS, main, validate_report, validate_resolution_record

ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = ROOT / "grounding/governance/templates/code-level-resiliency-assessment-template.md"


class ConditionalReviewTests(unittest.TestCase):
    """Keep unknowns visible without allowing them to become executable defects."""

    def setUp(self) -> None:
        self.pending = {
            "finding_id": "F-001", "finding_status": "conditional", "control_ids": ["CTRL-1"],
            "evidence_refs": ["FIXTURE-SOURCE-001"], "implementation_eligibility": "blocked",
            "condition": {"description": "Endpoint is remote-only", "outcome_if_confirmed": "Regional readiness loss",
                          "evidence_required": ["Effective endpoint binding"], "evidence_that_rules_out": ["Local endpoint binding"],
                          "evidence_owner": "Fixture owner", "verification_status": "unresolved"},
            "finding_confidence": {"level": "high", "rationale": "Source establishes readiness coupling"},
            "verification": {"disposition": "pending", "evidence_validated": False, "evidence_refs": []},
            "resolution_history": [],
        }
        self.priority = {"value": "P1", "policy_id": "AA-REMEDIATION-PRIORITY", "policy_version": "1.3.0",
                         "rule_id": "FIXTURE-RULE-001", "rationale": "Fixture governed regional impact"}
        blocker = {key: "Fixture fact or explicit unknown with resolution request" for key in BLOCKER_FIELDS}
        blocker.update(control_id="CTRL-1", available_evidence=["FIXTURE-SOURCE-001"], conditional_finding_ids=["F-001"])
        self.record = {
            "policy_id": "CONDITIONAL-FINDING-RESOLUTION", "policy_version": "1.0.0",
            "review_artifact": "fixture-review-v1.md", "review_revision": "review-v1",
            "plan_artifact": "fixture-plan-v1.md", "plan_review_revision": "review-v1",
            "plan_review_artifact": "fixture-review-v1.md",
            "findings": [self.pending, {"finding_id": "F-002", "finding_status": "verified", "control_ids": ["CTRL-2"], "evidence_refs": ["FIXTURE-SOURCE-002"]}],
            "controls": [{"control_id": "CTRL-1", "status": "not_assessed", "assessment_mode": "conditional", "outcome_if_confirmed": "non_compliant"},
                         {"control_id": "CTRL-2", "status": "non_compliant"}],
            "changes": [{"change_id": "CHANGE-002", "finding_ids": ["F-002"], "priority": self.priority, "implementation_allowed": True}],
            "conditional_proposals": [{"proposal_id": "PROPOSAL-001", "finding_ids": ["F-001"], "status": "conditional_blocked",
                                       "implementation_allowed": False, "priority_if_confirmed": self.priority,
                                       "targets": [{"repository_path": "fixture/Readiness.java", "symbol": "isReady", "source_language": "java", "target_kind": "application",
                                                    "illustrative_code_status": "generated", "illustrative_code": "return localReady;"}]}],
            "not_assessed_register": [blocker], "conditional_register_included": True,
            "evidence_gaps_included": True, "omission_reason": "", "confirmed_finding_ids": ["F-002"],
            "pending_conditional_ids": ["F-001"], "matrix_finding_ids": ["F-002"], "roadmap_change_ids": ["CHANGE-002"],
            "testing_output": {"mode": "full", "show_test_code": True},
        }

    def report(self, record: dict | None = None) -> str:
        record = self.record if record is None else record
        text = TEMPLATE.read_text(encoding="utf-8")
        overview = f"Confirmed findings in this report: {len(record['confirmed_finding_ids'])}\nPending conditional findings: {len(record['pending_conditional_ids'])}\n"
        text = text.replace("<!-- content:assessment-overview:start -->", "<!-- content:assessment-overview:start -->\n" + overview)
        verified = "\n".join(f"<!-- finding:{identifier} -->" for identifier in record["confirmed_finding_ids"])
        text = text.replace("<!-- content:resiliency-recommendations:start -->", "<!-- content:resiliency-recommendations:start -->\n" + verified)
        evidence = ""
        if record["conditional_register_included"]:
            evidence += "### Conditional Findings Pending Verification\n"
            evidence += "\n".join(f"<!-- conditional-finding:{identifier} -->" for identifier in record["pending_conditional_ids"])
            evidence += "\nIllustrative proposal only.\n```java\nreturn localReady;\n```\n"
        if record["evidence_gaps_included"]:
            evidence += "### Not-Assessed Control Register\n"
            evidence += "\n".join(f"<!-- not-assessed-control:{row['control_id']} -->" for row in record["not_assessed_register"])
        if not record["conditional_register_included"] or not record["evidence_gaps_included"]:
            evidence += "Review coverage limitation: " + record["omission_reason"] + "\n"
        text = text.replace("<!-- content:evidence-gap-analysis:start -->", "<!-- content:evidence-gap-analysis:start -->\n" + evidence)
        matrix = "\n".join(f"<!-- matrix-finding:{identifier} -->" for identifier in record["matrix_finding_ids"])
        text = text.replace("<!-- content:full-finding-matrix:start -->", "<!-- content:full-finding-matrix:start -->\n" + matrix)
        roadmap = "\n".join(f"<!-- roadmap-change:{identifier} -->" for identifier in record["roadmap_change_ids"])
        text = text.replace("<!-- content:implementation-roadmap:start -->", "<!-- content:implementation-roadmap:start -->\n" + roadmap)
        return text + "\n<!-- conditional-review-manifest\n" + json.dumps(record, indent=2) + "\n-->\n"

    def resolve(self, disposition: str = "confirmed") -> None:
        self.pending["finding_status"] = "verified" if disposition == "confirmed" else "ruled_out"
        self.pending["condition"]["verification_status"] = disposition
        self.pending["verification"] = {"disposition": disposition, "evidence_validated": True, "reviewed_by": "Fixture reviewer",
                                        "reviewed_at": "2026-11-05T12:00:00Z", "rationale": "Validated fixture evidence",
                                        "evidence_refs": ["FIXTURE-CONFIG-003"]}
        self.pending["resolution_history"] = [{"previous_finding_status": "conditional", "parent_review_artifact": "fixture-review-v1.md", "evidence_refs": ["FIXTURE-CONFIG-003"]}]
        self.pending["implementation_eligibility"] = "requires_step_3a_approval" if disposition == "confirmed" else "excluded"
        self.record["conditional_proposals"] = []
        self.record["pending_conditional_ids"] = []
        self.record["review_revision"] = "review-v2"
        self.record["plan_review_revision"] = "review-v2"
        if disposition == "confirmed":
            self.record["controls"][0].update(status="non_compliant", assessment_mode="verified")
            self.record["not_assessed_register"] = []
            self.record["changes"].append({"change_id": "CHANGE-001", "finding_ids": ["F-001"], "priority": self.priority, "implementation_allowed": False})
            for field in ("confirmed_finding_ids", "matrix_finding_ids"):
                self.record[field].append("F-001")
        else:
            self.record["controls"][0]["assessment_mode"] = "evidence_required"
            self.record["not_assessed_register"][0]["conditional_finding_ids"] = []

    def test_pending_report_and_verified_scope_pass(self) -> None:
        original = copy.deepcopy(self.record)
        self.assertEqual(validate_resolution_record(self.record, ["CHANGE-002"]), [])
        self.assertEqual(validate_report(self.report(), True), [])
        self.assertEqual(self.record, original)

    def test_promotion_moves_to_main_report_but_still_requires_approval(self) -> None:
        self.resolve()
        self.assertEqual(validate_report(self.report(), True), [])
        self.assertTrue(validate_resolution_record(self.record, ["CHANGE-001"]))
        self.record["changes"][-1]["implementation_allowed"] = True
        self.assertEqual(validate_resolution_record(self.record, ["CHANGE-001"]), [])
        self.assertNotIn("<!-- conditional-finding:F-001 -->", self.report())
        self.assertIn("<!-- finding:F-001 -->", self.report())

    def test_ruled_out_remains_historical_not_compliant(self) -> None:
        self.resolve("ruled_out")
        self.assertEqual(validate_report(self.report(), True), [])
        self.assertEqual(self.record["controls"][0]["status"], "not_assessed")
        self.assertTrue(validate_resolution_record(self.record, ["PROPOSAL-001"]))

    def test_deferred_remains_blocked(self) -> None:
        self.pending["verification"]["disposition"] = "deferred"
        self.assertEqual(validate_report(self.report(), True), [])
        self.assertTrue(validate_resolution_record(self.record, ["PROPOSAL-001"]))

    def test_low_confidence_and_missing_condition_fail(self) -> None:
        self.pending["finding_confidence"]["level"] = "low"
        self.assertTrue(validate_resolution_record(self.record))
        self.pending["finding_confidence"]["level"] = "high"
        self.pending["condition"]["evidence_that_rules_out"] = []
        self.assertTrue(validate_resolution_record(self.record))

    def test_pending_cannot_be_executable_or_counted_as_verified(self) -> None:
        self.record["changes"][0]["finding_ids"] = ["F-001"]
        self.assertTrue(validate_resolution_record(self.record, ["CHANGE-002"]))
        self.record["confirmed_finding_ids"].append("F-001")
        self.record["matrix_finding_ids"].append("F-001")
        self.assertTrue(validate_report(self.report(), True))

    def test_missing_blocker_or_unexplained_unknown_fails(self) -> None:
        original = self.record["not_assessed_register"]
        self.record["not_assessed_register"] = []
        self.assertTrue(validate_resolution_record(self.record))
        self.record["not_assessed_register"] = original
        del original[0]["missing_input"]
        self.assertTrue(validate_resolution_record(self.record))

    def test_duplicate_ids_and_bad_links_fail(self) -> None:
        self.record["findings"].append(copy.deepcopy(self.pending))
        self.assertTrue(validate_resolution_record(self.record))
        self.record["findings"].pop()
        self.record["not_assessed_register"][0]["conditional_finding_ids"] = []
        self.assertTrue(validate_resolution_record(self.record))

    def test_missing_and_discovery_only_proposals(self) -> None:
        target = self.record["conditional_proposals"][0]["targets"][0]
        target["illustrative_code"] = ""
        self.assertTrue(validate_resolution_record(self.record))
        target.update(illustrative_code_status="targeted_discovery_required", discovery_required_reason="Endpoint API unresolved", unresolved_inputs=["Approved endpoint contract"])
        self.assertEqual(validate_resolution_record(self.record), [])
        del target["unresolved_inputs"]
        self.assertTrue(validate_resolution_record(self.record))

    def test_code_omission_and_wrong_section_fail(self) -> None:
        self.assertTrue(validate_report(self.report().replace("return localReady;\n```", "\n```"), True))
        moved = self.report().replace("<!-- conditional-finding:F-001 -->", "", 1)
        moved = moved.replace("<!-- content:resiliency-recommendations:start -->", "<!-- content:resiliency-recommendations:start -->\n<!-- conditional-finding:F-001 -->")
        self.assertTrue(validate_report(moved, True))

    def test_priority_filter_does_not_hide_pending(self) -> None:
        for field in ("confirmed_finding_ids", "matrix_finding_ids", "roadmap_change_ids"):
            self.record[field] = []
        self.assertEqual(validate_report(self.report(), True), [])

    def test_hidden_registers_require_notice_and_keep_obligations(self) -> None:
        self.record.update(conditional_register_included=False, evidence_gaps_included=False, omission_reason="Explicit fixture report preferences")
        self.assertEqual(validate_report(self.report(), True), [])
        self.assertTrue(validate_report(self.report().replace("Review coverage limitation:", "Hidden:"), True))
        self.record["not_assessed_register"] = []
        self.assertTrue(validate_report(self.report(), True))

    def test_stale_plan_and_approval_without_evidence_fail(self) -> None:
        self.resolve()
        self.record["plan_review_revision"] = "review-v1"
        self.assertTrue(validate_resolution_record(self.record))
        self.record["plan_review_revision"] = "review-v2"
        self.pending["verification"]["evidence_validated"] = False
        self.assertTrue(validate_resolution_record(self.record))
        self.pending["verification"]["evidence_validated"] = True
        self.pending["resolution_history"] = []
        self.assertTrue(validate_resolution_record(self.record))

    def test_template_legacy_and_new_schema_requirement(self) -> None:
        template = TEMPLATE.read_text(encoding="utf-8")
        self.assertEqual(validate_report(template), [])
        self.assertTrue(validate_report(template, True))
        self.assertTrue(validate_report("schema_id: CODE-LEVEL-RESILIENCY-ASSESSMENT-REPORT\nschema_version: \"1.14.0\"\n" + template))

    def test_invalid_json_and_duplicate_keys_fail(self) -> None:
        report = self.report()
        self.assertTrue(validate_report(report.replace('"policy_id":', '"policy_id": null, "policy_id":', 1), True))
        self.assertTrue(validate_report(report + "\n<!-- conditional-review-manifest\n{}\n-->\n", True))
        self.assertTrue(validate_report(report.replace('"policy_id":', '"policy_id"', 1), True))

    def test_malformed_records_fail_without_crashing(self) -> None:
        for malformed in (None, [], {}, {"findings": [None], "controls": [False]}):
            with self.subTest(malformed=malformed):
                self.assertTrue(validate_resolution_record(malformed))

    def test_exact_plan_assessment_path_must_match(self) -> None:
        self.record["plan_review_artifact"] = "different-service-review.md"
        self.assertTrue(validate_resolution_record(self.record, ["CHANGE-002"]))

    def test_rendered_blocker_rows_are_required(self) -> None:
        self.assertTrue(validate_report(self.report().replace("<!-- not-assessed-control:CTRL-1 -->", ""), True))

    def test_illustrative_code_requires_fenced_block(self) -> None:
        report = self.report().replace("```java\nreturn localReady;\n```", "return localReady;")
        self.assertTrue(validate_report(report, True))

    def test_counts_are_exact_not_prefix_matches(self) -> None:
        report = self.report().replace("Confirmed findings in this report: 1", "Confirmed findings in this report: 10")
        self.assertTrue(validate_report(report, True))

    def test_hidden_testing_preserves_obligations_without_rendering_test_code(self) -> None:
        target = self.record["conditional_proposals"][0]["targets"][0]
        target["target_kind"] = "test"
        self.record["testing_output"] = {"mode": "hidden", "show_test_code": False}
        report = self.report().replace("```java\nreturn localReady;\n```", "")
        self.assertEqual(validate_report(report, True), [])
        target["illustrative_code"] = ""
        self.assertTrue(validate_resolution_record(self.record))

    def test_testing_preferences_cannot_hide_application_code(self) -> None:
        self.record["testing_output"] = {"mode": "hidden", "show_test_code": False}
        report = self.report().replace("```java\nreturn localReady;\n```", "")
        self.assertTrue(validate_report(report, True))

    def test_malformed_nested_fields_fail_without_crashing(self) -> None:
        for field in ("proposals", "targets", "controls"):
            with self.subTest(field=field):
                record = copy.deepcopy(self.record)
                if field == "proposals":
                    record["conditional_proposals"] = None
                elif field == "targets":
                    record["conditional_proposals"][0]["targets"] = None
                else:
                    record["findings"][0]["control_ids"] = None
                self.assertTrue(validate_report(self.report(record), True))

    def test_cli_preflight_and_report_exit_codes(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            record_path = Path(directory) / "resolution.json"
            record_path.write_text(json.dumps(self.record), encoding="utf-8")
            report_path = Path(directory) / "report.md"
            report_path.write_text(self.report(), encoding="utf-8")
            with patch("sys.stdout", new_callable=io.StringIO):
                self.assertEqual(main([str(report_path), "--require-conditional-review"]), 0)
                self.assertEqual(main(["--resolution-record", str(record_path), "--selected-change-id", "CHANGE-002"]), 0)
                self.assertEqual(main(["--resolution-record", str(record_path), "--selected-change-id", "PROPOSAL-001"]), 1)
            record_path.write_text("{broken", encoding="utf-8")
            with patch("sys.stderr", new_callable=io.StringIO):
                self.assertEqual(main(["--resolution-record", str(record_path), "--selected-change-id", "CHANGE-002"]), 2)

    def test_governance_yaml_has_no_duplicate_keys(self) -> None:
        def check_node(node: yaml.Node, path: Path) -> None:
            if isinstance(node, yaml.MappingNode):
                keys = [key.value for key, _ in node.value]
                self.assertEqual(len(keys), len(set(keys)), f"Duplicate YAML key in {path}")
                for _, value in node.value:
                    check_node(value, path)
            elif isinstance(node, yaml.SequenceNode):
                for value in node.value:
                    check_node(value, path)

        for name in ("conditional-finding-policy.yml", "phase-handoff-schema.yml",
                     "resiliency-finding-qualification-policy.yml", "external-configuration-resolution-policy.yml",
                     "assessment-scope-schema.yml"):
            path = ROOT / "grounding/governance" / name
            for document in yaml.compose_all(path.read_text(encoding="utf-8")):
                if document is not None:
                    check_node(document, path)


if __name__ == "__main__":
    unittest.main()