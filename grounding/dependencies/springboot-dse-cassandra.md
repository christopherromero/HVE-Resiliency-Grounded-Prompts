---
schema_version: 2.2.0
document_type: dependency_behavior
service: dse-cassandra
service_name: DSE Cassandra
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
- id: DSE-001
  title: Contact points, local datacenter, and keyspace are deployment-injected
  severity: critical
  category: configuration
  evidence_patterns:
  - basic.contact-points
  - local-datacenter
  - CqlSessionBuilder
  finding_when: datacenter or host is hardcoded
  emit_on_failure: true
- id: DSE-002
  title: Driver uses datacenter-aware local routing
  severity: critical
  category: regional-affinity
  evidence_patterns:
  - localDatacenter
  - DcInferringLoadBalancingPolicy
  finding_when: normal requests can cross regions unexpectedly
  emit_on_failure: true
- id: DSE-003
  title: Consistency levels match the approved local quorum model
  severity: critical
  category: consistency
  evidence_patterns:
  - LOCAL_QUORUM
  - LOCAL_ONE
  - serial consistency
  finding_when: code requires cross-region quorum or uses unsafe consistency without
    rationale
  emit_on_failure: true
- id: DSE-004
  title: Timeout, retry, and speculative execution policies are bounded
  severity: critical
  category: resilience
  evidence_patterns:
  - request timeout
  - RetryPolicy
  - SpeculativeExecutionPolicy
  finding_when: retry amplifies load or hides unavailable consistency
  emit_on_failure: true
- id: DSE-005
  title: Writes are idempotent before driver retries or speculation
  severity: critical
  category: consistency
  evidence_patterns:
  - setIdempotent
  - idempotent statement
  - business key
  finding_when: non-idempotent write may execute more than once
  emit_on_failure: true
- id: DSE-006
  title: Session reconnects and topology refreshes without restart
  severity: high
  category: recovery
  evidence_patterns:
  - CqlSession
  - reconnection policy
  - schema refresh
  finding_when: client remains pinned to failed nodes or DC
  emit_on_failure: true
- id: DSE-007
  title: Critical Cassandra failure affects readiness but not liveness
  severity: critical
  category: health
  evidence_patterns:
  - HealthIndicator
  - readiness group
  finding_when: health signaling is incorrect
  emit_on_failure: true
- id: DSE-008
  title: Tests cover node/DC loss, unavailable consistency, timeout, retry, and recovery
  severity: critical
  category: testing
  evidence_patterns:
  - Testcontainers
  - fault injection
  - integration test
  finding_when: Cassandra failure behavior is untested
  emit_on_failure: true
---

# DSE Cassandra Target-State Application Behavior Standard

### Shared-service operating-model contract

This standard does not select the application's shared-service topology. Resolve the operating model from:

```text
architecture_context.shared_service_operating_models.services.dse_cassandra
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

This dependency-specific standard assesses how a Spring Boot microservice uses DSE Cassandra when evaluated for the approved target operating model supplied by application architecture context. The local regional service endpoint is assumed to exist and be reachable through the approved private networking design.

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

## DSE-001: Contact points, local datacenter, and keyspace are deployment-injected

**Severity:** Critical  
**Category:** configuration

### Requirement

The application code and configuration must satisfy this behavior when the same artifact runs in either active region.

### Repository evidence to inspect

- `basic.contact-points`
- `local-datacenter`
- `CqlSessionBuilder`

### Finding condition

Emit a finding when evidence shows that datacenter or host is hardcoded.

### Evidence rule

Cite the file path, symbol, property, and line range when available. If the repository does not contain enough evidence, return `not_assessed` rather than assuming noncompliance.

---

## DSE-002: Driver uses datacenter-aware local routing

**Severity:** Critical  
**Category:** regional-affinity

### Requirement

The application code and configuration must satisfy this behavior when the same artifact runs in either active region.

### Repository evidence to inspect

- `localDatacenter`
- `DcInferringLoadBalancingPolicy`

### Finding condition

Emit a finding when evidence shows that normal requests can cross regions unexpectedly.

### Evidence rule

Cite the file path, symbol, property, and line range when available. If the repository does not contain enough evidence, return `not_assessed` rather than assuming noncompliance.

---

## DSE-003: Consistency levels match the approved local quorum model

**Severity:** Critical  
**Category:** consistency

### Requirement

The application code and configuration must satisfy this behavior when the same artifact runs in either active region.

### Repository evidence to inspect

- `LOCAL_QUORUM`
- `LOCAL_ONE`
- `serial consistency`

### Finding condition

Emit a finding when evidence shows that code requires cross-region quorum or uses unsafe consistency without rationale.

### Evidence rule

Cite the file path, symbol, property, and line range when available. If the repository does not contain enough evidence, return `not_assessed` rather than assuming noncompliance.

---

## DSE-004: Timeout, retry, and speculative execution policies are bounded

**Severity:** Critical  
**Category:** resilience

### Requirement

The application code and configuration must satisfy this behavior when the same artifact runs in either active region.

### Repository evidence to inspect

- `request timeout`
- `RetryPolicy`
- `SpeculativeExecutionPolicy`

### Finding condition

Emit a finding when evidence shows that retry amplifies load or hides unavailable consistency.

### Evidence rule

Cite the file path, symbol, property, and line range when available. If the repository does not contain enough evidence, return `not_assessed` rather than assuming noncompliance.

---

## DSE-005: Writes are idempotent before driver retries or speculation

**Severity:** Critical  
**Category:** consistency

### Requirement

The application code and configuration must satisfy this behavior when the same artifact runs in either active region.

### Repository evidence to inspect

- `setIdempotent`
- `idempotent statement`
- `business key`

### Finding condition

Emit a finding when evidence shows that non-idempotent write may execute more than once.

### Evidence rule

Cite the file path, symbol, property, and line range when available. If the repository does not contain enough evidence, return `not_assessed` rather than assuming noncompliance.

---

## DSE-006: Session reconnects and topology refreshes without restart

**Severity:** High  
**Category:** recovery

### Requirement

The application code and configuration must satisfy this behavior when the same artifact runs in either active region.

### Repository evidence to inspect

- `CqlSession`
- `reconnection policy`
- `schema refresh`

### Finding condition

Emit a finding when evidence shows that client remains pinned to failed nodes or DC.

### Evidence rule

Cite the file path, symbol, property, and line range when available. If the repository does not contain enough evidence, return `not_assessed` rather than assuming noncompliance.

---

## DSE-007: Critical Cassandra failure affects readiness but not liveness

**Severity:** Critical  
**Category:** health

### Requirement

The application code and configuration must satisfy this behavior when the same artifact runs in either active region.

### Repository evidence to inspect

- `HealthIndicator`
- `readiness group`

### Finding condition

Emit a finding when evidence shows that health signaling is incorrect.

### Evidence rule

Cite the file path, symbol, property, and line range when available. If the repository does not contain enough evidence, return `not_assessed` rather than assuming noncompliance.

---

## DSE-008: Tests cover node/DC loss, unavailable consistency, timeout, retry, and recovery

**Severity:** Critical  
**Category:** testing

### Requirement

The application code and configuration must satisfy this behavior when the same artifact runs in either active region.

### Repository evidence to inspect

- `Testcontainers`
- `fault injection`
- `integration test`

### Finding condition

Emit a finding when evidence shows that Cassandra failure behavior is untested.

### Evidence rule

Cite the file path, symbol, property, and line range when available. If the repository does not contain enough evidence, return `not_assessed` rather than assuming noncompliance.

---

# Standard finding format

- **Title:** [specific code-level gap]
- **Control:** [DSE-NNN]
- **Severity:** [severity]
- **Repository evidence:** [file, symbol/property, line]
- **Observed behavior:** [what code currently does]
- **Active-active risk:** [effect during regional dependency or network failure]
- **Required code/configuration change:** [specific remediation]
- **Validation test:** [test that proves the behavior]

# Non-findings

Do not create infrastructure findings such as missing second-region resources, private endpoints, zone redundancy, geo-replication, capacity, DNS, or global load-balancer configuration. Those are assumed platform responsibilities and are outside this repository assessment.
