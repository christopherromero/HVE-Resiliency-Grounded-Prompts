---
schema_version: 2.3.0
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
- id: SQL-009
  title: R2DBC connection acquisition, statement execution, and overall operations
    are bounded
  severity: critical
  category: resilience
  evidence_patterns:
  - spring.r2dbc.pool.acquire-timeout
  - ConnectionPoolConfiguration
  - DatabaseClient
  - R2dbcEntityTemplate
  - statement timeout
  - lock timeout
  - Reactor timeout
  finding_when: reactive connection acquisition, statement execution, lock waits,
    or the composed database operation can exceed the application failure budget
  emit_on_failure: true
- id: SQL-010
  title: R2DBC pool remotely validates connections and recovers after failover
  severity: critical
  category: recovery
  evidence_patterns:
  - spring.r2dbc.pool.validation-query
  - ValidationDepth.REMOTE
  - max-life-time
  - max-idle-time
  - acquire-retry
  - io.r2dbc.pool.ConnectionPool
  finding_when: stale or invalid pooled connections can remain eligible after endpoint
    failover, acquisition recovery is unbounded, or application recovery requires
    a pod restart
  emit_on_failure: true
- id: SQL-011
  title: Reactive transaction boundaries cover publisher execution and subscription
  severity: critical
  category: consistency
  evidence_patterns:
  - ReactiveTransactionManager
  - R2dbcTransactionManager
  - TransactionalOperator
  - '@Transactional'
  - internal subscribe
  - Mono.defer
  finding_when: related reactive writes subscribe separately, use an incompatible
    transaction manager, execute after the transaction scope ends, or escape the transaction
    through an internal subscription
  emit_on_failure: true
- id: SQL-012
  title: Retry handles transient and ambiguous SQL outcomes safely
  severity: critical
  category: resilience
  evidence_patterns:
  - R2dbcTransientResourceException
  - R2dbcRollbackException
  - SQLTransientException
  - commit timeout
  - connection reset during commit
  - Retry.backoff
  - idempotency key
  finding_when: terminal failures are retried, non-idempotent transactions are repeated
    blindly, or an unknown commit outcome is treated as a definite rollback without
    status lookup or reconciliation
  emit_on_failure: true
- id: SQL-013
  title: Cross-store SQL workflows have durable reconciliation
  severity: critical
  category: consistency
  evidence_patterns:
  - SQL and Cosmos
  - SQL and MongoDB
  - SQL and Kafka
  - outbox
  - saga
  - reconciliation status
  - fallback repository
  finding_when: SQL and another store, broker, or external provider can diverge without
    durable intent, terminal status, compensation, outbox, or reconciliation
  emit_on_failure: true
- id: SQL-014
  title: R2DBC driver and pool behavior are supported and regression-tested
  severity: high
  category: compatibility
  evidence_patterns:
  - r2dbc-mssql
  - r2dbc-pool
  - dependencyManagement
  - driver release notes
  - archived dependency
  - failover integration test
  finding_when: the selected driver or pool version is unsupported or materially incompatible,
    or dependency upgrades can alter failover, timeout, transaction, or recovery behavior
    without regression testing
  emit_on_failure: true
- id: SQL-015
  title: Database readiness checks are bounded and topology-aware
  severity: critical
  category: health
  evidence_patterns:
  - DataSourceHealthIndicator
  - ReactiveHealthIndicator
  - SELECT 1
  - management.endpoint.health.group.readiness
  - health timeout
  finding_when: the database health check is unbounded, participates in liveness,
    or gates readiness without evidence that the SQL path is a critical region-local
    serving dependency
  emit_on_failure: true
- id: SQL-016
  title: R2DBC failover and unknown-outcome behavior is tested
  severity: critical
  category: testing
  evidence_patterns:
  - Toxiproxy
  - Testcontainers
  - connection reset
  - stale pooled connection
  - unknown commit outcome
  - endpoint recovery test
  finding_when: tests do not demonstrate bounded failure, pool recovery, safe retry,
    unknown commit handling, and restoration without restart for the effective reactive
    SQL path
  emit_on_failure: true
---

# Azure SQL Target-State Application Behavior Standard

### Shared-service operating-model contract

This standard does not select the application's shared-service topology. Resolve the operating model from:

```text
architecture_context.shared_service_operating_models.services.azure_sql
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

This dependency-specific standard assesses how a Spring Boot microservice uses Azure SQL when evaluated for the approved target operating model supplied by application architecture context. The local regional service endpoint is assumed to exist and be reachable through the approved private networking design.

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

## Dependency-specific quality caveats

- Adding `@Transactional` is not sufficient for reactive work. Verify a compatible reactive transaction manager, publisher composition, and subscription boundary.
- Do not blindly retry non-idempotent work or an operation with an unknown commit outcome.
- A random UUID or timestamp generated per attempt is not a stable idempotency key.
- Do not add every database dependency to readiness, and never add external dependencies to liveness.
- A fallback store must be independently bounded, durable when required, and observable. Distinguish primary failure, fallback success, and dual failure.
- Do not infer Azure SQL Failover Group, private endpoint, DNS, firewall, or regional-replica noncompliance from absent repository evidence.

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

## SQL-009: R2DBC connection acquisition, statement execution, and overall operations are bounded

**Severity:** Critical  
**Category:** resilience

### Requirement

R2DBC connection acquisition, SQL statement execution, lock waits, and the complete reactive database operation must have configurable and mutually consistent bounds. The overall operation deadline must include pool acquisition, connection establishment, execution, retry, and response propagation, and it must remain below the caller or workload deadline.

### Repository evidence to inspect

- `spring.r2dbc.pool.acquire-timeout`
- `ConnectionPoolConfiguration`
- `DatabaseClient`
- `R2dbcEntityTemplate`
- `statement timeout`
- `lock timeout`
- `Reactor timeout`

### Finding condition

Emit a finding when evidence shows that reactive connection acquisition, statement execution, lock waits, or the composed database operation can exceed the application failure budget.

### Evidence rule

Cite the file path, symbol, property, and line range when available. Evaluate effective runtime behavior rather than the presence of an annotation, library, property name, or default alone. If the repository does not contain enough evidence, return `not_assessed` rather than assuming noncompliance.

### Quality caveats

- A driver connect timeout does not prove that pool acquisition, statement execution, or the complete reactive chain is bounded.
- Do not prescribe numeric timeout values without workload evidence. Require external configurability and alignment with request, scheduler, service-mesh, gateway, and load-balancer budgets.
- Do not duplicate SQL-002 when the same root cause affects both JDBC and R2DBC. Use one primary control and list the other as related.

---

## SQL-010: R2DBC pool remotely validates connections and recovers after failover

**Severity:** Critical  
**Category:** recovery

### Requirement

The R2DBC pool must detect connections made invalid by failover, evict or recycle stale connections, bound connection acquisition retries, and restore successful database operations after endpoint recovery without requiring process or pod restart. Validation must exercise the remote database path when local-only validation cannot prove usability.

### Repository evidence to inspect

- `spring.r2dbc.pool.validation-query`
- `ValidationDepth.REMOTE`
- `max-life-time`
- `max-idle-time`
- `acquire-retry`
- `io.r2dbc.pool.ConnectionPool`

### Finding condition

Emit a finding when evidence shows that stale or invalid pooled connections can remain eligible after endpoint failover, acquisition recovery is unbounded, or application recovery requires a pod restart.

### Evidence rule

Cite the file path, symbol, property, and line range when available. Evaluate effective runtime behavior rather than the presence of an annotation, library, property name, or default alone. If the repository does not contain enough evidence, return `not_assessed` rather than assuming noncompliance.

### Quality caveats

- Local validation alone may not prove that a connection can execute against the database after a failover event.
- Maximum lifetime, idle time, validation, and acquisition settings must be configurable and validated with the actual driver and pool versions.
- Do not infer that the Azure SQL Failover Group or DNS configuration is incorrect from repository absence. Record external evidence required.

---

## SQL-011: Reactive transaction boundaries cover publisher execution and subscription

**Severity:** Critical  
**Category:** consistency

### Requirement

Reactive database operations that must commit atomically must use a compatible reactive transaction manager and remain inside one composed publisher and subscription boundary. Error handling must preserve rollback semantics, and controllers or callers must observe terminal success or failure from that same chain.

### Repository evidence to inspect

- `ReactiveTransactionManager`
- `R2dbcTransactionManager`
- `TransactionalOperator`
- `@Transactional`
- `internal subscribe`
- `Mono.defer`

### Finding condition

Emit a finding when evidence shows that related reactive writes subscribe separately, use an incompatible transaction manager, execute after the transaction scope ends, or escape the transaction through an internal subscription.

### Evidence rule

Cite the file path, symbol, property, and line range when available. Evaluate effective runtime behavior rather than the presence of an annotation, library, property name, or default alone. If the repository does not contain enough evidence, return `not_assessed` rather than assuming noncompliance.

### Quality caveats

- Adding `@Transactional` alone is not evidence of an effective reactive transaction. Verify a compatible `ReactiveTransactionManager` or `TransactionalOperator` and publisher execution within the transaction.
- An internal `.subscribe()` normally creates an independent subscription that escapes the caller transaction and error boundary.
- Do not suggest a database transaction as a way to atomically include Kafka, Cosmos DB, HTTP payment providers, or other external systems.

---

## SQL-012: Retry handles transient and ambiguous SQL outcomes safely

**Severity:** Critical  
**Category:** resilience

### Requirement

SQL retries must be limited to classified transient failures and applied at a transactionally safe boundary. When a timeout or connection loss occurs during commit, the application must treat the result as potentially committed until durable operation identity, status lookup, uniqueness, or reconciliation establishes the actual outcome.

### Repository evidence to inspect

- `R2dbcTransientResourceException`
- `R2dbcRollbackException`
- `SQLTransientException`
- `commit timeout`
- `connection reset during commit`
- `Retry.backoff`
- `idempotency key`

### Finding condition

Emit a finding when evidence shows that terminal failures are retried, non-idempotent transactions are repeated blindly, or an unknown commit outcome is treated as a definite rollback without status lookup or reconciliation.

### Evidence rule

Cite the file path, symbol, property, and line range when available. Evaluate effective runtime behavior rather than the presence of an annotation, library, property name, or default alone. If the repository does not contain enough evidence, return `not_assessed` rather than assuming noncompliance.

### Quality caveats

- Do not blindly retry after timeout or connection loss during commit because the transaction may have committed.
- A random UUID or timestamp generated for each attempt is not a stable idempotency key.
- Retry counts and backoff values must remain configurable and fit within the end-to-end operation deadline.

---

## SQL-013: Cross-store SQL workflows have durable reconciliation

**Severity:** Critical  
**Category:** consistency

### Requirement

A workflow spanning SQL and another durable store, broker, or external provider must record stable intent and operation identity, define terminal states, and provide compensation or reconciliation for partial and ambiguous completion. Total failure of both the primary and fallback path must be surfaced and actionable.

### Repository evidence to inspect

- `SQL and Cosmos`
- `SQL and MongoDB`
- `SQL and Kafka`
- `outbox`
- `saga`
- `reconciliation status`
- `fallback repository`

### Finding condition

Emit a finding when evidence shows that SQL and another store, broker, or external provider can diverge without durable intent, terminal status, compensation, outbox, or reconciliation.

### Evidence rule

Cite the file path, symbol, property, and line range when available. Evaluate effective runtime behavior rather than the presence of an annotation, library, property name, or default alone. If the repository does not contain enough evidence, return `not_assessed` rather than assuming noncompliance.

### Quality caveats

- A SQL transaction cannot atomically include Cosmos DB, Kafka, or an external payment provider.
- A fallback store is not resilient when its write is detached, unbounded, or unobservable.
- Distinguish primary failure, fallback success, and dual failure in telemetry and tests.

---

## SQL-014: R2DBC driver and pool behavior are supported and regression-tested

**Severity:** High  
**Category:** compatibility

### Requirement

The application must use supported R2DBC driver and pool versions and protect critical connection, transaction, timeout, and recovery behavior with automated regression tests. Shared BOM or parent upgrades must not silently alter the established database resiliency contract.

### Repository evidence to inspect

- `r2dbc-mssql`
- `r2dbc-pool`
- `dependencyManagement`
- `driver release notes`
- `archived dependency`
- `failover integration test`

### Finding condition

Emit a finding when evidence shows that the selected driver or pool version is unsupported or materially incompatible, or dependency upgrades can alter failover, timeout, transaction, or recovery behavior without regression testing.

### Evidence rule

Cite the file path, symbol, property, and line range when available. Evaluate effective runtime behavior rather than the presence of an annotation, library, property name, or default alone. If the repository does not contain enough evidence, return `not_assessed` rather than assuming noncompliance.

### Quality caveats

- An older version is not automatically noncompliant. Cite maintenance or support evidence and the material application impact.
- Do not recommend a version upgrade without checking Spring Boot, driver, pool, Java, and Azure SQL compatibility.

---

## SQL-015: Database readiness checks are bounded and topology-aware

**Severity:** Critical  
**Category:** health

### Requirement

A database health contributor must perform a lightweight bounded operation that represents the application database path. It may participate in readiness only when the application cannot safely serve without the region-local SQL dependency. It must never participate in liveness.

### Repository evidence to inspect

- `DataSourceHealthIndicator`
- `ReactiveHealthIndicator`
- `SELECT 1`
- `management.endpoint.health.group.readiness`
- `health timeout`

### Finding condition

Emit a finding when evidence shows that the database health check is unbounded, participates in liveness, or gates readiness without evidence that the SQL path is a critical region-local serving dependency.

### Evidence rule

Cite the file path, symbol, property, and line range when available. Evaluate effective runtime behavior rather than the presence of an annotation, library, property name, or default alone. If the repository does not contain enough evidence, return `not_assessed` rather than assuming noncompliance.

### Quality caveats

- Do not add every database or external dependency to readiness automatically.
- If both regions resolve to one shared SQL endpoint, readiness gating can drain both regions simultaneously and requires architecture review.
- Health checks must not create material load, locking, cost, or transaction side effects.

---

## SQL-016: R2DBC failover and unknown-outcome behavior is tested

**Severity:** Critical  
**Category:** testing

### Requirement

Automated validation must cover connection loss before execution, interruption during execution and commit, stale pooled connections after failover, retry classification, idempotent or reconciled ambiguous outcomes, endpoint restoration, and successful recovery without process restart.

### Repository evidence to inspect

- `Toxiproxy`
- `Testcontainers`
- `connection reset`
- `stale pooled connection`
- `unknown commit outcome`
- `endpoint recovery test`

### Finding condition

Emit a finding when evidence shows that tests do not demonstrate bounded failure, pool recovery, safe retry, unknown commit handling, and restoration without restart for the effective reactive SQL path.

### Evidence rule

Cite the file path, symbol, property, and line range when available. Evaluate effective runtime behavior rather than the presence of an annotation, library, property name, or default alone. If the repository does not contain enough evidence, return `not_assessed` rather than assuming noncompliance.

### Quality caveats

- Mock-only tests do not prove driver, pool, socket, DNS, or endpoint-transition behavior.
- Keep infrastructure provisioning outside this finding. The test may simulate a transition while the platform topology remains an external evidence item.


---

# ### SQL-017: Read-write connectivity uses the approved failover-group listener

**Severity:** Critical  
**Category:** connectivity  
**Applies when:** Target connectivity model is `failover_group_listener`.

#### Requirement
Read-write JDBC and R2DBC configuration must resolve to the approved FOG read-write listener and must not name a physical regional logical server. The endpoint must be deployment-injected.

#### Finding condition
Emit a finding when repository evidence hardcodes or constructs a regional logical-server hostname, or bypasses the required listener for ordinary read-write traffic.

#### Evidence and caveats
Inspect `spring.datasource.url`, `spring.r2dbc.url`, `JDBC_URL`, `R2DBC_URL`, configuration binding, and `database.windows.net` hostnames. Do not invent the listener name or report missing FOG deployment as code noncompliance. Changing the effective endpoint requires architecture approval.

### SQL-018: Read-only listener use is explicitly isolated

**Severity:** High  
**Category:** connectivity-and-consistency

Use a FOG read-only listener only for explicitly read-only operations with approved replica-lag and read-after-write semantics. Emit a finding when mutating or correctness-sensitive work can route to the read-only listener. Enabling read-only routing requires product and data approval.

### SQL-019: Pools recover through listener redirection without restart

**Severity:** Critical  
**Category:** recovery

After failover disconnects existing sessions and redirects the listener, pools must evict unusable connections, reconnect within bounded budgets, and recover without redeploying, changing the connection string, or restarting the process. Do not prescribe numeric DNS TTL or pool lifetime values without evidence.

### SQL-020: Tests prove FOG listener failover and ambiguous-commit safety

**Severity:** Critical  
**Category:** testing

Tests must cover connection interruption, stale-pool eviction, listener redirection, bounded reconnect, recovery without configuration change or restart, and safe handling of transactions whose commit outcome is unknown during failover. Mock-only tests do not prove socket, pool, DNS-redirection, or commit-outcome behavior.

Standard finding format

- **Title:** [specific code-level gap]
- **Control:** [SQL-NNN]
- **Severity:** [severity]
- **Repository evidence:** [file, symbol/property, line]
- **Observed behavior:** [what code currently does]
- **Active-active risk:** [effect during regional dependency or network failure]
- **Required code/configuration change:** [specific remediation]
- **Validation test:** [test that proves the behavior]

# Non-findings

Do not create infrastructure findings such as missing second-region resources, private endpoints, zone redundancy, geo-replication, capacity, DNS, or global load-balancer configuration. Those are assumed platform responsibilities and are outside this repository assessment.### Shared-service operating and connectivity contract

Resolve the Azure SQL target operating model from `architecture_context.shared_service_operating_models.services.azure_sql.target` and connectivity from `architecture_context.shared_service_connectivity_contracts.services.azure_sql.target`.

The approved target remains `active_standby`. When connectivity is `failover_group_listener`, read-write JDBC and R2DBC traffic must use the approved FOG read-write listener rather than a regional logical-server hostname. Missing proof of deployed FOG resources is external evidence, not a code finding.
