#!/usr/bin/env python3
from pathlib import Path
import importlib.util,sys,json,re
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'scripts'))
from solution_steps import numeric_steps
BOOK=ROOT/'books/materiales-mantenimiento-motores'
spec=importlib.util.spec_from_file_location('materials_procedures',BOOK/'solutions/manual_procedures.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
records=[]
for n,case in m.CASES.items():
 body,checks=numeric_steps(case['steps'],case['values'])
 out=r'\par\textbf{Desarrollo para comparar tu intento.} '+case['strategy']+'\n\n'+body
 name=f'M{n:02}';(BOOK/'solutions/generated'/(name+'.tex')).write_text(out+'\n')
 path=BOOK/'content'/f'c{n:02}.tex';text=path.read_text();a=text.index(r'\caso{'+name)
 # Find the end of the title argument, then balance the body argument.
 title_end=text.index('}{',a)+1;b=title_end+1;depth=1
 while depth:
  if text[b] in '{}':
   preceding=len(text[:b])-len(text[:b].rstrip('\\'))
   if preceding%2==0:depth+=1 if text[b]=='{' else -1
  b+=1
 token=r'\input{solutions/generated/'+name+'.tex}'
 if token not in text[a:b]:text=text[:b-1]+'\n'+token+'\n'+text[b-1:]
 path.write_text(text);records.append(dict(key=name,steps=checks))
(BOOK/'evidence/manual-solution-procedures.json').write_text(json.dumps(dict(scope='Eleven numeric manual cases expanded; qualitative cases retain their evidence-based reasoning, not independent approval',records=records),ensure_ascii=False,indent=2)+'\n')
print(len(records),'manual numeric cases expanded')
