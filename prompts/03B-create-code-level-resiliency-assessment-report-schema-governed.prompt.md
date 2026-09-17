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
INVENTORY_ARTIFACT=.copilot-tracking/research/{{YYYY-MM-DD}}/{{task_slug}}-research.md
REVIEW_ARTIFACT=<exact Step 2 authoritative review artifact or output path>
PLAN_ARTIFACT=<exact Step 3A authoritative remediation-plan artifact>
APPLICATION_CONTEXT=<optional application-context file path>
REFERENCE_ARCHITECTURE_REGISTRY=<optional approved reference-architecture registry path>
REPORT_SCHEMA=grounding/governance/assessment-report-schema.md
REPORT_TEMPLATE=grounding/governance/templates/code-level-resiliency-assessment-template.md
REPORT_OUTPUT_PATH=<optional; defaults to .copilot-tracking/plans/reports/code-level-resiliency-assessment.md>
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
  schema_version: "<active-version-read-from-REPORT_SCHEMA>"
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

### Schema-version and template-value rules

Read `schema_id`, `schema_version`, and `lifecycle_status` directly from `REPORT_SCHEMA`. Do not hardcode an expected schema version in this prompt or generated report. Require the schema ID to equal `CODE-LEVEL-RESILIENCY-ASSESSMENT-REPORT` and lifecycle status to be `active`; preserve the version actually read.

Pipe-delimited placeholders in examples describe allowed values only. Generated artifacts must contain one concrete value. Emit `status: passed`, never `status: passed|failed`.

### Source locator authority

Render and validate source locators in this order:

1. Repository path
2. Symbol or configuration/build element
3. Exact original source excerpt
4. Source fingerprint
5. Assessment snapshot
6. Original assessed line range, explicitly labeled advisory

Line numbers are navigation metadata. Never present a line number alone as the authoritative locator, recalculate Step 2 line numbers, or treat line drift as evidence drift.

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
  schema_version: "<active-version-read-from-REPORT_SCHEMA>"
  schema_path: grounding/governance/assessment-report-schema.md
  schema_validation: passed
  generated_by_phase: Step 3B
  artifact_type: assessment_documentation
  implementation_artifact: false
-->
```

#### Canonical template rendering contract

Use `REPORT_TEMPLATE` as the fixed starting skeleton. Do not reconstruct the report layout from memory. Validate the eight required section headings, their order, all fixed section markers, and every authorized insertion-region marker before writing.

Write content only between the template's matching `:start` and `:end` markers. Preserve fixed headings, table-of-contents links, section markers, and back-to-top links unchanged, except for the H1 title, which the schema's report-title rule governs when the report is a filtered view. Insert `<!-- finding:{STEP_2_FINDING_ID} -->` immediately before each detailed finding, exactly once per selected finding.

Render the shared-service reference-architecture table from the schema's required Albertsons Azure Services table in full. It is required content and the schema is authoritative for required content, so do not drop rows for services this repository does not use. Mark each row's applicability from authoritative Step 1 and Step 2 facts instead, and state that an unevidenced service was not evidenced within the enabled assessment domains rather than implying it is absent from the deployed environment.

When `REFERENCE_ARCHITECTURE_REGISTRY` is supplied and publishes reference-architecture links, add or override entries from it, because a supplied registry is the more current customer source. A registry that only maps dependency keys to grounding standards publishes no links and must not narrow the table. When the schema carries no table and no registry is supplied, render the schema-required no-registry statement.

Never invent a reference-architecture URL that appears in neither the schema nor a supplied registry.

### Schema-driven report rendering

Follow `assessment-report-schema.md` exactly for top-level sections, section order, required finding fields, notices, tables, finding matrix, standards alignment, roadmap, priority filtering, testing-output preferences, source-locator display, and report conformance.

Do not reproduce or reinterpret the schema contract from memory. For each required section:

- Preserve the section even when authoritative content is unavailable.
- Use the schema-defined unavailable-content behavior.
- Render only authoritative Step 1, Step 2, and Step 3A facts.
- Preserve Step 2 finding status and severity and Step 3A priority and change mapping.
- Apply the frozen report selection consistently to detailed findings, summary, matrix, and roadmap.
- Render exact Step 2 source excerpts and Step 3A illustrative proposals according to their target-level status.
- Display source locators using the authority order defined in this prompt.

The final report must include every schema-required top-level section exactly once and in schema order. Repository-specific categories may appear only beneath schema-authorized sections.

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
  schema_version: "<active-version-read-from-REPORT_SCHEMA>"
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

### Kafka scenario reporting

When Kafka is applicable, render the Step 1 scenario declaration, provenance, policy validation, processing model, regional processing model, external-side-effect classification, Kafka-backed state, conditional assumptions, architecture confirmation requirement, and unresolved infrastructure facts exactly as required by `REPORT_SCHEMA` and the authoritative Kafka policy.

Do not recreate scenario inference in Step 3B. Keep repository-observed interactions and supplied architecture context separate. Do not present context as source-code evidence or as proof of deployed infrastructure.

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
```

Show a Git commit SHA only for `git_revision`. Apply the active schema version read from `REPORT_SCHEMA` and record repository-agnostic snapshot conformance in the final comment and handoff.

## Incremental Report Assembly and Recovery

Generate the report through bounded incremental assembly. Do not attempt one unbounded write containing the entire report when detailed findings contain substantial evidence or illustrative code.

### Freeze before writing

Before creating the report:

1. Validate all authoritative inputs and the active schema version read from `REPORT_SCHEMA`.
2. Freeze selected priorities, omitted priorities, selected finding IDs, selected change IDs, display IDs, categories, counts, and roadmap mappings.
3. Create the schema-required `report_assembly_manifest`.
4. Do not reconsider these values during writing or recovery.

Freezing applies to scope, identifiers, counts, and mappings. The assembly manifest's `assembly_status` is progress tracking and is expected to change as sections and findings are appended.

### Bounded write sequence

1. Initialize the final report with the governance block, the assembly manifest, the title, and the table of contents.
2. Append Assessment Overview.
3. Append detailed recommendations one complete finding at a time.
4. Append Non-Resiliency Recommendations.
5. Append Repository and IaC Evidence Gap Analysis.
6. Append the Full Finding Matrix.
7. Append Standards Alignment.
8. Append the Implementation Roadmap.
9. Append Appendix A: Traceability.
10. Append the hidden report-metadata block.
11. Append the final conformance block.
12. Reopen and validate the completed file.

Use the schema's assembly block names. The governance block, assembly manifest, report-metadata block, and conformance block are four separate blocks in three positions, and none substitutes for another. The report-metadata block is the required report metadata fields, is hidden, and belongs after Appendix A rather than beneath the title.

Use the schema-required invisible markers before each top-level section and detailed finding.

### Internal identifier suppression

Sections 1 through 7 are customer-facing narrative and must not contain internal workflow identifiers. Follow the schema's internal-identifier-suppression rule exactly.

Do not emit Step 2 finding IDs, Step 3A change IDs, test IDs, control IDs, priority rule IDs, open-question IDs, evidence-gap IDs, or targeted-discovery IDs in body content. Reference findings, dependencies, and consolidation through display IDs. State test obligations, open questions, evidence gaps, and discovery items in prose. Omit the `Cross-refs` notes sub-bullet.

Carry every suppressed identifier into Appendix A so nothing is lost. Suppression and appendix placement are presentation-only and must not change findings, priorities, severity, status, evidence, control mappings, change mappings, or validation obligations.

Hidden governance, manifest, and conformance comment blocks retain full identifiers and are exempt.

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
