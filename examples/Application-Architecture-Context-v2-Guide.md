# Application Architecture Context v2 Guide

## Purpose

The `application-architecture-context.yml` file is the primary architecture authority for a repository assessment.

This version is optimized for the common model:

```text
1 Repository
    ↓
1 Microservice
```

The goal is to provide architecture intent that cannot always be reliably inferred from source code.

Examples:

- Approved Kafka operating scenario
- Authoritative state ownership
- Service business role
- Upstream service relationships
- Downstream service relationships
- External side effects
- Regional processing expectations

The context file supplements repository evidence.

Repository evidence remains authoritative for:

- Actual implementation
- Dependencies in use
- Runtime behavior implemented in code
- Findings
- Source evidence

---

# Location

Store the file at:

```text
application-context/application-architecture-context.yml
```

Only one active application context should exist per repository assessment.

---

# Assessment Processing Order

The recommended precedence is:

```text
1. application-architecture-context.yml

2. repository evidence

3. solution-architecture-context.yml (optional)

4. policy inference

5. unresolved
```

If repository evidence conflicts with the approved architecture context:

```text
Route to architecture review
```

Do not automatically override either source.

---

# Metadata Section

```yaml
metadata:
  application_name:
  repository_name:
  business_role:
```

## application_name

Human-friendly application identifier.

Example:

```yaml
application_name: notification-service
```

## repository_name

Repository containing the service.

Example:

```yaml
repository_name: ecommerce-notification-service
```

## business_role

Describes the function of the service.

Examples:

```yaml
business_role: customer_notification
```

```yaml
business_role: order_processing
```

```yaml
business_role: payment_processing
```

This field helps assessment reviewers understand business impact.

---

# Deployment Model

```yaml
deployment_model:
  operating_model:
  regions:
  same_application_artifact_across_regions:
```

## operating_model

Allowed values:

```yaml
active_active
```

or

```yaml
active_standby
```

Example:

```yaml
operating_model: active_active
```

## regions

Regions where the application is deployed.

Example:

```yaml
regions:
  - westus3
  - eastus2
```

## same_application_artifact_across_regions

Should normally be:

```yaml
true
```

The same application artifact should be deployed to every region.

---

# Authoritative State

```yaml
authoritative_state:
  dependency:
  role:
  operating_model:
```

## dependency

Primary system of record.

Examples:

```yaml
dependency: azure_sql
```

```yaml
dependency: cosmos_db
```

```yaml
dependency: cassandra
```

```yaml
dependency: none
```

## role

Allowed values:

```yaml
authoritative_business_state
```

```yaml
supporting_state
```

```yaml
none
```

## operating_model

Examples:

```yaml
active_standby
```

```yaml
multi_region_write
```

```yaml
regional_independent
```

```yaml
none
```

---

# Kafka Operating Model

```yaml
kafka_operating_model:
  scenario:
  scenario_policy_id:
  expected_scenario_rule_id:
```

## scenario

Allowed values:

```yaml
active_standby
```

```yaml
independent_regional_active_active
```

```yaml
database_independent_kafka
```

Example:

```yaml
scenario: active_standby
```

## expected_scenario_rule_id

Examples:

```yaml
KAFKA-SCENARIO-001
```

```yaml
KAFKA-SCENARIO-002
```

```yaml
KAFKA-SCENARIO-003
```

---

# New Feature: Upstream Dependencies

```yaml
upstream_dependencies:
```

This identifies who provides work to the service.

Example:

```yaml
upstream_dependencies:

  - service: order-service
    interaction: kafka
    role: business_event_source
```

## Why this is useful

The repository may only show:

```text
Kafka Consumer
```

but not reveal:

```text
Who created the event.
```

This helps:

- Scenario selection
- Workflow understanding
- Business impact analysis
- Ownership reasoning

### interaction values

Examples:

```yaml
kafka
rest
grpc
event_grid
event_hub
other
```

### role values

Examples:

```yaml
business_event_source
request_source
data_source
other
```

---

# New Feature: Downstream Dependencies

```yaml
downstream_dependencies:
```

This identifies systems that depend on this service.

Example:

```yaml
downstream_dependencies:

  - service: sendgrid
    interaction: api
    role: external_side_effect
```

## Why this is useful

Repository code may not clearly communicate:

```text
Business side effects
```

or

```text
Dependent systems.
```

Declaring them improves assessment accuracy.

### Common roles

```yaml
external_side_effect
```

```yaml
event_consumer
```

```yaml
dependent_service
```

---

# New Feature: External Side Effects

```yaml
external_side_effects:
```

Example:

```yaml
external_side_effects:

  present: true

  types:
    - email_delivery
```

Common values:

```yaml
email_delivery
sms_delivery
payment_processing
partner_api_call
inventory_update
```

This helps identify:

- Idempotency requirements
- Replay requirements
- Recovery requirements
- Duplicate-processing risk

---

# Direct Dependency Expectations

```yaml
direct_dependency_expectations:
```

Example:

```yaml
direct_dependency_expectations:

  kafka: true

  azure_sql: false

  cosmos_db: false
```

This documents approved architecture expectations.

It is not used as proof that the dependency exists.

Repository evidence must still confirm actual implementation.

---

# Architecture Decisions

```yaml
architecture_decisions:
```

Example:

```yaml
architecture_decisions:

  - decision_id: ADR-001
    title: Kafka follows SQL ownership
    status: approved
```

Use this section for important architecture approvals.

---

# Architecture Evidence

```yaml
architecture_evidence:
```

Example:

```yaml
architecture_evidence:
  - reference_id: ARCH-001
    description: Approved active-active architecture
    source: Architecture Review Board
```

Provides traceability for context declarations.

---

# Typical Notification Service Example

```yaml
metadata:
  application_name: notification-service
  repository_name: notification-service
  business_role: customer_notification

authoritative_state:
  dependency: none
  role: none
  operating_model: none

kafka_operating_model:
  scenario: active_standby

upstream_dependencies:
  - service: order-service
    interaction: kafka
    role: business_event_source

downstream_dependencies:
  - service: sendgrid
    interaction: rest
    role: external_side_effect

external_side_effects:
  present: true
  types:
    - email_delivery
```

This gives the assessment framework enough architectural context without requiring a separate solution-architecture-context file.
