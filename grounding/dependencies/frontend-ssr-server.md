---
schema_version: "1.0.0"
document_type: dependency_standard
standard_id: FRONTEND-SSR-SERVER
service: frontend-ssr-server
service_name: Frontend Server-Side Rendering Workload
language: typescript-javascript
framework: ssr-framework-agnostic
version: "1.0.0"
lifecycle_status: active
assessment_domain: frontend_application
assessment_scope: server_rendering_workload_code_and_repository_owned_configuration
workload_kind: server
repository_owned_only: true
infrastructure_findings_allowed: false
requires_standard: frontend-web-client
activation:
  scope_context_path: application-context/assessment-scope-context.yml
  required_status: enabled
  additional_gate: ssr_detected
  gate_behavior: not_applicable_when_ssr_absent
assessment:
  enabled: true
  emit_findings: true
  include_in_score: true
  unknown_evidence_status: not_assessed
ssr_detection:
  resolution_rule: require_positive_repository_evidence
  absent_behavior: standard_not_applicable
  ambiguous_behavior: not_assessed_and_record_evidence_gap
  modes:
  - id: nextjs
    display_name: Next.js server rendering
    detect_dependencies: [next]
    detect_patterns:
    - next.config
    - getServerSideProps
    - getStaticProps
    - 'next start'
    - app/
    - use server
  - id: angular_ssr
    display_name: Angular SSR or Universal
    detect_dependencies: ['@angular/ssr', '@nguniversal/express-engine']
    detect_patterns:
    - server.ts
    - ngExpressEngine
    - CommonEngine
    - provideServerRendering
    - 'serve-ssr'
  - id: remix
    display_name: Remix or React Router server runtime
    detect_dependencies: ['@remix-run/node', '@remix-run/server-runtime']
    detect_patterns:
    - remix.config
    - 'export async function loader'
    - 'export async function action'
    - createRequestHandler
  - id: custom_node_ssr
    display_name: Custom Node render server
    detect_dependencies: [express, fastify, koa]
    detect_patterns:
    - renderToString
    - renderToPipeableStream
    - renderToReadableStream
    - hydrateRoot
    - createServer
  non_ssr_indicators:
  - static build output only
  - index.html served from storage or CDN
  - no server entry point in repository
  - build script produces client bundle only
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
- id: SSR-001
  title: Server render has a bounded deadline
  severity: critical
  category: timeout
  applies_when: the server renders markup for a request
  evidence_patterns:
  - renderToPipeableStream
  - renderToString
  - CommonEngine
  - onShellError
  - timeout
  finding_when: a server render can run without a bounded deadline, or an abandoned
    client connection does not abort the in-progress render
  emit_on_failure: true
- id: SSR-002
  title: Server-side data fetching is bounded and failure-isolated
  severity: critical
  category: dependency-resilience
  applies_when: the server fetches data while rendering a request
  evidence_patterns:
  - getServerSideProps
  - loader
  - 'fetch('
  - AbortSignal
  - Promise.allSettled
  finding_when: a render-time dependency call has no timeout, retry is unbounded, or
    a single non-critical dependency failure fails the entire server render
  emit_on_failure: true
- id: SSR-003
  title: Render failure degrades to a recoverable response
  severity: critical
  category: failure-containment
  applies_when: a server render can throw or time out
  evidence_patterns:
  - onShellError
  - onError
  - error boundary
  - 'status(500)'
  - fallback
  finding_when: a render failure returns an unusable response with no client-side fallback,
    leaks internal error detail to the browser, or cannot be distinguished from a dependency
    failure in telemetry
  emit_on_failure: true
- id: SSR-004
  title: Readiness and liveness represent serving eligibility
  severity: critical
  category: health
  applies_when: the render server is deployed as a long-lived process or container
  evidence_patterns:
  - /health
  - /ready
  - readinessProbe
  - livenessProbe
  - healthCheckPath
  finding_when: no readiness signal exists for a traffic-receiving render server, readiness
    reports healthy while the server cannot render the primary route, an external dependency
    failure participates in liveness and causes restart loops, or a probe targets a
    path or port the server does not expose
  emit_on_failure: true
- id: SSR-005
  title: Shutdown withdraws readiness and drains in-flight renders
  severity: critical
  category: lifecycle
  applies_when: the render server can be terminated by the platform
  evidence_patterns:
  - SIGTERM
  - server.close
  - terminationGracePeriodSeconds
  - preStop
  - keepAliveTimeout
  finding_when: the process does not handle SIGTERM, accepts new requests after termination
    begins, terminates before bounded drain of in-flight renders, or its drain budget
    exceeds the platform termination budget
  emit_on_failure: true
- id: SSR-006
  title: Per-request state is isolated
  severity: critical
  category: data-correctness
  applies_when: the server holds state across or during request rendering
  evidence_patterns:
  - module scope
  - let
  - global
  - singleton
  - createStore
  finding_when: mutable state, a store, a cache, or a client instance is shared across
    requests so one user's data, credentials, or locale can render into another user's
    response
  emit_on_failure: true
- id: SSR-007
  title: Server-only material stays out of the serialized payload
  severity: critical
  category: security-material
  applies_when: the server serializes state or props into the rendered document
  evidence_patterns:
  - __NEXT_DATA__
  - TransferState
  - dangerouslySetInnerHTML
  - process.env
  - serialize
  finding_when: secrets, internal endpoints, tokens, or personal data beyond the authenticated
    user's entitlement are serialized into the rendered document or transfer state
  emit_on_failure: true
- id: SSR-008
  title: Caching and revalidation are explicit and identity-safe
  severity: high
  category: data-freshness
  applies_when: rendered output or render-time data is cached
  evidence_patterns:
  - Cache-Control
  - revalidate
  - unstable_cache
  - s-maxage
  - private
  finding_when: personalized or authorization-dependent output is cached in a shared
    or public cache, cached output has no revalidation bound, or cache identity omits
    a factor that changes the rendered result
  emit_on_failure: true
- id: SSR-009
  title: Render concurrency and resource use are bounded
  severity: high
  category: resource-management
  applies_when: the render server handles concurrent requests
  evidence_patterns:
  - concurrency
  - maxSockets
  - event loop
  - heap
  - stream backpressure
  finding_when: unbounded concurrent rendering can exhaust CPU, memory, or the event
    loop, render work blocks the event loop without yielding, or the server applies
    no overload protection on a degraded dependency
  emit_on_failure: true
- id: SSR-010
  title: Regional configuration resolves at runtime on the server
  severity: critical
  category: configuration
  applies_when: the render server targets a backend endpoint, region, or environment-specific
    service
  evidence_patterns:
  - process.env
  - runtime config
  - serverRuntimeConfig
  - NEXT_PUBLIC_
  - environment.ts
  finding_when: a regional or environment endpoint is baked into the server build so
    the artifact cannot be promoted unchanged across regions, or a required endpoint
    can be omitted and silently default to a region
  emit_on_failure: true
- id: SSR-011
  title: Server observability and correlation are wired
  severity: high
  category: observability
  applies_when: the render server is operated as a production workload
  evidence_patterns:
  - traceparent
  - correlationId
  - structured log
  - render duration
  - trackDependency
  finding_when: render failures, render latency, and render-time dependency failures
    are not observable, correlation identity is not propagated from the inbound request
    to downstream calls, or logs carry secrets or personal data
  emit_on_failure: true
- id: SSR-012
  title: Hydration mismatch is prevented and detected
  severity: high
  category: consistency
  applies_when: server-rendered markup is hydrated on the client
  evidence_patterns:
  - hydrateRoot
  - hydration
  - suppressHydrationWarning
  - Date.now
  - window
  finding_when: render output depends on request-time or environment-specific values
    that differ between server and client, hydration mismatches are suppressed without
    investigation, or a mismatch can silently discard server-rendered state
  emit_on_failure: true
- id: SSR-013
  title: Tests cover render failure, shutdown, and isolation
  severity: critical
  category: testing
  applies_when: the repository contains tests for the render server
  evidence_patterns:
  - supertest
  - Playwright
  - integration test
  - SIGTERM test
  - concurrent request test
  finding_when: tests do not prove render timeout, dependency failure isolation, per-request
    state isolation under concurrency, graceful shutdown with in-flight renders, and
    hydration consistency
  emit_on_failure: true
---

# Frontend Server-Side Rendering Workload Standard

### Shared-service scope for concrete frontend dependencies

Resolve each concrete upstream service the render server calls through the registry and apply `architecture_context.shared_service_assessment_scope.services`. Evaluate service-specific behavior only when that concrete service is `in_scope`.

## Purpose

Evaluate a repository-owned server-side rendering workload as a **server**, not as a browser client. An SSR process accepts inbound requests, calls downstream dependencies, holds process state, and is deployed with a lifecycle and probe contract. Those properties require server controls that do not apply to an ordinary client-side single-page application.

## Activation

This standard requires **two** gates:

1. `frontend_application` is `enabled` in the active assessment scope.
2. Server-side rendering is confirmed through positive repository evidence per `ssr_detection`.

When SSR is not detected, every control in this standard is `not_applicable`. Do not apply SSR controls to a client-side SPA. When SSR evidence is ambiguous, mark controls `not_assessed` and record an evidence gap rather than assuming either state.

A repository that builds only a client bundle and serves `index.html` from storage or a CDN is **not** an SSR workload, even when the framework supports SSR.

## Workload boundary

When SSR is detected, the repository contains at least two workloads: the browser client and the render server. Record both in the inventory workload list and assess each against its applicable standards:

| Workload | Standards |
|---|---|
| Browser client | `FRONTEND-WEB-CLIENT`, plus `ANGULAR-RXJS` or `REACT-UI` |
| Render server | `FRONTEND-SSR-SERVER`, plus `JVM-RUNTIME-RESILIENCY` equivalents where a Node runtime standard exists, plus `KUBERNETES-DEPLOY` and container or CI/CD standards when those domains are enabled |

Controls that exist in both the client baseline and this standard are deduplicated under one root cause, attributed to the workload where the defect originates.

## Controls

### SSR-001: Server render has a bounded deadline

**Severity:** Critical  
**Category:** timeout  
**Applies when:** The server renders markup for a request.

**Requirement:** Every server render must be bounded and must abort when the client abandons the connection.

**Evidence to inspect:** Streaming and string render calls, shell error and timeout callbacks, request abort handling, framework render timeout configuration, reverse-proxy expectations declared in the repository.  
**Finding condition:** Emit a finding when a server render can run without a bounded deadline, or when an abandoned client connection does not abort the in-progress render.

### SSR-002: Server-side data fetching is bounded and failure-isolated

**Severity:** Critical  
**Category:** dependency-resilience  
**Applies when:** The server fetches data while rendering a request.

**Requirement:** Render-time dependency calls must be bounded, classified, and isolated so one non-critical failure does not fail the response.

**Evidence to inspect:** Server data functions and loaders, `fetch` and client calls with signal and timeout wiring, retry logic, parallel composition and failure aggregation, critical versus optional dependency treatment.  
**Finding condition:** Emit a finding when a render-time dependency call has no timeout, when retry is unbounded, or when a single non-critical dependency failure fails the entire server render.

**Quality caveats:** The render path inherits the caller's deadline. A render-time call slower than the upstream gateway timeout produces a wasted render and a user-visible error.

### SSR-003: Render failure degrades to a recoverable response

**Severity:** Critical  
**Category:** failure-containment  
**Applies when:** A server render can throw or time out.

**Requirement:** A failed render must produce a usable, non-leaking response with a client-side recovery path.

**Evidence to inspect:** Shell error handlers, error routes and pages, status code selection, error detail exposed in the response body, client-side fallback rendering.  
**Finding condition:** Emit a finding when a render failure returns an unusable response with no client-side fallback, leaks internal error detail to the browser, or cannot be distinguished from a dependency failure in telemetry.

### SSR-004: Readiness and liveness represent serving eligibility

**Severity:** Critical  
**Category:** health  
**Applies when:** The render server is deployed as a long-lived process or container.

**Requirement:** Readiness must reflect the server's ability to render the primary route. Liveness must exclude external dependency health.

**Evidence to inspect:** Health and readiness route definitions, probe configuration in repository-owned manifests or charts, health-check path settings, dependency participation in each signal, probe path and port alignment with the server's actual listener.  
**Finding condition:** Emit a finding when no readiness signal exists for a traffic-receiving render server, when readiness reports healthy while the server cannot render the primary route, when an external dependency failure participates in liveness and causes restart loops, or when a probe targets a path or port the server does not expose.

**Quality caveats:** A route that returns 200 without exercising the render path is not a readiness signal. Deduplicate with `K8S-DEPLOY-001` and `K8S-DEPLOY-002` when the defect originates in the manifest rather than the server, and with `HK-011` when it originates in chart or overlay composition.

### SSR-005: Shutdown withdraws readiness and drains in-flight renders

**Severity:** Critical  
**Category:** lifecycle  
**Applies when:** The render server can be terminated by the platform.

**Requirement:** Termination must withdraw readiness, stop accepting new requests, and drain in-flight renders within a bounded budget that fits the platform termination budget.

**Evidence to inspect:** SIGTERM handling, server close and connection draining, keep-alive and header timeouts, repository-owned grace period and preStop configuration, in-flight render accounting.  
**Finding condition:** Emit a finding when the process does not handle SIGTERM, accepts new requests after termination begins, terminates before bounded drain of in-flight renders, or when its drain budget exceeds the platform termination budget.

**Quality caveats:** Node does not drain keep-alive connections by default on `server.close()`. Deduplicate with `K8S-DEPLOY-004` when the defect originates in the manifest.

### SSR-006: Per-request state is isolated

**Severity:** Critical  
**Category:** data-correctness  
**Applies when:** The server holds state across or during request rendering.

**Requirement:** No user-scoped or request-scoped state may be shared across concurrent or sequential requests.

**Evidence to inspect:** Module-scoped mutable variables, singleton stores and caches created at import time, credential-bearing client instances, locale and theme state, dependency injection scope.  
**Finding condition:** Emit a finding when mutable state, a store, a cache, or a client instance is shared across requests so one user's data, credentials, or locale can render into another user's response.

**Quality caveats:** This is the highest-severity SSR defect class. A module-level store initialized once and mutated per request will cross-contaminate under concurrency even when single-request testing passes.

### SSR-007: Server-only material stays out of the serialized payload

**Severity:** Critical  
**Category:** security-material  
**Applies when:** The server serializes state or props into the rendered document.

**Requirement:** Serialized state must contain only what the authenticated user is entitled to receive.

**Evidence to inspect:** Serialized data islands and transfer state, props returned from server data functions, environment variable access in serialized paths, raw HTML injection, redaction before serialization.  
**Finding condition:** Emit a finding when secrets, internal endpoints, tokens, or personal data beyond the authenticated user's entitlement are serialized into the rendered document or transfer state.

### SSR-008: Caching and revalidation are explicit and identity-safe

**Severity:** High  
**Category:** data-freshness  
**Applies when:** Rendered output or render-time data is cached.

**Requirement:** Cache scope and lifetime must match the identity and authorization sensitivity of the rendered content.

**Evidence to inspect:** Response cache headers, framework revalidation settings, server cache helpers, cache key composition, public versus private cache designation.  
**Finding condition:** Emit a finding when personalized or authorization-dependent output is cached in a shared or public cache, when cached output has no revalidation bound, or when cache identity omits a factor that changes the rendered result.

### SSR-009: Render concurrency and resource use are bounded

**Severity:** High  
**Category:** resource-management  
**Applies when:** The render server handles concurrent requests.

**Requirement:** Rendering must not exhaust CPU, memory, or the event loop under load or dependency degradation.

**Evidence to inspect:** Concurrency limits, outbound socket limits, synchronous work on the request path, stream backpressure handling, memory and heap configuration, overload shedding.  
**Finding condition:** Emit a finding when unbounded concurrent rendering can exhaust CPU, memory, or the event loop, when render work blocks the event loop without yielding, or when the server applies no overload protection on a degraded dependency.

### SSR-010: Regional configuration resolves at runtime on the server

**Severity:** Critical  
**Category:** configuration  
**Applies when:** The render server targets a backend endpoint, region, or environment-specific service.

**Requirement:** One built server artifact must be promotable across every approved region and environment.

**Evidence to inspect:** Build-time versus runtime environment access, server runtime configuration mechanism, required-value validation at startup, defaults for regional endpoints, deployment injection.  
**Finding condition:** Emit a finding when a regional or environment endpoint is baked into the server build so the artifact cannot be promoted unchanged across regions, or when a required endpoint can be omitted and silently default to a region.

**Quality caveats:** Public-prefixed environment variables are inlined into client output at build time even when read on the server. Deduplicate with `FE-009`, `REACT-011`, and `CICD-002`.

### SSR-011: Server observability and correlation are wired

**Severity:** High  
**Category:** observability  
**Applies when:** The render server is operated as a production workload.

**Requirement:** Render outcomes, latency, and dependency failures must be observable and correlatable end to end.

**Evidence to inspect:** Inbound correlation header extraction, propagation to downstream calls, structured logging, render duration and outcome metrics, dependency tracking, redaction and sampling.  
**Finding condition:** Emit a finding when render failures, render latency, and render-time dependency failures are not observable, when correlation identity is not propagated from the inbound request to downstream calls, or when logs carry secrets or personal data.

### SSR-012: Hydration mismatch is prevented and detected

**Severity:** High  
**Category:** consistency  
**Applies when:** Server-rendered markup is hydrated on the client.

**Requirement:** Server and client render output must agree, and mismatches must be surfaced rather than suppressed.

**Evidence to inspect:** Time, random, locale, and browser-global usage in render paths, hydration suppression attributes, conditional client-only rendering, hydration error handling and reporting.  
**Finding condition:** Emit a finding when render output depends on request-time or environment-specific values that differ between server and client, when hydration mismatches are suppressed without investigation, or when a mismatch can silently discard server-rendered state.

### SSR-013: Tests cover render failure, shutdown, and isolation

**Severity:** Critical  
**Category:** testing  
**Applies when:** The repository contains tests for the render server.

**Requirement:** Tests must exercise the render server as a server, including concurrency and lifecycle.

**Evidence to inspect:** Server integration tests, dependency failure and latency simulation, concurrent request tests asserting state isolation, SIGTERM and drain tests, hydration consistency tests.  
**Finding condition:** Emit a finding when tests do not prove render timeout, dependency failure isolation, per-request state isolation under concurrency, graceful shutdown with in-flight renders, and hydration consistency.

## Evidence and finding rules

- Use the control `severity` and `category` declared in frontmatter; do not reassign severity per finding.
- Record the detected SSR mode and the evidence that established it in every finding.
- Return `not_assessed` when SSR evidence is ambiguous; return `not_applicable` when SSR is positively absent.
- Attribute a finding to the render server workload, not the browser client, and state the workload identity in the finding.
- Deduplicate with `FRONTEND-WEB-CLIENT`, `KUBERNETES-DEPLOY`, `HELM-KUSTOMIZE-RESILIENCY`, and container or CI/CD standards under one root cause.

## Finding classification

Resiliency classification follows `grounding/governance/resiliency-finding-qualification-policy.yml`. Unbounded renders, probe misrepresentation, shutdown defects, and cross-request state leakage qualify as `resiliency`. Cross-request leakage of user data is additionally a security defect and must preserve both classifications where the policy permits.

## Non-findings

- Any SSR control applied to a repository that produces a client bundle only.
- Deployed hosting plan, CDN, reverse proxy, and platform autoscale configuration.
- Framework version upgrades proposed without an evidenced control violation.
- Static site generation output that performs no per-request server rendering.
