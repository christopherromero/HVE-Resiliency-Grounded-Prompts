---
schema_version: 2.2.0
document_type: dependency_behavior
service: azure-function
service_name: Azure Functions
language: dotnet-java-node-python-powershell
runtime_platform: azure-functions
assessment_scope: function_code_and_repository_owned_configuration
lifecycle_status: active
assessment:
  enabled: true
  emit_findings: true
  include_in_score: true
  unknown_evidence_status: not_assessed
controls:
- id: FUNC-001
  title: Function triggers and handlers are idempotent
  severity: critical
  category: consistency
  applies_when: a trigger or HTTP function can receive duplicate input
  evidence_patterns:
  - idempotency key
  - dedupe store
  - event id
  - unique constraint
  - ETag
  finding_when: replay, redelivery, retry, or scale-out can repeat a business effect
  emit_on_failure: true
- id: FUNC-002
  title: Retry policy matches trigger and operation semantics
  severity: critical
  category: resilience
  applies_when: a trigger or dependency can retry
  evidence_patterns:
  - host.json retry
  - FixedDelayRetry
  - ExponentialBackoffRetry
  - retry context
  finding_when: retry is absent where required, unbounded, or repeats a terminal or
    ambiguous non-idempotent operation
  emit_on_failure: true
- id: FUNC-003
  title: Event Hubs and stream processing handle checkpoint advancement and poison
    events
  severity: critical
  category: event-processing
  applies_when: Event Hubs or Kafka-style stream trigger is used
  evidence_patterns:
  - EventHubTrigger
  - consumer group
  - checkpoint
  - batch
  - poison event
  finding_when: exceptions, batch handling, or checkpoint semantics can lose events,
    block a partition, or repeatedly poison healthy records
  emit_on_failure: true
- id: FUNC-004
  title: Queue and Service Bus completion follows successful durable processing
  severity: critical
  category: event-processing
  applies_when: queue or Service Bus trigger is used
  evidence_patterns:
  - QueueTrigger
  - ServiceBusTrigger
  - completeMessage
  - autoCompleteMessages
  finding_when: a message is completed before required durable or external work succeeds,
    or abandonment/dead-letter behavior is undefined
  emit_on_failure: true
- id: FUNC-005
  title: Poison and terminal failures have a durable disposition
  severity: high
  category: event-processing
  applies_when: event, queue, or scheduled processing exists
  evidence_patterns:
  - dead-letter
  - poison queue
  - failed event store
  - attempt count
  finding_when: terminally failing input retries indefinitely, disappears, or blocks
    healthy processing
  emit_on_failure: true
- id: FUNC-006
  title: Timer-trigger and scheduled work ownership is safe across regions
  severity: critical
  category: workload-ownership
  applies_when: TimerTrigger or custom schedule exists
  evidence_patterns:
  - TimerTrigger
  - useMonitor
  - schedule status
  - feature flag
  - lease
  finding_when: both regions or function apps can execute the same schedule without
    an approved single-active or idempotent multi-active design
  emit_on_failure: true
- id: FUNC-007
  title: Batch and timer runs have durable run identity and terminal status
  severity: high
  category: batch
  applies_when: scheduled or batch functions exist
  evidence_patterns:
  - runId
  - business date
  - attempt
  - last success
  - completion status
  finding_when: reruns cannot distinguish complete, partial, failed, or duplicate
    execution
  emit_on_failure: true
- id: FUNC-008
  title: Dependency calls have complete bounded time budgets
  severity: critical
  category: dependency-resilience
  applies_when: function calls remote services
  evidence_patterns:
  - HttpClient timeout
  - SQL timeout
  - Storage retry
  - Cosmos retry
  - CancellationToken
  finding_when: connection, pool acquisition, read, operation, or total execution
    can exceed the function or caller budget
  emit_on_failure: true
- id: FUNC-009
  title: Non-idempotent and ambiguous external outcomes are reconciled
  severity: critical
  category: financial-integrity
  applies_when: function invokes payment or mutating external operation
  evidence_patterns:
  - provider transaction id
  - status lookup
  - reconciliation
  - idempotency header
  finding_when: timeout or connection loss can lead to blind replay when the provider
    might have succeeded
  emit_on_failure: true
- id: FUNC-010
  title: Cross-store and output-binding workflows handle partial success
  severity: critical
  category: consistency
  applies_when: one invocation writes multiple systems
  evidence_patterns:
  - output binding
  - SQL
  - Cosmos
  - Storage
  - Service Bus
  - Event Hubs
  finding_when: one destination can succeed while another fails without durable reconciliation
  emit_on_failure: true
- id: FUNC-011
  title: Durable Functions orchestrators remain deterministic
  severity: critical
  category: durable-functions
  applies_when: Durable Functions orchestration is used
  evidence_patterns:
  - orchestration trigger
  - DurableOrchestrationContext
  - TaskOrchestrationContext
  - currentUtcDateTime
  finding_when: orchestrator code performs nondeterministic I/O, random generation,
    wall-clock access, or unsupported side effects
  emit_on_failure: true
- id: FUNC-012
  title: Durable activity retries and compensation are explicit
  severity: high
  category: durable-functions
  applies_when: Durable Functions activities perform side effects
  evidence_patterns:
  - CallActivityWithRetry
  - retry options
  - compensation
  - saga
  finding_when: activity side effects can repeat or partial workflow completion has
    no compensation or reconciliation
  emit_on_failure: true
- id: FUNC-013
  title: Configuration, endpoints, and secrets are externalized and validated
  severity: critical
  category: configuration
  applies_when: function uses external services
  evidence_patterns:
  - local.settings.json
  - app settings
  - Key Vault reference
  - environment variable
  - options validation
  finding_when: regional endpoint, credential, or required setting is committed, hardcoded,
    missing validation, or defaults unsafely
  emit_on_failure: true
- id: FUNC-014
  title: Managed identity and credential reuse avoid token stampedes
  severity: high
  category: identity
  applies_when: Azure SDK or OAuth credentials are used
  evidence_patterns:
  - DefaultAzureCredential
  - ManagedIdentityCredential
  - TokenCredential
  - client singleton
  finding_when: credentials or SDK clients are recreated per invocation, static secrets
    are embedded, or concurrent refresh can stampede
  emit_on_failure: true
- id: FUNC-015
  title: HTTP-trigger functions use safe methods, authorization, and error semantics
  severity: high
  category: http-api
  applies_when: HTTP trigger exists
  evidence_patterns:
  - HttpTrigger
  - AuthorizationLevel
  - GET
  - POST
  - '429'
  - '503'
  finding_when: GET mutates state, authorization is overly permissive, or dependency
    failure is returned as success/not-found
  emit_on_failure: true
- id: FUNC-016
  title: Fallback and synthetic success are durably recoverable
  severity: critical
  category: fallback
  applies_when: function returns deferred, accepted, or synthetic success
  evidence_patterns:
  - '202'
  - fallback store
  - synthetic approval
  - on failure
  finding_when: success is returned before complete recoverable intent is durably
    recorded or fallback failure is silent
  emit_on_failure: true
- id: FUNC-017
  title: Business throughput, backlog, retries, and stuck work are observable
  severity: high
  category: observability
  applies_when: nontrivial trigger processing exists
  evidence_patterns:
  - Application Insights
  - custom metric
  - backlog age
  - last success
  - dead-letter count
  finding_when: runtime health appears normal while processing stops, backlog grows,
    ownership is ambiguous, or terminal failures are invisible
  emit_on_failure: true
- id: FUNC-018
  title: Correlation identity propagates across triggers and dependencies
  severity: high
  category: observability
  applies_when: workflow spans multiple services
  evidence_patterns:
  - traceparent
  - correlationId
  - invocationId
  - provider transaction id
  finding_when: correlation is regenerated or not persisted and propagated across
    durable and external boundaries
  emit_on_failure: true
- id: FUNC-019
  title: Concurrency and scale settings protect downstream systems and correctness
  severity: high
  category: scaling
  applies_when: function can scale out or process batches
  evidence_patterns:
  - host.json concurrency
  - maxConcurrentCalls
  - batch size
  - dynamic concurrency
  - partition count
  finding_when: unbounded or mismatched concurrency overloads dependencies, violates
    ordering, or increases duplicate effects
  emit_on_failure: true
- id: FUNC-020
  title: Long-running work uses an appropriate execution model
  severity: high
  category: execution-model
  applies_when: invocation may exceed normal execution duration
  evidence_patterns:
  - Durable Functions
  - timeout
  - checkpoint
  - async polling
  finding_when: long-running work relies on one in-memory invocation without checkpoint,
    continuation, or durable orchestration
  emit_on_failure: true
- id: FUNC-021
  title: Client and resource lifecycle is safe across invocations
  severity: high
  category: resource-management
  applies_when: SDK, HTTP, database, or broker clients are used
  evidence_patterns:
  - static client
  - singleton
  - HttpClient
  - connection pool
  - dispose
  finding_when: clients are recreated per invocation, pools leak, or shared mutable
    state is unsafe under concurrency
  emit_on_failure: true
- id: FUNC-022
  title: Source excerpts and illustrative remediation preserve trigger contracts
  severity: high
  category: assessment-quality
  applies_when: remediation is proposed
  evidence_patterns:
  - function.json
  - annotations
  - attributes
  - binding names
  - return type
  finding_when: a proposed code change would alter trigger, binding, checkpoint, completion,
    authorization, or orchestration behavior without identifying the contract impact
  emit_on_failure: true
- id: FUNC-023
  title: Fault tests cover trigger-specific retry, replay, scaling, and recovery
  severity: critical
  category: testing
  applies_when: a Function trigger or Durable workflow exists
  evidence_patterns:
  - Azurite
  - Functions host test
  - Event Hubs test
  - Service Bus test
  - fault injection
  finding_when: tests do not prove duplicate input, retry exhaustion, poison handling,
    host recycle, scale-out, dependency outage, and recovery behavior
  emit_on_failure: true
---

# Azure Functions Resiliency and Processing Behavior Standard

### Shared-service operating-model contract

This standard does not select the application's shared-service topology. Resolve the operating model from:

```text
architecture_context.shared_service_operating_models.services.azure_function
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

This standard evaluates Azure Functions code and repository-owned configuration for reliable HTTP, timer, queue, Service Bus, Event Hubs, Kafka-style stream, and Durable Functions workloads. It incorporates recurring reliability patterns identified across the reviewed assessment reports.

## Scope boundary

Assess function code, trigger and binding declarations, host.json, repository-owned settings contracts, durable orchestration, SDK clients, retries, idempotency, checkpoint/completion behavior, fallback, security, observability, scaling assumptions, and tests. Do not infer deployed Function App plans, network topology, app settings, managed identity, storage redundancy, or regional deployment from absent repository evidence.

## Evaluator workflow

- Identify language, worker model, Functions runtime, extension/bundle versions, hosting plan evidence, and all triggers/bindings.
- Evaluate trigger-specific delivery, retry, completion, checkpoint, and poison behavior.
- Identify external side effects and stable operation identities.
- Inspect host.json, functions metadata, configuration validation, client lifecycle, concurrency, telemetry, and tests.
- Separate code findings from external platform evidence.
- Deduplicate with service-specific dependency standards.

## Required statuses

- `compliant`: Repository evidence demonstrates the behavior.
- `non_compliant`: Repository evidence demonstrates a gap.
- `not_assessed`: Evidence is unavailable or insufficient.
- `not_applicable`: The dependency or behavior does not apply.
- `accepted_risk`: A cited approved exception exists.

## Dependency-specific quality caveats

- Azure Functions trigger semantics vary by trigger type, extension version, language, and worker model; evaluate evidence, not generic assumptions.
- Identical inputs and retries require idempotent behavior.
- Event streams are not queues and do not intrinsically provide dead-letter semantics.
- A function timeout or exception does not prove an external side effect failed.
- Timer triggers and active-active deployments require explicit ownership or safely idempotent multi-active execution.
- Do not prescribe retry, concurrency, batch, timeout, or scale values without evidence.
- Missing deployed app settings, networking, identity, plan, or regional topology is `not_assessed`, not code noncompliance.

## Controls

### FUNC-001: Function triggers and handlers are idempotent

**Severity:** Critical  
**Category:** consistency  
**Applies when:** a trigger or HTTP function can receive duplicate input

#### Requirement

Each logical operation must use stable identity and concurrency-safe duplicate detection so identical input produces one effective outcome.

#### Repository evidence to inspect

- `idempotency key`
- `dedupe store`
- `event id`
- `unique constraint`
- `ETag`

#### Finding condition

Emit a finding when evidence shows that replay, redelivery, retry, or scale-out can repeat a business effect.

#### Evidence rule

Cite the repository-relative file path, symbol or property, original assessed line range, and exact source excerpt when available. Evaluate effective behavior rather than the presence of an annotation, resource, library, or default alone. If evidence is unavailable or external, return `not_assessed` rather than assuming noncompliance.

#### Quality caveats

- A random UUID generated on each invocation is correlation, not idempotency.
- Idempotency must cover external side effects, not only local persistence.

---

### FUNC-002: Retry policy matches trigger and operation semantics

**Severity:** Critical  
**Category:** resilience  
**Applies when:** a trigger or dependency can retry

#### Requirement

Use the runtime or application retry mechanism appropriate to the trigger. Classify transient failures, cap attempts and duration, preserve original identity, and route terminal failure explicitly.

#### Repository evidence to inspect

- `host.json retry`
- `FixedDelayRetry`
- `ExponentialBackoffRetry`
- `retry context`

#### Finding condition

Emit a finding when evidence shows that retry is absent where required, unbounded, or repeats a terminal or ambiguous non-idempotent operation.

#### Evidence rule

Cite the repository-relative file path, symbol or property, original assessed line range, and exact source excerpt when available. Evaluate effective behavior rather than the presence of an annotation, resource, library, or default alone. If evidence is unavailable or external, return `not_assessed` rather than assuming noncompliance.

#### Quality caveats

- Trigger retry behavior differs by binding and hosting model. Evaluate the actual extension and version.
- Do not blindly retry ambiguous financial or database outcomes.

---

### FUNC-003: Event Hubs and stream processing handle checkpoint advancement and poison events

**Severity:** Critical  
**Category:** event-processing  
**Applies when:** Event Hubs or Kafka-style stream trigger is used

#### Requirement

The handler must define per-event or per-batch failure behavior, durable failed-event capture, replay, and idempotent processing consistent with checkpoint advancement.

#### Repository evidence to inspect

- `EventHubTrigger`
- `consumer group`
- `checkpoint`
- `batch`
- `poison event`

#### Finding condition

Emit a finding when evidence shows that exceptions, batch handling, or checkpoint semantics can lose events, block a partition, or repeatedly poison healthy records.

#### Evidence rule

Cite the repository-relative file path, symbol or property, original assessed line range, and exact source excerpt when available. Evaluate effective behavior rather than the presence of an annotation, resource, library, or default alone. If evidence is unavailable or external, return `not_assessed` rather than assuming noncompliance.

#### Quality caveats

- Streams are not queues and do not provide inherent dead-letter semantics.
- A function exception does not by itself prove the event will be retried safely.

---

### FUNC-004: Queue and Service Bus completion follows successful durable processing

**Severity:** Critical  
**Category:** event-processing  
**Applies when:** queue or Service Bus trigger is used

#### Requirement

Completion must follow successful required processing. Terminal failures require bounded retry and dead-letter or durable failed-work routing.

#### Repository evidence to inspect

- `QueueTrigger`
- `ServiceBusTrigger`
- `completeMessage`
- `autoCompleteMessages`

#### Finding condition

Emit a finding when evidence shows that a message is completed before required durable or external work succeeds, or abandonment/dead-letter behavior is undefined.

#### Evidence rule

Cite the repository-relative file path, symbol or property, original assessed line range, and exact source excerpt when available. Evaluate effective behavior rather than the presence of an annotation, resource, library, or default alone. If evidence is unavailable or external, return `not_assessed` rather than assuming noncompliance.

#### Quality caveats

- Output binding failures might occur outside user code; evaluate binding semantics and observability.

---

### FUNC-005: Poison and terminal failures have a durable disposition

**Severity:** High  
**Category:** event-processing  
**Applies when:** event, queue, or scheduled processing exists

#### Requirement

Persist failed input with stable identity, reason, attempt count, correlation, and replay governance, or use a supported dead-letter mechanism.

#### Repository evidence to inspect

- `dead-letter`
- `poison queue`
- `failed event store`
- `attempt count`

#### Finding condition

Emit a finding when evidence shows that terminally failing input retries indefinitely, disappears, or blocks healthy processing.

#### Evidence rule

Cite the repository-relative file path, symbol or property, original assessed line range, and exact source excerpt when available. Evaluate effective behavior rather than the presence of an annotation, resource, library, or default alone. If evidence is unavailable or external, return `not_assessed` rather than assuming noncompliance.

#### Quality caveats

- Event Hubs has no native dead-letter queue; consumer-side handling must be explicit.

---

### FUNC-006: Timer-trigger and scheduled work ownership is safe across regions

**Severity:** Critical  
**Category:** workload-ownership  
**Applies when:** TimerTrigger or custom schedule exists

#### Requirement

Define whether scheduled work is single-active or safely multi-active. Use fail-safe regional activation, stable run identity, durable ownership, and split-brain detection where necessary.

#### Repository evidence to inspect

- `TimerTrigger`
- `useMonitor`
- `schedule status`
- `feature flag`
- `lease`

#### Finding condition

Emit a finding when evidence shows that both regions or function apps can execute the same schedule without an approved single-active or idempotent multi-active design.

#### Evidence rule

Cite the repository-relative file path, symbol or property, original assessed line range, and exact source excerpt when available. Evaluate effective behavior rather than the presence of an annotation, resource, library, or default alone. If evidence is unavailable or external, return `not_assessed` rather than assuming noncompliance.

#### Quality caveats

- A feature flag alone is not a distributed ownership guarantee.
- Do not assume inbound traffic management controls timer execution.

---

### FUNC-007: Batch and timer runs have durable run identity and terminal status

**Severity:** High  
**Category:** batch  
**Applies when:** scheduled or batch functions exist

#### Requirement

Record stable business-window identity, attempt history, terminal result, and reconciliation state before reporting completion.

#### Repository evidence to inspect

- `runId`
- `business date`
- `attempt`
- `last success`
- `completion status`

#### Finding condition

Emit a finding when evidence shows that reruns cannot distinguish complete, partial, failed, or duplicate execution.

#### Evidence rule

Cite the repository-relative file path, symbol or property, original assessed line range, and exact source excerpt when available. Evaluate effective behavior rather than the presence of an annotation, resource, library, or default alone. If evidence is unavailable or external, return `not_assessed` rather than assuming noncompliance.

#### Quality caveats

- Do not use invocation ID alone when the same business run can be retried.

---

### FUNC-008: Dependency calls have complete bounded time budgets

**Severity:** Critical  
**Category:** dependency-resilience  
**Applies when:** function calls remote services

#### Requirement

Every dependency call must have configurable per-attempt and overall deadlines and consume cancellation appropriately.

#### Repository evidence to inspect

- `HttpClient timeout`
- `SQL timeout`
- `Storage retry`
- `Cosmos retry`
- `CancellationToken`

#### Finding condition

Emit a finding when evidence shows that connection, pool acquisition, read, operation, or total execution can exceed the function or caller budget.

#### Evidence rule

Cite the repository-relative file path, symbol or property, original assessed line range, and exact source excerpt when available. Evaluate effective behavior rather than the presence of an annotation, resource, library, or default alone. If evidence is unavailable or external, return `not_assessed` rather than assuming noncompliance.

#### Quality caveats

- Coordinate retry and timeout with function execution limits, trigger lock/visibility duration, and upstream deadlines.

---

### FUNC-009: Non-idempotent and ambiguous external outcomes are reconciled

**Severity:** Critical  
**Category:** financial-integrity  
**Applies when:** function invokes payment or mutating external operation

#### Requirement

Persist durable intent and stable identity before the side effect, then use provider idempotency, status lookup, compensation, or reconciliation for ambiguous completion.

#### Repository evidence to inspect

- `provider transaction id`
- `status lookup`
- `reconciliation`
- `idempotency header`

#### Finding condition

Emit a finding when evidence shows that timeout or connection loss can lead to blind replay when the provider might have succeeded.

#### Evidence rule

Cite the repository-relative file path, symbol or property, original assessed line range, and exact source excerpt when available. Evaluate effective behavior rather than the presence of an annotation, resource, library, or default alone. If evidence is unavailable or external, return `not_assessed` rather than assuming noncompliance.

#### Quality caveats

- Timeout is not proof of failure.

---

### FUNC-010: Cross-store and output-binding workflows handle partial success

**Severity:** Critical  
**Category:** consistency  
**Applies when:** one invocation writes multiple systems

#### Requirement

Define ordering, durable intent, terminal status, and reconciliation for multiple stores, bindings, brokers, and providers.

#### Repository evidence to inspect

- `output binding`
- `SQL`
- `Cosmos`
- `Storage`
- `Service Bus`
- `Event Hubs`

#### Finding condition

Emit a finding when evidence shows that one destination can succeed while another fails without durable reconciliation.

#### Evidence rule

Cite the repository-relative file path, symbol or property, original assessed line range, and exact source excerpt when available. Evaluate effective behavior rather than the presence of an annotation, resource, library, or default alone. If evidence is unavailable or external, return `not_assessed` rather than assuming noncompliance.

#### Quality caveats

- A local transaction cannot atomically include independent Azure services.
- Output-binding errors can have different handling constraints from SDK calls.

---

### FUNC-011: Durable Functions orchestrators remain deterministic

**Severity:** Critical  
**Category:** durable-functions  
**Applies when:** Durable Functions orchestration is used

#### Requirement

Orchestrator logic must remain replay-safe and deterministic; external I/O and nondeterminism belong in activities or supported durable APIs.

#### Repository evidence to inspect

- `orchestration trigger`
- `DurableOrchestrationContext`
- `TaskOrchestrationContext`
- `currentUtcDateTime`

#### Finding condition

Emit a finding when evidence shows that orchestrator code performs nondeterministic I/O, random generation, wall-clock access, or unsupported side effects.

#### Evidence rule

Cite the repository-relative file path, symbol or property, original assessed line range, and exact source excerpt when available. Evaluate effective behavior rather than the presence of an annotation, resource, library, or default alone. If evidence is unavailable or external, return `not_assessed` rather than assuming noncompliance.

#### Quality caveats

- Orchestrator replay can execute code multiple times. Logging and side effects require replay-aware handling.

---

### FUNC-012: Durable activity retries and compensation are explicit

**Severity:** High  
**Category:** durable-functions  
**Applies when:** Durable Functions activities perform side effects

#### Requirement

Configure activity retry based on idempotency and define compensation or reconciliation for partial durable workflows.

#### Repository evidence to inspect

- `CallActivityWithRetry`
- `retry options`
- `compensation`
- `saga`

#### Finding condition

Emit a finding when evidence shows that activity side effects can repeat or partial workflow completion has no compensation or reconciliation.

#### Evidence rule

Cite the repository-relative file path, symbol or property, original assessed line range, and exact source excerpt when available. Evaluate effective behavior rather than the presence of an annotation, resource, library, or default alone. If evidence is unavailable or external, return `not_assessed` rather than assuming noncompliance.

#### Quality caveats

- Durable orchestration does not make an external activity side effect exactly-once.

---

### FUNC-013: Configuration, endpoints, and secrets are externalized and validated

**Severity:** Critical  
**Category:** configuration  
**Applies when:** function uses external services

#### Requirement

Use deployment-injected settings and approved identity/secret delivery. Validate required values and fail safely when invalid.

#### Repository evidence to inspect

- `local.settings.json`
- `app settings`
- `Key Vault reference`
- `environment variable`
- `options validation`

#### Finding condition

Emit a finding when evidence shows that regional endpoint, credential, or required setting is committed, hardcoded, missing validation, or defaults unsafely.

#### Evidence rule

Cite the repository-relative file path, symbol or property, original assessed line range, and exact source excerpt when available. Evaluate effective behavior rather than the presence of an annotation, resource, library, or default alone. If evidence is unavailable or external, return `not_assessed` rather than assuming noncompliance.

#### Quality caveats

- Do not commit local.settings.json secrets.
- Do not infer deployed app settings or Key Vault configuration from repository absence.

---

### FUNC-014: Managed identity and credential reuse avoid token stampedes

**Severity:** High  
**Category:** identity  
**Applies when:** Azure SDK or OAuth credentials are used

#### Requirement

Reuse thread-safe clients and supported credential chains, externalize identity selection, and bound authentication failure behavior.

#### Repository evidence to inspect

- `DefaultAzureCredential`
- `ManagedIdentityCredential`
- `TokenCredential`
- `client singleton`

#### Finding condition

Emit a finding when evidence shows that credentials or SDK clients are recreated per invocation, static secrets are embedded, or concurrent refresh can stampede.

#### Evidence rule

Cite the repository-relative file path, symbol or property, original assessed line range, and exact source excerpt when available. Evaluate effective behavior rather than the presence of an annotation, resource, library, or default alone. If evidence is unavailable or external, return `not_assessed` rather than assuming noncompliance.

#### Quality caveats

- Client reuse recommendations depend on the SDK thread-safety contract.

---

### FUNC-015: HTTP-trigger functions use safe methods, authorization, and error semantics

**Severity:** High  
**Category:** http-api  
**Applies when:** HTTP trigger exists

#### Requirement

Use safe HTTP semantics, explicit authorization, stable caller-visible status, correlation, and idempotency for mutating requests.

#### Repository evidence to inspect

- `HttpTrigger`
- `AuthorizationLevel`
- `GET`
- `POST`
- `429`
- `503`

#### Finding condition

Emit a finding when evidence shows that GET mutates state, authorization is overly permissive, or dependency failure is returned as success/not-found.

#### Evidence rule

Cite the repository-relative file path, symbol or property, original assessed line range, and exact source excerpt when available. Evaluate effective behavior rather than the presence of an annotation, resource, library, or default alone. If evidence is unavailable or external, return `not_assessed` rather than assuming noncompliance.

#### Quality caveats

- Platform authentication can complement but does not replace application authorization where business roles apply.

---

### FUNC-016: Fallback and synthetic success are durably recoverable

**Severity:** Critical  
**Category:** fallback  
**Applies when:** function returns deferred, accepted, or synthetic success

#### Requirement

Persist complete recovery state before success, make fallback independently bounded and observable, and define terminal handling.

#### Repository evidence to inspect

- `202`
- `fallback store`
- `synthetic approval`
- `on failure`

#### Finding condition

Emit a finding when evidence shows that success is returned before complete recoverable intent is durably recorded or fallback failure is silent.

#### Evidence rule

Cite the repository-relative file path, symbol or property, original assessed line range, and exact source excerpt when available. Evaluate effective behavior rather than the presence of an annotation, resource, library, or default alone. If evidence is unavailable or external, return `not_assessed` rather than assuming noncompliance.

#### Quality caveats

- Distinguish primary failure, fallback success, and dual failure.

---

### FUNC-017: Business throughput, backlog, retries, and stuck work are observable

**Severity:** High  
**Category:** observability  
**Applies when:** nontrivial trigger processing exists

#### Requirement

Emit safe structured telemetry for trigger, operation identity, region, instance, success/failure, retry, latency, backlog, dead-letter, and last successful processing.

#### Repository evidence to inspect

- `Application Insights`
- `custom metric`
- `backlog age`
- `last success`
- `dead-letter count`

#### Finding condition

Emit a finding when evidence shows that runtime health appears normal while processing stops, backlog grows, ownership is ambiguous, or terminal failures are invisible.

#### Evidence rule

Cite the repository-relative file path, symbol or property, original assessed line range, and exact source excerpt when available. Evaluate effective behavior rather than the presence of an annotation, resource, library, or default alone. If evidence is unavailable or external, return `not_assessed` rather than assuming noncompliance.

#### Quality caveats

- Avoid high-cardinality and sensitive tags.
- Runtime execution count alone may not prove business success.

---

### FUNC-018: Correlation identity propagates across triggers and dependencies

**Severity:** High  
**Category:** observability  
**Applies when:** workflow spans multiple services

#### Requirement

Preserve trace and business correlation from trigger through stores, events, and external providers while keeping idempotency identity distinct.

#### Repository evidence to inspect

- `traceparent`
- `correlationId`
- `invocationId`
- `provider transaction id`

#### Finding condition

Emit a finding when evidence shows that correlation is regenerated or not persisted and propagated across durable and external boundaries.

#### Evidence rule

Cite the repository-relative file path, symbol or property, original assessed line range, and exact source excerpt when available. Evaluate effective behavior rather than the presence of an annotation, resource, library, or default alone. If evidence is unavailable or external, return `not_assessed` rather than assuming noncompliance.

#### Quality caveats

- Invocation ID is not necessarily the business operation ID.

---

### FUNC-019: Concurrency and scale settings protect downstream systems and correctness

**Severity:** High  
**Category:** scaling  
**Applies when:** function can scale out or process batches

#### Requirement

Configure and test trigger concurrency, batch size, and downstream bulkheads according to ordering, partition, and dependency capacity requirements.

#### Repository evidence to inspect

- `host.json concurrency`
- `maxConcurrentCalls`
- `batch size`
- `dynamic concurrency`
- `partition count`

#### Finding condition

Emit a finding when evidence shows that unbounded or mismatched concurrency overloads dependencies, violates ordering, or increases duplicate effects.

#### Evidence rule

Cite the repository-relative file path, symbol or property, original assessed line range, and exact source excerpt when available. Evaluate effective behavior rather than the presence of an annotation, resource, library, or default alone. If evidence is unavailable or external, return `not_assessed` rather than assuming noncompliance.

#### Quality caveats

- Do not prescribe concurrency numbers without load evidence.
- Scaling configuration may be external and should be not_assessed when unavailable.

---

### FUNC-020: Long-running work uses an appropriate execution model

**Severity:** High  
**Category:** execution-model  
**Applies when:** invocation may exceed normal execution duration

#### Requirement

Use bounded units of work, durable orchestration, queues, or checkpoints so host recycle and scale events do not lose progress.

#### Repository evidence to inspect

- `Durable Functions`
- `timeout`
- `checkpoint`
- `async polling`

#### Finding condition

Emit a finding when evidence shows that long-running work relies on one in-memory invocation without checkpoint, continuation, or durable orchestration.

#### Evidence rule

Cite the repository-relative file path, symbol or property, original assessed line range, and exact source excerpt when available. Evaluate effective behavior rather than the presence of an annotation, resource, library, or default alone. If evidence is unavailable or external, return `not_assessed` rather than assuming noncompliance.

#### Quality caveats

- Do not use fire-and-forget background threads after function return.

---

### FUNC-021: Client and resource lifecycle is safe across invocations

**Severity:** High  
**Category:** resource-management  
**Applies when:** SDK, HTTP, database, or broker clients are used

#### Requirement

Reuse supported thread-safe clients, bound pools and caches, and avoid per-invocation connection or TLS setup.

#### Repository evidence to inspect

- `static client`
- `singleton`
- `HttpClient`
- `connection pool`
- `dispose`

#### Finding condition

Emit a finding when evidence shows that clients are recreated per invocation, pools leak, or shared mutable state is unsafe under concurrency.

#### Evidence rule

Cite the repository-relative file path, symbol or property, original assessed line range, and exact source excerpt when available. Evaluate effective behavior rather than the presence of an annotation, resource, library, or default alone. If evidence is unavailable or external, return `not_assessed` rather than assuming noncompliance.

#### Quality caveats

- Global mutable state can survive between invocations and must be concurrency safe.

---

### FUNC-022: Source excerpts and illustrative remediation preserve trigger contracts

**Severity:** High  
**Category:** assessment-quality  
**Applies when:** remediation is proposed

#### Requirement

Assessment and remediation artifacts must preserve exact trigger/binding evidence and explicitly validate any proposed contract changes.

#### Repository evidence to inspect

- `function.json`
- `annotations`
- `attributes`
- `binding names`
- `return type`

#### Finding condition

Emit a finding when evidence shows that a proposed code change would alter trigger, binding, checkpoint, completion, authorization, or orchestration behavior without identifying the contract impact.

#### Evidence rule

Cite the repository-relative file path, symbol or property, original assessed line range, and exact source excerpt when available. Evaluate effective behavior rather than the presence of an annotation, resource, library, or default alone. If evidence is unavailable or external, return `not_assessed` rather than assuming noncompliance.

#### Quality caveats

- Illustrative code is not an applied patch. Task Implementor must validate language model, extension version, and hosting model.

---

### FUNC-023: Fault tests cover trigger-specific retry, replay, scaling, and recovery

**Severity:** Critical  
**Category:** testing  
**Applies when:** a Function trigger or Durable workflow exists

#### Requirement

Automated or repeatable tests must exercise the actual trigger family and effective extension/version behavior, including duplicate delivery and recovery.

#### Repository evidence to inspect

- `Azurite`
- `Functions host test`
- `Event Hubs test`
- `Service Bus test`
- `fault injection`

#### Finding condition

Emit a finding when evidence shows that tests do not prove duplicate input, retry exhaustion, poison handling, host recycle, scale-out, dependency outage, and recovery behavior.

#### Evidence rule

Cite the repository-relative file path, symbol or property, original assessed line range, and exact source excerpt when available. Evaluate effective behavior rather than the presence of an annotation, resource, library, or default alone. If evidence is unavailable or external, return `not_assessed` rather than assuming noncompliance.

#### Quality caveats

- Mock-only tests do not prove runtime checkpoint or binding behavior.

---

## Standard finding format

- **Title:** [specific evidence-based gap]
- **Control:** [control ID]
- **Related controls:** [control IDs]
- **Severity:** [severity]
- **Repository evidence:** [file, symbol/property, original lines, exact excerpt]
- **Observed behavior:** [effective current behavior]
- **Regional or operational risk:** [failure effect]
- **Required code/configuration change:** [specific remediation]
- **Validation test:** [test proving behavior]
- **Confidence:** [high, medium, low]

## Non-findings

- Missing Function App, hosting plan, regional deployment, private endpoint, DNS, VNet integration, managed identity assignment, or storage account topology.
- Missing deployed app settings or Key Vault references when the repository only defines a configuration contract.
- Azure Front Door, APIM, load balancer, platform autoscale, and infrastructure deployment state.
- PCF migration, modernization, cleanup, or findings.
