---
schema_version: 2.2.0
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
- AKS, networking, private endpoints, DNS, identities, certificates, and dependent services follow the
  approved active-active infrastructure design.
- The deployment pipeline injects region-specific configuration into the same application artifact.
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
  business_logic_risk: low
  requires_approval_before_implementation: false
  approval_owner: architecture
  safe_remediation_without_approval:
  - Externalize an existing hardcoded value to configuration while preserving the same effective default.
  - Add or improve metrics, logs, traces, and health details without changing decisions or payload content.
  - Add tests that characterize and lock in current behavior.
  requires_approval_for:
  - Changing the effective database endpoint.
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
  business_logic_risk: severe
  requires_approval_before_implementation: true
  approval_owner: product_and_architecture
  safe_remediation_without_approval:
  - Add query-duration and timeout telemetry.
  - Add tests that demonstrate the current behavior and the failure mode.
  requires_approval_for:
  - Introducing statement, lock, or transaction timeouts that can abort operations currently completing
    successfully.
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
  business_logic_risk: severe
  requires_approval_before_implementation: true
  approval_owner: product
  safe_remediation_without_approval:
  - Add retry and outcome telemetry.
  - Add tests that demonstrate the current behavior and the failure mode.
  requires_approval_for:
  - Adding retry around any transaction that is not proven idempotent.
  - Changing retry boundaries.
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
  business_logic_risk: severe
  requires_approval_before_implementation: true
  approval_owner: product_and_data
  safe_remediation_without_approval:
  - Add conflict and concurrency telemetry.
  - Add tests that demonstrate the current behavior and the failure mode.
  requires_approval_for:
  - Adding optimistic or pessimistic concurrency control that changes which writes succeed.
  - Adding ON CONFLICT behavior.
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
  business_logic_risk: moderate
  requires_approval_before_implementation: false
  approval_owner: architecture
  safe_remediation_without_approval:
  - Add pool and connection-validation telemetry.
  - Add tests that demonstrate the current behavior and the failure mode.
  requires_approval_for:
  - Changing connection lifetime where it affects long-running operations.
- id: PG-006
  title: Critical database failure affects readiness but not liveness
  severity: critical
  category: health
  evidence_patterns:
  - DataSourceHealthIndicator
  - readiness group
  finding_when: readiness/liveness semantics are incorrect
  emit_on_failure: true
  business_logic_risk: severe
  requires_approval_before_implementation: true
  approval_owner: architecture_and_product
  safe_remediation_without_approval:
  - Add dependency-state telemetry.
  - Add tests that demonstrate the current behavior and the failure mode.
  requires_approval_for:
  - Adding the database to readiness.
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
  business_logic_risk: severe
  requires_approval_before_implementation: true
  approval_owner: architecture_and_data
  safe_remediation_without_approval:
  - Add read-routing and replica-lag telemetry.
  - Add tests that demonstrate the current behavior and the failure mode.
  requires_approval_for:
  - Changing read routing between primary and replica.
  - Changing transaction isolation.
- id: PG-008
  title: Tests cover failover, serialization/deadlock errors, ambiguous commit, and recovery
  severity: critical
  category: testing
  evidence_patterns:
  - Testcontainers PostgreSQL
  - Toxiproxy
  - integration tests
  finding_when: PostgreSQL recovery behavior is untested
  emit_on_failure: true
  business_logic_risk: none
  requires_approval_before_implementation: false
  approval_owner: none
  safe_remediation_without_approval:
  - Add tests that demonstrate the current behavior and the failure mode.
  requires_approval_for: []
- id: PG-009
  title: Connection pool is bounded, monitored, and leak-detecting
  severity: high
  category: resource-management
  evidence_patterns:
  - maximumPoolSize
  - leakDetectionThreshold
  - connectionTimeout
  - pool metrics
  finding_when: pool sizing is unbounded or unjustified, leaks are undetected, or saturation cannot be
    observed
  emit_on_failure: true
  business_logic_risk: moderate
  requires_approval_before_implementation: false
  approval_owner: architecture
  safe_remediation_without_approval:
  - Add pool saturation, wait-time, and leak telemetry.
  - Add tests that demonstrate the current behavior and the failure mode.
  requires_approval_for:
  - Reducing pool size where it can reject work currently served.
- id: PG-010
  title: Endpoint resolution and connection lifetime support failover
  severity: high
  category: recovery
  evidence_patterns:
  - dns ttl
  - networkaddress.cache.ttl
  - maxLifetime
  - targetServerType
  finding_when: cached endpoint resolution or long-lived connections keep the application bound to a failed
    endpoint
  emit_on_failure: true
  business_logic_risk: moderate
  requires_approval_before_implementation: false
  approval_owner: platform_and_architecture
  safe_remediation_without_approval:
  - Add endpoint-resolution and connection-age telemetry.
  - Add tests that demonstrate the current behavior and the failure mode.
  requires_approval_for:
  - Changing connection recycling where it interrupts long operations.
- id: PG-011
  title: TLS verification is enabled and certificate material is managed
  severity: critical
  category: security
  evidence_patterns:
  - sslmode
  - sslrootcert
  - verify-full
  - truststore
  finding_when: TLS is disabled, verification is weakened, or certificate material cannot be rotated without
    redeploying the application
  emit_on_failure: true
  business_logic_risk: severe
  requires_approval_before_implementation: true
  approval_owner: security
  safe_remediation_without_approval:
  - Add TLS-mode telemetry.
  - Add tests that demonstrate the current behavior and the failure mode.
  requires_approval_for:
  - Changing sslmode or certificate verification, which can break connectivity or weaken security.
- id: PG-012
  title: Credentials use approved identity with supported rotation
  severity: critical
  category: security
  evidence_patterns:
  - password
  - IAM token
  - credential refresh
  - secret reference
  finding_when: credentials are embedded or logged, or rotation requires restart without an approved contract
  emit_on_failure: true
  business_logic_risk: severe
  requires_approval_before_implementation: true
  approval_owner: security
  safe_remediation_without_approval:
  - Add authentication-failure telemetry with values redacted.
  - Add tests that demonstrate the current behavior and the failure mode.
  requires_approval_for:
  - Changing credential type or authentication flow.
- id: PG-013
  title: Long-running and idle transactions are bounded
  severity: high
  category: resilience
  evidence_patterns:
  - idle_in_transaction_session_timeout
  - transaction timeout
  - '@Transactional timeout'
  finding_when: transactions can remain open indefinitely, holding locks or connections during degradation
  emit_on_failure: true
  business_logic_risk: severe
  requires_approval_before_implementation: true
  approval_owner: product
  safe_remediation_without_approval:
  - Add transaction-duration telemetry.
  - Add tests that demonstrate the current behavior and the failure mode.
  requires_approval_for:
  - Introducing idle or transaction timeouts that can abort legitimate long-running business operations.
- id: PG-014
  title: Large result sets stream with bounded memory
  severity: high
  category: performance
  evidence_patterns:
  - fetchSize
  - setFetchSize
  - cursor
  - stream
  finding_when: queries materialize unbounded result sets in application memory
  emit_on_failure: true
  business_logic_risk: moderate
  requires_approval_before_implementation: false
  approval_owner: architecture
  safe_remediation_without_approval:
  - Add result-size and memory telemetry.
  - Add tests that demonstrate the current behavior and the failure mode.
  requires_approval_for:
  - Changing fetch behavior where it alters transaction scope or resource lifetime.
- id: PG-015
  title: Schema migrations are safe for rolling and multi-instance deployment
  severity: critical
  category: schema
  evidence_patterns:
  - Flyway
  - Liquibase
  - migration lock
  - backward compatible
  finding_when: migrations block startup unsafely, run concurrently without locking, or break compatibility
    with the previously deployed application version
  emit_on_failure: true
  business_logic_risk: severe
  requires_approval_before_implementation: true
  approval_owner: data_and_product
  safe_remediation_without_approval:
  - Add migration-execution telemetry.
  - Add tests that demonstrate the current behavior and the failure mode.
  requires_approval_for:
  - Any schema migration change, ordering change, or locking change.
- id: PG-016
  title: Dual writes to the database and messaging use durable reconciliation
  severity: critical
  category: consistency
  evidence_patterns:
  - outbox
  - transactional publish
  - after commit
  - reconciliation
  finding_when: a database commit and a message publish can diverge without an outbox, compensation, or
    reconciliation path
  emit_on_failure: true
  business_logic_risk: severe
  requires_approval_before_implementation: true
  approval_owner: architecture_and_product
  safe_remediation_without_approval:
  - Add divergence-detection telemetry between commit and publish.
  - Add tests that demonstrate the current behavior and the failure mode.
  requires_approval_for:
  - Introducing an outbox or post-commit publish, which changes transaction boundaries and event timing.
- id: PG-017
  title: Identity and sequence generation are safe for concurrent instances
  severity: high
  category: consistency
  evidence_patterns:
  - sequence
  - identity
  - uuid
  - allocationSize
  finding_when: identifier generation can collide, reuse values, or depend on single-instance assumptions
  emit_on_failure: true
  business_logic_risk: severe
  requires_approval_before_implementation: true
  approval_owner: data_and_partner_contract
  safe_remediation_without_approval:
  - Add identifier-collision telemetry.
  - Add tests that demonstrate the current behavior and the failure mode.
  requires_approval_for:
  - Changing identifier generation strategy, format, or allocation.
- id: PG-018
  title: Batch operations bound size and handle partial failure
  severity: high
  category: consistency
  evidence_patterns:
  - batch update
  - saveAll
  - rewriteBatchedInserts
  - partial failure
  finding_when: batch operations are unbounded or partial failure is treated as full success
  emit_on_failure: true
  business_logic_risk: moderate
  requires_approval_before_implementation: false
  approval_owner: product
  safe_remediation_without_approval:
  - Add per-item batch outcome telemetry.
  - Add tests that demonstrate the current behavior and the failure mode.
  requires_approval_for:
  - Changing batch size where lock duration or partial-failure behavior changes.
- id: PG-019
  title: SQL logging and diagnostics exclude sensitive data
  severity: critical
  category: security
  evidence_patterns:
  - show-sql
  - log parameters
  - PII
  - bind values
  finding_when: SQL logging can emit personal data, credentials, or full bind parameters
  emit_on_failure: true
  business_logic_risk: low
  requires_approval_before_implementation: false
  approval_owner: security
  safe_remediation_without_approval:
  - Add or strengthen redaction.
  - Add or improve metrics, logs, traces, and health details without changing decisions or payload content.
  - Add tests that characterize and lock in current behavior.
  requires_approval_for:
  - Weakening existing redaction.
- id: PG-020
  title: Prepared-statement behavior is compatible with the connection path
  severity: medium
  category: compatibility
  evidence_patterns:
  - prepareThreshold
  - preparedStatementCacheQueries
  - pgbouncer
  - transaction pooling
  finding_when: server-side prepared statement behavior is incompatible with the effective connection
    pooling path
  emit_on_failure: true
  business_logic_risk: moderate
  requires_approval_before_implementation: false
  approval_owner: platform_and_architecture
  safe_remediation_without_approval:
  - Add prepared-statement telemetry.
  - Add tests that demonstrate the current behavior and the failure mode.
  requires_approval_for:
  - Changing prepared-statement settings where pooler compatibility or plan behavior changes.
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

# PostgreSQL Target-State Application Behavior Standard

### Shared-service operating-model contract

This standard does not select the application's shared-service topology. Resolve the operating model from:

```text
architecture_context.shared_service_operating_models.services.postgresql
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

This dependency-specific standard assesses how a Spring Boot microservice uses PostgreSQL when evaluated for the approved target operating model supplied by application architecture context. The local regional service endpoint is assumed to exist and be reachable through the approved private networking design.

## Scope boundary

This standard assesses **application code, application configuration checked into the repository, and automated tests only**. It does not assess whether Azure or third-party infrastructure has been deployed correctly.

## Mandatory assumptions

- Two independent Azure regions are provisioned and active.
- AKS, networking, private endpoints, DNS, identities, certificates, and dependent services follow the approved active-active infrastructure design.
- The deployment pipeline injects region-specific configuration into the same application artifact.
- The application repository does not provision or validate infrastructure.

## Evaluator workflow

- Confirm the dependency is actually used by production code.
- Resolve source and target models from `architecture_context.shared_service_operating_models.services.postgresql` before evaluating model-specific controls.
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

### PG-001: JDBC endpoint is deployment-injected and local-region appropriate

**Severity:** Critical  
**Category:** configuration

#### Requirement

The application code and configuration must satisfy this behavior when the same artifact runs in either active region.

#### Repository evidence to inspect

- `spring.datasource.url`
- `PGHOST`
- `JDBC_URL`

#### Finding condition

Emit a finding when evidence shows that host or region is hardcoded.

#### Evidence rule

Cite the file path, symbol or property, and advisory line range when available. Evaluate effective behavior rather than the presence of a library, annotation, or property alone. If the repository does not contain enough evidence, return `not_assessed` rather than assuming noncompliance.

#### Business-logic risk

**Risk level:** `low`  
**Requires approval before implementation:** `false`  
**Approval owner:** `architecture`

**Safe remediation without approval:**

- Externalize an existing hardcoded value to configuration while preserving the same effective default.
- Add or improve metrics, logs, traces, and health details without changing decisions or payload content.
- Add tests that characterize and lock in current behavior.

**Requires approval for:**

- Changing the effective database endpoint.

---

### PG-002: Connection, socket, statement, lock, and transaction timeouts are bounded

**Severity:** Critical  
**Category:** resilience

#### Requirement

The application code and configuration must satisfy this behavior when the same artifact runs in either active region.

#### Repository evidence to inspect

- `connectTimeout`
- `socketTimeout`
- `statement_timeout`
- `lock_timeout`

#### Finding condition

Emit a finding when evidence shows that database operations can hang beyond failure budget.

#### Evidence rule

Cite the file path, symbol or property, and advisory line range when available. Evaluate effective behavior rather than the presence of a library, annotation, or property alone. If the repository does not contain enough evidence, return `not_assessed` rather than assuming noncompliance.

#### Business-logic risk

**Risk level:** `severe`  
**Requires approval before implementation:** `true`  
**Approval owner:** `product_and_architecture`

**Safe remediation without approval:**

- Add query-duration and timeout telemetry.
- Add tests that demonstrate the current behavior and the failure mode.

**Requires approval for:**

- Introducing statement, lock, or transaction timeouts that can abort operations currently completing successfully.

---

### PG-003: Transient retry occurs only at idempotent transaction boundaries

**Severity:** Critical  
**Category:** resilience

#### Requirement

The application code and configuration must satisfy this behavior when the same artifact runs in either active region.

#### Repository evidence to inspect

- `PSQLException`
- `SQLState`
- `retry template`

#### Finding condition

Emit a finding when evidence shows that retry is absent or repeats ambiguous/non-idempotent work.

#### Evidence rule

Cite the file path, symbol or property, and advisory line range when available. Evaluate effective behavior rather than the presence of a library, annotation, or property alone. If the repository does not contain enough evidence, return `not_assessed` rather than assuming noncompliance.

#### Business-logic risk

**Risk level:** `severe`  
**Requires approval before implementation:** `true`  
**Approval owner:** `product`

**Safe remediation without approval:**

- Add retry and outcome telemetry.
- Add tests that demonstrate the current behavior and the failure mode.

**Requires approval for:**

- Adding retry around any transaction that is not proven idempotent.
- Changing retry boundaries.

---

### PG-004: Writes use idempotency and optimistic/pessimistic concurrency appropriately

**Severity:** Critical  
**Category:** consistency

#### Requirement

The application code and configuration must satisfy this behavior when the same artifact runs in either active region.

#### Repository evidence to inspect

- `ON CONFLICT`
- `unique constraint`
- `@Version`
- `advisory lock`

#### Finding condition

Emit a finding when evidence shows that concurrent multi-region processing corrupts or duplicates state.

#### Evidence rule

Cite the file path, symbol or property, and advisory line range when available. Evaluate effective behavior rather than the presence of a library, annotation, or property alone. If the repository does not contain enough evidence, return `not_assessed` rather than assuming noncompliance.

#### Business-logic risk

**Risk level:** `severe`  
**Requires approval before implementation:** `true`  
**Approval owner:** `product_and_data`

**Safe remediation without approval:**

- Add conflict and concurrency telemetry.
- Add tests that demonstrate the current behavior and the failure mode.

**Requires approval for:**

- Adding optimistic or pessimistic concurrency control that changes which writes succeed.
- Adding ON CONFLICT behavior.

---

### PG-005: Pool invalidates failed connections and reconnects after endpoint recovery

**Severity:** High  
**Category:** recovery

#### Requirement

The application code and configuration must satisfy this behavior when the same artifact runs in either active region.

#### Repository evidence to inspect

- `HikariCP`
- `validationTimeout`
- `maxLifetime`

#### Finding condition

Emit a finding when evidence shows that recovery requires application restart.

#### Evidence rule

Cite the file path, symbol or property, and advisory line range when available. Evaluate effective behavior rather than the presence of a library, annotation, or property alone. If the repository does not contain enough evidence, return `not_assessed` rather than assuming noncompliance.

#### Business-logic risk

**Risk level:** `moderate`  
**Requires approval before implementation:** `false`  
**Approval owner:** `architecture`

**Safe remediation without approval:**

- Add pool and connection-validation telemetry.
- Add tests that demonstrate the current behavior and the failure mode.

**Requires approval for:**

- Changing connection lifetime where it affects long-running operations.

---

### PG-006: Critical database failure affects readiness but not liveness

**Severity:** Critical  
**Category:** health

#### Requirement

The application code and configuration must satisfy this behavior when the same artifact runs in either active region.

#### Repository evidence to inspect

- `DataSourceHealthIndicator`
- `readiness group`

#### Finding condition

Emit a finding when evidence shows that readiness/liveness semantics are incorrect.

#### Evidence rule

Cite the file path, symbol or property, and advisory line range when available. Evaluate effective behavior rather than the presence of a library, annotation, or property alone. If the repository does not contain enough evidence, return `not_assessed` rather than assuming noncompliance.

#### Business-logic risk

**Risk level:** `severe`  
**Requires approval before implementation:** `true`  
**Approval owner:** `architecture_and_product`

**Safe remediation without approval:**

- Add dependency-state telemetry.
- Add tests that demonstrate the current behavior and the failure mode.

**Requires approval for:**

- Adding the database to readiness.

---

### PG-007: Read-after-write and replica-lag assumptions are explicit

**Severity:** High  
**Category:** consistency

#### Requirement

The application code and configuration must satisfy this behavior when the same artifact runs in either active region.

#### Repository evidence to inspect

- `read routing`
- `transaction isolation`
- `replica lag`

#### Finding condition

Emit a finding when evidence shows that code assumes immediate consistency when reads may use a replica.

#### Evidence rule

Cite the file path, symbol or property, and advisory line range when available. Evaluate effective behavior rather than the presence of a library, annotation, or property alone. If the repository does not contain enough evidence, return `not_assessed` rather than assuming noncompliance.

#### Business-logic risk

**Risk level:** `severe`  
**Requires approval before implementation:** `true`  
**Approval owner:** `architecture_and_data`

**Safe remediation without approval:**

- Add read-routing and replica-lag telemetry.
- Add tests that demonstrate the current behavior and the failure mode.

**Requires approval for:**

- Changing read routing between primary and replica.
- Changing transaction isolation.

---

### PG-008: Tests cover failover, serialization/deadlock errors, ambiguous commit, and recovery

**Severity:** Critical  
**Category:** testing

#### Requirement

The application code and configuration must satisfy this behavior when the same artifact runs in either active region.

#### Repository evidence to inspect

- `Testcontainers PostgreSQL`
- `Toxiproxy`
- `integration tests`

#### Finding condition

Emit a finding when evidence shows that PostgreSQL recovery behavior is untested.

#### Evidence rule

Cite the file path, symbol or property, and advisory line range when available. Evaluate effective behavior rather than the presence of a library, annotation, or property alone. If the repository does not contain enough evidence, return `not_assessed` rather than assuming noncompliance.

#### Business-logic risk

**Risk level:** `none`  
**Requires approval before implementation:** `false`  
**Approval owner:** `none`

**Safe remediation without approval:**

- Add tests that demonstrate the current behavior and the failure mode.

---

### PG-009: Connection pool is bounded, monitored, and leak-detecting

**Severity:** High  
**Category:** resource-management

#### Requirement

The application code and configuration must satisfy this behavior when the same artifact runs in either active region.

#### Repository evidence to inspect

- `maximumPoolSize`
- `leakDetectionThreshold`
- `connectionTimeout`
- `pool metrics`

#### Finding condition

Emit a finding when evidence shows that pool sizing is unbounded or unjustified, leaks are undetected, or saturation cannot be observed.

#### Evidence rule

Cite the file path, symbol or property, and advisory line range when available. Evaluate effective behavior rather than the presence of a library, annotation, or property alone. If the repository does not contain enough evidence, return `not_assessed` rather than assuming noncompliance.

#### Quality caveats

- Pool size must reflect database capacity, not only application concurrency.

#### Business-logic risk

**Risk level:** `moderate`  
**Requires approval before implementation:** `false`  
**Approval owner:** `architecture`

**Safe remediation without approval:**

- Add pool saturation, wait-time, and leak telemetry.
- Add tests that demonstrate the current behavior and the failure mode.

**Requires approval for:**

- Reducing pool size where it can reject work currently served.

---

### PG-010: Endpoint resolution and connection lifetime support failover

**Severity:** High  
**Category:** recovery

#### Requirement

The application code and configuration must satisfy this behavior when the same artifact runs in either active region.

#### Repository evidence to inspect

- `dns ttl`
- `networkaddress.cache.ttl`
- `maxLifetime`
- `targetServerType`

#### Finding condition

Emit a finding when evidence shows that cached endpoint resolution or long-lived connections keep the application bound to a failed endpoint.

#### Evidence rule

Cite the file path, symbol or property, and advisory line range when available. Evaluate effective behavior rather than the presence of a library, annotation, or property alone. If the repository does not contain enough evidence, return `not_assessed` rather than assuming noncompliance.

#### Quality caveats

- Connection recycling settings must be validated against the actual failover behavior.

#### Business-logic risk

**Risk level:** `moderate`  
**Requires approval before implementation:** `false`  
**Approval owner:** `platform_and_architecture`

**Safe remediation without approval:**

- Add endpoint-resolution and connection-age telemetry.
- Add tests that demonstrate the current behavior and the failure mode.

**Requires approval for:**

- Changing connection recycling where it interrupts long operations.

---

### PG-011: TLS verification is enabled and certificate material is managed

**Severity:** Critical  
**Category:** security

#### Requirement

The application code and configuration must satisfy this behavior when the same artifact runs in either active region.

#### Repository evidence to inspect

- `sslmode`
- `sslrootcert`
- `verify-full`
- `truststore`

#### Finding condition

Emit a finding when evidence shows that TLS is disabled, verification is weakened, or certificate material cannot be rotated without redeploying the application.

#### Evidence rule

Cite the file path, symbol or property, and advisory line range when available. Evaluate effective behavior rather than the presence of a library, annotation, or property alone. If the repository does not contain enough evidence, return `not_assessed` rather than assuming noncompliance.

#### Quality caveats

- Do not disable certificate verification to work around connectivity issues.

#### Business-logic risk

**Risk level:** `severe`  
**Requires approval before implementation:** `true`  
**Approval owner:** `security`

**Safe remediation without approval:**

- Add TLS-mode telemetry.
- Add tests that demonstrate the current behavior and the failure mode.

**Requires approval for:**

- Changing sslmode or certificate verification, which can break connectivity or weaken security.

---

### PG-012: Credentials use approved identity with supported rotation

**Severity:** Critical  
**Category:** security

#### Requirement

The application code and configuration must satisfy this behavior when the same artifact runs in either active region.

#### Repository evidence to inspect

- `password`
- `IAM token`
- `credential refresh`
- `secret reference`

#### Finding condition

Emit a finding when evidence shows that credentials are embedded or logged, or rotation requires restart without an approved contract.

#### Evidence rule

Cite the file path, symbol or property, and advisory line range when available. Evaluate effective behavior rather than the presence of a library, annotation, or property alone. If the repository does not contain enough evidence, return `not_assessed` rather than assuming noncompliance.

#### Quality caveats

- Token-based authentication requires refresh before expiration, including for pooled connections.

#### Business-logic risk

**Risk level:** `severe`  
**Requires approval before implementation:** `true`  
**Approval owner:** `security`

**Safe remediation without approval:**

- Add authentication-failure telemetry with values redacted.
- Add tests that demonstrate the current behavior and the failure mode.

**Requires approval for:**

- Changing credential type or authentication flow.

---

### PG-013: Long-running and idle transactions are bounded

**Severity:** High  
**Category:** resilience

#### Requirement

The application code and configuration must satisfy this behavior when the same artifact runs in either active region.

#### Repository evidence to inspect

- `idle_in_transaction_session_timeout`
- `transaction timeout`
- `@Transactional timeout`

#### Finding condition

Emit a finding when evidence shows that transactions can remain open indefinitely, holding locks or connections during degradation.

#### Evidence rule

Cite the file path, symbol or property, and advisory line range when available. Evaluate effective behavior rather than the presence of a library, annotation, or property alone. If the repository does not contain enough evidence, return `not_assessed` rather than assuming noncompliance.

#### Quality caveats

- Timeout values must align with the request and failover budget.

#### Business-logic risk

**Risk level:** `severe`  
**Requires approval before implementation:** `true`  
**Approval owner:** `product`

**Safe remediation without approval:**

- Add transaction-duration telemetry.
- Add tests that demonstrate the current behavior and the failure mode.

**Requires approval for:**

- Introducing idle or transaction timeouts that can abort legitimate long-running business operations.

---

### PG-014: Large result sets stream with bounded memory

**Severity:** High  
**Category:** performance

#### Requirement

The application code and configuration must satisfy this behavior when the same artifact runs in either active region.

#### Repository evidence to inspect

- `fetchSize`
- `setFetchSize`
- `cursor`
- `stream`

#### Finding condition

Emit a finding when evidence shows that queries materialize unbounded result sets in application memory.

#### Evidence rule

Cite the file path, symbol or property, and advisory line range when available. Evaluate effective behavior rather than the presence of a library, annotation, or property alone. If the repository does not contain enough evidence, return `not_assessed` rather than assuming noncompliance.

#### Quality caveats

- Streaming requires an open transaction and correct resource closure.

#### Business-logic risk

**Risk level:** `moderate`  
**Requires approval before implementation:** `false`  
**Approval owner:** `architecture`

**Safe remediation without approval:**

- Add result-size and memory telemetry.
- Add tests that demonstrate the current behavior and the failure mode.

**Requires approval for:**

- Changing fetch behavior where it alters transaction scope or resource lifetime.

---

### PG-015: Schema migrations are safe for rolling and multi-instance deployment

**Severity:** Critical  
**Category:** schema

#### Requirement

The application code and configuration must satisfy this behavior when the same artifact runs in either active region.

#### Repository evidence to inspect

- `Flyway`
- `Liquibase`
- `migration lock`
- `backward compatible`

#### Finding condition

Emit a finding when evidence shows that migrations block startup unsafely, run concurrently without locking, or break compatibility with the previously deployed application version.

#### Evidence rule

Cite the file path, symbol or property, and advisory line range when available. Evaluate effective behavior rather than the presence of a library, annotation, or property alone. If the repository does not contain enough evidence, return `not_assessed` rather than assuming noncompliance.

#### Quality caveats

- Schema changes are business-affecting and require approval and rollback planning.

#### Business-logic risk

**Risk level:** `severe`  
**Requires approval before implementation:** `true`  
**Approval owner:** `data_and_product`

**Safe remediation without approval:**

- Add migration-execution telemetry.
- Add tests that demonstrate the current behavior and the failure mode.

**Requires approval for:**

- Any schema migration change, ordering change, or locking change.

---

### PG-016: Dual writes to the database and messaging use durable reconciliation

**Severity:** Critical  
**Category:** consistency

#### Requirement

The application code and configuration must satisfy this behavior when the same artifact runs in either active region.

#### Repository evidence to inspect

- `outbox`
- `transactional publish`
- `after commit`
- `reconciliation`

#### Finding condition

Emit a finding when evidence shows that a database commit and a message publish can diverge without an outbox, compensation, or reconciliation path.

#### Evidence rule

Cite the file path, symbol or property, and advisory line range when available. Evaluate effective behavior rather than the presence of a library, annotation, or property alone. If the repository does not contain enough evidence, return `not_assessed` rather than assuming noncompliance.

#### Quality caveats

- A local transaction cannot atomically include an external broker.

#### Business-logic risk

**Risk level:** `severe`  
**Requires approval before implementation:** `true`  
**Approval owner:** `architecture_and_product`

**Safe remediation without approval:**

- Add divergence-detection telemetry between commit and publish.
- Add tests that demonstrate the current behavior and the failure mode.

**Requires approval for:**

- Introducing an outbox or post-commit publish, which changes transaction boundaries and event timing.

---

### PG-017: Identity and sequence generation are safe for concurrent instances

**Severity:** High  
**Category:** consistency

#### Requirement

The application code and configuration must satisfy this behavior when the same artifact runs in either active region.

#### Repository evidence to inspect

- `sequence`
- `identity`
- `uuid`
- `allocationSize`

#### Finding condition

Emit a finding when evidence shows that identifier generation can collide, reuse values, or depend on single-instance assumptions.

#### Evidence rule

Cite the file path, symbol or property, and advisory line range when available. Evaluate effective behavior rather than the presence of a library, annotation, or property alone. If the repository does not contain enough evidence, return `not_assessed` rather than assuming noncompliance.

#### Quality caveats

- Identifier strategy changes can affect data contracts and require approval.

#### Business-logic risk

**Risk level:** `severe`  
**Requires approval before implementation:** `true`  
**Approval owner:** `data_and_partner_contract`

**Safe remediation without approval:**

- Add identifier-collision telemetry.
- Add tests that demonstrate the current behavior and the failure mode.

**Requires approval for:**

- Changing identifier generation strategy, format, or allocation.

---

### PG-018: Batch operations bound size and handle partial failure

**Severity:** High  
**Category:** consistency

#### Requirement

The application code and configuration must satisfy this behavior when the same artifact runs in either active region.

#### Repository evidence to inspect

- `batch update`
- `saveAll`
- `rewriteBatchedInserts`
- `partial failure`

#### Finding condition

Emit a finding when evidence shows that batch operations are unbounded or partial failure is treated as full success.

#### Evidence rule

Cite the file path, symbol or property, and advisory line range when available. Evaluate effective behavior rather than the presence of a library, annotation, or property alone. If the repository does not contain enough evidence, return `not_assessed` rather than assuming noncompliance.

#### Quality caveats

- Large batches can extend lock duration and increase failover impact.

#### Business-logic risk

**Risk level:** `moderate`  
**Requires approval before implementation:** `false`  
**Approval owner:** `product`

**Safe remediation without approval:**

- Add per-item batch outcome telemetry.
- Add tests that demonstrate the current behavior and the failure mode.

**Requires approval for:**

- Changing batch size where lock duration or partial-failure behavior changes.

---

### PG-019: SQL logging and diagnostics exclude sensitive data

**Severity:** Critical  
**Category:** security

#### Requirement

The application code and configuration must satisfy this behavior when the same artifact runs in either active region.

#### Repository evidence to inspect

- `show-sql`
- `log parameters`
- `PII`
- `bind values`

#### Finding condition

Emit a finding when evidence shows that SQL logging can emit personal data, credentials, or full bind parameters.

#### Evidence rule

Cite the file path, symbol or property, and advisory line range when available. Evaluate effective behavior rather than the presence of a library, annotation, or property alone. If the repository does not contain enough evidence, return `not_assessed` rather than assuming noncompliance.

#### Quality caveats

- Query text may be acceptable where parameter values are not.

#### Business-logic risk

**Risk level:** `low`  
**Requires approval before implementation:** `false`  
**Approval owner:** `security`

**Safe remediation without approval:**

- Add or strengthen redaction.
- Add or improve metrics, logs, traces, and health details without changing decisions or payload content.
- Add tests that characterize and lock in current behavior.

**Requires approval for:**

- Weakening existing redaction.

---

### PG-020: Prepared-statement behavior is compatible with the connection path

**Severity:** Medium  
**Category:** compatibility

#### Requirement

The application code and configuration must satisfy this behavior when the same artifact runs in either active region.

#### Repository evidence to inspect

- `prepareThreshold`
- `preparedStatementCacheQueries`
- `pgbouncer`
- `transaction pooling`

#### Finding condition

Emit a finding when evidence shows that server-side prepared statement behavior is incompatible with the effective connection pooling path.

#### Evidence rule

Cite the file path, symbol or property, and advisory line range when available. Evaluate effective behavior rather than the presence of a library, annotation, or property alone. If the repository does not contain enough evidence, return `not_assessed` rather than assuming noncompliance.

#### Quality caveats

- Pooler mode is often external evidence; assess the application setting and its assumption.

#### Business-logic risk

**Risk level:** `moderate`  
**Requires approval before implementation:** `false`  
**Approval owner:** `platform_and_architecture`

**Safe remediation without approval:**

- Add prepared-statement telemetry.
- Add tests that demonstrate the current behavior and the failure mode.

**Requires approval for:**

- Changing prepared-statement settings where pooler compatibility or plan behavior changes.

---

## Standard finding format

- **Title:** [specific code-level gap]
- **Control:** [PG-NNN]
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
