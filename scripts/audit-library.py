#!/usr/bin/env python3
"""Replay existing audits and add independently constructed model regressions.

Historical report files are restored byte for byte after each legacy audit;
new results and execution receipts live under reports/edition-v2.
"""
from pathlib import Path
import hashlib,json,subprocess,sys
from datetime import datetime,timezone
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'reports/edition-v2'
TASKS=[
 ('structures',['scripts/audit-estructuras.py'],['reports/bundle-audit/estructuras.json']),
 ('structures-companions',['scripts/audit-estructuras-companions.py'],['reports/bundle-audit/estructuras-companions.json']),
 ('turbomachinery',['scripts/audit-turbomaquinas.py'],['reports/bundle-audit/turbomaquinas.json']),
 ('fluids-symbolic',['books/mecanica-fluidos/scripts/verificaciones_simbolicas_fase6.py','--json',str(OUT/'fluids-symbolic.json')],[]),
 ('fluids-bank',['books/mecanica-fluidos/scripts/check_fluid_bank.py'],['books/mecanica-fluidos/reports/fluid-bank-checks.json']),
 ('technology-models',['books/tecnologia-aeroespacial/scripts/check_science.py'],['books/tecnologia-aeroespacial/reports/scientific-tests.json']),
 ('technology-bank',['books/tecnologia-aeroespacial/scripts/check_bank.py'],['books/tecnologia-aeroespacial/reports/bank-crosschecks.json']),
 ('rocket-models',['books/motores-cohete/scripts/check_science.py'],['books/motores-cohete/reports/science-checks.json']),
 ('flight-models',['books/mecanica-vuelo/scripts/verify_models.py'],['books/mecanica-vuelo/reports/model-checks.json']),
 ('flight-additional',['books/mecanica-vuelo/scripts/additional_checks.py'],['books/mecanica-vuelo/reports/additional-symbolic-checks.json']),
 ('flight-bank',['books/mecanica-vuelo/scripts/validate_problem_bank.py'],['books/mecanica-vuelo/reports/problem-checks.json']),
 ('flight-all-cases',['books/mecanica-vuelo/scripts/validate_all_cases.py'],['books/mecanica-vuelo/reports/all-cases-checks.json']),
 ('independent-models',['scripts/verify-library-models.py'],[]),
 ('figure-science',['scripts/verify-figure-science.py'],[]),
 ('figure-review',['scripts/audit-figure-review.py'],[]),
 ('preservation',['scripts/check-library-preservation.py'],[]),
]

def main():
 OUT.mkdir(exist_ok=True);receipts=[]
 for name,args,artifacts in TASKS:
  saved={path:(ROOT/path).read_bytes() if (ROOT/path).exists() else None for path in artifacts}
  try:
   cp=subprocess.run([sys.executable,*args],cwd=ROOT,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
   (OUT/(name+'.txt')).write_bytes(cp.stdout)
   for relative in artifacts:
    path=ROOT/relative
    if path.exists():(OUT/(name+'.json')).write_bytes(path.read_bytes())
  finally:
   for relative,old in saved.items():
    path=ROOT/relative
    if old is None:path.unlink(missing_ok=True)
    else:path.write_bytes(old)
  receipts.append(dict(id=name,command=[sys.executable,*args],exit_code=cp.returncode,
    script_sha256=hashlib.sha256((ROOT/args[0]).read_bytes()).hexdigest(),output=name+'.txt'))
  print(name,cp.returncode,flush=True)
 import importlib.metadata
 (OUT/'audit-runs.json').write_text(json.dumps(dict(
    run_at=datetime.now(timezone.utc).isoformat(),python=sys.version,
    packages={m:importlib.metadata.version(m) for m in ['sympy','numpy','scipy','pint','pymupdf']},
    status='PASSED' if all(r['exit_code']==0 for r in receipts) else 'FAILED',
    scope='Existing audits plus selected independently derived checks; no automatic expert approval.',runs=receipts),ensure_ascii=False,indent=2)+'\n')
 raise SystemExit(any(r['exit_code'] for r in receipts))
if __name__=='__main__':main()
