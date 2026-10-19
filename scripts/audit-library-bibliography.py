#!/usr/bin/env python3
"""Locate references and distinguish availability from scientific support."""
from pathlib import Path
import importlib.util,json,re
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'reports/edition-v2'
s=importlib.util.spec_from_file_location('inventory',ROOT/'scripts/inventory-library.py');iv=importlib.util.module_from_spec(s);s.loader.exec_module(iv)
entries=[]
for cfg in sorted((ROOT/'books').glob('*/studium-import.json')):
 d=json.loads(cfg.read_text());work=cfg.parent/d['workdir']
 for doc in d['documents']:
  for path,text in iv.reachable(work/doc['source'],work):
   for m in re.finditer(r'\\bibitem(?:\[[^]]*\])?\{([^}]+)\}',text):
    tail=text[m.end():];next_entry=re.search(r'\\(?:bibitem|end\{thebibliography)',tail)
    body=tail[:next_entry.start()] if next_entry else tail
    urls=re.findall(r'\\(?:url|href)\{([^}]+)\}',body)
    entries.append(dict(book=cfg.parent.name,document=doc['source'],source=str(path.relative_to(ROOT)),id=m[1],citation=body.strip(),urls=urls,
       risks=(['WIKIPEDIA_NOT_PRIMARY_SCIENTIFIC_EVIDENCE'] if any('wikipedia.org' in x for x in urls) else [])+(['NO_PUBLIC_URL_LOCATED'] if not urls else []),
       bibliographic_identity='NOT_RECHECKED_IN_FULL',semantic_support='PENDING_EXPERT_REVIEW',
       limits='A compiled citation or reachable URL is not evidence that the source supports the nearby assertion. Recommended commercial books are not treated as read.'))
(OUT/'bibliography-register.json').write_text(json.dumps(entries,ensure_ascii=False,indent=2)+'\n')
print(len(entries),'located bibliography records;',sum(bool(e['risks']) for e in entries),'flagged for documentary review')
