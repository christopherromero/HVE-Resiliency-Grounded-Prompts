#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = ["PyYAML>=6.0.2,<7"]
# ///
"""Validate local YAML configuration mirrors without contacting external services.

Run with ``uv run tools/validate_external_configuration_sources.py``. Optional
``--observed-bindings`` accepts an inventory-produced JSON object keyed by source
ID, containing config_client_detected, application_name, profiles, label, and
evidence_refs. This tool validates supplied observations; it does not discover
clients, verify customer approvals independently, or merge effective keys.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from collections.abc import Mapping
from pathlib import Path
from typing import Any

import yaml

POLICY_VERSION = "1.1.0"
PLACEHOLDERS = {"todo", "unknown", "not_available", "required_customer_input", "pending_customer_input"}
EXIT_SUCCESS = 0
EXIT_FAILURE = 1
EXIT_ERROR = 2


class MirrorValidationError(ValueError):
    """Carry a safe failure code and field name, never configuration values."""

    def __init__(self, code: str, field: str) -> None:
        super().__init__(code)
        self.code = code
        self.field = field


class UniqueKeyLoader(yaml.SafeLoader):
    """Reject duplicate explicit YAML keys while preserving normal merge overrides."""


def construct_mapping(loader: UniqueKeyLoader, node: yaml.MappingNode, deep: bool = False) -> dict:
    """Construct a safe mapping with unique explicit keys."""
    seen = set()
    for key_node, _value_node in node.value:
        if key_node.tag == "tag:yaml.org,2002:merge":
            continue
        key = loader.construct_object(key_node, deep=deep)
        if key in seen:
            raise MirrorValidationError("invalid_configuration", "duplicate_yaml_key")
        seen.add(key)
    loader.flatten_mapping(node)
    return yaml.SafeLoader.construct_mapping(loader, node, deep=deep)


UniqueKeyLoader.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, construct_mapping)


def populated(value: Any) -> bool:
    """Return whether a required declaration value is supplied rather than a placeholder."""
    return (
        isinstance(value, str)
        and bool(value.strip())
        and value.strip().lower() not in PLACEHOLDERS
        and "<" not in value
        and ">" not in value
    )


def required_text(value: Any, field: str) -> str:
    """Require nonplaceholder metadata without including its value in diagnostics."""
    if not populated(value):
        raise MirrorValidationError("missing_metadata", field)
    return value


def contained_path(parent: Path, value: str, field: str) -> Path:
    """Resolve a relative path and prevent traversal or symlink escape."""
    candidate = Path(value)
    if candidate.is_absolute():
        raise MirrorValidationError("invalid_metadata", field)
    resolved = (parent / candidate).resolve()
    if not resolved.is_relative_to(parent.resolve()):
        raise MirrorValidationError("invalid_metadata", field)
    return resolved


def load_yaml_documents(raw: bytes) -> list[Any]:
    """Parse UTF-8 YAML without exposing parser excerpts in errors."""
    try:
        return list(yaml.load_all(raw.decode("utf-8-sig"), Loader=UniqueKeyLoader))
    except (yaml.YAMLError, UnicodeError, TypeError, ValueError) as error:
        raise MirrorValidationError("invalid_configuration", "yaml") from error


def validate_source(
    source: Mapping[str, Any], workspace: Path, observed_binding: Mapping[str, Any] | None = None
) -> dict[str, Any]:
    """Validate one declared mirror and return provenance without configuration values."""
    workspace = workspace.resolve()
    observation = observed_binding if observed_binding is not None else {}
    source_id = source.get("source_id", "not_available")
    result: dict[str, Any] = {
        "source_id": source_id if isinstance(source_id, str) and re.fullmatch(r"CFG-SRC-[0-9]{3}", source_id) else "not_available",
        "policy_id": "EXTERNAL-CONFIG-RESOLUTION",
        "policy_version": POLICY_VERSION,
        "activation_mode": source.get("activation_mode", "detected_config_client"),
        "authority": "unresolved",
        "authority_basis": "unresolved",
        "local_equivalent_status": "missing_metadata",
        "computed_fingerprint": "not_available",
        "fingerprint_handling": "not_available",
        "fingerprint_validation": "not_assessed",
        "file_fingerprints": [],
        "binding_observation_refs": [],
        "observations": [],
        "validation_errors": [],
        "runtime_consumption_verified": False,
    }
    try:
        if result["source_id"] == "not_available" or source.get("type") != "spring_cloud_config_server":
            raise MirrorValidationError("invalid_metadata", "source_id_or_type")
        mode = result["activation_mode"]
        if mode not in ("detected_config_client", "customer_declared_mirror"):
            raise MirrorValidationError("invalid_metadata", "activation_mode")
        application = required_text(source.get("application_name"), "application_name")
        profiles = source.get("profiles")
        if not isinstance(profiles, list) or not all(populated(profile) for profile in profiles) or len(profiles) != len(set(profiles)):
            raise MirrorValidationError("invalid_metadata", "profiles")
        label = source.get("label", "not_provided")
        if "label" in source:
            required_text(label, "label")
        if source.get("server_availability") not in ("available", "unavailable"):
            raise MirrorValidationError("invalid_metadata", "server_availability")
        result.update(application_name=application, profiles=profiles, label=label)
        local = source.get("local_equivalent")
        if not isinstance(local, Mapping):
            raise MirrorValidationError("missing_metadata", "local_equivalent")
        if local.get("status") != "present":
            raise MirrorValidationError("none", "local_equivalent.status")
        if local.get("authority") != "authoritative":
            raise MirrorValidationError("invalid_metadata", "local_equivalent.authority")
        if mode == "customer_declared_mirror":
            declaration = source.get("declaration", {})
            if not isinstance(declaration, Mapping):
                raise MirrorValidationError("missing_metadata", "declaration")
            result["declaration_owner"] = required_text(declaration.get("owner"), "declaration.owner")
            result["declaration_reference"] = required_text(declaration.get("reference"), "declaration.reference")
        else:
            required_text(source.get("detected_via"), "detected_via")
            result.update(declaration_owner="not_applicable", declaration_reference="not_applicable")
        if not isinstance(observation, Mapping):
            raise MirrorValidationError("invalid_metadata", "observed_bindings")
        detected = observation.get("config_client_detected", False)
        if not isinstance(detected, bool):
            raise MirrorValidationError("invalid_metadata", "observed_bindings.config_client_detected")
        refs = observation.get("evidence_refs", [])
        if not isinstance(refs, list) or not all(populated(ref) for ref in refs):
            raise MirrorValidationError("invalid_metadata", "observed_bindings.evidence_refs")
        if detected and not refs:
            raise MirrorValidationError("missing_metadata", "observed_bindings.evidence_refs")
        result.update(config_client_detected=detected, client_detection_evidence_supplied=observed_binding is not None, binding_observation_refs=refs)
        for field, expected in (("application_name", application), ("profiles", profiles), ("label", label)):
            actual = observation.get(field)
            known = isinstance(actual, list) if field == "profiles" else populated(actual)
            if known:
                if not refs:
                    raise MirrorValidationError("missing_metadata", "observed_bindings.evidence_refs")
                if actual != expected and not (field == "label" and label == "not_provided"):
                    raise MirrorValidationError("binding_conflict", field)
            elif mode == "detected_config_client" and (field in ("application_name", "profiles") or label != "not_provided"):
                raise MirrorValidationError("client_unconfirmed", field)
        if mode == "detected_config_client" and (not detected or not refs):
            raise MirrorValidationError("client_unconfirmed", "config_client_detected")
        binding_matched = (
            detected
            and observation.get("application_name") == application
            and observation.get("profiles") == profiles
            and (label == "not_provided" or observation.get("label") == label)
        )
        result["client_match_status"] = "matched" if binding_matched else "customer_declaration_only"
        if not detected:
            result["observations"].append("Client detection is not established by this validator; authority relies on the customer declaration.")
        provenance = local.get("provenance", {})
        if not isinstance(provenance, Mapping):
            raise MirrorValidationError("missing_metadata", "local_equivalent.provenance")
        result["provenance_origin"] = required_text(provenance.get("origin"), "local_equivalent.provenance.origin")
        result["provenance_source_revision"] = provenance.get("source_revision", "not_available")
        root_value = required_text(local.get("root_path"), "local_equivalent.root_path")
        root = contained_path(workspace, root_value, "local_equivalent.root_path")
        result["root_path"] = root.relative_to(workspace).as_posix()
        files = local.get("files")
        if not isinstance(files, list) or not files or not all(populated(name) for name in files):
            raise MirrorValidationError("missing_metadata", "local_equivalent.files")
        fingerprint = local.get("fingerprint", {})
        if not isinstance(fingerprint, Mapping):
            raise MirrorValidationError("missing_metadata", "local_equivalent.fingerprint")
        if fingerprint.get("algorithm") != "sha256" or fingerprint.get("scope") != "concatenated_listed_files_in_order":
            raise MirrorValidationError("invalid_metadata", "local_equivalent.fingerprint")
        expected_hash = fingerprint.get("value")
        if not isinstance(expected_hash, str) or not re.fullmatch(r"compute_at_inventory|[A-Fa-f0-9]{64}", expected_hash):
            raise MirrorValidationError("invalid_metadata", "local_equivalent.fingerprint.value")
        result["declared_fingerprint"] = expected_hash
        digest = hashlib.sha256()
        manifest = []
        seen_paths = set()
        for index, name in enumerate(files):
            field = f"local_equivalent.files[{index}]"
            path = contained_path(root, name, field)
            if path in seen_paths:
                raise MirrorValidationError("invalid_metadata", field)
            seen_paths.add(path)
            if not path.is_file():
                raise MirrorValidationError("missing_file", field)
            if path.suffix.lower() not in (".yml", ".yaml"):
                raise MirrorValidationError("unsupported_format", field)
            try:
                raw = path.read_bytes()
            except OSError as error:
                raise MirrorValidationError("unreadable_file", field) from error
            documents = load_yaml_documents(raw)
            if any(document is not None and not isinstance(document, Mapping) for document in documents):
                raise MirrorValidationError("invalid_configuration", field)
            digest.update(raw)
            manifest.append({"repository_path": path.relative_to(workspace).as_posix(), "size_bytes": len(raw), "sha256": hashlib.sha256(raw).hexdigest()})
        result.update(computed_fingerprint=digest.hexdigest(), file_fingerprints=manifest, files_in_precedence_order=files)
        if expected_hash == "compute_at_inventory":
            result.update(fingerprint_handling="computed_at_inventory", fingerprint_validation="captured")
        elif expected_hash.lower() == digest.hexdigest():
            result.update(fingerprint_handling="supplied_hash_verified", fingerprint_validation="matched")
        else:
            result["fingerprint_validation"] = "mismatch"
            raise MirrorValidationError("fingerprint_mismatch", "local_equivalent.fingerprint.value")
        result.update(authority="authoritative", authority_basis="customer_declaration" if mode == "customer_declared_mirror" else "detected_config_client", local_equivalent_status="validated")
    except MirrorValidationError as error:
        result["local_equivalent_status"] = error.code
        result["validation_errors"].append({"code": error.code, "field": error.field})
        if error.code == "binding_conflict":
            result.update(client_match_status="binding_conflict", route_to="architecture_governance_review", conflict_rule_id="ECR-CONFLICT-003")
    return result


def validate_context(context: Mapping[str, Any], workspace: Path, observations: Mapping[str, Any] | None = None) -> dict[str, Any]:
    """Validate all declarations, retaining failed records and rejecting duplicate IDs."""
    sources = context.get("external_configuration_sources", [])
    if not isinstance(sources, list) or not all(isinstance(source, Mapping) for source in sources):
        raise MirrorValidationError("invalid_metadata", "external_configuration_sources")
    bindings = observations if observations is not None else {}
    if not isinstance(bindings, Mapping):
        raise MirrorValidationError("invalid_metadata", "observed_bindings")
    records = []
    for source in sources:
        source_id = source.get("source_id")
        observation = bindings.get(source_id) if isinstance(source_id, str) else None
        records.append(validate_source(source, workspace, observation))
    counts: dict[str, int] = {}
    for record in records:
        source_id = record["source_id"]
        counts[source_id] = counts.get(source_id, 0) + 1
    for record in records:
        if counts[record["source_id"]] > 1:
            record.update(authority="unresolved", authority_basis="unresolved", local_equivalent_status="invalid_metadata")
            record["validation_errors"].append({"code": "duplicate_source_id", "field": "source_id"})
    return {"policy_id": "EXTERNAL-CONFIG-RESOLUTION", "policy_version": POLICY_VERSION, "status": "unresolved" if any(record["authority"] != "authoritative" for record in records) else "validated", "sources": records}


def create_parser() -> argparse.ArgumentParser:
    """Create the read-only mirror validation CLI."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--workspace", type=Path, default=Path(__file__).resolve().parent.parent)
    parser.add_argument("--context", type=Path, default=Path("application-context/assessment-scope-context.yml"))
    parser.add_argument("--observed-bindings", type=Path)
    return parser


def main() -> int:
    """Print safe JSON validation results and return a standard exit code."""
    args = create_parser().parse_args()
    try:
        workspace = args.workspace.resolve()
        context_path = contained_path(workspace, args.context.as_posix(), "context")
        documents = load_yaml_documents(context_path.read_bytes())
        contexts = [document for document in documents if isinstance(document, Mapping) and "assessment_scope" in document]
        if len(contexts) != 1:
            raise MirrorValidationError("invalid_configuration", "context")
        observations = None
        if args.observed_bindings is not None:
            observations_path = contained_path(workspace, args.observed_bindings.as_posix(), "observed_bindings")
            observations = json.loads(observations_path.read_text(encoding="utf-8"))
        result = validate_context(contexts[0], workspace, observations)
        print(json.dumps(result, indent=2))
        return EXIT_SUCCESS if result["status"] == "validated" else EXIT_FAILURE
    except KeyboardInterrupt:
        return 130
    except BrokenPipeError:
        return EXIT_FAILURE
    except (MirrorValidationError, OSError, UnicodeError, ValueError):
        print(json.dumps({"status": "configuration_error", "message": "Unable to validate context or supplied observations; configuration contents are omitted."}))
        return EXIT_ERROR


if __name__ == "__main__":
    sys.exit(main())