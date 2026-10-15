---
schema_version: "1.0.0"
document_type: dependency_standard
standard_id: REACT-UI
service: react-ui
service_name: React UI
language: typescript-javascript
framework: react
version: "1.0.0"
lifecycle_status: active
assessment_domain: frontend_application
assessment_scope: browser_client_code_and_repository_owned_configuration
repository_owned_only: true
infrastructure_findings_allowed: false
requires_standard: frontend-web-client
activation:
  scope_context_path: application-context/assessment-scope-context.yml
  required_status: enabled
assessment:
  enabled: true
  emit_findings: true
  include_in_score: true
  unknown_evidence_status: not_assessed
framework_version_detection:
  version_source_order:
  - package.json dependencies react
  - package-lock.json or yarn.lock resolved react
  unknown_version_behavior: not_assessed_for_version_conditional_controls
data_layer_detection:
  resolution_rule: detect_all_present_and_evaluate_each_against_its_own_patterns
  multiple_layers_behavior: evaluate_each_detected_layer_independently
  unknown_layer_behavior: not_assessed
  layers:
  - id: tanstack_query
    display_name: TanStack Query or React Query
    detect_dependencies:
    - '@tanstack/react-query'
    - react-query
    detect_patterns:
    - useQuery
    - useMutation
    - QueryClient
    - queryKey
    - invalidateQueries
  - id: rtk_query
    display_name: RTK Query
    detect_dependencies:
    - '@reduxjs/toolkit'
    detect_patterns:
    - createApi
    - fetchBaseQuery
    - endpoints:
    - useGetQuery
    - providesTags
  - id: raw_fetch
    display_name: Raw fetch in effects or handlers
    detect_dependencies: []
    detect_patterns:
    - fetch(
    - useEffect
    - AbortController
    - .then(
    - async function
  - id: http_client
    display_name: Axios or custom HTTP client
    detect_dependencies:
    - axios
    - ky
    - superagent
    - swr
    detect_patterns:
    - axios.create
    - interceptors.request
    - interceptors.response
    - CancelToken
    - apiClient
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
- id: REACT-001
  title: Effects cancel in-flight work on unmount and dependency change
  severity: critical
  category: concurrency
  applies_when: a component starts asynchronous work from an effect or handler
  evidence_patterns:
  - useEffect
  - AbortController
  - return () =>
  - signal
  - isMounted
  evidence_patterns_by_data_layer:
    tanstack_query: [useQuery, signal, queryFn, AbortSignal]
    rtk_query: [queryFn, signal, baseQuery]
    raw_fetch: [useEffect, AbortController, 'return () =>', setState]
    http_client: [axios, AbortController, CancelToken, interceptors.request]
  finding_when: asynchronous work started by a component is not cancelled when the
    component unmounts or its dependencies change, so a stale response can overwrite
    newer state or update a destroyed component
  emit_on_failure: true
- id: REACT-002
  title: Data fetching carries a bounded deadline
  severity: critical
  category: timeout
  applies_when: the application issues outbound data requests
  evidence_patterns:
  - AbortSignal.timeout
  - setTimeout
  - timeout
  - signal
  - abort(
  evidence_patterns_by_data_layer:
    tanstack_query: [queryFn, AbortSignal.timeout, networkMode]
    rtk_query: [fetchBaseQuery, timeout, prepareHeaders]
    raw_fetch: ['fetch(', AbortSignal.timeout, setTimeout, 'controller.abort(']
    http_client: [axios.create, timeout, AbortSignal.timeout]
  finding_when: an outbound request has no bounded deadline, or a sequence of requests
    backing one user action has no shared end-to-end budget
  emit_on_failure: true
- id: REACT-003
  title: Query and mutation retry is bounded and classified
  severity: critical
  category: retry
  applies_when: the application retries failed data operations
  evidence_patterns:
  - retry
  - retryDelay
  - attempts
  - backoff
  - status
  evidence_patterns_by_data_layer:
    tanstack_query: [retry, retryDelay, defaultOptions, QueryClient, mutations]
    rtk_query: [retry, maxRetries, retryCondition, baseQuery]
    raw_fetch: [for, while, 'retry(', setTimeout]
    http_client: [axios-retry, interceptors.response, retryCondition, backoff]
  finding_when: retry is unbounded, applies to non-transient failures such as 4xx or
    validation errors, omits backoff or jitter, or is enabled by default on non-idempotent
    mutations
  emit_on_failure: true
- id: REACT-004
  title: Mutations are guarded and optimistic updates roll back
  severity: critical
  category: data-correctness
  applies_when: the application performs a non-idempotent mutation or applies an optimistic
    update
  evidence_patterns:
  - onSubmit
  - disabled
  - isPending
  - onMutate
  - rollback
  evidence_patterns_by_data_layer:
    tanstack_query: [useMutation, onMutate, onError, setQueryData, isPending]
    rtk_query: [useMutation, onQueryStarted, updateQueryData, undo]
    raw_fetch: [onSubmit, isSubmitting, disabled, setState]
    http_client: [onSubmit, isSubmitting, apiClient, 'Idempotency-Key']
  finding_when: a mutation can be issued concurrently or repeated for one user intent,
    an optimistic update has no rollback on failure, or a rollback leaves client state
    inconsistent with an unknown server outcome
  emit_on_failure: true
- id: REACT-005
  title: Unknown outcomes are preserved in component state
  severity: critical
  category: data-correctness-and-reconciliation
  applies_when: the application derives a business outcome from a request result
  evidence_patterns:
  - catch
  - AbortError
  - TimeoutError
  - isError
  - status
  evidence_patterns_by_data_layer:
    tanstack_query: [isError, error, status, failureReason]
    rtk_query: [isError, error, isUninitialized, status]
    raw_fetch: [catch, AbortError, 'response.ok', setState]
    http_client: [catch, isAxiosError, 'error.response', 'error.code']
  finding_when: a timeout, abort, network failure, or 5xx response is rendered or stored
    as definitive success or failure, or an unresolved outcome has no status-lookup
    or recovery path
  emit_on_failure: true
- id: REACT-006
  title: Error boundaries contain render failures
  severity: critical
  category: failure-containment
  applies_when: the application renders routed or composed component trees
  evidence_patterns:
  - ErrorBoundary
  - componentDidCatch
  - getDerivedStateFromError
  - errorElement
  - react-error-boundary
  finding_when: no error boundary exists above a routed view so one render throw blanks
    the application, a boundary swallows the error without reporting, or a boundary
    provides no recovery path
  emit_on_failure: true
- id: REACT-007
  title: Loading and suspended states are bounded
  severity: high
  category: degradation
  applies_when: the application defers rendering on asynchronous data or lazy components
  evidence_patterns:
  - Suspense
  - fallback
  - isLoading
  - isPending
  - lazy(
  finding_when: a suspended or loading state has no bounded exit on failure or timeout,
    a lazy component failure leaves a permanent fallback, or a single slow dependency
    suspends the primary flow
  emit_on_failure: true
- id: REACT-008
  title: State updates avoid stale closures and race conditions
  severity: high
  category: consistency
  applies_when: the application updates state from asynchronous callbacks
  evidence_patterns:
  - useState
  - setState
  - useRef
  - useCallback
  - dependency array
  finding_when: an asynchronous callback captures stale state, concurrent responses
    resolve out of order and overwrite newer state, or an incomplete dependency array
    causes missed or duplicated requests
  emit_on_failure: true
- id: REACT-009
  title: Authentication refresh is sequenced and deduplicated
  severity: high
  category: authentication
  applies_when: the application attaches or refreshes credentials on outbound requests
  evidence_patterns:
  - '401'
  - refresh
  - acquireTokenSilent
  - interceptor
  - Authorization
  evidence_patterns_by_data_layer:
    tanstack_query: [queryFn, QueryClient, onError, '401']
    rtk_query: [baseQuery, fetchBaseQuery, prepareHeaders, reauth]
    raw_fetch: ['fetch(', Authorization, '401', refresh]
    http_client: [interceptors.response, '401', refresh, Authorization]
  finding_when: concurrent requests trigger a refresh stampede, a retried request is
    sent without the refreshed credential, or refresh failure produces an indefinite
    loop or unrecoverable blank state
  emit_on_failure: true
- id: REACT-010
  title: Application availability telemetry reflects real usability
  severity: high
  category: health
  applies_when: the application is operated as a production user-facing workload
  evidence_patterns:
  - trackException
  - ApplicationInsights
  - onError
  - unhandledrejection
  - traceparent
  finding_when: boundary-caught errors, failed queries or mutations, and stuck loading
    states produce no operator-visible signal, telemetry reports the application healthy
    while users cannot complete the primary flow, or client telemetry cannot be correlated
    to backend traces
  emit_on_failure: true
- id: REACT-011
  title: Endpoints and environment configuration resolve at runtime
  severity: critical
  category: configuration
  applies_when: the application targets a backend endpoint, region, or environment-specific
    service
  evidence_patterns:
  - process.env.REACT_APP_
  - import.meta.env
  - NEXT_PUBLIC_
  - runtime config
  - window.__CONFIG__
  finding_when: a regional or environment endpoint is inlined into the built bundle
    so the artifact cannot be promoted unchanged across regions, or a required endpoint
    can be omitted and silently default to a region
  emit_on_failure: true
- id: REACT-012
  title: Tests cover failure, cancellation, retry, and recovery
  severity: critical
  category: testing
  applies_when: the repository contains React unit, component, or end-to-end tests
  evidence_patterns:
  - msw
  - Testing Library
  - waitFor
  - mockRejectedValue
  - Playwright
  finding_when: tests do not prove timeout, unmount cancellation, retry exhaustion,
    error-boundary containment, duplicate submission, and session-expiry behavior on
    the actual data layer in use
  emit_on_failure: true
---

# React UI Application Behavior Standard

### Shared-service scope for concrete frontend dependencies

Resolve each concrete upstream service the client calls through the registry and apply `architecture_context.shared_service_assessment_scope.services`. Evaluate service-specific behavior only when that concrete service is `in_scope`. Application-owned React defects not attributable to an excluded service may still be evaluated under the application or cross-cutting scope.

## Purpose

Evaluate repository-owned React code for cancellation-safe effects, bounded data operations, contained render failures, and safe mutation semantics. This standard assumes the framework-agnostic `FRONTEND-WEB-CLIENT` baseline is also loaded and does not restate its controls.

## Activation

This standard is evaluated only when `frontend_application` is `enabled` in the active assessment scope and React is confirmed through repository evidence. When the domain is `disabled`, every control is `not_applicable`.

## Data-layer applicability

Controls in this standard apply regardless of how the application fetches data. The **evidence patterns** differ by data layer, not the control.

Resolve the data layer or layers in use with `data_layer_detection`, then evaluate each detected layer against its own patterns:

| Layer | Detected by | Evaluate |
|---|---|---|
| TanStack Query or React Query | `@tanstack/react-query`, `react-query`, `useQuery`, `QueryClient` | Default and per-call `retry`, `retryDelay`, `queryFn` signal wiring, mutation guards, `onMutate` rollback |
| RTK Query | `@reduxjs/toolkit` with `createApi`, `fetchBaseQuery` | `baseQuery` timeout and reauth wrapping, `retry` and `maxRetries`, `onQueryStarted` optimistic updates |
| Raw fetch | `fetch(` inside `useEffect` or handlers | `AbortController` creation and cleanup, manual retry loops, `response.ok` handling, state writes after await |
| Axios or custom client | `axios`, `ky`, `superagent`, `swr`, shared `apiClient` | Instance `timeout`, request and response interceptors, cancellation, retry middleware |

Rules:

- A repository may use more than one layer. Detect all present and evaluate each independently; do not let one compliant layer suppress a finding in another.
- When no recognized layer is detected but outbound calls exist, evaluate under `raw_fetch` patterns and record the detection basis.
- When the layer cannot be established, mark layer-dependent controls `not_assessed` and record an evidence gap.
- Record the detected layer in every finding produced by a layer-dependent control.
- Illustrative remediation must target the detected layer. Do not propose `QueryClient` defaults for a repository that uses only Axios.

## Library default caveats

Library defaults are frequently the defect. Evaluate the effective configuration:

- TanStack Query retries failed queries three times by default. On a non-idempotent mutation or a 4xx response this default is noncompliant under `REACT-003`.
- `fetch` has no timeout. Absence of `AbortSignal.timeout` or an equivalent is meaningful evidence under `REACT-002`.
- Axios has no default timeout. `timeout: 0` means no limit.
- RTK Query caches and deduplicates by default, which can mask a dependency failure from the user under `REACT-005`.

## Controls

### REACT-001: Effects cancel in-flight work on unmount and dependency change

**Severity:** Critical  
**Category:** concurrency  
**Applies when:** A component starts asynchronous work from an effect or handler.

**Requirement:** Asynchronous work owned by a component must be cancelled when the component unmounts or its dependencies change.

**Evidence to inspect:** `useEffect` cleanup returns, `AbortController` creation and `signal` wiring, `isMounted` guards, state writes after `await`, query function signal forwarding.  
**Finding condition:** Emit a finding when asynchronous work started by a component is not cancelled when the component unmounts or its dependencies change, so a stale response can overwrite newer state or update a destroyed component.

**Quality caveats:** An `isMounted` flag suppresses the warning but does not cancel the request. It is not equivalent to an `AbortController`.

### REACT-002: Data fetching carries a bounded deadline

**Severity:** Critical  
**Category:** timeout  
**Applies when:** The application issues outbound data requests.

**Requirement:** Every outbound request must have a bounded deadline, and a sequence backing one user action must share an end-to-end budget.

**Evidence to inspect:** `AbortSignal.timeout`, manual `setTimeout` plus `abort()`, client instance `timeout` options, base query configuration, chained request sequences.  
**Finding condition:** Emit a finding when an outbound request has no bounded deadline, or when a sequence of requests backing one user action has no shared end-to-end budget.

### REACT-003: Query and mutation retry is bounded and classified

**Severity:** Critical  
**Category:** retry  
**Applies when:** The application retries failed data operations.

**Requirement:** Retry must be bounded, delayed, limited to transient failures, and disabled by default on non-idempotent mutations.

**Evidence to inspect:** Client default options, per-call retry configuration, retry predicates against status, backoff and jitter, retry middleware, manual retry loops.  
**Finding condition:** Emit a finding when retry is unbounded, applies to non-transient failures such as 4xx or validation errors, omits backoff or jitter, or is enabled by default on non-idempotent mutations.

### REACT-004: Mutations are guarded and optimistic updates roll back

**Severity:** Critical  
**Category:** data-correctness  
**Applies when:** The application performs a non-idempotent mutation or applies an optimistic update.

**Requirement:** One user intent must produce exactly one business effect, and optimistic state must reconcile with the real outcome.

**Evidence to inspect:** Submit handler guards, pending-state disabling, optimistic update application and rollback, cache invalidation after mutation, idempotency identity on the request.  
**Finding condition:** Emit a finding when a mutation can be issued concurrently or repeated for one user intent, when an optimistic update has no rollback on failure, or when a rollback leaves client state inconsistent with an unknown server outcome.

**Quality caveats:** Rolling back an optimistic update on a timeout asserts the operation failed. When the outcome is unknown, this is a correctness defect; pair with `REACT-005`.

### REACT-005: Unknown outcomes are preserved in component state

**Severity:** Critical  
**Category:** data-correctness-and-reconciliation  
**Applies when:** The application derives a business outcome from a request result.

**Requirement:** Component state must distinguish pending, succeeded, failed, and unknown outcomes.

**Evidence to inspect:** Catch blocks, `AbortError` and `TimeoutError` discrimination, error and status flags, rendering of error state, reconciliation or polling paths.  
**Finding condition:** Emit a finding when a timeout, abort, network failure, or 5xx response is rendered or stored as definitive success or failure, or when an unresolved outcome has no status-lookup or recovery path.

### REACT-006: Error boundaries contain render failures

**Severity:** Critical  
**Category:** failure-containment  
**Applies when:** The application renders routed or composed component trees.

**Requirement:** A render failure must be contained, reported, and recoverable without destroying the application.

**Evidence to inspect:** Error boundary components, `componentDidCatch`, `getDerivedStateFromError`, router `errorElement`, boundary placement relative to routes, reset and recovery affordances.  
**Finding condition:** Emit a finding when no error boundary exists above a routed view so one render throw blanks the application, when a boundary swallows the error without reporting, or when a boundary provides no recovery path.

**Quality caveats:** Error boundaries do not catch errors in event handlers, asynchronous callbacks, or effects. A boundary alone does not satisfy `FE-006`.

### REACT-007: Loading and suspended states are bounded

**Severity:** High  
**Category:** degradation  
**Applies when:** The application defers rendering on asynchronous data or lazy components.

**Requirement:** Every deferred state must have a bounded exit on failure or timeout.

**Evidence to inspect:** `Suspense` boundaries and fallbacks, loading and pending flags, lazy component imports, chunk load failure handling, scope of suspension relative to the primary flow.  
**Finding condition:** Emit a finding when a suspended or loading state has no bounded exit on failure or timeout, when a lazy component failure leaves a permanent fallback, or when a single slow dependency suspends the primary flow.

### REACT-008: State updates avoid stale closures and race conditions

**Severity:** High  
**Category:** consistency  
**Applies when:** The application updates state from asynchronous callbacks.

**Requirement:** Asynchronous state updates must reflect current values and resolve deterministically under concurrency.

**Evidence to inspect:** `useState` updater usage, captured values in asynchronous callbacks, `useRef` for current values, dependency arrays, ordering guards on concurrent responses.  
**Finding condition:** Emit a finding when an asynchronous callback captures stale state, when concurrent responses resolve out of order and overwrite newer state, or when an incomplete dependency array causes missed or duplicated requests.

### REACT-009: Authentication refresh is sequenced and deduplicated

**Severity:** High  
**Category:** authentication  
**Applies when:** The application attaches or refreshes credentials on outbound requests.

**Requirement:** Refresh must be deduplicated across concurrent requests and must reattach the refreshed credential to the retried request.

**Evidence to inspect:** 401 handling location, refresh promise sharing, interceptor or base-query reauth wrapping, retry placement relative to refresh, login redirect behavior.  
**Finding condition:** Emit a finding when concurrent requests trigger a refresh stampede, when a retried request is sent without the refreshed credential, or when refresh failure produces an indefinite loop or unrecoverable blank state.

### REACT-010: Application availability telemetry reflects real usability

**Severity:** High  
**Category:** health  
**Applies when:** The application is operated as a production user-facing workload.

**Requirement:** Operators must be able to determine whether real users can complete the primary flow.

**Evidence to inspect:** Telemetry SDK initialization, error boundary reporting callbacks, query and mutation error handlers, global `unhandledrejection` wiring, correlation header propagation, sampling and redaction.  
**Finding condition:** Emit a finding when boundary-caught errors, failed queries or mutations, and stuck loading states produce no operator-visible signal, when telemetry reports the application healthy while users cannot complete the primary flow, or when client telemetry cannot be correlated to backend traces.

**Quality caveats:** A browser client has no probe contract. Do not emit a finding because no readiness or liveness endpoint exists. Deduplicate with `FE-007` under one root cause.

### REACT-011: Endpoints and environment configuration resolve at runtime

**Severity:** Critical  
**Category:** configuration  
**Applies when:** The application targets a backend endpoint, region, or environment-specific service.

**Requirement:** One built artifact must be promotable across every approved region and environment.

**Evidence to inspect:** Build-time environment variable usage for endpoints, runtime configuration fetch or injected global, defaults for required endpoints, deployment substitution mechanism, build pipeline environment injection.  
**Finding condition:** Emit a finding when a regional or environment endpoint is inlined into the built bundle so the artifact cannot be promoted unchanged across regions, or when a required endpoint can be omitted and silently default to a region.

**Quality caveats:** `process.env.REACT_APP_*`, `import.meta.env.*`, and `NEXT_PUBLIC_*` are substituted at build time. Using them for feature flags is acceptable; using them for regional endpoints is the defect. Deduplicate with `FE-009` and `CICD-002`.

### REACT-012: Tests cover failure, cancellation, retry, and recovery

**Severity:** Critical  
**Category:** testing  
**Applies when:** The repository contains React unit, component, or end-to-end tests.

**Requirement:** Tests must exercise failure behavior against the data layer actually in use.

**Evidence to inspect:** Request mocking setup, rejected and delayed response tests, unmount-during-request tests, error boundary tests, duplicate submission tests, end-to-end failure scenarios.  
**Finding condition:** Emit a finding when tests do not prove timeout, unmount cancellation, retry exhaustion, error-boundary containment, duplicate submission, and session-expiry behavior on the actual data layer in use.

## Evidence and finding rules

- Use the control `severity` and `category` declared in frontmatter; do not reassign severity per finding.
- Record the detected data layer and the evidence that established it in every finding produced by a layer-dependent control.
- Record the detected React version when a finding depends on version-specific behavior.
- Return `not_assessed` when the data layer or required evidence cannot be established.
- Evaluate effective configuration rather than the presence of a library or hook alone.
- Deduplicate with `FRONTEND-WEB-CLIENT` under one root cause; attribute the finding here when the defect is expressed in React or data-layer API usage.

## Finding classification

Resiliency classification follows `grounding/governance/resiliency-finding-qualification-policy.yml`. Uncancelled effects, unbounded retries on mutations, unrolled-back optimistic updates, and uncontained render failures qualify as `resiliency`. Style, naming, and presentational defects are `non_resiliency`.

## Non-findings

- Choice of data layer, state library, or router where the required behavior is present.
- Absence of a readiness or liveness probe in a browser client.
- React version upgrades proposed without an evidenced control violation.
- Deployed CDN, hosting, and gateway configuration.
- Server-side rendering behavior, which is evaluated by `FRONTEND-SSR-SERVER` only when SSR is detected.
