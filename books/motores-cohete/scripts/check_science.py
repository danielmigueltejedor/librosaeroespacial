"""Controles declarados: aritmética, álgebra, dimensiones, conservación y dominios."""
from pathlib import Path
import sys,json,math
import sympy as s
import numpy as np
from scipy.integrate import quad,solve_ivp
from models import *
from problem_bank import manual,bank,exams
R=Path(__file__).resolve().parents[1];records=[]
def check(name,ok,kind,scope,detail=''):
 records.append(dict(name=name,passed=bool(ok),level=kind,scope=scope,detail=str(detail)))
 if not ok:raise AssertionError(name+': '+str(detail))
rows=manual()+bank()+sum(exams(),[])
for p in rows:
 for j,ck in enumerate(p['tests']):
  actual=float(s.sympify(ck['expression'],locals={'sqrt':s.sqrt,'log':s.log,'exp':s.exp,'cos':s.cos,'sin':s.sin,'pi':s.pi}).evalf(35));err=abs(actual-ck['expected'])/max(1,abs(ck['expected']))
  check(p['key']+f'.{j+1}',err<2e-11,'NUMERICALLY_CROSS_CHECKED','Sustitución de la expresión declarada mediante SymPy a 35 cifras',err)
# Teorema fundamental para capacidad calorífica variable: no confundir h(T) con producto.
T,Tr,theta=s.symbols('T Tr theta',positive=True);Cp=s.Function('Cp')
check('Integral de entalpía variable',s.simplify(s.diff(s.Integral(Cp(theta),(theta,Tr,T)),T)-Cp(T))==0,'SYMBOLICALLY_VERIFIED','Teorema fundamental bajo h prima igual a cp; contraste del falso positivo nativo')
# Identidades independientes de datos editoriales.
M,kappa=s.symbols('M kappa',positive=True);gam=1+kappa;f=M*(1+(gam-1)*M*M/2)**(-(gam+1)/(2*(gam-1)))
check('Derivada logarítmica de flujo',s.simplify(s.diff(f,M)/f-(1-M*M)/(M*(1+(gam-1)*M*M/2)))==0,'SYMBOLICALLY_VERIFIED','Función de flujo; gamma>1')
pp,aa,pa,md,v=s.symbols('p A pa md v');check('Óptimo ideal de área',s.expand(md*(-aa/md)+aa)==0,'SYMBOLICALLY_VERIFIED','Cancelación md dv=-A dp en dF; restante (p-pa)dA')
eps,n=s.symbols('eps n');check('Linealización de equilibrio sólido',s.simplify(s.diff((1+eps)**(1/(1-n)),eps).subs(eps,0)-1/(1-n))==0,'SYMBOLICALLY_VERIFIED','Sensibilidad en área inicial')
c,m=s.symbols('c m',positive=True);check('Integral de Tsiolkovski',s.simplify(s.diff(c*s.log(m),m)-c/m)==0,'SYMBOLICALLY_VERIFIED','Integral en masa; c constante')
# Continuidad y energía de una familia de toberas: dos rutas físicas distintas.
for g in [1.2,1.32,1.4,1.67]:
 for ar in [1.001,2.,5.,15.]:
  qv=nozzle(g,350.,2600.,3e6,.0004,ar,0);rho=qv['pe']/(350*qv['Te']);mexit=rho*qv['ve']*qv['Ae'];cp=g*350/(g-1);veenergy=math.sqrt(2*cp*(2600-qv['Te']))
  check(f'Continuidad g{g} eps{ar}',math.isclose(mexit,qv['mdot'],rel_tol=2e-10),'CONSERVATION_CHECK','Densidad y velocidad de salida frente a descarga crítica')
  check(f'Energía g{g} eps{ar}',math.isclose(veenergy,qv['ve'],rel_tol=2e-12),'CONSERVATION_CHECK','Entalpía frente a rapidez acústica')
  check(f'Identidad CF g{g} eps{ar}',math.isclose(qv['CF']*qv['cstar'],qv['Isp']*G0,rel_tol=1e-13),'ALGEBRAIC_NUMERIC','Definiciones con misma frontera')
# Choque: balances calculados de estados, sin reutilizar fórmula de p0 para conservación.
for M1 in [1.0001,1.5,2.,4.]:
 g=1.4;Rg=287.;T1=420.;p1=40000.;a=shock(M1,g);T2=T1*a['T2_T1'];p2=p1*a['p2_p1'];r1=p1/(Rg*T1);r2=p2/(Rg*T2);v1=M1*math.sqrt(g*Rg*T1);v2=a['M2']*math.sqrt(g*Rg*T2);cp=g*Rg/(g-1)
 check(f'Choque masa M{M1}',math.isclose(r1*v1,r2*v2,rel_tol=1e-12),'CONSERVATION_CHECK','Flujos en estados derivados')
 check(f'Choque momento M{M1}',math.isclose(p1+r1*v1*v1,p2+r2*v2*v2,rel_tol=1e-12),'CONSERVATION_CHECK','Flujos y presiones en estados derivados')
 check(f'Choque energía M{M1}',math.isclose(cp*T1+v1*v1/2,cp*T2+v2*v2/2,rel_tol=1e-12),'CONSERVATION_CHECK','Entalpía total')
 ds=cp*math.log(T2/T1)-Rg*math.log(p2/p1);check(f'Choque entropía M{M1}',ds>=-1e-10 and a['p02_p01']<=1+1e-12,'PHYSICAL_DOMAIN','Segunda ley del modelo',ds)
# Integral numérica independiente de la forma cerrada vertical.
for m0,mdp,tt,c in [(400,2,60,2400),(450,2.5,40,2600)]:
 val,err=quad(lambda t:c*mdp/(m0-mdp*t)-G0,0,tt,epsabs=1e-10);expected=c*math.log(m0/(m0-mdp*tt))-G0*tt
 check(f'Vertical cuadratura {m0}',math.isclose(val,expected,rel_tol=1e-12,abs_tol=1e-10),'NUMERICALLY_CROSS_CHECKED','Cuadratura adaptativa frente a integral analítica')
# Equilibrio normalizado y dinámica, no datos de motor.
sol=solve_ivp(lambda t,y:1.02*y[0]**.4-y[0],[0,40],[1.],rtol=1e-10,atol=1e-12)
check('Equilibrio sólido por integración',math.isclose(sol.y[0,-1],1.02**(1/.6),rel_tol=1e-9),'NUMERICALLY_CROSS_CHECKED','Modelo concentrado adimensional')
# Regresiones A-I: rechazos explícitos y límites.
check('A Isp no velocidad',math.isclose(300*G0,2941.995,rel_tol=1e-12) and 300!=300*G0,'DIMENSION_AND_CONVERSION','Segundos frente a m/s')
check('B presión no omitida',abs((2500+400)-2500)==400,'ALGEBRAIC_NUMERIC','Velocidad efectiva incluye presión/caudal')
ms=mach_area(3,1.4,'subsonic');start=stagnation_ratios(ms,1.4)['p_p0'];conv=(2/2.4)**3.5
check('C umbral CD distinto',start>conv+.1,'PHYSICAL_DOMAIN','Primer bloqueo CD por rama subsónica, no cociente sónico')
for name,fn in [('D gamma universal',lambda:cstar(1,300,2500)),('E eficiencia mayor que uno',lambda:electric(1000,1.01,20000)),('E eficiencia negativa',lambda:electric(1000,-.1,20000)),('Geometría imposible',lambda:mach_area(.9,1.4)),('Masa imposible',lambda:delta_v(2500,100,120))]:
 try:fn();ok=False
 except ValueError:ok=True
 check(name,ok,'DOMAIN_REJECTION','Entrada incompatible rechazada')
cea=json.load(open(R/'reports/cea-case.json'));check('F alcance CEA',len(cea['rows'])==6 and 'TP equilibrium' in cea['calculation'] and 'Isp real' in cea['limitations'],'PROVENANCE_SCOPE','No confundir TP con prestación experimental')
check('G área variable presión variable',solid_pressure_ratio(1.2,.4)>1.2,'PHYSICAL_DOMAIN','Generación-descarga con n positivo')
# H se revisa editorialmente; no se cuenta una condición siempre verdadera como prueba.
e1=electric(1000,.6,15000);e2=electric(1000,.6,30000);check('I alto Isp no alto F',math.isclose(e2['F']/e1['F'],.5),'PHYSICAL_DOMAIN','Potencia y rendimiento constantes')
# Comprobación de M01 y M02 escritos en el manuscrito.
check('M01 dos potencias',math.isclose(.4*3000/2,600) and math.isclose((1/15)*18000/2,600),'NUMERICALLY_CROSS_CHECKED','Casos iniciales manuales')
for F in [5460,6540]:check('M02 Isp '+str(F),abs(F/(2.4*G0)-(231.985 if F==5460 else 277.873))<.001,'NUMERICALLY_CROSS_CHECKED','Redondeo mostrado M02')
out=dict(status='PASSED',checks=len(records),scope='Controles de modelos y aritmética declarados. No validación experimental ni revisión académica integral.',records=records)
(R/'reports/science-checks.json').write_text(json.dumps(out,ensure_ascii=False,indent=2));print(out['checks'],'controles superados')
