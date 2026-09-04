---
schema_version: 1.0.0
document_type: dependency_behavior
service: storage-blob
service_name: Azure Blob Storage
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
- id: BLOB-001
  title: Storage endpoint or account is deployment-injected
  severity: critical
  category: configuration
  evidence_patterns:
  - spring.cloud.azure.storage
  - BlobServiceClientBuilder
  - STORAGE_ACCOUNT
  finding_when: account or endpoint is hardcoded
  emit_on_failure: true
- id: BLOB-002
  title: Client timeout and retry policies are bounded
  severity: high
  category: resilience
  evidence_patterns:
  - RequestRetryOptions
  - ClientOptions
  - responseTimeout
  finding_when: blob operations lack bounded retry or timeout
  emit_on_failure: true
- id: BLOB-003
  title: Write operations are idempotent and concurrency-safe
  severity: critical
  category: consistency
  evidence_patterns:
  - ETag
  - BlobRequestConditions
  - overwrite flag
  - idempotency key
  finding_when: retry or concurrent write can overwrite or duplicate data unexpectedly
  emit_on_failure: true
- id: BLOB-004
  title: Application does not store durable state on pod-local storage
  severity: critical
  category: state
  evidence_patterns:
  - java.io
  - Files.write
  - /tmp
  - emptyDir
  finding_when: durable business state is written only to container or node filesystem
  emit_on_failure: true
- id: BLOB-005
  title: Critical storage failure affects readiness only when service cannot operate
  severity: high
  category: health
  evidence_patterns:
  - storage HealthIndicator
  - readiness group
  finding_when: readiness does not reflect critical storage loss or treats optional
    storage as fatal
  emit_on_failure: true
- id: BLOB-006
  title: Downloads and uploads stream data and bound memory usage
  severity: high
  category: performance
  evidence_patterns:
  - stream
  - Flux<ByteBuffer>
  - block size
  finding_when: large blob operation loads unbounded content into JVM memory
  emit_on_failure: true
- id: BLOB-007
  title: Recovery handles DNS, private endpoint, authentication, and client reconnection
  severity: high
  category: recovery
  evidence_patterns:
  - credential refresh
  - connection recovery
  finding_when: application requires restart after storage recovery
  emit_on_failure: true
- id: BLOB-008
  title: Tests cover timeout, conflict, partial transfer, retry, and recovery
  severity: high
  category: testing
  evidence_patterns:
  - Azurite
  - mock BlobClient
  - fault injection
  finding_when: storage failure behaviors are untested
  emit_on_failure: true
---

# Azure Blob Storage Active-Active Application Behavior Standard

## Purpose

This dependency-specific standard assesses how a Spring Boot microservice uses Azure Blob Storage when deployed to two active Azure regions. The local regional service endpoint is assumed to exist and be reachable through the approved private networking design.

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

## BLOB-001: Storage endpoint or account is deployment-injected

**Severity:** Critical  
**Category:** configuration

### Requirement

The application code and configuration must satisfy this behavior when the same artifact runs in either active region.

### Repository evidence to inspect

- `spring.cloud.azure.storage`
- `BlobServiceClientBuilder`
- `STORAGE_ACCOUNT`

### Finding condition

Emit a finding when evidence shows that account or endpoint is hardcoded.

### Evidence rule

Cite the file path, symbol, property, and line range when available. If the repository does not contain enough evidence, return `not_assessed` rather than assuming noncompliance.

---

## BLOB-002: Client timeout and retry policies are bounded

**Severity:** High  
**Category:** resilience

### Requirement

The application code and configuration must satisfy this behavior when the same artifact runs in either active region.

### Repository evidence to inspect

- `RequestRetryOptions`
- `ClientOptions`
- `responseTimeout`

### Finding condition

Emit a finding when evidence shows that blob operations lack bounded retry or timeout.

### Evidence rule

Cite the file path, symbol, property, and line range when available. If the repository does not contain enough evidence, return `not_assessed` rather than assuming noncompliance.

---

## BLOB-003: Write operations are idempotent and concurrency-safe

**Severity:** Critical  
**Category:** consistency

### Requirement

The application code and configuration must satisfy this behavior when the same artifact runs in either active region.

### Repository evidence to inspect

- `ETag`
- `BlobRequestConditions`
- `overwrite flag`
- `idempotency key`

### Finding condition

Emit a finding when evidence shows that retry or concurrent write can overwrite or duplicate data unexpectedly.

### Evidence rule

Cite the file path, symbol, property, and line range when available. If the repository does not contain enough evidence, return `not_assessed` rather than assuming noncompliance.

---

## BLOB-004: Application does not store durable state on pod-local storage

**Severity:** Critical  
**Category:** state

### Requirement

The application code and configuration must satisfy this behavior when the same artifact runs in either active region.

### Repository evidence to inspect

- `java.io`
- `Files.write`
- `/tmp`
- `emptyDir`

### Finding condition

Emit a finding when evidence shows that durable business state is written only to container or node filesystem.

### Evidence rule

Cite the file path, symbol, property, and line range when available. If the repository does not contain enough evidence, return `not_assessed` rather than assuming noncompliance.

---

## BLOB-005: Critical storage failure affects readiness only when service cannot operate

**Severity:** High  
**Category:** health

### Requirement

The application code and configuration must satisfy this behavior when the same artifact runs in either active region.

### Repository evidence to inspect

- `storage HealthIndicator`
- `readiness group`

### Finding condition

Emit a finding when evidence shows that readiness does not reflect critical storage loss or treats optional storage as fatal.

### Evidence rule

Cite the file path, symbol, property, and line range when available. If the repository does not contain enough evidence, return `not_assessed` rather than assuming noncompliance.

---

## BLOB-006: Downloads and uploads stream data and bound memory usage

**Severity:** High  
**Category:** performance

### Requirement

The application code and configuration must satisfy this behavior when the same artifact runs in either active region.

### Repository evidence to inspect

- `stream`
- `Flux<ByteBuffer>`
- `block size`

### Finding condition

Emit a finding when evidence shows that large blob operation loads unbounded content into JVM memory.

### Evidence rule

Cite the file path, symbol, property, and line range when available. If the repository does not contain enough evidence, return `not_assessed` rather than assuming noncompliance.

---

## BLOB-007: Recovery handles DNS, private endpoint, authentication, and client reconnection

**Severity:** High  
**Category:** recovery

### Requirement

The application code and configuration must satisfy this behavior when the same artifact runs in either active region.

### Repository evidence to inspect

- `credential refresh`
- `connection recovery`

### Finding condition

Emit a finding when evidence shows that application requires restart after storage recovery.

### Evidence rule

Cite the file path, symbol, property, and line range when available. If the repository does not contain enough evidence, return `not_assessed` rather than assuming noncompliance.

---

## BLOB-008: Tests cover timeout, conflict, partial transfer, retry, and recovery

**Severity:** High  
**Category:** testing

### Requirement

The application code and configuration must satisfy this behavior when the same artifact runs in either active region.

### Repository evidence to inspect

- `Azurite`
- `mock BlobClient`
- `fault injection`

### Finding condition

Emit a finding when evidence shows that storage failure behaviors are untested.

### Evidence rule

Cite the file path, symbol, property, and line range when available. If the repository does not contain enough evidence, return `not_assessed` rather than assuming noncompliance.

---

# Standard finding format

- **Title:** [specific code-level gap]
- **Control:** [BLOB-NNN]
- **Severity:** [severity]
- **Repository evidence:** [file, symbol/property, line]
- **Observed behavior:** [what code currently does]
- **Active-active risk:** [effect during regional dependency or network failure]
- **Required code/configuration change:** [specific remediation]
- **Validation test:** [test that proves the behavior]

# Non-findings

Do not create infrastructure findings such as missing second-region resources, private endpoints, zone redundancy, geo-replication, capacity, DNS, or global load-balancer configuration. Those are assumed platform responsibilities and are outside this repository assessment.
