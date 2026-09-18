---
description: "Authoritative Step 3A remediation plan for inventory-service active-active resiliency findings"
applyTo: '.copilot-tracking/changes/**'
---

# Inventory Service Authoritative Remediation Plan

Illustrative proposal only. Every code and configuration block in this artifact is a non-authoritative illustrative proposal. Task Implementor validates the current repository state and produces the final repository-specific implementation.

## 1. Planning Metadata

```yaml
planning:
  schema_version: "2.0"
  phase: remediation_planning
  phase_order: "03A"
  artifact_role: authoritative_remediation_plan
  assessment_run_id: "inventory-service-2026-09-18-001"
  application_name: inventory-service
  repository_root: source/inventory-service
  inventory_artifact: ".copilot-tracking/research/2026-09-18/inventory-service-inventory-research.md"
  review_artifact: ".copilot-tracking/reviews/2026-09-18/inventory-service-inventory-research-review.md"
  plan_artifact: ".copilot-tracking/plans/2026-09-18/inventory-service-remediation-plan.instructions.md"
  planner_agent: task-planner
  generated_at: "2026-09-18T00:00:00Z"
  repository_reinventoried: false
  controls_reassessed: false
  new_findings_created: false
  source_code_modified: false
  infrastructure_remediation_added: false
  pcf_remediation_added: false
  illustrative_code_included: true
  prioritization_policy:
    path: grounding/governance/remediation-prioritization.md
    policy_id: AA-REMEDIATION-PRIORITY
    policy_version: "1.0.0"
  resiliency_qualification_policy:
    path: grounding/governance/resiliency-finding-qualification-policy.yml
    policy_id: RESILIENCY-FINDING-QUALIFICATION
    policy_version: "1.0.0"
    classification_preserved: true
    non_resiliency_findings_suppressed: 0
  approved_libraries:
    path: grounding/governance/approved-libraries.yml
    lifecycle_status: approved
    used_as_approval_authority: true
```

```yaml
assessment_scope_carried_forward:
  carried_from_step_2: true
  recalculated: false
  enabled_domains:
    - application_code
    - application_configuration
  disabled_domains:
    - container_build
    - cicd_pipeline
    - deployment_configuration
    - infrastructure_as_code
    - deployed_infrastructure
  scope_rules:
    repository_owned_only: true
    deployed_infrastructure_findings_allowed: false
    pcf_findings_allowed: false
  report_preferences:
    finding_selection_mode: all_priorities
    included_priorities: [P0, P1, P2, P3]
    testing_output_mode: hidden
  testing_visibility_note: >-
    testing_output_mode hidden is a Step 3B report rendering preference only. Every proposed test,
    acceptance criterion, validation command, and closure obligation in this artifact remains
    authoritative and binding on Step 4 and Step 5.
  remediation_targets_restricted_to:
    - application_code
    - application_configuration
    - repository_owned_build_file
    - repository_owned_test_source
```

```yaml
assessment_snapshot:
  type: workspace_snapshot
  identifier: "inventory-service-workspace-2026-09-18"
  provenance: workspace_generated
  git_commit_sha: not_applicable
  dirty_worktree: not_applicable
  captured_at: "2026-09-18T00:00:00Z"
  preserved_verbatim_from_step_2: true
  limitations:
    - No Git metadata is present at the workspace root or under source/inventory-service, so no commit identifier is available.
    - Evidence is anchored by repository path, symbol, and exact excerpt rather than by revision.
    - Line ranges are advisory navigation metadata and may shift if the source drop is replaced.
  source_locator_precedence:
    - repository_path
    - symbol
    - original_source_excerpt
    - source_fingerprint
    - assessment_snapshot
    - original_line_range
  line_numbers_authoritative: false
  missing_git_is_targeted_discovery: false
```

```yaml
architecture_context_carried_forward:
  carried_from_step_2: true
  recalculated: false
  source_path: application-context/application-architecture-context.yml
  context_status: approved
  context_version: "3.0.0"
  authoritative_state_dependency: azure-sql
  current_deployment_operating_model: active_standby
  approved_target_deployment_operating_model: active_active
  assessment_target_state: approved_target
  architecture_conflict_detected: false
```

```yaml
kafka_scenario_preserved:
  carried_from_step_2: true
  recalculated: false
  redesigned_during_planning: false
  operating_scenario: active_standby
  scenario_source: approved_application_architecture_context
  context_version: "3.0.0"
  scenario_policy_id: KAFKA-OPERATING-SCENARIO
  scenario_policy_version: "3.2.0"
  scenario_rule_id: KAFKA-SCENARIO-001
  scenario_validation_status: consistent
  architecture_confirmation_required: false
  processing_model: mixed
  regional_processing_model: single_active
  external_side_effects: none
  kafka_backed_state: none
  cluster_model_type: independent_regional_clusters
  database_introduced_by_remediation: false
  database_independent_remediation_note: not_applicable
```

## 2. Executive Remediation Strategy

The inventory-service repository is a single Spring Boot 3.3.5 Maven module that serves seven REST endpoints, consumes `order-events`, publishes `inventory-events`, and treats Azure SQL as its authoritative business state. Step 2 recorded 29 verified findings across 85 non-compliant controls, with 26 findings classified `resiliency` and 3 classified `non_resiliency`. The code is assessed against the approved target deployment, which is active-active for the application with an active-standby Kafka operating scenario and an active-standby authoritative database.

Step 3A converts those findings into 24 root-cause changes. The consolidation is deliberate: several findings share one implementation surface, so a single change carries the primary finding and the findings it subsumes. No finding was dropped, reclassified, or reprioritized by severity.

### Strategic shape of the remediation

The remediation divides into four dependency-ordered waves.

Wave 1 establishes the platform contract the rest of the work depends on. Regional traffic eligibility becomes real by putting the authoritative dependency into the readiness group, startup stops being an unbounded remote call, schema changes stop happening at runtime, pod termination becomes a drained transition rather than a cut, and every metric and log record carries a region dimension plus an actual failure signal. Until Wave 1 lands, no other remediation can be observed, validated, or failed over.

Wave 2 makes the regional ownership model expressible and makes authoritative writes replay-safe. The Kafka listener gains an externalized activation contract so a role change becomes a configuration action rather than a redeploy, and order-event processing gains a durable operation identity so promotion replay, rebalance redelivery, and gateway retry stop multiplying stock movements.

Wave 3 installs the region-agnostic resiliency mechanisms that preserve current production behaviour once the service runs in more than one region: bounded deadlines on every remote call, bounded retry with transient classification, conflict handling, dependency isolation, cache failure containment, an explicit cache manager contract, coalesced cache loads, a bounded list endpoint, producer durability, and listener error handling with dead-letter routing.

Wave 4 carries the architectural patterns that improve resiliency but are not required to bring the service into multi-region operation, plus the consolidated fault-injection and failover regression suite.

### Governed priority outcome

Nine changes are P0, twelve are P1, three are P2, and none are P3. Priority was assigned exclusively through `AA-REMEDIATION-PRIORITY` version 1.0.0. Two priority outcomes deserve explicit attention because they diverge from severity.

F-026 carries `medium` severity but its change is P0. Without a region dimension on telemetry, a regional failure test cannot be interpreted and a both-active condition cannot be confirmed or refuted, which is exactly what rule P0-AA-013 governs.

F-002 and F-020 carry `critical` severity but their changes are P2. The transactional outbox is named directly by rule P2-DATA-002 as a P2 architectural adoption, and the cache invalidation gap is a normal-operation correctness defect that rule P2-DATA-010 places at P2. Both were evaluated for P0 elevation and the evaluation is recorded on each change.

### What this plan does not do

No change touches the Dockerfile, the GitHub Actions workflow, the Kubernetes manifests, or any deployed infrastructure. Those artifacts exist in the repository but their assessment domains are disabled, so they remain out of the remediation boundary and their unresolved facts stay recorded as evidence gaps. No PCF work is planned. No change redesigns the Kafka operating scenario, and no remediation introduces a database that the approved architecture does not already declare.

### Approval-gated targets

Six implementation targets change externally observable behaviour and are held at `implementation_allowed: false` until an approval record exists: the dependency-failure HTTP status contract, the optimistic-conflict HTTP status contract, the list-endpoint pagination contract, REST-level idempotency-key semantics, the published event envelope contract, and the outbox publication-timing and delivery semantics. Each target is isolated inside its change so the surrounding resiliency mechanism can proceed without waiting.

### Implementation scope index

```yaml
implementation_scope_index:
  by_priority:
    P0:
      - CHANGE-AA-001
      - CHANGE-AA-002
      - CHANGE-AA-003
      - CHANGE-AA-004
      - CHANGE-AA-005
      - CHANGE-AA-006
      - CHANGE-AA-007
      - CHANGE-AA-008
      - CHANGE-AA-024
    P1:
      - CHANGE-AA-009
      - CHANGE-AA-010
      - CHANGE-AA-011
      - CHANGE-AA-012
      - CHANGE-AA-013
      - CHANGE-AA-014
      - CHANGE-AA-015
      - CHANGE-AA-016
      - CHANGE-AA-017
      - CHANGE-AA-018
      - CHANGE-AA-019
      - CHANGE-AA-020
    P2:
      - CHANGE-AA-021
      - CHANGE-AA-022
      - CHANGE-AA-023
    P3: []
  by_wave:
    "1":
      - CHANGE-AA-001
      - CHANGE-AA-002
      - CHANGE-AA-003
      - CHANGE-AA-004
      - CHANGE-AA-005
      - CHANGE-AA-006
    "2":
      - CHANGE-AA-007
      - CHANGE-AA-008
    "3":
      - CHANGE-AA-009
      - CHANGE-AA-010
      - CHANGE-AA-011
      - CHANGE-AA-012
      - CHANGE-AA-013
      - CHANGE-AA-014
      - CHANGE-AA-015
      - CHANGE-AA-016
      - CHANGE-AA-017
      - CHANGE-AA-018
      - CHANGE-AA-019
      - CHANGE-AA-020
    "4":
      - CHANGE-AA-021
      - CHANGE-AA-022
      - CHANGE-AA-023
      - CHANGE-AA-024
  by_classification:
    resiliency:
      - CHANGE-AA-001
      - CHANGE-AA-002
      - CHANGE-AA-003
      - CHANGE-AA-004
      - CHANGE-AA-005
      - CHANGE-AA-006
      - CHANGE-AA-007
      - CHANGE-AA-008
      - CHANGE-AA-009
      - CHANGE-AA-010
      - CHANGE-AA-011
      - CHANGE-AA-012
      - CHANGE-AA-013
      - CHANGE-AA-014
      - CHANGE-AA-015
      - CHANGE-AA-016
      - CHANGE-AA-017
      - CHANGE-AA-018
      - CHANGE-AA-019
      - CHANGE-AA-020
      - CHANGE-AA-021
      - CHANGE-AA-022
      - CHANGE-AA-024
    non_resiliency:
      - CHANGE-AA-023
    mixed_classification_changes:
      - change_id: CHANGE-AA-015
        note: >-
          Carries resiliency finding F-017 and non_resiliency findings F-018 and F-029 because all three
          are remediated by one RedisCacheConfiguration bean. Classification of each finding is preserved.
```

```yaml
change_counts:
  total_changes: 24
  by_priority: {P0: 9, P1: 12, P2: 3, P3: 0}
  by_wave: {"1": 6, "2": 2, "3": 12, "4": 4}
  by_complexity: {low: 7, medium: 12, high: 5}
  governance_blocked_changes: 0
  priority_overrides_applied: 0
  approval_required_targets: 6
```

## 3. Finding-to-Change Mapping

Every one of the 29 approved findings maps to exactly one primary change, or is explicitly consolidated under another root-cause change. No finding is unmapped and no change exists without an approved non-compliant finding.

```yaml
mapping:
  - {finding_id: F-001, primary_control_id: APP-KAFKA-005, change_id: CHANGE-AA-018, disposition: planned, role: primary, priority: P1, priority_rule_id: P1-RCV-005, implementation_wave: 3, classification: resiliency}
  - {finding_id: F-002, primary_control_id: APP-DB-003, change_id: CHANGE-AA-021, disposition: planned, role: primary, priority: P2, priority_rule_id: P2-DATA-002, implementation_wave: 4, classification: resiliency}
  - {finding_id: F-003, primary_control_id: APP-AA-011, change_id: CHANGE-AA-008, disposition: planned, role: primary, priority: P0, priority_rule_id: P0-AA-012, implementation_wave: 2, classification: resiliency}
  - {finding_id: F-004, primary_control_id: APP-KAFKA-001, change_id: CHANGE-AA-007, disposition: planned, role: primary, priority: P0, priority_rule_id: P0-AA-006, implementation_wave: 2, classification: resiliency}
  - {finding_id: F-005, primary_control_id: APP-KAFKA-002, change_id: CHANGE-AA-019, disposition: planned, role: primary, priority: P1, priority_rule_id: P1-RCV-007, implementation_wave: 3, classification: resiliency}
  - {finding_id: F-006, primary_control_id: APP-KAFKA-003, change_id: CHANGE-AA-019, disposition: consolidated_under_root_cause, role: related, consolidation_reason: "Both findings are remediated by one listener container factory that owns ack mode, error handling, dead-letter routing, and guarded payload extraction.", priority: P1, priority_rule_id: P1-RCV-007, implementation_wave: 3, classification: resiliency}
  - {finding_id: F-007, primary_control_id: APP-KAFKA-006, change_id: CHANGE-AA-022, disposition: planned, role: primary, priority: P2, priority_rule_id: P2-DATA-007, implementation_wave: 4, classification: resiliency}
  - {finding_id: F-008, primary_control_id: APP-AA-007, change_id: CHANGE-AA-001, disposition: planned, role: primary, priority: P0, priority_rule_id: P0-AA-004, implementation_wave: 1, classification: resiliency}
  - {finding_id: F-009, primary_control_id: SQL-002, change_id: CHANGE-AA-009, disposition: planned, role: primary, priority: P1, priority_rule_id: P1-RCV-006, implementation_wave: 3, classification: resiliency}
  - {finding_id: F-010, primary_control_id: REDIS-005, change_id: CHANGE-AA-009, disposition: consolidated_under_root_cause, role: related, consolidation_reason: "Single root cause: no repository-owned deadline exists for any remote dependency. One externalized timeout contract covers SQL, Redis, and Kafka.", priority: P1, priority_rule_id: P1-RCV-006, implementation_wave: 3, classification: resiliency}
  - {finding_id: F-011, primary_control_id: KAFKA-005, change_id: CHANGE-AA-009, disposition: consolidated_under_root_cause, role: related, consolidation_reason: "Same root cause and same configuration surface as F-009 and F-010.", priority: P1, priority_rule_id: P1-RCV-006, implementation_wave: 3, classification: resiliency}
  - {finding_id: F-012, primary_control_id: SQL-003, change_id: CHANGE-AA-010, disposition: planned, role: primary, priority: P1, priority_rule_id: P1-RCV-001, implementation_wave: 3, classification: resiliency}
  - {finding_id: F-013, primary_control_id: SQL-007, change_id: CHANGE-AA-011, disposition: planned, role: primary, priority: P1, priority_rule_id: P1-RCV-001, implementation_wave: 3, classification: resiliency}
  - {finding_id: F-014, primary_control_id: APP-WEB-002, change_id: CHANGE-AA-012, disposition: planned, role: primary, priority: P1, priority_rule_id: P1-RCV-005, implementation_wave: 3, classification: resiliency}
  - {finding_id: F-015, primary_control_id: APP-AA-006, change_id: CHANGE-AA-013, disposition: planned, role: primary, priority: P1, priority_rule_id: P1-RCV-008, implementation_wave: 3, classification: resiliency}
  - {finding_id: F-016, primary_control_id: REDIS-020, change_id: CHANGE-AA-014, disposition: planned, role: primary, priority: P1, priority_rule_id: P1-RCV-011, implementation_wave: 3, classification: resiliency}
  - {finding_id: F-017, primary_control_id: REDIS-011, change_id: CHANGE-AA-015, disposition: consolidated_under_root_cause, role: related, consolidation_reason: "TTL, key prefix, and value serialization are all absent for the same reason: no RedisCacheConfiguration bean exists. One bean remediates all three.", priority: P1, priority_rule_id: P1-RCV-011, implementation_wave: 3, classification: resiliency}
  - {finding_id: F-018, primary_control_id: REDIS-022, change_id: CHANGE-AA-015, disposition: consolidated_under_root_cause, role: related, consolidation_reason: "Same absent RedisCacheConfiguration bean.", priority: P1, priority_rule_id: P1-RCV-011, implementation_wave: 3, classification: non_resiliency}
  - {finding_id: F-019, primary_control_id: REDIS-009, change_id: CHANGE-AA-016, disposition: planned, role: primary, priority: P1, priority_rule_id: P1-RCV-008, implementation_wave: 3, classification: resiliency}
  - {finding_id: F-020, primary_control_id: REDIS-015, change_id: CHANGE-AA-023, disposition: planned, role: primary, priority: P2, priority_rule_id: P2-DATA-010, implementation_wave: 4, classification: non_resiliency}
  - {finding_id: F-021, primary_control_id: APP-AA-017, change_id: CHANGE-AA-004, disposition: planned, role: primary, priority: P0, priority_rule_id: P0-AA-014, implementation_wave: 1, classification: resiliency}
  - {finding_id: F-022, primary_control_id: KV-009, change_id: CHANGE-AA-003, disposition: planned, role: primary, priority: P0, priority_rule_id: P0-AA-009, implementation_wave: 1, classification: resiliency}
  - {finding_id: F-023, primary_control_id: KV-005, change_id: CHANGE-AA-020, disposition: planned, role: primary, priority: P1, priority_rule_id: P1-RCV-009, implementation_wave: 3, classification: resiliency}
  - {finding_id: F-024, primary_control_id: APP-AA-013, change_id: CHANGE-AA-002, disposition: planned, role: primary, priority: P0, priority_rule_id: P0-AA-001, implementation_wave: 1, classification: resiliency}
  - {finding_id: F-025, primary_control_id: JVM-004, change_id: CHANGE-AA-017, disposition: planned, role: primary, priority: P1, priority_rule_id: P1-RCV-008, implementation_wave: 3, classification: resiliency}
  - {finding_id: F-026, primary_control_id: APP-AA-015, change_id: CHANGE-AA-005, disposition: planned, role: primary, priority: P0, priority_rule_id: P0-AA-013, implementation_wave: 1, classification: resiliency}
  - {finding_id: F-027, primary_control_id: APP-AA-016, change_id: CHANGE-AA-006, disposition: planned, role: primary, priority: P0, priority_rule_id: P0-AA-013, implementation_wave: 1, classification: resiliency}
  - {finding_id: F-028, primary_control_id: APP-AA-018, change_id: CHANGE-AA-024, disposition: planned, role: primary, priority: P0, priority_rule_id: P0-AA-013, implementation_wave: 4, classification: resiliency}
  - {finding_id: F-029, primary_control_id: REDIS-012, change_id: CHANGE-AA-015, disposition: planned, role: primary, priority: P1, priority_rule_id: P1-RCV-011, implementation_wave: 3, classification: non_resiliency}
```

```yaml
mapping_reconciliation:
  approved_findings_total: 29
  findings_mapped: 29
  findings_unmapped: 0
  findings_with_primary_change: 24
  findings_consolidated_under_another_change: 5
  consolidated_finding_ids: [F-006, F-010, F-011, F-017, F-018]
  changes_without_approved_finding: 0
  new_findings_created_in_step_3a: 0
  control_status_changes: 0
  severity_changes: 0
  classification_changes: 0
  not_assessed_controls_planned: 0
  not_applicable_controls_planned: 0
  compliant_controls_planned: 0
  accepted_risk_controls_planned: 0
  evidence_gaps_converted_to_changes: 0
  control_coverage_gaps_converted_to_changes: 0
```

```yaml
excluded_from_remediation:
  note: >-
    These items were carried forward from Step 2 and are deliberately not converted into remediation
    work. They remain routed to their recorded owners.
  evidence_gaps:
    - {id: EG-001, route_to: platform_evidence_request}
    - {id: EG-002, route_to: platform_evidence_request}
    - {id: EG-003, route_to: platform_evidence_request}
    - {id: EG-004, route_to: platform_evidence_request}
    - {id: EG-005, route_to: assessment_scope_decision}
    - {id: EG-006, route_to: platform_evidence_request}
    - {id: EG-007, route_to: platform_evidence_request}
    - {id: EG-008, route_to: architecture_governance_review}
    - {id: EG-009, route_to: assessment_scope_decision}
    - {id: EG-010, route_to: architecture_governance_review}
    - {id: EG-011, route_to: architecture_governance_review}
  control_coverage_gaps:
    - {id: CCG-001, route_to: grounding_standard_governance}
    - {id: CCG-002, route_to: grounding_standard_governance}
    - {id: CCG-003, route_to: grounding_standard_governance}
    - {id: CCG-004, route_to: grounding_standard_governance}
  not_assessed_controls: 17
  infrastructure_remediation: none_planned
  pcf_remediation: none_planned
```

## 4. Detailed Change Specifications

Each change carries its governed priority record, its target locations with Step 2 evidence preserved verbatim, its change-boundary classification, and references to the illustrative code blocks in Section 5. Original source excerpts, target locations, and proposed implementations are kept separate throughout.

### CHANGE-AA-001: Make regional traffic eligibility reflect authoritative dependency health

```yaml
change_id: CHANGE-AA-001
title: Make regional traffic eligibility reflect authoritative dependency health
finding_ids: [F-008]
primary_finding_id: F-008
primary_control_id: APP-AA-007
related_control_ids: [APP-AA-009, SQL-006, SQL-015, REDIS-019, KV-014, KAFKA-007, GLB-002, GLB-004]
category: traffic_eligibility
resiliency_related: true
finding_classification: resiliency
priority:
  value: P0
  policy_id: AA-REMEDIATION-PRIORITY
  policy_version: "1.0.0"
  rule_id: P0-AA-004
  rationale: >-
    Probes are enabled but the readiness group resolves to the framework default containing only the
    application availability state, so the auto-configured Azure SQL contributor never participates in
    readiness. Rule P0-AA-004 applies directly because an existing health probe does not include a
    critical application dependency. Rule P0-AA-008 applies concurrently because a sustained Azure SQL
    outage leaves every pod reporting readiness UP and therefore eligible for gateway traffic.
  calculated_priority: P0
  override_applied: false
  override_priority: null
  override_reason: null
  override_approved_by: null
  override_approved_at: null
  additional_applicable_rules: [P0-AA-008]
  p0_elevation_evaluated: not_applicable
implementation_wave: 1
complexity: medium
implementation_status: proposed
implementation_allowed_in_planning_phase: false
objective: >-
  Make readiness a true statement about whether this regional deployment can serve its critical
  inventory capability, so the global load balancer can withdraw a failed region, and make readiness
  transitions observable.
existing_behavior:
  description: >-
    management.endpoint.health.probes.enabled is true with no readiness or liveness group include or
    exclude list. The Azure SQL, Redis, Kafka, and Key Vault contributors report into the aggregate
    health endpoint only. No custom HealthIndicator exists and no production code publishes an
    AvailabilityChangeEvent or manipulates ReadinessState.
  evidence: [EV-F-008-01, EV-F-008-02]
proposed_behavior: >-
  Readiness includes the authoritative Azure SQL contributor and the application availability state.
  Redis is excluded from readiness because it is a non-authoritative cache with a safe degraded mode
  once CHANGE-AA-014 lands. Liveness remains the framework default so external dependency loss cannot
  cause restart loops. Readiness recovers automatically after dependency restoration without a process
  restart, and every readiness transition emits a region-tagged metric and structured log record.
what_this_solves: >-
  A failed regional dependency now removes the region from traffic eligibility instead of leaving it
  silently absorbing requests it cannot serve.
operating_scenario_impact: >-
  Supplies the application-side trigger the approved active-standby regional failover model requires.
  Kafka health participation is intentionally deferred to CHANGE-AA-007, which introduces the role
  contract needed to distinguish an intentionally inactive standby consumer from a failed one.
kafka_scenario_context:
  operating_scenario: active_standby
  scenario_preserved: true
  note: >-
    Kafka is deliberately excluded from the readiness group in this change. Including it before the
    region-role activation contract exists would make an intentionally inactive standby consumer look
    like a failure.
affected_files:
  - source/inventory-service/src/main/resources/application.yml
new_files:
  - source/inventory-service/src/main/java/com/ecommerce/inventory/health/ReadinessTransitionListener.java
configuration_changes:
  - management.endpoint.health.group.readiness.include
  - management.endpoint.health.group.readiness.show-details
  - management.endpoint.health.group.liveness.include
  - management.endpoint.health.status.http-mapping.out-of-service
dependency_changes: []
illustrative_code_blocks: [ICB-001-01, ICB-001-02]
proposed_tests: [PT-001-01, PT-001-02]
acceptance_criteria:
  - /actuator/health/readiness returns OUT_OF_SERVICE within the configured health budget when the Azure SQL contributor is DOWN.
  - /actuator/health/liveness remains UP while the Azure SQL contributor is DOWN, and the process is not restarted.
  - /actuator/health/readiness returns UP again after Azure SQL connectivity is restored, without a process or pod restart.
  - Redis unavailability alone does not make readiness fail once CHANGE-AA-014 provides the degraded read path.
  - Every readiness state transition emits exactly one structured log record and increments a region-tagged counter.
  - Health details remain hidden from unauthenticated callers on the aggregate health endpoint.
validation_commands:
  - "mvn -f source/inventory-service/pom.xml -Dtest=ReadinessProbeIntegrationTest test"
  - "mvn -f source/inventory-service/pom.xml verify"
risks:
  - id: RISK-001-01
    description: Including the database contributor in readiness can cause a transient database blip to withdraw an entire region from traffic.
    mitigation: Depends on CHANGE-AA-009 bounded timeouts and CHANGE-AA-010 bounded retry so a transient blip is absorbed before it reaches the health contributor.
  - id: RISK-001-02
    description: An unbounded health contributor can add load to a failing dependency during an incident.
    mitigation: CHANGE-AA-009 bounds the underlying client calls that the contributors use, and readiness caching limits probe frequency.
compatibility_considerations:
  - Readiness semantics change for platform probe consumers. The probe paths themselves are unchanged, so no gateway or Kubernetes probe path change is required.
  - Kubernetes probe timing and terminationGracePeriod are in the disabled deployment_configuration domain and are not modified.
rollback_considerations:
  - Removing the readiness group include list restores the framework default readiness behaviour with no schema, data, or contract impact.
depends_on_change_ids: [CHANGE-AA-005]
blocks_change_ids: [CHANGE-AA-004, CHANGE-AA-007]
open_questions: [OQ-001]
targeted_implementation_discovery_required: false
change_boundary:
  classification: resiliency_mechanism
  existing_business_behavior_preserved: true
  security_and_privacy_behavior_preserved: true
  external_interaction_pattern_changed: false
  approval_required: false
  approval:
    status: not_required
    decision_id: not_applicable
    approved_by: not_applicable
    approved_at: not_applicable
  implementation_allowed: true
  unresolved_inputs: []
```

### CHANGE-AA-002: Replace runtime DDL with a versioned, gated schema migration contract

```yaml
change_id: CHANGE-AA-002
title: Replace runtime DDL with a versioned, gated schema migration contract
finding_ids: [F-024]
primary_finding_id: F-024
primary_control_id: APP-AA-013
related_control_ids: []
category: startup_safety
resiliency_related: true
finding_classification: resiliency
priority:
  value: P0
  policy_id: AA-REMEDIATION-PRIORITY
  policy_version: "1.0.0"
  rule_id: P0-AA-001
  rationale: >-
    spring.jpa.hibernate.ddl-auto is update in the default profile and is not overridden in prod, so
    every startup in every region attempts a write-capable schema operation against whichever database
    the injected connection string resolves to. A pod starting against a read-only geo-secondary or a
    database mid-promotion fails to start. Rule P0-AA-001 applies because application configuration
    prevents successful startup in a region. Rule P0-AA-005 applies concurrently because CHANGE-AA-008
    is P0 and requires a versioned migration mechanism for its deduplication table.
  calculated_priority: P0
  override_applied: false
  override_priority: null
  override_reason: null
  override_approved_by: null
  override_approved_at: null
  additional_applicable_rules: [P0-AA-005]
  p0_elevation_evaluated: not_applicable
implementation_wave: 1
complexity: medium
implementation_status: proposed
implementation_allowed_in_planning_phase: false
objective: >-
  Remove the write-capable schema operation from the startup path and replace it with a versioned,
  reviewable migration contract that a standby-region pod can satisfy without mutating the database.
existing_behavior:
  description: >-
    spring.jpa.hibernate.ddl-auto is set to update in application.yml and is not overridden in
    application-prod.yml. No Flyway or Liquibase dependency is declared, so there is no versioned
    migration contract and no controlled migration gate.
  evidence: [EV-F-024-01]
proposed_behavior: >-
  Hibernate performs schema validation only. The schema itself is expressed as versioned SQL migration
  scripts held in the repository under src/main/resources/db/migration, applied by an approved
  migration runner outside the ordinary application startup path or gated by an explicit, bounded,
  role-aware startup step.
what_this_solves: >-
  A standby-region pod can start against a read-only or mid-promotion endpoint, and schema state stops
  drifting silently between regions.
operating_scenario_impact: >-
  Directly enables the approved active-standby promotion path. The standby region can be deployed and
  started at any time without attempting DDL against a database it does not own.
kafka_scenario_context: null
affected_files:
  - source/inventory-service/src/main/resources/application.yml
  - source/inventory-service/src/main/resources/application-prod.yml
new_files:
  - source/inventory-service/src/main/resources/db/migration/V1__baseline_inventory_items.sql
configuration_changes:
  - spring.jpa.hibernate.ddl-auto
  - spring.jpa.open-in-view
dependency_changes:
  - target: versioned_migration_runner
    status: targeted_discovery_required
    reason: grounding/governance/approved-libraries.yml declares no approved schema-migration library.
illustrative_code_blocks: [ICB-002-01, ICB-002-02, ICB-002-03]
proposed_tests: [PT-002-01]
acceptance_criteria:
  - No profile sets spring.jpa.hibernate.ddl-auto to update, create, or create-drop.
  - Application startup performs no DDL statement against the configured database.
  - Startup fails fast with a clear message when the deployed schema does not match the entity model.
  - The baseline schema, including the productId unique constraint and the version column, exists as a versioned repository-owned migration script.
  - An integration test starting against a schema created only by the migration script passes.
validation_commands:
  - "mvn -f source/inventory-service/pom.xml -Dtest=SchemaValidationIntegrationTest test"
  - "mvn -f source/inventory-service/pom.xml verify"
risks:
  - id: RISK-002-01
    description: Switching to validate will fail startup in any environment whose schema was created implicitly by ddl-auto update and has since drifted.
    mitigation: The baseline migration script is generated from the current entity model, and a pre-cutover schema comparison is required in each environment before the change is deployed.
  - id: RISK-002-02
    description: Without an approved migration runner the schema application step remains a manual or externally owned process.
    mitigation: The repository-owned migration scripts and the ddl-auto change are delivered regardless; only the runner selection is held as a targeted-discovery item.
compatibility_considerations:
  - No entity, table, column, or constraint definition changes. The migration script reproduces the existing model exactly.
  - Database permissions required at runtime reduce from DDL to DML, which is a tightening rather than a loosening.
rollback_considerations:
  - Restoring ddl-auto update returns the previous behaviour. The migration scripts are additive and inert when the runner is not enabled.
depends_on_change_ids: []
blocks_change_ids: [CHANGE-AA-008, CHANGE-AA-021]
open_questions: [OQ-002]
targeted_implementation_discovery_required: true
targeted_discovery_scope: dependency_target_only
change_boundary:
  classification: supporting_configuration
  existing_business_behavior_preserved: true
  security_and_privacy_behavior_preserved: true
  external_interaction_pattern_changed: false
  approval_required: false
  approval:
    status: not_required
    decision_id: not_applicable
    approved_by: not_applicable
    approved_at: not_applicable
  implementation_allowed: true
  unresolved_inputs:
    - Approved versioned schema-migration library and its execution model for this platform
```

### CHANGE-AA-003: Bound the Key Vault startup dependency

```yaml
change_id: CHANGE-AA-003
title: Bound the Key Vault startup dependency
finding_ids: [F-022]
primary_finding_id: F-022
primary_control_id: KV-009
related_control_ids: [KV-003, GLB-009]
category: startup_safety
resiliency_related: true
finding_classification: resiliency
priority:
  value: P0
  policy_id: AA-REMEDIATION-PRIORITY
  policy_version: "1.0.0"
  rule_id: P0-AA-009
  rationale: >-
    The prod profile imports azure-keyvault as a mandatory property source with no bounded retry or
    timeout. During a regional recovery many pods start at once and are the most likely to be throttled,
    so an external dependency failure produces repeated startup failures and a restart loop that cannot
    restore service until the dependency recovers. Rule P0-AA-009 applies. Rule P1-RCV-010 also applies
    but is superseded because the highest applicable rule wins.
  calculated_priority: P0
  override_applied: false
  override_priority: null
  override_reason: null
  override_approved_by: null
  override_approved_at: null
  additional_applicable_rules: [P1-RCV-010]
  p0_elevation_evaluated: not_applicable
implementation_wave: 1
complexity: medium
implementation_status: proposed
implementation_allowed_in_planning_phase: false
objective: >-
  Make startup dependence on Key Vault explicit, bounded, and observable so a recovering region can
  bring capacity online predictably instead of stalling on an implicit SDK default.
existing_behavior:
  description: >-
    application-prod.yml declares spring.config.import as azure-keyvault:${AZURE_KEYVAULT_ENDPOINT}
    without the optional: prefix. No ClientOptions, RetryOptions, startup timeout, or last-known-good
    policy is configured for the Key Vault client.
  evidence: [EV-F-022-01]
proposed_behavior: >-
  The Key Vault property source is imported with an explicit, externally configured retry and timeout
  budget through spring.cloud.azure.keyvault.secret client properties. The import remains mandatory
  because the datasource and Redis credentials genuinely cannot be resolved without it, but the failure
  is now bounded, and the startup contract is stated explicitly in repository-owned configuration.
what_this_solves: >-
  A Key Vault throttle or transient identity failure produces a bounded, diagnosable startup failure
  rather than an unbounded stall, so a startup probe can tell a progressing startup from a stuck one.
operating_scenario_impact: >-
  Removes the unbounded startup dependency that would otherwise prevent the standby region from
  regaining capacity during a regional recovery.
kafka_scenario_context: null
affected_files:
  - source/inventory-service/src/main/resources/application-prod.yml
new_files: []
configuration_changes:
  - spring.cloud.azure.keyvault.secret.client.connect-timeout
  - spring.cloud.azure.keyvault.secret.client.response-timeout
  - spring.cloud.azure.keyvault.secret.retry.exponential.max-retries
  - spring.cloud.azure.keyvault.secret.retry.exponential.base-delay
  - spring.cloud.azure.keyvault.secret.retry.exponential.max-delay
dependency_changes: []
illustrative_code_blocks: [ICB-003-01]
proposed_tests: [PT-003-01]
acceptance_criteria:
  - Key Vault client connect, response, and retry budgets are declared in repository-owned configuration and are overridable per environment.
  - No hardcoded vault endpoint, region, or credential appears in any profile.
  - Startup failure caused by an unreachable Key Vault occurs within the declared budget and emits a diagnosable message naming the property source.
  - The mandatory-versus-optional startup contract is stated explicitly in the prod profile.
validation_commands:
  - "mvn -f source/inventory-service/pom.xml -Dtest=KeyVaultStartupContractTest test"
  - "mvn -f source/inventory-service/pom.xml verify"
risks:
  - id: RISK-003-01
    description: A retry budget set too low can turn a recoverable throttle into a startup failure.
    mitigation: All budget values are externalized placeholders with no approved default asserted by this plan; the deployment supplies values aligned to the regional recovery budget.
compatibility_considerations:
  - The import remains mandatory, so no behavioural change occurs when Key Vault is healthy.
  - Kubernetes startup probe configuration is in the disabled deployment_configuration domain and is not modified.
rollback_considerations:
  - Removing the client property block restores SDK defaults with no contract or data impact.
depends_on_change_ids: []
blocks_change_ids: [CHANGE-AA-020]
open_questions: [OQ-003]
targeted_implementation_discovery_required: false
change_boundary:
  classification: supporting_configuration
  existing_business_behavior_preserved: true
  security_and_privacy_behavior_preserved: true
  external_interaction_pattern_changed: false
  approval_required: false
  approval:
    status: not_required
    decision_id: not_applicable
    approved_by: not_applicable
    approved_at: not_applicable
  implementation_allowed: true
  unresolved_inputs: []
```

### CHANGE-AA-004: Add graceful shutdown, readiness withdrawal, and work draining

```yaml
change_id: CHANGE-AA-004
title: Add graceful shutdown, readiness withdrawal, and work draining
finding_ids: [F-021]
primary_finding_id: F-021
primary_control_id: APP-AA-017
related_control_ids: [GLB-007, JVM-016, JVM-017]
category: graceful_termination
resiliency_related: true
finding_classification: resiliency
priority:
  value: P0
  policy_id: AA-REMEDIATION-PRIORITY
  policy_version: "1.0.0"
  rule_id: P0-AA-014
  rationale: >-
    Rule P0-AA-014 applies on its stated conditions. The finding is against control APP-AA-017, graceful
    shutdown is missing, and the workload qualifies as authoritative processing under the rule's own
    enumeration because the service runs a Kafka consumer that performs durable state mutation inside
    transactions. Pod termination therefore interrupts in-flight work between the database write and the
    offset commit, producing duplicate or lost processing. Rule P1-RCV-012 also matches but is
    superseded because the highest applicable rule wins.
  calculated_priority: P0
  override_applied: false
  override_priority: null
  override_reason: null
  override_approved_by: null
  override_approved_at: null
  additional_applicable_rules: [P1-RCV-012]
  policy_note: >-
    The policy heading names this rule P0-AA-014 while the embedded rule body declares
    rule_id P0-RCV-014. The heading identifier is cited here and the discrepancy is recorded as OQ-004.
  p0_elevation_evaluated: not_applicable
implementation_wave: 1
complexity: medium
implementation_status: proposed
implementation_allowed_in_planning_phase: false
objective: >-
  Make pod termination an ordered transition that first stops being eligible for traffic, then stops
  acquiring new work, then completes or cleanly abandons in-flight work within a bounded window.
existing_behavior:
  description: >-
    Neither profile configures server.shutdown graceful or spring.lifecycle.timeout-per-shutdown-phase.
    No production class implements SmartLifecycle, DisposableBean, or @PreDestroy, and no code withdraws
    readiness before termination. The Kafka listener container and the servlet container stop on the
    framework default immediate shutdown.
  evidence: [EV-F-021-01]
proposed_behavior: >-
  server.shutdown is graceful and spring.lifecycle.timeout-per-shutdown-phase is externally configured.
  A lifecycle component runs at the earliest shutdown phase, publishes a REFUSING_TRAFFIC readiness
  state so the load balancer withdraws the pod, stops the Kafka listener containers so no new records
  are polled, and then allows the ordinary graceful web shutdown to drain in-flight HTTP requests.
what_this_solves: >-
  Rolling deployments, scale-in, node drains, and planned regional transitions stop cutting in-flight
  HTTP writes and stop interrupting Kafka records between the database write and the offset commit.
operating_scenario_impact: >-
  Provides the controlled intake-stop that an active-standby role transfer requires, and it is the same
  mechanism CHANGE-AA-007 reuses when a region is deactivated without terminating the process.
kafka_scenario_context:
  operating_scenario: active_standby
  scenario_preserved: true
  note: Listener stop ordering is a prerequisite for safe role transfer under KAFKA-AS-007.
affected_files:
  - source/inventory-service/src/main/resources/application.yml
new_files:
  - source/inventory-service/src/main/java/com/ecommerce/inventory/lifecycle/GracefulShutdownCoordinator.java
configuration_changes:
  - server.shutdown
  - spring.lifecycle.timeout-per-shutdown-phase
  - app.lifecycle.readiness-withdrawal-delay
dependency_changes: []
illustrative_code_blocks: [ICB-004-01, ICB-004-02]
proposed_tests: [PT-004-01]
acceptance_criteria:
  - server.shutdown is graceful and the per-phase shutdown timeout is declared and externally overridable.
  - On SIGTERM the readiness probe reports OUT_OF_SERVICE before the servlet container stops accepting requests.
  - On SIGTERM all Kafka listener containers stop polling before in-flight record processing is abandoned.
  - An HTTP request in flight at SIGTERM completes when it finishes within the configured drain window.
  - Shutdown emits a structured log record naming each phase and its duration.
validation_commands:
  - "mvn -f source/inventory-service/pom.xml -Dtest=GracefulShutdownIntegrationTest test"
  - "mvn -f source/inventory-service/pom.xml verify"
risks:
  - id: RISK-004-01
    description: A drain window longer than the platform termination grace period is truncated by SIGKILL, which reintroduces the original failure.
    mitigation: Recorded as OQ-005. The application-side window must be shorter than the platform grace period, which lives in the disabled deployment_configuration domain and must be confirmed externally.
compatibility_considerations:
  - Deployment and drain duration increase by the configured window. No API or event contract changes.
  - Kubernetes terminationGracePeriodSeconds and preStop hooks are out of the remediation boundary.
rollback_considerations:
  - Removing the lifecycle component and the two properties restores immediate shutdown with no data or contract impact.
depends_on_change_ids: [CHANGE-AA-001]
blocks_change_ids: [CHANGE-AA-007]
open_questions: [OQ-005]
targeted_implementation_discovery_required: false
change_boundary:
  classification: resiliency_mechanism
  existing_business_behavior_preserved: true
  security_and_privacy_behavior_preserved: true
  external_interaction_pattern_changed: false
  approval_required: false
  approval:
    status: not_required
    decision_id: not_applicable
    approved_by: not_applicable
    approved_at: not_applicable
  implementation_allowed: true
  unresolved_inputs:
    - Platform termination grace period, required to bound the application drain window
```

### CHANGE-AA-005: Attach regional identity to every metric and log record

```yaml
change_id: CHANGE-AA-005
title: Attach regional identity to every metric and log record
finding_ids: [F-026]
primary_finding_id: F-026
primary_control_id: APP-AA-015
related_control_ids: [GLB-018]
category: failure_observability
resiliency_related: true
finding_classification: resiliency
priority:
  value: P0
  policy_id: AA-REMEDIATION-PRIORITY
  policy_version: "1.0.0"
  rule_id: P0-AA-013
  rationale: >-
    Metrics and logs from both regions are indistinguishable once aggregated, so an operator cannot
    determine which region produced an error, which region is serving traffic, or whether single-active
    Kafka processing is actually single. Rule P0-AA-013 applies because the defect prevents the team
    from executing or interpreting active-active regional failure tests, including the split-brain
    detection that CHANGE-AA-007 must be validated against. Rule P0-AA-002 applies concurrently because
    a region-identifying configuration value must be added and externalized. Severity for F-026 is
    medium; priority is governed by the rule, not by severity.
  calculated_priority: P0
  override_applied: false
  override_priority: null
  override_reason: null
  override_approved_by: null
  override_approved_at: null
  additional_applicable_rules: [P0-AA-002, P0-AA-005]
  p0_elevation_evaluated: not_applicable
implementation_wave: 1
complexity: low
implementation_status: proposed
implementation_allowed_in_planning_phase: false
objective: >-
  Give every emitted metric and log record a deployment-supplied region and role dimension so regional
  behaviour can be separated in aggregate views.
existing_behavior:
  description: >-
    No management.metrics.tags entry, MeterFilter, or common-tag configuration exists. logback-spring.xml
    is a single console appender using LogstashEncoder with no MDC provider, custom field, or region
    field, and no production code populates MDC.
  evidence: [EV-F-026-01, EV-F-026-02]
proposed_behavior: >-
  A region identifier and a deployment role identifier are bound from environment-supplied properties,
  applied as Micrometer common tags, and emitted as static structured-logging fields. No region name or
  regional endpoint is hardcoded anywhere in the repository.
what_this_solves: >-
  Regional failure attribution and split-brain detection become possible from emitted telemetry.
operating_scenario_impact: >-
  Supplies the evidence needed to confirm or refute the single-active Kafka processing model that the
  approved active-standby scenario depends on.
kafka_scenario_context:
  operating_scenario: active_standby
  scenario_preserved: true
  note: The role tag reports the configured regional role; it does not assign or change it.
affected_files:
  - source/inventory-service/src/main/resources/application.yml
  - source/inventory-service/src/main/resources/logback-spring.xml
new_files:
  - source/inventory-service/src/main/java/com/ecommerce/inventory/config/DeploymentIdentityProperties.java
configuration_changes:
  - management.metrics.tags.region
  - management.metrics.tags.role
  - app.deployment.region
  - app.deployment.role
dependency_changes: []
illustrative_code_blocks: [ICB-005-01, ICB-005-02, ICB-005-03]
proposed_tests: [PT-005-01]
acceptance_criteria:
  - Every meter scraped from /actuator/prometheus carries a region tag and a role tag.
  - Every JSON log record carries a region field and a role field.
  - The region and role values are supplied entirely by environment placeholders with no hardcoded region name or regional endpoint anywhere in the repository.
  - A missing region value produces an explicit startup-visible default of unknown rather than an absent tag.
validation_commands:
  - "mvn -f source/inventory-service/pom.xml -Dtest=DeploymentIdentityTelemetryTest test"
  - "mvn -f source/inventory-service/pom.xml verify"
risks:
  - id: RISK-005-01
    description: Adding common tags increases metric cardinality in the aggregation backend.
    mitigation: Two low-cardinality tags are added, both bounded by the number of deployed regions and roles.
compatibility_considerations:
  - Existing dashboards and alert rules that aggregate without a region dimension continue to work; the aggregation backend is outside the remediation boundary.
rollback_considerations:
  - Removing the tag configuration and the logback fields restores the previous telemetry shape.
depends_on_change_ids: []
blocks_change_ids: [CHANGE-AA-001, CHANGE-AA-006, CHANGE-AA-007, CHANGE-AA-022]
open_questions: [OQ-006]
targeted_implementation_discovery_required: false
change_boundary:
  classification: supporting_configuration
  existing_business_behavior_preserved: true
  security_and_privacy_behavior_preserved: true
  external_interaction_pattern_changed: false
  approval_required: false
  approval:
    status: not_required
    decision_id: not_applicable
    approved_by: not_applicable
    approved_at: not_applicable
  implementation_allowed: true
  unresolved_inputs: []
```

### CHANGE-AA-006: Emit failure and business-outcome telemetry

```yaml
change_id: CHANGE-AA-006
title: Emit failure and business-outcome telemetry
finding_ids: [F-027]
primary_finding_id: F-027
primary_control_id: APP-AA-016
related_control_ids: [APP-OBS-002, REDIS-025, REDIS-026, KAFKA-007, GLB-018]
category: failure_observability
resiliency_related: true
finding_classification: resiliency
priority:
  value: P0
  policy_id: AA-REMEDIATION-PRIORITY
  policy_version: "1.0.0"
  rule_id: P0-AA-013
  rationale: >-
    No production class declares a logger and no custom metric exists for publication failure,
    consumption outcome, cache failure versus cache miss, last successful processing time, or backlog
    age, so every failure mode in this assessment is silent and a stopped consumer is indistinguishable
    from an idle one. Rule P0-AA-013 applies because the defect prevents the team from executing or
    interpreting regional failure tests. Rule P0-AA-005 applies concurrently because CHANGE-AA-007 and
    CHANGE-AA-024 are P0 and cannot be validated without these signals.
  calculated_priority: P0
  override_applied: false
  override_priority: null
  override_reason: null
  override_approved_by: null
  override_approved_at: null
  additional_applicable_rules: [P0-AA-005]
  p0_elevation_evaluated: not_applicable
implementation_wave: 1
complexity: medium
implementation_status: proposed
implementation_allowed_in_planning_phase: false
objective: >-
  Make every failure and every business outcome produce an application-emitted signal, so failures are
  detectable, recovery is initiable, and a stopped consumer is distinguishable from an idle one.
existing_behavior:
  description: >-
    No production class declares a logger, uses @Slf4j, or emits a log statement. Logback has a single
    INFO console appender. No custom metric, counter, timer, or gauge is registered. The producer
    discards its send result and logs nothing on failure.
  evidence: [EV-F-027-01, EV-F-027-02]
proposed_behavior: >-
  A small telemetry component registers counters and timers for inventory publication outcome, order
  consumption outcome, cache outcome distinguishing failure from miss, and a last-success timestamp
  gauge per processing path. Failure paths emit structured log records at WARN or ERROR with the
  operation, the outcome, the correlation reference, and the exception class, with no payload,
  credential, or connection string in the record.
what_this_solves: >-
  Dropped publications, abandoned records, quarantined poison records, and cache outages become visible,
  and mean time to detect stops being unbounded.
operating_scenario_impact: >-
  Supplies the last-success and backlog-age signals that make an intentionally inactive standby
  consumer distinguishable from a failed consumer, which KAFKA-007 requires and which CHANGE-AA-007
  depends on.
kafka_scenario_context:
  operating_scenario: active_standby
  scenario_preserved: true
  note: Signals report processing activity; they do not assign or change regional role.
affected_files:
  - source/inventory-service/src/main/resources/logback-spring.xml
new_files:
  - source/inventory-service/src/main/java/com/ecommerce/inventory/observability/InventoryTelemetry.java
configuration_changes:
  - logging.level.com.ecommerce.inventory
dependency_changes: []
illustrative_code_blocks: [ICB-006-01, ICB-006-02]
proposed_tests: [PT-006-01]
acceptance_criteria:
  - A counter records inventory event publication outcome with a success or failure dimension and the region tag from CHANGE-AA-005.
  - A counter records order event consumption outcome with success, retryable failure, and quarantined dimensions.
  - A counter distinguishes cache miss from cache failure.
  - A gauge reports seconds since the last successful order-event application and is present even when zero records have been processed.
  - Every failure path emits exactly one structured log record containing the operation, outcome, correlation reference, and exception class.
  - No log record, metric tag, or metric name contains a payload value, credential, connection string, or secret.
validation_commands:
  - "mvn -f source/inventory-service/pom.xml -Dtest=InventoryTelemetryTest test"
  - "mvn -f source/inventory-service/pom.xml verify"
risks:
  - id: RISK-006-01
    description: Logging on high-volume failure paths can amplify an incident through log volume.
    mitigation: Failure logging is one record per operation outcome with no payload content, and levels are externally configurable.
  - id: RISK-006-02
    description: Adding a correlation reference to log records could expose business identifiers.
    mitigation: Only the existing referenceId and orderId values already present in the event contract are recorded; no customer, credential, or payment field exists in this service.
compatibility_considerations:
  - Log output shape gains fields but remains LogstashEncoder JSON, so existing parsers continue to work.
  - New meters are additive; no existing meter name or tag changes.
rollback_considerations:
  - Removing the telemetry component and reverting the logback configuration restores the previous silent behaviour.
depends_on_change_ids: [CHANGE-AA-005]
blocks_change_ids: [CHANGE-AA-007, CHANGE-AA-018, CHANGE-AA-019, CHANGE-AA-024]
open_questions: []
targeted_implementation_discovery_required: false
change_boundary:
  classification: resiliency_mechanism
  existing_business_behavior_preserved: true
  security_and_privacy_behavior_preserved: true
  external_interaction_pattern_changed: false
  approval_required: false
  approval:
    status: not_required
    decision_id: not_applicable
    approved_by: not_applicable
    approved_at: not_applicable
  implementation_allowed: true
  unresolved_inputs: []
```

### CHANGE-AA-007: Give the Kafka listener an externalized region-role activation contract

```yaml
change_id: CHANGE-AA-007
title: Give the Kafka listener an externalized region-role activation contract
finding_ids: [F-004]
primary_finding_id: F-004
primary_control_id: APP-KAFKA-001
related_control_ids: [KAFKA-AS-001, KAFKA-AS-002, KAFKA-AS-003, KAFKA-AS-007, KAFKA-AS-008, KAFKA-010, KAFKA-012, APP-WORKLOAD-001, APP-WORKLOAD-002]
category: workload_ownership
resiliency_related: true
finding_classification: resiliency
priority:
  value: P0
  policy_id: AA-REMEDIATION-PRIORITY
  policy_version: "1.0.0"
  rule_id: P0-AA-006
  rationale: >-
    The @KafkaListener declares only topics and groupId, so every started instance in every region
    consumes order-events immediately and the same immutable artifact cannot operate correctly in a
    standby region. Rule P0-AA-006 applies. Rule P0-AA-002 applies concurrently because a region-role
    activation value must be added and externalized before a role change can be applied by configuration
    alone. Rule P0-AA-012 applies concurrently because concurrent consumption from two regional roles
    produces duplicate execution against a single authoritative database.
  calculated_priority: P0
  override_applied: false
  override_priority: null
  override_reason: null
  override_approved_by: null
  override_approved_at: null
  additional_applicable_rules: [P0-AA-002, P0-AA-012]
  p0_elevation_evaluated: not_applicable
implementation_wave: 2
complexity: high
implementation_status: proposed
implementation_allowed_in_planning_phase: false
objective: >-
  Make Kafka consumption a deployment-controlled, observable, and reversible decision so that a regional
  role change is a configuration action rather than a code change, and so that consumption state is
  visible to an operator.
existing_behavior:
  description: >-
    The @KafkaListener declares only topics and groupId with no id, no autoStartup attribute, no
    containerFactory reference, and no property-driven enablement. No KafkaListenerEndpointRegistry
    manipulation, lease acquisition, ownership epoch, fencing token, or SQL primary-role verification
    exists in production source.
  evidence: [EV-F-004-01]
proposed_behavior: >-
  The listener carries a stable id and an autoStartup expression bound to an externalized property. An
  activation component exposes start and stop of the named listener container through the
  KafkaListenerEndpointRegistry, reports the current activation state as a region-tagged gauge, and
  logs every activation transition. The default value of the activation property preserves today's
  behaviour so no existing deployment silently stops consuming.
what_this_solves: >-
  A standby-region deployment can be configured not to consume, a promotion can start consumption
  without a redeploy, and the activation state is visible so a both-active condition can be detected.
operating_scenario_impact: >-
  Directly implements the single_active regional processing model that the approved active_standby Kafka
  operating scenario declares. It does not change the scenario, the cluster model, or the regional role
  assignment, all of which remain deployment and architecture decisions.
kafka_scenario_context:
  operating_scenario: active_standby
  scenario_source: approved_application_architecture_context
  scenario_policy_id: KAFKA-OPERATING-SCENARIO
  scenario_policy_version: "3.2.0"
  scenario_rule_id: KAFKA-SCENARIO-001
  scenario_validation_status: consistent
  architecture_confirmation_required: false
  processing_model: mixed
  regional_processing_model: single_active
  external_side_effects: none
  kafka_backed_state: none
  scenario_preserved: true
  scenario_redesigned: false
affected_files:
  - source/inventory-service/src/main/java/com/ecommerce/inventory/kafka/consumer/OrderEventConsumer.java
  - source/inventory-service/src/main/resources/application.yml
new_files:
  - source/inventory-service/src/main/java/com/ecommerce/inventory/kafka/RegionalConsumptionController.java
configuration_changes:
  - app.kafka.consumer.enabled
  - app.kafka.consumer.listener-id
  - management.endpoint.health.group.readiness.include
dependency_changes: []
illustrative_code_blocks: [ICB-007-01, ICB-007-02, ICB-007-03]
proposed_tests: [PT-007-01, PT-007-02]
acceptance_criteria:
  - The listener declares a stable id and an autoStartup expression bound to app.kafka.consumer.enabled.
  - Setting app.kafka.consumer.enabled to false prevents any record from being polled while the application starts, serves HTTP traffic, and reports readiness UP.
  - Setting the property to true starts consumption at startup with no code change.
  - Activation and deactivation each emit one structured log record and update a region-tagged gauge whose value distinguishes active from inactive.
  - An intentionally inactive consumer does not cause the readiness probe to fail.
  - Deactivation stops record acquisition before in-flight record processing completes or is abandoned, reusing the CHANGE-AA-004 drain contract.
validation_commands:
  - "mvn -f source/inventory-service/pom.xml -Dtest=RegionalConsumptionControlTest test"
  - "mvn -f source/inventory-service/pom.xml -Dtest=OrderEventConsumerActivationTest test"
  - "mvn -f source/inventory-service/pom.xml verify"
risks:
  - id: RISK-007-01
    description: An operator can enable consumption in both regions at once, because the mechanism is deployment-controlled rather than self-fencing.
    mitigation: The activation gauge from CHANGE-AA-005 and CHANGE-AA-006 makes a both-active condition detectable. A self-fencing ownership lease is deliberately not proposed here; it is recorded as OQ-007 because no approved ownership or fencing mechanism exists in the repository or in governance.
  - id: RISK-007-02
    description: Defaulting the property to true preserves current behaviour and therefore does not by itself stop standby consumption.
    mitigation: The repository-owned defect is the absence of the mechanism. The deployment obligation to set the value per region is stated in the acceptance criteria and carried to Step 5 as a closure condition.
compatibility_considerations:
  - Default value true preserves current behaviour for every existing deployment.
  - The consumer group id, topic name, and payload contract are unchanged.
rollback_considerations:
  - Removing the id and autoStartup attributes and the activation component restores unconditional auto-start.
depends_on_change_ids: [CHANGE-AA-004, CHANGE-AA-005, CHANGE-AA-006]
blocks_change_ids: []
open_questions: [OQ-007, OQ-008]
targeted_implementation_discovery_required: true
targeted_discovery_scope: ownership_fencing_target_only
change_boundary:
  classification: resiliency_mechanism
  existing_business_behavior_preserved: true
  security_and_privacy_behavior_preserved: true
  external_interaction_pattern_changed: false
  approval_required: false
  approval:
    status: not_required
    decision_id: not_applicable
    approved_by: not_applicable
    approved_at: not_applicable
  implementation_allowed: true
  unresolved_inputs:
    - Approved ownership, lease, or fencing mechanism for self-enforced single-active consumption
    - Confirmation of how standby-region consumption is currently prevented, carried from EG-010
```

### CHANGE-AA-008: Make order-event consumption and stock adjustment idempotent

```yaml
change_id: CHANGE-AA-008
title: Make order-event consumption and stock adjustment idempotent
finding_ids: [F-003]
primary_finding_id: F-003
primary_control_id: APP-AA-011
related_control_ids: [KAFKA-003, KAFKA-AS-004, KAFKA-AS-006, SQL-004, GLB-013, JVM-019]
category: data_integrity
resiliency_related: true
finding_classification: resiliency
priority:
  value: P0
  policy_id: AA-REMEDIATION-PRIORITY
  policy_version: "1.0.0"
  rule_id: P0-AA-012
  rationale: >-
    reserve and release apply relative quantity deltas with no persisted operation identity and no
    duplicate detection, and auto-offset-reset is earliest. Rebalance redelivery, container restart,
    offset reset, promotion replay, and gateway retry each repeat the same business effect against the
    single authoritative Azure SQL record. Rule P0-AA-012 applies because duplicate execution and replay
    behaviour make a critical business transaction unsafe when more than one region is active. Rules
    P1-RCV-004, P2-DATA-006, and P2-DATA-007 also match but are superseded because the highest
    applicable rule wins.
  calculated_priority: P0
  override_applied: false
  override_priority: null
  override_reason: null
  override_approved_by: null
  override_approved_at: null
  additional_applicable_rules: [P1-RCV-004, P2-DATA-006, P2-DATA-007]
  p0_elevation_evaluated: not_applicable
implementation_wave: 2
complexity: high
implementation_status: proposed
implementation_allowed_in_planning_phase: false
objective: >-
  Give every stock adjustment a stable, durable operation identity so that a repeated delivery of the
  same business operation produces exactly one stock movement.
existing_behavior:
  description: >-
    OrderEventConsumer maps ORDER_CREATED to service.reserve and ORDER_CANCELLED to service.release and
    passes the event orderId through as referenceId. referenceId is never persisted, never checked, and
    never used to derive a stable operation identity. No reservation record, processed-event table,
    unique constraint on (productId, referenceId), or conditional update guards a repeated application.
  evidence: [EV-F-003-01, EV-F-003-02]
proposed_behavior: >-
  A durable processed-operation record keyed by a stable operation identity derived from the operation
  type, the product identifier, and the reference identifier is written inside the same transaction as
  the stock adjustment. A unique constraint makes a second application of the same operation fail at the
  database, and the service translates that failure into a no-op that returns the current inventory
  state. The consumer derives the operation identity from the consumed order event rather than
  generating one.
what_this_solves: >-
  Promotion replay from a restored or reset offset, rebalance redelivery, and container restart stop
  silently corrupting authoritative stock quantities, which makes the documented failover procedure safe
  to execute.
operating_scenario_impact: >-
  This is the precondition for safe active-standby promotion. Without it, the approved failover
  procedure cannot be run.
kafka_scenario_context:
  operating_scenario: active_standby
  scenario_preserved: true
  note: >-
    The deduplication record lives in Azure SQL, which the approved architecture already declares as the
    authoritative business state. No new datastore is introduced and the database-independent constraint
    does not apply to this repository.
affected_files:
  - source/inventory-service/src/main/java/com/ecommerce/inventory/service/impl/InventoryServiceImpl.java
  - source/inventory-service/src/main/java/com/ecommerce/inventory/kafka/consumer/OrderEventConsumer.java
new_files:
  - source/inventory-service/src/main/java/com/ecommerce/inventory/model/ProcessedOperation.java
  - source/inventory-service/src/main/java/com/ecommerce/inventory/repository/ProcessedOperationRepository.java
  - source/inventory-service/src/main/resources/db/migration/V2__processed_operation.sql
configuration_changes: []
dependency_changes: []
illustrative_code_blocks: [ICB-008-01, ICB-008-02, ICB-008-03, ICB-008-04, ICB-008-05]
proposed_tests: [PT-008-01, PT-008-02]
acceptance_criteria:
  - A processed-operation record is written in the same transaction as the stock adjustment it represents.
  - A unique constraint on the operation identity exists in the versioned migration script.
  - Delivering the same ORDER_CREATED event twice produces exactly one reservation and leaves availableQuantity and reservedQuantity unchanged after the second delivery.
  - Replaying the entire retained order-events history against a populated database produces no additional stock movement.
  - A duplicate detection outcome increments the region-tagged consumption counter with a duplicate dimension rather than a failure dimension.
  - An operation with an absent or blank reference identifier is handled by the explicitly recorded policy rather than silently deduplicated to a shared key.
validation_commands:
  - "mvn -f source/inventory-service/pom.xml -Dtest=IdempotentStockAdjustmentTest test"
  - "mvn -f source/inventory-service/pom.xml -Dtest=OrderEventReplayIntegrationTest test"
  - "mvn -f source/inventory-service/pom.xml verify"
risks:
  - id: RISK-008-01
    description: The processed-operation table grows without bound.
    mitigation: A retention window is required. The window value is an unresolved input recorded as OQ-009 because no approved retention policy exists in the supplied context.
  - id: RISK-008-02
    description: REST callers currently send an optional referenceId and may send blank values, which cannot be deduplicated.
    mitigation: The REST-level idempotency-key contract is isolated as an approval-required target and is not implemented until approved. Consumer-side deduplication proceeds independently because order events always carry orderId.
compatibility_considerations:
  - The consumer path changes from at-least-once effect to exactly-once effect. No topic, key, group, or payload contract changes.
  - The REST reserve and release contract is unchanged in this change; making a blank referenceId rejected or generating a server-side key would change caller-visible behaviour and is gated behind approval.
rollback_considerations:
  - The behaviour is reversible by removing the deduplication check. The table and constraint remain and are inert.
  - Rolling back after records exist requires no data migration because the table is not referenced by any other entity.
depends_on_change_ids: [CHANGE-AA-002, CHANGE-AA-006]
blocks_change_ids: [CHANGE-AA-010, CHANGE-AA-011, CHANGE-AA-019, CHANGE-AA-022]
open_questions: [OQ-009, OQ-010]
targeted_implementation_discovery_required: false
change_boundary:
  classification: mixed
  existing_business_behavior_preserved: true
  security_and_privacy_behavior_preserved: true
  external_interaction_pattern_changed: false
  approval_required: true
  approval:
    status: not_available
    decision_id: not_applicable
    approved_by: not_applicable
    approved_at: not_applicable
  implementation_allowed: true
  target_level_boundaries:
    - target: consumer_side_deduplication
      classification: resiliency_mechanism
      approval_required: false
      implementation_allowed: true
      note: Order events already carry orderId, so no new caller obligation is created and no externally observable contract changes.
    - target: rest_idempotency_key_contract
      classification: business_logic_change
      approval_required: true
      approval_status: not_available
      implementation_allowed: false
      note: >-
        Treating a repeated POST reserve or release with the same referenceId as a no-op changes the
        duplicate classification visible to callers, and rejecting a blank referenceId changes request
        validation. Both require product and API-contract owner approval.
  unresolved_inputs:
    - Approved REST idempotency-key contract, including behaviour for absent or blank referenceId
    - Approved retention window for processed-operation records
```

### CHANGE-AA-009: Declare bounded, externalized deadlines for every remote dependency

```yaml
change_id: CHANGE-AA-009
title: Declare bounded, externalized deadlines for every remote dependency
finding_ids: [F-009, F-010, F-011]
primary_finding_id: F-009
primary_control_id: SQL-002
related_control_ids: [REDIS-005, KAFKA-005, APP-AA-004, JVM-021, GLB-010]
category: bounded_failure
resiliency_related: true
finding_classification: resiliency
consolidation_note: >-
  F-009, F-010, and F-011 share one root cause: no repository-owned deadline exists for any remote
  dependency, and every value is left at a client default that cannot be tuned per environment. One
  externalized timeout contract covering Azure SQL, Redis, and Kafka remediates all three.
priority:
  value: P1
  policy_id: AA-REMEDIATION-PRIORITY
  policy_version: "1.0.0"
  rule_id: P1-RCV-006
  rationale: >-
    No connect, socket, command, query, transaction, request, or delivery deadline exists for any remote
    dependency, so blocking operations run to driver and client defaults. Rule P1-RCV-006 applies
    because missing timeouts delay health transition, consume request capacity, and prevent traffic
    draining within the required budget. Rule P1-RCV-002 applies concurrently. No P0 rule applies: the
    application starts and operates, and CHANGE-AA-001 independently establishes accurate health
    determination.
  calculated_priority: P1
  override_applied: false
  override_priority: null
  override_reason: null
  override_approved_by: null
  override_approved_at: null
  additional_applicable_rules: [P1-RCV-002]
  p0_elevation_evaluated: not_applicable
implementation_wave: 3
complexity: medium
implementation_status: proposed
implementation_allowed_in_planning_phase: false
objective: >-
  Give every remote call a deadline that is expressed in repository-owned configuration, overridable per
  environment, and orderable against the regional failure budget.
existing_behavior:
  description: >-
    spring.datasource declares only url, username, and password with no Hikari or JDBC timeout property.
    Redis is configured only through spring.data.redis.url and spring.cache.type. Neither profile
    declares any Kafka client timeout, backoff, session, or poll-interval property. The prod profile adds
    only bootstrap-servers and security.protocol.
  evidence: [EV-F-009-01, EV-F-010-01, EV-F-011-01]
proposed_behavior: >-
  HikariCP connection, validation, and lifetime budgets, a JDBC login and socket timeout, a JPA query
  timeout, an explicit transaction timeout on the write paths, a Redis command and connect timeout, and
  the Kafka producer and consumer timeout and backoff properties are all declared as externalized
  placeholders in repository-owned configuration.
what_this_solves: >-
  An Azure SQL failover-group transition, a slow Redis, or an unreachable Kafka cluster produces a clean
  bounded failure instead of an unbounded regional stall.
operating_scenario_impact: >-
  Makes the failure-detection budget expressible so that regional withdrawal, draining, and failover can
  happen inside the approved budget rather than at the outer gateway timeout.
kafka_scenario_context:
  operating_scenario: active_standby
  scenario_preserved: true
  note: Client budgets are declared as placeholders; no approved numeric value is asserted by this plan.
affected_files:
  - source/inventory-service/src/main/resources/application.yml
  - source/inventory-service/src/main/java/com/ecommerce/inventory/service/impl/InventoryServiceImpl.java
new_files: []
configuration_changes:
  - spring.datasource.hikari.connection-timeout
  - spring.datasource.hikari.validation-timeout
  - spring.datasource.hikari.max-lifetime
  - spring.datasource.hikari.keepalive-time
  - spring.datasource.hikari.maximum-pool-size
  - spring.datasource.hikari.data-source-properties.loginTimeout
  - spring.datasource.hikari.data-source-properties.socketTimeout
  - spring.jpa.properties.jakarta.persistence.query.timeout
  - spring.data.redis.timeout
  - spring.data.redis.connect-timeout
  - spring.kafka.producer.properties.max.block.ms
  - spring.kafka.producer.properties.request.timeout.ms
  - spring.kafka.producer.properties.delivery.timeout.ms
  - spring.kafka.consumer.properties.session.timeout.ms
  - spring.kafka.consumer.properties.heartbeat.interval.ms
  - spring.kafka.consumer.properties.max.poll.interval.ms
  - spring.kafka.consumer.properties.max.poll.records
  - spring.kafka.properties.reconnect.backoff.ms
  - spring.kafka.properties.reconnect.backoff.max.ms
  - spring.kafka.properties.retry.backoff.ms
dependency_changes: []
illustrative_code_blocks: [ICB-009-01, ICB-009-02]
proposed_tests: [PT-009-01]
acceptance_criteria:
  - Every declared budget resolves from an environment placeholder and no value is hardcoded without an override.
  - No configuration value contains a region name, regional endpoint, host, or credential.
  - A blocked Azure SQL endpoint causes the affected request to fail within the declared budget rather than blocking indefinitely.
  - A blocked Redis endpoint causes the cache operation to fail within the declared command timeout.
  - A producer send against an unreachable broker returns within the declared max.block.ms rather than blocking the calling transaction indefinitely.
  - Every @Transactional write path declares an explicit timeout attribute.
validation_commands:
  - "mvn -f source/inventory-service/pom.xml -Dtest=DependencyTimeoutConfigurationTest test"
  - "mvn -f source/inventory-service/pom.xml verify"
risks:
  - id: RISK-009-01
    description: A budget set below normal operating latency causes spurious failures.
    mitigation: No approved numeric value is asserted by this plan. Values are placeholders and must be derived from the gateway and load balancer budgets recorded as EG-006.
  - id: RISK-009-02
    description: Constraining the Hikari pool size changes concurrency characteristics under load.
    mitigation: Pool sizing is externalized and is validated together with CHANGE-AA-013 dependency isolation.
compatibility_considerations:
  - Callers may now observe bounded failures where they previously observed long stalls. The caller-visible status mapping for those failures is governed by CHANGE-AA-012 and is approval-gated.
  - JDBC connection-string properties are supplied through Hikari data-source-properties so the externally supplied SQL_CONNECTION_STRING value is not rewritten.
rollback_considerations:
  - Removing the properties restores client defaults with no schema, data, or contract impact.
depends_on_change_ids: []
blocks_change_ids: [CHANGE-AA-010, CHANGE-AA-013]
open_questions: [OQ-011]
targeted_implementation_discovery_required: false
change_boundary:
  classification: supporting_configuration
  existing_business_behavior_preserved: true
  security_and_privacy_behavior_preserved: true
  external_interaction_pattern_changed: false
  approval_required: false
  approval:
    status: not_required
    decision_id: not_applicable
    approved_by: not_applicable
    approved_at: not_applicable
  implementation_allowed: true
  unresolved_inputs:
    - Approved gateway, mesh, and load balancer timeout budget needed to order the application deadlines, carried from EG-006
```

### CHANGE-AA-010: Add bounded retry with transient-failure classification for Azure SQL writes

```yaml
change_id: CHANGE-AA-010
title: Add bounded retry with transient-failure classification for Azure SQL writes
finding_ids: [F-012]
primary_finding_id: F-012
primary_control_id: SQL-003
related_control_ids: [APP-AA-005]
category: retry_management
resiliency_related: true
finding_classification: resiliency
priority:
  value: P1
  policy_id: AA-REMEDIATION-PRIORITY
  policy_version: "1.0.0"
  rule_id: P1-RCV-001
  rationale: >-
    No retry mechanism of any kind exists, so an Azure SQL failover-group transition or transient
    connection reset becomes a terminal application failure on first occurrence. Rule P1-RCV-001 applies
    because retry logic is required. Rule P1-RCV-007 applies concurrently as a constraint: the retry
    introduced here must be bounded and safe, which is why it is sequenced after CHANGE-AA-008
    idempotency. No P0 rule applies because the application starts and operates, and the failure is
    caller-visible rather than silent.
  calculated_priority: P1
  override_applied: false
  override_priority: null
  override_reason: null
  override_approved_by: null
  override_approved_at: null
  additional_applicable_rules: [P1-RCV-007]
  p0_elevation_evaluated: not_applicable
implementation_wave: 3
complexity: medium
implementation_status: proposed
implementation_allowed_in_planning_phase: false
objective: >-
  Let the service ride through a normal Azure SQL transition by retrying transient failures at a safe
  transaction boundary with an externalized, bounded policy.
existing_behavior:
  description: >-
    The build declares no spring-retry, resilience4j, Spring Cloud Circuit Breaker, or equivalent
    dependency, and no production class declares @Retryable, builds a RetryTemplate, or wraps a
    transaction boundary in a retry policy.
  evidence: [EV-F-012-01, EV-F-012-02]
proposed_behavior: >-
  A Resilience4j retry instance with externalized attempt count, backoff, and jitter wraps the write
  operations from outside the transaction boundary, retrying only classified transient failures.
  Non-transient failures, business validation failures, and ambiguous commit outcomes are not retried.
  The retry is safe only because CHANGE-AA-008 has already made the underlying operation idempotent.
what_this_solves: >-
  Routine database transitions stop producing user-visible write failures and stop causing consumed
  order events to exhaust their attempt budget.
operating_scenario_impact: >-
  Failover-group transitions are expected events in the approved deployment model; this makes them
  survivable without operator action.
kafka_scenario_context: null
affected_files:
  - source/inventory-service/pom.xml
  - source/inventory-service/src/main/resources/application.yml
  - source/inventory-service/src/main/java/com/ecommerce/inventory/service/impl/InventoryServiceImpl.java
new_files:
  - source/inventory-service/src/main/java/com/ecommerce/inventory/service/TransientFailureClassifier.java
configuration_changes:
  - resilience4j.retry.instances.inventoryWrite.max-attempts
  - resilience4j.retry.instances.inventoryWrite.wait-duration
  - resilience4j.retry.instances.inventoryWrite.enable-exponential-backoff
  - resilience4j.retry.instances.inventoryWrite.enable-randomized-wait
dependency_changes:
  - io.github.resilience4j:resilience4j-spring-boot3
illustrative_code_blocks: [ICB-010-01, ICB-010-02, ICB-010-03]
proposed_tests: [PT-010-01]
acceptance_criteria:
  - Retry attempt count, wait duration, backoff, and jitter are externalized and overridable per environment.
  - Retry is applied outside the transaction boundary so each attempt runs in a fresh transaction.
  - A classified transient failure is retried; IllegalArgumentException, ResourceNotFoundException, and any business validation failure are not.
  - An ambiguous commit outcome is not retried blindly; it is routed through the idempotency check from CHANGE-AA-008.
  - Every retry attempt and every exhaustion emits a region-tagged metric and a structured log record.
  - Retry exhaustion produces a deterministic terminal outcome rather than an unbounded wait.
validation_commands:
  - "mvn -f source/inventory-service/pom.xml -Dtest=TransientFailureRetryTest test"
  - "mvn -f source/inventory-service/pom.xml verify"
risks:
  - id: RISK-010-01
    description: Retry of a non-idempotent write duplicates a stock movement.
    mitigation: This change hard-depends on CHANGE-AA-008 and must not be implemented before it.
  - id: RISK-010-02
    description: Synchronous retry extends request latency and can exceed the gateway budget.
    mitigation: The total retry budget must be ordered inside the deadlines from CHANGE-AA-009; ordering is asserted in the acceptance criteria and validated in CHANGE-AA-024.
compatibility_considerations:
  - Successful requests are unaffected. Failing requests take longer before failing.
  - Resilience4j is the approved resiliency library; no unapproved substitution is proposed.
rollback_considerations:
  - Removing the retry annotation and configuration restores immediate failure. The dependency can remain declared without effect.
depends_on_change_ids: [CHANGE-AA-008, CHANGE-AA-009]
blocks_change_ids: []
open_questions: [OQ-012]
targeted_implementation_discovery_required: false
library_resolution:
  capability: retry
  approved_library: resilience4j
  approval_source: approved_libraries_governance
  approval_status: approved
  repository_availability: dependency_change_required
  version_source: not_specified
  dependency_change_required: true
  unresolved_inputs:
    - >-
      library_rules.version_source in grounding/governance/approved-libraries.yml is not_specified and
      the Spring Boot 3.3.5 parent does not manage Resilience4j versions, so the version source must be
      confirmed as a BOM import or a managed property before the dependency block is finalized.
change_boundary:
  classification: resiliency_mechanism
  existing_business_behavior_preserved: true
  security_and_privacy_behavior_preserved: true
  external_interaction_pattern_changed: false
  approval_required: false
  approval:
    status: not_required
    decision_id: not_applicable
    approved_by: not_applicable
    approved_at: not_applicable
  implementation_allowed: true
  unresolved_inputs:
    - Approved retry attempt, backoff, and total budget values ordered against the gateway budget
```

### CHANGE-AA-011: Detect, absorb, and report optimistic-locking conflicts

```yaml
change_id: CHANGE-AA-011
title: Detect, absorb, and report optimistic-locking conflicts
finding_ids: [F-013]
primary_finding_id: F-013
primary_control_id: SQL-007
related_control_ids: [APP-AA-012]
category: concurrency_conflict
resiliency_related: true
finding_classification: resiliency
priority:
  value: P1
  policy_id: AA-REMEDIATION-PRIORITY
  policy_version: "1.0.0"
  rule_id: P1-RCV-001
  rationale: >-
    InventoryItem declares @Version so conflicts are detected by the persistence layer, but no service
    method catches ObjectOptimisticLockingFailureException, no retry reloads and reapplies the
    adjustment, and GlobalExceptionHandler does not map it. Rule P1-RCV-001 applies because a bounded
    reload-and-reapply retry is required. Rule P2-DATA-009 also matches but is superseded because the
    highest applicable rule wins. No P0 rule applies because optimistic locking already prevents the lost
    update; the defect converts contention into lost work rather than into corruption.
  calculated_priority: P1
  override_applied: false
  override_priority: null
  override_reason: null
  override_approved_by: null
  override_approved_at: null
  additional_applicable_rules: [P2-DATA-009]
  p0_elevation_evaluated: >-
    Evaluated against the P2 elevation rule and not elevated. The @Version column already prevents a
    silent overwrite, so concurrent operation does not produce a materially unsafe transaction; the
    impact is lost work, not corrupted state.
implementation_wave: 3
complexity: medium
implementation_status: proposed
implementation_allowed_in_planning_phase: false
objective: >-
  Turn ordinary write contention into a bounded reload-and-reapply retry, and give the caller a stable
  answer when contention cannot be resolved.
existing_behavior:
  description: >-
    InventoryItem declares an @Version column. No service method catches
    ObjectOptimisticLockingFailureException, no retry reloads and reapplies the adjustment, no
    pessimistic lock or conditional update is used on reserve and release, and GlobalExceptionHandler
    maps only ResourceNotFoundException, IllegalArgumentException, and MethodArgumentNotValidException.
  evidence: [EV-F-013-01, EV-F-013-02]
proposed_behavior: >-
  Reserve and release are wrapped in a bounded reload-and-reapply retry that re-reads the item and
  re-evaluates the business precondition on each attempt. Exhaustion produces a mapped, documented
  response rather than an opaque 500. The idempotency record from CHANGE-AA-008 ensures a reapplied
  attempt cannot double-apply.
what_this_solves: >-
  A REST reservation and a consumed ORDER_CREATED event adjusting the same row stop discarding one of
  the two operations.
operating_scenario_impact: >-
  Contention between REST traffic and consumer traffic is the normal pattern for this service and
  becomes more likely, not less, as regional traffic patterns change.
kafka_scenario_context: null
affected_files:
  - source/inventory-service/src/main/java/com/ecommerce/inventory/service/impl/InventoryServiceImpl.java
  - source/inventory-service/src/main/java/com/ecommerce/inventory/exception/GlobalExceptionHandler.java
  - source/inventory-service/src/main/resources/application.yml
new_files: []
configuration_changes:
  - resilience4j.retry.instances.inventoryConflict.max-attempts
  - resilience4j.retry.instances.inventoryConflict.wait-duration
dependency_changes: []
illustrative_code_blocks: [ICB-011-01, ICB-011-02]
proposed_tests: [PT-011-01]
acceptance_criteria:
  - A single optimistic-locking conflict on reserve is absorbed by reload-and-reapply and the operation succeeds.
  - Each retry attempt re-reads the entity and re-evaluates the availability or reserved-quantity precondition.
  - Retry attempts and exhaustion are bounded and externally configurable.
  - Conflict occurrences and exhaustions emit region-tagged metrics and structured log records.
  - Exhausted conflict on the consumer path routes through the CHANGE-AA-019 error handler rather than silently advancing the offset.
validation_commands:
  - "mvn -f source/inventory-service/pom.xml -Dtest=OptimisticLockConflictTest test"
  - "mvn -f source/inventory-service/pom.xml verify"
risks:
  - id: RISK-011-01
    description: Reload-and-reapply under sustained contention can extend request latency.
    mitigation: The attempt budget is bounded and externalized, and the total budget is ordered inside the deadlines from CHANGE-AA-009.
compatibility_considerations:
  - Successful conflict absorption is invisible to callers.
  - Mapping exhausted conflict to HTTP 409 introduces a status code the API does not use today, which is an approval-gated target.
rollback_considerations:
  - Removing the retry wrapper and the handler restores the previous behaviour with no data impact.
depends_on_change_ids: [CHANGE-AA-008]
blocks_change_ids: []
open_questions: [OQ-013]
targeted_implementation_discovery_required: false
library_resolution:
  capability: retry
  approved_library: resilience4j
  approval_source: approved_libraries_governance
  approval_status: approved
  repository_availability: dependency_change_required
  version_source: not_specified
  dependency_change_required: false
  note: The dependency itself is introduced by CHANGE-AA-010; this change reuses it.
  unresolved_inputs: []
change_boundary:
  classification: mixed
  existing_business_behavior_preserved: true
  security_and_privacy_behavior_preserved: true
  external_interaction_pattern_changed: false
  approval_required: true
  approval:
    status: not_available
    decision_id: not_applicable
    approved_by: not_applicable
    approved_at: not_applicable
  implementation_allowed: true
  target_level_boundaries:
    - target: reload_and_reapply_retry
      classification: resiliency_mechanism
      approval_required: false
      implementation_allowed: true
    - target: conflict_http_status_mapping
      classification: partner_contract_change
      approval_required: true
      approval_status: not_available
      implementation_allowed: false
      note: >-
        Returning HTTP 409 for an exhausted conflict assigns a new meaning to a status code the API does
        not currently emit and changes the caller-visible failure classification. API contract owner
        approval is required.
  unresolved_inputs:
    - Approved HTTP status and response body for an unresolvable inventory write conflict
```

### CHANGE-AA-012: Give dependency failures stable caller-visible semantics

```yaml
change_id: CHANGE-AA-012
title: Give dependency failures stable caller-visible semantics
finding_ids: [F-014]
primary_finding_id: F-014
primary_control_id: APP-WEB-002
related_control_ids: []
category: failure_classification
resiliency_related: true
finding_classification: resiliency
priority:
  value: P1
  policy_id: AA-REMEDIATION-PRIORITY
  policy_version: "1.0.0"
  rule_id: P1-RCV-005
  rationale: >-
    GlobalExceptionHandler maps only three exception types, so DataAccessException, pool exhaustion,
    Redis connection and command timeout failures, cache serialization failures, and Kafka client
    exceptions all surface as an opaque HTTP 500. Rule P1-RCV-005 applies because exception handling
    must change so that failure signalling matches current production behaviour once the service runs in
    more than one region. No P0 rule applies because traffic eligibility is governed separately by
    CHANGE-AA-001.
  calculated_priority: P1
  override_applied: false
  override_priority: null
  override_reason: null
  override_approved_by: null
  override_approved_at: null
  additional_applicable_rules: []
  p0_elevation_evaluated: not_applicable
implementation_wave: 3
complexity: medium
implementation_status: proposed
implementation_allowed_in_planning_phase: false
objective: >-
  Let a caller and the gateway tell a transient regional dependency failure apart from a permanent
  application error, so a retry or reroute decision can be made safely.
existing_behavior:
  description: >-
    GlobalExceptionHandler maps ResourceNotFoundException to 404 and IllegalArgumentException plus
    MethodArgumentNotValidException to 400. Every other exception falls through to framework default
    error handling and surfaces as an opaque HTTP 500 with no Retry-After, no ProblemDetail, and no
    distinction between permanent and transient failure.
  evidence: [EV-F-014-01]
proposed_behavior: >-
  A dependency-failure handler classifies transient dependency exceptions and returns a distinct,
  documented status with a Retry-After hint and a stable machine-readable error code, while permanent
  application errors keep their current status. Every classification decision is recorded as a
  region-tagged metric.
what_this_solves: >-
  During a regional dependency incident the API stops returning the same opaque status for a request
  that would succeed in the peer region as for one that would fail everywhere.
operating_scenario_impact: >-
  Restores the transient-versus-terminal signal that the approved multi-region routing design depends
  on.
kafka_scenario_context: null
affected_files:
  - source/inventory-service/src/main/java/com/ecommerce/inventory/exception/GlobalExceptionHandler.java
new_files: []
configuration_changes:
  - app.api.retry-after-seconds
dependency_changes: []
illustrative_code_blocks: [ICB-012-01]
proposed_tests: [PT-012-01]
acceptance_criteria:
  - Transient dependency failures are classified and returned with a distinct approved status and a Retry-After header.
  - Permanent application errors continue to return their current status codes unchanged.
  - The error response body preserves the existing timestamp, status, error, and message fields and adds a stable machine-readable code.
  - No response body, header, or log record exposes a connection string, credential, stack trace, or internal host name.
  - Every classification decision increments a region-tagged counter with the classified outcome as a dimension.
validation_commands:
  - "mvn -f source/inventory-service/pom.xml -Dtest=DependencyFailureSemanticsTest test"
  - "mvn -f source/inventory-service/pom.xml verify"
risks:
  - id: RISK-012-01
    description: Clients that treat any non-2xx as terminal may behave differently when a new status appears.
    mitigation: The change is approval-gated precisely because it alters caller-visible failure classification.
  - id: RISK-012-02
    description: Exposing exception detail in the message field could leak infrastructure information.
    mitigation: Dependency failures return a fixed message; the exception message is logged, not returned. This preserves the existing redaction posture.
compatibility_considerations:
  - The existing 400 and 404 mappings and the existing response body shape are preserved.
  - The new status for transient dependency failure is a caller-visible contract change and is therefore gated.
rollback_considerations:
  - Removing the added handler restores the previous opaque 500 behaviour.
depends_on_change_ids: [CHANGE-AA-006]
blocks_change_ids: []
open_questions: [OQ-014]
targeted_implementation_discovery_required: false
change_boundary:
  classification: partner_contract_change
  existing_business_behavior_preserved: true
  security_and_privacy_behavior_preserved: true
  external_interaction_pattern_changed: false
  approval_required: true
  approval:
    status: not_available
    decision_id: not_applicable
    approved_by: not_applicable
    approved_at: not_applicable
  implementation_allowed: false
  target_level_boundaries:
    - target: dependency_failure_status_contract
      classification: partner_contract_change
      approval_required: true
      approval_status: not_available
      implementation_allowed: false
      note: >-
        Returning HTTP 503 with Retry-After for a transient dependency failure assigns a new meaning to a
        status code and changes the failure classification visible to callers and to the gateway. API
        contract owner approval is required before implementation.
    - target: failure_classification_telemetry
      classification: resiliency_mechanism
      approval_required: false
      implementation_allowed: true
      note: >-
        Recording the classification as a metric and a structured log record changes no caller-visible
        behaviour and may proceed independently.
  unresolved_inputs:
    - Approved HTTP status, Retry-After policy, and error-code vocabulary for transient dependency failure
```

### CHANGE-AA-013: Isolate request threads from blocking dependencies

```yaml
change_id: CHANGE-AA-013
title: Isolate request threads from blocking dependencies
finding_ids: [F-015]
primary_finding_id: F-015
primary_control_id: APP-AA-006
related_control_ids: [REDIS-008, JVM-010]
category: dependency_isolation
resiliency_related: true
finding_classification: resiliency
priority:
  value: P1
  policy_id: AA-REMEDIATION-PRIORITY
  policy_version: "1.0.0"
  rule_id: P1-RCV-008
  rationale: >-
    No bulkhead, circuit breaker, semaphore, or custom executor exists, and every REST request, cache
    access, database access, and Kafka production runs on the default servlet thread pool whose default
    size is far larger than the default HikariCP pool with no rejection policy between them. Rule
    P1-RCV-008 applies directly because a missing isolation mechanism can exhaust shared threads and
    connection pools. No P0 rule applies because the failure is a capacity failure rather than a startup,
    crash, or traffic-eligibility failure.
  calculated_priority: P1
  override_applied: false
  override_priority: null
  override_reason: null
  override_approved_by: null
  override_approved_at: null
  additional_applicable_rules: []
  p0_elevation_evaluated: not_applicable
implementation_wave: 3
complexity: high
implementation_status: proposed
implementation_allowed_in_planning_phase: false
objective: >-
  Stop a single degraded dependency from consuming the whole shared request-thread pool, so one failing
  capability degrades instead of removing the pod and the region from service.
existing_behavior:
  description: >-
    The build declares no resilience4j, Spring Cloud Circuit Breaker, Hystrix, or rate-limiter dependency,
    and production source defines no bulkhead, semaphore, or custom executor.
  evidence: [EV-F-015-01]
proposed_behavior: >-
  A Resilience4j bulkhead bounds concurrent calls per dependency, and a circuit breaker opens on
  classified dependency failure so callers fail fast instead of parking. Both are configured through
  externalized properties. The technology-neutral design is stated separately from the library binding.
what_this_solves: >-
  A slow Redis or a blocked Azure SQL pool no longer parks every servlet thread, so read endpoints that
  do not touch the failing dependency and the Actuator endpoints served on the same port keep
  responding.
operating_scenario_impact: >-
  Prevents a single dependency degradation from converting into full regional loss of service, which is
  what the readiness contract from CHANGE-AA-001 would otherwise be forced to react to.
kafka_scenario_context: null
affected_files:
  - source/inventory-service/src/main/resources/application.yml
  - source/inventory-service/src/main/java/com/ecommerce/inventory/service/impl/InventoryServiceImpl.java
new_files: []
configuration_changes:
  - resilience4j.bulkhead.instances.inventoryDb.max-concurrent-calls
  - resilience4j.bulkhead.instances.inventoryDb.max-wait-duration
  - resilience4j.bulkhead.instances.inventoryCache.max-concurrent-calls
  - resilience4j.bulkhead.instances.inventoryCache.max-wait-duration
  - resilience4j.circuitbreaker.instances.inventoryDb
  - resilience4j.circuitbreaker.instances.inventoryCache
dependency_changes: []
illustrative_code_blocks: [ICB-013-01, ICB-013-02, ICB-013-03]
proposed_tests: [PT-013-01]
acceptance_criteria:
  - Concurrent calls to the authoritative store and to the cache are separately bounded and externally configurable.
  - A saturated cache dependency does not prevent an inventory read that misses the cache from completing against the authoritative store.
  - A saturated or open dependency produces a fast, classified failure rather than an indefinite park.
  - Actuator health and prometheus endpoints continue to respond while a dependency is saturated.
  - Breaker state transitions and bulkhead rejections emit region-tagged metrics.
  - No threshold, window size, open duration, half-open call count, or wait duration is hardcoded.
validation_commands:
  - "mvn -f source/inventory-service/pom.xml -Dtest=DependencyIsolationTest test"
  - "mvn -f source/inventory-service/pom.xml verify"
risks:
  - id: RISK-013-01
    description: A concurrency limit set too low reduces throughput under normal load.
    mitigation: All limits are externalized placeholders. No approved numeric value is asserted by this plan.
  - id: RISK-013-02
    description: A circuit breaker on the authoritative store can fail requests that would have succeeded.
    mitigation: The breaker fails fast only after the classified failure rate threshold is met, and the readiness contract from CHANGE-AA-001 governs whether the region should still receive traffic at all.
compatibility_considerations:
  - Successful requests are unaffected. Rejected requests surface through the CHANGE-AA-012 classification, which is approval-gated.
  - Resilience4j is the approved library for circuit_breaker and bulkhead; no unapproved substitution is proposed.
rollback_considerations:
  - Removing the annotations and configuration restores unbounded shared-pool behaviour.
depends_on_change_ids: [CHANGE-AA-009, CHANGE-AA-010]
blocks_change_ids: []
open_questions: [OQ-015]
targeted_implementation_discovery_required: false
library_resolution:
  capability: bulkhead
  approved_library: resilience4j
  approval_source: approved_libraries_governance
  approval_status: approved
  repository_availability: dependency_change_required
  version_source: not_specified
  dependency_change_required: false
  note: The dependency is introduced by CHANGE-AA-010; circuit_breaker and bulkhead are both listed under approved_capabilities.
  unresolved_inputs: []
circuit_breaker_design:
  protected_operation: InventoryServiceImpl.get and InventoryServiceImpl write paths
  fallback_behavior: fail_fast
  failure_classification: transient dependency failure as classified by TransientFailureClassifier from CHANGE-AA-010
  state_scope: per_dependency
  timeout_relationship: >-
    The breaker call budget must be shorter than the dependency deadlines declared in CHANGE-AA-009,
    which must in turn be shorter than the gateway budget recorded as EG-006.
  configuration_externalized: true
  approved_library: resilience4j
change_boundary:
  classification: resiliency_mechanism
  existing_business_behavior_preserved: true
  security_and_privacy_behavior_preserved: true
  external_interaction_pattern_changed: false
  approval_required: false
  approval:
    status: not_required
    decision_id: not_applicable
    approved_by: not_applicable
    approved_at: not_applicable
  implementation_allowed: true
  unresolved_inputs:
    - Approved concurrency limits, failure-rate threshold, sliding-window size, open duration, and half-open call count
```

### CHANGE-AA-014: Contain Redis cache failures and fall through to the authoritative store

```yaml
change_id: CHANGE-AA-014
title: Contain Redis cache failures and fall through to the authoritative store
finding_ids: [F-016]
primary_finding_id: F-016
primary_control_id: REDIS-020
related_control_ids: [APP-AA-006]
category: fault_containment
resiliency_related: true
finding_classification: resiliency
priority:
  value: P1
  policy_id: AA-REMEDIATION-PRIORITY
  policy_version: "1.0.0"
  rule_id: P1-RCV-011
  rationale: >-
    CacheConfig declares @EnableCaching with no body, does not implement CachingConfigurer, and registers
    no CacheErrorHandler, so any Redis get, put, or evict failure propagates to the caller instead of
    falling through to the authoritative Azure SQL repository. Rule P1-RCV-011 applies because an
    optional, non-authoritative dependency unnecessarily prevents safe degraded operation. No P0 rule
    applies because the application starts, operates, and reports health accurately once CHANGE-AA-001
    lands.
  calculated_priority: P1
  override_applied: false
  override_priority: null
  override_reason: null
  override_approved_by: null
  override_approved_at: null
  additional_applicable_rules: [P1-RCV-008]
  p0_elevation_evaluated: not_applicable
implementation_wave: 3
complexity: low
implementation_status: proposed
implementation_allowed_in_planning_phase: false
objective: >-
  Make the cache genuinely optional, so a Redis outage degrades read latency instead of failing a read
  whose authoritative data is fully available.
existing_behavior:
  description: >-
    CacheConfig declares @EnableCaching with no body. It does not implement CachingConfigurer, registers
    no CacheErrorHandler, and supplies no RedisCacheManager.
  evidence: [EV-F-016-01]
proposed_behavior: >-
  CacheConfig implements CachingConfigurer and registers a CacheErrorHandler that absorbs get, put,
  evict, and clear failures, records them as cache-failure outcomes distinct from cache misses, and
  allows the cache interceptor to fall through to the repository.
what_this_solves: >-
  A Redis outage stops taking down a serviceable read capability, and cache eviction failures stop
  failing otherwise successful writes.
operating_scenario_impact: >-
  Keeps the regional read path serviceable when the regional cache tier is unavailable, which is a
  precondition for excluding Redis from the readiness group in CHANGE-AA-001.
kafka_scenario_context: null
affected_files:
  - source/inventory-service/src/main/java/com/ecommerce/inventory/config/CacheConfig.java
new_files: []
configuration_changes: []
dependency_changes: []
illustrative_code_blocks: [ICB-014-01]
proposed_tests: [PT-014-01]
acceptance_criteria:
  - A Redis get failure results in a successful read served from the authoritative repository.
  - A Redis put failure does not fail the surrounding read.
  - A Redis evict or clear failure does not fail the surrounding write.
  - Cache failures increment a cache-failure counter that is distinct from the cache-miss counter.
  - Absorbed cache failures emit a structured log record at WARN containing the cache name and the exception class, with no cached value content.
validation_commands:
  - "mvn -f source/inventory-service/pom.xml -Dtest=CacheFailureContainmentTest test"
  - "mvn -f source/inventory-service/pom.xml verify"
risks:
  - id: RISK-014-01
    description: Silently absorbing evict failures can leave a stale entry after a successful write.
    mitigation: Absorbed evict failures are counted and logged, and the TTL introduced by CHANGE-AA-015 bounds how long a stale entry can survive.
compatibility_considerations:
  - Read and write responses become more available, not less. No API contract changes.
rollback_considerations:
  - Removing the CachingConfigurer implementation restores propagating behaviour.
depends_on_change_ids: [CHANGE-AA-006]
blocks_change_ids: []
reinforces_change_ids: [CHANGE-AA-001]
reinforcement_note: >-
  CHANGE-AA-001 excludes Redis from the readiness group on its own evidence, so it does not wait on this
  change. This change completes the degraded-mode behaviour that makes that exclusion operationally
  safe, and Step 5 closure of F-008 and F-016 should be evaluated together.
open_questions: []
targeted_implementation_discovery_required: false
change_boundary:
  classification: resiliency_mechanism
  existing_business_behavior_preserved: true
  security_and_privacy_behavior_preserved: true
  external_interaction_pattern_changed: false
  approval_required: false
  approval:
    status: not_required
    decision_id: not_applicable
    approved_by: not_applicable
    approved_at: not_applicable
  implementation_allowed: true
  unresolved_inputs: []
```

### CHANGE-AA-015: Declare an explicit Redis cache manager contract

```yaml
change_id: CHANGE-AA-015
title: Declare an explicit Redis cache manager contract
finding_ids: [F-029, F-017, F-018]
primary_finding_id: F-029
primary_control_id: REDIS-012
related_control_ids: [REDIS-011, REDIS-022, APP-CACHE-001]
category: cache_contract
resiliency_related: true
finding_classification: mixed
finding_classification_detail:
  F-029: non_resiliency
  F-017: resiliency
  F-018: non_resiliency
consolidation_note: >-
  All three findings exist for the same reason: no RedisCacheConfiguration bean is declared, so value
  serialization, entry expiry, and key prefixing all fall to framework defaults. One bean remediates all
  three, and generating three separate proposals for the same bean would duplicate the code proposal.
  Each finding keeps its Step 2 classification.
priority:
  value: P1
  policy_id: AA-REMEDIATION-PRIORITY
  policy_version: "1.0.0"
  rule_id: P1-RCV-011
  rationale: >-
    The cached type InventoryResponse is a Java record that does not implement Serializable and no value
    SerializationPair is declared, so the default JDK value serializer fails on every cache write. The
    optional cache dependency therefore prevents safe operation of the read path, which rule P1-RCV-011
    governs. The TTL gap under F-017 matches rule P2-DATA-010 and the key-namespace gap under F-018
    matches rule P3-OPS-001; both are superseded because the highest applicable rule wins across the
    consolidated change.
  calculated_priority: P1
  override_applied: false
  override_priority: null
  override_reason: null
  override_approved_by: null
  override_approved_at: null
  additional_applicable_rules: [P2-DATA-010, P3-OPS-001]
  p0_elevation_evaluated: >-
    Evaluated and not elevated. The defect fails a read path but does not prevent startup, cause a crash,
    or corrupt authoritative state, and it is not specific to concurrent regional operation.
implementation_wave: 3
complexity: medium
implementation_status: proposed
implementation_allowed_in_planning_phase: false
objective: >-
  Replace three framework defaults with one explicit cache contract covering value serialization, entry
  expiry, and key isolation.
existing_behavior:
  description: >-
    spring.cache.type is redis and CacheConfig supplies no RedisCacheConfiguration, so the framework
    default JDK value serializer applies to a non-Serializable record, no time-to-live is configured, and
    no key prefix, environment qualifier, or payload schema version is applied.
  evidence: [EV-F-029-01, EV-F-029-02, EV-F-017-01, EV-F-018-01]
proposed_behavior: >-
  A RedisCacheConfiguration bean declares an explicit JSON value serializer bound to the cached type, an
  externalized entry time-to-live, and a key prefix composed from an externalized application, environment,
  and cache-schema-version qualifier. Null values are not cached.
what_this_solves: >-
  The cached read path works, cache entries expire on a bounded schedule, and two deployments sharing a
  Redis instance or two application versions during a rolling release stop colliding on identical keys.
operating_scenario_impact: >-
  A bounded freshness window lets a regional cache converge after a failover, and versioned keys let a
  response-model change invalidate a generation without flushing a shared instance.
kafka_scenario_context: null
affected_files:
  - source/inventory-service/src/main/java/com/ecommerce/inventory/config/CacheConfig.java
  - source/inventory-service/src/main/resources/application.yml
new_files: []
configuration_changes:
  - app.cache.inventory.ttl
  - app.cache.key-prefix
  - app.cache.schema-version
dependency_changes: []
illustrative_code_blocks: [ICB-015-01, ICB-015-02]
proposed_tests: [PT-015-01, PT-015-02]
acceptance_criteria:
  - A cached read of an inventory item succeeds against a real Redis instance and returns an equal InventoryResponse on the second call.
  - The value serializer is declared explicitly and does not depend on Java serialization or on the cached type implementing Serializable.
  - Every cache entry carries a time-to-live sourced from externalized configuration.
  - Every cache key is prefixed with the application, environment, and cache schema version qualifiers.
  - Changing the cache schema version produces a disjoint key space with no reuse of previously cached values.
  - Null results are not cached.
validation_commands:
  - "mvn -f source/inventory-service/pom.xml -Dtest=RedisCacheContractIntegrationTest test"
  - "mvn -f source/inventory-service/pom.xml verify"
risks:
  - id: RISK-015-01
    description: Changing the key prefix orphans every existing cached entry.
    mitigation: Entries are non-authoritative and the authoritative repository serves every miss. The orphaned generation expires under the new TTL or under the deployed maxmemory policy.
  - id: RISK-015-02
    description: A JSON value serializer that embeds type information can break when the cached record shape changes.
    mitigation: The cache schema version qualifier is part of the key, so a shape change produces a new key space rather than a deserialization failure.
compatibility_considerations:
  - The cached value wire format changes. Because the key prefix changes at the same time, no reader ever encounters a value written in the old format.
  - No REST response shape changes; the serializer applies to the cache only.
rollback_considerations:
  - Reverting the bean restores the default serializer and the broken cached read path, so rollback must be paired with reverting the caching annotation or disabling the cache.
depends_on_change_ids: []
blocks_change_ids: [CHANGE-AA-016, CHANGE-AA-023]
open_questions: [OQ-016]
targeted_implementation_discovery_required: false
change_boundary:
  classification: supporting_configuration
  existing_business_behavior_preserved: true
  security_and_privacy_behavior_preserved: true
  external_interaction_pattern_changed: false
  approval_required: false
  approval:
    status: not_required
    decision_id: not_applicable
    approved_by: not_applicable
    approved_at: not_applicable
  implementation_allowed: true
  unresolved_inputs:
    - Approved inventory cache time-to-live value
    - Environment qualifier source, since the environment name is supplied at deployment time
```

### CHANGE-AA-016: Coalesce concurrent cache misses

```yaml
change_id: CHANGE-AA-016
title: Coalesce concurrent cache misses
finding_ids: [F-019]
primary_finding_id: F-019
primary_control_id: REDIS-009
related_control_ids: [APP-CACHE-004]
category: overload_protection
resiliency_related: true
finding_classification: resiliency
priority:
  value: P1
  policy_id: AA-REMEDIATION-PRIORITY
  policy_version: "1.0.0"
  rule_id: P1-RCV-008
  rationale: >-
    @Cacheable is declared without sync and no single-flight or lock guards the cache loader, so every
    concurrent miss for the same key executes its own repository read. Rule P1-RCV-008 applies because a
    missing equivalent limiting mechanism can exhaust the connection pool and shared request threads
    exactly when a recovering database is least able to absorb the load. No P0 rule applies because the
    condition is a load amplification rather than a startup, crash, or traffic-eligibility failure.
  calculated_priority: P1
  override_applied: false
  override_priority: null
  override_reason: null
  override_approved_by: null
  override_approved_at: null
  additional_applicable_rules: []
  p0_elevation_evaluated: not_applicable
implementation_wave: 3
complexity: low
implementation_status: proposed
implementation_allowed_in_planning_phase: false
objective: >-
  Make a cold or emptied regional cache produce one authoritative read per key rather than one per
  concurrent request.
existing_behavior:
  description: >-
    @Cacheable is declared without sync, and no single-flight, lock, or SETNX guard exists around the
    cache loader. Every concurrent miss for the same key executes its own repository.findById.
  evidence: [EV-F-019-01]
proposed_behavior: >-
  The cached read declares sync so the cache abstraction coalesces concurrent loads for the same key, and
  the coalescing behaviour is covered by a concurrency test.
what_this_solves: >-
  A regional cache that is empty after a failover or a Redis restart no longer produces a concurrent load
  spike against a database that is itself recovering.
operating_scenario_impact: >-
  Protects the authoritative store during exactly the window the approved regional recovery model creates.
kafka_scenario_context: null
affected_files:
  - source/inventory-service/src/main/java/com/ecommerce/inventory/service/impl/InventoryServiceImpl.java
new_files: []
configuration_changes: []
dependency_changes: []
illustrative_code_blocks: [ICB-016-01]
proposed_tests: [PT-016-01]
acceptance_criteria:
  - Concurrent reads for the same identifier against an empty cache produce exactly one repository read.
  - Concurrent reads for different identifiers are not serialized against one another.
  - Coalescing does not change the value returned to any caller.
validation_commands:
  - "mvn -f source/inventory-service/pom.xml -Dtest=CacheStampedeTest test"
  - "mvn -f source/inventory-service/pom.xml verify"
risks:
  - id: RISK-016-01
    description: sync serializes loaders per key, so a slow authoritative read increases latency for other waiters on the same key.
    mitigation: The read is bounded by the deadlines from CHANGE-AA-009 and by the bulkhead from CHANGE-AA-013.
  - id: RISK-016-02
    description: sync is not supported by every cache manager configuration.
    mitigation: RedisCacheManager supports synchronized cache access; CHANGE-AA-015 declares the cache manager explicitly, so the capability is established before this change lands.
compatibility_considerations:
  - No API, key, or value contract changes.
rollback_considerations:
  - Removing the sync attribute restores the previous behaviour.
depends_on_change_ids: [CHANGE-AA-015]
blocks_change_ids: []
open_questions: []
targeted_implementation_discovery_required: false
change_boundary:
  classification: resiliency_mechanism
  existing_business_behavior_preserved: true
  security_and_privacy_behavior_preserved: true
  external_interaction_pattern_changed: false
  approval_required: false
  approval:
    status: not_required
    decision_id: not_applicable
    approved_by: not_applicable
    approved_at: not_applicable
  implementation_allowed: true
  unresolved_inputs: []
```

### CHANGE-AA-017: Bound the inventory list endpoint

```yaml
change_id: CHANGE-AA-017
title: Bound the inventory list endpoint
finding_ids: [F-025]
primary_finding_id: F-025
primary_control_id: JVM-004
related_control_ids: []
category: overload_protection
resiliency_related: true
finding_classification: resiliency
priority:
  value: P1
  policy_id: AA-REMEDIATION-PRIORITY
  policy_version: "1.0.0"
  rule_id: P1-RCV-008
  rationale: >-
    InventoryServiceImpl.list calls repository.findAll and materializes the whole table per request with
    no Pageable, page size, result limit, or streaming. Rule P1-RCV-008 applies because the missing bound
    lets ordinary API usage exhaust heap, a shared application resource, and remove pod capacity. No P0
    rule applies because the failure is load-dependent rather than a deterministic startup or crash
    condition.
  calculated_priority: P1
  override_applied: false
  override_priority: null
  override_reason: null
  override_approved_by: null
  override_approved_at: null
  additional_applicable_rules: []
  p0_elevation_evaluated: not_applicable
implementation_wave: 3
complexity: medium
implementation_status: proposed
implementation_allowed_in_planning_phase: false
objective: >-
  Make the peak heap required by a list request independent of the size of the inventory table.
existing_behavior:
  description: >-
    InventoryServiceImpl.list calls repository.findAll, streams every returned entity through the mapper,
    and collects the result into a list. There is no Pageable parameter, no page size, no result limit,
    no streaming, and no maximum on the response.
  evidence: [EV-F-025-01]
proposed_behavior: >-
  The service exposes a paged list operation with an externally configured default and maximum page size,
  and the controller binds a Pageable with the same bounds. The response contract change is isolated as
  an approval-required target; the service-level bound is implementable independently.
what_this_solves: >-
  A handful of concurrent list requests against a production-sized table can no longer drive the pod into
  sustained GC pressure or an OutOfMemoryError.
operating_scenario_impact: >-
  Removes a pod-loss mechanism that is indistinguishable from a dependency failure and that removes
  capacity from a region.
kafka_scenario_context: null
affected_files:
  - source/inventory-service/src/main/java/com/ecommerce/inventory/service/InventoryService.java
  - source/inventory-service/src/main/java/com/ecommerce/inventory/service/impl/InventoryServiceImpl.java
  - source/inventory-service/src/main/java/com/ecommerce/inventory/controller/InventoryController.java
  - source/inventory-service/src/main/resources/application.yml
new_files: []
configuration_changes:
  - spring.data.web.pageable.default-page-size
  - spring.data.web.pageable.max-page-size
dependency_changes: []
illustrative_code_blocks: [ICB-017-01, ICB-017-02]
proposed_tests: [PT-017-01]
acceptance_criteria:
  - No production code path calls repository.findAll without a Pageable.
  - A list request returns at most the configured maximum page size regardless of the requested size.
  - Default and maximum page sizes are externalized and overridable per environment.
  - Peak allocation for a list request is bounded by the page size rather than by the table size.
validation_commands:
  - "mvn -f source/inventory-service/pom.xml -Dtest=BoundedInventoryListTest test"
  - "mvn -f source/inventory-service/pom.xml verify"
risks:
  - id: RISK-017-01
    description: Existing callers of GET /api/v1/inventory expect an unbounded JSON array and will silently receive a truncated or reshaped result.
    mitigation: The caller-visible contract change is held at implementation_allowed false until the API contract owner approves the pagination shape and the migration approach.
compatibility_considerations:
  - Returning a page envelope instead of a bare array is a breaking response-shape change.
  - Returning a bare array capped at the maximum page size silently truncates results, which is also a caller-visible behaviour change.
  - Both options require approval; neither is selected by this plan.
rollback_considerations:
  - Reverting the controller signature and the service method restores the previous contract.
depends_on_change_ids: []
blocks_change_ids: []
open_questions: [OQ-017]
targeted_implementation_discovery_required: false
change_boundary:
  classification: mixed
  existing_business_behavior_preserved: false
  security_and_privacy_behavior_preserved: true
  external_interaction_pattern_changed: false
  approval_required: true
  approval:
    status: not_available
    decision_id: not_applicable
    approved_by: not_applicable
    approved_at: not_applicable
  implementation_allowed: false
  target_level_boundaries:
    - target: paged_service_operation
      classification: resiliency_mechanism
      approval_required: false
      implementation_allowed: true
      note: >-
        Adding a paged service operation alongside the existing one introduces the bound without removing
        any caller-visible behaviour.
    - target: list_endpoint_response_contract
      classification: partner_contract_change
      approval_required: true
      approval_status: not_available
      implementation_allowed: false
      note: >-
        Changing GET /api/v1/inventory to return a page envelope or a truncated array changes
        customer-visible results and requires API contract owner approval.
  unresolved_inputs:
    - Approved pagination contract for GET /api/v1/inventory, including response shape and default and maximum page size
```

### CHANGE-AA-018: Make Kafka publication durable and its outcome observable

```yaml
change_id: CHANGE-AA-018
title: Make Kafka publication durable and its outcome observable
finding_ids: [F-001]
primary_finding_id: F-001
primary_control_id: APP-KAFKA-005
related_control_ids: [KAFKA-002, APP-AA-016]
category: durability
resiliency_related: true
finding_classification: resiliency
priority:
  value: P1
  policy_id: AA-REMEDIATION-PRIORITY
  policy_version: "1.0.0"
  rule_id: P1-RCV-005
  rationale: >-
    The send future is discarded and acks, retries, enable.idempotence, delivery.timeout.ms, and
    max.in.flight.requests.per.connection are all left at client defaults, so a failed produce is
    indistinguishable from a successful one inside the application. Rule P1-RCV-005 applies because
    processing, logging, and exception handling must change for failure behaviour to be preserved once
    the service runs in more than one region. Rule P1-RCV-002 applies concurrently for the delivery and
    request timeout settings. No P0 rule applies: the application starts and operates, and the impact is
    on downstream event state rather than on authoritative state or on regional health determination.
  calculated_priority: P1
  override_applied: false
  override_priority: null
  override_reason: null
  override_approved_by: null
  override_approved_at: null
  additional_applicable_rules: [P1-RCV-002]
  p0_elevation_evaluated: >-
    Evaluated against the P2 elevation rule and against P0-AA-012 and not elevated. Authoritative Azure
    SQL state remains correct; the impact is downstream event divergence, which does not make the
    authoritative business transaction unsafe when both regions are active.
implementation_wave: 3
complexity: medium
implementation_status: proposed
implementation_allowed_in_planning_phase: false
objective: >-
  Stop losing inventory events silently, and make every publication outcome observable and deployment
  tunable.
existing_behavior:
  description: >-
    InventoryEventProducer.publish calls kafkaTemplate.send and discards the returned CompletableFuture.
    No callback, whenComplete handler, ProducerListener, or blocking get inspects the delivery outcome.
    The producer configuration sets only key and value serializers.
  evidence: [EV-F-001-01, EV-F-001-02]
proposed_behavior: >-
  Producer acks, enable.idempotence, retries, delivery.timeout.ms, and
  max.in.flight.requests.per.connection are declared as externalized properties. The send result is
  observed through whenComplete, and success and failure each increment the region-tagged publication
  counter and, on failure, emit a structured log record naming the topic, key, and exception class.
what_this_solves: >-
  A broker outage, leader election, partition unavailability, or serialization failure stops being
  invisible, so an operator can detect the loss and decide on replay.
operating_scenario_impact: >-
  Publication durability and failure visibility are preconditions for any recovery action during an
  active-standby failover window.
kafka_scenario_context:
  operating_scenario: active_standby
  scenario_preserved: true
  note: >-
    Broker-side min.insync.replicas, topic replication factor, and Cluster Linking state are outside the
    remediation boundary and are not modified.
affected_files:
  - source/inventory-service/src/main/java/com/ecommerce/inventory/kafka/producer/InventoryEventProducer.java
  - source/inventory-service/src/main/resources/application.yml
new_files: []
configuration_changes:
  - spring.kafka.producer.acks
  - spring.kafka.producer.properties.enable.idempotence
  - spring.kafka.producer.properties.max.in.flight.requests.per.connection
  - spring.kafka.producer.retries
dependency_changes: []
illustrative_code_blocks: [ICB-018-01, ICB-018-02]
proposed_tests: [PT-018-01]
acceptance_criteria:
  - acks, enable.idempotence, retries, delivery.timeout.ms, and max.in.flight.requests.per.connection are declared as externalized properties.
  - Every send result is observed and produces exactly one success or failure outcome record.
  - A failed send emits a structured log record naming the topic, the record key, and the exception class, and increments the failure counter.
  - A failed send does not swallow the failure silently and does not block the calling thread beyond the configured max.block.ms from CHANGE-AA-009.
  - No log record or metric tag contains the event payload.
validation_commands:
  - "mvn -f source/inventory-service/pom.xml -Dtest=InventoryEventProducerDurabilityTest test"
  - "mvn -f source/inventory-service/pom.xml verify"
risks:
  - id: RISK-018-01
    description: Enabling idempotence and acks all increases produce latency and can surface as slower writes.
    mitigation: The producer path is bounded by max.block.ms from CHANGE-AA-009, and the values are externalized rather than fixed.
  - id: RISK-018-02
    description: Observing the send result asynchronously still leaves the event lost if the callback fires after the transaction commits.
    mitigation: Commit-ordered publication and the durable intent record are delivered by CHANGE-AA-021, which is sequenced after this change and depends on it.
compatibility_considerations:
  - Topic name, key, and payload shape are unchanged by this change; the envelope contract change is governed by CHANGE-AA-022.
rollback_considerations:
  - Removing the callback and the producer properties restores fire-and-forget behaviour with no schema or contract impact.
depends_on_change_ids: [CHANGE-AA-006, CHANGE-AA-009]
blocks_change_ids: [CHANGE-AA-021]
open_questions: [OQ-018]
targeted_implementation_discovery_required: false
change_boundary:
  classification: resiliency_mechanism
  existing_business_behavior_preserved: true
  security_and_privacy_behavior_preserved: true
  external_interaction_pattern_changed: false
  approval_required: false
  approval:
    status: not_required
    decision_id: not_applicable
    approved_by: not_applicable
    approved_at: not_applicable
  implementation_allowed: true
  unresolved_inputs:
    - Approved acks and idempotence settings, which interact with broker-side min.insync.replicas recorded as EG-002
```

### CHANGE-AA-019: Own the Kafka listener error, offset, and dead-letter contract

```yaml
change_id: CHANGE-AA-019
title: Own the Kafka listener error, offset, and dead-letter contract
finding_ids: [F-005, F-006]
primary_finding_id: F-005
primary_control_id: APP-KAFKA-002
related_control_ids: [APP-KAFKA-003, KAFKA-004, KAFKA-006]
category: fault_tolerance
resiliency_related: true
finding_classification: resiliency
consolidation_note: >-
  F-005 and F-006 share one root cause: the listener container contract is entirely default, so ack mode,
  attempt budget, error handling, and recovery destination are all implicit. One listener container
  factory plus guarded payload extraction remediates both.
priority:
  value: P1
  policy_id: AA-REMEDIATION-PRIORITY
  policy_version: "1.0.0"
  rule_id: P1-RCV-007
  rationale: >-
    Offset commit is governed entirely by container defaults and no error handler or recoverer is
    declared, so a failing record is retried on the container default backoff and then skipped while the
    offset advances. Rule P1-RCV-007 applies because the retry behaviour is immediate, unbounded by
    repository-owned configuration, and unsafe against the non-idempotent effects addressed by
    CHANGE-AA-008. Rules P2-DATA-001 and P2-DATA-007 also match but are superseded because the highest
    applicable rule wins.
  calculated_priority: P1
  override_applied: false
  override_priority: null
  override_reason: null
  override_approved_by: null
  override_approved_at: null
  additional_applicable_rules: [P2-DATA-001, P2-DATA-007]
  p0_elevation_evaluated: >-
    Evaluated against P0-AA-012 and not elevated. Once CHANGE-AA-008 makes the effect idempotent, the
    container retry no longer duplicates a business effect, so the residual impact is work loss rather
    than unsafe concurrent mutation.
implementation_wave: 3
complexity: high
implementation_status: proposed
implementation_allowed_in_planning_phase: false
objective: >-
  Make offset advancement a consequence of durable business completion or of an explicit quarantine
  decision, never of an exhausted implicit attempt budget.
existing_behavior:
  description: >-
    The Kafka consumer configuration declares only auto-offset-reset, serializers, and trusted packages.
    No ack-mode, manual acknowledgment, listener container factory, or transactional.id is configured. No
    CommonErrorHandler, DefaultErrorHandler bean, DeadLetterPublishingRecoverer, dead-letter topic, or
    retry topic is declared. Payload extraction reads untyped map values with String.valueOf and an
    unchecked (Number) cast on quantity with no null or type guard.
  evidence: [EV-F-005-01, EV-F-006-01]
proposed_behavior: >-
  A named listener container factory declares manual immediate acknowledgment, an externally configured
  attempt budget with exponential backoff, a classification of non-retryable extraction and validation
  failures, and a DeadLetterPublishingRecoverer that routes exhausted and non-retryable records to an
  externally named dead-letter destination. The consumer extracts payload fields through a guarded
  mapper that raises a classified non-retryable failure on a missing or wrongly typed field.
what_this_solves: >-
  An order event that cannot be applied is either retried within a bounded budget and then quarantined
  with a durable copy, or is quarantined immediately when it is structurally invalid. No record is
  abandoned without an artifact.
operating_scenario_impact: >-
  Removes the silent-loss path that a database transition during an active-standby window would
  otherwise trigger.
kafka_scenario_context:
  operating_scenario: active_standby
  scenario_preserved: true
  note: >-
    Dead-letter topic provisioning, ACLs, and retention are outside the remediation boundary; the
    destination name is supplied through externalized configuration.
affected_files:
  - source/inventory-service/src/main/java/com/ecommerce/inventory/kafka/consumer/OrderEventConsumer.java
  - source/inventory-service/src/main/resources/application.yml
new_files:
  - source/inventory-service/src/main/java/com/ecommerce/inventory/kafka/KafkaConsumerConfig.java
  - source/inventory-service/src/main/java/com/ecommerce/inventory/kafka/consumer/OrderEventPayload.java
  - source/inventory-service/src/main/java/com/ecommerce/inventory/kafka/consumer/NonRetryablePayloadException.java
configuration_changes:
  - spring.kafka.listener.ack-mode
  - app.kafka.consumer.max-attempts
  - app.kafka.consumer.backoff-initial-interval
  - app.kafka.consumer.backoff-multiplier
  - app.kafka.consumer.backoff-max-interval
  - app.kafka.consumer.dead-letter-topic
dependency_changes: []
illustrative_code_blocks: [ICB-019-01, ICB-019-02, ICB-019-03, ICB-019-04]
proposed_tests: [PT-019-01, PT-019-02]
acceptance_criteria:
  - The listener acknowledges manually and the offset advances only after durable business completion or after a successful quarantine publication.
  - The attempt budget and backoff are externally configured and no attempt is immediate.
  - A record with a missing or non-numeric quantity is classified non-retryable and quarantined on the first attempt without consuming the retry budget.
  - A record whose processing exhausts the retry budget is published to the configured dead-letter destination before the offset advances.
  - A quarantine publication failure does not advance the offset.
  - Every retry, quarantine, and quarantine failure emits a region-tagged metric and a structured log record with no payload content.
validation_commands:
  - "mvn -f source/inventory-service/pom.xml -Dtest=OrderEventErrorHandlingTest test"
  - "mvn -f source/inventory-service/pom.xml -Dtest=PoisonRecordQuarantineTest test"
  - "mvn -f source/inventory-service/pom.xml verify"
risks:
  - id: RISK-019-01
    description: Manual acknowledgment introduces the possibility of a stuck partition if a bug prevents acknowledgment.
    mitigation: Every path through the listener either acknowledges or raises a classified exception that the error handler resolves; the backlog-age gauge from CHANGE-AA-006 makes a stuck partition visible.
  - id: RISK-019-02
    description: The dead-letter destination may not exist, which turns a quarantine into a publication failure.
    mitigation: Topic provisioning is outside the boundary and is recorded as an unresolved input; the failure path is explicitly defined to hold the offset rather than lose the record.
compatibility_considerations:
  - Consumer group id, topic name, and inbound payload shape are unchanged.
  - Records that would previously have been skipped are now quarantined, which is a new outbound publication to a new destination.
rollback_considerations:
  - Removing the container factory reference restores default container behaviour. Records already quarantined remain on the dead-letter destination.
depends_on_change_ids: [CHANGE-AA-006, CHANGE-AA-008, CHANGE-AA-009]
blocks_change_ids: []
open_questions: [OQ-019]
targeted_implementation_discovery_required: false
change_boundary:
  classification: resiliency_mechanism
  existing_business_behavior_preserved: true
  security_and_privacy_behavior_preserved: true
  external_interaction_pattern_changed: true
  external_interaction_change_note: >-
    Quarantined records are published to a new dead-letter destination. This is a new outbound Kafka
    publication, but it carries no new business effect, changes no customer-visible result, and replaces
    a silent discard. It is classified as a resiliency mechanism rather than a partner-contract change
    because the destination is owned by this service and no external consumer contract is altered.
  approval_required: false
  approval:
    status: not_required
    decision_id: not_applicable
    approved_by: not_applicable
    approved_at: not_applicable
  implementation_allowed: true
  unresolved_inputs:
    - Approved dead-letter destination name, retention, and access policy
```

### CHANGE-AA-020: Recover from credential rotation without a process restart

```yaml
change_id: CHANGE-AA-020
title: Recover from credential rotation without a process restart
finding_ids: [F-023]
primary_finding_id: F-023
primary_control_id: KV-005
related_control_ids: [KV-007, KV-010, APP-AA-014]
category: recovery
resiliency_related: true
finding_classification: resiliency
priority:
  value: P1
  policy_id: AA-REMEDIATION-PRIORITY
  policy_version: "1.0.0"
  rule_id: P1-RCV-009
  rationale: >-
    Key Vault material is resolved once at startup and the HikariCP datasource and the Lettuce connection
    factory retain it for the lifetime of the process, with no refresh interval, scheduled refresh,
    @RefreshScope bean, EnvironmentChangeEvent listener, or client-recreation path. Rule P1-RCV-009
    applies because the application cannot refresh credentials or return to readiness after a rotation or
    a vault restoration without restarting the process. No P0 rule applies because the running service
    does not require live vault access and remains able to serve until the held material is invalidated.
  calculated_priority: P1
  override_applied: false
  override_priority: null
  override_reason: null
  override_approved_by: null
  override_approved_at: null
  additional_applicable_rules: []
  p0_elevation_evaluated: not_applicable
implementation_wave: 3
complexity: high
implementation_status: proposed
implementation_allowed_in_planning_phase: false
objective: >-
  Either converge automatically on rotated credential material, or make the restart requirement an
  explicit, detected, and observable contract rather than an implicit assumption.
existing_behavior:
  description: >-
    Key Vault material is resolved through a Spring property source at startup. No refresh interval,
    scheduled refresh, @RefreshScope bean, EnvironmentChangeEvent listener, or client-recreation path
    exists. The HikariCP datasource and the Lettuce connection factory are initialized once with startup
    material.
  evidence: [EV-F-023-01]
proposed_behavior: >-
  A scheduled refresh reloads the Key Vault property source on an externally configured interval, an
  authentication-failure detector classifies credential rejection separately from connectivity failure,
  and a rotation handler evicts the affected pool so new connections are established with the refreshed
  material. Where automatic re-initialization is not possible for a given client, the restart requirement
  is stated explicitly in repository-owned configuration and surfaced as a metric and a log record.
what_this_solves: >-
  Recovery from a credential or identity event stops requiring a manual rolling restart of every pod in
  the region.
operating_scenario_impact: >-
  Removes an operator-dependent step from regional recovery.
kafka_scenario_context: null
affected_files:
  - source/inventory-service/src/main/resources/application-prod.yml
new_files:
  - source/inventory-service/src/main/java/com/ecommerce/inventory/config/SecretRotationHandler.java
configuration_changes:
  - spring.cloud.azure.keyvault.secret.property-sources[0].refresh-interval
  - app.secrets.rotation.enabled
  - app.secrets.rotation.pool-eviction-enabled
dependency_changes: []
illustrative_code_blocks: [ICB-020-01, ICB-020-02, ICB-020-03]
proposed_tests: [PT-020-01]
acceptance_criteria:
  - The Key Vault property-source refresh interval is declared in repository-owned configuration and is externally overridable.
  - A credential rejection is classified separately from a connectivity failure and increments a distinct region-tagged counter.
  - After a simulated rotation the service establishes new connections with the refreshed material without a process restart.
  - Where automatic re-initialization is not implemented for a client, the restart requirement is stated explicitly in configuration and emitted as an observable signal.
  - No secret value is written to a log record, metric name, metric tag, or health detail.
validation_commands:
  - "mvn -f source/inventory-service/pom.xml -Dtest=SecretRotationRecoveryTest test"
  - "mvn -f source/inventory-service/pom.xml verify"
risks:
  - id: RISK-020-01
    description: Pool eviction on a false-positive credential rejection causes an unnecessary connection storm.
    mitigation: Eviction is gated behind the classification and behind an externally configurable enablement flag, and it is rate limited by the refresh interval.
  - id: RISK-020-02
    description: A refresh interval that is too short increases Key Vault request volume and can trigger throttling.
    mitigation: The interval is externalized and is bounded by the Key Vault client retry budget from CHANGE-AA-003.
compatibility_considerations:
  - No API, event, or schema contract changes.
  - The Spring Cloud Azure refresh-interval property is a supported capability of the declared starter version and is not a new dependency.
rollback_considerations:
  - Disabling the rotation flag and removing the refresh interval restores the previous startup-only binding.
depends_on_change_ids: [CHANGE-AA-003, CHANGE-AA-006]
blocks_change_ids: []
open_questions: [OQ-020]
targeted_implementation_discovery_required: true
targeted_discovery_scope: redis_client_reinitialization_target_only
change_boundary:
  classification: mixed
  existing_business_behavior_preserved: true
  security_and_privacy_behavior_preserved: true
  external_interaction_pattern_changed: false
  approval_required: false
  approval:
    status: not_required
    decision_id: not_applicable
    approved_by: not_applicable
    approved_at: not_applicable
  implementation_allowed: true
  unresolved_inputs:
    - Approved credential rotation schedule and whether rotation is coordinated with a rolling restart today
    - Whether Redis authentication material is supplied as a connection-string URL that requires full client re-creation rather than a credential refresh
```

### CHANGE-AA-021: Adopt a transactional outbox for commit-ordered event publication

```yaml
change_id: CHANGE-AA-021
title: Adopt a transactional outbox for commit-ordered event publication
finding_ids: [F-002]
primary_finding_id: F-002
primary_control_id: APP-DB-003
related_control_ids: [SQL-013]
category: cross_store_consistency
resiliency_related: true
finding_classification: resiliency
priority:
  value: P2
  policy_id: AA-REMEDIATION-PRIORITY
  policy_version: "1.0.0"
  rule_id: P2-DATA-002
  rationale: >-
    saveAndPublish issues the Kafka send inside the @Transactional service method, and no transactional
    outbox, @TransactionalEventListener, or AFTER_COMMIT hook exists. Rule P2-DATA-002 names outbox
    adoption directly and is the precise match. Rule P2-DATA-005 also applies. No P1 rule applies because
    the remediation is an architectural pattern adoption rather than a retry, timeout, isolation, or
    recovery mechanism.
  calculated_priority: P2
  override_applied: false
  override_priority: null
  override_reason: null
  override_approved_by: null
  override_approved_at: null
  additional_applicable_rules: [P2-DATA-005]
  p0_elevation_evaluated: >-
    Evaluated against the P2 elevation rule and against P0-AA-012 and not elevated. The authoritative
    Azure SQL record remains correct in both divergence directions, and the enumerated P0-AA-012
    conditions of duplicate execution, unsafe transaction retry, concurrency conflict, and replay do not
    describe this failure mode. The material impact is downstream event divergence, which does not by
    itself make the critical inventory transaction unsafe when both regions are active. Severity for
    F-002 is critical; priority is governed by the rule, not by severity.
implementation_wave: 4
complexity: high
implementation_status: proposed
implementation_allowed_in_planning_phase: false
objective: >-
  Give the Azure SQL write and the inventory-events publication a common commit point and a durable
  intent record that recovery can inspect.
existing_behavior:
  description: >-
    saveAndPublish performs repository.save and then producer.publish inside the same @Transactional
    service method, so the Kafka send is issued before the database transaction commits. delete removes
    the entity and publishes INVENTORY_DELETED in the same transaction. No transactional outbox table,
    @TransactionalEventListener, or AFTER_COMMIT hook exists anywhere in production source.
  evidence: [EV-F-002-01, EV-F-002-02]
proposed_behavior: >-
  The service writes an outbox record inside the business transaction instead of sending directly. A
  relay reads unpublished outbox records, publishes them through the durable producer from
  CHANGE-AA-018, and marks them published only after a confirmed delivery outcome. The outbox record
  carries a terminal status and an attempt count so recovery can detect and repair divergence.
what_this_solves: >-
  A rollback after a send can no longer leave downstream consumers holding state that was never
  committed, and a commit failure after an in-flight send is now represented by a durable intent record.
operating_scenario_impact: >-
  Provides the reconciliation marker that rebuilding downstream state after an active-standby promotion
  requires.
kafka_scenario_context:
  operating_scenario: active_standby
  scenario_preserved: true
  note: >-
    The outbox table lives in Azure SQL, which the approved architecture already declares as the
    authoritative business state. No new datastore is introduced. Broker transaction coordinator
    configuration remains outside the boundary.
affected_files:
  - source/inventory-service/src/main/java/com/ecommerce/inventory/service/impl/InventoryServiceImpl.java
new_files:
  - source/inventory-service/src/main/java/com/ecommerce/inventory/outbox/OutboxRecord.java
  - source/inventory-service/src/main/java/com/ecommerce/inventory/outbox/OutboxRepository.java
  - source/inventory-service/src/main/java/com/ecommerce/inventory/outbox/OutboxRelay.java
  - source/inventory-service/src/main/resources/db/migration/V3__outbox.sql
configuration_changes:
  - app.outbox.relay.enabled
  - app.outbox.relay.poll-interval
  - app.outbox.relay.batch-size
  - app.outbox.relay.max-attempts
dependency_changes: []
illustrative_code_blocks: [ICB-021-01, ICB-021-02, ICB-021-03, ICB-021-04]
proposed_tests: [PT-021-01, PT-021-02]
acceptance_criteria:
  - No production code path sends to Kafka inside an active business transaction.
  - An outbox record is written in the same transaction as the business state change it describes.
  - A rolled-back transaction leaves no outbox record and produces no published event.
  - The relay publishes each outbox record at least once and marks it published only after a confirmed delivery outcome.
  - An outbox record that exhausts its attempt budget reaches an explicit terminal status that is queryable and observable.
  - The relay is enabled or disabled by externalized configuration so its regional activation follows the same contract as CHANGE-AA-007.
validation_commands:
  - "mvn -f source/inventory-service/pom.xml -Dtest=OutboxCommitOrderingTest test"
  - "mvn -f source/inventory-service/pom.xml -Dtest=OutboxRelayIntegrationTest test"
  - "mvn -f source/inventory-service/pom.xml verify"
risks:
  - id: RISK-021-01
    description: The relay introduces at-least-once publication, so downstream consumers can now receive duplicates where they previously received at most one.
    mitigation: CHANGE-AA-022 supplies the stable event identity downstream consumers need to deduplicate. The two changes must be released together, which is why both sit in Wave 4.
  - id: RISK-021-02
    description: A relay running in more than one region publishes the same outbox record twice.
    mitigation: The relay enablement property follows the same externalized regional activation contract as the listener, and the activation state is observable.
  - id: RISK-021-03
    description: The outbox table grows without bound.
    mitigation: A retention and purge policy is required and is recorded as an unresolved input.
compatibility_considerations:
  - Publication moves from inside the transaction to after commit, so event timing changes and duplicate publication becomes possible.
  - Topic name, key, and payload shape are unchanged by this change.
rollback_considerations:
  - Reverting to direct publication is possible, but outbox records already written and not yet published would need to be drained or explicitly abandoned first.
depends_on_change_ids: [CHANGE-AA-002, CHANGE-AA-018]
blocks_change_ids: []
open_questions: [OQ-021, OQ-022]
targeted_implementation_discovery_required: false
change_boundary:
  classification: mixed
  existing_business_behavior_preserved: true
  security_and_privacy_behavior_preserved: true
  external_interaction_pattern_changed: true
  external_interaction_change_note: >-
    The number and timing of externally observable Kafka publications change. Publication moves to after
    commit and becomes at-least-once rather than at-most-once.
  approval_required: true
  approval:
    status: not_available
    decision_id: not_applicable
    approved_by: not_applicable
    approved_at: not_applicable
  implementation_allowed: false
  target_level_boundaries:
    - target: outbox_persistence_model
      classification: resiliency_mechanism
      approval_required: false
      implementation_allowed: true
      note: The outbox entity, repository, and migration script introduce no externally observable behaviour on their own.
    - target: publication_timing_and_delivery_semantics
      classification: partner_contract_change
      approval_required: true
      approval_status: not_available
      implementation_allowed: false
      note: >-
        Moving publication after commit and changing delivery semantics to at-least-once alters the
        externally observable interaction pattern for every consumer of inventory-events. Architecture and
        event-contract owner approval is required, and the approval must be coordinated with EG-011.
  unresolved_inputs:
    - Architecture approval for the transactional outbox pattern and the relay execution model
    - Approved at-least-once delivery semantics for inventory-events consumers
    - Approved outbox retention and purge policy
```

### CHANGE-AA-022: Give published events a stable identity and correlation context

```yaml
change_id: CHANGE-AA-022
title: Give published events a stable identity and correlation context
finding_ids: [F-007]
primary_finding_id: F-007
primary_control_id: APP-KAFKA-006
related_control_ids: [KAFKA-011, KAFKA-AS-006, APP-OBS-003]
category: event_contract
resiliency_related: true
finding_classification: resiliency
priority:
  value: P2
  policy_id: AA-REMEDIATION-PRIORITY
  policy_version: "1.0.0"
  rule_id: P2-DATA-007
  rationale: >-
    The published payload carries no message id, event id, schema version, producing region, or trace
    context, no RecordHeader is written, and occurredAt is regenerated on every call, so a republished
    event for the same business operation is not recognizable as the same event. Rule P2-DATA-007 applies
    because the messaging code lacks the identity that reliable duplicate detection and replay handling
    require. No P0 or P1 rule applies: this service's own idempotency is delivered by CHANGE-AA-008, and
    downstream deduplication implementations are outside the repository boundary.
  calculated_priority: P2
  override_applied: false
  override_priority: null
  override_reason: null
  override_approved_by: null
  override_approved_at: null
  additional_applicable_rules: [P2-DATA-005]
  p0_elevation_evaluated: >-
    Evaluated against the P2 elevation rule and not elevated. The absence of downstream event identity
    does not make this service's critical inventory transaction unsafe during concurrent regional
    operation; it limits downstream recovery options.
implementation_wave: 4
complexity: medium
implementation_status: proposed
implementation_allowed_in_planning_phase: false
objective: >-
  Make a republished event recognizable as the same business event, and make a consumed order event, its
  resulting SQL state change, and its published inventory event traceable to one another.
existing_behavior:
  description: >-
    The published payload contains type, occurredAt, referenceId, and the inventory response. No message
    id, event id, schema version, producing region, or trace context is present, and no RecordHeader is
    written. occurredAt is regenerated with Instant.now on every call.
  evidence: [EV-F-007-01]
proposed_behavior: >-
  The event envelope carries a deterministic event identifier derived from the same stable operation
  identity introduced by CHANGE-AA-008, an explicit schema version, the producing region from
  CHANGE-AA-005, and a correlation identifier propagated from the consumed order event. The same values
  are written as Kafka record headers. occurredAt is derived from the business state change rather than
  from the publication attempt.
what_this_solves: >-
  Replay after a promotion and republication from the outbox become safe for downstream consumers to
  deduplicate, and cross-boundary incident correlation becomes possible.
operating_scenario_impact: >-
  This is the downstream counterpart to CHANGE-AA-008. Without it, every replay-based recovery action
  propagates indistinguishable duplicates outward.
kafka_scenario_context:
  operating_scenario: active_standby
  scenario_preserved: true
  note: >-
    Schema registry subject governance is outside the boundary and is recorded as EG-011. The schema
    version introduced here is an envelope field, not a registry subject declaration.
affected_files:
  - source/inventory-service/src/main/java/com/ecommerce/inventory/kafka/producer/InventoryEventProducer.java
  - source/inventory-service/src/main/java/com/ecommerce/inventory/kafka/consumer/OrderEventConsumer.java
  - source/inventory-service/src/main/java/com/ecommerce/inventory/service/impl/InventoryServiceImpl.java
new_files:
  - source/inventory-service/src/main/java/com/ecommerce/inventory/kafka/producer/InventoryEventEnvelope.java
configuration_changes:
  - app.events.schema-version
dependency_changes: []
illustrative_code_blocks: [ICB-022-01, ICB-022-02]
proposed_tests: [PT-022-01]
acceptance_criteria:
  - Every published event carries a deterministic event identifier that is identical across republication of the same business operation.
  - Every published event carries an explicit schema version, the producing region, and a correlation identifier.
  - The same identity values are present as Kafka record headers and as envelope fields.
  - occurredAt reflects the business state change timestamp and does not change between republication attempts.
  - The correlation identifier from a consumed order event is present on the resulting published inventory event.
  - No customer, credential, payment, or secret value is added to the envelope or to any header.
validation_commands:
  - "mvn -f source/inventory-service/pom.xml -Dtest=InventoryEventEnvelopeTest test"
  - "mvn -f source/inventory-service/pom.xml verify"
risks:
  - id: RISK-022-01
    description: Adding envelope fields changes the published payload shape for every existing consumer.
    mitigation: The change is additive, but it remains an event-contract change and is therefore approval-gated and coordinated with EG-011.
  - id: RISK-022-02
    description: Downstream consumers may not deduplicate even when identity is supplied.
    mitigation: Downstream implementation is outside the repository boundary and is recorded as an implementation-boundary exclusion, not as a change target.
compatibility_considerations:
  - The payload gains fields; existing consumers that ignore unknown fields are unaffected, but that behaviour is not verifiable from this repository.
  - Record headers are added where none existed; consumers that do not read headers are unaffected.
rollback_considerations:
  - Reverting the envelope restores the previous payload shape. Consumers that began relying on the identity fields would lose them, so rollback requires downstream coordination.
depends_on_change_ids: [CHANGE-AA-005, CHANGE-AA-008, CHANGE-AA-018]
blocks_change_ids: []
open_questions: [OQ-023]
targeted_implementation_discovery_required: false
change_boundary:
  classification: partner_contract_change
  existing_business_behavior_preserved: true
  security_and_privacy_behavior_preserved: true
  external_interaction_pattern_changed: false
  approval_required: true
  approval:
    status: not_available
    decision_id: not_applicable
    approved_by: not_applicable
    approved_at: not_applicable
  implementation_allowed: false
  target_level_boundaries:
    - target: correlation_propagation_internal
      classification: resiliency_mechanism
      approval_required: false
      implementation_allowed: true
      note: >-
        Propagating a correlation identifier from the consumed event through the service to logs and
        metrics changes no external contract and may proceed independently.
    - target: published_event_envelope_contract
      classification: partner_contract_change
      approval_required: true
      approval_status: not_available
      implementation_allowed: false
      note: >-
        Adding identity, schema version, and region fields to inventory-events changes the published event
        contract. Event-contract owner approval is required and must be coordinated with EG-011.
  unresolved_inputs:
    - Approved event envelope contract and schema versioning scheme for inventory-events
    - Confirmation of whether a schema registry governs these subjects, carried from EG-011
```

### CHANGE-AA-023: Invalidate the cache on reserve and release

```yaml
change_id: CHANGE-AA-023
title: Invalidate the cache on reserve and release
finding_ids: [F-020]
primary_finding_id: F-020
primary_control_id: REDIS-015
related_control_ids: [APP-CACHE-003]
category: cache_correctness
resiliency_related: false
finding_classification: non_resiliency
non_resiliency_category: correctness
priority:
  value: P2
  policy_id: AA-REMEDIATION-PRIORITY
  policy_version: "1.0.0"
  rule_id: P2-DATA-010
  rationale: >-
    reserve and release locate the item by productId and change availableQuantity and reservedQuantity
    but carry no @CacheEvict, @CachePut, or explicit eviction, while the cached entry is keyed by the
    entity id. The read path therefore relies on a read-after-write consistency guarantee that the
    mutation paths do not establish. Rule P2-DATA-010 applies. No P0 or P1 rule applies: the defect
    occurs during entirely normal operation with no dependency failure, regional transition, or recovery
    event involved, which is also why Step 2 classified the finding non_resiliency. Severity for F-020 is
    critical; priority is governed by the rule, not by severity.
  calculated_priority: P2
  override_applied: false
  override_priority: null
  override_reason: null
  override_approved_by: null
  override_approved_at: null
  additional_applicable_rules: []
  p0_elevation_evaluated: >-
    Evaluated against the P2 elevation rule and not elevated. The authoritative Azure SQL record is
    re-read and the availability precondition re-evaluated inside every reserve transaction, so a stale
    cached read cannot cause an over-reservation against the authoritative record even when both regions
    are active.
  governance_note: >-
    The policy contains no rule that addresses a normal-operation data-correctness defect outside the
    active-active resiliency frame. P2-DATA-010 is the closest applicable rule and is cited. The coverage
    gap is recorded as OQ-024 and routed to policy governance.
implementation_wave: 4
complexity: low
implementation_status: proposed
implementation_allowed_in_planning_phase: false
objective: >-
  Make every path that changes inventory quantities invalidate the cached representation of that item.
existing_behavior:
  description: >-
    @CacheEvict is declared on update and delete, keyed by the entity id. reserve and release locate the
    item by productId and change availableQuantity and reservedQuantity, but carry no @CacheEvict,
    @CachePut, or explicit eviction.
  evidence: [EV-F-020-01, EV-F-020-02]
proposed_behavior: >-
  reserve and release evict the cached entry for the affected item using the entity id resolved inside
  the operation, and the eviction is ordered after the transaction commits so a rolled-back adjustment
  does not evict a still-valid entry.
what_this_solves: >-
  The read endpoint stops serving pre-adjustment quantities indefinitely after every reservation and
  release, including every reservation driven by order-events consumption.
operating_scenario_impact: >-
  None specific to the operating scenario. The defect and its remediation are region-agnostic.
kafka_scenario_context: null
affected_files:
  - source/inventory-service/src/main/java/com/ecommerce/inventory/service/impl/InventoryServiceImpl.java
new_files: []
configuration_changes: []
dependency_changes: []
illustrative_code_blocks: [ICB-023-01]
proposed_tests: [PT-023-01]
acceptance_criteria:
  - A reserve operation removes the cached entry for the affected item.
  - A release operation removes the cached entry for the affected item.
  - The eviction key resolves to the same key used by the @Cacheable read, so the id-keyed cache and the productId-keyed mutation path stay aligned.
  - A rolled-back reserve or release does not evict a valid cached entry.
  - A read immediately following a successful reserve returns the post-adjustment quantities.
validation_commands:
  - "mvn -f source/inventory-service/pom.xml -Dtest=CacheInvalidationOnAdjustmentTest test"
  - "mvn -f source/inventory-service/pom.xml verify"
risks:
  - id: RISK-023-01
    description: Post-commit eviction can fail while the transaction has already committed, leaving a stale entry.
    mitigation: The failure is absorbed and counted by the CacheErrorHandler from CHANGE-AA-014, and the TTL from CHANGE-AA-015 bounds how long the stale entry survives.
compatibility_considerations:
  - Callers begin observing correct post-adjustment quantities. This corrects a defect rather than changing intended behaviour, so no contract change is involved.
rollback_considerations:
  - Removing the eviction restores the previous stale-read behaviour with no data impact.
depends_on_change_ids: [CHANGE-AA-014, CHANGE-AA-015]
blocks_change_ids: []
open_questions: [OQ-024]
targeted_implementation_discovery_required: false
change_boundary:
  classification: supporting_configuration
  existing_business_behavior_preserved: true
  security_and_privacy_behavior_preserved: true
  external_interaction_pattern_changed: false
  approval_required: false
  approval:
    status: not_required
    decision_id: not_applicable
    approved_by: not_applicable
    approved_at: not_applicable
  implementation_allowed: true
  unresolved_inputs: []
```

### CHANGE-AA-024: Build the failure, failover, and probe-transition regression suite

```yaml
change_id: CHANGE-AA-024
title: Build the failure, failover, and probe-transition regression suite
finding_ids: [F-028]
primary_finding_id: F-028
primary_control_id: APP-AA-018
related_control_ids: [SQL-008, KAFKA-008, KAFKA-AS-009, REDIS-027, KV-008, GLB-008, APP-SUPPLY-001]
category: verification
resiliency_related: true
finding_classification: resiliency
priority:
  value: P0
  policy_id: AA-REMEDIATION-PRIORITY
  policy_version: "1.0.0"
  rule_id: P0-AA-013
  rationale: >-
    The test suite contains one happy-path unit test and one integration test whose only assertion is
    that the context loads. No test exercises duplicate delivery, replay, rebalance, broker
    unavailability, database failover, unknown commit outcome, optimistic-locking conflict, Redis
    unavailability, Key Vault denial, probe transitions, or graceful shutdown. Rule P0-AA-013 applies
    because the absence of these tests prevents the team from executing or interpreting active-active
    regional failure tests at all. The default rule tests_inherit_behavior_priority also applies: the
    behaviours left unverified include every P0 change in this plan.
  calculated_priority: P0
  override_applied: false
  override_priority: null
  override_reason: null
  override_approved_by: null
  override_approved_at: null
  additional_applicable_rules: [P0-AA-005]
  p0_elevation_evaluated: not_applicable
implementation_wave: 4
wave_rationale: >-
  The change is P0 but sits in Wave 4 because the consolidated suite depends on the behaviour every other
  change introduces. Wave ordering here is a dependency statement, not a priority statement. Each
  individual change carries its own proposed tests in its own wave, so P0 behaviours are verified as they
  land rather than only at the end.
complexity: high
implementation_status: proposed
implementation_allowed_in_planning_phase: false
objective: >-
  Prove that the failure behaviour the approved target deployment depends on actually holds, and protect
  it from regression when the Spring Boot parent or the Spring Cloud Azure BOM changes.
existing_behavior:
  description: >-
    The test suite contains one Mockito unit test covering the happy-path reserve flow and one
    @SpringBootTest with Testcontainers MSSQL and @EmbeddedKafka whose only assertion is that the
    application context loads. create, get, list, update, delete, release, OrderEventConsumer,
    InventoryEventProducer, and GlobalExceptionHandler have no test coverage at all.
  evidence: [EV-F-028-01, EV-F-028-02]
proposed_behavior: >-
  A fault-injection and failover suite built on the existing Testcontainers, @EmbeddedKafka, and Spring
  Boot Test model covers duplicate delivery, replay from an earlier offset, rebalance, broker
  unavailability, database connection loss, optimistic-locking conflict, Redis unavailability, Key Vault
  denial, probe transitions, graceful shutdown, and regional activation and deactivation. A dependency
  regression test asserts the resilience-relevant effective configuration so a managed version bump
  cannot silently change timeout, retry, offset, or health semantics.
what_this_solves: >-
  Remediation of every other finding becomes demonstrable, and future changes are protected from
  regression.
operating_scenario_impact: >-
  Provides the promotion, stale-active fencing, offset restoration, duplicate replay, and failback
  coverage that KAFKA-AS-009 requires.
kafka_scenario_context:
  operating_scenario: active_standby
  scenario_preserved: true
  note: >-
    Tests exercise application behaviour under the active-standby scenario. Live regional failover
    exercises and platform chaos tooling remain outside the boundary.
affected_files:
  - source/inventory-service/src/test/java/com/ecommerce/inventory/InventoryIntegrationTest.java
new_files:
  - source/inventory-service/src/test/java/com/ecommerce/inventory/resiliency/DatabaseFailoverIntegrationTest.java
  - source/inventory-service/src/test/java/com/ecommerce/inventory/resiliency/KafkaFailureIntegrationTest.java
  - source/inventory-service/src/test/java/com/ecommerce/inventory/resiliency/RedisFailureIntegrationTest.java
  - source/inventory-service/src/test/java/com/ecommerce/inventory/resiliency/ProbeTransitionIntegrationTest.java
  - source/inventory-service/src/test/java/com/ecommerce/inventory/resiliency/RegionalActivationIntegrationTest.java
  - source/inventory-service/src/test/java/com/ecommerce/inventory/resiliency/EffectiveResiliencyConfigurationTest.java
configuration_changes: []
dependency_changes:
  - org.testcontainers:testcontainers (Redis module or generic container for Redis fault injection)
illustrative_code_blocks: [ICB-024-01, ICB-024-02, ICB-024-03]
proposed_tests: [PT-024-01, PT-024-02, PT-024-03]
acceptance_criteria:
  - Duplicate delivery of the same order event produces exactly one stock movement.
  - Replay from offset zero against a populated database produces no additional stock movement.
  - Database connection loss produces a bounded failure and a readiness transition to OUT_OF_SERVICE, and readiness recovers without a restart.
  - Redis unavailability produces a successful read served from the authoritative store.
  - Broker unavailability produces an observed publication failure rather than a silent drop.
  - A poison record is quarantined on the dead-letter destination and the offset advances only afterward.
  - An optimistic-locking conflict is absorbed by reload-and-reapply.
  - Readiness reports OUT_OF_SERVICE before the servlet container stops during shutdown.
  - Setting the consumer activation property to false prevents consumption while readiness stays UP.
  - The effective resiliency configuration test fails when a managed version bump changes a timeout, retry, offset, or health default that this plan relies on.
  - The suite executes in CI without requiring a live Azure dependency.
validation_commands:
  - "mvn -f source/inventory-service/pom.xml -Dtest='com.ecommerce.inventory.resiliency.*' test"
  - "mvn -f source/inventory-service/pom.xml verify"
risks:
  - id: RISK-024-01
    description: Container-based fault injection lengthens the build and can be flaky.
    mitigation: The suite reuses the existing Testcontainers disabledWithoutDocker guard and the existing @EmbeddedKafka model, and fault-injection tests are grouped so they can be run as a separate execution.
  - id: RISK-024-02
    description: Testcontainers coverage for Azure Managed Redis and Key Vault is approximate.
    mitigation: Redis behaviour is exercised against a generic Redis container and Key Vault behaviour is exercised through property-source substitution; the approximation is recorded as an unresolved input.
compatibility_considerations:
  - Test-only change. No production source, configuration, or contract is affected.
rollback_considerations:
  - Tests can be removed without production impact, but doing so reopens F-028.
depends_on_change_ids:
  - CHANGE-AA-001
  - CHANGE-AA-002
  - CHANGE-AA-003
  - CHANGE-AA-004
  - CHANGE-AA-005
  - CHANGE-AA-006
  - CHANGE-AA-007
  - CHANGE-AA-008
  - CHANGE-AA-009
  - CHANGE-AA-010
  - CHANGE-AA-011
  - CHANGE-AA-013
  - CHANGE-AA-014
  - CHANGE-AA-015
  - CHANGE-AA-016
  - CHANGE-AA-018
  - CHANGE-AA-019
  - CHANGE-AA-020
blocks_change_ids: []
open_questions: [OQ-025]
targeted_implementation_discovery_required: false
library_resolution:
  capability: integration_testing
  approved_library: testcontainers
  approval_source: approved_libraries_governance
  approval_status: approved
  repository_availability: available
  version_source: repository_declared
  dependency_change_required: false
  note: >-
    testcontainers.version 1.20.3 is declared as a repository property and junit-jupiter and mssqlserver
    modules are already present. A Redis container requires either the generic container API already on
    the classpath or an additional module.
  unresolved_inputs: []
change_boundary:
  classification: test_only
  existing_business_behavior_preserved: true
  security_and_privacy_behavior_preserved: true
  external_interaction_pattern_changed: false
  approval_required: false
  approval:
    status: not_required
    decision_id: not_applicable
    approved_by: not_applicable
    approved_at: not_applicable
  implementation_allowed: true
  unresolved_inputs:
    - Whether the CI environment provides a Docker daemon for the fault-injection suite
```

## 5. Illustrative Code Proposals

Illustrative proposal only. None of the blocks below is an applied patch. Original source excerpts are reproduced verbatim from Step 2 and are never regenerated or normalized. Target location, original source, and proposed implementation are kept separate. Line numbers are advisory and are not authoritative.

### ICB-001-01: Readiness and liveness group membership

```yaml
change_id: CHANGE-AA-001
block_id: ICB-001-01
target:
  repository_path: source/inventory-service/src/main/resources/application.yml
  symbol: management.endpoint.health
  assessment_snapshot:
    type: workspace_snapshot
    identifier: "inventory-service-workspace-2026-09-18"
    provenance: workspace_generated
    git_commit_sha: not_applicable
    limitations: []
  source_fingerprint:
    algorithm: sha256
    value: "653a483edc8b2f53255c32fb9a607d3d9e8a7e5f543531165e9ff2230b5471f6"
  original_line_range: {start_line: 29, end_line: 37, status: advisory}
  line_numbers_authoritative: false
current_implementation:
  evidence_id: EV-F-008-01
  original_source_excerpt: |
    management:
      endpoints:
        web:
          exposure:
            include: health,info,prometheus
      endpoint:
        health:
          probes:
            enabled: true
proposed_implementation:
  illustrative_code_status: generated
  source_language: yaml
  target_repository_path: source/inventory-service/src/main/resources/application.yml
  target_symbol: management.endpoint.health
  replaces_or_updates_evidence_ids: [EV-F-008-01]
  illustrative_code: |
    management:
      endpoints:
        web:
          exposure:
            include: health,info,prometheus
      endpoint:
        health:
          probes:
            enabled: true
          show-details: never
          group:
            readiness:
              include: readinessState,db
              show-details: never
              additional-path: never
            liveness:
              include: livenessState
      health:
        redis:
          enabled: true
        defaults:
          enabled: true
  narrative_explanation: >-
    The readiness group is declared explicitly so the Azure SQL contributor participates in traffic
    eligibility. Redis stays out of readiness because it is a non-authoritative cache with a degraded
    path from CHANGE-AA-014. Kafka stays out until CHANGE-AA-007 supplies the role contract. Liveness is
    pinned to livenessState so external dependency loss cannot cause restart loops. Contributors remain
    enabled so the aggregate endpoint still reports them.
  discovery_required_reason: null
  unresolved_inputs: []
```

### ICB-001-02: Readiness transition observability

```yaml
change_id: CHANGE-AA-001
block_id: ICB-001-02
target:
  repository_path: source/inventory-service/src/main/java/com/ecommerce/inventory/health/ReadinessTransitionListener.java
  symbol: ReadinessTransitionListener
  target_status: new_file
current_implementation:
  evidence_id: EV-F-008-02
  original_source_excerpt: not_available
  evidence_note: >-
    Step 2 recorded this as absence evidence with no excerpt available. The absence of any
    HealthIndicator, AvailabilityChangeEvent, or ReadinessState usage in production source is the
    assessed condition.
proposed_implementation:
  illustrative_code_status: generated
  source_language: java
  target_repository_path: source/inventory-service/src/main/java/com/ecommerce/inventory/health/ReadinessTransitionListener.java
  target_symbol: ReadinessTransitionListener
  replaces_or_updates_evidence_ids: [EV-F-008-02]
  illustrative_code: |
    package com.ecommerce.inventory.health;

    import io.micrometer.core.instrument.MeterRegistry;
    import lombok.RequiredArgsConstructor;
    import lombok.extern.slf4j.Slf4j;
    import org.springframework.boot.availability.AvailabilityChangeEvent;
    import org.springframework.boot.availability.ReadinessState;
    import org.springframework.context.event.EventListener;
    import org.springframework.stereotype.Component;

    @Slf4j
    @Component
    @RequiredArgsConstructor
    public class ReadinessTransitionListener {

        private final MeterRegistry meterRegistry;

        @EventListener
        public void onReadinessChange(AvailabilityChangeEvent<ReadinessState> event) {
            ReadinessState state = event.getState();
            meterRegistry.counter("inventory.readiness.transition", "state", state.name()).increment();
            log.info("readiness state changed state={}", state);
        }
    }
  narrative_explanation: >-
    Every readiness transition produces exactly one counter increment and one structured log record. The
    region and role dimensions are supplied automatically by the Micrometer common tags introduced in
    CHANGE-AA-005, so they are not repeated here.
  discovery_required_reason: null
  unresolved_inputs: []
```

### ICB-002-01: Remove runtime DDL from the startup path

```yaml
change_id: CHANGE-AA-002
block_id: ICB-002-01
target:
  repository_path: source/inventory-service/src/main/resources/application.yml
  symbol: spring.jpa.hibernate.ddl-auto
  source_fingerprint:
    algorithm: sha256
    value: "26b82c5e056df6c3871feb9337d2e99258ee6736739300bfdc11cb4eb6c5cdb2"
  original_line_range: {start_line: 10, end_line: 12, status: advisory}
  line_numbers_authoritative: false
current_implementation:
  evidence_id: EV-F-024-01
  original_source_excerpt: |
      jpa:
        hibernate:
          ddl-auto: update
proposed_implementation:
  illustrative_code_status: generated
  source_language: yaml
  target_repository_path: source/inventory-service/src/main/resources/application.yml
  target_symbol: spring.jpa
  replaces_or_updates_evidence_ids: [EV-F-024-01]
  illustrative_code: |
      jpa:
        hibernate:
          ddl-auto: ${JPA_DDL_AUTO:validate}
        open-in-view: false
  narrative_explanation: >-
    Startup validates the deployed schema instead of mutating it, so a pod starting against a read-only
    geo-secondary or a database mid-promotion no longer attempts DDL. The value stays overridable so a
    local development profile can select a different mode without a code change. open-in-view is disabled
    so a database session is not held for the duration of view rendering, which keeps the connection
    budget from CHANGE-AA-009 meaningful.
  discovery_required_reason: null
  unresolved_inputs: []
```

### ICB-002-02: Baseline versioned migration script

```yaml
change_id: CHANGE-AA-002
block_id: ICB-002-02
target:
  repository_path: source/inventory-service/src/main/resources/db/migration/V1__baseline_inventory_items.sql
  symbol: baseline schema for inventory_items
  target_status: new_file
current_implementation:
  evidence_id: EV-F-024-01
  original_source_excerpt: |
      jpa:
        hibernate:
          ddl-auto: update
  evidence_note: >-
    The schema currently has no repository-owned definition at all; it is produced implicitly by the
    ddl-auto update setting shown above.
proposed_implementation:
  illustrative_code_status: generated
  source_language: sql
  target_repository_path: source/inventory-service/src/main/resources/db/migration/V1__baseline_inventory_items.sql
  target_symbol: inventory_items
  replaces_or_updates_evidence_ids: [EV-F-024-01]
  illustrative_code: |
    CREATE TABLE inventory_items (
        id                 BIGINT IDENTITY(1,1) NOT NULL,
        productId          VARCHAR(255)         NULL,
        availableQuantity  INT                  NOT NULL,
        reservedQuantity   INT                  NOT NULL,
        updatedAt          DATETIME2            NULL,
        version            BIGINT               NOT NULL,
        CONSTRAINT PK_inventory_items PRIMARY KEY (id),
        CONSTRAINT UQ_inventory_items_productId UNIQUE (productId)
    );
  narrative_explanation: >-
    The baseline reproduces the current InventoryItem mapping exactly: the identity primary key, the
    unique constraint on productId declared on the @Table annotation, the two quantity columns, the
    updatedAt instant, and the @Version column. No column is added, removed, widened, or renamed, so
    switching ddl-auto to validate does not change the schema contract.
  discovery_required_reason: null
  unresolved_inputs:
    - Exact column types and nullability produced by the current implicit schema in each deployed environment, which must be compared before cutover
```

### ICB-002-03: Versioned migration runner dependency

```yaml
change_id: CHANGE-AA-002
block_id: ICB-002-03
target:
  repository_path: source/inventory-service/pom.xml
  symbol: project/dependencies migration runner
  source_fingerprint:
    algorithm: sha256
    value: "d1af2cf103de040ee5932ef455e58ec46fd6409bfba9ea02838287f980a47ecd"
  original_line_range: {start_line: 7, end_line: 26, status: advisory}
  line_numbers_authoritative: false
current_implementation:
  evidence_id: EV-F-012-01
  evidence_note: >-
    The dependency list assessed in Step 2 contains no schema-migration library. The excerpt is preserved
    verbatim in ICB-010-01 and is not duplicated here.
proposed_implementation:
  illustrative_code_status: targeted_discovery_required
  source_language: xml
  target_repository_path: source/inventory-service/pom.xml
  target_symbol: project/dependencies
  replaces_or_updates_evidence_ids: [EV-F-012-01]
  illustrative_code: null
  narrative_explanation: >-
    A versioned migration runner must apply the scripts in db/migration and record the applied version,
    either outside the ordinary application startup path or behind an explicit, bounded, role-aware
    startup gate.
  discovery_required_reason: >-
    grounding/governance/approved-libraries.yml declares approved libraries for resiliency,
    observability, and testing only. It declares no approved schema-migration library, and no repository
    evidence establishes an organizational choice between Flyway, Liquibase, and an externally executed
    migration process. Selecting one would be an unapproved product decision.
  unresolved_inputs:
    - Approved schema-migration library or externally governed migration process
    - Whether migrations execute inside the application startup path or as a separate release step
```

### ICB-003-01: Bounded Key Vault client budget

```yaml
change_id: CHANGE-AA-003
block_id: ICB-003-01
target:
  repository_path: source/inventory-service/src/main/resources/application-prod.yml
  symbol: spring.config.import
  source_fingerprint:
    algorithm: sha256
    value: "e7c1e56e4046bbfc9fcf5c3a01e365fb206b1f607e3db7809765093a706a1915"
  original_line_range: {start_line: 1, end_line: 3, status: advisory}
  line_numbers_authoritative: false
current_implementation:
  evidence_id: EV-F-022-01
  original_source_excerpt: |
    spring:
      config:
        import: azure-keyvault:${AZURE_KEYVAULT_ENDPOINT}
proposed_implementation:
  illustrative_code_status: generated
  source_language: yaml
  target_repository_path: source/inventory-service/src/main/resources/application-prod.yml
  target_symbol: spring.config.import and spring.cloud.azure.keyvault.secret
  replaces_or_updates_evidence_ids: [EV-F-022-01]
  illustrative_code: |
    spring:
      config:
        # Mandatory by design: datasource and cache credentials cannot be resolved without it.
        import: azure-keyvault:${AZURE_KEYVAULT_ENDPOINT}
      cloud:
        azure:
          keyvault:
            secret:
              client:
                connect-timeout: ${KEYVAULT_CONNECT_TIMEOUT}
                response-timeout: ${KEYVAULT_RESPONSE_TIMEOUT}
              retry:
                mode: exponential
                exponential:
                  max-retries: ${KEYVAULT_MAX_RETRIES}
                  base-delay: ${KEYVAULT_RETRY_BASE_DELAY}
                  max-delay: ${KEYVAULT_RETRY_MAX_DELAY}
  narrative_explanation: >-
    The import stays mandatory because the credentials genuinely are required, but the wait is now
    bounded and tunable. Every budget resolves from a deployment-supplied placeholder, so no approved
    numeric value is asserted by this plan and the values can be aligned to the regional recovery budget.
    The comment states the startup contract explicitly in the file where it is enforced.
  discovery_required_reason: null
  unresolved_inputs:
    - Approved connect, response, and retry budget values for the regional recovery scenario
```

### ICB-004-01: Enable graceful shutdown

```yaml
change_id: CHANGE-AA-004
block_id: ICB-004-01
target:
  repository_path: source/inventory-service/src/main/resources/application.yml
  symbol: server and spring.lifecycle
  source_fingerprint:
    algorithm: sha256
    value: "f52a6730d9cb9c1627c17420ab6e361f886ffc4be09fcb5253ead6f9e83034ea"
  original_line_range: {start_line: 1, end_line: 12, status: advisory}
  line_numbers_authoritative: false
current_implementation:
  evidence_id: EV-F-021-01
  original_source_excerpt: |
    spring:
      config:
        import: azure-keyvault:${AZURE_KEYVAULT_ENDPOINT}
      datasource:
        url: ${SQL_CONNECTION_STRING}
      data:
        redis:
          url: ${REDIS_CONNECTION_STRING}
      kafka:
        bootstrap-servers: ${KAFKA_BOOTSTRAP_SERVERS}
        properties:
          security.protocol: ${KAFKA_SECURITY_PROTOCOL:PLAINTEXT}
  evidence_note: >-
    The excerpt is the complete assessed prod profile and demonstrates the absence of any shutdown or
    lifecycle property. The proposed properties are placed in the default profile so both profiles
    inherit them.
proposed_implementation:
  illustrative_code_status: generated
  source_language: yaml
  target_repository_path: source/inventory-service/src/main/resources/application.yml
  target_symbol: server.shutdown and spring.lifecycle.timeout-per-shutdown-phase
  replaces_or_updates_evidence_ids: [EV-F-021-01]
  illustrative_code: |
    server:
      port: 8082
      shutdown: graceful
    spring:
      lifecycle:
        timeout-per-shutdown-phase: ${SHUTDOWN_PHASE_TIMEOUT}
    app:
      lifecycle:
        readiness-withdrawal-delay: ${READINESS_WITHDRAWAL_DELAY}
  narrative_explanation: >-
    Graceful shutdown lets the servlet container drain in-flight requests. The per-phase timeout and the
    readiness withdrawal delay are externalized so the total application drain window can be kept shorter
    than the platform termination grace period, which lives outside the remediation boundary.
  discovery_required_reason: null
  unresolved_inputs:
    - Platform termination grace period, required to bound the drain window
```

### ICB-004-02: Ordered shutdown coordinator

```yaml
change_id: CHANGE-AA-004
block_id: ICB-004-02
target:
  repository_path: source/inventory-service/src/main/java/com/ecommerce/inventory/lifecycle/GracefulShutdownCoordinator.java
  symbol: GracefulShutdownCoordinator
  target_status: new_file
current_implementation:
  evidence_id: EV-F-021-01
  evidence_note: >-
    No production class implements SmartLifecycle, DisposableBean, or @PreDestroy, and no code withdraws
    readiness before termination.
proposed_implementation:
  illustrative_code_status: generated
  source_language: java
  target_repository_path: source/inventory-service/src/main/java/com/ecommerce/inventory/lifecycle/GracefulShutdownCoordinator.java
  target_symbol: GracefulShutdownCoordinator
  replaces_or_updates_evidence_ids: [EV-F-021-01]
  illustrative_code: |
    package com.ecommerce.inventory.lifecycle;

    import lombok.extern.slf4j.Slf4j;
    import org.springframework.boot.availability.AvailabilityChangeEvent;
    import org.springframework.boot.availability.ReadinessState;
    import org.springframework.context.ApplicationEventPublisher;
    import org.springframework.context.SmartLifecycle;
    import org.springframework.kafka.config.KafkaListenerEndpointRegistry;
    import org.springframework.beans.factory.annotation.Value;
    import org.springframework.stereotype.Component;

    import java.time.Duration;

    @Slf4j
    @Component
    public class GracefulShutdownCoordinator implements SmartLifecycle {

        private final ApplicationEventPublisher publisher;
        private final KafkaListenerEndpointRegistry listenerRegistry;
        private final Duration readinessWithdrawalDelay;
        private volatile boolean running;

        public GracefulShutdownCoordinator(ApplicationEventPublisher publisher,
                                           KafkaListenerEndpointRegistry listenerRegistry,
                                           @Value("${app.lifecycle.readiness-withdrawal-delay}") Duration readinessWithdrawalDelay) {
            this.publisher = publisher;
            this.listenerRegistry = listenerRegistry;
            this.readinessWithdrawalDelay = readinessWithdrawalDelay;
        }

        @Override
        public int getPhase() {
            // Runs before the web server and the listener containers stop.
            return Integer.MIN_VALUE;
        }

        @Override
        public void start() {
            this.running = true;
        }

        @Override
        public void stop() {
            long startedAt = System.nanoTime();
            AvailabilityChangeEvent.publish(publisher, this, ReadinessState.REFUSING_TRAFFIC);
            log.info("shutdown phase=readiness_withdrawn delayMs={}", readinessWithdrawalDelay.toMillis());
            sleepQuietly(readinessWithdrawalDelay);

            listenerRegistry.getListenerContainers().forEach(container -> {
                container.stop();
                log.info("shutdown phase=listener_stopped listenerId={}", container.getListenerId());
            });

            this.running = false;
            log.info("shutdown phase=intake_stopped durationMs={}", (System.nanoTime() - startedAt) / 1_000_000);
        }

        @Override
        public boolean isRunning() {
            return running;
        }

        private void sleepQuietly(Duration duration) {
            try {
                Thread.sleep(duration.toMillis());
            } catch (InterruptedException interrupted) {
                Thread.currentThread().interrupt();
            }
        }
    }
  narrative_explanation: >-
    The coordinator runs at the earliest shutdown phase, so it executes before the web server and the
    Kafka listener containers are stopped by the ordinary lifecycle. It publishes REFUSING_TRAFFIC so the
    readiness probe reports OUT_OF_SERVICE, waits the configured withdrawal delay to let the load
    balancer notice, then stops every listener container so no new records are polled. The graceful web
    shutdown enabled in ICB-004-01 then drains in-flight HTTP requests.
  discovery_required_reason: null
  unresolved_inputs: []
```

### ICB-005-01: Deployment identity properties

```yaml
change_id: CHANGE-AA-005
block_id: ICB-005-01
target:
  repository_path: source/inventory-service/src/main/resources/application.yml
  symbol: management.metrics.tags and app.deployment
  source_fingerprint:
    algorithm: sha256
    value: "653a483edc8b2f53255c32fb9a607d3d9e8a7e5f543531165e9ff2230b5471f6"
  original_line_range: {start_line: 29, end_line: 37, status: advisory}
  line_numbers_authoritative: false
current_implementation:
  evidence_id: EV-F-026-01
  original_source_excerpt: |
    management:
      endpoints:
        web:
          exposure:
            include: health,info,prometheus
      endpoint:
        health:
          probes:
            enabled: true
  evidence_note: >-
    The excerpt is the complete assessed management block and demonstrates the absence of any common
    metric tag.
proposed_implementation:
  illustrative_code_status: generated
  source_language: yaml
  target_repository_path: source/inventory-service/src/main/resources/application.yml
  target_symbol: management.metrics.tags and app.deployment
  replaces_or_updates_evidence_ids: [EV-F-026-01]
  illustrative_code: |
    app:
      deployment:
        region: ${APP_DEPLOYMENT_REGION:unknown}
        role: ${APP_DEPLOYMENT_ROLE:unknown}
    management:
      metrics:
        tags:
          region: ${app.deployment.region}
          role: ${app.deployment.role}
  narrative_explanation: >-
    Both values are supplied entirely by deployment-time environment variables. No region name and no
    regional endpoint appears in the repository. The explicit unknown default makes an unset value
    visible in telemetry rather than silently absent.
  discovery_required_reason: null
  unresolved_inputs: []
```

### ICB-005-02: Deployment identity binding

```yaml
change_id: CHANGE-AA-005
block_id: ICB-005-02
target:
  repository_path: source/inventory-service/src/main/java/com/ecommerce/inventory/config/DeploymentIdentityProperties.java
  symbol: DeploymentIdentityProperties
  target_status: new_file
current_implementation:
  evidence_id: EV-F-026-01
  evidence_note: No @ConfigurationProperties binding class exists in production source.
proposed_implementation:
  illustrative_code_status: generated
  source_language: java
  target_repository_path: source/inventory-service/src/main/java/com/ecommerce/inventory/config/DeploymentIdentityProperties.java
  target_symbol: DeploymentIdentityProperties
  replaces_or_updates_evidence_ids: [EV-F-026-01]
  illustrative_code: |
    package com.ecommerce.inventory.config;

    import org.springframework.boot.context.properties.ConfigurationProperties;
    import org.springframework.boot.context.properties.EnableConfigurationProperties;
    import org.springframework.context.annotation.Configuration;

    @Configuration
    @EnableConfigurationProperties(DeploymentIdentityProperties.class)
    @ConfigurationProperties(prefix = "app.deployment")
    public class DeploymentIdentityProperties {

        private String region = "unknown";
        private String role = "unknown";

        public String getRegion() {
            return region;
        }

        public void setRegion(String region) {
            this.region = region;
        }

        public String getRole() {
            return role;
        }

        public void setRole(String role) {
            this.role = role;
        }
    }
  narrative_explanation: >-
    A typed binding makes the region and role available to the logback configuration and to any component
    that needs to tag a record. The repository has no existing @ConfigurationProperties class, so this
    establishes the pattern the later changes reuse.
  discovery_required_reason: null
  unresolved_inputs: []
```

### ICB-005-03: Region fields on structured log records

```yaml
change_id: CHANGE-AA-005
block_id: ICB-005-03
target:
  repository_path: source/inventory-service/src/main/resources/logback-spring.xml
  symbol: LogstashEncoder console appender
  source_fingerprint:
    algorithm: sha256
    value: "fa4169b08e5c5d67b946d965d6650ba77a0d20b70ba489846c279543a8c290ae"
  original_line_range: {start_line: 1, end_line: 1, status: advisory}
  line_numbers_authoritative: false
current_implementation:
  evidence_id: EV-F-026-02
  original_source_excerpt: |
    <configuration><appender name="CONSOLE" class="ch.qos.logback.core.ConsoleAppender"><encoder class="net.logstash.logback.encoder.LogstashEncoder"/></appender><root level="INFO"><appender-ref ref="CONSOLE"/></root></configuration>
proposed_implementation:
  illustrative_code_status: generated
  source_language: xml
  target_repository_path: source/inventory-service/src/main/resources/logback-spring.xml
  target_symbol: LogstashEncoder customFields
  replaces_or_updates_evidence_ids: [EV-F-026-02]
  illustrative_code: |
    <configuration>
        <springProperty scope="context" name="deploymentRegion" source="app.deployment.region" defaultValue="unknown"/>
        <springProperty scope="context" name="deploymentRole" source="app.deployment.role" defaultValue="unknown"/>
        <springProperty scope="context" name="applicationName" source="spring.application.name" defaultValue="inventory-service"/>
        <appender name="CONSOLE" class="ch.qos.logback.core.ConsoleAppender">
            <encoder class="net.logstash.logback.encoder.LogstashEncoder">
                <customFields>{"application":"${applicationName}","region":"${deploymentRegion}","role":"${deploymentRole}"}</customFields>
            </encoder>
        </appender>
        <root level="INFO">
            <appender-ref ref="CONSOLE"/>
        </root>
    </configuration>
  narrative_explanation: >-
    springProperty reads the same externalized values the metrics tags use, so metrics and logs carry the
    identical region and role dimension. The encoder, appender, and root level are otherwise unchanged,
    so existing log parsers continue to work.
  discovery_required_reason: null
  unresolved_inputs: []
```

### ICB-006-01: Business and failure telemetry component

```yaml
change_id: CHANGE-AA-006
block_id: ICB-006-01
target:
  repository_path: source/inventory-service/src/main/java/com/ecommerce/inventory/observability/InventoryTelemetry.java
  symbol: InventoryTelemetry
  target_status: new_file
current_implementation:
  evidence_id: EV-F-027-01
  original_source_excerpt: |
        public void publish(String type, InventoryResponse inventory, String referenceId) {
            kafkaTemplate.send("inventory-events", inventory.productId(), Map.of("type", type, "occurredAt", Instant.now().toString(), "referenceId", referenceId == null ? "" : referenceId, "inventory", inventory));
        }
  evidence_note: >-
    The producer discards its send result entirely and logs nothing on failure. No custom metric exists
    anywhere in production source.
proposed_implementation:
  illustrative_code_status: generated
  source_language: java
  target_repository_path: source/inventory-service/src/main/java/com/ecommerce/inventory/observability/InventoryTelemetry.java
  target_symbol: InventoryTelemetry
  replaces_or_updates_evidence_ids: [EV-F-027-01]
  illustrative_code: |
    package com.ecommerce.inventory.observability;

    import io.micrometer.core.instrument.MeterRegistry;
    import io.micrometer.core.instrument.Gauge;
    import org.springframework.stereotype.Component;

    import java.time.Instant;
    import java.util.concurrent.atomic.AtomicReference;

    @Component
    public class InventoryTelemetry {

        public static final String OUTCOME_SUCCESS = "success";
        public static final String OUTCOME_FAILURE = "failure";
        public static final String OUTCOME_DUPLICATE = "duplicate";
        public static final String OUTCOME_QUARANTINED = "quarantined";
        public static final String CACHE_MISS = "miss";
        public static final String CACHE_FAILURE = "failure";

        private final MeterRegistry meterRegistry;
        private final AtomicReference<Instant> lastConsumeSuccess = new AtomicReference<>(Instant.EPOCH);

        public InventoryTelemetry(MeterRegistry meterRegistry) {
            this.meterRegistry = meterRegistry;
            Gauge.builder("inventory.consume.last_success.age.seconds", lastConsumeSuccess,
                            reference -> secondsSince(reference.get()))
                    .description("Seconds since the last successfully applied order event")
                    .register(meterRegistry);
        }

        public void recordPublication(String eventType, String outcome) {
            meterRegistry.counter("inventory.publish.outcome", "eventType", eventType, "outcome", outcome).increment();
        }

        public void recordConsumption(String eventType, String outcome) {
            meterRegistry.counter("inventory.consume.outcome", "eventType", eventType, "outcome", outcome).increment();
            if (OUTCOME_SUCCESS.equals(outcome)) {
                lastConsumeSuccess.set(Instant.now());
            }
        }

        public void recordCacheOutcome(String cacheName, String outcome) {
            meterRegistry.counter("inventory.cache.outcome", "cache", cacheName, "outcome", outcome).increment();
        }

        private static double secondsSince(Instant instant) {
            return Instant.EPOCH.equals(instant)
                    ? -1d
                    : (System.currentTimeMillis() - instant.toEpochMilli()) / 1000d;
        }
    }
  narrative_explanation: >-
    One component owns every business and failure meter so the names and dimensions stay consistent. The
    region and role tags come from the Micrometer common tags in CHANGE-AA-005 and are not repeated on
    each meter. The last-success gauge is registered at construction so it is present even before any
    record is processed, and it reports a negative sentinel until the first success, which lets an
    operator tell a never-started consumer from a stalled one. No meter name or tag carries payload
    content.
  discovery_required_reason: null
  unresolved_inputs: []
```

### ICB-006-02: Application logging level contract

```yaml
change_id: CHANGE-AA-006
block_id: ICB-006-02
target:
  repository_path: source/inventory-service/src/main/resources/logback-spring.xml
  symbol: root logger and appender configuration
  source_fingerprint:
    algorithm: sha256
    value: "fa4169b08e5c5d67b946d965d6650ba77a0d20b70ba489846c279543a8c290ae"
  original_line_range: {start_line: 1, end_line: 1, status: advisory}
  line_numbers_authoritative: false
current_implementation:
  evidence_id: EV-F-027-02
  original_source_excerpt: |
    <configuration><appender name="CONSOLE" class="ch.qos.logback.core.ConsoleAppender"><encoder class="net.logstash.logback.encoder.LogstashEncoder"/></appender><root level="INFO"><appender-ref ref="CONSOLE"/></root></configuration>
proposed_implementation:
  illustrative_code_status: generated
  source_language: xml
  target_repository_path: source/inventory-service/src/main/resources/logback-spring.xml
  target_symbol: application logger declaration
  replaces_or_updates_evidence_ids: [EV-F-027-02]
  illustrative_code: |
    <logger name="com.ecommerce.inventory" level="${APP_LOG_LEVEL:-INFO}" additivity="false">
        <appender-ref ref="CONSOLE"/>
    </logger>
  narrative_explanation: >-
    An explicit application logger makes the failure and outcome records emitted by the other changes
    independently tunable from framework logging, so log volume can be reduced during an incident without
    losing framework diagnostics. The element is added inside the configuration produced by ICB-005-03.
  discovery_required_reason: null
  unresolved_inputs: []
```

### ICB-007-01: Listener identity and externalized activation

```yaml
change_id: CHANGE-AA-007
block_id: ICB-007-01
target:
  repository_path: source/inventory-service/src/main/java/com/ecommerce/inventory/kafka/consumer/OrderEventConsumer.java
  symbol: OrderEventConsumer @KafkaListener declaration
  source_fingerprint:
    algorithm: sha256
    value: "3fb33358ad66f79a55d8159b7b75f84047f79eeff124770bdf2fc91b41219111"
  original_line_range: {start_line: 13, end_line: 14, status: advisory}
  line_numbers_authoritative: false
current_implementation:
  evidence_id: EV-F-004-01
  original_source_excerpt: |
        @KafkaListener(topics = "order-events", groupId = "inventory-service")
        public void consume(Map<String, Object> event) {
proposed_implementation:
  illustrative_code_status: generated
  source_language: java
  target_repository_path: source/inventory-service/src/main/java/com/ecommerce/inventory/kafka/consumer/OrderEventConsumer.java
  target_symbol: OrderEventConsumer @KafkaListener declaration
  replaces_or_updates_evidence_ids: [EV-F-004-01]
  illustrative_code: |
    @KafkaListener(
            id = "${app.kafka.consumer.listener-id:order-events-listener}",
            topics = "order-events",
            groupId = "inventory-service",
            autoStartup = "${app.kafka.consumer.enabled:true}",
            containerFactory = "orderEventListenerContainerFactory")
    public void consume(Map<String, Object> event, Acknowledgment acknowledgment) {
  narrative_explanation: >-
    The listener gains a stable id so the endpoint registry can address it, and an autoStartup expression
    so a deployment can decide whether this regional instance consumes. The default value is true, which
    preserves today's behaviour for every existing deployment. The topic and groupId are unchanged. The
    containerFactory reference and the Acknowledgment parameter are introduced by CHANGE-AA-019, which
    owns the ack and error contract; they appear here because the two changes edit the same declaration.
  discovery_required_reason: null
  unresolved_inputs: []
```

### ICB-007-02: Regional consumption controller

```yaml
change_id: CHANGE-AA-007
block_id: ICB-007-02
target:
  repository_path: source/inventory-service/src/main/java/com/ecommerce/inventory/kafka/RegionalConsumptionController.java
  symbol: RegionalConsumptionController
  target_status: new_file
current_implementation:
  evidence_id: EV-F-004-01
  evidence_note: >-
    No KafkaListenerEndpointRegistry manipulation, lease acquisition, ownership epoch, fencing token, or
    SQL primary-role verification exists in production source.
proposed_implementation:
  illustrative_code_status: generated
  source_language: java
  target_repository_path: source/inventory-service/src/main/java/com/ecommerce/inventory/kafka/RegionalConsumptionController.java
  target_symbol: RegionalConsumptionController
  replaces_or_updates_evidence_ids: [EV-F-004-01]
  illustrative_code: |
    package com.ecommerce.inventory.kafka;

    import io.micrometer.core.instrument.Gauge;
    import io.micrometer.core.instrument.MeterRegistry;
    import lombok.extern.slf4j.Slf4j;
    import org.springframework.beans.factory.annotation.Value;
    import org.springframework.kafka.config.KafkaListenerEndpointRegistry;
    import org.springframework.kafka.listener.MessageListenerContainer;
    import org.springframework.stereotype.Component;

    import jakarta.annotation.PostConstruct;

    @Slf4j
    @Component
    public class RegionalConsumptionController {

        private final KafkaListenerEndpointRegistry registry;
        private final MeterRegistry meterRegistry;
        private final String listenerId;

        public RegionalConsumptionController(KafkaListenerEndpointRegistry registry,
                                             MeterRegistry meterRegistry,
                                             @Value("${app.kafka.consumer.listener-id:order-events-listener}") String listenerId) {
            this.registry = registry;
            this.meterRegistry = meterRegistry;
            this.listenerId = listenerId;
        }

        @PostConstruct
        void registerActivationGauge() {
            Gauge.builder("inventory.kafka.consumption.active", this, controller -> controller.isActive() ? 1d : 0d)
                    .description("1 when this instance is consuming order-events, 0 when it is not")
                    .tag("listenerId", listenerId)
                    .register(meterRegistry);
            log.info("kafka consumption activation state={} listenerId={}", isActive(), listenerId);
        }

        public boolean isActive() {
            MessageListenerContainer container = registry.getListenerContainer(listenerId);
            return container != null && container.isRunning();
        }

        public void activate() {
            MessageListenerContainer container = requireContainer();
            if (!container.isRunning()) {
                container.start();
                log.info("kafka consumption transition=activated listenerId={}", listenerId);
            }
        }

        public void deactivate() {
            MessageListenerContainer container = requireContainer();
            if (container.isRunning()) {
                container.stop();
                log.info("kafka consumption transition=deactivated listenerId={}", listenerId);
            }
        }

        private MessageListenerContainer requireContainer() {
            MessageListenerContainer container = registry.getListenerContainer(listenerId);
            if (container == null) {
                throw new IllegalStateException("No Kafka listener container registered for id " + listenerId);
            }
            return container;
        }
    }
  narrative_explanation: >-
    The controller exposes start and stop for the named listener container and publishes the current
    activation state as a gauge. Combined with the region tag from CHANGE-AA-005, an operator can see at
    a glance whether more than one region is consuming, which is the split-brain condition F-004
    describes. The controller reports and changes local activation only; it does not assign the regional
    role.
  discovery_required_reason: null
  unresolved_inputs: []
```

### ICB-007-03: Self-enforced single-active ownership

```yaml
change_id: CHANGE-AA-007
block_id: ICB-007-03
target:
  repository_path: not_yet_selected
  symbol: OwnershipLease
  target_status: new_file
current_implementation:
  evidence_id: EV-F-004-01
  evidence_note: >-
    No lease acquisition, ownership epoch, fencing token, or SQL primary-role verification exists in
    production source.
proposed_implementation:
  illustrative_code_status: targeted_discovery_required
  source_language: java
  target_repository_path: not_yet_selected
  target_symbol: OwnershipLease
  replaces_or_updates_evidence_ids: [EV-F-004-01]
  illustrative_code: null
  narrative_explanation: >-
    Beyond deployment-controlled activation, the approved single_active model would be enforced by the
    application itself through an ownership lease with an epoch or fencing token, so that a stale
    former-active instance cannot resume consumption after a promotion even if its configuration still
    says enabled.
  discovery_required_reason: >-
    No approved ownership, lease, or fencing mechanism exists in the repository or in
    grounding/governance/approved-libraries.yml, and EG-010 records that how standby-region consumption
    is currently prevented remains unconfirmed. Selecting a lease store, a lease protocol, or a fencing
    token scheme would be an unapproved architecture decision, and it would also determine whether a new
    persistence target is introduced, which the approved architecture does not currently declare.
  unresolved_inputs:
    - Approved ownership and fencing mechanism for single-active consumption
    - Confirmation from EG-010 of how standby-region consumption is prevented today
    - Whether the lease may reside in the existing Azure SQL authoritative store or requires another mechanism
```

### ICB-008-01: Processed operation entity

```yaml
change_id: CHANGE-AA-008
block_id: ICB-008-01
target:
  repository_path: source/inventory-service/src/main/java/com/ecommerce/inventory/model/ProcessedOperation.java
  symbol: ProcessedOperation
  target_status: new_file
current_implementation:
  evidence_id: EV-F-003-02
  evidence_note: >-
    No reservation record, processed-event table, unique constraint on (productId, referenceId), or
    conditional update guards a repeated application.
proposed_implementation:
  illustrative_code_status: generated
  source_language: java
  target_repository_path: source/inventory-service/src/main/java/com/ecommerce/inventory/model/ProcessedOperation.java
  target_symbol: ProcessedOperation
  replaces_or_updates_evidence_ids: [EV-F-003-02]
  illustrative_code: |
    package com.ecommerce.inventory.model;

    import jakarta.persistence.Column;
    import jakarta.persistence.Entity;
    import jakarta.persistence.GeneratedValue;
    import jakarta.persistence.GenerationType;
    import jakarta.persistence.Id;
    import jakarta.persistence.Table;
    import jakarta.persistence.UniqueConstraint;
    import lombok.AllArgsConstructor;
    import lombok.Builder;
    import lombok.Data;
    import lombok.NoArgsConstructor;

    import java.time.Instant;

    @Entity
    @Table(name = "processed_operations",
            uniqueConstraints = @UniqueConstraint(name = "UQ_processed_operations_identity", columnNames = "operationIdentity"))
    @Data @Builder @NoArgsConstructor @AllArgsConstructor
    public class ProcessedOperation {
        @Id @GeneratedValue(strategy = GenerationType.IDENTITY) private Long id;
        @Column(nullable = false, length = 512) private String operationIdentity;
        @Column(nullable = false, length = 64) private String operationType;
        @Column(nullable = false, length = 255) private String productId;
        @Column(nullable = false, length = 255) private String referenceId;
        @Column(nullable = false) private Instant processedAt;
    }
  narrative_explanation: >-
    The entity follows the existing InventoryItem conventions exactly: Lombok @Data with @Builder, an
    identity primary key, and a table-level unique constraint. operationIdentity is the stable key that
    makes a repeated application detectable, and the component parts are stored alongside it so an
    operator can inspect the record without parsing the key.
  discovery_required_reason: null
  unresolved_inputs: []
```

### ICB-008-02: Processed operation repository

```yaml
change_id: CHANGE-AA-008
block_id: ICB-008-02
target:
  repository_path: source/inventory-service/src/main/java/com/ecommerce/inventory/repository/ProcessedOperationRepository.java
  symbol: ProcessedOperationRepository
  target_status: new_file
current_implementation:
  evidence_id: EV-F-003-02
  evidence_note: The only repository is InventoryRepository extends JpaRepository<InventoryItem, Long>.
proposed_implementation:
  illustrative_code_status: generated
  source_language: java
  target_repository_path: source/inventory-service/src/main/java/com/ecommerce/inventory/repository/ProcessedOperationRepository.java
  target_symbol: ProcessedOperationRepository
  replaces_or_updates_evidence_ids: [EV-F-003-02]
  illustrative_code: |
    package com.ecommerce.inventory.repository;

    import com.ecommerce.inventory.model.ProcessedOperation;
    import org.springframework.data.jpa.repository.JpaRepository;

    public interface ProcessedOperationRepository extends JpaRepository<ProcessedOperation, Long> {
        boolean existsByOperationIdentity(String operationIdentity);
    }
  narrative_explanation: >-
    A derived query in the same style as the existing existsByProductId method on InventoryRepository.
    The existence check is the fast path; the unique constraint remains the authority under concurrency.
  discovery_required_reason: null
  unresolved_inputs: []
```

### ICB-008-03: Processed operation migration script

```yaml
change_id: CHANGE-AA-008
block_id: ICB-008-03
target:
  repository_path: source/inventory-service/src/main/resources/db/migration/V2__processed_operation.sql
  symbol: processed_operations
  target_status: new_file
current_implementation:
  evidence_id: EV-F-003-02
  evidence_note: No deduplication table exists in the assessed schema.
proposed_implementation:
  illustrative_code_status: generated
  source_language: sql
  target_repository_path: source/inventory-service/src/main/resources/db/migration/V2__processed_operation.sql
  target_symbol: processed_operations
  replaces_or_updates_evidence_ids: [EV-F-003-02]
  illustrative_code: |
    CREATE TABLE processed_operations (
        id                BIGINT IDENTITY(1,1) NOT NULL,
        operationIdentity VARCHAR(512)         NOT NULL,
        operationType     VARCHAR(64)          NOT NULL,
        productId         VARCHAR(255)         NOT NULL,
        referenceId       VARCHAR(255)         NOT NULL,
        processedAt       DATETIME2            NOT NULL,
        CONSTRAINT PK_processed_operations PRIMARY KEY (id),
        CONSTRAINT UQ_processed_operations_identity UNIQUE (operationIdentity)
    );

    CREATE INDEX IX_processed_operations_processedAt ON processed_operations (processedAt);
  narrative_explanation: >-
    The unique constraint is what makes duplicate suppression correct under concurrency; the existence
    check in the repository is only an optimization. The processedAt index supports the retention purge
    that RISK-008-01 requires once a retention window is approved. The script is written in the same
    dialect as the ICB-002-02 baseline and is applied by whichever runner ICB-002-03 resolves to.
  discovery_required_reason: null
  unresolved_inputs:
    - Approved retention window, which determines the purge statement that accompanies this table
```

### ICB-008-04: Idempotent stock adjustment

```yaml
change_id: CHANGE-AA-008
block_id: ICB-008-04
target:
  repository_path: source/inventory-service/src/main/java/com/ecommerce/inventory/service/impl/InventoryServiceImpl.java
  symbol: InventoryServiceImpl.reserve and InventoryServiceImpl.release
  source_fingerprint:
    algorithm: sha256
    value: "0f2357c4e940ae72aaa92d8f2daf7677017121934274498c15ac4e150ebbafe4"
  original_line_range: {start_line: 37, end_line: 50, status: advisory}
  line_numbers_authoritative: false
current_implementation:
  evidence_id: EV-F-003-02
  original_source_excerpt: |
        @Override @Transactional
        public InventoryResponse reserve(String productId, int quantity, String referenceId) {
            InventoryItem item = findByProduct(productId);
            if (item.getAvailableQuantity() < quantity) throw new IllegalArgumentException("Insufficient inventory for product: " + productId);
            item.setAvailableQuantity(item.getAvailableQuantity() - quantity); item.setReservedQuantity(item.getReservedQuantity() + quantity); item.setUpdatedAt(Instant.now());
            return saveAndPublish(item, "INVENTORY_RESERVED", referenceId);
        }
        @Override @Transactional
        public InventoryResponse release(String productId, int quantity, String referenceId) {
            InventoryItem item = findByProduct(productId);
            if (item.getReservedQuantity() < quantity) throw new IllegalArgumentException("Release exceeds reserved inventory for product: " + productId);
            item.setReservedQuantity(item.getReservedQuantity() - quantity); item.setAvailableQuantity(item.getAvailableQuantity() + quantity); item.setUpdatedAt(Instant.now());
            return saveAndPublish(item, "INVENTORY_RELEASED", referenceId);
        }
proposed_implementation:
  illustrative_code_status: generated
  source_language: java
  target_repository_path: source/inventory-service/src/main/java/com/ecommerce/inventory/service/impl/InventoryServiceImpl.java
  target_symbol: InventoryServiceImpl.reserve and InventoryServiceImpl.release
  replaces_or_updates_evidence_ids: [EV-F-003-02]
  illustrative_code: |
    @Override
    @Transactional(timeout = 10)
    public InventoryResponse reserve(String productId, int quantity, String referenceId) {
        return applyOnce("INVENTORY_RESERVED", productId, referenceId, item -> {
            if (item.getAvailableQuantity() < quantity) {
                throw new IllegalArgumentException("Insufficient inventory for product: " + productId);
            }
            item.setAvailableQuantity(item.getAvailableQuantity() - quantity);
            item.setReservedQuantity(item.getReservedQuantity() + quantity);
        });
    }

    @Override
    @Transactional(timeout = 10)
    public InventoryResponse release(String productId, int quantity, String referenceId) {
        return applyOnce("INVENTORY_RELEASED", productId, referenceId, item -> {
            if (item.getReservedQuantity() < quantity) {
                throw new IllegalArgumentException("Release exceeds reserved inventory for product: " + productId);
            }
            item.setReservedQuantity(item.getReservedQuantity() - quantity);
            item.setAvailableQuantity(item.getAvailableQuantity() + quantity);
        });
    }

    private InventoryResponse applyOnce(String operationType,
                                        String productId,
                                        String referenceId,
                                        Consumer<InventoryItem> adjustment) {
        InventoryItem item = findByProduct(productId);
        String operationIdentity = operationIdentity(operationType, productId, referenceId);

        if (processedOperations.existsByOperationIdentity(operationIdentity)) {
            telemetry.recordConsumption(operationType, InventoryTelemetry.OUTCOME_DUPLICATE);
            return mapper.toResponse(item);
        }

        adjustment.accept(item);
        item.setUpdatedAt(Instant.now());

        try {
            processedOperations.saveAndFlush(ProcessedOperation.builder()
                    .operationIdentity(operationIdentity)
                    .operationType(operationType)
                    .productId(productId)
                    .referenceId(referenceId)
                    .processedAt(Instant.now())
                    .build());
        } catch (DataIntegrityViolationException duplicate) {
            telemetry.recordConsumption(operationType, InventoryTelemetry.OUTCOME_DUPLICATE);
            throw new DuplicateOperationException(operationIdentity, duplicate);
        }

        return saveAndPublish(item, operationType, referenceId);
    }

    private static String operationIdentity(String operationType, String productId, String referenceId) {
        return operationType + ':' + productId + ':' + referenceId;
    }
  narrative_explanation: >-
    Both adjustment paths route through one method that derives a stable operation identity, checks for a
    prior application, performs the existing business precondition and quantity arithmetic unchanged, and
    writes the deduplication record inside the same transaction. The existence check is the fast path and
    the unique constraint is the authority under concurrency, which is why the constraint violation is
    caught and translated rather than allowed to surface as a generic failure. The quantity arithmetic,
    the exception types, and the exception messages are preserved exactly as assessed so business
    semantics do not change. The explicit transaction timeout is the CHANGE-AA-009 obligation applied at
    the same edit site.
  discovery_required_reason: null
  unresolved_inputs:
    - >-
      Behaviour for an absent or blank referenceId on the REST path. The consumer path always supplies
      orderId, so consumer-side deduplication is unaffected, but the REST contract decision is
      approval-gated under CHANGE-AA-008 change_boundary.
```

### ICB-008-05: Consumer-side operation identity

```yaml
change_id: CHANGE-AA-008
block_id: ICB-008-05
target:
  repository_path: source/inventory-service/src/main/java/com/ecommerce/inventory/kafka/consumer/OrderEventConsumer.java
  symbol: OrderEventConsumer.consume
  source_fingerprint:
    algorithm: sha256
    value: "f2448385d75dddda90a66a8f14c24be293a8598977f02d7139d1625ea498f4e9"
  original_line_range: {start_line: 13, end_line: 21, status: advisory}
  line_numbers_authoritative: false
current_implementation:
  evidence_id: EV-F-003-01
  original_source_excerpt: |
        @KafkaListener(topics = "order-events", groupId = "inventory-service")
        public void consume(Map<String, Object> event) {
            String type = String.valueOf(event.get("type"));
            String productId = String.valueOf(event.get("productId"));
            int quantity = ((Number) event.get("quantity")).intValue();
            String orderId = String.valueOf(event.get("orderId"));
            if ("ORDER_CREATED".equals(type)) service.reserve(productId, quantity, orderId);
            if ("ORDER_CANCELLED".equals(type)) service.release(productId, quantity, orderId);
        }
proposed_implementation:
  illustrative_code_status: generated
  source_language: java
  target_repository_path: source/inventory-service/src/main/java/com/ecommerce/inventory/kafka/consumer/OrderEventConsumer.java
  target_symbol: OrderEventConsumer.consume duplicate handling
  replaces_or_updates_evidence_ids: [EV-F-003-01]
  illustrative_code: |
    try {
        switch (payload.type()) {
            case "ORDER_CREATED" -> service.reserve(payload.productId(), payload.quantity(), payload.orderId());
            case "ORDER_CANCELLED" -> service.release(payload.productId(), payload.quantity(), payload.orderId());
            default -> telemetry.recordConsumption(payload.type(), InventoryTelemetry.OUTCOME_SUCCESS);
        }
        telemetry.recordConsumption(payload.type(), InventoryTelemetry.OUTCOME_SUCCESS);
    } catch (DuplicateOperationException alreadyApplied) {
        log.info("order event already applied operationIdentity={}", alreadyApplied.getOperationIdentity());
        telemetry.recordConsumption(payload.type(), InventoryTelemetry.OUTCOME_DUPLICATE);
    }
    acknowledgment.acknowledge();
  narrative_explanation: >-
    The consumer continues to pass the event orderId through as the reference identifier, which is what
    makes the operation identity stable across redelivery, rebalance, restart, and promotion replay. A
    duplicate is treated as a completed operation rather than a failure, so the offset advances and the
    record is not retried or quarantined. The payload record and the acknowledgment parameter are
    supplied by CHANGE-AA-019; this block shows only the duplicate handling that CHANGE-AA-008 owns. The
    business mapping of ORDER_CREATED to reserve and ORDER_CANCELLED to release is unchanged.
  discovery_required_reason: null
  unresolved_inputs: []
```

### ICB-009-01: Externalized dependency deadlines

```yaml
change_id: CHANGE-AA-009
block_id: ICB-009-01
target:
  repository_path: source/inventory-service/src/main/resources/application.yml
  symbol: spring.datasource, spring.data.redis, and spring.kafka timeout properties
  source_fingerprint:
    algorithm: sha256
    value: "e5de0c96c0169828ab9cf2747ececd749c083244d46003486999f23bde203f1b"
  original_line_range: {start_line: 6, end_line: 9, status: advisory}
  line_numbers_authoritative: false
current_implementation:
  evidence_id: EV-F-009-01
  original_source_excerpt: |
      datasource:
        url: ${SQL_URL:jdbc:sqlserver://localhost:1433;databaseName=inventory;encrypt=false}
        username: ${SQL_USERNAME}
        password: ${SQL_PASSWORD}
  additional_evidence:
    - evidence_id: EV-F-010-01
      original_source_excerpt: |
          data:
            redis:
              url: ${REDIS_URL:redis://localhost:6379}
          cache:
            type: redis
    - evidence_id: EV-F-011-01
      original_source_excerpt: |
          kafka:
            bootstrap-servers: ${KAFKA_BOOTSTRAP_SERVERS}
            properties:
              security.protocol: ${KAFKA_SECURITY_PROTOCOL:PLAINTEXT}
proposed_implementation:
  illustrative_code_status: generated
  source_language: yaml
  target_repository_path: source/inventory-service/src/main/resources/application.yml
  target_symbol: spring.datasource.hikari, spring.jpa.properties, spring.data.redis, spring.kafka
  replaces_or_updates_evidence_ids: [EV-F-009-01, EV-F-010-01, EV-F-011-01]
  illustrative_code: |
    spring:
      datasource:
        url: ${SQL_URL:jdbc:sqlserver://localhost:1433;databaseName=inventory;encrypt=false}
        username: ${SQL_USERNAME}
        password: ${SQL_PASSWORD}
        hikari:
          connection-timeout: ${SQL_CONNECTION_TIMEOUT_MS}
          validation-timeout: ${SQL_VALIDATION_TIMEOUT_MS}
          max-lifetime: ${SQL_MAX_LIFETIME_MS}
          keepalive-time: ${SQL_KEEPALIVE_MS}
          maximum-pool-size: ${SQL_MAX_POOL_SIZE}
          data-source-properties:
            loginTimeout: ${SQL_LOGIN_TIMEOUT_SECONDS}
            socketTimeout: ${SQL_SOCKET_TIMEOUT_MS}
      jpa:
        properties:
          jakarta.persistence.query.timeout: ${SQL_QUERY_TIMEOUT_MS}
      data:
        redis:
          url: ${REDIS_URL:redis://localhost:6379}
          timeout: ${REDIS_COMMAND_TIMEOUT}
          connect-timeout: ${REDIS_CONNECT_TIMEOUT}
      kafka:
        properties:
          reconnect.backoff.ms: ${KAFKA_RECONNECT_BACKOFF_MS}
          reconnect.backoff.max.ms: ${KAFKA_RECONNECT_BACKOFF_MAX_MS}
          retry.backoff.ms: ${KAFKA_RETRY_BACKOFF_MS}
        producer:
          properties:
            max.block.ms: ${KAFKA_PRODUCER_MAX_BLOCK_MS}
            request.timeout.ms: ${KAFKA_PRODUCER_REQUEST_TIMEOUT_MS}
            delivery.timeout.ms: ${KAFKA_PRODUCER_DELIVERY_TIMEOUT_MS}
        consumer:
          properties:
            session.timeout.ms: ${KAFKA_CONSUMER_SESSION_TIMEOUT_MS}
            heartbeat.interval.ms: ${KAFKA_CONSUMER_HEARTBEAT_INTERVAL_MS}
            max.poll.interval.ms: ${KAFKA_CONSUMER_MAX_POLL_INTERVAL_MS}
            max.poll.records: ${KAFKA_CONSUMER_MAX_POLL_RECORDS}
  narrative_explanation: >-
    Every deadline is a placeholder with no default, so a deployment must supply a value and no
    unapproved number is embedded in the repository. JDBC login and socket timeouts are supplied through
    Hikari data-source-properties rather than by appending to the connection string, so the externally
    supplied SQL_CONNECTION_STRING value in the prod profile is never rewritten. The existing url,
    username, password, and Redis url lines are preserved unchanged.
  discovery_required_reason: null
  unresolved_inputs:
    - Approved numeric budgets, which depend on the gateway and load balancer timeouts recorded as EG-006
```

### ICB-009-02: Explicit transaction deadlines

```yaml
change_id: CHANGE-AA-009
block_id: ICB-009-02
target:
  repository_path: source/inventory-service/src/main/java/com/ecommerce/inventory/service/impl/InventoryServiceImpl.java
  symbol: InventoryServiceImpl @Transactional write paths
  source_fingerprint:
    algorithm: sha256
    value: "b83ea6804189eda80504680e18a8e5d142666b78feb552b48057aac1162f3989"
  original_line_range: {start_line: 44, end_line: 50, status: advisory}
  line_numbers_authoritative: false
current_implementation:
  evidence_id: EV-F-012-02
  original_source_excerpt: |
        @Override @Transactional
        public InventoryResponse release(String productId, int quantity, String referenceId) {
            InventoryItem item = findByProduct(productId);
            if (item.getReservedQuantity() < quantity) throw new IllegalArgumentException("Release exceeds reserved inventory for product: " + productId);
            item.setReservedQuantity(item.getReservedQuantity() - quantity); item.setAvailableQuantity(item.getAvailableQuantity() + quantity); item.setUpdatedAt(Instant.now());
            return saveAndPublish(item, "INVENTORY_RELEASED", referenceId);
        }
proposed_implementation:
  illustrative_code_status: generated
  source_language: java
  target_repository_path: source/inventory-service/src/main/java/com/ecommerce/inventory/service/impl/InventoryServiceImpl.java
  target_symbol: "@Transactional timeout attribute on create, update, delete, reserve, and release"
  replaces_or_updates_evidence_ids: [EV-F-012-02]
  illustrative_code: |
    @Override
    @Transactional(timeout = ${SQL_TRANSACTION_TIMEOUT_SECONDS})
    public InventoryResponse release(String productId, int quantity, String referenceId) {
        // Body unchanged; see ICB-008-04 for the idempotent form of this method.
    }
  narrative_explanation: >-
    Every @Transactional write path declares an explicit timeout so a commit cannot block for the driver
    default. Because the annotation attribute must be a compile-time constant, the implementer binds the
    value through a constant or a TransactionTemplate rather than a property placeholder; the placeholder
    shown here identifies the value that must be externalized, not the literal syntax.
  discovery_required_reason: null
  unresolved_inputs:
    - >-
      Whether the transaction deadline is expressed as a compile-time constant on the annotation or
      through a TransactionTemplate bound to an externalized property. The plan requires the value to be
      externally configurable; the binding mechanism is an implementation choice for Task Implementor.
```

### ICB-010-01: Approved resiliency library dependency

```yaml
change_id: CHANGE-AA-010
block_id: ICB-010-01
target:
  repository_path: source/inventory-service/pom.xml
  symbol: project/dependencies
  source_fingerprint:
    algorithm: sha256
    value: "d1af2cf103de040ee5932ef455e58ec46fd6409bfba9ea02838287f980a47ecd"
  original_line_range: {start_line: 7, end_line: 26, status: advisory}
  line_numbers_authoritative: false
current_implementation:
  evidence_id: EV-F-012-01
  original_source_excerpt: |
        <dependencies>
            <dependency><groupId>org.springframework.boot</groupId><artifactId>spring-boot-starter-web</artifactId></dependency>
            <dependency><groupId>org.springframework.boot</groupId><artifactId>spring-boot-starter-validation</artifactId></dependency>
            <dependency><groupId>org.springframework.boot</groupId><artifactId>spring-boot-starter-actuator</artifactId></dependency>
            <dependency><groupId>org.springframework.boot</groupId><artifactId>spring-boot-starter-data-jpa</artifactId></dependency>
            <dependency><groupId>org.springframework.boot</groupId><artifactId>spring-boot-starter-data-redis</artifactId></dependency>
            <dependency><groupId>org.springframework.boot</groupId><artifactId>spring-boot-starter-cache</artifactId></dependency>
            <dependency><groupId>org.springframework.kafka</groupId><artifactId>spring-kafka</artifactId></dependency>
            <dependency><groupId>com.microsoft.sqlserver</groupId><artifactId>mssql-jdbc</artifactId><scope>runtime</scope></dependency>
            <dependency><groupId>com.azure.spring</groupId><artifactId>spring-cloud-azure-starter-keyvault-secrets</artifactId></dependency>
            <dependency><groupId>org.springdoc</groupId><artifactId>springdoc-openapi-starter-webmvc-ui</artifactId><version>2.6.0</version></dependency>
            <dependency><groupId>io.micrometer</groupId><artifactId>micrometer-registry-prometheus</artifactId></dependency>
            <dependency><groupId>net.logstash.logback</groupId><artifactId>logstash-logback-encoder</artifactId><version>8.0</version></dependency>
            <dependency><groupId>org.mapstruct</groupId><artifactId>mapstruct</artifactId><version>${mapstruct.version}</version></dependency>
            <dependency><groupId>org.projectlombok</groupId><artifactId>lombok</artifactId><optional>true</optional></dependency>
            <dependency><groupId>org.springframework.boot</groupId><artifactId>spring-boot-starter-test</artifactId><scope>test</scope></dependency>
            <dependency><groupId>org.springframework.kafka</groupId><artifactId>spring-kafka-test</artifactId><scope>test</scope></dependency>
            <dependency><groupId>org.testcontainers</groupId><artifactId>junit-jupiter</artifactId><version>${testcontainers.version}</version><scope>test</scope></dependency>
            <dependency><groupId>org.testcontainers</groupId><artifactId>mssqlserver</artifactId><version>${testcontainers.version}</version><scope>test</scope></dependency>
        </dependencies>
proposed_implementation:
  illustrative_code_status: generated
  source_language: xml
  target_repository_path: source/inventory-service/pom.xml
  target_symbol: project/dependencies resilience4j
  replaces_or_updates_evidence_ids: [EV-F-012-01]
  illustrative_code: |
    <dependency>
        <groupId>io.github.resilience4j</groupId>
        <artifactId>resilience4j-spring-boot3</artifactId>
    </dependency>
    <dependency>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-aop</artifactId>
    </dependency>
  narrative_explanation: >-
    Resilience4j is the approved resiliency library and retry, circuit_breaker, bulkhead, and
    time_limiter are all listed under approved_capabilities, so this dependency supports CHANGE-AA-010,
    CHANGE-AA-011, and CHANGE-AA-013. The Spring Boot AOP starter is required for the annotation-driven
    model and its version is managed by the existing Spring Boot parent. No version is declared for
    Resilience4j because the approved version source is not yet established.
  discovery_required_reason: null
  unresolved_inputs:
    - >-
      library_rules.version_source is not_specified and the Spring Boot 3.3.5 parent does not manage
      Resilience4j versions, so the version must be supplied by an approved BOM import or a managed
      property before this block is finalized.
```

### ICB-010-02: Transient failure classifier

```yaml
change_id: CHANGE-AA-010
block_id: ICB-010-02
target:
  repository_path: source/inventory-service/src/main/java/com/ecommerce/inventory/service/TransientFailureClassifier.java
  symbol: TransientFailureClassifier
  target_status: new_file
current_implementation:
  evidence_id: EV-F-012-01
  evidence_note: >-
    No production class declares @Retryable, builds a RetryTemplate, or wraps a transaction boundary in a
    retry policy, so no failure classification exists to extend.
proposed_implementation:
  illustrative_code_status: generated
  source_language: java
  target_repository_path: source/inventory-service/src/main/java/com/ecommerce/inventory/service/TransientFailureClassifier.java
  target_symbol: TransientFailureClassifier
  replaces_or_updates_evidence_ids: [EV-F-012-01]
  illustrative_code: |
    package com.ecommerce.inventory.service;

    import org.springframework.dao.ConcurrencyFailureException;
    import org.springframework.dao.TransientDataAccessException;
    import org.springframework.stereotype.Component;
    import org.springframework.transaction.TransactionSystemException;

    import java.sql.SQLTransientException;

    @Component
    public class TransientFailureClassifier {

        public boolean isTransient(Throwable throwable) {
            for (Throwable cause = throwable; cause != null; cause = cause.getCause()) {
                if (cause instanceof TransientDataAccessException
                        || cause instanceof ConcurrencyFailureException
                        || cause instanceof SQLTransientException) {
                    return true;
                }
                if (cause instanceof TransactionSystemException) {
                    // Commit outcome is unknown; never retried blindly.
                    return false;
                }
                if (cause == cause.getCause()) {
                    break;
                }
            }
            return false;
        }
    }
  narrative_explanation: >-
    Classification is explicit and conservative. Spring's transient and concurrency data access
    hierarchies plus the JDBC transient exception are treated as retryable. A TransactionSystemException
    signals an ambiguous commit outcome and is deliberately excluded, so it is routed to the idempotency
    check from CHANGE-AA-008 rather than retried. Business failures such as IllegalArgumentException and
    ResourceNotFoundException are not in the retryable set, so their current caller-visible behaviour is
    preserved exactly.
  discovery_required_reason: null
  unresolved_inputs: []
```

### ICB-010-03: Externalized retry policy

```yaml
change_id: CHANGE-AA-010
block_id: ICB-010-03
target:
  repository_path: source/inventory-service/src/main/resources/application.yml
  symbol: resilience4j.retry.instances.inventoryWrite
  target_status: new_configuration_block
current_implementation:
  evidence_id: EV-F-012-01
  evidence_note: No retry property exists in either profile.
proposed_implementation:
  illustrative_code_status: generated
  source_language: yaml
  target_repository_path: source/inventory-service/src/main/resources/application.yml
  target_symbol: resilience4j.retry
  replaces_or_updates_evidence_ids: [EV-F-012-01]
  illustrative_code: |
    resilience4j:
      retry:
        instances:
          inventoryWrite:
            max-attempts: ${RETRY_WRITE_MAX_ATTEMPTS}
            wait-duration: ${RETRY_WRITE_WAIT_DURATION}
            enable-exponential-backoff: true
            exponential-backoff-multiplier: ${RETRY_WRITE_BACKOFF_MULTIPLIER}
            enable-randomized-wait: true
            randomized-wait-factor: ${RETRY_WRITE_JITTER_FACTOR}
            retry-exception-predicate: com.ecommerce.inventory.service.TransientRetryPredicate
          inventoryConflict:
            max-attempts: ${RETRY_CONFLICT_MAX_ATTEMPTS}
            wait-duration: ${RETRY_CONFLICT_WAIT_DURATION}
            enable-randomized-wait: true
            retry-exceptions:
              - org.springframework.orm.ObjectOptimisticLockingFailureException
  narrative_explanation: >-
    Two retry instances are declared: one for transient dependency failures governed by the classifier
    from ICB-010-02, and one for optimistic-locking conflicts used by CHANGE-AA-011. Every attempt count,
    wait, multiplier, and jitter factor is an externalized placeholder, so no approved numeric value is
    asserted by this plan. Randomized wait is enabled on both so a regional recovery does not produce
    synchronized retry storms.
  discovery_required_reason: null
  unresolved_inputs:
    - Approved attempt counts, wait durations, and total retry budget ordered against the gateway budget
```

### ICB-011-01: Bounded reload and reapply

```yaml
change_id: CHANGE-AA-011
block_id: ICB-011-01
target:
  repository_path: source/inventory-service/src/main/java/com/ecommerce/inventory/service/impl/InventoryServiceImpl.java
  symbol: InventoryServiceImpl conflict handling
  source_fingerprint:
    algorithm: sha256
    value: "5e29c55e63ae5f984a5a875a87980656b30c6cb572f0499822fc50589ea074ea"
  original_line_range: {start_line: 26, end_line: 26, status: advisory}
  line_numbers_authoritative: false
current_implementation:
  evidence_id: EV-F-013-01
  original_source_excerpt: |
        @Version private long version;
  evidence_note: >-
    The @Version column exists on InventoryItem, so conflicts are raised at flush or commit, but no
    service method catches ObjectOptimisticLockingFailureException.
proposed_implementation:
  illustrative_code_status: generated
  source_language: java
  target_repository_path: source/inventory-service/src/main/java/com/ecommerce/inventory/service/impl/InventoryServiceImpl.java
  target_symbol: InventoryServiceImpl.reserve and InventoryServiceImpl.release conflict retry
  replaces_or_updates_evidence_ids: [EV-F-013-01]
  illustrative_code: |
    @Override
    @Retry(name = "inventoryConflict")
    public InventoryResponse reserve(String productId, int quantity, String referenceId) {
        return transactionTemplate.execute(status -> applyOnce("INVENTORY_RESERVED", productId, referenceId, item -> {
            if (item.getAvailableQuantity() < quantity) {
                throw new IllegalArgumentException("Insufficient inventory for product: " + productId);
            }
            item.setAvailableQuantity(item.getAvailableQuantity() - quantity);
            item.setReservedQuantity(item.getReservedQuantity() + quantity);
        }));
    }
  narrative_explanation: >-
    The retry sits outside the transaction, so each attempt runs in a fresh transaction that re-reads the
    item through findByProduct and re-evaluates the availability precondition against the reloaded state.
    That is what makes reload-and-reapply correct rather than a blind replay of a stale computation. The
    InventoryItem @Version column is unchanged. The idempotency record from CHANGE-AA-008 guarantees the
    reapplied attempt cannot double-apply if a prior attempt actually committed. The @Retry annotation
    requires the AOP proxy boundary, so the implementer must ensure the annotated method is invoked
    through the proxy rather than internally.
  discovery_required_reason: null
  unresolved_inputs: []
```

### ICB-011-02: Conflict exhaustion response mapping

```yaml
change_id: CHANGE-AA-011
block_id: ICB-011-02
target:
  repository_path: source/inventory-service/src/main/java/com/ecommerce/inventory/exception/GlobalExceptionHandler.java
  symbol: GlobalExceptionHandler conflict mapping
  source_fingerprint:
    algorithm: sha256
    value: "c2bc4b46127d9c7fe09cd5784943e3ffbeae121dd7cd6137fd79a7f3db1a0940"
  original_line_range: {start_line: 12, end_line: 21, status: advisory}
  line_numbers_authoritative: false
current_implementation:
  evidence_id: EV-F-013-02
  original_source_excerpt: |
    @RestControllerAdvice
    public class GlobalExceptionHandler {
        @ExceptionHandler(ResourceNotFoundException.class)
        ResponseEntity<Map<String, Object>> notFound(ResourceNotFoundException exception) { return error(HttpStatus.NOT_FOUND, exception.getMessage()); }
        @ExceptionHandler({IllegalArgumentException.class, MethodArgumentNotValidException.class})
        ResponseEntity<Map<String, Object>> badRequest(Exception exception) { return error(HttpStatus.BAD_REQUEST, exception.getMessage()); }
        private ResponseEntity<Map<String, Object>> error(HttpStatus status, String message) {
            return ResponseEntity.status(status).body(Map.of("timestamp", Instant.now().toString(), "status", status.value(), "error", status.getReasonPhrase(), "message", message));
        }
    }
proposed_implementation:
  illustrative_code_status: generated
  source_language: java
  target_repository_path: source/inventory-service/src/main/java/com/ecommerce/inventory/exception/GlobalExceptionHandler.java
  target_symbol: GlobalExceptionHandler.conflict
  replaces_or_updates_evidence_ids: [EV-F-013-02]
  illustrative_code: |
    @ExceptionHandler(ObjectOptimisticLockingFailureException.class)
    ResponseEntity<Map<String, Object>> conflict(ObjectOptimisticLockingFailureException exception) {
        return error(HttpStatus.CONFLICT, "Inventory was modified concurrently. Retry the request.");
    }
  narrative_explanation: >-
    The existing notFound and badRequest handlers and the private error helper are untouched, so the
    current caller-visible contract for those cases is preserved exactly. The new handler returns a fixed
    message rather than the exception message, which keeps entity and version detail out of the response.
    This target is held at implementation_allowed false until the API contract owner approves the use of
    HTTP 409.
  discovery_required_reason: null
  unresolved_inputs:
    - Approved HTTP status and response body for an unresolvable inventory write conflict
```

### ICB-012-01: Dependency failure classification handler

```yaml
change_id: CHANGE-AA-012
block_id: ICB-012-01
target:
  repository_path: source/inventory-service/src/main/java/com/ecommerce/inventory/exception/GlobalExceptionHandler.java
  symbol: GlobalExceptionHandler exception coverage
  source_fingerprint:
    algorithm: sha256
    value: "c2bc4b46127d9c7fe09cd5784943e3ffbeae121dd7cd6137fd79a7f3db1a0940"
  original_line_range: {start_line: 12, end_line: 21, status: advisory}
  line_numbers_authoritative: false
current_implementation:
  evidence_id: EV-F-014-01
  original_source_excerpt: |
    @RestControllerAdvice
    public class GlobalExceptionHandler {
        @ExceptionHandler(ResourceNotFoundException.class)
        ResponseEntity<Map<String, Object>> notFound(ResourceNotFoundException exception) { return error(HttpStatus.NOT_FOUND, exception.getMessage()); }
        @ExceptionHandler({IllegalArgumentException.class, MethodArgumentNotValidException.class})
        ResponseEntity<Map<String, Object>> badRequest(Exception exception) { return error(HttpStatus.BAD_REQUEST, exception.getMessage()); }
        private ResponseEntity<Map<String, Object>> error(HttpStatus status, String message) {
            return ResponseEntity.status(status).body(Map.of("timestamp", Instant.now().toString(), "status", status.value(), "error", status.getReasonPhrase(), "message", message));
        }
    }
proposed_implementation:
  illustrative_code_status: generated
  source_language: java
  target_repository_path: source/inventory-service/src/main/java/com/ecommerce/inventory/exception/GlobalExceptionHandler.java
  target_symbol: GlobalExceptionHandler.dependencyUnavailable
  replaces_or_updates_evidence_ids: [EV-F-014-01]
  illustrative_code: |
    @ExceptionHandler({DataAccessResourceFailureException.class,
                       QueryTimeoutException.class,
                       TransientDataAccessException.class,
                       RedisConnectionFailureException.class,
                       QueryTimeoutException.class,
                       KafkaException.class})
    ResponseEntity<Map<String, Object>> dependencyUnavailable(Exception exception) {
        telemetry.recordFailureClassification(exception.getClass().getSimpleName(), "transient_dependency");
        log.warn("dependency failure classified as transient exception={}", exception.getClass().getName(), exception);
        Map<String, Object> body = new LinkedHashMap<>(error(HttpStatus.SERVICE_UNAVAILABLE,
                "A required dependency is temporarily unavailable.").getBody());
        body.put("code", "DEPENDENCY_UNAVAILABLE");
        return ResponseEntity.status(HttpStatus.SERVICE_UNAVAILABLE)
                .header(HttpHeaders.RETRY_AFTER, String.valueOf(retryAfterSeconds))
                .body(body);
    }
  narrative_explanation: >-
    Transient dependency exceptions are classified and answered with a distinct status, a Retry-After
    hint, and a stable machine-readable code, while the existing 400 and 404 mappings and the existing
    body shape are preserved. The exception message is logged rather than returned, so no connection
    string, host name, or stack detail reaches the caller. The classification itself is recorded as a
    metric, which is the portion of this change that may proceed without approval; the status contract is
    held at implementation_allowed false.
  discovery_required_reason: null
  unresolved_inputs:
    - Approved HTTP status, Retry-After policy, and error-code vocabulary for transient dependency failure
```

### ICB-013-01: Technology-neutral isolation boundary

```yaml
change_id: CHANGE-AA-013
block_id: ICB-013-01
target:
  repository_path: source/inventory-service/src/main/java/com/ecommerce/inventory/service/impl/InventoryServiceImpl.java
  symbol: InventoryServiceImpl.get and write paths
  source_fingerprint:
    algorithm: sha256
    value: "d1af2cf103de040ee5932ef455e58ec46fd6409bfba9ea02838287f980a47ecd"
  original_line_range: {start_line: 7, end_line: 26, status: advisory}
  line_numbers_authoritative: false
current_implementation:
  evidence_id: EV-F-015-01
  evidence_note: >-
    The dependency list assessed in Step 2 contains no bulkhead, circuit breaker, or rate limiter. The
    excerpt is preserved verbatim in ICB-010-01 and is not duplicated here. Production source defines no
    bulkhead, semaphore, or custom executor.
proposed_implementation:
  illustrative_code_status: generated
  source_language: java
  target_repository_path: source/inventory-service/src/main/java/com/ecommerce/inventory/service/impl/InventoryServiceImpl.java
  target_symbol: InventoryServiceImpl dependency isolation annotations
  replaces_or_updates_evidence_ids: [EV-F-015-01]
  illustrative_code: |
    @Override
    @Cacheable(cacheNames = "inventory", key = "#id", sync = true)
    @Bulkhead(name = "inventoryCache", type = Bulkhead.Type.SEMAPHORE)
    public InventoryResponse get(Long id) {
        return mapper.toResponse(find(id));
    }

    @Override
    @Bulkhead(name = "inventoryDb", type = Bulkhead.Type.SEMAPHORE)
    @CircuitBreaker(name = "inventoryDb")
    @Retry(name = "inventoryWrite")
    public InventoryResponse create(InventoryRequest request) {
        // Body unchanged.
    }
  narrative_explanation: >-
    Concurrency into the cache path and into the authoritative store are bounded separately, so a
    saturated cache cannot consume the capacity the database path needs and neither can consume the whole
    servlet pool. Semaphore bulkheads are used rather than thread-pool bulkheads because the existing
    programming model is synchronous servlet code and a thread-pool bulkhead would break the transaction
    and security context propagation this service relies on. The sync attribute shown here is
    CHANGE-AA-016; it appears because the two changes edit the same annotation.
  discovery_required_reason: null
  unresolved_inputs: []
```

### ICB-013-02: Externalized bulkhead and breaker policy

```yaml
change_id: CHANGE-AA-013
block_id: ICB-013-02
target:
  repository_path: source/inventory-service/src/main/resources/application.yml
  symbol: resilience4j.bulkhead and resilience4j.circuitbreaker
  target_status: new_configuration_block
current_implementation:
  evidence_id: EV-F-015-01
  evidence_note: No bulkhead, breaker, or rate-limiter property exists in either profile.
proposed_implementation:
  illustrative_code_status: generated
  source_language: yaml
  target_repository_path: source/inventory-service/src/main/resources/application.yml
  target_symbol: resilience4j.bulkhead and resilience4j.circuitbreaker
  replaces_or_updates_evidence_ids: [EV-F-015-01]
  illustrative_code: |
    resilience4j:
      bulkhead:
        instances:
          inventoryDb:
            max-concurrent-calls: ${BULKHEAD_DB_MAX_CONCURRENT}
            max-wait-duration: ${BULKHEAD_DB_MAX_WAIT}
          inventoryCache:
            max-concurrent-calls: ${BULKHEAD_CACHE_MAX_CONCURRENT}
            max-wait-duration: ${BULKHEAD_CACHE_MAX_WAIT}
      circuitbreaker:
        instances:
          inventoryDb:
            sliding-window-type: COUNT_BASED
            sliding-window-size: ${BREAKER_DB_WINDOW_SIZE}
            minimum-number-of-calls: ${BREAKER_DB_MIN_CALLS}
            failure-rate-threshold: ${BREAKER_DB_FAILURE_RATE}
            wait-duration-in-open-state: ${BREAKER_DB_OPEN_DURATION}
            permitted-number-of-calls-in-half-open-state: ${BREAKER_DB_HALF_OPEN_CALLS}
            automatic-transition-from-open-to-half-open-enabled: true
            record-exceptions:
              - org.springframework.dao.TransientDataAccessException
              - org.springframework.dao.DataAccessResourceFailureException
            ignore-exceptions:
              - com.ecommerce.inventory.exception.ResourceNotFoundException
              - java.lang.IllegalArgumentException
          inventoryCache:
            sliding-window-type: COUNT_BASED
            sliding-window-size: ${BREAKER_CACHE_WINDOW_SIZE}
            minimum-number-of-calls: ${BREAKER_CACHE_MIN_CALLS}
            failure-rate-threshold: ${BREAKER_CACHE_FAILURE_RATE}
            wait-duration-in-open-state: ${BREAKER_CACHE_OPEN_DURATION}
            permitted-number-of-calls-in-half-open-state: ${BREAKER_CACHE_HALF_OPEN_CALLS}
            automatic-transition-from-open-to-half-open-enabled: true
      metrics:
        enabled: true
  narrative_explanation: >-
    No threshold, window size, open duration, half-open call count, or wait duration is hardcoded; every
    value is an externalized placeholder. The exception lists are not invented: recorded exceptions are
    the same Spring data access types the classifier in ICB-010-02 treats as transient, and ignored
    exceptions are the two business exception types the service already throws, so business failures
    never move the breaker. Automatic half-open transition ensures the breaker recovers without traffic
    having to arrive at exactly the right moment.
  discovery_required_reason: null
  unresolved_inputs:
    - Approved concurrency limits, failure-rate thresholds, window sizes, open durations, and half-open call counts
```

### ICB-013-03: Isolation telemetry binding

```yaml
change_id: CHANGE-AA-013
block_id: ICB-013-03
target:
  repository_path: source/inventory-service/src/main/resources/application.yml
  symbol: management.endpoints.web.exposure.include
  source_fingerprint:
    algorithm: sha256
    value: "653a483edc8b2f53255c32fb9a607d3d9e8a7e5f543531165e9ff2230b5471f6"
  original_line_range: {start_line: 29, end_line: 37, status: advisory}
  line_numbers_authoritative: false
current_implementation:
  evidence_id: EV-F-008-01
  evidence_note: >-
    Exposure is limited to health, info, and prometheus. The excerpt is preserved verbatim in ICB-001-01
    and is not duplicated here.
proposed_implementation:
  illustrative_code_status: generated
  source_language: yaml
  target_repository_path: source/inventory-service/src/main/resources/application.yml
  target_symbol: management.metrics.distribution and resilience4j meter binding
  replaces_or_updates_evidence_ids: [EV-F-008-01]
  illustrative_code: |
    management:
      metrics:
        distribution:
          percentiles-histogram:
            resilience4j.circuitbreaker.calls: true
            resilience4j.bulkhead.available.concurrent.calls: true
  narrative_explanation: >-
    Resilience4j registers its own meters into the existing Micrometer Prometheus registry, so breaker
    state transitions and bulkhead rejections reach the already-exposed prometheus endpoint with the
    region and role tags from CHANGE-AA-005. Only the distribution hint is added; the exposure list is
    unchanged, so no new endpoint becomes reachable.
  discovery_required_reason: null
  unresolved_inputs: []
```

### ICB-014-01: Cache error handler

```yaml
change_id: CHANGE-AA-014
block_id: ICB-014-01
target:
  repository_path: source/inventory-service/src/main/java/com/ecommerce/inventory/config/CacheConfig.java
  symbol: CacheConfig
  source_fingerprint:
    algorithm: sha256
    value: "a6a2631175d32371721dbb655166cbd6e505087d9b108c87fd719d65e3e2af65"
  original_line_range: {start_line: 6, end_line: 8, status: advisory}
  line_numbers_authoritative: false
current_implementation:
  evidence_id: EV-F-016-01
  original_source_excerpt: |
    @Configuration @EnableCaching
    public class CacheConfig {
    }
proposed_implementation:
  illustrative_code_status: generated
  source_language: java
  target_repository_path: source/inventory-service/src/main/java/com/ecommerce/inventory/config/CacheConfig.java
  target_symbol: CacheConfig implements CachingConfigurer
  replaces_or_updates_evidence_ids: [EV-F-016-01]
  illustrative_code: |
    package com.ecommerce.inventory.config;

    import com.ecommerce.inventory.observability.InventoryTelemetry;
    import lombok.RequiredArgsConstructor;
    import lombok.extern.slf4j.Slf4j;
    import org.springframework.cache.Cache;
    import org.springframework.cache.annotation.CachingConfigurer;
    import org.springframework.cache.annotation.EnableCaching;
    import org.springframework.cache.interceptor.CacheErrorHandler;
    import org.springframework.context.annotation.Bean;
    import org.springframework.context.annotation.Configuration;

    @Slf4j
    @Configuration
    @EnableCaching
    @RequiredArgsConstructor
    public class CacheConfig implements CachingConfigurer {

        private final InventoryTelemetry telemetry;

        @Bean
        @Override
        public CacheErrorHandler errorHandler() {
            return new CacheErrorHandler() {
                @Override
                public void handleCacheGetError(RuntimeException exception, Cache cache, Object key) {
                    absorb("get", cache, exception);
                }

                @Override
                public void handleCachePutError(RuntimeException exception, Cache cache, Object key, Object value) {
                    absorb("put", cache, exception);
                }

                @Override
                public void handleCacheEvictError(RuntimeException exception, Cache cache, Object key) {
                    absorb("evict", cache, exception);
                }

                @Override
                public void handleCacheClearError(RuntimeException exception, Cache cache) {
                    absorb("clear", cache, exception);
                }

                private void absorb(String operation, Cache cache, RuntimeException exception) {
                    telemetry.recordCacheOutcome(cache.getName(), InventoryTelemetry.CACHE_FAILURE);
                    log.warn("cache operation failed operation={} cache={} exception={}",
                            operation, cache.getName(), exception.getClass().getName());
                }
            };
        }
    }
  narrative_explanation: >-
    Implementing CachingConfigurer and returning a CacheErrorHandler that absorbs rather than rethrows is
    what makes the cache genuinely optional: the cache interceptor falls through to the repository on a
    get failure, and a put, evict, or clear failure no longer fails the surrounding operation. Each
    absorbed failure is counted as a cache failure, which is a distinct dimension from a cache miss, and
    logged without any cached value content. The @EnableCaching declaration is preserved.
  discovery_required_reason: null
  unresolved_inputs: []
```

### ICB-015-01: Explicit Redis cache manager configuration

```yaml
change_id: CHANGE-AA-015
block_id: ICB-015-01
target:
  repository_path: source/inventory-service/src/main/java/com/ecommerce/inventory/config/CacheConfig.java
  symbol: CacheConfig RedisCacheConfiguration
  source_fingerprint:
    algorithm: sha256
    value: "a6a2631175d32371721dbb655166cbd6e505087d9b108c87fd719d65e3e2af65"
  original_line_range: {start_line: 6, end_line: 8, status: advisory}
  line_numbers_authoritative: false
current_implementation:
  evidence_id: EV-F-029-01
  original_source_excerpt: |
    public record InventoryResponse(Long id, String productId, int availableQuantity, int reservedQuantity, Instant updatedAt) {
    }
  additional_evidence:
    - evidence_id: EV-F-017-01
      original_source_excerpt: |
          cache:
            type: redis
    - evidence_id: EV-F-018-01
      original_source_excerpt: |
            @Override @Cacheable(cacheNames = "inventory", key = "#id")
            public InventoryResponse get(Long id) { return mapper.toResponse(find(id)); }
proposed_implementation:
  illustrative_code_status: generated
  source_language: java
  target_repository_path: source/inventory-service/src/main/java/com/ecommerce/inventory/config/CacheConfig.java
  target_symbol: CacheConfig.inventoryCacheConfiguration
  replaces_or_updates_evidence_ids: [EV-F-029-01, EV-F-017-01, EV-F-018-01]
  illustrative_code: |
    @Bean
    public RedisCacheConfiguration inventoryCacheConfiguration(
            @Value("${app.cache.inventory.ttl}") Duration ttl,
            @Value("${app.cache.key-prefix}") String keyPrefix,
            @Value("${app.cache.schema-version}") String schemaVersion,
            ObjectMapper objectMapper) {

        ObjectMapper cacheMapper = objectMapper.copy().registerModule(new JavaTimeModule());
        Jackson2JsonRedisSerializer<InventoryResponse> valueSerializer =
                new Jackson2JsonRedisSerializer<>(cacheMapper, InventoryResponse.class);

        return RedisCacheConfiguration.defaultCacheConfig()
                .entryTtl(ttl)
                .disableCachingNullValues()
                .computePrefixWith(cacheName -> keyPrefix + ':' + schemaVersion + ':' + cacheName + "::")
                .serializeKeysWith(SerializationPair.fromSerializer(new StringRedisSerializer()))
                .serializeValuesWith(SerializationPair.fromSerializer(valueSerializer));
    }
  narrative_explanation: >-
    One bean resolves all three defects. An explicit Jackson serializer bound to InventoryResponse removes
    the dependency on JDK serialization, so the record no longer needs to implement Serializable. entryTtl
    gives every entry a bounded lifetime sourced from configuration. computePrefixWith puts an
    externalized application and environment prefix and a cache schema version in front of every key, so
    two deployments sharing a Redis instance and two application versions during a rolling release write
    to disjoint key spaces. disableCachingNullValues preserves the existing behaviour in which a missing
    item raises ResourceNotFoundException before any cache write.
  discovery_required_reason: null
  unresolved_inputs:
    - Approved inventory cache time-to-live value
    - Source of the environment qualifier that forms part of app.cache.key-prefix
```

### ICB-015-02: Cache contract properties

```yaml
change_id: CHANGE-AA-015
block_id: ICB-015-02
target:
  repository_path: source/inventory-service/src/main/resources/application.yml
  symbol: spring.cache and app.cache
  source_fingerprint:
    algorithm: sha256
    value: "5921b25eb1c9acfac5e43cb0c833f6ea37f042b0ee97ebe1c05de562013e3bee"
  original_line_range: {start_line: 16, end_line: 17, status: advisory}
  line_numbers_authoritative: false
current_implementation:
  evidence_id: EV-F-017-01
  original_source_excerpt: |
      cache:
        type: redis
proposed_implementation:
  illustrative_code_status: generated
  source_language: yaml
  target_repository_path: source/inventory-service/src/main/resources/application.yml
  target_symbol: spring.cache and app.cache
  replaces_or_updates_evidence_ids: [EV-F-017-01]
  illustrative_code: |
      cache:
        type: redis
    app:
      cache:
        key-prefix: ${CACHE_KEY_PREFIX:inventory-service:local}
        schema-version: v1
        inventory:
          ttl: ${CACHE_INVENTORY_TTL}
  narrative_explanation: >-
    spring.cache.type stays redis. The key prefix carries the application and environment qualifier and
    is supplied at deployment time, the schema version is a repository-owned constant that the team bumps
    when the cached response model changes, and the TTL is an externalized placeholder with no value
    asserted by this plan.
  discovery_required_reason: null
  unresolved_inputs:
    - Approved inventory cache time-to-live value
```

### ICB-016-01: Coalesced cache loading

```yaml
change_id: CHANGE-AA-016
block_id: ICB-016-01
target:
  repository_path: source/inventory-service/src/main/java/com/ecommerce/inventory/service/impl/InventoryServiceImpl.java
  symbol: InventoryServiceImpl.get @Cacheable
  source_fingerprint:
    algorithm: sha256
    value: "af81ef398962c1d6360ab1362e5147578fd509562c148022a7a917a1b3f71ddf"
  original_line_range: {start_line: 30, end_line: 31, status: advisory}
  line_numbers_authoritative: false
current_implementation:
  evidence_id: EV-F-019-01
  original_source_excerpt: |
        @Override @Cacheable(cacheNames = "inventory", key = "#id")
        public InventoryResponse get(Long id) { return mapper.toResponse(find(id)); }
proposed_implementation:
  illustrative_code_status: generated
  source_language: java
  target_repository_path: source/inventory-service/src/main/java/com/ecommerce/inventory/service/impl/InventoryServiceImpl.java
  target_symbol: InventoryServiceImpl.get @Cacheable sync
  replaces_or_updates_evidence_ids: [EV-F-019-01]
  illustrative_code: |
    @Override
    @Cacheable(cacheNames = "inventory", key = "#id", sync = true)
    public InventoryResponse get(Long id) {
        return mapper.toResponse(find(id));
    }
  narrative_explanation: >-
    sync makes the cache abstraction coalesce concurrent loads for the same key, so an empty regional
    cache after a failover or a Redis restart produces one authoritative read per key rather than one per
    request. The cache name, key expression, return type, and method body are unchanged, so the value
    returned to every caller is identical.
  discovery_required_reason: null
  unresolved_inputs: []
```

### ICB-017-01: Bounded list operation

```yaml
change_id: CHANGE-AA-017
block_id: ICB-017-01
target:
  repository_path: source/inventory-service/src/main/java/com/ecommerce/inventory/service/impl/InventoryServiceImpl.java
  symbol: InventoryServiceImpl.list
  source_fingerprint:
    algorithm: sha256
    value: "fa3fa59291d992c50163fa623bfd1535288aedce4ba7a673588ad42b4a49f031"
  original_line_range: {start_line: 32, end_line: 32, status: advisory}
  line_numbers_authoritative: false
current_implementation:
  evidence_id: EV-F-025-01
  original_source_excerpt: |
        @Override public List<InventoryResponse> list() { return repository.findAll().stream().map(mapper::toResponse).toList(); }
proposed_implementation:
  illustrative_code_status: generated
  source_language: java
  target_repository_path: source/inventory-service/src/main/java/com/ecommerce/inventory/service/impl/InventoryServiceImpl.java
  target_symbol: InventoryServiceImpl.list
  replaces_or_updates_evidence_ids: [EV-F-025-01]
  illustrative_code: |
    @Override
    public Page<InventoryResponse> list(Pageable pageable) {
        return repository.findAll(pageable).map(mapper::toResponse);
    }
  narrative_explanation: >-
    findAll(Pageable) is already available on the existing JpaRepository, so no repository change is
    needed. Page.map applies the existing mapper, so the element shape is unchanged. Peak allocation
    becomes a function of the page size rather than of the table size. The interface method in
    InventoryService changes signature accordingly.
  discovery_required_reason: null
  unresolved_inputs: []
```

### ICB-017-02: Page size bounds and controller binding

```yaml
change_id: CHANGE-AA-017
block_id: ICB-017-02
target:
  repository_path: source/inventory-service/src/main/java/com/ecommerce/inventory/controller/InventoryController.java
  symbol: InventoryController.list
  source_fingerprint:
    algorithm: sha256
    value: not_available
  original_line_range: {start_line: 19, end_line: 19, status: advisory}
  line_numbers_authoritative: false
current_implementation:
  evidence_id: EV-F-025-01
  evidence_note: >-
    Step 2 anchored this finding on InventoryServiceImpl.list. The controller method that exposes it is
    cited by the Step 1 inventory under InventoryController with an advisory line range and has no Step 2
    excerpt, so no excerpt is reproduced here.
proposed_implementation:
  illustrative_code_status: generated
  source_language: yaml
  target_repository_path: source/inventory-service/src/main/resources/application.yml
  target_symbol: spring.data.web.pageable
  replaces_or_updates_evidence_ids: [EV-F-025-01]
  illustrative_code: |
    spring:
      data:
        web:
          pageable:
            default-page-size: ${INVENTORY_PAGE_SIZE_DEFAULT}
            max-page-size: ${INVENTORY_PAGE_SIZE_MAX}
            one-indexed-parameters: false
  narrative_explanation: >-
    Spring Data web support caps the requested page size at max-page-size, so a caller cannot defeat the
    bound by asking for a very large page. Both values are externalized. The corresponding controller
    signature change from List<InventoryResponse> to Page<InventoryResponse> is the approval-gated part
    of this change and is not applied until the API contract owner approves the response shape.
  discovery_required_reason: null
  unresolved_inputs:
    - Approved pagination contract for GET /api/v1/inventory, including response shape and default and maximum page size
```

### ICB-018-01: Observed publication outcome

```yaml
change_id: CHANGE-AA-018
block_id: ICB-018-01
target:
  repository_path: source/inventory-service/src/main/java/com/ecommerce/inventory/kafka/producer/InventoryEventProducer.java
  symbol: InventoryEventProducer.publish
  source_fingerprint:
    algorithm: sha256
    value: "c77eedf9776fd6bdfbd13ff41642bb1f00ae2767f58bba7c495f40b6dbc8ce8f"
  original_line_range: {start_line: 14, end_line: 16, status: advisory}
  line_numbers_authoritative: false
current_implementation:
  evidence_id: EV-F-001-01
  original_source_excerpt: |
        public void publish(String type, InventoryResponse inventory, String referenceId) {
            kafkaTemplate.send("inventory-events", inventory.productId(), Map.of("type", type, "occurredAt", Instant.now().toString(), "referenceId", referenceId == null ? "" : referenceId, "inventory", inventory));
        }
proposed_implementation:
  illustrative_code_status: generated
  source_language: java
  target_repository_path: source/inventory-service/src/main/java/com/ecommerce/inventory/kafka/producer/InventoryEventProducer.java
  target_symbol: InventoryEventProducer.publish
  replaces_or_updates_evidence_ids: [EV-F-001-01]
  illustrative_code: |
    public void publish(String type, InventoryResponse inventory, String referenceId) {
        String key = inventory.productId();
        Map<String, Object> payload = Map.of(
                "type", type,
                "occurredAt", Instant.now().toString(),
                "referenceId", referenceId == null ? "" : referenceId,
                "inventory", inventory);

        kafkaTemplate.send(TOPIC, key, payload).whenComplete((result, failure) -> {
            if (failure == null) {
                telemetry.recordPublication(type, InventoryTelemetry.OUTCOME_SUCCESS);
            } else {
                telemetry.recordPublication(type, InventoryTelemetry.OUTCOME_FAILURE);
                log.error("inventory event publication failed topic={} key={} eventType={} exception={}",
                        TOPIC, key, type, failure.getClass().getName(), failure);
            }
        });
    }
  narrative_explanation: >-
    The returned future is observed instead of discarded. Success and failure each produce exactly one
    counter increment, and a failure produces one structured log record naming the topic, the record key,
    and the exception class. The payload is not logged. The topic name, the record key, and the payload
    shape are unchanged by this change; the envelope contract change belongs to CHANGE-AA-022. The
    literal topic name is lifted to a constant so CHANGE-AA-019 and CHANGE-AA-021 can reference it.
  discovery_required_reason: null
  unresolved_inputs: []
```

### ICB-018-02: Producer durability settings

```yaml
change_id: CHANGE-AA-018
block_id: ICB-018-02
target:
  repository_path: source/inventory-service/src/main/resources/application.yml
  symbol: spring.kafka.producer
  source_fingerprint:
    algorithm: sha256
    value: "825e9b9cd362296fb3cc671568f190b240d2240909ad86c9e2d6799014bfbcca"
  original_line_range: {start_line: 26, end_line: 28, status: advisory}
  line_numbers_authoritative: false
current_implementation:
  evidence_id: EV-F-001-02
  original_source_excerpt: |
        producer:
          key-serializer: org.apache.kafka.common.serialization.StringSerializer
          value-serializer: org.springframework.kafka.support.serializer.JsonSerializer
proposed_implementation:
  illustrative_code_status: generated
  source_language: yaml
  target_repository_path: source/inventory-service/src/main/resources/application.yml
  target_symbol: spring.kafka.producer
  replaces_or_updates_evidence_ids: [EV-F-001-02]
  illustrative_code: |
        producer:
          key-serializer: org.apache.kafka.common.serialization.StringSerializer
          value-serializer: org.springframework.kafka.support.serializer.JsonSerializer
          acks: ${KAFKA_PRODUCER_ACKS}
          retries: ${KAFKA_PRODUCER_RETRIES}
          properties:
            enable.idempotence: ${KAFKA_PRODUCER_ENABLE_IDEMPOTENCE}
            max.in.flight.requests.per.connection: ${KAFKA_PRODUCER_MAX_IN_FLIGHT}
  narrative_explanation: >-
    The existing serializers are preserved. Durability settings become explicit and deployment tunable
    rather than implicit client defaults. No value is hardcoded, because the safe setting for acks
    depends on the broker-side min.insync.replicas and replication factor recorded as EG-002, which is
    outside the remediation boundary. The timeout properties for this producer are declared in ICB-009-01.
  discovery_required_reason: null
  unresolved_inputs:
    - Approved acks, idempotence, and in-flight settings, which depend on broker replication configuration from EG-002
```

### ICB-019-01: Listener container factory with bounded error handling

```yaml
change_id: CHANGE-AA-019
block_id: ICB-019-01
target:
  repository_path: source/inventory-service/src/main/java/com/ecommerce/inventory/kafka/KafkaConsumerConfig.java
  symbol: KafkaConsumerConfig.orderEventListenerContainerFactory
  target_status: new_file
current_implementation:
  evidence_id: EV-F-005-01
  original_source_excerpt: |
      kafka:
        bootstrap-servers: ${KAFKA_BOOTSTRAP_SERVERS:localhost:9092}
        consumer:
          auto-offset-reset: earliest
          key-deserializer: org.apache.kafka.common.serialization.StringDeserializer
          value-deserializer: org.springframework.kafka.support.serializer.JsonDeserializer
          properties:
            spring.json.trusted.packages: "*"
        producer:
          key-serializer: org.apache.kafka.common.serialization.StringSerializer
          value-serializer: org.springframework.kafka.support.serializer.JsonSerializer
proposed_implementation:
  illustrative_code_status: generated
  source_language: java
  target_repository_path: source/inventory-service/src/main/java/com/ecommerce/inventory/kafka/KafkaConsumerConfig.java
  target_symbol: KafkaConsumerConfig
  replaces_or_updates_evidence_ids: [EV-F-005-01]
  illustrative_code: |
    package com.ecommerce.inventory.kafka;

    import com.ecommerce.inventory.kafka.consumer.NonRetryablePayloadException;
    import com.ecommerce.inventory.observability.InventoryTelemetry;
    import lombok.extern.slf4j.Slf4j;
    import org.apache.kafka.clients.consumer.ConsumerRecord;
    import org.springframework.beans.factory.annotation.Value;
    import org.springframework.context.annotation.Bean;
    import org.springframework.context.annotation.Configuration;
    import org.springframework.kafka.config.ConcurrentKafkaListenerContainerFactory;
    import org.springframework.kafka.core.ConsumerFactory;
    import org.springframework.kafka.core.KafkaTemplate;
    import org.springframework.kafka.listener.ContainerProperties;
    import org.springframework.kafka.listener.DeadLetterPublishingRecoverer;
    import org.springframework.kafka.listener.DefaultErrorHandler;
    import org.springframework.util.backoff.ExponentialBackOff;
    import org.apache.kafka.common.TopicPartition;

    import java.util.Map;

    @Slf4j
    @Configuration
    public class KafkaConsumerConfig {

        @Bean
        public ConcurrentKafkaListenerContainerFactory<String, Map<String, Object>> orderEventListenerContainerFactory(
                ConsumerFactory<String, Map<String, Object>> consumerFactory,
                DefaultErrorHandler orderEventErrorHandler) {

            ConcurrentKafkaListenerContainerFactory<String, Map<String, Object>> factory =
                    new ConcurrentKafkaListenerContainerFactory<>();
            factory.setConsumerFactory(consumerFactory);
            factory.setCommonErrorHandler(orderEventErrorHandler);
            factory.getContainerProperties().setAckMode(ContainerProperties.AckMode.MANUAL_IMMEDIATE);
            return factory;
        }

        @Bean
        public DefaultErrorHandler orderEventErrorHandler(
                KafkaTemplate<String, Object> kafkaTemplate,
                InventoryTelemetry telemetry,
                @Value("${app.kafka.consumer.dead-letter-topic}") String deadLetterTopic,
                @Value("${app.kafka.consumer.max-attempts}") int maxAttempts,
                @Value("${app.kafka.consumer.backoff-initial-interval}") long initialInterval,
                @Value("${app.kafka.consumer.backoff-multiplier}") double multiplier,
                @Value("${app.kafka.consumer.backoff-max-interval}") long maxInterval) {

            DeadLetterPublishingRecoverer recoverer = new DeadLetterPublishingRecoverer(kafkaTemplate,
                    (record, exception) -> new TopicPartition(deadLetterTopic, record.partition()));

            ExponentialBackOff backOff = new ExponentialBackOff(initialInterval, multiplier);
            backOff.setMaxInterval(maxInterval);
            backOff.setMaxAttempts(maxAttempts);

            DefaultErrorHandler errorHandler = new DefaultErrorHandler((record, exception) -> {
                recoverer.accept((ConsumerRecord<?, ?>) record, exception);
                telemetry.recordConsumption("order-events", InventoryTelemetry.OUTCOME_QUARANTINED);
                log.error("order event quarantined topic={} partition={} offset={} exception={}",
                        record.topic(), record.partition(), record.offset(), exception.getClass().getName());
            }, backOff);

            errorHandler.addNotRetryableExceptions(NonRetryablePayloadException.class, IllegalArgumentException.class);
            return errorHandler;
        }
    }
  narrative_explanation: >-
    Manual immediate acknowledgment moves offset advancement under the listener's control, so the offset
    no longer advances as a side effect of an exhausted implicit attempt budget. The attempt count and the
    exponential backoff are externalized, so no retry is immediate. Structurally invalid payloads and
    business validation failures are declared non-retryable so they are quarantined on the first attempt
    without consuming the budget. The recoverer publishes to an externally named dead-letter destination
    using the KafkaTemplate that is already a bean in this application, and each quarantine produces one
    counter increment and one log record with no payload content.
  discovery_required_reason: null
  unresolved_inputs:
    - Approved dead-letter destination name, retention, and access policy
```

### ICB-019-02: Guarded payload extraction

```yaml
change_id: CHANGE-AA-019
block_id: ICB-019-02
target:
  repository_path: source/inventory-service/src/main/java/com/ecommerce/inventory/kafka/consumer/OrderEventPayload.java
  symbol: OrderEventPayload
  target_status: new_file
current_implementation:
  evidence_id: EV-F-006-01
  original_source_excerpt: |
        public void consume(Map<String, Object> event) {
            String type = String.valueOf(event.get("type"));
            String productId = String.valueOf(event.get("productId"));
            int quantity = ((Number) event.get("quantity")).intValue();
            String orderId = String.valueOf(event.get("orderId"));
proposed_implementation:
  illustrative_code_status: generated
  source_language: java
  target_repository_path: source/inventory-service/src/main/java/com/ecommerce/inventory/kafka/consumer/OrderEventPayload.java
  target_symbol: OrderEventPayload.from
  replaces_or_updates_evidence_ids: [EV-F-006-01]
  illustrative_code: |
    package com.ecommerce.inventory.kafka.consumer;

    import java.util.Map;

    public record OrderEventPayload(String type, String productId, int quantity, String orderId) {

        public static OrderEventPayload from(Map<String, Object> event) {
            return new OrderEventPayload(
                    requiredText(event, "type"),
                    requiredText(event, "productId"),
                    requiredQuantity(event),
                    requiredText(event, "orderId"));
        }

        private static String requiredText(Map<String, Object> event, String field) {
            Object value = event.get(field);
            if (value == null || String.valueOf(value).isBlank()) {
                throw new NonRetryablePayloadException("Order event is missing required field " + field);
            }
            return String.valueOf(value);
        }

        private static int requiredQuantity(Map<String, Object> event) {
            Object value = event.get("quantity");
            if (!(value instanceof Number number)) {
                throw new NonRetryablePayloadException("Order event quantity is missing or is not numeric");
            }
            return number.intValue();
        }
    }
  narrative_explanation: >-
    Extraction produces a typed record with the same four fields the current code reads, in the same
    order, with the same names. A missing field or a non-numeric quantity now raises a classified
    non-retryable failure instead of a NullPointerException or a ClassCastException, so the error handler
    can quarantine the record immediately with a diagnostic artifact. The record type follows the
    existing DTO convention in this repository, which already uses Java records for InventoryResponse and
    StockAdjustmentRequest. The exception message contains no payload values.
  discovery_required_reason: null
  unresolved_inputs: []
```

### ICB-019-03: Non-retryable payload exception

```yaml
change_id: CHANGE-AA-019
block_id: ICB-019-03
target:
  repository_path: source/inventory-service/src/main/java/com/ecommerce/inventory/kafka/consumer/NonRetryablePayloadException.java
  symbol: NonRetryablePayloadException
  target_status: new_file
current_implementation:
  evidence_id: EV-F-006-01
  evidence_note: >-
    No classified payload exception exists; extraction failures surface as NullPointerException or
    ClassCastException.
proposed_implementation:
  illustrative_code_status: generated
  source_language: java
  target_repository_path: source/inventory-service/src/main/java/com/ecommerce/inventory/kafka/consumer/NonRetryablePayloadException.java
  target_symbol: NonRetryablePayloadException
  replaces_or_updates_evidence_ids: [EV-F-006-01]
  illustrative_code: |
    package com.ecommerce.inventory.kafka.consumer;

    public class NonRetryablePayloadException extends RuntimeException {

        public NonRetryablePayloadException(String message) {
            super(message);
        }
    }
  narrative_explanation: >-
    A dedicated unchecked exception in the same style as the existing ResourceNotFoundException. It is
    registered with the error handler as non-retryable so a structurally invalid record is quarantined on
    the first attempt.
  discovery_required_reason: null
  unresolved_inputs: []
```

### ICB-019-04: Listener error-handling properties

```yaml
change_id: CHANGE-AA-019
block_id: ICB-019-04
target:
  repository_path: source/inventory-service/src/main/resources/application.yml
  symbol: spring.kafka.listener and app.kafka.consumer
  source_fingerprint:
    algorithm: sha256
    value: "d249f7885663c10bfb25cac5530b32e398241519f204cdb12008192b9decfbbb"
  original_line_range: {start_line: 18, end_line: 28, status: advisory}
  line_numbers_authoritative: false
current_implementation:
  evidence_id: EV-F-005-01
  evidence_note: >-
    The excerpt is preserved verbatim in ICB-019-01 and is not duplicated here. No ack-mode, error
    handler, or dead-letter property exists.
proposed_implementation:
  illustrative_code_status: generated
  source_language: yaml
  target_repository_path: source/inventory-service/src/main/resources/application.yml
  target_symbol: spring.kafka.listener and app.kafka.consumer
  replaces_or_updates_evidence_ids: [EV-F-005-01]
  illustrative_code: |
    spring:
      kafka:
        listener:
          ack-mode: manual_immediate
    app:
      kafka:
        consumer:
          enabled: ${KAFKA_CONSUMER_ENABLED:true}
          listener-id: order-events-listener
          dead-letter-topic: ${KAFKA_ORDER_EVENTS_DLT}
          max-attempts: ${KAFKA_CONSUMER_MAX_ATTEMPTS}
          backoff-initial-interval: ${KAFKA_CONSUMER_BACKOFF_INITIAL_MS}
          backoff-multiplier: ${KAFKA_CONSUMER_BACKOFF_MULTIPLIER}
          backoff-max-interval: ${KAFKA_CONSUMER_BACKOFF_MAX_MS}
  narrative_explanation: >-
    The activation property from CHANGE-AA-007 and the error-handling properties from this change share
    the app.kafka.consumer prefix because they configure the same listener. The dead-letter destination
    name is supplied at deployment time so no topic name is fixed in the repository. Attempt count and
    backoff are externalized placeholders with no asserted values. The existing consumer serializers,
    auto-offset-reset, and trusted-packages settings are unchanged by this block.
  discovery_required_reason: null
  unresolved_inputs:
    - Approved dead-letter destination name and the attempt and backoff budget
```

### ICB-020-01: Key Vault property source refresh

```yaml
change_id: CHANGE-AA-020
block_id: ICB-020-01
target:
  repository_path: source/inventory-service/src/main/resources/application-prod.yml
  symbol: spring.cloud.azure.keyvault.secret.property-sources
  source_fingerprint:
    algorithm: sha256
    value: "e7c1e56e4046bbfc9fcf5c3a01e365fb206b1f607e3db7809765093a706a1915"
  original_line_range: {start_line: 1, end_line: 3, status: advisory}
  line_numbers_authoritative: false
current_implementation:
  evidence_id: EV-F-023-01
  original_source_excerpt: |
    spring:
      config:
        import: azure-keyvault:${AZURE_KEYVAULT_ENDPOINT}
proposed_implementation:
  illustrative_code_status: generated
  source_language: yaml
  target_repository_path: source/inventory-service/src/main/resources/application-prod.yml
  target_symbol: spring.cloud.azure.keyvault.secret.property-sources
  replaces_or_updates_evidence_ids: [EV-F-023-01]
  illustrative_code: |
    spring:
      cloud:
        azure:
          keyvault:
            secret:
              property-sources:
                - name: inventory-secrets
                  endpoint: ${AZURE_KEYVAULT_ENDPOINT}
                  refresh-interval: ${KEYVAULT_REFRESH_INTERVAL}
    app:
      secrets:
        rotation:
          enabled: ${SECRET_ROTATION_ENABLED:false}
          pool-eviction-enabled: ${SECRET_POOL_EVICTION_ENABLED:false}
  narrative_explanation: >-
    The declared Spring Cloud Azure starter supports a property-source refresh interval, so the reload is
    a supported capability of an existing dependency rather than a new mechanism. The refresh interval and
    both rotation behaviours are externalized, and both rotation flags default to false so the change is
    inert until a deployment opts in.
  discovery_required_reason: null
  unresolved_inputs:
    - Approved refresh interval, bounded by the Key Vault client retry budget from CHANGE-AA-003
```

### ICB-020-02: Datasource credential rotation handling

```yaml
change_id: CHANGE-AA-020
block_id: ICB-020-02
target:
  repository_path: source/inventory-service/src/main/java/com/ecommerce/inventory/config/SecretRotationHandler.java
  symbol: SecretRotationHandler
  target_status: new_file
current_implementation:
  evidence_id: EV-F-023-01
  evidence_note: >-
    The HikariCP datasource is initialized once with startup material and no client-recreation path
    exists.
proposed_implementation:
  illustrative_code_status: generated
  source_language: java
  target_repository_path: source/inventory-service/src/main/java/com/ecommerce/inventory/config/SecretRotationHandler.java
  target_symbol: SecretRotationHandler
  replaces_or_updates_evidence_ids: [EV-F-023-01]
  illustrative_code: |
    package com.ecommerce.inventory.config;

    import com.ecommerce.inventory.observability.InventoryTelemetry;
    import com.zaxxer.hikari.HikariDataSource;
    import lombok.extern.slf4j.Slf4j;
    import org.springframework.beans.factory.annotation.Value;
    import org.springframework.boot.context.properties.ConfigurationPropertiesBinding;
    import org.springframework.core.env.Environment;
    import org.springframework.scheduling.annotation.Scheduled;
    import org.springframework.stereotype.Component;

    import javax.sql.DataSource;
    import java.util.Objects;

    @Slf4j
    @Component
    public class SecretRotationHandler {

        private final DataSource dataSource;
        private final Environment environment;
        private final InventoryTelemetry telemetry;
        private final boolean poolEvictionEnabled;
        private volatile String lastObservedPassword;

        public SecretRotationHandler(DataSource dataSource,
                                     Environment environment,
                                     InventoryTelemetry telemetry,
                                     @Value("${app.secrets.rotation.pool-eviction-enabled:false}") boolean poolEvictionEnabled) {
            this.dataSource = dataSource;
            this.environment = environment;
            this.telemetry = telemetry;
            this.poolEvictionEnabled = poolEvictionEnabled;
            this.lastObservedPassword = environment.getProperty("spring.datasource.password");
        }

        @Scheduled(fixedDelayString = "${app.secrets.rotation.check-interval}")
        public void applyRotationIfChanged() {
            if (!poolEvictionEnabled || !(dataSource instanceof HikariDataSource hikari)) {
                return;
            }
            String current = environment.getProperty("spring.datasource.password");
            if (Objects.equals(current, lastObservedPassword)) {
                return;
            }
            lastObservedPassword = current;
            hikari.getHikariConfigMXBean().setPassword(current);
            hikari.getHikariPoolMXBean().softEvictConnections();
            telemetry.recordCredentialRotation("datasource");
            log.info("credential rotation applied target=datasource action=soft_evict");
        }
    }
  narrative_explanation: >-
    HikariCP exposes a supported runtime password update through HikariConfigMXBean and a non-disruptive
    connection turnover through softEvictConnections, so the datasource converges on rotated material
    without a process restart and without dropping in-flight work. The handler compares the refreshed
    property value rather than reacting to a failure, so it is proactive and does not depend on an
    authentication error occurring first. The whole path is gated behind an externalized flag that
    defaults to false. No secret value is logged or recorded as a metric tag.
  discovery_required_reason: null
  unresolved_inputs:
    - Whether the approved rotation model updates the password property or replaces the whole connection string
```

### ICB-020-03: Redis client re-initialization on rotation

```yaml
change_id: CHANGE-AA-020
block_id: ICB-020-03
target:
  repository_path: not_yet_selected
  symbol: Redis connection factory re-initialization
  target_status: new_file
current_implementation:
  evidence_id: EV-F-023-01
  evidence_note: >-
    The Lettuce connection factory is initialized once with startup material and retains it for the
    lifetime of the process.
proposed_implementation:
  illustrative_code_status: targeted_discovery_required
  source_language: java
  target_repository_path: not_yet_selected
  target_symbol: Redis connection factory re-initialization
  replaces_or_updates_evidence_ids: [EV-F-023-01]
  illustrative_code: null
  narrative_explanation: >-
    On a rotated Redis access key the connection factory would need to pick up the new credential and
    re-establish connections without a process restart.
  discovery_required_reason: >-
    Production Redis credentials and the TLS scheme are contained inside the externally supplied
    REDIS_CONNECTION_STRING value, which EG-003 records as outside repository evidence. Whether the
    rotated material arrives as a new password within the same URL, as an entirely new URL, or as a
    managed-identity token determines whether a credential update, a full client re-creation, or a
    token-refresh hook is the correct mechanism. Choosing one without that fact would invent an
    unverifiable client lifecycle.
  unresolved_inputs:
    - Resolved REDIS_CONNECTION_STRING scheme and authentication mode per region, carried from EG-003
    - Whether Redis authentication uses an access key or a managed identity token
```

### ICB-021-01: Outbox record entity

```yaml
change_id: CHANGE-AA-021
block_id: ICB-021-01
target:
  repository_path: source/inventory-service/src/main/java/com/ecommerce/inventory/outbox/OutboxRecord.java
  symbol: OutboxRecord
  target_status: new_file
current_implementation:
  evidence_id: EV-F-002-01
  original_source_excerpt: |
        private InventoryResponse saveAndPublish(InventoryItem item, String type, String referenceId) { InventoryResponse response = mapper.toResponse(repository.save(item)); producer.publish(type, response, referenceId); return response; }
proposed_implementation:
  illustrative_code_status: generated
  source_language: java
  target_repository_path: source/inventory-service/src/main/java/com/ecommerce/inventory/outbox/OutboxRecord.java
  target_symbol: OutboxRecord
  replaces_or_updates_evidence_ids: [EV-F-002-01]
  illustrative_code: |
    package com.ecommerce.inventory.outbox;

    import jakarta.persistence.Column;
    import jakarta.persistence.Entity;
    import jakarta.persistence.EnumType;
    import jakarta.persistence.Enumerated;
    import jakarta.persistence.GeneratedValue;
    import jakarta.persistence.GenerationType;
    import jakarta.persistence.Id;
    import jakarta.persistence.Lob;
    import jakarta.persistence.Table;
    import lombok.AllArgsConstructor;
    import lombok.Builder;
    import lombok.Data;
    import lombok.NoArgsConstructor;

    import java.time.Instant;

    @Entity
    @Table(name = "inventory_event_outbox")
    @Data @Builder @NoArgsConstructor @AllArgsConstructor
    public class OutboxRecord {

        public enum Status { PENDING, PUBLISHED, FAILED }

        @Id @GeneratedValue(strategy = GenerationType.IDENTITY) private Long id;
        @Column(nullable = false, length = 64) private String eventType;
        @Column(nullable = false, length = 255) private String aggregateKey;
        @Column(nullable = false, length = 255) private String referenceId;
        @Lob @Column(nullable = false) private String payload;
        @Enumerated(EnumType.STRING) @Column(nullable = false, length = 16) private Status status;
        @Column(nullable = false) private int attemptCount;
        @Column(nullable = false) private Instant createdAt;
        private Instant publishedAt;
        private String lastError;
    }
  narrative_explanation: >-
    The entity follows the same Lombok and JPA conventions as InventoryItem and ProcessedOperation. It
    records the durable intent, the aggregate key that becomes the Kafka record key, an explicit terminal
    status, and an attempt count, which together give recovery a queryable basis for detecting and
    repairing divergence. lastError holds the exception class and message so a stuck record can be
    diagnosed without correlating logs.
  discovery_required_reason: null
  unresolved_inputs: []
```

### ICB-021-02: Outbox repository

```yaml
change_id: CHANGE-AA-021
block_id: ICB-021-02
target:
  repository_path: source/inventory-service/src/main/java/com/ecommerce/inventory/outbox/OutboxRepository.java
  symbol: OutboxRepository
  target_status: new_file
current_implementation:
  evidence_id: EV-F-002-01
  evidence_note: No outbox repository exists; the only repository is InventoryRepository.
proposed_implementation:
  illustrative_code_status: generated
  source_language: java
  target_repository_path: source/inventory-service/src/main/java/com/ecommerce/inventory/outbox/OutboxRepository.java
  target_symbol: OutboxRepository
  replaces_or_updates_evidence_ids: [EV-F-002-01]
  illustrative_code: |
    package com.ecommerce.inventory.outbox;

    import org.springframework.data.domain.Limit;
    import org.springframework.data.jpa.repository.JpaRepository;

    import java.util.List;

    public interface OutboxRepository extends JpaRepository<OutboxRecord, Long> {
        List<OutboxRecord> findByStatusOrderByCreatedAtAsc(OutboxRecord.Status status, Limit limit);
    }
  narrative_explanation: >-
    A derived query in the same style as the existing findByProductId method. Ordering by creation time
    preserves per-aggregate publication order, and the Limit bounds each relay batch so a large backlog
    cannot be materialized in one read.
  discovery_required_reason: null
  unresolved_inputs: []
```

### ICB-021-03: Commit-ordered relay

```yaml
change_id: CHANGE-AA-021
block_id: ICB-021-03
target:
  repository_path: source/inventory-service/src/main/java/com/ecommerce/inventory/outbox/OutboxRelay.java
  symbol: OutboxRelay
  target_status: new_file
current_implementation:
  evidence_id: EV-F-002-02
  original_source_excerpt: |
        @Override @Transactional @CacheEvict(cacheNames = "inventory", key = "#id")
        public void delete(Long id) { InventoryItem item = find(id); repository.delete(item); producer.publish("INVENTORY_DELETED", mapper.toResponse(item), ""); }
proposed_implementation:
  illustrative_code_status: generated
  source_language: java
  target_repository_path: source/inventory-service/src/main/java/com/ecommerce/inventory/outbox/OutboxRelay.java
  target_symbol: OutboxRelay.publishPending
  replaces_or_updates_evidence_ids: [EV-F-002-02]
  illustrative_code: |
    package com.ecommerce.inventory.outbox;

    import com.ecommerce.inventory.observability.InventoryTelemetry;
    import lombok.extern.slf4j.Slf4j;
    import org.springframework.beans.factory.annotation.Value;
    import org.springframework.boot.autoconfigure.condition.ConditionalOnProperty;
    import org.springframework.data.domain.Limit;
    import org.springframework.kafka.core.KafkaTemplate;
    import org.springframework.scheduling.annotation.Scheduled;
    import org.springframework.stereotype.Component;
    import org.springframework.transaction.annotation.Transactional;

    import java.time.Instant;
    import java.util.List;

    @Slf4j
    @Component
    @ConditionalOnProperty(name = "app.outbox.relay.enabled", havingValue = "true")
    public class OutboxRelay {

        private final OutboxRepository outbox;
        private final KafkaTemplate<String, Object> kafkaTemplate;
        private final InventoryTelemetry telemetry;
        private final String topic;
        private final int batchSize;
        private final int maxAttempts;

        public OutboxRelay(OutboxRepository outbox,
                           KafkaTemplate<String, Object> kafkaTemplate,
                           InventoryTelemetry telemetry,
                           @Value("${app.outbox.topic:inventory-events}") String topic,
                           @Value("${app.outbox.relay.batch-size}") int batchSize,
                           @Value("${app.outbox.relay.max-attempts}") int maxAttempts) {
            this.outbox = outbox;
            this.kafkaTemplate = kafkaTemplate;
            this.telemetry = telemetry;
            this.topic = topic;
            this.batchSize = batchSize;
            this.maxAttempts = maxAttempts;
        }

        @Scheduled(fixedDelayString = "${app.outbox.relay.poll-interval}")
        @Transactional
        public void publishPending() {
            List<OutboxRecord> pending =
                    outbox.findByStatusOrderByCreatedAtAsc(OutboxRecord.Status.PENDING, Limit.of(batchSize));

            for (OutboxRecord record : pending) {
                try {
                    kafkaTemplate.send(topic, record.getAggregateKey(), record.getPayload()).join();
                    record.setStatus(OutboxRecord.Status.PUBLISHED);
                    record.setPublishedAt(Instant.now());
                    telemetry.recordPublication(record.getEventType(), InventoryTelemetry.OUTCOME_SUCCESS);
                } catch (RuntimeException failure) {
                    record.setAttemptCount(record.getAttemptCount() + 1);
                    record.setLastError(failure.getClass().getName());
                    if (record.getAttemptCount() >= maxAttempts) {
                        record.setStatus(OutboxRecord.Status.FAILED);
                    }
                    telemetry.recordPublication(record.getEventType(), InventoryTelemetry.OUTCOME_FAILURE);
                    log.error("outbox publication failed outboxId={} attempt={} exception={}",
                            record.getId(), record.getAttemptCount(), failure.getClass().getName(), failure);
                }
            }
        }
    }
  narrative_explanation: >-
    The relay runs outside any business transaction and marks a record published only after the send
    completes, so a rolled-back business transaction leaves no record to publish and a publication
    failure leaves the record recoverable. Exhausting the attempt budget moves the record to an explicit
    FAILED status rather than silently dropping it. The relay is conditional on an externalized property
    so its regional activation follows the same contract as the listener in CHANGE-AA-007, which is what
    keeps a single region publishing under the approved single-active model.
  discovery_required_reason: null
  unresolved_inputs:
    - Approved relay execution model, including whether it runs in-process or as a separate component
    - Approved outbox retention and purge policy
```

### ICB-021-04: Outbox migration script

```yaml
change_id: CHANGE-AA-021
block_id: ICB-021-04
target:
  repository_path: source/inventory-service/src/main/resources/db/migration/V3__outbox.sql
  symbol: inventory_event_outbox
  target_status: new_file
current_implementation:
  evidence_id: EV-F-002-01
  evidence_note: No outbox table exists in the assessed schema.
proposed_implementation:
  illustrative_code_status: generated
  source_language: sql
  target_repository_path: source/inventory-service/src/main/resources/db/migration/V3__outbox.sql
  target_symbol: inventory_event_outbox
  replaces_or_updates_evidence_ids: [EV-F-002-01]
  illustrative_code: |
    CREATE TABLE inventory_event_outbox (
        id           BIGINT IDENTITY(1,1) NOT NULL,
        eventType    VARCHAR(64)          NOT NULL,
        aggregateKey VARCHAR(255)         NOT NULL,
        referenceId  VARCHAR(255)         NOT NULL,
        payload      NVARCHAR(MAX)        NOT NULL,
        status       VARCHAR(16)          NOT NULL,
        attemptCount INT                  NOT NULL CONSTRAINT DF_outbox_attemptCount DEFAULT 0,
        createdAt    DATETIME2            NOT NULL,
        publishedAt  DATETIME2            NULL,
        lastError    VARCHAR(512)         NULL,
        CONSTRAINT PK_inventory_event_outbox PRIMARY KEY (id)
    );

    CREATE INDEX IX_outbox_status_createdAt ON inventory_event_outbox (status, createdAt);
  narrative_explanation: >-
    The composite index on status and creation time supports the relay query directly, so a large
    published backlog does not slow the scan for pending records. The table lives in the Azure SQL
    authoritative store the approved architecture already declares, so no new datastore is introduced.
  discovery_required_reason: null
  unresolved_inputs:
    - Approved retention and purge policy for published and failed outbox records
```

### ICB-022-01: Event envelope with stable identity

```yaml
change_id: CHANGE-AA-022
block_id: ICB-022-01
target:
  repository_path: source/inventory-service/src/main/java/com/ecommerce/inventory/kafka/producer/InventoryEventEnvelope.java
  symbol: InventoryEventEnvelope
  target_status: new_file
current_implementation:
  evidence_id: EV-F-007-01
  original_source_excerpt: |
            kafkaTemplate.send("inventory-events", inventory.productId(), Map.of("type", type, "occurredAt", Instant.now().toString(), "referenceId", referenceId == null ? "" : referenceId, "inventory", inventory));
proposed_implementation:
  illustrative_code_status: generated
  source_language: java
  target_repository_path: source/inventory-service/src/main/java/com/ecommerce/inventory/kafka/producer/InventoryEventEnvelope.java
  target_symbol: InventoryEventEnvelope
  replaces_or_updates_evidence_ids: [EV-F-007-01]
  illustrative_code: |
    package com.ecommerce.inventory.kafka.producer;

    import com.ecommerce.inventory.dto.InventoryResponse;

    import java.time.Instant;

    public record InventoryEventEnvelope(
            String eventId,
            String type,
            String schemaVersion,
            String region,
            String correlationId,
            String referenceId,
            Instant occurredAt,
            InventoryResponse inventory) {

        public static String eventId(String type, String productId, String referenceId) {
            return type + ':' + productId + ':' + referenceId;
        }
    }
  narrative_explanation: >-
    The envelope preserves the four fields the current payload carries and adds the identity, schema
    version, region, and correlation dimensions. eventId is derived from the same components as the
    operation identity in CHANGE-AA-008, so republication of the same business operation produces an
    identical identifier and a downstream consumer can deduplicate. occurredAt becomes a supplied
    business timestamp rather than a per-attempt Instant.now, which is what makes the identifier stable
    across republication. The record shape follows the existing DTO convention in this repository.
  discovery_required_reason: null
  unresolved_inputs:
    - Approved event envelope contract and schema versioning scheme, coordinated with EG-011
```

### ICB-022-02: Identity headers and correlation propagation

```yaml
change_id: CHANGE-AA-022
block_id: ICB-022-02
target:
  repository_path: source/inventory-service/src/main/java/com/ecommerce/inventory/kafka/producer/InventoryEventProducer.java
  symbol: InventoryEventProducer.publish event envelope
  source_fingerprint:
    algorithm: sha256
    value: "03e52ea3ceb6ce1190a0b09ce17bd46427d072dcbc314879c49ee1b24a2e77ac"
  original_line_range: {start_line: 15, end_line: 15, status: advisory}
  line_numbers_authoritative: false
current_implementation:
  evidence_id: EV-F-007-01
  original_source_excerpt: |
            kafkaTemplate.send("inventory-events", inventory.productId(), Map.of("type", type, "occurredAt", Instant.now().toString(), "referenceId", referenceId == null ? "" : referenceId, "inventory", inventory));
proposed_implementation:
  illustrative_code_status: generated
  source_language: java
  target_repository_path: source/inventory-service/src/main/java/com/ecommerce/inventory/kafka/producer/InventoryEventProducer.java
  target_symbol: InventoryEventProducer.publish record headers
  replaces_or_updates_evidence_ids: [EV-F-007-01]
  illustrative_code: |
    public void publish(String type, InventoryResponse inventory, String referenceId, String correlationId) {
        String safeReference = referenceId == null ? "" : referenceId;
        String eventId = InventoryEventEnvelope.eventId(type, inventory.productId(), safeReference);

        InventoryEventEnvelope envelope = new InventoryEventEnvelope(
                eventId, type, schemaVersion, deploymentIdentity.getRegion(),
                correlationId, safeReference, inventory.updatedAt(), inventory);

        ProducerRecord<String, Object> record =
                new ProducerRecord<>(TOPIC, inventory.productId(), envelope);
        record.headers()
                .add(new RecordHeader("eventId", eventId.getBytes(StandardCharsets.UTF_8)))
                .add(new RecordHeader("schemaVersion", schemaVersion.getBytes(StandardCharsets.UTF_8)))
                .add(new RecordHeader("region", deploymentIdentity.getRegion().getBytes(StandardCharsets.UTF_8)))
                .add(new RecordHeader("correlationId", correlationId.getBytes(StandardCharsets.UTF_8)));

        kafkaTemplate.send(record).whenComplete(this::recordOutcome);
    }
  narrative_explanation: >-
    Identity values are written both as envelope fields and as record headers, so a consumer can
    deduplicate without deserializing the payload. occurredAt is taken from the item updatedAt value the
    service already sets on every mutation, which makes it a business timestamp rather than a publication
    timestamp. The region comes from the DeploymentIdentityProperties bean introduced in CHANGE-AA-005.
    The topic name and the record key remain productId, exactly as assessed. No customer, credential, or
    payment field is added.
  discovery_required_reason: null
  unresolved_inputs:
    - Approved event envelope contract and header vocabulary, coordinated with EG-011
```

### ICB-023-01: Cache invalidation on stock adjustment

```yaml
change_id: CHANGE-AA-023
block_id: ICB-023-01
target:
  repository_path: source/inventory-service/src/main/java/com/ecommerce/inventory/service/impl/InventoryServiceImpl.java
  symbol: InventoryServiceImpl.reserve and InventoryServiceImpl.release cache eviction
  source_fingerprint:
    algorithm: sha256
    value: "ce19ccf64430ee1002c885469f8e2155bb45455c2e7a9655269964ac1f59ea97"
  original_line_range: {start_line: 33, end_line: 36, status: advisory}
  line_numbers_authoritative: false
current_implementation:
  evidence_id: EV-F-020-01
  original_source_excerpt: |
        @Override @Transactional @CacheEvict(cacheNames = "inventory", key = "#id")
        public InventoryResponse update(Long id, InventoryRequest request) { InventoryItem item = find(id); mapper.update(request, item); item.setUpdatedAt(Instant.now()); return saveAndPublish(item, "INVENTORY_UPDATED", ""); }
        @Override @Transactional @CacheEvict(cacheNames = "inventory", key = "#id")
        public void delete(Long id) { InventoryItem item = find(id); repository.delete(item); producer.publish("INVENTORY_DELETED", mapper.toResponse(item), ""); }
proposed_implementation:
  illustrative_code_status: generated
  source_language: java
  target_repository_path: source/inventory-service/src/main/java/com/ecommerce/inventory/service/impl/InventoryServiceImpl.java
  target_symbol: InventoryServiceImpl.evictAfterCommit
  replaces_or_updates_evidence_ids: [EV-F-020-01, EV-F-020-02]
  illustrative_code: |
    private void evictAfterCommit(Long itemId) {
        if (!TransactionSynchronizationManager.isSynchronizationActive()) {
            cacheManager.getCache("inventory").evict(itemId);
            return;
        }
        TransactionSynchronizationManager.registerSynchronization(new TransactionSynchronization() {
            @Override
            public void afterCommit() {
                cacheManager.getCache("inventory").evict(itemId);
            }
        });
    }
  narrative_explanation: >-
    The reserve and release paths locate the item by productId but the cache is keyed by the entity id,
    so a declarative @CacheEvict keyed on a method parameter cannot express the correct key. Evicting by
    the resolved entity id inside the operation keeps the id-keyed cache and the productId-keyed mutation
    path aligned. Registering the eviction after commit means a rolled-back adjustment does not discard a
    still-valid entry. An eviction failure is absorbed and counted by the CacheErrorHandler from
    CHANGE-AA-014. The existing @CacheEvict declarations on update and delete are left in place.
  discovery_required_reason: null
  unresolved_inputs: []
```

### ICB-024-01: Duplicate delivery and replay coverage

```yaml
change_id: CHANGE-AA-024
block_id: ICB-024-01
target:
  repository_path: source/inventory-service/src/test/java/com/ecommerce/inventory/resiliency/KafkaFailureIntegrationTest.java
  symbol: KafkaFailureIntegrationTest
  target_status: new_file
current_implementation:
  evidence_id: EV-F-028-01
  original_source_excerpt: |
    @SpringBootTest(properties = "spring.kafka.bootstrap-servers=${spring.embedded.kafka.brokers}")
    @EmbeddedKafka(partitions = 1, topics = {"order-events", "inventory-events"})
    @Testcontainers(disabledWithoutDocker = true)
    class InventoryIntegrationTest {
        @Container static final MSSQLServerContainer<?> SQL = new MSSQLServerContainer<>("mcr.microsoft.com/mssql/server:2022-latest").acceptLicense();
        @DynamicPropertySource static void properties(DynamicPropertyRegistry registry) {
            registry.add("spring.datasource.url", SQL::getJdbcUrl); registry.add("spring.datasource.username", SQL::getUsername); registry.add("spring.datasource.password", SQL::getPassword);
        }
        @Test void contextLoads() {
        }
    }
proposed_implementation:
  illustrative_code_status: generated
  source_language: java
  target_repository_path: source/inventory-service/src/test/java/com/ecommerce/inventory/resiliency/KafkaFailureIntegrationTest.java
  target_symbol: KafkaFailureIntegrationTest
  replaces_or_updates_evidence_ids: [EV-F-028-01]
  illustrative_code: |
    @SpringBootTest(properties = {
            "spring.kafka.bootstrap-servers=${spring.embedded.kafka.brokers}",
            "app.kafka.consumer.enabled=true",
            "app.kafka.consumer.dead-letter-topic=order-events-dlt"})
    @EmbeddedKafka(partitions = 1, topics = {"order-events", "inventory-events", "order-events-dlt"})
    @Testcontainers(disabledWithoutDocker = true)
    class KafkaFailureIntegrationTest {

        @Container
        static final MSSQLServerContainer<?> SQL =
                new MSSQLServerContainer<>("mcr.microsoft.com/mssql/server:2022-latest").acceptLicense();

        @DynamicPropertySource
        static void properties(DynamicPropertyRegistry registry) {
            registry.add("spring.datasource.url", SQL::getJdbcUrl);
            registry.add("spring.datasource.username", SQL::getUsername);
            registry.add("spring.datasource.password", SQL::getPassword);
        }

        @Autowired KafkaTemplate<String, Object> kafkaTemplate;
        @Autowired InventoryRepository repository;

        @Test
        void duplicateOrderEventProducesExactlyOneReservation() {
            repository.save(InventoryItem.builder()
                    .productId("p1").availableQuantity(10).reservedQuantity(0)
                    .updatedAt(Instant.now()).build());

            Map<String, Object> event = Map.of(
                    "type", "ORDER_CREATED", "productId", "p1", "quantity", 3, "orderId", "o1");

            kafkaTemplate.send("order-events", "p1", event);
            kafkaTemplate.send("order-events", "p1", event);

            await().atMost(Duration.ofSeconds(30)).untilAsserted(() -> {
                InventoryItem item = repository.findByProductId("p1").orElseThrow();
                assertThat(item.getAvailableQuantity()).isEqualTo(7);
                assertThat(item.getReservedQuantity()).isEqualTo(3);
            });
        }
    }
  narrative_explanation: >-
    The test reuses the exact Testcontainers, @EmbeddedKafka, and @DynamicPropertySource model already
    present in InventoryIntegrationTest, so no new test infrastructure is introduced. It publishes the
    same business event twice and asserts that the authoritative quantities reflect exactly one
    application, which is the behaviour CHANGE-AA-008 introduces and which no existing test covers.
  discovery_required_reason: null
  unresolved_inputs: []
```

### ICB-024-02: Probe transition coverage

```yaml
change_id: CHANGE-AA-024
block_id: ICB-024-02
target:
  repository_path: source/inventory-service/src/test/java/com/ecommerce/inventory/resiliency/ProbeTransitionIntegrationTest.java
  symbol: ProbeTransitionIntegrationTest
  target_status: new_file
current_implementation:
  evidence_id: EV-F-028-01
  evidence_note: >-
    The excerpt is preserved verbatim in ICB-024-01. No Actuator integration test or fault injection
    verifies probe transitions or traffic eligibility.
proposed_implementation:
  illustrative_code_status: generated
  source_language: java
  target_repository_path: source/inventory-service/src/test/java/com/ecommerce/inventory/resiliency/ProbeTransitionIntegrationTest.java
  target_symbol: ProbeTransitionIntegrationTest
  replaces_or_updates_evidence_ids: [EV-F-028-01]
  illustrative_code: |
    @SpringBootTest(webEnvironment = SpringBootTest.WebEnvironment.RANDOM_PORT)
    @AutoConfigureMockMvc
    @Testcontainers(disabledWithoutDocker = true)
    class ProbeTransitionIntegrationTest {

        @Container
        static final MSSQLServerContainer<?> SQL =
                new MSSQLServerContainer<>("mcr.microsoft.com/mssql/server:2022-latest").acceptLicense();

        @DynamicPropertySource
        static void properties(DynamicPropertyRegistry registry) {
            registry.add("spring.datasource.url", SQL::getJdbcUrl);
            registry.add("spring.datasource.username", SQL::getUsername);
            registry.add("spring.datasource.password", SQL::getPassword);
        }

        @Autowired MockMvc mockMvc;

        @Test
        void readinessFailsWhenDatabaseIsUnavailableAndRecoversAfterwards() throws Exception {
            mockMvc.perform(get("/actuator/health/readiness")).andExpect(status().isOk());

            SQL.getDockerClient().pauseContainerCmd(SQL.getContainerId()).exec();
            try {
                await().atMost(Duration.ofSeconds(30)).untilAsserted(() ->
                        mockMvc.perform(get("/actuator/health/readiness"))
                                .andExpect(status().isServiceUnavailable()));

                mockMvc.perform(get("/actuator/health/liveness")).andExpect(status().isOk());
            } finally {
                SQL.getDockerClient().unpauseContainerCmd(SQL.getContainerId()).exec();
            }

            await().atMost(Duration.ofSeconds(60)).untilAsserted(() ->
                    mockMvc.perform(get("/actuator/health/readiness")).andExpect(status().isOk()));
        }
    }
  narrative_explanation: >-
    Pausing the database container is the fault injection; it exercises the readiness group membership
    from CHANGE-AA-001 without requiring a live Azure dependency. The test asserts all three properties
    the readiness design rule requires: readiness fails on critical dependency loss, liveness does not,
    and readiness recovers after restoration without a process restart.
  discovery_required_reason: null
  unresolved_inputs: []
```

### ICB-024-03: Effective resiliency configuration regression guard

```yaml
change_id: CHANGE-AA-024
block_id: ICB-024-03
target:
  repository_path: source/inventory-service/src/test/java/com/ecommerce/inventory/resiliency/EffectiveResiliencyConfigurationTest.java
  symbol: EffectiveResiliencyConfigurationTest
  target_status: new_file
current_implementation:
  evidence_id: EV-F-028-02
  original_source_excerpt: |
    @ExtendWith(MockitoExtension.class)
    class InventoryServiceImplTest {
        @Mock InventoryRepository repository; @Mock InventoryMapper mapper; @Mock InventoryEventProducer producer; @InjectMocks InventoryServiceImpl service;
        @Test void reservesAvailableStockAndPublishesEvent() {
            InventoryItem item = InventoryItem.builder().id(1L).productId("p1").availableQuantity(10).build();
            InventoryResponse response = new InventoryResponse(1L, "p1", 7, 3, Instant.now());
            when(repository.findByProductId("p1")).thenReturn(Optional.of(item)); when(repository.save(any())).thenReturn(item); when(mapper.toResponse(item)).thenReturn(response);
            assertThat(service.reserve("p1", 3, "o1")).isEqualTo(response);
            assertThat(item.getAvailableQuantity()).isEqualTo(7); verify(producer).publish("INVENTORY_RESERVED", response, "o1");
        }
    }
proposed_implementation:
  illustrative_code_status: generated
  source_language: java
  target_repository_path: source/inventory-service/src/test/java/com/ecommerce/inventory/resiliency/EffectiveResiliencyConfigurationTest.java
  target_symbol: EffectiveResiliencyConfigurationTest
  replaces_or_updates_evidence_ids: [EV-F-028-02]
  illustrative_code: |
    @SpringBootTest
    @ActiveProfiles("test")
    class EffectiveResiliencyConfigurationTest {

        @Autowired HikariDataSource dataSource;
        @Autowired KafkaProperties kafkaProperties;
        @Autowired HealthEndpointGroups healthEndpointGroups;

        @Test
        void databaseDeadlinesAreBounded() {
            assertThat(dataSource.getConnectionTimeout()).isPositive();
            assertThat(dataSource.getValidationTimeout()).isPositive();
            assertThat(dataSource.getMaxLifetime()).isPositive();
        }

        @Test
        void producerBlockingIsBounded() {
            assertThat(kafkaProperties.getProducer().getProperties())
                    .containsKey("max.block.ms")
                    .containsKey("delivery.timeout.ms");
        }

        @Test
        void readinessGroupIncludesTheAuthoritativeStore() {
            HealthEndpointGroup readiness = healthEndpointGroups.get("readiness").orElseThrow();
            assertThat(readiness.isMember("db")).isTrue();
            assertThat(readiness.isMember("redis")).isFalse();
        }
    }
  narrative_explanation: >-
    The guard asserts the effective resolved configuration rather than the file content, so a Spring Boot
    parent or Spring Cloud Azure BOM bump that changes a managed default fails the build instead of
    silently changing timeout, offset, or health semantics in production. This is the regression
    protection APP-SUPPLY-001 requires and that the existing context-load assertion does not provide. The
    existing InventoryServiceImplTest is left in place; this test is additive.
  discovery_required_reason: null
  unresolved_inputs: []
```

## 6. Proposed Test Changes

Illustrative proposal only. Every test below inherits the priority of the behaviour it proves, in accordance with `default_rules.tests_inherit_behavior_priority`. The Step 3B report preference `testing_output_mode: hidden` controls report rendering only and does not reduce these obligations. The repository test model is known: JUnit 5, Mockito, AssertJ, Spring Boot Test, `@EmbeddedKafka` from `spring-kafka-test`, and Testcontainers 1.20.3 with the `junit-jupiter` and `mssqlserver` modules. Every proposal below reuses that model.

```yaml
test_model:
  frameworks_present:
    - junit-jupiter
    - mockito
    - assertj
    - spring-boot-starter-test
    - spring-kafka-test
    - testcontainers junit-jupiter
    - testcontainers mssqlserver
  frameworks_required_but_absent:
    - id: awaitility
      note: >-
        Transitively available through spring-boot-starter-test in Spring Boot 3.3.x. The implementer must
        confirm availability before relying on it, otherwise a polling helper is required.
    - id: testcontainers redis or generic container
      note: Required by PT-014-01 and PT-024-02 for Redis fault injection.
  approved_testing_libraries:
    integration: testcontainers
    api_mocking: wiremock
  wiremock_applicability: >-
    not_required; the service makes no outbound HTTP call, so no API mocking target exists.
```

### Wave 1 tests

```yaml
proposed_tests:
  - test_id: PT-001-01
    change_id: CHANGE-AA-001
    inherits_priority: P0
    proves: F-008 readiness reflects authoritative dependency health and liveness does not
    target_repository_path: source/inventory-service/src/test/java/com/ecommerce/inventory/resiliency/ReadinessProbeIntegrationTest.java
    test_type: integration
    illustrative_code_status: generated
    source_language: java
    illustrative_code: |
      @Test
      void readinessGroupIncludesDatabaseAndExcludesCache() {
          HealthEndpointGroup readiness = healthEndpointGroups.get("readiness").orElseThrow();
          assertThat(readiness.isMember("db")).isTrue();
          assertThat(readiness.isMember("redis")).isFalse();
          assertThat(healthEndpointGroups.get("liveness").orElseThrow().isMember("db")).isFalse();
      }
  - test_id: PT-001-02
    change_id: CHANGE-AA-001
    inherits_priority: P0
    proves: F-008 readiness transitions are observable
    target_repository_path: source/inventory-service/src/test/java/com/ecommerce/inventory/health/ReadinessTransitionListenerTest.java
    test_type: unit
    illustrative_code_status: generated
    source_language: java
    illustrative_code: |
      @Test
      void readinessTransitionIncrementsCounter() {
          SimpleMeterRegistry registry = new SimpleMeterRegistry();
          ReadinessTransitionListener listener = new ReadinessTransitionListener(registry);

          listener.onReadinessChange(new AvailabilityChangeEvent<>(this, ReadinessState.REFUSING_TRAFFIC));

          assertThat(registry.counter("inventory.readiness.transition", "state", "REFUSING_TRAFFIC").count())
                  .isEqualTo(1d);
      }
  - test_id: PT-002-01
    change_id: CHANGE-AA-002
    inherits_priority: P0
    proves: F-024 startup validates the schema and applies no DDL
    target_repository_path: source/inventory-service/src/test/java/com/ecommerce/inventory/resiliency/SchemaValidationIntegrationTest.java
    test_type: integration
    illustrative_code_status: generated
    source_language: java
    illustrative_code: |
      @Test
      void applicationStartsAgainstSchemaCreatedOnlyByMigrationScript() {
          assertThat(environment.getProperty("spring.jpa.hibernate.ddl-auto")).isEqualTo("validate");
          assertThat(repository.count()).isZero();
      }

      @Test
      void noProfileEnablesRuntimeDdl() {
          Stream.of("application.yml", "application-prod.yml")
                  .map(TestResources::readClasspathResource)
                  .forEach(content -> assertThat(content)
                          .doesNotContain("ddl-auto: update")
                          .doesNotContain("ddl-auto: create"));
      }
  - test_id: PT-003-01
    change_id: CHANGE-AA-003
    inherits_priority: P0
    proves: F-022 the Key Vault startup dependency is bounded
    target_repository_path: source/inventory-service/src/test/java/com/ecommerce/inventory/resiliency/KeyVaultStartupContractTest.java
    test_type: integration
    illustrative_code_status: generated
    source_language: java
    illustrative_code: |
      @Test
      void keyVaultClientBudgetsAreDeclaredAndExternalized() {
          String prodProfile = TestResources.readClasspathResource("application-prod.yml");
          assertThat(prodProfile)
                  .contains("connect-timeout: ${KEYVAULT_CONNECT_TIMEOUT}")
                  .contains("response-timeout: ${KEYVAULT_RESPONSE_TIMEOUT}")
                  .contains("max-retries: ${KEYVAULT_MAX_RETRIES}");
          assertThat(prodProfile).doesNotContain("vault.azure.net");
      }
  - test_id: PT-004-01
    change_id: CHANGE-AA-004
    inherits_priority: P0
    proves: F-021 shutdown withdraws readiness and stops listeners before draining
    target_repository_path: source/inventory-service/src/test/java/com/ecommerce/inventory/resiliency/GracefulShutdownIntegrationTest.java
    test_type: integration
    illustrative_code_status: generated
    source_language: java
    illustrative_code: |
      @Test
      void shutdownWithdrawsReadinessThenStopsListeners() {
          MessageListenerContainer container =
                  listenerRegistry.getListenerContainer("order-events-listener");
          assertThat(container.isRunning()).isTrue();

          coordinator.stop();

          assertThat(applicationAvailability.getReadinessState())
                  .isEqualTo(ReadinessState.REFUSING_TRAFFIC);
          assertThat(container.isRunning()).isFalse();
      }
  - test_id: PT-005-01
    change_id: CHANGE-AA-005
    inherits_priority: P0
    proves: F-026 metrics and logs carry regional identity
    target_repository_path: source/inventory-service/src/test/java/com/ecommerce/inventory/observability/DeploymentIdentityTelemetryTest.java
    test_type: integration
    illustrative_code_status: generated
    source_language: java
    illustrative_code: |
      @Test
      void everyMeterCarriesRegionAndRoleTags() {
          meterRegistry.counter("inventory.publish.outcome", "eventType", "INVENTORY_RESERVED", "outcome", "success")
                  .increment();

          meterRegistry.getMeters().forEach(meter -> {
              assertThat(meter.getId().getTag("region")).isNotNull();
              assertThat(meter.getId().getTag("role")).isNotNull();
          });
      }
  - test_id: PT-006-01
    change_id: CHANGE-AA-006
    inherits_priority: P0
    proves: F-027 failure and business outcomes emit actionable signals
    target_repository_path: source/inventory-service/src/test/java/com/ecommerce/inventory/observability/InventoryTelemetryTest.java
    test_type: unit
    illustrative_code_status: generated
    source_language: java
    illustrative_code: |
      @Test
      void lastSuccessGaugeIsPresentBeforeAnyRecordIsProcessed() {
          SimpleMeterRegistry registry = new SimpleMeterRegistry();
          InventoryTelemetry telemetry = new InventoryTelemetry(registry);

          assertThat(registry.get("inventory.consume.last_success.age.seconds").gauge().value())
                  .isEqualTo(-1d);

          telemetry.recordConsumption("ORDER_CREATED", InventoryTelemetry.OUTCOME_SUCCESS);

          assertThat(registry.get("inventory.consume.last_success.age.seconds").gauge().value())
                  .isGreaterThanOrEqualTo(0d);
          assertThat(registry.counter("inventory.consume.outcome",
                  "eventType", "ORDER_CREATED", "outcome", "success").count()).isEqualTo(1d);
      }

      @Test
      void cacheFailureIsCountedSeparatelyFromCacheMiss() {
          SimpleMeterRegistry registry = new SimpleMeterRegistry();
          InventoryTelemetry telemetry = new InventoryTelemetry(registry);

          telemetry.recordCacheOutcome("inventory", InventoryTelemetry.CACHE_MISS);
          telemetry.recordCacheOutcome("inventory", InventoryTelemetry.CACHE_FAILURE);

          assertThat(registry.counter("inventory.cache.outcome", "cache", "inventory", "outcome", "miss").count())
                  .isEqualTo(1d);
          assertThat(registry.counter("inventory.cache.outcome", "cache", "inventory", "outcome", "failure").count())
                  .isEqualTo(1d);
      }
```

### Wave 2 tests

```yaml
proposed_tests:
  - test_id: PT-007-01
    change_id: CHANGE-AA-007
    inherits_priority: P0
    proves: F-004 consumption is deployment controlled and does not affect readiness
    target_repository_path: source/inventory-service/src/test/java/com/ecommerce/inventory/resiliency/RegionalConsumptionControlTest.java
    test_type: integration
    illustrative_code_status: generated
    source_language: java
    illustrative_code: |
      @SpringBootTest(properties = "app.kafka.consumer.enabled=false")
      @EmbeddedKafka(partitions = 1, topics = {"order-events", "inventory-events"})
      class RegionalConsumptionDisabledTest {

          @Autowired KafkaTemplate<String, Object> kafkaTemplate;
          @Autowired InventoryRepository repository;
          @Autowired MockMvc mockMvc;

          @Test
          void disabledConsumerDoesNotConsumeButStaysReady() throws Exception {
              repository.save(InventoryItem.builder().productId("p1").availableQuantity(10)
                      .reservedQuantity(0).updatedAt(Instant.now()).build());

              kafkaTemplate.send("order-events", "p1",
                      Map.of("type", "ORDER_CREATED", "productId", "p1", "quantity", 3, "orderId", "o1"));

              mockMvc.perform(get("/actuator/health/readiness")).andExpect(status().isOk());
              Thread.sleep(2000);
              assertThat(repository.findByProductId("p1").orElseThrow().getAvailableQuantity()).isEqualTo(10);
          }
      }
  - test_id: PT-007-02
    change_id: CHANGE-AA-007
    inherits_priority: P0
    proves: F-004 activation transitions are observable and reversible
    target_repository_path: source/inventory-service/src/test/java/com/ecommerce/inventory/kafka/OrderEventConsumerActivationTest.java
    test_type: integration
    illustrative_code_status: generated
    source_language: java
    illustrative_code: |
      @Test
      void activationGaugeReflectsConsumptionState() {
          controller.deactivate();
          assertThat(meterRegistry.get("inventory.kafka.consumption.active").gauge().value()).isZero();

          controller.activate();
          assertThat(meterRegistry.get("inventory.kafka.consumption.active").gauge().value()).isOne();
      }
  - test_id: PT-008-01
    change_id: CHANGE-AA-008
    inherits_priority: P0
    proves: F-003 a repeated operation produces exactly one stock movement
    target_repository_path: source/inventory-service/src/test/java/com/ecommerce/inventory/service/IdempotentStockAdjustmentTest.java
    test_type: integration
    illustrative_code_status: generated
    source_language: java
    illustrative_code: |
      @Test
      void repeatedReserveWithSameReferenceAppliesOnce() {
          repository.save(InventoryItem.builder().productId("p1").availableQuantity(10)
                  .reservedQuantity(0).updatedAt(Instant.now()).build());

          service.reserve("p1", 3, "order-1");
          service.reserve("p1", 3, "order-1");

          InventoryItem item = repository.findByProductId("p1").orElseThrow();
          assertThat(item.getAvailableQuantity()).isEqualTo(7);
          assertThat(item.getReservedQuantity()).isEqualTo(3);
          assertThat(processedOperations.existsByOperationIdentity("INVENTORY_RESERVED:p1:order-1")).isTrue();
      }

      @Test
      void distinctReferencesEachApply() {
          repository.save(InventoryItem.builder().productId("p2").availableQuantity(10)
                  .reservedQuantity(0).updatedAt(Instant.now()).build());

          service.reserve("p2", 2, "order-1");
          service.reserve("p2", 2, "order-2");

          assertThat(repository.findByProductId("p2").orElseThrow().getReservedQuantity()).isEqualTo(4);
      }
  - test_id: PT-008-02
    change_id: CHANGE-AA-008
    inherits_priority: P0
    proves: F-003 replay from an earlier offset produces no additional movement
    target_repository_path: source/inventory-service/src/test/java/com/ecommerce/inventory/resiliency/OrderEventReplayIntegrationTest.java
    test_type: integration
    illustrative_code_status: generated
    source_language: java
    illustrative_code: |
      @Test
      void replayingTheRetainedHistoryProducesNoAdditionalMovement() {
          repository.save(InventoryItem.builder().productId("p1").availableQuantity(100)
                  .reservedQuantity(0).updatedAt(Instant.now()).build());

          List<Map<String, Object>> history = List.of(
                  Map.of("type", "ORDER_CREATED", "productId", "p1", "quantity", 5, "orderId", "o1"),
                  Map.of("type", "ORDER_CREATED", "productId", "p1", "quantity", 7, "orderId", "o2"),
                  Map.of("type", "ORDER_CANCELLED", "productId", "p1", "quantity", 5, "orderId", "o1"));

          history.forEach(event -> kafkaTemplate.send("order-events", "p1", event));
          awaitReserved("p1", 7);

          // Simulate a promotion replaying from the beginning of the retained history.
          history.forEach(event -> kafkaTemplate.send("order-events", "p1", event));

          Thread.sleep(3000);
          InventoryItem item = repository.findByProductId("p1").orElseThrow();
          assertThat(item.getReservedQuantity()).isEqualTo(7);
          assertThat(item.getAvailableQuantity()).isEqualTo(93);
      }
```

### Wave 3 tests

```yaml
proposed_tests:
  - test_id: PT-009-01
    change_id: CHANGE-AA-009
    inherits_priority: P1
    proves: F-009, F-010, F-011 every remote dependency has a bounded, externalized deadline
    target_repository_path: source/inventory-service/src/test/java/com/ecommerce/inventory/resiliency/DependencyTimeoutConfigurationTest.java
    test_type: integration
    illustrative_code_status: generated
    source_language: java
    illustrative_code: |
      @Test
      void everyDependencyDeadlineIsResolvedAndPositive() {
          assertThat(hikariDataSource.getConnectionTimeout()).isPositive();
          assertThat(hikariDataSource.getValidationTimeout()).isPositive();
          assertThat(redisProperties.getTimeout()).isNotNull().isPositive();
          assertThat(kafkaProperties.getProducer().getProperties().get("max.block.ms")).isNotNull();
          assertThat(kafkaProperties.getConsumer().getProperties().get("max.poll.interval.ms")).isNotNull();
      }

      @Test
      void noDeadlineValueIsHardcodedWithARegionOrEndpoint() {
          String defaults = TestResources.readClasspathResource("application.yml");
          assertThat(defaults)
                  .doesNotContain("westus")
                  .doesNotContain("eastus")
                  .doesNotContain(".azure.com");
      }
  - test_id: PT-010-01
    change_id: CHANGE-AA-010
    inherits_priority: P1
    proves: F-012 transient failures are retried and business failures are not
    target_repository_path: source/inventory-service/src/test/java/com/ecommerce/inventory/service/TransientFailureRetryTest.java
    test_type: integration
    illustrative_code_status: generated
    source_language: java
    illustrative_code: |
      @Test
      void transientFailureIsRetriedAndThenSucceeds() {
          when(repository.findByProductId("p1"))
                  .thenThrow(new TransientDataAccessResourceException("connection reset"))
                  .thenReturn(Optional.of(item));

          assertThat(service.reserve("p1", 1, "order-1")).isNotNull();
          verify(repository, times(2)).findByProductId("p1");
      }

      @Test
      void businessFailureIsNotRetried() {
          when(repository.findByProductId("p1")).thenReturn(Optional.of(emptyStockItem));

          assertThatThrownBy(() -> service.reserve("p1", 99, "order-1"))
                  .isInstanceOf(IllegalArgumentException.class);
          verify(repository, times(1)).findByProductId("p1");
      }

      @Test
      void ambiguousCommitOutcomeIsNotClassifiedTransient() {
          assertThat(classifier.isTransient(new TransactionSystemException("commit outcome unknown")))
                  .isFalse();
      }
  - test_id: PT-011-01
    change_id: CHANGE-AA-011
    inherits_priority: P1
    proves: F-013 a conflict is absorbed by reload and reapply
    target_repository_path: source/inventory-service/src/test/java/com/ecommerce/inventory/service/OptimisticLockConflictTest.java
    test_type: integration
    illustrative_code_status: generated
    source_language: java
    illustrative_code: |
      @Test
      void concurrentReservationsBothApply() throws Exception {
          repository.save(InventoryItem.builder().productId("p1").availableQuantity(10)
                  .reservedQuantity(0).updatedAt(Instant.now()).build());

          ExecutorService pool = Executors.newFixedThreadPool(2);
          Future<?> first = pool.submit(() -> service.reserve("p1", 3, "order-1"));
          Future<?> second = pool.submit(() -> service.reserve("p1", 4, "order-2"));
          first.get(30, TimeUnit.SECONDS);
          second.get(30, TimeUnit.SECONDS);

          InventoryItem item = repository.findByProductId("p1").orElseThrow();
          assertThat(item.getReservedQuantity()).isEqualTo(7);
          assertThat(item.getAvailableQuantity()).isEqualTo(3);
      }
  - test_id: PT-012-01
    change_id: CHANGE-AA-012
    inherits_priority: P1
    proves: F-014 dependency failures are classified distinctly from application errors
    target_repository_path: source/inventory-service/src/test/java/com/ecommerce/inventory/exception/DependencyFailureSemanticsTest.java
    test_type: integration
    implementation_gate: >-
      The status-contract assertions execute only after the API contract owner approves CHANGE-AA-012.
      The classification-telemetry assertion is unconditional.
    illustrative_code_status: generated
    source_language: java
    illustrative_code: |
      @Test
      void existingMappingsAreUnchanged() throws Exception {
          when(service.get(99L)).thenThrow(new ResourceNotFoundException("Inventory not found: 99"));
          mockMvc.perform(get("/api/v1/inventory/99")).andExpect(status().isNotFound());

          when(service.get(1L)).thenThrow(new IllegalArgumentException("bad request"));
          mockMvc.perform(get("/api/v1/inventory/1")).andExpect(status().isBadRequest());
      }

      @Test
      void transientDependencyFailureIsClassifiedAndCounted() throws Exception {
          when(service.get(1L)).thenThrow(new DataAccessResourceFailureException("db down"));

          mockMvc.perform(get("/api/v1/inventory/1"))
                  .andExpect(status().isServiceUnavailable())
                  .andExpect(header().exists(HttpHeaders.RETRY_AFTER))
                  .andExpect(jsonPath("$.code").value("DEPENDENCY_UNAVAILABLE"))
                  .andExpect(jsonPath("$.message").value("A required dependency is temporarily unavailable."));
      }
  - test_id: PT-013-01
    change_id: CHANGE-AA-013
    inherits_priority: P1
    proves: F-015 one saturated dependency does not consume capacity for the others
    target_repository_path: source/inventory-service/src/test/java/com/ecommerce/inventory/resiliency/DependencyIsolationTest.java
    test_type: integration
    illustrative_code_status: generated
    source_language: java
    illustrative_code: |
      @Test
      void saturatedCacheBulkheadDoesNotBlockActuatorEndpoints() throws Exception {
          Bulkhead cacheBulkhead = bulkheadRegistry.bulkhead("inventoryCache");
          int limit = cacheBulkhead.getBulkheadConfig().getMaxConcurrentCalls();
          for (int held = 0; held < limit; held++) {
              assertThat(cacheBulkhead.tryAcquirePermission()).isTrue();
          }

          mockMvc.perform(get("/actuator/health/readiness")).andExpect(status().isOk());
          mockMvc.perform(get("/actuator/prometheus")).andExpect(status().isOk());
      }

      @Test
      void breakerOpensOnClassifiedFailuresAndIgnoresBusinessFailures() {
          CircuitBreaker breaker = circuitBreakerRegistry.circuitBreaker("inventoryDb");

          breaker.onError(0, TimeUnit.MILLISECONDS, new IllegalArgumentException("business"));
          assertThat(breaker.getMetrics().getNumberOfFailedCalls()).isZero();
      }
  - test_id: PT-014-01
    change_id: CHANGE-AA-014
    inherits_priority: P1
    proves: F-016 a Redis outage degrades the read path rather than failing it
    target_repository_path: source/inventory-service/src/test/java/com/ecommerce/inventory/config/CacheFailureContainmentTest.java
    test_type: integration
    illustrative_code_status: generated
    source_language: java
    illustrative_code: |
      @Test
      void redisGetFailureFallsThroughToTheRepository() {
          repository.save(InventoryItem.builder().productId("p1").availableQuantity(5)
                  .reservedQuantity(0).updatedAt(Instant.now()).build());
          Long id = repository.findByProductId("p1").orElseThrow().getId();

          redis.stop();

          assertThat(service.get(id)).isNotNull();
          assertThat(meterRegistry.counter("inventory.cache.outcome",
                  "cache", "inventory", "outcome", "failure").count()).isPositive();
      }

      @Test
      void redisEvictFailureDoesNotFailTheWrite() {
          Long id = repository.findByProductId("p1").orElseThrow().getId();
          redis.stop();

          assertThatNoException().isThrownBy(() ->
                  service.update(id, new InventoryRequest("p1", 9, 0)));
      }
  - test_id: PT-015-01
    change_id: CHANGE-AA-015
    inherits_priority: P1
    proves: F-029 the cached read path works against a real cache
    target_repository_path: source/inventory-service/src/test/java/com/ecommerce/inventory/config/RedisCacheContractIntegrationTest.java
    test_type: integration
    illustrative_code_status: generated
    source_language: java
    illustrative_code: |
      @Test
      void cachedReadSucceedsAndReturnsAnEqualValueOnTheSecondCall() {
          Long id = repository.findByProductId("p1").orElseThrow().getId();

          InventoryResponse first = service.get(id);
          InventoryResponse second = service.get(id);

          assertThat(second).isEqualTo(first);
          assertThat(cacheManager.getCache("inventory").get(id)).isNotNull();
      }
  - test_id: PT-015-02
    change_id: CHANGE-AA-015
    inherits_priority: P1
    proves: F-017 and F-018 entries expire and keys are namespaced and versioned
    target_repository_path: source/inventory-service/src/test/java/com/ecommerce/inventory/config/RedisCacheContractIntegrationTest.java
    test_type: integration
    illustrative_code_status: generated
    source_language: java
    illustrative_code: |
      @Test
      void everyEntryCarriesATtlAndAVersionedNamespacedKey() {
          Long id = repository.findByProductId("p1").orElseThrow().getId();
          service.get(id);

          RedisCacheConfiguration configuration =
                  ((RedisCacheManager) cacheManager).getCacheConfigurations().get("inventory");
          assertThat(configuration.getTtlFunction()).isNotNull();

          Set<String> keys = redisTemplate.keys("*");
          assertThat(keys).allMatch(key -> key.startsWith(keyPrefix + ":" + schemaVersion + ":inventory::"));
      }
  - test_id: PT-016-01
    change_id: CHANGE-AA-016
    inherits_priority: P1
    proves: F-019 concurrent misses produce one authoritative read
    target_repository_path: source/inventory-service/src/test/java/com/ecommerce/inventory/service/CacheStampedeTest.java
    test_type: integration
    illustrative_code_status: generated
    source_language: java
    illustrative_code: |
      @Test
      void concurrentMissesForTheSameKeyProduceOneRepositoryRead() throws Exception {
          cacheManager.getCache("inventory").clear();
          Long id = repository.findByProductId("p1").orElseThrow().getId();
          reset(countingRepository);

          ExecutorService pool = Executors.newFixedThreadPool(16);
          List<Callable<InventoryResponse>> calls =
                  Collections.nCopies(16, () -> service.get(id));
          pool.invokeAll(calls).forEach(future -> assertThatNoException().isThrownBy(future::get));

          verify(countingRepository, times(1)).findById(id);
      }
  - test_id: PT-017-01
    change_id: CHANGE-AA-017
    inherits_priority: P1
    proves: F-025 the list path is bounded independently of table size
    target_repository_path: source/inventory-service/src/test/java/com/ecommerce/inventory/service/BoundedInventoryListTest.java
    test_type: integration
    implementation_gate: >-
      The endpoint response-shape assertion executes only after the API contract owner approves
      CHANGE-AA-017. The service-level bound assertion is unconditional.
    illustrative_code_status: generated
    source_language: java
    illustrative_code: |
      @Test
      void listReturnsAtMostTheConfiguredMaximumPageSize() {
          IntStream.range(0, 500).forEach(index -> repository.save(
                  InventoryItem.builder().productId("p" + index).availableQuantity(1)
                          .reservedQuantity(0).updatedAt(Instant.now()).build()));

          Page<InventoryResponse> page = service.list(PageRequest.of(0, 10_000));

          assertThat(page.getContent()).hasSizeLessThanOrEqualTo(maxPageSize);
          assertThat(page.getTotalElements()).isEqualTo(500);
      }
  - test_id: PT-018-01
    change_id: CHANGE-AA-018
    inherits_priority: P1
    proves: F-001 publication failure is observed rather than dropped
    target_repository_path: source/inventory-service/src/test/java/com/ecommerce/inventory/kafka/InventoryEventProducerDurabilityTest.java
    test_type: unit
    illustrative_code_status: generated
    source_language: java
    illustrative_code: |
      @Test
      void failedSendIncrementsTheFailureCounter() {
          CompletableFuture<SendResult<String, Object>> failed = new CompletableFuture<>();
          failed.completeExceptionally(new TimeoutException("delivery timeout"));
          when(kafkaTemplate.send(eq("inventory-events"), eq("p1"), any())).thenReturn(failed);

          producer.publish("INVENTORY_RESERVED", response, "order-1");

          assertThat(registry.counter("inventory.publish.outcome",
                  "eventType", "INVENTORY_RESERVED", "outcome", "failure").count()).isEqualTo(1d);
      }

      @Test
      void producerDurabilityPropertiesAreDeclared() {
          String defaults = TestResources.readClasspathResource("application.yml");
          assertThat(defaults)
                  .contains("acks: ${KAFKA_PRODUCER_ACKS}")
                  .contains("enable.idempotence: ${KAFKA_PRODUCER_ENABLE_IDEMPOTENCE}");
      }
  - test_id: PT-019-01
    change_id: CHANGE-AA-019
    inherits_priority: P1
    proves: F-005 the offset does not advance past unprocessed work
    target_repository_path: source/inventory-service/src/test/java/com/ecommerce/inventory/kafka/OrderEventErrorHandlingTest.java
    test_type: integration
    illustrative_code_status: generated
    source_language: java
    illustrative_code: |
      @Test
      void ackModeIsManualImmediateAndAttemptsAreBounded() {
          assertThat(containerFactory.getContainerProperties().getAckMode())
                  .isEqualTo(ContainerProperties.AckMode.MANUAL_IMMEDIATE);
          assertThat(errorHandler.getClass()).isEqualTo(DefaultErrorHandler.class);
          assertThat(TestResources.readClasspathResource("application.yml"))
                  .contains("max-attempts: ${KAFKA_CONSUMER_MAX_ATTEMPTS}");
      }
  - test_id: PT-019-02
    change_id: CHANGE-AA-019
    inherits_priority: P1
    proves: F-006 a poison record is quarantined with a durable artifact
    target_repository_path: source/inventory-service/src/test/java/com/ecommerce/inventory/kafka/PoisonRecordQuarantineTest.java
    test_type: integration
    illustrative_code_status: generated
    source_language: java
    illustrative_code: |
      @Test
      void recordWithoutQuantityIsQuarantinedOnTheFirstAttempt() {
          kafkaTemplate.send("order-events", "p1",
                  Map.of("type", "ORDER_CREATED", "productId", "p1", "orderId", "o1"));

          ConsumerRecord<String, Object> quarantined =
                  KafkaTestUtils.getSingleRecord(dltConsumer, "order-events-dlt", Duration.ofSeconds(30));

          assertThat(quarantined).isNotNull();
          assertThat(registry.counter("inventory.consume.outcome",
                  "eventType", "order-events", "outcome", "quarantined").count()).isEqualTo(1d);
      }

      @Test
      void payloadExtractionRejectsNonNumericQuantity() {
          assertThatThrownBy(() -> OrderEventPayload.from(
                  Map.of("type", "ORDER_CREATED", "productId", "p1", "quantity", "three", "orderId", "o1")))
                  .isInstanceOf(NonRetryablePayloadException.class);
      }
  - test_id: PT-020-01
    change_id: CHANGE-AA-020
    inherits_priority: P1
    proves: F-023 rotated credentials are applied without a process restart
    target_repository_path: source/inventory-service/src/test/java/com/ecommerce/inventory/config/SecretRotationRecoveryTest.java
    test_type: integration
    illustrative_code_status: generated
    source_language: java
    illustrative_code: |
      @Test
      void rotatedDatasourcePasswordEvictsThePoolWithoutRestart() {
          String rotated = "rotated-" + UUID.randomUUID();
          environment.getPropertySources().addFirst(
                  new MapPropertySource("rotation", Map.of("spring.datasource.password", rotated)));

          handler.applyRotationIfChanged();

          assertThat(hikariDataSource.getHikariConfigMXBean().getPassword()).isEqualTo(rotated);
          assertThat(registry.counter("inventory.credential.rotation", "target", "datasource").count())
                  .isEqualTo(1d);
      }
```

### Wave 4 tests

```yaml
proposed_tests:
  - test_id: PT-021-01
    change_id: CHANGE-AA-021
    inherits_priority: P2
    proves: F-002 no event is published for a rolled-back transaction
    target_repository_path: source/inventory-service/src/test/java/com/ecommerce/inventory/outbox/OutboxCommitOrderingTest.java
    test_type: integration
    implementation_gate: Executes only after architecture approval of CHANGE-AA-021.
    illustrative_code_status: generated
    source_language: java
    illustrative_code: |
      @Test
      void rolledBackTransactionLeavesNoOutboxRecordAndPublishesNothing() {
          assertThatThrownBy(() -> service.reserve("p1", 9999, "order-1"))
                  .isInstanceOf(IllegalArgumentException.class);

          assertThat(outbox.count()).isZero();
          assertThat(KafkaTestUtils.getRecords(inventoryEventsConsumer, Duration.ofSeconds(5))).isEmpty();
      }

      @Test
      void noProductionPathSendsInsideAnActiveTransaction() {
          service.reserve("p1", 1, "order-2");
          assertThat(outbox.findByStatusOrderByCreatedAtAsc(OutboxRecord.Status.PENDING, Limit.of(10)))
                  .hasSize(1);
      }
  - test_id: PT-021-02
    change_id: CHANGE-AA-021
    inherits_priority: P2
    proves: F-002 the relay reaches a terminal status and is recoverable
    target_repository_path: source/inventory-service/src/test/java/com/ecommerce/inventory/outbox/OutboxRelayIntegrationTest.java
    test_type: integration
    implementation_gate: Executes only after architecture approval of CHANGE-AA-021.
    illustrative_code_status: generated
    source_language: java
    illustrative_code: |
      @Test
      void exhaustedOutboxRecordReachesFailedStatus() {
          OutboxRecord record = outbox.save(OutboxRecord.builder()
                  .eventType("INVENTORY_RESERVED").aggregateKey("p1").referenceId("order-1")
                  .payload("{}").status(OutboxRecord.Status.PENDING).attemptCount(maxAttempts - 1)
                  .createdAt(Instant.now()).build());

          when(kafkaTemplate.send(anyString(), anyString(), any()))
                  .thenReturn(failedFuture(new TimeoutException("broker unavailable")));

          relay.publishPending();

          assertThat(outbox.findById(record.getId()).orElseThrow().getStatus())
                  .isEqualTo(OutboxRecord.Status.FAILED);
      }
  - test_id: PT-022-01
    change_id: CHANGE-AA-022
    inherits_priority: P2
    proves: F-007 republication produces a stable identity
    target_repository_path: source/inventory-service/src/test/java/com/ecommerce/inventory/kafka/InventoryEventEnvelopeTest.java
    test_type: unit
    implementation_gate: >-
      The envelope-contract assertions execute only after event-contract owner approval of
      CHANGE-AA-022. The correlation propagation assertion is unconditional.
    illustrative_code_status: generated
    source_language: java
    illustrative_code: |
      @Test
      void eventIdIsStableAcrossRepublication() {
          String first = InventoryEventEnvelope.eventId("INVENTORY_RESERVED", "p1", "order-1");
          String second = InventoryEventEnvelope.eventId("INVENTORY_RESERVED", "p1", "order-1");

          assertThat(second).isEqualTo(first);
          assertThat(InventoryEventEnvelope.eventId("INVENTORY_RELEASED", "p1", "order-1"))
                  .isNotEqualTo(first);
      }

      @Test
      void envelopeCarriesIdentitySchemaVersionRegionAndCorrelation() {
          producer.publish("INVENTORY_RESERVED", response, "order-1", "corr-1");

          ProducerRecord<String, Object> sent = captureSentRecord();
          assertThat(sent.headers().lastHeader("eventId")).isNotNull();
          assertThat(sent.headers().lastHeader("schemaVersion")).isNotNull();
          assertThat(sent.headers().lastHeader("region")).isNotNull();
          assertThat(sent.headers().lastHeader("correlationId")).isNotNull();
          assertThat(sent.key()).isEqualTo("p1");
          assertThat(sent.topic()).isEqualTo("inventory-events");
      }
  - test_id: PT-023-01
    change_id: CHANGE-AA-023
    inherits_priority: P2
    proves: F-020 reserve and release invalidate the cached entry
    target_repository_path: source/inventory-service/src/test/java/com/ecommerce/inventory/service/CacheInvalidationOnAdjustmentTest.java
    test_type: integration
    illustrative_code_status: generated
    source_language: java
    illustrative_code: |
      @Test
      void reserveEvictsTheCachedEntry() {
          Long id = repository.findByProductId("p1").orElseThrow().getId();
          InventoryResponse cached = service.get(id);
          assertThat(cacheManager.getCache("inventory").get(id)).isNotNull();

          service.reserve("p1", 3, "order-1");

          assertThat(cacheManager.getCache("inventory").get(id)).isNull();
          assertThat(service.get(id).availableQuantity())
                  .isEqualTo(cached.availableQuantity() - 3);
      }

      @Test
      void rolledBackReserveDoesNotEvictAValidEntry() {
          Long id = repository.findByProductId("p1").orElseThrow().getId();
          service.get(id);

          assertThatThrownBy(() -> service.reserve("p1", 9999, "order-2"))
                  .isInstanceOf(IllegalArgumentException.class);

          assertThat(cacheManager.getCache("inventory").get(id)).isNotNull();
      }
  - test_id: PT-024-01
    change_id: CHANGE-AA-024
    inherits_priority: P0
    proves: F-028 Kafka failure and duplicate behaviour is verified
    target_repository_path: source/inventory-service/src/test/java/com/ecommerce/inventory/resiliency/KafkaFailureIntegrationTest.java
    test_type: integration
    illustrative_code_status: generated
    source_language: java
    illustrative_code_reference: ICB-024-01
    illustrative_code: |
      // Full test class is provided in ICB-024-01 and is not duplicated here.
      @Test
      void duplicateOrderEventProducesExactlyOneReservation() {
          // See ICB-024-01 for the complete implementation.
      }
  - test_id: PT-024-02
    change_id: CHANGE-AA-024
    inherits_priority: P0
    proves: F-028 probe transitions and dependency failure behaviour are verified
    target_repository_path: source/inventory-service/src/test/java/com/ecommerce/inventory/resiliency/ProbeTransitionIntegrationTest.java
    test_type: integration
    illustrative_code_status: generated
    source_language: java
    illustrative_code_reference: ICB-024-02
    illustrative_code: |
      // Full test class is provided in ICB-024-02 and is not duplicated here.
      @Test
      void readinessFailsWhenDatabaseIsUnavailableAndRecoversAfterwards() {
          // See ICB-024-02 for the complete implementation.
      }
  - test_id: PT-024-03
    change_id: CHANGE-AA-024
    inherits_priority: P0
    proves: F-028 and APP-SUPPLY-001 a managed version bump cannot silently change resiliency semantics
    target_repository_path: source/inventory-service/src/test/java/com/ecommerce/inventory/resiliency/EffectiveResiliencyConfigurationTest.java
    test_type: integration
    illustrative_code_status: generated
    source_language: java
    illustrative_code_reference: ICB-024-03
    illustrative_code: |
      // Full test class is provided in ICB-024-03 and is not duplicated here.
      @Test
      void readinessGroupIncludesTheAuthoritativeStore() {
          // See ICB-024-03 for the complete implementation.
      }
```

### Illustrative-code coverage summary

```yaml
illustrative_code_coverage:
  source_or_configuration_change_count: 57
  targets_requiring_illustrative_code: 89
  targets_with_generated_code: 86
  targets_with_targeted_discovery_required: 3
  targets_not_applicable: 0
  narrative_only_generated_proposals: 0
  coverage_complete: true
  breakdown:
    source_configuration_build_targets: 57
    test_targets: 32
  by_source_language:
    java: 40
    yaml: 15
    sql: 3
    xml: 4
    other: 0
    blocked: 3
  targeted_discovery_targets:
    - block_id: ICB-002-03
      change_id: CHANGE-AA-002
      target: versioned migration runner dependency
      blocking_fact: No approved schema-migration library exists in governance and no repository evidence establishes an organizational choice.
      partial_proposal_delivered: true
      partial_proposal_blocks: [ICB-002-01, ICB-002-02]
    - block_id: ICB-007-03
      change_id: CHANGE-AA-007
      target: self-enforced single-active ownership lease
      blocking_fact: No approved ownership or fencing mechanism exists and EG-010 leaves current standby prevention unconfirmed.
      partial_proposal_delivered: true
      partial_proposal_blocks: [ICB-007-01, ICB-007-02]
    - block_id: ICB-020-03
      change_id: CHANGE-AA-020
      target: Redis client re-initialization on credential rotation
      blocking_fact: EG-003 leaves the Redis authentication mode inside an externally supplied connection string, so the correct client lifecycle cannot be established.
      partial_proposal_delivered: true
      partial_proposal_blocks: [ICB-020-01, ICB-020-02]
  partial_proposal_compliance:
    changes_with_a_blocked_target: 3
    changes_marked_entirely_discovery_required: 0
    note: >-
      Every change containing a blocked target still delivers concrete code for its unblocked targets, in
      accordance with the partial proposal requirement.
  hardcoding_checks:
    hardcoded_region_names: 0
    hardcoded_regional_endpoints: 0
    hardcoded_credentials: 0
    unapproved_numeric_settings: 0
    note: >-
      Every timeout, retry, backoff, threshold, window, TTL, page size, and budget is expressed as an
      externalized placeholder. The only fixed values in the proposals are structural constants such as
      the cache schema version and the listener id default.
```

## 7. Engineering Backlog

The backlog is ordered by wave, then by priority within the wave. It is the sequencing view of the same 24 changes; it creates no scope of its own.

| Order | Change ID     | Priority | Wave | Complexity | Title                                                        | Approval gate |
|-------|---------------|----------|------|------------|--------------------------------------------------------------|---------------|
| 1     | CHANGE-AA-005 | P0       | 1    | low        | Attach regional identity to every metric and log record       | none          |
| 2     | CHANGE-AA-006 | P0       | 1    | medium     | Emit failure and business-outcome telemetry                   | none          |
| 3     | CHANGE-AA-001 | P0       | 1    | medium     | Make regional traffic eligibility reflect dependency health   | none          |
| 4     | CHANGE-AA-002 | P0       | 1    | medium     | Replace runtime DDL with versioned migrations                 | none          |
| 5     | CHANGE-AA-003 | P0       | 1    | medium     | Bound the Key Vault startup dependency                        | none          |
| 6     | CHANGE-AA-004 | P0       | 1    | medium     | Add graceful shutdown, readiness withdrawal, and draining     | none          |
| 7     | CHANGE-AA-008 | P0       | 2    | high       | Make order-event consumption idempotent                       | partial       |
| 8     | CHANGE-AA-007 | P0       | 2    | high       | Give the Kafka listener a region-role activation contract     | none          |
| 9     | CHANGE-AA-009 | P1       | 3    | medium     | Declare bounded, externalized dependency deadlines            | none          |
| 10    | CHANGE-AA-010 | P1       | 3    | medium     | Add bounded retry for transient Azure SQL failures            | none          |
| 11    | CHANGE-AA-013 | P1       | 3    | high       | Isolate request threads from blocking dependencies            | none          |
| 12    | CHANGE-AA-011 | P1       | 3    | medium     | Detect, absorb, and report optimistic-locking conflicts       | partial       |
| 13    | CHANGE-AA-015 | P1       | 3    | medium     | Declare an explicit Redis cache manager contract              | none          |
| 14    | CHANGE-AA-014 | P1       | 3    | low        | Contain Redis cache failures                                  | none          |
| 15    | CHANGE-AA-016 | P1       | 3    | low        | Coalesce concurrent cache misses                              | none          |
| 16    | CHANGE-AA-018 | P1       | 3    | medium     | Make Kafka publication durable and observable                 | none          |
| 17    | CHANGE-AA-019 | P1       | 3    | high       | Own the listener error, offset, and dead-letter contract      | none          |
| 18    | CHANGE-AA-020 | P1       | 3    | high       | Recover from credential rotation without a restart            | none          |
| 19    | CHANGE-AA-012 | P1       | 3    | medium     | Give dependency failures stable caller-visible semantics      | blocking      |
| 20    | CHANGE-AA-017 | P1       | 3    | medium     | Bound the inventory list endpoint                             | blocking      |
| 21    | CHANGE-AA-023 | P2       | 4    | low        | Invalidate the cache on reserve and release                   | none          |
| 22    | CHANGE-AA-021 | P2       | 4    | high       | Adopt a transactional outbox                                  | blocking      |
| 23    | CHANGE-AA-022 | P2       | 4    | medium     | Give published events a stable identity                       | blocking      |
| 24    | CHANGE-AA-024 | P0       | 4    | high       | Build the failure and failover regression suite               | none          |

```yaml
backlog_notes:
  approval_gate_legend:
    none: Every target may be implemented on approval of this plan.
    partial: Some targets are implementable now; at least one target is held pending approval.
    blocking: The change carries change_boundary.implementation_allowed false at the change level.
  ordering_rule: >-
    Ordered by wave, then by dependency, then by governed priority. CHANGE-AA-005 and CHANGE-AA-006 are
    placed first inside Wave 1 because CHANGE-AA-001 and CHANGE-AA-007 both consume the telemetry they
    introduce.
  date_estimates: not_provided
  sprint_mapping: not_provided
  estimation_note: >-
    No dates, durations, or sprint boundaries are implied. Complexity is a relative sizing signal only.
```

## 8. Implementation Waves

```yaml
implementation_waves:
  - wave: 1
    name: Platform contract
    objective: >-
      Establish accurate regional traffic eligibility, a safe startup path, an ordered termination path,
      and telemetry with a region dimension, so that every subsequent change can be observed and
      validated.
    change_ids: [CHANGE-AA-005, CHANGE-AA-006, CHANGE-AA-001, CHANGE-AA-002, CHANGE-AA-003, CHANGE-AA-004]
    priorities_present: [P0]
    parallelizable_groups:
      - [CHANGE-AA-005, CHANGE-AA-002, CHANGE-AA-003]
      - [CHANGE-AA-006]
      - [CHANGE-AA-001]
      - [CHANGE-AA-004]
    entry_criteria:
      - This plan is approved.
    exit_criteria:
      - Readiness reflects Azure SQL health and liveness does not.
      - No profile performs runtime DDL.
      - Key Vault startup is bounded.
      - Shutdown withdraws readiness, stops listeners, and drains.
      - Every metric and log record carries a region and role dimension and at least one failure signal exists.
    decisions_required:
      - Platform termination grace period, to bound the drain window.
      - Approved Key Vault client budgets.
      - Approved migration runner or confirmation of an externally governed migration process.
  - wave: 2
    name: Regional ownership and replay safety
    objective: >-
      Make regional consumption a configuration decision and make authoritative writes safe to replay,
      which together make the approved active-standby promotion procedure executable.
    change_ids: [CHANGE-AA-008, CHANGE-AA-007]
    priorities_present: [P0]
    parallelizable_groups:
      - [CHANGE-AA-008]
      - [CHANGE-AA-007]
    entry_criteria:
      - Wave 1 exit criteria met.
    exit_criteria:
      - A repeated order event produces exactly one stock movement.
      - Consumption can be disabled and enabled by configuration with no code change, and the state is observable.
    decisions_required:
      - Approved retention window for processed-operation records.
      - Approved REST idempotency-key contract, for the gated portion of CHANGE-AA-008.
      - Architecture direction on a self-enforced ownership mechanism.
  - wave: 3
    name: Region-agnostic resiliency mechanisms
    objective: >-
      Install the bounded-failure, retry, isolation, cache, and messaging mechanisms that preserve current
      production behaviour once the service runs in more than one region.
    change_ids:
      - CHANGE-AA-009
      - CHANGE-AA-010
      - CHANGE-AA-013
      - CHANGE-AA-011
      - CHANGE-AA-015
      - CHANGE-AA-014
      - CHANGE-AA-016
      - CHANGE-AA-018
      - CHANGE-AA-019
      - CHANGE-AA-020
      - CHANGE-AA-012
      - CHANGE-AA-017
    priorities_present: [P1]
    parallelizable_groups:
      - [CHANGE-AA-009, CHANGE-AA-015, CHANGE-AA-014, CHANGE-AA-020, CHANGE-AA-017]
      - [CHANGE-AA-010, CHANGE-AA-016, CHANGE-AA-018]
      - [CHANGE-AA-013, CHANGE-AA-011, CHANGE-AA-019, CHANGE-AA-012]
    entry_criteria:
      - Wave 2 exit criteria met.
      - Resilience4j version source confirmed.
    exit_criteria:
      - Every remote call has a bounded, externalized deadline.
      - A transient database transition is survivable without operator action.
      - A single degraded dependency does not remove the pod from service.
      - The cached read path works, expires, and is namespaced.
      - Publication outcome is observed and listener failures are quarantined rather than dropped.
    decisions_required:
      - Approved gateway and load balancer budgets, to order the application deadlines.
      - Approved concurrency limits and breaker thresholds.
      - Approved cache time-to-live.
      - Approved dead-letter destination name.
      - API contract owner approval for CHANGE-AA-012 and CHANGE-AA-017.
  - wave: 4
    name: Architectural patterns and verification
    objective: >-
      Adopt the cross-store consistency and event identity patterns, correct the remaining cache
      invalidation defect, and prove the whole failure model with a regression suite.
    change_ids: [CHANGE-AA-023, CHANGE-AA-021, CHANGE-AA-022, CHANGE-AA-024]
    priorities_present: [P0, P2]
    parallelizable_groups:
      - [CHANGE-AA-023]
      - [CHANGE-AA-021, CHANGE-AA-022]
      - [CHANGE-AA-024]
    entry_criteria:
      - Wave 3 exit criteria met.
      - Architecture and event-contract owner approval for CHANGE-AA-021 and CHANGE-AA-022.
    exit_criteria:
      - No production path publishes inside an active transaction.
      - Republication of the same business operation carries an identical event identity.
      - Reserve and release invalidate the cached entry.
      - The regression suite passes and fails on a managed-version regression.
    decisions_required:
      - Architecture approval for the transactional outbox and the relay execution model.
      - Event-contract owner approval for the envelope change, coordinated with EG-011.
      - Confirmation that CI provides a Docker daemon.
    wave_priority_note: >-
      CHANGE-AA-024 is P0 but sits in this wave because the consolidated suite depends on every other
      change. Wave placement is a dependency statement, not a priority statement, and each change carries
      its own tests in its own wave.
```

```yaml
dependency_integrity:
  every_change_in_exactly_one_wave: true
  prerequisites_in_earlier_or_equal_wave: true
  cross_wave_violations: 0
  circular_dependencies: 0
  changes_with_no_prerequisites: 8
  longest_dependency_chain:
    - CHANGE-AA-005
    - CHANGE-AA-006
    - CHANGE-AA-008
    - CHANGE-AA-018
    - CHANGE-AA-021
    - CHANGE-AA-024
```

## 9. Validation Strategy

```yaml
validation_strategy:
  build_command: "mvn -f source/inventory-service/pom.xml verify"
  unit_test_command: "mvn -f source/inventory-service/pom.xml test"
  resiliency_suite_command: "mvn -f source/inventory-service/pom.xml -Dtest='com.ecommerce.inventory.resiliency.*' test"
  static_analysis: not_configured_in_repository
  prerequisites:
    - Docker daemon available for Testcontainers; the existing suite already guards on disabledWithoutDocker.
    - No live Azure dependency is required by any proposed test.
  per_wave_gates:
    wave_1:
      - Readiness reports OUT_OF_SERVICE on authoritative dependency loss and UP after restoration, with no restart.
      - Liveness stays UP throughout a dependency outage.
      - Startup applies no DDL and fails fast on a schema mismatch.
      - Key Vault startup failure occurs within the declared budget.
      - Shutdown emits readiness withdrawal before the servlet container stops.
      - Every meter and log record carries region and role.
    wave_2:
      - Duplicate delivery of one order event yields exactly one stock movement.
      - Full replay of retained history yields no additional stock movement.
      - Consumption disabled by configuration consumes nothing while readiness stays UP.
      - Activation state is observable and reversible without a redeploy.
    wave_3:
      - Every dependency deadline resolves to a positive bounded value.
      - Transient database failure is retried; business failure is not.
      - A saturated dependency leaves Actuator endpoints responsive.
      - Cached read succeeds against a real Redis and the entry carries a TTL and a namespaced key.
      - Redis outage yields a successful read from the authoritative store.
      - Publication failure is counted and logged.
      - A poison record is quarantined before the offset advances.
    wave_4:
      - No publication occurs for a rolled-back transaction.
      - An exhausted outbox record reaches an explicit terminal status.
      - Republication carries an identical event identity.
      - Reserve and release evict the cached entry and a rollback does not.
      - The effective-configuration guard fails on a managed default change.
  consolidated_regression_gate:
    change_id: CHANGE-AA-024
    requirement: >-
      The consolidated suite must pass before the remediation is considered complete. Individual wave
      gates are necessary but not sufficient.
  closure_evidence_required_for_step_5:
    - Repository evidence for each modified file and symbol.
    - Passing output for each validation command listed on the closed change.
    - The approval record for every approval-gated target that was implemented.
    - A recorded deviation for any change implemented differently from this plan.
  testing_visibility_note: >-
    report_preferences.testing_output is hidden. That setting suppresses test detail in the Step 3B
    report only. Every obligation in this section remains binding on Step 4 and Step 5.
```

## 10. Risks, Assumptions, and Open Questions

### Assumptions

```yaml
assumptions:
  - id: ASM-001
    statement: >-
      Azure SQL remains the single authoritative business state and the approved active-standby database
      model is unchanged.
    source: approved application architecture context version 3.0.0
    invalidation_impact: Would invalidate the idempotency, outbox, and readiness designs.
  - id: ASM-002
    statement: >-
      The Kafka operating scenario remains active_standby with a single_active regional processing model.
    source: approved application architecture context, validated under KAFKA-SCENARIO-001
    invalidation_impact: Would change CHANGE-AA-007 and CHANGE-AA-019 materially.
  - id: ASM-003
    statement: >-
      Container build, CI/CD, deployment configuration, and infrastructure remain outside the remediation
      boundary for this cycle.
    source: application-context/assessment-scope-context.yml
    invalidation_impact: Would add JVM, probe timing, and termination grace remediation currently recorded as EG-005.
  - id: ASM-004
    statement: >-
      Resilience4j is the approved resiliency library and no substitution is permitted.
    source: grounding/governance/approved-libraries.yml lifecycle_status approved
    invalidation_impact: Would require re-resolution of CHANGE-AA-010, CHANGE-AA-011, and CHANGE-AA-013.
  - id: ASM-005
    statement: >-
      The deployment supplies a value for every externalized placeholder introduced by this plan.
    source: repository evidence that every endpoint already resolves from an environment placeholder
    invalidation_impact: A missing value would cause a startup binding failure rather than a silent default.
  - id: ASM-006
    statement: >-
      Downstream consumers of inventory-events are owned outside this repository and cannot be modified
      by this remediation.
    source: approved context declares no downstream_dependencies; repository evidence shows no consumer
    invalidation_impact: Would change the approval path for CHANGE-AA-021 and CHANGE-AA-022.
```

### Cross-cutting risks

```yaml
cross_cutting_risks:
  - id: RISK-X-001
    description: >-
      Wave 3 introduces bounded failures where the service previously stalled, but the caller-visible
      status contract that explains those failures is approval-gated in CHANGE-AA-012. Until approval
      lands, callers see an opaque 500 for a now-faster failure.
    affected_changes: [CHANGE-AA-009, CHANGE-AA-010, CHANGE-AA-013, CHANGE-AA-012]
    mitigation: >-
      Prioritize the CHANGE-AA-012 approval decision early in Wave 3 so the two land together.
  - id: RISK-X-002
    description: >-
      CHANGE-AA-021 makes publication at-least-once while CHANGE-AA-022 supplies the identity downstream
      consumers need to deduplicate. Releasing the outbox without the envelope would push duplicates
      outward with no defence.
    affected_changes: [CHANGE-AA-021, CHANGE-AA-022]
    mitigation: Both are placed in Wave 4 and must be released together.
  - id: RISK-X-003
    description: >-
      Several remediations depend on budget values that can only be derived from gateway and load
      balancer configuration recorded as EG-006, which is outside the assessment boundary.
    affected_changes: [CHANGE-AA-009, CHANGE-AA-010, CHANGE-AA-013, CHANGE-AA-004]
    mitigation: >-
      Every value is externalized rather than fixed, so the code change can land before the numbers are
      settled. The numbers become a deployment configuration decision, not a code change.
  - id: RISK-X-004
    description: >-
      CHANGE-AA-007 supplies a deployment-controlled activation mechanism but not a self-enforced one,
      so an operator error can still produce a both-active condition.
    affected_changes: [CHANGE-AA-007]
    mitigation: >-
      The activation gauge plus the region tag makes the condition detectable, and the residual gap is
      recorded as OQ-007 for architecture governance rather than silently accepted.
  - id: RISK-X-005
    description: >-
      Switching ddl-auto to validate will fail startup in any environment whose implicitly created schema
      has drifted from the entity model.
    affected_changes: [CHANGE-AA-002]
    mitigation: A pre-cutover schema comparison in each environment is an explicit acceptance criterion.
```

### Open questions

```yaml
open_questions:
  - id: OQ-001
    change_id: CHANGE-AA-001
    question: >-
      Once CHANGE-AA-007 supplies the region-role contract, should the Kafka contributor join the
      readiness group in the active region only, and what health-check caching interval is approved?
    route_to: architecture_governance_review
    blocking: false
  - id: OQ-002
    change_id: CHANGE-AA-002
    question: Which versioned schema-migration mechanism is approved, and does it execute in-process or as a separate release step?
    route_to: architecture_governance_review
    blocking: true
    blocks_targets: [ICB-002-03]
  - id: OQ-003
    change_id: CHANGE-AA-003
    question: What connect, response, and retry budgets are approved for the Key Vault client during a regional recovery?
    route_to: platform_evidence_request
    blocking: false
  - id: OQ-004
    change_id: CHANGE-AA-004
    question: >-
      The prioritization policy heading names the graceful-shutdown rule P0-AA-014 while the embedded
      rule body declares rule_id P0-RCV-014. The policy also references P0-AA-011 in the P2 elevation
      rule but defines no rule with that identifier; the defined data-integrity rule is P0-AA-012. Which
      identifiers are authoritative?
    route_to: policy_governance
    blocking: false
    planner_action: >-
      Heading identifiers were cited throughout this plan and the discrepancies are recorded rather than
      resolved. No priority outcome depends on the resolution.
  - id: OQ-005
    change_id: CHANGE-AA-004
    question: What is the platform termination grace period, so the application drain window can be set shorter than it?
    route_to: platform_evidence_request
    blocking: false
    related_evidence_gap: EG-005
  - id: OQ-006
    change_id: CHANGE-AA-005
    question: Which deployment mechanism supplies APP_DEPLOYMENT_REGION and APP_DEPLOYMENT_ROLE, and what is the approved value vocabulary?
    route_to: platform_evidence_request
    blocking: false
  - id: OQ-007
    change_id: CHANGE-AA-007
    question: >-
      Is a self-enforced ownership lease with an epoch or fencing token required, and if so may it reside
      in the existing Azure SQL authoritative store?
    route_to: architecture_governance_review
    blocking: true
    blocks_targets: [ICB-007-03]
  - id: OQ-008
    change_id: CHANGE-AA-007
    question: How is standby-region consumption prevented today, if at all?
    route_to: architecture_governance_review
    blocking: false
    related_evidence_gap: EG-010
  - id: OQ-009
    change_id: CHANGE-AA-008
    question: What retention window applies to processed-operation records, and what purges them?
    route_to: architecture_governance_review
    blocking: false
  - id: OQ-010
    change_id: CHANGE-AA-008
    question: >-
      What is the approved REST idempotency-key contract for POST reserve and release, including behaviour
      for an absent or blank referenceId?
    route_to: product_and_api_contract_approval
    blocking: true
    blocks_targets: [rest_idempotency_key_contract]
  - id: OQ-011
    change_id: CHANGE-AA-009
    question: What are the approved gateway, mesh, and load balancer budgets against which the application deadlines must be ordered?
    route_to: platform_evidence_request
    blocking: false
    related_evidence_gap: EG-006
  - id: OQ-012
    change_id: CHANGE-AA-010
    question: >-
      approved-libraries.yml sets library_rules.version_source to not_specified and the Spring Boot 3.3.5
      parent does not manage Resilience4j. Is the version supplied by a BOM import or a managed property?
    route_to: platform_governance
    blocking: false
  - id: OQ-013
    change_id: CHANGE-AA-011
    question: What HTTP status and response body are approved for an unresolvable inventory write conflict?
    route_to: product_and_api_contract_approval
    blocking: true
    blocks_targets: [conflict_http_status_mapping]
  - id: OQ-014
    change_id: CHANGE-AA-012
    question: What HTTP status, Retry-After policy, and error-code vocabulary are approved for a transient dependency failure?
    route_to: product_and_api_contract_approval
    blocking: true
    blocks_targets: [dependency_failure_status_contract]
  - id: OQ-015
    change_id: CHANGE-AA-013
    question: What concurrency limits, failure-rate thresholds, window sizes, open durations, and half-open call counts are approved?
    route_to: architecture_governance_review
    blocking: false
  - id: OQ-016
    change_id: CHANGE-AA-015
    question: What inventory cache time-to-live is approved, and which deployment value supplies the environment qualifier in the key prefix?
    route_to: architecture_governance_review
    blocking: false
  - id: OQ-017
    change_id: CHANGE-AA-017
    question: >-
      What pagination contract is approved for GET /api/v1/inventory, and how are existing callers
      migrated?
    route_to: product_and_api_contract_approval
    blocking: true
    blocks_targets: [list_endpoint_response_contract]
  - id: OQ-018
    change_id: CHANGE-AA-018
    question: What acks, idempotence, and in-flight settings are approved, given the broker replication configuration?
    route_to: platform_evidence_request
    blocking: false
    related_evidence_gap: EG-002
  - id: OQ-019
    change_id: CHANGE-AA-019
    question: What dead-letter destination name, retention, and access policy apply to quarantined order events?
    route_to: platform_evidence_request
    blocking: false
  - id: OQ-020
    change_id: CHANGE-AA-020
    question: >-
      What is the approved credential rotation model, and does Redis authentication use an access key or
      a managed identity token?
    route_to: platform_evidence_request
    blocking: true
    blocks_targets: [ICB-020-03]
    related_evidence_gap: EG-003
  - id: OQ-021
    change_id: CHANGE-AA-021
    question: Is the transactional outbox pattern approved, and what relay execution model is approved?
    route_to: architecture_governance_review
    blocking: true
    blocks_targets: [publication_timing_and_delivery_semantics]
  - id: OQ-022
    change_id: CHANGE-AA-021
    question: What retention and purge policy applies to published and failed outbox records?
    route_to: architecture_governance_review
    blocking: false
  - id: OQ-023
    change_id: CHANGE-AA-022
    question: What event envelope contract, schema versioning scheme, and header vocabulary are approved for inventory-events?
    route_to: architecture_governance_review
    blocking: true
    blocks_targets: [published_event_envelope_contract]
    related_evidence_gap: EG-011
  - id: OQ-024
    change_id: CHANGE-AA-023
    question: >-
      The prioritization policy contains no rule addressing a normal-operation data-correctness defect
      outside the active-active resiliency frame. F-020 is a critical-severity correctness defect that
      lands at P2 under the closest applicable rule. Should the policy gain a correctness rule?
    route_to: policy_governance
    blocking: false
    planner_action: >-
      P2-DATA-010 was cited as the closest applicable rule and the coverage gap is recorded. No priority
      was invented.
  - id: OQ-025
    change_id: CHANGE-AA-024
    question: Does the CI environment provide a Docker daemon for the Testcontainers-based fault-injection suite?
    route_to: platform_evidence_request
    blocking: false
```

### Approval-required target register

```yaml
approval_required_targets:
  - target_id: rest_idempotency_key_contract
    change_id: CHANGE-AA-008
    classification: business_logic_change
    approval_status: not_available
    implementation_allowed: false
    owner: product_and_api_contract_owner
    open_question: OQ-010
  - target_id: conflict_http_status_mapping
    change_id: CHANGE-AA-011
    classification: partner_contract_change
    approval_status: not_available
    implementation_allowed: false
    owner: api_contract_owner
    open_question: OQ-013
  - target_id: dependency_failure_status_contract
    change_id: CHANGE-AA-012
    classification: partner_contract_change
    approval_status: not_available
    implementation_allowed: false
    owner: api_contract_owner
    open_question: OQ-014
  - target_id: list_endpoint_response_contract
    change_id: CHANGE-AA-017
    classification: partner_contract_change
    approval_status: not_available
    implementation_allowed: false
    owner: api_contract_owner
    open_question: OQ-017
  - target_id: publication_timing_and_delivery_semantics
    change_id: CHANGE-AA-021
    classification: partner_contract_change
    approval_status: not_available
    implementation_allowed: false
    owner: architecture_and_event_contract_owner
    open_question: OQ-021
  - target_id: published_event_envelope_contract
    change_id: CHANGE-AA-022
    classification: partner_contract_change
    approval_status: not_available
    implementation_allowed: false
    owner: event_contract_owner
    open_question: OQ-023
security_and_privacy_preservation:
  pii_scrubbing_removed_or_weakened: false
  logging_sanitization_removed_or_weakened: false
  authentication_or_authorization_changed: false
  encryption_tokenization_or_masking_changed: false
  validation_behavior_removed: false
  note: >-
    No change removes, weakens, or bypasses a security, privacy, redaction, authentication,
    authorization, encryption, or validation behaviour. Every new log record, metric name, metric tag,
    and error response is explicitly constrained to exclude payload values, credentials, connection
    strings, and stack detail. The existing show-details never health posture is preserved and
    CHANGE-AA-001 restates it explicitly. CCG-003 records the absence of business-API authorization as a
    control coverage gap; it is routed to grounding standard governance and is deliberately not converted
    into remediation work here.
```

## 11. Step 3B Report Handoff Contract

```yaml
report_handoff:
  artifact_role: authoritative_report_input
  next_phase: assessment_report_generation
  next_prompt: 03B-create-code-level-resiliency-assessment-report-schema-governed.prompt.md
  inventory_artifact: ".copilot-tracking/research/2026-09-18/inventory-service-inventory-research.md"
  review_artifact: ".copilot-tracking/reviews/2026-09-18/inventory-service-inventory-research-review.md"
  remediation_plan_artifact: ".copilot-tracking/plans/2026-09-18/inventory-service-remediation-plan.instructions.md"
  inventory_reuse_required: true
  review_reuse_required: true
  remediation_plan_reuse_required: true
  re_inventory_allowed: false
  reassessment_allowed: false
  new_findings_allowed: false
  report_must_preserve_finding_status: true
  report_must_preserve_priority: true
  report_must_preserve_finding_classification: true
  illustrative_code_must_be_labeled: true
  infrastructure_findings_allowed: false
  pcf_findings_allowed: false
  report_finding_selection:
    mode: all_priorities
    included_priorities: [P0, P1, P2, P3]
    omitted_priorities: []
    include_conditional_findings: true
    include_verified_controls: false
    include_evidence_gaps: true
    selection_frozen: true
    included_finding_ids:
      - F-001
      - F-002
      - F-003
      - F-004
      - F-005
      - F-006
      - F-007
      - F-008
      - F-009
      - F-010
      - F-011
      - F-012
      - F-013
      - F-014
      - F-015
      - F-016
      - F-017
      - F-018
      - F-019
      - F-020
      - F-021
      - F-022
      - F-023
      - F-024
      - F-025
      - F-026
      - F-027
      - F-028
      - F-029
    omitted_finding_ids: []
    included_change_ids:
      - CHANGE-AA-001
      - CHANGE-AA-002
      - CHANGE-AA-003
      - CHANGE-AA-004
      - CHANGE-AA-005
      - CHANGE-AA-006
      - CHANGE-AA-007
      - CHANGE-AA-008
      - CHANGE-AA-009
      - CHANGE-AA-010
      - CHANGE-AA-011
      - CHANGE-AA-012
      - CHANGE-AA-013
      - CHANGE-AA-014
      - CHANGE-AA-015
      - CHANGE-AA-016
      - CHANGE-AA-017
      - CHANGE-AA-018
      - CHANGE-AA-019
      - CHANGE-AA-020
      - CHANGE-AA-021
      - CHANGE-AA-022
      - CHANGE-AA-023
      - CHANGE-AA-024
    omitted_change_ids: []
  report_testing_output:
    mode: hidden
    show_test_findings: true
    show_test_code: false
    show_validation_commands: false
    show_acceptance_criteria: false
    show_validation_evidence: false
    include_consolidated_validation_strategy: false
    authority_note: >-
      Hidden testing output affects report rendering only. F-028 remains a reported finding and
      CHANGE-AA-024 remains a reported P0 change; only the test detail is suppressed in the report.
  report_finding_classification_output:
    include_resiliency_findings: true
    include_non_resiliency_findings: true
    report_section_order: [resiliency, non_resiliency]
    priority_order_within_each_class: [P0, P1, P2, P3]
    resiliency_finding_count: 26
    non_resiliency_finding_count: 3
    non_resiliency_finding_ids: [F-018, F-020, F-029]
```

## 12. Step 4 Task Implementor Handoff Contract

```yaml
handoff:
  artifact_role: authoritative_remediation_plan
  next_phase: implementation
  next_agent: task-implementor
  next_prompt: 04-implement-approved-remediation-complete-priority-aware.prompt.md
  plan_artifact: ".copilot-tracking/plans/2026-09-18/inventory-service-remediation-plan.instructions.md"
  approved_change_selectors_supported:
    - priorities
    - waves
    - change_ids
  approved_change_ids_required: false
  re_inventory_allowed: false
  reassessment_allowed: false
  unrelated_refactoring_allowed: false
  source_modification_allowed_in_next_phase: true
  illustrative_code_is_authoritative_patch: false
  implementation_must_validate_repository_context: true
  deviations_must_be_recorded: true
  new_findings_allowed: false
  infrastructure_changes_allowed: false
  pcf_changes_allowed: false
  scope_constraints:
    modifiable_artifact_classes:
      - application_code
      - application_configuration
      - repository_owned_build_file
      - repository_owned_test_source
    prohibited_artifact_classes:
      - source/inventory-service/Dockerfile
      - source/inventory-service/.github/workflows/ci-cd.yml
      - source/inventory-service/k8s/
      - any deployed infrastructure
    prohibited_reason: assessment_domain_disabled
  implementation_gates:
    - gate: approval_required_targets
      rule: >-
        Do not implement any target listed in the approval-required target register until an approval
        record exists. Implement the sibling targets inside the same change normally.
      targets:
        - rest_idempotency_key_contract
        - conflict_http_status_mapping
        - dependency_failure_status_contract
        - list_endpoint_response_contract
        - publication_timing_and_delivery_semantics
        - published_event_envelope_contract
    - gate: targeted_discovery_targets
      rule: >-
        Resolve the named unresolved input before implementing the target. Do not select a technology,
        product, or mechanism on the organization's behalf.
      targets: [ICB-002-03, ICB-007-03, ICB-020-03]
    - gate: dependency_ordering
      rule: >-
        Honour depends_on_change_ids. CHANGE-AA-010 must not be implemented before CHANGE-AA-008, because
        retry of a non-idempotent write duplicates a stock movement.
    - gate: externalized_values
      rule: >-
        Every timeout, retry, backoff, threshold, window, TTL, and page size introduced by this plan must
        remain externally configurable. Do not substitute a hardcoded value for a placeholder.
  snapshot_drift_handling:
    assessment_snapshot_type: workspace_snapshot
    git_commit_sha: not_applicable
    rule: >-
      Line numbers in this plan are advisory. Locate each target by repository path and symbol, then
      confirm the original source excerpt and, where present, the sha256 fingerprint before editing. If
      the excerpt no longer matches, record a drift deviation and stop for that target rather than
      guessing.
  library_governance:
    approved_libraries_path: grounding/governance/approved-libraries.yml
    lifecycle_status: approved
    approved_resiliency_library: resilience4j
    approved_capabilities: [circuit_breaker, retry, bulkhead, time_limiter]
    substitution_allowed: false
    version_source: not_specified
    version_source_unresolved: true
    unmanaged_version_invention_allowed: false
  scenario_preservation:
    kafka_operating_scenario: active_standby
    scenario_redesign_allowed: false
    new_datastore_introduction_allowed: false
    note: >-
      Both new tables proposed by this plan reside in the Azure SQL authoritative store the approved
      architecture already declares.
```

## Completion Validation

```yaml
completion_validation:
  phase: remediation_planning
  status: passed
  core_planning:
    every_change_maps_to_an_approved_noncompliant_finding: true
    every_approved_finding_mapped_exactly_once: true
    new_findings_created: 0
    new_dependencies_created: 0
    control_status_changes: 0
    repository_files_modified: 0
    unique_change_ids: 24
    every_change_has_wave_complexity_objective_criteria_commands_risks_rollback_dependencies: true
    priority_assigned_only_through_governed_policy: true
    every_change_cites_policy_id_version_and_rule_id: true
    priority_derived_from_severity: false
    p2_data_correctness_candidates_evaluated_for_p0_elevation: true
    p0_elevations_applied: 0
    p0_elevation_evaluations_recorded: 7
    tests_inherit_behavior_priority: true
    priority_index_contains_every_change_once: true
    wave_index_contains_every_change_once: true
    deployed_infrastructure_remediation_added: false
    pcf_remediation_added: false
  source_evidence_and_targeting:
    step_2_paths_symbols_excerpts_fingerprints_snapshots_preserved_verbatim: true
    original_source_regenerated_or_normalized: false
    original_source_target_and_proposal_kept_separate: true
    targeting_precedence_applied: true
    line_numbers_marked_non_authoritative: true
    missing_git_suppressed_planning: false
    evidence_limitations_explicit: true
    evidence_not_available_records_preserved: 1
    evidence_not_available_ids: [EV-F-008-02]
  illustrative_code:
    every_target_has_exactly_one_status: true
    targets_with_sufficient_evidence_generated: 86
    narrative_text_in_illustrative_code: 0
    comment_only_blocks: 0
    remediation_divided_into_independent_targets: true
    multi_file_changes_have_proposals_for_every_unblocked_target: true
    targeted_discovery_scoped_to_blocked_target_only: true
    every_targeted_discovery_record_names_the_blocking_fact: true
    unresolved_decisions_suppressed_neutral_contracts: false
    unrelated_findings_combined_to_avoid_code: false
    hardcoded_regions_endpoints_credentials_or_unapproved_numbers: 0
    all_proposals_labeled_non_authoritative: true
    narrative_only_generated_proposals: 0
    coverage_complete: true
  business_logic_security_and_privacy:
    every_target_has_change_boundary_classification: true
    directly_implementable_targets_preserve_business_semantics: true
    http_status_reinterpreted_without_approval: false
    outcome_classification_changed_without_approval: false
    new_external_interaction_proposed_as_directly_implementable: false
    fallback_retry_compensation_reconciliation_changed_without_approval: false
    security_privacy_or_validation_behavior_weakened: false
    mixed_changes_isolate_eligible_targets: true
    approval_required_targets_blocked: 6
    approval_required_targets_implementation_allowed_false: true
  approved_library:
    every_vendor_specific_proposal_has_library_resolution: true
    governance_used_only_when_lifecycle_status_approved: true
    selected_capabilities_listed_under_approved_capabilities: true
    product_approval_and_repository_availability_evaluated_separately: true
    dependency_presence_treated_as_approval: false
    policy_approval_treated_as_availability: false
    version_source_strategy_followed: true
    unmanaged_version_or_unsupported_api_invented: false
    missing_approval_blocked_only_vendor_specific_targets: true
    new_finding_created_because_of_library_governance_gap: false
  handoff_and_completion:
    report_handoff_present: true
    implementor_handoff_present: true
    priority_and_wave_indexes_frozen: true
    handoff_summary_written: true
    handoff_summary_path: ".copilot-tracking/plans/handoffs/03A-planning-summary.yml"
    handoff_summary_non_authoritative: true
    unresolved_decisions_reported: 25
    governance_blocked_changes: 0
  governance_observations:
    - id: GOV-001
      observation: >-
        The prioritization policy heading names the graceful-shutdown rule P0-AA-014 while the embedded
        rule body declares rule_id P0-RCV-014.
      planner_action: Cited the heading identifier and recorded the discrepancy as OQ-004.
    - id: GOV-002
      observation: >-
        The P2 elevation rule directs elevation under P0-AA-011, but no rule with that identifier is
        defined. The defined data-integrity rule is P0-AA-012.
      planner_action: >-
        Elevation evaluations reference P0-AA-012 and the discrepancy is recorded as OQ-004. No elevation
        outcome depends on the resolution, because no candidate was elevated.
    - id: GOV-003
      observation: >-
        The policy has no rule for a normal-operation data-correctness defect outside the active-active
        resiliency frame, which affects F-020.
      planner_action: Cited the closest applicable rule P2-DATA-010 and recorded the gap as OQ-024.
```

