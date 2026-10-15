# Code-Level Resiliency Assessment Solution Maintenance Guide

## 1. Purpose

This guide explains how to maintain and extend the governed code-level resiliency assessment solution. It is intended for solution maintainers, architects, prompt engineers, technical reviewers, and Human SMEs.

The solution uses a controlled multi-phase lifecycle:

```text
Step 1  Inventory and context resolution
Step 2  Evidence-backed finding generation and classification
Step 3A Authoritative remediation planning and prioritization
Step 3B Customer-facing report generation
Step 4  Approved implementation
Step 5  Implementation validation and closure review
```

The primary maintenance principle is:

> Put architecture intent in application context, reusable assessment logic in grounding and governance, phase behavior in prompts, rendering requirements in report schemas, and implementation detail in the authoritative Step 3A plan.

---

## 2. Solution map and ownership

### Application-specific context

```text
application-context/
├── application-architecture-context.yml
├── assessment-scope-context.yml
└── reference-architecture-registry.yml
```

Use these files for facts and decisions specific to one assessed repository or application.

- `application-architecture-context.yml` defines current/source deployment, approved target deployment, runtime expectations, shared-service operating models, connectivity contracts, dependency expectations, architecture decisions, and per-service assessment scope.
- `assessment-scope-context.yml` enables or disables repository artifact domains such as application code, CI/CD, container build, Kubernetes, Helm/Kustomize, and infrastructure files.
- `reference-architecture-registry.yml` contains approved customer-specific reference architecture links used by Step 3B.

### Reusable dependency and domain standards

```text
grounding/dependencies/
├── springboot-<service>.md
├── jvm-runtime-resiliency.md
├── kubernetes-deployment-resiliency.md
├── cicd-pipeline-resiliency.md
└── ...
```

Use these files for reusable controls, evidence patterns, applicability rules, finding conditions, qualification guidance, and implementation boundaries.

### Governance and policy

```text
grounding/governance/
├── assessment-scope-schema.yml
├── assessment-report-schema.md
├── phase-handoff-schema.yml
├── resiliency-finding-qualification-policy.yml
├── remediation-prioritization.md
├── shared-service-assessment-scope-schema.yml
├── shared-service-operating-model-policy.yml
├── kafka-operating-scenario-policy.yml
└── ...
```

Use governance files for rules shared by all applications and phases.

### Registry

```text
grounding/registry/dependency-standard-registry.yml
```

The registry is the single authority that maps canonical service IDs to grounding files, versions, activation patterns, scenario policies, and context requirements.

### Prompts and wrappers

```text
prompts/
├── 01-create-inventory-hve-task-researcher.prompt.md
├── 02-generate-findings-from-hve-research.prompt.md
├── 03A-create-authoritative-remediation-plan.prompt.md
├── 03B-create-code-level-resiliency-assessment-report-schema-governed.prompt.md
├── 04-implement-approved-remediation-complete-priority-aware.prompt.md
└── 05-review-implemented-remediation-complete-priority-aware.prompt.md

.github/prompts/
├── 01-inventory.prompt.md
└── ...
```

The authoritative prompts define phase responsibilities. Wrapper prompts collect parameters and route execution to the authoritative prompts.

---

# Part I: Adding a New Shared Service

## 3. Decide whether a new grounding standard is needed

Create a new dependency grounding file when all are true:

1. The service is used or expected in production application code.
2. The service has application-owned resiliency behaviors that can be evaluated from repository evidence.
3. Existing standards do not accurately cover the service.
4. The service may be in scope for findings and remediation.

Do not create a new grounding file merely because the service is visible in architecture. A service classified `out_of_scope`, `informational_only`, or `architecture_only` can remain in context without a grounding standard.

## 4. Choose the canonical service key

Use a stable kebab-case identifier:

```yaml
databricks
elasticsearch
mongo-atlas
azure-sql
confluent-kafka
```

Rules:

- Match the registry ID exactly across all files.
- Do not use aliases such as `mongo_atlas`, `mongoAtlas`, or `mongo-db-atlas`.
- Do not use display names as keys.
- Once published, treat the canonical key as an API contract.

## 5. Create the grounding file

Use:

```text
grounding/dependencies/springboot-<canonical-key>.md
```

For example:

```text
grounding/dependencies/springboot-mongo-atlas.md
```

The standard should include:

1. Metadata and version.
2. Purpose and scope boundary.
3. Shared-service assessment-scope contract.
4. Operating-model and connectivity-context contract.
5. Evaluator workflow.
6. Evidence and locator rules.
7. Controls with stable IDs.
8. Finding and non-finding rules.
9. Business-logic and security boundaries.
10. Validation expectations.

### Control ID convention

Choose a stable prefix:

```text
DATABRICKS-001
ES-001
MONGO-ATLAS-001
```

Never renumber published controls. Deprecate old controls instead.

### Control structure

Each control should define:

```yaml
id: MONGO-ATLAS-001
title: Connection endpoint is deployment-injected
severity: critical
category: configuration
evidence_patterns:
  - mongodb+srv
  - connection string
  - spring.data.mongodb.uri
finding_when: A physical or region-specific endpoint is hardcoded.
emit_on_failure: true
```

The narrative must also state:

- Requirement
- Repository evidence to inspect
- Finding condition
- Evidence rule
- Quality caveats
- Resiliency qualification guidance
- Business-logic risk

## 6. Add the registry entry

Update:

```text
grounding/registry/dependency-standard-registry.yml
```

Example:

```yaml
standards:
  mongo-atlas:
    display_name: MongoDB Atlas
    grounding_file: grounding/dependencies/springboot-mongo-atlas.md
    type: dependency_standard

    activate_when_any:
      inventory_dependencies:
        - mongo-atlas
        - mongodb-atlas

      repository_patterns:
        - mongodb+srv
        - spring.data.mongodb.uri
        - MongoClientSettings

    standard:
      path: grounding/dependencies/springboot-mongo-atlas.md
      version: "1.0.0"

    architecture_context_required: true
    shared_service_scope_required: true
```

Validation rules:

- `grounding_file` equals `standard.path`.
- The file exists.
- The version matches the standard metadata.
- Repository patterns are evidence hints, not proof of production use.
- Activation does not override approved shared-service scope.

## 7. Add application architecture context

Add the service under the applicable sections.

### Dependency expectation

```yaml
dependency_expectations:
  mongo-atlas: required
```

Allowed statuses:

```text
required
optional
not_expected
unknown
```

### Operating model

```yaml
shared_service_operating_models:
  services:
    mongo-atlas:
      dependency_standard_id: mongo-atlas

      source:
        operating_model: single_region
        lifecycle_status: current

      target:
        operating_model: active_active
        lifecycle_status: approved_target
```

Only declare operating models supported by approved architecture evidence.

### Connectivity contract

Add a connectivity contract only when the application must use a resiliency-significant endpoint abstraction.

```yaml
shared_service_connectivity_contracts:
  services:
    mongo-atlas:
      dependency_standard_id: mongo-atlas

      target:
        connectivity_model: global_srv_endpoint
        lifecycle_status: approved_target
```

Do not add empty connectivity contracts simply for consistency.

### Assessment scope

```yaml
shared_service_assessment_scope:
  services:
    mongo-atlas:
      assessment_scope: in_scope
      rationale: Mongo Atlas application behavior is included in this assessment.
      scope_owner: application_architecture
```

## 8. Determine whether a scenario policy is needed

Create a scenario policy when the same service supports materially different operating patterns that change applicable controls.

Examples:

- Kafka active-standby versus independent-regional active-active
- DSE Cassandra single-datacenter versus multi-datacenter
- Database-backed versus database-independent Kafka processing

Register it under the service:

```yaml
scenario_policy:
  path: grounding/governance/mongo-atlas-operating-scenario-policy.yml
  version: "1.0.0"
```

Do not encode application-specific topology directly in the reusable grounding standard.

## 9. Update reference architecture registry when applicable

If an approved customer reference exists, add it to:

```text
application-context/reference-architecture-registry.yml
```

Do not embed customer URLs in the reusable report schema or grounding standard.

## 10. Validate the new service

Run the checklist in `checklists/new-shared-service-checklist.md`.

Minimum validation:

- Canonical keys match.
- Registry paths and versions match.
- Context has dependency expectation and scope.
- Operating and connectivity models are explicit or unresolved.
- Step 1 can inventory the service.
- Step 2 respects scope before control evaluation.
- Findings map to stable controls.
- Step 3A preserves business behavior.
- Step 3B renders the service correctly.
- Step 4 cannot implement excluded scope.
- Step 5 validates closure.

---

# Part II: Managing Shared-Service Assessment Scope

## 11. Understand the four scope values

### `in_scope`

Use when the service may be control-evaluated and produce findings, priorities, remediation, implementation, and closure review.

### `out_of_scope`

Use when the service is used and architecturally relevant but belongs to another engagement or team.

Behavior:

- Inventory required
- Architecture reasoning allowed
- Control evaluation prohibited
- Findings prohibited
- Remediation prohibited
- Implementation prohibited

### `informational_only`

Use when concise observations are useful but must not become findings.

Behavior:

- Inventory required
- Architecture reasoning allowed
- Observations allowed
- Finding IDs and priorities prohibited
- Remediation and implementation prohibited

### `architecture_only`

Use when the service affects authoritative state, processing-chain, operating scenario, ownership, or target design but repository controls must not be evaluated.

## 12. Add or change a service scope

Modify:

```yaml
architecture_context:
  shared_service_assessment_scope:
    services:
```

Example:

```yaml
databricks:
  assessment_scope: out_of_scope
  rationale: Assessed separately by the enterprise data platform team.
  scope_owner: data_platform_team
  external_assessment_reference: not_provided
```

## 13. Scope-change governance

Treat a scope change as an approved architecture-governance amendment.

Record:

```yaml
scope_amendment:
  amendment_id: SCOPE-2026-001
  service_key: databricks
  original_scope: out_of_scope
  revised_scope: in_scope
  rationale: Databricks application integration is now included in this engagement.
  approved_by: Architecture Review Board
  approved_at: 2026-10-01
```

If scope changes after Step 1:

1. Update application context.
2. Rerun Step 1.
3. Rerun Step 2.
4. Rerun Step 3A and Step 3B.
5. Do not let Step 4 infer the scope amendment.

## 14. Scope versus exclusion

Use repository exclusion for content that should not be processed:

```text
Historical PCF files
Generated code
Vendored code
Build output
Archived migration assets
```

Use shared-service scope for a real dependency that remains visible but has restricted assessment participation.

## 15. Unregistered services

A service can appear in architecture context before a grounding standard exists.

If it is non-in-scope:

- Inventory it.
- Preserve architecture relationships.
- Do not invent a grounding path.
- Do not load another service's standard.

If it becomes `in_scope`:

- Add a registry entry.
- Add a grounding standard.
- Validate activation patterns.
- Rerun Step 1 onward.

---

# Part III: Managing Artifact-Domain Scope and Repository Exclusions

## 16. Artifact-domain scope

Use:

```text
application-context/assessment-scope-context.yml
```

for domains such as:

```text
application_code
cicd_pipeline
container_build
deployment_configuration
infrastructure_as_code
runtime_configuration
```

Do not place individual services here.

## 17. Repository exclusions

Define path-based exclusions for files that must not be evaluated.

Example:

```yaml
repository_exclusions:
  paths:
    - legacy/pcf/**
    - generated/**
    - vendor/**
    - target/**

  reasons:
    legacy/pcf/**: Historical PCF assets are outside the AKS target assessment.
```

Rules:

- Exclusion applies to artifacts, not service existence.
- Excluded files cannot become source evidence.
- Excluded files must not trigger dependencies.
- Exclusions must not hide active source code through overly broad patterns.

## 18. Changing domain scope

When enabling a new domain:

1. Set the domain to enabled in assessment scope context.
2. Ensure the corresponding standard exists.
3. Add or verify registry/domain activation rules.
4. Add evidence patterns.
5. Verify Step 1 inventories the domain.
6. Verify Step 2 can generate findings.
7. Add corresponding test and report conformance checks.

---

# Part IV: Testing and Validation Options

## 19. Testing option categories

Maintain distinct options for:

1. Existing-test execution
2. Generated test proposals
3. Fault-injection recommendations
4. Integration-test requirements
5. Load and soak testing
6. Manual validation
7. External platform evidence
8. Implementation verification

## 20. Configure testing output

Use `assessment-scope-context.yml` for assessment-wide testing behavior.

Recommended structure:

```yaml
testing_options:
  run_existing_tests: true
  propose_missing_tests: true
  create_test_code_in_step_4: true
  require_failure_scenario_mapping: true
  require_target_architecture_relevance: true
  allow_mock_only_validation: false
  include_manual_validation_steps: true
```

## 21. Test-finding governance

A missing test is not automatically a resiliency finding.

Rules:

- The test must map to a specific applicable failure behavior.
- The test finding inherits the resiliency classification of that behavior.
- Generic test absence is non-resiliency.
- Avoid duplicate test findings when the underlying behavior already has a finding; add validation requirements to the primary remediation change instead.

## 22. Validation by phase

### Step 1

Validate inventory completeness, scope resolution, context paths, registry activation, and evidence provenance.

### Step 2

Validate repository evidence, control applicability, classification, deduplication, and scope gate.

### Step 3A

Validate priority rule, business-logic risk, scope, implementation boundary, approved library, test plan, and selector indexes.

### Step 3B

Validate class/priority order, count reconciliation, concise rendering, scope summary, matrix completeness, roadmap mapping, and traceability.

### Step 4

Validate selector resolution, approval gates, scope gates, behavior preservation, build/tests, and updated files.

### Step 5

Validate implementation against the original causal mechanism, acceptance criteria, source evidence, target architecture, and unchanged business behavior.

## 23. Recommended validation commands

At minimum:

```bash
python -c "import yaml; list(yaml.safe_load_all(open('application-context/application-architecture-context.yml')))"
```

```bash
unzip -t package.zip
```

Use repository-specific build and test commands instead of hardcoded universal commands.

## 24. Regression fixtures

Maintain sample contexts for:

- Azure SQL with FOG listener
- Cosmos DB without SQL
- No-database Kafka
- Kafka active-standby
- Kafka independent-regional active-active with mirroring
- Shared service out of scope
- Shared service informational only
- Shared service architecture only
- Application with no database
- Repository with excluded PCF files

Each fixture should declare expected:

- Loaded standards
- Effective scope
- Findings allowed/prohibited
- Scenario selected
- Priorities
- Report sections
- Step 4 selectors

---

# Part V: Finding Classification and Prioritization

## 25. Maintain finding classification

The qualification policy owns whether a finding is:

```text
resiliency
non_resiliency
```

Resiliency requires:

- Repository evidence
- Applicable violated control
- Credible failure scenario
- Approved resiliency domain
- Causal mechanism
- Target-architecture impact
- Material impact

Do not embed priority logic into the qualification policy beyond allowed combinations.

## 26. Maintain allowed priorities

Current contract:

```yaml
resiliency: [P0, P1, P2, P3]
non_resiliency: [P2, P3]
```

Existing non-resiliency P0/P1 findings must be reprioritized, not hidden.

## 27. Add a new priority rule

Update:

```text
grounding/governance/remediation-prioritization.md
```

Every new rule needs:

- Stable rule ID
- Applicability conditions
- Required evidence
- Exclusions
- Precedence
- Examples
- Migration guidance

Do not lower priority based on remediation owner, implementation effort, or evidence confidence. Keep those as separate fields.

## 28. Human SME amendments

If an SME changes priority:

- Preserve calculated priority.
- Record the approved override.
- Update all indexes and counts.

If an SME changes classification:

- Amend Step 2 first.
- Regenerate or amend Step 3A.
- Regenerate Step 3B.
- Keep IDs stable.

---

# Part VI: Maintaining Operating Models and Connectivity Contracts

## 29. Operating model versus connectivity model

Operating model describes service topology:

```text
active_active
active_standby
single_region
```

Connectivity model describes how the application consumes the service:

```text
failover_group_listener
regional_endpoint_discovery
independent_regional_clusters
```

Do not mix these concepts.

## 30. Azure SQL FOG maintenance

Keep:

```yaml
operating_model: active_standby
```

and separately define:

```yaml
connectivity_model: failover_group_listener
```

Grounding may evaluate:

- Listener usage
- Direct regional endpoint prohibition
- Pool recovery
- Stale connection cleanup
- Reconnect without restart

Grounding must not recommend custom application failover or failback orchestration already provided by FOG.

## 31. Kafka scenario maintenance

Kafka application scenario must be selected through the Kafka scenario policy.

For independent-regional active-active:

- Independent regional clusters
- Local-region affinity
- Topic mirroring contract
- Offset recovery strategy
- Duplicate and replay safety
- External side-effect classification

Missing deployed mirroring proof is an evidence gap. Repository behavior that assumes unmirrored required topics despite an approved mirroring contract may produce a finding.

## 32. Architecture decisions

Add approved application decisions under:

```yaml
architecture_context:
  architecture_decisions:
```

Use for decisions such as mandatory Kafka topic mirroring or Azure SQL listener usage. Do not place application-specific decisions in reusable grounding files.

---

# Part VII: Prompt and Handoff Maintenance

## 33. Changing a prompt safely

Before editing a prompt:

1. Identify the phase authority.
2. Identify input artifacts.
3. Identify prohibited behavior.
4. Identify output artifacts.
5. Identify handoff fields.
6. Identify downstream consumers.

After editing:

1. Update corresponding handoff schema.
2. Update report schema if rendering changes.
3. Update scope schemas if applicability changes.
4. Add completion validation.
5. Validate wrapper references.
6. Run a sample end to end.

## 34. Wrapper maintenance

Wrappers should:

- Collect parameters
- Resolve paths
- Name the expected artifact
- Invoke the authoritative prompt

Wrappers should not duplicate governance logic.

Validate:

```text
RUN_DATE
SOURCE_ROOT
TASK_SLUG
expected artifact path
context paths
governance paths
```

## 35. Handoff maintenance

When adding a new authoritative field, add it to the handoff schema and prohibit downstream recalculation.

Examples:

```text
shared-service scope
finding classification
priority rule
business-logic risk
architecture conflicts
scenario selection
```

---

# Part VIII: Report Maintenance

## 36. Preserve report authority boundaries

The report summarizes Step 2 and Step 3A. It must not create, reclassify, or reprioritize findings.

## 37. Report ordering

Current order:

```text
Resiliency findings: P0, P1, P2, P3
Non-resiliency findings: P2, P3
```

## 38. Concise rendering

Maintain field-specific limits and avoid repeating the same concept across Finding, Impact, Architecture Context, Evidence, and Recommendation.

Do not remove required traceability merely to shorten reports.

## 39. Scope summary

Assessment Overview should list service scope without counting non-finding scope records as findings.

---

# Part IX: Versioning and Release Management

## 40. Versioning rules

Use semantic versions:

- Major: incompatible schema or behavior change
- Minor: backward-compatible controls or governance capability
- Patch: clarification or non-behavioral correction

Keep versions synchronized across:

- Registry entry
- Grounding metadata
- Scenario policy reference
- Context contract
- Prompt-required version

## 41. Package checklist

Every release package should include:

```text
CHANGE-SUMMARY.md
UPGRADE-INSTRUCTIONS.md
VALIDATION-REPORT.json
MANIFEST.json
```

The manifest should include repository-relative paths, sizes, and SHA-256 hashes.

## 42. Upgrade procedure

1. Back up current files.
2. Overlay package at repository root.
3. Validate YAML and Markdown structure.
4. Compare registry paths and versions.
5. Run regression fixtures.
6. Determine the earliest phase that must be rerun.
7. Mark superseded artifacts.
8. Do not reuse incompatible downstream artifacts.

---

# Part X: Common Maintenance Scenarios

## 43. Add an in-scope shared service

1. Choose canonical key.
2. Create grounding.
3. Add registry entry.
4. Add dependency expectation.
5. Add operating model.
6. Add connectivity contract if needed.
7. Set `assessment_scope: in_scope`.
8. Add architecture decision if required.
9. Add test fixture.
10. Rerun Step 1 through Step 3B.

## 44. Add an out-of-scope service

1. Add it to dependency/architecture context.
2. Set `assessment_scope: out_of_scope`.
3. Add rationale and owner.
4. Do not invent grounding.
5. Verify Step 1 inventories it.
6. Verify Step 2 creates no findings.
7. Verify report shows it as outside scope.

## 45. Change a service from out of scope to in scope

1. Obtain approval.
2. Add grounding and registry entry if missing.
3. Update context scope.
4. Rerun Step 1 onward.
5. Do not reuse old Step 2 or Step 3A artifacts.

## 46. Add a new control

1. Confirm reusable applicability.
2. Assign stable ID.
3. Define exact evidence.
4. Define finding condition.
5. Define non-finding/evidence-gap boundary.
6. Define resiliency relevance.
7. Define business-logic risk.
8. Define test validation.
9. Bump standard version.
10. Update registry version.

## 47. Deprecate a control

1. Do not delete its ID from history.
2. Mark lifecycle status deprecated.
3. State replacement control when applicable.
4. Update registry/standard version.
5. Add migration guidance.

## 48. Add or refine exclusions

1. Identify exact repository paths.
2. Document why they are excluded.
3. Ensure patterns do not match active source.
4. Verify Step 1 does not use them as evidence.
5. Preserve architecture facts from approved context, not excluded files.

## 49. Update testing behavior

1. Change assessment scope testing options.
2. Update Step 1 inventory requirements if discovery changes.
3. Update Step 2 classification for test-only gaps.
4. Update Step 3A test-plan output.
5. Update Step 4 generated-test permissions.
6. Update Step 5 closure evidence.
7. Add regression fixture.

## 50. Update report verbosity

1. Change report schema field limits.
2. Change Step 3B rendering instructions.
3. Do not modify Step 2 evidence detail.
4. Do not modify Step 3A implementation detail.
5. Validate counts and traceability remain complete.

---

# Part XI: Troubleshooting

## 51. Prompt appears but does not run

Check:

- Workspace root contains `.github/prompts`.
- Wrapper frontmatter is valid.
- `agent: agent` is compatible with manual role selection.
- Input variables use exact names and casing.
- Expected artifact paths resolve.
- VS Code window is reloaded after changes.
- Output logs show no parser error.

## 52. Service detected but no grounding loaded

Check:

- Canonical key normalization
- Registry activation patterns
- Production-use evidence
- Assessment scope
- Registry path and version
- Missing standard gap

## 53. Out-of-scope service generated findings

Check:

- Step 1 emitted effective scope.
- Step 2 used Step 1 scope instead of recalculating.
- Service key matches exactly.
- Default scope did not apply due to a missing key.
- Dependency standard includes the scope gate.

## 54. Findings use wrong priority class

Check:

```yaml
resiliency: [P0, P1, P2, P3]
non_resiliency: [P2, P3]
```

Reprioritize existing non-resiliency P0/P1 findings in Step 3A; do not hide them in Step 3B.

## 55. Report counts do not reconcile

Compare:

- Step 2 finding total
- Step 3A planned/disposition totals
- Resiliency/non-resiliency totals
- Priority totals
- Detailed section findings
- Full Finding Matrix
- Appendix A

Treat mismatch as report conformance failure.

---

# Part XII: Maintenance Cadence

## 56. Per change

- Update versions
- Update registry
- Run syntax checks
- Run targeted fixture
- Update change summary

## 57. Per release

- Run all regression fixtures
- Validate all registry paths
- Validate context keys
- Validate control IDs are unique
- Validate report and plan counts
- Validate package integrity

## 58. Quarterly governance review

Review:

- SME classification disagreements
- Priority overrides
- Repeated evidence gaps
- New shared services
- Deprecated libraries
- Platform architecture changes
- False-positive controls
- Findings repeatedly reclassified by humans
- Report usability feedback

Use repeated patterns, not isolated preferences, to justify governance changes.
