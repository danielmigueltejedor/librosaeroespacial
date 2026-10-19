"""Seis simulacros originales, enunciados y soluciones separados."""
from pathlib import Path
import json,math
import numpy as np
from scipy.integrate import quad
from scipy.optimize import brentq
from models import *
from problem_bank import test,f
from render_problems import solution,prose
RDIR=Path(__file__).resolve().parents[1]
EX=[]
def exam(title,time):
    e=dict(key=f'S{len(EX)+1:02}',title=title,time=time,questions=[]);EX.append(e);return e
def question(e,title,prompt,data,hyp,eqs,steps,tests,interpret,check,limits,score,frame='Cuerpo x adelante, y derecha, z abajo; NED cuando corresponda.'):
    q=dict(key=e['key']+'.'+str(len(e['questions'])+1),ch=1,title=title,prompt=prompt,data=data,unknown='Magnitudes y conclusiones solicitadas en el enunciado.',frame=frame,hyp=hyp,model=title,eqs=eqs,steps=steps,tests=tests,interpretation=interpret,independent=check,limits=limits,level='EXAM_LEVEL',score=score)
    e['questions'].append(q)

e=exam('Ejes, planeo y maniobra',120)
vb=c_body_ned(math.radians(12),math.radians(6),math.radians(25))@np.array([82.,-4.,-3.])
question(e,'Reconstrucción de velocidad y actitud',r'Un avión tiene Euler $(\phi,\theta,\psi)=(12,6,25)^\circ$ y velocidad aérea NED $(82,-4,-3)\SIu{m/s}$. Calcule velocidad cuerpo, TAS e incidencia. Explique por qué ascenso terrestre no determina el signo de w cuerpo.',
 r'Secuencia pasiva 3--2--1; viento nulo en este caso.',
 'Horizonte local fijo, convención del manual y velocidad no nula.',
 [r'\vect v_a^b=C_{bn}\vect v_a^n',r'V=\|\vect v_a\|,\quad\alpha=\operatorname{atan2}(w_a,u_a)'],
 ['Se construyen las tres rotaciones en orden y se multiplican por la velocidad NED.','Se calcula la norma y se compara antes y después de rotar.','El vector NED tiene componente abajo negativa, pero el componente cuerpo incluye la actitud.'],
 [test('u cuerpo',f(vb[0]),'m/s'),test('v cuerpo',f(vb[1]),'m/s'),test('w cuerpo',f(vb[2]),'m/s'),test('TAS','sqrt(82**2+4**2+3**2)','m/s'),test('Incidencia',f(math.atan2(vb[2],vb[0])),'radian')],
 'El ascenso se reconoce en NED; incidencia y w describen la dirección relativa al fuselaje.','Aplicar la transpuesta para recuperar el vector NED y comprobar norma y determinante.','El replay de los tres componentes literales no prueba la multiplicación: se conserva la prueba matricial de ida y vuelta.',3)
gp=Polar(17.6,.0132,.0305,1.6);m=490;cl=gp.cl_ld();gg=glide_integral(gp,m,3400,600,cl,wind=-6)
question(e,'Alcance y duración con atmósfera variable',r'Un planeador de 490 kg y S=17.6 m² desciende de 3400 a 600 m ISA manteniendo CL de mejor planeo en calma. Polar 0.0132+0.0305CL². Calcule CL, alcance aéreo, duración y alcance terrestre con viento de cara 6 m/s.',
 r'ISA troposférica con constantes generales del cuaderno; CLmax=1.6.',
 'Masa y polar constantes; equilibrio local exacto y sucesión cuasiestacionaria; viento vertical nulo.',
 [r'C_L=\sqrt{C_{D0}/k},\quad\delta=\arctan(C_D/C_L)',r'R_a=\Delta hC_L/C_D',r'E=\int_{h_f}^{h_i}\dd h/s(h),\quad R_g=R_a-6E'],
 ['Se obtiene CL y se comprueba con CLmax.','Se usa ángulo exacto para la velocidad local y descenso.','Se integra con densidad ISA y se resta el desplazamiento de viento durante todo el tiempo.'],
 [test('CL óptimo','sqrt(.0132/.0305)'),test('Alcance aéreo',f(gg['air_range']),'m'),test('Duración',f(gg['time']),'s'),test('Alcance terrestre',f(gg['ground_range']),'m')],
 'No se reoptimiza el vuelo para viento; se evalúa la ley explícitamente impuesta.','Comparar cuadratura con la primitiva de potencia de temperatura y comprobar que Ra/E no se confunde con la TAS inicial.','La variación lenta de TAS se omite en el balance inercial local.',4,frame='Trayectoria aérea descendente, gamma<0; ruta terrestre alineada con viento.')
question(e,'Viraje nivelado y pérdida',r'Una aeronave vuela a 84 m/s con alabeo 38 grados. Masa 3100 kg, S=27 m², rho=0.96 kg/m³ y CLmax=1.55. Calcule n, radio, razón de giro y CL requerido; indique qué falta para probar viraje sostenido.',
 r'Viraje coordinado en calma, altitud y rapidez constantes.',
 'Empuje paralelo a velocidad; se comprueba sólo geometría y sustentación, sin mapa de propulsión.',
 [r'n=1/\cos\phi,\quad R=V^2/(g_0\tan\phi)',r'\dot\chi=g_0\tan\phi/V,\quad C_L=2nmg_0/(\rho V^2S)'],
 ['La sustentación se incrementa a nW.','Se calcula la aceleración centrípeta y se obtiene el radio.','Se verifica CL y se identifica que falta resistencia y empuje disponible para sostenibilidad.'],
 [test('n','1/cos(38*pi/180)'),test('Radio','84**2/(9.80665*tan(38*pi/180))','m'),test('Razón','9.80665*tan(38*pi/180)/84','1/s'),test('CL requerido','2*3100*9.80665/(cos(38*pi/180)*.96*84**2*27)')],
 'La geometría puede ser posible por sustentación y aun no ser sostenible por motor.','Comprobar n g sin(phi)=V²/R y CL<=CLmax.','Sin límite estructural ni trim de momentos.',3)

e=exam('Crucero de reactor y leyes de pilotaje',150)
pj=Polar(52,.024,.044,1.5);rho=isa(6500)[2];ct=1.68e-5;cl=pj.cl_ld();ld=pj.ld(cl)
m0=11400;tA=2700;mA=m0*math.exp(-G*ct/ld*tA)
ra=jet_fixed_cl(pj,m0,mA,rho,cl,ct)
V=175;av=.5*rho*V*V*pj.S*pj.cd0;bv=2*pj.k/(rho*V*V*pj.S)
phaseB=jet_fixed_v(pj,mA,9300,rho,V,ct)
question(e,'Primera fase de autonomía',r'Un reactor de 11400 kg y masa seca 9300 kg vuela 45 minutos a 6500 m ISA con CL de máxima autonomía. S=52 m², polar 0.024+0.044CL² y cT=1.68e-5 kg/(N s). Calcule masa final, distancia y velocidades extremas.',
 r'Se conservan altitud y CL; no hay viento ni reserva en este cálculo.',
 'Polar y consumo constantes; T=D; masa variable y vuelo cuasiestacionario.',
 [r'C_L=\sqrt{C_{D0}/k}',r'm_f=m_i\exp[-g_0c_Tt/(C_L/C_D)]',r'R=K_m(\sqrt{m_i}-\sqrt{m_f})'],
 ['Se utiliza CL de autonomía de reactor.','Se invierte la integral temporal logarítmica para encontrar masa.','Se integra la velocidad variable para alcance y se calculan ambos extremos de TAS.'],
 [test('Masa final',f'11400*exp(-9.80665*1.68e-5*2700/{f(ld)})','kg'),test('Distancia',f(ra['range']),'m'),test('Vi',f(ra['Vi']),'m/s'),test('Vf',f(ra['Vf']),'m/s')],
 'La velocidad disminuye con masa aunque la altitud no cambie.','Integrar dm/dt y dx/dt con la ley CL fija y comprobar mA mayor que masa seca.','Se omiten ascenso y transitorios de mando.',4,frame='Ruta horizontal y ejes viento; TAS variable.')
question(e,'Segunda fase a TAS fija',r'Desde la masa final anterior, el reactor pasa a TAS 175 m/s a la misma altitud y continúa hasta masa seca 9300 kg. Calcule duración y alcance adicionales. No mantenga artificialmente constante CL.',
 r'La fase comienza en la masa de enlace calculada; polar, S, cT y altitud de la primera fase.',
 'Cambio idealizado instantáneo de velocidad sin combustible de transición; se declara como simplificación.',
 [r'D(W)=A_V+B_VW^2',r'E=\frac{\arctan(W_i\sqrt{B_V/A_V})-\arctan(W_f\sqrt{B_V/A_V})}{g_0c_T\sqrt{A_VB_V}}',r'R=175E'],
 ['Se actualiza la masa inicial de la fase.','Se calcula el nuevo CL para cada peso con la misma TAS.','Se evalúa la integral arcotangente y se añade al tiempo y distancia de la fase anterior si se solicita misión total.'],
 [test('Tiempo adicional',f(phaseB['time']),'s'),test('Distancia adicional',f(phaseB['range']),'m'),test('Combustible de la segunda fase',f'{f(mA)}-9300','kg')],
 'Cambiar la ley de vuelo obliga a cambiar la integral, conservando masa de enlace.','ODE de masa a TAS fija con evento final 9300 kg y comparación con arcotangente.','La aceleración entre leyes no se ha modelado y debe añadirse en una misión física más precisa.',4,frame='Vuelo horizontal en calma; TAS constante y CL variable.')
question(e,'Comprobación de dos restricciones',r'Con los mismos datos, compruebe al inicio de la fase a TAS fija si CLmax=1.5 y empuje disponible 10500 N permiten sostener esa condición. Explique qué otra información se necesitaría.',
 r'Use masa final de fase A, TAS 175 m/s y densidad ISA a 6500 m.',
 'Empuje disponible dado en ese punto; sin margen añadido ni resistencia de coordinación.',
 [r'C_L=2mg_0/(\rho V^2S)',r'D=q_\infty S(C_{D0}+kC_L^2)',r'M_T=T_d-D'],
 ['Se calcula CL con la masa real de enlace.','Se evalúa resistencia y margen de empuje.','Ambas desigualdades son necesarias; faltan trim, Mach y otras limitaciones.'],
 [test('CL de entrada',f'2*{f(mA)}*9.80665/({f(rho)}*175**2*52)'),test('Resistencia',f(pj.drag(175,mA,rho)),'N'),test('Margen de empuje',f(10500-pj.drag(175,mA,rho)),'N')],
 'Un margen positivo de empuje no demuestra estabilidad ni autoridad de elevador.','Sustituir T=D+MT y comprobar la magnitud de cada componente de resistencia.','El empuje se da sólo para esta condición, sin mapa completo.',2)

e=exam('Hélice, potencia y combustible de misión',135)
pp=Polar(21.4,.028,.049,1.6);cp=.30/3.6e6;eta=.78;burn=cp*230000*420;mass=2180-burn
cl=pp.cl_ld();ld=pp.ld(cl);mf=1760;res=prop_fixed_cl(pp,mass,mf,isa(2200)[2],cl,cp,eta)
question(e,'Consumo de ascenso y masa de enlace',r'Un avión parte con 2180 kg, de los que 420 kg son combustible. Mantiene potencia al eje 230 kW durante siete minutos, consumo 0.30 kg/kWh y eficiencia 0.78. Calcule gasto, combustible consumido y masa al comenzar crucero.',
 r'No hay otra pérdida de masa; el resto de datos se usará en el siguiente problema.',
 'Potencia y consumo específicos constantes en esa fase; no se calcula aquí la altura.',
 [r'\dot m_f=c_PP_{eje}',r'm_{fin}=m_0-c_PP_{eje}t'],
 ['Se distingue potencia al eje de potencia de empuje.','Se convierte tiempo a horas o consumo a kg/J de forma coherente.','Se actualiza masa y combustible antes de calcular crucero.'],
 [test('Gasto','.30*230/3600','kg/s'),test('Combustible ascenso','.30*230*7/60','kg'),test('Masa de enlace','2180-.30*230*7/60','kg')],
 'El rendimiento de hélice no modifica el gasto definido por potencia al eje en este ejercicio.','Repetir en kg/kWh por kW y horas y comprobar la misma masa consumida.','La potencia constante no fija por sí sola la tasa de ascenso.',3)
question(e,'Crucero con combustible de reserva',r'Desde esa masa de enlace, el avión vuela a 2200 m ISA con CL de máximo alcance. S=21.4 m² y polar 0.028+0.049CL². Debe conservar 60 kg de combustible. Calcule masa final, alcance y tiempo, con eficiencia y consumo anteriores.',
 r'Masa seca 1760 kg; reserva 60 kg: masa final requerida 1820 kg.',
 'CL, altitud, eficiencia y consumo constantes en crucero; sin viento.',
 [r'C_L=\sqrt{C_{D0}/k}',r'R=\eta_p(C_L/C_D)\ln(m_i/m_f)/(g_0c_P)',r'E=\frac{2\eta_p}{g_0c_P}\sqrt{\frac{\rho S C_L}{2g_0}}\frac{C_L}{C_D}(m_f^{-1/2}-m_i^{-1/2})'],
 ['Se incorpora la reserva a masa final, sin quemarla.','Se utiliza CL de alcance para hélice y no CL de autonomía.','Se integra tiempo con la TAS decreciente; no se divide por una sola velocidad inicial.'],
 [test('Masa final','1760+60','kg'),test('Alcance',f(prop_fixed_cl(pp,mass,1820,isa(2200)[2],cl,cp,eta)['range']),'m'),test('Duración',f(prop_fixed_cl(pp,mass,1820,isa(2200)[2],cl,cp,eta)['time']),'s')],
 'La misión nominal termina con reserva y no al agotar el tanque.','Cuadratura en masa de avance y tiempo por gasto de potencia, verificando contabilidad de reserva.','No se comprueba aquí la potencia de crucero disponible; debe evaluarse en ambos extremos.',4,frame='Ruta horizontal en calma, TAS variable para mantener CL.')
question(e,'Comparar potencia y empuje para ascenso',r'En una condición distinta, rho=1.02 kg/m³, m=2100 kg y TAS=59 m/s, calcule potencia necesaria con la polar anterior y tasa de ascenso aproximada con potencia al eje 230 kW. Explique por qué no basta con usar empuje máximo por un coeficiente.',
 r'Eficiencia 0.78; S=21.4 m²; L≈W y polar de crucero como modelo docente.',
 'Ángulo pequeño, velocidad constante y potencia disponible en el punto.',
 [r'P_n=D(V,m,\rho)V',r'P_d=\eta_pP_{eje}',r'\dot h=(P_d-P_n)/(mg_0)'],
 ['Se calcula CL requerido a la TAS y densidad dadas.','Se obtiene resistencia y potencia necesaria.','Se resta de potencia útil y se divide por peso; empuje por un factor sigue siendo fuerza.'],
 [test('Potencia necesaria',f(pp.power(59,2100,1.02)),'W'),test('Potencia disponible','.78*230000','W'),test('Tasa de ascenso',f((.78*230000-pp.power(59,2100,1.02))/(2100*G)),'m/s')],
 'La potencia al eje excedente no se puede comparar directamente con DV sin aplicar rendimiento.','Comprobar que Tdis=eta Peje/V y (Tdis-D)V/W dan la misma tasa.','No incluye corrección de aceleración ni variación de eficiencia.',3)

e=exam('Operaciones y margen estático',120)
tk=Polar(20,.033,.050,1.8);rr=ground_roll(tk,1720,1.17,32,lambda v:5500,.03,.60,wind=5)
question(e,'Carrera con viento de cara',r'Un avión de 1720 kg debe alcanzar TAS 37 m/s con viento de cara 5 m/s. S=20 m², rho=1.17 kg/m³, empuje 5500 N, rodadura 0.03 y CL de carrera 0.60; polar 0.033+0.050CL². Calcule velocidad terrestre final y carrera por integración.',
 r'Vaire=Vsuelo+5 m/s; pista horizontal.',
 'Empuje finito constante; coeficientes de carrera fijos y reacción no negativa.',
 [r'V_{g,f}=37-5',r'a(V_g)=[T-D(V_g+5)-\mu(W-L(V_g+5))]/m',r's=\int_0^{32}V_g/a(V_g)\,\dd V_g'],
 ['Se obtiene la velocidad terrestre objetivo sin confundirla con la aerodinámica.','Las fuerzas se evalúan con Vg+5 desde el inicio de carrera.','Se verifica aceleración y reacción y se integra distancia terrestre.'],
 [test('Velocidad terrestre final','37-5','m/s'),test('Carrera',f(rr['distance']),'m'),test('Tiempo',f(rr['time']),'s')],
 'El viento modifica tanto velocidad final terrestre como fuerzas durante la carrera.','Marcha temporal independiente y comparación con cuadratura en velocidad; no usar una simple resta de distancia por viento.','Sin rotación ni obstáculo; no es prestación certificada.',4,frame='Pista terrestre y velocidad aérea alineada.')
ll=ground_roll(tk,1720,1.17,29,lambda v:0,.29,.16,braking=True)
question(e,'Frenada y demora',r'En calma, la misma aeronave toma a 29 m/s con CL residual 0.16, freno 0.29 y empuje nulo. Calcule carrera de frenado y distancia añadida por una demora de 1.2 s a velocidad media prescrita de 28 m/s.',
 r'S, densidad y polar anteriores; la demora es una fase adicional.',
 'Frenado de Coulomb, coeficientes constantes, sin pendiente ni empuje inverso.',
 [r'b=[D+\mu_b(W-L)]/m',r's_b=\int_0^{29}V_g/b(V_g)\,\dd V_g',r's_d=28(1.2)'],
 ['Se conserva la descarga normal por sustentación residual.','Se integra con desaceleración positiva.','Se añade la fase de demora con su velocidad media dada.'],
 [test('Frenado',f(ll['distance']),'m'),test('Demora','28*1.2','m'),test('Total terrestre',f(ll['distance']+28*1.2),'m')],
 'Un retraso aumenta la distancia aun cuando la eficacia posterior del freno no cambie.','Comprobar balance energético de la fase frenada y signos de normal y desaceleración.','No incluye aproximación ni recogida.',3)
kt=.9*.18*4.2*.65;aa=5.1+kt;hn=(5.1*.25+kt*3.1-.06)/aa
question(e,'CG, punto neutro y mando',r'Un modelo tiene aw=5.1, at=4.2, St/S=0.18, eta_t=0.9, epsilon_alpha=0.35, hac=0.25, ht=3.1 y Cm_alpha_f=0.06. Calcule hn, margen para h=0.35 y Cm_alpha. ¿Prueba esto estabilidad dinámica?',
 r'Pendientes por radián, posiciones hacia atrás en unidades de cuerda.',
 'Mando fijo y aerodinámica lineal; mismo datum y configuración.',
 [r'K_t=\eta_t(S_t/S)a_t(1-\varepsilon_\alpha)',r'h_n=(a_wh_{ac}+K_th_t-C_{m\alpha,f})/(a_w+K_t)',r'C_{m\alpha}=-(a_w+K_t)(h_n-h)'],
 ['Se calcula la contribución de cola a sustentación total.','Se despeja el CG neutral de la condición de pendiente nula.','Se evalúa el margen y se distingue tendencia estática de amortiguamiento.'],
 [test('Punto neutro',f(hn)),test('Margen',f(hn-.35)),test('Cm_alpha',f(-aa*(hn-.35)),'1/radian')],
 'Un margen positivo no garantiza autovalores de parte real negativa; faltan derivadas de tasa y acoplamientos.','Evaluar directamente las tres contribuciones a Cm_alpha y comprobar el mismo valor.','No determina autoridad de elevador ni estabilidad de mando libre.',3)

e=exam('Newton--Euler y estabilidad como ampliación',135)
I=np.array([[11000,0,-850],[0,16500,0],[-850,0,21000]]);om=np.array([.10,.06,-.08]);mm=np.array([700,-450,380]);acc=omega_derivative(om,mm,I)
question(e,'Momento angular con producto de inercia',r'Use Ixx=11000, Iyy=16500, Izz=21000 e Ixz=850 kg m², con entradas cruzadas negativas. Para omega=(0.10,0.06,-0.08) rad/s y momentos (700,-450,380) N m, calcule aceleraciones y compruebe el balance vectorial.',
 r'Tensor constante y momentos respecto al CG.',
 'Sólido rígido simétrico, sin masa móvil ni flujo de momento angular.',
 [r'\vect H=I\vect\omega',r'\dot{\vect\omega}=I^{-1}(\vect M-\vect\omega\times\vect H)'],
 ['Se forma el tensor con -Ixz, no con +Ixz.','Se calculan los tres componentes de H y el producto giroscópico.','Se resuelve el sistema y se recuperan los momentos por sustitución.'],
 [test('pdot',f(acc[0]),'1/s^2'),test('qdot',f(acc[1]),'1/s^2'),test('rdot',f(acc[2]),'1/s^2')],
 'Los acoplamientos impiden dividir cada momento bruto por una sola inercia.','Resolver también el bloque p,r por determinante y verificar residuo vectorial próximo a precisión de máquina.','La reproducción de literales de aceleración no sustituye esas operaciones matriciales.',4)
question(e,'Derivadas de cola vertical',r'Para q=2400 Pa, Sv=4.5 m², eficiencia 0.93, av=3.9/rad, x_v=-5.8 m y beta=2.5 grados, calcule fuerza y momento de cola. Razone el signo de Cn_beta y qué dato faltaría para amortiguamiento en guiñada.',
 r'Flujo local beta igual al global; cola detrás del CG.',
 'Cola lineal y sin interferencia; no hay timón.',
 [r'Y_v=-q_\infty\eta_vS_va_v\beta',r'N_v=x_vY_v'],
 ['Se convierte beta a radianes.','Se obtiene Y negativa y N positiva con el brazo cuerpo.','La derivada de tasa Cnr requiere cómo cambia el flujo local con r y no se deduce sólo del equilibrio estático.'],
 [test('Fuerza','-2400*.93*4.5*3.9*2.5*pi/180','N'),test('Momento','-5.8*(-2400*.93*4.5*3.9*2.5*pi/180)','N*m')],
 'La tendencia direccional restauradora no determina todo el modo lateral.','Comprobar con r×F y con la derivada analítica de N respecto a beta.','No se incluyen fuselaje ni efectos de altura de cola sobre alabeo.',3)
question(e,'Par modal y respuesta creciente',r'Como ampliación, estudie una ecuación sintética xddot+0.5 xdot+3.24x=0. Calcule autovalores, periodo y tiempo de reducción a la mitad. Compare con cambiar el signo del término de tasa.',
 r'x adimensional, tiempo en segundos; no es modelo de una aeronave identificada.',
 'Sistema lineal autónomo sin forzamiento.',
 [r'\lambda=-0.25\pm i\sqrt{3.24-0.25^2}',r'T=2\pi/\omega_d,\quad t_{1/2}=\ln2/0.25'],
 ['La parte real depende del coeficiente de tasa y su signo.','Se calcula frecuencia amortiguada y se distingue periodo de decaimiento.','Al cambiar el signo de tasa, la parte real pasa a positiva y la envolvente crece.'],
 [test('Frecuencia amortiguada','sqrt(3.24-.25**2)','1/s'),test('Periodo','2*pi/sqrt(3.24-.25**2)','s'),test('Semiamplitud','log(2)/.25','s')],
 'La rigidez positiva puede coexistir con crecimiento cuando el amortiguamiento es negativo.','Traza y determinante del sistema equivalente de dos estados y solución exponencial.','Contenido dinámico de ampliación; no se atribuye como bloque explícito a la guía oficial.',3)

e=exam('Auditoría de simulación y decisión de modelo',120)
report=json.loads((RDIR/'reports/endurance-results.json').read_text());c=report['cases'][0];initial=c['initial']
question(e,'Revisar una autonomía ejecutada',r'En el experimento original B747 de 28000 lbm, el tiempo simulado hasta agotamiento es el de los datos adjuntos. Compare con congelar el gasto inicial y con el modelo equivalente. Calcule diferencias relativas y explique por qué ninguna constituye validación experimental.',
 f"Tiempo simulado {c['simulated_time_s']:.6f} s; gasto constante {c['constant_initial_flow_time_s']:.6f} s; equivalente {c['equivalent_polar_time_s']:.6f} s. Deriva máxima de altura {c['max_height_error_m']:.3f} m; paso 0.1 s.",
 'Datos realmente ejecutados del modelo educativo, no mediciones de avión real.',
 [r'\epsilon_c=E_{const}/E_{sim}-1',r'\epsilon_{eq}=E_{eq}/E_{sim}-1'],
 ['Se distingue gasto congelado de masa variable y modelo equivalente ajustado al mismo simulador.','Se calculan diferencias con el mismo denominador.','La deriva de altura impide afirmar altitud perfectamente constante y falta refinamiento completo del paso.'],
 [test('Error de gasto constante',f(c['constant_initial_flow_time_s']/c['simulated_time_s']-1)),test('Error del equivalente',f(c['equivalent_polar_time_s']/c['simulated_time_s']-1))],
 'El ajuste comparte modelo de origen y no es evidencia experimental independiente.','Revisar el CSV y la condición de agotamiento; sumar gasto de cuatro motores e integrar combustible.','No se infiere autonomía certificada ni se oculta error de seguimiento.',4,frame='Propiedades SI del experimento; tiempo de simulación y combustible de depósitos alimentadores.')
question(e,'Potencia disponible y ejes de velocidad',r'Un registro sintético indica empuje máximo 2500 lbf, factor de tabla 0.64, TAS 340 ft/s y EAS 285 ft/s. Calcule empuje disponible, potencia correcta y error al multiplicar por EAS. Identifique el error dimensional de llamar potencia al empuje por el factor.',
 r'1 lbf=4.448221615 N y 1 ft=0.3048 m; datos sintéticos originales.',
 'Factor adimensional de empuje y velocidad alineada con empuje.',
 [r'T_d=T_{base}f',r'P_d=T_dV_{TAS}',r'P_{err}/P_d=V_{EAS}/V_{TAS}'],
 ['Se aplica el factor a fuerza, conservando unidades de fuerza.','Se convierte TAS y se calcula potencia.','Se cuantifica la subestimación que produciría EAS en ese producto.'],
 [test('Empuje disponible','2500*.64*4.448221615','N'),test('Potencia correcta','2500*.64*4.448221615*340*.3048','W'),test('Error relativo por EAS','285/340-1')],
 'El gráfico puede usar EAS como abscisa, pero la ordenada de potencia física utiliza TAS.','Verificar dimensionalmente N por m/s y comparar ambas conversiones completas.','El ejemplo no atribuye estas cifras a PT6 ni a un modelo ejecutado.',3)
question(e,'Comparar flaps sin inventar un ensayo',r'Dos configuraciones docentes tienen la misma sustentación requerida CL=0.85. Limpia: CD0=0.025, k=0.045. Flaps: CD0=0.040, k=0.047. Con qS=29000 N y empuje 4400 N, calcule márgenes de empuje. ¿Permite concluir qué configuración tiene mayor ángulo máximo global?',
 r'Comparación a la misma condición local y mismo empuje; no son datos SAULE.',
 'Polar parabólica, mismas referencias y L=qS CL; empuje paralelo a trayectoria.',
 [r'D=q_\infty S(C_{D0}+kC_L^2)',r'M_T=T-D'],
 ['Se calculan ambas resistencias en el mismo CL y presión dinámica.','Se comparan márgenes de empuje del punto.','Para el máximo global hay que optimizar velocidad, comprobar CLmax, rendimiento y mapa de empuje de cada configuración.'],
 [test('Margen limpia','4400-29000*(.025+.045*.85**2)','N'),test('Margen flaps','4400-29000*(.040+.047*.85**2)','N')],
 'La configuración limpia tiene menor resistencia en este punto, pero un solo punto no prueba el máximo global de ascenso de cada configuración.','Comparar diferencia de resistencias con qS por diferencia de CD y comprobar mismo signo del margen.','Datos docentes; no hay ensayo físico SAULE ni velocidades óptimas identificadas.',3)

def build():
    (RDIR/'evidence/exam-bank.json').write_text(json.dumps(EX,ensure_ascii=False,indent=2))
    text=[r'\part{Enunciados originales}']
    for e in EX:
        text += [r'\chapter{'+e['title']+'}',f"Tiempo orientativo: {e['time']} minutos. Puntuación total orientativa: 10 puntos. No es un examen oficial."]
        for i,q in enumerate(e['questions'],1):
            text += [r'\section{Problema '+str(i)+f" · {q['score']} puntos"+'}',prose(q['prompt']),r'\apartado{Datos y condiciones}{'+prose(q['data'])+' '+prose(q['hyp'])+'}']
    text += [r'\part{Soluciones desarrolladas}']
    for e in EX:
        text += [r'\chapter{Soluciones: '+e['title']+'}']
        for i,q in enumerate(e['questions'],1):
            text += [r'\section{Problema '+str(i)+': '+q['title']+'}',solution(q,include_prompt=False)]
    (RDIR/'content/exams.tex').write_text('\n\n'.join(text))
    (RDIR/'simulacros.tex').write_text(r'''\input{latex/preamble}
\hypersetup{pdftitle={Simulacros de Mecánica de Vuelo},pdfauthor={Studium}}
\begin{document}
\portada{SIMULACROS Y SOLUCIONES}{SIMULACROS\\DE MECÁNICA DE VUELO}{Seis exámenes originales · Soluciones separadas y razonadas}
\frontmatter
\chapter*{Instrucciones y constantes}
Los seis simulacros combinan competencias de ejes, actuaciones, operaciones, estabilidad y simulación. Sus datos y enunciados son originales. No son exámenes oficiales ni pronostican una convocatoria. Los problemas de dinámica del quinto simulacro están marcados como ampliación.

Use $g_0=9.80665\SIu{m/s^2}$, $R_a=287.05287\SIu{J/(kg\,K)}$, $T_0=288.15\SIu K$, $p_0=101325\SIu{Pa}$ y $\rho_0=1.225\SIu{kg/m^3}$. Hasta 11 km geopotenciales, $T=T_0-0.0065h$, $p=p_0(T/T_0)^{g_0/(0.0065R_a)}$ y $\rho=p/(R_aT)$. Los ángulos numéricos se convierten a radianes antes de evaluarse.

Se permite calculadora o un entorno numérico para las integrales y matrices; esta condición es propia del cuaderno y no una norma de evaluación ULE. Las soluciones están agrupadas después de todos los enunciados. Antes de consultarlas, explicite ley de vuelo, masa de enlace y restricciones. La revisión experta independiente continúa pendiente.
\consejo{Criterio orientativo de corrección}{Se valora el planteamiento físico y sistema de referencia, el desarrollo coherente con las hipótesis, la sustitución y las unidades, y la interpretación de restricciones. Un resultado sin modelo no equivale a una solución completa. Los repartos de puntos son docentes y no reproducen rúbricas oficiales.}
\input{assets/cover-credit.tex}
\tableofcontents
\mainmatter
\input{content/exams}
\end{document}
''')
    print('Simulacros:',len(EX),'Problemas:',sum(len(e['questions']) for e in EX))
if __name__=='__main__':build()
