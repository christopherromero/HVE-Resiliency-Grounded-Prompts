# Here is the process for setting up your workstation

There is a ZIP that has the folder structure and the required files

/Assessment
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

 - .github
    - instructions
    - modernize
 - .vscode
 - application-context
    - templates
 - grounding
    - archive
    - dependencies
    - exclusions
    - governance
    - master
    - registry
 - prompts
    - archive
 - source/customer-app (repo source goes here)
execution prompts.md


1) Create a directory called assessment
2) Right click the Zip, select properties, check unblock, apply, ok
3) Open the ZIP and copy the contents into C:\assessment
4) From VSCode, open the C;\assessment folder so it is the workspace root


## Prep for the repo assessment

1) Copy, clone, the repository code into the customer-app folder
2) Open assessment-context/assessment-context.md and change the application name at the top to the name of the repo you are assessing.
3) Prepare the Solution-architecture-context and the application-architecture context files, see below

### Setting the Solution Architecture Context

solution-application-context.md - this allows you to specify the overall application architecture context across all of the microservices

There is only one template for the solution architecture, so just copy it tot he application-context folder and rename it to solution-application-context.md and edit it.

### Setting the repo architecture context

application-architecture-context.md - this allows you to specify the context of the repo you are assessing.

Under the \application-context\templates folder are sample templates for DB/Kafka scenarios

For the application-architecture-context, You take the sample template that would apply (Active-Active with Cosmos, Active-Standby with SQL, No DB but still Kafka) copy it to the \application-context folder and then rename it to application-architecture-context.md and the edit it

NOTE: There are simple form templates and then detailed form templates, use the simple for now.

## Instructions to run the assessment for a prepared repo

1) Open the Execution Prompts.md file in the folder root, these are the steps you will execute
2) Copy the step 1 instructions from Follow: to the end of the step instructions
3) Set your agent to Task Reasearcher
4) Set the model to Claude Opus 5.0
5) If you are using MS EMU license, Enable Autopilot so you do not have to approve anything (status bar under the agent selection)
6) Paste the step 1 prompt into the chat window and run it,
7) The output files have the todays date in the name, you must ensure the instructions are updated with todays date in the paths. For example Step 1 produces the inventory file INVENTORY_ARTIFACT=.copilot-tracking/research/2026-09-02/springboot-active-active-inventory-research.md, you must make sure that Step 2, 3A, 3B all have the correct filename before you run those instructions, best to edit them all now.
When Step 1 Prompt is done, run /clear, reenable opus as the model, reenable autopilot, Change agent to Task Reviewer , run the step 2 instructions
8) When Step 2 prompt is done, run /clear, reenable opus as the model, reenable autopilot, Change agent to Task Planner, run step 3A instructions
9) When Step 3A is done, run /clear, reenable opus as the model, reneable autopilot, leave agent to Task Planner, run step 3B instructions
10) When step 3B is done, the assessment report should be created. Assessment report will be created under .copilot-tracking/plans/reports and have the name code-level-resiliency-assessment.md

Summary of each step work will also be created and stored in the handoffs subfolder of each agent folder, but full details are in the normal locations


## New features



