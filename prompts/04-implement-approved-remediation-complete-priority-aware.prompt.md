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
INVENTORY_ARTIFACT=.copilot-tracking/research/{{YYYY-MM-DD}}/{{task_slug}}-research.md
REVIEW_ARTIFACT=.copilot-tracking/reviews/{{YYYY-MM-DD}}/{{task_slug}}-research-review.md
PLAN_ARTIFACT=.copilot-tracking/plans/{{YYYY-MM-DD}}/{{task_slug}}-remediation-plan.md

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

## Optional Atomic Commit Mode

Commit creation is opt-in. Supported modes are:

```yaml
commit_control:
  mode: none|per_change
  push_allowed: false
  branch_creation_allowed: false
  pull_request_creation_allowed: false
  require_clean_starting_worktree: true
  require_validation_before_commit: true
  stop_on_failed_validation: true
```

Generated records must contain one concrete value, not the pipe-delimited template.

When `mode: per_change`:

- Require an existing Git repository and a clean starting worktree.
- Never run `git init`.
- Implement, validate, stage, and commit one complete Step 3A change ID at a time.
- A commit may cover multiple findings mapped to the same root-cause change.
- Do not combine unrelated change IDs in one commit.
- Exclude unrelated existing edits from staging.
- Do not commit when required validation fails.
- Do not create a branch, push, or open a pull request unless separately authorized.
- Preserve dependency order among change IDs.

Use a deterministic commit message:

```text
fix(resiliency): CHANGE-AA-003 persist notification history

Change-ID: CHANGE-AA-003
Finding-IDs: F-003,F-004
Priority: P0
Policy-Rule: P0-AA-005
```

Record:

```yaml
commit_execution:
  mode: per_change
  repository_is_git: true
  starting_worktree_clean: true
  push_allowed: false
  push_performed: false
  pull_request_allowed: false
  pull_request_created: false

change_commits:
  - change_id: CHANGE-AA-003
    finding_ids:
      - F-003
      - F-004
    commit_status: committed
    commit_sha: "<full-sha>"
    commit_subject: "fix(resiliency): CHANGE-AA-003 persist notification history"
    files_committed: []
    validation_status: passed
    validation_commands: []
```

Allowed commit statuses are `committed`, `not_committed`, `validation_failed`, `blocked`, and `skipped_non_git_workspace`.

When `mode: per_change` and the workspace is not a Git repository, do not initialize Git. Record `skipped_non_git_workspace`; continue implementation only when the invocation permits uncommitted changes.

## Source Locator Authority

Resolve each implementation target using this precedence:

1. Repository path
2. Symbol or configuration/build element
3. Exact original source excerpt
4. Source fingerprint
5. Assessment snapshot
6. Original assessed line range, treated as advisory

Do not use line numbers as the primary locator. Do not reject a target solely because lines moved. When source drift exists, follow the repository-agnostic source-drift protocol later in this prompt.

## Assessment-Scope Implementation Boundary

Read and preserve the Step 1 `assessment_scope_resolution` record. It is authoritative for the repository artifact classes that may be changed.

```yaml
implementation_domain_scope:
  enabled_domains: []
  disabled_domains: []
  inventory_only_domains: []
  source: authoritative_step_1_inventory
```

Rules:

- Application code and application configuration may be modified only when enabled.
- Dockerfiles may be modified only when `container_build` is enabled.
- Pipeline files may be modified only when `cicd_pipeline` is enabled.
- Helm, Kustomize, Kubernetes manifests, and deployment scripts may be modified only when `deployment_configuration` is enabled.
- Repository-owned IaC may be modified only when `infrastructure_as_code` is `findings_enabled` and the approved Step 3A change explicitly targets it.
- `inventory_only` permits inspection but not modification.
- Never modify deployed infrastructure.
- A Step 3A proposal cannot expand a disabled Step 1 assessment domain. Stop the affected target and record a scope conflict.

## Approved-Library Implementation Rule

For every change that uses a vendor or framework API, read the Step 3A `library_resolution` record.

Implementation is allowed only when:

- `approval_status: approved`, and
- `repository_availability` is `available` or an explicitly approved dependency change is part of the change, and
- the capability is approved, and
- the library/API is compatible with the effective repository runtime and dependency version.

Do not introduce or substitute Resilience4j, Spring Retry, Failsafe, Hystrix, a custom platform wrapper, or another library without the corresponding approved resolution.

```yaml
library_implementation_check:
  change_id: CHANGE-AA-001
  capability: circuit_breaker
  approved_library: resilience4j
  approval_status: approved
  repository_availability: dependency_change_required
  version_source: dependency_management
  compatibility_validated: true
  implementation_allowed: true
  unresolved_inputs: []
```

Do not hardcode a dependency version when the approved version source is a parent POM, BOM, or dependency-management section. If exact API compatibility cannot be validated, block only the vendor-specific target and preserve any independently implementable technology-neutral target.

## Business-Logic, Partner-Contract, Security, and Privacy Guardrail

Step 4 may implement approved resiliency mechanisms, but it must not independently change business semantics, partner-contract interpretation, security controls, or privacy behavior.

Before modifying each target, read its Step 3A `change_boundary` record. Implementation is permitted only when:

```yaml
change_boundary:
  implementation_allowed: true
  existing_business_behavior_preserved: true
  security_and_privacy_behavior_preserved: true
  approval_required: false
  approval:
    status: not_required
```

If `approval_required: true`, implementation is permitted only when `approval.status: approved` and the approval record identifies the governing decision.

### Prohibited unapproved changes

Do not make an unapproved change that:

- Reinterprets an HTTP status code
- Changes success, failure, duplicate, pending, or unknown classification
- Adds a new partner status-lookup, reconciliation, or mutation request
- Changes primary or fallback-provider selection
- Changes fallback conditions
- Changes retry, discard, compensation, or recovery behavior for a business operation
- Changes externally observable business state transitions
- Changes customer-visible behavior
- Removes or weakens PII scrubbing or logging redaction
- Changes authentication, authorization, encryption, tokenization, masking, input validation, or audit behavior

### Required behavior-preservation record

```yaml
behavior_preservation_check:
  change_id: CHANGE-AA-001
  existing_behavior:
    http_status_mapping: "<summary-or-not_applicable>"
    duplicate_classification: "<summary-or-not_applicable>"
    fallback_conditions: "<summary-or-not_applicable>"
    external_calls: []
    security_and_privacy_controls: []
  planned_implementation:
    http_status_mapping_changed: false
    duplicate_classification_changed: false
    fallback_conditions_changed: false
    external_calls_added: []
    security_or_privacy_controls_changed: false
  approval_required: false
  approval_status: not_required
  implementation_allowed: true
```

If Step 3A does not contain enough information to complete this check, stop the affected target, mark it blocked, and route it to Step 3A planning revision. Do not infer business intent or blindly implement illustrative code.

When adding timeouts, retries, circuit breakers, bulkheads, health checks, or reconciliation scaffolding, wrap and preserve the existing business contract unless an approved decision explicitly changes it.

For mixed remediations, implement only independently complete and eligible resiliency targets. Do not leave the repository in a partial, uncompilable, behaviorally inconsistent, or security-weakened state.

## Implementation Requirements

For every resolved change ID:

1. Confirm mapped findings, controls, governed priority, and policy rule.
2. Confirm affected files, symbols, tests, acceptance criteria, change boundary, library resolution, and enabled assessment domains.
3. Record a concise pre-change evidence snapshot and behavior-preservation check.
4. Modify only the minimum necessary production code and repository configuration.
5. Add or update the approved automated tests.
6. Preserve readiness versus liveness semantics.
7. Use deployment-injected regional endpoints without hardcoded region names.
8. Apply bounded timeout, retry, circuit-breaker, bulkhead, and recovery behavior only when approved and required.
9. Protect non-idempotent operations from unsafe retry.
10. Preserve secure identity, secrets, PII scrubbing, redaction, and authorization behavior.
11. Preserve or improve recovery after dependency restoration without requiring a restart when required.
12. Apply every supporting configuration change required by the implementation.
13. Verify no disabled contributor, orphaned property, contradictory setting, or incomplete dependency change is introduced.
14. Run focused validation first, followed by approved broader validation.
15. Record changed files, validation results, deviations, unresolved issues, blockers, scope checks, and commit outcome.

## Readiness and Liveness Implementation Rule

Unless the grounded control or approved plan explicitly states otherwise:

- Sustained loss of a critical local dependency should make the application not ready when it cannot safely provide its critical capability.
- External dependency failure should not normally make application liveness fail.
- Optional dependency failure should permit readiness when a safe degraded mode exists.
- Readiness should recover after dependency restoration without a process or pod restart.
- Health evaluation must be bounded and must not overload dependencies.

## Validation Sequence

Use validation commands from the approved plan when available. Otherwise, use repository-native commands supported by the inventoried build and artifact files.

Run when applicable:

1. Formatting or static checks that do not introduce unrelated changes
2. Unit tests for changed components
3. Integration, fault, recovery, and security-regression tests mapped to acceptance criteria
4. Module build
5. Repository build
6. Container build validation when `container_build` is enabled and changed
7. Pipeline syntax or local validation when `cicd_pipeline` is enabled and changed
8. Helm, Kustomize, Kubernetes, or deployment configuration rendering/validation when `deployment_configuration` is enabled and changed
9. IaC formatting and validation only when repository-owned IaC modification was explicitly authorized

Do not claim a command passed if it was not run. Record `passed`, `failed`, `blocked`, or `not_run`, and distinguish environmental limitations from code failures.

## Configuration Dependency Validation

When a remediation modifies readiness, liveness, startup probes, health groups, readiness membership, dependency health checks, Actuator contributors, timeout/retry/circuit-breaker settings, or dependency management, validate every prerequisite property and effective setting.

If readiness includes `mongo`, verify that the effective configuration enables the Mongo health contributor, for example:

```yaml
management:
  health:
    mongo:
      enabled: true
```

The exact property must match the repository's Spring Boot version and configuration model.

Record:

```yaml
configuration_consistency_validation:
  change_id: CHANGE-AA-001
  readiness_configuration_verified: true
  liveness_configuration_verified: true
  startup_configuration_verified: true
  health_contributors_verified: true
  resiliency_properties_verified: true
  dependency_management_verified: true
  contradictory_configuration: []
  missing_required_configuration: []
  validation_status: passed
```

Do not mark a remediation implemented when code and configuration disagree, a referenced health contributor is disabled, or required supporting configuration is missing.

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
  commit_mode: none
  commit_created: false
  commit_sha: not_applicable
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
12. Verify every implemented target was marked implementation-allowed by Step 3A.
13. Verify no HTTP status code was reinterpreted without approval.
14. Verify no new external provider call was introduced without approval.
15. Verify duplicate and fallback semantics were preserved unless an approved decision explicitly changed them.
16. Verify PII scrubbing, redaction, authorization, and security behavior were preserved.
17. Verify every blocked business, partner-contract, security, or privacy decision was routed back to Step 3A or the appropriate approval owner.


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

## Repository-Agnostic Source Drift Resolution

Do not require a Git repository or commit SHA before implementation. Resolve source using path, symbol, original excerpt, and fingerprint. Use `assessment_snapshot` only to describe provenance and expected baseline.

```yaml
source_resolution:
  evidence_id: EV-F-001-01
  assessment_snapshot:
    type: workspace_snapshot
    identifier: <identifier-or-not_available>
    provenance: workspace_generated
  repository_path: src/main/java/example/Service.java
  approved_symbol: Service.processPayment
  assessed_fingerprint: <sha256-or-not_available>
  current_fingerprint: <sha256-or-not_available>
  current_excerpt_match: exact|equivalent|changed|not_found
  source_drift_status: none|line_drift_only|content_drift|symbol_moved|target_not_found|baseline_provenance_limited
  original_line_range: 142-156
  current_line_range: 165-179|not_available
  line_numbers_authoritative: false
  implementation_allowed: true|false
```

Rules:

- Never run `git init`, create a commit, or require Git metadata for drift validation.
- When both assessed and current source fingerprints are available, compare them.
- When fingerprint is unavailable, compare path, symbol, exact excerpt, and behavior and record `baseline_provenance_limited` where appropriate.
- Non-Git snapshot types do not block implementation.
- `unknown` snapshot type requires an explicit limitation, but implementation may continue when the approved target is otherwise unambiguous.
- Line drift alone never blocks implementation.
