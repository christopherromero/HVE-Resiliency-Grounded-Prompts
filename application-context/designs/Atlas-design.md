---
title: Atlas Global Cluster Design
description: Regional record ownership, shard-key, and consistency contract for authoritative state
decision_id: ADR-ATLAS-001
status: approved
version: "2.1.0"
approved_by: Architecture, database, and application owners
approved_at: "2026-11-04"
---

## Decision Summary

Authoritative business state uses an Atlas Global Cluster with two write-owning zones, one per active region. Every business record has exactly one owning region. Writes for a record go to the primary of the shard in that record's zone. Each shard has one writable primary, so a region cannot write every record during every partition.

## Contract

| Subject                | Decision                                                                                                                                                                                                                                                                                                               |
|------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Zone ownership         | Each business record carries an `owningRegion` field with the value `westus2` or `westus`. The zone whose highest-priority region matches `owningRegion` owns writes for that record.                                                                                                                                  |
| Ownership assignment   | The region that accepts a record's creation request sets `owningRegion` once, and the value never changes. Related records inherit the parent record's `owningRegion`. Ownership transfer requires the approved runbook.                                                                                               |
| Zones                  | `westus2-zone` has highest-priority region `westus2` and electable regions `westus` and `eastus`. `westus-zone` has highest-priority region `westus` and electable regions `westus2` and `eastus`. Electable secondaries are election targets, not additional write owners.                                            |
| Shard keys             | Record-scoped collections use `{owningRegion: 1, <record identifier>: 1}`. Applying the Contract defines which collections are record-scoped.                                                                                                                                                                          |
| Unsharded collections  | Collections that are not record-scoped stay unsharded on the database primary shard. Writes to them depend on that shard's primary.                                                                                                                                                                                    |
| Uniqueness             | Record identity is unique within `owningRegion` through a unique index prefixed by the shard key. The issuing system guarantees cross-region uniqueness of record identifiers. The database does not enforce uniqueness of non-shard-key attributes across zones. Any such rule needs a separately approved mechanism. |
| Cross-zone lookups     | Queries without `owningRegion`, such as a lookup by a secondary business identifier, are permitted scatter-gather reads. If a lookup cannot reach every zone, the result is unknown rather than "not found", and the caller keeps the work recoverable.                                                                |
| Write durability       | Business writes use `w: majority` with a bounded write timeout. A timeout does not prove that the write failed.                                                                                                                                                                                                        |
| Read consistency       | Decision-making reads use the primary with `majority` read concern. Secondary and nearest reads are permitted only for views that an approved addendum declares stale-tolerant.                                                                                                                                        |
| Read-your-writes       | Multi-step operations that write and then read the same record use causally consistent sessions with majority read and write concern.                                                                                                                                                                                  |
| Election and partition | Writes for a zone pause when the zone has no electable primary or quorum. A region stays available for records whose zone primary it can reach. The application must not claim universal regional autonomy.                                                                                                            |
| Readiness              | Readiness reflects whether the driver can select a server through topology discovery. Losing one zone's primary does not by itself make every pod unready, and affected operations fail recoverably. Liveness never depends on MongoDB.                                                                                |
| Recovery               | Driver topology discovery, retryable writes and reads, and bounded server-selection timeouts handle election recovery without restarting the process.                                                                                                                                                                  |

## Applying the Contract

These rules map any application's collections to the contract without application-specific bindings.

* A collection is record-scoped when each document belongs to one business record and carries that record's identifier, either as a field or as the document `_id`.
* A record-scoped collection keyed by a secondary business identifier copies `owningRegion` from the record that owns the identifier.
* Reference data, configuration, user preferences, feature-toggle state, and coordination data such as scheduler locks are not record-scoped.
* Every database and client the application uses on the cluster follows this contract.
* Exceptions, such as stale-tolerant views or a different shard key, require an approved addendum referenced from the application architecture context. Do not infer an exception.

## Assessment Interpretation

* Repository behavior that contradicts this contract can produce a finding, such as a record-scoped collection without `owningRegion`, a non-majority write concern, or a secondary read used for a decision.
* When repository evidence cannot show whether a collection is record-scoped, record the collection as `not_assessed` and route it to architecture governance.
* Deployed zones, node placement, quorum, and failover behavior are external evidence. Missing proof is an evidence gap. It does not create a finding and does not make this contract unapproved.

## External Validation

The platform and database teams validate the following items against the deployed cluster. These items are not approval conditions.

* Zone-to-shard mapping and `owningRegion` routing on the deployed Global Cluster
* Electable node placement, quorum, and election behavior after region loss
* Data distribution and query routing for each shard key
* Recovery time and recovery point objectives

## Approval

Approved by the architecture, database, and application owners for the target active-active state.
