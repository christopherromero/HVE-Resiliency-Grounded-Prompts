---
schema_version: "1.0.0"
document_type: assessment_domain_standard
standard_id: HELM-KUSTOMIZE-RESILIENCY
version: "1.0.0"
lifecycle_status: active
owner: Cloud Architecture Team
assessment_domain: deployment_configuration
activation:
  scope_context_path: application-context/assessment-scope-context.yml
  required_status: enabled
repository_owned_only: true
infrastructure_findings_allowed: false
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

## Evaluation rules

- Render or reason from repository-native chart/overlay composition when available, but do not deploy.
- Apply Kubernetes deployment controls to the effective rendered behavior when it can be established.
- Deduplicate Helm/Kustomize and rendered-manifest findings under one root cause.
- Treat missing external values and platform overlays as `not_assessed`.
