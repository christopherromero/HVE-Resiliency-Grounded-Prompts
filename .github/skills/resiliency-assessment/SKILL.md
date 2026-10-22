---
name: resiliency-assessment
description: 'Route new, resumed, or status-only resiliency assessments to HVE agents - Brought to you by microsoft/hve-core'
user-invocable: true
compatibility: 'Requires Claude Opus 5.5 and the HVE Core agents declared by the workspace wrapper prompts'
---

# Resiliency Assessment Routing

## Overview

Resolve one next step and its invocation from repository artifacts.
The caller executes that step. This skill does not perform assessment work, launch agents, or write workflow artifacts.
Paths below are relative to the assessment workspace root, not the installed skill folder.
This branch executes through Claude Opus 5.5 as required by repository governance and the bound agents' model metadata. VS Code uses `Claude Opus 5.5 (copilot)`; the Copilot SDK task tool uses `claude-opus-5.5`. Routing never selects a fallback model.

## Prerequisites

Read `.github/copilot-instructions.md` before routing.
For the target step, read the wrapper and authoritative prompt listed below.
Stop with the exact expected path if a required file is missing.

Use each source for one purpose:

* Repository instructions govern boundaries, evidence, authority, and approvals.
* Authoritative step prompts govern work, prerequisites, completion, and handoffs.
* Wrapper frontmatter binds the HVE agent. Wrapper inputs bind argument names and caller-supplied paths.
* Completed authoritative artifacts establish run state. Handoff summaries are non-authoritative indexes only.
* The owning step applies the schemas and policies referenced by its authoritative prompt.

Do not load the orchestrator agent to resolve routing. It consumes this skill, not the reverse.
Do not duplicate assessment, priority, classification, report, or closure rules here.

## Quick start

* `Start a new assessment`: resolve new-run inputs and return Step 1.
* `Resume the assessment`: identify the existing run and return its next eligible step.
* `Check assessment status`: validate existing artifacts and report state without running anything.
* A named step: resolve that step only, validate its prerequisites, and confirm any overwrite.

The orchestrator chains Steps 1 through 3B, stops for approval, then chains Steps 4 and 5 after approval.
Manual execution uses a fresh chat for each step.

## Step map

Read the bound agent and argument contract from the wrapper rather than maintaining another agent/input map.

| Step   | Wrapper                                        | Authoritative prompt                                                                     |
| ------ | ---------------------------------------------- | ---------------------------------------------------------------------------------------- |
| 1      | `.github/prompts/01-inventory.prompt.md`       | `prompts/01-create-inventory-hve-task-researcher.prompt.md`                              |
| 2      | `.github/prompts/02-findings.prompt.md`        | `prompts/02-generate-findings-from-hve-research.prompt.md`                               |
| 3A     | `.github/prompts/03a-plan.prompt.md`           | `prompts/03A-create-authoritative-remediation-plan.prompt.md`                            |
| 3B     | `.github/prompts/03b-report.prompt.md`         | `prompts/03B-create-code-level-resiliency-assessment-report-schema-governed.prompt.md`   |
| 4      | `.github/prompts/04-implement.prompt.md`       | `prompts/04-implement-approved-remediation-complete-priority-aware.prompt.md`            |
| 5      | `.github/prompts/05-review.prompt.md`          | `prompts/05-review-implemented-remediation-complete-priority-aware.prompt.md`            |

## Run identity

Resolve intent before assigning defaults. Ask when new versus resume is unclear.

For a new run:

1. Use user-supplied values first. Default `runDate` to the current date in `YYYY-MM-DD` format.
2. If application files are directly under `source/`, use `source` as `sourceRoot`. If the application is in one child folder, use that folder. Ask when several application roots are plausible; stop if no application source exists.
3. Default `taskSlug` to the final segment of `sourceRoot`, and `planSlug` to `<taskSlug>-remediation-plan` when a plan is needed.
4. Check for an existing run with the same date and task slug before creating anything. Do not overwrite it or silently merge two runs.

For a resumed run:

1. Inspect run-scoped artifacts under `.copilot-tracking/research/`, `reviews/`, `plans/`, and `changes/`.
2. Match the user's date, slug, or exact artifact path. If one run matches, state its identity and use it. If several match, ask the user to select one.
3. Recover values from that run's authoritative artifacts and declared paths. Ask for values that cannot be recovered uniquely. Do not apply today's date or new-run slug defaults to an existing run.
4. Keep an explicitly supplied implementation artifact tied to its own run and plan. Never choose an implementation record by newest timestamp alone.

For Step 3B, derive `reportDate` from the resolved `runDate` as `MM-DD-YYYY`.
Derive `microserviceSlug` by lowercasing `taskSlug` and removing a trailing `-inventory` suffix.
These derived names never establish run identity.
Handoff paths are not run-scoped and cannot establish run identity either.

## Routing procedure

### 1. Classify existing artifacts

For each artifact needed to determine the current state:

1. Read its owning authoritative prompt and resolve its exact path using Artifact paths below.
2. Validate the artifact against that prompt's completion requirements, not file presence alone.
3. Classify it as absent, complete, or blocked/incomplete. Preserve the prompt's own statuses and reasons.

Stop on blocked, partial, invalid, or conflicting artifacts unless their authority explicitly permits continuation.
Do not treat unresolved findings as an incomplete artifact when the owning prompt permits them.
If downstream artifacts exist but a required upstream artifact is missing, report the inconsistency instead of regenerating the missing step.

### 2. Select one target

An explicit step request takes precedence over automatic routing but never bypasses prerequisites or approval.
For an explicit implementation request, target Step 4 after Step 3A and scope approval; a Step 3B report is not required.
For an explicit review request, target Step 5 using the exact implementation record.
Confirm before rerunning a step whose authoritative output already exists.

For automatic routing, apply the following rows from top to bottom within the selected run and implementation scope.
An absent next output is eligible only when its actual required prerequisites are complete.

| Validated state                                                                    | Next action                                |
| ---------------------------------------------------------------------------------- | ------------------------------------------ |
| Implementation record exists; its required Step 5 review is absent                 | Resolve Step 5                             |
| Implementation record and its Step 5 review are complete                           | Report remediation complete; stop          |
| Step 1 inventory is absent and no downstream artifact exists                       | Resolve Step 1                             |
| Step 1 is complete; Step 2 findings are absent                                     | Resolve Step 2                             |
| Step 2 is complete; Step 3A plan is absent                                         | Resolve Step 3A                            |
| Step 3A is complete; Step 3B report is absent; no implementation request was made  | Resolve Step 3B                            |
| Step 3A and Step 3B are complete; no implementation request was made               | Report assessment complete; await approval |

Do not start Step 4 merely because a plan or report exists.
Explicit user-supplied implementation selectors can establish an implementation request, but must still satisfy the approval gate.
For status or next-step requests, describe the selected action without executing it or requesting approval to execute it.
If no row applies, report the unresolved state and required input rather than guessing.

### 3. Resolve invocation and approval

1. Read the target wrapper's bound `agent`, input names, defaults, and path bindings.
2. Resolve only that step's required values from the request and validated run artifacts. Ask for missing values in one focused interaction.
3. Validate all prerequisites declared by the authoritative prompt. Step numbering alone does not create a prerequisite.
4. Before Step 4, require explicit approved `priorities`, `waves`, or `changeIds` from the user and apply the plan's approval conditions. All three cannot be empty.
5. Preserve selectors literally. Step 4, not the router, resolves and freezes change IDs according to its authoritative prompt. Use `commitMode=none` unless the user explicitly chooses the supported `per_change` mode.
6. Before Step 5, use `implementationArtifact` exactly as reported by Step 4 and validated against the selected run. Preserve its frozen change IDs; do not reselect scope.
7. Return the resolved invocation. The caller executes, validates the resulting artifact, then asks this skill to resolve again.

## Artifact paths

Resolve locations in this order:

1. Use a concrete path declared by the artifact's authoritative prompt.
2. If the authority makes the path caller-supplied, use the wrapper's Inputs binding with resolved run values.
3. For Steps 4 and 5 agent-authorized output locations, use the exact path reported by the owning agent. On resume, a handoff may locate candidates, but validate the actual artifact, run identity, and scope before using one.

If another step's prompt references a different location for the same input artifact, retain the wrapper's invocation binding, check both declared locations, and report both paths as a divergence.
Do not rename, copy, or choose an unrelated artifact to hide a conflict. Stop if the correct authoritative artifact cannot be established.
For non-path conflicts, apply repository governance precedence; stop when no declared rule resolves the conflict.

## Troubleshooting

* Missing required file: report the exact expected path and stop.
* Multiple matching runs, plans, or implementation records: present candidates and ask the user to select one.
* Handoff disagrees with its artifact: use the authoritative artifact and report the handoff exception.
* Unknown bound agent: report the wrapper's exact `agent` value; do not substitute another agent.
* Missing approval or unresolved plan condition: stop before Step 4 and request the specific decision.
* Incomplete output: report the failed completion requirement; do not advance or automatically overwrite it.

## Response format

Return intent, run identity, target step or stop reason, bound agent, wrapper and authority paths, validated prerequisite paths, expected output location when known, and the resolved slash command.
List unresolved inputs, approval requirements, path divergences, and blockers separately.
Leave no required placeholder unresolved in a runnable command. Optional empty selectors are allowed.
Do not claim execution or completion while routing, create a separate run index, or write assessment artifacts.

> Brought to you by microsoft/hve-core
