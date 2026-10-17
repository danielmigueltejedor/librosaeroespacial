"""Modelos docentes SI: gas caloríficamente perfecto y balances declarados."""
import math
from scipy.optimize import brentq
G0=9.80665; RU=8314.46261815324

def gas(gamma,R,T):
 if not gamma>1 or min(R,T)<=0:raise ValueError('Se requiere gamma>1, R>0, T>0')

def area_mach(M,gamma):
 if M<=0 or gamma<=1:raise ValueError('Mach positivo y gamma>1')
 return (2/(gamma+1)*(1+(gamma-1)/2*M*M))**((gamma+1)/(2*(gamma-1)))/M

def mach_area(eps,gamma,branch='supersonic'):
 if eps<1 or gamma<=1:raise ValueError('A/A* >= 1 y gamma>1')
 if eps==1:return 1.
 f=lambda M:area_mach(M,gamma)-eps
 if branch=='subsonic':return brentq(f,1e-10,1-1e-9)
 if branch!='supersonic':raise ValueError('Rama no reconocida')
 hi=4.
 while f(hi)<0 and hi<1000:hi*=2
 return brentq(f,1+1e-9,hi)

def stagnation_ratios(M,gamma):
 if M<0 or gamma<=1:raise ValueError('Dominio de Mach o gamma')
 tau=1/(1+(gamma-1)*M*M/2)
 return dict(T_T0=tau,p_p0=tau**(gamma/(gamma-1)),rho_rho0=tau**(1/(gamma-1)))

def cstar(gamma,R,Tc):
 gas(gamma,R,Tc)
 return math.sqrt(R*Tc/gamma)*((gamma+1)/2)**((gamma+1)/(2*(gamma-1)))

def nozzle(gamma,R,Tc,pc,At,eps,pa=0.):
 gas(gamma,R,Tc)
 if min(pc,At)<=0 or pa<0:raise ValueError('Presión y área positivas; ambiente no negativo')
 M=mach_area(eps,gamma);r=stagnation_ratios(M,gamma);Te=Tc*r['T_T0'];pe=pc*r['p_p0'];ve=M*math.sqrt(gamma*R*Te);cs=cstar(gamma,R,Tc);md=pc*At/cs;F=md*ve+(pe-pa)*At*eps;cf=F/(pc*At)
 return dict(Me=M,Te=Te,pe=pe,ve=ve,cstar=cs,mdot=md,F=F,CF=cf,Isp=F/(md*G0),ceff=F/md,Ae=At*eps,ideal_fully_supersonic=True)

def shock(M,gamma):
 if M<1 or gamma<=1:raise ValueError('Choque normal requiere M>=1, gamma>1')
 m2=math.sqrt((1+(gamma-1)*M*M/2)/(gamma*M*M-(gamma-1)/2));pr=(2*gamma*M*M-(gamma-1))/(gamma+1);rr=(gamma+1)*M*M/(2+(gamma-1)*M*M);p0=pr*((1+(gamma-1)*m2*m2/2)/(1+(gamma-1)*M*M/2))**(gamma/(gamma-1))
 return dict(M2=m2,p2_p1=pr,rho2_rho1=rr,T2_T1=pr/rr,p02_p01=p0)

def solid_pressure_ratio(area_ratio,n):
 if area_ratio<=0 or not 0<=n<1:raise ValueError('Modelo cuasiestacionario: área positiva y 0<=n<1')
 return area_ratio**(1/(1-n))

def electric(P,eta,ve):
 if P<=0 or ve<=0 or not 0<eta<=1:raise ValueError('P, ve positivos; 0<eta<=1')
 F=2*eta*P/ve;md=F/ve
 return dict(F=F,mdot=md,Isp=ve/G0,Pjet=eta*P)

def delta_v(c,m0,mf):
 if c<=0 or not 0<mf<m0:raise ValueError('c>0 y 0<mf<m0')
 return c*math.log(m0/mf)
