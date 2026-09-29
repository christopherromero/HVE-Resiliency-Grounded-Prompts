#!/usr/bin/env python3
"""Validate grounding/registry/microsoft-pattern-registry.yml.

Usage:
  python tools/validate_microsoft_pattern_registry.py <registry.yml> [--check-links]

Structural checks always run. --check-links additionally issues an HTTP HEAD
request per pattern URL and fails on any non-200 response.
"""
import collections
import sys
from pathlib import Path

import yaml

FINDING_ELIGIBLE = "finding_reference_and_alignment"
ALIGNMENT_ONLY = "standards_alignment_only"


def structural(doc):
    errors = []
    pats = doc.get("patterns") or []
    fams = doc.get("control_families") or []
    if not pats:
        errors.append("no patterns defined")
    if not fams:
        errors.append("no control families defined")

    famids = {f["family_id"] for f in fams}
    controls = [c for f in fams for c in f["controls"]]

    for f in fams:
        if f["control_count"] != len(f["controls"]):
            errors.append(f"{f['family_id']}: control_count {f['control_count']} != {len(f['controls'])} listed")

    dupe_controls = [k for k, v in collections.Counter(controls).items() if v > 1]
    if dupe_controls:
        errors.append(f"controls in more than one family: {sorted(dupe_controls)}")

    covered = set()
    for p in pats:
        pid = p.get("pattern_id", "<missing id>")
        for field in ("pattern_id", "title", "url", "usage", "precedence", "link_status"):
            if field not in p:
                errors.append(f"{pid}: missing {field}")
        if p.get("link_status") != "verified_200":
            errors.append(f"{pid}: link_status is not verified_200")
        if "/en-us/" in p.get("url", ""):
            errors.append(f"{pid}: url is not locale-neutral")
        usage = p.get("usage")
        if usage not in (FINDING_ELIGIBLE, ALIGNMENT_ONLY):
            errors.append(f"{pid}: unknown usage {usage!r}")
        pf = p.get("applies_to_control_families") or []
        for fm in pf:
            if fm not in famids:
                errors.append(f"{pid}: references unknown family {fm}")
        if usage == ALIGNMENT_ONLY and pf:
            errors.append(f"{pid}: standards_alignment_only must not bind to a family")
        if usage == FINDING_ELIGIBLE:
            covered |= set(pf)

    orphans = sorted(famids - covered)
    if orphans:
        errors.append(f"families with no finding-eligible pattern: {orphans}")

    for label, key in (("pattern_id", "pattern_id"), ("url", "url")):
        dupes = [k for k, v in collections.Counter(p.get(key) for p in pats).items() if v > 1]
        if dupes:
            errors.append(f"duplicate {label}: {dupes}")

    return errors


def check_links(doc):
    import urllib.request

    errors = []
    for p in doc["patterns"]:
        req = urllib.request.Request(p["url"], method="HEAD", headers={"User-Agent": "registry-linkcheck"})
        try:
            with urllib.request.urlopen(req, timeout=30) as r:
                if r.status != 200:
                    errors.append(f"{p['pattern_id']}: HTTP {r.status} {p['url']}")
        except Exception as exc:  # noqa: BLE001 - any failure is a link failure
            errors.append(f"{p['pattern_id']}: {exc} {p['url']}")
    return errors


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return 2
    doc = yaml.safe_load(Path(sys.argv[1]).read_text(encoding="utf-8"))
    errors = structural(doc)
    if "--check-links" in sys.argv:
        errors += check_links(doc)

    pats = doc.get("patterns") or []
    fams = doc.get("control_families") or []
    print(
        f"patterns={len(pats)} "
        f"(finding-eligible={sum(1 for p in pats if p.get('usage') == FINDING_ELIGIBLE)}, "
        f"alignment-only={sum(1 for p in pats if p.get('usage') == ALIGNMENT_ONLY)}) "
        f"families={len(fams)} controls={sum(f['control_count'] for f in fams)}"
    )
    if errors:
        print("FAILED:")
        for e in errors:
            print(f"  - {e}")
        return 1
    print("PASSED")
    return 0


if __name__ == "__main__":
    sys.exit(main())
