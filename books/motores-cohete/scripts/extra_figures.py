"""Perfiles ideales de presión y empuje frente a altura atmosférica académica."""
from pathlib import Path
import json,math
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from models import mach_area,stagnation_ratios,shock,nozzle
R=Path(__file__).resolve().parents[1];O=R/'figures'
def save(key,fig):
 for ext in ['pdf','svg']:fig.savefig(O/(key+'.'+ext))
 fig.savefig(O/(key+'.png'),dpi=160);plt.close(fig)
def draw():
 plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10,'pdf.fonttype':42,'axes.spines.top':False,'axes.spines.right':False})
 x=np.linspace(-1,2,301);area=lambda t:1+(2 if t<0 else 1.5)*t*t;g=1.4
 f,a=plt.subplots(figsize=(7.2,4.3),layout='constrained')
 psub=[stagnation_ratios(mach_area(area(float(t)),g,'subsonic'),g)['p_p0'] for t in x]
 psup=[stagnation_ratios(mach_area(area(float(t)),g,'subsonic' if t<0 else 'supersonic'),g)['p_p0'] for t in x]
 a.plot(x,psub,label='Primer bloqueo; divergente subsónico',color='#184a82');a.plot(x,psup,label='Rama supersónica completa',color='#00a5b5')
 xs=.8;M1=mach_area(area(xs),g);s=shock(M1,g);ratio=s['p02_p01'];xp=np.linspace(xs,2,140);pp=[ratio*stagnation_ratios(mach_area(area(float(t))*ratio,g,'subsonic'),g)['p_p0'] for t in xp];before=stagnation_ratios(M1,g)['p_p0'];after=before*s['p2_p1']
 left=np.linspace(-1,xs,200);pl=[stagnation_ratios(mach_area(area(float(t)),g,'subsonic' if t<0 else 'supersonic'),g)['p_p0'] for t in left];a.plot(left,pl,color='#ad7931');a.plot([xs,xs],[before,after],color='#ad7931');a.plot(xp,pp,color='#ad7931',label='Choque normal interno')
 a.axvline(0,color='gray',ls=':',lw=.8);a.set(title='Distribución de presión: tres regímenes ideales',xlabel='Coordenada axial normalizada; garganta en 0',ylabel='Presión estática / p₀ de cámara');a.grid(alpha=.2);a.legend(fontsize=8);save('pressure-profiles',f)
 h=np.linspace(0,30000,250);pa=101325*np.exp(-h/7000);vals=[nozzle(1.32,350,2600,3e6,.0004,4,float(p)) for p in pa];vac=nozzle(1.32,350,2600,3e6,.0004,4,0)['F'];f,a=plt.subplots(figsize=(7.2,4.3),layout='constrained');a.plot(h/1000,[v['F']/1000 for v in vals],color='#184a82',label='Ambiente exponencial');a.axhline(vac/1000,color='#00a5b5',ls='--',label='Vacío, igual estado interno');a.set(title='Empuje y presión exterior durante un ascenso idealizado',xlabel='Altura del modelo (km)',ylabel='Empuje (kN)');a.grid(alpha=.2);a.legend();a.text(.45,.14,'pₐ = 101325 exp(−h/7000) Pa\nModelo atmosférico académico',transform=a.transAxes,fontsize=9);save('thrust-altitude',f)
if __name__=='__main__':
 draw();data=[dict(key='pressure-profiles',chapter=8,caption='Perfiles de presión de una misma geometría ideal. El choque cambia presión total y área crítica de referencia; la separación viscosa no está modelada.',model='gamma1.4; A/At=1+2x² convergente,1+1.5x² divergente; choque en x=.8'),dict(key='thrust-altitude',chapter=7,caption='Empuje calculado con cámara y geometría fijas y presión exterior exponencial académica. No es una atmósfera estándar ni una trayectoria validada; se supone flujo adherido.',model='gamma1.32,R350,Tc2600,pc3MPa,At4e-4m²,eps4; pa101325exp(-h/7000)')];(R/'evidence/additional-figures.json').write_text(json.dumps(data,ensure_ascii=False,indent=2))
