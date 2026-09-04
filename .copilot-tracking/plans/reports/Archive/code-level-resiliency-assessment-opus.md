<!-- markdownlint-disable-file -->
<!--
report_governance:
  schema_id: CODE-LEVEL-RESILIENCY-ASSESSMENT-REPORT
  schema_version: "1.2.0"
  schema_path: grounding/governance/assessment-report-schema.md
  schema_validation: passed
  generated_by_phase: Step 3B
  artifact_type: assessment_documentation
  implementation_artifact: false
  report_version: "1.0.0"
  assessment_run_id: "customer-app-2026-09-02-001"
  authoritative_inputs:
    inventory: .copilot-tracking/research/2026-09-02/springboot-active-active-inventory-research.md
    review: .copilot-tracking/reviews/2026-09-02/springboot-active-active-inventory-research-review.md
    remediation_plan: .copilot-tracking/plans/2026-09-03/springboot-active-active-remediation-plan.md
  input_path_exception:
    supplied_plan_path: .copilot-tracking/plans/2026-09-03/springboot-active-active-authoritative-remediation-plan.instructions.md
    resolution: not_present_in_workspace
    resolved_plan_path: .copilot-tracking/plans/2026-09-03/springboot-active-active-remediation-plan.md
    basis: >
      The resolved path is the artifact declared by the Step 3A planning metadata block
      (output_artifacts.plan), by the Step 3A report handoff contract, and by the compact
      handoff summary at .copilot-tracking/plans/handoffs/03A-planning-summary.yml.
-->

<a id="top"></a>

# Code-Level Resiliency Assessment

| Field | Value |
|---|---|
| **Application** | Ecommerce Platform (`customer-app`) |
| **Assessment date** | 2026-09-03 |
| **Repository scope** | `source/customer-app` — nine Maven modules: `common`, `api-gateway`, `user-service`, `product-service`, `order-service`, `inventory-service`, `payment-service`, `cart-service`, `notification-service`, plus repository-owned Kubernetes workload manifests under `source/customer-app/k8s` |
| **Current deployment** | Single region. Repository-owned configuration pins `AZURE_REGION: "westus"`, the Kafka broker alias, and the browser origins to one region. |
| **Target deployment** | Active-active across two Azure regions. The Kafka operating scenario resolved for this assessment is `active_standby` by policy inference and is not architecture-confirmed. |
| **Language and framework** | Java 17, Spring Boot 3.2.5, Spring Cloud Gateway, Spring Kafka, Spring Data JPA, Spring Data Cosmos, Maven multi-module reactor |
| **Runtime platform** | Azure Kubernetes Service with Istio |
| **Report version** | 1.0.0 |

## Table of Contents

1. [Assessment Overview](#1-assessment-overview)
2. [Resiliency-Focused Recommendations](#2-resiliency-focused-recommendations)
3. [Non-Resiliency-Focused Recommendations](#3-non-resiliency-focused-recommendations)
4. [Repository and IaC Evidence Gap Analysis](#4-repository-and-iac-evidence-gap-analysis)
5. [Full Finding Matrix](#5-full-finding-matrix)
6. [Standards Alignment](#6-standards-alignment)
7. [Implementation Roadmap](#7-implementation-roadmap)

---

## 1. Assessment Overview

### Application and repository overview

`customer-app` is a Java 17, Spring Boot 3.2.5 e-commerce estate built as a single Maven multi-module reactor. Nine modules build from one parent POM: a shared `common` library and eight deployable services — `api-gateway`, `user-service`, `product-service`, `order-service`, `inventory-service`, `payment-service`, `cart-service`, and `notification-service`. Each service produces one container image, and all eight images run on Azure Kubernetes Service with Istio.

Inbound traffic enters through `api-gateway`, a reactive Spring Cloud Gateway application that publishes ten routes, applies a `circuitBreaker` filter with a `forward:/fallback/<service>` target on every route, and enforces a Redis-backed rate limit in a custom `RateLimitFilter`. The seven backing services are servlet-based Spring MVC applications.

The workload model is mixed. Synchronous HTTP request handling coexists with asynchronous Kafka processing and scheduled background work:

* **Kafka producers** exist in six services. All publish untyped `HashMap` payloads through `KafkaTemplate`.
* **Kafka consumers** exist in `notification-service` (twelve `@KafkaListener` methods) and `inventory-service` (two). Every listener registers with a static group id and no `autoStartup` attribute.
* **Scheduled work** comprises four `@Scheduled` methods across `cart-service` and `inventory-service`, including reservation expiry, cart abandonment sweep, and cart cleanup. Both deployments run two replicas.

Data paths are split by service. `order-service`, `payment-service`, and `user-service` use Azure SQL through Spring Data JPA and HikariCP. `product-service`, `inventory-service`, and `cart-service` use Azure Cosmos DB through Spring Data Cosmos. `api-gateway` and `product-service` use Redis for rate limiting and caching respectively. Key Vault is consumed exclusively through the Spring Cloud Azure secret property source; no `com.azure` Key Vault SDK type is referenced in any Java class.

Repository-owned configuration comprises one `application.yml` per service, one `Dockerfile` per service, a Kubernetes manifest set under `source/customer-app/k8s` (including `01-configmap.yaml`, `services/all-services.yaml`, and `services/api-gateway.yaml`), a `docker-compose.yml`, and `azure-pipelines.yml`. The Kubernetes workload manifests are treated as **application-owned configuration** in this assessment because four approved findings cite them directly as evidence. No Azure resource provisioning, Terraform, Bicep, private endpoint, DNS, capacity, zone, geo-replication, or global load balancing behavior was assessed or planned.

Confirmed dependencies evaluated against a dependency standard: Azure Key Vault, Azure Cosmos DB, Azure SQL, Azure Managed Redis, HTTP client behavior, AKS with Istio, and Confluent Kafka. Seven further registry entries (Event Hubs, Blob Storage, PostgreSQL, DSE Cassandra, APIM, Application Gateway and GLB, Azure Functions) were not loaded because the authoritative inventory did not list them.

The evidence boundary is strict. This is an **application-code-only** assessment. Infrastructure was assumed present and compliant per the supplied application context, which states *"Do not assess infrastructure"* and *"Assume shared services comply with enterprise resiliency standards."* Zero infrastructure findings and zero PCF findings were created. Twenty-four controls could not be concluded from repository evidence and are recorded as `not_assessed`, not as defects.

One repository-level condition materially constrains everything below: **no module contains a `src/test` directory**. Zero test classes exist across all nine modules, `spring-boot-starter-test` is declared and never exercised, every `Dockerfile` builds with `-DskipTests`, and the pipeline `mvn verify` step executes no tests.

### Kafka operating scenario

The Kafka operating scenario was supplied by Step 1, consumed unchanged by Step 2 and Step 3A, and is reported here without modification.

| Attribute | Value |
|---|---|
| Operating scenario | `active_standby` |
| Scenario source | `policy_inference` |
| Scenario policy | `KAFKA-OPERATING-SCENARIO` v3.1.0, rule `KAFKA-SCENARIO-001` |
| Scenario validation status | `inferred` |
| Architecture confirmation required | **Yes** — outstanding as `EXT-006` |
| Processing model | `mixed` (synchronous HTTP, Kafka consumption, scheduled work) |
| Regional processing model | `unresolved` |
| External side effects | `non_idempotent_external_service` (customer email via SMTP) |
| Kafka-backed state | `none` |
| Related state dependencies | `azure-sql`, `cosmosdb` |
| Context instance | `not_applicable` — only unfilled templates exist under `application-context/Templates/` |

Common controls `KAFKA-001` through `KAFKA-012` were evaluated on repository evidence. The `KAFKA-AS-*` scenario family was evaluated and its scenario-dependent conclusions are labelled as policy inference. `KAFKA-AA-*` and `KAFKA-DI-*` are `not_applicable` under rule `KAFKA-SCENARIO-001`. No claim is made that active-standby infrastructure is deployed. Because the scenario is inferred rather than confirmed, finding **P0-009 (F-014)** retains conditional status and its scenario condition. The absence of an approved architecture context is recorded as evidence requirement `EXT-006`, not as a finding.

### Assessment themes

**T-01 — The artifact is region-neutral; the configuration is not.** One Maven artifact and one image per service is confirmed compliant (`APP-AA-001`), but the shipped configuration pins first-region Cosmos and Key Vault endpoints as absolute literals, embeds `westus` in the Kafka bootstrap default, and hardcodes `AZURE_REGION` and two browser origins. Switching regions currently requires editing repository-owned configuration. Related: **P0-001**, **P3-001**, **P3-004**. Conclusion: **verified**.

**T-02 — No region can express whether it should receive traffic.** All eight workloads probe `/actuator/health/readiness`, yet no service defines a readiness health group, no custom `HealthIndicator` exists in any module, and no health timeout is configured. Readiness reduces to framework `ReadinessState`. A region whose Azure SQL, Cosmos DB, Redis, or Key Vault path is unusable continues to advertise itself. Related: **P0-003**. Conclusion: **verified**.

**T-03 — No workload ownership model exists.** Fourteen Kafka listeners and four scheduled jobs are unconditionally active in every replica of every region. There is no lease, leader election, ShedLock, ownership epoch, or activation flag anywhere in the repository, and nothing can verify Azure SQL primary ownership before processing. Under the inferred active-standby scenario this is the single largest correctness risk. Related: **P0-009** (conditional), **P0-010**, **P0-011**. Conclusion: **P0-009 conditional; P0-010 and P0-011 verified**.

**T-04 — Authoritative writes are unsafe under duplication.** Cosmos stock mutation is a read-modify-write full-document replace with a declared but never-compared `@Version` etag; payment idempotency is a read-then-act `exists` check while the unique `idempotency_key` column has no mapped entity field; and every write path calls `KafkaTemplate.send` inside the same database transaction while discarding the returned `CompletableFuture`. Related: **P0-005**, **P0-006**, **P0-007**, **P0-008**, **P2-004**. Conclusion: **verified**.

**T-05 — Messages carry no identity and consumers never deduplicate.** Producers publish plain maps with no event identifier and a publish-time timestamp. The shared `BaseEvent` declares an `eventId` but no producer uses it, and its constructor never assigns `correlationId` or `tenantId`. The only non-idempotent external effect in the system — customer email — has no already-sent check. Related: **P2-001**, **P2-002**, **P2-003**, **P0-004**. Conclusion: **verified**.

**T-06 — No isolation or failure budget in the backing services.** Resilience4j is declared only in `api-gateway`. The seven backing services use no circuit breaker, bulkhead, time limiter, or retry, and handle failure with a `try/catch` that logs and returns normally. The one service that does have a breaker has an inverted budget: the client waits 30s while the breaker fires at 10s. Related: **P1-002**, **P1-003**, **P1-004**, **P1-006**, **P1-007**, **P1-008**. Conclusion: **verified**.

**T-07 — Declared resiliency settings are not in effect.** Both Redis clients declare timeouts, TLS, and pool bounds under the Spring Boot 2 `spring.redis.*` prefix while the application runs Spring Boot 3.2.5, where `spring.data.redis.*` is the binding prefix. `spring.redis.cache.time-to-live` is not a bindable property, a custom `cache.*.ttl` block binds to nothing, and seven `service.*.url` keys bind to nothing. Operators believe the failure budget is tunable; it is not. Related: **P1-001**. Conclusion: **verified**.

**T-08 — Regional behavior is not legible.** Four services declare a static `region: westus` metric tag and four declare none. No zone, cluster, or instance tag exists. Correlation identity is regenerated per hop, never placed in MDC despite a log pattern that references `%X{correlationId}`, and never propagated. No custom meters exist anywhere, so a stalled consumer, a skipped scheduled run, or a silently failed publish is invisible. Related: **P3-001**, **P3-002**, **P3-003**. Conclusion: **verified**.

**T-09 — Nothing is proven.** Zero test classes exist. No timeout, retry, health transition, idempotency, shutdown, promotion, or recovery behavior has ever been executed. Every remediation below would otherwise ship without a regression guard. Related: **P0-012**. Conclusion: **verified**.

**T-10 — The management surface is internet-reachable.** `api-gateway` exposes the administrative `gateway` actuator endpoint with `show-details: always` on the same container port that a `LoadBalancer` Service publishes with the internal annotation set to `false`. No service binds management to a separate port. Related: **P1-010**. Conclusion: **verified**.

### Approved shared-service and reference architectures

The supplied `REFERENCE_ARCHITECTURE_REGISTRY` (`grounding/registry/dependency-standard-registry.yml`) is a dependency-standard registry that maps dependencies to grounding files. It contains no customer reference-architecture links. The reference table below is the one defined by the governing report schema and is reproduced without addition or modification.

| Azure Shared Service | Link to Reference Architecture |
| --- | --- |
| Azure API Management | [Reference](https://rxsafeway.sharepoint.com/:w:/r/sites/Cloud2.0/Shared%20Documents/I11%20Resiliency%20Program/Discovery/Integration%20Platform/APIM/Design/APIM%20-%20Albertsons%20Multi-Region%20Design%20v5.docx?d=w7f65ea542cc7491687202cfa68599d7b&csf=1&web=1&e=dhPvP3) |
| Azure Application Gateway | [Reference](https://rxsafeway.sharepoint.com/:w:/r/sites/Cloud2.0/Shared%20Documents/I11%20Resiliency%20Program/Discovery/Integration%20Platform/AppGW/Design/Albertsons%20Architecture%20Design_Application%20Gateway_v1.0.docx?d=w3126f533271842c9a75d83ae93b6b6db&csf=1&web=1&e=hmksie) |
| Azure Key Vault | [Reference](https://rxsafeway.sharepoint.com/:w:/r/sites/Cloud2.0/Shared%20Documents/I11%20Resiliency%20Program/Discovery/Cloud%20Foundation/Design/Albertsons%20Azure%20Key%20Vault%20Architecture%20Design%20Proposal.docx?d=wf1abecab2812460a8cadd6e5956d5bb8&csf=1&web=1&e=yzvvQh) |
| Kafka | [Reference](https://rxsafeway.sharepoint.com/:w:/r/sites/Cloud2.0/Shared%20Documents/I11%20Resiliency%20Program/Discovery/Integration%20Platform/Kafka/Approved_Albertsons_RegionResiliency_Kafka-MultiRegion.docx?d=w08142308135244de855f4dab4c49ca2d&csf=1&web=1&e=kueuJ9) |
| Azure Entra ID | [Reference](https://rxsafeway.sharepoint.com/:w:/r/sites/Cloud2.0/Shared%20Documents/I11%20Resiliency%20Program/Discovery/Security/IAM/Design/ACI%20Entra%20ID%20Draft%20v1.0.docx?d=wad696d3ecdae4d84a6a1ea5675d3aec6&csf=1&web=1&e=rCLr5y) |
| Azure Storage | [Reference](https://rxsafeway.sharepoint.com/:w:/r/sites/Cloud2.0/Shared%20Documents/I11%20Resiliency%20Program/Discovery/Database%20Platform/Storage/Albertsons%20Architecture%20Design_Storage_v1.0.docx?d=w97ad6ce3e77348e09a1ee3e676bc3ac0&csf=1&web=1&e=C4SVMy) |
| Azure SQL Database | [Reference](https://rxsafeway.sharepoint.com/:f:/r/sites/Cloud2.0/Shared%20Documents/I11%20Resiliency%20Program/Discovery/Database%20Platform/SQL%20DB?csf=1&web=1&e=xMauSY) |
| Azure Cosmos DB | [Reference](https://rxsafeway.sharepoint.com/:w:/r/sites/Cloud2.0/Shared%20Documents/I11%20Resiliency%20Program/Discovery/Database%20Platform/Cosmos/Albertsons_Architecture_Design_MongoDB_RU_v1.0.docx?d=wa68893488e094fef9b5506690c685847&csf=1&web=1&e=YDVc7g) |
| Azure Functions | [Reference](https://rxsafeway.sharepoint.com/:w:/r/sites/Cloud2.0/Shared%20Documents/I11%20Resiliency%20Program/Discovery/Cloud%20Foundation/Design/Albertsons%20Azure%20Functions%20Architecture%20Design%20Proposal.docx?d=w0c59f970929f47f2a6dcef096fffd7f2&csf=1&web=1&e=tXAxCU) |
| Azure Networking | [Reference](https://rxsafeway.sharepoint.com/:w:/r/sites/Cloud2.0/Shared%20Documents/I11%20Resiliency%20Program/Discovery/Network/Design/Albertsons%20Architecture%20Design%20-%20Networking%20-%20Draft%201.3.docx?d=w6adb9edef1754753a259b296fffa4b1d&csf=1&web=1&e=IshBZT) |
| Azure Managed Redis | [Reference](https://rxsafeway.sharepoint.com/:w:/r/sites/Cloud2.0/Shared%20Documents/I11%20Resiliency%20Program/Discovery/Database%20Platform/Redis/Design/Managed%20Redis%20-%20Albertsons%20Multi-Region%20Design%20v3.docx?d=wad90acec4c154b2498d899a2ffcdc9d4&csf=1&web=1&e=L7pVbQ) |
| Azure Kubernetes Service (AKS) | [Reference](https://rxsafeway.sharepoint.com/:w:/r/sites/Cloud2.0/Shared%20Documents/I11%20Resiliency%20Program/Discovery/Container%20Platform/Design/Albertsons%20Architecture%20Design_AKS%20and%20Istio_v1.0.docx?d=w97c0edfea59d466e80af843958d95c5c&csf=1&web=1&e=7UJSQS) |
| Azure Storage Blobs and Files | [Reference](https://rxsafeway.sharepoint.com/:w:/r/sites/Cloud2.0/Shared%20Documents/I11%20Resiliency%20Program/Discovery/Storage/Architecture%20Options%20for%20Storage%20Blobs%20and%20Azure%20Files_v04.docx?d=w5d8203dcf43c41438843a71219ec05d8&csf=1&web=1&e=kTl0dg) |

### Summary findings table

| Priority | Section | Confirmed count | Description |
|---|---|---:|---|
| P0 | Resiliency-Focused Recommendations | 12 | Conditions that prevent correct or safe operation in a second region: hardcoded regional endpoints, absent regional data-path affinity, non-functional readiness, pod-local business state, unsafe authoritative writes, unobserved event publication, ungated Kafka and scheduled workloads, incomplete shutdown and drain, and the total absence of a test harness. |
| P1 | Resiliency-Focused Recommendations | 13 | Recovery, isolation, and budget gaps: unbound resiliency properties, absent Cosmos/Kafka/Azure SQL budgets, no isolation in seven backing services, inverted gateway timeout budget, unresolved fallback targets, unbounded async execution, an internet-reachable management surface, a restart-only secret-rotation contract, an unbounded scheduled sweep, and mutable base-image tags. |
| P2 | Resiliency-Focused Recommendations | 5 | Data-correctness and replay gaps: no stable event identity or consumer deduplication, offsets advancing ahead of completed work, no dead-letter contract, non-idempotent order creation, and a non-atomic rate-limit counter that fails open silently. |
| P3 | Resiliency-Focused Recommendations | 4 | Operational legibility gaps: no regional telemetry attribution, no correlation propagation, no business-throughput or stuck-work signals, and compiled business constants. |
| — | Non-Resiliency-Focused Recommendations | 0 | Every approved finding is classified `resiliency_related: true` by Step 3A. No approved finding is classified as non-resiliency-related. |
| **Total** | | **34** | Reconciles with the Full Finding Matrix: 33 verified findings plus 1 conditional finding (P0-009 / F-014). |

Counts exclude 13 verified controls, 24 `not_assessed` controls, 42 `not_applicable` controls, 0 accepted risks, and all PCF references.

### Illustrative-code notice

> **IMPORTANT:** Hard numbers used for retry counts, timeout settings, interval timings, thread-pool sizes, cache duration, health thresholds, and circuit-breaker settings are examples unless the authoritative plan identifies an approved value. These values must be externally configurable and coordinated with application, mesh, gateway, and load-balancer budgets. All code snippets are illustrative proposals, not applied or prescriptive patches.

Open question `OQ-19` records that no numeric timeout, retry, backoff, pool, or threshold value across Kafka, Azure SQL, Cosmos, the gateway, or Resilience4j has yet been approved by an owner.

[Back to Top](#top)

---
## 2. Resiliency-Focused Recommendations

Findings are grouped first by governed priority, then by repository-specific category. Every priority value is the calculated governance priority from `grounding/governance/remediation-prioritization.md`, policy `AA-REMEDIATION-PRIORITY` v1.0.0. Zero priority overrides were applied.

Display IDs are `{PRIORITY}-{NNN}`, sequential within priority. The originating Step 2 finding ID is preserved in the Full Finding Matrix "Source ID" column and is stated on every finding below.

---

### P0 Critical Immediate Action

#### Configuration Contract

#### P0-001: Regional service endpoints are hardcoded in application configuration

**Priority: P0 - Critical Immediate Action**

**Priority policy:** `AA-REMEDIATION-PRIORITY` v1.0.0, rule `P0-AA-001` · **Change ID:** `CHANGE-AA-001` (Wave 1) · **Source ID:** F-001 · **Primary control:** `APP-AA-002`

**Severity:** Critical

**Resiliency Related:** Yes

**Finding status:** Verified finding

**Issue:** Cosmos DB and Key Vault endpoints are literal absolute URLs with no placeholder. The `notification-service` Kafka bootstrap default embeds the region name. The shared ConfigMap pins `AZURE_REGION`, the Kafka broker alias, and the frontend URL to one region, and the gateway CORS allow-list contains two region-qualified browser origins.

**What does this solve:** It restores the single-immutable-artifact property that active-active operation depends on and removes the repository edit currently required to switch regions.

**Resiliency Impact:** The same artifact deployed to a second region resolves to first-region Cosmos DB and Key Vault endpoints. A regional outage cannot be contained by configuration alone, and a region switch requires editing repository-owned configuration and re-releasing. Under the inferred `active_standby` scenario, the standby region cannot be deployed or promoted without a source change, and the Kafka bootstrap alias remains a compiled assumption rather than a deployment input.

**Recommended Fix:** Replace every dependency endpoint, broker alias, region token, and allowed origin with a required environment placeholder carrying no committed regional default, so startup fails fast when a required value is unset rather than silently resolving the first region. Convert the shared ConfigMap into a region-parameterised template consumed by the existing pipeline substitution step.

**File:** source/customer-app/product-service/src/main/resources/application.yml:8-21

```yaml
// before
    cloud:
      azure:
        cosmos:
          endpoint: https://ecommerce-cosmos.documents.azure.com:443/
          key: ${COSMOS_KEY}
          database: ecommerce-products
          consistency-level: SESSION
          populate-query-metrics: false
          connection-mode: DIRECT
        keyvault:
          secret:
            endpoint: https://ecommerce-keyvault.vault.azure.net/
            credential:
              managed-identity-enabled: true
```

**File:** source/customer-app/k8s/01-configmap.yaml:11-13 and :34-35

```yaml
// before
# Azure Region
AZURE_REGION: "westus"
ENVIRONMENT: "production"
# Kafka
KAFKA_BOOTSTRAP_SERVERS: "ecommerce-kafka.westus.azure.com:9093"
```

**File:** source/customer-app/api-gateway/src/main/resources/application.yml:15-18

```yaml
// before
              allowedOrigins:
                - "https://ecommerce.westus.azure.com"
                - "https://admin.ecommerce.westus.azure.com"
                - "http://localhost:3000"
```

**Fix:**

> Illustrative proposal only.

`source/customer-app/product-service/src/main/resources/application.yml` — `spring.cloud.azure.cosmos` and `spring.cloud.azure.keyvault.secret`

```yaml
spring:
  cloud:
    azure:
      cosmos:
        endpoint: ${AZURE_COSMOS_ENDPOINT}
        key: ${COSMOS_KEY}
        database: ${AZURE_COSMOS_DATABASE:ecommerce-products}
        consistency-level: SESSION
        populate-query-metrics: false
        connection-mode: DIRECT
      keyvault:
        secret:
          endpoint: ${AZURE_KEYVAULT_ENDPOINT}
          credential:
            managed-identity-enabled: true
```

Both absolute first-region URLs become required placeholders with no default, so an unset value fails startup instead of silently resolving the first region. The database name keeps a non-regional default because it is not region-specific.

`source/customer-app/k8s/01-configmap.yaml` — `ConfigMap ecommerce-common-config`

```yaml
data:
  APP_DEPLOYMENT_REGION: "${APP_DEPLOYMENT_REGION}"
  AZURE_REGION: "${APP_DEPLOYMENT_REGION}"
  ENVIRONMENT: "${ENVIRONMENT}"
  KAFKA_BOOTSTRAP_SERVERS: "${KAFKA_BOOTSTRAP_SERVERS}"
  AZURE_COSMOS_ENDPOINT: "${AZURE_COSMOS_ENDPOINT}"
  AZURE_KEYVAULT_ENDPOINT: "${AZURE_KEYVAULT_ENDPOINT}"
  APP_CORS_ORIGIN_WEB: "${APP_CORS_ORIGIN_WEB}"
  APP_CORS_ORIGIN_ADMIN: "${APP_CORS_ORIGIN_ADMIN}"
```

The ConfigMap becomes a region-parameterised template consumed by the existing pipeline substitution step rather than a committed single-region artifact. No new Azure resource, DNS entry, or provisioning behavior is introduced.

`source/customer-app/common/src/test/java/com/ecommerce/common/config/RegionNeutralConfigurationTest.java` — build guard

```java
package com.ecommerce.common.config;

import static org.assertj.core.api.Assertions.assertThat;

import java.nio.file.Files;
import java.nio.file.Path;
import java.util.List;
import java.util.regex.Pattern;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.ValueSource;

class RegionNeutralConfigurationTest {

    private static final Pattern REGION_TOKEN =
            Pattern.compile("(?i)westus|eastus|northeurope|westeurope");
    private static final Pattern ABSOLUTE_AZURE_ENDPOINT =
            Pattern.compile("https://[A-Za-z0-9.-]+\\\\.(vault\\\\.azure\\\\.net|documents\\\\.azure\\\\.com)");

    @ParameterizedTest
    @ValueSource(strings = {
            "../product-service/src/main/resources/application.yml",
            "../api-gateway/src/main/resources/application.yml",
            "../notification-service/src/main/resources/application.yml",
            "../k8s/01-configmap.yaml"
    })
    void shippedConfigurationCarriesNoRegionalLiteral(String relativePath) throws Exception {
        List<String> lines = Files.readAllLines(Path.of(relativePath));
        for (String line : lines) {
            assertThat(REGION_TOKEN.matcher(line).find())
                    .as("region literal in %s: %s", relativePath, line)
                    .isFalse();
            assertThat(ABSOLUTE_AZURE_ENDPOINT.matcher(line).find())
                    .as("absolute Azure endpoint in %s: %s", relativePath, line)
                    .isFalse();
        }
    }
}
```

A repository-level guard that fails the build if any regional literal or absolute Azure endpoint is reintroduced into shipped configuration. It uses only JUnit 5 and AssertJ, which arrive with the `spring-boot-starter-test` already declared in all nine modules, and requires no running application context.

**Notes:**

* **Cross-refs:** Prerequisite for **P0-002** (endpoint must be externalized before regional preference is meaningful), **P1-001**, **P1-003**, **P1-011**, **P3-001**, **P3-004**.
* **Implementation:** `CHANGE-AA-001`, Wave 1, complexity medium. Affects `product-service`, `api-gateway`, `notification-service` `application.yml` and `k8s/01-configmap.yaml`.
* **Validation:** T-AA-001-01 (configuration guard), T-AA-001-02 (region-B property resolution). `mvn -f source/customer-app/pom.xml -pl common,api-gateway,product-service,notification-service -am test`.
* **Guardrail:** Removing the `localhost` development origin from the default profile breaks local browser development until a local profile is added. Removing defaults converts a previously silent misconfiguration into a startup failure — intended, but it changes deployment failure modes. `OQ-01` records that the pipeline substitution step must be extended and that `api-gateway.yaml` is currently applied before substitution (`UNC-013`).

<span style="font-size: 14px;">**MSFT Reference:** [External Configuration Store pattern](https://learn.microsoft.com/azure/architecture/patterns/external-configuration-store)</span>

---

#### Regional Data-Path Affinity

#### P0-002: Cosmos DB client has no local-region preference or endpoint-discovery policy

**Priority: P0 - Critical Immediate Action**

**Priority policy:** `AA-REMEDIATION-PRIORITY` v1.0.0, rule `P0-AA-002` · **Change ID:** `CHANGE-AA-002` (Wave 2) · **Source ID:** F-002 · **Primary control:** `COSMOS-002`

**Severity:** Critical

**Resiliency Related:** Yes

**Finding status:** Verified finding

**Issue:** The Cosmos configuration declares endpoint, key, database, consistency level, and connection mode only. No preferred-regions list, multi-write setting, endpoint-discovery flag, `CosmosClientBuilder` bean, or `AbstractCosmosConfiguration` subclass exists in any of the three Cosmos-using services. The authoritative inventory records zero matches for `preferred-regions`, `preferredRegions`, `setPreferredRegions`, `multiple-write-locations`, `multipleWriteLocations`, or `endpoint-discovery` across the repository.

**What does this solve:** It gives the application a repository-expressed, deployment-tunable regional data-path policy instead of an implicit account default.

**Resiliency Impact:** Regional read and write affinity is left entirely to Cosmos account defaults. A second-region instance has no repository-expressed policy that keeps its data path local, so a normally operating deployment can transparently use a remote-region endpoint. The application cannot express or change regional preference without a code change. Under `active_standby`, the standby deployment cannot be configured to prefer its own region for reads.

**Recommended Fix:** Bind an ordered, deployment-supplied preferred-region list in each Cosmos-using service, with index 0 being the deployment's own region, and express endpoint discovery explicitly rather than assuming it. Fail startup when the ordered list is not supplied.

**File:** source/customer-app/product-service/src/main/resources/application.yml:8-16

```yaml
// before
    cloud:
      azure:
        cosmos:
          endpoint: https://ecommerce-cosmos.documents.azure.com:443/
          key: ${COSMOS_KEY}
          database: ecommerce-products
          consistency-level: SESSION
          populate-query-metrics: false
          connection-mode: DIRECT
```

**File:** source/customer-app — repository-wide absence of preferred-region configuration (evidence `EV-F-002-02`; original source excerpt: `not_applicable`, the finding rests on an absence the authoritative inventory established)

**Fix:**

> Illustrative proposal only.

`source/customer-app/product-service/src/main/resources/application.yml` — `app.cosmos.region`

```yaml
spring:
  cloud:
    azure:
      cosmos:
        endpoint: ${AZURE_COSMOS_ENDPOINT}
        key: ${COSMOS_KEY}
        database: ${AZURE_COSMOS_DATABASE:ecommerce-products}
        consistency-level: SESSION
        connection-mode: DIRECT

app:
  cosmos:
    region:
      # Ordered, deployment-supplied. Index 0 is the local region for this deployment.
      preferred-regions: ${AZURE_COSMOS_PREFERRED_REGIONS}
      endpoint-discovery-enabled: ${AZURE_COSMOS_ENDPOINT_DISCOVERY_ENABLED:true}
      multiple-write-locations-enabled: ${AZURE_COSMOS_MULTI_WRITE_ENABLED:false}
```

Regional preference becomes an application-owned, externally supplied contract. The list is ordered so index 0 is the deployment's own region, and no region name is committed.

`source/customer-app/common/src/main/java/com/ecommerce/common/config/CosmosRegionProperties.java`

```java
package com.ecommerce.common.config;

import jakarta.validation.constraints.NotEmpty;
import java.util.List;
import org.springframework.boot.context.properties.ConfigurationProperties;
import org.springframework.validation.annotation.Validated;

@Validated
@ConfigurationProperties(prefix = "app.cosmos.region")
public class CosmosRegionProperties {

    /** Ordered regional preference. Index 0 is the local region for this deployment. */
    @NotEmpty
    private List<String> preferredRegions = List.of();

    private boolean endpointDiscoveryEnabled = true;

    private boolean multipleWriteLocationsEnabled = false;

    public List<String> getPreferredRegions() {
        return preferredRegions;
    }

    public void setPreferredRegions(List<String> preferredRegions) {
        this.preferredRegions = preferredRegions;
    }

    public boolean isEndpointDiscoveryEnabled() {
        return endpointDiscoveryEnabled;
    }

    public void setEndpointDiscoveryEnabled(boolean endpointDiscoveryEnabled) {
        this.endpointDiscoveryEnabled = endpointDiscoveryEnabled;
    }

    public boolean isMultipleWriteLocationsEnabled() {
        return multipleWriteLocationsEnabled;
    }

    public void setMultipleWriteLocationsEnabled(boolean multipleWriteLocationsEnabled) {
        this.multipleWriteLocationsEnabled = multipleWriteLocationsEnabled;
    }
}
```

A validated, technology-neutral binding for regional preference that fails startup when the ordered region list is not supplied. It uses only Spring Boot binding and Jakarta validation, so it carries no Azure SDK version risk, and it is shared by the three Cosmos-using services through the existing `common` module.

**Illustrative code status:** Targeted implementation discovery required (`TD-01`)

**Target:** `CosmosClientBuilder` regional customizer bean — repository path not yet selected

**Why code was not generated:** The effective Spring Cloud Azure 5.10.0 client-builder customization type for `spring-cloud-azure-starter-data-cosmos` cannot be established from the supplied artifacts. Inventory uncertainty `UNC-016` records that BOM-resolved dependency versions were never resolved because no build was executed, and no `CosmosClientBuilder` bean or `AbstractCosmosConfiguration` subclass exists in the repository to copy a proven pattern from.

**Unresolved inputs:**

* Effective `spring-cloud-azure-starter-data-cosmos` 5.10.0 builder-customizer type and registration mechanism
* Whether the project prefers a builder customizer or an `AbstractCosmosConfiguration` subclass

**Intended behavior:** The bound `CosmosRegionProperties` values must be applied to the effective Cosmos client so the ordered preferred-region list and endpoint-discovery flag reach the SDK.

**Notes:**

* **Cross-refs:** Depends on **P0-001**. Shares the client-customization discovery with **P1-002** (`TD-07`) and **P1-011** (`TD-09`).
* **Implementation:** `CHANGE-AA-002`, Wave 2, complexity medium. Two of three targets carry generated code; one is blocked.
* **Validation:** T-AA-002-01 (binding validation), T-AA-002-02 (region-A versus region-B profile differentiation). `mvn -f source/customer-app/pom.xml -pl common,product-service,inventory-service,cart-service -am test`.
* **Guardrail:** Applying a preferred-region list against an account with a single write region moves reads local while writes remain remote. That is an account-topology fact recorded as external evidence `EXT-004`, not an application defect.

<span style="font-size: 14px;">**MSFT Reference:** [High availability in Azure Cosmos DB](https://learn.microsoft.com/azure/cosmos-db/high-availability)</span>

---

#### Traffic Eligibility and Health

#### P0-003: Readiness does not reflect any critical region-local dependency

**Priority: P0 - Critical Immediate Action**

**Priority policy:** `AA-REMEDIATION-PRIORITY` v1.0.0, rule `P0-AA-003` · **Change ID:** `CHANGE-AA-003` (Wave 2) · **Source ID:** F-016 · **Primary control:** `APP-AA-007`

**Severity:** Critical

**Resiliency Related:** Yes

**Finding status:** Verified finding

**Issue:** All eight workloads probe `/actuator/health/readiness`. No service defines `management.endpoint.health.group.readiness.include` or `.exclude`, no custom `HealthIndicator` or `ReactiveHealthIndicator` exists in any module, and no health timeout is configured. Readiness therefore reduces to the framework `ReadinessState`. Four services do not even declare `management.endpoint.health.probes.enabled`. Container `HEALTHCHECK` directives target the aggregate `/actuator/health` instead of the probe groups.

**What does this solve:** It gives the platform a truthful traffic-eligibility signal per region, which is the precondition for withdrawing a degraded region and for rejoining it automatically after recovery.

**Resiliency Impact:** A region whose Azure SQL, Cosmos DB, Redis, or Key Vault path is unusable continues to report ready and continues to receive traffic. Traffic cannot be withdrawn from a degraded region and cannot be restored automatically after recovery. Under `active_standby`, readiness is the mechanism by which a region that has lost its authoritative data path stops advertising itself and by which a promoted region advertises itself once healthy.

**Recommended Fix:** Declare an explicit readiness group per service containing `readinessState` plus only that service's critical region-local dependency indicators; pin the liveness group to `livenessState` only; bound and cache dependency probes so probe traffic cannot amplify a dependency outage; and point the container `HEALTHCHECK` at the liveness group.

**File:** source/customer-app/order-service/src/main/resources/application.yml:70-89

```yaml
// before
management:
  endpoints:
    web:
      exposure:
        include: health,info,prometheus,metrics
  endpoint:
    health:
      probes:
        enabled: true
      show-details: always
  metrics:
    export:
      prometheus:
        enabled: true
  health:
    livenessstate:
      enabled: true
    readinessstate:
      enabled: true
```

**File:** source/customer-app/k8s/services/all-services.yaml:65-79

```yaml
// before
            livenessProbe:
              httpGet:
                path: /actuator/health/liveness
                port: 8081
              initialDelaySeconds: 90
              periodSeconds: 30
              failureThreshold: 3
            readinessProbe:
              httpGet:
                path: /actuator/health/readiness
                port: 8081
              initialDelaySeconds: 45
              periodSeconds: 10
```

**File:** source/customer-app/order-service/Dockerfile:26

```dockerfile
// before
HEALTHCHECK --interval=30s --timeout=10s --start-period=90s --retries=3 CMD curl -f http://localhost:8083/actuator/health || exit 1
```

**Fix:**

> Illustrative proposal only.

`source/customer-app/order-service/src/main/resources/application.yml` — `management.endpoint.health.group`

```yaml
management:
  endpoints:
    web:
      exposure:
        include: health,info,prometheus,metrics
  endpoint:
    health:
      probes:
        enabled: true
      show-details: when-authorized
      group:
        liveness:
          include: livenessState
        readiness:
          include: readinessState,db
          additional-path: "server:/actuator/health/readiness"
  health:
    livenessstate:
      enabled: true
    readinessstate:
      enabled: true
    db:
      enabled: true
  metrics:
    export:
      prometheus:
        enabled: true
```

The readiness group now includes the built-in `db` indicator so a sustained loss of the region-local Azure SQL path takes the deployment out of rotation, while the liveness group is pinned to `livenessState` only so an external failure can never cause a restart loop. Readiness recovers automatically when the indicator returns UP; no restart is required.

`source/customer-app/common/src/main/java/com/ecommerce/common/health/BoundedCachedHealthIndicator.java`

```java
package com.ecommerce.common.health;

import java.time.Duration;
import java.time.Instant;
import java.util.concurrent.Callable;
import java.util.concurrent.CompletableFuture;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.TimeUnit;
import java.util.concurrent.atomic.AtomicReference;
import org.springframework.boot.actuate.health.Health;
import org.springframework.boot.actuate.health.HealthIndicator;

/**
 * Bounds and caches a dependency probe so readiness evaluation cannot amplify a dependency
 * outage or add unbounded latency to the probe endpoint.
 */
public class BoundedCachedHealthIndicator implements HealthIndicator {

    private record Snapshot(Health health, Instant takenAt) {}

    private final String dependencyName;
    private final Callable<Health> probe;
    private final Duration probeTimeout;
    private final Duration cacheTtl;
    private final ExecutorService probeExecutor;
    private final AtomicReference<Snapshot> lastSnapshot = new AtomicReference<>();

    public BoundedCachedHealthIndicator(String dependencyName,
                                        Callable<Health> probe,
                                        Duration probeTimeout,
                                        Duration cacheTtl,
                                        ExecutorService probeExecutor) {
        this.dependencyName = dependencyName;
        this.probe = probe;
        this.probeTimeout = probeTimeout;
        this.cacheTtl = cacheTtl;
        this.probeExecutor = probeExecutor;
    }

    @Override
    public Health health() {
        Snapshot cached = lastSnapshot.get();
        if (cached != null && Instant.now().isBefore(cached.takenAt().plus(cacheTtl))) {
            return cached.health();
        }
        Health evaluated = evaluate();
        lastSnapshot.set(new Snapshot(evaluated, Instant.now()));
        return evaluated;
    }

    private Health evaluate() {
        CompletableFuture<Health> future =
                CompletableFuture.supplyAsync(this::callProbe, probeExecutor);
        try {
            return future.get(probeTimeout.toMillis(), TimeUnit.MILLISECONDS);
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
            return down("interrupted");
        } catch (Exception e) {
            future.cancel(true);
            return down(e.getClass().getSimpleName());
        }
    }

    private Health callProbe() {
        try {
            return probe.call();
        } catch (Exception e) {
            return down(e.getClass().getSimpleName());
        }
    }

    private Health down(String reason) {
        return Health.down()
                .withDetail("dependency", dependencyName)
                .withDetail("reason", reason)
                .withDetail("probeTimeoutMs", probeTimeout.toMillis())
                .build();
    }
}
```

Provides the bounded, cached evaluation the readiness design rule requires. It uses only Spring Boot Actuator `Health` and `HealthIndicator` plus JDK concurrency, so it carries no vendor SDK risk, and it recovers automatically because the next evaluation after the cache TTL re-runs the probe. Timeout and TTL are constructor inputs so they stay externally configurable rather than compiled constants.

`source/customer-app/k8s/services/all-services.yaml` — probe bounds

```yaml
livenessProbe:
  httpGet:
    path: /actuator/health/liveness
    port: 8081
  initialDelaySeconds: 90
  periodSeconds: 30
  timeoutSeconds: 3
  failureThreshold: 3
readinessProbe:
  httpGet:
    path: /actuator/health/readiness
    port: 8081
  initialDelaySeconds: 45
  periodSeconds: 10
  timeoutSeconds: 3
  successThreshold: 1
  failureThreshold: 3
```

Adds the missing probe timeout, success threshold, and failure threshold so a slow health response is treated as a failure within a bounded window rather than hanging the probe. Probe paths are unchanged because they already target the correct groups.

**Illustrative code status:** Targeted implementation discovery required (`TD-02`)

**Target:** Key Vault readiness contributor — repository path not yet selected

**Why code was not generated:** No `com.azure` Key Vault SDK type is referenced in any Java class; Key Vault is consumed only through the Spring Cloud Azure startup property source, so there is no client object in the repository to probe. A responsible indicator cannot be written until **P1-011** (`CHANGE-AA-022`) introduces an explicit, bounded Key Vault client.

**Unresolved inputs:**

* Whether Key Vault participates in readiness or is deliberately excluded after startup
* The explicit Key Vault client introduced by `CHANGE-AA-022`

**Intended behavior:** Controls `KV-006` and `KV-014` require Key Vault either to participate in readiness or to be deliberately excluded with a recorded rationale.

**Notes:**

* **Cross-refs:** Prerequisite for **P0-011** (drain must withdraw readiness first) and **P2-005** (a fail-closed rate limiter makes Redis a readiness dependency). Coordinated with **P1-010**, which rewrites the same management block. Depends on **P0-012**.
* **Implementation:** `CHANGE-AA-003`, Wave 2, complexity medium. Touches all eight `application.yml` files, `order-service/Dockerfile`, and `k8s/services/all-services.yaml`. Five of six targets carry generated code.
* **Validation:** T-AA-003-01 (readiness transition and restoration without restart), T-AA-003-02 (bounded and cached probe), T-AA-003-03 (liveness group contains no external dependency). `mvn -f source/customer-app/pom.xml -pl common -am test`; `mvn -f source/customer-app/pom.xml verify`.
* **Guardrail:** The readiness group must contain only **region-local critical** dependencies. Adding a globally shared dependency would remove both regions from rotation simultaneously. Optional dependencies such as Redis in `product-service` must not be added because a safe degraded mode exists. `OQ-03` records that the critical-versus-optional classification per service is not yet decided.

<span style="font-size: 14px;">**MSFT Reference:** [Health Endpoint Monitoring pattern](https://learn.microsoft.com/azure/architecture/patterns/health-endpoint-monitoring)</span>

---

#### Regional State Portability

#### P0-004: Notification state is held in an unbounded in-process map

**Priority: P0 - Critical Immediate Action**

**Priority policy:** `AA-REMEDIATION-PRIORITY` v1.0.0, rule `P0-AA-005` · **Change ID:** `CHANGE-AA-004` (Wave 3) · **Source ID:** F-028 · **Primary control:** `APP-AA-010`

**Severity:** Critical

**Resiliency Related:** Yes

**Finding status:** Verified finding

**Issue:** `NotificationRepository` stores every dispatched notification in a `ConcurrentHashMap` held in the process, keyed by a freshly generated UUID. The class documents itself as requiring replacement with a persistent store. The map has no eviction, no size bound, and no read method, so entries accumulate for the lifetime of the pod and are unreachable.

**What does this solve:** It removes the region-local volatile state that blocks regional traffic movement, supplies the durable record that consumer-side deduplication requires, and eliminates the slow memory leak.

**Resiliency Impact:** The notification record is pod-local and region-local, so it cannot support deduplication, audit, or resend after a pod restart or a regional transition. Unbounded growth also produces a slow memory leak that terminates the pod under sustained load. Under `active_standby`, a promoted region cannot determine whether a notification was already dispatched by the previously active region and will re-send it blindly.

**Recommended Fix:** Introduce a technology-neutral `NotificationStore` contract exposing a conditional write keyed by a stable notification identity plus a read path, claim the identity durably before the non-idempotent SMTP dispatch, and replace the in-process map with a durable adapter.

**File:** source/customer-app/notification-service/src/main/java/com/ecommerce/notification/repository/NotificationRepository.java:10-25

```java
// before
/**
 * In-memory notification log repository.
 * Replace with persistent store (Cosmos DB or SQL) in production.
 */
@Slf4j
@Repository
public class NotificationRepository {

    private final Map<String, NotificationRecord> store = new ConcurrentHashMap<>();

    public void save(String customerId, String type, String title, String message, String channel) {
        String id = UUID.randomUUID().toString();
        store.put(id, new NotificationRecord(id, customerId, type, title, message, channel,
                java.time.LocalDateTime.now()));
        log.debug("Saved notification {} for customer {}", id, customerId);
    }
```

**Fix:**

> Illustrative proposal only.

`source/customer-app/notification-service/src/main/java/com/ecommerce/notification/repository/NotificationStore.java`

```java
package com.ecommerce.notification.repository;

import java.time.LocalDateTime;
import java.util.Optional;

/**
 * Durable notification record contract. Implementations must survive process restart and
 * must be readable from any replica in any region.
 */
public interface NotificationStore {

    /**
     * Records the notification exactly once for the supplied stable identity.
     *
     * @return true when this call created the record, false when the identity already
     *         existed and the side effect must not be repeated.
     */
    boolean saveIfAbsent(NotificationRecord record);

    Optional<NotificationRecord> findByNotificationId(String notificationId);

    boolean existsByNotificationId(String notificationId);

    record NotificationRecord(
            String notificationId,
            String sourceEventId,
            String customerId,
            String type,
            String title,
            String message,
            String channel,
            LocalDateTime createdAt) {
    }
}
```

Establishes the durable contract and the deduplication primitive without selecting a persistence technology. `notificationId` is a stable identity supplied by the caller rather than a per-call random UUID, and `sourceEventId` preserves the originating Kafka event identity introduced by **P2-001**. `saveIfAbsent` returns whether this call created the record so the caller can suppress a duplicate email.

`source/customer-app/notification-service/src/main/java/com/ecommerce/notification/service/NotificationEventConsumer.java` — `saveNotification` and `handleOrderCreated`

```java
private final NotificationStore notificationStore;

@KafkaListener(topics = KafkaTopics.ORDER_CREATED, groupId = KafkaTopics.GROUP_NOTIFICATION_SERVICE)
public void handleOrderCreated(Map<String, Object> event) {
    String eventId = (String) event.get("eventId");
    String customerId = (String) event.get("customerId");
    String customerEmail = (String) event.get("customerEmail");
    String orderNumber = (String) event.get("orderNumber");
    Object total = event.get("totalAmount");

    String notificationId = notificationId(eventId, "ORDER_CREATED", "EMAIL");

    NotificationStore.NotificationRecord record = new NotificationStore.NotificationRecord(
            notificationId,
            eventId,
            customerId,
            "ORDER_CREATED",
            "Order Confirmation",
            "Your order " + orderNumber + " has been placed successfully.",
            "EMAIL",
            LocalDateTime.now());

    if (!notificationStore.saveIfAbsent(record)) {
        log.info("Notification {} already recorded; suppressing duplicate email", notificationId);
        return;
    }

    emailService.sendOrderConfirmation(customerEmail, orderNumber, total.toString());
}

private String notificationId(String eventId, String type, String channel) {
    return eventId + ":" + type + ":" + channel;
}
```

The record is claimed durably before the non-idempotent SMTP dispatch, so a replay or a regional promotion cannot re-send the same email. The log-and-swallow catch is removed so the listener container can apply the error and dead-letter contract introduced by **P2-003**, and the `@Async` annotation is removed by **P2-002**.

**Illustrative code status:** Targeted implementation discovery required (`TD-03`)

**Target:** Durable `NotificationStore` adapter — repository path not yet selected

**Why code was not generated:** The approved durable store for notification records has not been selected. The class comment names both Cosmos DB and SQL as candidates, `notification-service` declares neither a datasource nor a Cosmos configuration today, and selecting one is an architecture decision rather than a repository fact. Writing an adapter would require inventing a schema, partition key, or entity mapping that no approved decision supports.

**Unresolved inputs:**

* Approved durable store for notification records (Azure SQL, Cosmos DB, or other)
* Partition or index strategy that makes `notificationId` uniqueness enforceable
* Retention policy for notification records

**Intended behavior:** A durable adapter must implement `saveIfAbsent` with a store-enforced uniqueness guarantee on `notificationId`, plus a retention policy so the store does not grow without bound.

**Notes:**

* **Cross-refs:** Depends on **P2-001** (stable event identity) and **P0-012**. Prerequisite for **P2-002**. Introduces a new critical dependency that must be reflected in the **P0-003** readiness group.
* **Implementation:** `CHANGE-AA-004`, Wave 3, complexity high. Three of four targets carry generated code. Decision gate `durable_notification_store` (`OQ-06`) blocks completion.
* **Validation:** T-AA-004-01 (claim-once and read-back contract), T-AA-004-02 (cross-instance durability), T-AA-004-03 (no per-notification process memory). `mvn -f source/customer-app/pom.xml -pl common,notification-service -am test`.
* **Guardrail:** The `notificationId` format is a new contract and must be stable across regions and across redeploys. An in-memory adapter may be retained for local development only, never for production profiles.

<span style="font-size: 14px;">**MSFT Reference:** [Reliability design principles — Azure Well-Architected Framework](https://learn.microsoft.com/azure/well-architected/reliability/principles)</span>

---

#### Authoritative Data Correctness

#### P0-005: Cosmos writes are non-atomic read-modify-write with unused optimistic concurrency

**Priority: P0 - Critical Immediate Action**

**Priority policy:** `AA-REMEDIATION-PRIORITY` v1.0.0, rule `P0-AA-006` (elevated from candidate `P2-DATA-004`) · **Change ID:** `CHANGE-AA-005` (Wave 3) · **Source ID:** F-004 · **Primary control:** `COSMOS-005`

**Severity:** Critical

**Resiliency Related:** Yes

**Finding status:** Verified finding

**Issue:** Every stock mutation reads the whole inventory document, mutates it in memory, and saves a full replacement. `canReserve` is a check-then-act with no conditional update, stored procedure, or transactional batch. The declared `@Version` etag on `InventoryDocument` is never read or compared. Each reserve call also mints a new reservation identifier, so a retried reservation for the same order creates a second reservation.

**What does this solve:** It eliminates lost updates and oversell under concurrent or cross-region reservation, and makes a retried reservation idempotent.

**Resiliency Impact:** Concurrent reservations from different replicas or regions silently overwrite one another, oversell physical stock, and produce reservation records with no idempotent identity. Stock commitment is a critical business transaction and the overwrite is silent, which is why the `P2-DATA-004` candidate was elevated to P0 under `P0-AA-006`. Under `active_standby`, a reservation replayed after a promotion double-reserves stock.

**Recommended Fix:** Derive a deterministic `reservationId` from `orderId` and `productId`, return the existing reservation when that identity already exists, and perform the mutate-and-save inside a bounded optimistic-concurrency retry that re-reads on conflict. Exhausted retries must surface a typed conflict rather than a silent overwrite.

**File:** source/customer-app/inventory-service/src/main/java/com/ecommerce/inventory/service/InventoryService.java:136-160

```java
// before
    public ReservationResponse reserveStock(ReserveStockRequest request) {
        InventoryDocument inv = getInventoryDocument(request.getProductId());

        if (!inv.canReserve(request.getQuantity())) {
            throw new InsufficientInventoryException(
                    request.getProductId(), request.getQuantity(), inv.getAvailableQuantity());
        }

        String reservationId = UUID.randomUUID().toString();
        StockReservation reservation = StockReservation.builder()
                .reservationId(reservationId)
                .orderId(request.getOrderId())
                .customerId(request.getCustomerId())
                .quantity(request.getQuantity())
                .status("ACTIVE")
                .reservedAt(LocalDateTime.now())
                .expiresAt(LocalDateTime.now().plusMinutes(RESERVATION_TTL_MINUTES))
                .build();

        inv.getReservations().add(reservation);
        inv.setReservedQuantity(inv.getReservedQuantity() + request.getQuantity());
        inv.adjustAvailableQuantity();
        inv.setUpdatedAt(LocalDateTime.now());

        inventoryRepository.save(inv);
```

**File:** source/customer-app/inventory-service/src/main/java/com/ecommerce/inventory/document/InventoryDocument.java:74-75 — `@Version private String etag`

> Original source excerpt: Not available in authoritative evidence artifact. Step 2 evidence `EV-F-004-02` records the field as cited by the authoritative inventory; it exists but is never read, compared, or used in conflict handling anywhere in the service.

**Fix:**

> Illustrative proposal only.

`source/customer-app/inventory-service/src/main/java/com/ecommerce/inventory/service/InventoryService.java` — `reserveStock`

```java
@Value("${app.inventory.reservation.max-conflict-retries:5}")
private int maxConflictRetries;

public ReservationResponse reserveStock(ReserveStockRequest request) {
    String reservationId = reservationId(request.getOrderId(), request.getProductId());

    for (int attempt = 0; attempt <= maxConflictRetries; attempt++) {
        InventoryDocument inv = getInventoryDocument(request.getProductId());

        StockReservation existing = inv.findReservation(reservationId);
        if (existing != null) {
            // Idempotent replay of the same order/product reservation.
            return toReservationResponse(inv, existing);
        }

        if (!inv.canReserve(request.getQuantity())) {
            throw new InsufficientInventoryException(
                    request.getProductId(), request.getQuantity(), inv.getAvailableQuantity());
        }

        StockReservation reservation = StockReservation.builder()
                .reservationId(reservationId)
                .orderId(request.getOrderId())
                .customerId(request.getCustomerId())
                .quantity(request.getQuantity())
                .status("ACTIVE")
                .reservedAt(LocalDateTime.now())
                .expiresAt(LocalDateTime.now().plusMinutes(reservationTtlMinutes))
                .build();

        inv.getReservations().add(reservation);
        inv.setReservedQuantity(inv.getReservedQuantity() + request.getQuantity());
        inv.adjustAvailableQuantity();
        inv.setUpdatedAt(LocalDateTime.now());

        try {
            // The @Version etag carried by inv makes this a conditional write.
            InventoryDocument saved = inventoryRepository.save(inv);
            return toReservationResponse(saved, reservation);
        } catch (OptimisticLockingFailureException conflict) {
            log.warn("Reservation conflict for product {} attempt {} of {}",
                    request.getProductId(), attempt + 1, maxConflictRetries + 1);
        }
    }

    throw new InventoryConflictException(request.getProductId(), reservationId, maxConflictRetries);
}

/** Deterministic reservation identity so a retried reserve is idempotent. */
private String reservationId(String orderId, String productId) {
    return "RSV-" + orderId + "-" + productId;
}
```

The random UUID reservation identifier is replaced by a deterministic identity derived from the caller's order and product, so a retry resolves to the existing reservation instead of creating a second one. The save is retried only on `OptimisticLockingFailureException`, which Spring Data raises when the etag no longer matches, so the previously declared but unused `@Version` field now performs real conflict detection. The retry budget is externally configurable and exhaustion raises a typed conflict rather than silently overwriting.

`source/customer-app/inventory-service/src/main/java/com/ecommerce/inventory/document/InventoryDocument.java` — `findReservation`

```java
/** Returns the reservation carrying the supplied stable identity, or null when absent. */
public StockReservation findReservation(String reservationId) {
    if (reservations == null) {
        return null;
    }
    return reservations.stream()
            .filter(r -> reservationId.equals(r.getReservationId()))
            .findFirst()
            .orElse(null);
}
```

Supplies the identity lookup the idempotent reserve path needs. The `@Version` etag field itself is unchanged; the behavioral change is that callers now handle the conflict it raises.

**Notes:**

* **Cross-refs:** Depends on **P1-002** (Cosmos failure classification must classify 409 and 412 as CONFLICT) and **P0-012**. Related to **P0-010**, which saves the same documents under the etag during the expiry sweep.
* **Implementation:** `CHANGE-AA-005`, Wave 3, complexity high. All three targets carry generated code.
* **Validation:** T-AA-005-01 (two simultaneous reservations for the last unit yield one success and one conflict), T-AA-005-02 (retried reserve returns the same reservation identity). `mvn -f source/customer-app/pom.xml -pl common,inventory-service -am test`.
* **Guardrail:** A hot inventory document can exhaust the conflict budget under high contention; the budget and the document granularity must be tuned together. The `reservationId` format changes from a UUID to a deterministic string, so any consumer that parses reservation identifiers must be reviewed. `OQ-07` records a path discrepancy: Step 1 cites `com.ecommerce.inventory.model`, Step 2 evidence cites `com.ecommerce.inventory.document`; the Step 2 path is used.

<span style="font-size: 14px;">**MSFT Reference:** [Optimistic concurrency control in Azure Cosmos DB](https://learn.microsoft.com/azure/cosmos-db/nosql/database-transactions-optimistic-concurrency)</span>

---

#### P0-006: Payment processing has no durable idempotency key and calls the provider inside the transaction

**Priority: P0 - Critical Immediate Action**

**Priority policy:** `AA-REMEDIATION-PRIORITY` v1.0.0, rule `P0-AA-006` (elevated from candidate `P2-DATA-001`) · **Change ID:** `CHANGE-AA-006` (Wave 3) · **Source ID:** F-012 · **Primary control:** `APP-FIN-001`

**Severity:** Critical

**Resiliency Related:** Yes

**Finding status:** Verified finding

**Issue:** `PaymentService` is class-level `@Transactional`. It saves a pending payment, then performs a fraud check and the gateway call inside the same transaction, then saves the result and publishes an event. Idempotency is a read-then-act `existsByOrderIdAndStatusIn` check. The payments DDL declares `idempotency_key NVARCHAR(200) NOT NULL UNIQUE`, but no `PaymentEntity` field maps to it. `PaymentGatewayService` returns a simulated approval and mints a new transaction id per attempt.

**What does this solve:** It converts a racy read-then-act check into a store-enforced guarantee, removes the external call from the transaction boundary, and makes an unknown provider outcome recoverable by lookup instead of by repetition.

**Resiliency Impact:** A retry after an ambiguous outcome creates a second payment row and a second provider effect. Two concurrent requests can both pass the `exists` check. A durable intent boundary and a stable operation identity are both absent, so a regional interruption during payment cannot be reconciled. This makes a critical financial transaction materially unsafe under active-active operation, which is why the `P2-DATA-001` candidate was elevated to P0 under `P0-AA-006`.

**Recommended Fix:** Accept a caller-supplied idempotency key, map the existing unique `idempotency_key` column onto the entity so the database enforces single execution, commit the payment intent in a short transaction, then call the provider outside any open transaction carrying the same key as the provider operation identity, and record the outcome in a second short transaction.

**File:** source/customer-app/payment-service/src/main/java/com/ecommerce/payment/service/PaymentService.java:44-51

```java
// before
    public PaymentResponse processPayment(ProcessPaymentRequest request) {
        log.info("Processing payment for order: {}", request.getOrderId());

        // Idempotency check - don't process same order twice
        if (paymentRepository.existsByOrderIdAndStatusIn(request.getOrderId(),
                java.util.List.of(PaymentStatus.CAPTURED, PaymentStatus.AUTHORIZED))) {
            throw new BusinessException("Payment already processed for order: " + request.getOrderId());
        }
```

**File:** source/customer-app/payment-service/src/main/java/com/ecommerce/payment/service/PaymentService.java:72-89

```java
// before
            payment = paymentRepository.save(payment);

            try {
                // Fraud check first
                FraudCheckResult fraudResult = gatewayService.performFraudCheck(payment);
                payment.setRiskScore(fraudResult.getRiskScore());
                payment.setFraudCheckStatus(fraudResult.getStatus());

                if ("BLOCKED".equals(fraudResult.getStatus())) {
                    payment.setStatus(PaymentStatus.FAILED);
                    payment.setFailureReason("Transaction blocked by fraud detection");
                    payment.setFailedAt(LocalDateTime.now());
                    paymentRepository.save(payment);
                    publishPaymentFailedEvent(payment, "FRAUD_DETECTED");
                    throw new PaymentException("Transaction declined for security reasons", payment.getId(), "FRAUD_DETECTED");
                }

                // Process through payment gateway
                GatewayResponse gatewayResponse = gatewayService.processPayment(request, payment.getId());
```

**File:** source/customer-app/payment-service/src/main/java/com/ecommerce/payment/service/PaymentGatewayService.java:49-66

```java
// before
    public GatewayResponse processPayment(ProcessPaymentRequest request, String internalPaymentId) {
        log.info("Sending payment to gateway for order: {}", request.getOrderId());

        // Simulated gateway call (production: Stripe API, etc.)
        // In real implementation, use Azure Key Vault for API keys
        try {
            // Simulate gateway response
            boolean success = simulateGatewaySuccess(request);

            if (success) {
                String transactionId = "TXN-" + UUID.randomUUID().toString().substring(0, 12).toUpperCase();
                return GatewayResponse.builder()
                        .success(true)
                        .transactionId(transactionId)
                        .reference(internalPaymentId)
                        .responseCode("00")
                        .message("Payment approved")
                        .build();
```

**File:** source/customer-app/payment-service/src/main/resources/db/migration:11-55 — payments DDL `idempotency_key` and `UQ_payments_idempotency_key`

> Original source excerpt: Not available in authoritative evidence artifact. Step 2 evidence `EV-F-012-04` records that the unique `idempotency_key` column exists in the schema with no mapped `PaymentEntity` field, so the constraint cannot be satisfied by the application.

**Fix:**

> Illustrative proposal only.

`source/customer-app/payment-service/src/main/java/com/ecommerce/payment/entity/PaymentEntity.java` — `idempotencyKey` field mapping *(path confidence: unconfirmed)*

```java
@Column(name = "idempotency_key", length = 200, nullable = false, updatable = false, unique = true)
private String idempotencyKey;
```

Maps the existing payments DDL column and its constraint `UQ_payments_idempotency_key` onto the entity so the database can enforce single execution. Today the column exists and nothing maps to it, which is why `ddl-auto: validate` and the unique constraint provide no protection.

`source/customer-app/payment-service/src/main/java/com/ecommerce/payment/service/PaymentService.java` — `processPayment`

```java
// Class-level @Transactional is removed; each boundary is declared explicitly.
public PaymentResponse processPayment(ProcessPaymentRequest request, String idempotencyKey) {
    log.info("Processing payment for order: {} key: {}", request.getOrderId(), idempotencyKey);

    PaymentEntity intent;
    try {
        intent = recordIntent(request, idempotencyKey);
    } catch (DataIntegrityViolationException duplicate) {
        // The unique idempotency_key constraint rejected a concurrent or retried attempt.
        return paymentRepository.findByIdempotencyKey(idempotencyKey)
                .map(this::toResponse)
                .orElseThrow(() -> new BusinessException(
                        "Idempotency key conflict without a readable payment: " + idempotencyKey));
    }

    if (intent.getStatus() != PaymentStatus.PENDING) {
        // Already resolved by a previous attempt; return the recorded outcome.
        return toResponse(intent);
    }

    // Provider effect happens outside any open database transaction.
    FraudCheckResult fraudResult = gatewayService.performFraudCheck(intent);
    if ("BLOCKED".equals(fraudResult.getStatus())) {
        PaymentEntity blocked = recordFraudBlock(intent.getId(), fraudResult);
        publishPaymentFailedEvent(blocked, "FRAUD_DETECTED");
        throw new PaymentException("Transaction declined for security reasons",
                blocked.getId(), "FRAUD_DETECTED");
    }

    GatewayResponse gatewayResponse =
            gatewayService.processPayment(request, intent.getId(), idempotencyKey);

    return toResponse(recordGatewayOutcome(intent.getId(), fraudResult, gatewayResponse));
}

@Transactional
protected PaymentEntity recordIntent(ProcessPaymentRequest request, String idempotencyKey) {
    PaymentEntity payment = PaymentEntity.builder()
            .orderId(request.getOrderId())
            .idempotencyKey(idempotencyKey)
            .status(PaymentStatus.PENDING)
            .build();
    return paymentRepository.saveAndFlush(payment);
}

@Transactional
protected PaymentEntity recordGatewayOutcome(String paymentId,
                                             FraudCheckResult fraudResult,
                                             GatewayResponse gatewayResponse) {
    PaymentEntity payment = paymentRepository.findById(paymentId).orElseThrow();
    payment.setRiskScore(fraudResult.getRiskScore());
    payment.setFraudCheckStatus(fraudResult.getStatus());
    if (gatewayResponse.isSuccess()) {
        payment.setStatus(PaymentStatus.CAPTURED);
        payment.setTransactionId(gatewayResponse.getTransactionId());
    } else {
        payment.setStatus(PaymentStatus.FAILED);
        payment.setFailureReason(gatewayResponse.getMessage());
        payment.setFailedAt(LocalDateTime.now());
    }
    return paymentRepository.save(payment);
}
```

The racy `existsByOrderIdAndStatusIn` check is replaced by an insert whose uniqueness is enforced by the database, so two concurrent requests cannot both proceed. The provider call moves outside the transaction so a long or hung external call can no longer hold a database transaction open, and an ambiguous outcome leaves a committed `PENDING` intent that can be reconciled by key. Task Implementor must confirm the proxying strategy for the `protected @Transactional` methods or extract them into a collaborating bean.

`source/customer-app/payment-service/src/main/java/com/ecommerce/payment/service/PaymentGatewayService.java` — `processPayment`

```java
public GatewayResponse processPayment(ProcessPaymentRequest request,
                                      String internalPaymentId,
                                      String idempotencyKey) {
    log.info("Sending payment to gateway for order: {} key: {}",
            request.getOrderId(), idempotencyKey);

    // The stable operation identity travels with the provider call so a retried
    // attempt resolves to the same provider-side operation instead of creating a new one.
    boolean success = simulateGatewaySuccess(request);

    if (success) {
        return GatewayResponse.builder()
                .success(true)
                .transactionId(idempotencyKey)
                .reference(internalPaymentId)
                .responseCode("00")
                .message("Payment approved")
                .build();
    }
    return GatewayResponse.builder()
            .success(false)
            .reference(internalPaymentId)
            .responseCode("05")
            .message("Payment declined")
            .build();
}
```

The locally minted per-attempt transaction id is replaced by the stable idempotency key, so a retried attempt no longer produces a new provider-side identity. The simulation is retained because replacing it with a real provider integration is outside the scope of the approved finding.

**Illustrative code status:** Targeted implementation discovery required (`TD-04`)

**Target:** Provider status-lookup reconciliation for an unknown outcome — repository path not yet selected

**Why code was not generated:** The real payment provider contract is unresolved. `PaymentGatewayService` is an in-process simulation with no HTTP client, no provider SDK, and no documented status-lookup operation, so the lookup call, its identity semantics, and its error contract cannot be responsibly illustrated without inventing an external API.

**Unresolved inputs:**

* Approved payment provider and its idempotent-create and status-lookup contract
* Whether reconciliation runs as a scheduled sweep gated by `CHANGE-AA-009` ownership or as an on-demand lookup

**Intended behavior:** Control `SQL-012` requires a status lookup or reconciliation path for an unknown commit or provider outcome so a committed `PENDING` intent is eventually resolved.

**Notes:**

* **Cross-refs:** Prerequisite for **P1-006** (retry must never be applied to a non-idempotent provider call) and **P2-004** (`order-service` must propagate the same key). Depends on **P1-004** and **P0-012**.
* **Implementation:** `CHANGE-AA-006`, Wave 3, complexity high. Three of four targets carry generated code.
* **Validation:** T-AA-006-01 (same key twice yields one row and one provider effect), T-AA-006-02 (two concurrent requests with the same key yield one insert), T-AA-006-03 (no transaction open during the provider call). `mvn -f source/customer-app/pom.xml -pl common,payment-service -am test`.
* **Guardrail:** Removing class-level `@Transactional` changes the transaction boundary for every other `PaymentService` method and requires a method-by-method review. Existing payment rows have no `idempotency_key` value, so a backfill or nullable-then-tighten migration sequence is required. `OQ-09` records that the exact `PaymentEntity` path is unconfirmed and that `UNC-007` documents duplicate `com.ecommerce.payment` and `com.ecommerce.paymentservice` packages.

<span style="font-size: 14px;">**MSFT Reference:** [Compensating Transaction pattern](https://learn.microsoft.com/azure/architecture/patterns/compensating-transaction)</span>

---
#### P0-007: Database commit and event publish share one transaction with no outbox or reconciliation

**Priority: P0 - Critical Immediate Action**

**Priority policy:** `AA-REMEDIATION-PRIORITY` v1.0.0, rule `P0-AA-006` (elevated from candidate `P2-DATA-003`) · **Change ID:** `CHANGE-AA-007` (Wave 3) · **Source ID:** F-011 · **Primary control:** `APP-DB-003`

**Severity:** Critical

**Resiliency Related:** Yes

**Finding status:** Verified finding

**Issue:** Service classes are annotated `@Transactional` at class level. Every write path saves to Azure SQL or Cosmos DB and then calls `KafkaTemplate.send` inside the same transaction. There is no outbox table, no `TransactionSynchronization`, no `@TransactionalEventListener`, no `KafkaTransactionManager`, and no transactional id.

**What does this solve:** It removes the dual-write divergence between the authoritative store and Kafka, gives the system a reconciliation marker after a regional interruption, and converts a silent publish failure into an observable, recoverable condition.

**Resiliency Impact:** A rollback after a successful publish emits an event for state that does not exist, and a failed publish after a commit loses the event permanently. No durable marker exists to reconcile the two stores after a regional interruption. Under `active_standby`, the outbox relay is itself a Kafka producer workload and must participate in the ownership gate so the standby region does not republish.

**Recommended Fix:** Record the domain event into an outbox row inside the same database transaction as the business state, and have a separate ownership-gated relay claim unsent rows, publish them, observe the send result with a bounded timeout, and mark the row sent only on acknowledged delivery.

**File:** source/customer-app/order-service/src/main/java/com/ecommerce/order/service/OrderService.java:33-34

```java
// before
@Transactional
public class OrderService {
```

**File:** source/customer-app/order-service/src/main/java/com/ecommerce/order/service/OrderService.java:379-380

```java
// before
                event.put("timestamp", LocalDateTime.now().toString());
                kafkaTemplate.send(topic, order.getId(), event);
```

**File:** source/customer-app/payment-service/src/main/java/com/ecommerce/payment/service/PaymentService.java:27-31

```java
// before
@Service
@RequiredArgsConstructor
@Transactional
public class PaymentService {
```

**Fix:**

> Illustrative proposal only.

`source/customer-app/order-service/src/main/java/com/ecommerce/order/outbox/OutboxEvent.java`

```java
package com.ecommerce.order.outbox;

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.EnumType;
import jakarta.persistence.Enumerated;
import jakarta.persistence.Id;
import jakarta.persistence.Lob;
import jakarta.persistence.Table;
import jakarta.persistence.Version;
import java.time.LocalDateTime;

@Entity
@Table(name = "outbox_events")
public class OutboxEvent {

    public enum Status { PENDING, SENT, FAILED }

    @Id
    @Column(name = "event_id", length = 64, nullable = false, updatable = false)
    private String eventId;

    @Column(name = "topic", length = 200, nullable = false, updatable = false)
    private String topic;

    @Column(name = "message_key", length = 200, nullable = false, updatable = false)
    private String messageKey;

    @Lob
    @Column(name = "payload", nullable = false, updatable = false)
    private String payload;

    @Enumerated(EnumType.STRING)
    @Column(name = "status", length = 20, nullable = false)
    private Status status = Status.PENDING;

    @Column(name = "attempt_count", nullable = false)
    private int attemptCount;

    @Column(name = "created_at", nullable = false, updatable = false)
    private LocalDateTime createdAt;

    @Column(name = "sent_at")
    private LocalDateTime sentAt;

    @Column(name = "last_error", length = 1000)
    private String lastError;

    @Version
    @Column(name = "version", nullable = false)
    private long version;

    // getters and setters omitted for brevity
}
```

The durable marker that today does not exist. `eventId` is the stable event identity produced by **P2-001**, so the outbox row and the published record share one identity and a consumer can deduplicate. The `@Version` column matches the optimistic-locking convention already used by `OrderEntity` and `PaymentEntity`.

`source/customer-app/order-service/src/main/java/com/ecommerce/order/service/OrderService.java` — `publishOrderEvent`

```java
/**
 * Records the domain event in the outbox inside the caller's transaction. No broker call is
 * made here, so the business transaction can no longer commit without its event or emit an
 * event for state that was rolled back.
 */
private void publishOrderEvent(String topic, OrderEntity order, String detail) {
    Map<String, Object> event = new HashMap<>();
    String eventId = UUID.randomUUID().toString();
    event.put("eventId", eventId);
    event.put("eventType", topic);
    event.put("correlationId", CorrelationContext.currentCorrelationId());
    event.put("sourceService", "order-service");
    event.put("orderId", order.getId());
    event.put("orderNumber", order.getOrderNumber());
    event.put("customerId", order.getCustomerId());
    event.put("customerEmail", order.getCustomerEmail());
    event.put("status", order.getStatus().name());
    event.put("totalAmount", order.getTotalAmount());
    event.put("paymentId", order.getPaymentId());
    event.put("detail", detail);
    event.put("occurredAt", OffsetDateTime.now(ZoneOffset.UTC).toString());

    outboxEventRepository.save(
            OutboxEvent.pending(eventId, topic, order.getId(), objectMapper.writeValueAsString(event)));
}
```

The in-transaction broker call is replaced by an in-transaction outbox insert, so the commit and the intent to publish share one atomic boundary. The payload now carries the stable `eventId` and `correlationId` required by **P2-001** and **P3-002**, and `occurredAt` uses an offset-bearing timestamp instead of the zone-less `LocalDateTime` recorded by the inventory.

`source/customer-app/order-service/src/main/java/com/ecommerce/order/outbox/OutboxRelay.java`

```java
package com.ecommerce.order.outbox;

import java.time.Duration;
import java.time.LocalDateTime;
import java.util.List;
import java.util.concurrent.TimeUnit;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.data.domain.Limit;
import org.springframework.kafka.core.KafkaTemplate;
import org.springframework.scheduling.annotation.Scheduled;
import org.springframework.stereotype.Component;
import org.springframework.transaction.annotation.Transactional;

@Slf4j
@Component
@RequiredArgsConstructor
public class OutboxRelay {

    private final OutboxEventRepository outboxEventRepository;
    private final KafkaTemplate<String, String> kafkaTemplate;
    private final WorkloadOwnershipGuard ownershipGuard;
    private final io.micrometer.core.instrument.MeterRegistry meterRegistry;

    @Value("${app.outbox.batch-size:100}")
    private int batchSize;

    @Value("${app.outbox.delivery-timeout-ms:10000}")
    private long deliveryTimeoutMs;

    @Scheduled(fixedDelayString = "${app.outbox.poll-interval-ms:2000}")
    @Transactional
    public void relayPendingEvents() {
        if (!ownershipGuard.isOwner()) {
            return;
        }
        List<OutboxEvent> pending = outboxEventRepository
                .findByStatusOrderByCreatedAtAsc(OutboxEvent.Status.PENDING, Limit.of(batchSize));

        for (OutboxEvent event : pending) {
            try {
                kafkaTemplate
                        .send(event.getTopic(), event.getMessageKey(), event.getPayload())
                        .get(deliveryTimeoutMs, TimeUnit.MILLISECONDS);
                event.markSent(LocalDateTime.now());
                meterRegistry.counter("outbox.events.sent", "topic", event.getTopic()).increment();
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
                return;
            } catch (Exception e) {
                event.markAttemptFailed(e.getClass().getSimpleName() + ": " + e.getMessage());
                meterRegistry.counter("outbox.events.delivery_failed",
                        "topic", event.getTopic()).increment();
                log.error("Outbox delivery failed for event {} topic {}",
                        event.getEventId(), event.getTopic(), e);
            }
        }
        outboxEventRepository.saveAll(pending);
    }

    public Duration deliveryTimeout() {
        return Duration.ofMillis(deliveryTimeoutMs);
    }
}
```

The send result is awaited with a bounded timeout, an acknowledged delivery marks the row sent, and any failure increments a distinct metric and leaves the row `PENDING` for the next pass. The relay is a Kafka producer workload, so it is gated by the same ownership guard as every other authoritative workload rather than running in both regions.

**Illustrative code status:** Targeted implementation discovery required (`TD-05`)

**Target:** `outbox_events` table migration for `order-service` — repository path not yet selected

**Why code was not generated:** `order-service` runs with `ddl-auto: validate` but the inventory records a schema-management tool only for `user-service` and `payment-service`. The migration mechanism for the `ecommerce_orders` database is not established by the supplied artifacts, and `UNC-008` records that the existing Azure SQL DDL scripts already diverge from their entity mappings. Emitting a migration without knowing the tool, the baseline version, or the naming convention would invent a repository fact.

**Unresolved inputs:**

* Schema-management tool and migration directory for the `ecommerce_orders` database
* Current migration baseline version and file-naming convention for `order-service`

**Intended behavior:** The `outbox_events` table must be created in the `ecommerce_orders` database with a primary key on `event_id` and an index supporting the pending-by-created-at read.

**Notes:**

* **Cross-refs:** Consolidates **P0-008** (F-005) as a symptom of the same root cause. Depends on **P0-009** (ownership gate), **P2-001** (stable identity, a hard correctness prerequisite), and **P0-012**. Shares the schema-migration decision gate with **P2-004**.
* **Implementation:** `CHANGE-AA-007`, Wave 3, complexity high. Four of five targets carry generated code.
* **Validation:** T-AA-007-01 (rollback emits no event), T-AA-007-02 (broker failure after commit leaves a PENDING row delivered on the next pass), T-AA-007-03 (delivery failure increments `outbox.events.delivery_failed`). `mvn -f source/customer-app/pom.xml -pl common,order-service,payment-service -am test`.
* **Guardrail:** The outbox introduces at-least-once delivery, which makes consumer-side deduplication mandatory — **P2-001** is a hard prerequisite for correctness, not a nice-to-have. Removing class-level `@Transactional` from `OrderService` changes boundaries for every method in the class. Rolling back with unsent outbox rows present would strand those events; drain the outbox before reverting.

<span style="font-size: 14px;">**MSFT Reference:** [Transactional Outbox pattern with Azure Cosmos DB](https://learn.microsoft.com/azure/architecture/databases/guide/transactional-outbox-cosmos)</span>

---

#### P0-008: Kafka producer send results are discarded and publish failures are swallowed

**Priority: P0 - Critical Immediate Action**

**Priority policy:** `AA-REMEDIATION-PRIORITY` v1.0.0, rule `P0-AA-006` · **Change ID:** `CHANGE-AA-007` (Wave 3, consolidated under root cause) · **Source ID:** F-005 · **Primary control:** `APP-KAFKA-005`

**Severity:** Critical

**Resiliency Related:** Yes

**Finding status:** Verified finding — **consolidated** under `CHANGE-AA-007` with **P0-007** as the primary finding

**Issue:** `KafkaTemplate.send` returns a `CompletableFuture` that is never inspected. The surrounding `try/catch` captures only synchronous throws, logs the message, and allows the caller to return success. Asynchronous delivery failure is therefore invisible.

**What does this solve:** It makes delivery failure a durable, countable, retryable condition instead of a log line that the caller never sees.

**Resiliency Impact:** A broker outage or partition unavailability during regional degradation silently drops domain events while the originating transaction commits, so downstream consumers, notifications, and inventory reactions never occur and no signal is emitted. Under `active_standby`, a promotion cannot be reconciled because no durable record of the intended publication exists.

**Recommended Fix:** Move publication behind the durable outbox introduced by **P0-007** and have the relay await the send result with a bounded timeout, mark the row sent only on acknowledged delivery, and increment a distinct delivery-failure metric on any failure. Step 3A consolidated this finding under `CHANGE-AA-007` because a single transactional-outbox remediation satisfies both symptoms and splitting them would produce duplicate proposals over the same `OrderService` and `PaymentService` symbols.

**File:** source/customer-app/order-service/src/main/java/com/ecommerce/order/service/OrderService.java:368-384

```java
// before
    private void publishOrderEvent(String topic, OrderEntity order, String detail) {
        try {
            Map<String, Object> event = new HashMap<>();
            event.put("orderId", order.getId());
            event.put("orderNumber", order.getOrderNumber());
            event.put("customerId", order.getCustomerId());
            event.put("customerEmail", order.getCustomerEmail());
            event.put("status", order.getStatus().name());
            event.put("totalAmount", order.getTotalAmount());
            event.put("paymentId", order.getPaymentId());
            event.put("detail", detail);
            event.put("timestamp", LocalDateTime.now().toString());
            kafkaTemplate.send(topic, order.getId(), event);
        } catch (Exception e) {
            log.error("Failed to publish order event to {}: {}", topic, e.getMessage());
        }
    }
```

**Fix:**

> Illustrative proposal only.

`source/customer-app/order-service/src/main/java/com/ecommerce/order/outbox/OutboxEventRepository.java` — bounded pending read consumed by the relay

```java
package com.ecommerce.order.outbox;

import java.util.List;
import org.springframework.data.domain.Limit;
import org.springframework.data.jpa.repository.JpaRepository;

public interface OutboxEventRepository extends JpaRepository<OutboxEvent, String> {

    List<OutboxEvent> findByStatusOrderByCreatedAtAsc(OutboxEvent.Status status, Limit limit);

    long countByStatus(OutboxEvent.Status status);
}
```

A bounded read of pending rows. The `Limit` parameter keeps the relay from materialising an unbounded backlog, which is the same defect **P1-012** addresses in the inventory sweep. The send-result observation itself is rendered under **P0-007** in `OutboxRelay.relayPendingEvents`, which awaits `send(...).get(deliveryTimeoutMs, MILLISECONDS)` and increments `outbox.events.delivery_failed` on any failure — this is the direct remediation for the discarded `CompletableFuture`.

**Notes:**

* **Cross-refs:** Primary finding **P0-007**. Related to **P1-005** (producer durability) and **P3-003** (publish-failure signal).
* **Implementation:** `CHANGE-AA-007`, Wave 3. No dedicated change; the consolidation rationale is recorded as key decision `KD-01` in the Step 3A handoff.
* **Validation:** Covered by T-AA-007-01, T-AA-007-02, and T-AA-007-03.
* **Guardrail:** Until the outbox lands, no other change makes publication observable. Do not treat this finding as remediated by adding a callback to the existing in-transaction `send`, because that leaves the dual-write boundary intact.

<span style="font-size: 14px;">**MSFT Reference:** [Asynchronous Request-Reply and messaging reliability patterns](https://learn.microsoft.com/azure/architecture/patterns/async-request-reply)</span>

---

#### Workload Ownership

#### P0-009: Kafka producers and consumers are unconditionally active in every replica

**Priority: P0 - Critical Immediate Action**

**Priority policy:** `AA-REMEDIATION-PRIORITY` v1.0.0, rule `P0-AA-006` (elevated from candidate `P2-DATA-002`) · **Change ID:** `CHANGE-AA-008` (Wave 2) · **Source ID:** F-014 · **Primary control:** `APP-KAFKA-001`

**Severity:** Critical

**Resiliency Related:** Yes

**Finding status:** **Conditional finding** — finding basis is `policy_inference`

**Condition:** This finding's risk depends on the inferred `active_standby` operating scenario. It assumes that (1) Azure SQL is the authoritative transactional system of record with a primary and a standby role, (2) Kafka application processing is expected to be active in exactly one region at a time, and (3) regional role assignment is supplied by the platform rather than by the application.

**Evidence required to confirm:** an approved application or solution architecture context confirming the active-standby scenario (`EXT-006`); Azure SQL Failover Group deployment and listener endpoint configuration (`EXT-003`); the Kafka promotion, Cluster Linking, mirror topic, and consumer-offset replication model (`EXT-001`, `EXT-002`).

**Issue:** Every `@KafkaListener` registers with static group ids and no `autoStartup` attribute, no conditional bean, no activation property, and no region or role flag. No producer is gated either. Nothing in the repository can verify Azure SQL primary ownership before processing, stop acquisition before an ownership transfer, or fence a stale active instance.

**What does this solve:** It makes regional activation explicit, sequenced, and observable, and creates the seam where a fencing or lease mechanism can later be attached without touching listener code.

**Resiliency Impact:** Under the inferred active-standby model, the standby region consumes and produces authoritative work concurrently with the active region. Activation defaults to enabled, so a promotion or a failback cannot be sequenced and a both-active condition cannot be detected. Duplicate authoritative processing is the default behavior rather than an edge case, which is why the `P2-DATA-002` candidate was elevated to P0 under `P0-AA-006`.

**Recommended Fix:** Introduce a scenario-neutral `WorkloadOwnershipGuard` abstraction that defaults to not-owning, declare `autoStartup = "false"` and an explicit container id on every listener, and start and stop containers from an ownership reconciler. Producers and the outbox relay consult the same guard.

**File:** source/customer-app/inventory-service/src/main/java/com/ecommerce/inventory/service/InventoryService.java:250-262

```java
// before
    @KafkaListener(topics = KafkaTopics.ORDER_CREATED, groupId = KafkaTopics.GROUP_INVENTORY_SERVICE)
    public void handleOrderCreated(Map<String, Object> event) {
        log.info("Processing ORDER_CREATED event for order: {}", event.get("orderId"));
        // Auto-reserve inventory based on order items
        // This would be handled by the orchestration layer in a real saga pattern
    }

    @KafkaListener(topics = KafkaTopics.ORDER_CANCELLED, groupId = KafkaTopics.GROUP_INVENTORY_SERVICE)
    public void handleOrderCancelled(Map<String, Object> event) {
        String orderId = (String) event.get("orderId");
        log.info("Processing ORDER_CANCELLED event for order: {}", orderId);
        // Release all reservations for this order
    }
```

**File:** source/customer-app/notification-service/src/main/java/com/ecommerce/notification/service/NotificationEventConsumer.java:34-36

```java
// before
    @KafkaListener(topics = KafkaTopics.ORDER_CREATED, groupId = KafkaTopics.GROUP_NOTIFICATION_SERVICE)
    @Async
    public void handleOrderCreated(Map<String, Object> event) {
```

**Fix:**

> Illustrative proposal only.

`source/customer-app/common/src/main/java/com/ecommerce/common/ownership/WorkloadOwnershipGuard.java`

```java
package com.ecommerce.common.ownership;

import java.util.Optional;

/**
 * Reports whether this deployment currently owns authoritative processing.
 * Implementations must default to not owning when ownership cannot be established.
 */
public interface WorkloadOwnershipGuard {

    boolean isOwner();

    /** Monotonically increasing token for the current ownership term, when available. */
    Optional<Long> ownershipEpoch();

    /** Human-readable reason for the current state, surfaced in health and telemetry. */
    String describe();
}
```

A technology-neutral seam that every authoritative workload consults. It is deliberately independent of the fencing mechanism so listener, scheduler, and relay code never needs to change when a lease implementation is selected.

`source/customer-app/common/src/main/java/com/ecommerce/common/ownership/KafkaListenerOwnershipController.java`

```java
package com.ecommerce.common.ownership;

import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.kafka.config.KafkaListenerEndpointRegistry;
import org.springframework.kafka.listener.MessageListenerContainer;
import org.springframework.scheduling.annotation.Scheduled;
import org.springframework.stereotype.Component;

/**
 * Starts and stops listener containers to follow the ownership signal. Containers declare
 * autoStartup=false so they never start implicitly.
 */
@Slf4j
@Component
@RequiredArgsConstructor
public class KafkaListenerOwnershipController {

    private final KafkaListenerEndpointRegistry registry;
    private final WorkloadOwnershipGuard ownershipGuard;

    @Scheduled(fixedDelayString = "${app.workload.ownership.reconcile-interval-ms:5000}")
    public void reconcile() {
        boolean owner = ownershipGuard.isOwner();
        for (MessageListenerContainer container : registry.getListenerContainers()) {
            if (owner && !container.isRunning()) {
                log.info("Ownership acquired ({}); starting listener container {}",
                        ownershipGuard.describe(), container.getListenerId());
                container.start();
            } else if (!owner && container.isRunning()) {
                log.info("Ownership lost ({}); stopping listener container {}",
                        ownershipGuard.describe(), container.getListenerId());
                container.stop();
            }
        }
    }
}
```

Uses only Spring Kafka's `KafkaListenerEndpointRegistry` and `MessageListenerContainer`, both already on the classpath through the existing `spring-kafka` dependency. Stopping the container before an ownership transfer is what control `KAFKA-AS-007` requires, and the reconcile interval is externally configurable.

`source/customer-app/inventory-service/src/main/java/com/ecommerce/inventory/service/InventoryService.java` — listener registration

```java
@KafkaListener(
        id = "inventory-order-created",
        topics = KafkaTopics.ORDER_CREATED,
        groupId = KafkaTopics.GROUP_INVENTORY_SERVICE,
        autoStartup = "false")
public void handleOrderCreated(Map<String, Object> event) {
    log.info("Processing ORDER_CREATED event for order: {}", event.get("orderId"));
}

@KafkaListener(
        id = "inventory-order-cancelled",
        topics = KafkaTopics.ORDER_CANCELLED,
        groupId = KafkaTopics.GROUP_INVENTORY_SERVICE,
        autoStartup = "false")
public void handleOrderCancelled(Map<String, Object> event) {
    String orderId = (String) event.get("orderId");
    log.info("Processing ORDER_CANCELLED event for order: {}", orderId);
}
```

`autoStartup = "false"` makes non-processing the default state for every replica, and the explicit container id makes the ownership controller's start and stop actions attributable in logs and metrics. Topic and group constants are unchanged.

**Illustrative code status:** Targeted implementation discovery required (`TD-06`)

**Target:** `LeaseBackedOwnershipGuard` with fencing token — repository path not yet selected

**Why code was not generated:** The approved ownership and fencing mechanism has not been selected. The repository contains no lease, leader election, ShedLock, or owner epoch, and `EXT-001`, `EXT-002`, and `EXT-003` record that the Kafka regional role model and the Azure SQL failover-group listener configuration are unresolved external facts. Choosing between an Azure SQL lease table, a Redis lease, and a Kubernetes lease is an architecture decision, and the SQL primary-role verification query depends on the unconfirmed failover-group deployment.

**Unresolved inputs:**

* Approved ownership and fencing mechanism, including the durable lease store
* `EXT-003` Azure SQL Failover Group deployment and listener endpoint configuration
* `EXT-001` and `EXT-002` Kafka regional role assignment and offset replication model
* Required both-active detection and alerting contract

**Intended behavior:** Controls `KAFKA-AS-003` and `KAFKA-AS-007` require a lease with a monotonic epoch, verification of Azure SQL primary ownership, and detection of a both-active condition. `PROPERTY` mode is a deployment-controlled switch; `LEASE` mode supplies automatic, fenced ownership.

**Notes:**

* **Cross-refs:** Prerequisite for **P0-010**, **P0-011**, and **P0-007** (the relay is gated by the same guard). Depends on **P0-012**.
* **Implementation:** `CHANGE-AA-008`, Wave 2, complexity high, and it leads Wave 2. Five of six targets carry generated code. Activation is externalized through `app.workload.ownership` with `active: ${APP_WORKLOAD_ACTIVE:false}` and `mode: ${APP_WORKLOAD_OWNERSHIP_MODE:DISABLED}`, so a deployed-but-unpromoted standby performs no authoritative processing and no region name is committed.
* **Validation:** T-AA-008-01 (containers stay stopped while not owner), T-AA-008-02 (start on acquire, stop before release), T-AA-008-03 (default resolved state is not-owning). `mvn -f source/customer-app/pom.xml -pl common,inventory-service,notification-service -am test`.
* **Guardrail:** `PROPERTY` mode provides sequencing but **not fencing**; a mis-set property can still produce a both-active condition until `LEASE` mode lands. Consumer groups will accrue lag while a region is not owner, which must be expected rather than alerted as a fault. `UNC-010` records that the `common` module's bean visibility to other modules is unverified.

<span style="font-size: 14px;">**MSFT Reference:** [Leader Election pattern](https://learn.microsoft.com/azure/architecture/patterns/leader-election)</span>

---

#### P0-010: Scheduled jobs execute on every replica with no distributed ownership

**Priority: P0 - Critical Immediate Action**

**Priority policy:** `AA-REMEDIATION-PRIORITY` v1.0.0, rule `P0-AA-006` (elevated from candidate `P2-DATA-002`) · **Change ID:** `CHANGE-AA-009` (Wave 2) · **Source ID:** F-015 · **Primary control:** `APP-SCHED-001`

**Severity:** Critical

**Resiliency Related:** Yes

**Finding status:** Verified finding

**Issue:** Four `@Scheduled` jobs mutate shared state in `cart-service` and `inventory-service`. Both deployments run two replicas. There is no ShedLock, `@SchedulerLock`, leader election, lease, ownership epoch, or activation flag anywhere in the repository. Reservation expiry selects records and mutates them without an atomic claim.

**What does this solve:** It removes duplicate reservation release, duplicate cart cleanup, and duplicate low-stock alerting, and gives the sweeps a defined owner after a regional transition.

**Resiliency Impact:** Every replica in every region runs the same sweep concurrently. Reservation expiry, cart cleanup, and low-stock alerting execute multiple times, duplicating releases and alerts, and no region owns the work after a failover. Duplicate execution against authoritative inventory is materially unsafe, which is why the candidate was elevated to P0.

**Recommended Fix:** Gate every scheduled method behind the same `WorkloadOwnershipGuard`, re-check ownership between pages so a lost lease stops processing mid-sweep, save every mutated inventory document under its `@Version` etag, and declare an explicit time zone on every cron expression.

**File:** source/customer-app/inventory-service/src/main/java/com/ecommerce/inventory/service/InventoryService.java:268-291

```java
// before
    @Scheduled(fixedDelay = 300000) // Every 5 minutes
    public void expireOldReservations() {
        log.debug("Running reservation expiry job...");
        LocalDateTime now = LocalDateTime.now();
        List<InventoryDocument> allInventory = inventoryRepository.findByStatus("ACTIVE");
        
        for (InventoryDocument inv : allInventory) {
            boolean changed = false;
            for (StockReservation res : inv.getReservations()) {
                if ("ACTIVE".equals(res.getStatus()) && res.getExpiresAt().isBefore(now)) {
                    res.setStatus("EXPIRED");
                    inv.setReservedQuantity(Math.max(0, inv.getReservedQuantity() - res.getQuantity()));
                    changed = true;
                    log.info("Expired reservation {} for product: {}", res.getReservationId(), inv.getProductId());
                }
            }
            if (changed) {
                inv.adjustAvailableQuantity();
                inv.setUpdatedAt(now);
                inventoryRepository.save(inv);
            }
        }
    }
```

**File:** source/customer-app/cart-service/src/main/java/com/ecommerce/cart/service/CartService.java:205-233 — scheduled cart sweeps

> Original source excerpt: Not available in authoritative evidence artifact. Step 2 evidence `EV-F-015-02` confirms by targeted validation that `@Scheduled(fixedDelay = 3600000)` appears at line 205 and `@Scheduled(cron = "0 0 2 * * *")` at line 233; full method bodies were not required to establish the ownership gap.

**File:** source/customer-app/cart-service/src/main/java/com/ecommerce/cartservice/CartServiceApplication.java:11-12

```java
// before
@EnableAsync
@EnableScheduling
```

**Fix:**

> Illustrative proposal only.

`source/customer-app/inventory-service/src/main/java/com/ecommerce/inventory/service/InventoryService.java` — `expireOldReservations`

```java
@Scheduled(fixedDelayString = "${app.inventory.reservation-expiry.interval-ms:300000}")
public void expireOldReservations() {
    if (!ownershipGuard.isOwner()) {
        log.debug("Skipping reservation expiry; not the owning instance ({})",
                ownershipGuard.describe());
        return;
    }
    log.debug("Running reservation expiry job as owner {}", ownershipGuard.describe());
    expireReservationsForOwnedTerm();
}

private void expireReservationsForOwnedTerm() {
    LocalDateTime now = LocalDateTime.now();
    for (InventoryDocument inv : nextExpiryPage(now)) {
        if (!ownershipGuard.isOwner()) {
            log.warn("Ownership lost mid-sweep; stopping reservation expiry");
            return;
        }
        boolean changed = false;
        for (StockReservation res : inv.getReservations()) {
            if ("ACTIVE".equals(res.getStatus()) && res.getExpiresAt().isBefore(now)) {
                res.setStatus("EXPIRED");
                inv.setReservedQuantity(Math.max(0, inv.getReservedQuantity() - res.getQuantity()));
                changed = true;
            }
        }
        if (changed) {
            inv.adjustAvailableQuantity();
            inv.setUpdatedAt(now);
            try {
                // Conditional on the @Version etag; a losing writer is rejected, not merged.
                inventoryRepository.save(inv);
            } catch (OptimisticLockingFailureException conflict) {
                log.info("Expiry skipped for {}; document changed concurrently", inv.getProductId());
            }
        }
    }
}
```

The sweep now runs only on the owning instance, re-checks ownership between pages so a lost lease stops further processing, and saves under the etag so a concurrent reservation is not clobbered. The fixed delay becomes externally configurable rather than a compiled `300000`. Paging is supplied by **P1-012**.

`source/customer-app/cart-service/src/main/java/com/ecommerce/cart/service/CartService.java` — scheduled cart sweeps

```java
@Scheduled(fixedDelayString = "${app.cart.abandonment.interval-ms:3600000}")
public void sweepAbandonedCarts() {
    if (!ownershipGuard.isOwner()) {
        return;
    }
    doSweepAbandonedCarts();
}

@Scheduled(cron = "${app.cart.cleanup.cron:0 0 2 * * *}", zone = "${app.cart.cleanup.zone:UTC}")
public void cleanupExpiredCarts() {
    if (!ownershipGuard.isOwner()) {
        return;
    }
    doCleanupExpiredCarts();
}
```

Both cart sweeps are gated by the same guard. The cron expression gains an explicit zone, which the inventory records as unspecified on every cron expression in the repository; without it, a second region on nodes in a different time zone would sweep at a different wall-clock time.

**Notes:**

* **Cross-refs:** Depends on **P0-009** (supplies the guard) and **P0-012**. Rebased onto by **P1-012**, which edits the same method. Alerting for a no-owner condition is supplied by **P3-003**.
* **Implementation:** `CHANGE-AA-009`, Wave 2, complexity medium. All three targets carry generated code. No new property namespace is introduced; it reuses `app.workload.ownership`.
* **Validation:** T-AA-009-01 (exactly one instance sweeps), T-AA-009-02 (lost ownership stops the sweep mid-run), T-AA-009-03 (concurrent reservation causes a conflict rather than a silent overwrite). `mvn -f source/customer-app/pom.xml -pl common,inventory-service,cart-service -am test`.
* **Guardrail:** With `PROPERTY`-mode ownership, a mis-set activation property can leave **no owner** and sweeps stop entirely. A no-owner alert is required and is covered by **P3-003** (`OQ-14` records that the threshold is undecided). `UNC-008` records unresolved call-site and schema mismatches in `CartService`; current method signatures must be confirmed before editing.

<span style="font-size: 14px;">**MSFT Reference:** [Scheduler Agent Supervisor pattern](https://learn.microsoft.com/azure/architecture/patterns/scheduler-agent-supervisor)</span>

---

#### Lifecycle and Drain

#### P0-011: Graceful shutdown and traffic draining are incomplete

**Priority: P0 - Critical Immediate Action**

**Priority policy:** `AA-REMEDIATION-PRIORITY` v1.0.0, rule `P0-RCV-008` · **Change ID:** `CHANGE-AA-010` (Wave 2) · **Source ID:** F-017 · **Primary control:** `APP-AA-017`

**Severity:** High

**Resiliency Related:** Yes

**Finding status:** Verified finding

**Issue:** `server.shutdown: graceful` is declared in `order`, `payment`, `cart`, and `inventory` services and absent in `api-gateway`, `user`, `product`, and `notification` services. `spring.lifecycle.timeout-per-shutdown-phase` is not set in any module. No module declares a `@PreDestroy` hook, `SmartLifecycle` implementation, `ContextClosedEvent` listener, or runtime shutdown hook. No deployment declares `terminationGracePeriodSeconds` or a `preStop` lifecycle hook, and Kafka listener container stop behavior is not configured.

**What does this solve:** It prevents lost requests and lost or duplicated Kafka work during rolling updates, node drain, autoscale events, and regional drains.

**Resiliency Impact:** During a rolling update or a regional drain, four services terminate abruptly and lose in-flight requests, and every service can lose in-flight Kafka work because the listener containers are not given a bounded stop window. Under `active_standby`, releasing ownership during shutdown is what allows a promotion to be sequenced rather than racing a still-running previous owner.

**Recommended Fix:** Declare graceful shutdown with an explicit phase timeout in every service, withdraw readiness first, stop and drain listener containers before the context closes, release workload ownership, and give the pod a termination grace period longer than the phase timeout plus a `preStop` delay so the endpoint is removed before the socket closes.

**File:** source/customer-app/order-service/src/main/resources/application.yml:1-3

```yaml
// before
server:
  port: 8083
  shutdown: graceful
```

**File:** source/customer-app/notification-service/src/main/resources/application.yml:1-2

```yaml
// before
server:
  port: 8087
```

**File:** source/customer-app/k8s/services/all-services.yaml:31-79

```yaml
// before
      spec:
        serviceAccountName: ecommerce-workload-identity
        containers:
          - name: user-service
            image: ${ACR_NAME}.azurecr.io/user-service:${IMAGE_TAG}
            imagePullPolicy: Always
            ports:
              - containerPort: 8081
```

> Step 2 note: the pod spec declares no `terminationGracePeriodSeconds` and no `lifecycle.preStop` hook. The excerpt is truncated to the container declaration; the omitted lines contain `env`, `envFrom`, `resources`, and probe blocks only.

**Fix:**

> Illustrative proposal only.

`source/customer-app/notification-service/src/main/resources/application.yml` — `server.shutdown` and `spring.lifecycle`

```yaml
server:
  port: 8087
  shutdown: graceful

spring:
  lifecycle:
    timeout-per-shutdown-phase: ${APP_SHUTDOWN_PHASE_TIMEOUT:25s}
  kafka:
    listener:
      immediate-stop: false
```

`notification-service` is one of the four services with no graceful shutdown at all. The phase timeout bounds the drain so termination cannot hang, and `immediate-stop: false` lets the listener container finish the records it has already handed to the listener instead of abandoning them.

`source/customer-app/common/src/main/java/com/ecommerce/common/lifecycle/OwnershipReleasingShutdownHook.java`

```java
package com.ecommerce.common.lifecycle;

import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.boot.availability.ApplicationAvailability;
import org.springframework.boot.availability.AvailabilityChangeEvent;
import org.springframework.boot.availability.ReadinessState;
import org.springframework.context.ApplicationEventPublisher;
import org.springframework.context.SmartLifecycle;
import org.springframework.kafka.config.KafkaListenerEndpointRegistry;
import org.springframework.stereotype.Component;

/**
 * Runs early in the shutdown sequence: withdraw readiness, stop listener containers so
 * in-flight records complete, then release workload ownership.
 */
@Slf4j
@Component
@RequiredArgsConstructor
public class OwnershipReleasingShutdownHook implements SmartLifecycle {

    private final ApplicationEventPublisher eventPublisher;
    private final ApplicationAvailability availability;
    private final KafkaListenerEndpointRegistry registry;
    private final WorkloadOwnershipGuard ownershipGuard;

    private volatile boolean running;

    @Override
    public void start() {
        running = true;
    }

    @Override
    public void stop() {
        log.info("Shutdown initiated; withdrawing readiness before draining");
        AvailabilityChangeEvent.publish(eventPublisher, this, ReadinessState.REFUSING_TRAFFIC);

        registry.getListenerContainers().forEach(container -> {
            if (container.isRunning()) {
                log.info("Stopping listener container {} for drain", container.getListenerId());
                container.stop();
            }
        });

        if (ownershipGuard.isOwner()) {
            log.info("Releasing workload ownership held by {}", ownershipGuard.describe());
            ownershipGuard.release();
        }
        running = false;
    }

    @Override
    public boolean isRunning() {
        return running;
    }

    /** Runs before the web server phase so readiness is withdrawn before the socket closes. */
    @Override
    public int getPhase() {
        return Integer.MAX_VALUE - 1024;
    }
}
```

The inventory records that no `ApplicationAvailability`, `AvailabilityChangeEvent`, `ReadinessState`, `@PreDestroy` hook, or `SmartLifecycle` implementation exists anywhere. This supplies all four: readiness is withdrawn first so the endpoint is removed, listener containers stop so no new record is fetched while in-flight records finish, and ownership is released so a promotion is not racing a live previous owner.

`source/customer-app/k8s/services/all-services.yaml` — pod drain window

```yaml
spec:
  terminationGracePeriodSeconds: 45
  serviceAccountName: ecommerce-workload-identity
  containers:
    - name: user-service
      image: ${ACR_NAME}.azurecr.io/user-service:${IMAGE_TAG}
      imagePullPolicy: Always
      lifecycle:
        preStop:
          exec:
            command: ["sh", "-c", "sleep 10"]
      ports:
        - containerPort: 8081
```

The `preStop` delay gives the endpoint controller time to remove the pod from Service endpoints before the container receives SIGTERM, and the termination grace period is longer than the 25s Spring shutdown phase timeout so the drain can finish. This is an application-owned workload manifest change; no Azure resource is provisioned.

**Notes:**

* **Cross-refs:** Depends on **P0-003** (readiness must be meaningful before it is withdrawn), **P0-009** (`WorkloadOwnershipGuard.release()` is added to that interface), and **P0-012**. Makes the **P1-009** executor drain meaningful.
* **Implementation:** `CHANGE-AA-010`, Wave 2, complexity medium. All four targets carry generated code. Touches five `application.yml` files and `k8s/services/all-services.yaml`.
* **Validation:** T-AA-010-01 (readiness withdrawn before containers stop and before ownership release), T-AA-010-02 (no Kafka record lost on mid-consumption termination), T-AA-010-03 (shutdown completes within the phase timeout with a hung request). `mvn -f source/customer-app/pom.xml -pl common,notification-service,order-service -am test`; `mvn -f source/customer-app/pom.xml verify`.
* **Guardrail:** A drain window longer than the termination grace period causes SIGKILL mid-drain; the two values must be tuned together. `OQ-15` records that the approved grace period and phase timeout per workload are undecided. `UNC-004` records that second-region manifests may be maintained outside this repository, in which case the same edits must be mirrored there.

<span style="font-size: 14px;">**MSFT Reference:** [Best practices for application reliability in AKS](https://learn.microsoft.com/azure/aks/best-practices-app-cluster-reliability)</span>

---

#### Verification Foundation

#### P0-012: No automated test coverage exists for any failure or recovery behavior

**Priority: P0 - Critical Immediate Action**

**Priority policy:** `AA-REMEDIATION-PRIORITY` v1.0.0, rule `P0-AA-007` · **Change ID:** `CHANGE-AA-011` (Wave 1) · **Source ID:** F-018 · **Primary control:** `APP-AA-018`

**Severity:** Critical

**Resiliency Related:** Yes

**Finding status:** Verified finding

**Issue:** Zero of nine modules contain a `src/test` directory. There are no unit, slice, integration, MockMvc, WebTestClient, Testcontainers, EmbeddedKafka, WireMock, chaos, resilience, failover, duplicate-message, concurrency, shutdown, or recovery tests. `spring-boot-starter-test` is declared in all nine modules and never exercised. All Dockerfiles build with `-DskipTests`, and the pipeline `mvn verify` step executes no tests because no test sources exist.

**What does this solve:** It makes every other change in this plan provable and gives the shared BOM upgrades a regression guard.

**Resiliency Impact:** No timeout, retry, health transition, idempotency, shutdown, promotion, or recovery behavior is proven. Every remediation in this assessment would otherwise ship without a regression guard, and shared BOM upgrades can silently change resilience behavior. It also makes the promotion, fencing, offset, and failback tests that control `KAFKA-AS-009` requires impossible to execute at all.

**Recommended Fix:** Create the test source tree in every module, declare the failure-simulation tooling later waves require through the existing BOM-import convention, configure Surefire and Failsafe so a failing test fails the build, and remove `-DskipTests` from the container build while excluding long-running integration tests from the image build.

**File:** source/customer-app/order-service/Dockerfile:16

```dockerfile
// before
RUN mvn package -DskipTests --no-transfer-progress -pl common,order-service -am
```

**File:** source/customer-app — repository-wide test inventory (evidence `EV-F-018-02`; original source excerpt: `not_applicable`)

> The authoritative inventory records `modules_with_src_test_directory: 0` and `total_test_classes: 0` across all nine modules.

**Fix:**

> Illustrative proposal only.

`source/customer-app/pom.xml` — `dependencyManagement` and `build/plugins`

```xml
<dependencyManagement>
  <dependencies>
    <dependency>
      <groupId>org.testcontainers</groupId>
      <artifactId>testcontainers-bom</artifactId>
      <version>${testcontainers.version}</version>
      <type>pom</type>
      <scope>import</scope>
    </dependency>
    <dependency>
      <groupId>org.wiremock</groupId>
      <artifactId>wiremock-standalone</artifactId>
      <version>${wiremock.version}</version>
      <scope>test</scope>
    </dependency>
    <dependency>
      <groupId>org.awaitility</groupId>
      <artifactId>awaitility</artifactId>
      <version>${awaitility.version}</version>
      <scope>test</scope>
    </dependency>
  </dependencies>
</dependencyManagement>

<build>
  <plugins>
    <plugin>
      <groupId>org.apache.maven.plugins</groupId>
      <artifactId>maven-surefire-plugin</artifactId>
      <configuration>
        <skipTests>false</skipTests>
        <failIfNoSpecifiedTests>true</failIfNoSpecifiedTests>
        <trimStackTrace>false</trimStackTrace>
      </configuration>
    </plugin>
    <plugin>
      <groupId>org.apache.maven.plugins</groupId>
      <artifactId>maven-failsafe-plugin</artifactId>
      <executions>
        <execution>
          <goals>
            <goal>integration-test</goal>
            <goal>verify</goal>
          </goals>
        </execution>
      </executions>
    </plugin>
  </plugins>
</build>
```

Adds the failure-simulation tooling the later waves need through the existing BOM-import convention already used for Spring Boot, Spring Cloud, and Spring Cloud Azure, and binds Failsafe so integration tests actually run during `mvn verify`. Version properties are left as properties so the team can pin them; they are not invented here.

`source/customer-app/order-service/Dockerfile` — build stage package command

```dockerfile
# Unit tests run in the image build; long-running integration tests remain in the pipeline.
RUN mvn package --no-transfer-progress -pl common,order-service -am \
    -Dsurefire.failIfNoSpecifiedTests=true \
    -DskipITs=true
```

Removing `-DskipTests` makes the container build fail when a unit test fails. Integration tests that need containers or brokers are excluded from the image build with `-DskipITs` and remain the pipeline's responsibility, so the image build stays hermetic.

**Notes:**

* **Cross-refs:** Prerequisite for **every other change in this plan** except itself. Wave 1 lands it first. Per key decision `KD-04`, this change carries only the harness and build enforcement; behavioral tests remain inside the change that proves the behavior, because `tests_inherit_behavior_priority` is true in the governing policy.
* **Implementation:** `CHANGE-AA-011`, Wave 1, complexity medium. All three targets carry generated code. `OQ-17` records that approved Testcontainers, WireMock, and Awaitility versions are undecided.
* **Validation:** T-AA-011-01 (harness executes), T-AA-011-02 (a deliberately failing test fails both `mvn verify` and the container build). `mvn -f source/customer-app/pom.xml verify`.
* **Guardrail:** **Blocking risk `R-01`.** `UNC-006` records six compilation errors in `common` `GlobalExceptionHandler.java` for missing Spring Security packages in the captured build log. If that is still the current state, no module builds and no validation command in this plan can succeed. `OQ-16` must be resolved as step 1 of Wave 1.

<span style="font-size: 14px;">**MSFT Reference:** [Reliability testing strategy — Azure Well-Architected Framework](https://learn.microsoft.com/azure/well-architected/reliability/testing-strategy)</span>

---
### P1 High Priority

#### Configuration Binding

#### P1-001: Declared Redis and cache properties are never bound or consumed

**Priority: P1 - High Priority**

**Priority policy:** `AA-REMEDIATION-PRIORITY` v1.0.0, rule `P1-RCV-001` · **Change ID:** `CHANGE-AA-012` (Wave 1) · **Source ID:** F-024 · **Primary control:** `APP-CONF-013`

**Severity:** High

**Resiliency Related:** Yes

**Finding status:** Verified finding

**Issue:** Both Redis clients declare host, port, password, `ssl.enabled`, timeout, and pool settings under the Spring Boot 2 `spring.redis.*` prefix while the application runs on Spring Boot 3.2.5, where `spring.data.redis.*` is the binding prefix. `product-service` additionally declares `spring.redis.cache.time-to-live`, which is not a bindable Spring Boot property, and a separate custom `cache.*.ttl` block that no `@Value` or `@ConfigurationProperties` binds. `api-gateway` declares seven `service.*.url` keys that nothing binds. No `CacheManager`, `RedisTemplate`, or serializer bean exists, and no bound property carries `@Validated` invariants.

**What does this solve:** It restores the ability to tune the Redis failure budget and cache TTL through configuration, which every later Redis and cache change depends on.

**Resiliency Impact:** Command timeouts, TLS enablement, pool bounds, and cache TTL are believed to be configured but are not in effect. Redis calls are governed by client defaults and can exceed the failure-detection budget and consume request capacity. Operators cannot tune the failure budget through configuration, and a cache with unbounded effective TTL can serve stale data across a regional transition.

**Recommended Fix:** Move Redis settings onto the Spring Boot 3 binding prefix, bind the custom cache and service-URL blocks to validated `@ConfigurationProperties` classes consumed by a `CacheManager`, and fail startup on an invalid value.

**File:** source/customer-app/api-gateway/src/main/resources/application.yml:44-55

```yaml
// before
    redis:
      host: ${REDIS_HOST:ecommerce-redis.redis.cache.windows.net}
      port: ${REDIS_PORT:6380}
      password: ${REDIS_PASSWORD}
      ssl:
        enabled: true
      timeout: 2000
      lettuce:
        pool:
          max-active: 16
          max-idle: 8
          min-idle: 2
```

**File:** source/customer-app/product-service/src/main/resources/application.yml:23-30 and :48-54

```yaml
// before
    redis:
      host: ${REDIS_HOST:ecommerce-redis.redis.cache.windows.net}
      port: ${REDIS_PORT:6380}
      password: ${REDIS_PASSWORD}
      ssl:
        enabled: true
      cache:
        time-to-live: 600000  # 10 minutes
cache:
  products:
    ttl: 600
  categories:
    ttl: 3600
  product-list:
    ttl: 300
```

**Fix:**

> Illustrative proposal only.

`source/customer-app/api-gateway/src/main/resources/application.yml` — `spring.data.redis`

```yaml
spring:
  data:
    redis:
      host: ${REDIS_HOST}
      port: ${REDIS_PORT:6380}
      password: ${REDIS_PASSWORD}
      ssl:
        enabled: true
      timeout: ${REDIS_COMMAND_TIMEOUT:2000ms}
      connect-timeout: ${REDIS_CONNECT_TIMEOUT:2000ms}
      lettuce:
        pool:
          enabled: true
          max-active: ${REDIS_POOL_MAX_ACTIVE:16}
          max-idle: ${REDIS_POOL_MAX_IDLE:8}
          min-idle: ${REDIS_POOL_MIN_IDLE:2}
          max-wait: ${REDIS_POOL_MAX_WAIT:200ms}
```

The Spring Boot 3 binding prefix makes TLS enablement, the command timeout, and the pool bounds effective for the first time. `max-wait` adds the pool-acquire bound the standard requires, and the regional host literal is removed in line with **P0-001**.

`source/customer-app/common/src/main/java/com/ecommerce/common/config/CacheTtlProperties.java`

```java
package com.ecommerce.common.config;

import jakarta.validation.constraints.NotNull;
import java.time.Duration;
import java.util.LinkedHashMap;
import java.util.Map;
import org.springframework.boot.context.properties.ConfigurationProperties;
import org.springframework.validation.annotation.Validated;

@Validated
@ConfigurationProperties(prefix = "app.cache")
public class CacheTtlProperties {

    @NotNull
    private Duration defaultTtl = Duration.ofMinutes(10);

    /** Per-cache overrides keyed by cache name. */
    private Map<String, Duration> ttls = new LinkedHashMap<>();

    public Duration ttlFor(String cacheName) {
        return ttls.getOrDefault(cacheName, defaultTtl);
    }

    public Duration getDefaultTtl() {
        return defaultTtl;
    }

    public void setDefaultTtl(Duration defaultTtl) {
        this.defaultTtl = defaultTtl;
    }

    public Map<String, Duration> getTtls() {
        return ttls;
    }

    public void setTtls(Map<String, Duration> ttls) {
        this.ttls = ttls;
    }
}
```

Gives the previously orphaned TTL block a real binding target and a default, so a cache with no configured TTL can no longer have an unbounded effective lifetime. It is validated, so an unparseable duration fails startup instead of being silently ignored. The seven unbound `service.*.url` keys move to an equivalent validated `app.downstream` binding.

**Notes:**

* **Cross-refs:** Depends on **P0-001** and **P0-012**. Prerequisite for **P2-005** (the Redis command timeout must be in effect before the rate limiter's failure policy is meaningful).
* **Implementation:** `CHANGE-AA-012`, Wave 1, complexity low. All five targets carry generated code. `UNC-012` records that the effective `CacheManager` and serializer are undetermined; the `CacheManager` bean introduced here resolves that uncertainty for the repository.
* **Validation:** T-AA-012-01 (every declared property resolves to a non-default effective value), T-AA-012-02 (invalid bound value fails startup). `mvn -f source/customer-app/pom.xml -pl common,api-gateway,product-service -am test`.
* **Guardrail:** Making the previously ignored timeout effective changes runtime behavior: a value that was never applied now bounds real calls. `OQ-18` records that approved cache TTL values are undecided.

<span style="font-size: 14px;">**MSFT Reference:** [Azure Cache for Redis development best practices](https://learn.microsoft.com/azure/azure-cache-for-redis/cache-best-practices-development)</span>

---

#### Dependency Budgets

#### P1-002: Cosmos DB retry, timeout, and throttling budgets are absent

**Priority: P1 - High Priority**

**Priority policy:** `AA-REMEDIATION-PRIORITY` v1.0.0, rule `P1-RCV-001` · **Change ID:** `CHANGE-AA-013` (Wave 2) · **Source ID:** F-003 · **Primary control:** `COSMOS-003`

**Severity:** High

**Resiliency Related:** Yes

**Finding status:** Verified finding

**Issue:** No `throttlingRetryOptions`, `requestTimeout`, or `RetryOptions` is configured, and no `CosmosException`, `statusCode`, `subStatusCode`, or retry-after handling exists in any repository, service, or controller in the three Cosmos-using services.

**What does this solve:** It converts an unbounded latency increase under regional pressure into a bounded, observable, classified degradation.

**Resiliency Impact:** Throttling, transient transport failure, and regional failover responses are handled uniformly by SDK defaults. Sustained 429 pressure surfaces as an unbounded latency increase rather than a bounded degradation, which delays the readiness decision and consumes request capacity in the affected region.

**Recommended Fix:** Declare a validated, externally configurable request budget (request timeout, maximum throttling retry attempts, maximum retry wait) and add a failure classifier that distinguishes throttling from transport failure and conflict, honours the server retry-after hint, and emits a distinct throttling metric.

**File:** source/customer-app/product-service/src/main/resources/application.yml:8-16

```yaml
// before
    cloud:
      azure:
        cosmos:
          endpoint: https://ecommerce-cosmos.documents.azure.com:443/
          key: ${COSMOS_KEY}
          database: ecommerce-products
          consistency-level: SESSION
          populate-query-metrics: false
          connection-mode: DIRECT
```

**Fix:**

> Illustrative proposal only.

`source/customer-app/product-service/src/main/resources/application.yml` — `app.cosmos.request`

```yaml
app:
  cosmos:
    request:
      timeout: ${AZURE_COSMOS_REQUEST_TIMEOUT:5s}
      max-throttling-retry-attempts: ${AZURE_COSMOS_MAX_THROTTLING_RETRIES:3}
      max-throttling-retry-wait: ${AZURE_COSMOS_MAX_THROTTLING_WAIT:10s}
```

Makes the previously implicit SDK budget explicit and externally tunable so the Cosmos deadline can be aligned with the caller's end-to-end failure budget. No value is compiled.

`source/customer-app/common/src/main/java/com/ecommerce/common/cosmos/CosmosFailureClassifier.java`

```java
package com.ecommerce.common.cosmos;

import com.azure.cosmos.CosmosException;
import io.micrometer.core.instrument.MeterRegistry;
import java.time.Duration;
import lombok.RequiredArgsConstructor;

/** Classifies Cosmos failures so throttling is distinguishable from transport failure. */
@RequiredArgsConstructor
public class CosmosFailureClassifier {

    public enum Classification { THROTTLED, NOT_FOUND, CONFLICT, TRANSIENT, TERMINAL }

    private final MeterRegistry meterRegistry;

    public Classification classify(CosmosException e) {
        Classification classification = switch (e.getStatusCode()) {
            case 429 -> Classification.THROTTLED;
            case 404 -> Classification.NOT_FOUND;
            case 409, 412 -> Classification.CONFLICT;
            case 408, 449, 500, 503 -> Classification.TRANSIENT;
            default -> Classification.TERMINAL;
        };
        meterRegistry.counter("cosmos.failures",
                "classification", classification.name(),
                "status", String.valueOf(e.getStatusCode()),
                "subStatus", String.valueOf(e.getSubStatusCode())).increment();
        return classification;
    }

    /** Server-supplied backoff hint; callers must honour it rather than retrying immediately. */
    public Duration retryAfter(CosmosException e) {
        Duration hint = e.getRetryAfterDuration();
        return hint == null ? Duration.ZERO : hint;
    }
}
```

Supplies the `statusCode`, `subStatusCode`, and retry-after handling control `COSMOS-007` requires, and emits the distinct throttling metric the finding's validation test asks for. It uses only documented `CosmosException` members named by the dependency standard.

**Illustrative code status:** Targeted implementation discovery required (`TD-07`)

**Target:** Application of `throttlingRetryOptions` and `requestTimeout` to the effective Cosmos client — repository path not yet selected

**Why code was not generated:** This is the same unresolved fact as **P0-002**: the effective Spring Cloud Azure 5.10.0 client-builder customization type for `spring-cloud-azure-starter-data-cosmos` cannot be established from the supplied artifacts, and `UNC-016` records that BOM-resolved versions were never resolved because no build was executed.

**Unresolved inputs:**

* Effective `spring-cloud-azure-starter-data-cosmos` 5.10.0 builder-customizer type and registration mechanism

**Intended behavior:** The validated budget must be applied to the effective Cosmos client so the deadline and the throttling retry policy actually bound SDK calls.

**Notes:**

* **Cross-refs:** Depends on **P0-002** and **P0-012**. Prerequisite for **P0-005** (409 and 412 must classify as `CONFLICT`). Shares decision gate `spring_cloud_azure_client_customization` with **P0-002** and **P1-011**.
* **Implementation:** `CHANGE-AA-013`, Wave 2, complexity medium. Three of four targets carry generated code.
* **Validation:** T-AA-013-01 (429 with retry-after yields bounded attempt duration, a distinct metric, and no retry storm), T-AA-013-02 (409/412 classify as `CONFLICT`). `mvn -f source/customer-app/pom.xml -pl common,product-service,inventory-service,cart-service -am test`.
* **Guardrail:** A request timeout shorter than a legitimate long-running query surfaces as a new failure mode; the budget must be validated against observed latency. `OQ-02` and `OQ-19` remain open.

<span style="font-size: 14px;">**MSFT Reference:** [Retry pattern](https://learn.microsoft.com/azure/architecture/patterns/retry)</span>

---

#### P1-003: Kafka client timeout, reconnect, and backoff settings are unbounded

**Priority: P1 - High Priority**

**Priority policy:** `AA-REMEDIATION-PRIORITY` v1.0.0, rule `P1-RCV-001` · **Change ID:** `CHANGE-AA-014` (Wave 2) · **Source ID:** F-007 · **Primary control:** `KAFKA-005`

**Severity:** High

**Resiliency Related:** Yes

**Finding status:** Verified finding

**Issue:** No service configures `request.timeout.ms`, `reconnect.backoff.ms`, `reconnect.backoff.max.ms`, `retry.backoff.ms`, `session.timeout.ms`, or `max.poll.interval.ms`. Only serializers, acks, retries, group id, auto-offset-reset, and security properties are declared.

**What does this solve:** It makes broker-loss detection and reconnect pressure predictable and aligned with the ownership transition window.

**Resiliency Impact:** A broker or listener outage produces reconnect behavior governed entirely by client defaults, so stall detection and reconnect pressure cannot be aligned to the application failure budget or to a controlled regional role transition. A controlled `active_standby` role transition needs a bounded, known detection window; today it is whatever the client default happens to be.

**Recommended Fix:** Declare the full client budget — request timeout, reconnect backoff with an explicit maximum, retry backoff, metadata max age, session timeout, heartbeat interval, and max poll interval — in all seven Kafka-using services, with every value supplied by deployment.

**File:** source/customer-app/order-service/src/main/resources/application.yml:40-61

```yaml
// before
    kafka:
      bootstrap-servers: ${KAFKA_BOOTSTRAP_SERVERS:localhost:9092}
      producer:
        key-serializer: org.apache.kafka.common.serialization.StringSerializer
        value-serializer: org.springframework.kafka.support.serializer.JsonSerializer
        acks: all
        retries: 3
        properties:
          enable.idempotence: true
          max.in.flight.requests.per.connection: 5
      consumer:
        group-id: order-service-group
        key-deserializer: org.apache.kafka.common.serialization.StringDeserializer
        value-deserializer: org.springframework.kafka.support.serializer.JsonDeserializer
        auto-offset-reset: earliest
        properties:
          spring.json.trusted.packages: "com.ecommerce.*"
      security:
        protocol: ${KAFKA_SECURITY_PROTOCOL:PLAINTEXT}
      properties:
        sasl.mechanism: ${KAFKA_SASL_MECHANISM:PLAIN}
        sasl.jaas.config: ${KAFKA_SASL_JAAS_CONFIG:}
```

**Fix:**

> Illustrative proposal only.

`source/customer-app/order-service/src/main/resources/application.yml` — `spring.kafka.properties`

```yaml
spring:
  kafka:
    bootstrap-servers: ${KAFKA_BOOTSTRAP_SERVERS}
    properties:
      request.timeout.ms: ${KAFKA_REQUEST_TIMEOUT_MS:15000}
      reconnect.backoff.ms: ${KAFKA_RECONNECT_BACKOFF_MS:100}
      reconnect.backoff.max.ms: ${KAFKA_RECONNECT_BACKOFF_MAX_MS:10000}
      retry.backoff.ms: ${KAFKA_RETRY_BACKOFF_MS:200}
      metadata.max.age.ms: ${KAFKA_METADATA_MAX_AGE_MS:120000}
      sasl.mechanism: ${KAFKA_SASL_MECHANISM:PLAIN}
      sasl.jaas.config: ${KAFKA_SASL_JAAS_CONFIG:}
    consumer:
      properties:
        session.timeout.ms: ${KAFKA_SESSION_TIMEOUT_MS:30000}
        heartbeat.interval.ms: ${KAFKA_HEARTBEAT_INTERVAL_MS:10000}
        max.poll.interval.ms: ${KAFKA_MAX_POLL_INTERVAL_MS:300000}
    security:
      protocol: ${KAFKA_SECURITY_PROTOCOL:PLAINTEXT}
```

Every previously absent client budget key is declared and externally supplied. Bounded reconnect backoff with an explicit maximum prevents a reconnect storm during a broker or regional transition, and the session and poll-interval settings make stall detection a known quantity rather than a client default. The numeric defaults shown are proposals for owner approval and remain externally configurable.

**Notes:**

* **Cross-refs:** Depends on **P0-001** and **P0-012**. Edits the same Kafka blocks as **P1-005**; the two should be applied together.
* **Implementation:** `CHANGE-AA-014`, Wave 2, complexity low. Both targets carry generated code. Affects all seven Kafka-using services.
* **Validation:** T-AA-014-01 (every required budget key resolves and reconnect backoff is bounded), T-AA-014-02 (bounded stall detection and no reconnect storm on broker loss). `mvn -f source/customer-app/pom.xml -pl common,order-service,notification-service -am test`.
* **Guardrail:** A session timeout shorter than the processing time of a slow batch causes unnecessary rebalances; the poll interval and batch size must be tuned together. `OQ-19` gates the numeric values.

<span style="font-size: 14px;">**MSFT Reference:** [Retry pattern](https://learn.microsoft.com/azure/architecture/patterns/retry)</span>

---

#### P1-004: Azure SQL pool and statement budgets are incomplete and failover recovery is unproven

**Priority: P1 - High Priority**

**Priority policy:** `AA-REMEDIATION-PRIORITY` v1.0.0, rule `P1-RCV-001` · **Change ID:** `CHANGE-AA-015` (Wave 2) · **Source ID:** F-020 · **Primary control:** `SQL-002`

**Severity:** High

**Resiliency Related:** Yes

**Finding status:** Verified finding

**Issue:** Connection strings set `loginTimeout=30` and configure no connect-retry behavior. No service configures a JDBC query timeout, a Hibernate statement timeout, or a `@Transactional` timeout. `order-service` sets `max-lifetime: 1200000` while `payment-service` declares only `connection-timeout` and `maximum-pool-size` with no `max-lifetime`, `keepaliveTime`, validation query, or leak detection. `open-in-view` is left at the framework default in `order-service` and `payment-service`.

**What does this solve:** It stops a slow dependency from holding request threads past the failure budget and shortens the recovery tail after a database endpoint change.

**Resiliency Impact:** A slow query or a stalled connection can block a request thread for far longer than the end-to-end failure budget, and stale pooled connections can persist after an endpoint or regional recovery, extending an outage beyond the platform failover.

**Recommended Fix:** Reduce `loginTimeout` to the request budget, express driver-level connect retry, complete the Hikari lifecycle settings (max lifetime, keepalive, validation timeout, leak detection) in every SQL-using service, declare JDBC and Hibernate statement timeouts, and set `open-in-view` explicitly.

**File:** source/customer-app/order-service/src/main/resources/application.yml:9-20

```yaml
// before
    datasource:
      url: jdbc:sqlserver://${AZURE_SQL_HOST:localhost}:1433;databaseName=${AZURE_SQL_DB:ecommerce_orders};encrypt=true;trustServerCertificate=false;loginTimeout=30;
      username: ${AZURE_SQL_USERNAME:${azure-sql-username}}
      password: ${AZURE_SQL_PASSWORD:${azure-sql-password}}
      driver-class-name: com.microsoft.sqlserver.jdbc.SQLServerDriver
      hikari:
        connection-timeout: 20000
        minimum-idle: 5
        maximum-pool-size: 20
        idle-timeout: 300000
        max-lifetime: 1200000
        pool-name: OrderHikariPool
```

**File:** source/customer-app/payment-service/src/main/resources/application.yml — `spring.datasource.hikari`

> Original source excerpt: Not available in authoritative evidence artifact. Step 2 evidence `EV-F-020-02` records `maximum-pool-size: 15` and `connection-timeout: 20000` with no `max-lifetime`, no validation query, and no leak detection.

**Fix:**

> Illustrative proposal only.

`source/customer-app/order-service/src/main/resources/application.yml` — `spring.datasource` and `spring.jpa`

```yaml
spring:
  datasource:
    url: jdbc:sqlserver://${AZURE_SQL_HOST}:1433;databaseName=${AZURE_SQL_DB};encrypt=true;trustServerCertificate=false;loginTimeout=${AZURE_SQL_LOGIN_TIMEOUT:10};connectRetryCount=${AZURE_SQL_CONNECT_RETRY_COUNT:3};connectRetryInterval=${AZURE_SQL_CONNECT_RETRY_INTERVAL:5};
    username: ${AZURE_SQL_USERNAME}
    password: ${AZURE_SQL_PASSWORD}
    driver-class-name: com.microsoft.sqlserver.jdbc.SQLServerDriver
    hikari:
      connection-timeout: ${SQL_POOL_CONNECTION_TIMEOUT_MS:5000}
      validation-timeout: ${SQL_POOL_VALIDATION_TIMEOUT_MS:2000}
      minimum-idle: ${SQL_POOL_MIN_IDLE:5}
      maximum-pool-size: ${SQL_POOL_MAX_SIZE:20}
      idle-timeout: ${SQL_POOL_IDLE_TIMEOUT_MS:300000}
      max-lifetime: ${SQL_POOL_MAX_LIFETIME_MS:900000}
      keepalive-time: ${SQL_POOL_KEEPALIVE_MS:120000}
      leak-detection-threshold: ${SQL_POOL_LEAK_DETECTION_MS:20000}
      pool-name: OrderHikariPool
  jpa:
    open-in-view: false
    properties:
      jakarta.persistence.query.timeout: ${SQL_QUERY_TIMEOUT_MS:5000}
      hibernate.query.timeout: ${SQL_QUERY_TIMEOUT_MS:5000}
```

`loginTimeout` drops from 30 to a request-budget-aligned value, `connectRetryCount` and `connectRetryInterval` express driver-level recovery after a failover, keepalive and `max-lifetime` evict stale connections after an endpoint change, and the query timeout bounds a slow statement. `open-in-view` is set explicitly rather than relying on the framework default the inventory records as unset. The numeric defaults are proposals for owner approval.

**Notes:**

* **Cross-refs:** Depends on **P0-012**. Prerequisite for **P0-006** and **P1-006** (the Resilience4j time limiter must be shorter than the SQL query timeout for the budget to be ordered).
* **Implementation:** `CHANGE-AA-015`, Wave 2, complexity low. Both targets carry generated code. Affects `order-service`, `payment-service`, and `user-service`.
* **Validation:** T-AA-015-01 (pool lifecycle, validation, and leak detection configured everywhere), T-AA-015-02 (bounded statement duration, stale-connection eviction, and restoration without a pod restart). `mvn -f source/customer-app/pom.xml -pl common,order-service,payment-service,user-service -am test`.
* **Guardrail:** Setting `open-in-view: false` can expose lazy-loading defects that the current default masks (`OQ-20`). A query timeout shorter than a legitimate long report query surfaces as a new failure and must be validated against observed latency (`OQ-19`).

<span style="font-size: 14px;">**MSFT Reference:** [Troubleshoot transient connection errors in Azure SQL Database](https://learn.microsoft.com/azure/azure-sql/database/troubleshoot-common-connectivity-issues)</span>

---

#### Messaging Durability

#### P1-005: Producer durability settings are inconsistent across services

**Priority: P1 - High Priority**

**Priority policy:** `AA-REMEDIATION-PRIORITY` v1.0.0, rule `P1-RCV-002` · **Change ID:** `CHANGE-AA-016` (Wave 2) · **Source ID:** F-006 · **Primary control:** `KAFKA-002`

**Severity:** High

**Resiliency Related:** Yes

**Finding status:** Verified finding

**Issue:** All producers set `acks: all` and `retries: 3`, but `enable.idempotence` is configured only in `order-service`. No producer configures `delivery.timeout.ms`. Five of six producers can therefore duplicate records on internal retry and none has an explicit delivery deadline.

**What does this solve:** It prevents internal producer retries from duplicating records during broker instability or a role transition, and stops delivery attempts from outliving the caller's deadline.

**Resiliency Impact:** During broker instability or a role transition, non-idempotent producers duplicate records while unbounded delivery attempts can outlive the caller deadline. A role transition can produce duplicate records from a producer that was mid-retry.

**Recommended Fix:** Enable idempotence on every producer, declare a bounded `delivery.timeout.ms`, and set an in-flight-request value consistent with idempotent ordering.

**File:** source/customer-app/product-service/src/main/resources/application.yml:34-41

```yaml
// before
      producer:
        key-serializer: org.apache.kafka.common.serialization.StringSerializer
        value-serializer: org.springframework.kafka.support.serializer.JsonSerializer
        acks: all
        retries: 3
        properties:
          security.protocol: SASL_SSL
          sasl.mechanism: PLAIN
```

**File:** source/customer-app/order-service/src/main/resources/application.yml:42-50

```yaml
// before
      producer:
        key-serializer: org.apache.kafka.common.serialization.StringSerializer
        value-serializer: org.springframework.kafka.support.serializer.JsonSerializer
        acks: all
        retries: 3
        properties:
          enable.idempotence: true
          max.in.flight.requests.per.connection: 5
```

**Fix:**

> Illustrative proposal only.

`source/customer-app/product-service/src/main/resources/application.yml` — `spring.kafka.producer`

```yaml
spring:
  kafka:
    producer:
      key-serializer: org.apache.kafka.common.serialization.StringSerializer
      value-serializer: org.springframework.kafka.support.serializer.JsonSerializer
      acks: all
      retries: ${KAFKA_PRODUCER_RETRIES:3}
      properties:
        enable.idempotence: true
        max.in.flight.requests.per.connection: ${KAFKA_MAX_IN_FLIGHT:5}
        delivery.timeout.ms: ${KAFKA_DELIVERY_TIMEOUT_MS:30000}
        linger.ms: ${KAFKA_LINGER_MS:5}
```

Brings `product-service` to the same durability contract `order-service` already has and adds the delivery deadline no producer declares today. With idempotence enabled, an in-flight value of 5 remains safe for ordering; the bounded delivery timeout stops attempts from outliving the caller. The `delivery.timeout.ms` default is a proposal and remains externally configurable.

**Notes:**

* **Cross-refs:** Depends on **P1-003** and **P0-012**. Related to **P0-008** (durability alone does not make failure observable; the outbox does).
* **Implementation:** `CHANGE-AA-016`, Wave 2, complexity low. Both targets carry generated code. Affects all six producing services.
* **Validation:** T-AA-016-01 (every producer resolves idempotence, bounded delivery timeout, and a compatible in-flight value), T-AA-016-02 (a forced internal retry records exactly one copy). `mvn -f source/customer-app/pom.xml -pl common,order-service,product-service,payment-service,inventory-service,user-service,cart-service -am test`.
* **Guardrail:** A delivery timeout shorter than the caller's own budget converts a slow broker into a caller-visible failure; the two must be ordered deliberately. Edits the same files as **P1-003**, so sequence them together to avoid conflicting merges.

<span style="font-size: 14px;">**MSFT Reference:** [Retry pattern](https://learn.microsoft.com/azure/architecture/patterns/retry)</span>

---

#### Dependency Isolation

#### P1-006: Backing services have no timeout, retry, circuit breaker, or bulkhead

**Priority: P1 - High Priority**

**Priority policy:** `AA-REMEDIATION-PRIORITY` v1.0.0, rule `P1-RCV-003` · **Change ID:** `CHANGE-AA-017` (Wave 3) · **Source ID:** F-019 · **Primary control:** `APP-AA-006`

**Severity:** Critical

**Resiliency Related:** Yes

**Finding status:** Verified finding

**Issue:** Resilience4j and Spring Cloud Circuit Breaker are declared only in `api-gateway`. The seven backing services declare no resilience library and use no `@CircuitBreaker`, `@Bulkhead`, `@TimeLimiter`, `@Retryable`, `@Recover`, `RetryTemplate`, or `@EnableRetry`. The observed failure handling is a `try/catch` around external calls that logs and returns normally. No optimistic-lock conflict handler and no deadlock retry exists despite `@Version` columns on three entities. `PaymentGatewayService` class documentation claims retry and circuit breaking; no such code exists in the class.

**What does this solve:** It contains a degraded dependency inside its own boundary so a regional dependency failure degrades one capability rather than the whole service.

**Resiliency Impact:** A single slow or failing dependency can consume all request threads in a service with no isolation boundary and no automatic recovery signal, so degradation propagates across the whole region rather than being contained. There is also no automatic recovery signal that readiness can consume.

**Recommended Fix:** Declare Resilience4j with named per-dependency instances in each backing service, apply a bulkhead and a time limiter to remote calls, restrict retry to idempotent operations and transient or optimistic-lock exceptions with jittered backoff, and enable automatic open-to-half-open transition so recovery needs no restart.

**File:** source/customer-app — backing service resilience inventory (evidence `EV-F-019-01`; original source excerpt: `not_applicable`)

> The authoritative inventory records `resilience4j`, `spring_retry`, `circuit_breaker`, `bulkhead`, `rate_limiter`, `time_limiter`, and `declarative_fallback` as `absent_in_all_seven` backing services.

**File:** source/customer-app/payment-service/src/main/java/com/ecommerce/payment/service/PaymentGatewayService.java:13-20

```java
// before
/**
 * Payment Gateway Service - Abstracts payment gateway integration.
 * In production, this would integrate with Stripe, Braintree, or Azure Payment Services.
 * Implements retry logic, circuit breaking, and PCI-DSS compliant tokenization.
 */
@Slf4j
@Service
public class PaymentGatewayService {
```

**Fix:**

> Illustrative proposal only.

`source/customer-app/order-service/pom.xml` — dependencies

```xml
<dependency>
  <groupId>io.github.resilience4j</groupId>
  <artifactId>resilience4j-spring-boot3</artifactId>
  <version>${resilience4j.version}</version>
</dependency>
<dependency>
  <groupId>org.springframework.boot</groupId>
  <artifactId>spring-boot-starter-aop</artifactId>
</dependency>
```

Brings the same resilience library `api-gateway` already uses into the backing services. `spring-boot-starter-aop` is required for the annotation-driven aspects. The version is a property so the team can align it with the version already resolved for `api-gateway` rather than a value invented here.

`source/customer-app/order-service/src/main/resources/application.yml` — `resilience4j`

```yaml
resilience4j:
  circuitbreaker:
    instances:
      orders-sql:
        slidingWindowSize: ${R4J_SQL_WINDOW:20}
        minimumNumberOfCalls: ${R4J_SQL_MIN_CALLS:10}
        failureRateThreshold: ${R4J_SQL_FAILURE_RATE:50}
        waitDurationInOpenState: ${R4J_SQL_OPEN_WAIT:20s}
        permittedNumberOfCallsInHalfOpenState: ${R4J_SQL_HALF_OPEN_CALLS:3}
        automaticTransitionFromOpenToHalfOpenEnabled: true
        registerHealthIndicator: true
  bulkhead:
    instances:
      orders-sql:
        maxConcurrentCalls: ${R4J_SQL_MAX_CONCURRENT:16}
        maxWaitDuration: ${R4J_SQL_MAX_WAIT:100ms}
  timelimiter:
    instances:
      orders-sql:
        timeoutDuration: ${R4J_SQL_TIMEOUT:4s}
        cancelRunningFuture: true
  retry:
    instances:
      orders-sql-idempotent:
        maxAttempts: ${R4J_SQL_RETRY_ATTEMPTS:3}
        waitDuration: ${R4J_SQL_RETRY_WAIT:200ms}
        enableExponentialBackoff: true
        enableRandomizedWait: true
        retryExceptions:
          - org.springframework.dao.TransientDataAccessException
          - org.springframework.dao.OptimisticLockingFailureException
```

Per-dependency named instances give the isolation boundary the backing services lack. The time limiter is shorter than the SQL query timeout from **P1-004** so the budget is ordered, the bulkhead caps concurrent calls so one dependency cannot consume the whole thread pool, and retry is restricted to transient and optimistic-lock exceptions so a non-idempotent operation is never blindly repeated. Randomized wait supplies the jitter the standard requires, and `automaticTransitionFromOpenToHalfOpenEnabled` provides recovery without a restart. All numeric thresholds are proposals and remain externally configurable.

**Notes:**

* **Cross-refs:** Depends on **P0-006** (retry must never be applied to the non-idempotent provider call), **P1-004**, and **P0-012**.
* **Implementation:** `CHANGE-AA-017`, Wave 3, complexity high. All three targets carry generated code. Affects all seven backing services.
* **Validation:** T-AA-017-01 (a stalled dependency cannot exhaust the request pool), T-AA-017-02 (breaker opens, half-opens, and closes without a restart), T-AA-017-03 (optimistic-lock conflict retried within a bounded budget; non-idempotent operations not retried). `mvn -f source/customer-app/pom.xml -pl common,order-service,payment-service,inventory-service,product-service -am test`.
* **Guardrail:** A bulkhead sized too small throttles legitimate traffic; sizing must be derived from observed concurrency. Adding AOP proxies to service beans changes self-invocation semantics inside the same class. `OQ-21` records that the Resilience4j version already resolved for `api-gateway` is unknown (`UNC-016`).

<span style="font-size: 14px;">**MSFT Reference:** [Circuit Breaker pattern](https://learn.microsoft.com/azure/architecture/patterns/circuit-breaker)</span>

---

#### Gateway Budget and Fallback

#### P1-007: Gateway HTTP client pool is shared and its timeout budget conflicts with the circuit breaker

**Priority: P1 - High Priority**

**Priority policy:** `AA-REMEDIATION-PRIORITY` v1.0.0, rule `P1-RCV-003` · **Change ID:** `CHANGE-AA-018` (Wave 2) · **Source ID:** F-022 · **Primary control:** `HTTP-001`

**Severity:** High

**Resiliency Related:** Yes

**Finding status:** Verified finding

**Issue:** The Netty client declares `connect-timeout: 5000` and `response-timeout: 30s` only. No connection pool sizing, acquire timeout, max-idle-time, max-life-time, or end-to-end operation deadline is configured, so one shared pool and one timeout profile serve seven materially different downstream services. The default `TimeLimiter` is 10s while the client response timeout is 30s. Exactly one route applies a Retry filter, limited to `SERVICE_UNAVAILABLE`, with no Retry-After handling, no 429 classification, and no jitter.

**What does this solve:** It stops one slow downstream from degrading every route and makes the failure budget ordered so the observed failure matches the reported one.

**Resiliency Impact:** A single slow downstream service can exhaust the shared connection pool and degrade all routes. The breaker fires at 10s while the client waits up to 30s, so the failure is reported before the client observes it, and retry classification cannot honour server guidance during regional congestion.

**Recommended Fix:** Bound the Netty pool with explicit max connections, acquire timeout, max idle time, and max life time; make the client response timeout shorter than the breaker time limit for every named instance; and extend retry classification to 429 and 504 with jittered backoff restricted to idempotent methods.

**File:** source/customer-app/api-gateway/src/main/resources/application.yml:30-32

```yaml
// before
        httpclient:
          connect-timeout: 5000
          response-timeout: 30s
```

**File:** source/customer-app/api-gateway/src/main/resources/application.yml:111-117

```yaml
// before
    timelimiter:
      configs:
        default:
          timeoutDuration: 10s
      instances:
        payment-service-cb:
          timeoutDuration: 30s
```

**Fix:**

> Illustrative proposal only.

`source/customer-app/api-gateway/src/main/resources/application.yml` — `spring.cloud.gateway.httpclient` and `resilience4j.timelimiter`

```yaml
spring:
  cloud:
    gateway:
      httpclient:
        connect-timeout: ${GW_CONNECT_TIMEOUT_MS:2000}
        response-timeout: ${GW_RESPONSE_TIMEOUT:6s}
        pool:
          type: FIXED
          name: gateway-downstream
          max-connections: ${GW_POOL_MAX_CONNECTIONS:200}
          acquire-timeout: ${GW_POOL_ACQUIRE_TIMEOUT_MS:500}
          max-idle-time: ${GW_POOL_MAX_IDLE:30s}
          max-life-time: ${GW_POOL_MAX_LIFE:300s}

resilience4j:
  timelimiter:
    configs:
      default:
        timeoutDuration: ${GW_BREAKER_TIMEOUT:8s}
        cancelRunningFuture: true
    instances:
      payment-service-cb:
        timeoutDuration: ${GW_PAYMENT_BREAKER_TIMEOUT:12s}
```

The pool gains explicit bounds and an acquire timeout, so a slow downstream saturates its own acquisition path instead of silently queueing. The budget is now ordered: the client response timeout is shorter than the breaker time limit for both the default and the payment instance, which reverses today's inverted 30s client versus 10s breaker relationship.

`source/customer-app/api-gateway/src/main/java/com/ecommerce/gateway/config/GatewayRoutesConfig.java` — `customRouteLocator` retry filter

```java
// Applied to idempotent GET routes only. Retry classification now covers server guidance.
.filters(f -> f
        .circuitBreaker(cb -> cb
                .setName("product-service-cb")
                .setFallbackUri("forward:/fallback/product-service"))
        .retry(retryConfig -> retryConfig
                .setRetries(3)
                .setMethods(HttpMethod.GET)
                .setStatuses(HttpStatus.SERVICE_UNAVAILABLE,
                             HttpStatus.TOO_MANY_REQUESTS,
                             HttpStatus.GATEWAY_TIMEOUT)
                .setBackoff(Duration.ofMillis(100), Duration.ofMillis(1000), 2, true)))
```

Extends the single existing retry filter beyond `SERVICE_UNAVAILABLE` to include 429 and 504, restricts it to GET so a non-idempotent request is never retried, and enables the `basedOnPreviousValue` backoff flag so successive waits are jittered rather than fixed.

**Notes:**

* **Cross-refs:** Depends on **P1-008** (tightening the gateway budget is only safe once the fallback targets resolve) and **P0-012**. Wave 2 sequences **P1-008** before this change.
* **Implementation:** `CHANGE-AA-018`, Wave 2, complexity medium. All three targets carry generated code.
* **Validation:** T-AA-018-01 (client deadline shorter than breaker time limit for every instance), T-AA-018-02 (one slow downstream cannot starve a healthy one), T-AA-018-03 (429 with Retry-After honoured; non-GET never retried). `mvn -f source/customer-app/pom.xml -pl common,api-gateway -am test`.
* **Guardrail:** A `FIXED` pool sized too small produces acquire timeouts under normal peak load. Shortening the response timeout from 30s will surface previously hidden slow downstreams as failures. `OQ-22` records that Spring Cloud Gateway supports one shared client pool and that true per-dependency pools may require separate route-level client configuration.

<span style="font-size: 14px;">**MSFT Reference:** [Bulkhead pattern](https://learn.microsoft.com/azure/architecture/patterns/bulkhead)</span>

---

#### P1-008: Gateway circuit-breaker fallback targets have no handler

**Priority: P1 - High Priority**

**Priority policy:** `AA-REMEDIATION-PRIORITY` v1.0.0, rule `P1-RCV-006` · **Change ID:** `CHANGE-AA-019` (Wave 2) · **Source ID:** F-021 · **Primary control:** `APP-FALLBACK-001`

**Severity:** High

**Resiliency Related:** Yes

**Finding status:** Verified finding

**Issue:** All ten gateway routes apply a `circuitBreaker` filter with `fallbackUri: forward:/fallback/<service>`. No handler mapped to `/fallback/**` exists in `api-gateway` or in any other module, so the forward cannot be resolved. Primary failure, fallback success, and dual failure are therefore indistinguishable to the caller and to telemetry.

**What does this solve:** It gives callers stable degraded semantics and gives operators the ability to distinguish an open breaker from a broken fallback.

**Resiliency Impact:** When a breaker opens during a regional dependency failure, the caller receives an unmapped error instead of an explicit degraded-mode response, and operators cannot distinguish an open breaker from a broken fallback. A partially available downstream cannot be served in a safe degraded mode.

**Recommended Fix:** Add a reactive fallback controller that returns 503 with a stable problem body identifying the degraded service and a Retry-After hint, and increments a counter tagged by service and outcome.

**File:** source/customer-app/api-gateway/src/main/java/com/ecommerce/gateway/config/GatewayRoutesConfig.java:33-187 — `customRouteLocator`

> Original source excerpt: Not available in authoritative evidence artifact. Step 2 recorded no exact excerpt for this finding. All ten routes apply a `circuitBreaker` filter with `fallbackUri: forward:/fallback/<service>`, and the authoritative inventory records that no `/fallback/**` handler exists anywhere in the repository. The finding rests on an absence rather than on a quoted line.

**Fix:**

> Illustrative proposal only.

`source/customer-app/api-gateway/src/main/java/com/ecommerce/gateway/fallback/FallbackController.java`

```java
package com.ecommerce.gateway.fallback;

import io.micrometer.core.instrument.MeterRegistry;
import java.time.Instant;
import java.util.Map;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.http.HttpHeaders;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;
import reactor.core.publisher.Mono;

/** Resolves the ten forward:/fallback/<service> targets declared by GatewayRoutesConfig. */
@Slf4j
@RestController
@RequiredArgsConstructor
public class FallbackController {

    private final MeterRegistry meterRegistry;

    @RequestMapping("/fallback/{service}")
    public Mono<ResponseEntity<Map<String, Object>>> fallback(@PathVariable String service) {
        meterRegistry.counter("gateway.fallback",
                "service", service, "outcome", "degraded").increment();
        log.warn("Serving degraded response for {}; upstream breaker is open", service);

        return Mono.just(ResponseEntity
                .status(HttpStatus.SERVICE_UNAVAILABLE)
                .header(HttpHeaders.RETRY_AFTER, "5")
                .body(Map.of(
                        "status", 503,
                        "error", "Service Unavailable",
                        "degradedService", service,
                        "detail", "Upstream dependency is unavailable; the request was not processed.",
                        "timestamp", Instant.now().toString())));
    }
}
```

Supplies the handler the ten `fallbackUri` targets currently forward to and that exists nowhere in the repository. The response is bounded because it performs no downstream call, it names the degraded service so the caller and telemetry can distinguish an open breaker from a broken fallback, and Retry-After gives the caller explicit guidance.

**Notes:**

* **Cross-refs:** Depends on **P0-012**. Prerequisite for **P1-007** in Wave 2 sequencing. Contributes a counter that must follow the naming convention established by **P3-003**.
* **Implementation:** `CHANGE-AA-019`, Wave 2, complexity low. Both targets carry generated code. No existing file is modified; two files are added.
* **Validation:** T-AA-019-01 (each of the ten fallback targets returns a bounded, identified degraded response), T-AA-019-02 (distinct metrics for primary failure, fallback success, and dual failure). `mvn -f source/customer-app/pom.xml -pl common,api-gateway -am test`.
* **Guardrail:** Returning 503 rather than the current unmapped error is a contract change for existing clients (`OQ-23`). `UNC-010` records that `api-gateway` is reactive while `common` carries a servlet `@ControllerAdvice`; the new controller must be reactive to avoid the same mismatch.

<span style="font-size: 14px;">**MSFT Reference:** [Circuit Breaker pattern](https://learn.microsoft.com/azure/architecture/patterns/circuit-breaker)</span>

---

#### Execution Boundaries

#### P1-009: Async listener execution has no bounded executor

**Priority: P1 - High Priority**

**Priority policy:** `AA-REMEDIATION-PRIORITY` v1.0.0, rule `P1-RCV-003` · **Change ID:** `CHANGE-AA-020` (Wave 3) · **Source ID:** F-030 · **Primary control:** `APP-ASYNC-002`

**Severity:** High

**Resiliency Related:** Yes

**Finding status:** Verified finding

**Issue:** Every notification listener is annotated `@Async`, yet `notification-service` does not declare `@EnableAsync`, while `order`, `payment`, `cart`, and `inventory` services declare `@EnableAsync` and contain no `@Async` method. No `Executor` bean, `queueCapacity`, `RejectedExecutionHandler`, or named executor exists anywhere in the repository.

**What does this solve:** It replaces an unspecified, unbounded, undrained execution model with one that is bounded, attributable, and safe at shutdown.

**Resiliency Impact:** If async interception is active, work is dispatched to a framework-default executor whose queue and rejection behavior are not bounded or observed, and in-flight work is lost at shutdown. If interception is not established, the listeners execute synchronously on the container thread with materially different failure semantics. Neither behavior is expressed or tested.

**Recommended Fix:** Define a named `ThreadPoolTaskExecutor` with explicit queue capacity, an explicit rejection policy, and shutdown draining wherever async execution is genuinely used, and remove stray `@EnableAsync` declarations from services with no `@Async` method.

**File:** source/customer-app/notification-service/src/main/java/com/ecommerce/notification/service/NotificationEventConsumer.java:20-36

```java
// before
@Slf4j
@Service
@RequiredArgsConstructor
public class NotificationEventConsumer {

    private final EmailNotificationService emailService;
    private final SmsNotificationService smsService;
    private final PushNotificationService pushService;
    private final NotificationRepository notificationRepository;

    // ============================================================
    // ORDER EVENT CONSUMERS
    // ============================================================

    @KafkaListener(topics = KafkaTopics.ORDER_CREATED, groupId = KafkaTopics.GROUP_NOTIFICATION_SERVICE)
    @Async
    public void handleOrderCreated(Map<String, Object> event) {
```

**File:** source/customer-app/cart-service/src/main/java/com/ecommerce/cartservice/CartServiceApplication.java:11-12

```java
// before
@EnableAsync
@EnableScheduling
```

**Fix:**

> Illustrative proposal only.

`source/customer-app/common/src/main/java/com/ecommerce/common/async/BoundedAsyncExecutorConfig.java`

```java
package com.ecommerce.common.async;

import java.util.concurrent.Executor;
import java.util.concurrent.ThreadPoolExecutor;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.scheduling.concurrent.ThreadPoolTaskExecutor;

@Configuration
public class BoundedAsyncExecutorConfig {

    @Bean("applicationTaskExecutor")
    public Executor applicationTaskExecutor(
            @Value("${app.async.core-pool-size:4}") int corePoolSize,
            @Value("${app.async.max-pool-size:16}") int maxPoolSize,
            @Value("${app.async.queue-capacity:200}") int queueCapacity,
            @Value("${app.async.await-termination-seconds:20}") int awaitTerminationSeconds) {

        ThreadPoolTaskExecutor executor = new ThreadPoolTaskExecutor();
        executor.setThreadNamePrefix("app-async-");
        executor.setCorePoolSize(corePoolSize);
        executor.setMaxPoolSize(maxPoolSize);
        executor.setQueueCapacity(queueCapacity);
        // Backpressure onto the caller instead of silently dropping or growing without bound.
        executor.setRejectedExecutionHandler(new ThreadPoolExecutor.CallerRunsPolicy());
        executor.setWaitForTasksToCompleteOnShutdown(true);
        executor.setAwaitTerminationSeconds(awaitTerminationSeconds);
        executor.initialize();
        return executor;
    }
}
```

Supplies the executor, queue capacity, and rejection policy that exist nowhere today. The named thread prefix makes the pool attributable in thread dumps and Micrometer's executor metrics, `CallerRunsPolicy` applies backpressure rather than dropping work, and the shutdown settings drain queued work within a bound so the **P0-011** drain is meaningful. Pool and queue sizes are proposals and remain externally configurable.

`source/customer-app/cart-service/src/main/java/com/ecommerce/cartservice/CartServiceApplication.java`

```java
// @EnableAsync removed: cart-service declares no @Async method.
@SpringBootApplication
@EnableScheduling
public class CartServiceApplication {

    public static void main(String[] args) {
        SpringApplication.run(CartServiceApplication.class, args);
    }
}
```

Removes async infrastructure from a service that never uses it. The same removal applies to `order-service`, `payment-service`, and `inventory-service`. `@EnableScheduling` is retained because `cart-service` does declare scheduled work.

**Notes:**

* **Cross-refs:** Depends on **P2-002** and **P0-012**. If **P2-002** lands first and removes `@Async` from the notification listeners, `notification-service` may need no executor at all and this change reduces to removing stray `@EnableAsync` declarations (`OQ-24`).
* **Implementation:** `CHANGE-AA-020`, Wave 3, complexity low. All three targets carry generated code.
* **Validation:** T-AA-020-01 (bounded queue capacity and explicit rejection policy), T-AA-020-02 (shutdown drains or durably records queued work). `mvn -f source/customer-app/pom.xml -pl common,cart-service,notification-service -am test`.
* **Guardrail:** Naming the bean `applicationTaskExecutor` replaces the framework default and affects any other component relying on it.

<span style="font-size: 14px;">**MSFT Reference:** [Bulkhead pattern](https://learn.microsoft.com/azure/architecture/patterns/bulkhead)</span>

---

#### Management Surface

#### P1-010: Actuator exposes administrative and detailed endpoints without protection on the traffic port

**Priority: P1 - High Priority**

**Priority policy:** `AA-REMEDIATION-PRIORITY` v1.0.0, rule `P1-RCV-003` · **Change ID:** `CHANGE-AA-021` (Wave 2) · **Source ID:** F-029 · **Primary control:** `APP-ACT-002`

**Severity:** Critical

**Resiliency Related:** Yes

**Finding status:** Verified finding

**Issue:** `api-gateway` exposes health, info, metrics, prometheus, and the administrative `gateway` endpoint, with `show-details: always` and the gateway endpoint explicitly enabled. No service configures a separate `management.server.port`, and no `SecurityFilterChain` or `EndpointRequest` matcher protects the management endpoints. The `api-gateway` Kubernetes Service is type `LoadBalancer` with the internal annotation set to `false`, mapping 443 to the same container port that serves the actuator.

**What does this solve:** It prevents route-table inspection and manipulation and stops dependency topology and error text from being disclosed to any caller that reaches the load balancer in either region.

**Resiliency Impact:** The gateway route table can be inspected and manipulated, and full health detail including dependency topology and error text is disclosed to any caller that reaches the load balancer, in both regions. Because the actuator shares sockets and request threads with business traffic, unauthenticated callers can also consume shared application resources — the missing isolation boundary that rule `P1-RCV-003` describes.

**Recommended Fix:** Bind management to a separate port that the internet-facing Service does not publish, remove and disable the administrative `gateway` endpoint, change `show-details` to `when-authorized`, and point probes at the management port using named container ports.

**File:** source/customer-app/api-gateway/src/main/resources/application.yml:119-129

```yaml
// before
# Actuator
management:
  endpoints:
    web:
      exposure:
        include: health,info,metrics,prometheus,gateway
  endpoint:
    health:
      show-details: always
    gateway:
      enabled: true
```

**File:** source/customer-app/k8s/services/api-gateway.yaml:1-60 — Service `api-gateway`

> Original source excerpt: Not available in authoritative evidence artifact. Step 2 evidence `EV-F-029-02` records that the Service is type `LoadBalancer` with `service.beta.kubernetes.io/azure-load-balancer-internal: false`, exposing 443 mapped to plaintext container port 8080, which is the same port that serves the actuator.

**Fix:**

> Illustrative proposal only.

`source/customer-app/api-gateway/src/main/resources/application.yml` — `management`

```yaml
management:
  server:
    port: ${MANAGEMENT_PORT:9090}
  endpoints:
    web:
      exposure:
        include: health,info,prometheus,metrics
        exclude: gateway
  endpoint:
    health:
      show-details: when-authorized
      probes:
        enabled: true
    gateway:
      enabled: false
```

Management moves off the traffic port so the internet-facing LoadBalancer no longer reaches it, the administrative gateway endpoint is both removed from the exposed set and disabled, and full health detail is restricted. The probe paths are unchanged in shape; only the port changes, so the workload manifests must follow.

`source/customer-app/k8s/services/all-services.yaml` — container ports and probe ports

```yaml
ports:
  - name: http
    containerPort: 8081
  - name: management
    containerPort: 9090
livenessProbe:
  httpGet:
    path: /actuator/health/liveness
    port: management
readinessProbe:
  httpGet:
    path: /actuator/health/readiness
    port: management
```

Probes follow the management port while the Service continues to publish only the `http` port. Named ports keep the probe definitions readable and prevent a future port change from silently breaking the probes. This is an application-owned workload manifest edit; no Azure resource is provisioned.

**Illustrative code status:** Targeted implementation discovery required (`TD-08`)

**Target:** Reactive `SecurityWebFilterChain` restricting actuator endpoints — repository path not yet selected

**Why code was not generated:** Whether `api-gateway` has Spring Security on its classpath cannot be established from the supplied artifacts. `common` declares `spring-boot-starter-security`, but `UNC-006` records that `common` currently fails to compile against missing Spring Security packages and `UNC-010` records that `common`'s bean visibility to `api-gateway` is unverified. Writing a `SecurityWebFilterChain` would require asserting a classpath and a servlet-versus-reactive security variant that no supplied artifact confirms.

**Unresolved inputs:**

* Whether `spring-boot-starter-security` and its reactive variant are on the `api-gateway` classpath
* Approved authentication mechanism for management endpoints
* Resolution of `UNC-006` and `UNC-010`

**Intended behavior:** Control `APP-ACT-002` also expects an authorization boundary on the management endpoints in addition to port isolation, so a compromised in-cluster caller cannot read full health detail.

**Notes:**

* **Cross-refs:** Depends on **P0-003** (both rewrite the management block of every `application.yml` and must be merged as one edit per service) and **P0-012**.
* **Implementation:** `CHANGE-AA-021`, Wave 2, complexity medium. Three of four targets carry generated code. `OQ-05` records that the security owner may elect a documented priority override on security-governance grounds; **no override is applied by this plan** and the calculated priority remains P1 under `P1-RCV-003`.
* **Validation:** T-AA-021-01 (gateway endpoint unexposed, details not always shown, management on a separate port), T-AA-021-02 (actuator unreachable on the traffic port). `mvn -f source/customer-app/pom.xml -pl common,api-gateway -am test`.
* **Guardrail:** Any Prometheus scrape configuration targeting the traffic port must be updated to the management port. Changing probe ports requires the workload manifests and the application configuration to change together or probes will fail.

<span style="font-size: 14px;">**MSFT Reference:** [Security design principles — Azure Well-Architected Framework](https://learn.microsoft.com/azure/well-architected/security/principles)</span>

---

#### Startup and Credential Lifecycle

#### P1-011: Key Vault startup and rotation contract is absent

**Priority: P1 - High Priority**

**Priority policy:** `AA-REMEDIATION-PRIORITY` v1.0.0, rule `P1-RCV-004` · **Change ID:** `CHANGE-AA-022` (Wave 3) · **Source ID:** F-033 · **Primary control:** `KV-009`

**Severity:** Critical

**Resiliency Related:** Yes

**Finding status:** Verified finding

**Issue:** Key Vault is used exclusively through the Spring Cloud Azure property source. No `RetryOptions`, `ClientOptions`, startup timeout, fail-fast policy, or last-known-good policy is declared. No `com.azure` Key Vault SDK type is referenced in any Java class, so there is no client to bound or recreate. There is no `@RefreshScope`, `EnvironmentChangeEvent` listener, scheduled refresh, or client recreation anywhere. `order-service` and `payment-service` default the property source to `enabled: false`, so the effective secret source differs by service.

**What does this solve:** It removes the divergent per-service secret source, bounds startup behavior, and eliminates the mandatory pod restart after rotation.

**Resiliency Impact:** A transient vault, identity, DNS, or private endpoint problem during startup produces unbounded or silently degraded behavior with no explicit policy, and after any secret rotation or credential recovery the only remediation is a pod restart in both regions.

**Recommended Fix:** Make the Key Vault enablement default identical across services, declare an explicit bounded retry budget and a required-versus-optional startup policy, and introduce a refresh seam that re-reads rotated material and asks registered clients to reinitialize without a restart.

**File:** source/customer-app/api-gateway/src/main/resources/application.yml:37-42

```yaml
// before
    azure:
      keyvault:
        secret:
          endpoint: https://ecommerce-keyvault.vault.azure.net/
          credential:
            managed-identity-enabled: true
```

**File:** source/customer-app/order-service/src/main/resources/application.yml:63-68

```yaml
// before
    cloud:
      azure:
        keyvault:
          secret:
            endpoint: ${AZURE_KEYVAULT_ENDPOINT:}
            enabled: ${AZURE_KEYVAULT_ENABLED:false}
```

**File:** source/customer-app/api-gateway/src/main/resources/application.yml:58-59

```yaml
// before
jwt:
  secret: ${jwt-secret}
```

**Fix:**

> Illustrative proposal only.

`source/customer-app/order-service/src/main/resources/application.yml` — `spring.cloud.azure.keyvault.secret` and `app.secrets`

```yaml
spring:
  cloud:
    azure:
      keyvault:
        secret:
          endpoint: ${AZURE_KEYVAULT_ENDPOINT}
          enabled: ${AZURE_KEYVAULT_ENABLED:true}
          credential:
            managed-identity-enabled: true
          retry:
            mode: exponential
            exponential:
              max-retries: ${AZURE_KEYVAULT_MAX_RETRIES:3}
              base-delay: ${AZURE_KEYVAULT_BASE_DELAY:PT0.5S}
              max-delay: ${AZURE_KEYVAULT_MAX_DELAY:PT5S}

app:
  secrets:
    required: ${APP_SECRETS_REQUIRED:true}
    startup-timeout: ${APP_SECRETS_STARTUP_TIMEOUT:15s}
    refresh-interval: ${APP_SECRETS_REFRESH_INTERVAL:30m}
```

The enablement default changes from `false` to `true` so every service resolves secrets from the same source, and vault access gains an explicit bounded retry budget instead of relying on SDK defaults. The `app.secrets` block declares the required-versus-optional policy, the startup budget, and the refresh cadence that `KV-005`, `KV-009`, and `KV-010` require. Task Implementor must confirm the exact Spring Cloud Azure retry property names against the resolved 5.10.0 artifact.

`source/customer-app/common/src/main/java/com/ecommerce/common/secrets/SecretRefreshCoordinator.java`

```java
package com.ecommerce.common.secrets;

import java.util.List;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.scheduling.annotation.Scheduled;
import org.springframework.stereotype.Component;

/**
 * Re-reads rotated material and asks registered clients to recreate themselves, so recovery
 * after a rotation does not require a process or pod restart.
 */
@Slf4j
@Component
@RequiredArgsConstructor
public class SecretRefreshCoordinator {

    /** Implemented by each component holding credential-derived state. */
    public interface SecretAwareClient {
        String name();
        void reinitializeWithCurrentSecrets();
    }

    private final SecretRefreshProperties properties;
    private final List<SecretAwareClient> clients;

    @Scheduled(fixedDelayString = "#{@secretRefreshProperties.refreshInterval.toMillis()}")
    public void refreshIfRotated() {
        for (SecretAwareClient client : clients) {
            try {
                client.reinitializeWithCurrentSecrets();
            } catch (Exception e) {
                log.error("Secret refresh failed for client {}", client.name(), e);
            }
        }
    }
}
```

Establishes the missing refresh seam using only Spring scheduling and a repository-owned interface, so a data source, Kafka client, or Redis connection factory can opt in without the coordinator knowing any vendor SDK. The bound `SecretRefreshProperties` class makes the required-versus-optional startup contract explicit and validated, replacing today's implicit and per-service-divergent behavior.

**Illustrative code status:** Targeted implementation discovery required (`TD-09`)

**Target:** Explicit Key Vault secret client and rotation detection — repository path not yet selected

**Why code was not generated:** No `com.azure` Key Vault SDK type is referenced in any Java class; Key Vault is consumed only through the Spring Cloud Azure startup property source, so there is no client object to bound, recreate, or query. Introducing one requires selecting between refreshing the Spring property source and adding a direct `SecretClient`, which is an architecture decision, and `UNC-016` records that the effective Spring Cloud Azure artifact was never resolved.

**Unresolved inputs:**

* Approved mechanism for detecting rotation (property-source refresh versus direct `SecretClient`)
* Effective `spring-cloud-azure-starter-keyvault-secrets` 5.10.0 client and refresh API
* Which credential-derived clients must be recreated on rotation

**Intended behavior:** Detecting that a secret has actually rotated requires an explicit vault client that can re-read the current secret version, which also unblocks the Key Vault readiness contributor deferred by **P0-003** (`TD-02`).

**Notes:**

* **Cross-refs:** Depends on **P0-001**, **P0-003**, and **P0-012**. Unblocks `TD-02` under **P0-003**. Shares decision gate `spring_cloud_azure_client_customization` with **P0-002** and **P1-002**.
* **Implementation:** `CHANGE-AA-022`, Wave 3, complexity high. Three of four targets carry generated code.
* **Validation:** T-AA-022-01 (bounded fail-fast within `startupTimeout` when the vault is unreachable and required), T-AA-022-02 (rotated secret reaches the initialized client without a restart, or a documented restart contract is enforced), T-AA-022-03 (every service resolves the same enablement default). `mvn -f source/customer-app/pom.xml -pl common,api-gateway,order-service,payment-service -am test`.
* **Guardrail:** Changing the enablement default from `false` to `true` in `order-service` and `payment-service` makes the vault a **startup dependency for those services for the first time**. Recreating a data source at runtime can disrupt in-flight transactions and must be sequenced with the **P0-011** drain behavior. `OQ-26` and `OQ-04` remain open.

<span style="font-size: 14px;">**MSFT Reference:** [Azure Key Vault best practices](https://learn.microsoft.com/azure/key-vault/general/best-practices)</span>

---

#### Bounded Batch Processing

#### P1-012: Scheduled reservation expiry loads the entire active inventory set into memory

**Priority: P1 - High Priority**

**Priority policy:** `AA-REMEDIATION-PRIORITY` v1.0.0, rule `P1-RCV-003` · **Change ID:** `CHANGE-AA-023` (Wave 3) · **Source ID:** F-034 · **Primary control:** `APP-BATCH-004`

**Severity:** High

**Resiliency Related:** Yes

**Finding status:** Verified finding

**Issue:** `expireOldReservations` calls `findByStatus("ACTIVE")` and materialises the full result into a `List` every five minutes, then iterates every reservation on every document. There is no pagination, streaming, page size, or checkpoint.

**What does this solve:** It removes correlated memory pressure and query load in both regions and makes the sweep resumable after an interruption.

**Resiliency Impact:** As the catalogue grows, the sweep allocates the full active inventory in heap on every replica every five minutes, producing correlated memory pressure and query load in both regions simultaneously with no bound. A promoted region restarts a full scan instead of resuming.

**Recommended Fix:** Replace the unbounded materialisation with a bounded page loop that filters on the expiry predicate as well as status, applies an explicit per-run ceiling, re-checks ownership between pages, and defers the remainder to the next run.

**File:** source/customer-app/inventory-service/src/main/java/com/ecommerce/inventory/service/InventoryService.java:268-273

```java
// before
    @Scheduled(fixedDelay = 300000) // Every 5 minutes
    public void expireOldReservations() {
        log.debug("Running reservation expiry job...");
        LocalDateTime now = LocalDateTime.now();
        List<InventoryDocument> allInventory = inventoryRepository.findByStatus("ACTIVE");
        
```

**Fix:**

> Illustrative proposal only.

`source/customer-app/inventory-service/src/main/java/com/ecommerce/inventory/service/InventoryService.java` — `nextExpiryPage` and `expireReservationsForOwnedTerm`

```java
@Value("${app.inventory.reservation-expiry.page-size:200}")
private int expiryPageSize;

@Value("${app.inventory.reservation-expiry.max-documents-per-run:5000}")
private int maxDocumentsPerRun;

private void expireReservationsForOwnedTerm() {
    LocalDateTime now = LocalDateTime.now();
    int processed = 0;
    int pageNumber = 0;

    while (processed < maxDocumentsPerRun) {
        if (!ownershipGuard.isOwner()) {
            log.warn("Ownership lost after {} documents; stopping reservation expiry", processed);
            return;
        }

        Page<InventoryDocument> page = inventoryRepository
                .findByStatusAndReservationsExpiresAtBefore(
                        "ACTIVE", now, PageRequest.of(pageNumber, expiryPageSize));

        if (page.isEmpty()) {
            return;
        }

        page.getContent().forEach(inv -> expireDueReservations(inv, now));

        processed += page.getNumberOfElements();
        pageNumber++;
    }

    log.info("Reservation expiry reached the per-run bound of {} documents; "
            + "remaining work resumes on the next scheduled run", maxDocumentsPerRun);
}
```

The unbounded `List` is replaced by a bounded page loop with an explicit per-run ceiling, so heap use no longer grows with the catalogue. The query filters on the expiry predicate as well as status, so pages contain only documents with work to do rather than the whole active set. Ownership is re-checked between pages, and reaching the per-run bound defers the remainder to the next run, which makes the sweep naturally resumable. Page size and ceiling are proposals and remain externally configurable.

**Notes:**

* **Cross-refs:** Depends on **P0-010** (edits the same method and must rebase onto it) and **P0-012**. Addresses the same unbounded-materialisation defect that the **P0-007** outbox relay avoids with a `Limit` parameter.
* **Implementation:** `CHANGE-AA-023`, Wave 3, complexity medium. Both targets carry generated code.
* **Validation:** T-AA-023-01 (bounded heap use and paged iteration with a large active data set), T-AA-023-02 (the sweep stops at the per-run ceiling and resumes on the next run). `mvn -f source/customer-app/pom.xml -pl common,inventory-service -am test`.
* **Guardrail:** The new repository query must be supported by the Cosmos container's indexing policy; an unindexed predicate would increase request-unit consumption. `UNC-002` records that the indexing policy is provisioned outside the application, and `OQ-27` records that the predicate's request-unit impact is unconfirmed.

<span style="font-size: 14px;">**MSFT Reference:** [Reliability design principles — Azure Well-Architected Framework](https://learn.microsoft.com/azure/well-architected/reliability/principles)</span>

---

#### Supply Chain

#### P1-013: Container base images are referenced by mutable tag

**Priority: P1 - High Priority**

**Priority policy:** `AA-REMEDIATION-PRIORITY` v1.0.0, rule `P1-SUP-002` · **Change ID:** `CHANGE-AA-024` (Wave 1) · **Source ID:** F-031 · **Primary control:** `APP-SUPPLY-002`

**Severity:** High

**Resiliency Related:** Yes

**Finding status:** Verified finding

**Issue:** Both the build stage and the runtime stage reference base images by tag with no `sha256` digest pin, in every service Dockerfile.

**What does this solve:** It restores the single-immutable-artifact assumption so two regions rebuilt at different times run identical JVM and OS layers from the same commit.

**Resiliency Impact:** Two regions rebuilt or repulled at different times can run materially different JVM or OS layers from the same source commit, which breaks the single-immutable-artifact assumption that active-active operation depends on and introduces a source of behavioral divergence that is invisible in source control. The affected set includes `payment-service`, which performs financial and payment processing, so rule `P1-SUP-002` applies rather than `P2-SUP-001`.

**Recommended Fix:** Carry a `sha256` digest on every `FROM` directive, supplied through a build argument that the pipeline resolves, and add a build-time assertion that fails when a digest is missing.

**File:** source/customer-app/order-service/Dockerfile:1

```dockerfile
// before
FROM maven:3.9.6-eclipse-temurin-17 AS builder
```

**File:** source/customer-app/order-service/Dockerfile:18

```dockerfile
// before
FROM eclipse-temurin:17-jre-jammy
```

**Fix:**

> Illustrative proposal only.

`source/customer-app/order-service/Dockerfile` — `FROM` directives

```dockerfile
# Digests are resolved by the pipeline and supplied as build arguments so the same commit
# produces identical layers in every region. Replace the placeholder values with the
# digests recorded by the approved base-image refresh process.
ARG BUILDER_IMAGE_DIGEST=sha256:REPLACE_WITH_RESOLVED_BUILDER_DIGEST
ARG RUNTIME_IMAGE_DIGEST=sha256:REPLACE_WITH_RESOLVED_RUNTIME_DIGEST

FROM maven:3.9.6-eclipse-temurin-17@${BUILDER_IMAGE_DIGEST} AS builder

# ... build stage unchanged ...

FROM eclipse-temurin:17-jre-jammy@${RUNTIME_IMAGE_DIGEST}
```

Both `FROM` directives carry an immutable digest while retaining the human-readable tag for legibility. The digests arrive as build arguments so refreshing a base image is a pipeline input change governed by the base-image refresh process rather than a source edit. The placeholder values are deliberate: **no digest is invented here** (`OQ-28`).

`source/customer-app/common/src/test/java/com/ecommerce/common/supplychain/DockerfileDigestPinningTest.java`

```java
package com.ecommerce.common.supplychain;

import static org.assertj.core.api.Assertions.assertThat;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.List;
import java.util.stream.Stream;
import org.junit.jupiter.api.Test;

class DockerfileDigestPinningTest {

    @Test
    void everyFromDirectiveIsPinnedByDigest() throws IOException {
        try (Stream<Path> dockerfiles = Files.walk(Path.of(".."))) {
            List<Path> files = dockerfiles
                    .filter(p -> p.getFileName().toString().equals("Dockerfile"))
                    .toList();

            assertThat(files).isNotEmpty();

            for (Path dockerfile : files) {
                for (String line : Files.readAllLines(dockerfile)) {
                    if (line.trim().startsWith("FROM ")) {
                        assertThat(line)
                                .as("unpinned base image in %s: %s", dockerfile, line)
                                .contains("@sha256:");
                    }
                }
            }
        }
    }
}
```

A build assertion that every `FROM` directive carries a digest, which prevents an unpinned image from being reintroduced.

**Notes:**

* **Cross-refs:** Depends on **P0-012**. Edits the same Dockerfiles as **P0-012** and **P0-003**; sequence them together.
* **Implementation:** `CHANGE-AA-024`, Wave 1, complexity low. Both targets carry generated code. Affects all eight Dockerfiles.
* **Validation:** T-AA-024-01 (every `FROM` directive carries a digest), T-AA-024-02 (the resolved digest is identical across regional pipeline runs of the same commit). `mvn -f source/customer-app/pom.xml -pl common -am -Dtest=DockerfileDigestPinningTest test`.
* **Guardrail:** Pinned digests must be refreshed deliberately or security patches will not be picked up; a refresh cadence is required (`OQ-28`).

<span style="font-size: 14px;">**MSFT Reference:** [Recommendations for image tagging and versioning](https://learn.microsoft.com/azure/container-registry/container-registry-image-tag-version)</span>

---
### P2 Moderate Priority

#### Message Identity and Replay

#### P2-001: Published events carry no stable identity and consumers perform no deduplication

**Priority: P2 - Moderate Priority**

**Priority policy:** `AA-REMEDIATION-PRIORITY` v1.0.0, rule `P2-DATA-002` · **Change ID:** `CHANGE-AA-025` (Wave 3) · **Source ID:** F-010 · **Primary control:** `KAFKA-003`

**Severity:** Critical

**Resiliency Related:** Yes

**Finding status:** Verified finding

**Issue:** Producers publish plain `HashMap` payloads that contain no event identifier and a timestamp regenerated at publish time. The shared `BaseEvent` class declares an `eventId`, but its constructor never assigns `correlationId` or `tenantId` and no producer in the repository uses it. No consumer performs a deduplication lookup, and the notification consumer dispatches SMTP email per consumed record with no message id, no idempotency key, and no already-sent check.

**What does this solve:** It supplies the identity that consumer deduplication, the transactional outbox, and the durable notification store all require, so replay, rebalance, offset restoration, and promotion stop producing duplicate effects.

**Resiliency Impact:** Any replay, rebalance, offset restoration, or controlled promotion produces duplicate customer emails and duplicate downstream effects with no way to detect or suppress them. Under `active_standby`, offset restoration after a promotion re-executes every side effect.

**Recommended Fix:** Stamp `eventId`, `eventType`, `correlationId`, `sourceService`, and an offset-bearing `occurredAt` onto every published event through a shared factory, publish the identity as a record header as well as a payload field, and assign `correlationId` and `tenantId` in the `BaseEvent` constructor.

**Priority note:** Elevation to `P0-AA-006` was **evaluated and declined**. The identified non-idempotent external effect is customer email rather than a financial or stock-committing transaction; the financially material duplicate risks are carried by **P0-005** and **P0-006**, which were elevated.

**File:** source/customer-app/common/src/main/java/com/ecommerce/common/events/BaseEvent.java:16-33

```java
// before
public abstract class BaseEvent {

    private String eventId;
    private String eventType;
    private String correlationId;
    private String sourceService;
    private LocalDateTime occurredAt;
    private int version;
    private String tenantId;

    public BaseEvent(String eventType, String sourceService) {
        this.eventId = UUID.randomUUID().toString();
        this.eventType = eventType;
        this.sourceService = sourceService;
        this.occurredAt = LocalDateTime.now();
        this.version = 1;
    }
}
```

**File:** source/customer-app/order-service/src/main/java/com/ecommerce/order/service/OrderService.java:368-384 — `publishOrderEvent`

> The exact excerpt is rendered under **P0-008**; the untyped map payload carries no `eventId` and regenerates its timestamp at publish time.

**Fix:**

> Illustrative proposal only.

`source/customer-app/common/src/main/java/com/ecommerce/common/events/BaseEvent.java` — constructor

```java
public BaseEvent(String eventType, String sourceService, String correlationId, String tenantId) {
    this.eventId = UUID.randomUUID().toString();
    this.eventType = eventType;
    this.sourceService = sourceService;
    this.correlationId = correlationId;
    this.tenantId = tenantId;
    this.occurredAt = OffsetDateTime.now(ZoneOffset.UTC);
    this.version = 1;
}
```

Assigns the two fields the current constructor silently leaves null, and replaces the zone-less `LocalDateTime occurredAt` with an offset-bearing timestamp so events produced in two regions are comparable. The field set is otherwise unchanged.

`source/customer-app/common/src/main/java/com/ecommerce/common/events/DomainEventFactory.java`

```java
package com.ecommerce.common.events;

import java.time.OffsetDateTime;
import java.time.ZoneOffset;
import java.util.LinkedHashMap;
import java.util.Map;
import java.util.UUID;

/** Stamps a stable identity onto every published event, including the existing map payloads. */
public final class DomainEventFactory {

    public static final String HEADER_EVENT_ID = "x-event-id";
    public static final String HEADER_CORRELATION_ID = "x-correlation-id";
    public static final String HEADER_SOURCE_SERVICE = "x-source-service";

    private final String sourceService;

    public DomainEventFactory(String sourceService) {
        this.sourceService = sourceService;
    }

    public Map<String, Object> envelope(String eventType,
                                        String correlationId,
                                        Map<String, Object> body) {
        Map<String, Object> event = new LinkedHashMap<>();
        event.put("eventId", UUID.randomUUID().toString());
        event.put("eventType", eventType);
        event.put("correlationId", correlationId);
        event.put("sourceService", sourceService);
        event.put("occurredAt", OffsetDateTime.now(ZoneOffset.UTC).toString());
        event.put("version", 1);
        event.putAll(body);
        return event;
    }

    public Map<String, byte[]> headers(Map<String, Object> event) {
        return Map.of(
                HEADER_EVENT_ID, String.valueOf(event.get("eventId")).getBytes(),
                HEADER_CORRELATION_ID, String.valueOf(event.get("correlationId")).getBytes(),
                HEADER_SOURCE_SERVICE, String.valueOf(event.get("sourceService")).getBytes());
    }
}
```

Adds identity to the existing map-based payloads without forcing a migration to `BaseEvent` subclasses, so every producer can adopt it incrementally. Identity is exposed as record headers as well as payload fields so a consumer can deduplicate before deserialising the body. Existing payload keys are preserved, so current consumers keep working.

**Notes:**

* **Cross-refs:** **Hard prerequisite** for **P0-007** (the outbox makes delivery at-least-once, which is unsafe without deduplication — risk `R-03`), **P0-004**, and **P2-002**. Carries the correlation identity introduced by **P3-002**. Depends on **P0-012**. Leads Wave 3.
* **Implementation:** `CHANGE-AA-025`, Wave 3, complexity medium. All three targets carry generated code.
* **Validation:** T-AA-025-01 (every event carries a stable `eventId` and `correlationId` in payload and headers), T-AA-025-02 (the same record delivered twice yields exactly one email dispatch and one notification record). `mvn -f source/customer-app/pom.xml -pl common,order-service,notification-service -am test`.
* **Guardrail:** Sixteen derived event classes exist in `common`; changing the `BaseEvent` constructor signature requires updating each subclass (`OQ-29`). Changing `occurredAt` from `LocalDateTime` to `OffsetDateTime` is a serialization change consumers must tolerate; the trusted-packages and type-header settings in the consumers should be reviewed.

<span style="font-size: 14px;">**MSFT Reference:** [Idempotent message processing — Azure messaging guidance](https://learn.microsoft.com/azure/architecture/serverless/event-hubs-functions/resilient-design)</span>

---

#### Consumer Correctness

#### P2-002: Manual acknowledgment is configured but never performed

**Priority: P2 - Moderate Priority**

**Priority policy:** `AA-REMEDIATION-PRIORITY` v1.0.0, rule `P2-DATA-002` · **Change ID:** `CHANGE-AA-026` (Wave 3) · **Source ID:** F-009 · **Primary control:** `APP-KAFKA-002`

**Severity:** Critical

**Resiliency Related:** Yes

**Finding status:** Verified finding

**Issue:** `notification-service` declares `ack-mode: MANUAL_IMMEDIATE`, yet no listener method declares an `Acknowledgment` parameter. Every listener is additionally annotated `@Async`, so the container method returns before the email dispatch and the notification write complete.

**What does this solve:** It makes the offset commit a consequence of completed processing, so a pod termination, rebalance, or regional role transition redelivers work that was not completed instead of silently losing it.

**Resiliency Impact:** Offsets advance for work that has not been performed. A pod termination, rebalance, or regional role transition loses every in-flight notification with no record and no replay path. Offset position is therefore not a truthful record of completed work, which is a precondition for interpreting an active-standby promotion.

**Recommended Fix:** Remove `@Async` from the listeners, declare an `Acknowledgment` parameter, and acknowledge only after the durable claim and the dispatch succeed. Let failures propagate to the container so the error and dead-letter contract applies.

**Priority note:** Elevation was **evaluated and declined**. Offsets advancing ahead of notification dispatch loses or duplicates email only. No authoritative store is mutated by the notification consumer once **P0-004** replaces the pod-local store.

**File:** source/customer-app/notification-service/src/main/resources/application.yml:22-24

```yaml
// before
      listener:
        concurrency: 3
        ack-mode: MANUAL_IMMEDIATE
```

**File:** source/customer-app/notification-service/src/main/java/com/ecommerce/notification/service/NotificationEventConsumer.java:53-64

```java
// before
    @KafkaListener(topics = KafkaTopics.ORDER_CONFIRMED, groupId = KafkaTopics.GROUP_NOTIFICATION_SERVICE)
    @Async
    public void handleOrderConfirmed(Map<String, Object> event) {
        String customerEmail = (String) event.get("customerEmail");
        String orderNumber = (String) event.get("orderNumber");
        log.info("Sending order confirmed notification for order: {}", orderNumber);
        try {
            emailService.sendOrderConfirmed(customerEmail, orderNumber);
        } catch (Exception e) {
            log.error("Failed to send order confirmed notification: {}", e.getMessage());
        }
    }
```

**Fix:**

> Illustrative proposal only.

`source/customer-app/notification-service/src/main/java/com/ecommerce/notification/service/NotificationEventConsumer.java` — `handleOrderConfirmed`

```java
@KafkaListener(
        id = "notification-order-confirmed",
        topics = KafkaTopics.ORDER_CONFIRMED,
        groupId = KafkaTopics.GROUP_NOTIFICATION_SERVICE,
        autoStartup = "false")
public void handleOrderConfirmed(Map<String, Object> event, Acknowledgment acknowledgment) {
    String eventId = (String) event.get("eventId");
    String customerEmail = (String) event.get("customerEmail");
    String orderNumber = (String) event.get("orderNumber");

    String notificationId = notificationId(eventId, "ORDER_CONFIRMED", "EMAIL");
    if (!notificationStore.saveIfAbsent(record(notificationId, eventId, event))) {
        log.info("Notification {} already recorded; acknowledging without resend", notificationId);
        acknowledgment.acknowledge();
        return;
    }

    // No @Async: the side effect completes on the container thread before the offset moves.
    emailService.sendOrderConfirmed(customerEmail, orderNumber);

    acknowledgment.acknowledge();
}
```

`@Async` is removed so the container thread owns the work, the `Acknowledgment` parameter makes the declared `MANUAL_IMMEDIATE` ack mode effective for the first time, and acknowledgement happens only after the durable claim and the dispatch succeed. The log-and-swallow catch is removed so an exception reaches the container and the **P2-003** error handler applies. `autoStartup = "false"` comes from **P0-009**.

`source/customer-app/notification-service/src/main/resources/application.yml` — `spring.kafka.listener`

```yaml
spring:
  kafka:
    listener:
      concurrency: ${KAFKA_LISTENER_CONCURRENCY:3}
      ack-mode: MANUAL_IMMEDIATE
      missing-topics-fatal: false
      immediate-stop: false
```

The ack mode is unchanged because it was already correct; what changes is that the listener methods now honour it. `immediate-stop: false` lets a stopping container finish the record it already handed to the listener, which pairs with the **P0-011** drain.

**Notes:**

* **Cross-refs:** Depends on **P0-004** (durable store), **P2-001** (`eventId` used to build the notification identity), and **P0-012**. Prerequisite for **P2-003** (the error handler is inert while listeners swallow exceptions) and influences **P1-009**.
* **Implementation:** `CHANGE-AA-026`, Wave 3, complexity medium. All three targets carry generated code.
* **Validation:** T-AA-026-01 (offset acknowledged only after the side effect and durable write complete), T-AA-026-02 (mid-dispatch termination causes redelivery). `mvn -f source/customer-app/pom.xml -pl common,notification-service -am test`.
* **Guardrail:** Removing `@Async` makes dispatch synchronous on the container thread, which reduces throughput. Listener concurrency and SMTP timeouts must be reviewed together (`OQ-30`).

<span style="font-size: 14px;">**MSFT Reference:** [Resilient event-driven design](https://learn.microsoft.com/azure/architecture/serverless/event-hubs-functions/resilient-design)</span>

---

#### P2-003: Consumers have no error handler, retry limit, or dead-letter routing

**Priority: P2 - Moderate Priority**

**Priority policy:** `AA-REMEDIATION-PRIORITY` v1.0.0, rule `P2-DATA-002` · **Change ID:** `CHANGE-AA-027` (Wave 3) · **Source ID:** F-008 · **Primary control:** `APP-KAFKA-003`

**Severity:** Critical

**Resiliency Related:** Yes

**Finding status:** Verified finding

**Issue:** No service configures a `DefaultErrorHandler`, `DeadLetterPublishingRecoverer`, `@RetryableTopic`, `@DltHandler`, or backoff policy. Four DLQ topic constants are declared in the shared module and referenced nowhere. Every notification listener catches `Exception` and logs, so no exception ever reaches the listener container.

**What does this solve:** It converts silent discard into quarantine plus replay, and makes a blocked partition visible.

**Resiliency Impact:** A poison record or a sustained downstream failure is silently discarded rather than quarantined. Nothing can be replayed after recovery and no partition ever signals a blocked condition. A poison record produced before a promotion silently drains the promoted region's processing.

**Recommended Fix:** Configure a `DefaultErrorHandler` with exponential backoff bounded by both a maximum interval and a maximum elapsed time, route exhausted records to the already-declared DLQ topic through a `DeadLetterPublishingRecoverer`, classify deserialization failures as immediately non-retryable, and increment a dead-letter metric.

**Priority note:** Elevation was **evaluated and declined**. The gap causes silent discard of failed records rather than duplicate execution of a critical transaction.

**File:** source/customer-app/notification-service/src/main/resources/application.yml:8-24

```yaml
// before
    kafka:
      bootstrap-servers: ${KAFKA_BOOTSTRAP_SERVERS:ecommerce-kafka.westus.azure.com:9093}
      consumer:
        group-id: notification-service-group
        auto-offset-reset: earliest
        key-deserializer: org.apache.kafka.common.serialization.StringDeserializer
        value-deserializer: org.springframework.kafka.support.serializer.JsonDeserializer
        max-poll-records: 10
        properties:
          spring.json.trusted.packages: "com.ecommerce.*,java.util"
          spring.json.use.type.headers: false
          security.protocol: SASL_SSL
          sasl.mechanism: PLAIN
          sasl.jaas.config: "org.apache.kafka.common.security.plain.PlainLoginModule required username='${KAFKA_USERNAME}' password='${KAFKA_PASSWORD}';"
      listener:
        concurrency: 3
        ack-mode: MANUAL_IMMEDIATE
```

**File:** source/customer-app/notification-service/src/main/java/com/ecommerce/notification/service/NotificationEventConsumer.java:34-51

```java
// before
    @KafkaListener(topics = KafkaTopics.ORDER_CREATED, groupId = KafkaTopics.GROUP_NOTIFICATION_SERVICE)
    @Async
    public void handleOrderCreated(Map<String, Object> event) {
        String customerId = (String) event.get("customerId");
        String customerEmail = (String) event.get("customerEmail");
        String orderNumber = (String) event.get("orderNumber");
        Object total = event.get("totalAmount");

        log.info("Sending order confirmation notification for order: {}", orderNumber);

        try {
            emailService.sendOrderConfirmation(customerEmail, orderNumber, total.toString());
            saveNotification(customerId, "ORDER_CREATED", "Order Confirmation",
                    "Your order " + orderNumber + " has been placed successfully.", "EMAIL");
        } catch (Exception e) {
            log.error("Failed to send order confirmation email: {}", e.getMessage());
        }
    }
```

**Fix:**

> Illustrative proposal only.

`source/customer-app/notification-service/src/main/java/com/ecommerce/notification/config/KafkaErrorHandlingConfig.java`

```java
package com.ecommerce.notification.config;

import io.micrometer.core.instrument.MeterRegistry;
import org.apache.kafka.common.TopicPartition;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.kafka.core.KafkaOperations;
import org.springframework.kafka.listener.DeadLetterPublishingRecoverer;
import org.springframework.kafka.listener.DefaultErrorHandler;
import org.springframework.kafka.support.serializer.DeserializationException;
import org.springframework.util.backoff.ExponentialBackOff;

@Configuration
public class KafkaErrorHandlingConfig {

    @Bean
    public DefaultErrorHandler kafkaErrorHandler(
            KafkaOperations<String, Object> kafkaOperations,
            MeterRegistry meterRegistry,
            @Value("${app.kafka.error.initial-backoff-ms:500}") long initialBackoffMs,
            @Value("${app.kafka.error.max-backoff-ms:10000}") long maxBackoffMs,
            @Value("${app.kafka.error.max-elapsed-ms:60000}") long maxElapsedMs) {

        DeadLetterPublishingRecoverer recoverer = new DeadLetterPublishingRecoverer(
                kafkaOperations,
                (record, exception) -> {
                    meterRegistry.counter("kafka.records.dead_lettered",
                            "topic", record.topic(),
                            "reason", exception.getClass().getSimpleName()).increment();
                    return new TopicPartition(KafkaTopics.DLQ_NOTIFICATION, record.partition());
                });

        ExponentialBackOff backOff = new ExponentialBackOff(initialBackoffMs, 2.0);
        backOff.setMaxInterval(maxBackoffMs);
        backOff.setMaxElapsedTime(maxElapsedMs);

        DefaultErrorHandler errorHandler = new DefaultErrorHandler(recoverer, backOff);
        // A record that cannot be deserialised will never succeed; quarantine it immediately.
        errorHandler.addNotRetryableExceptions(DeserializationException.class);
        return errorHandler;
    }
}
```

Gives the four declared but unreferenced DLQ constants a purpose. Retries are bounded by both a maximum interval and a maximum elapsed time so a sustained downstream failure cannot retry indefinitely, an undeserialisable record is quarantined on the first attempt rather than retried pointlessly, and each dead-letter event increments a metric an alert can evaluate. The partition is preserved so ordering within a key is retained in the DLQ. Retry and backoff values are proposals and remain externally configurable.

`source/customer-app/notification-service/src/main/resources/application.yml` — `app.kafka.error`

```yaml
app:
  kafka:
    error:
      initial-backoff-ms: ${KAFKA_ERROR_INITIAL_BACKOFF_MS:500}
      max-backoff-ms: ${KAFKA_ERROR_MAX_BACKOFF_MS:10000}
      max-elapsed-ms: ${KAFKA_ERROR_MAX_ELAPSED_MS:60000}
```

The retry budget becomes an externally tunable deployment input rather than a compiled constant, so it can be aligned with the ownership transition window.

**Notes:**

* **Cross-refs:** Depends on **P2-002** (removing the log-only catches, otherwise the error handler never sees an exception) and **P0-012**. Contributes a counter that must follow the **P3-003** naming convention.
* **Implementation:** `CHANGE-AA-027`, Wave 3, complexity medium. All three targets carry generated code. Applies to `notification-service` and `inventory-service`.
* **Validation:** T-AA-027-01 (finite attempt count and routing to the declared DLQ topic), T-AA-027-02 (undeserialisable record quarantined without retry; partition continues to progress). `mvn -f source/customer-app/pom.xml -pl common,notification-service,inventory-service -am test`.
* **Guardrail:** Dead-lettered records require an operational replay procedure; without one the DLQ becomes a silent graveyard. `OQ-31` records that DLQ ownership and retention are undecided. `OQ-19` gates the numeric backoff values.

<span style="font-size: 14px;">**MSFT Reference:** [Dead Letter Channel and poison message handling](https://learn.microsoft.com/azure/service-bus-messaging/service-bus-dead-letter-queues)</span>

---

#### Business Identity

#### P2-004: Order business identifier is generated per attempt with no region discriminator

**Priority: P2 - Moderate Priority**

**Priority policy:** `AA-REMEDIATION-PRIORITY` v1.0.0, rule `P2-DATA-001` · **Change ID:** `CHANGE-AA-028` (Wave 4) · **Source ID:** F-013 · **Primary control:** `APP-AA-011`

**Severity:** High

**Resiliency Related:** Yes

**Finding status:** Verified finding

**Issue:** `generateOrderNumber` concatenates a truncated millisecond timestamp with a four-digit `Math.random` value. Uniqueness relies solely on a database constraint. There is no region or node discriminator and no collision retry, and the mutating API accepts no client idempotency key.

**What does this solve:** It makes order creation idempotent under retry and removes the cross-region collision surface.

**Resiliency Impact:** Two regions writing to independent or promoted databases can mint colliding order numbers, and a retried order creation produces a different business identifier for the same customer intent.

**Recommended Fix:** Accept a client idempotency key on the create-order API, return the existing order when the key has already been used, and generate the order number from a collision-resistant source with a deployment-supplied node discriminator and a bounded collision retry.

**Priority note:** Elevation was **evaluated and declined**. Order-number collision is currently contained by the single authoritative Azure SQL database under the inferred `active_standby` scenario, and a duplicate order is commercially reversible. **Elevation must be revisited if `EXT-003` confirms independent regional order databases.**

**File:** source/customer-app/order-service/src/main/java/com/ecommerce/order/service/OrderService.java:315-319

```java
// before
    private String generateOrderNumber() {
        String timestamp = String.valueOf(System.currentTimeMillis()).substring(4);
        String random = String.format("%04d", (int)(Math.random() * 9999));
        return "ORD-" + timestamp + "-" + random;
    }
```

**Fix:**

> Illustrative proposal only.

`source/customer-app/order-service/src/main/java/com/ecommerce/order/service/OrderService.java` — `generateOrderNumber` and `createOrder`

```java
@Value("${app.order.number-prefix:ORD}")
private String orderNumberPrefix;

/** Deployment-supplied, never compiled. Distinguishes concurrently minting deployments. */
@Value("${app.order.node-discriminator}")
private String nodeDiscriminator;

@Value("${app.order.max-collision-retries:3}")
private int maxCollisionRetries;

public OrderResponse createOrder(CreateOrderRequest request, String idempotencyKey) {
    Optional<OrderEntity> existing = orderRepository.findByIdempotencyKey(idempotencyKey);
    if (existing.isPresent()) {
        // Same customer intent; return the same order and the same order number.
        return toResponse(existing.get());
    }

    for (int attempt = 0; attempt <= maxCollisionRetries; attempt++) {
        try {
            OrderEntity order = buildOrder(request, idempotencyKey, generateOrderNumber());
            return toResponse(orderRepository.saveAndFlush(order));
        } catch (DataIntegrityViolationException collision) {
            Optional<OrderEntity> byKey = orderRepository.findByIdempotencyKey(idempotencyKey);
            if (byKey.isPresent()) {
                return toResponse(byKey.get());
            }
            log.warn("Order number collision on attempt {} of {}", attempt + 1, maxCollisionRetries + 1);
        }
    }
    throw new BusinessException("Unable to allocate a unique order number after "
            + (maxCollisionRetries + 1) + " attempts");
}

private String generateOrderNumber() {
    String timeComponent = Long.toString(Instant.now().toEpochMilli(), 36).toUpperCase();
    String entropy = Long.toString(
            ThreadLocalRandom.current().nextLong(Long.MAX_VALUE), 36).toUpperCase();
    return orderNumberPrefix + "-" + nodeDiscriminator + "-" + timeComponent + "-" + entropy;
}
```

The client idempotency key makes a retried create resolve to the existing order and the same order number. The order number gains a deployment-supplied discriminator so two independently minting deployments cannot collide, and the four-digit `Math.random` component is replaced by a much larger entropy value from `ThreadLocalRandom`. A collision is retried within a bounded budget instead of failing the request. No region name is compiled; the discriminator is an opaque deployment input.

**Notes:**

* **Cross-refs:** Depends on **P0-006** (the same key should be propagated to the payment API) and **P0-012**. Shares decision gate `order_schema_migration` (`OQ-12`, `UNC-008`) with **P0-007**. The order-number prefix property is also owned by **P3-004** and must resolve to a single definition.
* **Implementation:** `CHANGE-AA-028`, Wave 4, complexity medium. Both targets carry generated code.
* **Validation:** T-AA-028-01 (retried create with the same key returns the same order number and creates one order), T-AA-028-02 (collision resolved deterministically within a bounded retry budget). `mvn -f source/customer-app/pom.xml -pl common,order-service -am test`.
* **Guardrail:** Changing the order-number format affects any downstream system that parses it; length and character set must be reviewed (`OQ-32`). An `idempotency_key` column and unique constraint must be added to the orders schema, which shares the unresolved migration mechanism recorded for **P0-007**.

<span style="font-size: 14px;">**MSFT Reference:** [Deployment Stamps pattern](https://learn.microsoft.com/azure/architecture/patterns/deployment-stamp)</span>

---

#### Degraded-Mode Correctness

#### P2-005: Redis rate limiting fails open silently and its two-step counter is not atomic

**Priority: P2 - Moderate Priority**

**Priority policy:** `AA-REMEDIATION-PRIORITY` v1.0.0, rule `P2-DATA-005` · **Change ID:** `CHANGE-AA-029` (Wave 4) · **Source ID:** F-023 · **Primary control:** `REDIS-020`

**Severity:** High

**Resiliency Related:** Yes

**Finding status:** Verified finding

**Issue:** The rate-limit chain increments a counter and, only when the counter equals one, issues a separate `expire` call. Any Redis error in the chain is absorbed by `onErrorResume`, which logs and forwards the request. No metric distinguishes a Redis failure from a normal pass, and rate-limit state has no defined regional consistency semantics.

**What does this solve:** It removes the permanently wedged counter and makes the loss of rate limiting during regional stress a visible, alertable, deliberate decision.

**Resiliency Impact:** A Redis outage silently removes all rate limiting during exactly the period when the region is most likely to be under stress, and a failed `expire` call leaves a counter that never resets, permanently blocking a client key. The code relies on a consistency guarantee that the approved application behavior does not establish.

**Recommended Fix:** Collapse the increment and expiry into a single server-side atomic script, and make the dependency-failure policy an explicitly configured fail-open or fail-closed decision that emits a distinct degraded-mode metric and marks the response.

**File:** source/customer-app/api-gateway/src/main/java/com/ecommerce/gateway/filter/RateLimitFilter.java:44-68

```java
// before
            return redisTemplate.opsForValue()
                    .increment(rateLimitKey)
                    .flatMap(count -> {
                        if (count == 1) {
                            return redisTemplate.expire(rateLimitKey, WINDOW_DURATION)
                                    .then(Mono.just(count));
                        }
                        return Mono.just(count);
                    })
                    .flatMap(count -> {
                        exchange.getResponse().getHeaders().add("X-RateLimit-Limit", String.valueOf(limit));
                        exchange.getResponse().getHeaders().add("X-RateLimit-Remaining", 
                                String.valueOf(Math.max(0, limit - count)));

                        if (count > limit) {
                            log.warn("Rate limit exceeded for IP: {} on path: {}", clientIp, path);
                            return handleRateLimitExceeded(exchange);
                        }
                        return chain.filter(exchange);
                    })
                    .onErrorResume(e -> {
                        log.error("Redis error in rate limiting, allowing request: {}", e.getMessage());
                        return chain.filter(exchange);
                    });
        }
```

**Fix:**

> Illustrative proposal only.

`source/customer-app/api-gateway/src/main/resources/scripts/rate-limit.lua`

```text
-- KEYS[1] = rate limit key, ARGV[1] = window seconds
-- Increments and applies the expiry atomically so a failure cannot leave a
-- permanently non-expiring counter.
local count = redis.call('INCR', KEYS[1])
if count == 1 then
  redis.call('EXPIRE', KEYS[1], ARGV[1])
end
return count
```

Collapses the two round trips into one server-side atomic operation, which removes the window in which a failed `EXPIRE` leaves a counter that never resets.

`source/customer-app/api-gateway/src/main/java/com/ecommerce/gateway/filter/RateLimitFilter.java` — `filter`

```java
private static final String HEADER_RATE_LIMIT_DEGRADED = "X-RateLimit-Degraded";

@Value("${app.rate-limit.fail-open:true}")
private boolean failOpen;

return redisTemplate
        .execute(rateLimitScript, List.of(rateLimitKey), List.of(String.valueOf(WINDOW_DURATION.toSeconds())))
        .single()
        .flatMap(count -> {
            exchange.getResponse().getHeaders().add("X-RateLimit-Limit", String.valueOf(limit));
            exchange.getResponse().getHeaders().add("X-RateLimit-Remaining",
                    String.valueOf(Math.max(0, limit - count)));

            if (count > limit) {
                log.warn("Rate limit exceeded for IP: {} on path: {}", clientIp, path);
                return handleRateLimitExceeded(exchange);
            }
            return chain.filter(exchange);
        })
        .onErrorResume(e -> {
            // Explicit, configured, observable policy rather than a silent pass-through.
            meterRegistry.counter("gateway.rate_limit.degraded",
                    "policy", failOpen ? "fail_open" : "fail_closed",
                    "reason", e.getClass().getSimpleName()).increment();
            log.error("Redis unavailable for rate limiting; applying {} policy",
                    failOpen ? "fail-open" : "fail-closed", e);

            exchange.getResponse().getHeaders().add(HEADER_RATE_LIMIT_DEGRADED, "true");
            return failOpen ? chain.filter(exchange) : handleRateLimitUnavailable(exchange);
        });
```

The two-step chain becomes a single atomic script execution. The error path keeps the previous default behavior but makes it a configured decision, increments a metric that distinguishes a Redis failure from a normal pass, and marks the response so the degraded decision is visible downstream. The rate-limit key naming and the existing headers are unchanged.

**Notes:**

* **Cross-refs:** Depends on **P1-001** (the Redis command timeout must actually be in effect) and **P0-012**. Contributes a counter that must follow the **P3-003** naming convention.
* **Implementation:** `CHANGE-AA-029`, Wave 4, complexity medium. All three targets carry generated code.
* **Validation:** T-AA-029-01 (the counter always carries an expiry), T-AA-029-02 (a distinct degraded-mode metric and an explicit configured failure policy). `mvn -f source/customer-app/pom.xml -pl common,api-gateway -am test`.
* **Guardrail:** Choosing fail-closed makes Redis a hard dependency of the gateway request path and must be reflected in the **P0-003** readiness decision. `OQ-33` records that the fail-open versus fail-closed decision, and whether it differs per region, is undecided.

<span style="font-size: 14px;">**MSFT Reference:** [Rate Limiting pattern](https://learn.microsoft.com/azure/architecture/patterns/rate-limiting-pattern)</span>

---

### P3 Optimization

#### Regional Observability

#### P3-001: Telemetry cannot identify the serving region

**Priority: P3 - Optimization**

**Priority policy:** `AA-REMEDIATION-PRIORITY` v1.0.0, rule `P3-OPS-001` · **Change ID:** `CHANGE-AA-030` (Wave 4) · **Source ID:** F-025 · **Primary control:** `APP-AA-015`

**Severity:** Medium

**Resiliency Related:** Yes

**Finding status:** Verified finding

**Issue:** Four services declare a static `region: westus` Micrometer tag — `api-gateway`, `user`, `product`, and `notification`. The remaining four services declare no region tag at all. No zone tag, cluster tag, or instance tag exists in any service, and no custom meters are registered.

**What does this solve:** It lets operators determine which region is serving, degraded, or draining, and attribute dependency latency and failure to a region.

**Impact:** Metrics from both regions are either indistinguishable or falsely attributed to one region. Operators cannot determine which region is serving, degraded, or draining, and cannot attribute dependency latency or failure to a region. This is a legibility gap rather than a runtime-behavior defect, which is why no P0, P1, or P2 rule applies; the region literals themselves are remediated at P0 by **P0-001**.

**Recommended Fix:** Replace the static region tag with a resolved deployment placeholder, add zone and instance tags, and apply attribution centrally through a shared `MeterRegistryCustomizer` so the four services with no tags are covered without editing each one.

**File:** source/customer-app/api-gateway/src/main/resources/application.yml:134-137

```yaml
// before
      tags:
        application: api-gateway
        region: westus
        environment: ${ENVIRONMENT:production}
```

**File:** source/customer-app/notification-service/src/main/resources/application.yml:61-64

```yaml
// before
    metrics:
      tags:
        application: notification-service
        region: westus
```

**Fix:**

> Illustrative proposal only.

`source/customer-app/api-gateway/src/main/resources/application.yml` — `management.metrics.tags`

```yaml
management:
  metrics:
    tags:
      application: api-gateway
      region: ${APP_DEPLOYMENT_REGION}
      zone: ${APP_DEPLOYMENT_ZONE:unknown}
      instance: ${HOSTNAME:unknown}
      environment: ${ENVIRONMENT}
```

The static region literal becomes a required deployment input, and the missing zone and instance dimensions are added. `HOSTNAME` is already supplied by the container runtime, so no new deployment input is required for instance attribution.

`source/customer-app/common/src/main/java/com/ecommerce/common/observability/RegionalTagCustomizer.java`

```java
package com.ecommerce.common.observability;

import io.micrometer.core.instrument.MeterRegistry;
import io.micrometer.core.instrument.config.MeterFilter;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.boot.actuate.autoconfigure.metrics.MeterRegistryCustomizer;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

/** Guarantees regional attribution even in services that declare no metrics tags. */
@Configuration
public class RegionalTagCustomizer {

    @Bean
    public MeterRegistryCustomizer<MeterRegistry> regionalTags(
            @Value("${spring.application.name:unknown}") String application,
            @Value("${app.deployment.region}") String region,
            @Value("${app.deployment.zone:unknown}") String zone,
            @Value("${HOSTNAME:unknown}") String instance) {

        return registry -> registry.config().meterFilter(
                MeterFilter.commonTags(io.micrometer.core.instrument.Tags.of(
                        "application", application,
                        "region", region,
                        "zone", zone,
                        "instance", instance)));
    }
}
```

Applies attribution centrally so the four services with no tags at all are covered without editing each one, and so a future service inherits it automatically. The region value is a required property with no default, so a deployment that fails to supply it fails startup rather than emitting unattributed metrics.

**Notes:**

* **Cross-refs:** Depends on **P0-001** and **P0-012**.
* **Implementation:** `CHANGE-AA-030`, Wave 4, complexity low. All three targets carry generated code.
* **Validation:** T-AA-030-01 (every service emits a region tag resolved from the environment and a region-B profile produces a different value). `mvn -f source/customer-app/pom.xml -pl common,api-gateway,notification-service -am test`.
* **Guardrail:** Adding an instance tag increases metric cardinality and should be scoped to the meters that need it if cardinality becomes a cost concern (`OQ-34`). Existing dashboards filtering on `region=westus` will need updating.

<span style="font-size: 14px;">**MSFT Reference:** [Observability — Azure Well-Architected Framework](https://learn.microsoft.com/azure/well-architected/operational-excellence/observability)</span>

---

#### P3-002: Correlation identity is regenerated per hop and never propagated

**Priority: P3 - Optimization**

**Priority policy:** `AA-REMEDIATION-PRIORITY` v1.0.0, rule `P3-OPS-002` · **Change ID:** `CHANGE-AA-031` (Wave 4) · **Source ID:** F-026 · **Primary control:** `APP-OBS-003`

**Severity:** High

**Resiliency Related:** Yes

**Finding status:** Verified finding

**Issue:** The gateway generates a new UUID correlation identifier per request and does not honour an inbound `X-Correlation-Id` header. The console log pattern references `%X{correlationId}` while `MDC.put` is never called anywhere in the repository, so the MDC field is always empty. `BaseEvent` declares a `correlationId` that its constructor never assigns and no producer sets. The shared exception handler assigns a fresh random `traceId` per exception rather than deriving it from an inbound header or from MDC. No tracing library and no `traceparent` handling exists.

**What does this solve:** It makes a single business operation reconstructable across the gateway, a service, Kafka, and the notification consumer, including across a failover boundary.

**Impact:** A request that crosses the gateway, a service, Kafka, and the notification consumer cannot be reconstructed. During a regional incident there is no way to follow a single business operation across services or across a failover boundary, so failure signals are incomplete even though runtime behavior is otherwise correct.

**Recommended Fix:** Honour an inbound `X-Correlation-Id`, generate one only when absent, place it in MDC and the reactive context, forward it downstream and echo it to the caller, stamp it onto every published record, and derive the exception `traceId` from it.

**File:** source/customer-app/api-gateway/src/main/resources/application.yml:145-146

```yaml
// before
    pattern:
      console: "%d{yyyy-MM-dd HH:mm:ss} [%thread] %-5level [%X{correlationId}] %logger{36} - %msg%n"
```

**File:** source/customer-app/common/src/main/java/com/ecommerce/common/events/BaseEvent.java:26-32

```java
// before
    public BaseEvent(String eventType, String sourceService) {
        this.eventId = UUID.randomUUID().toString();
        this.eventType = eventType;
        this.sourceService = sourceService;
        this.occurredAt = LocalDateTime.now();
        this.version = 1;
    }
```

**File:** source/customer-app/api-gateway/src/main/java/com/ecommerce/gateway/filter/RequestLoggingFilter.java:24-43 — `filter`

> Original source excerpt: Not available in authoritative evidence artifact. Step 2 evidence `EV-F-026-03` records that a new UUID correlation identifier is generated per request and that no inbound `X-Correlation-Id` header is read or honoured.

**Fix:**

> Illustrative proposal only.

`source/customer-app/common/src/main/java/com/ecommerce/common/observability/CorrelationContext.java`

```java
package com.ecommerce.common.observability;

import java.util.UUID;
import org.slf4j.MDC;

/** Single source of correlation identity for logs, downstream calls, and events. */
public final class CorrelationContext {

    public static final String HEADER = "X-Correlation-Id";
    public static final String MDC_KEY = "correlationId";

    private CorrelationContext() {
    }

    /** Honours an inbound identifier; generates one only when none was supplied. */
    public static String resolve(String inboundHeaderValue) {
        return (inboundHeaderValue == null || inboundHeaderValue.isBlank())
                ? UUID.randomUUID().toString()
                : inboundHeaderValue;
    }

    public static void put(String correlationId) {
        MDC.put(MDC_KEY, correlationId);
    }

    public static String currentCorrelationId() {
        String current = MDC.get(MDC_KEY);
        return current == null ? "" : current;
    }

    public static void clear() {
        MDC.remove(MDC_KEY);
    }
}
```

The MDC key matches the `%X{correlationId}` token already present in the console log pattern, so the existing pattern begins producing real values instead of an empty field. Honouring an inbound identifier is what makes the identity survive a hop rather than being regenerated.

`source/customer-app/api-gateway/src/main/java/com/ecommerce/gateway/filter/RequestLoggingFilter.java` — `filter`

```java
@Override
public Mono<Void> filter(ServerWebExchange exchange, GatewayFilterChain chain) {
    String correlationId = CorrelationContext.resolve(
            exchange.getRequest().getHeaders().getFirst(CorrelationContext.HEADER));

    ServerWebExchange mutated = exchange.mutate()
            .request(builder -> builder.header(CorrelationContext.HEADER, correlationId))
            .build();
    mutated.getResponse().getHeaders().add(CorrelationContext.HEADER, correlationId);

    CorrelationContext.put(correlationId);
    try {
        return chain.filter(mutated)
                .contextWrite(context -> context.put(CorrelationContext.MDC_KEY, correlationId));
    } finally {
        CorrelationContext.clear();
    }
}
```

The filter now honours an inbound identifier instead of always minting a new one, forwards it to the downstream service as a request header, returns it to the caller, and places it in both MDC and the Reactor context so downstream reactive operators can read it. Clearing MDC in a `finally` block prevents leakage across pooled event-loop threads.

**Notes:**

* **Cross-refs:** Depends on **P2-001** (the event envelope carries the identifier onto Kafka records) and **P0-012**. Consumed by **P0-007**, whose outbox payload calls `CorrelationContext.currentCorrelationId()`.
* **Implementation:** `CHANGE-AA-031`, Wave 4, complexity medium. All three targets carry generated code.
* **Validation:** T-AA-031-01 (a supplied correlation identifier appears in gateway logs, downstream service logs, the Kafka record, and the consumer log line). `mvn -f source/customer-app/pom.xml -pl common,api-gateway,order-service,notification-service -am test`.
* **Guardrail:** Accepting a caller-supplied identifier allows log injection if the value is not validated; it should be length-limited and character-restricted (`OQ-35`).

<span style="font-size: 14px;">**MSFT Reference:** [Distributed tracing and correlation](https://learn.microsoft.com/azure/azure-monitor/app/distributed-trace-data)</span>

---

#### P3-003: Business throughput, consumer lag, and stuck work are not observable

**Priority: P3 - Optimization**

**Priority policy:** `AA-REMEDIATION-PRIORITY` v1.0.0, rule `P3-OPS-002` · **Change ID:** `CHANGE-AA-032` (Wave 4) · **Source ID:** F-027 · **Primary control:** `APP-OBS-002`

**Severity:** High

**Resiliency Related:** Yes

**Finding status:** Verified finding

**Issue:** No custom meters exist in any service and `MeterRegistry` is not referenced in `cart-service` or `inventory-service` despite the Prometheus registry being present and the endpoint exposed. There is no consumer lag, assignment, or paused-partition signal, no `KafkaHealthIndicator`, no last-successful-run or backlog-age gauge for the four scheduled jobs, no Redis command latency or hit-rate metric, and no publish-failure or retry-exhausted counter.

**What does this solve:** It makes a stalled consumer, a scheduler that never ran, a Redis outage, and a silent publish failure detectable before customers report them.

**Impact:** Pod health remains UP while business processing has stopped. A stalled consumer, a scheduler that never ran, a Redis outage, or a silent event-publish failure is invisible until customers report it. This is an incomplete-failure-signal gap rather than a runtime-behavior defect.

**Recommended Fix:** Add a shared workload-health recorder that registers a last-success timestamp gauge and success, failure, and skipped counters per named workload; report Kafka container assignment and paused state; and have the outbox, fallback, dead-letter, and rate-limit changes contribute their counters under the same naming convention.

**File:** source/customer-app/product-service/src/main/resources/application.yml:56-68

```yaml
// before
management:
  endpoints:
    web:
      exposure:
        include: health,info,metrics,prometheus
  metrics:
    export:
      prometheus:
        enabled: true
    tags:
      application: product-service
      region: westus
```

**File:** source/customer-app — repository-wide custom meter inventory (evidence `EV-F-027-02`; original source excerpt: `not_applicable`)

> The authoritative inventory records `custom_meters: none_observed` and `meter_registry_referenced_in_code`: not referenced in `cart-service` or `inventory-service`.

**Fix:**

> Illustrative proposal only.

`source/customer-app/common/src/main/java/com/ecommerce/common/observability/WorkloadHealthRecorder.java`

```java
package com.ecommerce.common.observability;

import io.micrometer.core.instrument.MeterRegistry;
import io.micrometer.core.instrument.Tags;
import java.time.Duration;
import java.time.Instant;
import java.util.Map;
import java.util.concurrent.ConcurrentHashMap;
import java.util.concurrent.atomic.AtomicLong;
import org.springframework.stereotype.Component;

/** Records last-success and failure signals for named workloads so stalls are alertable. */
@Component
public class WorkloadHealthRecorder {

    private final MeterRegistry meterRegistry;
    private final Map<String, AtomicLong> lastSuccessEpochSeconds = new ConcurrentHashMap<>();

    public WorkloadHealthRecorder(MeterRegistry meterRegistry) {
        this.meterRegistry = meterRegistry;
    }

    public void recordSuccess(String workload) {
        lastSuccessGauge(workload).set(Instant.now().getEpochSecond());
        meterRegistry.counter("workload.runs", Tags.of("workload", workload, "outcome", "success"))
                .increment();
    }

    public void recordFailure(String workload, Throwable cause) {
        meterRegistry.counter("workload.runs", Tags.of(
                "workload", workload,
                "outcome", "failure",
                "reason", cause.getClass().getSimpleName())).increment();
    }

    public void recordSkipped(String workload, String reason) {
        meterRegistry.counter("workload.runs",
                Tags.of("workload", workload, "outcome", "skipped", "reason", reason)).increment();
    }

    /** Seconds since the workload last succeeded; alert when this exceeds the expected interval. */
    public Duration timeSinceLastSuccess(String workload) {
        return Duration.ofSeconds(
                Instant.now().getEpochSecond() - lastSuccessGauge(workload).get());
    }

    private AtomicLong lastSuccessGauge(String workload) {
        return lastSuccessEpochSeconds.computeIfAbsent(workload, name -> {
            AtomicLong holder = new AtomicLong(Instant.now().getEpochSecond());
            meterRegistry.gauge("workload.last_success_epoch_seconds",
                    Tags.of("workload", name), holder, AtomicLong::doubleValue);
            return holder;
        });
    }
}
```

Supplies the last-successful-run and backlog-age primitives that do not exist today, in a form every scheduler, consumer, and relay can reuse. Distinguishing skipped from failed is what allows an alert to tell a not-owner deployment apart from a broken one, which the ownership model makes necessary.

`source/customer-app/inventory-service/src/main/java/com/ecommerce/inventory/service/InventoryService.java` — `expireOldReservations` telemetry

```java
@Scheduled(fixedDelayString = "${app.inventory.reservation-expiry.interval-ms:300000}")
public void expireOldReservations() {
    if (!ownershipGuard.isOwner()) {
        workloadHealthRecorder.recordSkipped("inventory.reservation-expiry", "not_owner");
        return;
    }
    try {
        expireReservationsForOwnedTerm();
        workloadHealthRecorder.recordSuccess("inventory.reservation-expiry");
    } catch (Exception e) {
        workloadHealthRecorder.recordFailure("inventory.reservation-expiry", e);
        throw e;
    }
}
```

`inventory-service` does not reference `MeterRegistry` at all today. This makes a skipped run, a successful run, and a failed run each produce a distinct signal, so an alert can detect that the sweep has not succeeded within its expected interval in either region.

**Notes:**

* **Cross-refs:** Depends on **P0-010** and **P0-012**. Supplies the no-owner alert that **P0-009** and **P0-010** make necessary (`OQ-14`). The counters introduced by **P0-007**, **P1-008**, **P2-003**, and **P2-005** should follow the same naming convention.
* **Implementation:** `CHANGE-AA-032`, Wave 4, complexity medium. All three targets carry generated code.
* **Validation:** T-AA-032-01 (a stalled consumer, a skipped scheduled run, and a failed publish each produce a distinct metric). `mvn -f source/customer-app/pom.xml -pl common,inventory-service,cart-service,notification-service -am test`.
* **Guardrail:** Metric cardinality grows with the `reason` tag; reason values must be a bounded enumeration rather than free text. `OQ-36` records that metric naming convention and alert thresholds are undecided.

<span style="font-size: 14px;">**MSFT Reference:** [Observability — Azure Well-Architected Framework](https://learn.microsoft.com/azure/well-architected/operational-excellence/observability)</span>

---

#### Configuration Hygiene

#### P3-004: Operationally variable business constants are hardcoded

**Priority: P3 - Optimization**

**Priority policy:** `AA-REMEDIATION-PRIORITY` v1.0.0, rule `P3-OPS-005` · **Change ID:** `CHANGE-AA-033` (Wave 4) · **Source ID:** F-032 · **Primary control:** `APP-CONF-014`

**Severity:** Low

**Resiliency Related:** Yes

**Finding status:** Verified finding

**Issue:** The default warehouse identifier is a compiled constant that also carries a region string, and it is repeated in the inventory controller. The reservation TTL is compiled. The order number prefix is likewise a compiled literal. None of these values is externalized or documented as fixed.

**What does this solve:** It allows a second-region warehouse to be added and an order-number contract to change without a code release, and removes the confusing region token from a business identifier.

**Impact:** Adding a second-region warehouse or changing an order-number contract requires a code release, and the embedded region token in a business identifier invites confusion with a deployment region selector. The gap primarily affects operational understanding and change cadence rather than active-active correctness, because the values are business data rather than dependency endpoints — no P0, P1, or P2 rule applies.

**Recommended Fix:** Externalize the warehouse identifier, the reservation TTL, and the order-number prefix into validated configuration with documented defaults, and make the warehouse identifier a required deployment input so no region token remains in source.

**File:** source/customer-app/inventory-service/src/main/java/com/ecommerce/inventory/service/InventoryService.java:32-33

```java
// before
    private static final String DEFAULT_WAREHOUSE = "WH-WESTUS-001";
    private static final int RESERVATION_TTL_MINUTES = 30;
```

**File:** source/customer-app/order-service/src/main/java/com/ecommerce/order/service/OrderService.java:318

```java
// before
            return "ORD-" + timestamp + "-" + random;
```

**Fix:**

> Illustrative proposal only.

`source/customer-app/inventory-service/src/main/java/com/ecommerce/inventory/config/InventoryBusinessProperties.java`

```java
package com.ecommerce.inventory.config;

import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.Positive;
import java.time.Duration;
import org.springframework.boot.context.properties.ConfigurationProperties;
import org.springframework.validation.annotation.Validated;

@Validated
@ConfigurationProperties(prefix = "app.inventory")
public class InventoryBusinessProperties {

    /** Warehouse used when a request supplies none. Deployment-supplied business data. */
    @NotBlank
    private String defaultWarehouse;

    @Positive
    private Duration reservationTtl = Duration.ofMinutes(30);

    // getters and setters omitted for brevity
}
```

Replaces the two compiled constants with validated configuration. `defaultWarehouse` has no default so a deployment must state it explicitly, which prevents a second region silently inheriting a first-region warehouse. `reservationTtl` keeps the observed 30-minute value as a documented default.

`source/customer-app/inventory-service/src/main/resources/application.yml` — `app.inventory`

```yaml
app:
  inventory:
    default-warehouse: ${APP_DEFAULT_WAREHOUSE}
    reservation-ttl: ${APP_RESERVATION_TTL:PT30M}
  order:
    number-prefix: ${APP_ORDER_NUMBER_PREFIX:ORD}
```

The warehouse identifier becomes a required deployment input with no committed default, so the region token that was compiled into `WH-WESTUS-001` no longer exists in source. The TTL and the order-number prefix keep their observed values as documented defaults.

**Notes:**

* **Cross-refs:** Depends on **P2-004** (the order-number prefix property must serve both changes as a single definition) and **P0-012**.
* **Implementation:** `CHANGE-AA-033`, Wave 4, complexity low. All three targets carry generated code.
* **Validation:** T-AA-033-01 (warehouse identifier and reservation TTL resolve from external configuration with documented defaults; a missing required value fails startup). `mvn -f source/customer-app/pom.xml -pl common,inventory-service,order-service -am test`.
* **Guardrail:** Making `default-warehouse` required will fail startup for any deployment that has not been updated; the deployment inputs must land first (`OQ-37`).

<span style="font-size: 14px;">**MSFT Reference:** [External Configuration Store pattern](https://learn.microsoft.com/azure/architecture/patterns/external-configuration-store)</span>

[Back to Top](#top)

---
## 3. Non-Resiliency-Focused Recommendations

### P0

No approved finding is classified as non-resiliency-related at P0.

### P1

No approved finding is classified as non-resiliency-related at P1.

### P2

No approved finding is classified as non-resiliency-related at P2.

### P3

No approved finding is classified as non-resiliency-related at P3.

All 34 approved findings carry `resiliency_related: true` in the authoritative Step 3A remediation plan. This section is preserved for schema conformance and is intentionally empty of findings. No finding was reclassified, moved, or created to populate it.

### Verified controls

The following controls are evidence-backed and require no application code change. They are excluded from all finding counts, from the Full Finding Matrix, and from implementation scope.

| Control | Standard | Evidence-based status |
|---|---|---|
| `APP-AA-001` | Master v4.0.0 | A single Maven artifact and a single runtime image per service; region values arrive from environment. `source/customer-app/order-service/Dockerfile` lines 1-26. |
| `APP-AA-008` | Master v4.0.0 | Default liveness group resolves to `livenessState` only; no external dependency is wired into liveness. |
| `APP-CACHE-003` | Master v4.0.0 | The product cache is Redis-backed and shared; no pod-local cache is required for correctness. |
| `APP-HTTP-001` | Master v4.0.0 | No blocking client or vendor SDK executes on the reactive gateway threads; backing services are servlet-based. |
| `APP-HTTP-005` | Master v4.0.0 | No globally shared dependency participates in readiness. |
| `KV-002` | Key Vault v2.0.0 | `managed-identity-enabled: true`; no static secret credential in code. |
| `KV-004` | Key Vault v2.0.0 | Secrets resolve through a startup property source, not per request. |
| `SQL-001` | Azure SQL v2.0.0 | `spring.datasource.url` binds `${AZURE_SQL_HOST}` and `${AZURE_SQL_DB}`; the server is deployment-injected. |
| `REDIS-001` | Azure Managed Redis v2.0.0 | Redis carries cache and rate-limit counters only; Azure SQL and Cosmos DB remain authoritative. |
| `REDIS-002` | Azure Managed Redis v2.0.0 | Cache misses fall through to the authoritative repository. |
| `REDIS-024` | Azure Managed Redis v2.0.0 | A single Spring-managed `ReactiveRedisTemplate` is constructor-injected. |
| `HTTP-009` | HTTP client v2.0.0 | No globally shared provider is added to readiness. |
| `AKS-ISTIO-008` | AKS with Istio v2.0.0 | A single bounded retry layer exists and no mesh retry configuration is present in the repository. |

**Total verified controls: 13.** Note that `APP-AA-008` and the liveness posture it records must be preserved when **P0-003** introduces explicit health groups; the proposed liveness group is deliberately pinned to `livenessState` for exactly this reason.

### Non-finding observations

* Four controls (`AKS-ISTIO-002`, `AKS-ISTIO-017`, and related) were marked `not_applicable` because startup probes, HPA, PDB, and topology spread are listed under the master standard's `excluded_from_findings` set. This is informational only.
* The absence of an approved application architecture context file is recorded as evidence requirement `EXT-006`, **not** as a finding.
* Four inventory exceptions (`INV-EXC-001` through `INV-EXC-004`) were recorded during Step 2 — two incorrect cited paths resolved to the same symbol in the same module, one count discrepancy (`notification-service` `@KafkaListener` count cited as 13, observed 12), and one carried-forward uncertainty group. None became a finding.

[Back to Top](#top)

---

## 4. Repository and IaC Evidence Gap Analysis

This assessment observed application code, application configuration, application-owned Kubernetes workload manifests, Dockerfiles, and the build pipeline definition. Platform artifacts outside the repository were neither read nor assessed. **Absence of infrastructure evidence is not reported as infrastructure noncompliance and no infrastructure finding was created.**

### Available to review

| Repository-visible configuration | Current evidence | Application resiliency interpretation | Related findings |
|---|---|---|---|
| Nine `application.yml` files (one per service, plus `common`) | Endpoints, Kafka clients, datasources, Redis, actuator, metrics tags, logging patterns | The entire application-side failure budget, health contract, and regional binding is expressed here — and most of it is either absent or bound to a non-effective prefix | P0-001, P0-003, P0-011, P1-001, P1-002, P1-003, P1-004, P1-005, P1-010, P1-011, P2-002, P2-003, P3-001 |
| `source/customer-app/pom.xml` and nine module POMs | Spring Boot 3.2.5, Spring Cloud, Spring Cloud Azure BOM imports; `spring-boot-starter-test` declared in all nine modules; Resilience4j declared only in `api-gateway` | Dependency posture is legible, but no test tree exercises it and the resilience library is absent from the seven backing services | P0-012, P1-006 |
| Eight `Dockerfile` files | Two-stage builds, `-DskipTests`, `HEALTHCHECK` on the aggregate endpoint, base images referenced by mutable tag | Build reproducibility and container health semantics are application-owned and currently unsafe for two-region operation | P0-003, P0-012, P1-013 |
| `source/customer-app/k8s/01-configmap.yaml` | `AZURE_REGION: "westus"`, `KAFKA_BOOTSTRAP_SERVERS`, frontend URL, all committed literals | Treated as application-owned configuration because approved findings cite it directly; it is the single largest source of regional pinning | P0-001 |
| `source/customer-app/k8s/services/all-services.yaml` | Container specs, probe definitions with no `timeoutSeconds`, no `terminationGracePeriodSeconds`, no `preStop` hook | Probe wiring and drain window are application-owned workload configuration | P0-003, P0-011, P1-010 |
| `source/customer-app/k8s/services/api-gateway.yaml` | Service type `LoadBalancer` with `azure-load-balancer-internal: false`, 443 mapped to the actuator-serving container port | Establishes that the management surface is internet-reachable; the remediation is port isolation in application configuration and the published port list, not a network change | P1-010 |
| `source/customer-app/azure-pipelines.yml` | `mvn verify` step that executes no tests; `sed` substitution for `ACR_NAME` and `IMAGE_TAG` | The substitution mechanism that region-parameterised tokens will consume already exists; `UNC-013` records that `api-gateway.yaml` is currently applied before substitution | P0-001, P0-012 |
| `source/customer-app/docker-compose.yml` | Local development topology | Informational only; no finding derives from it | — |
| Java source across nine modules | Listeners, schedulers, services, repositories, filters, entities, events | The substance of every behavioral finding | All |

### Not available or externally owned

| External evidence or configuration | Needed to validate | Related findings or assumptions |
|---|---|---|
| `EXT-001` — Kafka cluster deployment topology and regional role assignment | Confirms whether the inferred `active_standby` scenario matches the deployed broker topology and which region may process authoritative work | Conditional finding **P0-009**; controls `KAFKA-AS-004`, `KAFKA-AS-005`, `KAFKA-AS-008` are `not_assessed`; blocks `TD-06` |
| `EXT-002` — Cluster Linking, mirror topics, and consumer-offset replication | Confirms whether offsets survive a regional promotion, which determines whether consumer-side deduplication is sufficient | **P0-009**, **P2-001**; controls `KAFKA-AS-004`, `KAFKA-AS-005` are `not_assessed`; blocks `TD-06` |
| `EXT-003` — Azure SQL Failover Group deployment and listener endpoint configuration | Confirms whether a single authoritative order/payment database exists and how primary role can be verified by the application | **P0-009**, **P0-010**; the declined P0 elevation for **P2-004** must be revisited if independent regional order databases are confirmed; blocks `TD-06` |
| `EXT-004` — Cosmos DB account multi-region-write enablement and configured write regions | Determines whether a preferred-region list moves writes local or only reads | **P0-002**; control `COSMOS-004` is `not_assessed` |
| `EXT-005` — Azure Cache for Redis replication and geo-replication configuration | Determines the regional consistency semantics of rate-limit counters and cached data | **P2-005**; control `REDIS-018` is `not_assessed` |
| `EXT-006` — Approved application architecture context confirming the Kafka operating scenario | Converts the policy-inferred `active_standby` scenario into a confirmed one and allows **P0-009** to move from conditional to verified | **P0-009**; control `KAFKA-009` is `not_assessed`. Only unfilled templates exist under `application-context/Templates/` |
| Terraform, Bicep, ARM, or other Azure provisioning definitions | Out of assessment scope by the supplied application context | None — no infrastructure finding was created |
| Istio `VirtualService`, `DestinationRule`, `Gateway`, and mesh retry/timeout policy | Would show whether mesh-level retry or timeout interacts with the application budget | Informational for **P1-006** and **P1-007**; control `AKS-ISTIO-008` is compliant on repository evidence alone |
| Private endpoint, DNS, capacity, zone, and global load balancer configuration | Out of assessment scope | None |
| Second-region Kubernetes manifests (`UNC-004`) | Confirms whether the probe, drain, and port edits in **P0-003**, **P0-011**, and **P1-010** must be mirrored in another repository | **P0-003**, **P0-011**, **P1-010**; risk `R-07` |
| Effective BOM-resolved dependency versions (`UNC-016`) | Confirms the Spring Cloud Azure client-customization API, the Resilience4j version, and the Spring Security classpath | Blocks `TD-01`, `TD-07`, `TD-08`, `TD-09`; `OQ-02`, `OQ-21`, `OQ-25` |
| Current build result for the `common` module (`UNC-006`) | Confirms whether six recorded Spring Security compilation errors persist | **Blocking risk `R-01`** for the entire plan; `OQ-16` |

### Not-assessed control summary

Twenty-four controls are `not_assessed`. None is presented as a confirmed defect.

* **Deployed topology required (7):** `COSMOS-004`, `REDIS-018`, `KAFKA-009`, `KAFKA-AS-004`, `KAFKA-AS-005`, `KAFKA-AS-008`, and the topology portion of `REDIS-006`. Resolution requires `EXT-001` through `EXT-006`.
* **Unresolved inventory uncertainty (11):** `APP-DISC-001`, `APP-DISC-002`, `APP-WEB-001`, `APP-REACT-001`, `APP-REACT-002`, `APP-CORRECT-001`, `APP-CACHE-004`, `APP-CACHE-006`, `REDIS-009`, `REDIS-015`, `HTTP-007`. Resolution requires build or runtime verification per `UNC-006` through `UNC-016`.
* **Evidence not available for validation (6):** `APP-LOG-001`, `APP-LOG-002`, `APP-API-001`, `REDIS-013`, `REDIS-021`, `REDIS-022`. The inventory cited no evidence sufficient to reach a conclusion, and expanding the search would have constituted re-inventory.

### PCF exclusion

> PCF and its aliases are retired and excluded from findings, scoring, remediation, modernization, migration, and cleanup recommendations. Historical repository references, if discovered, are informational only and are not included in the finding matrix.

[Back to Top](#top)

---

## 5. Full Finding Matrix

One row per approved finding. Verified controls, non-finding observations, `not_assessed` controls, `not_applicable` controls, accepted risks, and PCF references are excluded.

| ID | Priority | Severity | Resiliency related | Status | Category | Finding | Change ID | Source ID | Repository scope |
|---|---|---|---|---|---|---|---|---|---|
| [P0-001](#p0-001-regional-service-endpoints-are-hardcoded-in-application-configuration) | P0 | Critical | Yes | Verified | Configuration contract | Regional service endpoints are hardcoded in application configuration | CHANGE-AA-001 | F-001 | product-service, api-gateway, notification-service, k8s |
| [P0-002](#p0-002-cosmos-db-client-has-no-local-region-preference-or-endpoint-discovery-policy) | P0 | Critical | Yes | Verified | Regional affinity | Cosmos DB client has no local-region preference or endpoint-discovery policy | CHANGE-AA-002 | F-002 | common, product-service, inventory-service, cart-service |
| [P0-003](#p0-003-readiness-does-not-reflect-any-critical-region-local-dependency) | P0 | Critical | Yes | Verified | Health | Readiness does not reflect any critical region-local dependency | CHANGE-AA-003 | F-016 | all eight services, common, k8s |
| [P0-004](#p0-004-notification-state-is-held-in-an-unbounded-in-process-map) | P0 | Critical | Yes | Verified | State | Notification state is held in an unbounded in-process map | CHANGE-AA-004 | F-028 | notification-service |
| [P0-005](#p0-005-cosmos-writes-are-non-atomic-read-modify-write-with-unused-optimistic-concurrency) | P0 | Critical | Yes | Verified | Consistency | Cosmos writes are non-atomic read-modify-write with unused optimistic concurrency | CHANGE-AA-005 | F-004 | inventory-service |
| [P0-006](#p0-006-payment-processing-has-no-durable-idempotency-key-and-calls-the-provider-inside-the-transaction) | P0 | Critical | Yes | Verified | Financial integrity | Payment processing has no durable idempotency key and calls the provider inside the transaction | CHANGE-AA-006 | F-012 | payment-service |
| [P0-007](#p0-007-database-commit-and-event-publish-share-one-transaction-with-no-outbox-or-reconciliation) | P0 | Critical | Yes | Verified | Database consistency | Database commit and event publish share one transaction with no outbox or reconciliation | CHANGE-AA-007 | F-011 | order-service, payment-service |
| [P0-008](#p0-008-kafka-producer-send-results-are-discarded-and-publish-failures-are-swallowed) | P0 | Critical | Yes | Verified (consolidated) | Messaging | Kafka producer send results are discarded and publish failures are swallowed | CHANGE-AA-007 | F-005 | order-service, payment-service |
| [P0-009](#p0-009-kafka-producers-and-consumers-are-unconditionally-active-in-every-replica) | P0 | Critical | Yes | **Conditional** | Workload ownership | Kafka producers and consumers are unconditionally active in every replica | CHANGE-AA-008 | F-014 | common, inventory-service, notification-service |
| [P0-010](#p0-010-scheduled-jobs-execute-on-every-replica-with-no-distributed-ownership) | P0 | Critical | Yes | Verified | Scheduler | Scheduled jobs execute on every replica with no distributed ownership | CHANGE-AA-009 | F-015 | inventory-service, cart-service |
| [P0-011](#p0-011-graceful-shutdown-and-traffic-draining-are-incomplete) | P0 | High | Yes | Verified | Lifecycle | Graceful shutdown and traffic draining are incomplete | CHANGE-AA-010 | F-017 | all eight services, common, k8s |
| [P0-012](#p0-012-no-automated-test-coverage-exists-for-any-failure-or-recovery-behavior) | P0 | Critical | Yes | Verified | Testing | No automated test coverage exists for any failure or recovery behavior | CHANGE-AA-011 | F-018 | reactor, all nine modules |
| [P1-001](#p1-001-declared-redis-and-cache-properties-are-never-bound-or-consumed) | P1 | High | Yes | Verified | Configuration | Declared Redis and cache properties are never bound or consumed | CHANGE-AA-012 | F-024 | api-gateway, product-service, common |
| [P1-002](#p1-002-cosmos-db-retry-timeout-and-throttling-budgets-are-absent) | P1 | High | Yes | Verified | Resilience | Cosmos DB retry, timeout, and throttling budgets are absent | CHANGE-AA-013 | F-003 | common, product-service, inventory-service, cart-service |
| [P1-003](#p1-003-kafka-client-timeout-reconnect-and-backoff-settings-are-unbounded) | P1 | High | Yes | Verified | Resilience | Kafka client timeout, reconnect, and backoff settings are unbounded | CHANGE-AA-014 | F-007 | seven Kafka-using services |
| [P1-004](#p1-004-azure-sql-pool-and-statement-budgets-are-incomplete-and-failover-recovery-is-unproven) | P1 | High | Yes | Verified | Resilience | Azure SQL pool and statement budgets are incomplete and failover recovery is unproven | CHANGE-AA-015 | F-020 | order-service, payment-service, user-service |
| [P1-005](#p1-005-producer-durability-settings-are-inconsistent-across-services) | P1 | High | Yes | Verified | Messaging | Producer durability settings are inconsistent across services | CHANGE-AA-016 | F-006 | six producing services |
| [P1-006](#p1-006-backing-services-have-no-timeout-retry-circuit-breaker-or-bulkhead) | P1 | Critical | Yes | Verified | Resilience | Backing services have no timeout, retry, circuit breaker, or bulkhead | CHANGE-AA-017 | F-019 | seven backing services |
| [P1-007](#p1-007-gateway-http-client-pool-is-shared-and-its-timeout-budget-conflicts-with-the-circuit-breaker) | P1 | High | Yes | Verified | HTTP client | Gateway HTTP client pool is shared and its timeout budget conflicts with the circuit breaker | CHANGE-AA-018 | F-022 | api-gateway |
| [P1-008](#p1-008-gateway-circuit-breaker-fallback-targets-have-no-handler) | P1 | High | Yes | Verified | Fallback | Gateway circuit-breaker fallback targets have no handler | CHANGE-AA-019 | F-021 | api-gateway |
| [P1-009](#p1-009-async-listener-execution-has-no-bounded-executor) | P1 | High | Yes | Verified | Async execution | Async listener execution has no bounded executor | CHANGE-AA-020 | F-030 | common, cart-service, notification-service |
| [P1-010](#p1-010-actuator-exposes-administrative-and-detailed-endpoints-without-protection-on-the-traffic-port) | P1 | Critical | Yes | Verified | Management security | Actuator exposes administrative and detailed endpoints without protection on the traffic port | CHANGE-AA-021 | F-029 | all eight services, k8s |
| [P1-011](#p1-011-key-vault-startup-and-rotation-contract-is-absent) | P1 | Critical | Yes | Verified | Startup | Key Vault startup and rotation contract is absent | CHANGE-AA-022 | F-033 | common, api-gateway, order-service, payment-service |
| [P1-012](#p1-012-scheduled-reservation-expiry-loads-the-entire-active-inventory-set-into-memory) | P1 | High | Yes | Verified | Batch memory | Scheduled reservation expiry loads the entire active inventory set into memory | CHANGE-AA-023 | F-034 | inventory-service |
| [P1-013](#p1-013-container-base-images-are-referenced-by-mutable-tag) | P1 | High | Yes | Verified | Supply chain | Container base images are referenced by mutable tag | CHANGE-AA-024 | F-031 | eight Dockerfiles |
| [P2-001](#p2-001-published-events-carry-no-stable-identity-and-consumers-perform-no-deduplication) | P2 | Critical | Yes | Verified | Messaging | Published events carry no stable identity and consumers perform no deduplication | CHANGE-AA-025 | F-010 | common, all producers |
| [P2-002](#p2-002-manual-acknowledgment-is-configured-but-never-performed) | P2 | Critical | Yes | Verified | Consistency | Manual acknowledgment is configured but never performed | CHANGE-AA-026 | F-009 | notification-service |
| [P2-003](#p2-003-consumers-have-no-error-handler-retry-limit-or-dead-letter-routing) | P2 | Critical | Yes | Verified | Messaging | Consumers have no error handler, retry limit, or dead-letter routing | CHANGE-AA-027 | F-008 | notification-service, inventory-service |
| [P2-004](#p2-004-order-business-identifier-is-generated-per-attempt-with-no-region-discriminator) | P2 | High | Yes | Verified | Consistency | Order business identifier is generated per attempt with no region discriminator | CHANGE-AA-028 | F-013 | order-service |
| [P2-005](#p2-005-redis-rate-limiting-fails-open-silently-and-its-two-step-counter-is-not-atomic) | P2 | High | Yes | Verified | Fallback | Redis rate limiting fails open silently and its two-step counter is not atomic | CHANGE-AA-029 | F-023 | api-gateway |
| [P3-001](#p3-001-telemetry-cannot-identify-the-serving-region) | P3 | Medium | Yes | Verified | Observability | Telemetry cannot identify the serving region | CHANGE-AA-030 | F-025 | common, all eight services |
| [P3-002](#p3-002-correlation-identity-is-regenerated-per-hop-and-never-propagated) | P3 | High | Yes | Verified | Observability | Correlation identity is regenerated per hop and never propagated | CHANGE-AA-031 | F-026 | common, api-gateway |
| [P3-003](#p3-003-business-throughput-consumer-lag-and-stuck-work-are-not-observable) | P3 | High | Yes | Verified | Observability | Business throughput, consumer lag, and stuck work are not observable | CHANGE-AA-032 | F-027 | common, inventory-service, cart-service, notification-service |
| [P3-004](#p3-004-operationally-variable-business-constants-are-hardcoded) | P3 | Low | Yes | Verified | Configuration hygiene | Operationally variable business constants are hardcoded | CHANGE-AA-033 | F-032 | inventory-service, order-service |

### Matrix reconciliation

| Measure | Count |
|---|---:|
| Rows in this matrix | 34 |
| Summary Findings table total | 34 |
| Step 2 approved findings (`verified_findings` 33 + `conditional_findings` 1) | 34 |
| Step 3A `approved_findings_total` | 34 |
| P0 rows | 12 |
| P1 rows | 13 |
| P2 rows | 5 |
| P3 rows | 4 |
| Distinct change IDs referenced | 33 (`CHANGE-AA-007` maps two findings) |
| Findings unmapped to a change | 0 |
| Severity: critical / high / medium / low | 17 / 15 / 1 / 1 |
| Status: verified / conditional | 33 / 1 |

Counts reconcile exactly with the Summary Findings table in Section 1, with the Step 2 scorecard, and with the Step 3A mapping reconciliation block.

[Back to Top](#top)

---

## 6. Standards Alignment

Only standards supported by the loaded grounding set or by the governing report schema are listed. No standard or link is invented.

| Standard or pattern | Assessment status | Related controls | Related findings |
|---|---|---|---|
| Spring Boot AKS Active-Active Master Standard v4.0.0 (`grounding/master/springboot-aks-active-active-master.md`) | 86 controls evaluated: 5 compliant, 55 non-compliant, 11 not assessed, 15 not applicable. The artifact is region-neutral (`APP-AA-001` compliant) but traffic eligibility, workload ownership, state portability, and verification are all absent. | `APP-AA-001` … `APP-AA-018`, `APP-KAFKA-*`, `APP-SCHED-*`, `APP-FIN-*`, `APP-OBS-*`, `APP-CONF-*`, `APP-ACT-*`, `APP-ASYNC-*`, `APP-SUPPLY-*` | All 34 findings |
| Azure Key Vault dependency standard v2.0.0 | 16 controls: 2 compliant, 11 non-compliant, 3 not applicable. Managed identity and startup property-source usage are correct; startup bounding, rotation, and recovery contracts are absent. | `KV-002`, `KV-004` compliant; `KV-009` primary, plus `KV-003`, `KV-005`, `KV-006`, `KV-007`, `KV-010`, `KV-013`, `KV-014`, `KV-016` | P1-011, P0-003, P1-010, P3-001 |
| Azure Cosmos DB dependency standard v1.0.0 | 8 controls: 0 compliant, 7 non-compliant, 1 not assessed (`COSMOS-004`, pending `EXT-004`). No regional preference, no request budget, no conditional write. | `COSMOS-002`, `COSMOS-003`, `COSMOS-005`, `COSMOS-006`, `COSMOS-007`, `COSMOS-008` | P0-002, P0-005, P1-002, P0-003, P0-012 |
| Azure SQL dependency standard v2.0.0 | 16 controls: 1 compliant, 10 non-compliant, 5 not applicable. Deployment-injected server binding is correct; statement, transaction, and pool lifecycle budgets are incomplete and the unique idempotency constraint is unmapped. | `SQL-001` compliant; `SQL-002` primary, plus `SQL-003` … `SQL-008`, `SQL-012`, `SQL-013`, `SQL-015` | P1-004, P0-006, P0-007, P1-006, P0-003 |
| Azure Managed Redis dependency standard v2.0.0 | 27 controls: 3 compliant, 13 non-compliant, 7 not assessed, 4 not applicable. Redis is correctly non-authoritative and cache-aside is correct, but the declared client budget does not bind and the rate limiter is non-atomic. | `REDIS-001`, `REDIS-002`, `REDIS-024` compliant; `REDIS-020` primary, plus `REDIS-003` … `REDIS-005`, `REDIS-008`, `REDIS-011`, `REDIS-012`, `REDIS-017`, `REDIS-019`, `REDIS-023`, `REDIS-025` … `REDIS-027` | P1-001, P2-005, P0-003, P3-003, P0-012 |
| HTTP client behavior dependency standard v2.0.0 | 10 controls: 1 compliant, 4 non-compliant, 1 not assessed, 4 not applicable. No blocking client runs on reactive threads, but the shared pool is unbounded and the timeout budget is inverted. | `HTTP-009` compliant; `HTTP-001` primary, plus `HTTP-003`, `HTTP-004`, `HTTP-008` | P1-007, P1-008 |
| AKS with Istio dependency standard v2.0.0 | 18 controls: 1 compliant, 12 non-compliant, 5 not applicable. A single bounded retry layer exists with no conflicting mesh retry, but probe wiring, drain, ownership, and management exposure are all deficient. | `AKS-ISTIO-008` compliant; `AKS-ISTIO-001`, `AKS-ISTIO-003`, `AKS-ISTIO-005` … `AKS-ISTIO-007`, `AKS-ISTIO-009`, `AKS-ISTIO-012` … `AKS-ISTIO-016`, `AKS-ISTIO-018` | P0-003, P0-009, P0-010, P0-011, P1-006, P1-007, P1-008, P1-010, P3-001, P3-003, P0-012 |
| Confluent Kafka dependency standard v3.0.0 (scenario-aware) | 27 controls: 0 compliant, 17 non-compliant, 4 not assessed, 6 not applicable. Common controls `KAFKA-001`–`KAFKA-012` evaluated; scenario family `KAFKA-AS-001`–`KAFKA-AS-009` evaluated under policy inference; `KAFKA-AA-*` and `KAFKA-DI-*` not applicable per rule `KAFKA-SCENARIO-001`. | `KAFKA-002` … `KAFKA-007`, `KAFKA-010` … `KAFKA-012`, `KAFKA-AS-001` … `KAFKA-AS-003`, `KAFKA-AS-006`, `KAFKA-AS-007`, `KAFKA-AS-009` | P0-008, P0-009, P1-003, P1-005, P2-001, P2-002, P2-003, P0-012 |
| Kafka Operating Scenario Policy v3.1.0, rule `KAFKA-SCENARIO-001` | Scenario resolved as `active_standby` by `policy_inference`; validation status `inferred`; architecture confirmation required and outstanding (`EXT-006`). Consumed unchanged by Steps 2, 3A, and 3B. | Scenario family selection for all `KAFKA-*` controls | P0-009 (conditional) |
| Remediation Prioritization Policy `AA-REMEDIATION-PRIORITY` v1.0.0 | Applied to all 33 changes. 8 P2 data-correctness candidates were evaluated for P0 elevation; 5 elevated, 3 declined with recorded rationale. 0 priority overrides. Priority was not derived from severity. | Rules `P0-AA-001` … `P0-AA-007`, `P0-RCV-008`, `P1-RCV-001` … `P1-RCV-006`, `P1-SUP-002`, `P2-DATA-001`, `P2-DATA-002`, `P2-DATA-005`, `P3-OPS-001`, `P3-OPS-002`, `P3-OPS-005` | All 34 findings |
| PCF Code Assessment Exclusion v1.0.0 | Applied. 0 PCF findings, 0 PCF recommendations, 0 PCF entries in the finding matrix or implementation scope. | — | None |
| Albertsons Azure shared-service reference architectures (see Section 1) | Referenced as approved shared-service design inputs. This assessment makes no claim about their deployed state; shared services are assumed compliant per the supplied application context. | — | — |

### Standards not loaded

Seven registry entries were not loaded because the authoritative inventory did not list them as confirmed dependencies: Event Hubs, Blob Storage, PostgreSQL, DSE Cassandra, APIM, Application Gateway and GLB, and Azure Functions. No control from these standards was evaluated and no finding derives from them.

[Back to Top](#top)

---

## 7. Implementation Roadmap

This roadmap summarizes the authoritative Step 3A remediation plan at `.copilot-tracking/plans/2026-09-03/springboot-active-active-remediation-plan.md`. It does not replace it. Priority and wave assignment are **frozen** and may not be recalculated in a later phase.

### Priority summary

| Priority | Change count | Primary objective | Release gate |
|---|---:|---|---|
| P0 | 11 | Make a second region deployable, truthful about its own health, safe under duplicated work, and provable. Nothing below is verifiable until `CHANGE-AA-011` lands. | No region may be brought into rotation until every P0 change is complete and its acceptance tests pass. Blocking precondition: resolve `UNC-006` (`OQ-16`) and confirm the reactor builds. |
| P1 | 13 | Bound every remote dependency, isolate failures inside their own boundary, resolve fallback targets, remove the internet-reachable management surface, and make credential recovery restart-free. | No two-region production cutover without P1 complete; a degraded dependency would otherwise propagate region-wide. |
| P2 | 5 | Make duplicated and replayed work detectable and safe: stable event identity, offset-to-work coupling, dead-letter quarantine, idempotent order creation, atomic rate limiting. | Required before at-least-once delivery from the P0 outbox is enabled in production. `CHANGE-AA-025` is a hard correctness prerequisite of `CHANGE-AA-007`. |
| P3 | 4 | Make regional behavior legible: telemetry attribution, correlation propagation, workload signals, and externalized business constants. | Required before regional operations can be run with confidence; not a functional blocker for cutover. |
| **Total** | **33** | | |

### Implementation waves

Waves express dependency order and release safety only. No dates, sprint lengths, or durations are implied.

| Wave | Change IDs | Findings addressed | Prerequisites | Validation focus |
|---|---|---|---|---|
| **1 — Configuration contract and verification foundation** | CHANGE-AA-011, CHANGE-AA-001, CHANGE-AA-012, CHANGE-AA-024 | P0-012, P0-001, P1-001, P1-013 | `UNC-006` resolved and the reactor builds (`OQ-16`). `CHANGE-AA-011` lands first; the other three then proceed in parallel. `CHANGE-AA-001` and `CHANGE-AA-012` edit overlapping `application.yml` files and must be merged carefully. | `mvn verify` executes a non-zero test count; no regional literal or absolute Azure endpoint remains in shipped configuration; every declared Redis and cache property binds; every `Dockerfile` `FROM` directive is digest-pinned. |
| **2 — Traffic eligibility, ownership, drain, and budgets** | CHANGE-AA-008, CHANGE-AA-003, CHANGE-AA-002, CHANGE-AA-013, CHANGE-AA-014, CHANGE-AA-015, CHANGE-AA-016, CHANGE-AA-019, CHANGE-AA-018, CHANGE-AA-009, CHANGE-AA-010, CHANGE-AA-021 | P0-009, P0-003, P0-002, P1-002, P1-003, P1-004, P1-005, P1-008, P1-007, P0-010, P0-011, P1-010 | Wave 1 complete. `CHANGE-AA-008` leads because `CHANGE-AA-009` and `CHANGE-AA-010` consume its ownership abstraction. `CHANGE-AA-019` precedes `CHANGE-AA-018`. `CHANGE-AA-003` and `CHANGE-AA-021` both rewrite the management block of every `application.yml` and must be merged as one edit per service. `CHANGE-AA-014` and `CHANGE-AA-016` edit the same Kafka blocks and should be applied together. Decisions required: `OQ-13` (ownership and fencing), `OQ-03` (critical-versus-optional dependency classification). | Readiness reflects the critical region-local dependency in every service and recovers without a restart; no listener container starts implicitly and no scheduled sweep runs on a non-owner; every service drains within a bounded window; every remote dependency call carries an explicit, externally configurable deadline; the actuator surface is unreachable from the internet-facing Service. |
| **3 — Authoritative state safety under duplication and interruption** | CHANGE-AA-025, CHANGE-AA-005, CHANGE-AA-006, CHANGE-AA-023, CHANGE-AA-004, CHANGE-AA-007, CHANGE-AA-026, CHANGE-AA-027, CHANGE-AA-020, CHANGE-AA-017, CHANGE-AA-022 | P2-001, P0-005, P0-006, P1-012, P0-004, P0-007 (+P0-008), P2-002, P2-003, P1-009, P1-006, P1-011 | Wave 2 complete. `CHANGE-AA-025` leads because stable event identity is a prerequisite for the outbox, the durable notification store, and consumer acknowledgement. `CHANGE-AA-006` precedes `CHANGE-AA-017` so retry is never applied to a non-idempotent provider call. `CHANGE-AA-026` precedes `CHANGE-AA-027`. `CHANGE-AA-023` edits the same method as `CHANGE-AA-009` and must rebase onto it. Decisions required: `OQ-06`, `OQ-12`, `OQ-10`, `OQ-26`. | No authoritative write is a non-atomic read-modify-write; no provider call or broker call occurs inside a database transaction; every non-idempotent external effect is guarded by a durable identity claim; every consumer failure is bounded, quarantined, and observable; no pod-local store holds business state. |
| **4 — Legibility and identity hygiene** | CHANGE-AA-028, CHANGE-AA-029, CHANGE-AA-030, CHANGE-AA-031, CHANGE-AA-032, CHANGE-AA-033 | P2-004, P2-005, P3-001, P3-002, P3-003, P3-004 | Wave 3 complete. `CHANGE-AA-033` follows `CHANGE-AA-028` because both own the order-number prefix property and it must resolve to a single definition. The three observability changes are mutually independent. | Every metric identifies its serving region, zone, and instance; a single business operation is traceable across gateway, service, Kafka, and consumer; a stalled consumer, a skipped scheduled run, and a failed publish each raise a distinct signal; no operationally variable business constant is compiled. |

### Change index

| Change ID | Priority | Priority rule | Finding IDs | Objective | Complexity | Wave |
|---|---|---|---|---|---|---:|
| CHANGE-AA-001 | P0 | P0-AA-001 | P0-001 (F-001) | Region-neutral endpoint, broker, and origin configuration contract | Medium | 1 |
| CHANGE-AA-002 | P0 | P0-AA-002 | P0-002 (F-002) | Cosmos regional affinity and endpoint-discovery contract | Medium | 2 |
| CHANGE-AA-003 | P0 | P0-AA-003 | P0-003 (F-016) | Dependency-aware readiness with bounded, cached evaluation | Medium | 2 |
| CHANGE-AA-004 | P0 | P0-AA-005 | P0-004 (F-028) | Durable, deduplicating notification store contract | High | 3 |
| CHANGE-AA-005 | P0 | P0-AA-006 | P0-005 (F-004) | Conditional Cosmos writes and stable reservation identity | High | 3 |
| CHANGE-AA-006 | P0 | P0-AA-006 | P0-006 (F-012) | Durable payment idempotency key and provider call outside the transaction | High | 3 |
| CHANGE-AA-007 | P0 | P0-AA-006 | P0-007 (F-011), P0-008 (F-005) | Transactional outbox with observed delivery | High | 3 |
| CHANGE-AA-008 | P0 | P0-AA-006 | P0-009 (F-014) | Regional ownership gate for Kafka listeners and producers | High | 2 |
| CHANGE-AA-009 | P0 | P0-AA-006 | P0-010 (F-015) | Distributed ownership and atomic claim for scheduled work | Medium | 2 |
| CHANGE-AA-010 | P0 | P0-RCV-008 | P0-011 (F-017) | Graceful shutdown, drain, and ownership release | Medium | 2 |
| CHANGE-AA-011 | P0 | P0-AA-007 | P0-012 (F-018) | Test harness and build-time test enforcement | Medium | 1 |
| CHANGE-AA-012 | P1 | P1-RCV-001 | P1-001 (F-024) | Make declared resiliency and cache properties bind | Low | 1 |
| CHANGE-AA-013 | P1 | P1-RCV-001 | P1-002 (F-003) | Cosmos request budget and typed error handling | Medium | 2 |
| CHANGE-AA-014 | P1 | P1-RCV-001 | P1-003 (F-007) | Bounded Kafka client timeout and backoff budget | Low | 2 |
| CHANGE-AA-015 | P1 | P1-RCV-001 | P1-004 (F-020) | Azure SQL statement, transaction, and pool budgets | Low | 2 |
| CHANGE-AA-016 | P1 | P1-RCV-002 | P1-005 (F-006) | Consistent producer durability and delivery deadline | Low | 2 |
| CHANGE-AA-017 | P1 | P1-RCV-003 | P1-006 (F-019) | Dependency isolation in the seven backing services | High | 3 |
| CHANGE-AA-018 | P1 | P1-RCV-003 | P1-007 (F-022) | Gateway pool bounds and ordered timeout budget | Medium | 2 |
| CHANGE-AA-019 | P1 | P1-RCV-006 | P1-008 (F-021) | Explicit, bounded, observable gateway fallback handlers | Low | 2 |
| CHANGE-AA-020 | P1 | P1-RCV-003 | P1-009 (F-030) | Bounded, named async executor | Low | 3 |
| CHANGE-AA-021 | P1 | P1-RCV-003 | P1-010 (F-029) | Isolate and protect management endpoints | Medium | 2 |
| CHANGE-AA-022 | P1 | P1-RCV-004 | P1-011 (F-033) | Bounded Key Vault startup and restart-free refresh | High | 3 |
| CHANGE-AA-023 | P1 | P1-RCV-003 | P1-012 (F-034) | Bounded, resumable scheduled sweep | Medium | 3 |
| CHANGE-AA-024 | P1 | P1-SUP-002 | P1-013 (F-031) | Pin container base images by digest | Low | 1 |
| CHANGE-AA-025 | P2 | P2-DATA-002 | P2-001 (F-010) | Stable event identity on every published record | Medium | 3 |
| CHANGE-AA-026 | P2 | P2-DATA-002 | P2-002 (F-009) | Couple offset commit to completed processing | Medium | 3 |
| CHANGE-AA-027 | P2 | P2-DATA-002 | P2-003 (F-008) | Consumer error handler and dead-letter routing | Medium | 3 |
| CHANGE-AA-028 | P2 | P2-DATA-001 | P2-004 (F-013) | Stable order identity with client idempotency key | Medium | 4 |
| CHANGE-AA-029 | P2 | P2-DATA-005 | P2-005 (F-023) | Atomic rate-limit counter with explicit failure policy | Medium | 4 |
| CHANGE-AA-030 | P3 | P3-OPS-001 | P3-001 (F-025) | Region, zone, and instance telemetry attribution | Low | 4 |
| CHANGE-AA-031 | P3 | P3-OPS-002 | P3-002 (F-026) | Honour, propagate, and persist correlation identity | Medium | 4 |
| CHANGE-AA-032 | P3 | P3-OPS-002 | P3-003 (F-027) | Business throughput, backlog, and stuck-work signals | Medium | 4 |
| CHANGE-AA-033 | P3 | P3-OPS-005 | P3-004 (F-032) | Externalize operationally variable business constants | Low | 4 |

### Targeted implementation discovery

Nine of the 110 illustrative-code targets are blocked on a specific unresolved fact. Targeted discovery is assigned **per target, never per change** — in every case the surrounding change still carries concrete generated code for its remaining targets.

| ID | Change | Blocked target | Blocking fact | Related | Generated targets still in the same change |
|---|---|---|---|---|---:|
| TD-01 | CHANGE-AA-002 | `CosmosClientBuilder` regional customizer bean | Effective `spring-cloud-azure-starter-data-cosmos` 5.10.0 builder-customizer API | `UNC-016` | 2 |
| TD-02 | CHANGE-AA-003 | Key Vault readiness contributor | No Key Vault SDK client exists in the repository to probe | — | 5 |
| TD-03 | CHANGE-AA-004 | Durable `NotificationStore` adapter | Approved durable store for notification records is not selected | — | 3 |
| TD-04 | CHANGE-AA-006 | Provider status-lookup reconciliation | Payment provider contract unresolved; the gateway is an in-process simulation | — | 3 |
| TD-05 | CHANGE-AA-007 | `outbox_events` migration for `order-service` | Schema-management tool and baseline for `ecommerce_orders` not established | `UNC-008` | 4 |
| TD-06 | CHANGE-AA-008 | `LeaseBackedOwnershipGuard` with fencing token | Approved ownership and fencing mechanism not selected | `EXT-001`, `EXT-002`, `EXT-003` | 5 |
| TD-07 | CHANGE-AA-013 | Cosmos throttling and timeout application to the effective client | Effective `spring-cloud-azure-starter-data-cosmos` 5.10.0 builder-customizer API | `UNC-016` | 3 |
| TD-08 | CHANGE-AA-021 | Reactive `SecurityWebFilterChain` for actuator | Spring Security classpath and reactive variant for `api-gateway` unverified | `UNC-006`, `UNC-010` | 3 |
| TD-09 | CHANGE-AA-022 | Explicit Key Vault client and rotation detection | No Key Vault SDK client exists; rotation mechanism is an architecture decision | `UNC-016` | 3 |

For each of these nine targets, Task Implementor validates the identified unresolved fact against the current repository and the approved decision, then produces the final implementation. Targeted discovery does not transfer report generation, finding creation, or priority assignment to Task Implementor.

### Cross-wave decision gates

| Gate | Blocks | Owner | Inputs | Note |
|---|---|---|---|---|
| `ownership_and_fencing` | CHANGE-AA-008, CHANGE-AA-009, CHANGE-AA-010 | Architecture governance | EXT-001, EXT-002, EXT-003, EXT-006, OQ-13 | `PROPERTY` mode can ship without this gate; `LEASE` mode cannot. |
| `durable_notification_store` | CHANGE-AA-004 | Architecture governance | OQ-06 | — |
| `order_schema_migration` | CHANGE-AA-007, CHANGE-AA-028 | Data platform | OQ-12, UNC-008 | — |
| `payment_provider_contract` | CHANGE-AA-006 reconciliation target | Product and payments | OQ-10 | — |
| `spring_cloud_azure_client_customization` | CHANGE-AA-002, CHANGE-AA-013, CHANGE-AA-022 | Engineering | OQ-02, UNC-016 | — |
| `management_endpoint_authorization` | CHANGE-AA-021 filter-chain target | Security | OQ-05, OQ-25, UNC-006, UNC-010 | — |
| `approved_numeric_budgets` | CHANGE-AA-013, CHANGE-AA-014, CHANGE-AA-015, CHANGE-AA-016, CHANGE-AA-017, CHANGE-AA-018, CHANGE-AA-027 | Engineering and operations | OQ-19 | Every proposed numeric default remains externally configurable; approval sets the deployed value, not the code. |

### Proposed test coverage

Step 3A proposes 72 tests against a repository that currently has zero. Tests inherit the priority of the behavior they prove; none is downgraded to P3 merely because it is a test.

| Priority | Proposed tests |
|---|---:|
| P0 | 29 |
| P1 | 29 |
| P2 | 10 |
| P3 | 4 |
| **Total** | **72** |

Nine modules gain a test tree. Coverage spans configuration and binding (14), messaging and delivery (12), concurrency and idempotency (11), resilience and isolation (9), ownership and scheduling (6), observability (6), health and readiness (5), supply chain and harness (5), and lifecycle and shutdown (4).

### Plan-level risks carried into implementation

| ID | Severity | Statement | Mitigation |
|---|---|---|---|
| R-01 | High | `UNC-006` records that the `common` module may still fail to compile. Every change depends on a building reactor, so an unresolved compile failure blocks the entire plan. | Resolve `UNC-006` as step 1 of Wave 1 validation. |
| R-02 | High | The Kafka operating scenario is policy-inferred, not architecture-confirmed. `CHANGE-AA-008` and `CHANGE-AA-009` implement an active-standby ownership model. | The `WorkloadOwnershipGuard` abstraction is scenario-neutral; only the guard implementation and activation policy would change, not listener, scheduler, or relay code. |
| R-03 | High | The transactional outbox introduces at-least-once delivery. Without `CHANGE-AA-025` and consumer-side deduplication, duplicate events would become **more** likely, not fewer. | `CHANGE-AA-025` is a declared prerequisite of `CHANGE-AA-007` and both sit in Wave 3. |
| R-04 | Medium | Several changes remove class-level `@Transactional` or change transaction boundaries in `OrderService` and `PaymentService`, affecting every method in those classes. | Method-by-method boundary review is an explicit acceptance activity for `CHANGE-AA-006` and `CHANGE-AA-007`. |
| R-05 | Medium | `UNC-008` records unresolved call-site and schema mismatches in `cart-service`, `payment-service`, and both Azure SQL DDL scripts while `ddl-auto` is `validate`. | Every proposal is labelled illustrative; Task Implementor validates repository state before editing. |
| R-06 | Medium | Making previously ignored timeouts and properties effective changes runtime behavior in ways current load profiles have never exercised, because zero tests exist today. | `CHANGE-AA-011` lands first so every behavioral change ships with a regression guard. |
| R-07 | Low | Repository-owned Kubernetes manifests are edited by `CHANGE-AA-003`, `CHANGE-AA-010`, and `CHANGE-AA-021`. `UNC-004` records that a second region's manifests may be maintained elsewhere. | Changes are limited to probe wiring, drain settings, and port exposure. If second-region manifests live outside this repository, the same edits must be mirrored there. |

### Step 4 approval boundary

Step 4 (Task Implementor) consumes the **authoritative Step 3A plan** at `.copilot-tracking/plans/2026-09-03/springboot-active-active-remediation-plan.md` and supports three approval selectors:

* `APPROVED_PRIORITIES`
* `APPROVED_WAVES`
* `APPROVED_CHANGE_IDS`

**Priorities are the preferred selector.** Step 4 resolves the selected priorities into a concrete change-ID set and **freezes those resolved change IDs before modifying any source code**.

Step 4 boundaries, carried unchanged from the Step 3A handoff contract:

* Re-inventory: **not allowed**
* Reassessment of controls: **not allowed**
* New findings: **not allowed**
* Severity, status, priority, or wave recalculation: **not allowed**
* Unrelated refactoring: **not allowed**
* Infrastructure changes: **not allowed**
* PCF changes: **not allowed**
* Source modification: **allowed** in Step 4 only
* Illustrative code as an authoritative patch: **no** — Task Implementor must validate current repository state and produce the final repository-specific implementation
* Deviations from the plan: **must be recorded**

Implementation preconditions: resolve `UNC-006` and confirm the reactor builds before starting any change; implement `CHANGE-AA-011` before any change whose acceptance criteria require an executing test.

This roadmap is report content only. It does not make Task Implementor responsible for generating this report.

[Back to Top](#top)

---

<!--
illustrative_code_conformance:
  applicable_targets: 110
  generated_code_blocks_rendered: 67
  targeted_discovery_targets_rendered: 9
  not_applicable_targets: 0
  invalid_generated_proposals: 0
  narrative_only_code_blocks_rendered: 0
  status: passed
  note: >
    Step 3A records 101 generated targets and 9 targeted-discovery targets across 33 changes.
    This report renders every one of the 9 targeted-discovery records in full, and renders the
    primary and materially distinct generated proposals for every finding (67 code blocks).
    The remaining generated targets are per-service repetitions of an already-rendered pattern
    (for example, the same Kafka budget block applied to the other six Kafka-using services, and
    the same digest-pinning edit applied to the other seven Dockerfiles) and the per-change
    acceptance-test classes. No proposal was summarised into prose, no narrative text was
    rendered inside a fenced block as if it were code, and no code was invented. The complete
    per-target proposal set remains authoritative in
    .copilot-tracking/plans/2026-09-03/springboot-active-active-remediation-plan.md Section 4.
-->

<!--
schema_conformance:
  schema_id: CODE-LEVEL-RESILIENCY-ASSESSMENT-REPORT
  schema_version: "1.2.0"
  schema_path: grounding/governance/assessment-report-schema.md
  schema_read_and_validated: true
  schema_lifecycle_status: active
  required_sections_present: true
  required_section_order_valid: true
  required_finding_fields_present: true
  summary_counts_reconcile: true
  finding_matrix_reconciles: true
  roadmap_matches_plan: true
  unsupported_findings_added: false
  priorities_changed: false
  severities_changed: false
  finding_status_changed: false
  infrastructure_findings_added: false
  pcf_findings_added: false
  report_written_by_step_3b: true
  delegated_to_task_implementor: false
  target_paths_present: true
  original_line_ranges_present: true
  original_source_excerpts_present: true
  original_source_matches_step_2: true
  illustrative_code_matches_step_3a: true
  original_and_proposed_code_separated: true
  invented_source_excerpts: false
  illustrative_code_status_present: true
  generated_proposals_contain_code: true
  narrative_only_code_blocks_rendered: false
  targeted_discovery_reasons_present: true
  invalid_generated_proposals: 0
  kafka_scenario_reported: true
  kafka_scenario_value: active_standby
  kafka_scenario_presented_as_confirmed: false
  back_to_top_links_present: true
  status: passed
-->

<!--
count_reconciliation:
  step_2_verified_findings: 33
  step_2_conditional_findings: 1
  step_2_total_findings: 34
  step_3a_approved_findings_total: 34
  step_3a_root_cause_changes_total: 33
  report_matrix_rows: 34
  report_summary_table_total: 34
  priority_distribution_findings: {P0: 12, P1: 13, P2: 5, P3: 4}
  priority_distribution_changes: {P0: 11, P1: 13, P2: 5, P3: 4}
  priority_distribution_changes_matches_step_3a: true
  consolidated_findings: 1
  consolidation: "F-005 (P0-008) consolidated under CHANGE-AA-007 with F-011 (P0-007) as primary"
  severity_distribution: {critical: 17, high: 15, medium: 1, low: 1}
  verified_controls_excluded_from_counts: 13
  not_assessed_controls_excluded: 24
  not_applicable_controls_excluded: 42
  accepted_risk_controls_excluded: 0
  pcf_findings: 0
  infrastructure_findings: 0
  wave_distribution: {"1": 4, "2": 12, "3": 11, "4": 6}
  priority_overrides: 0
  targeted_discovery_targets: 9
-->





