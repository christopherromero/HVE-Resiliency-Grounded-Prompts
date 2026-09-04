---
schema_version: 1.0.0
document_type: dependency_behavior
service: cosmosdb
service_name: Azure Cosmos DB
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
- id: COSMOS-001
  title: Cosmos endpoint and preferred region are deployment-injected
  severity: critical
  category: configuration
  evidence_patterns:
  - spring.cloud.azure.cosmos
  - preferredRegions
  - CosmosClientBuilder
  finding_when: endpoint or preferred region is hardcoded
  emit_on_failure: true
- id: COSMOS-002
  title: Client uses local-region preference and approved endpoint discovery
  severity: critical
  category: regional-affinity
  evidence_patterns:
  - preferredRegions
  - endpointDiscoveryEnabled
  finding_when: client can route normally to another region or disables discovery
    without approved reason
  emit_on_failure: true
- id: COSMOS-003
  title: SDK retry and timeout budgets are explicit
  severity: high
  category: resilience
  evidence_patterns:
  - throttlingRetryOptions
  - requestTimeout
  - RetryOptions
  finding_when: retry or timeout behavior is absent or unbounded
  emit_on_failure: true
- id: COSMOS-004
  title: Reads and writes use the approved consistency and session-token strategy
  severity: critical
  category: consistency
  evidence_patterns:
  - consistencyLevel
  - session token
  finding_when: code assumes stronger cross-region consistency than configured or
    loses required session guarantees
  emit_on_failure: true
- id: COSMOS-005
  title: Writes use idempotency and optimistic concurrency where required
  severity: critical
  category: consistency
  evidence_patterns:
  - ETag
  - IfMatch
  - idempotency key
  - unique key
  finding_when: duplicate or concurrent multi-region writes can create inconsistent
    business state
  emit_on_failure: true
- id: COSMOS-006
  title: Critical Cosmos failure affects readiness without coupling liveness
  severity: critical
  category: health
  evidence_patterns:
  - cosmos HealthIndicator
  - readiness group
  finding_when: unusable data path remains ready or external failure kills liveness
  emit_on_failure: true
- id: COSMOS-007
  title: Application handles 429, transient transport, and regional failover responses
  severity: high
  category: resilience
  evidence_patterns:
  - CosmosException
  - statusCode
  - subStatusCode
  - retry after
  finding_when: errors are treated uniformly or generate retry storms
  emit_on_failure: true
- id: COSMOS-008
  title: Tests cover endpoint selection, conflict, throttling, failover, and recovery
  severity: high
  category: testing
  evidence_patterns:
  - Cosmos emulator
  - mock client
  - fault injection
  finding_when: active-active data behaviors are untested
  emit_on_failure: true
---

# Azure Cosmos DB Active-Active Application Behavior Standard

## Purpose

This dependency-specific standard assesses how a Spring Boot microservice uses Azure Cosmos DB when deployed to two active Azure regions. The local regional service endpoint is assumed to exist and be reachable through the approved private networking design.

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

## COSMOS-001: Cosmos endpoint and preferred region are deployment-injected

**Severity:** Critical  
**Category:** configuration

### Requirement

The application code and configuration must satisfy this behavior when the same artifact runs in either active region.

### Repository evidence to inspect

- `spring.cloud.azure.cosmos`
- `preferredRegions`
- `CosmosClientBuilder`

### Finding condition

Emit a finding when evidence shows that endpoint or preferred region is hardcoded.

### Evidence rule

Cite the file path, symbol, property, and line range when available. If the repository does not contain enough evidence, return `not_assessed` rather than assuming noncompliance.

---

## COSMOS-002: Client uses local-region preference and approved endpoint discovery

**Severity:** Critical  
**Category:** regional-affinity

### Requirement

The application code and configuration must satisfy this behavior when the same artifact runs in either active region.

### Repository evidence to inspect

- `preferredRegions`
- `endpointDiscoveryEnabled`

### Finding condition

Emit a finding when evidence shows that client can route normally to another region or disables discovery without approved reason.

### Evidence rule

Cite the file path, symbol, property, and line range when available. If the repository does not contain enough evidence, return `not_assessed` rather than assuming noncompliance.

---

## COSMOS-003: SDK retry and timeout budgets are explicit

**Severity:** High  
**Category:** resilience

### Requirement

The application code and configuration must satisfy this behavior when the same artifact runs in either active region.

### Repository evidence to inspect

- `throttlingRetryOptions`
- `requestTimeout`
- `RetryOptions`

### Finding condition

Emit a finding when evidence shows that retry or timeout behavior is absent or unbounded.

### Evidence rule

Cite the file path, symbol, property, and line range when available. If the repository does not contain enough evidence, return `not_assessed` rather than assuming noncompliance.

---

## COSMOS-004: Reads and writes use the approved consistency and session-token strategy

**Severity:** Critical  
**Category:** consistency

### Requirement

The application code and configuration must satisfy this behavior when the same artifact runs in either active region.

### Repository evidence to inspect

- `consistencyLevel`
- `session token`

### Finding condition

Emit a finding when evidence shows that code assumes stronger cross-region consistency than configured or loses required session guarantees.

### Evidence rule

Cite the file path, symbol, property, and line range when available. If the repository does not contain enough evidence, return `not_assessed` rather than assuming noncompliance.

---

## COSMOS-005: Writes use idempotency and optimistic concurrency where required

**Severity:** Critical  
**Category:** consistency

### Requirement

The application code and configuration must satisfy this behavior when the same artifact runs in either active region.

### Repository evidence to inspect

- `ETag`
- `IfMatch`
- `idempotency key`
- `unique key`

### Finding condition

Emit a finding when evidence shows that duplicate or concurrent multi-region writes can create inconsistent business state.

### Evidence rule

Cite the file path, symbol, property, and line range when available. If the repository does not contain enough evidence, return `not_assessed` rather than assuming noncompliance.

---

## COSMOS-006: Critical Cosmos failure affects readiness without coupling liveness

**Severity:** Critical  
**Category:** health

### Requirement

The application code and configuration must satisfy this behavior when the same artifact runs in either active region.

### Repository evidence to inspect

- `cosmos HealthIndicator`
- `readiness group`

### Finding condition

Emit a finding when evidence shows that unusable data path remains ready or external failure kills liveness.

### Evidence rule

Cite the file path, symbol, property, and line range when available. If the repository does not contain enough evidence, return `not_assessed` rather than assuming noncompliance.

---

## COSMOS-007: Application handles 429, transient transport, and regional failover responses

**Severity:** High  
**Category:** resilience

### Requirement

The application code and configuration must satisfy this behavior when the same artifact runs in either active region.

### Repository evidence to inspect

- `CosmosException`
- `statusCode`
- `subStatusCode`
- `retry after`

### Finding condition

Emit a finding when evidence shows that errors are treated uniformly or generate retry storms.

### Evidence rule

Cite the file path, symbol, property, and line range when available. If the repository does not contain enough evidence, return `not_assessed` rather than assuming noncompliance.

---

## COSMOS-008: Tests cover endpoint selection, conflict, throttling, failover, and recovery

**Severity:** High  
**Category:** testing

### Requirement

The application code and configuration must satisfy this behavior when the same artifact runs in either active region.

### Repository evidence to inspect

- `Cosmos emulator`
- `mock client`
- `fault injection`

### Finding condition

Emit a finding when evidence shows that active-active data behaviors are untested.

### Evidence rule

Cite the file path, symbol, property, and line range when available. If the repository does not contain enough evidence, return `not_assessed` rather than assuming noncompliance.

---

# Standard finding format

- **Title:** [specific code-level gap]
- **Control:** [COSMOS-NNN]
- **Severity:** [severity]
- **Repository evidence:** [file, symbol/property, line]
- **Observed behavior:** [what code currently does]
- **Active-active risk:** [effect during regional dependency or network failure]
- **Required code/configuration change:** [specific remediation]
- **Validation test:** [test that proves the behavior]

# Non-findings

Do not create infrastructure findings such as missing second-region resources, private endpoints, zone redundancy, geo-replication, capacity, DNS, or global load-balancer configuration. Those are assumed platform responsibilities and are outside this repository assessment.
