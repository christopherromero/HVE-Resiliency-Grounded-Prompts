---
schema_version: 4.0.0
document_type: master_application_behavior
service: springboot_aks_active_active
version: 4.0.0
last_updated: '2026-08-27'
assessment_scope: application_code_only
lifecycle_status: active
control_count: 86
quality_caveats:
- Adding @Transactional is not sufficient for reactive work; verify ReactiveTransactionManager
  or TransactionalOperator and one composed subscription boundary.
- Do not place every dependency in readiness. Gate on critical region-local serving
  dependencies only; a globally shared dependency can drain all regions simultaneously.
- A timestamp or random UUID generated per attempt is correlation, not a stable idempotency
  key.
- Do not retry a non-idempotent operation after an ambiguous completion unless provider
  idempotency or reconciliation makes it safe.
- A feature flag alone is not a distributed single-active guarantee. Require fail-safe
  defaults, observable ownership, and split-brain detection; prefer a lease or atomic
  ownership token when concurrent activation is possible.
- A fallback store or service is not resilient when its write is detached, unbounded,
  or unobservable. Evaluate primary failure, fallback success, and dual failure separately.
- External dependencies must not be coupled to liveness.
- Durable work should store a logical destination and resolve the current regional
  endpoint at execution time; preserve the original physical endpoint only for audit.
- Do not prescribe numeric retry, timeout, pool, or circuit-breaker values without
  workload evidence. Require external configurability and budget alignment.
- Do not infer deployed infrastructure noncompliance from absent repository evidence.
  Use not_assessed or external evidence required.
excluded_from_findings:
- deployment workflow regional parity
- Actionsfile and Helm regional descriptors
- AKS HPA, PDB, topology spread, startup probes, and sidecar annotations
- Istio ServiceEntry, DestinationRule, mTLS, egress, and static IP configuration
- Azure SQL Failover Group provisioning
- ACR geo-replication
- Key Vault regional deployment and secret synchronization
- private endpoints, DNS, VPN, certificates, and GLB configuration
- PCF migration, modernization, cleanup, and findings
controls:
- id: APP-AA-001
  title: One immutable artifact supports both regions
  severity: high
  category: deployability
  applies_when: always
  evidence_patterns:
  - profiles
  - artifact
  - Dockerfile
  finding_when: region-specific code or artifact is required
  unknown_evidence_status: not_assessed
  emit_on_failure: true
  quality_guidance: []
- id: APP-AA-002
  title: Regional endpoints are externally configured
  severity: critical
  category: configuration
  applies_when: remote dependencies exist
  evidence_patterns:
  - application.yml
  - '@ConfigurationProperties'
  - baseUrl
  finding_when: a regional endpoint or physical hostname is hardcoded
  unknown_evidence_status: not_assessed
  emit_on_failure: true
  quality_guidance: []
- id: APP-AA-003
  title: Local-region dependency affinity is explicit
  severity: critical
  category: regional-affinity
  applies_when: regional dependencies exist
  evidence_patterns:
  - region property
  - endpoint mapping
  finding_when: normal operation can use a remote-region dependency without an explicit
    policy
  unknown_evidence_status: not_assessed
  emit_on_failure: true
  quality_guidance: []
- id: APP-AA-004
  title: Dependency calls have bounded timeouts
  severity: critical
  category: resilience
  applies_when: remote calls exist
  evidence_patterns:
  - connect timeout
  - response timeout
  - .timeout(
  - query timeout
  finding_when: a remote call can exceed the end-to-end failure budget
  unknown_evidence_status: not_assessed
  emit_on_failure: true
  quality_guidance: []
- id: APP-AA-005
  title: Transient failures use bounded retry with backoff
  severity: high
  category: resilience
  applies_when: retryable calls exist
  evidence_patterns:
  - Retry.backoff
  - '@Retryable'
  - RetryOptions
  finding_when: retry is absent, unbounded, or applies to terminal or ambiguous operations
    without safety
  unknown_evidence_status: not_assessed
  emit_on_failure: true
  quality_guidance: []
- id: APP-AA-006
  title: Repeated failures are isolated
  severity: high
  category: resilience
  applies_when: remote calls exist
  evidence_patterns:
  - CircuitBreaker
  - Bulkhead
  - connection pool
  finding_when: one dependency can exhaust shared resources
  unknown_evidence_status: not_assessed
  emit_on_failure: true
  quality_guidance: []
- id: APP-AA-007
  title: Critical regional dependency failure affects readiness
  severity: critical
  category: health
  applies_when: critical regional dependency exists
  evidence_patterns:
  - HealthIndicator
  - readiness group
  finding_when: a critical region-local dependency remains failed while readiness
    is UP
  unknown_evidence_status: not_assessed
  emit_on_failure: true
  quality_guidance: []
- id: APP-AA-008
  title: Liveness excludes external dependencies
  severity: critical
  category: health
  applies_when: Actuator probes exist
  evidence_patterns:
  - liveness group
  - livenessState
  finding_when: external failure causes liveness failure or restart loops
  unknown_evidence_status: not_assessed
  emit_on_failure: true
  quality_guidance: []
- id: APP-AA-009
  title: Health checks are bounded and representative
  severity: high
  category: health
  applies_when: health contributors exist
  evidence_patterns:
  - health timeout
  - synthetic check
  finding_when: health can hang, overload a dependency, or bypass the serving path
  unknown_evidence_status: not_assessed
  emit_on_failure: true
  quality_guidance: []
- id: APP-AA-010
  title: Application state is region independent
  severity: critical
  category: state
  applies_when: stateful behavior exists
  evidence_patterns:
  - session
  - local file
  - in-memory state
  finding_when: required state is pod-local or region-local
  unknown_evidence_status: not_assessed
  emit_on_failure: true
  quality_guidance: []
- id: APP-AA-011
  title: Mutating operations are idempotent
  severity: critical
  category: consistency
  applies_when: mutating operations exist
  evidence_patterns:
  - idempotency key
  - dedupe
  - unique index
  finding_when: retry or replay can duplicate business effects
  unknown_evidence_status: not_assessed
  emit_on_failure: true
  quality_guidance: []
- id: APP-AA-012
  title: Concurrency and conflict behavior is defined
  severity: high
  category: consistency
  applies_when: concurrent writes are possible
  evidence_patterns:
  - '@Version'
  - ETag
  - rowversion
  finding_when: concurrent writes can silently overwrite state
  unknown_evidence_status: not_assessed
  emit_on_failure: true
  quality_guidance: []
- id: APP-AA-013
  title: Startup tolerates temporary dependency unavailability
  severity: high
  category: startup
  applies_when: startup dependencies exist
  evidence_patterns:
  - fail-fast
  - startup retry
  - readiness
  finding_when: temporary outage causes uncontrolled or unbounded startup failure
  unknown_evidence_status: not_assessed
  emit_on_failure: true
  quality_guidance: []
- id: APP-AA-014
  title: Dependency recovery occurs without restart
  severity: high
  category: recovery
  applies_when: remote clients exist
  evidence_patterns:
  - reconnect
  - credential refresh
  - half-open
  finding_when: recovery requires process restart
  unknown_evidence_status: not_assessed
  emit_on_failure: true
  quality_guidance: []
- id: APP-AA-015
  title: Regional identity is present in telemetry
  severity: medium
  category: observability
  applies_when: telemetry exists
  evidence_patterns:
  - region tag
  - cluster tag
  finding_when: telemetry cannot identify the serving region
  unknown_evidence_status: not_assessed
  emit_on_failure: true
  quality_guidance: []
- id: APP-AA-016
  title: Failures generate actionable signals
  severity: critical
  category: observability
  applies_when: critical dependencies exist
  evidence_patterns:
  - metrics
  - structured logs
  - retry exhausted
  finding_when: critical failure or recovery is not observable
  unknown_evidence_status: not_assessed
  emit_on_failure: true
  quality_guidance: []
- id: APP-AA-017
  title: Graceful shutdown and traffic draining are implemented
  severity: high
  category: lifecycle
  applies_when: service receives traffic or processes work
  evidence_patterns:
  - graceful shutdown
  - readiness transition
  finding_when: termination accepts new work or loses in-flight work
  unknown_evidence_status: not_assessed
  emit_on_failure: true
  quality_guidance: []
- id: APP-AA-018
  title: Failure behavior is tested
  severity: critical
  category: testing
  applies_when: always
  evidence_patterns:
  - fault test
  - integration test
  finding_when: tests do not prove timeout, retry, health transition, idempotency,
    shutdown, and recovery behavior
  unknown_evidence_status: not_assessed
  emit_on_failure: true
  quality_guidance: []
- id: APP-DISC-001
  title: Discovery endpoint and regional selection are configurable
  severity: critical
  category: service-discovery
  applies_when: DiscoveryClient is used
  evidence_patterns:
  - '@EnableDiscoveryClient'
  - registry endpoint
  finding_when: discovery endpoint or region is hardcoded
  unknown_evidence_status: not_assessed
  emit_on_failure: true
  quality_guidance: []
- id: APP-DISC-002
  title: Critical discovery state participates in readiness
  severity: high
  category: service-discovery
  applies_when: discovery is critical
  evidence_patterns:
  - DiscoveryClientHealthIndicator
  - readiness
  finding_when: critical registration or lookup failure leaves readiness UP
  unknown_evidence_status: not_assessed
  emit_on_failure: true
  quality_guidance: []
- id: APP-CONF-010
  title: Runtime refresh behavior is defined and safe
  severity: high
  category: configuration
  applies_when: dynamic refresh is enabled or expected
  evidence_patterns:
  - '@RefreshScope'
  - EnvironmentChangeEvent
  finding_when: refreshed values do not safely affect initialized clients, pools,
    executors, or caches
  unknown_evidence_status: not_assessed
  emit_on_failure: true
  quality_guidance: []
- id: APP-REACT-001
  title: Reactive side effects execute once
  severity: critical
  category: reactive
  applies_when: Reactor side effects exist
  evidence_patterns:
  - Mono.defer
  - cache()
  - subscribe
  finding_when: a cold publisher can be subscribed more than once and repeat a side
    effect
  unknown_evidence_status: not_assessed
  emit_on_failure: true
  quality_guidance: []
- id: APP-REACT-002
  title: Reactive business chains avoid detached subscriptions
  severity: critical
  category: reactive
  applies_when: Reactor is used
  evidence_patterns:
  - .subscribe()
  - void service method
  finding_when: business work is detached from caller-visible completion or error
  unknown_evidence_status: not_assessed
  emit_on_failure: true
  quality_guidance: []
- id: APP-REACT-003
  title: Reactive error handling preserves failure semantics
  severity: high
  category: reactive
  applies_when: Reactor is used
  evidence_patterns:
  - onErrorResume
  - switchIfEmpty
  finding_when: dependency failures become empty, not-found, or success
  unknown_evidence_status: not_assessed
  emit_on_failure: true
  quality_guidance: []
- id: APP-CACHE-001
  title: Cache TTL and refresh intervals are configurable
  severity: medium
  category: cache
  applies_when: application cache exists
  evidence_patterns:
  - expireAfterWrite
  - refreshAfterWrite
  finding_when: TTL or refresh is an unexplained literal
  unknown_evidence_status: not_assessed
  emit_on_failure: true
  quality_guidance: []
- id: APP-CACHE-002
  title: Cache size and eviction are configurable and bounded
  severity: high
  category: cache
  applies_when: application cache exists
  evidence_patterns:
  - maximumSize
  - maximumWeight
  finding_when: cache is unbounded or non-tunable
  unknown_evidence_status: not_assessed
  emit_on_failure: true
  quality_guidance: []
- id: APP-CACHE-003
  title: Cache contents do not create regional correctness dependency
  severity: high
  category: cache
  applies_when: application cache exists
  evidence_patterns:
  - cache key
  - invalidation
  finding_when: pod-local cache is required for correctness or session continuity
  unknown_evidence_status: not_assessed
  emit_on_failure: true
  quality_guidance: []
- id: APP-ACT-001
  title: Actuator exposure is minimized
  severity: high
  category: management-security
  applies_when: Actuator is used
  evidence_patterns:
  - exposure.include
  - env
  - heapdump
  - loggers
  finding_when: unnecessary diagnostic or administrative endpoints are exposed
  unknown_evidence_status: not_assessed
  emit_on_failure: true
  quality_guidance: []
- id: APP-ACT-002
  title: Sensitive Actuator endpoints are protected
  severity: critical
  category: management-security
  applies_when: sensitive endpoints are exposed
  evidence_patterns:
  - SecurityFilterChain
  - EndpointRequest
  finding_when: sensitive endpoints lack authentication or isolation
  unknown_evidence_status: not_assessed
  emit_on_failure: true
  quality_guidance: []
- id: APP-ACT-003
  title: Health details avoid sensitive disclosure
  severity: medium
  category: management-security
  applies_when: health endpoint is exposed
  evidence_patterns:
  - show-details
  - show-components
  finding_when: untrusted callers can see sensitive topology or errors
  unknown_evidence_status: not_assessed
  emit_on_failure: true
  quality_guidance: []
- id: APP-LOG-001
  title: Credentials and sensitive payment data are not logged
  severity: critical
  category: logging-security
  applies_when: sensitive values exist
  evidence_patterns:
  - Authorization
  - clientSecret
  - PAN
  - HMAC
  - APIM key
  - request body
  finding_when: secrets, credentials, PCI/PII, signed headers, payment data, or connection
    strings can be logged
  unknown_evidence_status: not_assessed
  emit_on_failure: true
  quality_guidance: []
- id: APP-LOG-002
  title: Sensitive objects are masked during serialization
  severity: high
  category: logging-security
  applies_when: sensitive configuration objects exist
  evidence_patterns:
  - '@ToString'
  - ToString.Exclude
  - redact
  finding_when: generated or structured serialization exposes sensitive fields
  unknown_evidence_status: not_assessed
  emit_on_failure: true
  quality_guidance: []
- id: APP-WEB-001
  title: Exception advice matches servlet or reactive model
  severity: high
  category: web-error-handling
  applies_when: web endpoints exist
  evidence_patterns:
  - '@ControllerAdvice'
  - ErrorWebExceptionHandler
  - WebFlux
  finding_when: handler model or precedence leaves reactive or servlet errors unmapped
  unknown_evidence_status: not_assessed
  emit_on_failure: true
  quality_guidance: []
- id: APP-WEB-002
  title: Dependency failures map to stable caller-visible semantics
  severity: high
  category: web-error-handling
  applies_when: API exists
  evidence_patterns:
  - '503'
  - ProblemDetail
  - onErrorMap
  finding_when: dependency failure returns success, not-found, null, or an inconsistent
    status
  unknown_evidence_status: not_assessed
  emit_on_failure: true
  quality_guidance: []
- id: APP-CONF-011
  title: Spring Cloud Config bootstrap has bounded fail-fast behavior
  severity: critical
  category: configuration-bootstrap
  applies_when: Config Client is used
  evidence_patterns:
  - fail-fast
  - spring.cloud.config.retry
  - request-connect-timeout
  finding_when: bootstrap uses a regional default or lacks bounded fail-fast, retry,
    and per-attempt timeouts
  unknown_evidence_status: not_assessed
  emit_on_failure: true
  quality_guidance: []
- id: APP-CONF-012
  title: Required configuration properties have validated invariants
  severity: high
  category: configuration-bootstrap
  applies_when: external configuration is bound
  evidence_patterns:
  - '@Validated'
  - '@NotNull'
  - '@Min'
  finding_when: invalid external values can reach initialized clients or executors
  unknown_evidence_status: not_assessed
  emit_on_failure: true
  quality_guidance: []
- id: APP-CONF-013
  title: Bound resiliency properties are actually consumed
  severity: high
  category: configuration
  applies_when: configuration properties exist
  evidence_patterns:
  - getter usage
  - retryBackoffMaxDuration
  - sessionTimeout
  finding_when: a declared resiliency property is never applied
  unknown_evidence_status: not_assessed
  emit_on_failure: true
  quality_guidance: []
- id: APP-HTTP-001
  title: Blocking dependency and SDK calls are isolated
  severity: critical
  category: dependency-client
  applies_when: reactive or shared-thread runtime is used
  evidence_patterns:
  - .block(
  - RestTemplate
  - vendor SDK
  - boundedElastic
  finding_when: blocking calls execute on event-loop, health, or shared executor threads
  unknown_evidence_status: not_assessed
  emit_on_failure: true
  quality_guidance: []
- id: APP-HTTP-002
  title: Dependencies use isolated client pools and timeout profiles
  severity: high
  category: http-client
  applies_when: multiple downstream hosts exist
  evidence_patterns:
  - ConnectionProvider
  - WebClient.Builder
  - responseTimeout
  finding_when: unrelated dependencies share one pool and timeout profile
  unknown_evidence_status: not_assessed
  emit_on_failure: true
  quality_guidance: []
- id: APP-HTTP-003
  title: Retry classification covers transient conditions and server guidance
  severity: high
  category: http-client
  applies_when: HTTP retry exists
  evidence_patterns:
  - Retry-After
  - '429'
  - 5xx
  - ReadTimeoutException
  finding_when: retry classification is unsafe or ignores server guidance
  unknown_evidence_status: not_assessed
  emit_on_failure: true
  quality_guidance: []
- id: APP-HTTP-004
  title: Authentication recovery is sequenced inside retry
  severity: high
  category: http-client
  applies_when: token-authenticated calls exist
  evidence_patterns:
  - '401'
  - invalidate token
  - onErrorResume
  finding_when: credential refresh is detached or repeats stale credentials
  unknown_evidence_status: not_assessed
  emit_on_failure: true
  quality_guidance: []
- id: APP-HTTP-005
  title: Shared global dependency failure does not drain all regions
  severity: high
  category: health
  applies_when: shared third-party dependency exists
  evidence_patterns:
  - readiness contributor
  - circuit breaker health
  finding_when: a globally shared dependency is placed in regional readiness without
    an alternative
  unknown_evidence_status: not_assessed
  emit_on_failure: true
  quality_guidance: []
- id: APP-TOKEN-001
  title: Token acquisition has bounded last-known-good fallback
  severity: high
  category: authentication-resilience
  applies_when: OAuth token acquisition exists
  evidence_patterns:
  - token cache
  - expiresAt
  - grace period
  finding_when: every request synchronously depends on token service without a bounded
    valid-token fallback
  unknown_evidence_status: not_assessed
  emit_on_failure: true
  quality_guidance: []
- id: APP-TOKEN-002
  title: Token refresh is concurrency safe
  severity: high
  category: authentication-resilience
  applies_when: token cache exists
  evidence_patterns:
  - single-flight
  - atomic
  - invalidate
  finding_when: concurrent refreshes stampede or return divergent tokens
  unknown_evidence_status: not_assessed
  emit_on_failure: true
  quality_guidance: []
- id: APP-STATE-001
  title: Durable workflow state transitions are ordered and observable
  severity: critical
  category: durable-state
  applies_when: workflow status is persisted
  evidence_patterns:
  - INPROCESS
  - FAILED
  - COMPLETED
  finding_when: state changes are fire-and-forget or can reorder
  unknown_evidence_status: not_assessed
  emit_on_failure: true
  quality_guidance: []
- id: APP-STATE-002
  title: Retry exhaustion reaches a durable terminal state
  severity: high
  category: durable-state
  applies_when: retries wrap durable work
  evidence_patterns:
  - doOnError
  - onErrorResume
  - FAILED
  finding_when: retry exhaustion strands records in an intermediate state
  unknown_evidence_status: not_assessed
  emit_on_failure: true
  quality_guidance: []
- id: APP-ASYNC-001
  title: Async infrastructure is explicitly enabled
  severity: high
  category: async-execution
  applies_when: '@Async is used'
  evidence_patterns:
  - '@EnableAsync'
  - '@Configuration'
  - '@Bean name'
  finding_when: async interception or named executor resolution is not established
  unknown_evidence_status: not_assessed
  emit_on_failure: true
  quality_guidance: []
- id: APP-ASYNC-002
  title: Executor capacity, rejection, and blocking behavior are bounded
  severity: high
  category: async-execution
  applies_when: custom executor or scheduler exists
  evidence_patterns:
  - queueCapacity
  - RejectedExecutionHandler
  - Thread.sleep
  - parallelStream
  finding_when: capacity is invalid or work can be silently rejected, blocked, or
    routed to the common pool
  unknown_evidence_status: not_assessed
  emit_on_failure: true
  quality_guidance: []
- id: APP-KAFKA-001
  title: Consumer startup is region-role controlled
  severity: critical
  category: messaging
  applies_when: Kafka consumers exist
  evidence_patterns:
  - autoStartup
  - consumer.autostart
  finding_when: listeners auto-start in multiple regions without ownership
  unknown_evidence_status: not_assessed
  emit_on_failure: true
  quality_guidance: []
- id: APP-KAFKA-002
  title: Consumer acknowledgment follows successful processing
  severity: critical
  category: messaging
  applies_when: Kafka consumers mutate state
  evidence_patterns:
  - AckMode
  - enable.auto.commit
  finding_when: offsets advance before processing succeeds
  unknown_evidence_status: not_assessed
  emit_on_failure: true
  quality_guidance: []
- id: APP-KAFKA-003
  title: Consumer errors have finite retry and dead-letter routing
  severity: high
  category: messaging
  applies_when: Kafka consumers exist
  evidence_patterns:
  - DefaultErrorHandler
  - DeadLetterPublishingRecoverer
  finding_when: poison records retry indefinitely or disappear
  unknown_evidence_status: not_assessed
  emit_on_failure: true
  quality_guidance: []
- id: APP-KAFKA-004
  title: Consumer lag and assignment are observable
  severity: high
  category: messaging
  applies_when: Kafka consumers exist
  evidence_patterns:
  - lag metric
  - assignment
  - paused
  finding_when: consumer degradation is not observable
  unknown_evidence_status: not_assessed
  emit_on_failure: true
  quality_guidance: []
- id: APP-KAFKA-005
  title: Producer delivery is awaited and durable
  severity: critical
  category: messaging
  applies_when: Kafka producer exists
  evidence_patterns:
  - send future
  - acks
  - enable.idempotence
  finding_when: producer result is discarded or durability is absent
  unknown_evidence_status: not_assessed
  emit_on_failure: true
  quality_guidance: []
- id: APP-KAFKA-006
  title: Kafka records carry stable dedupe identity
  severity: high
  category: messaging
  applies_when: Kafka producer exists
  evidence_patterns:
  - message-id
  - event-id
  - RecordHeader
  finding_when: records lack stable identity across retry
  unknown_evidence_status: not_assessed
  emit_on_failure: true
  quality_guidance: []
- id: APP-KAFKA-007
  title: Bound Kafka client properties are applied
  severity: high
  category: messaging
  applies_when: custom Kafka config exists
  evidence_patterns:
  - session.timeout.ms
  - max.poll.interval.ms
  finding_when: declared settings are absent from effective client config
  unknown_evidence_status: not_assessed
  emit_on_failure: true
  quality_guidance: []
- id: APP-CACHE-004
  title: Cache loading coalesces concurrent misses
  severity: high
  category: cache
  applies_when: cache loader calls dependencies
  evidence_patterns:
  - LoadingCache
  - single-flight
  - Mono.cache
  finding_when: cold start causes a stampede
  unknown_evidence_status: not_assessed
  emit_on_failure: true
  quality_guidance: []
- id: APP-CACHE-005
  title: Refresh and warm-up are protected during degradation
  severity: high
  category: cache
  applies_when: refresh or warm-up exists
  evidence_patterns:
  - refreshAfterWrite
  - CircuitBreaker
  finding_when: refresh repeatedly calls a failing dependency
  unknown_evidence_status: not_assessed
  emit_on_failure: true
  quality_guidance: []
- id: APP-CACHE-006
  title: Cache null and stale semantics are explicit
  severity: high
  category: cache
  applies_when: cache stores tokens or remote data
  evidence_patterns:
  - Mono.empty
  - last known good
  finding_when: null results appear successful or stale use exceeds safety window
  unknown_evidence_status: not_assessed
  emit_on_failure: true
  quality_guidance: []
- id: APP-HEALTH-001
  title: Health contributor identifiers are verified
  severity: high
  category: health
  applies_when: custom health groups exist
  evidence_patterns:
  - group.readiness.include
  - validate-group-membership
  finding_when: an unverified contributor ID breaks startup or readiness
  unknown_evidence_status: not_assessed
  emit_on_failure: true
  quality_guidance: []
- id: APP-HEALTH-002
  title: Health state updates after recovery
  severity: high
  category: health
  applies_when: cached health state exists
  evidence_patterns:
  - lastExecutionTime
  - lastSuccess
  finding_when: successful checks do not restore health state
  unknown_evidence_status: not_assessed
  emit_on_failure: true
  quality_guidance: []
- id: APP-API-001
  title: State-changing endpoints use safe methods and authorization
  severity: high
  category: api-security
  applies_when: admin endpoints exist
  evidence_patterns:
  - '@GetMapping'
  - '@PreAuthorize'
  finding_when: GET mutates state or administration lacks authorization
  unknown_evidence_status: not_assessed
  emit_on_failure: true
  quality_guidance: []
- id: APP-SUPPLY-001
  title: Shared dependency upgrades have regression tests
  severity: medium
  category: dependency-governance
  applies_when: parent BOM or shared models exist
  evidence_patterns:
  - parent version
  - dependencyManagement
  finding_when: transitive upgrades can change resilience behavior without tests
  unknown_evidence_status: not_assessed
  emit_on_failure: true
  quality_guidance: []
- id: APP-SUPPLY-002
  title: Runtime base image is immutable
  severity: high
  category: supply-chain
  applies_when: Dockerfile exists
  evidence_patterns:
  - FROM
  - '@sha256'
  finding_when: base image is tag-only
  unknown_evidence_status: not_assessed
  emit_on_failure: true
  quality_guidance: []
- id: APP-OBS-001
  title: Trace export and correlation are operationally complete
  severity: medium
  category: observability
  applies_when: tracing exists
  evidence_patterns:
  - OTLP
  - traceparent
  - exporter
  finding_when: tracing has no exporter or continuity
  unknown_evidence_status: not_assessed
  emit_on_failure: true
  quality_guidance: []
- id: APP-CONF-014
  title: Operationally variable constants are externalized or documented
  severity: low
  category: configuration-hygiene
  applies_when: partner constants exist
  evidence_patterns:
  - TODO hardcode
  - scope constant
  finding_when: a variable contract requires a code release without rationale
  unknown_evidence_status: not_assessed
  emit_on_failure: true
  quality_guidance: []
- id: APP-WORKLOAD-001
  title: Workload failover model matches its execution model
  severity: critical
  category: workload-model
  applies_when: scheduled, polling, batch, or externally triggered work exists
  evidence_patterns:
  - '@Scheduled'
  - CommandLineRunner
  - ApplicationRunner
  - kubectl exec
  - Stonebranch
  finding_when: non-HTTP work is assumed to fail over through traffic routing or can
    execute concurrently in both regions
  unknown_evidence_status: not_assessed
  emit_on_failure: true
  quality_guidance: []
- id: APP-WORKLOAD-002
  title: Single-active workload activation is fail-safe
  severity: critical
  category: workload-model
  applies_when: exactly one region must own work
  evidence_patterns:
  - enabled flag
  - region owner
  - lease
  - epoch
  finding_when: activation defaults enabled, permits split brain, or lacks observable
    ownership
  unknown_evidence_status: not_assessed
  emit_on_failure: true
  quality_guidance: []
- id: APP-SCHED-001
  title: Scheduled work uses distributed ownership
  severity: critical
  category: scheduler
  applies_when: scheduled work processes shared state
  evidence_patterns:
  - '@Scheduled'
  - AtomicBoolean
  - ShedLock
  - leader election
  finding_when: multiple pods or regions can process the same work using only process-local
    coordination
  unknown_evidence_status: not_assessed
  emit_on_failure: true
  quality_guidance: []
- id: APP-SCHED-002
  title: Scheduled reprocessing atomically claims and completes work
  severity: critical
  category: scheduler
  applies_when: reprocessor selects durable records
  evidence_patterns:
  - pickFlag
  - status update
  - lease owner
  - attempt count
  finding_when: selection and claim are non-atomic or completion is not durably verified
  unknown_evidence_status: not_assessed
  emit_on_failure: true
  quality_guidance: []
- id: APP-BATCH-001
  title: Batch exit status reflects terminal completion
  severity: critical
  category: batch
  applies_when: application exits after a run
  evidence_patterns:
  - System.exit
  - exit code
  - subscribe
  finding_when: process exits successfully before work completes or despite failure
  unknown_evidence_status: not_assessed
  emit_on_failure: true
  quality_guidance: []
- id: APP-BATCH-002
  title: Batch runs have durable idempotent run identity
  severity: high
  category: batch
  applies_when: repeatable business runs exist
  evidence_patterns:
  - runId
  - businessDate
  - attempt
  - completion marker
  finding_when: rerun cannot distinguish complete, partial, failed, or duplicate execution
  unknown_evidence_status: not_assessed
  emit_on_failure: true
  quality_guidance: []
- id: APP-BATCH-003
  title: Business output is durable before success
  severity: critical
  category: batch-output
  applies_when: job produces required files or reports
  evidence_patterns:
  - Files.write
  - FileOutputStream
  - /tmp
  - BlobClient
  finding_when: success is reported while output exists only on ephemeral storage
    or before durable upload
  unknown_evidence_status: not_assessed
  emit_on_failure: true
  quality_guidance: []
- id: APP-BATCH-004
  title: Large result sets are streamed or bounded
  severity: high
  category: batch-memory
  applies_when: job reads potentially large results
  evidence_patterns:
  - collectList
  - toList
  - fetchAll
  - page size
  finding_when: unbounded results are accumulated in memory without pagination, streaming,
    or checkpointing
  unknown_evidence_status: not_assessed
  emit_on_failure: true
  quality_guidance: []
- id: APP-FIN-001
  title: Irreversible financial effects follow a durable intent boundary
  severity: critical
  category: financial-integrity
  applies_when: external financial effect occurs
  evidence_patterns:
  - authorize
  - charge
  - credit
  - capture
  - refund
  - void
  finding_when: provider effect can occur before a durable intent and stable operation
    identity exist
  unknown_evidence_status: not_assessed
  emit_on_failure: true
  quality_guidance: []
- id: APP-FIN-002
  title: Partial financial workflows define compensation and reconciliation
  severity: critical
  category: financial-integrity
  applies_when: workflow spans provider and durable stores
  evidence_patterns:
  - compensation
  - reconcile
  - outbox
  - saga
  finding_when: partial success has no compensation or durable reconciliation path
  unknown_evidence_status: not_assessed
  emit_on_failure: true
  quality_guidance: []
- id: APP-FIN-003
  title: Payment identity is stable across retries and regions
  severity: critical
  category: financial-integrity
  applies_when: financial operation can retry
  evidence_patterns:
  - UUID.randomUUID
  - currentTimeMillis
  - idempotency key
  finding_when: each attempt generates a new identity or correlation identity is mistaken
    for idempotency identity
  unknown_evidence_status: not_assessed
  emit_on_failure: true
  quality_guidance: []
- id: APP-FIN-004
  title: Synthetic success is backed by durable recoverable state
  severity: critical
  category: financial-integrity
  applies_when: service can return synthetic or deferred approval
  evidence_patterns:
  - synthetic approved
  - fallback approval
  - accepted
  finding_when: success can be returned before a complete recoverable record is durably
    written
  unknown_evidence_status: not_assessed
  emit_on_failure: true
  quality_guidance: []
- id: APP-DB-001
  title: Reactive database transaction boundaries are effective
  severity: critical
  category: database-consistency
  applies_when: multiple related reactive writes exist
  evidence_patterns:
  - TransactionalOperator
  - ReactiveTransactionManager
  - '@Transactional'
  finding_when: related writes subscribe separately or transaction scope does not
    cover publisher execution
  unknown_evidence_status: not_assessed
  emit_on_failure: true
  quality_guidance: []
- id: APP-DB-003
  title: Cross-store writes have reconciliation
  severity: critical
  category: database-consistency
  applies_when: one operation writes multiple stores
  evidence_patterns:
  - SQL
  - Mongo
  - Cosmos
  - fallback store
  finding_when: stores can diverge without a durable reconciliation marker
  unknown_evidence_status: not_assessed
  emit_on_failure: true
  quality_guidance: []
- id: APP-CORRECT-001
  title: Reactive contracts never return null
  severity: critical
  category: correctness
  applies_when: Mono or Flux is returned
  evidence_patterns:
  - return null
  - Mono.empty
  - Flux.empty
  finding_when: a reactive method or required branch returns null
  unknown_evidence_status: not_assessed
  emit_on_failure: true
  quality_guidance: []
- id: APP-CORRECT-002
  title: Required business-data failures cannot silently default
  severity: critical
  category: correctness
  applies_when: mandatory business data is read
  evidence_patterns:
  - default value
  - return null
  - empty result
  - catch
  finding_when: mandatory data failure becomes null, empty, zero, or success and processing
    continues
  unknown_evidence_status: not_assessed
  emit_on_failure: true
  quality_guidance: []
- id: APP-FALLBACK-001
  title: Fallback paths are independently reliable and observable
  severity: critical
  category: fallback
  applies_when: a primary failure invokes fallback
  evidence_patterns:
  - fallback
  - onErrorResume
  - secondary store
  finding_when: fallback has no bounded completion, dual failure is swallowed, or
    outcomes are indistinguishable
  unknown_evidence_status: not_assessed
  emit_on_failure: true
  quality_guidance: []
- id: APP-OBS-002
  title: Business throughput and stuck work are observable
  severity: high
  category: observability
  applies_when: batch, scheduler, or reprocessor exists
  evidence_patterns:
  - last success
  - backlog age
  - run duration
  - zero throughput
  finding_when: process health can stay UP while business processing stops or records
    remain stuck
  unknown_evidence_status: not_assessed
  emit_on_failure: true
  quality_guidance: []
- id: APP-OBS-003
  title: Correlation propagates across durable and external boundaries
  severity: high
  category: observability
  applies_when: workflow spans dependencies
  evidence_patterns:
  - correlationId
  - provider transaction id
  - traceId
  finding_when: correlation is regenerated or not persisted and propagated
  unknown_evidence_status: not_assessed
  emit_on_failure: true
  quality_guidance: []
- id: APP-ENDPOINT-001
  title: Durable work stores logical destinations, not stale physical endpoints
  severity: high
  category: regional-affinity
  applies_when: durable records contain destination URLs
  evidence_patterns:
  - url field
  - endpoint field
  - baseUrl
  finding_when: reprocessing uses a stored region-specific physical endpoint instead
    of current logical service identity
  unknown_evidence_status: not_assessed
  emit_on_failure: true
  quality_guidance: []
- id: APP-PROC-001
  title: Required companion processes participate in health and lifecycle
  severity: high
  category: process-model
  applies_when: container runs multiple required processes
  evidence_patterns:
  - supervisor
  - ProcessBuilder
  - side process
  - proxy process
  finding_when: a required process can fail while application readiness remains UP
    or shutdown signals are not coordinated
  unknown_evidence_status: not_assessed
  emit_on_failure: true
  quality_guidance: []
---

# Spring Boot on AKS Active-Active Code Assessment Standard v4

## Purpose

This master retains the v3 control set and adds workload-model, scheduler, batch, financial-integrity, cross-store, fallback, correctness, business-observability, durable-destination, and companion-process controls derived from the reviewed OSPG and OCSE reports.

## Global quality caveats

1. Adding @Transactional is not sufficient for reactive work; verify ReactiveTransactionManager or TransactionalOperator and one composed subscription boundary.
2. Do not place every dependency in readiness. Gate on critical region-local serving dependencies only; a globally shared dependency can drain all regions simultaneously.
3. A timestamp or random UUID generated per attempt is correlation, not a stable idempotency key.
4. Do not retry a non-idempotent operation after an ambiguous completion unless provider idempotency or reconciliation makes it safe.
5. A feature flag alone is not a distributed single-active guarantee. Require fail-safe defaults, observable ownership, and split-brain detection; prefer a lease or atomic ownership token when concurrent activation is possible.
6. A fallback store or service is not resilient when its write is detached, unbounded, or unobservable. Evaluate primary failure, fallback success, and dual failure separately.
7. External dependencies must not be coupled to liveness.
8. Durable work should store a logical destination and resolve the current regional endpoint at execution time; preserve the original physical endpoint only for audit.
9. Do not prescribe numeric retry, timeout, pool, or circuit-breaker values without workload evidence. Require external configurability and budget alignment.
10. Do not infer deployed infrastructure noncompliance from absent repository evidence. Use not_assessed or external evidence required.

## Evaluator workflow

1. Load this master for every Spring Boot assessment.
2. Classify the workload as API, event consumer, scheduler, batch, or hybrid before applying controls.
3. Load only dependency standards selected by inventory.
4. Evaluate applicable controls using repository evidence.
5. Return `not_assessed` for absent external evidence.
6. Deduplicate findings by root cause.
7. Suppress deployment, infrastructure, and PCF findings.

# Controls

## APP-AA-001: One immutable artifact supports both regions

**Severity:** High  
**Category:** deployability  
**Applies when:** always

### Requirement

The implementation must satisfy this behavior when the same artifact runs in either regional deployment or under its approved active-passive ownership model.

### Evidence to inspect

- `profiles`
- `artifact`
- `Dockerfile`

### Finding condition

Emit a finding when repository evidence demonstrates that region-specific code or artifact is required.

### Quality guidance

- Apply the global quality caveats and evidence-only rules.

### Evaluation constraints

- Cite the exact file, symbol or property, and line range.
- Evaluate effective behavior, not the presence of a library or annotation.
- Return `not_assessed` when evidence is insufficient.
- Deduplicate overlapping controls under one root-cause finding.
- Do not create deployment, infrastructure, or PCF findings from this master.

---

## APP-AA-002: Regional endpoints are externally configured

**Severity:** Critical  
**Category:** configuration  
**Applies when:** remote dependencies exist

### Requirement

The implementation must satisfy this behavior when the same artifact runs in either regional deployment or under its approved active-passive ownership model.

### Evidence to inspect

- `application.yml`
- `@ConfigurationProperties`
- `baseUrl`

### Finding condition

Emit a finding when repository evidence demonstrates that a regional endpoint or physical hostname is hardcoded.

### Quality guidance

- Apply the global quality caveats and evidence-only rules.

### Evaluation constraints

- Cite the exact file, symbol or property, and line range.
- Evaluate effective behavior, not the presence of a library or annotation.
- Return `not_assessed` when evidence is insufficient.
- Deduplicate overlapping controls under one root-cause finding.
- Do not create deployment, infrastructure, or PCF findings from this master.

---

## APP-AA-003: Local-region dependency affinity is explicit

**Severity:** Critical  
**Category:** regional-affinity  
**Applies when:** regional dependencies exist

### Requirement

The implementation must satisfy this behavior when the same artifact runs in either regional deployment or under its approved active-passive ownership model.

### Evidence to inspect

- `region property`
- `endpoint mapping`

### Finding condition

Emit a finding when repository evidence demonstrates that normal operation can use a remote-region dependency without an explicit policy.

### Quality guidance

- Apply the global quality caveats and evidence-only rules.

### Evaluation constraints

- Cite the exact file, symbol or property, and line range.
- Evaluate effective behavior, not the presence of a library or annotation.
- Return `not_assessed` when evidence is insufficient.
- Deduplicate overlapping controls under one root-cause finding.
- Do not create deployment, infrastructure, or PCF findings from this master.

---

## APP-AA-004: Dependency calls have bounded timeouts

**Severity:** Critical  
**Category:** resilience  
**Applies when:** remote calls exist

### Requirement

The implementation must satisfy this behavior when the same artifact runs in either regional deployment or under its approved active-passive ownership model.

### Evidence to inspect

- `connect timeout`
- `response timeout`
- `.timeout(`
- `query timeout`

### Finding condition

Emit a finding when repository evidence demonstrates that a remote call can exceed the end-to-end failure budget.

### Quality guidance

- Apply the global quality caveats and evidence-only rules.

### Evaluation constraints

- Cite the exact file, symbol or property, and line range.
- Evaluate effective behavior, not the presence of a library or annotation.
- Return `not_assessed` when evidence is insufficient.
- Deduplicate overlapping controls under one root-cause finding.
- Do not create deployment, infrastructure, or PCF findings from this master.

---

## APP-AA-005: Transient failures use bounded retry with backoff

**Severity:** High  
**Category:** resilience  
**Applies when:** retryable calls exist

### Requirement

The implementation must satisfy this behavior when the same artifact runs in either regional deployment or under its approved active-passive ownership model.

### Evidence to inspect

- `Retry.backoff`
- `@Retryable`
- `RetryOptions`

### Finding condition

Emit a finding when repository evidence demonstrates that retry is absent, unbounded, or applies to terminal or ambiguous operations without safety.

### Quality guidance

- Apply the global quality caveats and evidence-only rules.

### Evaluation constraints

- Cite the exact file, symbol or property, and line range.
- Evaluate effective behavior, not the presence of a library or annotation.
- Return `not_assessed` when evidence is insufficient.
- Deduplicate overlapping controls under one root-cause finding.
- Do not create deployment, infrastructure, or PCF findings from this master.

---

## APP-AA-006: Repeated failures are isolated

**Severity:** High  
**Category:** resilience  
**Applies when:** remote calls exist

### Requirement

The implementation must satisfy this behavior when the same artifact runs in either regional deployment or under its approved active-passive ownership model.

### Evidence to inspect

- `CircuitBreaker`
- `Bulkhead`
- `connection pool`

### Finding condition

Emit a finding when repository evidence demonstrates that one dependency can exhaust shared resources.

### Quality guidance

- Apply the global quality caveats and evidence-only rules.

### Evaluation constraints

- Cite the exact file, symbol or property, and line range.
- Evaluate effective behavior, not the presence of a library or annotation.
- Return `not_assessed` when evidence is insufficient.
- Deduplicate overlapping controls under one root-cause finding.
- Do not create deployment, infrastructure, or PCF findings from this master.

---

## APP-AA-007: Critical regional dependency failure affects readiness

**Severity:** Critical  
**Category:** health  
**Applies when:** critical regional dependency exists

### Requirement

The implementation must satisfy this behavior when the same artifact runs in either regional deployment or under its approved active-passive ownership model.

### Evidence to inspect

- `HealthIndicator`
- `readiness group`

### Finding condition

Emit a finding when repository evidence demonstrates that a critical region-local dependency remains failed while readiness is UP.

### Quality guidance

- Apply the global quality caveats and evidence-only rules.

### Evaluation constraints

- Cite the exact file, symbol or property, and line range.
- Evaluate effective behavior, not the presence of a library or annotation.
- Return `not_assessed` when evidence is insufficient.
- Deduplicate overlapping controls under one root-cause finding.
- Do not create deployment, infrastructure, or PCF findings from this master.

---

## APP-AA-008: Liveness excludes external dependencies

**Severity:** Critical  
**Category:** health  
**Applies when:** Actuator probes exist

### Requirement

The implementation must satisfy this behavior when the same artifact runs in either regional deployment or under its approved active-passive ownership model.

### Evidence to inspect

- `liveness group`
- `livenessState`

### Finding condition

Emit a finding when repository evidence demonstrates that external failure causes liveness failure or restart loops.

### Quality guidance

- Apply the global quality caveats and evidence-only rules.

### Evaluation constraints

- Cite the exact file, symbol or property, and line range.
- Evaluate effective behavior, not the presence of a library or annotation.
- Return `not_assessed` when evidence is insufficient.
- Deduplicate overlapping controls under one root-cause finding.
- Do not create deployment, infrastructure, or PCF findings from this master.

---

## APP-AA-009: Health checks are bounded and representative

**Severity:** High  
**Category:** health  
**Applies when:** health contributors exist

### Requirement

The implementation must satisfy this behavior when the same artifact runs in either regional deployment or under its approved active-passive ownership model.

### Evidence to inspect

- `health timeout`
- `synthetic check`

### Finding condition

Emit a finding when repository evidence demonstrates that health can hang, overload a dependency, or bypass the serving path.

### Quality guidance

- Apply the global quality caveats and evidence-only rules.

### Evaluation constraints

- Cite the exact file, symbol or property, and line range.
- Evaluate effective behavior, not the presence of a library or annotation.
- Return `not_assessed` when evidence is insufficient.
- Deduplicate overlapping controls under one root-cause finding.
- Do not create deployment, infrastructure, or PCF findings from this master.

---

## APP-AA-010: Application state is region independent

**Severity:** Critical  
**Category:** state  
**Applies when:** stateful behavior exists

### Requirement

The implementation must satisfy this behavior when the same artifact runs in either regional deployment or under its approved active-passive ownership model.

### Evidence to inspect

- `session`
- `local file`
- `in-memory state`

### Finding condition

Emit a finding when repository evidence demonstrates that required state is pod-local or region-local.

### Quality guidance

- Apply the global quality caveats and evidence-only rules.

### Evaluation constraints

- Cite the exact file, symbol or property, and line range.
- Evaluate effective behavior, not the presence of a library or annotation.
- Return `not_assessed` when evidence is insufficient.
- Deduplicate overlapping controls under one root-cause finding.
- Do not create deployment, infrastructure, or PCF findings from this master.

---

## APP-AA-011: Mutating operations are idempotent

**Severity:** Critical  
**Category:** consistency  
**Applies when:** mutating operations exist

### Requirement

The implementation must satisfy this behavior when the same artifact runs in either regional deployment or under its approved active-passive ownership model.

### Evidence to inspect

- `idempotency key`
- `dedupe`
- `unique index`

### Finding condition

Emit a finding when repository evidence demonstrates that retry or replay can duplicate business effects.

### Quality guidance

- Apply the global quality caveats and evidence-only rules.

### Evaluation constraints

- Cite the exact file, symbol or property, and line range.
- Evaluate effective behavior, not the presence of a library or annotation.
- Return `not_assessed` when evidence is insufficient.
- Deduplicate overlapping controls under one root-cause finding.
- Do not create deployment, infrastructure, or PCF findings from this master.

---

## APP-AA-012: Concurrency and conflict behavior is defined

**Severity:** High  
**Category:** consistency  
**Applies when:** concurrent writes are possible

### Requirement

The implementation must satisfy this behavior when the same artifact runs in either regional deployment or under its approved active-passive ownership model.

### Evidence to inspect

- `@Version`
- `ETag`
- `rowversion`

### Finding condition

Emit a finding when repository evidence demonstrates that concurrent writes can silently overwrite state.

### Quality guidance

- Apply the global quality caveats and evidence-only rules.

### Evaluation constraints

- Cite the exact file, symbol or property, and line range.
- Evaluate effective behavior, not the presence of a library or annotation.
- Return `not_assessed` when evidence is insufficient.
- Deduplicate overlapping controls under one root-cause finding.
- Do not create deployment, infrastructure, or PCF findings from this master.

---

## APP-AA-013: Startup tolerates temporary dependency unavailability

**Severity:** High  
**Category:** startup  
**Applies when:** startup dependencies exist

### Requirement

The implementation must satisfy this behavior when the same artifact runs in either regional deployment or under its approved active-passive ownership model.

### Evidence to inspect

- `fail-fast`
- `startup retry`
- `readiness`

### Finding condition

Emit a finding when repository evidence demonstrates that temporary outage causes uncontrolled or unbounded startup failure.

### Quality guidance

- Apply the global quality caveats and evidence-only rules.

### Evaluation constraints

- Cite the exact file, symbol or property, and line range.
- Evaluate effective behavior, not the presence of a library or annotation.
- Return `not_assessed` when evidence is insufficient.
- Deduplicate overlapping controls under one root-cause finding.
- Do not create deployment, infrastructure, or PCF findings from this master.

---

## APP-AA-014: Dependency recovery occurs without restart

**Severity:** High  
**Category:** recovery  
**Applies when:** remote clients exist

### Requirement

The implementation must satisfy this behavior when the same artifact runs in either regional deployment or under its approved active-passive ownership model.

### Evidence to inspect

- `reconnect`
- `credential refresh`
- `half-open`

### Finding condition

Emit a finding when repository evidence demonstrates that recovery requires process restart.

### Quality guidance

- Apply the global quality caveats and evidence-only rules.

### Evaluation constraints

- Cite the exact file, symbol or property, and line range.
- Evaluate effective behavior, not the presence of a library or annotation.
- Return `not_assessed` when evidence is insufficient.
- Deduplicate overlapping controls under one root-cause finding.
- Do not create deployment, infrastructure, or PCF findings from this master.

---

## APP-AA-015: Regional identity is present in telemetry

**Severity:** Medium  
**Category:** observability  
**Applies when:** telemetry exists

### Requirement

The implementation must satisfy this behavior when the same artifact runs in either regional deployment or under its approved active-passive ownership model.

### Evidence to inspect

- `region tag`
- `cluster tag`

### Finding condition

Emit a finding when repository evidence demonstrates that telemetry cannot identify the serving region.

### Quality guidance

- Apply the global quality caveats and evidence-only rules.

### Evaluation constraints

- Cite the exact file, symbol or property, and line range.
- Evaluate effective behavior, not the presence of a library or annotation.
- Return `not_assessed` when evidence is insufficient.
- Deduplicate overlapping controls under one root-cause finding.
- Do not create deployment, infrastructure, or PCF findings from this master.

---

## APP-AA-016: Failures generate actionable signals

**Severity:** Critical  
**Category:** observability  
**Applies when:** critical dependencies exist

### Requirement

The implementation must satisfy this behavior when the same artifact runs in either regional deployment or under its approved active-passive ownership model.

### Evidence to inspect

- `metrics`
- `structured logs`
- `retry exhausted`

### Finding condition

Emit a finding when repository evidence demonstrates that critical failure or recovery is not observable.

### Quality guidance

- Apply the global quality caveats and evidence-only rules.

### Evaluation constraints

- Cite the exact file, symbol or property, and line range.
- Evaluate effective behavior, not the presence of a library or annotation.
- Return `not_assessed` when evidence is insufficient.
- Deduplicate overlapping controls under one root-cause finding.
- Do not create deployment, infrastructure, or PCF findings from this master.

---

## APP-AA-017: Graceful shutdown and traffic draining are implemented

**Severity:** High  
**Category:** lifecycle  
**Applies when:** service receives traffic or processes work

### Requirement

The implementation must satisfy this behavior when the same artifact runs in either regional deployment or under its approved active-passive ownership model.

### Evidence to inspect

- `graceful shutdown`
- `readiness transition`

### Finding condition

Emit a finding when repository evidence demonstrates that termination accepts new work or loses in-flight work.

### Quality guidance

- Apply the global quality caveats and evidence-only rules.

### Evaluation constraints

- Cite the exact file, symbol or property, and line range.
- Evaluate effective behavior, not the presence of a library or annotation.
- Return `not_assessed` when evidence is insufficient.
- Deduplicate overlapping controls under one root-cause finding.
- Do not create deployment, infrastructure, or PCF findings from this master.

---

## APP-AA-018: Failure behavior is tested

**Severity:** Critical  
**Category:** testing  
**Applies when:** always

### Requirement

The implementation must satisfy this behavior when the same artifact runs in either regional deployment or under its approved active-passive ownership model.

### Evidence to inspect

- `fault test`
- `integration test`

### Finding condition

Emit a finding when repository evidence demonstrates that tests do not prove timeout, retry, health transition, idempotency, shutdown, and recovery behavior.

### Quality guidance

- Apply the global quality caveats and evidence-only rules.

### Evaluation constraints

- Cite the exact file, symbol or property, and line range.
- Evaluate effective behavior, not the presence of a library or annotation.
- Return `not_assessed` when evidence is insufficient.
- Deduplicate overlapping controls under one root-cause finding.
- Do not create deployment, infrastructure, or PCF findings from this master.

---

## APP-DISC-001: Discovery endpoint and regional selection are configurable

**Severity:** Critical  
**Category:** service-discovery  
**Applies when:** DiscoveryClient is used

### Requirement

The implementation must satisfy this behavior when the same artifact runs in either regional deployment or under its approved active-passive ownership model.

### Evidence to inspect

- `@EnableDiscoveryClient`
- `registry endpoint`

### Finding condition

Emit a finding when repository evidence demonstrates that discovery endpoint or region is hardcoded.

### Quality guidance

- Apply the global quality caveats and evidence-only rules.

### Evaluation constraints

- Cite the exact file, symbol or property, and line range.
- Evaluate effective behavior, not the presence of a library or annotation.
- Return `not_assessed` when evidence is insufficient.
- Deduplicate overlapping controls under one root-cause finding.
- Do not create deployment, infrastructure, or PCF findings from this master.

---

## APP-DISC-002: Critical discovery state participates in readiness

**Severity:** High  
**Category:** service-discovery  
**Applies when:** discovery is critical

### Requirement

The implementation must satisfy this behavior when the same artifact runs in either regional deployment or under its approved active-passive ownership model.

### Evidence to inspect

- `DiscoveryClientHealthIndicator`
- `readiness`

### Finding condition

Emit a finding when repository evidence demonstrates that critical registration or lookup failure leaves readiness UP.

### Quality guidance

- Apply the global quality caveats and evidence-only rules.

### Evaluation constraints

- Cite the exact file, symbol or property, and line range.
- Evaluate effective behavior, not the presence of a library or annotation.
- Return `not_assessed` when evidence is insufficient.
- Deduplicate overlapping controls under one root-cause finding.
- Do not create deployment, infrastructure, or PCF findings from this master.

---

## APP-CONF-010: Runtime refresh behavior is defined and safe

**Severity:** High  
**Category:** configuration  
**Applies when:** dynamic refresh is enabled or expected

### Requirement

The implementation must satisfy this behavior when the same artifact runs in either regional deployment or under its approved active-passive ownership model.

### Evidence to inspect

- `@RefreshScope`
- `EnvironmentChangeEvent`

### Finding condition

Emit a finding when repository evidence demonstrates that refreshed values do not safely affect initialized clients, pools, executors, or caches.

### Quality guidance

- Apply the global quality caveats and evidence-only rules.

### Evaluation constraints

- Cite the exact file, symbol or property, and line range.
- Evaluate effective behavior, not the presence of a library or annotation.
- Return `not_assessed` when evidence is insufficient.
- Deduplicate overlapping controls under one root-cause finding.
- Do not create deployment, infrastructure, or PCF findings from this master.

---

## APP-REACT-001: Reactive side effects execute once

**Severity:** Critical  
**Category:** reactive  
**Applies when:** Reactor side effects exist

### Requirement

The implementation must satisfy this behavior when the same artifact runs in either regional deployment or under its approved active-passive ownership model.

### Evidence to inspect

- `Mono.defer`
- `cache()`
- `subscribe`

### Finding condition

Emit a finding when repository evidence demonstrates that a cold publisher can be subscribed more than once and repeat a side effect.

### Quality guidance

- Apply the global quality caveats and evidence-only rules.

### Evaluation constraints

- Cite the exact file, symbol or property, and line range.
- Evaluate effective behavior, not the presence of a library or annotation.
- Return `not_assessed` when evidence is insufficient.
- Deduplicate overlapping controls under one root-cause finding.
- Do not create deployment, infrastructure, or PCF findings from this master.

---

## APP-REACT-002: Reactive business chains avoid detached subscriptions

**Severity:** Critical  
**Category:** reactive  
**Applies when:** Reactor is used

### Requirement

The implementation must satisfy this behavior when the same artifact runs in either regional deployment or under its approved active-passive ownership model.

### Evidence to inspect

- `.subscribe()`
- `void service method`

### Finding condition

Emit a finding when repository evidence demonstrates that business work is detached from caller-visible completion or error.

### Quality guidance

- Apply the global quality caveats and evidence-only rules.

### Evaluation constraints

- Cite the exact file, symbol or property, and line range.
- Evaluate effective behavior, not the presence of a library or annotation.
- Return `not_assessed` when evidence is insufficient.
- Deduplicate overlapping controls under one root-cause finding.
- Do not create deployment, infrastructure, or PCF findings from this master.

---

## APP-REACT-003: Reactive error handling preserves failure semantics

**Severity:** High  
**Category:** reactive  
**Applies when:** Reactor is used

### Requirement

The implementation must satisfy this behavior when the same artifact runs in either regional deployment or under its approved active-passive ownership model.

### Evidence to inspect

- `onErrorResume`
- `switchIfEmpty`

### Finding condition

Emit a finding when repository evidence demonstrates that dependency failures become empty, not-found, or success.

### Quality guidance

- Apply the global quality caveats and evidence-only rules.

### Evaluation constraints

- Cite the exact file, symbol or property, and line range.
- Evaluate effective behavior, not the presence of a library or annotation.
- Return `not_assessed` when evidence is insufficient.
- Deduplicate overlapping controls under one root-cause finding.
- Do not create deployment, infrastructure, or PCF findings from this master.

---

## APP-CACHE-001: Cache TTL and refresh intervals are configurable

**Severity:** Medium  
**Category:** cache  
**Applies when:** application cache exists

### Requirement

The implementation must satisfy this behavior when the same artifact runs in either regional deployment or under its approved active-passive ownership model.

### Evidence to inspect

- `expireAfterWrite`
- `refreshAfterWrite`

### Finding condition

Emit a finding when repository evidence demonstrates that TTL or refresh is an unexplained literal.

### Quality guidance

- Apply the global quality caveats and evidence-only rules.

### Evaluation constraints

- Cite the exact file, symbol or property, and line range.
- Evaluate effective behavior, not the presence of a library or annotation.
- Return `not_assessed` when evidence is insufficient.
- Deduplicate overlapping controls under one root-cause finding.
- Do not create deployment, infrastructure, or PCF findings from this master.

---

## APP-CACHE-002: Cache size and eviction are configurable and bounded

**Severity:** High  
**Category:** cache  
**Applies when:** application cache exists

### Requirement

The implementation must satisfy this behavior when the same artifact runs in either regional deployment or under its approved active-passive ownership model.

### Evidence to inspect

- `maximumSize`
- `maximumWeight`

### Finding condition

Emit a finding when repository evidence demonstrates that cache is unbounded or non-tunable.

### Quality guidance

- Apply the global quality caveats and evidence-only rules.

### Evaluation constraints

- Cite the exact file, symbol or property, and line range.
- Evaluate effective behavior, not the presence of a library or annotation.
- Return `not_assessed` when evidence is insufficient.
- Deduplicate overlapping controls under one root-cause finding.
- Do not create deployment, infrastructure, or PCF findings from this master.

---

## APP-CACHE-003: Cache contents do not create regional correctness dependency

**Severity:** High  
**Category:** cache  
**Applies when:** application cache exists

### Requirement

The implementation must satisfy this behavior when the same artifact runs in either regional deployment or under its approved active-passive ownership model.

### Evidence to inspect

- `cache key`
- `invalidation`

### Finding condition

Emit a finding when repository evidence demonstrates that pod-local cache is required for correctness or session continuity.

### Quality guidance

- Apply the global quality caveats and evidence-only rules.

### Evaluation constraints

- Cite the exact file, symbol or property, and line range.
- Evaluate effective behavior, not the presence of a library or annotation.
- Return `not_assessed` when evidence is insufficient.
- Deduplicate overlapping controls under one root-cause finding.
- Do not create deployment, infrastructure, or PCF findings from this master.

---

## APP-ACT-001: Actuator exposure is minimized

**Severity:** High  
**Category:** management-security  
**Applies when:** Actuator is used

### Requirement

The implementation must satisfy this behavior when the same artifact runs in either regional deployment or under its approved active-passive ownership model.

### Evidence to inspect

- `exposure.include`
- `env`
- `heapdump`
- `loggers`

### Finding condition

Emit a finding when repository evidence demonstrates that unnecessary diagnostic or administrative endpoints are exposed.

### Quality guidance

- Apply the global quality caveats and evidence-only rules.

### Evaluation constraints

- Cite the exact file, symbol or property, and line range.
- Evaluate effective behavior, not the presence of a library or annotation.
- Return `not_assessed` when evidence is insufficient.
- Deduplicate overlapping controls under one root-cause finding.
- Do not create deployment, infrastructure, or PCF findings from this master.

---

## APP-ACT-002: Sensitive Actuator endpoints are protected

**Severity:** Critical  
**Category:** management-security  
**Applies when:** sensitive endpoints are exposed

### Requirement

The implementation must satisfy this behavior when the same artifact runs in either regional deployment or under its approved active-passive ownership model.

### Evidence to inspect

- `SecurityFilterChain`
- `EndpointRequest`

### Finding condition

Emit a finding when repository evidence demonstrates that sensitive endpoints lack authentication or isolation.

### Quality guidance

- Apply the global quality caveats and evidence-only rules.

### Evaluation constraints

- Cite the exact file, symbol or property, and line range.
- Evaluate effective behavior, not the presence of a library or annotation.
- Return `not_assessed` when evidence is insufficient.
- Deduplicate overlapping controls under one root-cause finding.
- Do not create deployment, infrastructure, or PCF findings from this master.

---

## APP-ACT-003: Health details avoid sensitive disclosure

**Severity:** Medium  
**Category:** management-security  
**Applies when:** health endpoint is exposed

### Requirement

The implementation must satisfy this behavior when the same artifact runs in either regional deployment or under its approved active-passive ownership model.

### Evidence to inspect

- `show-details`
- `show-components`

### Finding condition

Emit a finding when repository evidence demonstrates that untrusted callers can see sensitive topology or errors.

### Quality guidance

- Apply the global quality caveats and evidence-only rules.

### Evaluation constraints

- Cite the exact file, symbol or property, and line range.
- Evaluate effective behavior, not the presence of a library or annotation.
- Return `not_assessed` when evidence is insufficient.
- Deduplicate overlapping controls under one root-cause finding.
- Do not create deployment, infrastructure, or PCF findings from this master.

---

## APP-LOG-001: Credentials and sensitive payment data are not logged

**Severity:** Critical  
**Category:** logging-security  
**Applies when:** sensitive values exist

### Requirement

The implementation must satisfy this behavior when the same artifact runs in either regional deployment or under its approved active-passive ownership model.

### Evidence to inspect

- `Authorization`
- `clientSecret`
- `PAN`
- `HMAC`
- `APIM key`
- `request body`

### Finding condition

Emit a finding when repository evidence demonstrates that secrets, credentials, PCI/PII, signed headers, payment data, or connection strings can be logged.

### Quality guidance

- Apply the global quality caveats and evidence-only rules.

### Evaluation constraints

- Cite the exact file, symbol or property, and line range.
- Evaluate effective behavior, not the presence of a library or annotation.
- Return `not_assessed` when evidence is insufficient.
- Deduplicate overlapping controls under one root-cause finding.
- Do not create deployment, infrastructure, or PCF findings from this master.

---

## APP-LOG-002: Sensitive objects are masked during serialization

**Severity:** High  
**Category:** logging-security  
**Applies when:** sensitive configuration objects exist

### Requirement

The implementation must satisfy this behavior when the same artifact runs in either regional deployment or under its approved active-passive ownership model.

### Evidence to inspect

- `@ToString`
- `ToString.Exclude`
- `redact`

### Finding condition

Emit a finding when repository evidence demonstrates that generated or structured serialization exposes sensitive fields.

### Quality guidance

- Apply the global quality caveats and evidence-only rules.

### Evaluation constraints

- Cite the exact file, symbol or property, and line range.
- Evaluate effective behavior, not the presence of a library or annotation.
- Return `not_assessed` when evidence is insufficient.
- Deduplicate overlapping controls under one root-cause finding.
- Do not create deployment, infrastructure, or PCF findings from this master.

---

## APP-WEB-001: Exception advice matches servlet or reactive model

**Severity:** High  
**Category:** web-error-handling  
**Applies when:** web endpoints exist

### Requirement

The implementation must satisfy this behavior when the same artifact runs in either regional deployment or under its approved active-passive ownership model.

### Evidence to inspect

- `@ControllerAdvice`
- `ErrorWebExceptionHandler`
- `WebFlux`

### Finding condition

Emit a finding when repository evidence demonstrates that handler model or precedence leaves reactive or servlet errors unmapped.

### Quality guidance

- Apply the global quality caveats and evidence-only rules.

### Evaluation constraints

- Cite the exact file, symbol or property, and line range.
- Evaluate effective behavior, not the presence of a library or annotation.
- Return `not_assessed` when evidence is insufficient.
- Deduplicate overlapping controls under one root-cause finding.
- Do not create deployment, infrastructure, or PCF findings from this master.

---

## APP-WEB-002: Dependency failures map to stable caller-visible semantics

**Severity:** High  
**Category:** web-error-handling  
**Applies when:** API exists

### Requirement

The implementation must satisfy this behavior when the same artifact runs in either regional deployment or under its approved active-passive ownership model.

### Evidence to inspect

- `503`
- `ProblemDetail`
- `onErrorMap`

### Finding condition

Emit a finding when repository evidence demonstrates that dependency failure returns success, not-found, null, or an inconsistent status.

### Quality guidance

- Apply the global quality caveats and evidence-only rules.

### Evaluation constraints

- Cite the exact file, symbol or property, and line range.
- Evaluate effective behavior, not the presence of a library or annotation.
- Return `not_assessed` when evidence is insufficient.
- Deduplicate overlapping controls under one root-cause finding.
- Do not create deployment, infrastructure, or PCF findings from this master.

---

## APP-CONF-011: Spring Cloud Config bootstrap has bounded fail-fast behavior

**Severity:** Critical  
**Category:** configuration-bootstrap  
**Applies when:** Config Client is used

### Requirement

The implementation must satisfy this behavior when the same artifact runs in either regional deployment or under its approved active-passive ownership model.

### Evidence to inspect

- `fail-fast`
- `spring.cloud.config.retry`
- `request-connect-timeout`

### Finding condition

Emit a finding when repository evidence demonstrates that bootstrap uses a regional default or lacks bounded fail-fast, retry, and per-attempt timeouts.

### Quality guidance

- Apply the global quality caveats and evidence-only rules.

### Evaluation constraints

- Cite the exact file, symbol or property, and line range.
- Evaluate effective behavior, not the presence of a library or annotation.
- Return `not_assessed` when evidence is insufficient.
- Deduplicate overlapping controls under one root-cause finding.
- Do not create deployment, infrastructure, or PCF findings from this master.

---

## APP-CONF-012: Required configuration properties have validated invariants

**Severity:** High  
**Category:** configuration-bootstrap  
**Applies when:** external configuration is bound

### Requirement

The implementation must satisfy this behavior when the same artifact runs in either regional deployment or under its approved active-passive ownership model.

### Evidence to inspect

- `@Validated`
- `@NotNull`
- `@Min`

### Finding condition

Emit a finding when repository evidence demonstrates that invalid external values can reach initialized clients or executors.

### Quality guidance

- Apply the global quality caveats and evidence-only rules.

### Evaluation constraints

- Cite the exact file, symbol or property, and line range.
- Evaluate effective behavior, not the presence of a library or annotation.
- Return `not_assessed` when evidence is insufficient.
- Deduplicate overlapping controls under one root-cause finding.
- Do not create deployment, infrastructure, or PCF findings from this master.

---

## APP-CONF-013: Bound resiliency properties are actually consumed

**Severity:** High  
**Category:** configuration  
**Applies when:** configuration properties exist

### Requirement

The implementation must satisfy this behavior when the same artifact runs in either regional deployment or under its approved active-passive ownership model.

### Evidence to inspect

- `getter usage`
- `retryBackoffMaxDuration`
- `sessionTimeout`

### Finding condition

Emit a finding when repository evidence demonstrates that a declared resiliency property is never applied.

### Quality guidance

- Apply the global quality caveats and evidence-only rules.

### Evaluation constraints

- Cite the exact file, symbol or property, and line range.
- Evaluate effective behavior, not the presence of a library or annotation.
- Return `not_assessed` when evidence is insufficient.
- Deduplicate overlapping controls under one root-cause finding.
- Do not create deployment, infrastructure, or PCF findings from this master.

---

## APP-HTTP-001: Blocking dependency and SDK calls are isolated

**Severity:** Critical  
**Category:** dependency-client  
**Applies when:** reactive or shared-thread runtime is used

### Requirement

The implementation must satisfy this behavior when the same artifact runs in either regional deployment or under its approved active-passive ownership model.

### Evidence to inspect

- `.block(`
- `RestTemplate`
- `vendor SDK`
- `boundedElastic`

### Finding condition

Emit a finding when repository evidence demonstrates that blocking calls execute on event-loop, health, or shared executor threads.

### Quality guidance

- Apply the global quality caveats and evidence-only rules.

### Evaluation constraints

- Cite the exact file, symbol or property, and line range.
- Evaluate effective behavior, not the presence of a library or annotation.
- Return `not_assessed` when evidence is insufficient.
- Deduplicate overlapping controls under one root-cause finding.
- Do not create deployment, infrastructure, or PCF findings from this master.

---

## APP-HTTP-002: Dependencies use isolated client pools and timeout profiles

**Severity:** High  
**Category:** http-client  
**Applies when:** multiple downstream hosts exist

### Requirement

The implementation must satisfy this behavior when the same artifact runs in either regional deployment or under its approved active-passive ownership model.

### Evidence to inspect

- `ConnectionProvider`
- `WebClient.Builder`
- `responseTimeout`

### Finding condition

Emit a finding when repository evidence demonstrates that unrelated dependencies share one pool and timeout profile.

### Quality guidance

- Apply the global quality caveats and evidence-only rules.

### Evaluation constraints

- Cite the exact file, symbol or property, and line range.
- Evaluate effective behavior, not the presence of a library or annotation.
- Return `not_assessed` when evidence is insufficient.
- Deduplicate overlapping controls under one root-cause finding.
- Do not create deployment, infrastructure, or PCF findings from this master.

---

## APP-HTTP-003: Retry classification covers transient conditions and server guidance

**Severity:** High  
**Category:** http-client  
**Applies when:** HTTP retry exists

### Requirement

The implementation must satisfy this behavior when the same artifact runs in either regional deployment or under its approved active-passive ownership model.

### Evidence to inspect

- `Retry-After`
- `429`
- `5xx`
- `ReadTimeoutException`

### Finding condition

Emit a finding when repository evidence demonstrates that retry classification is unsafe or ignores server guidance.

### Quality guidance

- Apply the global quality caveats and evidence-only rules.

### Evaluation constraints

- Cite the exact file, symbol or property, and line range.
- Evaluate effective behavior, not the presence of a library or annotation.
- Return `not_assessed` when evidence is insufficient.
- Deduplicate overlapping controls under one root-cause finding.
- Do not create deployment, infrastructure, or PCF findings from this master.

---

## APP-HTTP-004: Authentication recovery is sequenced inside retry

**Severity:** High  
**Category:** http-client  
**Applies when:** token-authenticated calls exist

### Requirement

The implementation must satisfy this behavior when the same artifact runs in either regional deployment or under its approved active-passive ownership model.

### Evidence to inspect

- `401`
- `invalidate token`
- `onErrorResume`

### Finding condition

Emit a finding when repository evidence demonstrates that credential refresh is detached or repeats stale credentials.

### Quality guidance

- Apply the global quality caveats and evidence-only rules.

### Evaluation constraints

- Cite the exact file, symbol or property, and line range.
- Evaluate effective behavior, not the presence of a library or annotation.
- Return `not_assessed` when evidence is insufficient.
- Deduplicate overlapping controls under one root-cause finding.
- Do not create deployment, infrastructure, or PCF findings from this master.

---

## APP-HTTP-005: Shared global dependency failure does not drain all regions

**Severity:** High  
**Category:** health  
**Applies when:** shared third-party dependency exists

### Requirement

The implementation must satisfy this behavior when the same artifact runs in either regional deployment or under its approved active-passive ownership model.

### Evidence to inspect

- `readiness contributor`
- `circuit breaker health`

### Finding condition

Emit a finding when repository evidence demonstrates that a globally shared dependency is placed in regional readiness without an alternative.

### Quality guidance

- Apply the global quality caveats and evidence-only rules.

### Evaluation constraints

- Cite the exact file, symbol or property, and line range.
- Evaluate effective behavior, not the presence of a library or annotation.
- Return `not_assessed` when evidence is insufficient.
- Deduplicate overlapping controls under one root-cause finding.
- Do not create deployment, infrastructure, or PCF findings from this master.

---

## APP-TOKEN-001: Token acquisition has bounded last-known-good fallback

**Severity:** High  
**Category:** authentication-resilience  
**Applies when:** OAuth token acquisition exists

### Requirement

The implementation must satisfy this behavior when the same artifact runs in either regional deployment or under its approved active-passive ownership model.

### Evidence to inspect

- `token cache`
- `expiresAt`
- `grace period`

### Finding condition

Emit a finding when repository evidence demonstrates that every request synchronously depends on token service without a bounded valid-token fallback.

### Quality guidance

- Apply the global quality caveats and evidence-only rules.

### Evaluation constraints

- Cite the exact file, symbol or property, and line range.
- Evaluate effective behavior, not the presence of a library or annotation.
- Return `not_assessed` when evidence is insufficient.
- Deduplicate overlapping controls under one root-cause finding.
- Do not create deployment, infrastructure, or PCF findings from this master.

---

## APP-TOKEN-002: Token refresh is concurrency safe

**Severity:** High  
**Category:** authentication-resilience  
**Applies when:** token cache exists

### Requirement

The implementation must satisfy this behavior when the same artifact runs in either regional deployment or under its approved active-passive ownership model.

### Evidence to inspect

- `single-flight`
- `atomic`
- `invalidate`

### Finding condition

Emit a finding when repository evidence demonstrates that concurrent refreshes stampede or return divergent tokens.

### Quality guidance

- Apply the global quality caveats and evidence-only rules.

### Evaluation constraints

- Cite the exact file, symbol or property, and line range.
- Evaluate effective behavior, not the presence of a library or annotation.
- Return `not_assessed` when evidence is insufficient.
- Deduplicate overlapping controls under one root-cause finding.
- Do not create deployment, infrastructure, or PCF findings from this master.

---

## APP-STATE-001: Durable workflow state transitions are ordered and observable

**Severity:** Critical  
**Category:** durable-state  
**Applies when:** workflow status is persisted

### Requirement

The implementation must satisfy this behavior when the same artifact runs in either regional deployment or under its approved active-passive ownership model.

### Evidence to inspect

- `INPROCESS`
- `FAILED`
- `COMPLETED`

### Finding condition

Emit a finding when repository evidence demonstrates that state changes are fire-and-forget or can reorder.

### Quality guidance

- Apply the global quality caveats and evidence-only rules.

### Evaluation constraints

- Cite the exact file, symbol or property, and line range.
- Evaluate effective behavior, not the presence of a library or annotation.
- Return `not_assessed` when evidence is insufficient.
- Deduplicate overlapping controls under one root-cause finding.
- Do not create deployment, infrastructure, or PCF findings from this master.

---

## APP-STATE-002: Retry exhaustion reaches a durable terminal state

**Severity:** High  
**Category:** durable-state  
**Applies when:** retries wrap durable work

### Requirement

The implementation must satisfy this behavior when the same artifact runs in either regional deployment or under its approved active-passive ownership model.

### Evidence to inspect

- `doOnError`
- `onErrorResume`
- `FAILED`

### Finding condition

Emit a finding when repository evidence demonstrates that retry exhaustion strands records in an intermediate state.

### Quality guidance

- Apply the global quality caveats and evidence-only rules.

### Evaluation constraints

- Cite the exact file, symbol or property, and line range.
- Evaluate effective behavior, not the presence of a library or annotation.
- Return `not_assessed` when evidence is insufficient.
- Deduplicate overlapping controls under one root-cause finding.
- Do not create deployment, infrastructure, or PCF findings from this master.

---

## APP-ASYNC-001: Async infrastructure is explicitly enabled

**Severity:** High  
**Category:** async-execution  
**Applies when:** @Async is used

### Requirement

The implementation must satisfy this behavior when the same artifact runs in either regional deployment or under its approved active-passive ownership model.

### Evidence to inspect

- `@EnableAsync`
- `@Configuration`
- `@Bean name`

### Finding condition

Emit a finding when repository evidence demonstrates that async interception or named executor resolution is not established.

### Quality guidance

- Apply the global quality caveats and evidence-only rules.

### Evaluation constraints

- Cite the exact file, symbol or property, and line range.
- Evaluate effective behavior, not the presence of a library or annotation.
- Return `not_assessed` when evidence is insufficient.
- Deduplicate overlapping controls under one root-cause finding.
- Do not create deployment, infrastructure, or PCF findings from this master.

---

## APP-ASYNC-002: Executor capacity, rejection, and blocking behavior are bounded

**Severity:** High  
**Category:** async-execution  
**Applies when:** custom executor or scheduler exists

### Requirement

The implementation must satisfy this behavior when the same artifact runs in either regional deployment or under its approved active-passive ownership model.

### Evidence to inspect

- `queueCapacity`
- `RejectedExecutionHandler`
- `Thread.sleep`
- `parallelStream`

### Finding condition

Emit a finding when repository evidence demonstrates that capacity is invalid or work can be silently rejected, blocked, or routed to the common pool.

### Quality guidance

- Apply the global quality caveats and evidence-only rules.

### Evaluation constraints

- Cite the exact file, symbol or property, and line range.
- Evaluate effective behavior, not the presence of a library or annotation.
- Return `not_assessed` when evidence is insufficient.
- Deduplicate overlapping controls under one root-cause finding.
- Do not create deployment, infrastructure, or PCF findings from this master.

---

## APP-KAFKA-001: Consumer startup is region-role controlled

**Severity:** Critical  
**Category:** messaging  
**Applies when:** Kafka consumers exist

### Requirement

The implementation must satisfy this behavior when the same artifact runs in either regional deployment or under its approved active-passive ownership model.

### Evidence to inspect

- `autoStartup`
- `consumer.autostart`

### Finding condition

Emit a finding when repository evidence demonstrates that listeners auto-start in multiple regions without ownership.

### Quality guidance

- Apply the global quality caveats and evidence-only rules.

### Evaluation constraints

- Cite the exact file, symbol or property, and line range.
- Evaluate effective behavior, not the presence of a library or annotation.
- Return `not_assessed` when evidence is insufficient.
- Deduplicate overlapping controls under one root-cause finding.
- Do not create deployment, infrastructure, or PCF findings from this master.

---

## APP-KAFKA-002: Consumer acknowledgment follows successful processing

**Severity:** Critical  
**Category:** messaging  
**Applies when:** Kafka consumers mutate state

### Requirement

The implementation must satisfy this behavior when the same artifact runs in either regional deployment or under its approved active-passive ownership model.

### Evidence to inspect

- `AckMode`
- `enable.auto.commit`

### Finding condition

Emit a finding when repository evidence demonstrates that offsets advance before processing succeeds.

### Quality guidance

- Apply the global quality caveats and evidence-only rules.

### Evaluation constraints

- Cite the exact file, symbol or property, and line range.
- Evaluate effective behavior, not the presence of a library or annotation.
- Return `not_assessed` when evidence is insufficient.
- Deduplicate overlapping controls under one root-cause finding.
- Do not create deployment, infrastructure, or PCF findings from this master.

---

## APP-KAFKA-003: Consumer errors have finite retry and dead-letter routing

**Severity:** High  
**Category:** messaging  
**Applies when:** Kafka consumers exist

### Requirement

The implementation must satisfy this behavior when the same artifact runs in either regional deployment or under its approved active-passive ownership model.

### Evidence to inspect

- `DefaultErrorHandler`
- `DeadLetterPublishingRecoverer`

### Finding condition

Emit a finding when repository evidence demonstrates that poison records retry indefinitely or disappear.

### Quality guidance

- Apply the global quality caveats and evidence-only rules.

### Evaluation constraints

- Cite the exact file, symbol or property, and line range.
- Evaluate effective behavior, not the presence of a library or annotation.
- Return `not_assessed` when evidence is insufficient.
- Deduplicate overlapping controls under one root-cause finding.
- Do not create deployment, infrastructure, or PCF findings from this master.

---

## APP-KAFKA-004: Consumer lag and assignment are observable

**Severity:** High  
**Category:** messaging  
**Applies when:** Kafka consumers exist

### Requirement

The implementation must satisfy this behavior when the same artifact runs in either regional deployment or under its approved active-passive ownership model.

### Evidence to inspect

- `lag metric`
- `assignment`
- `paused`

### Finding condition

Emit a finding when repository evidence demonstrates that consumer degradation is not observable.

### Quality guidance

- Apply the global quality caveats and evidence-only rules.

### Evaluation constraints

- Cite the exact file, symbol or property, and line range.
- Evaluate effective behavior, not the presence of a library or annotation.
- Return `not_assessed` when evidence is insufficient.
- Deduplicate overlapping controls under one root-cause finding.
- Do not create deployment, infrastructure, or PCF findings from this master.

---

## APP-KAFKA-005: Producer delivery is awaited and durable

**Severity:** Critical  
**Category:** messaging  
**Applies when:** Kafka producer exists

### Requirement

The implementation must satisfy this behavior when the same artifact runs in either regional deployment or under its approved active-passive ownership model.

### Evidence to inspect

- `send future`
- `acks`
- `enable.idempotence`

### Finding condition

Emit a finding when repository evidence demonstrates that producer result is discarded or durability is absent.

### Quality guidance

- Apply the global quality caveats and evidence-only rules.

### Evaluation constraints

- Cite the exact file, symbol or property, and line range.
- Evaluate effective behavior, not the presence of a library or annotation.
- Return `not_assessed` when evidence is insufficient.
- Deduplicate overlapping controls under one root-cause finding.
- Do not create deployment, infrastructure, or PCF findings from this master.

---

## APP-KAFKA-006: Kafka records carry stable dedupe identity

**Severity:** High  
**Category:** messaging  
**Applies when:** Kafka producer exists

### Requirement

The implementation must satisfy this behavior when the same artifact runs in either regional deployment or under its approved active-passive ownership model.

### Evidence to inspect

- `message-id`
- `event-id`
- `RecordHeader`

### Finding condition

Emit a finding when repository evidence demonstrates that records lack stable identity across retry.

### Quality guidance

- Apply the global quality caveats and evidence-only rules.

### Evaluation constraints

- Cite the exact file, symbol or property, and line range.
- Evaluate effective behavior, not the presence of a library or annotation.
- Return `not_assessed` when evidence is insufficient.
- Deduplicate overlapping controls under one root-cause finding.
- Do not create deployment, infrastructure, or PCF findings from this master.

---

## APP-KAFKA-007: Bound Kafka client properties are applied

**Severity:** High  
**Category:** messaging  
**Applies when:** custom Kafka config exists

### Requirement

The implementation must satisfy this behavior when the same artifact runs in either regional deployment or under its approved active-passive ownership model.

### Evidence to inspect

- `session.timeout.ms`
- `max.poll.interval.ms`

### Finding condition

Emit a finding when repository evidence demonstrates that declared settings are absent from effective client config.

### Quality guidance

- Apply the global quality caveats and evidence-only rules.

### Evaluation constraints

- Cite the exact file, symbol or property, and line range.
- Evaluate effective behavior, not the presence of a library or annotation.
- Return `not_assessed` when evidence is insufficient.
- Deduplicate overlapping controls under one root-cause finding.
- Do not create deployment, infrastructure, or PCF findings from this master.

---

## APP-CACHE-004: Cache loading coalesces concurrent misses

**Severity:** High  
**Category:** cache  
**Applies when:** cache loader calls dependencies

### Requirement

The implementation must satisfy this behavior when the same artifact runs in either regional deployment or under its approved active-passive ownership model.

### Evidence to inspect

- `LoadingCache`
- `single-flight`
- `Mono.cache`

### Finding condition

Emit a finding when repository evidence demonstrates that cold start causes a stampede.

### Quality guidance

- Apply the global quality caveats and evidence-only rules.

### Evaluation constraints

- Cite the exact file, symbol or property, and line range.
- Evaluate effective behavior, not the presence of a library or annotation.
- Return `not_assessed` when evidence is insufficient.
- Deduplicate overlapping controls under one root-cause finding.
- Do not create deployment, infrastructure, or PCF findings from this master.

---

## APP-CACHE-005: Refresh and warm-up are protected during degradation

**Severity:** High  
**Category:** cache  
**Applies when:** refresh or warm-up exists

### Requirement

The implementation must satisfy this behavior when the same artifact runs in either regional deployment or under its approved active-passive ownership model.

### Evidence to inspect

- `refreshAfterWrite`
- `CircuitBreaker`

### Finding condition

Emit a finding when repository evidence demonstrates that refresh repeatedly calls a failing dependency.

### Quality guidance

- Apply the global quality caveats and evidence-only rules.

### Evaluation constraints

- Cite the exact file, symbol or property, and line range.
- Evaluate effective behavior, not the presence of a library or annotation.
- Return `not_assessed` when evidence is insufficient.
- Deduplicate overlapping controls under one root-cause finding.
- Do not create deployment, infrastructure, or PCF findings from this master.

---

## APP-CACHE-006: Cache null and stale semantics are explicit

**Severity:** High  
**Category:** cache  
**Applies when:** cache stores tokens or remote data

### Requirement

The implementation must satisfy this behavior when the same artifact runs in either regional deployment or under its approved active-passive ownership model.

### Evidence to inspect

- `Mono.empty`
- `last known good`

### Finding condition

Emit a finding when repository evidence demonstrates that null results appear successful or stale use exceeds safety window.

### Quality guidance

- Apply the global quality caveats and evidence-only rules.

### Evaluation constraints

- Cite the exact file, symbol or property, and line range.
- Evaluate effective behavior, not the presence of a library or annotation.
- Return `not_assessed` when evidence is insufficient.
- Deduplicate overlapping controls under one root-cause finding.
- Do not create deployment, infrastructure, or PCF findings from this master.

---

## APP-HEALTH-001: Health contributor identifiers are verified

**Severity:** High  
**Category:** health  
**Applies when:** custom health groups exist

### Requirement

The implementation must satisfy this behavior when the same artifact runs in either regional deployment or under its approved active-passive ownership model.

### Evidence to inspect

- `group.readiness.include`
- `validate-group-membership`

### Finding condition

Emit a finding when repository evidence demonstrates that an unverified contributor ID breaks startup or readiness.

### Quality guidance

- Apply the global quality caveats and evidence-only rules.

### Evaluation constraints

- Cite the exact file, symbol or property, and line range.
- Evaluate effective behavior, not the presence of a library or annotation.
- Return `not_assessed` when evidence is insufficient.
- Deduplicate overlapping controls under one root-cause finding.
- Do not create deployment, infrastructure, or PCF findings from this master.

---

## APP-HEALTH-002: Health state updates after recovery

**Severity:** High  
**Category:** health  
**Applies when:** cached health state exists

### Requirement

The implementation must satisfy this behavior when the same artifact runs in either regional deployment or under its approved active-passive ownership model.

### Evidence to inspect

- `lastExecutionTime`
- `lastSuccess`

### Finding condition

Emit a finding when repository evidence demonstrates that successful checks do not restore health state.

### Quality guidance

- Apply the global quality caveats and evidence-only rules.

### Evaluation constraints

- Cite the exact file, symbol or property, and line range.
- Evaluate effective behavior, not the presence of a library or annotation.
- Return `not_assessed` when evidence is insufficient.
- Deduplicate overlapping controls under one root-cause finding.
- Do not create deployment, infrastructure, or PCF findings from this master.

---

## APP-API-001: State-changing endpoints use safe methods and authorization

**Severity:** High  
**Category:** api-security  
**Applies when:** admin endpoints exist

### Requirement

The implementation must satisfy this behavior when the same artifact runs in either regional deployment or under its approved active-passive ownership model.

### Evidence to inspect

- `@GetMapping`
- `@PreAuthorize`

### Finding condition

Emit a finding when repository evidence demonstrates that GET mutates state or administration lacks authorization.

### Quality guidance

- Apply the global quality caveats and evidence-only rules.

### Evaluation constraints

- Cite the exact file, symbol or property, and line range.
- Evaluate effective behavior, not the presence of a library or annotation.
- Return `not_assessed` when evidence is insufficient.
- Deduplicate overlapping controls under one root-cause finding.
- Do not create deployment, infrastructure, or PCF findings from this master.

---

## APP-SUPPLY-001: Shared dependency upgrades have regression tests

**Severity:** Medium  
**Category:** dependency-governance  
**Applies when:** parent BOM or shared models exist

### Requirement

The implementation must satisfy this behavior when the same artifact runs in either regional deployment or under its approved active-passive ownership model.

### Evidence to inspect

- `parent version`
- `dependencyManagement`

### Finding condition

Emit a finding when repository evidence demonstrates that transitive upgrades can change resilience behavior without tests.

### Quality guidance

- Apply the global quality caveats and evidence-only rules.

### Evaluation constraints

- Cite the exact file, symbol or property, and line range.
- Evaluate effective behavior, not the presence of a library or annotation.
- Return `not_assessed` when evidence is insufficient.
- Deduplicate overlapping controls under one root-cause finding.
- Do not create deployment, infrastructure, or PCF findings from this master.

---

## APP-SUPPLY-002: Runtime base image is immutable

**Severity:** High  
**Category:** supply-chain  
**Applies when:** Dockerfile exists

### Requirement

The implementation must satisfy this behavior when the same artifact runs in either regional deployment or under its approved active-passive ownership model.

### Evidence to inspect

- `FROM`
- `@sha256`

### Finding condition

Emit a finding when repository evidence demonstrates that base image is tag-only.

### Quality guidance

- Apply the global quality caveats and evidence-only rules.

### Evaluation constraints

- Cite the exact file, symbol or property, and line range.
- Evaluate effective behavior, not the presence of a library or annotation.
- Return `not_assessed` when evidence is insufficient.
- Deduplicate overlapping controls under one root-cause finding.
- Do not create deployment, infrastructure, or PCF findings from this master.

---

## APP-OBS-001: Trace export and correlation are operationally complete

**Severity:** Medium  
**Category:** observability  
**Applies when:** tracing exists

### Requirement

The implementation must satisfy this behavior when the same artifact runs in either regional deployment or under its approved active-passive ownership model.

### Evidence to inspect

- `OTLP`
- `traceparent`
- `exporter`

### Finding condition

Emit a finding when repository evidence demonstrates that tracing has no exporter or continuity.

### Quality guidance

- Apply the global quality caveats and evidence-only rules.

### Evaluation constraints

- Cite the exact file, symbol or property, and line range.
- Evaluate effective behavior, not the presence of a library or annotation.
- Return `not_assessed` when evidence is insufficient.
- Deduplicate overlapping controls under one root-cause finding.
- Do not create deployment, infrastructure, or PCF findings from this master.

---

## APP-CONF-014: Operationally variable constants are externalized or documented

**Severity:** Low  
**Category:** configuration-hygiene  
**Applies when:** partner constants exist

### Requirement

The implementation must satisfy this behavior when the same artifact runs in either regional deployment or under its approved active-passive ownership model.

### Evidence to inspect

- `TODO hardcode`
- `scope constant`

### Finding condition

Emit a finding when repository evidence demonstrates that a variable contract requires a code release without rationale.

### Quality guidance

- Apply the global quality caveats and evidence-only rules.

### Evaluation constraints

- Cite the exact file, symbol or property, and line range.
- Evaluate effective behavior, not the presence of a library or annotation.
- Return `not_assessed` when evidence is insufficient.
- Deduplicate overlapping controls under one root-cause finding.
- Do not create deployment, infrastructure, or PCF findings from this master.

---

## APP-WORKLOAD-001: Workload failover model matches its execution model

**Severity:** Critical  
**Category:** workload-model  
**Applies when:** scheduled, polling, batch, or externally triggered work exists

### Requirement

The implementation must satisfy this behavior when the same artifact runs in either regional deployment or under its approved active-passive ownership model.

### Evidence to inspect

- `@Scheduled`
- `CommandLineRunner`
- `ApplicationRunner`
- `kubectl exec`
- `Stonebranch`

### Finding condition

Emit a finding when repository evidence demonstrates that non-HTTP work is assumed to fail over through traffic routing or can execute concurrently in both regions.

### Quality guidance

- Apply the global quality caveats and evidence-only rules.

### Evaluation constraints

- Cite the exact file, symbol or property, and line range.
- Evaluate effective behavior, not the presence of a library or annotation.
- Return `not_assessed` when evidence is insufficient.
- Deduplicate overlapping controls under one root-cause finding.
- Do not create deployment, infrastructure, or PCF findings from this master.

---

## APP-WORKLOAD-002: Single-active workload activation is fail-safe

**Severity:** Critical  
**Category:** workload-model  
**Applies when:** exactly one region must own work

### Requirement

The implementation must satisfy this behavior when the same artifact runs in either regional deployment or under its approved active-passive ownership model.

### Evidence to inspect

- `enabled flag`
- `region owner`
- `lease`
- `epoch`

### Finding condition

Emit a finding when repository evidence demonstrates that activation defaults enabled, permits split brain, or lacks observable ownership.

### Quality guidance

- Apply the global quality caveats and evidence-only rules.

### Evaluation constraints

- Cite the exact file, symbol or property, and line range.
- Evaluate effective behavior, not the presence of a library or annotation.
- Return `not_assessed` when evidence is insufficient.
- Deduplicate overlapping controls under one root-cause finding.
- Do not create deployment, infrastructure, or PCF findings from this master.

---

## APP-SCHED-001: Scheduled work uses distributed ownership

**Severity:** Critical  
**Category:** scheduler  
**Applies when:** scheduled work processes shared state

### Requirement

The implementation must satisfy this behavior when the same artifact runs in either regional deployment or under its approved active-passive ownership model.

### Evidence to inspect

- `@Scheduled`
- `AtomicBoolean`
- `ShedLock`
- `leader election`

### Finding condition

Emit a finding when repository evidence demonstrates that multiple pods or regions can process the same work using only process-local coordination.

### Quality guidance

- Apply the global quality caveats and evidence-only rules.

### Evaluation constraints

- Cite the exact file, symbol or property, and line range.
- Evaluate effective behavior, not the presence of a library or annotation.
- Return `not_assessed` when evidence is insufficient.
- Deduplicate overlapping controls under one root-cause finding.
- Do not create deployment, infrastructure, or PCF findings from this master.

---

## APP-SCHED-002: Scheduled reprocessing atomically claims and completes work

**Severity:** Critical  
**Category:** scheduler  
**Applies when:** reprocessor selects durable records

### Requirement

The implementation must satisfy this behavior when the same artifact runs in either regional deployment or under its approved active-passive ownership model.

### Evidence to inspect

- `pickFlag`
- `status update`
- `lease owner`
- `attempt count`

### Finding condition

Emit a finding when repository evidence demonstrates that selection and claim are non-atomic or completion is not durably verified.

### Quality guidance

- Apply the global quality caveats and evidence-only rules.

### Evaluation constraints

- Cite the exact file, symbol or property, and line range.
- Evaluate effective behavior, not the presence of a library or annotation.
- Return `not_assessed` when evidence is insufficient.
- Deduplicate overlapping controls under one root-cause finding.
- Do not create deployment, infrastructure, or PCF findings from this master.

---

## APP-BATCH-001: Batch exit status reflects terminal completion

**Severity:** Critical  
**Category:** batch  
**Applies when:** application exits after a run

### Requirement

The implementation must satisfy this behavior when the same artifact runs in either regional deployment or under its approved active-passive ownership model.

### Evidence to inspect

- `System.exit`
- `exit code`
- `subscribe`

### Finding condition

Emit a finding when repository evidence demonstrates that process exits successfully before work completes or despite failure.

### Quality guidance

- Apply the global quality caveats and evidence-only rules.

### Evaluation constraints

- Cite the exact file, symbol or property, and line range.
- Evaluate effective behavior, not the presence of a library or annotation.
- Return `not_assessed` when evidence is insufficient.
- Deduplicate overlapping controls under one root-cause finding.
- Do not create deployment, infrastructure, or PCF findings from this master.

---

## APP-BATCH-002: Batch runs have durable idempotent run identity

**Severity:** High  
**Category:** batch  
**Applies when:** repeatable business runs exist

### Requirement

The implementation must satisfy this behavior when the same artifact runs in either regional deployment or under its approved active-passive ownership model.

### Evidence to inspect

- `runId`
- `businessDate`
- `attempt`
- `completion marker`

### Finding condition

Emit a finding when repository evidence demonstrates that rerun cannot distinguish complete, partial, failed, or duplicate execution.

### Quality guidance

- Apply the global quality caveats and evidence-only rules.

### Evaluation constraints

- Cite the exact file, symbol or property, and line range.
- Evaluate effective behavior, not the presence of a library or annotation.
- Return `not_assessed` when evidence is insufficient.
- Deduplicate overlapping controls under one root-cause finding.
- Do not create deployment, infrastructure, or PCF findings from this master.

---

## APP-BATCH-003: Business output is durable before success

**Severity:** Critical  
**Category:** batch-output  
**Applies when:** job produces required files or reports

### Requirement

The implementation must satisfy this behavior when the same artifact runs in either regional deployment or under its approved active-passive ownership model.

### Evidence to inspect

- `Files.write`
- `FileOutputStream`
- `/tmp`
- `BlobClient`

### Finding condition

Emit a finding when repository evidence demonstrates that success is reported while output exists only on ephemeral storage or before durable upload.

### Quality guidance

- Apply the global quality caveats and evidence-only rules.

### Evaluation constraints

- Cite the exact file, symbol or property, and line range.
- Evaluate effective behavior, not the presence of a library or annotation.
- Return `not_assessed` when evidence is insufficient.
- Deduplicate overlapping controls under one root-cause finding.
- Do not create deployment, infrastructure, or PCF findings from this master.

---

## APP-BATCH-004: Large result sets are streamed or bounded

**Severity:** High  
**Category:** batch-memory  
**Applies when:** job reads potentially large results

### Requirement

The implementation must satisfy this behavior when the same artifact runs in either regional deployment or under its approved active-passive ownership model.

### Evidence to inspect

- `collectList`
- `toList`
- `fetchAll`
- `page size`

### Finding condition

Emit a finding when repository evidence demonstrates that unbounded results are accumulated in memory without pagination, streaming, or checkpointing.

### Quality guidance

- Apply the global quality caveats and evidence-only rules.

### Evaluation constraints

- Cite the exact file, symbol or property, and line range.
- Evaluate effective behavior, not the presence of a library or annotation.
- Return `not_assessed` when evidence is insufficient.
- Deduplicate overlapping controls under one root-cause finding.
- Do not create deployment, infrastructure, or PCF findings from this master.

---

## APP-FIN-001: Irreversible financial effects follow a durable intent boundary

**Severity:** Critical  
**Category:** financial-integrity  
**Applies when:** external financial effect occurs

### Requirement

The implementation must satisfy this behavior when the same artifact runs in either regional deployment or under its approved active-passive ownership model.

### Evidence to inspect

- `authorize`
- `charge`
- `credit`
- `capture`
- `refund`
- `void`

### Finding condition

Emit a finding when repository evidence demonstrates that provider effect can occur before a durable intent and stable operation identity exist.

### Quality guidance

- Apply the global quality caveats and evidence-only rules.

### Evaluation constraints

- Cite the exact file, symbol or property, and line range.
- Evaluate effective behavior, not the presence of a library or annotation.
- Return `not_assessed` when evidence is insufficient.
- Deduplicate overlapping controls under one root-cause finding.
- Do not create deployment, infrastructure, or PCF findings from this master.

---

## APP-FIN-002: Partial financial workflows define compensation and reconciliation

**Severity:** Critical  
**Category:** financial-integrity  
**Applies when:** workflow spans provider and durable stores

### Requirement

The implementation must satisfy this behavior when the same artifact runs in either regional deployment or under its approved active-passive ownership model.

### Evidence to inspect

- `compensation`
- `reconcile`
- `outbox`
- `saga`

### Finding condition

Emit a finding when repository evidence demonstrates that partial success has no compensation or durable reconciliation path.

### Quality guidance

- Apply the global quality caveats and evidence-only rules.

### Evaluation constraints

- Cite the exact file, symbol or property, and line range.
- Evaluate effective behavior, not the presence of a library or annotation.
- Return `not_assessed` when evidence is insufficient.
- Deduplicate overlapping controls under one root-cause finding.
- Do not create deployment, infrastructure, or PCF findings from this master.

---

## APP-FIN-003: Payment identity is stable across retries and regions

**Severity:** Critical  
**Category:** financial-integrity  
**Applies when:** financial operation can retry

### Requirement

The implementation must satisfy this behavior when the same artifact runs in either regional deployment or under its approved active-passive ownership model.

### Evidence to inspect

- `UUID.randomUUID`
- `currentTimeMillis`
- `idempotency key`

### Finding condition

Emit a finding when repository evidence demonstrates that each attempt generates a new identity or correlation identity is mistaken for idempotency identity.

### Quality guidance

- Apply the global quality caveats and evidence-only rules.

### Evaluation constraints

- Cite the exact file, symbol or property, and line range.
- Evaluate effective behavior, not the presence of a library or annotation.
- Return `not_assessed` when evidence is insufficient.
- Deduplicate overlapping controls under one root-cause finding.
- Do not create deployment, infrastructure, or PCF findings from this master.

---

## APP-FIN-004: Synthetic success is backed by durable recoverable state

**Severity:** Critical  
**Category:** financial-integrity  
**Applies when:** service can return synthetic or deferred approval

### Requirement

The implementation must satisfy this behavior when the same artifact runs in either regional deployment or under its approved active-passive ownership model.

### Evidence to inspect

- `synthetic approved`
- `fallback approval`
- `accepted`

### Finding condition

Emit a finding when repository evidence demonstrates that success can be returned before a complete recoverable record is durably written.

### Quality guidance

- Apply the global quality caveats and evidence-only rules.

### Evaluation constraints

- Cite the exact file, symbol or property, and line range.
- Evaluate effective behavior, not the presence of a library or annotation.
- Return `not_assessed` when evidence is insufficient.
- Deduplicate overlapping controls under one root-cause finding.
- Do not create deployment, infrastructure, or PCF findings from this master.

---

## APP-DB-001: Reactive database transaction boundaries are effective

**Severity:** Critical  
**Category:** database-consistency  
**Applies when:** multiple related reactive writes exist

### Requirement

The implementation must satisfy this behavior when the same artifact runs in either regional deployment or under its approved active-passive ownership model.

### Evidence to inspect

- `TransactionalOperator`
- `ReactiveTransactionManager`
- `@Transactional`

### Finding condition

Emit a finding when repository evidence demonstrates that related writes subscribe separately or transaction scope does not cover publisher execution.

### Quality guidance

- Apply the global quality caveats and evidence-only rules.

### Evaluation constraints

- Cite the exact file, symbol or property, and line range.
- Evaluate effective behavior, not the presence of a library or annotation.
- Return `not_assessed` when evidence is insufficient.
- Deduplicate overlapping controls under one root-cause finding.
- Do not create deployment, infrastructure, or PCF findings from this master.

---

## APP-DB-003: Cross-store writes have reconciliation

**Severity:** Critical  
**Category:** database-consistency  
**Applies when:** one operation writes multiple stores

### Requirement

The implementation must satisfy this behavior when the same artifact runs in either regional deployment or under its approved active-passive ownership model.

### Evidence to inspect

- `SQL`
- `Mongo`
- `Cosmos`
- `fallback store`

### Finding condition

Emit a finding when repository evidence demonstrates that stores can diverge without a durable reconciliation marker.

### Quality guidance

- Apply the global quality caveats and evidence-only rules.

### Evaluation constraints

- Cite the exact file, symbol or property, and line range.
- Evaluate effective behavior, not the presence of a library or annotation.
- Return `not_assessed` when evidence is insufficient.
- Deduplicate overlapping controls under one root-cause finding.
- Do not create deployment, infrastructure, or PCF findings from this master.

---

## APP-CORRECT-001: Reactive contracts never return null

**Severity:** Critical  
**Category:** correctness  
**Applies when:** Mono or Flux is returned

### Requirement

The implementation must satisfy this behavior when the same artifact runs in either regional deployment or under its approved active-passive ownership model.

### Evidence to inspect

- `return null`
- `Mono.empty`
- `Flux.empty`

### Finding condition

Emit a finding when repository evidence demonstrates that a reactive method or required branch returns null.

### Quality guidance

- Apply the global quality caveats and evidence-only rules.

### Evaluation constraints

- Cite the exact file, symbol or property, and line range.
- Evaluate effective behavior, not the presence of a library or annotation.
- Return `not_assessed` when evidence is insufficient.
- Deduplicate overlapping controls under one root-cause finding.
- Do not create deployment, infrastructure, or PCF findings from this master.

---

## APP-CORRECT-002: Required business-data failures cannot silently default

**Severity:** Critical  
**Category:** correctness  
**Applies when:** mandatory business data is read

### Requirement

The implementation must satisfy this behavior when the same artifact runs in either regional deployment or under its approved active-passive ownership model.

### Evidence to inspect

- `default value`
- `return null`
- `empty result`
- `catch`

### Finding condition

Emit a finding when repository evidence demonstrates that mandatory data failure becomes null, empty, zero, or success and processing continues.

### Quality guidance

- Apply the global quality caveats and evidence-only rules.

### Evaluation constraints

- Cite the exact file, symbol or property, and line range.
- Evaluate effective behavior, not the presence of a library or annotation.
- Return `not_assessed` when evidence is insufficient.
- Deduplicate overlapping controls under one root-cause finding.
- Do not create deployment, infrastructure, or PCF findings from this master.

---

## APP-FALLBACK-001: Fallback paths are independently reliable and observable

**Severity:** Critical  
**Category:** fallback  
**Applies when:** a primary failure invokes fallback

### Requirement

The implementation must satisfy this behavior when the same artifact runs in either regional deployment or under its approved active-passive ownership model.

### Evidence to inspect

- `fallback`
- `onErrorResume`
- `secondary store`

### Finding condition

Emit a finding when repository evidence demonstrates that fallback has no bounded completion, dual failure is swallowed, or outcomes are indistinguishable.

### Quality guidance

- Apply the global quality caveats and evidence-only rules.

### Evaluation constraints

- Cite the exact file, symbol or property, and line range.
- Evaluate effective behavior, not the presence of a library or annotation.
- Return `not_assessed` when evidence is insufficient.
- Deduplicate overlapping controls under one root-cause finding.
- Do not create deployment, infrastructure, or PCF findings from this master.

---

## APP-OBS-002: Business throughput and stuck work are observable

**Severity:** High  
**Category:** observability  
**Applies when:** batch, scheduler, or reprocessor exists

### Requirement

The implementation must satisfy this behavior when the same artifact runs in either regional deployment or under its approved active-passive ownership model.

### Evidence to inspect

- `last success`
- `backlog age`
- `run duration`
- `zero throughput`

### Finding condition

Emit a finding when repository evidence demonstrates that process health can stay UP while business processing stops or records remain stuck.

### Quality guidance

- Apply the global quality caveats and evidence-only rules.

### Evaluation constraints

- Cite the exact file, symbol or property, and line range.
- Evaluate effective behavior, not the presence of a library or annotation.
- Return `not_assessed` when evidence is insufficient.
- Deduplicate overlapping controls under one root-cause finding.
- Do not create deployment, infrastructure, or PCF findings from this master.

---

## APP-OBS-003: Correlation propagates across durable and external boundaries

**Severity:** High  
**Category:** observability  
**Applies when:** workflow spans dependencies

### Requirement

The implementation must satisfy this behavior when the same artifact runs in either regional deployment or under its approved active-passive ownership model.

### Evidence to inspect

- `correlationId`
- `provider transaction id`
- `traceId`

### Finding condition

Emit a finding when repository evidence demonstrates that correlation is regenerated or not persisted and propagated.

### Quality guidance

- Apply the global quality caveats and evidence-only rules.

### Evaluation constraints

- Cite the exact file, symbol or property, and line range.
- Evaluate effective behavior, not the presence of a library or annotation.
- Return `not_assessed` when evidence is insufficient.
- Deduplicate overlapping controls under one root-cause finding.
- Do not create deployment, infrastructure, or PCF findings from this master.

---

## APP-ENDPOINT-001: Durable work stores logical destinations, not stale physical endpoints

**Severity:** High  
**Category:** regional-affinity  
**Applies when:** durable records contain destination URLs

### Requirement

The implementation must satisfy this behavior when the same artifact runs in either regional deployment or under its approved active-passive ownership model.

### Evidence to inspect

- `url field`
- `endpoint field`
- `baseUrl`

### Finding condition

Emit a finding when repository evidence demonstrates that reprocessing uses a stored region-specific physical endpoint instead of current logical service identity.

### Quality guidance

- Apply the global quality caveats and evidence-only rules.

### Evaluation constraints

- Cite the exact file, symbol or property, and line range.
- Evaluate effective behavior, not the presence of a library or annotation.
- Return `not_assessed` when evidence is insufficient.
- Deduplicate overlapping controls under one root-cause finding.
- Do not create deployment, infrastructure, or PCF findings from this master.

---

## APP-PROC-001: Required companion processes participate in health and lifecycle

**Severity:** High  
**Category:** process-model  
**Applies when:** container runs multiple required processes

### Requirement

The implementation must satisfy this behavior when the same artifact runs in either regional deployment or under its approved active-passive ownership model.

### Evidence to inspect

- `supervisor`
- `ProcessBuilder`
- `side process`
- `proxy process`

### Finding condition

Emit a finding when repository evidence demonstrates that a required process can fail while application readiness remains UP or shutdown signals are not coordinated.

### Quality guidance

- Apply the global quality caveats and evidence-only rules.

### Evaluation constraints

- Cite the exact file, symbol or property, and line range.
- Evaluate effective behavior, not the presence of a library or annotation.
- Return `not_assessed` when evidence is insufficient.
- Deduplicate overlapping controls under one root-cause finding.
- Do not create deployment, infrastructure, or PCF findings from this master.
