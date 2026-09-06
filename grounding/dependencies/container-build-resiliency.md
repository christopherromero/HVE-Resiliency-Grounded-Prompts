---
schema_version: "1.0.0"
document_type: assessment_domain_standard
standard_id: CONTAINER-BUILD-RESILIENCY
version: "1.0.0"
lifecycle_status: active
owner: Cloud Architecture Team
assessment_domain: container_build
activation:
  scope_context_path: application-context/assessment-scope-context.yml
  required_status: enabled
repository_owned_only: true
infrastructure_findings_allowed: false
---

# Container Build Resiliency Standard

## Purpose

Evaluate repository-owned Dockerfiles and container build definitions for repeatability, immutability, runtime safety, and compatibility with resilient application operation.

## Controls

### BUILD-001: Runtime base images are immutable

**Severity:** High  
**Category:** image-immutability  
**Applies when:** A Dockerfile defines a runtime image.

**Evidence to inspect:** `FROM`, image tag, image digest, build arguments.  
**Finding condition:** Emit a finding when the runtime base image is referenced only by a mutable tag or floating label without an approved pinning mechanism.

### BUILD-002: Builder images and toolchains are governed and reproducible

**Severity:** High  
**Category:** build-reproducibility  
**Applies when:** A multi-stage build or containerized toolchain is used.

**Evidence to inspect:** Builder image digests, JDK versions, package manager versions, downloaded tools.  
**Finding condition:** Emit a finding when builder inputs can change independently of source and materially alter the output without an approved update process.

### BUILD-003: Dependency resolution fails closed

**Severity:** Critical  
**Category:** build-integrity  
**Applies when:** Dependencies or tools are downloaded during the image build.

**Evidence to inspect:** Shell error handling, checksum verification, package-manager commands, curl/wget pipelines.  
**Finding condition:** Emit a finding when download, verification, test, or packaging failures can be ignored while a runnable image is still produced.

### BUILD-004: Runtime images contain only required runtime content

**Severity:** High  
**Category:** runtime-minimization  
**Applies when:** A runtime image is assembled.

**Evidence to inspect:** Copy statements, build tools, source files, credentials, package managers, shells.  
**Finding condition:** Emit a finding when build-time secrets, source credentials, unnecessary build tools, or sensitive files are copied into the runtime image.

### BUILD-005: Container process startup and signal handling are correct

**Severity:** Critical  
**Category:** lifecycle  
**Applies when:** A container entrypoint or command is defined.

**Evidence to inspect:** `ENTRYPOINT`, `CMD`, shell wrappers, `exec`, process supervisors, signal forwarding.  
**Finding condition:** Emit a finding when the application is not PID 1 or signals are not correctly forwarded, causing shutdown and drain behavior to be bypassed.

### BUILD-006: Runtime executes with a non-root identity when supported

**Severity:** High  
**Category:** runtime-security  
**Applies when:** The application does not require root privileges.

**Evidence to inspect:** `USER`, file ownership, privileged ports, startup scripts.  
**Finding condition:** Emit a finding when the final image runs as root without an evidenced application requirement.

### BUILD-007: Build secrets do not persist in layers

**Severity:** Critical  
**Category:** build-secrets  
**Applies when:** Private dependencies, registries, certificates, or credentials are used during build.

**Evidence to inspect:** Build arguments, environment variables, copied credential files, BuildKit secret mounts, image history implications.  
**Finding condition:** Emit a finding when secrets can persist in a layer, build argument, environment variable, cache, or final image.

### BUILD-008: Health behavior is not duplicated incorrectly in the image

**Severity:** Medium  
**Category:** health-contract  
**Applies when:** Docker `HEALTHCHECK` or image-level health scripts exist.

**Evidence to inspect:** `HEALTHCHECK`, health scripts, application Actuator paths, deployment probes.  
**Finding condition:** Emit a finding when image health semantics conflict with the application's readiness/liveness contract or couple liveness to an external dependency.

### BUILD-009: Build output identity is traceable

**Severity:** Medium  
**Category:** image-observability  
**Applies when:** A container image is produced.

**Evidence to inspect:** OCI labels, source revision, version, build date policy, artifact name.  
**Finding condition:** Emit a finding when source revision and application version cannot be associated with the image through repository-owned build metadata.

### BUILD-010: Architecture and platform targeting are explicit

**Severity:** High  
**Category:** platform-compatibility  
**Applies when:** Images are built for one or more processor architectures or base OS variants.

**Evidence to inspect:** Platform flags, native libraries, multi-arch builds, architecture-specific downloads.  
**Finding condition:** Emit a finding when the build can silently produce incompatible regional runtime artifacts or download architecture-dependent binaries without validation.

## Evaluation rules

- Assess repository-owned build definitions only.
- Do not assess registry replication, scanning service deployment, or runtime admission unless separately grounded and in scope.
- Deduplicate BUILD-001 with `APP-SUPPLY-002` under one root-cause finding.
- Do not prescribe a particular vendor base image.
