# Prompt 5: Review Implemented Multi-Region Remediation Changes

## Agent and phase

Run this prompt in a new VS Code Copilot Chat session with HVE `task-reviewer` selected, or invoke the HVE `/rpi-review` skill when that is the review surface available in your installation.

This is a focused post-implementation reconciliation. It validates the frozen Step 4 implementation scope against the original findings, approved plan, changed code, tests, and acceptance criteria.

It does not repeat inventory or the full multi-region assessment.

## Required inputs

Provide exact artifact paths:

```text
INVENTORY_ARTIFACT=.copilot-tracking/research/YYYY-MM-DD/springboot-active-active-inventory-research.md
ORIGINAL_REVIEW_ARTIFACT=<exact Step 2 assessment artifact or output path>
PLAN_ARTIFACT=<exact Step 3 authoritative remediation-plan artifact>
IMPLEMENTATION_ARTIFACT=<exact Step 4 authoritative implementation-record artifact>
```

Optional selectors may be supplied for audit comparison only:

```text
APPROVED_PRIORITIES=P0,P1
APPROVED_WAVES=
APPROVED_CHANGE_IDS=
```

When the implementation artifact contains a valid frozen `implementation_scope`, the reviewer must use its `resolved_change_ids`. User-supplied selectors must not replace, recalculate, broaden, or narrow that scope.

Read:

1. The authoritative Step 1 inventory.
2. The original Step 2 findings and control results.
3. The approved Step 3 remediation plan.
4. The authoritative Step 4 implementation record.
5. Current versions and diffs of files changed for resolved change IDs.
6. Tests and validation evidence associated with resolved change IDs.
7. Grounded controls and acceptance criteria mapped to resolved change IDs.

## Review-scope precedence

Resolve review scope using this order:

1. Frozen `implementation_scope.resolved_change_ids` from the authoritative Step 4 implementation artifact
2. `APPROVED_PRIORITIES`, only when no valid implementation scope exists
3. `APPROVED_WAVES`, only when no valid implementation scope and no priorities exist
4. `APPROVED_CHANGE_IDS`, only when no valid implementation scope, priorities, or waves exist

The Step 4 frozen implementation scope always takes precedence.

In the normal workflow, Step 5 must not recalculate priority-based scope. It must review exactly what Step 4 resolved and attempted to implement.

## Scope-resolution and validation algorithm

Before reviewing code:

1. Read `implementation_scope` from the Step 4 artifact.
2. Validate that `scope_frozen: true`.
3. Validate that `resolved_change_ids` is present and non-empty.
4. Validate that every resolved change ID exists in the Step 3 plan.
5. Compare the Step 4 plan path and policy version with Step 3.
6. Compare `scope_fingerprint` when present.
7. Set the review scope to the Step 4 `resolved_change_ids`.
8. Treat any supplied selectors as audit inputs only.
9. Confirm that the supplied selectors, when present, would not indicate a broader or different approval request than the Step 4 record.
10. Freeze the Step 5 review scope.

If the implementation artifact lacks a valid implementation scope, use the same fallback selector precedence as Step 4:

1. Priorities
2. Waves
3. Change IDs

Record that fallback was used and set `implementation_scope_found: false`.

If the resolved review scope differs from the Step 4 implementation scope, stop the review and report a scope mismatch.

## Required scope validation record

```yaml
scope_validation:
  implementation_scope_found: true
  implementation_scope_frozen: true
  implementation_selection_method: priority
  implementation_requested_priorities:
    - P0
    - P1
  implementation_requested_waves: []
  implementation_requested_change_ids: []
  implementation_resolved_change_ids:
    - CHANGE-AA-001
    - CHANGE-AA-002
  review_resolved_change_ids:
    - CHANGE-AA-001
    - CHANGE-AA-002
  resolved_change_count: 2
  scope_fingerprint_match: true
  review_scope_matches_implementation_scope: true
  selector_recalculation_performed: false
  fallback_scope_resolution_used: false
```

If scope differs:

```yaml
scope_validation:
  review_scope_matches_implementation_scope: false
  review_stopped: true
  reason: "Review scope differs from the frozen Step 4 implementation scope."
```

Do not continue with finding closure when a scope mismatch exists.

## Review boundaries

Review only resolved change IDs.

Do not:

- Re-inventory the repository
- Repeat the full multi-region assessment
- Search for new dependencies
- Recalculate remediation priorities
- Create unrelated findings
- Change original finding severity
- Modify source code
- Review infrastructure or PCF
- Review unapproved or unresolved change IDs except to detect accidental scope expansion

You may inspect:

- Changed files
- Relevant diffs
- Directly related unchanged symbols
- Tests required to validate acceptance criteria
- Build and validation output

If implementation exposes a possible unrelated issue, record it as `follow_up_observation`. Do not convert it into a new finding during this review.

## Review objectives

For every resolved change ID:

1. Verify that changed files match the plan or a documented deviation.
2. Verify that the implementation addresses the mapped original findings.
3. Verify that source code compiles, or record why compilation could not be established.
4. Verify that relevant automated tests exist.
5. Verify that test and build evidence is credible.
6. Verify each acceptance criterion.
7. Verify readiness and liveness semantics.
8. Verify deployment-injected regional endpoints remain free of hardcoded region assumptions.
9. Verify retries and timeouts are bounded and safe.
10. Verify non-idempotent operations are protected from unsafe retries.
11. Verify recovery after dependency restoration when required.
12. Verify no unrelated scope was introduced.
13. Verify supporting files changed outside core production code were necessary for resolved changes.

### Configuration consistency validation

When a remediation introduces, removes, or modifies:

- readiness indicators
- liveness indicators
- startup probes
- actuator health contributors
- health groups
- dependency health checks
- readiness participation requirements
- dependency enablement properties

the reviewer must verify that all supporting configuration required by
the implementation is present and internally consistent.

Examples:

If readiness includes:

```yaml
mongo
```

then verify that the corresponding Mongo health contributor is enabled.

Example:

```yaml
management.health.mongo.enabled=true
```

or an equivalent implementation.

Review validation must confirm:

- readiness groups reference valid health contributors
- required contributors are enabled
- code and configuration describe the same behavior
- no remediation introduced disabled contributors
- no remediation introduced contradictory health settings
- startup, readiness, and liveness semantics remain aligned

If implementation intent and configuration behavior differ:

- do not mark the change fully remediated
- record the finding as partially_closed or open
- document the configuration inconsistency
- identify the affected files and configuration keys

## Required status model

Assign each resolved change one status:

- `validated_remediated`
- `validated_partially_remediated`
- `not_remediated`
- `unable_to_validate`
- `implementation_scope_violation`

Assign each associated original finding one disposition:

- `closed`
- `partially_closed`
- `open`
- `validation_blocked`

A finding may be closed only when:

- Required code or configuration changes are present
- Acceptance criteria are satisfied
- Supporting validation evidence exists
- No unresolved defect prevents the intended behavior

Do not close a finding based only on illustrative planner code or the implementor narrative.

## Evidence hierarchy

Use evidence in this order:

1. Current source diff and changed code
2. Passing automated tests tied to acceptance criteria
3. Build or static-analysis output
4. Step 4 implementation record
5. Step 3 plan assertions

Narrative claims cannot override source or test evidence.

## Required review record

```yaml
review_execution:
  phase: post_implementation_review
  inventory_artifact: "exact path"
  original_review_artifact: "exact path"
  plan_artifact: "exact path"
  implementation_artifact: "exact path"
  reviewer_agent: task-reviewer
  review_scope_source: implementation_artifact
  resolved_change_ids: []
  re_inventory_performed: false
  full_reassessment_performed: false
  priorities_recalculated: false
  new_dependencies_discovered: false
  source_code_modified: false

change_reviews:
  - change_id: CHANGE-AA-001
    status: validated_remediated
    finding_dispositions:
      - finding_id: FINDING-KV-001
        disposition: closed
    control_ids: []
    files_reviewed: []
    acceptance_criteria_results: []
    test_evidence: []
    build_evidence: []
    deviations_reviewed: []
    regressions_detected: []
    scope_violations: []
    unresolved_items: []
    rationale: ""

follow_up_observations: []
```

## Scope-expansion detection

Compare the actual changed files and recorded work with the frozen resolved change IDs.

Record:

```yaml
scope_expansion_review:
  changed_files_outside_resolved_scope: []
  unapproved_change_ids_detected: []
  unrelated_refactoring_detected: false
  infrastructure_changes_detected: false
  pcf_changes_detected: false
  scope_violation_detected: false
```

Necessary shared build or test support is not automatically a violation, but it must map to at least one resolved change ID and be proportionate to the approved remediation.

## Output artifact

Use the HVE review artifact generated by `/rpi-review` as the authoritative post-implementation review record.

If repository-owned output is permitted, also create:

- `assessment/outputs/post-implementation-review.yml`
- `assessment/outputs/post-implementation-review.md`
- `assessment/outputs/finding-closure-summary.md`

If write permissions are constrained, preserve all required scope-validation, review, closure, and follow-up sections in the HVE-authorized review artifact and report its exact path.

## Follow-up routing

Route unresolved work to the earliest responsible phase:

- Missing or incorrect inventory evidence: research or inventory correction
- Incorrect finding mapping: assessment-review correction
- Plan defect: planning revision
- Implementation defect: implementation rework
- Validation environment problem: follow-up validation
- Approval or scope conflict: human governance review

Do not silently repair issues during review.

### Kafka scenario review

Verify implementation preserves the approved scenario, processing model, regional ownership, external-side-effect safety, and state/recovery contract. For database-independent Kafka, verify no unapproved database dependency or pod-local correctness state was introduced.

## End-of-Phase Compact Handoff Summary

At the end of this phase, create one compact handoff summary under:

```text
.copilot-tracking/reviews/handoffs/
```

Read and follow:

```text
grounding/governance/phase-handoff-schema.yml
```

The handoff summary is a non-authoritative index of facts already established by this phase. It supports state reconstruction after `/clear` or a new chat. It never replaces the authoritative phase artifact.

Requirements:

- Derive every value from the authoritative phase artifacts.
- Preserve stable finding, evidence, change, policy, scenario, and control IDs.
- Include exact authoritative input and output artifact paths.
- Include key decisions, counts, unresolved items, exceptions, and required next-phase inputs.
- Do not create findings, reassess controls, recalculate priority, change scenarios, invent evidence, authorize implementation, or modify source.
- When the summary conflicts with an authoritative artifact, the authoritative artifact wins and the handoff must record a `handoff_exception`.
- Report the generated handoff path in the completion response.

### Step 5 handoff

Write `.copilot-tracking/reviews/handoffs/05-review-summary.yml`.

Include the frozen review scope, scope-match result, status per change ID, original finding dispositions, regressions, scope violations, follow-up routing, and workflow completion status.

The handoff must not close a finding independently. It only summarizes dispositions recorded in the authoritative Step 5 review artifact.


## Completion validation

Before completing, verify that:

1. The review used the frozen Step 4 implementation scope when available.
2. Priority, wave, and change-ID selectors were not recalculated when a valid implementation scope existed.
3. Review scope exactly matches the Step 4 resolved change IDs.
4. Every resolved change has one review status.
5. Every associated original finding has one disposition.
6. Closed findings have source and validation evidence.
7. Partial, open, or blocked findings identify unmet acceptance criteria.
8. No new dependencies, findings, priorities, infrastructure, or PCF scope were added.
9. No source code was modified during review.
10. Scope expansion and regressions were explicitly checked.
11. Follow-up work was routed to the correct phase.
12. Verify that all prerequisite configuration required by implemented source-code changes is present.
13. Verify that readiness, liveness, startup, and actuator configuration are internally consistent.
14. Verify that enabled health contributors match health-group participation.
15. Verify that code behavior and configuration behavior are aligned.
16. Verify that implementation did not introduce disabled or orphaned resiliency configuration.

Report:

- Authoritative review artifact path
- Review-scope source
- Frozen resolved change IDs and count
- Scope-validation result
- Counts by change-review status
- Findings closed, partially closed, open, and blocked
- Regressions
- Scope violations
- Required follow-up

## Repository-Agnostic Snapshot Review

Do not require Git metadata to validate implementation. Review the Step 4 source-resolution record against path, symbol, original behavior, fingerprint when available, current diff, and validation evidence.

```yaml
source_locator_review:
  snapshot_type: git_revision|workspace_snapshot|uploaded_archive|source_drop|unknown
  snapshot_identifier_considered: true
  git_metadata_required: false
  path_match: true
  symbol_match: true
  original_excerpt_addressed: true
  fingerprint_validation: matched|changed_and_explained|not_available
  provenance_limitations_accepted_or_escalated: true
  line_numbers_treated_as_advisory: true
  source_drift_handled_correctly: true
```

Do not block closure solely because a commit SHA is unavailable. Block closure when source identity or behavioral remediation cannot be established.
