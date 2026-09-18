---
title: Inventory Service
description: API, storage, configuration, and event reference for inventory reservations
---

## Purpose

The inventory service owns available and reserved stock for each product. It
supports direct stock adjustments and reacts to order lifecycle events.

## Data and Cache

Inventory records persist in SQL Server through Spring Data JPA. Individual
inventory reads use the Redis-backed `inventory` cache.

## API

The base path is `/api/v1/inventory` on port `8082`.

* `POST /api/v1/inventory` creates inventory for a product
* `GET /api/v1/inventory/{id}` gets an inventory record
* `GET /api/v1/inventory` lists inventory records
* `PUT /api/v1/inventory/{id}` replaces the product and available quantity
* `DELETE /api/v1/inventory/{id}` deletes an inventory record
* `POST /api/v1/inventory/products/{productId}/reserve` reserves stock
* `POST /api/v1/inventory/products/{productId}/release` releases stock

Create and update requests contain `productId` and `availableQuantity`.
Reserve and release requests contain positive `quantity` and optional
`referenceId`.

## Run and Test

Start SQL Server, Redis, and Kafka first, then run:

```powershell
mvn spring-boot:run
```

```powershell
mvn test
```

From the repository root, `docker compose up --build inventory-service` starts
the service and its dependencies.

## Configuration

Local variables are `SQL_URL`, `SQL_USERNAME`, `SQL_PASSWORD`, `REDIS_URL`, and
`KAFKA_BOOTSTRAP_SERVERS`. Production also uses `SPRING_PROFILES_ACTIVE=prod`,
`AZURE_KEYVAULT_ENDPOINT`, `SQL_CONNECTION_STRING`,
`REDIS_CONNECTION_STRING`, and optional `KAFKA_SECURITY_PROTOCOL`.

Key Vault secrets are `sql-connection-string` and `redis-connection-string`.

## Kafka

The service consumes `order-events` as group `inventory-service`. It reserves
stock for `ORDER_CREATED` and releases stock for `ORDER_CANCELLED`. It produces
`inventory-events`, keyed by product ID, for `INVENTORY_CREATED`,
`INVENTORY_UPDATED`, `INVENTORY_DELETED`, `INVENTORY_RESERVED`, and
`INVENTORY_RELEASED`.

See [API and event contracts](../docs/API-CONTRACTS.md) and the
[`inventory-events` schema](../docs/schemas/inventory-events.schema.json).