---
schema_version: 2.0.0
document_type: dependency_behavior
service: azure-managed-redis
service_name: Azure Managed Redis
language: java
framework: spring-boot
runtime_platform: aks-or-azure-hosted
assessment_scope: application_code_and_repository_owned_configuration
lifecycle_status: active
assessment:
  enabled: true
  emit_findings: true
  include_in_score: true
  unknown_evidence_status: not_assessed
infrastructure_assumptions:
- Azure Managed Redis deployment, zones, active geo-replication, networking, DNS,
  private endpoints, Entra configuration, capacity, and maintenance configuration
  are external unless repository-owned evidence is explicitly in scope.
controls:
- id: REDIS-001
  title: Redis role and authoritative source are explicit
  severity: critical
  category: data-correctness
  applies_when: Redis is used
  evidence_patterns:
  - RedisTemplate
  - ReactiveRedisTemplate
  - RedisCacheManager
  - source of truth
  - system of record
  finding_when: business correctness or durable recovery depends on Redis without
    an explicit authoritative source and recovery contract
  emit_on_failure: true
- id: REDIS-002
  title: Cache residency is not required for correctness
  severity: critical
  category: data-correctness
  applies_when: Redis is used as a cache
  evidence_patterns:
  - cache miss
  - fallback loader
  - authoritative repository
  - null cache value
  finding_when: cache miss, eviction, restart, or regional failover causes incorrect
    authorization, pricing, transaction, or workflow behavior
  emit_on_failure: true
- id: REDIS-003
  title: Redis endpoint and region selection are externally configured
  severity: critical
  category: configuration
  applies_when: Redis client exists
  evidence_patterns:
  - spring.data.redis.host
  - spring.data.redis.url
  - RedisURI
  - RedisStandaloneConfiguration
  - RedisClusterConfiguration
  finding_when: a physical regional endpoint, port, database, or topology is hardcoded
    or a remote region is the normal endpoint without an explicit policy
  emit_on_failure: true
- id: REDIS-004
  title: Authentication and TLS use approved external identity and secret delivery
  severity: critical
  category: security
  applies_when: Redis authentication is used
  evidence_patterns:
  - password
  - username
  - SSL
  - TLS
  - DefaultAzureCredential
  - Entra ID
  finding_when: credentials are committed, embedded, logged, or TLS verification is
    disabled
  emit_on_failure: true
- id: REDIS-005
  title: Connection establishment and commands are bounded
  severity: critical
  category: resilience
  applies_when: Redis client exists
  evidence_patterns:
  - connectTimeout
  - commandTimeout
  - timeout
  - LettuceClientConfiguration
  - JedisPoolConfig
  finding_when: connection, pool acquisition, command, topology refresh, or complete
    cache operation can exceed the request or workload budget
  emit_on_failure: true
- id: REDIS-006
  title: Clients and connections recover after failover without restart
  severity: critical
  category: recovery
  applies_when: Redis client exists
  evidence_patterns:
  - autoReconnect
  - ClusterTopologyRefreshOptions
  - validateConnection
  - reconnect
  - refreshPeriod
  finding_when: closed or stale connections persist after failover and application
    recovery requires a pod/process restart
  emit_on_failure: true
- id: REDIS-007
  title: Retry is bounded and safe for the command semantics
  severity: high
  category: resilience
  applies_when: Redis retries exist
  evidence_patterns:
  - Retry.backoff
  - retryWhen
  - reconnect
  - RedisCommandTimeoutException
  finding_when: retry is unbounded, repeats terminal errors, exceeds deadlines, or
    repeats a non-idempotent compound operation unsafely
  emit_on_failure: true
- id: REDIS-008
  title: Circuit breaking and bulkheading protect application resources
  severity: high
  category: resilience
  applies_when: Redis is on a high-volume path
  evidence_patterns:
  - CircuitBreaker
  - Bulkhead
  - semaphore
  - connection pool
  - boundedElastic
  finding_when: Redis degradation can exhaust request threads, event loops, connections,
    or shared executors
  emit_on_failure: true
- id: REDIS-009
  title: Cache loading coalesces concurrent misses
  severity: high
  category: cache-stampede
  applies_when: cache miss loads remote or expensive data
  evidence_patterns:
  - Cacheable
  - sync=true
  - single-flight
  - Mono.cache
  - SETNX
  finding_when: cold start, eviction, or expiration causes concurrent callers to fan
    out to the authoritative dependency
  emit_on_failure: true
- id: REDIS-010
  title: Refresh and warm-up are protected during dependency degradation
  severity: high
  category: cache-stampede
  applies_when: refresh, warm-up, or preload exists
  evidence_patterns:
  - warmup
  - preload
  - refreshAfterWrite
  - scheduler
  - CircuitBreaker
  finding_when: refresh or warm-up repeatedly fans out to a failing dependency or
    every pod/region performs the same load simultaneously
  emit_on_failure: true
- id: REDIS-011
  title: TTL and expiration semantics are externally configurable and justified
  severity: high
  category: cache-lifecycle
  applies_when: cached entries expire
  evidence_patterns:
  - TTL
  - Duration.of
  - expire
  - entryTtl
  - timeToLive
  finding_when: TTL or expiration is a hardcoded operational literal, absent for bounded
    data, or inconsistent with business freshness and recovery requirements
  emit_on_failure: true
- id: REDIS-012
  title: Cache size, value size, and serialization are bounded
  severity: high
  category: capacity
  applies_when: application controls cache population or value model
  evidence_patterns:
  - maxmemory
  - value size
  - serializer
  - RedisSerializer
  - Jackson2JsonRedisSerializer
  finding_when: unbounded key/value growth, oversized values, or unsafe serialization
    can cause latency, eviction, memory, or compatibility failures
  emit_on_failure: true
- id: REDIS-013
  title: Null, empty, negative, and stale-value semantics are explicit
  severity: critical
  category: data-correctness
  applies_when: cache can contain absence or stale data
  evidence_patterns:
  - nullValue
  - unless
  - '#result == null'
  - negative cache
  - last known good
  finding_when: a dependency failure is cached as absence/success, null causes unsafe
    processing, or stale data is used without a bounded safety policy
  emit_on_failure: true
- id: REDIS-014
  title: Last-known-good cache use is bounded and safe
  severity: critical
  category: degraded-mode
  applies_when: stale cache values may be served
  evidence_patterns:
  - last known good
  - stale-if-error
  - expiresAt
  - grace period
  finding_when: stale values can be used indefinitely, beyond security or business
    validity, or without alerting
  emit_on_failure: true
- id: REDIS-015
  title: Invalidation and write ordering preserve correctness
  severity: critical
  category: consistency
  applies_when: cache is updated around durable writes
  evidence_patterns:
  - evict
  - put
  - delete
  - transaction commit
  - afterCommit
  finding_when: cache is updated before the authoritative transaction commits, invalidation
    failure is silent, or stale data remains after a successful write
  emit_on_failure: true
- id: REDIS-016
  title: Distributed locks have ownership, fencing, and safe expiry
  severity: critical
  category: coordination
  applies_when: Redis is used for locks or leader election
  evidence_patterns:
  - SET NX PX
  - Redisson lock
  - ShedLock
  - lease owner
  - fencing token
  finding_when: a lock can expire while work continues, be released by a non-owner,
    or allow stale owners to mutate state
  emit_on_failure: true
- id: REDIS-017
  title: Sessions and security state have explicit regional consistency semantics
  severity: critical
  category: session-security
  applies_when: Redis stores session, token, authorization, or rate-limit state
  evidence_patterns:
  - Spring Session
  - session TTL
  - token cache
  - rate limiter
  - revocation
  finding_when: regional failover loses required session/security state, stale authorization
    persists, or conflicting active-region writes are unresolved
  emit_on_failure: true
- id: REDIS-018
  title: Active geo-replication conflict behavior is compatible with data structures
  severity: critical
  category: multi-region
  applies_when: active geo-replication or multi-region writes are intended
  evidence_patterns:
  - geo-replication
  - CRDT
  - conflict
  - multi-region write
  finding_when: the application assumes strong ordering, transactions, or conflict
    behavior not provided by the selected multi-region data structures
  emit_on_failure: true
- id: REDIS-019
  title: Readiness participation is topology-aware
  severity: critical
  category: health
  applies_when: Redis contributes to health
  evidence_patterns:
  - RedisHealthIndicator
  - readiness group
  - health timeout
  finding_when: Redis is blindly included or excluded from readiness, health is unbounded,
    or Redis participates in liveness
  emit_on_failure: true
- id: REDIS-020
  title: Fallback behavior is independently reliable and observable
  severity: critical
  category: fallback
  applies_when: Redis failure invokes fallback
  evidence_patterns:
  - fallback repository
  - cache-aside
  - onErrorResume
  - degraded mode
  finding_when: fallback is detached, unbounded, silent, or converts required-data
    failure to success
  emit_on_failure: true
- id: REDIS-021
  title: Sensitive data in Redis is minimized and protected
  severity: critical
  category: security
  applies_when: Redis stores customer, payment, token, session, or credential data
  evidence_patterns:
  - PAN
  - PII
  - token
  - credential
  - session
  - encryption
  finding_when: sensitive values are cached unnecessarily, logged, weakly serialized,
    over-retained, or accessible through unsafe key design
  emit_on_failure: true
- id: REDIS-022
  title: Cache keys are stable, namespaced, and versioned
  severity: high
  category: data-model
  applies_when: application constructs Redis keys
  evidence_patterns:
  - key prefix
  - namespace
  - schema version
  - tenant
  - region
  finding_when: key collisions, cross-environment contamination, incompatible schema
    reuse, or accidental region pinning can occur
  emit_on_failure: true
- id: REDIS-023
  title: Pipelining, batching, and Lua scripts preserve failure semantics
  severity: high
  category: performance-correctness
  applies_when: application uses batch, pipeline, MULTI/EXEC, or Lua
  evidence_patterns:
  - pipeline
  - executePipelined
  - MULTI
  - EXEC
  - EVAL
  finding_when: partial or per-command failures are ignored, transactions are assumed
    across unsupported boundaries, or large batches exceed time budgets
  emit_on_failure: true
- id: REDIS-024
  title: Client lifecycle and multiplexer reuse are safe
  severity: high
  category: resource-management
  applies_when: Redis clients are created
  evidence_patterns:
  - LettuceConnectionFactory
  - JedisPool
  - RedissonClient
  - singleton
  - destroy
  finding_when: clients or multiplexers are recreated per request, improperly shared
    when not thread-safe, leaked, or disposed while in use
  emit_on_failure: true
- id: REDIS-025
  title: Redis telemetry identifies saturation, latency, failures, and cache effectiveness
  severity: high
  category: observability
  applies_when: Redis is used in production paths
  evidence_patterns:
  - Micrometer
  - command latency
  - pool usage
  - hit rate
  - miss rate
  - evictions
  finding_when: operators cannot distinguish cache miss, Redis failure, timeout, saturation,
    fallback, stale use, and recovery
  emit_on_failure: true
- id: REDIS-026
  title: Business throughput remains observable during Redis degradation
  severity: high
  category: observability
  applies_when: Redis supports batch, scheduler, or critical request processing
  evidence_patterns:
  - last success
  - items processed
  - backlog age
  - zero throughput
  finding_when: Redis outage or stale cache causes business processing to stop while
    process health remains UP
  emit_on_failure: true
- id: REDIS-027
  title: Fault tests cover failover, reconnect, eviction, stampede, and stale behavior
  severity: critical
  category: testing
  applies_when: Redis is a material dependency
  evidence_patterns:
  - Toxiproxy
  - Testcontainers
  - failover test
  - connection reset
  - eviction test
  - stampede test
  finding_when: tests do not prove bounded failure, safe fallback, reconnect, topology
    refresh, eviction/miss behavior, lock safety, and post-recovery correctness
  emit_on_failure: true
---

# Azure Managed Redis Application Behavior Standard

## Purpose

This dependency-specific standard assesses how an application uses Azure Managed Redis for caching, coordination, sessions, transient work, and approved data structures in resilient regional deployments. It incorporates cache, concurrency, health, fallback, observability, and correctness themes observed across the previously reviewed service assessments.

## Scope boundary

Assess application code, Spring configuration, Redis client construction, cache semantics, locks, sessions, retries, health, telemetry, and automated tests. Do not infer deployed Redis tier, capacity, zones, active geo-replication, private endpoints, DNS, identity assignment, firewall, or regional topology from absent repository evidence.

## Evaluator workflow

- Confirm Redis is actually used by production code.
- Classify each Redis use as cache, session store, coordination/lock, transient queue/work store, rate limiter, or approved data service.
- Identify the authoritative source and rebuild/reconciliation behavior.
- Locate client construction, topology, credentials, timeout/retry, serialization, TTL, invalidation, health, telemetry, and tests.
- Evaluate only applicable controls and deduplicate with the master and HTTP/client standards.
- Use `not_assessed` for unavailable deployed topology.

## Required statuses

- `compliant`: Repository evidence demonstrates the behavior.
- `non_compliant`: Repository evidence demonstrates a gap.
- `not_assessed`: Evidence is unavailable or insufficient.
- `not_applicable`: The dependency or behavior does not apply.
- `accepted_risk`: A cited approved exception exists.

## Dependency-specific quality caveats

- Redis is not automatically disposable and is not automatically a system of record. Evaluate the declared role.
- Cache availability must not override business correctness or security validity.
- Do not add Redis blindly to readiness, and never add it to liveness.
- A feature flag or simple Redis lock is not a complete single-active guarantee.
- A retry can be unsafe for increments, queue operations, locks, transactions, scripts, and compound business work.
- Active geo-replication behavior depends on supported data structures and conflict semantics; do not assume it is enabled.
- Numeric timeout, TTL, pool, retry, lock, batch, and stale-value settings are examples unless approved and must remain configurable.
- Missing deployed configuration is `not_assessed`, not infrastructure noncompliance.

## Controls

### REDIS-001: Redis role and authoritative source are explicit

**Severity:** Critical  
**Category:** data-correctness  
**Applies when:** Redis is used

#### Requirement

The application must define whether Redis is a cache, coordination store, session store, transient work store, or approved durable data service. When Redis is a cache, an authoritative system of record and rebuild behavior must be explicit.

#### Repository evidence to inspect

- `RedisTemplate`
- `ReactiveRedisTemplate`
- `RedisCacheManager`
- `source of truth`
- `system of record`

#### Finding condition

Emit a finding when evidence shows that business correctness or durable recovery depends on Redis without an explicit authoritative source and recovery contract.

#### Evidence rule

Cite repository-relative path, symbol or property, original assessed line range, and exact excerpt when available. Evaluate effective runtime behavior rather than the presence of a client, annotation, property, or default alone. If evidence is unavailable or external, return `not_assessed`.

#### Quality caveats

- Do not assume Redis is always disposable; evaluate its declared role.
- Do not recommend Redis as the system of record merely to improve availability.

---

### REDIS-002: Cache residency is not required for correctness

**Severity:** Critical  
**Category:** data-correctness  
**Applies when:** Redis is used as a cache

#### Requirement

A missing cache entry must cause a safe authoritative lookup, explicit degraded response, or bounded recovery path. Cache residency must not be the only copy of required business state.

#### Repository evidence to inspect

- `cache miss`
- `fallback loader`
- `authoritative repository`
- `null cache value`

#### Finding condition

Emit a finding when evidence shows that cache miss, eviction, restart, or regional failover causes incorrect authorization, pricing, transaction, or workflow behavior.

#### Evidence rule

Cite repository-relative path, symbol or property, original assessed line range, and exact excerpt when available. Evaluate effective runtime behavior rather than the presence of a client, annotation, property, or default alone. If evidence is unavailable or external, return `not_assessed`.

#### Quality caveats

- A cached value may affect performance without being required for correctness. Distinguish the two.

---

### REDIS-003: Redis endpoint and region selection are externally configured

**Severity:** Critical  
**Category:** configuration  
**Applies when:** Redis client exists

#### Requirement

Connection endpoints and topology inputs must be deployment-injected and allow the same artifact to use the approved local regional Redis service.

#### Repository evidence to inspect

- `spring.data.redis.host`
- `spring.data.redis.url`
- `RedisURI`
- `RedisStandaloneConfiguration`
- `RedisClusterConfiguration`

#### Finding condition

Emit a finding when evidence shows that a physical regional endpoint, port, database, or topology is hardcoded or a remote region is the normal endpoint without an explicit policy.

#### Evidence rule

Cite repository-relative path, symbol or property, original assessed line range, and exact excerpt when available. Evaluate effective runtime behavior rather than the presence of a client, annotation, property, or default alone. If evidence is unavailable or external, return `not_assessed`.

#### Quality caveats

- Do not infer deployed geo-replication, DNS, private endpoints, or regional instances from repository absence.

---

### REDIS-004: Authentication and TLS use approved external identity and secret delivery

**Severity:** Critical  
**Category:** security  
**Applies when:** Redis authentication is used

#### Requirement

Authentication material must be externally supplied through approved identity or secret delivery, protected from logs, and used with TLS and certificate validation.

#### Repository evidence to inspect

- `password`
- `username`
- `SSL`
- `TLS`
- `DefaultAzureCredential`
- `Entra ID`

#### Finding condition

Emit a finding when evidence shows that credentials are committed, embedded, logged, or TLS verification is disabled.

#### Evidence rule

Cite repository-relative path, symbol or property, original assessed line range, and exact excerpt when available. Evaluate effective runtime behavior rather than the presence of a client, annotation, property, or default alone. If evidence is unavailable or external, return `not_assessed`.

#### Quality caveats

- Do not prescribe password authentication when supported identity-based access is approved.

---

### REDIS-005: Connection establishment and commands are bounded

**Severity:** Critical  
**Category:** resilience  
**Applies when:** Redis client exists

#### Requirement

Redis connection establishment, acquisition, command execution, and the complete operation must have externally configurable bounds coordinated with caller deadlines.

#### Repository evidence to inspect

- `connectTimeout`
- `commandTimeout`
- `timeout`
- `LettuceClientConfiguration`
- `JedisPoolConfig`

#### Finding condition

Emit a finding when evidence shows that connection, pool acquisition, command, topology refresh, or complete cache operation can exceed the request or workload budget.

#### Evidence rule

Cite repository-relative path, symbol or property, original assessed line range, and exact excerpt when available. Evaluate effective runtime behavior rather than the presence of a client, annotation, property, or default alone. If evidence is unavailable or external, return `not_assessed`.

#### Quality caveats

- Do not prescribe numeric settings without workload evidence.
- A socket timeout alone does not prove pool acquisition and the complete operation are bounded.

---

### REDIS-006: Clients and connections recover after failover without restart

**Severity:** Critical  
**Category:** recovery  
**Applies when:** Redis client exists

#### Requirement

Clients must reconnect, refresh topology when applicable, discard invalid connections, and resume successful operations after failover or patching without restart.

#### Repository evidence to inspect

- `autoReconnect`
- `ClusterTopologyRefreshOptions`
- `validateConnection`
- `reconnect`
- `refreshPeriod`

#### Finding condition

Emit a finding when evidence shows that closed or stale connections persist after failover and application recovery requires a pod/process restart.

#### Evidence rule

Cite repository-relative path, symbol or property, original assessed line range, and exact excerpt when available. Evaluate effective runtime behavior rather than the presence of a client, annotation, property, or default alone. If evidence is unavailable or external, return `not_assessed`.

#### Quality caveats

- Failover can close existing connections; the application must tolerate transient disconnects.
- Do not infer the managed service failover topology from code.

---

### REDIS-007: Retry is bounded and safe for the command semantics

**Severity:** High  
**Category:** resilience  
**Applies when:** Redis retries exist

#### Requirement

Retry only classified transient connection or command failures, cap attempts and total duration, and ensure replay is safe for the actual Redis command and surrounding business operation.

#### Repository evidence to inspect

- `Retry.backoff`
- `retryWhen`
- `reconnect`
- `RedisCommandTimeoutException`

#### Finding condition

Emit a finding when evidence shows that retry is unbounded, repeats terminal errors, exceeds deadlines, or repeats a non-idempotent compound operation unsafely.

#### Evidence rule

Cite repository-relative path, symbol or property, original assessed line range, and exact excerpt when available. Evaluate effective runtime behavior rather than the presence of a client, annotation, property, or default alone. If evidence is unavailable or external, return `not_assessed`.

#### Quality caveats

- An increment, queue operation, lock acquisition, or multi-step sequence may not be safe to replay blindly.

---

### REDIS-008: Circuit breaking and bulkheading protect application resources

**Severity:** High  
**Category:** resilience  
**Applies when:** Redis is on a high-volume path

#### Requirement

Bound Redis concurrency and isolate failures so slow or unavailable Redis does not consume all application capacity.

#### Repository evidence to inspect

- `CircuitBreaker`
- `Bulkhead`
- `semaphore`
- `connection pool`
- `boundedElastic`

#### Finding condition

Emit a finding when evidence shows that Redis degradation can exhaust request threads, event loops, connections, or shared executors.

#### Evidence rule

Cite repository-relative path, symbol or property, original assessed line range, and exact excerpt when available. Evaluate effective runtime behavior rather than the presence of a client, annotation, property, or default alone. If evidence is unavailable or external, return `not_assessed`.

#### Quality caveats

- Do not place blocking clients on Reactor event loops.

---

### REDIS-009: Cache loading coalesces concurrent misses

**Severity:** High  
**Category:** cache-stampede  
**Applies when:** cache miss loads remote or expensive data

#### Requirement

Use request coalescing, single-flight loading, or an equivalent bounded mechanism for expensive cache fills.

#### Repository evidence to inspect

- `Cacheable`
- `sync=true`
- `single-flight`
- `Mono.cache`
- `SETNX`

#### Finding condition

Emit a finding when evidence shows that cold start, eviction, or expiration causes concurrent callers to fan out to the authoritative dependency.

#### Evidence rule

Cite repository-relative path, symbol or property, original assessed line range, and exact excerpt when available. Evaluate effective runtime behavior rather than the presence of a client, annotation, property, or default alone. If evidence is unavailable or external, return `not_assessed`.

#### Quality caveats

- Distributed locking is not always required; use the least complex safe coalescing scope.

---

### REDIS-010: Refresh and warm-up are protected during dependency degradation

**Severity:** High  
**Category:** cache-stampede  
**Applies when:** refresh, warm-up, or preload exists

#### Requirement

Warm-up and refresh must be bounded, observable, coordinated where needed, and protected by dependency resilience policies.

#### Repository evidence to inspect

- `warmup`
- `preload`
- `refreshAfterWrite`
- `scheduler`
- `CircuitBreaker`

#### Finding condition

Emit a finding when evidence shows that refresh or warm-up repeatedly fans out to a failing dependency or every pod/region performs the same load simultaneously.

#### Evidence rule

Cite repository-relative path, symbol or property, original assessed line range, and exact excerpt when available. Evaluate effective runtime behavior rather than the presence of a client, annotation, property, or default alone. If evidence is unavailable or external, return `not_assessed`.

#### Quality caveats

- A startup warm-up must not create an uncontrolled regional thundering herd.

---

### REDIS-011: TTL and expiration semantics are externally configurable and justified

**Severity:** High  
**Category:** cache-lifecycle  
**Applies when:** cached entries expire

#### Requirement

TTL and expiration behavior must be externally configurable or explicitly documented as an immutable invariant and validated against data freshness and load requirements.

#### Repository evidence to inspect

- `TTL`
- `Duration.of`
- `expire`
- `entryTtl`
- `timeToLive`

#### Finding condition

Emit a finding when evidence shows that TTL or expiration is a hardcoded operational literal, absent for bounded data, or inconsistent with business freshness and recovery requirements.

#### Evidence rule

Cite repository-relative path, symbol or property, original assessed line range, and exact excerpt when available. Evaluate effective runtime behavior rather than the presence of a client, annotation, property, or default alone. If evidence is unavailable or external, return `not_assessed`.

#### Quality caveats

- A TTL is not a substitute for explicit invalidation when correctness requires immediate change.

---

### REDIS-012: Cache size, value size, and serialization are bounded

**Severity:** High  
**Category:** capacity  
**Applies when:** application controls cache population or value model

#### Requirement

The application must bound key cardinality and value size, choose a compatible serializer, and avoid monolithic values that cause head-of-line blocking or excessive transfer.

#### Repository evidence to inspect

- `maxmemory`
- `value size`
- `serializer`
- `RedisSerializer`
- `Jackson2JsonRedisSerializer`

#### Finding condition

Emit a finding when evidence shows that unbounded key/value growth, oversized values, or unsafe serialization can cause latency, eviction, memory, or compatibility failures.

#### Evidence rule

Cite repository-relative path, symbol or property, original assessed line range, and exact excerpt when available. Evaluate effective runtime behavior rather than the presence of a client, annotation, property, or default alone. If evidence is unavailable or external, return `not_assessed`.

#### Quality caveats

- Smaller values and pipelining may improve efficiency, but recommendations require workload evidence.

---

### REDIS-013: Null, empty, negative, and stale-value semantics are explicit

**Severity:** Critical  
**Category:** data-correctness  
**Applies when:** cache can contain absence or stale data

#### Requirement

Define behavior for misses, legitimate absence, dependency failure, negative caching, and stale values. Required data failure must not silently become null, empty, zero, or success.

#### Repository evidence to inspect

- `nullValue`
- `unless`
- `#result == null`
- `negative cache`
- `last known good`

#### Finding condition

Emit a finding when evidence shows that a dependency failure is cached as absence/success, null causes unsafe processing, or stale data is used without a bounded safety policy.

#### Evidence rule

Cite repository-relative path, symbol or property, original assessed line range, and exact excerpt when available. Evaluate effective runtime behavior rather than the presence of a client, annotation, property, or default alone. If evidence is unavailable or external, return `not_assessed`.

#### Quality caveats

- Do not conflate a legitimate not-found result with a failed cache loader.

---

### REDIS-014: Last-known-good cache use is bounded and safe

**Severity:** Critical  
**Category:** degraded-mode  
**Applies when:** stale cache values may be served

#### Requirement

Last-known-good use must have an approved maximum stale interval, validity checks, explicit degraded-state telemetry, and fail-closed behavior where safety requires it.

#### Repository evidence to inspect

- `last known good`
- `stale-if-error`
- `expiresAt`
- `grace period`

#### Finding condition

Emit a finding when evidence shows that stale values can be used indefinitely, beyond security or business validity, or without alerting.

#### Evidence rule

Cite repository-relative path, symbol or property, original assessed line range, and exact excerpt when available. Evaluate effective runtime behavior rather than the presence of a client, annotation, property, or default alone. If evidence is unavailable or external, return `not_assessed`.

#### Quality caveats

- Never extend credentials, authorization, certificates, or security-sensitive values beyond validity.

---

### REDIS-015: Invalidation and write ordering preserve correctness

**Severity:** Critical  
**Category:** consistency  
**Applies when:** cache is updated around durable writes

#### Requirement

Cache update or invalidation must align with authoritative commit, define failure handling, and prevent stale values from overwriting newer state.

#### Repository evidence to inspect

- `evict`
- `put`
- `delete`
- `transaction commit`
- `afterCommit`

#### Finding condition

Emit a finding when evidence shows that cache is updated before the authoritative transaction commits, invalidation failure is silent, or stale data remains after a successful write.

#### Evidence rule

Cite repository-relative path, symbol or property, original assessed line range, and exact excerpt when available. Evaluate effective runtime behavior rather than the presence of a client, annotation, property, or default alone. If evidence is unavailable or external, return `not_assessed`.

#### Quality caveats

- A database transaction usually cannot atomically include Redis. Use after-commit actions, versioning, events, or reconciliation.

---

### REDIS-016: Distributed locks have ownership, fencing, and safe expiry

**Severity:** Critical  
**Category:** coordination  
**Applies when:** Redis is used for locks or leader election

#### Requirement

Locks must use unique ownership, atomic acquire/release, bounded lease, renewal policy, and fencing or authoritative conditional writes when stale owners can cause harm.

#### Repository evidence to inspect

- `SET NX PX`
- `Redisson lock`
- `ShedLock`
- `lease owner`
- `fencing token`

#### Finding condition

Emit a finding when evidence shows that a lock can expire while work continues, be released by a non-owner, or allow stale owners to mutate state.

#### Evidence rule

Cite repository-relative path, symbol or property, original assessed line range, and exact excerpt when available. Evaluate effective runtime behavior rather than the presence of a client, annotation, property, or default alone. If evidence is unavailable or external, return `not_assessed`.

#### Quality caveats

- A feature flag or SETNX alone is not a complete distributed ownership guarantee.
- Do not use Redis locks as a substitute for idempotency.

---

### REDIS-017: Sessions and security state have explicit regional consistency semantics

**Severity:** Critical  
**Category:** session-security  
**Applies when:** Redis stores session, token, authorization, or rate-limit state

#### Requirement

Define regional read/write, replication, revocation, failover, and expiration semantics for session and security state.

#### Repository evidence to inspect

- `Spring Session`
- `session TTL`
- `token cache`
- `rate limiter`
- `revocation`

#### Finding condition

Emit a finding when evidence shows that regional failover loses required session/security state, stale authorization persists, or conflicting active-region writes are unresolved.

#### Evidence rule

Cite repository-relative path, symbol or property, original assessed line range, and exact excerpt when available. Evaluate effective runtime behavior rather than the presence of a client, annotation, property, or default alone. If evidence is unavailable or external, return `not_assessed`.

#### Quality caveats

- Evaluate the managed service topology as external evidence when it is not repository-owned.

---

### REDIS-018: Active geo-replication conflict behavior is compatible with data structures

**Severity:** Critical  
**Category:** multi-region  
**Applies when:** active geo-replication or multi-region writes are intended

#### Requirement

Use only supported data types and operation semantics for multi-region writes and document conflict, convergence, and ordering expectations.

#### Repository evidence to inspect

- `geo-replication`
- `CRDT`
- `conflict`
- `multi-region write`

#### Finding condition

Emit a finding when evidence shows that the application assumes strong ordering, transactions, or conflict behavior not provided by the selected multi-region data structures.

#### Evidence rule

Cite repository-relative path, symbol or property, original assessed line range, and exact excerpt when available. Evaluate effective runtime behavior rather than the presence of a client, annotation, property, or default alone. If evidence is unavailable or external, return `not_assessed`.

#### Quality caveats

- Do not infer active geo-replication is enabled from client code.
- Do not prescribe geo-replication when the application only needs independently rebuildable regional caches.

---

### REDIS-019: Readiness participation is topology-aware

**Severity:** Critical  
**Category:** health  
**Applies when:** Redis contributes to health

#### Requirement

Redis may gate readiness only when the application cannot safely serve without the region-local Redis capability and no safe authoritative fallback exists. Health must be bounded and never included in liveness.

#### Repository evidence to inspect

- `RedisHealthIndicator`
- `readiness group`
- `health timeout`

#### Finding condition

Emit a finding when evidence shows that Redis is blindly included or excluded from readiness, health is unbounded, or Redis participates in liveness.

#### Evidence rule

Cite repository-relative path, symbol or property, original assessed line range, and exact excerpt when available. Evaluate effective runtime behavior rather than the presence of a client, annotation, property, or default alone. If evidence is unavailable or external, return `not_assessed`.

#### Quality caveats

- A shared global Redis dependency in readiness can drain all regions simultaneously.

---

### REDIS-020: Fallback behavior is independently reliable and observable

**Severity:** Critical  
**Category:** fallback  
**Applies when:** Redis failure invokes fallback

#### Requirement

Measure primary failure, fallback success, and dual failure separately. Preserve durable intent when returning accepted or synthetic success.

#### Repository evidence to inspect

- `fallback repository`
- `cache-aside`
- `onErrorResume`
- `degraded mode`

#### Finding condition

Emit a finding when evidence shows that fallback is detached, unbounded, silent, or converts required-data failure to success.

#### Evidence rule

Cite repository-relative path, symbol or property, original assessed line range, and exact excerpt when available. Evaluate effective runtime behavior rather than the presence of a client, annotation, property, or default alone. If evidence is unavailable or external, return `not_assessed`.

#### Quality caveats

- A fallback to the system of record can overload it during cache outage; apply bulkheads and load protection.

---

### REDIS-021: Sensitive data in Redis is minimized and protected

**Severity:** Critical  
**Category:** security  
**Applies when:** Redis stores customer, payment, token, session, or credential data

#### Requirement

Minimize sensitive cache content, use approved protection and TTL, avoid secrets in keys, sanitize diagnostics, and define deletion and revocation behavior.

#### Repository evidence to inspect

- `PAN`
- `PII`
- `token`
- `credential`
- `session`
- `encryption`

#### Finding condition

Emit a finding when evidence shows that sensitive values are cached unnecessarily, logged, weakly serialized, over-retained, or accessible through unsafe key design.

#### Evidence rule

Cite repository-relative path, symbol or property, original assessed line range, and exact excerpt when available. Evaluate effective runtime behavior rather than the presence of a client, annotation, property, or default alone. If evidence is unavailable or external, return `not_assessed`.

#### Quality caveats

- Do not place secret values, PAN, or PII in metric labels, Redis keys, or logs.

---

### REDIS-022: Cache keys are stable, namespaced, and versioned

**Severity:** High  
**Category:** data-model  
**Applies when:** application constructs Redis keys

#### Requirement

Keys must include stable namespace and schema version, avoid sensitive values, and use business identity rather than physical region unless regional isolation is intentional.

#### Repository evidence to inspect

- `key prefix`
- `namespace`
- `schema version`
- `tenant`
- `region`

#### Finding condition

Emit a finding when evidence shows that key collisions, cross-environment contamination, incompatible schema reuse, or accidental region pinning can occur.

#### Evidence rule

Cite repository-relative path, symbol or property, original assessed line range, and exact excerpt when available. Evaluate effective runtime behavior rather than the presence of a client, annotation, property, or default alone. If evidence is unavailable or external, return `not_assessed`.

#### Quality caveats

- A region suffix can prevent portability and create stale durable references; justify it explicitly.

---

### REDIS-023: Pipelining, batching, and Lua scripts preserve failure semantics

**Severity:** High  
**Category:** performance-correctness  
**Applies when:** application uses batch, pipeline, MULTI/EXEC, or Lua

#### Requirement

Inspect individual command results, bound batch size, and define atomicity and retry behavior for pipelines, transactions, and scripts.

#### Repository evidence to inspect

- `pipeline`
- `executePipelined`
- `MULTI`
- `EXEC`
- `EVAL`

#### Finding condition

Emit a finding when evidence shows that partial or per-command failures are ignored, transactions are assumed across unsupported boundaries, or large batches exceed time budgets.

#### Evidence rule

Cite repository-relative path, symbol or property, original assessed line range, and exact excerpt when available. Evaluate effective runtime behavior rather than the presence of a client, annotation, property, or default alone. If evidence is unavailable or external, return `not_assessed`.

#### Quality caveats

- Redis transaction semantics do not extend to external stores or providers.

---

### REDIS-024: Client lifecycle and multiplexer reuse are safe

**Severity:** High  
**Category:** resource-management  
**Applies when:** Redis clients are created

#### Requirement

Reuse supported thread-safe clients and connection resources, configure lifecycle and shutdown, and isolate materially different workloads when needed.

#### Repository evidence to inspect

- `LettuceConnectionFactory`
- `JedisPool`
- `RedissonClient`
- `singleton`
- `destroy`

#### Finding condition

Emit a finding when evidence shows that clients or multiplexers are recreated per request, improperly shared when not thread-safe, leaked, or disposed while in use.

#### Evidence rule

Cite repository-relative path, symbol or property, original assessed line range, and exact excerpt when available. Evaluate effective runtime behavior rather than the presence of a client, annotation, property, or default alone. If evidence is unavailable or external, return `not_assessed`.

#### Quality caveats

- Follow the selected client library lifecycle contract.

---

### REDIS-025: Redis telemetry identifies saturation, latency, failures, and cache effectiveness

**Severity:** High  
**Category:** observability  
**Applies when:** Redis is used in production paths

#### Requirement

Emit safe metrics and traces for command latency/errors, connection state, pool saturation, hit/miss, eviction, fallback, stale use, lock contention, and recovery, tagged with application and region.

#### Repository evidence to inspect

- `Micrometer`
- `command latency`
- `pool usage`
- `hit rate`
- `miss rate`
- `evictions`

#### Finding condition

Emit a finding when evidence shows that operators cannot distinguish cache miss, Redis failure, timeout, saturation, fallback, stale use, and recovery.

#### Evidence rule

Cite repository-relative path, symbol or property, original assessed line range, and exact excerpt when available. Evaluate effective runtime behavior rather than the presence of a client, annotation, property, or default alone. If evidence is unavailable or external, return `not_assessed`.

#### Quality caveats

- Avoid key names, values, and unbounded-cardinality tags.

---

### REDIS-026: Business throughput remains observable during Redis degradation

**Severity:** High  
**Category:** observability  
**Applies when:** Redis supports batch, scheduler, or critical request processing

#### Requirement

Track business success, backlog, degraded operation, and recovery in addition to Redis technical health.

#### Repository evidence to inspect

- `last success`
- `items processed`
- `backlog age`
- `zero throughput`

#### Finding condition

Emit a finding when evidence shows that Redis outage or stale cache causes business processing to stop while process health remains UP.

#### Evidence rule

Cite repository-relative path, symbol or property, original assessed line range, and exact excerpt when available. Evaluate effective runtime behavior rather than the presence of a client, annotation, property, or default alone. If evidence is unavailable or external, return `not_assessed`.

#### Quality caveats

- Technical Redis health does not prove business correctness.

---

### REDIS-027: Fault tests cover failover, reconnect, eviction, stampede, and stale behavior

**Severity:** Critical  
**Category:** testing  
**Applies when:** Redis is a material dependency

#### Requirement

Use automated or repeatable tests for disconnects, failover, patch-like connection closure, latency, saturation, cache loss, concurrent misses, stale values, lock expiry, and recovery without restart.

#### Repository evidence to inspect

- `Toxiproxy`
- `Testcontainers`
- `failover test`
- `connection reset`
- `eviction test`
- `stampede test`

#### Finding condition

Emit a finding when evidence shows that tests do not prove bounded failure, safe fallback, reconnect, topology refresh, eviction/miss behavior, lock safety, and post-recovery correctness.

#### Evidence rule

Cite repository-relative path, symbol or property, original assessed line range, and exact excerpt when available. Evaluate effective runtime behavior rather than the presence of a client, annotation, property, or default alone. If evidence is unavailable or external, return `not_assessed`.

#### Quality caveats

- Mock-only tests do not prove socket, client, pool, or failover behavior.

---

## Standard finding format

- **Title:** [specific Redis behavior gap]
- **Control:** [REDIS-NNN]
- **Related controls:** [control IDs]
- **Severity:** [severity]
- **Redis role:** [cache/session/lock/etc.]
- **Repository evidence:** [path, symbol/property, original lines, excerpt]
- **Observed behavior:** [effective behavior]
- **Regional or operational risk:** [impact]
- **Required code/configuration change:** [remediation]
- **Validation test:** [test proving behavior]
- **Confidence:** [high/medium/low]

## Non-findings

- Missing Azure Managed Redis instance, regional instance, zone redundancy, active geo-replication, private endpoint, DNS, firewall, identity assignment, or capacity when deployed evidence is unavailable.
- Missing infrastructure deployment or migration work.
- Azure Cache for Redis retirement or migration unless migration assessment is explicitly requested.
- PCF migration, modernization, cleanup, or findings.
