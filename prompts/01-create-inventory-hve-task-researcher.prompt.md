---
description: Create the authoritative repository inventory with governed scope and dependency resolution
---

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

## Dependency and capability activation rule

A standard activates through one of two routes. Record which route and which signal fired.

1. **Production dependency** (`production_dependency`) — repository evidence confirms production use, and the service is in scope. Either signal qualifies:
   - `production_code_evidence`: a client builder, Spring bean, configuration binding, repository implementation, producer, consumer, listener, or invocation demonstrates effective interaction. Classify the dependency `confirmed`.
   - `repository_pattern_evidence`: a repository-owned production file, configuration key, manifest, or build element matches the registry `repository_patterns` and identifies the specific dependency or platform. Test-only, documentation-only, and generated matches do not qualify. A generic pattern shared by several standards, such as `spring.datasource.url` or `WebClient.Builder`, qualifies only with dependency-specific corroboration.
2. **Approved target-platform capability** (`approved_target_platform_capability`) — approved application architecture context declares a capability that matches the registry `inventory_capabilities`, the registry entry sets `capability_activation_allowed: true`, and the service is in scope. The signal is `architecture_declared_capability`.

Capability activation does not confirm deployed infrastructure or production integration. Do not require a platform SDK, a service-mesh or platform manifest, or deployed-state evidence to activate a standard through the capability route.

A build dependency alone, with no qualifying signal, is `declared_only` and activates nothing.

Activation and finding authority are separate decisions. Activation establishes applicability. Only repository evidence may later establish a defect.

Resolve registry keys from `grounding/registry/dependency-standard-registry.yml`. Do not hardcode or memorize the key list; it changes as standards are added.

## Required research artifact structure

Use these exact top-level headings:

1. `# Spring Boot Active-Active Application Inventory`
2. `## Inventory Metadata`
3. `## Application Profile`
4. `## Confirmed Dependencies`
5. `## Declared-Only Dependencies`
6. `## Architecture-Activated Standards`
7. `## Resilience Mechanisms`
8. `## Health and Traffic Eligibility`
9. `## State and Consistency`
10. `## Lifecycle and Recovery`
11. `## Observability`
12. `## Test Coverage`
13. `## Historical PCF References`
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

## Resolving standards to load

Read: grounding/registry/dependency-standard-registry.yml

For every entry under `standards` and `assessment_domain_standards`, perform these steps literally. Do not add a confirmation test beyond what the registry declares.

1. Evaluate `activate_when.scope_status` first. If the required assessment domain is disabled, the standard is `not_applicable` with `exclusion_reason: assessment_domain_disabled`. Record it and stop.
2. Match `inventory_dependencies` against confirmed dependencies (`production_code_evidence`).
3. Match `repository_patterns`, and `inventory_capabilities` against the repository-derived application profile, against repository-owned production files and configuration (`repository_pattern_evidence`). Apply the registry `excluded_matches`.
4. Match `inventory_capabilities` against approved application architecture context (`architecture_declared_capability`). Count the match only when the context status is `approved` and the entry sets `capability_activation_allowed: true`. Otherwise record `capability_context_not_approved` or `capability_activation_not_accepted_by_registry`.
5. Resolve the route: steps 2 or 3 give `production_dependency`; step 4 alone gives `approved_target_platform_capability`. When both match, record both and use `production_dependency` as primary.
6. Apply the shared-service scope gate from `Shared-Service Assessment Scope Resolution`. A standard whose effective scope is not `in_scope` is `not_activated` with `exclusion_reason: shared_service_not_in_scope` or `shared_service_scope_unresolved`. A standard without a `shared_service_assessment_scope` block passes this gate.
7. Apply any `additional_gate` and `requires_standard`, resolving the required baseline with this same procedure.
8. Record the `evaluation_mode` from the route: `full` for `production_dependency`, `repository_verifiable_controls_only` for `approved_target_platform_capability`.
9. Write one `standard_resolution` record for the entry, whether it activated or not.

A standard activated **only** by the capability route loads in `repository_verifiable_controls_only` mode. It is listed, loaded, and evaluated. Its application-side controls are evaluated from application code, configuration, and tests. Only its integration-dependent controls are later marked `not_assessed`.

Do not omit a standard because production integration is unconfirmed. Never silently omit a registry entry. When a registry entry with `capability_activation_allowed: true` declares a capability that approved context also declares, it must be activated or carry a specific exclusion reason.

Do not hardcode dependency mappings in this prompt.

Record every candidate under `## Dependency Standards to Load`:

```yaml
standard_resolution:
  - id: aks-istio
    registry_section: standards
    candidate_status: activated
    activation_route: approved_target_platform_capability
    matched_signals:
      - {signal: architecture_declared_capability, matched: "runtime_platform: aks", evidence: "application-architecture-context.yml runtime_platform: aks"}
    evaluation_mode: repository_verifiable_controls_only
    shared_service_effective_scope: in_scope
    exclusion_reason: none
    rationale: "Approved context declares AKS; registry accepts capability activation."
  - id: postgresql
    registry_section: standards
    candidate_status: not_activated
    activation_route: none
    matched_signals:
      - {signal: repository_pattern_evidence, matched: "spring.datasource.url", evidence: "application.yml:12"}
    evaluation_mode: none
    shared_service_effective_scope: not_applicable
    exclusion_reason: pattern_not_dependency_specific
    rationale: "Generic datasource key without a PostgreSQL driver, URL scheme, or client."
  - id: cicd-pipeline-resiliency
    registry_section: assessment_domain_standards
    candidate_status: not_applicable
    activation_route: none
    matched_signals: []
    evaluation_mode: none
    shared_service_effective_scope: not_applicable
    exclusion_reason: assessment_domain_disabled
    rationale: "cicd_pipeline is disabled in assessment scope."
```

Use only the `allowed_exclusion_reasons` in the registry `candidate_resolution` block. Then list activated standards:

```yaml
Dependency Standards to Load:
  - id: mongodb
    grounding_file: grounding/dependencies/springboot-mongodb.md
    activation_route: production_dependency
    activation_signal: production_code_evidence
    evaluation_mode: full
    evidence: "source/cart-service/.../CartRepository.java:5 extends MongoRepository"

  - id: keyvault
    grounding_file: grounding/dependencies/springboot-keyvault.md
    activation_route: production_dependency
    activation_signal: production_code_evidence
    evaluation_mode: full
    evidence: "SecretClient bean construction"

  - id: aks-istio
    grounding_file: grounding/dependencies/springboot-aks-istio.md
    activation_route: approved_target_platform_capability
    activation_signal: architecture_declared_capability
    evaluation_mode: repository_verifiable_controls_only
    evidence: "application-architecture-context.yml runtime_platform: aks"
    integration_status: unconfirmed_in_repository
```

## Workload detection

A repository may contain more than one deployable workload, such as a backend service plus a browser client. Detect every workload before resolving standards, and record the exception required by the repository model when more than one deployable workload exists.

For each workload record `id`, `kind`, `language`, `framework`, `root`, and the evidence that established it. Allowed `kind` values are `service`, `browser_client`, `server_rendering`, `batch`, and `library`.

The existing scalar `language`, `framework`, and `runtime_platform` fields remain and describe the primary workload.

### Frontend workload detection

Evaluate frontend detection only when `frontend_application` is `enabled` or `inventory_only` in the active assessment scope. When the domain is `disabled`, record that frontend detection was skipped by scope and do not load frontend standards.

1. Locate every `package.json` in the repository, excluding dependency and build output directories.
2. Resolve the framework from `dependencies` and `devDependencies`:
   - `@angular/core` indicates Angular. Record the resolved `@angular/core` and `rxjs` versions.
   - `react` with `react-dom` indicates React. Record the resolved `react` version.
   - Neither present with browser entry evidence indicates an unclassified browser client. Load the baseline only.
3. Resolve the version from the lockfile when present. When only a range is declared, record the lowest version the range permits and mark it range-derived.
4. For React, detect every data layer present using the standard's `data_layer_detection` block and record each one. More than one may be present.
5. Detect server-side rendering using positive evidence only. Record `ssr_detected: true` with the mode and evidence, `false` with the basis for exclusion, or `unknown` with an evidence gap.
6. Resolve standards through the registry. Framework standards require the `frontend-web-client` baseline. The SSR standard loads only when `ssr_detected` is `true`.
<!--> Enhanced rules <-->
7. Perform explicit evaluation of critical customer journeys like Menu, User Info, or dependent features.
8. Validate timeout, retry, cancellation, and recovery behavior.
9. Perform assessment of UI loading, error, empty, degraded-service, and success states.
10. Perform analysis of service startup, readiness, cache warm-up, and shutdown behavior.
11. Perform strong evaluation of React and Angular state management and feature-flag resiliency implementations.
12. Evaluate the robustness of API integration, including error handling, retries, and fallback mechanisms.
13. Assess the security posture, including authentication, authorization, and data protection measures.


Do not infer a frontend workload from a repository that contains only build output, and do not assume SSR because a framework supports it.

Example output:

```yaml
Workloads:
  - id: backend
    kind: service
    language: java
    framework: spring-boot
    root: source/cart-service
  - id: frontend
    kind: browser_client
    language: typescript
    framework: angular
    framework_version: "16.2.0"
    companion_versions: {rxjs: "7.8.1"}
    version_basis: lockfile
    root: source/customer-app
    ssr_detected: false
    ssr_detection_basis: "No server entry point; build script produces client bundle only."

Dependency Standards to Load:
  - id: frontend-web-client
    grounding_file: grounding/dependencies/frontend-web-client.md
  - id: angular-rxjs
    grounding_file: grounding/dependencies/angular-rxjs.md
```

## Kafka Operating Scenario Discovery and Resolution

### Optional architecture-context inputs

```text
APPLICATION_ARCHITECTURE_CONTEXT=application-context/application-architecture-context.yml
SOLUTION_ARCHITECTURE_CONTEXT=application-context/solution-architecture-context.yml
KAFKA_SCENARIO_POLICY=grounding/governance/kafka-operating-scenario-policy.yml
COSMOS_MONGODB_VARIANT_POLICY=grounding/governance/cosmos-mongodb-variant-policy.yml
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

### Cosmos MongoDB variant resolution

When Cosmos DB for MongoDB production use is confirmed, read
`grounding/governance/cosmos-mongodb-variant-policy.yml` before resolving Kafka
scenario predicates or MongoDB variant-specific applicability. This governance
input does not activate a dependency or expand assessment scope.

Store the single `cosmos_mongodb_variant_resolution` object in a fenced YAML
document under the existing `## State and Consistency` heading. When Kafka is
confirmed, place `kafka_scenario_inputs` in that section as well and reference the
same resolution object; do not duplicate it or introduce a new top-level heading
or inventory artifact. Cosmos MongoDB workloads without Kafka still record their
variant resolution without activating Kafka.

1. Resolve the selected assessment state and retain its approved declarations separately from repository observations.
2. Read optional `architecture_context.dependency_variants.cosmosdb.source` or `.target` for that state. Each object may declare `api`, `throughput_model`, and an existing `exception_reference`; absent objects remain valid.
3. Apply the shared policy's precedence and terminal gates. An approved application declaration takes precedence over a supplied solution declaration; same-state contradictions require review rather than silent selection.
4. For confirmed Cosmos MongoDB target use with no declaration or positive variant evidence, resolve RU using `approved_organization_default`. Do not leave the throughput model unknown solely because no RU hostname or per-application RU declaration is available.
5. Explicit vCore declarations or positive vCore evidence prevent the RU default. Preserve the exception signal without inventing an exception approval. A vCore result does not satisfy an RU-only Kafka rule.
6. Keep unknown source-state identity when neither a source declaration nor positive source evidence exists. Do not treat an approved source-to-target migration as a same-state conflict.
7. Record the complete resolution below, populate `kafka_scenario_inputs.cosmos_db.throughput_model` from it, and retain policy provenance outside repository evidence. The default does not prove deployed identity, multi-region writes, or any code defect.

For an eligible target-state RU default, emit this concrete shape with actual
evidence references populated when available:

```yaml
cosmos_mongodb_variant_resolution:
  throughput_model: ru
  resolution_source: approved_organization_default
  default_applied: true
  resolution_status: resolved
  selected_assessment_state: target
  observed_throughput_model: unknown
  deployed_variant_verified: false
  policy_id: COSMOS-MONGODB-VARIANT
  policy_version: "1.0.0"
  policy_path: grounding/governance/cosmos-mongodb-variant-policy.yml
  evidence: []
  exception_reference: not_available
```

The sample's `evidence: []` means no positive variant evidence is supplied, not
that Cosmos production use or the MongoDB API was inferred from the default.
Record those qualifying facts with their existing inventory evidence. Never use
the default for native MongoDB, Cosmos NoSQL, or an unconfirmed provider or API.
For overrides and conflicts, emit the actual concrete values defined by the policy.

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
    throughput_model_resolution_ref: cosmos_mongodb_variant_resolution
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

If Kafka and Cosmos DB are used by production code, Cosmos DB uses MongoDB API and RU throughput resolved through the shared variant policy, Cosmos DB is authoritative business or durable operational state, Azure SQL is not authoritative state, and repository evidence indicates regional multi-write intent, infer:

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

A governed RU default satisfies only the throughput-model predicate. Preserve
the other conditions and the existing confirmation paths: approved target context
may establish target intent, while repository-only scenario inference remains
conditional. Never set the Kafka scenario source to an architecture context merely
because the variant used an organization default.

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

#### Rule 4: DSE Cassandra active-active

When the selected Kafka policy's DSE Cassandra predicates are satisfied, preserve
`KAFKA-SCENARIO-004` and its approved-context and local-affinity requirements.
Do not use this rule for Cosmos DB or for an unresolved scenario.

#### Rule 5: Unresolved

Use:

```yaml
value: unresolved
rule_id: KAFKA-SCENARIO-005
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
    policy_version: "3.3.0"
    rule_id: KAFKA-SCENARIO-001|KAFKA-SCENARIO-002|KAFKA-SCENARIO-003|KAFKA-SCENARIO-004|KAFKA-SCENARIO-005
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
  workloads: []
  frontend:
    detection_status: <skipped_by_scope|detected|not_detected|unknown>
    framework: <angular|react|unclassified|none>
    framework_version: <value-or-unknown>
    version_basis: <lockfile|declared_range|unknown>
    data_layers: []
    ssr_detected: <true|false|unknown>
    ssr_mode: <value-or-none>

dependency_summary:
  confirmed_dependencies: []
  declared_only_dependencies: []
  architecture_activated_standards: []
  dependency_standards_to_load: []
  standard_resolution_summary:
    candidates: 0
    activated_production_dependency: []
    activated_approved_capability: []
    not_activated: []
    not_applicable: []

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
- Verify every standard in the list records an `activation_route`, an `activation_signal`, its `evaluation_mode`, and the evidence that produced it.
- Verify every standard activated through `production_dependency` has production-code evidence or a dependency-specific production pattern match.
- Verify standards activated through `approved_target_platform_capability` are present with `evaluation_mode: repository_verifiable_controls_only`, come from approved context, belong to registry entries with `capability_activation_allowed: true`, and were not omitted for lack of a platform SDK, manifest, deployed state, or production-code evidence.
- Verify the `standard_resolution` record count equals the registry entry count under `standards` plus `assessment_domain_standards`, and every non-activated record carries an allowed `exclusion_reason`.
- Verify every activated standard is `in_scope` or declares no shared service.
- Verify no standard appears without a matched registry signal.
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
Use `grounding/governance/resiliency-finding-qualification-policy.yml` version 1.1.0. Preserve every evidence-backed applicable control violation as either `resiliency` or `non_resiliency`. Do not suppress a valid non-resiliency finding merely because it fails the resiliency gate. Resiliency classification requires a credible failure scenario, approved resiliency domain, target-architecture element, causal mechanism, and material impact. Preserve classification and rationale across phase artifacts. Business-logic risk remains a separate implementation-approval dimension.

### Phase-specific rule
Inventory applicable target architecture elements and credible failure scenarios needed by Step 2; do not classify findings in Step 1.

### Shared-Service Assessment Scope Resolution

Read `grounding/governance/shared-service-assessment-scope-schema.yml` and `architecture_context.shared_service_assessment_scope`. Resolve one effective scope for every confirmed or architecture-declared shared service. Inventory all services regardless of scope. Add dependency standards to the control-evaluation load list only for `in_scope` services. Preserve non-in-scope services in dependency and architecture inventories. Do not create findings in Step 1. Emit `shared_service_scope_resolution` records with service key, production-use status, effective scope, scope source, rationale, scope owner, architecture reasoning allowed, observations allowed, findings allowed, remediation allowed, and conflicts. Preserve a categorized `shared_service_assessment_scope_summary` in the authoritative inventory and Step 1 handoff. Repository evidence must not silently expand approved scope; route conflicts to architecture governance.



## DSE Cassandra and Kafka Active-Active Inventory Contract

When approved context selects DSE Cassandra authoritative state and active-active targets, inventory and hand off DSE scenario, datacenters, local affinity, consistency contract, Kafka scenario, regional processing model, cluster model, mirroring contract, offset recovery, external side effects, and scope. Do not infer deployed topology.
