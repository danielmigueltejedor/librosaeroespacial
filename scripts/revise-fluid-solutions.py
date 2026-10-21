#!/usr/bin/env python3
"""Rebuild detailed solutions in the existing manual without losing figures."""
from pathlib import Path
import json,re,sys,hashlib
import importlib.util
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from solution_steps import numeric_steps
BOOK=ROOT/'books/mecanica-fluidos'
spec=importlib.util.spec_from_file_location('fluid_procedures',BOOK/'solutions/procedures.py')
module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
rows=json.loads((BOOK/'solutions/source-cases.json').read_text())
assert set(module.ROUTES)==set(range(1,129))
generated=BOOK/'solutions/generated';generated.mkdir(exist_ok=True)
records=[]
for row in rows:
 n=row['index'];route=module.ROUTES[n]
 env={k:v['value'] for k,v in row['given'].items()}
 for k,(v,u) in route['extra'].items():env[k]=v
 try:body,calculations=numeric_steps(route['steps'],env)
 except Exception as exc:raise ValueError(f'Exercise {n}: {exc}') from exc
 content=r'\noindent\textbf{Elección del procedimiento.} '+route['strategy']+'\n\n'+body
 if route['check']:content+='\n\n'+r'\noindent\textbf{Contraste y comparación.} '+route['check']
 (generated/f'mf-{n:03d}.tex').write_text(content+'\n')
 records.append(dict(index=n,prompt_sha256=row['prompt_sha256'],steps=calculations,
                     source_sha256=hashlib.sha256(content.encode()).hexdigest()))
# Replace only the reasoning section. The statement, authored data, diagrams,
# model and references stay at their existing locations.
manual=BOOK/'latex/manual.tex';text=manual.read_text()
marks=list(re.finditer(re.escape(r'\noindent\textbf{Enunciado}'),text));assert len(marks)==128
for i,m in reversed(list(enumerate(marks))):
 end=marks[i+1].start() if i+1<len(marks) else len(text)
 block=text[m.start():end]
 prompt=block[len(m[0]):].split(r'\noindent\textbf{')[0].strip()
 if hashlib.sha256(prompt.encode()).hexdigest()!=rows[i]['prompt_sha256']:
  raise ValueError(f'Statement changed: {i+1}')
 labels=['Desarrollo'] if i+1 not in [17,18,19,20] else ['Resolución','Modelo y resolución']
 done=False
 for label in labels:
  pattern=re.escape(r'\noindent\textbf{'+label+'}')+r'.*?(?=\\noindent\\textbf\{)'
  if re.search(pattern,block,re.S):
   replacement=r'\noindent\textbf{Desarrollo paso a paso}'+'\n\n'+r'\input{../solutions/generated/mf-'+f'{i+1:03d}'+'.tex}\n\n'
   block=re.sub(pattern,lambda m:replacement,block,count=1,flags=re.S);done=True;break
 # Idempotent rebuild: prior input remains, generated file gets refreshed.
 if not done:assert f'generated/mf-{i+1:03d}.tex' in block
 # Historic replay summaries did not contain the equations and some values
 # were explicitly false. They remain in source-cases.json as audit history.
 pattern=re.escape(r'\noindent\textbf{Comprobación de los pasos}')+r'.*?(?=\\noindent\\textbf\{)'
 block=re.sub(pattern,'',block,count=1,flags=re.S)
 text=text[:m.start()]+block+text[end:]
# Correct known conclusions rather than keeping a misleading old result.
text=text.replace(r'\eta_p \approx 0{,}588',r'\eta_p \approx 0{,}5940')
text=text.replace('la fuerza de pico es varias veces mayor que la media.',
                  'la fuerza de pico no puede deducirse sin conocer la historia temporal del impacto.')
text=text.replace('Una carrera de unos 1,3 km es del orden de las distancias de despegue reales de aviones de pasillo único; la cifra real es algo mayor porque la fuerza neta disminuye con la velocidad.',
                  'En el modelo dado, la distancia hasta la velocidad de rotación es 1312,5 m. No representa una distancia certificada de despegue: faltan la variación de fuerzas, la rotación y el ascenso posterior.')
manual.write_text(text)
report=dict(scope='128 existing manual solutions, algebra and computed intermediate values; authored model review, not independent academic approval',
            reviewer='same authoring model',solutions=len(records),steps=sum(len(r['steps']) for r in records),records=records)
(BOOK/'reports/solution-procedure-checks.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(report['solutions'],'solutions;',report['steps'],'computed operations')
