---
name: 04-implement
description: Implement the approved remediation scope from the Step 3A plan
argument-hint: "runDate=YYYY-MM-DD taskSlug=springboot-active-active-inventory planSlug=springboot-active-active-remediation-plan priorities=P0,P1 waves= changeIds="
agent: agent
---

# Step 4: Implement Approved Remediation

## Inputs

RUN_DATE=${input:runDate:Assessment run date used by Steps 1 through 3A}
TASK_SLUG=${input:taskSlug:Task slug used by Steps 1 and 2}
PLAN_SLUG=${input:planSlug:Plan slug used by Step 3A}
APPROVED_PRIORITIES=${input:priorities:Comma-separated priorities, for example P0,P1}
APPROVED_WAVES=${input:waves:Optional comma-separated approved waves}
APPROVED_CHANGE_IDS=${input:changeIds:Optional comma-separated approved change IDs}

AUTHORITATIVE_PROMPT=prompts/04-implement-approved-remediation-complete-priority-aware.prompt.md
INVENTORY_ARTIFACT=.copilot-tracking/research/${RUN_DATE}/${TASK_SLUG}-research.md
REVIEW_ARTIFACT=.copilot-tracking/reviews/${RUN_DATE}/${TASK_SLUG}-research-review.md
PLAN_ARTIFACT=.copilot-tracking/plans/${RUN_DATE}/${PLAN_SLUG}.instructions.md
EXPECTED_HANDOFF_ARTIFACT=.copilot-tracking/changes/handoffs/04-implementation-summary.yml
PHASE_HANDOFF_SCHEMA=grounding/governance/phase-handoff-schema.yml

## Execution

All paths are workspace-relative. Do not guess alternate artifact paths. If a required artifact does not exist, stop and report the exact missing path. Read the authoritative governed prompt before acting. A handoff summary is non-authoritative and does not replace required artifacts.

Run the `/rpi-implement` workflow and use the Task Implementor behavior defined by `AUTHORITATIVE_PROMPT`.

Resolve implementation scope from `PLAN_ARTIFACT` using the supplied approved selectors, then freeze the exact change-ID set before editing. If all selectors are empty, stop and request an explicit approval selector. Do not derive implementation scope from the assessment report.

Implement only the frozen approved change IDs. Do not re-inventory, reassess, recalculate priority, redesign architecture, or broaden scope. Optional delivery files may be modified only when their assessment domain, repository ownership, artifact class, and approved change mapping permit it.

Run the plan-required validation. Do not commit, push, create a pull request, execute a live deployment, or modify deployed infrastructure.

Write the authoritative implementation record in the agent-authorized changes area and create the compact Step 4 handoff at `EXPECTED_HANDOFF_ARTIFACT` when permitted. Report exact paths.
