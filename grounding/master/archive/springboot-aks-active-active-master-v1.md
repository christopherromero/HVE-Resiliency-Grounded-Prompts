---
schema_version: 1.0.0
document_type: dependency_behavior
service: springboot_aks_active_active
service_name: Spring Boot on AKS Active-Active Code Assessment
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
- AKS, networking, private endpoints, DNS, identities, certificates, and dependent
  services follow the approved active-active infrastructure design.
- The deployment pipeline injects region-specific configuration into the same application
  artifact.
- The application repository does not provision or validate infrastructure.
controls:
- id: APP-AA-001
  title: One immutable artifact supports both regions
  severity: high
  category: deployability
  evidence_patterns:
  - pom.xml
  - build.gradle
  - Dockerfile
  - environment placeholders
  finding_when: region-specific code branch, build, artifact, or profile is required
  emit_on_failure: true
- id: APP-AA-002
  title: Regional endpoints are externally configured
  severity: critical
  category: configuration
  evidence_patterns:
  - application.yml
  - application-*.yml
  - ConfigMap references
  - environment variables
  - '@ConfigurationProperties'
  finding_when: a regional endpoint, hostname, vault URI, namespace, account, cluster,
    or region is hardcoded
  emit_on_failure: true
- id: APP-AA-003
  title: Local-region affinity is explicit
  severity: critical
  category: regional-affinity
  evidence_patterns:
  - region variable
  - regional endpoint mapping
  - deployment configuration contract
  finding_when: code can select or default to a remote-region dependency during normal
    operation
  emit_on_failure: true
- id: APP-AA-004
  title: Dependency calls have bounded timeouts
  severity: critical
  category: resilience
  evidence_patterns:
  - Azure SDK client options
  - HTTP client timeout
  - JDBC timeout
  - Kafka timeout
  finding_when: a critical remote call can block indefinitely or beyond the failure-detection
    budget
  emit_on_failure: true
- id: APP-AA-005
  title: Transient failures use bounded retry with backoff
  severity: high
  category: resilience
  evidence_patterns:
  - SDK retry options
  - Spring Retry
  - Resilience4j Retry
  - retry configuration
  finding_when: transient dependency failures are not retried or retry indefinitely
  emit_on_failure: true
- id: APP-AA-006
  title: Repeated failures are isolated by circuit breaking
  severity: high
  category: resilience
  evidence_patterns:
  - Resilience4j CircuitBreaker
  - Spring Cloud CircuitBreaker
  - SDK equivalent
  finding_when: repeated failure can exhaust threads, sockets, or connection pools
  emit_on_failure: true
- id: APP-AA-007
  title: Critical dependency failure affects readiness
  severity: critical
  category: health
  evidence_patterns:
  - HealthIndicator
  - ReactiveHealthIndicator
  - AvailabilityChangeEvent
  - readiness health group
  finding_when: critical dependency remains unavailable after retry exhaustion but
    readiness remains UP
  emit_on_failure: true
- id: APP-AA-008
  title: Liveness is not coupled to external dependencies
  severity: critical
  category: health
  evidence_patterns:
  - liveness health group
  - ApplicationAvailability
  finding_when: external dependency failure restarts otherwise healthy JVMs or creates
    restart loops
  emit_on_failure: true
- id: APP-AA-009
  title: Health checks are bounded and representative
  severity: high
  category: health
  evidence_patterns:
  - health groups
  - probe timeout
  - cached health state
  - synthetic operation
  finding_when: health check can hang, overload a dependency, or succeed without testing
    the request-serving path
  emit_on_failure: true
- id: APP-AA-010
  title: Application state is region independent
  severity: critical
  category: state
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
  evidence_patterns:
  - idempotency key
  - deduplication store
  - unique constraint
  - processed-event store
  finding_when: retry, replay, or cross-region duplicate can create duplicate business
    effects
  emit_on_failure: true
- id: APP-AA-012
  title: Concurrency and conflict behavior is defined
  severity: high
  category: consistency
  evidence_patterns:
  - ETag
  - optimistic locking
  - version field
  - conflict handler
  finding_when: simultaneous writes from both regions can silently overwrite or corrupt
    state
  emit_on_failure: true
- id: APP-AA-013
  title: Startup tolerates temporary dependency unavailability
  severity: high
  category: startup
  evidence_patterns:
  - lazy initialization
  - startup retry
  - readiness transition
  finding_when: temporary dependency outage causes permanent startup failure or crash
    loop
  emit_on_failure: true
- id: APP-AA-014
  title: Recovery occurs without process restart
  severity: high
  category: recovery
  evidence_patterns:
  - connection recreation
  - credential refresh
  - circuit half-open
  - client lifecycle
  finding_when: application cannot reconnect after dependency or network recovery
  emit_on_failure: true
- id: APP-AA-015
  title: Regional identity is present in telemetry
  severity: medium
  category: observability
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
  evidence_patterns:
  - metrics
  - structured logs
  - alerts
  - health details
  finding_when: retry exhaustion or critical dependency loss produces no actionable
    signal for regional traffic management
  emit_on_failure: true
- id: APP-AA-017
  title: Graceful shutdown and traffic draining are implemented
  severity: high
  category: lifecycle
  evidence_patterns:
  - server.shutdown
  - preStop awareness
  - termination grace handling
  finding_when: pod termination interrupts in-flight work or accepts traffic while
    shutting down
  emit_on_failure: true
- id: APP-AA-018
  title: Active-active failure behavior is tested
  severity: critical
  category: testing
  evidence_patterns:
  - unit tests
  - integration tests
  - fault injection
  - Testcontainers
  - WireMock
  finding_when: no automated test demonstrates timeout, retry, health transition,
    idempotency, and recovery behavior
  emit_on_failure: true
---

# Spring Boot on AKS Active-Active Code Assessment Active-Active Application Behavior Standard

## Purpose

This master standard assesses whether Java Spring Boot microservices are coded and configured to operate safely as the same immutable artifact in two simultaneously active Azure regions. It assumes regional infrastructure is already deployed according to the approved architecture.

## Scope boundary

This standard assesses **application code, application configuration checked into the repository, and automated tests only**. It does not assess whether Azure or third-party infrastructure has been deployed correctly.

## Mandatory assumptions

- Two independent Azure regions are provisioned and active.
- AKS, networking, private endpoints, DNS, identities, certificates, and dependent services follow the approved active-active infrastructure design.
- The deployment pipeline injects region-specific configuration into the same application artifact.
- The application repository does not provision or validate infrastructure.

## Evaluator workflow

1. Confirm the dependency is actually used by production code.
2. Locate client construction, configuration binding, error handling, health integration, telemetry, and tests.
3. Evaluate only controls supported by repository evidence.
4. Separate framework defaults from explicit application behavior. Flag reliance on a default only when the assessment requires explicit configuration or the default does not meet the failure budget.
5. Do not recommend deploying infrastructure. Recommend application code, configuration contract, health behavior, telemetry, or testing changes.
6. Link each finding to exactly one primary control and list related controls separately.
7. Do not emit a finding for a dependency that is not used.

## Required statuses

- `compliant`: Repository evidence demonstrates the behavior.
- `non_compliant`: Repository evidence demonstrates a gap.
- `not_assessed`: Evidence is unavailable or insufficient.
- `not_applicable`: The dependency or behavior does not apply.
- `accepted_risk`: A cited approved exception exists.

# Controls

## APP-AA-001: One immutable artifact supports both regions

**Severity:** High  
**Category:** deployability

### Requirement

The application code and configuration must satisfy this behavior when the same artifact runs in either active region.

### Repository evidence to inspect

- `pom.xml`
- `build.gradle`
- `Dockerfile`
- `environment placeholders`

### Finding condition

Emit a finding when evidence shows that region-specific code branch, build, artifact, or profile is required.

### Evidence rule

Cite the file path, symbol, property, and line range when available. If the repository does not contain enough evidence, return `not_assessed` rather than assuming noncompliance.

---

## APP-AA-002: Regional endpoints are externally configured

**Severity:** Critical  
**Category:** configuration

### Requirement

The application code and configuration must satisfy this behavior when the same artifact runs in either active region.

### Repository evidence to inspect

- `application.yml`
- `application-*.yml`
- `ConfigMap references`
- `environment variables`
- `@ConfigurationProperties`

### Finding condition

Emit a finding when evidence shows that a regional endpoint, hostname, vault URI, namespace, account, cluster, or region is hardcoded.

### Evidence rule

Cite the file path, symbol, property, and line range when available. If the repository does not contain enough evidence, return `not_assessed` rather than assuming noncompliance.

---

## APP-AA-003: Local-region affinity is explicit

**Severity:** Critical  
**Category:** regional-affinity

### Requirement

The application code and configuration must satisfy this behavior when the same artifact runs in either active region.

### Repository evidence to inspect

- `region variable`
- `regional endpoint mapping`
- `deployment configuration contract`

### Finding condition

Emit a finding when evidence shows that code can select or default to a remote-region dependency during normal operation.

### Evidence rule

Cite the file path, symbol, property, and line range when available. If the repository does not contain enough evidence, return `not_assessed` rather than assuming noncompliance.

---

## APP-AA-004: Dependency calls have bounded timeouts

**Severity:** Critical  
**Category:** resilience

### Requirement

The application code and configuration must satisfy this behavior when the same artifact runs in either active region.

### Repository evidence to inspect

- `Azure SDK client options`
- `HTTP client timeout`
- `JDBC timeout`
- `Kafka timeout`

### Finding condition

Emit a finding when evidence shows that a critical remote call can block indefinitely or beyond the failure-detection budget.

### Evidence rule

Cite the file path, symbol, property, and line range when available. If the repository does not contain enough evidence, return `not_assessed` rather than assuming noncompliance.

---

## APP-AA-005: Transient failures use bounded retry with backoff

**Severity:** High  
**Category:** resilience

### Requirement

The application code and configuration must satisfy this behavior when the same artifact runs in either active region.

### Repository evidence to inspect

- `SDK retry options`
- `Spring Retry`
- `Resilience4j Retry`
- `retry configuration`

### Finding condition

Emit a finding when evidence shows that transient dependency failures are not retried or retry indefinitely.

### Evidence rule

Cite the file path, symbol, property, and line range when available. If the repository does not contain enough evidence, return `not_assessed` rather than assuming noncompliance.

---

## APP-AA-006: Repeated failures are isolated by circuit breaking

**Severity:** High  
**Category:** resilience

### Requirement

The application code and configuration must satisfy this behavior when the same artifact runs in either active region.

### Repository evidence to inspect

- `Resilience4j CircuitBreaker`
- `Spring Cloud CircuitBreaker`
- `SDK equivalent`

### Finding condition

Emit a finding when evidence shows that repeated failure can exhaust threads, sockets, or connection pools.

### Evidence rule

Cite the file path, symbol, property, and line range when available. If the repository does not contain enough evidence, return `not_assessed` rather than assuming noncompliance.

---

## APP-AA-007: Critical dependency failure affects readiness

**Severity:** Critical  
**Category:** health

### Requirement

The application code and configuration must satisfy this behavior when the same artifact runs in either active region.

### Repository evidence to inspect

- `HealthIndicator`
- `ReactiveHealthIndicator`
- `AvailabilityChangeEvent`
- `readiness health group`

### Finding condition

Emit a finding when evidence shows that critical dependency remains unavailable after retry exhaustion but readiness remains UP.

### Evidence rule

Cite the file path, symbol, property, and line range when available. If the repository does not contain enough evidence, return `not_assessed` rather than assuming noncompliance.

---

## APP-AA-008: Liveness is not coupled to external dependencies

**Severity:** Critical  
**Category:** health

### Requirement

The application code and configuration must satisfy this behavior when the same artifact runs in either active region.

### Repository evidence to inspect

- `liveness health group`
- `ApplicationAvailability`

### Finding condition

Emit a finding when evidence shows that external dependency failure restarts otherwise healthy JVMs or creates restart loops.

### Evidence rule

Cite the file path, symbol, property, and line range when available. If the repository does not contain enough evidence, return `not_assessed` rather than assuming noncompliance.

---

## APP-AA-009: Health checks are bounded and representative

**Severity:** High  
**Category:** health

### Requirement

The application code and configuration must satisfy this behavior when the same artifact runs in either active region.

### Repository evidence to inspect

- `health groups`
- `probe timeout`
- `cached health state`
- `synthetic operation`

### Finding condition

Emit a finding when evidence shows that health check can hang, overload a dependency, or succeed without testing the request-serving path.

### Evidence rule

Cite the file path, symbol, property, and line range when available. If the repository does not contain enough evidence, return `not_assessed` rather than assuming noncompliance.

---

## APP-AA-010: Application state is region independent

**Severity:** Critical  
**Category:** state

### Requirement

The application code and configuration must satisfy this behavior when the same artifact runs in either active region.

### Repository evidence to inspect

- `HTTP session configuration`
- `local file writes`
- `in-memory maps`
- `cache configuration`

### Finding condition

Emit a finding when evidence shows that correct processing or session continuity depends on pod-local or region-local volatile state.

### Evidence rule

Cite the file path, symbol, property, and line range when available. If the repository does not contain enough evidence, return `not_assessed` rather than assuming noncompliance.

---

## APP-AA-011: Mutating operations are idempotent

**Severity:** Critical  
**Category:** consistency

### Requirement

The application code and configuration must satisfy this behavior when the same artifact runs in either active region.

### Repository evidence to inspect

- `idempotency key`
- `deduplication store`
- `unique constraint`
- `processed-event store`

### Finding condition

Emit a finding when evidence shows that retry, replay, or cross-region duplicate can create duplicate business effects.

### Evidence rule

Cite the file path, symbol, property, and line range when available. If the repository does not contain enough evidence, return `not_assessed` rather than assuming noncompliance.

---

## APP-AA-012: Concurrency and conflict behavior is defined

**Severity:** High  
**Category:** consistency

### Requirement

The application code and configuration must satisfy this behavior when the same artifact runs in either active region.

### Repository evidence to inspect

- `ETag`
- `optimistic locking`
- `version field`
- `conflict handler`

### Finding condition

Emit a finding when evidence shows that simultaneous writes from both regions can silently overwrite or corrupt state.

### Evidence rule

Cite the file path, symbol, property, and line range when available. If the repository does not contain enough evidence, return `not_assessed` rather than assuming noncompliance.

---

## APP-AA-013: Startup tolerates temporary dependency unavailability

**Severity:** High  
**Category:** startup

### Requirement

The application code and configuration must satisfy this behavior when the same artifact runs in either active region.

### Repository evidence to inspect

- `lazy initialization`
- `startup retry`
- `readiness transition`

### Finding condition

Emit a finding when evidence shows that temporary dependency outage causes permanent startup failure or crash loop.

### Evidence rule

Cite the file path, symbol, property, and line range when available. If the repository does not contain enough evidence, return `not_assessed` rather than assuming noncompliance.

---

## APP-AA-014: Recovery occurs without process restart

**Severity:** High  
**Category:** recovery

### Requirement

The application code and configuration must satisfy this behavior when the same artifact runs in either active region.

### Repository evidence to inspect

- `connection recreation`
- `credential refresh`
- `circuit half-open`
- `client lifecycle`

### Finding condition

Emit a finding when evidence shows that application cannot reconnect after dependency or network recovery.

### Evidence rule

Cite the file path, symbol, property, and line range when available. If the repository does not contain enough evidence, return `not_assessed` rather than assuming noncompliance.

---

## APP-AA-015: Regional identity is present in telemetry

**Severity:** Medium  
**Category:** observability

### Requirement

The application code and configuration must satisfy this behavior when the same artifact runs in either active region.

### Repository evidence to inspect

- `region tag`
- `OpenTelemetry resource attributes`
- `Application Insights dimensions`

### Finding condition

Emit a finding when evidence shows that logs, metrics, traces, and health events cannot identify the serving region.

### Evidence rule

Cite the file path, symbol, property, and line range when available. If the repository does not contain enough evidence, return `not_assessed` rather than assuming noncompliance.

---

## APP-AA-016: Failures generate actionable monitoring signals

**Severity:** Critical  
**Category:** observability

### Requirement

The application code and configuration must satisfy this behavior when the same artifact runs in either active region.

### Repository evidence to inspect

- `metrics`
- `structured logs`
- `alerts`
- `health details`

### Finding condition

Emit a finding when evidence shows that retry exhaustion or critical dependency loss produces no actionable signal for regional traffic management.

### Evidence rule

Cite the file path, symbol, property, and line range when available. If the repository does not contain enough evidence, return `not_assessed` rather than assuming noncompliance.

---

## APP-AA-017: Graceful shutdown and traffic draining are implemented

**Severity:** High  
**Category:** lifecycle

### Requirement

The application code and configuration must satisfy this behavior when the same artifact runs in either active region.

### Repository evidence to inspect

- `server.shutdown`
- `preStop awareness`
- `termination grace handling`

### Finding condition

Emit a finding when evidence shows that pod termination interrupts in-flight work or accepts traffic while shutting down.

### Evidence rule

Cite the file path, symbol, property, and line range when available. If the repository does not contain enough evidence, return `not_assessed` rather than assuming noncompliance.

---

## APP-AA-018: Active-active failure behavior is tested

**Severity:** Critical  
**Category:** testing

### Requirement

The application code and configuration must satisfy this behavior when the same artifact runs in either active region.

### Repository evidence to inspect

- `unit tests`
- `integration tests`
- `fault injection`
- `Testcontainers`
- `WireMock`

### Finding condition

Emit a finding when evidence shows that no automated test demonstrates timeout, retry, health transition, idempotency, and recovery behavior.

### Evidence rule

Cite the file path, symbol, property, and line range when available. If the repository does not contain enough evidence, return `not_assessed` rather than assuming noncompliance.

---

# Standard finding format

- **Title:** [specific code-level gap]
- **Control:** [APP-AA-NNN]
- **Severity:** [severity]
- **Repository evidence:** [file, symbol/property, line]
- **Observed behavior:** [what code currently does]
- **Active-active risk:** [effect during regional dependency or network failure]
- **Required code/configuration change:** [specific remediation]
- **Validation test:** [test that proves the behavior]

# Non-findings

Do not create infrastructure findings such as missing second-region resources, private endpoints, zone redundancy, geo-replication, capacity, DNS, or global load-balancer configuration. Those are assumed platform responsibilities and are outside this repository assessment.
