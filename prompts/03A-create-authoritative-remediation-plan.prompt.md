# Prompt 3A: Create the Authoritative Multi-Region Remediation Plan

## Agent and phase

Run this prompt in a new VS Code Copilot Chat session with HVE `task-planner` selected, or use the HVE planning phase available in your installation.

Step 3A creates the **machine-consumable and implementation-ready remediation plan** used by Step 4. It does not create the customer-facing assessment report. That report is created separately by Step 3B.

This is a planning phase. Do not modify application source code, repository configuration, tests, pipelines, or infrastructure.

## Required inputs

Provide exact paths when invoking this prompt:

```text
INVENTORY_ARTIFACT=<exact authoritative Step 1 inventory artifact path>
REVIEW_ARTIFACT=<exact authoritative Step 2 review artifact path>
PLAN_ARTIFACT=<exact authoritative Step 3A output artifact path>
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

### Business-Logic and Security Preservation Boundary

Resiliency remediation must preserve existing business semantics,
partner-contract interpretation, privacy controls, and security behavior
unless an explicit approved architecture or business decision authorizes
a change.

#### Business-logic changes requiring explicit approval

Do not propose a change as directly implementable when it would alter:

- The meaning assigned to an HTTP status code
- Success, failure, duplicate, pending, or unknown classification
- Primary or fallback provider selection
- The conditions under which fallback is attempted
- Order, payment, delivery, inventory, or enrollment state transitions
- Whether a business operation is retried, discarded, compensated, or
  routed for reconciliation
- The number or type of externally observable partner operations
- Customer-visible results
- Business validation rules
- Authorization behavior
- Personal-information redaction or scrubbing
- Logging sanitization
- Encryption, tokenization, masking, or security controls

These changes require an explicit approval record from the appropriate
architecture, product, business, security, privacy, or partner-contract
owner.

#### Required change classification

Classify every proposed implementation target:

```yaml
change_boundary:
  classification:
    resiliency_mechanism |
    supporting_configuration |
    test_only |
    business_logic_change |
    partner_contract_change |
    security_or_privacy_change |
    mixed

  existing_business_behavior_preserved: true|false|unknown

  security_and_privacy_behavior_preserved: true|false|unknown

  external_interaction_pattern_changed: true|false

  approval_required: true|false

  approval:
    status: approved|not_approved|not_required|not_available
    decision_id: <ADR-or-approval-id-or-not_applicable>
    approved_by: <owner-or-not_applicable>
    approved_at: <date-or-not_applicable>

  implementation_allowed: true|false
  unresolved_inputs: []

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

Write exactly one consolidated authoritative planning artifact to
PLAN_ARTIFACT.

PLAN_ARTIFACT is the binding authoritative output path supplied by
the execution wrapper.

Do not rename the artifact, remove filename suffixes, or substitute
an HVE-selected default path.

If PLAN_ARTIFACT cannot be written, stop and report the exact blocked
path. Do not create an alternate authoritative planning artifact.

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
  inventory_artifact: "${INVENTORY_ARTIFACT}"
  review_artifact: "${REVIEW_ARTIFACT}"
  plan_artifact: "${PLAN_ARTIFACT}"
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

Before completing Step 3A, run the following consolidated validation gate.

### Core planning validation

- Verify every planned change maps to at least one approved noncompliant Step 2 finding.
- Verify every approved finding is mapped to exactly one primary change or explicitly consolidated under another root-cause change.
- Verify no new findings, dependencies, or control statuses were created.
- Verify no repository source, configuration, test, pipeline, deployment, or infrastructure file was modified.
- Verify every change has a unique stable change ID, implementation wave, complexity, objective, acceptance criteria, validation commands, risks, rollback considerations, and dependency mapping.
- Verify priority was assigned only through the governed remediation-prioritization policy.
- Verify every change cites a valid policy ID, policy version, and rule ID.
- Verify priority was not derived solely from severity.
- Verify P2 data-correctness candidates were evaluated for P0 elevation where active-active operation could make a critical transaction materially unsafe.
- Verify required tests inherit the priority of the behavior they validate.
- Verify priority and wave indexes contain every change exactly once in each applicable index.
- Verify no deployed-infrastructure or PCF remediation was added.

### Source evidence and targeting validation

- Verify Step 2 repository paths, symbols or configuration elements, exact excerpts, source fingerprints, assessment snapshots, evidence IDs, and advisory line ranges were preserved verbatim.
- Verify original source was never regenerated or normalized.
- Verify original source, target location, and illustrative implementation remain separate.
- Verify source targeting uses path, symbol or element, exact excerpt, fingerprint, assessment snapshot, and advisory line range in that order.
- Verify line numbers are explicitly non-authoritative for every source or configuration target.
- Verify missing Git metadata did not suppress planning or illustrative proposals.
- Verify evidence limitations are explicit where snapshot identity, fingerprint, excerpt, or line range is unavailable.

### Illustrative-code validation

- Verify every source, configuration, build, or test target has exactly one status: `generated`, `targeted_discovery_required`, or `not_applicable`.
- Verify every target with sufficient authoritative evidence has `illustrative_code_status: generated` and a non-empty syntactic code or configuration block.
- Verify narrative-only text does not appear in `illustrative_code`.
- Verify comments alone do not satisfy Java, YAML, properties, XML, SQL, shell, build, or test proposal requirements.
- Verify each remediation was divided into independently expressible targets.
- Verify multi-file changes contain concrete proposals for every unblocked target.
- Verify targeted discovery applies only to the specific blocked target, not automatically to the entire change.
- Verify every targeted-discovery record identifies the exact blocking fact and required unresolved input.
- Verify unresolved adapter, persistence, vendor, or external-contract decisions did not suppress technology-neutral interfaces, service contracts, configuration contracts, domain changes, or tests.
- Verify unrelated findings or downstream contracts were not combined merely to avoid generating code.
- Verify configuration examples contain no hardcoded region names, regional endpoints, credentials, or unapproved numeric settings.
- Verify all illustrative proposals are labeled non-authoritative.
- Verify `illustrative_code_coverage.narrative_only_generated_proposals` is `0`.
- Verify `illustrative_code_coverage.coverage_complete` is `true`.

### Business-logic, partner-contract, security, and privacy validation

- Verify every implementation target has a `change_boundary` classification.
- Verify directly implementable targets preserve existing business semantics and security/privacy behavior.
- Verify HTTP status codes were not reinterpreted without approved partner-contract evidence.
- Verify success, failure, duplicate, pending, and unknown classifications were not changed without explicit approval.
- Verify no new external provider call or external interaction pattern was proposed as directly implementable without explicit approval.
- Verify primary-provider, fallback-provider, retry, discard, compensation, and reconciliation behavior remains unchanged unless an approved decision authorizes the change.
- Verify no PII scrubbing, logging sanitization, redaction, authentication, authorization, encryption, tokenization, masking, or validation behavior was removed, weakened, or bypassed.
- Verify mixed changes isolate eligible resiliency targets from approval-required business, partner-contract, security, and privacy targets.
- Verify approval-required targets have `implementation_allowed: false` until approval is recorded.

### Approved-library validation

- Verify every vendor-specific illustrative proposal contains the compact `library_resolution` record.
- Verify `approved-libraries.yml` was used as approval authority only when `lifecycle_status: approved`.
- Verify the selected capability is listed under `approved_capabilities`.
- Verify product approval and repository availability were evaluated separately.
- Verify dependency presence was not treated as governance approval.
- Verify policy approval was not treated as proof that the dependency or compatible API is present.
- Verify dependency proposals follow the approved version-source strategy.
- Verify no unmanaged version, unsupported API signature, or unapproved library substitution was invented.
- Verify missing library approval blocked only vendor-specific targets and did not suppress technology-neutral contracts or tests.
- Verify Step 3A did not create a new finding solely because the approved-library file was absent, draft, or incomplete.

### Handoff and completion validation

- Verify the Step 3B report handoff and Step 4 Task Implementor handoff contracts are present.
- Verify the planning handoff preserves the frozen priority and wave indexes without recalculation.
- Verify one compact handoff summary exists under `.copilot-tracking/plans/handoffs/` when agent write permissions permit it.
- Verify the handoff summary is non-authoritative and identifies exact authoritative artifact paths.
- Verify all unresolved decisions, governance blocks, targeted-discovery items, and approval-required targets are reported.

Report:

- Authoritative planning artifact path
- Prioritization policy version
- Change counts by priority
- Implementation waves
- Illustrative-code coverage summary
- Items requiring targeted implementation discovery
- Approval-required business, partner-contract, security, or privacy targets
- Approved-library resolution exceptions
- Priority overrides
- Confirmation that no source code or repository configuration was modified

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

## Simplified Approved-Library Resolution

### Optional governance input

Read this optional file when present:

```text
APPROVED_LIBRARIES=grounding/governance/approved-libraries.yml
```

The file is valid as approval authority only when its top-level `lifecycle_status` is `approved`. A missing or draft file does not authorize a vendor-specific library.

The simplified policy identifies:

- The approved resiliency library
- Approved resiliency capabilities
- Observability and testing libraries
- The approved version-source strategy
- Cross-cutting library usage constraints

Do not require artifact coordinates, exact versions, framework matrices, or a Git repository in this governance file. Resolve repository compatibility and dependency availability from the authoritative inventory, findings, cited build evidence, and permitted targeted inspection.

### Resolution precedence

Use this order:

1. Approved application-specific library declaration, when supplied
2. Approved `grounding/governance/approved-libraries.yml`
3. Existing repository dependency or parent/build-management evidence
4. Technology-neutral illustrative implementation
5. Targeted discovery for only the blocked vendor-specific target

Preserve these distinctions:

- Policy approval means the product choice is sanctioned.
- Repository evidence means the library or API is currently available.
- Policy approval does not prove repository availability.
- Repository dependency presence does not prove governance approval.

### Required compact resolution record

For each proposal requiring a vendor or framework API, record:

```yaml
library_resolution:
  capability: circuit_breaker|retry|bulkhead|time_limiter|metrics|tracing|integration_testing|api_mocking|other
  approved_library: resilience4j|spring_retry|failsafe|custom_platform_wrapper|micrometer|open_telemetry|testcontainers|wiremock|other|not_selected
  approval_source: application_architecture_context|approved_libraries_governance|not_available
  approval_status: approved|not_approved|not_available
  repository_availability: available|dependency_change_required|unknown
  version_source: parent_pom|bom|dependency_management|repository_declared|not_specified
  dependency_change_required: true|false|unknown
  unresolved_inputs: []
```

### Approved and repository-available

When the policy is approved, the capability is listed under `approved_capabilities`, and repository evidence establishes a compatible library/API:

- Generate concrete vendor-specific illustrative code and configuration.
- Reuse repository-observed package names, APIs, configuration prefixes, programming model, and test conventions.
- Do not invent API signatures that cannot be validated from the repository's effective library version.

### Approved but dependency change required

When the policy is approved but the library is not currently available:

- Set `repository_availability: dependency_change_required`.
- Set `dependency_change_required: true`.
- Generate a dependency-change proposal only when the artifact identity can be established from authoritative repository or organization evidence.
- Follow `library_rules.version_source`.
- Do not hardcode a version when the approved source is a parent POM, BOM, or dependency-management section.
- Generate vendor-specific code only when compatibility and the API family can be established responsibly.
- Otherwise generate technology-neutral boundaries and mark only the vendor-specific adapter/decorator target `targeted_discovery_required`.

### Repository library present but not approved

When repository evidence contains a resilience library but no approved policy or application decision sanctions it:

- Set `approval_status: not_available` or `not_approved` as applicable.
- Do not treat dependency presence as product approval.
- Generate technology-neutral proposals where possible.
- Identify governance confirmation as an unresolved input for the vendor-specific target.
- Do not create a new finding in Step 3A solely because approval is unavailable.

### No approved library

When no approved library is selected:

- Do not choose Resilience4j, Spring Retry, Failsafe, or another vendor on behalf of the organization.
- Generate technology-neutral interfaces, configuration contracts, fallback behavior, failure classification, metrics expectations, and tests where supported.
- Mark only the vendor-specific dependency, decorator, adapter, or annotation target `targeted_discovery_required`.
- State that product selection is an architecture or platform-governance input, not a repository defect by itself.

### Circuit-breaker proposal behavior

For circuit-breaker remediation, always define the technology-neutral design first:

```yaml
circuit_breaker_design:
  protected_operation: <repository symbol>
  fallback_behavior: fail_fast|cached_read|safe_default|queued_recovery|none|unresolved
  failure_classification: <repository-supported classification>
  state_scope: per_dependency|per_operation|other|unresolved
  timeout_relationship: <bounded ordering contract>
  configuration_externalized: true
  approved_library: <library_resolution.approved_library>
```

Do not invent breaker names, thresholds, sliding-window values, open durations, half-open call counts, fallback values, or exception lists. Use externalized placeholders unless authoritative evidence supplies approved values.

### Simplified example

```yaml
library_resolution:
  capability: circuit_breaker
  approved_library: resilience4j
  approval_source: approved_libraries_governance
  approval_status: approved
  repository_availability: dependency_change_required
  version_source: dependency_management
  dependency_change_required: true
  unresolved_inputs: []
```

If artifact coordinates are established elsewhere, an illustrative dependency proposal may omit an explicit version when dependency management is authoritative:

```xml
<dependency>
  <groupId>io.github.resilience4j</groupId>
  <artifactId>resilience4j-spring-boot3</artifactId>
</dependency>
```

### Approved-library validation

Validate library resolution while building each affected change. The authoritative phase-completion gate is the consolidated `## Completion validation` section later in this prompt.

Before completing library resolution, verify:

- Every vendor-specific proposal includes the compact `library_resolution` record.
- The governance file was used as approval authority only when `lifecycle_status: approved`.
- The selected capability is listed under `approved_capabilities`.
- Repository availability and product approval were evaluated separately.
- Missing library approval blocked only vendor-specific targets.
- Technology-neutral contracts and tests were still generated when evidence supported them.
- No unmanaged version, unsupported API, or unapproved product substitution was invented.
- Step 3A did not create a new finding solely because the approved-library file was absent or draft.
