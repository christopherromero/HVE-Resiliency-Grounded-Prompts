<a id="top"></a>

<!-- report-governance:start -->
<!--
report_governance:
  schema_id: CODE-LEVEL-RESILIENCY-ASSESSMENT-REPORT
  schema_version: "1.11.0"
  schema_path: grounding/governance/assessment-report-schema.md
  schema_validation: passed
  generated_by_phase: Step 3B
  artifact_type: assessment_documentation
  implementation_artifact: false
-->
<!--
report_assembly_manifest:
  report_path: .copilot-tracking/plans/reports/code-level-resiliency-assessment.md
  selected_priorities: [P0, P1, P2, P3]
  omitted_priorities: []
  selected_finding_ids: [F-001, F-002, F-003, F-004, F-005, F-006, F-007, F-008, F-009, F-010, F-011, F-012, F-013, F-014, F-015, F-016, F-017, F-018, F-019, F-020, F-021, F-022, F-023, F-024, F-025, F-026, F-027, F-028, F-029]
  selected_change_ids: [CHANGE-AA-001, CHANGE-AA-002, CHANGE-AA-003, CHANGE-AA-004, CHANGE-AA-005, CHANGE-AA-006, CHANGE-AA-007, CHANGE-AA-008, CHANGE-AA-009, CHANGE-AA-010, CHANGE-AA-011, CHANGE-AA-012, CHANGE-AA-013, CHANGE-AA-014, CHANGE-AA-015, CHANGE-AA-016, CHANGE-AA-017, CHANGE-AA-018, CHANGE-AA-019, CHANGE-AA-020, CHANGE-AA-021, CHANGE-AA-022, CHANGE-AA-023, CHANGE-AA-024]
  expected_finding_count: 29
  display_id_map:
    P0-001: F-003
    P0-002: F-004
    P0-003: F-008
    P0-004: F-021
    P0-005: F-022
    P0-006: F-024
    P0-007: F-026
    P0-008: F-027
    P0-009: F-028
    P1-001: F-001
    P1-002: F-005
    P1-003: F-006
    P1-004: F-009
    P1-005: F-010
    P1-006: F-011
    P1-007: F-012
    P1-008: F-013
    P1-009: F-014
    P1-010: F-015
    P1-011: F-016
    P1-012: F-017
    P1-013: F-018
    P1-014: F-019
    P1-015: F-023
    P1-016: F-025
    P1-017: F-029
    P2-001: F-002
    P2-002: F-007
    P2-003: F-020
  sections:
    - assessment_overview
    - resiliency_recommendations
    - non_resiliency_recommendations
    - evidence_gap_analysis
    - full_finding_matrix
    - standards_alignment
    - implementation_roadmap
    - appendix_traceability
  assembly_status:
    report_initialized: true
    completed_sections:
      - assessment_overview
      - resiliency_recommendations
      - non_resiliency_recommendations
      - evidence_gap_analysis
      - full_finding_matrix
      - standards_alignment
      - implementation_roadmap
      - appendix_traceability
    completed_finding_ids: [F-001, F-002, F-003, F-004, F-005, F-006, F-007, F-008, F-009, F-010, F-011, F-012, F-013, F-014, F-015, F-016, F-017, F-018, F-019, F-020, F-021, F-022, F-023, F-024, F-025, F-026, F-027, F-028, F-029]
    recovery_count: 0
    final_validation_complete: true
-->
<!-- report-governance:end -->

# Code-Level Resiliency Assessment

<!-- report-metadata:start -->

| Field                      | Value                                                                                     |
|----------------------------|-------------------------------------------------------------------------------------------|
| Application                | Ecommerce Platform - Inventory Service                                                     |
| Assessment date            | 2026-09-18                                                                                 |
| Repository scope           | `source/inventory-service` (single microservice repository)                                |
| Current deployment         | Active-standby: West US active, East US reserved for disaster recovery                     |
| Approved target deployment | Active-active across West US 2 and West US using the same application artifact             |
| Migration context          | Target-state code readiness assessment; the target is not claimed to be deployed           |
| Language and framework     | Java, Spring Boot 3.3.5, Maven                                                             |
| Runtime platform           | Azure Kubernetes Service                                                                   |
| Report version             | 1.0                                                                                        |

<!-- report-metadata:end -->

## Table of Contents

- [Assessment Overview](#assessment-overview)
- [Resiliency-Focused Recommendations](#resiliency-recommendations)
- [Non-Resiliency-Focused Recommendations](#non-resiliency-recommendations)
- [Repository and IaC Evidence Gap Analysis](#evidence-gap-analysis)
- [Full Finding Matrix](#full-finding-matrix)
- [Standards Alignment](#standards-alignment)
- [Implementation Roadmap](#implementation-roadmap)
- [Appendix A: Traceability](#appendix-traceability)

<!-- section:assessment-overview -->
## Assessment Overview

<!-- content:assessment-overview:start -->

### Application and repository overview

The Inventory Service is a single Spring Boot 3.3.5 Maven module that owns inventory quantity for the Ecommerce Platform. It exposes seven REST endpoints under `/api/v1/inventory`, consumes the `order-events` topic through one `@KafkaListener` in the `inventory-service` consumer group, publishes to `inventory-events`, and treats Azure SQL as its authoritative business state. Azure Managed Redis is used strictly as a non-authoritative read cache with a repository fallback on miss, and Azure Key Vault supplies secrets at startup. The service runs on Azure Kubernetes Service behind Application Gateway.

The assessment boundary is the repository at `source/inventory-service`. Six dependencies were confirmed from production code and production configuration rather than from build declarations alone: Azure SQL, Confluent Kafka, Azure Managed Redis, Azure Key Vault, the JVM runtime, and Application Gateway with global load balancing.

### Deployment evolution

**Current deployment:** West US is the active production region and East US is reserved for disaster recovery. The application operates active-standby with a single-active traffic model.

**Approved target deployment:** The approved target runs the same application artifact actively in West US 2 and West US, with a multi-active traffic model.

**Migration context:** This assessment evaluates application code readiness for the approved target state while preserving existing business behaviour. It does not claim the target infrastructure is deployed, and the difference between the current and target states is not itself a finding. Azure SQL remains active-standby in the approved target and is reported separately from the application deployment topology.

### Assessment scope

Two assessment domains were enabled: application code and application configuration. Container build, CI/CD pipeline, deployment configuration, infrastructure as code, and deployed infrastructure were disabled. The repository contains a Dockerfile, a GitHub Actions workflow, and Kubernetes manifests, and those artifacts were deliberately not assessed. Facts that depend on them are recorded as evidence gaps rather than as findings.

This report renders all governed priorities, P0 through P3. Test detail, validation commands, acceptance criteria, and validation evidence are suppressed by the configured testing-output preference; every test and validation obligation remains binding in the authoritative remediation plan.

Authoritative artifacts:

- Inventory: `.copilot-tracking/research/2026-09-18/inventory-service-inventory-research.md`
- Findings and control results: `.copilot-tracking/reviews/2026-09-18/inventory-service-inventory-research-review.md`
- Remediation plan: `.copilot-tracking/plans/2026-09-18/inventory-service-remediation-plan.instructions.md`

### Assessment snapshot and source locators

> Source line numbers are advisory and identify the location observed in the assessed snapshot. Repository path, symbol, exact source excerpt, and source fingerprint are the primary evidence locators. The assessment snapshot may be a Git revision, workspace snapshot, uploaded archive, or source drop. Git metadata is optional.

**Assessment snapshot:** Workspace snapshot `inventory-service-workspace-2026-09-18`

**Snapshot provenance:** Workspace generated

**Snapshot limitations:** No Git metadata exists at the workspace root or under `source/inventory-service`, so no commit identifier is available. Evidence is anchored by repository path, symbol, and exact excerpt rather than by revision. Line ranges may shift if the source drop is replaced.

### Kafka operating scenario

| Attribute                            | Value                                                                    |
|--------------------------------------|--------------------------------------------------------------------------|
| Operating scenario                   | `active_standby`                                                          |
| Scenario source                      | Approved application architecture context, version 3.0.0                  |
| Scenario policy                      | `KAFKA-OPERATING-SCENARIO` version 3.2.0, rule `KAFKA-SCENARIO-001`        |
| Scenario validation status           | Consistent                                                                |
| Architecture confirmation required   | No                                                                        |
| Processing model                     | Mixed request-driven and event-driven                                     |
| Regional processing model            | Single active                                                             |
| External side effects                | None                                                                      |
| Kafka-backed authoritative state     | None; Azure SQL holds authoritative business state                        |
| Cluster model                        | Independent regional clusters, not stretched                              |

The scenario was supplied by approved architecture context and validated as consistent because Azure SQL is the authoritative business state. Kafka active-standby processing describes event consumption ownership only. It is not the application deployment model, and it does not prove the deployed Kafka topology. Deployed cluster topology, Cluster Linking, and consumer-offset replication remain unresolved infrastructure facts recorded in the evidence gap analysis.

### Assessment themes

Six themes account for the 29 findings.

**Regional ownership is not expressible in code.** The Kafka listener has no identifier and no activation control, so which region consumes `order-events` cannot be set, changed, or observed without a redeploy (P0-002). Order-event processing and the REST reserve and release paths apply stock movements with no durable operation identity, so promotion replay, consumer rebalance redelivery, and gateway retry each multiply inventory movements (P0-001).

**Traffic eligibility does not reflect dependency health.** Readiness and health rely entirely on framework defaults, so a pod whose authoritative database is unreachable continues to advertise itself as ready and continues to receive regional traffic (P0-003).

**Lifecycle transitions are unbounded or destructive.** Startup performs an unbounded Key Vault import (P0-005) and applies Hibernate schema changes in every profile including production (P0-006), while termination performs no readiness withdrawal and no draining (P0-004).

**Failures are invisible at regional granularity.** Telemetry carries no region or role dimension (P0-007), no metric or log record distinguishes a dependency failure from normal operation (P0-008), and no test exercises failure or failover behaviour (P0-009). Together these prevent any regional failure test from being interpreted and prevent a both-active condition from being confirmed or refuted.

**Remote calls and cached reads are unbounded.** No repository-owned deadline exists for Azure SQL, Redis, or Kafka (P1-004, P1-005, P1-006). There is no bounded retry for transient database failures (P1-007), no optimistic-conflict handling (P1-008), no stable caller-visible failure semantics (P1-009), and no isolation between request threads and blocking dependencies (P1-010). Cache failures propagate into the request path (P1-011), cached entries never expire (P1-012), and concurrent misses are not coalesced (P1-014). The list endpoint loads the entire inventory table into memory (P1-016).

**Event delivery carries no durability or identity guarantee.** Publication is fire-and-forget with no observed outcome (P1-001), consumer offsets advance past permanently failing records (P1-002), poison records have no dead-letter route (P1-003), publication occurs inside the database transaction with no outbox (P2-001), and published events carry no stable identity or correlation context (P2-002).

Three additional findings are evidence-backed control violations that manifest during normal operation rather than during a failure or recovery event. They are preserved as non-resiliency findings: cache keys without namespace or schema version (P1-013), reliance on default JDK serialization for a non-serializable cached type (P1-017), and reserve and release mutating inventory without invalidating the cache (P2-003).

### Approved Azure Shared Services Reference Architectures

| Azure Shared Service             | Architecture Title                                          | Reference                                                                                                                                                                                                                                                                                                                                                                                              | Approval Status | Version      |
|----------------------------------|-------------------------------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-----------------|--------------|
| Azure Application Gateway        | Albertsons Architecture Design - Application Gateway v1.0    | [Reference](https://rxsafeway.sharepoint.com/:w:/r/sites/Cloud2.0/Shared%20Documents/I11%20Resiliency%20Program/Discovery/Integration%20Platform/AppGW/Design/Albertsons%20Architecture%20Design_Application%20Gateway_v1.0.docx?d=w3126f533271842c9a75d83ae93b6b6db&csf=1&web=1&e=hmksie)                                                                                                                | approved        | v1.0         |
| Azure Key Vault                  | Albertsons Azure Key Vault Architecture Design Proposal      | [Reference](https://rxsafeway.sharepoint.com/:w:/r/sites/Cloud2.0/Shared%20Documents/I11%20Resiliency%20Program/Discovery/Cloud%20Foundation/Design/Albertsons%20Azure%20Key%20Vault%20Architecture%20Design%20Proposal.docx?d=wf1abecab2812460a8cadd6e5956d5bb8&csf=1&web=1&e=yzvvQh)                                                                                                                    | approved        | v1.0         |
| Azure Kubernetes Service (AKS)   | Albertsons Architecture Design - AKS and Istio v1.0          | [Reference](https://rxsafeway.sharepoint.com/:w:/r/sites/Cloud2.0/Shared%20Documents/I11%20Resiliency%20Program/Discovery/Container%20Platform/Design/Albertsons%20Architecture%20Design_AKS%20and%20Istio_v1.0.docx?d=w97c0edfea59d466e80af843958d95c5c&csf=1&web=1&e=7UJSQS)                                                                                                                            | approved        | v1.0         |
| Azure Managed Redis              | Managed Redis - Albertsons Multi-Region Design v3            | [Reference](https://rxsafeway.sharepoint.com/:w:/r/sites/Cloud2.0/Shared%20Documents/I11%20Resiliency%20Program/Discovery/Database%20Platform/Redis/Design/Managed%20Redis%20-%20Albertsons%20Multi-Region%20Design%20v3.docx?d=wad90acec4c154b2498d899a2ffcdc9d4&csf=1&web=1&e=L7pVbQ)                                                                                                                   | approved        | v3           |
| Azure SQL Database               | Azure SQL Database architecture design library               | [Reference](https://rxsafeway.sharepoint.com/:f:/r/sites/Cloud2.0/Shared%20Documents/I11%20Resiliency%20Program/Discovery/Database%20Platform/SQL%20DB?csf=1&web=1&e=xMauSY)                                                                                                                                                                                                                             | approved        | not_provided |
| Kafka                            | Approved Albertsons Region Resiliency - Kafka Multi-Region   | [Reference](https://rxsafeway.sharepoint.com/:w:/r/sites/Cloud2.0/Shared%20Documents/I11%20Resiliency%20Program/Discovery/Integration%20Platform/Kafka/Approved_Albertsons_RegionResiliency_Kafka-MultiRegion.docx?d=w08142308135244de855f4dab4c49ca2d&csf=1&web=1&e=kueuJ9)                                                                                                                              | approved        | not_provided |

Document status by entry: Application Gateway final, Key Vault proposal, AKS and Istio final, Managed Redis final, Azure SQL document library, Kafka final. A reference architecture describes intended design. It is not evidence that infrastructure is deployed or configured correctly, and it is never used as repository source evidence for a finding.

### Summary findings

| Priority | Section                              | Confirmed count | Description                                                                                                       |
|----------|--------------------------------------|-----------------|-------------------------------------------------------------------------------------------------------------------|
| P0       | Resiliency-Focused Recommendations   | 9               | Regional ownership, replay safety, traffic eligibility, lifecycle transitions, and regional failure observability  |
| P1       | Resiliency-Focused Recommendations   | 15              | Bounded dependency deadlines, transient failure recovery, isolation, cache behaviour, and event durability         |
| P2       | Resiliency-Focused Recommendations   | 2               | Cross-store consistency through a transactional outbox and stable published event identity                        |
| P1       | Non-Resiliency-Focused Recommendations | 2             | Cache key contract and cached value compatibility                                                                 |
| P2       | Non-Resiliency-Focused Recommendations | 1             | Cache invalidation correctness on inventory mutation                                                              |
| Total    | All sections                         | 29              | 26 resiliency findings and 3 non-resiliency findings, all verified                                                |

All 29 findings are verified findings. No conditional findings were recorded. Evaluation covered 210 controls across eight loaded standards, of which 121 were applicable, 36 compliant, 85 non-compliant, 17 not assessed, and 72 not applicable. Severity distribution is 14 critical, 14 high, and 1 medium. Severity is inherited from the primary control in its governing standard. Remediation priority is governed separately by `AA-REMEDIATION-PRIORITY` version 1.0.0 and is not derived from severity, which produces three deliberate divergences noted in the Implementation Roadmap.

### Illustrative-code notice

> **IMPORTANT:** Hard numbers used for retry counts, timeout settings, interval timings, thread-pool sizes, cache duration, health thresholds, and circuit-breaker settings are examples unless the authoritative plan identifies an approved value. These values must be externally configurable and coordinated with application, mesh, gateway, and load-balancer budgets. All code snippets are illustrative proposals, not applied or prescriptive patches.

<!-- content:assessment-overview:end -->

[Back to Top](#top)

<!-- section:resiliency-recommendations -->
## Resiliency-Focused Recommendations

<!-- content:resiliency-recommendations:start -->
### Priority P0

<h3 style="color:#0F6CBD;">
Regional Ownership and Replay Safety
</h3>

<!-- finding:F-003 -->
#### P0-001: Order-event consumption and stock adjustment are not idempotent

**Priority: P0 - Critical risk**

**Priority policy:** AA-REMEDIATION-PRIORITY version 1.0.0

**Severity:** critical

**Resiliency Related:** Yes

**Finding status:** Verified finding

**Issue:** The order-event consumer maps `ORDER_CREATED` to `service.reserve` and `ORDER_CANCELLED` to `service.release`, passing the event `orderId` through as `referenceId`. The `reserve` and `release` methods apply relative quantity deltas to the `InventoryItem` entity. `referenceId` is never persisted, never checked, and never used to derive a stable operation identity. No reservation record, processed-event table, unique constraint on product and reference, or conditional update guards a repeated application, and the same gap applies to the `POST /products/{productId}/reserve` and `/release` endpoints.

**What does this solve:** Every stock adjustment gains a stable, durable operation identity so a repeated delivery of the same business operation produces exactly one stock movement. Promotion replay from a restored or reset offset, consumer rebalance redelivery, and container restart stop silently corrupting authoritative stock quantities. The documented failover procedure becomes safe to execute.

**Resiliency Impact:** At-least-once Kafka delivery, consumer rebalance, container restart, offset reset, active-standby promotion replay, and gateway or client retry of the POST endpoints all repeat the same business effect, and each repetition moves additional stock from available to reserved with no corrective path. Because `auto-offset-reset` is `earliest`, a lost or reset consumer-group offset replays the entire retained order-events history, which corrupts authoritative inventory quantities visible from both regions. Replay during recovery is inherent to the approved active-standby model, so this defect makes the recovery path itself unsafe. Idempotent adjustment is the precondition for a safe promotion.

**Recommended Fix:** Write a durable processed-operation record keyed by a stable identity derived from the operation type, the product identifier, and the reference identifier, inside the same transaction as the stock adjustment. Enforce the identity with a database unique constraint so a second application of the same operation fails at the database, and translate that failure into a no-op that returns the current inventory state. Derive the operation identity in the consumer from the consumed order event rather than generating one per attempt. The quantity arithmetic, exception types, and exception messages remain unchanged.

**File:** `source/inventory-service/src/main/java/com/ecommerce/inventory/kafka/consumer/OrderEventConsumer.java`:13-21

**Repository evidence:**

- Repository path: `source/inventory-service/src/main/java/com/ecommerce/inventory/kafka/consumer/OrderEventConsumer.java`
- Symbol: `OrderEventConsumer.consume`
- Source fingerprint: `sha256:f2448385d75d...`
- Assessment snapshot: Workspace snapshot `inventory-service-workspace-2026-09-18`
- Original assessed lines (advisory): 13-21

**Original source requiring update:**

```java
@KafkaListener(topics = "order-events", groupId = "inventory-service")
public void consume(Map<String, Object> event) {
    String type = String.valueOf(event.get("type"));
    String productId = String.valueOf(event.get("productId"));
    int quantity = ((Number) event.get("quantity")).intValue();
    String orderId = String.valueOf(event.get("orderId"));
    if ("ORDER_CREATED".equals(type)) service.reserve(productId, quantity, orderId);
    if ("ORDER_CANCELLED".equals(type)) service.release(productId, quantity, orderId);
}
```

**File:** `source/inventory-service/src/main/java/com/ecommerce/inventory/service/impl/InventoryServiceImpl.java`:37-50

**Repository evidence:**

- Repository path: `source/inventory-service/src/main/java/com/ecommerce/inventory/service/impl/InventoryServiceImpl.java`
- Symbol: `InventoryServiceImpl.reserve and InventoryServiceImpl.release`
- Source fingerprint: `sha256:0f2357c4e940...`
- Assessment snapshot: Workspace snapshot `inventory-service-workspace-2026-09-18`
- Original assessed lines (advisory): 37-50

**Original source requiring update:**

```java
@Override @Transactional
public InventoryResponse reserve(String productId, int quantity, String referenceId) {
    InventoryItem item = findByProduct(productId);
    if (item.getAvailableQuantity() < quantity) throw new IllegalArgumentException("Insufficient inventory for product: " + productId);
    item.setAvailableQuantity(item.getAvailableQuantity() - quantity); item.setReservedQuantity(item.getReservedQuantity() + quantity); item.setUpdatedAt(Instant.now());
    return saveAndPublish(item, "INVENTORY_RESERVED", referenceId);
}
@Override @Transactional
public InventoryResponse release(String productId, int quantity, String referenceId) {
    InventoryItem item = findByProduct(productId);
    if (item.getReservedQuantity() < quantity) throw new IllegalArgumentException("Release exceeds reserved inventory for product: " + productId);
    item.setReservedQuantity(item.getReservedQuantity() - quantity); item.setAvailableQuantity(item.getAvailableQuantity() + quantity); item.setUpdatedAt(Instant.now());
    return saveAndPublish(item, "INVENTORY_RELEASED", referenceId);
}
```

**Fix:**

**Proposed change: Processed operation entity** — `source/inventory-service/src/main/java/com/ecommerce/inventory/model/ProcessedOperation.java`

Illustrative proposal only.

```java
package com.ecommerce.inventory.model;

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import jakarta.persistence.Table;
import jakarta.persistence.UniqueConstraint;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.time.Instant;

@Entity
@Table(name = "processed_operations",
        uniqueConstraints = @UniqueConstraint(name = "UQ_processed_operations_identity", columnNames = "operationIdentity"))
@Data @Builder @NoArgsConstructor @AllArgsConstructor
public class ProcessedOperation {
    @Id @GeneratedValue(strategy = GenerationType.IDENTITY) private Long id;
    @Column(nullable = false, length = 512) private String operationIdentity;
    @Column(nullable = false, length = 64) private String operationType;
    @Column(nullable = false, length = 255) private String productId;
    @Column(nullable = false, length = 255) private String referenceId;
    @Column(nullable = false) private Instant processedAt;
}
```

The entity follows the existing `InventoryItem` conventions exactly: Lombok `@Data` with `@Builder`, an identity primary key, and a table-level unique constraint. `operationIdentity` is the stable key that makes a repeated application detectable, and the component parts are stored alongside it so an operator can inspect the record without parsing the key.

**Proposed change: Processed operation repository** — `source/inventory-service/src/main/java/com/ecommerce/inventory/repository/ProcessedOperationRepository.java`

Illustrative proposal only.

```java
package com.ecommerce.inventory.repository;

import com.ecommerce.inventory.model.ProcessedOperation;
import org.springframework.data.jpa.repository.JpaRepository;

public interface ProcessedOperationRepository extends JpaRepository<ProcessedOperation, Long> {
    boolean existsByOperationIdentity(String operationIdentity);
}
```

A derived query in the same style as the existing `existsByProductId` method on `InventoryRepository`. The existence check is the fast path; the unique constraint remains the authority under concurrency.

**Proposed change: Processed operation migration script** — `source/inventory-service/src/main/resources/db/migration/V2__processed_operation.sql`

Illustrative proposal only.

```sql
CREATE TABLE processed_operations (
    id                BIGINT IDENTITY(1,1) NOT NULL,
    operationIdentity VARCHAR(512)         NOT NULL,
    operationType     VARCHAR(64)          NOT NULL,
    productId         VARCHAR(255)         NOT NULL,
    referenceId       VARCHAR(255)         NOT NULL,
    processedAt       DATETIME2            NOT NULL,
    CONSTRAINT PK_processed_operations PRIMARY KEY (id),
    CONSTRAINT UQ_processed_operations_identity UNIQUE (operationIdentity)
);

CREATE INDEX IX_processed_operations_processedAt ON processed_operations (processedAt);
```

The unique constraint is what makes duplicate suppression correct under concurrency; the existence check in the repository is only an optimization. The `processedAt` index supports the retention purge that becomes necessary once a retention window is approved. The script is written in the same dialect as the baseline migration script and is applied by whichever migration runner the versioned schema migration change resolves to.

**Proposed change: Idempotent stock adjustment** — `source/inventory-service/src/main/java/com/ecommerce/inventory/service/impl/InventoryServiceImpl.java`

Illustrative proposal only.

```java
@Override
@Transactional(timeout = 10)
public InventoryResponse reserve(String productId, int quantity, String referenceId) {
    return applyOnce("INVENTORY_RESERVED", productId, referenceId, item -> {
        if (item.getAvailableQuantity() < quantity) {
            throw new IllegalArgumentException("Insufficient inventory for product: " + productId);
        }
        item.setAvailableQuantity(item.getAvailableQuantity() - quantity);
        item.setReservedQuantity(item.getReservedQuantity() + quantity);
    });
}

@Override
@Transactional(timeout = 10)
public InventoryResponse release(String productId, int quantity, String referenceId) {
    return applyOnce("INVENTORY_RELEASED", productId, referenceId, item -> {
        if (item.getReservedQuantity() < quantity) {
            throw new IllegalArgumentException("Release exceeds reserved inventory for product: " + productId);
        }
        item.setReservedQuantity(item.getReservedQuantity() - quantity);
        item.setAvailableQuantity(item.getAvailableQuantity() + quantity);
    });
}

private InventoryResponse applyOnce(String operationType,
                                    String productId,
                                    String referenceId,
                                    Consumer<InventoryItem> adjustment) {
    InventoryItem item = findByProduct(productId);
    String operationIdentity = operationIdentity(operationType, productId, referenceId);

    if (processedOperations.existsByOperationIdentity(operationIdentity)) {
        telemetry.recordConsumption(operationType, InventoryTelemetry.OUTCOME_DUPLICATE);
        return mapper.toResponse(item);
    }

    adjustment.accept(item);
    item.setUpdatedAt(Instant.now());

    try {
        processedOperations.saveAndFlush(ProcessedOperation.builder()
                .operationIdentity(operationIdentity)
                .operationType(operationType)
                .productId(productId)
                .referenceId(referenceId)
                .processedAt(Instant.now())
                .build());
    } catch (DataIntegrityViolationException duplicate) {
        telemetry.recordConsumption(operationType, InventoryTelemetry.OUTCOME_DUPLICATE);
        throw new DuplicateOperationException(operationIdentity, duplicate);
    }

    return saveAndPublish(item, operationType, referenceId);
}

private static String operationIdentity(String operationType, String productId, String referenceId) {
    return operationType + ':' + productId + ':' + referenceId;
}
```

Both adjustment paths route through one method that derives a stable operation identity, checks for a prior application, performs the existing business precondition and quantity arithmetic unchanged, and writes the deduplication record inside the same transaction. The existence check is the fast path and the unique constraint is the authority under concurrency, which is why the constraint violation is caught and translated rather than allowed to surface as a generic failure. The quantity arithmetic, the exception types, and the exception messages are preserved exactly as assessed so business semantics do not change. The explicit transaction timeout is the bounded dependency deadline obligation from P1-004 applied at the same edit site.

**Proposed change: Consumer-side operation identity** — `source/inventory-service/src/main/java/com/ecommerce/inventory/kafka/consumer/OrderEventConsumer.java`

Illustrative proposal only.

```java
try {
    switch (payload.type()) {
        case "ORDER_CREATED" -> service.reserve(payload.productId(), payload.quantity(), payload.orderId());
        case "ORDER_CANCELLED" -> service.release(payload.productId(), payload.quantity(), payload.orderId());
        default -> telemetry.recordConsumption(payload.type(), InventoryTelemetry.OUTCOME_SUCCESS);
    }
    telemetry.recordConsumption(payload.type(), InventoryTelemetry.OUTCOME_SUCCESS);
} catch (DuplicateOperationException alreadyApplied) {
    log.info("order event already applied operationIdentity={}", alreadyApplied.getOperationIdentity());
    telemetry.recordConsumption(payload.type(), InventoryTelemetry.OUTCOME_DUPLICATE);
}
acknowledgment.acknowledge();
```

The consumer continues to pass the event `orderId` through as the reference identifier, which is what makes the operation identity stable across redelivery, rebalance, restart, and promotion replay. A duplicate is treated as a completed operation rather than a failure, so the offset advances and the record is not retried or quarantined. The payload record and the acknowledgment parameter are supplied by the consumer acknowledgement and error-handling change described in P1-002; this block shows only the duplicate handling owned here. The business mapping of `ORDER_CREATED` to reserve and `ORDER_CANCELLED` to release is unchanged.

**Validation requirements:** Validation requires repository evidence that a repeated delivery of the same order operation produces exactly one stock movement and that the deduplication record is written in the same transaction as the adjustment it represents.

**Dependencies:** Depends on P0-006 and P0-008.

**Notes:**

- Implementation: The deduplication record lives in Azure SQL, which the approved architecture already declares as the authoritative business state, so no new datastore is introduced.
- Validation: Closure requires evidence that a full replay of the retained order-events history against a populated database produces no additional stock movement.
- Guardrail: The REST idempotency-key contract, including behaviour for an absent or blank reference identifier, is an approval-gated business-logic decision and is excluded from this change; consumer-side deduplication proceeds independently because order events always carry an order identifier.

<span style="font-size: 14px;">**Standards reference:** springboot-aks-active-active-master v4.0.0 — `grounding/master/springboot-aks-active-active-master.md`</span>

---

<!-- finding:F-004 -->
#### P0-002: Kafka listener has no region-role activation control

**Priority: P0 - Critical risk**

**Priority policy:** AA-REMEDIATION-PRIORITY version 1.0.0

**Severity:** critical

**Resiliency Related:** Yes

**Finding status:** Verified finding

**Issue:** The `@KafkaListener` declares only `topics` and `groupId`. It has no `id`, no `autoStartup` attribute, no `containerFactory` reference, and no property-driven enablement. No endpoint-registry manipulation, lease acquisition, ownership epoch, fencing token, or Azure SQL primary-role verification exists in production source. Every started instance in every region therefore begins consuming `order-events` immediately, and no repository-owned mechanism can start or stop consumption when the regional role changes.

**What does this solve:** Kafka consumption becomes a deployment-controlled, observable, and reversible decision. A standby-region deployment can be configured not to consume, a promotion can start consumption without a redeploy, and the current activation state is visible so a both-active condition can be detected.

**Resiliency Impact:** The approved Kafka regional processing model is single active and the authoritative Azure SQL state is active-standby. With no activation control, a standby-region deployment consumes and mutates authoritative inventory concurrently with the active region, and a stale former-active instance continues consuming after a promotion. Both conditions produce split-brain writes against a single authoritative database. The role change also cannot be applied by configuration alone, so a documented failover runbook would require a code change to execute.

**Recommended Fix:** Give the listener a stable identifier and an `autoStartup` expression bound to an externalized activation property, defaulting to the current behaviour so no existing deployment silently stops consuming. Add an activation component that starts and stops the named listener container through the listener endpoint registry, reports the current activation state as a region-tagged gauge, and logs every activation transition. Self-enforced ownership through a lease or fencing token is deliberately not proposed because no approved mechanism exists.

**File:** `source/inventory-service/src/main/java/com/ecommerce/inventory/kafka/consumer/OrderEventConsumer.java`:13-14

**Repository evidence:**

- Repository path: `source/inventory-service/src/main/java/com/ecommerce/inventory/kafka/consumer/OrderEventConsumer.java`
- Symbol: `OrderEventConsumer @KafkaListener declaration`
- Source fingerprint: `sha256:3fb33358ad66...`
- Assessment snapshot: Workspace snapshot `inventory-service-workspace-2026-09-18`
- Original assessed lines (advisory): 13-14

**Original source requiring update:**

```java
@KafkaListener(topics = "order-events", groupId = "inventory-service")
public void consume(Map<String, Object> event) {
```

**Fix:**

**Proposed change: Listener identity and externalized activation** — `source/inventory-service/src/main/java/com/ecommerce/inventory/kafka/consumer/OrderEventConsumer.java`

Illustrative proposal only.

```java
@KafkaListener(
        id = "${app.kafka.consumer.listener-id:order-events-listener}",
        topics = "order-events",
        groupId = "inventory-service",
        autoStartup = "${app.kafka.consumer.enabled:true}",
        containerFactory = "orderEventListenerContainerFactory")
public void consume(Map<String, Object> event, Acknowledgment acknowledgment) {
```

The listener gains a stable identifier so the endpoint registry can address it, and an `autoStartup` expression so a deployment can decide whether this regional instance consumes. The default value is `true`, which preserves today's behaviour for every existing deployment. The topic and `groupId` are unchanged. The `containerFactory` reference and the `Acknowledgment` parameter are introduced by the consumer acknowledgement and error-handling change described in P1-002; they appear here because both changes edit the same declaration.

**Proposed change: Regional consumption controller** — `source/inventory-service/src/main/java/com/ecommerce/inventory/kafka/RegionalConsumptionController.java`

Illustrative proposal only.

```java
package com.ecommerce.inventory.kafka;

import io.micrometer.core.instrument.Gauge;
import io.micrometer.core.instrument.MeterRegistry;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.kafka.config.KafkaListenerEndpointRegistry;
import org.springframework.kafka.listener.MessageListenerContainer;
import org.springframework.stereotype.Component;

import jakarta.annotation.PostConstruct;

@Slf4j
@Component
public class RegionalConsumptionController {

    private final KafkaListenerEndpointRegistry registry;
    private final MeterRegistry meterRegistry;
    private final String listenerId;

    public RegionalConsumptionController(KafkaListenerEndpointRegistry registry,
                                         MeterRegistry meterRegistry,
                                         @Value("${app.kafka.consumer.listener-id:order-events-listener}") String listenerId) {
        this.registry = registry;
        this.meterRegistry = meterRegistry;
        this.listenerId = listenerId;
    }

    @PostConstruct
    void registerActivationGauge() {
        Gauge.builder("inventory.kafka.consumption.active", this, controller -> controller.isActive() ? 1d : 0d)
                .description("1 when this instance is consuming order-events, 0 when it is not")
                .tag("listenerId", listenerId)
                .register(meterRegistry);
        log.info("kafka consumption activation state={} listenerId={}", isActive(), listenerId);
    }

    public boolean isActive() {
        MessageListenerContainer container = registry.getListenerContainer(listenerId);
        return container != null && container.isRunning();
    }

    public void activate() {
        MessageListenerContainer container = requireContainer();
        if (!container.isRunning()) {
            container.start();
            log.info("kafka consumption transition=activated listenerId={}", listenerId);
        }
    }

    public void deactivate() {
        MessageListenerContainer container = requireContainer();
        if (container.isRunning()) {
            container.stop();
            log.info("kafka consumption transition=deactivated listenerId={}", listenerId);
        }
    }

    private MessageListenerContainer requireContainer() {
        MessageListenerContainer container = registry.getListenerContainer(listenerId);
        if (container == null) {
            throw new IllegalStateException("No Kafka listener container registered for id " + listenerId);
        }
        return container;
    }
}
```

The controller exposes start and stop for the named listener container and publishes the current activation state as a gauge. Combined with the region tag introduced by the regional telemetry change described in P0-007, an operator can see at a glance whether more than one region is consuming, which is the split-brain condition this finding describes. The controller reports and changes local activation only; it does not assign the regional role.

**Proposed change: Self-enforced single-active ownership** — target repository path not yet selected

**Illustrative code status:** Targeted implementation discovery required

**Why code was not generated:** No approved ownership, lease, or fencing mechanism exists in the repository or in the approved libraries governance file, and how standby-region consumption is prevented today remains unconfirmed. Selecting a lease store, a lease protocol, or a fencing token scheme would be an unapproved architecture decision, and it would also determine whether a new persistence target is introduced, which the approved architecture does not currently declare.

**Unresolved inputs:**
- Approved ownership and fencing mechanism for single-active consumption
- Confirmation of how standby-region consumption is prevented today
- Whether the lease may reside in the existing Azure SQL authoritative store or requires another mechanism

**Intended behavior:** Beyond deployment-controlled activation, the approved single-active model would be enforced by the application itself through an ownership lease with an epoch or fencing token, so that a stale former-active instance cannot resume consumption after a promotion even if its configuration still says enabled.

**Validation requirements:** Validation requires repository evidence that consumption can be disabled and enabled by configuration alone, that an intentionally inactive consumer still starts and reports readiness UP, and that every activation transition is observable.

**Dependencies:** Depends on P0-004, P0-007, and P0-008.

**Notes:**

- Implementation: The consumer group identifier, topic name, and payload contract are unchanged, and the default activation value preserves current behaviour for every existing deployment.
- Validation: Closure requires evidence that deactivation stops record acquisition before in-flight processing completes or is abandoned, reusing the shutdown drain contract from P0-004.
- Guardrail: The mechanism is deployment-controlled rather than self-fencing, so an operator can still enable consumption in both regions at once; the activation gauge makes that condition detectable but does not prevent it.

<span style="font-size: 14px;">**Standards reference:** springboot-aks-active-active-master v4.0.0 — `grounding/master/springboot-aks-active-active-master.md`</span>

---

<h3 style="color:#0F6CBD;">
Traffic Eligibility and Health
</h3>

<!-- finding:F-008 -->
#### P0-003: Readiness and health configuration relies entirely on framework defaults

**Priority: P0 - Critical risk**

**Priority policy:** AA-REMEDIATION-PRIORITY version 1.0.0

**Severity:** critical

**Resiliency Related:** Yes

**Finding status:** Verified finding

**Issue:** Health probes are enabled and no readiness or liveness group include or exclude list is configured, so the readiness group resolves to the framework default that contains only the application availability state. The auto-configured Azure SQL, Redis, and Kafka health contributors report into the aggregate health endpoint but do not participate in readiness. No custom health indicator exists and no health-check timeout is configured for any contributor. No production code publishes an availability change event or manipulates readiness state.

**What does this solve:** Readiness becomes a true statement about whether this regional deployment can serve its critical inventory capability, so the global load balancer can withdraw a failed region. Readiness recovers automatically after dependency restoration without a process restart, and every readiness transition becomes observable.

**Resiliency Impact:** A sustained Azure SQL outage in the serving region leaves every pod reporting readiness UP, so the global load balancer continues to send traffic to a region that cannot serve its critical capability and regional traffic is never withdrawn. Because no code path can change readiness, the approved regional failover behaviour has no application-side trigger at all. The same defaults leave dependency health checks unbounded, so during a dependency incident the aggregate health endpoint can block and add load to the failing dependency. This change supplies the application-side trigger the approved active-standby failover model requires.

**Recommended Fix:** Declare the readiness group explicitly so the authoritative Azure SQL contributor and the application availability state participate in traffic eligibility. Keep Redis out of readiness because it is a non-authoritative cache with a safe degraded mode, and keep Kafka out until the region-role activation contract exists to distinguish an intentionally inactive standby consumer from a failed one. Pin liveness to the application liveness state so external dependency loss cannot cause restart loops. Emit a region-tagged metric and a structured log record on every readiness transition.

**File:** `source/inventory-service/src/main/resources/application.yml`:29-37

**Repository evidence:**

- Repository path: `source/inventory-service/src/main/resources/application.yml`
- Symbol: `management.endpoints.web.exposure.include and management.endpoint.health.probes.enabled`
- Source fingerprint: `sha256:653a483edc8b...`
- Assessment snapshot: Workspace snapshot `inventory-service-workspace-2026-09-18`
- Original assessed lines (advisory): 29-37

**Original source requiring update:**

```yaml
management:
  endpoints:
    web:
      exposure:
        include: health,info,prometheus
  endpoint:
    health:
      probes:
        enabled: true
```

**File:** `source/inventory-service/src/main/java` (absence evidence; no line range recorded)

**Repository evidence:**

- Repository path: `source/inventory-service/src/main/java`
- Symbol: `absence of HealthIndicator, AvailabilityChangeEvent, and ReadinessState usage`
- Source fingerprint: not available for absence evidence
- Assessment snapshot: Workspace snapshot `inventory-service-workspace-2026-09-18`
- Original assessed lines (advisory): not available

**Original source requiring update:**

No source excerpt exists. The assessed condition is the absence of any health indicator, availability change event, or readiness state usage across production source.

**Fix:**

**Proposed change: Readiness and liveness group membership** — `source/inventory-service/src/main/resources/application.yml`

Illustrative proposal only.

```yaml
management:
  endpoints:
    web:
      exposure:
        include: health,info,prometheus
  endpoint:
    health:
      probes:
        enabled: true
      show-details: never
      group:
        readiness:
          include: readinessState,db
          show-details: never
          additional-path: never
        liveness:
          include: livenessState
  health:
    redis:
      enabled: true
    defaults:
      enabled: true
```

The readiness group is declared explicitly so the Azure SQL contributor participates in traffic eligibility. Redis stays out of readiness because it is a non-authoritative cache with a degraded read path supplied by the cache degradation change described in P1-011. Kafka stays out until the region-role activation contract described in P0-002 supplies the role contract. Liveness is pinned to the liveness state so external dependency loss cannot cause restart loops. Contributors remain enabled so the aggregate endpoint still reports them.

**Proposed change: Readiness transition observability** — `source/inventory-service/src/main/java/com/ecommerce/inventory/health/ReadinessTransitionListener.java`

Illustrative proposal only.

```java
package com.ecommerce.inventory.health;

import io.micrometer.core.instrument.MeterRegistry;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.boot.availability.AvailabilityChangeEvent;
import org.springframework.boot.availability.ReadinessState;
import org.springframework.context.event.EventListener;
import org.springframework.stereotype.Component;

@Slf4j
@Component
@RequiredArgsConstructor
public class ReadinessTransitionListener {

    private final MeterRegistry meterRegistry;

    @EventListener
    public void onReadinessChange(AvailabilityChangeEvent<ReadinessState> event) {
        ReadinessState state = event.getState();
        meterRegistry.counter("inventory.readiness.transition", "state", state.name()).increment();
        log.info("readiness state changed state={}", state);
    }
}
```

Every readiness transition produces exactly one counter increment and one structured log record. The region and role dimensions are supplied automatically by the Micrometer common tags introduced in the regional telemetry change described in P0-007, so they are not repeated here.

**Validation requirements:** Validation requires repository evidence that readiness reflects authoritative database health, recovers without a process or pod restart after connectivity is restored, and that liveness remains unaffected by dependency loss.

**Dependencies:** Depends on P0-007.

**Notes:**

- Implementation: The probe paths themselves are unchanged, so no gateway or Kubernetes probe path change is required; only readiness semantics change for platform probe consumers.
- Validation: Closure requires evidence that health details remain hidden from unauthenticated callers on the aggregate health endpoint.
- Guardrail: Including the authoritative database contributor in readiness can withdraw an entire region on a transient blip, so bounded deadlines and bounded retry must land alongside it, and Kubernetes probe timing remains outside the assessment boundary.

<span style="font-size: 14px;">**Standards reference:** springboot-aks-active-active-master v4.0.0 — `grounding/master/springboot-aks-active-active-master.md`</span>

---

<h3 style="color:#0F6CBD;">
Startup and Termination Lifecycle
</h3>

<!-- finding:F-021 -->
#### P0-004: No graceful shutdown, readiness withdrawal, or work draining

**Priority: P0 - Critical risk**

**Priority policy:** AA-REMEDIATION-PRIORITY version 1.0.0

**Severity:** high

**Resiliency Related:** Yes

**Finding status:** Verified finding

**Issue:** Neither profile configures graceful server shutdown or a per-phase shutdown timeout. No production class implements a lifecycle, disposal, or pre-destroy contract, and no code withdraws readiness before termination. The Kafka listener container and the servlet container therefore stop on the framework default immediate shutdown with no coordinated intake-stop or drain phase.

**What does this solve:** Pod termination becomes an ordered transition that first stops being eligible for traffic, then stops acquiring new work, then completes or cleanly abandons in-flight work within a bounded window. Rolling deployments, scale-in, node drains, and planned regional transitions stop cutting in-flight HTTP writes and stop interrupting Kafka records between the database write and the offset commit.

**Resiliency Impact:** On every rolling deployment, scale-in, node drain, and planned regional transition the pod stops accepting nothing and completes nothing. In-flight HTTP writes are cut mid-transaction and in-flight Kafka records are interrupted between the database write and the offset commit, which compounds the duplicate-processing exposure described in P0-001 and the loss exposure described in P1-002. Because readiness is never withdrawn first, the load balancer continues to send requests to a pod that is already terminating. The same mechanism supplies the controlled intake-stop that an active-standby role transfer requires.

**Recommended Fix:** Enable graceful server shutdown and declare an externally configured per-phase shutdown timeout. Introduce a lifecycle component that runs at the earliest shutdown phase, publishes a refusing-traffic readiness state so the load balancer withdraws the pod, then stops the Kafka listener containers so no new records are polled. The ordinary graceful web shutdown then drains in-flight HTTP requests within the configured window.

**File:** `source/inventory-service/src/main/resources/application-prod.yml`:1-12

**Repository evidence:**

- Repository path: `source/inventory-service/src/main/resources/application-prod.yml`
- Symbol: `absence of server.shutdown and spring.lifecycle.timeout-per-shutdown-phase`
- Source fingerprint: `sha256:f52a6730d9cb...`
- Assessment snapshot: Workspace snapshot `inventory-service-workspace-2026-09-18`
- Original assessed lines (advisory): 1-12

**Original source requiring update:**

```yaml
spring:
  config:
    import: azure-keyvault:${AZURE_KEYVAULT_ENDPOINT}
  datasource:
    url: ${SQL_CONNECTION_STRING}
  data:
    redis:
      url: ${REDIS_CONNECTION_STRING}
  kafka:
    bootstrap-servers: ${KAFKA_BOOTSTRAP_SERVERS}
    properties:
      security.protocol: ${KAFKA_SECURITY_PROTOCOL:PLAINTEXT}
```

The excerpt is the complete assessed prod profile and demonstrates the absence of any shutdown or lifecycle property. The proposed properties are placed in the default profile so both profiles inherit them.

**Fix:**

**Proposed change: Enable graceful shutdown** — `source/inventory-service/src/main/resources/application.yml`

Illustrative proposal only.

```yaml
server:
  port: 8082
  shutdown: graceful
spring:
  lifecycle:
    timeout-per-shutdown-phase: ${SHUTDOWN_PHASE_TIMEOUT}
app:
  lifecycle:
    readiness-withdrawal-delay: ${READINESS_WITHDRAWAL_DELAY}
```

Graceful shutdown lets the servlet container drain in-flight requests. The per-phase timeout and the readiness withdrawal delay are externalized so the total application drain window can be kept shorter than the platform termination grace period, which lives outside the remediation boundary.

**Proposed change: Ordered shutdown coordinator** — `source/inventory-service/src/main/java/com/ecommerce/inventory/lifecycle/GracefulShutdownCoordinator.java`

Illustrative proposal only.

```java
package com.ecommerce.inventory.lifecycle;

import lombok.extern.slf4j.Slf4j;
import org.springframework.boot.availability.AvailabilityChangeEvent;
import org.springframework.boot.availability.ReadinessState;
import org.springframework.context.ApplicationEventPublisher;
import org.springframework.context.SmartLifecycle;
import org.springframework.kafka.config.KafkaListenerEndpointRegistry;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Component;

import java.time.Duration;

@Slf4j
@Component
public class GracefulShutdownCoordinator implements SmartLifecycle {

    private final ApplicationEventPublisher publisher;
    private final KafkaListenerEndpointRegistry listenerRegistry;
    private final Duration readinessWithdrawalDelay;
    private volatile boolean running;

    public GracefulShutdownCoordinator(ApplicationEventPublisher publisher,
                                       KafkaListenerEndpointRegistry listenerRegistry,
                                       @Value("${app.lifecycle.readiness-withdrawal-delay}") Duration readinessWithdrawalDelay) {
        this.publisher = publisher;
        this.listenerRegistry = listenerRegistry;
        this.readinessWithdrawalDelay = readinessWithdrawalDelay;
    }

    @Override
    public int getPhase() {
        // Runs before the web server and the listener containers stop.
        return Integer.MIN_VALUE;
    }

    @Override
    public void start() {
        this.running = true;
    }

    @Override
    public void stop() {
        long startedAt = System.nanoTime();
        AvailabilityChangeEvent.publish(publisher, this, ReadinessState.REFUSING_TRAFFIC);
        log.info("shutdown phase=readiness_withdrawn delayMs={}", readinessWithdrawalDelay.toMillis());
        sleepQuietly(readinessWithdrawalDelay);

        listenerRegistry.getListenerContainers().forEach(container -> {
            container.stop();
            log.info("shutdown phase=listener_stopped listenerId={}", container.getListenerId());
        });

        this.running = false;
        log.info("shutdown phase=intake_stopped durationMs={}", (System.nanoTime() - startedAt) / 1_000_000);
    }

    @Override
    public boolean isRunning() {
        return running;
    }

    private void sleepQuietly(Duration duration) {
        try {
            Thread.sleep(duration.toMillis());
        } catch (InterruptedException interrupted) {
            Thread.currentThread().interrupt();
        }
    }
}
```

The coordinator runs at the earliest shutdown phase, so it executes before the web server and the Kafka listener containers are stopped by the ordinary lifecycle. It publishes a refusing-traffic state so the readiness probe reports OUT_OF_SERVICE, waits the configured withdrawal delay to let the load balancer notice, then stops every listener container so no new records are polled. The graceful web shutdown enabled by the configuration change then drains in-flight HTTP requests.

**Validation requirements:** Validation requires repository evidence that readiness reports OUT_OF_SERVICE before the servlet container stops accepting requests, that every Kafka listener container stops polling before in-flight record processing is abandoned, and that each shutdown phase and its duration are observable.

**Dependencies:** Depends on P0-003.

**Notes:**

- Implementation: Deployment and drain duration increase by the configured window, and no API or event contract changes.
- Validation: Closure requires evidence that an HTTP request in flight at termination completes when it finishes within the configured drain window.
- Guardrail: A drain window longer than the platform termination grace period is truncated by forced termination, which reintroduces the original failure, so the application-side window must be confirmed shorter than the platform grace period that lives outside the assessment boundary.

<span style="font-size: 14px;">**Standards reference:** springboot-aks-active-active-master v4.0.0 — `grounding/master/springboot-aks-active-active-master.md`</span>

---

<!-- finding:F-022 -->
#### P0-005: Startup depends on a mandatory Key Vault import with no bounded or optional contract

**Priority: P0 - Critical risk**

**Priority policy:** AA-REMEDIATION-PRIORITY version 1.0.0

**Severity:** critical

**Resiliency Related:** Yes

**Finding status:** Verified finding

**Issue:** The prod profile declares the Key Vault config import without the optional prefix, which makes the property source mandatory. No client options, retry options, startup timeout, or last-known-good policy is configured for the Key Vault client. No startup failure contract is documented anywhere in the enabled scope, so the wait is governed entirely by implicit SDK defaults.

**What does this solve:** Startup dependence on Key Vault becomes explicit, bounded, and observable. A throttle or transient identity failure produces a bounded, diagnosable startup failure rather than an unbounded stall, so a startup probe can tell a progressing startup from a stuck one.

**Resiliency Impact:** A Key Vault throttle, transient identity failure, private endpoint DNS delay, or access-policy issue prevents the application from starting at all. During a regional recovery this is exactly when many pods start simultaneously and are most likely to be throttled, so the recovering region cannot regain capacity and the outage extends beyond the dependency incident itself. Because the behaviour is neither bounded nor explicit, a startup probe cannot distinguish a progressing startup from a stuck one.

**Recommended Fix:** Declare an explicit, externally configured retry and timeout budget through the Key Vault secret client properties. Keep the import mandatory because the datasource and Redis credentials genuinely cannot be resolved without it, and state that contract explicitly in the profile where it is enforced. Every budget value resolves from a deployment-supplied placeholder so it can be aligned to the regional recovery budget without a code change.

**File:** `source/inventory-service/src/main/resources/application-prod.yml`:1-3

**Repository evidence:**

- Repository path: `source/inventory-service/src/main/resources/application-prod.yml`
- Symbol: `spring.config.import`
- Source fingerprint: `sha256:e7c1e56e4046...`
- Assessment snapshot: Workspace snapshot `inventory-service-workspace-2026-09-18`
- Original assessed lines (advisory): 1-3

**Original source requiring update:**

```yaml
spring:
  config:
    import: azure-keyvault:${AZURE_KEYVAULT_ENDPOINT}
```

**Fix:**

Illustrative proposal only.

```yaml
spring:
  config:
    # Mandatory by design: datasource and cache credentials cannot be resolved without it.
    import: azure-keyvault:${AZURE_KEYVAULT_ENDPOINT}
  cloud:
    azure:
      keyvault:
        secret:
          client:
            connect-timeout: ${KEYVAULT_CONNECT_TIMEOUT}
            response-timeout: ${KEYVAULT_RESPONSE_TIMEOUT}
          retry:
            mode: exponential
            exponential:
              max-retries: ${KEYVAULT_MAX_RETRIES}
              base-delay: ${KEYVAULT_RETRY_BASE_DELAY}
              max-delay: ${KEYVAULT_RETRY_MAX_DELAY}
```

The import stays mandatory because the credentials genuinely are required, but the wait is now bounded and tunable. Every budget resolves from a deployment-supplied placeholder, so no approved numeric value is asserted here and the values can be aligned to the regional recovery budget. The comment states the startup contract explicitly in the file where it is enforced.

**Validation requirements:** Validation requires repository evidence that the connect, response, and retry budgets are declared and overridable per environment, that no vault endpoint or credential is hardcoded in any profile, and that an unreachable Key Vault fails startup within the declared budget with a diagnosable message naming the property source.

**Dependencies:** None.

**Notes:**

- Implementation: The import remains mandatory, so no behavioural change occurs when Key Vault is healthy.
- Validation: Closure requires evidence that the mandatory startup contract is stated explicitly in the prod profile.
- Guardrail: A retry budget set too low can turn a recoverable throttle into a startup failure, so the deployment must supply values aligned to the regional recovery budget rather than arbitrary defaults.

<span style="font-size: 14px;">**Standards reference:** springboot-keyvault v2.2.0 — `grounding/dependencies/springboot-keyvault.md`</span>

---

<!-- finding:F-024 -->
#### P0-006: Hibernate applies schema changes at startup in every profile

**Priority: P0 - Critical risk**

**Priority policy:** AA-REMEDIATION-PRIORITY version 1.0.0

**Severity:** high

**Resiliency Related:** Yes

**Finding status:** Verified finding

**Issue:** The Hibernate schema mode is set to update in the default profile and is not overridden in the prod profile. Every startup in every region therefore performs schema introspection and applies DDL against whichever database the injected connection string resolves to. No versioned migration dependency is declared, so there is no migration contract and no controlled migration gate.

**What does this solve:** The write-capable schema operation is removed from the startup path and replaced with a versioned, reviewable migration contract. A standby-region pod can start against a read-only or mid-promotion endpoint, and schema state stops drifting silently between regions.

**Resiliency Impact:** Startup is coupled to a write-capable schema operation on the authoritative database. When a pod starts against a read-only geo-secondary, against a database mid-promotion, or while another region's pods perform the same introspection, startup fails or contends in ways the application neither bounds nor reports. In an active-standby model the standby region's pods perform this DDL attempt on every deployment, so the failure surfaces at exactly the moment the standby is needed. Removing it directly enables the approved active-standby promotion path.

**Recommended Fix:** Set Hibernate to schema validation only and express the schema as versioned SQL migration scripts held in the repository. Apply those scripts through an approved migration runner outside the ordinary application startup path, or behind an explicit, bounded, role-aware startup gate. Startup then fails fast with a clear message when the deployed schema does not match the entity model instead of mutating a database it may not own.

**File:** `source/inventory-service/src/main/resources/application.yml`:10-12

**Repository evidence:**

- Repository path: `source/inventory-service/src/main/resources/application.yml`
- Symbol: `spring.jpa.hibernate.ddl-auto`
- Source fingerprint: `sha256:26b82c5e056d...`
- Assessment snapshot: Workspace snapshot `inventory-service-workspace-2026-09-18`
- Original assessed lines (advisory): 10-12

**Original source requiring update:**

```yaml
  jpa:
    hibernate:
      ddl-auto: update
```

**Fix:**

**Proposed change: Remove runtime DDL from the startup path** — `source/inventory-service/src/main/resources/application.yml`

Illustrative proposal only.

```yaml
  jpa:
    hibernate:
      ddl-auto: ${JPA_DDL_AUTO:validate}
    open-in-view: false
```

Startup validates the deployed schema instead of mutating it, so a pod starting against a read-only geo-secondary or a database mid-promotion no longer attempts DDL. The value stays overridable so a local development profile can select a different mode without a code change. Open-in-view is disabled so a database session is not held for the duration of view rendering, which keeps the connection budget described in P1-004 meaningful.

**Proposed change: Baseline versioned migration script** — `source/inventory-service/src/main/resources/db/migration/V1__baseline_inventory_items.sql`

Illustrative proposal only.

```sql
CREATE TABLE inventory_items (
    id                 BIGINT IDENTITY(1,1) NOT NULL,
    productId          VARCHAR(255)         NULL,
    availableQuantity  INT                  NOT NULL,
    reservedQuantity   INT                  NOT NULL,
    updatedAt          DATETIME2            NULL,
    version            BIGINT               NOT NULL,
    CONSTRAINT PK_inventory_items PRIMARY KEY (id),
    CONSTRAINT UQ_inventory_items_productId UNIQUE (productId)
);
```

The schema currently has no repository-owned definition at all; it is produced implicitly by the schema update setting. The baseline reproduces the current inventory item mapping exactly: the identity primary key, the unique constraint on the product identifier declared on the table annotation, the two quantity columns, the updated instant, and the optimistic locking version column. No column is added, removed, widened, or renamed, so switching to validation does not change the schema contract.

**Proposed change: Versioned migration runner dependency** — `source/inventory-service/pom.xml`

**Illustrative code status:** Targeted implementation discovery required

**Why code was not generated:** The approved libraries governance file declares approved libraries for resiliency, observability, and testing only. It declares no approved schema-migration library, and no repository evidence establishes an organizational choice between Flyway, Liquibase, and an externally executed migration process. Selecting one would be an unapproved product decision.

**Unresolved inputs:**
- Approved schema-migration library or externally governed migration process
- Whether migrations execute inside the application startup path or as a separate release step

**Intended behavior:** A versioned migration runner must apply the scripts held under the repository migration folder and record the applied version, either outside the ordinary application startup path or behind an explicit, bounded, role-aware startup gate.

**Validation requirements:** Validation requires repository evidence that no profile selects a schema-mutating mode, that startup performs no DDL statement against the configured database, that startup fails fast with a clear message when the deployed schema does not match the entity model, and that the baseline schema exists as a versioned repository-owned migration script.

**Dependencies:** None.

**Notes:**

- Implementation: No entity, table, column, or constraint definition changes, and the database permissions required at runtime reduce from DDL to DML, which is a tightening rather than a loosening.
- Validation: Closure requires evidence that the application starts successfully against a schema created only by the migration script.
- Guardrail: Switching to validation will fail startup in any environment whose schema was created implicitly and has since drifted, so a pre-cutover schema comparison is required in each environment before the change is deployed.

<span style="font-size: 14px;">**Standards reference:** springboot-aks-active-active-master v4.0.0 — `grounding/master/springboot-aks-active-active-master.md`</span>

---

<h3 style="color:#0F6CBD;">
Regional Failure Observability
</h3>

<!-- finding:F-026 -->
#### P0-007: Telemetry carries no regional identity

**Priority: P0 - Critical risk**

**Priority policy:** AA-REMEDIATION-PRIORITY version 1.0.0

**Severity:** medium

**Resiliency Related:** Yes

**Finding status:** Verified finding

**Issue:** No common metric tag configuration, meter filter, or tag registration exists, so every metric scraped from the Prometheus endpoint carries no region, cluster, or role dimension. The logging configuration is a single console appender using the JSON encoder with no diagnostic context provider, custom field, or region field, and no production class populates the diagnostic context. Metrics and logs emitted from the two regions are therefore byte-for-byte indistinguishable once aggregated.

**What does this solve:** Every metric and every log record gains a deployment-supplied region dimension and role dimension, so per-region behaviour can be separated in aggregate views. Regional failure attribution and split-brain detection become possible from emitted telemetry alone.

**Resiliency Impact:** During a regional incident an operator cannot determine which region produced an error, which region is serving traffic, or whether the intended single-active Kafka processing is actually single. This removes the primary evidence needed to confirm or refute the concurrent dual-region consumption condition described in P0-002. Without a region dimension, regional failure tests cannot be executed or interpreted, so the approved active-standby promotion path cannot be exercised with confidence.

**Recommended Fix:** Bind a region identifier and a deployment role identifier from environment-supplied properties, apply them as common metric tags, and emit them as static structured-logging fields sourced from the same properties. Supply both values entirely through deployment-time placeholders so no region name and no regional endpoint appears anywhere in the repository. Default an unset value to an explicit unknown marker so a missing region is visible in telemetry rather than silently absent.

**File:** `source/inventory-service/src/main/resources/application.yml`:29-37

**Repository evidence:**

- Repository path: `source/inventory-service/src/main/resources/application.yml`
- Symbol: `absence of management.metrics.tags`
- Source fingerprint: `sha256:653a483edc8b...`
- Assessment snapshot: Workspace snapshot `inventory-service-workspace-2026-09-18`
- Original assessed lines (advisory): 29-37

**Original source requiring update:**

```yaml
management:
  endpoints:
    web:
      exposure:
        include: health,info,prometheus
  endpoint:
    health:
      probes:
        enabled: true
```

**File:** `source/inventory-service/src/main/resources/logback-spring.xml`:1-1

**Repository evidence:**

- Repository path: `source/inventory-service/src/main/resources/logback-spring.xml`
- Symbol: `LogstashEncoder console appender`
- Source fingerprint: `sha256:fa4169b08e5c...`
- Assessment snapshot: Workspace snapshot `inventory-service-workspace-2026-09-18`
- Original assessed lines (advisory): 1-1

**Original source requiring update:**

```xml
<configuration><appender name="CONSOLE" class="ch.qos.logback.core.ConsoleAppender"><encoder class="net.logstash.logback.encoder.LogstashEncoder"/></appender><root level="INFO"><appender-ref ref="CONSOLE"/></root></configuration>
```

**Fix:**

**Proposed change: Deployment identity properties** — `source/inventory-service/src/main/resources/application.yml`

Illustrative proposal only.

```yaml
app:
  deployment:
    region: ${APP_DEPLOYMENT_REGION:unknown}
    role: ${APP_DEPLOYMENT_ROLE:unknown}
management:
  metrics:
    tags:
      region: ${app.deployment.region}
      role: ${app.deployment.role}
```

Both values are supplied entirely by deployment-time environment variables. No region name and no regional endpoint appears in the repository. The explicit unknown default makes an unset value visible in telemetry rather than silently absent.

**Proposed change: Deployment identity binding** — `source/inventory-service/src/main/java/com/ecommerce/inventory/config/DeploymentIdentityProperties.java`

Illustrative proposal only.

```java
package com.ecommerce.inventory.config;

import org.springframework.boot.context.properties.ConfigurationProperties;
import org.springframework.boot.context.properties.EnableConfigurationProperties;
import org.springframework.context.annotation.Configuration;

@Configuration
@EnableConfigurationProperties(DeploymentIdentityProperties.class)
@ConfigurationProperties(prefix = "app.deployment")
public class DeploymentIdentityProperties {

    private String region = "unknown";
    private String role = "unknown";

    public String getRegion() {
        return region;
    }

    public void setRegion(String region) {
        this.region = region;
    }

    public String getRole() {
        return role;
    }

    public void setRole(String role) {
        this.role = role;
    }
}
```

A typed binding makes the region and role available to the logback configuration and to any component that needs to tag a record. The repository has no existing configuration-properties class, so this establishes the pattern the later changes reuse.

**Proposed change: Region fields on structured log records** — `source/inventory-service/src/main/resources/logback-spring.xml`

Illustrative proposal only.

```xml
<configuration>
    <springProperty scope="context" name="deploymentRegion" source="app.deployment.region" defaultValue="unknown"/>
    <springProperty scope="context" name="deploymentRole" source="app.deployment.role" defaultValue="unknown"/>
    <springProperty scope="context" name="applicationName" source="spring.application.name" defaultValue="inventory-service"/>
    <appender name="CONSOLE" class="ch.qos.logback.core.ConsoleAppender">
        <encoder class="net.logstash.logback.encoder.LogstashEncoder">
            <customFields>{"application":"${applicationName}","region":"${deploymentRegion}","role":"${deploymentRole}"}</customFields>
        </encoder>
    </appender>
    <root level="INFO">
        <appender-ref ref="CONSOLE"/>
    </root>
</configuration>
```

The spring property elements read the same externalized values the metrics tags use, so metrics and logs carry the identical region and role dimension. The encoder, appender, and root level are otherwise unchanged, so existing log parsers continue to work.

**Validation requirements:** Validation requires repository evidence that every scraped meter and every emitted log record carries a region dimension and a role dimension sourced entirely from deployment-supplied properties, with an explicit unknown default when the value is unset.

**Dependencies:** None.

**Notes:**

- Implementation: Two low-cardinality dimensions are added and no existing meter name, log field, or appender configuration is removed.
- Validation: Closure requires evidence that no region name and no regional endpoint is hardcoded anywhere in the repository.
- Guardrail: The role dimension reports the configured regional role and must never be used to assign or change it.

<span style="font-size: 14px;">**Standards reference:** springboot-aks-active-active-master v4.0.0 — `grounding/master/springboot-aks-active-active-master.md`</span>

---

<!-- finding:F-027 -->
#### P0-008: Critical failures and business throughput produce no actionable signal

**Priority: P0 - Critical risk**

**Priority policy:** AA-REMEDIATION-PRIORITY version 1.0.0

**Severity:** critical

**Resiliency Related:** Yes

**Finding status:** Verified finding

**Issue:** No production class declares a logger or emits a log statement, and the logging configuration exposes a single console appender at information level, so the only records produced are framework logs. No custom counter, timer, or gauge is registered for publication failure, consumption outcome, reservation volume, cache failure versus cache miss, last successful processing time, or backlog age. The event producer discards its send result entirely and emits nothing on failure.

**What does this solve:** Every failure path and every business outcome produces an application-emitted signal, so failures become detectable and recovery becomes initiable. A stopped consumer becomes distinguishable from an idle one, which bounds the mean time to detect.

**Resiliency Impact:** Every failure mode identified in this assessment is silent. A dropped publication under P1-001, a rolled-back transaction after a published event under P2-001, a skipped record under P1-002, a quarantine-less poison record under P1-003, and a cache outage under P1-011 all occur with no application-emitted evidence. Operators cannot distinguish a healthy idle service from one whose Kafka processing has stopped entirely, because process health reports as up in both cases, so mean time to detect is unbounded.

**Recommended Fix:** Register a single telemetry component that owns counters and timers for inventory publication outcome, order consumption outcome, cache outcome distinguishing failure from miss, and a last-success timestamp gauge for each processing path. Emit exactly one structured record on every failure path at warning or error level carrying the operation, the outcome, the correlation reference, and the exception class. Exclude payload content, credentials, and connection strings from every record, meter name, and meter tag, and keep the application log level externally configurable so volume can be reduced during an incident.

**File:** `source/inventory-service/src/main/java/com/ecommerce/inventory/kafka/producer/InventoryEventProducer.java`:14-16

**Repository evidence:**

- Repository path: `source/inventory-service/src/main/java/com/ecommerce/inventory/kafka/producer/InventoryEventProducer.java`
- Symbol: `InventoryEventProducer.publish`
- Source fingerprint: `sha256:c77eedf9776f...`
- Assessment snapshot: Workspace snapshot `inventory-service-workspace-2026-09-18`
- Original assessed lines (advisory): 14-16

**Original source requiring update:**

```java
    public void publish(String type, InventoryResponse inventory, String referenceId) {
        kafkaTemplate.send("inventory-events", inventory.productId(), Map.of("type", type, "occurredAt", Instant.now().toString(), "referenceId", referenceId == null ? "" : referenceId, "inventory", inventory));
    }
```

**File:** `source/inventory-service/src/main/resources/logback-spring.xml`:1-1

**Repository evidence:**

- Repository path: `source/inventory-service/src/main/resources/logback-spring.xml`
- Symbol: `root logger and appender configuration`
- Source fingerprint: `sha256:fa4169b08e5c...`
- Assessment snapshot: Workspace snapshot `inventory-service-workspace-2026-09-18`
- Original assessed lines (advisory): 1-1

**Original source requiring update:**

```xml
<configuration><appender name="CONSOLE" class="ch.qos.logback.core.ConsoleAppender"><encoder class="net.logstash.logback.encoder.LogstashEncoder"/></appender><root level="INFO"><appender-ref ref="CONSOLE"/></root></configuration>
```

**Fix:**

**Proposed change: Business and failure telemetry component** — `source/inventory-service/src/main/java/com/ecommerce/inventory/observability/InventoryTelemetry.java`

Illustrative proposal only.

```java
package com.ecommerce.inventory.observability;

import io.micrometer.core.instrument.MeterRegistry;
import io.micrometer.core.instrument.Gauge;
import org.springframework.stereotype.Component;

import java.time.Instant;
import java.util.concurrent.atomic.AtomicReference;

@Component
public class InventoryTelemetry {

    public static final String OUTCOME_SUCCESS = "success";
    public static final String OUTCOME_FAILURE = "failure";
    public static final String OUTCOME_DUPLICATE = "duplicate";
    public static final String OUTCOME_QUARANTINED = "quarantined";
    public static final String CACHE_MISS = "miss";
    public static final String CACHE_FAILURE = "failure";

    private final MeterRegistry meterRegistry;
    private final AtomicReference<Instant> lastConsumeSuccess = new AtomicReference<>(Instant.EPOCH);

    public InventoryTelemetry(MeterRegistry meterRegistry) {
        this.meterRegistry = meterRegistry;
        Gauge.builder("inventory.consume.last_success.age.seconds", lastConsumeSuccess,
                        reference -> secondsSince(reference.get()))
                .description("Seconds since the last successfully applied order event")
                .register(meterRegistry);
    }

    public void recordPublication(String eventType, String outcome) {
        meterRegistry.counter("inventory.publish.outcome", "eventType", eventType, "outcome", outcome).increment();
    }

    public void recordConsumption(String eventType, String outcome) {
        meterRegistry.counter("inventory.consume.outcome", "eventType", eventType, "outcome", outcome).increment();
        if (OUTCOME_SUCCESS.equals(outcome)) {
            lastConsumeSuccess.set(Instant.now());
        }
    }

    public void recordCacheOutcome(String cacheName, String outcome) {
        meterRegistry.counter("inventory.cache.outcome", "cache", cacheName, "outcome", outcome).increment();
    }

    private static double secondsSince(Instant instant) {
        return Instant.EPOCH.equals(instant)
                ? -1d
                : (System.currentTimeMillis() - instant.toEpochMilli()) / 1000d;
    }
}
```

One component owns every business and failure meter so the names and dimensions stay consistent. The region and role tags come from the common metric tags introduced by P0-007 and are not repeated on each meter. The last-success gauge is registered at construction so it is present even before any record is processed, and it reports a negative sentinel until the first success, which lets an operator tell a never-started consumer from a stalled one. No meter name or tag carries payload content.

**Proposed change: Application logging level contract** — `source/inventory-service/src/main/resources/logback-spring.xml`

Illustrative proposal only.

```xml
<logger name="com.ecommerce.inventory" level="${APP_LOG_LEVEL:-INFO}" additivity="false">
    <appender-ref ref="CONSOLE"/>
</logger>
```

An explicit application logger makes the failure and outcome records emitted by the other changes independently tunable from framework logging, so log volume can be reduced during an incident without losing framework diagnostics. The element is added inside the logging configuration produced by P0-007.

**Validation requirements:** Validation requires repository evidence that publication outcome, consumption outcome, cache miss versus cache failure, and seconds since the last successful order-event application are each observable, that every failure path emits exactly one structured record carrying the operation, outcome, correlation reference, and exception class, and that no record, meter name, or meter tag carries payload content, a credential, or a connection string.

**Dependencies:** Depends on P0-007.

**Notes:**

- Implementation: New meters are additive and the log output remains JSON, so no existing meter name, tag, or log parser is affected.
- Validation: Closure requires evidence that the last-success gauge is present and reports a distinguishable value even when zero records have been processed.
- Guardrail: Failure logging must remain one record per operation outcome with no payload content so a high-volume failure cannot amplify the incident through log volume.

<span style="font-size: 14px;">**Standards reference:** springboot-aks-active-active-master v4.0.0 — `grounding/master/springboot-aks-active-active-master.md`</span>

---

<h3 style="color:#0F6CBD;">
Failure and Failover Verification
</h3>

<!-- finding:F-028 -->
#### P0-009: Failure and failover behaviour is untested

**Priority: P0 - Critical risk**

**Priority policy:** AA-REMEDIATION-PRIORITY version 1.0.0

**Severity:** critical

**Resiliency Related:** Yes

**Finding status:** Verified finding

**Issue:** The test suite contains one unit test covering the happy-path reserve flow and one Spring Boot integration test whose only assertion is that the application context loads. No test exercises duplicate delivery, replay from an earlier offset, consumer rebalance, broker unavailability, database failover or connection loss, unknown commit outcome, optimistic-locking conflict, cache unavailability, secret-store denial or throttling, probe transitions, or graceful shutdown. The create, get, list, update, delete, and release operations, the order event consumer, the inventory event producer, and the global exception handler have no test coverage at all.

**What does this solve:** The failure behaviour the approved target deployment depends on becomes demonstrable rather than assumed, so remediation of the other findings in this assessment can be proven. The same coverage protects that behaviour from silent regression when managed dependency versions change.

**Resiliency Impact:** None of the failure behaviour the approved active-standby deployment depends on is verified, so neither the current defects nor their remediation can be demonstrated. The managed dependency versions also govern resilience-relevant transitive behaviour, and a version bump can silently change timeout, retry, offset, or health semantics with only a context-load assertion standing between the change and production. Promotion, stale-active fencing, offset restoration, duplicate replay, and failback behaviour all remain unproven.

**Recommended Fix:** Build a fault-injection and failover regression suite on the existing container-based and embedded-broker test model covering duplicate delivery, replay from an earlier offset, rebalance, broker unavailability, database connection loss, optimistic-locking conflict, cache unavailability, secret-store denial, probe transitions, graceful shutdown, and regional activation and deactivation. Add a configuration regression assertion over the resilience-relevant effective settings so a managed version bump cannot silently change timeout, retry, offset, or health semantics. Keep the suite executable without a live cloud dependency so it runs in the ordinary build.

**File:** `source/inventory-service/src/test/java/com/ecommerce/inventory/InventoryIntegrationTest.java`:12-22

**Repository evidence:**

- Repository path: `source/inventory-service/src/test/java/com/ecommerce/inventory/InventoryIntegrationTest.java`
- Symbol: `InventoryIntegrationTest.contextLoads`
- Source fingerprint: `sha256:710fb9f0da4e...`
- Assessment snapshot: Workspace snapshot `inventory-service-workspace-2026-09-18`
- Original assessed lines (advisory): 12-22

**Original source requiring update:**

```java
@SpringBootTest(properties = "spring.kafka.bootstrap-servers=${spring.embedded.kafka.brokers}")
@EmbeddedKafka(partitions = 1, topics = {"order-events", "inventory-events"})
@Testcontainers(disabledWithoutDocker = true)
class InventoryIntegrationTest {
    @Container static final MSSQLServerContainer<?> SQL = new MSSQLServerContainer<>("mcr.microsoft.com/mssql/server:2022-latest").acceptLicense();
    @DynamicPropertySource static void properties(DynamicPropertyRegistry registry) {
        registry.add("spring.datasource.url", SQL::getJdbcUrl); registry.add("spring.datasource.username", SQL::getUsername); registry.add("spring.datasource.password", SQL::getPassword);
    }
    @Test void contextLoads() {
    }
}
```

**File:** `source/inventory-service/src/test/java/com/ecommerce/inventory/service/InventoryServiceImplTest.java`:21-31

**Repository evidence:**

- Repository path: `source/inventory-service/src/test/java/com/ecommerce/inventory/service/InventoryServiceImplTest.java`
- Symbol: `InventoryServiceImplTest.reservesAvailableStockAndPublishesEvent`
- Source fingerprint: `sha256:f445abad3d58...`
- Assessment snapshot: Workspace snapshot `inventory-service-workspace-2026-09-18`
- Original assessed lines (advisory): 21-31

**Original source requiring update:**

```java
@ExtendWith(MockitoExtension.class)
class InventoryServiceImplTest {
    @Mock InventoryRepository repository; @Mock InventoryMapper mapper; @Mock InventoryEventProducer producer; @InjectMocks InventoryServiceImpl service;
    @Test void reservesAvailableStockAndPublishesEvent() {
        InventoryItem item = InventoryItem.builder().id(1L).productId("p1").availableQuantity(10).build();
        InventoryResponse response = new InventoryResponse(1L, "p1", 7, 3, Instant.now());
        when(repository.findByProductId("p1")).thenReturn(Optional.of(item)); when(repository.save(any())).thenReturn(item); when(mapper.toResponse(item)).thenReturn(response);
        assertThat(service.reserve("p1", 3, "o1")).isEqualTo(response);
        assertThat(item.getAvailableQuantity()).isEqualTo(7); verify(producer).publish("INVENTORY_RESERVED", response, "o1");
    }
}
```

**Fix:**

Illustrative proposal only.

The proposed coverage is a fault-injection and failover regression suite built on the container-based database, embedded broker, and Spring Boot test model the repository already uses, extended with a container-backed cache and property-source substitution for the secret store. It exercises duplicate delivery and replay from an earlier offset producing exactly one stock movement, consumer rebalance and broker unavailability producing an observed publication failure rather than a silent drop, poison-record quarantine with the offset advancing only afterward, database connection loss producing a bounded failure and a readiness transition that recovers without a restart, optimistic-locking conflict absorbed by reload and reapply, cache unavailability still serving a successful read from the authoritative store, readiness reporting out of service before the servlet container stops during shutdown, and externalized regional activation suppressing consumption while readiness stays up. A further assertion pins the resilience-relevant effective configuration so a managed version bump that changes a timeout, retry, offset, or health default fails the build instead of reaching production. Together this coverage guards every remediation in this plan against silent regression and makes the approved active-standby promotion and failback behaviour demonstrable without a live cloud dependency.

**Test detail suppressed:** The configured report testing-output preference suppresses test code, test names, validation commands, and acceptance criteria. Every proposed test and validation obligation remains binding in the authoritative remediation plan.

**Validation requirements:** Validation requires repository evidence that each identified failure, duplicate, replay, promotion, probe-transition, and shutdown behaviour is exercised and asserted, and that the resilience-relevant effective configuration is pinned against managed version drift.

**Dependencies:** Depends on P0-003, P0-006, P0-005, P0-004, P0-007, P0-008, P0-002, P0-001, P1-004, P1-007, P1-008, P1-010, P1-011, P1-017, P1-014, P1-001, P1-002, and P1-015.

**Notes:**

- Implementation: The change is test-only, so no production source, configuration, or external contract is affected.
- Validation: Closure requires evidence that the suite executes in the ordinary build without a live cloud dependency.
- Guardrail: Container-based fault injection lengthens the build and can be flaky, so the fault-injection group must remain separately executable and must retain the existing guard that skips it when no container runtime is available.

<span style="font-size: 14px;">**Standards reference:** springboot-aks-active-active-master v4.0.0 — `grounding/master/springboot-aks-active-active-master.md`</span>

---

### Priority P1

<h3 style="color:#0F6CBD;">
Event Publication and Consumption Durability
</h3>

<!-- finding:F-001 -->
#### P1-001: Kafka publication is fire-and-forget with no durability configuration

**Priority: P1 - High risk**

**Priority policy:** AA-REMEDIATION-PRIORITY version 1.0.0

**Severity:** critical

**Resiliency Related:** Yes

**Finding status:** Verified finding

**Issue:** The producer publishes every inventory event by calling send and discarding the returned future. No callback, completion handler, producer listener, or blocking wait inspects the delivery outcome. The producer configuration declares only key and value serializers, so acknowledgement mode, retries, idempotence, delivery timeout, and maximum in-flight requests per connection all remain at client defaults. None of those settings is deployment tunable through repository-owned configuration.

**What does this solve:** A broker outage, leader election, partition unavailability, or serialization failure stops being invisible to the application. An operator gains a signal that identifies the lost event and can decide on replay. Durability settings become explicit and adjustable per environment rather than inherited from client defaults.

**Resiliency Impact:** Every inventory state change publishes an event whose delivery outcome is never observed. A failed produce silently drops the event while the Azure SQL write is reported successful to the caller. Downstream consumers of the inventory event stream then hold state that permanently disagrees with authoritative inventory. No signal exists that would let an operator detect or replay the loss, which removes the basis for any targeted recovery action during an active-standby failover window.

**Recommended Fix:** Declare acknowledgement mode, idempotence, retries, delivery timeout, and maximum in-flight requests per connection as externalized properties. Observe the send result through a completion handler so success and failure each increment the region-tagged publication counter. On failure, emit one structured log record naming the topic, the record key, and the exception class, carrying no payload content. Broker-side minimum in-sync replicas, topic replication factor, and cluster linking state remain outside the change boundary.

**File:** `source/inventory-service/src/main/java/com/ecommerce/inventory/kafka/producer/InventoryEventProducer.java`:14-16

**Repository evidence:**

- Repository path: `source/inventory-service/src/main/java/com/ecommerce/inventory/kafka/producer/InventoryEventProducer.java`
- Symbol: `InventoryEventProducer.publish`
- Source fingerprint: `sha256:c77eedf9776f...`
- Assessment snapshot: Workspace snapshot `inventory-service-workspace-2026-09-18`
- Original assessed lines (advisory): 14-16

**Original source requiring update:**

```java
public void publish(String type, InventoryResponse inventory, String referenceId) {
    kafkaTemplate.send("inventory-events", inventory.productId(), Map.of("type", type, "occurredAt", Instant.now().toString(), "referenceId", referenceId == null ? "" : referenceId, "inventory", inventory));
}
```

**File:** `source/inventory-service/src/main/resources/application.yml`:26-28

**Repository evidence:**

- Repository path: `source/inventory-service/src/main/resources/application.yml`
- Symbol: `spring.kafka.producer`
- Source fingerprint: `sha256:825e9b9cd362...`
- Assessment snapshot: Workspace snapshot `inventory-service-workspace-2026-09-18`
- Original assessed lines (advisory): 26-28

**Original source requiring update:**

```yaml
producer:
  key-serializer: org.apache.kafka.common.serialization.StringSerializer
  value-serializer: org.springframework.kafka.support.serializer.JsonSerializer
```

**Fix:**

**Proposed change: Observed publication outcome** — `source/inventory-service/src/main/java/com/ecommerce/inventory/kafka/producer/InventoryEventProducer.java`

Illustrative proposal only.

```java
public void publish(String type, InventoryResponse inventory, String referenceId) {
    String key = inventory.productId();
    Map<String, Object> payload = Map.of(
            "type", type,
            "occurredAt", Instant.now().toString(),
            "referenceId", referenceId == null ? "" : referenceId,
            "inventory", inventory);

    kafkaTemplate.send(TOPIC, key, payload).whenComplete((result, failure) -> {
        if (failure == null) {
            telemetry.recordPublication(type, InventoryTelemetry.OUTCOME_SUCCESS);
        } else {
            telemetry.recordPublication(type, InventoryTelemetry.OUTCOME_FAILURE);
            log.error("inventory event publication failed topic={} key={} eventType={} exception={}",
                    TOPIC, key, type, failure.getClass().getName(), failure);
        }
    });
}
```

The returned future is observed instead of discarded. Success and failure each produce exactly one counter increment, and a failure produces one structured log record naming the topic, the record key, and the exception class. The payload is not logged. The topic name, the record key, and the payload shape are unchanged by this change, and the envelope contract change belongs to P2-002. The literal topic name is lifted to a constant so P1-002, P1-003, and P2-001 can reference it.

**Proposed change: Producer durability settings** — `source/inventory-service/src/main/resources/application.yml`

Illustrative proposal only.

```yaml
producer:
  key-serializer: org.apache.kafka.common.serialization.StringSerializer
  value-serializer: org.springframework.kafka.support.serializer.JsonSerializer
  acks: ${KAFKA_PRODUCER_ACKS}
  retries: ${KAFKA_PRODUCER_RETRIES}
  properties:
    enable.idempotence: ${KAFKA_PRODUCER_ENABLE_IDEMPOTENCE}
    max.in.flight.requests.per.connection: ${KAFKA_PRODUCER_MAX_IN_FLIGHT}
```

The existing serializers are preserved. Durability settings become explicit and deployment tunable rather than implicit client defaults. No value is hardcoded, because the safe setting for acknowledgement mode depends on the broker-side minimum in-sync replicas and replication factor, which is an unresolved external input outside the remediation boundary. The timeout properties for this producer are declared by P1-004.

**Validation requirements:** Validation requires repository evidence that every send outcome is observed exactly once, that a failed publication emits a structured failure record naming the topic, the record key, and the exception class, and that no log record or metric tag carries payload content.

**Dependencies:** Depends on P0-008, P1-004, P1-005, and P1-006.

**Notes:**

- Implementation: The topic name, record key, and payload shape are unchanged, so no downstream consumer contract is affected.
- Validation: Closure requires evidence that a failed publication is observable and does not block the calling thread beyond the configured client block deadline.
- Guardrail: Acknowledgement and idempotence values must remain externalized because the safe setting depends on broker replication configuration owned outside this repository.

<span style="font-size: 14px;">**Standards reference:** springboot-aks-active-active-master v4.0.0 — `grounding/master/springboot-aks-active-active-master.md`</span>

---

<!-- finding:F-005 -->
#### P1-002: Consumer offsets advance past records that fail permanently

**Priority: P1 - High risk**

**Priority policy:** AA-REMEDIATION-PRIORITY version 1.0.0

**Severity:** critical

**Resiliency Related:** Yes

**Finding status:** Verified finding

**Issue:** The Kafka consumer configuration declares only auto-offset-reset, serializers, and trusted packages. No acknowledgement mode, manual acknowledgment, listener container factory, or transactional identity is configured, so offset commit is governed entirely by framework container defaults. No error handler or recoverer is declared alongside it. A record whose processing exhausts the default attempt budget is therefore skipped and its offset is committed.

**What does this solve:** An order event that cannot be applied is retried within a bounded, externally configured budget and then quarantined with a durable copy instead of being abandoned. Offset advancement becomes a consequence of durable business completion or of an explicit quarantine decision. An operator retains both a recoverable position and an inspectable artifact for every record that failed.

**Resiliency Impact:** Business work is discarded without a durable record. An order creation event that cannot be applied, for example because of a transient Azure SQL failure during a failover window, is retried inside the container and then abandoned, after which the offset advances. The reservation is never made and no durable terminal state records the loss. The event cannot be located for replay because the consumer group has already moved past it.

**Recommended Fix:** Declare a named listener container factory with manual immediate acknowledgment, an externally configured attempt budget with exponential backoff, and a dead-letter publishing recoverer that routes exhausted and non-retryable records to an externally named quarantine destination. Externalize the acknowledgement mode, attempt count, backoff parameters, and destination name so no retry is immediate and no topic name is fixed in the repository. Dead-letter topic provisioning, access policy, and retention remain outside the change boundary.

**Remediated with:** P1-003

**File:** `source/inventory-service/src/main/resources/application.yml`:18-28

**Repository evidence:**

- Repository path: `source/inventory-service/src/main/resources/application.yml`
- Symbol: `spring.kafka`
- Source fingerprint: `sha256:d249f7885663...`
- Assessment snapshot: Workspace snapshot `inventory-service-workspace-2026-09-18`
- Original assessed lines (advisory): 18-28

**Original source requiring update:**

```yaml
kafka:
  bootstrap-servers: ${KAFKA_BOOTSTRAP_SERVERS:localhost:9092}
  consumer:
    auto-offset-reset: earliest
    key-deserializer: org.apache.kafka.common.serialization.StringDeserializer
    value-deserializer: org.springframework.kafka.support.serializer.JsonDeserializer
    properties:
      spring.json.trusted.packages: "*"
  producer:
    key-serializer: org.apache.kafka.common.serialization.StringSerializer
    value-serializer: org.springframework.kafka.support.serializer.JsonSerializer
```

**Fix:**

**Proposed change: Listener container factory with bounded error handling** — `source/inventory-service/src/main/java/com/ecommerce/inventory/kafka/KafkaConsumerConfig.java`

Illustrative proposal only.

```java
package com.ecommerce.inventory.kafka;

import com.ecommerce.inventory.kafka.consumer.NonRetryablePayloadException;
import com.ecommerce.inventory.observability.InventoryTelemetry;
import lombok.extern.slf4j.Slf4j;
import org.apache.kafka.clients.consumer.ConsumerRecord;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.kafka.config.ConcurrentKafkaListenerContainerFactory;
import org.springframework.kafka.core.ConsumerFactory;
import org.springframework.kafka.core.KafkaTemplate;
import org.springframework.kafka.listener.ContainerProperties;
import org.springframework.kafka.listener.DeadLetterPublishingRecoverer;
import org.springframework.kafka.listener.DefaultErrorHandler;
import org.springframework.util.backoff.ExponentialBackOff;
import org.apache.kafka.common.TopicPartition;

import java.util.Map;

@Slf4j
@Configuration
public class KafkaConsumerConfig {

    @Bean
    public ConcurrentKafkaListenerContainerFactory<String, Map<String, Object>> orderEventListenerContainerFactory(
            ConsumerFactory<String, Map<String, Object>> consumerFactory,
            DefaultErrorHandler orderEventErrorHandler) {

        ConcurrentKafkaListenerContainerFactory<String, Map<String, Object>> factory =
                new ConcurrentKafkaListenerContainerFactory<>();
        factory.setConsumerFactory(consumerFactory);
        factory.setCommonErrorHandler(orderEventErrorHandler);
        factory.getContainerProperties().setAckMode(ContainerProperties.AckMode.MANUAL_IMMEDIATE);
        return factory;
    }

    @Bean
    public DefaultErrorHandler orderEventErrorHandler(
            KafkaTemplate<String, Object> kafkaTemplate,
            InventoryTelemetry telemetry,
            @Value("${app.kafka.consumer.dead-letter-topic}") String deadLetterTopic,
            @Value("${app.kafka.consumer.max-attempts}") int maxAttempts,
            @Value("${app.kafka.consumer.backoff-initial-interval}") long initialInterval,
            @Value("${app.kafka.consumer.backoff-multiplier}") double multiplier,
            @Value("${app.kafka.consumer.backoff-max-interval}") long maxInterval) {

        DeadLetterPublishingRecoverer recoverer = new DeadLetterPublishingRecoverer(kafkaTemplate,
                (record, exception) -> new TopicPartition(deadLetterTopic, record.partition()));

        ExponentialBackOff backOff = new ExponentialBackOff(initialInterval, multiplier);
        backOff.setMaxInterval(maxInterval);
        backOff.setMaxAttempts(maxAttempts);

        DefaultErrorHandler errorHandler = new DefaultErrorHandler((record, exception) -> {
            recoverer.accept((ConsumerRecord<?, ?>) record, exception);
            telemetry.recordConsumption("order-events", InventoryTelemetry.OUTCOME_QUARANTINED);
            log.error("order event quarantined topic={} partition={} offset={} exception={}",
                    record.topic(), record.partition(), record.offset(), exception.getClass().getName());
        }, backOff);

        errorHandler.addNotRetryableExceptions(NonRetryablePayloadException.class, IllegalArgumentException.class);
        return errorHandler;
    }
}
```

Manual immediate acknowledgment moves offset advancement under the listener's control, so the offset no longer advances as a side effect of an exhausted implicit attempt budget. The attempt count and the exponential backoff are externalized, so no retry is immediate. Structurally invalid payloads and business validation failures are declared non-retryable so they are quarantined on the first attempt without consuming the budget. The recoverer publishes to an externally named dead-letter destination using the KafkaTemplate that is already a bean in this application, and each quarantine produces one counter increment and one log record with no payload content.

**Proposed change: Listener error-handling properties** — `source/inventory-service/src/main/resources/application.yml`

Illustrative proposal only.

```yaml
spring:
  kafka:
    listener:
      ack-mode: manual_immediate
app:
  kafka:
    consumer:
      enabled: ${KAFKA_CONSUMER_ENABLED:true}
      listener-id: order-events-listener
      dead-letter-topic: ${KAFKA_ORDER_EVENTS_DLT}
      max-attempts: ${KAFKA_CONSUMER_MAX_ATTEMPTS}
      backoff-initial-interval: ${KAFKA_CONSUMER_BACKOFF_INITIAL_MS}
      backoff-multiplier: ${KAFKA_CONSUMER_BACKOFF_MULTIPLIER}
      backoff-max-interval: ${KAFKA_CONSUMER_BACKOFF_MAX_MS}
```

The activation property from P0-002 and the error-handling properties from this change share the app.kafka.consumer prefix because they configure the same listener. The dead-letter destination name is supplied at deployment time so no topic name is fixed in the repository. Attempt count and backoff are externalized placeholders with no asserted values. The existing consumer serializers, auto-offset-reset, and trusted-packages settings are unchanged by this block.

**Validation requirements:** Validation requires repository evidence that the offset advances only after durable business completion or a successful quarantine publication, that no attempt is immediate, and that a failed quarantine publication holds the offset rather than losing the record.

**Dependencies:** Depends on P0-008, P0-001, P1-004, P1-005, and P1-006.

**Notes:**

- Implementation: Consumer group identity, topic name, and inbound payload shape are unchanged, and records that were previously skipped are now published to a quarantine destination owned by this service.
- Validation: Closure requires evidence that a record exhausting the retry budget reaches the configured quarantine destination before the offset advances.
- Guardrail: Every path through the listener must either acknowledge or raise a classified failure the error handler resolves, so manual acknowledgment cannot leave a partition stuck.

<span style="font-size: 14px;">**Standards reference:** springboot-aks-active-active-master v4.0.0 — `grounding/master/springboot-aks-active-active-master.md`</span>

---

<!-- finding:F-006 -->
#### P1-003: Poison records have no dead-letter routing and payload extraction is unguarded

**Priority: P1 - High risk**

**Priority policy:** AA-REMEDIATION-PRIORITY version 1.0.0

**Severity:** high

**Resiliency Related:** Yes

**Finding status:** Verified finding

**Issue:** No common error handler, error handler bean, dead-letter publishing recoverer, dead-letter topic, or retry topic is declared. Payload extraction reads untyped map values with String.valueOf and an unchecked numeric cast on quantity. There is no null check and no type guard on any extracted field. A malformed or partially populated order event therefore throws before any business validation occurs.

**What does this solve:** A structurally invalid order event is classified as non-retryable and quarantined on the first attempt, leaving a durable copy an operator can inspect and reprocess. Extraction failures become explicit and typed rather than surfacing as null pointer or class cast errors from inside the listener. A repeating malformed payload shape can no longer render a partition's traffic unprocessable without a diagnostic artifact.

**Resiliency Impact:** A single malformed order event repeatedly fails deserialization or extraction inside the listener. With no recoverer or quarantine destination the record is retried and then dropped by the container default, so the operator has no quarantined copy to inspect or reprocess. Because the same defect produces a null pointer or class cast failure for every occurrence of the malformed shape, a systematic producer change can render the entire partition's traffic unprocessable with no diagnostic artifact.

**Recommended Fix:** Extract payload fields through a guarded mapper that raises a classified non-retryable failure on a missing or wrongly typed field. Register that failure type as non-retryable with the listener error handler so a structurally invalid record is quarantined on the first attempt without consuming the retry budget. Keep failure messages free of payload values. Dead-letter destination provisioning, access policy, and retention remain outside the change boundary.

**Remediated with:** P1-002

**File:** `source/inventory-service/src/main/java/com/ecommerce/inventory/kafka/consumer/OrderEventConsumer.java`:14-18

**Repository evidence:**

- Repository path: `source/inventory-service/src/main/java/com/ecommerce/inventory/kafka/consumer/OrderEventConsumer.java`
- Symbol: `OrderEventConsumer.consume payload extraction`
- Source fingerprint: `sha256:0411994fedf4...`
- Assessment snapshot: Workspace snapshot `inventory-service-workspace-2026-09-18`
- Original assessed lines (advisory): 14-18

**Original source requiring update:**

```java
public void consume(Map<String, Object> event) {
    String type = String.valueOf(event.get("type"));
    String productId = String.valueOf(event.get("productId"));
    int quantity = ((Number) event.get("quantity")).intValue();
    String orderId = String.valueOf(event.get("orderId"));
```

**Fix:**

**Proposed change: Guarded payload extraction** — `source/inventory-service/src/main/java/com/ecommerce/inventory/kafka/consumer/OrderEventPayload.java`

Illustrative proposal only.

```java
package com.ecommerce.inventory.kafka.consumer;

import java.util.Map;

public record OrderEventPayload(String type, String productId, int quantity, String orderId) {

    public static OrderEventPayload from(Map<String, Object> event) {
        return new OrderEventPayload(
                requiredText(event, "type"),
                requiredText(event, "productId"),
                requiredQuantity(event),
                requiredText(event, "orderId"));
    }

    private static String requiredText(Map<String, Object> event, String field) {
        Object value = event.get(field);
        if (value == null || String.valueOf(value).isBlank()) {
            throw new NonRetryablePayloadException("Order event is missing required field " + field);
        }
        return String.valueOf(value);
    }

    private static int requiredQuantity(Map<String, Object> event) {
        Object value = event.get("quantity");
        if (!(value instanceof Number number)) {
            throw new NonRetryablePayloadException("Order event quantity is missing or is not numeric");
        }
        return number.intValue();
    }
}
```

Extraction produces a typed record with the same four fields the current code reads, in the same order, with the same names. A missing field or a non-numeric quantity now raises a classified non-retryable failure instead of a NullPointerException or a ClassCastException, so the error handler can quarantine the record immediately with a diagnostic artifact. The record type follows the existing DTO convention in this repository, which already uses Java records for InventoryResponse and StockAdjustmentRequest. The exception message contains no payload values.

**Proposed change: Non-retryable payload exception** — `source/inventory-service/src/main/java/com/ecommerce/inventory/kafka/consumer/NonRetryablePayloadException.java`

Illustrative proposal only.

```java
package com.ecommerce.inventory.kafka.consumer;

public class NonRetryablePayloadException extends RuntimeException {

    public NonRetryablePayloadException(String message) {
        super(message);
    }
}
```

A dedicated unchecked exception in the same style as the existing ResourceNotFoundException. It is registered with the error handler as non-retryable so a structurally invalid record is quarantined on the first attempt.

**Validation requirements:** Validation requires repository evidence that a record with a missing or non-numeric quantity is classified non-retryable and quarantined on the first attempt, and that no failure message, log record, or metric tag carries payload content.

**Dependencies:** Depends on P0-008, P0-001, P1-004, P1-005, and P1-006.

**Notes:**

- Implementation: Extraction produces a typed record carrying the same four fields the current code reads, so the inbound payload contract is unchanged.
- Validation: Closure requires evidence that a structurally invalid record produces a quarantined copy rather than a container-default discard.
- Guardrail: Failure messages and telemetry must name the failing field only and never the field value, so quarantine diagnostics cannot leak payload content.

<span style="font-size: 14px;">**Standards reference:** springboot-aks-active-active-master v4.0.0 — `grounding/master/springboot-aks-active-active-master.md`</span>

---

<h3 style="color:#0F6CBD;">
Bounded Dependency Deadlines
</h3>

<!-- finding:F-009 -->
#### P1-004: Azure SQL access has no bounded timeouts

**Priority: P1 - High risk**

**Priority policy:** AA-REMEDIATION-PRIORITY version 1.0.0

**Severity:** critical

**Resiliency Related:** Yes

**Finding status:** Verified finding

**Issue:** The datasource configuration declares only url, username, and password. No HikariCP connection timeout, validation timeout, maximum lifetime, keepalive, or pool size is configured, no JDBC loginTimeout or socketTimeout is present in the connection string, and no query or transaction timeout is declared anywhere in the persistence path. The prod profile supplies the entire URL through an external connection string and adds no timeout property. Every blocking database operation therefore runs to the driver or pool default.

**What does this solve:** Connection acquisition, login, socket reads, query execution, and commit each gain a deadline the service owns and can order against the regional failure budget. A database transition produces a clean bounded failure at a known point instead of an open-ended wait. Operators can tune each budget per environment without a code change.

**Resiliency Impact:** During an Azure SQL failover-group transition, connection acquisition, login, socket reads, query execution, and commit can each block for the driver or pool default. Request threads accumulate against the failing database and the service has no deadline at which it can fail cleanly. The outer gateway timeout becomes the effective deadline, which converts a bounded database transition into an unbounded regional stall. Health transition, traffic draining, and regional withdrawal are all delayed beyond the failure budget.

**Recommended Fix:** Declare HikariCP connection, validation, lifetime, keepalive, and pool-size budgets as externalized placeholders in repository-owned configuration. Supply JDBC login and socket timeouts through Hikari data-source properties so the externally supplied connection string value is never rewritten. Add a JPA query timeout and an explicit timeout on every transactional write path. The resolved connection-string value and the deployed failover-group configuration remain outside the change boundary.

**Remediated with:** P1-005, P1-006

**File:** `source/inventory-service/src/main/resources/application.yml`:6-9

**Repository evidence:**

- Repository path: `source/inventory-service/src/main/resources/application.yml`
- Symbol: `spring.datasource`
- Source fingerprint: `sha256:e5de0c96c016...`
- Assessment snapshot: Workspace snapshot `inventory-service-workspace-2026-09-18`
- Original assessed lines (advisory): 6-9

**Original source requiring update:**

```yaml
datasource:
  url: ${SQL_URL:jdbc:sqlserver://localhost:1433;databaseName=inventory;encrypt=false}
  username: ${SQL_USERNAME}
  password: ${SQL_PASSWORD}
```

**Fix:**

**Proposed change: Externalized dependency deadlines** — `source/inventory-service/src/main/resources/application.yml`

Illustrative proposal only.

```yaml
spring:
  datasource:
    url: ${SQL_URL:jdbc:sqlserver://localhost:1433;databaseName=inventory;encrypt=false}
    username: ${SQL_USERNAME}
    password: ${SQL_PASSWORD}
    hikari:
      connection-timeout: ${SQL_CONNECTION_TIMEOUT_MS}
      validation-timeout: ${SQL_VALIDATION_TIMEOUT_MS}
      max-lifetime: ${SQL_MAX_LIFETIME_MS}
      keepalive-time: ${SQL_KEEPALIVE_MS}
      maximum-pool-size: ${SQL_MAX_POOL_SIZE}
      data-source-properties:
        loginTimeout: ${SQL_LOGIN_TIMEOUT_SECONDS}
        socketTimeout: ${SQL_SOCKET_TIMEOUT_MS}
  jpa:
    properties:
      jakarta.persistence.query.timeout: ${SQL_QUERY_TIMEOUT_MS}
  data:
    redis:
      url: ${REDIS_URL:redis://localhost:6379}
      timeout: ${REDIS_COMMAND_TIMEOUT}
      connect-timeout: ${REDIS_CONNECT_TIMEOUT}
  kafka:
    properties:
      reconnect.backoff.ms: ${KAFKA_RECONNECT_BACKOFF_MS}
      reconnect.backoff.max.ms: ${KAFKA_RECONNECT_BACKOFF_MAX_MS}
      retry.backoff.ms: ${KAFKA_RETRY_BACKOFF_MS}
    producer:
      properties:
        max.block.ms: ${KAFKA_PRODUCER_MAX_BLOCK_MS}
        request.timeout.ms: ${KAFKA_PRODUCER_REQUEST_TIMEOUT_MS}
        delivery.timeout.ms: ${KAFKA_PRODUCER_DELIVERY_TIMEOUT_MS}
    consumer:
      properties:
        session.timeout.ms: ${KAFKA_CONSUMER_SESSION_TIMEOUT_MS}
        heartbeat.interval.ms: ${KAFKA_CONSUMER_HEARTBEAT_INTERVAL_MS}
        max.poll.interval.ms: ${KAFKA_CONSUMER_MAX_POLL_INTERVAL_MS}
        max.poll.records: ${KAFKA_CONSUMER_MAX_POLL_RECORDS}
```

Every deadline is a placeholder with no default, so a deployment must supply a value and no unapproved number is embedded in the repository. JDBC login and socket timeouts are supplied through Hikari data-source-properties rather than by appending to the connection string, so the externally supplied SQL_CONNECTION_STRING value in the prod profile is never rewritten. The existing url, username, password, and Redis url lines are preserved unchanged.

**Proposed change: Explicit transaction deadlines** — `source/inventory-service/src/main/java/com/ecommerce/inventory/service/impl/InventoryServiceImpl.java`

Illustrative proposal only.

```java
@Override
@Transactional(timeout = ${SQL_TRANSACTION_TIMEOUT_SECONDS})
public InventoryResponse release(String productId, int quantity, String referenceId) {
    // Body unchanged; see ICB-008-04 for the idempotent form of this method.
}
```

Every @Transactional write path declares an explicit timeout so a commit cannot block for the driver default. Because the annotation attribute must be a compile-time constant, the implementer binds the value through a constant or a TransactionTemplate rather than a property placeholder; the placeholder shown here identifies the value that must be externalized, not the literal syntax.

**Validation requirements:** Validation requires repository evidence that every declared budget resolves from an environment placeholder and that a blocked database endpoint causes the affected request to fail within the declared budget rather than blocking indefinitely.

**Dependencies:** None.

**Notes:**

- Implementation: Business behavior is unchanged; the change adds pool, driver, persistence, and transaction budgets that the deployment supplies.
- Validation: Closure requires evidence that no timeout value is hardcoded without an override and that every transactional write path declares an explicit timeout.
- Guardrail: No configuration value may contain a region name, regional endpoint, host, or credential, and no numeric budget may be asserted without the approved gateway and load balancer ordering.

<span style="font-size: 14px;">**Standards reference:** springboot-azure-sql v2.3.0 — `grounding/dependencies/springboot-azure-sql.md`</span>

---

<!-- finding:F-010 -->
#### P1-005: Redis access has no bounded connect or command timeouts

**Priority: P1 - High risk**

**Priority policy:** AA-REMEDIATION-PRIORITY version 1.0.0

**Severity:** critical

**Resiliency Related:** Yes

**Finding status:** Verified finding

**Issue:** Redis is configured only through a connection url and a cache type. No command timeout, connect timeout, Lettuce client configuration, pool acquisition timeout, or topology refresh setting is present in either profile. No client configuration customizer exists in production source. Every cache operation therefore runs to the client default.

**What does this solve:** A cache lookup gains a deadline the service owns, so a slow cache fails fast on the request thread instead of extending the latency of a request the authoritative store could already serve. The connect timeout bounds the cost of reestablishing a client during a Redis transition. Both budgets become tunable per environment.

**Resiliency Impact:** Every cached read is subject to the client default command timeout with no repository-owned deadline. When Azure Managed Redis becomes slow rather than unavailable, request threads serving the inventory read endpoint block on the cache lookup even though the authoritative Azure SQL data is available. A non-authoritative cache dependency therefore extends the latency of an otherwise serviceable request and consumes request capacity during a Redis incident.

**Recommended Fix:** Declare a Redis command timeout and a connect timeout as externalized placeholders in repository-owned configuration, ordered inside the request budget so a cache call can never dominate a serviceable read. Keep the existing connection url unchanged. The resolved connection-string value and deployed Redis capacity remain outside the change boundary.

**Remediated with:** P1-004, P1-006

**File:** `source/inventory-service/src/main/resources/application.yml`:13-17

**Repository evidence:**

- Repository path: `source/inventory-service/src/main/resources/application.yml`
- Symbol: `spring.data.redis and spring.cache`
- Source fingerprint: `sha256:395445d5f6c0...`
- Assessment snapshot: Workspace snapshot `inventory-service-workspace-2026-09-18`
- Original assessed lines (advisory): 13-17

**Original source requiring update:**

```yaml
data:
  redis:
    url: ${REDIS_URL:redis://localhost:6379}
cache:
  type: redis
```

**Fix:**

Illustrative proposal only.

```yaml
  data:
    redis:
      url: ${REDIS_URL:redis://localhost:6379}
      timeout: ${REDIS_COMMAND_TIMEOUT}
      connect-timeout: ${REDIS_CONNECT_TIMEOUT}
```

The complete externalized deadline contract covering this dependency, Azure SQL, and Kafka is shown under P1-004.

**Validation requirements:** Validation requires repository evidence that a blocked Redis endpoint causes the cache operation to fail within the declared command timeout rather than holding the request thread.

**Dependencies:** None.

**Notes:**

- Implementation: The existing Redis url and cache type are preserved and only the two deadline properties are added.
- Validation: Closure requires evidence that both Redis budgets resolve from environment placeholders with no hardcoded value.
- Guardrail: The command timeout must be ordered inside the request budget so a cache call can never exceed the deadline of the read it serves.

<span style="font-size: 14px;">**Standards reference:** springboot-azure-managed-redis v2.2.0 — `grounding/dependencies/springboot-azure-managed-redis.md`</span>

---

<!-- finding:F-011 -->
#### P1-006: Kafka client timeouts, reconnect, and backoff are unbounded by repository configuration

**Priority: P1 - High risk**

**Priority policy:** AA-REMEDIATION-PRIORITY version 1.0.0

**Severity:** high

**Resiliency Related:** Yes

**Finding status:** Verified finding

**Issue:** Neither profile declares a producer request timeout, delivery timeout, or max block setting, any reconnect or retry backoff bound, or any consumer session timeout, heartbeat interval, poll interval, or poll record limit. The prod profile adds only bootstrap servers and the security protocol. All client blocking and reconnect behavior is therefore governed by implicit client defaults.

**What does this solve:** Producer blocking, delivery, reconnect, and consumer liveness budgets become explicit values the service owns and can order against the regional failure budget. A producer send against an unreachable broker returns at a known point instead of holding a request thread inside a database transaction. Each budget becomes tunable per environment without a rebuild.

**Resiliency Impact:** Producer sends can block on metadata acquisition for the client default while holding a request thread inside a database transaction. Consumer session and poll-interval behavior during a regional Kafka transition is entirely implicit, so rebalance and reconnect timing cannot be reasoned about. Because the values are not expressed in repository-owned configuration, they cannot be aligned to the regional failure budget or tuned per environment without a code change. Broker unavailability therefore stalls request threads and database transactions beyond the intended budget.

**Recommended Fix:** Declare producer max block, request timeout, and delivery timeout, consumer session timeout, heartbeat interval, poll interval, and poll record limit, and shared reconnect and retry backoff bounds as externalized placeholders in repository-owned configuration. Order each budget against the regional failure budget so broker unavailability produces a bounded failure. Broker-side timeouts and deployed cluster behavior remain outside the change boundary.

**Remediated with:** P1-004, P1-005

**File:** `source/inventory-service/src/main/resources/application-prod.yml`:9-12

**Repository evidence:**

- Repository path: `source/inventory-service/src/main/resources/application-prod.yml`
- Symbol: `spring.kafka`
- Source fingerprint: `sha256:92075e18bc37...`
- Assessment snapshot: Workspace snapshot `inventory-service-workspace-2026-09-18`
- Original assessed lines (advisory): 9-12

**Original source requiring update:**

```yaml
kafka:
  bootstrap-servers: ${KAFKA_BOOTSTRAP_SERVERS}
  properties:
    security.protocol: ${KAFKA_SECURITY_PROTOCOL:PLAINTEXT}
```

**Fix:**

Illustrative proposal only.

```yaml
  kafka:
    properties:
      reconnect.backoff.ms: ${KAFKA_RECONNECT_BACKOFF_MS}
      reconnect.backoff.max.ms: ${KAFKA_RECONNECT_BACKOFF_MAX_MS}
      retry.backoff.ms: ${KAFKA_RETRY_BACKOFF_MS}
    producer:
      properties:
        max.block.ms: ${KAFKA_PRODUCER_MAX_BLOCK_MS}
        request.timeout.ms: ${KAFKA_PRODUCER_REQUEST_TIMEOUT_MS}
        delivery.timeout.ms: ${KAFKA_PRODUCER_DELIVERY_TIMEOUT_MS}
    consumer:
      properties:
        session.timeout.ms: ${KAFKA_CONSUMER_SESSION_TIMEOUT_MS}
        heartbeat.interval.ms: ${KAFKA_CONSUMER_HEARTBEAT_INTERVAL_MS}
        max.poll.interval.ms: ${KAFKA_CONSUMER_MAX_POLL_INTERVAL_MS}
        max.poll.records: ${KAFKA_CONSUMER_MAX_POLL_RECORDS}
```

The complete externalized deadline contract covering this dependency, Azure SQL, and Redis is shown under P1-004.

**Validation requirements:** Validation requires repository evidence that a producer send against an unreachable broker returns within the declared blocking budget rather than holding the calling transaction indefinitely.

**Dependencies:** None.

**Notes:**

- Implementation: Bootstrap servers, the security protocol, consumer group identity, and topic names are unchanged, and only client budget properties are added.
- Validation: Closure requires evidence that every declared Kafka budget resolves from an environment placeholder with no hardcoded value.
- Guardrail: No configuration value may contain a region name, regional endpoint, host, or credential, and the approved active-standby operating scenario is preserved.

<span style="font-size: 14px;">**Standards reference:** springboot-confluent-kafka v3.1.0 — `grounding/dependencies/springboot-confluent-kafka.md`</span>

---

<h3 style="color:#0F6CBD;">
Transient Failure Recovery and Conflict Handling
</h3>

<!-- finding:F-012 -->
#### P1-007: No bounded retry exists for transient Azure SQL failures

**Priority: P1 - High risk**

**Priority policy:** AA-REMEDIATION-PRIORITY version 1.0.0

**Severity:** critical

**Resiliency Related:** Yes

**Finding status:** Verified finding

**Issue:** No retry mechanism of any kind exists. The build declares no spring-retry, resilience4j, Spring Cloud Circuit Breaker, or equivalent dependency, and no production class declares @Retryable, builds a RetryTemplate, or wraps a transaction boundary in a retry policy. A transient SQLTransientException or connection reset therefore propagates out of the service method on the first occurrence.

**What does this solve:** The service rides through a normal Azure SQL transition by retrying classified transient failures at a safe transaction boundary under an externalized, bounded policy. Routine database transitions stop producing user-visible write failures. Consumed order events stop exhausting their attempt budget because of a condition that clears within seconds.

**Resiliency Impact:** Azure SQL failover-group transitions and transient connection resets are expected events in the approved deployment model. Without a bounded retry at a safe transaction boundary, every REST write fails outright and every consumed order event exhausts its container attempts and is abandoned. The service cannot ride through a normal database transition even when the database returns within seconds.

**Recommended Fix:** Introduce the approved resiliency library and wrap the write operations from outside the transaction boundary with a bounded retry that applies only to classified transient failures. Exclude business validation failures and ambiguous commit outcomes from the retryable set, routing ambiguous outcomes through the idempotency check instead. Externalize attempt count, wait duration, backoff, and jitter so every environment supplies its own values. Failover-group transition duration and platform-level retry remain outside the change boundary.

**File:** `source/inventory-service/pom.xml`:7-26

**Repository evidence:**

- Repository path: `source/inventory-service/pom.xml`
- Symbol: `project/dependencies`
- Source fingerprint: `sha256:d1af2cf103de...`
- Assessment snapshot: Workspace snapshot `inventory-service-workspace-2026-09-18`
- Original assessed lines (advisory): 7-26

**Original source requiring update:**

```xml
<dependencies>
    <dependency><groupId>org.springframework.boot</groupId><artifactId>spring-boot-starter-web</artifactId></dependency>
    <dependency><groupId>org.springframework.boot</groupId><artifactId>spring-boot-starter-validation</artifactId></dependency>
    <dependency><groupId>org.springframework.boot</groupId><artifactId>spring-boot-starter-actuator</artifactId></dependency>
    <dependency><groupId>org.springframework.boot</groupId><artifactId>spring-boot-starter-data-jpa</artifactId></dependency>
    <dependency><groupId>org.springframework.boot</groupId><artifactId>spring-boot-starter-data-redis</artifactId></dependency>
    <dependency><groupId>org.springframework.boot</groupId><artifactId>spring-boot-starter-cache</artifactId></dependency>
    <dependency><groupId>org.springframework.kafka</groupId><artifactId>spring-kafka</artifactId></dependency>
    <dependency><groupId>com.microsoft.sqlserver</groupId><artifactId>mssql-jdbc</artifactId><scope>runtime</scope></dependency>
    <dependency><groupId>com.azure.spring</groupId><artifactId>spring-cloud-azure-starter-keyvault-secrets</artifactId></dependency>
    <dependency><groupId>org.springdoc</groupId><artifactId>springdoc-openapi-starter-webmvc-ui</artifactId><version>2.6.0</version></dependency>
    <dependency><groupId>io.micrometer</groupId><artifactId>micrometer-registry-prometheus</artifactId></dependency>
    <dependency><groupId>net.logstash.logback</groupId><artifactId>logstash-logback-encoder</artifactId><version>8.0</version></dependency>
    <dependency><groupId>org.mapstruct</groupId><artifactId>mapstruct</artifactId><version>${mapstruct.version}</version></dependency>
    <dependency><groupId>org.projectlombok</groupId><artifactId>lombok</artifactId><optional>true</optional></dependency>
    <dependency><groupId>org.springframework.boot</groupId><artifactId>spring-boot-starter-test</artifactId><scope>test</scope></dependency>
    <dependency><groupId>org.springframework.kafka</groupId><artifactId>spring-kafka-test</artifactId><scope>test</scope></dependency>
    <dependency><groupId>org.testcontainers</groupId><artifactId>junit-jupiter</artifactId><version>${testcontainers.version}</version><scope>test</scope></dependency>
    <dependency><groupId>org.testcontainers</groupId><artifactId>mssqlserver</artifactId><version>${testcontainers.version}</version><scope>test</scope></dependency>
</dependencies>
```

**File:** `source/inventory-service/src/main/java/com/ecommerce/inventory/service/impl/InventoryServiceImpl.java`:44-50

**Repository evidence:**

- Repository path: `source/inventory-service/src/main/java/com/ecommerce/inventory/service/impl/InventoryServiceImpl.java`
- Symbol: `InventoryServiceImpl.release`
- Source fingerprint: `sha256:b83ea6804189...`
- Assessment snapshot: Workspace snapshot `inventory-service-workspace-2026-09-18`
- Original assessed lines (advisory): 44-50

**Original source requiring update:**

```java
@Override @Transactional
public InventoryResponse release(String productId, int quantity, String referenceId) {
    InventoryItem item = findByProduct(productId);
    if (item.getReservedQuantity() < quantity) throw new IllegalArgumentException("Release exceeds reserved inventory for product: " + productId);
    item.setReservedQuantity(item.getReservedQuantity() - quantity); item.setAvailableQuantity(item.getAvailableQuantity() + quantity); item.setUpdatedAt(Instant.now());
    return saveAndPublish(item, "INVENTORY_RELEASED", referenceId);
}
```

**Fix:**

**Proposed change: Approved resiliency library dependency** — `source/inventory-service/pom.xml`

Illustrative proposal only.

```xml
<dependency>
    <groupId>io.github.resilience4j</groupId>
    <artifactId>resilience4j-spring-boot3</artifactId>
</dependency>
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-aop</artifactId>
</dependency>
```

Resilience4j is the approved resiliency library and retry, circuit breaker, bulkhead, and time limiter are all listed under approved capabilities, so this dependency also supports P1-008 and the later dependency-isolation work. The Spring Boot AOP starter is required for the annotation-driven model and its version is managed by the existing Spring Boot parent. No version is declared for Resilience4j because the approved version source is not yet established.

**Proposed change: Transient failure classifier** — `source/inventory-service/src/main/java/com/ecommerce/inventory/service/TransientFailureClassifier.java`

Illustrative proposal only.

```java
package com.ecommerce.inventory.service;

import org.springframework.dao.ConcurrencyFailureException;
import org.springframework.dao.TransientDataAccessException;
import org.springframework.stereotype.Component;
import org.springframework.transaction.TransactionSystemException;

import java.sql.SQLTransientException;

@Component
public class TransientFailureClassifier {

    public boolean isTransient(Throwable throwable) {
        for (Throwable cause = throwable; cause != null; cause = cause.getCause()) {
            if (cause instanceof TransientDataAccessException
                    || cause instanceof ConcurrencyFailureException
                    || cause instanceof SQLTransientException) {
                return true;
            }
            if (cause instanceof TransactionSystemException) {
                // Commit outcome is unknown; never retried blindly.
                return false;
            }
            if (cause == cause.getCause()) {
                break;
            }
        }
        return false;
    }
}
```

Classification is explicit and conservative. Spring's transient and concurrency data access hierarchies plus the JDBC transient exception are treated as retryable. A TransactionSystemException signals an ambiguous commit outcome and is deliberately excluded, so it is routed to the idempotency check introduced under P0-001 rather than retried. Business failures such as IllegalArgumentException and ResourceNotFoundException are not in the retryable set, so their current caller-visible behaviour is preserved exactly.

**Proposed change: Externalized retry policy** — `source/inventory-service/src/main/resources/application.yml`

Illustrative proposal only.

```yaml
resilience4j:
  retry:
    instances:
      inventoryWrite:
        max-attempts: ${RETRY_WRITE_MAX_ATTEMPTS}
        wait-duration: ${RETRY_WRITE_WAIT_DURATION}
        enable-exponential-backoff: true
        exponential-backoff-multiplier: ${RETRY_WRITE_BACKOFF_MULTIPLIER}
        enable-randomized-wait: true
        randomized-wait-factor: ${RETRY_WRITE_JITTER_FACTOR}
        retry-exception-predicate: com.ecommerce.inventory.service.TransientRetryPredicate
      inventoryConflict:
        max-attempts: ${RETRY_CONFLICT_MAX_ATTEMPTS}
        wait-duration: ${RETRY_CONFLICT_WAIT_DURATION}
        enable-randomized-wait: true
        retry-exceptions:
          - org.springframework.orm.ObjectOptimisticLockingFailureException
```

Two retry instances are declared: one for transient dependency failures governed by the classifier shown above, and one for optimistic-locking conflicts used by P1-008. Every attempt count, wait, multiplier, and jitter factor is an externalized placeholder, so no approved numeric value is asserted by this plan. Randomized wait is enabled on both so a regional recovery does not produce synchronized retry storms.

**Validation requirements:** Validation requires repository evidence that a classified transient database failure is retried at a fresh transaction boundary within a bounded, externally configured budget while business validation failures and ambiguous commit outcomes are not retried.

**Dependencies:** P0-001, P1-004

**Notes:**

- Implementation: Retry is applied outside the transaction boundary so each attempt runs in a fresh transaction, and successful requests are unaffected.
- Validation: Closure requires evidence that attempt count, wait duration, backoff, and jitter resolve from environment placeholders and that retry exhaustion produces a deterministic terminal outcome.
- Guardrail: This change must not be implemented before the idempotency work under P0-001, and the total retry budget must be ordered inside the deadlines established under P1-004.

<span style="font-size: 14px;">**Standards reference:** springboot-azure-sql v2.3.0 — `grounding/dependencies/springboot-azure-sql.md`</span>

---

<!-- finding:F-013 -->
#### P1-008: Optimistic-locking conflicts are neither detected, retried, nor mapped

**Priority: P1 - High risk**

**Priority policy:** AA-REMEDIATION-PRIORITY version 1.0.0

**Severity:** high

**Resiliency Related:** Yes

**Finding status:** Verified finding

**Issue:** InventoryItem declares an @Version column, so concurrent updates to the same row raise ObjectOptimisticLockingFailureException at flush or commit. No service method catches it, no retry reloads and reapplies the adjustment, and no pessimistic lock or conditional update is used on the reserve and release paths. GlobalExceptionHandler maps only ResourceNotFoundException, IllegalArgumentException, and MethodArgumentNotValidException.

**What does this solve:** Ordinary write contention becomes a bounded reload-and-reapply retry rather than a discarded operation. A REST reservation and a consumed order event adjusting the same row stop discarding one of the two operations. When contention cannot be resolved within the attempt budget, the caller receives a stable, documented answer instead of an opaque failure.

**Resiliency Impact:** Two concurrent reservations for the same productId, which is the normal pattern when REST traffic and Kafka consumption both adjust the same item, cause one operation to fail with an unmapped exception surfaced as HTTP 500 or, on the consumer path, an exhausted attempt budget and an abandoned record. Optimistic locking prevents a lost update, but the absence of conflict handling converts an ordinary contention event into lost business work. Contention between REST traffic and consumer traffic becomes more likely, not less, as regional traffic patterns change.

**Recommended Fix:** Wrap reserve and release in a bounded reload-and-reapply retry that re-reads the item and re-evaluates the business precondition on every attempt. Map an exhausted conflict to a documented response rather than an unhandled exception, and route an exhausted conflict on the consumer path through the governed error handler rather than silently advancing the offset. Bound and externalize the attempt budget. Database isolation level configuration deployed at the server remains outside the change boundary.

**File:** `source/inventory-service/src/main/java/com/ecommerce/inventory/model/InventoryItem.java`:26-26

**Repository evidence:**

- Repository path: `source/inventory-service/src/main/java/com/ecommerce/inventory/model/InventoryItem.java`
- Symbol: `InventoryItem.version`
- Source fingerprint: `sha256:5e29c55e63ae...`
- Assessment snapshot: Workspace snapshot `inventory-service-workspace-2026-09-18`
- Original assessed lines (advisory): 26-26

**Original source requiring update:**

```java
@Version private long version;
```

**File:** `source/inventory-service/src/main/java/com/ecommerce/inventory/exception/GlobalExceptionHandler.java`:12-21

**Repository evidence:**

- Repository path: `source/inventory-service/src/main/java/com/ecommerce/inventory/exception/GlobalExceptionHandler.java`
- Symbol: `GlobalExceptionHandler`
- Source fingerprint: `sha256:c2bc4b461279...`
- Assessment snapshot: Workspace snapshot `inventory-service-workspace-2026-09-18`
- Original assessed lines (advisory): 12-21

**Original source requiring update:**

```java
@RestControllerAdvice
public class GlobalExceptionHandler {
    @ExceptionHandler(ResourceNotFoundException.class)
    ResponseEntity<Map<String, Object>> notFound(ResourceNotFoundException exception) { return error(HttpStatus.NOT_FOUND, exception.getMessage()); }
    @ExceptionHandler({IllegalArgumentException.class, MethodArgumentNotValidException.class})
    ResponseEntity<Map<String, Object>> badRequest(Exception exception) { return error(HttpStatus.BAD_REQUEST, exception.getMessage()); }
    private ResponseEntity<Map<String, Object>> error(HttpStatus status, String message) {
        return ResponseEntity.status(status).body(Map.of("timestamp", Instant.now().toString(), "status", status.value(), "error", status.getReasonPhrase(), "message", message));
    }
}
```

**Fix:**

**Proposed change: Bounded reload and reapply** — `source/inventory-service/src/main/java/com/ecommerce/inventory/service/impl/InventoryServiceImpl.java`

Illustrative proposal only.

```java
@Override
@Retry(name = "inventoryConflict")
public InventoryResponse reserve(String productId, int quantity, String referenceId) {
    return transactionTemplate.execute(status -> applyOnce("INVENTORY_RESERVED", productId, referenceId, item -> {
        if (item.getAvailableQuantity() < quantity) {
            throw new IllegalArgumentException("Insufficient inventory for product: " + productId);
        }
        item.setAvailableQuantity(item.getAvailableQuantity() - quantity);
        item.setReservedQuantity(item.getReservedQuantity() + quantity);
    }));
}
```

The retry sits outside the transaction, so each attempt runs in a fresh transaction that re-reads the item through findByProduct and re-evaluates the availability precondition against the reloaded state. That is what makes reload-and-reapply correct rather than a blind replay of a stale computation. The InventoryItem @Version column is unchanged. The idempotency record introduced under P0-001 guarantees the reapplied attempt cannot double-apply if a prior attempt actually committed. The @Retry annotation requires the AOP proxy boundary, so the implementer must ensure the annotated method is invoked through the proxy rather than internally.

**Proposed change: Conflict exhaustion response mapping** — `source/inventory-service/src/main/java/com/ecommerce/inventory/exception/GlobalExceptionHandler.java`

Illustrative proposal only.

```java
@ExceptionHandler(ObjectOptimisticLockingFailureException.class)
ResponseEntity<Map<String, Object>> conflict(ObjectOptimisticLockingFailureException exception) {
    return error(HttpStatus.CONFLICT, "Inventory was modified concurrently. Retry the request.");
}
```

The existing notFound and badRequest handlers and the private error helper are untouched, so the current caller-visible contract for those cases is preserved exactly. The new handler returns a fixed message rather than the exception message, which keeps entity and version detail out of the response. This response mapping is held pending approval of the conflict status code by the API contract owner.

**Validation requirements:** Validation requires repository evidence that a single optimistic-locking conflict on the reserve path is absorbed by a bounded reload-and-reapply that re-evaluates the business precondition, and that an exhausted conflict produces a mapped outcome on the REST path and a governed error outcome on the consumer path.

**Dependencies:** P0-001

**Approval gate:** Returning a dedicated conflict response to API callers when an inventory write cannot be resolved introduces a caller-visible failure outcome the published interface does not emit today, and the API contract owner must approve that response before implementation.

**Notes:**

- Implementation: Successful conflict absorption is invisible to callers, and no business rule or persistence model changes.
- Validation: Closure requires evidence that attempt counts are bounded and externally configurable and that each attempt re-reads the entity rather than replaying stale state.
- Guardrail: This change must not be implemented before the idempotency work under P0-001, and the total attempt budget must be ordered inside the deadlines established under P1-004.

<span style="font-size: 14px;">**Standards reference:** springboot-azure-sql v2.3.0 — `grounding/dependencies/springboot-azure-sql.md`</span>

---

<h3 style="color:#0F6CBD;">
Failure Semantics and Dependency Isolation
</h3>

<!-- finding:F-014 -->
#### P1-009: Dependency failures have no stable caller-visible semantics

**Priority: P1 - High risk**

**Priority policy:** AA-REMEDIATION-PRIORITY version 1.0.0

**Severity:** high

**Resiliency Related:** Yes

**Finding status:** Verified finding

**Issue:** GlobalExceptionHandler maps only three exception types. DataAccessException, Hikari pool exhaustion, RedisConnectionFailureException, RedisCommandTimeoutException, Spring cache serialization failures, and Kafka client exceptions all fall through to framework default error handling. Each of them surfaces as an opaque HTTP 500 with no Retry-After header and no ProblemDetail. The response gives no distinction between a permanent error and a transient dependency outage.

**What does this solve:** A caller and the gateway can tell a transient regional dependency failure apart from a permanent application error, so a retry or reroute decision can be made safely. During a regional dependency incident the API stops returning the same opaque status for a request that would succeed in the peer region as for one that would fail everywhere. Every classification decision becomes an observable, region-tagged signal rather than an undifferentiated error count.

**Resiliency Impact:** Callers and the gateway cannot distinguish a transient regional dependency failure from a permanent application error, so no caller can make a safe retry or failover decision. During a regional dependency incident the API returns the same opaque status for a request that would succeed in the peer region as for one that would fail everywhere. That suppresses the signal the approved multi-region routing design depends on, which means retry and reroute behaviour degrades to guesswork exactly when the failure is regional and recoverable.

**Recommended Fix:** Add a dependency-failure handler that classifies transient dependency exceptions and returns a distinct documented status carrying a Retry-After hint and a stable machine-readable error code. Preserve the existing status mappings and the existing response body shape for permanent application errors. Log the exception detail rather than returning it, so no connection string, host name, or stack detail reaches the caller. Record every classification decision as a region-tagged metric. Gateway retry policy and client behaviour remain outside the change boundary.

**File:** `source/inventory-service/src/main/java/com/ecommerce/inventory/exception/GlobalExceptionHandler.java`:12-21

**Repository evidence:**

- Repository path: `source/inventory-service/src/main/java/com/ecommerce/inventory/exception/GlobalExceptionHandler.java`
- Symbol: `GlobalExceptionHandler exception coverage`
- Source fingerprint: `sha256:c2bc4b46127d...`
- Assessment snapshot: Workspace snapshot `inventory-service-workspace-2026-09-18`
- Original assessed lines (advisory): 12-21

**Original source requiring update:**

```java
@RestControllerAdvice
public class GlobalExceptionHandler {
    @ExceptionHandler(ResourceNotFoundException.class)
    ResponseEntity<Map<String, Object>> notFound(ResourceNotFoundException exception) { return error(HttpStatus.NOT_FOUND, exception.getMessage()); }
    @ExceptionHandler({IllegalArgumentException.class, MethodArgumentNotValidException.class})
    ResponseEntity<Map<String, Object>> badRequest(Exception exception) { return error(HttpStatus.BAD_REQUEST, exception.getMessage()); }
    private ResponseEntity<Map<String, Object>> error(HttpStatus status, String message) {
        return ResponseEntity.status(status).body(Map.of("timestamp", Instant.now().toString(), "status", status.value(), "error", status.getReasonPhrase(), "message", message));
    }
}
```

**Fix:**

Illustrative proposal only.

```java
@ExceptionHandler({DataAccessResourceFailureException.class,
                   QueryTimeoutException.class,
                   TransientDataAccessException.class,
                   RedisConnectionFailureException.class,
                   QueryTimeoutException.class,
                   KafkaException.class})
ResponseEntity<Map<String, Object>> dependencyUnavailable(Exception exception) {
    telemetry.recordFailureClassification(exception.getClass().getSimpleName(), "transient_dependency");
    log.warn("dependency failure classified as transient exception={}", exception.getClass().getName(), exception);
    Map<String, Object> body = new LinkedHashMap<>(error(HttpStatus.SERVICE_UNAVAILABLE,
            "A required dependency is temporarily unavailable.").getBody());
    body.put("code", "DEPENDENCY_UNAVAILABLE");
    return ResponseEntity.status(HttpStatus.SERVICE_UNAVAILABLE)
            .header(HttpHeaders.RETRY_AFTER, String.valueOf(retryAfterSeconds))
            .body(body);
}
```

Transient dependency exceptions are classified and answered with a distinct status, a Retry-After hint, and a stable machine-readable code, while the existing 400 and 404 mappings and the existing body shape are preserved. The exception message is logged rather than returned, so no connection string, host name, or stack detail reaches the caller. The classification itself is recorded as a metric, and that telemetry portion of the change carries no caller-visible contract effect; the status contract is held pending approval.

**Validation requirements:** Validation requires repository evidence that transient dependency failures are classified and answered with a distinct approved status and a Retry-After header, that permanent application errors keep their current status codes and body shape, and that no response, header, or log record exposes a credential, connection string, stack trace, or internal host name.

**Dependencies:** P0-008

**Approval gate:** Returning a dedicated temporarily-unavailable response with a retry hint when a backing dependency fails introduces a new failure outcome that partners and the gateway will observe on the published interface, and the API contract owner must approve that response, its retry guidance, and its error-code vocabulary before implementation.

**Notes:**

- Implementation: Only the exception-to-status mapping and the error response contract in the handler change; no business rule, persistence model, or dependency call path is altered.
- Validation: Closure requires evidence that each classification decision increments a region-tagged counter carrying the classified outcome as a dimension.
- Guardrail: The dependency-failure message returned to callers must remain fixed text, and the underlying exception detail must be confined to the log record.

<span style="font-size: 14px;">**Standards reference:** springboot-aks-active-active-master v4.0.0 — `grounding/master/springboot-aks-active-active-master.md`</span>

---

<!-- finding:F-015 -->
#### P1-010: No isolation exists between request threads and blocking dependencies

**Priority: P1 - High risk**

**Priority policy:** AA-REMEDIATION-PRIORITY version 1.0.0

**Severity:** high

**Resiliency Related:** Yes

**Finding status:** Verified finding

**Issue:** The build declares no resilience4j, Spring Cloud Circuit Breaker, Hystrix, or rate-limiter dependency, and production source defines no bulkhead, semaphore, or custom executor. All REST request processing, cache access, database access, and Kafka production execute on the default servlet container thread pool. That default pool is far larger than the default HikariCP pool, with no rejection policy and no queue bound between them. Every dependency call therefore competes for the same unbounded shared capacity.

**What does this solve:** A slow Redis or a blocked Azure SQL pool no longer parks every servlet thread. Read endpoints that do not touch the failing dependency keep responding, and the Actuator endpoints served on the same port continue to answer probes. One failing capability degrades on its own instead of removing the pod, and the region, from service.

**Resiliency Impact:** A single degraded dependency consumes the entire shared request-thread pool. A slow Redis or a blocked Azure SQL pool causes every servlet thread to park, so read endpoints that do not touch the failing dependency, and the Actuator endpoints served on the same port, also stop responding. One dependency failure therefore removes the whole pod from service rather than degrading a single capability, and the blast radius escalates from one capability to regional loss of service.

**Recommended Fix:** Bound concurrent calls per dependency with a semaphore bulkhead so the cache path and the authoritative store path cannot consume each other's capacity or the whole servlet pool. Open a circuit breaker on classified dependency failure so callers fail fast instead of parking indefinitely. Externalize every concurrency limit, failure-rate threshold, window size, open duration, half-open call count, and wait duration. Emit region-tagged metrics for breaker state transitions and bulkhead rejections. Pod CPU and memory limits and mesh-level outlier detection remain outside the change boundary.

**File:** `source/inventory-service/pom.xml`:7-26

**Repository evidence:**

- Repository path: `source/inventory-service/pom.xml`
- Symbol: `project/dependencies`
- Source fingerprint: `sha256:d1af2cf103de...`
- Assessment snapshot: Workspace snapshot `inventory-service-workspace-2026-09-18`
- Original assessed lines (advisory): 7-26

**Original source requiring update:**

```xml
    <dependencies>
        <dependency><groupId>org.springframework.boot</groupId><artifactId>spring-boot-starter-web</artifactId></dependency>
        <dependency><groupId>org.springframework.boot</groupId><artifactId>spring-boot-starter-validation</artifactId></dependency>
        <dependency><groupId>org.springframework.boot</groupId><artifactId>spring-boot-starter-actuator</artifactId></dependency>
        <dependency><groupId>org.springframework.boot</groupId><artifactId>spring-boot-starter-data-jpa</artifactId></dependency>
        <dependency><groupId>org.springframework.boot</groupId><artifactId>spring-boot-starter-data-redis</artifactId></dependency>
        <dependency><groupId>org.springframework.boot</groupId><artifactId>spring-boot-starter-cache</artifactId></dependency>
        <dependency><groupId>org.springframework.kafka</groupId><artifactId>spring-kafka</artifactId></dependency>
        <dependency><groupId>com.microsoft.sqlserver</groupId><artifactId>mssql-jdbc</artifactId><scope>runtime</scope></dependency>
        <dependency><groupId>com.azure.spring</groupId><artifactId>spring-cloud-azure-starter-keyvault-secrets</artifactId></dependency>
        <dependency><groupId>org.springdoc</groupId><artifactId>springdoc-openapi-starter-webmvc-ui</artifactId><version>2.6.0</version></dependency>
        <dependency><groupId>io.micrometer</groupId><artifactId>micrometer-registry-prometheus</artifactId></dependency>
        <dependency><groupId>net.logstash.logback</groupId><artifactId>logstash-logback-encoder</artifactId><version>8.0</version></dependency>
        <dependency><groupId>org.mapstruct</groupId><artifactId>mapstruct</artifactId><version>${mapstruct.version}</version></dependency>
        <dependency><groupId>org.projectlombok</groupId><artifactId>lombok</artifactId><optional>true</optional></dependency>
        <dependency><groupId>org.springframework.boot</groupId><artifactId>spring-boot-starter-test</artifactId><scope>test</scope></dependency>
        <dependency><groupId>org.springframework.kafka</groupId><artifactId>spring-kafka-test</artifactId><scope>test</scope></dependency>
        <dependency><groupId>org.testcontainers</groupId><artifactId>junit-jupiter</artifactId><version>${testcontainers.version}</version><scope>test</scope></dependency>
        <dependency><groupId>org.testcontainers</groupId><artifactId>mssqlserver</artifactId><version>${testcontainers.version}</version><scope>test</scope></dependency>
    </dependencies>
```

The assessed dependency list above records the absence of any bulkhead, circuit breaker, or rate-limiter library. Production source likewise defines no bulkhead, semaphore, or custom executor, and no bulkhead, breaker, or rate-limiter property exists in either application profile, so there is no existing source excerpt to cite for those elements.

**Fix:**

**Proposed change: Technology-neutral isolation boundary** — `source/inventory-service/src/main/java/com/ecommerce/inventory/service/impl/InventoryServiceImpl.java`

Illustrative proposal only.

```java
@Override
@Cacheable(cacheNames = "inventory", key = "#id", sync = true)
@Bulkhead(name = "inventoryCache", type = Bulkhead.Type.SEMAPHORE)
public InventoryResponse get(Long id) {
    return mapper.toResponse(find(id));
}

@Override
@Bulkhead(name = "inventoryDb", type = Bulkhead.Type.SEMAPHORE)
@CircuitBreaker(name = "inventoryDb")
@Retry(name = "inventoryWrite")
public InventoryResponse create(InventoryRequest request) {
    // Body unchanged.
}
```

Concurrency into the cache path and into the authoritative store are bounded separately, so a saturated cache cannot consume the capacity the database path needs and neither can consume the whole servlet pool. Semaphore bulkheads are used rather than thread-pool bulkheads because the existing programming model is synchronous servlet code and a thread-pool bulkhead would break the transaction and security context propagation this service relies on. The sync attribute shown here belongs to P1-014; it appears because the two changes edit the same annotation.

**Proposed change: Externalized bulkhead and breaker policy** — `source/inventory-service/src/main/resources/application.yml`

Illustrative proposal only.

```yaml
resilience4j:
  bulkhead:
    instances:
      inventoryDb:
        max-concurrent-calls: ${BULKHEAD_DB_MAX_CONCURRENT}
        max-wait-duration: ${BULKHEAD_DB_MAX_WAIT}
      inventoryCache:
        max-concurrent-calls: ${BULKHEAD_CACHE_MAX_CONCURRENT}
        max-wait-duration: ${BULKHEAD_CACHE_MAX_WAIT}
  circuitbreaker:
    instances:
      inventoryDb:
        sliding-window-type: COUNT_BASED
        sliding-window-size: ${BREAKER_DB_WINDOW_SIZE}
        minimum-number-of-calls: ${BREAKER_DB_MIN_CALLS}
        failure-rate-threshold: ${BREAKER_DB_FAILURE_RATE}
        wait-duration-in-open-state: ${BREAKER_DB_OPEN_DURATION}
        permitted-number-of-calls-in-half-open-state: ${BREAKER_DB_HALF_OPEN_CALLS}
        automatic-transition-from-open-to-half-open-enabled: true
        record-exceptions:
          - org.springframework.dao.TransientDataAccessException
          - org.springframework.dao.DataAccessResourceFailureException
        ignore-exceptions:
          - com.ecommerce.inventory.exception.ResourceNotFoundException
          - java.lang.IllegalArgumentException
      inventoryCache:
        sliding-window-type: COUNT_BASED
        sliding-window-size: ${BREAKER_CACHE_WINDOW_SIZE}
        minimum-number-of-calls: ${BREAKER_CACHE_MIN_CALLS}
        failure-rate-threshold: ${BREAKER_CACHE_FAILURE_RATE}
        wait-duration-in-open-state: ${BREAKER_CACHE_OPEN_DURATION}
        permitted-number-of-calls-in-half-open-state: ${BREAKER_CACHE_HALF_OPEN_CALLS}
        automatic-transition-from-open-to-half-open-enabled: true
  metrics:
    enabled: true
```

No threshold, window size, open duration, half-open call count, or wait duration is hardcoded; every value is an externalized placeholder. The exception lists are not invented: recorded exceptions are the same Spring data access types the transient-failure classifier introduced under P1-007 treats as transient, and ignored exceptions are the two business exception types the service already throws, so business failures never move the breaker. Automatic half-open transition ensures the breaker recovers without traffic having to arrive at exactly the right moment.

**Proposed change: Isolation telemetry binding** — `source/inventory-service/src/main/resources/application.yml`

Illustrative proposal only.

```yaml
management:
  metrics:
    distribution:
      percentiles-histogram:
        resilience4j.circuitbreaker.calls: true
        resilience4j.bulkhead.available.concurrent.calls: true
```

Resilience4j registers its own meters into the existing Micrometer Prometheus registry, so breaker state transitions and bulkhead rejections reach the already-exposed prometheus endpoint with the region and role tags established under P0-007. Only the distribution hint is added; the exposure list is unchanged, so no new endpoint becomes reachable.

**Validation requirements:** Validation requires repository evidence that concurrent calls to the authoritative store and to the cache are separately bounded and externally configurable, that a saturated cache does not block an inventory read that misses the cache from completing against the authoritative store, that a saturated or open dependency produces a fast classified failure rather than an indefinite park, and that health and metrics endpoints keep responding while a dependency is saturated.

**Dependencies:** P1-004, P1-007

**Notes:**

- Implementation: Successful requests are unaffected, and the isolation boundary is introduced through the approved resilience library with no unapproved substitution.
- Validation: Closure requires evidence that breaker state transitions and bulkhead rejections emit region-tagged metrics and that no limit, threshold, window size, open duration, half-open call count, or wait duration is hardcoded.
- Guardrail: The breaker call budget must be shorter than the dependency deadlines established under P1-004, which must in turn remain shorter than the gateway budget, and rejected requests surface through the approval-gated failure classification described in P1-009.

<span style="font-size: 14px;">**Standards reference:** springboot-aks-active-active-master v4.0.0 — `grounding/master/springboot-aks-active-active-master.md`</span>

---

<h3 style="color:#0F6CBD;">
Cache Behaviour Under Load and Failure
</h3>

<!-- finding:F-016 -->
#### P1-011: Redis cache failures propagate into the request path with no error handler

**Priority: P1 - High risk**

**Priority policy:** AA-REMEDIATION-PRIORITY version 1.0.0

**Severity:** critical

**Resiliency Related:** Yes

**Finding status:** Verified finding

**Issue:** The cache configuration class declares caching support with an empty body. It does not implement the caching configurer contract, registers no cache error handler, and supplies no Redis cache manager. With the cache type set to redis, any Redis get, put, or evict failure raised by the cache interceptor propagates to the caller instead of being absorbed. The interceptor therefore never falls through to the authoritative Azure SQL repository.

**What does this solve:** A Redis outage stops taking down a serviceable read capability whose authoritative data remains fully available. Cache eviction failures stop failing otherwise successful writes. The cache becomes genuinely optional, which is the precondition for excluding Redis from the readiness group.

**Resiliency Impact:** Azure Managed Redis is a cache whose authoritative source is Azure SQL, yet a Redis outage makes the inventory read endpoint fail outright even though the authoritative data is fully available. Cache eviction failures on update and delete propagate the same way and can fail an otherwise successful write. A non-authoritative dependency is therefore able to take down a serviceable capability in the region.

**Recommended Fix:** Implement the caching configurer contract and register a cache error handler that absorbs get, put, evict, and clear failures. Record absorbed failures as a cache-failure outcome that is a distinct dimension from a cache miss, and log them at warning level with the cache name and exception class only. Allow the cache interceptor to fall through to the authoritative repository on a get failure. Azure Managed Redis availability and deployed topology remain outside the change boundary.

**File:** `source/inventory-service/src/main/java/com/ecommerce/inventory/config/CacheConfig.java`:6-8

**Repository evidence:**

- Repository path: `source/inventory-service/src/main/java/com/ecommerce/inventory/config/CacheConfig.java`
- Symbol: `CacheConfig`
- Source fingerprint: `sha256:a6a2631175d3...`
- Assessment snapshot: Workspace snapshot `inventory-service-workspace-2026-09-18`
- Original assessed lines (advisory): 6-8

**Original source requiring update:**

```java
@Configuration @EnableCaching
public class CacheConfig {
}
```

**Fix:**

Illustrative proposal only.

```java
package com.ecommerce.inventory.config;

import com.ecommerce.inventory.observability.InventoryTelemetry;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.cache.Cache;
import org.springframework.cache.annotation.CachingConfigurer;
import org.springframework.cache.annotation.EnableCaching;
import org.springframework.cache.interceptor.CacheErrorHandler;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

@Slf4j
@Configuration
@EnableCaching
@RequiredArgsConstructor
public class CacheConfig implements CachingConfigurer {

    private final InventoryTelemetry telemetry;

    @Bean
    @Override
    public CacheErrorHandler errorHandler() {
        return new CacheErrorHandler() {
            @Override
            public void handleCacheGetError(RuntimeException exception, Cache cache, Object key) {
                absorb("get", cache, exception);
            }

            @Override
            public void handleCachePutError(RuntimeException exception, Cache cache, Object key, Object value) {
                absorb("put", cache, exception);
            }

            @Override
            public void handleCacheEvictError(RuntimeException exception, Cache cache, Object key) {
                absorb("evict", cache, exception);
            }

            @Override
            public void handleCacheClearError(RuntimeException exception, Cache cache) {
                absorb("clear", cache, exception);
            }

            private void absorb(String operation, Cache cache, RuntimeException exception) {
                telemetry.recordCacheOutcome(cache.getName(), InventoryTelemetry.CACHE_FAILURE);
                log.warn("cache operation failed operation={} cache={} exception={}",
                        operation, cache.getName(), exception.getClass().getName());
            }
        };
    }
}
```

Implementing the caching configurer contract and returning a cache error handler that absorbs rather than rethrows is what makes the cache genuinely optional: the cache interceptor falls through to the repository on a get failure, and a put, evict, or clear failure no longer fails the surrounding operation. Each absorbed failure is counted as a cache failure, which is a distinct dimension from a cache miss, and logged without any cached value content. The existing caching declaration is preserved.

**Validation requirements:** Validation requires repository evidence that a Redis get failure still returns a read served from the authoritative repository, that put, evict, and clear failures do not fail the surrounding operation, and that absorbed failures are counted and logged separately from cache misses with no cached value content.

**Dependencies:** P0-008

**Notes:**

- Implementation: Only cache-failure handling is introduced; the caching declaration, cached values, and business behaviour are unchanged.
- Validation: Closure requires repository evidence that absorbed cache failures increment a cache-failure counter distinct from the cache-miss counter.
- Guardrail: Absorbed eviction failures must remain bounded by the entry expiry established under P1-012 so a stale entry cannot survive indefinitely.

<span style="font-size: 14px;">**Standards reference:** springboot-azure-managed-redis v2.2.0 — `grounding/dependencies/springboot-azure-managed-redis.md`</span>

---

<!-- finding:F-017 -->
#### P1-012: Cached entries have no TTL or expiration policy

**Priority: P1 - High risk**

**Priority policy:** AA-REMEDIATION-PRIORITY version 1.0.0

**Severity:** high

**Resiliency Related:** Yes

**Finding status:** Verified finding

**Issue:** The cache type is set to redis with no time-to-live property, no per-cache Redis cache configuration, and no entry expiry on any cache. The cache configuration class supplies no Redis cache manager. Inventory cache entries are therefore written without expiry and persist until they are explicitly evicted or until Redis evicts them under memory pressure.

**What does this solve:** Cache entries expire on a bounded schedule rather than persisting for the lifetime of the deployment. A bounded freshness window lets a regional cache converge after a failover. Eviction stops depending on the deployed memory policy reaching its limit.

**Resiliency Impact:** Cache entries accumulate without bound across the lifetime of the deployment and are only removed by an explicit evict on update or delete. Entries for items mutated through reserve and release are never evicted at all, so they persist indefinitely. Growth is limited only by the deployed Redis memory policy, at which point eviction behaviour becomes non-deterministic, and there is no bounded freshness window that would let a regional cache converge after a failover.

**Recommended Fix:** Declare an explicit Redis cache configuration bean carrying an externalized entry time-to-live, an explicit JSON value serializer bound to the cached type, and a key prefix composed from externalized application, environment, and cache schema version qualifiers. Do not cache null values. Externalize the expiry value and the environment qualifier rather than asserting either in the repository. Azure Managed Redis memory policy and capacity remain outside the change boundary.

**Remediated with:** P1-013, P1-017

**File:** `source/inventory-service/src/main/resources/application.yml`:16-17

**Repository evidence:**

- Repository path: `source/inventory-service/src/main/resources/application.yml`
- Symbol: `spring.cache`
- Source fingerprint: `sha256:5921b25eb1c9...`
- Assessment snapshot: Workspace snapshot `inventory-service-workspace-2026-09-18`
- Original assessed lines (advisory): 16-17

**Original source requiring update:**

```yaml
  cache:
    type: redis
```

**Fix:**

**Proposed change: Explicit Redis cache manager configuration** — `source/inventory-service/src/main/java/com/ecommerce/inventory/config/CacheConfig.java`

Illustrative proposal only.

```java
@Bean
public RedisCacheConfiguration inventoryCacheConfiguration(
        @Value("${app.cache.inventory.ttl}") Duration ttl,
        @Value("${app.cache.key-prefix}") String keyPrefix,
        @Value("${app.cache.schema-version}") String schemaVersion,
        ObjectMapper objectMapper) {

    ObjectMapper cacheMapper = objectMapper.copy().registerModule(new JavaTimeModule());
    Jackson2JsonRedisSerializer<InventoryResponse> valueSerializer =
            new Jackson2JsonRedisSerializer<>(cacheMapper, InventoryResponse.class);

    return RedisCacheConfiguration.defaultCacheConfig()
            .entryTtl(ttl)
            .disableCachingNullValues()
            .computePrefixWith(cacheName -> keyPrefix + ':' + schemaVersion + ':' + cacheName + "::")
            .serializeKeysWith(SerializationPair.fromSerializer(new StringRedisSerializer()))
            .serializeValuesWith(SerializationPair.fromSerializer(valueSerializer));
}
```

One bean resolves all three defects. An explicit Jackson serializer bound to the cached response type removes the dependency on JDK serialization, so the record no longer needs to implement the serializable marker. The entry expiry gives every entry a bounded lifetime sourced from configuration. The computed prefix puts an externalized application and environment prefix and a cache schema version in front of every key, so two deployments sharing a Redis instance and two application versions during a rolling release write to disjoint key spaces. Disabling null caching preserves the existing behaviour in which a missing item raises the not-found exception before any cache write.

**Proposed change: Cache contract properties** — `source/inventory-service/src/main/resources/application.yml`

Illustrative proposal only.

```yaml
  cache:
    type: redis
app:
  cache:
    key-prefix: ${CACHE_KEY_PREFIX:inventory-service:local}
    schema-version: v1
    inventory:
      ttl: ${CACHE_INVENTORY_TTL}
```

The cache type stays redis. The key prefix carries the application and environment qualifier and is supplied at deployment time, the schema version is a repository-owned constant that the team bumps when the cached response model changes, and the expiry is an externalized placeholder with no value asserted by this plan.

**Validation requirements:** Validation requires repository evidence that every cache entry carries an expiry sourced from externalized configuration, that the value serializer is declared explicitly without reliance on Java serialization, and that every key is prefixed with the application, environment, and cache schema version qualifiers.

**Dependencies:** None.

**Notes:**

- Implementation: The cached value wire format and the key space change together, so no reader ever encounters a value written under the previous contract.
- Validation: Closure requires repository evidence that changing the cache schema version produces a disjoint key space with no reuse of previously cached values.
- Guardrail: No expiry value and no environment qualifier may be hardcoded; both remain deployment-supplied inputs that are still unresolved.

<span style="font-size: 14px;">**Standards reference:** springboot-azure-managed-redis v2.2.0 — `grounding/dependencies/springboot-azure-managed-redis.md`</span>

---

<!-- finding:F-019 -->
#### P1-014: Concurrent cache misses are not coalesced

**Priority: P1 - High risk**

**Priority policy:** AA-REMEDIATION-PRIORITY version 1.0.0

**Severity:** high

**Resiliency Related:** Yes

**Finding status:** Verified finding

**Issue:** The cached read is declared without synchronized loading, and no single-flight, lock, or set-if-absent guard exists around the cache loader. Every concurrent miss for the same key therefore executes its own repository lookup against Azure SQL. Nothing limits how many concurrent loads a single cold key can produce.

**What does this solve:** A regional cache that is empty after a failover or a Redis restart produces one authoritative read per key rather than one per concurrent request. The authoritative store is protected during exactly the window the approved regional recovery model creates.

**Resiliency Impact:** A cold start, a Redis restart, a regional cache that has not yet been populated after a failover, or a burst of traffic for a popular product causes every concurrent request to fan out to Azure SQL at once. This happens precisely when the database is most likely to be recovering. Combined with the absence of any isolation boundary described in P1-010, it can exhaust the connection pool and the request threads at the same moment.

**Recommended Fix:** Declare synchronized loading on the cached read so the cache abstraction coalesces concurrent loads for the same key. Keep the cache name, key expression, return type, and method body unchanged so no caller observes a different value. Redis capacity and Azure SQL server-side concurrency limits remain outside the change boundary.

**File:** `source/inventory-service/src/main/java/com/ecommerce/inventory/service/impl/InventoryServiceImpl.java`:30-31

**Repository evidence:**

- Repository path: `source/inventory-service/src/main/java/com/ecommerce/inventory/service/impl/InventoryServiceImpl.java`
- Symbol: `InventoryServiceImpl.get @Cacheable`
- Source fingerprint: `sha256:af81ef398962...`
- Assessment snapshot: Workspace snapshot `inventory-service-workspace-2026-09-18`
- Original assessed lines (advisory): 30-31

**Original source requiring update:**

```java
    @Override @Cacheable(cacheNames = "inventory", key = "#id")
    public InventoryResponse get(Long id) { return mapper.toResponse(find(id)); }
```

**Fix:**

Illustrative proposal only.

```java
@Override
@Cacheable(cacheNames = "inventory", key = "#id", sync = true)
public InventoryResponse get(Long id) {
    return mapper.toResponse(find(id));
}
```

Synchronized loading makes the cache abstraction coalesce concurrent loads for the same key, so an empty regional cache after a failover or a Redis restart produces one authoritative read per key rather than one per request. The cache name, key expression, return type, and method body are unchanged, so the value returned to every caller is identical.

**Validation requirements:** Validation requires repository evidence that concurrent reads for the same identifier against an empty cache produce exactly one repository read, that reads for different identifiers are not serialized against one another, and that the value returned to callers is unchanged.

**Dependencies:** P1-012

**Notes:**

- Implementation: The cache name, key expression, return type, and method body are unchanged, so no caller observes a different value.
- Validation: Closure requires repository evidence that coalescing is active on the cached read path and does not serialize loads for distinct keys.
- Guardrail: Coalesced loads must remain bounded by the dependency deadlines and the isolation boundary established under P1-004 and P1-010 so a slow authoritative read cannot park waiters indefinitely.

<span style="font-size: 14px;">**Standards reference:** springboot-azure-managed-redis v2.2.0 — `grounding/dependencies/springboot-azure-managed-redis.md`</span>

---

<h3 style="color:#0F6CBD;">
Credential Rotation
</h3>

<!-- finding:F-023 -->
#### P1-015: Secrets are bound once at startup with no refresh or rotation handling

**Priority: P1 - High risk**

**Priority policy:** AA-REMEDIATION-PRIORITY version 1.0.0

**Severity:** high

**Resiliency Related:** Yes

**Finding status:** Verified finding

**Issue:** Key Vault material is resolved through a Spring property source at startup. No refresh interval, scheduled refresh, refresh-scoped bean, environment-change listener, or client-recreation path exists. The connection pool for Azure SQL and the Redis connection factory are therefore initialized once with startup material and retain it for the lifetime of the process. Nothing in the application detects that the held material has become invalid.

**What does this solve:** Recovery from a credential or identity event stops requiring a manual rolling restart of every pod in the region. A rotated database password, a regenerated Redis access key, or a vault restored after an incident converges automatically. Where automatic convergence is not possible for a given client, the restart requirement becomes an explicit and observable contract rather than an implicit assumption.

**Resiliency Impact:** A credential rotation, a regenerated Redis access key, or a restored vault after an incident cannot take effect without a full pod restart. The application holds invalid material and continues to present it on every new connection attempt with no detection path. Regional recovery therefore depends on an operator performing a rolling restart, which extends the outage window. The recovery path is operator-dependent at exactly the moment automated convergence matters most.

**Recommended Fix:** Declare a Key Vault property-source refresh interval so the property source reloads on an externally configured schedule. Add a rotation handler that detects a changed credential value, applies it to the connection pool, and turns over pooled connections so new connections use the refreshed material. Gate the whole path behind externalized flags that default to off so the change is inert until a deployment opts in. Where automatic re-initialization is not implemented for a client, state the restart requirement explicitly in repository-owned configuration and emit it as an observable signal.

**File:** `source/inventory-service/src/main/resources/application-prod.yml`:1-3

**Repository evidence:**

- Repository path: `source/inventory-service/src/main/resources/application-prod.yml`
- Symbol: `spring.config.import`
- Source fingerprint: `sha256:e7c1e56e4046...`
- Assessment snapshot: Workspace snapshot `inventory-service-workspace-2026-09-18`
- Original assessed lines (advisory): 1-3

**Original source requiring update:**

```yaml
spring:
  config:
    import: azure-keyvault:${AZURE_KEYVAULT_ENDPOINT}
```

**Fix:**

**Proposed change: Key Vault property source refresh** — `source/inventory-service/src/main/resources/application-prod.yml`

Illustrative proposal only.

```yaml
spring:
  cloud:
    azure:
      keyvault:
        secret:
          property-sources:
            - name: inventory-secrets
              endpoint: ${AZURE_KEYVAULT_ENDPOINT}
              refresh-interval: ${KEYVAULT_REFRESH_INTERVAL}
app:
  secrets:
    rotation:
      enabled: ${SECRET_ROTATION_ENABLED:false}
      pool-eviction-enabled: ${SECRET_POOL_EVICTION_ENABLED:false}
```

The declared Spring Cloud Azure starter supports a property-source refresh interval, so the reload is a supported capability of an existing dependency rather than a new mechanism. The refresh interval and both rotation behaviours are externalized, and both rotation flags default to false so the change is inert until a deployment opts in.

**Proposed change: Datasource credential rotation handling** — `source/inventory-service/src/main/java/com/ecommerce/inventory/config/SecretRotationHandler.java`

Illustrative proposal only.

```java
package com.ecommerce.inventory.config;

import com.ecommerce.inventory.observability.InventoryTelemetry;
import com.zaxxer.hikari.HikariDataSource;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.boot.context.properties.ConfigurationPropertiesBinding;
import org.springframework.core.env.Environment;
import org.springframework.scheduling.annotation.Scheduled;
import org.springframework.stereotype.Component;

import javax.sql.DataSource;
import java.util.Objects;

@Slf4j
@Component
public class SecretRotationHandler {

    private final DataSource dataSource;
    private final Environment environment;
    private final InventoryTelemetry telemetry;
    private final boolean poolEvictionEnabled;
    private volatile String lastObservedPassword;

    public SecretRotationHandler(DataSource dataSource,
                                 Environment environment,
                                 InventoryTelemetry telemetry,
                                 @Value("${app.secrets.rotation.pool-eviction-enabled:false}") boolean poolEvictionEnabled) {
        this.dataSource = dataSource;
        this.environment = environment;
        this.telemetry = telemetry;
        this.poolEvictionEnabled = poolEvictionEnabled;
        this.lastObservedPassword = environment.getProperty("spring.datasource.password");
    }

    @Scheduled(fixedDelayString = "${app.secrets.rotation.check-interval}")
    public void applyRotationIfChanged() {
        if (!poolEvictionEnabled || !(dataSource instanceof HikariDataSource hikari)) {
            return;
        }
        String current = environment.getProperty("spring.datasource.password");
        if (Objects.equals(current, lastObservedPassword)) {
            return;
        }
        lastObservedPassword = current;
        hikari.getHikariConfigMXBean().setPassword(current);
        hikari.getHikariPoolMXBean().softEvictConnections();
        telemetry.recordCredentialRotation("datasource");
        log.info("credential rotation applied target=datasource action=soft_evict");
    }
}
```

The connection pool exposes a supported runtime password update and a non-disruptive connection turnover, so the datasource converges on rotated material without a process restart and without dropping in-flight work. The handler compares the refreshed property value rather than reacting to a failure, so it is proactive and does not depend on an authentication error occurring first. The whole path is gated behind an externalized flag that defaults to false. No secret value is logged or recorded as a metric tag.

**Proposed change: Redis client re-initialization on rotation** — target repository path not yet selected

**Illustrative code status:** Targeted implementation discovery required

**Why code was not generated:** Production Redis credentials and the TLS scheme are contained inside the externally supplied connection-string value, which is recorded as outside repository evidence. Whether the rotated material arrives as a new password within the same URL, as an entirely new URL, or as a managed-identity token determines whether a credential update, a full client re-creation, or a token-refresh hook is the correct mechanism. Choosing one without that fact would invent an unverifiable client lifecycle.

**Unresolved inputs:**

- Resolved Redis connection-string scheme and authentication mode per region
- Whether Redis authentication uses an access key or a managed identity token

**Intended behavior:** On a rotated Redis access key the connection factory would need to pick up the new credential and re-establish connections without a process restart.

**Validation requirements:** Validation requires repository evidence that the refresh interval is externally overridable, that a credential rejection is classified separately from a connectivity failure, that new connections are established with refreshed material without a process restart, and that no secret value reaches a log record, metric name, metric tag, or health detail.

**Dependencies:** P0-005, P0-007

**Notes:**

- Implementation: The rotation path is additive and gated behind externalized flags that default to off, so no existing startup binding changes until a deployment opts in.
- Validation: Closure requires repository evidence that rotated material takes effect on new connections without a process restart, and that any client without automatic re-initialization declares its restart requirement explicitly.
- Guardrail: The refresh interval must remain externally supplied and bounded by the vault client retry budget so a short interval cannot drive vault request volume into throttling.

<span style="font-size: 14px;">**Standards reference:** springboot-keyvault v2.2.0 — `grounding/dependencies/springboot-keyvault.md`</span>

---

<h3 style="color:#0F6CBD;">
Request Resource Bounding
</h3>

<!-- finding:F-025 -->
#### P1-016: The list endpoint loads the entire inventory table into memory

**Priority: P1 - High risk**

**Priority policy:** AA-REMEDIATION-PRIORITY version 1.0.0

**Severity:** high

**Resiliency Related:** Yes

**Finding status:** Verified finding

**Issue:** The list operation reads every row from the inventory table, streams every returned entity through the mapper, and collects the result into a list. There is no page parameter, no page size, no result limit, no streaming, and no maximum on the response. The public list endpoint exposes this directly and without authentication-derived scoping. Peak heap for a single request is therefore a function of table size rather than of anything the application controls.

**What does this solve:** The peak heap required by a list request becomes a function of the page size rather than of the inventory table size. Ordinary API usage can no longer drive a pod into sustained garbage-collection pressure or an out-of-memory failure. Regional serving capacity stops depending on how large the inventory table has grown.

**Resiliency Impact:** The peak heap required by a single request grows linearly with the inventory table and is entirely outside application control. Concurrent calls multiply the allocation. Because there is no isolation boundary under P1-010 and no dependency deadline under P1-004, a handful of concurrent list requests against a large table can drive the pod into sustained garbage-collection pressure or an out-of-memory failure. The resulting pod loss is indistinguishable from a dependency failure and removes capacity from the region.

**Recommended Fix:** Expose a paged list operation that pushes the bound into the repository query, so allocation is capped by the requested page rather than by the table. Externalize a default and a maximum page size so a caller cannot defeat the bound by requesting a very large page. Keep the element shape unchanged so the mapped record a caller receives is identical. Hold the caller-visible response-shape change until the contract owner approves the pagination model.

**File:** `source/inventory-service/src/main/java/com/ecommerce/inventory/service/impl/InventoryServiceImpl.java`:32-32

**Repository evidence:**

- Repository path: `source/inventory-service/src/main/java/com/ecommerce/inventory/service/impl/InventoryServiceImpl.java`
- Symbol: `InventoryServiceImpl.list`
- Source fingerprint: `sha256:fa3fa59291d9...`
- Assessment snapshot: Workspace snapshot `inventory-service-workspace-2026-09-18`
- Original assessed lines (advisory): 32-32

**Original source requiring update:**

```java
    @Override public List<InventoryResponse> list() { return repository.findAll().stream().map(mapper::toResponse).toList(); }
```

The controller method that exposes this operation is recorded in the repository inventory with an advisory line range and carries no assessed excerpt, so no source excerpt is reproduced for it.

**Fix:**

**Proposed change: Bounded list operation** — `source/inventory-service/src/main/java/com/ecommerce/inventory/service/impl/InventoryServiceImpl.java`

Illustrative proposal only.

```java
@Override
public Page<InventoryResponse> list(Pageable pageable) {
    return repository.findAll(pageable).map(mapper::toResponse);
}
```

The paged repository read is already available on the existing repository interface, so no repository change is needed. The page mapping applies the existing mapper, so the element shape is unchanged. Peak allocation becomes a function of the page size rather than of the table size. The service interface method changes signature accordingly.

**Proposed change: Page size bounds and controller binding** — `source/inventory-service/src/main/resources/application.yml`

Illustrative proposal only.

```yaml
spring:
  data:
    web:
      pageable:
        default-page-size: ${INVENTORY_PAGE_SIZE_DEFAULT}
        max-page-size: ${INVENTORY_PAGE_SIZE_MAX}
        one-indexed-parameters: false
```

Spring Data web support caps the requested page size at the configured maximum, so a caller cannot defeat the bound by asking for a very large page. Both values are externalized. The corresponding controller signature change from a bare list to a page is the approval-gated part of this change and is not applied until the contract owner approves the response shape.

**Validation requirements:** Validation requires repository evidence that no production path reads the inventory table without a page bound, that a request returns at most the configured maximum page size regardless of what is requested, and that both page-size values are externally overridable.

**Dependencies:** None.

**Approval gate:** Changing what the public inventory list endpoint returns to callers, either a paged envelope or a result set capped at a maximum size, is a customer-visible behaviour change that requires approval from the API contract owner before implementation.

**Notes:**

- Implementation: The paged service operation can be added alongside the existing one so the bound is introduced without removing any caller-visible behaviour.
- Validation: Closure requires repository evidence that peak allocation for a list request is bounded by the page size rather than by the table size.
- Guardrail: Default and maximum page sizes must remain deployment-supplied inputs and must not be hardcoded, and the caller-visible response shape must not change ahead of contract approval.

<span style="font-size: 14px;">**Standards reference:** jvm-runtime-resiliency v1.0.0 — `grounding/dependencies/jvm-runtime-resiliency.md`</span>

---

### Priority P2

<h3 style="color:#0F6CBD;">
Cross-Store Consistency and Event Identity
</h3>

<!-- finding:F-002 -->
#### P2-001: Event publication occurs inside the database transaction with no outbox or commit coordination

**Priority: P2 - Medium risk**

**Priority policy:** AA-REMEDIATION-PRIORITY version 1.0.0

**Severity:** critical

**Resiliency Related:** Yes

**Finding status:** Verified finding

**Issue:** The save-and-publish helper performs the repository save and then the producer publish inside the same transactional service method, so the Kafka send is issued before the database transaction commits. The delete operation removes the entity and publishes the deletion event in that same transaction. No transactional outbox table, transactional event listener, or after-commit hook exists anywhere in production source. The database write and the event publication therefore share no common commit point.

**What does this solve:** A rollback after a send can no longer leave downstream consumers holding state that was never committed. A commit failure after an in-flight send becomes represented by a durable intent record rather than by nothing at all. The Azure SQL write and the inventory event publication gain a common commit point that recovery can inspect.

**Resiliency Impact:** The Azure SQL write and the Kafka publication can diverge in both directions. If the transaction rolls back after the send, downstream consumers receive an event describing inventory state that was never committed. If the broker is reachable but the commit fails, the event is already in flight. There is no durable intent record, terminal status, or reconciliation marker that would let recovery detect or repair the divergence, which is precisely the state that must be rebuilt after an active-standby regional promotion.

**Recommended Fix:** Write an outbox record inside the business transaction instead of sending directly from the service. Run a relay that reads unpublished outbox records, publishes them through the durable producer introduced by P1-001, and marks them published only after a confirmed delivery outcome. Give each outbox record a terminal status and an attempt count so recovery can detect and repair divergence. Keep the outbox table in the Azure SQL authoritative store the approved architecture already declares, so no new datastore is introduced.

**File:** `source/inventory-service/src/main/java/com/ecommerce/inventory/service/impl/InventoryServiceImpl.java`:51-51

**Repository evidence:**

- Repository path: `source/inventory-service/src/main/java/com/ecommerce/inventory/service/impl/InventoryServiceImpl.java`
- Symbol: `InventoryServiceImpl.saveAndPublish`
- Source fingerprint: `sha256:2f208c196a95...`
- Assessment snapshot: Workspace snapshot `inventory-service-workspace-2026-09-18`
- Original assessed lines (advisory): 51-51

**Original source requiring update:**

```java
    private InventoryResponse saveAndPublish(InventoryItem item, String type, String referenceId) { InventoryResponse response = mapper.toResponse(repository.save(item)); producer.publish(type, response, referenceId); return response; }
```

**File:** `source/inventory-service/src/main/java/com/ecommerce/inventory/service/impl/InventoryServiceImpl.java`:35-36

**Repository evidence:**

- Repository path: `source/inventory-service/src/main/java/com/ecommerce/inventory/service/impl/InventoryServiceImpl.java`
- Symbol: `InventoryServiceImpl.delete`
- Source fingerprint: `sha256:5b17867aea81...`
- Assessment snapshot: Workspace snapshot `inventory-service-workspace-2026-09-18`
- Original assessed lines (advisory): 35-36

**Original source requiring update:**

```java
    @Override @Transactional @CacheEvict(cacheNames = "inventory", key = "#id")
    public void delete(Long id) { InventoryItem item = find(id); repository.delete(item); producer.publish("INVENTORY_DELETED", mapper.toResponse(item), ""); }
```

No outbox table, outbox repository, or relay component exists in the assessed source, so no source excerpt is reproduced for those targets.

**Fix:**

**Proposed change: Outbox record entity** — `source/inventory-service/src/main/java/com/ecommerce/inventory/outbox/OutboxRecord.java`

Illustrative proposal only.

```java
package com.ecommerce.inventory.outbox;

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.EnumType;
import jakarta.persistence.Enumerated;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import jakarta.persistence.Lob;
import jakarta.persistence.Table;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.time.Instant;

@Entity
@Table(name = "inventory_event_outbox")
@Data @Builder @NoArgsConstructor @AllArgsConstructor
public class OutboxRecord {

    public enum Status { PENDING, PUBLISHED, FAILED }

    @Id @GeneratedValue(strategy = GenerationType.IDENTITY) private Long id;
    @Column(nullable = false, length = 64) private String eventType;
    @Column(nullable = false, length = 255) private String aggregateKey;
    @Column(nullable = false, length = 255) private String referenceId;
    @Lob @Column(nullable = false) private String payload;
    @Enumerated(EnumType.STRING) @Column(nullable = false, length = 16) private Status status;
    @Column(nullable = false) private int attemptCount;
    @Column(nullable = false) private Instant createdAt;
    private Instant publishedAt;
    private String lastError;
}
```

The entity follows the same Lombok and JPA conventions as InventoryItem and ProcessedOperation. It records the durable intent, the aggregate key that becomes the Kafka record key, an explicit terminal status, and an attempt count, which together give recovery a queryable basis for detecting and repairing divergence. lastError holds the exception class and message so a stuck record can be diagnosed without correlating logs.

**Proposed change: Outbox repository** — `source/inventory-service/src/main/java/com/ecommerce/inventory/outbox/OutboxRepository.java`

Illustrative proposal only.

```java
package com.ecommerce.inventory.outbox;

import org.springframework.data.domain.Limit;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.List;

public interface OutboxRepository extends JpaRepository<OutboxRecord, Long> {
    List<OutboxRecord> findByStatusOrderByCreatedAtAsc(OutboxRecord.Status status, Limit limit);
}
```

A derived query in the same style as the existing findByProductId method. Ordering by creation time preserves per-aggregate publication order, and the Limit bounds each relay batch so a large backlog cannot be materialized in one read.

**Proposed change: Commit-ordered relay** — `source/inventory-service/src/main/java/com/ecommerce/inventory/outbox/OutboxRelay.java`

Illustrative proposal only.

```java
package com.ecommerce.inventory.outbox;

import com.ecommerce.inventory.observability.InventoryTelemetry;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.boot.autoconfigure.condition.ConditionalOnProperty;
import org.springframework.data.domain.Limit;
import org.springframework.kafka.core.KafkaTemplate;
import org.springframework.scheduling.annotation.Scheduled;
import org.springframework.stereotype.Component;
import org.springframework.transaction.annotation.Transactional;

import java.time.Instant;
import java.util.List;

@Slf4j
@Component
@ConditionalOnProperty(name = "app.outbox.relay.enabled", havingValue = "true")
public class OutboxRelay {

    private final OutboxRepository outbox;
    private final KafkaTemplate<String, Object> kafkaTemplate;
    private final InventoryTelemetry telemetry;
    private final String topic;
    private final int batchSize;
    private final int maxAttempts;

    public OutboxRelay(OutboxRepository outbox,
                       KafkaTemplate<String, Object> kafkaTemplate,
                       InventoryTelemetry telemetry,
                       @Value("${app.outbox.topic:inventory-events}") String topic,
                       @Value("${app.outbox.relay.batch-size}") int batchSize,
                       @Value("${app.outbox.relay.max-attempts}") int maxAttempts) {
        this.outbox = outbox;
        this.kafkaTemplate = kafkaTemplate;
        this.telemetry = telemetry;
        this.topic = topic;
        this.batchSize = batchSize;
        this.maxAttempts = maxAttempts;
    }

    @Scheduled(fixedDelayString = "${app.outbox.relay.poll-interval}")
    @Transactional
    public void publishPending() {
        List<OutboxRecord> pending =
                outbox.findByStatusOrderByCreatedAtAsc(OutboxRecord.Status.PENDING, Limit.of(batchSize));

        for (OutboxRecord record : pending) {
            try {
                kafkaTemplate.send(topic, record.getAggregateKey(), record.getPayload()).join();
                record.setStatus(OutboxRecord.Status.PUBLISHED);
                record.setPublishedAt(Instant.now());
                telemetry.recordPublication(record.getEventType(), InventoryTelemetry.OUTCOME_SUCCESS);
            } catch (RuntimeException failure) {
                record.setAttemptCount(record.getAttemptCount() + 1);
                record.setLastError(failure.getClass().getName());
                if (record.getAttemptCount() >= maxAttempts) {
                    record.setStatus(OutboxRecord.Status.FAILED);
                }
                telemetry.recordPublication(record.getEventType(), InventoryTelemetry.OUTCOME_FAILURE);
                log.error("outbox publication failed outboxId={} attempt={} exception={}",
                        record.getId(), record.getAttemptCount(), failure.getClass().getName(), failure);
            }
        }
    }
}
```

The relay runs outside any business transaction and marks a record published only after the send completes, so a rolled-back business transaction leaves no record to publish and a publication failure leaves the record recoverable. Exhausting the attempt budget moves the record to an explicit FAILED status rather than silently dropping it. The relay is conditional on an externalized property so its regional activation follows the same contract as the listener in P0-002, which is what keeps a single region publishing under the approved single-active model.

**Proposed change: Outbox migration script** — `source/inventory-service/src/main/resources/db/migration/V3__outbox.sql`

Illustrative proposal only.

```sql
CREATE TABLE inventory_event_outbox (
    id           BIGINT IDENTITY(1,1) NOT NULL,
    eventType    VARCHAR(64)          NOT NULL,
    aggregateKey VARCHAR(255)         NOT NULL,
    referenceId  VARCHAR(255)         NOT NULL,
    payload      NVARCHAR(MAX)        NOT NULL,
    status       VARCHAR(16)          NOT NULL,
    attemptCount INT                  NOT NULL CONSTRAINT DF_outbox_attemptCount DEFAULT 0,
    createdAt    DATETIME2            NOT NULL,
    publishedAt  DATETIME2            NULL,
    lastError    VARCHAR(512)         NULL,
    CONSTRAINT PK_inventory_event_outbox PRIMARY KEY (id)
);

CREATE INDEX IX_outbox_status_createdAt ON inventory_event_outbox (status, createdAt);
```

The composite index on status and creation time supports the relay query directly, so a large published backlog does not slow the scan for pending records. The table lives in the Azure SQL authoritative store the approved architecture already declares, so no new datastore is introduced.

**Validation requirements:** Validation requires repository evidence that no production path sends to Kafka inside an active business transaction, that an outbox record is written in the same transaction as the business state change it describes and is marked published only after a confirmed delivery outcome, and that a record exhausting its attempt budget reaches an explicit terminal status.

**Dependencies:** Depends on P0-006 and P1-001.

**Approval gate:** Moving event publication to after the database commit changes when downstream consumers see inventory events and allows the same event to be delivered more than once, so the architecture owner and the inventory event contract owner must approve the delivery semantics before implementation.

**Notes:**

- Implementation: The outbox entity, repository, and migration script introduce no externally observable behaviour on their own and can be added ahead of the publication timing change.
- Validation: Closure requires repository evidence that a rolled-back transaction leaves no outbox record and produces no published event.
- Guardrail: Relay enablement must remain an externalized property following the same regional activation contract as the consumer, and a retention and purge policy for published and failed outbox records must be approved before the table is introduced.
- Priority: Governed priority is assigned by the remediation policy from the nature of the remediation rather than inherited from the finding severity, and this change was evaluated for elevation and not elevated.

<span style="font-size: 14px;">**Standards reference:** springboot-aks-active-active-master v4.0.0 — `grounding/master/springboot-aks-active-active-master.md`</span>

---

<!-- finding:F-007 -->
#### P2-002: Published events carry no stable identity or correlation context

**Priority: P2 - Medium risk**

**Priority policy:** AA-REMEDIATION-PRIORITY version 1.0.0

**Severity:** high

**Resiliency Related:** Yes

**Finding status:** Verified finding

**Issue:** The published payload contains only the event type, a publication timestamp, a reference identifier, and the inventory response. No message identifier, event identifier, schema version, producing region, or trace context is present, and no record header is written. The publication timestamp is regenerated on every call, so a re-published event for the same business operation is not recognizable as the same event. No correlation identifier is persisted alongside the Azure SQL write or propagated from the consumed order event to the published inventory event.

**What does this solve:** Replay after a promotion and republication from the outbox become safe for downstream consumers to deduplicate. Cross-boundary incident correlation becomes possible, because a consumed order event, its resulting SQL state change, and its published inventory event carry a shared identifier.

**Resiliency Impact:** Downstream consumers have no basis on which to deduplicate, which means every remediation that relies on republication or replay after a regional promotion propagates duplicates outward. During an incident there is no identifier that connects a consumed order event, the resulting SQL state change, and the published inventory event, so the divergence introduced by P1-001 and P2-001 cannot be traced or reconciled.

**Recommended Fix:** Carry a deterministic event identifier derived from the same stable operation identity introduced by P0-001, an explicit schema version, the producing region from P0-007, and a correlation identifier propagated from the consumed order event. Write the same values as Kafka record headers so a consumer can deduplicate without deserializing the payload. Derive the event timestamp from the business state change rather than from the publication attempt, which is what keeps the identifier stable across republication.

**File:** `source/inventory-service/src/main/java/com/ecommerce/inventory/kafka/producer/InventoryEventProducer.java`:15-15

**Repository evidence:**

- Repository path: `source/inventory-service/src/main/java/com/ecommerce/inventory/kafka/producer/InventoryEventProducer.java`
- Symbol: `InventoryEventProducer.publish event envelope`
- Source fingerprint: `sha256:03e52ea3ceb6...`
- Assessment snapshot: Workspace snapshot `inventory-service-workspace-2026-09-18`
- Original assessed lines (advisory): 15-15

**Original source requiring update:**

```java
        kafkaTemplate.send("inventory-events", inventory.productId(), Map.of("type", type, "occurredAt", Instant.now().toString(), "referenceId", referenceId == null ? "" : referenceId, "inventory", inventory));
```

**Fix:**

**Proposed change: Event envelope with stable identity** — `source/inventory-service/src/main/java/com/ecommerce/inventory/kafka/producer/InventoryEventEnvelope.java`

Illustrative proposal only.

```java
package com.ecommerce.inventory.kafka.producer;

import com.ecommerce.inventory.dto.InventoryResponse;

import java.time.Instant;

public record InventoryEventEnvelope(
        String eventId,
        String type,
        String schemaVersion,
        String region,
        String correlationId,
        String referenceId,
        Instant occurredAt,
        InventoryResponse inventory) {

    public static String eventId(String type, String productId, String referenceId) {
        return type + ':' + productId + ':' + referenceId;
    }
}
```

The envelope preserves the four fields the current payload carries and adds the identity, schema version, region, and correlation dimensions. eventId is derived from the same components as the operation identity in P0-001, so republication of the same business operation produces an identical identifier and a downstream consumer can deduplicate. occurredAt becomes a supplied business timestamp rather than a per-attempt Instant.now, which is what makes the identifier stable across republication. The record shape follows the existing DTO convention in this repository.

**Proposed change: Identity headers and correlation propagation** — `source/inventory-service/src/main/java/com/ecommerce/inventory/kafka/producer/InventoryEventProducer.java`

Illustrative proposal only.

```java
public void publish(String type, InventoryResponse inventory, String referenceId, String correlationId) {
    String safeReference = referenceId == null ? "" : referenceId;
    String eventId = InventoryEventEnvelope.eventId(type, inventory.productId(), safeReference);

    InventoryEventEnvelope envelope = new InventoryEventEnvelope(
            eventId, type, schemaVersion, deploymentIdentity.getRegion(),
            correlationId, safeReference, inventory.updatedAt(), inventory);

    ProducerRecord<String, Object> record =
            new ProducerRecord<>(TOPIC, inventory.productId(), envelope);
    record.headers()
            .add(new RecordHeader("eventId", eventId.getBytes(StandardCharsets.UTF_8)))
            .add(new RecordHeader("schemaVersion", schemaVersion.getBytes(StandardCharsets.UTF_8)))
            .add(new RecordHeader("region", deploymentIdentity.getRegion().getBytes(StandardCharsets.UTF_8)))
            .add(new RecordHeader("correlationId", correlationId.getBytes(StandardCharsets.UTF_8)));

    kafkaTemplate.send(record).whenComplete(this::recordOutcome);
}
```

Identity values are written both as envelope fields and as record headers, so a consumer can deduplicate without deserializing the payload. occurredAt is taken from the item updatedAt value the service already sets on every mutation, which makes it a business timestamp rather than a publication timestamp. The region comes from the DeploymentIdentityProperties bean introduced in P0-007. The topic name and the record key remain productId, exactly as assessed. No customer, credential, or payment field is added.

**Validation requirements:** Validation requires repository evidence that every published event carries a deterministic identifier that is identical across republication of the same business operation, that the identifier, schema version, producing region, and correlation identifier are present both as envelope fields and as record headers, and that no customer, credential, payment, or secret value is added to the envelope or to any header.

**Dependencies:** Depends on P0-001, P0-007, and P1-001.

**Approval gate:** Adding identity, schema version, region, and correlation fields to the published inventory event payload and to its record headers changes what every downstream consumer receives, so the inventory event contract owner must approve the envelope shape before implementation.

**Notes:**

- Implementation: Propagating a correlation identifier from the consumed event through the service to logs and metrics changes no external contract and can proceed independently of the envelope change.
- Validation: Closure requires repository evidence that the event timestamp reflects the business state change and does not change between republication attempts.
- Guardrail: The schema version must remain an externalized property, and the envelope must carry no customer, credential, payment, or secret value in any field or header.
- Priority: Governed priority is assigned by the remediation policy from the nature of the remediation rather than inherited from the finding severity, and this change was evaluated for elevation and not elevated.

<span style="font-size: 14px;">**Standards reference:** springboot-aks-active-active-master v4.0.0 — `grounding/master/springboot-aks-active-active-master.md`</span>

---

<!-- content:resiliency-recommendations:end -->

[Back to Top](#top)

<!-- section:non-resiliency-recommendations -->
## Non-Resiliency-Focused Recommendations

<!-- content:non-resiliency-recommendations:start -->
The findings in this section are evidence-backed violations of applicable controls whose impact occurs during entirely normal operation, with no dependency failure, regional transition, or recovery event involved. They are preserved as findings rather than downgraded to observations because each one is supported by repository evidence, an applicable control, and a defensible risk statement. Each carries a governed remediation priority assigned by the same prioritization policy that governs resiliency findings, and each is subject to the same implementation and closure obligations.

### Priority P1

<h3 style="color:#0F6CBD;">
Cache Contract and Compatibility
</h3>

<!-- finding:F-018 -->
#### P1-013: Cache keys have no namespace, environment scope, or schema version

**Priority: P1 - High risk**

**Priority policy:** AA-REMEDIATION-PRIORITY version 1.0.0

**Severity:** high

**Resiliency Related:** No

**Finding status:** Verified finding

**Issue:** The only cache name is inventory and the key expression is the raw entity identifier. No key prefix, environment qualifier, tenant qualifier, or payload schema version is configured. Keys therefore resolve to the framework default cache-name prefix followed by the numeric identifier, which is the same value in every deployment of the service.

**What does this solve:** Cache keys become scoped to a specific application, environment, and payload generation. Two deployments that share a Redis instance or database index write to disjoint key spaces. A response-model change can invalidate a generation of cached values by moving to a new key space instead of flushing the shared instance.

**Impact:** Any two deployments that share a Redis instance or database index, for example a non-production and a production deployment or two application versions during a rolling release, write to identical keys. A cached value produced by one payload shape is then read by code expecting a different shape, which yields incorrect data or a deserialization failure depending on the shapes involved. There is no mechanism to retire a generation of cached values other than flushing the shared instance, which discards every unrelated key at the same time.

**Recommended Fix:** Compose the cache key prefix from externalized application, environment, and cache schema version qualifiers so that every key is scoped to a specific deployment and payload generation. Keep the cache name and the key expression on the cached read unchanged so no caller behaviour changes. Whether a Redis instance or database index is actually shared between environments is deployment configuration and remains outside the change boundary.

**Remediated with:** P1-012, P1-017

**File:** `source/inventory-service/src/main/java/com/ecommerce/inventory/service/impl/InventoryServiceImpl.java`:30-31

**Repository evidence:**

- Repository path: `source/inventory-service/src/main/java/com/ecommerce/inventory/service/impl/InventoryServiceImpl.java`
- Symbol: `InventoryServiceImpl.get @Cacheable`
- Source fingerprint: `sha256:af81ef398962...`
- Assessment snapshot: Workspace snapshot `inventory-service-workspace-2026-09-18`
- Original assessed lines (advisory): 30-31

**Original source requiring update:**

```java
    @Override @Cacheable(cacheNames = "inventory", key = "#id")
    public InventoryResponse get(Long id) { return mapper.toResponse(find(id)); }
```

**Fix:**

Illustrative proposal only.

```java
            .computePrefixWith(cacheName -> keyPrefix + ':' + schemaVersion + ':' + cacheName + "::")
```

The computed prefix puts an externalized application and environment prefix and a cache schema version in front of every key, so two deployments sharing a Redis instance and two application versions during a rolling release write to disjoint key spaces. The complete cache manager contract that carries this prefix computation is shown under P1-012.

**Validation requirements:** Validation requires repository evidence that every cache key is prefixed with the application, environment, and cache schema version qualifiers, and that changing the schema version produces a disjoint key space with no reuse of previously cached values.

**Dependencies:** None.

**Notes:**

- Implementation: The prefix is applied by the same cache configuration bean that establishes the value serializer and the entry expiry, so this finding is implemented as part of that single bean rather than as a separate change.
- Validation: Closure requires repository evidence that no key is written without the application, environment, and schema version qualifiers.
- Guardrail: The environment qualifier must remain a deployment-supplied input and must not be hardcoded in the repository.

<span style="font-size: 14px;">**Standards reference:** springboot-azure-managed-redis v2.2.0 — `grounding/dependencies/springboot-azure-managed-redis.md`</span>

---

<!-- finding:F-029 -->
#### P1-017: Cached values rely on default JDK serialization but the cached type is not serializable

**Priority: P1 - High risk**

**Priority policy:** AA-REMEDIATION-PRIORITY version 1.0.0

**Severity:** high

**Resiliency Related:** No

**Finding status:** Verified finding

**Issue:** The cache type is set to redis and the cache configuration class supplies no Redis cache configuration and no value serialization pair, so the framework default value serializer applies. The cached type is a Java record that does not implement the serializable marker and declares no explicit serializer or type mapping. The value written by the cached read is therefore not serializable by the serializer that is actually in effect.

**What does this solve:** The cached read path writes and reads values through an explicit serializer bound to the cached type, independent of Java serialization. The read endpoint functions in every environment where the Redis cache is active rather than failing on every request.

**Impact:** The cache write raises a serialization failure on every cached read. Combined with the absence of a cache error handler covered under P1-011, that failure propagates to the caller and makes the read endpoint fail on every request in any environment where the Redis cache is active. The defect is invisible in the current test suite because no test exercises the cached read path against a real cache, so it surfaces first in a deployed environment rather than in the build.

**Recommended Fix:** Declare an explicit JSON value serializer bound to the cached response type so that cache serialization no longer depends on Java serialization or on the cached type implementing the serializable marker. Keep the cached response type and the REST response shape unchanged; the serializer applies to the cache only. Redis server configuration remains outside the change boundary.

**Remediated with:** P1-012, P1-013

**File:** `source/inventory-service/src/main/java/com/ecommerce/inventory/dto/InventoryResponse.java`:5-6

**Repository evidence:**

- Repository path: `source/inventory-service/src/main/java/com/ecommerce/inventory/dto/InventoryResponse.java`
- Symbol: `InventoryResponse`
- Source fingerprint: `sha256:cc90710b26c7...`
- Assessment snapshot: Workspace snapshot `inventory-service-workspace-2026-09-18`
- Original assessed lines (advisory): 5-6

**Original source requiring update:**

```java
public record InventoryResponse(Long id, String productId, int availableQuantity, int reservedQuantity, Instant updatedAt) {
}
```

**File:** `source/inventory-service/src/main/resources/application.yml`:16-17

**Repository evidence:**

- Repository path: `source/inventory-service/src/main/resources/application.yml`
- Symbol: `spring.cache.type`
- Source fingerprint: `sha256:5921b25eb1c9...`
- Assessment snapshot: Workspace snapshot `inventory-service-workspace-2026-09-18`
- Original assessed lines (advisory): 16-17

**Original source requiring update:**

```yaml
  cache:
    type: redis
```

**Fix:**

Illustrative proposal only.

```java
    ObjectMapper cacheMapper = objectMapper.copy().registerModule(new JavaTimeModule());
    Jackson2JsonRedisSerializer<InventoryResponse> valueSerializer =
            new Jackson2JsonRedisSerializer<>(cacheMapper, InventoryResponse.class);
```

An explicit Jackson serializer bound to the cached response type removes the dependency on JDK serialization, so the record no longer needs to implement the serializable marker, and the time module registration preserves the instant field carried by the response. The complete cache manager contract that binds this serializer to the cache is shown under P1-012.

**Validation requirements:** Validation requires repository evidence that the value serializer is declared explicitly, that it does not depend on Java serialization or on the cached type implementing the serializable marker, and that a cached read against a real Redis instance returns an equal response on the second call.

**Dependencies:** None.

**Notes:**

- Implementation: The serializer is declared by the same cache configuration bean that establishes the entry expiry and the key prefix, so this finding is implemented as part of that single bean rather than as a separate change.
- Validation: Closure requires repository evidence that the cached read path is exercised against a real cache rather than against a no-op cache manager.
- Guardrail: The REST response shape must not change; the serializer applies to the cache value only.

<span style="font-size: 14px;">**Standards reference:** springboot-azure-managed-redis v2.2.0 — `grounding/dependencies/springboot-azure-managed-redis.md`</span>

---

### Priority P2

<h3 style="color:#0F6CBD;">
Cache Correctness
</h3>

<!-- finding:F-020 -->
#### P2-003: Reserve and release mutate inventory without invalidating the cache

**Priority: P2 - Medium risk**

**Priority policy:** AA-REMEDIATION-PRIORITY version 1.0.0

**Severity:** critical

**Resiliency Related:** No

**Finding status:** Verified finding

**Issue:** Cache eviction is declared on update and delete, keyed by the entity identifier. Reserve and release locate the item by product identifier and change the available and reserved quantities, but carry no eviction of any kind. The cached entry keyed by the entity identifier is therefore left in place with the pre-adjustment quantities after every stock adjustment.

**What does this solve:** Every path that changes inventory quantities invalidates the cached representation of that item. The read endpoint returns post-adjustment quantities immediately after a reservation or release rather than continuing to serve the value captured before the adjustment.

**Impact:** Every stock reservation and release, including all reservations driven by order-events consumption, leaves a stale quantity in the cache. Because the entry has no expiry under P1-012, the stale value is served by the item read endpoint indefinitely until an unrelated update or delete happens to evict it. Callers relying on the read endpoint therefore observe availability that does not exist, which can drive over-reservation decisions upstream even though the authoritative record is re-read inside each reserve transaction.

**Recommended Fix:** Evict the cached entry for the affected item on the reserve and release paths using the entity identifier resolved inside the operation, so the identifier-keyed cache and the product-identifier-keyed mutation path stay aligned. Order the eviction after the transaction commits so a rolled-back adjustment does not discard a still-valid entry. Redis behaviour itself remains outside the change boundary.

**File:** `source/inventory-service/src/main/java/com/ecommerce/inventory/service/impl/InventoryServiceImpl.java`:33-36

**Repository evidence:**

- Repository path: `source/inventory-service/src/main/java/com/ecommerce/inventory/service/impl/InventoryServiceImpl.java`
- Symbol: `InventoryServiceImpl.update and InventoryServiceImpl.delete @CacheEvict`
- Source fingerprint: `sha256:ce19ccf64430...`
- Assessment snapshot: Workspace snapshot `inventory-service-workspace-2026-09-18`
- Original assessed lines (advisory): 33-36

**Original source requiring update:**

```java
    @Override @Transactional @CacheEvict(cacheNames = "inventory", key = "#id")
    public InventoryResponse update(Long id, InventoryRequest request) { InventoryItem item = find(id); mapper.update(request, item); item.setUpdatedAt(Instant.now()); return saveAndPublish(item, "INVENTORY_UPDATED", ""); }
    @Override @Transactional @CacheEvict(cacheNames = "inventory", key = "#id")
    public void delete(Long id) { InventoryItem item = find(id); repository.delete(item); producer.publish("INVENTORY_DELETED", mapper.toResponse(item), ""); }
```

**File:** `source/inventory-service/src/main/java/com/ecommerce/inventory/service/impl/InventoryServiceImpl.java`:37-50

**Repository evidence:**

- Repository path: `source/inventory-service/src/main/java/com/ecommerce/inventory/service/impl/InventoryServiceImpl.java`
- Symbol: `InventoryServiceImpl.reserve and InventoryServiceImpl.release`
- Source fingerprint: `sha256:0f2357c4e940...`
- Assessment snapshot: Workspace snapshot `inventory-service-workspace-2026-09-18`
- Original assessed lines (advisory): 37-50

**Original source requiring update:**

```java
    @Override @Transactional
    public InventoryResponse reserve(String productId, int quantity, String referenceId) {
        InventoryItem item = findByProduct(productId);
        if (item.getAvailableQuantity() < quantity) throw new IllegalArgumentException("Insufficient inventory for product: " + productId);
        item.setAvailableQuantity(item.getAvailableQuantity() - quantity); item.setReservedQuantity(item.getReservedQuantity() + quantity); item.setUpdatedAt(Instant.now());
        return saveAndPublish(item, "INVENTORY_RESERVED", referenceId);
    }
    @Override @Transactional
    public InventoryResponse release(String productId, int quantity, String referenceId) {
        InventoryItem item = findByProduct(productId);
        if (item.getReservedQuantity() < quantity) throw new IllegalArgumentException("Release exceeds reserved inventory for product: " + productId);
        item.setReservedQuantity(item.getReservedQuantity() - quantity); item.setAvailableQuantity(item.getAvailableQuantity() + quantity); item.setUpdatedAt(Instant.now());
        return saveAndPublish(item, "INVENTORY_RELEASED", referenceId);
    }
```

**Fix:**

Illustrative proposal only.

```java
private void evictAfterCommit(Long itemId) {
    if (!TransactionSynchronizationManager.isSynchronizationActive()) {
        cacheManager.getCache("inventory").evict(itemId);
        return;
    }
    TransactionSynchronizationManager.registerSynchronization(new TransactionSynchronization() {
        @Override
        public void afterCommit() {
            cacheManager.getCache("inventory").evict(itemId);
        }
    });
}
```

The reserve and release paths locate the item by product identifier but the cache is keyed by the entity identifier, so a declarative eviction keyed on a method parameter cannot express the correct key. Evicting by the resolved entity identifier inside the operation keeps the identifier-keyed cache and the product-identifier-keyed mutation path aligned. Registering the eviction after commit means a rolled-back adjustment does not discard a still-valid entry. An eviction failure is absorbed and counted by the cache error handler established under P1-011, and the existing eviction declarations on update and delete are left in place.

**Validation requirements:** Validation requires repository evidence that a successful reserve or release removes the cached entry for the affected item using the same key used by the cached read, and that a rolled-back adjustment leaves a valid cached entry in place.

**Dependencies:** Depends on P1-011 and P1-012.

**Notes:**

- Implementation: The eviction is added to the reserve and release paths only; the existing eviction declarations on update and delete and all business behaviour remain unchanged.
- Validation: Closure requires repository evidence that a read immediately following a successful reserve returns the post-adjustment quantities.
- Guardrail: An eviction that fails after commit must be absorbed and counted rather than propagated to the caller, and the entry expiry established under P1-012 must bound how long a surviving stale entry persists.
- Priority: Governed priority is assigned by the remediation policy from the nature of the remediation rather than inherited from the finding severity, and this change was evaluated for elevation and not elevated.

<span style="font-size: 14px;">**Standards reference:** springboot-azure-managed-redis v2.2.0 — `grounding/dependencies/springboot-azure-managed-redis.md`</span>

---

<!-- content:non-resiliency-recommendations:end -->

[Back to Top](#top)

<!-- section:evidence-gap-analysis -->
## Repository and IaC Evidence Gap Analysis

<!-- content:evidence-gap-analysis:start -->

Two assessment domains were enabled for this engagement: application code and application configuration. Container build, CI/CD pipeline, deployment configuration, infrastructure as code, and deployed infrastructure were disabled. This section records what the repository could and could not establish. Absence of infrastructure evidence is not reported as infrastructure noncompliance, and no finding in this report was created from a missing external fact.

### Available to review

| Repository-visible configuration                                     | Current evidence                                                                                                            | Application resiliency interpretation                                                                                    | Related findings         |
|----------------------------------------------------------------------|------------------------------------------------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------------------------------------|--------------------------|
| Datasource URL and credentials                                       | Supplied entirely through environment placeholders; no regional hostname, port, or server name appears in any profile         | The artifact is region-portable, but no repository-owned connect, query, or transaction deadline exists                     | P1-004, P1-007           |
| Kafka client configuration                                           | Bootstrap servers, consumer group, and security protocol are environment-supplied; no client timeout or backoff is declared   | Client failure detection, reconnect, and backoff fall to library defaults that the repository never bounds                  | P1-006, P1-001, P1-002   |
| Kafka listener declaration                                           | One listener with no identifier, no activation flag, and `auto-offset-reset` set to earliest                                  | Regional consumption cannot be enabled, disabled, or observed by configuration, and offset loss replays retained history     | P0-001, P0-002           |
| Redis connection configuration                                       | A single environment-supplied connection string with no region awareness and no declared connect or command timeout            | The cache client is single-endpoint from the application's perspective and its waits are unbounded                          | P1-005, P1-011           |
| Cache configuration                                                  | Caching is enabled with annotations only; no cache manager bean, TTL, key prefix, serializer, or error handler is declared     | Every cache behaviour that matters under load and failure is taken from framework defaults                                  | P1-011, P1-012, P1-013, P1-014, P1-017, P2-003 |
| Key Vault property source                                            | A mandatory configuration import with no optional prefix and no declared client budget                                        | Startup hard-depends on a remote secret store with no bounded failure path and no refresh contract                          | P0-005, P1-015           |
| Hibernate schema management                                          | `ddl-auto` applies schema changes in every profile including production                                                       | The application mutates its own authoritative schema at startup, which is unsafe when two regions start concurrently        | P0-006                   |
| Actuator and health configuration                                    | Exposure limited to health, info, and prometheus with health details defaulting to never; no readiness group membership declared | The management surface is minimized, but traffic eligibility does not reflect authoritative dependency health              | P0-003                   |
| Lifecycle configuration                                              | No graceful shutdown property, no shutdown phase ordering, and no readiness withdrawal hook                                    | Termination is a cut rather than a drained transition                                                                       | P0-004                   |
| Telemetry configuration and production code                          | Metrics and structured logs are emitted with no region or role dimension and no failure or business-outcome signal             | Regional behaviour cannot be distinguished in telemetry, so a failover test cannot be interpreted                           | P0-007, P0-008           |
| Web layer and exception handling                                     | A global exception handler maps business exceptions only; dependency failures reach the caller as an opaque server error       | Callers cannot distinguish a retryable dependency condition from a permanent business rejection                             | P1-008, P1-009           |
| List endpoint implementation                                         | The endpoint materializes the entire table into memory with no pagination or result bound                                      | Request-driven memory growth is unbounded and scales with data volume rather than with request size                         | P1-016                   |
| Existing test sources                                                | The suite guards on Docker availability and exercises functional behaviour only                                               | No repository test exercises dependency failure, promotion, replay, or probe transition                                     | P0-009                   |

### Not available or externally owned

| External evidence or configuration                                                      | Needed to validate                                                                                                     | Related findings or assumptions                                        |
|------------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------------------------------------|------------------------------------------------------------------------|
| Resolved database connection string per region and the approved failover-group listener name | Whether the application uses the read-write listener and can reconnect without a redeploy or connection-string change      | Supports the assumptions behind P1-004 and P1-007                       |
| Deployed Kafka cluster topology, Cluster Linking, and consumer-offset replication          | Promotion behaviour, mirror-topic state, and how much history a promoted region would replay                               | Supports the assumptions behind P0-001, P0-002, and P1-002              |
| How standby-region consumption is prevented today, if at all                              | The current operational urgency of the missing activation control, not its validity                                        | Affects urgency of P0-002; the finding itself is verified from the repository |
| Redis authentication mode and transport scheme inside the supplied connection string       | The correct client lifecycle for credential rotation and whether rotation requires a process restart                        | Blocks one target of P1-015                                             |
| Deployed Redis regional topology and geo-replication configuration                        | Cache behaviour and conflict handling during a regional event                                                              | Supports the assumptions behind P1-011                                  |
| JVM options, container entrypoint and signal forwarding, resource limits, probes, and termination grace | Heap strategy, container awareness, signal handling, probe timing, and the drain window the application must fit inside | Supports the assumptions behind P0-004 and P1-010                       |
| Gateway, mesh, and load balancer timeout and keep-alive budgets                           | Whether application deadlines are correctly ordered inside the end-to-end budget                                           | Required to select values for P1-004, P1-007, P1-009, and P1-010        |
| Ingress routing rules and management-port separation for the application port             | External reachability of management and API documentation endpoints                                                        | No finding; recorded as an evidence boundary only                       |
| Approved schema contract and registry expectation for the inventory and order event topics | The approved envelope, versioning scheme, and header vocabulary for published events                                       | Blocks approval of P2-002                                               |
| Architecture confirmation of whether API Management applies to this repository             | Whether an inbound-only capability expectation is correct, given that the service makes no outbound HTTP call               | No finding; recorded as an expectation without repository evidence      |
| Repository-owned Dockerfile, CI/CD workflow, and Kubernetes manifests                     | Container, pipeline, and deployment resiliency behaviour                                                                   | Present in the repository but deliberately out of assessment scope      |

### Repository-evidenced risks without an applicable control

Four repository-evidenced observations were recorded during evaluation for which no loaded standard contains an applicable control. A finding requires an applicable control, so none was created. Each is routed to standards governance for control-catalog coverage review.

- The Kafka client security protocol falls back to a plaintext transport when the environment value is unset, and no SASL or SSL configuration exists in the repository.
- Inbound event deserialization trusts all packages, which removes package-level type restriction on consumed payloads.
- No authentication or authorization is applied to any inventory endpoint, including the state-changing reserve, release, update, and delete operations.
- API documentation tooling is a compile-scope dependency and its user interface path is configured on the application port in all profiles.

### Scope exceptions carried forward

One citation correction was recorded during evaluation: an inventory line range overshot the assessed file by one line and was corrected, with the affected evidence re-anchored to the exact range and verified by fingerprint. Three scope exceptions were carried forward unchanged and are preserved as evidence boundaries rather than findings: disabled delivery domains, an inbound capability expectation with no outbound client to validate, and a service mesh expectation whose evidence lives in a disabled domain.

<!-- content:evidence-gap-analysis:end -->

[Back to Top](#top)

<!-- section:full-finding-matrix -->
## Full Finding Matrix

<!-- content:full-finding-matrix:start -->

All 29 findings are verified findings supported by exact repository evidence. No conditional findings, infrastructure findings, or excluded-platform findings were created. `Remediated with` names the other findings that share a single remediation change.

| ID     | Priority | Severity | Resiliency related | Status   | Category                                      | Finding                                                                                         | Remediated with  | Repository scope                          |
|--------|----------|----------|--------------------|----------|-----------------------------------------------|-------------------------------------------------------------------------------------------------|------------------|-------------------------------------------|
| P0-001 | P0       | critical | Yes                | Verified | Regional Ownership and Replay Safety          | Order-event consumption and stock adjustment are not idempotent                                   | —                | Kafka consumer and inventory service       |
| P0-002 | P0       | critical | Yes                | Verified | Regional Ownership and Replay Safety          | Kafka listener has no region-role activation control                                              | —                | Kafka consumer                             |
| P0-003 | P0       | critical | Yes                | Verified | Traffic Eligibility and Health                | Readiness and health configuration relies entirely on framework defaults                          | —                | Application configuration and health       |
| P0-004 | P0       | high     | Yes                | Verified | Startup and Termination Lifecycle             | No graceful shutdown, readiness withdrawal, or work draining                                      | —                | Application configuration and lifecycle    |
| P0-005 | P0       | critical | Yes                | Verified | Startup and Termination Lifecycle             | Startup depends on a mandatory Key Vault import with no bounded or optional contract               | —                | Application configuration                  |
| P0-006 | P0       | high     | Yes                | Verified | Startup and Termination Lifecycle             | Hibernate applies schema changes at startup in every profile                                       | —                | Application configuration and schema        |
| P0-007 | P0       | medium   | Yes                | Verified | Regional Failure Observability                | Telemetry carries no regional identity                                                             | —                | Application configuration and telemetry     |
| P0-008 | P0       | critical | Yes                | Verified | Regional Failure Observability                | Critical failures and business throughput produce no actionable signal                             | —                | Service, consumer, and producer paths       |
| P0-009 | P0       | critical | Yes                | Verified | Failure and Failover Verification             | Failure and failover behaviour is untested                                                         | —                | Test sources                                |
| P1-001 | P1       | critical | Yes                | Verified | Event Publication and Consumption Durability  | Kafka publication is fire-and-forget with no durability configuration                              | —                | Kafka producer and configuration            |
| P1-002 | P1       | critical | Yes                | Verified | Event Publication and Consumption Durability  | Consumer offsets advance past records that fail permanently                                        | P1-003           | Kafka consumer and configuration            |
| P1-003 | P1       | high     | Yes                | Verified | Event Publication and Consumption Durability  | Poison records have no dead-letter routing and payload extraction is unguarded                     | P1-002           | Kafka consumer                              |
| P1-004 | P1       | critical | Yes                | Verified | Bounded Dependency Deadlines                  | Azure SQL access has no bounded timeouts                                                           | P1-005, P1-006   | Application configuration and data access   |
| P1-005 | P1       | critical | Yes                | Verified | Bounded Dependency Deadlines                  | Redis access has no bounded connect or command timeouts                                            | P1-004, P1-006   | Application configuration                   |
| P1-006 | P1       | high     | Yes                | Verified | Bounded Dependency Deadlines                  | Kafka client timeouts, reconnect, and backoff are unbounded by repository configuration            | P1-004, P1-005   | Application configuration                   |
| P1-007 | P1       | critical | Yes                | Verified | Transient Failure Recovery and Conflict Handling | No bounded retry exists for transient Azure SQL failures                                        | —                | Service layer and build configuration       |
| P1-008 | P1       | high     | Yes                | Verified | Transient Failure Recovery and Conflict Handling | Optimistic-locking conflicts are neither detected, retried, nor mapped                          | —                | Service layer and web layer                 |
| P1-009 | P1       | high     | Yes                | Verified | Failure Semantics and Dependency Isolation    | Dependency failures have no stable caller-visible semantics                                        | —                | Web layer                                   |
| P1-010 | P1       | high     | Yes                | Verified | Failure Semantics and Dependency Isolation    | No isolation exists between request threads and blocking dependencies                              | —                | Service layer and configuration             |
| P1-011 | P1       | critical | Yes                | Verified | Cache Behaviour Under Load and Failure        | Redis cache failures propagate into the request path with no error handler                         | —                | Cache configuration                         |
| P1-012 | P1       | high     | Yes                | Verified | Cache Behaviour Under Load and Failure        | Cached entries have no TTL or expiration policy                                                    | P1-013, P1-017   | Cache configuration                         |
| P1-013 | P1       | high     | No                 | Verified | Cache Contract and Compatibility              | Cache keys have no namespace, environment scope, or schema version                                 | P1-012, P1-017   | Cache configuration                         |
| P1-014 | P1       | high     | Yes                | Verified | Cache Behaviour Under Load and Failure        | Concurrent cache misses are not coalesced                                                          | —                | Cache configuration                         |
| P1-015 | P1       | high     | Yes                | Verified | Credential Rotation                           | Secrets are bound once at startup with no refresh or rotation handling                             | —                | Application configuration and secrets        |
| P1-016 | P1       | high     | Yes                | Verified | Request Resource Bounding                     | The list endpoint loads the entire inventory table into memory                                     | —                | Service layer and web layer                 |
| P1-017 | P1       | high     | No                 | Verified | Cache Contract and Compatibility              | Cached values rely on default JDK serialization but the cached type is not serializable            | P1-012, P1-013   | Cache configuration and model               |
| P2-001 | P2       | critical | Yes                | Verified | Cross-Store Consistency and Event Identity    | Event publication occurs inside the database transaction with no outbox or commit coordination     | —                | Service layer and persistence               |
| P2-002 | P2       | high     | Yes                | Verified | Cross-Store Consistency and Event Identity    | Published events carry no stable identity or correlation context                                   | —                | Kafka producer and service layer            |
| P2-003 | P2       | critical | No                 | Verified | Cache Correctness                             | Reserve and release mutate inventory without invalidating the cache                                | —                | Service layer and cache annotations         |

Counts reconcile with the Summary Findings table: 9 findings at P0, 17 at P1, and 3 at P2, of which 26 are resiliency findings and 3 are non-resiliency findings. Severity distribution is 14 critical, 14 high, and 1 medium.

<!-- content:full-finding-matrix:end -->

[Back to Top](#top)

<!-- section:standards-alignment -->
## Standards Alignment

<!-- content:standards-alignment:start -->

Eight standards were loaded for this assessment: the master application behaviour standard, six dependency standards resolved from confirmed repository dependencies, and one platform exclusion standard. No substitute standard was loaded for any disabled assessment domain. Control areas are named descriptively in this section; individual control identifiers are resolved in Appendix A.

| Standard or pattern                                              | Assessment status                                                                        | Related controls                                                                                                           | Related findings                                                                                     |
|-------------------------------------------------------------------|-------------------------------------------------------------------------------------------|-----------------------------------------------------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------|
| Spring Boot on AKS active-active application behaviour, v4.0.0   | 86 controls evaluated: 15 compliant, 27 non-compliant, 2 not assessed, 42 not applicable  | Regional traffic eligibility, readiness and health groups, idempotent business operations, event consumption and publication ownership, lifecycle and termination, regional telemetry, web failure semantics, dependency isolation, failure testing | P0-001, P0-002, P0-003, P0-004, P0-006, P0-007, P0-008, P0-009, P1-001, P1-002, P1-003, P1-009, P1-010, P2-001, P2-002 |
| Spring Boot with Azure SQL, v2.3.0                              | 16 controls evaluated: 2 compliant, 8 non-compliant, 0 not assessed, 6 not applicable     | Connection and query deadlines, transient failure retry, optimistic concurrency handling, failover-aware connectivity          | P1-004, P1-007, P1-008                                                                               |
| Spring Boot with Confluent Kafka, v3.1.0                        | 27 controls evaluated: 2 compliant, 18 non-compliant, 1 not assessed, 6 not applicable    | Client deadline and backoff configuration, producer durability, consumer acknowledgement and error handling, active-standby scenario controls | P1-006                                                                                               |
| Spring Boot with Azure Managed Redis, v2.2.0                    | 27 controls evaluated: 6 compliant, 12 non-compliant, 2 not assessed, 7 not applicable    | Client deadlines, cache error containment, expiration policy, key namespacing, value serialization, cache invalidation on mutation, request coalescing | P1-005, P1-011, P1-012, P1-013, P1-014, P1-017, P2-003                                               |
| Spring Boot with Azure Key Vault, v2.2.0                        | 14 controls evaluated: 5 compliant, 7 non-compliant, 0 not assessed, 2 not applicable     | Bounded startup dependency, optional property source contract, secret refresh and rotation handling, secret logging safety      | P0-005, P1-015                                                                                       |
| JVM runtime resiliency, v1.0.0                                  | 22 controls evaluated: 2 compliant, 6 non-compliant, 9 not assessed, 5 not applicable     | Request-driven memory bounding, heap strategy, container awareness, lifecycle signal handling                                  | P1-016                                                                                               |
| Application Gateway and global load balancing, v2.2.0           | 18 controls evaluated: 4 compliant, 7 non-compliant, 3 not assessed, 4 not applicable     | Probe semantics, stateless request handling, end-to-end timeout ordering, management endpoint separation                        | No separate findings; non-compliant controls in this standard were consolidated by root cause into findings recorded under the master and dependency standards |
| Excluded legacy platform assessment standard, v1.0.0            | Applied as suppress-all; 0 platform references found in the repository                    | Not applicable                                                                                                                | None                                                                                                 |

Three governance policies shaped the outcome without contributing controls. The Kafka operating-scenario policy validated the supplied active-standby scenario as consistent with the authoritative database model. The remediation prioritization policy assigned every governed priority. The resiliency finding qualification policy separated the 26 resiliency findings from the 3 non-resiliency findings and required that both classes be preserved.

The approved reference architectures listed in the Assessment Overview describe intended design for the shared services this repository consumes. They were not used as repository source evidence for any finding.

<!-- content:standards-alignment:end -->

[Back to Top](#top)

<!-- section:implementation-roadmap -->
## Implementation Roadmap

<!-- content:implementation-roadmap:start -->

The authoritative remediation plan converts the 29 findings into 24 root-cause changes across four dependency-ordered waves. Five findings are consolidated under another finding's change because they share one implementation surface. No finding was dropped, reclassified, or reprioritized by severity.

### Priority summary

| Priority | Change count | Primary objective                                                                                                          | Release gate                                                      |
|----------|--------------|-----------------------------------------------------------------------------------------------------------------------------|-------------------------------------------------------------------|
| P0       | 9            | Make regional ownership, replay safety, traffic eligibility, lifecycle transitions, and regional failure observability real   | Required before any multi-region cutover                          |
| P1       | 12           | Install bounded deadlines, transient failure recovery, dependency isolation, cache containment, and event durability          | Required before sustained multi-region operation                   |
| P2       | 3            | Adopt cross-store consistency and event identity patterns and correct cache invalidation                                      | Scheduled once the multi-region operating model is stable          |
| P3       | 0            | None recorded                                                                                                                 | Not applicable                                                     |

Governed priority is assigned by remediation policy and is never derived from severity. Three outcomes diverge deliberately. P0-007 carries medium severity but its change is P0, because without a region dimension on telemetry a regional failure test cannot be interpreted and a both-active condition cannot be confirmed or refuted. P2-001 and P2-003 carry critical severity but their changes are P2, because the transactional outbox is a governed architectural adoption and the cache invalidation gap is a normal-operation correctness defect. Seven candidates were evaluated for elevation to P0 and none were elevated.

### Implementation waves

| Wave | Findings addressed                                                                                                                                 | Prerequisites                                                                                  | Validation focus                                                                                                                                              |
|------|-----------------------------------------------------------------------------------------------------------------------------------------------------|------------------------------------------------------------------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 1    | P0-003, P0-004, P0-005, P0-006, P0-007, P0-008                                                                                                       | Plan approval                                                                                   | Readiness reflects authoritative dependency health while liveness does not, startup applies no schema change and is bounded, shutdown withdraws and drains, every metric and log record carries region and role |
| 2    | P0-001, P0-002                                                                                                                                        | Wave 1 exit criteria met                                                                        | A repeated order event produces exactly one stock movement, and consumption can be disabled and enabled by configuration with an observable state               |
| 3    | P1-001, P1-002, P1-003, P1-004, P1-005, P1-006, P1-007, P1-008, P1-009, P1-010, P1-011, P1-012, P1-013, P1-014, P1-015, P1-016, P1-017                 | Wave 2 exit criteria met; approved resiliency library version source confirmed                  | Every remote call carries a bounded externalized deadline, transient database transitions are survivable, a degraded dependency does not remove the pod from service, cache reads expire and are namespaced, publication outcome is observed and poison records are quarantined |
| 4    | P0-009, P2-001, P2-002, P2-003                                                                                                                        | Wave 3 exit criteria met; architecture and event-contract owner approval                        | No publication occurs for a rolled-back transaction, republication carries identical event identity, reserve and release evict the cached entry, and the regression suite passes |

Wave placement is a dependency statement rather than a priority statement. P0-009 is a P0 finding in Wave 4 because the consolidated regression suite depends on every other change; each change still carries its own tests in its own wave.

### Remediation index

| Display ID | Priority | Objective                                                                     | Complexity | Wave | Remediated with  |
|------------|----------|--------------------------------------------------------------------------------|------------|------|------------------|
| P0-001     | P0       | Make order-event consumption and stock adjustment idempotent                    | high       | 2    | —                |
| P0-002     | P0       | Give the Kafka listener an externalized region-role activation contract         | high       | 2    | —                |
| P0-003     | P0       | Make regional traffic eligibility reflect authoritative dependency health       | medium     | 1    | —                |
| P0-004     | P0       | Add graceful shutdown, readiness withdrawal, and work draining                  | medium     | 1    | —                |
| P0-005     | P0       | Bound the Key Vault startup dependency                                          | medium     | 1    | —                |
| P0-006     | P0       | Replace runtime schema changes with a versioned, gated migration contract       | medium     | 1    | —                |
| P0-007     | P0       | Attach regional identity to every metric and log record                         | low        | 1    | —                |
| P0-008     | P0       | Emit failure and business-outcome telemetry                                     | medium     | 1    | —                |
| P0-009     | P0       | Build the failure, failover, and probe-transition regression suite              | high       | 4    | —                |
| P1-001     | P1       | Make Kafka publication durable and its outcome observable                       | medium     | 3    | —                |
| P1-002     | P1       | Own the Kafka listener error, offset, and dead-letter contract                   | high       | 3    | P1-003           |
| P1-003     | P1       | Own the Kafka listener error, offset, and dead-letter contract                   | high       | 3    | P1-002           |
| P1-004     | P1       | Declare bounded, externalized deadlines for every remote dependency              | medium     | 3    | P1-005, P1-006   |
| P1-005     | P1       | Declare bounded, externalized deadlines for every remote dependency              | medium     | 3    | P1-004, P1-006   |
| P1-006     | P1       | Declare bounded, externalized deadlines for every remote dependency              | medium     | 3    | P1-004, P1-005   |
| P1-007     | P1       | Add bounded retry with transient-failure classification for database writes      | medium     | 3    | —                |
| P1-008     | P1       | Detect, absorb, and report optimistic-locking conflicts                          | medium     | 3    | —                |
| P1-009     | P1       | Give dependency failures stable caller-visible semantics                         | medium     | 3    | —                |
| P1-010     | P1       | Isolate request threads from blocking dependencies                               | high       | 3    | —                |
| P1-011     | P1       | Contain cache failures and fall through to the authoritative store               | low        | 3    | —                |
| P1-012     | P1       | Declare an explicit cache manager contract                                       | medium     | 3    | P1-013, P1-017   |
| P1-013     | P1       | Declare an explicit cache manager contract                                       | medium     | 3    | P1-012, P1-017   |
| P1-014     | P1       | Coalesce concurrent cache misses                                                 | low        | 3    | —                |
| P1-015     | P1       | Recover from credential rotation without a process restart                       | high       | 3    | —                |
| P1-016     | P1       | Bound the inventory list endpoint                                                | medium     | 3    | —                |
| P1-017     | P1       | Declare an explicit cache manager contract                                       | medium     | 3    | P1-012, P1-013   |
| P2-001     | P2       | Adopt a transactional outbox for commit-ordered event publication                | high       | 4    | —                |
| P2-002     | P2       | Give published events a stable identity and correlation context                  | medium     | 4    | —                |
| P2-003     | P2       | Invalidate the cache on reserve and release                                      | low        | 4    | —                |

### Targeted implementation discovery

Three implementation targets could not be given concrete illustrative code because the decision they depend on has not been made. In each case the surrounding remediation still delivers concrete code for its unblocked targets, so no recommendation is entirely blocked.

| Blocked target                                                  | Related finding | Unresolved input                                                                                                                | Route to                        |
|-------------------------------------------------------------------|-----------------|------------------------------------------------------------------------------------------------------------------------------------|---------------------------------|
| Versioned schema migration runner                                | P0-006          | Which versioned migration mechanism is approved, and whether it executes in-process or as a separate release step                     | Architecture governance review  |
| Self-enforced single-active ownership lease                      | P0-002          | Whether a self-enforced ownership lease with an epoch or fencing token is required, and where it may reside                          | Architecture governance review  |
| Cache client re-initialization on credential rotation            | P1-015          | The approved credential rotation model and whether cache authentication uses an access key or a managed identity token                | Platform evidence request       |

### Approval-gated targets

Six implementation targets change externally observable behaviour and are held until an approval record exists. Each is isolated inside its recommendation so the surrounding resiliency mechanism can proceed without waiting.

| Behaviour requiring approval                                          | Related finding | Decision owner                          |
|-------------------------------------------------------------------------|-----------------|-----------------------------------------|
| Idempotency-key semantics on the reserve and release endpoints           | P0-001          | Product and API contract owner          |
| Response status and body for an unresolvable write conflict              | P1-008          | API contract owner                      |
| Response status, retry guidance, and error vocabulary for dependency failure | P1-009      | API contract owner                      |
| Pagination contract on the inventory list endpoint                       | P1-016          | API contract owner                      |
| Publication timing and delivery semantics for published events           | P2-001          | Architecture and event contract owner   |
| Published event envelope contract and versioning scheme                  | P2-002          | Event contract owner                    |

### Validation and approval boundary

Every numeric budget, threshold, window, retention period, and page size introduced by the remediation is expressed as an externally configurable value, so the code change can land before the numbers are settled. No change modifies the Dockerfile, the CI/CD workflow, the Kubernetes manifests, or any deployed infrastructure, because those assessment domains are disabled. Test detail, validation commands, and acceptance criteria are suppressed in this report by the configured testing-output preference; they remain binding in the authoritative remediation plan and govern implementation and post-implementation review.

<!-- content:implementation-roadmap:end -->

[Back to Top](#top)

<!-- section:appendix-traceability -->
## Appendix A: Traceability

<!-- content:appendix-traceability:start -->

Sections 1 through 7 use display identifiers only. This appendix is the single location where internal workflow identifiers appear, so that traceability is preserved rather than lost. It is presentation-only and adds no finding and no change to priority, severity, status, evidence, control mapping, or change mapping.

Authoritative artifacts that resolve every identifier below:

- Step 2 findings, evidence, and control results: `.copilot-tracking/reviews/2026-09-18/inventory-service-inventory-research-review.md`
- Step 3A remediation plan, priorities, waves, and proposed tests: `.copilot-tracking/plans/2026-09-18/inventory-service-remediation-plan.instructions.md`
- Prioritization policy: `grounding/governance/remediation-prioritization.md`, policy `AA-REMEDIATION-PRIORITY` version 1.0.0

The `Related controls` column names the primary control for each finding. The complete related-control set for every finding is recorded in the Step 2 artifact.

| Display ID | Step 2 finding ID | Step 3A change ID | Priority rule | Proposed test IDs            | Wave | Related controls | Open questions, evidence gaps, and targeted-discovery items |
|------------|-------------------|-------------------|---------------|-------------------------------|------|------------------|---------------------------------------------------------------|
| P0-001     | F-003             | CHANGE-AA-008     | P0-AA-012     | PT-008-01, PT-008-02          | 2    | APP-AA-011       | OQ-009, OQ-010                                                 |
| P0-002     | F-004             | CHANGE-AA-007     | P0-AA-006     | PT-007-01, PT-007-02          | 2    | APP-KAFKA-001    | OQ-007 (blocks ICB-007-03), OQ-008, EG-010                      |
| P0-003     | F-008             | CHANGE-AA-001     | P0-AA-004     | PT-001-01, PT-001-02          | 1    | APP-AA-007       | OQ-001                                                          |
| P0-004     | F-021             | CHANGE-AA-004     | P0-AA-014     | PT-004-01                     | 1    | APP-AA-017       | OQ-004, OQ-005, EG-005                                          |
| P0-005     | F-022             | CHANGE-AA-003     | P0-AA-009     | PT-003-01                     | 1    | KV-009           | OQ-003                                                          |
| P0-006     | F-024             | CHANGE-AA-002     | P0-AA-001     | PT-002-01                     | 1    | APP-AA-013       | OQ-002 (blocks ICB-002-03)                                      |
| P0-007     | F-026             | CHANGE-AA-005     | P0-AA-013     | PT-005-01                     | 1    | APP-AA-015       | OQ-006                                                          |
| P0-008     | F-027             | CHANGE-AA-006     | P0-AA-013     | PT-006-01                     | 1    | APP-AA-016       | —                                                               |
| P0-009     | F-028             | CHANGE-AA-024     | P0-AA-013     | PT-024-01, PT-024-02, PT-024-03 | 4  | APP-AA-018       | OQ-025                                                          |
| P1-001     | F-001             | CHANGE-AA-018     | P1-RCV-005    | PT-018-01                     | 3    | APP-KAFKA-005    | OQ-018, EG-002                                                  |
| P1-002     | F-005             | CHANGE-AA-019     | P1-RCV-007    | PT-019-01, PT-019-02          | 3    | APP-KAFKA-002    | OQ-019                                                          |
| P1-003     | F-006             | CHANGE-AA-019     | P1-RCV-007    | PT-019-01, PT-019-02          | 3    | APP-KAFKA-003    | OQ-019                                                          |
| P1-004     | F-009             | CHANGE-AA-009     | P1-RCV-006    | PT-009-01                     | 3    | SQL-002          | OQ-011, EG-006                                                  |
| P1-005     | F-010             | CHANGE-AA-009     | P1-RCV-006    | PT-009-01                     | 3    | REDIS-005        | OQ-011, EG-006                                                  |
| P1-006     | F-011             | CHANGE-AA-009     | P1-RCV-006    | PT-009-01                     | 3    | KAFKA-005        | OQ-011, EG-006                                                  |
| P1-007     | F-012             | CHANGE-AA-010     | P1-RCV-001    | PT-010-01                     | 3    | SQL-003          | OQ-012                                                          |
| P1-008     | F-013             | CHANGE-AA-011     | P1-RCV-001    | PT-011-01                     | 3    | SQL-007          | OQ-013                                                          |
| P1-009     | F-014             | CHANGE-AA-012     | P1-RCV-005    | PT-012-01                     | 3    | APP-WEB-002      | OQ-014                                                          |
| P1-010     | F-015             | CHANGE-AA-013     | P1-RCV-008    | PT-013-01                     | 3    | APP-AA-006       | OQ-015                                                          |
| P1-011     | F-016             | CHANGE-AA-014     | P1-RCV-011    | PT-014-01                     | 3    | REDIS-020        | —                                                               |
| P1-012     | F-017             | CHANGE-AA-015     | P1-RCV-011    | PT-015-01, PT-015-02          | 3    | REDIS-011        | OQ-016                                                          |
| P1-013     | F-018             | CHANGE-AA-015     | P1-RCV-011    | PT-015-01, PT-015-02          | 3    | REDIS-022        | OQ-016                                                          |
| P1-014     | F-019             | CHANGE-AA-016     | P1-RCV-008    | PT-016-01                     | 3    | REDIS-009        | —                                                               |
| P1-015     | F-023             | CHANGE-AA-020     | P1-RCV-009    | PT-020-01                     | 3    | KV-005           | OQ-020 (blocks ICB-020-03), EG-003                              |
| P1-016     | F-025             | CHANGE-AA-017     | P1-RCV-008    | PT-017-01                     | 3    | JVM-004          | OQ-017                                                          |
| P1-017     | F-029             | CHANGE-AA-015     | P1-RCV-011    | PT-015-01, PT-015-02          | 3    | REDIS-012        | OQ-016                                                          |
| P2-001     | F-002             | CHANGE-AA-021     | P2-DATA-002   | PT-021-01, PT-021-02          | 4    | APP-DB-003       | OQ-021, OQ-022                                                  |
| P2-002     | F-007             | CHANGE-AA-022     | P2-DATA-007   | PT-022-01                     | 4    | APP-KAFKA-006    | OQ-023, EG-011                                                  |
| P2-003     | F-020             | CHANGE-AA-023     | P2-DATA-010   | PT-023-01                     | 4    | REDIS-015        | OQ-024                                                          |

All governed priorities are included in this report, so no finding identifiers are omitted. Five findings share a remediation change with another finding, which is visible above where the same change identifier appears on more than one row: F-005 and F-006 under `CHANGE-AA-019`, F-009, F-010, and F-011 under `CHANGE-AA-009`, and F-017, F-018, and F-029 under `CHANGE-AA-015`.

### Carried-forward unresolved items

Evidence gaps `EG-001` through `EG-011` and control coverage gaps `CCG-001` through `CCG-004` were carried forward from Step 2 without conversion into remediation work. Inventory exceptions `EXC-A-001`, `EXC-001`, `EXC-002`, `EXC-003`, and `EXC-004` were preserved as recorded.

### Governance observations recorded during planning

Three prioritization-policy observations were recorded and routed to policy governance. They do not change any priority in this report.

- The graceful-shutdown rule heading is `P0-AA-014` while its embedded rule body declares `P0-RCV-014`. Heading identifiers are cited throughout the plan and this appendix.
- The P2 elevation rule references `P0-AA-011`, which is undefined; the defined data-integrity rule is `P0-AA-012`.
- No rule addresses a normal-operation data-correctness defect outside the active-active frame, which is why `F-020` lands at P2 under the closest applicable rule `P2-DATA-010`.

<!-- content:appendix-traceability:end -->

[Back to Top](#top)

<!-- schema-conformance:start -->
<!--
schema_conformance:
  schema_id: CODE-LEVEL-RESILIENCY-ASSESSMENT-REPORT
  schema_version: "1.11.0"
  required_sections_present: true
  required_section_order_valid: true
  required_finding_fields_present: true
  summary_counts_reconcile: true
  finding_matrix_reconciles: true
  roadmap_matches_plan: true
  unsupported_findings_added: false
  priorities_changed: false
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
  reference_architecture_registry_supplied: true
  reference_architecture_registry_lifecycle_status: approved
  reference_architecture_table_rendered: true
  reference_architecture_source: approved_registry
  reference_architecture_column_order_valid: true
  no_registry_statement_used: false
  invented_reference_links: 0
  deployment_source_and_target_separated: true
  current_deployment_rendered_from_source: true
  approved_target_deployment_rendered_from_target: true
  migration_context_rendered: true
  target_reported_as_current: false
  source_reported_as_target: false
  source_and_target_regions_merged: false
  dependency_topology_used_as_application_topology: false
  migration_delta_reported_as_finding: false
  status: passed

report_finding_selection:
  mode: all_priorities
  requested_priorities: [P0, P1, P2, P3]
  included_priorities: [P0, P1, P2, P3]
  omitted_priorities: []
  included_finding_ids: [F-001, F-002, F-003, F-004, F-005, F-006, F-007, F-008, F-009, F-010, F-011, F-012, F-013, F-014, F-015, F-016, F-017, F-018, F-019, F-020, F-021, F-022, F-023, F-024, F-025, F-026, F-027, F-028, F-029]
  omitted_finding_ids: []
  included_change_ids: [CHANGE-AA-001, CHANGE-AA-002, CHANGE-AA-003, CHANGE-AA-004, CHANGE-AA-005, CHANGE-AA-006, CHANGE-AA-007, CHANGE-AA-008, CHANGE-AA-009, CHANGE-AA-010, CHANGE-AA-011, CHANGE-AA-012, CHANGE-AA-013, CHANGE-AA-014, CHANGE-AA-015, CHANGE-AA-016, CHANGE-AA-017, CHANGE-AA-018, CHANGE-AA-019, CHANGE-AA-020, CHANGE-AA-021, CHANGE-AA-022, CHANGE-AA-023, CHANGE-AA-024]
  omitted_change_ids: []
  selection_frozen: true
  authoritative_findings_changed: false
  priorities_recalculated: false
  filtered_view: false

report_testing_output:
  mode: hidden
  show_test_findings: true
  show_test_code: false
  show_validation_commands: false
  show_acceptance_criteria: false
  show_validation_evidence: false
  include_consolidated_validation_strategy: false
  test_targets_suppressed: 32
  authority_note: Report rendering only. Every test and validation obligation remains binding on Step 4 and Step 5.

illustrative_code_conformance:
  applicable_targets: 57
  generated_code_blocks_rendered: 51
  shared_remediation_verbatim_excerpt_blocks_rendered: 4
  targeted_discovery_targets_rendered: 3
  not_applicable_targets: 0
  invalid_generated_proposals: 0
  narrative_only_code_blocks_rendered: 0
  status: passed

repository_agnostic_snapshot_conformance:
  repository_git_metadata_required: false
  assessment_snapshot_type: workspace_snapshot
  assessment_snapshot_type_valid: true
  assessment_snapshot_identifier_present_or_explicitly_unavailable: true
  git_sha_shown_only_for_git_revision: true
  source_fingerprint_precedes_snapshot_and_lines: true
  line_numbers_labeled_advisory: true

report_assembly_conformance:
  incremental_assembly_used: true
  report_manifest_frozen: true
  selected_findings_written_once: true
  required_sections_written_once: true
  duplicate_section_markers: 0
  duplicate_finding_markers: 0
  missing_selected_finding_markers: 0
  unexpected_finding_markers: 0
  report_reopened_after_write: true
  final_report_parse_complete: true
  recovery_count: 0
  section_markers_present: 8
  finding_markers_present: 29
  original_source_labels_rendered: 40
  back_to_top_links: 8
  standards_reference_lines: 29

source_rendering_conformance:
  full_fingerprints_preserved_in_authoritative_artifacts: true
  report_fingerprints_abbreviated: true
  original_source_blocks_unmodified: true
  comments_added_inside_original_source_blocks: false

finding_classification_conformance:
  qualification_policy_id: RESILIENCY-FINDING-QUALIFICATION
  qualification_policy_version: "1.0.0"
  every_finding_has_classification: true
  resiliency_findings_have_complete_impact_chain: true
  non_resiliency_findings_retained: true
  resiliency_section_precedes_non_resiliency_section: true
  priority_order_within_each_class: [P0, P1, P2, P3]
  classes_not_intermixed: true
  class_priority_counts_reconcile: true
  counts_by_class: {resiliency: 26, non_resiliency: 3}
  counts_by_priority: {P0: 9, P1: 17, P2: 3, P3: 0}

identifier_suppression_conformance:
  display_ids_only_in_sections_1_to_7: true
  internal_identifiers_resolved_in_appendix_a: true
  suppression_changed_findings_or_priorities: false
-->
<!-- schema-conformance:end -->
