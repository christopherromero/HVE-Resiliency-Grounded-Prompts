"""Focused regression tests for offline configuration-mirror authority and integrity."""

from __future__ import annotations

import copy
import hashlib
import io
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import yaml

from validate_external_configuration_sources import main, validate_context, validate_source


class MirrorValidationTests(unittest.TestCase):
    """Exercise customer declarations and legacy client-based sources using local fixtures."""

    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.workspace = Path(self.temporary.name).resolve()
        self.mirror = self.workspace / "mirrors" / "cart-service"
        self.mirror.mkdir(parents=True)
        self.base_bytes = b"clients:\r\n  timeout: 1000\r\n"
        self.prod_bytes = b"spring:\n  application:\n    name: cart-service\n"
        (self.mirror / "application.yml").write_bytes(self.base_bytes)
        (self.mirror / "application-prod.yml").write_bytes(self.prod_bytes)
        self.source = {
            "source_id": "CFG-SRC-001",
            "type": "spring_cloud_config_server",
            "activation_mode": "customer_declared_mirror",
            "declaration": {"owner": "Fixture configuration owner", "reference": "FIXTURE-APPROVAL-001"},
            "application_name": "cart-service",
            "profiles": ["prod"],
            "label": "main",
            "server_availability": "unavailable",
            "local_equivalent": {
                "status": "present",
                "authority": "authoritative",
                "root_path": "mirrors/cart-service",
                "files": ["application.yml", "application-prod.yml"],
                "provenance": {"origin": "fixture-config-repo/cart-service"},
                "fingerprint": {"algorithm": "sha256", "scope": "concatenated_listed_files_in_order", "value": "compute_at_inventory"},
            },
        }

    def validate(self, observation: dict | None = None) -> dict:
        return validate_source(self.source, self.workspace, observation)

    def test_customer_declaration_captures_hash_without_client(self) -> None:
        original = copy.deepcopy(self.source)
        result = self.validate()
        self.assertEqual(result["authority"], "authoritative")
        self.assertEqual(result["authority_basis"], "customer_declaration")
        self.assertFalse(result["config_client_detected"])
        self.assertFalse(result["client_detection_evidence_supplied"])
        self.assertFalse(result["runtime_consumption_verified"])
        self.assertEqual(result["fingerprint_handling"], "computed_at_inventory")
        self.assertEqual(result["fingerprint_validation"], "captured")
        self.assertEqual(result["computed_fingerprint"], hashlib.sha256(self.base_bytes + self.prod_bytes).hexdigest())
        self.assertEqual(len(result["file_fingerprints"]), 2)
        self.assertEqual(self.source, original)
        self.assertEqual((self.mirror / "application.yml").read_bytes(), self.base_bytes)

    def test_supplied_hash_matching_and_mismatching(self) -> None:
        fingerprint = self.source["local_equivalent"]["fingerprint"]
        fingerprint["value"] = hashlib.sha256(self.base_bytes + self.prod_bytes).hexdigest().upper()
        self.assertEqual(self.validate()["fingerprint_validation"], "matched")
        fingerprint["value"] = "0" * 64
        result = self.validate()
        self.assertEqual(result["authority"], "unresolved")
        self.assertEqual(result["fingerprint_validation"], "mismatch")

    def test_raw_byte_order_and_changes_are_not_normalized(self) -> None:
        baseline = self.validate()["computed_fingerprint"]
        self.source["local_equivalent"]["files"].reverse()
        self.assertNotEqual(self.validate()["computed_fingerprint"], baseline)
        self.source["local_equivalent"]["files"].reverse()
        (self.mirror / "application.yml").write_bytes(self.base_bytes.replace(b"\r\n", b"\n"))
        self.assertNotEqual(self.validate()["computed_fingerprint"], baseline)
        self.source["local_equivalent"]["fingerprint"]["value"] = baseline
        self.assertEqual(self.validate()["local_equivalent_status"], "fingerprint_mismatch")

    def test_legacy_mode_requires_observed_client(self) -> None:
        del self.source["activation_mode"]
        self.source["detected_via"] = "source/cart-service/bootstrap.yml"
        self.assertEqual(self.validate()["authority"], "unresolved")
        observation = {"config_client_detected": True, "application_name": "cart-service", "profiles": ["prod"], "label": "main", "evidence_refs": ["FIXTURE-E001"]}
        result = self.validate(observation)
        self.assertEqual(result["authority_basis"], "detected_config_client")

    def test_known_binding_conflicts_cannot_be_overridden(self) -> None:
        for field, value in (("application_name", "other-service"), ("profiles", ["dev"]), ("label", "other-branch")):
            with self.subTest(field=field):
                result = self.validate({field: value, "evidence_refs": ["FIXTURE-E001"]})
                self.assertEqual(result["authority"], "unresolved")
                self.assertEqual(result["conflict_rule_id"], "ECR-CONFLICT-003")

    def test_detected_client_claim_requires_evidence_and_does_not_imply_binding(self) -> None:
        self.assertEqual(self.validate({"config_client_detected": True})["authority"], "unresolved")
        result = self.validate({"config_client_detected": True, "evidence_refs": ["FIXTURE-E001"]})
        self.assertEqual(result["authority"], "authoritative")
        self.assertEqual(result["client_match_status"], "customer_declaration_only")
        del self.source["activation_mode"]
        self.source["detected_via"] = "source/cart-service/bootstrap.yml"
        observation = {"config_client_detected": True, "application_name": "cart-service", "profiles": ["prod"], "evidence_refs": ["FIXTURE-E001"]}
        self.assertEqual(self.validate(observation)["local_equivalent_status"], "client_unconfirmed")

    def test_missing_and_placeholder_declarations_fail(self) -> None:
        for value in (None, "", "<customer configuration owner>", "TODO", "required_customer_input"):
            with self.subTest(value=value):
                self.source["declaration"]["owner"] = value
                self.assertEqual(self.validate()["authority"], "unresolved")

    def test_missing_or_malformed_fingerprint_does_not_default(self) -> None:
        for value in (None, "", "compute", "a" * 63, "g" * 64):
            with self.subTest(value=value):
                self.source["local_equivalent"]["fingerprint"]["value"] = value
                self.assertEqual(self.validate()["authority"], "unresolved")

    def test_missing_file_never_returns_partial_fingerprint(self) -> None:
        (self.mirror / "application-prod.yml").unlink()
        result = self.validate()
        self.assertEqual(result["local_equivalent_status"], "missing_file")
        self.assertEqual(result["computed_fingerprint"], "not_available")
        self.assertEqual(result["file_fingerprints"], [])

    def test_unreadable_file_leaves_authority_unresolved(self) -> None:
        with patch.object(Path, "read_bytes", side_effect=PermissionError("fixture")):
            result = self.validate()
        self.assertEqual(result["local_equivalent_status"], "unreadable_file")

    def test_invalid_yaml_and_duplicate_keys_do_not_expose_values(self) -> None:
        for content in (b"secret: [SECRET_FIXTURE", b"secret: SECRET_FIXTURE\nsecret: duplicate\n"):
            with self.subTest(content=content):
                (self.mirror / "application-prod.yml").write_bytes(content)
                result = self.validate()
                self.assertEqual(result["authority"], "unresolved")
                self.assertEqual(result["local_equivalent_status"], "invalid_configuration")
                self.assertNotIn("SECRET_FIXTURE", json.dumps(result))

    def test_unique_paths_and_containment_are_enforced(self) -> None:
        for files in (["application.yml", "./application.yml"], ["../outside.yml"], [str(self.mirror / "application.yml")], []):
            with self.subTest(files=files):
                self.source["local_equivalent"]["files"] = files
                self.assertEqual(self.validate()["authority"], "unresolved")

    def test_yaml_merges_and_unresolved_values_are_not_resolved(self) -> None:
        (self.mirror / "application-prod.yml").write_bytes(b"defaults: &defaults\n  timeout: 1\nclient:\n  <<: *defaults\n  timeout: 2\n  secret: ${SECRET_VALUE}\n")
        result = self.validate()
        self.assertEqual(result["authority"], "authoritative")
        self.assertNotIn("SECRET_VALUE", json.dumps(result))
        self.assertNotIn("effective_configuration", result)

    def test_duplicate_source_ids_fail_and_records_are_retained(self) -> None:
        result = validate_context({"external_configuration_sources": [self.source, copy.deepcopy(self.source)]}, self.workspace)
        self.assertEqual(result["status"], "unresolved")
        self.assertEqual(len(result["sources"]), 2)
        self.assertTrue(all(source["authority"] == "unresolved" for source in result["sources"]))

    def test_missing_local_equivalent_is_recorded_without_authority(self) -> None:
        self.source["local_equivalent"]["status"] = "none"
        result = self.validate()
        self.assertEqual(result["local_equivalent_status"], "none")
        self.assertEqual(result["authority"], "unresolved")

    def test_malformed_source_id_is_an_unresolved_record(self) -> None:
        self.source["source_id"] = []
        result = validate_context({"external_configuration_sources": [self.source]}, self.workspace)
        self.assertEqual(result["status"], "unresolved")
        self.assertEqual(result["sources"][0]["source_id"], "not_available")

    def test_cli_reads_frontmatter_context_without_mutating_it(self) -> None:
        context = self.workspace / "scope.yml"
        context.write_text(yaml.safe_dump_all([{"schema_version": "1.1.0"}, {"assessment_scope": {}, "external_configuration_sources": [self.source]}]), encoding="utf-8")
        original = context.read_bytes()
        output = io.StringIO()
        with patch("sys.argv", ["validator", "--workspace", str(self.workspace), "--context", "scope.yml"]), patch("sys.stdout", output):
            self.assertEqual(main(), 0)
        self.assertEqual(json.loads(output.getvalue())["status"], "validated")
        self.assertEqual(context.read_bytes(), original)

    def test_cli_invalid_context_does_not_disclose_configuration(self) -> None:
        context = self.workspace / "scope.yml"
        context.write_bytes(b"secret: [SECRET_FIXTURE")
        output = io.StringIO()
        with patch("sys.argv", ["validator", "--workspace", str(self.workspace), "--context", "scope.yml"]), patch("sys.stdout", output):
            self.assertEqual(main(), 2)
        self.assertNotIn("SECRET_FIXTURE", output.getvalue())


if __name__ == "__main__":
    unittest.main()