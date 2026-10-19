# JVM Runtime Resiliency Grounding Standard

```yaml
standard:
  id: JVM-RUNTIME-RESILIENCY
  version: "1.0.0"
  lifecycle_status: active
  scope: repository-owned JVM and Spring Boot runtime behavior
  infrastructure_findings_allowed: false
```

## Purpose

Evaluate whether repository-owned JVM runtime configuration and application lifecycle behavior support bounded latency, memory safety, container operation, concurrency safety, observable failure, and controlled termination. Do not infer deployed limits or production behavior that are not present in repository evidence or approved context.

## Evidence and authority

Use, in order: build files and runtime version declarations; container entrypoints and JVM environment variables; repository-owned manifests and deployment configuration when enabled; application configuration; source lifecycle/concurrency code; tests; approved architecture context. Preserve path, symbol or configuration key, exact excerpt, fingerprint, snapshot, and advisory line range.

Missing deployed telemetry, limits, or platform configuration is an evidence gap, not application noncompliance. Never prescribe hard numbers without workload evidence, SLOs, load tests, and platform limits.

## Control catalog

### JVM-001 Supported runtime and flag compatibility

**Requirement:** Declare an explicit supported JDK runtime and ensure JVM flags, libraries, agents, and container images are compatible with it.

**Inspect:** Maven/Gradle toolchains, parent/BOM, container base image, CI runtime, JAVA_TOOL_OPTIONS/JAVA_OPTS, removed or experimental flags.

**Noncompliant when:** Repository-owned runtime declarations conflict; flags are invalid for the effective JDK; unsupported preview features are used without explicit enablement and test parity.

### JVM-002 Container awareness

**Requirement:** The effective JDK must honor container memory and CPU limits. Do not disable container support without evidence and approval.

**Inspect:** `-XX:+/-UseContainerSupport`, `-XX:ActiveProcessorCount`, CPU-derived pool sizing, cgroup-compatible JDK version, base image.

**Rules:** Do not infer Kubernetes limits from Java code. Validate effective processor count because it affects GC, ForkJoinPool, parallel streams, virtual-thread scheduling, and framework pools. Treat manually forced processor counts as requiring rationale and validation.

### JVM-003 Heap sizing against total container memory

**Requirement:** Heap sizing must leave measured headroom for metaspace, code cache, thread stacks, direct/native buffers, GC structures, JIT, agents, libc, and application-native allocations.

**Inspect:** `-Xms`, `-Xmx`, `-XX:InitialRAMPercentage`, `-XX:MaxRAMPercentage`, `-XX:MinRAMPercentage`, container limits, direct-memory configuration, thread counts.

**Noncompliant when:** Heap equals or nearly consumes the container limit; contradictory fixed and percentage sizing is unexplained; a fixed heap is copied across materially different pod sizes; no allowance exists for known native-heavy workloads.

**Guidance:** Prefer one governed sizing strategy. Percentages are not automatically safe. Validate peak RSS, live set after GC, allocation rate, native memory, and OOM behavior under representative load.

### JVM-004 Heap stability and leak detection

**Requirement:** Demonstrate stable live-set behavior and bounded allocation under steady and degraded load.

**Evidence:** GC logs, JFR, heap histograms/dumps in safe environments, allocation profiles, soak tests, cache bounds, queue bounds.

**Findings:** Unbounded caches/collections/queues, retained request context, listener leaks, classloader leaks, or retry amplification are findings only with repository evidence. Missing production heap telemetry is an evidence gap.

### JVM-005 Garbage collector selection

**Requirement:** Use a collector supported by the effective JDK and justified by latency, throughput, heap, CPU, and operational objectives.

**Inspect:** explicit collector flags, default reliance, pause goals, allocation rate, humongous allocations, concurrent-cycle headroom.

**Rules:** Do not claim one collector is universally best. G1 is a general-purpose default on modern server-class HotSpot. Low-latency collectors such as ZGC require compatible runtimes and sufficient CPU/memory headroom. Collector changes require benchmark and fault validation.

### JVM-006 GC configuration safety

**Requirement:** Avoid obsolete, contradictory, or cargo-cult GC flags. Keep the minimum set necessary and document intent.

**Inspect:** pause targets, initiating occupancy, region sizing, survivor/tenuring overrides, explicit GC behavior, uncommit settings.

**Noncompliant when:** Unsupported flags prevent startup; mutually inconsistent collectors are selected; tuning hides allocation/leak defects; `System.gc()` is used as a correctness or routine capacity mechanism.

### JVM-007 GC observability

**Requirement:** Enable version-compatible GC logging sufficient to associate pauses, concurrent cycles, allocation pressure, promotion/evacuation failures, and heap occupancy with incidents while controlling retention and sensitive-data exposure.

**Expected:** timestamped unified logging where supported, rotation/collection strategy, correlation with application latency, alerting based on symptoms rather than arbitrary single-event thresholds.

### JVM-008 Out-of-memory behavior and diagnostics

**Requirement:** OOM behavior must be deterministic, observable, and compatible with platform restart policy.

**Inspect:** `-XX:+HeapDumpOnOutOfMemoryError`, dump path and storage capacity/security, `-XX:+ExitOnOutOfMemoryError` or approved equivalent, orchestrator restart behavior, incident collection.

**Rules:** A heap dump may contain secrets or personal data and needs access controls and retention. Do not use `CrashOnOutOfMemoryError` without operational approval. Distinguish Java heap, metaspace, direct buffer, native-thread, and container OOMKill failure modes.

### JVM-009 Native and off-heap memory

**Requirement:** Bound and observe non-heap consumers.

**Inspect:** direct buffers/Netty, mmap, compression/native clients, metaspace, code cache, JNI, thread stacks, agents, glibc arenas; `-XX:MaxDirectMemorySize` only when appropriate.

**Validation:** Native Memory Tracking may assist diagnosis but adds overhead and should be enabled deliberately. Container RSS is the capacity authority, not Java heap usage alone.

### JVM-010 Thread and executor bounds

**Requirement:** Platform-thread pools and queues must be bounded according to downstream capacity and overload behavior.

**Inspect:** ThreadPoolExecutor sizes/queues/rejection, scheduler pools, connection pools, ForkJoinPool/common pool, parallel streams, blocking calls, thread-local retention.

**Noncompliant when:** Unbounded queueing hides overload; pool size materially exceeds downstream capacity without rationale; rejection loses critical work silently; shutdown does not drain or account for tasks.

### JVM-011 Virtual-thread eligibility

**Requirement:** Use virtual threads only on a compatible JDK and for high-concurrency tasks dominated by blocking I/O. They improve scalability, not per-request speed, and do not remove downstream limits.

**Inspect:** JDK 21+ production use, framework enablement, executor creation, JDBC/HTTP/client behavior, connection pools, rate limits, CPU-bound work.

**Rules:** Do not pool virtual threads to limit concurrency; use semaphores/rate limits/bulkheads for scarce resources. Do not migrate CPU-intensive loops expecting throughput gains. Preserve transaction, security-context, observability, and cancellation semantics.

### JVM-012 Virtual-thread pinning and compatibility

**Requirement:** Assess pinning and library compatibility under representative load.

**Inspect:** blocking while holding `synchronized` monitors on applicable JDKs, native/foreign calls, long critical sections, carrier starvation symptoms, JFR pinned-thread events and thread dumps.

**Rules:** Do not label every synchronized block a finding. Require a blocking path and material concurrency risk. Consider effective JDK improvements before remediation. Replace synchronization only when thread safety and business behavior remain correct.

### JVM-013 Virtual-thread observability and context

**Requirement:** Observability must remain useful at virtual-thread scale.

**Inspect:** thread names, trace/MDC propagation, ThreadLocal/InheritableThreadLocal use, per-thread caches, dumps/JFR, metrics cardinality.

**Noncompliant when:** Per-thread state creates unbounded memory at expected concurrency; security or tracing context is lost; monitoring assumes a small fixed thread population.

### JVM-014 Safepoints, JIT, and startup

**Requirement:** Detect JVM latency and startup risks outside GC.

**Inspect:** safepoint logs/JFR, class loading, deoptimization, code-cache pressure, startup probes, CDS/AppCDS where supported, classpath scanning, eager initialization.

**Rules:** Do not attribute every pause to GC. Startup optimization must not bypass required validation, security initialization, migrations, or readiness gates.

### JVM-015 Graceful shutdown signal handling

**Requirement:** PID 1 must receive SIGTERM and initiate framework shutdown. Entrypoints must use `exec` or equivalent signal forwarding; do not rely on SIGKILL or IDE termination.

**Inspect:** Docker ENTRYPOINT/CMD, shell scripts, tini/dumb-init where approved, Spring shutdown settings, shutdown hooks.

### JVM-016 Readiness withdrawal and request draining

**Requirement:** Stop accepting new work before termination and allow in-flight work to complete within a bounded budget.

**Inspect:** Spring Boot graceful shutdown, `spring.lifecycle.timeout-per-shutdown-phase`, readiness transition, Kubernetes termination grace period and preStop when repository-owned, ingress/mesh draining context.

**Rules:** Application shutdown timeout must fit within the platform termination budget with safety margin. Do not hardcode a universal duration. Persistent connections, streaming, and long-running requests need explicit behavior.

### JVM-017 Background work and messaging shutdown

**Requirement:** Consumers, schedulers, executors, and producers must stop intake, drain or checkpoint safely, and close in dependency-safe order.

**Inspect:** Kafka/Cassandra/client sessions, acknowledgments, offsets, leases, scheduled jobs, async executors, connection pools.

**Noncompliant when:** Shutdown can acknowledge before durable completion, abandon non-idempotent work without recovery, accept new tasks after readiness withdrawal, or close dependencies before users.

### JVM-018 Shutdown hooks and lifecycle ownership

**Requirement:** Lifecycle resources must have one clear owner and bounded close behavior.

**Inspect:** `@PreDestroy`, DisposableBean, SmartLifecycle phases, JVM shutdown hooks, AutoCloseable, executor shutdown/awaitTermination.

**Rules:** Avoid duplicate cleanup registered in framework and raw JVM hooks. Hooks must not depend on already-closed services, wait indefinitely, or call unsafe remote mutations without idempotency/recovery design.

### JVM-019 Forced termination and recovery

**Requirement:** Design for expiration of the graceful period and abrupt process/container loss.

**Expected:** Durable work state, idempotency/deduplication, replay/reconciliation, transaction boundaries, startup recovery, poison-work handling. Graceful shutdown is not a substitute for crash consistency.

### JVM-020 Runtime observability baseline

**Requirement:** Provide actionable, bounded telemetry for heap/non-heap, GC pause and cycle behavior, allocation pressure, process RSS, CPU throttling, thread/executor saturation, class loading, open descriptors, direct buffers, and shutdown progress.

**Rules:** Use JFR/jcmd/jstack/jmap only under approved operational procedures. Avoid unbounded metric cardinality and exposing secrets, queries, payloads, or personal data.

### JVM-021 Resource limits and coordinated budgets

**Requirement:** Coordinate JVM, application, client, mesh, gateway, load balancer, and orchestrator budgets.

**Examples:** request timeout < caller timeout; shutdown phases < pod termination grace; executor concurrency <= safe downstream concurrency; heap + native headroom < container memory; startup completion < startup-probe budget.

**Hard numbers:** Illustrative unless approved by workload evidence and architecture context.

### JVM-022 Validation requirements

For applicable changes, require:

- JVM startup with the effective production image and flags
- Effective settings capture such as `-XshowSettings:vm`, `-XX:+PrintFlagsFinal`, or approved equivalent
- Container-limited memory and CPU tests
- Representative load, allocation, and soak testing
- GC/JFR review for pauses, cycles, allocation, pinning, and safepoints
- OOM and container-OOM behavior tests in a safe environment
- Graceful SIGTERM test with in-flight requests and background work
- Forced-kill recovery test for durable operations
- Security/privacy review of diagnostics and dumps

## Finding and planning rules

- Findings require repository-owned evidence of noncompliance with an applicable control.
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
