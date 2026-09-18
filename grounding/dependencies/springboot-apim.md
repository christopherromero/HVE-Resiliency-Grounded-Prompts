---
schema_version: 2.2.0
document_type: dependency_behavior
service: apim
service_name: Azure API Management Client Behavior
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
- id: APIM-001
  title: Upstream API base URL is deployment-injected
  severity: critical
  category: configuration
  evidence_patterns:
  - base-url
  - WebClient.Builder
  - RestClient.Builder
  - FeignClient
  finding_when: APIM hostname or region is hardcoded
  emit_on_failure: true
  business_logic_risk: low
  requires_approval_before_implementation: false
  approval_owner: architecture
  safe_remediation_without_approval:
  - Externalize an existing hardcoded value to configuration while preserving the same effective default.
  - Add or improve metrics, logs, traces, and health details without changing decisions or payload content.
  - Add tests that characterize and lock in current behavior.
  requires_approval_for:
  - Changing the effective upstream endpoint or routing target.
- id: APIM-002
  title: Client honors bounded connect, response, and overall timeouts
  severity: critical
  category: resilience
  evidence_patterns:
  - WebClient timeout
  - HttpClient responseTimeout
  - Feign options
  finding_when: outbound API call can exceed failure budget
  emit_on_failure: true
  business_logic_risk: moderate
  requires_approval_before_implementation: false
  approval_owner: architecture
  safe_remediation_without_approval:
  - Add a bounded timeout where none exists, set to a value at or above observed p99 latency.
  - Add or improve metrics, logs, traces, and health details without changing decisions or payload content.
  - Add tests that characterize and lock in current behavior.
  requires_approval_for:
  - Reducing an existing timeout below observed successful call duration.
  - Changing an operation from unbounded to bounded where callers rely on long completion.
- id: APIM-003
  title: Retries are bounded and restricted to safe operations
  severity: critical
  category: resilience
  evidence_patterns:
  - Retry
  - Retry-After
  - HTTP method filtering
  finding_when: non-idempotent request can be duplicated or 429/5xx causes retry storm
  emit_on_failure: true
  business_logic_risk: severe
  requires_approval_before_implementation: true
  approval_owner: partner_contract_and_product
  safe_remediation_without_approval:
  - Add observability for retry attempts, exhaustion, and outcome classification.
  - Add tests that demonstrate current retry behavior.
  requires_approval_for:
  - Adding retries to any non-idempotent operation.
  - Changing which HTTP status codes trigger retry.
  - Changing retry counts or backoff where partner rate limits or costs apply.
- id: APIM-004
  title: Circuit breaker and bulkhead isolate failing APIs
  severity: high
  category: resilience
  evidence_patterns:
  - CircuitBreaker
  - Bulkhead
  - separate pool
  finding_when: failed API exhausts shared application resources
  emit_on_failure: true
  business_logic_risk: moderate
  requires_approval_before_implementation: false
  approval_owner: architecture
  safe_remediation_without_approval:
  - Add circuit-breaker and bulkhead telemetry without changing open or reject behavior.
  - Add tests that demonstrate the current behavior and the failure mode.
  requires_approval_for:
  - Introducing fail-fast rejection that changes caller-visible responses.
  - Changing fallback behavior.
- id: APIM-005
  title: Forwarded host, scheme, and client headers are handled safely
  severity: high
  category: http
  evidence_patterns:
  - ForwardedHeaderFilter
  - X-Forwarded-For
  - X-Forwarded-Proto
  finding_when: redirects, links, or security logic break behind regional gateways
  emit_on_failure: true
  business_logic_risk: severe
  requires_approval_before_implementation: true
  approval_owner: security
  safe_remediation_without_approval: &id001
  - Add or improve metrics, logs, traces, and health details without changing decisions or payload content.
  - Add tests that characterize and lock in current behavior.
  requires_approval_for:
  - Changing forwarded-header handling that affects client IP, scheme, redirect targets, or security decisions.
- id: APIM-006
  title: Correlation and region headers propagate through calls
  severity: medium
  category: observability
  evidence_patterns:
  - traceparent
  - correlation id
  - region tag
  finding_when: distributed requests cannot be traced by region
  emit_on_failure: true
  business_logic_risk: none
  requires_approval_before_implementation: false
  approval_owner: none
  safe_remediation_without_approval:
  - Add or improve metrics, logs, traces, and health details without changing decisions or payload content.
  - Add tests that characterize and lock in current behavior.
  - Add correlation and region propagation without altering request semantics.
  requires_approval_for: []
- id: APIM-007
  title: Critical upstream loss affects readiness only when no degraded mode exists
  severity: high
  category: health
  evidence_patterns:
  - HealthIndicator
  - fallback
  - readiness group
  finding_when: health does not align with business capability
  emit_on_failure: true
  business_logic_risk: severe
  requires_approval_before_implementation: true
  approval_owner: architecture_and_product
  safe_remediation_without_approval:
  - Add health telemetry distinguishing dependency state from readiness state.
  - Add tests that demonstrate the current behavior and the failure mode.
  requires_approval_for:
  - Adding or removing a dependency from readiness.
  - Changing degraded-mode behavior visible to callers.
- id: APIM-008
  title: Tests cover 429, 5xx, timeout, connection reset, duplicate prevention, and recovery
  severity: high
  category: testing
  evidence_patterns:
  - WireMock
  - MockWebServer
  - fault tests
  finding_when: client failure behavior is untested
  emit_on_failure: true
  business_logic_risk: none
  requires_approval_before_implementation: false
  approval_owner: none
  safe_remediation_without_approval:
  - Add tests that demonstrate the current behavior and the failure mode.
  requires_approval_for: []
- id: APIM-009
  title: Subscription keys, tokens, and certificates are externally supplied and refreshed safely
  severity: critical
  category: security
  evidence_patterns:
  - Ocp-Apim-Subscription-Key
  - Authorization header
  - TokenCredential
  - keystore
  - credential refresh
  finding_when: credentials are embedded in source, logged, or cannot be rotated without redeploying the
    application
  emit_on_failure: true
  business_logic_risk: severe
  requires_approval_before_implementation: true
  approval_owner: security
  safe_remediation_without_approval:
  - Add credential-failure and refresh telemetry with values redacted.
  - Add tests that demonstrate the current behavior and the failure mode.
  requires_approval_for:
  - Changing the credential type, scope, or authentication flow.
  - Changing credential refresh sequencing relative to retries.
- id: APIM-010
  title: Throttling responses honor server guidance with jittered backoff
  severity: high
  category: resilience
  evidence_patterns:
  - '429'
  - Retry-After
  - backoff
  - jitter
  - rate limiter
  finding_when: 429 or quota responses are retried immediately, ignore Retry-After, or use synchronized
    backoff across instances
  emit_on_failure: true
  business_logic_risk: moderate
  requires_approval_before_implementation: false
  approval_owner: architecture
  safe_remediation_without_approval:
  - Add jitter to existing backoff.
  - Add throttling telemetry.
  - Add tests that demonstrate the current behavior and the failure mode.
  requires_approval_for:
  - Honoring Retry-After where the application currently ignores it, when this changes partner call volume
    or user-visible latency.
- id: APIM-011
  title: Ambiguous upstream outcomes are not classified as success or duplicate
  severity: critical
  category: data-correctness
  evidence_patterns:
  - status lookup
  - reconcile
  - duplicate
  - '409'
  - '404'
  - unknown outcome
  finding_when: a timeout, transport failure, or failed status lookup is treated as proof that the operation
    succeeded, failed, or already exists
  emit_on_failure: true
  business_logic_risk: severe
  requires_approval_before_implementation: true
  approval_owner: partner_contract_and_product
  safe_remediation_without_approval:
  - Add telemetry that distinguishes success, failure, duplicate, and unknown outcomes.
  - Add tests that capture the current classification of each partner response.
  requires_approval_for:
  - Reinterpreting any HTTP status code, including 404 and 409.
  - Adding a status-lookup or reconciliation call.
  - Changing duplicate classification.
  - Changing fallback-provider conditions.
  - Changing which outcomes discard or retry a business operation.
- id: APIM-012
  title: Request and response payloads are bounded and streamed where required
  severity: high
  category: performance
  evidence_patterns:
  - maxInMemorySize
  - DataBufferLimit
  - stream
  - multipart
  - response buffering
  finding_when: large or unbounded upstream payloads are fully materialized in memory
  emit_on_failure: true
  business_logic_risk: moderate
  requires_approval_before_implementation: false
  approval_owner: architecture
  safe_remediation_without_approval:
  - Add payload-size telemetry.
  - Add tests that demonstrate the current behavior and the failure mode.
  requires_approval_for:
  - Introducing a size limit that can reject or truncate payloads the application currently accepts.
- id: APIM-013
  title: Connection pooling, endpoint resolution, and TLS material are managed for regional endpoints
  severity: high
  category: recovery
  evidence_patterns:
  - ConnectionProvider
  - maxConnections
  - dns ttl
  - SSLContext
  - truststore
  finding_when: stale connections, cached endpoint resolution, or expired TLS material prevent recovery
    without restart
  emit_on_failure: true
  business_logic_risk: moderate
  requires_approval_before_implementation: false
  approval_owner: platform_and_architecture
  safe_remediation_without_approval:
  - Add connection-pool and endpoint-resolution telemetry.
  - Add tests that demonstrate the current behavior and the failure mode.
  requires_approval_for:
  - Changing connection lifetime or endpoint caching where it alters regional routing behavior.
- id: APIM-014
  title: Stable idempotency identity is propagated for non-idempotent operations
  severity: critical
  category: consistency
  evidence_patterns:
  - Idempotency-Key
  - operation id
  - request id
  - dedupe key
  finding_when: each attempt generates a new identity or correlation identity is used as the idempotency
    key
  emit_on_failure: true
  business_logic_risk: severe
  requires_approval_before_implementation: true
  approval_owner: partner_contract
  safe_remediation_without_approval:
  - Add telemetry showing the identity sent with each attempt.
  - Add tests that demonstrate the current behavior and the failure mode.
  requires_approval_for:
  - Changing the idempotency key value, derivation, or header sent to a partner.
- id: APIM-015
  title: Cached upstream responses have bounded freshness and safe stale behavior
  severity: medium
  category: cache
  evidence_patterns:
  - cache
  - TTL
  - stale-while-revalidate
  - last known good
  finding_when: cached upstream data can be served beyond an approved staleness window or masks upstream
    failure as success
  emit_on_failure: true
  business_logic_risk: severe
  requires_approval_before_implementation: true
  approval_owner: product_and_security
  safe_remediation_without_approval:
  - Add cache hit, miss, age, and staleness telemetry.
  - Add tests that demonstrate the current behavior and the failure mode.
  requires_approval_for:
  - Changing cache TTL or staleness windows for authorization, pricing, entitlement, or inventory data.
  - Introducing stale-on-error serving.
- id: APIM-016
  title: API version and contract compatibility are explicit
  severity: medium
  category: contract
  evidence_patterns:
  - api-version
  - Accept header
  - DTO
  - schema
  - version path
  finding_when: the client depends on an implicit or unversioned upstream contract that can change without
    application awareness
  emit_on_failure: true
  business_logic_risk: severe
  requires_approval_before_implementation: true
  approval_owner: partner_contract
  safe_remediation_without_approval: *id001
  requires_approval_for:
  - Changing api-version, Accept headers, or request/response contract shape.
- id: APIM-017
  title: Diagnostics exclude secrets, tokens, and personal data
  severity: critical
  category: security
  evidence_patterns:
  - log request
  - log response
  - Authorization
  - PAN
  - PII
  - mask
  finding_when: request or response logging can emit credentials, tokens, signed headers, or personal
    data
  emit_on_failure: true
  business_logic_risk: low
  requires_approval_before_implementation: false
  approval_owner: security
  safe_remediation_without_approval:
  - Add or strengthen redaction and masking.
  - Add or improve metrics, logs, traces, and health details without changing decisions or payload content.
  - Add tests that characterize and lock in current behavior.
  requires_approval_for:
  - Removing or weakening existing redaction.
  - Adding logging that could expose payload content.
- id: APIM-018
  title: Client-side concurrency limiting prevents overload amplification
  severity: high
  category: resilience
  evidence_patterns:
  - Semaphore
  - bulkhead
  - max concurrent requests
  - queue limit
  finding_when: unbounded concurrent outbound calls can overwhelm the upstream API or exhaust local resources
    during degradation
  emit_on_failure: true
  business_logic_risk: moderate
  requires_approval_before_implementation: false
  approval_owner: architecture
  safe_remediation_without_approval:
  - Add concurrency and saturation telemetry.
  - Add tests that demonstrate the current behavior and the failure mode.
  requires_approval_for:
  - Introducing rejection or queuing that changes caller-visible behavior under load.
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

# Azure API Management Client Behavior Target-State Application Behavior Standard

### Shared-service operating-model contract

This standard does not select the application's shared-service topology. Resolve the operating model from:

```text
architecture_context.shared_service_operating_models.services.apim
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

This dependency-specific standard assesses how a Spring Boot microservice uses Azure API Management Client Behavior when evaluated for the approved target operating model supplied by application architecture context. The local regional service endpoint is assumed to exist and be reachable through the approved private networking design.

## Scope boundary

This standard assesses **application code, application configuration checked into the repository, and automated tests only**. It does not assess whether Azure or third-party infrastructure has been deployed correctly.

## Mandatory assumptions

- Two independent Azure regions are provisioned and active.
- AKS, networking, private endpoints, DNS, identities, certificates, and dependent services follow the approved active-active infrastructure design.
- The deployment pipeline injects region-specific configuration into the same application artifact.
- The application repository does not provision or validate infrastructure.

## Evaluator workflow

- Confirm the dependency is actually used by production code.
- Resolve source and target models from `architecture_context.shared_service_operating_models.services.apim` before evaluating model-specific controls.
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

### APIM-001: Upstream API base URL is deployment-injected

**Severity:** Critical  
**Category:** configuration

#### Requirement

The application code and configuration must satisfy this behavior when the same artifact runs in either active region.

#### Repository evidence to inspect

- `base-url`
- `WebClient.Builder`
- `RestClient.Builder`
- `FeignClient`

#### Finding condition

Emit a finding when evidence shows that APIM hostname or region is hardcoded.

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

- Changing the effective upstream endpoint or routing target.

---

### APIM-002: Client honors bounded connect, response, and overall timeouts

**Severity:** Critical  
**Category:** resilience

#### Requirement

The application code and configuration must satisfy this behavior when the same artifact runs in either active region.

#### Repository evidence to inspect

- `WebClient timeout`
- `HttpClient responseTimeout`
- `Feign options`

#### Finding condition

Emit a finding when evidence shows that outbound API call can exceed failure budget.

#### Evidence rule

Cite the file path, symbol or property, and advisory line range when available. Evaluate effective behavior rather than the presence of a library, annotation, or property alone. If the repository does not contain enough evidence, return `not_assessed` rather than assuming noncompliance.

#### Business-logic risk

**Risk level:** `moderate`  
**Requires approval before implementation:** `false`  
**Approval owner:** `architecture`

**Safe remediation without approval:**

- Add a bounded timeout where none exists, set to a value at or above observed p99 latency.
- Add or improve metrics, logs, traces, and health details without changing decisions or payload content.
- Add tests that characterize and lock in current behavior.

**Requires approval for:**

- Reducing an existing timeout below observed successful call duration.
- Changing an operation from unbounded to bounded where callers rely on long completion.

---

### APIM-003: Retries are bounded and restricted to safe operations

**Severity:** Critical  
**Category:** resilience

#### Requirement

The application code and configuration must satisfy this behavior when the same artifact runs in either active region.

#### Repository evidence to inspect

- `Retry`
- `Retry-After`
- `HTTP method filtering`

#### Finding condition

Emit a finding when evidence shows that non-idempotent request can be duplicated or 429/5xx causes retry storm.

#### Evidence rule

Cite the file path, symbol or property, and advisory line range when available. Evaluate effective behavior rather than the presence of a library, annotation, or property alone. If the repository does not contain enough evidence, return `not_assessed` rather than assuming noncompliance.

#### Business-logic risk

**Risk level:** `severe`  
**Requires approval before implementation:** `true`  
**Approval owner:** `partner_contract_and_product`

**Safe remediation without approval:**

- Add observability for retry attempts, exhaustion, and outcome classification.
- Add tests that demonstrate current retry behavior.

**Requires approval for:**

- Adding retries to any non-idempotent operation.
- Changing which HTTP status codes trigger retry.
- Changing retry counts or backoff where partner rate limits or costs apply.

---

### APIM-004: Circuit breaker and bulkhead isolate failing APIs

**Severity:** High  
**Category:** resilience

#### Requirement

The application code and configuration must satisfy this behavior when the same artifact runs in either active region.

#### Repository evidence to inspect

- `CircuitBreaker`
- `Bulkhead`
- `separate pool`

#### Finding condition

Emit a finding when evidence shows that failed API exhausts shared application resources.

#### Evidence rule

Cite the file path, symbol or property, and advisory line range when available. Evaluate effective behavior rather than the presence of a library, annotation, or property alone. If the repository does not contain enough evidence, return `not_assessed` rather than assuming noncompliance.

#### Business-logic risk

**Risk level:** `moderate`  
**Requires approval before implementation:** `false`  
**Approval owner:** `architecture`

**Safe remediation without approval:**

- Add circuit-breaker and bulkhead telemetry without changing open or reject behavior.
- Add tests that demonstrate the current behavior and the failure mode.

**Requires approval for:**

- Introducing fail-fast rejection that changes caller-visible responses.
- Changing fallback behavior.

---

### APIM-005: Forwarded host, scheme, and client headers are handled safely

**Severity:** High  
**Category:** http

#### Requirement

The application code and configuration must satisfy this behavior when the same artifact runs in either active region.

#### Repository evidence to inspect

- `ForwardedHeaderFilter`
- `X-Forwarded-For`
- `X-Forwarded-Proto`

#### Finding condition

Emit a finding when evidence shows that redirects, links, or security logic break behind regional gateways.

#### Evidence rule

Cite the file path, symbol or property, and advisory line range when available. Evaluate effective behavior rather than the presence of a library, annotation, or property alone. If the repository does not contain enough evidence, return `not_assessed` rather than assuming noncompliance.

#### Business-logic risk

**Risk level:** `severe`  
**Requires approval before implementation:** `true`  
**Approval owner:** `security`

**Safe remediation without approval:**

- Add or improve metrics, logs, traces, and health details without changing decisions or payload content.
- Add tests that characterize and lock in current behavior.

**Requires approval for:**

- Changing forwarded-header handling that affects client IP, scheme, redirect targets, or security decisions.

---

### APIM-006: Correlation and region headers propagate through calls

**Severity:** Medium  
**Category:** observability

#### Requirement

The application code and configuration must satisfy this behavior when the same artifact runs in either active region.

#### Repository evidence to inspect

- `traceparent`
- `correlation id`
- `region tag`

#### Finding condition

Emit a finding when evidence shows that distributed requests cannot be traced by region.

#### Evidence rule

Cite the file path, symbol or property, and advisory line range when available. Evaluate effective behavior rather than the presence of a library, annotation, or property alone. If the repository does not contain enough evidence, return `not_assessed` rather than assuming noncompliance.

#### Business-logic risk

**Risk level:** `none`  
**Requires approval before implementation:** `false`  
**Approval owner:** `none`

**Safe remediation without approval:**

- Add or improve metrics, logs, traces, and health details without changing decisions or payload content.
- Add tests that characterize and lock in current behavior.
- Add correlation and region propagation without altering request semantics.

---

### APIM-007: Critical upstream loss affects readiness only when no degraded mode exists

**Severity:** High  
**Category:** health

#### Requirement

The application code and configuration must satisfy this behavior when the same artifact runs in either active region.

#### Repository evidence to inspect

- `HealthIndicator`
- `fallback`
- `readiness group`

#### Finding condition

Emit a finding when evidence shows that health does not align with business capability.

#### Evidence rule

Cite the file path, symbol or property, and advisory line range when available. Evaluate effective behavior rather than the presence of a library, annotation, or property alone. If the repository does not contain enough evidence, return `not_assessed` rather than assuming noncompliance.

#### Business-logic risk

**Risk level:** `severe`  
**Requires approval before implementation:** `true`  
**Approval owner:** `architecture_and_product`

**Safe remediation without approval:**

- Add health telemetry distinguishing dependency state from readiness state.
- Add tests that demonstrate the current behavior and the failure mode.

**Requires approval for:**

- Adding or removing a dependency from readiness.
- Changing degraded-mode behavior visible to callers.

---

### APIM-008: Tests cover 429, 5xx, timeout, connection reset, duplicate prevention, and recovery

**Severity:** High  
**Category:** testing

#### Requirement

The application code and configuration must satisfy this behavior when the same artifact runs in either active region.

#### Repository evidence to inspect

- `WireMock`
- `MockWebServer`
- `fault tests`

#### Finding condition

Emit a finding when evidence shows that client failure behavior is untested.

#### Evidence rule

Cite the file path, symbol or property, and advisory line range when available. Evaluate effective behavior rather than the presence of a library, annotation, or property alone. If the repository does not contain enough evidence, return `not_assessed` rather than assuming noncompliance.

#### Business-logic risk

**Risk level:** `none`  
**Requires approval before implementation:** `false`  
**Approval owner:** `none`

**Safe remediation without approval:**

- Add tests that demonstrate the current behavior and the failure mode.

---

### APIM-009: Subscription keys, tokens, and certificates are externally supplied and refreshed safely

**Severity:** Critical  
**Category:** security

#### Requirement

The application code and configuration must satisfy this behavior when the same artifact runs in either active region.

#### Repository evidence to inspect

- `Ocp-Apim-Subscription-Key`
- `Authorization header`
- `TokenCredential`
- `keystore`
- `credential refresh`

#### Finding condition

Emit a finding when evidence shows that credentials are embedded in source, logged, or cannot be rotated without redeploying the application.

#### Evidence rule

Cite the file path, symbol or property, and advisory line range when available. Evaluate effective behavior rather than the presence of a library, annotation, or property alone. If the repository does not contain enough evidence, return `not_assessed` rather than assuming noncompliance.

#### Quality caveats

- Credential refresh must occur inside the same composed call chain so an outer retry does not reuse an expired credential.
- Do not weaken certificate or token validation to improve availability.

#### Business-logic risk

**Risk level:** `severe`  
**Requires approval before implementation:** `true`  
**Approval owner:** `security`

**Safe remediation without approval:**

- Add credential-failure and refresh telemetry with values redacted.
- Add tests that demonstrate the current behavior and the failure mode.

**Requires approval for:**

- Changing the credential type, scope, or authentication flow.
- Changing credential refresh sequencing relative to retries.

---

### APIM-010: Throttling responses honor server guidance with jittered backoff

**Severity:** High  
**Category:** resilience

#### Requirement

The application code and configuration must satisfy this behavior when the same artifact runs in either active region.

#### Repository evidence to inspect

- `429`
- `Retry-After`
- `backoff`
- `jitter`
- `rate limiter`

#### Finding condition

Emit a finding when evidence shows that 429 or quota responses are retried immediately, ignore Retry-After, or use synchronized backoff across instances.

#### Evidence rule

Cite the file path, symbol or property, and advisory line range when available. Evaluate effective behavior rather than the presence of a library, annotation, or property alone. If the repository does not contain enough evidence, return `not_assessed` rather than assuming noncompliance.

#### Quality caveats

- Backoff without jitter can synchronize retries across pods and regions.
- Client-side rate limiting does not replace honoring server guidance.

#### Business-logic risk

**Risk level:** `moderate`  
**Requires approval before implementation:** `false`  
**Approval owner:** `architecture`

**Safe remediation without approval:**

- Add jitter to existing backoff.
- Add throttling telemetry.
- Add tests that demonstrate the current behavior and the failure mode.

**Requires approval for:**

- Honoring Retry-After where the application currently ignores it, when this changes partner call volume or user-visible latency.

---

### APIM-011: Ambiguous upstream outcomes are not classified as success or duplicate

**Severity:** Critical  
**Category:** data-correctness

#### Requirement

The application code and configuration must satisfy this behavior when the same artifact runs in either active region.

#### Repository evidence to inspect

- `status lookup`
- `reconcile`
- `duplicate`
- `409`
- `404`
- `unknown outcome`

#### Finding condition

Emit a finding when evidence shows that a timeout, transport failure, or failed status lookup is treated as proof that the operation succeeded, failed, or already exists.

#### Evidence rule

Cite the file path, symbol or property, and advisory line range when available. Evaluate effective behavior rather than the presence of a library, annotation, or property alone. If the repository does not contain enough evidence, return `not_assessed` rather than assuming noncompliance.

#### Quality caveats

- A failed reconciliation lookup is not positive evidence of duplicate execution.
- The meaning of 404 or 409 must come from the approved provider contract, not generic resiliency guidance.

#### Business-logic risk

**Risk level:** `severe`  
**Requires approval before implementation:** `true`  
**Approval owner:** `partner_contract_and_product`

**Safe remediation without approval:**

- Add telemetry that distinguishes success, failure, duplicate, and unknown outcomes.
- Add tests that capture the current classification of each partner response.

**Requires approval for:**

- Reinterpreting any HTTP status code, including 404 and 409.
- Adding a status-lookup or reconciliation call.
- Changing duplicate classification.
- Changing fallback-provider conditions.
- Changing which outcomes discard or retry a business operation.

---

### APIM-012: Request and response payloads are bounded and streamed where required

**Severity:** High  
**Category:** performance

#### Requirement

The application code and configuration must satisfy this behavior when the same artifact runs in either active region.

#### Repository evidence to inspect

- `maxInMemorySize`
- `DataBufferLimit`
- `stream`
- `multipart`
- `response buffering`

#### Finding condition

Emit a finding when evidence shows that large or unbounded upstream payloads are fully materialized in memory.

#### Evidence rule

Cite the file path, symbol or property, and advisory line range when available. Evaluate effective behavior rather than the presence of a library, annotation, or property alone. If the repository does not contain enough evidence, return `not_assessed` rather than assuming noncompliance.

#### Quality caveats

- Bounding payloads must not silently truncate business data.

#### Business-logic risk

**Risk level:** `moderate`  
**Requires approval before implementation:** `false`  
**Approval owner:** `architecture`

**Safe remediation without approval:**

- Add payload-size telemetry.
- Add tests that demonstrate the current behavior and the failure mode.

**Requires approval for:**

- Introducing a size limit that can reject or truncate payloads the application currently accepts.

---

### APIM-013: Connection pooling, endpoint resolution, and TLS material are managed for regional endpoints

**Severity:** High  
**Category:** recovery

#### Requirement

The application code and configuration must satisfy this behavior when the same artifact runs in either active region.

#### Repository evidence to inspect

- `ConnectionProvider`
- `maxConnections`
- `dns ttl`
- `SSLContext`
- `truststore`

#### Finding condition

Emit a finding when evidence shows that stale connections, cached endpoint resolution, or expired TLS material prevent recovery without restart.

#### Evidence rule

Cite the file path, symbol or property, and advisory line range when available. Evaluate effective behavior rather than the presence of a library, annotation, or property alone. If the repository does not contain enough evidence, return `not_assessed` rather than assuming noncompliance.

#### Quality caveats

- Connection reuse is desirable, but stale resolution can pin traffic to a failed regional endpoint.

#### Business-logic risk

**Risk level:** `moderate`  
**Requires approval before implementation:** `false`  
**Approval owner:** `platform_and_architecture`

**Safe remediation without approval:**

- Add connection-pool and endpoint-resolution telemetry.
- Add tests that demonstrate the current behavior and the failure mode.

**Requires approval for:**

- Changing connection lifetime or endpoint caching where it alters regional routing behavior.

---

### APIM-014: Stable idempotency identity is propagated for non-idempotent operations

**Severity:** Critical  
**Category:** consistency

#### Requirement

The application code and configuration must satisfy this behavior when the same artifact runs in either active region.

#### Repository evidence to inspect

- `Idempotency-Key`
- `operation id`
- `request id`
- `dedupe key`

#### Finding condition

Emit a finding when evidence shows that each attempt generates a new identity or correlation identity is used as the idempotency key.

#### Evidence rule

Cite the file path, symbol or property, and advisory line range when available. Evaluate effective behavior rather than the presence of a library, annotation, or property alone. If the repository does not contain enough evidence, return `not_assessed` rather than assuming noncompliance.

#### Quality caveats

- A per-attempt UUID provides correlation, not duplicate prevention.

#### Business-logic risk

**Risk level:** `severe`  
**Requires approval before implementation:** `true`  
**Approval owner:** `partner_contract`

**Safe remediation without approval:**

- Add telemetry showing the identity sent with each attempt.
- Add tests that demonstrate the current behavior and the failure mode.

**Requires approval for:**

- Changing the idempotency key value, derivation, or header sent to a partner.

---

### APIM-015: Cached upstream responses have bounded freshness and safe stale behavior

**Severity:** Medium  
**Category:** cache

#### Requirement

The application code and configuration must satisfy this behavior when the same artifact runs in either active region.

#### Repository evidence to inspect

- `cache`
- `TTL`
- `stale-while-revalidate`
- `last known good`

#### Finding condition

Emit a finding when evidence shows that cached upstream data can be served beyond an approved staleness window or masks upstream failure as success.

#### Evidence rule

Cite the file path, symbol or property, and advisory line range when available. Evaluate effective behavior rather than the presence of a library, annotation, or property alone. If the repository does not contain enough evidence, return `not_assessed` rather than assuming noncompliance.

#### Quality caveats

- Stale authorization, pricing, or entitlement data can create business or security risk.

#### Business-logic risk

**Risk level:** `severe`  
**Requires approval before implementation:** `true`  
**Approval owner:** `product_and_security`

**Safe remediation without approval:**

- Add cache hit, miss, age, and staleness telemetry.
- Add tests that demonstrate the current behavior and the failure mode.

**Requires approval for:**

- Changing cache TTL or staleness windows for authorization, pricing, entitlement, or inventory data.
- Introducing stale-on-error serving.

---

### APIM-016: API version and contract compatibility are explicit

**Severity:** Medium  
**Category:** contract

#### Requirement

The application code and configuration must satisfy this behavior when the same artifact runs in either active region.

#### Repository evidence to inspect

- `api-version`
- `Accept header`
- `DTO`
- `schema`
- `version path`

#### Finding condition

Emit a finding when evidence shows that the client depends on an implicit or unversioned upstream contract that can change without application awareness.

#### Evidence rule

Cite the file path, symbol or property, and advisory line range when available. Evaluate effective behavior rather than the presence of a library, annotation, or property alone. If the repository does not contain enough evidence, return `not_assessed` rather than assuming noncompliance.

#### Quality caveats

- Contract changes are partner decisions and require approval before client behavior is altered.

#### Business-logic risk

**Risk level:** `severe`  
**Requires approval before implementation:** `true`  
**Approval owner:** `partner_contract`

**Safe remediation without approval:**

- Add or improve metrics, logs, traces, and health details without changing decisions or payload content.
- Add tests that characterize and lock in current behavior.

**Requires approval for:**

- Changing api-version, Accept headers, or request/response contract shape.

---

### APIM-017: Diagnostics exclude secrets, tokens, and personal data

**Severity:** Critical  
**Category:** security

#### Requirement

The application code and configuration must satisfy this behavior when the same artifact runs in either active region.

#### Repository evidence to inspect

- `log request`
- `log response`
- `Authorization`
- `PAN`
- `PII`
- `mask`

#### Finding condition

Emit a finding when evidence shows that request or response logging can emit credentials, tokens, signed headers, or personal data.

#### Evidence rule

Cite the file path, symbol or property, and advisory line range when available. Evaluate effective behavior rather than the presence of a library, annotation, or property alone. If the repository does not contain enough evidence, return `not_assessed` rather than assuming noncompliance.

#### Quality caveats

- Resiliency remediation must never weaken existing redaction or masking behavior.

#### Business-logic risk

**Risk level:** `low`  
**Requires approval before implementation:** `false`  
**Approval owner:** `security`

**Safe remediation without approval:**

- Add or strengthen redaction and masking.
- Add or improve metrics, logs, traces, and health details without changing decisions or payload content.
- Add tests that characterize and lock in current behavior.

**Requires approval for:**

- Removing or weakening existing redaction.
- Adding logging that could expose payload content.

---

### APIM-018: Client-side concurrency limiting prevents overload amplification

**Severity:** High  
**Category:** resilience

#### Requirement

The application code and configuration must satisfy this behavior when the same artifact runs in either active region.

#### Repository evidence to inspect

- `Semaphore`
- `bulkhead`
- `max concurrent requests`
- `queue limit`

#### Finding condition

Emit a finding when evidence shows that unbounded concurrent outbound calls can overwhelm the upstream API or exhaust local resources during degradation.

#### Evidence rule

Cite the file path, symbol or property, and advisory line range when available. Evaluate effective behavior rather than the presence of a library, annotation, or property alone. If the repository does not contain enough evidence, return `not_assessed` rather than assuming noncompliance.

#### Quality caveats

- Concurrency limits must be externally configurable and aligned with approved upstream capacity.

#### Business-logic risk

**Risk level:** `moderate`  
**Requires approval before implementation:** `false`  
**Approval owner:** `architecture`

**Safe remediation without approval:**

- Add concurrency and saturation telemetry.
- Add tests that demonstrate the current behavior and the failure mode.

**Requires approval for:**

- Introducing rejection or queuing that changes caller-visible behavior under load.

---

## Standard finding format

- **Title:** [specific code-level gap]
- **Control:** [APIM-NNN]
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
