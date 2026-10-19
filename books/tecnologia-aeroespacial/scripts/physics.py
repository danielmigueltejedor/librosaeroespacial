"""Modelos docentes explícitos; SI y altitud geopotencial. No biblioteca operativa."""
import math
G0=9.80665; R=287.05287; GAMMA=1.4; RE=6356766.0
BASES=[0.,11000.,20000.,32000.,47000.,51000.,71000.,84852.]
LAPSE=[-.0065,0.,.001,.0028,0.,-.0028,-.002]
def isa(H):
 if not math.isfinite(H) or not 0<=H<=BASES[-1]:raise ValueError('ISA: H geopotencial debe estar en [0,84852] m')
 T=288.15;p=101325.
 for i,L in enumerate(LAPSE):
  dh=min(H,BASES[i+1])-BASES[i]
  if dh<0:break
  Tb=T;T=Tb+L*dh
  p*=math.exp(-G0*dh/(R*Tb)) if L==0 else (T/Tb)**(-G0/(R*L))
  if H<=BASES[i+1]:break
 return {'H':H,'T':T,'p':p,'rho':p/(R*T),'a':math.sqrt(GAMMA*R*T),'mu':1.716e-5*(T/273.15)**1.5*(273.15+110.4)/(T+110.4)}
def geopotential(z):
 if z<0:raise ValueError('z negativa fuera del alcance docente')
 return RE*z/(RE+z)
def pitot_mach(pt,p):
 if not 0<p<=pt:raise ValueError('Se requiere 0 < p <= pt')
 M=math.sqrt(2/(GAMMA-1)*((pt/p)**((GAMMA-1)/GAMMA)-1))
 if M>=1:raise ValueError('Inversión subsónica fuera de dominio; usar choque normal y Pitot Rayleigh')
 return M
def drag(V,rho,W,S,CD0,K,n=1):
 if min(V,rho,W,S,CD0,K,n)<=0:raise ValueError('Parámetros positivos requeridos')
 q=.5*rho*V*V;CL=n*W/(q*S);return q*S*(CD0+K*CL*CL)
def drag_limits(T,rho,W,S,CD0,K):
 """Positive mathematical speeds for constant thrust; stall/Mach limits are external.

 Use the product of the quadratic roots for the lower speed, avoiding
 catastrophic cancellation in T-sqrt(T*T-4*A*B). A repeated root is returned
 twice for compatibility with callers expecting a lower/upper pair.
 """
 if not all(math.isfinite(x) and x>0 for x in (T,rho,W,S,CD0,K)):
  raise ValueError('Empuje y parámetros de la polar finitos y positivos')
 A=.5*rho*S*CD0;B=2*K*W*W/(rho*S)
 minimum=2*math.sqrt(A)*math.sqrt(B)
 if T<minimum:return []
 # Scaled discriminant avoids overflow of T*T and cancellation near zero.
 ratio=minimum/T
 root=T*math.sqrt(max(0.,(1-ratio)*(1+ratio)))
 upper_square=(T/2+root/2)/A
 lower_square=B/(T/2+root/2)
 return [math.sqrt(lower_square),math.sqrt(upper_square)]
