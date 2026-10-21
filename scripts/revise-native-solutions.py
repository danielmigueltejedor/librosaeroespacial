#!/usr/bin/env python3
"""Expose numeric operations omitted by companion renderers.

Keep authored hypotheses and algebra; never turn a stored literal into a
claimed derivation. Additional method-specific routes are authored separately.
"""
from pathlib import Path
import json,sys,re,ast,importlib.util
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'scripts'))
from solution_steps import numeric_steps

def replay(p):
 rows=[];literals=[]
 for i,t in enumerate(p['tests'],1):
  tree=ast.parse(t['expression'],mode='eval')
  if isinstance(tree.body,ast.Constant) or (isinstance(tree.body,ast.UnaryOp) and isinstance(tree.body.operand,ast.Constant)):
   literals.append(dict(index=i,name=t.get('name',f'y_{i}'),value=t['expected'],unit=t.get('unit','')));continue
  rows.append(dict(target=f'y_{i}',expression=t['expression'],expected=t['expected'],unit=t.get('unit',''),why=t.get('name',f'Magnitud {i}')+'.'))
 body,checks=numeric_steps(rows) if rows else ('',[])
 return body,checks,literals

def replace_ninth(path, cases, prefix, heading_pattern=None):
 text=path.read_text();marks=list(re.finditer(r'\\apartado\{9\. Sustitución numérica\}',text));assert len(marks)==len(cases),(path,len(marks),len(cases))
 for m,p in reversed(list(zip(marks,cases))):
  end=text.find(r'\apartado{10.',m.end());assert end>=0
  body=r'\apartado{9. Sustitución numérica}{Se conservan los resultados intermedios sin redondear y se muestran todas las operaciones escalares disponibles.}'+'\n\n'+r'\input{'+prefix+'/'+p['key']+'.tex}\n\n'
  text=text[:m.start()]+body+text[end:]
 path.write_text(text)

records=[]
book=ROOT/'books/mecanica-vuelo';folder=book/'solutions/generated';folder.mkdir(parents=True,exist_ok=True)
sets=[('problems',json.loads((book/'evidence/problem-bank.json').read_text())),
      ('workshops',json.loads((book/'evidence/manual-workshops.json').read_text())),
      ('exams',[q for e in json.loads((book/'evidence/exam-bank.json').read_text()) for q in e['questions']])]
for kind,cases in sets:
 for p in cases:
  body,checks,literals=replay(p)
  if not body:body=r'\noindent Los resultados de este caso proceden de las operaciones vectoriales o del método numérico desarrollados en el apartado anterior.'
  method=book/'solutions/methods'/(p['key']+'.tex')
  if method.is_file():body=r'\input{solutions/methods/'+p['key']+'.tex}\n\n'+(body if checks else '')
  (folder/(p['key']+'.tex')).write_text(body+'\n')
  records.append(dict(book=book.name,key=p['key'],kind=kind,steps=checks,non_scalar_results=literals))
 if kind=='workshops':
  for p in cases:replace_ninth(book/'content'/f't{p["ch"]:02}.tex',[p],'solutions/generated')
 else:replace_ninth(book/'content'/('problems.tex' if kind=='problems' else 'exams.tex'),cases,'solutions/generated')

# Materials: the algebraic routes are already individually authored in D.
# Include each registered numerical substitution, instead of only the final
# shorthand substitution string. Qualitative maintenance cases keep reasoning.
book=ROOT/'books/materiales-mantenimiento-motores';folder=book/'solutions/generated';folder.mkdir(parents=True,exist_ok=True)
cases=json.loads((book/'evidence/problem-bank.json').read_text())
for p in cases:
 body,checks,literals=replay(p);assert not literals,p['key']
 (folder/(p['key']+'.tex')).write_text(body+'\n')
 records.append(dict(book=book.name,key=p['key'],steps=checks))
text=(book/'problemas.tex').read_text()
for p in cases:
 start=text.index(r'\section{'+p['key']+'.');end=text.find(r'\section{',start+1);end=len(text) if end<0 else end
 block=text[start:end];a=block.index(r'\apartado{Sustitución numérica}');b=block.index(r'\caso{Resultado}',a)
 block=block[:a]+r'\apartado{Sustitución numérica}{Se desarrolla cada operación con las unidades del resultado.}'+'\n'+r'\input{solutions/generated/'+p['key']+'.tex}\n'+block[b:]
 text=text[:start]+block+text[end:]
(book/'problemas.tex').write_text(text)
# Academic exam answers already show reasoning. Add their actual operations.
cases=[(e['key']+'-'+str(i),q) for e in json.loads((book/'evidence/exam-bank.json').read_text()) for i,q in enumerate(e['questions'],1)]
text=(book/'simulacros.tex').read_text();section=text.index(r'\part{Soluciones y criterios de corrección}')
for key,q in cases:
 if not q.get('tests'):continue
 body,checks,literals=replay(q);assert not literals,key
 (folder/(key+'.tex')).write_text(body+'\n');records.append(dict(book=book.name,key=key,steps=checks))
 needle=q['solution']
 # The renderer escapes prose outside math. Match section title instead.
 title=key.split('-')[-1]+'. '+q['title'].replace(',propagación',', propagación');needle=r'\section{'+title+'}'
 if needle not in text[section:]:raise ValueError((key,title))
 a=text.index(needle,section);b=text.find(r'\section{',a+1)
 if b<0:b=text.find(r'\backmatter',a)
 token=r'\input{solutions/generated/'+key+'.tex}'
 if token not in text[a:b]:text=text[:b]+'\n'+token+'\n'+text[b:]
(book/'simulacros.tex').write_text(text)

# Rocket examples already state the physical choices and every requested
# intermediate in prose. Append the complete substitutions of their controls.
book=ROOT/'books/motores-cohete';sys.path.insert(0,str(book/'scripts'))
spec=importlib.util.spec_from_file_location('rocket_cases',book/'scripts/problem_bank.py');module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
sets=[('manual',module.manual()),('bank',module.bank()),('exams',[q for e in module.exams() for q in e])]
folder=book/'solutions/generated';folder.mkdir(parents=True,exist_ok=True)
for kind,cases in sets:
 for p in cases:
  body,checks,literals=replay(p)
  (folder/(p['key']+'.tex')).write_text(body+'\n');records.append(dict(book=book.name,key=p['key'],steps=checks,non_scalar_results=literals))
  paths=[book/'latex'/(p['key']+'.tex')] if kind=='manual' else [book/'latex'/('problemas.tex' if kind=='bank' else 'simulacros.tex')]
  for path in paths:
   text=path.read_text();m=re.search(r'\\begin\{studiumworked\}\{'+re.escape(p['key'])+r'[. ·]',text)
   if not m:raise ValueError((path,p['key']))
   b=text.index(r'\textbf{Resultados.}',m.start())
   token=r'\input{../solutions/generated/'+p['key']+'.tex}'
   if token not in text[m.start():b]:text=text[:b]+r'\textbf{Operaciones para contrastar el cálculo.}'+'\n'+token+'\n'+text[b:]
   path.write_text(text)
(ROOT/'reports/solution-procedure-native.json').write_text(json.dumps(dict(scope='Complete scalar operations plus authored algebra; non-scalar outputs separately identified, not independent approval',records=records),ensure_ascii=False,indent=2)+'\n')
print(len(records),'native cases updated')
