package com.ecommerce.inventory.kafka.producer;

import com.ecommerce.inventory.dto.InventoryResponse;
import lombok.RequiredArgsConstructor;
import org.springframework.kafka.core.KafkaTemplate;
import org.springframework.stereotype.Component;

import java.time.Instant;
import java.util.Map;

@Component @RequiredArgsConstructor
public class InventoryEventProducer {
    private final KafkaTemplate<String, Object> kafkaTemplate;
    public void publish(String type, InventoryResponse inventory, String referenceId) {
        kafkaTemplate.send("inventory-events", inventory.productId(), Map.of("type", type, "occurredAt", Instant.now().toString(), "referenceId", referenceId == null ? "" : referenceId, "inventory", inventory));
    }
}