#!/usr/bin/env python3
"""Validate report layout, conditional review, and authoritative implementation indexes.

Usage:
	python tools/validate_assessment_report.py REPORT --require-conditional-review
	python tools/validate_assessment_report.py --resolution-record INDEX.json \
		--selected-change-id CHANGE-AA-001
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

SECTIONS = [
	("assessment-overview", "Assessment Overview"),
	("resiliency-recommendations", "Resiliency-Focused Recommendations"),
	("non-resiliency-recommendations", "Non-Resiliency-Focused Recommendations"),
	("evidence-gap-analysis", "Repository and IaC Evidence Gap Analysis"),
	("full-finding-matrix", "Full Finding Matrix"),
	("standards-alignment", "Standards Alignment"),
	("implementation-roadmap", "Implementation Roadmap"),
	("appendix-traceability", "Appendix A: Traceability"),
]
POLICY_ID = "CONDITIONAL-FINDING-RESOLUTION"
MANIFEST = re.compile(r"<!-- conditional-review-manifest\s*\n(.*?)^-->\s*$", re.M | re.S)
BLOCKER_FIELDS = (
	"service", "failure_scenario", "potential_impact", "missing_input", "context_path",
	"context_authority", "blocking_reason", "policy_rule", "evidence_owner",
	"verification_request", "resolution_criteria",
)


def _text(value: Any) -> bool:
	return isinstance(value, str) and bool(value.strip())


def _resolved(value: Any) -> bool:
	return _text(value) and value.strip().lower() not in {
		"unknown", "pending", "todo", "not_available", "not provided", "unresolved",
	} and not value.strip().startswith("<")


def _object(value: Any, label: str, errors: list[str]) -> dict[str, Any]:
	if not isinstance(value, dict):
		errors.append(f"{label} must be an object")
		return {}
	return value


def _ids(value: Any, label: str, errors: list[str], *, empty: bool = False) -> list[str]:
	if not isinstance(value, list) or not all(_text(item) for item in value):
		errors.append(f"{label} must be a list of nonempty IDs")
		return []
	if (not empty and not value) or len(value) != len(set(value)):
		errors.append(f"{label} must contain unique IDs" + (" and cannot be empty" if not empty else ""))
	return value


def _rows(record: dict[str, Any], key: str, id_key: str, errors: list[str]) -> dict[str, dict[str, Any]]:
	rows = record.get(key)
	if not isinstance(rows, list):
		errors.append(f"{key} must be a list")
		return {}
	indexed = {}
	for row in rows:
		if not isinstance(row, dict) or not _text(row.get(id_key)):
			errors.append(f"{key} contains a record without {id_key}")
			continue
		identifier = row[id_key]
		if identifier in indexed:
			errors.append(f"duplicate {key} ID: {identifier}")
		indexed[identifier] = row
	return indexed


def _priority(value: Any, label: str, errors: list[str]) -> None:
	priority = _object(value, label, errors)
	if priority.get("value") not in ("P0", "P1", "P2", "P3") or not all(
		_resolved(priority.get(key)) for key in ("policy_id", "policy_version", "rule_id", "rationale")
	):
		errors.append(f"{label} requires a complete governed priority object")


def _verification(finding: dict[str, Any], label: str, errors: list[str]) -> None:
	condition = _object(finding.get("condition"), f"{label}.condition", errors)
	confidence = _object(finding.get("finding_confidence"), f"{label}.finding_confidence", errors)
	verification = _object(finding.get("verification"), f"{label}.verification", errors)
	for key in ("description", "outcome_if_confirmed", "evidence_owner"):
		if not _text(condition.get(key)):
			errors.append(f"{label}.condition.{key} is required")
	for key in ("evidence_required", "evidence_that_rules_out"):
		_ids(condition.get(key), f"{label}.condition.{key}", errors)
	if confidence.get("level") not in ("high", "medium") or not _text(confidence.get("rationale")):
		errors.append(f"{label} requires qualified high/medium confidence and rationale")
	history = finding.get("resolution_history")
	if not isinstance(history, list):
		errors.append(f"{label}.resolution_history must be a list")
		history = []
	status = finding.get("finding_status")
	if status == "conditional":
		if condition.get("verification_status") != "unresolved" or verification.get("disposition") not in ("pending", "deferred"):
			errors.append(f"{label} pending condition must remain unresolved")
		if verification.get("evidence_validated") is not False or finding.get("implementation_eligibility") != "blocked":
			errors.append(f"{label} pending conditional must be unverified and blocked")
		return
	expected = "confirmed" if status == "verified" else "ruled_out"
	if condition.get("verification_status") != expected or verification.get("disposition") != expected:
		errors.append(f"{label} requires matching {expected} condition and disposition")
	if verification.get("evidence_validated") is not True or not all(
		_resolved(verification.get(key)) for key in ("reviewed_by", "reviewed_at", "rationale")
	):
		errors.append(f"{label} resolution requires validated evidence and real reviewer metadata")
	_ids(verification.get("evidence_refs"), f"{label}.verification.evidence_refs", errors)
	if not history or not any(
		isinstance(entry, dict) and entry.get("previous_finding_status") == "conditional"
		and _resolved(entry.get("parent_review_artifact")) and entry.get("evidence_refs")
		for entry in history
	):
		errors.append(f"{label} resolution history must preserve prior conditional status, artifact, and evidence")
	eligibility = "requires_step_3a_approval" if status == "verified" else "excluded"
	if finding.get("implementation_eligibility") != eligibility:
		errors.append(f"{label} resolution cannot itself grant implementation approval")


def _proposal_targets(proposal: dict[str, Any], label: str, errors: list[str]) -> None:
	targets = proposal.get("targets")
	if not isinstance(targets, list) or not targets:
		errors.append(f"{label} requires illustrative targets or explicit discovery records")
		return
	for target in targets:
		target = _object(target, f"{label}.target", errors)
		status = target.get("illustrative_code_status")
		if status == "not_applicable":
			if not _text(target.get("reason")):
				errors.append(f"{label} not_applicable target requires a reason")
			continue
		if target.get("target_kind") not in ("application", "configuration", "test"):
			errors.append(f"{label} target_kind must be application, configuration, or test")
		if not all(_text(target.get(key)) for key in ("repository_path", "symbol", "source_language")):
			errors.append(f"{label} target requires path, symbol, and language")
		if status == "generated":
			if not _text(target.get("illustrative_code")):
				errors.append(f"{label} generated target requires concrete illustrative code")
		elif status == "targeted_discovery_required":
			if not _text(target.get("discovery_required_reason")):
				errors.append(f"{label} discovery target requires a specific reason")
			_ids(target.get("unresolved_inputs"), f"{label}.unresolved_inputs", errors)
		else:
			errors.append(f"{label} has an invalid illustrative_code_status")


def validate_resolution_record(record: Any, selected_change_ids: list[str] | None = None) -> list[str]:
	"""Check supplied authoritative indexes without verifying external facts or granting approval."""
	errors: list[str] = []
	record = _object(record, "resolution record", errors)
	if record.get("policy_id") != POLICY_ID or record.get("policy_version") != "1.0.0":
		errors.append("conditional policy identity/version missing or unsupported")
	for key in ("review_artifact", "review_revision", "plan_artifact", "plan_review_artifact", "plan_review_revision"):
		if not _resolved(record.get(key)):
			errors.append(f"{key} requires an exact authoritative path or revision")
	if record.get("review_artifact") != record.get("plan_review_artifact"):
		errors.append("plan references a different assessment artifact; Step 3A refresh required")
	if record.get("review_revision") != record.get("plan_review_revision"):
		errors.append("plan references a stale assessment revision; Step 3A refresh required")
	findings = _rows(record, "findings", "finding_id", errors)
	controls = _rows(record, "controls", "control_id", errors)
	changes = _rows(record, "changes", "change_id", errors)
	proposals = _rows(record, "conditional_proposals", "proposal_id", errors)
	blockers = _rows(record, "not_assessed_register", "control_id", errors)
	pending = set()
	finding_control_ids = {}
	for identifier, control in controls.items():
		if control.get("status") not in ("compliant", "non_compliant", "not_assessed", "not_applicable", "accepted_risk"):
			errors.append(f"{identifier} has an invalid control status")
	for identifier, finding in findings.items():
		status = finding.get("finding_status")
		if status not in ("verified", "conditional", "ruled_out"):
			errors.append(f"{identifier} has an invalid finding status")
		linked = _ids(finding.get("control_ids"), f"{identifier}.control_ids", errors)
		finding_control_ids[identifier] = linked
		_ids(finding.get("evidence_refs"), f"{identifier}.evidence_refs", errors)
		for control_id in linked:
			control = controls.get(control_id, {})
			if not control:
				errors.append(f"{identifier} references an unknown control: {control_id}")
			elif status == "verified" and control.get("status") != "non_compliant":
				errors.append(f"{identifier} verified finding must map to non_compliant controls")
			elif status == "conditional" and (
				control.get("status") != "not_assessed" or control.get("assessment_mode") != "conditional"
				or control.get("outcome_if_confirmed") != "non_compliant"
			):
				errors.append(f"{identifier} conditional control must preserve its unverified outcome")
		if status == "conditional":
			pending.add(identifier)
		if status in ("conditional", "ruled_out") or "condition" in finding or finding.get("resolution_history"):
			_verification(finding, identifier, errors)
	covered = set()
	for identifier, proposal in proposals.items():
		if proposal.get("status") != "conditional_blocked" or proposal.get("implementation_allowed") is not False:
			errors.append(f"{identifier} conditional proposal must remain blocked")
		if "priority" in proposal or "change_id" in proposal:
			errors.append(f"{identifier} conditional proposal cannot carry executable priority/change_id")
		linked = _ids(proposal.get("finding_ids"), f"{identifier}.finding_ids", errors)
		if not set(linked).issubset(pending):
			errors.append(f"{identifier} proposal must reference pending findings only")
		covered.update(linked)
		if "priority_if_confirmed" in proposal:
			_priority(proposal["priority_if_confirmed"], f"{identifier}.priority_if_confirmed", errors)
		elif not _text(proposal.get("governance_gap")):
			errors.append(f"{identifier} requires priority_if_confirmed or an explicit governance_gap")
		_proposal_targets(proposal, identifier, errors)
	if covered != pending:
		errors.append("every pending finding requires a full blocked conditional proposal")
	for identifier, change in changes.items():
		linked = _ids(change.get("finding_ids"), f"{identifier}.finding_ids", errors)
		if any(findings.get(finding_id, {}).get("finding_status") != "verified" for finding_id in linked):
			errors.append(f"{identifier} executable changes cannot reference pending, ruled-out, or unknown findings")
		if not isinstance(change.get("implementation_allowed"), bool):
			errors.append(f"{identifier}.implementation_allowed must be boolean")
		_priority(change.get("priority"), f"{identifier}.priority", errors)
	unassessed = {identifier for identifier, control in controls.items() if control.get("status") == "not_assessed"}
	if set(blockers) != unassessed:
		errors.append("not_assessed_register must account for every not_assessed control exactly once")
	for identifier, blocker in blockers.items():
		for field in BLOCKER_FIELDS:
			if not _text(blocker.get(field)):
				errors.append(f"{identifier} blocker requires {field}, or an explicit unknown reason")
		_ids(blocker.get("available_evidence"), f"{identifier}.available_evidence", errors, empty=True)
		linked = _ids(blocker.get("conditional_finding_ids"), f"{identifier}.conditional_finding_ids", errors, empty=True)
		expected = {finding_id for finding_id in pending if identifier in finding_control_ids[finding_id]}
		if set(linked) != expected:
			errors.append(f"{identifier} blocker conditional links do not reconcile")
	for identifier in selected_change_ids or []:
		change = changes.get(identifier)
		if change is None:
			errors.append(f"selected change is unknown or a non-executable conditional proposal: {identifier}")
		elif change.get("implementation_allowed") is not True:
			errors.append(f"selected change is blocked or lacks required plan approval: {identifier}")
	return errors


def _markers(text: str, kind: str) -> list[str]:
	return re.findall(r"<!-- " + re.escape(kind) + r":([A-Za-z0-9_-]+) -->", text)


def _unique_json(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
	result: dict[str, Any] = {}
	for key, value in pairs:
		if key in result:
			raise ValueError(f"duplicate JSON key: {key}")
		result[key] = value
	return result


def validate_report(text: str, require_conditional_review: bool = False) -> list[str]:
	"""Validate legacy layout and, for new reports, conditional-review reconciliation."""
	errors: list[str] = []
	positions = []
	for section_id, title in SECTIONS:
		marker = f"<!-- section:{section_id} -->"
		positions.append(text.find(marker))
		for value in (marker, f"## {title}", f"<!-- content:{section_id}:start -->", f"<!-- content:{section_id}:end -->"):
			if text.count(value) != 1:
				errors.append(f"missing or duplicate section element: {value}")
	if positions != sorted(positions) or min(positions) < 0:
		errors.append("section order")
	if text.count("[Back to Top](#top)") != len(SECTIONS):
		errors.append("back-to-top count")
	versions = re.findall(r"schema_id: CODE-LEVEL-RESILIENCY-ASSESSMENT-REPORT\s+schema_version: [\"']?(\d+)\.(\d+)\.(\d+)", text)
	required = require_conditional_review or any(tuple(map(int, version)) >= (1, 14, 0) for version in versions)
	manifests = list(MANIFEST.finditer(text))
	if len(manifests) != 1:
		if required or manifests or "<!-- conditional-review-manifest" in text:
			errors.append("exactly one valid conditional-review-manifest is required")
		if len(_markers(text, "finding")) != len(set(_markers(text, "finding"))):
			errors.append("duplicate finding markers")
		return errors
	try:
		record = json.loads(manifests[0].group(1), object_pairs_hook=_unique_json)
	except ValueError as error:
		return errors + [f"invalid conditional-review JSON: {error}"]
	errors.extend(validate_resolution_record(record))
	if not isinstance(record, dict):
		return errors
	visible = text[:manifests[0].start()] + text[manifests[0].end():]
	findings = _rows(record, "findings", "finding_id", errors)
	changes = _rows(record, "changes", "change_id", errors)
	proposals = _rows(record, "conditional_proposals", "proposal_id", errors)
	blockers = _rows(record, "not_assessed_register", "control_id", errors)
	confirmed = _ids(record.get("confirmed_finding_ids"), "confirmed_finding_ids", errors, empty=True)
	testing = _object(record.get("testing_output"), "testing_output", errors)
	if testing.get("mode") not in ("full", "summary", "roadmap_only", "hidden") or not isinstance(testing.get("show_test_code"), bool):
		errors.append("testing_output requires a supported mode and boolean show_test_code")
	pending = _ids(record.get("pending_conditional_ids"), "pending_conditional_ids", errors, empty=True)
	matrix = _ids(record.get("matrix_finding_ids"), "matrix_finding_ids", errors, empty=True)
	roadmap = _ids(record.get("roadmap_change_ids"), "roadmap_change_ids", errors, empty=True)
	if set(confirmed) != set(matrix) or any(findings.get(identifier, {}).get("finding_status") != "verified" for identifier in confirmed):
		errors.append("confirmed counts and matrix must contain the same selected verified findings only")
	if set(pending) != {identifier for identifier, finding in findings.items() if finding.get("finding_status") == "conditional"}:
		errors.append("pending_conditional_ids must account for all active conditional findings")
	for key in ("conditional_register_included", "evidence_gaps_included"):
		if not isinstance(record.get(key), bool):
			errors.append(f"{key} must be boolean")
	if (record.get("conditional_register_included") is False or record.get("evidence_gaps_included") is False) and not _text(record.get("omission_reason")):
		errors.append("hidden review registers require an explicit omission_reason")
	if not record.get("conditional_register_included") or not record.get("evidence_gaps_included"):
		if "Review coverage limitation:" not in visible:
			errors.append("hidden registers require a visible Review coverage limitation notice")
	for kind, expected in (("finding", confirmed), ("matrix-finding", matrix), ("roadmap-change", roadmap)):
		actual = _markers(visible, kind)
		if len(actual) != len(set(actual)) or set(actual) != set(expected):
			errors.append(f"{kind} markers do not reconcile with the validation index")
	for identifier in roadmap:
		change = changes.get(identifier, {})
		linked = _ids(change.get("finding_ids"), f"{identifier}.finding_ids", errors)
		if not change or not set(linked).intersection(confirmed):
			errors.append(f"roadmap change is not mapped to selected verified findings: {identifier}")
	expected_pending = pending if record.get("conditional_register_included") is True else []
	actual_pending = _markers(visible, "conditional-finding")
	if len(actual_pending) != len(set(actual_pending)) or set(actual_pending) != set(expected_pending):
		errors.append("conditional-finding markers do not reconcile with the pending register")
	region = visible.split("<!-- content:evidence-gap-analysis:start -->")[-1].split("<!-- content:evidence-gap-analysis:end -->")[0]
	expected_blockers = set(blockers) if record.get("evidence_gaps_included") is True else set()
	actual_blockers = _markers(visible, "not-assessed-control")
	if len(actual_blockers) != len(set(actual_blockers)) or set(actual_blockers) != expected_blockers:
		errors.append("rendered not-assessed rows do not reconcile with the blocker register")
	if set(_markers(region, "not-assessed-control")) != expected_blockers:
		errors.append("not-assessed blocker rows must appear inside Evidence Gap Analysis")
	if record.get("conditional_register_included") is True:
		if "### Conditional Findings Pending Verification" not in region:
			errors.append("conditional review section is required inside Evidence Gap Analysis")
		if set(_markers(region, "conditional-finding")) != set(expected_pending):
			errors.append("pending conditionals must appear only in Evidence Gap Analysis")
		fenced_blocks = re.findall(r"^```[^\n]*\n(.*?)^```[ \t]*$", region, re.M | re.S)
		for proposal in proposals.values():
			targets = proposal.get("targets")
			if not isinstance(targets, list):
				continue
			for target in targets:
				if isinstance(target, dict) and target.get("illustrative_code_status") == "generated":
					if target.get("target_kind") == "test" and (testing.get("mode") != "full" or testing.get("show_test_code") is not True):
						continue
					code = target.get("illustrative_code")
					if _text(code) and not any(code.replace("\r\n", "\n").strip() in block for block in fenced_blocks):
						errors.append("conditional illustrative code from Step 3A requires its fenced block")
		if pending and "Illustrative proposal only" not in region:
			errors.append("conditional proposals require the illustrative-only notice")
	if record.get("evidence_gaps_included") is True and "### Not-Assessed Control Register" not in region:
		errors.append("Not-Assessed Control Register heading is required")
	for label, count in (("Confirmed findings in this report", len(confirmed)), ("Pending conditional findings", len(pending))):
		if not re.search(re.escape(label) + r":\s*" + str(count) + r"(?=\s|$)", visible):
			errors.append(f"missing or incorrect visible count: {label}")
	return errors


def create_parser() -> argparse.ArgumentParser:
	parser = argparse.ArgumentParser(description=__doc__)
	parser.add_argument("report", nargs="?", type=Path)
	parser.add_argument("--require-conditional-review", action="store_true")
	parser.add_argument("--resolution-record", type=Path)
	parser.add_argument("--selected-change-id", action="append", default=[])
	return parser


def main(argv: list[str] | None = None) -> int:
	parser = create_parser()
	arguments = parser.parse_args(argv)
	if bool(arguments.report) == bool(arguments.resolution_record):
		parser.error("provide either REPORT or --resolution-record, not both")
	if arguments.resolution_record and not arguments.selected_change_id:
		parser.error("implementation preflight requires at least one --selected-change-id")
	if arguments.selected_change_id and not arguments.resolution_record:
		parser.error("selected changes must be checked against authoritative --resolution-record, not a report")
	try:
		if arguments.resolution_record:
			record = json.loads(arguments.resolution_record.read_text(encoding="utf-8-sig"), object_pairs_hook=_unique_json)
			errors = validate_resolution_record(record, arguments.selected_change_id)
		else:
			errors = validate_report(arguments.report.read_text(encoding="utf-8-sig"), arguments.require_conditional_review)
	except (OSError, UnicodeError, ValueError) as error:
		print(f"ERROR: {error}", file=sys.stderr)
		return 2
	print("PASSED" if not errors else "FAILED\n- " + "\n- ".join(errors))
	return 1 if errors else 0


if __name__ == "__main__":
	sys.exit(main())
