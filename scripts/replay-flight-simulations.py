#!/usr/bin/env python3
"""Run the published JSBSim experiments in an isolated copy, preserving original evidence.

Requires jsbsim==1.3.3 plus the book's numerical dependencies. The upstream
checkout is pinned; CSV outputs remain in dist/simulation-replay for inspection.
"""
from pathlib import Path
import hashlib,importlib.metadata,json,os,shutil,subprocess,sys
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'reports/edition-v2'
WORK=ROOT/'dist/simulation-replay';PIN='66f7fafc07fe13e7ede9db20873030fed2881713'
def main():
 if importlib.metadata.version('jsbsim')!='1.3.3':raise RuntimeError('Requires JSBSim 1.3.3')
 WORK.mkdir(parents=True,exist_ok=True)
 # Copy editable sources and existing CSV evidence; generated results go only to WORK.
 shutil.copytree(ROOT/'books/mecanica-vuelo',WORK,dirs_exist_ok=True)
 upstream=WORK/'simulations/jsbsim-upstream'
 if not (upstream/'.git').exists():
  subprocess.run(['git','clone','--depth','1','--branch','v1.3.3','https://github.com/JSBSim-Team/jsbsim.git',str(upstream)],check=True)
 sha=subprocess.check_output(['git','rev-parse','HEAD'],cwd=upstream,text=True).strip()
 if sha!=PIN:raise RuntimeError('Unexpected upstream commit; refusing to run')
 OUT.mkdir(exist_ok=True);records=[]
 for name in ['run_jsbsim','run_xml','run_endurance']:
  with (OUT/(name+'.txt')).open('w') as stream:
   cp=subprocess.run([sys.executable,'scripts/'+name+'.py'],cwd=WORK,stdout=stream,stderr=subprocess.STDOUT,
                     env=os.environ|{'OPENBLAS_NUM_THREADS':'1','OMP_NUM_THREADS':'1'})
  records.append(dict(script=name,exit_code=cp.returncode,jsbsim_commit=sha,source_sha256=hashlib.sha256((WORK/'scripts'/(name+'.py')).read_bytes()).hexdigest()))
  print(name,cp.returncode,flush=True)
 for name in ['jsbsim-results','xml-run','endurance-results']:
  source=WORK/'reports'/(name+'.json')
  if source.exists():(OUT/(name+'-replayed.json')).write_bytes(source.read_bytes())
 csvs=[dict(file=str(p.relative_to(WORK)),sha256=hashlib.sha256(p.read_bytes()).hexdigest(),bytes=p.stat().st_size) for p in sorted((WORK/'simulations/results').glob('*.csv'))]
 (OUT/'simulation-runs.json').write_text(json.dumps(dict(runs=records,csvs=csvs,jsbsim_version=importlib.metadata.version('jsbsim'),
    scope='New runs in an isolated copy; original evidence preserved. Educational models; no experimental validation. Full endurance step refinement remains pending.'),ensure_ascii=False,indent=2)+'\n')
 raise SystemExit(any(x['exit_code'] for x in records))
if __name__=='__main__':main()
