"""Regression tests for Atlas target governance and independent provider scopes."""

from __future__ import annotations

import copy
import unittest
from pathlib import Path

from validate_atlas_kafka_scenario import load_documents, resolve_mongo_scope, validate_context


WORKSPACE = Path(__file__).resolve().parents[1]
SAMPLE = WORKSPACE / "application-context/Samples/application-architecture-context-mongodb-atlas-global-kafka-active-active.yml"


class AtlasScenarioTests(unittest.TestCase):
    def setUp(self) -> None:
        self.policy = load_documents(WORKSPACE / "grounding/governance/mongodb-atlas-kafka-operating-scenario-policy.yml")[0]
        documents = load_documents(WORKSPACE / "grounding/governance/shared-service-assessment-scope-schema.yml")
        self.scope_schema = next(document for document in documents if "provider_aware_scope_binding" in document)
        self.documents = copy.deepcopy(load_documents(SAMPLE))
        self.header = self.documents[0]
        self.context = self.documents[1]["architecture_context"]
        self.header["lifecycle_status"] = "approved"
        self.context["metadata"].update({
            "lifecycle_status": "approved", "context_owner": "Fixture owner",
            "approved_by": "Fixture approver", "approved_at": "2026-10-29", "sample_only": False,
        })
        target = self.context["atlas_global_cluster_contract"]["target"]
        target["contract_status"] = "approved"
        for field in self.policy["context_contract"]["required_contract_fields"]:
            if field != "zones":
                target[field] = f"FIXTURE-{field}"
        for zone in target["zones"]:
            zone["electable_regions"] = ["fixture-recovery-region"]
            zone["data_ownership_reference"] = "FIXTURE-OWNERSHIP"
        mirroring = self.context["shared_service_connectivity_contracts"]["services"]["confluent-kafka"]["target"]["mirroring_contract"]
        for field in self.policy["context_contract"]["required_mirroring_fields"]:
            mirroring[field] = f"FIXTURE-{field}"

    def validate(self) -> dict:
        return validate_context(self.documents, self.policy, self.scope_schema)

    def test_complete_supplied_contract_selects_atlas_without_runtime_claims(self) -> None:
        result = self.validate()
        self.assertEqual(result["errors"], [])
        self.assertEqual(result["kafka_rule_id"], "KAFKA-SCENARIO-006")
        self.assertEqual(result["joint_controls_status"], "evaluate_when_repository_evidence_available")
        self.assertFalse(result["deployed_topology_verified"])
        self.assertFalse(result["approval_authenticity_verified"])
        self.assertFalse(result["production_integration_verified"])

    def test_draft_sample_stays_unresolved_and_unchanged(self) -> None:
        before = SAMPLE.read_bytes()
        result = validate_context(load_documents(SAMPLE), self.policy, self.scope_schema)
        self.assertEqual(result["kafka_scenario"], "unresolved")
        self.assertEqual(result["joint_controls_status"], "not_assessed")
        self.assertTrue(result["architecture_confirmation_required"])
        self.assertEqual(SAMPLE.read_bytes(), before)

    def test_replica_set_and_other_provider_targets_are_not_supported(self) -> None:
        target = self.context["dependency_variants"]["mongodb"]["target"]
        target["deployment_model"] = "replica_set"
        self.assertTrue(self.validate()["errors"])
        target.update({"deployment_model": "global_cluster", "provider": "cosmosdb"})
        self.assertTrue(self.validate()["errors"])

    def test_global_cluster_is_not_unrestricted_multi_primary(self) -> None:
        target = self.context["atlas_global_cluster_contract"]["target"]
        target["unrestricted_multi_primary_per_record"] = True
        self.assertTrue(self.validate()["errors"])
        target["unrestricted_multi_primary_per_record"] = False
        target["single_primary_per_shard"] = False
        self.assertTrue(self.validate()["errors"])

    def test_registry_preserves_driver_selection_and_version_consistency(self) -> None:
        registry = load_documents(WORKSPACE / "grounding/registry/dependency-standard-registry.yml")[0]["standards"]
        self.assertEqual(registry["cosmosdb"]["default_standard_activation_requires"], "cosmos_sdk_production_integration")
        self.assertEqual(registry["cosmosdb"]["api_behavior_standards"]["mongodb"], registry["mongodb"]["grounding_file"])
        kafka_policy = load_documents(WORKSPACE / "grounding/governance/kafka-operating-scenario-policy.yml")[0]
        self.assertEqual(registry["confluent-kafka"]["scenario_policy"]["version"], kafka_policy["policy_version"])

    def test_active_standby_and_stretched_kafka_targets_are_blocked(self) -> None:
        target = self.context["kafka_operating_model"]["target"]
        target["scenario"] = "active_standby"
        self.assertTrue(self.validate()["errors"])
        target["scenario"] = "independent_regional_active_active"
        target["cluster_model"]["stretched_cluster"] = True
        self.assertTrue(self.validate()["errors"])

    def test_every_required_contract_reference_is_enforced(self) -> None:
        target = self.context["atlas_global_cluster_contract"]["target"]
        for field in self.policy["context_contract"]["required_contract_fields"]:
            if field == "zones":
                continue
            original = target[field]
            with self.subTest(field=field):
                target[field] = "requires_approval"
                self.assertTrue(self.validate()["errors"])
            target[field] = original

    def test_mirroring_ownership_direction_loop_and_recovery_are_required(self) -> None:
        contract = self.context["shared_service_connectivity_contracts"]["services"]["confluent-kafka"]["target"]["mirroring_contract"]
        for field in self.policy["context_contract"]["required_mirroring_fields"]:
            original = contract.pop(field)
            with self.subTest(field=field):
                self.assertTrue(self.validate()["errors"])
            contract[field] = original
        contract["topic_mirroring_required"] = False
        self.assertTrue(self.validate()["errors"])

    def test_zones_require_distinct_region_ownership_and_electable_inputs(self) -> None:
        zones = self.context["atlas_global_cluster_contract"]["target"]["zones"]
        zones[1]["highest_priority_region"] = zones[0]["highest_priority_region"]
        self.assertTrue(self.validate()["errors"])
        zones[1]["highest_priority_region"] = "fixture-other-region"
        zones[0]["electable_regions"] = ["requires_approval"]
        self.assertTrue(self.validate()["errors"])

    def test_source_is_preserved_and_does_not_select_another_target(self) -> None:
        self.context["dependency_variants"]["mongodb"]["source"]["deployment_model"] = "unknown"
        result = self.validate()
        self.assertEqual(result["errors"], [])
        self.assertEqual(result["source_deployment_model"], "unknown")
        self.assertEqual(result["target_deployment_model"], "global_cluster")

    def test_partial_scope_preserves_scenario_but_blocks_joint_controls(self) -> None:
        services = self.context["shared_service_assessment_scope"]["services"]
        for service in ("mongodb", "confluent-kafka"):
            services[service]["assessment_scope"] = "out_of_scope"
            result = self.validate()
            self.assertEqual(result["resolution_status"], "consistent")
            self.assertEqual(result["joint_controls_status"], "not_assessed")
            services[service]["assessment_scope"] = "in_scope"

    def test_atlas_exclusion_does_not_suppress_cosmos_mongo(self) -> None:
        services = {"mongodb": {"assessment_scope": "out_of_scope"}, "cosmosdb": {"assessment_scope": "in_scope"}}
        for variant in ("cosmos_mongo_ru", "cosmos_mongo_vcore"):
            binding = resolve_mongo_scope(variant, services, self.scope_schema)
            self.assertEqual(binding, {"service_key": "cosmosdb", "assessment_scope": "in_scope"})
        self.assertEqual(resolve_mongo_scope("native_mongodb", services, self.scope_schema)["assessment_scope"], "out_of_scope")
        self.assertEqual(resolve_mongo_scope("unknown", services, self.scope_schema)["assessment_scope"], "not_assessed")

    def test_cosmos_exclusion_does_not_suppress_atlas(self) -> None:
        services = {"mongodb": {"assessment_scope": "in_scope"}, "cosmosdb": {"assessment_scope": "out_of_scope"}}
        self.assertEqual(resolve_mongo_scope("native_mongodb", services, self.scope_schema)["assessment_scope"], "in_scope")
        self.assertEqual(resolve_mongo_scope("cosmos_mongo_ru", services, self.scope_schema)["assessment_scope"], "out_of_scope")

    def test_existing_samples_keep_scopes_and_scenario_rules(self) -> None:
        paths = list((WORKSPACE / "application-context/Samples").glob("*.yml"))
        self.assertEqual(len(paths), 6)
        for path in paths + [WORKSPACE / "application-context/application-architecture-context.yml"]:
            documents = load_documents(path)
            context = next(document["architecture_context"] for document in documents if "architecture_context" in document)
            services = context["shared_service_assessment_scope"]["services"]
            self.assertNotIn("mongo-atlas", services)
            expected = "in_scope" if path == SAMPLE else "out_of_scope"
            self.assertEqual(services["mongodb"]["assessment_scope"], expected)
            if path != SAMPLE:
                self.assertEqual(validate_context(documents, self.policy, self.scope_schema)["resolution_status"], "not_applicable")

    def test_existing_rule_ids_and_sql_precedence_are_preserved(self) -> None:
        kafka_policy = load_documents(WORKSPACE / "grounding/governance/kafka-operating-scenario-policy.yml")[0]
        rules = kafka_policy["consistency_rules"]
        indexed = {rule["rule_id"]: rule for rule in rules}
        self.assertEqual(len(rules), len(indexed))
        self.assertEqual(set(indexed), {f"KAFKA-SCENARIO-{number:03d}" for number in range(1, 7)})
        ordered = sorted(rules, key=lambda rule: rule["precedence"])
        self.assertEqual(ordered[0]["rule_id"], "KAFKA-SCENARIO-001")
        self.assertEqual(ordered[-1]["rule_id"], "KAFKA-SCENARIO-005")
        for rule_id, scenario in (("001", "active_standby"), ("002", "independent_regional_active_active"), ("003", "database_independent_kafka"), ("004", "independent_regional_active_active")):
            self.assertEqual(indexed[f"KAFKA-SCENARIO-{rule_id}"]["expected_target"]["scenario"], scenario)

    def test_phase_prompts_and_handoff_preserve_provider_and_scenario_records(self) -> None:
        for path in (WORKSPACE / "prompts").glob("*.prompt.md"):
            text = path.read_text(encoding="utf-8")
            self.assertIn("mongodb_scope_bindings", text)
            self.assertIn("atlas_kafka_scenario", text)
        handoff = load_documents(WORKSPACE / "grounding/governance/phase-handoff-schema.yml")[0]
        self.assertEqual(handoff["mongodb_provider_and_atlas_handoff"]["preserve"], ["mongodb_scope_bindings", "atlas_kafka_scenario"])


if __name__ == "__main__":
    unittest.main()