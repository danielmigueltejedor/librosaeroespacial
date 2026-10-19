"""Legible vector redraws of ten original practice models.
Reproduces the equations printed in the manuscript with NumPy/SciPy;
these are new renders, not the historical Mathematica exports.
"""
from pathlib import Path
import hashlib,json,os
import numpy as np
from scipy.integrate import solve_ivp
from scipy.special import ellipk
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.ticker import NullFormatter
R=Path(__file__).resolve().parents[1];records=[]
(R/'evidence').mkdir(exist_ok=True)
plt.rcParams.update({'font.size':10,'text.color':'#142c40','axes.labelcolor':'#142c40','xtick.color':'#142c40','ytick.color':'#142c40','axes.spines.top':False,'axes.spines.right':False,'pdf.fonttype':42,'figure.facecolor':'white','axes.facecolor':'white'})
def new():return plt.subplots(figsize=(7,3.5),layout='constrained')
def save(i,fig,model,checks):
 p=R/f'figures/FIG-{i:04}/figure'
 if not os.environ.get('STUDIUM_FIGURES') or f'FIG-{i:04}' in os.environ['STUDIUM_FIGURES'].split(','):fig.savefig(p.with_suffix('.pdf'))
 plt.close(fig)
 assert all(checks.values()),checks
 records.append(dict(id=f'FIG-{i:04}',file=str(p.with_suffix('.pdf').relative_to(R)),sha256=hashlib.sha256(p.with_suffix('.pdf').read_bytes()).hexdigest(),model=model,checks={k:bool(v) for k,v in checks.items()}))
z=np.linspace(0,11000,301);T=288.15-.0065*z;p=(T/288.15)**(9.80665/(.0065*287.05287));rho=p*288.15/T
f,a=new()
for y,l in [(T/288.15,'T/T₀'),(p,'p/p₀'),(rho,'ρ/ρ₀')]:a.plot(z/1000,y,label=l)
a.set(xlabel='Altitud z (km)',ylabel='Valor relativo al nivel del mar (−)');a.legend();save(80,f,'Troposphere: ideal dry air, constant lapse and gravity',{'sea_level':all(abs(y[0]-1)<1e-12 for y in [p,rho]),'p_11km':abs(101325*p[-1]-22632.04)<.1})
g=9.81;v=30;th=np.deg2rad(40);k=1.2*.55*np.pi*.067**2/8;mass=.057
initial=[0,0,v*np.cos(th),v*np.sin(th)]
def ode(t,s):return [s[2],s[3],-k/mass*np.hypot(*s[2:])*s[2],-g-k/mass*np.hypot(*s[2:])*s[3]]
def ground(t,s):return s[1]
ground.terminal=True;ground.direction=-1
sol=solve_ivp(ode,[0,10],initial,events=ground,rtol=1e-10,atol=1e-11,max_step=.01);tt=np.linspace(0,2*v*np.sin(th)/g,301)
f,a=new();a.plot(v*np.cos(th)*tt,v*np.sin(th)*tt-g*tt**2/2,'--',color='black',label='Sin resistencia');a.plot(sol.y[0],sol.y[1],label='Resistencia cuadrática');a.set(xlabel='x (m)',ylabel='y (m)');a.legend();E=.5*mass*(sol.y[2]**2+sol.y[3]**2)+mass*g*sol.y[1];save(81,f,'Quadratic drag projectile with ground event',{'impact':abs(sol.y[1,-1])<1e-8,'energy_dissipates':np.max(np.diff(E))<1e-8,'shorter_range':sol.y[0,-1]<v**2*np.sin(2*th)/g})
amp=np.linspace(0,170,301);period=4*ellipk(np.sin(np.deg2rad(amp)/2)**2)/np.sqrt(g)
f,a=new();a.plot(amp,period,label='Periodo exacto (integral elíptica)');a.axhline(2*np.pi/np.sqrt(g),ls='--',color='black',label='Pequeñas oscilaciones');a.set(xlabel='Amplitud (grados)',ylabel='Periodo T (s)');a.legend();save(82,f,'Nonlinear pendulum, L=1 m',{'small_angle_limit':abs(period[0]-2*np.pi/np.sqrt(g))<1e-12,'period_increases':np.all(np.diff(period)>0)})
x=np.linspace(-2,2,241);y=np.linspace(-1,3,241);X,Y=np.meshgrid(x,y);u=X**2+4*X*Y;vv=-2*X*Y-2*Y**2;psi=X**2*Y+2*X*Y**2
f,a=new();a.streamplot(x,y,u,vv,color='#8899a6',density=.65,linewidth=.7);cs=a.contour(X,Y,psi,levels=[-12,-6,-2,-.5,.5,2,6,12],colors='#184a82',linewidths=1);a.plot(1,2,'o',color='#ab4515');a.annotate('',(1+42/150,2+84/150),(1,2),arrowprops={'arrowstyle':'->','color':'#ab4515'});a.text(-1.9,2.8,'a(1,2) = (42, 84) m/s²',fontsize=9,bbox={'facecolor':'white','edgecolor':'none','pad':2});a.set(xlabel='x (m)',ylabel='y (m)',aspect='equal');save(83,f,'psi=x²y+2xy², u=psi_y, v=-psi_x',{'point_velocity':9==1+4*1*2 and -12==-2*1*2-2*4,'divergence_identity':np.max(abs((2*X+4*Y)+(-2*X-4*Y)))<1e-12,'acceleration_at_point':10*9+4*(-12)==42 and (-4)*9+(-10)*(-12)==84})
dp=np.linspace(0,40000,301);f,a=new()
for b in [.4,.5,.6,.7]:a.plot(dp/1000,1000*np.pi*(b*.1)**2/4*np.sqrt(2*dp/(998*(1-b**4))),label=f'd₂/d₁ = {b}')
a.set(xlabel='Diferencia de presión Δp (kPa)',ylabel='Caudal Q (L/s)');a.legend();q=np.pi*.05**2/4*np.sqrt(40000/(998*(1-.5**4)));save(84,f,'Ideal incompressible Venturi, d1=100 mm, rho=998 kg/m³',{'reference_flow':abs(q-.012838)<1e-6})
th=np.linspace(0,2*np.pi,721);f,a=new()
for G in [0,.5]:a.plot(np.rad2deg(th),1-(2*np.sin(th)+G)**2,label='Sin circulación' if G==0 else 'G = 0,5')
a.set(xlabel='Ángulo θ (grados)',ylabel='Coeficiente de presión Cₚ (−)');a.legend();save(85,f,'Inviscid cylinder Cp=1−(2sinθ+G)²',{'stagnation_no_circulation':abs((1-(2*np.sin(0))**2)-1)<1e-12})
e=np.linspace(0,1,301);f,a=new()
for P in [-2,-1,0,1,2]:a.plot(e,e*(1+P-P*e),label=f'P = {P}')
a.set(xlabel='Posición y/h (−)',ylabel='Velocidad u/U (−)');a.legend(ncol=2);save(86,f,'Couette–Poiseuille: eta(1+P−P eta)',{'both_wall_conditions':all(abs((1+P-P)-1)<1e-12 for P in [-2,-1,0,1,2])})
r=np.linspace(.01,.03,301);finite=r[r<=.015];A=-3*.01/(.015**2-.01**2);B=-A*.015**2
f,a=new();a.plot(finite*1000,A*finite+B/finite,label='Carcasa fija a 15 mm');a.plot(r*1000,3*.01/r,'--',label='Fluido ilimitado');a.set(xlabel='Radio r (mm)',ylabel='Velocidad azimutal uθ (m/s)');a.legend();save(87,f,'Concentric-cylinder Couette: Ar+B/r',{'inner_wall':abs(A*.01+B/.01-3)<1e-12,'outer_wall':abs(A*.015+B/.015)<1e-12})
Bdat=np.array([5,10,20,40,80]);Udat=np.array([28.2,34.7,42.8,52.7,64.8])*.001;Ar=1000*Bdat*.004**3/1e-6;Re=1000*Udat*.004/.001;n,lc=np.polyfit(np.log(Ar),np.log(Re),1);ar=np.geomspace(200,8000,200)
f,a=new();a.loglog(Ar,Re,'ks',label='Tabla del capítulo 10');a.loglog(ar,np.exp(lc)*ar**n,label=fr'Ajuste: Re = {np.exp(lc):.3f} Ar$^{{{n:.5f}}}$');a.set(xlabel='Número de Arquímedes Ar (−)',ylabel='Reynolds crítico Re (−)');a.legend();a.set_xticks([200,500,1000,2000,5000],labels=['200','500','1000','2000','5000']);a.set_yticks([100,200,300],labels=['100','200','300']);a.xaxis.set_minor_formatter(NullFormatter());a.yaxis.set_minor_formatter(NullFormatter());save(88,f,'Log least-squares power law on original rounded table',{'exponent':abs(n-.30035)<1e-5})
y=np.linspace(0,.01,401);f,a=new();checks={}
for t in [2,10,30,60,200]:
 nn=np.arange(1,161)[:,None];vel=.1*(1-y/.01)-.2/np.pi*np.sum(np.exp(-nn**2*np.pi**2*1e-6*t/.01**2)*np.sin(nn*np.pi*y/.01)/nn,axis=0);a.plot(y*1000,vel,label=f't = {t} s');checks[f'walls_{t}s']=abs(vel[0]-.1)<1e-12 and abs(vel[-1])<1e-12
checks['stationary_limit']=np.max(abs(vel-.1*(1-y/.01)))<1e-8
a.set(xlabel='Distancia a la placa móvil y (mm)',ylabel='Velocidad u (m/s)');a.legend();save(89,f,'Exact startup Couette Fourier series, 160 terms (not NDSolve output)',checks)
(R/'evidence/practice-figure-redraws.json').write_text(json.dumps(dict(generator='scripts/redraw_practice_figures.py',classification='derived',figures=records),ensure_ascii=False,indent=2)+'\n')
