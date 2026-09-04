<!-- markdownlint-disable-file -->
<!--
report_governance:
  schema_id: CODE-LEVEL-RESILIENCY-ASSESSMENT-REPORT
  schema_version: "1.1.0"
  schema_path: grounding/governance/assessment-report-schema.md
  schema_validation: passed
  generated_by_phase: Step 3B
  artifact_type: assessment_documentation
  implementation_artifact: false
-->

<a id="top"></a>

# Code-Level Resiliency Assessment

| Report metadata | Value |
|---|---|
| Application | Ecommerce Platform |
| Assessment date | 2026-09-01 |
| Repository scope | `source/customer-app` |
| Current deployment | AKS; repository configuration identifies `westus` |
| Target deployment | Active-active application behavior; Kafka scenario provisionally active-standby |
| Language and framework | Java 17, Spring Boot 3.2.5 |
| Runtime platform | Azure Kubernetes Service (AKS) |
| Report version | 1.0 |

## Table of Contents

1. [Assessment Overview](#1-assessment-overview)
2. [Resiliency-Focused Recommendations](#2-resiliency-focused-recommendations)
3. [Non-Resiliency-Focused Recommendations](#3-non-resiliency-focused-recommendations)
4. [Repository and IaC Evidence Gap Analysis](#4-repository-and-iac-evidence-gap-analysis)
5. [Full Finding Matrix](#5-full-finding-matrix)
6. [Standards Alignment](#6-standards-alignment)
7. [Implementation Roadmap](#7-implementation-roadmap)

## 1. Assessment Overview

### Application and repository overview

The Ecommerce Platform is a Maven reactor containing a shared `common` library and eight Spring Boot microservices: API gateway, user, product, order, inventory, payment, cart, and notification. The services expose REST interfaces through Spring Cloud Gateway, consume and produce Kafka events, run scheduled inventory and cart work, and use Azure SQL, Azure Cosmos DB for NoSQL, Azure Managed Redis, Azure Key Vault, and SMTP through repository-observed application integrations.

Authoritative business state is split across Azure SQL for users, orders, and payments and Cosmos DB for product, inventory, and cart data. Notification history is held in a process-local map. Repository-owned configuration includes Maven builds, application YAML, eight Dockerfiles, Azure Pipelines configuration, and Kubernetes manifests. The repository contains no source-controlled tests, although Maven and CI declare test and coverage tooling.

The assessment is limited to application code, repository-owned configuration, and available test and delivery evidence. Deployed regional topology, service provisioning, network configuration, data replication, and platform operation remain external evidence. Their absence is not treated as infrastructure noncompliance.

### Repository-Observed Interactions

Repository evidence directly establishes Spring Cloud Gateway routes and REST controllers; Kafka listeners in inventory and notification services; Kafka producers in user, product, order, inventory, payment, and cart services; scheduled inventory and cart jobs; JPA access to Azure SQL; Cosmos repositories; Redis rate-limit and cache access; Key Vault property and CSI secret use; and SMTP delivery through `JavaMailSender`. Akamai, F5, Azure Application Gateway, API Management, downstream processors, and transitive state stores were not established as direct repository interactions.

### Supplied External Architecture Context

The supplied application context identifies the Ecommerce Platform as Java and Spring Boot on AKS, with a goal of correct active-active operation. It instructs the assessment to assume shared services comply with enterprise resiliency standards and excludes infrastructure assessment. No approved application-architecture or solution-architecture context with an ID, version, owner, lifecycle status, Kafka topology, or promotion contract was supplied.

### Kafka Operating Scenario

* **Scenario:** Active-Standby
* **Processing model:** Hybrid producer, consumer, and scheduler
* **Regional processing model:** Single active, pending architecture confirmation
* **External side effects:** Email delivery, shared-state mutation, and event publication
* **Kafka-backed state:** Not established; offsets and replication are externally owned
* **Scenario source:** Inferred from repository-observed dependencies
* **Context ID:** Not provided
* **Context version:** Not provided
* **Policy:** `KAFKA-OPERATING-SCENARIO` version `3.0.0`
* **Policy rule:** `KAFKA-SCENARIO-001`
* **Policy validation:** Inferred and consistent with authoritative Azure SQL use
* **Repository compatibility:** Consistent
* **Architecture confirmation required:** Yes
* **Kafka topology:** Not provided
* **Stretched cluster:** Not established
* **Authoritative state alignment:** Azure SQL authoritative state requires active-standby alignment

Scenario-specific findings `F-008` through `F-010` remain conditional until approved architecture evidence confirms the cluster model, promotion sequence, offset synchronization, ownership authority, fencing, and failback contract.

### Assessment themes

* Regional determinism is not established because repository defaults can select one region's endpoints and labels, and runtime base images are mutable (`F-001`, `F-011`; verified).
* Required state and cross-store work are not durable across pod or regional movement (`F-003`, `F-007`; verified).
* Kafka and scheduled workloads lack observable, fenced ownership and recoverable completion semantics (`F-008` through `F-010`, `F-012`; `F-012` verified and Kafka scenario findings conditional).
* SQL and gateway calls lack complete deadline, isolation, and retry budgets (`F-002`, `F-005`, `F-006`; verified).
* Operational health details are exposed more broadly than required (`F-004`; verified, non-resiliency-focused).

### Approved shared-service and reference architectures

The governance schema supplies the following approved references applicable to observed services. The dependency registry supplies standards mappings but no additional customer-specific architecture links.

| Azure Shared Service | Link to Reference Architecture |
|---|---|
| Azure Key Vault | [Reference](https://rxsafeway.sharepoint.com/:w:/r/sites/Cloud2.0/Shared%20Documents/I11%20Resiliency%20Program/Discovery/Cloud%20Foundation/Design/Albertsons%20Azure%20Key%20Vault%20Architecture%20Design%20Proposal.docx?d=wf1abecab2812460a8cadd6e5956d5bb8&csf=1&web=1&e=yzvvQh) |
| Kafka | [Reference](https://rxsafeway.sharepoint.com/:w:/r/sites/Cloud2.0/Shared%20Documents/I11%20Resiliency%20Program/Discovery/Integration%20Platform/Kafka/Approved_Albertsons_RegionResiliency_Kafka-MultiRegion.docx?d=w08142308135244de855f4dab4c49ca2d&csf=1&web=1&e=kueuJ9) |
| Azure SQL Database | [Reference](https://rxsafeway.sharepoint.com/:f:/r/sites/Cloud2.0/Shared%20Documents/I11%20Resiliency%20Program/Discovery/Database%20Platform/SQL%20DB?csf=1&web=1&e=xMauSY) |
| Azure Cosmos DB | [Reference](https://rxsafeway.sharepoint.com/:w:/r/sites/Cloud2.0/Shared%20Documents/I11%20Resiliency%20Program/Discovery/Database%20Platform/Cosmos/Albertsons_Architecture_Design_MongoDB_RU_v1.0.docx?d=wa68893488e094fef9b5506690c685847&csf=1&web=1&e=YDVc7g) |
| Azure Managed Redis | [Reference](https://rxsafeway.sharepoint.com/:w:/r/sites/Cloud2.0/Shared%20Documents/I11%20Resiliency%20Program/Discovery/Database%20Platform/Redis/Design/Managed%20Redis%20-%20Albertsons%20Multi-Region%20Design%20v3.docx?d=wad90acec4c154b2498d899a2ffcdc9d4&csf=1&web=1&e=L7pVbQ) |
| Azure Kubernetes Service (AKS) | [Reference](https://rxsafeway.sharepoint.com/:w:/r/sites/Cloud2.0/Shared%20Documents/I11%20Resiliency%20Program/Discovery/Container%20Platform/Design/Albertsons%20Architecture%20Design_AKS%20and%20Istio_v1.0.docx?d=w97c0edfea59d466e80af843958d95c5c&csf=1&web=1&e=7UJSQS) |

### Summary findings table

| Priority | Section | Confirmed count | Description |
|---|---:|---:|---|
| P0 | Resiliency-focused | 4 | Regional configuration, durable state, SQL/Kafka reconciliation, and scheduled ownership |
| P0 | Resiliency-focused conditional | 1 | Kafka active-standby ownership, pending architecture confirmation |
| P0 | Non-resiliency-focused | 1 | Immutable runtime image identity |
| P1 | Resiliency-focused | 3 | SQL deadlines, HTTP dependency isolation, and retry classification |
| P2 | Resiliency-focused conditional | 2 | Kafka consumer and producer completion semantics |
| P3 | Non-resiliency-focused | 1 | Health-detail disclosure |
| Total | All approved findings | 12 | 9 confirmed and 3 conditional findings |

> **IMPORTANT:** Hard numbers used for retry counts, timeout settings, interval timings, thread-pool sizes, cache duration, health thresholds, and circuit-breaker settings are examples unless the authoritative plan identifies an approved value. These values must be externally configurable and coordinated with application, mesh, gateway, and load-balancer budgets. All code snippets are illustrative proposals, not applied or prescriptive patches.

[Back to Top](#top)

## 2. Resiliency-Focused Recommendations

### P0 Critical Immediate Action

#### Regional Configuration

#### P0-001: Hardcoded regional defaults prevent safe reuse of one artifact

**Priority: P0 - Active-active deployment or traffic-eligibility blocker**

**Priority policy:** `AA-REMEDIATION-PRIORITY` version `1.0.0`, rule `P0-AA-001`.

**Severity:** Critical

**Resiliency Related:** Yes

**Finding status:** Verified finding (`non_compliant`)

**Issue:** Production-capable defaults pin Kafka, Key Vault, telemetry, SMTP, and frontend values to one physical or named region.

**What does this solve:** Requiring deployment-injected values allows one immutable artifact to select the correct regional dependencies and telemetry identity.

**Resiliency Impact:** A second-region instance can otherwise connect to the wrong dependency or emit misleading regional telemetry.

**Recommended Fix:** Remove production-capable regional fallbacks, validate required production values, and retain explicit local-only defaults in a local profile.

**Repository evidence:** `EV-F-001-01` is primary; `EV-F-001-02` and `EV-F-001-03` support the same root cause.

**Target file and location:** Repository path `source/customer-app/notification-service/src/main/resources/application.yml`; symbols `spring.kafka.bootstrap-servers`, `spring.cloud.azure.keyvault.secret.endpoint`, and `management.metrics.tags.region`; original lines 9, 41, and 64; change `CHANGE-AA-001`.

**Original source requiring update:**

```yaml
bootstrap-servers: ${KAFKA_BOOTSTRAP_SERVERS:ecommerce-kafka.westus.azure.com:9093}
endpoint: https://ecommerce-keyvault.vault.azure.net/
region: westus
```

**Illustrative proposed implementation:**

> Illustrative proposal only.

```yaml
spring:
  kafka:
    bootstrap-servers: ${KAFKA_BOOTSTRAP_SERVERS}
  cloud.azure.keyvault.secret.endpoint: ${AZURE_KEYVAULT_ENDPOINT}
management.metrics.tags.region: ${APP_REGION}
```

**Validation requirements:** Verify two regional configurations resolve distinct endpoints and labels, missing production values fail startup, and the local profile remains usable.

**Dependencies:** Confirm the canonical deployment-supplied region property name; targeted implementation discovery must enumerate inventory-cited service configuration.

**Notes:**

* Cross-refs: `F-001`, `APP-AA-002`, `APP-AA-015`, `KV-001`, `KAFKA-001`, `CHANGE-AA-001`
* Implementation: Preserve explicit local-profile defaults only
* Validation: Run module-scoped tests and Maven verification for API gateway and notification service
* Guardrail: Do not hardcode physical region names or modify infrastructure

<span style="font-size: 14px;">**MSFT Reference:** [Azure Key Vault reference architecture](https://rxsafeway.sharepoint.com/:w:/r/sites/Cloud2.0/Shared%20Documents/I11%20Resiliency%20Program/Discovery/Cloud%20Foundation/Design/Albertsons%20Azure%20Key%20Vault%20Architecture%20Design%20Proposal.docx?d=wf1abecab2812460a8cadd6e5956d5bb8&csf=1&web=1&e=yzvvQh)</span>

---

#### State and Cross-Store Consistency

#### P0-002: Notification history is process-local state

**Priority: P0 - Active-active deployment or traffic-eligibility blocker**

**Priority policy:** `AA-REMEDIATION-PRIORITY` version `1.0.0`, rule `P0-AA-005`.

**Severity:** Critical

**Resiliency Related:** Yes

**Finding status:** Verified finding (`non_compliant`)

**Issue:** Required notification history is held only in a process-local `ConcurrentHashMap`.

**What does this solve:** A durable repository makes history consistent across instances and persistent across restarts.

**Resiliency Impact:** Requests moved between pods or regions can observe different or missing history.

**Recommended Fix:** Introduce a repository port and an architecture-approved durable adapter with stable record identity and concurrency behavior.

**Repository evidence:** `EV-F-003-01` directly establishes process-local storage.

**Target file and location:** `source/customer-app/notification-service/src/main/java/com/ecommerce/notification/repository/NotificationRepository.java`; symbol `NotificationRepository.store`; line 18; change `CHANGE-AA-003`.

**Original source requiring update:**

```java
private final Map<String, NotificationRecord> store = new ConcurrentHashMap<>();
```

**Illustrative proposed implementation:**

> Illustrative proposal only.

```java
public interface NotificationHistoryRepository {
    NotificationRecord save(NotificationRecord record);
    List<NotificationRecord> findByCustomerId(String customerId);
}
```

**Validation requirements:** Write through instance A, read through instance B, restart both, and verify stable identity prevents duplicate records.

**Dependencies:** Architecture approval of an existing durable store and product decisions for retention and read consistency.

**Notes:**

* Cross-refs: `F-003`, `APP-AA-010`, `CHANGE-AA-003`
* Implementation: Store-specific code remains intentionally unspecified
* Validation: Add cross-instance persistence and restart tests
* Guardrail: Do not silently fall back to process-local state

<span style="font-size: 14px;">**MSFT Reference:** Not provided</span>

---

#### P0-003: SQL order state and Kafka events can diverge

**Priority: P0 - Active-active deployment or traffic-eligibility blocker**

**Priority policy:** `AA-REMEDIATION-PRIORITY` version `1.0.0`, rule `P0-AA-006`.

**Severity:** Critical

**Resiliency Related:** Yes

**Finding status:** Verified finding (`non_compliant`)

**Issue:** Order state is committed before Kafka publication without durable intent, terminal status, or reconciliation.

**What does this solve:** A transactional outbox makes partial SQL/Kafka completion recoverable without repeating the business transition.

**Resiliency Impact:** Process or broker failure can leave authoritative order state without its required event, while retry can repeat publication.

**Recommended Fix:** Commit a stable event identity and outbox row with the order transaction, then publish asynchronously with bounded retries and terminal status.

**Repository evidence:** `EV-F-007-01` establishes save-before-publish ordering.

**Target file and location:** `source/customer-app/order-service/src/main/java/com/ecommerce/order/service/OrderService.java`; symbol `createOrder`; lines 100-105; change `CHANGE-AA-007`.

**Original source requiring update:**

```java
OrderEntity savedOrder = orderRepository.save(order);
log.info("Order created: {} for customer: {}", orderNumber, customerId);

// Publish ORDER_CREATED event to trigger inventory reservation & payment
publishOrderEvent(KafkaTopics.ORDER_CREATED, savedOrder, "Order created");
```

**Illustrative proposed implementation:**

> Illustrative proposal only.

```java
OrderEntity saved = orderRepository.save(order);
outboxRepository.save(OrderOutbox.pending(stableEventId, KafkaTopics.ORDER_CREATED, saved));
return mapToOrderResponse(saved);
```

**Validation requirements:** Fail after SQL commit and before or during send, run concurrent dispatchers, and verify one logical event with durable recovery status.

**Dependencies:** Approve outbox retention, terminal failure, replay, and operational reconciliation contracts.

**Notes:**

* Cross-refs: `F-007`, `SQL-013`, `APP-STATE-001`, `APP-DB-003`, `CHANGE-AA-007`
* Implementation: Use existing JPA transaction semantics and preserve payload compatibility
* Validation: Include failure-after-commit and dispatcher-concurrency integration tests
* Guardrail: Do not claim a SQL transaction can atomically include Kafka

<span style="font-size: 14px;">**MSFT Reference:** [Azure SQL Database reference architecture](https://rxsafeway.sharepoint.com/:f:/r/sites/Cloud2.0/Shared%20Documents/I11%20Resiliency%20Program/Discovery/Database%20Platform/SQL%20DB?csf=1&web=1&e=xMauSY)</span>

---

#### Kafka and Scheduler Ownership

#### P0-004: Active-standby Kafka work is not role-gated or fenced

**Priority: P0 - Active-active deployment or traffic-eligibility blocker**

**Priority policy:** `AA-REMEDIATION-PRIORITY` version `1.0.0`, rule `P0-AA-006`.

**Severity:** Critical

**Resiliency Related:** Yes

**Finding status:** Conditional finding (`non_compliant` under inferred active-standby scenario)

**Condition and evidence required:** GOV-001 must confirm approved active-standby architecture, cluster and replication model, promotion order, offset synchronization, ownership authority, and failback contract.

**Issue:** Kafka listeners and scheduled producers start through unconditional annotations with no regional owner check or stale-owner fence.

**What does this solve:** Fail-closed ownership and epoch fencing prevent both-active, stale-active, and role-misaligned processing.

**Resiliency Impact:** Under the inferred scenario, both regions can acquire or produce authoritative work and a stale active can continue after transfer.

**Recommended Fix:** After architecture confirmation, coordinate listener and scheduler lifecycle with an approved ownership provider and reject stale writes by fencing token.

**Repository evidence:** `EV-F-008-01` is primary and `EV-F-008-02` supports unconditional scheduler activation.

**Target file and location:** `source/customer-app/inventory-service/src/main/java/com/ecommerce/inventory/service/InventoryService.java`; symbols `handleOrderCreated` and `expireOldReservations`; lines 250-252 and 268-269; change `CHANGE-AA-008`.

**Original source requiring update:**

```java
@KafkaListener(topics = KafkaTopics.ORDER_CREATED, groupId = KafkaTopics.GROUP_INVENTORY_SERVICE)
public void handleOrderCreated(Map<String, Object> event) {
    log.info("Processing ORDER_CREATED event for order: {}", event.get("orderId"));

@Scheduled(fixedDelay = 300000) // Every 5 minutes
public void expireOldReservations() {
```

**Illustrative proposed implementation:**

> Illustrative proposal only.

```java
if (!ownership.current().permitsWork(fencingToken)) {
    throw new StaleWorkloadOwnerException();
}
listenerRegistry.getListenerContainer(listenerId).start();
```

**Validation requirements:** Exercise active, standby, both-active, both-inactive, stale-owner, ownership loss, promotion, and failback states.

**Dependencies:** `CHANGE-AA-001` and GOV-001 architecture confirmation; the ownership provider must be approved before implementation.

**Notes:**

* Cross-refs: `F-008`, `KAFKA-AS-001`, `KAFKA-AS-003`, `KAFKA-AS-007`, `KAFKA-012`, `CHANGE-AA-008`
* Implementation: Default ownership to inactive and expose owner and epoch safely
* Validation: Verify only the current fenced owner acquires work
* Guardrail: A property flag alone is not split-brain protection

<span style="font-size: 14px;">**MSFT Reference:** [Kafka reference architecture](https://rxsafeway.sharepoint.com/:w:/r/sites/Cloud2.0/Shared%20Documents/I11%20Resiliency%20Program/Discovery/Integration%20Platform/Kafka/Approved_Albertsons_RegionResiliency_Kafka-MultiRegion.docx?d=w08142308135244de855f4dab4c49ca2d&csf=1&web=1&e=kueuJ9)</span>

---

#### P0-006: Scheduled shared-state work has no distributed claim

**Priority: P0 - Active-active deployment or traffic-eligibility blocker**

**Priority policy:** `AA-REMEDIATION-PRIORITY` version `1.0.0`, rule `P0-AA-006`.

**Severity:** Critical

**Resiliency Related:** Yes

**Finding status:** Verified finding (`non_compliant`)

**Issue:** Every instance scans and mutates shared state or publishes events without a durable lease, atomic claim, or fencing epoch.

**What does this solve:** Per-item durable claims prevent duplicate mutation and allow safe takeover of abandoned work.

**Resiliency Impact:** Multiple pods and regions can process the same reservation, cart, or alert concurrently.

**Recommended Fix:** After regional ownership gating, atomically claim each logical item in its authoritative store and record owner, epoch, attempt, expiry, completion, and recovery state.

**Repository evidence:** `EV-F-012-01` is primary and `EV-F-012-02` establishes a second unconditional schedule.

**Target file and location:** `source/customer-app/inventory-service/src/main/java/com/ecommerce/inventory/service/InventoryService.java`; symbol `expireOldReservations`; lines 268-287; change `CHANGE-AA-012`.

**Original source requiring update:**

```java
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
```

**Illustrative proposed implementation:**

> Illustrative proposal only.

```java
claimRepository.tryClaim(itemId, ownerId, fencingEpoch, leaseUntil)
    .ifPresent(claim -> processAndComplete(claim));
```

**Validation requirements:** Run two pods and two region identities concurrently, expire a lease, crash after claim, and verify recovery, stale-owner rejection, and duplicate prevention.

**Dependencies:** `CHANGE-AA-008`; approve claim granularity, lease budget, and existing-store claim location.

**Notes:**

* Cross-refs: `F-012`, `APP-SCHED-001`, `APP-SCHED-002`, `APP-WORKLOAD-001`, `CHANGE-AA-012`
* Implementation: Prefer conditional writes in an existing authoritative store
* Validation: Prove exactly one valid fenced owner per logical item
* Guardrail: Do not add an infrastructure service or rely on an unfenced lease

<span style="font-size: 14px;">**MSFT Reference:** [Azure Cosmos DB reference architecture](https://rxsafeway.sharepoint.com/:w:/r/sites/Cloud2.0/Shared%20Documents/I11%20Resiliency%20Program/Discovery/Database%20Platform/Cosmos/Albertsons_Architecture_Design_MongoDB_RU_v1.0.docx?d=wa68893488e094fef9b5506690c685847&csf=1&web=1&e=YDVc7g)</span>

### P1 High Priority

#### Database Resilience

#### P1-001: Azure SQL operations lack a complete bounded timeout budget

**Priority: P1 - Failure-amplification or recovery blocker**

**Priority policy:** `AA-REMEDIATION-PRIORITY` version `1.0.0`, rule `P1-RCV-001`.

**Severity:** Critical

**Resiliency Related:** Yes

**Finding status:** Verified finding (`non_compliant`)

**Issue:** Login and pool acquisition are bounded, but socket, statement, lock, transaction, and complete caller deadlines are not established.

**What does this solve:** A coordinated deadline hierarchy prevents SQL calls from retaining request threads and pool capacity beyond the regional drain budget.

**Resiliency Impact:** Database calls can outlive request or failover budgets during regional interruption.

**Recommended Fix:** Bind all timeout layers to approved external properties and enforce transaction deadlines below the caller budget without blind transaction retry.

**Repository evidence:** `EV-F-002-01` establishes the partial datasource budget.

**Target file and location:** `source/customer-app/order-service/src/main/resources/application.yml`; symbol `spring.datasource`; lines 8-17; change `CHANGE-AA-002`.

**Original source requiring update:**

```yaml
datasource:
  url: jdbc:sqlserver://${AZURE_SQL_HOST:localhost}:1433;databaseName=${AZURE_SQL_DB:ecommerce_orders};encrypt=true;trustServerCertificate=false;loginTimeout=30;
  username: ${AZURE_SQL_USERNAME:${azure-sql-username}}
  password: ${AZURE_SQL_PASSWORD:${azure-sql-password}}
  driver-class-name: com.microsoft.sqlserver.jdbc.SQLServerDriver
  hikari:
    connection-timeout: 20000
    minimum-idle: 5
    maximum-pool-size: 20
```

**Illustrative proposed implementation:**

> Illustrative proposal only.

```yaml
spring:
  datasource:
    url: jdbc:sqlserver://${AZURE_SQL_HOST}:1433;databaseName=${AZURE_SQL_DB};loginTimeout=${SQL_LOGIN_TIMEOUT_SECONDS};socketTimeout=${SQL_SOCKET_TIMEOUT_MILLIS}
  jpa.properties.jakarta.persistence.query.timeout: ${SQL_QUERY_TIMEOUT_MILLIS}
  transaction.default-timeout: ${SQL_TRANSACTION_TIMEOUT_SECONDS}
```

**Validation requirements:** Delay acquisition, connection, statement, lock, and commit separately and assert each terminates within its configured layer and overall budget.

**Dependencies:** Approved caller, traffic-drain, SQL, transaction, and lock budgets; validate driver property names for the managed version.

**Notes:**

* Cross-refs: `F-002`, `SQL-002`, `APP-AA-004`, `CHANGE-AA-002`
* Implementation: Externalize every value and validate timeout ordering
* Validation: Use integration-level driver and pool fault tests
* Guardrail: Do not prescribe unevidenced production values or add blind retries

<span style="font-size: 14px;">**MSFT Reference:** [Azure SQL Database reference architecture](https://rxsafeway.sharepoint.com/:f:/r/sites/Cloud2.0/Shared%20Documents/I11%20Resiliency%20Program/Discovery/Database%20Platform/SQL%20DB?csf=1&web=1&e=xMauSY)</span>

---

#### HTTP Client Resilience

#### P1-002: Gateway dependencies share one HTTP client timeout and pool profile

**Priority: P1 - Failure-amplification or recovery blocker**

**Priority policy:** `AA-REMEDIATION-PRIORITY` version `1.0.0`, rule `P1-RCV-003`.

**Severity:** High

**Resiliency Related:** Yes

**Finding status:** Verified finding (`non_compliant`)

**Issue:** Materially different downstream services share one timeout and connection-resource profile.

**What does this solve:** Dependency-specific bounded pools, concurrency, deadlines, and telemetry isolate saturation and slow failures.

**Resiliency Impact:** One degraded dependency can consume capacity required by unrelated routes.

**Recommended Fix:** Use supported Spring Cloud Gateway and Reactor Netty extension points to define named bounded dependency profiles.

**Repository evidence:** `EV-F-005-01` establishes the shared profile.

**Target file and location:** `source/customer-app/api-gateway/src/main/resources/application.yml`; symbol `spring.cloud.gateway.httpclient`; lines 30-33; change `CHANGE-AA-005`.

**Original source requiring update:**

```yaml
httpclient:
  connect-timeout: 5000
  response-timeout: 30s
```

**Illustrative proposed implementation:**

> Illustrative proposal only.

```java
ConnectionProvider provider = ConnectionProvider.builder(dependencyName)
    .maxConnections(properties.maxConnections())
    .pendingAcquireTimeout(properties.acquireTimeout())
    .build();
```

**Validation requirements:** Saturate one downstream route and verify unrelated routes retain bounded latency and capacity with dependency-specific metrics.

**Dependencies:** Approved route latency and concurrency budgets; validate supported Spring Cloud 2023.0.1 APIs.

**Notes:**

* Cross-refs: `F-005`, `APP-HTTP-002`, `HTTP-003`, `CHANGE-AA-005`
* Implementation: Use supported Gateway customizer or filter APIs
* Validation: Include saturation and resource-isolation tests
* Guardrail: Keep all capacity and timeout values externally configurable

<span style="font-size: 14px;">**MSFT Reference:** Not provided</span>

---

#### P1-003: Gateway retry classification ignores server guidance

**Priority: P1 - Failure-amplification or recovery blocker**

**Priority policy:** `AA-REMEDIATION-PRIORITY` version `1.0.0`, rule `P1-RCV-002`.

**Severity:** High

**Resiliency Related:** Yes

**Finding status:** Verified finding (`non_compliant`)

**Issue:** The product GET route retries only 503 responses with configured backoff and does not process `Retry-After`.

**What does this solve:** Response-aware classification avoids premature or excessive retries during throttling and controlled recovery.

**Resiliency Impact:** Existing behavior can retry at the wrong time, omit approved transient failures, or exceed the route deadline.

**Recommended Fix:** Retry only idempotent GET failures classified as transient, honor capped `Retry-After`, add jitter, and enforce one total deadline.

**Repository evidence:** `EV-F-006-01` establishes current retry classification and backoff.

**Target file and location:** `source/customer-app/api-gateway/src/main/java/com/ecommerce/gateway/config/GatewayRoutesConfig.java`; symbol `customRouteLocator product-service-public retry`; lines 73-77; change `CHANGE-AA-006`.

**Original source requiring update:**

```java
.retry(config -> config
    .setRetries(3)
    .setStatuses(org.springframework.http.HttpStatus.SERVICE_UNAVAILABLE)
    .setBackoff(Duration.ofMillis(100), Duration.ofMillis(1000), 2, true))
```

**Illustrative proposed implementation:**

> Illustrative proposal only.

```java
return exchange(chain, exchange).retryWhen(
    Retry.withThrowable(throwable -> retryPolicy.transientFailure(throwable))
).timeout(retryPolicy.totalBudget());
```

**Validation requirements:** Exercise 429 and 503 with valid, absent, malformed, and excessive `Retry-After`, transport failures, terminal 4xx, and the total deadline.

**Dependencies:** `CHANGE-AA-005`; approve transient classifications, maximum server-directed delay, and route deadline.

**Notes:**

* Cross-refs: `F-006`, `APP-HTTP-003`, `HTTP-004`, `CHANGE-AA-006`
* Implementation: Preserve GET-only retry scope
* Validation: Verify terminal and ambiguous operations are never retried
* Guardrail: Follow Gateway buffer and response lifecycle APIs

<span style="font-size: 14px;">**MSFT Reference:** Not provided</span>

### P2 Moderate Priority

#### Kafka Completion Semantics

#### P2-001: Kafka consumer side-effect failures are converted to successful returns

**Priority: P2 - Data-correctness or processing-resilience gap**

**Priority policy:** `AA-REMEDIATION-PRIORITY` version `1.0.0`, rule `P2-DATA-002`.

**Severity:** Critical

**Resiliency Related:** Yes

**Finding status:** Conditional finding (`non_compliant` under inferred active-standby scenario)

**Condition and evidence required:** GOV-001 must confirm the Kafka operating model; channel idempotency and quarantine retention also require approval.

**Issue:** Notification listeners catch side-effect failures, log them, and return normally.

**What does this solve:** Coupling listener completion to successful side effect or durable retry intent prevents failed work from disappearing.

**Resiliency Impact:** The container can advance records after failed email or notification work, making recovery incomplete.

**Recommended Fix:** Propagate retryable failures to a finite error handler and quarantine exhausted records with stable identity, or durably record retry work before returning success.

**Repository evidence:** `EV-F-009-01` establishes swallowed channel failures.

**Target file and location:** `source/customer-app/notification-service/src/main/java/com/ecommerce/notification/service/NotificationEventConsumer.java`; symbol `handleOrderCreated`; lines 45-50; change `CHANGE-AA-009`.

**Original source requiring update:**

```java
try {
    emailService.sendOrderConfirmation(customerEmail, orderNumber, total.toString());
    saveNotification(customerId, "ORDER_CREATED", "Order Confirmation",
            "Your order " + orderNumber + " has been placed successfully.", "EMAIL");
} catch (Exception e) {
    log.error("Failed to send order confirmation email: {}", e.getMessage());
}
```

**Illustrative proposed implementation:**

> Illustrative proposal only.

```java
emailService.sendOrderConfirmation(customerEmail, orderNumber, total.toString());
notificationRepository.save(customerId, type, title, message, channel);
// Let retryable failures escape to the configured finite error handler.
```

**Validation requirements:** Force each channel to fail and verify no premature commit, finite retry, quarantine, successful redelivery, and recovery.

**Dependencies:** `CHANGE-AA-003`, `CHANGE-AA-008`, approved channel idempotency, and quarantine retention.

**Notes:**

* Cross-refs: `F-009`, `KAFKA-004`, `APP-KAFKA-002`, `CHANGE-AA-009`
* Implementation: Listener success must mean side effect or durable retry intent succeeded
* Validation: Prove offsets do not irrecoverably advance on failure
* Guardrail: Direct email redelivery requires stable provider or durable idempotency

<span style="font-size: 14px;">**MSFT Reference:** [Kafka reference architecture](https://rxsafeway.sharepoint.com/:w:/r/sites/Cloud2.0/Shared%20Documents/I11%20Resiliency%20Program/Discovery/Integration%20Platform/Kafka/Approved_Albertsons_RegionResiliency_Kafka-MultiRegion.docx?d=w08142308135244de855f4dab4c49ca2d&csf=1&web=1&e=kueuJ9)</span>

---

#### P2-002: Kafka producer completion is not observed

**Priority: P2 - Data-correctness or processing-resilience gap**

**Priority policy:** `AA-REMEDIATION-PRIORITY` version `1.0.0`, rule `P2-DATA-002`.

**Severity:** Critical

**Resiliency Related:** Yes

**Finding status:** Conditional finding (`non_compliant` under inferred active-standby scenario)

**Condition and evidence required:** GOV-001 must confirm the Kafka operating model; durable publication status and quarantine policy require approval.

**Issue:** The scheduled cart producer discards the send future and logs publication before broker completion.

**What does this solve:** Observing bounded send completion and persisting outcome makes asynchronous rejection recoverable with stable event identity.

**Resiliency Impact:** Broker rejection or timeout can lose an event while the schedule reports success.

**Recommended Fix:** Compose or await send completion within an external deadline and persist claim, event identity, attempt, and terminal outcome.

**Repository evidence:** `EV-F-010-01` establishes fire-and-forget publication.

**Target file and location:** `source/customer-app/cart-service/src/main/java/com/ecommerce/cart/service/CartService.java`; symbol `detectAbandonedCarts`; lines 217-228; change `CHANGE-AA-010`.

**Original source requiring update:**

```java
kafkaTemplate.send(KafkaTopics.CART_ABANDONED, cart.getCustomerId(), Map.of(
    "cartId", cart.getId(),
    "customerId", cart.getCustomerId(),
    "guestEmail", cart.getGuestEmail() != null ? cart.getGuestEmail() : "",
    "cartTotal", cart.getEstimatedTotal() != null ? cart.getEstimatedTotal() : BigDecimal.ZERO,
    "itemCount", cart.getTotalItems(),
    "abandonedAt", LocalDateTime.now().toString(),
    "lastActivityAt", cart.getLastActivityAt() != null ? cart.getLastActivityAt().toString() : ""
));
log.info("Cart abandonment event published for customer: {}", cart.getCustomerId());
```

**Illustrative proposed implementation:**

> Illustrative proposal only.

```java
kafkaTemplate.send(topic, key, payload)
    .orTimeout(properties.sendTimeout().toMillis(), TimeUnit.MILLISECONDS)
    .whenComplete((result, error) -> publicationStore.recordOutcome(eventId, error));
```

**Validation requirements:** Simulate asynchronous rejection and timeout, retry with the same event ID, quarantine exhaustion, and verify no premature success log.

**Dependencies:** `CHANGE-AA-008`, `CHANGE-AA-012`, approved durable publication status, and quarantine policy.

**Notes:**

* Cross-refs: `F-010`, `APP-KAFKA-005`, `KAFKA-002`, `CHANGE-AA-010`
* Implementation: Prefer composition; block only within a small approved scheduler bound
* Validation: Record success only after broker acknowledgment
* Guardrail: Retries must preserve logical event identity

<span style="font-size: 14px;">**MSFT Reference:** [Kafka reference architecture](https://rxsafeway.sharepoint.com/:w:/r/sites/Cloud2.0/Shared%20Documents/I11%20Resiliency%20Program/Discovery/Integration%20Platform/Kafka/Approved_Albertsons_RegionResiliency_Kafka-MultiRegion.docx?d=w08142308135244de855f4dab4c49ca2d&csf=1&web=1&e=kueuJ9)</span>

[Back to Top](#top)

## 3. Non-Resiliency-Focused Recommendations

### P0 Critical Immediate Action

#### Supply Chain

#### P0-005: Runtime image is mutable by tag

**Priority: P0 - Active-active deployment or traffic-eligibility blocker**

**Priority policy:** `AA-REMEDIATION-PRIORITY` version `1.0.0`, rule `P0-AA-001`.

**Severity:** High

**Resiliency Related:** No

**Finding status:** Verified finding (`non_compliant`)

**Issue:** The Java runtime base image uses a mutable tag without a digest.

**What does this solve:** Digest pinning makes regional builds, rebuilds, and rollback inputs reproducible.

**Impact:** Two delivery paths can resolve different runtime contents despite identical Dockerfiles.

**Recommended Fix:** Pin all eight runtime stages to one security-approved Java 17 image digest and update it through dependency maintenance.

**Repository evidence:** `EV-F-011-01` establishes tag-only runtime identity.

**Target file and location:** `source/customer-app/api-gateway/Dockerfile`; symbol `runtime FROM`; line 42; change `CHANGE-AA-011`.

**Original source requiring update:**

```dockerfile
FROM eclipse-temurin:17-jre-jammy
```

**Illustrative proposed implementation:**

> Illustrative proposal only.

```dockerfile
ARG RUNTIME_IMAGE_DIGEST
FROM eclipse-temurin:17-jre-jammy@${RUNTIME_IMAGE_DIGEST}
```

**Validation requirements:** Build every service, inspect the resolved base digest in both delivery paths, and run image policy and vulnerability checks.

**Dependencies:** Security owner approval of the exact digest and targeted confirmation of all service Dockerfiles.

**Notes:**

* Cross-refs: `F-011`, `APP-SUPPLY-002`, `CHANGE-AA-011`
* Implementation: Pin the same approved digest in every runtime stage
* Validation: Compare resolved image identity across builds
* Guardrail: Never use a placeholder, invented, or stale digest

<span style="font-size: 14px;">**MSFT Reference:** Not provided</span>

### P3 Optimization

#### Management Security

#### P3-001: Health details are exposed unconditionally

**Priority: P3 - Operational-maturity or verification gap**

**Priority policy:** `AA-REMEDIATION-PRIORITY` version `1.0.0`, rule `P3-OPS-005`.

**Severity:** Medium

**Resiliency Related:** No

**Finding status:** Verified finding (`non_compliant`)

**Issue:** Gateway and order-service health details are configured as always visible.

**What does this solve:** Authorized detail access preserves operator diagnostics while removing dependency and topology disclosure from anonymous callers.

**Impact:** Untrusted callers can receive component details during normal operation and degradation.

**Recommended Fix:** Set health details to `when-authorized` and preserve minimal liveness and readiness responses.

**Repository evidence:** `EV-F-004-01` directly establishes unconditional detail visibility.

**Target file and location:** `source/customer-app/api-gateway/src/main/resources/application.yml`; symbol `management.endpoint.health.show-details`; line 127; change `CHANGE-AA-004`.

**Original source requiring update:**

```yaml
show-details: always
```

**Illustrative proposed implementation:**

> Illustrative proposal only.

```yaml
management.endpoint.health.show-details: when-authorized
```

**Validation requirements:** Compare anonymous and authorized health responses and confirm liveness and readiness status behavior remains correct.

**Dependencies:** Confirm the operator authority used for Actuator detail access.

**Notes:**

* Cross-refs: `F-004`, `APP-ACT-003`, `CHANGE-AA-004`
* Implementation: Coordinate authorization with existing Spring Security conventions
* Validation: Test anonymous probes and authorized operational access
* Guardrail: Do not expose protected values through health details

<span style="font-size: 14px;">**MSFT Reference:** Not provided</span>

### Verified controls

The authoritative review identifies six evidence-backed compliant controls. They are excluded from finding counts and implementation scope.

| Control | Verified behavior |
|---|---|
| `APP-ACT-001` | Actuator endpoint exposure is limited to operational endpoints |
| `KV-002` | Key Vault identity uses managed identity behavior |
| `KV-004` | Key Vault is used as a property source rather than called per request |
| `SQL-001` | JDBC host and database values are deployment-injected |
| `KAFKA-011` | Topic and consumer-group contracts are stable and portable |
| `HTTP-007` | Gateway circuit breakers decorate routed request execution |

[Back to Top](#top)

## 4. Repository and IaC Evidence Gap Analysis

The assessment reviewed repository-visible application and delivery artifacts only. Platform topology and deployment state are external unless directly supplied. Missing platform evidence is not an infrastructure finding.

### Available to review

| Repository-visible configuration | Current evidence | Application resiliency interpretation | Related findings |
|---|---|---|---|
| Maven reactor and module POMs | Java 17, Spring Boot 3.2.5, Spring Cloud 2023.0.1, eight deployable modules | Establishes runtime and dependency context | All |
| Application YAML | Eight service configurations with endpoints, clients, health, and telemetry | Establishes repository-owned runtime defaults and budgets | `F-001`, `F-002`, `F-004`, `F-005` |
| Java application source | Controllers, repositories, Kafka handlers, services, and schedules | Establishes state, completion, and ownership behavior | `F-003`, `F-006` through `F-010`, `F-012` |
| Dockerfiles | Eight service Dockerfiles | Establishes mutable runtime image identity | `F-011` |
| Kubernetes manifests | ConfigMap, SecretProviderClass, deployments, services, probes, and ingress | Supports evidence-boundary and runtime interpretation only | `F-001`; no infrastructure findings |
| Azure Pipelines | Maven verify, Surefire publication, and JaCoCo publication | Test tooling is configured, but source-controlled tests are absent | Validation scope only |

### Not available or externally owned

| External evidence or configuration | Needed to validate | Related findings or assumptions |
|---|---|---|
| Approved application architecture context | Context ID, version, owner, lifecycle status, and approved Kafka scenario | `F-008` through `F-010`, GOV-001 |
| Kafka cluster and replication model | Cluster topology, linking, writable role, offsets, promotion, and failback | `F-008` through `F-010` |
| Regional ownership authority | Fail-closed owner, epoch source, fencing, and split-brain response | `F-008`, `F-012` |
| Cosmos DB deployed topology | API/throughput confirmation, preferred regions, multi-region writes, and conflict policy | Active-active data assumptions; no infrastructure finding |
| Azure Managed Redis exact assessment standard | Registry path correction or approved alias for the existing standard | Redis controls remain `not_assessed` |
| Approved timeout and capacity budgets | Caller, drain, SQL, gateway, retry, pool, and concurrency budgets | `F-002`, `F-005`, `F-006` |
| Approved notification durable store | Existing service, retention, identity, and consistency contract | `F-003` |
| Approved runtime image digest | Security-approved Java 17 digest and update process | `F-011` |
| Claim, outbox, retry, and quarantine operations | Lease, retention, terminal state, replay, and reconciliation procedures | `F-007`, `F-009`, `F-010`, `F-012` |

### PCF exclusion

> PCF and its aliases are retired and excluded from findings, scoring, remediation, modernization, migration, and cleanup recommendations. Historical repository references, if discovered, are informational only and are not included in the finding matrix.

[Back to Top](#top)

## 5. Full Finding Matrix

| ID | Source ID | Priority | Severity | Resiliency related | Status | Category | Finding | Change ID | Repository scope |
|---|---|---|---|---|---|---|---|---|---|
| [P0-001](#p0-001-hardcoded-regional-defaults-prevent-safe-reuse-of-one-artifact) | F-001 | P0 | Critical | Yes | Verified | Regional configuration | Hardcoded regional defaults prevent safe reuse of one artifact | CHANGE-AA-001 | Notification and gateway configuration |
| [P0-002](#p0-002-notification-history-is-process-local-state) | F-003 | P0 | Critical | Yes | Verified | State | Notification history is process-local state | CHANGE-AA-003 | Notification repository |
| [P0-003](#p0-003-sql-order-state-and-kafka-events-can-diverge) | F-007 | P0 | Critical | Yes | Verified | Cross-store consistency | SQL order state and Kafka events can diverge | CHANGE-AA-007 | Order service |
| [P0-004](#p0-004-active-standby-kafka-work-is-not-role-gated-or-fenced) | F-008 | P0 | Critical | Yes | Conditional | Kafka workload ownership | Active-standby Kafka work is not role-gated or fenced | CHANGE-AA-008 | Inventory, notification, and cart services |
| [P0-005](#p0-005-runtime-image-is-mutable-by-tag) | F-011 | P0 | High | No | Verified | Supply chain | Runtime image is mutable by tag | CHANGE-AA-011 | Service Dockerfiles |
| [P0-006](#p0-006-scheduled-shared-state-work-has-no-distributed-claim) | F-012 | P0 | Critical | Yes | Verified | Scheduler | Scheduled shared-state work has no distributed claim | CHANGE-AA-012 | Inventory and cart services |
| [P1-001](#p1-001-azure-sql-operations-lack-a-complete-bounded-timeout-budget) | F-002 | P1 | Critical | Yes | Verified | Database resilience | Azure SQL operations lack a complete bounded timeout budget | CHANGE-AA-002 | Order service |
| [P1-002](#p1-002-gateway-dependencies-share-one-http-client-timeout-and-pool-profile) | F-005 | P1 | High | Yes | Verified | HTTP client | Gateway dependencies share one HTTP client profile | CHANGE-AA-005 | API gateway |
| [P1-003](#p1-003-gateway-retry-classification-ignores-server-guidance) | F-006 | P1 | High | Yes | Verified | HTTP retry | Gateway retry classification ignores server guidance | CHANGE-AA-006 | API gateway |
| [P2-001](#p2-001-kafka-consumer-side-effect-failures-are-converted-to-successful-returns) | F-009 | P2 | Critical | Yes | Conditional | Kafka consistency | Consumer side-effect failures become successful returns | CHANGE-AA-009 | Notification service |
| [P2-002](#p2-002-kafka-producer-completion-is-not-observed) | F-010 | P2 | Critical | Yes | Conditional | Kafka delivery | Kafka producer completion is not observed | CHANGE-AA-010 | Cart service |
| [P3-001](#p3-001-health-details-are-exposed-unconditionally) | F-004 | P3 | Medium | No | Verified | Management security | Health details are exposed unconditionally | CHANGE-AA-004 | Gateway and order configuration |

Matrix totals are 12 approved findings: P0 6, P1 3, P2 2, and P3 1. Nine are confirmed and three are conditional. Verified controls, observations, `not_assessed`, `not_applicable`, accepted risks, and PCF references are excluded.

[Back to Top](#top)

## 6. Standards Alignment

| Standard or pattern | Assessment status | Related controls | Related findings |
|---|---|---|---|
| Spring Boot on AKS Active-Active Code Assessment Standard v4.0.0 | Evaluated; 1 compliant master control, mapped noncompliance, and evidence-limited controls preserved as `not_assessed` | `APP-*` | `F-001`, `F-003` through `F-012` |
| Azure Key Vault Application Behavior Standard v2.0.0 | Evaluated; 2 compliant controls, 1 mapped noncompliance, remaining controls evidence-limited or not applicable | `KV-001` through `KV-016` | `F-001` |
| Azure Cosmos DB Application Behavior Standard v1.0.0 | Evaluated; all controls remain `not_assessed` because effective multi-region behavior is not proven | `COSMOS-001` through `COSMOS-008` | None |
| Azure SQL Application Behavior Standard v2.0.0 | Evaluated; 1 compliant and 2 mapped noncompliant controls | `SQL-001`, `SQL-002`, `SQL-013` | `F-002`, `F-007` |
| Confluent Kafka Multi-Region Standard v3.0.0 | Evaluated under policy-inferred active-standby; scenario-specific conclusions remain conditional | `KAFKA-*`, `KAFKA-AS-*` | `F-001`, `F-008` through `F-010` |
| Spring HTTP and SDK Client Grounding v2.0.0 | Evaluated; circuit-breaker execution compliant and client isolation/retry controls noncompliant | `HTTP-003`, `HTTP-004`, `HTTP-007` | `F-005`, `F-006` |
| Azure Managed Redis Application Behavior Standard | Not assessed because the exact inventory-selected registry path was absent and substitution was prohibited in Step 2 | Standard-level result | None |
| Active-Active Remediation Prioritization Policy v1.0.0 | Applied without overrides; every change preserves its governed rule | `P0-AA-*`, `P1-RCV-*`, `P2-DATA-*`, `P3-OPS-*` | All findings |

[Back to Top](#top)

## 7. Implementation Roadmap

The authoritative Step 3A remediation plan remains the implementation source. This section summarizes its governed sequence without replacing its change specifications, tests, acceptance criteria, decisions, or validation commands.

### Priority summary

| Priority | Change count | Primary objective | Release gate |
|---|---:|---|---|
| P0 | 6 | Establish regional determinism, durable state, consistency, ownership, and scheduler safety | Before active-active release |
| P1 | 3 | Bound and isolate dependency failure and retry behavior | Before failover certification |
| P2 | 2 | Preserve Kafka processing and delivery completion semantics | Before full active-active enablement |
| P3 | 1 | Restrict operational health disclosure | Before operational acceptance |

### Implementation waves

| Wave | Change IDs | Findings addressed | Prerequisites | Validation focus |
|---|---|---|---|---|
| 1 | CHANGE-AA-001, CHANGE-AA-011 | F-001, F-011 | Region property and approved image digest | Regional configuration and immutable artifact parity |
| 2 | CHANGE-AA-003, CHANGE-AA-007, CHANGE-AA-008, CHANGE-AA-012 | F-003, F-007, F-008, F-012 | Durable-store decision, outbox contract, GOV-001, ownership contract | Persistence, split brain, reconciliation, and claims |
| 3 | CHANGE-AA-002, CHANGE-AA-005, CHANGE-AA-006 | F-002, F-005, F-006 | Approved SQL, route, resource, and retry budgets | Deadlines, isolation, saturation, and retry classification |
| 4 | CHANGE-AA-009, CHANGE-AA-010 | F-009, F-010 | Ownership, durable state, claims, idempotency, and quarantine policy | Redelivery, completion, stable identity, and quarantine |
| 5 | CHANGE-AA-004 | F-004 | Actuator operator authority | Anonymous probes and authorized detail access |

### Change index

| Change ID | Priority | Priority rule | Finding IDs | Objective | Complexity | Wave |
|---|---|---|---|---|---|---:|
| CHANGE-AA-001 | P0 | P0-AA-001 | F-001 | Externalize and validate regional configuration | Medium | 1 |
| CHANGE-AA-002 | P1 | P1-RCV-001 | F-002 | Establish a bounded Azure SQL operation budget | Medium | 3 |
| CHANGE-AA-003 | P0 | P0-AA-005 | F-003 | Persist notification history in an approved durable store | High | 2 |
| CHANGE-AA-004 | P3 | P3-OPS-005 | F-004 | Restrict health detail disclosure | Low | 5 |
| CHANGE-AA-005 | P1 | P1-RCV-003 | F-005 | Isolate gateway dependency resources and budgets | High | 3 |
| CHANGE-AA-006 | P1 | P1-RCV-002 | F-006 | Classify and budget gateway retries | Medium | 3 |
| CHANGE-AA-007 | P0 | P0-AA-006 | F-007 | Introduce a transactional order outbox | High | 2 |
| CHANGE-AA-008 | P0 | P0-AA-006 | F-008 | Gate and fence active-standby Kafka workload ownership | High | 2 |
| CHANGE-AA-009 | P2 | P2-DATA-002 | F-009 | Preserve Kafka consumer failure semantics | Medium | 4 |
| CHANGE-AA-010 | P2 | P2-DATA-002 | F-010 | Observe and recover scheduled Kafka producer completion | Medium | 4 |
| CHANGE-AA-011 | P0 | P0-AA-001 | F-011 | Pin all runtime images by approved digest | Low | 1 |
| CHANGE-AA-012 | P0 | P0-AA-006 | F-012 | Add distributed ownership and atomic claims to scheduled work | High | 2 |

### Targeted implementation discovery

`CHANGE-AA-001`, `CHANGE-AA-003`, `CHANGE-AA-008`, `CHANGE-AA-011`, and `CHANGE-AA-012` require targeted discovery before modification. Discovery must resolve exact owning packages and files, the approved durable store, Kafka architecture and ownership provider, the security-approved image digest, and claim semantics. It must not reopen findings, severity, status, or priority.

### Approval boundary

Step 4 uses `.copilot-tracking/plans/2026-09-01/springboot-active-active-authoritative-remediation-plan.instructions.md` and supports `APPROVED_PRIORITIES`, `APPROVED_WAVES`, and `APPROVED_CHANGE_IDS`. Priorities are the preferred selector. Before source modification, Step 4 resolves selectors and freezes the resulting change IDs in its implementation artifact. Only those resolved changes may be implemented, and no source code, configuration, tests, deployment automation, or infrastructure were modified by Step 3B.

[Back to Top](#top)

<!--
schema_conformance:
  schema_id: CODE-LEVEL-RESILIENCY-ASSESSMENT-REPORT
  schema_version: "1.1.0"
  required_sections_present: true
  required_section_order_valid: true
  required_finding_fields_present: true
  summary_counts_reconcile: true
  finding_matrix_reconciles: true
  roadmap_matches_plan: true
  target_paths_present: true
  original_line_ranges_present: true
  original_source_excerpts_present: true
  original_source_matches_step_2: true
  illustrative_code_matches_step_3a: true
  original_and_proposed_code_separated: true
  invented_source_excerpts: false
  unsupported_findings_added: false
  priorities_changed: false
  infrastructure_findings_added: false
  pcf_findings_added: false
  report_written_by_step_3b: true
  delegated_to_task_implementor: false
  status: passed
-->