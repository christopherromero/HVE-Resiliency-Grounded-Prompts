---
schema_version: "1.1.0"
document_type: assessment_domain_standard
standard_id: KUBERNETES-DEPLOYMENT-RESILIENCY
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

# Kubernetes Deployment Resiliency Standard

## Purpose

Evaluate repository-owned Kubernetes workload configuration for compatibility with the application's resilient runtime behavior. This standard does not assess the deployed AKS cluster, node pools, zones, networking, ingress controllers, or shared platform services.

## Controls

### K8S-DEPLOY-001: Readiness probes represent serving eligibility

**Severity:** Critical  
**Category:** traffic-eligibility  
**Applies when:** A workload receives traffic or performs readiness-gated work.

**Evidence to inspect:** Readiness probe path, port, thresholds, timing, application health groups.  
**Finding condition:** Emit a finding when readiness targets an incorrect endpoint, cannot reflect critical local dependency failure, or remains successful while the application cannot safely serve.

### K8S-DEPLOY-002: Liveness probes exclude external dependency health

**Severity:** Critical  
**Category:** liveness  
**Applies when:** A liveness probe is configured.

**Evidence to inspect:** Liveness path and application health-group composition.  
**Finding condition:** Emit a finding when external dependency failure can make liveness fail and create restart loops.

### K8S-DEPLOY-003: Startup probes bound slow initialization without masking permanent failure

**Severity:** High  
**Category:** startup  
**Applies when:** Startup may exceed normal liveness timing or a startup probe exists.

**Evidence to inspect:** Startup probe timing, application startup behavior, liveness activation.  
**Finding condition:** Emit a finding when startup is unbounded, liveness can kill valid initialization, or the startup probe permanently masks a failed application.

### K8S-DEPLOY-004: Termination permits readiness withdrawal and graceful drain

**Severity:** Critical  
**Category:** lifecycle  
**Applies when:** A service receives traffic or processes work.

**Evidence to inspect:** `terminationGracePeriodSeconds`, lifecycle hooks, application shutdown timeout, listener or scheduler termination behavior.  
**Finding condition:** Emit a finding when the pod can terminate before readiness withdrawal and bounded graceful completion, or when configured grace is inconsistent with application shutdown behavior.

### K8S-DEPLOY-005: Rolling update settings preserve serving capacity

**Severity:** High  
**Category:** rollout  
**Applies when:** A Deployment or StatefulSet uses rolling updates.

**Evidence to inspect:** `maxUnavailable`, `maxSurge`, replica count, readiness behavior, progress deadline.  
**Finding condition:** Emit a finding when repository-owned rollout settings can remove all serving replicas or promote an unhealthy revision without an explicit safe strategy.

### K8S-DEPLOY-006: Resource requests and limits are explicit and coherent

**Severity:** High  
**Category:** resource-governance  
**Applies when:** A workload manifest is repository-owned.

**Evidence to inspect:** CPU and memory requests/limits, JVM/container awareness, ephemeral storage.  
**Finding condition:** Emit a finding only when absent or contradictory resource boundaries have an evidenced availability impact. Do not invent numeric values.

### K8S-DEPLOY-007: Regional configuration is deployment-injected

**Severity:** Critical  
**Category:** regional-configuration  
**Applies when:** The same application is deployed to multiple regions.

**Evidence to inspect:** ConfigMaps, Secrets references, environment variables, values, command arguments.  
**Finding condition:** Emit a finding when regional endpoint or identity values are hardcoded into a shared manifest or require a different application image.

### K8S-DEPLOY-008: Workload ownership controls match the processing model

**Severity:** Critical  
**Category:** workload-ownership  
**Applies when:** Kafka consumers, schedulers, relays, pollers, or batch workloads must be single-active or role-controlled.

**Evidence to inspect:** Replicas, activation properties, regional values, leader/lease settings, consumer auto-start configuration.  
**Finding condition:** Emit a finding when deployment configuration activates concurrent owners contrary to the approved processing model or defaults unsafe when ownership input is absent.

### K8S-DEPLOY-009: Configuration references are fail-safe and explicit

**Severity:** High  
**Category:** configuration  
**Applies when:** Workloads reference ConfigMaps, Secrets, volumes, or external configuration.

**Evidence to inspect:** Optional references, missing-key behavior, defaults, mounted paths.  
**Finding condition:** Emit a finding when required resiliency configuration can be silently omitted or default to unsafe regional or ownership behavior.

### K8S-DEPLOY-010: Service and workload ports are consistent

**Severity:** High  
**Category:** service-routing  
**Applies when:** Service and workload manifests are repository-owned.

**Evidence to inspect:** Container ports, Service target ports, named ports, probe ports, management ports.  
**Finding condition:** Emit a finding when inconsistency can make traffic or health checks target the wrong application endpoint.

### K8S-DEPLOY-011: Disruption controls align with availability requirements

**Severity:** High  
**Category:** disruption  
**Applies when:** Repository-owned PodDisruptionBudget or equivalent workload availability settings exist.

**Evidence to inspect:** PDB selector, min/max availability, replicas, workload labels.  
**Finding condition:** Emit a finding when repository-owned disruption settings select the wrong pods, permit complete voluntary disruption, or make routine maintenance impossible. Missing platform-owned PDB evidence is `not_assessed` unless ownership is confirmed.

### K8S-DEPLOY-012: Placement intent does not create a false regional guarantee

**Severity:** Medium  
**Category:** placement  
**Applies when:** Affinity, anti-affinity, topology spread, or node selection is repository-owned.

**Evidence to inspect:** Selectors, topology keys, required/preferred rules, labels.  
**Finding condition:** Emit a finding when repository configuration contradicts the approved workload placement intent or can co-locate all replicas despite an explicit repository-owned distribution requirement. Do not assess actual node or zone availability.

## Evaluation rules

- Validate manifests against observed application ports, health paths, and lifecycle behavior.
- Missing externally owned workload settings are evidence gaps, not findings.
- Do not infer actual scheduling, traffic, or rollout state.
- Deduplicate lifecycle and health findings with the application master controls.### Architecture operating-model contract

Use `architecture_context.deployment_evolution.target` for the application deployment target and `architecture_context.shared_service_operating_models.services` for dependency-specific target models. Application active-active does not imply every consumer, scheduler, database, or shared service is multi-active. K8S-DEPLOY-008 must use each workload's approved processing or service model. Source-target differences are not findings without repository evidence.


