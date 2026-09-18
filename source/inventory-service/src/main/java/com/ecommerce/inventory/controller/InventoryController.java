package com.ecommerce.inventory.controller;

import com.ecommerce.inventory.dto.InventoryRequest;
import com.ecommerce.inventory.dto.InventoryResponse;
import com.ecommerce.inventory.dto.StockAdjustmentRequest;
import com.ecommerce.inventory.service.InventoryService;
import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController @RequestMapping("/api/v1/inventory") @RequiredArgsConstructor
public class InventoryController {
    private final InventoryService service;
    @PostMapping @ResponseStatus(HttpStatus.CREATED) public InventoryResponse create(@Valid @RequestBody InventoryRequest request) { return service.create(request); }
    @GetMapping("/{id}") public InventoryResponse get(@PathVariable Long id) { return service.get(id); }
    @GetMapping public List<InventoryResponse> list() { return service.list(); }
    @PutMapping("/{id}") public InventoryResponse update(@PathVariable Long id, @Valid @RequestBody InventoryRequest request) { return service.update(id, request); }
    @DeleteMapping("/{id}") @ResponseStatus(HttpStatus.NO_CONTENT) public void delete(@PathVariable Long id) { service.delete(id); }
    @PostMapping("/products/{productId}/reserve") public InventoryResponse reserve(@PathVariable String productId, @Valid @RequestBody StockAdjustmentRequest request) { return service.reserve(productId, request.quantity(), request.referenceId()); }
    @PostMapping("/products/{productId}/release") public InventoryResponse release(@PathVariable String productId, @Valid @RequestBody StockAdjustmentRequest request) { return service.release(productId, request.quantity(), request.referenceId()); }
}