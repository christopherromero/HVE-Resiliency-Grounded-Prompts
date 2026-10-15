# Shared-Service Assessment Scope Guide

## Purpose

Use shared-service scope when a service is used by the application and remains architecturally relevant, but its control evaluation is limited or excluded for the current assessment. Do not use repository exclusions for this case. Exclusions are for files or artifact classes that should not be processed, such as historical PCF assets.

## Effective scopes

- `in_scope`: inventory, architecture reasoning, controls, findings, remediation, implementation, and review are allowed.
- `out_of_scope`: inventory and architecture reasoning remain; controls, findings, observations, remediation, and implementation are prohibited.
- `informational_only`: inventory, architecture reasoning, and concise observations are allowed; findings, priorities, remediation, and implementation are prohibited.
- `architecture_only`: architecture reasoning is required when relevant; repository controls, findings, remediation, and implementation are prohibited.

## Add the three sample services

Add the services under `architecture_context.shared_service_assessment_scope.services`. Use canonical kebab-case keys. Because these services are not currently in the dependency registry, also represent their architecture role in the appropriate architecture relationship or operating-model section only when approved facts are available. Do not invent a grounding standard or registry path.

```yaml
architecture_context:
  shared_service_assessment_scope:
    contract_version: "1.0.0"
    default_scope: in_scope
    canonical_key_source: dependency_standard_registry
    services:
      databricks:
        assessment_scope: out_of_scope
        rationale: >-
          Databricks is used by the solution but is assessed separately by the
          enterprise data platform team.
        scope_owner: data_platform_team
        external_assessment_reference: not_provided

      elasticsearch:
        assessment_scope: informational_only
        rationale: >-
          Elasticsearch usage is documented for dependency and processing-chain
          context, but Elasticsearch controls are not evaluated in this assessment.
        scope_owner: search_platform_team
        external_assessment_reference: not_provided

      mongo-atlas:
        assessment_scope: architecture_only
        rationale: >-
          Mongo Atlas participates in authoritative-state and processing-chain
          reasoning but is reviewed under a separate database platform assessment.
        scope_owner: database_platform_team
        external_assessment_reference: not_provided
```

## Registry behavior for unregistered services

The service may be listed in architecture context before a dependency grounding standard exists. Step 1 must inventory it and preserve its scope. It must not invent a grounding path. If the service later becomes `in_scope`, add a governed registry entry and grounding standard before control evaluation; until then, record a governance gap and mark service-specific controls `not_assessed`.

## Do not duplicate scope flags

The schema derives findings and remediation permissions from `assessment_scope`. Do not add independent Boolean fields that can contradict the selected scope.
