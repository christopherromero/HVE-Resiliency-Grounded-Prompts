# Application Assessment Context

Application:
Ecommerce Platform

Language:
Java

Framework:
Spring Boot

Runtime:
AKS

Assessment Goal:
Determine whether the application can operate
correctly in an active-active deployment.

Do not assess infrastructure.

Assume shared services comply with
enterprise resiliency standards.

## Assessment Scope Control

Optional domain and report-rendering behavior is controlled by:

`application-context/assessment-scope-context.yml`

If the file is absent, assess application code and application configuration only. Deployed infrastructure remains out of scope in all supported configurations.
