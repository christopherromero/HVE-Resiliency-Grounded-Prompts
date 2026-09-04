---
schema_version: 1.0.0
document_type: dependency_behavior
service: apim
service_name: Azure API Management Client Behavior
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
- id: APIM-001
  title: Upstream API base URL is deployment-injected
  severity: critical
  category: configuration
  evidence_patterns:
  - base-url
  - WebClient.Builder
  - RestClient.Builder
  - FeignClient
  finding_when: APIM hostname or region is hardcoded
  emit_on_failure: true
- id: APIM-002
  title: Client honors bounded connect, response, and overall timeouts
  severity: critical
  category: resilience
  evidence_patterns:
  - WebClient timeout
  - HttpClient responseTimeout
  - Feign options
  finding_when: outbound API call can exceed failure budget
  emit_on_failure: true
- id: APIM-003
  title: Retries are bounded and restricted to safe operations
  severity: critical
  category: resilience
  evidence_patterns:
  - Retry
  - Retry-After
  - HTTP method filtering
  finding_when: non-idempotent request can be duplicated or 429/5xx causes retry storm
  emit_on_failure: true
- id: APIM-004
  title: Circuit breaker and bulkhead isolate failing APIs
  severity: high
  category: resilience
  evidence_patterns:
  - CircuitBreaker
  - Bulkhead
  - separate pool
  finding_when: failed API exhausts shared application resources
  emit_on_failure: true
- id: APIM-005
  title: Forwarded host, scheme, and client headers are handled safely
  severity: high
  category: http
  evidence_patterns:
  - ForwardedHeaderFilter
  - X-Forwarded-For
  - X-Forwarded-Proto
  finding_when: redirects, links, or security logic break behind regional gateways
  emit_on_failure: true
- id: APIM-006
  title: Correlation and region headers propagate through calls
  severity: medium
  category: observability
  evidence_patterns:
  - traceparent
  - correlation id
  - region tag
  finding_when: distributed requests cannot be traced by region
  emit_on_failure: true
- id: APIM-007
  title: Critical upstream loss affects readiness only when no degraded mode exists
  severity: high
  category: health
  evidence_patterns:
  - HealthIndicator
  - fallback
  - readiness group
  finding_when: health does not align with business capability
  emit_on_failure: true
- id: APIM-008
  title: Tests cover 429, 5xx, timeout, connection reset, duplicate prevention, and
    recovery
  severity: high
  category: testing
  evidence_patterns:
  - WireMock
  - MockWebServer
  - fault tests
  finding_when: client failure behavior is untested
  emit_on_failure: true
---

# Azure API Management Client Behavior Active-Active Application Behavior Standard

## Purpose

This dependency-specific standard assesses how a Spring Boot microservice uses Azure API Management Client Behavior when deployed to two active Azure regions. The local regional service endpoint is assumed to exist and be reachable through the approved private networking design.

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

## APIM-001: Upstream API base URL is deployment-injected

**Severity:** Critical  
**Category:** configuration

### Requirement

The application code and configuration must satisfy this behavior when the same artifact runs in either active region.

### Repository evidence to inspect

- `base-url`
- `WebClient.Builder`
- `RestClient.Builder`
- `FeignClient`

### Finding condition

Emit a finding when evidence shows that APIM hostname or region is hardcoded.

### Evidence rule

Cite the file path, symbol, property, and line range when available. If the repository does not contain enough evidence, return `not_assessed` rather than assuming noncompliance.

---

## APIM-002: Client honors bounded connect, response, and overall timeouts

**Severity:** Critical  
**Category:** resilience

### Requirement

The application code and configuration must satisfy this behavior when the same artifact runs in either active region.

### Repository evidence to inspect

- `WebClient timeout`
- `HttpClient responseTimeout`
- `Feign options`

### Finding condition

Emit a finding when evidence shows that outbound API call can exceed failure budget.

### Evidence rule

Cite the file path, symbol, property, and line range when available. If the repository does not contain enough evidence, return `not_assessed` rather than assuming noncompliance.

---

## APIM-003: Retries are bounded and restricted to safe operations

**Severity:** Critical  
**Category:** resilience

### Requirement

The application code and configuration must satisfy this behavior when the same artifact runs in either active region.

### Repository evidence to inspect

- `Retry`
- `Retry-After`
- `HTTP method filtering`

### Finding condition

Emit a finding when evidence shows that non-idempotent request can be duplicated or 429/5xx causes retry storm.

### Evidence rule

Cite the file path, symbol, property, and line range when available. If the repository does not contain enough evidence, return `not_assessed` rather than assuming noncompliance.

---

## APIM-004: Circuit breaker and bulkhead isolate failing APIs

**Severity:** High  
**Category:** resilience

### Requirement

The application code and configuration must satisfy this behavior when the same artifact runs in either active region.

### Repository evidence to inspect

- `CircuitBreaker`
- `Bulkhead`
- `separate pool`

### Finding condition

Emit a finding when evidence shows that failed API exhausts shared application resources.

### Evidence rule

Cite the file path, symbol, property, and line range when available. If the repository does not contain enough evidence, return `not_assessed` rather than assuming noncompliance.

---

## APIM-005: Forwarded host, scheme, and client headers are handled safely

**Severity:** High  
**Category:** http

### Requirement

The application code and configuration must satisfy this behavior when the same artifact runs in either active region.

### Repository evidence to inspect

- `ForwardedHeaderFilter`
- `X-Forwarded-For`
- `X-Forwarded-Proto`

### Finding condition

Emit a finding when evidence shows that redirects, links, or security logic break behind regional gateways.

### Evidence rule

Cite the file path, symbol, property, and line range when available. If the repository does not contain enough evidence, return `not_assessed` rather than assuming noncompliance.

---

## APIM-006: Correlation and region headers propagate through calls

**Severity:** Medium  
**Category:** observability

### Requirement

The application code and configuration must satisfy this behavior when the same artifact runs in either active region.

### Repository evidence to inspect

- `traceparent`
- `correlation id`
- `region tag`

### Finding condition

Emit a finding when evidence shows that distributed requests cannot be traced by region.

### Evidence rule

Cite the file path, symbol, property, and line range when available. If the repository does not contain enough evidence, return `not_assessed` rather than assuming noncompliance.

---

## APIM-007: Critical upstream loss affects readiness only when no degraded mode exists

**Severity:** High  
**Category:** health

### Requirement

The application code and configuration must satisfy this behavior when the same artifact runs in either active region.

### Repository evidence to inspect

- `HealthIndicator`
- `fallback`
- `readiness group`

### Finding condition

Emit a finding when evidence shows that health does not align with business capability.

### Evidence rule

Cite the file path, symbol, property, and line range when available. If the repository does not contain enough evidence, return `not_assessed` rather than assuming noncompliance.

---

## APIM-008: Tests cover 429, 5xx, timeout, connection reset, duplicate prevention, and recovery

**Severity:** High  
**Category:** testing

### Requirement

The application code and configuration must satisfy this behavior when the same artifact runs in either active region.

### Repository evidence to inspect

- `WireMock`
- `MockWebServer`
- `fault tests`

### Finding condition

Emit a finding when evidence shows that client failure behavior is untested.

### Evidence rule

Cite the file path, symbol, property, and line range when available. If the repository does not contain enough evidence, return `not_assessed` rather than assuming noncompliance.

---

# Standard finding format

- **Title:** [specific code-level gap]
- **Control:** [APIM-NNN]
- **Severity:** [severity]
- **Repository evidence:** [file, symbol/property, line]
- **Observed behavior:** [what code currently does]
- **Active-active risk:** [effect during regional dependency or network failure]
- **Required code/configuration change:** [specific remediation]
- **Validation test:** [test that proves the behavior]

# Non-findings

Do not create infrastructure findings such as missing second-region resources, private endpoints, zone redundancy, geo-replication, capacity, DNS, or global load-balancer configuration. Those are assumed platform responsibilities and are outside this repository assessment.
