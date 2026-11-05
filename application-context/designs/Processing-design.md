---
title: Processing and Completion Design
description: Operation identity, deduplication, and database and Kafka completion contract
decision_id: ADR-PROCESSING-001
status: approved
version: "2.1.0"
approved_by: Product, application, and database owners
approved_at: "2026-11-04"
---

## Decision Summary

Event-triggered processing is at-least-once and idempotent. Both regions may process the same event. A durable processing receipt, written in the same Atlas transaction as the business-state change, ensures that each operation mutates state once. Consumer offsets advance only after that transaction commits.

## Contract

| Subject             | Decision                                                                                                                                                                                                                                                                                                                   |
|---------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Scope               | This version governs event-triggered processing. HTTP-initiated actions and outbound side effects are covered under Additional effects.                                                                                                                                                                                    |
| Operation identity  | For event-triggered processing, the operation ID equals the event's `eventId` (see Kafka design). Retries reuse it. The processor never generates a replacement identity.                                                                                                                                                  |
| Event identity      | Each logical event has a stable `eventId` that mirroring, retry, and replay leave unchanged. Kafka offsets, partitions, and timestamps are not identity.                                                                                                                                                                   |
| Deduplication       | A durable receipt in a `processing_receipt` collection records each applied operation, keyed by `{owningRegion, <record identifier>, operationId}` with a payload fingerprint. When an operation ID is reused with a different payload, the receipt records it as quarantined and the processor does not apply it.         |
| Atomic state change | One Atlas multi-document transaction covers every business-record write for an operation and its receipt. An operation changes records of a single `owningRegion`, so cross-zone transactions are not part of this design.                                                                                                 |
| Concurrent attempts | When both regions process the same event, the zone primary serializes the transactions. The unique receipt index lets exactly one commit, and the other attempt confirms the receipt and treats the operation as applied.                                                                                                  |
| Offset completion   | Consumer offsets advance only after the transaction commits with majority acknowledgment. Logging an error and then acknowledging the record is not completion. Kafka transactions do not make Atlas writes atomic with offsets.                                                                                           |
| Business skips      | An intentional business decision not to apply an event, such as a record that is not eligible, is a completed outcome. A dependency error, a timeout, or an unknown lookup result is a failure, not a skip.                                                                                                                |
| Ambiguous outcome   | After a timeout or an unknown commit result, the processor checks the receipt before retrying. If completion cannot be established, the record stays unacknowledged and recoverable.                                                                                                                                       |
| Poison events       | An event that fails deterministically after bounded retries is recorded as a quarantined receipt with the failure reason and then acknowledged. If the event does not identify a record, the receipt uses the consuming region as `owningRegion` and a null record identifier. Replay from quarantine follows the runbook. |
| Replay              | Replaying a completed operation produces no additional state change.                                                                                                                                                                                                                                                       |
| Additional effects  | Outbound events, calls that mutate other services, writes to other databases, and notifications are not covered by this transaction. They need a separately approved completion and reconciliation design.                                                                                                                 |

## Applying the Contract

These rules map any application's processing flows to the contract without application-specific bindings.

* Every Kafka listener or receiver that changes authoritative state is an event-triggered flow under this contract.
* The receipt's record identifier is the identifier of the business record the flow changes, as defined in the Atlas design.
* A flow that resolves its record through a cross-zone lookup treats an incomplete lookup as a failure, not a skip.
* Effects outside the Atlas transaction are additional effects. Assessments evaluate only the common controls that apply to them until a separate design is approved.
* Exceptions require an approved addendum referenced from the application architecture context. Do not infer an exception.

## Assessment Interpretation

* Repository behavior that contradicts this contract can produce a finding. Examples include using an offset as identity, acknowledging after an error, writing related records outside one transaction, or treating an unknown lookup as a skip.
* Missing production evidence for transaction performance or the deployed receipt indexes is an evidence gap. It does not create a finding and does not make this contract unapproved.
* Do not infer a completion design for additional effects.

## External Validation

The application and database teams validate the following items. These items are not approval conditions.

* Transaction latency and abort rates under production load
* Receipt index creation and receipt retention
* Quarantine replay runbook rehearsal

## Approval

Approved by the product, application, and database owners for business identity, duplicate semantics, transaction boundaries, and recovery behavior.
