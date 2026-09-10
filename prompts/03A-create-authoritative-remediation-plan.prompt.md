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

### Highest-confidence illustrative implementation principle

Generate the highest-confidence concrete illustrative implementation
supported by the authoritative repository evidence.

Do not suppress all illustrative code merely because one implementation
choice, architecture decision, vendor-specific adapter, or external
contract remains unresolved.

For every remediation change:

1. Divide the remediation into independently expressible targets.
2. Generate concrete illustrative code or configuration for every target
   supported by the authoritative evidence.
3. Mark only the target that depends on an unresolved decision as
   `targeted_discovery_required`.
4. Preserve unresolved decisions as explicit inputs for Task Implementor.
5. Do not make an unapproved architecture, persistence, topology,
   security, or product decision.

When supported by evidence, generate concrete proposals for:

- Interfaces and repository contracts
- Domain models and state transitions
- Method signatures and focused method bodies
- Configuration-property classes and configuration structures
- Client lifecycle and listener configuration
- Stable identity propagation
- Error and completion contracts
- Test cases and test configuration
- Technology-neutral application boundaries

Use `targeted_discovery_required` only for the portion that cannot be
responsibly illustrated, including:

- Unselected persistence technology
- Unselected ownership or fencing mechanism
- Unknown vendor-specific API
- Unverified library-version capability
- Unresolved external provider contract
- Required architecture, security, or product-owner decision

An unresolved adapter or technology selection must not prevent the
planner from generating a technology-neutral interface, service
contract, configuration contract, domain change, or test that is
supported by repository evidence.

The Task Planner defines the intended implementation and provides the
highest-confidence illustrative code possible. Task Implementor validates
the current repository state and creates the final repository-specific
implementation.

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


### Enforced illustrative-code generation contract

For every planned change, determine whether the authoritative Step 2 evidence is sufficient to generate a concrete illustrative source or configuration change.

#### Code-required condition

A concrete illustrative code or configuration proposal is required when all of the following are present:

- At least one repository-relative target path
- A target symbol, method, class, property, configuration key, build element, or test location
- An exact original source excerpt from Step 2
- Sufficient repository evidence to identify the programming language or configuration format
- Sufficient repository evidence to express the intended remediation without inventing an external architecture decision, an unverified library API, or an approved numeric value

When this condition is satisfied, narrative-only text is not a valid illustrative proposal. The planner must emit one or more fenced code or configuration blocks showing the proposed change.

#### Required proposed-implementation structure

Use this structure for every affected target:

```yaml
proposed_implementation:
  illustrative_code_status: generated|targeted_discovery_required|not_applicable
  source_language: java|yaml|properties|xml|sql|shell|text|other
  target_repository_path: "relative/path"
  target_symbol: "class, method, property, key, build element, or test"
  replaces_or_updates_evidence_ids:
    - EV-F-001-01
  illustrative_code: |
    // concrete illustrative replacement or updated configuration
  narrative_explanation: >
    Concise explanation of how the proposed code changes the behavior.
  discovery_required_reason: null
  unresolved_inputs: []
```

Rules:

- `illustrative_code_status: generated` requires non-empty `illustrative_code` containing code or configuration syntax appropriate to `source_language`.
- A sentence that describes an action is not code and must not be placed in `illustrative_code`.
- `narrative_explanation` supplements code; it must not replace code when the code-required condition is satisfied.
- `targeted_discovery_required` is permitted only when a specific unresolved repository or API fact prevents a responsible example.
- `not_applicable` is permitted only when the remediation is documentation-only or has no source, configuration, build, or test target.
- Preserve one proposal per target when a change affects multiple files or symbols.
- Do not invent package names, APIs, property names, schemas, storage technologies, topology, or approved numeric settings.
- Reuse repository-observed names and patterns wherever evidence supports them.
- Hard numbers remain externally configurable unless the authoritative plan identifies an approved value.

#### Minimum completeness by target type

For a Java target, the illustrative block must include the affected annotation, method, class member, bean, or focused method body needed to demonstrate the behavioral change. A comment-only block is invalid.

For YAML or properties, the illustrative block must include valid key/value structure showing the changed property contract. A prose instruction such as `Bind the regional properties` is invalid.

For Maven or Gradle, the illustrative block must include the relevant dependency, plugin, configuration, or task syntax.

For tests, the illustrative block must include a concrete test method or focused test configuration when the repository's test model is known.

For a multi-file remediation such as an outbox, ownership protocol, or durable deduplication boundary:

- Generate concrete code for every target that can be responsibly expressed from existing evidence.
- Mark only the blocked targets `targeted_discovery_required`.
- Do not mark the entire change discovery-required if at least one target can receive a useful concrete proposal.

#### Targeted-discovery exception

Use:

```yaml
proposed_implementation:
  illustrative_code_status: targeted_discovery_required
  source_language: java
  target_repository_path: "relative/path"
  target_symbol: "symbol"
  replaces_or_updates_evidence_ids:
    - EV-F-001-01
  illustrative_code: null
  narrative_explanation: >
    The intended behavioral change.
  discovery_required_reason: >
    The exact missing repository or API fact that prevents a responsible code example.
  unresolved_inputs:
    - "Specific missing fact"
```

Valid reasons include:

- The repository does not identify the approved durable store or ownership mechanism.
- The effective library/version API cannot be established from the supplied artifacts.
- The target symbol is generated or owned outside the repository.
- An architecture, security, or product decision is required before selecting an implementation pattern.

Invalid reasons include:

- The change is complex.
- The planner prefers not to generate code.
- Validation is still required.
- The proposal is illustrative.
- Task Implementor will determine it later.

Targeted discovery does not transfer responsibility for report generation to Task Implementor. It only records why concrete illustrative code could not be responsibly produced for that target.

#### Partial proposal requirement

Do not mark an entire change or finding
`targeted_discovery_required` merely because one target or implementation
decision remains unresolved.

For every remediation change:

1. Separate the remediation into independently expressible targets.
2. Generate concrete illustrative code for every target supported by
   authoritative repository evidence.
3. Mark only the blocked target or adapter
   `targeted_discovery_required`.
4. Identify the exact decision preventing code generation for that target.
5. Keep generated and blocked targets within the same root-cause change
   when they collectively implement one remediation.
6. Do not combine unrelated findings or downstream contracts merely to
   avoid generating code.

A change may contain multiple proposed implementation records:

```yaml
proposed_implementations:
  - illustrative_code_status: generated
    target_repository_path: src/main/java/example/NotificationRepository.java
    target_symbol: NotificationRepository
    source_language: java
    illustrative_code: |
      // Concrete repository abstraction

  - illustrative_code_status: targeted_discovery_required
    target_repository_path: not_yet_selected
    target_symbol: DurableNotificationRepositoryAdapter
    source_language: java
    illustrative_code: null
    discovery_required_reason: >
      The approved persistence technology has not been selected.
    unresolved_inputs:
      - Approved durable store

#### Examples of invalid and valid output

Invalid:

```yaml
illustrative_code_status: generated
illustrative_code: |
  Bind APP_DEPLOYMENT_REGION and dependency endpoints from deployment inputs.
```

Valid YAML proposal:

```yaml
illustrative_code_status: generated
source_language: yaml
illustrative_code: |
  data:
    APP_DEPLOYMENT_REGION: ${APP_DEPLOYMENT_REGION}
    KAFKA_BOOTSTRAP_SERVERS: ${KAFKA_BOOTSTRAP_SERVERS}
```

Invalid:

```yaml
illustrative_code_status: generated
illustrative_code: |
  Persist a stable event identity and deduplicate side effects.
```

Valid Java proposal when repository evidence supports the types and names:

```yaml
illustrative_code_status: generated
source_language: java
illustrative_code: |
  @KafkaListener(
      topics = KafkaTopics.ORDER_SHIPPED,
      groupId = KafkaTopics.GROUP_NOTIFICATION_SERVICE,
      autoStartup = "${app.kafka.consumer.enabled:false}")
  public void handleOrderShipped(OrderEvent event, Acknowledgment acknowledgment) {
      notificationService.processOnce(event.eventId(), event);
      acknowledgment.acknowledge();
  }
```

#### Illustrative-code coverage summary

Include this machine-readable summary in the planning artifact:

```yaml
illustrative_code_coverage:
  source_or_configuration_change_count: 0
  targets_requiring_illustrative_code: 0
  targets_with_generated_code: 0
  targets_with_targeted_discovery_required: 0
  targets_not_applicable: 0
  narrative_only_generated_proposals: 0
  coverage_complete: true
```

`coverage_complete` may be true when every required target has either generated code or a valid targeted-discovery exception. It must be false when any required target has only narrative remediation text.

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

## End-of-Phase Compact Handoff Summary

At the end of this phase, create one compact handoff summary under:

```text
.copilot-tracking/plans/handoffs/
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

### Step 3A handoff

Write `.copilot-tracking/plans/handoffs/03A-planning-summary.yml`.

Include all planned change IDs, governed priority distribution, wave indexes, finding-to-change mapping counts, open questions, targeted discovery, and illustrative-code coverage.

```yaml
illustrative_code_summary:
  targets_requiring_illustrative_code: 0
  targets_with_generated_code: 0
  targets_with_targeted_discovery_required: 0
  targets_not_applicable: 0
  narrative_only_generated_proposals: 0
  coverage_complete: true
```

The handoff must preserve the Step 3A frozen priority and wave indexes without recalculation.


## Completion validation

Before completing:

1. Verify every target with a path, symbol, original excerpt, and sufficient implementation evidence has `illustrative_code_status: generated` and a non-empty syntactic code/configuration block.
2. Verify narrative-only text does not appear in `illustrative_code`.
3. Verify every `targeted_discovery_required` target identifies a specific blocking fact and unresolved input.
4. Verify multi-file changes generate concrete proposals for all unblocked targets rather than suppressing the whole change.
5. Verify `illustrative_code_coverage.narrative_only_generated_proposals` is `0`.
6. Verify `illustrative_code_coverage.coverage_complete` is `true`.
7. Verify every planned change maps to an approved noncompliant finding.
8. Verify every approved finding is mapped or explicitly consolidated.
9. Verify no new findings or control statuses were created.
10. Verify no source files were modified.
11. Verify every change cites a valid governance rule and policy version.
12. Verify priority was not derived solely from severity.
13. Verify P2 data-correctness candidates were evaluated for P0 elevation.
14. Verify required tests inherit the priority of the behavior they validate.
15. Verify illustrative code is labeled non-authoritative and grounded in evidence.
16. Verify configuration examples contain no hardcoded region names or endpoints.
17. Verify every change has tests, acceptance criteria, and validation commands.
18. Verify no infrastructure or PCF remediation was added.
19. Verify priority and wave indexes contain every change exactly once in each applicable index.
20. Verify both Step 3B and Step 4 handoff contracts are present.
21. Verify that one compact handoff summary exists under `.copilot-tracking/plans/handoffs/`.
22. Verify targeted discovery is assigned per target, not automatically per change.
23. Verify an unresolved adapter or technology choice does not suppress
  repository interfaces, configuration contracts, service boundaries,
  domain changes, or tests that can be responsibly illustrated.
24. Verify unresolved inputs from related findings do not block code
  generation for the current finding unless they are genuinely required.
25. Verify every narrative-only change was evaluated for partial concrete
  proposals.
26. Verify each targeted-discovery reason references the specific target
  that cannot be generated.
27. Verify each remediation was divided into independently expressible
  implementation targets.
28. Verify concrete illustrative code was generated for every target
  supported by authoritative repository evidence.
29. Verify targeted discovery applies only to the specific blocked target,
  not automatically to the entire change.
30. Verify unresolved adapter, persistence, or vendor decisions did not
  suppress technology-neutral interfaces, service contracts,
  configuration contracts, domain changes, or tests.
31. Verify every targeted-discovery record identifies the exact unresolved
  decision and the information Task Implementor must validate.
32. Verify concrete illustrative code was generated for every target
  supported by authoritative repository evidence.
33. Verify targeted discovery applies only to the specific blocked target,
  not automatically to the entire change.
34. Verify unresolved adapter, persistence, or vendor decisions did not
  suppress technology-neutral interfaces, service contracts,
  configuration contracts, domain changes, or tests.
35. Verify every targeted-discovery record identifies the exact unresolved
  decision and the information Task Implementor must validate.

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

## Repository-Agnostic Snapshot Preservation

Preserve Step 2 `assessment_snapshot` and `source_fingerprint` verbatim. Do not require or invent a Git commit SHA. Do not convert a workspace snapshot, uploaded archive, or source drop into a Git revision.

Targeting precedence is path, symbol/element, original excerpt, fingerprint, assessment snapshot, then advisory line range.

```yaml
target:
  repository_path: src/main/java/example/Service.java
  symbol: Service.processPayment
  assessment_snapshot:
    type: workspace_snapshot
    identifier: assessment-run-2026-09-09T190000Z
    provenance: workspace_generated
    git_commit_sha: not_applicable
    limitations: []
  source_fingerprint:
    algorithm: sha256
    value: <hash>
  original_line_range:
    start_line: 142
    end_line: 156
    status: advisory
  line_numbers_authoritative: false
```

A missing Git repository is not targeted-discovery justification and must not suppress illustrative implementation. Preserve any snapshot limitations for Step 4 drift handling.
