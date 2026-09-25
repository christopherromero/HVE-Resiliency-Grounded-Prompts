---
schema_version: 2.2.0
document_type: dependency_behavior
service: eventhubs
service_name: Azure Event Hubs
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
- id: EH-001
  title: Namespace and event hub names are deployment-injected
  severity: critical
  category: configuration
  evidence_patterns:
  - spring.cloud.azure.eventhubs
  - fullyQualifiedNamespace
  - EVENTHUB_NAMESPACE
  finding_when: namespace is hardcoded
  emit_on_failure: true
  business_logic_risk: low
  requires_approval_before_implementation: false
  approval_owner: architecture
  safe_remediation_without_approval:
  - Externalize an existing hardcoded value to configuration while preserving the same effective default.
  - Add or improve metrics, logs, traces, and health details without changing decisions or payload content.
  - Add tests that characterize and lock in current behavior.
  requires_approval_for:
  - Changing the effective namespace or hub.
- id: EH-002
  title: Producer retries are bounded and preserve business idempotency
  severity: critical
  category: resilience
  evidence_patterns:
  - EventHubProducerClient
  - AmqpRetryOptions
  - idempotency key
  finding_when: producer retry can duplicate business effects without detection
  emit_on_failure: true
  business_logic_risk: severe
  requires_approval_before_implementation: true
  approval_owner: product
  safe_remediation_without_approval:
  - Add producer retry and outcome telemetry.
  - Add tests that demonstrate the current behavior and the failure mode.
  requires_approval_for:
  - Changing producer retry counts where duplicate publication risk changes.
  - Changing idempotency key derivation.
- id: EH-003
  title: Consumer processing tolerates duplicate and replayed events
  severity: critical
  category: messaging
  evidence_patterns:
  - event id
  - deduplication
  - processed event store
  finding_when: duplicate delivery causes duplicate mutation
  emit_on_failure: true
  business_logic_risk: severe
  requires_approval_before_implementation: true
  approval_owner: product
  safe_remediation_without_approval:
  - Add duplicate-detection telemetry.
  - Add tests that demonstrate the current behavior and the failure mode.
  requires_approval_for:
  - Introducing or changing deduplication that alters which events are processed.
- id: EH-004
  title: Checkpoint storage is deployment-configured and recovery behavior is defined
  severity: critical
  category: messaging
  evidence_patterns:
  - checkpoint store
  - BlobCheckpointStore
  - consumer group
  finding_when: checkpoint dependency is hardcoded or loss causes undefined replay behavior
  emit_on_failure: true
  business_logic_risk: severe
  requires_approval_before_implementation: true
  approval_owner: architecture
  safe_remediation_without_approval:
  - Add checkpoint-store telemetry.
  - Add tests that demonstrate the current behavior and the failure mode.
  requires_approval_for:
  - Changing the checkpoint store or consumer group.
  - Changing replay behavior after checkpoint loss.
- id: EH-005
  title: Partition-key and ordering assumptions remain valid across regions
  severity: high
  category: consistency
  evidence_patterns:
  - partitionKey
  - partitionId
  - sequence number
  finding_when: code assumes global ordering or pins partitions without documented need
  emit_on_failure: true
  business_logic_risk: severe
  requires_approval_before_implementation: true
  approval_owner: architecture_and_product
  safe_remediation_without_approval:
  - Add partition and ordering telemetry.
  - Add tests that demonstrate the current behavior and the failure mode.
  requires_approval_for:
  - Changing partition key derivation or partition assignment.
- id: EH-006
  title: Backpressure, poison events, and retry exhaustion are handled
  severity: high
  category: resilience
  evidence_patterns:
  - dead letter
  - quarantine
  - retry topic
  - max attempts
  finding_when: poison events create infinite retry or block a partition
  emit_on_failure: true
  business_logic_risk: severe
  requires_approval_before_implementation: true
  approval_owner: product
  safe_remediation_without_approval:
  - Add poison-event and retry-exhaustion telemetry.
  - Add tests that demonstrate the current behavior and the failure mode.
  requires_approval_for:
  - Introducing dead-letter routing.
  - Changing how many times an event is retried before being set aside.
- id: EH-007
  title: Critical producer or consumer failure changes the correct readiness signal
  severity: high
  category: health
  evidence_patterns:
  - HealthIndicator
  - lag metric
  - processor state
  finding_when: service reports ready when its critical messaging role cannot operate
  emit_on_failure: true
  business_logic_risk: severe
  requires_approval_before_implementation: true
  approval_owner: architecture_and_product
  safe_remediation_without_approval:
  - Add processor-state and lag telemetry.
  - Add tests that demonstrate the current behavior and the failure mode.
  requires_approval_for:
  - Adding messaging state to readiness.
- id: EH-008
  title: Tests cover duplicate delivery, replay, checkpoint loss, throttling, and recovery
  severity: high
  category: testing
  evidence_patterns:
  - mock producer
  - test consumer
  - fault injection
  finding_when: messaging failure modes are untested
  emit_on_failure: true
  business_logic_risk: none
  requires_approval_before_implementation: false
  approval_owner: none
  safe_remediation_without_approval:
  - Add tests that demonstrate the current behavior and the failure mode.
  requires_approval_for: []
- id: EH-009
  title: Clients are reused with explicit AMQP lifecycle management
  severity: high
  category: resource-management
  evidence_patterns:
  - EventHubClientBuilder
  - singleton
  - close
  - connection reuse
  - prefetch
  finding_when: clients or processors are created per message or per request, or connection lifecycle
    and prefetch behavior are undefined
  emit_on_failure: true
  business_logic_risk: low
  requires_approval_before_implementation: false
  approval_owner: architecture
  safe_remediation_without_approval:
  - Convert per-message client creation to a managed singleton preserving identical configuration.
  - Add or improve metrics, logs, traces, and health details without changing decisions or payload content.
  - Add tests that characterize and lock in current behavior.
  requires_approval_for:
  - Changing prefetch or connection configuration where throughput or ordering behavior changes.
- id: EH-010
  title: Authentication uses approved identity with supported rotation
  severity: critical
  category: security
  evidence_patterns:
  - DefaultAzureCredential
  - managed identity
  - SAS
  - connection string
  finding_when: connection strings or SAS values are embedded or logged, or credential rotation requires
    restart without an approved contract
  emit_on_failure: true
  business_logic_risk: severe
  requires_approval_before_implementation: true
  approval_owner: security
  safe_remediation_without_approval:
  - Add authentication-failure telemetry with values redacted.
  - Add tests that demonstrate the current behavior and the failure mode.
  requires_approval_for:
  - Changing credential type or authentication flow.
- id: EH-011
  title: Batch sends respect size limits and handle partial failure
  severity: high
  category: messaging
  evidence_patterns:
  - EventDataBatch
  - tryAdd
  - max message size
  - batch send
  finding_when: batch sends ignore capacity limits, drop events silently, or treat partial failure as
    success
  emit_on_failure: true
  business_logic_risk: severe
  requires_approval_before_implementation: true
  approval_owner: product
  safe_remediation_without_approval:
  - Add batch-size and per-event outcome telemetry.
  - Add tests that demonstrate the current behavior and the failure mode.
  requires_approval_for:
  - Changing batching behavior where event grouping, ordering, or delivery timing changes.
- id: EH-012
  title: Checkpoint strategy balances replay and duplication explicitly
  severity: critical
  category: messaging
  evidence_patterns:
  - updateCheckpoint
  - checkpoint interval
  - after processing
  finding_when: checkpoints advance before durable processing completes or checkpoint frequency is undefined
  emit_on_failure: true
  business_logic_risk: severe
  requires_approval_before_implementation: true
  approval_owner: architecture_and_product
  safe_remediation_without_approval:
  - Add checkpoint-position and replay telemetry.
  - Add tests that demonstrate the current behavior and the failure mode.
  requires_approval_for:
  - Changing checkpoint timing or frequency, which shifts the duplicate-versus-loss tradeoff.
- id: EH-013
  title: Consumer activation and partition ownership are region-role controlled
  severity: critical
  category: workload-ownership
  evidence_patterns:
  - consumer group
  - ownership
  - processor start
  - region role
  finding_when: both regional deployments can process the same partitions without an approved multi-active
    or single-active ownership model
  emit_on_failure: true
  business_logic_risk: severe
  requires_approval_before_implementation: true
  approval_owner: architecture_and_product
  safe_remediation_without_approval:
  - Add ownership and activation telemetry.
  - Add tests that demonstrate the current behavior and the failure mode.
  requires_approval_for:
  - Enabling or disabling consumers in any region.
  - Changing partition ownership behavior.
- id: EH-014
  title: Processor error handling is implemented and actionable
  severity: high
  category: resilience
  evidence_patterns:
  - processError
  - error handler
  - partition close
  - reason
  finding_when: processor errors are ignored, swallowed, or provide no actionable signal
  emit_on_failure: true
  business_logic_risk: moderate
  requires_approval_before_implementation: false
  approval_owner: architecture
  safe_remediation_without_approval:
  - Implement an error handler that only records and emits telemetry.
  - Add tests that demonstrate the current behavior and the failure mode.
  requires_approval_for:
  - Adding error handling that changes event disposition or partition behavior.
- id: EH-015
  title: Event handlers avoid unbounded blocking and thread starvation
  severity: high
  category: performance
  evidence_patterns:
  - blocking call
  - thread pool
  - executor
  - processEvent
  finding_when: event handlers perform unbounded blocking work that starves processing threads or delays
    checkpointing
  emit_on_failure: true
  business_logic_risk: severe
  requires_approval_before_implementation: true
  approval_owner: architecture_and_product
  safe_remediation_without_approval:
  - Add handler-duration and thread-saturation telemetry.
  - Add tests that demonstrate the current behavior and the failure mode.
  requires_approval_for:
  - Moving processing to another thread or executor, which changes completion and checkpoint ordering.
- id: EH-016
  title: Serialization and schema compatibility are governed
  severity: high
  category: contract
  evidence_patterns:
  - schema registry
  - Avro
  - JSON schema
  - deserialization
  finding_when: event serialization or schema evolution can break consumers or cause undetected data loss
  emit_on_failure: true
  business_logic_risk: severe
  requires_approval_before_implementation: true
  approval_owner: partner_contract
  safe_remediation_without_approval: &id001
  - Add or improve metrics, logs, traces, and health details without changing decisions or payload content.
  - Add tests that characterize and lock in current behavior.
  requires_approval_for:
  - Changing event schema, serialization format, or compatibility mode.
- id: EH-017
  title: Consumer lag, throughput, and stalled processing are observable
  severity: high
  category: observability
  evidence_patterns:
  - lag
  - last processed
  - throughput metric
  - partition metric
  finding_when: processing can stop or fall behind without an actionable signal
  emit_on_failure: true
  business_logic_risk: none
  requires_approval_before_implementation: false
  approval_owner: none
  safe_remediation_without_approval: *id001
  requires_approval_for: []
- id: EH-018
  title: Shutdown stops processors and flushes required state
  severity: high
  category: lifecycle
  evidence_patterns:
  - processor stop
  - close
  - graceful shutdown
  - flush
  finding_when: shutdown abandons in-flight events, skips required checkpointing, or leaves producers
    unflushed
  emit_on_failure: true
  business_logic_risk: severe
  requires_approval_before_implementation: true
  approval_owner: product_and_architecture
  safe_remediation_without_approval:
  - Add shutdown-phase telemetry.
  - Add tests that demonstrate the current behavior and the failure mode.
  requires_approval_for:
  - Changing shutdown behavior that affects whether in-flight events are processed, checkpointed, or replayed.
- id: EH-019
  title: Event payloads and diagnostics exclude sensitive data
  severity: critical
  category: security
  evidence_patterns:
  - log event body
  - PII
  - payload
  - mask
  finding_when: event payloads, keys, or personal data can be written to logs or diagnostics
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
- id: EH-020
  title: Ambiguous producer outcomes are reconciled
  severity: critical
  category: data-correctness
  evidence_patterns:
  - send timeout
  - unknown outcome
  - reconcile
  - duplicate detection
  finding_when: an unknown send outcome is treated as success or failure without reconciliation or duplicate-safe
    replay
  emit_on_failure: true
  business_logic_risk: severe
  requires_approval_before_implementation: true
  approval_owner: product
  safe_remediation_without_approval:
  - Add telemetry distinguishing confirmed, failed, and unknown send outcomes.
  - Add tests that demonstrate the current behavior and the failure mode.
  requires_approval_for:
  - Reclassifying an unknown send outcome.
  - Adding reconciliation or replay that can publish an event again.
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

# Azure Event Hubs Target-State Application Behavior Standard

### Shared-service operating-model contract

This standard does not select the application's shared-service topology. Resolve the operating model from:

```text
architecture_context.shared_service_operating_models.services.eventhubs
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

This dependency-specific standard assesses how a Spring Boot microservice uses Azure Event Hubs when evaluated for the approved target operating model supplied by application architecture context. The local regional service endpoint is assumed to exist and be reachable through the approved private networking design.

## Scope boundary

This standard assesses **application code, application configuration checked into the repository, and automated tests only**. It does not assess whether Azure or third-party infrastructure has been deployed correctly.

## Mandatory assumptions

- Two independent Azure regions are provisioned and active.
- AKS, networking, private endpoints, DNS, identities, certificates, and dependent services follow the approved active-active infrastructure design.
- The deployment pipeline injects region-specific configuration into the same application artifact.
- The application repository does not provision or validate infrastructure.

## Evaluator workflow

- Confirm the dependency is actually used by production code.
- Resolve source and target models from `architecture_context.shared_service_operating_models.services.eventhubs` before evaluating model-specific controls.
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

### EH-001: Namespace and event hub names are deployment-injected

**Severity:** Critical  
**Category:** configuration

#### Requirement

The application code and configuration must satisfy this behavior when the same artifact runs in either active region.

#### Repository evidence to inspect

- `spring.cloud.azure.eventhubs`
- `fullyQualifiedNamespace`
- `EVENTHUB_NAMESPACE`

#### Finding condition

Emit a finding when evidence shows that namespace is hardcoded.

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

- Changing the effective namespace or hub.

---

### EH-002: Producer retries are bounded and preserve business idempotency

**Severity:** Critical  
**Category:** resilience

#### Requirement

The application code and configuration must satisfy this behavior when the same artifact runs in either active region.

#### Repository evidence to inspect

- `EventHubProducerClient`
- `AmqpRetryOptions`
- `idempotency key`

#### Finding condition

Emit a finding when evidence shows that producer retry can duplicate business effects without detection.

#### Evidence rule

Cite the file path, symbol or property, and advisory line range when available. Evaluate effective behavior rather than the presence of a library, annotation, or property alone. If the repository does not contain enough evidence, return `not_assessed` rather than assuming noncompliance.

#### Business-logic risk

**Risk level:** `severe`  
**Requires approval before implementation:** `true`  
**Approval owner:** `product`

**Safe remediation without approval:**

- Add producer retry and outcome telemetry.
- Add tests that demonstrate the current behavior and the failure mode.

**Requires approval for:**

- Changing producer retry counts where duplicate publication risk changes.
- Changing idempotency key derivation.

---

### EH-003: Consumer processing tolerates duplicate and replayed events

**Severity:** Critical  
**Category:** messaging

#### Requirement

The application code and configuration must satisfy this behavior when the same artifact runs in either active region.

#### Repository evidence to inspect

- `event id`
- `deduplication`
- `processed event store`

#### Finding condition

Emit a finding when evidence shows that duplicate delivery causes duplicate mutation.

#### Evidence rule

Cite the file path, symbol or property, and advisory line range when available. Evaluate effective behavior rather than the presence of a library, annotation, or property alone. If the repository does not contain enough evidence, return `not_assessed` rather than assuming noncompliance.

#### Business-logic risk

**Risk level:** `severe`  
**Requires approval before implementation:** `true`  
**Approval owner:** `product`

**Safe remediation without approval:**

- Add duplicate-detection telemetry.
- Add tests that demonstrate the current behavior and the failure mode.

**Requires approval for:**

- Introducing or changing deduplication that alters which events are processed.

---

### EH-004: Checkpoint storage is deployment-configured and recovery behavior is defined

**Severity:** Critical  
**Category:** messaging

#### Requirement

The application code and configuration must satisfy this behavior when the same artifact runs in either active region.

#### Repository evidence to inspect

- `checkpoint store`
- `BlobCheckpointStore`
- `consumer group`

#### Finding condition

Emit a finding when evidence shows that checkpoint dependency is hardcoded or loss causes undefined replay behavior.

#### Evidence rule

Cite the file path, symbol or property, and advisory line range when available. Evaluate effective behavior rather than the presence of a library, annotation, or property alone. If the repository does not contain enough evidence, return `not_assessed` rather than assuming noncompliance.

#### Business-logic risk

**Risk level:** `severe`  
**Requires approval before implementation:** `true`  
**Approval owner:** `architecture`

**Safe remediation without approval:**

- Add checkpoint-store telemetry.
- Add tests that demonstrate the current behavior and the failure mode.

**Requires approval for:**

- Changing the checkpoint store or consumer group.
- Changing replay behavior after checkpoint loss.

---

### EH-005: Partition-key and ordering assumptions remain valid across regions

**Severity:** High  
**Category:** consistency

#### Requirement

The application code and configuration must satisfy this behavior when the same artifact runs in either active region.

#### Repository evidence to inspect

- `partitionKey`
- `partitionId`
- `sequence number`

#### Finding condition

Emit a finding when evidence shows that code assumes global ordering or pins partitions without documented need.

#### Evidence rule

Cite the file path, symbol or property, and advisory line range when available. Evaluate effective behavior rather than the presence of a library, annotation, or property alone. If the repository does not contain enough evidence, return `not_assessed` rather than assuming noncompliance.

#### Business-logic risk

**Risk level:** `severe`  
**Requires approval before implementation:** `true`  
**Approval owner:** `architecture_and_product`

**Safe remediation without approval:**

- Add partition and ordering telemetry.
- Add tests that demonstrate the current behavior and the failure mode.

**Requires approval for:**

- Changing partition key derivation or partition assignment.

---

### EH-006: Backpressure, poison events, and retry exhaustion are handled

**Severity:** High  
**Category:** resilience

#### Requirement

The application code and configuration must satisfy this behavior when the same artifact runs in either active region.

#### Repository evidence to inspect

- `dead letter`
- `quarantine`
- `retry topic`
- `max attempts`

#### Finding condition

Emit a finding when evidence shows that poison events create infinite retry or block a partition.

#### Evidence rule

Cite the file path, symbol or property, and advisory line range when available. Evaluate effective behavior rather than the presence of a library, annotation, or property alone. If the repository does not contain enough evidence, return `not_assessed` rather than assuming noncompliance.

#### Business-logic risk

**Risk level:** `severe`  
**Requires approval before implementation:** `true`  
**Approval owner:** `product`

**Safe remediation without approval:**

- Add poison-event and retry-exhaustion telemetry.
- Add tests that demonstrate the current behavior and the failure mode.

**Requires approval for:**

- Introducing dead-letter routing.
- Changing how many times an event is retried before being set aside.

---

### EH-007: Critical producer or consumer failure changes the correct readiness signal

**Severity:** High  
**Category:** health

#### Requirement

The application code and configuration must satisfy this behavior when the same artifact runs in either active region.

#### Repository evidence to inspect

- `HealthIndicator`
- `lag metric`
- `processor state`

#### Finding condition

Emit a finding when evidence shows that service reports ready when its critical messaging role cannot operate.

#### Evidence rule

Cite the file path, symbol or property, and advisory line range when available. Evaluate effective behavior rather than the presence of a library, annotation, or property alone. If the repository does not contain enough evidence, return `not_assessed` rather than assuming noncompliance.

#### Business-logic risk

**Risk level:** `severe`  
**Requires approval before implementation:** `true`  
**Approval owner:** `architecture_and_product`

**Safe remediation without approval:**

- Add processor-state and lag telemetry.
- Add tests that demonstrate the current behavior and the failure mode.

**Requires approval for:**

- Adding messaging state to readiness.

---

### EH-008: Tests cover duplicate delivery, replay, checkpoint loss, throttling, and recovery

**Severity:** High  
**Category:** testing

#### Requirement

The application code and configuration must satisfy this behavior when the same artifact runs in either active region.

#### Repository evidence to inspect

- `mock producer`
- `test consumer`
- `fault injection`

#### Finding condition

Emit a finding when evidence shows that messaging failure modes are untested.

#### Evidence rule

Cite the file path, symbol or property, and advisory line range when available. Evaluate effective behavior rather than the presence of a library, annotation, or property alone. If the repository does not contain enough evidence, return `not_assessed` rather than assuming noncompliance.

#### Business-logic risk

**Risk level:** `none`  
**Requires approval before implementation:** `false`  
**Approval owner:** `none`

**Safe remediation without approval:**

- Add tests that demonstrate the current behavior and the failure mode.

---

### EH-009: Clients are reused with explicit AMQP lifecycle management

**Severity:** High  
**Category:** resource-management

#### Requirement

The application code and configuration must satisfy this behavior when the same artifact runs in either active region.

#### Repository evidence to inspect

- `EventHubClientBuilder`
- `singleton`
- `close`
- `connection reuse`
- `prefetch`

#### Finding condition

Emit a finding when evidence shows that clients or processors are created per message or per request, or connection lifecycle and prefetch behavior are undefined.

#### Evidence rule

Cite the file path, symbol or property, and advisory line range when available. Evaluate effective behavior rather than the presence of a library, annotation, or property alone. If the repository does not contain enough evidence, return `not_assessed` rather than assuming noncompliance.

#### Quality caveats

- AMQP connection churn increases latency and failure rates during recovery.

#### Business-logic risk

**Risk level:** `low`  
**Requires approval before implementation:** `false`  
**Approval owner:** `architecture`

**Safe remediation without approval:**

- Convert per-message client creation to a managed singleton preserving identical configuration.
- Add or improve metrics, logs, traces, and health details without changing decisions or payload content.
- Add tests that characterize and lock in current behavior.

**Requires approval for:**

- Changing prefetch or connection configuration where throughput or ordering behavior changes.

---

### EH-010: Authentication uses approved identity with supported rotation

**Severity:** Critical  
**Category:** security

#### Requirement

The application code and configuration must satisfy this behavior when the same artifact runs in either active region.

#### Repository evidence to inspect

- `DefaultAzureCredential`
- `managed identity`
- `SAS`
- `connection string`

#### Finding condition

Emit a finding when evidence shows that connection strings or SAS values are embedded or logged, or credential rotation requires restart without an approved contract.

#### Evidence rule

Cite the file path, symbol or property, and advisory line range when available. Evaluate effective behavior rather than the presence of a library, annotation, or property alone. If the repository does not contain enough evidence, return `not_assessed` rather than assuming noncompliance.

#### Quality caveats

- Do not log connection strings or tokens in diagnostics.

#### Business-logic risk

**Risk level:** `severe`  
**Requires approval before implementation:** `true`  
**Approval owner:** `security`

**Safe remediation without approval:**

- Add authentication-failure telemetry with values redacted.
- Add tests that demonstrate the current behavior and the failure mode.

**Requires approval for:**

- Changing credential type or authentication flow.

---

### EH-011: Batch sends respect size limits and handle partial failure

**Severity:** High  
**Category:** messaging

#### Requirement

The application code and configuration must satisfy this behavior when the same artifact runs in either active region.

#### Repository evidence to inspect

- `EventDataBatch`
- `tryAdd`
- `max message size`
- `batch send`

#### Finding condition

Emit a finding when evidence shows that batch sends ignore capacity limits, drop events silently, or treat partial failure as success.

#### Evidence rule

Cite the file path, symbol or property, and advisory line range when available. Evaluate effective behavior rather than the presence of a library, annotation, or property alone. If the repository does not contain enough evidence, return `not_assessed` rather than assuming noncompliance.

#### Quality caveats

- A full batch must be flushed or handled explicitly rather than discarded.

#### Business-logic risk

**Risk level:** `severe`  
**Requires approval before implementation:** `true`  
**Approval owner:** `product`

**Safe remediation without approval:**

- Add batch-size and per-event outcome telemetry.
- Add tests that demonstrate the current behavior and the failure mode.

**Requires approval for:**

- Changing batching behavior where event grouping, ordering, or delivery timing changes.

---

### EH-012: Checkpoint strategy balances replay and duplication explicitly

**Severity:** Critical  
**Category:** messaging

#### Requirement

The application code and configuration must satisfy this behavior when the same artifact runs in either active region.

#### Repository evidence to inspect

- `updateCheckpoint`
- `checkpoint interval`
- `after processing`

#### Finding condition

Emit a finding when evidence shows that checkpoints advance before durable processing completes or checkpoint frequency is undefined.

#### Evidence rule

Cite the file path, symbol or property, and advisory line range when available. Evaluate effective behavior rather than the presence of a library, annotation, or property alone. If the repository does not contain enough evidence, return `not_assessed` rather than assuming noncompliance.

#### Quality caveats

- Frequent checkpointing reduces replay but increases storage operations; the tradeoff must be intentional.

#### Business-logic risk

**Risk level:** `severe`  
**Requires approval before implementation:** `true`  
**Approval owner:** `architecture_and_product`

**Safe remediation without approval:**

- Add checkpoint-position and replay telemetry.
- Add tests that demonstrate the current behavior and the failure mode.

**Requires approval for:**

- Changing checkpoint timing or frequency, which shifts the duplicate-versus-loss tradeoff.

---

### EH-013: Consumer activation and partition ownership are region-role controlled

**Severity:** Critical  
**Category:** workload-ownership

#### Requirement

The application code and configuration must satisfy this behavior when the same artifact runs in either active region.

#### Repository evidence to inspect

- `consumer group`
- `ownership`
- `processor start`
- `region role`

#### Finding condition

Emit a finding when evidence shows that both regional deployments can process the same partitions without an approved multi-active or single-active ownership model.

#### Evidence rule

Cite the file path, symbol or property, and advisory line range when available. Evaluate effective behavior rather than the presence of a library, annotation, or property alone. If the repository does not contain enough evidence, return `not_assessed` rather than assuming noncompliance.

#### Quality caveats

- Ownership must be explicit; running in both regions is not automatically safe.

#### Business-logic risk

**Risk level:** `severe`  
**Requires approval before implementation:** `true`  
**Approval owner:** `architecture_and_product`

**Safe remediation without approval:**

- Add ownership and activation telemetry.
- Add tests that demonstrate the current behavior and the failure mode.

**Requires approval for:**

- Enabling or disabling consumers in any region.
- Changing partition ownership behavior.

---

### EH-014: Processor error handling is implemented and actionable

**Severity:** High  
**Category:** resilience

#### Requirement

The application code and configuration must satisfy this behavior when the same artifact runs in either active region.

#### Repository evidence to inspect

- `processError`
- `error handler`
- `partition close`
- `reason`

#### Finding condition

Emit a finding when evidence shows that processor errors are ignored, swallowed, or provide no actionable signal.

#### Evidence rule

Cite the file path, symbol or property, and advisory line range when available. Evaluate effective behavior rather than the presence of a library, annotation, or property alone. If the repository does not contain enough evidence, return `not_assessed` rather than assuming noncompliance.

#### Quality caveats

- Silent processor failure can stop business processing while the pod remains healthy.

#### Business-logic risk

**Risk level:** `moderate`  
**Requires approval before implementation:** `false`  
**Approval owner:** `architecture`

**Safe remediation without approval:**

- Implement an error handler that only records and emits telemetry.
- Add tests that demonstrate the current behavior and the failure mode.

**Requires approval for:**

- Adding error handling that changes event disposition or partition behavior.

---

### EH-015: Event handlers avoid unbounded blocking and thread starvation

**Severity:** High  
**Category:** performance

#### Requirement

The application code and configuration must satisfy this behavior when the same artifact runs in either active region.

#### Repository evidence to inspect

- `blocking call`
- `thread pool`
- `executor`
- `processEvent`

#### Finding condition

Emit a finding when evidence shows that event handlers perform unbounded blocking work that starves processing threads or delays checkpointing.

#### Evidence rule

Cite the file path, symbol or property, and advisory line range when available. Evaluate effective behavior rather than the presence of a library, annotation, or property alone. If the repository does not contain enough evidence, return `not_assessed` rather than assuming noncompliance.

#### Quality caveats

- Offloading work must preserve completion semantics before checkpointing.

#### Business-logic risk

**Risk level:** `severe`  
**Requires approval before implementation:** `true`  
**Approval owner:** `architecture_and_product`

**Safe remediation without approval:**

- Add handler-duration and thread-saturation telemetry.
- Add tests that demonstrate the current behavior and the failure mode.

**Requires approval for:**

- Moving processing to another thread or executor, which changes completion and checkpoint ordering.

---

### EH-016: Serialization and schema compatibility are governed

**Severity:** High  
**Category:** contract

#### Requirement

The application code and configuration must satisfy this behavior when the same artifact runs in either active region.

#### Repository evidence to inspect

- `schema registry`
- `Avro`
- `JSON schema`
- `deserialization`

#### Finding condition

Emit a finding when evidence shows that event serialization or schema evolution can break consumers or cause undetected data loss.

#### Evidence rule

Cite the file path, symbol or property, and advisory line range when available. Evaluate effective behavior rather than the presence of a library, annotation, or property alone. If the repository does not contain enough evidence, return `not_assessed` rather than assuming noncompliance.

#### Quality caveats

- Schema changes are contract decisions requiring producer and consumer coordination.

#### Business-logic risk

**Risk level:** `severe`  
**Requires approval before implementation:** `true`  
**Approval owner:** `partner_contract`

**Safe remediation without approval:**

- Add or improve metrics, logs, traces, and health details without changing decisions or payload content.
- Add tests that characterize and lock in current behavior.

**Requires approval for:**

- Changing event schema, serialization format, or compatibility mode.

---

### EH-017: Consumer lag, throughput, and stalled processing are observable

**Severity:** High  
**Category:** observability

#### Requirement

The application code and configuration must satisfy this behavior when the same artifact runs in either active region.

#### Repository evidence to inspect

- `lag`
- `last processed`
- `throughput metric`
- `partition metric`

#### Finding condition

Emit a finding when evidence shows that processing can stop or fall behind without an actionable signal.

#### Evidence rule

Cite the file path, symbol or property, and advisory line range when available. Evaluate effective behavior rather than the presence of a library, annotation, or property alone. If the repository does not contain enough evidence, return `not_assessed` rather than assuming noncompliance.

#### Quality caveats

- Process health alone does not prove business event processing is progressing.

#### Business-logic risk

**Risk level:** `none`  
**Requires approval before implementation:** `false`  
**Approval owner:** `none`

**Safe remediation without approval:**

- Add or improve metrics, logs, traces, and health details without changing decisions or payload content.
- Add tests that characterize and lock in current behavior.

---

### EH-018: Shutdown stops processors and flushes required state

**Severity:** High  
**Category:** lifecycle

#### Requirement

The application code and configuration must satisfy this behavior when the same artifact runs in either active region.

#### Repository evidence to inspect

- `processor stop`
- `close`
- `graceful shutdown`
- `flush`

#### Finding condition

Emit a finding when evidence shows that shutdown abandons in-flight events, skips required checkpointing, or leaves producers unflushed.

#### Evidence rule

Cite the file path, symbol or property, and advisory line range when available. Evaluate effective behavior rather than the presence of a library, annotation, or property alone. If the repository does not contain enough evidence, return `not_assessed` rather than assuming noncompliance.

#### Quality caveats

- Shutdown must not acknowledge work that was not durably completed.

#### Business-logic risk

**Risk level:** `severe`  
**Requires approval before implementation:** `true`  
**Approval owner:** `product_and_architecture`

**Safe remediation without approval:**

- Add shutdown-phase telemetry.
- Add tests that demonstrate the current behavior and the failure mode.

**Requires approval for:**

- Changing shutdown behavior that affects whether in-flight events are processed, checkpointed, or replayed.

---

### EH-019: Event payloads and diagnostics exclude sensitive data

**Severity:** Critical  
**Category:** security

#### Requirement

The application code and configuration must satisfy this behavior when the same artifact runs in either active region.

#### Repository evidence to inspect

- `log event body`
- `PII`
- `payload`
- `mask`

#### Finding condition

Emit a finding when evidence shows that event payloads, keys, or personal data can be written to logs or diagnostics.

#### Evidence rule

Cite the file path, symbol or property, and advisory line range when available. Evaluate effective behavior rather than the presence of a library, annotation, or property alone. If the repository does not contain enough evidence, return `not_assessed` rather than assuming noncompliance.

#### Quality caveats

- Use identifiers and metadata for troubleshooting rather than full payloads.

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

### EH-020: Ambiguous producer outcomes are reconciled

**Severity:** Critical  
**Category:** data-correctness

#### Requirement

The application code and configuration must satisfy this behavior when the same artifact runs in either active region.

#### Repository evidence to inspect

- `send timeout`
- `unknown outcome`
- `reconcile`
- `duplicate detection`

#### Finding condition

Emit a finding when evidence shows that an unknown send outcome is treated as success or failure without reconciliation or duplicate-safe replay.

#### Evidence rule

Cite the file path, symbol or property, and advisory line range when available. Evaluate effective behavior rather than the presence of a library, annotation, or property alone. If the repository does not contain enough evidence, return `not_assessed` rather than assuming noncompliance.

#### Quality caveats

- A send timeout does not prove the event was not published.

#### Business-logic risk

**Risk level:** `severe`  
**Requires approval before implementation:** `true`  
**Approval owner:** `product`

**Safe remediation without approval:**

- Add telemetry distinguishing confirmed, failed, and unknown send outcomes.
- Add tests that demonstrate the current behavior and the failure mode.

**Requires approval for:**

- Reclassifying an unknown send outcome.
- Adding reconciliation or replay that can publish an event again.

---

## Standard finding format

- **Title:** [specific code-level gap]
- **Control:** [EH-NNN]
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
