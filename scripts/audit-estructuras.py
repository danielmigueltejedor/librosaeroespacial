"""Recalculate all published worked steps with rounding-aware tolerances.

Original exercise data are public; no private excerpts or authoring state needed.
This is an arithmetic audit plus selected separate physical routes, not approval.
"""
from pathlib import Path
from decimal import Decimal,InvalidOperation
import json,math,re
import sympy as sp
import numpy as np
from scipy.integrate import quad
import runpy
ROOT=Path(__file__).resolve().parents[1]
rows=json.loads((ROOT/'reports/bundle-audit/structures-problem-bank.json').read_text())['problems']
records=[]
thin_solve=runpy.run_path(str(ROOT/'scripts/thin-wall-audit.py'))['solve']
for p in rows:
    geometry=thin_solve(p['thin_wall_geometry']) if p.get('thin_wall_geometry') and p['id'] in [f'PRB-{i:04d}' for i in range(216,224)] else None
    for i,step in enumerate(p['solution'].get('steps',[]),1):
        env={'pi':sp.pi,'sqrt':sp.sqrt,'sin':sp.sin,'cos':sp.cos,'tan':sp.tan,'log':sp.log}
        try:
            if 'expression' not in step:
                assert geometry is not None,(p['id'],step)
                matches=re.findall(r'([A-Za-z_]+)=(-?\d+(?:\.\d+)?(?:e[+-]?\d+)?)',step['equation'])
                assert matches,(p['id'],step)
                for name,expected_text in matches:
                    ex=Decimal(expected_text);expected=float(ex);actual=geometry[name]
                    tol=max(.51*10.**ex.as_tuple().exponent,abs(expected)*3e-9,1e-10)
                    records.append(dict(problem=p['id'],step=i,quantity=name,passed=bool(abs(actual-expected)<=tol),actual=float(actual),expected=expected,absolute_tolerance=tol,route='independent wall/boom integrals and shear-flow network with zero twist'))
                continue
            actual=float(sp.sympify(step['expression'],locals=env).evalf(35))
            ex=Decimal(str(step['expected']));expected=float(ex)
            rounding=.51*10.**ex.as_tuple().exponent
            tol=max(rounding,abs(expected)*3e-9,1e-12)
            ok=math.isfinite(actual) and abs(actual-expected)<=tol
            records.append(dict(problem=p['id'],step=i,passed=ok,actual=actual,expected=expected,absolute_tolerance=tol,unit=step.get('unit'),route='SymPy 35-digit recalculation of printed-step expression, rounded target'))
        except Exception as e:records.append(dict(problem=p['id'],step=i,passed=False,error=str(e)))
    if geometry:
        expected=float(p['solution']['steps'][-1]['expected'])
        records.append(dict(problem=p['id'],quantity='maximum shear stress',passed=math.isclose(geometry['tau_max'],expected,rel_tol=2e-8,abs_tol=1e-7),actual=geometry['tau_max'],expected=expected,route='critical points of reconstructed wall-flow polynomials'))

def ck(name,ok,route):records.append(dict(name=name,passed=bool(ok),route=route))
# Distinct constructions for important families: eigenvalues, load integrals,
# direct energy derivatives and closed/open thin-wall torsion.
tensor=np.array([[90.,15.,0.],[15.,110.,0.],[0.,0.,100.]])
principal=np.linalg.eigvalsh(tensor)
vm=math.sqrt(sum((principal[i]-principal[(i+1)%3])**2 for i in range(3))/2)
ck('C02 eigenvalue von Mises',abs(vm-5*math.sqrt(39))<1e-10,'symmetric-matrix eigenvalues versus component invariant')
E=71700.;I=5e7;P=3000.;L=2500.
rotation=quad(lambda x:P*x/(E*I),0,L)[0]
ck('C07 cantilever end rotation',math.isclose(rotation,P*L**2/(2*E*I),rel_tol=1e-12),'virtual-moment quadrature versus elastic-curve slope')
M0=sp.symbols('M0');x=sp.symbols('x');energy=sp.integrate((P*x+M0)**2/(2*E*I),(x,0,L))
ck('C07 Castigliano rotation',abs(float(sp.diff(energy,M0).subs(M0,0))-rotation)<1e-12,'derivative of energy with auxiliary moment retained')
G=26955.;At=120*80;Pt=120/3+80/1+120/2+80/2;J=4*At**2/Pt
ck('C05 variable-wall twist',abs(2400000*1500/(G*J)-.0797046)<5e-8,'Bredt compliance from four wall integrals')
ck('C05 closed box shear',2100000/(2*120*70*2)==62.5,'torque from constant shear flow')
ck('C05 open U shear',abs(20000*3/((120+80+120)*3**3/3)-20.8333333333)<1e-9,'Saint-Venant strip sum; not polar area moment')
Pbar,Lbar,Ebar,Abar=sp.symbols('P L E A',positive=True)
energy=Pbar**2*Lbar/(2*Ebar*Abar)
ck('C03 axial Castigliano',sp.simplify(sp.diff(energy,Pbar)-Pbar*Lbar/(Ebar*Abar))==0,'energy derivative versus direct axial strain')
failed=[r for r in records if not r['passed']]
out=dict(status='PASSED' if not failed else 'FAILED',problems=len(rows),checks=len(records),failed=len(failed),scope='All 105 original exercise step expressions, all C06 equation-only geometry results and reconstructed maximum shear stresses. Dimensional checks are not inferred from unit labels. Selected separate model checks; no certification of all theory, materials or applicability.',reviewer='same agent, fresh calculation pass',records=records)
(ROOT/'reports/bundle-audit/estructuras.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
print(len(records),'checks;',len(failed),'failures');print(json.dumps(failed[:12],ensure_ascii=False,indent=2))
raise SystemExit(bool(failed))
