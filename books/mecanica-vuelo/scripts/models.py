"""Modelos docentes originales. Unidades SI; h es altitud geopotencial.

No son modelos certificados. Polar parabólica, flujo subsónico y vuelo
cuasiestacionario salvo cuando una función declara otra cosa.
"""
from dataclasses import dataclass
from math import sqrt, exp, atan, log, sin, cos, tan
import numpy as np
from scipy.integrate import quad, solve_ivp
from scipy.optimize import minimize_scalar, brentq

G = 9.80665
R = 287.05287
RHO0 = 1.225

def isa(h):
    """ISA 0--20 km geopotenciales: T[K], p[Pa], rho[kg/m3], a[m/s]."""
    if not 0 <= h <= 20000:
        raise ValueError('Dominio ISA implementado: 0 <= h <= 20000 m')
    T0,p0,lapse=288.15,101325.0,-0.0065
    T11=T0+lapse*11000
    p11=p0*(T11/T0)**(-G/(R*lapse))
    if h<=11000:
        T=T0+lapse*h
        p=p0*(T/T0)**(-G/(R*lapse))
    else:
        T=T11
        p=p11*exp(-G*(h-11000)/(R*T))
    rho=p/(R*T)
    return T,p,rho,sqrt(1.4*R*T)

def c_body_ned(phi,theta,psi):
    """Matriz pasiva: componentes NED -> componentes cuerpo, Euler 3-2-1."""
    cph,sph,ct,st,cp,sp=cos(phi),sin(phi),cos(theta),sin(theta),cos(psi),sin(psi)
    return np.array([[ct*cp,ct*sp,-st],
      [sph*st*cp-cph*sp,sph*st*sp+cph*cp,sph*ct],
      [cph*st*cp+sph*sp,cph*st*sp-sph*cp,cph*ct]])

def c_body_wind(alpha,beta):
    """Ejes viento x paralelo velocidad aire, z abajo; Fw=(-D,Y,-L)."""
    ca,sa,cb,sb=cos(alpha),sin(alpha),cos(beta),sin(beta)
    return np.array([[ca*cb,-ca*sb,-sa],[sb,cb,0],[sa*cb,-sa*sb,ca]])

def body_derivative(velocity,omega,force,mass):
    return np.array(force)/mass-np.cross(omega,velocity)

def omega_derivative(omega,moment,inertia):
    omega=np.array(omega); inertia=np.array(inertia)
    return np.linalg.solve(inertia,np.array(moment)-np.cross(omega,inertia@omega))

@dataclass(frozen=True)
class Polar:
    S: float
    cd0: float
    k: float
    clmax: float=1.5

    def cd(self,cl): return self.cd0+self.k*cl*cl
    def ld(self,cl): return cl/self.cd(cl)
    def cl_ld(self): return sqrt(self.cd0/self.k)
    def cl_minpower(self): return sqrt(3*self.cd0/self.k)
    def cl_jet_range(self): return sqrt(self.cd0/(3*self.k))
    def speed(self,m,rho,cl,n=1): return sqrt(2*n*m*G/(rho*self.S*cl))
    def drag(self,V,m,rho,n=1):
        q=.5*rho*V*V; cl=n*m*G/(q*self.S)
        return q*self.S*self.cd(cl)
    def power(self,V,m,rho,n=1): return V*self.drag(V,m,rho,n)
    def stall(self,m,rho,n=1): return self.speed(m,rho,self.clmax,n)

def glide_exact(polar,m,rho,cl):
    """Descenso rectilíneo estacionario: gamma < 0, L=W cos(gamma)."""
    gamma=-atan(polar.cd(cl)/cl)
    V=sqrt(2*m*G*cos(gamma)/(rho*polar.S*cl))
    return dict(gamma=gamma,V=V,sink=-V*sin(gamma),horizontal=V*cos(gamma))

def glide_integral(polar,m,hi,hf,cl,wind=0):
    """Viento horizontal uniforme, positivo de cola; sin movimiento vertical aire."""
    def at(h): return glide_exact(polar,m,isa(h)[2],cl)
    duration=quad(lambda h:1/at(h)['sink'],hf,hi,epsabs=1e-7)[0]
    air_range=(hi-hf)*polar.ld(cl)
    return dict(time=duration,air_range=air_range,ground_range=air_range+wind*duration)

def jet_fixed_v(polar,mi,mf,rho,V,cT):
    """cT[kg/(N s)]. Altitud y TAS constantes. Resultados exactos del modelo polar."""
    A=.5*rho*V*V*polar.S*polar.cd0
    B=2*polar.k/(rho*V*V*polar.S)  # D=A+B W^2
    Wi,Wf=mi*G,mf*G
    E=(atan(Wi*sqrt(B/A))-atan(Wf*sqrt(B/A)))/(G*cT*sqrt(A*B))
    return dict(time=E,range=V*E)

def jet_fixed_cl(polar,mi,mf,rho,cl,cT):
    """Altitud y CL constantes; V decrece como sqrt(m)."""
    f=polar.ld(cl)
    E=f/(G*cT)*log(mi/mf)
    distance=2*f/(G*cT)*sqrt(2*G/(rho*polar.S*cl))*(sqrt(mi)-sqrt(mf))
    return dict(time=E,range=distance,Vi=polar.speed(mi,rho,cl),Vf=polar.speed(mf,rho,cl))

def prop_fixed_cl(polar,mi,mf,rho,cl,cP,eta):
    """cP[kg/J] referido al eje; rho, CL, eta y cP constantes."""
    f=polar.ld(cl)
    distance=eta*f/(G*cP)*log(mi/mf)
    K=eta*f/(G*cP)*sqrt(rho*polar.S*cl/(2*G))
    E=2*K*(1/sqrt(mf)-1/sqrt(mi))
    return dict(time=E,range=distance)

def integrate_jet(polar,mi,mf,rho,V,cT,rtol=1e-9,max_step=60):
    def fun(t,y): return [-cT*polar.drag(V,y[0],rho),V]
    def stop(t,y): return y[0]-mf
    stop.terminal=True;stop.direction=-1
    sol=solve_ivp(fun,[0,1e7],[mi,0],events=stop,rtol=rtol,atol=rtol*1e-3,max_step=max_step)
    if len(sol.t_events[0])!=1: raise RuntimeError('No se alcanzó la masa final')
    return dict(time=sol.t_events[0][0],range=sol.y_events[0][0,1],evaluations=sol.nfev)

def turn(V,bank):
    if abs(bank)>=np.pi/2: raise ValueError('Viraje nivelado exige |phi| < pi/2')
    return dict(n=1/cos(bank),radius=V*V/(G*abs(tan(bank))),rate=G*tan(bank)/V)

def ground_roll(polar,m,rho,Vtarget,thrust,mu,cl_ground,wind=0,braking=False):
    """Vground>=0, Vair=Vground+wind (viento de cara positivo).
    Integración distancia en Vground; thrust es una función de Vair.
    En frenado thrust es positivo hacia delante y Vtarget es velocidad inicial.
    """
    def acc(v):
        va=v+wind
        if va<0: raise ValueError('Flujo invertido no modelado')
        q=.5*rho*va*va; L=q*polar.S*cl_ground
        if L>m*G: raise ValueError('Modelo de rodadura excede sustentación de despegue')
        D=q*polar.S*polar.cd(cl_ground)
        return (thrust(va)-D-mu*(m*G-L))/m
    sign=-1 if braking else 1
    if min(sign*acc(v) for v in np.linspace(0,Vtarget,100))<=0:
        raise ValueError('No hay aceleración/frenado monótono en el dominio')
    s=quad(lambda v:sign*v/acc(v),0,Vtarget,epsabs=1e-7)[0]
    t=quad(lambda v:sign/acc(v),0,Vtarget,epsabs=1e-7)[0]
    return dict(distance=s,time=t)
