---
schema_version: 2.0.0
document_type: master_application_behavior
service: springboot_aks_active_active
service_name: Spring Boot on AKS Active-Active Code Assessment
language: java
framework: spring-boot
runtime_platform: aks
assessment_scope: application_code_only
lifecycle_status: active
version: 2.0.0
last_updated: '2026-08-26'
owner: Cloud Architecture Team
assessment:
  enabled: true
  emit_findings: true
  include_in_score: true
  unknown_evidence_status: not_assessed
infrastructure_assumptions:
- Two independent Azure regions are provisioned and active.
- AKS, networking, private endpoints, DNS, identities, certificates, and dependent
  services follow the approved active-active infrastructure design.
- The deployment pipeline injects region-specific configuration into the same application
  artifact.
- The application repository does not provision or validate infrastructure.
exclusions:
- platform topology validation
- deployment workflow regional-parity controls
- infrastructure deployment
- PCF findings and remediation
controls:
- id: APP-AA-001
  title: One immutable artifact supports both regions
  severity: high
  category: deployability
  applies_when: always
  evidence_patterns:
  - pom.xml or build.gradle
  - Dockerfile
  - environment placeholders
  - profile selection
  finding_when: a region-specific code branch, build, artifact, or application profile
    is required
  emit_on_failure: true
- id: APP-AA-002
  title: Regional endpoints are externally configured
  severity: critical
  category: configuration
  applies_when: always
  evidence_patterns:
  - application.yml
  - application-*.yml
  - environment variables
  - '@ConfigurationProperties'
  - client builders
  finding_when: a regional endpoint, hostname, vault URI, namespace, account, cluster,
    or region is hardcoded
  emit_on_failure: true
- id: APP-AA-003
  title: Local-region dependency affinity is explicit
  severity: critical
  category: regional-affinity
  applies_when: always
  evidence_patterns:
  - region variable
  - regional endpoint mapping
  - deployment configuration contract
  finding_when: the application can select or default to a remote-region dependency
    during normal operation
  emit_on_failure: true
- id: APP-AA-004
  title: Dependency calls have bounded timeouts
  severity: critical
  category: resilience
  applies_when: always
  evidence_patterns:
  - Azure SDK client options
  - HTTP client timeout
  - JDBC timeout
  - Reactor timeout
  - Kafka timeout
  finding_when: a critical remote call can block indefinitely or beyond the failure-detection
    budget
  emit_on_failure: true
- id: APP-AA-005
  title: Transient failures use bounded retry with backoff
  severity: high
  category: resilience
  applies_when: always
  evidence_patterns:
  - SDK retry options
  - Spring Retry
  - Resilience4j Retry
  - Reactor retryWhen
  finding_when: transient failures are not retried, retries are unbounded, or terminal
    failures are retried without filtering
  emit_on_failure: true
- id: APP-AA-006
  title: Repeated failures are isolated by circuit breaking or bulkheading
  severity: high
  category: resilience
  applies_when: always
  evidence_patterns:
  - Resilience4j CircuitBreaker
  - Spring Cloud CircuitBreaker
  - Bulkhead
  - isolated connection pool
  finding_when: repeated dependency failure can exhaust shared threads, sockets, event
    loops, or connection pools
  emit_on_failure: true
- id: APP-AA-007
  title: Critical dependency failure affects readiness
  severity: critical
  category: health
  applies_when: always
  evidence_patterns:
  - HealthIndicator
  - ReactiveHealthIndicator
  - AvailabilityChangeEvent
  - readiness health group
  finding_when: a critical dependency remains unavailable after retry exhaustion while
    application readiness remains UP
  emit_on_failure: true
- id: APP-AA-008
  title: Liveness is not coupled to external dependencies
  severity: critical
  category: health
  applies_when: always
  evidence_patterns:
  - liveness health group
  - ApplicationAvailability
  - LivenessStateHealthIndicator
  finding_when: external dependency failure makes liveness fail or creates a restart
    loop
  emit_on_failure: true
- id: APP-AA-009
  title: Health checks are bounded and representative
  severity: high
  category: health
  applies_when: always
  evidence_patterns:
  - health groups
  - probe timeout
  - cached health state
  - synthetic operation
  finding_when: a health check can hang, overload a dependency, incur excessive cost,
    or succeed without representing the request-serving path
  emit_on_failure: true
- id: APP-AA-010
  title: Application state is region independent
  severity: critical
  category: state
  applies_when: always
  evidence_patterns:
  - HTTP session configuration
  - local file writes
  - in-memory maps
  - cache configuration
  finding_when: correct processing or session continuity depends on pod-local or region-local
    volatile state
  emit_on_failure: true
- id: APP-AA-011
  title: Mutating operations are idempotent
  severity: critical
  category: consistency
  applies_when: always
  evidence_patterns:
  - idempotency key
  - deduplication store
  - unique constraint
  - processed-event store
  finding_when: retry, replay, or cross-region duplicate delivery can create duplicate
    business effects
  emit_on_failure: true
- id: APP-AA-012
  title: Concurrency and conflict behavior is defined
  severity: high
  category: consistency
  applies_when: always
  evidence_patterns:
  - ETag
  - optimistic locking
  - '@Version'
  - conflict handler
  finding_when: simultaneous writes from both regions can silently overwrite or corrupt
    state
  emit_on_failure: true
- id: APP-AA-013
  title: Startup tolerates temporary dependency unavailability
  severity: high
  category: startup
  applies_when: always
  evidence_patterns:
  - lazy initialization
  - startup retry
  - readiness transition
  - fail-fast configuration
  finding_when: temporary dependency outage causes permanent startup failure or an
    uncontrolled crash loop
  emit_on_failure: true
- id: APP-AA-014
  title: Dependency recovery occurs without process restart
  severity: high
  category: recovery
  applies_when: always
  evidence_patterns:
  - connection recreation
  - credential refresh
  - circuit half-open
  - client lifecycle
  finding_when: the application cannot reconnect or return to readiness after dependency
    or network restoration
  emit_on_failure: true
- id: APP-AA-015
  title: Regional identity is present in telemetry
  severity: medium
  category: observability
  applies_when: always
  evidence_patterns:
  - region tag
  - OpenTelemetry resource attributes
  - Application Insights dimensions
  finding_when: logs, metrics, traces, and health events cannot identify the serving
    region
  emit_on_failure: true
- id: APP-AA-016
  title: Failures generate actionable monitoring signals
  severity: critical
  category: observability
  applies_when: always
  evidence_patterns:
  - metrics
  - structured logs
  - alerts
  - health details
  finding_when: retry exhaustion or critical dependency loss produces no actionable
    monitoring signal
  emit_on_failure: true
- id: APP-AA-017
  title: Graceful shutdown and traffic draining are implemented
  severity: high
  category: lifecycle
  applies_when: always
  evidence_patterns:
  - server.shutdown
  - preStop awareness
  - termination handling
  - readiness transition
  finding_when: pod termination interrupts in-flight work or accepts new traffic while
    shutting down
  emit_on_failure: true
- id: APP-AA-018
  title: Active-active failure behavior is tested
  severity: critical
  category: testing
  applies_when: always
  evidence_patterns:
  - unit tests
  - integration tests
  - fault injection
  - Testcontainers
  - WireMock
  finding_when: no automated test demonstrates timeout, retry, health transition,
    idempotency, and recovery behavior
  emit_on_failure: true
- id: APP-DISC-001
  title: Discovery-client endpoint and local-region topology are externally configurable
  severity: critical
  category: service-discovery
  applies_when: service discovery is used
  evidence_patterns:
  - '@EnableDiscoveryClient'
  - DiscoveryClient
  - service registry properties
  - registry endpoint
  - region metadata
  finding_when: the discovery endpoint or region is hardcoded, defaults to another
    region, or local-region registration and lookup behavior cannot be established
  emit_on_failure: true
- id: APP-DISC-002
  title: Discovery registration state participates in readiness when business-critical
  severity: high
  category: service-discovery
  applies_when: service discovery is critical
  evidence_patterns:
  - DiscoveryClientHealthIndicator
  - ReactiveDiscoveryClientHealthIndicator
  - custom HealthIndicator
  - readiness health group
  finding_when: critical registration or lookup failure leaves the application ready,
    or discovery failure is incorrectly coupled to liveness
  emit_on_failure: true
- id: APP-CONF-010
  title: Runtime configuration refresh behavior is defined and safe
  severity: high
  category: configuration
  applies_when: runtime refresh is enabled or expected
  evidence_patterns:
  - '@RefreshScope'
  - EnvironmentChangeEvent
  - ConfigurationPropertiesRebinder
  - actuator refresh
  - client or executor construction
  finding_when: refreshed values do not affect already-created clients or executors
    as intended, mutable settings change unsafely, or restart-required settings are
    undocumented
  emit_on_failure: true
- id: APP-REACT-001
  title: Reactive side effects execute exactly once per intended operation
  severity: critical
  category: reactive
  applies_when: Reactor is used
  evidence_patterns:
  - Mono.defer
  - Flux.defer
  - cache()
  - share()
  - publish
  - side-effecting repository call
  finding_when: a cold Mono or Flux containing a side effect can be subscribed more
    than once and repeat the operation
  emit_on_failure: true
- id: APP-REACT-002
  title: Reactive chains do not use detached internal subscriptions for business work
  severity: critical
  category: reactive
  applies_when: Reactor is used
  evidence_patterns:
  - .subscribe()
  - '@Async'
  - void service method
  - thenReturn
  - flatMap
  finding_when: production service code invokes subscribe internally, acknowledges
    before terminal completion, or detaches errors from the caller-visible chain
  emit_on_failure: true
- id: APP-REACT-003
  title: Reactive error handling preserves dependency failures and empty-result semantics
  severity: high
  category: reactive
  applies_when: Reactor is used
  evidence_patterns:
  - onErrorResume
  - switchIfEmpty
  - onErrorMap
  - timeout
  - retryWhen
  finding_when: dependency failures are converted to empty publishers, not-found results,
    silent success, or otherwise lose failure semantics
  emit_on_failure: true
- id: APP-CACHE-001
  title: Cache TTL and refresh intervals are externally configurable
  severity: medium
  category: cache
  applies_when: application-managed caching is used
  evidence_patterns:
  - expireAfterWrite
  - expireAfterAccess
  - Duration.of
  - time-to-live
  - spring.cache
  - Caffeine
  finding_when: cache TTL, refresh, or stale-value duration is a hardcoded literal
    without a documented invariant
  emit_on_failure: true
- id: APP-CACHE-002
  title: Cache sizing and eviction limits are externally configurable and bounded
  severity: high
  category: cache
  applies_when: application-managed caching is used
  evidence_patterns:
  - maximumSize
  - maximumWeight
  - CacheBuilder
  - Caffeine
  - cache capacity
  finding_when: cache size is unbounded or a hardcoded capacity cannot be tuned for
    regional workload and memory limits
  emit_on_failure: true
- id: APP-CACHE-003
  title: Cache contents do not create region-specific correctness dependencies
  severity: high
  category: cache
  applies_when: application-managed caching is used
  evidence_patterns:
  - cache key
  - local cache
  - distributed cache
  - invalidation
  - last-known-good
  finding_when: region-local cache state is required for correctness, authorization,
    session continuity, or safe failover
  emit_on_failure: true
- id: APP-ACT-001
  title: Actuator HTTP exposure is minimized to required endpoints
  severity: high
  category: management-security
  applies_when: Spring Boot Actuator is used
  evidence_patterns:
  - management.endpoints.web.exposure.include
  - management.endpoints.web.exposure.exclude
  - beans
  - env
  - heapdump
  - loggers
  - shutdown
  finding_when: broad or wildcard Actuator exposure makes unnecessary diagnostic or
    administrative endpoints remotely accessible
  emit_on_failure: true
- id: APP-ACT-002
  title: Sensitive Actuator endpoints are authenticated or network-isolated
  severity: critical
  category: management-security
  applies_when: sensitive Actuator endpoints are exposed
  evidence_patterns:
  - SecurityFilterChain
  - EndpointRequest
  - management.server.port
  - network policy
  - show-details
  finding_when: sensitive management endpoints are exposed without demonstrated access
    control or isolation
  emit_on_failure: true
- id: APP-ACT-003
  title: Actuator health detail disclosure is appropriate for its audience
  severity: medium
  category: management-security
  applies_when: Actuator health is exposed
  evidence_patterns:
  - management.endpoint.health.show-details
  - show-components
  - roles
  finding_when: health output available to untrusted callers can reveal dependency
    names, endpoints, exception details, or topology
  emit_on_failure: true
- id: APP-LOG-001
  title: Credentials, tokens, secrets, and connection strings are not logged
  severity: critical
  category: logging-security
  applies_when: always
  evidence_patterns:
  - log.debug
  - log.info
  - log.error
  - connection string
  - Authorization header
  - credential object
  - token
  - password
  finding_when: code logs secrets, tokens, credentials, authorization headers, full
    connection strings, or unredacted sensitive configuration
  emit_on_failure: true
- id: APP-LOG-002
  title: Sensitive values are masked before structured logging
  severity: high
  category: logging-security
  applies_when: always
  evidence_patterns:
  - mask
  - redact
  - sanitize
  - MDC
  - structured logger
  - toString
  finding_when: sensitive objects or configuration can be serialized or emitted without
    field-level masking
  emit_on_failure: true
- id: APP-WEB-001
  title: Exception advice matches the active servlet or reactive web model
  severity: high
  category: web-error-handling
  applies_when: always
  evidence_patterns:
  - '@ControllerAdvice'
  - '@RestControllerAdvice'
  - WebExceptionHandler
  - ErrorWebExceptionHandler
  - Mono
  - Flux
  - spring-boot-starter-web
  - spring-boot-starter-webflux
  finding_when: exception handling relies on servlet-only assumptions in a reactive
    path, reactive-only handling in a servlet path, or mixed-stack precedence leaves
    errors unmapped
  emit_on_failure: true
- id: APP-WEB-002
  title: Dependency failures map to stable, caller-visible error semantics
  severity: high
  category: web-error-handling
  applies_when: always
  evidence_patterns:
  - '@ExceptionHandler'
  - ResponseStatusException
  - HTTP 503
  - ProblemDetail
  - onErrorMap
  finding_when: dependency failure is returned as success, not found, validation failure,
    or an inconsistent status that prevents safe caller retry
  emit_on_failure: true
---

# Spring Boot on AKS Active-Active Code Assessment Standard

## Purpose

This master grounding standard assesses whether Java Spring Boot microservices are coded and configured to operate safely as the same immutable artifact in two simultaneously active Azure regions. It assumes the approved regional infrastructure already exists and is correctly deployed.

Version 2.0 adds application-level controls for discovery-client behavior, runtime refresh semantics, Reactor subscription safety, caches, Actuator exposure, credential logging, and servlet/reactive exception-handling alignment. Deployment automation and platform-topology controls are intentionally excluded from this version.

## Scope boundary

Assess:

- Java and Spring Boot production code
- Repository-owned application configuration
- Client construction and dependency behavior
- Health, readiness, and liveness
- State, idempotency, concurrency, and reactive behavior
- Application-managed caching
- Application logging and management-endpoint security
- Automated application tests

Do not assess:

- Whether two regions or shared services have been deployed
- Azure resource configuration or platform topology
- Private endpoints, DNS, capacity, availability zones, or geo-replication
- Regional deployment jobs, `Actionsfile` descriptors, workflow parity, or shared workflow catalog compatibility
- PCF migration, modernization, cleanup, or findings

## Mandatory evaluator workflow

1. Load this master standard for every Spring Boot active-active code assessment.
2. Load only dependency-specific standards listed in the authoritative inventory.
3. Evaluate controls only when their applicability condition is met.
4. Cite repository evidence for every decision.
5. Return `not_assessed` when evidence is insufficient.
6. Emit findings only for evidence-backed `non_compliant` controls.
7. Deduplicate findings by root cause.
8. Do not create infrastructure or PCF findings.

## Required statuses

- `compliant`
- `non_compliant`
- `not_assessed`
- `not_applicable`
- `accepted_risk`

## Cross-control guidance

- A critical dependency failure normally affects readiness, not liveness.
- A hardcoded regional endpoint can violate both endpoint externalization and local-region affinity; emit one root-cause finding with related controls.
- A detached `.subscribe()` may also cause early acknowledgement, lost error propagation, duplicate cold-publisher execution, or inability to validate completion. Consolidate when one implementation change addresses the root cause.
- A missing fault test inherits the priority of the behavior it must prove.
- Actuator exposure and credential logging are application-code/configuration findings, but network topology is outside scope.
- Discovery-client code/configuration behavior is in scope; external service-registry deployment topology is not.
- `@RefreshScope` presence alone does not prove already-created clients, pools, executors, or caches are reconfigured safely.

# Controls

## APP-AA-001: One immutable artifact supports both regions

**Severity:** High  
**Category:** deployability  
**Applies when:** always

### Requirement

The application code and repository-owned configuration must satisfy this behavior when the same artifact runs in either active region.

### Repository evidence to inspect

- `pom.xml or build.gradle`
- `Dockerfile`
- `environment placeholders`
- `profile selection`

### Finding condition

Emit a finding when evidence shows that a region-specific code branch, build, artifact, or application profile is required.

### Evaluation guidance

- Cite file path, symbol or property, and line range when available.
- Distinguish explicit application behavior from framework defaults.
- If evidence is missing or ambiguous, return `not_assessed`, not `non_compliant`.
- Do not create an infrastructure finding or assume external platform topology is incorrect.
- Do not emit the control when its applicability condition is not met.

### Recommended remediation scope

Recommend application code, repository-owned application configuration, health behavior, error handling, telemetry, or automated-test changes only.

---

## APP-AA-002: Regional endpoints are externally configured

**Severity:** Critical  
**Category:** configuration  
**Applies when:** always

### Requirement

The application code and repository-owned configuration must satisfy this behavior when the same artifact runs in either active region.

### Repository evidence to inspect

- `application.yml`
- `application-*.yml`
- `environment variables`
- `@ConfigurationProperties`
- `client builders`

### Finding condition

Emit a finding when evidence shows that a regional endpoint, hostname, vault URI, namespace, account, cluster, or region is hardcoded.

### Evaluation guidance

- Cite file path, symbol or property, and line range when available.
- Distinguish explicit application behavior from framework defaults.
- If evidence is missing or ambiguous, return `not_assessed`, not `non_compliant`.
- Do not create an infrastructure finding or assume external platform topology is incorrect.
- Do not emit the control when its applicability condition is not met.

### Recommended remediation scope

Recommend application code, repository-owned application configuration, health behavior, error handling, telemetry, or automated-test changes only.

---

## APP-AA-003: Local-region dependency affinity is explicit

**Severity:** Critical  
**Category:** regional-affinity  
**Applies when:** always

### Requirement

The application code and repository-owned configuration must satisfy this behavior when the same artifact runs in either active region.

### Repository evidence to inspect

- `region variable`
- `regional endpoint mapping`
- `deployment configuration contract`

### Finding condition

Emit a finding when evidence shows that the application can select or default to a remote-region dependency during normal operation.

### Evaluation guidance

- Cite file path, symbol or property, and line range when available.
- Distinguish explicit application behavior from framework defaults.
- If evidence is missing or ambiguous, return `not_assessed`, not `non_compliant`.
- Do not create an infrastructure finding or assume external platform topology is incorrect.
- Do not emit the control when its applicability condition is not met.

### Recommended remediation scope

Recommend application code, repository-owned application configuration, health behavior, error handling, telemetry, or automated-test changes only.

---

## APP-AA-004: Dependency calls have bounded timeouts

**Severity:** Critical  
**Category:** resilience  
**Applies when:** always

### Requirement

The application code and repository-owned configuration must satisfy this behavior when the same artifact runs in either active region.

### Repository evidence to inspect

- `Azure SDK client options`
- `HTTP client timeout`
- `JDBC timeout`
- `Reactor timeout`
- `Kafka timeout`

### Finding condition

Emit a finding when evidence shows that a critical remote call can block indefinitely or beyond the failure-detection budget.

### Evaluation guidance

- Cite file path, symbol or property, and line range when available.
- Distinguish explicit application behavior from framework defaults.
- If evidence is missing or ambiguous, return `not_assessed`, not `non_compliant`.
- Do not create an infrastructure finding or assume external platform topology is incorrect.
- Do not emit the control when its applicability condition is not met.

### Recommended remediation scope

Recommend application code, repository-owned application configuration, health behavior, error handling, telemetry, or automated-test changes only.

---

## APP-AA-005: Transient failures use bounded retry with backoff

**Severity:** High  
**Category:** resilience  
**Applies when:** always

### Requirement

The application code and repository-owned configuration must satisfy this behavior when the same artifact runs in either active region.

### Repository evidence to inspect

- `SDK retry options`
- `Spring Retry`
- `Resilience4j Retry`
- `Reactor retryWhen`

### Finding condition

Emit a finding when evidence shows that transient failures are not retried, retries are unbounded, or terminal failures are retried without filtering.

### Evaluation guidance

- Cite file path, symbol or property, and line range when available.
- Distinguish explicit application behavior from framework defaults.
- If evidence is missing or ambiguous, return `not_assessed`, not `non_compliant`.
- Do not create an infrastructure finding or assume external platform topology is incorrect.
- Do not emit the control when its applicability condition is not met.

### Recommended remediation scope

Recommend application code, repository-owned application configuration, health behavior, error handling, telemetry, or automated-test changes only.

---

## APP-AA-006: Repeated failures are isolated by circuit breaking or bulkheading

**Severity:** High  
**Category:** resilience  
**Applies when:** always

### Requirement

The application code and repository-owned configuration must satisfy this behavior when the same artifact runs in either active region.

### Repository evidence to inspect

- `Resilience4j CircuitBreaker`
- `Spring Cloud CircuitBreaker`
- `Bulkhead`
- `isolated connection pool`

### Finding condition

Emit a finding when evidence shows that repeated dependency failure can exhaust shared threads, sockets, event loops, or connection pools.

### Evaluation guidance

- Cite file path, symbol or property, and line range when available.
- Distinguish explicit application behavior from framework defaults.
- If evidence is missing or ambiguous, return `not_assessed`, not `non_compliant`.
- Do not create an infrastructure finding or assume external platform topology is incorrect.
- Do not emit the control when its applicability condition is not met.

### Recommended remediation scope

Recommend application code, repository-owned application configuration, health behavior, error handling, telemetry, or automated-test changes only.

---

## APP-AA-007: Critical dependency failure affects readiness

**Severity:** Critical  
**Category:** health  
**Applies when:** always

### Requirement

The application code and repository-owned configuration must satisfy this behavior when the same artifact runs in either active region.

### Repository evidence to inspect

- `HealthIndicator`
- `ReactiveHealthIndicator`
- `AvailabilityChangeEvent`
- `readiness health group`

### Finding condition

Emit a finding when evidence shows that a critical dependency remains unavailable after retry exhaustion while application readiness remains UP.

### Evaluation guidance

- Cite file path, symbol or property, and line range when available.
- Distinguish explicit application behavior from framework defaults.
- If evidence is missing or ambiguous, return `not_assessed`, not `non_compliant`.
- Do not create an infrastructure finding or assume external platform topology is incorrect.
- Do not emit the control when its applicability condition is not met.

### Recommended remediation scope

Recommend application code, repository-owned application configuration, health behavior, error handling, telemetry, or automated-test changes only.

---

## APP-AA-008: Liveness is not coupled to external dependencies

**Severity:** Critical  
**Category:** health  
**Applies when:** always

### Requirement

The application code and repository-owned configuration must satisfy this behavior when the same artifact runs in either active region.

### Repository evidence to inspect

- `liveness health group`
- `ApplicationAvailability`
- `LivenessStateHealthIndicator`

### Finding condition

Emit a finding when evidence shows that external dependency failure makes liveness fail or creates a restart loop.

### Evaluation guidance

- Cite file path, symbol or property, and line range when available.
- Distinguish explicit application behavior from framework defaults.
- If evidence is missing or ambiguous, return `not_assessed`, not `non_compliant`.
- Do not create an infrastructure finding or assume external platform topology is incorrect.
- Do not emit the control when its applicability condition is not met.

### Recommended remediation scope

Recommend application code, repository-owned application configuration, health behavior, error handling, telemetry, or automated-test changes only.

---

## APP-AA-009: Health checks are bounded and representative

**Severity:** High  
**Category:** health  
**Applies when:** always

### Requirement

The application code and repository-owned configuration must satisfy this behavior when the same artifact runs in either active region.

### Repository evidence to inspect

- `health groups`
- `probe timeout`
- `cached health state`
- `synthetic operation`

### Finding condition

Emit a finding when evidence shows that a health check can hang, overload a dependency, incur excessive cost, or succeed without representing the request-serving path.

### Evaluation guidance

- Cite file path, symbol or property, and line range when available.
- Distinguish explicit application behavior from framework defaults.
- If evidence is missing or ambiguous, return `not_assessed`, not `non_compliant`.
- Do not create an infrastructure finding or assume external platform topology is incorrect.
- Do not emit the control when its applicability condition is not met.

### Recommended remediation scope

Recommend application code, repository-owned application configuration, health behavior, error handling, telemetry, or automated-test changes only.

---

## APP-AA-010: Application state is region independent

**Severity:** Critical  
**Category:** state  
**Applies when:** always

### Requirement

The application code and repository-owned configuration must satisfy this behavior when the same artifact runs in either active region.

### Repository evidence to inspect

- `HTTP session configuration`
- `local file writes`
- `in-memory maps`
- `cache configuration`

### Finding condition

Emit a finding when evidence shows that correct processing or session continuity depends on pod-local or region-local volatile state.

### Evaluation guidance

- Cite file path, symbol or property, and line range when available.
- Distinguish explicit application behavior from framework defaults.
- If evidence is missing or ambiguous, return `not_assessed`, not `non_compliant`.
- Do not create an infrastructure finding or assume external platform topology is incorrect.
- Do not emit the control when its applicability condition is not met.

### Recommended remediation scope

Recommend application code, repository-owned application configuration, health behavior, error handling, telemetry, or automated-test changes only.

---

## APP-AA-011: Mutating operations are idempotent

**Severity:** Critical  
**Category:** consistency  
**Applies when:** always

### Requirement

The application code and repository-owned configuration must satisfy this behavior when the same artifact runs in either active region.

### Repository evidence to inspect

- `idempotency key`
- `deduplication store`
- `unique constraint`
- `processed-event store`

### Finding condition

Emit a finding when evidence shows that retry, replay, or cross-region duplicate delivery can create duplicate business effects.

### Evaluation guidance

- Cite file path, symbol or property, and line range when available.
- Distinguish explicit application behavior from framework defaults.
- If evidence is missing or ambiguous, return `not_assessed`, not `non_compliant`.
- Do not create an infrastructure finding or assume external platform topology is incorrect.
- Do not emit the control when its applicability condition is not met.

### Recommended remediation scope

Recommend application code, repository-owned application configuration, health behavior, error handling, telemetry, or automated-test changes only.

---

## APP-AA-012: Concurrency and conflict behavior is defined

**Severity:** High  
**Category:** consistency  
**Applies when:** always

### Requirement

The application code and repository-owned configuration must satisfy this behavior when the same artifact runs in either active region.

### Repository evidence to inspect

- `ETag`
- `optimistic locking`
- `@Version`
- `conflict handler`

### Finding condition

Emit a finding when evidence shows that simultaneous writes from both regions can silently overwrite or corrupt state.

### Evaluation guidance

- Cite file path, symbol or property, and line range when available.
- Distinguish explicit application behavior from framework defaults.
- If evidence is missing or ambiguous, return `not_assessed`, not `non_compliant`.
- Do not create an infrastructure finding or assume external platform topology is incorrect.
- Do not emit the control when its applicability condition is not met.

### Recommended remediation scope

Recommend application code, repository-owned application configuration, health behavior, error handling, telemetry, or automated-test changes only.

---

## APP-AA-013: Startup tolerates temporary dependency unavailability

**Severity:** High  
**Category:** startup  
**Applies when:** always

### Requirement

The application code and repository-owned configuration must satisfy this behavior when the same artifact runs in either active region.

### Repository evidence to inspect

- `lazy initialization`
- `startup retry`
- `readiness transition`
- `fail-fast configuration`

### Finding condition

Emit a finding when evidence shows that temporary dependency outage causes permanent startup failure or an uncontrolled crash loop.

### Evaluation guidance

- Cite file path, symbol or property, and line range when available.
- Distinguish explicit application behavior from framework defaults.
- If evidence is missing or ambiguous, return `not_assessed`, not `non_compliant`.
- Do not create an infrastructure finding or assume external platform topology is incorrect.
- Do not emit the control when its applicability condition is not met.

### Recommended remediation scope

Recommend application code, repository-owned application configuration, health behavior, error handling, telemetry, or automated-test changes only.

---

## APP-AA-014: Dependency recovery occurs without process restart

**Severity:** High  
**Category:** recovery  
**Applies when:** always

### Requirement

The application code and repository-owned configuration must satisfy this behavior when the same artifact runs in either active region.

### Repository evidence to inspect

- `connection recreation`
- `credential refresh`
- `circuit half-open`
- `client lifecycle`

### Finding condition

Emit a finding when evidence shows that the application cannot reconnect or return to readiness after dependency or network restoration.

### Evaluation guidance

- Cite file path, symbol or property, and line range when available.
- Distinguish explicit application behavior from framework defaults.
- If evidence is missing or ambiguous, return `not_assessed`, not `non_compliant`.
- Do not create an infrastructure finding or assume external platform topology is incorrect.
- Do not emit the control when its applicability condition is not met.

### Recommended remediation scope

Recommend application code, repository-owned application configuration, health behavior, error handling, telemetry, or automated-test changes only.

---

## APP-AA-015: Regional identity is present in telemetry

**Severity:** Medium  
**Category:** observability  
**Applies when:** always

### Requirement

The application code and repository-owned configuration must satisfy this behavior when the same artifact runs in either active region.

### Repository evidence to inspect

- `region tag`
- `OpenTelemetry resource attributes`
- `Application Insights dimensions`

### Finding condition

Emit a finding when evidence shows that logs, metrics, traces, and health events cannot identify the serving region.

### Evaluation guidance

- Cite file path, symbol or property, and line range when available.
- Distinguish explicit application behavior from framework defaults.
- If evidence is missing or ambiguous, return `not_assessed`, not `non_compliant`.
- Do not create an infrastructure finding or assume external platform topology is incorrect.
- Do not emit the control when its applicability condition is not met.

### Recommended remediation scope

Recommend application code, repository-owned application configuration, health behavior, error handling, telemetry, or automated-test changes only.

---

## APP-AA-016: Failures generate actionable monitoring signals

**Severity:** Critical  
**Category:** observability  
**Applies when:** always

### Requirement

The application code and repository-owned configuration must satisfy this behavior when the same artifact runs in either active region.

### Repository evidence to inspect

- `metrics`
- `structured logs`
- `alerts`
- `health details`

### Finding condition

Emit a finding when evidence shows that retry exhaustion or critical dependency loss produces no actionable monitoring signal.

### Evaluation guidance

- Cite file path, symbol or property, and line range when available.
- Distinguish explicit application behavior from framework defaults.
- If evidence is missing or ambiguous, return `not_assessed`, not `non_compliant`.
- Do not create an infrastructure finding or assume external platform topology is incorrect.
- Do not emit the control when its applicability condition is not met.

### Recommended remediation scope

Recommend application code, repository-owned application configuration, health behavior, error handling, telemetry, or automated-test changes only.

---

## APP-AA-017: Graceful shutdown and traffic draining are implemented

**Severity:** High  
**Category:** lifecycle  
**Applies when:** always

### Requirement

The application code and repository-owned configuration must satisfy this behavior when the same artifact runs in either active region.

### Repository evidence to inspect

- `server.shutdown`
- `preStop awareness`
- `termination handling`
- `readiness transition`

### Finding condition

Emit a finding when evidence shows that pod termination interrupts in-flight work or accepts new traffic while shutting down.

### Evaluation guidance

- Cite file path, symbol or property, and line range when available.
- Distinguish explicit application behavior from framework defaults.
- If evidence is missing or ambiguous, return `not_assessed`, not `non_compliant`.
- Do not create an infrastructure finding or assume external platform topology is incorrect.
- Do not emit the control when its applicability condition is not met.

### Recommended remediation scope

Recommend application code, repository-owned application configuration, health behavior, error handling, telemetry, or automated-test changes only.

---

## APP-AA-018: Active-active failure behavior is tested

**Severity:** Critical  
**Category:** testing  
**Applies when:** always

### Requirement

The application code and repository-owned configuration must satisfy this behavior when the same artifact runs in either active region.

### Repository evidence to inspect

- `unit tests`
- `integration tests`
- `fault injection`
- `Testcontainers`
- `WireMock`

### Finding condition

Emit a finding when evidence shows that no automated test demonstrates timeout, retry, health transition, idempotency, and recovery behavior.

### Evaluation guidance

- Cite file path, symbol or property, and line range when available.
- Distinguish explicit application behavior from framework defaults.
- If evidence is missing or ambiguous, return `not_assessed`, not `non_compliant`.
- Do not create an infrastructure finding or assume external platform topology is incorrect.
- Do not emit the control when its applicability condition is not met.

### Recommended remediation scope

Recommend application code, repository-owned application configuration, health behavior, error handling, telemetry, or automated-test changes only.

---

## APP-DISC-001: Discovery-client endpoint and local-region topology are externally configurable

**Severity:** Critical  
**Category:** service-discovery  
**Applies when:** service discovery is used

### Requirement

The application code and repository-owned configuration must satisfy this behavior when the same artifact runs in either active region.

### Repository evidence to inspect

- `@EnableDiscoveryClient`
- `DiscoveryClient`
- `service registry properties`
- `registry endpoint`
- `region metadata`

### Finding condition

Emit a finding when evidence shows that the discovery endpoint or region is hardcoded, defaults to another region, or local-region registration and lookup behavior cannot be established.

### Evaluation guidance

- Cite file path, symbol or property, and line range when available.
- Distinguish explicit application behavior from framework defaults.
- If evidence is missing or ambiguous, return `not_assessed`, not `non_compliant`.
- Do not create an infrastructure finding or assume external platform topology is incorrect.
- Do not emit the control when its applicability condition is not met.

### Recommended remediation scope

Recommend application code, repository-owned application configuration, health behavior, error handling, telemetry, or automated-test changes only.

---

## APP-DISC-002: Discovery registration state participates in readiness when business-critical

**Severity:** High  
**Category:** service-discovery  
**Applies when:** service discovery is critical

### Requirement

The application code and repository-owned configuration must satisfy this behavior when the same artifact runs in either active region.

### Repository evidence to inspect

- `DiscoveryClientHealthIndicator`
- `ReactiveDiscoveryClientHealthIndicator`
- `custom HealthIndicator`
- `readiness health group`

### Finding condition

Emit a finding when evidence shows that critical registration or lookup failure leaves the application ready, or discovery failure is incorrectly coupled to liveness.

### Evaluation guidance

- Cite file path, symbol or property, and line range when available.
- Distinguish explicit application behavior from framework defaults.
- If evidence is missing or ambiguous, return `not_assessed`, not `non_compliant`.
- Do not create an infrastructure finding or assume external platform topology is incorrect.
- Do not emit the control when its applicability condition is not met.

### Recommended remediation scope

Recommend application code, repository-owned application configuration, health behavior, error handling, telemetry, or automated-test changes only.

---

## APP-CONF-010: Runtime configuration refresh behavior is defined and safe

**Severity:** High  
**Category:** configuration  
**Applies when:** runtime refresh is enabled or expected

### Requirement

The application code and repository-owned configuration must satisfy this behavior when the same artifact runs in either active region.

### Repository evidence to inspect

- `@RefreshScope`
- `EnvironmentChangeEvent`
- `ConfigurationPropertiesRebinder`
- `actuator refresh`
- `client or executor construction`

### Finding condition

Emit a finding when evidence shows that refreshed values do not affect already-created clients or executors as intended, mutable settings change unsafely, or restart-required settings are undocumented.

### Evaluation guidance

- Cite file path, symbol or property, and line range when available.
- Distinguish explicit application behavior from framework defaults.
- If evidence is missing or ambiguous, return `not_assessed`, not `non_compliant`.
- Do not create an infrastructure finding or assume external platform topology is incorrect.
- Do not emit the control when its applicability condition is not met.

### Recommended remediation scope

Recommend application code, repository-owned application configuration, health behavior, error handling, telemetry, or automated-test changes only.

---

## APP-REACT-001: Reactive side effects execute exactly once per intended operation

**Severity:** Critical  
**Category:** reactive  
**Applies when:** Reactor is used

### Requirement

The application code and repository-owned configuration must satisfy this behavior when the same artifact runs in either active region.

### Repository evidence to inspect

- `Mono.defer`
- `Flux.defer`
- `cache()`
- `share()`
- `publish`
- `side-effecting repository call`

### Finding condition

Emit a finding when evidence shows that a cold Mono or Flux containing a side effect can be subscribed more than once and repeat the operation.

### Evaluation guidance

- Cite file path, symbol or property, and line range when available.
- Distinguish explicit application behavior from framework defaults.
- If evidence is missing or ambiguous, return `not_assessed`, not `non_compliant`.
- Do not create an infrastructure finding or assume external platform topology is incorrect.
- Do not emit the control when its applicability condition is not met.

### Recommended remediation scope

Recommend application code, repository-owned application configuration, health behavior, error handling, telemetry, or automated-test changes only.

---

## APP-REACT-002: Reactive chains do not use detached internal subscriptions for business work

**Severity:** Critical  
**Category:** reactive  
**Applies when:** Reactor is used

### Requirement

The application code and repository-owned configuration must satisfy this behavior when the same artifact runs in either active region.

### Repository evidence to inspect

- `.subscribe()`
- `@Async`
- `void service method`
- `thenReturn`
- `flatMap`

### Finding condition

Emit a finding when evidence shows that production service code invokes subscribe internally, acknowledges before terminal completion, or detaches errors from the caller-visible chain.

### Evaluation guidance

- Cite file path, symbol or property, and line range when available.
- Distinguish explicit application behavior from framework defaults.
- If evidence is missing or ambiguous, return `not_assessed`, not `non_compliant`.
- Do not create an infrastructure finding or assume external platform topology is incorrect.
- Do not emit the control when its applicability condition is not met.

### Recommended remediation scope

Recommend application code, repository-owned application configuration, health behavior, error handling, telemetry, or automated-test changes only.

---

## APP-REACT-003: Reactive error handling preserves dependency failures and empty-result semantics

**Severity:** High  
**Category:** reactive  
**Applies when:** Reactor is used

### Requirement

The application code and repository-owned configuration must satisfy this behavior when the same artifact runs in either active region.

### Repository evidence to inspect

- `onErrorResume`
- `switchIfEmpty`
- `onErrorMap`
- `timeout`
- `retryWhen`

### Finding condition

Emit a finding when evidence shows that dependency failures are converted to empty publishers, not-found results, silent success, or otherwise lose failure semantics.

### Evaluation guidance

- Cite file path, symbol or property, and line range when available.
- Distinguish explicit application behavior from framework defaults.
- If evidence is missing or ambiguous, return `not_assessed`, not `non_compliant`.
- Do not create an infrastructure finding or assume external platform topology is incorrect.
- Do not emit the control when its applicability condition is not met.

### Recommended remediation scope

Recommend application code, repository-owned application configuration, health behavior, error handling, telemetry, or automated-test changes only.

---

## APP-CACHE-001: Cache TTL and refresh intervals are externally configurable

**Severity:** Medium  
**Category:** cache  
**Applies when:** application-managed caching is used

### Requirement

The application code and repository-owned configuration must satisfy this behavior when the same artifact runs in either active region.

### Repository evidence to inspect

- `expireAfterWrite`
- `expireAfterAccess`
- `Duration.of`
- `time-to-live`
- `spring.cache`
- `Caffeine`

### Finding condition

Emit a finding when evidence shows that cache TTL, refresh, or stale-value duration is a hardcoded literal without a documented invariant.

### Evaluation guidance

- Cite file path, symbol or property, and line range when available.
- Distinguish explicit application behavior from framework defaults.
- If evidence is missing or ambiguous, return `not_assessed`, not `non_compliant`.
- Do not create an infrastructure finding or assume external platform topology is incorrect.
- Do not emit the control when its applicability condition is not met.

### Recommended remediation scope

Recommend application code, repository-owned application configuration, health behavior, error handling, telemetry, or automated-test changes only.

---

## APP-CACHE-002: Cache sizing and eviction limits are externally configurable and bounded

**Severity:** High  
**Category:** cache  
**Applies when:** application-managed caching is used

### Requirement

The application code and repository-owned configuration must satisfy this behavior when the same artifact runs in either active region.

### Repository evidence to inspect

- `maximumSize`
- `maximumWeight`
- `CacheBuilder`
- `Caffeine`
- `cache capacity`

### Finding condition

Emit a finding when evidence shows that cache size is unbounded or a hardcoded capacity cannot be tuned for regional workload and memory limits.

### Evaluation guidance

- Cite file path, symbol or property, and line range when available.
- Distinguish explicit application behavior from framework defaults.
- If evidence is missing or ambiguous, return `not_assessed`, not `non_compliant`.
- Do not create an infrastructure finding or assume external platform topology is incorrect.
- Do not emit the control when its applicability condition is not met.

### Recommended remediation scope

Recommend application code, repository-owned application configuration, health behavior, error handling, telemetry, or automated-test changes only.

---

## APP-CACHE-003: Cache contents do not create region-specific correctness dependencies

**Severity:** High  
**Category:** cache  
**Applies when:** application-managed caching is used

### Requirement

The application code and repository-owned configuration must satisfy this behavior when the same artifact runs in either active region.

### Repository evidence to inspect

- `cache key`
- `local cache`
- `distributed cache`
- `invalidation`
- `last-known-good`

### Finding condition

Emit a finding when evidence shows that region-local cache state is required for correctness, authorization, session continuity, or safe failover.

### Evaluation guidance

- Cite file path, symbol or property, and line range when available.
- Distinguish explicit application behavior from framework defaults.
- If evidence is missing or ambiguous, return `not_assessed`, not `non_compliant`.
- Do not create an infrastructure finding or assume external platform topology is incorrect.
- Do not emit the control when its applicability condition is not met.

### Recommended remediation scope

Recommend application code, repository-owned application configuration, health behavior, error handling, telemetry, or automated-test changes only.

---

## APP-ACT-001: Actuator HTTP exposure is minimized to required endpoints

**Severity:** High  
**Category:** management-security  
**Applies when:** Spring Boot Actuator is used

### Requirement

The application code and repository-owned configuration must satisfy this behavior when the same artifact runs in either active region.

### Repository evidence to inspect

- `management.endpoints.web.exposure.include`
- `management.endpoints.web.exposure.exclude`
- `beans`
- `env`
- `heapdump`
- `loggers`
- `shutdown`

### Finding condition

Emit a finding when evidence shows that broad or wildcard Actuator exposure makes unnecessary diagnostic or administrative endpoints remotely accessible.

### Evaluation guidance

- Cite file path, symbol or property, and line range when available.
- Distinguish explicit application behavior from framework defaults.
- If evidence is missing or ambiguous, return `not_assessed`, not `non_compliant`.
- Do not create an infrastructure finding or assume external platform topology is incorrect.
- Do not emit the control when its applicability condition is not met.

### Recommended remediation scope

Recommend application code, repository-owned application configuration, health behavior, error handling, telemetry, or automated-test changes only.

---

## APP-ACT-002: Sensitive Actuator endpoints are authenticated or network-isolated

**Severity:** Critical  
**Category:** management-security  
**Applies when:** sensitive Actuator endpoints are exposed

### Requirement

The application code and repository-owned configuration must satisfy this behavior when the same artifact runs in either active region.

### Repository evidence to inspect

- `SecurityFilterChain`
- `EndpointRequest`
- `management.server.port`
- `network policy`
- `show-details`

### Finding condition

Emit a finding when evidence shows that sensitive management endpoints are exposed without demonstrated access control or isolation.

### Evaluation guidance

- Cite file path, symbol or property, and line range when available.
- Distinguish explicit application behavior from framework defaults.
- If evidence is missing or ambiguous, return `not_assessed`, not `non_compliant`.
- Do not create an infrastructure finding or assume external platform topology is incorrect.
- Do not emit the control when its applicability condition is not met.

### Recommended remediation scope

Recommend application code, repository-owned application configuration, health behavior, error handling, telemetry, or automated-test changes only.

---

## APP-ACT-003: Actuator health detail disclosure is appropriate for its audience

**Severity:** Medium  
**Category:** management-security  
**Applies when:** Actuator health is exposed

### Requirement

The application code and repository-owned configuration must satisfy this behavior when the same artifact runs in either active region.

### Repository evidence to inspect

- `management.endpoint.health.show-details`
- `show-components`
- `roles`

### Finding condition

Emit a finding when evidence shows that health output available to untrusted callers can reveal dependency names, endpoints, exception details, or topology.

### Evaluation guidance

- Cite file path, symbol or property, and line range when available.
- Distinguish explicit application behavior from framework defaults.
- If evidence is missing or ambiguous, return `not_assessed`, not `non_compliant`.
- Do not create an infrastructure finding or assume external platform topology is incorrect.
- Do not emit the control when its applicability condition is not met.

### Recommended remediation scope

Recommend application code, repository-owned application configuration, health behavior, error handling, telemetry, or automated-test changes only.

---

## APP-LOG-001: Credentials, tokens, secrets, and connection strings are not logged

**Severity:** Critical  
**Category:** logging-security  
**Applies when:** always

### Requirement

The application code and repository-owned configuration must satisfy this behavior when the same artifact runs in either active region.

### Repository evidence to inspect

- `log.debug`
- `log.info`
- `log.error`
- `connection string`
- `Authorization header`
- `credential object`
- `token`
- `password`

### Finding condition

Emit a finding when evidence shows that code logs secrets, tokens, credentials, authorization headers, full connection strings, or unredacted sensitive configuration.

### Evaluation guidance

- Cite file path, symbol or property, and line range when available.
- Distinguish explicit application behavior from framework defaults.
- If evidence is missing or ambiguous, return `not_assessed`, not `non_compliant`.
- Do not create an infrastructure finding or assume external platform topology is incorrect.
- Do not emit the control when its applicability condition is not met.

### Recommended remediation scope

Recommend application code, repository-owned application configuration, health behavior, error handling, telemetry, or automated-test changes only.

---

## APP-LOG-002: Sensitive values are masked before structured logging

**Severity:** High  
**Category:** logging-security  
**Applies when:** always

### Requirement

The application code and repository-owned configuration must satisfy this behavior when the same artifact runs in either active region.

### Repository evidence to inspect

- `mask`
- `redact`
- `sanitize`
- `MDC`
- `structured logger`
- `toString`

### Finding condition

Emit a finding when evidence shows that sensitive objects or configuration can be serialized or emitted without field-level masking.

### Evaluation guidance

- Cite file path, symbol or property, and line range when available.
- Distinguish explicit application behavior from framework defaults.
- If evidence is missing or ambiguous, return `not_assessed`, not `non_compliant`.
- Do not create an infrastructure finding or assume external platform topology is incorrect.
- Do not emit the control when its applicability condition is not met.

### Recommended remediation scope

Recommend application code, repository-owned application configuration, health behavior, error handling, telemetry, or automated-test changes only.

---

## APP-WEB-001: Exception advice matches the active servlet or reactive web model

**Severity:** High  
**Category:** web-error-handling  
**Applies when:** always

### Requirement

The application code and repository-owned configuration must satisfy this behavior when the same artifact runs in either active region.

### Repository evidence to inspect

- `@ControllerAdvice`
- `@RestControllerAdvice`
- `WebExceptionHandler`
- `ErrorWebExceptionHandler`
- `Mono`
- `Flux`
- `spring-boot-starter-web`
- `spring-boot-starter-webflux`

### Finding condition

Emit a finding when evidence shows that exception handling relies on servlet-only assumptions in a reactive path, reactive-only handling in a servlet path, or mixed-stack precedence leaves errors unmapped.

### Evaluation guidance

- Cite file path, symbol or property, and line range when available.
- Distinguish explicit application behavior from framework defaults.
- If evidence is missing or ambiguous, return `not_assessed`, not `non_compliant`.
- Do not create an infrastructure finding or assume external platform topology is incorrect.
- Do not emit the control when its applicability condition is not met.

### Recommended remediation scope

Recommend application code, repository-owned application configuration, health behavior, error handling, telemetry, or automated-test changes only.

---

## APP-WEB-002: Dependency failures map to stable, caller-visible error semantics

**Severity:** High  
**Category:** web-error-handling  
**Applies when:** always

### Requirement

The application code and repository-owned configuration must satisfy this behavior when the same artifact runs in either active region.

### Repository evidence to inspect

- `@ExceptionHandler`
- `ResponseStatusException`
- `HTTP 503`
- `ProblemDetail`
- `onErrorMap`

### Finding condition

Emit a finding when evidence shows that dependency failure is returned as success, not found, validation failure, or an inconsistent status that prevents safe caller retry.

### Evaluation guidance

- Cite file path, symbol or property, and line range when available.
- Distinguish explicit application behavior from framework defaults.
- If evidence is missing or ambiguous, return `not_assessed`, not `non_compliant`.
- Do not create an infrastructure finding or assume external platform topology is incorrect.
- Do not emit the control when its applicability condition is not met.

### Recommended remediation scope

Recommend application code, repository-owned application configuration, health behavior, error handling, telemetry, or automated-test changes only.

---

# Standard finding format

- **Title:** [specific code-level gap]
- **Primary control:** [control ID]
- **Related controls:** [control IDs]
- **Severity:** [severity]
- **Repository evidence:** [file, symbol/property, lines]
- **Observed behavior:** [what the code/configuration does]
- **Active-active risk:** [regional traffic, recovery, correctness, security, or operational effect]
- **Required code/configuration change:** [specific remediation]
- **Validation test:** [test proving the behavior]
- **Confidence:** [high, medium, low]

# Non-findings

Do not create findings for missing regional resources, platform topology, private endpoints, DNS, capacity, zone redundancy, geo-replication, regional deployment jobs, workflow parity, ACR replication, or PCF. These are excluded from this master application-code assessment version.
