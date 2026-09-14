---
name: resiliency-assessment
description: 'Orchestrates HVE Core agents through governed resiliency assessment and remediation. Use to start, resume, or check an assessment - Brought to you by microsoft/hve-core'
user-invocable: true
compatibility: 'Requires the HVE Core agents declared by the workspace wrapper prompts'
---

# Resiliency Assessment Orchestration Skill

## Overview

Route the governed resiliency assessment to the HVE agent bound by each workspace wrapper prompt.

This skill performs orchestration only. It does not perform assessment work, define assessment behavior, duplicate prompt requirements, execute slash commands, or change the active chat agent.

## Sources of truth

Read and apply these sources directly. Do not reproduce their substantive rules in this skill or rely on memory of their contents.

1. `.github/copilot-instructions.md` governs the cross-phase authority model, assessment boundary, evidence rules, approval requirements, and completion behavior.
2. The target step's file under `prompts/` is the authoritative specification for that step's inputs, outputs, boundaries, validation, handoff, and completion criteria.
3. The matching file under `.github/prompts/` is the invocation wrapper. Use it for the slash-command name and bound HVE agent from its frontmatter, and for invocation input names and declared artifact paths from its Inputs section. Use its declared paths only as described in Artifact path resolution.
4. `.github/agents/resiliency-assessment.agent.md` is the workspace entry-point agent that delegates step resolution to this skill. Use it only for the handoff labels and bound agents it declares. When it implies a workflow gate that `.github/copilot-instructions.md` does not require, apply `.github/copilot-instructions.md` and report the divergence.
5. Authoritative artifacts produced by completed steps are the source of truth for run state. Phase handoffs provide orientation only and never replace an authoritative artifact.

When sources conflict, follow the precedence rules in `.github/copilot-instructions.md` and the Artifact path resolution order below. Do not resolve any other conflict by inventing a value or by adding a new workflow rule.

Verify `.github/copilot-instructions.md` exists before routing. Verify a step's wrapper and authoritative prompt exist at the paths in Step map once that step is resolved as the target.

## Quick start

For a new assessment, read the Step 1 authoritative prompt in full and the wrapper's invocation metadata, collect only the inputs they require, and present the fully resolved Step 1 slash command.

For a resumed assessment, follow Required procedure to resolve the target step from authoritative artifacts, then present only that step's fully resolved slash command.

## Step map

Each entry pairs an invocation wrapper with its authoritative specification.

1. Step 1
   * Wrapper: `.github/prompts/01-inventory.prompt.md`
   * Authority: `prompts/01-create-inventory-hve-task-researcher.prompt.md`
2. Step 2
   * Wrapper: `.github/prompts/02-findings.prompt.md`
   * Authority: `prompts/02-generate-findings-from-hve-research.prompt.md`
3. Step 3A
   * Wrapper: `.github/prompts/03a-plan.prompt.md`
   * Authority: `prompts/03A-create-authoritative-remediation-plan.prompt.md`
4. Step 3B
   * Wrapper: `.github/prompts/03b-report.prompt.md`
   * Authority: `prompts/03B-create-code-level-resiliency-assessment-report-schema-governed.prompt.md`
5. Step 4
   * Wrapper: `.github/prompts/04-implement.prompt.md`
   * Authority: `prompts/04-implement-approved-remediation-complete-priority-aware.prompt.md`
6. Step 5
   * Wrapper: `.github/prompts/05-review.prompt.md`
   * Authority: `prompts/05-review-implemented-remediation-complete-priority-aware.prompt.md`

## Artifact path resolution

A step's authoritative prompt does not always declare a concrete output path. Resolve the location of an artifact in this order:

1. When the step's authoritative prompt declares a concrete path, use it.
2. When the authoritative prompt declares the path as caller-supplied, such as `PLAN_ARTIFACT=<exact authoritative Step 3A output artifact path>`, use the path declared in that step's wrapper Inputs section.
3. When the wrapper and another step's authoritative prompt declare different paths for the same artifact, use the wrapper path for invocation, check both locations when validating, and report both exact paths as a divergence.

This order locates artifacts only. It never changes an artifact's role, required structure, validation, or completion criteria, which remain governed by the authoritative prompt.

Some declared paths are not run-scoped, including handoff summaries and the Step 3B report default. Never infer run identity, run date, task slug, or plan slug from a non-run-scoped path. Resolve run identity from run-scoped artifact folders or from the user.

## Required procedure

### Stage A: Load governance

Read `.github/copilot-instructions.md` in full. Preserve its phase boundaries and authority model.

### Stage B: Establish run intent

Determine whether the user is starting a new assessment, resuming one, checking status, asking what comes next, or requesting a specific step.

When intent or run identity is ambiguous, inspect existing run-scoped `.copilot-tracking/` phase artifacts and present the matching runs for the user to choose from. Do not assume the current date, select among multiple runs, or invent a task slug, plan slug, artifact path, approval, or selector.

### Stage C: Resolve the target step

When the user explicitly requests a specific step, treat that step as the target, including a step whose output already exists. Confirm before routing a re-run that would overwrite an existing authoritative artifact.

Otherwise evaluate steps in workflow order and take the earliest step whose output is not complete as the target.

For each candidate step:

1. Read its authoritative prompt in full.
2. Locate its output using Artifact path resolution.
3. Use only that prompt's declared artifact role, required structure, handoff rules, and completion validation to validate the output.
4. Treat a missing, partial, blocked, invalid, or nonconforming output exactly as that prompt instructs.

Validate prerequisites from the inputs the target step's authoritative prompt declares as required, not from step numbering. A step whose output the target step does not require is not a prerequisite. Apply a workflow gate only when `.github/copilot-instructions.md` or the target step's authoritative prompt declares it.

Use handoff summaries only as indexes to candidate authoritative artifacts. Validate completion from the authoritative artifact and that step's prompt, not from a handoff summary or file presence alone.

### Stage D: Resolve invocation

Read the target step's wrapper frontmatter and Inputs section. Derive only the invocation metadata from that file:

* Slash-command name
* Bound HVE agent
* Input names and casing
* Required and optional inputs
* Default values explicitly declared by the wrapper
* Declared artifact paths, used only as described in Artifact path resolution

When VS Code reports the bound agent unavailable, stop and report the exact agent name without selecting a substitute.

Resolve phase transitions and handoff behavior only from `.github/copilot-instructions.md` and the authoritative prompt. Resolve input values from the user's request and validated authoritative artifacts. Ask for missing required values. Do not create defaults, normalize values, or reinterpret selectors unless the wrapper or authoritative prompt explicitly instructs it.

### Stage E: Present one handoff

Present only the target step's resolved slash command and its bound HVE agent. Instruct the user to run it in a new conversation when the authoritative prompt requires a new session.

Do not execute the command, invoke the bound HVE agent as a subagent, continue into the next step, or claim the step completed.

## Approval gate

Before routing Step 4, apply the approval requirements from `.github/copilot-instructions.md`, the Step 3A authoritative artifact, and the Step 4 authoritative prompt. Never infer approval or implementation scope. Stop and ask the user for any approval input required by those sources.

## Failure handling

* If a required wrapper, authoritative prompt, governing file, schema, or artifact is missing, report its exact expected path from the source that requires it.
* If an artifact conflicts with a handoff summary, use the authoritative artifact and report the handoff exception as required by `.github/copilot-instructions.md`.
* If a wrapper and an authoritative prompt declare different paths for the same artifact, apply Artifact path resolution and report the divergence. Do not edit either prompt.
* If authoritative sources conflict on anything other than an artifact path, apply their declared precedence and conflict behavior. When no rule resolves the conflict, stop and report it without choosing a value.
* If the current step or run cannot be identified uniquely, present the supported candidates and ask the user to choose.
* If VS Code cannot resolve the wrapper's bound HVE agent, report the exact `agent` value and stop without substituting another agent.

## Boundaries

This skill adds no assessment, evidence, architecture, scenario, priority, implementation, report, testing, or closure rules. Apply those boundaries only from `.github/copilot-instructions.md`, the current authoritative prompt, its referenced governance files, and validated authoritative artifacts.

Do not create a separate run index, assessment artifact, finding, plan, report, implementation record, review record, or handoff summary while routing.

Do not support unattended execution across steps. Preserve the conversation and approval boundaries required by the authoritative sources.

## Response format

For a resolved step, report:

* Target step
* Bound HVE agent read from wrapper frontmatter
* Validated prerequisite artifact paths required by the target step's authoritative prompt
* Exact slash command with all required values resolved
* Any unresolved required input, path divergence, or source conflict that affects routing

Do not summarize the target step's authoritative prompt's substantive instructions unless the user asks. The slash command and source paths are the handoff.
