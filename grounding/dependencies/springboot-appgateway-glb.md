---
schema_version: 2.1.0
document_type: dependency_behavior
service: appgateway-glb
service_name: Application Gateway and Global Load Balancer Behavior
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
- id: GLB-001
  title: Application exposes Spring Boot readiness and liveness endpoints
  severity: critical
  category: health
  evidence_patterns:
  - /actuator/health/readiness
  - /actuator/health/liveness
  finding_when: required probe endpoints are absent
  emit_on_failure: true
  business_logic_risk: moderate
  requires_approval_before_implementation: false
  approval_owner: architecture
  safe_remediation_without_approval:
  - Add readiness and liveness endpoints where none exist, initially reporting current effective state.
  - Add or improve metrics, logs, traces, and health details without changing decisions or payload content.
  - Add tests that characterize and lock in current behavior.
  requires_approval_for:
  - Changing what an existing probe reports.
- id: GLB-002
  title: Critical dependency failure propagates to readiness after bounded retries
  severity: critical
  category: health
  evidence_patterns:
  - HealthIndicator
  - readiness group
  - AvailabilityChangeEvent
  finding_when: failed regional dependency leaves pod ready
  emit_on_failure: true
  business_logic_risk: severe
  requires_approval_before_implementation: true
  approval_owner: architecture_and_product
  safe_remediation_without_approval:
  - Add dependency-state telemetry separate from readiness.
  - Add tests that demonstrate the current behavior and the failure mode.
  requires_approval_for:
  - Adding a dependency to readiness.
  - Changing when a pod becomes ineligible for traffic.
- id: GLB-003
  title: Liveness excludes external dependency health
  severity: critical
  category: health
  evidence_patterns:
  - liveness group
  finding_when: dependency outage triggers pod restart loops
  emit_on_failure: true
  business_logic_risk: severe
  requires_approval_before_implementation: true
  approval_owner: architecture
  safe_remediation_without_approval:
  - Add telemetry distinguishing liveness from dependency health.
  - Add tests that demonstrate the current behavior and the failure mode.
  requires_approval_for:
  - Changing liveness composition where it alters restart behavior.
- id: GLB-004
  title: Health endpoint is fast, local, bounded, and representative
  severity: critical
  category: health
  evidence_patterns:
  - probe timeout
  - health cache
  - main port
  finding_when: health check hangs, overloads dependencies, or bypasses the serving path
  emit_on_failure: true
  business_logic_risk: moderate
  requires_approval_before_implementation: false
  approval_owner: architecture
  safe_remediation_without_approval:
  - Add health-check duration and outcome telemetry.
  - Add tests that demonstrate the current behavior and the failure mode.
  requires_approval_for:
  - Changing what the health check evaluates.
- id: GLB-005
  title: Application handles forwarded headers and original scheme correctly
  severity: high
  category: http
  evidence_patterns:
  - server.forward-headers-strategy
  - ForwardedHeaderFilter
  finding_when: redirect, cookie, callback, or security behavior fails behind proxies
  emit_on_failure: true
  business_logic_risk: severe
  requires_approval_before_implementation: true
  approval_owner: security
  safe_remediation_without_approval: &id001
  - Add or improve metrics, logs, traces, and health details without changing decisions or payload content.
  - Add tests that characterize and lock in current behavior.
  requires_approval_for:
  - Changing forwarded-header strategy, scheme resolution, or redirect construction.
- id: GLB-006
  title: Session and authentication state do not require region stickiness
  severity: critical
  category: state
  evidence_patterns:
  - stateless session
  - external session store
  - JWT
  finding_when: traffic movement to another region loses required state
  emit_on_failure: true
  business_logic_risk: severe
  requires_approval_before_implementation: true
  approval_owner: architecture_and_security
  safe_remediation_without_approval:
  - Add session-affinity and state-location telemetry.
  - Add tests that demonstrate the current behavior and the failure mode.
  requires_approval_for:
  - Moving session or authentication state.
  - Changing session storage or token handling.
- id: GLB-007
  title: Graceful shutdown removes readiness before terminating work
  severity: high
  category: lifecycle
  evidence_patterns:
  - server.shutdown=graceful
  - preStop
  - readiness transition
  finding_when: terminating pod continues receiving traffic or drops work
  emit_on_failure: true
  business_logic_risk: moderate
  requires_approval_before_implementation: false
  approval_owner: platform_and_architecture
  safe_remediation_without_approval:
  - Add shutdown-phase telemetry.
  - Add tests that demonstrate the current behavior and the failure mode.
  requires_approval_for:
  - Changing shutdown duration where it affects deployment or in-flight request completion.
- id: GLB-008
  title: Tests verify probe transitions, recovery, and regional traffic eligibility
  severity: critical
  category: testing
  evidence_patterns:
  - Actuator integration test
  - fault injection
  finding_when: GLB-relevant health semantics are untested
  emit_on_failure: true
  business_logic_risk: none
  requires_approval_before_implementation: false
  approval_owner: none
  safe_remediation_without_approval:
  - Add tests that demonstrate the current behavior and the failure mode.
  requires_approval_for: []
- id: GLB-009
  title: Startup behavior is explicit and bounded
  severity: high
  category: lifecycle
  evidence_patterns:
  - startup probe
  - initialDelaySeconds
  - fail-fast
  - startup dependency
  finding_when: slow or failed initialization is handled by fixed probe delays, permanently masks failure,
    or allows liveness to kill a progressing startup
  emit_on_failure: true
  business_logic_risk: moderate
  requires_approval_before_implementation: false
  approval_owner: platform
  safe_remediation_without_approval:
  - Add startup-duration and startup-failure telemetry.
  - Add tests that demonstrate the current behavior and the failure mode.
  requires_approval_for:
  - Changing probe timing where it alters restart or rollout behavior.
- id: GLB-010
  title: Application timeouts align with gateway and idle timeouts
  severity: critical
  category: traffic-management
  evidence_patterns:
  - server timeout
  - idle timeout
  - request timeout
  - keep-alive
  finding_when: application, gateway, and load-balancer deadlines are unordered so an outer layer times
    out before the application can fail cleanly
  emit_on_failure: true
  business_logic_risk: severe
  requires_approval_before_implementation: true
  approval_owner: architecture
  safe_remediation_without_approval:
  - Add timeout-budget telemetry across layers.
  - Add tests that demonstrate the current behavior and the failure mode.
  requires_approval_for:
  - Changing any timeout where an outer layer currently absorbs the difference.
- id: GLB-011
  title: Long-lived connections define drain and failover behavior
  severity: high
  category: lifecycle
  evidence_patterns:
  - WebSocket
  - SSE
  - streaming
  - long polling
  finding_when: streaming or persistent connections are terminated abruptly or block pod drain beyond
    the termination budget
  emit_on_failure: true
  business_logic_risk: severe
  requires_approval_before_implementation: true
  approval_owner: product_and_architecture
  safe_remediation_without_approval:
  - Add connection-lifetime and drain telemetry.
  - Add tests that demonstrate the current behavior and the failure mode.
  requires_approval_for:
  - Changing streaming or persistent-connection termination behavior visible to clients.
- id: GLB-012
  title: Management endpoints are exposed safely behind regional ingress
  severity: critical
  category: management-security
  evidence_patterns:
  - management.server.port
  - exposure.include
  - EndpointRequest
  - show-details
  finding_when: probe or management endpoints expose sensitive diagnostics or administrative operations
    through externally reachable paths
  emit_on_failure: true
  business_logic_risk: severe
  requires_approval_before_implementation: true
  approval_owner: security
  safe_remediation_without_approval:
  - Add access telemetry for management endpoints.
  - Add tests that demonstrate the current behavior and the failure mode.
  requires_approval_for:
  - Changing management-endpoint exposure, authentication, or port where orchestration or operations depend
    on current access.
- id: GLB-013
  title: Gateway and application retries do not combine into duplicate work
  severity: critical
  category: resilience
  evidence_patterns:
  - retry
  - idempotency
  - POST
  - duplicate
  finding_when: layered retries can repeat a non-idempotent request without a stable operation identity
    or duplicate protection
  emit_on_failure: true
  business_logic_risk: severe
  requires_approval_before_implementation: true
  approval_owner: partner_contract_and_product
  safe_remediation_without_approval:
  - Add telemetry showing retry origin and duplicate exposure.
  - Add tests that demonstrate the current behavior and the failure mode.
  requires_approval_for:
  - Adding or removing retries at any layer for non-idempotent requests.
- id: GLB-014
  title: Generated URLs, redirects, and cookies are region-neutral
  severity: high
  category: http
  evidence_patterns:
  - absolute URL
  - redirect
  - Location header
  - cookie domain
  - callback URL
  finding_when: the application generates region-specific hostnames, redirect targets, or cookie scopes
    that break during regional traffic movement
  emit_on_failure: true
  business_logic_risk: severe
  requires_approval_before_implementation: true
  approval_owner: security_and_product
  safe_remediation_without_approval: *id001
  requires_approval_for:
  - Changing cookie domain, path, or scope.
  - Changing redirect targets or callback URLs.
  - Changing generated absolute URLs.
- id: GLB-015
  title: Forwarded header trust boundary is explicit
  severity: high
  category: security
  evidence_patterns:
  - trusted proxies
  - X-Forwarded-For
  - client IP
  - rate limit key
  finding_when: the application trusts client-controlled forwarded headers for security, rate limiting,
    auditing, or authorization decisions
  emit_on_failure: true
  business_logic_risk: severe
  requires_approval_before_implementation: true
  approval_owner: security
  safe_remediation_without_approval:
  - Add telemetry showing derived client IP and its source header.
  - Add tests that demonstrate the current behavior and the failure mode.
  requires_approval_for:
  - Changing client-IP derivation used for rate limiting, authorization, auditing, or fraud controls.
- id: GLB-016
  title: Connection lifecycle settings avoid mid-request termination
  severity: medium
  category: http
  evidence_patterns:
  - keep-alive
  - connection timeout
  - max connections
  - idle eviction
  finding_when: idle or keep-alive handling can terminate in-flight requests or leak connections during
    regional failover
  emit_on_failure: true
  business_logic_risk: moderate
  requires_approval_before_implementation: false
  approval_owner: platform_and_architecture
  safe_remediation_without_approval:
  - Add connection-lifecycle telemetry.
  - Add tests that demonstrate the current behavior and the failure mode.
  requires_approval_for:
  - Changing keep-alive or idle behavior where it can terminate in-flight requests.
- id: GLB-017
  title: Probe endpoints are stable, predictable, and orchestration-compatible
  severity: high
  category: health
  evidence_patterns:
  - probe path
  - management context path
  - health group names
  finding_when: probe paths change across environments, require authentication that orchestration cannot
    provide, or depend on undocumented behavior
  emit_on_failure: true
  business_logic_risk: moderate
  requires_approval_before_implementation: false
  approval_owner: platform
  safe_remediation_without_approval:
  - Document current probe paths and validate health-group contributor identifiers.
  - Add tests that demonstrate the current behavior and the failure mode.
  requires_approval_for:
  - Changing probe paths, ports, or authentication requirements.
- id: GLB-018
  title: Readiness transitions and traffic eligibility are observable
  severity: medium
  category: observability
  evidence_patterns:
  - readiness metric
  - AvailabilityChangeEvent
  - state change log
  - region tag
  finding_when: readiness changes and regional traffic eligibility cannot be observed or correlated during
    an incident
  emit_on_failure: true
  business_logic_risk: none
  requires_approval_before_implementation: false
  approval_owner: none
  safe_remediation_without_approval: *id001
  requires_approval_for: []
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

# Application Gateway and Global Load Balancer Behavior Active-Active Application Behavior Standard

## Purpose

This dependency-specific standard assesses how a Spring Boot microservice uses Application Gateway and Global Load Balancer Behavior when deployed to two active Azure regions. The local regional service endpoint is assumed to exist and be reachable through the approved private networking design.

## Scope boundary

This standard assesses **application code, application configuration checked into the repository, and automated tests only**. It does not assess whether Azure or third-party infrastructure has been deployed correctly.

## Mandatory assumptions

- Two independent Azure regions are provisioned and active.
- AKS, networking, private endpoints, DNS, identities, certificates, and dependent services follow the approved active-active infrastructure design.
- The deployment pipeline injects region-specific configuration into the same application artifact.
- The application repository does not provision or validate infrastructure.

## Evaluator workflow

- Confirm the dependency is actually used by production code.
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

### GLB-001: Application exposes Spring Boot readiness and liveness endpoints

**Severity:** Critical  
**Category:** health

#### Requirement

The application code and configuration must satisfy this behavior when the same artifact runs in either active region.

#### Repository evidence to inspect

- `/actuator/health/readiness`
- `/actuator/health/liveness`

#### Finding condition

Emit a finding when evidence shows that required probe endpoints are absent.

#### Evidence rule

Cite the file path, symbol or property, and advisory line range when available. Evaluate effective behavior rather than the presence of a library, annotation, or property alone. If the repository does not contain enough evidence, return `not_assessed` rather than assuming noncompliance.

#### Business-logic risk

**Risk level:** `moderate`  
**Requires approval before implementation:** `false`  
**Approval owner:** `architecture`

**Safe remediation without approval:**

- Add readiness and liveness endpoints where none exist, initially reporting current effective state.
- Add or improve metrics, logs, traces, and health details without changing decisions or payload content.
- Add tests that characterize and lock in current behavior.

**Requires approval for:**

- Changing what an existing probe reports.

---

### GLB-002: Critical dependency failure propagates to readiness after bounded retries

**Severity:** Critical  
**Category:** health

#### Requirement

The application code and configuration must satisfy this behavior when the same artifact runs in either active region.

#### Repository evidence to inspect

- `HealthIndicator`
- `readiness group`
- `AvailabilityChangeEvent`

#### Finding condition

Emit a finding when evidence shows that failed regional dependency leaves pod ready.

#### Evidence rule

Cite the file path, symbol or property, and advisory line range when available. Evaluate effective behavior rather than the presence of a library, annotation, or property alone. If the repository does not contain enough evidence, return `not_assessed` rather than assuming noncompliance.

#### Business-logic risk

**Risk level:** `severe`  
**Requires approval before implementation:** `true`  
**Approval owner:** `architecture_and_product`

**Safe remediation without approval:**

- Add dependency-state telemetry separate from readiness.
- Add tests that demonstrate the current behavior and the failure mode.

**Requires approval for:**

- Adding a dependency to readiness.
- Changing when a pod becomes ineligible for traffic.

---

### GLB-003: Liveness excludes external dependency health

**Severity:** Critical  
**Category:** health

#### Requirement

The application code and configuration must satisfy this behavior when the same artifact runs in either active region.

#### Repository evidence to inspect

- `liveness group`

#### Finding condition

Emit a finding when evidence shows that dependency outage triggers pod restart loops.

#### Evidence rule

Cite the file path, symbol or property, and advisory line range when available. Evaluate effective behavior rather than the presence of a library, annotation, or property alone. If the repository does not contain enough evidence, return `not_assessed` rather than assuming noncompliance.

#### Business-logic risk

**Risk level:** `severe`  
**Requires approval before implementation:** `true`  
**Approval owner:** `architecture`

**Safe remediation without approval:**

- Add telemetry distinguishing liveness from dependency health.
- Add tests that demonstrate the current behavior and the failure mode.

**Requires approval for:**

- Changing liveness composition where it alters restart behavior.

---

### GLB-004: Health endpoint is fast, local, bounded, and representative

**Severity:** Critical  
**Category:** health

#### Requirement

The application code and configuration must satisfy this behavior when the same artifact runs in either active region.

#### Repository evidence to inspect

- `probe timeout`
- `health cache`
- `main port`

#### Finding condition

Emit a finding when evidence shows that health check hangs, overloads dependencies, or bypasses the serving path.

#### Evidence rule

Cite the file path, symbol or property, and advisory line range when available. Evaluate effective behavior rather than the presence of a library, annotation, or property alone. If the repository does not contain enough evidence, return `not_assessed` rather than assuming noncompliance.

#### Business-logic risk

**Risk level:** `moderate`  
**Requires approval before implementation:** `false`  
**Approval owner:** `architecture`

**Safe remediation without approval:**

- Add health-check duration and outcome telemetry.
- Add tests that demonstrate the current behavior and the failure mode.

**Requires approval for:**

- Changing what the health check evaluates.

---

### GLB-005: Application handles forwarded headers and original scheme correctly

**Severity:** High  
**Category:** http

#### Requirement

The application code and configuration must satisfy this behavior when the same artifact runs in either active region.

#### Repository evidence to inspect

- `server.forward-headers-strategy`
- `ForwardedHeaderFilter`

#### Finding condition

Emit a finding when evidence shows that redirect, cookie, callback, or security behavior fails behind proxies.

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

- Changing forwarded-header strategy, scheme resolution, or redirect construction.

---

### GLB-006: Session and authentication state do not require region stickiness

**Severity:** Critical  
**Category:** state

#### Requirement

The application code and configuration must satisfy this behavior when the same artifact runs in either active region.

#### Repository evidence to inspect

- `stateless session`
- `external session store`
- `JWT`

#### Finding condition

Emit a finding when evidence shows that traffic movement to another region loses required state.

#### Evidence rule

Cite the file path, symbol or property, and advisory line range when available. Evaluate effective behavior rather than the presence of a library, annotation, or property alone. If the repository does not contain enough evidence, return `not_assessed` rather than assuming noncompliance.

#### Business-logic risk

**Risk level:** `severe`  
**Requires approval before implementation:** `true`  
**Approval owner:** `architecture_and_security`

**Safe remediation without approval:**

- Add session-affinity and state-location telemetry.
- Add tests that demonstrate the current behavior and the failure mode.

**Requires approval for:**

- Moving session or authentication state.
- Changing session storage or token handling.

---

### GLB-007: Graceful shutdown removes readiness before terminating work

**Severity:** High  
**Category:** lifecycle

#### Requirement

The application code and configuration must satisfy this behavior when the same artifact runs in either active region.

#### Repository evidence to inspect

- `server.shutdown=graceful`
- `preStop`
- `readiness transition`

#### Finding condition

Emit a finding when evidence shows that terminating pod continues receiving traffic or drops work.

#### Evidence rule

Cite the file path, symbol or property, and advisory line range when available. Evaluate effective behavior rather than the presence of a library, annotation, or property alone. If the repository does not contain enough evidence, return `not_assessed` rather than assuming noncompliance.

#### Business-logic risk

**Risk level:** `moderate`  
**Requires approval before implementation:** `false`  
**Approval owner:** `platform_and_architecture`

**Safe remediation without approval:**

- Add shutdown-phase telemetry.
- Add tests that demonstrate the current behavior and the failure mode.

**Requires approval for:**

- Changing shutdown duration where it affects deployment or in-flight request completion.

---

### GLB-008: Tests verify probe transitions, recovery, and regional traffic eligibility

**Severity:** Critical  
**Category:** testing

#### Requirement

The application code and configuration must satisfy this behavior when the same artifact runs in either active region.

#### Repository evidence to inspect

- `Actuator integration test`
- `fault injection`

#### Finding condition

Emit a finding when evidence shows that GLB-relevant health semantics are untested.

#### Evidence rule

Cite the file path, symbol or property, and advisory line range when available. Evaluate effective behavior rather than the presence of a library, annotation, or property alone. If the repository does not contain enough evidence, return `not_assessed` rather than assuming noncompliance.

#### Business-logic risk

**Risk level:** `none`  
**Requires approval before implementation:** `false`  
**Approval owner:** `none`

**Safe remediation without approval:**

- Add tests that demonstrate the current behavior and the failure mode.

---

### GLB-009: Startup behavior is explicit and bounded

**Severity:** High  
**Category:** lifecycle

#### Requirement

The application code and configuration must satisfy this behavior when the same artifact runs in either active region.

#### Repository evidence to inspect

- `startup probe`
- `initialDelaySeconds`
- `fail-fast`
- `startup dependency`

#### Finding condition

Emit a finding when evidence shows that slow or failed initialization is handled by fixed probe delays, permanently masks failure, or allows liveness to kill a progressing startup.

#### Evidence rule

Cite the file path, symbol or property, and advisory line range when available. Evaluate effective behavior rather than the presence of a library, annotation, or property alone. If the repository does not contain enough evidence, return `not_assessed` rather than assuming noncompliance.

#### Quality caveats

- Probe timing must reflect measured startup behavior rather than an arbitrary value.

#### Business-logic risk

**Risk level:** `moderate`  
**Requires approval before implementation:** `false`  
**Approval owner:** `platform`

**Safe remediation without approval:**

- Add startup-duration and startup-failure telemetry.
- Add tests that demonstrate the current behavior and the failure mode.

**Requires approval for:**

- Changing probe timing where it alters restart or rollout behavior.

---

### GLB-010: Application timeouts align with gateway and idle timeouts

**Severity:** Critical  
**Category:** traffic-management

#### Requirement

The application code and configuration must satisfy this behavior when the same artifact runs in either active region.

#### Repository evidence to inspect

- `server timeout`
- `idle timeout`
- `request timeout`
- `keep-alive`

#### Finding condition

Emit a finding when evidence shows that application, gateway, and load-balancer deadlines are unordered so an outer layer times out before the application can fail cleanly.

#### Evidence rule

Cite the file path, symbol or property, and advisory line range when available. Evaluate effective behavior rather than the presence of a library, annotation, or property alone. If the repository does not contain enough evidence, return `not_assessed` rather than assuming noncompliance.

#### Quality caveats

- Budget ordering must be coordinated; do not prescribe values without measured evidence.

#### Business-logic risk

**Risk level:** `severe`  
**Requires approval before implementation:** `true`  
**Approval owner:** `architecture`

**Safe remediation without approval:**

- Add timeout-budget telemetry across layers.
- Add tests that demonstrate the current behavior and the failure mode.

**Requires approval for:**

- Changing any timeout where an outer layer currently absorbs the difference.

---

### GLB-011: Long-lived connections define drain and failover behavior

**Severity:** High  
**Category:** lifecycle

#### Requirement

The application code and configuration must satisfy this behavior when the same artifact runs in either active region.

#### Repository evidence to inspect

- `WebSocket`
- `SSE`
- `streaming`
- `long polling`

#### Finding condition

Emit a finding when evidence shows that streaming or persistent connections are terminated abruptly or block pod drain beyond the termination budget.

#### Evidence rule

Cite the file path, symbol or property, and advisory line range when available. Evaluate effective behavior rather than the presence of a library, annotation, or property alone. If the repository does not contain enough evidence, return `not_assessed` rather than assuming noncompliance.

#### Quality caveats

- Persistent connections may require client reconnection contracts, not only server-side draining.

#### Business-logic risk

**Risk level:** `severe`  
**Requires approval before implementation:** `true`  
**Approval owner:** `product_and_architecture`

**Safe remediation without approval:**

- Add connection-lifetime and drain telemetry.
- Add tests that demonstrate the current behavior and the failure mode.

**Requires approval for:**

- Changing streaming or persistent-connection termination behavior visible to clients.

---

### GLB-012: Management endpoints are exposed safely behind regional ingress

**Severity:** Critical  
**Category:** management-security

#### Requirement

The application code and configuration must satisfy this behavior when the same artifact runs in either active region.

#### Repository evidence to inspect

- `management.server.port`
- `exposure.include`
- `EndpointRequest`
- `show-details`

#### Finding condition

Emit a finding when evidence shows that probe or management endpoints expose sensitive diagnostics or administrative operations through externally reachable paths.

#### Evidence rule

Cite the file path, symbol or property, and advisory line range when available. Evaluate effective behavior rather than the presence of a library, annotation, or property alone. If the repository does not contain enough evidence, return `not_assessed` rather than assuming noncompliance.

#### Quality caveats

- Probe endpoints must remain reachable for orchestration while sensitive endpoints stay restricted.

#### Business-logic risk

**Risk level:** `severe`  
**Requires approval before implementation:** `true`  
**Approval owner:** `security`

**Safe remediation without approval:**

- Add access telemetry for management endpoints.
- Add tests that demonstrate the current behavior and the failure mode.

**Requires approval for:**

- Changing management-endpoint exposure, authentication, or port where orchestration or operations depend on current access.

---

### GLB-013: Gateway and application retries do not combine into duplicate work

**Severity:** Critical  
**Category:** resilience

#### Requirement

The application code and configuration must satisfy this behavior when the same artifact runs in either active region.

#### Repository evidence to inspect

- `retry`
- `idempotency`
- `POST`
- `duplicate`

#### Finding condition

Emit a finding when evidence shows that layered retries can repeat a non-idempotent request without a stable operation identity or duplicate protection.

#### Evidence rule

Cite the file path, symbol or property, and advisory line range when available. Evaluate effective behavior rather than the presence of a library, annotation, or property alone. If the repository does not contain enough evidence, return `not_assessed` rather than assuming noncompliance.

#### Quality caveats

- Gateway retry configuration may be external evidence; assess the application behavior that makes retries safe.

#### Business-logic risk

**Risk level:** `severe`  
**Requires approval before implementation:** `true`  
**Approval owner:** `partner_contract_and_product`

**Safe remediation without approval:**

- Add telemetry showing retry origin and duplicate exposure.
- Add tests that demonstrate the current behavior and the failure mode.

**Requires approval for:**

- Adding or removing retries at any layer for non-idempotent requests.

---

### GLB-014: Generated URLs, redirects, and cookies are region-neutral

**Severity:** High  
**Category:** http

#### Requirement

The application code and configuration must satisfy this behavior when the same artifact runs in either active region.

#### Repository evidence to inspect

- `absolute URL`
- `redirect`
- `Location header`
- `cookie domain`
- `callback URL`

#### Finding condition

Emit a finding when evidence shows that the application generates region-specific hostnames, redirect targets, or cookie scopes that break during regional traffic movement.

#### Evidence rule

Cite the file path, symbol or property, and advisory line range when available. Evaluate effective behavior rather than the presence of a library, annotation, or property alone. If the repository does not contain enough evidence, return `not_assessed` rather than assuming noncompliance.

#### Quality caveats

- Cookie scope and callback URLs may be part of an approved security contract and require approval before change.

#### Business-logic risk

**Risk level:** `severe`  
**Requires approval before implementation:** `true`  
**Approval owner:** `security_and_product`

**Safe remediation without approval:**

- Add or improve metrics, logs, traces, and health details without changing decisions or payload content.
- Add tests that characterize and lock in current behavior.

**Requires approval for:**

- Changing cookie domain, path, or scope.
- Changing redirect targets or callback URLs.
- Changing generated absolute URLs.

---

### GLB-015: Forwarded header trust boundary is explicit

**Severity:** High  
**Category:** security

#### Requirement

The application code and configuration must satisfy this behavior when the same artifact runs in either active region.

#### Repository evidence to inspect

- `trusted proxies`
- `X-Forwarded-For`
- `client IP`
- `rate limit key`

#### Finding condition

Emit a finding when evidence shows that the application trusts client-controlled forwarded headers for security, rate limiting, auditing, or authorization decisions.

#### Evidence rule

Cite the file path, symbol or property, and advisory line range when available. Evaluate effective behavior rather than the presence of a library, annotation, or property alone. If the repository does not contain enough evidence, return `not_assessed` rather than assuming noncompliance.

#### Quality caveats

- Client IP derivation is security sensitive; changes require security review.

#### Business-logic risk

**Risk level:** `severe`  
**Requires approval before implementation:** `true`  
**Approval owner:** `security`

**Safe remediation without approval:**

- Add telemetry showing derived client IP and its source header.
- Add tests that demonstrate the current behavior and the failure mode.

**Requires approval for:**

- Changing client-IP derivation used for rate limiting, authorization, auditing, or fraud controls.

---

### GLB-016: Connection lifecycle settings avoid mid-request termination

**Severity:** Medium  
**Category:** http

#### Requirement

The application code and configuration must satisfy this behavior when the same artifact runs in either active region.

#### Repository evidence to inspect

- `keep-alive`
- `connection timeout`
- `max connections`
- `idle eviction`

#### Finding condition

Emit a finding when evidence shows that idle or keep-alive handling can terminate in-flight requests or leak connections during regional failover.

#### Evidence rule

Cite the file path, symbol or property, and advisory line range when available. Evaluate effective behavior rather than the presence of a library, annotation, or property alone. If the repository does not contain enough evidence, return `not_assessed` rather than assuming noncompliance.

#### Quality caveats

- Connection settings must be coordinated with gateway and mesh behavior.

#### Business-logic risk

**Risk level:** `moderate`  
**Requires approval before implementation:** `false`  
**Approval owner:** `platform_and_architecture`

**Safe remediation without approval:**

- Add connection-lifecycle telemetry.
- Add tests that demonstrate the current behavior and the failure mode.

**Requires approval for:**

- Changing keep-alive or idle behavior where it can terminate in-flight requests.

---

### GLB-017: Probe endpoints are stable, predictable, and orchestration-compatible

**Severity:** High  
**Category:** health

#### Requirement

The application code and configuration must satisfy this behavior when the same artifact runs in either active region.

#### Repository evidence to inspect

- `probe path`
- `management context path`
- `health group names`

#### Finding condition

Emit a finding when evidence shows that probe paths change across environments, require authentication that orchestration cannot provide, or depend on undocumented behavior.

#### Evidence rule

Cite the file path, symbol or property, and advisory line range when available. Evaluate effective behavior rather than the presence of a library, annotation, or property alone. If the repository does not contain enough evidence, return `not_assessed` rather than assuming noncompliance.

#### Quality caveats

- Health-group names must be validated against actual contributor identifiers.

#### Business-logic risk

**Risk level:** `moderate`  
**Requires approval before implementation:** `false`  
**Approval owner:** `platform`

**Safe remediation without approval:**

- Document current probe paths and validate health-group contributor identifiers.
- Add tests that demonstrate the current behavior and the failure mode.

**Requires approval for:**

- Changing probe paths, ports, or authentication requirements.

---

### GLB-018: Readiness transitions and traffic eligibility are observable

**Severity:** Medium  
**Category:** observability

#### Requirement

The application code and configuration must satisfy this behavior when the same artifact runs in either active region.

#### Repository evidence to inspect

- `readiness metric`
- `AvailabilityChangeEvent`
- `state change log`
- `region tag`

#### Finding condition

Emit a finding when evidence shows that readiness changes and regional traffic eligibility cannot be observed or correlated during an incident.

#### Evidence rule

Cite the file path, symbol or property, and advisory line range when available. Evaluate effective behavior rather than the presence of a library, annotation, or property alone. If the repository does not contain enough evidence, return `not_assessed` rather than assuming noncompliance.

#### Quality caveats

- Avoid unbounded-cardinality labels in readiness telemetry.

#### Business-logic risk

**Risk level:** `none`  
**Requires approval before implementation:** `false`  
**Approval owner:** `none`

**Safe remediation without approval:**

- Add or improve metrics, logs, traces, and health details without changing decisions or payload content.
- Add tests that characterize and lock in current behavior.

---

## Standard finding format

- **Title:** [specific code-level gap]
- **Control:** [GLB-NNN]
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
