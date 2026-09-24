---
name: 02-findings
description: Generate authoritative findings from the Step 1 inventory
argument-hint: "runDate=YYYY-MM-DD taskSlug=springboot-active-active-inventory"
agent: Task Reviewer
---

# Step 2: Findings

## Inputs

RUN_DATE=${input:runDate:Assessment run date used by Step 1}
TASK_SLUG=${input:taskSlug:Task slug used by Step 1}

AUTHORITATIVE_PROMPT=prompts/02-generate-findings-from-hve-research.prompt.md
INVENTORY_ARTIFACT=.copilot-tracking/research/${RUN_DATE}/${TASK_SLUG}-research.md
EXPECTED_REVIEW_ARTIFACT=.copilot-tracking/reviews/${RUN_DATE}/${TASK_SLUG}-research-review.md
EXPECTED_HANDOFF_ARTIFACT=.copilot-tracking/reviews/handoffs/02-assessment-summary.yml
PHASE_HANDOFF_SCHEMA=grounding/governance/phase-handoff-schema.yml

## Execution

All paths are workspace-relative. Do not guess alternate artifact paths. If a required artifact does not exist, stop and report the exact missing path. Read the authoritative governed prompt before acting. A handoff summary is non-authoritative and does not replace required artifacts.

Use the Task Reviewer agent behavior defined by `AUTHORITATIVE_PROMPT`. This prompt binds that agent through its `agent` frontmatter field. Before any other action, read `AUTHORITATIVE_PROMPT` in full and treat it as the governing specification for this phase; it overrides conflicting default agent behavior. If it cannot be read, stop and report the exact path.

Read `INVENTORY_ARTIFACT`. Do not re-inventory the repository. Evaluate only the master, dependency, and assessment-domain standards listed by Step 1. Open repository files only when cited by the inventory and needed to validate a specific control.

Preserve the Step 1 assessment-scope resolution and architecture/Kafka scenario provenance. Generate findings only for enabled domains and repository-owned evidence. Do not assign remediation priority. Do not invoke Task Researcher, researcher subagents, or modify source code.

Create the compact Step 2 handoff at `EXPECTED_HANDOFF_ARTIFACT` when permitted. Report the exact review and handoff paths. Verify the review path against `EXPECTED_REVIEW_ARTIFACT`; report the runtime-selected path if different.

## Next phase

End the response with the exact next command, substituting resolved values:

`/03a-plan runDate=${RUN_DATE} taskSlug=${TASK_SLUG} planSlug=<plan-slug>`

Step 3A runs as `Task Planner` in a new conversation. Do not continue into Step 3A from this conversation.

## Repository-agnostic snapshot rule

Do not require Git metadata. Capture assessment_snapshot, exact excerpt fingerprint, path, symbol, and advisory line range.


## Resiliency and non-resiliency finding classification contract
Use `grounding/governance/resiliency-finding-qualification-policy.yml` version 1.1.0. Preserve every evidence-backed applicable control violation as either `resiliency` or `non_resiliency`. Do not suppress a valid non-resiliency finding merely because it fails the resiliency gate. Resiliency classification requires a credible failure scenario, approved resiliency domain, target-architecture element, causal mechanism, and material impact. Preserve classification and rationale across phase artifacts. Business-logic risk remains a separate implementation-approval dimension.
