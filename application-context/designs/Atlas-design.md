---
title: Atlas Global Cluster Design
description: Inventory-state ownership and consistency contract
decision_id: ADR-ATLAS-001
status: Approved
---

## Contract

| Subject | Decision |
|---|---|
| Zone ownership | West US 2 owns location group A; West US owns location group B. Geographic ownership routes records to the corresponding shards. |
| Shard keys | Inventory records use `{location: 1, inventoryId: 1}`. Production data distribution and query routing must validate this choice. |
| Uniqueness | Inventory identity is unique within location. Any required global uniqueness needs a separately approved enforcement mechanism. |
| Write durability | Business writes require majority acknowledgment. A timeout does not prove that the write failed. |
| Read consistency | Decision-making reads use the primary with majority read concern. Secondary reads are permitted only for explicitly stale-tolerant views. |
| Read-your-writes | Workflows requiring causal visibility use supported causal sessions and appropriate read/write concerns. |
| Election and partition | Each shard has one writable primary. Writes pause when no suitable primary or required quorum is available; the application must not claim universal regional autonomy. |
| Recovery | Driver topology discovery and bounded retries support election recovery without process restart. Node placement, quorum, and recovery objectives require platform validation. |

## Approval

Approved. Architecture, database, and application owners must validate
ownership, shard keys, uniqueness, consistency, node placement, and failure budgets.