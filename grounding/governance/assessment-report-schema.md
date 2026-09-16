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
8. Appendix A: Traceability

Sections 1 through 7 are readable customer-facing content. Section 8 is the traceability appendix and must be rendered last.

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

### Report metadata placement and visibility

Render report metadata as a hidden HTML comment block between the `report-metadata` markers at the end of the report, after Appendix A and before the schema-conformance block. It is provenance rather than narrative, so it must not open the document.

Follow the marker pattern already used by the governance block. The `report-metadata:start` and `report-metadata:end` markers are separate comments, and the metadata itself is one comment block between them. Never nest a comment inside another comment.

Because the metadata is hidden, the readable title and its summary line carry document identification. They must state the application, and when the report is a priority-filtered view, they must state that and name the included priorities. This satisfies the priority-filtered reporting rule that the title and metadata identify the document as a filtered view.

Metadata placement and visibility are presentation-only. Every required field is still rendered, and no field may be dropped.

<!--
Superseded 2026-09-16. Retained for reference. Not active.

Report metadata was previously rendered as a visible table immediately below the H1
title, using `report-metadata` markers positioned there in the report template.

Reason: the metadata is provenance for the reader, and no downstream phase consumes it.
Step 4 resolves scope from the Step 3A plan and is explicitly prohibited from deriving
scope from the assessment report, and Step 5 reviews against Steps 2, 3A, and the Step 4
implementation record. A ten-row table ahead of all narrative reduced readability without
serving a consumer. Restore the original placement by moving the `report-metadata`
markers back beneath the H1 in the template and rendering the block visibly.
-->

## Required Assessment Overview content

- Application and repository overview
- Assessment themes with finding references
- Approved shared-service/reference-architecture table, rendered in full per the rule below, or the no-registry statement when no table and no registry are available
- Summary findings table
- Illustrative-code notice

## Required Albertsons Azure Services Reference Architectures

Render this table in full in every report. Do not drop rows for services the assessed repository does not use, because readers rely on the report to reach any approved reference architecture.

Add an Applicability column and populate it only from authoritative Step 1 and Step 2 facts, using terms such as confirmed dependency, declared-only, repository-observed, declared by supplied context only, or not evidenced within the enabled assessment domains. Applicability is descriptive presentation. It must not create, remove, or reclassify a finding.

When a service is unevidenced, say it was not evidenced within the enabled assessment domains. Never imply the service is absent from the deployed environment, because disabled domains are not assessed.

A supplied reference-architecture registry may add or override entries when it publishes reference-architecture links. A registry that only maps dependency keys to grounding standards publishes no links and must not narrow this table. Never invent a link that appears in neither this table nor a supplied registry.

| Azure Shared Service                | Link to Reference Architecture                |
| ----------------------------------- | --------------------------------------------- |
| Azure API Management                | [Reference](https://rxsafeway.sharepoint.com/:w:/r/sites/Cloud2.0/Shared%20Documents/I11%20Resiliency%20Program/Discovery/Integration%20Platform/APIM/Design/APIM%20-%20Albertsons%20Multi-Region%20Design%20v5.docx?d=w7f65ea542cc7491687202cfa68599d7b&csf=1&web=1&e=dhPvP3) |
| Azure Application Gateway           | [Reference](https://rxsafeway.sharepoint.com/:w:/r/sites/Cloud2.0/Shared%20Documents/I11%20Resiliency%20Program/Discovery/Integration%20Platform/AppGW/Design/Albertsons%20Architecture%20Design_Application%20Gateway_v1.0.docx?d=w3126f533271842c9a75d83ae93b6b6db&csf=1&web=1&e=hmksie) |
| Azure Key Vault                     | [Reference](https://rxsafeway.sharepoint.com/:w:/r/sites/Cloud2.0/Shared%20Documents/I11%20Resiliency%20Program/Discovery/Cloud%20Foundation/Design/Albertsons%20Azure%20Key%20Vault%20Architecture%20Design%20Proposal.docx?d=wf1abecab2812460a8cadd6e5956d5bb8&csf=1&web=1&e=yzvvQh) |
| Kafka                               | [Reference](https://rxsafeway.sharepoint.com/:w:/r/sites/Cloud2.0/Shared%20Documents/I11%20Resiliency%20Program/Discovery/Integration%20Platform/Kafka/Approved_Albertsons_RegionResiliency_Kafka-MultiRegion.docx?d=w08142308135244de855f4dab4c49ca2d&csf=1&web=1&e=kueuJ9) |
| Azure Entra ID                      | [Reference](https://rxsafeway.sharepoint.com/:w:/r/sites/Cloud2.0/Shared%20Documents/I11%20Resiliency%20Program/Discovery/Security/IAM/Design/ACI%20Entra%20ID%20Draft%20v1.0.docx?d=wad696d3ecdae4d84a6a1ea5675d3aec6&csf=1&web=1&e=rCLr5y) |
| Azure Storage                       | [Reference](https://rxsafeway.sharepoint.com/:w:/r/sites/Cloud2.0/Shared%20Documents/I11%20Resiliency%20Program/Discovery/Database%20Platform/Storage/Albertsons%20Architecture%20Design_Storage_v1.0.docx?d=w97ad6ce3e77348e09a1ee3e676bc3ac0&csf=1&web=1&e=C4SVMy) |
| Azure SQL Database                  | [Reference](https://rxsafeway.sharepoint.com/:f:/r/sites/Cloud2.0/Shared%20Documents/I11%20Resiliency%20Program/Discovery/Database%20Platform/SQL%20DB?csf=1&web=1&e=xMauSY) |
| Azure Cosmos DB                     | [Reference](https://rxsafeway.sharepoint.com/:w:/r/sites/Cloud2.0/Shared%20Documents/I11%20Resiliency%20Program/Discovery/Database%20Platform/Cosmos/Albertsons_Architecture_Design_MongoDB_RU_v1.0.docx?d=wa68893488e094fef9b5506690c685847&csf=1&web=1&e=YDVc7g) |
| Azure Functions                     | [Reference](https://rxsafeway.sharepoint.com/:w:/r/sites/Cloud2.0/Shared%20Documents/I11%20Resiliency%20Program/Discovery/Cloud%20Foundation/Design/Albertsons%20Azure%20Functions%20Architecture%20Design%20Proposal.docx?d=w0c59f970929f47f2a6dcef096fffd7f2&csf=1&web=1&e=tXAxCU) |
| Azure Networking                    | [Reference](https://rxsafeway.sharepoint.com/:w:/r/sites/Cloud2.0/Shared%20Documents/I11%20Resiliency%20Program/Discovery/Network/Design/Albertsons%20Architecture%20Design%20-%20Networking%20-%20Draft%201.3.docx?d=w6adb9edef1754753a259b296fffa4b1d&csf=1&web=1&e=IshBZT) |
| Azure Managed Redis                 | [Reference](https://rxsafeway.sharepoint.com/:w:/r/sites/Cloud2.0/Shared%20Documents/I11%20Resiliency%20Program/Discovery/Database%20Platform/Redis/Design/Managed%20Redis%20-%20Albertsons%20Multi-Region%20Design%20v3.docx?d=wad90acec4c154b2498d899a2ffcdc9d4&csf=1&web=1&e=L7pVbQ) |
| Azure Kubernetes Service (AKS)      | [Reference](https://rxsafeway.sharepoint.com/:w:/r/sites/Cloud2.0/Shared%20Documents/I11%20Resiliency%20Program/Discovery/Container%20Platform/Design/Albertsons%20Architecture%20Design_AKS%20and%20Istio_v1.0.docx?d=w97c0edfea59d466e80af843958d95c5c&csf=1&web=1&e=7UJSQS) |
| Azure Storage Blobs and Files       | [Reference](https://rxsafeway.sharepoint.com/:w:/r/sites/Cloud2.0/Shared%20Documents/I11%20Resiliency%20Program/Discovery/Storage/Architecture%20Options%20for%20Storage%20Blobs%20and%20Azure%20Files_v04.docx?d=w5d8203dcf43c41438843a71219ec05d8&csf=1&web=1&e=kTl0dg) |

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

<!--
Superseded 2026-09-15. Retained for reference. Not active.

  3. Priority policy ID, version, and rule ID

Reason: the internal-identifier-suppression rule moves priority rule IDs out of
sections 1 through 7. The policy ID and version remain in the finding, and the rule
ID is preserved in Appendix A, so no traceability is lost. Restore this line if
identifier suppression is withdrawn.
-->

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

<!--
Superseded 2026-09-16. Retained for reference. Not active.

  Within each priority section, repository-specific categories must be
  rendered as visually distinct grouping headers.

  Render categories using HTML:

      <h3 style="color:#0F6CBD;">
      {Category Name}
      </h3>

Reason: the title occupied H1 and top-level sections occupied H2, which left only H3 and
H4 for the four semantic levels of priority group, category, and finding. The styled HTML
heading was used to invent the missing level, but it rendered at the same level as the
priority group rather than beneath it, so categories appeared as siblings of the group
that contained them. Promoting sections to numbered H1 frees a level and allows native
headings throughout. Restore the HTML form only if the heading hierarchy above is
withdrawn.
-->

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

<!--
Superseded 2026-09-15. Retained for reference. Not active.

  - `**Notes:**` sub-bullets (`Cross-refs`, `Implementation`, `Validation`, `Guardrail`)
  - `<span style="font-size: 14px;">**MSFT Reference:** [title](url)</span>`

Reason for the Notes change: the `Cross-refs` sub-bullet carried Step 2 finding IDs,
change IDs, control IDs, and open-question IDs in body narrative. Its content moves to
Appendix A under the internal-identifier-suppression rule.

Reason for the reference change: the previous line required an external Microsoft Learn
URL for every finding, but the grounded standards publish no per-control external URLs,
and inventing one is prohibited by the required-exclusions rule. It also conflicted with
required finding field 18, "Standards reference, when supported". The active line cites
the grounded standard and still permits an external URL when one genuinely exists.

Restore both lines if identifier suppression is withdrawn.
-->

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

<!--
Superseded 2026-09-15. Retained for reference. Not active.

Previous columns included, in place of "Remediated with":

  - Change ID
  - Source ID

Reason: the internal-identifier-suppression rule moves change IDs and Step 2 source
IDs to Appendix A. "Remediated with" preserves the consolidation fact in the matrix
using display IDs. Restore these columns if identifier suppression is withdrawn.
-->

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
- Approval boundary

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

<!--
Superseded 2026-09-15. Retained for reference. Not active.

Implementation waves columns previously included:

  - Change IDs

The subsection "Remediation index" was previously named "Change index" with columns:

  - Change ID
  - Priority
  - Priority rule
  - Finding IDs
  - Objective
  - Complexity
  - Wave

Reason: the internal-identifier-suppression rule moves change IDs, finding IDs, and
priority rule IDs to Appendix A. The roadmap keys off display IDs instead. Restore
these if identifier suppression is withdrawn.
-->

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
- Invent internal links or reference architectures

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

<!--
Superseded 2026-09-16. Retained for reference. Not active.

  1. Read and validate all authoritative inputs.
  2. Freeze report scope, selected findings, display IDs, categories, and change mappings.
  3. Create a report assembly manifest.
  4. Initialize the final report with governance metadata, title, and table of contents.
  5. Append top-level sections in schema order.
  6. Append one complete detailed finding at a time.
  7. Append the Full Finding Matrix, Standards Alignment, and Implementation Roadmap.
  8. Append final conformance metadata.
  9. Reopen and validate the completed report.

Reason: this order predated Appendix A and the hidden report-metadata block, so an agent
following it would omit both. Step 4 also did not state that the assembly manifest is
written into the report, although recovery depends on finding it there. The active order
adds the two missing append steps, records the manifest in the initialize step, and uses
the distinct block names defined below.
-->

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
