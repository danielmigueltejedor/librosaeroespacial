"""Figuras originales. Los parámetros son docentes salvo CSV JSBSim identificado."""
from pathlib import Path
import os
import json,csv
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from scipy.linalg import expm
from models import *
ROOT=Path(__file__).resolve().parents[1]
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10,'axes.spines.top':False,'axes.spines.right':False,'axes.labelcolor':'#142c40','text.color':'#142c40','axes.prop_cycle':plt.cycler(color=['#184a82','#8a4e0c','#603082','#1b6b3a'])})
def save(name,ax,xlabel=None,ylabel=None):
    if xlabel:ax.set_xlabel(xlabel)
    if ylabel:ax.set_ylabel(ylabel)
    ax.grid(alpha=.2);ax.figure.tight_layout()
    if not os.environ.get('STUDIUM_FIGURES') or name in os.environ['STUDIUM_FIGURES'].split(','):ax.figure.savefig(ROOT/'figures'/f'{name}.pdf')
    plt.close(ax.figure)
def plot(name,x,ys,xlabel,ylabel):
    fig,ax=plt.subplots(figsize=(7,3.8))
    for label,y in ys:ax.plot(x,y,label=label)
    if len(ys)>1:ax.legend(frameon=False)
    save(name,ax,xlabel,ylabel)

p=Polar(28,.024,.046,1.55);m=4800;rho=isa(4500)[2]
cl=np.linspace(.05,1.55,300)
plot('polar',cl,[('Polar total',p.cd(cl))],'Coeficiente de sustentación $C_L$','Coeficiente de resistencia $C_D$')
plot('eficiencias',cl,[('$C_L/C_D$',cl/p.cd(cl)),('$C_L^{3/2}/C_D$',cl**1.5/p.cd(cl)),(r'$\sqrt{C_L}/C_D$',np.sqrt(cl)/p.cd(cl))],'$C_L$','Funciones objetivo adimensionales')
v=np.linspace(p.stall(m,rho),180,300)
A=.5*rho*p.S*p.cd0; B=2*p.k*(m*G)**2/(rho*p.S)
plot('resistencia',v,[('Total',p.drag(v,m,rho)/1000),('Término $AV^2$',A*v*v/1000),('Término $B/V^2$',B/v**2/1000)],'TAS (m/s)','Resistencia (kN)')
plot('potencia',v,[('Potencia de empuje necesaria',p.power(v,m,rho)/1000),('Disponible: ejemplo constante',np.zeros_like(v)+650)],'TAS (m/s)','Potencia (kW)')
gl=Polar(15.8,.013,.031,1.6);vm=np.linspace(18,55,260)
sink=[]
for V in vm:
    CL=2*420*G/(1.225*gl.S*V*V)
    sink.append(gl.power(V,420,1.225)/(420*G))
plot('polar-descenso',vm,[('Descenso, aproximación de ángulo pequeño',sink)],'TAS (m/s)','Tasa de descenso positiva (m/s)')
h=np.linspace(0,9000,150);dens=np.array([isa(x)[2] for x in h])
fig,ax=plt.subplots(figsize=(7,3.8));ax.plot(dens,h/1000);save('isa-densidad',ax,'Densidad ISA (kg/m³)','Altitud geopotencial (km)')
plot('velocidades-altura',h/1000,[('TAS para EAS = 60 m/s',60*np.sqrt(RHO0/dens)),('EAS mantenida',np.zeros_like(h)+60)],'Altitud geopotencial (km)','Velocidad (m/s)')
clg=gl.cl_ld();gs=[glide_integral(gl,420,x,0,clg) for x in h]
plot('planeo-integral',h/1000,[('Alcance en calma (km)',[z['air_range']/1000 for z in gs]),('Con viento de cara 8 m/s (km)',[z['ground_range']/1000-z['time']*8/1000 for z in gs])],'Altitud inicial (km)','Alcance horizontal (km)')
mf=np.linspace(3800,4799,150)
rs=[jet_fixed_cl(p,4800,x,rho,p.cl_jet_range(),1.65e-5) for x in mf]
rc=[jet_fixed_v(p,4800,x,rho,105,1.65e-5) for x in mf]
plot('jet-consumo',(4800-mf),[('CL constante, óptimo de alcance',np.array([x['range'] for x in rs])/1000),('TAS constante 105 m/s',np.array([x['range'] for x in rc])/1000)],'Combustible consumido (kg)','Alcance en calma (km)')
plot('leyes-pilotaje',mf/4800,[('V constante',np.ones_like(mf)),('CL y densidad constantes',np.sqrt(mf/4800))],'Masa / masa inicial','TAS / TAS inicial')
T=6500
excess=(T-p.drag(v,m,rho))/(m*G)
plot('ascenso',v,[('Tasa de ascenso aproximada',v*excess)],'TAS (m/s)','Velocidad vertical (m/s)')
fig,axes=plt.subplots(2,1,figsize=(7,5.2),sharex=True);et=T-p.drag(v,m,rho);ep=v*et
for ax,values,unit in [(axes[0],et/1000,'Exceso de empuje (kN)'),(axes[1],ep/1000,'Exceso de potencia (kW)')]:
 ax.plot(v,values);opt=int(np.argmax(values));ax.axvline(v[opt],color='#8a4e0c',ls='--',lw=1);ax.scatter([v[opt]],[values[opt]],color='#8a4e0c');ax.set_ylabel(unit);ax.grid(alpha=.2);ax.annotate(f'Máximo de rejilla: {v[opt]:.1f} m/s',(v[opt],values[opt]),xytext=(6,-18),textcoords='offset points',fontsize=8)
save('vx-vy',axes[1],'TAS (m/s)')
ceiling=[]
hceil=np.linspace(0,16000,240)
for z in hceil:
    rz=isa(z)[2];vz=np.linspace(p.stall(m,rz),220,500)
    ceiling.append(np.max((9000*(rz/RHO0)**.8-p.drag(vz,m,rz))*vz/(m*G)))
plot('techo',hceil/1000,[('Máxima tasa del modelo',ceiling)],'Altitud (km)','Tasa de ascenso máxima (m/s)')
bank=np.deg2rad(np.linspace(0,70,250))
plot('carga-viraje',np.rad2deg(bank),[('Factor de carga',1/np.cos(bank)),('Factor de velocidad de pérdida',np.sqrt(1/np.cos(bank)))],'Alabeo (grados)','Factor respecto al vuelo nivelado')
vv=np.linspace(35,120,300)
plot('radio-viraje',vv,[('Alabeo 25°',vv**2/(G*np.tan(np.deg2rad(25)))),('Alabeo 45°',vv**2/G)],'TAS (m/s)','Radio de viraje (m)')
plot('helice-eta',np.linspace(15,120,150),[('Ejemplo de eficiencia variable',.83*(1-np.exp(-np.linspace(15,120,150)/30)))],'TAS (m/s)','Eficiencia de hélice (modelo ilustrativo)')
land=Polar(18,.035,.055,1.9)
mass=np.linspace(1100,1750,120)
dist=[ground_roll(land,x,1.225,1.12*land.stall(x,1.225),lambda v:5000,.03,.65)['distance'] for x in mass]
plot('despegue-masa',mass,[('Rodadura hasta 1.12 Vs',dist)],'Masa (kg)','Distancia de rodadura (m)')
mu=np.linspace(.15,.5,100)
dist=[ground_roll(land,1500,1.225,30,lambda v:0,x,.20,braking=True)['distance'] for x in mu]
plot('aterrizaje-freno',mu,[('Rodadura con T=0',dist)],'Coeficiente de frenado','Distancia desde 30 m/s (m)')
alpha=np.deg2rad(np.linspace(-3,12,150))
plot('cm-alpha',np.rad2deg(alpha),[('CG adelantado: estable',.06-.8*alpha),('Punto neutro',.06+0*alpha),('CG retrasado: inestable',.06+.35*alpha)],'Incidencia (grados)','$C_m$')
beta=np.deg2rad(np.linspace(-10,10,100))
plot('lateral-derivadas',np.rad2deg(beta),[(r'$C_\ell$: diedro estabilizador',-.10*beta),('$C_n$: estabilidad direccional',.13*beta)],'Resbalamiento (grados)','Coeficiente de momento')
t=np.linspace(0,35,500)
plot('modos-dinamicos',t,[('Oscilación amortiguada',np.exp(-.12*t)*np.cos(1.5*t)),('Oscilación creciente',np.exp(.025*t)*np.cos(1.5*t))],'Tiempo (s)','Perturbación normalizada (ejemplo sintético)')
for name in ['t6-trim-grid.csv','b747-cruise-1800s.csv']:
    with (ROOT/'simulations/results'/name).open() as stream:rows=list(csv.DictReader(stream))
    if name.startswith('t6'):
        fig,ax=plt.subplots(figsize=(7,3.8))
        for fuel in [300,425]:
         for alt in [5000,9000]:
          rr=[r for r in rows if float(r['tank_each_lbm'])==fuel and float(r['requested_h_ft'])==alt]
          ax.plot([float(r['EAS_m_s']) for r in rr],[float(r['drag_N'])/1000 for r in rr],label=f'{5000+2*fuel:.0f} lbm; {alt} ft')
        ax.legend(frameon=False,fontsize=8);save('jsbsim-t6',ax,'EAS resultante (m/s)','Resistencia de trim (kN)')
        fig,ax=plt.subplots(figsize=(7,3.8))
        rr=[r for r in rows if float(r['tank_each_lbm'])==425 and float(r['requested_h_ft'])==5000]
        ax.plot([float(r['TAS_m_s']) for r in rr],[float(r['excess_power_approx_m_s']) for r in rr]);save('jsbsim-ascenso',ax,'TAS (m/s)','Tasa aproximada por exceso de potencia (m/s)')
    else:
        plot('jsbsim-b747',np.array([float(r['time_s']) for r in rows])/60,[('Combustible calculado por JSBSim',np.array([float(r['fuel_kg']) for r in rows])/1000)],'Tiempo (min)','Combustible (t)')

# Diagramas vectoriales con ejes y fuerzas definidos, sin figuras protegidas.
fig,ax=plt.subplots(figsize=(7,3.8));ax.set_aspect('equal');ax.axis('off')
g=-.12; tangent=np.array([np.cos(g),np.sin(g)]);normal=np.array([-np.sin(g),np.cos(g)])
for vec,label,color in [(tangent*2,'V','#184a82'),(-tangent*(-1.8*np.sin(g)),'D','#8a4e0c'),(normal*(1.8*np.cos(g)),'L','#1b6b3a'),(np.array([0,-1.8]),'W','#603082')]:
 ax.annotate('',xy=vec,xytext=(0,0),arrowprops=dict(arrowstyle='->',lw=2,color=color))
 if label=='D':ax.annotate(label,xy=vec,xytext=(-.75,.4),color=color,arrowprops={'arrowstyle':'-','color':color,'lw':.7})
 else:ax.text(*(vec*1.1),label,color=color)
ax.plot([-2,2],[.24,-.24],':',color='gray');ax.scatter([0],[0],color='#142c40');ax.set_xlim(-2.5,2.5);ax.set_ylim(-2.2,2.3);save('fuerzas-planeo',ax)
fig,ax=plt.subplots(figsize=(6,4.6));ax.set_aspect('equal');ax.axis('off');phi=np.deg2rad(35)
for vec,label in [(np.array([np.sin(phi),np.cos(phi)])*2,'L'),(np.array([0,-2*np.cos(phi)]),'W')]:
 ax.annotate('',xy=vec,xytext=(0,0),arrowprops=dict(arrowstyle='->',lw=2));ax.text(*(vec*1.1),label)
ax.plot([-1.5,1.5],[1.5*np.tan(phi),-1.5*np.tan(phi)],color='#184a82',lw=3);ax.plot([0,2*np.sin(phi)],[2*np.cos(phi),2*np.cos(phi)],':',color='gray');ax.annotate('',(2*np.sin(phi),0),(0,0),arrowprops={'arrowstyle':'->','color':'#8a4e0c','lw':1.5});ax.text(.5,-.35,r'$L\sin\phi$',color='#8a4e0c');ax.text(-1.85,1.85,r'$L\cos\phi=W$',fontsize=10);ax.set_xlim(-2,2);ax.set_ylim(-2.2,2.5);save('fuerzas-viraje',ax)
print('Figuras PDF originales:',len(list((ROOT/'figures').glob('*.pdf'))))
