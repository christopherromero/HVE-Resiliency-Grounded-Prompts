package com.ecommerce.inventory.kafka.consumer;

import com.ecommerce.inventory.service.InventoryService;
import lombok.RequiredArgsConstructor;
import org.springframework.kafka.annotation.KafkaListener;
import org.springframework.stereotype.Component;

import java.util.Map;

@Component @RequiredArgsConstructor
public class OrderEventConsumer {
    private final InventoryService service;
    @KafkaListener(topics = "order-events", groupId = "inventory-service")
    public void consume(Map<String, Object> event) {
        String type = String.valueOf(event.get("type"));
        String productId = String.valueOf(event.get("productId"));
        int quantity = ((Number) event.get("quantity")).intValue();
        String orderId = String.valueOf(event.get("orderId"));
        if ("ORDER_CREATED".equals(type)) service.reserve(productId, quantity, orderId);
        if ("ORDER_CANCELLED".equals(type)) service.release(productId, quantity, orderId);
    }
}