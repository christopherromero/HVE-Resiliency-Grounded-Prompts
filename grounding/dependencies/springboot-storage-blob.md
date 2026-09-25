---
schema_version: 2.2.0
document_type: dependency_behavior
service: storage-blob
service_name: Azure Blob Storage
language: java
framework: spring-boot
runtime_platform: aks
assessment_scope: application_code_only
lifecycle_status: active
assessment:
  enabled: true
  emit_findings: true
  include_in_score: true
  unknown_evidence_status: not_assessed
infrastructure_assumptions:
- Two independent Azure regions are provisioned and active.
- AKS, networking, private endpoints, DNS, identities, certificates, and dependent services follow the
  approved active-active infrastructure design.
- The deployment pipeline injects region-specific configuration into the same application artifact.
- The application repository does not provision or validate infrastructure.
controls:
- id: BLOB-001
  title: Storage endpoint or account is deployment-injected
  severity: critical
  category: configuration
  evidence_patterns:
  - spring.cloud.azure.storage
  - BlobServiceClientBuilder
  - STORAGE_ACCOUNT
  finding_when: account or endpoint is hardcoded
  emit_on_failure: true
  business_logic_risk: low
  requires_approval_before_implementation: false
  approval_owner: architecture
  safe_remediation_without_approval:
  - Externalize an existing hardcoded value to configuration while preserving the same effective default.
  - Add or improve metrics, logs, traces, and health details without changing decisions or payload content.
  - Add tests that characterize and lock in current behavior.
  requires_approval_for:
  - Changing the effective storage account or endpoint.
- id: BLOB-002
  title: Client timeout and retry policies are bounded
  severity: high
  category: resilience
  evidence_patterns:
  - RequestRetryOptions
  - ClientOptions
  - responseTimeout
  finding_when: blob operations lack bounded retry or timeout
  emit_on_failure: true
  business_logic_risk: moderate
  requires_approval_before_implementation: false
  approval_owner: architecture
  safe_remediation_without_approval:
  - Add operation-duration and retry telemetry.
  - Add tests that demonstrate the current behavior and the failure mode.
  requires_approval_for:
  - Reducing timeouts below observed successful transfer duration.
- id: BLOB-003
  title: Write operations are idempotent and concurrency-safe
  severity: critical
  category: consistency
  evidence_patterns:
  - ETag
  - BlobRequestConditions
  - overwrite flag
  - idempotency key
  finding_when: retry or concurrent write can overwrite or duplicate data unexpectedly
  emit_on_failure: true
  business_logic_risk: severe
  requires_approval_before_implementation: true
  approval_owner: product_and_data
  safe_remediation_without_approval:
  - Add ETag and overwrite telemetry.
  - Add tests that demonstrate the current behavior and the failure mode.
  requires_approval_for:
  - Adding or changing conditional-write behavior that determines which writes succeed.
  - Changing overwrite semantics.
- id: BLOB-004
  title: Application does not store durable state on pod-local storage
  severity: critical
  category: state
  evidence_patterns:
  - java.io
  - Files.write
  - /tmp
  - emptyDir
  finding_when: durable business state is written only to container or node filesystem
  emit_on_failure: true
  business_logic_risk: severe
  requires_approval_before_implementation: true
  approval_owner: architecture_and_product
  safe_remediation_without_approval:
  - Add local-write telemetry.
  - Add tests that demonstrate the current behavior and the failure mode.
  requires_approval_for:
  - Relocating durable state, which changes persistence and recovery behavior.
- id: BLOB-005
  title: Critical storage failure affects readiness only when service cannot operate
  severity: high
  category: health
  evidence_patterns:
  - storage HealthIndicator
  - readiness group
  finding_when: readiness does not reflect critical storage loss or treats optional storage as fatal
  emit_on_failure: true
  business_logic_risk: severe
  requires_approval_before_implementation: true
  approval_owner: architecture_and_product
  safe_remediation_without_approval:
  - Add dependency-state telemetry.
  - Add tests that demonstrate the current behavior and the failure mode.
  requires_approval_for:
  - Adding storage to readiness.
- id: BLOB-006
  title: Downloads and uploads stream data and bound memory usage
  severity: high
  category: performance
  evidence_patterns:
  - stream
  - Flux<ByteBuffer>
  - block size
  finding_when: large blob operation loads unbounded content into JVM memory
  emit_on_failure: true
  business_logic_risk: moderate
  requires_approval_before_implementation: false
  approval_owner: architecture
  safe_remediation_without_approval:
  - Add transfer-size and memory telemetry.
  - Add tests that demonstrate the current behavior and the failure mode.
  requires_approval_for:
  - Changing transfer behavior where partial-content handling or resumability changes.
- id: BLOB-007
  title: Recovery handles DNS, private endpoint, authentication, and client reconnection
  severity: high
  category: recovery
  evidence_patterns:
  - credential refresh
  - connection recovery
  finding_when: application requires restart after storage recovery
  emit_on_failure: true
  business_logic_risk: moderate
  requires_approval_before_implementation: false
  approval_owner: architecture
  safe_remediation_without_approval:
  - Add recovery telemetry.
  - Add tests that demonstrate the current behavior and the failure mode.
  requires_approval_for:
  - Changing client recovery behavior that alters endpoint selection.
- id: BLOB-008
  title: Tests cover timeout, conflict, partial transfer, retry, and recovery
  severity: high
  category: testing
  evidence_patterns:
  - Azurite
  - mock BlobClient
  - fault injection
  finding_when: storage failure behaviors are untested
  emit_on_failure: true
  business_logic_risk: none
  requires_approval_before_implementation: false
  approval_owner: none
  safe_remediation_without_approval:
  - Add tests that demonstrate the current behavior and the failure mode.
  requires_approval_for: []
- id: BLOB-009
  title: Credentials use approved identity and least-privilege delegation
  severity: critical
  category: security
  evidence_patterns:
  - DefaultAzureCredential
  - managed identity
  - account key
  - SAS permissions
  - expiry
  finding_when: account keys are embedded, SAS tokens are overly permissive or long-lived, or credential
    rotation requires restart without an approved contract
  emit_on_failure: true
  business_logic_risk: severe
  requires_approval_before_implementation: true
  approval_owner: security
  safe_remediation_without_approval:
  - Add credential-failure telemetry with values redacted.
  - Add tests that demonstrate the current behavior and the failure mode.
  requires_approval_for:
  - Changing credential type, SAS scope, or expiry.
- id: BLOB-010
  title: Signed URLs and tokens are never logged or persisted unsafely
  severity: critical
  category: security
  evidence_patterns:
  - blob url
  - sig=
  - SAS token
  - log url
  finding_when: URLs containing signatures or tokens are logged, stored, or returned where they can be
    reused
  emit_on_failure: true
  business_logic_risk: low
  requires_approval_before_implementation: false
  approval_owner: security
  safe_remediation_without_approval:
  - Add or strengthen URL and token redaction.
  - Add or improve metrics, logs, traces, and health details without changing decisions or payload content.
  - Add tests that characterize and lock in current behavior.
  requires_approval_for:
  - Weakening existing redaction.
- id: BLOB-011
  title: Large transfers use bounded chunking, parallelism, and safe retry
  severity: high
  category: performance
  evidence_patterns:
  - ParallelTransferOptions
  - block size
  - maxConcurrency
  - stage block
  finding_when: large transfers are unbounded, unresumable, or retried in a way that corrupts or duplicates
    content
  emit_on_failure: true
  business_logic_risk: moderate
  requires_approval_before_implementation: false
  approval_owner: architecture
  safe_remediation_without_approval:
  - Add transfer-progress and retry telemetry.
  - Add tests that demonstrate the current behavior and the failure mode.
  requires_approval_for:
  - Changing chunking or parallelism where transfer integrity, ordering, or resumability changes.
- id: BLOB-012
  title: Data integrity is verified for critical transfers
  severity: high
  category: data-correctness
  evidence_patterns:
  - Content-MD5
  - contentHash
  - checksum
  - verify
  finding_when: critical uploads or downloads complete without integrity verification when corruption
    or truncation would be business-affecting
  emit_on_failure: true
  business_logic_risk: severe
  requires_approval_before_implementation: true
  approval_owner: product_and_data
  safe_remediation_without_approval:
  - Add integrity-verification telemetry in report-only mode.
  - Add tests that demonstrate the current behavior and the failure mode.
  requires_approval_for:
  - Enforcing integrity checks that can reject transfers the application currently accepts.
- id: BLOB-013
  title: Blob naming and prefix strategy avoids collisions and hotspots
  severity: medium
  category: data-model
  evidence_patterns:
  - blob name
  - prefix
  - path pattern
  - timestamp key
  finding_when: naming can collide across instances or concentrate load on a narrow key range
  emit_on_failure: true
  business_logic_risk: severe
  requires_approval_before_implementation: true
  approval_owner: partner_contract_and_data
  safe_remediation_without_approval: &id001
  - Add or improve metrics, logs, traces, and health details without changing decisions or payload content.
  - Add tests that characterize and lock in current behavior.
  requires_approval_for:
  - Changing blob naming, prefixes, or path structure that downstream consumers depend on.
- id: BLOB-014
  title: Versioning, soft delete, and immutability assumptions are explicit
  severity: high
  category: data-model
  evidence_patterns:
  - versioning
  - soft delete
  - immutability
  - overwrite
  finding_when: business correctness depends on version retention, deletion recovery, or immutability
    behavior that the application does not explicitly establish
  emit_on_failure: true
  business_logic_risk: severe
  requires_approval_before_implementation: true
  approval_owner: data_and_product
  safe_remediation_without_approval: *id001
  requires_approval_for:
  - Changing versioning, soft-delete, immutability, or overwrite assumptions.
- id: BLOB-015
  title: Blob leases used for coordination are bounded and fenced
  severity: critical
  category: coordination
  evidence_patterns:
  - acquireLease
  - lease duration
  - renew
  - lease id
  finding_when: leases are acquired without bounded duration, renewal, ownership validation, or safe expiry
    behavior
  emit_on_failure: true
  business_logic_risk: severe
  requires_approval_before_implementation: true
  approval_owner: architecture_and_product
  safe_remediation_without_approval:
  - Add lease-acquisition, renewal, and expiry telemetry.
  - Add tests that demonstrate the current behavior and the failure mode.
  requires_approval_for:
  - Changing lease duration, renewal, or fencing behavior that determines which instance performs work.
- id: BLOB-016
  title: Secondary-endpoint read behavior and staleness are explicit
  severity: high
  category: consistency
  evidence_patterns:
  - secondary endpoint
  - -secondary
  - RA-GRS
  - stale read
  finding_when: reads can silently fall back to a secondary endpoint where staleness would be business-affecting
  emit_on_failure: true
  business_logic_risk: severe
  requires_approval_before_implementation: true
  approval_owner: data_and_product
  safe_remediation_without_approval:
  - Add secondary-read and staleness telemetry.
  - Add tests that demonstrate the current behavior and the failure mode.
  requires_approval_for:
  - Enabling or disabling secondary-endpoint reads, which changes data freshness callers observe.
- id: BLOB-017
  title: Clients are reused with explicit lifecycle and bounded resources
  severity: high
  category: resource-management
  evidence_patterns:
  - BlobServiceClient
  - singleton
  - close
  - http client reuse
  finding_when: clients are created per request or per operation, or client resources are unbounded
  emit_on_failure: true
  business_logic_risk: low
  requires_approval_before_implementation: false
  approval_owner: architecture
  safe_remediation_without_approval:
  - Convert per-request client creation to a managed singleton preserving identical configuration.
  - Add or improve metrics, logs, traces, and health details without changing decisions or payload content.
  - Add tests that characterize and lock in current behavior.
  requires_approval_for:
  - Changing effective client configuration.
- id: BLOB-018
  title: Batch and parallel operations handle partial failure
  severity: high
  category: consistency
  evidence_patterns:
  - batch
  - deleteBlobs
  - bulk
  - partial failure
  finding_when: batch or parallel operations ignore per-item results or treat partial success as full
    success
  emit_on_failure: true
  business_logic_risk: moderate
  requires_approval_before_implementation: false
  approval_owner: product
  safe_remediation_without_approval:
  - Add per-item batch outcome telemetry.
  - Add tests that demonstrate the current behavior and the failure mode.
  requires_approval_for:
  - Changing batch failure handling where partial success is currently accepted.
- id: BLOB-019
  title: Content metadata and type handling are explicit
  severity: medium
  category: contract
  evidence_patterns:
  - contentType
  - metadata
  - tags
  - encoding
  finding_when: content type, metadata, or tags are assumed rather than set explicitly where downstream
    behavior depends on them
  emit_on_failure: true
  business_logic_risk: severe
  requires_approval_before_implementation: true
  approval_owner: partner_contract
  safe_remediation_without_approval: *id001
  requires_approval_for:
  - Changing content type, metadata, tags, or encoding that downstream consumers depend on.
- id: BLOB-020
  title: Temporary and intermediate blob cleanup is defined
  severity: medium
  category: lifecycle
  evidence_patterns:
  - temp blob
  - cleanup
  - orphan
  - retention
  finding_when: temporary or failed-transfer blobs accumulate without a defined cleanup or retention contract
  emit_on_failure: true
  business_logic_risk: severe
  requires_approval_before_implementation: true
  approval_owner: data_and_product
  safe_remediation_without_approval:
  - Add orphan-blob telemetry.
  - Add tests that demonstrate the current behavior and the failure mode.
  requires_approval_for:
  - Introducing deletion or retention behavior.
business_logic_risk_classification:
  enabled: true
  levels:
  - none
  - low
  - moderate
  - severe
  severe_requires_approval: true
  risk_never_suppresses_findings: true
---

# Azure Blob Storage Target-State Application Behavior Standard

### Shared-service operating-model contract

This standard does not select the application's shared-service topology. Resolve the operating model from:

```text
architecture_context.shared_service_operating_models.services.storage_blob
```

Use `source.operating_model` only to describe current state. Use `target.operating_model` for control applicability and target-state code-readiness assessment.

- Evaluate common client controls whenever production use is confirmed.
- Evaluate model-specific controls only for the resolved target operating model.
- `not_applicable` plus no repository production use makes this standard not applicable.
- `not_applicable` plus confirmed repository production use is a context conflict, not an automatic code finding.
- Missing, unresolved, or conflicting target model makes model-specific controls `not_assessed` and routes to architecture review.
- A source-target difference is migration context, not a finding by itself.
- Findings require repository-owned evidence that the application is incompatible with an applicable target-state control.
- Do not infer deployed topology from this standard's title, examples, or assumptions.

## Purpose

This dependency-specific standard assesses how a Spring Boot microservice uses Azure Blob Storage when evaluated for the approved target operating model supplied by application architecture context. The local regional service endpoint is assumed to exist and be reachable through the approved private networking design.

## Scope boundary

This standard assesses **application code, application configuration checked into the repository, and automated tests only**. It does not assess whether Azure or third-party infrastructure has been deployed correctly.

## Mandatory assumptions

- Two independent Azure regions are provisioned and active.
- AKS, networking, private endpoints, DNS, identities, certificates, and dependent services follow the approved active-active infrastructure design.
- The deployment pipeline injects region-specific configuration into the same application artifact.
- The application repository does not provision or validate infrastructure.

## Evaluator workflow

- Confirm the dependency is actually used by production code.
- Resolve source and target models from `architecture_context.shared_service_operating_models.services.storage_blob` before evaluating model-specific controls.
- Locate client construction, configuration binding, error handling, health integration, telemetry, and tests.
- Evaluate only controls supported by repository evidence.
- Separate framework defaults from explicit application behavior. Flag reliance on a default only when the assessment requires explicit configuration or the default does not meet the failure budget.
- Do not recommend deploying infrastructure. Recommend application code, configuration contract, health behavior, telemetry, or testing changes.
- Link each finding to exactly one primary control and list related controls separately.
- Do not emit a finding for a dependency that is not used.
- Record each finding's `business_logic_risk`, `requires_approval_before_implementation`, and `approval_owner` so Step 3A can set the change boundary correctly.
- A `severe` control may produce a finding, but its behavior-changing remediation must be classified `approval_required: true` and blocked from Step 4 until approval is recorded.

## Required statuses

- `compliant`: Repository evidence demonstrates the behavior.
- `non_compliant`: Repository evidence demonstrates a gap.
- `not_assessed`: Evidence is unavailable or insufficient.
- `not_applicable`: The dependency or behavior does not apply.
- `accepted_risk`: A cited approved exception exists.

## Evidence and locator rules

Use this source-locator precedence: repository path, symbol or configuration key, exact original source excerpt, source fingerprint, assessment snapshot, and original assessed line range. Line numbers are advisory navigation metadata and may drift. Do not require a Git repository or commit SHA to record evidence.

## Global quality caveats

- Resiliency remediation must preserve existing business semantics, partner-contract interpretation, security controls, and privacy behavior unless an approved decision authorizes a change.
- Do not retry a non-idempotent operation after an ambiguous outcome unless stable identity, status lookup, or reconciliation makes replay safe.
- A random identifier generated per attempt is correlation, not idempotency.
- Do not add every dependency to readiness, and never add an external dependency to liveness.
- Timeout, retry, pool, batch, concurrency, and cache values are illustrative unless approved and must remain externally configurable.
- Missing deployed or externally owned evidence is an evidence gap, not application noncompliance.

## Business-logic risk classification

Every control in this standard carries a `business_logic_risk` classification. The classification governs what may be implemented without approval. It does not change whether a finding may be raised.

| Level | Meaning |
|---|---|
| `none` | Remediation cannot change business behavior, partner contracts, security, or privacy. |
| `low` | Remediation is normally behavior-preserving but must be verified. |
| `moderate` | Remediation can change timing, capacity, resource, or failure behavior under load. |
| `severe` | Remediation can change business semantics, data, partner contracts, security, or privacy. |

Rules:

- A control at any risk level may produce a finding when repository evidence supports it. Risk classification never suppresses detection.
- Step 3A must set `approval_required: true` for every change whose primary or related control is `severe`, or where `requires_approval_before_implementation` is `true`.
- Step 3A may plan and Step 4 may implement the `safe_remediation_without_approval` items for any control without approval, provided they do not alter business behavior.
- Step 4 must not implement any item listed under `requires_approval_for` unless an explicit approval record exists naming the `approval_owner`.
- When a control is `severe` and approval is unavailable, Step 3A must still produce the observability, characterization-test, and evidence work as an implementable target, and mark the behavior-changing portion blocked.
- Step 5 must treat an unapproved behavior change as an implementation-scope violation and must not close the associated finding.

## Controls

### BLOB-001: Storage endpoint or account is deployment-injected

**Severity:** Critical  
**Category:** configuration

#### Requirement

The application code and configuration must satisfy this behavior when the same artifact runs in either active region.

#### Repository evidence to inspect

- `spring.cloud.azure.storage`
- `BlobServiceClientBuilder`
- `STORAGE_ACCOUNT`

#### Finding condition

Emit a finding when evidence shows that account or endpoint is hardcoded.

#### Evidence rule

Cite the file path, symbol or property, and advisory line range when available. Evaluate effective behavior rather than the presence of a library, annotation, or property alone. If the repository does not contain enough evidence, return `not_assessed` rather than assuming noncompliance.

#### Business-logic risk

**Risk level:** `low`  
**Requires approval before implementation:** `false`  
**Approval owner:** `architecture`

**Safe remediation without approval:**

- Externalize an existing hardcoded value to configuration while preserving the same effective default.
- Add or improve metrics, logs, traces, and health details without changing decisions or payload content.
- Add tests that characterize and lock in current behavior.

**Requires approval for:**

- Changing the effective storage account or endpoint.

---

### BLOB-002: Client timeout and retry policies are bounded

**Severity:** High  
**Category:** resilience

#### Requirement

The application code and configuration must satisfy this behavior when the same artifact runs in either active region.

#### Repository evidence to inspect

- `RequestRetryOptions`
- `ClientOptions`
- `responseTimeout`

#### Finding condition

Emit a finding when evidence shows that blob operations lack bounded retry or timeout.

#### Evidence rule

Cite the file path, symbol or property, and advisory line range when available. Evaluate effective behavior rather than the presence of a library, annotation, or property alone. If the repository does not contain enough evidence, return `not_assessed` rather than assuming noncompliance.

#### Business-logic risk

**Risk level:** `moderate`  
**Requires approval before implementation:** `false`  
**Approval owner:** `architecture`

**Safe remediation without approval:**

- Add operation-duration and retry telemetry.
- Add tests that demonstrate the current behavior and the failure mode.

**Requires approval for:**

- Reducing timeouts below observed successful transfer duration.

---

### BLOB-003: Write operations are idempotent and concurrency-safe

**Severity:** Critical  
**Category:** consistency

#### Requirement

The application code and configuration must satisfy this behavior when the same artifact runs in either active region.

#### Repository evidence to inspect

- `ETag`
- `BlobRequestConditions`
- `overwrite flag`
- `idempotency key`

#### Finding condition

Emit a finding when evidence shows that retry or concurrent write can overwrite or duplicate data unexpectedly.

#### Evidence rule

Cite the file path, symbol or property, and advisory line range when available. Evaluate effective behavior rather than the presence of a library, annotation, or property alone. If the repository does not contain enough evidence, return `not_assessed` rather than assuming noncompliance.

#### Business-logic risk

**Risk level:** `severe`  
**Requires approval before implementation:** `true`  
**Approval owner:** `product_and_data`

**Safe remediation without approval:**

- Add ETag and overwrite telemetry.
- Add tests that demonstrate the current behavior and the failure mode.

**Requires approval for:**

- Adding or changing conditional-write behavior that determines which writes succeed.
- Changing overwrite semantics.

---

### BLOB-004: Application does not store durable state on pod-local storage

**Severity:** Critical  
**Category:** state

#### Requirement

The application code and configuration must satisfy this behavior when the same artifact runs in either active region.

#### Repository evidence to inspect

- `java.io`
- `Files.write`
- `/tmp`
- `emptyDir`

#### Finding condition

Emit a finding when evidence shows that durable business state is written only to container or node filesystem.

#### Evidence rule

Cite the file path, symbol or property, and advisory line range when available. Evaluate effective behavior rather than the presence of a library, annotation, or property alone. If the repository does not contain enough evidence, return `not_assessed` rather than assuming noncompliance.

#### Business-logic risk

**Risk level:** `severe`  
**Requires approval before implementation:** `true`  
**Approval owner:** `architecture_and_product`

**Safe remediation without approval:**

- Add local-write telemetry.
- Add tests that demonstrate the current behavior and the failure mode.

**Requires approval for:**

- Relocating durable state, which changes persistence and recovery behavior.

---

### BLOB-005: Critical storage failure affects readiness only when service cannot operate

**Severity:** High  
**Category:** health

#### Requirement

The application code and configuration must satisfy this behavior when the same artifact runs in either active region.

#### Repository evidence to inspect

- `storage HealthIndicator`
- `readiness group`

#### Finding condition

Emit a finding when evidence shows that readiness does not reflect critical storage loss or treats optional storage as fatal.

#### Evidence rule

Cite the file path, symbol or property, and advisory line range when available. Evaluate effective behavior rather than the presence of a library, annotation, or property alone. If the repository does not contain enough evidence, return `not_assessed` rather than assuming noncompliance.

#### Business-logic risk

**Risk level:** `severe`  
**Requires approval before implementation:** `true`  
**Approval owner:** `architecture_and_product`

**Safe remediation without approval:**

- Add dependency-state telemetry.
- Add tests that demonstrate the current behavior and the failure mode.

**Requires approval for:**

- Adding storage to readiness.

---

### BLOB-006: Downloads and uploads stream data and bound memory usage

**Severity:** High  
**Category:** performance

#### Requirement

The application code and configuration must satisfy this behavior when the same artifact runs in either active region.

#### Repository evidence to inspect

- `stream`
- `Flux<ByteBuffer>`
- `block size`

#### Finding condition

Emit a finding when evidence shows that large blob operation loads unbounded content into JVM memory.

#### Evidence rule

Cite the file path, symbol or property, and advisory line range when available. Evaluate effective behavior rather than the presence of a library, annotation, or property alone. If the repository does not contain enough evidence, return `not_assessed` rather than assuming noncompliance.

#### Business-logic risk

**Risk level:** `moderate`  
**Requires approval before implementation:** `false`  
**Approval owner:** `architecture`

**Safe remediation without approval:**

- Add transfer-size and memory telemetry.
- Add tests that demonstrate the current behavior and the failure mode.

**Requires approval for:**

- Changing transfer behavior where partial-content handling or resumability changes.

---

### BLOB-007: Recovery handles DNS, private endpoint, authentication, and client reconnection

**Severity:** High  
**Category:** recovery

#### Requirement

The application code and configuration must satisfy this behavior when the same artifact runs in either active region.

#### Repository evidence to inspect

- `credential refresh`
- `connection recovery`

#### Finding condition

Emit a finding when evidence shows that application requires restart after storage recovery.

#### Evidence rule

Cite the file path, symbol or property, and advisory line range when available. Evaluate effective behavior rather than the presence of a library, annotation, or property alone. If the repository does not contain enough evidence, return `not_assessed` rather than assuming noncompliance.

#### Business-logic risk

**Risk level:** `moderate`  
**Requires approval before implementation:** `false`  
**Approval owner:** `architecture`

**Safe remediation without approval:**

- Add recovery telemetry.
- Add tests that demonstrate the current behavior and the failure mode.

**Requires approval for:**

- Changing client recovery behavior that alters endpoint selection.

---

### BLOB-008: Tests cover timeout, conflict, partial transfer, retry, and recovery

**Severity:** High  
**Category:** testing

#### Requirement

The application code and configuration must satisfy this behavior when the same artifact runs in either active region.

#### Repository evidence to inspect

- `Azurite`
- `mock BlobClient`
- `fault injection`

#### Finding condition

Emit a finding when evidence shows that storage failure behaviors are untested.

#### Evidence rule

Cite the file path, symbol or property, and advisory line range when available. Evaluate effective behavior rather than the presence of a library, annotation, or property alone. If the repository does not contain enough evidence, return `not_assessed` rather than assuming noncompliance.

#### Business-logic risk

**Risk level:** `none`  
**Requires approval before implementation:** `false`  
**Approval owner:** `none`

**Safe remediation without approval:**

- Add tests that demonstrate the current behavior and the failure mode.

---

### BLOB-009: Credentials use approved identity and least-privilege delegation

**Severity:** Critical  
**Category:** security

#### Requirement

The application code and configuration must satisfy this behavior when the same artifact runs in either active region.

#### Repository evidence to inspect

- `DefaultAzureCredential`
- `managed identity`
- `account key`
- `SAS permissions`
- `expiry`

#### Finding condition

Emit a finding when evidence shows that account keys are embedded, SAS tokens are overly permissive or long-lived, or credential rotation requires restart without an approved contract.

#### Evidence rule

Cite the file path, symbol or property, and advisory line range when available. Evaluate effective behavior rather than the presence of a library, annotation, or property alone. If the repository does not contain enough evidence, return `not_assessed` rather than assuming noncompliance.

#### Quality caveats

- Least privilege and short expiry must be preserved during resiliency remediation.

#### Business-logic risk

**Risk level:** `severe`  
**Requires approval before implementation:** `true`  
**Approval owner:** `security`

**Safe remediation without approval:**

- Add credential-failure telemetry with values redacted.
- Add tests that demonstrate the current behavior and the failure mode.

**Requires approval for:**

- Changing credential type, SAS scope, or expiry.

---

### BLOB-010: Signed URLs and tokens are never logged or persisted unsafely

**Severity:** Critical  
**Category:** security

#### Requirement

The application code and configuration must satisfy this behavior when the same artifact runs in either active region.

#### Repository evidence to inspect

- `blob url`
- `sig=`
- `SAS token`
- `log url`

#### Finding condition

Emit a finding when evidence shows that URLs containing signatures or tokens are logged, stored, or returned where they can be reused.

#### Evidence rule

Cite the file path, symbol or property, and advisory line range when available. Evaluate effective behavior rather than the presence of a library, annotation, or property alone. If the repository does not contain enough evidence, return `not_assessed` rather than assuming noncompliance.

#### Quality caveats

- Redaction must occur before logging, not only in the log platform.

#### Business-logic risk

**Risk level:** `low`  
**Requires approval before implementation:** `false`  
**Approval owner:** `security`

**Safe remediation without approval:**

- Add or strengthen URL and token redaction.
- Add or improve metrics, logs, traces, and health details without changing decisions or payload content.
- Add tests that characterize and lock in current behavior.

**Requires approval for:**

- Weakening existing redaction.

---

### BLOB-011: Large transfers use bounded chunking, parallelism, and safe retry

**Severity:** High  
**Category:** performance

#### Requirement

The application code and configuration must satisfy this behavior when the same artifact runs in either active region.

#### Repository evidence to inspect

- `ParallelTransferOptions`
- `block size`
- `maxConcurrency`
- `stage block`

#### Finding condition

Emit a finding when evidence shows that large transfers are unbounded, unresumable, or retried in a way that corrupts or duplicates content.

#### Evidence rule

Cite the file path, symbol or property, and advisory line range when available. Evaluate effective behavior rather than the presence of a library, annotation, or property alone. If the repository does not contain enough evidence, return `not_assessed` rather than assuming noncompliance.

#### Quality caveats

- Parallelism must be bounded relative to memory and network capacity.

#### Business-logic risk

**Risk level:** `moderate`  
**Requires approval before implementation:** `false`  
**Approval owner:** `architecture`

**Safe remediation without approval:**

- Add transfer-progress and retry telemetry.
- Add tests that demonstrate the current behavior and the failure mode.

**Requires approval for:**

- Changing chunking or parallelism where transfer integrity, ordering, or resumability changes.

---

### BLOB-012: Data integrity is verified for critical transfers

**Severity:** High  
**Category:** data-correctness

#### Requirement

The application code and configuration must satisfy this behavior when the same artifact runs in either active region.

#### Repository evidence to inspect

- `Content-MD5`
- `contentHash`
- `checksum`
- `verify`

#### Finding condition

Emit a finding when evidence shows that critical uploads or downloads complete without integrity verification when corruption or truncation would be business-affecting.

#### Evidence rule

Cite the file path, symbol or property, and advisory line range when available. Evaluate effective behavior rather than the presence of a library, annotation, or property alone. If the repository does not contain enough evidence, return `not_assessed` rather than assuming noncompliance.

#### Quality caveats

- Integrity verification requirements should follow the approved data contract.

#### Business-logic risk

**Risk level:** `severe`  
**Requires approval before implementation:** `true`  
**Approval owner:** `product_and_data`

**Safe remediation without approval:**

- Add integrity-verification telemetry in report-only mode.
- Add tests that demonstrate the current behavior and the failure mode.

**Requires approval for:**

- Enforcing integrity checks that can reject transfers the application currently accepts.

---

### BLOB-013: Blob naming and prefix strategy avoids collisions and hotspots

**Severity:** Medium  
**Category:** data-model

#### Requirement

The application code and configuration must satisfy this behavior when the same artifact runs in either active region.

#### Repository evidence to inspect

- `blob name`
- `prefix`
- `path pattern`
- `timestamp key`

#### Finding condition

Emit a finding when evidence shows that naming can collide across instances or concentrate load on a narrow key range.

#### Evidence rule

Cite the file path, symbol or property, and advisory line range when available. Evaluate effective behavior rather than the presence of a library, annotation, or property alone. If the repository does not contain enough evidence, return `not_assessed` rather than assuming noncompliance.

#### Quality caveats

- Naming changes may affect downstream consumers and require coordination.

#### Business-logic risk

**Risk level:** `severe`  
**Requires approval before implementation:** `true`  
**Approval owner:** `partner_contract_and_data`

**Safe remediation without approval:**

- Add or improve metrics, logs, traces, and health details without changing decisions or payload content.
- Add tests that characterize and lock in current behavior.

**Requires approval for:**

- Changing blob naming, prefixes, or path structure that downstream consumers depend on.

---

### BLOB-014: Versioning, soft delete, and immutability assumptions are explicit

**Severity:** High  
**Category:** data-model

#### Requirement

The application code and configuration must satisfy this behavior when the same artifact runs in either active region.

#### Repository evidence to inspect

- `versioning`
- `soft delete`
- `immutability`
- `overwrite`

#### Finding condition

Emit a finding when evidence shows that business correctness depends on version retention, deletion recovery, or immutability behavior that the application does not explicitly establish.

#### Evidence rule

Cite the file path, symbol or property, and advisory line range when available. Evaluate effective behavior rather than the presence of a library, annotation, or property alone. If the repository does not contain enough evidence, return `not_assessed` rather than assuming noncompliance.

#### Quality caveats

- Account-level configuration is external evidence; assess the application assumption.

#### Business-logic risk

**Risk level:** `severe`  
**Requires approval before implementation:** `true`  
**Approval owner:** `data_and_product`

**Safe remediation without approval:**

- Add or improve metrics, logs, traces, and health details without changing decisions or payload content.
- Add tests that characterize and lock in current behavior.

**Requires approval for:**

- Changing versioning, soft-delete, immutability, or overwrite assumptions.

---

### BLOB-015: Blob leases used for coordination are bounded and fenced

**Severity:** Critical  
**Category:** coordination

#### Requirement

The application code and configuration must satisfy this behavior when the same artifact runs in either active region.

#### Repository evidence to inspect

- `acquireLease`
- `lease duration`
- `renew`
- `lease id`

#### Finding condition

Emit a finding when evidence shows that leases are acquired without bounded duration, renewal, ownership validation, or safe expiry behavior.

#### Evidence rule

Cite the file path, symbol or property, and advisory line range when available. Evaluate effective behavior rather than the presence of a library, annotation, or property alone. If the repository does not contain enough evidence, return `not_assessed` rather than assuming noncompliance.

#### Quality caveats

- A lease is not a substitute for idempotent business processing.

#### Business-logic risk

**Risk level:** `severe`  
**Requires approval before implementation:** `true`  
**Approval owner:** `architecture_and_product`

**Safe remediation without approval:**

- Add lease-acquisition, renewal, and expiry telemetry.
- Add tests that demonstrate the current behavior and the failure mode.

**Requires approval for:**

- Changing lease duration, renewal, or fencing behavior that determines which instance performs work.

---

### BLOB-016: Secondary-endpoint read behavior and staleness are explicit

**Severity:** High  
**Category:** consistency

#### Requirement

The application code and configuration must satisfy this behavior when the same artifact runs in either active region.

#### Repository evidence to inspect

- `secondary endpoint`
- `-secondary`
- `RA-GRS`
- `stale read`

#### Finding condition

Emit a finding when evidence shows that reads can silently fall back to a secondary endpoint where staleness would be business-affecting.

#### Evidence rule

Cite the file path, symbol or property, and advisory line range when available. Evaluate effective behavior rather than the presence of a library, annotation, or property alone. If the repository does not contain enough evidence, return `not_assessed` rather than assuming noncompliance.

#### Quality caveats

- Read fallback is a data-correctness decision, not only an availability optimization.

#### Business-logic risk

**Risk level:** `severe`  
**Requires approval before implementation:** `true`  
**Approval owner:** `data_and_product`

**Safe remediation without approval:**

- Add secondary-read and staleness telemetry.
- Add tests that demonstrate the current behavior and the failure mode.

**Requires approval for:**

- Enabling or disabling secondary-endpoint reads, which changes data freshness callers observe.

---

### BLOB-017: Clients are reused with explicit lifecycle and bounded resources

**Severity:** High  
**Category:** resource-management

#### Requirement

The application code and configuration must satisfy this behavior when the same artifact runs in either active region.

#### Repository evidence to inspect

- `BlobServiceClient`
- `singleton`
- `close`
- `http client reuse`

#### Finding condition

Emit a finding when evidence shows that clients are created per request or per operation, or client resources are unbounded.

#### Evidence rule

Cite the file path, symbol or property, and advisory line range when available. Evaluate effective behavior rather than the presence of a library, annotation, or property alone. If the repository does not contain enough evidence, return `not_assessed` rather than assuming noncompliance.

#### Quality caveats

- Client construction is expensive and affects connection reuse and recovery.

#### Business-logic risk

**Risk level:** `low`  
**Requires approval before implementation:** `false`  
**Approval owner:** `architecture`

**Safe remediation without approval:**

- Convert per-request client creation to a managed singleton preserving identical configuration.
- Add or improve metrics, logs, traces, and health details without changing decisions or payload content.
- Add tests that characterize and lock in current behavior.

**Requires approval for:**

- Changing effective client configuration.

---

### BLOB-018: Batch and parallel operations handle partial failure

**Severity:** High  
**Category:** consistency

#### Requirement

The application code and configuration must satisfy this behavior when the same artifact runs in either active region.

#### Repository evidence to inspect

- `batch`
- `deleteBlobs`
- `bulk`
- `partial failure`

#### Finding condition

Emit a finding when evidence shows that batch or parallel operations ignore per-item results or treat partial success as full success.

#### Evidence rule

Cite the file path, symbol or property, and advisory line range when available. Evaluate effective behavior rather than the presence of a library, annotation, or property alone. If the repository does not contain enough evidence, return `not_assessed` rather than assuming noncompliance.

#### Quality caveats

- Partial failure must be surfaced and recoverable.

#### Business-logic risk

**Risk level:** `moderate`  
**Requires approval before implementation:** `false`  
**Approval owner:** `product`

**Safe remediation without approval:**

- Add per-item batch outcome telemetry.
- Add tests that demonstrate the current behavior and the failure mode.

**Requires approval for:**

- Changing batch failure handling where partial success is currently accepted.

---

### BLOB-019: Content metadata and type handling are explicit

**Severity:** Medium  
**Category:** contract

#### Requirement

The application code and configuration must satisfy this behavior when the same artifact runs in either active region.

#### Repository evidence to inspect

- `contentType`
- `metadata`
- `tags`
- `encoding`

#### Finding condition

Emit a finding when evidence shows that content type, metadata, or tags are assumed rather than set explicitly where downstream behavior depends on them.

#### Evidence rule

Cite the file path, symbol or property, and advisory line range when available. Evaluate effective behavior rather than the presence of a library, annotation, or property alone. If the repository does not contain enough evidence, return `not_assessed` rather than assuming noncompliance.

#### Quality caveats

- Metadata contracts may be shared with other systems and require coordination.

#### Business-logic risk

**Risk level:** `severe`  
**Requires approval before implementation:** `true`  
**Approval owner:** `partner_contract`

**Safe remediation without approval:**

- Add or improve metrics, logs, traces, and health details without changing decisions or payload content.
- Add tests that characterize and lock in current behavior.

**Requires approval for:**

- Changing content type, metadata, tags, or encoding that downstream consumers depend on.

---

### BLOB-020: Temporary and intermediate blob cleanup is defined

**Severity:** Medium  
**Category:** lifecycle

#### Requirement

The application code and configuration must satisfy this behavior when the same artifact runs in either active region.

#### Repository evidence to inspect

- `temp blob`
- `cleanup`
- `orphan`
- `retention`

#### Finding condition

Emit a finding when evidence shows that temporary or failed-transfer blobs accumulate without a defined cleanup or retention contract.

#### Evidence rule

Cite the file path, symbol or property, and advisory line range when available. Evaluate effective behavior rather than the presence of a library, annotation, or property alone. If the repository does not contain enough evidence, return `not_assessed` rather than assuming noncompliance.

#### Quality caveats

- Cleanup must not delete data required for reconciliation or audit.

#### Business-logic risk

**Risk level:** `severe`  
**Requires approval before implementation:** `true`  
**Approval owner:** `data_and_product`

**Safe remediation without approval:**

- Add orphan-blob telemetry.
- Add tests that demonstrate the current behavior and the failure mode.

**Requires approval for:**

- Introducing deletion or retention behavior.

---

## Standard finding format

- **Title:** [specific code-level gap]
- **Control:** [BLOB-NNN]
- **Related controls:** [control IDs]
- **Severity:** [severity]
- **Repository evidence:** [path, symbol/property, advisory lines, exact excerpt]
- **Observed behavior:** [what code currently does]
- **Active-active risk:** [effect during regional dependency or network failure]
- **Required code/configuration change:** [specific remediation]
- **Validation test:** [test that proves the behavior]
- **Confidence:** [high, medium, low]

## Non-findings

Do not create infrastructure findings such as missing second-region resources, private endpoints, zone redundancy, geo-replication, capacity, DNS, or global load-balancer configuration. Those are assumed platform responsibilities and are outside this repository assessment.

Do not create findings for account-, namespace-, cluster-, or service-level configuration that the repository does not own. Record those as external evidence requirements. Do not create PCF findings, migration work, or modernization recommendations.
