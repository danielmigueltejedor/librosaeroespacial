"""Banco original de problemas con solución y registro de sustituciones.
Datos docentes creados para este libro; no son fichas de aeronaves reales.
"""
from pathlib import Path
import json,math
import sympy as sp
import numpy as np
from scipy.optimize import brentq,minimize_scalar
from scipy.integrate import quad
from models import *
RDIR=Path(__file__).resolve().parents[1]
BANK=[]
def test(name,expr,unit='dimensionless'):
    value=float(sp.sympify(expr).evalf(30))
    return dict(name=name,expression=expr,expected=value,unit=unit)
def add(ch,title,prompt,data,unknown,frame,hyp,model,eqs,steps,tests,interpret,check,limits,level='INTERMEDIATE'):
    BANK.append(dict(key=f'P{len(BANK)+1:02}',ch=ch,title=title,prompt=prompt,data=data,unknown=unknown,frame=frame,hyp=hyp,model=model,eqs=eqs,steps=steps,tests=tests,interpretation=interpret,independent=check,limits=limits,level=level))
def f(x):return format(float(x),'.16g')

add(10,'Consumo másico y ponderal',r'Un reactor entrega $38\,000\SIu N$ con consumo específico $18.2\SIu{g/(kN\,s)}$. Obtenga gasto másico, consumo en 25 minutos y consumo ponderal equivalente.',
 r'$T=38\,000\SIu N$, $c_T=18.2\times10^{-6}\SIu{kg/(N\,s)}$, $t=1500\SIu s$.','Gasto, masa consumida y consumo ponderal.','Escalares propulsivos; empuje en dirección de vuelo.','Empuje y consumo específico constantes durante el intervalo.','Gasto referido a empuje',
 [r'\dot m_f=c_TT',r'\Delta m=\dot m_ft',r'\widetilde c_T=g_0c_T'],
 ['Se convierten gramos a kg y kN a N: cada conversión aporta un factor de mil en sentidos distintos.','El gasto se multiplica por segundos, sin introducir gravedad en una masa.','El factor de gravedad se aplica sólo para pasar a consumo ponderal.'],
 [test('Gasto','18.2e-6*38000','kg/s'),test('Combustible','18.2e-6*38000*1500','kg'),test('Consumo ponderal','9.80665*18.2e-6','1/s')],
 'El gasto constante no implica que el avión conserve masa; la masa del avión disminuye exactamente en la cantidad calculada.','Rehacer la operación en g/s: 18.2 g por kN y segundo multiplicados por 38 kN; convertir al final.','No se ha supuesto un mapa de motor válido fuera del intervalo.', 'BASIC')

add(2,'Velocidad en ejes cuerpo',r'Una velocidad aérea tiene componentes cuerpo $(74,6,9)\SIu{m\,s^{-1}}$. Determine TAS, incidencia y resbalamiento y reconstruya el vector.',
 r'$u_a=74$, $v_a=6$, $w_a=9$, en $\mathrm{m/s}$.','TAS, alpha y beta.','Cuerpo: x adelante, y derecha, z abajo; matriz pasiva viento a cuerpo.','Velocidad no nula; ángulos dentro de la rama habitual de vuelo hacia delante.','Definición de ángulos aerodinámicos',
 [r'V=\sqrt{u_a^2+v_a^2+w_a^2}',r'\alpha=\arctan(w_a/u_a),\quad\beta=\arcsin(v_a/V)',r'\vect v_a^b=V(\cos\alpha\cos\beta,\sin\beta,\sin\alpha\cos\beta)^T'],
 ['Se calcula primero el módulo de las tres componentes.','La incidencia utiliza w/u; el resbalamiento utiliza v/V y no v/u.','Los resultados angulares se convierten a grados sólo para presentación.'],
 [test('TAS','sqrt(74**2+6**2+9**2)','m/s'),test('Incidencia grados','atan(9/74)*180/pi','degree'),test('Resbalamiento grados','asin(6/sqrt(74**2+6**2+9**2))*180/pi','degree')],
 'El w positivo representa velocidad hacia abajo en cuerpo, sin determinar todavía ascenso o descenso terrestre.','Multiplicar V por la primera columna de Cbw y comprobar que recupera las tres entradas y su norma.','No hay información de actitud ni viento para reconstruir la trayectoria terrestre.','BASIC')

add(2,'Peso en actitud inclinada',r'Un avión de $1800\SIu{kg}$ tiene alabeo $22^\circ$ y cabeceo $7^\circ$. Exprese el peso en cuerpo y compruebe su norma.',
 r'$m=1800\SIu{kg}$, $\phi=22^\circ$, $\theta=7^\circ$.','Tres componentes de peso.','NED a cuerpo con Euler 3--2--1.','Gravedad uniforme; no se necesitan guiñada ni velocidad para esta proyección.','Transformación de gravedad',
 [r'\vect W^b=mg_0(-\sin\theta,\sin\phi\cos\theta,\cos\phi\cos\theta)^T'],
 ['Se transforman grados a radianes en las funciones trigonométricas.','El componente x es negativo con morro alto.','Los componentes y y z dependen del alabeo y del coseno de cabeceo.'],
 [test('Wx','-1800*9.80665*sin(7*pi/180)','N'),test('Wy','1800*9.80665*sin(22*pi/180)*cos(7*pi/180)','N'),test('Wz','1800*9.80665*cos(22*pi/180)*cos(7*pi/180)','N')],
 'La proyección lateral del peso no constituye por sí sola una fuerza aerodinámica lateral.','Usar ortogonalidad: la suma de cuadrados debe ser (mg)^2 y el límite phi=theta=0 debe dar sólo Wz.','No se añaden términos centrífugos a una gravedad ya definida como efectiva.','BASIC')

add(3,'Ruta con viento cruzado',r'Una aeronave debe seguir una ruta este con TAS $68\SIu{m/s}$. El viento sopla hacia el norte a $16\SIu{m/s}$ y hacia el este a $5\SIu{m/s}$. Calcule corrección de rumbo y tiempo para $240\SIu{km}$.',
 r'$V=68$, $U_\perp=16$, $U_\parallel=5$, en m/s; $R_g=240\,000\SIu m$.','Corrección angular y tiempo.','Horizonte local; componentes paralela y normal a la ruta este.','Viento uniforme, vuelo horizontal, TAS constante y corrección de rumbo sostenida.','Triángulo vectorial de viento',
 [r'\sin\delta=-U_\perp/V',r'V_{g,\parallel}=\sqrt{V^2-U_\perp^2}+U_\parallel',r't=R_g/V_{g,\parallel}'],
 ['Se verifica primero que el viento transversal no excede TAS.','Se orienta el morro hacia el sur de la ruta para anular la deriva al norte.','Se calcula el avance proyectado y se divide la distancia terrestre por él.'],
 [test('Corrección grados','-asin(16/68)*180/pi','degree'),test('Avance terrestre','sqrt(68**2-16**2)+5','m/s'),test('Tiempo','240000/(sqrt(68**2-16**2)+5)','s')],
 'El viento de cola ayuda al avance, pero el viento cruzado consume parte de la velocidad aérea en corregir deriva.','Sumar las componentes normal y paralela de velocidad y comprobar normal nula.','No se han incluido cambios de viento ni curvatura terrestre.','BASIC')

add(3,'Aceleración con componentes estacionarias',r'En un instante, $\vect v^b=(95,0,0)\SIu{m/s}$ y $\vect\omega^b=(0,0,0.045)\SIu{rad/s}$. Las componentes de velocidad no cambian. Calcule aceleración y fuerza resultante para $3200\SIu{kg}$.',
 r'$u=95\SIu{m/s}$, $r=0.045\SIu{rad/s}$, $m=3200\SIu{kg}$.','Aceleración lateral y fuerza total.','Componentes cuerpo; derivada física respecto a referencia inercial local.','Masa constante y movimiento instantáneo definido por los datos.','Teorema de transporte',
 [r'\vect a^b=\dot{\vect v}^{\,b}+\vect\omega^b\times\vect v^b',r'a_y=ru,\qquad F_y=ma_y'],
 ['Se anula la derivada de componentes, no la del vector físico.','El producto z por x apunta a y positivo.','La fuerza solicitada es la resultante total, no sólo la aerodinámica.'],
 [test('Aceleración','0.045*95','m/s^2'),test('Fuerza resultante','3200*0.045*95','N'),test('Radio cinemático','95/0.045','m')],
 'El movimiento tiene rapidez constante y aceleración no nula.','Comparar la aceleración con V²/R usando R=V/r.','La geometría cinemática no fija el alabeo ni la distribución de fuerzas.','BASIC')

add(4,'De coeficientes a fuerzas',r'Con $\rho=0.93\SIu{kg/m^3}$, TAS $88\SIu{m/s}$, $S=31\SIu{m^2}$, $C_L=0.62$, $C_{D0}=0.025$, $k=0.044$, determine sustentación, resistencia y potencia necesaria.',
 r'Los datos anteriores corresponden a una configuración docente fija.','L, D y potencia de empuje.','Fuerzas en ejes viento; L y D son magnitudes positivas.','Polar parabólica; no se presupone vuelo horizontal hasta comprobar peso si se proporciona.','Dimensionalización aerodinámica',
 [r'q_\infty=\tfrac12\rho V^2',r'L=q_\infty SC_L,\quad D=q_\infty S(C_{D0}+kC_L^2),\quad P_n=DV'],
 ['Se calcula presión dinámica con TAS local.','Se evalúa la polar antes de multiplicar por presión y superficie.','La potencia utiliza la misma TAS, no una velocidad equivalente.'],
 [test('Sustentación','.5*.93*88**2*31*.62','N'),test('Resistencia','.5*.93*88**2*31*(.025+.044*.62**2)','N'),test('Potencia','.5*.93*88**3*31*(.025+.044*.62**2)','W')],
 'Los coeficientes son adimensionales; la fuerza resultante depende de presión dinámica y superficie de referencia.','Calcular L/D a partir de fuerzas y comprobar que coincide con CL/CD.','No se verifica trim ni límites de sustentación sin datos adicionales.','BASIC')

add(4,'Oswald y eficiencia de envergadura',r'Para $AR=10.5$, $e_i=0.91$ y una contribución de perfil $0.007C_L^2$, encuentre k total y Oswald equivalente. Determine el error al omitir el perfil para $C_L=0.9$.',
 r'$AR=10.5$, $e_i=0.91$, $k_{perfil}=0.007$, $C_L=0.9$.','k total, eO y resistencia cuadrática omitida.','Coeficientes referidos a la misma S y envergadura.','Separación parabólica válida; misma configuración y Mach.','Suma de contribuciones cuadráticas',
 [r'k=1/(\pi AR e_i)+k_{perfil}',r'e_O=1/(\pi AR k)',r'\Delta C_D=k_{perfil}C_L^2'],
 ['Se calcula la parte inducida con eficiencia de envergadura.','Se suma la contribución de perfil antes de definir el factor equivalente de la polar total.','La diferencia se evalúa en el CL dado.'],
 [test('k total','1/(pi*10.5*.91)+.007'),test('Oswald','1/(pi*10.5*(1/(pi*10.5*.91)+.007))'),test('CD omitido','.007*.9**2')],
 'Oswald es menor que la eficiencia de envergadura bajo una contribución de perfil cuadrática positiva.','Sustituir el Oswald obtenido en 1/(pi AR eO) y recuperar k total.','No es una igualdad universal entre modelos de resistencia no parabólicos.','INTERMEDIATE')

I=np.array([[9200,0,-700],[0,14000,0],[-700,0,18500]])
omega=np.array([.15,-.07,.11]);M=np.array([800,-620,290]);od=omega_derivative(omega,M,I)
Ap=800-(18500-14000)*(-.07)*.11+700*.15*(-.07)
Ar=290-(14000-9200)*.15*(-.07)-700*(-.07)*.11
add(5,'Producto de inercia en movimiento acoplado',r'Un sólido simétrico tiene el tensor indicado y $\vect\omega=(0.15,-0.07,0.11)\SIu{rad/s}$. Con momentos $(800,-620,290)\SIu{N\,m}$, determine las tres aceleraciones angulares.',
 r'$I_{xx}=9200$, $I_{yy}=14000$, $I_{zz}=18500$, $I_{xz}=700$, en kg m²; tensor con entradas cruzadas $-I_{xz}$.','pdot, qdot y rdot.','Cuerpo dextrógiro; producto Ixz definido como integral xz dm.','Sólido rígido, tensor constante y momentos respecto al centro de gravedad.','Newton--Euler vectorial y solución del bloque p,r',
 [r'I\dot{\vect\omega}=\vect M-\vect\omega\times(I\vect\omega)',r'\Delta=I_{xx}I_{zz}-I_{xz}^2',r'\dot p=(I_{zz}A_p+I_{xz}A_r)/\Delta,\quad\dot r=(I_{xz}A_p+I_{xx}A_r)/\Delta'],
 ['Se forma H=I omega y su producto con omega.','Se conservan los signos negativos del tensor cruzado y se calculan los residuos de momento.','La ecuación q se resuelve directamente; las otras dos se resuelven juntas.'],
 [test('pdot',f'(18500*({f(Ap)})+700*({f(Ar)}))/(9200*18500-700**2)','1/s^2'),test('qdot','(-620-(9200-18500)*.15*.11-700*(.15**2-.11**2))/14000','1/s^2'),test('rdot',f'(700*({f(Ap)})+9200*({f(Ar)}))/(9200*18500-700**2)','1/s^2')],
 'Los momentos y las aceleraciones no son independientes por ejes cuando existe producto de inercia.','Resolver con una matriz lineal y comprobar I odot+omega×Iomega-M=0; además comprobar tensor definido positivo.','No incluye flexibilidad, masa interna móvil ni flujo de momento angular.','ADVANCED')

m,rho,S,V=2300,1.08,25,67
cl=2*m*G/(rho*S*V**2);alpha=(cl-.22-.3*.05/1.1)/(5.3-.3*.75/1.1);de=(.05-.75*alpha)/1.1
add(6,'Trim con sustentación de elevador',r'Resuelva el trim de un avión docente con $C_L=0.22+5.3\alpha+0.30\delta_e$ y $C_m=0.05-0.75\alpha-1.10\delta_e$. Use los datos y determine también empuje para polar $0.026+0.045C_L^2$.',
 r'$m=2300\SIu{kg}$, $S=25\SIu{m^2}$, $\rho=1.08\SIu{kg/m^3}$, $V=67\SIu{m/s}$; ángulos en radianes.','Incidencia, elevador y empuje.','Cuerpo/viento en vuelo simétrico; empuje aproximado paralelo a trayectoria.','Vuelo horizontal, coeficientes lineales, autoridad de mando suficiente.','Sistema de dos ecuaciones y balance T=D',
 [r'C_{L,req}=2mg_0/(\rho V^2S)',r'\delta_e=(0.05-0.75\alpha)/1.10',r'\alpha=(C_{L,req}-0.22-0.30\cdot0.05/1.10)/(5.3-0.30\cdot0.75/1.10)'],
 ['El CL requerido se calcula con el peso, sin suponer una incidencia inicial.','Se elimina elevador en la ecuación de sustentación y después se recupera el mando.','Con CL de equilibrio se evalúa la polar y la resistencia.'],
 [test('Incidencia',f'({f(cl)}-.22-.30*.05/1.10)/(5.3-.30*.75/1.10)','radian'),test('Elevador',f'(.05-.75*({f(alpha)}))/1.10','radian'),test('Empuje',f'.5*1.08*67**2*25*(.026+.045*({f(cl)})**2)','N')],
 'El elevador participa en la sustentación y no sólo en el momento; ignorarlo cambia la incidencia.','Sustituir alpha y elevador en ambas ecuaciones y comprobar L-W y Cm; comprobar el límite de mando que se imponga.','No se modela empuje inclinado ni aerodinámica no lineal.','INTERMEDIATE')

gl=Polar(16.4,.0125,.029,1.55)
CL=.72;delta=math.atan(gl.cd(CL)/CL);vg=glide_exact(gl,445,1.12,CL)
add(7,'Planeo con equilibrio exacto',r'Un planeador de $445\SIu{kg}$ y $16.4\SIu{m^2}$ vuela a $C_L=0.72$ en densidad $1.12\SIu{kg/m^3}$. Con polar $0.0125+0.029C_L^2$, calcule ángulo, TAS y descenso.',
 r'$m=445$, $S=16.4$, $C_L=0.72$, $\rho=1.12$ en SI.','gamma, TAS y tasa de descenso.','Ejes trayectoria, gamma positivo en ascenso.','Planeo rectilíneo estacionario sin empuje; polar fija.','Equilibrio exacto de planeador',
 [r'\gamma=-\arctan(C_D/C_L)',r'V=\sqrt{2W\cos\gamma/(\rho SC_L)}',r's=-V\sin\gamma'],
 ['Se evalúa CD antes de calcular el ángulo.','Se conserva coseno de gamma en el balance normal.','Se convierte la velocidad total en componente vertical con seno de gamma.'],
 [test('Gamma',f'-atan((.0125+.029*.72**2)/.72)','radian'),test('TAS',f'sqrt(2*445*9.80665*cos({f(delta)})/(1.12*16.4*.72))','m/s'),test('Descenso',f'{f(vg["V"])}*sin({f(delta)})','m/s')],
 'La tasa de descenso es positiva en la presentación y la altitud tiene derivada negativa.','Comprobar D+W sin(gamma)=0 y L-W cos(gamma)=0 usando las fuerzas calculadas.','No representa una transición ni pérdida dinámica.','INTERMEDIATE')

add(8,'Dos objetivos de planeador',r'Para la polar anterior determine CL de mejor planeo y mínimo descenso aproximado; compare sus velocidades a igual masa y densidad y compruebe admisibilidad con $C_{L\max}=1.55$.',
 r'$C_{D0}=0.0125$, $k=0.029$, $C_{L\max}=1.55$.','Óptimos, eficiencia máxima y relación de velocidades.','Vuelo simétrico; ángulos pequeños para mínimo descenso.','Polar parabólica, masa y densidad fijas, sin viento.','Optimización por derivadas',
 [r'C_{L,E}=\sqrt{C_{D0}/k}',r'C_{L,s}=\sqrt{3C_{D0}/k}',r'E_{a,max}=1/(2\sqrt{C_{D0}k}),\quad V_s/V_E=3^{-1/4}'],
 ['Se maximiza CL/CD para alcance y CL^(3/2)/CD para tiempo.','Se comprueba el cambio de signo de derivadas y se compara con la frontera CLmax.','La relación de velocidades usa V proporcional a CL^(-1/2).'],
 [test('CL mejor planeo','sqrt(.0125/.029)'),test('CL mínimo descenso','sqrt(3*.0125/.029)'),test('Eficiencia máxima','1/(2*sqrt(.0125*.029))'),test('Relación velocidades','3**(-1/4)')],
 'El mínimo descenso se consigue más despacio que el máximo alcance en calma.','Maximizar numéricamente ambas funciones sobre 0<CL<=1.55 y contrastar con las raíces.','El óptimo exacto de mínimo descenso tiene una corrección de pequeño ángulo.','INTERMEDIATE')

CL=gl.cl_ld();d=math.atan(gl.cd(CL)/CL);b=.0065/288.15;n=(G/(R*.0065)-1)/2
K=math.sqrt(1.225*gl.S*CL/(2*445*G*math.cos(d)))/math.sin(d)
Eexpr=f'{f(K)}/({f(b)}*({f(n)}+1))*((1-{f(b)}*300)**({f(n)}+1)-(1-{f(b)}*3600)**({f(n)}+1))'
Eval=float(sp.sympify(Eexpr));air=3300*gl.ld(CL)
add(9,'Descenso integral con viento',r'El planeador de $445\SIu{kg}$ desciende de 3600 a 300 m geopotenciales manteniendo CL de mejor planeo en calma. Determine alcance aéreo, duración ISA y alcance terrestre con viento de cara $7\SIu{m/s}$.',
 r'$S=16.4\SIu{m^2}$, polar $0.0125+0.029C_L^2$; ISA troposférica y viento vertical nulo.','Alcance y tiempo integrados.','Trayectoria aérea y ruta terrestre alineadas con el viento.','Masa y polar constantes; sucesión cuasiestacionaria de equilibrios; viento horizontal uniforme.','Integral exacta local del planeo con densidad variable',
 [r'R_a=\Delta h\,C_L/C_D',r'E=\int_{h_f}^{h_i}\dd h/s(h)',r'R_g=R_a-7E'],
 ['Se obtiene CL de mejor planeo y el ángulo exacto de descenso.','Se sustituye la densidad ISA bajo la raíz de 1/s y se integra su potencia de temperatura.','Se resta el desplazamiento del viento durante el tiempo calculado.'],
 [test('Tiempo ISA',Eexpr,'s'),test('Alcance aéreo',f'3300*({f(gl.ld(CL))})','m'),test('Alcance terrestre',f'{f(air)}-7*({Eexpr})','m')],
 'El viento reduce alcance terrestre sin cambiar el tiempo de esta ley aérea.','Cuadratura de 1/s(h) frente a la primitiva; el proyecto calcula también glide_integral con el mismo modelo.','No es la estrategia reoptimizada para viento; no usa una densidad única para todo el descenso.','ADVANCED')

tan=math.tan(math.radians(4));disc=tan*tan-4*.029*.0125
add(8,'Dos ramas para un ángulo de planeo',r'¿Qué valores de CL permiten un descenso estacionario de $4^\circ$ con polar $0.0125+0.029C_L^2$? Examine ambas ramas con CLmax=1.55.',
 r'$\delta=4^\circ$, $C_{D0}=0.0125$, $k=0.029$, $C_{L\max}=1.55$.','Raíces y rama admisible.','Ángulo de descenso positivo delta; gamma=-delta.','Polar válida sólo hasta CLmax; equilibrio exacto de fuerza.','Ecuación cuadrática de CD/CL',
 [r'kC_L^2-\tan\delta\,C_L+C_{D0}=0',r'C_{L,\pm}=[\tan\delta\pm\sqrt{\tan^2\delta-4kC_{D0}}]/(2k)'],
 ['Se calcula el discriminante y se exige no negatividad.','Las dos raíces son matemáticas; la mayor puede exceder el dominio aerodinámico.','Se evalúa CD/CL para cada raíz y se recorta con CLmax.'],
 [test('CL bajo','(tan(4*pi/180)-sqrt(tan(4*pi/180)**2-4*.029*.0125))/(2*.029)'),test('CL alto','(tan(4*pi/180)+sqrt(tan(4*pi/180)**2-4*.029*.0125))/(2*.029)')],
 'Un mismo ángulo puede corresponder a una rama rápida de CL pequeño y otra lenta; la lenta puede estar fuera de la envolvente.','Sustituir cada raíz en atan(CD/CL) y recuperar cuatro grados.','La existencia de raíz no prueba estabilidad ni trim de momentos.','ADVANCED')

pol=Polar(34,.023,.043,1.6);mass=6200;rh=isa(5000)[2];A=.5*rh*pol.S*pol.cd0;BB=2*pol.k*(mass*G)**2/(rh*pol.S)
add(11,'Raíces de vuelo nivelado',r'Un reactor docente de $6200\SIu{kg}$ vuela a 5000 m ISA con $S=34\SIu{m^2}$ y polar $0.023+0.043C_L^2$. Para $T_d=8200\SIu N$, encuentre las dos velocidades matemáticas y compare con pérdida CLmax=1.6.',
 r'$\rho$ procede de ISA; empuje constante con velocidad en el intervalo.','V baja, V alta y pérdida.','Vuelo nivelado en ejes viento; velocidades TAS.','Masa fija, empuje paralelo a trayectoria y polar parabólica.','Cuadrática en V²',
 [r'A=\rho SC_{D0}/2,\quad B=2kW^2/(\rho S)',r'V_\pm^2=(T\pm\sqrt{T^2-4AB})/(2A)',r'V_{stall}=\sqrt{2W/(\rho SC_{Lmax})}'],
 ['Se calcula la densidad antes de dimensionalizar A y B.','Se verifica T>=2sqrt(AB) y se resuelven ambas ramas.','Se compara la inferior con pérdida y se conserva sólo el intervalo admisible.'],
 [test('V baja',f'sqrt(2*{f(BB)}/(8200+sqrt(8200**2-4*{f(A)}*{f(BB)})))','m/s'),test('V alta',f'sqrt((8200+sqrt(8200**2-4*{f(A)}*{f(BB)}))/(2*{f(A)}))','m/s'),test('Pérdida',f'sqrt(2*6200*9.80665/({f(rh)}*34*1.6))','m/s')],
 'La raíz de empuje pequeña no se identifica automáticamente con velocidad mínima utilizable.','Sustituir cada velocidad en D=AV²+B/V² y comprobar 8200 N; comprobar producto de velocidades normalizadas.','No se ha impuesto límite de Mach ni trim de momentos; deben añadirse si se dispone de ellos.','INTERMEDIATE')

mi,mf=6200,5100;ct=1.72e-5;CL=pol.cl_jet_range();CD=pol.cd(CL)
Krange=2/(G*ct)*math.sqrt(2/(rh*pol.S))*math.sqrt(CL)/CD
add(12,'Reactor a incidencia constante',r'El reactor anterior consume desde 6200 hasta 5100 kg a altitud fija y CL constante de máximo alcance. Obtenga alcance, autonomía y velocidades extremas.',
 r'$h=5000\SIu m$ ISA, $c_T=1.72\times10^{-5}\SIu{kg/(N\,s)}$, $S=34\SIu{m^2}$ y polar anterior.','R, E, Vi y Vf.','Ruta horizontal sin viento; TAS variable.','CL, densidad, consumo específico y polar constantes; cuasiestacionario.','Breguet con diferencia de raíces',
 [r'C_L=\sqrt{C_{D0}/(3k)}',r'R_a=\frac{2}{g_0c_T}\sqrt{\frac2{\rho S}}\frac{\sqrt{C_L}}{C_D}(\sqrt{W_i}-\sqrt{W_f})',r'E=\frac{C_L}{g_0c_TC_D}\ln(W_i/W_f)'],
 ['Se usa el óptimo de alcance del reactor, no el de mínima resistencia.','El tiempo integra 1/W y el alcance integra 1/sqrt(W).','Las velocidades se calculan con cada masa y el mismo CL.'],
 [test('Alcance',f'{f(Krange)}*(sqrt(6200*9.80665)-sqrt(5100*9.80665))','m'),test('Tiempo',f'{f(CL/CD)}/(9.80665*1.72e-5)*log(6200/5100)','s'),test('Vi',f'sqrt(2*6200*9.80665/({f(rh)}*34*{f(CL)}))','m/s'),test('Vf',f'sqrt(2*5100*9.80665/({f(rh)}*34*{f(CL)}))','m/s')],
 'El avión se ralentiza al aligerarse; multiplicar la duración por Vi no da el alcance de esta ley.','Integrar V(W)/(g cT D(W)) por cuadratura y verificar Vf/Vi=sqrt(mf/mi).','Óptimo condicionado a consumo constante, ausencia de límites y polar invariable.','ADVANCED')

V=118;av=.5*rh*V**2*pol.S*pol.cd0;bv=2*pol.k/(rh*V**2*pol.S)
Eexpr=f'(atan(6200*9.80665*sqrt({f(bv)}/{f(av)}))-atan(5100*9.80665*sqrt({f(bv)}/{f(av)})))/(9.80665*1.72e-5*sqrt({f(av*bv)}))'
add(12,'Reactor a TAS constante',r'Repita la misión de masas 6200 a 5100 kg conservando TAS $118\SIu{m/s}$ y altitud 5000 m. Determine autonomía, alcance y CL inicial y final.',
 r'$S=34\SIu{m^2}$, polar $0.023+0.043C_L^2$, $c_T=1.72\times10^{-5}$ en SI.','Tiempo, alcance y cambio de sustentación adimensional.','Ruta horizontal en calma; TAS fija.','Misma densidad y polar; T=D y masa variable.','Integral arcotangente de resistencia cuadrática en peso',
 [r'D=A_V+B_VW^2',r'E=[\arctan(W\sqrt{B_V/A_V})]_{W_f}^{W_i}/(g_0c_T\sqrt{A_VB_V})',r'R_a=VE'],
 ['Se recalculan A_V y B_V, que no tienen las mismas dimensiones que A y B de la curva D(V).','Se integra 1/(A_V+B_V W²), sin imponer eficiencia constante.','Se calculan CL extremos con el mismo qS.'],
 [test('Tiempo',Eexpr,'s'),test('Alcance',f'118*({Eexpr})','m'),test('CL inicial',f'2*6200*9.80665/({f(rh)}*118**2*34)'),test('CL final',f'2*5100*9.80665/({f(rh)}*118**2*34)')],
 'La eficiencia cambia durante el consumo aunque la TAS no cambie.','Resolver la ODE dm/dt=-cT D(m) con evento de masa final y comparar el tiempo; verificar dR/dt=118.','No se usa la fórmula logarítmica de eficiencia y velocidad simultáneamente constantes.','ADVANCED')

add(12,'Empuje constante y contabilidad de masa',r'Una fase utiliza empuje constante de $17\SIu{kN}$ durante 38 minutos con $c_T=1.6\times10^{-5}\SIu{kg/(N\,s)}$. La masa inicial es 9800 kg y la masa seca 8600 kg. Determine combustible gastado y restante y el tiempo máximo antes de masa seca.',
 r'$T=17000\SIu N$, $t=2280\SIu s$, $m_i=9800\SIu{kg}$, $m_{seco}=8600\SIu{kg}$.','Gasto de fase, remanente y duración máxima.','Escalares de masa y tiempo; el mantenimiento de vuelo debe comprobarse aparte.','cT y T constantes, sin otra pérdida de masa ni reservas.','Integración lineal de gasto constante',
 [r'm_f=m_i-c_TTt',r't_{max}=(m_i-m_{seco})/(c_TT)'],
 ['Se calcula la masa de combustible inicial por diferencia de masas.','Se integra gasto constante durante el intervalo y se resta de la carga inicial.','Se comprueba que la masa final no cae por debajo de la seca.'],
 [test('Combustible gastado','1.6e-5*17000*2280','kg'),test('Remanente','9800-8600-1.6e-5*17000*2280','kg'),test('Tiempo máximo','(9800-8600)/(1.6e-5*17000)','s')],
 'La ley de consumo está cerrada, pero la velocidad de equilibrio puede cambiar con la masa.','Comparar gasto por segundo por tiempo y fracción del combustible inicial; comprobar cero remanente en tmax.','No prueba que el empuje sea suficiente en toda la fase ni incluye reserva.','BASIC')

add(13,'Vx y Vy de un reactor docente',r'Con los parámetros del problema de vuelo nivelado y empuje $8200\SIu N$, calcule Vx y Vy aproximadas a 5000 m, tasas en ambos puntos y ángulo en Vx.',
 r'$m=6200\SIu{kg}$, $A$ y $B$ calculados con la polar docente; $T=8200\SIu N$.','Óptimos de ángulo y tasa.','Trayectoria aérea; TAS y gamma positivo en ascenso.','Ángulo pequeño, L≈W, empuje constante con V y polar fija.','Maximización de excesos de empuje y potencia',
 [r'V_x=(B/A)^{1/4}',r'V_y^2=[T+\sqrt{T^2+12AB}]/(6A)',r'\dot h=(T-D)V/W'],
 ['El máximo ángulo reduce D a su mínimo.','El máximo de V(T-D) se deriva por separado y se toma la raíz positiva.','Se evalúan las fuerzas en cada velocidad y se revisa pérdida.'],
 [test('Vx',f'({f(BB)}/{f(A)})**(1/4)','m/s'),test('Vy',f'sqrt((8200+sqrt(8200**2+12*{f(A*BB)}))/(6*{f(A)}))','m/s'),test('Seno gamma en Vx',f'(8200-2*sqrt({f(A*BB)}))/(6200*9.80665)')],
 'El óptimo de tasa se encuentra a otra velocidad que el de exceso de empuje.','Optimización numérica acotada de las dos funciones objetivo y sustitución en sus derivadas.','Las tasas son aproximadas; un trim de ascenso exacto usa L=W cos(gamma).','INTERMEDIATE')

Dmin=mass*G/pol.ld(pol.cl_ld());sigma=(Dmin/18000)**(1/.8);rhceil=RHO0*sigma
hceil=brentq(lambda z:isa(z)[2]-rhceil,0,20000)
add(13,'Techo por una ley de pérdida de empuje',r'Un reactor docente dispone de $T_{max}=18\,000\sigma^{0.8}\SIu N$. Para masa 6200 kg y la polar anterior, encuentre densidad y altitud del techo absoluto ideal.',
 r'$C_{D0}=0.023$, $k=0.043$, $\rho_0=1.225\SIu{kg/m^3}$.','sigma, densidad y altitud.','Vuelo horizontal óptimo de resistencia en atmósfera ISA.','Polar constante, óptimo admisible, sin límite anterior de Mach o control.','Igualdad entre empuje máximo y resistencia mínima',
 [r'D_{min}=2W\sqrt{C_{D0}k}',r'\sigma=(D_{min}/18000)^{1/0.8}',r'\rho(h)=\rho_0\sigma'],
 ['Se calcula la mínima resistencia con el peso de la condición.','Se invierte la ley de empuje para obtener densidad relativa.','Se busca la altitud por capas ISA, sin extrapolar la troposfera.'],
 [test('Densidad relativa',f'({f(Dmin)}/18000)**(1/.8)'),test('Densidad techo',f'1.225*({f(Dmin)}/18000)**(1/.8)','kg/m^3'),test('Altitud techo',f(hceil),'m')],
 'El resultado es techo por empuje del modelo; no es un límite operativo certificado.','Recalcular ISA a la altura encontrada y comprobar Tmax/Dmin=1. La altura es una raíz numérica; su prueba no se reduce al replay de su literal.','Se requiere verificar velocidad de techo, CLmax y límites adicionales.','ADVANCED')

add(14,'Carga, radio y pérdida en viraje',r'Un avión de 2800 kg vira a $78\SIu{m/s}$ y $42^\circ$ de alabeo a densidad $0.98\SIu{kg/m^3}$. Con S=25 m² y CLmax=1.5, calcule n, radio, razón de giro y margen sobre pérdida.',
 r'$m=2800$, $V=78$, $\phi=42^\circ$, $\rho=0.98$, $S=25$ en SI.','n, R, razón y velocidad de pérdida.','Viraje coordinado nivelado en calma; componentes horizontales centrípetas.','Velocidad y altura constantes; empuje suficiente se comprueba aparte.','Equilibrio vertical y centrípeto',
 [r'n=1/\cos\phi',r'R=V^2/(g_0\tan\phi)',r'\dot\chi=g_0\tan\phi/V',r'V_{stall,n}=\sqrt{2nW/(\rho SC_{Lmax})}'],
 ['Se calcula n antes de la velocidad de pérdida.','El radio usa TAS y el ángulo en radianes dentro de trigonometría.','La razón se obtiene en rad/s y puede convertirse a grados/s.'],
 [test('Factor de carga','1/cos(42*pi/180)'),test('Radio','78**2/(9.80665*tan(42*pi/180))','m'),test('Razón de giro','9.80665*tan(42*pi/180)/78','1/s'),test('Pérdida en viraje','sqrt(2*2800*9.80665/(cos(42*pi/180)*.98*25*1.5))','m/s')],
 'Una velocidad mayor que pérdida en vuelo recto puede ser insuficiente en viraje.','Comprobar n g sin(phi)=V²/R y que CL requerido no excede 1.5.','No se ha impuesto un límite estructural ni comprobado potencia disponible.','INTERMEDIATE')

add(14,'Viraje sostenido limitado por empuje',r'A TAS 110 m/s, una aeronave de 6200 kg a 5000 m dispone de 8200 N. Use S=34 m², polar 0.023+0.043CL², CLmax=1.6 y n estructural=3.2. Determine la carga sostenida máxima a esa velocidad.',
 r'Condiciones y polar del reactor docente; densidad ISA a 5000 m.','Límites por motor, sustentación y estructura.','Viraje nivelado y coordinado; fuerzas en viento.','Empuje independiente de alabeo y polar sin resistencia adicional de coordinación.','Intersección de tres restricciones',
 [r'n_T=\sqrt{(T-AV^2)V^2/B}',r'n_L=\rho V^2SC_{Lmax}/(2W)',r'n_{max}=\min(n_T,n_L,n_{estructural})'],
 ['Se calcula el margen de empuje después del término parásito.','Se convierte ese margen a carga mediante el término cuadrático.','Se compara con sustentación máxima y estructura; se identifica la frontera activa.'],
 [test('n por empuje',f'sqrt((8200-{f(A)}*110**2)*110**2/{f(BB)})'),test('n por sustentación',f'{f(rh)}*110**2*34*1.6/(2*6200*9.80665)'),test('Límite estructural','3.2')],
 'La menor frontera determina carga sostenida; una carga instantánea superior puede consumir energía.','Evaluar D(V,nmax) y comprobar que no supera T, además de CL y estructura.','No se ha buscado el óptimo sobre todas las velocidades.','ADVANCED')

pr=Polar(18.2,.025,.048,1.65);eta=.81;cp=.305/3.6e6;CL=pr.cl_ld();ld=pr.ld(CL)
add(16,'Alcance de un avión de hélice',r'Un avión docente pasa de 1760 a 1440 kg en crucero con CL constante de máximo alcance. Tiene S=18.2 m², polar 0.025+0.048CL², rendimiento 0.81 y consumo 0.305 kg/kWh. Determine alcance ideal.',
 r'$m_i=1760\SIu{kg}$, $m_f=1440\SIu{kg}$, $c_P=0.305/(3.6\times10^6)\SIu{kg/J}$.','CL óptimo, eficiencia y alcance.','Vuelo horizontal en calma; velocidad aérea adaptada a masa.','Rendimiento, consumo y polar constantes; fase cuasiestacionaria.','Breguet por potencia al eje',
 [r'C_L=\sqrt{C_{D0}/k}',r'R_a=\eta_p(C_L/C_D)\ln(m_i/m_f)/(g_0c_P)'],
 ['La conversión de kWh a J se realiza antes de integrar.','Para hélice se maximiza CL/CD, a diferencia del alcance del reactor a densidad fija.','Se evalúa el logaritmo de masas sin sustituir diferencia de masas por razón.'],
 [test('Eficiencia máxima','1/(2*sqrt(.025*.048))'),test('Alcance',f'.81*{f(ld)}/(9.80665*({f(cp)}))*log(1760/1440)','m')],
 'El alcance ideal no contiene densidad explícita, aunque la capacidad de mantener la condición sí depende de ella.','Cuadratura de eta/(g cP D(W)) y comprobación dimensional de eta/(g cP) como longitud.','Sin reservas, ascenso ni variación de rendimiento; no es alcance operativo.','INTERMEDIATE')

rhpr=isa(2500)[2];CL=pr.cl_minpower();CD=pr.cd(CL)
Eexpr=f'2*.81/(9.80665*{f(cp)})*sqrt({f(rhpr)}*18.2/2)*({f(CL)}**1.5/{f(CD)})*(1/sqrt(1440*9.80665)-1/sqrt(1760*9.80665))'
add(16,'Autonomía de hélice a densidad fija',r'Con los mismos parámetros del avión de hélice, calcule autonomía entre 1760 y 1440 kg a 2500 m ISA y CL de máxima autonomía. Compruebe si CLmax=1.65 permite ese óptimo.',
 r'$\eta_p=0.81$, consumo $0.305\SIu{kg/kWh}$, polar $0.025+0.048C_L^2$.','CL y autonomía.','Crucero horizontal en calma; TAS decrece con masa.','Densidad fija, consumo y eficiencia constantes.','Integral de potencia con W^(-3/2)',
 [r'C_L=\sqrt{3C_{D0}/k}',r'E=\frac{2\eta_p}{g_0c_P}\sqrt{\frac{\rho S}{2}}\frac{C_L^{3/2}}{C_D}(W_f^{-1/2}-W_i^{-1/2})'],
 ['Se deriva el máximo de CL^(3/2)/CD y se comprueba su dominio.','Se integra gasto proporcional a W^(3/2) bajo esta ley de velocidad.','Se presenta tiempo en segundos y horas sin alterar el consumo original.'],
 [test('CL de autonomía','sqrt(3*.025/.048)'),test('Autonomía',Eexpr,'s')],
 'La mayor autonomía se obtiene a CL mayor que en máximo alcance y a menor velocidad.','Cuadratura de 1/(cP Peje(m)) con V(m) y comparación con la primitiva.','La eficiencia constante puede dejar de ser adecuada cerca de baja velocidad.','ADVANCED')

add(15,'Potencia al eje, útil y gasto',r'Un motor entrega 205 kW con rendimiento de hélice 0.77 y TAS 62 m/s. Para consumo 0.285 kg/kWh, determine potencia útil, empuje y gasto. Explique por qué la misma fórmula de empuje no vale al reposo.',
 r'$P_{eje}=205\,000\SIu W$, $\eta_p=0.77$, $V=62\SIu{m/s}$.','Potencia de empuje, T y gasto.','Empuje alineado con velocidad aérea.','Condición de crucero; rendimiento y consumo dados para este punto.','Conversión entre potencia y empuje',
 [r'P_T=\eta_pP_{eje}',r'T=P_T/V',r'\dot m_f=c_PP_{eje}'],
 ['Se aplica eficiencia una sola vez.','Se divide potencia útil por TAS para obtener fuerza.','El gasto usa potencia al eje porque así se define el consumo.'],
 [test('Potencia útil','.77*205000','W'),test('Empuje','.77*205000/62','N'),test('Gasto','.285*205/3600','kg/s')],
 'El motor consume según su potencia al eje; el rendimiento de hélice convierte sólo la parte útil para avance.','Verificar T V/P_eje=0.77 y convertir gasto a kg/h: 0.285 por 205 kW.','A V=0 falla la hipótesis de eficiencia constante; se necesita empuje estático finito.','BASIC')

tk=Polar(19,.034,.052,1.8);mass=1620;rh0=1.225;CLg=.62;mu=.028;T=5200;target=34
a0=T/mass-mu*G;a2=rh0*tk.S/(2*mass)*(mu*CLg-tk.cd(CLg))
sexpr=f'log(({f(a0)}+({f(a2)})*34**2)/{f(a0)})/(2*({f(a2)}))'
add(17,'Carrera de despegue con reacción variable',r'Calcule carrera hasta 34 m/s terrestres para un avión de 1620 kg, S=19 m², empuje 5200 N y rodadura 0.028. Use densidad 1.225, CL de carrera 0.62 y polar 0.034+0.052CL², sin viento.',
 r'Todos los datos están en SI; actitud de carrera fija.','Distancia y condición de contacto.','Pista horizontal; avance terrestre y aire en calma.','Masa y empuje constantes; reacción N=W-L no negativa.','Integral logarítmica de a0+a2V²',
 [r'a_0=T/m-\mu_rg_0',r'a_2=\rho S(\mu_rC_L-C_D)/(2m)',r's=[\ln((a_0+a_2V_f^2)/a_0)]/(2a_2)'],
 ['Se calcula la sustentación durante la carrera, sin imponer L=W.','Se forma la aceleración y se comprueba positiva en todo el intervalo.','Se integra V/a(V) y se compara con el modelo de aceleración constante como estimación, no como igualdad.'],
 [test('Carrera',sexpr,'m'),test('Normal final','1620*9.80665-.5*1.225*34**2*19*.62','N'),test('Aceleración inicial',f(a0),'m/s^2')],
 'La reducción de reacción al aumentar velocidad disminuye rodadura, mientras la resistencia aumenta.','Cuadratura directa de V/a y marcha temporal con paso decreciente.','No incluye rotación ni obstáculo y la velocidad final es una condición del ejercicio.','ADVANCED')

land=ground_roll(tk,1620,1.225,31,lambda v:0,.32,.18,braking=True)
b0=.32*G;b2=1.225*19/(2*1620)*(tk.cd(.18)-.32*.18)
add(18,'Frenado con sustentación residual',r'El avión docente de 1620 kg toma a 31 m/s en calma. Con empuje nulo, CL residual 0.18, polar 0.034+0.052CL² y coeficiente de freno 0.32, determine carrera hasta reposo.',
 r'$S=19\SIu{m^2}$, $\rho=1.225\SIu{kg/m^3}$, $\mu_b=0.32$.','Distancia y desaceleraciones extremas.','Pista horizontal; velocidad terrestre positiva.','Modelo de Coulomb, masa y coeficientes constantes; freno aplicado inmediatamente.','Cuadratura de velocidad sobre desaceleración',
 [r'b=\mu_bg_0+\rho S(C_D-\mu_bC_L)V^2/(2m)',r's_b=\int_0^{V_0}V/b(V)\,\dd V'],
 ['Se distingue b positiva de Vdot negativa.','La sustentación residual reduce carga normal y capacidad de frenado.','Se integra hasta cero sin añadir otra distancia aérea.'],
 [test('Carrera',f'log(({f(b0)}+({f(b2)})*31**2)/{f(b0)})/(2*({f(b2)}))','m'),test('Desaceleración inicial',f'{f(b0)}+({f(b2)})*31**2','m/s^2'),test('Desaceleración final',f(b0),'m/s^2')],
 'Con estos coeficientes, el término aerodinámico puede disminuir la desaceleración neta al descargar las ruedas.','Comparar con ground_roll y comprobar el trabajo de resistencia más frenos frente a energía cinética inicial.','No incluye demora de freno, antideslizamiento ni temperatura.','INTERMEDIATE')

kt=.94*.21*4.0*(1-.32);aa=5.2+kt;hn=(5.2*.25+kt*3.4-.08)/aa
add(19,'Punto neutro con sustentación de cola',r'Calcule punto neutro y margen con aw=5.2, at=4.0, St/S=0.21, eta=0.94, gradiente de estela 0.32, hac=0.25, ht=3.4, contribución de fuselaje Cm_alpha=0.08 y CG h=0.38.',
 r'Pendientes por radián; posiciones adimensionales hacia atrás desde el mismo origen.','hn, margen y Cm_alpha total.','Coordenada h hacia atrás; momento positivo morro arriba.','Aerodinámica lineal, mando fijo y presión de cola proporcional a presión de referencia.','Suma de pendientes con brazo de cola variable',
 [r'K_t=\eta_t(S_t/S)a_t(1-\varepsilon_\alpha)',r'h_n=(a_wh_{ac}+K_th_t-C_{m\alpha,f})/(a_w+K_t)',r'SM=h_n-h,\quad C_{m\alpha}=-(a_w+K_t)SM'],
 ['Se conserva la contribución de cola en la pendiente total de sustentación.','Se plantea Cm_alpha=0 antes de despejar h.','Se compara el CG con el punto neutro y se calcula la pendiente restauradora.'],
 [test('Punto neutro',f(hn)),test('Margen',f'{f(hn)}-.38'),test('Pendiente total',f'-{f(aa)}*({f(hn)}-.38)','1/radian')],
 'Margen positivo equivale a pendiente negativa si la pendiente de sustentación total es positiva.','Evaluar aw(h-hac)-Kt(ht-h)+Cm_alpha_f directamente y comparar con -a SM.','Sólo mando fijo; no contempla efectos de potencia ni elevador libre.','ADVANCED')

add(19,'Cambio de trim al mover el centro de gravedad',r'En un modelo con a=5.6/rad, el CG se desplaza de h=0.32 a h=0.39 y el punto neutro permanece hn=0.48. Para alpha=0.08 rad, Cm0=0.035 y Cm_delta=-1.0/rad, calcule los elevadores de trim.',
 r'La posición h aumenta hacia atrás. Se mantienen Cm0 y pendiente total sólo para este modelo docente.','Pendientes de estabilidad y dos mandos de trim.','Momento positivo morro arriba y elevador positivo según Cm_delta dado.','Modelo lineal local; mismo alpha y potencia.','Margen estático y equilibrio de momentos',
 [r'C_{m\alpha}=a(h-h_n)',r'\delta_e=-(C_{m0}+C_{m\alpha}\alpha)/C_{m\delta_e}'],
 ['Se calculan por separado los márgenes antes y después.','Se convierte cada margen en pendiente Cm_alpha.','Se evalúa el mando que anula el momento a la incidencia prescrita.'],
 [test('Cm_alpha anterior','5.6*(.32-.48)','1/radian'),test('Cm_alpha posterior','5.6*(.39-.48)','1/radian'),test('Elevador anterior','.035+5.6*(.32-.48)*.08','radian'),test('Elevador posterior','.035+5.6*(.39-.48)*.08','radian')],
 'El desplazamiento retrasado reduce la tendencia restauradora y cambia el mando necesario.','Sustituir cada delta en Cm y comprobar cero; ambos márgenes siguen siendo positivos.','Mover CG puede cambiar Cm0 y otros coeficientes en un avión real; aquí se fijan por hipótesis.','INTERMEDIATE')

add(20,'Fuerza de deriva y momento de guiñada',r'Una cola vertical tiene área 3.8 m², pendiente 3.7/rad, eficiencia de presión 0.91 y brazo cuerpo x=-4.9 m. Para q=1900 Pa y beta=4 grados calcule fuerza lateral y guiñada.',
 r'$q_\infty=1900\SIu{Pa}$; $\beta=4\pi/180\SIu{rad}$.','Yv y Nv con signos.','Cuerpo x adelante, y derecha, z abajo; beta positiva hacia derecha.','Cola lineal, beta local igual a global; sin interferencia ni timón.','Fuerza lateral y traslado de momento',
 [r'Y_v=-q_\infty\eta_vS_va_v\beta',r'N_v=x_vY_v'],
 ['El resbalamiento se convierte a radianes.','Una beta positiva genera fuerza lateral negativa con este convenio.','El brazo negativo transforma esa fuerza en momento de guiñada positivo.'],
 [test('Fuerza lateral','-1900*.91*3.8*3.7*4*pi/180','N'),test('Momento de guiñada','-4.9*(-1900*.91*3.8*3.7*4*pi/180)','N*m')],
 'La cola aporta una tendencia direccional restauradora, no una demostración de amortiguamiento del modo completo.','Usar el producto vectorial r×F y comprobar el sentido de giro del morro.','No incluye fuerza de fuselaje ni interacción con ala.','BASIC')

add(21,'Autovalores de un modelo sintético',r'Para estados alpha y q, analice la matriz A=[[-0.6,1],[-3.5,-1.4]]. Determine autovalores, frecuencia natural, amortiguamiento y periodo.',
 r'alpha en radianes, q en rad/s; tiempo en segundos. Matriz docente sin aeronave asociada.','Par modal y clasificación local.','Estados longitudinales perturbados alrededor de un equilibrio.','Sistema lineal autónomo de dos estados, sin mandos ni saturación.','Polinomio característico de segundo orden',
 [r'\lambda^2-\operatorname{tr}(A)\lambda+\det(A)=0',r'\omega_n=\sqrt{\det A},\quad\zeta=-\operatorname{tr}(A)/(2\omega_n)',r'\omega_d=\sqrt{\det A-[\operatorname{tr}(A)/2]^2}'],
 ['Se calculan traza=-2 y determinante=4.34.','La parte real es -1 y la imaginaria se obtiene de la diferencia entre determinante y uno.','Se clasifica amortiguamiento por la parte real y se calcula periodo con omega_d.'],
 [test('Parte real','-1','1/s'),test('Frecuencia amortiguada','sqrt(4.34-1)','1/s'),test('Frecuencia natural','sqrt(4.34)','1/s'),test('Amortiguamiento','1/sqrt(4.34)'),test('Periodo','2*pi/sqrt(4.34-1)','s')],
 'La oscilación decae; el periodo no es el tiempo de reducción de su amplitud.','Comparar suma y producto de autovalores con traza y determinante y con un cálculo matricial de autovalores.','La matriz es sintética y su estabilidad no se atribuye al modelo JSBSim.','ADVANCED')

add(22,'Auditoría de una salida de simulador',r'Un registro contiene TAS=312 ft/s, resistencia=610 lbf y flujo por motor 0.19 lbm/s para dos motores idénticos. Determine TAS SI, potencia de empuje necesaria y gasto total. Explique qué datos faltan para validar la aeronave.',
 r'Conversiones exactas: ft=0.3048 m, lbm=0.45359237 kg; lbf=4.448221615 N. Registro sintético para practicar unidades.','Velocidad, potencia y gasto.','Canal de resistencia positiva en viento; velocidad aérea.','Dos motores iguales; el dato de flujo es por motor, no del conjunto.','Conversión y suma de canales',
 [r'V=312(0.3048)',r'P_n=610(4.448221615)V',r'\dot m_{f,total}=2(0.19)(0.45359237)'],
 ['Se identifica el significado del canal y su unidad antes de operar.','Se usa TAS para la potencia y se suman ambos motores para gasto.','La validación necesitaría datos reales, configuración y condiciones con incertidumbre.'],
 [test('TAS','312*.3048','m/s'),test('Potencia','610*4.448221615*312*.3048','W'),test('Gasto total','2*.19*.45359237','kg/s')],
 'La reproducción numérica de un canal sintético sólo enseña a interpretar unidades y alcance.','Convertir a unidades de fuerza por ft/s y comprobar el mismo producto al aplicar el factor conjunto de potencia.','No son resultados de JSBSim ejecutado ni mediciones; son datos sintéticos del enunciado.','INTERMEDIATE')

add(23,'Sensibilidad al paso y alcance de una prueba',r'Un cálculo sintético produce distancias 1250.8, 1250.2 y 1250.05 m con pasos 0.2, 0.1 y 0.05 s. Estime orden observado y extrapolación si se cumple un error C dt^p. ¿Prueba esto fidelidad física?',
 r'Tres distancias sintéticas, mismo problema y condiciones.','Orden p, límite extrapolado y error estimado del último resultado.','Distancia escalar de trayectoria en el mismo sistema de referencia.','Régimen asintótico de una sola potencia de paso y errores de otro origen despreciables.','Extrapolación de Richardson condicionada',
 [r'p=\log_2[(s_h-s_{h/2})/(s_{h/2}-s_{h/4})]',r's_*=s_{h/4}+(s_{h/4}-s_{h/2})/(2^p-1)'],
 ['Las diferencias sucesivas son 0.6 y 0.15 m; su cociente es cuatro.','Se obtiene p=2 y se aplica la extrapolación bajo la hipótesis asintótica.','La diferencia respecto al límite es una estimación de discretización, no de error físico total.'],
 [test('Orden','log((1250.8-1250.2)/(1250.2-1250.05))/log(2)'),test('Extrapolación','1250.05+(1250.05-1250.2)/(4-1)','m'),test('Error último','abs(1250.05-1250)','m')],
 'Una secuencia coherente con segundo orden puede converger a la solución de un modelo físicamente inadecuado.','Sustituir s*=1250 y verificar que (s-s*)/dt² es constante en los tres datos.','Datos sintéticos; tres puntos no garantizan el régimen asintótico ni validan un simulador.','ADVANCED')

# Integración y nivel de examen: contextos y leyes distintos de los ejercicios de base.
pj=Polar(47,.024,.045,1.5);rj=isa(5500)[2];clj=pj.cl_jet_range();ldj=pj.ld(clj);ctj=1.65e-5
Kj=2*ldj/(G*ctj)*math.sqrt(2*G/(rj*pj.S*clj))
mA=(math.sqrt(9200)-700000/Kj)**2;mB=mA-900;mF=(math.sqrt(mB)-700000/Kj)**2
add(12,'Ida, descarga y retorno sin repostar',r'Una misión de reactor parte con 9200 kg, de los que 1600 kg son combustible y 900 kg carga que se entrega tras 700 km. Regresa otros 700 km sin repostar. Cada tramo conserva CL de máximo alcance a 5500 m ISA. Calcule masas de enlace, combustible final y tiempos.',
 r'$S=47\SIu{m^2}$, polar $0.024+0.045C_L^2$, $c_T=1.65\times10^{-5}\SIu{kg/(N\,s)}$; masa seca inicial 7600 kg y tras descarga 6700 kg.','Masas tras cada fase, reserva remanente y duración.','Ruta horizontal de ida y vuelta en calma.','Se omiten ascensos y consumos en tierra sólo en este ejercicio; misma polar tras descargar; ley CL constante en cada tramo.','Breguet de raíces e integración temporal por fases',
 [r'R=K_m(\sqrt{m_i}-\sqrt{m_f})',r'm_{f,A}=(\sqrt{m_0}-R_A/K_m)^2',r'm_{i,B}=m_{f,A}-m_{carga}',r'm_{f,B}=(\sqrt{m_{i,B}}-R_B/K_m)^2',r'E_j=(C_L/C_D)\ln(m_{i,j}/m_{f,j})/(g_0c_T)'],
 ['Se calcula Km con densidad y CL de la misión.','Se resuelve la masa final de ida sin mantener masa constante.','La descarga reduce masa seca y total en 900 kg, pero no reduce combustible.','Se integra la vuelta desde esa nueva masa y se compara el final con 6700 kg.','Los dos tiempos se suman; las velocidades de ambos tramos varían con masa.'],
 [test('Masa final ida',f'(sqrt(9200)-700000/{f(Kj)})**2','kg'),test('Masa inicio vuelta',f'{f(mA)}-900','kg'),test('Masa final vuelta',f'(sqrt({f(mB)})-700000/{f(Kj)})**2','kg'),test('Combustible final',f'{f(mF)}-6700','kg'),test('Tiempo total',f'{f(ldj)}/(9.80665*1.65e-5)*(log(9200/{f(mA)})+log({f(mB)}/{f(mF)}))','s')],
 'La misión resulta factible por combustible si el remanente es positivo; eso no demuestra factibilidad de empuje ni reservas operativas.','Integrar cada tramo por cuadratura en masa y comprobar conservación: combustible inicial menos quemado igual a final; descarga no se cuenta como consumo.','Sin reserva reglamentaria, despegue, ascenso, viento ni resistencia de trim añadida.','EXAM_LEVEL')

pp=Polar(20.5,.027,.050,1.55);cpp=.31/3.6e6;et=.80;burn=cpp*240000*300;mcl=2050-burn;mcavg=2050-burn/2
pn=pp.power(58,mcavg,1.08);roc=(et*240000-pn)/(mcavg*G)
lp=pp.ld(pp.cl_ld());rangep=et*lp/(G*cpp)*math.log(mcl/1690)
add(16,'Ascenso y crucero con reserva de hélice',r'Un avión parte con 2050 kg, masa seca 1650 kg y 400 kg de combustible. Asciende durante 300 s a potencia al eje de 240 kW y TAS 58 m/s; después vuela a CL de máximo alcance hasta conservar 40 kg de combustible. Calcule consumo y ganancia de altura aproximada del ascenso y alcance de crucero.',
 r'$S=20.5\SIu{m^2}$, polar $0.027+0.050C_L^2$, $c_P=0.31\SIu{kg/kWh}$, $\eta_p=0.80$; densidad media de ascenso 1.08 kg/m³.','Masas de enlace, altura ganada y alcance de crucero.','Ascenso aéreo y crucero horizontal; calma.','Ascenso corto con densidad y masa media para potencia necesaria; gasto de ascenso integrado exactamente a potencia fija; crucero CL constante y rendimiento constante.','Balance de potencia y Breguet de hélice',
 [r'\Delta m_c=c_PP_{eje}t_c',r'\Delta h\simeq[\eta_pP_{eje}-D(V,\bar m,\rho)V]t_c/(\bar m g_0)',r'R=\eta_pE_{a,max}\ln(m_{fin,c}/m_{seco+reserva})/(g_0c_P)'],
 ['Se convierte consumo a kg/J antes de calcular el gasto del ascenso.','Se usa la media de masas para el balance de potencia aproximado, pero la masa final conserva todo el consumo.','La masa final del crucero es 1690 kg, que ya incluye la reserva de 40 kg.','Se calcula alcance sólo del crucero; la distancia horizontal del ascenso sería otra contribución.'],
 [test('Combustible ascenso',f'{f(cpp)}*240000*300','kg'),test('Masa tras ascenso',f'2050-{f(cpp)}*240000*300','kg'),test('Altura ganada',f'({f(et*240000-pn)})/({f(mcavg)}*9.80665)*300','m'),test('Alcance crucero',f'.80*{f(lp)}/(9.80665*{f(cpp)})*log({f(mcl)}/1690)','m')],
 'La reserva se mantiene dentro de la masa final y no se vuelve a sumar al combustible gastado.','Comprobar contabilidad de masa y que la potencia excedente sea positiva; comparar el ascenso con integrar masa variable para estimar la aproximación.','Densidad media y ángulo pequeño; no se comprueba el mapa completo de potencia en altura.','EXAM_LEVEL')

gl2=Polar(17.1,.014,.032,1.6);CL2=gl2.cl_minpower();d2=math.atan(gl2.cd(CL2)/CL2)
base=glide_integral(gl2,475,2800,500,CL2)['time'];nturn=1/math.cos(math.radians(28));ratio=nturn**(-1.5)
add(9,'Permanencia recta frente a giro de planeador',r'Dos planeadores docentes idénticos de 475 kg descienden de 2800 a 500 m ISA. Uno vuela recto y otro realiza un descenso helicoidal tendido con alabeo constante de 28 grados. Compare tiempos bajo el modelo de mínimo descenso y estime la velocidad y radio iniciales del segundo.',
 r'$S=17.1\SIu{m^2}$, polar $0.014+0.032C_L^2$, $C_{Lmax}=1.6$.','Relación de tiempos, duración y geometría inicial aproximada.','Trayectoria aérea sin viento; aproximación de descenso pequeño para el viraje.','Masa y polar constantes, n≈1/cos(phi); mismo CL de mínima potencia.','Escalado de potencia resistente con n^(3/2)',
 [r'n\simeq1/\cos\phi',r'V_n\simeq\sqrt nV_1,\quad s_n\simeq n^{3/2}s_1',r'E_n/E_1\simeq n^{-3/2}',r'R\simeq V_n^2/(g_0\tan\phi)'],
 ['Se calcula n y se verifica CL óptimo dentro de la polar admisible.','La velocidad se incrementa por sqrt(n), pero la tasa de descenso lo hace por n^(3/2).','Se integra el tiempo recto con densidad variable y se aplica el escalado del modelo tendido.','La geometría inicial utiliza la TAS de la altitud inicial.'],
 [test('Factor de carga','1/cos(28*pi/180)'),test('Relación de tiempos','cos(28*pi/180)**1.5'),test('Tiempo recto de referencia',f(base),'s'),test('Tiempo helicoidal aproximado',f'{f(base)}*cos(28*pi/180)**1.5','s')],
 'El giro reduce permanencia en aire en calma; en una térmica puede ser necesario para permanecer en la corriente ascendente.','Comprobar por cuadratura local que s_n/s_1 permanece aproximadamente n^(3/2) con el mismo modelo; no confundir con una identidad para descenso pronunciado.','El tiempo recto usa equilibrio local exacto mientras el escalado de giro es aproximado; el error de pequeño ángulo debe revisarse para mayor precisión.','EXAM_LEVEL')

gw=Polar(16.8,.013,.030,1.6);mw=460;rw=1.02;wind=-10
def ground_glide(CL):
    z=glide_exact(gw,mw,rw,CL)
    return (z['horizontal']+wind)/z['sink']
opt=minimize_scalar(lambda cl:-ground_glide(cl),bounds=(.2,1.6),method='bounded')
zopt=glide_exact(gw,mw,rw,opt.x);zcalm=glide_exact(gw,mw,rw,gw.cl_ld())
add(8,'Elegir velocidad para volver contra viento',r'Un planeador de 460 kg, S=16.8 m² y polar 0.013+0.030CL² vuela en densidad 1.02 kg/m³ con viento de cara de 10 m/s. Maximice alcance terrestre por altura dentro de 0.2<=CL<=1.6 y compare con mejor planeo en calma.',
 r'Viento horizontal uniforme y sin componente vertical; datos docentes.','CL, TAS y razón de avance terrestre óptimos.','Ruta alineada contra viento; velocidad horizontal exacta de planeo.','Equilibrios locales exactos, polar fija y dominio de CL indicado.','Optimización numérica acotada de (VH+U)/s',
 [r'G(C_L)=[V(C_L)\cos\delta(C_L)+U]/s(C_L)',r'\dd G/\dd C_L=0\quad\text{si el máximo es interior}'],
 ['Se construyen ángulo, TAS, componente horizontal y descenso para cada CL.','Se maximiza la razón terrestre en el intervalo y se comprueban ambas fronteras.','Se compara con el CL que maximiza sólo CL/CD.','Se conserva en el informe que la raíz es numérica y no se sustituye su prueba por un literal.'],
 [test('CL óptimo numérico',f(opt.x)),test('TAS óptima',f(zopt['V']),'m/s'),test('Razón de avance óptima',f(ground_glide(opt.x))),test('TAS mejor planeo en calma',f(zcalm['V']),'m/s')],
 'El viento de cara favorece una velocidad mayor que la del mejor planeo en calma bajo este modelo.','Barrido fino de CL y evaluación a ambos lados del óptimo; diferencias centradas de la función objetivo.','Resultados de optimización local acotada; no incluye cambio de densidad a lo largo de un descenso completo.','EXAM_LEVEL')

qa=Polar(38,.022,.046,1.5);rqa=isa(6000)[2];miq,mfq=7000,5700;clq=qa.cl_ld();Vq=qa.speed(miq,rqa,clq);ctq=1.7e-5
exactq=jet_fixed_v(qa,miq,mfq,rqa,Vq,ctq);wrongq=qa.ld(clq)/(G*ctq)*math.log(miq/mfq)
add(12,'Diagnóstico de una Breguet aplicada fuera de hipótesis',r'Un reactor parte de 7000 kg y termina con 5700 kg a 6000 m. Mantiene la TAS inicial de mínima resistencia. Compare el tiempo correcto con el obtenido al mantener artificialmente la eficiencia inicial constante.',
 r'$S=38\SIu{m^2}$, polar $0.022+0.046C_L^2$, $c_T=1.7\times10^{-5}$ en SI.','Tiempo exacto del modelo, aproximación y error relativo.','Crucero horizontal en calma y altitud fija.','Polar y cT constantes; TAS fija de la condición inicial, CL decreciente.','Integral arcotangente frente a una aproximación logarítmica',
 [r'E_{exacto}=\int_{W_f}^{W_i}\dd W/[g_0c_T(A_V+B_VW^2)]',r'E_{aprox}=E_{a,i}\ln(W_i/W_f)/(g_0c_T)',r'\epsilon=E_{aprox}/E_{exacto}-1'],
 ['Se obtiene V inicial con CL de mínima resistencia.','Se conserva esa velocidad para la integral de resistencia en peso, no CL.','Se calcula por separado la aproximación de eficiencia inicial y su diferencia.','Se explica que la aproximación sólo puede juzgarse por su error en este intervalo.'],
 [test('TAS mantenida',f(Vq),'m/s'),test('Tiempo correcto',f(exactq['time']),'s'),test('Tiempo aproximado',f(wrongq),'s'),test('Error relativo',f(wrongq/exactq['time']-1))],
 'Un resultado aproximado cercano no convierte las hipótesis incompatibles en una identidad; al ampliar el consumo el error puede crecer.','Integrar la ODE de masa con TAS fija y contrastar con el tiempo arcotangente.','No incluye variaciones de Mach, densidad ni consumo específico.','EXAM_LEVEL')

rho6=isa(6000)[2];T6=isa(6000)[0];p6=isa(6000)[1];a6=isa(6000)[3];M6=170/a6
qc6=p6*((1+.2*M6*M6)**3.5-1)
cas6=math.sqrt(1.4*R*288.15)*math.sqrt(5*((1+qc6/101325)**(2/7)-1))
add(3,'TAS, EAS y CAS en flujo compresible',r'Una aeronave vuela a TAS 170 m/s y 6000 m ISA. Calcule Mach, EAS y CAS con pitot ideal isentrópico subsónico. Compare CAS con EAS sin identificarlas.',
 r'$\kappa=1.4$, $R_a=287.05287\SIu{J/(kg\,K)}$, referencia de nivel del mar ISA.','Mach, EAS y CAS.','Velocidad respecto al aire; presión de impacto del pitot ideal.','Flujo subsónico isentrópico, aire perfecto, sin errores de instalación ni instrumento.','Presión de impacto y calibración estándar',
 [r'M=V/\sqrt{\kappa R_aT}',r'V_E=V\sqrt{\rho/\rho_0}',r'q_c=p[(1+0.2M^2)^{3.5}-1]',r'V_C=a_0\sqrt{5[(1+q_c/p_0)^{2/7}-1]}'],
 ['Se obtiene T, p y densidad de la misma capa ISA.','La presión de impacto no se reemplaza por presión dinámica.','Se calibra qc a condiciones estándar de superficie para obtener CAS.','IAS no se puede obtener sin errores instrumentales e instalación.'],
 [test('Mach',f(M6)),test('EAS',f'170*sqrt({f(rho6)}/1.225)','m/s'),test('Presión de impacto',f(qc6),'Pa'),test('CAS',f(cas6),'m/s')],
 'A estas condiciones CAS y EAS difieren por compresibilidad aunque el sistema de medida sea ideal.','Reconstruir qc desde CAS con la fórmula estándar y comprobar igualdad con qc local.','No aplicable a pitot supersónico ni a una IAS real sin correcciones.','EXAM_LEVEL')

add(21,'Tendencia restauradora con oscilación creciente',r'Analice el modelo sintético $\ddot x-0.24\dot x+2.25x=0$. La rigidez es positiva. Determine autovalores y tiempo de duplicación de amplitud y explique la diferencia con estabilidad estática.',
 r'Tiempo en segundos; x perturbación adimensional. Modelo mecánico docente.','Parte real e imaginaria, duplicación y clasificación.','Sistema lineal de perturbación, sin asociación a una aeronave.','Coeficientes constantes, ausencia de saturación y forzamiento.','Ecuación característica y amortiguamiento negativo',
 [r'\lambda^2-0.24\lambda+2.25=0',r'\lambda=0.12\pm i\sqrt{2.25-0.12^2}',r't_2=\ln2/0.12'],
 ['El término de rigidez se opone al desplazamiento.','El signo negativo del amortiguamiento añade energía y hace positiva la parte real.','La envolvente se duplica exponencialmente aunque la respuesta cruce cero.'],
 [test('Parte real','.12','1/s'),test('Frecuencia amortiguada','sqrt(2.25-.12**2)','1/s'),test('Duplicación','log(2)/.12','s')],
 'La restauración estática no garantiza amortiguamiento dinámico.','Suma de autovalores igual a 0.24 y producto igual a 2.25; derivar energía para ver que el término de tasa la aumenta.','Analogía lineal, no modelo identificado de incidencia del avión.','EXAM_LEVEL')

add(17,'Enlace entre carrera, transición y obstáculo',r'Un modelo académico proporciona carrera 310 m y rotación de 2.2 s a velocidad terrestre media 35 m/s. Después sigue un arco de radio 420 m hasta 7 grados y ascenso recto hasta 15 m. Calcule distancia total y compruebe si el obstáculo se alcanza dentro del arco.',
 r'$s_g=310\SIu m$, $t_R=2.2\SIu s$, $\bar V_{g,R}=35\SIu{m/s}$, $R_c=420\SIu m$, $\gamma_c=7^\circ$, $H=15\SIu m$.','Altura y avance de transición y distancia total.','Geometría de trayectoria sobre terreno en calma; pista horizontal.','Arco circular y velocidad de rotación media prescritos; no se deriva control de cabeceo.','Suma de fases con comprobación de frontera',
 [r'h_{tr}=R_c(1-\cos\gamma_c),\quad x_{tr}=R_c\sin\gamma_c',r'x_{recto}=(H-h_{tr})/\tan\gamma_c',r's_{total}=s_g+\bar V_{g,R}t_R+x_{tr}+x_{recto}'],
 ['Se calcula primero htr y se compara con H.','Como el obstáculo está por encima de la transición, se añade un tramo recto positivo.','Se suma la distancia de rotación sin confundirla con tiempo de carrera ya incluido.','La distancia obtenida es hasta la altura prescrita, no sólo separación.'],
 [test('Altura de transición','420*(1-cos(7*pi/180))','m'),test('Avance de transición','420*sin(7*pi/180)','m'),test('Distancia total','310+35*2.2+420*sin(7*pi/180)+(15-420*(1-cos(7*pi/180)))/tan(7*pi/180)','m')],
 'La geometría obliga a comprobar en qué fase se alcanza el obstáculo antes de sumar longitudes.','Dibujar el arco y verificar x²+(h-R)²=R² en la salida; comprobar continuidad de pendiente con el tramo recto.','No es distancia certificada ni incluye fallo de motor o márgenes reglamentarios.','EXAM_LEVEL')

add(18,'Aproximación y recogida antes de frenar',r'Una aproximación comienza a 18 m con ángulo de 3.5 grados. La recogida es un arco de radio 350 m hasta horizontal y la carrera posterior es 170 m. Obtenga distancia desde 18 m y efecto de añadir una demora de freno de 1.5 s a velocidad media 28 m/s.',
 r'$H=18\SIu m$, $\delta=3.5^\circ$, $R_f=350\SIu m$, $s_b=170\SIu m$.','Distancia aérea, total y demora.','Trayectoria geométrica sobre terreno en calma.','Velocidad y arco idealizados; la demora dada es una fase adicional no incluida en 170 m.','Geometría de aproximación y suma de fases',
 [r'h_f=R_f(1-\cos\delta)',r'x_a=(H-h_f)/\tan\delta+R_f\sin\delta',r's_{total}=x_a+s_b+\bar V_gt_d'],
 ['Se verifica que hf es menor que la altura inicial.','Se separan recta de aproximación y arco para no duplicar altura.','La demora añade distancia terrestre y no cambia retroactivamente la carrera dada.'],
 [test('Altura de recogida','350*(1-cos(3.5*pi/180))','m'),test('Distancia aérea','(18-350*(1-cos(3.5*pi/180)))/tan(3.5*pi/180)+350*sin(3.5*pi/180)','m'),test('Total con demora','(18-350*(1-cos(3.5*pi/180)))/tan(3.5*pi/180)+350*sin(3.5*pi/180)+170+28*1.5','m')],
 'La demora de aplicación de freno puede ser relevante aunque la desaceleración posterior sea idéntica.','Comprobar el límite de ángulo pequeño y verificar que todas las longitudes de fases son positivas.','Modelo geométrico con carrera prescrita; no predice dinámica de recogida ni actuación certificada.','EXAM_LEVEL')

add(13,'Ascenso a EAS constante y corrección energética',r'A una altitud donde rho=0.80 kg/m³ y drho/dh=-0.000090 kg/m⁴, un avión mantiene EAS=75 m/s. Su exceso de potencia dividido por peso es 6 m/s. Calcule TAS y tasa de ascenso incluyendo la aceleración de esa ley.',
 r'$\rho_0=1.225\SIu{kg/m^3}$, gradiente local dado; potencia excedente por peso 6 m/s.','TAS, dV/dh y tasa geométrica.','Trayectoria aérea y altitud local; viento nulo.','EAS constante, gradiente local de densidad y balance energético cuasiestacionario.','Altura de energía con V(h)',
 [r'V=V_E\sqrt{\rho_0/\rho}',r'\frac{\dd V}{\dd h}=-\frac{V}{2\rho}\frac{\dd\rho}{\dd h}',r'\dot h=6/[1+(V/g_0)(\dd V/\dd h)]'],
 ['Se convierte EAS a TAS con la densidad local.','Se deriva la ley de velocidad respecto a altura manteniendo EAS fija.','La energía cinética creciente consume parte de la potencia excedente.'],
 [test('TAS','75*sqrt(1.225/.80)','m/s'),test('Gradiente de TAS','-(75*sqrt(1.225/.80))/(2*.80)*(-.000090)','1/s'),test('Tasa geométrica','6/(1+(75*sqrt(1.225/.80)/9.80665)*(-(75*sqrt(1.225/.80))/(2*.80)*(-.000090)))','m/s')],
 'La tasa es menor que 6 m/s porque parte de la energía se destina a acelerar respecto al aire.','Recomponer hdot+(V/g)Vdot con Vdot=(dV/dh)hdot y recuperar 6 m/s.','Gradiente local; no se integra un ascenso completo ni se incluye variación de masa.','EXAM_LEVEL')

add(23,'Balance de combustible de un CSV sintético',r'Un registro sintético de vuelo contiene tiempos 0, 60 y 120 s y gastos totales 0.84, 0.82 y 0.80 kg/s. El combustible pasa de 510 a 411.6 kg. Contraste la pérdida con integración trapezoidal y con congelar el gasto inicial.',
 r'Gasto total del conjunto de motores; datos sintéticos creados para practicar auditoría.','Combustible integrado, discrepancia y error de gasto constante.','Escalares másicos del mismo experimento y unidad SI.','Gasto lineal entre muestras; sin repostaje ni descarga de combustible.','Cuadratura trapezoidal y conservación de masa',
 [r'\Delta m_{trap}=\sum_j(t_{j+1}-t_j)(\dot m_j+\dot m_{j+1})/2',r'\Delta m_{registro}=m_{f,0}-m_{f,120}',r'\Delta m_{const}=\dot m_0\Delta t'],
 ['Se comprueba que el gasto está referido a todos los motores.','Se integra cada intervalo con sus dos extremos.','Se compara con el descenso de contenido y se calcula por separado la aproximación congelada.'],
 [test('Integral de gasto','60*(.84+.82)/2+60*(.82+.80)/2','kg'),test('Pérdida registrada','510-411.6','kg'),test('Aproximación constante','.84*120','kg'),test('Sobreestimación','.84*120-(510-411.6)','kg')],
 'El balance de masa coincide bajo el gasto lineal supuesto; la aproximación constante sobreestima el consumo.','El gasto medio de los extremos es 0.82 kg/s y por 120 s recupera la misma pérdida.','No son datos ejecutados de JSBSim ni ensayo real; no validan un mapa de motor.','EXAM_LEVEL')

def build():
    (RDIR/'evidence/problem-bank.json').write_text(json.dumps(BANK,ensure_ascii=False,indent=2))
    print('Problemas originales:',len(BANK))
if __name__=='__main__':build()
