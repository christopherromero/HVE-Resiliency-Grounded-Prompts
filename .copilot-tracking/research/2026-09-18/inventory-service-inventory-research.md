# Spring Boot Active-Active Application Inventory

## Inventory Metadata

```yaml
schema_version: "1.1"
assessment_run_id: "inventory-service-2026-09-18-001"
phase: inventory
inventory_status: complete
inventory_agent: task-researcher
repository_root: "source/inventory-service"
re_inventory_required: false
```

```yaml
assessment_snapshot:
  type: workspace_snapshot
  identifier: "inventory-service-workspace-2026-09-18"
  provenance: workspace_generated
  git_commit_sha: not_applicable
  dirty_worktree: not_applicable
  captured_at: "2026-09-18T00:00:00Z"
  limitations:
    - No Git metadata is present at the workspace root or under source/inventory-service, so no commit identifier is available.
    - Evidence is anchored by repository path, symbol, and exact excerpt rather than by revision.
    - Line ranges are advisory navigation metadata and may shift if the source drop is replaced.
```

```yaml
assessment_scope_resolution:
  context_path: application-context/assessment-scope-context.yml
  schema_path: grounding/governance/assessment-scope-schema.yml
  context_status: valid
  schema_status: valid
  defaults_used: false
  enabled_domains:
    - application_code
    - application_configuration
  disabled_domains:
    - container_build
    - cicd_pipeline
    - deployment_configuration
    - infrastructure_as_code
    - deployed_infrastructure
  inventory_only_domains: []
  report_preferences:
    finding_selection_mode: all_priorities
    included_priorities:
      - P0
      - P1
      - P2
      - P3
    testing_output_mode: hidden
  validation_errors: []
```

```yaml
scope_rules_resolution:
  repository_owned_only: true
  externally_owned_assets: evidence_gap_only
  missing_context_behavior: use_governed_defaults
  unknown_ownership_behavior: not_assessed
  deployed_infrastructure_findings_allowed: false
  pcf_findings_allowed: false
```

```yaml
report_preferences_resolution:
  finding_selection:
    mode: all_priorities
    include_priorities: [P0, P1, P2, P3]
    include_conditional_findings: true
    include_verified_controls: false
    include_evidence_gaps: true
    excluded_priority_behavior: omit_from_filtered_report
  testing_output:
    mode: hidden
    show_test_findings: true
    show_test_code: false
    show_validation_commands: false
    show_acceptance_criteria: false
    show_validation_evidence: false
    include_consolidated_validation_strategy: false
  finding_classification_output:
    include_resiliency_findings: true
    include_non_resiliency_findings: true
    report_section_order: [resiliency, non_resiliency]
    priority_order_within_each_class: [P0, P1, P2, P3]
```

```yaml
out_of_scope_artifacts_observed:
  note: Present in the repository but not inventoried or assessed because the owning domain is disabled.
  container_build:
    - source/inventory-service/Dockerfile
  cicd_pipeline:
    - source/inventory-service/.github/workflows/ci-cd.yml
  deployment_configuration:
    - source/inventory-service/k8s/deployment.yaml
    - source/inventory-service/k8s/service.yaml
    - source/inventory-service/k8s/hpa.yaml
    - source/inventory-service/k8s/secretproviderclass.yaml
  excluded_build_output:
    - source/inventory-service/target/
```

```yaml
resiliency_classification_contract:
  policy_id: RESILIENCY-FINDING-QUALIFICATION
  policy_version: "1.0.0"
  policy_path: grounding/governance/resiliency-finding-qualification-policy.yml
  preserve_finding_classes: [resiliency, non_resiliency]
  applied_in_phase: assessment
  inventory_action: record_evidence_only
```

## Application Profile

```yaml
application_profile:
  application_name: inventory-service
  maven_coordinates: "com.ecommerce:inventory-service:1.0.0"
  module_layout: single_maven_module
  build_tool: maven
  language: java
  java_version: "17"
  framework: spring-boot
  framework_version: "3.3.5"
  spring_cloud_azure_version: "5.18.0"
  runtime_platform: aks
  server_port: 8082
  packaging: jar
  application_type: rest_api_and_kafka_event_processor
  configuration_profiles:
    - default
    - prod
```

```yaml
evidence:
  - file: "source/inventory-service/pom.xml"
    symbol: "project/parent spring-boot-starter-parent"
    start_line: 4
    end_line: 4
    observation: "Spring Boot parent version 3.3.5 governs managed dependency versions."
    confidence: high
    original_line_range:
      start_line: 4
      end_line: 4
      status: exact
  - file: "source/inventory-service/pom.xml"
    symbol: "project/properties/java.version"
    start_line: 6
    end_line: 6
    observation: "Java 17 is the declared build and target language level."
    confidence: high
    original_line_range:
      start_line: 6
      end_line: 6
      status: exact
  - file: "source/inventory-service/src/main/java/com/ecommerce/inventory/InventoryServiceApplication.java"
    symbol: "InventoryServiceApplication"
    start_line: 6
    end_line: 8
    observation: "Single @SpringBootApplication entry point with no custom SpringApplication configuration."
    confidence: high
    original_line_range:
      start_line: 6
      end_line: 8
      status: exact
  - file: "source/inventory-service/src/main/resources/application.yml"
    symbol: "server.port"
    start_line: 2
    end_line: 2
    observation: "HTTP server listens on port 8082."
    confidence: high
    original_line_range:
      start_line: 2
      end_line: 2
      status: exact
  - file: "source/inventory-service/src/main/java/com/ecommerce/inventory/controller/InventoryController.java"
    symbol: "InventoryController"
    start_line: 14
    end_line: 24
    observation: "Seven synchronous REST endpoints under /api/v1/inventory covering create, get, list, update, delete, reserve, and release."
    confidence: high
    original_line_range:
      start_line: 14
      end_line: 24
      status: advisory
```

```yaml
architecture_relationship_context:
  source_path: application-context/application-architecture-context.yml
  context_status: approved
  context_schema_version: "3.0.0"
  context_version: "3.0.0"
  application_name: "Ecommerce Platform"
  repository_name: "Inventory Service"
  business_role: "Inventory tracking"
  context_owner: "Albertsons Ecommerce"
  approved_by: "Albertsons"
  approved_at: "2026-01-01"
  upstream_dependencies: []
  downstream_dependencies: []
  external_side_effects:
    present: false
    types: []
  notes:
    - The approved application context does not declare explicit upstream_dependencies or downstream_dependencies sections.
    - Relationship facts below under repository_observed_interactions are repository-derived and are not approved architecture declarations.
```

```yaml
solution_architecture_context:
  context_status: not_provided
  source_path: application-context/solution-architecture-context.yml
  reason: File does not exist. Single-microservice repository assessment does not require it.
```

```yaml
deployment_evolution_context:
  source:
    state_label: current_deployment
    lifecycle_status: current
    operating_model: active_standby
    traffic_model: single_active
    primary_region: westus
    disaster_recovery_region: eastus
    regions:
      - {region: westus, role: primary, processing_state: active}
      - {region: eastus, role: disaster_recovery, processing_state: standby}
  target:
    state_label: approved_target_deployment
    lifecycle_status: approved_target
    operating_model: active_active
    traffic_model: multi_active
    regions:
      - {region: westus2, role: active, processing_state: active}
      - {region: westus, role: active, processing_state: active}
  transition:
    transition_type: source_to_target
    assessment_focus: target_state_code_readiness
    assess_code_against: target
  reporting_rule: Report current deployment and approved target deployment separately. Do not merge region lists.
```

```yaml
authoritative_state_context:
  dependency: azure-sql
  role: authoritative_business_state
  source: {lifecycle_status: current, operating_model: active_standby, primary_region: westus, disaster_recovery_region: eastus}
  target: {lifecycle_status: approved_target, operating_model: active_standby, primary_region: westus2, standby_region: westus}
  repository_validation: consistent
  repository_basis:
    - JPA entity InventoryItem is the only durable business-state model.
    - Spring Data JPA repository backed by the SQL Server JDBC driver is the only authoritative write path.
```

```yaml
runtime_expectation_context:
  jvm-runtime:
    expected_status: required
    production_use_expected: true
    source: {runtime_family: jvm, runtime_version: unknown, execution_platform: aks, containerized: true}
    target: {runtime_family: jvm, minimum_runtime_version: unknown, execution_platform: aks, containerized: true}
    repository_observed_runtime_version: "17"
    repository_observed_jvm_options: not_available_in_enabled_scope
    virtual_threads_adoption_status: optional
    repository_virtual_thread_evidence: none_found
    notes:
      - spring.threads.virtual.enabled is not present in any in-scope configuration file.
      - Container entrypoint and repository-owned JVM options live in the disabled container_build domain and were not inventoried.
```

## Confirmed Dependencies

```yaml
confirmed_dependencies:

  - id: azure-sql
    classification: confirmed
    expected_status_from_context: required
    production_use_basis: spring_data_jpa_repository_and_jdbc_datasource
    evidence:
      - file: "source/inventory-service/pom.xml"
        symbol: "dependency com.microsoft.sqlserver:mssql-jdbc"
        start_line: 15
        end_line: 15
        observation: "Microsoft SQL Server JDBC driver is declared with runtime scope."
        confidence: high
        original_line_range: {start_line: 15, end_line: 15, status: exact}
      - file: "source/inventory-service/pom.xml"
        symbol: "dependency org.springframework.boot:spring-boot-starter-data-jpa"
        start_line: 11
        end_line: 11
        observation: "Spring Data JPA starter is declared as a compile dependency."
        confidence: high
        original_line_range: {start_line: 11, end_line: 11, status: exact}
      - file: "source/inventory-service/src/main/resources/application.yml"
        symbol: "spring.datasource.url"
        start_line: 7
        end_line: 7
        observation: "Datasource URL defaults to jdbc:sqlserver://localhost:1433;databaseName=inventory;encrypt=false and is overridable through SQL_URL."
        confidence: high
        original_line_range: {start_line: 7, end_line: 7, status: exact}
      - file: "source/inventory-service/src/main/resources/application-prod.yml"
        symbol: "spring.datasource.url"
        start_line: 5
        end_line: 5
        observation: "Production datasource URL is supplied entirely by the SQL_CONNECTION_STRING property with no repository-visible host, listener, or failover configuration."
        confidence: high
        original_line_range: {start_line: 5, end_line: 5, status: exact}
      - file: "source/inventory-service/src/main/java/com/ecommerce/inventory/repository/InventoryRepository.java"
        symbol: "InventoryRepository extends JpaRepository<InventoryItem, Long>"
        start_line: 8
        end_line: 11
        observation: "Spring Data JPA repository defines findByProductId and existsByProductId derived queries."
        confidence: high
        original_line_range: {start_line: 8, end_line: 11, status: exact}
      - file: "source/inventory-service/src/main/java/com/ecommerce/inventory/model/InventoryItem.java"
        symbol: "InventoryItem"
        start_line: 17
        end_line: 27
        observation: "JPA entity mapped to inventory_items with a unique constraint on productId and an @Version optimistic locking field."
        confidence: high
        original_line_range: {start_line: 17, end_line: 27, status: exact}

  - id: confluent-kafka
    classification: confirmed
    expected_status_from_context: required
    production_use_basis: kafka_template_producer_and_kafka_listener_consumer
    evidence:
      - file: "source/inventory-service/pom.xml"
        symbol: "dependency org.springframework.kafka:spring-kafka"
        start_line: 14
        end_line: 14
        observation: "Spring for Apache Kafka is declared as a compile dependency."
        confidence: high
        original_line_range: {start_line: 14, end_line: 14, status: exact}
      - file: "source/inventory-service/src/main/java/com/ecommerce/inventory/kafka/producer/InventoryEventProducer.java"
        symbol: "InventoryEventProducer.publish"
        start_line: 13
        end_line: 16
        observation: "KafkaTemplate<String, Object> publishes to the inventory-events topic keyed by productId."
        confidence: high
        original_line_range: {start_line: 13, end_line: 16, status: exact}
      - file: "source/inventory-service/src/main/java/com/ecommerce/inventory/kafka/consumer/OrderEventConsumer.java"
        symbol: "OrderEventConsumer.consume"
        start_line: 13
        end_line: 21
        observation: "@KafkaListener consumes topic order-events with groupId inventory-service and maps ORDER_CREATED and ORDER_CANCELLED to reserve and release."
        confidence: high
        original_line_range: {start_line: 13, end_line: 21, status: exact}
      - file: "source/inventory-service/src/main/resources/application.yml"
        symbol: "spring.kafka"
        start_line: 18
        end_line: 28
        observation: "Bootstrap servers, consumer auto-offset-reset earliest, String/JSON serializers and deserializers, and spring.json.trusted.packages set to '*'."
        confidence: high
        original_line_range: {start_line: 18, end_line: 28, status: exact}
      - file: "source/inventory-service/src/main/resources/application-prod.yml"
        symbol: "spring.kafka.properties.security.protocol"
        start_line: 9
        end_line: 12
        observation: "Production bootstrap servers come from KAFKA_BOOTSTRAP_SERVERS and security.protocol defaults to PLAINTEXT when KAFKA_SECURITY_PROTOCOL is unset."
        confidence: high
        original_line_range: {start_line: 9, end_line: 12, status: exact}

  - id: azure-managed-redis
    classification: confirmed
    expected_status_from_context: required
    production_use_basis: spring_cache_abstraction_backed_by_redis
    evidence:
      - file: "source/inventory-service/pom.xml"
        symbol: "dependency org.springframework.boot:spring-boot-starter-data-redis"
        start_line: 12
        end_line: 13
        observation: "Spring Data Redis and Spring Cache starters are declared as compile dependencies."
        confidence: high
        original_line_range: {start_line: 12, end_line: 13, status: exact}
      - file: "source/inventory-service/src/main/resources/application.yml"
        symbol: "spring.data.redis.url and spring.cache.type"
        start_line: 13
        end_line: 17
        observation: "Redis URL defaults to redis://localhost:6379 through REDIS_URL and the Spring cache type is set to redis."
        confidence: high
        original_line_range: {start_line: 13, end_line: 17, status: exact}
      - file: "source/inventory-service/src/main/resources/application-prod.yml"
        symbol: "spring.data.redis.url"
        start_line: 6
        end_line: 8
        observation: "Production Redis URL is supplied entirely by REDIS_CONNECTION_STRING."
        confidence: high
        original_line_range: {start_line: 6, end_line: 8, status: exact}
      - file: "source/inventory-service/src/main/java/com/ecommerce/inventory/config/CacheConfig.java"
        symbol: "CacheConfig"
        start_line: 6
        end_line: 8
        observation: "@EnableCaching is declared with no RedisCacheManager, TTL, serializer, or error handler customization."
        confidence: high
        original_line_range: {start_line: 6, end_line: 8, status: exact}
      - file: "source/inventory-service/src/main/java/com/ecommerce/inventory/service/impl/InventoryServiceImpl.java"
        symbol: "@Cacheable and @CacheEvict on inventory cache"
        start_line: 30
        end_line: 36
        observation: "get(Long) is @Cacheable on cache name inventory keyed by id; update and delete are @CacheEvict on the same cache and key."
        confidence: high
        original_line_range: {start_line: 30, end_line: 36, status: exact}

  - id: keyvault
    classification: confirmed
    expected_status_from_context: required
    production_use_basis: spring_config_import_property_source_in_prod_profile
    evidence:
      - file: "source/inventory-service/pom.xml"
        symbol: "dependency com.azure.spring:spring-cloud-azure-starter-keyvault-secrets"
        start_line: 16
        end_line: 16
        observation: "Spring Cloud Azure Key Vault secrets starter is declared as a compile dependency."
        confidence: high
        original_line_range: {start_line: 16, end_line: 16, status: exact}
      - file: "source/inventory-service/src/main/resources/application-prod.yml"
        symbol: "spring.config.import"
        start_line: 2
        end_line: 3
        observation: "The prod profile imports azure-keyvault:${AZURE_KEYVAULT_ENDPOINT} as a Spring property source with no optional: prefix and no refresh configuration."
        confidence: high
        original_line_range: {start_line: 2, end_line: 3, status: exact}
      - file: "source/inventory-service/pom.xml"
        symbol: "dependencyManagement spring-cloud-azure-dependencies"
        start_line: 27
        end_line: 27
        observation: "Spring Cloud Azure BOM 5.18.0 governs the Key Vault starter version."
        confidence: high
        original_line_range: {start_line: 27, end_line: 27, status: exact}

  - id: jvm-runtime
    classification: confirmed
    expected_status_from_context: required
    production_use_basis: java_spring_boot_runtime_declared_in_build
    evidence:
      - file: "source/inventory-service/pom.xml"
        symbol: "project/properties/java.version"
        start_line: 6
        end_line: 6
        observation: "Java 17 is the declared runtime language level; the approved target runtime version is unknown in context."
        confidence: high
        original_line_range: {start_line: 6, end_line: 6, status: exact}
      - file: "source/inventory-service/pom.xml"
        symbol: "plugin spring-boot-maven-plugin"
        start_line: 28
        end_line: 28
        observation: "Spring Boot Maven plugin produces the executable artifact with no repository-visible JVM option customization."
        confidence: high
        original_line_range: {start_line: 28, end_line: 28, status: exact}
      - file: "source/inventory-service/src/main/resources/application.yml"
        symbol: "absence of spring.lifecycle.timeout-per-shutdown-phase and server.shutdown"
        start_line: 1
        end_line: 40
        observation: "No graceful shutdown, thread pool, or virtual thread properties are present in the default profile."
        confidence: high
        original_line_range: {start_line: 1, end_line: 40, status: exact}

  - id: appgateway-glb
    classification: confirmed
    expected_status_from_context: required
    production_use_basis: approved_platform_capability_expectation_plus_repository_probe_configuration
    confidence_note: Approved context declares this platform capability as required; repository evidence covers only the application-side probe contract.
    evidence:
      - file: "source/inventory-service/src/main/resources/application.yml"
        symbol: "management.endpoint.health.probes.enabled"
        start_line: 34
        end_line: 37
        observation: "Kubernetes-style probes are enabled, which exposes /actuator/health/readiness and /actuator/health/liveness."
        confidence: high
        original_line_range: {start_line: 34, end_line: 37, status: exact}
      - file: "source/inventory-service/src/main/resources/application.yml"
        symbol: "management.endpoints.web.exposure.include"
        start_line: 29
        end_line: 33
        observation: "Only health, info, and prometheus endpoints are exposed over HTTP."
        confidence: high
        original_line_range: {start_line: 29, end_line: 33, status: exact}
      - file: "source/inventory-service/src/main/resources/application.yml"
        symbol: "absence of server.forward-headers-strategy"
        start_line: 1
        end_line: 2
        observation: "No forwarded-header strategy is configured, so X-Forwarded-* headers from an upstream gateway are not honored by default."
        confidence: high
        original_line_range: {start_line: 1, end_line: 2, status: exact}
```

## Declared-Only Dependencies

```yaml
declared_only_dependencies:

  - id: http-client
    classification: declared_only
    registry_activation_note: The registry activates http-client on the spring-web inventory dependency, but no outbound HTTP client evidence exists in this repository.
    evidence:
      - file: "source/inventory-service/pom.xml"
        symbol: "dependency org.springframework.boot:spring-boot-starter-web"
        start_line: 8
        end_line: 8
        observation: "spring-boot-starter-web is declared and used for inbound REST endpoints only."
        confidence: high
        original_line_range: {start_line: 8, end_line: 8, status: exact}
      - file: "source/inventory-service/src/main"
        symbol: "repository-wide search for RestTemplate, WebClient, RestClient, FeignClient, HttpClient"
        start_line: 0
        end_line: 0
        observation: "No outbound HTTP client construction, builder, or invocation exists anywhere in production source."
        confidence: high
        original_line_range: {start_line: 0, end_line: 0, status: not_available}

  - id: springdoc-openapi
    classification: declared_only
    normalized_registry_key: not_applicable
    evidence:
      - file: "source/inventory-service/pom.xml"
        symbol: "dependency org.springdoc:springdoc-openapi-starter-webmvc-ui"
        start_line: 17
        end_line: 17
        observation: "SpringDoc OpenAPI UI is declared; application.yml sets springdoc.swagger-ui.path but no production code uses SpringDoc APIs."
        confidence: high
        original_line_range: {start_line: 17, end_line: 17, status: exact}
```

```yaml
absent_dependencies:
  note: Declared not_expected in approved context and not observed in the repository.
  - id: cosmosdb
    expected_status_from_context: not_expected
    repository_evidence: none_found
  - id: eventhubs
    expected_status_from_context: not_expected
    repository_evidence: none_found
  - id: storage-blob
    expected_status_from_context: not_expected
    repository_evidence: none_found
  - id: postgresql
    expected_status_from_context: not_expected
    repository_evidence: none_found
  - id: dse-cassandra
    expected_status_from_context: not_expected
    repository_evidence: none_found
  - id: azure-functions
    expected_status_from_context: not_expected
    repository_evidence: none_found
```

```yaml
expectation_evidence_gaps:
  note: Approved context declares these capabilities, but the enabled assessment domains contain no supporting repository evidence. These are evidence gaps, not findings.

  - id: apim
    expected_status_from_context: required
    repository_evidence: none_found
    searched_indicators:
      - Ocp-Apim-Subscription-Key
      - azure-api.net
      - WebClient.Builder
      - RestClient.Builder
      - FeignClient
    status: not_assessed
    reason: The service performs no outbound HTTP calls, so no APIM client behavior can be validated from repository evidence.

  - id: aks-istio
    expected_status_from_context: optional
    repository_evidence: out_of_enabled_scope
    observed_but_not_inventoried:
      - source/inventory-service/k8s/
    status: not_assessed
    reason: Kubernetes manifests are repository-owned but the deployment_configuration domain is disabled.
```

## Resilience Mechanisms

```yaml
resilience_mechanisms:

  retry:
    status: none_observed
    evidence:
      - file: "source/inventory-service/src/main"
        symbol: "repository-wide search for @Retryable, RetryTemplate, resilience4j, retry topic configuration"
        start_line: 0
        end_line: 0
        observation: "No retry annotation, retry template, retry topic, or backoff configuration exists in production source or configuration."
        confidence: high
        original_line_range: {start_line: 0, end_line: 0, status: not_available}

  timeouts:
    status: none_observed
    evidence:
      - file: "source/inventory-service/src/main/resources/application.yml"
        symbol: "absence of datasource, redis, and kafka timeout properties"
        start_line: 1
        end_line: 40
        observation: "No connection timeout, socket timeout, command timeout, request timeout, delivery timeout, or transaction timeout is configured for SQL, Redis, or Kafka."
        confidence: high
        original_line_range: {start_line: 1, end_line: 40, status: exact}

  circuit_breakers:
    status: none_observed
    evidence:
      - file: "source/inventory-service/pom.xml"
        symbol: "dependencies"
        start_line: 7
        end_line: 26
        observation: "No resilience4j, Spring Cloud Circuit Breaker, or Hystrix dependency is declared."
        confidence: high
        original_line_range: {start_line: 7, end_line: 26, status: exact}

  bulkheads_and_isolation:
    status: none_observed
    evidence:
      - file: "source/inventory-service/pom.xml"
        symbol: "dependencies"
        start_line: 7
        end_line: 26
        observation: "No bulkhead, thread pool isolation, or rate limiter library is declared, and no custom executor is defined in production source."
        confidence: high
        original_line_range: {start_line: 7, end_line: 26, status: exact}

  connection_pool_configuration:
    status: defaults_only
    evidence:
      - file: "source/inventory-service/src/main/resources/application.yml"
        symbol: "spring.datasource"
        start_line: 6
        end_line: 9
        observation: "Only url, username, and password are configured; HikariCP pool size, connection timeout, validation timeout, and max lifetime use framework defaults."
        confidence: high
        original_line_range: {start_line: 6, end_line: 9, status: exact}

  kafka_consumer_error_handling:
    status: defaults_only
    evidence:
      - file: "source/inventory-service/src/main/java/com/ecommerce/inventory/kafka/consumer/OrderEventConsumer.java"
        symbol: "OrderEventConsumer.consume"
        start_line: 13
        end_line: 21
        observation: "No CommonErrorHandler, DefaultErrorHandler, dead-letter topic, ack mode, or container factory customization is declared; the listener relies on Spring Kafka defaults."
        confidence: high
        original_line_range: {start_line: 13, end_line: 21, status: exact}
      - file: "source/inventory-service/src/main/java/com/ecommerce/inventory/kafka/consumer/OrderEventConsumer.java"
        symbol: "OrderEventConsumer.consume payload extraction"
        start_line: 15
        end_line: 18
        observation: "Event fields are read with String.valueOf and an unchecked (Number) cast on quantity with no null or type guard."
        confidence: high
        original_line_range: {start_line: 15, end_line: 18, status: exact}

  kafka_producer_delivery_handling:
    status: fire_and_forget
    evidence:
      - file: "source/inventory-service/src/main/java/com/ecommerce/inventory/kafka/producer/InventoryEventProducer.java"
        symbol: "InventoryEventProducer.publish"
        start_line: 14
        end_line: 16
        observation: "kafkaTemplate.send returns a CompletableFuture that is discarded; no callback, whenComplete handler, get, or failure logging is present."
        confidence: high
        original_line_range: {start_line: 14, end_line: 16, status: exact}
      - file: "source/inventory-service/src/main/resources/application.yml"
        symbol: "spring.kafka.producer"
        start_line: 26
        end_line: 28
        observation: "Only key and value serializers are configured; acks, retries, enable.idempotence, delivery.timeout.ms, and max.in.flight.requests.per.connection are not set."
        confidence: high
        original_line_range: {start_line: 26, end_line: 28, status: exact}

  cache_failure_handling:
    status: defaults_only
    evidence:
      - file: "source/inventory-service/src/main/java/com/ecommerce/inventory/config/CacheConfig.java"
        symbol: "CacheConfig"
        start_line: 6
        end_line: 8
        observation: "No CacheErrorHandler is registered, so Redis failures propagate through the Spring cache interceptor by default."
        confidence: high
        original_line_range: {start_line: 6, end_line: 8, status: exact}

  http_error_handling:
    status: present
    evidence:
      - file: "source/inventory-service/src/main/java/com/ecommerce/inventory/exception/GlobalExceptionHandler.java"
        symbol: "GlobalExceptionHandler"
        start_line: 12
        end_line: 22
        observation: "@RestControllerAdvice maps ResourceNotFoundException to 404 and IllegalArgumentException plus MethodArgumentNotValidException to 400; no handler exists for data access, optimistic locking, Redis, or Kafka exceptions."
        confidence: high
        original_line_range: {start_line: 12, end_line: 22, status: exact}
```

## Health and Traffic Eligibility

```yaml
health_and_traffic_eligibility:

  actuator_dependency:
    status: present
    evidence:
      - file: "source/inventory-service/pom.xml"
        symbol: "dependency org.springframework.boot:spring-boot-starter-actuator"
        start_line: 10
        end_line: 10
        observation: "Spring Boot Actuator starter is declared."
        confidence: high
        original_line_range: {start_line: 10, end_line: 10, status: exact}

  exposed_endpoints:
    value: [health, info, prometheus]
    evidence:
      - file: "source/inventory-service/src/main/resources/application.yml"
        symbol: "management.endpoints.web.exposure.include"
        start_line: 29
        end_line: 33
        observation: "Exposure list is health, info, prometheus."
        confidence: high
        original_line_range: {start_line: 29, end_line: 33, status: exact}

  probes:
    readiness_endpoint: enabled_by_probes_property
    liveness_endpoint: enabled_by_probes_property
    evidence:
      - file: "source/inventory-service/src/main/resources/application.yml"
        symbol: "management.endpoint.health.probes.enabled"
        start_line: 34
        end_line: 37
        observation: "probes.enabled is true, which activates the readiness and liveness health groups."
        confidence: high
        original_line_range: {start_line: 34, end_line: 37, status: exact}

  health_group_membership:
    status: defaults_only
    evidence:
      - file: "source/inventory-service/src/main/resources/application.yml"
        symbol: "absence of management.endpoint.health.group.readiness.include"
        start_line: 29
        end_line: 37
        observation: "No explicit readiness or liveness group include or exclude list is configured, so group membership uses framework defaults for the auto-configured SQL, Redis, and Kafka indicators."
        confidence: high
        original_line_range: {start_line: 29, end_line: 37, status: exact}

  custom_health_indicators:
    status: none_observed
    evidence:
      - file: "source/inventory-service/src/main"
        symbol: "repository-wide search for HealthIndicator, AbstractHealthIndicator, ReactiveHealthIndicator"
        start_line: 0
        end_line: 0
        observation: "No custom health indicator class exists in production source."
        confidence: high
        original_line_range: {start_line: 0, end_line: 0, status: not_available}

  readiness_state_control:
    status: none_observed
    evidence:
      - file: "source/inventory-service/src/main"
        symbol: "repository-wide search for AvailabilityChangeEvent and ReadinessState"
        start_line: 0
        end_line: 0
        observation: "No application code publishes AvailabilityChangeEvent or manipulates ReadinessState to withdraw regional traffic eligibility."
        confidence: high
        original_line_range: {start_line: 0, end_line: 0, status: not_available}

  forwarded_header_handling:
    status: none_observed
    evidence:
      - file: "source/inventory-service/src/main/resources/application.yml"
        symbol: "absence of server.forward-headers-strategy"
        start_line: 1
        end_line: 2
        observation: "Neither server.forward-headers-strategy nor a ForwardedHeaderFilter bean is configured."
        confidence: high
        original_line_range: {start_line: 1, end_line: 2, status: exact}
```

## State and Consistency

```yaml
state_and_consistency:

  authoritative_state_store:
    value: azure-sql
    role: authoritative_business_state
    evidence:
      - file: "source/inventory-service/src/main/java/com/ecommerce/inventory/model/InventoryItem.java"
        symbol: "InventoryItem"
        start_line: 17
        end_line: 27
        observation: "Single JPA entity holding productId, availableQuantity, reservedQuantity, updatedAt, and an @Version column, with a unique constraint on productId."
        confidence: high
        original_line_range: {start_line: 17, end_line: 27, status: exact}

  optimistic_locking:
    status: present
    evidence:
      - file: "source/inventory-service/src/main/java/com/ecommerce/inventory/model/InventoryItem.java"
        symbol: "@Version private long version"
        start_line: 26
        end_line: 26
        observation: "JPA optimistic locking version column is declared; no ObjectOptimisticLockingFailureException handling exists in the service or the global exception handler."
        confidence: high
        original_line_range: {start_line: 26, end_line: 26, status: exact}

  pessimistic_locking:
    status: none_observed
    evidence:
      - file: "source/inventory-service/src/main/java/com/ecommerce/inventory/repository/InventoryRepository.java"
        symbol: "InventoryRepository"
        start_line: 8
        end_line: 11
        observation: "No @Lock, @Query with FOR UPDATE, or LockModeType is declared on any repository method."
        confidence: high
        original_line_range: {start_line: 8, end_line: 11, status: exact}

  transaction_boundaries:
    status: present
    evidence:
      - file: "source/inventory-service/src/main/java/com/ecommerce/inventory/service/impl/InventoryServiceImpl.java"
        symbol: "@Transactional on create, update, delete, reserve, release"
        start_line: 25
        end_line: 45
        observation: "Mutating service methods are annotated @Transactional with default propagation, isolation, timeout, and rollback rules; get and list are not transactional."
        confidence: high
        original_line_range: {start_line: 25, end_line: 45, status: exact}

  transaction_and_event_publication_coupling:
    status: publish_inside_transaction
    evidence:
      - file: "source/inventory-service/src/main/java/com/ecommerce/inventory/service/impl/InventoryServiceImpl.java"
        symbol: "InventoryServiceImpl.saveAndPublish"
        start_line: 51
        end_line: 51
        observation: "repository.save followed by producer.publish executes inside the same @Transactional method, so the Kafka send is issued before the database transaction commits and is not coordinated with commit or rollback."
        confidence: high
        original_line_range: {start_line: 51, end_line: 51, status: exact}
      - file: "source/inventory-service/src/main/java/com/ecommerce/inventory/service/impl/InventoryServiceImpl.java"
        symbol: "InventoryServiceImpl.delete"
        start_line: 35
        end_line: 36
        observation: "delete removes the entity and publishes INVENTORY_DELETED inside the same transaction with no transactional outbox or after-commit hook."
        confidence: high
        original_line_range: {start_line: 35, end_line: 36, status: exact}

  outbox_pattern:
    status: none_observed
    evidence:
      - file: "source/inventory-service/src/main/java"
        symbol: "repository-wide search for outbox, TransactionalEventListener, AFTER_COMMIT"
        start_line: 0
        end_line: 0
        observation: "No outbox table, no @TransactionalEventListener, and no after-commit publication mechanism exists."
        confidence: high
        original_line_range: {start_line: 0, end_line: 0, status: not_available}

  idempotency:
    status: none_observed
    evidence:
      - file: "source/inventory-service/src/main/java/com/ecommerce/inventory/kafka/consumer/OrderEventConsumer.java"
        symbol: "OrderEventConsumer.consume"
        start_line: 19
        end_line: 20
        observation: "ORDER_CREATED unconditionally calls reserve and ORDER_CANCELLED unconditionally calls release; the orderId is passed through as referenceId but is never used for deduplication, processed-event lookup, or conditional update."
        confidence: high
        original_line_range: {start_line: 19, end_line: 20, status: exact}
      - file: "source/inventory-service/src/main/java/com/ecommerce/inventory/service/impl/InventoryServiceImpl.java"
        symbol: "InventoryServiceImpl.reserve and InventoryServiceImpl.release"
        start_line: 37
        end_line: 50
        observation: "reserve and release apply relative quantity deltas with no stable operation identity, no reservation record keyed by referenceId, and no duplicate-detection guard."
        confidence: high
        original_line_range: {start_line: 37, end_line: 50, status: exact}

  cache_consistency:
    status: partial
    evidence:
      - file: "source/inventory-service/src/main/java/com/ecommerce/inventory/service/impl/InventoryServiceImpl.java"
        symbol: "@Cacheable get and @CacheEvict update/delete"
        start_line: 30
        end_line: 36
        observation: "The inventory cache is keyed by entity id and evicted only on update and delete; reserve and release mutate quantities by productId without evicting the id-keyed cache entry."
        confidence: high
        original_line_range: {start_line: 30, end_line: 36, status: exact}
      - file: "source/inventory-service/src/main/resources/application.yml"
        symbol: "spring.cache"
        start_line: 16
        end_line: 17
        observation: "Cache type is redis with no TTL, null-value policy, key prefix, or per-cache configuration."
        confidence: high
        original_line_range: {start_line: 16, end_line: 17, status: exact}

  schema_management:
    value: hibernate_ddl_auto_update
    evidence:
      - file: "source/inventory-service/src/main/resources/application.yml"
        symbol: "spring.jpa.hibernate.ddl-auto"
        start_line: 10
        end_line: 12
        observation: "ddl-auto is set to update in the default profile and is not overridden in the prod profile; no Flyway or Liquibase dependency is declared."
        confidence: high
        original_line_range: {start_line: 10, end_line: 12, status: exact}

  http_session_state:
    status: stateless
    evidence:
      - file: "source/inventory-service/src/main/java/com/ecommerce/inventory/controller/InventoryController.java"
        symbol: "InventoryController"
        start_line: 14
        end_line: 24
        observation: "No HttpSession, session scope, or spring-session dependency is used; all endpoints are stateless request/response."
        confidence: high
        original_line_range: {start_line: 14, end_line: 24, status: exact}

  regional_state_awareness:
    status: none_observed
    evidence:
      - file: "source/inventory-service/src/main/resources/application.yml"
        symbol: "repository-wide search for region, preferred region, and regional endpoint selection"
        start_line: 1
        end_line: 40
        observation: "No region property, region-aware endpoint selection, or preferred-write-region configuration is present in any in-scope configuration file or production class."
        confidence: high
        original_line_range: {start_line: 1, end_line: 40, status: exact}
```

## Lifecycle and Recovery

```yaml
lifecycle_and_recovery:

  graceful_shutdown:
    status: none_observed
    evidence:
      - file: "source/inventory-service/src/main/resources/application.yml"
        symbol: "absence of server.shutdown and spring.lifecycle.timeout-per-shutdown-phase"
        start_line: 1
        end_line: 40
        observation: "Neither server.shutdown: graceful nor spring.lifecycle.timeout-per-shutdown-phase is configured in the default profile."
        confidence: high
        original_line_range: {start_line: 1, end_line: 40, status: exact}
      - file: "source/inventory-service/src/main/resources/application-prod.yml"
        symbol: "absence of shutdown configuration"
        start_line: 1
        end_line: 12
        observation: "The prod profile adds only Key Vault import, datasource URL, Redis URL, and Kafka settings; no shutdown configuration is present."
        confidence: high
        original_line_range: {start_line: 1, end_line: 12, status: exact}

  lifecycle_hooks:
    status: none_observed
    evidence:
      - file: "source/inventory-service/src/main/java"
        symbol: "repository-wide search for @PreDestroy, SmartLifecycle, DisposableBean, ApplicationListener"
        start_line: 0
        end_line: 0
        observation: "No production class implements a shutdown, drain, or lifecycle callback."
        confidence: high
        original_line_range: {start_line: 0, end_line: 0, status: not_available}

  kafka_consumer_offset_handling:
    status: defaults_only
    evidence:
      - file: "source/inventory-service/src/main/resources/application.yml"
        symbol: "spring.kafka.consumer.auto-offset-reset"
        start_line: 20
        end_line: 25
        observation: "auto-offset-reset is earliest; enable.auto.commit, ack-mode, max.poll.records, max.poll.interval.ms, and session.timeout.ms are not configured."
        confidence: high
        original_line_range: {start_line: 20, end_line: 25, status: exact}

  kafka_listener_container_control:
    status: none_observed
    evidence:
      - file: "source/inventory-service/src/main/java/com/ecommerce/inventory/kafka/consumer/OrderEventConsumer.java"
        symbol: "@KafkaListener"
        start_line: 13
        end_line: 13
        observation: "The listener has no id, no autoStartup control, and no containerFactory reference, so it cannot be started or stopped to move processing ownership between regions."
        confidence: high
        original_line_range: {start_line: 13, end_line: 13, status: exact}

  startup_dependency_behavior:
    status: fail_fast_on_missing_property
    evidence:
      - file: "source/inventory-service/src/main/resources/application-prod.yml"
        symbol: "spring.config.import azure-keyvault"
        start_line: 2
        end_line: 3
        observation: "The Key Vault import is mandatory rather than optional, so an unavailable Key Vault endpoint prevents application startup."
        confidence: high
        original_line_range: {start_line: 2, end_line: 3, status: exact}
      - file: "source/inventory-service/src/main/resources/application.yml"
        symbol: "spring.datasource.username and spring.datasource.password"
        start_line: 8
        end_line: 9
        observation: "SQL_USERNAME and SQL_PASSWORD are required placeholders with no defaults in the default profile."
        confidence: high
        original_line_range: {start_line: 8, end_line: 9, status: exact}

  secret_refresh:
    status: none_observed
    evidence:
      - file: "source/inventory-service/src/main/resources/application-prod.yml"
        symbol: "spring.config.import"
        start_line: 2
        end_line: 3
        observation: "Key Vault secrets are resolved once at startup; no refresh interval, @RefreshScope, or credential rotation handling is configured."
        confidence: high
        original_line_range: {start_line: 2, end_line: 3, status: exact}

  compensation_and_replay:
    status: none_observed
    evidence:
      - file: "source/inventory-service/src/main/java/com/ecommerce/inventory/service/impl/InventoryServiceImpl.java"
        symbol: "InventoryServiceImpl"
        start_line: 20
        end_line: 55
        observation: "No compensating action, reconciliation job, replay guard, or recovery path exists for partially applied reserve or release operations."
        confidence: high
        original_line_range: {start_line: 20, end_line: 55, status: exact}
```

## Observability

```yaml
observability:

  metrics:
    status: present
    evidence:
      - file: "source/inventory-service/pom.xml"
        symbol: "dependency io.micrometer:micrometer-registry-prometheus"
        start_line: 18
        end_line: 18
        observation: "Micrometer Prometheus registry is declared."
        confidence: high
        original_line_range: {start_line: 18, end_line: 18, status: exact}
      - file: "source/inventory-service/src/main/resources/application.yml"
        symbol: "management.endpoints.web.exposure.include"
        start_line: 33
        end_line: 33
        observation: "The prometheus endpoint is exposed over HTTP."
        confidence: high
        original_line_range: {start_line: 33, end_line: 33, status: exact}

  common_metric_tags:
    status: none_observed
    evidence:
      - file: "source/inventory-service/src/main/resources/application.yml"
        symbol: "absence of management.metrics.tags"
        start_line: 29
        end_line: 37
        observation: "No common metric tags are configured, so emitted metrics carry no region, instance, or deployment dimension."
        confidence: high
        original_line_range: {start_line: 29, end_line: 37, status: exact}

  structured_logging:
    status: present
    evidence:
      - file: "source/inventory-service/src/main/resources/logback-spring.xml"
        symbol: "LogstashEncoder console appender"
        start_line: 1
        end_line: 1
        observation: "A single console appender uses net.logstash.logback.encoder.LogstashEncoder at root level INFO with no MDC, custom fields, or region field."
        confidence: high
        original_line_range: {start_line: 1, end_line: 1, status: exact}
      - file: "source/inventory-service/pom.xml"
        symbol: "dependency net.logstash.logback:logstash-logback-encoder"
        start_line: 19
        end_line: 19
        observation: "Logstash Logback encoder version 8.0 is declared."
        confidence: high
        original_line_range: {start_line: 19, end_line: 19, status: exact}

  application_logging:
    status: none_observed
    evidence:
      - file: "source/inventory-service/src/main/java"
        symbol: "repository-wide search for Logger, @Slf4j, log."
        start_line: 0
        end_line: 0
        observation: "No production class declares a logger; failures in the Kafka consumer, producer, cache, or service layer produce no application log statements."
        confidence: high
        original_line_range: {start_line: 0, end_line: 0, status: not_available}

  distributed_tracing:
    status: none_observed
    evidence:
      - file: "source/inventory-service/pom.xml"
        symbol: "dependencies"
        start_line: 7
        end_line: 26
        observation: "No micrometer-tracing, OpenTelemetry, or Application Insights dependency is declared."
        confidence: high
        original_line_range: {start_line: 7, end_line: 26, status: exact}

  correlation_identifier_propagation:
    status: none_observed
    evidence:
      - file: "source/inventory-service/src/main/java/com/ecommerce/inventory/kafka/producer/InventoryEventProducer.java"
        symbol: "InventoryEventProducer.publish"
        start_line: 14
        end_line: 16
        observation: "Published events carry type, occurredAt, referenceId, and inventory payload; no correlation identifier, trace context, message identity, or region attribute is set, and no Kafka headers are written."
        confidence: high
        original_line_range: {start_line: 14, end_line: 16, status: exact}

  regional_telemetry:
    status: none_observed
    evidence:
      - file: "source/inventory-service/src/main/resources"
        symbol: "repository-wide search for region tagging in logging and metrics configuration"
        start_line: 0
        end_line: 0
        observation: "No region identifier is attached to logs, metrics, or events, so per-region behavior cannot be distinguished in telemetry."
        confidence: high
        original_line_range: {start_line: 0, end_line: 0, status: not_available}
```

## Test Coverage

```yaml
test_coverage:

  unit_tests:
    count: 1
    evidence:
      - file: "source/inventory-service/src/test/java/com/ecommerce/inventory/service/InventoryServiceImplTest.java"
        symbol: "InventoryServiceImplTest.reservesAvailableStockAndPublishesEvent"
        start_line: 21
        end_line: 30
        observation: "A single Mockito unit test verifies the happy-path reserve flow and event publication."
        confidence: high
        original_line_range: {start_line: 21, end_line: 30, status: advisory}

  integration_tests:
    count: 1
    evidence:
      - file: "source/inventory-service/src/test/java/com/ecommerce/inventory/InventoryIntegrationTest.java"
        symbol: "InventoryIntegrationTest.contextLoads"
        start_line: 12
        end_line: 22
        observation: "A @SpringBootTest with Testcontainers MSSQL and @EmbeddedKafka asserts only that the application context loads."
        confidence: high
        original_line_range: {start_line: 12, end_line: 22, status: advisory}

  test_dependencies:
    evidence:
      - file: "source/inventory-service/pom.xml"
        symbol: "test-scoped dependencies"
        start_line: 22
        end_line: 26
        observation: "spring-boot-starter-test, spring-kafka-test, testcontainers junit-jupiter, and testcontainers mssqlserver are declared with test scope."
        confidence: high
        original_line_range: {start_line: 22, end_line: 26, status: exact}

  fault_and_failover_tests:
    status: none_observed
    evidence:
      - file: "source/inventory-service/src/test/java"
        symbol: "repository-wide search for fault injection, failover, retry, timeout, duplicate-delivery, and optimistic-locking tests"
        start_line: 0
        end_line: 0
        observation: "No test exercises broker unavailability, database failover, Redis unavailability, duplicate event delivery, concurrent reservation conflict, or graceful shutdown."
        confidence: high
        original_line_range: {start_line: 0, end_line: 0, status: not_available}

  untested_production_paths:
    - InventoryServiceImpl.create
    - InventoryServiceImpl.get
    - InventoryServiceImpl.list
    - InventoryServiceImpl.update
    - InventoryServiceImpl.delete
    - InventoryServiceImpl.release
    - OrderEventConsumer.consume
    - InventoryEventProducer.publish
    - GlobalExceptionHandler
```

## Historical PCF References

```yaml
historical_pcf_references:
  status: none_found
  informational_only: true
  pcf_findings_allowed: false
  searched_indicators:
    - manifest.yml
    - cloudfoundry
    - VCAP_
    - cfenv
    - pivotal
  evidence:
    - file: "source/inventory-service"
      symbol: "repository-wide search for Cloud Foundry artifacts and environment variables"
      start_line: 0
      end_line: 0
      observation: "No Cloud Foundry manifest, buildpack reference, VCAP environment binding, or PCF documentation reference exists in the repository."
      confidence: high
      original_line_range: {start_line: 0, end_line: 0, status: not_available}
```

## Uncertainties

```yaml
repository_observed_interactions:
  evidence_scope: repository_observed

  inbound_contracts:
    - type: http_rest
      path: "/api/v1/inventory"
      operations: [POST, "GET /{id}", GET, "PUT /{id}", "DELETE /{id}", "POST /products/{productId}/reserve", "POST /products/{productId}/release"]
      port: 8082
      evidence_file: "source/inventory-service/src/main/java/com/ecommerce/inventory/controller/InventoryController.java"
    - type: http_actuator
      path: "/actuator/health, /actuator/info, /actuator/prometheus"
      evidence_file: "source/inventory-service/src/main/resources/application.yml"

  direct_outbound_dependencies:
    - id: azure-sql
      mechanism: jdbc_via_spring_data_jpa
      endpoint_source: "SQL_CONNECTION_STRING (prod), SQL_URL (default)"
    - id: azure-managed-redis
      mechanism: spring_cache_abstraction
      endpoint_source: "REDIS_CONNECTION_STRING (prod), REDIS_URL (default)"
    - id: confluent-kafka
      mechanism: kafka_template_producer
      endpoint_source: "KAFKA_BOOTSTRAP_SERVERS"
    - id: keyvault
      mechanism: spring_config_import_property_source
      endpoint_source: "AZURE_KEYVAULT_ENDPOINT"

  produced_events:
    - topic: inventory-events
      key: productId
      event_types: [INVENTORY_CREATED, INVENTORY_UPDATED, INVENTORY_DELETED, INVENTORY_RESERVED, INVENTORY_RELEASED]
      payload_shape: "Map with type, occurredAt, referenceId, inventory"
      evidence_file: "source/inventory-service/src/main/java/com/ecommerce/inventory/kafka/producer/InventoryEventProducer.java"

  consumed_events:
    - topic: order-events
      consumer_group: inventory-service
      handled_types: [ORDER_CREATED, ORDER_CANCELLED]
      evidence_file: "source/inventory-service/src/main/java/com/ecommerce/inventory/kafka/consumer/OrderEventConsumer.java"

  scheduled_workloads: []

  direct_state_stores:
    - id: azure-sql
      role: authoritative_business_state
      table: inventory_items
    - id: azure-managed-redis
      role: cache
      cache_name: inventory

  direct_secret_sources:
    - id: keyvault
      mechanism: "spring.config.import: azure-keyvault:${AZURE_KEYVAULT_ENDPOINT}"
      profile: prod
    - id: environment_variables
      values: [SQL_USERNAME, SQL_PASSWORD]
      profile: default

  unresolved_endpoint_aliases:
    - SQL_CONNECTION_STRING
    - REDIS_CONNECTION_STRING
    - KAFKA_BOOTSTRAP_SERVERS
    - KAFKA_SECURITY_PROTOCOL
    - AZURE_KEYVAULT_ENDPOINT
```

```yaml
uncertainties:

  - id: UNC-001
    area: azure_sql_connectivity
    description: >-
      The approved target connectivity contract requires a failover group read-write listener for JDBC,
      but the production datasource URL is supplied entirely through SQL_CONNECTION_STRING, so the
      repository cannot demonstrate whether a listener DNS name or a direct regional server endpoint is used.
    repository_evidence: "source/inventory-service/src/main/resources/application-prod.yml lines 4-5"
    resolution_source: external_evidence_required
    required_input:
      - Approved failover group listener DNS name
      - Resolved value of SQL_CONNECTION_STRING in each target region
      - Database membership in the failover group
    downstream_action: assess_with_evidence_gap

  - id: UNC-002
    area: kafka_deployed_topology
    description: >-
      The approved context declares independent regional Kafka clusters with cluster_per_region true and
      stretched_cluster false. Repository evidence contains only a bootstrap-servers placeholder and cannot
      confirm deployed cluster topology, cluster linking, topic replication, or consumer-offset replication.
    repository_evidence: "source/inventory-service/src/main/resources/application-prod.yml lines 9-10"
    resolution_source: external_evidence_required
    downstream_action: treat_deployed_topology_as_unresolved_infrastructure_fact

  - id: UNC-003
    area: kafka_security_protocol
    description: >-
      Production Kafka security.protocol falls back to PLAINTEXT when KAFKA_SECURITY_PROTOCOL is unset,
      and no SASL, SSL, or schema registry configuration exists in the repository.
    repository_evidence: "source/inventory-service/src/main/resources/application-prod.yml lines 11-12"
    resolution_source: repository_observed_with_deployment_confirmation_required
    downstream_action: assess_configuration_evidence_in_enabled_scope

  - id: UNC-004
    area: regional_processing_ownership
    description: >-
      The approved Kafka target declares single_active regional processing, but the @KafkaListener has no id
      and no autoStartup control, so the repository provides no mechanism to enable or disable consumption per region.
      Whether the standby region's listener is prevented from consuming is not determinable from the repository.
    repository_evidence: "source/inventory-service/src/main/java/com/ecommerce/inventory/kafka/consumer/OrderEventConsumer.java line 13"
    resolution_source: repository_observed_gap_plus_deployment_confirmation
    downstream_action: assess_against_target_kafka_scenario

  - id: UNC-005
    area: apim_capability_expectation
    description: >-
      The approved context declares apim as a required platform capability, but the service makes no outbound
      HTTP calls, so no APIM client behavior can be validated from repository evidence.
    repository_evidence: none_found
    resolution_source: architecture_clarification_required
    downstream_action: not_assessed

  - id: UNC-006
    area: runtime_and_container_configuration
    description: >-
      The approved runtime target requires container awareness, bounded heap strategy, graceful shutdown, and
      readiness withdrawal. Container entrypoint and JVM options live in the disabled container_build domain,
      and Kubernetes probe, resource limit, and termination grace configuration lives in the disabled
      deployment_configuration domain, so only application-level evidence is available.
    repository_evidence: "source/inventory-service/pom.xml line 6 and source/inventory-service/src/main/resources/application.yml"
    resolution_source: scope_limited
    downstream_action: assess_application_level_evidence_only

  - id: UNC-007
    area: aks_istio_capability_expectation
    description: >-
      The approved context marks aks-istio as optional and declares execution_platform aks. Repository-owned
      Kubernetes manifests exist under source/inventory-service/k8s/ but the deployment_configuration domain
      is disabled, so no mesh or deployment evidence was inventoried.
    repository_evidence: out_of_enabled_scope
    resolution_source: scope_limited
    downstream_action: not_assessed

  - id: UNC-008
    area: schema_governance
    description: >-
      Events are published as untyped Map payloads with spring.json.trusted.packages set to '*' and no schema
      registry configuration. Whether a governed schema contract applies to inventory-events and order-events
      is not determinable from the repository.
    repository_evidence: "source/inventory-service/src/main/resources/application.yml lines 18-28"
    resolution_source: architecture_clarification_required
    downstream_action: assess_configuration_evidence_in_enabled_scope

  - id: UNC-009
    area: redis_operating_model
    description: >-
      The approved context sets the azure-managed-redis target operating model to active_active, but the
      repository supplies only a single REDIS_CONNECTION_STRING with no region awareness, no TTL, and no
      cache error handler. Deployed Redis topology is not determinable from the repository.
    repository_evidence: "source/inventory-service/src/main/resources/application-prod.yml lines 6-8"
    resolution_source: external_evidence_required
    downstream_action: assess_application_compatibility_only
```

```yaml
architecture_conflict:
  detected: false
  affected_area: not_applicable
  context_source: not_applicable
  context_declaration: not_applicable
  repository_evidence: []
  policy_evidence: []
  resolution_status: not_applicable
  assessment_action:
    common_controls: evaluate_when_evidence_available
    scenario_specific_controls: evaluate_when_evidence_available
    code_finding_created_for_conflict: false
    route_to: not_applicable
```

```yaml
dependency_standard_gaps: []
```

## Dependency Standards to Load

```yaml
supplied_architecture_context:
  context_status: provided
  source_path: application-context/application-architecture-context.yml
  context_id: not_applicable
  context_version: "3.0.0"
  lifecycle_status: approved
  kafka_declared_scenario: active_standby
```

```yaml
kafka_scenario_inputs:
  confluent_kafka:
    used_by_production_code: true
    interaction_types: [producer, consumer]
    evidence:
      - "source/inventory-service/src/main/java/com/ecommerce/inventory/kafka/producer/InventoryEventProducer.java lines 13-16"
      - "source/inventory-service/src/main/java/com/ecommerce/inventory/kafka/consumer/OrderEventConsumer.java lines 13-21"

  application_database:
    used_by_production_code: true
    evidence_basis:
      - "JPA entity InventoryItem at source/inventory-service/src/main/java/com/ecommerce/inventory/model/InventoryItem.java lines 17-27"
      - "Spring Data JPA repository at source/inventory-service/src/main/java/com/ecommerce/inventory/repository/InventoryRepository.java lines 8-11"

  azure_sql:
    used_by_production_code: true
    role: authoritative_business_state
    evidence:
      - "source/inventory-service/pom.xml line 15 declares mssql-jdbc"
      - "source/inventory-service/src/main/resources/application.yml line 7 sets a jdbc:sqlserver datasource URL"
      - "source/inventory-service/src/main/java/com/ecommerce/inventory/service/impl/InventoryServiceImpl.java lines 25-51 perform transactional writes"

  cosmos_db:
    used_by_production_code: false
    api: unknown
    throughput_model: unknown
    role: not_applicable
    multi_region_write_evidence:
      status: not_applicable
      indicators: []
    evidence: []

  other_databases: []

  processing_model:
    value: mixed
    evidence:
      - "OrderEventConsumer consumes order-events and mutates authoritative SQL state"
      - "InventoryEventProducer publishes inventory-events after each state change"
      - "InventoryController exposes synchronous REST write paths against the same state"

  regional_processing_model:
    value: single_active
    evidence:
      - "Approved context kafka_operating_model.target.regional_processing_model is single_active"
      - "Repository contains no region selection, listener enablement control, or partition ownership logic"

  external_side_effects:
    value: none
    evidence:
      - "Approved context external_side_effects.present is false"
      - "Production source performs no outbound HTTP, email, SMS, payment, or partner API call"

  kafka_backed_state:
    value: none
    evidence:
      - "No Kafka Streams dependency, state store, or compacted topic usage exists in production source"

  kafka_cluster_model:
    value: independent_regional_clusters
    evidence_status: approved_application_context
    evidence:
      - "architecture_context.kafka_operating_model.target.cluster_model.type is independent_regional_clusters with stretched_cluster false and cluster_per_region true"
```

```yaml
kafka_operating_scenario:
  value: active_standby

  declaration:
    source_type: approved_application_architecture_context
    source_path: application-context/application-architecture-context.yml
    context_id: not_applicable
    context_version: "3.0.0"
    approval_status: approved

  policy_validation:
    policy_id: KAFKA-OPERATING-SCENARIO
    policy_version: "3.2.0"
    rule_id: KAFKA-SCENARIO-001
    status: consistent

  repository_validation:
    status: consistent
    observed_dependencies:
      - confluent-kafka
      - azure-sql
      - azure-managed-redis
      - keyvault
    conflicting_evidence: []

  processing_model: mixed

  regional_processing_model:
    value: single_active
    evidence_status: approved_context

  external_side_effects: none
  kafka_backed_state: none
  architecture_confirmation_required: false
  conditional_assumptions: []
  unresolved_infrastructure_facts:
    - Deployed Kafka cluster topology per region
    - Cluster Linking and Schema Linking configuration
    - Cross-region topic, schema, ACL, and consumer-offset replication
    - Azure SQL failover group deployment and listener DNS name
    - Azure Managed Redis deployed regional topology
    - Regional Kafka role assignment and standby consumption control
```

```yaml
dependency_standards_to_load:

  - id: azure-sql
    grounding_file: grounding/dependencies/springboot-azure-sql.md
    standard_version: "2.3.0"
    registry_type: dependency_standard

  - id: confluent-kafka
    grounding_file: grounding/dependencies/springboot-confluent-kafka.md
    standard_version: "3.1.0"
    registry_type: scenario_aware_dependency_standard
    operating_scenario: active_standby
    scenario_source: approved_application_architecture_context
    scenario_rule_id: KAFKA-SCENARIO-001
    scenario_validation_status: consistent
    architecture_confirmation_required: false

  - id: azure-managed-redis
    grounding_file: grounding/dependencies/springboot-azure-managed-redis.md
    standard_version: "2.2.0"
    registry_type: dependency_standard

  - id: keyvault
    grounding_file: grounding/dependencies/springboot-keyvault.md
    standard_version: "2.2.0"
    registry_type: dependency_standard

  - id: jvm-runtime
    grounding_file: grounding/dependencies/jvm-runtime-resiliency.md
    standard_version: "1.0.0"
    registry_type: dependency_standard

  - id: appgateway-glb
    grounding_file: grounding/dependencies/springboot-appgateway-glb.md
    standard_version: "2.2.0"
    registry_type: dependency_standard
```

```yaml
assessment_domain_standards_to_load: []
```

```yaml
assessment_domain_standards_not_loaded:
  - id: container-build-resiliency
    assessment_domain: container_build
    reason: domain_disabled
  - id: cicd-pipeline-resiliency
    assessment_domain: cicd_pipeline
    reason: domain_disabled
  - id: kubernetes-deployment-resiliency
    assessment_domain: deployment_configuration
    reason: domain_disabled
  - id: helm-kustomize-resiliency
    assessment_domain: deployment_configuration
    reason: domain_disabled
```

## Inventory Summary

```yaml
inventory_summary:
  repository_root: source/inventory-service
  assessment_boundary: single_microservice_repository
  boundary_exceptions: []
  files_examined_in_scope: 22
  files_examined_breakdown:
    build: 1
    production_java: 15
    configuration: 3
    test_java: 2
    documentation: 1
  confirmed_dependency_count: 6
  declared_only_dependency_count: 2
  dependency_standards_to_load_count: 6
  assessment_domain_standards_to_load_count: 0
  dependency_standard_gap_count: 0
  uncertainty_count: 9
  architecture_conflict_count: 0
  pcf_reference_count: 0
  kafka_scenario: active_standby
  kafka_scenario_validation_status: consistent
  authoritative_state: azure-sql
  current_deployment_operating_model: active_standby
  approved_target_deployment_operating_model: active_active
  assessment_target_state: approved_target
```

```yaml
files_examined:
  - source/inventory-service/pom.xml
  - source/inventory-service/README.md
  - source/inventory-service/src/main/resources/application.yml
  - source/inventory-service/src/main/resources/application-prod.yml
  - source/inventory-service/src/main/resources/logback-spring.xml
  - source/inventory-service/src/main/java/com/ecommerce/inventory/InventoryServiceApplication.java
  - source/inventory-service/src/main/java/com/ecommerce/inventory/controller/InventoryController.java
  - source/inventory-service/src/main/java/com/ecommerce/inventory/service/InventoryService.java
  - source/inventory-service/src/main/java/com/ecommerce/inventory/service/impl/InventoryServiceImpl.java
  - source/inventory-service/src/main/java/com/ecommerce/inventory/repository/InventoryRepository.java
  - source/inventory-service/src/main/java/com/ecommerce/inventory/model/InventoryItem.java
  - source/inventory-service/src/main/java/com/ecommerce/inventory/mapper/InventoryMapper.java
  - source/inventory-service/src/main/java/com/ecommerce/inventory/config/CacheConfig.java
  - source/inventory-service/src/main/java/com/ecommerce/inventory/dto/InventoryRequest.java
  - source/inventory-service/src/main/java/com/ecommerce/inventory/dto/InventoryResponse.java
  - source/inventory-service/src/main/java/com/ecommerce/inventory/dto/StockAdjustmentRequest.java
  - source/inventory-service/src/main/java/com/ecommerce/inventory/exception/GlobalExceptionHandler.java
  - source/inventory-service/src/main/java/com/ecommerce/inventory/exception/ResourceNotFoundException.java
  - source/inventory-service/src/main/java/com/ecommerce/inventory/kafka/producer/InventoryEventProducer.java
  - source/inventory-service/src/main/java/com/ecommerce/inventory/kafka/consumer/OrderEventConsumer.java
  - source/inventory-service/src/test/java/com/ecommerce/inventory/service/InventoryServiceImplTest.java
  - source/inventory-service/src/test/java/com/ecommerce/inventory/InventoryIntegrationTest.java
```

```yaml
files_excluded:
  - path: source/inventory-service/target/
    reason: generated_build_output
  - path: source/inventory-service/Dockerfile
    reason: container_build_domain_disabled
  - path: source/inventory-service/.github/workflows/ci-cd.yml
    reason: cicd_pipeline_domain_disabled
  - path: source/inventory-service/k8s/
    reason: deployment_configuration_domain_disabled
```

## Evaluation Handoff Contract

```yaml
handoff:
  artifact_role: authoritative_inventory
  next_phase: evaluation
  next_agent: task-reviewer
  re_inventory_allowed: false
  source_validation_mode: cited_evidence_only
  missing_evidence_status: not_assessed
  infrastructure_assessment_allowed: false
  pcf_findings_allowed: false
```
