>>>>>>>Step 1 execution - Use Task Researcher Agent

Follow:

prompts/01-create-inventory-hve-task-researcher.prompt.md

Assess the application under:

source/customer-app

ASSESSMENT_SCOPE_CONTEXT=application-context/assessment-scope-context.yml

ASSESSMENT_SCOPE_SCHEMA=grounding/governance/assessment-scope-schema.yml

Read and validate the assessment scope context.

Record:
- enabled domains
- disabled domains
- testing output mode
- priority filtering settings

Preserve these values in the inventory and handoff.

Create the authoritative inventory as your HVE research artifact.

Use this task slug:

springboot-active-active-inventory

Generate the compact handoff summary before completion in .copilot.tracking/research/handoffs/

Do not generate findings, recommendations, severity ratings,
compliance statuses, readiness scores, or implementation plans.

Report the exact research artifact path when complete.


>>>>>>>Step 2 execution - Use Task Reviewer Agent

Follow:

prompts/02-generate-findings-from-hve-research.prompt.md

Use this authoritative inventory:

INVENTORY_ARTIFACT=.copilot-tracking/research/2026-09-05/
springboot-active-active-inventory-research.md

Do not re-inventory the repository.

Evaluate only dependencies listed under:

Dependency Standards to Load

You may open only files cited by the inventory when needed
to validate a specific control.

Generate the compact handoff summary before completion

Do not invoke Task Researcher or researcher subagents.
Do not modify application source code.

Report the exact review artifact path when complete.


>>>>>>>Step 3a execution - Use Task Planner Agent


Follow:

prompts/03A-create-authoritative-remediation-plan.prompt.md

INVENTORY_ARTIFACT=.copilot-tracking/research/2026-09-05/
springboot-active-active-inventory-research.md
REVIEW_ARTIFACT=.copilot-tracking/reviews/2026-09-05/
springboot-active-active-inventory-research-review.md

Create the authoritative remediation plan with governed priorities
and illustrative Java, Spring Boot configuration, and test proposals.

Apply the highest-confidence illustrative implementation principle from
Prompt 3A. Generate concrete proposals for every evidence-supported
target and isolate targeted discovery to only the blocked targets.

Do not modify source code.
Do not re-inventory the repository.
Do not reassess findings.
Do not add infrastructure or PCF remediation.

Generate the compact handoff summary before completion

Report the exact plan artifact path when complete.

>>>>>>>Step 3b execution  - Use Task Planner Agent

Follow:

prompts/03B-create-code-level-resiliency-assessment-report-schema-governed.prompt.md

INVENTORY_ARTIFACT=.copilot-tracking/research/2026-09-05/
springboot-active-active-inventory-research.md
REVIEW_ARTIFACT=.copilot-tracking/reviews/2026-09-05/
springboot-active-active-inventory-research-review.md
PLAN_ARTIFACT=.copilot-tracking/plans/2026-09-05/
springboot-active-active-remediation-plan.instructions.md

REPORT_SCHEMA=grounding/governance/assessment-report-schema.md
REPORT_VERSION = 1.0.0

APPLICATION_CONTEXT=application-context\assessment-context.md
REFERENCE_ARCHITECTURE_REGISTRY=grounding\registry\dependency-standard-registry.yml
ASSESSMENT_SCOPE_CONTEXT= application-context/assessment-scope-context.yml
ASSESSMENT_SCOPE_SCHEMA=grounding/governance/assessment-scope-schema.yml

Read and validate the report schema before generating the report.

Read and apply report_preferences from the
assessment scope context.

Generate the report according to:

finding_selection.mode

finding_selection.include_priorities

testing_output.mode

testing_output settings

Do not modify findings, priorities,
severity, status, evidence,
or remediation plans.

Do not put notes in the report or each finding about something not being rendered if that decision was defined in the assessement-scope-context.

Filtering applies only to report rendering.
`

Do not create new findings.
Do not create infrastructure findings.
Do not create PCF findings or recommendations.

Generate the compact handoff summary before completion

Report the exact assessment artifact path when complete.


>>>>>>>Step 4 execution

/rpi-implement

Follow:

prompts/04-implement-approved-remediation-complete-priority-aware.prompt.md

INVENTORY_ARTIFACT=.copilot-tracking/research/2026-09-01/
springboot-active-active-inventory-research.md
REVIEW_ARTIFACT=.copilot-tracking/reviews/2026-09-01/
springboot-active-active-inventory-research-review.md
PLAN_ARTIFACT=.copilot-tracking/plans/2026-09-01/
springboot-active-active-remediation-plan.instructions.md

APPROVED_PRIORITIES=P0,P1
APPROVED_WAVES=
APPROVED_CHANGE_IDS=

Use Task Implementor with the rpi-implement phase.

Implement only the scope resolved from the approved priorities.
Do not re-inventory, reassess, or recalculate priority.
Do not commit, push, or create a pull request.

>>>>>>>Step 5 Execution

/rpi-review

Follow:

assessment/prompts/
05-review-implemented-remediation-complete-priority-aware.prompt.md

INVENTORY_ARTIFACT=<exact Step 1 artifact path>
ORIGINAL_REVIEW_ARTIFACT=<exact Step 2 artifact path>
PLAN_ARTIFACT=<exact Step 3 artifact path>
IMPLEMENTATION_ARTIFACT=<exact Step 4 artifact path>

Use the frozen resolved_change_ids from the Step 4 implementation artifact.

Do not re-inventory.
Do not perform the full assessment again.
Do not recalculate priorities.
Do not create unrelated findings.
Do not modify source code.