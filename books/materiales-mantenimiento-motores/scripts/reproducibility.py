from pathlib import Path
import shutil,subprocess,json,hashlib,os
R=Path(__file__).resolve().parents[1];D=R/'work/reproducibility'
if D.exists():shutil.rmtree(D)
D.mkdir(parents=True)
for f in ['main.tex','problemas.tex','simulacros.tex']:shutil.copy2(R/f,D/f)
for d in ['latex','content','figures']:shutil.copytree(R/d,D/d)
results=[]
for name in ['main','problemas','simulacros']:
 cp=subprocess.run(['latexmk','-pdf','-interaction=nonstopmode','-halt-on-error','-outdir=build',name+'.tex'],cwd=D,capture_output=True)
 (R/'reports'/f'repro-{name}.log').write_bytes(cp.stdout+cp.stderr)
 if cp.returncode:raise RuntimeError(name+' no recompila')
 logs=(D/'build'/f'{name}.log').read_text(errors='replace')
 before=subprocess.check_output(['pdftotext','-layout',str(R/'build'/f'{name}.pdf'),'-'])
 after=subprocess.check_output(['pdftotext','-layout',str(D/'build'/f'{name}.pdf'),'-'])
 originfo=subprocess.check_output(['pdfinfo',str(R/'build'/f'{name}.pdf')],text=True)
 newinfo=subprocess.check_output(['pdfinfo',str(D/'build'/f'{name}.pdf')],text=True)
 page=lambda s:int(next(l.split(':')[1] for l in s.splitlines() if l.startswith('Pages:')))
 row={'document':name,'build_exit':cp.returncode,'pages_original':page(originfo),'pages_clean_build':page(newinfo),'text_identical':before==after,'text_sha256':hashlib.sha256(after).hexdigest(),'overfull':logs.count('Overfull'),'undefined':logs.count('undefined'),'warnings':logs.count('Warning')};results.append(row)
 assert row['text_identical'] and row['overfull']==row['undefined']==0,row
 print(name,row['pages_clean_build'],'páginas; texto idéntico; sin desbordamientos',flush=True)
(R/'reports/reproducibility.json').write_text(json.dumps(results,ensure_ascii=False,indent=2))
