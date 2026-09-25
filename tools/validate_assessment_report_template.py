#!/usr/bin/env python3
from pathlib import Path
import re, sys
SECTIONS = [('assessment-overview', 'Assessment Overview'), ('resiliency-recommendations', 'Resiliency-Focused Recommendations'), ('non-resiliency-recommendations', 'Non-Resiliency-Focused Recommendations'), ('evidence-gap-analysis', 'Repository and IaC Evidence Gap Analysis'), ('full-finding-matrix', 'Full Finding Matrix'), ('standards-alignment', 'Standards Alignment'), ('implementation-roadmap', 'Implementation Roadmap'), ('appendix-traceability', 'Appendix A: Traceability')]
text = Path(sys.argv[1]).read_text(encoding="utf-8")
errors=[]
if text.count("# Code-Level Resiliency Assessment") != 1:
    errors.append("H1 title must occur exactly once")
positions=[]
header_start="<!-- content:report-header:start -->"; header_end="<!-- content:report-header:end -->"
for value,label in [(header_start,"report header start marker"),(header_end,"report header end marker")]:
    if text.count(value)!=1: errors.append(f"{label} must occur once: {value}")
if text.find(header_start) < text.find("# Code-Level Resiliency Assessment"): errors.append("report header block must follow the H1 title")
if text.find(header_end) > text.find("## Table of Contents"): errors.append("report header block must precede the table of contents")
for sid,title in SECTIONS:
    marker=f"<!-- section:{sid} -->"; heading=f"## {title}"
    start=f"<!-- content:{sid}:start -->"; end=f"<!-- content:{sid}:end -->"
    positions.append(text.find(marker))
    for value,label in [(marker,"section marker"),(heading,"heading"),(start,"start marker"),(end,"end marker")]:
        if text.count(value)!=1: errors.append(f"{label} must occur once: {value}")
if any(p<0 for p in positions) or positions!=sorted(positions): errors.append("section order invalid")
if text.count("[Back to Top](#top)") != len(SECTIONS): errors.append("back-to-top count invalid")
if text.count("<!-- report-governance:start -->")!=1 or text.count("<!-- report-governance:end -->")!=1: errors.append("governance region invalid")
if text.count("<!-- report-metadata:start -->")!=1 or text.count("<!-- report-metadata:end -->")!=1: errors.append("metadata region invalid")
if text.count("<!-- schema-conformance:start -->")!=1 or text.count("<!-- schema-conformance:end -->")!=1: errors.append("conformance region invalid")
ids=re.findall(r"<!-- finding:([A-Za-z0-9_-]+) -->",text)
if len(ids)!=len(set(ids)): errors.append("duplicate finding markers")
print("PASSED" if not errors else "FAILED\n- "+"\n- ".join(errors))
sys.exit(1 if errors else 0)
