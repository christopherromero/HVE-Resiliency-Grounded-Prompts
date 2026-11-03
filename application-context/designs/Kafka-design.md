---
title: Independent Regional Kafka Design
description: Topic ownership, replication, and recovery contract
decision_id: ADR-KAFKA-001
status: approved
---

## Contract

| Subject | Decision |
|---|---|
| Clusters | West US 2 and West US use independent clusters. Applications normally connect only to their local cluster. |
| Topic ownership | Region A writes `inventory.commands.origin-a`; region B writes `inventory.commands.origin-b`. Each topic has one writable owner. |
| Replication | Each owned topic is mirrored to the other cluster through its approved link. Distinct names prevent ownership collisions. |
| Loop prevention | Mirrored events retain their original event ID and origin. Consumers do not republish received commands into either origin topic. |
| Consumers | Both regions may consume local and mirrored commands. Cross-cluster duplicate execution is handled by the application, not by Kafka group coordination. |
| Offset recovery | Recovery uses the approved checkpoint/translation procedure. Equal offset numbers across unrelated topics or clusters are not assumed equivalent. |
| Promotion and failback | Producers never write to unpromoted read-only mirrors. Ownership transfer, checkpoint selection, and reverse replication require a controlled runbook. |

## Approval

Approved. Kafka platform and application owners must approve topic/link
mapping, permissions, consumer behavior, promotion, and recovery procedures.