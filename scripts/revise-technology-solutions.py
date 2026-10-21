#!/usr/bin/env python3
from pathlib import Path
import sys,importlib.util,json,re
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'scripts'))
from solution_steps import numeric_steps
BOOK=ROOT/'books/tecnologia-aeroespacial';sys.path.insert(0,str(BOOK/'scripts'))
import problem_bank
spec=importlib.util.spec_from_file_location('technology_procedures',BOOK/'solutions/procedures.py');module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
folder=BOOK/'solutions/generated';folder.mkdir(exist_ok=True)
text=(BOOK/'latex/problemas.tex').read_text();records=[]
for p in problem_bank.bank():
 r=module.ROUTES[p['key']];env={d['symbol']:d['value'] for d in p['given']}
 out,checks=numeric_steps(r['steps'],env)
 body=r'\textbf{Elección y deducción del procedimiento.} '+r['strategy']+'\n\n'+out
 (folder/(p['key']+'.tex')).write_text(body+'\n');records.append(dict(key=p['key'],steps=checks))
 a=text.index(r'\begin{studiumworked}{'+p['key']);b=text.index(r'\textbf{10. Resultado.}',a)
 if r'\input{../solutions/generated/'+p['key']+'.tex}' in text[a:b]:continue
 start=text.index(r'\textbf{7.',a)
 text=text[:start]+r'\input{../solutions/generated/'+p['key']+'.tex}\n'+text[b:]
(BOOK/'latex/problemas.tex').write_text(text)
(BOOK/'reports/solution-procedure-checks.json').write_text(json.dumps(dict(solutions=len(records),scope='Authored derivations and arithmetic, not independent academic approval',records=records),ensure_ascii=False,indent=2)+'\n')
print(len(records),'technology solutions expanded')
