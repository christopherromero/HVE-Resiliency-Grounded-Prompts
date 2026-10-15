---
schema_version: "1.0.0"
document_type: dependency_standard
standard_id: FRONTEND-WEB-CLIENT
service: frontend-web-client
service_name: Frontend Web Client Behavior
language: typescript-javascript
framework: framework-agnostic
version: "1.0.0"
lifecycle_status: active
assessment_domain: frontend_application
assessment_scope: browser_client_code_and_repository_owned_configuration
repository_owned_only: true
infrastructure_findings_allowed: false
activation:
  scope_context_path: application-context/assessment-scope-context.yml
  required_status: enabled
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
  contract_section: Shared-service scope for concrete frontend dependencies
controls:
- id: FE-001
  title: Outbound calls carry a timeout and cancellation budget
  severity: critical
  category: timeout
  applies_when: the client issues HTTP, GraphQL, WebSocket, or SDK calls to a backend
  evidence_patterns:
  - AbortController
  - AbortSignal.timeout
  - signal
  - timeout
  - XMLHttpRequest.timeout
  finding_when: an outbound call has no bounded deadline, cannot be cancelled, or a
    sequence of calls backing one user action has no shared end-to-end budget
  emit_on_failure: true
- id: FE-002
  title: Retry is classified, bounded, and jittered
  severity: critical
  category: retry
  applies_when: the client retries failed outbound calls
  evidence_patterns:
  - retry
  - attempts
  - backoff
  - jitter
  - Retry-After
  finding_when: retries are unbounded or unclassified, retry non-transient failures,
    omit backoff or jitter, ignore Retry-After, or allow concurrent user-triggered
    retries to amplify load on a degraded backend
  emit_on_failure: true
- id: FE-003
  title: Non-idempotent submissions are protected against double execution
  severity: critical
  category: data-correctness
  applies_when: the client submits an order, payment, enrollment, or other non-idempotent
    business operation
  evidence_patterns:
  - onSubmit
  - disabled
  - isSubmitting
  - Idempotency-Key
  - correlationId
  finding_when: a submit control permits repeat invocation while a request is in flight,
    a retry or navigation can resubmit the operation, or the request carries no stable
    idempotency identity across attempts
  emit_on_failure: true
- id: FE-004
  title: Unknown outcomes are preserved in client state
  severity: critical
  category: data-correctness-and-reconciliation
  applies_when: the client determines a business operation's result from a response,
    poll, callback, or locally persisted state
  evidence_patterns:
  - catch
  - TimeoutError
  - AbortError
  - status
  - unknown
  finding_when: a timeout, abort, network failure, or 5xx response is presented to
    the user or stored as definitive success or failure, or an unresolved outcome has
    no status-lookup, reconciliation, or recovery path
  emit_on_failure: true
- id: FE-005
  title: Partial failure degrades a region of the UI, not the page
  severity: high
  category: degradation
  applies_when: a view composes data from more than one backend call or widget
  evidence_patterns:
  - Promise.all
  - Promise.allSettled
  - loading state
  - fallback
  - skeleton
  finding_when: one non-critical dependency failure blanks the page, blocks the primary
    flow, or leaves an indefinite loading state with no bounded fallback
  emit_on_failure: true
- id: FE-006
  title: Unhandled errors are contained and reported
  severity: critical
  category: failure-containment
  applies_when: the application renders any interactive view
  evidence_patterns:
  - window.onerror
  - unhandledrejection
  - ErrorHandler
  - ErrorBoundary
  - global error
  finding_when: an unhandled render or promise rejection can leave the application
    in an unusable state, or escapes without being captured, bounded, and reported
  emit_on_failure: true
- id: FE-007
  title: Client availability and failure telemetry reflect real usability
  severity: high
  category: health
  applies_when: the application is operated as a production user-facing workload
  evidence_patterns:
  - ApplicationInsights
  - trackException
  - trackPageView
  - traceparent
  - correlationId
  finding_when: telemetry reports the application healthy while users cannot complete
    the primary flow, client errors and failed API calls are not captured with correlation
    identity, a failed critical dependency produces no user-visible or operator-visible
    signal, or telemetry carries personal data or unbounded cardinality
  emit_on_failure: true
- id: FE-008
  title: Session expiry and token refresh are sequenced
  severity: high
  category: authentication
  applies_when: the client holds a token, cookie, or session that can expire
  evidence_patterns:
  - 401
  - refresh token
  - acquireTokenSilent
  - interceptor
  - redirect to login
  finding_when: concurrent requests trigger a refresh stampede, an expired session
    silently discards in-flight user work, or a refresh failure produces an indefinite
    loop or an unrecoverable blank state
  emit_on_failure: true
- id: FE-009
  title: Regional endpoints resolve at runtime, not at build time
  severity: critical
  category: configuration
  applies_when: the client targets a backend endpoint, region, or environment-specific
    service
  evidence_patterns:
  - process.env
  - import.meta.env
  - environment.ts
  - runtime config
  - /config endpoint
  finding_when: a regional or environment endpoint is inlined into the built bundle
    so the artifact cannot be promoted unchanged across regions, or a required endpoint
    can be omitted and silently default to a region
  emit_on_failure: true
- id: FE-010
  title: Connectivity loss and recovery are handled explicitly
  severity: medium
  category: resilience
  applies_when: the application is used on unreliable networks or supports long-lived
    sessions
  evidence_patterns:
  - navigator.onLine
  - online
  - offline
  - reconnect
  - visibilitychange
  finding_when: connectivity loss produces silent failure or permanent broken state,
    or reconnection replays non-idempotent work without duplicate protection
  emit_on_failure: true
- id: FE-011
  title: Cached and stale data have explicit boundaries
  severity: high
  category: data-freshness
  applies_when: the client caches responses in memory, storage, or a service worker
  evidence_patterns:
  - localStorage
  - sessionStorage
  - staleTime
  - cacheTime
  - service worker
  finding_when: safety-critical or financially significant data is served from cache
    with no freshness bound or invalidation, or cached state survives logout, user
    switch, or regional failover
  emit_on_failure: true
- id: FE-012
  title: Secrets and personal data stay out of the bundle and web storage
  severity: critical
  category: security-material
  applies_when: the client handles credentials, tokens, keys, or personal data
  evidence_patterns:
  - apiKey
  - clientSecret
  - connectionString
  - localStorage
  - console.log
  finding_when: secret material is embedded in source or the built bundle, a token
    is persisted to a storage mechanism inconsistent with the approved auth design,
    or personal data is written to logs or telemetry
  emit_on_failure: true
- id: FE-013
  title: Asset and chunk load failures are recoverable
  severity: medium
  category: delivery
  applies_when: the application uses code splitting, lazy routes, or externally hosted
    assets
  evidence_patterns:
  - import(
  - lazy
  - ChunkLoadError
  - crossorigin
  - integrity
  finding_when: a failed lazy chunk or asset request leaves the application permanently
    broken for an active session, or a deployment that replaces hashed assets produces
    no recovery path for already-loaded clients
  emit_on_failure: true
- id: FE-014
  title: Tests cover failure, cancellation, retry, and recovery
  severity: high
  category: testing
  applies_when: the repository contains automated frontend tests or a test harness
  evidence_patterns:
  - msw
  - mock server
  - fetch mock
  - Playwright
  - Cypress
  finding_when: tests do not prove timeout, cancellation, retry exhaustion, duplicate
    submission, partial failure, and session-expiry behavior on the actual client code
    path
  emit_on_failure: true
---

# Frontend Web Client Behavior Standard

### Shared-service scope for concrete frontend dependencies

`frontend-web-client` is a cross-cutting client standard, not a declaration that every upstream service is in scope. For each concrete upstream service the client calls, resolve its canonical service key through the registry and apply `architecture_context.shared_service_assessment_scope.services`. Evaluate service-specific behavior only when that concrete service is `in_scope`; otherwise preserve only the behavior allowed by its scope. Application-owned client defects not attributable to an excluded service may still be evaluated under the application or cross-cutting scope.

## Purpose

Evaluate repository-owned browser client code and configuration for bounded outbound calls, safe submission semantics, contained failure, honest availability signaling, and region-portable configuration. This standard is framework-agnostic. Framework-specific behavior is evaluated by `ANGULAR-RXJS` or `REACT-UI`, and server-side rendering is evaluated by `FRONTEND-SSR-SERVER` only when SSR is detected.

## Activation

This standard is evaluated only when `frontend_application` is `enabled` in the active assessment scope. When the domain is `disabled`, every control is `not_applicable`. When the domain is `inventory_only`, inventory and preserve evidence but emit no findings.

## Evidence boundary

Generate findings only from repository-owned client source, configuration, and build definitions. CDN behavior, WAF rules, gateway routing, browser versions, and deployed hosting configuration are external evidence unless the repository owns the definition and the relevant domain is in scope.

## Health interpretation

A browser client has no readiness or liveness probe. The health equivalent assessed by `FE-007` is whether the operator can tell that real users can complete the primary flow. Do not map `FE-007` onto a Kubernetes probe contract, and do not emit a finding because no probe exists.

## Controls

### FE-001: Outbound calls carry a timeout and cancellation budget

**Severity:** Critical  
**Category:** timeout  
**Applies when:** The client issues HTTP, GraphQL, WebSocket, or SDK calls to a backend.

**Requirement:** Every outbound call must have a bounded deadline and a cancellation path. A sequence of calls backing one user action must share an end-to-end budget.

**Evidence to inspect:** `AbortController`, `AbortSignal.timeout`, request `signal` wiring, client timeout options, `XMLHttpRequest.timeout`, framework HTTP configuration.  
**Finding condition:** Emit a finding when an outbound call has no bounded deadline, cannot be cancelled, or when a sequence of calls backing one user action has no shared end-to-end budget.

**Quality caveats:** Browser default timeouts are not a bounded deadline. A spinner is not a timeout.

### FE-002: Retry is classified, bounded, and jittered

**Severity:** Critical  
**Category:** retry  
**Applies when:** The client retries failed outbound calls.

**Requirement:** Retry transient failures only, cap attempts and total duration, apply backoff with jitter, and honor `Retry-After` when the contract defines it.

**Evidence to inspect:** Retry helpers and library options, attempt counts, backoff and jitter configuration, `Retry-After` handling, user-triggered retry controls.  
**Finding condition:** Emit a finding when retries are unbounded or unclassified, retry non-transient failures, omit backoff or jitter, ignore `Retry-After`, or when concurrent user-triggered retries can amplify load on a degraded backend.

**Quality caveats:** Many client data libraries retry by default on all errors. Evaluate the effective configuration, not the presence of a retry option.

### FE-003: Non-idempotent submissions are protected against double execution

**Severity:** Critical  
**Category:** data-correctness  
**Applies when:** The client submits an order, payment, enrollment, or other non-idempotent business operation.

**Requirement:** A non-idempotent submission must execute once per user intent. Repeat invocation, retry, and navigation must not duplicate the business effect.

**Evidence to inspect:** Submit handlers, control disabled state, in-flight guards, `Idempotency-Key` or stable business identity on the request, navigation and route-change behavior during submission.  
**Finding condition:** Emit a finding when a submit control permits repeat invocation while a request is in flight, when a retry or navigation can resubmit the operation, or when the request carries no stable idempotency identity across attempts.

**Quality caveats:** A newly generated UUID per attempt is correlation, not idempotency. Client-side guarding alone is not sufficient when the backend contract provides no idempotency key.

### FE-004: Unknown outcomes are preserved in client state

**Severity:** Critical  
**Category:** data-correctness-and-reconciliation  
**Applies when:** The client determines a business operation's result from a response, poll, callback, or locally persisted state.

**Requirement:** Client state must distinguish pending, succeeded, failed, and unknown outcomes. An unresolved outcome must remain recoverable.

**Evidence to inspect:** Catch blocks, `TimeoutError` and `AbortError` handling, status mapping, outcome state models, polling and reconciliation paths.  
**Finding condition:** Emit a finding when a timeout, abort, network failure, or 5xx response is presented to the user or stored as definitive success or failure, or when an unresolved outcome has no status-lookup, reconciliation, or recovery path.

**Quality caveats:** Telling a user an order failed when the outcome is unknown is a correctness defect, not a cosmetic one. This control mirrors `HTTP-011` and `HTTP-012` on the client side.

### FE-005: Partial failure degrades a region of the UI, not the page

**Severity:** High  
**Category:** degradation  
**Applies when:** A view composes data from more than one backend call or widget.

**Requirement:** Non-critical dependency failure must degrade locally while the primary flow remains usable.

**Evidence to inspect:** `Promise.all` versus `Promise.allSettled`, per-widget loading and error state, fallback content, skeleton and placeholder handling, route-level data requirements.  
**Finding condition:** Emit a finding when one non-critical dependency failure blanks the page, blocks the primary flow, or leaves an indefinite loading state with no bounded fallback.

### FE-006: Unhandled errors are contained and reported

**Severity:** Critical  
**Category:** failure-containment  
**Applies when:** The application renders any interactive view.

**Requirement:** Unhandled render errors and promise rejections must be contained, reported, and recoverable.

**Evidence to inspect:** `window.onerror`, `unhandledrejection` listeners, framework global error handling, boundary placement relative to routes, recovery affordances.  
**Finding condition:** Emit a finding when an unhandled render or promise rejection can leave the application in an unusable state, or escapes without being captured, bounded, and reported.

### FE-007: Client availability and failure telemetry reflect real usability

**Severity:** High  
**Category:** health  
**Applies when:** The application is operated as a production user-facing workload.

**Requirement:** Operators must be able to determine whether real users can complete the primary flow. Client errors, failed dependencies, and stuck states must be observable and correlatable to backend traces.

**Evidence to inspect:** Telemetry SDK initialization, `trackException` and equivalent calls, page and route instrumentation, correlation header propagation such as `traceparent`, dependency failure reporting, sampling and redaction configuration.  
**Finding condition:** Emit a finding when telemetry reports the application healthy while users cannot complete the primary flow, when client errors and failed API calls are not captured with correlation identity, when a failed critical dependency produces no user-visible or operator-visible signal, or when telemetry carries personal data or unbounded cardinality.

**Quality caveats:** A browser client has no probe contract. Do not emit a finding because no readiness or liveness endpoint exists. Successful asset delivery is not proof that the application is usable.

### FE-008: Session expiry and token refresh are sequenced

**Severity:** High  
**Category:** authentication  
**Applies when:** The client holds a token, cookie, or session that can expire.

**Requirement:** Expiry and refresh must be sequenced, deduplicated, and must not discard in-flight user work without recovery.

**Evidence to inspect:** 401 handling, refresh token flows, silent token acquisition, interceptor or middleware ordering, login redirect behavior, in-flight request queuing.  
**Finding condition:** Emit a finding when concurrent requests trigger a refresh stampede, when an expired session silently discards in-flight user work, or when a refresh failure produces an indefinite loop or an unrecoverable blank state.

### FE-009: Regional endpoints resolve at runtime, not at build time

**Severity:** Critical  
**Category:** configuration  
**Applies when:** The client targets a backend endpoint, region, or environment-specific service.

**Requirement:** One built artifact must be promotable across every approved region and environment. Regional identity must resolve at runtime.

**Evidence to inspect:** Build-time environment substitution, environment files, runtime configuration fetch or injected configuration element, defaults for required endpoints, deployment substitution mechanism.  
**Finding condition:** Emit a finding when a regional or environment endpoint is inlined into the built bundle so the artifact cannot be promoted unchanged across regions, or when a required endpoint can be omitted and silently default to a region.

**Quality caveats:** This control is the client-side equivalent of `APP-AA-001` and `APP-AA-002`. Deduplicate with `CICD-002` when the same root cause is already recorded as an artifact-promotion defect.

### FE-010: Connectivity loss and recovery are handled explicitly

**Severity:** Medium  
**Category:** resilience  
**Applies when:** The application is used on unreliable networks or supports long-lived sessions.

**Requirement:** Connectivity transitions must produce explicit, recoverable behavior.

**Evidence to inspect:** `navigator.onLine`, online and offline listeners, reconnect logic for sockets and streams, `visibilitychange` resume behavior, queued work.  
**Finding condition:** Emit a finding when connectivity loss produces silent failure or permanent broken state, or when reconnection replays non-idempotent work without duplicate protection.

### FE-011: Cached and stale data have explicit boundaries

**Severity:** High  
**Category:** data-freshness  
**Applies when:** The client caches responses in memory, storage, or a service worker.

**Requirement:** Cached data must have explicit freshness bounds, invalidation, and lifecycle tied to identity and region.

**Evidence to inspect:** Web storage usage, client cache configuration such as stale and cache durations, service worker caching strategy, logout and user-switch clearing, failover behavior.  
**Finding condition:** Emit a finding when safety-critical or financially significant data is served from cache with no freshness bound or invalidation, or when cached state survives logout, user switch, or regional failover.

### FE-012: Secrets and personal data stay out of the bundle and web storage

**Severity:** Critical  
**Category:** security-material  
**Applies when:** The client handles credentials, tokens, keys, or personal data.

**Requirement:** The built bundle and browser storage must not carry secret material, and diagnostics must not carry personal data.

**Evidence to inspect:** API keys and client secrets in source or environment files, connection strings, token persistence mechanism, console and telemetry output, committed fixtures.  
**Finding condition:** Emit a finding when secret material is embedded in source or the built bundle, when a token is persisted to a storage mechanism inconsistent with the approved authentication design, or when personal data is written to logs or telemetry.

**Quality caveats:** A public client identifier is not a secret. Evaluate the approved authentication design before classifying token storage.

### FE-013: Asset and chunk load failures are recoverable

**Severity:** Medium  
**Category:** delivery  
**Applies when:** The application uses code splitting, lazy routes, or externally hosted assets.

**Requirement:** A failed asset or chunk request must be recoverable for an active session.

**Evidence to inspect:** Dynamic `import()` usage, lazy route definitions, chunk load error handling, asset integrity and crossorigin attributes, deployment asset retention.  
**Finding condition:** Emit a finding when a failed lazy chunk or asset request leaves the application permanently broken for an active session, or when a deployment that replaces hashed assets produces no recovery path for already-loaded clients.

### FE-014: Tests cover failure, cancellation, retry, and recovery

**Severity:** High  
**Category:** testing  
**Applies when:** The repository contains automated frontend tests or a test harness.

**Requirement:** Tests must exercise failure behavior on the actual client code path, not only happy-path rendering.

**Evidence to inspect:** Request mocking setup, failure and latency simulation, cancellation tests, duplicate submission tests, session-expiry tests, end-to-end harness coverage.  
**Finding condition:** Emit a finding when tests do not prove timeout, cancellation, retry exhaustion, duplicate submission, partial failure, and session-expiry behavior on the actual client code path.

## Evidence and finding rules

- Use the control `severity` and `category` declared in frontmatter; do not reassign severity per finding.
- Cite the file path, symbol or configuration key, and line range when available.
- Return `not_assessed` when the repository lacks evidence to evaluate an applicable control.
- Evaluate effective behavior rather than the presence of a library, option, or default alone.
- Deduplicate framework-specific findings with this baseline under one root cause; attribute the finding to the framework standard when the defect is expressed in framework-specific API usage.

## Finding classification

Resiliency classification follows `grounding/governance/resiliency-finding-qualification-policy.yml`. Controls in this standard that establish a credible failure scenario with material user impact qualify as `resiliency`. Accessibility, visual design, bundle-size, and lint-style defects are `non_resiliency` and are limited to the non-resiliency priorities permitted by the active report configuration.

## Non-findings

- Absence of a readiness or liveness probe in a browser client.
- CDN, WAF, gateway, DNS, and hosting configuration not owned by the repository.
- Browser version, device, and network conditions.
- Framework version upgrades without an evidenced control violation.
