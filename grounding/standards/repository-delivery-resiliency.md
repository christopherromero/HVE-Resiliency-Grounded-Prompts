---
schema_version: "1.0.0"
document_type: repository_delivery_standard
standard_id: REPOSITORY-DELIVERY-RESILIENCY
version: "1.0.0"
lifecycle_status: active
owner: Cloud Architecture Team
---

# Repository-Owned Delivery Resiliency Standard

This standard is loaded only for explicitly enabled domains in `assessment-scope-context.yml`. It evaluates repository-owned artifacts and never proves deployed infrastructure state.

## Controls

### BUILD-001: Runtime base images are immutable
- Domain: `container_build`
- Severity: high
- Applies when: a repository-owned Dockerfile defines a runtime image
- Finding when: the runtime base image is referenced only by a mutable tag

### BUILD-002: Container builds are reproducible and fail closed
- Domain: `container_build`
- Severity: high
- Applies when: a repository-owned container build exists
- Finding when: dependency resolution, tests, or build failures can be ignored, or build inputs are materially unpinned without governance

### CICD-001: Required tests are enforced before artifact promotion
- Domain: `cicd_pipeline`
- Severity: critical
- Applies when: a repository-owned pipeline builds or promotes the application
- Finding when: required unit, integration, resiliency, or policy checks can be skipped or can fail without blocking promotion

### CICD-002: One immutable artifact is promoted across environments and regions
- Domain: `cicd_pipeline`
- Severity: critical
- Applies when: a repository-owned pipeline builds or deploys regional releases
- Finding when: different application artifacts are rebuilt for environments or regions, or promotion cannot prove artifact identity

### CICD-003: Deployment promotion has bounded health gates and rollback behavior
- Domain: `cicd_pipeline`
- Severity: high
- Applies when: repository-owned automation promotes a release
- Finding when: promotion lacks bounded readiness, smoke-test, failure, or rollback handling

### CICD-004: Pipeline secrets are referenced securely
- Domain: `cicd_pipeline`
- Severity: critical
- Applies when: repository-owned pipelines use credentials or tokens
- Finding when: secrets are embedded, printed, persisted as artifacts, or passed through unsafe plaintext mechanisms

### DEPLOY-001: Workload manifests use readiness, liveness, startup, and termination semantics correctly
- Domain: `deployment_configuration`
- Severity: critical
- Applies when: repository-owned Kubernetes, Helm, or Kustomize workload configuration exists
- Finding when: probe paths conflict with application behavior, external dependencies drive liveness, startup is unbounded, or termination does not allow safe drain

### DEPLOY-002: Regional values are injected without region-specific application artifacts
- Domain: `deployment_configuration`
- Severity: critical
- Applies when: repository-owned deployment configuration supplies regional values
- Finding when: physical endpoints or region values are hardcoded into source or require region-specific application artifacts

### DEPLOY-003: Rolling deployment settings preserve serving capacity
- Domain: `deployment_configuration`
- Severity: high
- Applies when: repository-owned deployment strategy is present
- Finding when: update strategy, disruption settings, or termination behavior can remove all available serving capacity for the application

### DEPLOY-004: Resource requests and limits are explicit and reviewable
- Domain: `deployment_configuration`
- Severity: high
- Applies when: repository-owned workload manifests are present
- Finding when: resource boundaries are absent or contradictory and repository evidence establishes a material availability risk

### IAC-001: Repository-owned IaC findings require explicit opt-in
- Domain: `infrastructure_as_code`
- Severity: high
- Applies when: status is `findings_enabled`
- Finding when: repository-owned IaC directly contradicts an approved application resiliency requirement
- Boundary: in `inventory_only`, record evidence but do not emit findings

## Evaluation rules
- Evaluate a control only when its domain is enabled.
- Disabled domains are `not_applicable`.
- Unknown or external ownership is `not_assessed` and routed to evidence gaps.
- Never infer deployed noncompliance from repository absence.
- Deduplicate delivery findings with application findings by root cause.
