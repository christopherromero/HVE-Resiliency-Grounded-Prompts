# Prompt 3B: Create the Schema-Governed Code-Level Resiliency Assessment Report

## Agent and phase

Run this prompt in a new VS Code Copilot Chat session with HVE `task-planner` selected.

Step 3B creates the complete human-readable assessment report for architects, application teams, engineering leadership, and customer review. Step 3B is a report-generation phase, not an implementation phase.

Step 3B must directly generate the report. It must not delegate report generation to Task Implementor.

## Report artifact authorization

Creating the Markdown assessment report is an explicitly authorized output of this phase.

The assessment report is a documentation artifact. It is not an implementation artifact, source-code change, remediation change, configuration change, test change, deployment change, or infrastructure change.

The Task Planner is authorized to create or update exactly one assessment-report file at the preferred path defined below.

Creating this Markdown report does not constitute source-code implementation and must not be delegated to Task Implementor.

Do not invoke, recommend, route to, or require Task Implementor to generate the assessment report.

Task Implementor is used only after Step 3B has generated the report and after remediation scope has been approved. Task Implementor implements approved remediation from the authoritative Step 3A plan. It does not own the Step 3B report.

References to Step 4, Task Implementor, approval selectors, and implementation boundaries are report content only. They describe a future execution phase and do not transfer ownership of report generation.

## Required inputs

Provide exact paths:

```text
INVENTORY_ARTIFACT=.copilot-tracking/research/YYYY-MM-DD/springboot-active-active-inventory-research.md
REVIEW_ARTIFACT=<exact Step 2 authoritative review artifact or output path>
PLAN_ARTIFACT=<exact Step 3A authoritative remediation-plan artifact>
APPLICATION_CONTEXT=<optional application-context file path>
REFERENCE_ARCHITECTURE_REGISTRY=<optional approved reference-architecture registry path>
REPORT_SCHEMA=grounding/governance/assessment-report-schema.md
```

`REPORT_SCHEMA` is normally fixed and must not be changed per application unless an approved schema version is intentionally selected.

## Mandatory inputs to read

Always read:

1. The authoritative Step 1 application inventory.
2. The authoritative Step 2 findings, control results, scorecard, and assessment summary.
3. The authoritative Step 3A remediation plan.
4. `grounding/governance/assessment-report-schema.md`.
5. `grounding/governance/remediation-prioritization.md`.
6. The grounded master application behavior standard used by Step 2.
7. Only dependency standards listed by the authoritative inventory and evaluated by Step 2.
8. `grounding/exclusions/pcf-code-assessment-exclusion.md`.
9. Any supplied application context.
10. Any supplied approved reference-architecture registry.

Do not generate the report until the schema file and the three authoritative phase artifacts have been read successfully.

## Schema authority and precedence

Use this precedence when instructions differ:

1. Authoritative Step 1, Step 2, and Step 3A artifact facts and classifications
2. `assessment-report-schema.md` for report structure and required content
3. This prompt for report-generation workflow, artifact authorization, and validation
4. Optional application context and reference registry for approved descriptive metadata

The schema controls:

- Required report sections
- Section order
- Required finding fields
- Summary and matrix structure
- Evidence-boundary sections
- Standards-alignment structure
- Implementation-roadmap structure
- Required notices and exclusions

This prompt controls who generates the report and where it may be written. Step 3B directly generates the report.

Do not omit a schema-required section.

If required report content is unavailable:

- Preserve the required section.
- State `Not provided` or `No evidence available in the supplied authoritative artifacts`.
- Do not invent content.
- Do not convert missing evidence into a finding.
- Do not delegate completion of the section to Task Implementor.

Do not add a new top-level report section unless the schema explicitly permits it. Repository-specific categories beneath a required section are allowed when supported by authoritative findings.

## Schema validation precheck

Before generating the report, verify that the schema contains:

```yaml
schema:
  schema_id: CODE-LEVEL-RESILIENCY-ASSESSMENT-REPORT
  schema_version: "1.7.0"
  lifecycle_status: active
```

Also verify that the schema defines these required sections:

1. Assessment Overview
2. Resiliency-Focused Recommendations
3. Non-Resiliency-Focused Recommendations
4. Repository and IaC Evidence Gap Analysis
5. Full Finding Matrix
6. Standards Alignment
7. Implementation Roadmap

If the schema is missing, unreadable, inactive, or structurally invalid, stop and report the schema validation error. Do not generate a best-effort report from memory, and do not route the error to Task Implementor.

## Purpose

Create one complete, polished Markdown report that:

- Explains the assessed application and repository scope
- Summarizes application architecture and regional resiliency themes
- Presents findings grouped by resiliency relationship and governed priority
- Includes precise repository evidence
- Includes illustrative proposed fixes from Step 3A
- Explains what each recommendation solves
- Explains active-active, active-passive, operational, data, or processing impact as applicable
- Distinguishes verified findings, conditional findings, evidence-required items, verified controls, and non-findings
- Summarizes repository-visible IaC and external platform evidence boundaries without creating infrastructure findings
- Provides a complete finding matrix
- Maps findings to applicable Microsoft or approved enterprise standards
- Summarizes the Step 3A implementation roadmap
- Conforms to the authoritative report schema

## Strict phase boundaries

Do not:

- Re-inventory the repository
- Reassess controls
- Create new findings
- Remove approved findings
- Change finding severity
- Change governed priority
- Recalculate priority
- Convert `not_assessed` into `non_compliant`
- Convert an external evidence gap into a confirmed defect
- Create infrastructure findings
- Create PCF findings, modernization recommendations, migration recommendations, cleanup recommendations, or implementation work
- Modify application source code
- Modify application configuration
- Modify tests
- Modify deployment automation
- Modify infrastructure files
- Present illustrative code as an applied patch
- Invent internal reference-architecture links
- Invent application names, regions, owners, dates, versions, or deployment modes
- Override schema-required content or ordering
- Delegate report generation to Task Implementor
- Produce only a plan for someone else to generate the report

Creating the assessment Markdown file is allowed and required.

Creating the report is not considered:

- Source-code modification
- Remediation implementation
- Repository refactoring
- Configuration implementation
- Test implementation
- Deployment implementation
- Infrastructure implementation

The phase remains read-only with respect to application code, application configuration, tests, deployment files, and infrastructure files. The only authorized write is the assessment report itself.

When a field is unavailable from supplied artifacts, use `Not provided` or omit it only when the schema marks the field optional.

## No-delegation rule

Step 3B must generate the report directly.

It must not produce:

- A plan to generate the report
- Instructions for Task Implementor to generate the report
- A placeholder report
- An empty report shell
- A report-generation backlog item
- A recommendation to run Step 4 before the report exists
- A handoff claiming the report is an implementation artifact

If all required inputs are readable and schema validation passes, report generation must complete during this phase.

## Finding classification

Every report item must retain its authoritative Step 2 and Step 3A classification.

Use these report classifications:

- **Verified finding:** Step 2 status is `non_compliant` and evidence is sufficient.
- **Conditional finding:** Step 2 identifies a failure only if an external fact is confirmed. State the condition and required evidence.
- **Evidence required / not assessed:** Do not present as a confirmed defect. Place it in the evidence-gap section or a clearly labeled evidence-required subsection.
- **Verified control:** Evidence establishes acceptable behavior and no code change is required.
- **Non-finding observation:** Informational only and excluded from counts and implementation scope.

PCF references must be informational only and excluded from findings, priorities, counts, score, recommendations, matrices, and implementation work.

## Required output behavior

### Preferred report path

Attempt to create the complete report at:

```text
.copilot-tracking/plans/reports/code-level-resiliency-assessment.md
```

Do not stop, delegate the report to Task Implementor, or request implementation merely because the preferred output path is unavailable.

The artifact must be the complete schema-conformant assessment report. It must not be a plan, placeholder, instruction set, or backlog item for later report generation.

### Last-resort response behavior

If both file paths are blocked by the active agent environment but report content can still be generated:

1. Generate the complete report in the current response.
2. Clearly state both attempted paths and the write restriction.
3. Do not instruct the user to run Task Implementor.
4. Do not claim that Step 3B completed successfully unless a complete report was produced.

## Report metadata

At the beginning of the report, include the schema identity in an HTML comment:

```html
<!--
report_governance:
  schema_id: CODE-LEVEL-RESILIENCY-ASSESSMENT-REPORT
  schema_version: "1.7.0"
  schema_path: grounding/governance/assessment-report-schema.md
  schema_validation: passed
  generated_by_phase: Step 3B
  artifact_type: assessment_documentation
  implementation_artifact: false
-->
```

## Required report structure

Follow `assessment-report-schema.md` exactly. The required top-level structure is reiterated below for workflow clarity, but the governance schema remains authoritative.

<a id="top"></a>

# Code-Level Resiliency Assessment

Include schema-required report metadata:

- Application
- Assessment date
- Repository scope
- Current deployment
- Target deployment
- Language and framework
- Runtime platform
- Report version

Use `Not provided` for unavailable required metadata.

## Table of Contents

Include schema-required links to:

1. Assessment Overview
2. Resiliency-Focused Recommendations
3. Non-Resiliency-Focused Recommendations
4. Repository and IaC Evidence Gap Analysis
5. Full Finding Matrix
6. Standards Alignment
7. Implementation Roadmap

## 1. Assessment Overview

### Application and repository overview

Write a factual narrative covering the schema-required application characteristics supported by inventory evidence, including build system, versions, modules, workload model, inbound interfaces, schedulers or consumers, data paths, repository-owned configuration, confirmed dependencies, deployment context, and evidence boundary.

### Assessment themes

Provide concise themes. Each theme must explain observed behavior, regional resiliency relevance, related finding IDs, and whether the conclusion is verified or conditional.

### Approved shared-service and reference architectures

If an approved reference registry is supplied, create the schema-defined reference table using only supplied references.

If no registry is supplied, state:

> No customer-specific reference-architecture registry was supplied. The assessment uses the grounded application behavior standards and cited Microsoft patterns.

### Summary findings table

Create the schema-defined summary table and reconcile counts to the Full Finding Matrix.

Count only approved findings. Exclude verified controls, non-findings, `not_assessed`, `not_applicable`, accepted risks, and PCF references.

### Illustrative-code notice

Include the exact notice required by the schema.

Include `[Back to Top](#top)`.

## 2. Resiliency-Focused Recommendations

### P0 Critical Immediate Action

#### Database Resiliency

F-001

#### Messaging Resiliency

F-002

### P1 High Priority

#### Configuration

F-003

### P2 Moderate Priority

F-004

### P3 Optimization

F-005
...

Create only priority subsections containing resiliency-related findings.

Group findings first by governed priority.

Required order:

P0
P1
P2
P3

Within each priority group,
organize findings by repository-specific category.

Render every category using:

```html
<h3 style="color:#0F6CBD;">
{Category Name}
</h3>
```

The category heading is a visual grouping construct and must:

- appear before the first finding in the category
- be larger than the finding heading
- not be treated as a finding
- not receive a finding ID
- not appear in finding counts

Do not create a category-only structure.

Priority is the primary organization mechanism.
Category is secondary. 
Do not force a category unsupported by evidence.


### Required detailed finding content

For each finding, include every schema-required field:

- Finding ID and title
- Priority
- Priority policy, version, and rule
- Severity
- Resiliency relationship
- Finding status
- Issue
- What the recommendation solves
- Active-active or active-passive impact
- Recommended fix
- Repository evidence
- Target file and location
- Original source requiring update
- Illustrative proposed implementation
- Validation requirements
- Dependencies
- Notes
- Standards reference

Rules:

- Preserve line numbers when available.
- Use fenced code blocks with the correct language.
- Label every illustrative code proposal as required by the schema.
- Do not fabricate code when Step 3A requires targeted implementation discovery.
- When Step 3A marks a proposal `generated`, render the concrete code/configuration block exactly; narrative-only remediation is invalid.
- When Step 3A marks targeted discovery required, render the reason and unresolved inputs without presenting prose as code.
- For conditional findings, include the condition and evidence required.
- Distinguish minimum remediation from optional architectural alternatives.
- Cross-reference related findings and change IDs.

Include `[Back to Top](#top)`.

## 3. Non-Resiliency-Focused Recommendations

### P0

...

### P1

...

### P2

...

### P3

...
Include only approved findings explicitly classified as not resiliency-related.

Use the schema-required detailed finding format, replacing regional resiliency impact with operational or quality impact where appropriate.

Do not place PCF references in this section.

### Verified controls

Include evidence-backed controls for which no application code change is required. Do not include verified controls in finding counts.

Include `[Back to Top](#top)`.

## 4. Repository and IaC Evidence Gap Analysis

Respect the application-code-only boundary.

Explain which application configuration, pipeline, Docker, Helm, Kubernetes, workflow, build, or test artifacts were actually present, and which platform artifacts were external or absent.

Absence of infrastructure evidence is not an infrastructure finding.

### Available to review

Create the schema-defined table using only proven repository artifacts.

### Not available or externally owned

Create the schema-defined table for evidence needed to validate application assumptions or conditional findings.

### PCF exclusion statement

Include the exact PCF exclusion statement required by the schema.

Include `[Back to Top](#top)`.

## 5. Full Finding Matrix

Create one row per approved finding using the schema-defined columns.

Requirements:

- Link each finding ID to its detailed heading.
- Preserve priority, severity, resiliency relationship, and status.
- Include the mapped Step 3A change ID.
- Exclude verified controls, observations, not-assessed controls, accepted risks, and PCF references.
- Reconcile counts with the summary table.

Include `[Back to Top](#top)`.

## 6. Standards Alignment

Create the schema-defined standards-alignment table.

Include only standards supported by grounding or supplied approved references. Use concise evidence-based status descriptions.

Do not invent standards or links.

Include `[Back to Top](#top)`.

## 7. Implementation Roadmap

Summarize Step 3A without replacing it.

Include the schema-required:

- Priority summary
- Implementation waves
- Change index
- Targeted implementation-discovery items
- Step 4 approval boundary

State that Step 4 uses the authoritative Step 3A plan and supports:

- `APPROVED_PRIORITIES`
- `APPROVED_WAVES`
- `APPROVED_CHANGE_IDS`

State that priorities are preferred and Step 4 freezes resolved change IDs before modifying source code.

This roadmap is report content only. It does not make Task Implementor responsible for generating the report.

Include `[Back to Top](#top)`.

## Report writing requirements

The report must be:

- Complete
- Professional and customer-ready
- Factual and evidence-based
- Written in direct architectural language
- Free of assistant or AI-generation references
- Free of unsupported claims
- Consistent in terminology
- Consistent in severity and priority usage
- Clear about conditional conclusions and external evidence
- Explicit that illustrative code is non-authoritative
- Conformant with `assessment-report-schema.md`

Avoid repeated boilerplate. Tailor every impact and recommendation to the actual application behavior.

## Original Source Evidence Rule
For each finding render the original Step 2 evidence exactly.
Do not reopen the repository to reconstruct code.
Do not infer source lines from illustrative code.
Do not invent excerpts.

### Mixed illustrative proposal rendering

A change may contain both generated proposals and targeted-discovery
records.

When a change contains mixed statuses:

1. Render all generated code and configuration blocks.
2. Render each generated target with its repository path and symbol.
3. Render targeted-discovery information only for the blocked target.
4. Do not replace generated proposals with one change-level
   "Targeted implementation discovery required" statement.
5. Do not imply that the entire remediation lacks illustrative code.

Use this structure:

```markdown
**Illustrative proposed implementation**

**Generated proposal: NotificationRepository**

Illustrative proposal only.

## Required Rendering
### Target file and location
- Repository path
- Symbol
- Original assessed lines
- Change ID

### Original source requiring update
Include exact Step 2 source excerpt.



### Illustrative proposed implementation
Include Step 3A illustrative code and disclaimer.

## Missing Evidence Handling
Render:
Original source excerpt: Not available in authoritative evidence artifact.


### Illustrative-code rendering and validation contract

Step 3B must preserve the distinction between concrete illustrative code and narrative remediation guidance.

For every source, configuration, build, or test target, read the corresponding Step 3A `proposed_implementation` record.

#### Generated code

When:

```yaml
illustrative_code_status: generated
```

Step 3B must:

- Verify `illustrative_code` is non-empty.
- Verify it contains code or configuration syntax appropriate to `source_language`.
- Render it in a fenced block using the supplied language.
- Render `narrative_explanation` after the code block as explanatory text.
- Never replace the block with a summary sentence.

Required order:

1. Target file and location
2. Original source requiring update
3. Illustrative proposal notice
4. Concrete illustrative code or configuration block
5. Explanation of the proposal
6. Validation requirements

#### Targeted discovery required

When:

```yaml
illustrative_code_status: targeted_discovery_required
```

Step 3B must not display the narrative explanation under a heading or field labeled `Fix` as though it were code.

Render:

```markdown
**Illustrative code status:** Targeted implementation discovery required

**Why code was not generated:** [specific discovery-required reason]

**Unresolved inputs:**
- [specific missing fact]

**Intended behavior:** [narrative explanation]
```

Do not create a fenced code block. Do not invent an example. Do not substitute prose for code.

#### Not applicable

When:

```yaml
illustrative_code_status: not_applicable
```

Render the reason the remediation has no source/configuration target. Do not emit an empty `Fix` block.

#### Invalid Step 3A proposal

Treat the Step 3A proposal as invalid when any of the following is true:

- Status is `generated` but `illustrative_code` is empty.
- Status is `generated` but the content is only a sentence or instruction.
- Status is missing for a source/configuration target.
- A targeted-discovery proposal lacks a specific reason or unresolved input.
- Narrative guidance is supplied in the code field without source syntax.

If invalid:

- Set report schema conformance to failed.
- Identify the affected change ID, finding ID, target path, and proposal defect.
- Do not silently render narrative remediation as illustrative code.
- Do not ask Task Implementor to generate the report or repair Step 3A.
- Route the defect to Step 3A planning revision.

#### Report coverage summary

Include:

```yaml
illustrative_code_conformance:
  applicable_targets: 0
  generated_code_blocks_rendered: 0
  targeted_discovery_targets_rendered: 0
  not_applicable_targets: 0
  invalid_generated_proposals: 0
  narrative_only_code_blocks_rendered: 0
  status: passed
```

The status is `passed` only when `invalid_generated_proposals` and `narrative_only_code_blocks_rendered` are both zero.

## Required schema-conformance record

Before completing, add this validation record to the report's final HTML comment:

```yaml
schema_conformance:
  schema_id: CODE-LEVEL-RESILIENCY-ASSESSMENT-REPORT
  schema_version: "1.7.0"
  required_sections_present: true
  required_section_order_valid: true
  required_finding_fields_present: true
  summary_counts_reconcile: true
  finding_matrix_reconciles: true
  roadmap_matches_plan: true
  unsupported_findings_added: false
  priorities_changed: false
  infrastructure_findings_added: false
  pcf_findings_added: false
  report_written_by_step_3b: true
  delegated_to_task_implementor: false
  status: passed
```

If any required validation fails, set `status: failed`, identify the failed checks, and do not claim the report is complete.

## Final consistency checks

Before completing:

1. Verify the schema file was read and validated.
2. Verify every required schema section exists in the required order.
3. Verify every finding in the report exists in Step 2.
4. Verify every priority matches Step 3A.
5. Verify every priority cites its governance rule.
6. Verify every detailed finding contains all required fields.
7. Verify every generated illustrative proposal comes from Step 3A and contains concrete source/configuration syntax.
8. Verify no narrative-only text is rendered as a code fix.
9. Verify every targeted-discovery record includes its specific reason and unresolved inputs.
10. Verify invalid Step 3A proposals cause report conformance failure and planning-revision routing.
11. Verify conditional findings identify conditions and evidence required.
12. Verify no `not_assessed` item is presented as noncompliant.
13. Verify summary counts match the Full Finding Matrix.
14. Verify the roadmap matches Step 3A priority and wave indexes.
15. Verify no infrastructure findings were created.
16. Verify no PCF findings or recommendations appear.
17. Verify internal links and anchors are valid.
18. Verify no unapproved links were invented.
19. Verify evidence and scope limitations are explicit.
20. Verify schema-conformance status is `passed`.
21. Verify the complete report was written by Step 3B.
22. Verify report generation was not delegated to Task Implementor.
23. Verify no application source, configuration, test, deployment, or infrastructure file was modified.
24. Verify every generated target in Step 3A is rendered even when another
  target in the same change requires discovery.
25. Verify a change-level targeted-discovery statement does not hide
  generated target-level proposals.
26. Verify blocked implementation adapters are distinguished from
  generated application abstractions and tests.

# Prompt 3B Update: Report Kafka Scenario Source and Validation

Add this subsection to Assessment Overview when Kafka is applicable:

```markdown
### Kafka Operating Scenario

- **Scenario:** <Active-Standby|Independent Regional Active-Active|Database-Independent Kafka>
- **Processing model:** <value-or-not-applicable>
- **Regional processing model:** <value-or-unresolved>
- **External side effects:** <value>
- **Kafka-backed state:** <value>
- **Scenario source:** Approved application architecture context
- **Context ID:** `<id>`
- **Context version:** `<version>`
- **Policy:** `KAFKA-OPERATING-SCENARIO` version `2.0.0`
- **Policy rule:** `KAFKA-SCENARIO-001`
- **Policy validation:** Consistent
- **Repository compatibility:** Consistent
- **Architecture confirmation required:** No
- **Kafka topology:** Independent primary and standby clusters
- **Stretched cluster:** No
- **Authoritative state alignment:** Azure SQL primary/standby
```

If inferred, report:

```markdown
- **Scenario source:** Inferred from repository-observed dependencies
- **Architecture confirmation required:** Yes
```

If conflicted or unresolved, report the reason and state that scenario-specific Kafka
controls were not assessed.

Add separate overview subsections:

1. `Repository-Observed Interactions`
2. `Supplied External Architecture Context`

Never present Akamai, F5, Application Gateway, APIM, downstream processors, or
transitive state stores as repository-discovered unless direct repository evidence exists.

External architecture context can explain scenario and impact. It cannot be used as the
original source-code evidence for a finding or as proof of deployed infrastructure noncompliance.

### Database-independent Kafka reporting

When selected, report that no application database is used, then state processing model, regional ownership, external side effects, Kafka-backed/local state, scenario source, confidence, and architecture confirmation. Do not describe database independence as automatically stateless, active-active, or safe for multi-active processing.

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

### Step 3B handoff

Write `.copilot-tracking/plans/handoffs/03B-report-summary.yml`.

Include report path, report schema identity, findings rendered by priority/status, source excerpts rendered, generated illustrative-code blocks, targeted-discovery records, report conformance, and any report-generation exceptions.

```yaml
schema_conformance_summary:
  schema_id: CODE-LEVEL-RESILIENCY-ASSESSMENT-REPORT
  schema_version: <version>
  status: passed|failed
  failed_checks: []
```

This handoff is informational and is not an input that authorizes Step 4. Step 4 remains governed by the authoritative Step 3A plan and explicit approval selectors.


## Completion contract

This phase is complete only when:

1. The full assessment report has been written at the preferred path or the complete report has been generated in the current response because both paths were blocked.
2. The report conforms to the assessment report schema.
3. All approved Step 2 findings are reconciled.
4. All Step 3A priorities and change IDs are preserved.
5. Summary counts match the Full Finding Matrix.
6. No application source, configuration, test, deployment, or infrastructure file was modified.
7. Report generation was not delegated to Task Implementor.
8. Verify that one compact handoff summary exists under `.copilot-tracking/plans/handoffs/`.

Do not report successful completion if only a report-generation plan, placeholder, shell, or backlog item was created.

Do not instruct the user to run Task Implementor to generate the report.

## Completion response

Report only:

- Generated report path
- Whether the preferred path was used
- Schema path, ID, version, and validation status
- Findings by priority
- Confirmed and conditional counts
- Number of verified controls
- Number of external evidence items
- Step 3A plan path used
- Confirmation that no findings, severities, priorities, or classifications were changed
- Confirmation that no application source, configuration, test, deployment, or infrastructure file was modified
- Confirmation that Step 3B generated the report directly and Task Implementor was not used

## Priority-Filtered Report Generation

Read `report_preferences.finding_selection` from `ASSESSMENT_SCOPE_CONTEXT`. If absent, use `all_priorities` and include P0 through P3.

### Selection algorithm

1. Validate `mode` and `include_priorities` against `assessment-scope-schema.yml`.
2. Read all authoritative Step 2 findings and Step 3A mappings before filtering.
3. Resolve every included priority to exact finding IDs and change IDs.
4. Freeze the report selection before rendering.
5. Render detailed recommendations, filtered summary counts, Full Finding Matrix, and roadmap from the frozen selection.
6. Do not modify or regenerate IDs, priorities, severity, status, category, evidence, or change mappings.
7. Preserve cross-references to excluded findings as `Not included in this priority-filtered report`.

Required machine-readable record:
```yaml
report_finding_selection:
  mode: priority_filter
  requested_priorities:
    - P0
    - P1
  included_priorities:
    - P0
    - P1
  omitted_priorities:
    - P2
    - P3
  included_finding_ids: []
  omitted_finding_ids: []
  included_change_ids: []
  omitted_change_ids: []
  selection_frozen: true
  authoritative_findings_changed: false
  priorities_recalculated: false
```

### Rendering requirements

- Title a P0/P1 view `Application Resiliency Assessment: Critical and High-Priority Findings`.
- Add a prominent `Report Scope` subsection in Assessment Overview.
- Label summary counts `Filtered Findings Summary`.
- Include only selected findings in detailed recommendation sections and the Full Finding Matrix.
- Include only selected changes in roadmap priority, wave, and change-index tables.
- Do not render empty excluded priority sections.
- State where the authoritative full assessment and plan are located.
- Apply testing-output preferences after priority selection.
- If `include_conditional_findings` is false, omit conditional findings from narrative and matrix, declare the omission, and preserve them in the authoritative Step 2 artifact.
- `include_verified_controls` and `include_evidence_gaps` remain independent of priority filtering.

### Conformance and handoff

Add the selected and omitted priority lists, finding/change counts, and frozen selection record to the final schema-conformance comment and `03B-report-summary.yml`. Validate that filtered summary, matrix, roadmap, and detailed sections reconcile exactly. A mismatch causes report conformance failure.

## Repository-Agnostic Snapshot Rendering

Render the Step 2 `assessment_snapshot` exactly as preserved by Step 3A. Do not reopen the workspace to manufacture Git metadata and do not treat non-Git snapshots as report errors.

Example non-Git rendering:

```markdown
**Repository path:** `src/main/java/example/Service.java`

**Symbol:** `Service.processPayment`

**Source fingerprint:** `sha256:1234567890ab...`

**Assessment snapshot:** Workspace snapshot `assessment-run-2026-09-09T190000Z`

**Snapshot provenance:** Workspace generated

**Original assessed lines (advisory):** 142-156

**Repository evidence:** `EV-F-001-01`
```

Show a Git commit SHA only for `git_revision`. Apply schema version 1.7.0 and record repository-agnostic snapshot conformance in the final comment and handoff.

## Incremental Report Assembly and Recovery

Generate the report through bounded incremental assembly. Do not attempt one unbounded write containing the entire report when detailed findings contain substantial evidence or illustrative code.

### Freeze before writing

Before creating the report:

1. Validate all authoritative inputs and schema version 1.7.0.
2. Freeze selected priorities, omitted priorities, selected finding IDs, selected change IDs, display IDs, categories, counts, and roadmap mappings.
3. Create the schema-required `report_assembly_manifest`.
4. Do not reconsider these values during writing or recovery.

### Bounded write sequence

1. Initialize the final report with governance metadata, title, table of contents, and the frozen manifest metadata.
2. Append Assessment Overview.
3. Append detailed recommendations one complete finding at a time.
4. Append Non-Resiliency Recommendations.
5. Append Repository and IaC Evidence Gap Analysis.
6. Append the Full Finding Matrix.
7. Append Standards Alignment.
8. Append the Implementation Roadmap.
9. Append final schema and assembly conformance metadata.
10. Reopen and validate the completed file.

Use the schema-required invisible markers before each top-level section and detailed finding.

### Finding write unit

For each selected finding:

- Read the authoritative Step 2 finding and its Step 3A change/proposals.
- Render the entire finding in memory.
- Validate all required fields and exact evidence.
- Verify its stable marker does not already exist.
- Append it once.
- Record its ID as completed.

Do not regenerate a completed finding after a recoverable error.

### Recoverable request and write errors

When a request or file-write operation recovers:

- Reopen the report.
- Inspect stable section and finding markers.
- Resume after the last verified completed unit.
- Preserve the frozen manifest.
- Do not restart report planning or generation.
- Do not duplicate content or change IDs, anchors, priorities, categories, counts, or scope.
- Record the recovery count.

If the last completed unit or file integrity cannot be established, stop, set report conformance to failed, identify the partial artifact and last verified marker, and do not claim completion.

### Source rendering safeguards

- Display source fingerprints in abbreviated form using the first 12 hexadecimal characters plus an ellipsis.
- Preserve complete fingerprints in Step 2 and Step 3A only.
- The `Original source requiring update` fenced block must contain the exact Step 2 excerpt and nothing else.
- Never insert language-specific `before` comments, labels, IDs, line annotations, or synthetic ellipses inside original-source blocks.
- Place all explanatory labels outside code fences.

### Final validation

After writing, reopen the report and verify:

- Every required section marker occurs exactly once.
- Every selected finding marker occurs exactly once.
- No omitted or unexpected finding marker exists.
- Summary, detailed findings, matrix, roadmap, and selected scope reconcile.
- Full source fingerprints remain only in authoritative artifacts.
- Original-source fenced blocks match Step 2 exactly.
- Final schema and assembly conformance are passed.

Successful Step 3B completion requires a complete validated final report, not a partial file or report text that exists only in chat.
