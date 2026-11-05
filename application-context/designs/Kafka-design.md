---
title: Independent Regional Kafka Design
description: Topic ownership, mirroring, event lineage, and offset recovery contract
decision_id: ADR-KAFKA-001
status: approved
version: "2.1.0"
approved_by: Kafka platform and application owners
approved_at: "2026-11-04"
---

## Decision Summary

Each active region runs an independent Kafka cluster. There is no stretched cluster. Every logical topic has one writable origin topic per region, and the other region receives it as a read-only mirror. Consumers in each region process both origin topics from their local cluster, and the Processing design makes cross-region duplicates safe.

## Contract

| Subject                | Decision                                                                                                                                                                                                          |
|------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Clusters               | `westus2` and `westus` use independent clusters. Applications connect only to the cluster in their own region.                                                                                                    |
| Topic ownership        | Each logical topic has one origin topic per region, named `<logical topic>-<region>`. Only producers in that region write to it, so each topic has one writable owner.                                            |
| Replication            | An approved cluster link or replication platform mirrors each origin topic to the other cluster as a read-only topic with the same name. Business and compacted topics are mirrored. Internal topics are not.     |
| Consumers              | In each region, consumers subscribe to both origin topics of a logical topic on the local cluster. A consumer group in one cluster has no relationship to a consumer group with the same ID in the other cluster. |
| Event identity         | Producers set the `eventId` and `originRegion` headers once per logical event. Mirroring, retry, and replay preserve both headers. Offsets, partitions, and timestamps are not event identity.                    |
| Loop prevention        | Consumers never republish a received event to any origin topic. A new event caused by processing receives a new `eventId` and carries the triggering ID in a `causationId` header.                                |
| Ordering               | Ordering holds only per key within a single origin-topic partition. Ordering across origin topics or regions is not guaranteed. Records are keyed by the business record identifier.                              |
| Producer completion    | Producers use `acks=all` with idempotence enabled and observe every send result. A send is complete only after the broker acknowledges it.                                                                        |
| Offset recovery        | Offsets are not equivalent across clusters or topics. Recovery uses the approved checkpoint and offset-translation procedure. Duplicates after recovery are expected, and the Processing design handles them.     |
| Promotion and failback | Producers never write to a read-only mirror. Promotion, ownership transfer, checkpoint selection, and reverse replication follow the controlled runbook.                                                          |

## Applying the Contract

These rules map any application's topics to the contract without application-specific bindings.

* Every topic the application produces to or consumes from is a logical topic under this contract.
* Each region's deployment points the bootstrap configuration at its local cluster.
* Producer topic settings resolve to the local region's origin topic only.
* Consumer topic settings bind both origin topics of the logical topic. A setting that can name only one topic does not meet the contract.
* Producers owned by the application generate one `eventId` per logical event and reuse it on every retry.
* Producers outside the repository supply the `eventId` and `originRegion` headers. Their conformance is external evidence.
* Exceptions, such as a topic that one region alone owns, require an approved addendum referenced from the application architecture context. Do not infer an exception.

## Assessment Interpretation

* Repository behavior that contradicts this contract can produce a finding. Examples include publishing to a mirrored topic, consuming only one origin topic, using an offset as event identity, or republishing received events.
* Topic names supplied through environment variables are bound by their configuration key. Their deployed values are external evidence.
* Deployed clusters, cluster links, mirror topics, permissions, and offset-translation state are external evidence. Missing proof is an evidence gap. It does not create a finding and does not make this contract unapproved.

## External Validation

The Kafka platform team validates the following items against the deployed clusters. These items are not approval conditions.

* Origin and mirror topic creation, cluster links, and replication lag
* Producer and consumer permissions that block writes to mirror topics
* Offset-translation and checkpoint behavior during failover and failback
* External producer conformance for the `eventId` and `originRegion` headers

## Approval

Approved by the Kafka platform and application owners for the target active-active state.
