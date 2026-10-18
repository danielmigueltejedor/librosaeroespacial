"""Check companion coverage and case identity, separately from model arithmetic."""
from pathlib import Path
from collections import Counter
import hashlib
import json
import re
import pymupdf

ROOT=Path(__file__).resolve().parents[1]
BOOK=ROOT/'books/estructuras-aeroespaciales'
bank_path=ROOT/'reports/bundle-audit/structures-problem-bank.json'
bank=json.loads(bank_path.read_text())['problems']
lookup={p['id']:p for p in bank}
selection=json.loads((BOOK/'content/exam-selections.json').read_text())
ids=sum(selection['papers'],[])
problem_tex=(BOOK/'content/problem-solutions.tex').read_text()
exam_tex=(BOOK/'content/exam-papers-and-solutions.tex').read_text()
worked=re.findall(r'\\section\{(PRB-\d{4})',problem_tex)
exam_worked=re.findall(r'\\section\{(PRB-\d{4})',exam_tex)
records=[]
def check(name,ok):
    records.append(dict(name=name,passed=bool(ok)))
check('105 unique worked cases, exactly the public bank',len(worked)==105 and set(worked)==set(lookup))
check('eight chapters in problem book',problem_tex.count(r'\chapter{')==8)
check('four papers of five different cases',len(selection['papers'])==4 and all(len(p)==5 for p in selection['papers']) and len(set(ids))==20)
check('full eight-theme coverage across papers',{lookup[i]['ch'] for i in ids}=={f'c{i:02d}' for i in range(1,9)})
check('one solution per selected case',Counter(exam_worked)==Counter(ids))
check('obsolete dependent example references removed',all(s not in problem_tex for s in ['del ejemplo anterior','Repita el cálculo del ejemplo','del ejemplo (']))
check('rotation label has not regressed','Desplazamiento total por suma de tramos' not in problem_tex.split(r'\section{PRB-0225')[1].split(r'\section{')[0])
inventory=[]
for kind,expected in [('problemas',set(lookup)),('simulacros',set(ids))]:
    path=ROOT/'dist/studium/estructuras-aeroespaciales'/f'estructuras-aeroespaciales-{kind}.pdf'
    pdf=pymupdf.open(path)
    titles=[entry[1] for entry in pdf.get_toc()]
    bookmarks=[re.search(r'PRB-\d{4}',title)[0] for title in titles if re.search(r'PRB-\d{4}',title)]
    check(kind+': every expected case has one solution bookmark',len(bookmarks)==len(expected) and set(bookmarks)==expected)
    if kind=='simulacros':
        toc=pdf.get_toc();start=next(row[2]-1 for row in toc if row[1].endswith(' Enunciados'))
        stop=next(row[2]-1 for row in toc if row[1].endswith(' Soluciones razonadas'))
        paper_text='\n'.join(pdf[n].get_text() for n in range(start,stop))
        check('all twenty problem IDs present in statement part',set(re.findall(r'PRB-\d{4}',paper_text))==expected)
        check('no solved manual-figure captions in statement part','Figura ' not in paper_text)
    inventory.append(dict(file=str(path.relative_to(ROOT)),pages=len(pdf),sha256=hashlib.sha256(path.read_bytes()).hexdigest()))
arithmetic=json.loads((ROOT/'reports/bundle-audit/estructuras.json').read_text())
check('405 existing bank controls passed',arithmetic['checks']==405 and arithmetic['failed']==0)
out=dict(status='PASSED' if all(r['passed'] for r in records) else 'FAILED',
    scope='Case identity, chapter coverage and rendered solution/statement inventory. Model and arithmetic checks remain in estructuras.json. Same authoring agent; no independent academic approval.',
    source_bank_sha256=hashlib.sha256(bank_path.read_bytes()).hexdigest(),
    chapters=dict(sorted(Counter(p['ch'] for p in bank).items())),
    problems=len(bank),papers=4,selected_existing_cases=len(ids),new_numerical_variants=0,
    diagrams_from_manual=sum(x['figures'] for x in json.loads((BOOK/'content/manual-figure-bindings.json').read_text())),
    records=records,documents=inventory)
(ROOT/'reports/bundle-audit/estructuras-companions.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
print(out['status'],len(records),'coverage checks')
for r in records:
    if not r['passed']:print(r)
raise SystemExit(out['status']!='PASSED')
