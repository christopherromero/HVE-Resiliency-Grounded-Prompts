---
schema_version: 2.2.0
document_type: dependency_standard
standard_id: JVM-RUNTIME-RESILIENCY
service: jvm-runtime
service_name: JVM Runtime Resiliency
language: java
framework: spring-boot
version: 1.1.0
lifecycle_status: active
assessment_scope: repository_owned_runtime_and_lifecycle
repository_owned_only: true
infrastructure_findings_allowed: false
assessment:
  enabled: true
  emit_findings: true
  include_in_score: true
  unknown_evidence_status: not_assessed
controls:
- id: JVM-001
  title: Supported runtime and flag compatibility
  severity: critical
  category: runtime-compatibility
  applies_when: the repository declares a JDK runtime, JVM flags, agents, or a container
    base image
  evidence_patterns:
  - maven.compiler.release
  - java.toolchain
  - JAVA_TOOL_OPTIONS
  - JAVA_OPTS
  - FROM eclipse-temurin
  finding_when: repository-owned runtime declarations conflict, a flag is invalid
    for the effective JDK, or a preview feature is used without explicit enablement
    and test parity
  emit_on_failure: true
- id: JVM-002
  title: Container awareness
  severity: critical
  category: container-awareness
  applies_when: the application runs in a container with memory or CPU limits
  evidence_patterns:
  - UseContainerSupport
  - ActiveProcessorCount
  - availableProcessors
  - MaxRAMPercentage
  finding_when: container support is disabled, processor count is forced without evidenced
    rationale and validation, or CPU-derived pool sizing depends on an unverified
    effective processor count
  emit_on_failure: true
- id: JVM-003
  title: Heap sizing against total container memory
  severity: critical
  category: memory-sizing
  applies_when: heap sizing is declared in repository-owned build, container, or runtime
    configuration
  evidence_patterns:
  - -Xmx
  - -Xms
  - InitialRAMPercentage
  - MaxRAMPercentage
  - MaxDirectMemorySize
  finding_when: heap equals or nearly consumes the container limit, contradictory fixed
    and percentage sizing is unexplained, a fixed heap is reused across materially
    different pod sizes, or a known native-heavy workload has no non-heap allowance
  emit_on_failure: true
- id: JVM-004
  title: Heap stability and leak detection
  severity: high
  category: memory-stability
  applies_when: the repository contains caches, collections, queues, listeners, or
    request-scoped retention
  evidence_patterns:
  - ConcurrentHashMap
  - Caffeine
  - ThreadLocal
  - LinkedBlockingQueue
  - addListener
  finding_when: repository evidence shows an unbounded cache, collection, or queue,
    retained request context, a listener or classloader leak, or retry amplification
    of retained state
  emit_on_failure: true
- id: JVM-005
  title: Garbage collector selection
  severity: high
  category: garbage-collection
  applies_when: a collector is selected explicitly or relied upon by default
  evidence_patterns:
  - UseG1GC
  - UseZGC
  - UseParallelGC
  - UseSerialGC
  - MaxGCPauseMillis
  finding_when: the selected collector is unsupported by the effective JDK, or is chosen
    without latency, throughput, heap, CPU, and operational rationale or validation
  emit_on_failure: true
- id: JVM-006
  title: GC configuration safety
  severity: high
  category: garbage-collection
  applies_when: GC tuning flags are present
  evidence_patterns:
  - InitiatingHeapOccupancyPercent
  - G1HeapRegionSize
  - MaxTenuringThreshold
  - DisableExplicitGC
  - System.gc()
  finding_when: unsupported flags prevent startup, mutually inconsistent collectors
    are selected, tuning masks an allocation or leak defect, or System.gc() is used
    as a correctness or routine capacity mechanism
  emit_on_failure: true
- id: JVM-007
  title: GC observability
  severity: medium
  category: observability
  applies_when: the application runs on a server-class JVM in a shared or latency-sensitive
    workload
  evidence_patterns:
  - -Xlog:gc
  - PrintGCDetails
  - gc log rotation
  - filecount
  finding_when: GC logging is absent or version-incompatible, pauses and concurrent
    cycles cannot be correlated with incidents, or log retention is unbounded or exposes
    sensitive data
  emit_on_failure: true
- id: JVM-008
  title: Out-of-memory behavior and diagnostics
  severity: critical
  category: failure-behavior
  applies_when: the application can exhaust heap, metaspace, direct memory, or container
    memory
  evidence_patterns:
  - HeapDumpOnOutOfMemoryError
  - HeapDumpPath
  - ExitOnOutOfMemoryError
  - CrashOnOutOfMemoryError
  finding_when: OOM leaves the process in an undefined serving state, dumps are written
    to an unbounded or unsecured location, CrashOnOutOfMemoryError is used without
    operational approval, or OOM failure modes cannot be distinguished
  emit_on_failure: true
- id: JVM-009
  title: Native and off-heap memory
  severity: high
  category: native-memory
  applies_when: direct buffers, native clients, agents, or large thread populations
    are used
  evidence_patterns:
  - DirectByteBuffer
  - Netty
  - MaxDirectMemorySize
  - -Xss
  - NativeMemoryTracking
  finding_when: non-heap consumers are unbounded or unobserved, or container capacity
    reasoning relies on Java heap usage instead of process RSS
  emit_on_failure: true
- id: JVM-010
  title: Thread and executor bounds
  severity: critical
  category: concurrency
  applies_when: the application creates platform-thread pools, schedulers, or queues
  evidence_patterns:
  - ThreadPoolExecutor
  - ThreadPoolTaskExecutor
  - newFixedThreadPool
  - ForkJoinPool
  - RejectedExecutionHandler
  finding_when: unbounded queueing hides overload, pool size materially exceeds downstream
    capacity without rationale, rejection silently loses critical work, or shutdown
    does not drain or account for queued tasks
  emit_on_failure: true
- id: JVM-011
  title: Virtual-thread eligibility
  severity: high
  category: concurrency
  applies_when: virtual threads are enabled or proposed
  evidence_patterns:
  - spring.threads.virtual.enabled
  - newVirtualThreadPerTaskExecutor
  - Thread.ofVirtual
  finding_when: virtual threads run on an incompatible JDK, are pooled to limit concurrency,
    are applied to CPU-bound work, bypass downstream concurrency limits, or lose transaction,
    security-context, observability, or cancellation semantics
  emit_on_failure: true
- id: JVM-012
  title: Virtual-thread pinning and compatibility
  severity: high
  category: concurrency
  applies_when: virtual threads execute blocking or synchronized code paths
  evidence_patterns:
  - synchronized
  - ReentrantLock
  - jdk.VirtualThreadPinned
  - native call
  finding_when: a blocking path holds a monitor or performs a native or foreign call
    at material concurrency, carrier starvation is evidenced, and the effective JDK
    does not already remove the pinning risk
  emit_on_failure: true
- id: JVM-013
  title: Virtual-thread observability and context
  severity: medium
  category: observability
  applies_when: virtual threads are enabled and the application emits traces, metrics,
    or thread diagnostics
  evidence_patterns:
  - ThreadLocal
  - InheritableThreadLocal
  - MDC
  - SecurityContextHolder
  - thread name
  finding_when: per-thread state creates unbounded memory at expected concurrency,
    security or tracing context is lost, or monitoring assumes a small fixed thread
    population
  emit_on_failure: true
- id: JVM-014
  title: Safepoints, JIT, and startup
  severity: medium
  category: startup
  applies_when: startup duration or non-GC pause behavior affects rollout, probes,
    or latency
  evidence_patterns:
  - -Xlog:safepoint
  - ReservedCodeCacheSize
  - AppCDS
  - SharedArchiveFile
  - component scan
  finding_when: non-GC pause and startup risks are unobservable, or startup optimization
    bypasses required validation, security initialization, schema migration, or readiness
    gating
  emit_on_failure: true
- id: JVM-015
  title: Graceful shutdown signal handling
  severity: critical
  category: lifecycle
  applies_when: the application is packaged in a repository-owned container image or
    launched by a repository-owned script
  evidence_patterns:
  - ENTRYPOINT
  - CMD
  - exec java
  - tini
  - dumb-init
  finding_when: the entrypoint prevents SIGTERM from reaching the JVM, so framework
    shutdown never runs and the process relies on SIGKILL
  emit_on_failure: true
- id: JVM-016
  title: Readiness withdrawal and request draining
  severity: critical
  category: health
  applies_when: the application serves traffic or performs readiness-gated work and
    can be terminated by the platform
  evidence_patterns:
  - server.shutdown
  - spring.lifecycle.timeout-per-shutdown-phase
  - management.endpoint.health.group.readiness
  - AvailabilityChangeEvent
  - preStop
  finding_when: readiness is not withdrawn before shutdown begins, new work is accepted
    after termination starts, draining is unbounded, the application shutdown budget
    exceeds the platform termination budget, or persistent, streaming, and long-running
    requests have no defined termination behavior
  emit_on_failure: true
- id: JVM-017
  title: Background work and messaging shutdown
  severity: critical
  category: lifecycle
  applies_when: consumers, schedulers, executors, or producers run outside the request
    path
  evidence_patterns:
  - KafkaListener
  - Scheduled
  - CqlSession
  - acknowledge
  - awaitTermination
  finding_when: shutdown acknowledges before durable completion, abandons non-idempotent
    work without recovery, accepts new tasks after readiness withdrawal, or closes
    a dependency before its users
  emit_on_failure: true
- id: JVM-018
  title: Shutdown hooks and lifecycle ownership
  severity: high
  category: lifecycle
  applies_when: the application registers cleanup through framework callbacks or JVM
    shutdown hooks
  evidence_patterns:
  - PreDestroy
  - DisposableBean
  - SmartLifecycle
  - addShutdownHook
  - AutoCloseable
  finding_when: cleanup is duplicated across framework and raw JVM hooks, a hook depends
    on an already-closed service, a hook waits indefinitely, or a hook performs an
    unsafe remote mutation without idempotency or recovery design
  emit_on_failure: true
- id: JVM-019
  title: Forced termination and recovery
  severity: critical
  category: recovery
  applies_when: durable, non-idempotent, or externally visible work can be in flight
    at process loss
  evidence_patterns:
  - transaction boundary
  - idempotency key
  - deduplication
  - replay
  - startup recovery
  finding_when: correctness depends on the graceful period completing, or abrupt process
    or container loss can lose or duplicate work without replay, reconciliation, or
    startup recovery
  emit_on_failure: true
- id: JVM-020
  title: Runtime observability baseline
  severity: high
  category: observability
  applies_when: the application runs as a long-lived JVM workload
  evidence_patterns:
  - micrometer
  - jvm.memory.used
  - jvm.threads.live
  - process.cpu.usage
  - management.endpoints.web.exposure.include
  finding_when: baseline runtime signals are absent so memory, saturation, throttling,
    or shutdown progress cannot be diagnosed, or telemetry exposes secrets, queries,
    payloads, or personal data, or uses unbounded metric cardinality
  emit_on_failure: true
- id: JVM-021
  title: Resource limits and coordinated budgets
  severity: critical
  category: budget-coordination
  applies_when: repository-owned timeout, concurrency, memory, or lifecycle budgets
    interact with an adjacent platform or caller budget
  evidence_patterns:
  - timeout-per-shutdown-phase
  - terminationGracePeriodSeconds
  - connection-timeout
  - startupProbe
  - resources.limits.memory
  finding_when: a repository-owned budget contradicts an adjacent budget, such as shutdown
    phases exceeding termination grace, a request timeout exceeding the caller timeout,
    heap plus native headroom exceeding container memory, or startup exceeding the
    startup-probe budget
  emit_on_failure: true
- id: JVM-022
  title: Validation requirements for runtime changes
  severity: high
  category: testing
  applies_when: a change affects runtime flags, memory sizing, garbage collection,
    concurrency, or lifecycle behavior
  evidence_patterns:
  - integration test
  - load test
  - soak test
  - Testcontainers
  - JFR recording
  finding_when: an applicable runtime change is proposed or merged without the required
    startup, container-limited, load, fault, shutdown, and diagnostics validation evidence
  emit_on_failure: true
---

# JVM Runtime Resiliency Grounding Standard

## Purpose

Evaluate whether repository-owned JVM runtime configuration and application lifecycle behavior support bounded latency, memory safety, container operation, concurrency safety, observable failure, and controlled termination. Do not infer deployed limits or production behavior that are not present in repository evidence or approved context.

## Evidence and authority

Use, in order: build files and runtime version declarations; container entrypoints and JVM environment variables; repository-owned manifests and deployment configuration when enabled; application configuration; source lifecycle/concurrency code; tests; approved architecture context. Preserve path, symbol or configuration key, exact excerpt, fingerprint, snapshot, and advisory line range.

Missing deployed telemetry, limits, or platform configuration is an evidence gap, not application noncompliance. Never prescribe hard numbers without workload evidence, SLOs, load tests, and platform limits.

## Controls

### JVM-001: Supported runtime and flag compatibility

**Severity:** Critical  
**Category:** runtime-compatibility  
**Applies when:** The repository declares a JDK runtime, JVM flags, agents, or a container base image.

**Requirement:** Declare an explicit supported JDK runtime and ensure JVM flags, libraries, agents, and container images are compatible with it.

**Evidence to inspect:** Maven/Gradle toolchains, parent/BOM, container base image, CI runtime, `JAVA_TOOL_OPTIONS`/`JAVA_OPTS`, removed or experimental flags.  
**Finding condition:** Emit a finding when repository-owned runtime declarations conflict, a flag is invalid for the effective JDK, or a preview feature is used without explicit enablement and test parity.

### JVM-002: Container awareness

**Severity:** Critical  
**Category:** container-awareness  
**Applies when:** The application runs in a container with memory or CPU limits.

**Requirement:** The effective JDK must honor container memory and CPU limits. Do not disable container support without evidence and approval.

**Evidence to inspect:** `-XX:+/-UseContainerSupport`, `-XX:ActiveProcessorCount`, CPU-derived pool sizing, cgroup-compatible JDK version, base image.  
**Finding condition:** Emit a finding when container support is disabled, processor count is forced without evidenced rationale and validation, or CPU-derived pool sizing depends on an unverified effective processor count.

**Rules:** Do not infer Kubernetes limits from Java code. Validate effective processor count because it affects GC, ForkJoinPool, parallel streams, virtual-thread scheduling, and framework pools.

### JVM-003: Heap sizing against total container memory

**Severity:** Critical  
**Category:** memory-sizing  
**Applies when:** Heap sizing is declared in repository-owned build, container, or runtime configuration.

**Requirement:** Heap sizing must leave measured headroom for metaspace, code cache, thread stacks, direct/native buffers, GC structures, JIT, agents, libc, and application-native allocations.

**Evidence to inspect:** `-Xms`, `-Xmx`, `-XX:InitialRAMPercentage`, `-XX:MaxRAMPercentage`, `-XX:MinRAMPercentage`, container limits, direct-memory configuration, thread counts.  
**Finding condition:** Emit a finding when heap equals or nearly consumes the container limit, contradictory fixed and percentage sizing is unexplained, a fixed heap is reused across materially different pod sizes, or a known native-heavy workload has no non-heap allowance.

**Guidance:** Prefer one governed sizing strategy. Percentages are not automatically safe. Validate peak RSS, live set after GC, allocation rate, native memory, and OOM behavior under representative load.

### JVM-004: Heap stability and leak detection

**Severity:** High  
**Category:** memory-stability  
**Applies when:** The repository contains caches, collections, queues, listeners, or request-scoped retention.

**Requirement:** Demonstrate stable live-set behavior and bounded allocation under steady and degraded load.

**Evidence to inspect:** GC logs, JFR, heap histograms/dumps in safe environments, allocation profiles, soak tests, cache bounds, queue bounds.  
**Finding condition:** Emit a finding when repository evidence shows an unbounded cache, collection, or queue, retained request context, a listener or classloader leak, or retry amplification of retained state.

**Rules:** Missing production heap telemetry is an evidence gap, not noncompliance.

### JVM-005: Garbage collector selection

**Severity:** High  
**Category:** garbage-collection  
**Applies when:** A collector is selected explicitly or relied upon by default.

**Requirement:** Use a collector supported by the effective JDK and justified by latency, throughput, heap, CPU, and operational objectives.

**Evidence to inspect:** Explicit collector flags, default reliance, pause goals, allocation rate, humongous allocations, concurrent-cycle headroom.  
**Finding condition:** Emit a finding when the selected collector is unsupported by the effective JDK, or is chosen without latency, throughput, heap, CPU, and operational rationale or validation.

**Rules:** Do not claim one collector is universally best. G1 is a general-purpose default on modern server-class HotSpot. Low-latency collectors such as ZGC require compatible runtimes and sufficient CPU/memory headroom. Collector changes require benchmark and fault validation.

### JVM-006: GC configuration safety

**Severity:** High  
**Category:** garbage-collection  
**Applies when:** GC tuning flags are present.

**Requirement:** Avoid obsolete, contradictory, or cargo-cult GC flags. Keep the minimum set necessary and document intent.

**Evidence to inspect:** Pause targets, initiating occupancy, region sizing, survivor/tenuring overrides, explicit GC behavior, uncommit settings.  
**Finding condition:** Emit a finding when unsupported flags prevent startup, mutually inconsistent collectors are selected, tuning masks an allocation or leak defect, or `System.gc()` is used as a correctness or routine capacity mechanism.

### JVM-007: GC observability

**Severity:** Medium  
**Category:** observability  
**Applies when:** The application runs on a server-class JVM in a shared or latency-sensitive workload.

**Requirement:** Enable version-compatible GC logging sufficient to associate pauses, concurrent cycles, allocation pressure, promotion/evacuation failures, and heap occupancy with incidents while controlling retention and sensitive-data exposure.

**Evidence to inspect:** Unified logging flags, timestamping, rotation and collection strategy, correlation with application latency, alerting thresholds.  
**Finding condition:** Emit a finding when GC logging is absent or version-incompatible, pauses and concurrent cycles cannot be correlated with incidents, or log retention is unbounded or exposes sensitive data.

**Rules:** Alert on symptoms rather than arbitrary single-event thresholds.

### JVM-008: Out-of-memory behavior and diagnostics

**Severity:** Critical  
**Category:** failure-behavior  
**Applies when:** The application can exhaust heap, metaspace, direct memory, or container memory.

**Requirement:** OOM behavior must be deterministic, observable, and compatible with platform restart policy.

**Evidence to inspect:** `-XX:+HeapDumpOnOutOfMemoryError`, dump path and storage capacity/security, `-XX:+ExitOnOutOfMemoryError` or approved equivalent, orchestrator restart behavior, incident collection.  
**Finding condition:** Emit a finding when OOM leaves the process in an undefined serving state, dumps are written to an unbounded or unsecured location, `CrashOnOutOfMemoryError` is used without operational approval, or OOM failure modes cannot be distinguished.

**Rules:** A heap dump may contain secrets or personal data and needs access controls and retention. Distinguish Java heap, metaspace, direct buffer, native-thread, and container OOMKill failure modes.

### JVM-009: Native and off-heap memory

**Severity:** High  
**Category:** native-memory  
**Applies when:** Direct buffers, native clients, agents, or large thread populations are used.

**Requirement:** Bound and observe non-heap consumers.

**Evidence to inspect:** Direct buffers/Netty, mmap, compression/native clients, metaspace, code cache, JNI, thread stacks, agents, glibc arenas, `-XX:MaxDirectMemorySize` where appropriate.  
**Finding condition:** Emit a finding when non-heap consumers are unbounded or unobserved, or container capacity reasoning relies on Java heap usage instead of process RSS.

**Validation:** Native Memory Tracking may assist diagnosis but adds overhead and should be enabled deliberately. Container RSS is the capacity authority, not Java heap usage alone.

### JVM-010: Thread and executor bounds

**Severity:** Critical  
**Category:** concurrency  
**Applies when:** The application creates platform-thread pools, schedulers, or queues.

**Requirement:** Platform-thread pools and queues must be bounded according to downstream capacity and overload behavior.

**Evidence to inspect:** `ThreadPoolExecutor` sizes/queues/rejection, scheduler pools, connection pools, ForkJoinPool/common pool, parallel streams, blocking calls, thread-local retention.  
**Finding condition:** Emit a finding when unbounded queueing hides overload, pool size materially exceeds downstream capacity without rationale, rejection silently loses critical work, or shutdown does not drain or account for queued tasks.

### JVM-011: Virtual-thread eligibility

**Severity:** High  
**Category:** concurrency  
**Applies when:** Virtual threads are enabled or proposed.

**Requirement:** Use virtual threads only on a compatible JDK and for high-concurrency tasks dominated by blocking I/O. They improve scalability, not per-request speed, and do not remove downstream limits.

**Evidence to inspect:** JDK 21+ production use, framework enablement, executor creation, JDBC/HTTP/client behavior, connection pools, rate limits, CPU-bound work.  
**Finding condition:** Emit a finding when virtual threads run on an incompatible JDK, are pooled to limit concurrency, are applied to CPU-bound work, bypass downstream concurrency limits, or lose transaction, security-context, observability, or cancellation semantics.

**Rules:** Do not pool virtual threads to limit concurrency; use semaphores, rate limits, or bulkheads for scarce resources.

### JVM-012: Virtual-thread pinning and compatibility

**Severity:** High  
**Category:** concurrency  
**Applies when:** Virtual threads execute blocking or synchronized code paths.

**Requirement:** Assess pinning and library compatibility under representative load.

**Evidence to inspect:** Blocking while holding `synchronized` monitors on applicable JDKs, native/foreign calls, long critical sections, carrier starvation symptoms, JFR pinned-thread events and thread dumps.  
**Finding condition:** Emit a finding when a blocking path holds a monitor or performs a native or foreign call at material concurrency, carrier starvation is evidenced, and the effective JDK does not already remove the pinning risk.

**Rules:** Do not label every synchronized block a finding. Replace synchronization only when thread safety and business behavior remain correct.

### JVM-013: Virtual-thread observability and context

**Severity:** Medium  
**Category:** observability  
**Applies when:** Virtual threads are enabled and the application emits traces, metrics, or thread diagnostics.

**Requirement:** Observability must remain useful at virtual-thread scale.

**Evidence to inspect:** Thread names, trace/MDC propagation, `ThreadLocal`/`InheritableThreadLocal` use, per-thread caches, dumps/JFR, metrics cardinality.  
**Finding condition:** Emit a finding when per-thread state creates unbounded memory at expected concurrency, security or tracing context is lost, or monitoring assumes a small fixed thread population.

### JVM-014: Safepoints, JIT, and startup

**Severity:** Medium  
**Category:** startup  
**Applies when:** Startup duration or non-GC pause behavior affects rollout, probes, or latency.

**Requirement:** Detect JVM latency and startup risks outside GC.

**Evidence to inspect:** Safepoint logs/JFR, class loading, deoptimization, code-cache pressure, startup probes, CDS/AppCDS where supported, classpath scanning, eager initialization.  
**Finding condition:** Emit a finding when non-GC pause and startup risks are unobservable, or startup optimization bypasses required validation, security initialization, schema migration, or readiness gating.

**Rules:** Do not attribute every pause to GC.

### JVM-015: Graceful shutdown signal handling

**Severity:** Critical  
**Category:** lifecycle  
**Applies when:** The application is packaged in a repository-owned container image or launched by a repository-owned script.

**Requirement:** PID 1 must receive SIGTERM and initiate framework shutdown. Entrypoints must use `exec` or equivalent signal forwarding; do not rely on SIGKILL or IDE termination.

**Evidence to inspect:** Docker `ENTRYPOINT`/`CMD`, shell scripts, tini/dumb-init where approved, Spring shutdown settings, shutdown hooks.  
**Finding condition:** Emit a finding when the entrypoint prevents SIGTERM from reaching the JVM, so framework shutdown never runs and the process relies on SIGKILL.

### JVM-016: Readiness withdrawal and request draining

**Severity:** Critical  
**Category:** health  
**Applies when:** The application serves traffic or performs readiness-gated work and can be terminated by the platform.

**Requirement:** Stop accepting new work before termination and allow in-flight work to complete within a bounded budget.

**Evidence to inspect:** Spring Boot graceful shutdown, `spring.lifecycle.timeout-per-shutdown-phase`, `server.shutdown`, readiness health group and availability-state transitions, Kubernetes termination grace period and `preStop` when repository-owned, ingress/mesh draining context.  
**Finding condition:** Emit a finding when readiness is not withdrawn before shutdown begins, new work is accepted after termination starts, draining is unbounded, the application shutdown budget exceeds the platform termination budget, or persistent, streaming, and long-running requests have no defined termination behavior.

**Rules:** Do not hardcode a universal duration. The application shutdown timeout must fit within the platform termination budget with safety margin.

### JVM-017: Background work and messaging shutdown

**Severity:** Critical  
**Category:** lifecycle  
**Applies when:** Consumers, schedulers, executors, or producers run outside the request path.

**Requirement:** Consumers, schedulers, executors, and producers must stop intake, drain or checkpoint safely, and close in dependency-safe order.

**Evidence to inspect:** Kafka/Cassandra/client sessions, acknowledgments, offsets, leases, scheduled jobs, async executors, connection pools.  
**Finding condition:** Emit a finding when shutdown acknowledges before durable completion, abandons non-idempotent work without recovery, accepts new tasks after readiness withdrawal, or closes a dependency before its users.

### JVM-018: Shutdown hooks and lifecycle ownership

**Severity:** High  
**Category:** lifecycle  
**Applies when:** The application registers cleanup through framework callbacks or JVM shutdown hooks.

**Requirement:** Lifecycle resources must have one clear owner and bounded close behavior.

**Evidence to inspect:** `@PreDestroy`, `DisposableBean`, `SmartLifecycle` phases, JVM shutdown hooks, `AutoCloseable`, executor `shutdown`/`awaitTermination`.  
**Finding condition:** Emit a finding when cleanup is duplicated across framework and raw JVM hooks, a hook depends on an already-closed service, a hook waits indefinitely, or a hook performs an unsafe remote mutation without idempotency or recovery design.

### JVM-019: Forced termination and recovery

**Severity:** Critical  
**Category:** recovery  
**Applies when:** Durable, non-idempotent, or externally visible work can be in flight at process loss.

**Requirement:** Design for expiration of the graceful period and abrupt process or container loss.

**Evidence to inspect:** Durable work state, idempotency/deduplication, replay/reconciliation, transaction boundaries, startup recovery, poison-work handling.  
**Finding condition:** Emit a finding when correctness depends on the graceful period completing, or abrupt process or container loss can lose or duplicate work without replay, reconciliation, or startup recovery.

**Rules:** Graceful shutdown is not a substitute for crash consistency.

### JVM-020: Runtime observability baseline

**Severity:** High  
**Category:** observability  
**Applies when:** The application runs as a long-lived JVM workload.

**Requirement:** Provide actionable, bounded telemetry for heap/non-heap, GC pause and cycle behavior, allocation pressure, process RSS, CPU throttling, thread/executor saturation, class loading, open descriptors, direct buffers, and shutdown progress.

**Evidence to inspect:** Micrometer/Actuator metric exposure, JVM metric binders, exported metric names, log and trace configuration, diagnostic endpoints.  
**Finding condition:** Emit a finding when baseline runtime signals are absent so memory, saturation, throttling, or shutdown progress cannot be diagnosed, or telemetry exposes secrets, queries, payloads, or personal data, or uses unbounded metric cardinality.

**Rules:** Use JFR/jcmd/jstack/jmap only under approved operational procedures.

### JVM-021: Resource limits and coordinated budgets

**Severity:** Critical  
**Category:** budget-coordination  
**Applies when:** Repository-owned timeout, concurrency, memory, or lifecycle budgets interact with an adjacent platform or caller budget.

**Requirement:** Coordinate JVM, application, client, mesh, gateway, load balancer, and orchestrator budgets.

**Evidence to inspect:** Shutdown phase timeouts, termination grace period, request and client timeouts, executor concurrency, heap and native sizing, startup-probe budget.  
**Finding condition:** Emit a finding when a repository-owned budget contradicts an adjacent budget, such as shutdown phases exceeding termination grace, a request timeout exceeding the caller timeout, heap plus native headroom exceeding container memory, or startup exceeding the startup-probe budget.

**Examples:** request timeout < caller timeout; shutdown phases < pod termination grace; executor concurrency <= safe downstream concurrency; heap + native headroom < container memory; startup completion < startup-probe budget.

**Hard numbers:** Illustrative unless approved by workload evidence and architecture context.

### JVM-022: Validation requirements for runtime changes

**Severity:** High  
**Category:** testing  
**Applies when:** A change affects runtime flags, memory sizing, garbage collection, concurrency, or lifecycle behavior.

**Requirement:** Applicable runtime changes must carry validation evidence.

**Evidence to inspect:**

- JVM startup with the effective production image and flags
- Effective settings capture such as `-XshowSettings:vm`, `-XX:+PrintFlagsFinal`, or approved equivalent
- Container-limited memory and CPU tests
- Representative load, allocation, and soak testing
- GC/JFR review for pauses, cycles, allocation, pinning, and safepoints
- OOM and container-OOM behavior tests in a safe environment
- Graceful SIGTERM test with in-flight requests and background work
- Forced-kill recovery test for durable operations
- Security/privacy review of diagnostics and dumps

**Finding condition:** Emit a finding when an applicable runtime change is proposed or merged without the required startup, container-limited, load, fault, shutdown, and diagnostics validation evidence.

## Finding and planning rules

- Findings require repository-owned evidence of noncompliance with an applicable control.
- Use the control `severity` and `category` declared in frontmatter; do not reassign severity per finding.
- Return `not_assessed` when the repository lacks evidence to evaluate an applicable control.
- Do not create infrastructure findings when limits, kubelet behavior, node topology, or production telemetry are unavailable.
- Separate code/configuration remediation from platform actions and evidence requests.
- Preserve business logic, partner contracts, security, and privacy behavior.
- Collector, heap, thread, timeout, and shutdown values must remain externally configurable where appropriate.
- Library/JDK upgrades require compatibility, rollback, test, and deployment plans.
- Line numbers are advisory; use path, symbol/key, excerpt, fingerprint, and snapshot as stronger locators.

## Required assessment output

```yaml
jvm_runtime_assessment:
  effective_jdk: "<version-or-unknown>"
  runtime_source: "<build|container|pipeline|context|unknown>"
  container_awareness: "<compliant|non_compliant|not_assessed|not_applicable>"
  heap_strategy: "<fixed|percentage|ergonomic|mixed|unknown>"
  garbage_collector: "<collector-or-unknown>"
  virtual_threads:
    status: "<enabled|disabled|not_detected|unknown>"
    applicability: "<applicable|not_applicable|not_assessed>"
  graceful_shutdown:
    status: "<configured|not_configured|partial|not_assessed>"
    platform_budget_alignment: "<aligned|conflict|unknown|not_applicable>"
  evidence_gaps: []
  applicable_controls: []
  not_assessed_controls: []
```

Pipe-delimited placeholders describe allowed values only. Generated artifacts must contain one concrete value.


## DSE/Kafka Active-Active Runtime Considerations

Validate that JVM resource bounds, shutdown, executor draining, and connection recovery do not strand Kafka work or Cassandra mutations during regional transition. These runtime controls do not authorize business logic changes.
