---
name: 05-review
description: Review the frozen Step 4 remediation implementation and determine finding closure
argument-hint: "runDate=YYYY-MM-DD taskSlug=springboot-active-active-inventory planSlug=springboot-active-active-remediation-plan implementationArtifact=.copilot-tracking/changes/.../implementation-record.md"
agent: agent
---

# Step 5: Review Implemented Remediation

## Inputs

RUN_DATE=${input:runDate:Assessment run date used by Steps 1 through 3A}
TASK_SLUG=${input:taskSlug:Task slug used by Steps 1 and 2}
PLAN_SLUG=${input:planSlug:Plan slug used by Step 3A}
IMPLEMENTATION_ARTIFACT=${input:implementationArtifact:Exact Step 4 implementation artifact path}

AUTHORITATIVE_PROMPT=prompts/05-review-implemented-remediation-complete-priority-aware.prompt.md
INVENTORY_ARTIFACT=.copilot-tracking/research/${RUN_DATE}/${TASK_SLUG}-research.md
REVIEW_ARTIFACT=.copilot-tracking/reviews/${RUN_DATE}/${TASK_SLUG}-research-review.md
PLAN_ARTIFACT=.copilot-tracking/plans/${RUN_DATE}/${PLAN_SLUG}.instructions.md
EXPECTED_HANDOFF_ARTIFACT=.copilot-tracking/reviews/handoffs/05-review-summary.yml
PHASE_HANDOFF_SCHEMA=grounding/governance/phase-handoff-schema.yml

## Execution

All paths are workspace-relative. Do not guess alternate artifact paths. If a required artifact does not exist, stop and report the exact missing path. Read the authoritative governed prompt before acting. A handoff summary is non-authoritative and does not replace required artifacts.

Run the `/rpi-review` workflow and use the Task Reviewer behavior defined by `AUTHORITATIVE_PROMPT`.

Read `IMPLEMENTATION_ARTIFACT` and use its frozen `resolved_change_ids`. Do not recompute selectors. Review only that frozen scope against Step 2 findings, Step 3A acceptance and validation requirements, Step 4 implementation evidence, and the current repository state.

Do not re-inventory, repeat the full assessment, recalculate priorities, create unrelated findings, or modify source code. Report scope violations separately. Report filtering and hidden testing output must not affect closure decisions.

Write the authoritative post-implementation review in the agent-authorized reviews area and create the compact Step 5 handoff at `EXPECTED_HANDOFF_ARTIFACT` when permitted. Report exact paths.
