# Prompt 2: Generate Findings from the HVE Research Inventory

## Agent

Run this prompt in a new VS Code Copilot Chat session with HVE `task-reviewer` selected.

## Authoritative inventory input

The authoritative inventory is the HVE Task Researcher artifact under `.copilot-tracking/research/`, not a file under `assessment/working/`.

Set the input path explicitly when invoking this prompt:

`INVENTORY_ARTIFACT=.copilot-tracking/research/YYYY-MM-DD/springboot-active-active-inventory-research.md`

Read that artifact first. Verify that its `Evaluation Handoff Contract` identifies it as `authoritative_inventory`, specifies `next_phase: evaluation`, and sets `re_inventory_allowed: false`.

If the exact path is not supplied, locate only the single research artifact whose Inventory Metadata and title identify it as the Spring Boot active-active inventory. If more than one candidate exists, stop and request the exact path. Do not select the newest file by assumption.

## Required grounding

Always read:

- `grounding/master/springboot-aks-active-active-master.md`
- `grounding/exclusions/pcf-code-assessment-exclusion.md`

Read dependency-specific standards only for identifiers listed under `Dependency Standards to Load` in the authoritative inventory artifact.

## Kafka Scenario Evaluation

Treat the authoritative Step 1 inventory as the source of the selected Kafka operating scenario. Do not independently discover, recalculate, or override the scenario, source, rule ID, validation status, processing model, regional processing model, external-side-effect classification, Kafka-backed-state classification, or architecture-confirmation requirement.

If Step 1 evidence is stale or contradictory, create an `inventory_exception`. Do not repair the inventory through broad repository discovery.

### Common Kafka controls

When Confluent Kafka is listed under Dependency Standards to Load, always evaluate evidence-backed common controls `KAFKA-001` through `KAFKA-012`. Common controls may be evaluated for approved, inferred, conditionally inferred, and unresolved scenarios when repository evidence is sufficient.

### Approved and consistent scenario

When the scenario source is approved application or solution architecture context and validation is `consistent`:

1. Evaluate common Kafka controls.
2. Evaluate only the declared scenario family.
3. Mark other scenario families `not_applicable`.
4. Record context provenance and policy rule on every Kafka finding.
5. Do not validate deployed Kafka infrastructure unless repository-owned evidence is explicitly in scope.

### Inferred active-standby scenario

When the scenario is `active_standby`, status is `inferred`, and rule is `KAFKA-SCENARIO-001`:

- Evaluate KAFKA-001 through KAFKA-012.
- Evaluate KAFKA-AS-001 through KAFKA-AS-009.
- Mark KAFKA-AA-* and KAFKA-DI-* `not_applicable`.
- Preserve `architecture_confirmation_required: true`.
- Label scenario-specific findings as based on policy inference.
- Do not claim active-standby infrastructure is deployed.
- Record SQL failover-group, Kafka promotion, Cluster Linking, mirror topics, and offset replication as external evidence requirements when not supplied.

### Conditionally inferred active-active scenario

When the scenario is `independent_regional_active_active`, status is `conditionally_inferred`, and rule is `KAFKA-SCENARIO-002`:

- Evaluate KAFKA-001 through KAFKA-012.
- Evaluate repository-verifiable KAFKA-AA-001 through KAFKA-AA-006.
- Mark KAFKA-AS-* and KAFKA-DI-* `not_applicable`.
- Preserve `architecture_confirmation_required: true`.
- Preserve every Step 1 conditional assumption.
- Do not suppress all active-active controls merely because deployed Cosmos multi-region writes or Kafka topology cannot be proven from the repository.

Generate a verified code finding when repository evidence independently demonstrates a code defect, including hardcoded endpoints, both clusters in one bootstrap list, unstable identity, non-idempotent consumption, global ordering assumptions, remote-cluster readiness coupling, synchronous dual-cluster publishing, or missing replay safety.

Generate a conditional finding when code behavior is unsafe only if the provisionally selected architecture is confirmed:

```yaml
finding_status: conditional
scenario_condition:
  operating_scenario: independent_regional_active_active
  assumptions:
    - Cosmos DB multi-region writes are enabled.
    - Kafka uses independent regional clusters.
    - The application uses its local regional cluster.
  evidence_required:
    - Approved application architecture context
    - Cosmos DB account multi-region-write confirmation
    - Kafka regional cluster model confirmation
```

Use `not_assessed` when evaluation requires deployed topology and the repository contains no independent application behavior to evaluate. Examples include actual cluster count, Cluster Linking state, Cosmos account settings, topic or offset replication, regional endpoint injection, and deployed routing behavior. Do not convert missing platform facts into code findings.

### Inferred database-independent Kafka scenario

When the scenario is `database_independent_kafka`, status is `inferred`, and rule is `KAFKA-SCENARIO-003`:

- Evaluate KAFKA-001 through KAFKA-012.
- Evaluate KAFKA-DI-* according to processing-model applicability.
- Mark KAFKA-AA-* and KAFKA-AS-* `not_applicable`.
- Preserve `architecture_confirmation_required: true`.
- Do not automatically mark every KAFKA-DI control applicable.
- Do not default regional ownership to multi-active.

Use these applicability groups:

- Producer-only: KAFKA-DI-001, 002, 003 when applicable, 004, 007, 010, 011, and 012.
- Consumer: KAFKA-DI-001, 002, 003, 005, 006 when external side effects exist, 007, 010, 011, and 012.
- Stream transformer or topic bridge: KAFKA-DI-001, 002, 003, 004, 005, 007, 008 when state stores exist, 009 when compacted topics are state, 010, 011, and 012.
- External-side-effect processor: KAFKA-DI-001, 002, 003, 005, 006, 007, 010, 011, and 012.
- Stateful stream processor: KAFKA-DI-001, 002, 003, 005, 007, 008, 009 when applicable, 010, 011, and 012.

Mark controls that truly do not apply as `not_applicable`. If regional ownership remains unresolved, evaluate controls independent of ownership and mark ownership-dependent portions `not_assessed` with architecture confirmation required.

### Unresolved or conflicted scenario

When the scenario is `unresolved` or status is `conflict` or `insufficient_evidence`:

- Evaluate evidence-backed common Kafka controls only.
- Mark KAFKA-AA-*, KAFKA-AS-*, and KAFKA-DI-* `not_assessed`.
- Create an architecture-governance or evidence-required follow-up.
- Do not create a code finding solely because the scenario is unresolved.
- Do not silently select another scenario.

### Required Kafka finding context

Every Kafka finding must preserve:

```yaml
dependency_context:
  dependency: confluent-kafka
  operating_scenario: active_standby|independent_regional_active_active|database_independent_kafka|unresolved
  scenario_source: approved_application_architecture_context|approved_solution_architecture_context|policy_inference|unresolved
  context_id: <id-or-not_applicable>
  context_version: <version-or-not_applicable>
  scenario_policy_id: KAFKA-OPERATING-SCENARIO
  scenario_policy_version: "3.1.0"
  scenario_rule_id: KAFKA-SCENARIO-001|KAFKA-SCENARIO-002|KAFKA-SCENARIO-003|KAFKA-SCENARIO-004
  scenario_validation_status: consistent|inferred|conditionally_inferred|conflict|insufficient_evidence
  architecture_confirmation_required: true|false
  processing_model: <value-or-not_applicable>
  regional_processing_model: multi_active|single_active|unresolved|not_applicable
  external_side_effects: <value-or-not_applicable>
  kafka_backed_state: <value-or-not_applicable>
  conditional_assumptions: []
  related_state_dependencies: []
```

### Evidence-source boundary

Repository source evidence remains authoritative for code findings. Supplied architecture context and policy inference may establish scenario applicability, scenario condition, processing-chain context, impact, and external evidence requirements. They must not be copied into `repository_evidence` or represented as original source-code evidence.

A missing architecture context file is not a finding. A conditionally inferred scenario is not a confirmed infrastructure topology. An absent infrastructure fact must not be converted into a code defect.


# Prompt 2 Update

Do not maintain dependency-to-grounding mappings in this prompt.

Read the authoritative inventory.

Locate:

```yaml
Dependency Standards to Load
```

For each entry:

```yaml
- id: keyvault
  grounding_file: grounding/dependencies/springboot-keyvault.md
```

Load the exact grounding_file specified.

Only load standards listed in the inventory.

Do not add additional dependencies.
Do not perform dependency rediscovery.

## No re-inventory rule

Do not perform workspace-wide discovery, dependency detection, repository mapping, module discovery, or technology inventory. Do not invoke Task Researcher, researcher subagents, or research skills. Do not add dependencies absent from the authoritative inventory.

You may open only files and line ranges already cited by the inventory when needed to validate a specific control. A small surrounding context window is permitted. This is evidence validation, not inventory expansion.

If cited evidence is missing, stale, incorrect, or insufficient, record an `inventory_exception` and assign affected controls `not_assessed`. Do not repair the inventory by searching unrelated files.

## Assessment scope

Assess Java and Spring Boot code, repository application configuration, client behavior, bounded timeouts, retries, circuit breakers, bulkheads, health, readiness, liveness, state, idempotency, concurrency, startup, recovery, graceful shutdown, telemetry, and tests.

Assume the approved two-region infrastructure exists. Do not assess Azure resource deployment, private endpoints, DNS, capacity, zones, geo-replication, GLB configuration, Terraform, Bicep, or PCF modernization.

## Outputs and Task Reviewer write permissions

Create exactly one authoritative review artifact using the HVE research path convention:

`.copilot-tracking/reviews/{{YYYY-MM-DD}}/springboot-active-active-inventory-research-review.md`

If HVE automatically chooses a date or equivalent slug-compliant filename, report the exact generated path in your completion response. That reported path becomes the input to Prompt 3A.

Preserve all four required sections in the consolidated artifact:

1. Control Results
2. Findings
3. Scorecard
4. Assessment Summary

Do not use Task Researcher to copy or relocate files. If repository-owned output files are required after review, use an authorized implementation-capable agent or manually copy the approved review artifact after the assessment phase.

## Evaluation rules

For every applicable control, return one of `compliant`, `non_compliant`, `not_assessed`, `not_applicable`, or `accepted_risk`. Generate findings only for evidence-backed `non_compliant` controls. Missing evidence is `not_assessed`, not a finding. Deduplicate findings by root cause.

A sustained critical dependency failure should normally make the application not ready when it cannot safely serve its critical capability. External dependency failure should not normally fail liveness. Recovery should restore readiness without a process restart.

## Required execution metadata

Include:

```yaml
assessment_execution:
  inventory_artifact: ".copilot-tracking/research/YYYY-MM-DD/springboot-active-active-inventory-research.md"
  inventory_agent: task-researcher
  evaluator_agent: task-reviewer
  re_inventory_performed: false
  researcher_invoked_during_evaluation: false
  targeted_evidence_validation_performed: false
  source_code_modified: false
  standards_loaded: []
```

## New Mandatory repository_evidence structure
```yaml
repository_evidence:
  - evidence_id: EV-F-001-01
    repository_path: src/main/java/example/Service.java
    symbol: processPayment
    start_line: 142
    end_line: 156
    source_language: java
    evidence_purpose: primary
    original_source_excerpt: |
      // exact source excerpt
```

## Required Rules
- Capture exact repository-relative path.
- Capture symbol, start_line, end_line.
- Preserve exact original source excerpt.
- Do not rewrite, normalize, or regenerate source.
- Redact only sensitive values.
- Use not_available when exact line numbers cannot be proven.
- Original source evidence becomes authoritative input for Step 3A and Step 3B.


## End-of-Phase Compact Handoff Summary

At the end of this phase, create one compact handoff summary under:

```text
.copilot-tracking/reviews/handoffs/
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

### Step 2 handoff

Write `.copilot-tracking/reviews/handoffs/02-assessment-summary.yml`.

Include standards actually loaded, control counts by status, findings by status and severity, exact finding IDs, source-evidence coverage, Kafka scenario provenance, inventory exceptions, and architecture/evidence follow-ups. Do not estimate remediation priority in Step 2 because priority is governed by Step 3A.

```yaml
finding_summary:
  verified_findings: 0
  conditional_findings: 0
  finding_ids: []
  by_severity:
    critical: 0
    high: 0
    medium: 0
    low: 0

evidence_summary:
  applicable_findings: 0
  findings_with_exact_excerpts: 0
  findings_with_evidence_not_available: 0
  findings_with_not_applicable_excerpts: 0
  invented_excerpts: 0
```


## Completion validation

Verify that the inventory run ID is carried into the outputs, no new dependencies were added, only listed standards were loaded, every finding maps to a noncompliant control, missing evidence became `not_assessed`, no infrastructure or PCF findings were created, and `re_inventory_performed` remains false. Report output paths, standards loaded, findings by severity, not-assessed count, inventory exceptions, and confirmation that no re-inventory occurred.
