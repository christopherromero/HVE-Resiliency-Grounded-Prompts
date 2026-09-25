---
document_type: assessment_report_schema
schema:
  schema_id: CODE-LEVEL-RESILIENCY-ASSESSMENT-REPORT
  schema_version: "1.7.0"
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

## Required report metadata

- Application
- Assessment date
- Repository scope
- Current deployment
- Target deployment
- Language and framework
- Runtime platform
- Report version

Use `Not provided` when required metadata is unavailable.

## Required Assessment Overview content

- Application and repository overview
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
3. Priority policy ID, version, and rule ID
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

### Category heading rendering

Within each priority section, repository-specific categories must be
rendered as visually distinct grouping headers.

Render categories using HTML:

```html
<h3 style="color:#0F6CBD;">
{Category Name}
</h3>
```

Examples:

```html
<h3 style="color:#0F6CBD;">
Regional Data-Path Affinity
</h3>
```

```html
<h3 style="color:#0F6CBD;">
Traffic Eligibility and Health
</h3>
```

```html
<h3 style="color:#0F6CBD;">
Authoritative Data Correctness
</h3>
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
- `**Notes:**` sub-bullets (`Cross-refs`, `Implementation`, `Validation`, `Guardrail`)
- `<span style="font-size: 14px;">**MSFT Reference:** [title](url)</span>`

Derive the display ID as `{PRIORITY}-{NNN}` (sequential within priority). Apply the
same display ID everywhere, including cross-references, and keep the Step 2 source ID
in the Full Finding Matrix "Source ID" column.

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
- Change ID
- Source ID
- Repository scope

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
- Change index
- Targeted implementation discovery
- Approval boundary

Priority summary columns:

- Priority
- Change count
- Primary objective
- Release gate

Implementation waves columns:

- Wave
- Change IDs
- Findings addressed
- Prerequisites
- Validation focus

Change index columns:

- Change ID
- Priority
- Priority rule
- Finding IDs
- Objective
- Complexity
- Wave

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

## Schema-conformance metadata

The generated report must record schema ID, schema version, schema path, and conformance status in HTML comments.

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
- The report title and metadata must identify the document as a filtered view.
- Assessment Overview must list included priorities, omitted priorities, context path/version, and the authoritative Step 2 and Step 3A artifact paths.
- The report must state that omitted priorities remain in the authoritative assessment and remediation plan.
- Filtered counts must reconcile to filtered sections and the filtered Full Finding Matrix. Do not label filtered counts as total assessment counts.
- A filtered report must not claim full-schema coverage of omitted priorities. Schema conformance evaluates the selected report scope.

Required metadata:
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

```

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

Add conformance checks:

```yaml
repository_git_metadata_required: false
assessment_snapshot_type_valid: true
assessment_snapshot_identifier_present_or_explicitly_unavailable: true
git_sha_shown_only_for_git_revision: true
source_fingerprint_precedes_snapshot_and_lines: true
line_numbers_labeled_advisory: true
```

### Incremental report assembly and recoverable-write protocol

Large reports must be assembled in bounded units rather than through one unbounded file-creation operation.

#### Required assembly order

1. Read and validate all authoritative inputs.
2. Freeze report scope, selected findings, display IDs, categories, and change mappings.
3. Create a report assembly manifest.
4. Initialize the final report with governance metadata, title, and table of contents.
5. Append top-level sections in schema order.
6. Append one complete detailed finding at a time.
7. Append the Full Finding Matrix, Standards Alignment, and Implementation Roadmap.
8. Append final conformance metadata.
9. Reopen and validate the completed report.

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

#### Required assembly conformance

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
```
