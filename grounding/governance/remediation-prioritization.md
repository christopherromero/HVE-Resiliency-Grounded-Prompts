---
document_type: remediation_prioritization_policy
schema_version: "1.0"
policy_id: AA-REMEDIATION-PRIORITY
policy_version: "1.0.0"
last_updated: "2026-08-25"
owner: Cloud Architecture Team
lifecycle_status: active
applies_to:
  - springboot-active-active-code-assessment
  - active-active-remediation-planning
assessment_scope: application_code_only
priority_levels:
  P0:
    name: Blocking/Critical Risk
    target_start: immediate
    target_completion: before_active_active_release
  P1:
    name: High Priority
    target_start: current_remediation_wave
    target_completion: before_failover_certification
  P2:
    name: Non-blocking Improvement/Best Practice
    target_start: planned_remediation
    target_completion: before_full_active_active_enablement
  P3:
    name: Non-Blocking Code Consistency (Best Practices / Maintainability)
    target_start: planned_backlog
    target_completion: before_operational_acceptance
default_rules:
  severity_does_not_equal_priority: true
  evidence_required: true
  rationale_required: true
  rule_id_required: true
  priority_assigned_per_root_cause_change: true
  human_override_allowed: true
  override_reason_required: true
  override_approver_required: true
  tests_inherit_behavior_priority: true
  highest_applicable_priority_wins: true
excluded_work:
  - compliant_controls
  - not_assessed_controls
  - not_applicable_controls
  - accepted_risks
  - infrastructure_deployment
  - pcf_modernization
  - pcf_migration
---

# Active-Active Remediation Prioritization Policy

## Purpose

This policy defines how HVE Task Planner assigns P0, P1, P2, and P3 remediation priorities to approved application-code findings from the Spring Boot on AKS active-active assessment.

Priority determines remediation order and release gating. Finding severity describes potential impact. Severity and priority are related but are not interchangeable.

## Mandatory planning behavior

Task Planner must:

1. Assign priority only to a root-cause change mapped to one or more approved `non_compliant` findings.
2. Select the highest applicable priority rule when more than one rule applies.
3. Cite the policy ID, policy version, and rule ID.
4. Provide a concise evidence-based priority rationale.
5. Keep a validation test in the same priority as the behavior it proves when that test is required to establish release readiness.
6. Record human-approved overrides separately from the calculated priority.
7. Never derive priority from severity alone.
8. Never assign remediation work to PCF exclusions or infrastructure-only observations.

# Priority levels and decision rules

## P0: Blocking/Critical Risk

**Definition**: Code or configuration changes required for the application to start and operate without crashing in both regions or for the global load balancer to determine regional health accurately.

Assign P0 when at least one P0 rule applies.

### Rule P0-AA-001: Application code prevents startup or cause crashes

Apply when application code or configuration prevents successful startup or causes crashes in either region.

### Rule P0-AA-002: Region specific configuration values issue

Apply when Region-specific configuration values must be added, changed, or externalized.

### Rule P0-AA-003: Health endpoint missing

Apply when a health endpoint must be created because none exists.

### Rule P0-AA-004: Existing Health probe missing dependencies

Apply when an existing health probe does not include all critical application dependencies.

### Rule P0-AA-005: Align prerequisite priorities

Apply when prerequisites for other P0 resiliency fixes: if fixing A is required before fixing B, and B is P0, then A is also P0.

### Rule P0-AA-006: Same artifact cannot operate in both regions

Apply when region-specific code, builds, artifacts, profiles, or hardcoded endpoints prevent the same immutable application artifact from operating correctly in both regions.

### Rule P0-AA-007: Local-region affinity is violated

Apply when a normally operating application deployment can use a remote-region dependency instead of its local regional dependency, contrary to the approved target behavior.

### Rule P0-AA-008: Failed regional deployment remains eligible for traffic

Apply when sustained failure of a critical local dependency does not cause the application to become not ready, allowing the failed deployment or region to remain eligible for traffic.

### Rule P0-AA-009: External failure creates liveness restart loops

Apply when an external dependency failure causes liveness failure, repeated pod restarts, or a startup/restart loop that cannot restore service.

### Rule P0-AA-010: Local state prevents regional traffic movement

Apply when required session, workflow, transaction, or business state exists only in pod-local or region-local volatile storage and requests cannot safely move to the other region.

### Rule P0-AA-012: Active-active operation creates immediate material data-integrity risk

Apply when duplicate execution, unsafe transaction retry, concurrency conflict, or replay behavior would make a critical business transaction unsafe when both regions are active.

### Rule P0-AA-013: Defect blocks meaningful regional failure testing

Apply when the defect prevents the team from executing or interpreting active-active regional failure tests.

### Rule P0-AA-014: Missing graceful shutdown for authoritative processing

- rule_id: P0-RCV-014

  title: Missing graceful shutdown for authoritative processing

  priority: P0

  category: recovery

  applies_when:

    - finding:
        control_id: APP-AA-017

    - condition:
        graceful_shutdown_missing

    - workload:
        authoritative_processing

  authoritative_processing:

    - payment_processing
    - financial_processing
    - kafka_consumer
    - event_processing
    - scheduler
    - durable_state_mutation
    - transaction_processing

  rationale: >
    The application performs authoritative business processing and
    lacks graceful shutdown behavior.

    Pod termination, deployment, autoscale operations, node drain,
    infrastructure maintenance, failover, or recovery operations
    can interrupt in-flight work and create duplicate processing,
    lost processing, inconsistent state, or incorrect business
    outcomes.

    Because authoritative processing correctness is affected,
    the missing graceful-shutdown implementation represents
    an immediate resiliency risk.

  implementation_guidance: >
    Implement readiness withdrawal, work draining,
    ownership release, offset safety, and bounded completion
    before process termination.

  examples:

    - Kafka consumer processing authoritative state

    - Payment transaction processing

    - Durable workflow execution

    - Scheduled business processing

    - Order fulfillment processing

## P1: High Priority

**Definition**: Generic, region-agnostic resiliency changes required to preserve current production behavior after multi-region deployment.

Assign P1 when no P0 rule applies and at least one P1 rule applies.

### Rule P1-RCV-001: Retry logic or circuit breakers are required

Apply when retry logic or circuit breakers are required.

### Rule P1-RCV-002: Timeout tuning is required

Apply when timeout tuning is required.

### Rule P1-RCV-003: Local caching must be replaced with distributed caching

Apply when local caching must be replaced with distributed caching.

### Rule P1-RCV-004: Idempotency controls are required

Idempotency controls are required.

### Rule P1-RCV-005: Latency, processing, logging, or exception handling must change

Apply when without the change, requests may still succeed, but latency, processing, logging, or exception handling could differ from current production behavior.

### Rule P1-RCV-006: Calls can exceed the failure-detection budget

Apply when missing or excessive timeouts can delay health transition, consume request capacity, or prevent traffic draining within the required budget.

### Rule P1-RCV-007: Retry behavior amplifies failure

Apply when retries are unbounded, immediate, unsafe, or likely to cause retry storms, duplicate side effects, or dependency overload.

### Rule P1-RCV-008: Failure is not isolated

Apply when a missing circuit breaker, bulkhead, or equivalent isolation mechanism can exhaust shared threads, sockets, connection pools, or other application resources.

### Rule P1-RCV-009: Application cannot recover without restart

Apply when the application cannot reconnect, refresh credentials, recreate clients, or return to readiness after dependency restoration without restarting the process or pod.

### Rule P1-RCV-010: Temporary dependency loss creates startup failure

Apply when temporary startup-time dependency unavailability causes permanent startup failure or crash looping.

### Rule P1-RCV-011: Safe degraded operation is unavailable

Apply when an optional or partially available dependency unnecessarily prevents safe degraded operation.

### Rule P1-RCV-012: Graceful shutdown implementation absent

- rule_id: P1-RCV-012

  title: Graceful shutdown implementation absent

  priority: P1

  category: recovery

  applies_when:

    - finding:
        control_id: APP-AA-017

    - condition:
        graceful_shutdown_missing

  rationale: >
    The application does not implement graceful shutdown,
    readiness withdrawal, work draining, or safe termination
    behavior.

    Lost requests, lost event processing, duplicate processing,
    and failed in-flight operations can occur during deployment,
    node maintenance, autoscale events, pod eviction,
    rolling upgrades, or regional failover.

  implementation_guidance: >
    Add graceful shutdown, readiness transition,
    traffic draining, and bounded completion or abandonment
    of in-flight work.

  examples:

    - Spring Boot server shutdown lifecycle

    - Kafka consumer stop and drain

    - Scheduler stop and ownership release

    - Executor shutdown and await termination

## P2: Non-blocking Improvement/Best Practice

**Definition**: A new architectural pattern, component, or redesign that improves resiliency but is not required to preserve current production behavior or enable multi-region deployment.

**Important**: These findings should still be reported. But they do **not** belong in the resiliency bucket and should not be prioritized above P0/P1 resiliency items. Frame them as code-quality recommendations, not resiliency risks.

Assign P2 when no P0 or P1 rule applies and at least one P2 rule applies.

### Rule P2-DATA-001: Dead-letter queue implementation is required

Apply when Dead-letter queue implementation is required.

### Rule P2-DATA-002: Saga or outbox pattern is required

Apply when Saga or outbox pattern adoption is required.

### Rule P2-DATA-003: Event-sourcing is required

Apply when event-sourcing introduction is required.

### Rule P2-DATA-004: Replication redesign is required

Apply when replication redesign is required.

### Rule P2-DATA-005: Architecture-level change is required

Apply when any comparable architecture-level change is required.

### Rule P2-DATA-006: Idempotency is incomplete

Apply when duplicate requests, retries, or event replay can repeat a business effect, but the issue does not meet P0-AA-006.

### Rule P2-DATA-007: Duplicate and replay handling is incomplete

Apply when messaging or workflow code lacks reliable duplicate detection, replay handling, or checkpoint recovery.

### Rule P2-DATA-008: Transaction retry is unsafe or ambiguous

Apply when transaction retry can repeat an operation, mishandle an unknown commit outcome, or cross an unsafe transaction boundary.

### Rule P2-DATA-009: Concurrency conflicts are not controlled

Apply when multi-region writes can silently overwrite one another or when optimistic or equivalent concurrency handling is absent.

### Rule P2-DATA-010: Ordering or consistency assumption is unsupported

Apply when code relies on global ordering, immediate read-after-write consistency, or another guarantee not established by the approved application behavior.

### P2 elevation rule

Elevate a P2 candidate to P0 under `P0-AA-011` when the condition makes a critical production transaction materially unsafe during active-active operation.



rule_id: P2-SUP-001

title: Mutable runtime image

priority: P2

category: supply_chain

applies_when:

  - finding:
      control_id: APP-SUPPLY-002

  - condition:
      image_digest_not_pinned

rationale: >
  Mutable tags can cause runtime behavior to change
  without repository modification.

  Different image versions may be deployed in
  different environments or regions.

  Repeatability, rollback consistency, vulnerability
  tracking, and deterministic recovery are reduced.

implementation_guidance: >
  Pin runtime images using immutable digests and
  establish image refresh governance.

examples:

  - FROM eclipse-temurin:17-jre@sha256:...

  - FROM mcr.microsoft.com/openjdk/jdk:17@sha256:...


  rule_id: P1-SUP-002

title: Mutable runtime image in regulated or financial processing

priority: P1

applies_when:

  - control_id: APP-SUPPLY-002

  - workload:
      financial_processing
      payment_processing
      pci_scope
      regulated_data
      

## P3: Non-Blocking Code Consistency (Best Practices / Maintainability)

**Definition**: A best-practice, hardening, maintainability, readability, duplication, or consistency improvement that is not required to preserve current production behavior or enable multi-region deployment.

Assign P3 only when no P0, P1, or P2 rule applies.

### Rule P3-OPS-001: Maintainability or readability improvements

Apply when maintainability or readability improvements are required.

### Rule P3-OPS-002: Duplicate code needs to be removed

Apply when duplicate-code removal is required.

### Rule P3-OPS-003: Naming, formatting, or pattern consistency

Apply when Naming, formatting, or pattern consistency exists.

### Rule P3-OPS-004: Non-blocking hardening improvements

Apply when Non-blocking hardening improvements are required.

### Rule P3-OPS-005: Findings that do not match P0, P1, or P2

Apply when findings that do not match P0, P1, or P2.

### Rule P3-OPS-006: Regional telemetry is incomplete

Apply when logs, metrics, traces, or health events do not identify the serving region or dependency context.

### Rule P3-OPS-007: Actionable failure signals are incomplete

Apply when retry exhaustion, circuit state, dependency degradation, or recovery lacks useful telemetry but runtime behavior remains otherwise correct.

### Rule P3-OPS-008: Supplemental failure testing is missing

Apply when additional automated failure tests are desirable but are not the sole proof required for a P0, P1, or P2 behavior.

### Rule P3-OPS-009: Graceful-shutdown verification is incomplete

Apply when the shutdown design exists but automated verification or supporting operational evidence is incomplete.

### Rule P3-OPS-010: Documentation or diagnostics need improvement

Apply when the remaining gap primarily affects operational understanding rather than active-active correctness.

### Test-priority inheritance rule

A missing test must not automatically be assigned P3. When a test is the acceptance evidence for a P0, P1, or P2 change, include that test in the same change and priority as the behavior it validates.

# Severity and priority relationship

Use severity as one input to planning, not as the priority formula.

Examples:

- A critical finding that prevents readiness from changing during a regional dependency failure is P0 under `P0-AA-003`.
- A high-severity unbounded retry finding can be P1 under `P1-RCV-002`.
- A critical idempotency finding is P2 under `P2-DATA-001`, unless it materially makes a critical active-active transaction unsafe, in which case elevate it to P0 under `P0-AA-006`.
- A medium regional telemetry finding is normally P3 under `P3-OPS-001`.

# Priority assignment format

Every planned change must include:

```yaml
priority:
  value: P0
  policy_id: AA-REMEDIATION-PRIORITY
  policy_version: "1.0.0"
  rule_id: P0-AA-003
  rationale: >
    Retry exhaustion for the critical local dependency does not change
    application readiness, so the failed regional deployment remains
    eligible for traffic.
  calculated_priority: P0
  override_applied: false
  override_priority: null
  override_reason: null
  override_approved_by: null
```

# Human override policy

A human may override the calculated priority when business sequencing, maintenance windows, risk acceptance, release dependencies, or another documented constraint requires it.

An override must preserve:

- The calculated priority
- The override priority
- The reason
- The approver
- The approval date

An override does not change the original finding severity or compliance status.

# Planning validation

Before completing a plan, verify:

1. Every change cites one valid rule ID from this policy.
2. The highest applicable priority rule was selected.
3. P2 candidates were evaluated for P0 data-integrity elevation.
4. Required tests inherit the priority of the behavior they validate.
5. Every override is complete and auditable.
6. No priority was assigned solely from finding severity.
7. No work was created for excluded statuses, infrastructure deployment, or PCF.
