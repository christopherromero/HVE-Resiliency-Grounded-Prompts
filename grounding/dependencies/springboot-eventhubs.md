---
schema_version: 1.0.0
document_type: dependency_behavior
service: eventhubs
service_name: Azure Event Hubs
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
- id: EH-001
  title: Namespace and event hub names are deployment-injected
  severity: critical
  category: configuration
  evidence_patterns:
  - spring.cloud.azure.eventhubs
  - fullyQualifiedNamespace
  - EVENTHUB_NAMESPACE
  finding_when: namespace is hardcoded
  emit_on_failure: true
- id: EH-002
  title: Producer retries are bounded and preserve business idempotency
  severity: critical
  category: resilience
  evidence_patterns:
  - EventHubProducerClient
  - AmqpRetryOptions
  - idempotency key
  finding_when: producer retry can duplicate business effects without detection
  emit_on_failure: true
- id: EH-003
  title: Consumer processing tolerates duplicate and replayed events
  severity: critical
  category: messaging
  evidence_patterns:
  - event id
  - deduplication
  - processed event store
  finding_when: duplicate delivery causes duplicate mutation
  emit_on_failure: true
- id: EH-004
  title: Checkpoint storage is deployment-configured and recovery behavior is defined
  severity: critical
  category: messaging
  evidence_patterns:
  - checkpoint store
  - BlobCheckpointStore
  - consumer group
  finding_when: checkpoint dependency is hardcoded or loss causes undefined replay
    behavior
  emit_on_failure: true
- id: EH-005
  title: Partition-key and ordering assumptions remain valid across regions
  severity: high
  category: consistency
  evidence_patterns:
  - partitionKey
  - partitionId
  - sequence number
  finding_when: code assumes global ordering or pins partitions without documented
    need
  emit_on_failure: true
- id: EH-006
  title: Backpressure, poison events, and retry exhaustion are handled
  severity: high
  category: resilience
  evidence_patterns:
  - dead letter
  - quarantine
  - retry topic
  - max attempts
  finding_when: poison events create infinite retry or block a partition
  emit_on_failure: true
- id: EH-007
  title: Critical producer or consumer failure changes the correct readiness signal
  severity: high
  category: health
  evidence_patterns:
  - HealthIndicator
  - lag metric
  - processor state
  finding_when: service reports ready when its critical messaging role cannot operate
  emit_on_failure: true
- id: EH-008
  title: Tests cover duplicate delivery, replay, checkpoint loss, throttling, and
    recovery
  severity: high
  category: testing
  evidence_patterns:
  - mock producer
  - test consumer
  - fault injection
  finding_when: messaging failure modes are untested
  emit_on_failure: true
---

# Azure Event Hubs Active-Active Application Behavior Standard

## Purpose

This dependency-specific standard assesses how a Spring Boot microservice uses Azure Event Hubs when deployed to two active Azure regions. The local regional service endpoint is assumed to exist and be reachable through the approved private networking design.

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

## EH-001: Namespace and event hub names are deployment-injected

**Severity:** Critical  
**Category:** configuration

### Requirement

The application code and configuration must satisfy this behavior when the same artifact runs in either active region.

### Repository evidence to inspect

- `spring.cloud.azure.eventhubs`
- `fullyQualifiedNamespace`
- `EVENTHUB_NAMESPACE`

### Finding condition

Emit a finding when evidence shows that namespace is hardcoded.

### Evidence rule

Cite the file path, symbol, property, and line range when available. If the repository does not contain enough evidence, return `not_assessed` rather than assuming noncompliance.

---

## EH-002: Producer retries are bounded and preserve business idempotency

**Severity:** Critical  
**Category:** resilience

### Requirement

The application code and configuration must satisfy this behavior when the same artifact runs in either active region.

### Repository evidence to inspect

- `EventHubProducerClient`
- `AmqpRetryOptions`
- `idempotency key`

### Finding condition

Emit a finding when evidence shows that producer retry can duplicate business effects without detection.

### Evidence rule

Cite the file path, symbol, property, and line range when available. If the repository does not contain enough evidence, return `not_assessed` rather than assuming noncompliance.

---

## EH-003: Consumer processing tolerates duplicate and replayed events

**Severity:** Critical  
**Category:** messaging

### Requirement

The application code and configuration must satisfy this behavior when the same artifact runs in either active region.

### Repository evidence to inspect

- `event id`
- `deduplication`
- `processed event store`

### Finding condition

Emit a finding when evidence shows that duplicate delivery causes duplicate mutation.

### Evidence rule

Cite the file path, symbol, property, and line range when available. If the repository does not contain enough evidence, return `not_assessed` rather than assuming noncompliance.

---

## EH-004: Checkpoint storage is deployment-configured and recovery behavior is defined

**Severity:** Critical  
**Category:** messaging

### Requirement

The application code and configuration must satisfy this behavior when the same artifact runs in either active region.

### Repository evidence to inspect

- `checkpoint store`
- `BlobCheckpointStore`
- `consumer group`

### Finding condition

Emit a finding when evidence shows that checkpoint dependency is hardcoded or loss causes undefined replay behavior.

### Evidence rule

Cite the file path, symbol, property, and line range when available. If the repository does not contain enough evidence, return `not_assessed` rather than assuming noncompliance.

---

## EH-005: Partition-key and ordering assumptions remain valid across regions

**Severity:** High  
**Category:** consistency

### Requirement

The application code and configuration must satisfy this behavior when the same artifact runs in either active region.

### Repository evidence to inspect

- `partitionKey`
- `partitionId`
- `sequence number`

### Finding condition

Emit a finding when evidence shows that code assumes global ordering or pins partitions without documented need.

### Evidence rule

Cite the file path, symbol, property, and line range when available. If the repository does not contain enough evidence, return `not_assessed` rather than assuming noncompliance.

---

## EH-006: Backpressure, poison events, and retry exhaustion are handled

**Severity:** High  
**Category:** resilience

### Requirement

The application code and configuration must satisfy this behavior when the same artifact runs in either active region.

### Repository evidence to inspect

- `dead letter`
- `quarantine`
- `retry topic`
- `max attempts`

### Finding condition

Emit a finding when evidence shows that poison events create infinite retry or block a partition.

### Evidence rule

Cite the file path, symbol, property, and line range when available. If the repository does not contain enough evidence, return `not_assessed` rather than assuming noncompliance.

---

## EH-007: Critical producer or consumer failure changes the correct readiness signal

**Severity:** High  
**Category:** health

### Requirement

The application code and configuration must satisfy this behavior when the same artifact runs in either active region.

### Repository evidence to inspect

- `HealthIndicator`
- `lag metric`
- `processor state`

### Finding condition

Emit a finding when evidence shows that service reports ready when its critical messaging role cannot operate.

### Evidence rule

Cite the file path, symbol, property, and line range when available. If the repository does not contain enough evidence, return `not_assessed` rather than assuming noncompliance.

---

## EH-008: Tests cover duplicate delivery, replay, checkpoint loss, throttling, and recovery

**Severity:** High  
**Category:** testing

### Requirement

The application code and configuration must satisfy this behavior when the same artifact runs in either active region.

### Repository evidence to inspect

- `mock producer`
- `test consumer`
- `fault injection`

### Finding condition

Emit a finding when evidence shows that messaging failure modes are untested.

### Evidence rule

Cite the file path, symbol, property, and line range when available. If the repository does not contain enough evidence, return `not_assessed` rather than assuming noncompliance.

---

# Standard finding format

- **Title:** [specific code-level gap]
- **Control:** [EH-NNN]
- **Severity:** [severity]
- **Repository evidence:** [file, symbol/property, line]
- **Observed behavior:** [what code currently does]
- **Active-active risk:** [effect during regional dependency or network failure]
- **Required code/configuration change:** [specific remediation]
- **Validation test:** [test that proves the behavior]

# Non-findings

Do not create infrastructure findings such as missing second-region resources, private endpoints, zone redundancy, geo-replication, capacity, DNS, or global load-balancer configuration. Those are assumed platform responsibilities and are outside this repository assessment.
