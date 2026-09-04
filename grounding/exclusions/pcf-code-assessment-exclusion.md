---
schema_version: 1.0.0
document_type: exclusion
service: pcf
aliases: [PCF, Pivotal Cloud Foundry, PAS, Pivotal Application Service, TAS, Tanzu Application Service, Tanzu Platform for Cloud Foundry]
lifecycle_status: retired
assessment:
  enabled: false
  emit_findings: false
  include_in_score: false
  finding_behavior: suppress_all
  repository_reference_behavior: historical_information_only
---

# PCF Code-Assessment Exclusion

PCF is retired and no longer used by the assessed application estate. Do not emit findings, recommendations, modernization actions, migration actions, or score impacts for PCF or its aliases. Historical manifests, pipeline fragments, documentation, comments, and dependencies should be recorded only as neutral inventory evidence if needed. Unexpected executable PCF deployment behavior should be routed for human review without automatically creating a resiliency finding.
