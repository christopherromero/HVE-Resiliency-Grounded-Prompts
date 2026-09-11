README - 09/09/2026

# Here is the process for setting up your workstation

There is a ZIP that has the folder structure and the required files

/Assessment
 - .copilot
 - .copilot.tracking
    - research
        - handoffs
        - subagents
    - reviews
        - handoffs
    - plans
        - handoffs
        - logs
        - reports
    - details
    - changes
      - handoffs
 - .github
    - instructions
    - modernize
    - prompts
 - .vscode
 - application-context
    - templates
 - examples
 - grounding
    - dependencies
    - exclusions
    - governance
    - master
    - registry
    - standards
 - prompts
 - source/customer-app (repo source goes here)
readme.md


1) Create a directory called assessment
2) Right click the Zip, select properties, check unblock, apply, ok
3) Open the ZIP and copy the contents into C:\assessment
4) From VSCode, open the C:\assessment folder so it is the workspace root

---
#### We do not want the prompts and output to be stored in the customer repo, that should be external to the repo, that is why the repo is in a child folder source/customer-app and not at the root.
---

## Prep for the repo assessment

1) Copy, clone, the repository code into the customer-app folder
2) Open assessment-context/assessment-context.md and change the application name at the top to the name of the repo you are assessing.
3) Prepare the application-architecture-context files, See the guide in the examples folder 

### Setting the scope

refer to examples/assessment-scope-context-options-explanation.yml

You need to configure what options you want in the inventory (assessment scope) and in the assessment report (report preferences)

The assessment details will always include P0-P3 priority findings even if you specify in the report to only output P0-P1 findings.

assessment-context/assessment-scope-context.yml

This file is where you enable or disable the different options for the report

There are the type of content in the assessment report under assessment_scope
There are the scope_rules
There are the report preferences like what priority findings need to be included
There are the testing output 

note look in /examples for some example scope configurations

The following example has app code/configuration and CICD included in the inventory, blocks deployed infrastructure and PCF findings, only includes P0-P1 findings, and hides all test and validation infomation.

For details on allowed options for each setting look at examples/assessment-scope-context-options-explanation.yml 

```
schema_version: "1.0.0"
document_type: assessment_scope_context
lifecycle_status: active
context_id: default-assessment-scope
context_version: "1.0.0"
owner: Cloud Architecture Team

assessment_scope:
  application_code: {status: enabled}
  application_configuration: {status: enabled}
  container_build: {status: enabled}
  cicd_pipeline: {status: enabled}
  deployment_configuration: {status: disabled}
  infrastructure_as_code: {status: disabled}
  deployed_infrastructure: {status: disabled}
scope_rules:
  repository_owned_only: true
  externally_owned_assets: evidence_gap_only
  missing_context_behavior: use_governed_defaults
  unknown_ownership_behavior: not_assessed
  deployed_infrastructure_findings_allowed: false
  pcf_findings_allowed: false
report_preferences:
  finding_selection:
    mode: priority_filter
    include_priorities:
      - P0
      - P1
    include_conditional_findings: true
    include_verified_controls: false
    include_evidence_gaps: true
    excluded_priority_behavior: omit_from_filtered_report
  testing_output:
    mode: hidden
    show_test_findings: false
    show_test_code: false
    show_validation_commands: false
    show_acceptance_criteria: false
    show_validation_evidence: false
    include_consolidated_validation_strategy: false
```

## Optional - recommend to not the solution context unless the application is provided with all microservices in a single repository

### Setting the Solution Architecture Context

solution-architecture-context.md - this allows you to specify the overall application architecture context across all of the microservices

There is only one template for the solution architecture, so just copy it tot he application-context folder and rename it to solution-application-context.md and edit it.

### Setting the repo architecture context

refer to examples/application-architecture-context-v2-guide.yml for details

application-architecture-context.md - this allows you to specify the context of the repo you are assessing.

Under the \application-context\templates folder are sample templates for DB/Kafka scenarios

For the application-architecture-context, You take the sample template that would apply (Active-Active with Cosmos, Active-Standby with SQL, No DB but still Kafka) copy it to the \application-context folder and then rename it to application-architecture-context.md and the edit it

NOTE: There are simple form templates and then detailed form templates, use the simple for now.

## Approved Libraies for use in the refactoring

There is a new file grounding\governance\approved-libraries.yml

This defines the libraries that should be used in the refactoring as the standard for different purposes 

New templates that describe the options

examples\approved-libraries-template-simplified.yml
examples\approved-libraries-template-complex.yml

## Instructions to run the assessment for a prepared repo

Note that each Step uses a HVE Agent that is different

1) To execute step one prompt
2) Set your agent to Task Reasearcher
3) Set the model to Claude Opus 5.0
4) If you are using MS EMU license, Enable Allow All so you do not have to approve anything (status bar under the agent selection)
5) Paste the following prompt into the chat window and modify it to todays date

/01-inventory runDate=2026-09-09 sourceroot=source/customer-app taskSlug=springboot-active-active-inventory

6) The output files have the todays date in the name, you must ensure the instructions are updated with todays date in the paths. For example Step 1 produces the inventory file INVENTORY_ARTIFACT=.copilot-tracking/research/2026-09-02/springboot-active-active-inventory-research.md
7) When Step 1 Prompt is done, Click the KEEP button, run /clear, reenable opus 5 as the model, reenable Allow ALL, Change agent to Task Reviewer , run the step 2 prompt

/02-findings  runDate=2026-09-09  taskSlug=springboot-active-active-inventory

8) When Step 2 prompt is done, click the KEEP button, run /clear, reenable opus 5 as the model, reenable Allow ALL, Change agent to Task Planner, run step 3A prompt

/03A-plan runDate=2026-09-09  taskSlug=springboot-active-active-inventory planSlug=springboot-active-active-remediation-plan

9) When Step 3A is done, click the KEEP button, run /clear, reenable opus 5 as the model, reneable Allow ALL, leave agent to Task Planner, run step 3B prompt

/03B-report runDate=2026-09-09  taskSlug=springboot-active-active-inventory planSlug=springboot-active-active-remediation-plan

10) When step 3B is done, the assessment report should be created. Assessment report will be created under .copilot-tracking/plans/reports and have the name code-level-resiliency-assessment.md

Summary of each step work will also be created and stored in the handoffs subfolder of each agent folder, but full details are in the normal locations


## Prompt Approach/Assumptions

Approach
- minimum prompts
- maximize flexibility
- use guidance and rules/policy to direct the Model
- Assessment report is just a report, the details in output files drive the process
- Support assessment and refactor implementation in one package
- modularize the approach so it can be easily updated with minimal to no changes to the prompts themselves. For example adding a new shared service just requires a new grounding file and editing the registry so the prompts know it exists. P0-P3 definitions are outside the prompts and imported, refactoring can target priority (P0-P1), specific findings in a list, waves, or a combination.

This grounding approach provides direction and control on the assessment. There are clear instructions that this is a code only assessment, no CICD, no deployment, no infrastructure aspects will be assessed. There is a core assumption that the infra is alrady setup via some other proccess and it configured for multi-region Active-active resiliency per the designs of the shared services (except for SQL which is A-S and Kafka which can be either)

There is policy logic built in for Kafka for example following our agreed rules
- If Cosmos DB only exists in a repo, then Kafka is A-A
- if Azure SQL exists in a repo (regardless if CosmosDB also exists) the Kafka is A-S
- if no CosmosDB or Sql exists but Kafka is in use, assume A-S

This can be enforced using the application-architecture-context files

There is a master grounding file for assessment rules and then there are files for each shared service with rules. The grounding files define what we are looking for at a min

### Assessment inventory Options

Optional assessment domains

The new context controls:

application_code
application_configuration
container_build
cicd_pipeline
deployment_configuration
infrastructure_as_code
deployed_infrastructure

Controlled by

application-context/assessment-scope-context.yml
grounding/governance/assessment-scope-schema.yml

### Testing Options

Testing-output modes

The assessment report now supports the following modes for testing and validation data:

full
summary
roadmap_only
hidden

Recommended default

report_preferences:
  testing_output:
    mode: summary
    show_test_findings: true
    show_test_code: false
    show_validation_commands: false
    show_acceptance_criteria: true
    show_validation_evidence: false
    include_consolidated_validation_strategy: true