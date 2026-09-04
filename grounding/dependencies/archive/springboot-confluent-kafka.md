---
schema_version: 1.0.0
document_type: dependency_behavior
service: confluent-kafka
service_name: Confluent Kafka
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
- id: KAFKA-001
  title: Bootstrap servers and schema/registry endpoints are deployment-injected
  severity: critical
  category: configuration
  evidence_patterns:
  - spring.kafka.bootstrap-servers
  - schema.registry.url
  - KAFKA_BOOTSTRAP_SERVERS
  finding_when: cluster endpoint is hardcoded
  emit_on_failure: true
- id: KAFKA-002
  title: Producer durability settings are explicit and approved
  severity: critical
  category: messaging
  evidence_patterns:
  - acks
  - enable.idempotence
  - retries
  - delivery.timeout.ms
  finding_when: producer can lose or duplicate records during failures
  emit_on_failure: true
- id: KAFKA-003
  title: Consumers are idempotent and tolerate replay and rebalance
  severity: critical
  category: messaging
  evidence_patterns:
  - event id
  - deduplication
  - ConsumerRebalanceListener
  finding_when: replay or rebalance duplicates business effects
  emit_on_failure: true
- id: KAFKA-004
  title: Offset commit aligns with business transaction completion
  severity: critical
  category: consistency
  evidence_patterns:
  - enable.auto.commit
  - AckMode
  - transactional.id
  finding_when: offset can commit before work or work can commit without recoverable
    offset
  emit_on_failure: true
- id: KAFKA-005
  title: Timeouts, reconnect, and backoff settings are bounded
  severity: high
  category: resilience
  evidence_patterns:
  - request.timeout.ms
  - reconnect.backoff.ms
  - retry.backoff.ms
  finding_when: client stalls or reconnect storms exceed failure budget
  emit_on_failure: true
- id: KAFKA-006
  title: Poison records have finite handling and quarantine
  severity: high
  category: messaging
  evidence_patterns:
  - DLT
  - DeadLetterPublishingRecoverer
  - max attempts
  finding_when: one record blocks a partition indefinitely
  emit_on_failure: true
- id: KAFKA-007
  title: Critical client/processor state affects readiness and telemetry
  severity: high
  category: health
  evidence_patterns:
  - KafkaHealthIndicator
  - listener container state
  - lag metric
  finding_when: application remains ready when critical stream processing is stopped
  emit_on_failure: true
- id: KAFKA-008
  title: Tests cover duplicate, replay, rebalance, broker loss, schema failure, and
    recovery
  severity: critical
  category: testing
  evidence_patterns:
  - EmbeddedKafka
  - Testcontainers Kafka
  - fault injection
  finding_when: Kafka active-active behavior is untested
  emit_on_failure: true
---

# Confluent Kafka Active-Active Application Behavior Standard

## Purpose

This dependency-specific standard assesses how a Spring Boot microservice uses Confluent Kafka when deployed to two active Azure regions. The local regional service endpoint is assumed to exist and be reachable through the approved private networking design.

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

## KAFKA-001: Bootstrap servers and schema/registry endpoints are deployment-injected

**Severity:** Critical  
**Category:** configuration

### Requirement

The application code and configuration must satisfy this behavior when the same artifact runs in either active region.

### Repository evidence to inspect

- `spring.kafka.bootstrap-servers`
- `schema.registry.url`
- `KAFKA_BOOTSTRAP_SERVERS`

### Finding condition

Emit a finding when evidence shows that cluster endpoint is hardcoded.

### Evidence rule

Cite the file path, symbol, property, and line range when available. If the repository does not contain enough evidence, return `not_assessed` rather than assuming noncompliance.

---

## KAFKA-002: Producer durability settings are explicit and approved

**Severity:** Critical  
**Category:** messaging

### Requirement

The application code and configuration must satisfy this behavior when the same artifact runs in either active region.

### Repository evidence to inspect

- `acks`
- `enable.idempotence`
- `retries`
- `delivery.timeout.ms`

### Finding condition

Emit a finding when evidence shows that producer can lose or duplicate records during failures.

### Evidence rule

Cite the file path, symbol, property, and line range when available. If the repository does not contain enough evidence, return `not_assessed` rather than assuming noncompliance.

---

## KAFKA-003: Consumers are idempotent and tolerate replay and rebalance

**Severity:** Critical  
**Category:** messaging

### Requirement

The application code and configuration must satisfy this behavior when the same artifact runs in either active region.

### Repository evidence to inspect

- `event id`
- `deduplication`
- `ConsumerRebalanceListener`

### Finding condition

Emit a finding when evidence shows that replay or rebalance duplicates business effects.

### Evidence rule

Cite the file path, symbol, property, and line range when available. If the repository does not contain enough evidence, return `not_assessed` rather than assuming noncompliance.

---

## KAFKA-004: Offset commit aligns with business transaction completion

**Severity:** Critical  
**Category:** consistency

### Requirement

The application code and configuration must satisfy this behavior when the same artifact runs in either active region.

### Repository evidence to inspect

- `enable.auto.commit`
- `AckMode`
- `transactional.id`

### Finding condition

Emit a finding when evidence shows that offset can commit before work or work can commit without recoverable offset.

### Evidence rule

Cite the file path, symbol, property, and line range when available. If the repository does not contain enough evidence, return `not_assessed` rather than assuming noncompliance.

---

## KAFKA-005: Timeouts, reconnect, and backoff settings are bounded

**Severity:** High  
**Category:** resilience

### Requirement

The application code and configuration must satisfy this behavior when the same artifact runs in either active region.

### Repository evidence to inspect

- `request.timeout.ms`
- `reconnect.backoff.ms`
- `retry.backoff.ms`

### Finding condition

Emit a finding when evidence shows that client stalls or reconnect storms exceed failure budget.

### Evidence rule

Cite the file path, symbol, property, and line range when available. If the repository does not contain enough evidence, return `not_assessed` rather than assuming noncompliance.

---

## KAFKA-006: Poison records have finite handling and quarantine

**Severity:** High  
**Category:** messaging

### Requirement

The application code and configuration must satisfy this behavior when the same artifact runs in either active region.

### Repository evidence to inspect

- `DLT`
- `DeadLetterPublishingRecoverer`
- `max attempts`

### Finding condition

Emit a finding when evidence shows that one record blocks a partition indefinitely.

### Evidence rule

Cite the file path, symbol, property, and line range when available. If the repository does not contain enough evidence, return `not_assessed` rather than assuming noncompliance.

---

## KAFKA-007: Critical client/processor state affects readiness and telemetry

**Severity:** High  
**Category:** health

### Requirement

The application code and configuration must satisfy this behavior when the same artifact runs in either active region.

### Repository evidence to inspect

- `KafkaHealthIndicator`
- `listener container state`
- `lag metric`

### Finding condition

Emit a finding when evidence shows that application remains ready when critical stream processing is stopped.

### Evidence rule

Cite the file path, symbol, property, and line range when available. If the repository does not contain enough evidence, return `not_assessed` rather than assuming noncompliance.

---

## KAFKA-008: Tests cover duplicate, replay, rebalance, broker loss, schema failure, and recovery

**Severity:** Critical  
**Category:** testing

### Requirement

The application code and configuration must satisfy this behavior when the same artifact runs in either active region.

### Repository evidence to inspect

- `EmbeddedKafka`
- `Testcontainers Kafka`
- `fault injection`

### Finding condition

Emit a finding when evidence shows that Kafka active-active behavior is untested.

### Evidence rule

Cite the file path, symbol, property, and line range when available. If the repository does not contain enough evidence, return `not_assessed` rather than assuming noncompliance.

---

# Standard finding format

- **Title:** [specific code-level gap]
- **Control:** [KAFKA-NNN]
- **Severity:** [severity]
- **Repository evidence:** [file, symbol/property, line]
- **Observed behavior:** [what code currently does]
- **Active-active risk:** [effect during regional dependency or network failure]
- **Required code/configuration change:** [specific remediation]
- **Validation test:** [test that proves the behavior]

# Non-findings

Do not create infrastructure findings such as missing second-region resources, private endpoints, zone redundancy, geo-replication, capacity, DNS, or global load-balancer configuration. Those are assumed platform responsibilities and are outside this repository assessment.
