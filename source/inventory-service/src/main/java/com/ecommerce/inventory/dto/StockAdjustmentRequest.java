package com.ecommerce.inventory.dto;

import jakarta.validation.constraints.Positive;

public record StockAdjustmentRequest(@Positive int quantity, String referenceId) {
}