---
schema_version: 3.0.0
document_type: master_application_behavior
service: springboot_aks_active_active
service_name: Spring Boot on AKS Active-Active Code Assessment
version: 3.0.0
last_updated: '2026-08-27'
language: java
framework: spring-boot
runtime_platform: aks
assessment_scope: application_code_only
lifecycle_status: active
source_reviewed:
- 08-27-2026-OSLM-3p-lmfeatureservice-Code-Level-Resiliency-Assessment-final.md
- 08-26-2026-OSLM-cacheservice-Code-Level-Resiliency-Assessment-final.md
- 08-25-2026-OSLM-3p-eventconsumer-Code-Level-Resiliency-Assessment-final.md
- 08-25-2026.oslm-3p-eventdataservice-Code-Level-Resiliency-Assessment-final.md
- 08.26.2026-oslm-3p-uberclient-Code-Level-Resiliency-Assessment-final.md
infrastructure_assumptions:
- Two Azure regions and required shared services are provisioned according to approved
  architecture.
- Regional endpoints and identity/network controls are supplied by deployment configuration.
excluded_from_findings:
- regional deployment jobs and Actionsfile parity
- shared workflow catalog compatibility
- ACR geo-replication and Azure resource topology
- private endpoints, DNS, capacity, zones, and platform configuration
- PCF migration, modernization, cleanup, or findings
assessment:
  enabled: true
  emit_findings: true
  include_in_score: true
  unknown_evidence_status: not_assessed
controls:
- id: APP-AA-001
  title: One immutable artifact supports both regions
  severity: high
  category: deployability
  scope: code
  applies_when: always
  evidence_patterns:
  - profiles
  - artifact
  - Dockerfile
  finding_when: region-specific code or artifact is required
  unknown_evidence_status: not_assessed
  emit_on_failure: true
- id: APP-AA-002
  title: Regional endpoints are externally configured
  severity: critical
  category: configuration
  scope: code
  applies_when: remote dependencies exist
  evidence_patterns:
  - application.yml
  - '@ConfigurationProperties'
  - baseUrl
  finding_when: regional endpoint or hostname is hardcoded
  unknown_evidence_status: not_assessed
  emit_on_failure: true
- id: APP-AA-003
  title: Local-region dependency affinity is explicit
  severity: critical
  category: regional-affinity
  scope: code
  applies_when: regional dependencies exist
  evidence_patterns:
  - region property
  - endpoint mapping
  finding_when: normal operation can use a remote-region dependency
  unknown_evidence_status: not_assessed
  emit_on_failure: true
- id: APP-AA-004
  title: Dependency calls have bounded timeouts
  severity: critical
  category: resilience
  scope: code
  applies_when: remote calls exist
  evidence_patterns:
  - connect timeout
  - response timeout
  - .timeout(
  - query timeout
  finding_when: remote call can exceed the failure budget
  unknown_evidence_status: not_assessed
  emit_on_failure: true
- id: APP-AA-005
  title: Transient failures use bounded retry with backoff
  severity: high
  category: resilience
  scope: code
  applies_when: retryable calls exist
  evidence_patterns:
  - Retry.backoff
  - '@Retryable'
  - RetryOptions
  finding_when: retry is absent, unbounded, or applies to terminal errors
  unknown_evidence_status: not_assessed
  emit_on_failure: true
- id: APP-AA-006
  title: Repeated failures are isolated
  severity: high
  category: resilience
  scope: code
  applies_when: remote calls exist
  evidence_patterns:
  - CircuitBreaker
  - Bulkhead
  - connection pool
  finding_when: one dependency can exhaust shared resources
  unknown_evidence_status: not_assessed
  emit_on_failure: true
- id: APP-AA-007
  title: Critical dependency failure affects readiness
  severity: critical
  category: health
  scope: code
  applies_when: critical regional dependency exists
  evidence_patterns:
  - HealthIndicator
  - readiness group
  finding_when: critical dependency remains failed while readiness is UP
  unknown_evidence_status: not_assessed
  emit_on_failure: true
- id: APP-AA-008
  title: Liveness excludes external dependencies
  severity: critical
  category: health
  scope: code
  applies_when: Actuator probes exist
  evidence_patterns:
  - liveness group
  - livenessState
  finding_when: external failure causes liveness failure or restart loops
  unknown_evidence_status: not_assessed
  emit_on_failure: true
- id: APP-AA-009
  title: Health checks are bounded and representative
  severity: high
  category: health
  scope: code
  applies_when: health contributors exist
  evidence_patterns:
  - health timeout
  - synthetic check
  finding_when: health can hang, overload a dependency, or bypass the serving path
  unknown_evidence_status: not_assessed
  emit_on_failure: true
- id: APP-AA-010
  title: Application state is region independent
  severity: critical
  category: state
  scope: code
  applies_when: stateful behavior exists
  evidence_patterns:
  - session
  - local file
  - in-memory state
  finding_when: required state is pod-local or region-local
  unknown_evidence_status: not_assessed
  emit_on_failure: true
- id: APP-AA-011
  title: Mutating operations are idempotent
  severity: critical
  category: consistency
  scope: code
  applies_when: mutating operations exist
  evidence_patterns:
  - idempotency key
  - dedupe
  - unique index
  finding_when: retry or replay can duplicate business effects
  unknown_evidence_status: not_assessed
  emit_on_failure: true
- id: APP-AA-012
  title: Concurrency and conflict behavior is defined
  severity: high
  category: consistency
  scope: code
  applies_when: concurrent writes are possible
  evidence_patterns:
  - '@Version'
  - ETag
  - rowversion
  finding_when: concurrent writes can silently overwrite state
  unknown_evidence_status: not_assessed
  emit_on_failure: true
- id: APP-AA-013
  title: Startup tolerates temporary dependency unavailability
  severity: high
  category: startup
  scope: code
  applies_when: startup dependencies exist
  evidence_patterns:
  - fail-fast
  - startup retry
  - readiness
  finding_when: temporary outage causes uncontrolled startup failure
  unknown_evidence_status: not_assessed
  emit_on_failure: true
- id: APP-AA-014
  title: Dependency recovery occurs without restart
  severity: high
  category: recovery
  scope: code
  applies_when: remote clients exist
  evidence_patterns:
  - reconnect
  - credential refresh
  - half-open
  finding_when: recovery requires process restart
  unknown_evidence_status: not_assessed
  emit_on_failure: true
- id: APP-AA-015
  title: Regional identity is present in telemetry
  severity: medium
  category: observability
  scope: code
  applies_when: telemetry exists
  evidence_patterns:
  - region tag
  - cluster tag
  finding_when: telemetry cannot identify serving region
  unknown_evidence_status: not_assessed
  emit_on_failure: true
- id: APP-AA-016
  title: Failures generate actionable signals
  severity: critical
  category: observability
  scope: code
  applies_when: critical dependencies exist
  evidence_patterns:
  - metrics
  - structured logs
  - retry exhausted
  finding_when: critical failure or recovery is not observable
  unknown_evidence_status: not_assessed
  emit_on_failure: true
- id: APP-AA-017
  title: Graceful shutdown and traffic draining are implemented
  severity: high
  category: lifecycle
  scope: code
  applies_when: service receives traffic or processes work
  evidence_patterns:
  - graceful shutdown
  - readiness transition
  finding_when: termination accepts new work or loses in-flight work
  unknown_evidence_status: not_assessed
  emit_on_failure: true
- id: APP-AA-018
  title: Active-active failure behavior is tested
  severity: critical
  category: testing
  scope: code
  applies_when: always
  evidence_patterns:
  - fault test
  - integration test
  finding_when: tests do not prove failure and recovery behavior
  unknown_evidence_status: not_assessed
  emit_on_failure: true
- id: APP-DISC-001
  title: Discovery endpoint and regional selection are configurable
  severity: critical
  category: service-discovery
  scope: code
  applies_when: DiscoveryClient is used
  evidence_patterns:
  - '@EnableDiscoveryClient'
  - registry endpoint
  finding_when: discovery endpoint or region is hardcoded
  unknown_evidence_status: not_assessed
  emit_on_failure: true
- id: APP-DISC-002
  title: Critical discovery state participates in readiness
  severity: high
  category: service-discovery
  scope: code
  applies_when: discovery is critical
  evidence_patterns:
  - DiscoveryClientHealthIndicator
  - readiness
  finding_when: critical registration or lookup failure leaves readiness UP
  unknown_evidence_status: not_assessed
  emit_on_failure: true
- id: APP-CONF-010
  title: Runtime refresh behavior is defined and safe
  severity: high
  category: configuration
  scope: code
  applies_when: dynamic refresh is enabled or expected
  evidence_patterns:
  - '@RefreshScope'
  - EnvironmentChangeEvent
  finding_when: refreshed values do not safely affect initialized clients, pools,
    executors, or caches
  unknown_evidence_status: not_assessed
  emit_on_failure: true
- id: APP-REACT-001
  title: Reactive side effects execute once
  severity: critical
  category: reactive
  scope: code
  applies_when: Reactor side effects exist
  evidence_patterns:
  - Mono.defer
  - cache()
  - subscribe
  finding_when: a cold publisher can be subscribed more than once and repeat a side
    effect
  unknown_evidence_status: not_assessed
  emit_on_failure: true
- id: APP-REACT-002
  title: Reactive business chains avoid detached subscriptions
  severity: critical
  category: reactive
  scope: code
  applies_when: Reactor is used
  evidence_patterns:
  - .subscribe()
  - void service method
  finding_when: business work is detached from caller-visible completion or error
  unknown_evidence_status: not_assessed
  emit_on_failure: true
- id: APP-REACT-003
  title: Reactive error handling preserves failure semantics
  severity: high
  category: reactive
  scope: code
  applies_when: Reactor is used
  evidence_patterns:
  - onErrorResume
  - switchIfEmpty
  finding_when: dependency failures become empty, not-found, or success
  unknown_evidence_status: not_assessed
  emit_on_failure: true
- id: APP-CACHE-001
  title: Cache TTL and refresh intervals are configurable
  severity: medium
  category: cache
  scope: code
  applies_when: application cache exists
  evidence_patterns:
  - expireAfterWrite
  - refreshAfterWrite
  finding_when: TTL or refresh is an unexplained code literal
  unknown_evidence_status: not_assessed
  emit_on_failure: true
- id: APP-CACHE-002
  title: Cache size and eviction are configurable and bounded
  severity: high
  category: cache
  scope: code
  applies_when: application cache exists
  evidence_patterns:
  - maximumSize
  - maximumWeight
  finding_when: cache is unbounded or non-tunable
  unknown_evidence_status: not_assessed
  emit_on_failure: true
- id: APP-CACHE-003
  title: Cache contents do not create regional correctness dependency
  severity: high
  category: cache
  scope: code
  applies_when: application cache exists
  evidence_patterns:
  - cache key
  - invalidation
  finding_when: pod-local cache is required for correctness or session continuity
  unknown_evidence_status: not_assessed
  emit_on_failure: true
- id: APP-ACT-001
  title: Actuator exposure is minimized
  severity: high
  category: management-security
  scope: code
  applies_when: Actuator is used
  evidence_patterns:
  - exposure.include
  - env
  - heapdump
  - loggers
  finding_when: unnecessary diagnostic or administrative endpoints are exposed
  unknown_evidence_status: not_assessed
  emit_on_failure: true
- id: APP-ACT-002
  title: Sensitive Actuator endpoints are protected
  severity: critical
  category: management-security
  scope: code
  applies_when: sensitive endpoints are exposed
  evidence_patterns:
  - SecurityFilterChain
  - EndpointRequest
  finding_when: sensitive endpoints lack authentication or isolation
  unknown_evidence_status: not_assessed
  emit_on_failure: true
- id: APP-ACT-003
  title: Health details avoid sensitive disclosure
  severity: medium
  category: management-security
  scope: code
  applies_when: health endpoint is exposed
  evidence_patterns:
  - show-details
  - show-components
  finding_when: untrusted callers can see sensitive topology or errors
  unknown_evidence_status: not_assessed
  emit_on_failure: true
- id: APP-LOG-001
  title: Credentials and tokens are not logged
  severity: critical
  category: logging-security
  scope: code
  applies_when: credentials exist
  evidence_patterns:
  - log.info
  - Authorization
  - clientSecret
  finding_when: secrets, tokens, credentials, or connection strings can be logged
  unknown_evidence_status: not_assessed
  emit_on_failure: true
- id: APP-LOG-002
  title: Sensitive objects are masked during serialization
  severity: high
  category: logging-security
  scope: code
  applies_when: sensitive configuration objects exist
  evidence_patterns:
  - '@ToString'
  - ToString.Exclude
  - redact
  finding_when: generated or structured serialization exposes sensitive fields
  unknown_evidence_status: not_assessed
  emit_on_failure: true
- id: APP-WEB-001
  title: Exception advice matches servlet or reactive model
  severity: high
  category: web-error-handling
  scope: code
  applies_when: web endpoints exist
  evidence_patterns:
  - '@ControllerAdvice'
  - ErrorWebExceptionHandler
  - WebFlux
  finding_when: handler model or precedence leaves reactive/servlet errors unmapped
  unknown_evidence_status: not_assessed
  emit_on_failure: true
- id: APP-WEB-002
  title: Dependency failures map to stable HTTP semantics
  severity: high
  category: web-error-handling
  scope: code
  applies_when: HTTP API exists
  evidence_patterns:
  - '503'
  - ProblemDetail
  - onErrorMap
  finding_when: dependency failure returns success, not-found, or inconsistent status
  unknown_evidence_status: not_assessed
  emit_on_failure: true
- id: APP-CONF-011
  title: Spring Cloud Config bootstrap has bounded fail-fast behavior
  severity: critical
  category: configuration-bootstrap
  scope: code
  applies_when: Spring Cloud Config Client is used
  evidence_patterns:
  - spring.cloud.config.fail-fast
  - spring.cloud.config.retry
  - request-connect-timeout
  - request-read-timeout
  finding_when: bootstrap uses a regional default or lacks bounded fail-fast, retry,
    and per-attempt timeouts
  unknown_evidence_status: not_assessed
  emit_on_failure: true
- id: APP-CONF-012
  title: Required configuration properties have validated invariants
  severity: high
  category: configuration-bootstrap
  scope: code
  applies_when: external configuration is bound
  evidence_patterns:
  - '@Validated'
  - '@NotNull'
  - '@Min'
  - InitializingBean
  finding_when: missing, null, zero, or invalid external values can reach initialized
    clients or executors
  unknown_evidence_status: not_assessed
  emit_on_failure: true
- id: APP-CONF-013
  title: Used configuration properties are actually consumed
  severity: high
  category: configuration
  scope: code
  applies_when: configuration properties exist
  evidence_patterns:
  - getter usage
  - retryBackoffMaxDuration
  - sessionTimeout
  finding_when: a resiliency property is declared or bound but never applied
  unknown_evidence_status: not_assessed
  emit_on_failure: true
- id: APP-HTTP-001
  title: Blocking calls do not run on reactive event loops or shared async executors
  severity: critical
  category: reactive-http
  scope: code
  applies_when: WebFlux or Reactor is used
  evidence_patterns:
  - .block(
  - boundedElastic
  - '@Async'
  finding_when: blocking calls execute on event-loop or shared executor paths
  unknown_evidence_status: not_assessed
  emit_on_failure: true
- id: APP-HTTP-002
  title: Dependencies use isolated client pools and timeout profiles
  severity: high
  category: http-client
  scope: code
  applies_when: multiple downstream hosts exist
  evidence_patterns:
  - ConnectionProvider
  - WebClient.Builder
  - responseTimeout
  finding_when: unrelated dependencies share one client pool and timeout profile
  unknown_evidence_status: not_assessed
  emit_on_failure: true
- id: APP-HTTP-003
  title: Retry classification covers transient conditions and honors server guidance
  severity: high
  category: http-client
  scope: code
  applies_when: HTTP retry exists
  evidence_patterns:
  - Retry-After
  - '429'
  - 5xx
  - ReadTimeoutException
  finding_when: retry filter is incorrect, omits transient failures, retries terminal
    failures, or ignores Retry-After
  unknown_evidence_status: not_assessed
  emit_on_failure: true
- id: APP-HTTP-004
  title: Authentication recovery is sequenced inside the retry chain
  severity: high
  category: http-client
  scope: code
  applies_when: token-authenticated calls exist
  evidence_patterns:
  - '401'
  - invalidate token
  - onErrorResume
  finding_when: credential invalidation or refresh is detached, occurs after outer
    retry, or repeats stale credentials
  unknown_evidence_status: not_assessed
  emit_on_failure: true
- id: APP-HTTP-005
  title: Shared/global dependency failure does not drain all regions
  severity: high
  category: health
  scope: code
  applies_when: shared third-party dependency exists
  evidence_patterns:
  - readiness contributor
  - circuit breaker health
  finding_when: a globally shared dependency is placed in regional readiness without
    a safe alternative
  unknown_evidence_status: not_assessed
  emit_on_failure: true
- id: APP-TOKEN-001
  title: Token acquisition has bounded last-known-good fallback
  severity: high
  category: authentication-resilience
  scope: code
  applies_when: OAuth token acquisition exists
  evidence_patterns:
  - token cache
  - expiresAt
  - grace period
  finding_when: every request synchronously depends on token service and no bounded
    valid-token fallback exists
  unknown_evidence_status: not_assessed
  emit_on_failure: true
- id: APP-TOKEN-002
  title: Token cache invalidation and refresh are concurrency safe
  severity: high
  category: authentication-resilience
  scope: code
  applies_when: token cache exists
  evidence_patterns:
  - single-flight
  - atomic
  - invalidate
  finding_when: concurrent refreshes stampede, double-subscribe, or return divergent
    tokens
  unknown_evidence_status: not_assessed
  emit_on_failure: true
- id: APP-STATE-001
  title: Durable workflow state transitions are ordered and observable
  severity: critical
  category: durable-state
  scope: code
  applies_when: workflow status is persisted
  evidence_patterns:
  - INPROCESS
  - FAILED
  - COMPLETED
  - then
  - flatMap
  finding_when: pre-network state is fire-and-forget, terminal failure is not persisted,
    or transitions can reorder
  unknown_evidence_status: not_assessed
  emit_on_failure: true
- id: APP-STATE-002
  title: Ambiguous completion and retry exhaustion reach terminal state
  severity: high
  category: durable-state
  scope: code
  applies_when: retries wrap durable work
  evidence_patterns:
  - doOnError
  - onErrorResume
  - FAILED
  finding_when: retry exhaustion leaves durable records stranded in an intermediate
    state
  unknown_evidence_status: not_assessed
  emit_on_failure: true
- id: APP-ASYNC-001
  title: Async infrastructure is explicitly enabled and named executors resolve
  severity: high
  category: async-execution
  scope: code
  applies_when: '@Async is used'
  evidence_patterns:
  - '@EnableAsync'
  - '@Configuration'
  - '@Bean name'
  finding_when: async interception or named executor resolution is not established
  unknown_evidence_status: not_assessed
  emit_on_failure: true
- id: APP-ASYNC-002
  title: Executor capacity and rejection behavior are bounded and validated
  severity: high
  category: async-execution
  scope: code
  applies_when: custom executor exists
  evidence_patterns:
  - queueCapacity
  - RejectedExecutionHandler
  - corePoolSize
  finding_when: executor values are invalid/unbounded or rejection loses work silently
  unknown_evidence_status: not_assessed
  emit_on_failure: true
- id: APP-KAFKA-001
  title: Consumer startup is region-role controlled
  severity: critical
  category: messaging
  scope: code
  applies_when: Kafka consumers exist
  evidence_patterns:
  - autoStartup
  - consumer.autostart
  - KafkaListenerEndpointRegistry
  finding_when: listeners auto-start in both regions without an explicit regional
    ownership decision
  unknown_evidence_status: not_assessed
  emit_on_failure: true
- id: APP-KAFKA-002
  title: Consumer acknowledgment follows successful processing
  severity: critical
  category: messaging
  scope: code
  applies_when: Kafka consumers mutate state or call downstreams
  evidence_patterns:
  - AckMode
  - enable.auto.commit
  - acknowledgment
  finding_when: offsets can advance before downstream and persistence work succeeds
  unknown_evidence_status: not_assessed
  emit_on_failure: true
- id: APP-KAFKA-003
  title: Consumer error handling has finite retry and dead-letter routing
  severity: high
  category: messaging
  scope: code
  applies_when: Kafka consumers exist
  evidence_patterns:
  - DefaultErrorHandler
  - CommonErrorHandler
  - DeadLetterPublishingRecoverer
  finding_when: poison records or terminal failures retry indefinitely, block partitions,
    or disappear
  unknown_evidence_status: not_assessed
  emit_on_failure: true
- id: APP-KAFKA-004
  title: Consumer liveness, lag, assignment, and paused state are observable
  severity: high
  category: messaging
  scope: code
  applies_when: Kafka consumers exist
  evidence_patterns:
  - lag metric
  - listener state
  - assignment
  finding_when: consumer processing can stop or lag without an actionable signal
  unknown_evidence_status: not_assessed
  emit_on_failure: true
- id: APP-KAFKA-005
  title: Producer delivery is awaited and durability settings are explicit
  severity: critical
  category: messaging
  scope: code
  applies_when: Kafka producer exists
  evidence_patterns:
  - send future
  - acks
  - enable.idempotence
  - delivery.timeout.ms
  finding_when: producer send result is discarded or durability settings are absent
  unknown_evidence_status: not_assessed
  emit_on_failure: true
- id: APP-KAFKA-006
  title: Kafka record identity supports downstream deduplication
  severity: high
  category: messaging
  scope: code
  applies_when: Kafka producer exists
  evidence_patterns:
  - message-id
  - event-id
  - RecordHeader
  finding_when: records lack a stable dedupe identity across retry or replay
  unknown_evidence_status: not_assessed
  emit_on_failure: true
- id: APP-KAFKA-007
  title: Kafka client properties bound by the application are applied
  severity: high
  category: messaging
  scope: code
  applies_when: custom Kafka configuration exists
  evidence_patterns:
  - session.timeout.ms
  - max.poll.interval.ms
  - consumer properties
  finding_when: declared listener or producer resiliency settings are not added to
    effective client configuration
  unknown_evidence_status: not_assessed
  emit_on_failure: true
- id: APP-CACHE-004
  title: Cache loading coalesces concurrent misses and refreshes
  severity: high
  category: cache
  scope: code
  applies_when: cache loader calls remote dependencies
  evidence_patterns:
  - LoadingCache
  - single-flight
  - Mono.cache
  finding_when: cold-start or expiration causes a request stampede
  unknown_evidence_status: not_assessed
  emit_on_failure: true
- id: APP-CACHE-005
  title: Refresh and warm-up are protected during dependency degradation
  severity: high
  category: cache
  scope: code
  applies_when: refreshAfterWrite or warm-up exists
  evidence_patterns:
  - refreshAfterWrite
  - warmup
  - CircuitBreaker
  finding_when: refresh or warm-up repeatedly fans out to failing dependencies
  unknown_evidence_status: not_assessed
  emit_on_failure: true
- id: APP-CACHE-006
  title: Cache null and stale-value behavior is explicit
  severity: high
  category: cache
  scope: code
  applies_when: cache stores tokens or remote data
  evidence_patterns:
  - Mono.empty
  - null fallback
  - last known good
  finding_when: null or empty results appear as success or stale use exceeds a validated
    safety window
  unknown_evidence_status: not_assessed
  emit_on_failure: true
- id: APP-HEALTH-001
  title: Health contributor identifiers are verified before group inclusion
  severity: high
  category: health
  scope: code
  applies_when: custom health groups exist
  evidence_patterns:
  - group.readiness.include
  - validate-group-membership
  finding_when: an unverified contributor ID can prevent startup or keep readiness
    DOWN
  unknown_evidence_status: not_assessed
  emit_on_failure: true
- id: APP-HEALTH-002
  title: Health state is updated correctly after successful checks
  severity: high
  category: health
  scope: code
  applies_when: custom filters or cached health state exist
  evidence_patterns:
  - lastExecutionTime
  - lastSuccess
  - AtomicReference
  finding_when: successful checks do not refresh cached health state or recovery remains
    invisible
  unknown_evidence_status: not_assessed
  emit_on_failure: true
- id: APP-API-001
  title: State-changing endpoints use safe HTTP semantics and authorization
  severity: high
  category: api-security
  scope: code
  applies_when: administrative or invalidation endpoints exist
  evidence_patterns:
  - '@GetMapping'
  - '@PostMapping'
  - '@PreAuthorize'
  finding_when: GET mutates state or administrative mutation lacks authentication
    and audit
  unknown_evidence_status: not_assessed
  emit_on_failure: true
- id: APP-SUPPLY-001
  title: Shared dependency upgrades have resiliency regression tests
  severity: medium
  category: dependency-governance
  scope: code
  applies_when: parent BOM or shared model libraries are used
  evidence_patterns:
  - parent version
  - dependencyManagement
  - integration test
  finding_when: transitive upgrades can silently change retry, timeout, bootstrap,
    or serialization behavior without a contract test
  unknown_evidence_status: not_assessed
  emit_on_failure: true
- id: APP-SUPPLY-002
  title: Runtime container base image is immutable
  severity: high
  category: supply-chain
  scope: code
  applies_when: Dockerfile exists
  evidence_patterns:
  - FROM
  - '@sha256'
  - tag
  finding_when: runtime base image is tag-only and can change without source change
  unknown_evidence_status: not_assessed
  emit_on_failure: true
- id: APP-OBS-001
  title: Trace export and correlation are operationally complete
  severity: medium
  category: observability
  scope: code
  applies_when: tracing libraries exist
  evidence_patterns:
  - OTLP
  - Zipkin
  - traceparent
  - exporter endpoint
  finding_when: tracing is declared but has no exporter or cross-service correlation
    cannot be established
  unknown_evidence_status: not_assessed
  emit_on_failure: true
- id: APP-CONF-014
  title: Domain and partner constants are externalized or explicitly immutable contracts
  severity: low
  category: configuration-hygiene
  scope: code
  applies_when: partner-specific constants exist
  evidence_patterns:
  - TODO hardcode
  - scope constant
  - partner code
  finding_when: operationally variable partner or domain values require a code release
    without an explicit immutable-contract rationale
  unknown_evidence_status: not_assessed
  emit_on_failure: true
---

# Spring Boot on AKS Active-Active Code Assessment Standard v3

## Purpose

This master standard consolidates the original application active-active controls, the v2 additions, and additional code-level behaviors identified by comparing five external assessment reports. It intentionally excludes deployment automation and platform/infrastructure findings.

## Mandatory boundary

Assess application code, repository-owned application configuration, runtime behavior, tests, security-sensitive application endpoints, dependency clients, messaging semantics, caching, and observability. Do not assess regional deployment jobs, Actionsfile parity, workflow-catalog support, ACR geo-replication, Azure resource topology, private endpoints, DNS, or other platform deployment state.

## Evaluator workflow

1. Load this master for every Spring Boot assessment.
2. Load dependency-specific standards selected by the inventory.
3. Evaluate only applicable controls.
4. Create findings only from evidence-backed noncompliance.
5. Treat missing evidence as `not_assessed`.
6. Deduplicate by root cause.
7. Suppress PCF findings.

# Controls

## APP-AA-001: One immutable artifact supports both regions

**Severity:** High  
**Category:** deployability  
**Scope:** Application code and repository-owned application configuration  
**Applies when:** always

### Requirement

The implementation must satisfy this behavior when the same artifact runs in either regional deployment.

### Evidence to inspect

- `profiles`
- `artifact`
- `Dockerfile`

### Finding condition

Emit a finding when repository evidence demonstrates that region-specific code or artifact is required.

### Evaluation constraints

- Cite file, symbol or property, and line range.
- Evaluate effective behavior, not the mere presence of a library or annotation.
- Use `not_assessed` when evidence is insufficient.
- Do not create deployment or platform findings from this control.
- Deduplicate overlapping controls under one root-cause finding.

---

## APP-AA-002: Regional endpoints are externally configured

**Severity:** Critical  
**Category:** configuration  
**Scope:** Application code and repository-owned application configuration  
**Applies when:** remote dependencies exist

### Requirement

The implementation must satisfy this behavior when the same artifact runs in either regional deployment.

### Evidence to inspect

- `application.yml`
- `@ConfigurationProperties`
- `baseUrl`

### Finding condition

Emit a finding when repository evidence demonstrates that regional endpoint or hostname is hardcoded.

### Evaluation constraints

- Cite file, symbol or property, and line range.
- Evaluate effective behavior, not the mere presence of a library or annotation.
- Use `not_assessed` when evidence is insufficient.
- Do not create deployment or platform findings from this control.
- Deduplicate overlapping controls under one root-cause finding.

---

## APP-AA-003: Local-region dependency affinity is explicit

**Severity:** Critical  
**Category:** regional-affinity  
**Scope:** Application code and repository-owned application configuration  
**Applies when:** regional dependencies exist

### Requirement

The implementation must satisfy this behavior when the same artifact runs in either regional deployment.

### Evidence to inspect

- `region property`
- `endpoint mapping`

### Finding condition

Emit a finding when repository evidence demonstrates that normal operation can use a remote-region dependency.

### Evaluation constraints

- Cite file, symbol or property, and line range.
- Evaluate effective behavior, not the mere presence of a library or annotation.
- Use `not_assessed` when evidence is insufficient.
- Do not create deployment or platform findings from this control.
- Deduplicate overlapping controls under one root-cause finding.

---

## APP-AA-004: Dependency calls have bounded timeouts

**Severity:** Critical  
**Category:** resilience  
**Scope:** Application code and repository-owned application configuration  
**Applies when:** remote calls exist

### Requirement

The implementation must satisfy this behavior when the same artifact runs in either regional deployment.

### Evidence to inspect

- `connect timeout`
- `response timeout`
- `.timeout(`
- `query timeout`

### Finding condition

Emit a finding when repository evidence demonstrates that remote call can exceed the failure budget.

### Evaluation constraints

- Cite file, symbol or property, and line range.
- Evaluate effective behavior, not the mere presence of a library or annotation.
- Use `not_assessed` when evidence is insufficient.
- Do not create deployment or platform findings from this control.
- Deduplicate overlapping controls under one root-cause finding.

---

## APP-AA-005: Transient failures use bounded retry with backoff

**Severity:** High  
**Category:** resilience  
**Scope:** Application code and repository-owned application configuration  
**Applies when:** retryable calls exist

### Requirement

The implementation must satisfy this behavior when the same artifact runs in either regional deployment.

### Evidence to inspect

- `Retry.backoff`
- `@Retryable`
- `RetryOptions`

### Finding condition

Emit a finding when repository evidence demonstrates that retry is absent, unbounded, or applies to terminal errors.

### Evaluation constraints

- Cite file, symbol or property, and line range.
- Evaluate effective behavior, not the mere presence of a library or annotation.
- Use `not_assessed` when evidence is insufficient.
- Do not create deployment or platform findings from this control.
- Deduplicate overlapping controls under one root-cause finding.

---

## APP-AA-006: Repeated failures are isolated

**Severity:** High  
**Category:** resilience  
**Scope:** Application code and repository-owned application configuration  
**Applies when:** remote calls exist

### Requirement

The implementation must satisfy this behavior when the same artifact runs in either regional deployment.

### Evidence to inspect

- `CircuitBreaker`
- `Bulkhead`
- `connection pool`

### Finding condition

Emit a finding when repository evidence demonstrates that one dependency can exhaust shared resources.

### Evaluation constraints

- Cite file, symbol or property, and line range.
- Evaluate effective behavior, not the mere presence of a library or annotation.
- Use `not_assessed` when evidence is insufficient.
- Do not create deployment or platform findings from this control.
- Deduplicate overlapping controls under one root-cause finding.

---

## APP-AA-007: Critical dependency failure affects readiness

**Severity:** Critical  
**Category:** health  
**Scope:** Application code and repository-owned application configuration  
**Applies when:** critical regional dependency exists

### Requirement

The implementation must satisfy this behavior when the same artifact runs in either regional deployment.

### Evidence to inspect

- `HealthIndicator`
- `readiness group`

### Finding condition

Emit a finding when repository evidence demonstrates that critical dependency remains failed while readiness is UP.

### Evaluation constraints

- Cite file, symbol or property, and line range.
- Evaluate effective behavior, not the mere presence of a library or annotation.
- Use `not_assessed` when evidence is insufficient.
- Do not create deployment or platform findings from this control.
- Deduplicate overlapping controls under one root-cause finding.

---

## APP-AA-008: Liveness excludes external dependencies

**Severity:** Critical  
**Category:** health  
**Scope:** Application code and repository-owned application configuration  
**Applies when:** Actuator probes exist

### Requirement

The implementation must satisfy this behavior when the same artifact runs in either regional deployment.

### Evidence to inspect

- `liveness group`
- `livenessState`

### Finding condition

Emit a finding when repository evidence demonstrates that external failure causes liveness failure or restart loops.

### Evaluation constraints

- Cite file, symbol or property, and line range.
- Evaluate effective behavior, not the mere presence of a library or annotation.
- Use `not_assessed` when evidence is insufficient.
- Do not create deployment or platform findings from this control.
- Deduplicate overlapping controls under one root-cause finding.

---

## APP-AA-009: Health checks are bounded and representative

**Severity:** High  
**Category:** health  
**Scope:** Application code and repository-owned application configuration  
**Applies when:** health contributors exist

### Requirement

The implementation must satisfy this behavior when the same artifact runs in either regional deployment.

### Evidence to inspect

- `health timeout`
- `synthetic check`

### Finding condition

Emit a finding when repository evidence demonstrates that health can hang, overload a dependency, or bypass the serving path.

### Evaluation constraints

- Cite file, symbol or property, and line range.
- Evaluate effective behavior, not the mere presence of a library or annotation.
- Use `not_assessed` when evidence is insufficient.
- Do not create deployment or platform findings from this control.
- Deduplicate overlapping controls under one root-cause finding.

---

## APP-AA-010: Application state is region independent

**Severity:** Critical  
**Category:** state  
**Scope:** Application code and repository-owned application configuration  
**Applies when:** stateful behavior exists

### Requirement

The implementation must satisfy this behavior when the same artifact runs in either regional deployment.

### Evidence to inspect

- `session`
- `local file`
- `in-memory state`

### Finding condition

Emit a finding when repository evidence demonstrates that required state is pod-local or region-local.

### Evaluation constraints

- Cite file, symbol or property, and line range.
- Evaluate effective behavior, not the mere presence of a library or annotation.
- Use `not_assessed` when evidence is insufficient.
- Do not create deployment or platform findings from this control.
- Deduplicate overlapping controls under one root-cause finding.

---

## APP-AA-011: Mutating operations are idempotent

**Severity:** Critical  
**Category:** consistency  
**Scope:** Application code and repository-owned application configuration  
**Applies when:** mutating operations exist

### Requirement

The implementation must satisfy this behavior when the same artifact runs in either regional deployment.

### Evidence to inspect

- `idempotency key`
- `dedupe`
- `unique index`

### Finding condition

Emit a finding when repository evidence demonstrates that retry or replay can duplicate business effects.

### Evaluation constraints

- Cite file, symbol or property, and line range.
- Evaluate effective behavior, not the mere presence of a library or annotation.
- Use `not_assessed` when evidence is insufficient.
- Do not create deployment or platform findings from this control.
- Deduplicate overlapping controls under one root-cause finding.

---

## APP-AA-012: Concurrency and conflict behavior is defined

**Severity:** High  
**Category:** consistency  
**Scope:** Application code and repository-owned application configuration  
**Applies when:** concurrent writes are possible

### Requirement

The implementation must satisfy this behavior when the same artifact runs in either regional deployment.

### Evidence to inspect

- `@Version`
- `ETag`
- `rowversion`

### Finding condition

Emit a finding when repository evidence demonstrates that concurrent writes can silently overwrite state.

### Evaluation constraints

- Cite file, symbol or property, and line range.
- Evaluate effective behavior, not the mere presence of a library or annotation.
- Use `not_assessed` when evidence is insufficient.
- Do not create deployment or platform findings from this control.
- Deduplicate overlapping controls under one root-cause finding.

---

## APP-AA-013: Startup tolerates temporary dependency unavailability

**Severity:** High  
**Category:** startup  
**Scope:** Application code and repository-owned application configuration  
**Applies when:** startup dependencies exist

### Requirement

The implementation must satisfy this behavior when the same artifact runs in either regional deployment.

### Evidence to inspect

- `fail-fast`
- `startup retry`
- `readiness`

### Finding condition

Emit a finding when repository evidence demonstrates that temporary outage causes uncontrolled startup failure.

### Evaluation constraints

- Cite file, symbol or property, and line range.
- Evaluate effective behavior, not the mere presence of a library or annotation.
- Use `not_assessed` when evidence is insufficient.
- Do not create deployment or platform findings from this control.
- Deduplicate overlapping controls under one root-cause finding.

---

## APP-AA-014: Dependency recovery occurs without restart

**Severity:** High  
**Category:** recovery  
**Scope:** Application code and repository-owned application configuration  
**Applies when:** remote clients exist

### Requirement

The implementation must satisfy this behavior when the same artifact runs in either regional deployment.

### Evidence to inspect

- `reconnect`
- `credential refresh`
- `half-open`

### Finding condition

Emit a finding when repository evidence demonstrates that recovery requires process restart.

### Evaluation constraints

- Cite file, symbol or property, and line range.
- Evaluate effective behavior, not the mere presence of a library or annotation.
- Use `not_assessed` when evidence is insufficient.
- Do not create deployment or platform findings from this control.
- Deduplicate overlapping controls under one root-cause finding.

---

## APP-AA-015: Regional identity is present in telemetry

**Severity:** Medium  
**Category:** observability  
**Scope:** Application code and repository-owned application configuration  
**Applies when:** telemetry exists

### Requirement

The implementation must satisfy this behavior when the same artifact runs in either regional deployment.

### Evidence to inspect

- `region tag`
- `cluster tag`

### Finding condition

Emit a finding when repository evidence demonstrates that telemetry cannot identify serving region.

### Evaluation constraints

- Cite file, symbol or property, and line range.
- Evaluate effective behavior, not the mere presence of a library or annotation.
- Use `not_assessed` when evidence is insufficient.
- Do not create deployment or platform findings from this control.
- Deduplicate overlapping controls under one root-cause finding.

---

## APP-AA-016: Failures generate actionable signals

**Severity:** Critical  
**Category:** observability  
**Scope:** Application code and repository-owned application configuration  
**Applies when:** critical dependencies exist

### Requirement

The implementation must satisfy this behavior when the same artifact runs in either regional deployment.

### Evidence to inspect

- `metrics`
- `structured logs`
- `retry exhausted`

### Finding condition

Emit a finding when repository evidence demonstrates that critical failure or recovery is not observable.

### Evaluation constraints

- Cite file, symbol or property, and line range.
- Evaluate effective behavior, not the mere presence of a library or annotation.
- Use `not_assessed` when evidence is insufficient.
- Do not create deployment or platform findings from this control.
- Deduplicate overlapping controls under one root-cause finding.

---

## APP-AA-017: Graceful shutdown and traffic draining are implemented

**Severity:** High  
**Category:** lifecycle  
**Scope:** Application code and repository-owned application configuration  
**Applies when:** service receives traffic or processes work

### Requirement

The implementation must satisfy this behavior when the same artifact runs in either regional deployment.

### Evidence to inspect

- `graceful shutdown`
- `readiness transition`

### Finding condition

Emit a finding when repository evidence demonstrates that termination accepts new work or loses in-flight work.

### Evaluation constraints

- Cite file, symbol or property, and line range.
- Evaluate effective behavior, not the mere presence of a library or annotation.
- Use `not_assessed` when evidence is insufficient.
- Do not create deployment or platform findings from this control.
- Deduplicate overlapping controls under one root-cause finding.

---

## APP-AA-018: Active-active failure behavior is tested

**Severity:** Critical  
**Category:** testing  
**Scope:** Application code and repository-owned application configuration  
**Applies when:** always

### Requirement

The implementation must satisfy this behavior when the same artifact runs in either regional deployment.

### Evidence to inspect

- `fault test`
- `integration test`

### Finding condition

Emit a finding when repository evidence demonstrates that tests do not prove failure and recovery behavior.

### Evaluation constraints

- Cite file, symbol or property, and line range.
- Evaluate effective behavior, not the mere presence of a library or annotation.
- Use `not_assessed` when evidence is insufficient.
- Do not create deployment or platform findings from this control.
- Deduplicate overlapping controls under one root-cause finding.

---

## APP-DISC-001: Discovery endpoint and regional selection are configurable

**Severity:** Critical  
**Category:** service-discovery  
**Scope:** Application code and repository-owned application configuration  
**Applies when:** DiscoveryClient is used

### Requirement

The implementation must satisfy this behavior when the same artifact runs in either regional deployment.

### Evidence to inspect

- `@EnableDiscoveryClient`
- `registry endpoint`

### Finding condition

Emit a finding when repository evidence demonstrates that discovery endpoint or region is hardcoded.

### Evaluation constraints

- Cite file, symbol or property, and line range.
- Evaluate effective behavior, not the mere presence of a library or annotation.
- Use `not_assessed` when evidence is insufficient.
- Do not create deployment or platform findings from this control.
- Deduplicate overlapping controls under one root-cause finding.

---

## APP-DISC-002: Critical discovery state participates in readiness

**Severity:** High  
**Category:** service-discovery  
**Scope:** Application code and repository-owned application configuration  
**Applies when:** discovery is critical

### Requirement

The implementation must satisfy this behavior when the same artifact runs in either regional deployment.

### Evidence to inspect

- `DiscoveryClientHealthIndicator`
- `readiness`

### Finding condition

Emit a finding when repository evidence demonstrates that critical registration or lookup failure leaves readiness UP.

### Evaluation constraints

- Cite file, symbol or property, and line range.
- Evaluate effective behavior, not the mere presence of a library or annotation.
- Use `not_assessed` when evidence is insufficient.
- Do not create deployment or platform findings from this control.
- Deduplicate overlapping controls under one root-cause finding.

---

## APP-CONF-010: Runtime refresh behavior is defined and safe

**Severity:** High  
**Category:** configuration  
**Scope:** Application code and repository-owned application configuration  
**Applies when:** dynamic refresh is enabled or expected

### Requirement

The implementation must satisfy this behavior when the same artifact runs in either regional deployment.

### Evidence to inspect

- `@RefreshScope`
- `EnvironmentChangeEvent`

### Finding condition

Emit a finding when repository evidence demonstrates that refreshed values do not safely affect initialized clients, pools, executors, or caches.

### Evaluation constraints

- Cite file, symbol or property, and line range.
- Evaluate effective behavior, not the mere presence of a library or annotation.
- Use `not_assessed` when evidence is insufficient.
- Do not create deployment or platform findings from this control.
- Deduplicate overlapping controls under one root-cause finding.

---

## APP-REACT-001: Reactive side effects execute once

**Severity:** Critical  
**Category:** reactive  
**Scope:** Application code and repository-owned application configuration  
**Applies when:** Reactor side effects exist

### Requirement

The implementation must satisfy this behavior when the same artifact runs in either regional deployment.

### Evidence to inspect

- `Mono.defer`
- `cache()`
- `subscribe`

### Finding condition

Emit a finding when repository evidence demonstrates that a cold publisher can be subscribed more than once and repeat a side effect.

### Evaluation constraints

- Cite file, symbol or property, and line range.
- Evaluate effective behavior, not the mere presence of a library or annotation.
- Use `not_assessed` when evidence is insufficient.
- Do not create deployment or platform findings from this control.
- Deduplicate overlapping controls under one root-cause finding.

---

## APP-REACT-002: Reactive business chains avoid detached subscriptions

**Severity:** Critical  
**Category:** reactive  
**Scope:** Application code and repository-owned application configuration  
**Applies when:** Reactor is used

### Requirement

The implementation must satisfy this behavior when the same artifact runs in either regional deployment.

### Evidence to inspect

- `.subscribe()`
- `void service method`

### Finding condition

Emit a finding when repository evidence demonstrates that business work is detached from caller-visible completion or error.

### Evaluation constraints

- Cite file, symbol or property, and line range.
- Evaluate effective behavior, not the mere presence of a library or annotation.
- Use `not_assessed` when evidence is insufficient.
- Do not create deployment or platform findings from this control.
- Deduplicate overlapping controls under one root-cause finding.

---

## APP-REACT-003: Reactive error handling preserves failure semantics

**Severity:** High  
**Category:** reactive  
**Scope:** Application code and repository-owned application configuration  
**Applies when:** Reactor is used

### Requirement

The implementation must satisfy this behavior when the same artifact runs in either regional deployment.

### Evidence to inspect

- `onErrorResume`
- `switchIfEmpty`

### Finding condition

Emit a finding when repository evidence demonstrates that dependency failures become empty, not-found, or success.

### Evaluation constraints

- Cite file, symbol or property, and line range.
- Evaluate effective behavior, not the mere presence of a library or annotation.
- Use `not_assessed` when evidence is insufficient.
- Do not create deployment or platform findings from this control.
- Deduplicate overlapping controls under one root-cause finding.

---

## APP-CACHE-001: Cache TTL and refresh intervals are configurable

**Severity:** Medium  
**Category:** cache  
**Scope:** Application code and repository-owned application configuration  
**Applies when:** application cache exists

### Requirement

The implementation must satisfy this behavior when the same artifact runs in either regional deployment.

### Evidence to inspect

- `expireAfterWrite`
- `refreshAfterWrite`

### Finding condition

Emit a finding when repository evidence demonstrates that TTL or refresh is an unexplained code literal.

### Evaluation constraints

- Cite file, symbol or property, and line range.
- Evaluate effective behavior, not the mere presence of a library or annotation.
- Use `not_assessed` when evidence is insufficient.
- Do not create deployment or platform findings from this control.
- Deduplicate overlapping controls under one root-cause finding.

---

## APP-CACHE-002: Cache size and eviction are configurable and bounded

**Severity:** High  
**Category:** cache  
**Scope:** Application code and repository-owned application configuration  
**Applies when:** application cache exists

### Requirement

The implementation must satisfy this behavior when the same artifact runs in either regional deployment.

### Evidence to inspect

- `maximumSize`
- `maximumWeight`

### Finding condition

Emit a finding when repository evidence demonstrates that cache is unbounded or non-tunable.

### Evaluation constraints

- Cite file, symbol or property, and line range.
- Evaluate effective behavior, not the mere presence of a library or annotation.
- Use `not_assessed` when evidence is insufficient.
- Do not create deployment or platform findings from this control.
- Deduplicate overlapping controls under one root-cause finding.

---

## APP-CACHE-003: Cache contents do not create regional correctness dependency

**Severity:** High  
**Category:** cache  
**Scope:** Application code and repository-owned application configuration  
**Applies when:** application cache exists

### Requirement

The implementation must satisfy this behavior when the same artifact runs in either regional deployment.

### Evidence to inspect

- `cache key`
- `invalidation`

### Finding condition

Emit a finding when repository evidence demonstrates that pod-local cache is required for correctness or session continuity.

### Evaluation constraints

- Cite file, symbol or property, and line range.
- Evaluate effective behavior, not the mere presence of a library or annotation.
- Use `not_assessed` when evidence is insufficient.
- Do not create deployment or platform findings from this control.
- Deduplicate overlapping controls under one root-cause finding.

---

## APP-ACT-001: Actuator exposure is minimized

**Severity:** High  
**Category:** management-security  
**Scope:** Application code and repository-owned application configuration  
**Applies when:** Actuator is used

### Requirement

The implementation must satisfy this behavior when the same artifact runs in either regional deployment.

### Evidence to inspect

- `exposure.include`
- `env`
- `heapdump`
- `loggers`

### Finding condition

Emit a finding when repository evidence demonstrates that unnecessary diagnostic or administrative endpoints are exposed.

### Evaluation constraints

- Cite file, symbol or property, and line range.
- Evaluate effective behavior, not the mere presence of a library or annotation.
- Use `not_assessed` when evidence is insufficient.
- Do not create deployment or platform findings from this control.
- Deduplicate overlapping controls under one root-cause finding.

---

## APP-ACT-002: Sensitive Actuator endpoints are protected

**Severity:** Critical  
**Category:** management-security  
**Scope:** Application code and repository-owned application configuration  
**Applies when:** sensitive endpoints are exposed

### Requirement

The implementation must satisfy this behavior when the same artifact runs in either regional deployment.

### Evidence to inspect

- `SecurityFilterChain`
- `EndpointRequest`

### Finding condition

Emit a finding when repository evidence demonstrates that sensitive endpoints lack authentication or isolation.

### Evaluation constraints

- Cite file, symbol or property, and line range.
- Evaluate effective behavior, not the mere presence of a library or annotation.
- Use `not_assessed` when evidence is insufficient.
- Do not create deployment or platform findings from this control.
- Deduplicate overlapping controls under one root-cause finding.

---

## APP-ACT-003: Health details avoid sensitive disclosure

**Severity:** Medium  
**Category:** management-security  
**Scope:** Application code and repository-owned application configuration  
**Applies when:** health endpoint is exposed

### Requirement

The implementation must satisfy this behavior when the same artifact runs in either regional deployment.

### Evidence to inspect

- `show-details`
- `show-components`

### Finding condition

Emit a finding when repository evidence demonstrates that untrusted callers can see sensitive topology or errors.

### Evaluation constraints

- Cite file, symbol or property, and line range.
- Evaluate effective behavior, not the mere presence of a library or annotation.
- Use `not_assessed` when evidence is insufficient.
- Do not create deployment or platform findings from this control.
- Deduplicate overlapping controls under one root-cause finding.

---

## APP-LOG-001: Credentials and tokens are not logged

**Severity:** Critical  
**Category:** logging-security  
**Scope:** Application code and repository-owned application configuration  
**Applies when:** credentials exist

### Requirement

The implementation must satisfy this behavior when the same artifact runs in either regional deployment.

### Evidence to inspect

- `log.info`
- `Authorization`
- `clientSecret`

### Finding condition

Emit a finding when repository evidence demonstrates that secrets, tokens, credentials, or connection strings can be logged.

### Evaluation constraints

- Cite file, symbol or property, and line range.
- Evaluate effective behavior, not the mere presence of a library or annotation.
- Use `not_assessed` when evidence is insufficient.
- Do not create deployment or platform findings from this control.
- Deduplicate overlapping controls under one root-cause finding.

---

## APP-LOG-002: Sensitive objects are masked during serialization

**Severity:** High  
**Category:** logging-security  
**Scope:** Application code and repository-owned application configuration  
**Applies when:** sensitive configuration objects exist

### Requirement

The implementation must satisfy this behavior when the same artifact runs in either regional deployment.

### Evidence to inspect

- `@ToString`
- `ToString.Exclude`
- `redact`

### Finding condition

Emit a finding when repository evidence demonstrates that generated or structured serialization exposes sensitive fields.

### Evaluation constraints

- Cite file, symbol or property, and line range.
- Evaluate effective behavior, not the mere presence of a library or annotation.
- Use `not_assessed` when evidence is insufficient.
- Do not create deployment or platform findings from this control.
- Deduplicate overlapping controls under one root-cause finding.

---

## APP-WEB-001: Exception advice matches servlet or reactive model

**Severity:** High  
**Category:** web-error-handling  
**Scope:** Application code and repository-owned application configuration  
**Applies when:** web endpoints exist

### Requirement

The implementation must satisfy this behavior when the same artifact runs in either regional deployment.

### Evidence to inspect

- `@ControllerAdvice`
- `ErrorWebExceptionHandler`
- `WebFlux`

### Finding condition

Emit a finding when repository evidence demonstrates that handler model or precedence leaves reactive/servlet errors unmapped.

### Evaluation constraints

- Cite file, symbol or property, and line range.
- Evaluate effective behavior, not the mere presence of a library or annotation.
- Use `not_assessed` when evidence is insufficient.
- Do not create deployment or platform findings from this control.
- Deduplicate overlapping controls under one root-cause finding.

---

## APP-WEB-002: Dependency failures map to stable HTTP semantics

**Severity:** High  
**Category:** web-error-handling  
**Scope:** Application code and repository-owned application configuration  
**Applies when:** HTTP API exists

### Requirement

The implementation must satisfy this behavior when the same artifact runs in either regional deployment.

### Evidence to inspect

- `503`
- `ProblemDetail`
- `onErrorMap`

### Finding condition

Emit a finding when repository evidence demonstrates that dependency failure returns success, not-found, or inconsistent status.

### Evaluation constraints

- Cite file, symbol or property, and line range.
- Evaluate effective behavior, not the mere presence of a library or annotation.
- Use `not_assessed` when evidence is insufficient.
- Do not create deployment or platform findings from this control.
- Deduplicate overlapping controls under one root-cause finding.

---

## APP-CONF-011: Spring Cloud Config bootstrap has bounded fail-fast behavior

**Severity:** Critical  
**Category:** configuration-bootstrap  
**Scope:** Application code and repository-owned application configuration  
**Applies when:** Spring Cloud Config Client is used

### Requirement

The implementation must satisfy this behavior when the same artifact runs in either regional deployment.

### Evidence to inspect

- `spring.cloud.config.fail-fast`
- `spring.cloud.config.retry`
- `request-connect-timeout`
- `request-read-timeout`

### Finding condition

Emit a finding when repository evidence demonstrates that bootstrap uses a regional default or lacks bounded fail-fast, retry, and per-attempt timeouts.

### Evaluation constraints

- Cite file, symbol or property, and line range.
- Evaluate effective behavior, not the mere presence of a library or annotation.
- Use `not_assessed` when evidence is insufficient.
- Do not create deployment or platform findings from this control.
- Deduplicate overlapping controls under one root-cause finding.

---

## APP-CONF-012: Required configuration properties have validated invariants

**Severity:** High  
**Category:** configuration-bootstrap  
**Scope:** Application code and repository-owned application configuration  
**Applies when:** external configuration is bound

### Requirement

The implementation must satisfy this behavior when the same artifact runs in either regional deployment.

### Evidence to inspect

- `@Validated`
- `@NotNull`
- `@Min`
- `InitializingBean`

### Finding condition

Emit a finding when repository evidence demonstrates that missing, null, zero, or invalid external values can reach initialized clients or executors.

### Evaluation constraints

- Cite file, symbol or property, and line range.
- Evaluate effective behavior, not the mere presence of a library or annotation.
- Use `not_assessed` when evidence is insufficient.
- Do not create deployment or platform findings from this control.
- Deduplicate overlapping controls under one root-cause finding.

---

## APP-CONF-013: Used configuration properties are actually consumed

**Severity:** High  
**Category:** configuration  
**Scope:** Application code and repository-owned application configuration  
**Applies when:** configuration properties exist

### Requirement

The implementation must satisfy this behavior when the same artifact runs in either regional deployment.

### Evidence to inspect

- `getter usage`
- `retryBackoffMaxDuration`
- `sessionTimeout`

### Finding condition

Emit a finding when repository evidence demonstrates that a resiliency property is declared or bound but never applied.

### Evaluation constraints

- Cite file, symbol or property, and line range.
- Evaluate effective behavior, not the mere presence of a library or annotation.
- Use `not_assessed` when evidence is insufficient.
- Do not create deployment or platform findings from this control.
- Deduplicate overlapping controls under one root-cause finding.

---

## APP-HTTP-001: Blocking calls do not run on reactive event loops or shared async executors

**Severity:** Critical  
**Category:** reactive-http  
**Scope:** Application code and repository-owned application configuration  
**Applies when:** WebFlux or Reactor is used

### Requirement

The implementation must satisfy this behavior when the same artifact runs in either regional deployment.

### Evidence to inspect

- `.block(`
- `boundedElastic`
- `@Async`

### Finding condition

Emit a finding when repository evidence demonstrates that blocking calls execute on event-loop or shared executor paths.

### Evaluation constraints

- Cite file, symbol or property, and line range.
- Evaluate effective behavior, not the mere presence of a library or annotation.
- Use `not_assessed` when evidence is insufficient.
- Do not create deployment or platform findings from this control.
- Deduplicate overlapping controls under one root-cause finding.

---

## APP-HTTP-002: Dependencies use isolated client pools and timeout profiles

**Severity:** High  
**Category:** http-client  
**Scope:** Application code and repository-owned application configuration  
**Applies when:** multiple downstream hosts exist

### Requirement

The implementation must satisfy this behavior when the same artifact runs in either regional deployment.

### Evidence to inspect

- `ConnectionProvider`
- `WebClient.Builder`
- `responseTimeout`

### Finding condition

Emit a finding when repository evidence demonstrates that unrelated dependencies share one client pool and timeout profile.

### Evaluation constraints

- Cite file, symbol or property, and line range.
- Evaluate effective behavior, not the mere presence of a library or annotation.
- Use `not_assessed` when evidence is insufficient.
- Do not create deployment or platform findings from this control.
- Deduplicate overlapping controls under one root-cause finding.

---

## APP-HTTP-003: Retry classification covers transient conditions and honors server guidance

**Severity:** High  
**Category:** http-client  
**Scope:** Application code and repository-owned application configuration  
**Applies when:** HTTP retry exists

### Requirement

The implementation must satisfy this behavior when the same artifact runs in either regional deployment.

### Evidence to inspect

- `Retry-After`
- `429`
- `5xx`
- `ReadTimeoutException`

### Finding condition

Emit a finding when repository evidence demonstrates that retry filter is incorrect, omits transient failures, retries terminal failures, or ignores Retry-After.

### Evaluation constraints

- Cite file, symbol or property, and line range.
- Evaluate effective behavior, not the mere presence of a library or annotation.
- Use `not_assessed` when evidence is insufficient.
- Do not create deployment or platform findings from this control.
- Deduplicate overlapping controls under one root-cause finding.

---

## APP-HTTP-004: Authentication recovery is sequenced inside the retry chain

**Severity:** High  
**Category:** http-client  
**Scope:** Application code and repository-owned application configuration  
**Applies when:** token-authenticated calls exist

### Requirement

The implementation must satisfy this behavior when the same artifact runs in either regional deployment.

### Evidence to inspect

- `401`
- `invalidate token`
- `onErrorResume`

### Finding condition

Emit a finding when repository evidence demonstrates that credential invalidation or refresh is detached, occurs after outer retry, or repeats stale credentials.

### Evaluation constraints

- Cite file, symbol or property, and line range.
- Evaluate effective behavior, not the mere presence of a library or annotation.
- Use `not_assessed` when evidence is insufficient.
- Do not create deployment or platform findings from this control.
- Deduplicate overlapping controls under one root-cause finding.

---

## APP-HTTP-005: Shared/global dependency failure does not drain all regions

**Severity:** High  
**Category:** health  
**Scope:** Application code and repository-owned application configuration  
**Applies when:** shared third-party dependency exists

### Requirement

The implementation must satisfy this behavior when the same artifact runs in either regional deployment.

### Evidence to inspect

- `readiness contributor`
- `circuit breaker health`

### Finding condition

Emit a finding when repository evidence demonstrates that a globally shared dependency is placed in regional readiness without a safe alternative.

### Evaluation constraints

- Cite file, symbol or property, and line range.
- Evaluate effective behavior, not the mere presence of a library or annotation.
- Use `not_assessed` when evidence is insufficient.
- Do not create deployment or platform findings from this control.
- Deduplicate overlapping controls under one root-cause finding.

---

## APP-TOKEN-001: Token acquisition has bounded last-known-good fallback

**Severity:** High  
**Category:** authentication-resilience  
**Scope:** Application code and repository-owned application configuration  
**Applies when:** OAuth token acquisition exists

### Requirement

The implementation must satisfy this behavior when the same artifact runs in either regional deployment.

### Evidence to inspect

- `token cache`
- `expiresAt`
- `grace period`

### Finding condition

Emit a finding when repository evidence demonstrates that every request synchronously depends on token service and no bounded valid-token fallback exists.

### Evaluation constraints

- Cite file, symbol or property, and line range.
- Evaluate effective behavior, not the mere presence of a library or annotation.
- Use `not_assessed` when evidence is insufficient.
- Do not create deployment or platform findings from this control.
- Deduplicate overlapping controls under one root-cause finding.

---

## APP-TOKEN-002: Token cache invalidation and refresh are concurrency safe

**Severity:** High  
**Category:** authentication-resilience  
**Scope:** Application code and repository-owned application configuration  
**Applies when:** token cache exists

### Requirement

The implementation must satisfy this behavior when the same artifact runs in either regional deployment.

### Evidence to inspect

- `single-flight`
- `atomic`
- `invalidate`

### Finding condition

Emit a finding when repository evidence demonstrates that concurrent refreshes stampede, double-subscribe, or return divergent tokens.

### Evaluation constraints

- Cite file, symbol or property, and line range.
- Evaluate effective behavior, not the mere presence of a library or annotation.
- Use `not_assessed` when evidence is insufficient.
- Do not create deployment or platform findings from this control.
- Deduplicate overlapping controls under one root-cause finding.

---

## APP-STATE-001: Durable workflow state transitions are ordered and observable

**Severity:** Critical  
**Category:** durable-state  
**Scope:** Application code and repository-owned application configuration  
**Applies when:** workflow status is persisted

### Requirement

The implementation must satisfy this behavior when the same artifact runs in either regional deployment.

### Evidence to inspect

- `INPROCESS`
- `FAILED`
- `COMPLETED`
- `then`
- `flatMap`

### Finding condition

Emit a finding when repository evidence demonstrates that pre-network state is fire-and-forget, terminal failure is not persisted, or transitions can reorder.

### Evaluation constraints

- Cite file, symbol or property, and line range.
- Evaluate effective behavior, not the mere presence of a library or annotation.
- Use `not_assessed` when evidence is insufficient.
- Do not create deployment or platform findings from this control.
- Deduplicate overlapping controls under one root-cause finding.

---

## APP-STATE-002: Ambiguous completion and retry exhaustion reach terminal state

**Severity:** High  
**Category:** durable-state  
**Scope:** Application code and repository-owned application configuration  
**Applies when:** retries wrap durable work

### Requirement

The implementation must satisfy this behavior when the same artifact runs in either regional deployment.

### Evidence to inspect

- `doOnError`
- `onErrorResume`
- `FAILED`

### Finding condition

Emit a finding when repository evidence demonstrates that retry exhaustion leaves durable records stranded in an intermediate state.

### Evaluation constraints

- Cite file, symbol or property, and line range.
- Evaluate effective behavior, not the mere presence of a library or annotation.
- Use `not_assessed` when evidence is insufficient.
- Do not create deployment or platform findings from this control.
- Deduplicate overlapping controls under one root-cause finding.

---

## APP-ASYNC-001: Async infrastructure is explicitly enabled and named executors resolve

**Severity:** High  
**Category:** async-execution  
**Scope:** Application code and repository-owned application configuration  
**Applies when:** @Async is used

### Requirement

The implementation must satisfy this behavior when the same artifact runs in either regional deployment.

### Evidence to inspect

- `@EnableAsync`
- `@Configuration`
- `@Bean name`

### Finding condition

Emit a finding when repository evidence demonstrates that async interception or named executor resolution is not established.

### Evaluation constraints

- Cite file, symbol or property, and line range.
- Evaluate effective behavior, not the mere presence of a library or annotation.
- Use `not_assessed` when evidence is insufficient.
- Do not create deployment or platform findings from this control.
- Deduplicate overlapping controls under one root-cause finding.

---

## APP-ASYNC-002: Executor capacity and rejection behavior are bounded and validated

**Severity:** High  
**Category:** async-execution  
**Scope:** Application code and repository-owned application configuration  
**Applies when:** custom executor exists

### Requirement

The implementation must satisfy this behavior when the same artifact runs in either regional deployment.

### Evidence to inspect

- `queueCapacity`
- `RejectedExecutionHandler`
- `corePoolSize`

### Finding condition

Emit a finding when repository evidence demonstrates that executor values are invalid/unbounded or rejection loses work silently.

### Evaluation constraints

- Cite file, symbol or property, and line range.
- Evaluate effective behavior, not the mere presence of a library or annotation.
- Use `not_assessed` when evidence is insufficient.
- Do not create deployment or platform findings from this control.
- Deduplicate overlapping controls under one root-cause finding.

---

## APP-KAFKA-001: Consumer startup is region-role controlled

**Severity:** Critical  
**Category:** messaging  
**Scope:** Application code and repository-owned application configuration  
**Applies when:** Kafka consumers exist

### Requirement

The implementation must satisfy this behavior when the same artifact runs in either regional deployment.

### Evidence to inspect

- `autoStartup`
- `consumer.autostart`
- `KafkaListenerEndpointRegistry`

### Finding condition

Emit a finding when repository evidence demonstrates that listeners auto-start in both regions without an explicit regional ownership decision.

### Evaluation constraints

- Cite file, symbol or property, and line range.
- Evaluate effective behavior, not the mere presence of a library or annotation.
- Use `not_assessed` when evidence is insufficient.
- Do not create deployment or platform findings from this control.
- Deduplicate overlapping controls under one root-cause finding.

---

## APP-KAFKA-002: Consumer acknowledgment follows successful processing

**Severity:** Critical  
**Category:** messaging  
**Scope:** Application code and repository-owned application configuration  
**Applies when:** Kafka consumers mutate state or call downstreams

### Requirement

The implementation must satisfy this behavior when the same artifact runs in either regional deployment.

### Evidence to inspect

- `AckMode`
- `enable.auto.commit`
- `acknowledgment`

### Finding condition

Emit a finding when repository evidence demonstrates that offsets can advance before downstream and persistence work succeeds.

### Evaluation constraints

- Cite file, symbol or property, and line range.
- Evaluate effective behavior, not the mere presence of a library or annotation.
- Use `not_assessed` when evidence is insufficient.
- Do not create deployment or platform findings from this control.
- Deduplicate overlapping controls under one root-cause finding.

---

## APP-KAFKA-003: Consumer error handling has finite retry and dead-letter routing

**Severity:** High  
**Category:** messaging  
**Scope:** Application code and repository-owned application configuration  
**Applies when:** Kafka consumers exist

### Requirement

The implementation must satisfy this behavior when the same artifact runs in either regional deployment.

### Evidence to inspect

- `DefaultErrorHandler`
- `CommonErrorHandler`
- `DeadLetterPublishingRecoverer`

### Finding condition

Emit a finding when repository evidence demonstrates that poison records or terminal failures retry indefinitely, block partitions, or disappear.

### Evaluation constraints

- Cite file, symbol or property, and line range.
- Evaluate effective behavior, not the mere presence of a library or annotation.
- Use `not_assessed` when evidence is insufficient.
- Do not create deployment or platform findings from this control.
- Deduplicate overlapping controls under one root-cause finding.

---

## APP-KAFKA-004: Consumer liveness, lag, assignment, and paused state are observable

**Severity:** High  
**Category:** messaging  
**Scope:** Application code and repository-owned application configuration  
**Applies when:** Kafka consumers exist

### Requirement

The implementation must satisfy this behavior when the same artifact runs in either regional deployment.

### Evidence to inspect

- `lag metric`
- `listener state`
- `assignment`

### Finding condition

Emit a finding when repository evidence demonstrates that consumer processing can stop or lag without an actionable signal.

### Evaluation constraints

- Cite file, symbol or property, and line range.
- Evaluate effective behavior, not the mere presence of a library or annotation.
- Use `not_assessed` when evidence is insufficient.
- Do not create deployment or platform findings from this control.
- Deduplicate overlapping controls under one root-cause finding.

---

## APP-KAFKA-005: Producer delivery is awaited and durability settings are explicit

**Severity:** Critical  
**Category:** messaging  
**Scope:** Application code and repository-owned application configuration  
**Applies when:** Kafka producer exists

### Requirement

The implementation must satisfy this behavior when the same artifact runs in either regional deployment.

### Evidence to inspect

- `send future`
- `acks`
- `enable.idempotence`
- `delivery.timeout.ms`

### Finding condition

Emit a finding when repository evidence demonstrates that producer send result is discarded or durability settings are absent.

### Evaluation constraints

- Cite file, symbol or property, and line range.
- Evaluate effective behavior, not the mere presence of a library or annotation.
- Use `not_assessed` when evidence is insufficient.
- Do not create deployment or platform findings from this control.
- Deduplicate overlapping controls under one root-cause finding.

---

## APP-KAFKA-006: Kafka record identity supports downstream deduplication

**Severity:** High  
**Category:** messaging  
**Scope:** Application code and repository-owned application configuration  
**Applies when:** Kafka producer exists

### Requirement

The implementation must satisfy this behavior when the same artifact runs in either regional deployment.

### Evidence to inspect

- `message-id`
- `event-id`
- `RecordHeader`

### Finding condition

Emit a finding when repository evidence demonstrates that records lack a stable dedupe identity across retry or replay.

### Evaluation constraints

- Cite file, symbol or property, and line range.
- Evaluate effective behavior, not the mere presence of a library or annotation.
- Use `not_assessed` when evidence is insufficient.
- Do not create deployment or platform findings from this control.
- Deduplicate overlapping controls under one root-cause finding.

---

## APP-KAFKA-007: Kafka client properties bound by the application are applied

**Severity:** High  
**Category:** messaging  
**Scope:** Application code and repository-owned application configuration  
**Applies when:** custom Kafka configuration exists

### Requirement

The implementation must satisfy this behavior when the same artifact runs in either regional deployment.

### Evidence to inspect

- `session.timeout.ms`
- `max.poll.interval.ms`
- `consumer properties`

### Finding condition

Emit a finding when repository evidence demonstrates that declared listener or producer resiliency settings are not added to effective client configuration.

### Evaluation constraints

- Cite file, symbol or property, and line range.
- Evaluate effective behavior, not the mere presence of a library or annotation.
- Use `not_assessed` when evidence is insufficient.
- Do not create deployment or platform findings from this control.
- Deduplicate overlapping controls under one root-cause finding.

---

## APP-CACHE-004: Cache loading coalesces concurrent misses and refreshes

**Severity:** High  
**Category:** cache  
**Scope:** Application code and repository-owned application configuration  
**Applies when:** cache loader calls remote dependencies

### Requirement

The implementation must satisfy this behavior when the same artifact runs in either regional deployment.

### Evidence to inspect

- `LoadingCache`
- `single-flight`
- `Mono.cache`

### Finding condition

Emit a finding when repository evidence demonstrates that cold-start or expiration causes a request stampede.

### Evaluation constraints

- Cite file, symbol or property, and line range.
- Evaluate effective behavior, not the mere presence of a library or annotation.
- Use `not_assessed` when evidence is insufficient.
- Do not create deployment or platform findings from this control.
- Deduplicate overlapping controls under one root-cause finding.

---

## APP-CACHE-005: Refresh and warm-up are protected during dependency degradation

**Severity:** High  
**Category:** cache  
**Scope:** Application code and repository-owned application configuration  
**Applies when:** refreshAfterWrite or warm-up exists

### Requirement

The implementation must satisfy this behavior when the same artifact runs in either regional deployment.

### Evidence to inspect

- `refreshAfterWrite`
- `warmup`
- `CircuitBreaker`

### Finding condition

Emit a finding when repository evidence demonstrates that refresh or warm-up repeatedly fans out to failing dependencies.

### Evaluation constraints

- Cite file, symbol or property, and line range.
- Evaluate effective behavior, not the mere presence of a library or annotation.
- Use `not_assessed` when evidence is insufficient.
- Do not create deployment or platform findings from this control.
- Deduplicate overlapping controls under one root-cause finding.

---

## APP-CACHE-006: Cache null and stale-value behavior is explicit

**Severity:** High  
**Category:** cache  
**Scope:** Application code and repository-owned application configuration  
**Applies when:** cache stores tokens or remote data

### Requirement

The implementation must satisfy this behavior when the same artifact runs in either regional deployment.

### Evidence to inspect

- `Mono.empty`
- `null fallback`
- `last known good`

### Finding condition

Emit a finding when repository evidence demonstrates that null or empty results appear as success or stale use exceeds a validated safety window.

### Evaluation constraints

- Cite file, symbol or property, and line range.
- Evaluate effective behavior, not the mere presence of a library or annotation.
- Use `not_assessed` when evidence is insufficient.
- Do not create deployment or platform findings from this control.
- Deduplicate overlapping controls under one root-cause finding.

---

## APP-HEALTH-001: Health contributor identifiers are verified before group inclusion

**Severity:** High  
**Category:** health  
**Scope:** Application code and repository-owned application configuration  
**Applies when:** custom health groups exist

### Requirement

The implementation must satisfy this behavior when the same artifact runs in either regional deployment.

### Evidence to inspect

- `group.readiness.include`
- `validate-group-membership`

### Finding condition

Emit a finding when repository evidence demonstrates that an unverified contributor ID can prevent startup or keep readiness DOWN.

### Evaluation constraints

- Cite file, symbol or property, and line range.
- Evaluate effective behavior, not the mere presence of a library or annotation.
- Use `not_assessed` when evidence is insufficient.
- Do not create deployment or platform findings from this control.
- Deduplicate overlapping controls under one root-cause finding.

---

## APP-HEALTH-002: Health state is updated correctly after successful checks

**Severity:** High  
**Category:** health  
**Scope:** Application code and repository-owned application configuration  
**Applies when:** custom filters or cached health state exist

### Requirement

The implementation must satisfy this behavior when the same artifact runs in either regional deployment.

### Evidence to inspect

- `lastExecutionTime`
- `lastSuccess`
- `AtomicReference`

### Finding condition

Emit a finding when repository evidence demonstrates that successful checks do not refresh cached health state or recovery remains invisible.

### Evaluation constraints

- Cite file, symbol or property, and line range.
- Evaluate effective behavior, not the mere presence of a library or annotation.
- Use `not_assessed` when evidence is insufficient.
- Do not create deployment or platform findings from this control.
- Deduplicate overlapping controls under one root-cause finding.

---

## APP-API-001: State-changing endpoints use safe HTTP semantics and authorization

**Severity:** High  
**Category:** api-security  
**Scope:** Application code and repository-owned application configuration  
**Applies when:** administrative or invalidation endpoints exist

### Requirement

The implementation must satisfy this behavior when the same artifact runs in either regional deployment.

### Evidence to inspect

- `@GetMapping`
- `@PostMapping`
- `@PreAuthorize`

### Finding condition

Emit a finding when repository evidence demonstrates that GET mutates state or administrative mutation lacks authentication and audit.

### Evaluation constraints

- Cite file, symbol or property, and line range.
- Evaluate effective behavior, not the mere presence of a library or annotation.
- Use `not_assessed` when evidence is insufficient.
- Do not create deployment or platform findings from this control.
- Deduplicate overlapping controls under one root-cause finding.

---

## APP-SUPPLY-001: Shared dependency upgrades have resiliency regression tests

**Severity:** Medium  
**Category:** dependency-governance  
**Scope:** Application code and repository-owned application configuration  
**Applies when:** parent BOM or shared model libraries are used

### Requirement

The implementation must satisfy this behavior when the same artifact runs in either regional deployment.

### Evidence to inspect

- `parent version`
- `dependencyManagement`
- `integration test`

### Finding condition

Emit a finding when repository evidence demonstrates that transitive upgrades can silently change retry, timeout, bootstrap, or serialization behavior without a contract test.

### Evaluation constraints

- Cite file, symbol or property, and line range.
- Evaluate effective behavior, not the mere presence of a library or annotation.
- Use `not_assessed` when evidence is insufficient.
- Do not create deployment or platform findings from this control.
- Deduplicate overlapping controls under one root-cause finding.

---

## APP-SUPPLY-002: Runtime container base image is immutable

**Severity:** High  
**Category:** supply-chain  
**Scope:** Application code and repository-owned application configuration  
**Applies when:** Dockerfile exists

### Requirement

The implementation must satisfy this behavior when the same artifact runs in either regional deployment.

### Evidence to inspect

- `FROM`
- `@sha256`
- `tag`

### Finding condition

Emit a finding when repository evidence demonstrates that runtime base image is tag-only and can change without source change.

### Evaluation constraints

- Cite file, symbol or property, and line range.
- Evaluate effective behavior, not the mere presence of a library or annotation.
- Use `not_assessed` when evidence is insufficient.
- Do not create deployment or platform findings from this control.
- Deduplicate overlapping controls under one root-cause finding.

---

## APP-OBS-001: Trace export and correlation are operationally complete

**Severity:** Medium  
**Category:** observability  
**Scope:** Application code and repository-owned application configuration  
**Applies when:** tracing libraries exist

### Requirement

The implementation must satisfy this behavior when the same artifact runs in either regional deployment.

### Evidence to inspect

- `OTLP`
- `Zipkin`
- `traceparent`
- `exporter endpoint`

### Finding condition

Emit a finding when repository evidence demonstrates that tracing is declared but has no exporter or cross-service correlation cannot be established.

### Evaluation constraints

- Cite file, symbol or property, and line range.
- Evaluate effective behavior, not the mere presence of a library or annotation.
- Use `not_assessed` when evidence is insufficient.
- Do not create deployment or platform findings from this control.
- Deduplicate overlapping controls under one root-cause finding.

---

## APP-CONF-014: Domain and partner constants are externalized or explicitly immutable contracts

**Severity:** Low  
**Category:** configuration-hygiene  
**Scope:** Application code and repository-owned application configuration  
**Applies when:** partner-specific constants exist

### Requirement

The implementation must satisfy this behavior when the same artifact runs in either regional deployment.

### Evidence to inspect

- `TODO hardcode`
- `scope constant`
- `partner code`

### Finding condition

Emit a finding when repository evidence demonstrates that operationally variable partner or domain values require a code release without an explicit immutable-contract rationale.

### Evaluation constraints

- Cite file, symbol or property, and line range.
- Evaluate effective behavior, not the mere presence of a library or annotation.
- Use `not_assessed` when evidence is insufficient.
- Do not create deployment or platform findings from this control.
- Deduplicate overlapping controls under one root-cause finding.

---

# Finding output contract

Every finding must include primary control, related controls, severity, repository evidence, observed behavior, active-active or operational impact, required application change, validation test, and confidence.
