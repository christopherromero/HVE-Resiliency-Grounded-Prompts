#!/usr/bin/env python3
from pathlib import Path
import sys,re
secs=[('assessment-overview', '1. Assessment Overview'), ('resiliency-recommendations', '2. Resiliency-Focused Recommendations'), ('non-resiliency-recommendations', '3. Non-Resiliency-Focused Recommendations'), ('evidence-gap-analysis', '4. Repository and IaC Evidence Gap Analysis'), ('full-finding-matrix', '5. Full Finding Matrix'), ('standards-alignment', '6. Standards Alignment'), ('implementation-roadmap', '7. Implementation Roadmap'), ('appendix-traceability', '8. Appendix A: Traceability')]
def slug(h):
 return re.sub(r"\s+","-",re.sub(r"[^\w\s-]","",h.strip().lower()))
t=Path(sys.argv[1]).read_text(encoding="utf-8"); e=[]; ps=[]
if t.count("<!-- content:report-header:start -->")!=1:e.append("report-header:start")
if t.count("<!-- content:report-header:end -->")!=1:e.append("report-header:end")
for sid,h in secs:
 m=f"<!-- section:{sid} -->"; ps.append(t.find(m))
 if t.count(m)!=1:e.append(m)
 # sections are H1; anchor the pattern to a line start so "## x" cannot satisfy "# x"
 if len(re.findall(r"(?m)^#\s+"+re.escape(h)+r"\s*$",t))!=1:e.append(f"# {h}")
 if t.count(f"<!-- content:{sid}:start -->")!=1:e.append(sid+":start")
 if t.count(f"<!-- content:{sid}:end -->")!=1:e.append(sid+":end")
if ps!=sorted(ps) or min(ps)<0:e.append("section order")
if t.count("[Back to Top](#top)")!=8:e.append("back-to-top count")
ids=re.findall(r"<!-- finding:([A-Za-z0-9_-]+) -->",t)
if len(ids)!=len(set(ids)):e.append("duplicate finding markers")
# every in-document anchor link must resolve to a real heading slug or an explicit anchor id
anchors={slug(x) for x in re.findall(r"(?m)^#{1,6}\s+(.+?)\s*$",t)}|set(re.findall(r'<a id="([^"]+)"',t))
for txt,tgt in re.findall(r"\[([^\]]+)\]\(#([^)]+)\)",t):
 if tgt not in anchors:e.append(f"broken anchor #{tgt}")
print("PASSED" if not e else "FAILED: "+", ".join(sorted(set(e))));sys.exit(bool(e))
