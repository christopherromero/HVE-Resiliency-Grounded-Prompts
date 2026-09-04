---
schema_version: 2.0.0
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
- id: KV-009
  title: Startup secret and certificate loading has an explicit bounded contract
  severity: critical
  category: startup
  evidence_patterns:
  - Spring Cloud Azure Key Vault property source
  - SecretClient
  - CertificateClient
  - fail-fast
  - startup timeout
  - last known good
  finding_when: startup can wait indefinitely for Key Vault, or the application proceeds
    with unresolved required material without an explicit and tested policy
  emit_on_failure: true
- id: KV-010
  title: Secret and certificate refresh updates initialized consumers safely
  severity: high
  category: recovery
  evidence_patterns:
  - '@RefreshScope'
  - EnvironmentChangeEvent
  - client recreation
  - connection pool
  - WebClient bean
  - SSLContext reload
  - scheduled refresh
  finding_when: rotated values are rebound but initialized clients, pools, SDK objects,
    TLS contexts, executors, or caches continue to use old material without a documented
    restart contract
  emit_on_failure: true
- id: KV-011
  title: Runtime certificate and trust-material retrieval is bounded and cached
  severity: critical
  category: resilience
  evidence_patterns:
  - CertificateClient
  - KeyStore
  - SSLContext
  - certificate download
  - trust material cache
  - notAfter
  finding_when: certificate or trust material is retrieved on every business request,
    lacks bounded timeout or controlled caching, or has no safe behavior during a
    transient vault outage
  emit_on_failure: true
- id: KV-012
  title: Certificate rotation and expiration are observable and tested
  severity: high
  category: testing
  evidence_patterns:
  - notAfter
  - certificate expiration metric
  - rotation test
  - SSLContext reload
  - keystore reload
  - certificate version
  finding_when: certificate expiration is not monitored or rotation is not proven
    to update the effective client or server TLS context without unsafe interruption
  emit_on_failure: true
- id: KV-013
  title: Secret and credential diagnostics are sanitized
  severity: critical
  category: security
  evidence_patterns:
  - log.info
  - log.error
  - '@ToString'
  - Authorization header
  - HMAC
  - APIM key
  - PAN
  - connection string
  - health details
  finding_when: logs, exceptions, health details, traces, or generated string representations
    can disclose secrets, credentials, signed headers, PCI or PII, protected payloads,
    or full connection strings
  emit_on_failure: true
- id: KV-014
  title: Key Vault readiness participation is topology-aware
  severity: critical
  category: health
  evidence_patterns:
  - HealthIndicator
  - ReactiveHealthIndicator
  - keyVault readiness group
  - cached secret
  - live vault access
  finding_when: Key Vault is blindly added to readiness, omitted when every request
    requires live regional vault access, or included in liveness
  emit_on_failure: true
- id: KV-015
  title: Cached last-known-good material is security bounded
  severity: critical
  category: security
  evidence_patterns:
  - last known good
  - TTL
  - expiresOn
  - notAfter
  - refresh failure
  - revocation policy
  finding_when: cached secret, token, certificate, or trust material can be used beyond
    expiration, beyond an approved maximum stale interval, or without fail-closed
    behavior when validity cannot be established
  emit_on_failure: true
- id: KV-016
  title: Key Vault failure and recovery telemetry is actionable without value disclosure
  severity: high
  category: observability
  evidence_patterns:
  - Micrometer
  - vault operation latency
  - throttling metric
  - refresh success
  - refresh failure
  - credential failure
  - expiration alert
  - region tag
  finding_when: vault access, refresh, throttling, credential, expiration, or recovery
    events are not measurable, cannot be attributed to a region, or diagnostics include
    protected values
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

## Dependency-specific quality caveats

- `@RefreshScope` alone does not prove that initialized clients, pools, caches, executors, or TLS contexts use rotated material.
- Do not add every external dependency to readiness, and never add Key Vault or another external dependency to liveness.
- Last-known-good material must remain cryptographically valid and inside an approved stale interval.
- Do not infer missing regional vaults, identity assignments, private endpoints, DNS, or secret synchronization from absent repository evidence.
- Do not prescribe numeric retry, timeout, refresh, or stale intervals without workload and security evidence.
- Diagnostics must never reveal secrets, certificates, signed headers, PCI or PII, or full protected configuration.

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

## KV-009: Startup secret and certificate loading has an explicit bounded contract

**Severity:** Critical  
**Category:** startup

### Requirement

Required startup secrets and certificates must be obtained within a configurable bounded interval and follow an explicit fail-fast or approved last-known-good policy. Startup failure must be visible to orchestration and must not leave a process running with incomplete protected configuration.

### Repository evidence to inspect

- `Spring Cloud Azure Key Vault property source`
- `SecretClient`
- `CertificateClient`
- `fail-fast`
- `startup timeout`
- `last known good`

### Finding condition

Emit a finding when evidence shows that startup can wait indefinitely for Key Vault, or the application proceeds with unresolved required material without an explicit and tested policy.

### Evidence rule

Cite the file path, symbol, property, and line range when available. Evaluate effective runtime behavior rather than the presence of an annotation, library, property name, or default alone. If the repository does not contain enough evidence, return `not_assessed` rather than assuming noncompliance.

### Quality caveats

- Do not recommend indefinite startup blocking.
- Do not infer that a regional vault, private endpoint, DNS record, or identity assignment is missing when deployment evidence is unavailable.
- Last-known-good startup behavior is allowed only when the material remains valid and the application can operate safely with it.

---

## KV-010: Secret and certificate refresh updates initialized consumers safely

**Severity:** High  
**Category:** recovery

### Requirement

Secret and certificate rotation must reach the initialized objects that consume the material. If safe live reload is not supported, the application must define, observe, and test a controlled restart strategy that preserves availability across regional instances.

### Repository evidence to inspect

- `@RefreshScope`
- `EnvironmentChangeEvent`
- `client recreation`
- `connection pool`
- `WebClient bean`
- `SSLContext reload`
- `scheduled refresh`

### Finding condition

Emit a finding when evidence shows that rotated values are rebound but initialized clients, pools, SDK objects, TLS contexts, executors, or caches continue to use old material without a documented restart contract.

### Evidence rule

Cite the file path, symbol, property, and line range when available. Evaluate effective runtime behavior rather than the presence of an annotation, library, property name, or default alone. If the repository does not contain enough evidence, return `not_assessed` rather than assuming noncompliance.

### Quality caveats

- `@RefreshScope` alone does not prove that already-created clients, connection pools, executors, caches, or TLS contexts consume the new value.
- Test rotation against the effective consumer object, not only configuration-property rebinding.
- Do not recreate high-cost clients on every request as a substitute for a controlled refresh lifecycle.

---

## KV-011: Runtime certificate and trust-material retrieval is bounded and cached

**Severity:** Critical  
**Category:** resilience

### Requirement

Runtime certificate and trust-material access must be bounded, protected by controlled caching, and removed from the synchronous business-request hot path. The application must define rotation, expiration, cache invalidation, and transient-vault-failure behavior.

### Repository evidence to inspect

- `CertificateClient`
- `KeyStore`
- `SSLContext`
- `certificate download`
- `trust material cache`
- `notAfter`

### Finding condition

Emit a finding when evidence shows that certificate or trust material is retrieved on every business request, lacks bounded timeout or controlled caching, or has no safe behavior during a transient vault outage.

### Evidence rule

Cite the file path, symbol, property, and line range when available. Evaluate effective runtime behavior rather than the presence of an annotation, library, property name, or default alone. If the repository does not contain enough evidence, return `not_assessed` rather than assuming noncompliance.

### Quality caveats

- Cached material may be used only while cryptographically valid and within an approved safety window.
- Do not extend use beyond expiration or applicable revocation policy to preserve availability.
- Certificate retrieval, parsing, and TLS-context construction may each require separate bounds.

---

## KV-012: Certificate rotation and expiration are observable and tested

**Severity:** High  
**Category:** testing

### Requirement

The application must monitor certificate validity and version and test rotation, reload, rollback, and failure behavior against the effective TLS consumer. Alerts must provide sufficient lead time without disclosing protected material.

### Repository evidence to inspect

- `notAfter`
- `certificate expiration metric`
- `rotation test`
- `SSLContext reload`
- `keystore reload`
- `certificate version`

### Finding condition

Emit a finding when evidence shows that certificate expiration is not monitored or rotation is not proven to update the effective client or server TLS context without unsafe interruption.

### Evidence rule

Cite the file path, symbol, property, and line range when available. Evaluate effective runtime behavior rather than the presence of an annotation, library, property name, or default alone. If the repository does not contain enough evidence, return `not_assessed` rather than assuming noncompliance.

### Quality caveats

- Replacing a mounted file, property, or secret does not prove that an existing `SSLContext`, connection pool, or SDK client reloads it.
- Tests must verify a new connection uses the rotated material and that old connections retire safely.

---

## KV-013: Secret and credential diagnostics are sanitized

**Severity:** Critical  
**Category:** security

### Requirement

Secret and certificate failures must be observable without emitting secret values, protected payloads, signed authentication material, card or account data, or full sensitive configuration. Sanitization must apply to normal logs, exception logs, structured logging, generated `toString()` output, traces, and Actuator details.

### Repository evidence to inspect

- `log.info`
- `log.error`
- `@ToString`
- `Authorization header`
- `HMAC`
- `APIM key`
- `PAN`
- `connection string`
- `health details`

### Finding condition

Emit a finding when evidence shows that logs, exceptions, health details, traces, or generated string representations can disclose secrets, credentials, signed headers, PCI or PII, protected payloads, or full connection strings.

### Evidence rule

Cite the file path, symbol, property, and line range when available. Evaluate effective runtime behavior rather than the presence of an annotation, library, property name, or default alone. If the repository does not contain enough evidence, return `not_assessed` rather than assuming noncompliance.

### Quality caveats

- Inspect Lombok-generated `toString()`, request and response logging, exception objects, and structured-logging serializers.
- Masking at the Config Server or log platform does not remove the need to prevent application-side disclosure.
- Health details must not expose secret names, values, account identifiers, or protected endpoints to untrusted callers.

---

## KV-014: Key Vault readiness participation is topology-aware

**Severity:** Critical  
**Category:** health

### Requirement

Key Vault may gate readiness only when live access to the region-local vault is required for safe request processing. If a running instance can safely use already-bound valid material, prefer bounded refresh behavior, failure telemetry, and expiration alerts over draining otherwise serviceable instances. Key Vault must never participate in liveness.

### Repository evidence to inspect

- `HealthIndicator`
- `ReactiveHealthIndicator`
- `keyVault readiness group`
- `cached secret`
- `live vault access`

### Finding condition

Emit a finding when evidence shows that Key Vault is blindly added to readiness, omitted when every request requires live regional vault access, or included in liveness.

### Evidence rule

Cite the file path, symbol, property, and line range when available. Evaluate effective runtime behavior rather than the presence of an annotation, library, property name, or default alone. If the repository does not contain enough evidence, return `not_assessed` rather than assuming noncompliance.

### Quality caveats

- Do not add every external dependency to readiness automatically.
- A globally shared vault endpoint in readiness can drain both regions simultaneously.
- Evaluate startup dependence, request-time dependence, cached-material validity, and regional topology separately.

---

## KV-015: Cached last-known-good material is security bounded

**Severity:** Critical  
**Category:** security

### Requirement

Last-known-good material must have an explicit validity check, configurable maximum stale interval, fail-closed boundary, and actionable telemetry for refresh failure and approaching expiration. Availability behavior must remain subordinate to cryptographic and security validity.

### Repository evidence to inspect

- `last known good`
- `TTL`
- `expiresOn`
- `notAfter`
- `refresh failure`
- `revocation policy`

### Finding condition

Emit a finding when evidence shows that cached secret, token, certificate, or trust material can be used beyond expiration, beyond an approved maximum stale interval, or without fail-closed behavior when validity cannot be established.

### Evidence rule

Cite the file path, symbol, property, and line range when available. Evaluate effective runtime behavior rather than the presence of an annotation, library, property name, or default alone. If the repository does not contain enough evidence, return `not_assessed` rather than assuming noncompliance.

### Quality caveats

- Do not prescribe a stale interval without security-owner and workload-owner approval.
- Never extend use beyond certificate expiration, token expiration, or an applicable revocation requirement.
- A cached client secret may have different rotation and validity semantics from a certificate or access token; evaluate the actual material type.

---

## KV-016: Key Vault failure and recovery telemetry is actionable without value disclosure

**Severity:** High  
**Category:** observability

### Requirement

The application must emit sanitized metrics and structured events for Key Vault access latency, throttling, denial, refresh, credential failure, certificate expiration, and recovery. Signals must identify the application, dependency operation, and serving region without including secret or certificate values.

### Repository evidence to inspect

- `Micrometer`
- `vault operation latency`
- `throttling metric`
- `refresh success`
- `refresh failure`
- `credential failure`
- `expiration alert`
- `region tag`

### Finding condition

Emit a finding when evidence shows that vault access, refresh, throttling, credential, expiration, or recovery events are not measurable, cannot be attributed to a region, or diagnostics include protected values.

### Evidence rule

Cite the file path, symbol, property, and line range when available. Evaluate effective runtime behavior rather than the presence of an annotation, library, property name, or default alone. If the repository does not contain enough evidence, return `not_assessed` rather than assuming noncompliance.

### Quality caveats

- Record event type, status, latency, and safe identifiers only. Never record secret or certificate values.
- Avoid high-cardinality tags such as full vault URLs, secret names when sensitive, request IDs from untrusted input, or exception messages.


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
