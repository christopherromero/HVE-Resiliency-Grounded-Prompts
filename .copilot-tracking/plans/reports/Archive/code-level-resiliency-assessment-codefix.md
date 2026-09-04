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
-->
<a id="top"></a>

# Code-Level Resiliency Assessment

| Metadata | Value |
|---|---|
| Report ID | `customer-app-2026-09-02-001-step-3b` |
| Assessment type | Code-level resiliency assessment |
| Generated at | 2026-09-02 |
| Application | Ecommerce Platform (`ecommerce-platform`) |
| Assessment date | 2026-09-02 |
| Repository scope | `source/customer-app` |
| Current deployment | AKS and West US repository intent; actual deployed state not provided |
| Target deployment | Active-active assessment goal; Kafka processing scenario is inferred active-standby |
| Language and framework | Java 17, Spring Boot 3.2.5, Spring Cloud 2023.0.1, Azure Spring 5.10.0 |
| Runtime platform | AKS |
| Report version | 1.0.0 |

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

The assessed repository is a Maven multi-module ecommerce platform with one shared library and eight deployable Spring Boot services. It exposes 63 HTTP handlers and ten gateway routes, produces 18 Kafka event types, contains 14 Kafka listener methods, and schedules four recurring workloads. Repository-visible state paths include Azure SQL for user, order, and payment services; Cosmos DB for product, inventory, and cart services; Redis for rate-limit and cache state; and process memory for notification records. Key Vault is the observed secret source.

The repository shows AKS and West US deployment intent, application YAML, Java source, Azure Pipelines, Docker health checks, Kubernetes manifests, and Terraform declarations. These artifacts establish repository intent, not deployed platform state. The assessment is application-code-only. Shared services are assumed compliant with enterprise resiliency standards, and no infrastructure compliance conclusion is made.

### Repository-Observed Interactions

Directly observed interactions include seven gateway HTTP dependencies; six Kafka-producing services; inventory and notification consumers; Azure SQL, Cosmos DB, Redis, Key Vault, and SMTP clients; and four scheduled workloads. The inventory records nine direct state-store relationships, one direct secret source, and three unresolved endpoint aliases. External Kafka consumers, service topology, and deployed regional resource configuration are outside the repository evidence boundary.

### Supplied External Architecture Context

`application-context/assessment-context.md` identifies the Ecommerce Platform, Java, Spring Boot, AKS, and an active-active assessment goal. It excludes infrastructure assessment and asks that shared services be assumed compliant. No approved architecture-context YAML containing a context ID, version, topology, or deployment approval was supplied. The context informs scope and impact but is not original source-code evidence.

### Kafka Operating Scenario

* **Scenario:** Active-Standby
* **Processing model:** Mixed
* **Regional processing model:** Single active
* **External side effects:** Unknown
* **Kafka-backed state:** None
* **Scenario source:** Inferred from repository-observed dependency roles
* **Context ID:** `not_applicable`
* **Context version:** `not_applicable`
* **Policy:** `KAFKA-OPERATING-SCENARIO` version `3.1.0`
* **Policy rule:** `KAFKA-SCENARIO-001`
* **Policy validation:** Inferred
* **Repository compatibility:** Consistent
* **Architecture confirmation required:** Yes
* **Kafka topology:** Not established
* **Stretched cluster:** Not established
* **Authoritative state alignment:** Azure SQL and Cosmos DB are related state dependencies; deployed ownership and failover topology are not established

### Assessment themes

* Regional configuration is not deployment-bound. P0-001 is verified: fixed or default physical endpoints can retain the wrong regional dependency after deployment.
* Authoritative processing lacks durable identity and ownership. P0-002 is conditional on the inferred active-standby Kafka scenario; P0-003, P0-004, and P0-006 are verified durability and concurrency findings.
* Failure behavior is incomplete. P1-001 and P1-002 are verified: dependency budgets are partial, and Redis loss changes a security decision to unconditional admission.
* Release and lifecycle evidence is insufficient. P0-005 and P0-007 are verified: no automated failure tests exist, and graceful shutdown is inconsistent.
* Operational correctness needs completion. P2-001, P2-002, P3-001, P3-002, and P3-003 cover delivery completion, atomic Redis state, diagnostic safety, regional telemetry, and management exposure.

### Approved shared-service and reference architectures

The report uses only links supplied by the governance schema.

| Azure Shared Service | Link to Reference Architecture |
|---|---|
| Azure API Management | [Reference](https://rxsafeway.sharepoint.com/:w:/r/sites/Cloud2.0/Shared%20Documents/I11%20Resiliency%20Program/Discovery/Integration%20Platform/APIM/Design/APIM%20-%20Albertsons%20Multi-Region%20Design%20v5.docx?d=w7f65ea542cc7491687202cfa68599d7b&csf=1&web=1&e=dhPvP3) |
| Azure Application Gateway | [Reference](https://rxsafeway.sharepoint.com/:w:/r/sites/Cloud2.0/Shared%20Documents/I11%20Resiliency%20Program/Discovery/Integration%20Platform/AppGW/Design/Albertsons%20Architecture%20Design_Application%20Gateway_v1.0.docx?d=w3126f533271842c9a75d83ae93b6b6db&csf=1&web=1&e=hmksie) |
| Azure Key Vault | [Reference](https://rxsafeway.sharepoint.com/:w:/r/sites/Cloud2.0/Shared%20Documents/I11%20Resiliency%20Program/Discovery/Cloud%20Foundation/Design/ACI%20Entra%20ID%20Draft%20v1.0.docx?d=wad696d3ecdae4d84a6a1ea5675d3aec6&csf=1&web=1&e=rCLr5y) |
| Kafka | [Reference](https://rxsafeway.sharepoint.com/:w:/r/sites/Cloud2.0/Shared%20Documents/I11%20Resiliency%20Program/Discovery/Integration%20Platform/Kafka/Approved_Albertsons_RegionResiliency_Kafka-MultiRegion.docx?d=w08142308135244de855f4dab4c49ca2d&csf=1&web=1&e=kueuJ9) |
| Azure SQL Database | [Reference](https://rxsafeway.sharepoint.com/:f:/r/sites/Cloud2.0/Shared%20Documents/I11%20Resiliency%20Program/Discovery/Database%20Platform/SQL%20DB?csf=1&web=1&e=xMauSY) |
| Azure Cosmos DB | [Reference](https://rxsafeway.sharepoint.com/:w:/r/sites/Cloud2.0/Shared%20Documents/I11%20Resiliency%20Program/Discovery/Database%20Platform/Cosmos/Albertsons_Architecture_Design_MongoDB_RU_v1.0.docx?d=wa68893488e094fef9b5506690c685847&csf=1&web=1&e=YDVc7g) |
| Azure Managed Redis | [Reference](https://rxsafeway.sharepoint.com/:w:/r/sites/Cloud2.0/Shared%20Documents/I11%20Resiliency%20Program/Discovery/Database%20Platform/Redis/Design/Managed%20Redis%20-%20Albertsons%20Multi-Region%20Design%20v3.docx?d=wad90acec4c154b2498d899a2ffcdc9d4&csf=1&web=1&e=L7pVbQ) |
| Azure Kubernetes Service (AKS) | [Reference](https://rxsafeway.sharepoint.com/:w:/r/sites/Cloud2.0/Shared%20Documents/I11%20Resiliency%20Program/Discovery/Container%20Platform/Design/Albertsons%20Architecture%20Design_AKS%20and%20Istio_v1.0.docx?d=w97c0edfea59d466e80af843958d95c5c&csf=1&web=1&e=7UJSQS) |

The schema also provides approved references for Azure Entra ID, Azure Storage, Azure Functions, Azure Networking, and Azure Storage Blobs and Files. Those services are not direct finding dependencies in this assessment and are not used as evidence.

### Summary findings table

| Priority | Section | Confirmed count | Description |
|---|---|---:|---|
| P0 | Resiliency-Focused Recommendations | 7 | Six verified active-active blockers and one conditional ownership blocker |
| P1 | Resiliency-Focused Recommendations | 2 | Bounded dependency behavior and safe Redis degradation |
| P2 | Resiliency-Focused Recommendations | 2 | Kafka delivery completion and Redis state correctness |
| P3 | Resiliency-Focused Recommendations | 3 | Diagnostic safety, regional telemetry, and management maturity |
| Total | Resiliency-Focused Recommendations | 14 | 13 verified findings and one conditional finding |

### Illustrative-code notice

> **IMPORTANT:** Hard numbers used for retry counts, timeout settings, interval timings, thread-pool sizes, cache duration, health thresholds, and circuit-breaker settings are examples unless the authoritative plan identifies an approved value. These values must be externally configurable and coordinated with application, mesh, gateway, and load-balancer budgets. All code snippets are illustrative proposals, not applied or prescriptive patches.

[Back to Top](#top)

## 2. Resiliency-Focused Recommendations

### P0 Critical Immediate Action

#### P0-001: Regional dependency endpoints are hardcoded

**Priority: P0 - active-active release blocker**

**Priority policy:** `AA-REMEDIATION-PRIORITY` version `1.0.0`, rule `P0-AA-001`

**Severity:** Critical

**Resiliency Related:** Yes

**Finding status:** Verified finding

**Issue:** Key Vault, Cosmos DB, and Redis use fixed Azure hostnames as defaults or direct values. Another region can silently retain West US or shared endpoints.

**What does this solve:** One immutable artifact selects only deployment-approved local regional endpoints.

**Resiliency Impact:** Removes cross-region latency and correlated dependency failure caused by stale regional endpoint configuration.

**Recommended Fix:** Require injected endpoint properties, remove physical production defaults, fail startup when required values are absent, and retain local-only defaults in local profiles.

**Repository evidence:** `EV-F-001-01`, `EV-F-001-02`, `EV-F-001-03`

**File:** `source/customer-app/api-gateway/src/main/resources/application.yml:40-40`

**Original source requiring update:** Key Vault endpoint, exact Step 2 excerpt:

```yaml
          endpoint: https://ecommerce-keyvault.vault.azure.net/
```

**File:** `source/customer-app/product-service/src/main/resources/application.yml:11-11`

```yaml
        endpoint: https://ecommerce-cosmos.documents.azure.com:443/
```

**File:** `source/customer-app/api-gateway/src/main/resources/application.yml:45-45`

```yaml
    host: ${REDIS_HOST:ecommerce-redis.redis.cache.windows.net}
```

**Fix:** Illustrative proposal only.

Generated target `AA001-T01`, `source/customer-app/api-gateway/src/main/resources/application.yml`, symbol `spring.cloud.azure.keyvault.secret.endpoint`:

```yaml
spring: {cloud: {azure: {keyvault: {secret: {endpoint: "${AZURE_KEYVAULT_ENDPOINT}"}}}}}
```

Generated target `AA001-T02`, `source/customer-app/product-service/src/main/resources/application.yml`, symbol `spring.cloud.azure.cosmos.endpoint`:

```yaml
spring: {cloud: {azure: {cosmos: {endpoint: "${AZURE_COSMOS_ENDPOINT}"}}}}
```

Generated target `AA001-T03`, `source/customer-app/api-gateway/src/main/resources/application.yml`, symbol `spring.redis.host`:

```yaml
spring: {redis: {host: "${REDIS_HOST}"}}
```

These targets remove physical production defaults for Key Vault, Cosmos DB, and Redis. Target files and symbols are the three original evidence locations above. `CHANGE-AA-001` creates local-profile files only for local defaults.

**Validation requirements:** Start gateway and product service with two regional property sets; verify all effective endpoints; prove missing production endpoints fail startup. Run `mvn -pl api-gateway,product-service -am verify`.

**Dependencies:** Deployment endpoint inputs and approved local-profile policy.

**Notes:**

* Cross-refs: `F-001`, `CHANGE-AA-001`, wave 1
* Implementation: Three generated configuration targets; no blocked target
* Validation: Regional binding and missing-value startup tests
* Guardrail: Do not introduce a different physical production default

<span style="font-size: 14px;">**MSFT Reference:** Grounded controls `APP-AA-002`, `APP-AA-003`, `KV-001`, `COSMOS-001`, `KAFKA-001`, and `REDIS-003`.</span>

---

#### P0-002: Active-standby Kafka work has no regional ownership gate

**Priority: P0 - active-active authoritative-processing blocker**

**Priority policy:** `AA-REMEDIATION-PRIORITY` version `1.0.0`, rule `P0-AA-006`

**Severity:** Critical

**Resiliency Related:** Yes

**Finding status:** Conditional finding. Applies if the inferred `active_standby` scenario is confirmed. Architecture confirmation is required under `KAFKA-OPERATING-SCENARIO` version `3.1.0`, rule `KAFKA-SCENARIO-001`.

**Issue:** Listeners and scheduled work have no active-role, SQL-ownership, lease, epoch, or fencing condition.

**What does this solve:** Standby and stale-active instances cannot process authoritative work concurrently.

**Resiliency Impact:** Prevents split-brain inventory mutation and processing before SQL and Kafka ownership align.

**Recommended Fix:** Introduce a fail-safe regional role contract, gate acquisition, use authoritative fencing, stop acquisition before transfer, and expose both-active, both-inactive, and epoch signals.

**Repository evidence:** `EV-F-004-01`

**File:** `source/customer-app/inventory-service/src/main/java/com/ecommerce/inventory/service/InventoryService.java:250-250`

**Original source requiring update:**

```java
    @KafkaListener(topics = KafkaTopics.ORDER_CREATED, groupId = KafkaTopics.GROUP_INVENTORY_SERVICE)
```

**Fix:** Illustrative proposal only.

Generated target `AA004-T01`, `source/customer-app/common/src/main/java/com/ecommerce/common/ownership/RegionalWorkOwnership.java`, symbol `RegionalWorkOwnership`:

```java
public interface RegionalWorkOwnership { OwnershipSnapshot current(); record OwnershipSnapshot(boolean active, long fencingEpoch, String region) {} }
```

Generated target `AA004-T02`, assessed service symbol `handleOrderCreated`:

```java
public void handleOrderCreated(Map<String, Object> event) { ownership.requireCurrentOwner(); processOrderCreated(event); }
```

Generated target `AA004-T03`, `source/customer-app/inventory-service/src/test/java/com/ecommerce/inventory/service/RegionalOwnershipTest.java`:

```java
@Test void onlyFencedOwnerAcquiresWork() { ownership.set(active("region-a", epoch)); service.handleOrderCreated(event); verify(processor).process(event); }
@Test void standbyAndStaleActiveDoNotAcquireWork() { ownership.set(standbyOrStale()); assertThatThrownBy(() -> service.handleOrderCreated(event)).isInstanceOf(IllegalStateException.class); }
@Test void ownershipLossStopsAcquisitionBeforeTransfer() { coordinator.onOwnershipLost(); inOrder(listenerRegistry, ownership).verify(listenerRegistry).stop(); }
```

**Illustrative code status:** Targeted implementation discovery required (`AA004-T04`, `AuthoritativeRegionalWorkOwnershipAdapter`, path not yet selected)

**Why code was not generated:** The approved SQL ownership signal, lease authority, fencing mechanism, and promotion authority are absent.

**Unresolved inputs:** SQL read-write ownership signal; lease store; fencing epoch; promotion authority; failback sequence.

**Intended behavior:** Resolve ownership from the approved SQL signal and reject stale epochs.

**Validation requirements:** Exercise active, standby, stale-active, both-active, both-inactive, promotion, and ownership-loss transitions; prove only the fenced owner acquires work.

**Dependencies:** Confirm scenario and approve ownership authority, lease, epoch, promotion, and failback.

**Notes:**

* Cross-refs: `F-004`, `CHANGE-AA-004`, wave 4
* Implementation: Three generated targets and one blocked adapter target
* Validation: `mvn -pl common,inventory-service,notification-service -am verify`
* Guardrail: Do not implement the adapter before scenario and authority approval

<span style="font-size: 14px;">**MSFT Reference:** Grounded controls `KAFKA-AS-001`, `KAFKA-010`, `KAFKA-012`, `APP-KAFKA-001`, and `APP-WORKLOAD-001`.</span>

---

#### P0-003: Kafka producer completion and event identity are not durable

**Priority: P0 - active-active authoritative-processing blocker**

**Priority policy:** `AA-REMEDIATION-PRIORITY` version `1.0.0`, rule `P0-AA-006`

**Severity:** Critical

**Resiliency Related:** Yes

**Finding status:** Verified finding

**Issue:** User events create a random ID per invocation, return before delivery, and only log callback failures.

**What does this solve:** Committed work cannot lose its event intent or change identity after retry or promotion.

**Resiliency Impact:** Preserves one event identity across broker interruption, process restart, retry, and regional promotion.

**Recommended Fix:** Persist event identity with business work and publish through a durable outbox or equivalent recoverable boundary.

**Repository evidence:** `EV-F-006-01`

**File:** `source/customer-app/user-service/src/main/java/com/ecommerce/userservice/event/UserEventPublisher.java:23-23`

**Original source requiring update:**

```java
        event.setEventId(UUID.randomUUID().toString());
```

**Fix:** Illustrative proposal only.

Generated target `AA006-T01`, `UserEventPublisher.publishUserRegistered`:

```java
public void publishUserRegistered(String eventId, UUID userId, String email) { outboxRepository.save(OutboxEvent.pending(eventId, KafkaTopics.USER_REGISTERED, userId.toString(), email)); }
```

Generated target `AA006-T02`, `source/customer-app/user-service/src/main/java/com/ecommerce/userservice/event/OutboxRepository.java`:

```java
public interface OutboxRepository { void save(OutboxEvent event); List<OutboxEvent> claimPending(String owner, int limit); void markPublished(String eventId); void markFailed(String eventId, String failureCode); }
```

Generated target `AA006-T03`, `source/customer-app/user-service/src/test/java/com/ecommerce/userservice/event/UserEventPublisherTest.java`:

```java
@Test void retryAndRestartReuseStableEventIdentity() { publisher.publishUserRegistered(eventId, userId, email); restartPublisher(); publisher.publishPending(); verify(kafkaTemplate, atLeastOnce()).send(KafkaTopics.USER_REGISTERED, eventId, eventCaptor.capture()); assertThat(eventCaptor.getAllValues()).allMatch(event -> event.getEventId().equals(eventId)); }
@Test void brokerLossAfterBusinessCommitLeavesRecoverableIntent() { commitBusinessOperation(eventId); broker.failNextSend(); publisher.publishPending(); assertThat(outboxRepository.find(eventId).status()).isEqualTo(OutboxStatus.PENDING); }
```

**Illustrative code status:** Targeted implementation discovery required (`AA006-T04`, `DurableOutboxRepositoryAdapter`, path not yet selected)

**Why code was not generated:** Outbox schema, transaction boundary, claim, retention, and fencing decisions are not approved.

**Unresolved inputs:** Store; schema; transaction boundary; claim protocol; retention; fencing.

**Intended behavior:** Persist and fence outbox claim and terminal publication state.

**Validation requirements:** Interrupt the broker around business commit and verify eventual publication with one stable event ID across restart, retry, and promotion.

**Dependencies:** Approved outbox store, schema, retention, claim, and fencing.

**Notes:**

* Cross-refs: `F-006`, `CHANGE-AA-006`, wave 3
* Implementation: Three generated targets and one blocked adapter
* Validation: `mvn -pl user-service -am verify`
* Guardrail: Do not claim SQL-Kafka atomicity

<span style="font-size: 14px;">**MSFT Reference:** Grounded controls `KAFKA-002`, `KAFKA-011`, `KAFKA-AS-006`, and `APP-AA-011`.</span>

---

#### P0-004: Notification records are stored only in process memory

**Priority: P0 - durable state blocker**

**Priority policy:** `AA-REMEDIATION-PRIORITY` version `1.0.0`, rule `P0-AA-005`

**Severity:** Critical

**Resiliency Related:** Yes

**Finding status:** Verified finding

**Issue:** Notification records use a `ConcurrentHashMap` and random process-local identifiers.

**What does this solve:** Required notification state remains visible and reconcilable after restart or regional movement.

**Resiliency Impact:** Prevents state loss and pod- or region-specific views of delivery state.

**Recommended Fix:** Use a durable repository contract, stable operation identity, explicit transitions, and retained terminal state.

**Repository evidence:** `EV-F-007-01`

**File:** `source/customer-app/notification-service/src/main/java/com/ecommerce/notification/repository/NotificationRepository.java:18-18`

**Original source requiring update:**

```java
    private final Map<String, NotificationRecord> store = new ConcurrentHashMap<>();
```

**Fix:** Illustrative proposal only.

Generated target `AA007-T01`, same path, symbol `NotificationRepository`:

```java
public interface NotificationRepository { NotificationRecord createIfAbsent(NotificationRecord record); Optional<NotificationRecord> findByOperationId(String operationId); NotificationRecord transition(String operationId, DeliveryStatus expected, DeliveryStatus next); }
```

Generated target `AA007-T02`, `source/customer-app/notification-service/src/test/java/com/ecommerce/notification/repository/NotificationRepositoryContractTest.java`:

```java
@Test void restartPreservesRecordAndStableIdentity() { repository.createIfAbsent(pending(operationId)); repository = restartRepository(); assertThat(repository.findByOperationId(operationId)).isPresent(); }
@Test void duplicateCreateReturnsOneRecord() { assertThat(repository.createIfAbsent(pending(operationId)).id()).isEqualTo(repository.createIfAbsent(pending(operationId)).id()); }
@Test void illegalStateTransitionFails() { repository.createIfAbsent(delivered(operationId)); assertThatThrownBy(() -> repository.transition(operationId, DeliveryStatus.DELIVERED, DeliveryStatus.PENDING)).isInstanceOf(IllegalStateException.class); }
```

**Illustrative code status:** Targeted implementation discovery required (`AA007-T03`, `DurableNotificationRepositoryAdapter`, path not yet selected)

**Why code was not generated:** The approved durable persistence technology is not selected.

**Unresolved inputs:** Durable store; partition or key design; encryption.

**Intended behavior:** Implement the generated repository contract using an approved durable store.

**Illustrative code status:** Targeted implementation discovery required (`AA007-T04`, notification persistence migration, path not yet selected)

**Why code was not generated:** Schema and migration depend on the unselected durable store and retention decision.

**Unresolved inputs:** Store; schema; retention; encryption; migration policy.

**Intended behavior:** Establish durable schema and migration while preserving stable operation identity.

**Validation requirements:** Prove restart persistence, stable duplicate identity, valid transitions, and terminal visibility.

**Dependencies:** Approved store, schema, retention, encryption, and migration policy.

**Notes:**

* Cross-refs: `F-007`, `CHANGE-AA-007`, wave 3
* Implementation: Two generated targets and two blocked persistence targets
* Validation: `mvn -pl notification-service -am verify`
* Guardrail: Process memory may remain only as a disposable cache

<span style="font-size: 14px;">**MSFT Reference:** Grounded controls `APP-AA-010`, `APP-STATE-001`, and `APP-STATE-002`.</span>

---

#### P0-005: Failure and recovery behavior has no automated tests

**Priority: P0 - verification release blocker**

**Priority policy:** `AA-REMEDIATION-PRIORITY` version `1.0.0`, rule `P0-AA-007`

**Severity:** Critical

**Resiliency Related:** Yes

**Finding status:** Verified finding

**Issue:** The inventory found zero tests, and the pipeline permits empty coverage.

**What does this solve:** Every remediation becomes release-gated and regression-testable.

**Resiliency Impact:** Makes timeout, ownership, replay, shutdown, failover, and recovery regressions detectable before release.

**Recommended Fix:** Add focused unit, integration, and fault tests and reject empty test or coverage output.

**Repository evidence:** `EV-F-008-01`

**File:** `source/customer-app/azure-pipelines.yml:68-68`

**Original source requiring update:**

```yaml
              failIfCoverageEmpty: false
```

**Fix:** Illustrative proposal only.

Generated target `AA008-T01`, `source/customer-app/azure-pipelines.yml`, symbol `PublishCodeCoverageResults`:

```yaml
- task: PublishCodeCoverageResults@2
  inputs: {failIfCoverageEmpty: true}
```

Generated target `AA008-T02`, `source/customer-app/pom.xml`, symbol `test dependency contract`:

```xml
<dependency><groupId>org.springframework.boot</groupId><artifactId>spring-boot-starter-test</artifactId><scope>test</scope></dependency>
```

Generated target `AA008-T03`, `source/customer-app/common/src/test/java/com/ecommerce/common/test/FaultScenario.java`:

```java
public record FaultScenario(String dependency, FaultPhase phase, boolean recoveryExpected) {}
```

**Validation requirements:** Run `mvn test` and `mvn verify`; require non-empty test and coverage output for affected modules.

**Dependencies:** Coverage threshold and CI fault-service decisions.

**Notes:**

* Cross-refs: `F-008`, `CHANGE-AA-008`, wave 1
* Implementation: Three generated targets; behavior tests remain owned by each remediation
* Validation: Maven test and verify
* Guardrail: Flaky tests require an owner and expiry; empty coverage remains prohibited

<span style="font-size: 14px;">**MSFT Reference:** Grounded controls `APP-AA-018`, `APP-SUPPLY-001`, `KV-008`, `COSMOS-008`, `SQL-008`, `KAFKA-008`, and `REDIS-027`.</span>

---

#### P0-006: Scheduled shared-state work has no distributed ownership

**Priority: P0 - authoritative-processing blocker**

**Priority policy:** `AA-REMEDIATION-PRIORITY` version `1.0.0`, rule `P0-AA-006`

**Severity:** Critical

**Resiliency Related:** Yes

**Finding status:** Verified finding

**Issue:** Every inventory-service instance schedules shared-state mutation without an atomic claim, lease, or fencing rule.

**What does this solve:** Overlapping schedulers cannot duplicate expiry, alerts, or shared-state mutation.

**Resiliency Impact:** Prevents duplicate effects and stale-owner writes during overlap and failover.

**Recommended Fix:** Require current ownership, claim bounded work atomically, fence completion, and externalize scheduling.

**Repository evidence:** `EV-F-010-01`

**File:** `source/customer-app/inventory-service/src/main/java/com/ecommerce/inventory/service/InventoryService.java:268-268`

**Original source requiring update:**

```java
    @Scheduled(fixedDelay = 300000) // Every 5 minutes
```

**Fix:** Illustrative proposal only.

Generated target `AA010-T01`, same path, symbol `expireOldReservations`:

```java
@Scheduled(fixedDelayString = "${app.inventory.expiry.fixed-delay}") public void expireOldReservations() { ownership.requireCurrentOwner(); claimRepository.claimExpired(owner(), epoch(), clock.instant(), properties.claimLimit()).forEach(this::expireClaimedReservation); }
```

Generated target `AA010-T02`, `source/customer-app/inventory-service/src/main/java/com/ecommerce/inventory/service/ReservationExpiryClaimRepository.java`:

```java
public interface ReservationExpiryClaimRepository { List<ClaimedReservation> claimExpired(String owner, long fencingEpoch, Instant now, int limit); void complete(String reservationId, String owner, long fencingEpoch); }
```

Generated target `AA010-T03`, `source/customer-app/inventory-service/src/test/java/com/ecommerce/inventory/service/ReservationExpiryOwnershipTest.java`:

```java
@Test void overlappingSchedulersProduceOneClaimAndOneAlert() { runConcurrently(firstScheduler, secondScheduler); verify(claimRepository, times(1)).complete(reservationId, owner, epoch); verify(alertPublisher, times(1)).publish(reservationId); }
@Test void staleOwnerCannotCompleteAfterLeaseTransfer() { transferLeaseTo(newOwner, newEpoch); assertThatThrownBy(() -> claimRepository.complete(reservationId, oldOwner, oldEpoch)).isInstanceOf(IllegalStateException.class); }
@Test void leaseExpiryMakesIncompleteWorkRecoverable() { expireLease(reservationId); assertThat(claimRepository.claimExpired(newOwner, newEpoch, now, limit)).extracting(ClaimedReservation::id).contains(reservationId); }
```

**Illustrative code status:** Targeted implementation discovery required (`AA010-T04`, `FencedReservationExpiryClaimAdapter`, path not yet selected)

**Why code was not generated:** The approved claim document model, conditional-write API, lease policy, and fencing rule are not selected.

**Unresolved inputs:** Claim document model; conditional-write API; lease policy; fencing rule.

**Intended behavior:** Atomically claim Cosmos work and reject stale-owner writes.

**Validation requirements:** Test overlapping schedules, lease expiry, stale fencing, optimistic conflicts, bounded work, and duplicate effects.

**Dependencies:** P0-002 ownership, P0-003 stable identity, test foundation, and region telemetry.

**Notes:**

* Cross-refs: `F-010`, `CHANGE-AA-010`, wave 4
* Implementation: Three generated targets and one blocked adapter
* Validation: `mvn -pl inventory-service -am verify`
* Guardrail: Disable schedules before adapter rollback

<span style="font-size: 14px;">**MSFT Reference:** Grounded controls `APP-SCHED-001`, `APP-SCHED-002`, `APP-WORKLOAD-001`, and `APP-OBS-002`.</span>

---

#### P0-007: Graceful shutdown is not configured consistently

**Priority: P0 - authoritative-processing recovery blocker**

**Priority policy:** `AA-REMEDIATION-PRIORITY` version `1.0.0`, rule `P0-RCV-008`

**Severity:** High

**Resiliency Related:** Yes

**Finding status:** Verified finding

**Issue:** Graceful shutdown is absent for api-gateway, user-service, product-service, and notification-service; no pre-stop hook or explicit grace period was observed.

**What does this solve:** Termination cannot accept new authoritative work after drain begins or silently lose in-flight work.

**Resiliency Impact:** Coordinates readiness withdrawal, acquisition stop, bounded completion, ownership release, and termination.

**Recommended Fix:** Enable configurable graceful shutdown and validate each applicable HTTP, Kafka, and asynchronous workload under termination.

**Repository evidence:** `EV-F-011-01`, inventory key `lifecycle_and_recovery.graceful_shutdown_not_explicitly_configured`

**File:** Not available in authoritative evidence artifact.

**Original source requiring update:** Original source excerpt: Not available in authoritative evidence artifact.

**Fix:** Illustrative proposal only.

Generated target `AA011-T01`, `source/customer-app/api-gateway/src/main/resources/application.yml`, symbol `server.shutdown and spring.lifecycle.timeout-per-shutdown-phase`:

```yaml
server: {shutdown: graceful}
spring: {lifecycle: {timeout-per-shutdown-phase: "${APP_SHUTDOWN_TIMEOUT}"}}
```

Generated target `AA011-T02`, `source/customer-app/user-service/src/main/resources/application.yml`, symbol `server.shutdown and spring.lifecycle.timeout-per-shutdown-phase`:

```yaml
server: {shutdown: graceful}
spring: {lifecycle: {timeout-per-shutdown-phase: "${APP_SHUTDOWN_TIMEOUT}"}}
```

Generated target `AA011-T03`, `source/customer-app/product-service/src/main/resources/application.yml`, symbol `server.shutdown and spring.lifecycle.timeout-per-shutdown-phase`:

```yaml
server: {shutdown: graceful}
spring: {lifecycle: {timeout-per-shutdown-phase: "${APP_SHUTDOWN_TIMEOUT}"}}
```

Generated target `AA011-T04`, `source/customer-app/notification-service/src/main/resources/application.yml`, symbol `server.shutdown and spring.lifecycle.timeout-per-shutdown-phase`:

```yaml
server: {shutdown: graceful}
spring: {lifecycle: {timeout-per-shutdown-phase: "${APP_SHUTDOWN_TIMEOUT}"}}
```

Each generated configuration enables bounded graceful shutdown without selecting a numeric deadline.

Generated target `AA011-T05`, `source/customer-app/notification-service/src/test/java/com/ecommerce/notification/service/GracefulShutdownTest.java`:

```java
@Test void listenerStopsAcceptingRecordsBeforeShutdownCompletes() { shutdownCoordinator.beginDrain(); assertThat(shutdownCoordinator.isReady()).isFalse(); verify(listenerRegistry).stop(); assertThat(shutdownCoordinator.awaitInFlight()).isTrue(); }
```

**Illustrative code status:** Targeted implementation discovery required for `AA011-T06` through `AA011-T16`.

| Target | Target file and location | Why code was not generated | Unresolved inputs | Intended behavior |
|---|---|---|---|---|
| AA011-T06 | `source/customer-app/api-gateway/src/test/java/com/ecommerce/gateway/lifecycle/HttpTerminationTest.java`, HTTP termination | No lifecycle symbol or frozen HTTP harness | Readiness symbol, HTTP fixture, in-flight accounting, drain deadline | Prove readiness drains before bounded completion |
| AA011-T07 | `source/customer-app/user-service/src/test/java/com/ecommerce/user/lifecycle/HttpTerminationTest.java`, HTTP termination | No lifecycle symbol or frozen HTTP harness | Readiness symbol, HTTP fixture, in-flight accounting, drain deadline | Prove no acceptance after drain |
| AA011-T08 | `source/customer-app/product-service/src/test/java/com/ecommerce/product/lifecycle/HttpTerminationTest.java`, HTTP termination | No lifecycle symbol or frozen HTTP harness | Readiness symbol, HTTP fixture, in-flight accounting, drain deadline | Prove bounded in-flight completion |
| AA011-T09 | `source/customer-app/notification-service/src/test/java/com/ecommerce/notification/lifecycle/HttpTerminationTest.java`, HTTP termination | HTTP entry point and harness are not established | HTTP applicability, readiness symbol, HTTP fixture, deadline | Test only if HTTP is applicable |
| AA011-T10 | `source/customer-app/api-gateway/src/test/java/com/ecommerce/gateway/lifecycle/KafkaTerminationTest.java`, Kafka termination | No gateway Kafka worker or lifecycle symbol | Kafka applicability, lifecycle symbol, in-flight accounting, deadline | Test acquisition stop when applicable |
| AA011-T11 | `source/customer-app/user-service/src/test/java/com/ecommerce/user/lifecycle/KafkaTerminationTest.java`, Kafka termination | No producer shutdown coordinator or broker harness | Producer lifecycle, accounting, Kafka fixture, deadline | Preserve completed or recoverable publication |
| AA011-T12 | `source/customer-app/product-service/src/test/java/com/ecommerce/product/lifecycle/KafkaTerminationTest.java`, Kafka termination | No producer shutdown coordinator or broker harness | Producer lifecycle, accounting, Kafka fixture, deadline | Preserve completed or recoverable publication |
| AA011-T13 | `source/customer-app/api-gateway/src/test/java/com/ecommerce/gateway/lifecycle/AsyncTerminationTest.java`, async termination | No asynchronous worker or lifecycle symbol | Async applicability, executor lifecycle, accounting, deadline | Reject work after drain when applicable |
| AA011-T14 | `source/customer-app/user-service/src/test/java/com/ecommerce/user/lifecycle/AsyncTerminationTest.java`, async termination | No asynchronous worker or lifecycle symbol | Async applicability, executor lifecycle, accounting, deadline | Reject work after drain when applicable |
| AA011-T15 | `source/customer-app/product-service/src/test/java/com/ecommerce/product/lifecycle/AsyncTerminationTest.java`, async termination | No asynchronous worker or lifecycle symbol | Async applicability, executor lifecycle, accounting, deadline | Reject work after drain when applicable |
| AA011-T16 | `source/customer-app/notification-service/src/test/java/com/ecommerce/notification/lifecycle/AsyncTerminationTest.java`, async termination | No shutdown coordinator, executor symbol, or frozen harness | Executor lifecycle, accounting, provider fixture, deadline | Complete accepted work or record recoverable state |

**Validation requirements:** Terminate all four services under applicable load and prove readiness withdrawal, stopped acquisition, bounded completion, and recoverable unfinished work.

**Dependencies:** Ownership, consumer completion, durable state, distributed scheduling, test foundation, and approved drain budgets.

**Notes:**

* Cross-refs: `F-011`, `CHANGE-AA-011`, wave 4
* Implementation: Five generated targets and eleven blocked harness targets
* Validation: Module tests followed by `mvn verify`
* Guardrail: Platform grace must exceed the approved application drain budget

<span style="font-size: 14px;">**MSFT Reference:** Grounded control `APP-AA-017`.</span>

### P1 High Priority

#### P1-001: Dependency operations lack complete bounded budgets and isolation

**Priority: P1 - failover certification blocker**

**Priority policy:** `AA-REMEDIATION-PRIORITY` version `1.0.0`, rule `P1-RCV-001`

**Severity:** Critical

**Resiliency Related:** Yes

**Finding status:** Verified finding

**Issue:** Only partial global HTTP and Redis timeouts exist; complete acquisition, connect, read, query, transaction, retry, and overall budgets and pool isolation are absent.

**What does this solve:** Slow dependencies cannot consume unrelated request capacity beyond the failure-detection budget.

**Resiliency Impact:** Bounds regional dependency failure and limits propagation across otherwise unrelated paths.

**Recommended Fix:** Externalize current bounds, then discover and configure effective per-dependency nested budgets, isolated pools, and fault tests.

**Repository evidence:** `EV-F-002-01`, `EV-F-002-02`

**File:** `source/customer-app/api-gateway/src/main/resources/application.yml:31-31`

**Original source requiring update:**

```yaml
        connect-timeout: 5000
```

**File:** `source/customer-app/api-gateway/src/main/resources/application.yml:50-50`

```yaml
    timeout: 2000
```

**Fix:** Illustrative proposal only.

Generated target `AA002-T01`, gateway HTTP client:

```yaml
spring: {cloud: {gateway: {httpclient: {connect-timeout: "${GATEWAY_CONNECT_TIMEOUT_MS}", response-timeout: "${GATEWAY_RESPONSE_TIMEOUT}"}}}}
```

Generated target `AA002-T02`, Redis command timeout:

```yaml
spring: {redis: {timeout: "${REDIS_COMMAND_TIMEOUT}"}}
```

**Illustrative code status:** Targeted implementation discovery required for `AA002-T03` through `AA002-T23`.

| Target | Target file and symbol | Why code was not generated | Unresolved inputs | Intended behavior |
|---|---|---|---|---|
| AA002-T03 | `source/customer-app/user-service/src/main/resources/application.yml`, user SQL budgets | SQL Server, Hikari, JPA, transaction properties and approved deadlines are unknown | Caller, acquisition, connect, query, transaction, retry budgets; property names | Bound and isolate every user SQL operation |
| AA002-T04 | `source/customer-app/order-service/src/main/resources/application.yml`, order SQL budgets | SQL Server, Hikari, JPA, transaction properties and approved deadlines are unknown | Caller, acquisition, connect, query, transaction, retry budgets; property names | Bound and isolate every order SQL operation |
| AA002-T05 | `source/customer-app/payment-service/src/main/resources/application.yml`, payment SQL budgets | SQL Server, Hikari, JPA, transaction properties and approved deadlines are unknown | Caller, acquisition, connect, query, transaction, retry budgets; property names | Bound and isolate every payment SQL operation |
| AA002-T06 | `source/customer-app/api-gateway/src/main/resources/application.yml`, user-service HTTP pool | Per-route Reactor Netty API and approved budgets are unknown | Pool API, acquisition, connect, read, retry, overall budgets | Isolate the user route and nest deadlines |
| AA002-T07 | `source/customer-app/api-gateway/src/main/resources/application.yml`, product-service HTTP pool | Per-route Reactor Netty API and approved budgets are unknown | Pool API, acquisition, connect, read, retry, overall budgets | Isolate the product route and nest deadlines |
| AA002-T08 | `source/customer-app/api-gateway/src/main/resources/application.yml`, order-service HTTP pool | Per-route Reactor Netty API and approved budgets are unknown | Pool API, acquisition, connect, read, retry, overall budgets | Isolate the order route and nest deadlines |
| AA002-T09 | `source/customer-app/api-gateway/src/main/resources/application.yml`, inventory-service HTTP pool | Per-route Reactor Netty API and approved budgets are unknown | Pool API, acquisition, connect, read, retry, overall budgets | Isolate the inventory route and nest deadlines |
| AA002-T10 | `source/customer-app/api-gateway/src/main/resources/application.yml`, payment-service HTTP pool | Per-route Reactor Netty API and approved budgets are unknown | Pool API, acquisition, connect, read, retry, overall budgets | Isolate the payment route and nest deadlines |
| AA002-T11 | `source/customer-app/api-gateway/src/main/resources/application.yml`, cart-service HTTP pool | Per-route Reactor Netty API and approved budgets are unknown | Pool API, acquisition, connect, read, retry, overall budgets | Isolate the cart route and nest deadlines |
| AA002-T12 | `source/customer-app/api-gateway/src/main/resources/application.yml`, notification-service HTTP pool | Per-route Reactor Netty API and approved budgets are unknown | Pool API, acquisition, connect, read, retry, overall budgets | Isolate the notification route and nest deadlines |
| AA002-T13 | `source/customer-app/product-service/src/main/resources/application.yml`, Redis pool and budget | Effective pool properties, capacities, and deadlines are unknown | Pool API/capacity; acquisition, connect, command, retry, overall budgets | Bound and isolate cache operations |
| AA002-T14 | `source/customer-app/product-service/src/main/resources/application.yml`, Cosmos budget | Effective Cosmos tuning API, capacity, and deadlines are unknown | Client API, concurrency, acquisition, connect, read, retry, overall budgets | Bound and isolate product Cosmos operations |
| AA002-T15 | `source/customer-app/inventory-service/src/main/resources/application.yml`, Cosmos budget | Effective Cosmos tuning API, capacity, and deadlines are unknown | Client API, concurrency, acquisition, connect, read, retry, overall budgets | Bound and isolate inventory Cosmos operations |
| AA002-T16 | `source/customer-app/cart-service/src/main/resources/application.yml`, Cosmos budget | Effective Cosmos tuning API, capacity, and deadlines are unknown | Client API, concurrency, acquisition, connect, read, retry, overall budgets | Bound and isolate cart Cosmos operations |
| AA002-T17 | `source/customer-app/api-gateway/src/main/resources/application.yml`, Key Vault budget | Effective Spring Cloud Azure API and deadlines are unknown | Client API, connect, read, retry, overall budgets | Bound gateway Key Vault access without coupling capacity |
| AA002-T18 | `source/customer-app/product-service/src/main/resources/application.yml`, Key Vault budget | Effective Spring Cloud Azure API and deadlines are unknown | Client API, connect, read, retry, overall budgets | Bound product Key Vault access without coupling capacity |
| AA002-T19 | `source/customer-app/api-gateway/src/test/java/com/ecommerce/gateway/config/GatewayDependencyBudgetTest.java`, seven routes | No frozen HTTP fault harness; route construction unresolved | Fault server, route API, approved budgets | Prove route isolation and bounded failure |
| AA002-T20 | `source/customer-app/api-gateway/src/test/java/com/ecommerce/gateway/config/RedisDependencyBudgetTest.java`, Redis clients | No frozen Redis fault harness; product pool unresolved | Redis fixture, client API, budgets | Prove bounded Redis starvation and failure |
| AA002-T21 | `source/customer-app/common/src/test/java/com/ecommerce/common/sql/SqlDependencyBudgetContractTest.java`, three SQL services | No SQL fault fixture or verified transaction bindings | SQL fixture, transaction API, budgets | Apply one SQL budget contract suite |
| AA002-T22 | `source/customer-app/common/src/test/java/com/ecommerce/common/cosmos/CosmosDependencyBudgetContractTest.java`, three services | No Cosmos fixture or verified client API | Cosmos fixture, client API, budgets | Prove bounded retry and isolated capacity |
| AA002-T23 | `source/customer-app/common/src/test/java/com/ecommerce/common/keyvault/KeyVaultDependencyBudgetContractTest.java`, two services | No Key Vault fixture or verified client API | Key Vault fixture, client API, budgets | Prove bounded delay and isolation |

**Validation requirements:** Inject latency and starvation independently for each dependency and prove bounded caller failure, pool isolation, and unaffected routes within the overall deadline.

**Dependencies:** P0-001, P0-005, P3-002, approved budgets, and verified client APIs.

**Notes:**

* Cross-refs: `F-002`, `CHANGE-AA-002`, wave 2
* Implementation: Two generated configuration targets and 21 blocked client/test targets
* Validation: `mvn -pl api-gateway,user-service,order-service,payment-service -am verify`
* Guardrail: Numeric examples are not approved production values

<span style="font-size: 14px;">**MSFT Reference:** Grounded controls `APP-AA-004`, `APP-AA-006`, `SQL-002`, `HTTP-001`, `HTTP-003`, and `REDIS-005`.</span>

---

#### P1-002: Redis rate-limit failure is converted to successful request processing

**Priority: P1 - unsafe degraded-mode blocker**

**Priority policy:** `AA-REMEDIATION-PRIORITY` version `1.0.0`, rule `P1-RCV-006`

**Severity:** Critical

**Resiliency Related:** Yes

**Finding status:** Verified finding

**Issue:** Any Redis error logs the exception message and admits the protected request.

**What does this solve:** Redis loss no longer disables throttling silently.

**Resiliency Impact:** Prevents a regional Redis outage from disabling authentication and API throttling and shifting abusive load downstream.

**Recommended Fix:** Route Redis errors through an explicit endpoint-specific policy; fail authentication closed and use only an approved independently bounded fallback elsewhere.

**Repository evidence:** `EV-F-003-01`

**File:** `source/customer-app/api-gateway/src/main/java/com/ecommerce/gateway/filter/RateLimitFilter.java:65-65`

**Original source requiring update:**

```java
                    log.error("Redis error in rate limiting, allowing request: {}", e.getMessage());
```

**Fix:** Illustrative proposal only.

Generated target `AA003-T01`, assessed filter:

```java
return redisDecision.onErrorResume(error -> failurePolicy.onRedisFailure(exchange, authenticationPath));
```

Generated target `AA003-T02`, `source/customer-app/api-gateway/src/main/java/com/ecommerce/gateway/filter/RateLimitFailurePolicy.java`:

```java
public interface RateLimitFailurePolicy { Mono<Void> onRedisFailure(ServerWebExchange exchange, boolean authenticationPath); }
```

Generated target `AA003-T03`, `source/customer-app/api-gateway/src/test/java/com/ecommerce/gateway/filter/RateLimitFilterTest.java`:

```java
@Test void deniesAuthenticationWhenRedisTimesOut() { assertThat(runAuthenticationRequestWithRedisFailure()).isEqualTo(HttpStatus.SERVICE_UNAVAILABLE); }
```

**Validation requirements:** Force timeout, disconnect, and command failures; verify approved authentication and general API outcomes, separate metrics, and recovery.

**Dependencies:** Test foundation, regional telemetry, P2-002 atomic limiter, and approval of general API degraded behavior.

**Notes:**

* Cross-refs: `F-003`, `CHANGE-AA-003`, wave 2
* Implementation: Three generated targets
* Validation: `mvn -pl api-gateway -am verify`
* Guardrail: Authentication denial remains fail closed during rollback

<span style="font-size: 14px;">**MSFT Reference:** Grounded controls `REDIS-020`, `REDIS-017`, `REDIS-021`, `APP-REACT-003`, and `APP-FALLBACK-001`.</span>

### P2 Moderate Priority

#### P2-001: Kafka consumer failures are swallowed after external side effects

**Priority: P2 - data and processing correctness**

**Priority policy:** `AA-REMEDIATION-PRIORITY` version `1.0.0`, rule `P2-DATA-002`

**Severity:** Critical

**Resiliency Related:** Yes

**Finding status:** Verified finding

**Issue:** Notification listeners perform asynchronous side effects, swallow exceptions, and have no durable dedupe or delivery ledger.

**What does this solve:** Notification delivery cannot be silently lost or repeated without durable completion evidence.

**Resiliency Impact:** Aligns offset completion, replay, and promotion with durable delivery status.

**Recommended Fix:** Make normal return represent durable completion, persist stable delivery identity, allow retryable failure to escape, and quarantine exhausted records for authorized replay.

**Repository evidence:** `EV-F-005-01`

**File:** `source/customer-app/notification-service/src/main/java/com/ecommerce/notification/service/NotificationEventConsumer.java:49-49`

**Original source requiring update:**

```java
            log.error("Failed to send order confirmation email: {}", e.getMessage());
```

**Fix:** Illustrative proposal only.

Generated target `AA005-T01`, assessed consumer:

```java
@KafkaListener(topics = KafkaTopics.ORDER_CREATED, groupId = KafkaTopics.GROUP_NOTIFICATION_SERVICE) public void handleOrderCreated(Map<String, Object> event) { deliveryService.deliverOrderConfirmation((String) event.get("eventId"), event); }
```

Generated target `AA005-T02`, `source/customer-app/notification-service/src/main/java/com/ecommerce/notification/service/NotificationDeliveryLedger.java`:

```java
public interface NotificationDeliveryLedger { DeliveryDecision begin(String eventId, String channel, String destination); void markDelivered(String eventId, String providerReference); void markRetryableFailure(String eventId, String failureCode); void markTerminalFailure(String eventId, String failureCode); }
```

Generated target `AA005-T03`, `source/customer-app/notification-service/src/test/java/com/ecommerce/notification/service/NotificationEventConsumerTest.java`:

```java
@Test void failureBeforeAcceptanceEscapesForRetry() { doThrow(retryableFailure()).when(deliveryService).deliverOrderConfirmation(eventId, event); assertThatThrownBy(() -> consumer.handleOrderCreated(event)).isInstanceOf(RuntimeException.class); }
@Test void replayAfterRecordedDeliveryDoesNotRepeatEffect() { ledger.recordDelivered(eventId); consumer.handleOrderCreated(event); verifyNoInteractions(provider); }
@Test void ambiguousAcceptanceRemainsRecoverable() { doThrow(ambiguousFailure()).when(provider).send(any()); assertThat(ledger.status(eventId)).isEqualTo(DeliveryStatus.RETRYABLE_FAILED); }
```

**Illustrative code status:** Targeted implementation discovery required (`AA005-T04`, durable ledger adapter, path not yet selected)

**Why code was not generated:** No approved durable store or provider completion contract is selected.

**Unresolved inputs:** Durable store; provider acceptance status; reconciliation contract.

**Intended behavior:** Persist delivery identity and completion state across restart and promotion.

**Illustrative code status:** Targeted implementation discovery required (`AA005-T05`, quarantine publisher, path not yet selected)

**Why code was not generated:** Quarantine destination, retention, replay authorization, and effective Spring Kafka error-handler API are unresolved.

**Unresolved inputs:** Quarantine topic; retention; replay authorization; Spring Kafka API.

**Intended behavior:** Preserve exhausted records for authorized replay with terminal status.

**Validation requirements:** Inject failure before, during, and after provider acceptance; verify retry, dedupe, terminal state, quarantine, rebalance, and replay.

**Dependencies:** Ownership, durable notification state, test foundation, provider and quarantine decisions.

**Notes:**

* Cross-refs: `F-005`, `CHANGE-AA-005`, wave 4
* Implementation: Three generated targets and two blocked adapters
* Validation: `mvn -pl notification-service -am verify`
* Guardrail: P0 elevation was evaluated; required critical-transaction materiality was not established

<span style="font-size: 14px;">**MSFT Reference:** Grounded controls `KAFKA-004`, `KAFKA-003`, `KAFKA-AS-006`, `APP-KAFKA-002`, and `APP-AA-011`.</span>

---

#### P2-002: Redis rate-limit keys and expiration are hardcoded and non-atomic

**Priority: P2 - data correctness**

**Priority policy:** `AA-REMEDIATION-PRIORITY` version `1.0.0`, rule `P2-DATA-001`

**Severity:** High

**Resiliency Related:** Yes

**Finding status:** Verified finding

**Issue:** Limits and window are constants, keys expose client IP without environment or schema version, and increment and expiration are separate.

**What does this solve:** Rate-limit counters cannot become immortal, collide across environments, or expose raw client identity.

**Resiliency Impact:** Preserves count and TTL correctness across interruption and regional operation.

**Recommended Fix:** Bind validated external policy, protect identity, namespace keys, and atomically update count and first-write expiry.

**Repository evidence:** `EV-F-014-01`

**File:** `source/customer-app/api-gateway/src/main/java/com/ecommerce/gateway/filter/RateLimitFilter.java:27-27`

**Original source requiring update:**

```java
    private static final int DEFAULT_REQUESTS_PER_MINUTE = 100;
```

**Fix:** Illustrative proposal only.

Generated target `AA014-T01`, `source/customer-app/api-gateway/src/main/java/com/ecommerce/gateway/filter/RateLimitProperties.java`:

```java
@ConfigurationProperties("app.rate-limit") @Validated public record RateLimitProperties(@Min(1) int defaultRequests, @Min(1) int authenticationRequests, @NotNull Duration window, @NotBlank String environment, @NotBlank String schemaVersion) {}
```

Generated target `AA014-T02`, `source/customer-app/api-gateway/src/main/resources/redis/rate-limit.lua`:

```lua
local count = redis.call('INCR', KEYS[1]); if count == 1 then redis.call('PEXPIRE', KEYS[1], ARGV[1]); end; return count
```

Generated target `AA014-T03`, `source/customer-app/api-gateway/src/test/java/com/ecommerce/gateway/filter/AtomicRateLimitTest.java`:

```java
@Test void atomicIncrementAlwaysCreatesExpiry() { assertThat(rateLimiter.increment(clientIdentity)).isEqualTo(1L); assertThat(redisTemplate.getExpire(rateLimiter.keyFor(clientIdentity))).isPositive(); }
```

**Validation requirements:** Test interruption between count and expiry, namespace isolation, protected identifiers, invalid configuration, recovery, and Redis cluster key-slot behavior.

**Dependencies:** Regional endpoints, test foundation, diagnostic safety, telemetry, and approved limits/window/namespace/digest policy.

**Notes:**

* Cross-refs: `F-014`, `CHANGE-AA-014`, wave 1
* Implementation: Three generated targets
* Validation: `mvn -pl api-gateway -am verify`
* Guardrail: P0 elevation was evaluated; required critical-transaction corruption was not established

<span style="font-size: 14px;">**MSFT Reference:** Grounded controls `REDIS-011`, `REDIS-017`, `REDIS-021`, `REDIS-022`, and `APP-CONF-014`.</span>

### P3 Optimization

#### P3-001: Generated user string output exposes authentication secrets

**Priority: P3 - diagnostic safety**

**Priority policy:** `AA-REMEDIATION-PRIORITY` version `1.0.0`, rule `P3-OPS-005`

**Severity:** Critical

**Resiliency Related:** Yes

**Finding status:** Verified finding

**Issue:** Generated `toString` excludes password and addresses but includes two-factor, verification, and password-reset secrets.

**What does this solve:** Reusable authentication material cannot enter generated diagnostics or structured serialization.

**Resiliency Impact:** Prevents secret replication into centralized regional telemetry during failure handling.

**Recommended Fix:** Exclude every observed protected field from strings and structured serialization and test both representations.

**Repository evidence:** `EV-F-009-01`, `EV-F-009-02`

**File:** `source/customer-app/user-service/src/main/java/com/ecommerce/user/entity/UserEntity.java:29-29`

**Original source requiring update:**

```java
@EqualsAndHashCode(exclude = {"addresses", "roles"})
```

**File:** `source/customer-app/user-service/src/main/java/com/ecommerce/user/entity/UserEntity.java:86-86`

```java
    @Column(name = "two_factor_secret")
```

**Fix:** Illustrative proposal only.

Generated targets `AA009-T01` and `AA009-T03`, assessed entity:

```java
@ToString(exclude = {"password", "addresses", "twoFactorSecret", "verificationToken", "passwordResetToken"})
```

```java
@JsonIgnore private String password;
@JsonIgnore private String twoFactorSecret;
@JsonIgnore private String verificationToken;
@JsonIgnore private String passwordResetToken;
```

Generated targets `AA009-T02` and `AA009-T04`, `source/customer-app/user-service/src/test/java/com/ecommerce/user/entity/UserEntityDiagnosticsTest.java`:

```java
@Test void generatedStringExcludesAuthenticationMaterial() { UserEntity user = protectedUser(); assertThat(user.toString()).doesNotContain(password, twoFactorSecret, verificationToken, passwordResetToken); }
```

```java
@Test void structuredSerializationExcludesAuthenticationMaterial() throws Exception { String json = objectMapper.writeValueAsString(protectedUser()); assertThat(json).doesNotContain(password, twoFactorSecret, verificationToken, passwordResetToken); }
```

**Validation requirements:** Populate every protected field and prove no supported diagnostic or serialization form contains it.

**Dependencies:** Test foundation.

**Notes:**

* Cross-refs: `F-009`, `CHANGE-AA-009`, wave 1
* Implementation: Four generated targets
* Validation: `mvn -pl user-service -am test`
* Guardrail: Future protected fields require explicit exclusion tests

<span style="font-size: 14px;">**MSFT Reference:** Grounded controls `APP-LOG-002`, `APP-LOG-001`, and `KV-013`.</span>

---

#### P3-002: Regional telemetry identity is incomplete

**Priority: P3 - operational attribution**

**Priority policy:** `AA-REMEDIATION-PRIORITY` version `1.0.0`, rule `P3-OPS-001`

**Severity:** Medium

**Resiliency Related:** Yes

**Finding status:** Verified finding

**Issue:** Order, inventory, payment, and cart services lack validated regional metric identity.

**What does this solve:** Operators can attribute failure, ownership, and recovery to the serving region.

**Resiliency Impact:** Enables regional diagnosis of lag, retry, ownership, fallback, and recovery without high-cardinality endpoint tags.

**Recommended Fix:** Inject one validated low-cardinality deployment-region value into service metrics and safe structured events.

**Repository evidence:** `EV-F-012-01`

**File:** `source/customer-app/order-service/src/main/resources/application.yml:82-82`

**Original source requiring update:**

```yaml
      prometheus:
```

**Fix:** Illustrative proposal only.

Generated target `AA012-T01`, `source/customer-app/order-service/src/main/resources/application.yml`, symbol `management.metrics.tags.region`:

```yaml
management: {metrics: {tags: {region: "${APP_DEPLOYMENT_REGION}"}}}
```

Generated target `AA012-T02`, `source/customer-app/inventory-service/src/main/resources/application.yml`, symbol `management.metrics.tags.region`:

```yaml
management: {metrics: {tags: {region: "${APP_DEPLOYMENT_REGION}"}}}
```

Generated target `AA012-T03`, `source/customer-app/payment-service/src/main/resources/application.yml`, symbol `management.metrics.tags.region`:

```yaml
management: {metrics: {tags: {region: "${APP_DEPLOYMENT_REGION}"}}}
```

Generated target `AA012-T04`, `source/customer-app/cart-service/src/main/resources/application.yml`, symbol `management.metrics.tags.region`:

```yaml
management: {metrics: {tags: {region: "${APP_DEPLOYMENT_REGION}"}}}
```

**Validation requirements:** Run two regional configurations and verify nonempty bounded region tags on representative failure and recovery signals.

**Dependencies:** Regional endpoint configuration, test foundation, and canonical region vocabulary.

**Notes:**

* Cross-refs: `F-012`, `CHANGE-AA-012`, wave 1
* Implementation: Four generated targets
* Validation: Module tests followed by `mvn verify`
* Guardrail: Do not use endpoint hostnames or arbitrary values as metric tags

<span style="font-size: 14px;">**MSFT Reference:** Grounded controls `APP-AA-015`, `APP-AA-016`, `APP-OBS-002`, `APP-OBS-003`, and `REDIS-025`.</span>

---

#### P3-003: Actuator health details are exposed unconditionally

**Priority: P3 - management security maturity**

**Priority policy:** `AA-REMEDIATION-PRIORITY` version `1.0.0`, rule `P3-OPS-005`

**Severity:** Medium

**Resiliency Related:** Yes

**Finding status:** Verified finding

**Issue:** Gateway and order-service always disclose health details, and gateway exposes its administrative endpoint.

**What does this solve:** Anonymous callers cannot obtain dependency details or administrative endpoint behavior.

**Resiliency Impact:** Reduces topology disclosure during regional degradation while preserving status-only probes.

**Recommended Fix:** Minimize endpoint exposure, restrict details to an approved operations role, and keep public probes status-only.

**Repository evidence:** `EV-F-013-01`

**File:** `source/customer-app/api-gateway/src/main/resources/application.yml:127-127`

**Original source requiring update:**

```yaml
      show-details: always
```

**Fix:** Illustrative proposal only.

Generated target `AA013-T01`, gateway management endpoints:

```yaml
management: {endpoints: {web: {exposure: {include: "health,info,metrics,prometheus"}}}, endpoint: {health: {show-details: when_authorized}}}
```

Generated target `AA013-T02`, order-service health details:

```yaml
management: {endpoint: {health: {show-details: when_authorized}}}
```

**Illustrative code status:** Targeted implementation discovery required (`AA013-T03`, `Management SecurityFilterChain`, path not yet selected)

**Why code was not generated:** The owning security chain, operations role, and management network boundary are not established.

**Unresolved inputs:** Security chain owner; operations role; management boundary.

**Intended behavior:** Authorize detailed management responses only for the approved operations role and boundary.

**Validation requirements:** Verify anonymous status-only probes, authorized details, and denied gateway administration.

**Dependencies:** Test foundation and approved operations role/management boundary.

**Notes:**

* Cross-refs: `F-013`, `CHANGE-AA-013`, wave 1
* Implementation: Two generated configuration targets and one blocked security target
* Validation: `mvn -pl api-gateway,order-service -am verify`
* Guardrail: Keep public probes available but status-only

<span style="font-size: 14px;">**MSFT Reference:** Grounded controls `APP-ACT-003`, `APP-ACT-001`, and `APP-ACT-002`.</span>

[Back to Top](#top)

## 3. Non-Resiliency-Focused Recommendations

No approved finding is classified as non-resiliency-related. This section is retained to satisfy the governing schema. PCF references are excluded.

### Verified controls

The following 13 evidence-backed controls require no application code change and are excluded from finding counts:

* Master standard: `APP-AA-001`, `APP-AA-008`, `APP-AA-012`, `APP-REACT-001`, `APP-REACT-002`, `APP-API-001`, `APP-CORRECT-001`
* Azure Key Vault: `KV-002`
* Confluent Kafka: `KAFKA-009`
* HTTP client: `HTTP-007`
* Azure Managed Redis: `REDIS-001`, `REDIS-004`, `REDIS-024`

[Back to Top](#top)

## 4. Repository and IaC Evidence Gap Analysis

The review assessed repository-visible application behavior and declarations. It did not assess deployed infrastructure. Missing infrastructure evidence remains an evidence gap and is not infrastructure noncompliance.

### Available to review

| Repository-visible configuration | Current evidence | Application resiliency interpretation | Related findings |
|---|---|---|---|
| Maven parent and nine modules | Java 17, Spring Boot 3.2.5, eight services and one library | Establishes build and dependency scope | P0-005 |
| Application YAML | Client endpoints, partial timeouts, health, telemetry, shutdown | Establishes effective repository defaults and gaps | P0-001, P0-007, P1-001, P3-002, P3-003 |
| Java source | HTTP, Kafka, Redis, schedulers, repositories, diagnostics | Establishes application processing and state behavior | P0-002, P0-003, P0-004, P0-006, P1-002, P2-001, P2-002, P3-001 |
| Azure Pipelines YAML | Maven verification and empty coverage allowed | Establishes current release verification behavior | P0-005 |
| Docker health checks | Eight service health checks | Shows repository health-check intent | Verified controls and evidence gaps |
| Kubernetes manifests | Eight liveness and eight readiness probes | Shows repository deployment intent, not deployed state | P0-007 and lifecycle evidence gaps |
| Terraform declarations | West US and service resource intent | Does not prove deployed topology or compliance | None; infrastructure excluded |
| Documentation | AKS and West US intent | Descriptive only | Assessment metadata |

### Not available or externally owned

| External evidence or configuration | Needed to validate | Related findings or assumptions |
|---|---|---|
| Deployed infrastructure state | Confirm actual resources, regions, routing, and settings | Repository intent only; no infrastructure finding |
| Kafka cluster topology, linking, and replication | Confirm active-standby topology and non-stretched deployment | P0-002 condition and Kafka scenario |
| Regional Kafka role assignment | Confirm which region may consume authoritative work | P0-002 |
| Cosmos DB multi-region write state | Confirm deployed regional write semantics | P0-002, P0-006 assumptions |
| Azure SQL failover group and ownership signal | Select authoritative role and fencing input | P0-002 |
| External Kafka consumers | Establish downstream replay and identity contracts | P0-003, P2-001 |
| SMTP/provider acceptance and reconciliation | Distinguish delivered, failed, and ambiguous outcomes | P2-001 |
| Effective listener acknowledgement behavior | Verify offset progression under failure | P2-001 |
| Approved durable-store choices | Select outbox, delivery ledger, notification, and claim adapters | P0-003, P0-004, P0-006, P2-001 |
| Operations role and management boundary | Implement detailed health authorization | P3-003 |
| Approved client budgets and runtime fault evidence | Freeze properties, fixtures, and nested deadlines | P1-001 |

The inventory also records unresolved Kafka, SMTP, and frontend aliases, the `azure-managed-redis` to `azure_managed_redis` registry-key mapping, and absence of approved architecture-context YAML. Seventy-three controls remain `not_assessed`; none is converted into a confirmed defect in this report.

### PCF exclusion

> PCF and its aliases are retired and excluded from findings, scoring, remediation, modernization, migration, and cleanup recommendations. Historical repository references, if discovered, are informational only and are not included in the finding matrix.

[Back to Top](#top)

## 5. Full Finding Matrix

| ID | Priority | Severity | Resiliency related | Status | Category | Finding | Change ID | Source ID | Repository scope |
|---|---|---|---|---|---|---|---|---|---|
| [P0-001](#p0-001-regional-dependency-endpoints-are-hardcoded) | P0 | Critical | Yes | Verified | Regional configuration | Regional dependency endpoints are hardcoded | CHANGE-AA-001 | F-001 | Gateway and product configuration |
| [P0-002](#p0-002-active-standby-kafka-work-has-no-regional-ownership-gate) | P0 | Critical | Yes | Conditional | Workload ownership | Active-standby Kafka work has no regional ownership gate | CHANGE-AA-004 | F-004 | Inventory listener and scheduler |
| [P0-003](#p0-003-kafka-producer-completion-and-event-identity-are-not-durable) | P0 | Critical | Yes | Verified | Messaging durability | Kafka producer completion and event identity are not durable | CHANGE-AA-006 | F-006 | User event publisher |
| [P0-004](#p0-004-notification-records-are-stored-only-in-process-memory) | P0 | Critical | Yes | Verified | Durable state | Notification records are stored only in process memory | CHANGE-AA-007 | F-007 | Notification repository |
| [P0-005](#p0-005-failure-and-recovery-behavior-has-no-automated-tests) | P0 | Critical | Yes | Verified | Verification | Failure and recovery behavior has no automated tests | CHANGE-AA-008 | F-008 | Build and pipeline |
| [P0-006](#p0-006-scheduled-shared-state-work-has-no-distributed-ownership) | P0 | Critical | Yes | Verified | Scheduler ownership | Scheduled shared-state work has no distributed ownership | CHANGE-AA-010 | F-010 | Inventory scheduler |
| [P0-007](#p0-007-graceful-shutdown-is-not-configured-consistently) | P0 | High | Yes | Verified | Lifecycle | Graceful shutdown is not configured consistently | CHANGE-AA-011 | F-011 | Four service configurations |
| [P1-001](#p1-001-dependency-operations-lack-complete-bounded-budgets-and-isolation) | P1 | Critical | Yes | Verified | Dependency resilience | Dependency operations lack complete bounded budgets and isolation | CHANGE-AA-002 | F-002 | Gateway and material clients |
| [P1-002](#p1-002-redis-rate-limit-failure-is-converted-to-successful-request-processing) | P1 | Critical | Yes | Verified | Security fallback | Redis rate-limit failure is converted to successful request processing | CHANGE-AA-003 | F-003 | Gateway rate limiter |
| [P2-001](#p2-001-kafka-consumer-failures-are-swallowed-after-external-side-effects) | P2 | Critical | Yes | Verified | Messaging consistency | Kafka consumer failures are swallowed after external side effects | CHANGE-AA-005 | F-005 | Notification consumer |
| [P2-002](#p2-002-redis-rate-limit-keys-and-expiration-are-hardcoded-and-non-atomic) | P2 | High | Yes | Verified | Redis data correctness | Redis rate-limit keys and expiration are hardcoded and non-atomic | CHANGE-AA-014 | F-014 | Gateway rate limiter |
| [P3-001](#p3-001-generated-user-string-output-exposes-authentication-secrets) | P3 | Critical | Yes | Verified | Diagnostic security | Generated user string output exposes authentication secrets | CHANGE-AA-009 | F-009 | User entity |
| [P3-002](#p3-002-regional-telemetry-identity-is-incomplete) | P3 | Medium | Yes | Verified | Observability | Regional telemetry identity is incomplete | CHANGE-AA-012 | F-012 | Four service configurations |
| [P3-003](#p3-003-actuator-health-details-are-exposed-unconditionally) | P3 | Medium | Yes | Verified | Management security | Actuator health details are exposed unconditionally | CHANGE-AA-013 | F-013 | Gateway and order configuration |

Matrix reconciliation: 14 approved findings, comprising 13 verified and one conditional finding. Priority counts are seven P0, two P1, two P2, and three P3. Severity counts are ten critical, two high, and two medium. Verified controls, observations, not-assessed controls, accepted risks, and PCF references are excluded.

[Back to Top](#top)

## 6. Standards Alignment

| Standard or pattern | Assessment status | Related controls | Related findings |
|---|---|---|---|
| Spring Boot AKS active-active master 4.0.0 | Applied; seven controls verified and application-level noncompliance preserved in findings | APP-AA, APP-REACT, APP-ACT, APP-LOG, APP-WORKLOAD, APP-SCHED, APP-OBS families | All findings |
| Azure Key Vault 2.0.0 | Applied; KV-002 verified, remaining results preserved | KV-001, KV-002, KV-008, KV-013 | P0-001, P0-005, P1-001, P3-001 |
| Azure Cosmos DB 1.0.0 | Applied; deployment facts remain external | COSMOS-001, COSMOS-008 | P0-001, P0-005, P1-001, P0-006 |
| Azure SQL 2.0.0 | Applied; deployment ownership remains external | SQL-002, SQL-008 | P0-002, P0-005, P1-001 |
| Confluent Kafka 3.0.0 | Applied with inferred active-standby scenario; KAFKA-009 verified | KAFKA-001..012 and KAFKA-AS controls as assessed | P0-001, P0-002, P0-003, P0-005, P2-001 |
| HTTP client 2.0.0 | Applied; HTTP-007 verified | HTTP-001, HTTP-003, HTTP-007 | P1-001 |
| Azure Managed Redis 2.0.0 | Applied; REDIS-001, REDIS-004, REDIS-024 verified | REDIS-003, REDIS-005, REDIS-011, REDIS-017, REDIS-020..027 as assessed | P0-001, P0-005, P1-001, P1-002, P2-002, P3-002 |
| PCF exclusion 1.0.0 | Applied as retired and suppressed | None included in assessment counts | None |

Input exceptions: the dependency registry carries stale Kafka `2.0.0` values and a nonexistent nested Redis path. Under artifact precedence, the report uses the Step 2 authoritative Kafka standard `3.0.0`, scenario policy `3.1.0`, and `grounding/dependencies/springboot-azure-managed-redis.md`. These corrections do not alter a finding or priority.

[Back to Top](#top)

## 7. Implementation Roadmap

This roadmap summarizes the authoritative Step 3A plan. It does not replace that plan or authorize implementation.

### Priority summary

| Priority | Change count | Primary objective | Release gate |
|---|---:|---|---|
| P0 | 7 | Remove traffic, integrity, state, verification, and authoritative-processing blockers | Before active-active release |
| P1 | 2 | Bound failure amplification and enforce safe Redis degradation | Before failover certification |
| P2 | 2 | Correct replay, delivery, and rate-limit state semantics | Before full active-active enablement |
| P3 | 3 | Complete diagnostic safety, regional telemetry, and management maturity | Before operational acceptance |

### Implementation waves

| Wave | Change IDs | Findings addressed | Prerequisites | Validation focus |
|---|---|---|---|---|
| 1 | CHANGE-AA-001, 008, 009, 012, 013, 014 | F-001, F-008, F-009, F-012, F-013, F-014 | Production inputs, security boundary, policy approvals | Regional binding, verification, diagnostics, telemetry, access, atomic TTL |
| 2 | CHANGE-AA-002, 003 | F-002, F-003 | Wave 1; approved budgets and degraded policy | Latency, starvation, isolation, denial/fallback, restoration |
| 3 | CHANGE-AA-006, 007 | F-006, F-007 | Approved stores, schemas, retention, fencing, encryption, migration | Stable identity, restart, recoverable publication, durable state |
| 4 | CHANGE-AA-004, 005, 010, 011 | F-004, F-005, F-010, F-011 | Waves 1-3; ownership, provider, quarantine, and claim decisions | Fenced roles, completion, scheduler claims, bounded drain |

Wave 1 parallel groups are `[001,008]`, `[009,012]`, `[013]`, and `[014]`; changes 012 and 013 are serialized because both modify order-service application YAML. Wave 2 groups are `[002]` and `[003]`. Wave 3 groups are `[006]` and `[007]`. Wave 4 groups are `[004]`, `[005,010]`, and `[011]`.

### Change index

| Change ID | Priority | Priority rule | Finding IDs | Objective | Complexity | Wave |
|---|---|---|---|---|---|---:|
| CHANGE-AA-001 | P0 | P0-AA-001 | F-001 | Require injected regional endpoints | Medium | 1 |
| CHANGE-AA-002 | P1 | P1-RCV-001 | F-002 | Define nested dependency budgets and isolation | High | 2 |
| CHANGE-AA-003 | P1 | P1-RCV-006 | F-003 | Enforce explicit Redis failure policy | Medium | 2 |
| CHANGE-AA-004 | P0 | P0-AA-006 | F-004 | Gate work on fenced regional ownership | High | 4 |
| CHANGE-AA-005 | P2 | P2-DATA-002 | F-005 | Align offset completion with durable side-effect state | High | 4 |
| CHANGE-AA-006 | P0 | P0-AA-006 | F-006 | Persist stable event identity and recover publication | High | 3 |
| CHANGE-AA-007 | P0 | P0-AA-005 | F-007 | Replace process-local required notification state | High | 3 |
| CHANGE-AA-008 | P0 | P0-AA-007 | F-008 | Establish executable failure and coverage gates | Medium | 1 |
| CHANGE-AA-009 | P3 | P3-OPS-005 | F-009 | Exclude authentication material from diagnostics | Low | 1 |
| CHANGE-AA-010 | P0 | P0-AA-006 | F-010 | Claim bounded shared-state work atomically | High | 4 |
| CHANGE-AA-011 | P0 | P0-RCV-008 | F-011 | Coordinate readiness, acquisition stop, drain, and termination | High | 4 |
| CHANGE-AA-012 | P3 | P3-OPS-001 | F-012 | Add validated region identity to service signals | Low | 1 |
| CHANGE-AA-013 | P3 | P3-OPS-005 | F-013 | Restrict management detail and administration | Medium | 1 |
| CHANGE-AA-014 | P2 | P2-DATA-001 | F-014 | Atomically update namespaced protected rate-limit state | Medium | 1 |

### Targeted implementation discovery

Forty target-specific records require discovery before implementation. They cover 21 dependency-budget client and test targets, one regional ownership adapter, two notification delivery adapters, one outbox adapter, two notification persistence targets, one scheduler claim adapter, eleven lifecycle test harnesses, and one management security chain. Each blocked target is rendered in its related finding with a specific reason, unresolved inputs, and intended behavior. They do not block report conformance and must not be replaced by fabricated code.

### Approval boundary

Step 4 uses `.copilot-tracking/plans/2026-09-02/springboot-active-active-authoritative-remediation-plan.instructions.md` and explicit approval selectors. It supports `APPROVED_PRIORITIES`, `APPROVED_WAVES`, and `APPROVED_CHANGE_IDS`. Priority approval is preferred. Step 4 resolves and freezes change IDs before modifying source code. This report and its handoff do not authorize implementation.

[Back to Top](#top)

<!--
illustrative_code_conformance:
  applicable_targets: 83
  generated_code_blocks_rendered: 43
  targeted_discovery_targets_rendered: 40
  not_applicable_targets: 0
  invalid_generated_proposals: 0
  narrative_only_code_blocks_rendered: 0
  status: passed
schema_conformance:
  schema_id: CODE-LEVEL-RESILIENCY-ASSESSMENT-REPORT
  schema_version: "1.2.0"
  required_sections_present: true
  required_section_order_valid: true
  required_finding_fields_present: true
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
  summary_counts_reconcile: true
  finding_matrix_reconciles: true
  roadmap_matches_plan: true
  unsupported_findings_added: false
  priorities_changed: false
  infrastructure_findings_added: false
  pcf_findings_added: false
  report_written_by_step_3b: true
  delegated_to_task_implementor: false
  status: passed
-->