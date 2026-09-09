# Assessment Review Checklist

## Purpose

Use this checklist before closing any assessment phase or advancing to the next phase.

This checklist supplements, but does not replace:

- `.github/copilot-instructions.md`
- Phase-specific prompts
- Governance policies and schemas
- Authoritative phase artifacts
- Phase handoff summaries

The framework assumes one microservice per repository unless Step 1 documents an exception.

---

## Global checks

- [ ] The repository assessment boundary is understood.
- [ ] The repository represents one microservice, or an exception is documented.
- [ ] `application-context/application-architecture-context.yml` was reviewed when present.
- [ ] `application-context/assessment-scope-context.yml` was reviewed when present.
- [ ] Approved solution context was used only when cross-repository information was necessary.
- [ ] Required grounding standards and governance policies were loaded.
- [ ] Repository evidence was used for code and configuration findings.
- [ ] Deployed infrastructure state was not inferred from repository absence.
- [ ] External and unknown ownership were handled as evidence gaps or `not_assessed`.
- [ ] Stable control, finding, evidence, change, policy, and scenario IDs were preserved.
- [ ] The authoritative phase artifact was created.
- [ ] The phase handoff summary was created in an agent-writable directory when permitted.
- [ ] Output paths, unresolved items, and blockers were reported.

---

# Step 1: Inventory

## Repository and application profile

- [ ] Repository root and assessed revision were recorded.
- [ ] Application name, business role, language, framework, and runtime were recorded.
- [ ] Build files and module structure were inventoried.
- [ ] Application source and configuration were inventoried.
- [ ] Tests and test frameworks were inventoried.
- [ ] Direct inbound and outbound interactions were inventoried.
- [ ] Upstream and downstream context was recorded separately from repository evidence.
- [ ] External side effects were classified.

## Dependencies and workloads

- [ ] Databases and their production roles were identified.
- [ ] Kafka producers, consumers, Streams topologies, and topic contracts were identified.
- [ ] HTTP, gRPC, Event Hubs, Functions, Key Vault, Redis, and other clients were identified.
- [ ] Scheduled, batch, polling, listener, and background workloads were identified.
- [ ] Authoritative state and supporting state were distinguished.
- [ ] Repository-declared but unused dependencies were distinguished from production use.

## Architecture context

- [ ] Approved application context was loaded when present.
- [ ] Context provenance, version, owner, and approval state were recorded.
- [ ] Repository evidence was not represented as architecture approval.
- [ ] Architecture context was not represented as source-code evidence.
- [ ] Context conflicts were routed to architecture governance review.

## Kafka scenario

- [ ] Kafka applicability was determined from production code.
- [ ] Approved scenario context was used when supplied.
- [ ] Policy inference was clearly labeled when context was absent.
- [ ] Application scenario classification was separated from deployed topology verification.
- [ ] Conditional assumptions and unresolved infrastructure facts were recorded.
- [ ] Database-independent Kafka was not assumed to be stateless or multi-active.

## Optional assessment domains

- [ ] Disabled domains were not inventoried beyond what was required to establish scope.
- [ ] `container_build` artifacts were inventoried only when enabled.
- [ ] `cicd_pipeline` artifacts were inventoried only when enabled.
- [ ] `deployment_configuration` artifacts were inventoried only when enabled.
- [ ] IaC behavior matched `disabled`, `inventory_only`, or `findings_enabled`.
- [ ] Repository ownership was recorded for optional-domain artifacts.
- [ ] Assessment-domain standards to load were resolved without duplicating umbrella standards.

## Step 1 completion

- [ ] The authoritative inventory artifact was generated.
- [ ] Dependency and assessment-domain standards to load were recorded.
- [ ] Inventory exceptions and unresolved endpoint aliases were recorded.
- [ ] The inventory handoff summary was generated under `.copilot-tracking/research/handoffs/` when permitted.

---

# Step 2: Assessment and Findings

## Control evaluation

- [ ] Every evaluated control came from an applicable loaded standard.
- [ ] Disabled-domain controls were marked `not_applicable`.
- [ ] External or unknown ownership was marked `not_assessed` when appropriate.
- [ ] Missing external evidence was not converted into noncompliance.
- [ ] Controls were evaluated against effective behavior, not keyword presence alone.

## Finding quality

- [ ] Every finding maps to a valid primary control.
- [ ] Related controls are cross-referenced without duplicating the root cause.
- [ ] Finding title, issue, risk, category, severity, status, and resiliency relationship are clear.
- [ ] Verified and conditional findings are distinguished.
- [ ] Conditional findings identify assumptions and required external evidence.
- [ ] Infrastructure and PCF findings were not created outside approved scope.
- [ ] Priority was not assigned or recalculated in Step 2.

## Source evidence

- [ ] Every applicable finding has repository-relative evidence paths.
- [ ] Symbols, properties, configuration keys, or build elements were recorded.
- [ ] Original assessed line ranges were recorded or explicitly unavailable.
- [ ] Original excerpts match the assessed repository revision.
- [ ] Exact formatting and comments were preserved.
- [ ] Sensitive values were redacted without removing required evidence.
- [ ] Illustrative code was not placed in original-source evidence.

## Optional domains

- [ ] CI/CD findings came only from repository-owned pipeline evidence.
- [ ] Container-build findings came only from enabled, repository-owned build definitions.
- [ ] Deployment findings came only from enabled, repository-owned manifests, charts, overlays, or scripts.
- [ ] IaC findings were emitted only when `findings_enabled`.
- [ ] Cross-standard findings were deduplicated by root cause.

## Step 2 completion

- [ ] The authoritative review artifact was generated.
- [ ] Finding and control counts reconcile.
- [ ] Source-evidence coverage counts reconcile.
- [ ] Architecture and evidence follow-ups were recorded.
- [ ] The assessment handoff summary was generated under `.copilot-tracking/reviews/handoffs/` when permitted.

---

# Step 3A: Remediation Planning

## Governance and priority

- [ ] Every planned change maps to one or more approved Step 2 findings.
- [ ] Priority was assigned only through the remediation-prioritization policy.
- [ ] Policy ID, version, and selected rule ID were recorded.
- [ ] The highest applicable priority rule was selected.
- [ ] Missing governance coverage resulted in a governance-blocked item, not an invented priority.
- [ ] Change IDs are unique and stable.
- [ ] Implementation waves and dependencies are explicit.

## Original source preservation

- [ ] Step 2 evidence IDs, paths, symbols, revisions, line ranges, and excerpts were preserved exactly.
- [ ] Missing evidence remains explicitly unavailable.
- [ ] Original and proposed implementations remain separate.

## Illustrative implementation

- [ ] The highest-confidence implementation was generated for every evidence-supported target.
- [ ] Remediations were divided into independently expressible targets.
- [ ] One unresolved adapter or architecture choice did not suppress all illustrative code.
- [ ] Generated proposals contain real code or configuration syntax, not narrative instructions.
- [ ] Technology-neutral interfaces, contracts, configuration structures, and tests were generated when supportable.
- [ ] Only specifically blocked targets use `targeted_discovery_required`.
- [ ] Each targeted-discovery record identifies the exact blocker and unresolved inputs.
- [ ] Multi-file changes generate proposals for every unblocked target.
- [ ] Narrative-only generated proposals equal zero.

## Testing and validation

- [ ] Acceptance criteria are specific and measurable.
- [ ] Validation requirements cover success, failure, recovery, duplicate, and rollback behavior as applicable.
- [ ] Test commands are repository-native and correctly scoped.
- [ ] Unknown numeric values remain configurable.
- [ ] Optional delivery changes include appropriate syntax, render, lint, and policy checks.

## Step 3A completion

- [ ] The authoritative remediation plan was generated.
- [ ] Priority and wave indexes reconcile to change objects.
- [ ] Illustrative-code coverage is complete or valid targeted discovery is recorded.
- [ ] The planning handoff summary was generated under `.copilot-tracking/plans/handoffs/` when permitted.

---

# Step 3B: Assessment Reporting

## Authority and scope

- [ ] The report used Step 2 as finding authority.
- [ ] The report used Step 3A as priority, change, roadmap, and illustrative-code authority.
- [ ] The report did not create, remove, reclassify, or reprioritize findings.
- [ ] The report schema ID and version are correct.
- [ ] Assessment scope and context provenance are disclosed.

## Priority filtering

- [ ] Finding-selection mode was loaded from assessment scope.
- [ ] Included priorities match configuration.
- [ ] Omitted priorities are disclosed.
- [ ] Findings and changes were not renumbered.
- [ ] Priorities were not recalculated.
- [ ] Filtered summary, detailed sections, matrix, and roadmap reconcile.
- [ ] Cross-references to omitted findings remain identifiable.
- [ ] The report identifies authoritative full assessment and plan paths.

## Testing output

- [ ] Testing-output mode was applied exactly.
- [ ] Test findings were included or omitted according to configuration.
- [ ] Hidden testing details remain authoritative in Step 3A.
- [ ] Test code, commands, acceptance criteria, and evidence follow their display settings.
- [ ] A consolidated Validation Strategy is present when required.
- [ ] Report preferences did not alter findings, priorities, implementation scope, or review obligations.

## Finding rendering

- [ ] Findings are grouped by selected priority and meaningful category.
- [ ] Category headings are visually distinct from finding headings.
- [ ] Target file, symbol, original assessed lines, evidence ID, and change ID are shown where applicable.
- [ ] Original source is rendered exactly from Step 2.
- [ ] Generated illustrative code is rendered exactly from Step 3A.
- [ ] Narrative guidance is not rendered as code.
- [ ] Mixed generated and targeted-discovery proposals are rendered per target.
- [ ] Targeted-discovery reasons and unresolved inputs are clear.

## Step 3B completion

- [ ] The report artifact was generated at the authorized path.
- [ ] Full Finding Matrix and roadmap reconcile to the report scope.
- [ ] Schema and illustrative-code conformance passed.
- [ ] The report handoff summary was generated under `.copilot-tracking/plans/handoffs/` when permitted.

---

# Step 4: Implementation

## Frozen scope

- [ ] Implementation selectors were resolved against Step 3A.
- [ ] The resolved change-ID set was frozen before editing.
- [ ] Only approved priorities, waves, or change IDs were included.
- [ ] The assessment report was not used as implementation authority.
- [ ] Scope fingerprint and requested selectors were recorded.

## Repository changes

- [ ] Every changed file maps to an approved change ID.
- [ ] Current repository state was inspected before editing.
- [ ] Final implementation follows the approved intent and acceptance criteria.
- [ ] Approved architecture and Kafka scenario were preserved.
- [ ] No unapproved database, topology, ownership, security, or product decision was introduced.
- [ ] Optional delivery artifacts were changed only when their domain and artifact class were approved.
- [ ] No live deployment or external repository modification was performed.

## Validation

- [ ] Build or compile validation was run when applicable.
- [ ] Unit, integration, and resiliency tests were run as required.
- [ ] Container-build validation was run when applicable.
- [ ] Pipeline syntax and gate validation was run when applicable.
- [ ] Helm or Kustomize rendering was validated when applicable.
- [ ] Kubernetes manifest validation was run when applicable.
- [ ] IaC validation was run only for approved repository-owned changes.
- [ ] Passed, failed, blocked, and not-run validation results were recorded accurately.

## Step 4 completion

- [ ] The authoritative implementation record was generated.
- [ ] Files changed, deviations, blockers, and scope violations were recorded.
- [ ] The implementation handoff summary was generated under `.copilot-tracking/changes/handoffs/` when permitted.

---

# Step 5: Post-Implementation Review

## Scope integrity

- [ ] Review scope matches the frozen Step 4 scope.
- [ ] Selectors were not recalculated.
- [ ] Every implemented change ID was reviewed.
- [ ] Out-of-scope changes were identified as scope violations.

## Closure evidence

- [ ] Step 2 findings were used as the original finding authority.
- [ ] Step 3A acceptance and validation requirements were used.
- [ ] Step 4 implementation records and repository evidence were reviewed.
- [ ] Closure is supported by repository evidence and required validation.
- [ ] Partial remediation, open risk, and validation blockers are explicit.
- [ ] Regressions and newly introduced risks are documented.

## Independence from report presentation

- [ ] Review conclusions were not based on report formatting.
- [ ] Priority filtering did not exclude changes from review.
- [ ] Hidden testing output did not reduce closure evidence.
- [ ] Omitted report priorities did not alter finding dispositions.

## Step 5 completion

- [ ] The authoritative post-implementation review was generated.
- [ ] Finding and change dispositions reconcile.
- [ ] Follow-up items and governance exceptions are recorded.
- [ ] The review handoff summary was generated under `.copilot-tracking/reviews/handoffs/` when permitted.

---

# Final Reproducibility Check

Before declaring the workflow complete, verify:

- [ ] A new chat can reconstruct each phase from authoritative artifacts alone.
- [ ] Inventory, findings, evidence, priorities, changes, implementation, and review IDs reconcile.
- [ ] Architecture context and policy decisions remain traceable.
- [ ] Assessment-scope decisions remain traceable.
- [ ] Filtered report output can be reproduced from Step 2, Step 3A, and the scope context.
- [ ] Testing-output behavior can be reproduced from the scope context.
- [ ] Handoff summaries reconcile to authoritative artifacts.
- [ ] Open items, accepted risks, unresolved evidence, and governance blocks are documented.
- [ ] No phase depends on hidden conversation history.

---

# Stop Conditions

Do not advance to the next phase when:

- [ ] The required authoritative artifact is missing or incomplete.
- [ ] Source evidence has been invented, rewritten, or cannot be traced.
- [ ] Architecture context conflicts are unresolved and affect scenario applicability.
- [ ] Priority governance is missing for a change intended for implementation.
- [ ] Step 3A contains narrative-only generated proposals where code is required.
- [ ] Step 3B conformance fails.
- [ ] Step 4 scope is not frozen.
- [ ] Required validation is failed or unaccounted for.
- [ ] Step 5 lacks sufficient evidence for closure.
