---
schema_version: 1.0.0
document_type: dependency_behavior
service: keyvault
service_name: Azure Key Vault
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
- id: KV-001
  title: Vault URI is deployment-injected and resolves to the local regional vault
  severity: critical
  category: configuration
  evidence_patterns:
  - spring.cloud.azure.keyvault
  - vaultUrl
  - KEY_VAULT_URI
  - '@ConfigurationProperties'
  finding_when: vault URI or region is hardcoded or a remote vault is the normal endpoint
  emit_on_failure: true
- id: KV-002
  title: Credential acquisition is regional and uses workload identity or approved
    identity chain
  severity: high
  category: identity
  evidence_patterns:
  - DefaultAzureCredential
  - WorkloadIdentityCredential
  - TokenCredential
  finding_when: static secret credentials are embedded or identity selection is region-specific
    in code
  emit_on_failure: true
- id: KV-003
  title: Secret and certificate access has bounded retry and timeout
  severity: critical
  category: resilience
  evidence_patterns:
  - SecretClientBuilder
  - CertificateClientBuilder
  - RetryOptions
  - ClientOptions
  finding_when: access lacks bounded transient retry or timeout
  emit_on_failure: true
- id: KV-004
  title: Secret access is not on the synchronous request hot path
  severity: high
  category: performance
  evidence_patterns:
  - cache
  - refresh scheduler
  - startup loading
  finding_when: every business request synchronously calls Key Vault
  emit_on_failure: true
- id: KV-005
  title: Cached material has controlled refresh and stale-value behavior
  severity: high
  category: resilience
  evidence_patterns:
  - TTL
  - refresh interval
  - last known good
  - rotation
  finding_when: cache never refreshes or failure behavior can serve expired/unsafe
    material
  emit_on_failure: true
- id: KV-006
  title: Sustained Key Vault failure changes readiness for services that cannot operate
    safely
  severity: critical
  category: health
  evidence_patterns:
  - HealthIndicator
  - keyvault readiness group
  finding_when: critical vault failure leaves readiness UP
  emit_on_failure: true
- id: KV-007
  title: Recovery refreshes credentials and vault clients without restart
  severity: high
  category: recovery
  evidence_patterns:
  - credential refresh
  - client recreation
  - scheduled refresh
  finding_when: application cannot recover after identity, DNS, private endpoint,
    or vault restoration
  emit_on_failure: true
- id: KV-008
  title: Tests cover local endpoint selection, throttling, timeout, denial, and recovery
  severity: high
  category: testing
  evidence_patterns:
  - mock SecretClient
  - WireMock
  - fault tests
  finding_when: tests do not exercise failure and recovery behavior
  emit_on_failure: true
---

# Azure Key Vault Active-Active Application Behavior Standard

## Purpose

This dependency-specific standard assesses how a Spring Boot microservice uses Azure Key Vault when deployed to two active Azure regions. The local regional service endpoint is assumed to exist and be reachable through the approved private networking design.

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

## KV-001: Vault URI is deployment-injected and resolves to the local regional vault

**Severity:** Critical  
**Category:** configuration

### Requirement

The application code and configuration must satisfy this behavior when the same artifact runs in either active region.

### Repository evidence to inspect

- `spring.cloud.azure.keyvault`
- `vaultUrl`
- `KEY_VAULT_URI`
- `@ConfigurationProperties`

### Finding condition

Emit a finding when evidence shows that vault URI or region is hardcoded or a remote vault is the normal endpoint.

### Evidence rule

Cite the file path, symbol, property, and line range when available. If the repository does not contain enough evidence, return `not_assessed` rather than assuming noncompliance.

---

## KV-002: Credential acquisition is regional and uses workload identity or approved identity chain

**Severity:** High  
**Category:** identity

### Requirement

The application code and configuration must satisfy this behavior when the same artifact runs in either active region.

### Repository evidence to inspect

- `DefaultAzureCredential`
- `WorkloadIdentityCredential`
- `TokenCredential`

### Finding condition

Emit a finding when evidence shows that static secret credentials are embedded or identity selection is region-specific in code.

### Evidence rule

Cite the file path, symbol, property, and line range when available. If the repository does not contain enough evidence, return `not_assessed` rather than assuming noncompliance.

---

## KV-003: Secret and certificate access has bounded retry and timeout

**Severity:** Critical  
**Category:** resilience

### Requirement

The application code and configuration must satisfy this behavior when the same artifact runs in either active region.

### Repository evidence to inspect

- `SecretClientBuilder`
- `CertificateClientBuilder`
- `RetryOptions`
- `ClientOptions`

### Finding condition

Emit a finding when evidence shows that access lacks bounded transient retry or timeout.

### Evidence rule

Cite the file path, symbol, property, and line range when available. If the repository does not contain enough evidence, return `not_assessed` rather than assuming noncompliance.

---

## KV-004: Secret access is not on the synchronous request hot path

**Severity:** High  
**Category:** performance

### Requirement

The application code and configuration must satisfy this behavior when the same artifact runs in either active region.

### Repository evidence to inspect

- `cache`
- `refresh scheduler`
- `startup loading`

### Finding condition

Emit a finding when evidence shows that every business request synchronously calls Key Vault.

### Evidence rule

Cite the file path, symbol, property, and line range when available. If the repository does not contain enough evidence, return `not_assessed` rather than assuming noncompliance.

---

## KV-005: Cached material has controlled refresh and stale-value behavior

**Severity:** High  
**Category:** resilience

### Requirement

The application code and configuration must satisfy this behavior when the same artifact runs in either active region.

### Repository evidence to inspect

- `TTL`
- `refresh interval`
- `last known good`
- `rotation`

### Finding condition

Emit a finding when evidence shows that cache never refreshes or failure behavior can serve expired/unsafe material.

### Evidence rule

Cite the file path, symbol, property, and line range when available. If the repository does not contain enough evidence, return `not_assessed` rather than assuming noncompliance.

---

## KV-006: Sustained Key Vault failure changes readiness for services that cannot operate safely

**Severity:** Critical  
**Category:** health

### Requirement

The application code and configuration must satisfy this behavior when the same artifact runs in either active region.

### Repository evidence to inspect

- `HealthIndicator`
- `keyvault readiness group`

### Finding condition

Emit a finding when evidence shows that critical vault failure leaves readiness UP.

### Evidence rule

Cite the file path, symbol, property, and line range when available. If the repository does not contain enough evidence, return `not_assessed` rather than assuming noncompliance.

---

## KV-007: Recovery refreshes credentials and vault clients without restart

**Severity:** High  
**Category:** recovery

### Requirement

The application code and configuration must satisfy this behavior when the same artifact runs in either active region.

### Repository evidence to inspect

- `credential refresh`
- `client recreation`
- `scheduled refresh`

### Finding condition

Emit a finding when evidence shows that application cannot recover after identity, DNS, private endpoint, or vault restoration.

### Evidence rule

Cite the file path, symbol, property, and line range when available. If the repository does not contain enough evidence, return `not_assessed` rather than assuming noncompliance.

---

## KV-008: Tests cover local endpoint selection, throttling, timeout, denial, and recovery

**Severity:** High  
**Category:** testing

### Requirement

The application code and configuration must satisfy this behavior when the same artifact runs in either active region.

### Repository evidence to inspect

- `mock SecretClient`
- `WireMock`
- `fault tests`

### Finding condition

Emit a finding when evidence shows that tests do not exercise failure and recovery behavior.

### Evidence rule

Cite the file path, symbol, property, and line range when available. If the repository does not contain enough evidence, return `not_assessed` rather than assuming noncompliance.

---

# Standard finding format

- **Title:** [specific code-level gap]
- **Control:** [KV-NNN]
- **Severity:** [severity]
- **Repository evidence:** [file, symbol/property, line]
- **Observed behavior:** [what code currently does]
- **Active-active risk:** [effect during regional dependency or network failure]
- **Required code/configuration change:** [specific remediation]
- **Validation test:** [test that proves the behavior]

# Non-findings

Do not create infrastructure findings such as missing second-region resources, private endpoints, zone redundancy, geo-replication, capacity, DNS, or global load-balancer configuration. Those are assumed platform responsibilities and are outside this repository assessment.
