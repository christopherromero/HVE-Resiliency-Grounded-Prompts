---
schema_version: "2.1.0"
document_type: dependency_standard
service: http-client
lifecycle_status: active
assessment_scope: application_client_behavior
---

# Spring HTTP and Blocking SDK Client Grounding

## Scope

Assess WebClient, RestClient, RestTemplate, Apache HttpClient, JDK HTTP clients, and blocking vendor SDK calls. Mesh and network routing are external evidence unless repository-owned configuration is explicitly in assessment scope.

## Controls

### HTTP-001: Complete timeout budget
Require connection, TLS handshake where available, pool-acquire, socket/read, response, and overall-operation deadlines. A sequence of calls must share an end-to-end deadline.

### HTTP-002: Blocking work is isolated
Blocking clients and vendor SDKs must not execute on Reactor event loops, health threads, or an unbounded/shared executor. Use a bounded dedicated execution resource and test saturation behavior.

### HTTP-003: Clients are isolated by dependency
Materially different dependencies require independent pools, timeouts, concurrency limits, and circuit-breaker telemetry.

### HTTP-004: Retry is classified and budgeted
Retry transient failures only, honor `Retry-After` when applicable, cap backoff and total duration, add controlled jitter, and keep the retry budget below the caller deadline.

### HTTP-005: Non-idempotent and ambiguous operations are safe
Do not retry charge, credit, capture, refund, cancel, void, or enrollment after ambiguous completion unless a stable provider-supported idempotency key or durable reconciliation makes it safe.

### HTTP-006: Authentication refresh is sequenced
On 401/expired token, invalidate and refresh within the same composed chain before any outer retry. Prevent refresh stampedes and preserve the original operation identity.

### HTTP-007: Circuit breaker and bulkhead reflect actual publisher execution
For Reactor, decorate with deferred operators around subscription. Guarding only publisher construction does not observe downstream failure.

### HTTP-008: Fallback semantics are explicit
Fallback must be bounded, independently observable, and must not convert required-data failure to null, empty, or success. Record primary failure, fallback success, and dual failure separately.

### HTTP-009: Shared dependencies are not blindly added to readiness
A globally shared provider should normally surface through metrics and circuit-breaker state rather than drain all regions. Readiness gating requires an evidenced region-local alternative.

### HTTP-010: Certificate and trust-material access is bounded
Do not fetch certificates or trust material on every request without timeout and cache. Require expiration monitoring, secure storage, rotation behavior, and bounded last-known-good use when approved.

#### HTTP-011: Reconciliation and status-lookup outcomes are classified correctly

Do not treat:

- timeout
- connection failure
- 5xx provider failure
- lookup failure
- unknown provider state
- incomplete provider response

as proof that:

- an operation succeeded
- an operation failed
- an operation is a duplicate

Require explicit handling of:

- success
- failure
- duplicate
- unknown

states.

Unknown outcomes must remain recoverable through
status lookup, reconciliation, compensation,
or controlled retry behavior.

A failed lookup must not suppress an operation
unless duplicate execution is proven.

#### HTTP-012: Business operation state machines preserve unknown outcomes

**Severity:** Critical

**Category:** data-correctness-and-reconciliation

**Applies when:**

The application performs a non-idempotent or externally observable business operation and uses any of the following to determine the operation's outcome:

- Provider status lookup
- Delivery lookup
- Duplicate lookup
- Reconciliation API
- Recovery workflow
- Callback or webhook
- Locally persisted operation state
- Fallback provider selection

Examples include:

- Order creation
- Payment authorization, capture, refund, or void
- Shipment or delivery creation
- Inventory reservation or release
- Customer enrollment
- Email or SMS delivery
- Loyalty transaction processing
- Partner API mutation

**Required behavior:**

Model business-operation outcomes using explicit states that preserve uncertainty.

The state model must distinguish at least:

- `pending`
- `completed`
- `failed`
- `duplicate`
- `unknown`

Additional domain-specific states may be used when required.

An `unknown` outcome must not be collapsed into:

- Success
- Completed
- Duplicate
- Permanent failure
- Safe-to-discard

unless authoritative evidence establishes that classification.

Duplicate classification requires positive evidence, such as:

- A matching stable business-operation identifier
- A matching provider idempotency key
- A provider response explicitly identifying the operation as duplicate
- A persisted authoritative operation record
- A successful status lookup that returns the previously completed operation

A timeout, connection failure, unavailable provider, HTTP `5xx`, malformed response, failed reconciliation lookup, or other transport failure is not proof of duplicate execution.

An HTTP `404` response may be treated as evidence that an operation does not exist only when the provider contract explicitly defines that behavior for the supplied stable operation identity. A `404` must not automatically be interpreted as duplicate, completed, or safe-to-discard.

**Unknown-outcome handling:**

When the outcome cannot be established, the application must use an explicitly governed recovery path, such as:

- Bounded status lookup
- Durable reconciliation
- Deferred recovery
- Retry using the same provider-supported idempotency key
- Safe fallback to another 

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
- Fallback to another provider must not occur while the primary-provider outcome is unknown unless duplicate effects are independently prevented### Shared-service operating-model contract

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

.