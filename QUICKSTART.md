---
title: Quickstart
description: How to run a governed resiliency assessment from start to finish.
---

# Contents

- [Setup](#setup)
  - [1. Create Assessment Workspace via Powershell](#1-create-assessment-workspace-via-powershell)
  - [2. Update Application Context](#2-update-application-context)
    - [Assessment scope](#assessment-scope)
    - [Optional: Populate context with Chat](#optional-populate-context-with-chat)
- [Running Agent and Create Assessment](#running-agent-and-create-assessment)
  - [Agent Orchestration](#agent-orchestration)
  - [Manual Run](#manual-run)
    - [Running one step at a time](#running-one-step-at-a-time)
- [Cleanup Notes](#cleanup-notes)
- [Other Notes](#other-notes)
  - [Values](#values)

# Setup

## 1. Create Assessment Workspace via Powershell

Run `tools/New-AssessmentWorkspace.ps1` from a framework clone. It prompts for the microservice path and the destination folder, pulls the latest framework content from the requested branch, creates the tracking scaffolding, and copies the microservice code into `source/`.

```powershell
# Prompts for the microservice path and the destination parent folder
pwsh ./tools/New-AssessmentWorkspace.ps1

# Fully specified, pulling the framework from the main branch
# Replace both placeholders with paths on your own machine
$microservicePath = '<path to the microservice repository you are assessing>'
$assessmentsRoot = '<parent folder that holds your assessment workspaces>'

pwsh ./tools/New-AssessmentWorkspace.ps1 `
  -MicroservicePath $microservicePath `
  -DestinationRoot $assessmentsRoot `
  -Branch main
```

Neither path is fixed by the framework. `$microservicePath` points at the code you want assessed, `$assessmentsRoot` is any folder you can write to, and the script creates `$assessmentsRoot\<AssessmentName>` under it. Keep the quotes so paths containing spaces work.

Useful switches:

| Switch | Effect |
|--------|--------|
| `-AssessmentName` | Names the new folder, defaults to the microservice folder name |
| `-Branch` | Framework branch to pull, defaults to `feature/refined-context-and-schema` |
| `-UseLocalFramework` | Copies from the local clone instead of cloning from GitHub |
| `-SourceSubfolder customer-app` | Nests the code under `source/customer-app` |
| `-IncludeSourceGitFolder` | Keeps the microservice `.git` folder |
| `-ExcludeFromSource` | Overrides the excluded build folders, defaults to `.git`, `target`, `node_modules`, `.gradle`, `.idea`, `bin`, `obj` |
| `-Force` | Writes into an existing, non-empty assessment folder |


## 2. Update Application Context

After the code lands under `source/`, update these three files before you run anything else. They carry template values from the framework and the assessment reads them as approved context.

| File | Adjust |
|------|--------|
| [application-context/application-architecture-context.yml](./application-context/application-architecture-context.yml) | Metadata, runtime expectations, Kafka operating scenario, authoritative state, upstream and downstream dependencies, external side effects, approved architecture decisions |
| [application-context/assessment-context.md](./application-context/assessment-context.md) | Application name, language, framework, runtime, assessment goal |
| [application-context/assessment-scope-context.yml](./application-context/assessment-scope-context.yml) | Report preferences only, leave the scope settings as shipped, see [Assessment scope](#assessment-scope) |

Starting an assessment against the shipped template values produces findings for the wrong application.

### Assessment scope

In `application-context/assessment-scope-context.yml`, the only settings in assessment_scope that should be enabled are `application_code` and `application_configuration`. 

```yaml
assessment_scope:
  application_code: {status: enabled}
  application_configuration: {status: enabled}
  container_build: {status: disabled}
  cicd_pipeline: {status: disabled}
  deployment_configuration: {status: disabled}
  infrastructure_as_code: {status: disabled}
  deployed_infrastructure: {status: disabled}
```

Do not enable `container_build`, `cicd_pipeline`, `deployment_configuration`, `infrastructure_as_code`, or `deployed_infrastructure` for our current scenario.

### Optional: Populate context with Chat

```text
Let's populate this context based on what we see in the source/ folder. There might be multiple projects in the source/ folder. 

Use GPT-6.1 Sol and keep my existing permissions.

We are targeting a westus2 westus active-active deployment

Again, we are only running the app code and config scopes
```

# Running Agent and Create Assessment

## Agent Orchestration

1. Put the application under `source/`, if the setup script did not already do it.
2. Update the three context files described above.
3. Open Chat and pick **Resiliency Assessment** from the agent dropdown.
4. Send:

   ```text
   Start a new assessment
   ```

5. Review the resolved run values, then let Steps 1 through 3B run. Each step uses its bound HVE agent in a separate subagent context and validates its output before the next step starts.
6. The orchestrator stops after the report. Review the Step 3A plan and reply with the scope you approve, for example `priorities=P0,P1 commitMode=none`. Approval must satisfy any additional conditions recorded in the plan.
7. Steps 4 and 5 apply only the approved scope and verify it. The default commit mode is `none`; choose `per_change` explicitly if you want local commits.

This GPT branch pins the orchestrator and all four phase-owning HVE agents to `GPT-6.1 Sol (copilot)`, the qualified VS Code model name. The Copilot SDK task tool instead uses the runtime ID `gpt-6.1-sol`; that ID is not a VS Code frontmatter model name.

Delegated steps and their internal subagents must use the same model. If the model is unavailable or the runtime cannot honor the pin, the workflow stops rather than falling back to another model or provider. Reasoning-effort and context-tier overrides remain unset unless explicitly requested; permissions remain unchanged.

Source code may be directly under `source/` (the workspace script's default) or in a nested application folder. The orchestrator asks you to choose when multiple application roots or runs match. You can supply a descriptive `taskSlug` when assessing `source` directly; otherwise it defaults to `source`.

Use `Resume the assessment` to continue an existing run without changing its date, or `Check assessment status` to inspect it without executing steps. Requesting a specific step runs only that step. Existing authoritative outputs require confirmation before a rerun.

You may explicitly request implementation after Step 3A without generating the optional Step 3B report. The same scope approval gate applies. If delegation is unavailable, use handoff mode: copy the fully resolved command supplied by the orchestrator into the named agent in a fresh chat using GPT-6.1 Sol. Handoff buttons contain command names only and do not fill in run values.

## Manual Run

1. Copy-and-paste the prompts located in the `/prompts` folder into the chat.
2. Set the proper HVE Agent:
   - prompt 1 - HVE Task Researcher
   - prompt 2 - HVE Task Reviewer
   - prompt 3a - HVE Task Planner
   - prompt 3b - HVE Task Planner
   - prompt 4 - HVE Task Implementor
   - prompt 5 - HVE Task Reviewer
3. Use GPT-6.1 Sol and keep your existing permissions. The workspace agents use `model: 'GPT-6.1 Sol (copilot)'`; if the UI requires manual selection, select GPT-6.1 Sol before sending.

### Running one step at a time

Each command runs under its own agent. Use a fresh chat for each.

```text
/01-inventory runDate=2026-09-15 sourceRoot=source/customer-app taskSlug=customer-app
/02-findings runDate=2026-09-15 taskSlug=customer-app
/03a-plan runDate=2026-09-15 taskSlug=customer-app planSlug=customer-app-remediation-plan
/03b-report runDate=2026-09-15 taskSlug=customer-app planSlug=customer-app-remediation-plan
/04-implement runDate=2026-09-15 taskSlug=customer-app planSlug=customer-app-remediation-plan priorities=P0,P1 waves= changeIds= commitMode=none
/05-review runDate=2026-09-15 taskSlug=customer-app planSlug=customer-app-remediation-plan implementationArtifact=<path Step 4 reported>
```

| Step | Agent            | Produces                             |
|------|------------------|--------------------------------------|
| 1    | Task Researcher  | Inventory of what the code does      |
| 2    | Task Reviewer    | Findings against the standards       |
| 3A   | Task Planner     | Remediation plan you approve         |
| 3B   | Task Planner     | Readable assessment report           |
| 4    | Task Implementor | Approved code changes                |
| 5    | Task Reviewer    | Verification that findings closed    |

Steps 1 through 3B never touch source code. Step 4 runs only after you approve scope.

# Cleanup Notes

```text
Let's create a new copy of this assessment. The new archival version can have “-initial” at the end of it. 

For the one without initial suffix, let’s edit:

- Repo scope should only be the repo/microservice name, no additional info is needed. 
- Remove metadata, like HTML tags or schema references or F-XXX or AA-XXX findings. These are not relevant to the reader as they won't always have access to the research.
- Remove any references to 'source/' as the assessment had it structured there, but the actual repo does not start at that folder. 
- Remove Appendix A: Traceability. This is again referring to the metadata and research
- Each finding should only have the following sections, and any sections outside of this should be move to another section if applicable. 
**Priority: 
**Resiliency Related:** 
**Issue:** 
**What does this solve:** 
**Resiliency Impact:** 
**Recommended Fix:** 
**File:**
**Fix:**
**Notes**
***MSFT Reference**
- Remove any AI Agent internals or comments on the reporting process. 
```

# Other Notes

## Values

Everything is derived unless you override it.

| Value           | Default                                   |
| --------------- | ----------------------------------------- |
| `runDate`       | Today, or the existing run's date         |
| `sourceRoot`    | `source` or one nested application folder |
| `taskSlug`      | The source root folder name               |
| `planSlug`      | Task slug plus `-remediation-plan`        |

Slugs are filename prefixes only. The date folder separates runs.
