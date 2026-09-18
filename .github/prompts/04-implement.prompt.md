---
name: 04-implement
description: Implement the approved remediation scope from the Step 3A plan
argument-hint: "runDate=YYYY-MM-DD taskSlug=springboot-active-active-inventory planSlug=springboot-active-active-remediation-plan priorities=P0,P1 waves= changeIds= commitMode=none"
agent: agent
---

# Step 4: Implement Approved Remediation

## Inputs

RUN_DATE=${input:runDate:Assessment run date used by Steps 1 through 3A}
TASK_SLUG=${input:taskSlug:Task slug used by Steps 1 and 2}
PLAN_SLUG=${input:planSlug:Plan slug used by Step 3A}
APPROVED_PRIORITIES=${input:priorities:Comma-separated priorities, for example P0,P1}
APPROVED_WAVES=${input:waves:Comma-separated implementation waves, for example 1,2; leave empty when unused}
APPROVED_CHANGE_IDS=${input:changeIds:Comma-separated Step 3A change IDs; leave empty when unused}
COMMIT_MODE=${input:commitMode:Commit mode: none or per_change; default none}
PUSH_ALLOWED=false
BRANCH_CREATION_ALLOWED=false
PULL_REQUEST_CREATION_ALLOWED=false
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

Run the plan-required validation.

Validate `COMMIT_MODE` before modifying files:

- `none`: do not create commits.
- `per_change`: implement and validate one complete Step 3A change ID, then create one atomic local commit for that change before beginning the next change. Include every finding mapped to that root-cause change ID. Do not combine unrelated change IDs.
- Any other value: stop before modifying files and report the invalid value.

For `per_change`, require an existing Git repository and a clean starting worktree. Never run `git init`. Do not commit a failed, blocked, partial, or unvalidated change. Stage only files mapped to the current change plus necessary supporting files. Record the commit SHA and subject from Git.

`PUSH_ALLOWED`, `BRANCH_CREATION_ALLOWED`, and `PULL_REQUEST_CREATION_ALLOWED` remain `false`. Do not push, create a branch, create a pull request, execute a live deployment, or modify deployed infrastructure.

Write the authoritative implementation record in the agent-authorized changes area and create the compact Step 4 handoff at `EXPECTED_HANDOFF_ARTIFACT` when permitted. Report exact paths.

## Repository-agnostic snapshot rule

Resolve source drift without requiring Git. Compare path, symbol, excerpt, and fingerprint; line numbers remain advisory.


### Commit-mode handoff requirements

Record `commit_mode`, commit status by change ID, commit SHA and subject when created, validation status, and whether push, branch creation, or pull-request creation occurred. Do not claim a commit exists unless Git confirms the SHA. If `per_change` is selected in a non-Git workspace, do not initialize Git; record `skipped_non_git_workspace` and follow the authoritative Prompt 4 rules for whether uncommitted implementation may continue.


## Resiliency and non-resiliency finding classification contract
Use `grounding/governance/resiliency-finding-qualification-policy.yml` version 1.0.0. Preserve every evidence-backed applicable control violation as either `resiliency` or `non_resiliency`. Do not suppress a valid non-resiliency finding merely because it fails the resiliency gate. Resiliency classification requires a credible failure scenario, approved resiliency domain, target-architecture element, causal mechanism, and material impact. Preserve classification and rationale across phase artifacts. Business-logic risk remains a separate implementation-approval dimension.
