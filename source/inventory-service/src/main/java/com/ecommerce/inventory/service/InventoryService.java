package com.ecommerce.inventory.service;

import com.ecommerce.inventory.dto.InventoryRequest;
import com.ecommerce.inventory.dto.InventoryResponse;

import java.util.List;

public interface InventoryService {
    InventoryResponse create(InventoryRequest request);
    InventoryResponse get(Long id);
    List<InventoryResponse> list();
    InventoryResponse update(Long id, InventoryRequest request);
    void delete(Long id);
    InventoryResponse reserve(String productId, int quantity, String referenceId);
    InventoryResponse release(String productId, int quantity, String referenceId);
}