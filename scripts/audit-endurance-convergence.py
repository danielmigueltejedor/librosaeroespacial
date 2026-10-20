#!/usr/bin/env python3
"""Full fuel exhaustion runs; dt refinement under one fixed feedback law.
Requires the isolated, pinned model checkout prepared by replay-flight-simulations.py.
"""
from pathlib import Path
import hashlib,json,os,shutil,subprocess,sys
R=Path(__file__).resolve().parents[1];W=R/'dist/simulation-replay';O=R/'reports/edition-v2'
def main():
 upstream=W/'simulations/jsbsim-upstream'
 assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=upstream,text=True).strip()=='66f7fafc07fe13e7ede9db20873030fed2881713'
 shutil.copy2(R/'books/mecanica-vuelo/scripts/run_endurance.py',W/'scripts/run_endurance.py')
 runs=[]
 for dt in [.1,.05,.025]:
  with (W/f'endurance-dt-{dt}.log').open('w') as log:
   subprocess.run([sys.executable,'scripts/run_endurance.py'],cwd=W,env=os.environ|{'STUDIUM_ENDURANCE_DT':str(dt),'OPENBLAS_NUM_THREADS':'1'},stdout=log,stderr=subprocess.STDOUT,check=True)
  report=json.loads((W/'reports/endurance-results.json').read_text());runs.append(report)
  for p in (W/'simulations/results').glob('b747-endurance-*.csv'):shutil.copy2(p,p.with_name(p.stem+f'-dt-{dt}.csv')) if '-dt-' not in p.stem else None
  print('Full endurance dt',dt,[(c['initial_fuel_lbm'],c['simulated_time_s'],c['termination']) for c in report['cases']],flush=True)
 comparisons=[]
 for i in range(2):
  cases=[r['cases'][i] for r in runs];times=[c['simulated_time_s'] for c in cases];deltas=[abs(times[i+1]-times[i]) for i in range(2)]
  item=dict(initial_fuel_lbm=cases[0]['initial_fuel_lbm'],times_s=times,successive_differences_s=deltas,relative_last_difference=deltas[-1]/times[-1],all_exhausted=all(c['termination']=='USABLE_FUEL_EXHAUSTED' for c in cases))
  # Fuel threshold crossing is resolved only to the integration step; do not infer an order from it.
  item['passed']=item['all_exhausted'] and item['relative_last_difference']<.001
  comparisons.append(item)
 report=dict(runs=runs,comparisons=comparisons,passed=all(c['passed'] for c in comparisons),source_sha256=hashlib.sha256((W/'scripts/run_endurance.py').read_bytes()).hexdigest(),scope='Derived numerical verification of complete exhaustion trajectories, fixed model/control and 0.1/0.05/0.025 s. Threshold event quantized to dt; no experimental or certified endurance validation.')
 (O/'endurance-convergence.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
 if not report['passed']:raise SystemExit(1)
if __name__=='__main__':main()
