---
schema_version: 1.0.0
document_type: dependency_behavior
service: azure-sql
service_name: Azure SQL
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
- id: SQL-001
  title: JDBC connection string is deployment-injected and points to the regional/listener
    endpoint
  severity: critical
  category: configuration
  evidence_patterns:
  - spring.datasource.url
  - JDBC_URL
  - failover listener
  finding_when: server or region is hardcoded
  emit_on_failure: true
- id: SQL-002
  title: Pool, connect, socket, query, and transaction timeouts are bounded
  severity: critical
  category: resilience
  evidence_patterns:
  - HikariConfig
  - loginTimeout
  - queryTimeout
  - transaction timeout
  finding_when: database work can block beyond failure budget
  emit_on_failure: true
- id: SQL-003
  title: Transient SQL failures use bounded retry at safe transaction boundaries
  severity: critical
  category: resilience
  evidence_patterns:
  - Spring Retry
  - RetryTemplate
  - SQLTransientException
  finding_when: retry is absent or blindly repeats non-idempotent transaction
  emit_on_failure: true
- id: SQL-004
  title: Transactions are idempotent or protected by business uniqueness
  severity: critical
  category: consistency
  evidence_patterns:
  - unique constraint
  - idempotency table
  - transaction key
  finding_when: regional retry can duplicate a committed business operation
  emit_on_failure: true
- id: SQL-005
  title: Connection pool evicts broken connections and recovers without restart
  severity: high
  category: recovery
  evidence_patterns:
  - Hikari validation
  - maxLifetime
  - keepaliveTime
  finding_when: stale connections persist after endpoint or regional recovery
  emit_on_failure: true
- id: SQL-006
  title: Database unavailability affects readiness but not liveness
  severity: critical
  category: health
  evidence_patterns:
  - DataSourceHealthIndicator
  - readiness group
  finding_when: database loss leaves ready or causes restart loop
  emit_on_failure: true
- id: SQL-007
  title: Application handles optimistic concurrency and deadlocks
  severity: high
  category: consistency
  evidence_patterns:
  - '@Version'
  - deadlock retry
  - rowversion
  finding_when: concurrent regional writes silently overwrite data or deadlocks are
    mishandled
  emit_on_failure: true
- id: SQL-008
  title: Tests cover connection loss, failover, unknown commit outcome, retry, and
    recovery
  severity: critical
  category: testing
  evidence_patterns:
  - Testcontainers
  - proxy fault
  - integration test
  finding_when: database failover semantics are untested
  emit_on_failure: true
---

# Azure SQL Active-Active Application Behavior Standard

## Purpose

This dependency-specific standard assesses how a Spring Boot microservice uses Azure SQL when deployed to two active Azure regions. The local regional service endpoint is assumed to exist and be reachable through the approved private networking design.

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

## SQL-001: JDBC connection string is deployment-injected and points to the regional/listener endpoint

**Severity:** Critical  
**Category:** configuration

### Requirement

The application code and configuration must satisfy this behavior when the same artifact runs in either active region.

### Repository evidence to inspect

- `spring.datasource.url`
- `JDBC_URL`
- `failover listener`

### Finding condition

Emit a finding when evidence shows that server or region is hardcoded.

### Evidence rule

Cite the file path, symbol, property, and line range when available. If the repository does not contain enough evidence, return `not_assessed` rather than assuming noncompliance.

---

## SQL-002: Pool, connect, socket, query, and transaction timeouts are bounded

**Severity:** Critical  
**Category:** resilience

### Requirement

The application code and configuration must satisfy this behavior when the same artifact runs in either active region.

### Repository evidence to inspect

- `HikariConfig`
- `loginTimeout`
- `queryTimeout`
- `transaction timeout`

### Finding condition

Emit a finding when evidence shows that database work can block beyond failure budget.

### Evidence rule

Cite the file path, symbol, property, and line range when available. If the repository does not contain enough evidence, return `not_assessed` rather than assuming noncompliance.

---

## SQL-003: Transient SQL failures use bounded retry at safe transaction boundaries

**Severity:** Critical  
**Category:** resilience

### Requirement

The application code and configuration must satisfy this behavior when the same artifact runs in either active region.

### Repository evidence to inspect

- `Spring Retry`
- `RetryTemplate`
- `SQLTransientException`

### Finding condition

Emit a finding when evidence shows that retry is absent or blindly repeats non-idempotent transaction.

### Evidence rule

Cite the file path, symbol, property, and line range when available. If the repository does not contain enough evidence, return `not_assessed` rather than assuming noncompliance.

---

## SQL-004: Transactions are idempotent or protected by business uniqueness

**Severity:** Critical  
**Category:** consistency

### Requirement

The application code and configuration must satisfy this behavior when the same artifact runs in either active region.

### Repository evidence to inspect

- `unique constraint`
- `idempotency table`
- `transaction key`

### Finding condition

Emit a finding when evidence shows that regional retry can duplicate a committed business operation.

### Evidence rule

Cite the file path, symbol, property, and line range when available. If the repository does not contain enough evidence, return `not_assessed` rather than assuming noncompliance.

---

## SQL-005: Connection pool evicts broken connections and recovers without restart

**Severity:** High  
**Category:** recovery

### Requirement

The application code and configuration must satisfy this behavior when the same artifact runs in either active region.

### Repository evidence to inspect

- `Hikari validation`
- `maxLifetime`
- `keepaliveTime`

### Finding condition

Emit a finding when evidence shows that stale connections persist after endpoint or regional recovery.

### Evidence rule

Cite the file path, symbol, property, and line range when available. If the repository does not contain enough evidence, return `not_assessed` rather than assuming noncompliance.

---

## SQL-006: Database unavailability affects readiness but not liveness

**Severity:** Critical  
**Category:** health

### Requirement

The application code and configuration must satisfy this behavior when the same artifact runs in either active region.

### Repository evidence to inspect

- `DataSourceHealthIndicator`
- `readiness group`

### Finding condition

Emit a finding when evidence shows that database loss leaves ready or causes restart loop.

### Evidence rule

Cite the file path, symbol, property, and line range when available. If the repository does not contain enough evidence, return `not_assessed` rather than assuming noncompliance.

---

## SQL-007: Application handles optimistic concurrency and deadlocks

**Severity:** High  
**Category:** consistency

### Requirement

The application code and configuration must satisfy this behavior when the same artifact runs in either active region.

### Repository evidence to inspect

- `@Version`
- `deadlock retry`
- `rowversion`

### Finding condition

Emit a finding when evidence shows that concurrent regional writes silently overwrite data or deadlocks are mishandled.

### Evidence rule

Cite the file path, symbol, property, and line range when available. If the repository does not contain enough evidence, return `not_assessed` rather than assuming noncompliance.

---

## SQL-008: Tests cover connection loss, failover, unknown commit outcome, retry, and recovery

**Severity:** Critical  
**Category:** testing

### Requirement

The application code and configuration must satisfy this behavior when the same artifact runs in either active region.

### Repository evidence to inspect

- `Testcontainers`
- `proxy fault`
- `integration test`

### Finding condition

Emit a finding when evidence shows that database failover semantics are untested.

### Evidence rule

Cite the file path, symbol, property, and line range when available. If the repository does not contain enough evidence, return `not_assessed` rather than assuming noncompliance.

---

# Standard finding format

- **Title:** [specific code-level gap]
- **Control:** [SQL-NNN]
- **Severity:** [severity]
- **Repository evidence:** [file, symbol/property, line]
- **Observed behavior:** [what code currently does]
- **Active-active risk:** [effect during regional dependency or network failure]
- **Required code/configuration change:** [specific remediation]
- **Validation test:** [test that proves the behavior]

# Non-findings

Do not create infrastructure findings such as missing second-region resources, private endpoints, zone redundancy, geo-replication, capacity, DNS, or global load-balancer configuration. Those are assumed platform responsibilities and are outside this repository assessment.
