#!/usr/bin/env python3
from pathlib import Path
import sys,re
secs=[('assessment-overview', 'Assessment Overview'), ('resiliency-recommendations', 'Resiliency-Focused Recommendations'), ('non-resiliency-recommendations', 'Non-Resiliency-Focused Recommendations'), ('evidence-gap-analysis', 'Repository and IaC Evidence Gap Analysis'), ('full-finding-matrix', 'Full Finding Matrix'), ('standards-alignment', 'Standards Alignment'), ('implementation-roadmap', 'Implementation Roadmap'), ('appendix-traceability', 'Appendix A: Traceability')]
t=Path(sys.argv[1]).read_text(); e=[]; ps=[]
for sid,h in secs:
 m=f"<!-- section:{sid} -->"; hd=f"## {h}"; ps.append(t.find(m))
 if t.count(m)!=1:e.append(m)
 if t.count(hd)!=1:e.append(hd)
 if t.count(f"<!-- content:{sid}:start -->")!=1:e.append(sid+":start")
 if t.count(f"<!-- content:{sid}:end -->")!=1:e.append(sid+":end")
if ps!=sorted(ps) or min(ps)<0:e.append("section order")
if t.count("[Back to Top](#top)")!=8:e.append("back-to-top count")
ids=re.findall(r"<!-- finding:([A-Za-z0-9_-]+) -->",t)
if len(ids)!=len(set(ids)):e.append("duplicate finding markers")
print("PASSED" if not e else "FAILED: "+", ".join(e));sys.exit(bool(e))
