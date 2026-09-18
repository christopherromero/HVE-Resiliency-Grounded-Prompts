---
name: 03b-report
description: Generate the schema-governed priority-filtered resiliency assessment report
argument-hint: "runDate=YYYY-MM-DD taskSlug=springboot-active-active-inventory planSlug=springboot-active-active-remediation-plan"
agent: agent
---

# Step 3B: Assessment Report

## Inputs

RUN_DATE=${input:runDate:Assessment run date used by Steps 1 through 3A}
TASK_SLUG=${input:taskSlug:Task slug used by Steps 1 and 2}
PLAN_SLUG=${input:planSlug:Plan slug used by Step 3A}

AUTHORITATIVE_PROMPT=prompts/03B-create-code-level-resiliency-assessment-report-schema-governed.prompt.md
INVENTORY_ARTIFACT=.copilot-tracking/research/${RUN_DATE}/${TASK_SLUG}-research.md
REVIEW_ARTIFACT=.copilot-tracking/reviews/${RUN_DATE}/${TASK_SLUG}-research-review.md
PLAN_ARTIFACT=.copilot-tracking/plans/${RUN_DATE}/${PLAN_SLUG}.instructions.md
REPORT_SCHEMA=grounding/governance/assessment-report-schema.md
REPORT_TEMPLATE=grounding/governance/templates/code-level-resiliency-assessment-template.md
APPLICATION_CONTEXT=application-context/assessment-context.md
APPLICATION_ARCHITECTURE_CONTEXT=application-context/application-architecture-context.yml
SOLUTION_ARCHITECTURE_CONTEXT=application-context/solution-architecture-context.yml
REFERENCE_ARCHITECTURE_REGISTRY=application-context/reference-architecture-registry.yml
ASSESSMENT_SCOPE_CONTEXT=application-context/assessment-scope-context.yml
ASSESSMENT_SCOPE_SCHEMA=grounding/governance/assessment-scope-schema.yml
EXPECTED_HANDOFF_ARTIFACT=.copilot-tracking/plans/handoffs/03B-report-summary.yml
PHASE_HANDOFF_SCHEMA=grounding/governance/phase-handoff-schema.yml

## Execution

All paths are workspace-relative. Do not guess alternate artifact paths. If a required artifact does not exist, stop and report the exact missing path. Read the authoritative governed prompt before acting. A handoff summary is non-authoritative and does not replace required artifacts.

Use the Task Planner reporting behavior defined by `AUTHORITATIVE_PROMPT`.

Read and validate `REPORT_SCHEMA` and `ASSESSMENT_SCOPE_CONTEXT`. Read the three authoritative phase artifacts before rendering. Apply `report_preferences.finding_selection` and `report_preferences.testing_output` exactly.

Filtering is presentation-only. Do not change findings, status, severity, priority, evidence, controls, change mappings, validation obligations, or remediation plans. Do not renumber selected findings. Declare included and omitted priorities and preserve stable cross-references.

Do not add notes to each finding merely stating that configured report content was intentionally omitted. Use the report-scope and testing-output declarations required by the schema instead.

Do not create new findings, infrastructure findings, or PCF findings and recommendations.

Create the compact Step 3B handoff at `EXPECTED_HANDOFF_ARTIFACT` when permitted. Report the exact assessment-report and handoff paths.

## Incremental report assembly requirement

Use the incremental assembly and recoverable-write protocol in the authoritative Step 3B prompt and the active report schema version read from REPORT_SCHEMA.

Freeze the report manifest before writing. Append bounded sections and one complete finding at a time. Use stable invisible markers and resume after the last verified completed unit following a recoverable request error. Do not restart report planning, duplicate completed content, or change IDs, counts, priorities, categories, or scope.

Abbreviate source fingerprints in the customer report. Preserve exact Step 2 source excerpts without adding comments or labels inside original-source code blocks. Reopen and validate the final report before claiming completion.


## Resiliency and non-resiliency finding classification contract
Use `grounding/governance/resiliency-finding-qualification-policy.yml` version 1.0.0. Preserve every evidence-backed applicable control violation as either `resiliency` or `non_resiliency`. Do not suppress a valid non-resiliency finding merely because it fails the resiliency gate. Resiliency classification requires a credible failure scenario, approved resiliency domain, target-architecture element, causal mechanism, and material impact. Preserve classification and rationale across phase artifacts. Business-logic risk remains a separate implementation-approval dimension.
