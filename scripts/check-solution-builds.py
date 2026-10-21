#!/usr/bin/env python3
"""Require reviewed procedures to be actual inputs of each intended PDF."""
from pathlib import Path
import json,hashlib,re,ast
ROOT=Path(__file__).resolve().parents[1]
builds={};files=[]
for p in sorted((ROOT/'dist/studium').glob('*/build-report.json')):
 r=json.loads(p.read_text());assert r['status']=='compiled',p
 for d in r['documents']:
  assert d['status']=='COMPILED',d
  assert hashlib.sha256((ROOT/d['file']).read_bytes()).hexdigest()==d['sha256'],d['file']
  for item in d['inputs']:
   assert hashlib.sha256((ROOT/item['path']).read_bytes()).hexdigest()==item['sha256'],item['path']
  key=(p.parent.name,Path(d['file']).stem.split('-')[-1]);builds[key]={x['path'] for x in d['inputs']}
  files.append(dict(file=d['file'],sha256=d['sha256'],inputs_checked=len(d['inputs'])))
assert len(builds)==21,len(builds)
expect={k:set() for k in builds}
def require(book,kind,name):expect[(book,kind)].add(f'books/{book}/solutions/generated/{name}.tex')
for r in json.loads((ROOT/'reports/solution-procedure-legacy.json').read_text())['records']:
 for kind in (('manual',) if r['book']=='estructuras-aeroespaciales' else ('manual','problemas')):require(r['book'],kind,r['key'])
for r in json.loads((ROOT/'books/mecanica-fluidos/solutions/source-cases.json').read_text()):require('mecanica-fluidos','manual',f'mf-{r["index"]:03}')
for r in json.loads((ROOT/'reports/solution-procedure-native.json').read_text())['records']:
 book,key=r['book'],r['key']
 if book=='mecanica-vuelo':kind={'problems':'problemas','workshops':'manual','exams':'simulacros'}[r['kind']]
 elif book=='motores-cohete':kind='manual' if key.startswith('M') else 'simulacros' if key.startswith('S') else 'problemas'
 else:kind='simulacros' if key.startswith('S') else 'problemas'
 require(book,kind,key)
for book,pattern in [('materiales-mantenimiento-motores','M*.tex'),('tecnologia-aeroespacial','M*.tex')]:
 for p in (ROOT/'books'/book/'solutions/generated').glob(pattern):require(book,'manual',p.stem)
for p in (ROOT/'books/tecnologia-aeroespacial/solutions/generated').glob('P*.tex'):require('tecnologia-aeroespacial','problemas',p.stem)
for n in (1,2,3):require('tecnologia-aeroespacial','problemas',f'EX{n}')
for n in (1,2):require('motores-cohete','manual',f'M{n:02}')
expect[('mecanica-vuelo','manual')].add('books/mecanica-vuelo/solutions/methods/manual-c05.tex')
# Structures companions intentionally inline these same operations. Bind each
# calculation to its own worked block in a source actually read by that PDF.
inline=[]
book='estructuras-aeroespaciales'
legacy=json.loads((ROOT/'reports/solution-procedure-legacy.json').read_text())['records']
all_keys=[r['key'] for r in legacy if r['book']==book]
module=ast.parse((ROOT/'books'/book/'scripts/make_companions.py').read_text())
papers=next(ast.literal_eval(n.value) for n in module.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='PAPERS' for t in n.targets))
for kind,filename,keys in [('problemas','problem-solutions.tex',all_keys),('simulacros','exam-papers-and-solutions.tex',[k for paper in papers for k in paper])]:
 path=f'books/{book}/content/{filename}'
 assert path in builds[(book,kind)],path
 text=(ROOT/path).read_text()
 for key in keys:
  begin=text.index(r'\begin{studiumworked}{'+key+'}')
  end=text.index(r'\end{studiumworked}',begin)
  original=(ROOT/'books'/book/'solutions/generated'/(key+'.tex')).read_text()
  formulas=re.findall(r'\\\[\\fitmath\{.*?\}\\\]',original,re.S)
  assert formulas and all(f in text[begin:end] for f in formulas),(kind,key)
  inline.append(dict(book=book,document=kind,key=key,source=path,formulas_checked=len(formulas)))
missing=[dict(book=k[0],document=k[1],missing=sorted(v-builds[k])) for k,v in expect.items() if v-builds[k]]
report=dict(scope='Actual recorded TeX inputs and current hashes, not independent academic approval',pdfs=files,required_procedure_inclusions=sum(map(len,expect.values()))+len(inline),inline_procedures=inline,missing=missing)
(ROOT/'reports/solution-build-checks.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print('PDFs:',len(files),'required procedure inclusions:',report['required_procedure_inclusions'],'missing groups:',len(missing))
if missing:raise SystemExit(json.dumps(missing,ensure_ascii=False))
