"""Caso de equilibrio TP de agua: no cálculo de prestaciones reales."""
from pathlib import Path
import cea,numpy as np,json,hashlib
R=Path(__file__).resolve().parents[1]
reactants=cea.Mixture(['H2O']);products=cea.Mixture(['H2O','H2','O2','OH','O','H'])
solver=cea.EqSolver(products,reactants=reactants);solution=cea.EqSolution(solver);rows=[]
for p in [1.,10.]:
 for T in [1500.,2500.,3500.]:
  solver.solve(solution,cea.TP,T,p,np.array([1.]));assert solution.converged
  x={k:float(v) for k,v in solution.mole_fractions.items()};atoms={'H2O':(2,1),'H2':(2,0),'O2':(0,2),'OH':(1,1),'O':(0,1),'H':(1,0)}
  H=sum(x[k]*atoms[k][0] for k in x);O=sum(x[k]*atoms[k][1] for k in x)
  assert abs(sum(x.values())-1)<1e-8 and abs(H/O-2)<1e-7
  rows.append(dict(T_K=T,p_bar=p,mole_fractions=x,MW_kg_kmol=float(solution.MW),gamma_s=float(solution.gamma_s),cp_frozen_kJ_kgK=float(solution.cp_fr),cp_equilibrium_kJ_kgK=float(solution.cp_eq),element_ratio_H_O=H/O))
db=Path(cea.__file__).parent/'share/cea/thermo.lib'
out={'version':cea.__version__,'calculation':'TP equilibrium; reactant H2O; only six neutral gas species; no condensed phases or ions','pressure_unit':'bar (not Pa)','database_sha256':hashlib.sha256(db.read_bytes()).hexdigest(),'status':'EJECUTADO Y REPRODUCIDO','limitations':'Modelo de equilibrio restringido; no ensayo, no simulación de motor, no predicción de Isp real. Propiedades de la API en kJ/kg/K y MW numéricamente kg/kmol.','rows':rows}
(R/'reports/cea-case.json').write_text(json.dumps(out,ensure_ascii=False,indent=2));print(json.dumps(out,ensure_ascii=False,indent=2))
