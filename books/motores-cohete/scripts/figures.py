"""28 figuras originales de modelos docentes. PDFs vectoriales y SVG editables."""
from pathlib import Path
import json,math
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle,Circle,Polygon
from models import area_mach,mach_area,stagnation_ratios,cstar,nozzle,shock,G0
R=Path(__file__).resolve().parents[1];O=R/'figures';O.mkdir(exist_ok=True)
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10,'pdf.fonttype':42,'axes.spines.top':False,'axes.spines.right':False,'savefig.facecolor':'white','text.color':'#142c40','axes.labelcolor':'#142c40'})
B='#184a82';C='#00a5b5';G='#ad7931';P='#70468b';META=[]
def canvas(title):
 f,a=plt.subplots(figsize=(7.2,4.2),layout='constrained');a.set_title(title,pad=13);a.grid(alpha=.18);return f,a
def save(ch,f,model,caption):
 key=f'c{ch:02d}'
 for ext in ['pdf','svg']:f.savefig(O/f'{key}.{ext}')
 f.savefig(O/f'{key}.png',dpi=140);plt.close(f);META.append(dict(key=key,chapter=ch,model=model,caption=caption,original=True))
def schematic(title):
 f,a=canvas(title);a.set(xlim=(0,10),ylim=(0,6));a.axis('off');return f,a
def box(a,x,y,w,h,t,c=B):
 a.add_patch(Rectangle((x,y),w,h,ec=c,fc='#eef3f8',lw=1.5));a.text(x+w/2,y+h/2,t,ha='center',va='center',fontsize=9)
def arrow(a,p,q,t='',c=B):
 a.annotate('',xy=q,xytext=p,arrowprops={'arrowstyle':'->','lw':1.6,'color':c})
 if t:a.text((p[0]+q[0])/2,(p[1]+q[1])/2+.18,t,ha='center',fontsize=9,color=c)
f,a=canvas('Energía de chorro fija: dos compromisos distintos');v=np.linspace(2000,30000,200);a.plot(v/1000,1200/v,c=B);a.set(xlabel='Velocidad de escape (km/s)',ylabel='Empuje (N)');a.text(15,.45,'Potencia cinética: 600 W\nChorro axial uniforme');save(1,f,'F=2Pj/v; Pj600W; sin presión de salida','A potencia de chorro fija, aumentar la rapidez reduce el empuje. Modelo axial monocinético, sin término de presión.')
f,a=schematic('Volumen de control y convenio axial');box(a,1.6,2.1,3,1.8,'Cámara\ny masa a bordo');a.plot([4.6,5.3,7.8],[3.9,3.5,4.2],c=B,lw=2);a.plot([4.6,5.3,7.8],[2.1,2.5,1.8],c=B,lw=2);a.add_patch(Rectangle((1.3,1.5),6.7,3,fill=False,ls='--',ec=P));arrow(a,(6.3,3),(9.3,3),'Escape: uₓ = −vₑ',C);arrow(a,(2,4.9),(.4,4.9),'+x, empuje',B);arrow(a,(7.8,.8),(9,.8),'Normal exterior',G);a.text(7.9,4.6,'Salida: pₑ, Aₑ',ha='center');a.text(4.9,.3,'Presión exterior uniforme: pₐ · Esquema sin escala',ha='center');save(2,f,'Eje positivo hacia delante; salida atrás; n_x=-1','El escape cruza hacia atrás y la reacción propulsiva apunta hacia delante. El cierre de presión utiliza la diferencia entre salida y ambiente.')
f,a=canvas('Estados estáticos y de remanso');M=np.linspace(0,4,300)
for name,fn,col in [('T/T₀',lambda m:stagnation_ratios(m,1.4)['T_T0'],B),('p/p₀',lambda m:stagnation_ratios(m,1.4)['p_p0'],C)]:a.plot(M,[fn(m) for m in M],label=name,c=col)
a.set(xlabel='Mach (adimensional)',ylabel='Cociente estático/total');a.legend();save(3,f,'Gas ideal gamma1.4; composición fija e isentropía','Relaciones de remanso de un gas caloríficamente perfecto. La presión disminuye más deprisa que la temperatura al aumentar Mach.')
f,a=canvas('Incertidumbre y correlación de medidas');r=np.linspace(-1,1,200);u=np.sqrt(.012**2+.008**2-2*r*.012*.008);a.plot(r,u*100,c=B);a.set(xlabel='Coeficiente de correlación F–caudal',ylabel='Incertidumbre relativa de Isp (%)');save(4,f,'uF/F=.012; um/m=.008; propagación lineal covarianza','La incertidumbre de un cociente depende también de la correlación. Curva linealizada con incertidumbres relativas fijas.')
x=np.linspace(-1,2,241);Ar=1+np.where(x<0,2*x*x,1.5*x*x);Mm=np.array([mach_area(float(ar),1.4,'subsonic' if xx<0 else 'supersonic') for xx,ar in zip(x,Ar)])
f,ax=plt.subplots(2,1,figsize=(7.2,5.2),layout='constrained');rad=np.sqrt(Ar);ax[0].plot(x,rad,c=B);ax[0].plot(x,-rad,c=B);ax[0].fill_between(x,rad,rad+.3,color='#dde6f0');ax[0].fill_between(x,-rad-.3,-rad,color='#dde6f0');ax[0].set(ylabel='Radio / radio garganta');ax[0].set_title('Tobera de Laval: solución transónica ideal');ax[1].plot(x,Mm,c=C);ax[1].axhline(1,ls='--',c=G);ax[1].set(xlabel='Coordenada axial normalizada',ylabel='Mach');save(5,f,'A/At=1+2x² aguas arriba,1+1.5x² aguas abajo; gamma1.4','Geometría académica y rama transónica isentrópica. La curva presupone condiciones de contorno compatibles; no describe cualquier contrapresión.')
f,a=canvas('Una misma área admite dos ramas');ms=np.linspace(.08,4,600);a.plot(ms,[area_mach(m,1.4) for m in ms],c=B);a.axvline(1,c=G,ls='--');a.axhline(3,c=C,ls='--',label='A/A* = 3');a.scatter([mach_area(3,1.4,b) for b in ['subsonic','supersonic']],[3,3],c=P,zorder=3);a.set(xlabel='Mach',ylabel='A/A*',ylim=(.8,8));a.legend();save(6,f,'Relación área-Mach gamma1.4, ambas raíces Brent','La inversión exige seleccionar rama. El mínimo de área crítica corresponde a Mach uno.')
f,a=canvas('Coeficiente de empuje y ambiente');ep=np.linspace(1,30,200)
for pr,col in [(0,B),(.01,C),(.03,G)]:a.plot(ep,[nozzle(1.3,350,2600,1e6,.001,float(e),pr*1e6)['CF'] for e in ep],label=f'pₐ/pc = {pr:g}',c=col)
a.set(xlabel='Relación de expansión Ae/At',ylabel='CF ideal');a.legend();a.text(.44,.13,'Rama supersónica candidata\nAdherencia no comprobada',transform=a.transAxes,fontsize=9,bbox={'facecolor':'white','edgecolor':'none','alpha':.8});save(7,f,'gamma1.3; ecuaciónCF; candidatas supersónicas no mapa separación','El ambiente penaliza áreas grandes. Las curvas son candidatas ideales de rama supersónica; su prolongación no demuestra compatibilidad ni ausencia de separación.')
f,a=canvas('Tres umbrales diferentes de contrapresión');eps=np.linspace(1.01,8,200);g=1.4;subs=[];sh=[];ad=[]
for e in eps:
 mu=mach_area(float(e),g,'subsonic');ms=mach_area(float(e),g);r=stagnation_ratios(ms,g)['p_p0'];subs.append(stagnation_ratios(mu,g)['p_p0']);sh.append(r*shock(ms,g)['p2_p1']);ad.append(r)
a.plot(eps,subs,c=B,label='Primer bloqueo');a.plot(eps,sh,c=G,label='Choque en salida');a.plot(eps,ad,c=C,label='Adaptación');a.set(xlabel='Ae/At',ylabel='pb/p₀',ylim=(0,1.05));a.legend();save(8,f,'gamma1.4; umbral inicio por rama subsónica y choque salida normal','Mapa de umbrales del modelo ideal. La separación viscosa no está incluida y no puede deducirse de estas curvas.')
f,a=canvas('Divergencia de un chorro cónico idealizado');ang=np.linspace(0,35,200);a.plot(ang,(1+np.cos(np.deg2rad(ang)))/2,c=B);a.set(xlabel='Semiángulo del cono (grados)',ylabel='Factor axial λ');save(9,f,'lambda=(1+cosalpha)/2; rapidez uniforme y reparto uniforme por ángulo sólido','Factor de momento axial para un reparto cónico idealizado. No corrige automáticamente empuje de presión ni representa cualquier campana.')
f,a=schematic('Motor sólido: funciones separadas');a.add_patch(Rectangle((1,1.7),6.3,2.6,ec=B,fc='#dce6ef',lw=3));a.add_patch(Rectangle((1.3,2),5.6,2,ec=G,fc='#f5e9d4',lw=2));a.add_patch(Rectangle((1.3,2.7),5.6,.6,ec=C,fc='white',lw=1.5));a.plot([7,7.4,9],[3.3,3.1,4],c=B,lw=2);a.plot([7,7.4,9],[2.7,2.9,2],c=B,lw=2);a.text(4,4.9,'Envolvente resistente y protección térmica',ha='center');a.text(4,3.65,'Masa propulsante',ha='center');arrow(a,(4,3),(6.5,3),'Gas',C);a.text(4,.8,'Superficie activa: frontera que retrocede\nDibujo funcional sin escala ni especificaciones',ha='center');save(10,f,'Esquema funcional; no dimensiones de fabricación','Funciones de envolvente, protección, masa almacenada y cavidad. La superficie activa evoluciona durante el consumo.')
f,a=canvas('Superficie activa frente a profundidad');w=np.linspace(0,.8,200);a.plot(w,1+w,c=B,label='Cilindro interior');a.plot(w,1-w,c=G,label='Cilindro exterior');a.axhline(1,c=C,label='Superficie plana');a.set(xlabel='Profundidad / radio de referencia',ylabel='Área activa / área inicial');a.legend();save(11,f,'L fijo; extremos inactivos; radios1±w; plana constante','Tres geometrías normalizadas. La progresividad se define respecto a profundidad, sin imponer una duración de regresión.')
f,a=canvas('Amplificación de presión cuasiestacionaria');ab=np.linspace(.7,1.5,250)
for n,col in [(.2,B),(.4,C),(.7,G)]:a.plot(ab,ab**(1/(1-n)),c=col,label=f'n = {n}')
a.set(xlabel='Área activa / área inicial',ylabel='Presión / presión inicial');a.legend();save(12,f,'P=area_ratio^(1/(1-n)); garganta y propiedades fijas','Modelo normalizado de equilibrio generación-descarga. Una superficie variable produce presión variable; no es una predicción de un propulsante real.')
f,a=canvas('Relajación del modelo concentrado lineal');tt=np.linspace(0,12,300)
for n,col in [(.2,B),(.5,C),(.8,G)]:a.plot(tt,np.exp(-(1-n)*tt),label=f'n = {n}',c=col)
a.set(xlabel='Tiempo / τ₀',ylabel='Perturbación / perturbación inicial');a.legend();save(13,f,'delta/delta0=exp[-(1-n)t/tau0]; perturbación pequeña','Estabilidad local de un único estado con temperatura y volumen fijos. No evalúa modos acústicos ni certifica estabilidad de combustión.')
f,a=canvas('Relación de mezcla y fracciones másicas');rr=np.linspace(.1,8,200);a.plot(rr,rr/(1+rr),c=B,label='Oxidante');a.plot(rr,1/(1+rr),c=C,label='Combustible');a.set(xlabel='Relación másica oxidante/combustible',ylabel='Fracción de masa');a.legend();save(14,f,'Dos corrientes sin acumulación ni auxiliares','Las fracciones suman uno, pero no determinan por sí solas composición local de cámara ni prestación.')
f,a=canvas('CEA ejecutado: disociación de agua en equilibrio');rows=json.load(open(R/'reports/cea-case.json'))['rows']
for p,col in [(1,B),(10,C)]:
 z=[r for r in rows if r['p_bar']==p];a.plot([r['T_K'] for r in z],[r['mole_fractions']['H2O'] for r in z],marker='o',c=col,label=f'{p} bar')
a.set(xlabel='Temperatura fijada (K)',ylabel='Fracción molar H₂O',ylim=(0,1.05));a.legend();save(15,f,'CEA3.3.4 TP; seis especies neutras H2O,H2,O2,OH,O,H; tresT porp','Resultados TP reales de software, con segmentos como guía visual entre estados discretos. No es una expansión de tobera ni un ensayo de motor.')
f,a=canvas('Vaporización de gota: escala del diámetro');t=np.linspace(0,4,300)
for d,col in [(1,B),(2,C)]:a.plot(t,np.maximum(d*d-t,0),c=col,label=f'd₀/dref = {d}')
a.set(xlabel='Tiempo · K / dref²',ylabel='d² / dref²');a.legend();save(16,f,'Leyd²=d0²-Kt; líneas sólohastaagotamiento','Modelo de gota aislada con propiedades constantes. Duplicar diámetro cuadruplica la escala de duración.')
f,a=schematic('Pared y refrigerante: resistencias en serie');names=['Gas\nTaw','Convección\n1/hg','Pared\nδ/k','Convección\n1/hl','Fluido\nTl']
for i,t in enumerate(names):
 box(a,.3+i*1.95,2.5,1.65,1.2,t)
 if i<4:arrow(a,(1.95+i*1.95,3.1),(2.25+i*1.95,3.1),c=C)
a.text(5,4.5,'Régimen estacionario · misma área de referencia',ha='center');a.text(5,1.2,'q″ = (Taw − Tl) / (1/hg + δ/k + 1/hl)',ha='center');save(17,f,'Convección-conducción plana-convección; sinradiación ni almacenamiento','Red térmica ideal. Las temperaturas de pared se obtienen de las caídas parciales; no se igualan a la temperatura del gas.')
f,a=canvas('Expansión de una masa fija de gas');vr=np.linspace(1,4,200);a.plot(vr,1/vr,c=B,label='Isotérmica');a.plot(vr,vr**(-1.4),c=C,label='Adiabática reversible, γ = 1.4');a.set(xlabel='V/V₀',ylabel='p/p₀');a.legend();save(18,f,'pV^kconst; k1 y1.4; masa fija','Dos procesos límite para gas ideal. No representan directamente un reservorio rígido que pierde masa.')
f,ax=plt.subplots(2,2,figsize=(8,5.8),layout='constrained')
for a,title,names,sub in zip(ax.flat,['Presión de gas','Generador de gas','Combustión escalonada','Expansor'],[['Depósito','Cámara','Tobera'],['Generador','Turbina','Descarga auxiliar'],['Precombustión','Turbina','Cámara principal'],['Refrigeración','Turbina','Cámara principal']],['Sin eje principal','Parte del caudal fuera de cámara','Masa de turbina vuelve a cámara','Calor recuperado aporta energía de eje']):
 a.axis('off');a.set(xlim=(0,10),ylim=(0,4));a.set_title(title)
 for j,t in enumerate(names):
  box(a,.1+j*3.35,1.4,2.9,1.1,t)
  if j<2:arrow(a,(3+j*3.35,1.95),(3.45+j*3.35,1.95))
 a.text(5,.45,sub,ha='center',fontsize=8)
save(19,f,'Rutas funcionales parciales; bombas,retornos y otrascorrientes omitidas,explicadas texto','Comparación de la ruta que distingue cada ciclo. Son esquemas funcionales parciales, no balances completos ni planos de instalación.')
f,a=canvas('La fase entre presión y calor importa');ph=np.linspace(0,360,300);a.plot(ph,.5*np.cos(np.deg2rad(ph)),c=B);a.axhline(0,c='gray',lw=.8);a.set(xlabel='Desfase (grados)',ylabel='Promedio p′q′ / (amplitudes)');save(20,f,'Promedio de cosenos=.5cosphi; no pérdidas acústicas','Indicador de aporte termoacústico para oscilaciones sinusoidales. El crecimiento exige además superar pérdidas y flujos por fronteras.')
f,a=canvas('Propulsión eléctrica: potencia disponible fija');vel=np.linspace(10e3,50e3,200)
for power,col in [(1000,B),(2000,C)]:a.plot(vel/1000,2*.6*power/vel,c=col,label=f'{power/1000:g} kW; η = 0.60')
a.set(xlabel='Velocidad de escape ideal (km/s)',ylabel='Empuje (N)');a.legend();save(21,f,'F2etaP/v; chorro axial uniforme eta.6','Mayor velocidad requiere menor empuje a potencia fija. La comparación mantiene idéntica definición de rendimiento.')
f,a=canvas('Calentamiento electrotérmico idealizado');m=np.linspace(.2,2,200);a.plot(m,.7*1000/(m/1000*2000),c=B);a.set(xlabel='Caudal (g/s)',ylabel='Aumento de temperatura (K)');a.text(1,1300,'P = 1 kW; ηh = 0.70\ncp = 2000 J/(kg K)');save(22,f,'DeltaT etaP/mdcp; propiedades constantes sin disociación','Aumento térmico de un gas académico. La curva no se extrapola a temperaturas donde cambien composición y propiedades.')
f,ax=plt.subplots(1,2,figsize=(8,4.2),layout='constrained')
for a,title in zip(ax,['Iónico de rejillas','Hall']):a.axis('off');a.set(xlim=(0,5),ylim=(0,5));a.set_title(title)
box(ax[0],.2,1.5,2.1,2,'Fuente de\nplasma');ax[0].plot([2.6,2.6],[1.3,3.7],c=G,lw=3);ax[0].plot([3,3],[1.3,3.7],c=G,lw=3);arrow(ax[0],(3.1,2.5),(4.8,2.5),'Iones');ax[0].text(2.8,.8,'Rejillas; campo E',ha='center',fontsize=9)
box(ax[1],.2,1.5,3.0,2,'Plasma\ne⁻ magnetizados');arrow(ax[1],(2.8,2.5),(4.8,2.5),'E, iones',C);ax[1].text(1.7,4,'B transversal',ha='center');ax[1].text(2.4,.5,'Geometrías funcionales sin escala',ha='center',fontsize=8)
save(23,f,'Ambos aceleraniones porE; Hall Borganizaelectrones','Dos formas de sostener aceleración electrostática. El esquema distingue el papel del campo magnético y no representa una geometría de construcción.')
f,a=canvas('Impulso pulsado y fuerza media');t=np.linspace(0,4,2001);signal=np.where((t%1)<.08,1.,0.);a.plot(t,signal,c=B,label='Pulso rectangular ideal');a.axhline(.08,c=G,ls='--',label='Media de periodo');a.set(xlabel='Tiempo / periodo',ylabel='Fuerza / fuerza de pulso',ylim=(-.05,1.2));a.legend();save(24,f,'Pulso rectangular duración.08periodo; Fmedia.08Fmax','La fuerza media reproduce el impulso por periodo. La forma rectangular es ilustrativa y no una señal de ensayo.')
f,a=canvas('Capacidad ideal y relación de masas');ratio=np.linspace(1,10,200);a.plot(ratio,np.log(ratio),c=B);a.set(xlabel='m₀/mf',ylabel='Δv ideal / c');save(25,f,'Tsiolkovski sinfuerzasexternas cconstante','Ganancia logarítmica del modelo ideal. No representa velocidad orbital alcanzada desde una superficie.')
f,a=canvas('Dos etapas: masa presente en cada evento');names=['Inicio 1','Fin combustión 1','Tras separación 1','Fin combustión 2'];s1,p1,s2,p2,L=120,580,45,180,75;data=np.array([[s1,p1,s2,p2,L],[s1,0,s2,p2,L],[0,0,s2,p2,L],[0,0,s2,0,L]])
bottom=np.zeros(4)
for j,(lab,col) in enumerate(zip(['Seca 1','Propulsante 1','Seca 2','Propulsante 2','Carga'],[B,C,G,P,'#899aa8'])):a.bar(names,data[:,j],bottom=bottom,label=lab,color=col);bottom+=data[:,j]
a.set(ylabel='Masa (kg)');a.tick_params(axis='x',labelsize=8);a.legend(fontsize=8,ncol=3);save(26,f,'s1120,p1580,s245,p2180,L75kg; sinimpulsoseparación','La masa seca permanece hasta el final de su combustión. Separarla no produce un salto de velocidad en el modelo ideal.')
f,a=canvas('Ascenso vertical: capacidad ideal y gravedad');t=np.linspace(0,60,250);m0=400;md=2;c=2400;dv=c*np.log(m0/(m0-md*t));a.plot(t,dv,c=B,label='Integral propulsiva ideal');a.plot(t,dv-9.80665*t,c=C,label='Cambio de velocidad con g fija');a.set(xlabel='Tiempo (s)',ylabel='Incremento de velocidad (m/s)');a.legend();save(27,f,'c2400,m0400kg,md2kg/s,g9.80665; sinresistencia; F4800N>initialweight3923N','Solución de ecuación vertical con gravedad constante, sin suelo ni resistencia. El empuje inicial supera el peso; el modelo no incluye atmósfera ni variación de gravedad.')
f,a=schematic('Navegación, guiado y control');names=['Sensores\ny estimación','Guiado:\nreferencia','Control:\nactuación','Vehículo:\ndinámica']
for i,n in enumerate(names):
 box(a,.15+i*2.5,2.4,2.15,1.3,n)
 if i<3:arrow(a,(2.3+i*2.5,3.05),(2.65+i*2.5,3.05))
a.plot([8.8,8.8,1.2,1.2],[2.4,1.3,1.3,2.4],c=C);a.text(5,.8,'Realimentación de estado y medidas',ha='center',color=C);a.text(5,4.6,'Funciones distintas, acopladas por dinámica e incertidumbre',ha='center');save(28,f,'Diagrama funcional de lazo; sinleyvuelo','El objetivo de misión, la estimación del estado y la autoridad de actuación deben ser compatibles. Es un esquema conceptual de funciones.')
# Portada vectorial provisional, misma composición de la colección Studium.
f=plt.figure(figsize=(8.2677,11.6929),facecolor='#142c40');a=f.add_axes([0,0,1,1]);a.set(xlim=(0,1),ylim=(0,1));a.axis('off')
for i in range(24):
 x=np.linspace(0,1,300);y=.25+i*.018+.07*np.sin(5*x+i*.12);a.plot(x,y,c='#00b8cd',alpha=.10+i*.01,lw=.8)
x=np.linspace(.12,.9,300);radius=.035+.16*((x-.35)/.55)**2;a.plot(x,.56+radius,c='white',lw=3);a.plot(x,.56-radius,c='white',lw=3)
for z in np.linspace(-.025,.025,7):a.plot(x,.56+z*(1+8*np.maximum(x-.35,0)),c='#00b8cd',lw=1.3,alpha=.65)
a.add_patch(Circle((.73,.79),.15,fill=False,ec='#487086',lw=.8));a.text(.12,.17,'',color='white');f.savefig(O/'cover-art.pdf',facecolor='#142c40');plt.close(f)
(R/'evidence/figures.json').write_text(json.dumps(META,ensure_ascii=False,indent=2));print(len(META),'figuras originales')
