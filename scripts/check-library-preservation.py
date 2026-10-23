#!/usr/bin/env python3
"""Keep citations, problem identifiers and mathematical figures when revising imports."""
from pathlib import Path
import subprocess,json,re,hashlib
ROOT=Path(__file__).resolve().parents[1]
BASE='119bc583b4f525c221f0dc815936fffbb4f770a4'
rows=[]
replacements=json.loads((ROOT/'reports/edition-v2/figure-replacements.json').read_text()) if (ROOT/'reports/edition-v2/figure-replacements.json').exists() else []
paths=subprocess.check_output(['git','ls-tree','-r','--name-only',BASE,'books'],cwd=ROOT,text=True).splitlines()
for name in paths:
    if not name.endswith('.tex'):continue
    old=subprocess.check_output(['git','show',f'{BASE}:{name}'],cwd=ROOT,text=True)
    path=ROOT/name
    if not path.is_file():
        removed=[]
        for registry in (ROOT/'books').glob('*/studium-import.json'):
            record=json.loads(registry.read_text()).get('removed_after_import')
            if record:removed+=[str(registry.parent.relative_to(ROOT)/f) for f in record['files']]
        if name in removed:
            rows.append(dict(path=name,passed=True,note='Removed after import with a recorded reason'));continue
        rows.append(dict(path=name,passed=False,error='Original TeX document removed'));continue
    new=path.read_text()
    for category,pattern in [('bibliography',r'\\bibitem(?:\[[^]]*\])?\{([^}]+)\}'),
                             ('citations',r'\\cite\w*\*?(?:\[[^]]*\])*\{([^}]+)\}'),
                             ('labels',r'\\label\{([^}]+)\}'),
                             ('problem_ids',r'\b(?:PRB-\d{4}|C\d{2}-\d{2}-[PRT])\b')]:
        before=set(re.findall(pattern,old));after=set(re.findall(pattern,new));missing=sorted(before-after)
        rows.append(dict(path=name,category=category,original_count=len(before),current_count=len(after),missing=missing,passed=not missing))
    if 'preamble' not in name and 'editorial' not in name and 'cover' not in name:
        # Original dependencies stay, or have an explicit source-bound, hash-checked redraw receipt.
        before=set(re.findall(r'\\(?:includegraphics(?:\[[^]]*\])?|figura|ilustra)\{([^}]+)\}',old))
        after=set(re.findall(r'\\(?:includegraphics(?:\[[^]]*\])?|figura|ilustra)\{([^}]+)\}',new))
        accepted=[]
        for r in replacements:
            if r['source']!=name or r['old_dependency'] not in before or r['new_dependency'] not in after:continue
            oldasset=(path.parent/r['old_dependency']).resolve();newasset=(path.parent/r['new_dependency']).resolve()
            if oldasset.exists() and newasset.exists() and hashlib.sha256(oldasset.read_bytes()).hexdigest()==r['old_sha256'] and hashlib.sha256(newasset.read_bytes()).hexdigest()==r['new_sha256']:
                accepted.append(r['old_dependency'])
        missing=sorted(before-after-set(accepted))
        rows.append(dict(path=name,category='figure_dependencies',missing=missing,documented_redraws=accepted,passed=not missing))
report=dict(baseline=BASE,status='PASSED' if all(r['passed'] for r in rows) else 'FAILED',checks=len(rows),
            scope='Identifier and literal dependency preservation, not proof of semantic equivalence or correctness.',records=rows)
out=ROOT/'reports/edition-v2/preservation.json';out.parent.mkdir(exist_ok=True);out.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(report['status'],report['checks'],'preservation checks')
for r in rows:
    if not r['passed']:print(r)
raise SystemExit(report['status']!='PASSED')
