---
document_type: assessment_report_schema
schema:
  schema_id: CODE-LEVEL-RESILIENCY-ASSESSMENT-REPORT
  schema_version: "1.10.0"
  lifecycle_status: active
owner: Cloud Architecture Team
applies_to:
  - springboot-active-active-code-assessment
required_output_format: markdown
finding_source: step_2_authoritative_review
priority_source: step_3a_authoritative_remediation_plan
infrastructure_findings_allowed: false
pcf_findings_allowed: false
---

# Code-Level Resiliency Assessment Report Schema

## Purpose

This governance document defines the required structure and content of the customer-facing code-level resiliency assessment report. It does not define findings, severity, priority, or remediation. Those remain authoritative in the Step 2 review and Step 3A remediation plan.

## Required section order

1. Assessment Overview
2. Resiliency-Focused Recommendations
3. Non-Resiliency-Focused Recommendations
4. Repository and IaC Evidence Gap Analysis
5. Full Finding Matrix
6. Standards Alignment
7. Implementation Roadmap
8. Appendix A: Traceability

Sections 1 through 7 are readable customer-facing content. Section 8 is the traceability appendix and must be rendered last.

## Required report metadata

- Application
- Assessment date
- Repository scope
- Current deployment
- Approved target deployment
- Migration context
- Language and framework
- Runtime platform
- Report version

Use `Not provided` when required metadata is unavailable.

### Deployment-state metadata contract

Resolve deployment metadata from the approved application architecture context:

```yaml
deployment_metadata_resolution:
  current_deployment_source: architecture_context.deployment_evolution.source
  approved_target_deployment_source: architecture_context.deployment_evolution.target
  migration_context_source: architecture_context.deployment_evolution.transition
```

Rules:

- `Current deployment` is the source state marked `lifecycle_status: current`.
- `Approved target deployment` is the future state marked `lifecycle_status: approved_target`.
- Render both fields separately. Do not collapse them into one ambiguous deployment-model field.
- Do not merge source and target region lists.
- Do not report the target as current or the source as target.
- Do not substitute Azure SQL, Kafka, or another dependency topology for the application deployment topology.
- A source-to-target difference is not a finding by itself. A finding requires repository evidence against an applicable target-state control.
- Missing target infrastructure is an evidence gap, not application noncompliance.

### Report metadata placement and visibility

Render report metadata as a hidden HTML comment block between the `report-metadata` markers at the end of the report, after Appendix A and before the schema-conformance block. It is provenance rather than narrative, so it must not open the document.

Follow the marker pattern already used by the governance block. The `report-metadata:start` and `report-metadata:end` markers are separate comments, and the metadata itself is one comment block between them. Never nest a comment inside another comment.

Because the metadata is hidden, the readable title and its summary line carry document identification. They must state the application, and when the report is a priority-filtered view, they must state that and name the included priorities. This satisfies the priority-filtered reporting rule that the title and metadata identify the document as a filtered view.

Metadata placement and visibility are presentation-only. Every required field is still rendered, and no field may be dropped.

## Required Assessment Overview content

- Application and repository overview
- Current deployment, approved target deployment, and migration-context summary
- Assessment themes with finding references
- Approved Azure Shared Services reference-architecture table, rendered from
  REFERENCE_ARCHITECTURE_REGISTRY, or the no-registry statement when no approved
  registry is supplied
- Summary findings table
- Illustrative-code notice


```markdown
### Approved reference-architecture table contract

Customer-specific reference architectures are supplied by an approved registry at
`REFERENCE_ARCHITECTURE_REGISTRY`. This schema defines structure only and must not
contain customer URLs.

When an approved registry is supplied, render under the Assessment Overview heading
**Approved Azure Shared Services Reference Architectures** with these columns in order:

1. Azure Shared Service
2. Architecture Title
3. Reference
4. Approval Status
5. Version

Render entries whose `applicable_when` matches a Step 1 confirmed dependency or
capability. When no entry matches, render every approved entry. Sort by Azure Shared
Service. Render `document_status` alongside approval status so a draft or proposal
document is not presented as a final approved design.

Registry-supplied URLs are pre-approved. They are explicitly exempt from the Required
exclusions rule prohibiting invented links.

Omitting this table when an approved registry is supplied is a conformance failure.

Render the no-registry statement only when the registry is absent, unreadable, or has
a lifecycle status other than approved:

> No customer-specific reference-architecture registry was supplied. The assessment
> uses the grounded application behavior standards and cited Microsoft patterns.

A reference architecture describes intended design. It is not evidence that
infrastructure is deployed correctly and must never be used as repository source
evidence for a finding.
```

## Deployment evolution rendering contract

Assessment Overview must render these items in order:

1. **Current deployment:** Use only `architecture_context.deployment_evolution.source`.
2. **Approved target deployment:** Use only `architecture_context.deployment_evolution.target`.
3. **Migration context:** State that the assessment evaluates target-state code readiness and does not claim the target is already deployed.

Expected semantic rendering for this application:

```text
Current deployment: West US is active, with East US reserved for disaster recovery.
Approved target deployment: Active-active across West US 2 and West US using the same application artifact.
Migration context: The assessment evaluates application code readiness for the approved target while preserving existing business behavior.
```

Wording may be polished, but state, region, and lifecycle meaning must not change. If source or target is missing or conflicting, state the limitation and route it to architecture review. Do not infer deployment state from repository configuration or dependency topology.

## Summary findings table columns

- Priority
- Section
- Confirmed count
- Description

Exclude verified controls, non-findings, not-assessed controls, not-applicable controls, accepted risks, and PCF references.

## Required detailed finding fields

Every detailed finding must include:

1. Finding ID and title
2. Priority
3. Priority policy ID and version. The rule ID resolves in Appendix A.
4. Severity
5. Resiliency relationship
6. Finding status
7. Issue
8. What the recommendation solves
9. Active-active impact or operational/quality impact
10. Recommended fix
11. Repository evidence
12. Target file and location
13. Original source requiring update
14. Illustrative proposed implementation
15. Validation requirements
16. Dependencies
17. Notes
18. Standards reference, when supported

Group findings primarily by governance priority.

Priority order:

P0
P1
P2
P3

Within each priority group, optionally organize findings
by repository-specific category.

Required order:

Priority
    Category
        Finding

### Report title

The report title is H1 and precedes section 1. The template carries a generic default title.

When the report is a priority-filtered view, replace the default with a title that identifies the filtered scope, then follow it with a one-line summary naming the application, stating that the document is a priority-filtered view, and listing the included priorities.

The title and that summary line are the readable identification of the document, because report metadata is rendered as a hidden block at the end. Together they satisfy the priority-filtered reporting rule that the title and metadata identify the document as a filtered view.

### Heading hierarchy

Use native Markdown headings at every level so the document outlines, folds, and anchors correctly.

| Level | Content | Form |
|---|---|---|
| H1 | Numbered top-level section | `# 2. Resiliency-Focused Recommendations` |
| H2 | Priority group with finding count | `## P0 — Critical Resiliency Risks (9)` |
| H3 | Repository-specific category | `### Traffic Eligibility and Health` |
| H4 | Detailed finding | `#### P0-001: {title}` |

The report title is also H1 and precedes section 1.

Number top-level sections in schema order. Derive table-of-contents anchors from the rendered heading text, so `# 2. Resiliency-Focused Recommendations` is linked as `#2-resiliency-focused-recommendations`.

State the finding count in each priority heading so the reader can scan volume without counting.

Do not use HTML headings. An HTML heading is absent from editor outlines and breadcrumbs, generates no anchor, does not fold, and carries styling that can clash with dark mode and PDF export.

### Category heading rendering

Within each priority section, repository-specific categories are rendered as native H3 headings, one level below the priority group and one level above each finding.

```markdown
### {Category Name}
```

Examples:

```markdown
### Regional Data-Path Affinity
```

```markdown
### Traffic Eligibility and Health
```

```markdown
### Authoritative Data Correctness
```

Rules:

- Category headers appear once per category.
- Category headers appear before the first finding in that category.
- Findings remain rendered using the existing H4 format.
- Category headers are not findings and are not included in finding counts.
- Category headers must be visually larger than the finding heading.

### Required detailed finding content

Render each finding as an H4 heading `#### {DISPLAY_ID}: {title}` and separate
findings with `---`. Use bold-prefixed paragraph fields, not bullet lists.

Emit fields in this order:

- `**Priority: {P0|P1|P2|P3} - {risk label}**`
- `**Resiliency Related:** {Yes|No}`
- `**Issue:**`
- `**What does this solve:**`
- `**Resiliency Impact:**` (or `**Impact:**` for non-resiliency findings)
- `**Recommended Fix:**`
- `**File:** {path}:{startLine}-{endLine}`
- a `// before` fenced code block showing current state
- `**Fix:**` then one or more fenced code blocks of the proposal
- `**Notes:**` sub-bullets (`Implementation`, `Validation`, `Guardrail`)
- `<span style="font-size: 14px;">**Standards reference:** {grounded standard name and version} — `{grounding file path}`</span>`, using `[title](url)` only when the grounded standard publishes an external URL for the cited control

Derive the display ID as `{PRIORITY}-{NNN}` (sequential within priority). Apply the
same display ID everywhere, including cross-references.
### Internal identifier suppression in report body

The display ID is the only finding identifier permitted in the readable report body.

Do not emit Step 2 finding IDs, Step 3A change IDs, test IDs, control IDs, evidence IDs, open-question IDs, evidence-gap IDs, or targeted-discovery IDs anywhere in section 1 through section 7 body content. They are internal workflow identifiers and interrupt customer-facing narrative.

Apply these substitutions:

- Reference another finding by its display ID, for example `Remediated together with P0-006`.
- Express change dependencies through display IDs, for example `Depends on P0-002`.
- State acceptance criteria and test obligations in prose rather than by test ID.
- Describe an open question, evidence gap, or targeted-discovery item by its substance rather than its identifier.
- Render repository evidence through its path, symbol, and exact excerpt rather than its evidence ID, because evidence IDs embed the Step 2 finding ID.
- Cite the priority policy ID and version in the finding. Resolve the priority rule ID in Appendix A.
- Omit the `Cross-refs` notes sub-bullet from the body. Its content belongs in Appendix A.

Record every suppressed identifier in Appendix A so traceability is preserved rather than lost. Suppression is presentation-only and must not change findings, priorities, evidence, control mappings, change mappings, or validation obligations.

Hidden governance and conformance comment blocks are exempt and retain full identifiers.

Rules:
- Preserve line numbers in `**File:**` when available.
- Use fenced code blocks with the correct language.
- Every code block is an illustrative proposal.
- Do not fabricate code when Step 3A requires targeted implementation discovery.


### Illustrative code status and completeness

Every repository source, configuration, build, or test target must have exactly one Step 3A illustrative-code status:

- `generated`
- `targeted_discovery_required`
- `not_applicable`

#### Generated

`generated` requires:

- A source language or configuration format
- Target repository path
- Target symbol or property
- Referenced Step 2 evidence ID
- Non-empty illustrative code containing valid-looking syntax for the declared language
- A separate narrative explanation

Narrative instructions are not code. Text such as `Bind the properties`, `Persist stable identity`, `Add a lease`, or `Use a durable outbox` must not satisfy the illustrative-code field by itself.

#### Targeted discovery required

`targeted_discovery_required` requires:

- A specific discovery-required reason
- A list of unresolved inputs
- A narrative statement of intended behavior
- No fabricated code block

#### Not applicable

`not_applicable` is valid only for a remediation with no source, configuration, build, or test target.

#### Required report rendering

For generated proposals, render original source and illustrative proposed source as separate fenced blocks. Render explanation after the proposed block.

For targeted discovery, render the status, specific reason, unresolved inputs, and intended behavior. Do not use a fenced code block and do not label narrative text as the fix implementation.

An invalid or missing proposal status for an applicable target causes report conformance failure and requires Step 3A planning revision.

## Illustrative-code notice

Include this notice in the Assessment Overview:

> **IMPORTANT:** Hard numbers used for retry counts, timeout settings, interval timings, thread-pool sizes, cache duration, health thresholds, and circuit-breaker settings are examples unless the authoritative plan identifies an approved value. These values must be externally configurable and coordinated with application, mesh, gateway, and load-balancer budgets. All code snippets are illustrative proposals, not applied or prescriptive patches.

Label every individual illustrative code proposal:

> Illustrative proposal only. 

## Target file and location
- Repository path
- Symbol
- Original assessed lines

## Finding classifications

- Verified finding
- Conditional finding
- Evidence required / not assessed
- Verified control
- Non-finding observation

Only approved verified and conditional findings appear in finding counts and the Full Finding Matrix.

## Repository and IaC Evidence Gap Analysis

Required subsections:

### Available to review

Columns:

- Repository-visible configuration
- Current evidence
- Application resiliency interpretation
- Related findings

### Not available or externally owned

Columns:

- External evidence or configuration
- Needed to validate
- Related findings or assumptions

Absence of infrastructure evidence must not be reported as infrastructure noncompliance.

<!--### PCF exclusion

Include:

> PCF and its aliases are retired and excluded from findings, scoring, remediation, modernization, migration, and cleanup recommendations. Historical repository references, if discovered, are informational only and are not included in the finding matrix.
-->

## Full Finding Matrix columns

- ID
- Priority
- Severity
- Resiliency related
- Status
- Category
- Finding
- Remediated with
- Repository scope

Use display IDs in the `ID` and `Remediated with` columns. `Remediated with` names the other display IDs that share a single remediation change, or `—` when the finding is remediated alone. Step 2 finding IDs and Step 3A change IDs belong in Appendix A, not in this matrix.

Counts must reconcile with the Summary Findings table.

## Standards Alignment columns

- Standard or pattern
- Assessment status
- Related controls
- Related findings

Only grounded or approved references may be used.

## Implementation Roadmap content

Required subsections:

- Priority summary
- Implementation waves
- Remediation index
- Targeted implementation discovery
<!--- Approval boundary -->

Priority summary columns:

- Priority
- Change count
- Primary objective
- Release gate

Implementation waves columns:

- Wave
- Findings addressed
- Prerequisites
- Validation focus

Remediation index columns:

- Display ID
- Priority
- Objective
- Complexity
- Wave
- Remediated with

Use display IDs throughout the roadmap. Change IDs, finding IDs, and priority rule IDs belong in Appendix A.

## Appendix A: Traceability

Render Appendix A as the final section, after the Implementation Roadmap. It is the single location where internal workflow identifiers appear in readable content, so that sections 1 through 7 stay free of them while traceability is fully preserved.

Render one row per finding included in the report scope, ordered by display ID.

Columns:

- Display ID
- Step 2 finding ID
- Step 3A change ID
- Priority rule
- Proposed test IDs
- Wave
- Related controls
- Open questions, evidence gaps, and targeted-discovery items

Rules:

- Use `—` for any cell with no applicable value.
- When two findings share one remediation change, render the same change ID on both rows so consolidation is visible.
- Reproduce identifiers exactly as they appear in the authoritative Step 2 and Step 3A artifacts. Do not renumber, abbreviate, or invent identifiers.
- Include only findings within the report's selected scope. State that omitted priorities retain their identifiers in the authoritative artifacts.
- Appendix A is presentation-only. It must not add findings or alter priority, severity, status, evidence, control mappings, or change mappings.

Precede the table with the authoritative Step 2 and Step 3A artifact paths so a reader can resolve any identifier to its source.

## Required exclusions

The report must not:

- Add findings that are absent from Step 2
- Change severity or compliance status
- Change Step 3A priority
- Present not-assessed items as confirmed findings
- Create infrastructure findings
- Create PCF findings or recommendations
- Present illustrative code as an applied patch
- Invent internal links or reference architectures not supplied by an approved
  REFERENCE_ARCHITECTURE_REGISTRY

## Back-to-top links

Include `[Back to Top](#top)` at the end of each numbered top-level section.

<!-- ## Schema-conformance metadata

The generated report must record schema ID, schema version, schema path, and conformance status in HTML comments. -->

## Original source requiring update
Must contain:
- exact Step 2 source excerpt
- repository path
- original line range

## Illustrative proposed implementation
Must contain:
- Step 3A illustrative code
- disclaimer that code is illustrative

## New Conformance Checks
```yaml
schema_conformance:
  target_paths_present: true
  original_line_ranges_present: true
  original_source_excerpts_present: true
  original_source_matches_step_2: true
  illustrative_code_matches_step_3a: true
  original_and_proposed_code_separated: true
  invented_source_excerpts: false
  illustrative_code_status_present: true
  generated_proposals_contain_code: true
  narrative_only_code_blocks_rendered: false
  targeted_discovery_reasons_present: true
  invalid_generated_proposals: 0
  reference_architecture_registry_supplied: true
  reference_architecture_registry_lifecycle_status: approved
  reference_architecture_table_rendered: true
  reference_architecture_source: approved_registry
  reference_architecture_column_order_valid: true
  no_registry_statement_used: false
  invented_reference_links: 0
  deployment_source_and_target_separated: true
  current_deployment_rendered_from_source: true
  approved_target_deployment_rendered_from_target: true
  migration_context_rendered: true
  target_reported_as_current: false
  source_reported_as_target: false
  source_and_target_regions_merged: false
  dependency_topology_used_as_application_topology: false
  migration_delta_reported_as_finding: false
```

### Kafka scenario reporting

When Kafka is applicable, Assessment Overview must include scenario, source, policy version/rule, validation status, architecture confirmation, processing model, regional processing model, external side effects, and Kafka-backed/local state. Allowed scenarios: `active_standby`, `independent_regional_active_active`, `database_independent_kafka`, and `unresolved`. Database-independent must not be presented as automatically stateless or multi-active.

### Priority-filtered report views

The report may be rendered as a priority-filtered view when `report_preferences.finding_selection.mode` is `priority_filter`.

Rules:
- `include_priorities` may contain only `P0`, `P1`, `P2`, and `P3` and must contain at least one unique value.
- Filtering is a presentation operation only. It must not modify Step 2 findings, Step 3A priorities, finding IDs, change IDs, or authoritative artifacts.
- Detailed recommendation sections, Summary Findings, Full Finding Matrix, and Implementation Roadmap must include only findings and changes mapped to the selected priorities.
- Cross-references to excluded findings must remain identifiable as omitted references and must not be silently renumbered or reassigned.
- Display IDs must remain deterministic from the complete authoritative finding set. Do not renumber selected findings merely because other priorities are omitted.
- Evidence gaps and verified controls follow their independent inclusion preferences. They are not selected by remediation priority unless an authoritative priority exists.
- The report title and metadata must identify the document as a filtered view. Because report metadata is rendered as a hidden block at the end, the readable title and its summary line must carry this identification.
- Assessment Overview must list included priorities, omitted priorities, context path/version, and the authoritative Step 2 and Step 3A artifact paths.
- Filtering must not remove or alter the separate Current deployment, Approved target deployment, and Migration context fields.
- The report must state that omitted priorities remain in the authoritative assessment and remediation plan.
- Filtered counts must reconcile to filtered sections and the filtered Full Finding Matrix. Do not label filtered counts as total assessment counts.
- A filtered report must not claim full-schema coverage of omitted priorities. Schema conformance evaluates the selected report scope.

<!-- Required metadata:
```yaml
report_scope:
  selection_mode: priority_filter
  included_priorities: [P0, P1]
  omitted_priorities: [P2, P3]
  filtered_view: true
  authoritative_findings_changed: false
  priorities_recalculated: false
```

Add these conformance fields:
```yaml
priority_filter_applied: true
included_priorities_valid: true
omitted_priorities_declared: true
filtered_summary_counts_reconcile: true
filtered_matrix_reconciles: true
filtered_roadmap_reconciles: true
excluded_findings_renumbered: false
``` -->

### Repository-Agnostic Assessment Snapshot

The report must not require or imply that the assessed folder is a Git repository.

Render source locators in this order:

1. Repository path
2. Symbol or configuration/build element
3. Source fingerprint
4. Assessment snapshot type and identifier
5. Git commit SHA only when snapshot type is `git_revision`
6. Original assessed lines, labeled advisory
7. Evidence ID

Allowed snapshot types:

- `git_revision`
- `workspace_snapshot`
- `uploaded_archive`
- `source_drop`
- `unknown`

Required Assessment Overview notice:

> Source line numbers are advisory and identify the location observed in the assessed snapshot. Repository path, symbol, exact source excerpt, and source fingerprint are the primary evidence locators. The assessment snapshot may be a Git revision, workspace snapshot, uploaded archive, or source drop. Git metadata is optional.

For non-Git snapshots, render the snapshot type, identifier, provenance, and material limitations. Do not display `commit SHA: not available` as an error or evidence defect. If snapshot type is unknown, state the limitation while preserving the remaining source evidence.

<!-- Add conformance checks:

```yaml
repository_git_metadata_required: false
assessment_snapshot_type_valid: true
assessment_snapshot_identifier_present_or_explicitly_unavailable: true
git_sha_shown_only_for_git_revision: true
source_fingerprint_precedes_snapshot_and_lines: true
line_numbers_labeled_advisory: true
``` -->

### Incremental report assembly and recoverable-write protocol

Large reports must be assembled in bounded units rather than through one unbounded file-creation operation.

#### Required assembly order

1. Read and validate all authoritative inputs.
2. Freeze report scope, selected findings, display IDs, categories, and change mappings.
3. Create the assembly manifest.
4. Initialize the final report with the governance block, the assembly manifest, the title, and the table of contents.
5. Append top-level sections in schema order.
6. Append one complete detailed finding at a time.
7. Append the Full Finding Matrix, Standards Alignment, and Implementation Roadmap.
8. Append Appendix A: Traceability.
9. Append the hidden report-metadata block.
10. Append the final conformance block.
11. Reopen and validate the completed report.

#### Assembly block names

The report carries four separate machine-readable blocks. Use these names exactly and do not merge them, because each has a different purpose and position.

- **Governance block** — schema ID, version, path, and validation status. Written at the top during initialization.
- **Assembly manifest** — frozen scope, display-ID map, and mutable assembly progress. Written at the top during initialization and required for recovery.
- **Report-metadata block** — the required report metadata fields. Hidden, written near the end after Appendix A.
- **Conformance block** — schema, assembly, and source-rendering conformance. Written last.

Only the assembly manifest's `assembly_status` changes during writing. Everything frozen in the assembly order remains fixed.

The final deliverable remains one Markdown report. Temporary fragments are non-authoritative and must not replace the final report.

#### Required report assembly manifest

```yaml
report_assembly_manifest:
  report_path: .copilot-tracking/plans/reports/code-level-resiliency-assessment.md
  selected_priorities: []
  omitted_priorities: []
  selected_finding_ids: []
  selected_change_ids: []
  expected_finding_count: 0
  sections:
    - assessment_overview
    - resiliency_recommendations
    - non_resiliency_recommendations
    - evidence_gap_analysis
    - full_finding_matrix
    - standards_alignment
    - implementation_roadmap
    - appendix_traceability
  assembly_status:
    report_initialized: false
    completed_sections: []
    completed_finding_ids: []
    recovery_count: 0
    final_validation_complete: false
```

The manifest controls assembly only. It must not alter findings, priorities, IDs, evidence, or roadmap mappings.

#### Stable invisible markers

Use invisible HTML markers so recovery can identify completed units:

```html
<!-- section:assessment-overview -->
<!-- finding:F-001 -->
<!-- section:full-finding-matrix -->
```

Each expected marker must occur exactly once in the completed report.

#### Recoverable-write behavior

After a recoverable request or file-write error:

- Reopen the current report.
- Inspect stable markers and the frozen assembly manifest.
- Resume after the last completed section or finding.
- Do not restart from the beginning.
- Do not duplicate completed content.
- Do not recalculate display IDs, categories, priorities, counts, or selected scope.
- Increment `recovery_count`.

If report integrity cannot be proven, stop with conformance failed, preserve the partial report for diagnostics, identify the last completed unit, and do not claim successful completion.

#### Fingerprint display

Authoritative artifacts retain complete source fingerprints. In the customer report display only the algorithm and first 12 hexadecimal characters followed by an ellipsis, for example:

```text
sha256:12ab34cd56ef...
```

The abbreviated report value must not be used for programmatic validation.

#### Exact original source blocks

The fenced block under `Original source requiring update` must contain only the exact Step 2 `original_source_excerpt`.

Do not insert `Before`, `Current`, finding IDs, evidence IDs, line comments, explanatory comments, or synthetic ellipses inside the original-source block. Place labels outside the fenced block.

<!-- #### Required assembly conformance

```yaml
report_assembly_conformance:
  incremental_assembly_used: true
  report_manifest_frozen: true
  selected_findings_written_once: true
  required_sections_written_once: true
  duplicate_section_markers: 0
  duplicate_finding_markers: 0
  missing_selected_finding_markers: 0
  unexpected_finding_markers: 0
  report_reopened_after_write: true
  final_report_parse_complete: true
  recovery_count: 0

source_rendering_conformance:
  full_fingerprints_preserved_in_authoritative_artifacts: true
  report_fingerprints_abbreviated: true
  original_source_blocks_unmodified: true
  comments_added_inside_original_source_blocks: false
``` -->
