#!/usr/bin/env python3
"""Pruebas matematicas independientes y acotadas de la auditoria fase 5.

Requiere SymPy. Los PASS no certifican las 158 ecuaciones del libro.
"""
from sympy import symbols, simplify, pi, sin, cos, exp, diff, Rational, log, integrate

passed=[]
def check(name,left,right=0):
    residual=simplify(left-right)
    if residual!=0:
        raise AssertionError((name,str(residual)))
    passed.append(name)
    print('PASS',name)
M,g,ph,V1,V2,P,k,rho,R,mu,h,U,G=symbols('M g ph V1 V2 P k rho R mu h U G',positive=True)
kP=M*g*sin(ph)*(V1+V2)/(V2**3-V1**3)
check('C01 potencia en subida y bajada',V1*(M*g*sin(ph)+kP*V1**2)-V2*(kP*V2**2-M*g*sin(ph)))
V=symbols('V',positive=True)
check('C01 derivada de fuerza neta',diff(P/V-M*g*sin(ph)-k*V**2,V),-P/V**2-2*k*V)
th,A,I,hc,sc=symbols('th A I hc sc',positive=True)
check('C05 presion vertical-plano inclinado',(sc+I/(sc*A))*sin(th),(hc+I*sin(th)**2/(hc*A)).subs(hc,sc*sin(th)))
Y=symbols('Y',real=True)
u=G*Y*(h-Y)/(2*mu)+U*Y/h
check('C06 ecuacion Couette-Poiseuille',mu*diff(u,Y,2),-G)
check('C06 condicion de contorno fija',u.subs(Y,0),0)
check('C06 condicion de contorno movil',u.subs(Y,h),U)
check('C06 caudal Hagen-Poiseuille',integrate(2*pi*Y*(G/(4*mu))*(R**2-Y**2),(Y,0,R)),pi*G*R**4/(8*mu))
x,y,t,nu=symbols('x y t nu',real=True,positive=True)
uvel=sin(x)*cos(y)*exp(-2*nu*t)
vvel=-cos(x)*sin(y)*exp(-2*nu*t)
p=rho*(cos(2*x)+cos(2*y))*exp(-4*nu*t)/4
for vel,coord in [(uvel,x),(vvel,y)]:
    conv=uvel*diff(vel,x)+vvel*diff(vel,y)
    residual=rho*(diff(vel,t)+conv)+diff(p,coord)-rho*nu*(diff(vel,x,2)+diff(vel,y,2))
    check('C14 Taylor-Green Navier-Stokes '+str(coord),residual)
check('C14 Taylor-Green continuidad',diff(uvel,x)+diff(vvel,y))
d1,d2,nu1,nu2,vc1=symbols('d1 d2 nu1 nu2 vc1',positive=True)
vc2=vc1*(nu2/nu1)*(d1/d2)
check('C10 Reynolds semejante',vc1*d1/nu1,vc2*d2/nu2)
a=symbols('a',real=True)
cp=4*a*(1-a)**2
check('C09 Betz 16/27',cp.subs(a,Rational(1,3)),Rational(16,27))
check('C09 Betz punto estacionario',diff(cp,a).subs(a,Rational(1,3)))
nuv,H=symbols('nuv H',positive=True)
t99=H**2*log(200)/(pi**2*nuv)
check('M07 Couette primer modo 99%',1-2*exp(-pi**2*nuv*t99/H**2),Rational(99,100))
print(f'\n{len(passed)}/{len(passed)} PRUEBAS SIMBOLICAS SUPERADAS')
print('No se ha ejecutado Mathematica ni se ha validado cientificamente el resto del libro.')
