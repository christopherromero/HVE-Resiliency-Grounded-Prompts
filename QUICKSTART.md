---
title: Quickstart
description: How to run a governed resiliency assessment from start to finish.
---

## Set up the workspace

Run `tools/New-AssessmentWorkspace.ps1` from a framework clone. It prompts for the microservice path and the destination folder, pulls the latest framework content from the requested branch, creates the tracking scaffolding, and copies the microservice code into `source/`.

```powershell
# Prompts for the microservice path and the destination parent folder
pwsh ./tools/New-AssessmentWorkspace.ps1

# Fully specified, pulling the framework from the main branch
pwsh ./tools/New-AssessmentWorkspace.ps1 `
  -MicroservicePath C:\src\ocsp-subscriptionservice `
  -DestinationRoot "C:\Phase 2\phase2-repos\OCSP\Assessments" `
  -Branch main
```

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

Open the new assessment folder in VS Code as the workspace root, then run the assessment.

## Run it

1. Put the application under `source/`, if the setup script did not already do it.
2. Open Chat and pick **Resiliency Assessment** from the agent dropdown.
3. Send:

   ```text
   Start a new assessment
   ```

4. Confirm the values it resolves, then let Steps 1 through 3B run.
5. Reply with the scope you approve, for example `priorities=P0,P1`.
6. Steps 4 and 5 apply the fixes and verify them.

## The steps

| Step | Agent            | Produces                             |
|------|------------------|--------------------------------------|
| 1    | Task Researcher  | Inventory of what the code does      |
| 2    | Task Reviewer    | Findings against the standards       |
| 3A   | Task Planner     | Remediation plan you approve         |
| 3B   | Task Planner     | Readable assessment report           |
| 4    | Task Implementor | Approved code changes                |
| 5    | Task Reviewer    | Verification that findings closed    |

Steps 1 through 3B never touch source code. Step 4 runs only after you approve scope.

## Values

Everything is derived unless you override it.

| Value         | Default                            |
|---------------|------------------------------------|
| `runDate`     | Today, or the existing run's date   |
| `sourceRoot`  | The single folder under `source/`   |
| `taskSlug`    | The source root folder name         |
| `planSlug`    | Task slug plus `-remediation-plan`  |

Slugs are filename prefixes only. The date folder separates runs.

## Where output lands

```text
.copilot-tracking/
├── research/<runDate>/<taskSlug>-research.md              Step 1
├── reviews/<runDate>/<taskSlug>-research-review.md        Step 2
├── plans/<runDate>/<planSlug>.instructions.md             Step 3A
└── changes/                                               Step 4
```

## Running one step at a time

Each command runs under its own agent. Use a fresh chat for each.

```text
/01-inventory runDate=2026-09-15 sourceRoot=source/customer-app taskSlug=customer-app
/02-findings runDate=2026-09-15 taskSlug=customer-app
/03a-plan runDate=2026-09-15 taskSlug=customer-app planSlug=customer-app-remediation-plan
/03b-report runDate=2026-09-15 taskSlug=customer-app planSlug=customer-app-remediation-plan
/04-implement runDate=2026-09-15 taskSlug=customer-app planSlug=customer-app-remediation-plan priorities=P0,P1 waves= changeIds= commitMode=none
/05-review runDate=2026-09-15 taskSlug=customer-app planSlug=customer-app-remediation-plan implementationArtifact=<path Step 4 reported>
```

## Checking where you are

```text
/resiliency-assessment
```

Reads what is on disk and reports the next step.

## When it stops

It stops rather than guessing. A missing artifact, an unresolved input, or the approval gate all end the run and report the exact path or value needed. Supply it and continue.
