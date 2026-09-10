---
name: 03a-plan
description: Create the governed authoritative remediation plan
argument-hint: "runDate=YYYY-MM-DD taskSlug=springboot-active-active-inventory planSlug=springboot-active-active-remediation-plan"
agent: agent
---

# Step 3A: Remediation Plan

## Inputs

RUN_DATE=${input:runDate:Assessment run date used by Steps 1 and 2}
TASK_SLUG=${input:taskSlug:Task slug used by Steps 1 and 2}
PLAN_SLUG=${input:planSlug:Remediation plan artifact slug}

AUTHORITATIVE_PROMPT=prompts/03A-create-authoritative-remediation-plan.prompt.md
INVENTORY_ARTIFACT=.copilot-tracking/research/${RUN_DATE}/${TASK_SLUG}-research.md
REVIEW_ARTIFACT=.copilot-tracking/reviews/${RUN_DATE}/${TASK_SLUG}-research-review.md
PRIORITY_POLICY=grounding/governance/remediation-prioritization.md
EXPECTED_PLAN_ARTIFACT=.copilot-tracking/plans/${RUN_DATE}/${PLAN_SLUG}.instructions.md
EXPECTED_HANDOFF_ARTIFACT=.copilot-tracking/plans/handoffs/03A-planning-summary.yml
PHASE_HANDOFF_SCHEMA=grounding/governance/phase-handoff-schema.yml

## Execution

All paths are workspace-relative. Do not guess alternate artifact paths. If a required artifact does not exist, stop and report the exact missing path. Read the authoritative governed prompt before acting. A handoff summary is non-authoritative and does not replace required artifacts.

Use the Task Planner behavior defined by `AUTHORITATIVE_PROMPT`.

Read `INVENTORY_ARTIFACT`, `REVIEW_ARTIFACT`, and `PRIORITY_POLICY`. Do not re-inventory, reassess, add new findings, or modify source code. Assign priority only through governed policy and mark missing policy coverage governance-blocked.

Apply the highest-confidence illustrative implementation principle. Generate concrete proposals for every evidence-supported target and isolate `targeted_discovery_required` to only blocked targets. Preserve optional assessment domains and repository ownership on changes. Preserve all tests, acceptance criteria, commands, and validation obligations regardless of later report-visibility preferences.

Do not add deployed-infrastructure or PCF remediation.

Create the compact Step 3A handoff at `EXPECTED_HANDOFF_ARTIFACT` when permitted. Report the exact plan and handoff paths. Verify the plan path against `EXPECTED_PLAN_ARTIFACT`; report the actual runtime path if different.

## Repository-agnostic snapshot rule

Preserve the repository-agnostic assessment snapshot and fingerprint. Missing Git is not targeted discovery.
