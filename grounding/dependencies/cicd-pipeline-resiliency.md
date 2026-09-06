---
schema_version: "1.0.0"
document_type: assessment_domain_standard
standard_id: CICD-PIPELINE-RESILIENCY
version: "1.0.0"
lifecycle_status: active
owner: Cloud Architecture Team
assessment_domain: cicd_pipeline
activation:
  scope_context_path: application-context/assessment-scope-context.yml
  required_status: enabled
repository_owned_only: true
infrastructure_findings_allowed: false
---

# CI/CD Pipeline Resiliency Standard

## Purpose

Evaluate repository-owned CI/CD workflows that build, test, package, promote, or deploy the assessed application. This standard does not assess externally owned pipeline templates, service connections, hosted agents, deployed environments, or Azure resource state unless the repository contains the authoritative definition and the applicable scope explicitly allows it.

## Evidence boundary

Generate findings only from repository-owned pipeline definitions and directly referenced repository files. Missing externally owned pipeline configuration is `not_assessed`, not noncompliant. A disabled `cicd_pipeline` domain makes all controls in this standard `not_applicable`.

## Controls

### CICD-001: Required validation gates block artifact promotion

**Severity:** Critical  
**Category:** pipeline-quality-gates  
**Applies when:** A repository-owned pipeline builds or promotes an application artifact.

**Evidence to inspect:**
- Azure Pipelines stages, jobs, conditions, dependencies, templates, and continue-on-error behavior
- GitHub Actions jobs, required dependencies, conditions, and failure handling
- Maven or Gradle test invocations
- Static analysis, security scanning, and policy validation steps

**Finding condition:** Emit a finding when required build, unit, integration, resiliency, policy, or security validation can be skipped, ignored, or allowed to fail while the artifact continues to promotion or deployment.

### CICD-002: One immutable artifact is promoted across environments and regions

**Severity:** Critical  
**Category:** artifact-promotion  
**Applies when:** A pipeline builds and deploys the application to more than one environment or region.

**Evidence to inspect:**
- Build and release stage separation
- Artifact publishing and download steps
- Image tags and digests
- Environment-specific rebuild steps
- Regional deployment jobs

**Finding condition:** Emit a finding when separate environment or regional jobs rebuild the application, cannot prove identical artifact identity, or deploy mutable references that can resolve differently between targets.

### CICD-003: Pipeline concurrency protects release integrity

**Severity:** High  
**Category:** release-concurrency  
**Applies when:** Multiple pipeline runs or deployment jobs can target the same application environment.

**Evidence to inspect:**
- Concurrency groups
- Environment locks or exclusive checks
- Batch behavior
- Deployment job serialization
- Cancellation and supersession behavior

**Finding condition:** Emit a finding when overlapping runs can concurrently promote, deploy, roll back, or mutate the same release target without an explicit serialization or supersession policy.

### CICD-004: Deployment promotion has bounded health gates and failure handling

**Severity:** High  
**Category:** deployment-gates  
**Applies when:** Repository-owned automation deploys or promotes the application.

**Evidence to inspect:**
- Smoke tests
- Readiness checks
- Health polling loops
- Timeouts
- Retry limits
- Rollback or stop conditions

**Finding condition:** Emit a finding when health verification is missing, unbounded, ignores failure, or permits promotion despite an unhealthy application.

### CICD-005: Pipeline credentials and sensitive values are handled securely

**Severity:** Critical  
**Category:** pipeline-security  
**Applies when:** Pipeline definitions use credentials, tokens, connection strings, certificates, or signed values.

**Evidence to inspect:**
- Literal secrets
- Variable usage
- Secret stores
- Logging and debug output
- Command-line arguments
- Published artifacts

**Finding condition:** Emit a finding when a secret is embedded, echoed, persisted in an artifact, passed through an unsafe plaintext mechanism, or exposed through verbose logging.

### CICD-006: Pipeline retries are bounded and safe

**Severity:** High  
**Category:** pipeline-retry  
**Applies when:** Pipeline steps retry builds, tests, publication, or deployment actions.

**Evidence to inspect:**
- Retry loops
- Task retry settings
- Script loops
- Backoff behavior
- Idempotency of repeated deployment actions

**Finding condition:** Emit a finding when retries are unbounded, immediate, hide deterministic failures, or repeat a non-idempotent deployment action without safety.

### CICD-007: Pipeline templates and actions are version-pinned

**Severity:** High  
**Category:** supply-chain  
**Applies when:** Pipelines consume external actions, templates, tasks, scripts, or reusable workflows.

**Evidence to inspect:**
- GitHub Action references
- External template repository references
- Pipeline task versions
- Downloaded scripts and tools

**Finding condition:** Emit a finding when executable pipeline dependencies use floating branches, mutable tags, unverified downloads, or otherwise lack an immutable or governed version reference.

### CICD-008: Regional configuration is injected without changing application artifacts

**Severity:** Critical  
**Category:** regional-deployment  
**Applies when:** The pipeline deploys the application to multiple regions.

**Evidence to inspect:**
- Regional variables
- Environment substitutions
- Values files
- Artifact selection
- Image references

**Finding condition:** Emit a finding when regional differences require a different application build, hardcoded regional artifact, or source modification instead of deployment-time configuration.

### CICD-009: Rollback preserves artifact identity and operational safety

**Severity:** High  
**Category:** rollback  
**Applies when:** Repository-owned pipeline automation supports rollback or redeployment.

**Evidence to inspect:**
- Rollback stages and scripts
- Previous artifact selection
- Database compatibility checks
- Migration ordering
- Feature flag handling

**Finding condition:** Emit a finding when rollback resolves a mutable artifact, cannot identify the prior version, or can restore application code without preserving required data/schema compatibility.

### CICD-010: Pipeline outcomes and deployment identity are observable

**Severity:** Medium  
**Category:** pipeline-observability  
**Applies when:** Pipeline automation builds or deploys the application.

**Evidence to inspect:**
- Artifact digest capture
- Commit and build identifiers
- Region and environment labels
- Test result publication
- Deployment annotations

**Finding condition:** Emit a finding when the deployed artifact, source revision, target environment, region, validation outcome, or rollback result cannot be reconstructed from pipeline evidence.

## Evaluation rules

- Evaluate effective stage and job behavior, not keyword presence.
- Follow local templates only when their repository path is available.
- Treat external template internals as `not_assessed`.
- Deduplicate with container-build and deployment findings by root cause.
- Do not infer that a pipeline executed successfully from its definition.
