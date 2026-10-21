#!/usr/bin/env python3
from pathlib import Path
import re,json,sys,importlib.util
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'scripts'))
from solution_steps import numeric_steps
BOOK=ROOT/'books/tecnologia-aeroespacial'
spec=importlib.util.spec_from_file_location('technology_manual',BOOK/'solutions/manual_procedures.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
records=[]
for (ch,i),case in m.CASES.items():
 body,checks=numeric_steps(case['steps']);key=f'M{ch:02}-{i}'
 (BOOK/'solutions/generated'/(key+'.tex')).write_text(r'\par\textbf{Procedimiento completo para comparar tu solución.} '+case['strategy']+'\n\n'+body+'\n')
 path=BOOK/'content-layout'/f'c{ch:02}.tex';text=path.read_text();marks=list(re.finditer(re.escape(r'\begin{studiumworked}'),text));a=marks[i-1].start();b=text.index(r'\end{studiumworked}',a)
 token=r'\input{../solutions/generated/'+key+'.tex}'
 if token not in text[a:b]:text=text[:b]+token+'\n'+text[b:]
 path.write_text(text);records.append(dict(key=key,steps=checks))
(BOOK/'reports/manual-solution-procedure-checks.json').write_text(json.dumps(dict(solutions=len(records),scope='Authored model reasoning and scalar operations; not independent academic approval',records=records),ensure_ascii=False,indent=2)+'\n')
print(len(records),'manual examples expanded')
