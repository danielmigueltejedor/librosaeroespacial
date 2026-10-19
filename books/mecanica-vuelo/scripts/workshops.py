"""Talleres originales autónomos del manual, distintos del cuaderno."""
from pathlib import Path
import json,math
import numpy as np
from scipy.optimize import root,brentq,minimize_scalar
from scipy.integrate import solve_ivp,quad
from scipy.linalg import expm
from models import *
from problem_bank import test,f
from render_problems import solution
RDIR=Path(__file__).resolve().parents[1];W=[]
def add(ch,title,prompt,data,frame,hyp,eqs,steps,tests,interpret,check,limits):
    W.append(dict(key=f'T{ch:02}',ch=ch,title=title,prompt=prompt,data=data,unknown='Las magnitudes y comprobaciones solicitadas en el caso.',frame=frame,hyp=hyp,model=title,eqs=eqs,steps=steps,tests=tests,interpretation=interpret,independent=check,limits=limits,level='INTERMEDIATE'))

add(1,'Elegir hipótesis antes de calcular',r'Una aeronave horizontal de 5400 kg consume 420 kg manteniendo TAS 110 m/s, densidad 0.85 kg/m³ y S=32 m². Calcule CL inicial y final y compruebe si podría mantenerse además incidencia constante con una sustentación lineal de configuración fija.',
 r'$m_i=5400\SIu{kg}$, $m_f=4980\SIu{kg}$; la polar y mando no cambian.',
 'Vuelo horizontal en calma y magnitudes aerodinámicas en viento.',
 'Sucesión cuasiestacionaria de trimas; relación CL-alpha fija para la pregunta de incidencia.',
 [r'C_L=2mg_0/(\rho V^2S)',r'C_{L,f}/C_{L,i}=m_f/m_i'],
 ['El peso inicial y final se calculan por separado.','La presión dinámica es constante porque lo son TAS y densidad.','Al disminuir peso debe disminuir CL. Con relación lineal fija, cambia incidencia; conservarla exigiría otra modificación del modelo.'],
 [test('CL inicial','2*5400*9.80665/(.85*110**2*32)'),test('CL final','2*4980*9.80665/(.85*110**2*32)'),test('Razón de CL','4980/5400')],
 'La ley de vuelo no puede fijar más magnitudes de las compatibles con el equilibrio.','Recalcular sustentación final con el CL inicial y comparar con el peso final; el exceso revela la incompatibilidad.','Un cambio de elevador puede modificar CL a incidencia fija en un modelo más completo; aquí se ha fijado expresamente la relación de sustentación.')

phi,theta,psi=np.deg2rad([18,9,32]);C=c_body_ned(phi,theta,psi);vec=np.array([96,8,-5]);rot=C@vec
add(2,'Una transformación completa de ida y vuelta',r'Construya Cbn para alabeo 18 grados, cabeceo 9 y guiñada 32. Transforme el vector NED (96,8,-5) m/s a cuerpo, vuelva a NED y compruebe norma y determinante.',
 r'Vector aéreo y ángulos Euler 3--2--1; no hay traslación del origen porque se transforma una velocidad.',
 'Matriz pasiva NED a cuerpo, vectores columna.',
 'Horizonte fijo local y ángulos fuera de singularidad de Euler.',
 [r'C_{bn}=T_1(\phi)T_2(\theta)T_3(\psi)',r'\vect v^b=C_{bn}\vect v^n,\quad\vect v^n=C_{bn}^T\vect v^b'],
 ['Se forman las tres matrices elementales con los signos pasivos.','Se multiplica en orden, empezando por guiñada a la derecha.','Se verifica la inversa por transposición y se compara con las componentes iniciales.','La norma se obtiene antes y después de la rotación y el determinante se calcula independientemente.'],
 [test('u cuerpo',f(rot[0]),'m/s'),test('v cuerpo',f(rot[1]),'m/s'),test('w cuerpo',f(rot[2]),'m/s'),test('Norma','sqrt(96**2+8**2+5**2)','m/s'),test('Determinante',f(np.linalg.det(C)))],
 'La misma velocidad tiene componentes diferentes; su módulo y el vector físico se conservan.','La multiplicación numérica se reproduce en el programa y se comprueba C transpuesta por C e ida y vuelta.','Una matriz ortogonal con otro orden de ángulos podría conservar norma y aun representar una actitud equivocada; la prueba geométrica de secuencia sigue siendo necesaria.')

add(3,'Una cizalladura de viento tiene aceleración',r'Un campo estacionario tiene viento norte U(h)=0.003h m/s. Un avión asciende a 4 m/s y mantiene velocidad aérea norte constante. Determine la aceleración norte de su velocidad terrestre y la fuerza adicional que supone para 2600 kg.',
 r'$\partial U/\partial h=0.003\SIu{s^{-1}}$, $\dot h=4\SIu{m/s}$.',
 'Componente norte local y altitud positiva hacia arriba; referencia plana.',
 'Se considera el gradiente indicado y se omiten otros cambios de viento y actitud.',
 [r'v_{g,N}=v_{a,N}+U(h)',r'\dot v_{g,N}=\dot v_{a,N}+(\dd U/\dd h)\dot h',r'\Delta F_N=m(\dd U/\dd h)\dot h'],
 ['El viento no cambia explícitamente con el reloj, pero el avión recorre su gradiente.','La derivada de viento a lo largo de la trayectoria usa hdot.','El producto por masa da el término inercial adicional; no se lo añade como fuerza aerodinámica ficticia.'],
 [test('Aceleración de viento','.003*4','m/s^2'),test('Término de fuerza','2600*.003*4','N')],
 'Mantener velocidad relativa al aire constante en cizalladura no implica velocidad terrestre constante.','Tomar dos instantes separados 10 s: h aumenta 40 m y U aumenta 0.12 m/s; dividir por tiempo recupera aceleración.','La pregunta es local y escalar; una cizalladura real puede alterar incidencia, cargas y control de modo adicional.')

pp=Polar(29,.024,.047,1.55);rho=.92;mass=5100;V=98;cl=2*mass*G/(rho*V*V*pp.S);D=pp.drag(V,mass,rho);D2=pp.drag(V,.9*mass,rho)
add(4,'Qué parte de resistencia disminuye al consumir',r'A TAS 98 m/s y densidad 0.92, un avión de 5100 kg con S=29 m² y polar 0.024+0.047CL² consume el 10 por ciento de su masa total. Calcule resistencia inicial y final manteniendo altitud y TAS.',
 r'La masa final es 4590 kg; vuelo horizontal en ambos extremos.',
 'Fuerzas en ejes viento; TAS mantenida.',
 'Polar fija; se omite variación de resistencia de trim y de centro de gravedad.',
 [r'D=A_V+B_VW^2',r'D_{parasita}=q_\infty SC_{D0}',r'D_{cuadratica,f}=0.9^2D_{cuadratica,i}'],
 ['La presión dinámica y el término parásito permanecen constantes.','La sustentación adimensional disminuye en la proporción de masa.','El término cuadrático disminuye con el cuadrado de esa proporción, no linealmente.','Se suman ambas partes para comparar la resistencia total.'],
 [test('Resistencia inicial',f(D),'N'),test('Resistencia final',f(D2),'N'),test('Reducción relativa',f(1-D2/D))],
 'Una reducción del 10 por ciento de masa no implica una reducción del 10 por ciento de resistencia total a TAS fija.','Calcular directamente CL inicial y final y evaluar la polar, contrastando con la separación A_V+B_V W².','El factor cuadrático total puede contener resistencia de perfil dependiente de sustentación; no se lo denomina inducida pura sin justificación.')

In=np.array([[9800,0,-760],[0,14800,0],[-760,0,19200]]);om=np.array([.13,.05,-.09]);mom=np.array([600,-380,420]);acc=omega_derivative(om,mom,In);power=float(om@mom)
add(5,'Dinámica y trabajo giroscópico',r'Para el tensor Ixx=9800, Iyy=14800, Izz=19200 e Ixz=760 kg m², omega=(0.13,0.05,-0.09) rad/s y momentos (600,-380,420) N m, calcule aceleraciones y tasa de energía de rotación.',
 r'El tensor usa -Ixz en entradas xz y zx y es constante en cuerpo.',
 'Cuerpo y momentos respecto al CG; producto integral Ixz positivo según dato.',
 'Sólido rígido y masa constante en el intervalo dinámico.',
 [r'I\dot{\vect\omega}=\vect M-\vect\omega\times I\vect\omega',r'\dot E_r=\vect\omega^TI\dot{\vect\omega}=\vect\omega^T\vect M'],
 ['Se calcula el momento angular antes del término giroscópico.','Se resuelve el sistema con el tensor completo.','Se evalúa la tasa de energía por dos vías: omega por M y omega por I odot.','El producto giroscópico no aporta trabajo porque es perpendicular a omega.'],
 [test('pdot',f(acc[0]),'1/s^2'),test('qdot',f(acc[1]),'1/s^2'),test('rdot',f(acc[2]),'1/s^2'),test('Tasa de energía',f(power),'W')],
 'La energía puede aumentar o disminuir según omega por M, aun cuando algunas tasas angulares tengan signo distinto.','Residuo vectorial y igualdad de las dos tasas energéticas, ejecutados con álgebra matricial.','No se interpreta un literal de aceleración como prueba del balance; las operaciones y residuos están conservados en el programa.')

mass=2450;rho=1.04;S=26;V=66;qS=.5*rho*V*V*S
def trimfun(z):
    al,de,T=z;cl=.24+5.2*al+.28*de;cd=.026+.046*cl*cl
    return [T*math.cos(al)-qS*cd,qS*cl+T*math.sin(al)-mass*G,.045-.72*al-1.08*de]
tr=root(trimfun,[.03,.02,2000]);assert tr.success
al,de,T=tr.x
add(6,'Trim no lineal con empuje en cuerpo',r'Resuelva el equilibrio de un avión a 66 m/s y rho=1.04 con empuje paralelo a cuerpo. Masa 2450 kg, S=26 m², CL=0.24+5.2alpha+0.28delta, Cm=0.045-0.72alpha-1.08delta y polar 0.026+0.046CL².',
 r'Vuelo horizontal: cabeceo theta=alpha; ángulos en radianes; límites de elevador ±0.35 rad y T entre 0 y 5000 N.',
 'Ejes viento para fuerzas y cuerpo para dirección de empuje.',
 'Modelo lineal de coeficientes, geometría exacta del empuje y momento propulsivo nulo respecto al CG.',
 [r'T\cos\alpha-D=0',r'L+T\sin\alpha-W=0',r'C_{m0}+C_{m\alpha}\alpha+C_{m\delta}\delta=0'],
 ['La fuerza de empuje se proyecta en dos direcciones.','Se plantean tres incógnitas y tres residuos; la incidencia aparece además dentro de CL.','Se resuelve con una estimación inicial física y se comprueban límites de mando y empuje.','Se sustituyen resultados sin redondear en los tres balances.'],
 [test('Incidencia',f(al),'radian'),test('Elevador',f(de),'radian'),test('Empuje',f(T),'N'),test('Residuo tangencial',f(abs(trimfun(tr.x)[0])),'N'),test('Residuo normal',f(abs(trimfun(tr.x)[1])),'N'),test('Residuo de momento adimensional',f(abs(trimfun(tr.x)[2])))],
 'El componente vertical del empuje reduce ligeramente la sustentación aerodinámica necesaria frente a L=W.','Resolver desde varias estimaciones iniciales y comprobar residuos por componente; compararlo con el modelo que omite T sin(alpha).','La norma combina un residuo adimensional de momento con fuerzas sólo como diagnóstico de raíz; una tolerancia física debe escalar ambos tipos por separado.')

gp=Polar(16.2,.014,.032,1.55);cl=.78;g=glide_exact(gp,455,1.05,cl);Vapprox=gp.speed(455,1.05,cl);sapprox=Vapprox*gp.cd(cl)/cl
add(7,'Medir el error de planeo tendido',r'Un planeador de 455 kg, S=16.2 m² y polar 0.014+0.032CL² vuela a CL=0.78 en rho=1.05. Compare TAS y descenso exactos con la aproximación L=W y seno de delta igual a tangente.',
 r'Equilibrio estacionario sin empuje; gamma negativo.',
 'Trayectoria aérea en calma y fuerzas viento.',
 'La misma polar se utiliza en ambas comparaciones; sólo cambian las aproximaciones trigonométricas.',
 [r'\delta=\arctan(C_D/C_L)',r'V_{exacto}=\sqrt{2W\cos\delta/(\rho SC_L)}',r's_{exacto}=V_{exacto}\sin\delta',r'V_{aprox}=\sqrt{2W/(\rho SC_L)},\quad s_{aprox}=V_{aprox}C_D/C_L'],
 ['Se evalúa un único CD y ángulo para ambas vías.','Se conserva coseno en el equilibrio exacto.','Se calcula el error relativo de descenso y se interpreta su tamaño respecto a datos de polar.'],
 [test('TAS exacta',f(g['V']),'m/s'),test('Descenso exacto',f(g['sink']),'m/s'),test('Descenso aproximado',f(sapprox),'m/s'),test('Error relativo de descenso',f(sapprox/g['sink']-1))],
 'La aproximación es buena para una eficiencia elevada, pero la igualdad exacta y la aproximada no son la misma relación.','Comprobar que el cociente de velocidades es sqrt(cos(delta)) y evaluar energía DV/W en el caso exacto.','Un error pequeño de trigonometría no compensa incertidumbre grande de la polar o falta de trim.')

gp=Polar(16.2,.014,.032,1.55);op=minimize_scalar(lambda cl:glide_exact(gp,455,1.05,cl)['sink'],bounds=(.3,1.55),method='bounded');ca=gp.cl_minpower();ce=op.x
add(8,'Óptimo exacto de mínimo descenso',r'Con el planeador anterior, encuentre por cálculo numérico el CL de mínimo descenso exacto en 0.3<=CL<=1.55 y compare con sqrt(3CD0/k). Compruebe la condición de derivada exacta.',
 r'Masa 455 kg y densidad 1.05 kg/m³; mismo dominio válido de polar.',
 'Planeo rectilíneo en calma; ángulo de descenso positivo delta.',
 'Equilibrio exacto y polar fija; se optimiza sólo dentro de su intervalo.',
 [r's=\sqrt{2W/(\rho S)}\,C_D/(C_L^2+C_D^2)^{3/4}',r'4kC_L^2-2kC_D^2-3C_D=0'],
 ['Se forma la función exacta de descenso sin aproximar coseno.','Se busca el mínimo acotado y se comparan extremos.','Se evalúa el residuo de la condición algebraica exacta cerca del óptimo.','Se compara con el CL de la fórmula tendida y se cuantifica la diferencia.'],
 [test('CL exacto',f(ce)),test('CL aproximado',f(ca)),test('Descenso mínimo exacto',f(op.fun),'m/s'),test('Diferencia relativa CL',f(ce/ca-1))],
 'El óptimo de la aproximación y el exacto se aproximan para ángulos pequeños; no se los identifica sin evaluar el error.','Búsqueda de raíz de 4kCL²-2kCD²-3CD y comparación con minimización directa de la tasa.','Una segunda raíz fuera del dominio no representa una condición de vuelo admisible.')

gi=glide_integral(gp,455,3100,350,gp.cl_ld(),wind=9)
add(9,'Una trayectoria integral con viento de cola',r'Calcule alcance y duración del mismo planeador desde 3100 hasta 350 m ISA, manteniendo CL de mejor planeo en calma, con viento de cola 9 m/s. Compare avance terrestre medio con TAS inicial.',
 r'S=16.2 m², masa 455 kg, polar 0.014+0.032CL²; viento vertical nulo.',
 'Ruta aérea y terrestre alineadas; altitud geopotencial.',
 'Masa y polar constantes, sucesión cuasiestacionaria de equilibrios locales.',
 [r'R_a=\Delta hC_L/C_D',r'E=\int\dd h/s(h)',r'R_g=R_a+9E,\quad\bar V_{g,H}=R_g/E'],
 ['Se evalúa el CL de máxima eficiencia.','Se integra la tasa a densidad variable y se añade el desplazamiento de viento.','La velocidad media terrestre se obtiene como distancia dividida por tiempo y no coincide con una TAS puntual.'],
 [test('Alcance aéreo',f(gi['air_range']),'m'),test('Duración',f(gi['time']),'s'),test('Alcance terrestre',f(gi['ground_range']),'m'),test('Avance terrestre medio',f(gi['ground_range']/gi['time']),'m/s')],
 'El viento de cola aumenta alcance sin cambiar la duración de la ley de descenso definida.','Comparar cuadratura con primitiva ISA y comprobar Rg-Ra=9E.','No se ha optimizado la velocidad para aprovechar el viento; sólo se evalúa la ley impuesta.')

add(10,'Consumo efectivo de motores distintos',r'Dos motores entregan 24 y 19 kN con consumos específicos 16 y 19 g/(kN s). Calcule gasto total, cT efectivo y combustible en 32 minutos. Compare con promediar sin ponderar.',
 r'T1=24000 N, T2=19000 N; consumos másicos referidos a empuje.',
 'Empujes paralelos; suma escalar longitudinal.',
 'Ambos puntos de funcionamiento permanecen constantes durante el intervalo.',
 [r'\dot m_f=c_{T1}T_1+c_{T2}T_2',r'c_{T,ef}=\dot m_f/(T_1+T_2)',r'\Delta m=\dot m_ft'],
 ['Se calcula el gasto de cada motor con su propio consumo.','Se suman gastos y empujes y se obtiene la razón efectiva.','La media aritmética sólo sería equivalente si los empujes fuesen iguales.'],
 [test('Gasto total','16e-6*24000+19e-6*19000','kg/s'),test('Consumo efectivo','(16e-6*24000+19e-6*19000)/(24000+19000)','kg/(N*s)'),test('Combustible','(16e-6*24000+19e-6*19000)*32*60','kg')],
 'El consumo efectivo es una media ponderada por empuje.','Calcular en gramos por segundo y comprobar que multiplicar cT efectivo por empuje total recupera el mismo gasto.','No incluye asimetría de momentos ni resistencia de compensación de mandos.')

pj=Polar(42,.024,.044,1.5);m=7600;rho=isa(7000)[2];A=.5*rho*pj.S*pj.cd0;B=2*pj.k*(m*G)**2/(rho*pj.S);T=10000
vlo=math.sqrt(2*B/(T+math.sqrt(T*T-4*A*B)));vhi=math.sqrt((T+math.sqrt(T*T-4*A*B))/(2*A));vstall=pj.stall(m,rho);vMach=.62*isa(7000)[3]
add(11,'Intersección con un límite de Mach',r'Un reactor de 7600 kg, S=42 m² y polar 0.024+0.044CL² dispone de 10000 N a 7000 m ISA. CLmax=1.5 y Mach máximo 0.62. Halle el intervalo horizontal admisible según esas tres restricciones.',
 r'Empuje constante con velocidad en el intervalo; límite de Mach local.',
 'Velocidades TAS y vuelo horizontal en calma.',
 'Polar fija y trim asumido posible; no se añaden otros límites estructurales.',
 [r'V_\pm^2=[T\pm\sqrt{T^2-4AB}]/(2A)',r'V_{inf}=\max(V_-,V_{stall})',r'V_{sup}=\min(V_+,M_{max}a)'],
 ['Se encuentran ambas raíces de equilibrio.','Se compara la raíz baja con pérdida.','Se convierte Mach a TAS usando temperatura de 7000 m.','Si el intervalo resultante quedase vacío, no habría vuelo horizontal que cumpla las restricciones.'],
 [test('Raíz baja',f(vlo),'m/s'),test('Raíz alta',f(vhi),'m/s'),test('Pérdida',f(vstall),'m/s'),test('Límite TAS por Mach',f(vMach),'m/s'),test('Límite inferior',f(max(vlo,vstall)),'m/s'),test('Límite superior',f(min(vhi,vMach)),'m/s')],
 'La máxima velocidad de empuje puede quedar excluida por Mach; la raíz baja puede quedar excluida por pérdida.','Evaluar D en las fronteras y comprobar CL y Mach con los valores finales.','Una envolvente completa requiere centro de gravedad, autoridad de mando y otros límites operativos.')

# Cierre de masa inicial para una ruta prescrita: el combustible aumenta el peso que debe transportarse.
cl=pj.cl_jet_range();rho=isa(7000)[2];ct=1.7e-5;ld=pj.ld(cl);K=2*ld/(G*ct)*math.sqrt(2*G/(rho*pj.S*cl));mf=6500;route=1400000
mi=(math.sqrt(mf)+route/K)**2;vi=pj.speed(mi,rho,cl);vf=pj.speed(mf,rho,cl)
add(12,'Dimensionar combustible por cierre de misión',r'Una fase de reactor debe recorrer 1400 km en calma a 7000 m ISA y CL de máximo alcance. La masa final, que incluye carga y reserva, es 6500 kg. Con S=42 m², polar 0.024+0.044CL² y cT=1.7e-5 kg/(N s), determine masa inicial y combustible de la fase.',
 r'El combustible de la fase es desconocido y forma parte de masa inicial.',
 'Crucero horizontal y TAS variable para CL fijo.',
 'Polar, densidad y consumo constantes; no hay ascenso ni transición dentro de la fase.',
 [r'R=K_m(\sqrt{m_i}-\sqrt{m_f})',r'm_i=(\sqrt{m_f}+R/K_m)^2',r'm_{comb}=m_i-m_f'],
 ['Se calcula CL de máximo alcance y el coeficiente Km de la ley.','Se despeja masa inicial antes de restar combustible; no se utiliza una masa media arbitraria.','Se verifican velocidades extremas y que el alcance se reconstruya con la masa hallada.'],
 [test('Masa inicial',f(mi),'kg'),test('Combustible de fase',f(mi-mf),'kg'),test('TAS inicial',f(vi),'m/s'),test('TAS final',f(vf),'m/s')],
 'La masa final ya contiene la reserva; el combustible calculado es sólo el quemado en esta fase.','Resolver por raíz numérica la diferencia entre alcance calculado y prescrito; comprobar cierre de masa.','La factibilidad necesita capacidad de tanque, masa máxima, empuje y límites de Mach, que no se han dado.')

# Ascenso integrado con masa variable: ley TAS fija y empuje que pierde con densidad.
pc=Polar(31,.025,.047,1.5);V=90;ct=1.8e-5
def climbfun(h,y):
    m=y[0];rho=isa(h)[2];T=9500*(rho/1.225)**.8;D=pc.drag(V,m,rho);roc=(T-D)*V/(m*G)
    if roc<=0:raise RuntimeError('Techo alcanzado')
    return [-ct*T/roc,1/roc,V/roc]
cs=solve_ivp(climbfun,[1200,4200],[5300,0,0],rtol=1e-10,atol=1e-10,max_step=25);cm,ctime,cx=cs.y[:,-1]
add(13,'Integrar un ascenso consumiendo masa',r'Un reactor docente asciende de 1200 a 4200 m ISA a TAS constante de 90 m/s. Parte con 5300 kg. S=31 m², polar 0.025+0.047CL², empuje máximo 9500 sigma^0.8 N y cT=1.8e-5 kg/(N s). Calcule tiempo, combustible y avance aproximado.',
 r'Ley TAS fija; gravedad constante y densidad ISA actualizada.',
 'Trayectoria aérea sin viento; aproximación de ángulo pequeño para L y avance.',
 'L≈W, xdot≈V; motor a empuje máximo y consumo específico constante; masa actualizada en cada evaluación.',
 [r'c(h,m)=[T(h)-D(V,m,\rho(h))]V/(mg_0)',r'\dd m/\dd h=-c_TT/c',r'\dd t/\dd h=1/c,\quad\dd x/\dd h=V/c'],
 ['Se calcula atmósfera y empuje en cada altura.','La resistencia usa masa instantánea y TAS mantenida.','Se integran simultáneamente masa, tiempo y avance con altura como variable.','Se comprueba que la tasa permanece positiva y no se cruza un techo.'],
 [test('Tiempo de ascenso',f(ctime),'s'),test('Masa final',f(cm),'kg'),test('Combustible consumido',f(5300-cm),'kg'),test('Avance aproximado',f(cx),'m')],
 'El consumo reduce el peso durante el ascenso y cambia la resistencia y la tasa; congelar masa produce otro problema.','Repetir con paso máximo de altura dividido por dos y contrastar x=Vt para la aproximación usada.','No incluye la corrección cos(gamma) ni xdot=V cos(gamma); la etiqueta de avance aproximado conserva ese límite.')

pt=Polar(30,.024,.046,1.6);mt=4500;rt=1.0;T=7200;ns=3.0
def turnradius(v):
    qS=.5*rt*v*v*pt.S;A=.5*rt*pt.S*pt.cd0;B=2*pt.k*(mt*G)**2/(rt*pt.S)
    nt=math.sqrt(max(0,(T-A*v*v)*v*v/B));nl=qS*pt.clmax/(mt*G);n=min(nt,nl,ns)
    return v*v/(G*math.sqrt(n*n-1)) if n>1 else 1e12
vv=np.linspace(pt.stall(mt,rt)*1.001,180,20001);idx=np.argmin([turnradius(v) for v in vv]);vo=vv[idx]
qS=.5*rt*vo*vo*pt.S;AA=.5*rt*pt.S*pt.cd0;BB=2*pt.k*(mt*G)**2/(rt*pt.S);nt=math.sqrt(max(0,(T-AA*vo*vo)*vo*vo/BB));nl=qS*pt.clmax/(mt*G);no=min(nt,nl,ns)
add(14,'Radio mínimo sostenido con tres fronteras',r'Busque por barrido el radio mínimo sostenido entre pérdida y TAS 180 m/s para masa 4500 kg, rho=1.0, S=30 m², polar 0.024+0.046CL², CLmax=1.6, carga estructural 3 y empuje 7200 N.',
 r'Barrido de 20001 velocidades; si n<=1 no existe viraje nivelado de radio finito.',
 'Viraje coordinado nivelado en calma; TAS.',
 'Empuje constante, polar fija, sin resistencia adicional de mandos ni límite de Mach.',
 [r'n_T=\sqrt{(T-AV^2)V^2/B}',r'n_L=\rho V^2SC_{Lmax}/(2W)',r'n_{max}(V)=\min(n_T,n_L,3)',r'R(V)=V^2/[g_0\sqrt{n_{max}^2-1}]'],
 ['Se recorre sólo el intervalo de velocidad declarado.','Para cada punto se toma el menor de los tres límites de carga.','Se descartan puntos sin carga superior a uno y se minimiza el radio.','Se revisa la frontera activa cerca del mínimo y se afina la rejilla si se requiere más precisión.'],
 [test('TAS de rejilla óptima',f(vo),'m/s'),test('Carga en el punto',f(no)),test('Radio de rejilla mínimo',f(turnradius(vo)),'m'),test('Límite motor en el punto',f(nt)),test('Límite sustentación en el punto',f(nl))],
 'El óptimo de rejilla puede estar junto a una intersección de límites; no debe presentarse como raíz suave universal.','Refinar la rejilla y resolver las intersecciones de las fronteras próximas; comprobar D<=T, CL<=CLmax y n<=3.','La resolución de velocidad limita la precisión del óptimo y no se oculta con muchas cifras impresas.')

add(15,'Leer un mapa adimensional de hélice',r'Una hélice de diámetro 2.1 m gira a 32 rev/s con avance 58 m/s. En ese punto se han dado CT=0.083 y CP=0.090, con densidad 1.08 kg/m³. Calcule J, empuje, potencia al eje y rendimiento.',
 r'Los coeficientes pertenecen al mismo punto de mapa y se usan las definiciones de este capítulo.',
 'Empuje paralelo al avance aéreo; coeficientes de hélice adimensionales.',
 'Régimen y paso fijos en el punto; los valores de mapa son datos docentes, no mediciones.',
 [r'J=V/(n_rd)',r'T=C_T\rho n_r^2d^4',r'P=C_P\rho n_r^3d^5',r'\eta_p=JC_T/C_P'],
 ['Se usa régimen en revoluciones por segundo, sin multiplicar por 2pi en estas definiciones.','Se calculan empuje y potencia con las potencias correctas de diámetro.','Se obtiene eficiencia por coeficientes y se comprueba con TV/P.'],
 [test('Avance J','58/(32*2.1)'),test('Empuje','.083*1.08*32**2*2.1**4','N'),test('Potencia al eje','.090*1.08*32**3*2.1**5','W'),test('Rendimiento','58/(32*2.1)*.083/.090')],
 'Un mapa convierte la hipótesis de rendimiento constante en una función de condición; no se extrapola este punto al reposo.','Calcular TV/P con fuerzas y potencia dimensionales y compararlo con J CT/CP.','No se han comprobado Mach de punta ni límites de par del motor; un rendimiento mayor que uno indicaría datos o convenciones incompatibles.')

pr=Polar(19.4,.026,.047,1.6);rho=isa(2000)[2];cp=.295/3.6e6;eta=.80;mi=1850;mf=1510
rbest=prop_fixed_cl(pr,mi,mf,rho,pr.cl_ld(),cp,eta);ebest=prop_fixed_cl(pr,mi,mf,rho,pr.cl_minpower(),cp,eta)
add(16,'Cuánto cuesta elegir autonomía en vez de alcance',r'Un avión de hélice pasa de 1850 a 1510 kg a 2000 m ISA. S=19.4 m², polar 0.026+0.047CL², eficiencia 0.80 y consumo 0.295 kg/kWh. Compare alcance y duración si conserva CL de máximo alcance o de máxima autonomía.',
 r'Las dos leyes usan las mismas masas y altitud; CLmax=1.6.',
 'Crucero horizontal en calma, TAS variable con masa.',
 'Polar, rendimiento y consumo constantes; se comparan dos objetivos factibles dentro del modelo.',
 [r'C_{L,R}=\sqrt{C_{D0}/k},\quad C_{L,E}=\sqrt{3C_{D0}/k}',r'R=\eta_p(C_L/C_D)\ln(m_i/m_f)/(g_0c_P)',r'E=\frac{2\eta_p}{g_0c_P}\sqrt{\frac{\rho S C_L}{2g_0}}\frac{C_L}{C_D}(m_f^{-1/2}-m_i^{-1/2})'],
 ['Se comprueba que ambos CL son inferiores al máximo.','Se evalúan alcance y tiempo para cada uno con sus funciones objetivo.','Se compara la ganancia de tiempo con la reducción de alcance, sin usar una velocidad única para ambas leyes.'],
 [test('Alcance con CL de alcance',f(rbest['range']),'m'),test('Tiempo con CL de alcance',f(rbest['time']),'s'),test('Alcance con CL de autonomía',f(ebest['range']),'m'),test('Tiempo con CL de autonomía',f(ebest['time']),'s')],
 'Optimizar permanencia sacrifica distancia para las mismas masas y condiciones de este modelo.','Cuadraturas de distancia y tiempo por gasto para ambas leyes; comprobar las derivadas de objetivos.','No se añade resistencia de trim ni variación de eficiencia a baja velocidad.')

tk=Polar(20.2,.034,.051,1.85);args=(tk,1680,1.20,34,lambda v:5400,.03,.63)
roll0=ground_roll(*args);rollw=ground_roll(tk,1680,1.20,29,lambda v:5400,.03,.63,wind=5)
add(17,'Viento de cara: fuerza y distancia',r'Para masa 1680 kg, S=20.2 m², rho=1.20 y empuje 5400 N, calcule carrera hasta TAS 34 m/s en calma y con viento de cara 5 m/s. Use rodadura 0.03, CL de carrera 0.63 y polar 0.034+0.051CL².',
 r'La velocidad terrestre objetivo cambia de 34 a 29 m/s.',
 'Pista horizontal; fuerzas con velocidad aérea y distancia con velocidad terrestre.',
 'Empuje finito constante; sin rotación ni obstáculo; mismo estado atmosférico y configuración.',
 [r'V_a=V_g+U',r'a=[T-D(V_a)-\mu(W-L(V_a))]/m',r's=\int_0^{V_{g,f}}V_g/a(V_g)\,\dd V_g'],
 ['Se prepara un caso en calma y otro con su objetivo terrestre distinto.','En el caso con viento las fuerzas se evalúan con velocidad aérea desde Vg=0.','Se comprueban aceleración positiva y contacto y se integran ambas carreras.','Se compara reducción de distancia y se distingue de una simple corrección de velocidad final.'],
 [test('Carrera en calma',f(roll0['distance']),'m'),test('Carrera con viento',f(rollw['distance']),'m'),test('Reducción relativa',f(1-rollw['distance']/roll0['distance']))],
 'El viento reduce la carrera por varios términos del mismo balance; no es sólo una resta de avance al final.','Marcha temporal con eventos de velocidad aérea y revisión de fuerzas iniciales en ambos casos.','No se estudia viento de cola con flujo invertido ni ráfagas.')

br=ground_roll(tk,1680,1.20,30,lambda v:0,.31,.17,braking=True)
add(18,'Auditar la energía de una frenada',r'Con el avión anterior, considere toma en calma a 30 m/s, empuje nulo, CL residual 0.17 y freno 0.31. Calcule distancia, tiempo y energía inicial que deben disipar conjuntamente aire y ruedas.',
 r'Masa 1680 kg, S=20.2 m² y la misma polar; pista horizontal.',
 'Velocidad terrestre y fuerza resistente opuesta al avance.',
 'Masa, coeficientes y freno constantes; no hay demora de aplicación ni inversión de empuje.',
 [r'b=[D+\mu_b(W-L)]/m',r's=\int_0^{V_0}V/b\,\dd V,\quad t=\int_0^{V_0}\dd V/b',r'E_{k,0}=mV_0^2/2'],
 ['Se integra distancia y tiempo sobre la misma desaceleración variable.','Se calcula energía terrestre inicial.','Para auditar el balance, se integra por separado el trabajo de resistencia y freno a lo largo de la trayectoria.','No se asigna toda la energía a discos: parte se disipa aerodinámicamente.'],
 [test('Distancia',f(br['distance']),'m'),test('Tiempo',f(br['time']),'s'),test('Energía inicial','1680*30**2/2','J')],
 'El trabajo total puede cerrar aunque la fracción absorbida por frenos requiera otra integral.','Integrar (D+Ffreno) dx y comparar con energía inicial; al usar dx=V/b dV el balance se reduce a integral de mV.','No predice temperatura de frenos sin capacidad térmica, transferencia de calor y reparto de energía.')

kt=.93*.20*4.3*.67;aa=5.0+kt;hn=(5*.25+kt*3.3-.09)/aa
add(19,'Un límite de CG con margen mínimo',r'Con aw=5.0, at=4.3, St/S=0.20, eta=0.93, epsilon_alpha=0.33, hac=0.25, ht=3.3 y Cm_alpha_f=0.09, determine el CG más retrasado que conserva margen estático mínimo 0.08.',
 r'Posiciones adimensionales hacia atrás; pendientes por radián; mando fijo.',
 'Momento de cabeceo positivo morro arriba; referencia de posición común.',
 'Modelo lineal con punto neutro independiente de CG dentro de las hipótesis declaradas.',
 [r'K_t=\eta_t(S_t/S)a_t(1-\varepsilon_\alpha)',r'h_n=(a_wh_{ac}+K_th_t-C_{m\alpha,f})/(a_w+K_t)',r'h_{max}=h_n-SM_{min}'],
 ['Se calcula punto neutro conservando sustentación de cola en la pendiente total.','Se resta el margen exigido para fijar el límite retrasado.','Se evalúa la pendiente de momento en ese límite para comprobar el requisito.'],
 [test('Punto neutro',f(hn)),test('CG máximo',f(hn-.08)),test('Cm_alpha en límite',f(-aa*.08),'1/radian')],
 'El requisito fija una frontera estática y no determina por sí solo límites de mando, estructura o certificación.','Sustituir el CG límite en la expresión directa de ala, cola y fuselaje y recuperar -a por 0.08.','El punto neutro puede cambiar con Mach, potencia, configuración o mando libre.')

add(20,'La cola vertical también produce alabeo',r'Una fuerza de cola Y=-1250 N actúa en cuerpo en r=(-5.2,0,-1.1) m respecto al CG. Calcule momentos de alabeo y guiñada y explique por qué la altura de cola acopla movimientos.',
 r'Fuerza F=(0,-1250,0) N; punto por encima del CG tiene z negativo.',
 'Cuerpo dextrógiro con z abajo; momentos respecto al CG.',
 'Fuerza puntual equivalente; se omiten otros momentos aerodinámicos de cola.',
 [r'\vect M=\vect r\times\vect F',r'\mathcal L=-zY,\quad\mathcal N=xY'],
 ['Se identifica el signo de z para una cola situada por encima del CG.','El producto vectorial determina ambos momentos sin memorizar una regla visual.','Se interpreta el momento de guiñada junto al alabeo generado por el mismo esfuerzo lateral.'],
 [test('Momento de alabeo','-(-1.1)*(-1250)','N*m'),test('Momento de guiñada','(-5.2)*(-1250)','N*m')],
 'Una superficie destinada a estabilidad direccional también puede modificar la dinámica de alabeo.','Expansión del determinante del producto vectorial y comprobación de unidades N m.','No se deriva la fuerza de un beta concreto ni se incluye la respuesta del resto del avión.')

Am=np.array([[-.7,1],[-3.8,-1.1]]);x0=np.array([.04,0]);ts=np.linspace(0,12,121);ss=solve_ivp(lambda t,x:Am@x,[0,12],x0,t_eval=ts,rtol=1e-11,atol=1e-13);xx=expm(Am*12)@x0;ev=np.linalg.eigvals(Am)
add(21,'Respuesta lineal por dos integradores conceptuales',r'Para la matriz sintética A=[[-0.7,1],[-3.8,-1.1]] y perturbación inicial (alpha,q)=(0.04,0), calcule autovalores y estado a 12 s. Compare exponencial matricial y una integración de ODE.',
 r'alpha en rad, q en rad/s; matriz no identificada de una aeronave.',
 'Estados longitudinales perturbados; tiempo en segundos.',
 'Sistema lineal autónomo, sin mando y sin saturación.',
 [r'\dot{\vect x}=A\vect x',r'\vect x(t)=e^{At}\vect x(0)'],
 ['Se comprueba que ambas partes reales son negativas.','Se evalúa la exponencial de matriz y se integra la ODE con las mismas condiciones.','Se compara el estado completo y no sólo un cruce de alpha por cero.','La diferencia numérica mide consistencia de estos algoritmos sobre el modelo lineal.'],
 [test('Parte real modal',f(ev[0].real),'1/s'),test('Parte imaginaria modal',f(abs(ev[0].imag)),'1/s'),test('Alpha a 12 s',f(xx[0]),'radian'),test('q a 12 s',f(xx[1]),'1/s'),test('Error de alpha entre métodos',f(abs(xx[0]-ss.y[0,-1])),'radian'),test('Error de q entre métodos',f(abs(xx[1]-ss.y[1,-1])),'1/s')],
 'El estado final pequeño corresponde a una oscilación amortiguada; el resultado pertenece a la matriz sintética.','La comparación expm frente a solve_ivp se ejecuta en el programa; se conservan tolerancias e intervalo.','La norma de error agrupa dos estados de unidades distintas sólo como diagnóstico numérico; cada componente se revisa además individualmente.')

xr=json.loads((RDIR/'reports/xml-run.json').read_text());a=xr['initial'];z=xr['final']
add(22,'Comprobar una inicialización XML ejecutada',r'El par XML original del proyecto inicializa el T-6 a CAS 155 kt y 5000 ft y se integra libremente 60 s. Con el CSV ejecutado, determine variación de altura, TAS y combustible. Explique por qué una deriva no es automáticamente un fallo de integración.',
 r'Los valores iniciales y finales se extraen del archivo t6-xml-executed.csv; modelo educativo t6texan2, JSBSim 1.3.3.',
 'Propiedades del simulador convertidas a SI; CAS de entrada distinta de EAS y TAS.',
 'Mandos de trim congelados; hay consumo y dinámica terrestre del modelo.',
 [r'\Delta h=h_f-h_i,\quad\Delta V=V_f-V_i',r'\Delta m_f=m_{comb,i}-m_{comb,f}'],
 ['Se comprueba la velocidad realmente inicializada, además de la solicitada.','Se restan estados de la misma columna y unidad.','El consumo cambia masa y el trim inicial tiene una tolerancia; ambos pueden generar deriva física del modelo.','Para atribuir error al paso se repite con otras discretizaciones manteniendo entradas.'],
 [test('Cambio de altura',f(z['h_m']-a['h_m']),'m'),test('Cambio de TAS',f(z['TAS_m_s']-a['TAS_m_s']),'m/s'),test('Combustible gastado',f(a['fuel_kg']-z['fuel_kg']),'kg')],
 'El experimento demuestra una ejecución de archivos concretos, no fidelidad de una aeronave real.','Releer el CSV y comprobar integridad temporal y masa; comparar con el experimento de refinamiento del capítulo siguiente.','Un replay de las diferencias no verifica por sí solo el motor de dinámica; los registros y modelo identifican qué se ejecutó.')

cv=json.loads((RDIR/'reports/jsbsim-results.json').read_text())['convergence'];d1=abs(cv[0]['TAS_m_s']-cv[1]['TAS_m_s']);d2=abs(cv[1]['TAS_m_s']-cv[2]['TAS_m_s'])
add(23,'Interpretar un refinamiento realmente ejecutado',r'En el ensayo libre de 60 s del T-6 se usaron pasos 0.10, 0.05 y 0.025 s. Compare las TAS finales y calcule diferencias sucesivas. ¿Permiten asignar un orden universal a JSBSim?',
 r'Los tres CSV y registros de versión están incluidos en el proyecto; las condiciones iniciales y duración son comunes.',
 'Misma propiedad TAS SI al final de cada trayectoria.',
 'Comparación de un experimento libre concreto, sin atribuir todo el error a una sola potencia de paso.',
 [r'\Delta_1=|V_{0.10}-V_{0.05}|',r'\Delta_2=|V_{0.05}-V_{0.025}|',r'p_{observado}=\ln(\Delta_1/\Delta_2)/\ln2'],
 ['Se extraen los valores finales sin redondear antes de restarlos.','Se calculan diferencias y un orden observado sólo como indicador condicionado.','La mezcla de actualización de masa, tolerancia de trim e integradores impide generalizarlo a todos los estados y casos.'],
 [test('Diferencia primera',f(d1),'m/s'),test('Diferencia segunda',f(d2),'m/s'),test('Orden observado condicionado',f(math.log(d1/d2,2)))],
 'Las diferencias pequeñas y decrecientes aportan sensibilidad temporal para esta TAS final; no prueban un orden formal global.','Comprobar también altura, actitud y masa final en los registros y repetir con otro paso si la aplicación exige tolerancias más estrictas.','Las autonomías completas del 747 no se declaran convergentes por este ensayo corto de otra aeronave.')

def build():
    # Unidades adicionales usadas en talleres: se registran explícitamente para el render.
    import render_problems
    render_problems.units.update({'kg/(N*s)':r'\mathrm{kg\,N^{-1}\,s^{-1}}','J':r'\mathrm J'})
    for p in W:
        content=solution(p)
        content=content.replace(r'\section{'+p['key']+' · '+p['title']+'}',r'\section{Taller resuelto: '+p['title']+'}')
        (RDIR/'content'/f't{p["ch"]:02}.tex').write_text(content)
        chapter=RDIR/'content'/f'c{p["ch"]:02}.tex';text=chapter.read_text()
        marker=rf'\input{{content/t{p["ch"]:02}}}'
        if marker not in text:
            at=text.index(r'\repaso{');text=text[:at]+marker+'\n\n'+text[at:];chapter.write_text(text)
    (RDIR/'evidence/manual-workshops.json').write_text(json.dumps(W,ensure_ascii=False,indent=2))
    print('Talleres originales de manual:',len(W))
if __name__=='__main__':build()
