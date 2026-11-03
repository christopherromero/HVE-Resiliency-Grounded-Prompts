---
title: Inventory Processing and Completion Design
description: Identity, deduplication, and database/Kafka completion contract
decision_id: ADR-PROCESSING-001
status: approved
---

## Contract

| Subject | Decision |
|---|---|
| Operation identity | The originating business request supplies a stable operation ID. Retries reuse it rather than generating another identity. |
| Event identity | Each logical command has a stable event ID, unchanged by mirroring, retry, or replay. |
| Deduplication | A durable processing receipt identifies an applied operation. Reuse with a different payload is rejected or quarantined, not silently accepted. |
| Atomic state change | The approved design uses an Atlas transaction covering the inventory update and processing receipt. Implementation must validate transaction support, collection placement, and performance. |
| Offset completion | Consumer offsets advance only after required database work is durably completed. Kafka transactions do not make Atlas writes atomic with offsets. |
| Ambiguous outcome | After a timeout, the processor checks the durable receipt before retrying. If completion cannot be established safely, processing remains recoverable and unacknowledged. |
| Replay | A replayed completed operation produces no additional inventory mutation. Concurrent attempts converge through approved uniqueness and concurrency controls. |
| Additional effects | This design excludes outbound events and external side effects. Those require a separately approved completion/reconciliation design. |

## Approval

Approved. Product, application, and database owners approve business
identity, duplicate semantics, transaction boundaries, and recovery behavior.