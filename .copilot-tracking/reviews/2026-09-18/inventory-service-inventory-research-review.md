# Inventory Service Assessment Review

## Assessment Execution

```yaml
assessment_execution:
  inventory_artifact: ".copilot-tracking/research/2026-09-18/inventory-service-inventory-research.md"
  inventory_agent: task-researcher
  evaluator_agent: task-reviewer
  assessment_run_id: "inventory-service-2026-09-18-001"
  phase: assessment
  phase_order: "02"
  re_inventory_performed: false
  researcher_invoked_during_evaluation: false
  targeted_evidence_validation_performed: true
  source_code_modified: false
  standards_loaded:
    - id: springboot-aks-active-active-master
      path: grounding/master/springboot-aks-active-active-master.md
      version: "4.0.0"
      control_count: 86
    - id: pcf-code-assessment-exclusion
      path: grounding/exclusions/pcf-code-assessment-exclusion.md
      version: "1.0.0"
      control_count: 0
    - id: azure-sql
      path: grounding/dependencies/springboot-azure-sql.md
      version: "2.3.0"
      control_count: 16
    - id: confluent-kafka
      path: grounding/dependencies/springboot-confluent-kafka.md
      version: "3.1.0"
      control_count: 27
    - id: azure-managed-redis
      path: grounding/dependencies/springboot-azure-managed-redis.md
      version: "2.2.0"
      control_count: 27
    - id: keyvault
      path: grounding/dependencies/springboot-keyvault.md
      version: "2.2.0"
      control_count: 14
    - id: jvm-runtime
      path: grounding/dependencies/jvm-runtime-resiliency.md
      version: "1.0.0"
      control_count: 22
    - id: appgateway-glb
      path: grounding/dependencies/springboot-appgateway-glb.md
      version: "2.2.0"
      control_count: 18
  standards_not_loaded:
    - id: container-build-resiliency
      reason: assessment_domain_disabled
    - id: cicd-pipeline-resiliency
      reason: assessment_domain_disabled
    - id: kubernetes-deployment-resiliency
      reason: assessment_domain_disabled
    - id: helm-kustomize-resiliency
      reason: assessment_domain_disabled
    - id: http-client
      reason: declared_only_dependency_not_listed_in_inventory_standards_to_load
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
  source_locator_precedence:
    - repository_path
    - symbol
    - original_source_excerpt
    - source_fingerprint
    - assessment_snapshot
    - original_line_range
  fingerprint_method:
    algorithm: sha256
    normalization: exact_utf8_excerpt
    line_separator: "\n"
    note: The excerpt is the exact assessed source text with lines joined by a single line feed and no trailing newline.
```

```yaml
assessment_scope_resolution:
  carried_from_step_1: true
  recalculated: false
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
    included_priorities: [P0, P1, P2, P3]
    testing_output_mode: hidden
  scope_rules:
    repository_owned_only: true
    deployed_infrastructure_findings_allowed: false
    pcf_findings_allowed: false
    missing_evidence_status: not_assessed
```

```yaml
architecture_relationship_context:
  carried_from_step_1: true
  recalculated: false
  source_path: application-context/application-architecture-context.yml
  context_status: approved
  context_version: "3.0.0"
  application_name: "Ecommerce Platform"
  repository_name: "Inventory Service"
  authoritative_state_dependency: azure-sql
  current_deployment_operating_model: active_standby
  approved_target_deployment_operating_model: active_active
  assessment_target_state: approved_target
  assess_code_against: target
  upstream_dependencies: []
  downstream_dependencies: []
  external_side_effects:
    present: false
    types: []
  solution_architecture_context: not_provided

architecture_conflict:
  detected: false
  resolution_status: not_applicable
  route_to: not_applicable
  code_finding_created_for_conflict: false

dependency_standard_gaps: []
```

```yaml
kafka_scenario_provenance:
  carried_from_step_1: true
  recalculated: false
  operating_scenario: active_standby
  scenario_source: approved_application_architecture_context
  context_id: not_applicable
  context_version: "3.0.0"
  scenario_policy_id: KAFKA-OPERATING-SCENARIO
  scenario_policy_version: "3.2.0"
  scenario_rule_id: KAFKA-SCENARIO-001
  scenario_validation_status: consistent
  architecture_confirmation_required: false
  processing_model: mixed
  regional_processing_model: single_active
  external_side_effects: none
  kafka_backed_state: none
  cluster_model_type: independent_regional_clusters
  conditional_assumptions: []
  related_state_dependencies:
    - azure-sql
  evaluation_rule_applied: approved_and_consistent_scenario
  scenario_families_evaluated:
    - KAFKA-001..KAFKA-012
    - KAFKA-AS-001..KAFKA-AS-009
  scenario_families_not_applicable:
    - KAFKA-AA-001..KAFKA-AA-006
  unresolved_infrastructure_facts:
    - Deployed Kafka cluster topology per region
    - Cluster Linking and Schema Linking configuration
    - Cross-region topic, schema, ACL, and consumer-offset replication
    - Azure SQL failover group deployment and listener DNS name
    - Azure Managed Redis deployed regional topology
    - Regional Kafka role assignment and standby consumption control
```

```yaml
resiliency_classification_contract:
  policy_id: RESILIENCY-FINDING-QUALIFICATION
  policy_version: "1.0.0"
  policy_path: grounding/governance/resiliency-finding-qualification-policy.yml
  applied_in_phase: assessment
  preserve_finding_classes: [resiliency, non_resiliency]
  non_resiliency_findings_suppressed: 0
```

## Control Results

### Master standard: springboot-aks-active-active-master v4.0.0

```yaml
control_results:
  standard: springboot-aks-active-active-master
  results:
    - {control: APP-AA-001, status: compliant, finding: not_applicable, note: "One Maven artifact with default and prod Spring profiles; no region-specific source or build path."}
    - {control: APP-AA-002, status: compliant, finding: not_applicable, note: "Every remote endpoint resolves from an environment placeholder (SQL_CONNECTION_STRING, REDIS_CONNECTION_STRING, KAFKA_BOOTSTRAP_SERVERS, AZURE_KEYVAULT_ENDPOINT)."}
    - {control: APP-AA-003, status: compliant, finding: not_applicable, note: "A single deployment-injected endpoint per dependency is the approved affinity mechanism; no remote-region endpoint is selected by the application."}
    - {control: APP-AA-004, status: non_compliant, finding: F-009, related_findings: [F-010, F-011], note: "No connect, socket, command, query, or transaction timeout exists for any remote dependency."}
    - {control: APP-AA-005, status: non_compliant, finding: F-012, note: "No retry or backoff mechanism exists anywhere in production code or configuration."}
    - {control: APP-AA-006, status: non_compliant, finding: F-015, primary: true}
    - {control: APP-AA-007, status: non_compliant, finding: F-008, primary: true}
    - {control: APP-AA-008, status: compliant, finding: not_applicable, note: "Probes are enabled with default groups, so the liveness group contains livenessState only and excludes external dependency indicators."}
    - {control: APP-AA-009, status: non_compliant, finding: F-008, note: "Auto-configured SQL, Redis, and Kafka health contributors have no bounded health timeout."}
    - {control: APP-AA-010, status: compliant, finding: not_applicable, note: "All durable state is in Azure SQL; HTTP handling is stateless and no pod-local or region-local state exists."}
    - {control: APP-AA-011, status: non_compliant, finding: F-003, primary: true}
    - {control: APP-AA-012, status: non_compliant, finding: F-013, note: "@Version exists but no conflict detection, retry, or caller-visible mapping is implemented."}
    - {control: APP-AA-013, status: non_compliant, finding: F-024, primary: true}
    - {control: APP-AA-014, status: non_compliant, finding: F-023, note: "Key Vault material is bound once at startup, so credential rotation or vault restoration requires a process restart."}
    - {control: APP-AA-015, status: non_compliant, finding: F-026, primary: true}
    - {control: APP-AA-016, status: non_compliant, finding: F-027, primary: true}
    - {control: APP-AA-017, status: non_compliant, finding: F-021, primary: true}
    - {control: APP-AA-018, status: non_compliant, finding: F-028, primary: true}
    - {control: APP-DISC-001, status: not_applicable, reason: "No DiscoveryClient or service registry is used."}
    - {control: APP-DISC-002, status: not_applicable, reason: "No DiscoveryClient or service registry is used."}
    - {control: APP-CONF-010, status: not_applicable, reason: "No dynamic refresh is enabled or expected; no @RefreshScope, actuator refresh endpoint, or config client exists."}
    - {control: APP-REACT-001, status: not_applicable, reason: "Servlet stack only; no Reactor usage in production source."}
    - {control: APP-REACT-002, status: not_applicable, reason: "Servlet stack only; no Reactor usage in production source."}
    - {control: APP-REACT-003, status: not_applicable, reason: "Servlet stack only; no Reactor usage in production source."}
    - {control: APP-CACHE-001, status: non_compliant, finding: F-017, note: "No TTL or refresh interval is configurable for the inventory cache."}
    - {control: APP-CACHE-002, status: not_assessed, reason: "Cache size and eviction are governed by Azure Managed Redis maxmemory policy, which is deployed infrastructure outside the enabled assessment domains."}
    - {control: APP-CACHE-003, status: compliant, finding: not_applicable, note: "The cache is an external shared Redis cache, not a pod-local cache, and correctness does not depend on cache residency."}
    - {control: APP-ACT-001, status: compliant, finding: not_applicable, note: "Exposure list is limited to health, info, and prometheus; env, heapdump, and loggers are not exposed."}
    - {control: APP-ACT-002, status: not_applicable, reason: "No sensitive administrative or diagnostic Actuator endpoint is exposed."}
    - {control: APP-ACT-003, status: compliant, finding: not_applicable, note: "management.endpoint.health.show-details is not set, so the framework default of never applies."}
    - {control: APP-LOG-001, status: compliant, finding: not_applicable, note: "No production class declares a logger, so no credential or payload logging path exists."}
    - {control: APP-LOG-002, status: compliant, finding: not_applicable, note: "Lombok-generated toString on InventoryItem and the DTO records contain no secret, credential, or payment field."}
    - {control: APP-WEB-001, status: compliant, finding: not_applicable, note: "Servlet stack with a matching @RestControllerAdvice handler model."}
    - {control: APP-WEB-002, status: non_compliant, finding: F-014, primary: true}
    - {control: APP-CONF-011, status: not_applicable, reason: "Spring Cloud Config Client is not used."}
    - {control: APP-CONF-012, status: not_applicable, reason: "No @ConfigurationProperties binding class exists in production source."}
    - {control: APP-CONF-013, status: not_applicable, reason: "No resiliency property is declared, so none can be declared-but-unapplied."}
    - {control: APP-HTTP-001, status: not_applicable, reason: "Servlet stack with no reactive event loop and no shared executor hosting blocking SDK calls."}
    - {control: APP-HTTP-002, status: not_applicable, reason: "No outbound HTTP client exists in production source."}
    - {control: APP-HTTP-003, status: not_applicable, reason: "No outbound HTTP client or HTTP retry exists."}
    - {control: APP-HTTP-004, status: not_applicable, reason: "No token-authenticated outbound call exists."}
    - {control: APP-HTTP-005, status: not_applicable, reason: "No shared global third-party dependency is invoked."}
    - {control: APP-TOKEN-001, status: not_applicable, reason: "No OAuth token acquisition exists in production source."}
    - {control: APP-TOKEN-002, status: not_applicable, reason: "No token cache exists in production source."}
    - {control: APP-STATE-001, status: not_applicable, reason: "No durable workflow status field or state machine is persisted."}
    - {control: APP-STATE-002, status: not_applicable, reason: "No retry wraps durable work, so retry exhaustion cannot strand records."}
    - {control: APP-ASYNC-001, status: not_applicable, reason: "@Async is not used."}
    - {control: APP-ASYNC-002, status: not_applicable, reason: "No custom executor or scheduler bean exists."}
    - {control: APP-KAFKA-001, status: non_compliant, finding: F-004, primary: true}
    - {control: APP-KAFKA-002, status: non_compliant, finding: F-005, primary: true}
    - {control: APP-KAFKA-003, status: non_compliant, finding: F-006, primary: true}
    - {control: APP-KAFKA-004, status: compliant, finding: not_applicable, note: "micrometer-registry-prometheus is present and the prometheus endpoint is exposed, so Spring Boot binds Kafka consumer client metrics including records-lag and assignment."}
    - {control: APP-KAFKA-005, status: non_compliant, finding: F-001, primary: true}
    - {control: APP-KAFKA-006, status: non_compliant, finding: F-007, primary: true}
    - {control: APP-KAFKA-007, status: compliant, finding: not_applicable, note: "The declared serializer, deserializer, auto-offset-reset, and trusted-packages settings are all applied to the effective client configuration."}
    - {control: APP-CACHE-004, status: non_compliant, finding: F-019, note: "@Cacheable is declared without sync, so concurrent misses fan out to Azure SQL."}
    - {control: APP-CACHE-005, status: not_applicable, reason: "No cache refresh, warm-up, or preload path exists."}
    - {control: APP-CACHE-006, status: compliant, finding: not_applicable, note: "get(Long) throws ResourceNotFoundException for a missing item, so a null or absent result is never cached or returned as success."}
    - {control: APP-HEALTH-001, status: not_applicable, reason: "No custom health group include or exclude list is configured."}
    - {control: APP-HEALTH-002, status: not_applicable, reason: "No cached or custom health state is maintained by the application."}
    - {control: APP-API-001, status: not_applicable, reason: "No administrative endpoint exists and no GET endpoint mutates state."}
    - {control: APP-SUPPLY-001, status: non_compliant, finding: F-028, note: "Spring Boot parent and Spring Cloud Azure BOM govern resilience-relevant transitive versions with no regression test beyond a context-load assertion."}
    - {control: APP-SUPPLY-002, status: not_assessed, reason: "Dockerfile is repository-owned but the container_build domain is disabled."}
    - {control: APP-OBS-001, status: not_applicable, reason: "No tracing instrumentation exists, so trace export completeness cannot apply."}
    - {control: APP-CONF-014, status: not_applicable, reason: "No partner or operationally variable constant is embedded in production source."}
    - {control: APP-WORKLOAD-001, status: non_compliant, finding: F-004, note: "Kafka consumption is non-HTTP work that cannot fail over through gateway traffic routing and can execute in both regions."}
    - {control: APP-WORKLOAD-002, status: non_compliant, finding: F-004, note: "Listener activation defaults to enabled with no ownership token, lease, or split-brain detection."}
    - {control: APP-SCHED-001, status: not_applicable, reason: "No @Scheduled or scheduled workload exists."}
    - {control: APP-SCHED-002, status: not_applicable, reason: "No reprocessor selects durable records."}
    - {control: APP-BATCH-001, status: not_applicable, reason: "The application is a long-running service and does not exit after a run."}
    - {control: APP-BATCH-002, status: not_applicable, reason: "No repeatable business run identity exists."}
    - {control: APP-BATCH-003, status: not_applicable, reason: "No job produces required files or reports."}
    - {control: APP-BATCH-004, status: not_applicable, reason: "No batch job reads large result sets; the unbounded list endpoint is assessed under JVM-004."}
    - {control: APP-FIN-001, status: not_applicable, reason: "Approved context declares external_side_effects present false and no financial provider call exists in production source."}
    - {control: APP-FIN-002, status: not_applicable, reason: "No workflow spans an external financial provider."}
    - {control: APP-FIN-003, status: not_applicable, reason: "No financial operation exists."}
    - {control: APP-FIN-004, status: not_applicable, reason: "No synthetic or deferred approval path exists."}
    - {control: APP-DB-001, status: not_applicable, reason: "No reactive database access; JPA over JDBC only."}
    - {control: APP-DB-003, status: non_compliant, finding: F-002, primary: true}
    - {control: APP-CORRECT-001, status: not_applicable, reason: "No Mono or Flux is returned by any production method."}
    - {control: APP-CORRECT-002, status: compliant, finding: not_applicable, note: "Missing mandatory business data raises ResourceNotFoundException rather than defaulting to null, empty, or zero."}
    - {control: APP-FALLBACK-001, status: not_applicable, reason: "No fallback path is invoked on primary failure; the absence of a Redis fallback is assessed under REDIS-020."}
    - {control: APP-OBS-002, status: non_compliant, finding: F-027, note: "No business throughput, last-success, or backlog-age signal exists, so Kafka processing can stop while the process remains healthy."}
    - {control: APP-OBS-003, status: non_compliant, finding: F-007, note: "No correlation identifier is persisted or propagated across the SQL and Kafka boundary."}
    - {control: APP-ENDPOINT-001, status: not_applicable, reason: "No durable record stores a destination URL or endpoint."}
    - {control: APP-PROC-001, status: not_applicable, reason: "No companion or side process is started by the application."}
  status_counts:
    compliant: 15
    non_compliant: 27
    not_assessed: 2
    not_applicable: 42
    accepted_risk: 0
    total: 86
```

### Dependency standard: azure-sql v2.3.0

```yaml
control_results:
  standard: azure-sql
  results:
    - {control: SQL-001, status: compliant, finding: not_applicable, note: "Production JDBC URL is fully deployment-injected through SQL_CONNECTION_STRING; no server or region is hardcoded. Whether the injected value is the failover-group read-write listener is an external evidence gap (EG-001)."}
    - {control: SQL-002, status: non_compliant, finding: F-009, primary: true}
    - {control: SQL-003, status: non_compliant, finding: F-012, primary: true}
    - {control: SQL-004, status: non_compliant, finding: F-003, note: "The unique constraint on productId protects create, but reserve and release apply relative deltas with no business uniqueness or idempotency key."}
    - {control: SQL-005, status: compliant, finding: not_applicable, note: "HikariCP default borrow-time validation and maxLifetime evict connections invalidated by an endpoint change without a process restart."}
    - {control: SQL-006, status: non_compliant, finding: F-008, note: "The auto-configured DataSourceHealthIndicator is not in the default readiness group, so database loss leaves the pod ready."}
    - {control: SQL-007, status: non_compliant, finding: F-013, primary: true}
    - {control: SQL-008, status: non_compliant, finding: F-028, note: "The only integration test asserts context load; no connection loss, failover, or unknown commit outcome is exercised."}
    - {control: SQL-009, status: not_applicable, reason: "R2DBC is not used."}
    - {control: SQL-010, status: not_applicable, reason: "R2DBC is not used."}
    - {control: SQL-011, status: not_applicable, reason: "R2DBC is not used."}
    - {control: SQL-012, status: not_applicable, reason: "R2DBC is not used."}
    - {control: SQL-013, status: non_compliant, finding: F-002, note: "Azure SQL and Kafka can diverge with no outbox, saga, terminal status, or reconciliation marker."}
    - {control: SQL-014, status: not_applicable, reason: "R2DBC driver and pool are not used."}
    - {control: SQL-015, status: non_compliant, finding: F-008, note: "Database readiness participation and health-check bounding are both framework defaults."}
    - {control: SQL-016, status: not_applicable, reason: "R2DBC is not used."}
  status_counts:
    compliant: 2
    non_compliant: 8
    not_assessed: 0
    not_applicable: 6
    accepted_risk: 0
    total: 16
```

### Dependency standard: confluent-kafka v3.1.0

```yaml
control_results:
  standard: confluent-kafka
  operating_scenario: active_standby
  scenario_rule_id: KAFKA-SCENARIO-001
  scenario_validation_status: consistent
  results:
    - {control: KAFKA-001, status: compliant, finding: not_applicable, note: "bootstrap-servers is injected through KAFKA_BOOTSTRAP_SERVERS in the prod profile; no cluster endpoint is hardcoded and no dual-cluster bootstrap list exists."}
    - {control: KAFKA-002, status: non_compliant, finding: F-001, note: "acks, retries, enable.idempotence, and delivery.timeout.ms are unset and the send result is discarded."}
    - {control: KAFKA-003, status: non_compliant, finding: F-003, note: "No event identity, deduplication store, or rebalance listener exists."}
    - {control: KAFKA-004, status: non_compliant, finding: F-005, note: "No ack mode, manual acknowledgment, or transactional.id aligns offset commit with the database transaction."}
    - {control: KAFKA-005, status: non_compliant, finding: F-011, primary: true}
    - {control: KAFKA-006, status: non_compliant, finding: F-006, note: "No dead-letter topic, DeadLetterPublishingRecoverer, or explicit attempt bound is configured."}
    - {control: KAFKA-007, status: non_compliant, finding: F-008, related_findings: [F-027], note: "Kafka health participation is a framework default and an intentionally inactive standby role cannot be distinguished from a failed consumer."}
    - {control: KAFKA-008, status: non_compliant, finding: F-028, note: "@EmbeddedKafka is present but no duplicate, replay, rebalance, broker-loss, schema-failure, or promotion test exists."}
    - {control: KAFKA-009, status: compliant, finding: not_applicable, note: "The operating scenario is declared by approved application architecture context, validated as consistent under KAFKA-SCENARIO-001, and aligned with Azure SQL as authoritative business state."}
    - {control: KAFKA-010, status: non_compliant, finding: F-004, note: "Kafka processing mutates authoritative Azure SQL state with no alignment to regional primary ownership."}
    - {control: KAFKA-011, status: non_compliant, finding: F-007, note: "Topic, key, group, and schema identity are portable, but published events carry no stable event identity across retry or failover."}
    - {control: KAFKA-012, status: non_compliant, finding: F-004, note: "Endpoints are externalized, but there is no consumer-enabled or cluster-role property, so a regional role change cannot be applied by configuration alone."}
    - {control: KAFKA-AA-001, status: not_applicable, reason: "Operating scenario is active_standby."}
    - {control: KAFKA-AA-002, status: not_applicable, reason: "Operating scenario is active_standby."}
    - {control: KAFKA-AA-003, status: not_applicable, reason: "Operating scenario is active_standby."}
    - {control: KAFKA-AA-004, status: not_applicable, reason: "Operating scenario is active_standby."}
    - {control: KAFKA-AA-005, status: not_applicable, reason: "Operating scenario is active_standby and no Cosmos DB dependency exists."}
    - {control: KAFKA-AA-006, status: not_applicable, reason: "Operating scenario is active_standby."}
    - {control: KAFKA-AS-001, status: non_compliant, finding: F-004, note: "The listener auto-starts in every instance, so a standby instance ordinarily consumes authoritative work."}
    - {control: KAFKA-AS-002, status: non_compliant, finding: F-004, note: "No activation gate verifies Azure SQL primary ownership before Kafka processing starts."}
    - {control: KAFKA-AS-003, status: non_compliant, finding: F-004, note: "Activation defaults to enabled with no lease, epoch, fencing token, or both-active detection."}
    - {control: KAFKA-AS-004, status: non_compliant, finding: F-003, note: "auto-offset-reset earliest combined with absent idempotency means a promotion or offset reset repeats reserve and release effects."}
    - {control: KAFKA-AS-005, status: not_assessed, reason: "Whether the injected bootstrap target is a passive mirror or a promoted writable cluster is deployed topology outside the enabled assessment domains (EG-002)."}
    - {control: KAFKA-AS-006, status: non_compliant, finding: F-003, related_findings: [F-007], note: "Failover replay can duplicate SQL-backed inventory effects and events carry no stable business operation identity."}
    - {control: KAFKA-AS-007, status: non_compliant, finding: F-004, note: "The application cannot stop acquisition before ownership transfer and can process while SQL and Kafka roles are misaligned."}
    - {control: KAFKA-AS-008, status: non_compliant, finding: F-004, note: "No ownership epoch or fencing prevents a stale consumer from reactivating during failback."}
    - {control: KAFKA-AS-009, status: non_compliant, finding: F-028, note: "No test covers promotion, stale-active fencing, offset restoration, duplicate replay, or failback."}
  status_counts:
    compliant: 2
    non_compliant: 18
    not_assessed: 1
    not_applicable: 6
    accepted_risk: 0
    total: 27
```

### Dependency standard: azure-managed-redis v2.2.0

```yaml
control_results:
  standard: azure-managed-redis
  results:
    - {control: REDIS-001, status: compliant, finding: not_applicable, note: "Redis is used only through the Spring cache abstraction; Azure SQL is the explicit authoritative business state."}
    - {control: REDIS-002, status: compliant, finding: not_applicable, note: "A cache miss falls through to the JPA repository, so business correctness does not require cache residency."}
    - {control: REDIS-003, status: compliant, finding: not_applicable, note: "The Redis URL is injected through REDIS_CONNECTION_STRING in the prod profile with no hardcoded regional endpoint."}
    - {control: REDIS-004, status: not_assessed, reason: "Production credentials and TLS scheme are contained inside the externally supplied REDIS_CONNECTION_STRING value, which is not repository evidence (EG-003)."}
    - {control: REDIS-005, status: non_compliant, finding: F-010, primary: true}
    - {control: REDIS-006, status: compliant, finding: not_applicable, note: "Lettuce default auto-reconnect restores connectivity after a failover without a process restart."}
    - {control: REDIS-007, status: not_applicable, reason: "No Redis retry is implemented."}
    - {control: REDIS-008, status: non_compliant, finding: F-015, note: "No bulkhead or circuit breaker separates request threads from blocking Redis commands."}
    - {control: REDIS-009, status: non_compliant, finding: F-019, primary: true}
    - {control: REDIS-010, status: not_applicable, reason: "No refresh, warm-up, or preload path exists."}
    - {control: REDIS-011, status: non_compliant, finding: F-017, primary: true}
    - {control: REDIS-012, status: non_compliant, finding: F-029, primary: true}
    - {control: REDIS-013, status: compliant, finding: not_applicable, note: "A missing item raises ResourceNotFoundException before any cache write, so absence is never cached as success."}
    - {control: REDIS-014, status: not_applicable, reason: "No last-known-good or stale-if-error behavior is implemented."}
    - {control: REDIS-015, status: non_compliant, finding: F-020, primary: true}
    - {control: REDIS-016, status: not_applicable, reason: "Redis is not used for locks or leader election."}
    - {control: REDIS-017, status: not_applicable, reason: "Redis stores no session, token, authorization, or rate-limit state."}
    - {control: REDIS-018, status: not_assessed, reason: "Approved context sets the Redis target operating model to active_active, but deployed geo-replication and conflict behavior are outside the enabled assessment domains (EG-004)."}
    - {control: REDIS-019, status: non_compliant, finding: F-008, note: "Redis health participation in readiness is a framework default with no bounded health timeout."}
    - {control: REDIS-020, status: non_compliant, finding: F-016, primary: true}
    - {control: REDIS-021, status: not_applicable, reason: "Cached values contain product identifiers and quantities only, with no customer, payment, token, or credential data."}
    - {control: REDIS-022, status: non_compliant, finding: F-018, primary: true}
    - {control: REDIS-023, status: not_applicable, reason: "No pipeline, MULTI/EXEC, or Lua script is used."}
    - {control: REDIS-024, status: compliant, finding: not_applicable, note: "The Lettuce connection factory is a singleton auto-configured bean; no per-request client is created."}
    - {control: REDIS-025, status: non_compliant, finding: F-027, note: "No metric or log distinguishes cache miss, Redis failure, timeout, saturation, or recovery."}
    - {control: REDIS-026, status: non_compliant, finding: F-027, note: "Redis degradation is not visible in business throughput signals."}
    - {control: REDIS-027, status: non_compliant, finding: F-028, note: "No fault test covers Redis failover, reconnect, eviction, stampede, or stale behavior."}
  status_counts:
    compliant: 6
    non_compliant: 12
    not_assessed: 2
    not_applicable: 7
    accepted_risk: 0
    total: 27
```

### Dependency standard: keyvault v2.2.0

```yaml
control_results:
  standard: keyvault
  results:
    - {control: KV-001, status: compliant, finding: not_applicable, note: "The vault URI is injected through AZURE_KEYVAULT_ENDPOINT with no hardcoded vault or region."}
    - {control: KV-002, status: compliant, finding: not_applicable, note: "No static credential is configured; the Spring Cloud Azure default credential chain applies."}
    - {control: KV-003, status: non_compliant, finding: F-022, note: "No ClientOptions, RetryOptions, or startup timeout bounds the Key Vault property-source resolution."}
    - {control: KV-004, status: compliant, finding: not_applicable, note: "Secrets resolve once through a Spring property source at startup and never on the request path."}
    - {control: KV-005, status: non_compliant, finding: F-023, primary: true}
    - {control: KV-006, status: compliant, finding: not_applicable, note: "The running service does not require live vault access, so a sustained vault failure does not make the service unsafe to serve."}
    - {control: KV-007, status: non_compliant, finding: F-023, note: "Vault or identity restoration cannot be picked up without a process restart."}
    - {control: KV-008, status: non_compliant, finding: F-028, note: "No test exercises endpoint selection, throttling, timeout, access denial, or recovery."}
    - {control: KV-009, status: non_compliant, finding: F-022, primary: true}
    - {control: KV-010, status: non_compliant, finding: F-023, note: "Rotated secrets are never rebound, so the datasource and Redis clients retain startup material."}
    - {control: KV-011, status: not_applicable, reason: "No certificate or trust material is retrieved at runtime."}
    - {control: KV-012, status: not_applicable, reason: "No certificate is managed by the application."}
    - {control: KV-013, status: compliant, finding: not_applicable, note: "No logging, health detail, or generated string representation can disclose secrets; health details default to never."}
    - {control: KV-014, status: non_compliant, finding: F-008, note: "Key Vault readiness participation is a framework default and was not evaluated against the application's actual live-access requirement."}
  status_counts:
    compliant: 5
    non_compliant: 7
    not_assessed: 0
    not_applicable: 2
    accepted_risk: 0
    total: 14
```

### Dependency standard: jvm-runtime v1.0.0

```yaml
control_results:
  standard: jvm-runtime
  results:
    - {control: JVM-001, status: compliant, finding: not_applicable, note: "java.version 17 is declared and is supported by Spring Boot 3.3.5; no conflicting repository-owned runtime declaration exists in the enabled domains."}
    - {control: JVM-002, status: not_assessed, reason: "Container base image and JVM environment variables are in the disabled container_build domain (EG-005)."}
    - {control: JVM-003, status: not_assessed, reason: "Heap flags and container memory limits are in disabled domains (EG-005)."}
    - {control: JVM-004, status: non_compliant, finding: F-025, primary: true}
    - {control: JVM-005, status: not_assessed, reason: "Collector selection is expressed through JVM flags in the disabled container_build domain (EG-005)."}
    - {control: JVM-006, status: not_assessed, reason: "GC flags are in the disabled container_build domain (EG-005)."}
    - {control: JVM-007, status: not_assessed, reason: "GC logging configuration is in the disabled container_build domain (EG-005)."}
    - {control: JVM-008, status: not_assessed, reason: "OOM flags and dump paths are in the disabled container_build domain (EG-005)."}
    - {control: JVM-009, status: not_assessed, reason: "Native and off-heap settings are in the disabled container_build domain (EG-005)."}
    - {control: JVM-010, status: non_compliant, finding: F-015, note: "The default servlet thread pool is far larger than the default HikariCP pool with no isolation or rejection policy between them."}
    - {control: JVM-011, status: not_applicable, reason: "Virtual threads are not enabled; spring.threads.virtual.enabled is absent and the effective runtime is Java 17."}
    - {control: JVM-012, status: not_applicable, reason: "Virtual threads are not used."}
    - {control: JVM-013, status: not_applicable, reason: "Virtual threads are not used."}
    - {control: JVM-014, status: not_assessed, reason: "Safepoint, JIT, and CDS behavior require runtime and container evidence outside the enabled domains (EG-005)."}
    - {control: JVM-015, status: not_assessed, reason: "Container ENTRYPOINT and signal forwarding are in the disabled container_build domain (EG-005)."}
    - {control: JVM-016, status: non_compliant, finding: F-021, note: "Neither server.shutdown graceful nor spring.lifecycle.timeout-per-shutdown-phase is configured."}
    - {control: JVM-017, status: non_compliant, finding: F-021, note: "The Kafka listener container and the servlet container have no coordinated intake-stop and drain contract."}
    - {control: JVM-018, status: not_applicable, reason: "No @PreDestroy, DisposableBean, SmartLifecycle, or raw JVM shutdown hook is declared in production source."}
    - {control: JVM-019, status: non_compliant, finding: F-003, related_findings: [F-002], note: "Abrupt process loss has no idempotency, replay guard, reconciliation, or startup recovery path."}
    - {control: JVM-020, status: compliant, finding: not_applicable, note: "Micrometer with the Prometheus registry exposes the default JVM memory, GC, thread, and class-loading meters through the exposed prometheus endpoint."}
    - {control: JVM-021, status: non_compliant, finding: F-009, related_findings: [F-010, F-011, F-021], note: "No application-layer deadline exists, so no budget ordering against gateway, mesh, or pod termination budgets can hold."}
    - {control: JVM-022, status: not_applicable, reason: "JVM-022 states validation obligations for proposed changes rather than an assessable repository behavior; validation requirements are carried into Step 3A."}
  status_counts:
    compliant: 2
    non_compliant: 6
    not_assessed: 9
    not_applicable: 5
    accepted_risk: 0
    total: 22
```

### Dependency standard: appgateway-glb v2.2.0

```yaml
control_results:
  standard: appgateway-glb
  results:
    - {control: GLB-001, status: compliant, finding: not_applicable, note: "management.endpoint.health.probes.enabled is true, which exposes /actuator/health/readiness and /actuator/health/liveness."}
    - {control: GLB-002, status: non_compliant, finding: F-008, note: "A failed regional dependency leaves the pod ready and traffic-eligible."}
    - {control: GLB-003, status: compliant, finding: not_applicable, note: "The default liveness group contains livenessState only, so a dependency outage cannot trigger restart loops."}
    - {control: GLB-004, status: non_compliant, finding: F-008, note: "Auto-configured dependency health contributors are unbounded and can hang or add load during a dependency incident."}
    - {control: GLB-005, status: not_applicable, reason: "The API returns JSON bodies only; no redirect, cookie, callback URL, or scheme-dependent security behavior exists."}
    - {control: GLB-006, status: compliant, finding: not_applicable, note: "No HttpSession, session scope, or authentication state is held; all endpoints are stateless."}
    - {control: GLB-007, status: non_compliant, finding: F-021, primary: false, note: "Readiness is not withdrawn before termination and in-flight work is not drained."}
    - {control: GLB-008, status: non_compliant, finding: F-028, note: "No Actuator integration test or fault injection verifies probe transitions or traffic eligibility."}
    - {control: GLB-009, status: non_compliant, finding: F-022, note: "Startup depends on a mandatory Key Vault property-source import with no bounded or optional contract."}
    - {control: GLB-010, status: not_assessed, reason: "No application-layer deadline exists to compare, and gateway and load-balancer idle timeouts are outside the enabled assessment domains (EG-006). The absent application timeout itself is recorded under F-009, F-010, and F-011."}
    - {control: GLB-011, status: not_applicable, reason: "No WebSocket, SSE, streaming, or long-polling endpoint exists."}
    - {control: GLB-012, status: not_assessed, reason: "Exposure is limited to health, info, and prometheus with default show-details never, but external reachability depends on ingress and management-port routing in the disabled deployment_configuration domain (EG-007)."}
    - {control: GLB-013, status: non_compliant, finding: F-003, note: "POST reserve and release are non-idempotent and carry an unused referenceId, so a gateway or client retry duplicates the business effect."}
    - {control: GLB-014, status: not_applicable, reason: "The application generates no absolute URL, redirect target, or cookie."}
    - {control: GLB-015, status: not_applicable, reason: "No forwarded header is used for security, rate limiting, auditing, or authorization."}
    - {control: GLB-016, status: not_assessed, reason: "Keep-alive and idle eviction behavior is governed by gateway and platform configuration outside the enabled domains (EG-006)."}
    - {control: GLB-017, status: compliant, finding: not_applicable, note: "Probe paths use the default Actuator context on the main port with no environment-specific override and no probe authentication requirement."}
    - {control: GLB-018, status: non_compliant, finding: F-026, related_findings: [F-027], note: "No readiness-transition metric, state-change log, or region tag exists."}
  status_counts:
    compliant: 4
    non_compliant: 7
    not_assessed: 3
    not_applicable: 4
    accepted_risk: 0
    total: 18
```

### Aggregate control results

```yaml
control_result_summary:
  total_controls_evaluated: 210
  compliant: 36
  non_compliant: 85
  not_assessed: 17
  not_applicable: 72
  accepted_risk: 0
  non_compliant_controls_mapped_to_findings: 85
  findings_without_noncompliant_control: 0
  by_standard:
    springboot-aks-active-active-master: {compliant: 15, non_compliant: 27, not_assessed: 2, not_applicable: 42, total: 86}
    azure-sql: {compliant: 2, non_compliant: 8, not_assessed: 0, not_applicable: 6, total: 16}
    confluent-kafka: {compliant: 2, non_compliant: 18, not_assessed: 1, not_applicable: 6, total: 27}
    azure-managed-redis: {compliant: 6, non_compliant: 12, not_assessed: 2, not_applicable: 7, total: 27}
    keyvault: {compliant: 5, non_compliant: 7, not_assessed: 0, not_applicable: 2, total: 14}
    jvm-runtime: {compliant: 2, non_compliant: 6, not_assessed: 9, not_applicable: 5, total: 22}
    appgateway-glb: {compliant: 4, non_compliant: 7, not_assessed: 3, not_applicable: 4, total: 18}
```

## Findings

All findings are `verified`. No finding is `conditional`, because the Kafka operating scenario is supplied by approved application architecture context and validated `consistent` under `KAFKA-SCENARIO-001` with `architecture_confirmation_required: false`.

### F-001: Kafka publication is fire-and-forget with no durability configuration

```yaml
finding:
  id: F-001
  title: Kafka publication is fire-and-forget with no durability configuration
  severity: critical
  finding_status: verified
  primary_control: APP-KAFKA-005
  primary_standard: springboot-aks-active-active-master
  related_controls: [KAFKA-002, APP-AA-016]
  observed_behavior: >-
    InventoryEventProducer.publish calls kafkaTemplate.send and discards the returned CompletableFuture.
    No callback, whenComplete handler, ProducerListener, or blocking get inspects the delivery outcome.
    The producer configuration sets only key and value serializers; acks, retries, enable.idempotence,
    delivery.timeout.ms, and max.in.flight.requests.per.connection are all left at client defaults and
    are not deployment-tunable through repository-owned configuration.
  risk: >-
    Every inventory state change publishes an event whose delivery outcome is never observed. A broker
    outage, leader election, partition unavailability, or serialization failure silently drops the event
    while the Azure SQL write is reported successful to the caller. Downstream consumers of
    inventory-events then hold state that permanently disagrees with authoritative inventory, and there
    is no signal that would let an operator detect or replay the loss.
  implementation_boundary: >-
    Repository-owned: producer result handling in InventoryEventProducer and Kafka producer properties
    in application.yml and application-prod.yml. Out of boundary: broker-side min.insync.replicas,
    topic replication factor, and Cluster Linking state.
  finding_classification:
    type: resiliency
    qualification_status: qualified
    policy_id: RESILIENCY-FINDING-QUALIFICATION
    policy_version: "1.0.0"
    resiliency_domains: [durability, failure_observability, recoverability]
    failure_scenario: >-
      A regional Kafka broker or partition leader becomes unavailable during an active-standby failover
      window while the service continues serving REST and consumer traffic.
    target_architecture_element: >-
      inventory-events topic publication from the active regional role in the approved active-standby
      Kafka operating scenario.
    causal_mechanism: >-
      The send future is discarded and no acks or idempotence setting is declared, so a failed or
      unacknowledged produce is indistinguishable from a successful one inside the application.
    material_impact: >-
      Silent permanent event loss with no detection path, which breaks downstream inventory state and
      removes any basis for targeted replay during recovery.
    non_resiliency_category: not_applicable
    classification_rationale: >-
      Evidence-backed control violation with a credible failure scenario in an approved resiliency
      domain, a direct causal mechanism, and a material impact on recovery and durability rather than a
      general quality concern.
  dependency_context:
    dependency: confluent-kafka
    operating_scenario: active_standby
    scenario_source: approved_application_architecture_context
    context_id: not_applicable
    context_version: "3.0.0"
    scenario_policy_id: KAFKA-OPERATING-SCENARIO
    scenario_policy_version: "3.2.0"
    scenario_rule_id: KAFKA-SCENARIO-001
    scenario_validation_status: consistent
    architecture_confirmation_required: false
    processing_model: mixed
    regional_processing_model: single_active
    external_side_effects: none
    kafka_backed_state: none
    conditional_assumptions: []
    related_state_dependencies: [azure-sql]
  repository_evidence:
    - evidence_id: EV-F-001-01
      repository_path: source/inventory-service/src/main/java/com/ecommerce/inventory/kafka/producer/InventoryEventProducer.java
      symbol: InventoryEventProducer.publish
      source_language: java
      assessment_snapshot:
        type: workspace_snapshot
        identifier: "inventory-service-workspace-2026-09-18"
        provenance: workspace_generated
        git_commit_sha: not_applicable
        dirty_worktree: not_applicable
        captured_at: "2026-09-18T00:00:00Z"
        limitations: []
      source_fingerprint:
        algorithm: sha256
        normalization: exact_utf8_excerpt
        fingerprint_scope: exact_excerpt
        value: "c77eedf9776fd6bdfbd13ff41642bb1f00ae2767f58bba7c495f40b6dbc8ce8f"
      original_line_range: {start_line: 14, end_line: 16, status: exact}
      evidence_purpose: primary
      original_source_excerpt: |
            public void publish(String type, InventoryResponse inventory, String referenceId) {
                kafkaTemplate.send("inventory-events", inventory.productId(), Map.of("type", type, "occurredAt", Instant.now().toString(), "referenceId", referenceId == null ? "" : referenceId, "inventory", inventory));
            }
    - evidence_id: EV-F-001-02
      repository_path: source/inventory-service/src/main/resources/application.yml
      symbol: spring.kafka.producer
      source_language: yaml
      assessment_snapshot:
        type: workspace_snapshot
        identifier: "inventory-service-workspace-2026-09-18"
        provenance: workspace_generated
        git_commit_sha: not_applicable
        dirty_worktree: not_applicable
        captured_at: "2026-09-18T00:00:00Z"
        limitations: []
      source_fingerprint:
        algorithm: sha256
        normalization: exact_utf8_excerpt
        fingerprint_scope: exact_excerpt
        value: "825e9b9cd362296fb3cc671568f190b240d2240909ad86c9e2d6799014bfbcca"
      original_line_range: {start_line: 26, end_line: 28, status: exact}
      evidence_purpose: supporting
      original_source_excerpt: |
            producer:
              key-serializer: org.apache.kafka.common.serialization.StringSerializer
              value-serializer: org.springframework.kafka.support.serializer.JsonSerializer
```

### F-002: Event publication occurs inside the database transaction with no outbox or commit coordination

```yaml
finding:
  id: F-002
  title: Event publication occurs inside the database transaction with no outbox or commit coordination
  severity: critical
  finding_status: verified
  primary_control: APP-DB-003
  primary_standard: springboot-aks-active-active-master
  related_controls: [SQL-013]
  observed_behavior: >-
    saveAndPublish performs repository.save and then producer.publish inside the same @Transactional
    service method, so the Kafka send is issued before the database transaction commits. delete removes
    the entity and publishes INVENTORY_DELETED in the same transaction. No transactional outbox table,
    @TransactionalEventListener, or AFTER_COMMIT hook exists anywhere in production source.
  risk: >-
    The Azure SQL write and the Kafka publication can diverge in both directions. If the transaction
    rolls back after the send, downstream consumers receive an event describing inventory state that was
    never committed. If the broker is reachable but the commit fails, the event is already in flight.
    There is no durable intent record, terminal status, or reconciliation marker that would let recovery
    detect or repair the divergence, which is precisely the state that must be rebuilt after an
    active-standby regional promotion.
  implementation_boundary: >-
    Repository-owned: InventoryServiceImpl transaction and publication sequencing, and any new outbox
    entity, repository, and relay. Out of boundary: broker transaction coordinator configuration and
    deployed database replication.
  finding_classification:
    type: resiliency
    qualification_status: qualified
    policy_id: RESILIENCY-FINDING-QUALIFICATION
    policy_version: "1.0.0"
    resiliency_domains: [durability, state_recovery, recoverability]
    failure_scenario: >-
      A commit failure, connection reset during commit, or regional promotion interrupts the service
      between the Kafka send and the SQL commit.
    target_architecture_element: >-
      The Azure SQL authoritative business state and the inventory-events topic contract in the approved
      active-standby target deployment.
    causal_mechanism: >-
      The send is executed inside the transaction scope with no commit-ordered publication and no durable
      intent record, so the two stores have no common commit point.
    material_impact: >-
      Permanent, undetectable divergence between authoritative inventory state and published inventory
      events, with no reconciliation path available during or after regional recovery.
    non_resiliency_category: not_applicable
    classification_rationale: >-
      Evidence-backed cross-store consistency violation whose impact is specific to durability and
      post-failover state recovery rather than to general code quality.
  repository_evidence:
    - evidence_id: EV-F-002-01
      repository_path: source/inventory-service/src/main/java/com/ecommerce/inventory/service/impl/InventoryServiceImpl.java
      symbol: InventoryServiceImpl.saveAndPublish
      source_language: java
      assessment_snapshot:
        type: workspace_snapshot
        identifier: "inventory-service-workspace-2026-09-18"
        provenance: workspace_generated
        git_commit_sha: not_applicable
        dirty_worktree: not_applicable
        captured_at: "2026-09-18T00:00:00Z"
        limitations: []
      source_fingerprint:
        algorithm: sha256
        normalization: exact_utf8_excerpt
        fingerprint_scope: exact_excerpt
        value: "2f208c196a95785202f3ca2288a61c4648aee79e5b12f266f73a899b81cbb827"
      original_line_range: {start_line: 51, end_line: 51, status: exact}
      evidence_purpose: primary
      original_source_excerpt: |
            private InventoryResponse saveAndPublish(InventoryItem item, String type, String referenceId) { InventoryResponse response = mapper.toResponse(repository.save(item)); producer.publish(type, response, referenceId); return response; }
    - evidence_id: EV-F-002-02
      repository_path: source/inventory-service/src/main/java/com/ecommerce/inventory/service/impl/InventoryServiceImpl.java
      symbol: InventoryServiceImpl.delete
      source_language: java
      assessment_snapshot:
        type: workspace_snapshot
        identifier: "inventory-service-workspace-2026-09-18"
        provenance: workspace_generated
        git_commit_sha: not_applicable
        dirty_worktree: not_applicable
        captured_at: "2026-09-18T00:00:00Z"
        limitations: []
      source_fingerprint:
        algorithm: sha256
        normalization: exact_utf8_excerpt
        fingerprint_scope: exact_excerpt
        value: "5b17867aea81565d2b0571757edcd4b0510e822d2bd7da662bdc644e48cf1848"
      original_line_range: {start_line: 35, end_line: 36, status: exact}
      evidence_purpose: supporting
      original_source_excerpt: |
            @Override @Transactional @CacheEvict(cacheNames = "inventory", key = "#id")
            public void delete(Long id) { InventoryItem item = find(id); repository.delete(item); producer.publish("INVENTORY_DELETED", mapper.toResponse(item), ""); }
```

### F-003: Order-event consumption and stock adjustment are not idempotent

```yaml
finding:
  id: F-003
  title: Order-event consumption and stock adjustment are not idempotent
  severity: critical
  finding_status: verified
  primary_control: APP-AA-011
  primary_standard: springboot-aks-active-active-master
  related_controls: [KAFKA-003, KAFKA-AS-004, KAFKA-AS-006, SQL-004, GLB-013, JVM-019]
  observed_behavior: >-
    OrderEventConsumer maps ORDER_CREATED to service.reserve and ORDER_CANCELLED to service.release and
    passes the event orderId through as referenceId. reserve and release apply relative quantity deltas
    to the InventoryItem entity. referenceId is never persisted, never checked, and never used to derive
    a stable operation identity. No reservation record, processed-event table, unique constraint on
    (productId, referenceId), or conditional update guards a repeated application. The same gap applies
    to the POST /products/{productId}/reserve and /release REST endpoints.
  risk: >-
    At-least-once Kafka delivery, consumer rebalance, container restart, offset reset, active-standby
    promotion replay, and gateway or client retry of the POST endpoints all repeat the same business
    effect. Each repetition moves additional stock from available to reserved with no corrective path.
    Because auto-offset-reset is earliest, a lost or reset consumer group offset replays the entire
    retained order-events history, which would corrupt authoritative inventory quantities across both
    regions.
  implementation_boundary: >-
    Repository-owned: consumer deduplication, a durable operation-identity record, and conditional or
    guarded update semantics in InventoryServiceImpl. Out of boundary: broker retention policy, Cluster
    Linking offset synchronization, and gateway retry policy.
  finding_classification:
    type: resiliency
    qualification_status: qualified
    policy_id: RESILIENCY-FINDING-QUALIFICATION
    policy_version: "1.0.0"
    resiliency_domains: [recoverability, state_recovery, fault_tolerance, regional_failover]
    failure_scenario: >-
      An active-standby promotion restores consumption from a replicated or reset offset, or a rebalance
      redelivers uncommitted records after a pod restart.
    target_architecture_element: >-
      The order-events consumer group inventory-service and the Azure SQL authoritative inventory state
      in the approved active-standby target deployment.
    causal_mechanism: >-
      Relative quantity mutation without stable operation identity or duplicate detection means each
      redelivery is applied as a new business effect.
    material_impact: >-
      Replay during recovery silently corrupts authoritative stock quantities, which makes the documented
      failover procedure unsafe to execute.
    non_resiliency_category: not_applicable
    classification_rationale: >-
      The defect is only material because redelivery and replay are inherent to the target recovery
      model, placing the impact squarely in recoverability and state recovery.
  dependency_context:
    dependency: confluent-kafka
    operating_scenario: active_standby
    scenario_source: approved_application_architecture_context
    context_id: not_applicable
    context_version: "3.0.0"
    scenario_policy_id: KAFKA-OPERATING-SCENARIO
    scenario_policy_version: "3.2.0"
    scenario_rule_id: KAFKA-SCENARIO-001
    scenario_validation_status: consistent
    architecture_confirmation_required: false
    processing_model: mixed
    regional_processing_model: single_active
    external_side_effects: none
    kafka_backed_state: none
    conditional_assumptions: []
    related_state_dependencies: [azure-sql]
  repository_evidence:
    - evidence_id: EV-F-003-01
      repository_path: source/inventory-service/src/main/java/com/ecommerce/inventory/kafka/consumer/OrderEventConsumer.java
      symbol: OrderEventConsumer.consume
      source_language: java
      assessment_snapshot:
        type: workspace_snapshot
        identifier: "inventory-service-workspace-2026-09-18"
        provenance: workspace_generated
        git_commit_sha: not_applicable
        dirty_worktree: not_applicable
        captured_at: "2026-09-18T00:00:00Z"
        limitations: []
      source_fingerprint:
        algorithm: sha256
        normalization: exact_utf8_excerpt
        fingerprint_scope: exact_excerpt
        value: "f2448385d75dddda90a66a8f14c24be293a8598977f02d7139d1625ea498f4e9"
      original_line_range: {start_line: 13, end_line: 21, status: exact}
      evidence_purpose: primary
      original_source_excerpt: |
            @KafkaListener(topics = "order-events", groupId = "inventory-service")
            public void consume(Map<String, Object> event) {
                String type = String.valueOf(event.get("type"));
                String productId = String.valueOf(event.get("productId"));
                int quantity = ((Number) event.get("quantity")).intValue();
                String orderId = String.valueOf(event.get("orderId"));
                if ("ORDER_CREATED".equals(type)) service.reserve(productId, quantity, orderId);
                if ("ORDER_CANCELLED".equals(type)) service.release(productId, quantity, orderId);
            }
    - evidence_id: EV-F-003-02
      repository_path: source/inventory-service/src/main/java/com/ecommerce/inventory/service/impl/InventoryServiceImpl.java
      symbol: InventoryServiceImpl.reserve and InventoryServiceImpl.release
      source_language: java
      assessment_snapshot:
        type: workspace_snapshot
        identifier: "inventory-service-workspace-2026-09-18"
        provenance: workspace_generated
        git_commit_sha: not_applicable
        dirty_worktree: not_applicable
        captured_at: "2026-09-18T00:00:00Z"
        limitations: []
      source_fingerprint:
        algorithm: sha256
        normalization: exact_utf8_excerpt
        fingerprint_scope: exact_excerpt
        value: "0f2357c4e940ae72aaa92d8f2daf7677017121934274498c15ac4e150ebbafe4"
      original_line_range: {start_line: 37, end_line: 50, status: exact}
      evidence_purpose: primary
      original_source_excerpt: |
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
```

### F-004: Kafka listener has no region-role activation control

```yaml
finding:
  id: F-004
  title: Kafka listener has no region-role activation control
  severity: critical
  finding_status: verified
  primary_control: APP-KAFKA-001
  primary_standard: springboot-aks-active-active-master
  related_controls: [KAFKA-AS-001, KAFKA-AS-002, KAFKA-AS-003, KAFKA-AS-007, KAFKA-AS-008, KAFKA-010, KAFKA-012, APP-WORKLOAD-001, APP-WORKLOAD-002]
  observed_behavior: >-
    The @KafkaListener declares only topics and groupId. It has no id, no autoStartup attribute, no
    containerFactory reference, and no property-driven enablement. No KafkaListenerEndpointRegistry
    manipulation, lease acquisition, ownership epoch, fencing token, or SQL primary-role verification
    exists in production source. Consequently every started instance in every region begins consuming
    order-events immediately, and there is no repository-owned mechanism to start or stop consumption
    when the regional role changes.
  risk: >-
    The approved Kafka regional processing model is single_active and the authoritative Azure SQL state
    is active-standby. With no activation control, a standby-region deployment consumes and mutates
    authoritative inventory concurrently with the active region, and a stale former-active instance
    continues consuming after a promotion. Both conditions produce split-brain writes against a single
    authoritative database. The role change also cannot be applied by configuration alone, so a
    documented failover runbook would require a code change.
  implementation_boundary: >-
    Repository-owned: listener id and autoStartup contract, an externally configured activation
    property, ownership verification, and observable ownership state. Out of boundary: which region is
    designated active at deployment time, Azure SQL failover group role, and Kafka cluster promotion.
  finding_classification:
    type: resiliency
    qualification_status: qualified
    policy_id: RESILIENCY-FINDING-QUALIFICATION
    policy_version: "1.0.0"
    resiliency_domains: [workload_ownership, regional_failover, state_recovery, availability]
    failure_scenario: >-
      Both regional deployments are running during a planned or unplanned active-standby transition, or a
      former-active instance survives the transition.
    target_architecture_element: >-
      Single-active regional processing of the order-events consumer group against the Azure SQL primary
      in the approved active-standby target deployment.
    causal_mechanism: >-
      Unconditional listener auto-start with no ownership gate allows concurrent consumption from more
      than one regional role.
    material_impact: >-
      Concurrent authoritative writes from two regions during failover, plus an inability to execute a
      controlled role transfer without redeploying different code.
    non_resiliency_category: not_applicable
    classification_rationale: >-
      Directly defeats the approved regional failover and workload ownership model; the impact is
      specific to failover safety rather than to general design quality.
  dependency_context:
    dependency: confluent-kafka
    operating_scenario: active_standby
    scenario_source: approved_application_architecture_context
    context_id: not_applicable
    context_version: "3.0.0"
    scenario_policy_id: KAFKA-OPERATING-SCENARIO
    scenario_policy_version: "3.2.0"
    scenario_rule_id: KAFKA-SCENARIO-001
    scenario_validation_status: consistent
    architecture_confirmation_required: false
    processing_model: mixed
    regional_processing_model: single_active
    external_side_effects: none
    kafka_backed_state: none
    conditional_assumptions: []
    related_state_dependencies: [azure-sql]
  repository_evidence:
    - evidence_id: EV-F-004-01
      repository_path: source/inventory-service/src/main/java/com/ecommerce/inventory/kafka/consumer/OrderEventConsumer.java
      symbol: OrderEventConsumer @KafkaListener declaration
      source_language: java
      assessment_snapshot:
        type: workspace_snapshot
        identifier: "inventory-service-workspace-2026-09-18"
        provenance: workspace_generated
        git_commit_sha: not_applicable
        dirty_worktree: not_applicable
        captured_at: "2026-09-18T00:00:00Z"
        limitations: []
      source_fingerprint:
        algorithm: sha256
        normalization: exact_utf8_excerpt
        fingerprint_scope: exact_excerpt
        value: "3fb33358ad66f79a55d8159b7b75f84047f79eeff124770bdf2fc91b41219111"
      original_line_range: {start_line: 13, end_line: 14, status: exact}
      evidence_purpose: primary
      original_source_excerpt: |
            @KafkaListener(topics = "order-events", groupId = "inventory-service")
            public void consume(Map<String, Object> event) {
```

### F-005: Consumer offsets advance past records that fail permanently

```yaml
finding:
  id: F-005
  title: Consumer offsets advance past records that fail permanently
  severity: critical
  finding_status: verified
  primary_control: APP-KAFKA-002
  primary_standard: springboot-aks-active-active-master
  related_controls: [KAFKA-004]
  observed_behavior: >-
    The Kafka consumer configuration declares only auto-offset-reset, serializers, and trusted packages.
    No ack-mode, manual acknowledgment, listener container factory, or transactional.id is configured,
    so offset commit is governed entirely by Spring Kafka container defaults. Combined with the absence
    of any error handler or recoverer, a record whose processing exhausts the default attempt budget is
    skipped and its offset is committed.
  risk: >-
    Business work is discarded without a durable record. An ORDER_CREATED event that cannot be applied,
    for example because of a transient Azure SQL failure during a failover window, is retried inside the
    container and then abandoned, after which the offset advances. The reservation is never made, no
    durable terminal state records the loss, and the event cannot be located for replay because the
    consumer group has already moved past it.
  implementation_boundary: >-
    Repository-owned: listener container ack-mode and acknowledgment strategy, error-handler
    configuration, and the durable record of abandoned work. Out of boundary: broker offset retention
    and cross-cluster offset replication.
  finding_classification:
    type: resiliency
    qualification_status: qualified
    policy_id: RESILIENCY-FINDING-QUALIFICATION
    policy_version: "1.0.0"
    resiliency_domains: [durability, recoverability, state_recovery]
    failure_scenario: >-
      Azure SQL is briefly unavailable or returns a conflict while the consumer is processing an order
      event, and the container's default attempt budget is exhausted.
    target_architecture_element: >-
      The order-events consumer group inventory-service and the Azure SQL authoritative inventory state.
    causal_mechanism: >-
      Offset commit is decoupled from durable business completion, so a skipped record still advances the
      committed position.
    material_impact: >-
      Permanent silent loss of an inventory reservation or release with no recoverable position to replay
      from.
    non_resiliency_category: not_applicable
    classification_rationale: >-
      Loss occurs specifically as a consequence of dependency failure handling, placing the impact in
      durability and recoverability.
  dependency_context:
    dependency: confluent-kafka
    operating_scenario: active_standby
    scenario_source: approved_application_architecture_context
    context_id: not_applicable
    context_version: "3.0.0"
    scenario_policy_id: KAFKA-OPERATING-SCENARIO
    scenario_policy_version: "3.2.0"
    scenario_rule_id: KAFKA-SCENARIO-001
    scenario_validation_status: consistent
    architecture_confirmation_required: false
    processing_model: mixed
    regional_processing_model: single_active
    external_side_effects: none
    kafka_backed_state: none
    conditional_assumptions: []
    related_state_dependencies: [azure-sql]
  repository_evidence:
    - evidence_id: EV-F-005-01
      repository_path: source/inventory-service/src/main/resources/application.yml
      symbol: spring.kafka
      source_language: yaml
      assessment_snapshot:
        type: workspace_snapshot
        identifier: "inventory-service-workspace-2026-09-18"
        provenance: workspace_generated
        git_commit_sha: not_applicable
        dirty_worktree: not_applicable
        captured_at: "2026-09-18T00:00:00Z"
        limitations: []
      source_fingerprint:
        algorithm: sha256
        normalization: exact_utf8_excerpt
        fingerprint_scope: exact_excerpt
        value: "d249f7885663c10bfb25cac5530b32e398241519f204cdb12008192b9decfbbb"
      original_line_range: {start_line: 18, end_line: 28, status: exact}
      evidence_purpose: primary
      original_source_excerpt: |
          kafka:
            bootstrap-servers: ${KAFKA_BOOTSTRAP_SERVERS:localhost:9092}
            consumer:
              auto-offset-reset: earliest
              key-deserializer: org.apache.kafka.common.serialization.StringDeserializer
              value-deserializer: org.springframework.kafka.support.serializer.JsonDeserializer
              properties:
                spring.json.trusted.packages: "*"
            producer:
              key-serializer: org.apache.kafka.common.serialization.StringSerializer
              value-serializer: org.springframework.kafka.support.serializer.JsonSerializer
```

### F-006: Poison records have no dead-letter routing and payload extraction is unguarded

```yaml
finding:
  id: F-006
  title: Poison records have no dead-letter routing and payload extraction is unguarded
  severity: high
  finding_status: verified
  primary_control: APP-KAFKA-003
  primary_standard: springboot-aks-active-active-master
  related_controls: [KAFKA-006]
  observed_behavior: >-
    No CommonErrorHandler, DefaultErrorHandler bean, DeadLetterPublishingRecoverer, dead-letter topic,
    or retry topic is declared. Payload extraction reads untyped map values with String.valueOf and an
    unchecked (Number) cast on quantity, with no null check and no type guard, so a malformed or
    partially populated order event throws before any business validation occurs.
  risk: >-
    A single malformed order event repeatedly fails deserialization or extraction inside the listener.
    With no recoverer or quarantine destination the record is retried and then dropped by the container
    default, so the operator has no quarantined copy to inspect or reprocess. Because the same defect
    produces a NullPointerException or ClassCastException for every occurrence of the malformed shape, a
    systematic producer change can render the entire partition's traffic unprocessable with no
    diagnostic artifact.
  implementation_boundary: >-
    Repository-owned: listener container error-handler and recoverer configuration, dead-letter
    destination naming, and defensive payload extraction. Out of boundary: dead-letter topic
    provisioning, ACLs, and retention.
  finding_classification:
    type: resiliency
    qualification_status: qualified
    policy_id: RESILIENCY-FINDING-QUALIFICATION
    policy_version: "1.0.0"
    resiliency_domains: [fault_tolerance, availability, failure_observability]
    failure_scenario: >-
      An upstream producer emits an order event without a quantity field or with a non-numeric quantity.
    target_architecture_element: >-
      The order-events consumer group inventory-service.
    causal_mechanism: >-
      Unguarded extraction throws and no recoverer quarantines the record, so failure handling falls back
      entirely to container defaults with no durable artifact.
    material_impact: >-
      Loss of inventory reservation work with no quarantined record, and no bounded, observable recovery
      path for a repeating malformed payload.
    non_resiliency_category: not_applicable
    classification_rationale: >-
      The impact is the absence of a bounded fault-containment and recovery path for a dependency-borne
      failure, which is a fault tolerance concern rather than a general correctness concern.
  dependency_context:
    dependency: confluent-kafka
    operating_scenario: active_standby
    scenario_source: approved_application_architecture_context
    context_id: not_applicable
    context_version: "3.0.0"
    scenario_policy_id: KAFKA-OPERATING-SCENARIO
    scenario_policy_version: "3.2.0"
    scenario_rule_id: KAFKA-SCENARIO-001
    scenario_validation_status: consistent
    architecture_confirmation_required: false
    processing_model: mixed
    regional_processing_model: single_active
    external_side_effects: none
    kafka_backed_state: none
    conditional_assumptions: []
    related_state_dependencies: [azure-sql]
  repository_evidence:
    - evidence_id: EV-F-006-01
      repository_path: source/inventory-service/src/main/java/com/ecommerce/inventory/kafka/consumer/OrderEventConsumer.java
      symbol: OrderEventConsumer.consume payload extraction
      source_language: java
      assessment_snapshot:
        type: workspace_snapshot
        identifier: "inventory-service-workspace-2026-09-18"
        provenance: workspace_generated
        git_commit_sha: not_applicable
        dirty_worktree: not_applicable
        captured_at: "2026-09-18T00:00:00Z"
        limitations: []
      source_fingerprint:
        algorithm: sha256
        normalization: exact_utf8_excerpt
        fingerprint_scope: exact_excerpt
        value: "0411994fedf47dda64d0c69ab25fc6b2af4239a86311697c7a33e12873b89ca8"
      original_line_range: {start_line: 14, end_line: 18, status: exact}
      evidence_purpose: primary
      original_source_excerpt: |
            public void consume(Map<String, Object> event) {
                String type = String.valueOf(event.get("type"));
                String productId = String.valueOf(event.get("productId"));
                int quantity = ((Number) event.get("quantity")).intValue();
                String orderId = String.valueOf(event.get("orderId"));
```

### F-007: Published events carry no stable identity or correlation context

```yaml
finding:
  id: F-007
  title: Published events carry no stable identity or correlation context
  severity: high
  finding_status: verified
  primary_control: APP-KAFKA-006
  primary_standard: springboot-aks-active-active-master
  related_controls: [KAFKA-011, KAFKA-AS-006, APP-OBS-003]
  observed_behavior: >-
    The published payload contains type, occurredAt, referenceId, and the inventory response. No message
    id, event id, schema version, producing region, or trace context is present, and no RecordHeader is
    written. occurredAt is regenerated with Instant.now on every call, so a re-published event for the
    same business operation is not recognizable as the same event. No correlation identifier is
    persisted alongside the Azure SQL write or propagated from the consumed order event to the published
    inventory event.
  risk: >-
    Downstream consumers have no basis on which to deduplicate, which means every remediation that
    relies on republication or replay after a regional promotion propagates duplicates outward. During an
    incident there is no identifier that connects a consumed order event, the resulting SQL state
    change, and the published inventory event, so the divergence introduced by F-001 and F-002 cannot be
    traced or reconciled.
  implementation_boundary: >-
    Repository-owned: event envelope fields, Kafka record headers, and correlation propagation from the
    consumer through the service to the producer. Out of boundary: schema registry subject governance
    and downstream consumer deduplication implementations.
  finding_classification:
    type: resiliency
    qualification_status: qualified
    policy_id: RESILIENCY-FINDING-QUALIFICATION
    policy_version: "1.0.0"
    resiliency_domains: [recoverability, failure_observability, state_recovery]
    failure_scenario: >-
      After an active-standby promotion, events are replayed from a restored offset and downstream
      consumers receive the same business events again.
    target_architecture_element: >-
      The inventory-events durable event contract across regional roles.
    causal_mechanism: >-
      Event identity is regenerated per attempt and carries no stable business operation key, so
      duplicates are indistinguishable from new events.
    material_impact: >-
      Recovery actions that depend on replay cannot be performed safely, and cross-boundary incident
      correlation is impossible.
    non_resiliency_category: not_applicable
    classification_rationale: >-
      Identity and correlation gaps are material specifically because the target recovery model depends
      on replay and on tracing state divergence after failover.
  dependency_context:
    dependency: confluent-kafka
    operating_scenario: active_standby
    scenario_source: approved_application_architecture_context
    context_id: not_applicable
    context_version: "3.0.0"
    scenario_policy_id: KAFKA-OPERATING-SCENARIO
    scenario_policy_version: "3.2.0"
    scenario_rule_id: KAFKA-SCENARIO-001
    scenario_validation_status: consistent
    architecture_confirmation_required: false
    processing_model: mixed
    regional_processing_model: single_active
    external_side_effects: none
    kafka_backed_state: none
    conditional_assumptions: []
    related_state_dependencies: [azure-sql]
  repository_evidence:
    - evidence_id: EV-F-007-01
      repository_path: source/inventory-service/src/main/java/com/ecommerce/inventory/kafka/producer/InventoryEventProducer.java
      symbol: InventoryEventProducer.publish event envelope
      source_language: java
      assessment_snapshot:
        type: workspace_snapshot
        identifier: "inventory-service-workspace-2026-09-18"
        provenance: workspace_generated
        git_commit_sha: not_applicable
        dirty_worktree: not_applicable
        captured_at: "2026-09-18T00:00:00Z"
        limitations: []
      source_fingerprint:
        algorithm: sha256
        normalization: exact_utf8_excerpt
        fingerprint_scope: exact_excerpt
        value: "03e52ea3ceb6ce1190a0b09ce17bd46427d072dcbc314879c49ee1b24a2e77ac"
      original_line_range: {start_line: 15, end_line: 15, status: exact}
      evidence_purpose: primary
      original_source_excerpt: |
                kafkaTemplate.send("inventory-events", inventory.productId(), Map.of("type", type, "occurredAt", Instant.now().toString(), "referenceId", referenceId == null ? "" : referenceId, "inventory", inventory));
```

### F-008: Readiness and health configuration relies entirely on framework defaults

```yaml
finding:
  id: F-008
  title: Readiness and health configuration relies entirely on framework defaults
  severity: critical
  finding_status: verified
  primary_control: APP-AA-007
  primary_standard: springboot-aks-active-active-master
  related_controls: [APP-AA-009, SQL-006, SQL-015, REDIS-019, KV-014, KAFKA-007, GLB-002, GLB-004]
  observed_behavior: >-
    management.endpoint.health.probes.enabled is true and no readiness or liveness group include or
    exclude list is configured, so the readiness group resolves to the framework default that contains
    only the application availability state. The auto-configured Azure SQL, Redis, and Kafka health
    contributors therefore report into the aggregate health endpoint but do not participate in readiness.
    No custom HealthIndicator exists, no health-check timeout is configured for any contributor, and no
    production code publishes an AvailabilityChangeEvent or manipulates ReadinessState.
  risk: >-
    A sustained Azure SQL outage in the serving region leaves every pod reporting readiness UP, so the
    global load balancer continues to send traffic to a region that cannot serve its critical capability
    and regional traffic is never withdrawn. Because no code path can change readiness, the approved
    regional failover behaviour has no application-side trigger at all. The same defaults leave the
    dependency health checks unbounded, so during a dependency incident /actuator/health can block and
    add load to the failing dependency.
  implementation_boundary: >-
    Repository-owned: readiness and liveness group membership, health-check timeouts, a critical
    region-local serving health indicator, and explicit readiness-state transitions. Out of boundary:
    Kubernetes probe timing, global load balancer probe configuration, and deployed dependency topology.
  finding_classification:
    type: resiliency
    qualification_status: qualified
    policy_id: RESILIENCY-FINDING-QUALIFICATION
    policy_version: "1.0.0"
    resiliency_domains: [traffic_eligibility, availability, regional_failover, failure_observability]
    failure_scenario: >-
      Azure SQL becomes unavailable to the serving region while pods remain running and the load balancer
      keeps probing readiness.
    target_architecture_element: >-
      Regional traffic eligibility for the inventory-service pods behind the approved gateway and global
      load balancer.
    causal_mechanism: >-
      Default readiness group membership excludes every dependency contributor and no code path can
      change readiness, so dependency failure is never reflected in traffic eligibility.
    material_impact: >-
      The failing region continues to absorb traffic it cannot serve, defeating the regional failover
      objective.
    non_resiliency_category: not_applicable
    classification_rationale: >-
      Directly governs traffic eligibility and regional failover, which are approved resiliency domains,
      with a causal mechanism visible in repository-owned configuration.
  repository_evidence:
    - evidence_id: EV-F-008-01
      repository_path: source/inventory-service/src/main/resources/application.yml
      symbol: management.endpoints.web.exposure.include and management.endpoint.health.probes.enabled
      source_language: yaml
      assessment_snapshot:
        type: workspace_snapshot
        identifier: "inventory-service-workspace-2026-09-18"
        provenance: workspace_generated
        git_commit_sha: not_applicable
        dirty_worktree: not_applicable
        captured_at: "2026-09-18T00:00:00Z"
        limitations: []
      source_fingerprint:
        algorithm: sha256
        normalization: exact_utf8_excerpt
        fingerprint_scope: exact_excerpt
        value: "653a483edc8b2f53255c32fb9a607d3d9e8a7e5f543531165e9ff2230b5471f6"
      original_line_range: {start_line: 29, end_line: 37, status: exact}
      evidence_purpose: primary
      original_source_excerpt: |
        management:
          endpoints:
            web:
              exposure:
                include: health,info,prometheus
          endpoint:
            health:
              probes:
                enabled: true
    - evidence_id: EV-F-008-02
      repository_path: source/inventory-service/src/main/java
      symbol: absence of HealthIndicator, AvailabilityChangeEvent, and ReadinessState usage
      source_language: java
      assessment_snapshot:
        type: workspace_snapshot
        identifier: "inventory-service-workspace-2026-09-18"
        provenance: workspace_generated
        git_commit_sha: not_applicable
        dirty_worktree: not_applicable
        captured_at: "2026-09-18T00:00:00Z"
        limitations:
          - Absence evidence carried from the Step 1 inventory sections health_and_traffic_eligibility.custom_health_indicators and health_and_traffic_eligibility.readiness_state_control.
      source_fingerprint:
        algorithm: sha256
        normalization: exact_utf8_excerpt
        fingerprint_scope: exact_excerpt
        value: not_available
      original_line_range: {start_line: not_available, end_line: not_available, status: not_available}
      evidence_purpose: supporting
      original_source_excerpt: not_available
```

### F-009: Azure SQL access has no bounded timeouts

```yaml
finding:
  id: F-009
  title: Azure SQL access has no bounded timeouts
  severity: critical
  finding_status: verified
  primary_control: SQL-002
  primary_standard: azure-sql
  related_controls: [APP-AA-004, JVM-021]
  observed_behavior: >-
    The datasource configuration declares only url, username, and password. No HikariCP connection
    timeout, validation timeout, maximum lifetime, keepalive, or pool size is configured, no JDBC
    loginTimeout or socketTimeout is present in the connection string, no javax.persistence.query.timeout
    or Hibernate query timeout is set, and no @Transactional declares a timeout attribute. The prod
    profile supplies the entire URL through SQL_CONNECTION_STRING and adds no timeout property.
  risk: >-
    During an Azure SQL failover-group transition, connection acquisition, login, socket reads, query
    execution, and commit can each block for the driver or pool default. Request threads accumulate
    against the failing database, the service has no deadline at which it can fail cleanly, and the
    outer gateway timeout becomes the effective deadline. This converts a bounded database transition
    into an unbounded regional stall.
  implementation_boundary: >-
    Repository-owned: HikariCP properties, JDBC connection properties supplied through repository-owned
    configuration, JPA query timeout, and transaction timeout. Out of boundary: the resolved value of
    SQL_CONNECTION_STRING and the deployed failover-group configuration.
  finding_classification:
    type: resiliency
    qualification_status: qualified
    policy_id: RESILIENCY-FINDING-QUALIFICATION
    policy_version: "1.0.0"
    resiliency_domains: [availability, overload_protection, fault_tolerance, recovery]
    failure_scenario: >-
      An Azure SQL failover-group transition or network partition makes the database endpoint slow or
      unreachable for a period.
    target_architecture_element: >-
      The JDBC path from inventory-service to the Azure SQL authoritative business state.
    causal_mechanism: >-
      No repository-owned deadline exists at any layer, so every blocking database operation runs to the
      driver or pool default.
    material_impact: >-
      Unbounded request-thread occupancy and no clean failure point, which prevents timely regional
      failure detection and recovery.
    non_resiliency_category: not_applicable
    classification_rationale: >-
      Absent deadlines directly extend outage duration and block clean failure, which is an availability
      and recovery impact rather than a performance-tuning preference.
  repository_evidence:
    - evidence_id: EV-F-009-01
      repository_path: source/inventory-service/src/main/resources/application.yml
      symbol: spring.datasource
      source_language: yaml
      assessment_snapshot:
        type: workspace_snapshot
        identifier: "inventory-service-workspace-2026-09-18"
        provenance: workspace_generated
        git_commit_sha: not_applicable
        dirty_worktree: not_applicable
        captured_at: "2026-09-18T00:00:00Z"
        limitations: []
      source_fingerprint:
        algorithm: sha256
        normalization: exact_utf8_excerpt
        fingerprint_scope: exact_excerpt
        value: "e5de0c96c0169828ab9cf2747ececd749c083244d46003486999f23bde203f1b"
      original_line_range: {start_line: 6, end_line: 9, status: exact}
      evidence_purpose: primary
      original_source_excerpt: |
          datasource:
            url: ${SQL_URL:jdbc:sqlserver://localhost:1433;databaseName=inventory;encrypt=false}
            username: ${SQL_USERNAME}
            password: ${SQL_PASSWORD}
```

### F-010: Redis access has no bounded connect or command timeouts

```yaml
finding:
  id: F-010
  title: Redis access has no bounded connect or command timeouts
  severity: critical
  finding_status: verified
  primary_control: REDIS-005
  primary_standard: azure-managed-redis
  related_controls: [APP-AA-004]
  observed_behavior: >-
    Redis is configured only through spring.data.redis.url and spring.cache.type. No
    spring.data.redis.timeout, connect-timeout, Lettuce client configuration, command timeout, pool
    acquisition timeout, or topology refresh setting is present in either profile, and no
    LettuceClientConfigurationBuilderCustomizer exists in production source.
  risk: >-
    Every cached read performed through @Cacheable is subject to the Lettuce default command timeout
    with no repository-owned deadline. When Azure Managed Redis becomes slow rather than unavailable,
    request threads serving GET /api/v1/inventory/{id} block on the cache lookup even though the
    authoritative Azure SQL data is available, so a non-authoritative cache dependency extends the
    latency of an otherwise serviceable request.
  implementation_boundary: >-
    Repository-owned: Redis timeout and Lettuce client properties, and any client configuration
    customizer. Out of boundary: the resolved REDIS_CONNECTION_STRING value and deployed Redis capacity.
  finding_classification:
    type: resiliency
    qualification_status: qualified
    policy_id: RESILIENCY-FINDING-QUALIFICATION
    policy_version: "1.0.0"
    resiliency_domains: [availability, overload_protection, dependency_isolation]
    failure_scenario: >-
      Azure Managed Redis becomes slow or partially unreachable during a maintenance or failover event.
    target_architecture_element: >-
      The Spring cache path between the inventory REST read endpoint and Azure Managed Redis.
    causal_mechanism: >-
      No repository-owned command or connection deadline exists, so cache operations run to client
      defaults on request threads.
    material_impact: >-
      Latency of a non-authoritative dependency propagates into the serving path and consumes request
      capacity during a Redis incident.
    non_resiliency_category: not_applicable
    classification_rationale: >-
      The impact is degraded availability of a servable request path caused by an unbounded dependency
      call, which is an availability and isolation concern.
  repository_evidence:
    - evidence_id: EV-F-010-01
      repository_path: source/inventory-service/src/main/resources/application.yml
      symbol: spring.data.redis and spring.cache
      source_language: yaml
      assessment_snapshot:
        type: workspace_snapshot
        identifier: "inventory-service-workspace-2026-09-18"
        provenance: workspace_generated
        git_commit_sha: not_applicable
        dirty_worktree: not_applicable
        captured_at: "2026-09-18T00:00:00Z"
        limitations: []
      source_fingerprint:
        algorithm: sha256
        normalization: exact_utf8_excerpt
        fingerprint_scope: exact_excerpt
        value: "395445d5f6c099e3d0f67606b3e1dda3d04c4525898c449525cebd23300f16e6"
      original_line_range: {start_line: 13, end_line: 17, status: exact}
      evidence_purpose: primary
      original_source_excerpt: |
          data:
            redis:
              url: ${REDIS_URL:redis://localhost:6379}
          cache:
            type: redis
```

### F-011: Kafka client timeouts, reconnect, and backoff are unbounded by repository configuration

```yaml
finding:
  id: F-011
  title: Kafka client timeouts, reconnect, and backoff are unbounded by repository configuration
  severity: high
  finding_status: verified
  primary_control: KAFKA-005
  primary_standard: confluent-kafka
  related_controls: [APP-AA-004, JVM-021]
  observed_behavior: >-
    Neither profile declares request.timeout.ms, delivery.timeout.ms, max.block.ms,
    reconnect.backoff.ms, reconnect.backoff.max.ms, retry.backoff.ms, session.timeout.ms,
    heartbeat.interval.ms, max.poll.interval.ms, or max.poll.records. The prod profile adds only
    bootstrap-servers and security.protocol.
  risk: >-
    Producer sends can block on metadata acquisition for the client default while holding a request
    thread inside a database transaction, and consumer session and poll-interval behaviour during a
    regional Kafka transition is entirely implicit. Because the values are not expressed in
    repository-owned configuration, they cannot be aligned to the regional failure budget or tuned per
    environment without a code change.
  implementation_boundary: >-
    Repository-owned: spring.kafka.producer.properties and spring.kafka.consumer.properties entries and
    their externalization. Out of boundary: broker-side timeouts and deployed cluster behaviour.
  finding_classification:
    type: resiliency
    qualification_status: qualified
    policy_id: RESILIENCY-FINDING-QUALIFICATION
    policy_version: "1.0.0"
    resiliency_domains: [availability, fault_tolerance, overload_protection]
    failure_scenario: >-
      The regional Kafka cluster becomes unreachable while REST write traffic continues, so producer
      metadata acquisition blocks inside transactional service methods.
    target_architecture_element: >-
      Producer and consumer client behaviour against the regional Kafka cluster in the approved
      active-standby scenario.
    causal_mechanism: >-
      No repository-owned client deadline or backoff bound exists, so client defaults govern blocking and
      reconnect behaviour and cannot be aligned to the failure budget.
    material_impact: >-
      Broker unavailability can stall request threads and database transactions, and reconnect behaviour
      during failover is not tunable without a rebuild.
    non_resiliency_category: not_applicable
    classification_rationale: >-
      The impact is on bounded failure and recovery behaviour of a critical dependency, not on general
      configuration hygiene.
  dependency_context:
    dependency: confluent-kafka
    operating_scenario: active_standby
    scenario_source: approved_application_architecture_context
    context_id: not_applicable
    context_version: "3.0.0"
    scenario_policy_id: KAFKA-OPERATING-SCENARIO
    scenario_policy_version: "3.2.0"
    scenario_rule_id: KAFKA-SCENARIO-001
    scenario_validation_status: consistent
    architecture_confirmation_required: false
    processing_model: mixed
    regional_processing_model: single_active
    external_side_effects: none
    kafka_backed_state: none
    conditional_assumptions: []
    related_state_dependencies: [azure-sql]
  repository_evidence:
    - evidence_id: EV-F-011-01
      repository_path: source/inventory-service/src/main/resources/application-prod.yml
      symbol: spring.kafka
      source_language: yaml
      assessment_snapshot:
        type: workspace_snapshot
        identifier: "inventory-service-workspace-2026-09-18"
        provenance: workspace_generated
        git_commit_sha: not_applicable
        dirty_worktree: not_applicable
        captured_at: "2026-09-18T00:00:00Z"
        limitations: []
      source_fingerprint:
        algorithm: sha256
        normalization: exact_utf8_excerpt
        fingerprint_scope: exact_excerpt
        value: "92075e18bc37e4a0a6d6d2719105ad264262f8cf9ce91e304421aaa1bb2bf747"
      original_line_range: {start_line: 9, end_line: 12, status: exact}
      evidence_purpose: primary
      original_source_excerpt: |
          kafka:
            bootstrap-servers: ${KAFKA_BOOTSTRAP_SERVERS}
            properties:
              security.protocol: ${KAFKA_SECURITY_PROTOCOL:PLAINTEXT}
```

### F-012: No bounded retry exists for transient Azure SQL failures

```yaml
finding:
  id: F-012
  title: No bounded retry exists for transient Azure SQL failures
  severity: critical
  finding_status: verified
  primary_control: SQL-003
  primary_standard: azure-sql
  related_controls: [APP-AA-005]
  observed_behavior: >-
    No retry mechanism of any kind exists. The build declares no spring-retry, resilience4j, Spring
    Cloud Circuit Breaker, or equivalent dependency, and no production class declares @Retryable, builds
    a RetryTemplate, or wraps a transaction boundary in a retry policy. A transient SQLTransientException
    or connection reset therefore propagates out of the service method on the first occurrence.
  risk: >-
    Azure SQL failover-group transitions and transient connection resets are expected events in the
    approved deployment model. Without a bounded retry at a safe transaction boundary, every REST write
    fails outright and every consumed order event exhausts its container attempts and is abandoned under
    F-005. The service cannot ride through a normal database transition even when the database returns
    within seconds.
  implementation_boundary: >-
    Repository-owned: retry dependency selection, retry classification for transient versus terminal and
    ambiguous outcomes, retry placement at safe transaction boundaries, and externalized retry
    parameters. Out of boundary: failover-group transition duration and platform-level retry.
  finding_classification:
    type: resiliency
    qualification_status: qualified
    policy_id: RESILIENCY-FINDING-QUALIFICATION
    policy_version: "1.0.0"
    resiliency_domains: [retry_management, recovery, fault_tolerance, availability]
    failure_scenario: >-
      An Azure SQL failover-group transition briefly resets connections while REST and consumer traffic
      continues.
    target_architecture_element: >-
      Transactional write paths in InventoryServiceImpl against the Azure SQL authoritative state.
    causal_mechanism: >-
      No retry wraps any transaction boundary, so a transient and self-healing database condition becomes
      a terminal application failure.
    material_impact: >-
      Routine database transitions cause user-visible write failures and abandoned event processing.
    non_resiliency_category: not_applicable
    classification_rationale: >-
      Retry management is an approved resiliency domain and the failure scenario is an expected event in
      the approved target deployment model.
  repository_evidence:
    - evidence_id: EV-F-012-01
      repository_path: source/inventory-service/pom.xml
      symbol: project/dependencies
      source_language: xml
      assessment_snapshot:
        type: workspace_snapshot
        identifier: "inventory-service-workspace-2026-09-18"
        provenance: workspace_generated
        git_commit_sha: not_applicable
        dirty_worktree: not_applicable
        captured_at: "2026-09-18T00:00:00Z"
        limitations: []
      source_fingerprint:
        algorithm: sha256
        normalization: exact_utf8_excerpt
        fingerprint_scope: exact_excerpt
        value: "d1af2cf103de040ee5932ef455e58ec46fd6409bfba9ea02838287f980a47ecd"
      original_line_range: {start_line: 7, end_line: 26, status: exact}
      evidence_purpose: primary
      original_source_excerpt: |
            <dependencies>
                <dependency><groupId>org.springframework.boot</groupId><artifactId>spring-boot-starter-web</artifactId></dependency>
                <dependency><groupId>org.springframework.boot</groupId><artifactId>spring-boot-starter-validation</artifactId></dependency>
                <dependency><groupId>org.springframework.boot</groupId><artifactId>spring-boot-starter-actuator</artifactId></dependency>
                <dependency><groupId>org.springframework.boot</groupId><artifactId>spring-boot-starter-data-jpa</artifactId></dependency>
                <dependency><groupId>org.springframework.boot</groupId><artifactId>spring-boot-starter-data-redis</artifactId></dependency>
                <dependency><groupId>org.springframework.boot</groupId><artifactId>spring-boot-starter-cache</artifactId></dependency>
                <dependency><groupId>org.springframework.kafka</groupId><artifactId>spring-kafka</artifactId></dependency>
                <dependency><groupId>com.microsoft.sqlserver</groupId><artifactId>mssql-jdbc</artifactId><scope>runtime</scope></dependency>
                <dependency><groupId>com.azure.spring</groupId><artifactId>spring-cloud-azure-starter-keyvault-secrets</artifactId></dependency>
                <dependency><groupId>org.springdoc</groupId><artifactId>springdoc-openapi-starter-webmvc-ui</artifactId><version>2.6.0</version></dependency>
                <dependency><groupId>io.micrometer</groupId><artifactId>micrometer-registry-prometheus</artifactId></dependency>
                <dependency><groupId>net.logstash.logback</groupId><artifactId>logstash-logback-encoder</artifactId><version>8.0</version></dependency>
                <dependency><groupId>org.mapstruct</groupId><artifactId>mapstruct</artifactId><version>${mapstruct.version}</version></dependency>
                <dependency><groupId>org.projectlombok</groupId><artifactId>lombok</artifactId><optional>true</optional></dependency>
                <dependency><groupId>org.springframework.boot</groupId><artifactId>spring-boot-starter-test</artifactId><scope>test</scope></dependency>
                <dependency><groupId>org.springframework.kafka</groupId><artifactId>spring-kafka-test</artifactId><scope>test</scope></dependency>
                <dependency><groupId>org.testcontainers</groupId><artifactId>junit-jupiter</artifactId><version>${testcontainers.version}</version><scope>test</scope></dependency>
                <dependency><groupId>org.testcontainers</groupId><artifactId>mssqlserver</artifactId><version>${testcontainers.version}</version><scope>test</scope></dependency>
            </dependencies>
    - evidence_id: EV-F-012-02
      repository_path: source/inventory-service/src/main/java/com/ecommerce/inventory/service/impl/InventoryServiceImpl.java
      symbol: InventoryServiceImpl.release
      source_language: java
      assessment_snapshot:
        type: workspace_snapshot
        identifier: "inventory-service-workspace-2026-09-18"
        provenance: workspace_generated
        git_commit_sha: not_applicable
        dirty_worktree: not_applicable
        captured_at: "2026-09-18T00:00:00Z"
        limitations: []
      source_fingerprint:
        algorithm: sha256
        normalization: exact_utf8_excerpt
        fingerprint_scope: exact_excerpt
        value: "b83ea6804189eda80504680e18a8e5d142666b78feb552b48057aac1162f3989"
      original_line_range: {start_line: 44, end_line: 50, status: exact}
      evidence_purpose: supporting
      original_source_excerpt: |
            @Override @Transactional
            public InventoryResponse release(String productId, int quantity, String referenceId) {
                InventoryItem item = findByProduct(productId);
                if (item.getReservedQuantity() < quantity) throw new IllegalArgumentException("Release exceeds reserved inventory for product: " + productId);
                item.setReservedQuantity(item.getReservedQuantity() - quantity); item.setAvailableQuantity(item.getAvailableQuantity() + quantity); item.setUpdatedAt(Instant.now());
                return saveAndPublish(item, "INVENTORY_RELEASED", referenceId);
            }
```

### F-013: Optimistic-locking conflicts are neither detected, retried, nor mapped

```yaml
finding:
  id: F-013
  title: Optimistic-locking conflicts are neither detected, retried, nor mapped
  severity: high
  finding_status: verified
  primary_control: SQL-007
  primary_standard: azure-sql
  related_controls: [APP-AA-012]
  observed_behavior: >-
    InventoryItem declares an @Version column, so concurrent updates to the same row raise
    ObjectOptimisticLockingFailureException at flush or commit. No service method catches it, no retry
    reloads and reapplies the adjustment, no pessimistic lock or conditional update is used on the
    reserve and release paths, and GlobalExceptionHandler maps only ResourceNotFoundException,
    IllegalArgumentException, and MethodArgumentNotValidException.
  risk: >-
    Two concurrent reservations for the same productId, which is the normal pattern when REST traffic
    and Kafka consumption both adjust the same item, cause one operation to fail with an unmapped
    exception surfaced as HTTP 500 or, on the consumer path, an exhausted attempt budget and an
    abandoned record under F-005. Optimistic locking prevents a lost update but the absence of conflict
    handling converts an ordinary contention event into lost business work.
  implementation_boundary: >-
    Repository-owned: conflict detection, bounded reload-and-reapply retry, and exception-to-response
    mapping. Out of boundary: database isolation level configuration deployed at the server.
  finding_classification:
    type: resiliency
    qualification_status: qualified
    policy_id: RESILIENCY-FINDING-QUALIFICATION
    policy_version: "1.0.0"
    resiliency_domains: [fault_tolerance, recoverability]
    failure_scenario: >-
      A REST reservation and a consumed ORDER_CREATED event adjust the same inventory row concurrently.
    target_architecture_element: >-
      Concurrent write paths against the single Azure SQL authoritative inventory row.
    causal_mechanism: >-
      The version conflict is raised by the persistence layer but no application path absorbs, retries,
      or reports it, so contention becomes terminal failure.
    material_impact: >-
      Routine contention discards inventory reservations and produces unhandled failures on both the
      REST and consumer paths.
    non_resiliency_category: not_applicable
    classification_rationale: >-
      Conflict handling failure is material because it causes work loss under normal concurrent
      operation, which is a fault tolerance and recoverability impact.
  repository_evidence:
    - evidence_id: EV-F-013-01
      repository_path: source/inventory-service/src/main/java/com/ecommerce/inventory/model/InventoryItem.java
      symbol: InventoryItem.version
      source_language: java
      assessment_snapshot:
        type: workspace_snapshot
        identifier: "inventory-service-workspace-2026-09-18"
        provenance: workspace_generated
        git_commit_sha: not_applicable
        dirty_worktree: not_applicable
        captured_at: "2026-09-18T00:00:00Z"
        limitations: []
      source_fingerprint:
        algorithm: sha256
        normalization: exact_utf8_excerpt
        fingerprint_scope: exact_excerpt
        value: "5e29c55e63ae5f984a5a875a87980656b30c6cb572f0499822fc50589ea074ea"
      original_line_range: {start_line: 26, end_line: 26, status: exact}
      evidence_purpose: primary
      original_source_excerpt: |
            @Version private long version;
    - evidence_id: EV-F-013-02
      repository_path: source/inventory-service/src/main/java/com/ecommerce/inventory/exception/GlobalExceptionHandler.java
      symbol: GlobalExceptionHandler
      source_language: java
      assessment_snapshot:
        type: workspace_snapshot
        identifier: "inventory-service-workspace-2026-09-18"
        provenance: workspace_generated
        git_commit_sha: not_applicable
        dirty_worktree: not_applicable
        captured_at: "2026-09-18T00:00:00Z"
        limitations:
          - The Step 1 inventory cited lines 12-22 with status exact; the assessed file contains 21 lines. Corrected to 12-21 and recorded as inventory exception EXC-A-001.
      source_fingerprint:
        algorithm: sha256
        normalization: exact_utf8_excerpt
        fingerprint_scope: exact_excerpt
        value: "c2bc4b46127d9c7fe09cd5784943e3ffbeae121dd7cd6137fd79a7f3db1a0940"
      original_line_range: {start_line: 12, end_line: 21, status: exact}
      evidence_purpose: supporting
      original_source_excerpt: |
        @RestControllerAdvice
        public class GlobalExceptionHandler {
            @ExceptionHandler(ResourceNotFoundException.class)
            ResponseEntity<Map<String, Object>> notFound(ResourceNotFoundException exception) { return error(HttpStatus.NOT_FOUND, exception.getMessage()); }
            @ExceptionHandler({IllegalArgumentException.class, MethodArgumentNotValidException.class})
            ResponseEntity<Map<String, Object>> badRequest(Exception exception) { return error(HttpStatus.BAD_REQUEST, exception.getMessage()); }
            private ResponseEntity<Map<String, Object>> error(HttpStatus status, String message) {
                return ResponseEntity.status(status).body(Map.of("timestamp", Instant.now().toString(), "status", status.value(), "error", status.getReasonPhrase(), "message", message));
            }
        }
```

### F-014: Dependency failures have no stable caller-visible semantics

```yaml
finding:
  id: F-014
  title: Dependency failures have no stable caller-visible semantics
  severity: high
  finding_status: verified
  primary_control: APP-WEB-002
  primary_standard: springboot-aks-active-active-master
  related_controls: []
  observed_behavior: >-
    GlobalExceptionHandler maps only three exception types. DataAccessException, Hikari pool exhaustion,
    RedisConnectionFailureException, RedisCommandTimeoutException, Spring cache serialization failures,
    and Kafka client exceptions all fall through to the framework default error handling and surface as
    an opaque HTTP 500 with no Retry-After, no ProblemDetail, and no distinction between a permanent
    error and a transient dependency outage.
  risk: >-
    Callers and the gateway cannot distinguish a transient regional dependency failure from a permanent
    application error, so no caller can make a safe retry or failover decision. During a regional
    dependency incident the API returns the same opaque status for a request that would succeed in the
    peer region as for one that would fail everywhere, which suppresses the signal the approved
    multi-region routing design depends on.
  implementation_boundary: >-
    Repository-owned: exception-to-status mapping in GlobalExceptionHandler and the error response
    contract. Out of boundary: gateway retry policy and client behaviour.
  finding_classification:
    type: resiliency
    qualification_status: qualified
    policy_id: RESILIENCY-FINDING-QUALIFICATION
    policy_version: "1.0.0"
    resiliency_domains: [fault_tolerance, availability, failure_observability]
    failure_scenario: >-
      Azure SQL or Redis becomes unavailable in the serving region while the peer region remains
      healthy.
    target_architecture_element: >-
      The caller-visible HTTP contract of /api/v1/inventory behind the approved gateway and global load
      balancer.
    causal_mechanism: >-
      Unmapped dependency exceptions collapse into an undifferentiated 500, removing the transient-versus-terminal
      signal that retry and routing decisions require.
    material_impact: >-
      Callers and the gateway cannot retry or reroute correctly during a regional dependency incident.
    non_resiliency_category: not_applicable
    classification_rationale: >-
      The impact is on failure signalling that the approved regional routing model depends on, not on
      general API design preference.
  repository_evidence:
    - evidence_id: EV-F-014-01
      repository_path: source/inventory-service/src/main/java/com/ecommerce/inventory/exception/GlobalExceptionHandler.java
      symbol: GlobalExceptionHandler exception coverage
      source_language: java
      assessment_snapshot:
        type: workspace_snapshot
        identifier: "inventory-service-workspace-2026-09-18"
        provenance: workspace_generated
        git_commit_sha: not_applicable
        dirty_worktree: not_applicable
        captured_at: "2026-09-18T00:00:00Z"
        limitations:
          - The Step 1 inventory cited lines 12-22 with status exact; the assessed file contains 21 lines. Corrected to 12-21 and recorded as inventory exception EXC-A-001.
      source_fingerprint:
        algorithm: sha256
        normalization: exact_utf8_excerpt
        fingerprint_scope: exact_excerpt
        value: "c2bc4b46127d9c7fe09cd5784943e3ffbeae121dd7cd6137fd79a7f3db1a0940"
      original_line_range: {start_line: 12, end_line: 21, status: exact}
      evidence_purpose: primary
      original_source_excerpt: |
        @RestControllerAdvice
        public class GlobalExceptionHandler {
            @ExceptionHandler(ResourceNotFoundException.class)
            ResponseEntity<Map<String, Object>> notFound(ResourceNotFoundException exception) { return error(HttpStatus.NOT_FOUND, exception.getMessage()); }
            @ExceptionHandler({IllegalArgumentException.class, MethodArgumentNotValidException.class})
            ResponseEntity<Map<String, Object>> badRequest(Exception exception) { return error(HttpStatus.BAD_REQUEST, exception.getMessage()); }
            private ResponseEntity<Map<String, Object>> error(HttpStatus status, String message) {
                return ResponseEntity.status(status).body(Map.of("timestamp", Instant.now().toString(), "status", status.value(), "error", status.getReasonPhrase(), "message", message));
            }
        }
```

### F-015: No isolation exists between request threads and blocking dependencies

```yaml
finding:
  id: F-015
  title: No isolation exists between request threads and blocking dependencies
  severity: high
  finding_status: verified
  primary_control: APP-AA-006
  primary_standard: springboot-aks-active-active-master
  related_controls: [REDIS-008, JVM-010]
  observed_behavior: >-
    The build declares no resilience4j, Spring Cloud Circuit Breaker, Hystrix, or rate-limiter
    dependency, and production source defines no bulkhead, semaphore, or custom executor. All REST
    request processing, cache access, database access, and Kafka production execute on the default
    servlet container thread pool, whose default size is far larger than the default HikariCP pool with
    no rejection policy or queue bound between them.
  risk: >-
    A single degraded dependency consumes the entire shared request-thread pool. A slow Redis or a
    blocked Azure SQL pool causes every servlet thread to park, so read endpoints that do not touch the
    failing dependency, and the Actuator endpoints served on the same port, also stop responding. One
    dependency failure therefore removes the whole pod from service rather than degrading a single
    capability.
  implementation_boundary: >-
    Repository-owned: circuit-breaker or bulkhead introduction, per-dependency concurrency limits, and
    externalized thresholds. Out of boundary: pod CPU and memory limits and mesh-level outlier
    detection.
  finding_classification:
    type: resiliency
    qualification_status: qualified
    policy_id: RESILIENCY-FINDING-QUALIFICATION
    policy_version: "1.0.0"
    resiliency_domains: [dependency_isolation, overload_protection, availability]
    failure_scenario: >-
      Azure Managed Redis or Azure SQL becomes slow while REST traffic continues at normal volume.
    target_architecture_element: >-
      The shared servlet request-thread pool serving both business endpoints and Actuator probes.
    causal_mechanism: >-
      Every dependency call is made on the shared request pool with no concurrency limit, so one slow
      dependency exhausts capacity for all others.
    material_impact: >-
      A single dependency degradation removes the entire pod, and the region, from service.
    non_resiliency_category: not_applicable
    classification_rationale: >-
      Dependency isolation and overload protection are approved resiliency domains and the blast radius
      is regional loss of service.
  repository_evidence:
    - evidence_id: EV-F-015-01
      repository_path: source/inventory-service/pom.xml
      symbol: project/dependencies
      source_language: xml
      assessment_snapshot:
        type: workspace_snapshot
        identifier: "inventory-service-workspace-2026-09-18"
        provenance: workspace_generated
        git_commit_sha: not_applicable
        dirty_worktree: not_applicable
        captured_at: "2026-09-18T00:00:00Z"
        limitations:
          - Shares the same assessed excerpt as EV-F-012-01; the two findings cite it for different control violations.
      source_fingerprint:
        algorithm: sha256
        normalization: exact_utf8_excerpt
        fingerprint_scope: exact_excerpt
        value: "d1af2cf103de040ee5932ef455e58ec46fd6409bfba9ea02838287f980a47ecd"
      original_line_range: {start_line: 7, end_line: 26, status: exact}
      evidence_purpose: primary
      original_source_excerpt: |
            <dependencies>
                <dependency><groupId>org.springframework.boot</groupId><artifactId>spring-boot-starter-web</artifactId></dependency>
                <dependency><groupId>org.springframework.boot</groupId><artifactId>spring-boot-starter-validation</artifactId></dependency>
                <dependency><groupId>org.springframework.boot</groupId><artifactId>spring-boot-starter-actuator</artifactId></dependency>
                <dependency><groupId>org.springframework.boot</groupId><artifactId>spring-boot-starter-data-jpa</artifactId></dependency>
                <dependency><groupId>org.springframework.boot</groupId><artifactId>spring-boot-starter-data-redis</artifactId></dependency>
                <dependency><groupId>org.springframework.boot</groupId><artifactId>spring-boot-starter-cache</artifactId></dependency>
                <dependency><groupId>org.springframework.kafka</groupId><artifactId>spring-kafka</artifactId></dependency>
                <dependency><groupId>com.microsoft.sqlserver</groupId><artifactId>mssql-jdbc</artifactId><scope>runtime</scope></dependency>
                <dependency><groupId>com.azure.spring</groupId><artifactId>spring-cloud-azure-starter-keyvault-secrets</artifactId></dependency>
                <dependency><groupId>org.springdoc</groupId><artifactId>springdoc-openapi-starter-webmvc-ui</artifactId><version>2.6.0</version></dependency>
                <dependency><groupId>io.micrometer</groupId><artifactId>micrometer-registry-prometheus</artifactId></dependency>
                <dependency><groupId>net.logstash.logback</groupId><artifactId>logstash-logback-encoder</artifactId><version>8.0</version></dependency>
                <dependency><groupId>org.mapstruct</groupId><artifactId>mapstruct</artifactId><version>${mapstruct.version}</version></dependency>
                <dependency><groupId>org.projectlombok</groupId><artifactId>lombok</artifactId><optional>true</optional></dependency>
                <dependency><groupId>org.springframework.boot</groupId><artifactId>spring-boot-starter-test</artifactId><scope>test</scope></dependency>
                <dependency><groupId>org.springframework.kafka</groupId><artifactId>spring-kafka-test</artifactId><scope>test</scope></dependency>
                <dependency><groupId>org.testcontainers</groupId><artifactId>junit-jupiter</artifactId><version>${testcontainers.version}</version><scope>test</scope></dependency>
                <dependency><groupId>org.testcontainers</groupId><artifactId>mssqlserver</artifactId><version>${testcontainers.version}</version><scope>test</scope></dependency>
            </dependencies>
```

### F-016: Redis cache failures propagate into the request path with no error handler

```yaml
finding:
  id: F-016
  title: Redis cache failures propagate into the request path with no error handler
  severity: critical
  finding_status: verified
  primary_control: REDIS-020
  primary_standard: azure-managed-redis
  related_controls: [APP-AA-006]
  observed_behavior: >-
    CacheConfig declares @EnableCaching with no body. It does not implement CachingConfigurer, registers
    no CacheErrorHandler, and supplies no RedisCacheManager. With spring.cache.type set to redis, any
    Redis get, put, or evict failure raised by the Spring cache interceptor therefore propagates to the
    caller instead of being absorbed and falling through to the authoritative Azure SQL repository.
  risk: >-
    Azure Managed Redis is a cache whose authoritative source is Azure SQL, yet a Redis outage makes
    GET /api/v1/inventory/{id} fail outright even though the authoritative data is fully available.
    Cache eviction failures on update and delete propagate the same way and can fail an otherwise
    successful write. A non-authoritative dependency is therefore able to take down a serviceable
    capability in the region.
  implementation_boundary: >-
    Repository-owned: a CacheErrorHandler or CachingConfigurer implementation, degraded-mode behaviour,
    and telemetry distinguishing cache failure from cache miss. Out of boundary: Azure Managed Redis
    availability and deployed topology.
  finding_classification:
    type: resiliency
    qualification_status: qualified
    policy_id: RESILIENCY-FINDING-QUALIFICATION
    policy_version: "1.0.0"
    resiliency_domains: [fault_tolerance, availability, dependency_isolation]
    failure_scenario: >-
      Azure Managed Redis is unavailable or times out while Azure SQL remains healthy.
    target_architecture_element: >-
      The cached read path for inventory items served from the approved regional deployment.
    causal_mechanism: >-
      No CacheErrorHandler is registered, so the Spring cache interceptor rethrows Redis failures instead
      of falling through to the authoritative repository.
    material_impact: >-
      A cache-tier outage causes full failure of a read capability whose authoritative data is available,
      unnecessarily converting a degraded condition into an outage.
    non_resiliency_category: not_applicable
    classification_rationale: >-
      The impact is loss of availability caused by absent fault containment around a non-authoritative
      dependency, which is squarely a fault tolerance and isolation concern.
  repository_evidence:
    - evidence_id: EV-F-016-01
      repository_path: source/inventory-service/src/main/java/com/ecommerce/inventory/config/CacheConfig.java
      symbol: CacheConfig
      source_language: java
      assessment_snapshot:
        type: workspace_snapshot
        identifier: "inventory-service-workspace-2026-09-18"
        provenance: workspace_generated
        git_commit_sha: not_applicable
        dirty_worktree: not_applicable
        captured_at: "2026-09-18T00:00:00Z"
        limitations: []
      source_fingerprint:
        algorithm: sha256
        normalization: exact_utf8_excerpt
        fingerprint_scope: exact_excerpt
        value: "a6a2631175d32371721dbb655166cbd6e505087d9b108c87fd719d65e3e2af65"
      original_line_range: {start_line: 6, end_line: 8, status: exact}
      evidence_purpose: primary
      original_source_excerpt: |
        @Configuration @EnableCaching
        public class CacheConfig {
        }
```

### F-017: Cached entries have no TTL or expiration policy

```yaml
finding:
  id: F-017
  title: Cached entries have no TTL or expiration policy
  severity: high
  finding_status: verified
  primary_control: REDIS-011
  primary_standard: azure-managed-redis
  related_controls: [APP-CACHE-001]
  observed_behavior: >-
    spring.cache.type is set to redis with no spring.cache.redis.time-to-live, no per-cache
    RedisCacheConfiguration, and no entryTtl on any cache. CacheConfig supplies no RedisCacheManager, so
    inventory cache entries are written without expiry and persist until they are explicitly evicted or
    until Redis evicts them under memory pressure.
  risk: >-
    Cache entries accumulate without bound across the lifetime of the deployment and are only removed by
    an explicit evict on update or delete. Entries for items mutated through reserve and release are
    never evicted at all under F-020, so they persist indefinitely. Growth is limited only by the
    deployed Redis maxmemory policy, at which point eviction behaviour becomes non-deterministic, and
    there is no bounded freshness window that would let a regional cache converge after a failover.
  implementation_boundary: >-
    Repository-owned: TTL configuration and its externalization, and per-cache RedisCacheConfiguration.
    Out of boundary: Azure Managed Redis maxmemory policy and capacity.
  finding_classification:
    type: resiliency
    qualification_status: qualified
    policy_id: RESILIENCY-FINDING-QUALIFICATION
    policy_version: "1.0.0"
    resiliency_domains: [availability, recovery]
    failure_scenario: >-
      Cache entries accumulate over a long-running deployment until Azure Managed Redis reaches its
      memory limit, or a regional failover leaves stale entries with no expiry to converge them.
    target_architecture_element: >-
      The inventory cache backing the regional read path.
    causal_mechanism: >-
      No expiry is configured, so entries persist indefinitely and staleness has no bounded window.
    material_impact: >-
      Non-deterministic eviction under memory pressure and unbounded staleness after a regional
      transition.
    non_resiliency_category: not_applicable
    classification_rationale: >-
      The impact is bounded-degradation behaviour of the cache tier during capacity pressure and regional
      recovery rather than a general tuning preference.
  repository_evidence:
    - evidence_id: EV-F-017-01
      repository_path: source/inventory-service/src/main/resources/application.yml
      symbol: spring.cache
      source_language: yaml
      assessment_snapshot:
        type: workspace_snapshot
        identifier: "inventory-service-workspace-2026-09-18"
        provenance: workspace_generated
        git_commit_sha: not_applicable
        dirty_worktree: not_applicable
        captured_at: "2026-09-18T00:00:00Z"
        limitations: []
      source_fingerprint:
        algorithm: sha256
        normalization: exact_utf8_excerpt
        fingerprint_scope: exact_excerpt
        value: "5921b25eb1c9acfac5e43cb0c833f6ea37f042b0ee97ebe1c05de562013e3bee"
      original_line_range: {start_line: 16, end_line: 17, status: exact}
      evidence_purpose: primary
      original_source_excerpt: |
          cache:
            type: redis
```

### F-018: Cache keys have no namespace, environment scope, or schema version

```yaml
finding:
  id: F-018
  title: Cache keys have no namespace, environment scope, or schema version
  severity: high
  finding_status: verified
  primary_control: REDIS-022
  primary_standard: azure-managed-redis
  related_controls: []
  observed_behavior: >-
    The only cache name is inventory and the key expression is the raw entity identifier. No key prefix,
    environment qualifier, tenant qualifier, or payload schema version is configured, so keys resolve to
    the framework default cache-name prefix followed by the numeric id.
  risk: >-
    Any two deployments that share a Redis instance or database index, for example a non-production and
    a production deployment or two application versions during a rolling release, write to identical
    keys. A cached value produced by one payload shape is then read by code expecting a different shape.
    There is also no way to invalidate a generation of cached values when the response model changes,
    other than flushing the shared instance.
  implementation_boundary: >-
    Repository-owned: cache key prefix, environment and version qualifiers, and per-cache key
    generation. Out of boundary: whether a Redis instance or database index is actually shared between
    environments, which is deployment configuration.
  finding_classification:
    type: non_resiliency
    qualification_status: not_qualified
    policy_id: RESILIENCY-FINDING-QUALIFICATION
    policy_version: "1.0.0"
    resiliency_domains: []
    failure_scenario: not_applicable
    target_architecture_element: not_applicable
    causal_mechanism: not_applicable
    material_impact: not_applicable
    non_resiliency_category: contract
    classification_rationale: >-
      The control violation is evidence-backed, but the impact is cache-contract and data-model hygiene,
      including cross-environment contamination and version reuse, rather than a failure-mode impact on
      an approved resiliency domain. Retained as non_resiliency in accordance with the qualification
      policy.
  repository_evidence:
    - evidence_id: EV-F-018-01
      repository_path: source/inventory-service/src/main/java/com/ecommerce/inventory/service/impl/InventoryServiceImpl.java
      symbol: InventoryServiceImpl.get @Cacheable
      source_language: java
      assessment_snapshot:
        type: workspace_snapshot
        identifier: "inventory-service-workspace-2026-09-18"
        provenance: workspace_generated
        git_commit_sha: not_applicable
        dirty_worktree: not_applicable
        captured_at: "2026-09-18T00:00:00Z"
        limitations: []
      source_fingerprint:
        algorithm: sha256
        normalization: exact_utf8_excerpt
        fingerprint_scope: exact_excerpt
        value: "af81ef398962c1d6360ab1362e5147578fd509562c148022a7a917a1b3f71ddf"
      original_line_range: {start_line: 30, end_line: 31, status: exact}
      evidence_purpose: primary
      original_source_excerpt: |
            @Override @Cacheable(cacheNames = "inventory", key = "#id")
            public InventoryResponse get(Long id) { return mapper.toResponse(find(id)); }
```

### F-019: Concurrent cache misses are not coalesced

```yaml
finding:
  id: F-019
  title: Concurrent cache misses are not coalesced
  severity: high
  finding_status: verified
  primary_control: REDIS-009
  primary_standard: azure-managed-redis
  related_controls: [APP-CACHE-004]
  observed_behavior: >-
    @Cacheable is declared without sync, and no single-flight, lock, or SETNX guard exists around the
    cache loader. Every concurrent miss for the same key therefore executes its own repository.findById
    against Azure SQL.
  risk: >-
    A cold start, a Redis restart, a regional cache that has not yet been populated after a failover, or
    a burst of traffic for a popular product causes every concurrent request to fan out to Azure SQL at
    once. This happens precisely when the database is most likely to be recovering, and combined with
    the absence of any bulkhead in F-015 it can exhaust the connection pool and the request threads at
    the same moment.
  implementation_boundary: >-
    Repository-owned: cache loader coalescing through sync or an equivalent single-flight mechanism. Out
    of boundary: Redis capacity and Azure SQL server-side concurrency limits.
  finding_classification:
    type: resiliency
    qualification_status: qualified
    policy_id: RESILIENCY-FINDING-QUALIFICATION
    policy_version: "1.0.0"
    resiliency_domains: [overload_protection, availability, recovery]
    failure_scenario: >-
      A regional cache is empty immediately after a failover or Redis restart while normal read traffic
      resumes.
    target_architecture_element: >-
      The cache-aside read path between the inventory read endpoint and Azure SQL.
    causal_mechanism: >-
      Uncoalesced misses convert each concurrent request into an independent authoritative-store read.
    material_impact: >-
      A recovering database is hit by a concurrent load spike at the moment it is least able to absorb
      it, extending the regional recovery window.
    non_resiliency_category: not_applicable
    classification_rationale: >-
      Stampede protection is an overload-protection and recovery concern, and the failure scenario is a
      normal consequence of the approved regional recovery model.
  repository_evidence:
    - evidence_id: EV-F-019-01
      repository_path: source/inventory-service/src/main/java/com/ecommerce/inventory/service/impl/InventoryServiceImpl.java
      symbol: InventoryServiceImpl.get @Cacheable
      source_language: java
      assessment_snapshot:
        type: workspace_snapshot
        identifier: "inventory-service-workspace-2026-09-18"
        provenance: workspace_generated
        git_commit_sha: not_applicable
        dirty_worktree: not_applicable
        captured_at: "2026-09-18T00:00:00Z"
        limitations:
          - Shares the same assessed excerpt as EV-F-018-01; the two findings cite it for different control violations.
      source_fingerprint:
        algorithm: sha256
        normalization: exact_utf8_excerpt
        fingerprint_scope: exact_excerpt
        value: "af81ef398962c1d6360ab1362e5147578fd509562c148022a7a917a1b3f71ddf"
      original_line_range: {start_line: 30, end_line: 31, status: exact}
      evidence_purpose: primary
      original_source_excerpt: |
            @Override @Cacheable(cacheNames = "inventory", key = "#id")
            public InventoryResponse get(Long id) { return mapper.toResponse(find(id)); }
```

### F-020: Reserve and release mutate inventory without invalidating the cache

```yaml
finding:
  id: F-020
  title: Reserve and release mutate inventory without invalidating the cache
  severity: critical
  finding_status: verified
  primary_control: REDIS-015
  primary_standard: azure-managed-redis
  related_controls: [APP-CACHE-003]
  observed_behavior: >-
    @CacheEvict is declared on update and delete, keyed by the entity id. reserve and release locate the
    item by productId and change availableQuantity and reservedQuantity, but carry no @CacheEvict,
    @CachePut, or explicit eviction. The cached entry keyed by the entity id is therefore left in place
    with the pre-adjustment quantities.
  risk: >-
    Every stock reservation and release, including all reservations driven by order-events consumption,
    leaves a stale quantity in the cache. Because F-017 leaves the entry with no TTL, the stale value is
    served by GET /api/v1/inventory/{id} indefinitely until an unrelated update or delete happens to
    evict it. Callers relying on the read endpoint therefore observe availability that does not exist,
    which can drive over-reservation against the authoritative record.
  implementation_boundary: >-
    Repository-owned: cache invalidation on the reserve and release paths, key alignment between the
    id-keyed cache and the productId-keyed mutation path, and eviction ordering relative to transaction
    commit. Out of boundary: Redis behaviour itself.
  finding_classification:
    type: non_resiliency
    qualification_status: not_qualified
    policy_id: RESILIENCY-FINDING-QUALIFICATION
    policy_version: "1.0.0"
    resiliency_domains: []
    failure_scenario: not_applicable
    target_architecture_element: not_applicable
    causal_mechanism: not_applicable
    material_impact: not_applicable
    non_resiliency_category: correctness
    classification_rationale: >-
      The control violation is evidence-backed and severe, but the impact occurs during entirely normal
      operation with no dependency failure, regional transition, or recovery event involved. It is a data
      correctness defect rather than a resiliency defect and is retained as non_resiliency under the
      qualification policy.
  repository_evidence:
    - evidence_id: EV-F-020-01
      repository_path: source/inventory-service/src/main/java/com/ecommerce/inventory/service/impl/InventoryServiceImpl.java
      symbol: InventoryServiceImpl.update and InventoryServiceImpl.delete @CacheEvict
      source_language: java
      assessment_snapshot:
        type: workspace_snapshot
        identifier: "inventory-service-workspace-2026-09-18"
        provenance: workspace_generated
        git_commit_sha: not_applicable
        dirty_worktree: not_applicable
        captured_at: "2026-09-18T00:00:00Z"
        limitations: []
      source_fingerprint:
        algorithm: sha256
        normalization: exact_utf8_excerpt
        fingerprint_scope: exact_excerpt
        value: "ce19ccf64430ee1002c885469f8e2155bb45455c2e7a9655269964ac1f59ea97"
      original_line_range: {start_line: 33, end_line: 36, status: exact}
      evidence_purpose: primary
      original_source_excerpt: |
            @Override @Transactional @CacheEvict(cacheNames = "inventory", key = "#id")
            public InventoryResponse update(Long id, InventoryRequest request) { InventoryItem item = find(id); mapper.update(request, item); item.setUpdatedAt(Instant.now()); return saveAndPublish(item, "INVENTORY_UPDATED", ""); }
            @Override @Transactional @CacheEvict(cacheNames = "inventory", key = "#id")
            public void delete(Long id) { InventoryItem item = find(id); repository.delete(item); producer.publish("INVENTORY_DELETED", mapper.toResponse(item), ""); }
    - evidence_id: EV-F-020-02
      repository_path: source/inventory-service/src/main/java/com/ecommerce/inventory/service/impl/InventoryServiceImpl.java
      symbol: InventoryServiceImpl.reserve and InventoryServiceImpl.release
      source_language: java
      assessment_snapshot:
        type: workspace_snapshot
        identifier: "inventory-service-workspace-2026-09-18"
        provenance: workspace_generated
        git_commit_sha: not_applicable
        dirty_worktree: not_applicable
        captured_at: "2026-09-18T00:00:00Z"
        limitations:
          - Shares the same assessed excerpt as EV-F-003-02; the two findings cite it for different control violations.
      source_fingerprint:
        algorithm: sha256
        normalization: exact_utf8_excerpt
        fingerprint_scope: exact_excerpt
        value: "0f2357c4e940ae72aaa92d8f2daf7677017121934274498c15ac4e150ebbafe4"
      original_line_range: {start_line: 37, end_line: 50, status: exact}
      evidence_purpose: primary
      original_source_excerpt: |
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
```

### F-021: No graceful shutdown, readiness withdrawal, or work draining

```yaml
finding:
  id: F-021
  title: No graceful shutdown, readiness withdrawal, or work draining
  severity: high
  finding_status: verified
  primary_control: APP-AA-017
  primary_standard: springboot-aks-active-active-master
  related_controls: [GLB-007, JVM-016, JVM-017]
  observed_behavior: >-
    Neither profile configures server.shutdown graceful or spring.lifecycle.timeout-per-shutdown-phase.
    No production class implements SmartLifecycle, DisposableBean, or @PreDestroy, and no code withdraws
    readiness before termination. The Kafka listener container and the servlet container therefore stop
    on the framework default immediate shutdown with no coordinated intake-stop or drain phase.
  risk: >-
    On every rolling deployment, scale-in, node drain, and planned regional transition the pod stops
    accepting nothing and completes nothing. In-flight HTTP writes are cut mid-transaction and in-flight
    Kafka records are interrupted between the database write and the offset commit, which directly
    compounds the duplicate-processing exposure in F-003 and the loss exposure in F-005. Because
    readiness is never withdrawn first, the load balancer continues to send requests to a pod that is
    already terminating.
  implementation_boundary: >-
    Repository-owned: graceful shutdown enablement, per-phase shutdown timeout, readiness withdrawal
    sequencing, and listener container stop ordering. Out of boundary: Kubernetes terminationGracePeriod
    and preStop hooks, which are in the disabled deployment_configuration domain.
  finding_classification:
    type: resiliency
    qualification_status: qualified
    policy_id: RESILIENCY-FINDING-QUALIFICATION
    policy_version: "1.0.0"
    resiliency_domains: [graceful_termination, traffic_eligibility, durability]
    failure_scenario: >-
      A rolling deployment or node drain terminates a pod while it is serving HTTP writes and processing
      order events.
    target_architecture_element: >-
      Pod termination behaviour behind the approved gateway and global load balancer.
    causal_mechanism: >-
      No drain phase and no readiness withdrawal exist, so traffic continues to arrive and in-flight work
      is cut at an arbitrary point.
    material_impact: >-
      Routine deployments produce user-visible request failures and partially applied inventory work.
    non_resiliency_category: not_applicable
    classification_rationale: >-
      Graceful termination and traffic eligibility are approved resiliency domains and the failure occurs
      on every ordinary lifecycle event.
  repository_evidence:
    - evidence_id: EV-F-021-01
      repository_path: source/inventory-service/src/main/resources/application-prod.yml
      symbol: absence of server.shutdown and spring.lifecycle.timeout-per-shutdown-phase
      source_language: yaml
      assessment_snapshot:
        type: workspace_snapshot
        identifier: "inventory-service-workspace-2026-09-18"
        provenance: workspace_generated
        git_commit_sha: not_applicable
        dirty_worktree: not_applicable
        captured_at: "2026-09-18T00:00:00Z"
        limitations:
          - The excerpt is the complete assessed prod profile and demonstrates the absence of any shutdown or lifecycle property.
      source_fingerprint:
        algorithm: sha256
        normalization: exact_utf8_excerpt
        fingerprint_scope: exact_excerpt
        value: "f52a6730d9cb9c1627c17420ab6e361f886ffc4be09fcb5253ead6f9e83034ea"
      original_line_range: {start_line: 1, end_line: 12, status: exact}
      evidence_purpose: primary
      original_source_excerpt: |
        spring:
          config:
            import: azure-keyvault:${AZURE_KEYVAULT_ENDPOINT}
          datasource:
            url: ${SQL_CONNECTION_STRING}
          data:
            redis:
              url: ${REDIS_CONNECTION_STRING}
          kafka:
            bootstrap-servers: ${KAFKA_BOOTSTRAP_SERVERS}
            properties:
              security.protocol: ${KAFKA_SECURITY_PROTOCOL:PLAINTEXT}
```

### F-022: Startup depends on a mandatory Key Vault import with no bounded or optional contract

```yaml
finding:
  id: F-022
  title: Startup depends on a mandatory Key Vault import with no bounded or optional contract
  severity: critical
  finding_status: verified
  primary_control: KV-009
  primary_standard: keyvault
  related_controls: [KV-003, GLB-009]
  observed_behavior: >-
    The prod profile declares spring.config.import as azure-keyvault:${AZURE_KEYVAULT_ENDPOINT} without
    the optional: prefix, which makes the property source mandatory. No ClientOptions, RetryOptions,
    startup timeout, or last-known-good policy is configured for the Key Vault client, and no startup
    failure contract is documented anywhere in the enabled scope.
  risk: >-
    A Key Vault throttle, transient identity failure, private endpoint DNS delay, or access-policy issue
    prevents the application from starting at all, and the wait is governed entirely by implicit SDK
    defaults. During a regional recovery this is exactly when many pods start simultaneously and are
    most likely to be throttled, so the region cannot regain capacity. Because the behaviour is neither
    bounded nor explicit, a startup probe cannot distinguish a progressing startup from a stuck one.
  implementation_boundary: >-
    Repository-owned: the config-import contract, Key Vault client retry and timeout options, and the
    explicit startup policy for unresolved required material. Out of boundary: Key Vault deployment,
    throttling limits, identity assignment, and Kubernetes startup probe configuration.
  finding_classification:
    type: resiliency
    qualification_status: qualified
    policy_id: RESILIENCY-FINDING-QUALIFICATION
    policy_version: "1.0.0"
    resiliency_domains: [availability, recovery, regional_failover]
    failure_scenario: >-
      Many pods start at once during a regional recovery and Key Vault throttles or is briefly
      unreachable.
    target_architecture_element: >-
      Application startup in the recovering region under the approved active-standby target deployment.
    causal_mechanism: >-
      A mandatory property-source import with no bounded retry or timeout makes startup depend
      unconditionally and unboundedly on a remote dependency.
    material_impact: >-
      The recovering region cannot bring capacity online, extending the outage beyond the dependency
      incident itself.
    non_resiliency_category: not_applicable
    classification_rationale: >-
      Startup availability during regional recovery is an approved resiliency domain and the causal
      mechanism is visible in repository-owned configuration.
  repository_evidence:
    - evidence_id: EV-F-022-01
      repository_path: source/inventory-service/src/main/resources/application-prod.yml
      symbol: spring.config.import
      source_language: yaml
      assessment_snapshot:
        type: workspace_snapshot
        identifier: "inventory-service-workspace-2026-09-18"
        provenance: workspace_generated
        git_commit_sha: not_applicable
        dirty_worktree: not_applicable
        captured_at: "2026-09-18T00:00:00Z"
        limitations: []
      source_fingerprint:
        algorithm: sha256
        normalization: exact_utf8_excerpt
        fingerprint_scope: exact_excerpt
        value: "e7c1e56e4046bbfc9fcf5c3a01e365fb206b1f607e3db7809765093a706a1915"
      original_line_range: {start_line: 1, end_line: 3, status: exact}
      evidence_purpose: primary
      original_source_excerpt: |
        spring:
          config:
            import: azure-keyvault:${AZURE_KEYVAULT_ENDPOINT}
```

### F-023: Secrets are bound once at startup with no refresh or rotation handling

```yaml
finding:
  id: F-023
  title: Secrets are bound once at startup with no refresh or rotation handling
  severity: high
  finding_status: verified
  primary_control: KV-005
  primary_standard: keyvault
  related_controls: [KV-007, KV-010, APP-AA-014]
  observed_behavior: >-
    Key Vault material is resolved through a Spring property source at startup. No refresh interval,
    scheduled refresh, @RefreshScope bean, EnvironmentChangeEvent listener, or client-recreation path
    exists. The HikariCP datasource and the Lettuce connection factory are therefore initialized once
    with startup material and retain it for the lifetime of the process.
  risk: >-
    A credential rotation, a regenerated Redis access key, or a restored vault after an incident cannot
    take effect without a full pod restart, and nothing in the application detects that the held
    material has become invalid. Recovery from an identity or credential event therefore requires a
    manual rolling restart rather than automatic convergence, which extends the outage and makes the
    recovery path operator-dependent.
  implementation_boundary: >-
    Repository-owned: refresh strategy, client re-initialization on rotation, and an explicit documented
    restart contract if refresh is intentionally excluded. Out of boundary: Key Vault rotation policy
    and the rotation schedule itself.
  finding_classification:
    type: resiliency
    qualification_status: qualified
    policy_id: RESILIENCY-FINDING-QUALIFICATION
    policy_version: "1.0.0"
    resiliency_domains: [recovery, availability]
    failure_scenario: >-
      A datasource or Redis credential is rotated, or Key Vault access is restored after an outage, while
      pods continue running.
    target_architecture_element: >-
      Credential material held by the initialized Azure SQL and Redis clients.
    causal_mechanism: >-
      Material is bound once at startup and never rebound, so initialized clients continue to present
      stale credentials with no detection or re-initialization path.
    material_impact: >-
      Recovery from a credential or identity event requires a manual restart of every pod in the region.
    non_resiliency_category: not_applicable
    classification_rationale: >-
      Recovery without restart is an explicit approved resiliency requirement, and the absent mechanism
      has a direct causal link to extended recovery time.
  repository_evidence:
    - evidence_id: EV-F-023-01
      repository_path: source/inventory-service/src/main/resources/application-prod.yml
      symbol: spring.config.import
      source_language: yaml
      assessment_snapshot:
        type: workspace_snapshot
        identifier: "inventory-service-workspace-2026-09-18"
        provenance: workspace_generated
        git_commit_sha: not_applicable
        dirty_worktree: not_applicable
        captured_at: "2026-09-18T00:00:00Z"
        limitations:
          - Shares the same assessed excerpt as EV-F-022-01; the two findings cite it for different control violations.
      source_fingerprint:
        algorithm: sha256
        normalization: exact_utf8_excerpt
        fingerprint_scope: exact_excerpt
        value: "e7c1e56e4046bbfc9fcf5c3a01e365fb206b1f607e3db7809765093a706a1915"
      original_line_range: {start_line: 1, end_line: 3, status: exact}
      evidence_purpose: primary
      original_source_excerpt: |
        spring:
          config:
            import: azure-keyvault:${AZURE_KEYVAULT_ENDPOINT}
```

### F-024: Hibernate applies schema changes at startup in every profile

```yaml
finding:
  id: F-024
  title: Hibernate applies schema changes at startup in every profile
  severity: high
  finding_status: verified
  primary_control: APP-AA-013
  primary_standard: springboot-aks-active-active-master
  related_controls: []
  observed_behavior: >-
    spring.jpa.hibernate.ddl-auto is set to update in the default profile and is not overridden in the
    prod profile, so every startup in every region performs schema introspection and applies DDL against
    whichever database the injected connection string resolves to. No Flyway or Liquibase dependency is
    declared, so there is no versioned migration contract and no controlled migration gate.
  risk: >-
    Startup is coupled to a write-capable schema operation on the authoritative database. When a pod
    starts against a read-only geo-secondary, against a database mid-promotion, or while another
    region's pods are performing the same introspection, startup fails or contends in ways the
    application neither bounds nor reports. In an active-standby model the standby region's pods perform
    this DDL attempt on every deployment, so the failure surfaces at exactly the moment the standby is
    needed.
  implementation_boundary: >-
    Repository-owned: ddl-auto setting per profile and adoption of a versioned migration mechanism with
    an explicit startup gate. Out of boundary: failover-group role assignment and database permissions.
  finding_classification:
    type: resiliency
    qualification_status: qualified
    policy_id: RESILIENCY-FINDING-QUALIFICATION
    policy_version: "1.0.0"
    resiliency_domains: [availability, recovery, regional_failover]
    failure_scenario: >-
      A standby-region pod starts while its database endpoint is read-only or mid-promotion, or multiple
      regions start simultaneously during a recovery.
    target_architecture_element: >-
      Application startup against the Azure SQL authoritative state in the approved active-standby target
      deployment.
    causal_mechanism: >-
      Startup unconditionally attempts a write-capable schema operation with no bounded, observable, or
      role-aware gate.
    material_impact: >-
      The standby region can fail to start exactly when it must take over, and schema state can diverge
      without a versioned migration record.
    non_resiliency_category: not_applicable
    classification_rationale: >-
      The impact is regional startup availability and promotion safety, which are approved resiliency
      domains, rather than a general schema-management style preference.
  repository_evidence:
    - evidence_id: EV-F-024-01
      repository_path: source/inventory-service/src/main/resources/application.yml
      symbol: spring.jpa.hibernate.ddl-auto
      source_language: yaml
      assessment_snapshot:
        type: workspace_snapshot
        identifier: "inventory-service-workspace-2026-09-18"
        provenance: workspace_generated
        git_commit_sha: not_applicable
        dirty_worktree: not_applicable
        captured_at: "2026-09-18T00:00:00Z"
        limitations: []
      source_fingerprint:
        algorithm: sha256
        normalization: exact_utf8_excerpt
        fingerprint_scope: exact_excerpt
        value: "26b82c5e056df6c3871feb9337d2e99258ee6736739300bfdc11cb4eb6c5cdb2"
      original_line_range: {start_line: 10, end_line: 12, status: exact}
      evidence_purpose: primary
      original_source_excerpt: |
          jpa:
            hibernate:
              ddl-auto: update
```

### F-025: The list endpoint loads the entire inventory table into memory

```yaml
finding:
  id: F-025
  title: The list endpoint loads the entire inventory table into memory
  severity: high
  finding_status: verified
  primary_control: JVM-004
  primary_standard: jvm-runtime
  related_controls: []
  observed_behavior: >-
    InventoryServiceImpl.list calls repository.findAll, streams every returned entity through the
    mapper, and collects the result into a list. There is no Pageable parameter, no page size, no result
    limit, no streaming, and no maximum on the response. GET /api/v1/inventory exposes this directly and
    without authentication-derived scoping.
  risk: >-
    The peak heap required by a single request grows linearly with the inventory table and is entirely
    outside application control. Concurrent calls multiply the allocation, and because there is no
    bulkhead under F-015 and no timeout under F-009, a handful of concurrent list requests against a
    large table can drive the pod into sustained GC pressure or an OutOfMemoryError. The resulting pod
    loss is indistinguishable from a dependency failure and removes capacity from the region.
  implementation_boundary: >-
    Repository-owned: pagination or streaming on the list path, a maximum result bound, and the
    corresponding API contract change. Out of boundary: container memory limits and JVM heap flags,
    which are in the disabled container_build domain.
  finding_classification:
    type: resiliency
    qualification_status: qualified
    policy_id: RESILIENCY-FINDING-QUALIFICATION
    policy_version: "1.0.0"
    resiliency_domains: [overload_protection, availability]
    failure_scenario: >-
      Concurrent calls to the list endpoint against a production-sized inventory table exhaust the pod
      heap.
    target_architecture_element: >-
      The JVM heap and request capacity of each regional inventory-service pod.
    causal_mechanism: >-
      An unbounded result set is materialized entirely in memory per request with no pagination or
      streaming.
    material_impact: >-
      Pod-level memory exhaustion and loss of regional serving capacity triggered by ordinary API usage.
    non_resiliency_category: not_applicable
    classification_rationale: >-
      Unbounded allocation on a public request path is an overload-protection and availability risk with
      a direct causal path to loss of capacity, not a general performance preference.
  repository_evidence:
    - evidence_id: EV-F-025-01
      repository_path: source/inventory-service/src/main/java/com/ecommerce/inventory/service/impl/InventoryServiceImpl.java
      symbol: InventoryServiceImpl.list
      source_language: java
      assessment_snapshot:
        type: workspace_snapshot
        identifier: "inventory-service-workspace-2026-09-18"
        provenance: workspace_generated
        git_commit_sha: not_applicable
        dirty_worktree: not_applicable
        captured_at: "2026-09-18T00:00:00Z"
        limitations: []
      source_fingerprint:
        algorithm: sha256
        normalization: exact_utf8_excerpt
        fingerprint_scope: exact_excerpt
        value: "fa3fa59291d992c50163fa623bfd1535288aedce4ba7a673588ad42b4a49f031"
      original_line_range: {start_line: 32, end_line: 32, status: exact}
      evidence_purpose: primary
      original_source_excerpt: |
            @Override public List<InventoryResponse> list() { return repository.findAll().stream().map(mapper::toResponse).toList(); }
```

### F-026: Telemetry carries no regional identity

```yaml
finding:
  id: F-026
  title: Telemetry carries no regional identity
  severity: medium
  finding_status: verified
  primary_control: APP-AA-015
  primary_standard: springboot-aks-active-active-master
  related_controls: [GLB-018]
  observed_behavior: >-
    No management.metrics.tags entry, MeterFilter, or common-tag configuration exists, so emitted
    Prometheus metrics carry no region, cluster, or role dimension. The Logback configuration is a
    single console appender using LogstashEncoder with no MDC provider, custom field, or region field,
    and no production code populates MDC.
  risk: >-
    Metrics and logs from both regions are indistinguishable once aggregated. During a regional incident
    an operator cannot determine which region produced an error, which region is serving traffic, or
    whether the intended single-active Kafka role is actually the only one processing. This removes the
    primary evidence needed to confirm or refute a split-brain condition arising from F-004.
  implementation_boundary: >-
    Repository-owned: common metric tags, log MDC or static fields sourced from injected environment
    values, and the region property contract. Out of boundary: the mechanism that supplies the region
    value at deployment time and the aggregation backend.
  finding_classification:
    type: resiliency
    qualification_status: qualified
    policy_id: RESILIENCY-FINDING-QUALIFICATION
    policy_version: "1.0.0"
    resiliency_domains: [failure_observability, regional_failover]
    failure_scenario: >-
      A regional incident or a suspected both-active condition requires operators to attribute telemetry
      to a specific region.
    target_architecture_element: >-
      Operational telemetry for the two-region approved target deployment.
    causal_mechanism: >-
      No region dimension is attached to any metric or log record, so per-region behaviour cannot be
      separated in aggregate views.
    material_impact: >-
      Regional failure attribution and split-brain detection are not possible from emitted telemetry.
    non_resiliency_category: not_applicable
    classification_rationale: >-
      Failure observability is an approved resiliency domain and the missing dimension is specifically
      required by the multi-region target architecture.
  repository_evidence:
    - evidence_id: EV-F-026-01
      repository_path: source/inventory-service/src/main/resources/application.yml
      symbol: absence of management.metrics.tags
      source_language: yaml
      assessment_snapshot:
        type: workspace_snapshot
        identifier: "inventory-service-workspace-2026-09-18"
        provenance: workspace_generated
        git_commit_sha: not_applicable
        dirty_worktree: not_applicable
        captured_at: "2026-09-18T00:00:00Z"
        limitations:
          - The excerpt is the complete assessed management block and demonstrates the absence of any common metric tag.
      source_fingerprint:
        algorithm: sha256
        normalization: exact_utf8_excerpt
        fingerprint_scope: exact_excerpt
        value: "653a483edc8b2f53255c32fb9a607d3d9e8a7e5f543531165e9ff2230b5471f6"
      original_line_range: {start_line: 29, end_line: 37, status: exact}
      evidence_purpose: primary
      original_source_excerpt: |
        management:
          endpoints:
            web:
              exposure:
                include: health,info,prometheus
          endpoint:
            health:
              probes:
                enabled: true
    - evidence_id: EV-F-026-02
      repository_path: source/inventory-service/src/main/resources/logback-spring.xml
      symbol: LogstashEncoder console appender
      source_language: xml
      assessment_snapshot:
        type: workspace_snapshot
        identifier: "inventory-service-workspace-2026-09-18"
        provenance: workspace_generated
        git_commit_sha: not_applicable
        dirty_worktree: not_applicable
        captured_at: "2026-09-18T00:00:00Z"
        limitations: []
      source_fingerprint:
        algorithm: sha256
        normalization: exact_utf8_excerpt
        fingerprint_scope: exact_excerpt
        value: "fa4169b08e5c5d67b946d965d6650ba77a0d20b70ba489846c279543a8c290ae"
      original_line_range: {start_line: 1, end_line: 1, status: exact}
      evidence_purpose: supporting
      original_source_excerpt: |
        <configuration><appender name="CONSOLE" class="ch.qos.logback.core.ConsoleAppender"><encoder class="net.logstash.logback.encoder.LogstashEncoder"/></appender><root level="INFO"><appender-ref ref="CONSOLE"/></root></configuration>
```

### F-027: Critical failures and business throughput produce no actionable signal

```yaml
finding:
  id: F-027
  title: Critical failures and business throughput produce no actionable signal
  severity: critical
  finding_status: verified
  primary_control: APP-AA-016
  primary_standard: springboot-aks-active-active-master
  related_controls: [APP-OBS-002, REDIS-025, REDIS-026, KAFKA-007, GLB-018]
  observed_behavior: >-
    No production class declares a logger, uses @Slf4j, or emits a log statement. Logback is configured
    with a single INFO console appender, so the only records emitted are framework logs. No custom
    metric, counter, timer, or gauge is registered for publication failure, consumption outcome,
    reservation volume, cache failure versus cache miss, last successful processing time, or backlog
    age. The producer discards its send result entirely and logs nothing on failure.
  risk: >-
    Every failure mode identified in this assessment is silent. A dropped Kafka publication under F-001,
    a rolled-back transaction after a published event under F-002, a skipped record under F-005, a
    quarantine-less poison record under F-006, and a Redis outage under F-016 all occur with no
    application-emitted evidence. Operators cannot distinguish a healthy idle service from one whose
    Kafka processing has stopped entirely, because process health remains UP in both cases.
  implementation_boundary: >-
    Repository-owned: structured failure logging, business outcome metrics, last-success and backlog
    signals, and producer failure handling telemetry. Out of boundary: alert rules, dashboards, and the
    log and metric aggregation platform.
  finding_classification:
    type: resiliency
    qualification_status: qualified
    policy_id: RESILIENCY-FINDING-QUALIFICATION
    policy_version: "1.0.0"
    resiliency_domains: [failure_observability, availability, recovery]
    failure_scenario: >-
      Kafka publication or consumption fails or stops entirely while the process continues to report
      healthy.
    target_architecture_element: >-
      Operational detection of failure and recovery for the inventory-events and order-events processing
      paths.
    causal_mechanism: >-
      No application log or business metric is emitted on any failure or success path, so failure is
      indistinguishable from idleness.
    material_impact: >-
      Failures are not detected, so recovery is never initiated and the mean time to detect is unbounded.
    non_resiliency_category: not_applicable
    classification_rationale: >-
      Failure observability is an approved resiliency domain and the absence of any signal directly
      extends outage duration for every other identified failure mode.
  repository_evidence:
    - evidence_id: EV-F-027-01
      repository_path: source/inventory-service/src/main/java/com/ecommerce/inventory/kafka/producer/InventoryEventProducer.java
      symbol: InventoryEventProducer.publish
      source_language: java
      assessment_snapshot:
        type: workspace_snapshot
        identifier: "inventory-service-workspace-2026-09-18"
        provenance: workspace_generated
        git_commit_sha: not_applicable
        dirty_worktree: not_applicable
        captured_at: "2026-09-18T00:00:00Z"
        limitations:
          - Shares the same assessed excerpt as EV-F-001-01; the two findings cite it for different control violations.
      source_fingerprint:
        algorithm: sha256
        normalization: exact_utf8_excerpt
        fingerprint_scope: exact_excerpt
        value: "c77eedf9776fd6bdfbd13ff41642bb1f00ae2767f58bba7c495f40b6dbc8ce8f"
      original_line_range: {start_line: 14, end_line: 16, status: exact}
      evidence_purpose: primary
      original_source_excerpt: |
            public void publish(String type, InventoryResponse inventory, String referenceId) {
                kafkaTemplate.send("inventory-events", inventory.productId(), Map.of("type", type, "occurredAt", Instant.now().toString(), "referenceId", referenceId == null ? "" : referenceId, "inventory", inventory));
            }
    - evidence_id: EV-F-027-02
      repository_path: source/inventory-service/src/main/resources/logback-spring.xml
      symbol: root logger and appender configuration
      source_language: xml
      assessment_snapshot:
        type: workspace_snapshot
        identifier: "inventory-service-workspace-2026-09-18"
        provenance: workspace_generated
        git_commit_sha: not_applicable
        dirty_worktree: not_applicable
        captured_at: "2026-09-18T00:00:00Z"
        limitations:
          - Shares the same assessed excerpt as EV-F-026-02; the two findings cite it for different control violations.
      source_fingerprint:
        algorithm: sha256
        normalization: exact_utf8_excerpt
        fingerprint_scope: exact_excerpt
        value: "fa4169b08e5c5d67b946d965d6650ba77a0d20b70ba489846c279543a8c290ae"
      original_line_range: {start_line: 1, end_line: 1, status: exact}
      evidence_purpose: supporting
      original_source_excerpt: |
        <configuration><appender name="CONSOLE" class="ch.qos.logback.core.ConsoleAppender"><encoder class="net.logstash.logback.encoder.LogstashEncoder"/></appender><root level="INFO"><appender-ref ref="CONSOLE"/></root></configuration>
```

### F-028: Failure and failover behaviour is untested

```yaml
finding:
  id: F-028
  title: Failure and failover behaviour is untested
  severity: critical
  finding_status: verified
  primary_control: APP-AA-018
  primary_standard: springboot-aks-active-active-master
  related_controls: [SQL-008, KAFKA-008, KAFKA-AS-009, REDIS-027, KV-008, GLB-008, APP-SUPPLY-001]
  observed_behavior: >-
    The test suite contains one Mockito unit test covering the happy-path reserve flow and one
    @SpringBootTest with Testcontainers MSSQL and @EmbeddedKafka whose only assertion is that the
    application context loads. No test exercises duplicate delivery, replay from an earlier offset,
    consumer rebalance, broker unavailability, database failover or connection loss, unknown commit
    outcome, optimistic-locking conflict, Redis unavailability, Key Vault denial or throttling, probe
    transitions, or graceful shutdown. create, get, list, update, delete, release, OrderEventConsumer,
    InventoryEventProducer, and GlobalExceptionHandler have no test coverage at all.
  risk: >-
    None of the failure behaviour the approved target deployment depends on is verified, so the
    remediation of the other findings in this assessment cannot be proven and future changes cannot be
    protected from regression. The Spring Boot parent and Spring Cloud Azure BOM also govern resilience-relevant
    transitive versions, and a version bump can silently change timeout, retry, offset, or health
    semantics with only a context-load assertion standing between the change and production.
  implementation_boundary: >-
    Repository-owned: fault-injection and failover tests, Actuator probe-transition tests, duplicate and
    replay tests, and dependency-upgrade regression tests. Out of boundary: live regional failover
    exercises and platform chaos tooling.
  finding_classification:
    type: resiliency
    qualification_status: qualified
    policy_id: RESILIENCY-FINDING-QUALIFICATION
    policy_version: "1.0.0"
    resiliency_domains: [recoverability, fault_tolerance, regional_failover, traffic_eligibility, graceful_termination]
    failure_scenario: >-
      Any of the dependency failure, duplicate delivery, replay, promotion, or shutdown scenarios
      identified in findings F-001 through F-027 occurs in production.
    target_architecture_element: >-
      The verified failure behaviour of inventory-service in the approved active-standby target
      deployment.
    causal_mechanism: >-
      No test exercises any of the specific failure behaviours, so neither the current defects nor their
      remediation can be demonstrated or protected.
    material_impact: >-
      Failure behaviour is unverified and unprotected against regression, so remediation of every other
      finding remains unproven.
    non_resiliency_category: not_applicable
    classification_rationale: >-
      Under the qualification policy a missing-test finding inherits the classification of the failure
      behaviour it leaves unverified; the unverified behaviours here are the identified resiliency
      failure modes rather than generic test absence.
  repository_evidence:
    - evidence_id: EV-F-028-01
      repository_path: source/inventory-service/src/test/java/com/ecommerce/inventory/InventoryIntegrationTest.java
      symbol: InventoryIntegrationTest.contextLoads
      source_language: java
      assessment_snapshot:
        type: workspace_snapshot
        identifier: "inventory-service-workspace-2026-09-18"
        provenance: workspace_generated
        git_commit_sha: not_applicable
        dirty_worktree: not_applicable
        captured_at: "2026-09-18T00:00:00Z"
        limitations: []
      source_fingerprint:
        algorithm: sha256
        normalization: exact_utf8_excerpt
        fingerprint_scope: exact_excerpt
        value: "710fb9f0da4e657a5764247697ea2d33ab01b1d799476bca3207e24a41aa1a67"
      original_line_range: {start_line: 12, end_line: 22, status: exact}
      evidence_purpose: primary
      original_source_excerpt: |
        @SpringBootTest(properties = "spring.kafka.bootstrap-servers=${spring.embedded.kafka.brokers}")
        @EmbeddedKafka(partitions = 1, topics = {"order-events", "inventory-events"})
        @Testcontainers(disabledWithoutDocker = true)
        class InventoryIntegrationTest {
            @Container static final MSSQLServerContainer<?> SQL = new MSSQLServerContainer<>("mcr.microsoft.com/mssql/server:2022-latest").acceptLicense();
            @DynamicPropertySource static void properties(DynamicPropertyRegistry registry) {
                registry.add("spring.datasource.url", SQL::getJdbcUrl); registry.add("spring.datasource.username", SQL::getUsername); registry.add("spring.datasource.password", SQL::getPassword);
            }
            @Test void contextLoads() {
            }
        }
    - evidence_id: EV-F-028-02
      repository_path: source/inventory-service/src/test/java/com/ecommerce/inventory/service/InventoryServiceImplTest.java
      symbol: InventoryServiceImplTest.reservesAvailableStockAndPublishesEvent
      source_language: java
      assessment_snapshot:
        type: workspace_snapshot
        identifier: "inventory-service-workspace-2026-09-18"
        provenance: workspace_generated
        git_commit_sha: not_applicable
        dirty_worktree: not_applicable
        captured_at: "2026-09-18T00:00:00Z"
        limitations: []
      source_fingerprint:
        algorithm: sha256
        normalization: exact_utf8_excerpt
        fingerprint_scope: exact_excerpt
        value: "f445abad3d58be08609ffb76411d3816c9f5ae3e23ce55b4952b19f4b9b605ec"
      original_line_range: {start_line: 21, end_line: 31, status: exact}
      evidence_purpose: supporting
      original_source_excerpt: |
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
```

### F-029: Cached values rely on default JDK serialization but the cached type is not serializable

```yaml
finding:
  id: F-029
  title: Cached values rely on default JDK serialization but the cached type is not serializable
  severity: high
  finding_status: verified
  primary_control: REDIS-012
  primary_standard: azure-managed-redis
  related_controls: []
  observed_behavior: >-
    spring.cache.type is redis and CacheConfig supplies no RedisCacheConfiguration or value
    SerializationPair, so the framework default value serializer applies. The cached type,
    InventoryResponse, is a Java record that does not implement Serializable and declares no explicit
    serializer or type mapping.
  risk: >-
    The value written by @Cacheable on get(Long) is not serializable by the default value serializer, so
    the cache write raises a serialization failure. Combined with the absence of a CacheErrorHandler
    under F-016, that failure propagates to the caller and makes the read endpoint fail on every request
    in any environment where the Redis cache is active. The defect is invisible in the current test
    suite because no test exercises the cached read path against a real cache.
  implementation_boundary: >-
    Repository-owned: explicit cache value serializer selection, serializable cache value model or
    dedicated cache DTO, and a test that exercises the cached read path. Out of boundary: Redis server
    configuration.
  finding_classification:
    type: non_resiliency
    qualification_status: not_qualified
    policy_id: RESILIENCY-FINDING-QUALIFICATION
    policy_version: "1.0.0"
    resiliency_domains: []
    failure_scenario: not_applicable
    target_architecture_element: not_applicable
    causal_mechanism: not_applicable
    material_impact: not_applicable
    non_resiliency_category: compatibility
    classification_rationale: >-
      The control violation is evidence-backed and high impact, but it manifests during entirely normal
      operation with no dependency failure, regional transition, or recovery event involved. It is a
      serialization compatibility defect rather than a resiliency defect and is retained as
      non_resiliency under the qualification policy.
  repository_evidence:
    - evidence_id: EV-F-029-01
      repository_path: source/inventory-service/src/main/java/com/ecommerce/inventory/dto/InventoryResponse.java
      symbol: InventoryResponse
      source_language: java
      assessment_snapshot:
        type: workspace_snapshot
        identifier: "inventory-service-workspace-2026-09-18"
        provenance: workspace_generated
        git_commit_sha: not_applicable
        dirty_worktree: not_applicable
        captured_at: "2026-09-18T00:00:00Z"
        limitations: []
      source_fingerprint:
        algorithm: sha256
        normalization: exact_utf8_excerpt
        fingerprint_scope: exact_excerpt
        value: "cc90710b26c764e0d3e324b86c90d3c7ace4aacef708ccdab72ef318bc7d0a8c"
      original_line_range: {start_line: 5, end_line: 6, status: exact}
      evidence_purpose: primary
      original_source_excerpt: |
        public record InventoryResponse(Long id, String productId, int availableQuantity, int reservedQuantity, Instant updatedAt) {
        }
    - evidence_id: EV-F-029-02
      repository_path: source/inventory-service/src/main/resources/application.yml
      symbol: spring.cache.type
      source_language: yaml
      assessment_snapshot:
        type: workspace_snapshot
        identifier: "inventory-service-workspace-2026-09-18"
        provenance: workspace_generated
        git_commit_sha: not_applicable
        dirty_worktree: not_applicable
        captured_at: "2026-09-18T00:00:00Z"
        limitations:
          - Shares the same assessed excerpt as EV-F-017-01; the two findings cite it for different control violations.
      source_fingerprint:
        algorithm: sha256
        normalization: exact_utf8_excerpt
        fingerprint_scope: exact_excerpt
        value: "5921b25eb1c9acfac5e43cb0c833f6ea37f042b0ee97ebe1c05de562013e3bee"
      original_line_range: {start_line: 16, end_line: 17, status: exact}
      evidence_purpose: supporting
      original_source_excerpt: |
          cache:
            type: redis
```

## Scorecard

```yaml
scorecard:
  assessment_run_id: "inventory-service-2026-09-18-001"
  application_name: inventory-service
  assessment_boundary: single_microservice_repository
  assessment_target_state: approved_target
  operating_scenario: active_standby

  control_totals:
    total_controls_evaluated: 210
    compliant: 36
    non_compliant: 85
    not_assessed: 17
    not_applicable: 72
    accepted_risk: 0

  applicable_control_base:
    note: Applicable controls are compliant plus non_compliant. not_assessed and not_applicable are excluded from the compliance rate.
    applicable_controls: 121
    compliant: 36
    non_compliant: 85
    compliance_rate_percent: 29.8

  finding_totals:
    total_findings: 29
    verified_findings: 29
    conditional_findings: 0
    by_severity:
      critical: 14
      high: 14
      medium: 1
      low: 0
    by_classification:
      resiliency: 26
      non_resiliency: 3

  findings_by_primary_standard:
    springboot-aks-active-active-master: 15
    azure-sql: 3
    confluent-kafka: 1
    azure-managed-redis: 7
    keyvault: 2
    jvm-runtime: 1
    appgateway-glb: 0

  non_compliant_controls_by_standard:
    springboot-aks-active-active-master: 27
    azure-sql: 8
    confluent-kafka: 18
    azure-managed-redis: 12
    keyvault: 7
    jvm-runtime: 6
    appgateway-glb: 7

  not_assessed_by_reason:
    assessment_domain_disabled: 12
    deployed_topology_or_external_value_required: 5
    total: 17

  resiliency_domain_exposure:
    note: Count of resiliency-classified findings touching each approved domain. A finding may touch several domains.
    availability: 17
    fault_tolerance: 10
    recovery: 8
    recoverability: 7
    failure_observability: 7
    regional_failover: 7
    overload_protection: 6
    state_recovery: 5
    durability: 4
    dependency_isolation: 3
    traffic_eligibility: 3
    graceful_termination: 2
    workload_ownership: 1
    retry_management: 1

  non_resiliency_category_exposure:
    correctness: 1
    compatibility: 1
    contract: 1

  severity_note: >-
    Severity is inherited from the primary control in its governing standard. Remediation priority is
    not assigned in this phase; priority is governed exclusively by Step 3A through
    grounding/governance/remediation-prioritization.md.
```

## Assessment Summary

### Finding index

```yaml
finding_index:
  - {id: F-001, severity: critical, class: resiliency, primary_control: APP-KAFKA-005, title: Kafka publication is fire-and-forget with no durability configuration}
  - {id: F-002, severity: critical, class: resiliency, primary_control: APP-DB-003, title: Event publication occurs inside the database transaction with no outbox or commit coordination}
  - {id: F-003, severity: critical, class: resiliency, primary_control: APP-AA-011, title: Order-event consumption and stock adjustment are not idempotent}
  - {id: F-004, severity: critical, class: resiliency, primary_control: APP-KAFKA-001, title: Kafka listener has no region-role activation control}
  - {id: F-005, severity: critical, class: resiliency, primary_control: APP-KAFKA-002, title: Consumer offsets advance past records that fail permanently}
  - {id: F-006, severity: high, class: resiliency, primary_control: APP-KAFKA-003, title: Poison records have no dead-letter routing and payload extraction is unguarded}
  - {id: F-007, severity: high, class: resiliency, primary_control: APP-KAFKA-006, title: Published events carry no stable identity or correlation context}
  - {id: F-008, severity: critical, class: resiliency, primary_control: APP-AA-007, title: Readiness and health configuration relies entirely on framework defaults}
  - {id: F-009, severity: critical, class: resiliency, primary_control: SQL-002, title: Azure SQL access has no bounded timeouts}
  - {id: F-010, severity: critical, class: resiliency, primary_control: REDIS-005, title: Redis access has no bounded connect or command timeouts}
  - {id: F-011, severity: high, class: resiliency, primary_control: KAFKA-005, title: Kafka client timeouts, reconnect, and backoff are unbounded by repository configuration}
  - {id: F-012, severity: critical, class: resiliency, primary_control: SQL-003, title: No bounded retry exists for transient Azure SQL failures}
  - {id: F-013, severity: high, class: resiliency, primary_control: SQL-007, title: Optimistic-locking conflicts are neither detected, retried, nor mapped}
  - {id: F-014, severity: high, class: resiliency, primary_control: APP-WEB-002, title: Dependency failures have no stable caller-visible semantics}
  - {id: F-015, severity: high, class: resiliency, primary_control: APP-AA-006, title: No isolation exists between request threads and blocking dependencies}
  - {id: F-016, severity: critical, class: resiliency, primary_control: REDIS-020, title: Redis cache failures propagate into the request path with no error handler}
  - {id: F-017, severity: high, class: resiliency, primary_control: REDIS-011, title: Cached entries have no TTL or expiration policy}
  - {id: F-018, severity: high, class: non_resiliency, primary_control: REDIS-022, title: Cache keys have no namespace, environment scope, or schema version}
  - {id: F-019, severity: high, class: resiliency, primary_control: REDIS-009, title: Concurrent cache misses are not coalesced}
  - {id: F-020, severity: critical, class: non_resiliency, primary_control: REDIS-015, title: Reserve and release mutate inventory without invalidating the cache}
  - {id: F-021, severity: high, class: resiliency, primary_control: APP-AA-017, title: No graceful shutdown, readiness withdrawal, or work draining}
  - {id: F-022, severity: critical, class: resiliency, primary_control: KV-009, title: Startup depends on a mandatory Key Vault import with no bounded or optional contract}
  - {id: F-023, severity: high, class: resiliency, primary_control: KV-005, title: Secrets are bound once at startup with no refresh or rotation handling}
  - {id: F-024, severity: high, class: resiliency, primary_control: APP-AA-013, title: Hibernate applies schema changes at startup in every profile}
  - {id: F-025, severity: high, class: resiliency, primary_control: JVM-004, title: The list endpoint loads the entire inventory table into memory}
  - {id: F-026, severity: medium, class: resiliency, primary_control: APP-AA-015, title: Telemetry carries no regional identity}
  - {id: F-027, severity: critical, class: resiliency, primary_control: APP-AA-016, title: Critical failures and business throughput produce no actionable signal}
  - {id: F-028, severity: critical, class: resiliency, primary_control: APP-AA-018, title: Failure and failover behaviour is untested}
  - {id: F-029, severity: high, class: non_resiliency, primary_control: REDIS-012, title: Cached values rely on default JDK serialization but the cached type is not serializable}
```

### Evidence summary

```yaml
evidence_summary:
  applicable_findings: 29
  findings_with_exact_excerpts: 29
  findings_with_evidence_not_available: 0
  findings_with_not_applicable_excerpts: 0
  invented_excerpts: 0
  total_evidence_items: 40
  evidence_items_with_exact_excerpt_and_fingerprint: 39
  evidence_items_marked_not_available: 1
  evidence_items_with_redacted_fingerprint_scope: 0
  evidence_snapshot_classification: workspace_snapshot
  evidence_line_range_status:
    exact: 39
    advisory: 0
    not_available: 1
  shared_excerpt_pairs:
    note: Distinct evidence identifiers that intentionally cite the same assessed excerpt for different control violations.
    - [EV-F-012-01, EV-F-015-01]
    - [EV-F-013-02, EV-F-014-01]
    - [EV-F-018-01, EV-F-019-01]
    - [EV-F-003-02, EV-F-020-02]
    - [EV-F-017-01, EV-F-029-02]
    - [EV-F-022-01, EV-F-023-01]
    - [EV-F-001-01, EV-F-027-01]
    - [EV-F-026-01, EV-F-008-01]
    - [EV-F-026-02, EV-F-027-02]
```

### Evidence gaps requiring external input

```yaml
evidence_gaps:
  note: >-
    These are unresolved facts outside the enabled assessment domains or outside repository evidence.
    They are not findings and must not be converted into code findings.

  - id: EG-001
    area: azure_sql_connectivity
    carried_from: UNC-001
    summary: The production datasource URL is supplied entirely through SQL_CONNECTION_STRING, so failover-group read-write listener usage cannot be validated from the repository.
    affected_controls: [SQL-001]
    required_input:
      - Approved failover-group listener DNS name
      - Resolved value of SQL_CONNECTION_STRING in each target region
      - Database membership in the failover group
    route_to: platform_evidence_request

  - id: EG-002
    area: kafka_deployed_topology
    carried_from: UNC-002
    summary: Deployed cluster topology, Cluster Linking, mirror-topic promotion state, and consumer-offset replication are not determinable from the repository.
    affected_controls: [KAFKA-AS-005]
    required_input:
      - Per-region cluster inventory and role assignment
      - Cluster Linking and Schema Linking configuration
      - Topic, schema, ACL, and consumer-offset replication configuration
    route_to: platform_evidence_request

  - id: EG-003
    area: redis_credentials_and_tls
    summary: Production Redis credentials and TLS scheme are contained inside the externally supplied REDIS_CONNECTION_STRING value.
    affected_controls: [REDIS-004]
    required_input:
      - Resolved REDIS_CONNECTION_STRING scheme and authentication mode per region
    route_to: platform_evidence_request

  - id: EG-004
    area: redis_operating_model
    carried_from: UNC-009
    summary: Approved context sets the Redis target operating model to active_active, but deployed geo-replication topology and conflict behaviour are not determinable from the repository.
    affected_controls: [REDIS-018]
    required_input:
      - Deployed Azure Managed Redis regional topology and geo-replication configuration
    route_to: platform_evidence_request

  - id: EG-005
    area: runtime_and_container_configuration
    carried_from: UNC-006
    summary: JVM options, container entrypoint and signal forwarding, resource limits, probes, and termination grace live in the disabled container_build and deployment_configuration domains.
    affected_controls: [JVM-002, JVM-003, JVM-005, JVM-006, JVM-007, JVM-008, JVM-009, JVM-014, JVM-015, APP-SUPPLY-002, APP-CACHE-002]
    required_input:
      - Enable the container_build and deployment_configuration assessment domains, or supply the approved runtime and deployment configuration as evidence
    route_to: assessment_scope_decision

  - id: EG-006
    area: gateway_and_load_balancer_budgets
    summary: Gateway, mesh, and load-balancer idle, request, and keep-alive timeouts are outside the enabled assessment domains, so end-to-end budget ordering cannot be evaluated.
    affected_controls: [GLB-010, GLB-016]
    required_input:
      - Approved gateway and global load balancer timeout and keep-alive configuration
    route_to: platform_evidence_request

  - id: EG-007
    area: management_endpoint_reachability
    summary: Actuator exposure is limited to health, info, and prometheus with default show-details never, and springdoc exposes /swagger-ui.html on the application port. External reachability depends on ingress and management-port routing in the disabled deployment_configuration domain.
    affected_controls: [GLB-012]
    required_input:
      - Ingress routing rules and management-port separation for the application port 8082
    route_to: platform_evidence_request

  - id: EG-008
    area: apim_capability_expectation
    carried_from: UNC-005
    summary: Approved context declares apim as a required platform capability, but the service performs no outbound HTTP call, so no APIM client behaviour exists to validate.
    affected_controls: []
    required_input:
      - Architecture confirmation of whether apim applies to this repository as an inbound capability only
    route_to: architecture_governance_review

  - id: EG-009
    area: aks_istio_capability_expectation
    carried_from: UNC-007
    summary: Approved context marks aks-istio optional and repository-owned Kubernetes manifests exist, but the deployment_configuration domain is disabled.
    affected_controls: []
    required_input:
      - Enable the deployment_configuration domain or confirm mesh behaviour is externally governed
    route_to: assessment_scope_decision

  - id: EG-010
    area: regional_processing_ownership_confirmation
    carried_from: UNC-004
    summary: >-
      The repository-side absence of any listener activation control is a verified finding (F-004). Whether
      a deployment-level mechanism currently prevents standby-region consumption remains unconfirmed and
      determines the operational urgency of F-004, not its validity.
    affected_controls: [KAFKA-AS-001, KAFKA-AS-003]
    required_input:
      - Confirmation of how standby-region consumption is currently prevented, if at all
    route_to: architecture_governance_review

  - id: EG-011
    area: event_schema_governance
    carried_from: UNC-008
    summary: Events are published as untyped Map payloads with no schema registry configuration and no versioned contract, and whether a governed schema contract applies to inventory-events and order-events is not determinable from the repository.
    affected_controls: []
    required_input:
      - Approved schema contract and registry expectation for inventory-events and order-events
    route_to: architecture_governance_review
```

### Control coverage gaps

```yaml
control_coverage_gaps:
  note: >-
    Repository-evidenced risks observed during evaluation for which no loaded standard contains an
    applicable control. No finding is created, because a finding requires an applicable control. These
    are routed to governance for control-catalog coverage review.

  - id: CCG-001
    observation: spring.kafka.properties.security.protocol falls back to PLAINTEXT when KAFKA_SECURITY_PROTOCOL is unset, and no SASL or SSL configuration exists in the repository.
    repository_path: source/inventory-service/src/main/resources/application-prod.yml
    symbol: spring.kafka.properties.security.protocol
    original_line_range: {start_line: 11, end_line: 12, status: exact}
    carried_from: UNC-003
    missing_control_coverage: Kafka client transport-security and credential-delivery control in the confluent-kafka standard.
    route_to: grounding_standard_governance

  - id: CCG-002
    observation: spring.json.trusted.packages is set to "*" for the Kafka JsonDeserializer, which removes package-level type restriction on inbound event deserialization.
    repository_path: source/inventory-service/src/main/resources/application.yml
    symbol: spring.kafka.consumer.properties.spring.json.trusted.packages
    original_line_range: {start_line: 24, end_line: 25, status: exact}
    missing_control_coverage: Inbound message deserialization trust control in the confluent-kafka or master standard.
    route_to: grounding_standard_governance

  - id: CCG-003
    observation: No authentication or authorization is applied to any /api/v1/inventory endpoint, including the state-changing reserve, release, update, and delete operations.
    repository_path: source/inventory-service/src/main/java/com/ecommerce/inventory/controller/InventoryController.java
    symbol: InventoryController
    original_line_range: {start_line: 14, end_line: 24, status: exact}
    missing_control_coverage: APP-API-001 applies only when administrative endpoints exist; no loaded standard contains a general business-API authentication or authorization control.
    route_to: grounding_standard_governance

  - id: CCG-004
    observation: springdoc-openapi-starter-webmvc-ui is a compile-scope dependency and springdoc.swagger-ui.path is configured on the application port in all profiles.
    repository_path: source/inventory-service/src/main/resources/application.yml
    symbol: springdoc.swagger-ui.path
    original_line_range: {start_line: 38, end_line: 40, status: exact}
    missing_control_coverage: API documentation exposure control; GLB-012 addresses management endpoints only and its reachability precondition is unresolved under EG-007.
    route_to: grounding_standard_governance
```

### Inventory exceptions

```yaml
inventory_exceptions:
  discovered_in_step_2:
    - id: EXC-A-001
      type: citation_line_range_overshoot
      description: >-
        The Step 1 inventory cited GlobalExceptionHandler at lines 12-22 with status exact. The assessed
        file contains 21 lines. The cited symbol, observation, and content are otherwise correct.
      affected_path: source/inventory-service/src/main/java/com/ecommerce/inventory/exception/GlobalExceptionHandler.java
      resolution: Evidence EV-F-013-02 and EV-F-014-01 use the corrected exact range 12-21 with a verified excerpt fingerprint.
      controls_affected: none
      downstream_action: informational_only

  carried_from_step_1:
    - id: EXC-001
      type: scope_limitation
      description: Repository-owned Dockerfile, GitHub Actions workflow, and Kubernetes manifests exist but were not inventoried because their domains are disabled.
      downstream_action: preserved_as_evidence_gap_EG-005_and_EG-009
    - id: EXC-002
      type: expectation_without_evidence
      description: Approved context declares apim as a required platform capability, but no outbound HTTP client exists in production source.
      downstream_action: preserved_as_evidence_gap_EG-008
    - id: EXC-003
      type: expectation_out_of_scope
      description: Approved context marks aks-istio optional with execution_platform aks, but mesh evidence lives in the disabled deployment_configuration domain.
      downstream_action: preserved_as_evidence_gap_EG-009
    - id: EXC-004
      type: registry_activation_note
      description: The registry activates http-client on the spring-web dependency, but no outbound HTTP client construction exists, so http-client is recorded declared_only and was not loaded as a standard.
      downstream_action: preserved_no_standard_loaded
```

### Notable compliant behaviour

```yaml
notable_compliant_behaviour:
  note: Recorded for Step 3A context only. These are not findings and carry no remediation obligation.
  - Every remote endpoint is deployment-injected; no regional hostname, port, or cluster is hardcoded in any profile (APP-AA-002, SQL-001, REDIS-003, KAFKA-001, KV-001).
  - A single immutable Maven artifact with default and prod profiles supports both regions (APP-AA-001).
  - Liveness excludes external dependencies by relying on the default liveness group, so a dependency outage cannot cause restart loops (APP-AA-008, GLB-003).
  - HTTP handling is fully stateless with no session or region-sticky state (APP-AA-010, GLB-006).
  - Actuator exposure is minimized to health, info, and prometheus, with health details defaulting to never (APP-ACT-001, APP-ACT-003).
  - Azure SQL is the unambiguous authoritative business state and Redis is used only as a non-authoritative cache with a repository fallback on miss (REDIS-001, REDIS-002).
  - The Kafka operating scenario is supplied by approved application architecture context and validated consistent under KAFKA-SCENARIO-001 (KAFKA-009).
  - No production class can log a secret, credential, or payment value, and no generated string representation exposes sensitive fields (APP-LOG-001, APP-LOG-002, KV-013).
```

### PCF exclusion

```yaml
pcf_exclusion:
  standard: grounding/exclusions/pcf-code-assessment-exclusion.md
  status_applied: suppress_all
  pcf_references_found: 0
  pcf_findings_created: 0
  note: The Step 1 inventory recorded no Cloud Foundry manifest, buildpack reference, VCAP binding, or documentation reference. No PCF finding, recommendation, or score impact was produced.
```

### Completion validation

```yaml
completion_validation:
  inventory_run_id_carried_into_outputs: true
  inventory_run_id: "inventory-service-2026-09-18-001"
  re_inventory_performed: false
  researcher_invoked_during_evaluation: false
  source_code_modified: false
  new_dependencies_added: 0
  only_inventory_listed_standards_loaded: true
  standards_loaded_count: 8
  dependency_standards_loaded_count: 6
  assessment_domain_standards_loaded_count: 0
  substitute_standards_loaded_for_gaps: 0
  every_finding_maps_to_noncompliant_control: true
  findings_without_primary_control: 0
  noncompliant_controls_without_finding: 0
  missing_evidence_recorded_as_not_assessed: true
  not_assessed_count: 17
  infrastructure_findings_created: 0
  deployed_infrastructure_findings_created: 0
  pcf_findings_created: 0
  disabled_domain_findings_created: 0
  remediation_priority_assigned: false
  priority_governance_note: Priority is assigned exclusively by Step 3A through grounding/governance/remediation-prioritization.md.
  scenario_recalculated: false
  architecture_context_copied_into_repository_evidence: false
  source_evidence_contract:
    every_applicable_finding_has_repository_path: true
    every_applicable_finding_has_symbol_or_element: true
    every_applicable_finding_has_exact_excerpt_or_explicit_unavailability: true
    every_evidence_item_has_snapshot_classification: true
    every_computable_evidence_item_has_fingerprint: true
    every_evidence_item_has_line_range_status: true
    excerpts_rewritten_or_normalized: 0
  targeted_evidence_validation:
    performed: true
    scope: Only files and line ranges already cited by the Step 1 inventory were opened, with a small surrounding context window, to confirm exact excerpts and line ranges.
    files_opened: 15
    new_files_discovered: 0
    inventory_exceptions_raised: 1
  required_sections_present:
    control_results: true
    findings: true
    scorecard: true
    assessment_summary: true
```

### Next phase

```yaml
next_phase:
  phase: remediation_planning
  phase_order: "03A"
  next_agent: task-planner
  authoritative_prompt: prompts/03A-create-authoritative-remediation-plan.prompt.md
  required_authoritative_inputs:
    - .copilot-tracking/reviews/2026-09-18/inventory-service-inventory-research-review.md
    - .copilot-tracking/research/2026-09-18/inventory-service-inventory-research.md
    - application-context/application-architecture-context.yml
    - application-context/assessment-scope-context.yml
    - grounding/governance/remediation-prioritization.md
    - grounding/governance/resiliency-finding-qualification-policy.yml
  inputs_frozen_by_this_phase:
    - finding identifiers F-001 through F-029
    - finding severity
    - finding classification and qualification rationale
    - control mapping
    - repository evidence and fingerprints
    - Kafka operating scenario provenance
    - assessment scope resolution
  step_3a_obligations:
    - Assign remediation priority to every finding through the approved priority policy, recording policy ID, policy version, and rule ID.
    - Preserve both finding classes and render resiliency recommendations before non-resiliency recommendations.
    - Treat evidence gaps EG-001 through EG-011 and coverage gaps CCG-001 through CCG-004 as non-implementation items routed to the recorded owners.
    - Carry JVM-022 validation obligations into the validation strategy for any JVM or lifecycle change.
  re_inventory_allowed: false
  reassessment_allowed: false
  handoff_summary_path: .copilot-tracking/reviews/handoffs/02-assessment-summary.yml
```
