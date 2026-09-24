---
name: 01-inventory
description: Create the authoritative single-microservice resiliency inventory
argument-hint: "runDate=YYYY-MM-DD sourceRoot=source/customer-app taskSlug=springboot-active-active-inventory"
agent: Task Researcher
---

# Step 1: Inventory

## Inputs

RUN_DATE=${input:runDate:Assessment run date in YYYY-MM-DD format}
SOURCE_ROOT=${input:sourceRoot:Repository-relative application source root}
TASK_SLUG=${input:taskSlug:Task slug without the -research suffix}

AUTHORITATIVE_PROMPT=prompts/01-create-inventory-hve-task-researcher.prompt.md
ASSESSMENT_SCOPE_CONTEXT=application-context/assessment-scope-context.yml
ASSESSMENT_SCOPE_SCHEMA=grounding/governance/assessment-scope-schema.yml
APPLICATION_ARCHITECTURE_CONTEXT=application-context/application-architecture-context.yml
SOLUTION_ARCHITECTURE_CONTEXT=application-context/solution-architecture-context.yml
DEPENDENCY_STANDARD_REGISTRY=grounding/registry/dependency-standard-registry.yml
PHASE_HANDOFF_SCHEMA=grounding/governance/phase-handoff-schema.yml
EXPECTED_INVENTORY_ARTIFACT=.copilot-tracking/research/${RUN_DATE}/${TASK_SLUG}-research.md
EXPECTED_HANDOFF_ARTIFACT=.copilot-tracking/research/handoffs/01-inventory-summary.yml

## Execution

All paths are workspace-relative. Do not guess alternate artifact paths. If a required artifact does not exist, stop and report the exact missing path. Read the authoritative governed prompt before acting. A handoff summary is non-authoritative and does not replace required artifacts.

Use the Task Researcher agent behavior defined by `AUTHORITATIVE_PROMPT`. This prompt binds that agent through its `agent` frontmatter field. Before any other action, read `AUTHORITATIVE_PROMPT` in full and treat it as the governing specification for this phase; it overrides conflicting default agent behavior. If it cannot be read, stop and report the exact path.

Assess only `SOURCE_ROOT` and the repository artifact domains enabled by `ASSESSMENT_SCOPE_CONTEXT`. Validate the scope context against `ASSESSMENT_SCOPE_SCHEMA`. Load optional application and solution architecture context only when the files exist. Treat application context as the primary architecture authority for this single-microservice repository.

Create the authoritative inventory using `TASK_SLUG`. Record enabled and disabled domains, assessment-domain standards to load, testing-output settings, priority-filter settings, architecture-context provenance, Kafka scenario resolution, upstream and downstream relationships, and unresolved evidence.

Do not generate findings, recommendations, severity, priority, compliance status, readiness scores, or implementation plans.

Create the compact Step 1 handoff at `EXPECTED_HANDOFF_ARTIFACT` when permitted by agent write boundaries. Report the exact inventory and handoff paths. Verify the inventory was written to `EXPECTED_INVENTORY_ARTIFACT`; if the HVE runtime chooses a different actual path, report that exact path and do not fabricate conformance.

## Next phase

End the response with the exact next command, substituting resolved values:

`/02-findings runDate=${RUN_DATE} taskSlug=${TASK_SLUG}`

Step 2 runs as `Task Reviewer` in a new conversation. Do not continue into Step 2 from this conversation.

## Repository-agnostic snapshot rule

Capture an assessment snapshot classification. Git revision is optional; workspace snapshots, uploaded archives, source drops, and unknown-with-limitations are supported.


## Resiliency and non-resiliency finding classification contract
Use `grounding/governance/resiliency-finding-qualification-policy.yml` version 1.1.0. Preserve every evidence-backed applicable control violation as either `resiliency` or `non_resiliency`. Do not suppress a valid non-resiliency finding merely because it fails the resiliency gate. Resiliency classification requires a credible failure scenario, approved resiliency domain, target-architecture element, causal mechanism, and material impact. Preserve classification and rationale across phase artifacts. Business-logic risk remains a separate implementation-approval dimension.
