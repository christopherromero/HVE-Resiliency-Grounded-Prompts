---
schema_version: 2.2.0
document_type: dependency_behavior
standard_id: SPRINGBOOT-MONGODB
service: mongodb
service_name: MongoDB and Azure Cosmos DB for MongoDB
language: java
framework: spring-boot
runtime_platform: aks
version: 1.1.0
assessment_scope: application_code_and_repository_owned_configuration
lifecycle_status: active
repository_owned_only: true
infrastructure_findings_allowed: false
assessment:
  enabled: true
  emit_findings: true
  include_in_score: true
  unknown_evidence_status: not_assessed
infrastructure_assumptions:
- Two independent Azure regions are provisioned and active.
- Account, cluster, networking, private endpoints, DNS, identities, and replication
  topology follow the approved multi-region infrastructure design.
- The deployment pipeline injects region-specific configuration into the same application
  artifact.
- The application repository does not provision or validate infrastructure.
api_variant_detection:
  resolution_rule: governed_cosmos_variant_resolution_with_positive_evidence_for_observed_identity
  policy_path: grounding/governance/cosmos-mongodb-variant-policy.yml
  policy_id: COSMOS-MONGODB-VARIANT
  policy_version: "1.0.0"
  inventory_record: cosmos_mongodb_variant_resolution
  observed_variant_rule: require_positive_repository_evidence
  native_mongodb_rule: require_positive_repository_evidence
  target_variant_rule: honor_recorded_governed_default_and_explicit_exceptions
  unknown_variant_behavior: not_assessed_for_variant_conditional_controls
  variants:
  - id: native_mongodb
    display_name: Native MongoDB replica set or sharded cluster
    detect_patterns:
    - mongodb://
    - mongodb+srv://
    - replicaSet=
    - authSource=admin
  - id: cosmos_mongo_ru
    display_name: Azure Cosmos DB for MongoDB, request-unit model
    detect_patterns:
    - .mongo.cosmos.azure.com
    - retrywrites=false
    - '16500'
    - '16501'
    - RU
  - id: cosmos_mongo_vcore
    display_name: Azure Cosmos DB for MongoDB, vCore model
    detect_patterns:
    - .mongocluster.cosmos.azure.com
    - vcore
  variant_capability_notes:
    multi_document_transactions: native_mongodb and cosmos_mongo_vcore support multi-document
      transactions; cosmos_mongo_ru support is limited and version dependent
    change_streams: capability and resume semantics differ by variant and version
    retryable_writes: cosmos_mongo_ru commonly requires retrywrites=false, which removes
      driver-level write retry and shifts the obligation to the application
    throttling_errors: cosmos_mongo_ru surfaces request-rate-exceeded errors that native
      MongoDB does not
shared_service_assessment_scope:
  service_key: mongodb
  service_key_resolution: per_integration_provider_aware_scope_binding
  variant_service_keys: {native_mongodb: mongodb, cosmos_mongo_ru: cosmosdb, cosmos_mongo_vcore: cosmosdb}
  context_path: architecture_context.shared_service_assessment_scope.services
  schema_path: grounding/governance/shared-service-assessment-scope-schema.yml
  evaluation_gate: required
  control_evaluation_allowed_only_when: in_scope
  architecture_reasoning_allowed_for:
  - in_scope
  - out_of_scope
  - informational_only
  - architecture_only
  scope_conflict_behavior: architecture_governance_review
  contract_section: Shared-service assessment-scope contract
controls:
- id: MONGO-001
  title: Connection string, database, and region are deployment-injected
  severity: critical
  category: configuration
  applies_when: the application connects to MongoDB or Cosmos DB for MongoDB
  evidence_patterns:
  - spring.data.mongodb.uri
  - MONGODB_URI
  - MongoClientSettings
  - MongoTemplate
  - database
  finding_when: a host, region, cluster, or database name is hardcoded or defaulted
    in the artifact so the same build cannot be promoted unchanged across regions
  emit_on_failure: true
- id: MONGO-002
  title: Write concern matches durability requirements
  severity: critical
  category: consistency
  applies_when: the application performs writes
  evidence_patterns:
  - WriteConcern
  - w=majority
  - journal
  - setWriteConcern
  - spring.data.mongodb
  finding_when: business-critical writes acknowledge before durable replication, or
    write concern is left to an unstated default that cannot be shown to meet the approved
    durability contract
  emit_on_failure: true
- id: MONGO-003
  title: Read preference and read concern match the regional model
  severity: critical
  category: regional-affinity
  applies_when: the application reads from a multi-region account or replica set
  evidence_patterns:
  - ReadPreference
  - readPreference
  - secondaryPreferred
  - ReadConcern
  - nearest
  finding_when: reads can be served from a region or replica inconsistent with the
    approved consistency contract, or normal reads cross regions unexpectedly and add
    unapproved latency
  emit_on_failure: true
- id: MONGO-004
  title: Read-your-writes assumptions survive the regional model
  severity: critical
  category: consistency
  applies_when: the application writes and then reads the same logical record within
    one workflow
  evidence_patterns:
  - ClientSession
  - causallyConsistent
  - session token
  - findById
  - save(
  finding_when: application logic assumes a write is immediately visible to a subsequent
    read while the effective read preference, consistency level, or region can serve
    a stale replica, and no causal session, re-read, or reconciliation compensates
  emit_on_failure: true
- id: MONGO-005
  title: Retryable writes and reads are enabled or compensated
  severity: critical
  category: resilience
  applies_when: the application performs writes against a replicated deployment
  evidence_patterns:
  - retryWrites
  - retrywrites=false
  - retryReads
  - MongoClientSettings
  - RetryTemplate
  finding_when: retryable writes are disabled without an application-level compensating
    mechanism, or retry is applied to a non-idempotent write without stable business
    identity
  emit_on_failure: true
- id: MONGO-006
  title: Operation, connection, and server-selection timeouts are bounded
  severity: critical
  category: timeout
  applies_when: the application issues database operations
  evidence_patterns:
  - connectTimeout
  - socketTimeout
  - serverSelectionTimeout
  - maxTime
  - waitQueueTimeout
  finding_when: connection, server-selection, socket, pool-acquire, or operation deadlines
    are unbounded or defaulted so a degraded region can stall request threads beyond
    the caller deadline
  emit_on_failure: true
- id: MONGO-007
  title: Connection pool is bounded and sized for the workload
  severity: high
  category: resource-management
  applies_when: the application uses a shared MongoClient
  evidence_patterns:
  - maxPoolSize
  - minPoolSize
  - maxIdleTime
  - waitQueueTimeout
  - MongoClient
  finding_when: the pool is unbounded, materially exceeds downstream capacity without
    rationale, is recreated per request, or pool exhaustion produces unbounded waiting
    instead of a bounded failure
  emit_on_failure: true
- id: MONGO-008
  title: Non-idempotent writes carry stable business identity
  severity: critical
  category: data-correctness
  applies_when: a write can be retried, replayed, or executed concurrently from more
    than one region
  evidence_patterns:
  - _id
  - business key
  - upsert
  - unique index
  - insertOne
  finding_when: a retried, replayed, or cross-region write can create a duplicate business
    record because identity is generated per attempt rather than derived from stable
    business data
  emit_on_failure: true
- id: MONGO-009
  title: Multi-document consistency is explicit and variant-aware
  severity: critical
  category: consistency
  applies_when: one business operation writes more than one document or collection
  evidence_patterns:
  - startSession
  - withTransaction
  - MongoTransactionManager
  - Transactional
  - bulkWrite
  finding_when: a multi-document business operation has no transaction, no documented
    ordering and compensation, or assumes transaction support the detected API variant
    does not provide
  emit_on_failure: true
- id: MONGO-010
  title: Optimistic concurrency and conflict behavior are defined
  severity: critical
  category: consistency
  applies_when: a document can be updated concurrently from more than one request or
    region
  evidence_patterns:
  - Version
  - OptimisticLockingFailureException
  - findAndModify
  - '$set'
  - save(
  finding_when: a read-modify-write sequence can silently overwrite a concurrent update,
    or an optimistic-locking failure has no defined retry, merge, or user-visible outcome
  emit_on_failure: true
- id: MONGO-011
  title: Shard key and unique constraints support the regional write model
  severity: critical
  category: data-model
  applies_when: the collection is sharded or partitioned, or declares unique constraints
  evidence_patterns:
  - shard key
  - Indexed(unique
  - CompoundIndex
  - partition key
  - createIndex
  finding_when: the shard or partition key forces cross-partition writes on the hot
    path, or a uniqueness guarantee is assumed that the deployment model cannot enforce
    across partitions or regions
  emit_on_failure: true
- id: MONGO-012
  title: Throttling and rate-limit responses are handled
  severity: critical
  category: resilience
  applies_when: the resolved assessment variant enforces request-unit or rate limits
  variant_conditional: true
  required_variant: cosmos_mongo_ru
  evidence_patterns:
  - '16500'
  - '16501'
  - TooManyRequests
  - RetryAfterMs
  - MongoCommandException
  finding_when: request-rate-exceeded responses are treated as generic failures, retried
    without honoring the server-provided delay, retried without a bound, or surfaced
    to the caller as data loss
  emit_on_failure: true
- id: MONGO-013
  title: Change streams and tailing are resumable and region-safe
  severity: high
  category: event-processing
  applies_when: the application consumes change streams or tails a collection
  evidence_patterns:
  - watch(
  - ChangeStream
  - resumeToken
  - startAfter
  - MessageListenerContainer
  finding_when: a change-stream consumer cannot resume from a durable token after disconnect
    or failover, processes events non-idempotently, or can run concurrently in both
    regions without an approved ownership model
  emit_on_failure: true
- id: MONGO-014
  title: Critical MongoDB failure affects readiness but not liveness
  severity: critical
  category: health
  applies_when: MongoDB contributes to application health
  evidence_patterns:
  - MongoHealthIndicator
  - ReactiveMongoHealthIndicator
  - readiness group
  - management.endpoint.health.group.readiness
  - health timeout
  finding_when: a critical region-local database failure leaves readiness UP, the database
    participates in liveness and creates restart loops, or the health check is unbounded
    or does not exercise the real serving path
  emit_on_failure: true
- id: MONGO-015
  title: Driver reconnect and topology discovery recover without restart
  severity: high
  category: recovery
  applies_when: the deployment can fail over, scale, or change primary
  evidence_patterns:
  - MongoClient
  - heartbeatFrequency
  - serverSelectionTimeout
  - MongoSocketException
  - cluster listener
  finding_when: the client remains pinned to a failed node or region after failover,
    requires a pod restart to recover, or treats a transient topology change as a terminal
    failure
  emit_on_failure: true
- id: MONGO-016
  title: Queries are indexed, filtered, and bounded
  severity: high
  category: performance
  applies_when: the application issues queries
  evidence_patterns:
  - findAll
  - Query(
  - Indexed
  - limit
  - sort
  finding_when: a hot-path query has no supporting index, scans an unbounded collection,
    or sorts without an index so a degraded or throttled region amplifies latency and
    cost
  emit_on_failure: true
- id: MONGO-017
  title: Large result sets are streamed or paginated
  severity: high
  category: resource-management
  applies_when: a query can return a large or unbounded result set
  evidence_patterns:
  - findAll
  - Pageable
  - Stream
  - batchSize
  - cursor
  finding_when: an unbounded result set is materialized into memory, or pagination
    is absent on a collection that grows without limit
  emit_on_failure: true
- id: MONGO-018
  title: Credentials and connection material are externalized and rotatable
  severity: critical
  category: security-material
  applies_when: the application authenticates to the database
  evidence_patterns:
  - mongodb://
  - password
  - KeyVault
  - managed identity
  - application.yml
  finding_when: credentials or a credential-bearing connection string are committed,
    defaulted, or logged, or rotation requires a code change
  emit_on_failure: true
- id: MONGO-019
  title: Diagnostics avoid leaking query payloads or personal data
  severity: high
  category: observability
  applies_when: the application logs or traces database activity
  evidence_patterns:
  - logger
  - toString
  - Query
  - exception message
  - command logging
  finding_when: queries, documents, filters, or exception detail containing personal
    data or credentials are written to logs, traces, or error responses
  emit_on_failure: true
- id: MONGO-020
  title: Database telemetry identifies region, operation, and outcome
  severity: high
  category: observability
  applies_when: the application is operated as a production workload
  evidence_patterns:
  - micrometer
  - CommandListener
  - trackDependency
  - region
  - correlationId
  finding_when: database latency, failure, retry, and throttling cannot be attributed
    to a region, operation, and outcome, or telemetry omits the correlation identity
    needed to trace a failed business operation
  emit_on_failure: true
- id: MONGO-021
  title: Tests cover failover, throttling, retry, and duplicate writes
  severity: critical
  category: testing
  applies_when: the repository contains automated tests for data access
  evidence_patterns:
  - Testcontainers
  - EmbeddedMongo
  - flapdoodle
  - fault injection
  - integration test
  finding_when: tests do not prove primary failover, read staleness, throttling, retry
    exhaustion, optimistic-lock conflict, and duplicate write behavior against a real
    driver path
  emit_on_failure: true
---

# MongoDB and Cosmos DB for MongoDB Target-State Application Behavior Standard

### Shared-service assessment-scope contract

Before evaluating controls, resolve each production integration through `provider_aware_scope_binding` in `grounding/governance/shared-service-assessment-scope-schema.yml`. Native MongoDB, including Atlas, uses `mongodb` scope; Cosmos Mongo RU and vCore use `cosmosdb` scope. The behavior standard remains `SPRINGBOOT-MONGODB` in both cases. Preserve `integration_id`, API variant, canonical service key, scope, and evidence provenance. Never let an Atlas exclusion suppress Cosmos Mongo coverage or an in-scope Cosmos integration enable Atlas findings. Unknown or conflicting providers remain `not_assessed` pending architecture review, rather than inheriting default scope. Evaluate controls and generate findings only for an effective `in_scope` integration. Preserve all non-in-scope integrations for inventory and architecture reasoning; scope conflicts are not code findings.

### Shared-service operating-model contract

This standard does not select the application's shared-service topology. Resolve the operating model from:

```text
architecture_context.shared_service_operating_models.services.<resolved-service-key>
```

Use `source.operating_model` only to describe current state. Use `target.operating_model` for control applicability and target-state code-readiness assessment.

Use the same resolved service key for connectivity contracts. Cosmos Mongo uses the Cosmos service's contracts but MongoDB driver controls, not Cosmos Java SDK settings. For Atlas Global Cluster with active-active Kafka, apply `grounding/governance/mongodb-atlas-kafka-operating-scenario-policy.yml`. This is the only supported Atlas/Kafka target pairing; other source models may be retained as migration context. Apply MONGO-011 to approved zone/shard routing and uniqueness, MONGO-002 through MONGO-005 to the approved read/write contract, and MONGO-015 to primary elections. Do not equate geographically distributed shard primaries with unrestricted multi-primary writes to the same record.

- Evaluate common data-access controls whenever production use is confirmed.
- Evaluate model-specific controls only for the resolved target operating model.
- Missing, unresolved, or conflicting target model makes model-specific controls `not_assessed` and routes to architecture review.
- A source-target difference is migration context, not a finding by itself.
- Findings require repository-owned evidence that the application is incompatible with an applicable target-state control.
- Do not infer deployed topology from this standard's title, examples, or assumptions.

## Purpose

Evaluate repository-owned Spring Data MongoDB and MongoDB driver usage for durable writes, correct regional read semantics, safe retry and conflict behavior, bounded resource use, and honest health signaling when the same artifact runs in more than one region.

## API variant applicability

Controls apply across deployment variants. The variant determines **which capability satisfies a control and which failure modes exist**, not whether the control applies.

Use the Step 1 `cosmos_mongodb_variant_resolution` for confirmed Cosmos DB for
MongoDB, following `grounding/governance/cosmos-mongodb-variant-policy.yml`.
Use the policy's `standard_variant_mapping` to map `ru` to `cosmos_mongo_ru`
and `vcore` to `cosmos_mongo_vcore`. Native MongoDB still requires positive
repository evidence. Resolve applicability for the selected assessment state,
then apply:

| Concern | Native MongoDB | Cosmos DB for MongoDB, RU | Cosmos DB for MongoDB, vCore |
|---|---|---|---|
| Multi-document transactions | Supported on replica sets and sharded clusters | Limited and version dependent; verify before relying on them | Supported |
| Retryable writes | Default enabled | Commonly requires `retrywrites=false`, which removes driver-level retry | Generally supported |
| Throttling errors | Not applicable | Request-rate-exceeded errors such as `16500` and `16501` with a server-provided delay | Not applicable in the same form |
| Change streams | Supported with resume tokens | Capability and resume semantics differ by version | Supported |

Rules:

- For confirmed Cosmos MongoDB target-state assessment, an absent variant declaration resolves to RU through the shared governed default unless positive vCore evidence or another terminal gate prevents it. Do not request separate RU confirmation solely because the variant is omitted.
- Explicit approved declarations and positive vCore evidence prevent defaulting; same-state conflicts or invalid declarations require architecture review. Different approved source and target variants remain migration intent.
- Preserve the inventory's model, resolution source, default-applied flag, policy identity, observed variant, and deployed-verification flag without recalculating them during evaluation.
- When resolution genuinely remains unknown, mark variant-conditional controls `not_assessed` and record the specific unresolved predicate.
- Record the resolved assessment variant and its full provenance in every finding produced by a variant-conditional control. Keep architecture and policy provenance outside repository source evidence.
- A governed RU default establishes control applicability, not a deployed account fact or a defect. Findings still require repository-owned behavior incompatible with the applicable control.
- Do not assume Cosmos behavior for a native deployment or the reverse.
- `MONGO-012` applies when `cosmos_mongo_ru` is resolved for the selected assessment state, including the governed target default; it does not apply to a resolved vCore exception.

## Controls

### MONGO-001: Connection string, database, and region are deployment-injected

**Severity:** Critical  
**Category:** configuration  
**Applies when:** the application connects to MongoDB or Cosmos DB for MongoDB

#### Requirement

One artifact must connect to the correct regional deployment through injected configuration.

#### Repository evidence to inspect

- `spring.data.mongodb.uri`
- `MONGODB_URI`
- `MongoClientSettings`
- `MongoTemplate`
- `database`

#### Finding condition

Emit a finding when evidence shows that a host, region, cluster, or database name is hardcoded or defaulted in the artifact so the same build cannot be promoted unchanged across regions.

#### Evidence rule

Cite the repository-relative file path, symbol or property, original assessed line range, and exact source excerpt when available. If evidence is unavailable or external, return `not_assessed` rather than assuming noncompliance.

#### Quality caveats

- A local development default such as `mongodb://localhost:27017` is a finding only when it can take effect in a deployed profile.
- Deduplicate with `APP-AA-002` under one root cause.

---

### MONGO-002: Write concern matches durability requirements

**Severity:** Critical  
**Category:** consistency  
**Applies when:** the application performs writes

#### Requirement

Business-critical writes must acknowledge only after the approved durability threshold is met.

#### Repository evidence to inspect

- `WriteConcern`
- `w=majority`
- `journal`
- `setWriteConcern`
- `spring.data.mongodb`

#### Finding condition

Emit a finding when evidence shows that business-critical writes acknowledge before durable replication, or that write concern is left to an unstated default that cannot be shown to meet the approved durability contract.

#### Evidence rule

Cite the repository-relative file path, symbol or property, original assessed line range, and exact source excerpt when available. If evidence is unavailable or external, return `not_assessed` rather than assuming noncompliance.

#### Quality caveats

- Driver defaults differ by variant and version. Evaluate the effective write concern, not the absence of a setting alone.

---

### MONGO-003: Read preference and read concern match the regional model

**Severity:** Critical  
**Category:** regional-affinity  
**Applies when:** the application reads from a multi-region account or replica set

#### Requirement

Reads must be served from a region and replica consistent with the approved consistency and latency contract.

#### Repository evidence to inspect

- `ReadPreference`
- `readPreference`
- `secondaryPreferred`
- `ReadConcern`
- `nearest`

#### Finding condition

Emit a finding when evidence shows that reads can be served from a region or replica inconsistent with the approved consistency contract, or that normal reads cross regions unexpectedly and add unapproved latency.

#### Evidence rule

Cite the repository-relative file path, symbol or property, original assessed line range, and exact source excerpt when available. If evidence is unavailable or external, return `not_assessed` rather than assuming noncompliance.

#### Quality caveats

- `secondaryPreferred` improves read scaling and weakens freshness. It is a finding only when the workflow requires freshness the setting cannot provide.
- Deduplicate with `APP-AA-003` under one root cause.

---

### MONGO-004: Read-your-writes assumptions survive the regional model

**Severity:** Critical  
**Category:** consistency  
**Applies when:** the application writes and then reads the same logical record within one workflow

#### Requirement

A workflow that depends on seeing its own write must remain correct under the effective regional read path.

#### Repository evidence to inspect

- `ClientSession`
- `causallyConsistent`
- `session token`
- `findById`
- `save(`

#### Finding condition

Emit a finding when evidence shows that application logic assumes a write is immediately visible to a subsequent read while the effective read preference, consistency level, or region can serve a stale replica, and no causal session, re-read, or reconciliation compensates.

#### Evidence rule

Cite the repository-relative file path, symbol or property, original assessed line range, and exact source excerpt when available. If evidence is unavailable or external, return `not_assessed` rather than assuming noncompliance.

#### Quality caveats

- This is a defining single-region to multi-region behavior change. Code that writes then immediately reads is correct in one region and can break when the read is served elsewhere.
- Returning the in-memory saved object instead of re-reading is a valid remediation and is not itself a finding.

---

### MONGO-005: Retryable writes and reads are enabled or compensated

**Severity:** Critical  
**Category:** resilience  
**Applies when:** the application performs writes against a replicated deployment

#### Requirement

Transient write failures during election or failover must be recoverable without duplicating a business effect.

#### Repository evidence to inspect

- `retryWrites`
- `retrywrites=false`
- `retryReads`
- `MongoClientSettings`
- `RetryTemplate`

#### Finding condition

Emit a finding when evidence shows that retryable writes are disabled without an application-level compensating mechanism, or that retry is applied to a non-idempotent write without stable business identity.

#### Evidence rule

Cite the repository-relative file path, symbol or property, original assessed line range, and exact source excerpt when available. If evidence is unavailable or external, return `not_assessed` rather than assuming noncompliance.

#### Quality caveats

- Request-unit Cosmos deployments commonly require `retrywrites=false`. That configuration is not itself the finding; the absence of a compensating application mechanism is.
- Pair with `MONGO-008` when identity is also unstable.

---

### MONGO-006: Operation, connection, and server-selection timeouts are bounded

**Severity:** Critical  
**Category:** timeout  
**Applies when:** the application issues database operations

#### Requirement

Every layer of the database call budget must be bounded and must fit inside the caller deadline.

#### Repository evidence to inspect

- `connectTimeout`
- `socketTimeout`
- `serverSelectionTimeout`
- `maxTime`
- `waitQueueTimeout`

#### Finding condition

Emit a finding when evidence shows that connection, server-selection, socket, pool-acquire, or operation deadlines are unbounded or defaulted so a degraded region can stall request threads beyond the caller deadline.

#### Evidence rule

Cite the repository-relative file path, symbol or property, original assessed line range, and exact source excerpt when available. If evidence is unavailable or external, return `not_assessed` rather than assuming noncompliance.

#### Quality caveats

- Server-selection timeout governs behavior during failover. An unbounded value converts a brief election into a sustained outage.
- Deduplicate with `APP-AA-004` and `JVM-021` under one root cause.

---

### MONGO-007: Connection pool is bounded and sized for the workload

**Severity:** High  
**Category:** resource-management  
**Applies when:** the application uses a shared MongoClient

#### Requirement

Pool capacity must be bounded, shared, and aligned to downstream capacity with a bounded acquisition failure path.

#### Repository evidence to inspect

- `maxPoolSize`
- `minPoolSize`
- `maxIdleTime`
- `waitQueueTimeout`
- `MongoClient`

#### Finding condition

Emit a finding when evidence shows that the pool is unbounded, materially exceeds downstream capacity without rationale, is recreated per request, or that pool exhaustion produces unbounded waiting instead of a bounded failure.

#### Evidence rule

Cite the repository-relative file path, symbol or property, original assessed line range, and exact source excerpt when available. If evidence is unavailable or external, return `not_assessed` rather than assuming noncompliance.

#### Quality caveats

- `MongoClient` is designed to be a long-lived singleton. Per-request construction is a defect, not a style choice.

---

### MONGO-008: Non-idempotent writes carry stable business identity

**Severity:** Critical  
**Category:** data-correctness  
**Applies when:** a write can be retried, replayed, or executed concurrently from more than one region

#### Requirement

A repeated write for one business intent must converge to one record.

#### Repository evidence to inspect

- `_id`
- `business key`
- `upsert`
- `unique index`
- `insertOne`

#### Finding condition

Emit a finding when evidence shows that a retried, replayed, or cross-region write can create a duplicate business record because identity is generated per attempt rather than derived from stable business data.

#### Evidence rule

Cite the repository-relative file path, symbol or property, original assessed line range, and exact source excerpt when available. If evidence is unavailable or external, return `not_assessed` rather than assuming noncompliance.

#### Quality caveats

- A driver-generated `ObjectId` per attempt is identity for the document, not idempotency for the business operation.
- Deduplicate with `APP-AA-011` and `APP-FIN-003` under one root cause.

---

### MONGO-009: Multi-document consistency is explicit and variant-aware

**Severity:** Critical  
**Category:** consistency  
**Applies when:** one business operation writes more than one document or collection

#### Requirement

A multi-document operation must be atomic, or must define ordering, failure visibility, and compensation.

#### Repository evidence to inspect

- `startSession`
- `withTransaction`
- `MongoTransactionManager`
- `Transactional`
- `bulkWrite`

#### Finding condition

Emit a finding when evidence shows that a multi-document business operation has no transaction, no documented ordering and compensation, or assumes transaction support the detected API variant does not provide.

#### Evidence rule

Cite the repository-relative file path, symbol or property, original assessed line range, and exact source excerpt when available. If evidence is unavailable or external, return `not_assessed` rather than assuming noncompliance.

#### Quality caveats

- `@Transactional` has no effect without a configured `MongoTransactionManager`.
- Transaction support differs by variant and version. Verify the detected variant before proposing a transaction-based remediation.
- Deduplicate with `APP-DB-003` under one root cause.

---

### MONGO-010: Optimistic concurrency and conflict behavior are defined

**Severity:** Critical  
**Category:** consistency  
**Applies when:** a document can be updated concurrently from more than one request or region

#### Requirement

Concurrent updates must not silently discard each other, and conflict outcomes must be defined.

#### Repository evidence to inspect

- `@Version`
- `OptimisticLockingFailureException`
- `findAndModify`
- `$set`
- `save(`

#### Finding condition

Emit a finding when evidence shows that a read-modify-write sequence can silently overwrite a concurrent update, or that an optimistic-locking failure has no defined retry, merge, or user-visible outcome.

#### Evidence rule

Cite the repository-relative file path, symbol or property, original assessed line range, and exact source excerpt when available. If evidence is unavailable or external, return `not_assessed` rather than assuming noncompliance.

#### Quality caveats

- Repository `save()` of a fully mapped entity replaces the document. Without a version field this is a last-writer-wins overwrite.
- Targeted field updates reduce but do not eliminate conflict risk.
- Deduplicate with `APP-AA-012` under one root cause.

---

### MONGO-011: Shard key and unique constraints support the regional write model

**Severity:** Critical  
**Category:** data-model  
**Applies when:** the collection is sharded or partitioned, or declares unique constraints

#### Requirement

The data model must support the approved write distribution without relying on guarantees the deployment cannot provide.

#### Repository evidence to inspect

- `shard key`
- `@Indexed(unique`
- `@CompoundIndex`
- `partition key`
- `createIndex`

#### Finding condition

Emit a finding when evidence shows that the shard or partition key forces cross-partition writes on the hot path, or that a uniqueness guarantee is assumed that the deployment model cannot enforce across partitions or regions.

#### Evidence rule

Cite the repository-relative file path, symbol or property, original assessed line range, and exact source excerpt when available. If evidence is unavailable or external, return `not_assessed` rather than assuming noncompliance.

#### Quality caveats

- Unique index semantics across shards and regions are deployment dependent. Do not assert a business uniqueness rule the approved topology cannot enforce.

---

### MONGO-012: Throttling and rate-limit responses are handled

**Severity:** Critical  
**Category:** resilience  
**Applies when:** the resolved assessment variant enforces request-unit or rate limits

#### Requirement

Rate-limit responses must be recognized, delayed as instructed, bounded, and never presented as data loss.

#### Repository evidence to inspect

- `16500`
- `16501`
- `TooManyRequests`
- `RetryAfterMs`
- `MongoCommandException`

#### Finding condition

Emit a finding when evidence shows that request-rate-exceeded responses are treated as generic failures, retried without honoring the server-provided delay, retried without a bound, or surfaced to the caller as data loss.

#### Evidence rule

Cite the repository-relative file path, symbol or property, original assessed line range, and exact source excerpt when available. If evidence is unavailable or external, return `not_assessed` rather than assuming noncompliance.

#### Quality caveats

- This control applies only when a request-unit variant is detected. Mark it `not_applicable` for native MongoDB and `not_assessed` when the variant is unknown.
- Throttling during regional failover is a load-concentration event, not a defect in itself. The defect is the handling.

---

### MONGO-013: Change streams and tailing are resumable and region-safe

**Severity:** High  
**Category:** event-processing  
**Applies when:** the application consumes change streams or tails a collection

#### Requirement

A change consumer must resume from durable state and must not duplicate effects across regions.

#### Repository evidence to inspect

- `watch(`
- `ChangeStream`
- `resumeToken`
- `startAfter`
- `MessageListenerContainer`

#### Finding condition

Emit a finding when evidence shows that a change-stream consumer cannot resume from a durable token after disconnect or failover, processes events non-idempotently, or can run concurrently in both regions without an approved ownership model.

#### Evidence rule

Cite the repository-relative file path, symbol or property, original assessed line range, and exact source excerpt when available. If evidence is unavailable or external, return `not_assessed` rather than assuming noncompliance.

#### Quality caveats

- Deduplicate with `APP-WORKLOAD-002` when the defect is the absence of single-active ownership rather than resume behavior.

---

### MONGO-014: Critical MongoDB failure affects readiness but not liveness

**Severity:** Critical  
**Category:** health  
**Applies when:** MongoDB contributes to application health

#### Requirement

Readiness must reflect the ability to serve using the database. Liveness must exclude it.

#### Repository evidence to inspect

- `MongoHealthIndicator`
- `ReactiveMongoHealthIndicator`
- `readiness group`
- `management.endpoint.health.group.readiness`
- `health timeout`

#### Finding condition

Emit a finding when evidence shows that a critical region-local database failure leaves readiness UP, that the database participates in liveness and creates restart loops, or that the health check is unbounded or does not exercise the real serving path.

#### Evidence rule

Cite the repository-relative file path, symbol or property, original assessed line range, and exact source excerpt when available. If evidence is unavailable or external, return `not_assessed` rather than assuming noncompliance.

#### Quality caveats

- A globally shared database included in readiness can drain every region simultaneously. Gate on region-local criticality.
- Deduplicate with `APP-AA-007`, `APP-AA-008`, and `APP-AA-009` under one root cause.

---

### MONGO-015: Driver reconnect and topology discovery recover without restart

**Severity:** High  
**Category:** recovery  
**Applies when:** the deployment can fail over, scale, or change primary

#### Requirement

The client must rediscover topology and resume work without a process restart.

#### Repository evidence to inspect

- `MongoClient`
- `heartbeatFrequency`
- `serverSelectionTimeout`
- `MongoSocketException`
- `cluster listener`

#### Finding condition

Emit a finding when evidence shows that the client remains pinned to a failed node or region after failover, requires a pod restart to recover, or treats a transient topology change as a terminal failure.

#### Evidence rule

Cite the repository-relative file path, symbol or property, original assessed line range, and exact source excerpt when available. If evidence is unavailable or external, return `not_assessed` rather than assuming noncompliance.

#### Quality caveats

- Deduplicate with `APP-AA-014` under one root cause.

---

### MONGO-016: Queries are indexed, filtered, and bounded

**Severity:** High  
**Category:** performance  
**Applies when:** the application issues queries

#### Requirement

Hot-path queries must be supported by indexes and must not scan unbounded data.

#### Repository evidence to inspect

- `findAll`
- `@Query(`
- `@Indexed`
- `limit`
- `sort`

#### Finding condition

Emit a finding when evidence shows that a hot-path query has no supporting index, scans an unbounded collection, or sorts without an index so a degraded or throttled region amplifies latency and cost.

#### Evidence rule

Cite the repository-relative file path, symbol or property, original assessed line range, and exact source excerpt when available. If evidence is unavailable or external, return `not_assessed` rather than assuming noncompliance.

#### Quality caveats

- Index definitions may be owned outside the repository. When index state cannot be established, return `not_assessed` for the index dimension and assess the query shape only.

---

### MONGO-017: Large result sets are streamed or paginated

**Severity:** High  
**Category:** resource-management  
**Applies when:** a query can return a large or unbounded result set

#### Requirement

Result-set size must be bounded relative to available heap and the caller deadline.

#### Repository evidence to inspect

- `findAll`
- `Pageable`
- `Stream`
- `batchSize`
- `cursor`

#### Finding condition

Emit a finding when evidence shows that an unbounded result set is materialized into memory, or that pagination is absent on a collection that grows without limit.

#### Evidence rule

Cite the repository-relative file path, symbol or property, original assessed line range, and exact source excerpt when available. If evidence is unavailable or external, return `not_assessed` rather than assuming noncompliance.

#### Quality caveats

- Deduplicate with `JVM-003` and `JVM-004` when the defect is recorded as a heap-sizing or allocation finding.

---

### MONGO-018: Credentials and connection material are externalized and rotatable

**Severity:** Critical  
**Category:** security-material  
**Applies when:** the application authenticates to the database

#### Requirement

Credentials must be injected, protected, and rotatable without a code change.

#### Repository evidence to inspect

- `mongodb://`
- `password`
- `KeyVault`
- `managed identity`
- `application.yml`

#### Finding condition

Emit a finding when evidence shows that credentials or a credential-bearing connection string are committed, defaulted, or logged, or that rotation requires a code change.

#### Evidence rule

Cite the repository-relative file path, symbol or property, original assessed line range, and exact source excerpt when available. Redact protected values while preserving the surrounding evidence. If evidence is unavailable or external, return `not_assessed` rather than assuming noncompliance.

#### Quality caveats

- A connection string embeds credentials. Treat it as secret material even when the host alone would not be.

---

### MONGO-019: Diagnostics avoid leaking query payloads or personal data

**Severity:** High  
**Category:** observability  
**Applies when:** the application logs or traces database activity

#### Requirement

Diagnostics must be useful without exposing document contents, filters, or credentials.

#### Repository evidence to inspect

- `logger`
- `toString`
- `Query`
- `exception message`
- `command logging`

#### Finding condition

Emit a finding when evidence shows that queries, documents, filters, or exception detail containing personal data or credentials are written to logs, traces, or error responses.

#### Evidence rule

Cite the repository-relative file path, symbol or property, original assessed line range, and exact source excerpt when available. Redact protected values while preserving the surrounding evidence. If evidence is unavailable or external, return `not_assessed` rather than assuming noncompliance.

#### Quality caveats

- Deduplicate with `APP-LOG-001` and `APP-LOG-002` under one root cause.

---

### MONGO-020: Database telemetry identifies region, operation, and outcome

**Severity:** High  
**Category:** observability  
**Applies when:** the application is operated as a production workload

#### Requirement

Database behavior must be attributable to a region, operation, and outcome during an incident.

#### Repository evidence to inspect

- `micrometer`
- `CommandListener`
- `trackDependency`
- `region`
- `correlationId`

#### Finding condition

Emit a finding when evidence shows that database latency, failure, retry, and throttling cannot be attributed to a region, operation, and outcome, or that telemetry omits the correlation identity needed to trace a failed business operation.

#### Evidence rule

Cite the repository-relative file path, symbol or property, original assessed line range, and exact source excerpt when available. If evidence is unavailable or external, return `not_assessed` rather than assuming noncompliance.

#### Quality caveats

- Deduplicate with `APP-AA-015` and `APP-OBS-001` under one root cause.

---

### MONGO-021: Tests cover failover, throttling, retry, and duplicate writes

**Severity:** Critical  
**Category:** testing  
**Applies when:** the repository contains automated tests for data access

#### Requirement

Tests must exercise the real driver path under failure, not only mapped happy-path persistence.

#### Repository evidence to inspect

- `Testcontainers`
- `EmbeddedMongo`
- `flapdoodle`
- `fault injection`
- `integration test`

#### Finding condition

Emit a finding when evidence shows that tests do not prove primary failover, read staleness, throttling, retry exhaustion, optimistic-lock conflict, and duplicate write behavior against a real driver path.

#### Evidence rule

Cite the repository-relative file path, symbol or property, original assessed line range, and exact source excerpt when available. If evidence is unavailable or external, return `not_assessed` rather than assuming noncompliance.

#### Quality caveats

- An embedded single-node MongoDB cannot prove replica-set failover, write-concern behavior, or throttling. Tests built on it satisfy mapping coverage only.

---

## Evidence and finding rules

- Use the control `severity` and `category` declared in frontmatter; do not reassign severity per finding.
- Record the resolved assessment API variant and the architecture, repository, or governed-default provenance that established applicability in every variant-conditional finding. Preserve `observed_throughput_model` independently and never represent a default as repository evidence.
- Return `not_assessed` when the repository lacks evidence to evaluate an applicable control.
- Evaluate effective behavior rather than the presence of an annotation, property, or default alone.
- Deduplicate with the master standard under one root cause; attribute the finding here when the defect is expressed in MongoDB driver or Spring Data MongoDB usage.

## Finding classification

Resiliency classification follows `grounding/governance/resiliency-finding-qualification-policy.yml`. Unbounded timeouts, stale-read assumptions, last-writer-wins overwrites, duplicate writes, unhandled throttling, and incorrect health signaling qualify as `resiliency`. Naming, mapping style, and non-behavioral schema preferences are `non_resiliency`.

## Non-findings

- Account, cluster, region, replication topology, private endpoint, DNS, and firewall provisioning.
- Deployed index state when the repository does not own the definition.
- Request-unit or vCore capacity sizing.
- Choice of Spring Data repositories versus `MongoTemplate` where the required behavior is present.
