package com.ecommerce.inventory.service;

import com.ecommerce.inventory.dto.InventoryResponse;
import com.ecommerce.inventory.kafka.producer.InventoryEventProducer;
import com.ecommerce.inventory.mapper.InventoryMapper;
import com.ecommerce.inventory.model.InventoryItem;
import com.ecommerce.inventory.repository.InventoryRepository;
import com.ecommerce.inventory.service.impl.InventoryServiceImpl;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.*;
import org.mockito.junit.jupiter.MockitoExtension;

import java.time.Instant;
import java.util.Optional;

import static org.assertj.core.api.Assertions.assertThat;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.*;

@ExtendWith(MockitoExtension.class)
class InventoryServiceImplTest {
    @Mock InventoryRepository repository; @Mock InventoryMapper mapper; @Mock InventoryEventProducer producer; @InjectMocks InventoryServiceImpl service;
    @Test void reservesAvailableStockAndPublishesEvent() {
        InventoryItem item = InventoryItem.builder().id(1L).productId("p1").availableQuantity(10).build();
        InventoryResponse response = new InventoryResponse(1L, "p1", 7, 3, Instant.now());
        when(repository.findByProductId("p1")).thenReturn(Optional.of(item)); when(repository.save(any())).thenReturn(item); when(mapper.toResponse(item)).thenReturn(response);
        assertThat(service.reserve("p1", 3, "o1")).isEqualTo(response);
        assertThat(item.getAvailableQuantity()).isEqualTo(7); verify(producer).publish("INVENTORY_RESERVED", response, "o1");
    }
}