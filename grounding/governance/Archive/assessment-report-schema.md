---
document_type: assessment_report_schema
schema:
  schema_id: CODE-LEVEL-RESILIENCY-ASSESSMENT-REPORT
  schema_version: "1.1.0"
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
- Approved shared-service/reference-architecture table or no-registry statement
- Summary findings table
- Illustrative-code notice

## Required Albertsons Azure Services Reference Architectures

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

### PCF exclusion

Include:

> PCF and its aliases are retired and excluded from findings, scoring, remediation, modernization, migration, and cleanup recommendations. Historical repository references, if discovered, are informational only and are not included in the finding matrix.

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
- Invent internal links or reference architectures

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
```

### Kafka scenario reporting

When Kafka is applicable, Assessment Overview must include scenario, source, policy version/rule, validation status, architecture confirmation, processing model, regional processing model, external side effects, and Kafka-backed/local state. Allowed scenarios: `active_standby`, `independent_regional_active_active`, `database_independent_kafka`, and `unresolved`. Database-independent must not be presented as automatically stateless or multi-active.
