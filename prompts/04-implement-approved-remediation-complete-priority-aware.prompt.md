# Prompt 4: Implement Approved Multi-Region Remediation Changes

## Agent and phase

Run this prompt in a new VS Code Copilot Chat session using the HVE implementation capability.

Preferred execution model:

1. Select HVE `task-implementor` when it is available and authorized to modify the repository.
2. Invoke or follow the HVE `/rpi-implement` phase workflow.
3. If `task-implementor` is unavailable, use the RPI Agent constrained to the implementation phase only.

This phase may modify source code, repository application configuration, and automated tests, but only for the resolved and approved remediation scope.

## Required inputs

Provide the exact artifact paths and at least one approval selector:

```text
INVENTORY_ARTIFACT=.copilot-tracking/research/YYYY-MM-DD/springboot-active-active-inventory-research.md
REVIEW_ARTIFACT=.copilot-tracking/reviews/YYYY-MM-DD/springboot-active-active-inventory-review.md
PLAN_ARTIFACT=.copilot-tracking/plans/YYYY-MM-DD/springboot-active-active-remediation-plan.md

APPROVED_PRIORITIES=P0,P1
APPROVED_WAVES=
APPROVED_CHANGE_IDS=
```

Empty selectors are allowed, but at least one selector must contain a value.

Read:

1. The authoritative Step 1 inventory artifact.
2. The authoritative Step 2 review artifact, including findings and control results.
3. The authoritative Step 3 remediation plan.
4. The grounded controls referenced by the changes selected for implementation.
5. `assessment/grounding/governance/remediation-prioritization.md` for policy traceability only.

Do not recalculate, reinterpret, or override the priority assigned by Task Planner.

## Approval selector precedence

Resolve implementation scope using this precedence:

1. `APPROVED_PRIORITIES`
2. `APPROVED_WAVES`
3. `APPROVED_CHANGE_IDS`

The first non-empty selector wins.

Examples:

- If `APPROVED_PRIORITIES=P0,P1`, ignore waves and change IDs.
- If priorities are empty and `APPROVED_WAVES=1,2`, ignore change IDs.
- If priorities and waves are empty, use `APPROVED_CHANGE_IDS`.

Priority-based selection is preferred because it applies the governed remediation policy consistently across the plan.

Do not combine selectors. Do not silently broaden or narrow the selected scope.

## Scope-resolution algorithm

Before modifying any file:

1. Read all planned changes from the authoritative plan.
2. Validate that each planned change has a stable `change_id`.
3. Validate that each planned change has a governed priority object containing:
   - `value`
   - `policy_id`
   - `policy_version`
   - `rule_id`
4. Select the first non-empty approval selector according to the precedence rules.
5. Resolve that selector into a concrete list of change IDs.
6. Sort the resolved IDs deterministically by implementation wave and then change ID.
7. Confirm that every resolved ID exists in the authoritative plan.
8. Confirm that every resolved ID maps to at least one approved `non_compliant` finding.
9. Confirm that no resolved change is marked excluded, accepted risk, already superseded, or blocked from implementation by the plan.
10. Freeze the resolved change list before implementation begins.

If no change ID resolves from the selected priorities, waves, or IDs, stop without changing source code and report the empty scope.

## Required frozen implementation scope

Record the selection request and its resolved change IDs in the authoritative implementation artifact:

```yaml
implementation_scope:
  selection_method: priority
  selector_precedence:
    - priority
    - wave
    - change_id
  requested_priorities:
    - P0
    - P1
  requested_waves: []
  requested_change_ids: []
  ignored_selectors:
    waves: []
    change_ids: []
  resolved_change_ids:
    - CHANGE-AA-001
    - CHANGE-AA-002
  resolved_change_count: 2
  scope_frozen: true
  scope_resolution_source: authoritative_remediation_plan
  plan_artifact: <exact Step 3 plan path>
  plan_policy_id: AA-REMEDIATION-PRIORITY
  plan_policy_version: "1.0.0"
  scope_fingerprint: <stable hash or deterministic identifier when available>
```

All implementation activity must use `resolved_change_ids`.

Once frozen, do not add or remove change IDs. If a resolved change cannot be implemented, mark it blocked or partially implemented. Do not replace it with an unapproved change.

## Preconditions

Do not begin implementation unless:

- The inventory artifact identifies itself as the authoritative inventory.
- The Step 2 artifact identifies itself as the authoritative assessment or review record.
- The Step 3 plan identifies `artifact_role: authoritative_remediation_plan`.
- The Step 3 handoff identifies the implementation phase and implementation-capable agent.
- The selected approval scope resolves to at least one change ID.
- Every resolved change ID exists in the plan.
- Every resolved change maps to an approved noncompliant finding.
- The repository state is suitable for changes.

If a precondition fails, stop and report the blocking condition without modifying source code.

## Scope boundaries

Implement only the frozen `resolved_change_ids`.

Do not:

- Re-inventory the repository
- Repeat the multi-region assessment
- Reassess findings or controls
- Recalculate P0, P1, P2, or P3
- Implement priorities, waves, or change IDs outside the frozen scope
- Add unrelated refactoring
- Change public behavior unless required by the approved plan
- Add infrastructure-as-code or Azure deployment changes
- Add PCF work
- Commit, push, create a branch, or open a pull request unless explicitly requested
- Hide deviations from the approved plan

Targeted implementation discovery is allowed only inside files, symbols, configuration, and adjacent tests necessary for the frozen change scope.

If planning assumptions conflict with repository reality, adapt the implementation minimally while preserving the planned behavior and acceptance criteria. Record the deviation. Do not silently redesign the remediation.

## Illustrative code handling

Illustrative code in the Step 3 plan is non-authoritative.

Before applying it, validate:

- Package and class names
- Spring Boot and Java versions
- Synchronous or reactive application model
- Existing dependency-injection patterns
- Existing client wrappers and error handling
- Existing configuration conventions
- Existing test frameworks and conventions
- Library and API availability
- Compatibility with the repository build

Do not copy illustrative code blindly. Preserve the intended behavior and acceptance criteria using the repository's actual patterns.

## Implementation requirements

For every resolved change ID:

1. Confirm the mapped findings and controls.
2. Confirm the governed priority and rule ID from the plan.
3. Confirm affected files, symbols, tests, and acceptance criteria.
4. Record a concise pre-change evidence snapshot.
5. Modify the minimum necessary production code and repository application configuration.
6. Add or update the planned automated tests.
7. Preserve readiness versus liveness semantics.
8. Use deployment-injected regional endpoints without hardcoded region names.
9. Apply bounded timeout, retry, circuit-breaking, and recovery behavior when required.
10. Protect non-idempotent operations from unsafe retry.
11. Preserve secure identity and secret handling.
12. Preserve or improve recovery after dependency restoration without requiring a pod restart when required.
13. Run focused tests first, followed by approved broader build and test commands.
14. Record changed files, validation results, deviations, unresolved issues, and blockers.

## Readiness and liveness implementation rule

Unless the grounded control or approved plan explicitly states otherwise:

- Sustained loss of a critical local dependency should make the application not ready when it cannot safely provide its critical capability.
- External dependency failure should not normally make application liveness fail.
- Optional dependency failure should permit readiness when a safe degraded mode exists.
- Readiness should recover after dependency restoration without a process or pod restart.
- Health evaluation must be bounded and must not overload dependencies.

## Validation sequence

Use validation commands from the approved plan when available. Otherwise, use repository-native commands supported by the discovered build files.

Run in this order when applicable:

1. Formatting or static checks that do not introduce unrelated changes
2. Unit tests for changed components
3. Integration or fault tests mapped to acceptance criteria
4. Module build
5. Repository build when practical

Do not claim a command passed if it was not run.

Record command outcomes as:

- `passed`
- `failed`
- `blocked`
- `not_run`

Distinguish environmental limitations from product or code failures.

## Required implementation record

For every resolved change, record:

```yaml
- change_id: CHANGE-AA-001
  implementation_status: implemented
  finding_ids:
    - FINDING-KV-001
  control_ids:
    - KV-001
    - APP-AA-002
  priority:
    value: P0
    policy_id: AA-REMEDIATION-PRIORITY
    policy_version: "1.0.0"
    rule_id: P0-AA-003
  files_changed:
    - path: src/main/java/example/File.java
      action: modified
      symbols: []
      summary: ""
  tests_added_or_changed: []
  validation_commands:
    - command: "./mvnw test"
      result: passed
      evidence: ""
  acceptance_criteria_results:
    - criterion: ""
      result: passed
      evidence: ""
  plan_deviations: []
  unresolved_issues: []
```

Allowed implementation statuses:

- `implemented`
- `partially_implemented`
- `blocked`
- `not_started`

## Scope-control record

Also record:

```yaml
scope_control:
  files_changed_outside_resolved_scope: []
  unapproved_change_ids_implemented: []
  scope_violation_detected: false
  source_code_modified: true
  infrastructure_code_modified: false
  pcf_code_modified: false
  commit_created: false
  push_performed: false
  pull_request_created: false
```

A file needed by multiple approved changes is allowed. A supporting build or test file may be changed only when necessary to validate a resolved change and must identify the related change IDs.

## Output artifact

Use the HVE implementation artifact produced by `/rpi-implement` as the authoritative implementation record.

If the selected HVE implementation surface permits repository-owned outputs, also create:

- `assessment/outputs/implementation-results.yml`
- `assessment/outputs/implementation-summary.md`

If write permissions are constrained, do not fail. Preserve the required implementation scope, change evidence, validation evidence, and handoff in the HVE-authorized implementation artifact, then report its exact path.

## Step 5 handoff contract

End the implementation record with:

```yaml
handoff:
  artifact_role: authoritative_implementation_record
  next_phase: post_implementation_review
  next_agent: task-reviewer
  original_inventory_reuse_required: true
  original_findings_reuse_required: true
  approved_plan_reuse_required: true
  frozen_implementation_scope_reuse_required: true
  review_must_use_resolved_change_ids: true
  selector_recalculation_allowed: false
  re_inventory_allowed: false
  full_reassessment_allowed: false
  new_findings_allowed: false
  source_modification_allowed_in_review: false
  infrastructure_review_allowed: false
  pcf_review_allowed: false
```

## End-of-Phase Compact Handoff Summary

At the end of this phase, create one compact handoff summary under:

```text
.copilot-tracking/changes/handoffs/
```

Read and follow:

```text
grounding/governance/phase-handoff-schema.yml
```

The handoff summary is a non-authoritative index of facts already established by this phase. It supports state reconstruction after `/clear` or a new chat. It never replaces the authoritative phase artifact.

Requirements:

- Derive every value from the authoritative phase artifacts.
- Preserve stable finding, evidence, change, policy, scenario, and control IDs.
- Include exact authoritative input and output artifact paths.
- Include key decisions, counts, unresolved items, exceptions, and required next-phase inputs.
- Do not create findings, reassess controls, recalculate priority, change scenarios, invent evidence, authorize implementation, or modify source.
- When the summary conflicts with an authoritative artifact, the authoritative artifact wins and the handoff must record a `handoff_exception`.
- Report the generated handoff path in the completion response.

### Step 4 handoff

Write `.copilot-tracking/changes/handoffs/04-implementation-summary.yml`.

Include the frozen selection method, requested selector values, resolved change IDs, scope fingerprint, result by change, files changed, validation command results, deviations, blockers, and scope violations.

The handoff must copy the frozen implementation scope from the authoritative implementation record. It must not resolve selectors again.


## Completion validation

Before completing, verify that:

1. Approval selector precedence was applied exactly as defined.
2. The first non-empty selector was recorded as `selection_method`.
3. The selector resolved to a frozen list of change IDs.
4. Only resolved change IDs were implemented.
5. Every changed file maps to a resolved change or required supporting test/build work.
6. Every planned acceptance criterion has a result.
7. Every validation command records `passed`, `failed`, `blocked`, or `not_run`.
8. Every deviation from the plan is documented.
9. No inventory, reassessment, priority recalculation, infrastructure, or PCF scope was added.
10. No commit, push, or pull request was created unless explicitly authorized.
11. The Step 5 handoff contract is present.

Report:

- Authoritative implementation artifact path
- Selection method
- Requested priorities, waves, or IDs
- Resolved change IDs and count
- Status by change
- Files changed
- Test and build results
- Plan deviations
- Blockers
- Scope violations, if any

### Kafka scenario constraint

Preserve the approved Kafka scenario and processing ownership from Step 3A. Do not introduce a database into database-independent Kafka, change multi-active/single-active ownership, or alter cluster topology without an approved architecture change.
