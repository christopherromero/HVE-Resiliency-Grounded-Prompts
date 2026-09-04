---
schema_version: 1.0.0
document_type: dependency_behavior
service: appgateway-glb
service_name: Application Gateway and Global Load Balancer Behavior
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
- id: GLB-001
  title: Application exposes Spring Boot readiness and liveness endpoints
  severity: critical
  category: health
  evidence_patterns:
  - /actuator/health/readiness
  - /actuator/health/liveness
  finding_when: required probe endpoints are absent
  emit_on_failure: true
- id: GLB-002
  title: Critical dependency failure propagates to readiness after bounded retries
  severity: critical
  category: health
  evidence_patterns:
  - HealthIndicator
  - readiness group
  - AvailabilityChangeEvent
  finding_when: failed regional dependency leaves pod ready
  emit_on_failure: true
- id: GLB-003
  title: Liveness excludes external dependency health
  severity: critical
  category: health
  evidence_patterns:
  - liveness group
  finding_when: dependency outage triggers pod restart loops
  emit_on_failure: true
- id: GLB-004
  title: Health endpoint is fast, local, bounded, and representative
  severity: critical
  category: health
  evidence_patterns:
  - probe timeout
  - health cache
  - main port
  finding_when: health check hangs, overloads dependencies, or bypasses the serving
    path
  emit_on_failure: true
- id: GLB-005
  title: Application handles forwarded headers and original scheme correctly
  severity: high
  category: http
  evidence_patterns:
  - server.forward-headers-strategy
  - ForwardedHeaderFilter
  finding_when: redirect, cookie, callback, or security behavior fails behind proxies
  emit_on_failure: true
- id: GLB-006
  title: Session and authentication state do not require region stickiness
  severity: critical
  category: state
  evidence_patterns:
  - stateless session
  - external session store
  - JWT
  finding_when: traffic movement to another region loses required state
  emit_on_failure: true
- id: GLB-007
  title: Graceful shutdown removes readiness before terminating work
  severity: high
  category: lifecycle
  evidence_patterns:
  - server.shutdown=graceful
  - preStop
  - readiness transition
  finding_when: terminating pod continues receiving traffic or drops work
  emit_on_failure: true
- id: GLB-008
  title: Tests verify probe transitions, recovery, and regional traffic eligibility
  severity: critical
  category: testing
  evidence_patterns:
  - Actuator integration test
  - fault injection
  finding_when: GLB-relevant health semantics are untested
  emit_on_failure: true
---

# Application Gateway and Global Load Balancer Behavior Active-Active Application Behavior Standard

## Purpose

This dependency-specific standard assesses how a Spring Boot microservice uses Application Gateway and Global Load Balancer Behavior when deployed to two active Azure regions. The local regional service endpoint is assumed to exist and be reachable through the approved private networking design.

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

## GLB-001: Application exposes Spring Boot readiness and liveness endpoints

**Severity:** Critical  
**Category:** health

### Requirement

The application code and configuration must satisfy this behavior when the same artifact runs in either active region.

### Repository evidence to inspect

- `/actuator/health/readiness`
- `/actuator/health/liveness`

### Finding condition

Emit a finding when evidence shows that required probe endpoints are absent.

### Evidence rule

Cite the file path, symbol, property, and line range when available. If the repository does not contain enough evidence, return `not_assessed` rather than assuming noncompliance.

---

## GLB-002: Critical dependency failure propagates to readiness after bounded retries

**Severity:** Critical  
**Category:** health

### Requirement

The application code and configuration must satisfy this behavior when the same artifact runs in either active region.

### Repository evidence to inspect

- `HealthIndicator`
- `readiness group`
- `AvailabilityChangeEvent`

### Finding condition

Emit a finding when evidence shows that failed regional dependency leaves pod ready.

### Evidence rule

Cite the file path, symbol, property, and line range when available. If the repository does not contain enough evidence, return `not_assessed` rather than assuming noncompliance.

---

## GLB-003: Liveness excludes external dependency health

**Severity:** Critical  
**Category:** health

### Requirement

The application code and configuration must satisfy this behavior when the same artifact runs in either active region.

### Repository evidence to inspect

- `liveness group`

### Finding condition

Emit a finding when evidence shows that dependency outage triggers pod restart loops.

### Evidence rule

Cite the file path, symbol, property, and line range when available. If the repository does not contain enough evidence, return `not_assessed` rather than assuming noncompliance.

---

## GLB-004: Health endpoint is fast, local, bounded, and representative

**Severity:** Critical  
**Category:** health

### Requirement

The application code and configuration must satisfy this behavior when the same artifact runs in either active region.

### Repository evidence to inspect

- `probe timeout`
- `health cache`
- `main port`

### Finding condition

Emit a finding when evidence shows that health check hangs, overloads dependencies, or bypasses the serving path.

### Evidence rule

Cite the file path, symbol, property, and line range when available. If the repository does not contain enough evidence, return `not_assessed` rather than assuming noncompliance.

---

## GLB-005: Application handles forwarded headers and original scheme correctly

**Severity:** High  
**Category:** http

### Requirement

The application code and configuration must satisfy this behavior when the same artifact runs in either active region.

### Repository evidence to inspect

- `server.forward-headers-strategy`
- `ForwardedHeaderFilter`

### Finding condition

Emit a finding when evidence shows that redirect, cookie, callback, or security behavior fails behind proxies.

### Evidence rule

Cite the file path, symbol, property, and line range when available. If the repository does not contain enough evidence, return `not_assessed` rather than assuming noncompliance.

---

## GLB-006: Session and authentication state do not require region stickiness

**Severity:** Critical  
**Category:** state

### Requirement

The application code and configuration must satisfy this behavior when the same artifact runs in either active region.

### Repository evidence to inspect

- `stateless session`
- `external session store`
- `JWT`

### Finding condition

Emit a finding when evidence shows that traffic movement to another region loses required state.

### Evidence rule

Cite the file path, symbol, property, and line range when available. If the repository does not contain enough evidence, return `not_assessed` rather than assuming noncompliance.

---

## GLB-007: Graceful shutdown removes readiness before terminating work

**Severity:** High  
**Category:** lifecycle

### Requirement

The application code and configuration must satisfy this behavior when the same artifact runs in either active region.

### Repository evidence to inspect

- `server.shutdown=graceful`
- `preStop`
- `readiness transition`

### Finding condition

Emit a finding when evidence shows that terminating pod continues receiving traffic or drops work.

### Evidence rule

Cite the file path, symbol, property, and line range when available. If the repository does not contain enough evidence, return `not_assessed` rather than assuming noncompliance.

---

## GLB-008: Tests verify probe transitions, recovery, and regional traffic eligibility

**Severity:** Critical  
**Category:** testing

### Requirement

The application code and configuration must satisfy this behavior when the same artifact runs in either active region.

### Repository evidence to inspect

- `Actuator integration test`
- `fault injection`

### Finding condition

Emit a finding when evidence shows that GLB-relevant health semantics are untested.

### Evidence rule

Cite the file path, symbol, property, and line range when available. If the repository does not contain enough evidence, return `not_assessed` rather than assuming noncompliance.

---

# Standard finding format

- **Title:** [specific code-level gap]
- **Control:** [GLB-NNN]
- **Severity:** [severity]
- **Repository evidence:** [file, symbol/property, line]
- **Observed behavior:** [what code currently does]
- **Active-active risk:** [effect during regional dependency or network failure]
- **Required code/configuration change:** [specific remediation]
- **Validation test:** [test that proves the behavior]

# Non-findings

Do not create infrastructure findings such as missing second-region resources, private endpoints, zone redundancy, geo-replication, capacity, DNS, or global load-balancer configuration. Those are assumed platform responsibilities and are outside this repository assessment.
