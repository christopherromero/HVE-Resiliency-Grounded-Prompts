---
schema_version: "1.1.0"
document_type: assessment_domain_standard
standard_id: HELM-KUSTOMIZE-RESILIENCY
version: "1.1.0"
lifecycle_status: active
owner: Cloud Architecture Team
assessment_domain: deployment_configuration
activation:
  scope_context_path: application-context/assessment-scope-context.yml
  required_status: enabled
repository_owned_only: true
infrastructure_findings_allowed: false
controls:
- id: HK-001
  title: A common base supports every approved region
  severity: critical
  category: regional-parity
  applies_when: Helm values or Kustomize overlays represent multiple regions
  evidence_patterns:
  - Chart.yaml
  - values-*.yaml
  - kustomization.yaml
  - overlays/
  - patchesStrategicMerge
  finding_when: regional deployments require separate application templates or materially
    divergent workload definitions without an approved reason
  emit_on_failure: true
- id: HK-002
  title: Image identity is immutable and consistently propagated
  severity: critical
  category: artifact-identity
  applies_when: image repository, tag, or digest is templated
  evidence_patterns:
  - image.tag
  - image.digest
  - newTag
  - newName
  - imagePullPolicy
  finding_when: rendered regions can resolve different mutable image references or
    digest values are ignored during rendering
  emit_on_failure: true
- id: HK-003
  title: Required regional values fail closed
  severity: critical
  category: regional-configuration
  applies_when: regional endpoints, region identifiers, ownership flags, or dependency
    settings are templated
  evidence_patterns:
  - required
  - default
  - values.schema.json
  - replacements
  - configMapGenerator
  finding_when: a required value can be omitted and silently default to a region, endpoint,
    or active ownership state
  emit_on_failure: true
- id: HK-004
  title: Values schemas validate safety-critical settings
  severity: high
  category: values-validation
  applies_when: Helm values configure probes, resources, ownership, endpoints, or image
    identity
  evidence_patterns:
  - values.schema.json
  - fail
  - required
  - documented invariant
  finding_when: malformed or incompatible safety-critical values can render successfully
    without validation
  emit_on_failure: true
- id: HK-005
  title: Overlays do not remove required resiliency behavior
  severity: critical
  category: overlay-integrity
  applies_when: Kustomize overlays or Helm environment values modify a common workload
  evidence_patterns:
  - patches
  - $patch:*delete*
  - 'null'
  - replacements
  - strategic merge
  finding_when: an overlay removes or overrides required probes, termination behavior,
    ownership controls, resource boundaries, or injected regional configuration
  emit_on_failure: true
- id: HK-006
  title: Rendered names, selectors, and labels remain consistent
  severity: high
  category: selector-integrity
  applies_when: templates generate Deployments, Services, PDBs, or policies
  evidence_patterns:
  - fullname
  - commonLabels
  - matchLabels
  - selector
  - nameSuffix
  finding_when: generated selectors can mismatch workload labels or cause availability
    and routing objects to target the wrong pods
  emit_on_failure: true
- id: HK-007
  title: Configuration checksums or equivalent rollout triggers are applied safely
  severity: high
  category: configuration-rollout
  applies_when: workload behavior depends on mounted or referenced configuration changes
  evidence_patterns:
  - checksum/config
  - configMapGenerator
  - secretGenerator
  - immutable
  - reload
  finding_when: repository-owned configuration can change without a defined application
    refresh or rollout mechanism and the running application retains stale safety-critical
    values
  emit_on_failure: true
- id: HK-008
  title: Template logic is deterministic and testable
  severity: high
  category: render-determinism
  applies_when: complex Helm logic, lookups, generators, or overlay composition is
    used
  evidence_patterns:
  - lookup
  - randAlphaNum
  - now
  - uuidv4
  - helm test
  finding_when: identical approved inputs can render materially different deployment
    behavior, or required resources depend on an unavailable live-cluster lookup during
    release preparation
  emit_on_failure: true
- id: HK-009
  title: Secrets are referenced, not embedded in values or rendered output
  severity: critical
  category: secret-handling
  applies_when: charts or overlays configure credentials or secret material
  evidence_patterns:
  - stringData
  - secretGenerator
  - ExternalSecret
  - connectionString
  - password
  finding_when: real secret material is committed, defaulted, logged, or rendered into
    non-secret artifacts
  emit_on_failure: true
- id: HK-010
  title: Regional and environment differences are explicit and bounded
  severity: medium
  category: configuration-governance
  applies_when: multiple values files or overlays exist
  evidence_patterns:
  - values-prod
  - values-dr
  - overlays/
  - duplicated block
  - undocumented override
  finding_when: materially different regional resiliency behavior is hidden in duplicated
    values or patches without an explicit, reviewable contract
  emit_on_failure: true
- id: HK-011
  title: Rendered health probe semantics are complete and regionally consistent
  severity: critical
  category: health
  applies_when: charts or overlays template readiness, liveness, or startup probes,
    or probe values are supplied per region or environment
  evidence_patterns:
  - readinessProbe
  - livenessProbe
  - startupProbe
  - actuator/health
  - health group
  finding_when: a rendered traffic-receiving workload has no readiness probe, a probe
    targets a path or port the application does not expose, liveness renders against
    a dependency-inclusive health group, probe timing renders inconsistently across
    regions, or probe values can be omitted and silently default to an unsafe configuration
  emit_on_failure: true
---

# Helm and Kustomize Resiliency Standard

## Purpose

Evaluate repository-owned Helm charts, values, templates, Kustomize bases, overlays, and patches for deterministic rendering and safe regional configuration. This standard complements, but does not duplicate, rendered Kubernetes workload controls.

## Controls

### HK-001: A common base supports every approved region

**Severity:** Critical  
**Category:** regional-parity  
**Applies when:** Helm values or Kustomize overlays represent multiple regions.

**Evidence to inspect:** Shared chart/base, regional values/overlays, duplicated templates, divergent patches.  
**Finding condition:** Emit a finding when regional deployments require separate application templates or materially divergent workload definitions without an approved reason.

### HK-002: Image identity is immutable and consistently propagated

**Severity:** Critical  
**Category:** artifact-identity  
**Applies when:** Image repository, tag, or digest is templated.

**Evidence to inspect:** Chart values, Helm templates, Kustomize images, pipeline substitutions.  
**Finding condition:** Emit a finding when rendered regions can resolve different mutable image references or when digest values are ignored during rendering.

### HK-003: Required regional values fail closed

**Severity:** Critical  
**Category:** regional-configuration  
**Applies when:** Regional endpoints, region identifiers, ownership flags, or dependency settings are templated.

**Evidence to inspect:** Helm `required`, defaults, schema validation, Kustomize substitutions, replacement behavior.  
**Finding condition:** Emit a finding when a required value can be omitted and silently default to a region, endpoint, or active ownership state.

### HK-004: Values schemas validate safety-critical settings

**Severity:** High  
**Category:** values-validation  
**Applies when:** Helm values configure probes, resources, ownership, endpoints, or image identity.

**Evidence to inspect:** `values.schema.json`, documented invariants, template guards.  
**Finding condition:** Emit a finding when malformed or incompatible safety-critical values can render successfully without validation.

### HK-005: Overlays do not remove required resiliency behavior

**Severity:** Critical  
**Category:** overlay-integrity  
**Applies when:** Kustomize overlays or Helm environment values modify a common workload.

**Evidence to inspect:** Patches, replacement directives, merge behavior, null/delete operations.  
**Finding condition:** Emit a finding when an overlay removes or overrides required probes, termination behavior, ownership controls, resource boundaries, or injected regional configuration.

### HK-006: Rendered names, selectors, and labels remain consistent

**Severity:** High  
**Category:** selector-integrity  
**Applies when:** Templates generate Deployments, Services, PDBs, or policies.

**Evidence to inspect:** Name helpers, common labels, selectors, release-name transformations.  
**Finding condition:** Emit a finding when generated selectors can mismatch workload labels or cause availability and routing objects to target the wrong pods.

### HK-007: Configuration checksums or equivalent rollout triggers are applied safely

**Severity:** High  
**Category:** configuration-rollout  
**Applies when:** Workload behavior depends on mounted or referenced configuration changes.

**Evidence to inspect:** Checksum annotations, rollout triggers, immutable ConfigMaps/Secrets, reload mechanism.  
**Finding condition:** Emit a finding when repository-owned configuration can change without a defined application refresh or rollout mechanism and the running application will retain stale safety-critical values.

### HK-008: Template logic is deterministic and testable

**Severity:** High  
**Category:** render-determinism  
**Applies when:** Complex Helm logic, lookups, generators, or overlay composition is used.

**Evidence to inspect:** Cluster lookups, time/random functions, generated values, conditional resources, chart tests.  
**Finding condition:** Emit a finding when identical approved inputs can render materially different deployment behavior or when required resources depend on unavailable live-cluster lookup during release preparation.

### HK-009: Secrets are referenced, not embedded in values or rendered output

**Severity:** Critical  
**Category:** secret-handling  
**Applies when:** Charts or overlays configure credentials or secret material.

**Evidence to inspect:** Values files, generated Secrets, external secret references, examples, test fixtures.  
**Finding condition:** Emit a finding when real secret material is committed, defaulted, logged, or rendered into non-secret artifacts.

### HK-010: Regional and environment differences are explicit and bounded

**Severity:** Medium  
**Category:** configuration-governance  
**Applies when:** Multiple values files or overlays exist.

**Evidence to inspect:** Difference sets, file naming, inheritance, duplicated blocks, undocumented overrides.  
**Finding condition:** Emit a finding when materially different regional resiliency behavior is hidden in duplicated values or patches without an explicit, reviewable contract.

### HK-011: Rendered health probe semantics are complete and regionally consistent

**Severity:** Critical  
**Category:** health  
**Applies when:** Charts or overlays template readiness, liveness, or startup probes, or probe values are supplied per region or environment.

**Evidence to inspect:** Probe blocks in templates, probe values and defaults, `values.schema.json` probe constraints, overlay patches touching probes, templated health paths and ports, application health-group values.  
**Finding condition:** Emit a finding when a rendered traffic-receiving workload has no readiness probe, a probe targets a path or port the application does not expose, liveness renders against a dependency-inclusive health group, probe timing renders inconsistently across regions, or probe values can be omitted and silently default to an unsafe configuration.

## Evaluation rules

- Render or reason from repository-native chart/overlay composition when available, but do not deploy.
- Apply Kubernetes deployment controls to the effective rendered behavior when it can be established.
- Deduplicate Helm/Kustomize and rendered-manifest findings under one root cause.
- Deduplicate HK-011 with `K8S-DEPLOY-001`, `K8S-DEPLOY-002`, and `K8S-DEPLOY-003`: attribute the finding to HK-011 when the defect originates in chart, values, or overlay composition, and to the Kubernetes control when it originates in a static manifest.
- Treat missing external values and platform overlays as `not_assessed`.
