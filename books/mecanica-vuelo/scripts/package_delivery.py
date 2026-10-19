"""Empaqueta sólo fuentes/evidencias entregables; excluye material privado y runtime."""
from pathlib import Path
import json,hashlib,zipfile,subprocess,shutil,sys
R=Path(__file__).resolve().parents[1]
D=Path(sys.argv[1]).resolve();D.mkdir(parents=True,exist_ok=True)
selected=set()
for name in ['main.tex','problemas.tex','simulacros.tex','requirements.txt','README.md','main.pdf','problemas.pdf','simulacros.pdf']:selected.add(Path(name))
for directory in ['content','latex','figures','evidence','scripts','project']:
 for p in (R/directory).rglob('*'):
  if not p.is_file() or '__pycache__' in p.parts:continue
  if directory=='project' and (p.suffix in ['.aux','.log','.out','.toc','.fls','.fdb_latexmk','.synctex'] or (p.suffix=='.pdf' and 'figures' not in p.parts)):continue
  if directory=='scripts' and p.name=='read_inputs.py':continue
  selected.add(p.relative_to(R))
for p in (R/'reports').iterdir():
 if p.suffix not in ['.md','.json'] and p.name not in ['framework-tests.log','compile-main-final.log','compile-problems-final.log','compile-exams-final.log','native-audits-final.log','final-inventory.log']:continue
 if p.name in ['studium-api-progress.json','jsbsim-probe.json']:continue
 selected.add(p.relative_to(R))
for p in (R/'simulations/results').glob('*.csv'):selected.add(p.relative_to(R))
for p in (R/'simulations').glob('*.xml'):selected.add(p.relative_to(R))
tracked=subprocess.check_output(['git','-C',str(R/'framework'),'ls-files'],text=True).splitlines()
for p in tracked:
 q=Path('framework')/p
 if (R/q).is_file():selected.add(q)
manifest={str(p):dict(bytes=(R/p).stat().st_size,sha256=hashlib.sha256((R/p).read_bytes()).hexdigest()) for p in sorted(selected)}
extra={'framework/COMMIT.txt':b'675274202360f717f3b835444e26d0f95d2a3c33\n'}
for p,data in extra.items():manifest[p]=dict(bytes=len(data),sha256=hashlib.sha256(data).hexdigest())
archive=D/'Studium_Mecanica_de_Vuelo_proyecto_completo.zip'
with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED,compresslevel=8) as z:
 for p in sorted(selected):z.write(R/p,'Studium-Mecanica-de-Vuelo/'+str(p))
 z.writestr('Studium-Mecanica-de-Vuelo/MANIFEST-SHA256.json',json.dumps(manifest,ensure_ascii=False,indent=2))
 for p,data in extra.items():z.writestr('Studium-Mecanica-de-Vuelo/'+p,data)
with zipfile.ZipFile(archive) as z:
 assert z.testzip() is None
 for p,v in manifest.items():assert hashlib.sha256(z.read('Studium-Mecanica-de-Vuelo/'+p)).hexdigest()==v['sha256']
 assert not any('/sources/private/' in p or '/work/' in p or '/.git/' in p or '/jsbsim-upstream/' in p for p in z.namelist())
 for required in ['main.tex','problemas.tex','simulacros.tex','framework/LICENSE','framework/src/studium/mcp/server.py','evidence/equation-inventory-native.json','simulations/results/b747-endurance-28000lbm.csv']:
  assert 'Studium-Mecanica-de-Vuelo/'+required in z.namelist()
names={'main':'Studium_Mecanica_de_Vuelo_Manual.pdf','problemas':'Studium_Mecanica_de_Vuelo_Problemas_resueltos.pdf','simulacros':'Studium_Mecanica_de_Vuelo_Simulacros_y_soluciones.pdf'}
for old,new in names.items():shutil.copy2(R/(old+'.pdf'),D/new)
for name in ['INFORME-FINAL.md','LIMITACIONES.md']:shutil.copy2(R/'reports'/name,D/name)
record=dict(files=len(selected),zip_bytes=archive.stat().st_size,zip_sha256=hashlib.sha256(archive.read_bytes()).hexdigest(),zip_test='passed',member_hashes='all passed',private_material='excluded',outputs={new:hashlib.sha256((D/new).read_bytes()).hexdigest() for new in names.values()})
(D/'comprobacion-entrega.json').write_text(json.dumps(record,ensure_ascii=False,indent=2))
print(json.dumps(record,ensure_ascii=False,indent=2))
