from pathlib import Path
import json,math
import numpy as np
from scipy.integrate import quad,solve_ivp
from scipy.optimize import minimize_scalar
from models import *
RDIR=Path(__file__).resolve().parents[1]
bank=json.loads((RDIR/'evidence/problem-bank.json').read_text())
registry=[]
namespace={k:getattr(math,k) for k in ['sqrt','sin','cos','tan','asin','acos','atan','log','exp','pi']};namespace['abs']=abs
for p in bank:
 for t in p['tests']:
    got=eval(t['expression'],{'__builtins__':{}},namespace)
    registry.append(dict(problem=p['key'],quantity=t['name'],method='ARITHMETIC_REPLAYED',engine='Python math, contrastado con SymPy de generación',expected=t['expected'],got=got,passed=math.isclose(got,t['expected'],rel_tol=1e-10,abs_tol=1e-10),scope='Misma sustitución; no demuestra el modelo físico.'))
def cross(name,a,b,scope,tol=1e-8):
    registry.append(dict(problem=name,method='MODEL_CROSSCHECK',got=float(a),reference=float(b),passed=math.isclose(a,b,rel_tol=tol,abs_tol=1e-8),scope=scope,expert_review='PENDING'))
def expected(key,idx):return next(p for p in bank if p['key']==key)['tests'][idx]['expected']
# Las claves de los ejercicios se fijan por el orden del banco y se comprueban por título.
bytitle={p['title']:p for p in bank}
def expval(title,idx=0):return bytitle[title]['tests'][idx]['expected']
pol=Polar(34,.023,.043,1.6);rho=isa(5000)[2]
sol=integrate_jet(pol,6200,5100,rho,118,1.72e-5,rtol=1e-10,max_step=30)
cross('Reactor a TAS constante',sol['time'],expval('Reactor a TAS constante'),'ODE de masa y evento final frente a integral arcotangente.')
cl=pol.cl_jet_range();cd=pol.cd(cl)
q=quad(lambda m:pol.speed(m,rho,cl)/(1.72e-5*m*G*cd/cl),5100,6200,epsabs=1e-6)[0]
cross('Reactor a incidencia constante',q,expval('Reactor a incidencia constante'),'Cuadratura en masa de avance por gasto frente a diferencia de raíces.')
gl=Polar(16.4,.0125,.029,1.55);clg=gl.cl_ld()
g=glide_integral(gl,445,3600,300,clg,wind=-7)
cross('Descenso integral con viento',g['time'],expval('Descenso integral con viento'),'Cuadratura con equilibrio exacto y densidad variable frente a primitiva troposférica.')
cross('Descenso integral: alcance viento',g['ground_range'],expval('Descenso integral con viento',2),'Avance horizontal y desplazamiento de viento con el mismo tiempo.')
pr=Polar(18.2,.025,.048,1.65);cp=.305/3.6e6;et=.81;clp=pr.cl_minpower();rhop=isa(2500)[2]
time=quad(lambda m:1/(cp/et*pr.power(pr.speed(m,rhop,clp),m,rhop)),1440,1760,epsabs=1e-7)[0]
cross('Autonomía de hélice a densidad fija',time,expval('Autonomía de hélice a densidad fija',1),'Cuadratura de gasto por potencia al eje frente a primitiva W^(-3/2).')
tk=Polar(19,.034,.052,1.8)
roll=ground_roll(tk,1620,1.225,34,lambda v:5200,.028,.62)
cross('Carrera de despegue con reacción variable',roll['distance'],expval('Carrera de despegue con reacción variable'),'Cuadratura sobre aceleración frente a expresión logarítmica.')
brake=ground_roll(tk,1620,1.225,31,lambda v:0,.32,.18,braking=True)
cross('Frenado con sustentación residual',brake['distance'],expval('Frenado con sustentación residual'),'Cuadratura de frenado frente a primitiva, conservando signo y descarga del tren.')
M=np.array([[-.6,1],[-3.5,-1.4]]);l=np.linalg.eigvals(M)
cross('Autovalores de un modelo sintético',abs(l[0].imag),expval('Autovalores de un modelo sintético',1),'Algoritmo matricial de autovalores frente a polinomio característico.')
# Misión de ida y retorno: integración en distancia con evento fijo y descarga entre fases.
pj=Polar(47,.024,.045,1.5);rhj=isa(5500)[2];clj=pj.cl_jet_range();ctj=1.65e-5
def segment(mi):
    def fun(x,y):
        m=y[0];v=pj.speed(m,rhj,clj);D=pj.drag(v,m,rhj)
        return [-ctj*D/v,1/v]
    return solve_ivp(fun,[0,700000],[mi,0],rtol=1e-10,atol=1e-10,max_step=5000).y[:,-1]
m1,t1=segment(9200);m2,t2=segment(m1-900)
cross('Ida, descarga y retorno: masa final',m2,expval('Ida, descarga y retorno sin repostar',2),'ODE en distancia, descarga de 900 kg y segundo tramo, frente a inversión de Breguet.')
cross('Ida, descarga y retorno: tiempo',t1+t2,expval('Ida, descarga y retorno sin repostar',4),'Tiempo integrado simultáneamente con masa y reiniciado al descargar.')
gw=Polar(16.8,.013,.030,1.6)
def objective(cl):
    z=glide_exact(gw,460,1.02,cl);return (z['horizontal']-10)/z['sink']
cls=np.linspace(.2,1.6,20001);vals=np.array([objective(cl) for cl in cls]);at=cls[np.argmax(vals)]
cross('Viento: barrido frente a optimizador',at,expval('Elegir velocidad para volver contra viento'),'Barrido de 20001 puntos frente a optimizador acotado; tolerancia ligada a separación de rejilla.',tol=2e-4)
report=dict(total=len(registry),passed=sum(r['passed'] for r in registry),failed=sum(not r['passed'] for r in registry),records=registry,
 limitations=['El replay con dos motores aritméticos no es independencia científica.','Los cruces numéricos comparten parámetros e hipótesis; no validan aviones reales.','Las comprobaciones de límites y aplicabilidad textual requieren revisión experta.'])
(RDIR/'reports/problem-checks.json').write_text(json.dumps(report,indent=2,ensure_ascii=False))
print(json.dumps({k:report[k] for k in ['total','passed','failed']}))
assert report['failed']==0
