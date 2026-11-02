"""Validate supplied Atlas/Kafka target contracts offline, without verifying deployments."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import yaml


def load_documents(path: Path) -> list[dict]:
    """Keep separate YAML documents separate, including context metadata headers."""
    parsed = yaml.safe_load_all(path.read_text(encoding="utf-8-sig"))
    documents = [document for document in parsed if document is not None]
    if not documents or any(not isinstance(document, dict) for document in documents):
        raise ValueError(f"Expected YAML mapping documents: {path}")
    return documents


def lookup(document: dict, path: str) -> object:
    """Resolve a dotted governance predicate in a parsed mapping."""
    value = document
    for component in path.split("."):
        if not isinstance(value, dict) or component not in value:
            return None
        value = value[component]
    return value


def resolved(value: object) -> bool:
    """Reject unresolved contract inputs without interpreting source or runtime facts."""
    if value is None or value is False:
        return False
    if isinstance(value, str):
        text = value.strip().lower()
        return bool(text) and text not in {
            "unknown", "unresolved", "requires_approval", "not_provided", "not_available",
        } and "<" not in text and ">" not in text and not text.startswith("replace_with_")
    if isinstance(value, dict):
        return bool(value) and all(resolved(item) for item in value.values())
    if isinstance(value, list):
        return bool(value) and all(resolved(item) for item in value)
    return True


def resolve_mongo_scope(variant: str, services: dict, schema: dict, default_scope: str = "in_scope") -> dict:
    """Apply a previously resolved variant; this function does not detect providers."""
    service_key = schema["provider_aware_scope_binding"]["variant_to_service_key"].get(variant)
    if service_key is None:
        return {"service_key": None, "assessment_scope": "not_assessed"}
    entry = services.get(service_key, {})
    scope = entry.get("assessment_scope", default_scope) if isinstance(entry, dict) else None
    if scope not in schema["allowed_scope_values"]:
        scope = "not_assessed"
    return {"service_key": service_key, "assessment_scope": scope}


def validate_context(documents: list[dict], policy: dict, scope_schema: dict) -> dict:
    """Check only supplied design structure; approvals and repository use remain external authority."""
    headers = [document for document in documents if document.get("document_type") == "application_architecture_context"]
    bodies = [document for document in documents if "architecture_context" in document]
    if len(headers) != 1 or len(bodies) != 1 or not isinstance(bodies[0]["architecture_context"], dict):
        raise ValueError("Expected one architecture-context header and one architecture-context body")
    header = headers[0]
    context = bodies[0]["architecture_context"]
    expected_rule = lookup(context, "kafka_operating_model.expected_scenario_rule_id")
    provider = lookup(context, "dependency_variants.mongodb.target.provider")
    if expected_rule != policy["registry_contract"]["kafka_rule_id"] and provider != "atlas":
        return {"resolution_status": "not_applicable", "errors": [], "deployed_topology_verified": False}

    errors = []
    if header.get("lifecycle_status") != "approved" or lookup(context, "metadata.lifecycle_status") != "approved":
        errors.append("Document and metadata lifecycle_status must both be approved")
    for field in ("context_owner", "approved_by", "approved_at", "version"):
        if not resolved(lookup(context, f"metadata.{field}")):
            errors.append(f"Missing or unresolved metadata.{field}")
    if expected_rule != policy["registry_contract"]["kafka_rule_id"]:
        errors.append("Expected Kafka rule must be KAFKA-SCENARIO-006")
    if lookup(context, "kafka_operating_model.scenario_policy_id") != "KAFKA-OPERATING-SCENARIO":
        errors.append("Incorrect Kafka scenario policy ID")

    contract_spec = policy["context_contract"]
    for path, expected in contract_spec["required_target_predicates"].items():
        actual = lookup(context, path)
        if type(actual) is not type(expected) or actual != expected:
            errors.append(f"Target predicate {path} must equal {expected!r}")

    target = lookup(context, "atlas_global_cluster_contract.target")
    target = target if isinstance(target, dict) else {}
    for field in contract_spec["required_contract_fields"]:
        if field != "zones" and (not isinstance(target.get(field), str) or not resolved(target[field])):
            errors.append(f"Missing or unresolved Atlas target contract: {field}")
    zones = target.get("zones", [])
    zones = zones if isinstance(zones, list) else []
    if len(zones) < contract_spec["minimum_zones"]:
        errors.append("Atlas target requires at least two declared zones")
    zone_ids = []
    primary_regions = []
    for zone in zones:
        if not isinstance(zone, dict):
            errors.append("Each Atlas zone must be a mapping")
            continue
        for field in contract_spec["zone_required_fields"]:
            if not resolved(zone.get(field)):
                errors.append(f"Missing or unresolved zone field: {field}")
        if not isinstance(zone.get("electable_regions"), list):
            errors.append("Zone electable_regions must be a list")
        zone_ids.append(str(zone.get("zone_id")))
        primary_regions.append(str(zone.get("highest_priority_region")))
    if len(set(zone_ids)) != len(zone_ids):
        errors.append("Atlas zone IDs must be unique")
    if len(set(primary_regions)) < contract_spec["minimum_distinct_highest_priority_regions"]:
        errors.append("Atlas target requires write-owning zones in at least two regions")

    mirroring = lookup(context, contract_spec["kafka_mirroring_path"])
    mirroring = mirroring if isinstance(mirroring, dict) else {}
    for field, expected in contract_spec["required_mirroring_predicates"].items():
        if type(mirroring.get(field)) is not type(expected) or mirroring.get(field) != expected:
            errors.append(f"Kafka mirroring predicate {field} must equal {expected!r}")
    for field in contract_spec["required_mirroring_fields"]:
        if not isinstance(mirroring.get(field), str) or not resolved(mirroring[field]):
            errors.append(f"Missing or unresolved mirroring contract: {field}")

    services = lookup(context, "shared_service_assessment_scope.services")
    services = services if isinstance(services, dict) else {}
    if "mongo-atlas" in services:
        errors.append("Use canonical mongodb scope, not mongo-atlas")
    default_scope = lookup(context, "shared_service_assessment_scope.default_scope") or "in_scope"
    mongo_scope = resolve_mongo_scope("native_mongodb", services, scope_schema, str(default_scope))
    kafka_scope = lookup(services, "confluent-kafka.assessment_scope") or default_scope
    joint_in_scope = mongo_scope["assessment_scope"] == "in_scope" and kafka_scope == "in_scope"
    consistent = not errors
    return {
        "policy_id": policy["policy_id"],
        "policy_version": policy["policy_version"],
        "context_version": lookup(context, "metadata.version"),
        "source_provider": lookup(context, "dependency_variants.mongodb.source.provider"),
        "source_deployment_model": lookup(context, "dependency_variants.mongodb.source.deployment_model"),
        "target_provider": provider,
        "target_deployment_model": lookup(context, "dependency_variants.mongodb.target.deployment_model"),
        "kafka_rule_id": expected_rule if consistent else "KAFKA-SCENARIO-005",
        "kafka_scenario": "independent_regional_active_active" if consistent else "unresolved",
        "resolution_status": "consistent" if consistent else "insufficient_evidence",
        "architecture_confirmation_required": not consistent,
        "joint_controls_status": "evaluate_when_repository_evidence_available" if consistent and joint_in_scope else "not_assessed",
        "scope_bindings": {"mongodb": mongo_scope["assessment_scope"], "confluent-kafka": kafka_scope},
        "unresolved_inputs": errors,
        "errors": errors,
        "deployed_topology_verified": False,
        "approval_authenticity_verified": False,
        "production_integration_verified": False,
    }


def create_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("context", type=Path, help="Application architecture context YAML")
    parser.add_argument("--workspace", type=Path, default=Path(__file__).resolve().parents[1])
    return parser


def main() -> int:
    arguments = create_parser().parse_args()
    try:
        policy = load_documents(arguments.workspace / "grounding/governance/mongodb-atlas-kafka-operating-scenario-policy.yml")[0]
        scope_documents = load_documents(arguments.workspace / "grounding/governance/shared-service-assessment-scope-schema.yml")
        scope_schema = next(document for document in scope_documents if "provider_aware_scope_binding" in document)
        result = validate_context(load_documents(arguments.context), policy, scope_schema)
    except (OSError, ValueError, yaml.YAMLError, KeyError, StopIteration) as error:
        print(f"Configuration error: {error}", file=sys.stderr)
        return 2
    print(json.dumps(result, indent=2, default=str))
    return 1 if result["errors"] else 0


if __name__ == "__main__":
    sys.exit(main())