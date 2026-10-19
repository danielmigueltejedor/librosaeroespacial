"""Comprobaciones originales: cada alcance de prueba se declara por separado."""
import json, math, sys
from pathlib import Path
import sympy as s
import numpy as np
from pint import UnitRegistry
from scipy.integrate import quad
from scipy.optimize import minimize_scalar
from models import *

ROOT=Path(__file__).resolve().parents[1]
checks=[]
def record(name,kind,ok,detail,scope):
    checks.append(dict(id=f'V{len(checks)+1:03}',name=name,kind=kind,passed=bool(ok),detail=detail,scope=scope,expert_review='PENDING'))
def symbolic(name,expr,scope):
    residual=s.simplify(s.trigsimp(expr))
    record(name,'SYMBOLICALLY_CHECKED',residual==0,str(residual),scope)

ph,th,ps,a,b=s.symbols('phi theta psi alpha beta',real=True)
T1=s.Matrix([[1,0,0],[0,s.cos(ph),s.sin(ph)],[0,-s.sin(ph),s.cos(ph)]])
T2=s.Matrix([[s.cos(th),0,-s.sin(th)],[0,1,0],[s.sin(th),0,s.cos(th)]])
T3=s.Matrix([[s.cos(ps),s.sin(ps),0],[-s.sin(ps),s.cos(ps),0],[0,0,1]])
C=T1*T2*T3
symbolic('Rotación NED-cuerpo: ortogonalidad',sum((v*v for v in C*C.T-s.eye(3))),'Matriz pasiva Euler 3-2-1')
symbolic('Rotación NED-cuerpo: determinante',C.det()-1,'Rotación propia')
Cw=s.Matrix([[s.cos(a)*s.cos(b),-s.cos(a)*s.sin(b),-s.sin(a)],[s.sin(b),s.cos(b),0],[s.sin(a)*s.cos(b),-s.sin(a)*s.sin(b),s.cos(a)]])
symbolic('Rotación viento-cuerpo',sum(v*v for v in Cw*Cw.T-s.eye(3)),'Ejes viento x paralelo a velocidad relativa al aire')
symbolic('Rotación viento-cuerpo: dirección velocidad',sum(v*v for v in Cw*s.Matrix([1,0,0])-s.Matrix([s.cos(a)*s.cos(b),s.sin(b),s.sin(a)*s.cos(b)])),'Definición alpha y beta')
E=s.Matrix([[1,0,-s.sin(th)],[0,s.cos(ph),s.sin(ph)*s.cos(th)],[0,-s.sin(ph),s.cos(ph)*s.cos(th)]])
symbolic('Jacobiano Euler: determinante',E.det()-s.cos(th),'Singularidad en cos(theta)=0')
gvec=C*s.Matrix([0,0,s.Symbol('g')])
symbolic('Gravedad: proyección',sum(v*v for v in gvec-s.Symbol('g')*s.Matrix([-s.sin(th),s.sin(ph)*s.cos(th),s.cos(ph)*s.cos(th)])),'NED z positivo abajo')
p,q,r,Ix,Iy,Iz,J=s.symbols('p q r Ix Iy Iz J',real=True)
pd,qd,rd=s.symbols('pd qd rd')
I=s.Matrix([[Ix,0,-J],[0,Iy,0],[-J,0,Iz]])
om=s.Matrix([p,q,r]); od=s.Matrix([pd,qd,rd])
mom=I*od+om.cross(I*om)
components=s.Matrix([Ix*pd-J*rd+(Iz-Iy)*q*r-J*p*q,
 Iy*qd+(Ix-Iz)*p*r+J*(p*p-r*r),
 Iz*rd-J*pd+(Iy-Ix)*p*q+J*q*r])
symbolic('Newton-Euler: tres términos de inercia cruzada',sum(v*v for v in mom-components),'J=integral x z dm; tensor usa -J')
symbolic('Trabajo giroscópico nulo',om.dot(om.cross(I*om)),'Tensor simétrico constante')

V,A,B,cd,k,cl=s.symbols('V A B CD0 k CL',positive=True)
D=A*V**2+B/V**2; P=V*D
symbolic('Mínimo D: V cuarta=B/A',s.diff(D,V).subs(V,(B/A)**s.Rational(1,4)),'A,B>0 y V>0; mínimo global por límites infinitos')
symbolic('Mínimo P: V cuarta=B/(3A)',s.diff(P,V).subs(V,(B/(3*A))**s.Rational(1,4)),'A,B>0, dominio físico debe excluir pérdida')
polar=cd+k*cl**2
for name,f,opt in [('Máxima L/D',cl/polar,s.sqrt(cd/k)),('Máximo CL^(3/2)/CD',cl**s.Rational(3,2)/polar,s.sqrt(3*cd/k)),('Máximo sqrt(CL)/CD',s.sqrt(cl)/polar,s.sqrt(cd/(3*k)))]:
    symbolic(name,s.diff(f,cl).subs(cl,opt),'Polar parabólica con CD0,k>0; eta y consumos constantes si se aplica a misión')
W,ct,g=s.symbols('W cT g',positive=True)
primitive=s.atan(W*s.sqrt(B/A))/(g*ct*s.sqrt(A*B))
symbolic('Integral jet a TAS y altitud constantes',s.diff(primitive,W)-1/(g*ct*(A+B*W**2)),'W es peso, cT consumo másico por empuje')
mi,mf,rho,S,eta,cp,CL,CD=s.symbols('mi mf rho S eta cP CL CD',positive=True)
K=s.sqrt(2*g/(rho*S*CL)); f=CL/CD
symbolic('Integral alcance jet a CL y rho constantes',s.diff(2*f*K/(g*ct)*s.sqrt(mi),mi)-f*K/(g*ct*s.sqrt(mi)),'V=K sqrt(m), masa decreciente')
symbolic('Integral autonomía hélice a CL y rho constantes',s.diff(-2*eta*f/(g*cp*K*s.sqrt(mi)),mi)-eta*f/(g*cp*K*mi**s.Rational(3,2)),'cP por potencia al eje, eta constante')
ei,AR,kprof=s.symbols('ei AR kprof',positive=True)
eo=1/(1/ei+s.pi*AR*kprof)
symbolic('Oswald frente a eficiencia de envergadura',1/(s.pi*AR*eo)-(1/(s.pi*AR*ei)+kprof),'Sólo si resistencia de perfil adicional es kprof CL²')

u=UnitRegistry()
for name,expression,expected in [
 ('Fuerza aerodinámica',.5*u.kg/u.m**3*(u.m/u.s)**2*u.m**2,u.newton),
 ('Potencia de empuje',u.newton*u.m/u.s,u.watt),
 ('Gasto combustible jet',u.kg/(u.newton*u.s)*u.newton,u.kg/u.s),
 ('Gasto combustible hélice',u.kg/u.joule*u.watt,u.kg/u.s),
 ('Breguet temporal jet',1/(u.m/u.s**2*u.kg/(u.newton*u.s)),u.s),
 ('Breguet alcance hélice',1/(u.m/u.s**2*u.kg/u.joule),u.m),
 ('Aceleración angular',u.newton*u.m/(u.kg*u.m**2),1/u.s**2),
 ('Radio de viraje',(u.m/u.s)**2/(u.m/u.s**2),u.m)]:
    record(name,'DIMENSIONALLY_CHECKED',expression.dimensionality==expected.dimensionality,str(expression.dimensionality),'Unidades SI antes de sustitución numérica')

pol=Polar(28,.024,.046,1.55)
analytic=jet_fixed_v(pol,4800,3900,isa(4500)[2],105,1.65e-5)
for step in [300,120,30]:
    sol=integrate_jet(pol,4800,3900,isa(4500)[2],105,1.65e-5,rtol=1e-8,max_step=step)
    error=abs(sol['time']/analytic['time']-1)
    record(f'Integración masa jet, paso máximo {step}s','NUMERICALLY_CONVERGED',error<2e-7,dict(**sol,relative_error=error),'ODE solve_ivp frente a integral analítica arctan; no valida polar')
for h in [0,10999.999,11000,11000.001,20000]:
    vals=isa(h)
    record(f'Atmósfera h={h}m','ARITHMETIC_REPLAYED',all(x>0 for x in vals),dict(T=vals[0],p=vals[1],rho=vals[2],a=vals[3]),'ISA implementada hasta 20 km; altitud geopotencial')
record('Continuidad ISA en 11 km','ARITHMETIC_REPLAYED',abs(isa(11000-1e-4)[2]/isa(11000+1e-4)[2]-1)<1e-7,'Valores a ambos lados de la tropopausa','No es comparación con observaciones meteorológicas')
rng=np.random.default_rng(20261018)
maxerr=0
for _ in range(200):
    rot=c_body_ned(*rng.uniform(-1,1,3)); vec=rng.normal(size=3)
    maxerr=max(maxerr,np.max(abs(rot.T@(rot@vec)-vec)))
record('Transformaciones aleatorias ida y vuelta','ARITHMETIC_REPLAYED',maxerr<1e-12,maxerr,'200 casos con semilla fija; complemento de prueba simbólica')
inertia=np.array([[8500,0,-620],[0,13000,0],[-620,0,17000]])
om=np.array([.12,-.08,.15]); moment=np.array([950,-500,340])
acc=omega_derivative(om,moment,inertia)
record('Residuo Newton-Euler numérico','ARITHMETIC_REPLAYED',np.linalg.norm(inertia@acc+np.cross(om,inertia@om)-moment)<1e-10,acc.tolist(),'Tensor definido positivo; producto de inercia no nulo')
for clv in [.4,.8,1.1]:
    gd=glide_exact(pol,4700,1.0,clv)
    qdyn=.5*gd['V']**2;L=qdyn*pol.S*clv;D=qdyn*pol.S*pol.cd(clv)
    residual=max(abs(L-4700*G*cos(gd['gamma'])),abs(D+4700*G*sin(gd['gamma'])))
    record(f'Equilibrio planeo CL={clv}','ARITHMETIC_REPLAYED',residual<1e-9,dict(**gd,residual_N=residual),'Descenso estacionario exacto, sin empuje')
lo=pol.stall(4700,1.0)*1.02; hi=200
opt=minimize_scalar(lambda v:pol.drag(v,4700,1.0),bounds=(lo,hi),method='bounded')
vd=pol.speed(4700,1.0,pol.cl_ld())
record('Mínimo resistencia: optimizador independiente','ARITHMETIC_REPLAYED',abs(opt.x/vd-1)<1e-6,dict(optimizer=opt.x,formula=vd),'Mismo modelo, algoritmos distintos')
bank=math.radians(35); tr=turn(90,bank)
record('Viraje: balance centrípeto','ARITHMETIC_REPLAYED',abs(tr['n']*G*sin(bank)-90**2/tr['radius'])<1e-12,tr,'Nivelado coordinado, viento nulo')
takepol=Polar(18,.035,.055,1.9)
roll=ground_roll(takepol,1500,1.225,32,lambda v:5000,.03,.65)
# Euler temporal independiente con paso decreciente frente a cuadratura en velocidad.
for dt in [.02,.01,.005]:
    v=x=t=0.0
    while v<32:
        qdyn=.5*1.225*v*v; lift=qdyn*18*.65; drag=qdyn*18*takepol.cd(.65)
        ac=(5000-drag-.03*(1500*G-lift))/1500
        dtt=min(dt,(32-v)/ac)
        x+=v*dtt+.5*ac*dtt*dtt;v+=ac*dtt;t+=dtt
    record(f'Rodadura: cuadratura frente a marcha temporal dt={dt}','NUMERICALLY_CONVERGED',abs(x/roll['distance']-1)<2e-4,dict(distance=x,reference=roll['distance'],time=t),'Modelo de rodadura; sin rotación ni distancia sobre obstáculo')
report=dict(checks=checks,total=len(checks),passed=sum(c['passed'] for c in checks),failed=sum(not c['passed'] for c in checks),
 vocabulary='Estados de este registro externo; no son estados añadidos a Studium.',
 limitations=['Revisión experta pendiente.','La coherencia dimensional no establece la validez del modelo.','Convergencia de estas ODE no implica convergencia de todos los ejemplos JSBSim.'])
(ROOT/'reports/model-checks.json').write_text(json.dumps(report,ensure_ascii=False,indent=2))
print(json.dumps(dict(total=report['total'],passed=report['passed'],failed=report['failed'])))
if report['failed']: sys.exit(1)
