"""Consistencia de cp de equilibrio y derivada de entalpía; mismo CEA, no validación externa."""
from pathlib import Path
import cea,numpy as np,json
R=Path(__file__).resolve().parents[1];react=cea.Mixture(['H2O']);prod=cea.Mixture(['H2O','H2','O2','OH','O','H']);solver=cea.EqSolver(prod,reactants=react);sol=cea.EqSolution(solver);rows=[]
for T in [1500.,2500.,3500.]:
 for p in [1.,10.]:
  hs=[];step=.02;cp=None
  for temperature in [T-step,T,T+step]:
   solver.solve(sol,cea.TP,temperature,p,np.array([1.]));assert sol.converged;hs.append(float(sol.enthalpy))
   if temperature==T:cp=float(sol.cp_eq)
  derivative=(hs[2]-hs[0])/(2*step);error=abs(derivative-cp)/cp;assert error<3e-4
  rows.append(dict(T_K=T,p_bar=p,cp_api_kJ_kgK=cp,dh_dT_kJ_kgK=derivative,relative_error=error))
(R/'reports/cea-cp-finite-difference.json').write_text(json.dumps({'method':'Diferencia centrada de h(T,p) a presión fija, paso 0.02 K; mismo código y base. Tolerancia relativa 3e-4. No es validación independiente.','rows':rows},ensure_ascii=False,indent=2));print('6 controles de derivada de entalpía; error máximo',max(x['relative_error'] for x in rows))
