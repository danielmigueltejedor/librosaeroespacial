"""Figuras vectoriales originales. Todos los datos son modelos docentes SI."""
from pathlib import Path
import os
import json, math
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon,Rectangle,Circle,FancyArrowPatch,Arc
from physics import isa,drag
ROOT=Path(__file__).resolve().parents[1]; OUT=ROOT/'figures';OUT.mkdir(exist_ok=True)
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10,'axes.spines.top':False,'axes.spines.right':False,'axes.labelcolor':'#1c283a','text.color':'#1c283a','axes.titleweight':'bold','pdf.fonttype':42,'savefig.facecolor':'white'})
BLUE='#184a82';GOLD='#c39143';TEAL='#18786f';RED='#a94343';META=[]
def canvas(title):
 f,a=plt.subplots(figsize=(7.2,4.1),layout='constrained');a.set_title(title,pad=14);return f,a
def save(key,f,model):
 if not os.environ.get('STUDIUM_FIGURES') or key in os.environ['STUDIUM_FIGURES'].split(','):
  f.savefig(OUT/(key+'.pdf'));f.savefig(OUT/(key+'.svg'));f.savefig(OUT/(key+'.png'),dpi=160)
 plt.close(f);META.append({'key':key,'original':True,'model':model,'formats':['pdf','svg','png']})
def schematic(title):
 f,a=canvas(title);a.set(xlim=(0,10),ylim=(0,5));a.axis('off');return f,a
def box(a,x,y,w,h,text,color=BLUE):
 a.add_patch(Rectangle((x,y),w,h,facecolor='#edf2f7',edgecolor=color,lw=1.5));a.text(x+w/2,y+h/2,text,ha='center',va='center',fontsize=9)
def arrow(a,p,q,text='',color=BLUE):
 a.annotate('',xy=q,xytext=p,arrowprops={'arrowstyle':'->','lw':1.8,'color':color})
 if text:
  vertical=abs(q[0]-p[0])<.2*abs(q[1]-p[1]);a.annotate(text,((p[0]+q[0])/2,(p[1]+q[1])/2),xytext=(8,0) if vertical else (0,7),textcoords='offset points',ha='left' if vertical else 'center',va='center' if vertical else 'bottom',fontsize=9,color=color,bbox={'facecolor':'white','edgecolor':'none','pad':.5})
def blocks(key,title,names,model):
 f,a=schematic(title);n=len(names);w=8.8/n-.25
 for i,name in enumerate(names):
  x=.5+i*8.8/n;box(a,x,2,w,1,name)
  if i<n-1:arrow(a,(x+w,2.5),(x+8.8/n,2.5))
 if key=='jet':
  a.plot([3.1,6.8],[1.65,1.65],color=GOLD,lw=2);arrow(a,(6.8,1.65),(3.1,1.65),'Eje: turbina → compresor',GOLD)
 if key=='hydraulic':
  a.plot([9,9,.9,.9],[2,1.4,1.4,2],color=TEAL,lw=1.5);arrow(a,(7,1.4),(4,1.4),'Retorno al depósito',TEAL)
 a.text(5,.65,'Esquema funcional; geometría sin escala',ha='center',fontsize=9)
 save(key,f,model)
f,a=schematic('Arquitectura de una aeronave de ala fija')
a.add_patch(Polygon([(5,4.7),(5.35,3.9),(5.35,.7),(5,.3),(4.65,.7),(4.65,3.9)],fc='#dbe5ef',ec=BLUE))
a.add_patch(Polygon([(4.65,3.0),(.5,1.9),(.7,1.55),(4.65,2.1),(5.35,2.1),(9.3,1.55),(9.5,1.9),(5.35,3.0)],fc='#dbe5ef',ec=BLUE))
a.add_patch(Polygon([(4.65,1.25),(3,.6),(3,.35),(5,.75),(7,.35),(7,.6),(5.35,1.25)],fc='#dbe5ef',ec=BLUE))
for xx in [3.5,6.1]:a.add_patch(Rectangle((xx,2.15),.4,1.0,fc='#adc4d8',ec=BLUE))
for p,q,t in [((5.1,3.7),(7.2,4.3),'Fuselaje'),((7,2.1),(8.5,3.3),'Ala'),((6.2,.65),(8,.7),'Empenaje'),((3.7,2.9),(2.2,3.7),'Grupo propulsor')]:a.annotate(t,p,xytext=q,ha='center',arrowprops={'arrowstyle':'->','color':BLUE},fontsize=9,bbox={'facecolor':'white','edgecolor':'none','pad':1})
a.text(5,.05,'Vista superior; sin escala',fontsize=9,ha='center',bbox={'facecolor':'white','edgecolor':'none','pad':1});save('aircraft',f,'Geometría conceptual, sin valores aeronave real')
f,ax=plt.subplots(1,3,figsize=(7.5,4.1),layout='constrained');h=np.linspace(0,20000,401);vals=[isa(x) for x in h]
for a,k,label in zip(ax,['T','p','rho'],['Temperatura (K)','Presión (kPa)','Densidad (kg/m³)']):
 y=np.array([v[k] for v in vals]);y=y/1000 if k=='p' else y;a.plot(y,h/1000,c=BLUE);a.set(xlabel=label,ylabel='H geopotencial (km)');a.axhline(11,ls='--',color=GOLD);a.grid(alpha=.2)
f.suptitle('Atmósfera estándar seca: 0–20 km');save('isa',f,'ISA por tramos, g0=9.80665, R=287.05287, L=-0.0065 K/m hasta 11 km, 216.65 K hasta 20 km')
f,a=schematic('Presión estática y presión de remanso')
a.plot([2,5.2,5.2],[3.2,3.2,1.8],c=BLUE,lw=3);a.plot([2,4.9,4.9],[2.9,2.9,1.8],c=BLUE,lw=3);a.plot([6.2,6.2],[3.5,1.8],c=TEAL,lw=2);a.plot([6,6.4],[3.5,3.5],c=TEAL,lw=2)
arrow(a,(.2,3),(1.5,3),'V');box(a,4.8,.5,2,1,'Diferencial\npt − p');a.text(2.4,3.6,'Toma frontal: pt');a.text(7.3,3.4,'Toma estática: p');arrow(a,(7.4,3.15),(6.25,3.45));a.text(5,.1,'El esquema separa funciones; sin escala.',ha='center',fontsize=9);save('pitot',f,'Frontal alineada con flujo, sin pérdidas de línea; modelo subsónico isentrópico o incompresible según M')
f,a=canvas('Envolvente de perturbaciones: cono de Mach');Ma=2.;u=math.asin(1/Ma)
for tau in [.35,.7,1.05,1.4]:a.add_patch(Circle((-Ma*tau,0),tau,fill=False,ec='#9baebf',lw=.8))
a.plot([0,-3],[0,3*math.tan(u)],c=BLUE);a.plot([0,-3],[0,-3*math.tan(u)],c=BLUE);arrow(a,(0,0),(1,0),'V');a.scatter([0],[0],c=RED);a.text(-1.2,1.65,r'$\mu=\arcsin(1/M)=30^\circ$',ha='center',bbox={'facecolor':'white','edgecolor':'none','pad':1});a.set(xlim=(-4.5,1.3),ylim=(-1.9,1.9),xlabel='x / (a·1 s)',ylabel='y / (a·1 s)',aspect='equal');a.grid(alpha=.15);save('mach',f,'M=2 constante; círculos acústicos en instantes anteriores, frente infinitesimal, no choque finito')
f,a=canvas('Perfil simétrico educativo y capa límite');x=np.linspace(0,1,301);yt=.6*(.2969*np.sqrt(x)-.126*x-.3516*x*x+.2843*x**3-.1036*x**4);a.fill_between(x,-yt,yt,color='#dbe5ef',edgecolor=BLUE);a.plot([0,1],[0,0],'--',c=GOLD);a.set(xlabel='x / c',ylabel='y / c',ylim=(-.2,.25),aspect='equal');a.annotate('Borde de ataque',xy=(0,0),xytext=(.05,.15),arrowprops={'arrowstyle':'->'});a.annotate('Cuerda',xy=(.65,0),xytext=(.65,-.15),arrowprops={'arrowstyle':'->'});save('airfoil',f,'Familia NACA simétrica educativa 12% con borde cerrado; no datos de sustentación medidos')
f,a=canvas('Capa límite: condición de no deslizamiento');eta=np.linspace(0,1,150);u=1.5*eta-.5*eta**3;a.plot(u,eta,c=BLUE,lw=2);a.plot([0,1.2],[0,0],lw=3,c='k');a.axvline(1,color=GOLD,ls='--');a.set(xlabel='u / U exterior',ylabel='y / δ',xlim=(-.05,1.25),ylim=(0,1.15));a.text(.15,.8,'Perfil ilustrativo\nno solución universal');a.grid(alpha=.2);save('boundary',f,'Perfil cúbico pedagógico con u(0)=0, u(δ)=U y du/dy(δ)=0; no ley de pared calibrada')
f,a=canvas('Ala trapezoidal: magnitudes geométricas');b=12;cr=2.5;ct=1.1;a.add_patch(Polygon([(-6,1.2),(-6,1.2+ct),(0,cr),(6,1.2+ct),(6,1.2),(0,0)],fc='#dbe5ef',ec=BLUE));a.set(xlim=(-7,7),xlabel='Coordenada transversal y (m)',ylabel='Coordenada longitudinal x (m)',aspect='equal',ylim=(-1,4));a.annotate('',xy=(6,-.5),xytext=(-6,-.5),arrowprops={'arrowstyle':'<->'});a.text(0,-.8,'b = 12 m',ha='center');a.text(.2,1,'cr = 2.5 m');a.text(4,3,'ct = 1.1 m');save('wing',f,'Ala de ejemplo b12m cr2.5m ct1.1m; S=b(cr+ct)/2, no corresponde a aeronave real')
f,a=canvas('Polar parabólica y resistencia inducida');CL=np.linspace(-1.3,1.3,200);cd0=.025;ei=.9;ar=8;kp=.008;ki=1/(np.pi*ei*ar);a.plot(CL,cd0+(ki+kp)*CL**2,c=BLUE,label='CD total');a.plot(CL,ki*CL**2,c=TEAL,label='CD inducido');a.plot(CL,cd0+kp*CL**2,c=GOLD,label='CD perfil y parásito');a.set(xlabel='CL (adimensional)',ylabel='CD (adimensional)');a.legend();a.grid(alpha=.2);save('polar',f,'CD0=.025; AR8; ei=.9; kp=.008; eO=1/[pi AR(ki+kp)] distinto ei; no correlación experimental')
f,a=canvas('Pendiente de perfil y pendiente del ala');al=np.linspace(-5,12,100);a0=2*np.pi;aw=a0/(1+a0/(np.pi*.9*8));a.plot(al,a0*np.deg2rad(al+2),label='Perfil: a0 = 2π rad⁻¹',c=BLUE);a.plot(al,aw*np.deg2rad(al+2),label='Ala finita: AR=8, ei=0.9',c=TEAL);a.set(xlabel='Ángulo de ataque α (grados)',ylabel='Coeficiente de sustentación (adimensional)');a.legend();a.grid(alpha=.2);save('liftcurve',f,'Modelo lineal sin pérdida, alpha0=-2°; no extrapolar hasta CLmax')
f,a=canvas('Resistencia necesaria en vuelo horizontal');vv=np.linspace(32,150,300);rho=1.0;W=42000.;S=22.;cd0=.026;K=.052;q=.5*rho*vv**2;pa=q*S*cd0;qd=K*W**2/(q*S);a.plot(vv,pa/1000,c=GOLD,label='Parásita');a.plot(vv,qd/1000,c=TEAL,label='Cuadrática total');a.plot(vv,(pa+qd)/1000,c=BLUE,label='Total');a.set(xlabel='TAS (m/s)',ylabel='Resistencia (kN)',ylim=(0,9));a.legend();a.grid(alpha=.2);save('drag',f,'rho1 W42kN S22 CD0.026 K.052; L=W; polar docente limitada a rama adherida')
f,a=canvas('Empuje disponible y necesario');a.plot(vv,(pa+qd)/1000,c=BLUE,label='T necesario = D');a.axhline(4,c=RED,label='T disponible = 4 kN');a.set(xlabel='TAS (m/s)',ylabel='Empuje (kN)',ylim=(0,9));a.legend();a.grid(alpha=.2);save('thrust',f,'Mismos datos figura drag; empuje disponible constante idealizado; raíces matemáticas sujetas a CLmax/Mach')
f,a=canvas('Estabilidad estática longitudinal');alpha=np.linspace(-4,12,80);a.plot(alpha,.05-.012*alpha,c=BLUE,label='Estable: Cmα < 0');a.plot(alpha,-.05+.012*alpha,c=RED,label='Inestable: Cmα > 0');a.axhline(0,c='gray',lw=.7);a.set(xlabel='α (grados)',ylabel='Cm alrededor del CG');a.legend();a.grid(alpha=.2);save('stability',f,'Pendientes docentes por grado; estabilidad local, no prueba estabilidad dinámica')
f,a=schematic('Aeropuerto: relación entre áreas funcionales');box(a,.4,3.5,9.2,.5,'Pista 09 / 27',color=TEAL);box(a,1,2.7,8,.25,'Calle de rodaje',color=TEAL);arrow(a,(2,3.5),(2,2.95));arrow(a,(8,3.5),(8,2.95));box(a,3,1.6,4,.7,'Plataforma');arrow(a,(5,2.7),(5,2.3));box(a,3,.4,4,.7,'Terminal y acceso terrestre');arrow(a,(5,1.6),(5,1.1));a.text(.4,.3,'Sin escala; pista ficticia',fontsize=8);save('airport',f,'Designación conceptual 09/27 aproximadamente magnética este/oeste; no plano normativo')
f,a=canvas('Triángulo vectorial de velocidades');arrow(a,(0,0),(160,0),'Va');arrow(a,(160,0),(140,35),'Viento');arrow(a,(0,0),(140,35),'Vg',TEAL);a.set(xlim=(-10,185),ylim=(-15,60),xlabel='Componente Este (m/s)',ylabel='Componente Norte (m/s)',aspect='equal');a.grid(alpha=.2);save('wind',f,'Va=(160,0), viento=(-20,35) m/s; Vg=Va+viento, no rumbos meteorológicos')
f,a=canvas('Órbita elíptica y foco gravitatorio');th=np.linspace(0,2*np.pi,400);ecc=.4;aa=10;rr=aa*(1-ecc*ecc)/(1+ecc*np.cos(th));a.plot(rr*np.cos(th),rr*np.sin(th),c=BLUE);a.add_patch(Circle((0,0),1.1,fc=TEAL));a.scatter([aa*(1-ecc),-aa*(1+ecc)],[0,0],c=GOLD);a.text(aa*(1-ecc),1,'Periapsis');a.text(-aa*(1+ecc),1,'Apoapsis');a.set(xlabel='x (unidades de longitud)',ylabel='y (unidades de longitud)',aspect='equal');a.grid(alpha=.2);save('orbit',f,'Órbita dos cuerpos con a10 e.4, foco origen; cuerpo dibujado sin escala')
f,a=schematic('Ala: caminos de carga en una estructura semimonocasco');a.add_patch(Rectangle((.6,1.4),8.8,2.0,fc='#edf2f7',ec=BLUE));a.plot([.6,9.4],[1.9,1.9],lw=4,c=BLUE);a.plot([.6,9.4],[2.9,2.9],lw=4,c=BLUE)
for x in np.linspace(1,9,7):a.plot([x,x],[1.4,3.4],c=GOLD,lw=2)
a.text(5,4,'Largueros: flexión / cortante',ha='center');a.text(5,.7,'Costillas: forma y transferencia de carga\nRevestimiento: cortante y parte de flexión',ha='center');save('structure',f,'Esquema conceptual de cajón alar; sin análisis de tensiones ni escala')
f,a=canvas('Selección: índices específicos de materiales docentes');names=['Aluminio','Titanio','Acero','Compuesto UD'];dens=np.array([2780,4430,7850,1600]);E=np.array([72,110,210,130])*1e9;sig=np.array([350,830,800,1000])*1e6;a.scatter(E/dens/1e6,sig/dens/1e3,c=[BLUE,GOLD,RED,TEAL],s=70)
for x,y,t in zip(E/dens/1e6,sig/dens/1e3,names):a.annotate(t,(x,y),xytext=(5,5),textcoords='offset points',fontsize=9)
a.set(xlabel='E/ρ (10⁶ m²/s²)',ylabel='σ/ρ (10³ m²/s²)',xlim=(20,100),ylim=(0,750));a.grid(alpha=.2);save('materials',f,'Valores ilustrativos, no allowables ni equivalencias certificados; UD en dirección de fibra')
f,a=canvas('Ciclo Otto ideal en el plano p–v');ga=1.4;rc=8;v1=1.;v2=v1/rc;p1=1.;p2=p1*rc**ga;p3=2.4*p2;p4=p3/rc**ga;v=np.linspace(v2,v1,200);a.plot(v,p1*(v1/v)**ga,c=BLUE);a.plot(v,p3*(v2/v)**ga,c=RED);a.plot([v2,v2],[p2,p3],c=GOLD);a.plot([v1,v1],[p4,p1],c=TEAL)
for xx,yy,dx,dy,col in [(.6,p1*(v1/.6)**ga,-.06,p1*(v1/.54)**ga-p1*(v1/.6)**ga,BLUE),(.4,p3*(v2/.4)**ga,.06,p3*(v2/.46)**ga-p3*(v2/.4)**ga,RED),(v2,p2*1.5,0,p2*.3,GOLD),(v1,p4*.8,0,-p4*.15,TEAL)]:a.annotate('',(xx+dx,yy+dy),(xx,yy),arrowprops={'arrowstyle':'->','color':col,'lw':1.8})
a.set(xlabel='v / v₁',ylabel='p / p₁',yscale='log');a.grid(alpha=.2);save('otto',f,'Gas perfecto gamma1.4, rc8, p3/p2=2.4; compresión/expansión isentrópicas y calor isócoro')
blocks('jet','Turborreactor: procesos y transferencia de energía',['Admisión','Compresor','Cámara\ncombustión','Turbina','Tobera'],'Esquema turborreactor; turbina acciona compresor, no toda expansión genera eje')
blocks('rocket','Cohete: masa almacenada y expansión',['Depósitos\npropulsantes','Alimentación','Cámara','Garganta','Tobera'],'Esquema cohete bipropulsante conceptual; empuje momento y presión de salida')
blocks('hydraulic','Sistema hidráulico: energía, distribución y actuación',['Depósito','Bomba','Válvula','Actuador','Retorno'],'Circuito funcional abierto gráficamente, retorno conceptual; presión no es caudal')
blocks('electric','Sistema eléctrico: fuente, protección y carga',['Generador','Regulación','Barra','Protección','Consumidor'],'Topología funcional simplificada, no arquitectura certificada')
blocks('fuel','Combustible: suministro y vigilancia',['Depósito\nventilado','Bomba','Filtro','Medición','Motor'],'Cadena de funciones; retorno, alimentación cruzada y redundancia omitidos en dibujo, discutidos texto')
f,a=schematic('Protección frente al hielo: balance energético');box(a,3,1.5,4,1.5,'Borde de ataque\nvolumen de control');arrow(a,(.5,3),(3,2.6),'Gotas');arrow(a,(5,.3),(5,1.5),'Calefacción',RED);arrow(a,(7,2.5),(9.5,2.5),'Convección');arrow(a,(6,3),(7.5,4),'Agua / evaporación');a.text(1,.5,'Sin escala; balance estacionario docente',fontsize=9);save('ice',f,'Calor aplicado compensa calentamiento/evaporación y pérdidas; sin predicción de certificación')
blocks('integration','Integración: funciones, interfaces y evidencias',['Requisito','Arquitectura','Interfaces','Ensayo','Verificación'],'Proceso de ingeniería conceptual; verificación distinta validación')
f,a=canvas('Curva cualitativa de sustentación y pérdida');alpha=np.linspace(-4,22,200);cl=np.where(alpha<=12,.1*(alpha+2),1.4-.004*(alpha-12)**2);a.plot(alpha,cl,c=BLUE,lw=2);a.axvline(12,ls='--',c=GOLD,label='Máximo ilustrativo');a.set(xlabel='Ángulo de ataque α (grados)',ylabel='CL ilustrativo (adimensional)');a.text(-2,1.2,'Curva educativa,\nsin datos experimentales');a.grid(alpha=.2);a.legend(loc='lower right');save('stall',f,'Modelo cualitativo por tramos: CL=.1(alpha+2) hasta12°, después1.4-.004(alpha-12)^2; no polar validada ni ley de pérdida universal')
f,a=schematic('Fuerzas en vuelo horizontal rectilíneo uniforme');a.add_patch(Polygon([(3,2.3),(7,2.5),(3,2.7),(4,2.5)],fc='#dbe5ef',ec=BLUE));arrow(a,(5,2.5),(5,4.5),'L',TEAL);arrow(a,(5,2.5),(5,.5),'W',RED);arrow(a,(5,2.5),(8.9,2.5),'T',BLUE);arrow(a,(5,2.5),(1.1,2.5),'D',GOLD);a.text(5,.05,'Empuje horizontal; L = W y T = D bajo equilibrio',ha='center',fontsize=10);save('forces',f,'Diagrama de cuerpo libre conceptual; fuerza aerodinámica descompuesta respecto a velocidad aérea horizontal, peso vertical')

(ROOT/'evidence').mkdir(exist_ok=True)
(ROOT/'evidence/figures.json').write_text(json.dumps(META,ensure_ascii=False,indent=2));print(len(META),'figuras originales')
