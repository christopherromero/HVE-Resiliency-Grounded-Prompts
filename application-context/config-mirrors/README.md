---
description: Customer-supplied cart-service configuration mirror preparation
ms.date: 2026-10-21
---

# Cart Service Configuration Mirror

Copy the authentic YAML files supplied from the customer's external configuration
repository into this directory. No configuration files have been populated by the
framework. Application-local resources are not substitutes for server-side files.

## Declaration

Complete the `CFG-SRC-001` entry in
[assessment-scope-context.yml](../../assessment-scope-context.yml):

* Replace the declaration owner and approval or evidence-handoff reference with
  real customer-supplied values. Placeholder values leave authority unresolved.
* Set the configuration repository and source directory in `provenance.origin`.
  Record an export or source revision when available and the actual capture date.
* Confirm application name, ordered profiles, and label match the intended source.
* Replace the listed filenames with the exact files copied here. Include relevant
  shared and profile-specific configuration and preserve their original contents.
* Follow the customer's evidence-handling process. Do not commit credentials or
  other protected values. Record approved redaction in provenance; the fingerprint
  identifies the supplied copy, not an independently verified remote original.

The declaration uses this workspace-relative root:

```yaml
root_path: application-context/config-mirrors/cart-service
```

The active file list initially names `application.yml` and `application-prod.yml`.
Neither file is supplied by this change. Adjust the list if the external repository
uses application-specific names such as `cart-service-prod.yml`.

## Inventory Validation

Run from the workspace root with Python 3.11 or later and PyYAML:

```powershell
uv run --python 3.11 tools/validate_external_configuration_sources.py
```

The validator is read-only and prints metadata, validation status, and fingerprints,
not configuration contents. A nonzero exit status means required evidence is missing
or invalid. It does not detect clients, contact Config Server, resolve placeholders,
or merge effective keys. Step 1 performs those offline evidence and precedence tasks.

For existing detected-client declarations, or known binding observations, provide
an inventory-generated JSON file through `--observed-bindings`. The object is keyed
by source ID; cite actual inventory evidence rather than creating observations to
force a match. For example, this shape preserves absent client detection:

```json
{
  "CFG-SRC-001": {
    "config_client_detected": false,
    "evidence_refs": []
  }
}
```

`compute_at_inventory` captures SHA256 over the raw listed files in declaration
order. A supplied 64-character SHA256 is instead compared to those bytes. Both
modes record a per-file manifest. The context and copied files remain unchanged.

## Authority And Refresh

A valid customer declaration, source binding, complete local files, and successful
fingerprint handling establish authoritative configuration evidence for assessment.
They do not prove deployed consumption, resolve secret placeholders, or verify
runtime behavior. Known application/profile/label contradictions block the source;
absence of client detection alone does not block a customer-declared mirror.

Run a new Step 1 inventory and then Step 2 assessment after preparing the mirror.
The earlier assessments remain historical and must not be rewritten to apply the
new authority decision. Changed file contents require a new Step 1 fingerprint and
resolution. Remediation targets the external configuration repository; do not edit
these evidence files as a substitute for changing the actual configuration source.