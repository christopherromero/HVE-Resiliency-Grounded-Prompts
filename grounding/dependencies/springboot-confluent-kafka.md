---
schema_version: 3.0.0
document_type: dependency_behavior
service: confluent-kafka
service_name: Confluent Kafka Multi-Region
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
  title: Bootstrap, schema, and registry endpoints are deployment-injected for the
    selected Kafka scenario
  severity: critical
  category: configuration
  evidence_patterns:
  - spring.kafka.bootstrap-servers
  - schema.registry.url
  - KAFKA_BOOTSTRAP_SERVERS
  finding_when: cluster or registry endpoint is hardcoded, normal regional routing
    conflicts with the selected scenario, or both clusters are combined without an
    approved client-routing design
  emit_on_failure: true
  applies_when: confluent-kafka is used; apply under any resolved operating scenario
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
  applies_when: confluent-kafka is used; apply under any resolved operating scenario
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
  applies_when: confluent-kafka is used; apply under any resolved operating scenario
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
  applies_when: confluent-kafka is used; apply under any resolved operating scenario
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
  applies_when: confluent-kafka is used; apply under any resolved operating scenario
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
  applies_when: confluent-kafka is used; apply under any resolved operating scenario
- id: KAFKA-007
  title: Critical client and processor state has scenario-aware readiness and telemetry
    behavior
  severity: high
  category: health
  evidence_patterns:
  - KafkaHealthIndicator
  - listener container state
  - lag metric
  finding_when: critical processing failure is invisible, an intentionally inactive
    standby is treated as failed, or remote/shared cluster failure drains healthy
    regional capacity
  emit_on_failure: true
  applies_when: confluent-kafka is used; apply under any resolved operating scenario
- id: KAFKA-008
  title: Tests cover duplicate, replay, rebalance, broker loss, schema failure, recovery,
    and the selected operating scenario
  severity: critical
  category: testing
  evidence_patterns:
  - EmbeddedKafka
  - Testcontainers Kafka
  - fault injection
  finding_when: Kafka behavior for the selected operating scenario is untested
  emit_on_failure: true
  applies_when: confluent-kafka is used; apply under any resolved operating scenario
- id: KAFKA-009
  title: Selected Kafka operating scenario is explicit and evidence-backed
  severity: critical
  category: architecture
  applies_when: confluent-kafka is used
  evidence_patterns:
  - kafka_operating_scenario
  - azure_sql role
  - cosmos_db api
  - multi-region writes
  - cluster model
  finding_when: the scenario is absent, unresolved without an evidence request, or
    conflicts with the authoritative persistence model
  emit_on_failure: true
- id: KAFKA-010
  title: Kafka processing role aligns with authoritative state ownership
  severity: critical
  category: consistency
  applies_when: Kafka processing mutates authoritative business state
  evidence_patterns:
  - authoritative_business_state
  - consumer activation
  - producer activation
  - database role
  finding_when: Kafka processing can run in a region that does not own the authoritative
    active-standby state, or active-active processing lacks multi-write-safe state
    behavior
  emit_on_failure: true
- id: KAFKA-011
  title: Topic, key, schema, group, and event identity are portable across regions
  severity: critical
  category: messaging
  applies_when: any Kafka scenario applies
  evidence_patterns:
  - topic name
  - message key
  - event id
  - schema subject
  - group.id
  - cluster name
  finding_when: physical cluster or region identity is embedded in durable event contracts,
    consumer identity is unstable, or event identity changes across retry or failover
  emit_on_failure: true
- id: KAFKA-012
  title: Scenario and regional role changes do not require rebuilding the application
  severity: high
  category: configuration
  applies_when: any Kafka scenario applies
  evidence_patterns:
  - bootstrap servers
  - schema registry
  - consumer enabled
  - producer enabled
  - region
  - cluster role
  finding_when: switching region, cluster role, or scenario requires a different code
    build or hardcoded source change
  emit_on_failure: true
- id: KAFKA-AA-001
  title: Regional clients use their local independent Kafka cluster
  severity: critical
  category: regional-affinity
  applies_when: operating scenario is independent_regional_active_active
  evidence_patterns:
  - regional bootstrap servers
  - local cluster alias
  - deployment-injected region
  finding_when: a region normally connects to the remote cluster, combines independent
    clusters in one bootstrap list, or silently falls back cross-region
  emit_on_failure: true
- id: KAFKA-AA-002
  title: Cross-cluster duplicate processing is safe
  severity: critical
  category: consistency
  applies_when: operating scenario is independent_regional_active_active
  evidence_patterns:
  - stable event id
  - dedupe store
  - unique constraint
  - idempotent consumer
  finding_when: the same business event can arrive through both independent clusters
    and duplicate a business effect
  emit_on_failure: true
- id: KAFKA-AA-003
  title: Ordering assumptions are scoped explicitly
  severity: high
  category: ordering
  applies_when: operating scenario is independent_regional_active_active
  evidence_patterns:
  - partition key
  - business sequence
  - version
  - region
  - cluster
  finding_when: the application assumes global ordering across independent regional
    clusters without an external sequence or conflict rule
  emit_on_failure: true
- id: KAFKA-AA-004
  title: Regional production and consumption remain locally autonomous
  severity: critical
  category: availability
  applies_when: operating scenario is independent_regional_active_active
  evidence_patterns:
  - local readiness
  - remote cluster health
  - dual publish
  - synchronous confirmation
  finding_when: remote cluster failure stops local processing, participates in local
    readiness, or synchronous dual-cluster publishing is required
  emit_on_failure: true
- id: KAFKA-AA-005
  title: Kafka replay and Cosmos multi-write behavior are jointly safe
  severity: critical
  category: consistency
  applies_when: active-active Kafka is aligned with Cosmos DB MongoDB API RU multi-region
    writes
  evidence_patterns:
  - document id
  - optimistic version
  - conflict policy
  - tentative write
  - reconciliation
  finding_when: Kafka replay or cross-cluster reordering can produce conflicting Cosmos
    writes without stable identity, versioning, conflict handling, or reconciliation
  emit_on_failure: true
- id: KAFKA-AA-006
  title: Active-active tests exercise both independent clusters
  severity: critical
  category: testing
  applies_when: operating scenario is independent_regional_active_active
  evidence_patterns:
  - two Kafka clusters
  - duplicate event
  - different order
  - regional outage
  - Cosmos conflict
  finding_when: tests do not prove local autonomy, duplicate tolerance, ordering behavior,
    Cosmos conflict safety, and recovery for independent clusters
  emit_on_failure: true
- id: KAFKA-AS-001
  title: Only the active regional role produces and consumes authoritative workloads
  severity: critical
  category: workload-ownership
  applies_when: operating scenario is active_standby
  evidence_patterns:
  - consumer auto-startup
  - producer enabled
  - scheduler enabled
  - active role
  finding_when: standby instances ordinarily produce, consume, schedule, or reprocess
    authoritative work
  emit_on_failure: true
- id: KAFKA-AS-002
  title: Kafka activation aligns with Azure SQL primary ownership
  severity: critical
  category: consistency
  applies_when: operating scenario is active_standby
  evidence_patterns:
  - SQL read-write listener
  - Kafka role
  - activation gate
  - ownership epoch
  finding_when: Kafka processing can activate before SQL primary ownership is verified
    or can remain active after losing authoritative database ownership
  emit_on_failure: true
- id: KAFKA-AS-003
  title: Standby activation is fail-safe and split-brain protected
  severity: critical
  category: workload-ownership
  applies_when: operating scenario is active_standby
  evidence_patterns:
  - lease
  - epoch
  - fencing token
  - feature flag
  - both-active alert
  finding_when: activation defaults enabled, relies only on a property flag where
    concurrency is possible, or stale-active processing is not fenced
  emit_on_failure: true
- id: KAFKA-AS-004
  title: Offsets and replicated topic state support controlled promotion
  severity: critical
  category: recovery
  applies_when: operating scenario is active_standby
  evidence_patterns:
  - consumer offset
  - cluster linking
  - mirror topic
  - offset sync
  - group id
  finding_when: promotion can start from an unknown or unsafe offset, lose data, or
    repeat effects without idempotency and reconciliation
  emit_on_failure: true
- id: KAFKA-AS-005
  title: Standby or mirror topics are not treated as writable before promotion
  severity: critical
  category: messaging
  applies_when: operating scenario is active_standby
  evidence_patterns:
  - mirror topic
  - read-only
  - producer bootstrap
  - promotion state
  finding_when: the application produces to passive mirror topics, interprets connectivity
    as writability, or consumes standby state before controlled activation
  emit_on_failure: true
- id: KAFKA-AS-006
  title: Failover preserves stable business and event identity
  severity: critical
  category: consistency
  applies_when: operating scenario is active_standby
  evidence_patterns:
  - event id
  - business operation id
  - database unique key
  - provider transaction id
  finding_when: failover regenerates identity or offset restoration can duplicate
    SQL-backed or external business effects
  emit_on_failure: true
- id: KAFKA-AS-007
  title: Application behavior supports ordered SQL and Kafka failover
  severity: critical
  category: recovery
  applies_when: operating scenario is active_standby
  evidence_patterns:
  - old-active fencing
  - SQL role verification
  - Kafka promotion
  - consumer activation
  - traffic enablement
  finding_when: the application can process while SQL and Kafka roles are misaligned
    or cannot stop acquisition before ownership transfer
  emit_on_failure: true
- id: KAFKA-AS-008
  title: Failback prevents reverse duplication and stale ownership
  severity: high
  category: recovery
  applies_when: operating scenario is active_standby
  evidence_patterns:
  - failback
  - reverse link
  - ownership epoch
  - offset readiness
  - fencing
  finding_when: role reversal can reactivate stale consumers/producers, replay without
    dedupe, or misalign SQL and Kafka roles
  emit_on_failure: true
- id: KAFKA-AS-009
  title: Active-standby tests cover promotion, fencing, offsets, and failback
  severity: critical
  category: testing
  applies_when: operating scenario is active_standby
  evidence_patterns:
  - SQL failover
  - Kafka promotion
  - stale active
  - both active
  - both inactive
  - failback
  finding_when: tests do not cover partial ordering, stale-active fencing, offset
    restoration, duplicate replay, both-active/both-inactive, and reverse failback
  emit_on_failure: true
scenario_policy: assessment/grounding/governance/kafka-operating-scenario-policy.yml
supported_operating_scenarios:
  independent_regional_active_active:
    description: Two independent regional Kafka clusters; regional applications normally
      use only their local cluster; database alignment is Cosmos DB for MongoDB RU
      with multi-region writes and no authoritative Azure SQL.
  active_standby:
    description: One active Kafka application-processing role and one standby role
      aligned with Azure SQL primary/standby ownership. Azure SQL presence takes precedence,
      including applications that also use Cosmos DB.
---

# Confluent Kafka Multi-Region Application Behavior Standard

## Purpose

This dependency-specific standard assesses Spring Boot use of Confluent Kafka under three approved scenarios: independent regional active-active Kafka clusters aligned with Cosmos DB for MongoDB RU multi-region writes; or active-standby Kafka aligned with Azure SQL primary/standby authoritative state. It does not assess a stretched Kafka cluster.

## Scope boundary

Assess application code, repository-owned configuration, producer/consumer lifecycle, identity, retry, offsets, replay, health, telemetry, scenario selection, and tests. Treat deployed Kafka replication, Cluster Linking, Schema Linking, ACL replication, Azure SQL role, and Cosmos multi-write enablement as external evidence unless authoritative context is supplied.

## Scenario decision

- Azure SQL used for authoritative business state: `active_standby`.
- Azure SQL plus Cosmos DB: `active_standby`.
- Cosmos DB for MongoDB RU only, with multi-region writes enabled and no authoritative Azure SQL: `independent_regional_active_active`.
- Otherwise: `unresolved`, with scenario-dependent controls `not_assessed`.

Dependency presence alone is insufficient. Use effective production responsibility and authoritative-state role.

## Evaluator workflow

1. Confirm Kafka is used by production code.
2. Read the Step 1 scenario inputs and governance policy.
3. Resolve exactly one scenario and record its rule ID.
4. Evaluate KAFKA-001 through KAFKA-012.
5. Evaluate only the selected scenario family: KAFKA-AA-*, KAFKA-AS-*, or KAFKA-DI-*.
6. Mark the other scenario family `not_applicable`.
7. Deduplicate findings by root cause.
8. Do not create infrastructure findings from missing deployed topology.

## Required statuses

- `compliant`
- `non_compliant`
- `not_assessed`
- `not_applicable`
- `accepted_risk`

## Controls

### KAFKA-001: Bootstrap, schema, and registry endpoints are deployment-injected for the selected Kafka scenario

**Severity:** Critical  
**Category:** configuration  
**Applies when:** confluent-kafka is used; apply under any resolved operating scenario

#### Requirement

The application code and repository-owned configuration must implement this behavior for the resolved Kafka operating scenario. Scenario-specific controls for the other scenario are `not_applicable`.

#### Repository evidence to inspect

- `spring.kafka.bootstrap-servers`
- `schema.registry.url`
- `KAFKA_BOOTSTRAP_SERVERS`

#### Finding condition

Emit a finding when evidence shows that cluster or registry endpoint is hardcoded, normal regional routing conflicts with the selected scenario, or both clusters are combined without an approved client-routing design.

#### Evidence rule

Cite repository-relative path, symbol/property, original assessed lines, and exact excerpt when available. Evaluate effective behavior, not the presence of a dependency or property alone. If persistence role, Cosmos multi-write state, Kafka cluster model, or deployed replication state is unavailable, return `not_assessed` and identify the required evidence.

#### Quality caveats

- Azure SQL presence as authoritative business state selects `active_standby`, even when Cosmos DB is also used.
- Cosmos DB alone selects active-active only when MongoDB API, RU throughput, and multi-region writes are evidence-backed.
- Two independent Kafka clusters do not provide global ordering or cross-cluster exactly-once behavior.
- A feature flag alone is not split-brain protection.
- Do not blindly retry ambiguous, non-idempotent business effects.
- Do not infer Cluster Linking, offset synchronization, mirror-topic promotion, or Cosmos multi-write deployment from repository absence.

---

### KAFKA-002: Producer durability settings are explicit and approved

**Severity:** Critical  
**Category:** messaging  
**Applies when:** confluent-kafka is used; apply under any resolved operating scenario

#### Requirement

The application code and repository-owned configuration must implement this behavior for the resolved Kafka operating scenario. Scenario-specific controls for the other scenario are `not_applicable`.

#### Repository evidence to inspect

- `acks`
- `enable.idempotence`
- `retries`
- `delivery.timeout.ms`

#### Finding condition

Emit a finding when evidence shows that producer can lose or duplicate records during failures.

#### Evidence rule

Cite repository-relative path, symbol/property, original assessed lines, and exact excerpt when available. Evaluate effective behavior, not the presence of a dependency or property alone. If persistence role, Cosmos multi-write state, Kafka cluster model, or deployed replication state is unavailable, return `not_assessed` and identify the required evidence.

#### Quality caveats

- Azure SQL presence as authoritative business state selects `active_standby`, even when Cosmos DB is also used.
- Cosmos DB alone selects active-active only when MongoDB API, RU throughput, and multi-region writes are evidence-backed.
- Two independent Kafka clusters do not provide global ordering or cross-cluster exactly-once behavior.
- A feature flag alone is not split-brain protection.
- Do not blindly retry ambiguous, non-idempotent business effects.
- Do not infer Cluster Linking, offset synchronization, mirror-topic promotion, or Cosmos multi-write deployment from repository absence.

---

### KAFKA-003: Consumers are idempotent and tolerate replay and rebalance

**Severity:** Critical  
**Category:** messaging  
**Applies when:** confluent-kafka is used; apply under any resolved operating scenario

#### Requirement

The application code and repository-owned configuration must implement this behavior for the resolved Kafka operating scenario. Scenario-specific controls for the other scenario are `not_applicable`.

#### Repository evidence to inspect

- `event id`
- `deduplication`
- `ConsumerRebalanceListener`

#### Finding condition

Emit a finding when evidence shows that replay or rebalance duplicates business effects.

#### Evidence rule

Cite repository-relative path, symbol/property, original assessed lines, and exact excerpt when available. Evaluate effective behavior, not the presence of a dependency or property alone. If persistence role, Cosmos multi-write state, Kafka cluster model, or deployed replication state is unavailable, return `not_assessed` and identify the required evidence.

#### Quality caveats

- Azure SQL presence as authoritative business state selects `active_standby`, even when Cosmos DB is also used.
- Cosmos DB alone selects active-active only when MongoDB API, RU throughput, and multi-region writes are evidence-backed.
- Two independent Kafka clusters do not provide global ordering or cross-cluster exactly-once behavior.
- A feature flag alone is not split-brain protection.
- Do not blindly retry ambiguous, non-idempotent business effects.
- Do not infer Cluster Linking, offset synchronization, mirror-topic promotion, or Cosmos multi-write deployment from repository absence.

---

### KAFKA-004: Offset commit aligns with business transaction completion

**Severity:** Critical  
**Category:** consistency  
**Applies when:** confluent-kafka is used; apply under any resolved operating scenario

#### Requirement

The application code and repository-owned configuration must implement this behavior for the resolved Kafka operating scenario. Scenario-specific controls for the other scenario are `not_applicable`.

#### Repository evidence to inspect

- `enable.auto.commit`
- `AckMode`
- `transactional.id`

#### Finding condition

Emit a finding when evidence shows that offset can commit before work or work can commit without recoverable offset.

#### Evidence rule

Cite repository-relative path, symbol/property, original assessed lines, and exact excerpt when available. Evaluate effective behavior, not the presence of a dependency or property alone. If persistence role, Cosmos multi-write state, Kafka cluster model, or deployed replication state is unavailable, return `not_assessed` and identify the required evidence.

#### Quality caveats

- Azure SQL presence as authoritative business state selects `active_standby`, even when Cosmos DB is also used.
- Cosmos DB alone selects active-active only when MongoDB API, RU throughput, and multi-region writes are evidence-backed.
- Two independent Kafka clusters do not provide global ordering or cross-cluster exactly-once behavior.
- A feature flag alone is not split-brain protection.
- Do not blindly retry ambiguous, non-idempotent business effects.
- Do not infer Cluster Linking, offset synchronization, mirror-topic promotion, or Cosmos multi-write deployment from repository absence.

---

### KAFKA-005: Timeouts, reconnect, and backoff settings are bounded

**Severity:** High  
**Category:** resilience  
**Applies when:** confluent-kafka is used; apply under any resolved operating scenario

#### Requirement

The application code and repository-owned configuration must implement this behavior for the resolved Kafka operating scenario. Scenario-specific controls for the other scenario are `not_applicable`.

#### Repository evidence to inspect

- `request.timeout.ms`
- `reconnect.backoff.ms`
- `retry.backoff.ms`

#### Finding condition

Emit a finding when evidence shows that client stalls or reconnect storms exceed failure budget.

#### Evidence rule

Cite repository-relative path, symbol/property, original assessed lines, and exact excerpt when available. Evaluate effective behavior, not the presence of a dependency or property alone. If persistence role, Cosmos multi-write state, Kafka cluster model, or deployed replication state is unavailable, return `not_assessed` and identify the required evidence.

#### Quality caveats

- Azure SQL presence as authoritative business state selects `active_standby`, even when Cosmos DB is also used.
- Cosmos DB alone selects active-active only when MongoDB API, RU throughput, and multi-region writes are evidence-backed.
- Two independent Kafka clusters do not provide global ordering or cross-cluster exactly-once behavior.
- A feature flag alone is not split-brain protection.
- Do not blindly retry ambiguous, non-idempotent business effects.
- Do not infer Cluster Linking, offset synchronization, mirror-topic promotion, or Cosmos multi-write deployment from repository absence.

---

### KAFKA-006: Poison records have finite handling and quarantine

**Severity:** High  
**Category:** messaging  
**Applies when:** confluent-kafka is used; apply under any resolved operating scenario

#### Requirement

The application code and repository-owned configuration must implement this behavior for the resolved Kafka operating scenario. Scenario-specific controls for the other scenario are `not_applicable`.

#### Repository evidence to inspect

- `DLT`
- `DeadLetterPublishingRecoverer`
- `max attempts`

#### Finding condition

Emit a finding when evidence shows that one record blocks a partition indefinitely.

#### Evidence rule

Cite repository-relative path, symbol/property, original assessed lines, and exact excerpt when available. Evaluate effective behavior, not the presence of a dependency or property alone. If persistence role, Cosmos multi-write state, Kafka cluster model, or deployed replication state is unavailable, return `not_assessed` and identify the required evidence.

#### Quality caveats

- Azure SQL presence as authoritative business state selects `active_standby`, even when Cosmos DB is also used.
- Cosmos DB alone selects active-active only when MongoDB API, RU throughput, and multi-region writes are evidence-backed.
- Two independent Kafka clusters do not provide global ordering or cross-cluster exactly-once behavior.
- A feature flag alone is not split-brain protection.
- Do not blindly retry ambiguous, non-idempotent business effects.
- Do not infer Cluster Linking, offset synchronization, mirror-topic promotion, or Cosmos multi-write deployment from repository absence.

---

### KAFKA-007: Critical client and processor state has scenario-aware readiness and telemetry behavior

**Severity:** High  
**Category:** health  
**Applies when:** confluent-kafka is used; apply under any resolved operating scenario

#### Requirement

The application code and repository-owned configuration must implement this behavior for the resolved Kafka operating scenario. Scenario-specific controls for the other scenario are `not_applicable`.

#### Repository evidence to inspect

- `KafkaHealthIndicator`
- `listener container state`
- `lag metric`

#### Finding condition

Emit a finding when evidence shows that critical processing failure is invisible, an intentionally inactive standby is treated as failed, or remote/shared cluster failure drains healthy regional capacity.

#### Evidence rule

Cite repository-relative path, symbol/property, original assessed lines, and exact excerpt when available. Evaluate effective behavior, not the presence of a dependency or property alone. If persistence role, Cosmos multi-write state, Kafka cluster model, or deployed replication state is unavailable, return `not_assessed` and identify the required evidence.

#### Quality caveats

- Azure SQL presence as authoritative business state selects `active_standby`, even when Cosmos DB is also used.
- Cosmos DB alone selects active-active only when MongoDB API, RU throughput, and multi-region writes are evidence-backed.
- Two independent Kafka clusters do not provide global ordering or cross-cluster exactly-once behavior.
- A feature flag alone is not split-brain protection.
- Do not blindly retry ambiguous, non-idempotent business effects.
- Do not infer Cluster Linking, offset synchronization, mirror-topic promotion, or Cosmos multi-write deployment from repository absence.

---

### KAFKA-008: Tests cover duplicate, replay, rebalance, broker loss, schema failure, recovery, and the selected operating scenario

**Severity:** Critical  
**Category:** testing  
**Applies when:** confluent-kafka is used; apply under any resolved operating scenario

#### Requirement

The application code and repository-owned configuration must implement this behavior for the resolved Kafka operating scenario. Scenario-specific controls for the other scenario are `not_applicable`.

#### Repository evidence to inspect

- `EmbeddedKafka`
- `Testcontainers Kafka`
- `fault injection`

#### Finding condition

Emit a finding when evidence shows that Kafka behavior for the selected operating scenario is untested.

#### Evidence rule

Cite repository-relative path, symbol/property, original assessed lines, and exact excerpt when available. Evaluate effective behavior, not the presence of a dependency or property alone. If persistence role, Cosmos multi-write state, Kafka cluster model, or deployed replication state is unavailable, return `not_assessed` and identify the required evidence.

#### Quality caveats

- Azure SQL presence as authoritative business state selects `active_standby`, even when Cosmos DB is also used.
- Cosmos DB alone selects active-active only when MongoDB API, RU throughput, and multi-region writes are evidence-backed.
- Two independent Kafka clusters do not provide global ordering or cross-cluster exactly-once behavior.
- A feature flag alone is not split-brain protection.
- Do not blindly retry ambiguous, non-idempotent business effects.
- Do not infer Cluster Linking, offset synchronization, mirror-topic promotion, or Cosmos multi-write deployment from repository absence.

---

### KAFKA-009: Selected Kafka operating scenario is explicit and evidence-backed

**Severity:** Critical  
**Category:** architecture  
**Applies when:** confluent-kafka is used

#### Requirement

The application code and repository-owned configuration must implement this behavior for the resolved Kafka operating scenario. Scenario-specific controls for the other scenario are `not_applicable`.

#### Repository evidence to inspect

- `kafka_operating_scenario`
- `azure_sql role`
- `cosmos_db api`
- `multi-region writes`
- `cluster model`

#### Finding condition

Emit a finding when evidence shows that the scenario is absent, unresolved without an evidence request, or conflicts with the authoritative persistence model.

#### Evidence rule

Cite repository-relative path, symbol/property, original assessed lines, and exact excerpt when available. Evaluate effective behavior, not the presence of a dependency or property alone. If persistence role, Cosmos multi-write state, Kafka cluster model, or deployed replication state is unavailable, return `not_assessed` and identify the required evidence.

#### Quality caveats

- Azure SQL presence as authoritative business state selects `active_standby`, even when Cosmos DB is also used.
- Cosmos DB alone selects active-active only when MongoDB API, RU throughput, and multi-region writes are evidence-backed.
- Two independent Kafka clusters do not provide global ordering or cross-cluster exactly-once behavior.
- A feature flag alone is not split-brain protection.
- Do not blindly retry ambiguous, non-idempotent business effects.
- Do not infer Cluster Linking, offset synchronization, mirror-topic promotion, or Cosmos multi-write deployment from repository absence.

---

### KAFKA-010: Kafka processing role aligns with authoritative state ownership

**Severity:** Critical  
**Category:** consistency  
**Applies when:** Kafka processing mutates authoritative business state

#### Requirement

The application code and repository-owned configuration must implement this behavior for the resolved Kafka operating scenario. Scenario-specific controls for the other scenario are `not_applicable`.

#### Repository evidence to inspect

- `authoritative_business_state`
- `consumer activation`
- `producer activation`
- `database role`

#### Finding condition

Emit a finding when evidence shows that Kafka processing can run in a region that does not own the authoritative active-standby state, or active-active processing lacks multi-write-safe state behavior.

#### Evidence rule

Cite repository-relative path, symbol/property, original assessed lines, and exact excerpt when available. Evaluate effective behavior, not the presence of a dependency or property alone. If persistence role, Cosmos multi-write state, Kafka cluster model, or deployed replication state is unavailable, return `not_assessed` and identify the required evidence.

#### Quality caveats

- Azure SQL presence as authoritative business state selects `active_standby`, even when Cosmos DB is also used.
- Cosmos DB alone selects active-active only when MongoDB API, RU throughput, and multi-region writes are evidence-backed.
- Two independent Kafka clusters do not provide global ordering or cross-cluster exactly-once behavior.
- A feature flag alone is not split-brain protection.
- Do not blindly retry ambiguous, non-idempotent business effects.
- Do not infer Cluster Linking, offset synchronization, mirror-topic promotion, or Cosmos multi-write deployment from repository absence.

---

### KAFKA-011: Topic, key, schema, group, and event identity are portable across regions

**Severity:** Critical  
**Category:** messaging  
**Applies when:** any Kafka scenario applies

#### Requirement

The application code and repository-owned configuration must implement this behavior for the resolved Kafka operating scenario. Scenario-specific controls for the other scenario are `not_applicable`.

#### Repository evidence to inspect

- `topic name`
- `message key`
- `event id`
- `schema subject`
- `group.id`
- `cluster name`

#### Finding condition

Emit a finding when evidence shows that physical cluster or region identity is embedded in durable event contracts, consumer identity is unstable, or event identity changes across retry or failover.

#### Evidence rule

Cite repository-relative path, symbol/property, original assessed lines, and exact excerpt when available. Evaluate effective behavior, not the presence of a dependency or property alone. If persistence role, Cosmos multi-write state, Kafka cluster model, or deployed replication state is unavailable, return `not_assessed` and identify the required evidence.

#### Quality caveats

- Azure SQL presence as authoritative business state selects `active_standby`, even when Cosmos DB is also used.
- Cosmos DB alone selects active-active only when MongoDB API, RU throughput, and multi-region writes are evidence-backed.
- Two independent Kafka clusters do not provide global ordering or cross-cluster exactly-once behavior.
- A feature flag alone is not split-brain protection.
- Do not blindly retry ambiguous, non-idempotent business effects.
- Do not infer Cluster Linking, offset synchronization, mirror-topic promotion, or Cosmos multi-write deployment from repository absence.

---

### KAFKA-012: Scenario and regional role changes do not require rebuilding the application

**Severity:** High  
**Category:** configuration  
**Applies when:** any Kafka scenario applies

#### Requirement

The application code and repository-owned configuration must implement this behavior for the resolved Kafka operating scenario. Scenario-specific controls for the other scenario are `not_applicable`.

#### Repository evidence to inspect

- `bootstrap servers`
- `schema registry`
- `consumer enabled`
- `producer enabled`
- `region`
- `cluster role`

#### Finding condition

Emit a finding when evidence shows that switching region, cluster role, or scenario requires a different code build or hardcoded source change.

#### Evidence rule

Cite repository-relative path, symbol/property, original assessed lines, and exact excerpt when available. Evaluate effective behavior, not the presence of a dependency or property alone. If persistence role, Cosmos multi-write state, Kafka cluster model, or deployed replication state is unavailable, return `not_assessed` and identify the required evidence.

#### Quality caveats

- Azure SQL presence as authoritative business state selects `active_standby`, even when Cosmos DB is also used.
- Cosmos DB alone selects active-active only when MongoDB API, RU throughput, and multi-region writes are evidence-backed.
- Two independent Kafka clusters do not provide global ordering or cross-cluster exactly-once behavior.
- A feature flag alone is not split-brain protection.
- Do not blindly retry ambiguous, non-idempotent business effects.
- Do not infer Cluster Linking, offset synchronization, mirror-topic promotion, or Cosmos multi-write deployment from repository absence.

---

### KAFKA-AA-001: Regional clients use their local independent Kafka cluster

**Severity:** Critical  
**Category:** regional-affinity  
**Applies when:** operating scenario is independent_regional_active_active

#### Requirement

The application code and repository-owned configuration must implement this behavior for the resolved Kafka operating scenario. Scenario-specific controls for the other scenario are `not_applicable`.

#### Repository evidence to inspect

- `regional bootstrap servers`
- `local cluster alias`
- `deployment-injected region`

#### Finding condition

Emit a finding when evidence shows that a region normally connects to the remote cluster, combines independent clusters in one bootstrap list, or silently falls back cross-region.

#### Evidence rule

Cite repository-relative path, symbol/property, original assessed lines, and exact excerpt when available. Evaluate effective behavior, not the presence of a dependency or property alone. If persistence role, Cosmos multi-write state, Kafka cluster model, or deployed replication state is unavailable, return `not_assessed` and identify the required evidence.

#### Quality caveats

- Azure SQL presence as authoritative business state selects `active_standby`, even when Cosmos DB is also used.
- Cosmos DB alone selects active-active only when MongoDB API, RU throughput, and multi-region writes are evidence-backed.
- Two independent Kafka clusters do not provide global ordering or cross-cluster exactly-once behavior.
- A feature flag alone is not split-brain protection.
- Do not blindly retry ambiguous, non-idempotent business effects.
- Do not infer Cluster Linking, offset synchronization, mirror-topic promotion, or Cosmos multi-write deployment from repository absence.

---

### KAFKA-AA-002: Cross-cluster duplicate processing is safe

**Severity:** Critical  
**Category:** consistency  
**Applies when:** operating scenario is independent_regional_active_active

#### Requirement

The application code and repository-owned configuration must implement this behavior for the resolved Kafka operating scenario. Scenario-specific controls for the other scenario are `not_applicable`.

#### Repository evidence to inspect

- `stable event id`
- `dedupe store`
- `unique constraint`
- `idempotent consumer`

#### Finding condition

Emit a finding when evidence shows that the same business event can arrive through both independent clusters and duplicate a business effect.

#### Evidence rule

Cite repository-relative path, symbol/property, original assessed lines, and exact excerpt when available. Evaluate effective behavior, not the presence of a dependency or property alone. If persistence role, Cosmos multi-write state, Kafka cluster model, or deployed replication state is unavailable, return `not_assessed` and identify the required evidence.

#### Quality caveats

- Azure SQL presence as authoritative business state selects `active_standby`, even when Cosmos DB is also used.
- Cosmos DB alone selects active-active only when MongoDB API, RU throughput, and multi-region writes are evidence-backed.
- Two independent Kafka clusters do not provide global ordering or cross-cluster exactly-once behavior.
- A feature flag alone is not split-brain protection.
- Do not blindly retry ambiguous, non-idempotent business effects.
- Do not infer Cluster Linking, offset synchronization, mirror-topic promotion, or Cosmos multi-write deployment from repository absence.

---

### KAFKA-AA-003: Ordering assumptions are scoped explicitly

**Severity:** High  
**Category:** ordering  
**Applies when:** operating scenario is independent_regional_active_active

#### Requirement

The application code and repository-owned configuration must implement this behavior for the resolved Kafka operating scenario. Scenario-specific controls for the other scenario are `not_applicable`.

#### Repository evidence to inspect

- `partition key`
- `business sequence`
- `version`
- `region`
- `cluster`

#### Finding condition

Emit a finding when evidence shows that the application assumes global ordering across independent regional clusters without an external sequence or conflict rule.

#### Evidence rule

Cite repository-relative path, symbol/property, original assessed lines, and exact excerpt when available. Evaluate effective behavior, not the presence of a dependency or property alone. If persistence role, Cosmos multi-write state, Kafka cluster model, or deployed replication state is unavailable, return `not_assessed` and identify the required evidence.

#### Quality caveats

- Azure SQL presence as authoritative business state selects `active_standby`, even when Cosmos DB is also used.
- Cosmos DB alone selects active-active only when MongoDB API, RU throughput, and multi-region writes are evidence-backed.
- Two independent Kafka clusters do not provide global ordering or cross-cluster exactly-once behavior.
- A feature flag alone is not split-brain protection.
- Do not blindly retry ambiguous, non-idempotent business effects.
- Do not infer Cluster Linking, offset synchronization, mirror-topic promotion, or Cosmos multi-write deployment from repository absence.

---

### KAFKA-AA-004: Regional production and consumption remain locally autonomous

**Severity:** Critical  
**Category:** availability  
**Applies when:** operating scenario is independent_regional_active_active

#### Requirement

The application code and repository-owned configuration must implement this behavior for the resolved Kafka operating scenario. Scenario-specific controls for the other scenario are `not_applicable`.

#### Repository evidence to inspect

- `local readiness`
- `remote cluster health`
- `dual publish`
- `synchronous confirmation`

#### Finding condition

Emit a finding when evidence shows that remote cluster failure stops local processing, participates in local readiness, or synchronous dual-cluster publishing is required.

#### Evidence rule

Cite repository-relative path, symbol/property, original assessed lines, and exact excerpt when available. Evaluate effective behavior, not the presence of a dependency or property alone. If persistence role, Cosmos multi-write state, Kafka cluster model, or deployed replication state is unavailable, return `not_assessed` and identify the required evidence.

#### Quality caveats

- Azure SQL presence as authoritative business state selects `active_standby`, even when Cosmos DB is also used.
- Cosmos DB alone selects active-active only when MongoDB API, RU throughput, and multi-region writes are evidence-backed.
- Two independent Kafka clusters do not provide global ordering or cross-cluster exactly-once behavior.
- A feature flag alone is not split-brain protection.
- Do not blindly retry ambiguous, non-idempotent business effects.
- Do not infer Cluster Linking, offset synchronization, mirror-topic promotion, or Cosmos multi-write deployment from repository absence.

---

### KAFKA-AA-005: Kafka replay and Cosmos multi-write behavior are jointly safe

**Severity:** Critical  
**Category:** consistency  
**Applies when:** active-active Kafka is aligned with Cosmos DB MongoDB API RU multi-region writes

#### Requirement

The application code and repository-owned configuration must implement this behavior for the resolved Kafka operating scenario. Scenario-specific controls for the other scenario are `not_applicable`.

#### Repository evidence to inspect

- `document id`
- `optimistic version`
- `conflict policy`
- `tentative write`
- `reconciliation`

#### Finding condition

Emit a finding when evidence shows that Kafka replay or cross-cluster reordering can produce conflicting Cosmos writes without stable identity, versioning, conflict handling, or reconciliation.

#### Evidence rule

Cite repository-relative path, symbol/property, original assessed lines, and exact excerpt when available. Evaluate effective behavior, not the presence of a dependency or property alone. If persistence role, Cosmos multi-write state, Kafka cluster model, or deployed replication state is unavailable, return `not_assessed` and identify the required evidence.

#### Quality caveats

- Azure SQL presence as authoritative business state selects `active_standby`, even when Cosmos DB is also used.
- Cosmos DB alone selects active-active only when MongoDB API, RU throughput, and multi-region writes are evidence-backed.
- Two independent Kafka clusters do not provide global ordering or cross-cluster exactly-once behavior.
- A feature flag alone is not split-brain protection.
- Do not blindly retry ambiguous, non-idempotent business effects.
- Do not infer Cluster Linking, offset synchronization, mirror-topic promotion, or Cosmos multi-write deployment from repository absence.

---

### KAFKA-AA-006: Active-active tests exercise both independent clusters

**Severity:** Critical  
**Category:** testing  
**Applies when:** operating scenario is independent_regional_active_active

#### Requirement

The application code and repository-owned configuration must implement this behavior for the resolved Kafka operating scenario. Scenario-specific controls for the other scenario are `not_applicable`.

#### Repository evidence to inspect

- `two Kafka clusters`
- `duplicate event`
- `different order`
- `regional outage`
- `Cosmos conflict`

#### Finding condition

Emit a finding when evidence shows that tests do not prove local autonomy, duplicate tolerance, ordering behavior, Cosmos conflict safety, and recovery for independent clusters.

#### Evidence rule

Cite repository-relative path, symbol/property, original assessed lines, and exact excerpt when available. Evaluate effective behavior, not the presence of a dependency or property alone. If persistence role, Cosmos multi-write state, Kafka cluster model, or deployed replication state is unavailable, return `not_assessed` and identify the required evidence.

#### Quality caveats

- Azure SQL presence as authoritative business state selects `active_standby`, even when Cosmos DB is also used.
- Cosmos DB alone selects active-active only when MongoDB API, RU throughput, and multi-region writes are evidence-backed.
- Two independent Kafka clusters do not provide global ordering or cross-cluster exactly-once behavior.
- A feature flag alone is not split-brain protection.
- Do not blindly retry ambiguous, non-idempotent business effects.
- Do not infer Cluster Linking, offset synchronization, mirror-topic promotion, or Cosmos multi-write deployment from repository absence.

---

### KAFKA-AS-001: Only the active regional role produces and consumes authoritative workloads

**Severity:** Critical  
**Category:** workload-ownership  
**Applies when:** operating scenario is active_standby

#### Requirement

The application code and repository-owned configuration must implement this behavior for the resolved Kafka operating scenario. Scenario-specific controls for the other scenario are `not_applicable`.

#### Repository evidence to inspect

- `consumer auto-startup`
- `producer enabled`
- `scheduler enabled`
- `active role`

#### Finding condition

Emit a finding when evidence shows that standby instances ordinarily produce, consume, schedule, or reprocess authoritative work.

#### Evidence rule

Cite repository-relative path, symbol/property, original assessed lines, and exact excerpt when available. Evaluate effective behavior, not the presence of a dependency or property alone. If persistence role, Cosmos multi-write state, Kafka cluster model, or deployed replication state is unavailable, return `not_assessed` and identify the required evidence.

#### Quality caveats

- Azure SQL presence as authoritative business state selects `active_standby`, even when Cosmos DB is also used.
- Cosmos DB alone selects active-active only when MongoDB API, RU throughput, and multi-region writes are evidence-backed.
- Two independent Kafka clusters do not provide global ordering or cross-cluster exactly-once behavior.
- A feature flag alone is not split-brain protection.
- Do not blindly retry ambiguous, non-idempotent business effects.
- Do not infer Cluster Linking, offset synchronization, mirror-topic promotion, or Cosmos multi-write deployment from repository absence.

---

### KAFKA-AS-002: Kafka activation aligns with Azure SQL primary ownership

**Severity:** Critical  
**Category:** consistency  
**Applies when:** operating scenario is active_standby

#### Requirement

The application code and repository-owned configuration must implement this behavior for the resolved Kafka operating scenario. Scenario-specific controls for the other scenario are `not_applicable`.

#### Repository evidence to inspect

- `SQL read-write listener`
- `Kafka role`
- `activation gate`
- `ownership epoch`

#### Finding condition

Emit a finding when evidence shows that Kafka processing can activate before SQL primary ownership is verified or can remain active after losing authoritative database ownership.

#### Evidence rule

Cite repository-relative path, symbol/property, original assessed lines, and exact excerpt when available. Evaluate effective behavior, not the presence of a dependency or property alone. If persistence role, Cosmos multi-write state, Kafka cluster model, or deployed replication state is unavailable, return `not_assessed` and identify the required evidence.

#### Quality caveats

- Azure SQL presence as authoritative business state selects `active_standby`, even when Cosmos DB is also used.
- Cosmos DB alone selects active-active only when MongoDB API, RU throughput, and multi-region writes are evidence-backed.
- Two independent Kafka clusters do not provide global ordering or cross-cluster exactly-once behavior.
- A feature flag alone is not split-brain protection.
- Do not blindly retry ambiguous, non-idempotent business effects.
- Do not infer Cluster Linking, offset synchronization, mirror-topic promotion, or Cosmos multi-write deployment from repository absence.

---

### KAFKA-AS-003: Standby activation is fail-safe and split-brain protected

**Severity:** Critical  
**Category:** workload-ownership  
**Applies when:** operating scenario is active_standby

#### Requirement

The application code and repository-owned configuration must implement this behavior for the resolved Kafka operating scenario. Scenario-specific controls for the other scenario are `not_applicable`.

#### Repository evidence to inspect

- `lease`
- `epoch`
- `fencing token`
- `feature flag`
- `both-active alert`

#### Finding condition

Emit a finding when evidence shows that activation defaults enabled, relies only on a property flag where concurrency is possible, or stale-active processing is not fenced.

#### Evidence rule

Cite repository-relative path, symbol/property, original assessed lines, and exact excerpt when available. Evaluate effective behavior, not the presence of a dependency or property alone. If persistence role, Cosmos multi-write state, Kafka cluster model, or deployed replication state is unavailable, return `not_assessed` and identify the required evidence.

#### Quality caveats

- Azure SQL presence as authoritative business state selects `active_standby`, even when Cosmos DB is also used.
- Cosmos DB alone selects active-active only when MongoDB API, RU throughput, and multi-region writes are evidence-backed.
- Two independent Kafka clusters do not provide global ordering or cross-cluster exactly-once behavior.
- A feature flag alone is not split-brain protection.
- Do not blindly retry ambiguous, non-idempotent business effects.
- Do not infer Cluster Linking, offset synchronization, mirror-topic promotion, or Cosmos multi-write deployment from repository absence.

---

### KAFKA-AS-004: Offsets and replicated topic state support controlled promotion

**Severity:** Critical  
**Category:** recovery  
**Applies when:** operating scenario is active_standby

#### Requirement

The application code and repository-owned configuration must implement this behavior for the resolved Kafka operating scenario. Scenario-specific controls for the other scenario are `not_applicable`.

#### Repository evidence to inspect

- `consumer offset`
- `cluster linking`
- `mirror topic`
- `offset sync`
- `group id`

#### Finding condition

Emit a finding when evidence shows that promotion can start from an unknown or unsafe offset, lose data, or repeat effects without idempotency and reconciliation.

#### Evidence rule

Cite repository-relative path, symbol/property, original assessed lines, and exact excerpt when available. Evaluate effective behavior, not the presence of a dependency or property alone. If persistence role, Cosmos multi-write state, Kafka cluster model, or deployed replication state is unavailable, return `not_assessed` and identify the required evidence.

#### Quality caveats

- Azure SQL presence as authoritative business state selects `active_standby`, even when Cosmos DB is also used.
- Cosmos DB alone selects active-active only when MongoDB API, RU throughput, and multi-region writes are evidence-backed.
- Two independent Kafka clusters do not provide global ordering or cross-cluster exactly-once behavior.
- A feature flag alone is not split-brain protection.
- Do not blindly retry ambiguous, non-idempotent business effects.
- Do not infer Cluster Linking, offset synchronization, mirror-topic promotion, or Cosmos multi-write deployment from repository absence.

---

### KAFKA-AS-005: Standby or mirror topics are not treated as writable before promotion

**Severity:** Critical  
**Category:** messaging  
**Applies when:** operating scenario is active_standby

#### Requirement

The application code and repository-owned configuration must implement this behavior for the resolved Kafka operating scenario. Scenario-specific controls for the other scenario are `not_applicable`.

#### Repository evidence to inspect

- `mirror topic`
- `read-only`
- `producer bootstrap`
- `promotion state`

#### Finding condition

Emit a finding when evidence shows that the application produces to passive mirror topics, interprets connectivity as writability, or consumes standby state before controlled activation.

#### Evidence rule

Cite repository-relative path, symbol/property, original assessed lines, and exact excerpt when available. Evaluate effective behavior, not the presence of a dependency or property alone. If persistence role, Cosmos multi-write state, Kafka cluster model, or deployed replication state is unavailable, return `not_assessed` and identify the required evidence.

#### Quality caveats

- Azure SQL presence as authoritative business state selects `active_standby`, even when Cosmos DB is also used.
- Cosmos DB alone selects active-active only when MongoDB API, RU throughput, and multi-region writes are evidence-backed.
- Two independent Kafka clusters do not provide global ordering or cross-cluster exactly-once behavior.
- A feature flag alone is not split-brain protection.
- Do not blindly retry ambiguous, non-idempotent business effects.
- Do not infer Cluster Linking, offset synchronization, mirror-topic promotion, or Cosmos multi-write deployment from repository absence.

---

### KAFKA-AS-006: Failover preserves stable business and event identity

**Severity:** Critical  
**Category:** consistency  
**Applies when:** operating scenario is active_standby

#### Requirement

The application code and repository-owned configuration must implement this behavior for the resolved Kafka operating scenario. Scenario-specific controls for the other scenario are `not_applicable`.

#### Repository evidence to inspect

- `event id`
- `business operation id`
- `database unique key`
- `provider transaction id`

#### Finding condition

Emit a finding when evidence shows that failover regenerates identity or offset restoration can duplicate SQL-backed or external business effects.

#### Evidence rule

Cite repository-relative path, symbol/property, original assessed lines, and exact excerpt when available. Evaluate effective behavior, not the presence of a dependency or property alone. If persistence role, Cosmos multi-write state, Kafka cluster model, or deployed replication state is unavailable, return `not_assessed` and identify the required evidence.

#### Quality caveats

- Azure SQL presence as authoritative business state selects `active_standby`, even when Cosmos DB is also used.
- Cosmos DB alone selects active-active only when MongoDB API, RU throughput, and multi-region writes are evidence-backed.
- Two independent Kafka clusters do not provide global ordering or cross-cluster exactly-once behavior.
- A feature flag alone is not split-brain protection.
- Do not blindly retry ambiguous, non-idempotent business effects.
- Do not infer Cluster Linking, offset synchronization, mirror-topic promotion, or Cosmos multi-write deployment from repository absence.

---

### KAFKA-AS-007: Application behavior supports ordered SQL and Kafka failover

**Severity:** Critical  
**Category:** recovery  
**Applies when:** operating scenario is active_standby

#### Requirement

The application code and repository-owned configuration must implement this behavior for the resolved Kafka operating scenario. Scenario-specific controls for the other scenario are `not_applicable`.

#### Repository evidence to inspect

- `old-active fencing`
- `SQL role verification`
- `Kafka promotion`
- `consumer activation`
- `traffic enablement`

#### Finding condition

Emit a finding when evidence shows that the application can process while SQL and Kafka roles are misaligned or cannot stop acquisition before ownership transfer.

#### Evidence rule

Cite repository-relative path, symbol/property, original assessed lines, and exact excerpt when available. Evaluate effective behavior, not the presence of a dependency or property alone. If persistence role, Cosmos multi-write state, Kafka cluster model, or deployed replication state is unavailable, return `not_assessed` and identify the required evidence.

#### Quality caveats

- Azure SQL presence as authoritative business state selects `active_standby`, even when Cosmos DB is also used.
- Cosmos DB alone selects active-active only when MongoDB API, RU throughput, and multi-region writes are evidence-backed.
- Two independent Kafka clusters do not provide global ordering or cross-cluster exactly-once behavior.
- A feature flag alone is not split-brain protection.
- Do not blindly retry ambiguous, non-idempotent business effects.
- Do not infer Cluster Linking, offset synchronization, mirror-topic promotion, or Cosmos multi-write deployment from repository absence.

---

### KAFKA-AS-008: Failback prevents reverse duplication and stale ownership

**Severity:** High  
**Category:** recovery  
**Applies when:** operating scenario is active_standby

#### Requirement

The application code and repository-owned configuration must implement this behavior for the resolved Kafka operating scenario. Scenario-specific controls for the other scenario are `not_applicable`.

#### Repository evidence to inspect

- `failback`
- `reverse link`
- `ownership epoch`
- `offset readiness`
- `fencing`

#### Finding condition

Emit a finding when evidence shows that role reversal can reactivate stale consumers/producers, replay without dedupe, or misalign SQL and Kafka roles.

#### Evidence rule

Cite repository-relative path, symbol/property, original assessed lines, and exact excerpt when available. Evaluate effective behavior, not the presence of a dependency or property alone. If persistence role, Cosmos multi-write state, Kafka cluster model, or deployed replication state is unavailable, return `not_assessed` and identify the required evidence.

#### Quality caveats

- Azure SQL presence as authoritative business state selects `active_standby`, even when Cosmos DB is also used.
- Cosmos DB alone selects active-active only when MongoDB API, RU throughput, and multi-region writes are evidence-backed.
- Two independent Kafka clusters do not provide global ordering or cross-cluster exactly-once behavior.
- A feature flag alone is not split-brain protection.
- Do not blindly retry ambiguous, non-idempotent business effects.
- Do not infer Cluster Linking, offset synchronization, mirror-topic promotion, or Cosmos multi-write deployment from repository absence.

---

### KAFKA-AS-009: Active-standby tests cover promotion, fencing, offsets, and failback

**Severity:** Critical  
**Category:** testing  
**Applies when:** operating scenario is active_standby

#### Requirement

The application code and repository-owned configuration must implement this behavior for the resolved Kafka operating scenario. Scenario-specific controls for the other scenario are `not_applicable`.

#### Repository evidence to inspect

- `SQL failover`
- `Kafka promotion`
- `stale active`
- `both active`
- `both inactive`
- `failback`

#### Finding condition

Emit a finding when evidence shows that tests do not cover partial ordering, stale-active fencing, offset restoration, duplicate replay, both-active/both-inactive, and reverse failback.

#### Evidence rule

Cite repository-relative path, symbol/property, original assessed lines, and exact excerpt when available. Evaluate effective behavior, not the presence of a dependency or property alone. If persistence role, Cosmos multi-write state, Kafka cluster model, or deployed replication state is unavailable, return `not_assessed` and identify the required evidence.

#### Quality caveats

- Azure SQL presence as authoritative business state selects `active_standby`, even when Cosmos DB is also used.
- Cosmos DB alone selects active-active only when MongoDB API, RU throughput, and multi-region writes are evidence-backed.
- Two independent Kafka clusters do not provide global ordering or cross-cluster exactly-once behavior.
- A feature flag alone is not split-brain protection.
- Do not blindly retry ambiguous, non-idempotent business effects.
- Do not infer Cluster Linking, offset synchronization, mirror-topic promotion, or Cosmos multi-write deployment from repository absence.


## Database-Independent Kafka Scenario Controls

---

### KAFKA-DI-001: Database-independent Kafka processing model is explicit

**Severity:** Critical  
**Category:** architecture  
**Applies when:** operating scenario is `database_independent_kafka`

#### Requirement

The application must implement this behavior for Kafka processing with no application database. Applicability depends on the processing model, regional ownership, external side effects, and Kafka-backed or local state.

#### Repository evidence to inspect

- Kafka producer, consumer, or Streams topology
- Event and business-operation identity
- Consumer completion and offset handling
- Regional activation and ownership configuration
- External client side effects
- Kafka Streams, compacted-topic, or local state-store configuration
- Failure and recovery tests

#### Finding condition

Emit a finding when repository evidence demonstrates that the required database-independent Kafka behavior is absent, unsafe, or incompatible with the declared processing and ownership model.

#### Evidence rule

Cite repository-relative path, symbol/property, original assessed lines, and exact excerpt. Do not infer no-database architecture from an absent driver alone. Use Step 1 production-use evidence and approved context.

#### Quality caveats

- Database-independent does not automatically mean stateless or multi-active.
- Kafka Streams state stores, compacted topics, local RocksDB, and external side effects create recovery and ownership requirements.
- Do not require a database solely to implement idempotency; use the approved durable mechanism for the workload.
- Scenario topology remains external evidence unless supplied through approved context.

---

### KAFKA-DI-002: Regional processing ownership is explicit and safe

**Severity:** Critical  
**Category:** workload-ownership  
**Applies when:** operating scenario is `database_independent_kafka`

#### Requirement

The application must implement this behavior for Kafka processing with no application database. Applicability depends on the processing model, regional ownership, external side effects, and Kafka-backed or local state.

#### Repository evidence to inspect

- Kafka producer, consumer, or Streams topology
- Event and business-operation identity
- Consumer completion and offset handling
- Regional activation and ownership configuration
- External client side effects
- Kafka Streams, compacted-topic, or local state-store configuration
- Failure and recovery tests

#### Finding condition

Emit a finding when repository evidence demonstrates that the required database-independent Kafka behavior is absent, unsafe, or incompatible with the declared processing and ownership model.

#### Evidence rule

Cite repository-relative path, symbol/property, original assessed lines, and exact excerpt. Do not infer no-database architecture from an absent driver alone. Use Step 1 production-use evidence and approved context.

#### Quality caveats

- Database-independent does not automatically mean stateless or multi-active.
- Kafka Streams state stores, compacted topics, local RocksDB, and external side effects create recovery and ownership requirements.
- Do not require a database solely to implement idempotency; use the approved durable mechanism for the workload.
- Scenario topology remains external evidence unless supplied through approved context.

---

### KAFKA-DI-003: Topic-to-topic processing preserves stable identity and lineage

**Severity:** Critical  
**Category:** messaging  
**Applies when:** operating scenario is `database_independent_kafka`

#### Requirement

The application must implement this behavior for Kafka processing with no application database. Applicability depends on the processing model, regional ownership, external side effects, and Kafka-backed or local state.

#### Repository evidence to inspect

- Kafka producer, consumer, or Streams topology
- Event and business-operation identity
- Consumer completion and offset handling
- Regional activation and ownership configuration
- External client side effects
- Kafka Streams, compacted-topic, or local state-store configuration
- Failure and recovery tests

#### Finding condition

Emit a finding when repository evidence demonstrates that the required database-independent Kafka behavior is absent, unsafe, or incompatible with the declared processing and ownership model.

#### Evidence rule

Cite repository-relative path, symbol/property, original assessed lines, and exact excerpt. Do not infer no-database architecture from an absent driver alone. Use Step 1 production-use evidence and approved context.

#### Quality caveats

- Database-independent does not automatically mean stateless or multi-active.
- Kafka Streams state stores, compacted topics, local RocksDB, and external side effects create recovery and ownership requirements.
- Do not require a database solely to implement idempotency; use the approved durable mechanism for the workload.
- Scenario topology remains external evidence unless supplied through approved context.

---

### KAFKA-DI-004: Producer-only workloads observe delivery and ambiguous outcomes

**Severity:** Critical  
**Category:** messaging  
**Applies when:** operating scenario is `database_independent_kafka`

#### Requirement

The application must implement this behavior for Kafka processing with no application database. Applicability depends on the processing model, regional ownership, external side effects, and Kafka-backed or local state.

#### Repository evidence to inspect

- Kafka producer, consumer, or Streams topology
- Event and business-operation identity
- Consumer completion and offset handling
- Regional activation and ownership configuration
- External client side effects
- Kafka Streams, compacted-topic, or local state-store configuration
- Failure and recovery tests

#### Finding condition

Emit a finding when repository evidence demonstrates that the required database-independent Kafka behavior is absent, unsafe, or incompatible with the declared processing and ownership model.

#### Evidence rule

Cite repository-relative path, symbol/property, original assessed lines, and exact excerpt. Do not infer no-database architecture from an absent driver alone. Use Step 1 production-use evidence and approved context.

#### Quality caveats

- Database-independent does not automatically mean stateless or multi-active.
- Kafka Streams state stores, compacted topics, local RocksDB, and external side effects create recovery and ownership requirements.
- Do not require a database solely to implement idempotency; use the approved durable mechanism for the workload.
- Scenario topology remains external evidence unless supplied through approved context.

---

### KAFKA-DI-005: Consumer completion and offset semantics match processing outcome

**Severity:** Critical  
**Category:** consistency  
**Applies when:** operating scenario is `database_independent_kafka`

#### Requirement

The application must implement this behavior for Kafka processing with no application database. Applicability depends on the processing model, regional ownership, external side effects, and Kafka-backed or local state.

#### Repository evidence to inspect

- Kafka producer, consumer, or Streams topology
- Event and business-operation identity
- Consumer completion and offset handling
- Regional activation and ownership configuration
- External client side effects
- Kafka Streams, compacted-topic, or local state-store configuration
- Failure and recovery tests

#### Finding condition

Emit a finding when repository evidence demonstrates that the required database-independent Kafka behavior is absent, unsafe, or incompatible with the declared processing and ownership model.

#### Evidence rule

Cite repository-relative path, symbol/property, original assessed lines, and exact excerpt. Do not infer no-database architecture from an absent driver alone. Use Step 1 production-use evidence and approved context.

#### Quality caveats

- Database-independent does not automatically mean stateless or multi-active.
- Kafka Streams state stores, compacted topics, local RocksDB, and external side effects create recovery and ownership requirements.
- Do not require a database solely to implement idempotency; use the approved durable mechanism for the workload.
- Scenario topology remains external evidence unless supplied through approved context.

---

### KAFKA-DI-006: External side effects are idempotent or reconciled

**Severity:** Critical  
**Category:** consistency  
**Applies when:** operating scenario is `database_independent_kafka`

#### Requirement

The application must implement this behavior for Kafka processing with no application database. Applicability depends on the processing model, regional ownership, external side effects, and Kafka-backed or local state.

#### Repository evidence to inspect

- Kafka producer, consumer, or Streams topology
- Event and business-operation identity
- Consumer completion and offset handling
- Regional activation and ownership configuration
- External client side effects
- Kafka Streams, compacted-topic, or local state-store configuration
- Failure and recovery tests

#### Finding condition

Emit a finding when repository evidence demonstrates that the required database-independent Kafka behavior is absent, unsafe, or incompatible with the declared processing and ownership model.

#### Evidence rule

Cite repository-relative path, symbol/property, original assessed lines, and exact excerpt. Do not infer no-database architecture from an absent driver alone. Use Step 1 production-use evidence and approved context.

#### Quality caveats

- Database-independent does not automatically mean stateless or multi-active.
- Kafka Streams state stores, compacted topics, local RocksDB, and external side effects create recovery and ownership requirements.
- Do not require a database solely to implement idempotency; use the approved durable mechanism for the workload.
- Scenario topology remains external evidence unless supplied through approved context.

---

### KAFKA-DI-007: Stateless processing does not rely on pod-local correctness state

**Severity:** Critical  
**Category:** state  
**Applies when:** operating scenario is `database_independent_kafka`

#### Requirement

The application must implement this behavior for Kafka processing with no application database. Applicability depends on the processing model, regional ownership, external side effects, and Kafka-backed or local state.

#### Repository evidence to inspect

- Kafka producer, consumer, or Streams topology
- Event and business-operation identity
- Consumer completion and offset handling
- Regional activation and ownership configuration
- External client side effects
- Kafka Streams, compacted-topic, or local state-store configuration
- Failure and recovery tests

#### Finding condition

Emit a finding when repository evidence demonstrates that the required database-independent Kafka behavior is absent, unsafe, or incompatible with the declared processing and ownership model.

#### Evidence rule

Cite repository-relative path, symbol/property, original assessed lines, and exact excerpt. Do not infer no-database architecture from an absent driver alone. Use Step 1 production-use evidence and approved context.

#### Quality caveats

- Database-independent does not automatically mean stateless or multi-active.
- Kafka Streams state stores, compacted topics, local RocksDB, and external side effects create recovery and ownership requirements.
- Do not require a database solely to implement idempotency; use the approved durable mechanism for the workload.
- Scenario topology remains external evidence unless supplied through approved context.

---

### KAFKA-DI-008: Kafka Streams and local state stores have an explicit restore contract

**Severity:** Critical  
**Category:** stream-state  
**Applies when:** operating scenario is `database_independent_kafka`

#### Requirement

The application must implement this behavior for Kafka processing with no application database. Applicability depends on the processing model, regional ownership, external side effects, and Kafka-backed or local state.

#### Repository evidence to inspect

- Kafka producer, consumer, or Streams topology
- Event and business-operation identity
- Consumer completion and offset handling
- Regional activation and ownership configuration
- External client side effects
- Kafka Streams, compacted-topic, or local state-store configuration
- Failure and recovery tests

#### Finding condition

Emit a finding when repository evidence demonstrates that the required database-independent Kafka behavior is absent, unsafe, or incompatible with the declared processing and ownership model.

#### Evidence rule

Cite repository-relative path, symbol/property, original assessed lines, and exact excerpt. Do not infer no-database architecture from an absent driver alone. Use Step 1 production-use evidence and approved context.

#### Quality caveats

- Database-independent does not automatically mean stateless or multi-active.
- Kafka Streams state stores, compacted topics, local RocksDB, and external side effects create recovery and ownership requirements.
- Do not require a database solely to implement idempotency; use the approved durable mechanism for the workload.
- Scenario topology remains external evidence unless supplied through approved context.

---

### KAFKA-DI-009: Compacted topics used as state have key, tombstone, and rebuild semantics

**Severity:** Critical  
**Category:** stream-state  
**Applies when:** operating scenario is `database_independent_kafka`

#### Requirement

The application must implement this behavior for Kafka processing with no application database. Applicability depends on the processing model, regional ownership, external side effects, and Kafka-backed or local state.

#### Repository evidence to inspect

- Kafka producer, consumer, or Streams topology
- Event and business-operation identity
- Consumer completion and offset handling
- Regional activation and ownership configuration
- External client side effects
- Kafka Streams, compacted-topic, or local state-store configuration
- Failure and recovery tests

#### Finding condition

Emit a finding when repository evidence demonstrates that the required database-independent Kafka behavior is absent, unsafe, or incompatible with the declared processing and ownership model.

#### Evidence rule

Cite repository-relative path, symbol/property, original assessed lines, and exact excerpt. Do not infer no-database architecture from an absent driver alone. Use Step 1 production-use evidence and approved context.

#### Quality caveats

- Database-independent does not automatically mean stateless or multi-active.
- Kafka Streams state stores, compacted topics, local RocksDB, and external side effects create recovery and ownership requirements.
- Do not require a database solely to implement idempotency; use the approved durable mechanism for the workload.
- Scenario topology remains external evidence unless supplied through approved context.

---

### KAFKA-DI-010: Cross-region duplicates and ordering are defined for the selected ownership model

**Severity:** Critical  
**Category:** ordering  
**Applies when:** operating scenario is `database_independent_kafka`

#### Requirement

The application must implement this behavior for Kafka processing with no application database. Applicability depends on the processing model, regional ownership, external side effects, and Kafka-backed or local state.

#### Repository evidence to inspect

- Kafka producer, consumer, or Streams topology
- Event and business-operation identity
- Consumer completion and offset handling
- Regional activation and ownership configuration
- External client side effects
- Kafka Streams, compacted-topic, or local state-store configuration
- Failure and recovery tests

#### Finding condition

Emit a finding when repository evidence demonstrates that the required database-independent Kafka behavior is absent, unsafe, or incompatible with the declared processing and ownership model.

#### Evidence rule

Cite repository-relative path, symbol/property, original assessed lines, and exact excerpt. Do not infer no-database architecture from an absent driver alone. Use Step 1 production-use evidence and approved context.

#### Quality caveats

- Database-independent does not automatically mean stateless or multi-active.
- Kafka Streams state stores, compacted topics, local RocksDB, and external side effects create recovery and ownership requirements.
- Do not require a database solely to implement idempotency; use the approved durable mechanism for the workload.
- Scenario topology remains external evidence unless supplied through approved context.

---

### KAFKA-DI-011: Health and telemetry reflect processing rather than database state

**Severity:** Critical  
**Category:** health  
**Applies when:** operating scenario is `database_independent_kafka`

#### Requirement

The application must implement this behavior for Kafka processing with no application database. Applicability depends on the processing model, regional ownership, external side effects, and Kafka-backed or local state.

#### Repository evidence to inspect

- Kafka producer, consumer, or Streams topology
- Event and business-operation identity
- Consumer completion and offset handling
- Regional activation and ownership configuration
- External client side effects
- Kafka Streams, compacted-topic, or local state-store configuration
- Failure and recovery tests

#### Finding condition

Emit a finding when repository evidence demonstrates that the required database-independent Kafka behavior is absent, unsafe, or incompatible with the declared processing and ownership model.

#### Evidence rule

Cite repository-relative path, symbol/property, original assessed lines, and exact excerpt. Do not infer no-database architecture from an absent driver alone. Use Step 1 production-use evidence and approved context.

#### Quality caveats

- Database-independent does not automatically mean stateless or multi-active.
- Kafka Streams state stores, compacted topics, local RocksDB, and external side effects create recovery and ownership requirements.
- Do not require a database solely to implement idempotency; use the approved durable mechanism for the workload.
- Scenario topology remains external evidence unless supplied through approved context.

---

### KAFKA-DI-012: Database-independent scenario behavior is fault-tested

**Severity:** Critical  
**Category:** testing  
**Applies when:** operating scenario is `database_independent_kafka`

#### Requirement

The application must implement this behavior for Kafka processing with no application database. Applicability depends on the processing model, regional ownership, external side effects, and Kafka-backed or local state.

#### Repository evidence to inspect

- Kafka producer, consumer, or Streams topology
- Event and business-operation identity
- Consumer completion and offset handling
- Regional activation and ownership configuration
- External client side effects
- Kafka Streams, compacted-topic, or local state-store configuration
- Failure and recovery tests

#### Finding condition

Emit a finding when repository evidence demonstrates that the required database-independent Kafka behavior is absent, unsafe, or incompatible with the declared processing and ownership model.

#### Evidence rule

Cite repository-relative path, symbol/property, original assessed lines, and exact excerpt. Do not infer no-database architecture from an absent driver alone. Use Step 1 production-use evidence and approved context.

#### Quality caveats

- Database-independent does not automatically mean stateless or multi-active.
- Kafka Streams state stores, compacted topics, local RocksDB, and external side effects create recovery and ownership requirements.
- Do not require a database solely to implement idempotency; use the approved durable mechanism for the workload.
- Scenario topology remains external evidence unless supplied through approved context.


## Standard finding format

- **Title:** [scenario-specific application gap]
- **Control:** [KAFKA-NNN, KAFKA-AA-NNN, or KAFKA-AS-NNN]
- **Related controls:** [control IDs]
- **Operating scenario:** [resolved scenario]
- **Scenario rule ID:** [policy rule]
- **Severity:** [severity]
- **Repository evidence:** [path, symbol/property, original lines, excerpt]
- **Observed behavior:** [effective behavior]
- **Regional and state-alignment risk:** [impact]
- **Required code/configuration change:** [remediation]
- **Validation test:** [scenario-specific test]

## Non-findings

- Missing regional Kafka clusters, Cluster Linking, Schema Linking, replicated ACLs, mirror-topic promotion, or offset synchronization when deployment evidence is unavailable.
- Missing Cosmos DB multi-region writes or Azure SQL failover group when only repository evidence is available; record external evidence required.
- Stretched-cluster recommendations. This standard supports independent regional clusters or active-standby only.
- PCF migration, modernization, cleanup, or findings.
