package com.ecommerce.inventory.model;

import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import jakarta.persistence.Table;
import jakarta.persistence.UniqueConstraint;
import jakarta.persistence.Version;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.time.Instant;

@Entity
@Table(name = "inventory_items", uniqueConstraints = @UniqueConstraint(columnNames = "productId"))
@Data @Builder @NoArgsConstructor @AllArgsConstructor
public class InventoryItem {
    @Id @GeneratedValue(strategy = GenerationType.IDENTITY) private Long id;
    private String productId;
    private int availableQuantity;
    private int reservedQuantity;
    private Instant updatedAt;
    @Version private long version;
}