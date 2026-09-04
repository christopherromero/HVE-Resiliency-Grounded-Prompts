---
schema_version: 1.0.0
document_type: dependency_behavior
service: postgresql
service_name: PostgreSQL
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
- id: PG-001
  title: JDBC endpoint is deployment-injected and local-region appropriate
  severity: critical
  category: configuration
  evidence_patterns:
  - spring.datasource.url
  - PGHOST
  - JDBC_URL
  finding_when: host or region is hardcoded
  emit_on_failure: true
- id: PG-002
  title: Connection, socket, statement, lock, and transaction timeouts are bounded
  severity: critical
  category: resilience
  evidence_patterns:
  - connectTimeout
  - socketTimeout
  - statement_timeout
  - lock_timeout
  finding_when: database operations can hang beyond failure budget
  emit_on_failure: true
- id: PG-003
  title: Transient retry occurs only at idempotent transaction boundaries
  severity: critical
  category: resilience
  evidence_patterns:
  - PSQLException
  - SQLState
  - retry template
  finding_when: retry is absent or repeats ambiguous/non-idempotent work
  emit_on_failure: true
- id: PG-004
  title: Writes use idempotency and optimistic/pessimistic concurrency appropriately
  severity: critical
  category: consistency
  evidence_patterns:
  - ON CONFLICT
  - unique constraint
  - '@Version'
  - advisory lock
  finding_when: concurrent multi-region processing corrupts or duplicates state
  emit_on_failure: true
- id: PG-005
  title: Pool invalidates failed connections and reconnects after endpoint recovery
  severity: high
  category: recovery
  evidence_patterns:
  - HikariCP
  - validationTimeout
  - maxLifetime
  finding_when: recovery requires application restart
  emit_on_failure: true
- id: PG-006
  title: Critical database failure affects readiness but not liveness
  severity: critical
  category: health
  evidence_patterns:
  - DataSourceHealthIndicator
  - readiness group
  finding_when: readiness/liveness semantics are incorrect
  emit_on_failure: true
- id: PG-007
  title: Read-after-write and replica-lag assumptions are explicit
  severity: high
  category: consistency
  evidence_patterns:
  - read routing
  - transaction isolation
  - replica lag
  finding_when: code assumes immediate consistency when reads may use a replica
  emit_on_failure: true
- id: PG-008
  title: Tests cover failover, serialization/deadlock errors, ambiguous commit, and
    recovery
  severity: critical
  category: testing
  evidence_patterns:
  - Testcontainers PostgreSQL
  - Toxiproxy
  - integration tests
  finding_when: PostgreSQL recovery behavior is untested
  emit_on_failure: true
---

# PostgreSQL Active-Active Application Behavior Standard

## Purpose

This dependency-specific standard assesses how a Spring Boot microservice uses PostgreSQL when deployed to two active Azure regions. The local regional service endpoint is assumed to exist and be reachable through the approved private networking design.

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

## PG-001: JDBC endpoint is deployment-injected and local-region appropriate

**Severity:** Critical  
**Category:** configuration

### Requirement

The application code and configuration must satisfy this behavior when the same artifact runs in either active region.

### Repository evidence to inspect

- `spring.datasource.url`
- `PGHOST`
- `JDBC_URL`

### Finding condition

Emit a finding when evidence shows that host or region is hardcoded.

### Evidence rule

Cite the file path, symbol, property, and line range when available. If the repository does not contain enough evidence, return `not_assessed` rather than assuming noncompliance.

---

## PG-002: Connection, socket, statement, lock, and transaction timeouts are bounded

**Severity:** Critical  
**Category:** resilience

### Requirement

The application code and configuration must satisfy this behavior when the same artifact runs in either active region.

### Repository evidence to inspect

- `connectTimeout`
- `socketTimeout`
- `statement_timeout`
- `lock_timeout`

### Finding condition

Emit a finding when evidence shows that database operations can hang beyond failure budget.

### Evidence rule

Cite the file path, symbol, property, and line range when available. If the repository does not contain enough evidence, return `not_assessed` rather than assuming noncompliance.

---

## PG-003: Transient retry occurs only at idempotent transaction boundaries

**Severity:** Critical  
**Category:** resilience

### Requirement

The application code and configuration must satisfy this behavior when the same artifact runs in either active region.

### Repository evidence to inspect

- `PSQLException`
- `SQLState`
- `retry template`

### Finding condition

Emit a finding when evidence shows that retry is absent or repeats ambiguous/non-idempotent work.

### Evidence rule

Cite the file path, symbol, property, and line range when available. If the repository does not contain enough evidence, return `not_assessed` rather than assuming noncompliance.

---

## PG-004: Writes use idempotency and optimistic/pessimistic concurrency appropriately

**Severity:** Critical  
**Category:** consistency

### Requirement

The application code and configuration must satisfy this behavior when the same artifact runs in either active region.

### Repository evidence to inspect

- `ON CONFLICT`
- `unique constraint`
- `@Version`
- `advisory lock`

### Finding condition

Emit a finding when evidence shows that concurrent multi-region processing corrupts or duplicates state.

### Evidence rule

Cite the file path, symbol, property, and line range when available. If the repository does not contain enough evidence, return `not_assessed` rather than assuming noncompliance.

---

## PG-005: Pool invalidates failed connections and reconnects after endpoint recovery

**Severity:** High  
**Category:** recovery

### Requirement

The application code and configuration must satisfy this behavior when the same artifact runs in either active region.

### Repository evidence to inspect

- `HikariCP`
- `validationTimeout`
- `maxLifetime`

### Finding condition

Emit a finding when evidence shows that recovery requires application restart.

### Evidence rule

Cite the file path, symbol, property, and line range when available. If the repository does not contain enough evidence, return `not_assessed` rather than assuming noncompliance.

---

## PG-006: Critical database failure affects readiness but not liveness

**Severity:** Critical  
**Category:** health

### Requirement

The application code and configuration must satisfy this behavior when the same artifact runs in either active region.

### Repository evidence to inspect

- `DataSourceHealthIndicator`
- `readiness group`

### Finding condition

Emit a finding when evidence shows that readiness/liveness semantics are incorrect.

### Evidence rule

Cite the file path, symbol, property, and line range when available. If the repository does not contain enough evidence, return `not_assessed` rather than assuming noncompliance.

---

## PG-007: Read-after-write and replica-lag assumptions are explicit

**Severity:** High  
**Category:** consistency

### Requirement

The application code and configuration must satisfy this behavior when the same artifact runs in either active region.

### Repository evidence to inspect

- `read routing`
- `transaction isolation`
- `replica lag`

### Finding condition

Emit a finding when evidence shows that code assumes immediate consistency when reads may use a replica.

### Evidence rule

Cite the file path, symbol, property, and line range when available. If the repository does not contain enough evidence, return `not_assessed` rather than assuming noncompliance.

---

## PG-008: Tests cover failover, serialization/deadlock errors, ambiguous commit, and recovery

**Severity:** Critical  
**Category:** testing

### Requirement

The application code and configuration must satisfy this behavior when the same artifact runs in either active region.

### Repository evidence to inspect

- `Testcontainers PostgreSQL`
- `Toxiproxy`
- `integration tests`

### Finding condition

Emit a finding when evidence shows that PostgreSQL recovery behavior is untested.

### Evidence rule

Cite the file path, symbol, property, and line range when available. If the repository does not contain enough evidence, return `not_assessed` rather than assuming noncompliance.

---

# Standard finding format

- **Title:** [specific code-level gap]
- **Control:** [PG-NNN]
- **Severity:** [severity]
- **Repository evidence:** [file, symbol/property, line]
- **Observed behavior:** [what code currently does]
- **Active-active risk:** [effect during regional dependency or network failure]
- **Required code/configuration change:** [specific remediation]
- **Validation test:** [test that proves the behavior]

# Non-findings

Do not create infrastructure findings such as missing second-region resources, private endpoints, zone redundancy, geo-replication, capacity, DNS, or global load-balancer configuration. Those are assumed platform responsibilities and are outside this repository assessment.
