---
schema_version: "1.0.0"
document_type: dependency_standard
standard_id: ANGULAR-RXJS
service: angular-rxjs
service_name: Angular and RxJS
language: typescript
framework: angular
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
  - package.json dependencies @angular/core
  - package-lock.json or yarn.lock resolved @angular/core
  - angular.json with corroborating source evidence
  rxjs_version_source_order:
  - package.json dependencies rxjs
  - package-lock.json or yarn.lock resolved rxjs
  unknown_version_behavior: not_assessed_for_version_conditional_controls
  version_range_behavior: use_lowest_supported_version_in_declared_range
version_capability_matrix:
  inject_function: angular>=14
  standalone_components: angular>=14
  functional_interceptors: angular>=15
  destroy_ref: angular>=16
  take_until_destroyed: angular>=16
  signals: angular>=16
  to_signal: angular>=16
  rxjs_retry_config_object: rxjs>=7.3
  rxjs_retry_when_deprecated: rxjs>=7
  rxjs_first_value_from: rxjs>=7
  rxjs_share_replay_config_object: rxjs>=6.4
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
- id: NG-001
  title: Subscriptions are deterministically terminated
  severity: critical
  category: memory-stability
  applies_when: component, directive, or component-scoped service code subscribes directly
    to an observable
  version_conditional: false
  remediation_capability_conditional: true
  preferred_capability: take_until_destroyed
  evidence_patterns:
  - .subscribe(
  - takeUntilDestroyed
  - takeUntil
  - ngOnDestroy
  - async pipe
  finding_when: a component-scoped subscription has no deterministic teardown path,
    so it can outlive its component and continue emitting, retaining state or issuing
    requests after destruction
  emit_on_failure: true
- id: NG-002
  title: HttpClient calls carry a bounded deadline and cancellation
  severity: critical
  category: timeout
  applies_when: the application calls HttpClient or an HttpClient-based service
  version_conditional: false
  evidence_patterns:
  - HttpClient
  - timeout(
  - takeUntil
  - switchMap
  - HttpInterceptor
  finding_when: an HttpClient call has no bounded deadline, cannot be cancelled when
    the initiating view or navigation is abandoned, or a chained sequence backing one
    user action has no shared end-to-end budget
  emit_on_failure: true
- id: NG-003
  title: RxJS retry is bounded and classified
  severity: critical
  category: retry
  applies_when: an observable chain retries a failed operation
  version_conditional: true
  required_capability: rxjs_retry_config_object
  capability_absent_behavior: evaluate_using_retry_when_equivalent
  evidence_patterns:
  - retry(
  - retryWhen
  - delayWhen
  - timer(
  - HttpErrorResponse
  finding_when: retry is unbounded, retries non-transient failures such as 4xx or validation
    errors, omits backoff or jitter, or re-subscribes to a source that repeats a non-idempotent
    effect
  emit_on_failure: true
- id: NG-004
  title: Error handling preserves failure semantics
  severity: critical
  category: error-semantics
  applies_when: an observable chain handles errors
  version_conditional: false
  evidence_patterns:
  - catchError
  - of(null)
  - EMPTY
  - throwError
  - finalize
  finding_when: an error handler converts a required-data failure into an apparent
    success such as null, an empty collection, or a silent completion, or swallows
    an error so the user and telemetry see no failure
  emit_on_failure: true
- id: NG-005
  title: Non-idempotent effects execute once per user intent
  severity: critical
  category: data-correctness
  applies_when: an observable chain triggers a non-idempotent business operation such
    as submit, payment, or enrollment
  version_conditional: false
  evidence_patterns:
  - exhaustMap
  - concatMap
  - switchMap
  - mergeMap
  - createEffect
  finding_when: a flattening operator permits a non-idempotent operation to be issued
    concurrently or re-issued on repeat emission, or cancels an in-flight mutation
    whose server-side effect may already have occurred
  emit_on_failure: true
- id: NG-006
  title: Flattening operator matches business semantics
  severity: high
  category: data-correctness
  applies_when: the application composes dependent or ordered asynchronous operations
  version_conditional: false
  evidence_patterns:
  - switchMap
  - mergeMap
  - concatMap
  - exhaustMap
  - forkJoin
  finding_when: the chosen flattening operator contradicts the required ordering, cancellation,
    or concurrency semantics of the operation, or forkJoin is used where one failure
    must not discard every result
  emit_on_failure: true
- id: NG-007
  title: Shared observables are bounded and reference-counted
  severity: high
  category: memory-stability
  applies_when: an observable is multicast for reuse across subscribers
  version_conditional: true
  required_capability: rxjs_share_replay_config_object
  capability_absent_behavior: evaluate_using_share_replay_arity_equivalent
  evidence_patterns:
  - shareReplay
  - refCount
  - publishReplay
  - ReplaySubject
  - BehaviorSubject
  finding_when: a multicast observable retains its source subscription and buffered
    values after all subscribers unsubscribe, or caches a stale or user-scoped value
    beyond its valid lifetime
  emit_on_failure: true
- id: NG-008
  title: Interceptors sequence authentication refresh correctly
  severity: high
  category: authentication
  applies_when: an interceptor attaches or refreshes credentials
  version_conditional: true
  required_capability: functional_interceptors
  capability_absent_behavior: evaluate_using_class_based_interceptor
  evidence_patterns:
  - HttpInterceptor
  - withInterceptors
  - 401
  - switchMap
  - shareReplay
  finding_when: token refresh occurs outside the intercepted chain, permits a refresh
    stampede across concurrent requests, retries the original request without the refreshed
    credential, or loses the original operation identity
  emit_on_failure: true
- id: NG-009
  title: Route guards and resolvers are bounded
  severity: high
  category: availability
  applies_when: the router uses guards or resolvers that perform asynchronous work
  version_conditional: false
  evidence_patterns:
  - CanActivate
  - canActivate
  - Resolve
  - ResolveFn
  - RouterStateSnapshot
  finding_when: a guard or resolver can block navigation indefinitely on a slow or
    failed dependency, or a resolver failure produces an unrecoverable navigation state
    with no fallback route
  emit_on_failure: true
- id: NG-010
  title: Global error handling and client health telemetry are wired
  severity: high
  category: health
  applies_when: the application is operated as a production user-facing workload
  version_conditional: false
  evidence_patterns:
  - ErrorHandler
  - handleError
  - unhandledrejection
  - trackException
  - traceparent
  finding_when: a custom ErrorHandler is absent or swallows errors without reporting,
    failed HttpClient calls and stuck resolver or guard states produce no operator-visible
    signal, or client telemetry cannot be correlated to backend traces
  emit_on_failure: true
- id: NG-011
  title: Asynchronous state integrates consistently with change detection
  severity: medium
  category: performance
  applies_when: the application renders asynchronous state in templates
  version_conditional: true
  required_capability: signals
  capability_absent_behavior: evaluate_using_zone_and_async_pipe
  evidence_patterns:
  - async pipe
  - toSignal
  - signal(
  - ChangeDetectionStrategy.OnPush
  - markForCheck
  finding_when: asynchronous state is manually assigned and rendered without a reliable
    change-detection path, a single observable is subscribed multiple times in one
    template causing duplicate requests, or OnPush components can render stale state
  emit_on_failure: true
- id: NG-012
  title: Tests cover failure, cancellation, retry, and replay
  severity: critical
  category: testing
  applies_when: the repository contains Angular unit or integration tests
  version_conditional: false
  evidence_patterns:
  - HttpTestingController
  - TestScheduler
  - marble
  - fakeAsync
  - TestBed
  finding_when: tests do not prove timeout, cancellation on destroy, retry exhaustion,
    error-path semantics, and duplicate submission behavior on the actual observable
    chains
  emit_on_failure: true
---

# Angular and RxJS Application Behavior Standard

### Shared-service scope for concrete frontend dependencies

Resolve each concrete upstream service the client calls through the registry and apply `architecture_context.shared_service_assessment_scope.services`. Evaluate service-specific behavior only when that concrete service is `in_scope`. Application-owned Angular defects not attributable to an excluded service may still be evaluated under the application or cross-cutting scope.

## Purpose

Evaluate repository-owned Angular and RxJS code for deterministic subscription lifecycle, bounded asynchronous work, honest error semantics, and safe non-idempotent operation handling. This standard assumes the framework-agnostic `FRONTEND-WEB-CLIENT` baseline is also loaded and does not restate its controls.

## Activation

This standard is evaluated only when `frontend_application` is `enabled` in the active assessment scope and Angular is confirmed through repository evidence. When the domain is `disabled`, every control is `not_applicable`.

## Angular version applicability

Controls in this standard apply across Angular versions. Version differences affect **which API satisfies a control**, not whether the control applies.

Resolve the effective Angular and RxJS versions using `framework_version_detection`, then apply `version_capability_matrix`:

| Capability | Available from | Compliant alternative on earlier versions |
|---|---|---|
| `takeUntilDestroyed`, `DestroyRef` | Angular 16 | `takeUntil` with a destroy `Subject` released in `ngOnDestroy`, or the `async` pipe |
| Signals, `toSignal` | Angular 16 | `async` pipe with `OnPush`, or explicit `markForCheck` |
| Functional interceptors, `withInterceptors` | Angular 15 | Class-based `HttpInterceptor` provided through `HTTP_INTERCEPTORS` |
| Standalone components, `inject()` | Angular 14 | `NgModule` declarations with constructor injection |
| `retry({ count, delay })` | RxJS 7.3 | `retryWhen` with an explicitly bounded and delayed notifier |
| `shareReplay({ refCount: true })` | RxJS 6.4 | `publishReplay` with `refCount()`, or an explicitly released `ReplaySubject` |

Rules:

- Do not emit a finding solely because a newer API is unused. Emit a finding when the **behavior** the control requires is absent.
- When the effective version is unknown or unresolvable, mark version-conditional controls `not_assessed` and record an evidence gap rather than assuming noncompliance.
- When `package.json` declares a range, evaluate against the lowest version the range permits unless a lockfile resolves it.
- Illustrative remediation must target the detected version. Do not propose `takeUntilDestroyed` for an Angular 14 repository.

## Controls

### NG-001: Subscriptions are deterministically terminated

**Severity:** Critical  
**Category:** memory-stability  
**Applies when:** Component, directive, or component-scoped service code subscribes directly to an observable.

**Requirement:** Every component-scoped subscription must have a deterministic teardown path tied to the owning lifecycle.

**Evidence to inspect:** Direct `.subscribe(` calls, `takeUntilDestroyed` or `DestroyRef` usage, `takeUntil` with a destroy subject, `ngOnDestroy` implementations, `async` pipe usage in templates, subscription collections.  
**Finding condition:** Emit a finding when a component-scoped subscription has no deterministic teardown path, so it can outlive its component and continue emitting, retaining state or issuing requests after destruction.

**Version guidance:** Angular 16 and later should use `takeUntilDestroyed`. Earlier versions satisfy this control with `takeUntil` plus `ngOnDestroy`, an explicit `Subscription.unsubscribe()`, or the `async` pipe. All are compliant.

**Quality caveats:** A subscription to a guaranteed single-emission source that completes is not automatically a finding. Require a path where the source can outlive the component.

### NG-002: HttpClient calls carry a bounded deadline and cancellation

**Severity:** Critical  
**Category:** timeout  
**Applies when:** The application calls `HttpClient` or an `HttpClient`-based service.

**Requirement:** Outbound calls must be bounded and cancellable when the initiating view or navigation is abandoned.

**Evidence to inspect:** `HttpClient` call sites, `timeout(` operators, `takeUntil` cancellation, `switchMap` cancellation semantics, interceptor-level timeout policy, chained request sequences.  
**Finding condition:** Emit a finding when an `HttpClient` call has no bounded deadline, cannot be cancelled when the initiating view or navigation is abandoned, or when a chained sequence backing one user action has no shared end-to-end budget.

**Quality caveats:** `HttpClient` has no default application timeout. Absence of `timeout(` is meaningful evidence.

### NG-003: RxJS retry is bounded and classified

**Severity:** Critical  
**Category:** retry  
**Applies when:** An observable chain retries a failed operation.

**Requirement:** Retry must be bounded, delayed, and limited to transient failures.

**Evidence to inspect:** `retry(` configuration, `retryWhen` notifier logic, `delayWhen` and `timer(` backoff, error classification against `HttpErrorResponse` status, retry placement relative to non-idempotent effects.  
**Finding condition:** Emit a finding when retry is unbounded, retries non-transient failures such as 4xx or validation errors, omits backoff or jitter, or re-subscribes to a source that repeats a non-idempotent effect.

**Version guidance:** RxJS 7.3 and later should use `retry({ count, delay })`. Earlier versions satisfy this control with a `retryWhen` notifier that is explicitly bounded and delayed. A bare `retry()` with no count is noncompliant on every version.

### NG-004: Error handling preserves failure semantics

**Severity:** Critical  
**Category:** error-semantics  
**Applies when:** An observable chain handles errors.

**Requirement:** Error handling must preserve the distinction between failure, empty result, and success.

**Evidence to inspect:** `catchError` return values, `of(null)` and `EMPTY` substitutions, `throwError` rethrow paths, `finalize` cleanup, downstream consumption of the substituted value.  
**Finding condition:** Emit a finding when an error handler converts a required-data failure into an apparent success such as null, an empty collection, or a silent completion, or swallows an error so the user and telemetry see no failure.

**Quality caveats:** `catchError(() => EMPTY)` on an optional, independently observable side panel is acceptable. The same operator on a required-data route resolver is a finding.

### NG-005: Non-idempotent effects execute once per user intent

**Severity:** Critical  
**Category:** data-correctness  
**Applies when:** An observable chain triggers a non-idempotent business operation such as submit, payment, or enrollment.

**Requirement:** One user intent must produce exactly one business effect.

**Evidence to inspect:** Flattening operator on submit streams, `exhaustMap` and `concatMap` usage, `switchMap` on mutations, NgRx `createEffect` definitions, in-flight guards.  
**Finding condition:** Emit a finding when a flattening operator permits a non-idempotent operation to be issued concurrently or re-issued on repeat emission, or cancels an in-flight mutation whose server-side effect may already have occurred.

**Quality caveats:** `switchMap` on a mutation is doubly unsafe: it permits a second request and abandons the first with an unknown outcome. Pair this finding with `FE-004` when the unknown outcome is also mishandled.

### NG-006: Flattening operator matches business semantics

**Severity:** High  
**Category:** data-correctness  
**Applies when:** The application composes dependent or ordered asynchronous operations.

**Requirement:** The flattening operator must match the required ordering, cancellation, and concurrency semantics.

**Evidence to inspect:** `switchMap`, `mergeMap`, `concatMap`, `exhaustMap` selection against operation semantics, `forkJoin` and `combineLatest` failure behavior, concurrency limits on `mergeMap`.  
**Finding condition:** Emit a finding when the chosen flattening operator contradicts the required ordering, cancellation, or concurrency semantics of the operation, or when `forkJoin` is used where one failure must not discard every result.

### NG-007: Shared observables are bounded and reference-counted

**Severity:** High  
**Category:** memory-stability  
**Applies when:** An observable is multicast for reuse across subscribers.

**Requirement:** Multicast observables must release their source subscription and buffered state when no longer in use.

**Evidence to inspect:** `shareReplay` configuration, `refCount` behavior, `publishReplay` usage, `ReplaySubject` and `BehaviorSubject` lifetimes, user-scoped cached values.  
**Finding condition:** Emit a finding when a multicast observable retains its source subscription and buffered values after all subscribers unsubscribe, or caches a stale or user-scoped value beyond its valid lifetime.

**Version guidance:** RxJS 6.4 and later should use `shareReplay({ bufferSize: 1, refCount: true })`. Earlier versions satisfy this control with `publishReplay(1)` plus `refCount()`. `shareReplay(1)` without reference counting is noncompliant on every version that supports the configuration object.

### NG-008: Interceptors sequence authentication refresh correctly

**Severity:** High  
**Category:** authentication  
**Applies when:** An interceptor attaches or refreshes credentials.

**Requirement:** Refresh must occur inside the intercepted chain, deduplicate across concurrent requests, and preserve original operation identity.

**Evidence to inspect:** Interceptor registration and ordering, 401 handling, refresh stream sharing, retry placement relative to refresh, credential reattachment on the retried request.  
**Finding condition:** Emit a finding when token refresh occurs outside the intercepted chain, permits a refresh stampede across concurrent requests, retries the original request without the refreshed credential, or loses the original operation identity.

**Version guidance:** Angular 15 and later may use functional interceptors with `withInterceptors`. Earlier versions use class-based `HttpInterceptor` registered through `HTTP_INTERCEPTORS`. Both are compliant; evaluate sequencing, not style.

### NG-009: Route guards and resolvers are bounded

**Severity:** High  
**Category:** availability  
**Applies when:** The router uses guards or resolvers that perform asynchronous work.

**Requirement:** Navigation must not depend on an unbounded or unrecoverable asynchronous operation.

**Evidence to inspect:** Guard and resolver implementations, timeout and fallback handling, error routes, navigation error subscriptions, loading affordances during resolution.  
**Finding condition:** Emit a finding when a guard or resolver can block navigation indefinitely on a slow or failed dependency, or when a resolver failure produces an unrecoverable navigation state with no fallback route.

### NG-010: Global error handling and client health telemetry are wired

**Severity:** High  
**Category:** health  
**Applies when:** The application is operated as a production user-facing workload.

**Requirement:** Unhandled Angular errors must be captured and reported, and operators must be able to see that users cannot complete the primary flow.

**Evidence to inspect:** Custom `ErrorHandler` provider and `handleError` implementation, `unhandledrejection` wiring, telemetry SDK initialization, `trackException` calls, correlation header propagation, router navigation error handling.  
**Finding condition:** Emit a finding when a custom `ErrorHandler` is absent or swallows errors without reporting, when failed `HttpClient` calls and stuck resolver or guard states produce no operator-visible signal, or when client telemetry cannot be correlated to backend traces.

**Quality caveats:** Angular's default `ErrorHandler` logs to the console only. Console logging is not operator-visible telemetry. Deduplicate with `FE-006` and `FE-007` under one root cause.

### NG-011: Asynchronous state integrates consistently with change detection

**Severity:** Medium  
**Category:** performance  
**Applies when:** The application renders asynchronous state in templates.

**Requirement:** Asynchronous state must reach the view through a reliable change-detection path without duplicating work.

**Evidence to inspect:** `async` pipe usage, `toSignal` and signal adoption, `ChangeDetectionStrategy.OnPush` components, manual `markForCheck` or `detectChanges` calls, repeated `async` pipes over one source.  
**Finding condition:** Emit a finding when asynchronous state is manually assigned and rendered without a reliable change-detection path, when a single observable is subscribed multiple times in one template causing duplicate requests, or when `OnPush` components can render stale state.

**Version guidance:** Angular 16 and later may use signals and `toSignal`. Earlier versions satisfy this control with the `async` pipe under `OnPush`. Do not emit a finding because signals are unused.

### NG-012: Tests cover failure, cancellation, retry, and replay

**Severity:** Critical  
**Category:** testing  
**Applies when:** The repository contains Angular unit or integration tests.

**Requirement:** Tests must exercise observable failure behavior, not only happy-path emissions.

**Evidence to inspect:** `HttpTestingController` error and timing flows, `TestScheduler` marble tests, `fakeAsync` and `tick` usage, destroy-during-request tests, duplicate submission tests.  
**Finding condition:** Emit a finding when tests do not prove timeout, cancellation on destroy, retry exhaustion, error-path semantics, and duplicate submission behavior on the actual observable chains.

## Evidence and finding rules

- Use the control `severity` and `category` declared in frontmatter; do not reassign severity per finding.
- Record the detected Angular and RxJS versions and the evidence that established them in every finding produced by a version-conditional control.
- Return `not_assessed` for version-conditional controls when the effective version cannot be established.
- Evaluate effective behavior rather than the presence of an operator, decorator, or provider alone.
- Deduplicate with `FRONTEND-WEB-CLIENT` under one root cause; attribute the finding here when the defect is expressed in Angular or RxJS API usage.

## Finding classification

Resiliency classification follows `grounding/governance/resiliency-finding-qualification-policy.yml`. Subscription leaks, unbounded retries, cancelled mutations with unknown outcomes, and swallowed failures qualify as `resiliency`. Style, naming, and template-formatting defects are `non_resiliency`.

## Non-findings

- Use of an older but supported Angular or RxJS API where the required behavior is present.
- Absence of signals, standalone components, or functional interceptors on versions that support them, with no behavioral defect.
- Framework version upgrades proposed without an evidenced control violation.
- Deployed CDN, hosting, and gateway configuration.
