package com.ecommerce.inventory.mapper;

import com.ecommerce.inventory.dto.InventoryRequest;
import com.ecommerce.inventory.dto.InventoryResponse;
import com.ecommerce.inventory.model.InventoryItem;
import org.mapstruct.Mapper;
import org.mapstruct.Mapping;
import org.mapstruct.MappingTarget;

@Mapper(componentModel = "spring")
public interface InventoryMapper {
    @Mapping(target = "id", ignore = true) @Mapping(target = "reservedQuantity", ignore = true) @Mapping(target = "updatedAt", ignore = true) @Mapping(target = "version", ignore = true)
    InventoryItem toEntity(InventoryRequest request);
    InventoryResponse toResponse(InventoryItem item);
    @Mapping(target = "id", ignore = true) @Mapping(target = "reservedQuantity", ignore = true) @Mapping(target = "updatedAt", ignore = true) @Mapping(target = "version", ignore = true)
    void update(InventoryRequest request, @MappingTarget InventoryItem item);
}