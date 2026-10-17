from pathlib import Path
import math,json,sys
import sympy as s
import numpy as np
from scipy.integrate import quad,solve_ivp
from scipy.optimize import minimize_scalar,brentq
from pint import UnitRegistry
from physics import *
RDIR=Path(__file__).resolve().parents[1]/'reports';checks=[]
def check(key,condition,method,scope,evidence=None):
 checks.append(dict(key=key,status='VERIFICADO' if bool(condition) else 'ERROR DETECTADO',method=method,scope=scope,evidence=evidence));assert condition,key
def eq(key,a,b,scope):check(key,s.simplify(a-b)==0,'SymPy: residuo simbólico',scope,str(s.simplify(a-b)))
H,L,Tb,pb,g,Rg=s.symbols('H L Tb pb g R',positive=True);T=Tb+L*H;p=pb*(T/Tb)**(-g/(Rg*L))
eq('ISA-gradiente-hidrostatica',s.diff(p,H),-g*p/(Rg*T),'Gradiente constante, gas ideal, H geopotencial, T>0')
eq('ISA-limite-isotermo',s.limit(p,L,0),pb*s.exp(-g*H/(Rg*Tb)),'Límite L→0 a H,Tb positivos')
V,A,B=s.symbols('V A B',positive=True);D=A*V**2+B/V**2
Vd=(B/A)**s.Rational(1,4);Vp=(B/(3*A))**s.Rational(1,4)
eq('D-min-derivada',s.diff(D,V).subs(V,Vd),0,'Polar parabólica, peso/rho constantes y V>0')
eq('P-min-derivada',s.diff(D*V,V).subs(V,Vp),0,'Potencia aerodinámica necesaria, no potencia del eje')
C,C0,K,ei,AR,kp=s.symbols('C C0 K ei AR kp',positive=True)
eq('eficiencia-optimo',s.diff(C/(C0+K*C**2),C).subs(C,s.sqrt(C0/K)),0,'CL positivo, CD0,K constantes')
res=s.simplify((C**2/(s.pi*ei*AR)-C0).subs(C,s.sqrt(C0/(1/(s.pi*ei*AR)+kp))))
check('Oswald-no-es-ei',res!=0,'SymPy: contraejemplo algebraico','No igualar resistencia inducida y CD0 con perfil cuadrático no nulo',str(res))
check('Oswald-caso-restringido',s.simplify(res.subs(kp,0))==0,'SymPy','El balance aislado sólo se recupera con kp=0')
M,ga=s.symbols('M gamma',positive=True);ratio=(1+(ga-1)*M*M/2)**(ga/(ga-1))
eq('Pitot-incompresible-limite',s.limit((ratio-1)/M**2,M,0),ga/2,'Gas caloríficamente perfecto, isentrópico, M→0')
m0,mf,c=s.symbols('m0 mf c',positive=True);m=s.symbols('m',positive=True)
eq('cohete-integral',s.integrate(-c/m,(m,m0,mf)),c*s.log(m0/mf),'Empuje ideal, c constante, sin pérdidas externas')
r,mu=s.symbols('r mu',positive=True);v=s.sqrt(mu/r)
eq('orbita-energia',v*v/2-mu/r,-mu/(2*r),'Órbita circular, dos cuerpos, energía específica')
u=UnitRegistry()
dim=[('rho','p/(R*T)',{'p':'Pa','R':'J/(kg*K)','T':'K'},'kg/m^3'),('sound','(gamma*R*T)**0.5',{'gamma':'','R':'J/(kg*K)','T':'K'},'m/s'),('Re','rho*V*c/mu',{'rho':'kg/m^3','V':'m/s','c':'m','mu':'Pa*s'},''),('lift','rho*V**2*S*CL/2',{'rho':'kg/m^3','V':'m/s','S':'m^2','CL':''},'N'),('power','F*V',{'F':'N','V':'m/s'},'W'),('hydraulic','dp*Q',{'dp':'Pa','Q':'m^3/s'},'W'),('electric','I**2*Relec',{'I':'A','Relec':'ohm'},'W'),('rocket','ve+(pe-pa)*Ae/mdot',{'ve':'m/s','pe':'Pa','pa':'Pa','Ae':'m^2','mdot':'kg/s'},'m/s'),('orbit','(mu/r)**0.5',{'mu':'m^3/s^2','r':'m'},'m/s'),('bending','Mb*y/Iz',{'Mb':'N*m','y':'m','Iz':'m^4'},'Pa'),('range-jet','V/cT*LD*logratio',{'V':'m/s','cT':'1/s','LD':'','logratio':''},'m')]
for key,expr,units,target in dim:
 env={k:1*u(v) for k,v in units.items()};a=eval(expr,{'__builtins__':{}},env)
 check('dim-'+key,a.dimensionality==u(target).dimensionality,'Pint: dimensiones','Consistencia dimensional, no validación física',dict(expression=expr,units=units,target=target))
for h in [0,5000,11000,15000,20000]:
 a=isa(h)
 # Numerical integration of hydrostatics, no layer pressure power formula.
 def ode(x,y):return [-G0*y[0]/(R*(288.15-.0065*x if x<=11000 else 216.65))]
 z=solve_ivp(ode,[0,max(h,.00001)],[101325.],rtol=1e-10,atol=1e-7,max_step=25).y[0,-1]
 check(f'ISA-ODE-{h}',abs(z-a['p'])/a['p']<1e-7,'SciPy: integración hidrostática independiente','0–20 km; constante g en H, gas seco',{'formula':a['p'],'ode':z})
for h in BASES[1:-1]:
 a,b=isa(h-1e-4),isa(h+1e-4)
 check(f'ISA-continuidad-{h}',abs(a['p']-b['p'])/a['p']<1e-6 and abs(a['T']-b['T'])<1e-4,'Límites numéricos de tramos','Continuidad de p,T, no derivadas')
check('ISA-tabla-11000',abs(isa(11000)['p']-22632.06)<.1,'Comparación tabla estándar','NASA TM X-74335, capa baja',isa(11000))
for fn,args in [(isa,(-1,)),(isa,(90000,)),(pitot_mach,(90000,100000)),(pitot_mach,(200000,100000)),(drag,(0,1,1,1,1,1))]:
 try:fn(*args);failed=False
 except ValueError:failed=True
 check('dominio-'+fn.__name__+str(args),failed,'Prueba de rechazo','Datos fuera del dominio declarado no deben generar resultados físicos')
for Ma in [.01,.3,.7,.95]:
 pt=90000*(1+.2*Ma*Ma)**3.5
 check('Pitot-inversa-'+str(Ma),abs(pitot_mach(pt,90000)-Ma)<1e-11,'Inversión vs relación directa','Subsónico isentrópico, gamma1.4')
W=42000.;rho=.82;S=22.;cd=.026;k=.052;A=.5*rho*S*cd;B=2*k*W*W/(rho*S);vd=(B/A)**.25
z=minimize_scalar(lambda v:drag(v,rho,W,S,cd,k),bounds=(10,250),method='bounded')
check('Dmin-optimizacion',abs(z.x-vd)<1e-4,'SciPy: búsqueda escalar vs expresión cerrada','Mismo modelo; métodos matemáticos distintos',dict(analytic=vd,numeric=z.x))
roots=drag_limits(1.15*2*math.sqrt(A*B),rho,W,S,cd,k)
check('empuje-dos-raices',len(roots)==2 and all(abs(drag(v,rho,W,S,cd,k)/(1.15*2*math.sqrt(A*B))-1)<1e-12 for v in roots),'Sustitución de ambas raíces','Existen matemáticamente; requieren CLmax y límites Mach por separado')
check('empuje-sin-equilibrio',drag_limits(.99*2*math.sqrt(A*B),rho,W,S,cd,k)==[],'Discriminante negativo','Empuje constante menor que Dmin')
# Mach-cone envelope: travel time of tangent wave vs geometry.
h=1350.;a=330.;Ma=1.8;t=h/a*math.sqrt(1-1/Ma**2);V=Ma*a
te=-h/(a*Ma*math.sqrt(Ma*Ma-1));horizontal=V*te
check('cono-envolvente',abs(math.hypot(horizontal,h)-a*(t-te))<1e-9,'Geometría del frente tangente','Rectilíneo supersónico, a constante, suelo plano')

# Consumption models: units, local optima, and an independent ODE integration.
CL,CD0,KK=s.symbols('CL CD0 KK',positive=True)
for key,power,opt in [('jet-range',s.Rational(1,2),s.sqrt(CD0/(3*KK))),('prop-endurance',s.Rational(3,2),s.sqrt(3*CD0/KK))]:
 eq('optimum-'+key,s.diff(CL**power/(CD0+KK*CL**2),CL).subs(CL,opt),0,'Polar parabólica, consumos/rendimiento constantes; óptimo local instantáneo')
check('dim-consumo-jet',(1*u('kg/(N*s)')*u('m/s^2')).dimensionality==u('1/s').dimensionality,'Pint','Consumo másico por empuje multiplicado por g')
check('dim-range-prop',(1/(u('m/s^2')*u('kg/J'))).dimensionality==u('m').dimensionality,'Pint','Consumo específico por potencia en kg/J')
wi=36000.;wf=33000.;eff=15.;cm=1.6e-5;v=100.;t=eff/(G0*cm)*math.log(wi/wf)
sol=solve_ivp(lambda tt,yy:[-G0*cm*yy[0]/eff,v],[0,t],[wi,0],rtol=1e-11,atol=1e-8)
check('Breguet-ODE-peso',abs(sol.y[0,-1]-wf)<1e-5,'SciPy: balance diferencial independiente','Modelo ideal de crucero cuasiestacionario; no incluye pérdidas de misión',dict(time_s=t,range_m=sol.y[1,-1],final_weight_N=sol.y[0,-1]))
check('Breguet-ODE-distancia',abs(sol.y[1,-1]-v*t)<1e-5,'Integración conjunta de x y W','TAS constante; viento nulo')

try:
 _wrong=(1*u('m/s')+1*u('N'))/(1*u('kg/s'));_rejected=False
except Exception:
 _rejected=True
check('NASA-error-dimensiones-detectado',_rejected,'Pint: rechazo de suma dimensional incompatible','Errata observada en definición web V_eq; se utiliza ve+(pe-pa)Ae/mdot, no (ve+(pe-pa)Ae)/mdot')
(RDIR/'scientific-tests.json').write_text(json.dumps(checks,ensure_ascii=False,indent=2));print(f'{len(checks)} comprobaciones superadas; revisión experta pendiente')
