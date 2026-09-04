# Prompt 2: Generate Findings from the HVE Research Inventory 9-1

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

# Prompt 2 Scenario-Aware Kafka Evaluation Update
When the Step 1 inventory loads `springboot-confluent-kafka.md`:

1. Read the selected `operating_scenario` and `scenario_rule_id`.
2. Evaluate common controls KAFKA-001 through KAFKA-012.
3. For `independent_regional_active_active`, evaluate KAFKA-AA-001 through KAFKA-AA-006 and mark all KAFKA-AS controls `not_applicable`.
4. For `active_standby`, evaluate KAFKA-AS-001 through KAFKA-AS-009 and mark all KAFKA-AA controls `not_applicable`.
5. For `unresolved`, evaluate evidence-backed common controls and mark scenario-dependent controls `not_assessed`; emit an evidence-required item, not an architecture finding.
6. Record scenario context on every Kafka finding:

```yaml
dependency_context:
  dependency: confluent-kafka
  operating_scenario: active_standby
  scenario_rule_id: KAFKA-SCENARIO-001
  related_state_dependencies:
    - azure-sql
    - cosmos-db
```

Do not independently override the Step 1 scenario. If authoritative evidence conflicts, report a scenario-integrity error and route correction to Step 1.

# Prompt 2 Update: Validate and Apply External-Context Kafka Scenario

## Required behavior

Read the Step 1 scenario record. Do not independently select or override the Kafka scenario.

### Valid declared scenario

When scenario source is approved context and policy/repository validation is `consistent`:

- Evaluate Kafka common controls.
- Evaluate only the declared scenario family.
- Mark the other scenario family `not_applicable`.
- Record context provenance and policy rule on each Kafka finding.

### Provisional inferred scenario

When scenario source is `policy_inference` and validation is `inferred`:

- Evaluate common and inferred scenario controls.
- Mark findings as based on an inferred scenario.
- Add `architecture_confirmation_required: true`.
- Do not represent the inference as approved architecture.

### Conflict or insufficient evidence

When validation is `conflict` or scenario is `unresolved`:

- Evaluate evidence-backed common Kafka controls only.
- Mark KAFKA-AA-* and KAFKA-AS-* controls `not_assessed`.
- Create an architecture-governance follow-up, not a code finding.
- Do not silently choose another scenario.

## Finding context

```yaml
dependency_context:
  dependency: confluent-kafka
  operating_scenario: active_standby
  scenario_source: approved_application_architecture_context
  context_id: <id>
  context_version: <version>
  scenario_policy_id: KAFKA-OPERATING-SCENARIO
  scenario_policy_version: "2.0.0"
  scenario_rule_id: KAFKA-SCENARIO-001
  scenario_validation_status: consistent
  architecture_confirmation_required: false
  related_state_dependencies: []
```

## Evidence boundary

Use repository evidence for code findings. Supplied context may establish applicability,
operating scenario, processing chains, and impact, but must not be copied into the
repository-evidence block or used to allege an infrastructure defect.


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

Write one consolidated review artifact to the agent-authorized HVE review location, normally under `.copilot-tracking/reviews/` or the location selected by the installed HVE review workflow, and report its exact path.

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
  inventory_artifact: ".copilot-tracking/research/YYYY-MM-DD/task-research.md"
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

## Completion validation

Verify that the inventory run ID is carried into the outputs, no new dependencies were added, only listed standards were loaded, every finding maps to a noncompliant control, missing evidence became `not_assessed`, no infrastructure or PCF findings were created, and `re_inventory_performed` remains false. Report output paths, standards loaded, findings by severity, not-assessed count, inventory exceptions, and confirmation that no re-inventory occurred.
