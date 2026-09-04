# Prompt 1: Create the Repository Inventory with HVE Task Researcher 9-1

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

`.copilot-tracking/research/{{YYYY-MM-DD}}/springboot-active-active-inventory-research.md`

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
- `spring-http-and-sdk-clients`
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

# Prompt 1 Update: External-Context Kafka Scenario Declaration and Validation

## Optional inputs

```text
APPLICATION_ARCHITECTURE_CONTEXT=application-context/application-architecture-context.yml
SOLUTION_ARCHITECTURE_CONTEXT=application-context/solution-architecture-context.yml
KAFKA_SCENARIO_POLICY=grounding/governance/kafka-operating-scenario-policy.yml
```

## Repository-observed interaction map

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

Do not infer Akamai, F5, Application Gateway, APIM, downstream consumers,
transitive state stores, Kafka replication, or regional infrastructure from
application code unless an approved context artifact supplies it.

## External context handling

If context is supplied:

1. Validate its schema, lifecycle status, owner, version, and Kafka fields.
2. Record it separately from repository-observed interactions.
3. Never present supplied context as repository evidence.
4. Preserve source path, context ID, version, and approval status.

```yaml
supplied_architecture_context:
  context_status: provided
  source_path: application-context/application-architecture-context.yml
  context_id: <id>
  context_version: <version>
  lifecycle_status: approved
  kafka_declared_scenario: active_standby
```

## Kafka scenario resolution

Preferred sequence:

1. Read the approved scenario declaration from application context.
2. If absent, read approved solution processing-chain context.
3. If absent, infer provisionally from repository-observed direct dependency roles.
4. Validate the declared or inferred scenario against the scenario policy.
5. Never silently override an approved declaration.

Output:

```yaml
kafka_operating_scenario:
  value: active_standby|independent_regional_active_active|unresolved
  declaration:
    source_type: approved_application_architecture_context|approved_solution_architecture_context|policy_inference|unresolved
    source_path: <path-or-not_available>
    context_id: <id-or-not_applicable>
    context_version: <version-or-not_applicable>
    approval_status: approved|not_applicable|unknown
  policy_validation:
    policy_id: KAFKA-OPERATING-SCENARIO
    policy_version: "2.0.0"
    rule_id: KAFKA-SCENARIO-001|KAFKA-SCENARIO-002|KAFKA-SCENARIO-003
    status: consistent|inferred|conflict|insufficient_evidence
  repository_validation:
    status: consistent|conflict|insufficient_evidence
    observed_dependencies: []
    conflicting_evidence: []
  architecture_confirmation_required: true|false
```

## Conflict behavior

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

Do not change the declared architecture, infer another scenario, or create a code finding.

## Dependency standard output

```yaml
dependency_standards_to_load:
  - id: confluent-kafka
    grounding_file: grounding/dependencies/springboot-confluent-kafka.md
    operating_scenario: <resolved value>
    scenario_source: <source type>
    scenario_rule_id: <rule ID>
    scenario_validation_status: <status>
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
# Prompt 1 Scenario-Aware Kafka Inventory Update

Add the following required output when Confluent Kafka or Spring Kafka is discovered:

```yaml
kafka_scenario_inputs:
  confluent_kafka:
    used_by_production_code: true
    evidence: []
  azure_sql:
    used_by_production_code: true|false|unknown
    role: authoritative_business_state|transactional_system_of_record|reporting|optional|not_applicable|unknown
    evidence: []
  cosmos_db:
    used_by_production_code: true|false|unknown
    api: mongodb|nosql|unknown
    throughput_model: ru|vcore|unknown
    role: authoritative_business_state|durable_operational_state|failure_queue|cache|optional|not_applicable|unknown
    multi_region_writes: true|false|external_evidence_required|unknown
    evidence: []
  kafka_cluster_model:
    value: independent_regional_clusters|active_standby|stretched_cluster|unknown
    evidence_status: repository|application_context|external_evidence_required
    evidence: []
```

Read `grounding/governance/kafka-operating-scenario-policy.yml` and resolve:

```yaml
dependency_standards_to_load:
  - id: confluent-kafka
    grounding_file: grounding/dependencies/springboot-confluent-kafka.md
    operating_scenario: active_standby|independent_regional_active_active|unresolved
    scenario_rule_id: KAFKA-SCENARIO-001|KAFKA-SCENARIO-002|KAFKA-SCENARIO-003
```

Rules:
- Azure SQL dependency presence alone is not enough; prove production use and role.
- Azure SQL authoritative-state presence selects active-standby, including SQL plus Cosmos.
- Cosmos-only selects active-active only when MongoDB API, RU, and multi-region writes are authoritative.
- Missing external topology produces `unresolved`, not an invented scenario.

## End-of-Phase Compact Handoff Summary

At the end of this phase, create one compact handoff summary under:

```text
.copilot-tracking/handoffs/
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
.copilot-tracking/handoffs/01-inventory-summary.yml
```

Include:

```yaml
phase_metadata:
  schema_id: ASSESSMENT-PHASE-HANDOFF
  schema_version: "1.0.0"
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
  handoff_summary_path: .copilot-tracking/handoffs/01-inventory-summary.yml
```


## Completion validation

Before completing:

1. Verify the research artifact exists under `.copilot-tracking/research/`.
2. Verify every confirmed dependency has production-code evidence.
3. Verify the dependency standards list contains only confirmed dependencies.
4. Verify no findings, recommendations, severity ratings, scores, or implementation plans appear.
5. Verify PCF references are informational only.
6. Verify the handoff block prohibits re-inventory.
7. Report the exact artifact path, assessment run ID, files examined, confirmed dependencies, and unresolved uncertainties.
