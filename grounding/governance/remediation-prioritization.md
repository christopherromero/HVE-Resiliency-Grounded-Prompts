---
document_type: remediation_prioritization_policy
schema_version: "1.1.0"
policy_id: AA-REMEDIATION-PRIORITY
policy_version: "1.2.0"
last_updated: "2026-09-20"
owner: Cloud Architecture Team
lifecycle_status: proposed
supersedes: "AA-REMEDIATION-PRIORITY 1.1.0"
applies_to:
  - springboot-active-active-code-assessment
  - active-active-remediation-planning
assessment_scope:
  - application_code
  - application_configuration

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
  highest_applicable_priority_wins: true
  human_override_allowed: true
  override_reason_required: true
  override_approver_required: true
  prerequisite_priority_inheritance: false
  standalone_test_finding_inherits_behavior_priority: false
  behavior_validation_tests_inherit_behavior_priority: true

cache_rules:

  default_priority: P3

  applies_to:
    - cache_size
    - cache_eviction
    - cache_staleness

  elevate_to:

    P2:
      - material_degradation_of_recovery

    P1:
      - customer_visible_incorrect_processing

    P0:
      - failover_failure
      - memory_driven_outage
      - loss_of_accepted_work

graceful_transition_rules:

  default_priority: P2

  applies_to:
    - graceful_shutdown
    - executor_drain
    - termination_drain

  elevate_to:

    P1:
      - repeated_duplicate_processing

    P0:
      - duplicate_payment
      - unrecoverable_state_divergence
      - loss_of_accepted_work

backpressure_rules:

  default_priority: P2

  applies_to:
    - executor_queue_bounds
    - rejection_policy
    - backpressure

  elevate_to:

    P1:
      - service_instability

    P0:
      - lost_accepted_work
      - memory_driven_outage
      - promotion_failure


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

## 1. Purpose

This policy defines how Task Planner assigns P0, P1, P2, and P3 remediation priorities to evidence-backed application-code and application-configuration findings.

Priority represents the impact of the defect itself. Priority must not be increased solely because a change is a prerequisite, a release gate, a test dependency, difficult to implement, or required earlier in an implementation wave.

Severity describes potential impact. Priority determines remediation order and release gating. Severity and priority are related inputs but are not interchangeable.

## 2. Mandatory decision sequence

For every root-cause finding or change, evaluate rules in this order:

1. Confirm that the finding is evidence-backed and within the enabled assessment scope.
2. Determine the finding classification using `RESILIENCY-FINDING-QUALIFICATION`.
3. Evaluate the numbered P0 rules in this policy.
4. If no P0 rule applies, evaluate the numbered P1 rules.
5. If no P0 or P1 rule applies, evaluate P2 rules.
6. Assign P3 only when no P0, P1, or P2 rule applies.
7. Record remediation dependencies, release gates, implementation waves, approvals, and test obligations separately from finding priority.
8. Cite exactly one primary numbered priority rule. Additional applicable rules may be recorded as secondary rules.

A priority decision is invalid when it cites an undefined rule ID or relies only on an unnumbered policy statement.

## 3. Priority must be based on

- Direct runtime or configuration impact of the finding
- Credible failure scenario established by evidence
- Availability or traffic-eligibility impact
- Accepted-work loss or false acknowledgement
- Authoritative-state corruption or unrecoverable divergence
- Regional failover or workload-ownership impact
- Recoverability and durability impact
- Material security or normal-operation correctness impact for non-resiliency findings

## 4. Priority must not be based on

- Remediation owner or implementation team
- Implementation effort, complexity, funding, or story points
- Implementation wave or sequencing preference
- The priority of a dependent change
- The fact that a change is a prerequisite for another change
- The need to test, certify, or document another remediation
- Confidence level alone
- Severity alone

## 5. Separation of priority, dependencies, and release gates

Every plan must record these dimensions independently:

- `priority`: impact of the defect itself
- `depends_on_change_ids`: technical implementation dependencies
- `required_by_change_ids`: downstream changes requiring this change
- `release_gate`: evidence or condition required before release
- `implementation_wave`: dependency and rollout ordering
- `approval_required`: business, architecture, security, privacy, or partner approval

A P1 prerequisite for a P0 remediation remains P1. The P0 remediation may not close until its P1 prerequisite is complete, but the prerequisite does not inherit P0.

## 6. Test and verification policy

### 6.1 Tests attached to a behavior change

Tests that prove a P0, P1, or P2 behavior remain part of that behavior change and inherit its implementation priority. This inheritance applies to the test task, not to a separate missing-test finding.

### 6.2 Standalone missing-test findings

A standalone finding whose root cause is only missing test coverage, a missing shared harness, or insufficient verification is normally:

- P2 under `P2-ASSURE-001`, or
- P3 under `P3-ASSURE-001` when supplemental only.

A standalone missing-test finding must not become P0 or P1 solely because it would test P0 or P1 behaviors. The test suite may still be a mandatory release gate.

### 6.3 Runtime defect that prevents failover testing

A runtime or configuration defect that prevents the application from entering, surviving, or recovering from a regional failure is prioritized by the underlying runtime rule. Do not use missing observability or missing tests alone to classify it as P0.

## 7. P0: Blocking or Critical Risk

Assign P0 only when repository-owned code or application configuration establishes at least one direct blocking or critical condition below.

### P0-AA-001: Application cannot start or repeatedly crashes in an approved target region

Apply when code or application configuration directly prevents successful startup or causes a repeatable crash or restart loop in an approved target region.

Evidence must establish the startup or crash mechanism. A theoretical dependency outage without evidence of startup prevention is not sufficient.

### P0-AA-002: Same immutable artifact cannot operate in both active regions

Apply when region-specific code, builds, artifacts, profiles, or hardcoded endpoints prevent the same approved artifact from operating correctly in both regions.

### P0-AA-003: Required local-region dependency affinity is violated

Apply when repository behavior can direct a normally operating regional deployment to an unauthorized remote-region dependency and that behavior violates the approved target design.

### P0-AA-004: Failed deployment remains eligible for GLB traffic

Apply when sustained failure of a critical serving dependency leaves the application ready or otherwise traffic-eligible, causing the GLB to continue routing requests to a deployment that cannot provide its critical capability.

### P0-AA-005: Local volatile state blocks safe traffic movement

Apply when required session, workflow, transaction, or business state exists only in pod-local or region-local volatile storage and requests cannot move safely to the other active region.

### P0-AA-006: Active-active operation creates immediate material authoritative-state corruption

Apply when concurrent regional operation, duplicate execution, replay, unsafe transaction retry, or an unsupported consistency assumption can directly and materially corrupt authoritative business state.

### P0-AA-007: Active-standby workload ownership is unenforced and creates both-active or stale-active processing risk

Apply when an approved active-standby workload can process concurrently in more than one region, or a former active instance cannot be fenced, and the workload mutates authoritative state or performs critical business processing.

### P0-DUR-001: Accepted work can be permanently lost or become unrecoverable

Apply when all are established:

- The application or its messaging boundary has accepted the work.
- Repository behavior can permanently discard, skip, or lose that work.
- No durable quarantine, retry, reconciliation, replay, or recovery record remains.
- The lost work has material business or authoritative-state impact.

Examples include advancing a Kafka offset after abandoning authoritative processing with no durable recovery path.

### P0-DUR-002: False acknowledgement before durable acceptance

Apply when the application reports success or completes an accepted operation before the required durable system has accepted or durably recorded the work, and a failure can produce permanent loss or unrecoverable divergence.

Do not apply when the defect only reduces telemetry or when another finding already captures the actual cross-store divergence and this finding is only a supporting producer configuration control.

### P0-DUR-003: Cross-store divergence is permanent and unreconciled

Apply when a critical business transaction updates authoritative state and another durable system, but repository behavior can leave the two permanently inconsistent with no durable intent, reconciliation marker, outbox, or compensating recovery path.

### P0-RCV-001: Regional promotion or recovery action can corrupt authoritative state

Apply when the approved promotion, replay, offset restoration, retry, or recovery mechanism itself can directly corrupt authoritative state or repeat a material business effect.

### P0-SEC-001: Repository evidence establishes an immediately exploitable critical application security condition

Apply only when application code or configuration evidence establishes both the critical weakness and its reachable impact within the enabled assessment scope. Do not infer network reachability from absent deployment evidence.

## 8. P1: High Priority

Assign P1 when no P0 rule applies and the defect materially increases outage duration, failure amplification, recovery difficulty, data inconsistency risk, security exposure, or normal-operation correctness risk.

### P1-RCV-001: Bounded retry or transient-failure classification is required

Apply when expected transient failures, conflicts, or failover transitions become terminal customer-visible failures because safe bounded retry or outcome classification is absent.

### P1-RCV-002: Timeout and failure-budget configuration is required

Apply when missing or excessive timeouts can delay failure detection, consume request or listener capacity, or exceed the required request, readiness, or shutdown budget.

A timeout finding remains P1 even when a P0 readiness implementation depends on it. Record the dependency separately.

### P1-RCV-003: Dependency isolation or safe degraded operation is absent

Apply when missing circuit breaking, bulkheading, pool isolation, cache error handling, or safe degraded behavior allows one dependency to remove otherwise healthy application capability.

### P1-RCV-004: Idempotency or stable event identity is required but direct P0 authoritative-state corruption is not established

Apply when duplicate processing is possible during failover or recovery, but the finding does not itself meet P0-AA-006 or P0-RCV-001.

### P1-RCV-005: Application cannot recover without restart

Apply when the application cannot reconnect, refresh credentials, recreate clients, restore readiness, or resume service after dependency restoration without restarting the process or pod.

### P1-RCV-006: Temporary startup dependency loss materially delays recovery but does not establish a target-region startup blocker

Apply when startup is degraded, delayed, or fragile but the evidence does not establish P0-AA-001.

### P1-RCV-007: Graceful termination is absent

Apply when the application lacks readiness withdrawal, request draining, listener draining, ownership release, or bounded termination and routine termination can interrupt work.

Elevate to P0 only when the finding also satisfies P0-DUR-001, P0-AA-006, or another numbered P0 rule through direct evidence of permanent accepted-work loss or authoritative-state corruption. Authoritative processing alone is not an automatic P0.

### P1-RCV-008: Failure and recovery signals are insufficient

Apply when operators cannot reliably detect a material dependency or processing failure, cannot verify recovery, or cannot determine whether a required workload is operating in the intended region.

Missing correlation, regional dimensions, or root-cause diagnostics alone are P2 unless they are inseparable from absent actionable failure and recovery signals in the same root cause.

### P1-RCV-009: Overload or unbounded resource consumption can remove regional capacity

Apply when application code contains an unbounded or inadequately isolated consumption path involving heap, threads, sockets, connections, queues, cache load, or result materialization that can materially impair availability.

### P1-DUR-001: Producer durability and outcome handling are incomplete

Apply when acknowledgment, idempotent producer configuration, send-result handling, delivery timeout, or failure signaling is absent, but the finding does not independently satisfy P0-DUR-002 or P0-DUR-003.

### P1-CORRECT-001: Material normal-operation correctness defect

Apply to non-resiliency findings when repository behavior can return materially incorrect business data, process malformed mandatory input, violate an established contract, or produce incorrect business outcomes during otherwise healthy operation.

### P1-SEC-001: High-priority application security or access-control defect

Apply when repository evidence establishes a material application-level security weakness, but the evidence does not establish the immediate critical reachability and impact required by P0-SEC-001.

## 9. P2: Non-blocking Improvement or Best Practice

Assign P2 when no P0 or P1 rule applies and the change improves resilience, assurance, diagnosis, architecture, or correctness without representing a blocking or high-priority defect.

### P2-ARCH-001: New architecture pattern or redesign improves resilience

Apply to optional or non-blocking adoption of an outbox, saga, event sourcing, replication redesign, or comparable architecture pattern when no P0/P1 material risk is established.

### P2-OBS-001: Diagnostic observability improvement

Apply when correlation, regional attribution, tracing, dashboards, or root-cause diagnostics improve incident analysis but runtime failure detection and recovery signals otherwise remain sufficient.

### P2-ASSURE-001: Shared failure or failover verification is missing

Apply to a standalone missing-test or shared-harness finding when runtime findings are separately recorded and the missing assurance does not itself create the failure.

The verification suite may be a mandatory release gate without being P0.

### P2-CORRECT-001: Non-blocking correctness or contract improvement

Apply when a correctness or contract issue is real but does not materially affect business outcomes and is not covered by P1-CORRECT-001.

### P2-DATA-001: Duplicate or replay handling is incomplete without material authoritative-state impact

Apply when duplicate or replay behavior exists but does not directly satisfy a P0 or P1 rule.

## 10. P3: Non-blocking Code Consistency and Maintainability

Assign P3 only when no P0, P1, or P2 rule applies.

### P3-OPS-001: Maintainability or readability

Apply to naming, formatting, duplication removal, code consistency, or readability improvements.

### P3-OPS-002: Non-blocking configuration consistency

Apply when externalization, naming, or configuration cleanup improves maintainability without material runtime impact.

### P3-ASSURE-001: Supplemental tests or documentation

Apply when additional tests or documentation are desirable but are not required to prove a governed remediation or satisfy a release gate.

## 11. Observability decision framework

Use the following order:

- P0: Do not assign P0 for observability alone. P0 requires a separate numbered P0 runtime, durability, security, or traffic-eligibility rule.
- P1: Actionable material failure or recovery cannot be detected or verified.
- P2: Failure is detectable, but correlation, regional attribution, or root-cause diagnosis is materially incomplete.
- P3: Visibility improvement is operationally useful but does not materially affect incident response or recovery.

When one finding combines P1 and P2 observability concerns, split the finding or remediation targets when they have distinct root causes and priority characteristics. Do not use the strongest subcondition to elevate unrelated diagnostic enhancements.

## 12. Idempotency and replay framework

- P0: Replay, duplicate execution, or recovery directly corrupts authoritative state or repeats a critical business effect.
- P1: Duplicate processing is possible during failover or recovery, but direct authoritative-state corruption is not established for this service.
- P2: Duplicate handling is incomplete but topology-independent and non-material.
- Non-resiliency: No credible failure, recovery, replay, or failover scenario is established.

## 13. Startup framework

- P0: Evidence establishes that the application cannot start or repeatedly crashes in an approved target region.
- P1: Startup is delayed, fragile, or requires recovery work, but successful startup remains possible.
- P2: Startup diagnostics or bootstrap observability are incomplete.

Compound findings that combine startup availability with schema governance should be split when the causes, evidence, or priorities differ.

## 14. Graceful-termination framework

- P0: Missing termination behavior directly satisfies P0-DUR-001, P0-AA-006, or another numbered P0 rule.
- P1: Missing readiness withdrawal, draining, or bounded completion creates high-priority interruption or duplication risk.
- P2: The design exists but operational verification is incomplete.
- P3: Documentation or minor consistency is incomplete.

## 15. Non-resiliency prioritization

Non-resiliency findings are limited to P2 and P3.

#### P2-NR-001: Material non-resiliency remediation

Assign P2 when an evidence-backed security, correctness, contract, compatibility, performance, assessment-quality, or operational problem warrants planned remediation but does not establish the complete resiliency impact chain.

#### P3-NR-001: Non-resiliency consistency or maintainability

Assign P3 for logging-only improvement, telemetry enhancement, scheduled-run improvement, documentation, maintainability, readability, configuration consistency, or supplemental verification when no material impact requiring P2 is established.

Rules:
- Never assign P0 or P1 to a non-resiliency finding.
- If a finding appears to satisfy P0 or P1, return it to resiliency-classification review.
- Human override may move a non-resiliency finding only between P2 and P3.

## 16. Human override policy

A human may override the calculated priority for documented business sequencing, maintenance windows, risk acceptance, regulatory obligations, or an approved architecture decision.

Every override must retain:

- calculated priority
- override priority
- reason
- approver
- approval date

An override does not change finding severity, classification, evidence, or compliance status.

## 17. Required priority record

```yaml
priority:
  value: P1
  policy_id: AA-REMEDIATION-PRIORITY
  policy_version: "1.2.0"
  rule_id: P1-RCV-002
  secondary_rule_ids: []
  rationale: >
    Repository evidence shows that dependency calls have no explicit timeout,
    so degraded dependencies can exceed the failure-detection budget and consume
    application capacity. The finding is P1 under P1-RCV-002. It is required by
    a P0 readiness change, but prerequisite priority inheritance is prohibited.
  calculated_priority: P1
  override_applied: false
  override_priority: null
  override_reason: null
  override_approved_by: null
  override_approved_at: null
```

## 18. Planning validation

Before completing Step 3A, verify:

- Every change cites a defined numbered rule ID.
- No undefined or obsolete rule ID is referenced.
- Priority is based on the defect itself.
- Prerequisites do not inherit downstream priority.
- Implementation waves do not alter priority.
- Release gates are recorded separately.
- Behavior-specific tests remain with the behavior change and inherit its implementation priority.
- Standalone missing-test findings use P2-ASSURE-001 or P3-ASSURE-001 unless another direct defect is established.
- Accepted-work loss is evaluated against P0-DUR-001.
- False acknowledgement is evaluated against P0-DUR-002.
- Cross-store divergence is evaluated against P0-DUR-003.
- Active-active state corruption is evaluated against P0-AA-006.
- Active-standby workload ownership is evaluated against P0-AA-007.
- Observability findings use the framework in section 11.
- Graceful termination uses the framework in section 14.
- Material non-resiliency correctness and security findings are evaluated for P1.
- Compound findings are split when different root causes or priority characteristics would otherwise be hidden.
- Severity was not used as the sole priority formula.
- Human overrides are complete and auditable.
- Resiliency findings use P0-P3.
- Non-resiliency findings use P2-P3 only.
- No non-resiliency finding appears in the P0 or P1 index.

## 19. Migration guidance from version 1.1.0

Re-evaluate existing plans using these corrections:

- Findings elevated only by former P0-AA-005 prerequisite inheritance should return to their intrinsic priority.
- Former P0-AA-013 testing/interpretation elevations should be reassessed under P1-RCV-008, P2-OBS-001, or P2-ASSURE-001.
- Missing graceful shutdown is P1 unless direct evidence satisfies a numbered P0 rule.
- Accepted-work loss should use P0-DUR-001.
- False acknowledgement should use P0-DUR-002.
- Cross-store divergence should use P0-DUR-003.
- Standalone shared test-harness findings should normally use P2-ASSURE-001.
- Material non-resiliency correctness findings should be evaluated under P1-CORRECT-001.
- Material application security findings should be evaluated under P1-SEC-001 or P0-SEC-001.
- Replace obsolete or inconsistent references to P0-AA-011, the former use of P0-AA-006 for unrelated idempotency elevation, and unnumbered precedence conditions with the defined rules in this version.
