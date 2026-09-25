---
schema_version: 2.2.0
document_type: dependency_behavior
service: cosmosdb
service_name: Azure Cosmos DB
language: java
framework: spring-boot
runtime_platform: aks
assessment_scope: application_code_only
lifecycle_status: active
assessment:
  enabled: true
  emit_findings: true
  include_in_score: true
  unknown_evidence_status: not_assessed
infrastructure_assumptions:
- Two independent Azure regions are provisioned and active.
- AKS, networking, private endpoints, DNS, identities, certificates, and dependent services follow the
  approved active-active infrastructure design.
- The deployment pipeline injects region-specific configuration into the same application artifact.
- The application repository does not provision or validate infrastructure.
controls:
- id: COSMOS-001
  title: Cosmos endpoint and preferred region are deployment-injected
  severity: critical
  category: configuration
  evidence_patterns:
  - spring.cloud.azure.cosmos
  - preferredRegions
  - CosmosClientBuilder
  finding_when: endpoint or preferred region is hardcoded
  emit_on_failure: true
  business_logic_risk: low
  requires_approval_before_implementation: false
  approval_owner: architecture
  safe_remediation_without_approval:
  - Externalize an existing hardcoded value to configuration while preserving the same effective default.
  - Add or improve metrics, logs, traces, and health details without changing decisions or payload content.
  - Add tests that characterize and lock in current behavior.
  requires_approval_for:
  - Changing the effective endpoint or preferred-region list.
- id: COSMOS-002
  title: Client uses local-region preference and approved endpoint discovery
  severity: critical
  category: regional-affinity
  evidence_patterns:
  - preferredRegions
  - endpointDiscoveryEnabled
  finding_when: client can route normally to another region or disables discovery without approved reason
  emit_on_failure: true
  business_logic_risk: severe
  requires_approval_before_implementation: true
  approval_owner: architecture
  safe_remediation_without_approval:
  - Add telemetry showing which region served each operation.
  - Add tests that demonstrate the current behavior and the failure mode.
  requires_approval_for:
  - Changing preferred regions or endpoint discovery where it alters read/write routing.
- id: COSMOS-003
  title: SDK retry and timeout budgets are explicit
  severity: high
  category: resilience
  evidence_patterns:
  - throttlingRetryOptions
  - requestTimeout
  - RetryOptions
  finding_when: retry or timeout behavior is absent or unbounded
  emit_on_failure: true
  business_logic_risk: moderate
  requires_approval_before_implementation: false
  approval_owner: architecture
  safe_remediation_without_approval:
  - Add retry and timeout telemetry including RU charge.
  - Add tests that demonstrate the current behavior and the failure mode.
  requires_approval_for:
  - Reducing timeouts below observed successful operation duration.
  - Changing retry counts where RU cost or throttling behavior changes.
- id: COSMOS-004
  title: Reads and writes use the approved consistency and session-token strategy
  severity: critical
  category: consistency
  evidence_patterns:
  - consistencyLevel
  - session token
  finding_when: code assumes stronger cross-region consistency than configured or loses required session
    guarantees
  emit_on_failure: true
  business_logic_risk: severe
  requires_approval_before_implementation: true
  approval_owner: architecture_and_product
  safe_remediation_without_approval:
  - Add telemetry for session-token propagation and consistency level in use.
  - Add tests that demonstrate the current behavior and the failure mode.
  requires_approval_for:
  - Changing consistency level.
  - Changing session-token handling.
- id: COSMOS-005
  title: Writes use idempotency and optimistic concurrency where required
  severity: critical
  category: consistency
  evidence_patterns:
  - ETag
  - IfMatch
  - idempotency key
  - unique key
  finding_when: duplicate or concurrent multi-region writes can create inconsistent business state
  emit_on_failure: true
  business_logic_risk: severe
  requires_approval_before_implementation: true
  approval_owner: product_and_architecture
  safe_remediation_without_approval:
  - Add telemetry for ETag and conflict occurrence.
  - Add tests that demonstrate the current behavior and the failure mode.
  requires_approval_for:
  - Adding or changing optimistic concurrency where it changes which writes succeed.
  - Changing idempotency key derivation.
- id: COSMOS-006
  title: Critical Cosmos failure affects readiness without coupling liveness
  severity: critical
  category: health
  evidence_patterns:
  - cosmos HealthIndicator
  - readiness group
  finding_when: unusable data path remains ready or external failure kills liveness
  emit_on_failure: true
  business_logic_risk: severe
  requires_approval_before_implementation: true
  approval_owner: architecture_and_product
  safe_remediation_without_approval:
  - Add dependency-state telemetry.
  - Add tests that demonstrate the current behavior and the failure mode.
  requires_approval_for:
  - Adding Cosmos to readiness.
- id: COSMOS-007
  title: Application handles 429, transient transport, and regional failover responses
  severity: high
  category: resilience
  evidence_patterns:
  - CosmosException
  - statusCode
  - subStatusCode
  - retry after
  finding_when: errors are treated uniformly or generate retry storms
  emit_on_failure: true
  business_logic_risk: moderate
  requires_approval_before_implementation: false
  approval_owner: architecture
  safe_remediation_without_approval:
  - Add status-code and sub-status telemetry.
  - Add tests that demonstrate the current behavior and the failure mode.
  requires_approval_for:
  - Changing how specific status codes are classified into business outcomes.
- id: COSMOS-008
  title: Tests cover endpoint selection, conflict, throttling, failover, and recovery
  severity: high
  category: testing
  evidence_patterns:
  - Cosmos emulator
  - mock client
  - fault injection
  finding_when: active-active data behaviors are untested
  emit_on_failure: true
  business_logic_risk: none
  requires_approval_before_implementation: false
  approval_owner: none
  safe_remediation_without_approval:
  - Add tests that demonstrate the current behavior and the failure mode.
  requires_approval_for: []
- id: COSMOS-009
  title: Client is reused as a singleton with explicit connection mode and lifecycle
  severity: high
  category: resource-management
  evidence_patterns:
  - CosmosAsyncClient
  - singleton
  - ConnectionMode
  - client close
  finding_when: clients are created per request or per operation, or client lifecycle and connection mode
    are undefined
  emit_on_failure: true
  business_logic_risk: low
  requires_approval_before_implementation: false
  approval_owner: architecture
  safe_remediation_without_approval:
  - Convert per-request client creation to a managed singleton preserving identical configuration.
  - Add or improve metrics, logs, traces, and health details without changing decisions or payload content.
  - Add tests that characterize and lock in current behavior.
  requires_approval_for:
  - Changing connection mode.
  - Changing effective client configuration.
- id: COSMOS-010
  title: Credentials use approved identity with supported rotation
  severity: critical
  category: security
  evidence_patterns:
  - DefaultAzureCredential
  - managed identity
  - account key
  - key rotation
  finding_when: account keys are embedded or logged, or credential rotation requires an application restart
    without an approved contract
  emit_on_failure: true
  business_logic_risk: severe
  requires_approval_before_implementation: true
  approval_owner: security
  safe_remediation_without_approval:
  - Add credential-failure telemetry with values redacted.
  - Add tests that demonstrate the current behavior and the failure mode.
  requires_approval_for:
  - Changing credential type or authentication flow.
- id: COSMOS-011
  title: Partition key strategy avoids hot partitions and unbounded cross-partition queries
  severity: critical
  category: data-model
  evidence_patterns:
  - partitionKey
  - cross partition
  - queryCrossPartition
  - partition key path
  finding_when: the partition strategy concentrates load on a single logical partition or relies on unbounded
    cross-partition queries in hot paths
  emit_on_failure: true
  business_logic_risk: severe
  requires_approval_before_implementation: true
  approval_owner: architecture_and_data
  safe_remediation_without_approval:
  - Add or improve metrics, logs, traces, and health details without changing decisions or payload content.
  - Add tests that characterize and lock in current behavior.
  - Add partition-distribution and RU-by-partition telemetry.
  requires_approval_for:
  - Changing the partition key.
  - Changing query patterns that alter returned data or ordering.
- id: COSMOS-012
  title: Queries paginate and bound result memory
  severity: high
  category: performance
  evidence_patterns:
  - continuation token
  - maxItemCount
  - byPage
  - iterableByPage
  finding_when: queries can return unbounded result sets into application memory or omit continuation
    handling
  emit_on_failure: true
  business_logic_risk: severe
  requires_approval_before_implementation: true
  approval_owner: product
  safe_remediation_without_approval:
  - Add result-size and continuation telemetry.
  - Add tests that demonstrate the current behavior and the failure mode.
  requires_approval_for:
  - Introducing pagination or item limits that can change the result set a caller receives.
- id: COSMOS-013
  title: Request-unit consumption and throttling are observable
  severity: high
  category: observability
  evidence_patterns:
  - requestCharge
  - RU
  - 429 metric
  - diagnostics
  finding_when: RU consumption, throttling, and latency cannot be observed or attributed to operations
    and regions
  emit_on_failure: true
  business_logic_risk: none
  requires_approval_before_implementation: false
  approval_owner: none
  safe_remediation_without_approval: &id001
  - Add or improve metrics, logs, traces, and health details without changing decisions or payload content.
  - Add tests that characterize and lock in current behavior.
  requires_approval_for: []
- id: COSMOS-014
  title: Conflict-resolution assumptions match the approved account policy
  severity: critical
  category: consistency
  evidence_patterns:
  - conflict resolution
  - last writer wins
  - conflict feed
  - _ts
  finding_when: application logic assumes a conflict-resolution behavior that is not established by the
    approved account configuration
  emit_on_failure: true
  business_logic_risk: severe
  requires_approval_before_implementation: true
  approval_owner: architecture_and_data
  safe_remediation_without_approval:
  - Add conflict-occurrence telemetry.
  - Add tests that demonstrate the current behavior and the failure mode.
  requires_approval_for:
  - Changing conflict-resolution assumptions or handling that determines which write wins.
- id: COSMOS-015
  title: Change-feed processing defines ownership, checkpointing, and duplicate handling
  severity: critical
  category: messaging
  evidence_patterns:
  - change feed
  - lease container
  - ChangeFeedProcessor
  - checkpoint
  finding_when: change-feed processing lacks defined lease ownership, checkpoint behavior, regional activation,
    or duplicate-safe handling
  emit_on_failure: true
  business_logic_risk: severe
  requires_approval_before_implementation: true
  approval_owner: architecture_and_product
  safe_remediation_without_approval:
  - Add change-feed lag, ownership, and checkpoint telemetry.
  - Add tests that demonstrate the current behavior and the failure mode.
  requires_approval_for:
  - Changing checkpoint frequency or position.
  - Changing which region or instance owns processing.
  - Changing duplicate handling.
- id: COSMOS-016
  title: Bulk and batch operations handle partial failure
  severity: high
  category: consistency
  evidence_patterns:
  - bulk
  - TransactionalBatch
  - batch response
  - partial failure
  finding_when: bulk or batch responses are not inspected for per-item failure or partial success is treated
    as full success
  emit_on_failure: true
  business_logic_risk: severe
  requires_approval_before_implementation: true
  approval_owner: product
  safe_remediation_without_approval:
  - Add per-item batch outcome telemetry.
  - Add tests that demonstrate the current behavior and the failure mode.
  requires_approval_for:
  - Changing batch partitioning or failure handling where partial success is currently accepted.
- id: COSMOS-017
  title: Document lifecycle assumptions such as TTL are explicit
  severity: medium
  category: data-model
  evidence_patterns:
  - ttl
  - expiration
  - soft delete
  - archival
  finding_when: business correctness depends on document retention or expiration behavior that is not
    explicitly defined in the application contract
  emit_on_failure: true
  business_logic_risk: severe
  requires_approval_before_implementation: true
  approval_owner: product_and_data
  safe_remediation_without_approval: *id001
  requires_approval_for:
  - Changing TTL, expiration, or deletion behavior.
- id: COSMOS-018
  title: Diagnostics and logging exclude sensitive data
  severity: critical
  category: security
  evidence_patterns:
  - diagnostics
  - log document
  - PII
  - activityId
  finding_when: document contents, keys, query parameters, or personal data can be written to logs or
    diagnostics output
  emit_on_failure: true
  business_logic_risk: low
  requires_approval_before_implementation: false
  approval_owner: security
  safe_remediation_without_approval:
  - Add or strengthen redaction.
  - Add or improve metrics, logs, traces, and health details without changing decisions or payload content.
  - Add tests that characterize and lock in current behavior.
  requires_approval_for:
  - Weakening existing redaction.
- id: COSMOS-019
  title: Recovery after regional or endpoint failover occurs without restart
  severity: high
  category: recovery
  evidence_patterns:
  - endpoint refresh
  - client recovery
  - reconnect
  - stale endpoint
  finding_when: the application requires a restart to resume normal operation after a Cosmos endpoint
    or regional transition
  emit_on_failure: true
  business_logic_risk: moderate
  requires_approval_before_implementation: false
  approval_owner: architecture
  safe_remediation_without_approval:
  - Add recovery telemetry.
  - Add tests that demonstrate the current behavior and the failure mode.
  requires_approval_for:
  - Changing client recovery behavior that alters routing.
- id: COSMOS-020
  title: Cross-store workflows define reconciliation
  severity: critical
  category: consistency
  evidence_patterns:
  - Cosmos and SQL
  - Cosmos and Kafka
  - outbox
  - reconciliation
  finding_when: Cosmos and another store, broker, or external provider can diverge without durable intent,
    compensation, or reconciliation
  emit_on_failure: true
  business_logic_risk: severe
  requires_approval_before_implementation: true
  approval_owner: architecture_and_product
  safe_remediation_without_approval:
  - Add divergence-detection telemetry.
  - Add tests that demonstrate the current behavior and the failure mode.
  requires_approval_for:
  - Introducing an outbox, compensation, or reconciliation flow that changes transaction boundaries or
    publish ordering.
business_logic_risk_classification:
  enabled: true
  levels:
  - none
  - low
  - moderate
  - severe
  severe_requires_approval: true
  risk_never_suppresses_findings: true
---

# Azure Cosmos DB Target-State Application Behavior Standard

### Shared-service operating-model contract

This standard does not select the application's shared-service topology. Resolve the operating model from:

```text
architecture_context.shared_service_operating_models.services.cosmosdb
```

Use `source.operating_model` only to describe current state. Use `target.operating_model` for control applicability and target-state code-readiness assessment.

- Evaluate common client controls whenever production use is confirmed.
- Evaluate model-specific controls only for the resolved target operating model.
- `not_applicable` plus no repository production use makes this standard not applicable.
- `not_applicable` plus confirmed repository production use is a context conflict, not an automatic code finding.
- Missing, unresolved, or conflicting target model makes model-specific controls `not_assessed` and routes to architecture review.
- A source-target difference is migration context, not a finding by itself.
- Findings require repository-owned evidence that the application is incompatible with an applicable target-state control.
- Do not infer deployed topology from this standard's title, examples, or assumptions.

## Purpose

This dependency-specific standard assesses how a Spring Boot microservice uses Azure Cosmos DB when evaluated for the approved target operating model supplied by application architecture context. The local regional service endpoint is assumed to exist and be reachable through the approved private networking design.

## Scope boundary

This standard assesses **application code, application configuration checked into the repository, and automated tests only**. It does not assess whether Azure or third-party infrastructure has been deployed correctly.

## Mandatory assumptions

- Two independent Azure regions are provisioned and active.
- AKS, networking, private endpoints, DNS, identities, certificates, and dependent services follow the approved active-active infrastructure design.
- The deployment pipeline injects region-specific configuration into the same application artifact.
- The application repository does not provision or validate infrastructure.

## Evaluator workflow

- Confirm the dependency is actually used by production code.
- Resolve source and target models from `architecture_context.shared_service_operating_models.services.cosmosdb` before evaluating model-specific controls.
- Locate client construction, configuration binding, error handling, health integration, telemetry, and tests.
- Evaluate only controls supported by repository evidence.
- Separate framework defaults from explicit application behavior. Flag reliance on a default only when the assessment requires explicit configuration or the default does not meet the failure budget.
- Do not recommend deploying infrastructure. Recommend application code, configuration contract, health behavior, telemetry, or testing changes.
- Link each finding to exactly one primary control and list related controls separately.
- Do not emit a finding for a dependency that is not used.
- Record each finding's `business_logic_risk`, `requires_approval_before_implementation`, and `approval_owner` so Step 3A can set the change boundary correctly.
- A `severe` control may produce a finding, but its behavior-changing remediation must be classified `approval_required: true` and blocked from Step 4 until approval is recorded.

## Required statuses

- `compliant`: Repository evidence demonstrates the behavior.
- `non_compliant`: Repository evidence demonstrates a gap.
- `not_assessed`: Evidence is unavailable or insufficient.
- `not_applicable`: The dependency or behavior does not apply.
- `accepted_risk`: A cited approved exception exists.

## Evidence and locator rules

Use this source-locator precedence: repository path, symbol or configuration key, exact original source excerpt, source fingerprint, assessment snapshot, and original assessed line range. Line numbers are advisory navigation metadata and may drift. Do not require a Git repository or commit SHA to record evidence.

## Global quality caveats

- Resiliency remediation must preserve existing business semantics, partner-contract interpretation, security controls, and privacy behavior unless an approved decision authorizes a change.
- Do not retry a non-idempotent operation after an ambiguous outcome unless stable identity, status lookup, or reconciliation makes replay safe.
- A random identifier generated per attempt is correlation, not idempotency.
- Do not add every dependency to readiness, and never add an external dependency to liveness.
- Timeout, retry, pool, batch, concurrency, and cache values are illustrative unless approved and must remain externally configurable.
- Missing deployed or externally owned evidence is an evidence gap, not application noncompliance.

## Business-logic risk classification

Every control in this standard carries a `business_logic_risk` classification. The classification governs what may be implemented without approval. It does not change whether a finding may be raised.

| Level | Meaning |
|---|---|
| `none` | Remediation cannot change business behavior, partner contracts, security, or privacy. |
| `low` | Remediation is normally behavior-preserving but must be verified. |
| `moderate` | Remediation can change timing, capacity, resource, or failure behavior under load. |
| `severe` | Remediation can change business semantics, data, partner contracts, security, or privacy. |

Rules:

- A control at any risk level may produce a finding when repository evidence supports it. Risk classification never suppresses detection.
- Step 3A must set `approval_required: true` for every change whose primary or related control is `severe`, or where `requires_approval_before_implementation` is `true`.
- Step 3A may plan and Step 4 may implement the `safe_remediation_without_approval` items for any control without approval, provided they do not alter business behavior.
- Step 4 must not implement any item listed under `requires_approval_for` unless an explicit approval record exists naming the `approval_owner`.
- When a control is `severe` and approval is unavailable, Step 3A must still produce the observability, characterization-test, and evidence work as an implementable target, and mark the behavior-changing portion blocked.
- Step 5 must treat an unapproved behavior change as an implementation-scope violation and must not close the associated finding.

## Controls

### COSMOS-001: Cosmos endpoint and preferred region are deployment-injected

**Severity:** Critical  
**Category:** configuration

#### Requirement

The application code and configuration must satisfy this behavior when the same artifact runs in either active region.

#### Repository evidence to inspect

- `spring.cloud.azure.cosmos`
- `preferredRegions`
- `CosmosClientBuilder`

#### Finding condition

Emit a finding when evidence shows that endpoint or preferred region is hardcoded.

#### Evidence rule

Cite the file path, symbol or property, and advisory line range when available. Evaluate effective behavior rather than the presence of a library, annotation, or property alone. If the repository does not contain enough evidence, return `not_assessed` rather than assuming noncompliance.

#### Business-logic risk

**Risk level:** `low`  
**Requires approval before implementation:** `false`  
**Approval owner:** `architecture`

**Safe remediation without approval:**

- Externalize an existing hardcoded value to configuration while preserving the same effective default.
- Add or improve metrics, logs, traces, and health details without changing decisions or payload content.
- Add tests that characterize and lock in current behavior.

**Requires approval for:**

- Changing the effective endpoint or preferred-region list.

---

### COSMOS-002: Client uses local-region preference and approved endpoint discovery

**Severity:** Critical  
**Category:** regional-affinity

#### Requirement

The application code and configuration must satisfy this behavior when the same artifact runs in either active region.

#### Repository evidence to inspect

- `preferredRegions`
- `endpointDiscoveryEnabled`

#### Finding condition

Emit a finding when evidence shows that client can route normally to another region or disables discovery without approved reason.

#### Evidence rule

Cite the file path, symbol or property, and advisory line range when available. Evaluate effective behavior rather than the presence of a library, annotation, or property alone. If the repository does not contain enough evidence, return `not_assessed` rather than assuming noncompliance.

#### Business-logic risk

**Risk level:** `severe`  
**Requires approval before implementation:** `true`  
**Approval owner:** `architecture`

**Safe remediation without approval:**

- Add telemetry showing which region served each operation.
- Add tests that demonstrate the current behavior and the failure mode.

**Requires approval for:**

- Changing preferred regions or endpoint discovery where it alters read/write routing.

---

### COSMOS-003: SDK retry and timeout budgets are explicit

**Severity:** High  
**Category:** resilience

#### Requirement

The application code and configuration must satisfy this behavior when the same artifact runs in either active region.

#### Repository evidence to inspect

- `throttlingRetryOptions`
- `requestTimeout`
- `RetryOptions`

#### Finding condition

Emit a finding when evidence shows that retry or timeout behavior is absent or unbounded.

#### Evidence rule

Cite the file path, symbol or property, and advisory line range when available. Evaluate effective behavior rather than the presence of a library, annotation, or property alone. If the repository does not contain enough evidence, return `not_assessed` rather than assuming noncompliance.

#### Business-logic risk

**Risk level:** `moderate`  
**Requires approval before implementation:** `false`  
**Approval owner:** `architecture`

**Safe remediation without approval:**

- Add retry and timeout telemetry including RU charge.
- Add tests that demonstrate the current behavior and the failure mode.

**Requires approval for:**

- Reducing timeouts below observed successful operation duration.
- Changing retry counts where RU cost or throttling behavior changes.

---

### COSMOS-004: Reads and writes use the approved consistency and session-token strategy

**Severity:** Critical  
**Category:** consistency

#### Requirement

The application code and configuration must satisfy this behavior when the same artifact runs in either active region.

#### Repository evidence to inspect

- `consistencyLevel`
- `session token`

#### Finding condition

Emit a finding when evidence shows that code assumes stronger cross-region consistency than configured or loses required session guarantees.

#### Evidence rule

Cite the file path, symbol or property, and advisory line range when available. Evaluate effective behavior rather than the presence of a library, annotation, or property alone. If the repository does not contain enough evidence, return `not_assessed` rather than assuming noncompliance.

#### Business-logic risk

**Risk level:** `severe`  
**Requires approval before implementation:** `true`  
**Approval owner:** `architecture_and_product`

**Safe remediation without approval:**

- Add telemetry for session-token propagation and consistency level in use.
- Add tests that demonstrate the current behavior and the failure mode.

**Requires approval for:**

- Changing consistency level.
- Changing session-token handling.

---

### COSMOS-005: Writes use idempotency and optimistic concurrency where required

**Severity:** Critical  
**Category:** consistency

#### Requirement

The application code and configuration must satisfy this behavior when the same artifact runs in either active region.

#### Repository evidence to inspect

- `ETag`
- `IfMatch`
- `idempotency key`
- `unique key`

#### Finding condition

Emit a finding when evidence shows that duplicate or concurrent multi-region writes can create inconsistent business state.

#### Evidence rule

Cite the file path, symbol or property, and advisory line range when available. Evaluate effective behavior rather than the presence of a library, annotation, or property alone. If the repository does not contain enough evidence, return `not_assessed` rather than assuming noncompliance.

#### Business-logic risk

**Risk level:** `severe`  
**Requires approval before implementation:** `true`  
**Approval owner:** `product_and_architecture`

**Safe remediation without approval:**

- Add telemetry for ETag and conflict occurrence.
- Add tests that demonstrate the current behavior and the failure mode.

**Requires approval for:**

- Adding or changing optimistic concurrency where it changes which writes succeed.
- Changing idempotency key derivation.

---

### COSMOS-006: Critical Cosmos failure affects readiness without coupling liveness

**Severity:** Critical  
**Category:** health

#### Requirement

The application code and configuration must satisfy this behavior when the same artifact runs in either active region.

#### Repository evidence to inspect

- `cosmos HealthIndicator`
- `readiness group`

#### Finding condition

Emit a finding when evidence shows that unusable data path remains ready or external failure kills liveness.

#### Evidence rule

Cite the file path, symbol or property, and advisory line range when available. Evaluate effective behavior rather than the presence of a library, annotation, or property alone. If the repository does not contain enough evidence, return `not_assessed` rather than assuming noncompliance.

#### Business-logic risk

**Risk level:** `severe`  
**Requires approval before implementation:** `true`  
**Approval owner:** `architecture_and_product`

**Safe remediation without approval:**

- Add dependency-state telemetry.
- Add tests that demonstrate the current behavior and the failure mode.

**Requires approval for:**

- Adding Cosmos to readiness.

---

### COSMOS-007: Application handles 429, transient transport, and regional failover responses

**Severity:** High  
**Category:** resilience

#### Requirement

The application code and configuration must satisfy this behavior when the same artifact runs in either active region.

#### Repository evidence to inspect

- `CosmosException`
- `statusCode`
- `subStatusCode`
- `retry after`

#### Finding condition

Emit a finding when evidence shows that errors are treated uniformly or generate retry storms.

#### Evidence rule

Cite the file path, symbol or property, and advisory line range when available. Evaluate effective behavior rather than the presence of a library, annotation, or property alone. If the repository does not contain enough evidence, return `not_assessed` rather than assuming noncompliance.

#### Business-logic risk

**Risk level:** `moderate`  
**Requires approval before implementation:** `false`  
**Approval owner:** `architecture`

**Safe remediation without approval:**

- Add status-code and sub-status telemetry.
- Add tests that demonstrate the current behavior and the failure mode.

**Requires approval for:**

- Changing how specific status codes are classified into business outcomes.

---

### COSMOS-008: Tests cover endpoint selection, conflict, throttling, failover, and recovery

**Severity:** High  
**Category:** testing

#### Requirement

The application code and configuration must satisfy this behavior when the same artifact runs in either active region.

#### Repository evidence to inspect

- `Cosmos emulator`
- `mock client`
- `fault injection`

#### Finding condition

Emit a finding when evidence shows that active-active data behaviors are untested.

#### Evidence rule

Cite the file path, symbol or property, and advisory line range when available. Evaluate effective behavior rather than the presence of a library, annotation, or property alone. If the repository does not contain enough evidence, return `not_assessed` rather than assuming noncompliance.

#### Business-logic risk

**Risk level:** `none`  
**Requires approval before implementation:** `false`  
**Approval owner:** `none`

**Safe remediation without approval:**

- Add tests that demonstrate the current behavior and the failure mode.

---

### COSMOS-009: Client is reused as a singleton with explicit connection mode and lifecycle

**Severity:** High  
**Category:** resource-management

#### Requirement

The application code and configuration must satisfy this behavior when the same artifact runs in either active region.

#### Repository evidence to inspect

- `CosmosAsyncClient`
- `singleton`
- `ConnectionMode`
- `client close`

#### Finding condition

Emit a finding when evidence shows that clients are created per request or per operation, or client lifecycle and connection mode are undefined.

#### Evidence rule

Cite the file path, symbol or property, and advisory line range when available. Evaluate effective behavior rather than the presence of a library, annotation, or property alone. If the repository does not contain enough evidence, return `not_assessed` rather than assuming noncompliance.

#### Quality caveats

- Client creation is expensive and affects connection, routing, and throughput behavior.

#### Business-logic risk

**Risk level:** `low`  
**Requires approval before implementation:** `false`  
**Approval owner:** `architecture`

**Safe remediation without approval:**

- Convert per-request client creation to a managed singleton preserving identical configuration.
- Add or improve metrics, logs, traces, and health details without changing decisions or payload content.
- Add tests that characterize and lock in current behavior.

**Requires approval for:**

- Changing connection mode.
- Changing effective client configuration.

---

### COSMOS-010: Credentials use approved identity with supported rotation

**Severity:** Critical  
**Category:** security

#### Requirement

The application code and configuration must satisfy this behavior when the same artifact runs in either active region.

#### Repository evidence to inspect

- `DefaultAzureCredential`
- `managed identity`
- `account key`
- `key rotation`

#### Finding condition

Emit a finding when evidence shows that account keys are embedded or logged, or credential rotation requires an application restart without an approved contract.

#### Evidence rule

Cite the file path, symbol or property, and advisory line range when available. Evaluate effective behavior rather than the presence of a library, annotation, or property alone. If the repository does not contain enough evidence, return `not_assessed` rather than assuming noncompliance.

#### Quality caveats

- Do not weaken identity controls to simplify recovery behavior.

#### Business-logic risk

**Risk level:** `severe`  
**Requires approval before implementation:** `true`  
**Approval owner:** `security`

**Safe remediation without approval:**

- Add credential-failure telemetry with values redacted.
- Add tests that demonstrate the current behavior and the failure mode.

**Requires approval for:**

- Changing credential type or authentication flow.

---

### COSMOS-011: Partition key strategy avoids hot partitions and unbounded cross-partition queries

**Severity:** Critical  
**Category:** data-model

#### Requirement

The application code and configuration must satisfy this behavior when the same artifact runs in either active region.

#### Repository evidence to inspect

- `partitionKey`
- `cross partition`
- `queryCrossPartition`
- `partition key path`

#### Finding condition

Emit a finding when evidence shows that the partition strategy concentrates load on a single logical partition or relies on unbounded cross-partition queries in hot paths.

#### Evidence rule

Cite the file path, symbol or property, and advisory line range when available. Evaluate effective behavior rather than the presence of a library, annotation, or property alone. If the repository does not contain enough evidence, return `not_assessed` rather than assuming noncompliance.

#### Quality caveats

- Partition key changes are data-model decisions that require architecture approval.

#### Business-logic risk

**Risk level:** `severe`  
**Requires approval before implementation:** `true`  
**Approval owner:** `architecture_and_data`

**Safe remediation without approval:**

- Add or improve metrics, logs, traces, and health details without changing decisions or payload content.
- Add tests that characterize and lock in current behavior.
- Add partition-distribution and RU-by-partition telemetry.

**Requires approval for:**

- Changing the partition key.
- Changing query patterns that alter returned data or ordering.

---

### COSMOS-012: Queries paginate and bound result memory

**Severity:** High  
**Category:** performance

#### Requirement

The application code and configuration must satisfy this behavior when the same artifact runs in either active region.

#### Repository evidence to inspect

- `continuation token`
- `maxItemCount`
- `byPage`
- `iterableByPage`

#### Finding condition

Emit a finding when evidence shows that queries can return unbounded result sets into application memory or omit continuation handling.

#### Evidence rule

Cite the file path, symbol or property, and advisory line range when available. Evaluate effective behavior rather than the presence of a library, annotation, or property alone. If the repository does not contain enough evidence, return `not_assessed` rather than assuming noncompliance.

#### Quality caveats

- Pagination must preserve correct business results, not silently truncate data.

#### Business-logic risk

**Risk level:** `severe`  
**Requires approval before implementation:** `true`  
**Approval owner:** `product`

**Safe remediation without approval:**

- Add result-size and continuation telemetry.
- Add tests that demonstrate the current behavior and the failure mode.

**Requires approval for:**

- Introducing pagination or item limits that can change the result set a caller receives.

---

### COSMOS-013: Request-unit consumption and throttling are observable

**Severity:** High  
**Category:** observability

#### Requirement

The application code and configuration must satisfy this behavior when the same artifact runs in either active region.

#### Repository evidence to inspect

- `requestCharge`
- `RU`
- `429 metric`
- `diagnostics`

#### Finding condition

Emit a finding when evidence shows that RU consumption, throttling, and latency cannot be observed or attributed to operations and regions.

#### Evidence rule

Cite the file path, symbol or property, and advisory line range when available. Evaluate effective behavior rather than the presence of a library, annotation, or property alone. If the repository does not contain enough evidence, return `not_assessed` rather than assuming noncompliance.

#### Quality caveats

- Avoid emitting full diagnostics strings that may contain sensitive data or create unbounded cardinality.

#### Business-logic risk

**Risk level:** `none`  
**Requires approval before implementation:** `false`  
**Approval owner:** `none`

**Safe remediation without approval:**

- Add or improve metrics, logs, traces, and health details without changing decisions or payload content.
- Add tests that characterize and lock in current behavior.

---

### COSMOS-014: Conflict-resolution assumptions match the approved account policy

**Severity:** Critical  
**Category:** consistency

#### Requirement

The application code and configuration must satisfy this behavior when the same artifact runs in either active region.

#### Repository evidence to inspect

- `conflict resolution`
- `last writer wins`
- `conflict feed`
- `_ts`

#### Finding condition

Emit a finding when evidence shows that application logic assumes a conflict-resolution behavior that is not established by the approved account configuration.

#### Evidence rule

Cite the file path, symbol or property, and advisory line range when available. Evaluate effective behavior rather than the presence of a library, annotation, or property alone. If the repository does not contain enough evidence, return `not_assessed` rather than assuming noncompliance.

#### Quality caveats

- Actual account configuration is external evidence; assess the assumption expressed by the application.

#### Business-logic risk

**Risk level:** `severe`  
**Requires approval before implementation:** `true`  
**Approval owner:** `architecture_and_data`

**Safe remediation without approval:**

- Add conflict-occurrence telemetry.
- Add tests that demonstrate the current behavior and the failure mode.

**Requires approval for:**

- Changing conflict-resolution assumptions or handling that determines which write wins.

---

### COSMOS-015: Change-feed processing defines ownership, checkpointing, and duplicate handling

**Severity:** Critical  
**Category:** messaging

#### Requirement

The application code and configuration must satisfy this behavior when the same artifact runs in either active region.

#### Repository evidence to inspect

- `change feed`
- `lease container`
- `ChangeFeedProcessor`
- `checkpoint`

#### Finding condition

Emit a finding when evidence shows that change-feed processing lacks defined lease ownership, checkpoint behavior, regional activation, or duplicate-safe handling.

#### Evidence rule

Cite the file path, symbol or property, and advisory line range when available. Evaluate effective behavior rather than the presence of a library, annotation, or property alone. If the repository does not contain enough evidence, return `not_assessed` rather than assuming noncompliance.

#### Quality caveats

- Change-feed delivery is at-least-once; duplicate-safe processing is required.

#### Business-logic risk

**Risk level:** `severe`  
**Requires approval before implementation:** `true`  
**Approval owner:** `architecture_and_product`

**Safe remediation without approval:**

- Add change-feed lag, ownership, and checkpoint telemetry.
- Add tests that demonstrate the current behavior and the failure mode.

**Requires approval for:**

- Changing checkpoint frequency or position.
- Changing which region or instance owns processing.
- Changing duplicate handling.

---

### COSMOS-016: Bulk and batch operations handle partial failure

**Severity:** High  
**Category:** consistency

#### Requirement

The application code and configuration must satisfy this behavior when the same artifact runs in either active region.

#### Repository evidence to inspect

- `bulk`
- `TransactionalBatch`
- `batch response`
- `partial failure`

#### Finding condition

Emit a finding when evidence shows that bulk or batch responses are not inspected for per-item failure or partial success is treated as full success.

#### Evidence rule

Cite the file path, symbol or property, and advisory line range when available. Evaluate effective behavior rather than the presence of a library, annotation, or property alone. If the repository does not contain enough evidence, return `not_assessed` rather than assuming noncompliance.

#### Quality caveats

- Transactional batch semantics apply only within a single logical partition.

#### Business-logic risk

**Risk level:** `severe`  
**Requires approval before implementation:** `true`  
**Approval owner:** `product`

**Safe remediation without approval:**

- Add per-item batch outcome telemetry.
- Add tests that demonstrate the current behavior and the failure mode.

**Requires approval for:**

- Changing batch partitioning or failure handling where partial success is currently accepted.

---

### COSMOS-017: Document lifecycle assumptions such as TTL are explicit

**Severity:** Medium  
**Category:** data-model

#### Requirement

The application code and configuration must satisfy this behavior when the same artifact runs in either active region.

#### Repository evidence to inspect

- `ttl`
- `expiration`
- `soft delete`
- `archival`

#### Finding condition

Emit a finding when evidence shows that business correctness depends on document retention or expiration behavior that is not explicitly defined in the application contract.

#### Evidence rule

Cite the file path, symbol or property, and advisory line range when available. Evaluate effective behavior rather than the presence of a library, annotation, or property alone. If the repository does not contain enough evidence, return `not_assessed` rather than assuming noncompliance.

#### Quality caveats

- TTL configuration may be external; assess the application assumption and recovery behavior.

#### Business-logic risk

**Risk level:** `severe`  
**Requires approval before implementation:** `true`  
**Approval owner:** `product_and_data`

**Safe remediation without approval:**

- Add or improve metrics, logs, traces, and health details without changing decisions or payload content.
- Add tests that characterize and lock in current behavior.

**Requires approval for:**

- Changing TTL, expiration, or deletion behavior.

---

### COSMOS-018: Diagnostics and logging exclude sensitive data

**Severity:** Critical  
**Category:** security

#### Requirement

The application code and configuration must satisfy this behavior when the same artifact runs in either active region.

#### Repository evidence to inspect

- `diagnostics`
- `log document`
- `PII`
- `activityId`

#### Finding condition

Emit a finding when evidence shows that document contents, keys, query parameters, or personal data can be written to logs or diagnostics output.

#### Evidence rule

Cite the file path, symbol or property, and advisory line range when available. Evaluate effective behavior rather than the presence of a library, annotation, or property alone. If the repository does not contain enough evidence, return `not_assessed` rather than assuming noncompliance.

#### Quality caveats

- Correlation identifiers are acceptable; document payloads generally are not.

#### Business-logic risk

**Risk level:** `low`  
**Requires approval before implementation:** `false`  
**Approval owner:** `security`

**Safe remediation without approval:**

- Add or strengthen redaction.
- Add or improve metrics, logs, traces, and health details without changing decisions or payload content.
- Add tests that characterize and lock in current behavior.

**Requires approval for:**

- Weakening existing redaction.

---

### COSMOS-019: Recovery after regional or endpoint failover occurs without restart

**Severity:** High  
**Category:** recovery

#### Requirement

The application code and configuration must satisfy this behavior when the same artifact runs in either active region.

#### Repository evidence to inspect

- `endpoint refresh`
- `client recovery`
- `reconnect`
- `stale endpoint`

#### Finding condition

Emit a finding when evidence shows that the application requires a restart to resume normal operation after a Cosmos endpoint or regional transition.

#### Evidence rule

Cite the file path, symbol or property, and advisory line range when available. Evaluate effective behavior rather than the presence of a library, annotation, or property alone. If the repository does not contain enough evidence, return `not_assessed` rather than assuming noncompliance.

#### Quality caveats

- Recovery must be demonstrated by tests rather than assumed from SDK defaults.

#### Business-logic risk

**Risk level:** `moderate`  
**Requires approval before implementation:** `false`  
**Approval owner:** `architecture`

**Safe remediation without approval:**

- Add recovery telemetry.
- Add tests that demonstrate the current behavior and the failure mode.

**Requires approval for:**

- Changing client recovery behavior that alters routing.

---

### COSMOS-020: Cross-store workflows define reconciliation

**Severity:** Critical  
**Category:** consistency

#### Requirement

The application code and configuration must satisfy this behavior when the same artifact runs in either active region.

#### Repository evidence to inspect

- `Cosmos and SQL`
- `Cosmos and Kafka`
- `outbox`
- `reconciliation`

#### Finding condition

Emit a finding when evidence shows that Cosmos and another store, broker, or external provider can diverge without durable intent, compensation, or reconciliation.

#### Evidence rule

Cite the file path, symbol or property, and advisory line range when available. Evaluate effective behavior rather than the presence of a library, annotation, or property alone. If the repository does not contain enough evidence, return `not_assessed` rather than assuming noncompliance.

#### Quality caveats

- A Cosmos operation cannot atomically include an external system.

#### Business-logic risk

**Risk level:** `severe`  
**Requires approval before implementation:** `true`  
**Approval owner:** `architecture_and_product`

**Safe remediation without approval:**

- Add divergence-detection telemetry.
- Add tests that demonstrate the current behavior and the failure mode.

**Requires approval for:**

- Introducing an outbox, compensation, or reconciliation flow that changes transaction boundaries or publish ordering.

---

## Standard finding format

- **Title:** [specific code-level gap]
- **Control:** [COSMOS-NNN]
- **Related controls:** [control IDs]
- **Severity:** [severity]
- **Repository evidence:** [path, symbol/property, advisory lines, exact excerpt]
- **Observed behavior:** [what code currently does]
- **Active-active risk:** [effect during regional dependency or network failure]
- **Required code/configuration change:** [specific remediation]
- **Validation test:** [test that proves the behavior]
- **Confidence:** [high, medium, low]

## Non-findings

Do not create infrastructure findings such as missing second-region resources, private endpoints, zone redundancy, geo-replication, capacity, DNS, or global load-balancer configuration. Those are assumed platform responsibilities and are outside this repository assessment.

Do not create findings for account-, namespace-, cluster-, or service-level configuration that the repository does not own. Record those as external evidence requirements. Do not create PCF findings, migration work, or modernization recommendations.
