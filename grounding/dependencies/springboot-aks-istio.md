---
schema_version: 2.0.0
document_type: dependency_behavior
service: aks-istio
service_name: AKS with Istio
language: any
framework: spring-boot-or-containerized-service
runtime_platform: aks
assessment_scope: application_code_and_repository_owned_workload_configuration
lifecycle_status: active
assessment:
  enabled: true
  emit_findings: true
  include_in_score: true
  unknown_evidence_status: not_assessed
controls:
- id: AKS-ISTIO-001
  title: Readiness and liveness responsibilities are separated
  severity: critical
  category: health
  applies_when: HTTP-serving workloads expose Kubernetes probes
  evidence_patterns:
  - management.endpoint.health.probes.enabled
  - management.endpoint.health.group.readiness
  - management.endpoint.health.group.liveness
  - readinessProbe
  - livenessProbe
  finding_when: external dependency failure participates in liveness, readiness and
    liveness use an undifferentiated always-UP signal, or failure semantics cannot
    support traffic withdrawal
  emit_on_failure: true
- id: AKS-ISTIO-002
  title: Startup behavior is explicitly modeled
  severity: high
  category: lifecycle
  applies_when: application startup can exceed normal liveness thresholds
  evidence_patterns:
  - startupProbe
  - initialDelaySeconds
  - SpringApplication
  - startup dependency
  - fail-fast
  finding_when: fixed readiness or liveness delays substitute for startup semantics,
    or liveness can kill a slow but progressing startup
  emit_on_failure: true
- id: AKS-ISTIO-003
  title: Health checks represent the actual serving path
  severity: critical
  category: health
  applies_when: workload receives traffic or processes critical work
  evidence_patterns:
  - HealthIndicator
  - ReactiveHealthIndicator
  - dependency client
  - business readiness
  - exec ls
  finding_when: health reports UP while the critical serving path is unusable, or
    an exec/file-system check proves only that the container exists
  emit_on_failure: true
- id: AKS-ISTIO-004
  title: Required companion processes participate in health and lifecycle
  severity: high
  category: process-model
  applies_when: a container or pod relies on a required companion process or proxy
  evidence_patterns:
  - ProcessBuilder
  - supervisor
  - side process
  - local proxy
  - localhost port
  finding_when: a required companion can fail while readiness remains UP or termination
    signals do not coordinate all required processes
  emit_on_failure: true
- id: AKS-ISTIO-005
  title: Workload execution model determines regional failover behavior
  severity: critical
  category: workload-model
  applies_when: scheduled, batch, polling, event-consumer, or externally invoked work
    exists
  evidence_patterns:
  - '@Scheduled'
  - CommandLineRunner
  - ApplicationRunner
  - KafkaListener
  - kubectl exec
  finding_when: non-HTTP work is assumed to fail over through GLB traffic routing
    or both regions can independently initiate the same business operation
  emit_on_failure: true
- id: AKS-ISTIO-006
  title: Single-active workloads prevent split-brain execution
  severity: critical
  category: workload-ownership
  applies_when: exactly one region or instance must own scheduled or polling work
  evidence_patterns:
  - feature flag
  - lease
  - leader election
  - ShedLock
  - owner epoch
  finding_when: activation defaults enabled, relies only on a local flag, or cannot
    detect concurrent ownership
  emit_on_failure: true
- id: AKS-ISTIO-007
  title: Application and mesh timeout budgets are coordinated
  severity: critical
  category: traffic-management
  applies_when: outbound calls traverse Istio or another proxy
  evidence_patterns:
  - WebClient timeout
  - RestTemplate timeout
  - VirtualService timeout
  - DestinationRule
  - request deadline
  finding_when: application, mesh, gateway, and dependency deadlines are absent or
    ordered so an outer layer times out before the application can recover or report
    correctly
  emit_on_failure: true
- id: AKS-ISTIO-008
  title: Application and mesh retries do not amplify one another
  severity: critical
  category: traffic-management
  applies_when: application or mesh retries are enabled
  evidence_patterns:
  - retryWhen
  - '@Retryable'
  - VirtualService retries
  - attempts
  - perTryTimeout
  finding_when: stacked retries multiply attempts, exceed deadlines, or repeat non-idempotent
    effects
  emit_on_failure: true
- id: AKS-ISTIO-009
  title: Circuit breaking and connection limits isolate dependencies
  severity: high
  category: traffic-management
  applies_when: multiple remote dependencies or high concurrency exists
  evidence_patterns:
  - DestinationRule
  - outlierDetection
  - connectionPool
  - CircuitBreaker
  - Bulkhead
  finding_when: one dependency can exhaust shared threads, sockets, event loops, or
    connections, and neither application nor mesh provides evidenced isolation
  emit_on_failure: true
- id: AKS-ISTIO-010
  title: Istio host and application target contracts are consistent
  severity: critical
  category: egress-contract
  applies_when: repository includes Istio egress resources and application endpoint
    configuration
  evidence_patterns:
  - ServiceEntry hosts
  - VirtualService hosts
  - REGISTRY_ONLY
  - baseUrl
  - DNS name
  finding_when: the application target and repository-owned Istio host contract differ,
    or a physical IP prevents logical endpoint changes
  emit_on_failure: true
- id: AKS-ISTIO-011
  title: Sidecar startup and shutdown dependencies are validated
  severity: high
  category: lifecycle
  applies_when: the application requires the Istio proxy for startup or egress
  evidence_patterns:
  - holdApplicationUntilProxyStarts
  - proxy.istio.io/config
  - preStop
  - terminationDrainDuration
  finding_when: the application makes required calls before the proxy is available
    or exits before in-flight proxy traffic drains
  emit_on_failure: true
- id: AKS-ISTIO-012
  title: Graceful shutdown drains traffic and completes bounded in-flight work
  severity: critical
  category: lifecycle
  applies_when: workload receives requests or owns messages/jobs
  evidence_patterns:
  - server.shutdown
  - preStop
  - terminationGracePeriodSeconds
  - readiness transition
  finding_when: the pod continues accepting work during termination or loses in-flight
    requests, messages, or durable state transitions
  emit_on_failure: true
- id: AKS-ISTIO-013
  title: Regional identity and routing outcomes are observable
  severity: medium
  category: observability
  applies_when: telemetry is available
  evidence_patterns:
  - region tag
  - cluster tag
  - pod name
  - response flag
  - Envoy response flags
  finding_when: logs, metrics, traces, and health events cannot identify serving region,
    cluster, workload ownership, dependency, and proxy routing outcome
  emit_on_failure: true
- id: AKS-ISTIO-014
  title: Business throughput and stuck-work conditions are observable
  severity: high
  category: observability
  applies_when: batch, scheduler, event consumer, or reprocessor exists
  evidence_patterns:
  - last successful run
  - backlog age
  - consumer lag
  - items processed
  - active owner
  finding_when: pod health remains UP while business processing has stopped, ownership
    is ambiguous, or backlog and stuck work are invisible
  emit_on_failure: true
- id: AKS-ISTIO-015
  title: Fallback paths are independently bounded, durable, and observable
  severity: critical
  category: fallback
  applies_when: a primary dependency has a fallback
  evidence_patterns:
  - onErrorResume
  - fallback repository
  - secondary endpoint
  - dead-letter
  finding_when: fallback work is detached, unbounded, silent, or converts required
    failure to success without durable recovery state
  emit_on_failure: true
- id: AKS-ISTIO-016
  title: Repository-owned workload security avoids embedded credentials and sensitive
    telemetry
  severity: critical
  category: security
  applies_when: manifests, Helm, or application configuration are in scope
  evidence_patterns:
  - Secret
  - ConfigMap
  - env.value
  - Authorization
  - APIM key
  - PAN
  finding_when: credentials or protected data are committed, rendered into non-secret
    configuration, or logged through application or proxy diagnostics
  emit_on_failure: true
- id: AKS-ISTIO-017
  title: Repository-owned topology and disruption settings are evidence items, not
    assumed facts
  severity: high
  category: availability
  applies_when: Helm or Kubernetes manifests are present
  evidence_patterns:
  - replicas
  - HorizontalPodAutoscaler
  - PodDisruptionBudget
  - topologySpreadConstraints
  - podAntiAffinity
  finding_when: repository-owned manifests explicitly create a single-failure-domain
    or zero-availability configuration inconsistent with the stated workload requirement
  emit_on_failure: true
- id: AKS-ISTIO-018
  title: Fault tests cover proxy, dependency, pod, and ownership transitions
  severity: critical
  category: testing
  applies_when: workload depends on AKS or Istio behavior
  evidence_patterns:
  - fault injection
  - pod termination test
  - proxy unavailable
  - regional ownership test
  finding_when: tests do not prove timeout/retry coordination, readiness transition,
    graceful termination, proxy startup, and single-active or active-active behavior
  emit_on_failure: true
---

# AKS + Istio Application and Repository Behavior Standard

## Purpose

This standard evaluates application and repository-owned workload behavior for services running on AKS with Istio. It incorporates recurring findings from the reviewed OSPG and OCSE assessments, while preserving a strict boundary between application evidence and deployed platform state.

## Scope boundary

Assess application health semantics, workload execution model, ownership, lifecycle, timeout and retry coordination, repository-owned Istio/Kubernetes contracts, security-sensitive configuration, observability, and tests. Do not infer deployed AKS, network, or Istio topology from absent repository evidence.

## Evaluator workflow

- Confirm AKS/Istio or repository-owned workload configuration is applicable.
- Classify the workload as API, event consumer, scheduler, batch, externally triggered, or hybrid.
- Inspect application probes, lifecycle, client budgets, ownership, metrics, and repository-owned Helm/Kubernetes/Istio resources.
- Separate application findings from external platform evidence.
- Deduplicate findings with master and HTTP/dependency standards.
- Do not emit platform findings when deployed state is unavailable.

## Required statuses

- `compliant`: Repository evidence demonstrates the behavior.
- `non_compliant`: Repository evidence demonstrates a gap.
- `not_assessed`: Evidence is unavailable or insufficient.
- `not_applicable`: The dependency or behavior does not apply.
- `accepted_risk`: A cited approved exception exists.

## Dependency-specific quality caveats

- Istio can supply traffic management, security, and observability, but its presence does not prove retries, failover, health, or isolation are correctly configured.
- GLB or ingress routing does not fail over scheduled, polling, or externally triggered work.
- Feature flags alone do not guarantee single-active ownership.
- External dependencies never belong in liveness, and not every dependency belongs in readiness.
- Application and mesh retries must be evaluated together to prevent multiplicative retry storms.
- Do not prescribe numeric probe, retry, timeout, drain, HPA, or capacity settings without workload evidence.
- Repository absence means `not_assessed` for external cluster, mesh, DNS, certificate, or network state.

## Controls

### AKS-ISTIO-001: Readiness and liveness responsibilities are separated

**Severity:** Critical  
**Category:** health  
**Applies when:** HTTP-serving workloads expose Kubernetes probes

#### Requirement

The application must expose distinct bounded readiness and liveness signals. Readiness represents whether the instance can safely receive traffic; liveness represents whether the process is irrecoverably unhealthy. External dependencies must not participate in liveness.

#### Repository evidence to inspect

- `management.endpoint.health.probes.enabled`
- `management.endpoint.health.group.readiness`
- `management.endpoint.health.group.liveness`
- `readinessProbe`
- `livenessProbe`

#### Finding condition

Emit a finding when evidence shows that external dependency failure participates in liveness, readiness and liveness use an undifferentiated always-UP signal, or failure semantics cannot support traffic withdrawal.

#### Evidence rule

Cite the repository-relative file path, symbol or property, original assessed line range, and exact source excerpt when available. Evaluate effective behavior rather than the presence of an annotation, resource, library, or default alone. If evidence is unavailable or external, return `not_assessed` rather than assuming noncompliance.

#### Quality caveats

- Do not add every dependency to readiness. Include only evidenced critical region-local serving dependencies.
- A globally shared dependency in readiness can withdraw all regions simultaneously.

---

### AKS-ISTIO-002: Startup behavior is explicitly modeled

**Severity:** High  
**Category:** lifecycle  
**Applies when:** application startup can exceed normal liveness thresholds

#### Requirement

Repository-owned workload configuration must distinguish startup from steady-state health so initialization, sidecar readiness, migrations, and bounded dependency startup do not trigger an avoidable restart loop.

#### Repository evidence to inspect

- `startupProbe`
- `initialDelaySeconds`
- `SpringApplication`
- `startup dependency`
- `fail-fast`

#### Finding condition

Emit a finding when evidence shows that fixed readiness or liveness delays substitute for startup semantics, or liveness can kill a slow but progressing startup.

#### Evidence rule

Cite the repository-relative file path, symbol or property, original assessed line range, and exact source excerpt when available. Evaluate effective behavior rather than the presence of an annotation, resource, library, or default alone. If evidence is unavailable or external, return `not_assessed` rather than assuming noncompliance.

#### Quality caveats

- Do not prescribe probe timings without measured startup evidence.
- Missing deployed probe configuration is `not_assessed` when manifests are external.

---

### AKS-ISTIO-003: Health checks represent the actual serving path

**Severity:** Critical  
**Category:** health  
**Applies when:** workload receives traffic or processes critical work

#### Requirement

Readiness checks must represent the critical application path with bounded, side-effect-free checks or cached dependency state. Batch workloads require business-progress signals in addition to process health.

#### Repository evidence to inspect

- `HealthIndicator`
- `ReactiveHealthIndicator`
- `dependency client`
- `business readiness`
- `exec ls`

#### Finding condition

Emit a finding when evidence shows that health reports UP while the critical serving path is unusable, or an exec/file-system check proves only that the container exists.

#### Evidence rule

Cite the repository-relative file path, symbol or property, original assessed line range, and exact source excerpt when available. Evaluate effective behavior rather than the presence of an annotation, resource, library, or default alone. If evidence is unavailable or external, return `not_assessed` rather than assuming noncompliance.

#### Quality caveats

- Health checks must not create costly or mutating dependency traffic.
- Use cached state when a direct check would overload a dependency.

---

### AKS-ISTIO-004: Required companion processes participate in health and lifecycle

**Severity:** High  
**Category:** process-model  
**Applies when:** a container or pod relies on a required companion process or proxy

#### Requirement

Every required local process must be represented in readiness and shutdown behavior, or be separated into an independently managed container with an explicit dependency contract.

#### Repository evidence to inspect

- `ProcessBuilder`
- `supervisor`
- `side process`
- `local proxy`
- `localhost port`

#### Finding condition

Emit a finding when evidence shows that a required companion can fail while readiness remains UP or termination signals do not coordinate all required processes.

#### Evidence rule

Cite the repository-relative file path, symbol or property, original assessed line range, and exact source excerpt when available. Evaluate effective behavior rather than the presence of an annotation, resource, library, or default alone. If evidence is unavailable or external, return `not_assessed` rather than assuming noncompliance.

#### Quality caveats

- Do not infer a companion process merely from an Istio sidecar. Apply only when the application depends on that local process.

---

### AKS-ISTIO-005: Workload execution model determines regional failover behavior

**Severity:** Critical  
**Category:** workload-model  
**Applies when:** scheduled, batch, polling, event-consumer, or externally invoked work exists

#### Requirement

Classify each workload as request-driven, event-driven, scheduled, externally triggered, or hybrid. Define single-active or multi-active behavior based on how work is acquired, not on HTTP traffic routing.

#### Repository evidence to inspect

- `@Scheduled`
- `CommandLineRunner`
- `ApplicationRunner`
- `KafkaListener`
- `kubectl exec`

#### Finding condition

Emit a finding when evidence shows that non-HTTP work is assumed to fail over through GLB traffic routing or both regions can independently initiate the same business operation.

#### Evidence rule

Cite the repository-relative file path, symbol or property, original assessed line range, and exact source excerpt when available. Evaluate effective behavior rather than the presence of an annotation, resource, library, or default alone. If evidence is unavailable or external, return `not_assessed` rather than assuming noncompliance.

#### Quality caveats

- GLB can route inbound traffic but cannot transfer timer, polling, or batch ownership.
- A workload can contain API and scheduler variants that require different failover models.

---

### AKS-ISTIO-006: Single-active workloads prevent split-brain execution

**Severity:** Critical  
**Category:** workload-ownership  
**Applies when:** exactly one region or instance must own scheduled or polling work

#### Requirement

Single-active work must use fail-safe activation, observable ownership, and an atomic lease, leader-election, or equivalent ownership mechanism when concurrent activation is possible.

#### Repository evidence to inspect

- `feature flag`
- `lease`
- `leader election`
- `ShedLock`
- `owner epoch`

#### Finding condition

Emit a finding when evidence shows that activation defaults enabled, relies only on a local flag, or cannot detect concurrent ownership.

#### Evidence rule

Cite the repository-relative file path, symbol or property, original assessed line range, and exact source excerpt when available. Evaluate effective behavior rather than the presence of an annotation, resource, library, or default alone. If evidence is unavailable or external, return `not_assessed` rather than assuming noncompliance.

#### Quality caveats

- A feature flag alone is not a distributed single-active guarantee.
- Both-enabled and both-disabled states must be tested and alerted.

---

### AKS-ISTIO-007: Application and mesh timeout budgets are coordinated

**Severity:** Critical  
**Category:** traffic-management  
**Applies when:** outbound calls traverse Istio or another proxy

#### Requirement

Application timeout, retry, and circuit-breaker budgets must be externally configurable and coordinated with ingress, sidecar, gateway, and dependency deadlines.

#### Repository evidence to inspect

- `WebClient timeout`
- `RestTemplate timeout`
- `VirtualService timeout`
- `DestinationRule`
- `request deadline`

#### Finding condition

Emit a finding when evidence shows that application, mesh, gateway, and dependency deadlines are absent or ordered so an outer layer times out before the application can recover or report correctly.

#### Evidence rule

Cite the repository-relative file path, symbol or property, original assessed line range, and exact source excerpt when available. Evaluate effective behavior rather than the presence of an annotation, resource, library, or default alone. If evidence is unavailable or external, return `not_assessed` rather than assuming noncompliance.

#### Quality caveats

- Do not prescribe numeric values without measured budgets.
- Repository evidence cannot prove effective cluster mesh policy when that policy is external.

---

### AKS-ISTIO-008: Application and mesh retries do not amplify one another

**Severity:** Critical  
**Category:** traffic-management  
**Applies when:** application or mesh retries are enabled

#### Requirement

Define one accountable retry strategy per operation. When application and mesh retries coexist, cap their combined attempts and duration and protect non-idempotent work with stable identity or reconciliation.

#### Repository evidence to inspect

- `retryWhen`
- `@Retryable`
- `VirtualService retries`
- `attempts`
- `perTryTimeout`

#### Finding condition

Emit a finding when evidence shows that stacked retries multiply attempts, exceed deadlines, or repeat non-idempotent effects.

#### Evidence rule

Cite the repository-relative file path, symbol or property, original assessed line range, and exact source excerpt when available. Evaluate effective behavior rather than the presence of an annotation, resource, library, or default alone. If evidence is unavailable or external, return `not_assessed` rather than assuming noncompliance.

#### Quality caveats

- Do not retry an ambiguous charge, capture, refund, or database commit blindly.
- A random UUID per attempt is not an idempotency key.

---

### AKS-ISTIO-009: Circuit breaking and connection limits isolate dependencies

**Severity:** High  
**Category:** traffic-management  
**Applies when:** multiple remote dependencies or high concurrency exists

#### Requirement

Material dependencies must have bounded concurrency and failure isolation at an appropriate layer, with telemetry that identifies which layer opened or rejected work.

#### Repository evidence to inspect

- `DestinationRule`
- `outlierDetection`
- `connectionPool`
- `CircuitBreaker`
- `Bulkhead`

#### Finding condition

Emit a finding when evidence shows that one dependency can exhaust shared threads, sockets, event loops, or connections, and neither application nor mesh provides evidenced isolation.

#### Evidence rule

Cite the repository-relative file path, symbol or property, original assessed line range, and exact source excerpt when available. Evaluate effective behavior rather than the presence of an annotation, resource, library, or default alone. If evidence is unavailable or external, return `not_assessed` rather than assuming noncompliance.

#### Quality caveats

- Do not claim an absent DestinationRule when Istio configuration is external. Evaluate application isolation independently.

---

### AKS-ISTIO-010: Istio host and application target contracts are consistent

**Severity:** Critical  
**Category:** egress-contract  
**Applies when:** repository includes Istio egress resources and application endpoint configuration

#### Requirement

Repository-owned application endpoints and Istio host declarations must use matching logical DNS identities and remain region-selectable without source changes.

#### Repository evidence to inspect

- `ServiceEntry hosts`
- `VirtualService hosts`
- `REGISTRY_ONLY`
- `baseUrl`
- `DNS name`

#### Finding condition

Emit a finding when evidence shows that the application target and repository-owned Istio host contract differ, or a physical IP prevents logical endpoint changes.

#### Evidence rule

Cite the repository-relative file path, symbol or property, original assessed line range, and exact source excerpt when available. Evaluate effective behavior rather than the presence of an annotation, resource, library, or default alone. If evidence is unavailable or external, return `not_assessed` rather than assuming noncompliance.

#### Quality caveats

- Static IP, DNS, private endpoint, and deployed egress-policy correctness are infrastructure concerns unless repository-owned evidence proves the mismatch.

---

### AKS-ISTIO-011: Sidecar startup and shutdown dependencies are validated

**Severity:** High  
**Category:** lifecycle  
**Applies when:** the application requires the Istio proxy for startup or egress

#### Requirement

When application correctness depends on the proxy, startup and termination behavior must be explicitly coordinated and tested using supported add-on configuration and workload lifecycle hooks.

#### Repository evidence to inspect

- `holdApplicationUntilProxyStarts`
- `proxy.istio.io/config`
- `preStop`
- `terminationDrainDuration`

#### Finding condition

Emit a finding when evidence shows that the application makes required calls before the proxy is available or exits before in-flight proxy traffic drains.

#### Evidence rule

Cite the repository-relative file path, symbol or property, original assessed line range, and exact source excerpt when available. Evaluate effective behavior rather than the presence of an annotation, resource, library, or default alone. If evidence is unavailable or external, return `not_assessed` rather than assuming noncompliance.

#### Quality caveats

- Do not modify the managed Istio default ConfigMap directly; use supported configuration surfaces.
- Do not assume sidecar ordering without evidence.

---

### AKS-ISTIO-012: Graceful shutdown drains traffic and completes bounded in-flight work

**Severity:** Critical  
**Category:** lifecycle  
**Applies when:** workload receives requests or owns messages/jobs

#### Requirement

On termination, the instance must become not ready, stop acquiring new work, finish or safely abandon in-flight work within a configured budget, and allow the proxy to drain.

#### Repository evidence to inspect

- `server.shutdown`
- `preStop`
- `terminationGracePeriodSeconds`
- `readiness transition`

#### Finding condition

Emit a finding when evidence shows that the pod continues accepting work during termination or loses in-flight requests, messages, or durable state transitions.

#### Evidence rule

Cite the repository-relative file path, symbol or property, original assessed line range, and exact source excerpt when available. Evaluate effective behavior rather than the presence of an annotation, resource, library, or default alone. If evidence is unavailable or external, return `not_assessed` rather than assuming noncompliance.

#### Quality caveats

- Termination budgets must reflect application and proxy drain behavior.
- Event consumers must coordinate offset or checkpoint completion.

---

### AKS-ISTIO-013: Regional identity and routing outcomes are observable

**Severity:** Medium  
**Category:** observability  
**Applies when:** telemetry is available

#### Requirement

Telemetry must include safe application, region, cluster, workload-role, and dependency dimensions and preserve correlation across proxy and application spans.

#### Repository evidence to inspect

- `region tag`
- `cluster tag`
- `pod name`
- `response flag`
- `Envoy response flags`

#### Finding condition

Emit a finding when evidence shows that logs, metrics, traces, and health events cannot identify serving region, cluster, workload ownership, dependency, and proxy routing outcome.

#### Evidence rule

Cite the repository-relative file path, symbol or property, original assessed line range, and exact source excerpt when available. Evaluate effective behavior rather than the presence of an annotation, resource, library, or default alone. If evidence is unavailable or external, return `not_assessed` rather than assuming noncompliance.

#### Quality caveats

- Avoid unbounded-cardinality labels.
- Do not log secrets or protected request bodies.

---

### AKS-ISTIO-014: Business throughput and stuck-work conditions are observable

**Severity:** High  
**Category:** observability  
**Applies when:** batch, scheduler, event consumer, or reprocessor exists

#### Requirement

Expose application metrics for last success, throughput, backlog age, failures, retries, active ownership, and terminally stuck work.

#### Repository evidence to inspect

- `last successful run`
- `backlog age`
- `consumer lag`
- `items processed`
- `active owner`

#### Finding condition

Emit a finding when evidence shows that pod health remains UP while business processing has stopped, ownership is ambiguous, or backlog and stuck work are invisible.

#### Evidence rule

Cite the repository-relative file path, symbol or property, original assessed line range, and exact source excerpt when available. Evaluate effective behavior rather than the presence of an annotation, resource, library, or default alone. If evidence is unavailable or external, return `not_assessed` rather than assuming noncompliance.

#### Quality caveats

- Process health is not sufficient for non-HTTP workloads.

---

### AKS-ISTIO-015: Fallback paths are independently bounded, durable, and observable

**Severity:** Critical  
**Category:** fallback  
**Applies when:** a primary dependency has a fallback

#### Requirement

Measure and validate primary failure, fallback success, and dual failure separately. Persist recovery intent before returning synthetic or deferred success.

#### Repository evidence to inspect

- `onErrorResume`
- `fallback repository`
- `secondary endpoint`
- `dead-letter`

#### Finding condition

Emit a finding when evidence shows that fallback work is detached, unbounded, silent, or converts required failure to success without durable recovery state.

#### Evidence rule

Cite the repository-relative file path, symbol or property, original assessed line range, and exact source excerpt when available. Evaluate effective behavior rather than the presence of an annotation, resource, library, or default alone. If evidence is unavailable or external, return `not_assessed` rather than assuming noncompliance.

#### Quality caveats

- A fallback is not resilient merely because it uses another store or endpoint.

---

### AKS-ISTIO-016: Repository-owned workload security avoids embedded credentials and sensitive telemetry

**Severity:** Critical  
**Category:** security  
**Applies when:** manifests, Helm, or application configuration are in scope

#### Requirement

Repository-owned configuration must reference approved secret delivery and application/proxy diagnostics must sanitize credentials, tokens, signed headers, PCI, and PII.

#### Repository evidence to inspect

- `Secret`
- `ConfigMap`
- `env.value`
- `Authorization`
- `APIM key`
- `PAN`

#### Finding condition

Emit a finding when evidence shows that credentials or protected data are committed, rendered into non-secret configuration, or logged through application or proxy diagnostics.

#### Evidence rule

Cite the repository-relative file path, symbol or property, original assessed line range, and exact source excerpt when available. Evaluate effective behavior rather than the presence of an annotation, resource, library, or default alone. If evidence is unavailable or external, return `not_assessed` rather than assuming noncompliance.

#### Quality caveats

- Do not infer deployed secret synchronization or workload identity from missing repository evidence.

---

### AKS-ISTIO-017: Repository-owned topology and disruption settings are evidence items, not assumed facts

**Severity:** High  
**Category:** availability  
**Applies when:** Helm or Kubernetes manifests are present

#### Requirement

When these manifests are in scope, report the explicit repository behavior and required application availability outcome. Otherwise record external evidence required.

#### Repository evidence to inspect

- `replicas`
- `HorizontalPodAutoscaler`
- `PodDisruptionBudget`
- `topologySpreadConstraints`
- `podAntiAffinity`

#### Finding condition

Emit a finding when evidence shows that repository-owned manifests explicitly create a single-failure-domain or zero-availability configuration inconsistent with the stated workload requirement.

#### Evidence rule

Cite the repository-relative file path, symbol or property, original assessed line range, and exact source excerpt when available. Evaluate effective behavior rather than the presence of an annotation, resource, library, or default alone. If evidence is unavailable or external, return `not_assessed` rather than assuming noncompliance.

#### Quality caveats

- Do not infer deployed replica counts, zones, capacity, or PDB state from absent manifests.

---

### AKS-ISTIO-018: Fault tests cover proxy, dependency, pod, and ownership transitions

**Severity:** Critical  
**Category:** testing  
**Applies when:** workload depends on AKS or Istio behavior

#### Requirement

Automated or repeatable validation must cover dependency latency/failure, proxy unavailability, pod termination, recovery, ownership conflict, and traffic eligibility.

#### Repository evidence to inspect

- `fault injection`
- `pod termination test`
- `proxy unavailable`
- `regional ownership test`

#### Finding condition

Emit a finding when evidence shows that tests do not prove timeout/retry coordination, readiness transition, graceful termination, proxy startup, and single-active or active-active behavior.

#### Evidence rule

Cite the repository-relative file path, symbol or property, original assessed line range, and exact source excerpt when available. Evaluate effective behavior rather than the presence of an annotation, resource, library, or default alone. If evidence is unavailable or external, return `not_assessed` rather than assuming noncompliance.

#### Quality caveats

- Tests may simulate platform behavior without treating infrastructure provisioning as application code.

---

## Standard finding format

- **Title:** [specific evidence-based gap]
- **Control:** [control ID]
- **Related controls:** [control IDs]
- **Severity:** [severity]
- **Repository evidence:** [file, symbol/property, original lines, exact excerpt]
- **Observed behavior:** [effective current behavior]
- **Regional or operational risk:** [failure effect]
- **Required code/configuration change:** [specific remediation]
- **Validation test:** [test proving behavior]
- **Confidence:** [high, medium, low]

## Non-findings

- Missing AKS cluster, regional cluster, private endpoint, DNS, VNet, firewall, gateway, certificate, or deployed Istio control-plane resources.
- ACR geo-replication, node-zone placement, deployed HPA/PDB state, or capacity unless explicitly represented in repository-owned configuration.
- Global load-balancer deployment or health-probe configuration when external to the repository.
- PCF migration, modernization, cleanup, or findings.
