"""Auditoría de talleres, simulacros y CSV, con alcances explícitos."""
from pathlib import Path
import csv,json,math
import numpy as np
from scipy.optimize import brentq
from scipy.integrate import solve_ivp
from models import *
RDIR=Path(__file__).resolve().parents[1]
manual=json.loads((RDIR/'evidence/manual-workshops.json').read_text())
exams=[q for e in json.loads((RDIR/'evidence/exam-bank.json').read_text()) for q in e['questions']]
ns={k:getattr(math,k) for k in ['sqrt','sin','cos','tan','asin','acos','atan','log','exp','pi']};ns['abs']=abs
rows=[]
for p in manual+exams:
 for t in p['tests']:
    got=eval(t['expression'],{'__builtins__':{}},ns)
    rows.append(dict(case=p['key'],quantity=t['name'],passed=math.isclose(got,t['expected'],rel_tol=1e-10,abs_tol=1e-10),method='ARITHMETIC_REPLAYED',scope='Misma sustitución con Python math; no prueba de modelo ni independencia física.'))
def result(name,ok,detail,scope):rows.append(dict(case=name,passed=bool(ok),method='MODEL_OR_NUMERICAL_CHECK',detail=detail,scope=scope,expert_review='PENDING'))
by={p['key']:p for p in manual}
def val(k,i):return by[k]['tests'][i]['expected']
phi,th,ps=np.deg2rad([18,9,32]);C=c_body_ned(phi,th,ps);v=np.array([96,8,-5]);b=np.array([val('T02',i) for i in range(3)])
result('T02: ida y vuelta',np.max(abs(C.T@b-v))<1e-10,float(np.max(abs(C.T@b-v))),'Transformación y secuencia declaradas, complemento de ortogonalidad simbólica.')
a,d,T=[val('T06',i) for i in range(3)];qS=.5*1.04*66**2*26;cl=.24+5.2*a+.28*d;cd=.026+.046*cl*cl
res=[T*math.cos(a)-qS*cd,qS*cl+T*math.sin(a)-2450*G,.045-.72*a-1.08*d]
result('T06: residuos por componente',max(abs(res[0]),abs(res[1]))<1e-5 and abs(res[2])<1e-10,res,'Residuos de fuerza en N y coeficiente de momento por separado; no norma de dimensiones mezcladas.')
gl=Polar(16.2,.014,.032,1.55)
root=brentq(lambda cl:4*.032*cl**2-2*.032*gl.cd(cl)**2-3*gl.cd(cl),.8,1.5)
result('T08: raíz frente a mínimo',abs(root-val('T08',0))<1e-5,dict(root=root,minimum=val('T08',0)),'Dos métodos para condición exacta en dominio de la polar.')
pc=Polar(31,.025,.047,1.5)
def rhs(h,y):
 m=y[0];rho=isa(h)[2];T=9500*(rho/1.225)**.8;D=pc.drag(90,m,rho);c=(T-D)*90/(m*G)
 return [-1.8e-5*T/c,1/c,90/c]
sol=solve_ivp(rhs,[1200,4200],[5300,0,0],rtol=1e-10,atol=1e-10,max_step=12.5)
reference=np.array([val('T13',1),val('T13',0),val('T13',3)])
result('T13: refinamiento de altura',np.max(abs(sol.y[:,-1]/reference-1))<1e-8,dict(refined=sol.y[:,-1].tolist(),reference=reference.tolist()),'Ascenso aproximado, paso máximo 12.5 frente a 25 m; mismos parámetros e hipótesis.')
eta=val('T15',3)
result('T15: dominio de eficiencia',0<eta<=1,eta,'Condición necesaria energética para la definición de eficiencia dada; no valida el mapa docente.')
report=json.loads((RDIR/'reports/jsbsim-results.json').read_text());cv=report['convergence']
dv=[abs(cv[i]['TAS_m_s']-cv[i+1]['TAS_m_s']) for i in [0,1]]
dh=[abs(cv[i]['h_m']-cv[i+1]['h_m']) for i in [0,1]]
result('JSBSim T6: sensibilidad temporal',dv[1]<dv[0] and dh[1]<dh[0] and dv[1]<1e-4 and dh[1]<1e-3,dict(delta_TAS=dv,delta_h=dh,tolerance_TAS_m_s=1e-4,tolerance_h_m=1e-3),'Convergencia empírica de dos magnitudes finales en 60s; no orden formal global.')
for filename in ['b747-cruise-1800s.csv','b747-endurance-28000lbm.csv','b747-endurance-36000lbm.csv','t6-xml-executed.csv']:
 with (RDIR/'simulations/results'/filename).open() as stream:rr=list(csv.DictReader(stream))
 t=np.array([float(r['time_s']) for r in rr]);fuel=np.array([float(r['fuel_kg']) for r in rr]);flow=np.array([float(r['fuel_flow_kg_s']) for r in rr])
 integrated=float(np.trapezoid(flow,t));burn=float(fuel[0]-fuel[-1]);relative=abs(integrated-burn)/max(1,burn)
 result(filename+': balance combustible',relative<.02,dict(integral_kg=integrated,contents_change_kg=burn,relative_difference=relative,tolerance=.02),'Cuadratura trapezoidal con salida muestreada; incluye estado inicial y paso de agotamiento. Tolerancia de auditoría, no precisión de fabricante.')
 result(filename+': tiempo y valores',np.all(np.diff(t)>0) and all(math.isfinite(float(v)) for r in rr for v in r.values()),dict(rows=len(rr),duration=float(t[-1]-t[0])),'Integridad numérica del CSV y monotonía temporal.')
out=dict(total=len(rows),passed=sum(r['passed'] for r in rows),failed=sum(not r['passed'] for r in rows),records=rows)
(RDIR/'reports/all-cases-checks.json').write_text(json.dumps(out,ensure_ascii=False,indent=2));print({k:out[k] for k in ['total','passed','failed']})
assert out['failed']==0
