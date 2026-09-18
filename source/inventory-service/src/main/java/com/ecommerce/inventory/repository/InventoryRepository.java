package com.ecommerce.inventory.repository;

import com.ecommerce.inventory.model.InventoryItem;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.Optional;

public interface InventoryRepository extends JpaRepository<InventoryItem, Long> {
    Optional<InventoryItem> findByProductId(String productId);
    boolean existsByProductId(String productId);
}