# Prompt 3A: Create the Authoritative Multi-Region Remediation Plan

## Agent and phase

Run this prompt in a new VS Code Copilot Chat session with HVE `task-planner` selected, or use the HVE planning phase available in your installation.

Step 3A creates the **machine-consumable and implementation-ready remediation plan** used by Step 4. It does not create the customer-facing assessment report. That report is created separately by Step 3B.

This is a planning phase. Do not modify application source code, repository configuration, tests, pipelines, or infrastructure.

## Required inputs

Provide exact paths when invoking this prompt:

```text
INVENTORY_ARTIFACT=.copilot-tracking/research/YYYY-MM-DD/springboot-active-active-inventory-research.md
REVIEW_ARTIFACT=.copilot-tracking/reviews/YYYY-MM-DD/springboot-active-active-inventory-review.md
```

Always read:

1. The authoritative Step 1 application inventory.
2. The authoritative Step 2 control results, findings, scorecard, and assessment summary.
3. `assessment/grounding/governance/remediation-prioritization.md`.
4. The grounded master application standard.
5. Only the dependency standards listed in the authoritative inventory.
6. `assessment/grounding/exclusions/pcf-code-assessment-exclusion.md`.
7. Source files and symbols cited by the inventory or findings, only when needed to create accurate change proposals.

## Purpose

Convert approved noncompliant findings into a governed, implementation-ready remediation plan containing:

- Stable root-cause change IDs
- Finding and control traceability
- Governed P0 to P3 priority assignments
- File- and symbol-level proposed changes
- Illustrative Java, Spring Boot, configuration, and test proposals
- Implementation dependencies and waves
- Acceptance criteria
- Build and validation commands
- Risk, compatibility, rollback, and open-question records
- A deterministic handoff to Step 4

## Phase boundaries

Do not:

- Re-inventory the repository
- Reassess controls
- Create new findings
- Change finding severity or compliance status
- Add remediation scope not tied to an approved finding
- Plan implementation for `not_assessed`, `not_applicable`, `compliant`, or `accepted_risk` controls
- Modify source code
- Apply patches
- Run formatters that change files
- Add infrastructure deployment work
- Add PCF findings, migration work, modernization work, or cleanup work
- Invoke Task Researcher or researcher subagents

You may inspect only files and symbols cited by Step 1 or Step 2. A small surrounding context window is allowed. If implementation context is insufficient, mark the proposal `targeted_implementation_discovery_required: true`. Do not perform broad discovery.

## Root-cause planning rule

Create one change ID per root-cause remediation, not one change ID per control.

When multiple findings require the same underlying change:

- Create one primary change ID.
- Map all affected findings and controls to it.
- Identify the primary finding and related findings.
- Avoid duplicate backlog items and duplicate code proposals.

Use stable IDs:

```text
CHANGE-AA-001
CHANGE-AA-002
CHANGE-AA-003
```

Do not reuse an ID for a different root cause.

## Governed priority assignment

`grounding/governance/remediation-prioritization.md` is the only definition of P0, P1, P2, and P3.

For every root-cause change:

1. Select the highest applicable governance rule.
2. Cite `policy_id`, `policy_version`, and `rule_id`.
3. Provide an evidence-based rationale.
4. Evaluate P2 data-correctness candidates for P0 elevation when active-active operation would make a critical transaction materially unsafe.
5. Keep required validation tests at the same priority as the behavior they prove.
6. Preserve the calculated priority when a human override is applied.
7. Record override priority, reason, approver, and approval date.
8. Do not derive priority directly from finding severity.
9. Do not invent priority definitions or rule IDs.

Use:

```yaml
priority:
  value: P0
  policy_id: AA-REMEDIATION-PRIORITY
  policy_version: "1.0.0"
  rule_id: P0-AA-003
  rationale: >
    Evidence-based explanation of why the governance rule applies.
  calculated_priority: P0
  override_applied: false
  override_priority: null
  override_reason: null
  override_approved_by: null
  override_approved_at: null
```

## New change structure
```yaml
change:
  change_id: CHG-001
  target:
    repository_path: ...
    symbol: ...
    start_line: 142
    end_line: 156
  current_implementation:
    evidence_id: EV-F-001-01
    original_source_excerpt: |
      ...
  proposed_implementation:
    status: illustrative
    illustrative_code: |
      ...
```

## Required Rules
- Preserve Step 2 source evidence verbatim.
- Never regenerate original source.
- Keep original source, target location, and illustrative code separate.
- Use evidence_not_available when Step 2 lacks an excerpt.


## Required change specification

Every change must contain:

```yaml
change_id: CHANGE-AA-001
finding_ids: []
primary_finding_id: null
primary_control_id: APP-AA-001
related_control_ids: []
category: ""
resiliency_related: true
priority:
  value: P0
  policy_id: AA-REMEDIATION-PRIORITY
  policy_version: "1.0.0"
  rule_id: P0-AA-003
  rationale: ""
  calculated_priority: P0
  override_applied: false
  override_priority: null
  override_reason: null
  override_approved_by: null
  override_approved_at: null
implementation_wave: 1
complexity: medium
implementation_status: proposed
implementation_allowed_in_planning_phase: false
objective: ""
existing_behavior:
  description: ""
  evidence: []
proposed_behavior: ""
what_this_solves: ""
operating_scenario_impact: ""
kafka_scenario_context: null
affected_files: []
new_files: []
configuration_changes: []
dependency_changes: []
illustrative_code_blocks: []
proposed_tests: []
acceptance_criteria: []
validation_commands: []
risks: []
compatibility_considerations: []
rollback_considerations: []
depends_on_change_ids: []
open_questions: []
targeted_implementation_discovery_required: false
```

## Illustrative code proposals

For every proposed code or repository-configuration change, provide a concise illustrative example when evidence is sufficient.

Examples may include:

- Java classes and methods
- Spring `@Configuration` and `@ConfigurationProperties`
- `HealthIndicator` or `ReactiveHealthIndicator`
- Spring Retry, Resilience4j, Reactor, or Azure SDK client behavior
- Timeout, backoff, circuit-breaker, and bulkhead configuration
- `application.yml` or `bootstrap.yml`
- Maven or Gradle changes
- JUnit, Mockito, WireMock, Testcontainers, or repository-native tests
- Application-owned Kubernetes probe-path settings when those files are present in the repository

Label every example:

> Illustrative proposal only. 

Do not present illustrative code as an applied patch.

Code examples must:

- Reuse actual package, class, symbol, property, and library names when evidenced
- Match the repository's synchronous or reactive programming model
- Follow existing dependency-injection and testing patterns
- Avoid unrelated refactoring
- Avoid hardcoded region names and regional endpoints
- Distinguish readiness from liveness
- Use bounded timeouts and retries
- Avoid unsafe retry of non-idempotent operations
- Include recovery behavior after dependency restoration
- Include corresponding test proposals

If names or APIs cannot be verified, do not invent compilable code. Describe the intended pattern and set `targeted_implementation_discovery_required: true`.

## Readiness and liveness design rule

Unless a grounded control explicitly states otherwise:

- Sustained loss of a critical local dependency should make the application not ready when it cannot safely provide its critical business capability.
- External dependency loss should not normally make application liveness fail.
- Optional dependencies should not make readiness fail when a safe degraded mode exists.
- Readiness should recover after dependency restoration without requiring a process or pod restart.
- Health evaluation must be bounded and must not create excessive dependency traffic or cost.

## Implementation waves

Create implementation waves based on dependencies, release safety, and governed priority.

The plan must:

- Assign every change to one implementation wave.
- Keep prerequisite changes in an earlier or equal wave.
- Keep tests required to prove a behavior in the same change and priority.
- Identify changes that can execute in parallel.
- Identify changes requiring architecture, security, product-owner, or platform-owner decisions.
- Avoid implying dates or sprint duration unless provided by the user.

## Required outputs

Write one consolidated authoritative planning artifact to the HVE-authorized planning location, normally under `.copilot-tracking/plans/` or the location selected by the installed HVE planning workflow.

The consolidated artifact must contain:

1. Planning Metadata
2. Executive Remediation Strategy
3. Finding-to-Change Mapping
4. Detailed Change Specifications
5. Illustrative Code Proposals
6. Proposed Test Changes
7. Engineering Backlog
8. Implementation Waves
9. Validation Strategy
10. Risks, Assumptions, and Open Questions
11. Step 3B Report Handoff Contract
12. Step 4 Task Implementor Handoff Contract

Report the exact artifact path. Do not fail only because repository-owned output is unavailable.

## Required planning metadata

```yaml
planning:
  schema_version: "2.0"
  phase: remediation_planning
  artifact_role: authoritative_remediation_plan
  inventory_artifact: "exact Step 1 path"
  review_artifact: "exact Step 2 path"
  planner_agent: task-planner
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
```

## Priority and wave summaries

Include machine-readable summaries so Step 4 can select all changes by priority or wave:

```yaml
implementation_scope_index:
  by_priority:
    P0:
      - CHANGE-AA-001
    P1:
      - CHANGE-AA-002
    P2: []
    P3: []
  by_wave:
    "1":
      - CHANGE-AA-001
    "2":
      - CHANGE-AA-002
```

## Finding-to-remediation mapping

Every approved finding must map to exactly one primary change ID or document consolidation under another root-cause change.

```yaml
mapping:
  - finding_id: FINDING-KV-001
    primary_control_id: KV-001
    change_id: CHANGE-AA-001
    priority: P0
    priority_rule_id: P0-AA-003
    implementation_wave: 1
    disposition: planned
```

## Step 3B report handoff contract

End the planning artifact with this report handoff in addition to the Step 4 handoff:

```yaml
report_handoff:
  artifact_role: authoritative_report_input
  next_phase: assessment_report_generation
  next_prompt: 03B-create-code-level-resiliency-assessment-report-schema-governed.prompt.md
  inventory_reuse_required: true
  review_reuse_required: true
  remediation_plan_reuse_required: true
  re_inventory_allowed: false
  reassessment_allowed: false
  new_findings_allowed: false
  report_must_preserve_finding_status: true
  report_must_preserve_priority: true
  illustrative_code_must_be_labeled: true
  infrastructure_findings_allowed: false
  pcf_findings_allowed: false
```

## Step 4 Task Implementor handoff contract

```yaml
handoff:
  artifact_role: authoritative_remediation_plan
  next_phase: implementation
  next_agent: task-implementor
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
```

## Completion validation

Before completing:

1. Verify every planned change maps to an approved noncompliant finding.
2. Verify every approved finding is mapped or explicitly consolidated.
3. Verify no new findings or control statuses were created.
4. Verify no source files were modified.
5. Verify every change cites a valid governance rule and policy version.
6. Verify priority was not derived solely from severity.
7. Verify P2 data-correctness candidates were evaluated for P0 elevation.
8. Verify required tests inherit the priority of the behavior they validate.
9. Verify illustrative code is labeled non-authoritative and grounded in evidence.
10. Verify configuration examples contain no hardcoded region names or endpoints.
11. Verify every change has tests, acceptance criteria, and validation commands.
12. Verify no infrastructure or PCF remediation was added.
13. Verify priority and wave indexes contain every change exactly once in each applicable index.
14. Verify both Step 3B and Step 4 handoff contracts are present.

Report:

- Authoritative planning artifact path
- Prioritization policy version
- Change counts by priority
- Implementation waves
- Items requiring targeted implementation discovery
- Priority overrides
- Confirmation that no source code was modified

### Kafka scenario preservation

For Kafka findings preserve operating_scenario, scenario_source, policy version/rule, processing_model, regional_processing_model, external_side_effects, kafka_backed_state, validation status, and architecture confirmation. Do not redesign scenario during planning. Database-independent remediation must not introduce a database unless an approved architecture decision requires it.
