# Prompt 1: Create the Repository Inventory with HVE Task Researcher

## HVE write-location constraint

HVE Task Researcher is read-only outside its durable research artifact location. Write the complete authoritative inventory directly under:

`.copilot-tracking/research/{{YYYY-MM-DD}}/{{task_slug}}-research.md`

For this assessment, use a stable task slug such as:

`springboot-active-active-inventory`

Do not attempt to write to `working/`, `outputs/`, the application source tree, or any other directory.

## Role

You are the repository inventory agent for a Java Spring Boot active-active code-readiness assessment. Inspect the application repository and create a factual, evidence-linked inventory. This is discovery only.

Do not generate findings, compliance statuses, severity ratings, recommendations, readiness scores, remediation plans, or source-code changes.

## Required durable output

Create exactly one authoritative research artifact using the HVE research path convention:

`.copilot-tracking/research/{{YYYY-MM-DD}}/{{task_slug}}-research.md`

If HVE automatically chooses a date or equivalent slug-compliant filename, report the exact generated path in your completion response. That reported path becomes the input to Prompt 2.

The research artifact itself is the inventory. Do not create a second inventory file elsewhere.

## Source scope

Inspect Maven and Gradle files, production and test Java source, Spring configuration, repository-owned Kubernetes or Helm application settings, Dockerfiles, deployment scripts, tests, and application documentation. Exclude generated build directories, binaries, `.git`, IDE caches, `target`, `build`, and `.gradle`.

## Inventory objectives

Record application modules, Java and Spring Boot versions, production dependencies, client construction, regional endpoint configuration, retries, timeouts, circuit breakers, bulkheads, Actuator configuration, readiness, liveness, health indicators, state and session handling, transaction behavior, messaging behavior, idempotency, concurrency controls, graceful shutdown, regional telemetry, fault tests, and historical PCF references.

## Dependency evidence rule

Classify a dependency as `confirmed` only when production use is supported by repository evidence such as a client builder, Spring bean, configuration binding, repository implementation, producer, consumer, listener, or invocation. A build dependency alone means `declared_only`.

Normalize confirmed dependencies to:

- `keyvault`
- `cosmosdb`
- `eventhubs`
- `storage-blob`
- `azure-sql`
- `postgresql`
- `confluent-kafka`
- `dse-cassandra`
- `apim`
- `appgateway-glb`
- `http-client`
- `azure-functions`
- `azure-managed-redis`
- `aks-istio`

## Required research artifact structure

Use these exact top-level headings:

1. `# Spring Boot Active-Active Application Inventory`
2. `## Inventory Metadata`
3. `## Application Profile`
4. `## Confirmed Dependencies`
5. `## Declared-Only Dependencies`
6. `## Resilience Mechanisms`
7. `## Health and Traffic Eligibility`
8. `## State and Consistency`
9. `## Lifecycle and Recovery`
10. `## Observability`
11. `## Test Coverage`
12. `## Historical PCF References`
13. `## Uncertainties`
14. `## Dependency Standards to Load`
15. `## Inventory Summary`
16. `## Evaluation Handoff Contract`

Under `Inventory Metadata`, include:

```yaml
schema_version: "1.1"
assessment_run_id: "repository-or-service-name-YYYY-MM-DD-001"
phase: inventory
inventory_status: complete
inventory_agent: task-researcher
repository_root: "relative path"
re_inventory_required: false
```

For every evidence item, use:

```yaml
- file: "relative/path/to/file"
  symbol: "class, method, bean, property, or test"
  start_line: 1
  end_line: 10
  observation: "Concise factual observation"
  confidence: high
```

## Update for dependency standards from separate grounding file

Read: grounding/registry/dependency-standard-registry.yml

When a dependency is confirmed through production-code evidence:
1. Normalize to a registry key.
2. Look up its grounding_file from the registry.
3. Add both id and grounding_file to Dependency Standards to Load.

Do not hardcode dependency mappings in this prompt.

Example output:

```yaml
Dependency Standards to Load:
  - id: keyvault
    grounding_file: grounding/dependencies/springboot-keyvault.md

  - id: cosmosdb
    grounding_file: grounding/dependencies/springboot-cosmosdb.md
```

## Kafka Operating Scenario Discovery and Resolution

### Optional architecture-context inputs

```text
APPLICATION_ARCHITECTURE_CONTEXT=application-context/application-architecture-context.yml
SOLUTION_ARCHITECTURE_CONTEXT=application-context/solution-architecture-context.yml
KAFKA_SCENARIO_POLICY=grounding/governance/kafka-operating-scenario-policy.yml
```

The application and solution architecture-context files are optional.

If neither file exists:

- Continue the inventory.
- Do not treat the missing context as an error.
- Do not stop the assessment.
- Do not require the user to create a context file.
- Attempt policy-based scenario inference from repository-observed production behavior.
- Keep deployed infrastructure facts separately unresolved.

Do not equate an unresolved infrastructure fact with an unresolved application operating-scenario classification.

### Repository-observed interaction map

Generate direct interactions using repository evidence only:

```yaml
repository_observed_interactions:
  evidence_scope: repository_observed
  inbound_contracts: []
  direct_outbound_dependencies: []
  produced_events: []
  consumed_events: []
  scheduled_workloads: []
  direct_state_stores: []
  direct_secret_sources: []
  unresolved_endpoint_aliases: []
```

Do not infer the following from application code unless approved architecture context explicitly supplies them:

- Akamai, F5, Azure Application Gateway, or Azure API Management deployment topology
- Kafka cluster deployment topology
- Cluster Linking or Schema Linking
- Cross-region topic, schema, ACL, or consumer-offset replication
- Downstream Kafka consumers in another repository
- Transitive authoritative state stores
- Azure SQL Failover Group deployment
- Cosmos DB account-level multi-region-write enablement

Supplied architecture context and repository evidence must remain separate and retain distinct provenance.

### Kafka scenario inputs

When Confluent Kafka or Spring Kafka is confirmed through production code, record:

```yaml
kafka_scenario_inputs:
  confluent_kafka:
    used_by_production_code: true
    interaction_types: []
    evidence: []

  application_database:
    used_by_production_code: true|false|unknown
    evidence_basis: []

  azure_sql:
    used_by_production_code: true|false|unknown
    role: authoritative_business_state|transactional_system_of_record|reporting|optional|not_applicable|unknown
    evidence: []

  cosmos_db:
    used_by_production_code: true|false|unknown
    api: mongodb|nosql|unknown
    throughput_model: ru|vcore|unknown
    role: authoritative_business_state|durable_operational_state|failure_queue|cache|optional|not_applicable|unknown
    multi_region_write_evidence:
      status: confirmed_by_approved_context|repository_indicates_intent|external_evidence_required|not_applicable|unknown
      indicators: []
    evidence: []

  other_databases: []

  processing_model:
    value: stateless_producer|stateless_consumer|stream_transformer|topic_bridge|external_side_effect_processor|stateful_stream_processor|mixed|unknown
    evidence: []

  regional_processing_model:
    value: multi_active|single_active|unresolved
    evidence: []

  external_side_effects:
    value: none|idempotent_external_service|non_idempotent_external_service|unknown
    evidence: []

  kafka_backed_state:
    value: none|compacted_topic|kafka_streams_state_store|unknown
    evidence: []

  kafka_cluster_model:
    value: independent_regional_clusters|active_standby|stretched_cluster|unknown
    evidence_status: repository|approved_application_context|approved_solution_context|external_evidence_required
    evidence: []
```

A database dependency declared only in Maven or Gradle is not sufficient to establish production database use. Classify a database as used only when production code demonstrates a client, repository, template, data-access method, transaction path, or other effective interaction.

### Architecture-context handling

If approved architecture context is supplied:

1. Validate its schema version, lifecycle status, owner, context ID, context version, and Kafka operating model.
2. Record it separately from repository-observed interaction evidence.
3. Use it as the preferred scenario declaration.
4. Validate the declaration using the Kafka scenario policy.
5. Never present supplied context as repository-discovered evidence.
6. Never silently override an approved scenario declaration.

```yaml
supplied_architecture_context:
  context_status: provided|not_provided|invalid
  source_path: application-context/application-architecture-context.yml
  context_id: <id-or-not_applicable>
  context_version: <version-or-not_applicable>
  lifecycle_status: approved|not_applicable|invalid
  kafka_declared_scenario: active_standby|independent_regional_active_active|database_independent_kafka|not_provided
```

### Missing architecture-context behavior

When architecture context is not provided:

- Continue the assessment.
- Attempt provisional scenario inference.
- Set `source_type: policy_inference`.
- Set `architecture_confirmation_required: true`.
- Keep actual deployed topology separately unresolved.
- Do not claim that the inferred scenario is approved architecture.

The repository may support inference of an application operating scenario while Kafka cluster topology, Cluster Linking, topic replication, offset replication, regional Kafka role assignment, Cosmos DB account-level multi-region writes, and Azure SQL Failover Group deployment remain unresolved.

An inferred scenario identifies the operating model against which the application can be provisionally assessed. It does not assert that the supporting infrastructure has been deployed.

Only leave the scenario `unresolved` when the policy's required application and supplied-context evidence is insufficient, conflicting, or unsupported.

### Scenario resolution rules

Apply the Kafka scenario policy in this order.

#### Rule 1: Azure SQL authoritative state

If production application behavior directly uses Azure SQL as authoritative business or transactional state, including applications that also use Cosmos DB:

```yaml
value: active_standby
rule_id: KAFKA-SCENARIO-001
status: inferred
architecture_confirmation_required: true
```

#### Rule 2: Cosmos DB MongoDB RU active-active intent

If Kafka and Cosmos DB are used by production code, Cosmos DB uses MongoDB API and RU throughput, Cosmos DB is authoritative business or durable operational state, Azure SQL is not authoritative state, and repository evidence indicates regional multi-write intent, infer:

```yaml
value: independent_regional_active_active
rule_id: KAFKA-SCENARIO-002
status: conditionally_inferred
architecture_confirmation_required: true
```

Preserve these conditions:

```yaml
conditional_assumptions:
  - Confirm Cosmos DB multi-region writes are enabled.
  - Confirm Kafka uses independent regional clusters.
  - Confirm the Kafka deployment is not a stretched cluster.
  - Confirm each regional deployment normally uses its local Kafka cluster.
```

Do not require an approved context file merely to perform this conditional inference. Do not record Cosmos DB multi-region writes or Kafka topology as confirmed platform facts unless approved context or another authoritative source confirms them.

Repository indicators of multi-region-write intent may include region-specific connection selection, preferred-write-region configuration, MongoDB `appName` regional configuration, region-aware configuration properties, or application logic explicitly designed for local regional writes.

#### Rule 3: Kafka with no application database

If Kafka is used by production code, no Azure SQL, Cosmos DB, or other application database is used by production code, and no approved processing-chain context identifies a downstream authoritative database, infer:

```yaml
value: database_independent_kafka
rule_id: KAFKA-SCENARIO-003
status: inferred
architecture_confirmation_required: true
```

Resolve `processing_model`, `regional_processing_model`, `external_side_effects`, and `kafka_backed_state` separately. Do not assume database-independent Kafka is stateless, multi-active, free of durable state, free of external side effects, or safe for duplicate processing.

#### Rule 4: Unresolved

Use:

```yaml
value: unresolved
rule_id: KAFKA-SCENARIO-004
status: insufficient_evidence
architecture_confirmation_required: true
```

only when required production-use evidence is insufficient, roles conflict, approved context conflicts with repository behavior, Cosmos active-active intent cannot be established even conditionally, the processing model cannot be determined, or the architecture uses an unsupported stretched cluster.

### Required scenario output

```yaml
kafka_operating_scenario:
  value: active_standby|independent_regional_active_active|database_independent_kafka|unresolved

  declaration:
    source_type: approved_application_architecture_context|approved_solution_architecture_context|policy_inference|unresolved
    source_path: <path-or-not_available>
    context_id: <id-or-not_applicable>
    context_version: <version-or-not_applicable>
    approval_status: approved|not_applicable|unknown

  policy_validation:
    policy_id: KAFKA-OPERATING-SCENARIO
    policy_version: "3.2.0"
    rule_id: KAFKA-SCENARIO-001|KAFKA-SCENARIO-002|KAFKA-SCENARIO-003|KAFKA-SCENARIO-004
    status: consistent|inferred|conditionally_inferred|conflict|insufficient_evidence

  repository_validation:
    status: consistent|conflict|insufficient_evidence
    observed_dependencies: []
    conflicting_evidence: []

  processing_model: <value-or-not_applicable>

  regional_processing_model:
    value: multi_active|single_active|unresolved|not_applicable
    evidence_status: repository|approved_context|unresolved

  external_side_effects: <value-or-not_applicable>
  kafka_backed_state: <value-or-not_applicable>
  architecture_confirmation_required: true|false
  conditional_assumptions: []
  unresolved_infrastructure_facts: []
```

### Conflict behavior

If approved context conflicts with repository or policy evidence:

```yaml
kafka_operating_scenario:
  value: unresolved
  policy_validation:
    status: conflict
  assessment_action:
    common_controls: evaluate_when_evidence_available
    scenario_specific_controls: not_assessed
    emit_code_finding: false
    route_to: architecture_governance_review
```

Do not silently select another scenario. Do not create a code finding solely because architecture context conflicts with repository evidence.

### Kafka dependency-standard output

When Kafka is confirmed, include:

```yaml
dependency_standards_to_load:
  - id: confluent-kafka
    grounding_file: grounding/dependencies/springboot-confluent-kafka.md
    operating_scenario: <resolved value>
    scenario_source: <source type>
    scenario_rule_id: <rule ID>
    scenario_validation_status: <status>
    architecture_confirmation_required: true|false
```


## Architecture and Scope Resolution

### Assessment scope context and schema boundary

Read these configured inputs:

```text
ASSESSMENT_SCOPE_CONTEXT=application-context/assessment-scope-context.yml
ASSESSMENT_SCOPE_SCHEMA=grounding/governance/assessment-scope-schema.yml
```

The context and schema are distinct artifacts:

- The context must declare `document_type: assessment_scope_context` and contains selected settings.
- The schema must declare `document_type: assessment_scope_schema` and defines allowed values, defaults, and validation rules.

Do not substitute an example, base, or similarly named file when the configured schema is missing or invalid. Do not search example folders for a replacement schema. If the schema is invalid, stop before optional-domain inventory and report the exact path and validation error. If the context is absent, apply defaults from the valid schema.

Required output:

```yaml
assessment_scope_resolution:
  context_path: application-context/assessment-scope-context.yml
  schema_path: grounding/governance/assessment-scope-schema.yml
  context_status: "<valid|not_provided|invalid>"
  schema_status: "<valid|missing|invalid>"
  defaults_used: false
  enabled_domains: []
  disabled_domains: []
  inventory_only_domains: []
  report_preferences:
    finding_selection_mode: "<all_priorities|priority_filter>"
    included_priorities: []
    testing_output_mode: "<full|summary|roadmap_only|hidden>"
  validation_errors: []
```

Inventory Dockerfiles, pipelines, deployment configuration, and IaC only when their domains are enabled. Never inventory or assess deployed infrastructure.

### Repository-agnostic assessment snapshot

Do not assume the assessed folder is a Git repository. Never initialize Git or create a commit solely to establish assessment provenance.

```yaml
assessment_snapshot:
  type: "<git_revision|workspace_snapshot|uploaded_archive|source_drop|unknown>"
  identifier: "<stable-identifier-or-not_available>"
  provenance: "<repository_metadata|workspace_generated|uploaded_file|customer_supplied|unknown>"
  git_commit_sha: "<full-sha-or-not_applicable>"
  dirty_worktree: "<true|false|not_applicable|unknown>"
  captured_at: "<ISO-8601-timestamp-or-not_available>"
  limitations: []
```

Use `git_revision` only when valid Git metadata is available. Otherwise classify the input as a workspace snapshot, uploaded archive, source drop, or unknown source with explicit limitations.

### Application architecture relationships

When approved application architecture context exists, preserve business role, authoritative state, upstream dependencies, downstream dependencies, external side effects, and architecture decisions separately from repository-observed interactions.

```yaml
architecture_relationship_context:
  source_path: application-context/application-architecture-context.yml
  context_status: "<approved|draft|invalid|not_provided>"
  business_role: "<value-or-not_provided>"
  upstream_dependencies: []
  downstream_dependencies: []
  external_side_effects:
    present: "<true|false|unknown>"
    types: []
```

Architecture context explains intended workflow position but does not prove implementation. Use solution architecture context only when cross-repository or transitive facts are required.

### Architecture conflict record

When approved context conflicts with repository or policy evidence, emit:

```yaml
architecture_conflict:
  detected: true
  affected_area: "<kafka_scenario|authoritative_state|regional_processing|dependency_relationship|other>"
  context_source: "<application_context|solution_context>"
  context_declaration: "<concise-value>"
  repository_evidence: []
  policy_evidence: []
  resolution_status: unresolved
  assessment_action:
    common_controls: evaluate_when_evidence_available
    scenario_specific_controls: not_assessed
    code_finding_created_for_conflict: false
    route_to: architecture_governance_review
```

Do not silently override approved context or create a code finding solely because of the conflict.

## Assessment Domain Standards to Load

Use `grounding/registry/dependency-standard-registry.yml` as the only registry authority. Do not invent grounding paths or search examples for substitutes.

If a confirmed dependency or enabled assessment domain has no valid registry entry, record:

```yaml
dependency_standard_gaps:
  - id: "<normalized-dependency-or-domain-id>"
    evidence: []
    registry_path: grounding/registry/dependency-standard-registry.yml
    gap_reason: "<entry_missing|grounding_file_missing|entry_invalid>"
    downstream_action: not_assessed_until_governance_resolved
```

Keep optional assessment-domain standards separate from runtime dependency standards:

```yaml
assessment_domain_standards_to_load:
  - id: cicd-pipeline-resiliency
    assessment_domain: cicd_pipeline
    grounding_file: grounding/dependencies/cicd-pipeline-resiliency.md
    repository_owned_artifacts: []
```

### Machine-readable template convention

Pipe-delimited placeholders document allowed values only. Generated artifacts must contain one concrete value. Emit `status: consistent`, never `status: consistent|conflict|insufficient_evidence`.

### Evidence location rule

Calculate line numbers when possible and never estimate them. Treat them as advisory navigation metadata:

```yaml
original_line_range:
  start_line: 1
  end_line: 10
  status: "<exact|advisory|not_available>"
```

## Evaluation handoff contract

End the artifact with this machine-readable block:

```yaml
handoff:
  artifact_role: authoritative_inventory
  next_phase: evaluation
  next_agent: task-reviewer
  re_inventory_allowed: false
  source_validation_mode: cited_evidence_only
  missing_evidence_status: not_assessed
  infrastructure_assessment_allowed: false
  pcf_findings_allowed: false
```

## End-of-Phase Compact Handoff Summary

At the end of this phase, create one compact handoff summary under:

```text
.copilot-tracking/research/handoffs/
```

Read and follow:

```text
grounding/governance/phase-handoff-schema.yml
```

The handoff summary is a non-authoritative index of facts already established by this phase. It supports state reconstruction after `/clear` or a new chat. It never replaces the authoritative phase artifact.

Requirements:

- Derive every value from the authoritative phase artifacts.
- Preserve stable finding, evidence, change, policy, scenario, and control IDs.
- Include exact authoritative input and output artifact paths.
- Include key decisions, counts, unresolved items, exceptions, and required next-phase inputs.
- Do not create findings, reassess controls, recalculate priority, change scenarios, invent evidence, authorize implementation, or modify source.
- When the summary conflicts with an authoritative artifact, the authoritative artifact wins and the handoff must record a `handoff_exception`.
- Report the generated handoff path in the completion response.

### Step 1 handoff

Write:

```text
.copilot-tracking/research/handoffs/01-inventory-summary.yml
```

Include:

```yaml
phase_metadata:
  schema_id: ASSESSMENT-PHASE-HANDOFF
  schema_version: "<active-version-from-phase-handoff-schema.yml>"
  phase: inventory
  phase_order: "01"
  assessment_run_id: <run-id>
  generated_at: <timestamp>
  generation_status: complete

authority:
  summary_role: non_authoritative_phase_index
  authoritative_source_artifacts:
    - <inventory-artifact-path>
  source_of_truth: authoritative_inventory
  conflict_behavior: use_authoritative_artifact_and_record_handoff_exception

input_artifacts: []
output_artifacts:
  inventory_artifact: <path>

application_profile:
  application_name: <value>
  language: <value>
  framework: <value>
  runtime_platform: <value>
  repository_root: <value>

dependency_summary:
  confirmed_dependencies: []
  declared_only_dependencies: []
  dependency_standards_to_load: []

repository_observed_interactions:
  inbound_contract_count: 0
  direct_outbound_dependency_count: 0
  produced_event_count: 0
  consumed_event_count: 0
  scheduled_workload_count: 0

scenario_summary:
  kafka:
    applicable: false
    value: not_applicable
    source: not_applicable
    validation_status: not_applicable
    policy_id: not_applicable
    policy_version: not_applicable
    rule_id: not_applicable
    architecture_confirmation_required: false
    conditional_assumptions: []
    unresolved_infrastructure_facts: []

inventory_exceptions: []
key_decisions: []
unresolved_items: []

next_phase:
  phase: assessment
  required_authoritative_inputs:
    - <inventory-artifact-path>
  handoff_summary_path: .copilot-tracking/research/handoffs/01-inventory-summary.yml
```


## Completion validation

Before completing:

- Verify the authoritative research artifact exists under `.copilot-tracking/research/` and its path uses the configured `task_slug` consistently.
- Verify every confirmed dependency has production-code evidence.
- Verify the dependency standards list contains only confirmed dependencies.
- Verify dependency standards and assessment-domain standards are listed separately.
- Verify missing or invalid registry entries are recorded as governance gaps and no grounding path was invented.
- Verify assessment-scope context and schema were distinguished and validated.
- Verify no example or base schema was used as an unapproved fallback.
- Verify optional artifact domains were inventoried only when enabled.
- Verify the assessment snapshot was classified without requiring Git metadata.
- Verify upstream dependencies, downstream dependencies, and external side effects from approved context remain separate from repository-observed interactions.
- Verify architecture conflicts use the deterministic conflict record and do not produce code findings by themselves.
- Verify generated machine-readable fields contain one concrete allowed value rather than pipe-delimited alternatives.
- Verify evidence line numbers were calculated when possible, never estimated, and classified as exact, advisory, or unavailable.
- Verify no findings, recommendations, severity ratings, scores, remediation plans, or source changes appear.
- Verify PCF references are informational only.
- Verify the evaluation handoff prohibits re-inventory.
- Verify the handoff schema version is read from `grounding/governance/phase-handoff-schema.yml` rather than hardcoded.
- Verify one compact handoff summary exists under `.copilot-tracking/research/handoffs/` when agent write permissions permit it.
- Report the exact artifact path, assessment run ID, snapshot type and identifier, files examined, enabled scope domains, confirmed dependencies, registry gaps, architecture conflicts, and unresolved uncertainties.


## Resiliency and non-resiliency finding classification contract
Use `grounding/governance/resiliency-finding-qualification-policy.yml` version 1.0.0. Preserve every evidence-backed applicable control violation as either `resiliency` or `non_resiliency`. Do not suppress a valid non-resiliency finding merely because it fails the resiliency gate. Resiliency classification requires a credible failure scenario, approved resiliency domain, target-architecture element, causal mechanism, and material impact. Preserve classification and rationale across phase artifacts. Business-logic risk remains a separate implementation-approval dimension.

### Phase-specific rule
Inventory applicable target architecture elements and credible failure scenarios needed by Step 2; do not classify findings in Step 1.
