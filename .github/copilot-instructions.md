# Resiliency Assessment Framework Instructions

## Framework purpose

This repository uses a governed assessment framework to evaluate application resiliency, availability, recovery behavior, operational readiness, and approved repository-owned delivery artifacts.

The default repository model is:

```text
One repository
    ↓
One microservice
```

The current repository is the primary assessment boundary unless authoritative repository evidence explicitly demonstrates otherwise.

## Global operating principles

1. Use an artifact-driven workflow.
2. Treat authoritative phase artifacts as the source of truth.
3. Do not require conversation history to continue the workflow.
4. Expect `/clear` or a new chat between phases.
5. Do not silently cross phase boundaries.
6. Preserve stable control, finding, evidence, change, policy, scenario, and validation identifiers.
7. Never invent missing source evidence, architecture facts, deployment state, test results, or approvals.
8. Use phase handoff summaries for orientation only. Handoffs never replace authoritative artifacts.

## Repository model and assessment boundary

Assume one microservice per repository.

Assess only the current repository and the artifact classes explicitly enabled by assessment scope.

Do not assume:

- Multi-repository ownership
- Solution-wide implementation behavior
- Transitive dependencies not declared by approved context
- Deployed infrastructure state
- Runtime health or operational readiness
- External pipeline, platform, or shared-service configuration

When the repository contains multiple deployable services or modules, record the exception in Step 1 and identify the actual assessment boundary before generating findings.

## Architecture authority

The primary architecture context is:

```text
application-context/application-architecture-context.yml
```

Use it for approved architecture intent, including:

- Application name and business role
- Deployment operating model
- Kafka operating scenario
- Authoritative state
- Regional processing model
- Upstream dependencies
- Downstream dependencies
- External side effects
- Approved architecture decisions

Repository evidence remains authoritative for implemented code and configuration.

Architecture context does not prove that infrastructure is deployed or operating as declared.

## Architecture-context precedence

Use architecture inputs in this order:

1. Approved `application-architecture-context.yml`
2. Repository-observed implementation evidence
3. Approved `solution-architecture-context.yml`, when supplied
4. Governed policy inference
5. Unresolved

Do not silently resolve conflicts between approved context and repository evidence.

Route conflicts to architecture governance review and mark affected scenario-specific evaluation `not_assessed` until resolved.

## Optional solution context

The following file is optional:

```text
application-context/solution-architecture-context.yml
```

Use it only when needed for:

- Cross-repository processing chains
- Transitive authoritative state
- Shared workload ownership
- Solution-wide Kafka scenario declarations
- Enterprise architecture decisions

Do not require solution context for a normal single-microservice repository assessment.

## Assessment workflow

The governed workflow is:

```text
Step 1: Inventory
Step 2: Assessment
Step 3A: Remediation planning
Step 3B: Assessment reporting
Step 4: Implementation
Step 5: Post-implementation review
```

Run one phase per conversation. Use `/clear` or start a new chat between phases.

Each phase must read the required authoritative artifacts rather than rely on prior conversation history.

## Authority model

- **Step 1** is the inventory authority.
- **Step 2** is the finding and source-evidence authority.
- **Step 3A** is the remediation priority, change, wave, validation, and implementation-plan authority.
- **Step 3B** is the presentation authority.
- **Step 4** is the implementation-record authority.
- **Step 5** is the post-implementation-review authority.

Step 3B must not alter findings or implementation scope.

Step 4 follows Step 3A, not the assessment report.

## Repository evidence rules

Create findings only from evidence supported by the active assessment scope, such as:

- Application source code
- Application configuration
- Tests
- Build files
- Repository-owned Dockerfiles
- Repository-owned CI/CD definitions
- Repository-owned Helm charts
- Repository-owned Kustomize overlays
- Repository-owned Kubernetes manifests
- Repository-owned deployment scripts
- Repository-owned infrastructure as code when explicitly enabled

Every source or configuration finding should preserve, when available:

- Repository-relative path
- Symbol, property, configuration key, or build element
- Original assessed line range
- Exact original source excerpt
- Assessed repository revision
- Evidence identifier

Do not rewrite or normalize original source evidence.

Redact protected values while preserving the surrounding evidence required to demonstrate the finding.

## Assessment scope

Read this optional file:

```text
application-context/assessment-scope-context.yml
```

Validate it against:

```text
grounding/governance/assessment-scope-schema.yml
```

If the context is absent, use these governed defaults:

```yaml
application_code:
  status: enabled

application_configuration:
  status: enabled

container_build:
  status: disabled

cicd_pipeline:
  status: disabled

deployment_configuration:
  status: disabled

infrastructure_as_code:
  status: disabled

deployed_infrastructure:
  status: disabled
```

Only evaluate optional domains that are explicitly enabled.

Assessment scope affects applicability only. It must not weaken evidence requirements or change severity and priority governance.

## Ownership rules

Only confirmed repository-owned artifacts may produce optional CI/CD, container-build, deployment-configuration, or infrastructure-as-code findings.

Use:

```yaml
status: not_assessed
```

when ownership is unknown or external and evaluation requires unavailable evidence.

Use the evidence-gap section for externally owned architecture or deployment facts needed to validate assumptions.

Do not create findings against assets outside the repository assessment boundary.

## Optional delivery assessment

When `container_build` is enabled, evaluate repository-owned container build definitions using the applicable container-build grounding standard.

When `cicd_pipeline` is enabled, evaluate repository-owned GitHub Actions, Azure Pipelines, release workflows, and related scripts using the applicable CI/CD grounding standard.

When `deployment_configuration` is enabled, evaluate repository-owned Kubernetes manifests, Helm charts, Kustomize overlays, and deployment scripts using the applicable deployment grounding standards.

When `infrastructure_as_code` is `inventory_only`, inventory and report evidence boundaries without generating findings.

When `infrastructure_as_code` is `findings_enabled`, generate findings only from repository-owned IaC that directly contradicts an approved application resiliency requirement.

Deployed infrastructure findings remain prohibited.

## Upstream dependencies

Use `upstream_dependencies` from application context to understand who provides requests, data, or events to the microservice.

Examples of upstream roles include:

- Business event source
- Request source
- Data source

Upstream context may establish workflow meaning and impact. It does not prove repository implementation.

Validate direct interaction through repository evidence whenever the assessed microservice is expected to consume or call the upstream component.

## Downstream dependencies

Use `downstream_dependencies` from application context to understand dependent services, event consumers, and external effects.

Examples of downstream roles include:

- Dependent service
- Event consumer
- External side effect

Use downstream context to evaluate dependency criticality, replay safety, idempotency expectations, and failure impact.

Validate direct interaction through repository evidence whenever the assessed microservice is expected to call or publish to the downstream component.

## External side effects

When approved context or repository evidence establishes external side effects, evaluate:

- Stable operation identity
- Idempotency
- Duplicate execution behavior
- Ambiguous outcome handling
- Status lookup or reconciliation
- Replay behavior
- Recovery and compensation

Examples include:

- Email delivery
- SMS delivery
- Payment processing
- Partner API mutation
- Inventory mutation

Do not assume an external side effect succeeded or failed solely from a timeout or connection error.

## Kafka scenario rules

Never assume a stretched Kafka cluster.

Use the approved application-context scenario when supplied and validate it against:

```text
grounding/governance/kafka-operating-scenario-policy.yml
```

Supported scenarios are:

- `active_standby`
- `independent_regional_active_active`
- `database_independent_kafka`
- `unresolved`

Without approved context, policy inference may classify the application scenario provisionally. Inferred scenarios require architecture confirmation and must not be presented as proof of deployed Kafka topology.

Keep these concepts separate:

- Application operating-scenario classification
- Deployed Kafka topology verification

An unresolved infrastructure fact does not automatically make the application scenario unresolved when policy evidence supports provisional assessment.

## Finding rules

A finding requires:

- An applicable control
- Repository-supported evidence
- A specific observed behavior
- A defensible risk statement
- A clear implementation or evidence boundary

Do not create findings from assumptions, missing external infrastructure, or context declarations alone.

Do not duplicate findings when multiple controls identify the same root cause.

Preserve verified, conditional, not-assessed, not-applicable, accepted-risk, and non-finding states separately.

## Priority governance

Assign remediation priority only through:

```text
grounding/governance/remediation-prioritization.md
```

Do not invent a priority rule.

Select the highest applicable governed rule and record the policy ID, policy version, and rule ID.

If no rule applies, mark the change governance-blocked and identify the missing policy coverage.

Priority is authoritative in Step 3A.

## Illustrative implementation

Generate the highest-confidence concrete illustrative implementation supported by authoritative repository evidence.

Do not suppress all illustrative code merely because one adapter, technology choice, product API, or external architecture decision remains unresolved.

For each change:

1. Separate independent implementation targets.
2. Generate code or configuration for every supported target.
3. Mark only the blocked target `targeted_discovery_required`.
4. State the exact unresolved decision and required input.
5. Avoid unapproved architecture, security, persistence, product, and topology decisions.

Generate evidence-supported proposals for:

- Interfaces
- Repository contracts
- Domain models
- Service boundaries
- Focused method bodies
- Configuration-property structures
- Listener and lifecycle configuration
- Stable identity propagation
- Tests and validation structures

Task Planner produces the highest-confidence plan and illustrative proposal.

Task Implementor validates the current repository and applies the final approved repository-specific changes.

## Report generation

Assessment reports are presentation artifacts.

Reports must not change:

- Finding identity
- Finding status
- Severity
- Priority
- Evidence
- Control mapping
- Change mapping
- Implementation scope

The report must identify its governing schema, source artifacts, context, and applied report preferences.

## Priority-filtered reporting

Priority filtering changes presentation only.

When configured, detailed report sections, filtered summary counts, the Full Finding Matrix, and the Implementation Roadmap include only selected priorities.

Do not:

- Renumber findings
- Recalculate priorities
- Reclassify omitted findings
- Imply omitted findings do not exist

Always declare included priorities, omitted priorities, and the authoritative full assessment and plan paths.

## Testing-output preferences

Supported report modes are:

- `full`
- `summary`
- `roadmap_only`
- `hidden`

These settings control report rendering only.

Testing findings, tests, acceptance criteria, validation commands, and closure evidence remain authoritative in their source artifacts even when report detail is reduced or hidden.

Never use report preferences to modify findings, priorities, implementation obligations, or review conclusions.

## Phase handoff summaries

Generate a compact handoff summary at the end of every phase using:

```text
grounding/governance/phase-handoff-schema.yml
```

Store each handoff in an agent-writable subfolder colocated with the phase artifact, such as:

```text
.copilot-tracking/research/handoffs/
.copilot-tracking/reviews/handoffs/
.copilot-tracking/plans/handoffs/
.copilot-tracking/changes/handoffs/
```

Handoffs preserve:

- Artifact paths
- Counts
- Stable identifiers
- Scenario selection
- Context provenance
- Scope settings
- Report preferences
- Unresolved items
- Next-phase input requirements

Handoffs are non-authoritative. If a handoff conflicts with an authoritative artifact, use the authoritative artifact and record a handoff exception.

## Step 4 implementation rules

Step 4 implements only the frozen approved change IDs resolved from Step 3A selectors:

- Approved priorities
- Approved waves
- Approved change IDs

Step 4 never takes implementation direction from the assessment report.

Modify optional delivery artifacts only when:

- Their assessment domain was enabled
- Repository ownership is confirmed
- The file is mapped to an approved change ID
- The plan explicitly authorizes the target artifact class

Do not execute live deployments or modify deployed infrastructure.

## Step 5 review rules

Step 5 validates implementation against:

- Step 2 findings
- Step 3A remediation plan
- Step 4 implementation record

Review must preserve the frozen implementation scope.

Report filtering, formatting, and testing visibility settings do not affect closure decisions.

Do not close a finding without repository evidence and the validation required by the authoritative plan.

## Completion behavior

At the end of every phase:

- Write the authoritative phase artifact.
- Validate phase-specific completion criteria.
- Write the phase handoff summary when permitted.
- Report exact output paths.
- Report unresolved items and blockers.
- Do not claim successful completion when the authoritative phase artifact is incomplete.

## Repository-Agnostic Assessment Snapshots

Do not assume the assessed folder is a Git repository. Supported snapshot types are `git_revision`, `workspace_snapshot`, `uploaded_archive`, `source_drop`, and `unknown`. Git commit SHA is optional and applies only to `git_revision`.

Use source locator authority in this order: repository path, symbol/configuration element, exact excerpt, source fingerprint, assessment snapshot, then advisory line range. Never initialize Git or require a commit solely for assessment traceability.


## Resiliency and non-resiliency finding classification contract
Use `grounding/governance/resiliency-finding-qualification-policy.yml` version 1.0.0. Preserve every evidence-backed applicable control violation as either `resiliency` or `non_resiliency`. Do not suppress a valid non-resiliency finding merely because it fails the resiliency gate. Resiliency classification requires a credible failure scenario, approved resiliency domain, target-architecture element, causal mechanism, and material impact. Preserve classification and rationale across phase artifacts. Business-logic risk remains a separate implementation-approval dimension.
