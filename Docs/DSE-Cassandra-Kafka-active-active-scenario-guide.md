# DSE Cassandra and Kafka Active-Active Scenario Guide

## Target design

- The application runs active-active in both approved regions.
- DSE Cassandra is the authoritative business-state dependency and operates active-active across approved datacenters.
- Kafka uses independent regional clusters with multi-active processing.
- Required business and compacted topics are mirrored.
- Cassandra clients use the local datacenter during normal operation.
- Kafka clients use the local regional cluster during normal operation.
- Stable operation and event identity supports duplicate, retry, replay, and recovery safety.

## Evidence boundaries

Repository evidence can validate configuration injection, local-affinity settings, consistency configuration, idempotency declarations, retry behavior, topic use, identity propagation, and tests. It cannot prove deployed Cassandra replication, repair state, cluster health, Kafka mirroring state, or offset synchronization. Missing deployed evidence is an evidence gap.

## Installation

Overlay this package at repository root. Use the new sample context as a starting point; do not replace another application's approved context without architecture review.

## Rerun sequence

Rerun Steps 1, 2, 3A, and 3B. Rerun Step 4 only after Human SME approval of the new plan. Step 5 validates only implementations produced from the revised authoritative plan.
