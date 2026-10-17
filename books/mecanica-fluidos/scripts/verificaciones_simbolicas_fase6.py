#!/usr/bin/env python3
"""Comprobaciones independendientes seleccionadas sobre formulas de Fluidos fase 6.

Solo se da por verificada la identidad matematica expresamente ensayada,
NO la validez fisica universal de un modelo ni todo el contenido del libro.
"""
from __future__ import annotations
import argparse
import json
from pathlib import Path
import sympy as sp

checks: list[dict[str, object]] = []

def test(name: str, labels: list[str], residual: sp.Expr, *, assumptions: str) -> None:
    r = sp.simplify(sp.trigsimp(residual))
    ok = r == 0
    checks.append({'name': name, 'equations': labels, 'status': 'PASS' if ok else 'FAIL', 'assumptions': assumptions, 'residual': str(r)})
    if not ok:
        raise AssertionError(f'{name}: residual {r}')

x,y,z,t,r,R,h,mu,nu,G,U = sp.symbols('x y z t r R h mu nu G U', positive=True, real=True)
rho,g,A,Delta,omega = sp.symbols('rho g A Delta omega', positive=True, real=True)

# 01/02. Polar y separacion rigurosa de terminos cuadraticos.
CD0, ei, AR, cd2, CL = sp.symbols('CD0 ei AR cd2 CL', positive=True, real=True)
k_ind = 1/(sp.pi*ei*AR); K = k_ind + cd2
clopt = sp.sqrt(CD0/K)
LD=CL/(CD0+K*CL**2)
test('C07 condicion de estacionariedad L/D', ['eq:c07-polar'], sp.diff(LD,CL).subs(CL,clopt),assumptions='CD0>0, K>0, CL>0')
test('C07 maximo L/D', ['eq:c07-polar'], LD.subs(CL,clopt)-1/(2*sp.sqrt(K*CD0)),assumptions='polar parabolica valida; CD0,K>0')
test('C07 K CL^2 es termino cuadratico total, no siempre inducido', ['eq:c07-polar','eq:c07-inducida'],
     (K*clopt**2-k_ind*clopt**2)-cd2*CD0/K,
     assumptions='K=1/(pi ei AR)+cd2, cd2>0')
# La diferencia NO debe ser nula si hay componente de perfil dependiente de CL.
assert sp.simplify((CD0-k_ind*clopt**2).subs({CD0:sp.Rational(18,1000),ei:sp.Rational(9,10),AR:sp.Rational(95,10),cd2:sp.Rational(4,1000)}))>0

# 04. Fuerza y resistencia en pendiente con dos condiciones constantes.
M,theta1,theta2,V1,V2,fric,k = sp.symbols('M theta1 theta2 V1 V2 fric k', real=True,nonzero=True)
kk=M*g*sp.sin(theta2-theta1)/(V2**2*sp.cos(theta1)-V1**2*sp.cos(theta2))
fr=(sp.sin(theta1)-kk*V1**2/(M*g))/sp.cos(theta1)
test('C07 esquiador elimina rozamiento seco', ['eq:c07-dos-pendientes'],
     M*g*sp.sin(theta2)-fr*M*g*sp.cos(theta2)-kk*V2**2,
     assumptions='cos(theta1) distinto de 0; denominador distinto de 0')

# 05. coast-down deceleraciones positivas.
a1,a2 = sp.symbols('a1 a2', real=True)
kk2 = M*(a1-a2)/(V1**2-V2**2); roll=M*a1-kk2*V1**2
test('C07 coastdown dos puntos', ['eq:c07-deceleracion'], roll+kk2*V2**2-M*a2, assumptions='deceleracion positiva; V1^2 != V2^2')

# 06-09. Couette, Poiseuille, caudal y esfuerzo.
u=G*y*(h-y)/(2*mu)+U*y/h
test('C06 balance Couette-Poiseuille', ['eq:c06-couette'], mu*sp.diff(u,y,2)+G,assumptions='mu>0; placas en y=0,h')
test('C06 condicion fija', ['eq:c06-couette'],u.subs(y,0),assumptions='u(0)=0')
test('C06 condicion movil', ['eq:c06-couette'],u.subs(y,h)-U,assumptions='u(h)=U')
test('C06 caudal general Couette-Poiseuille', ['eq:c06-couette','eq:c06-caudal-plano'],sp.integrate(u,(y,0,h))-(G*h**3/(12*mu)+U*h/2),assumptions='q escrito en el libro para U=0')

# 10. Hagen Poiseuille.
Q=sp.integrate((G/(4*mu))*(R**2-r**2)*2*sp.pi*r,(r,0,R))
test('C06 caudal Hagen-Poiseuille', ['eq:c06-hagen','eq:c06-perfil-tubo'],Q-sp.pi*G*R**4/(8*mu),assumptions='flujo laminar desarrollado')

# 11. Mecanica oscilador tubo U.
omega0=sp.sqrt(2*g/h)
test('C08 periodo de columna en U', ['eq:c08-tubo-u'], omega0**2-2*g/h,assumptions='L total columna=h, no viscosidad')

# 12/13. Rendimiento propulsivo y limite indeterminado.
ve,v0,mdot=sp.symbols('ve v0 mdot', positive=True)
eta_original=(mdot*(ve-v0)*v0)/(sp.Rational(1,2)*mdot*(ve**2-v0**2))
test('C09 rendimiento propulsivo cuando ve distinto de v0', ['eq:c09-rendimiento'],eta_original-2/(1+ve/v0),assumptions='ve>v0>0; combustible y presion adaptada')
test('C09 limite rendimiento propulsivo', ['eq:c09-rendimiento'],sp.limit(eta_original,ve,v0,dir='+')-1,assumptions='limite a lo largo de ve>v0')

# 14. Buckingham.
a,b,c=sp.symbols('a b c')
solution=sp.solve([1+a,1-3*a+b+c,-2-b],(a,b,c),dict=True)[0]
test('C10 exponentes Buckingham fuerza esfera', ['eq:c10-exponentes'],solution[a]+1, assumptions='dimensiones M L T')
assert solution[b]==-2 and solution[c]==-2

# 15. Campo de punto de remanso: traza no estacionaria.
u0,acc,tau=sp.symbols('u0 acc tau', positive=True)
xcur=u0*(t-tau); ycur=acc*(t**2-tau**2)/2
streak=acc/2*(2*t*xcur/u0-(xcur/u0)**2)
test('C04 formula traza inyeccion continua', ['eq:c04-traza'],ycur-streak,assumptions='u0>0, 0<=tau<=t')

# 16. Atmosfera isoterma.
Rair,T,p0=sp.symbols('Rair T p0', positive=True)
pz=p0*sp.exp(-g*z/(Rair*T))
test('C05 equilibrio hidrostatico isoterma', ['eq:c05-isoterma'],sp.diff(pz,z)+pz*g/(Rair*T),assumptions='T,Rair,g constantes')

# 17. Vortice libre y circulacion.
Gamma=sp.symbols('Gamma',real=True)
ut=Gamma/(2*sp.pi*r)
test('C11 vorticidad fuera del eje', ['eq:c11-torbellino'],sp.diff(r*ut,r)/r,assumptions='r>0; singularidad axial excluida')

# 18. Pelicula descendente estacionaria.
hf=sp.symbols('hf',positive=True)
ang=sp.symbols('ang',real=True)
uf=g*sp.sin(ang)/nu*(hf*y-y**2/2)
test('C15 pelicula solucion EDP', ['eq:c15-pelicula'], nu*sp.diff(uf,y,2)+g*sp.sin(ang),assumptions='laminar, estacionaria, sin gradiente presion x')
test('C15 pelicula caudal', ['eq:c15-pelicula'],sp.integrate(uf,(y,0,hf))-g*sp.sin(ang)*hf**3/(3*nu),assumptions='sin esfuerzos tangenciales en superficie')

# 20. Vaciado tanque: restringido a t <= tv.
h0,Atank,ap=sp.symbols('h0 Atank ap',positive=True)
expr=(sp.sqrt(h0)-ap/Atank*sp.sqrt(g/2)*t)**2
tv=Atank/ap*sp.sqrt(2*h0/g)
test('M04 vaciado deposito ecuacion diferencial para 0<t<tv', ['eq:m04-vaciado'],
     sp.diff(expr,t)+ap/Atank*sp.sqrt(2*g)*(sp.sqrt(h0)-ap/Atank*sp.sqrt(g/2)*t),
     assumptions='solo t<tv, raiz positiva; extrapolar despues de tv es incorrecto')
test('M04 vaciado deposito tiempo final', ['eq:m04-vaciado'],expr.subs(t,tv),assumptions='h(tv)=0')

# 22. Venturi e inversion del caudal.
beta,dp,diam,rhol=sp.symbols('beta dp diam rhol',positive=True)
A2=sp.pi*(beta*diam)**2/4
Qv=A2*sp.sqrt(2*dp/(rhol*(1-beta**4)))
test('M04 Venturi inversion delta p', ['eq:m04-venturi'],
     sp.simplify((Qv/A2)**2-(2*dp/(rhol*(1-beta**4)))),assumptions='ideal, incompresible, sin perdidas; 0<beta<1')

# 23. Solucion serie del arranque de Couette. Un modo individual satisface ecuacion difusion.
n=sp.symbols('n', integer=True,positive=True)
mode=sp.exp(-n*n*sp.pi**2*nu*t/h**2)*sp.sin(n*sp.pi*y/h)/n
test('M07 cada modo satisface difusion', ['eq:m07-serie','eq:m07-arranque'],sp.diff(mode,t)-nu*sp.diff(mode,y,2),assumptions='n entero positivo, t>0')

# 24. Geostrofia: f k x u=-grad(p)/rho.
f,px,py=sp.symbols('f px py',real=True,nonzero=True)
ug=-py/(rho*f);vg=px/(rho*f)
test('C16 balance geostrofico x', ['eq:c16-geostrofico'], -f*vg+px/rho,assumptions='latitud con f != 0; corriente estacionaria balanceada')
test('C16 balance geostrofico y', ['eq:c16-geostrofico'], f*ug+py/rho,assumptions='latitud con f != 0; corriente estacionaria balanceada')

if __name__=='__main__':
    arg=argparse.ArgumentParser()
    arg.add_argument('--json',type=Path)
    args=arg.parse_args()
    for check in checks:
        print(f"{check['status']} {check['name']} | {', '.join(check['equations'])}")
    print(f'\n{len(checks)}/{len(checks)} IDENTIDADES Y RELACIONES CONCRETAS COMPROBADAS')
    print('No certifica los 158 enunciados ni los resultados de Mathematica.')
    if args.json:
        args.json.parent.mkdir(parents=True,exist_ok=True)
        args.json.write_text(json.dumps({'checks':checks,'scope':'selected_exact_identities_not_general_scientific_certification'},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
