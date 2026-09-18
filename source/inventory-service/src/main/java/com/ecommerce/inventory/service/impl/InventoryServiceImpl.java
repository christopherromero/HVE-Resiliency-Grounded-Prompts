package com.ecommerce.inventory.service.impl;

import com.ecommerce.inventory.dto.InventoryRequest;
import com.ecommerce.inventory.dto.InventoryResponse;
import com.ecommerce.inventory.exception.ResourceNotFoundException;
import com.ecommerce.inventory.kafka.producer.InventoryEventProducer;
import com.ecommerce.inventory.mapper.InventoryMapper;
import com.ecommerce.inventory.model.InventoryItem;
import com.ecommerce.inventory.repository.InventoryRepository;
import com.ecommerce.inventory.service.InventoryService;
import lombok.RequiredArgsConstructor;
import org.springframework.cache.annotation.CacheEvict;
import org.springframework.cache.annotation.Cacheable;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.time.Instant;
import java.util.List;

@Service @RequiredArgsConstructor
public class InventoryServiceImpl implements InventoryService {
    private final InventoryRepository repository;
    private final InventoryMapper mapper;
    private final InventoryEventProducer producer;
    @Override @Transactional
    public InventoryResponse create(InventoryRequest request) {
        if (repository.existsByProductId(request.productId())) throw new IllegalArgumentException("Inventory already exists for product: " + request.productId());
        InventoryItem item = mapper.toEntity(request); item.setUpdatedAt(Instant.now()); return saveAndPublish(item, "INVENTORY_CREATED", "");
    }
    @Override @Cacheable(cacheNames = "inventory", key = "#id")
    public InventoryResponse get(Long id) { return mapper.toResponse(find(id)); }
    @Override public List<InventoryResponse> list() { return repository.findAll().stream().map(mapper::toResponse).toList(); }
    @Override @Transactional @CacheEvict(cacheNames = "inventory", key = "#id")
    public InventoryResponse update(Long id, InventoryRequest request) { InventoryItem item = find(id); mapper.update(request, item); item.setUpdatedAt(Instant.now()); return saveAndPublish(item, "INVENTORY_UPDATED", ""); }
    @Override @Transactional @CacheEvict(cacheNames = "inventory", key = "#id")
    public void delete(Long id) { InventoryItem item = find(id); repository.delete(item); producer.publish("INVENTORY_DELETED", mapper.toResponse(item), ""); }
    @Override @Transactional
    public InventoryResponse reserve(String productId, int quantity, String referenceId) {
        InventoryItem item = findByProduct(productId);
        if (item.getAvailableQuantity() < quantity) throw new IllegalArgumentException("Insufficient inventory for product: " + productId);
        item.setAvailableQuantity(item.getAvailableQuantity() - quantity); item.setReservedQuantity(item.getReservedQuantity() + quantity); item.setUpdatedAt(Instant.now());
        return saveAndPublish(item, "INVENTORY_RESERVED", referenceId);
    }
    @Override @Transactional
    public InventoryResponse release(String productId, int quantity, String referenceId) {
        InventoryItem item = findByProduct(productId);
        if (item.getReservedQuantity() < quantity) throw new IllegalArgumentException("Release exceeds reserved inventory for product: " + productId);
        item.setReservedQuantity(item.getReservedQuantity() - quantity); item.setAvailableQuantity(item.getAvailableQuantity() + quantity); item.setUpdatedAt(Instant.now());
        return saveAndPublish(item, "INVENTORY_RELEASED", referenceId);
    }
    private InventoryResponse saveAndPublish(InventoryItem item, String type, String referenceId) { InventoryResponse response = mapper.toResponse(repository.save(item)); producer.publish(type, response, referenceId); return response; }
    private InventoryItem find(Long id) { return repository.findById(id).orElseThrow(() -> new ResourceNotFoundException("Inventory not found: " + id)); }
    private InventoryItem findByProduct(String productId) { return repository.findByProductId(productId).orElseThrow(() -> new ResourceNotFoundException("Inventory not found for product: " + productId)); }
}