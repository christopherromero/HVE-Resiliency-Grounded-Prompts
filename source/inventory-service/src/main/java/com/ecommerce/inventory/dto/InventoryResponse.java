package com.ecommerce.inventory.dto;

import java.time.Instant;

public record InventoryResponse(Long id, String productId, int availableQuantity, int reservedQuantity, Instant updatedAt) {
}