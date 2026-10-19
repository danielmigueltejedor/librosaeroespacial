"""Figuras originales académicas. Valores sintéticos, sin datos de motores reales."""
from pathlib import Path
import sys,json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle,FancyBboxPatch
R=Path(__file__).resolve().parents[1]
OUT=R/'figures';OUT.mkdir(exist_ok=True)
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10,'axes.spines.top':False,'axes.spines.right':False,'axes.labelsize':10,'pdf.fonttype':42,'savefig.bbox':'tight'})
B='#184a82';C='#00a5bc';O='#aa671a';P='#653389';G='#277144';L='#e8f0fa'
META=[]
def save(key,fig,scope):
 fig.tight_layout();fig.savefig(OUT/(key+'.pdf'));fig.savefig(OUT/(key+'.png'),dpi=140);plt.close(fig);META.append({'key':key,'scope':scope,'source':'scripts/figures.py'})
def flow(key,labels,scope,cycle=False):
 fig,ax=plt.subplots(figsize=(8,1.35 if len(labels)<=5 else 3.0));ax.set(xlim=(-1.5,9.5),ylim=(.95,2.65) if len(labels)<=5 else (-.5,3.7));ax.axis('off')
 n=len(labels)
 if n<=5:positions=[(i*8/(n-1),1.8) for i in range(n)];width=1.45
 else:positions=[(0,2.8),(3.9,2.8),(7.8,2.8),(7.8,.4),(3.9,.4),(0,.4)];width=2.4
 for i,(txt,(x,y)) in enumerate(zip(labels,positions)):
  ax.add_patch(FancyBboxPatch((x-width/2,y-.6),width,1.2,boxstyle='round,pad=.05',edgecolor=B,facecolor=L));ax.text(x,y,txt,ha='center',va='center',fontsize=8)
  if i:
   px,py=positions[i-1]
   if py==y:sgn=np.sign(x-px);start=(px+sgn*(width/2+.08),py);end=(x-sgn*(width/2+.08),y)
   else:start=(px,py-.7);end=(x,y+.7)
   ax.annotate('',end,start,arrowprops={'arrowstyle':'->','color':B,'lw':1.5})
 if cycle and n==6:ax.annotate('',(0,2.1),(0,1.1),arrowprops={'arrowstyle':'->','color':B,'lw':1.5})
 save(key,fig,scope)
flow('cadena-material',['Proceso\ny tratamiento','Microestructura\ny defectos','Propiedades\ny dispersión','Respuesta\nen servicio','Seguimiento\ny revisión'],'Mapa conceptual, no ley causal determinista.')
fig,ax=plt.subplots(figsize=(7,3.4));x=np.array([0,.003,.012,.05,.11,.16,.2]);y=np.array([0,210,245,305,350,330,280]);ax.plot(x,y,color=B,lw=2,label='Carga: ejemplo sintético');ax.plot([.105,.105-345/70000],[345,0],color=O,ls='--',lw=1.8,label='Descarga elástica ideal');ax.set(xlabel='Deformación ingenieril e (−)',ylabel='Tensión ingenieril s (MPa)',xlim=(0,.21),ylim=(0,390));ax.annotate('Estricción\n(esquema)',(.16,330),(.14,390),arrowprops={'arrowstyle':'->','color':B},ha='center');ax.legend(loc='lower right',fontsize=9);save('tension-deformacion',fig,'Curva sintética, descarga con E=70 GPa; no material concreto.')
fig,axs=plt.subplots(1,4,figsize=(9,2.5))
for i,ax in enumerate(axs):
 ax.set(xlim=(-1.3,1.3),ylim=(-1.3,1.3));ax.axis('off');ax.set_aspect('equal')
 if i<3:
  ax.add_patch(Rectangle((-1,-1),2,.9,facecolor=L,edgecolor=B));ax.add_patch(Rectangle((-1,.1),2,.9,facecolor=L,edgecolor=B))
  if i==0:
   for v in [-1,1]:ax.annotate('',(.0,v*1.27),(.0,v*.65),arrowprops={'arrowstyle':'->','color':O,'lw':2})
  elif i==1:
   ax.annotate('',(1.2,.55),(.3,.55),arrowprops={'arrowstyle':'->','color':O,'lw':2});ax.annotate('',(-1.2,-.55),(-.3,-.55),arrowprops={'arrowstyle':'->','color':O,'lw':2})
  else:ax.text(0,.55,'⊙',fontsize=28,ha='center',va='center',color=O);ax.text(0,-.55,'⊗',fontsize=28,ha='center',va='center',color=O)
  ax.set_title(['I · Apertura','II · Deslizamiento','III · Desgarro'][i],fontsize=10)
 else:
  ax.add_patch(Rectangle((-1,-1),2,2,facecolor='white',edgecolor=B));ax.plot([-.65,.65],[0,0],color='black',lw=3);ax.annotate('',(.65,-.35),(-.65,-.35),arrowprops={'arrowstyle':'<->','color':O});ax.text(0,-.68,'2a',ha='center');ax.set_title('Grieta central',fontsize=10)
save('modos-grieta',fig,'Representación cinemática; símbolos de salida y entrada fuera del plano en modo III.')
a=np.linspace(.0001,.015,300);fig,ax=plt.subplots(figsize=(7,3));ax.plot(a*1000,180*np.sqrt(np.pi*a),color=B,label=r'$K_I=180\sqrt{\pi a}$');ax.axhline(32,color=O,ls='--',label=r'$K_{IC}=32$');ac=(32/180)**2/np.pi;ax.scatter([ac*1000],[32],color=P);ax.axvline(ac*1000,color=P,ls=':',lw=1);ax.set(xlabel='Semilongitud a (mm)',ylabel=r'Intensidad ($\mathrm{MPa\sqrt{m}}$)',ylim=(0,43));ax.legend();save('fractura-critica',fig,'MFEL, placa ancha, Y=1, tensión remota180MPa. Tenacidad ficticia32MPa√m.')
t=np.linspace(0,2,500);fig,ax=plt.subplots(figsize=(7,2.8));ax.plot(t,120+100*np.sin(2*np.pi*t),color=B);ax.axhline(120,color=O,ls='--',label=r'$\sigma_m=120$ MPa');ax.axhline(220,color='gray',lw=.8);ax.axhline(20,color='gray',lw=.8);ax.annotate('',(.25,220),(.25,120),arrowprops={'arrowstyle':'<->','color':P});ax.text(.29,170,r'$\sigma_a=100$ MPa',color=P);ax.set(xlabel='Tiempo ilustrativo (s)',ylabel='Tensión (MPa)',ylim=(-10,260));ax.legend(loc='lower right');save('ciclo-fatiga',fig,'Historia sintética sinusoidal, máximo220mínimo20MPa, frecuencia1Hz.')
fig,axs=plt.subplots(1,2,figsize=(8,3));N=np.logspace(3,7,200);axs[0].loglog(N,600*(N/1e3)**(-.12),color=B);axs[0].set(xlabel='Ciclos N (−)',ylabel='Amplitud ilustrativa (MPa)',title='Tramo S–N sintético');dk=np.logspace(.6,1.7,200);axs[1].loglog(dk,1e-12*dk**3,color=O,lw=2);axs[1].set(xlabel=r'$\Delta K$ ($\mathrm{MPa\sqrt{m}}$)',ylabel='da/dN (m/ciclo)',title='Tramo de Paris: m=3');save('sn-paris',fig,'Modelos sintéticos de tramos ajustados; no se representa umbral ni inestabilidad como ley de Paris.')
t=np.linspace(0,1.1,300);eps=.003+.01*(1-np.exp(-10*t))+.012*t+.02*t**7;fig,ax=plt.subplots(figsize=(7,3));ax.plot(t,eps,color=B,lw=2);ax.axvspan(0,.2,color=C,alpha=.09);ax.axvspan(.2,.6,color=G,alpha=.08);ax.axvspan(.6,1.1,color=O,alpha=.08);ax.set(xlabel='Tiempo normalizado (−)',ylabel='Deformación ilustrativa (−)',xlim=(0,1.1));ax.text(.08,.05,'Primaria',fontsize=9);ax.text(.32,.05,'Casi estacionaria',fontsize=9);ax.text(.82,.05,'Terciaria',fontsize=9);save('fluencia-curva',fig,'Curva sintética con evolución de tasa; no ajustada a una aleación ni a un tiempo de rotura.')
flow('corrosion',['Ánodo\nOxidación','Electrolito\nTransporte iónico','Cátodo\nReducción'],'Mapa de funciones electroquímicas; se necesita también continuidad electrónica. No representa una velocidad.')
fig,axs=plt.subplots(1,2,figsize=(8,3));axs[0].plot([0,1,3,3.2,4,5,8,9],[20,500,500,20,20,180,180,20],color=B);axs[0].set(xlabel='Tiempo (escala ilustrativa)',ylabel='Temperatura (°C)',title='Historia ficticia');axs[0].text(1.4,400,'Solubilización',fontsize=8);axs[0].text(5,220,'Maduración',fontsize=8);u=np.linspace(0,10,100);axs[1].plot(u,100+220*(u/3)*np.exp(1-u/3),color=O);axs[1].set(xlabel='Tiempo de maduración (ilustrativo)',ylabel='Resistencia (escala ilustrativa)',title='Máximo y sobreenvejecimiento');save('tratamiento-termico',fig,'Historia y respuesta sintéticas. No receta de fabricación ni predicción de una aleación real.')
fig,axs=plt.subplots(1,2,figsize=(8,3));
for i,(ori,col) in enumerate(zip([0,90,90,0],[B,C,C,B])):
 axs[0].add_patch(Rectangle((0,i*.5),4,.45,facecolor=col,alpha=.7));axs[0].text(4.2,i*.5+.2,str(ori)+'°',va='center')
axs[0].axhline(.975,color=O,ls='--');axs[0].set(xlim=(-.2,5.5),ylim=(-.3,2.2),title='Apilado simétrico [0/90]s');axs[0].axis('off')
for y,h,c,lab in [(0,.2,B,'Cara'),(.2,1.4,L,'Núcleo'),(1.6,.2,B,'Cara')]:
 axs[1].add_patch(Rectangle((0,y),4,h,facecolor=c,edgecolor=B));axs[1].text(4.2,y+h/2,lab,va='center')
axs[1].set(xlim=(-.2,5.5),ylim=(-.3,2.2),title='Sándwich (esquema)');axs[1].axis('off');save('laminados',fig,'Secuencias y sección conceptual; no representa dimensiones ni un producto real.')
flow('motor-materiales',['Fan\nTi / compuesto','Compresor\nTi / Ni\nsegún zona','Combustión\nSuperaleación','Turbina\nNi / CMC\nsegún pieza','Carcasas\nSegún función'],'Tendencias de familias y posición; no especificación de material de un motor particular.')
flow('estrategias',['Función\nrequerida','Modo de\nfallo','Consecuencia\ny riesgo','Evidencia\ndetectable','Tarea\ny revisión'],'Secuencia de razonamiento; no árbol reglamentario de aprobación.')
flow('certificacion',['Base y\nrequisito','Medio de\ncumplimiento','Evidencia\ny revisión','Configuración\ncontrolada','Instrucciones\ny seguimiento'],'Mapa conceptual de trazabilidad de certificación; no procedimiento exhaustivo.')
flow('revision-arc',['Documentos\ny configuración','Examen físico\ny registros','Coherencia\ny discrepancias','Resultado\nsegún requisitos'],'Mapa académico; no automatiza ARC y no omite condiciones del texto legal.')
flow('programa',['Fuentes\ny revisiones','Aplicabilidad\ny configuración','Tareas\ne intervalos','Ejecución\ny hallazgos','Registros\ny control','Revisión\ndel programa'],'Ciclo conceptual de mantenimiento, no AMP aprobado.',True)
flow('parte145',['Alcance\naprobado','Planificación\ny recursos','Datos\naplicables','Ejecución\ny comprobación','Certificación\ny registros'],'Funciones dentro de una organización, no condición suficiente para certificación.')
flow('flujo-ad',['Identidad\ny estado','Aplicabilidad\ncon evidencia','Acciones\ny plazos','Ejecución\ndocumentada','Estado\ny repetición'],'Secuencia académica de lectura; los datos faltantes mantienen pendiente el análisis.')
flow('monitorizacion',['Condiciones\nde medida','Señal\ny tendencia','Hipótesis\nde daño','Corroboración\ne inspección','Acción\ny verificación'],'Secuencia de diagnóstico; una señal no implica un diagnóstico único.')
flow('logistica',['Demanda\nde tareas','Recursos\ny repuestos','Ejecución\ny pruebas','Certificación\ny cierre','Revisión\nde tiempos'],'Mapa de recursos y dependencias; sin probabilidades reales.')
flow('control-academico',['Entradas\ne identidad','Historial\nde eventos','Cálculos\ny márgenes','Pendientes\ny alertas','Revisión\nhumana'],'Arquitectura del modelo académico; no herramienta operacional aprobada.')
# Equilibrio binario isomorfo esquemático.
x=np.linspace(0,1,400);base=700+300*x;li=base+60*np.sin(np.pi*x);so=base-60*np.sin(np.pi*x);fig,ax=plt.subplots(figsize=(7,3.3));ax.plot(x,li,color=B,label='Liquidus');ax.plot(x,so,color=O,label='Solidus');ax.fill_between(x,so,li,color=L);ax.text(.25,970,'Líquido');ax.text(.57,740,'Sólido α');ax.text(.45,850,'L + α');ax.set(xlabel='Fracción de B (escala esquemática)',ylabel='Temperatura (escala ilustrativa)',xlim=(0,1));ax.legend(loc='upper left');save('diagrama-fases',fig,'Diagrama binario isomorfo esquemático; no datos de un sistema real.')
# Crecimiento analítico m=3.
C0=1e-12;ds=100.;Y=1.;ai=.001;af=.008;k=C0*(Y*ds*np.sqrt(np.pi))**3;Nf=2*(ai**(-.5)-af**(-.5))/k;Nv=np.linspace(0,Nf,300);a=(ai**(-.5)-k*Nv/2)**(-2);fig,ax=plt.subplots(figsize=(7,3));ax.plot(Nv/1e6,a*1000,color=B);ax.set(xlabel='Ciclos acumulados (millones)',ylabel='Semilongitud a (mm)');save('crecimiento-grieta',fig,'Ley de Paris m3, C=1e-12m/ciclo/(MPa√m)^3, rango100MPa,Y1; no iniciación ni umbral.')
# Señal ultrasónica sintética.
us=np.linspace(0,18,1400);sig=sum(v*np.exp(-((us-pos)/.16)**2) for pos,v in [(0,1),(2*.02/5900*1e6,.55),(2*.04/5900*1e6,.8)]);fig,ax=plt.subplots(figsize=(7,3));ax.plot(us,sig,color=B);ax.set(xlabel='Tiempo de vuelo (μs)',ylabel='Amplitud normalizada',xlim=(-.5,18));ax.text(6.8,.63,'Eco de reflector',ha='center');ax.text(13.56,.88,'Eco de fondo',ha='center');save('ultrasonidos',fig,'Señal sintética pulso-eco: velocidad5900m/s, reflector20mm, fondo40mm. No umbral de detección.')
(R/'evidence/figures.json').write_text(json.dumps(META,ensure_ascii=False,indent=2))
print(len(META),'figuras generadas')
