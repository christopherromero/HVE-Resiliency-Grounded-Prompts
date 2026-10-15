---
schema_version: "2.2.0"
document_type: dependency_standard
standard_id: SPRINGBOOT-HTTP-CLIENT
service: http-client
service_name: HTTP Client Behavior
language: java
framework: spring-boot
version: 2.2.0
lifecycle_status: active
assessment_scope: application_client_behavior
repository_owned_only: true
infrastructure_findings_allowed: false
assessment:
  enabled: true
  emit_findings: true
  include_in_score: true
  unknown_evidence_status: not_assessed
shared_service_assessment_scope:
  applicability: per_concrete_upstream_service
  service_key_resolution: registry
  context_path: architecture_context.shared_service_assessment_scope.services
  schema_path: grounding/governance/shared-service-assessment-scope-schema.yml
  evaluation_gate: required
  control_evaluation_allowed_only_when: in_scope
  architecture_reasoning_allowed_for:
  - in_scope
  - out_of_scope
  - informational_only
  - architecture_only
  scope_conflict_behavior: architecture_governance_review
  contract_section: Shared-service scope for concrete HTTP dependencies
controls:
- id: HTTP-001
  title: Complete timeout budget
  severity: critical
  category: timeout
  applies_when: the application makes outbound HTTP calls or blocking vendor SDK calls
  evidence_patterns:
  - connectTimeout
  - responseTimeout
  - ReadTimeout
  - setConnectionRequestTimeout
  - Mono.timeout
  finding_when: any layer of the timeout budget is unbounded or defaulted, or a sequence
    of calls has no shared end-to-end deadline
  emit_on_failure: true
- id: HTTP-002
  title: Blocking work is isolated
  severity: critical
  category: concurrency
  applies_when: blocking clients or vendor SDKs are invoked from reactive, scheduled,
    or shared-thread contexts
  evidence_patterns:
  - .block()
  - Schedulers.boundedElastic
  - subscribeOn
  - ForkJoinPool.commonPool
  - CompletableFuture.supplyAsync
  finding_when: blocking work executes on a Reactor event loop, a health or probe thread,
    or an unbounded or shared executor, or saturation behavior is untested
  emit_on_failure: true
- id: HTTP-003
  title: Clients are isolated by dependency
  severity: high
  category: bulkhead
  applies_when: the application calls more than one materially different upstream dependency
  evidence_patterns:
  - WebClient.Builder
  - ConnectionProvider
  - PoolingHttpClientConnectionManager
  - maxConnections
  - RestClient.builder
  finding_when: materially different dependencies share a connection pool, timeout
    profile, concurrency limit, or circuit-breaker identity so one dependency's degradation
    can exhaust capacity for another
  emit_on_failure: true
- id: HTTP-004
  title: Retry is classified and budgeted
  severity: critical
  category: retry
  applies_when: the application retries outbound calls
  evidence_patterns:
  - Retry.backoff
  - maxAttempts
  - RetryTemplate
  - Retry-After
  - jitter
  finding_when: retries are unbounded or unclassified, retry non-transient failures,
    omit jitter, ignore Retry-After where applicable, or consume a budget that exceeds
    the caller deadline
  emit_on_failure: true
- id: HTTP-005
  title: Non-idempotent and ambiguous operations are safe
  severity: critical
  category: data-correctness
  applies_when: the application performs charge, credit, capture, refund, cancel, void,
    enrollment, or other non-idempotent outbound operations
  evidence_patterns:
  - Idempotency-Key
  - idempotencyKey
  - business key
  - POST
  - reconciliation
  finding_when: a non-idempotent or externally observable operation is retried after
    an ambiguous completion without a stable provider-supported idempotency key or
    durable reconciliation
  emit_on_failure: true
- id: HTTP-006
  title: Authentication refresh is sequenced
  severity: high
  category: authentication
  applies_when: outbound calls use tokens, certificates, or credentials that expire
  evidence_patterns:
  - ExchangeFilterFunction
  - OAuth2AuthorizedClientManager
  - 401
  - token refresh
  - retryWhen
  finding_when: token refresh occurs outside the composed chain, permits a refresh
    stampede, or loses the original operation identity across refresh and retry
  emit_on_failure: true
- id: HTTP-007
  title: Circuit breaker and bulkhead reflect actual publisher execution
  severity: high
  category: resilience
  applies_when: resilience decorators guard reactive or asynchronous outbound calls
  evidence_patterns:
  - CircuitBreakerOperator
  - transformDeferred
  - BulkheadOperator
  - CircuitBreaker
  - Resilience4j
  finding_when: resilience decorators wrap publisher construction instead of subscription,
    so downstream failure is never observed by the breaker or bulkhead
  emit_on_failure: true
- id: HTTP-008
  title: Fallback semantics are explicit
  severity: critical
  category: degradation
  applies_when: the application defines a fallback, default, or degraded response for
    an outbound call
  evidence_patterns:
  - fallbackMethod
  - onErrorResume
  - onErrorReturn
  - Optional.empty
  - default value
  finding_when: a fallback is unbounded or unobservable, converts a required-data failure
    into null, empty, or success, or primary failure, fallback success, and dual failure
    cannot be distinguished
  emit_on_failure: true
- id: HTTP-009
  title: Shared dependencies are not blindly added to readiness
  severity: high
  category: health
  applies_when: an outbound HTTP dependency contributes to readiness, liveness, or
    a health group
  evidence_patterns:
  - HealthIndicator
  - ReactiveHealthIndicator
  - management.endpoint.health.group.readiness
  - readiness group
  - circuit-breaker state
  finding_when: a globally shared provider gates readiness without an evidenced region-local
    alternative so its failure drains every region, a critical region-local dependency
    is excluded from readiness with no degraded mode, or an outbound dependency participates
    in liveness
  emit_on_failure: true
- id: HTTP-010
  title: Certificate and trust-material access is bounded
  severity: high
  category: security-material
  applies_when: the application loads certificates, keystores, or trust material for
    outbound calls
  evidence_patterns:
  - SSLContext
  - KeyStore
  - TrustManager
  - certificate reload
  - expiration
  finding_when: certificates or trust material are fetched per request without timeout
    and cache, or expiration monitoring, secure storage, rotation behavior, and bounded
    last-known-good use are absent
  emit_on_failure: true
- id: HTTP-011
  title: Reconciliation and status-lookup outcomes are classified correctly
  severity: critical
  category: data-correctness-and-reconciliation
  applies_when: the application uses a status lookup, reconciliation call, or recovery
    path to determine an outbound operation's outcome
  evidence_patterns:
  - status lookup
  - reconciliation
  - TimeoutException
  - duplicate
  - '404'
  finding_when: a timeout, connection failure, 5xx response, failed lookup, unknown
    provider state, or incomplete response is treated as proof that an operation succeeded,
    failed, or is a duplicate, or an unknown outcome is not recoverable through status
    lookup, reconciliation, compensation, or controlled retry
  emit_on_failure: true
- id: HTTP-012
  title: Business operation state machines preserve unknown outcomes
  severity: critical
  category: data-correctness-and-reconciliation
  applies_when: the application performs a non-idempotent or externally observable
    business operation and determines its outcome from a provider lookup, reconciliation
    API, callback, persisted state, or fallback provider
  evidence_patterns:
  - operation state
  - pending
  - unknown
  - idempotency key
  - persisted operation record
  finding_when: an unknown outcome is collapsed into success, completed, duplicate,
    permanent failure, or safe-to-discard without authoritative evidence, duplicate
    is classified without positive evidence tied to the stable business-operation identity,
    or an HTTP 404 is treated as duplicate, completed, or safe-to-discard outside an
    explicit provider contract
  emit_on_failure: true
---

# Spring HTTP and Blocking SDK Client Grounding

## Scope

Assess WebClient, RestClient, RestTemplate, Apache HttpClient, JDK HTTP clients, and blocking vendor SDK calls. Mesh and network routing are external evidence unless repository-owned configuration is explicitly in assessment scope.

## Controls

### HTTP-001: Complete timeout budget

**Severity:** Critical  
**Category:** timeout  
**Applies when:** The application makes outbound HTTP calls or blocking vendor SDK calls.

**Requirement:** Require connection, TLS handshake where available, pool-acquire, socket/read, response, and overall-operation deadlines. A sequence of calls must share an end-to-end deadline.

**Evidence to inspect:** `connectTimeout`, `responseTimeout`, `ReadTimeout`, `setConnectionRequestTimeout`, `Mono.timeout`, client builder defaults.  
**Finding condition:** Emit a finding when any layer of the timeout budget is unbounded or defaulted, or when a sequence of calls has no shared end-to-end deadline.

### HTTP-002: Blocking work is isolated

**Severity:** Critical  
**Category:** concurrency  
**Applies when:** Blocking clients or vendor SDKs are invoked from reactive, scheduled, or shared-thread contexts.

**Requirement:** Blocking clients and vendor SDKs must not execute on Reactor event loops, health threads, or an unbounded/shared executor. Use a bounded dedicated execution resource and test saturation behavior.

**Evidence to inspect:** `.block()`, `Schedulers.boundedElastic`, `subscribeOn`, `ForkJoinPool.commonPool`, `CompletableFuture.supplyAsync`, executor definitions.  
**Finding condition:** Emit a finding when blocking work executes on a Reactor event loop, a health or probe thread, or an unbounded or shared executor, or when saturation behavior is untested.

### HTTP-003: Clients are isolated by dependency

**Severity:** High  
**Category:** bulkhead  
**Applies when:** The application calls more than one materially different upstream dependency.

**Requirement:** Materially different dependencies require independent pools, timeouts, concurrency limits, and circuit-breaker telemetry.

**Evidence to inspect:** `WebClient.Builder`, `RestClient.builder`, `ConnectionProvider`, `PoolingHttpClientConnectionManager`, `maxConnections`, shared bean definitions.  
**Finding condition:** Emit a finding when materially different dependencies share a connection pool, timeout profile, concurrency limit, or circuit-breaker identity so one dependency's degradation can exhaust capacity for another.

### HTTP-004: Retry is classified and budgeted

**Severity:** Critical  
**Category:** retry  
**Applies when:** The application retries outbound calls.

**Requirement:** Retry transient failures only, honor `Retry-After` when applicable, cap backoff and total duration, add controlled jitter, and keep the retry budget below the caller deadline.

**Evidence to inspect:** `Retry.backoff`, `maxAttempts`, `RetryTemplate`, `Retry-After` handling, jitter configuration, caller deadline.  
**Finding condition:** Emit a finding when retries are unbounded or unclassified, retry non-transient failures, omit jitter, ignore `Retry-After` where applicable, or consume a budget that exceeds the caller deadline.

### HTTP-005: Non-idempotent and ambiguous operations are safe

**Severity:** Critical  
**Category:** data-correctness  
**Applies when:** The application performs charge, credit, capture, refund, cancel, void, enrollment, or other non-idempotent outbound operations.

**Requirement:** Do not retry a non-idempotent operation after ambiguous completion unless a stable provider-supported idempotency key or durable reconciliation makes it safe.

**Evidence to inspect:** `Idempotency-Key` headers, stable business keys, POST semantics, reconciliation paths, retry configuration on mutating calls.  
**Finding condition:** Emit a finding when a non-idempotent or externally observable operation is retried after an ambiguous completion without a stable provider-supported idempotency key or durable reconciliation.

### HTTP-006: Authentication refresh is sequenced

**Severity:** High  
**Category:** authentication  
**Applies when:** Outbound calls use tokens, certificates, or credentials that expire.

**Requirement:** On 401 or expired token, invalidate and refresh within the same composed chain before any outer retry. Prevent refresh stampedes and preserve the original operation identity.

**Evidence to inspect:** `ExchangeFilterFunction`, `OAuth2AuthorizedClientManager`, 401 handling, token caches and locks, `retryWhen` placement.  
**Finding condition:** Emit a finding when token refresh occurs outside the composed chain, permits a refresh stampede, or loses the original operation identity across refresh and retry.

### HTTP-007: Circuit breaker and bulkhead reflect actual publisher execution

**Severity:** High  
**Category:** resilience  
**Applies when:** Resilience decorators guard reactive or asynchronous outbound calls.

**Requirement:** For Reactor, decorate with deferred operators around subscription. Guarding only publisher construction does not observe downstream failure.

**Evidence to inspect:** `CircuitBreakerOperator`, `transformDeferred`, `BulkheadOperator`, annotation placement, Resilience4j configuration.  
**Finding condition:** Emit a finding when resilience decorators wrap publisher construction instead of subscription, so downstream failure is never observed by the breaker or bulkhead.

### HTTP-008: Fallback semantics are explicit

**Severity:** Critical  
**Category:** degradation  
**Applies when:** The application defines a fallback, default, or degraded response for an outbound call.

**Requirement:** Fallback must be bounded, independently observable, and must not convert required-data failure to null, empty, or success. Record primary failure, fallback success, and dual failure separately.

**Evidence to inspect:** `fallbackMethod`, `onErrorResume`, `onErrorReturn`, `Optional.empty`, default values, fallback telemetry.  
**Finding condition:** Emit a finding when a fallback is unbounded or unobservable, converts a required-data failure into null, empty, or success, or when primary failure, fallback success, and dual failure cannot be distinguished.

### HTTP-009: Shared dependencies are not blindly added to readiness

**Severity:** High  
**Category:** health  
**Applies when:** An outbound HTTP dependency contributes to readiness, liveness, or a health group.

**Requirement:** A globally shared provider should normally surface through metrics and circuit-breaker state rather than drain all regions. Readiness gating requires an evidenced region-local alternative.

**Evidence to inspect:** `HealthIndicator`, `ReactiveHealthIndicator`, `management.endpoint.health.group.readiness`, liveness group composition, circuit-breaker state exposure.  
**Finding condition:** Emit a finding when a globally shared provider gates readiness without an evidenced region-local alternative so its failure drains every region, when a critical region-local dependency is excluded from readiness with no degraded mode, or when an outbound dependency participates in liveness.

### HTTP-010: Certificate and trust-material access is bounded

**Severity:** High  
**Category:** security-material  
**Applies when:** The application loads certificates, keystores, or trust material for outbound calls.

**Requirement:** Do not fetch certificates or trust material on every request without timeout and cache. Require expiration monitoring, secure storage, rotation behavior, and bounded last-known-good use when approved.

**Evidence to inspect:** `SSLContext`, `KeyStore`, `TrustManager`, certificate reload paths, expiration monitoring, secret storage.  
**Finding condition:** Emit a finding when certificates or trust material are fetched per request without timeout and cache, or when expiration monitoring, secure storage, rotation behavior, and bounded last-known-good use are absent.

### HTTP-011: Reconciliation and status-lookup outcomes are classified correctly

**Severity:** Critical  
**Category:** data-correctness-and-reconciliation  
**Applies when:** The application uses a status lookup, reconciliation call, or recovery path to determine an outbound operation's outcome.

**Requirement:** Do not treat a timeout, connection failure, 5xx provider failure, lookup failure, unknown provider state, or incomplete provider response as proof that an operation succeeded, failed, or is a duplicate. Require explicit handling of success, failure, duplicate, and unknown states. Unknown outcomes must remain recoverable through status lookup, reconciliation, compensation, or controlled retry behavior. A failed lookup must not suppress an operation unless duplicate execution is proven.

**Evidence to inspect:** Status-lookup and reconciliation calls, exception handling for `TimeoutException` and connection failures, duplicate classification logic, `404` interpretation.  
**Finding condition:** Emit a finding when a timeout, connection failure, 5xx response, failed lookup, unknown provider state, or incomplete response is treated as proof that an operation succeeded, failed, or is a duplicate, or when an unknown outcome is not recoverable through status lookup, reconciliation, compensation, or controlled retry.

### HTTP-012: Business operation state machines preserve unknown outcomes

**Severity:** Critical  
**Category:** data-correctness-and-reconciliation  
**Applies when:** The application performs a non-idempotent or externally observable business operation and determines its outcome from a provider status lookup, delivery lookup, duplicate lookup, reconciliation API, recovery workflow, callback or webhook, locally persisted operation state, or fallback provider selection.

Examples include order creation, payment authorization, capture, refund, or void, shipment or delivery creation, inventory reservation or release, customer enrollment, email or SMS delivery, loyalty transaction processing, and partner API mutation.

**Requirement:** Model business-operation outcomes using explicit states that preserve uncertainty. The state model must distinguish at least `pending`, `completed`, `failed`, `duplicate`, and `unknown`. Additional domain-specific states may be used when required.

An `unknown` outcome must not be collapsed into success, completed, duplicate, permanent failure, or safe-to-discard unless authoritative evidence establishes that classification.

Duplicate classification requires positive evidence, such as:

- A matching stable business-operation identifier
- A matching provider idempotency key
- A provider response explicitly identifying the operation as duplicate
- A persisted authoritative operation record
- A successful status lookup that returns the previously completed operation

A timeout, connection failure, unavailable provider, HTTP `5xx`, malformed response, failed reconciliation lookup, or other transport failure is not proof of duplicate execution.

An HTTP `404` response may be treated as evidence that an operation does not exist only when the provider contract explicitly defines that behavior for the supplied stable operation identity. A `404` must not automatically be interpreted as duplicate, completed, or safe-to-discard.

**Unknown-outcome handling:** When the outcome cannot be established, the application must use an explicitly governed recovery path, such as bounded status lookup, durable reconciliation, deferred recovery, retry using the same provider-supported idempotency key, or safe fallback to another provider only when duplicate effects are independently prevented.

**Evidence to inspect:** Operation state enums and persisted records, `pending`/`unknown` handling, idempotency keys, callback and webhook processing, fallback provider selection.  
**Finding condition:** Emit a finding when an unknown outcome is collapsed into success, completed, duplicate, permanent failure, or safe-to-discard without authoritative evidence, when duplicate is classified without positive evidence tied to the stable business-operation identity, or when an HTTP `404` is treated as duplicate, completed, or safe-to-discard outside an explicit provider contract.

## Evidence and finding rules

- Use the control `severity` and `category` declared in frontmatter; do not reassign severity per finding.
- Cite the file path, symbol, property, and line range when available.
- Return `not_assessed` when the repository lacks evidence to evaluate an applicable control.
- Mesh, gateway, and network routing behavior is external evidence unless the repository owns the configuration and the domain is in assessment scope.

## Quality caveats

- Prescribed timeout and retry numbers are illustrative unless evidenced and approved.
- `RestTemplate` presence alone is not a finding; missing budgets or unsafe threading are.
- A random UUID per attempt is not idempotency.
- A fallback response must not hide an incomplete financial operation.
- A failed status lookup is not proof of duplicate execution.
- Unknown outcomes must remain distinguishable from success.
- Duplicate classification requires positive evidence.
- An unsuccessful reconciliation or status lookup is not proof of duplicate execution.
- Duplicate classification requires positive evidence tied to the stable business-operation identity.
- Unknown provider outcomes must remain distinguishable from success, failure, and duplicate outcomes.
- An HTTP 404 establishes non-creation only when the approved provider contract explicitly defines that meaning for the supplied operation identity.
- A failed lookup must not silently suppress the original operation or prevent an otherwise safe recovery path.
- Fallback to another provider must not occur while the primary-provider outcome is unknown unless duplicate effects are independently prevented.

### Shared-service operating-model contract

This standard does not select the application's shared-service topology. Resolve the operating model from:

```text
architecture_context.shared_service_operating_models.services.<dependency-service-key>
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

For each concrete upstream dependency, use that dependency standard ID to locate the matching service entry. If no service entry exists, continue common HTTP controls and record the operating-model context gap; do not assume active-active.

### Shared-service scope for concrete HTTP dependencies

`http-client` is a cross-cutting client standard, not a declaration that every upstream service is in scope. For each concrete upstream service, resolve its canonical service key through the registry and apply `architecture_context.shared_service_assessment_scope.services`. Evaluate service-specific HTTP controls only when that concrete service is `in_scope`; otherwise preserve only the behavior allowed by its scope. Common application-owned HTTP client defects not attributable to an excluded service may still be evaluated under the application or cross-cutting scope.


## DSE/Kafka Active-Active Boundary

HTTP retry or reconciliation changes must not alter the DSE/Kafka business workflow, duplicate classification, or external-side-effect contract. Preserve stable operation identity across retries.
