"""Original, hypothetical educational data. No exam or experiment is reproduced."""
from copy import deepcopy
import math
import sympy as sp

CHAPTERS = [
 'Mecánica clásica y balances de energía', 'Referencias giratorias, Lagrange y sistemas dinámicos',
 'Continuo y propiedades del fluido', 'Cinemática y descripción del movimiento',
 'Estática, fuerzas y flotación', 'Flujos internos laminares',
 'Resistencia, sustentación y polar', 'Oscilaciones y difusión no estacionaria',
 'Balances integrales y máquinas de flujo', 'Semejanza y análisis dimensional',
 'Operadores y teoremas integrales', 'Continuidad, Bernoulli y flujo potencial',
 'Esfuerzos, disipación y transporte', 'Soluciones de Navier--Stokes',
 'Escalas y aproximaciones', 'Estratificación, flotabilidad y rotación',
]
BANK=[]
def P(ch,title,level,question,data,hypotheses,model,steps,calc,interpretation,check,limits):
    BANK.append(dict(id=f'MF-P{len(BANK)+1:02d}',ch=ch,title=title,level=level,question=question,
      data=data,hypotheses=hypotheses,model=model,steps=steps,calc=calc,
      interpretation=interpretation,check=check,limits=limits))
# Data: symbol, SI value, unit, meaning, LaTeX symbol. Calculation: symbol, expression, unit, LaTeX symbol.
def d(k,v,u,label,tex=None):return [k,v,u,label,tex or k]
def c(k,e,u,tex=None):return [k,e,u,tex or k]

P(1,'Tracción de un vehículo en rampa','Intermedio',
 r'Un vehículo asciende a velocidad constante. Determine la tracción, la potencia útil y la potencia de entrada; compare después la demanda al aumentar la velocidad un 20\,\%, manteniendo la misma ley de resistencia.',
 [d('m',850,'kg','masa'),d('slope',.04,'','seno del ángulo de rampa',r'\sin\theta'),d('k',.32,'kg/m','coeficiente de resistencia cuadrática'),d('V',12,'m/s','velocidad'),d('eta',.82,'','rendimiento global',r'\eta')],
 'Movimiento rectilíneo estacionario; rozamiento de rodadura omitido. El rendimiento se mantiene constante en la comparación.',
 r'T=mg\sin\theta+kV^2,\qquad P_u=TV,\qquad P_e=P_u/\eta.',
 [r'Proyectar el equilibrio sobre la rampa: la tracción compensa gravedad y resistencia.',r'Multiplicar la fuerza por la velocidad para obtener potencia mecánica. El rendimiento relaciona potencia útil y de entrada.',r'Repetir el equilibrio con $V_2=1.2V$; no multiplicar toda la potencia por $1.2^3$, porque la contribución gravitatoria es lineal en velocidad.'],
 [c('T','m*g*slope+k*V**2','N'),c('Pu','T*V','W',r'P_u'),c('Pe','Pu/eta','W',r'P_e'),c('Pe2','(m*g*slope+k*(1.2*V)**2)*1.2*V/eta','W',r'P_{e,2}'),c('ratio','Pe2/Pe','',r'P_{e,2}/P_e')],
 'La masa pesa en el balance de fuerzas; la potencia depende también de la velocidad. La resistencia cuadrática no hace cúbica la parte gravitatoria.',
 r'Comprobar $\eta P_e=TV$ y que cada sumando de $T$ tiene unidades de newton. Si $k\to0$, la razón de potencias tiende a 1.2.',
 'No se han dimensionado motor, transmisión ni arranque. Los datos definen un caso académico, no un vehículo real.')

P(1,'Frenado por resistencia cuadrática','Básico',
 r'Una masa se mueve horizontalmente sin tracción y su resistencia es $k v^2$. Deduzca velocidad y recorrido, y calcúlelos al tiempo indicado. Explique si el modelo predice una detención exacta en tiempo finito.',
 [d('m',24,'kg','masa'),d('k',.8,'kg/m','resistencia cuadrática'),d('v0',8,'m/s','velocidad inicial',r'v_0'),d('t',6,'s','tiempo')],
 'Velocidad positiva, masa constante, fuerza opuesta al movimiento; no hay otras fuerzas horizontales.',
 r'm\dot v=-kv^2,\quad v(t)=\frac{v_0}{1+kv_0t/m},\quad x(t)=\frac{m}{k}\ln(1+kv_0t/m).',
 [r'Separar $dv/v^2=-(k/m)dt$ e integrar con $v(0)=v_0$.',r'Integrar la velocidad entre cero y el tiempo de observación para hallar el desplazamiento.',r'El denominador permanece positivo para $t\ge0$: la velocidad se aproxima a cero sin alcanzarlo en tiempo finito.'],
 [c('v','v0/(1+k*v0*t/m)','m/s'),c('x','m/k*log(1+k*v0*t/m)','m'),c('loss','m*(v0**2-v**2)/2','J',r'\Delta E')],
 'Una ley ideal de resistencia deja una cola de movimiento. La detención de un cuerpo real puede estar gobernada después por fuerzas no incluidas.',
 r'Derivar $x(t)$ para recuperar $v(t)$ y comprobar $m\dot v+kv^2=0$. La pérdida cinética debe ser positiva.',
 'No prolongar la ley cuadrática a velocidades en las que cambie el régimen de resistencia.')

P(1,'Caída con resistencia lineal','Intermedio',
 r'Una partícula se libera desde el reposo. Tomando positivo hacia abajo, obtenga velocidad límite, tiempo de relajación, velocidad y distancia recorrida. Distinga la energía potencial perdida de la energía cinética adquirida.',
 [d('m',.04,'kg','masa'),d('b',.12,'kg/s','coeficiente lineal'),d('t',.7,'s','tiempo')],
 'Fuerza resistiva $-bv$, gravedad uniforme y flotación despreciada; el coeficiente se toma constante.',
 r'\tau=m/b,\quad v_T=mg/b,\quad v=v_T(1-e^{-t/\tau}),\quad z=v_T[t-\tau(1-e^{-t/\tau})].',
 [r'Resolver $m\dot v=mg-bv$ con factor integrante y condición inicial nula.',r'Integrar la velocidad para obtener el descenso.',r'Aplicar energía mecánica: $mgz-mv^2/2$ es la energía disipada por la resistencia.'],
 [c('tau','m/b','s',r'\tau'),c('vt','m*g/b','m/s',r'v_T'),c('v','vt*(1-exp(-t/tau))','m/s'),c('z','vt*(t-tau*(1-exp(-t/tau)))','m'),c('Ed','m*g*z-m*v**2/2','J',r'E_d')],
 'La fuerza resultante tiende a cero, mientras la potencia gravitatoria termina disipándose por completo.',
 r'La solución satisface $v(0)=z(0)=0$ y $\dot v(0)=g$. Para $t\gg\tau$, $v\to v_T$; comprobar $E_d\ge0$.',
 'La ley lineal es una hipótesis del enunciado; no se atribuye a cualquier esfera o número de Reynolds.')

P(2,'Coriolis durante una deriva radial','Intermedio',
 r'Una partícula se desplaza radialmente sobre una plataforma giratoria. Halle la aceleración de Coriolis y estime la desviación transversal para un intervalo corto. Compare el orden de magnitud de Coriolis y la aceleración centrífuga.',
 [d('Om',.8,'1/s','velocidad angular positiva sobre $z$',r'\Omega'),d('vr',.15,'m/s','velocidad radial hacia fuera',r'v_r'),d('r0',.4,'m','radio inicial',r'r_0'),d('t',.08,'s','intervalo corto')],
 'Plataforma con rotación uniforme, aproximación local con bases prácticamente fijas durante el intervalo; no se prescribe aquí la dinámica completa de una partícula libre.',
 r'\boldsymbol a_C=-2\boldsymbol\Omega\times\boldsymbol v_{rel},\quad a_{C,\theta}=-2\Omega v_r,\quad a_{cf}=\Omega^2r_0,\quad s_\theta\simeq\tfrac12a_{C,\theta}t^2.',
 [r'Con $\boldsymbol\Omega=\Omega\boldsymbol e_z$ y velocidad radial exterior, el producto vectorial apunta hacia $+\boldsymbol e_\theta$; el término ficticio lleva signo negativo.',r'Integrar una aceleración transversal local constante con velocidad transversal inicial nula.',r'Comprobar $\Omega t\ll1$ y $v_rt/r_0\ll1$ antes de interpretar la aproximación.'],
 [c('ac','-2*Om*vr','m/s**2',r'a_{C,\theta}'),c('acf','Om**2*r0','m/s**2',r'a_{cf}'),c('sy','ac*t**2/2','m',r's_\theta'),c('eps1','Om*t','',r'\Omega t'),c('eps2','vr*t/r0','',r'v_rt/r_0')],
 'La desviación local es hacia el sentido opuesto a la rotación. Comparar módulos no permite sumar las dos aceleraciones como escalares: tienen direcciones distintas.',
 'Cambiar el signo de la rotación o de la velocidad radial invierte Coriolis; cambiar ambos conserva su signo.',
 'La desviación es una estimación local. Una trayectoria larga exige resolver las ecuaciones completas en la base giratoria.')

P(2,'Oscilador amortiguado desde Lagrange','Intermedio',
 r'Una masa unida a un muelle y un amortiguador parte de una elongación sin velocidad. Obtenga su ecuación, determine el régimen y calcule frecuencia amortiguada y amplitud de la envolvente al tiempo dado.',
 [d('m',2,'kg','masa'),d('k',80,'N/m','rigidez'),d('b',4,'kg/s','amortiguamiento'),d('x0',.03,'m','elongación inicial',r'x_0'),d('t',1.2,'s','tiempo')],
 r'Un grado de libertad, muelle lineal y fuerza disipativa $-b\dot x$; no hay excitación exterior.',
 r'L=\tfrac12m\dot x^2-\tfrac12kx^2,\quad m\ddot x+b\dot x+kx=0,\quad \zeta=\frac{b}{2\sqrt{km}},\quad \omega_d=\sqrt{k/m-b^2/(4m^2)}.',
 [r'Aplicar Euler--Lagrange con fuerza generalizada $-b\dot x$.',r'Comparar $\zeta$ con uno y resolver las raíces de la ecuación característica.',r'La solución con velocidad inicial nula es $x=x_0e^{-bt/(2m)}[\cos(\omega_dt)+b\sin(\omega_dt)/(2m\omega_d)]$. La envolvente exacta de esta expresión incluye el factor de fase.'],
 [c('wn','sqrt(k/m)','1/s',r'\omega_n'),c('zeta','b/(2*sqrt(k*m))','',r'\zeta'),c('wd','sqrt(k/m-b**2/(4*m**2))','1/s',r'\omega_d'),c('env','x0*sqrt(1+(b/(2*m*wd))**2)*exp(-b*t/(2*m))','m',r'A_{env}'),c('x','x0*exp(-b*t/(2*m))*(cos(wd*t)+b*sin(wd*t)/(2*m*wd))','m')],
 'La envolvente decrece exponencialmente, pero no es idéntica a la posición instantánea ni, con estas condiciones iniciales, a $x_0e^{-bt/(2m)}$.',
 r'$\dot E=-b\dot x^2\le0$; al hacer $b\to0$ se recupera la oscilación conservativa.',
 'La linealidad del muelle y del amortiguador limita la extrapolación a amplitudes grandes.')

P(2,'Equilibrios y estabilidad local de Lorenz','Avanzado',
 r'Para el sistema de Lorenz, calcule los tres equilibrios y aplique el criterio de Routh al equilibrio no nulo. Decida estabilidad local sin confundirla con una demostración de caos.',
 [d('sig',10,'','parámetro sigma',r'\sigma'),d('bb',8/3,'','parámetro beta',r'\beta'),d('rr',16,'','parámetro r',r'r')],
 r'Sistema adimensional $\dot x=\sigma(y-x)$, $\dot y=rx-y-xz$, $\dot z=xy-\beta z$. Los parámetros describen únicamente este modelo reducido.',
 r'(0,0,0),\quad (\pm\sqrt{\beta(r-1)},\pm\sqrt{\beta(r-1)},r-1).\quad \lambda^3+a_1\lambda^2+a_2\lambda+a_3=0,\quad a_1=\sigma+\beta+1,\ a_2=\beta(\sigma+r),\ a_3=2\sigma\beta(r-1).',
 [r'Imponer las tres derivadas nulas: en los equilibrios no triviales $y=x$, $z=r-1$ y $x^2=\beta(r-1)$.',r'Evaluar el polinomio característico del jacobiano en cualquiera de esos dos equilibrios.',r'Con coeficientes positivos, la condición adicional de Routh es $a_1a_2>a_3$. El origen tiene una dirección inestable para $r>1$.'],
 [c('xe','sqrt(bb*(rr-1))','',r'|x_e|'),c('ze','rr-1','',r'z_e'),c('a1','sig+bb+1','',r'a_1'),c('a2','bb*(sig+rr)','',r'a_2'),c('a3','2*sig*bb*(rr-1)','',r'a_3'),c('margin','a1*a2-a3','',r'a_1a_2-a_3')],
 'El margen positivo implica estabilidad lineal local de los dos equilibrios no triviales para estos parámetros. No afirma estabilidad global ni existencia de un atractor caótico.',
 'Sustituir los equilibrios en las tres ecuaciones y comprobar el polinomio mediante el determinante del jacobiano.',
 'Una discretización numérica o una gráfica irregular no demuestra caos; no se atribuye este conjunto de parámetros a un experimento.')

P(3,'Viscosidad a partir de un ensayo de placas','Básico',
 r'Una placa arrastra una capa de líquido. A partir de la fuerza tangencial, obtenga viscosidad dinámica y cinemática, esfuerzo y potencia disipada. Calcule un Reynolds basado en el espesor.',
 [d('F',3.6,'N','fuerza tangencial'),d('A',.12,'m**2','área mojada'),d('h',.002,'m','separación'),d('U',.4,'m/s','velocidad de la placa'),d('rho',950,'kg/m**3','densidad',r'\rho')],
 'Fluido newtoniano, perfil lineal, no deslizamiento, placa opuesta fija y gradiente de presión nulo. Fuerza neta de una sola cara mojada.',
 r'\tau=F/A=\mu U/h,\quad \mu=Fh/(AU),\quad \nu=\mu/\rho,\quad P=FU.',
 [r'Convertir fuerza en esfuerzo usando el área mojada correcta.',r'Aplicar la ley constitutiva al gradiente uniforme $U/h$.',r'La potencia de la placa se disipa por viscosidad: por unidad de volumen es $\mu(U/h)^2$.'],
 [c('tau','F/A','Pa',r'\tau'),c('mu','F*h/(A*U)','Pa*s',r'\mu'),c('nu','mu/rho','m**2/s',r'\nu'),c('power','F*U','W',r'P'),c('Re','rho*U*h/mu','',r'\mathrm{Re}_h')],
 'Viscosidad dinámica y cinemática tienen dimensiones distintas. Un Reynolds pequeño es coherente con este caso, pero no sustituye la comprobación de las condiciones de contorno.',
 r'Integrar $\mu(U/h)^2$ sobre el volumen $Ah$ y recuperar $FU$.',
 'Se omiten efectos de borde, calentamiento y dependencia de la viscosidad con temperatura o cizalla.')

P(3,'Compresibilidad y error de densidad constante','Intermedio',
 r'Un líquido tiene módulo volumétrico constante. Calcule su cambio exacto de densidad para un incremento de presión y compárelo con la aproximación lineal. ¿Es compatible con una tolerancia de variación de densidad del 0.5\,\%?',
 [d('rho0',980,'kg/m**3','densidad de referencia',r'\rho_0'),d('K',1.8e9,'Pa','módulo volumétrico'),d('dp',5e6,'Pa','incremento de presión',r'\Delta p')],
 r'Relación barotrópica a temperatura controlada; módulo $K=\rho\,dp/d\rho$ constante en el intervalo.',
 r'\frac{d\rho}{\rho}=\frac{dp}{K},\quad \rho=\rho_0e^{\Delta p/K},\quad \rho_{lin}=\rho_0(1+\Delta p/K).',
 [r'Integrar la definición del módulo; el modelo exponencial procede de mantener constante $K$, no de suponer constante $d\rho/dp$.',r'Expandir la exponencial para obtener la fórmula lineal y comparar ambas.',r'Comprobar la variación relativa frente a la tolerancia, separando esa variación del error de linealización.'],
 [c('eps','dp/K','',r'\Delta p/K'),c('rho','rho0*exp(dp/K)','kg/m**3',r'\rho'),c('rhol','rho0*(1+dp/K)','kg/m**3',r'\rho_{lin}'),c('variation','rho/rho0-1','',r'\Delta\rho/\rho_0'),c('error','(rho-rhol)/rho','',r'\varepsilon_{lin}')],
 'El fluido es compresible aunque una aproximación de densidad constante pueda ser aceptable con la tolerancia impuesta.',
 r'Al derivar la solución se obtiene $d\rho/dp=\rho/K$; para $\Delta p\to0$ desaparecen variación y error.',
 'No se supone que el módulo sea constante a cualquier presión ni en un proceso térmico arbitrario.')

P(3,'Escalas del continuo y número de Knudsen','Básico',
 r'Un gas circula por una microholgura. Evalúe Knudsen y Reynolds y estime el esfuerzo de Couette. Repita Knudsen al reducir cien veces la holgura y explique qué hipótesis pasa a ser cuestionable.',
 [d('lam',65e-9,'m','camino libre medio dado',r'\lambda'),d('h',50e-6,'m','holgura'),d('U',.02,'m/s','velocidad de la pared'),d('rho',1.2,'kg/m**3','densidad',r'\rho'),d('mu',1.8e-5,'Pa*s','viscosidad',r'\mu')],
 'En la holgura inicial se ensaya el modelo continuo newtoniano con no deslizamiento y sin gradiente de presión. Las propiedades son datos académicos del caso.',
 r'\mathrm{Kn}=\lambda/h,\quad \mathrm{Re}_h=\rho Uh/\mu,\quad \tau=\mu U/h.',
 [r'Distinguir la escala molecular $\lambda$ de la escala geométrica $h$.',r'Calcular ambos cocientes adimensionales: Reynolds compara inercia y viscosidad; Knudsen compara escalas molecular y macroscópica.',r'La nueva holgura eleva Knudsen cien veces. Una fórmula de Couette con no deslizamiento ya no constituye por sí sola una predicción justificada.'],
 [c('Kn','lam/h','',r'\mathrm{Kn}'),c('Re','rho*U*h/mu','',r'\mathrm{Re}_h'),c('tau','mu*U/h','Pa',r'\tau'),c('Kn2','100*lam/h','',r'\mathrm{Kn}_2')],
 'Un Reynolds diminuto no garantiza el continuo ni la condición de no deslizamiento. Son verificaciones diferentes.',
 'Comprobar que los dos cocientes carecen de unidades y que el esfuerzo cambia linealmente con la viscosidad.',
 'No se calcula un modelo cinético ni una corrección de deslizamiento. Los umbrales entre regímenes no se tratan como fronteras exactas universales.')

P(4,'Punto de remanso plano','Intermedio',
 r'Para $\boldsymbol u=(ax,-ay,0)$, determine divergencia, vorticidad, aceleración material y tasa de deformación. Evalúe la aceleración en el punto dado y explique por qué estacionario no significa aceleración nula.',
 [d('a',.6,'1/s','tasa de extensión'),d('x',.3,'m','coordenada x'),d('y',.2,'m','coordenada y')],
 'Campo cartesiano estacionario, diferenciable en el dominio considerado. No se prescribe aquí una pared ni una geometría de entrada.',
 r'\nabla\cdot\boldsymbol u=0,\quad\nabla\times\boldsymbol u=0,\quad \frac{D\boldsymbol u}{Dt}=(a^2x,a^2y,0),\quad \boldsymbol D=\operatorname{diag}(a,-a,0).',
 [r'Calcular las derivadas espaciales de cada componente, conservando los signos del campo.',r'Formar $(\boldsymbol u\cdot\nabla)\boldsymbol u$: el signo negativo de $v$ se multiplica por el de $\partial v/\partial y$.',r'La parte simétrica del gradiente mide extensión y compresión; la antisimétrica se anula.'],
 [c('u','a*x','m/s'),c('v','-a*y','m/s'),c('ax','a**2*x','m/s**2',r'a_x'),c('ay','a**2*y','m/s**2',r'a_y')],
 'La partícula acelera por moverse hacia regiones con otra velocidad, aunque el observador euleriano no vea cambios temporales.',
 r'Integrar las trayectorias $x=x_0e^{at}$, $y=y_0e^{-at}$ y comprobar su segunda derivada. El producto $xy$ permanece constante.',
 'El campo ideal no describe por sí solo el flujo completo alrededor de un cuerpo con no deslizamiento.')

P(4,'Cizalla simple y función de corriente','Básico',
 r'Para $u=\Gamma y$, $v=0$, construya una función de corriente, calcule vorticidad y aceleración y siga una partícula. Distinga el giro local del elemento fluido de la velocidad angular de su trayectoria.',
 [d('Gm',3,'1/s','tasa de cizalla',r'\Gamma'),d('x0',.1,'m','posición inicial x',r'x_0'),d('y0',.02,'m','posición inicial y',r'y_0'),d('t',2,'s','tiempo')],
 r'Campo bidimensional estacionario, incompresible; convenio $u=\partial_y\psi$, $v=-\partial_x\psi$.',
 r'\psi=\tfrac12\Gamma y^2+C,\quad \omega_z=-\Gamma,\quad D\boldsymbol u/Dt=0,\quad x=x_0+\Gamma y_0t,\ y=y_0.',
 [r'Integrar $\partial_y\psi=\Gamma y$; la condición $v=0$ hace constante la función de integración respecto de $x$.',r'Calcular $\partial_xv-\partial_yu$ para obtener el signo de la vorticidad.',r'El punto material se traslada en línea recta. El giro local de un elemento infinitesimal es $\omega_z/2$, que no es el giro orbital de esa partícula.'],
 [c('vel','Gm*y0','m/s',r'u(y_0)'),c('xf','x0+Gm*y0*t','m',r'x(t)'),c('psi','Gm*y0**2/2','m**2/s',r'\psi(y_0)-C'),c('wz','-Gm','1/s',r'\omega_z'),c('spin','-Gm/2','1/s',r'\Omega_{local}')],
 'Un flujo puede tener vorticidad sin que las trayectorias sean curvas y sin aceleración material.',
 r'$\nabla\cdot\boldsymbol u=0$ y $u\partial_xu+v\partial_yu=0$; el signo cambia si cambia el de $\Gamma$.',
 'La constante de la función de corriente es arbitraria. No se identifica el movimiento de una partícula con la rotación de un elemento.')

P(4,'Extensión no estacionaria','Avanzado',
 r'Sea $u=a(t)x$, $v=-a(t)y$, con $a(t)=a_0+bt$. Determine aceleración local y convectiva y evalúe la aceleración total en el punto y tiempo dados. Obtenga también la trayectoria desde la posición indicada.',
 [d('a0',.2,'1/s','tasa inicial',r'a_0'),d('b',.03,'1/s**2','variación temporal'),d('t',2,'s','instante'),d('x',.4,'m','coordenada euleriana x'),d('y',.3,'m','coordenada euleriana y'),d('x0',.1,'m','coordenada material inicial x',r'x_0'),d('y0',.2,'m','coordenada material inicial y',r'y_0')],
 'Campo suave incompresible; el punto euleriano de evaluación y la posición inicial de la trayectoria son datos distintos.',
 r'\boldsymbol a_{loc}=(bx,-by),\quad\boldsymbol a_{conv}=(a^2x,a^2y),\quad \boldsymbol a=((b+a^2)x,(a^2-b)y).\quad x_p=x_0e^{a_0t+bt^2/2},\ y_p=y_0e^{-a_0t-bt^2/2}.',
 [r'Derivar respecto del tiempo manteniendo fija la posición para obtener la parte local.',r'Formar las derivadas espaciales y sumar los dos mecanismos de aceleración.',r'Separar $dx_p/x_p=a(t)dt$ y $dy_p/y_p=-a(t)dt$; integrar desde cero.'],
 [c('at','a0+b*t','1/s',r'a(t)'),c('ax','(b+at**2)*x','m/s**2',r'a_x'),c('ay','(at**2-b)*y','m/s**2',r'a_y'),c('xp','x0*exp(a0*t+b*t**2/2)','m',r'x_p(t)'),c('yp','y0*exp(-a0*t-b*t**2/2)','m',r'y_p(t)')],
 'La componente vertical local puede oponerse a la convectiva. Es necesario sumar sus signos, no sus módulos.',
 r'El producto $x_py_p=x_0y_0$ se conserva. Al hacer $b=0$ se recupera el caso estacionario.',
 'La trayectoria calculada no tiene por qué pasar por el punto euleriano elegido al mismo instante.')

P(5,'Compuerta inclinada articulada','Intermedio',
 r'Una compuerta rectangular está articulada en su borde superior, situado bajo una superficie libre. Determine fuerza hidrostática, punto de aplicación y fuerza normal que debe ejercerse en el extremo inferior para equilibrarla.',
 [d('b',1.2,'m','anchura'),d('L',2,'m','longitud sobre el panel'),d('h0',.4,'m','profundidad de la articulación',r'h_0'),d('theta',math.pi/3,'','ángulo con la horizontal',r'\theta'),d('rho',1000,'kg/m**3','densidad',r'\rho')],
 'Líquido en reposo, presión atmosférica en la cara seca y superficie libre. Se omiten peso del panel y rozamiento de la articulación.',
 r'p(s)=\rho g(h_0+s\sin\theta),\quad F=b\int_0^L p(s)ds,\quad M=b\int_0^L sp(s)ds,\quad s_R=M/F.',
 [r'Usar presión manométrica: la atmosférica se cancela entre ambas caras.',r'Integrar por separado fuerza y momento respecto de la bisagra; $s$ mide distancia sobre el panel, no profundidad vertical.',r'Equilibrar momentos: $F_{ap}L=M$. La reacción de la bisagra completa el equilibrio de fuerzas.'],
 [c('hc','h0+L*sin(theta)/2','m',r'h_c'),c('F','rho*g*b*L*hc','N'),c('M','rho*g*b*(h0*L**2/2+sin(theta)*L**3/3)','N*m'),c('sr','M/F','m',r's_R'),c('hold','M/L','N',r'F_{ap}')],
 'El centro de presiones queda por debajo del centro geométrico porque la presión crece con la profundidad.',
 r'Comprobar $L/2<s_R<L$ y recuperar $s_R=2L/3$ cuando $h_0=0$. Una cuadratura de $p(s)$ reproduce fuerza y momento.',
 'La carga de equilibrio es normal al panel y se aplica en su extremo; otra dirección cambia el brazo de palanca.')

P(5,'Manómetro diferencial de dos líquidos','Básico',
 r'Dos tomas a la misma cota contienen agua y se conectan por un manómetro con un líquido más denso. La interfaz del lado A está más baja que la del lado B. Calcule $p_A-p_B$ y su altura equivalente de agua.',
 [d('rw',1000,'kg/m**3','densidad del líquido de las tomas',r'\rho_w'),d('rm',13200,'kg/m**3','densidad del líquido manométrico dada',r'\rho_m'),d('dh',.18,'m','desnivel de interfaces',r'\Delta h')],
 'Columnas estáticas, líquidos inmiscibles de densidad constante, sin capilaridad. La densidad alta es un dato académico, sin atribuirla a una sustancia concreta.',
 r'p_A-p_B=(\rho_m-\rho_w)g\Delta h,\qquad H_w=\frac{p_A-p_B}{\rho_wg}.',
 [r'Recorrer el circuito desde A hasta B sumando $\rho g\Delta z$ al bajar y restándolo al subir.',r'Agrupar los tramos de agua; las tomas a la misma cota hacen que sólo importe el desnivel de interfaces.',r'La interfaz más baja del lado A exige mayor presión en A; contrastar el signo con el dibujo mental del tubo.'],
 [c('dp','(rm-rw)*g*dh','Pa',r'p_A-p_B'),c('Hw','dp/(rw*g)','m',r'H_w')],
 'Usar sólo la densidad manométrica sobreestima la diferencia: también hay que descontar el peso de la columna desplazada de agua.',
 r'Para $\rho_m=\rho_w$, el desnivel deja de medir una diferencia entre tomas a igual cota. Invertir interfaces invierte el signo.',
 'Con tomas a diferente altura se añade el término hidrostático del líquido de conexión.')

P(5,'Estabilidad de un prisma flotante','Avanzado',
 r'Un prisma homogéneo flota con su cara ancha horizontal. Obtenga calado y altura metacéntrica para balanceo alrededor de su eje longitudinal. Estime el momento restaurador para un ángulo pequeño y decida estabilidad inicial.',
 [d('b',.4,'m','manga'),d('h',.2,'m','altura'),d('L',.8,'m','longitud'),d('rs',600,'kg/m**3','densidad del sólido',r'\rho_s'),d('rf',1000,'kg/m**3','densidad del líquido',r'\rho_f'),d('theta',.05,'','ángulo en radianes',r'\theta')],
 'Prisma rígido homogéneo, líquido en reposo y escora infinitesimal; el eje de balanceo es paralelo a la longitud.',
 r'd=\rho_sh/\rho_f,\quad BM=I_{wp}/\mathcal V=b^2/(12d),\quad BG=(h-d)/2,\quad GM=BM-BG,\quad M_R\simeq-WGM\theta.',
 [r'Igualar peso y empuje para obtener volumen desplazado y calado.',r'Usar $I_{wp}=Lb^3/12$ para el eje longitudinal; no intercambiar manga y longitud.',r'Calcular $GM$ y conservar el signo del momento: un $GM$ positivo produce un par opuesto a la escora.'],
 [c('draft','rs/rf*h','m',r'd'),c('BM','b**2/(12*draft)','m'),c('BG','(h-draft)/2','m'),c('GM','BM-BG','m'),c('W','rs*L*b*h*g','N'),c('moment','-W*GM*theta','N*m',r'M_R')],
 'La condición de flotación no garantiza estabilidad. En este caso la altura metacéntrica positiva da estabilidad inicial de balanceo.',
 r'El empuje calculado con el calado debe igualar $W$. Para $GM=0$ desaparece el término restaurador lineal, sin decidir la estabilidad de orden superior.',
 'No predice estabilidad a grandes ángulos, inundación, balanceo con oleaje ni estabilidad alrededor de otro eje.')

P(6,'Superposición Couette--Poiseuille','Intermedio',
 r'Un líquido circula entre placas separadas $h$. La inferior está fija y la superior se mueve con $U$. Un gradiente favorable $G=-dp/dx>0$ impulsa además el flujo. Halle perfil, caudal y esfuerzos cortantes en ambos extremos.',
 [d('h',.004,'m','separación'),d('U',.3,'m/s','velocidad superior'),d('mu',.08,'Pa*s','viscosidad',r'\mu'),d('G',100,'Pa/m','gradiente favorable'),d('b',.2,'m','anchura')],
 'Flujo estacionario, laminar, newtoniano y plenamente desarrollado; ancho mucho mayor que la separación.',
 r'\mu u^{\prime\prime}=-G,\quad u=Uy/h+Gy(h-y)/(2\mu),\quad q=Uh/2+Gh^3/(12\mu),\quad \tau_{xy}=\mu U/h+G(h/2-y).',
 [r'Integrar dos veces e imponer $u(0)=0$ y $u(h)=U$.',r'Integrar el perfil para obtener caudal por anchura y multiplicar por $b$.',r'Derivar el perfil para obtener el componente de esfuerzo. La tracción sobre cada pared exige además su normal exterior.'],
 [c('q','U*h/2+G*h**3/(12*mu)','m**2/s'),c('Q','b*q','m**3/s'),c('tau0','mu*U/h+G*h/2','Pa',r'\tau_{xy}(0)'),c('tauh','mu*U/h-G*h/2','Pa',r'\tau_{xy}(h)')],
 'La velocidad lineal y la parábola pueden sumarse porque esta ecuación reducida es lineal. El signo del componente de esfuerzo no es por sí solo el de la fuerza sobre ambas paredes.',
 r'Para $G=0$ se recupera Couette; para $U=0$, Poiseuille plano y esfuerzos opuestos en los extremos.',
 'Se omiten entrada, efectos laterales e inestabilidades; no se suman arbitrariamente soluciones no lineales de Navier--Stokes.')

P(6,'Viscosímetro capilar e inversión del caudal','Básico',
 r'Un capilar transporta el caudal dado. Calcule caída de presión, velocidad media, Reynolds, esfuerzo en pared y potencia disipada. Compruebe la coherencia del supuesto laminar.',
 [d('R',.001,'m','radio'),d('L',.8,'m','longitud'),d('rho',980,'kg/m**3','densidad',r'\rho'),d('mu',.012,'Pa*s','viscosidad',r'\mu'),d('Q',1e-6,'m**3/s','caudal')],
 'Tubo circular horizontal rígido; fluido incompresible newtoniano y flujo estacionario plenamente desarrollado.',
 r'\Delta p=8\mu LQ/(\pi R^4),\quad \bar u=Q/(\pi R^2),\quad \mathrm{Re}_D=2\rho\bar uR/\mu,\quad \tau_w=\Delta pR/(2L).',
 [r'Invertir la ley de caudal de Poiseuille; conservar el radio elevado a cuatro.',r'Usar diámetro $2R$ en Reynolds y señalarlo explícitamente.',r'La potencia $\Delta pQ$ se convierte en disipación en el tramo desarrollado; no incluye una bomba real ni sus pérdidas.'],
 [c('dp','8*mu*L*Q/(pi*R**4)','Pa',r'\Delta p'),c('um','Q/(pi*R**2)','m/s',r'\bar u'),c('Re','2*rho*um*R/mu','',r'\mathrm{Re}_D'),c('tau','dp*R/(2*L)','Pa',r'\tau_w'),c('power','dp*Q','W',r'P')],
 'El radio controla fuertemente la resistencia. La comprobación de Reynolds apoya el régimen supuesto, pero no sustituye la comprobación de longitud de entrada.',
 r'Integrar $u(r)=\Delta p(R^2-r^2)/(4\mu L)$ sobre el área reproduce $Q$. El balance axial da la misma tensión en pared.',
 'No se incorporan correcciones de entrada, deslizamiento, dependencia térmica ni errores de medida del radio.')

P(6,'Couette circular y par resistente','Avanzado',
 r'Un cilindro interior gira dentro de otro fijo. Halle los coeficientes del perfil azimutal, el par requerido, la potencia y la diferencia de presión radial entre cilindros.',
 [d('Ri',.02,'m','radio interior',r'R_i'),d('Ro',.05,'m','radio exterior',r'R_o'),d('Om',15,'1/s','giro interior',r'\Omega_i'),d('mu',.4,'Pa*s','viscosidad',r'\mu'),d('L',.3,'m','longitud'),d('rho',900,'kg/m**3','densidad',r'\rho')],
 'Solución base laminar estacionaria puramente azimutal, sin efectos de extremos. El cilindro exterior está fijo; no se certifica estabilidad frente a vórtices de Taylor.',
 r'u_\theta=Ar+B/r,\quad A=-\Omega_iR_i^2/(R_o^2-R_i^2),\quad B=\Omega_iR_i^2R_o^2/(R_o^2-R_i^2),\quad T=4\pi\mu LB,\quad dp/dr=\rho u_\theta^2/r.',
 [r'Imponer no deslizamiento en ambos radios para determinar $A,B$.',r'Usar $\tau_{r\theta}=\mu(du_\theta/dr-u_\theta/r)=-2\mu B/r^2$ y multiplicar por área y brazo.',r'Integrar el equilibrio radial. El par de entrada se da en módulo; el esfuerzo del líquido se opone al giro.'],
 [c('aa','-Om*Ri**2/(Ro**2-Ri**2)','1/s',r'A'),c('bb','Om*Ri**2*Ro**2/(Ro**2-Ri**2)','m**2/s',r'B'),c('torque','4*pi*mu*L*bb','N*m',r'T'),c('power','torque*Om','W',r'P'),c('dp','rho*(aa**2*(Ro**2-Ri**2)/2+2*aa*bb*log(Ro/Ri)+bb**2/2*(1/Ri**2-1/Ro**2))','Pa',r'p(R_o)-p(R_i)')],
 'La presión aumenta hacia fuera, aunque la pared exterior esté fija. Una diferencia pequeña resulta de cancelaciones entre términos de la integral.',
 r'Comprobar ambas velocidades de pared y evaluar la integral positiva $\int_{R_i}^{R_o}\rho u_\theta^2/r\,dr$ por otra ruta.',
 'El perfil es una solución base, no una garantía de que un montaje real permanezca en ese régimen.')

P(7,'Máxima eficiencia con una polar parabólica','Intermedio',
 r'Un avión en vuelo horizontal tiene $C_D=C_{D0}+KC_L^2$. Halle el $C_L$, velocidad y resistencia de máximo $L/D$. Separe la contribución inducida $K_i=1/(\pi eAR)$ de otras contribuciones cuadráticas.',
 [d('cd0',.025,'','coeficiente constante',r'C_{D0}'),d('K',.05,'','coeficiente cuadrático total'),d('e',.9,'','factor inducido dado'),d('AR',9,'','alargamiento'),d('W',4000,'N','peso'),d('rho',1.1,'kg/m**3','densidad',r'\rho'),d('S',12,'m**2','superficie')],
 'Vuelo estacionario horizontal, $L=W$, polar válida en el intervalo de sustentación empleado; datos sintéticos sin atribución a un avión.',
 r'D/W=C_{D0}/C_L+KC_L,\quad C_{L,*}=\sqrt{C_{D0}/K},\quad V_*=\sqrt{2W/(\rho SC_{L,*})},\quad D_{min}=2W\sqrt{C_{D0}K}.',
 [r'Derivar la resistencia respecto de $C_L>0$ con peso fijo y comprobar mínimo.',r'Obtener la velocidad a partir del equilibrio de sustentación.',r'Calcular $K_i$ y el resto $K-K_i$. La igualdad óptima es entre término constante y término cuadrático total, no necesariamente resistencia inducida sola.'],
 [c('CL','sqrt(cd0/K)','',r'C_{L,*}'),c('V','sqrt(2*W/(rho*S*CL))','m/s',r'V_*'),c('Dmin','2*W*sqrt(cd0*K)','N',r'D_{min}'),c('Ki','1/(pi*e*AR)','',r'K_i'),c('rest','K-Ki','',r'K-K_i'),c('LD','W/Dmin','',r'(L/D)_{max}')],
 'Atribuir todo el coeficiente cuadrático a inducción sólo es válido cuando el modelo de la polar lo establece.',
 r'La segunda derivada $2C_{D0}/C_L^3$ es positiva; verificar $KC_{L,*}^2=C_{D0}$.',
 'No se han comprobado pérdida, límites estructurales, variación de polar con Reynolds o compresibilidad.')

P(7,'Identificación de resistencia con dos mediciones sintéticas','Básico',
 r'Para la ley $F=aU+bU^2$, determine los dos coeficientes usando los pares de datos y prediga la fuerza a una tercera velocidad. Discuta qué puede y qué no puede concluirse con dos puntos exactos.',
 [d('U1',2,'m/s','primera velocidad',r'U_1'),d('F1',.3,'N','primera fuerza sintética',r'F_1'),d('U2',5,'m/s','segunda velocidad',r'U_2'),d('F2',1.2,'N','segunda fuerza sintética',r'F_2'),d('U3',8,'m/s','velocidad de predicción',r'U_3')],
 'Magnitudes positivas en un mismo sentido; modelo pasivo lineal más cuadrático. Los datos son construidos para el ejercicio y carecen de incertidumbre asignada.',
 r'F/U=a+bU,\quad b=\frac{F_2/U_2-F_1/U_1}{U_2-U_1},\quad a=F_1/U_1-bU_1.',
 [r'Dividir cada ecuación por su velocidad, que es distinta de cero.',r'Resolver la recta resultante y recuperar unidades distintas para $a$ y $b$.',r'Sustituir la velocidad de predicción. Un ajuste exacto de dos parámetros a dos puntos no mide capacidad predictiva.'],
 [c('bfit','(F2/U2-F1/U1)/(U2-U1)','kg/m',r'b'),c('afit','F1/U1-bfit*U1','kg/s',r'a'),c('F3','afit*U3+bfit*U3**2','N',r'F_3')],
 'Ambos coeficientes son positivos y la fuerza se opone al movimiento si se incorpora su signo vectorial. La extrapolación sigue siendo una hipótesis.',
 r'Reinsertar los coeficientes en los dos datos. Medidas adicionales y un análisis de residuos permitirían poner a prueba la ley.',
 'No son resultados experimentales. Sin errores de medida ni más datos no se calcula un intervalo de confianza válido.')

P(7,'Mínima potencia y restricción de sustentación','Avanzado',
 r'Con una polar parabólica, determine el estado de mínima potencia mecánica requerida en vuelo horizontal. Compárelo con máxima eficiencia y compruebe el límite de sustentación dado.',
 [d('cd0',.03,'','término constante',r'C_{D0}'),d('K',.05,'','coeficiente cuadrático'),d('W',4000,'N','peso'),d('rho',1.1,'kg/m**3','densidad',r'\rho'),d('S',12,'m**2','superficie'),d('CLlim',1.4,'','límite de sustentación',r'C_{L,lim}')],
 'Potencia aerodinámica $P=DV$, vuelo horizontal y polar fija. No se optimiza autonomía de un sistema propulsor con rendimiento variable.',
 r'P=W\sqrt{2W/(\rho S)}(C_{D0}C_L^{-3/2}+KC_L^{1/2}),\quad C_{L,P}=\sqrt{3C_{D0}/K}.',
 [r'Eliminar la velocidad mediante $L=W$ y expresar potencia en función de $C_L$.',r'Derivar: el mínimo interior satisface $KC_L^2=3C_{D0}$.',r'Comprobar $C_{L,P}\le C_{L,lim}$; si no se cumple, el óptimo factible se busca en la frontera. Comparar con $C_{L,L/D}=\sqrt{C_{D0}/K}$.'],
 [c('CLP','sqrt(3*cd0/K)','',r'C_{L,P}'),c('VP','sqrt(2*W/(rho*S*CLP))','m/s',r'V_P'),c('Pmin','W*VP*(cd0/CLP+K*CLP)','W',r'P_{min}'),c('CLD','sqrt(cd0/K)','',r'C_{L,L/D}'),c('VD','sqrt(2*W/(rho*S*CLD))','m/s',r'V_{L/D}'),c('margin','CLlim-CLP','',r'C_{L,lim}-C_{L,P}')],
 'La mínima potencia ocurre a menor velocidad y mayor sustentación que la mínima resistencia. Son objetivos de optimización distintos.',
 r'La razón ideal de velocidades es $V_P/V_{L/D}=3^{-1/4}$. El margen positivo comprueba factibilidad dentro del límite suministrado.',
 'No incluye potencia inducida de una hélice, pérdidas de transmisión ni consumo específico del motor.')

P(8,'Oscilación de un tubo en U','Básico',
 r'Un tubo en U de sección constante contiene una columna líquida de longitud total $L$. Una superficie se desplaza inicialmente $\eta_0$ respecto del equilibrio. Halle período, caudal máximo y energía mecánica.',
 [d('L',1.6,'m','longitud total de líquido'),d('A',.0006,'m**2','sección'),d('rho',1000,'kg/m**3','densidad',r'\rho'),d('eta0',.03,'m','desplazamiento de un brazo',r'\eta_0')],
 'Líquido incompresible sin pérdidas, área uniforme, brazos verticales y desplazamiento suficientemente pequeño para conservar la geometría.',
 r'\rho AL\ddot\eta=-2\rho gA\eta,\quad \omega=\sqrt{2g/L},\quad Q_{max}=A\omega\eta_0,\quad E=\rho gA\eta_0^2.',
 [r'El desnivel entre superficies es $2\eta$, no $\eta$. La masa que se acelera ocupa toda la longitud $L$.',r'Identificar la ecuación de un oscilador y aplicar condición inicial de velocidad nula.',r'Obtener el máximo caudal al pasar por el equilibrio y contrastar energías potencial y cinética.'],
 [c('omega','sqrt(2*g/L)','1/s',r'\omega'),c('period','2*pi/omega','s',r'T'),c('Qmax','A*omega*eta0','m**3/s',r'Q_{max}'),c('energy','rho*g*A*eta0**2','J',r'E')],
 'La densidad se cancela del período porque multiplica tanto inercia como restauración, pero no se cancela de la energía.',
 r'Comprobar $E=\rho AL(\omega\eta_0)^2/2$. Duplicar $L$ aumenta el período en $\sqrt2$.',
 'En un tubo real la viscosidad amortigua la oscilación y los codos pueden introducir pérdidas adicionales.')

P(8,'Pared oscilante: segundo problema de Stokes','Intermedio',
 r'Una pared plana oscila sinusoidalmente junto a un líquido profundo. Halle espesor de penetración, amplitud y retraso de fase a la distancia dada, esfuerzo máximo en pared y potencia media suministrada por unidad de área.',
 [d('nu',1e-5,'m**2/s','viscosidad cinemática',r'\nu'),d('U',.1,'m/s','amplitud de pared'),d('f',2,'1/s','frecuencia en ciclos por segundo'),d('rho',900,'kg/m**3','densidad',r'\rho'),d('y',.001,'m','distancia a pared')],
 'Fluido newtoniano semiinfinito, flujo paralelo y régimen periódico establecido, sin gradiente de presión. $y$ apunta hacia el líquido.',
 r'\delta=\sqrt{2\nu/\omega},\quad u=Ue^{-y/\delta}\cos(\omega t-y/\delta),\quad |\tau_w|=\mu U\sqrt{\omega/\nu},\quad \overline P/A=\mu U^2/(2\delta).',
 [r'Convertir ciclos por segundo a frecuencia angular $\omega=2\pi f$.',r'La solución compleja tiene un factor de amortiguación y otro de fase con la misma escala espacial.',r'Derivar en pared. La amplitud de esfuerzo contiene $\sqrt2/\delta$; al promediar la potencia se conserva sólo la parte en fase con la velocidad.'],
 [c('omega','2*pi*f','1/s',r'\omega'),c('delta','sqrt(2*nu/omega)','m',r'\delta'),c('amp','U*exp(-y/delta)','m/s',r'|u|'),c('phase','y/delta','',r'\varphi'),c('tau','rho*nu*U*sqrt(omega/nu)','Pa',r'|\tau_w|'),c('power','rho*nu*U**2/(2*delta)','W/m**2',r'\overline P/A')],
 'La perturbación penetra menos al aumentar la frecuencia. La fase indicada es un retraso en radianes, no un tiempo.',
 r'Sustituir el perfil en $\partial_tu=\nu\partial_{yy}u$ y comprobar $u(0,t)=U\cos\omega t$. La potencia media es positiva.',
 'No incluye el transitorio de arranque ni una segunda pared a distancia comparable con la penetración.')

P(8,'Difusión de un perfil sinusoidal','Avanzado',
 r'Entre placas fijas separadas $h$ se prescribe $u(y,0)=U_0\sin(\pi y/h)$. Sin gradiente de presión, obtenga la evolución, su tiempo de decaimiento, el caudal por anchura y el esfuerzo inferior al tiempo dado.',
 [d('h',.01,'m','separación'),d('nu',1e-5,'m**2/s','viscosidad cinemática',r'\nu'),d('U0',.2,'m/s','amplitud inicial',r'U_0'),d('t',.5,'s','tiempo'),d('rho',1000,'kg/m**3','densidad',r'\rho')],
 'Flujo paralelo newtoniano incompresible, sin variación longitudinal; ambas paredes fijas y viscosidad constante.',
 r'u=U_0\sin(\pi y/h)e^{-\nu\pi^2t/h^2},\quad t_d=h^2/(\nu\pi^2),\quad q=2hU_0e^{-t/t_d}/\pi.',
 [r'Separar variables usando la autofunción que ya satisface las dos condiciones de no deslizamiento.',r'La difusión multiplica el modo inicial por una exponencial; no cambia su forma espacial.',r'Integrar para hallar caudal y derivar en pared para el esfuerzo. La energía decae con el doble de exponente que la velocidad.'],
 [c('td','h**2/(nu*pi**2)','s',r't_d'),c('amp','U0*exp(-t/td)','m/s',r'U(t)'),c('q','2*h*amp/pi','m**2/s'),c('tau','rho*nu*amp*pi/h','Pa',r'\tau_{xy}(0)')],
 'Este perfil es un modo exacto de difusión: una sola escala temporal gobierna todos sus puntos.',
 r'Comprobar el residuo de la ecuación, las condiciones de pared y $u(y,0)$. Para una malla centrada, el error espacial esperado es de segundo orden.',
 'Un perfil inicial general necesita una serie de modos; no tiene necesariamente un solo tiempo de decaimiento.')

P(9,'Codo con salida a la atmósfera','Intermedio',
 r'Un codo desvía un chorro un ángulo $\theta$ desde $+x$ hacia $+y$, manteniendo la sección. Calcule la fuerza que el líquido ejerce sobre el codo, indicando componentes y signo.',
 [d('Q',.02,'m**3/s','caudal'),d('D',.04,'m','diámetro'),d('rho',1000,'kg/m**3','densidad',r'\rho'),d('p',120000,'Pa','presión manométrica de entrada'),d('theta',math.pi/3,'','ángulo de salida en radianes',r'\theta')],
 'Balance estacionario con perfiles uniformes, salida atmosférica y peso del volumen de líquido omitido. Las presiones se expresan respecto de la atmósfera.',
 r'\boldsymbol R+(pA,0)=\dot m V(\cos\theta-1,\sin\theta),\quad \boldsymbol F_{liquido\to codo}=-\boldsymbol R.',
 [r'Escoger el volumen de control interior al codo y calcular velocidad y caudal másico.',r'La presión de entrada empuja hacia $+x$; no se suma una fuerza de presión manométrica en la salida.',r'Obtener primero pared sobre líquido y después invertir el signo para contestar la pregunta.'],
 [c('A','pi*D**2/4','m**2'),c('V','Q/A','m/s'),c('md','rho*Q','kg/s',r'\dot m'),c('Fx','p*A-md*V*(cos(theta)-1)','N',r'F_x'),c('Fy','-md*V*sin(theta)','N',r'F_y'),c('Fmag','sqrt(Fx**2+Fy**2)','N',r'|\boldsymbol F|')],
 'La reacción sobre el soporte no se obtiene sólo multiplicando caudal por cambio de velocidad: la presión de entrada también interviene.',
 r'Con $\theta=0$ el cambio de momento desaparece y la fuerza axial queda $pA$. Comprobar cada componente por separado.',
 'Para perfiles no uniformes se necesitan coeficientes de cantidad de movimiento; el peso o las presiones exteriores se incorporan según la frontera elegida.')

P(9,'Disco actuador ideal','Avanzado',
 r'Un disco ideal extrae energía de una corriente uniforme con factor de inducción $a$. Obtenga velocidades en disco y estela, empuje, potencia y coeficiente de potencia. Compare con el máximo del modelo.',
 [d('a',.25,'','factor de inducción'),d('rho',1.2,'kg/m**3','densidad',r'\rho'),d('U',10,'m/s','velocidad lejana'),d('R',2,'m','radio de disco')],
 'Disco ideal sin rotación de estela, corriente estacionaria incompresible no confinada y presión ambiente lejos del disco. Se usa la rama de extracción $0<a<1/2$.',
 r'U_d=U(1-a),\quad U_w=U(1-2a),\quad T=2\rho AU^2a(1-a),\quad P=TU_d,\quad C_P=4a(1-a)^2.',
 [r'El caudal que atraviesa el disco es $\rho AU_d$, no $\rho AU$.',r'Aplicar cantidad de movimiento entre estados lejanos y multiplicar el empuje por la velocidad en el disco.',r'Derivar $C_P$ respecto de $a$: el máximo interior está en $a=1/3$, con $C_P=16/27$.'],
 [c('A','pi*R**2','m**2'),c('ud','U*(1-a)','m/s',r'U_d'),c('uw','U*(1-2*a)','m/s',r'U_w'),c('T','2*rho*A*U**2*a*(1-a)','N'),c('power','T*ud','W',r'P'),c('Cp','4*a*(1-a)**2','',r'C_P'),c('maxcp','16/27','',r'C_{P,max}')],
 'El límite pertenece al disco ideal y a su definición de potencia incidente. No es un rendimiento universal de cualquier turbomáquina.',
 r'Contrastar $P=\dot m(U^2-U_w^2)/2$ usando $\dot m=\rho AU_d$. Para $a\to0$, potencia y empuje desaparecen.',
 'Se omiten pérdidas de palas, bloqueo, rotación de estela y correcciones de inducción elevada.')

P(9,'Carro móvil que intercepta un chorro','Intermedio',
 r'Un carro se aleja en la dirección de un chorro y desvía el agua noventa grados en su sistema relativo. Halle caudal capturado, fuerza propulsora y potencia mecánica. Compruebe la energía en el sistema del laboratorio.',
 [d('V',20,'m/s','velocidad del chorro en laboratorio'),d('U',5,'m/s','velocidad constante del carro'),d('A',.001,'m**2','sección del chorro'),d('rho',1000,'kg/m**3','densidad',r'\rho')],
 'Chorro libre con $V>U$, sin pérdidas en la desviación relativa; la componente longitudinal relativa de salida es nula. No se cuenta todo el caudal emitido como capturado.',
 r'\dot m_c=\rho A(V-U),\quad F=\dot m_c(V-U),\quad P=FU,\quad |\boldsymbol v_{sal}|^2=U^2+(V-U)^2.',
 [r'El flujo de masa a través de una frontera móvil usa la velocidad relativa $V-U$.',r'En laboratorio la componente longitudinal de salida es $U$; el cambio de momento da la fuerza sobre el carro.',r'Comparar potencia con la pérdida de energía cinética del caudal realmente interceptado.'],
 [c('md','rho*A*(V-U)','kg/s',r'\dot m_c'),c('F','md*(V-U)','N'),c('power','F*U','W',r'P'),c('energy','md*(V**2-U**2-(V-U)**2)/2','W',r'\Delta\dot E_c')],
 'La velocidad relativa interviene dos veces en la fuerza: en masa capturada y en cambio de velocidad longitudinal.',
 r'Comprobar $\Delta\dot E_c=FU$. Si $U=0$, hay fuerza pero no potencia entregada al carro; si $U\to V$, desaparece la captura.',
 'Un deflector que devuelve el chorro ciento ochenta grados tiene otro cambio de momento y otra fuerza.')

P(10,'Modelo a escala con otro fluido','Intermedio',
 r'Se desea igualar Reynolds de un prototipo en aire con un modelo en otro fluido. Determine velocidad del modelo y razón de fuerzas para el mismo coeficiente adimensional. Valore si la igualdad de Reynolds basta para cualquier ensayo.',
 [d('Lp',3,'m','longitud del prototipo',r'L_p'),d('Lm',.15,'m','longitud del modelo',r'L_m'),d('Up',40,'m/s','velocidad del prototipo',r'U_p'),d('nup',1.5e-5,'m**2/s','viscosidad cinemática del prototipo',r'\nu_p'),d('num',1e-6,'m**2/s','viscosidad cinemática del modelo',r'\nu_m'),d('rp',1.2,'kg/m**3','densidad del prototipo',r'\rho_p'),d('rm',1000,'kg/m**3','densidad del modelo',r'\rho_m')],
 r'Geometrías semejantes y mismo convenio de fuerza $F=C\rho U^2L^2$. Se ensaya sólo semejanza de flujo viscoso incompresible sin superficie libre.',
 r'\frac{U_mL_m}{\nu_m}=\frac{U_pL_p}{\nu_p},\quad \frac{F_m}{F_p}=\frac{\rho_mU_m^2L_m^2}{\rho_pU_p^2L_p^2}.',
 [r'Igualar Reynolds resolviendo para la velocidad desconocida, sin invertir la razón de viscosidades.',r'Construir la escala de fuerza; el coeficiente y cualquier factor común un medio se cancelan.',r'Identificar números adicionales si aparecen compresibilidad, cavitación, oleaje o rugosidad relativa diferente.'],
 [c('Um','Up*(num/nup)*(Lp/Lm)','m/s',r'U_m'),c('Re','Up*Lp/nup','',r'\mathrm{Re}'),c('force','rm*Um**2*Lm**2/(rp*Up**2*Lp**2)','',r'F_m/F_p')],
 'Un modelo más pequeño no garantiza menor velocidad ni menor fuerza cuando se cambia de fluido.',
 r'Calcular Reynolds de ambos montajes por separado. Comprobar que la razón de fuerzas es adimensional.',
 'No se certifica seguridad ni factibilidad del ensayo; la presión y los números adicionales no están suministrados.')

P(10,'Grupos de Buckingham para una resistencia','Básico',
 r'La fuerza depende de densidad, viscosidad, velocidad y diámetro. Construya dos grupos independientes y evalúelos con los datos dados. Explique qué información experimental falta para predecir otra fuerza.',
 [d('F',.03,'N','fuerza sintética'),d('rho',1000,'kg/m**3','densidad',r'\rho'),d('mu',.01,'Pa*s','viscosidad',r'\mu'),d('U',.2,'m/s','velocidad'),d('D',.01,'m','diámetro')],
 'Se mantiene fija la forma del cuerpo y no se introducen superficies libres, compresibilidad ni otras longitudes independientes.',
 r'\Pi_1=F/(\rho U^2D^2),\quad \Pi_2=\rho UD/\mu=\mathrm{Re},\quad \Pi_1=\Phi(\Pi_2).',
 [r'Escribir dimensiones de las cinco variables en masa, longitud y tiempo; el rango de la matriz dimensional es tres.',r'Elegir $\rho,U,D$ como variables repetidas y eliminar dimensiones de fuerza y viscosidad.',r'El teorema reduce variables pero no determina la función $\Phi$. Se necesita una ley, solución o conjunto de datos adicional.'],
 [c('Re','rho*U*D/mu','',r'\mathrm{Re}'),c('CF','F/(rho*U**2*D**2)','',r'\Pi_1')],
 'El coeficiente definido usa $D^2$, sin factor un medio. No debe compararse directamente con otro coeficiente que use otra área o normalización.',
 r'La matriz dimensional tiene nulidad dos. Verificar que cada grupo tiene exponentes totales nulos en las tres dimensiones.',
 'Semejanza dimensional no demuestra independencia respecto de rugosidad, forma u otras variables omitidas.')

P(10,'Darcy, Fanning y Poiseuille','Intermedio',
 r'Calcule pérdidas en un tubo con la ley laminar, indicando los factores de Darcy y Fanning. Verifique el resultado mediante Poiseuille y explique el error de mezclar las dos convenciones.',
 [d('rho',900,'kg/m**3','densidad',r'\rho'),d('mu',.009,'Pa*s','viscosidad',r'\mu'),d('D',.01,'m','diámetro'),d('V',1,'m/s','velocidad media'),d('L',2,'m','longitud')],
 'Tubo circular horizontal, flujo laminar newtoniano plenamente desarrollado. Se omiten pérdidas locales y de entrada.',
 r'f_D=64/\mathrm{Re},\quad f_F=f_D/4,\quad \Delta p=f_D(L/D)\rho V^2/2=32\mu LV/D^2.',
 [r'Calcular Reynolds con velocidad media y diámetro.',r'Aplicar el factor de Darcy en su ecuación de caída de presión.',r'Obtener la misma caída a partir del balance laminar; introducir $f_F$ sin su factor cuatro daría una pérdida cuatro veces menor.'],
 [c('Re','rho*V*D/mu','',r'\mathrm{Re}_D'),c('fD','64/Re','',r'f_D'),c('fF','16/Re','',r'f_F'),c('dp','fD*(L/D)*rho*V**2/2','Pa',r'\Delta p'),c('dp2','32*mu*L*V/D**2','Pa',r'\Delta p_{Pois}')],
 'La notación del factor de fricción forma parte de la definición del modelo; una tabla sin convenio puede inducir errores grandes.',
 r'Comprobar $f_D=4f_F$ y la igualdad de las dos rutas de presión.',
 r'La transición no se toma como una frontera universal exacta; la ley $64/\mathrm{Re}$ no se extiende a régimen turbulento.')

P(11,'Gauss y continuidad en una expansión tridimensional','Intermedio',
 r'Para $\boldsymbol u=a(x,y,z)$, evalúe divergencia y flujo volumétrico a través de una esfera fija. Determine la densidad uniforme compatible con continuidad a partir de su valor inicial.',
 [d('a',.1,'1/s','tasa de expansión'),d('R',.3,'m','radio de esfera'),d('rho0',1000,'kg/m**3','densidad inicial',r'\rho_0'),d('t',2,'s','tiempo')],
 'Campo definido en el espacio, densidad inicialmente uniforme y sin fuentes de masa. El radio corresponde a un volumen de control fijo.',
 r'\nabla\cdot\boldsymbol u=3a,\quad \oint\boldsymbol u\cdot\boldsymbol n\,dS=4\pi aR^3,\quad \dot\rho+3a\rho=0,\quad\rho=\rho_0e^{-3at}.',
 [r'Sumar las tres derivadas diagonales para obtener divergencia.',r'En la esfera $u_n=aR$ es constante; multiplicar por su área y comparar con la integral de volumen.',r'La densidad espacialmente uniforme permite reducir continuidad a una ecuación temporal. Flujo volumétrico saliente no implica creación de masa.'],
 [c('div','3*a','1/s',r'\nabla\cdot\boldsymbol u'),c('flux','4*pi*a*R**3','m**3/s',r'Q_{sal}'),c('volume','4*pi*R**3/3','m**3',r'\mathcal V'),c('rho','rho0*exp(-3*a*t)','kg/m**3',r'\rho(t)')],
 'Este campo es compresible. Imponer densidad constante sin una fuente de masa sería incompatible con continuidad.',
 r'Comprobar $Q_{sal}=3a\mathcal V$ y $d(\rho\mathcal V)/dt=-\rho Q_{sal}$ en el volumen fijo.',
 'No se propone una ecuación de estado ni una solución global del balance de energía.')

P(11,'Stokes y giro de sólido rígido','Básico',
 r'Un líquido gira como sólido rígido. Obtenga circulación y vorticidad en un círculo horizontal, velocidad periférica y aumento de presión radial. Distinga vorticidad de deformación.',
 [d('Om',2,'1/s','velocidad angular',r'\Omega'),d('R',.15,'m','radio'),d('rho',1000,'kg/m**3','densidad',r'\rho')],
 r'Giro estacionario $\boldsymbol u=(-\Omega y,\Omega x,0)$; la diferencia de presión se compara a igual altura.',
 r'\omega_z=2\Omega,\quad \Gamma=2\pi\Omega R^2,\quad D_{ij}=0,\quad p(R)-p(0)=\rho\Omega^2R^2/2.',
 [r'Evaluar circulación directamente sobre el círculo y por el teorema de Stokes.',r'La parte simétrica del gradiente se anula aunque su parte antisimétrica no lo haga.',r'El balance centrípeto exige $dp/dr=\rho\Omega^2r$; integrar con presión central como referencia.'],
 [c('circulation','2*pi*Om*R**2','m**2/s',r'\Gamma'),c('vorticity','2*Om','1/s',r'\omega_z'),c('V','Om*R','m/s'),c('dp','rho*Om**2*R**2/2','Pa',r'\Delta p')],
 'Vorticidad no significa necesariamente deformación ni disipación viscosa: el giro rígido tiene tasa de deformación nula.',
 r'Comprobar $\Gamma=\omega_z\pi R^2$. El gradiente de presión radial apunta hacia fuera y la fuerza de presión resultante hacia dentro.',
 'La diferencia hidrostática vertical se debe añadir cuando los dos puntos tienen distinta altura.')

P(11,'Fuente y vórtice en un anillo','Avanzado',
 r'En un dominio anular se prescribe $u_r=C/r$, $u_\theta=K/r$. Halle caudal radial por longitud, circulación y aumento de presión entre dos radios. Explique por qué puede existir circulación con rotacional local nulo.',
 [d('C',.003,'m**2/s','intensidad radial'),d('K',.006,'m**2/s','intensidad azimutal'),d('r1',.1,'m','radio interior',r'r_1'),d('r2',.2,'m','radio exterior',r'r_2'),d('rho',1000,'kg/m**3','densidad',r'\rho')],
 r'Flujo ideal estacionario bidimensional en $r_1\le r\le r_2$, sin incluir la singularidad del origen; densidad constante.',
 r'Q^{\prime}=2\pi C,\quad \Gamma=2\pi K,\quad \nabla\cdot\boldsymbol u=0,\quad \nabla\times\boldsymbol u=0\ (r>0),\quad p_2-p_1=\tfrac12\rho(C^2+K^2)(r_1^{-2}-r_2^{-2}).',
 [r'Integrar las componentes normal y tangencial sobre un círculo.',r'Calcular operadores en coordenadas cilíndricas y conservar los factores $r$.',r'Aplicar Bernoulli en el campo irrotacional. Un contorno que rodea el agujero no limita una superficie enteramente contenida en el dominio del campo.'],
 [c('flux','2*pi*C','m**2/s',r'Q^{\prime}'),c('circ','2*pi*K','m**2/s',r'\Gamma'),c('dp','rho*(C**2+K**2)*(1/r1**2-1/r2**2)/2','Pa',r'p_2-p_1')],
 'La topología del dominio es parte de las hipótesis del teorema: no se puede aplicar Stokes atravesando la singularidad excluida.',
 r'Derivar la presión: $dp/dr=\rho(C^2+K^2)/r^3$. Para $K=0$ se conserva el caudal radial y desaparece circulación.',
 'No satisface no deslizamiento en una pared sólida anular y no modela el núcleo de un vórtice real.')

P(12,'Vaciado cuasiestacionario de un depósito','Intermedio',
 r'Un depósito de sección constante descarga por un orificio. Deduzca el tiempo para bajar entre los niveles dados y el caudal inicial, usando el coeficiente de descarga proporcionado.',
 [d('At',.8,'m**2','sección del depósito',r'A_t'),d('Ao',.0004,'m**2','área del orificio',r'A_o'),d('Cd',.62,'','coeficiente de descarga dado',r'C_d'),d('h0',2,'m','nivel inicial sobre orificio',r'h_0'),d('h1',.5,'m','nivel final sobre orificio',r'h_1')],
 'Superficie y salida atmosféricas, líquido incompresible, orificio pequeño respecto del depósito y coeficiente constante entre los niveles dados.',
 r'A_t\dot h=-C_dA_o\sqrt{2gh},\quad t=\frac{2A_t}{C_dA_o\sqrt{2g}}(\sqrt{h_0}-\sqrt{h_1}).',
 [r'Conectar Bernoulli ideal con la corrección empírica $C_d$ suministrada; no deducirla por análisis dimensional.',r'Usar continuidad para relacionar caudal con descenso de nivel.',r'Separar variables e integrar con los límites en el orden que haga positivo el tiempo.'],
 [c('time','2*At/(Cd*Ao*sqrt(2*g))*(sqrt(h0)-sqrt(h1))','s',r't'),c('Q0','Cd*Ao*sqrt(2*g*h0)','m**3/s',r'Q_0'),c('ratio','Ao/At','',r'A_o/A_t')],
 'El caudal decrece al bajar el nivel. Sustituirlo por el inicial durante todo el proceso subestima el tiempo.',
 r'Integrar la ecuación diferencial numéricamente y localizar $h=h_1$. Para $h_1=h_0$ el tiempo es cero.',
 'No extrapolar al vaciado final si cambian la geometría efectiva, la ventilación o el coeficiente de descarga.')

P(12,'Venturi elevado y margen de presión absoluta','Básico',
 r'Una contracción eleva el conducto. Calcule velocidades y presión en la sección estrecha. Convierta a presión absoluta y compare con la presión de vapor suministrada.',
 [d('A1',.01,'m**2','área inicial',r'A_1'),d('A2',.004,'m**2','área estrecha',r'A_2'),d('Q',.02,'m**3/s','caudal'),d('p1',60000,'Pa','presión manométrica inicial',r'p_{1,g}'),d('dz',.3,'m','elevación de la segunda sección',r'\Delta z'),d('rho',1000,'kg/m**3','densidad',r'\rho'),d('patm',101325,'Pa','presión ambiente dada',r'p_{atm}'),d('pv',2500,'Pa','presión de vapor dada',r'p_v')],
 'Flujo estacionario ideal incompresible entre las secciones, sin bomba ni pérdidas; velocidades uniformes.',
 r'V_i=Q/A_i,\quad p_{2,g}=p_{1,g}+\tfrac12\rho(V_1^2-V_2^2)-\rho g\Delta z,\quad p_{2,abs}=p_{2,g}+p_{atm}.',
 [r'Usar continuidad antes de aplicar energía.',r'La elevación y la aceleración reducen ambas la presión del segundo punto.',r'Comparar vapor con presión absoluta, nunca con presión manométrica. La comparación sólo evalúa la sección estudiada bajo el modelo.'],
 [c('V1','Q/A1','m/s',r'V_1'),c('V2','Q/A2','m/s',r'V_2'),c('p2','p1+rho*(V1**2-V2**2)/2-rho*g*dz','Pa',r'p_{2,g}'),c('pabs','p2+patm','Pa',r'p_{2,abs}'),c('margin','pabs-pv','Pa',r'p_{2,abs}-p_v')],
 'Un margen positivo en la sección calculada es compatible con líquido monofásico allí, pero no garantiza ausencia de cavitación en todo el dispositivo.',
 r'Reinsertar los dos estados en Bernoulli. Si $A_2=A_1$ sólo queda la diferencia hidrostática.',
 'No se incluyen pérdidas, mínimos locales de presión ni un modelo de nucleación de cavitación.')

P(12,'Flujo potencial alrededor de un cilindro','Avanzado',
 r'Para la superposición de corriente uniforme y doblete, obtenga velocidad superficial, coeficiente de presión y presión mínima. Explique el resultado de resistencia del modelo y su límite físico.',
 [d('R',.15,'m','radio del cilindro'),d('U',12,'m/s','velocidad lejana'),d('rho',1.2,'kg/m**3','densidad',r'\rho'),d('pinf',101325,'Pa','presión lejana absoluta',r'p_\infty')],
 'Flujo ideal incompresible estacionario, irrotacional, sin circulación y con condición de impermeabilidad en el cilindro.',
 r'\phi=U(r+R^2/r)\cos\theta,\quad u_r(R)=0,\quad u_\theta(R)=-2U\sin\theta,\quad C_p=1-4\sin^2\theta.',
 [r'Derivar el potencial con las métricas polares: $u_r=\partial_r\phi$ y $u_\theta=r^{-1}\partial_\theta\phi$.',r'Aplicar Bernoulli desde la corriente lejana para obtener $C_p$ y localizar su mínimo.',r'La integral simétrica de presión da resistencia y sustentación nulas. Es una propiedad de este modelo, no de un cilindro real.'],
 [c('Vmax','2*U','m/s',r'|u_\theta|_{max}'),c('Cpmin','-3','',r'C_{p,min}'),c('pmin','pinf-1.5*rho*U**2','Pa',r'p_{min}'),c('q','rho*U**2/2','Pa',r'q_\infty')],
 'La paradoja de resistencia nula señala la importancia de viscosidad, capa límite y separación para la resistencia real.',
 r'Integrar $C_p\cos\theta$ y $C_p\sin\theta$ de cero a $2\pi$: ambas integrales se anulan. Comprobar impermeabilidad.',
 'La condición tangencial es de deslizamiento ideal. No representa una pared viscosa con no deslizamiento.')

P(13,'Tracción y disipación en un campo lineal','Intermedio',
 r'Para $u=ax+by$, $v=-ay$, $w=0$, calcule tensor de esfuerzos, tracción normal y tangencial sobre el plano de normal $(1,1,0)/\sqrt2$ y disipación viscosa. Use tangente $(-1,1,0)/\sqrt2$.',
 [d('a',2,'1/s','extensión'),d('b',5,'1/s','cizalla'),d('mu',.3,'Pa*s','viscosidad',r'\mu'),d('p',1200,'Pa','presión')],
 r'Fluido newtoniano incompresible isotrópico, esfuerzo $\boldsymbol\sigma=-p\boldsymbol I+2\mu\boldsymbol D$. La tracción se define como $\boldsymbol\sigma\boldsymbol n$.',
 r'D=\begin{pmatrix}a&b/2&0\\b/2&-a&0\\0&0&0\end{pmatrix},\quad \sigma_{nn}=-p+\mu b,\quad\tau_{tn}=-2\mu a,\quad\Phi=2\mu D:D=\mu(4a^2+b^2).',
 [r'Simetrizar el gradiente y comprobar traza nula.',r'Multiplicar tensor por normal y proyectar el resultado en la normal y la tangente orientada dadas.',r'Contraer el tensor de deformación consigo mismo, contando los dos términos fuera de la diagonal.'],
 [c('sn','-p+mu*b','Pa',r'\sigma_{nn}'),c('st','-2*mu*a','Pa',r'\tau_{tn}'),c('phi','mu*(4*a**2+b**2)','W/m**3',r'\Phi')],
 'La presión contribuye a la tracción normal, mientras la parte viscosa puede tener componentes normales y tangenciales.',
 r'La disipación debe ser no negativa para $\mu>0$ y desaparecer si $D=0$. Invertir la tangente cambia el signo de $\tau_{tn}$.',
 'No se usa esta ley constitutiva para fluidos no newtonianos ni para compresión volumétrica arbitraria.')

P(13,'Calentamiento viscoso entre placas','Avanzado',
 r'En un flujo de Couette con paredes a igual temperatura, determine el incremento máximo de temperatura y el flujo térmico hacia cada pared. Compare la extracción de calor con la potencia mecánica por área.',
 [d('h',.002,'m','separación'),d('U',3,'m/s','velocidad superior'),d('mu',.15,'Pa*s','viscosidad',r'\mu'),d('kt',.13,'W/(m*K)','conductividad',r'k_T'),d('Tw',300,'K','temperatura de pared',r'T_w')],
 'Estado estacionario, propiedades constantes, perfil térmico plenamente desarrollado sin variación longitudinal, conducción transversal y disipación viscosa.',
 r'k_T T^{\prime\prime}+\mu(U/h)^2=0,\quad T-T_w=\frac{\mu U^2}{2k_Th^2}y(h-y),\quad\Delta T_{max}=\frac{\mu U^2}{8k_T}.',
 [r'Insertar el gradiente de Couette en la fuente de disipación.',r'Integrar dos veces con temperaturas iguales en $y=0,h$. El máximo está en el plano medio.',r'Aplicar Fourier en ambas paredes, cuidando sus normales; cada una evacúa la mitad del trabajo mecánico.'],
 [c('rise','mu*U**2/(8*kt)','K',r'\Delta T_{max}'),c('Tmax','Tw+rise','K',r'T_{max}'),c('qwall','mu*U**2/(2*h)','W/m**2',r'|q_w|'),c('power','mu*U**2/h','W/m**2',r'P/A')],
 'El incremento máximo no depende de la holgura en este modelo con velocidad impuesta, aunque el flujo térmico por área sí depende de ella.',
 r'Comprobar $2|q_w|=P/A$ y simetría térmica. Si $U=0$ o $\mu=0$, desaparece la fuente.',
 'Cambios apreciables de propiedades con temperatura o convección longitudinal requieren resolver un problema térmico acoplado.')

P(13,'Difusión de especie a través de una película','Básico',
 r'Una especie diluida difunde entre dos superficies de concentración fija. Obtenga perfil, flujo másico, transferencia total y escala temporal de difusión.',
 [d('D',2e-9,'m**2/s','difusividad'),d('h',100e-6,'m','espesor'),d('c0',10,'kg/m**3','concentración en primera cara',r'c_0'),d('c1',1,'kg/m**3','concentración en segunda cara',r'c_1'),d('A',.02,'m**2','área')],
 'Difusión unidimensional estacionaria de especie diluida, difusividad constante, sin reacción ni advección; $y$ apunta desde la cara 0 a la cara 1.',
 r'c=c_0+(c_1-c_0)y/h,\quad J=-D\,dc/dy=D(c_0-c_1)/h,\quad\dot m=JA,\quad t_D=h^2/D.',
 [r'La conservación estacionaria sin reacción hace constante el flujo.',r'Integrar la ley de Fick con las dos condiciones de concentración.',r'Calcular $t_D$ como escala de orden de magnitud, sin identificarla con un tiempo exacto de establecimiento.'],
 [c('J','D*(c0-c1)/h','kg/(m**2*s)'),c('md','J*A','kg/s',r'\dot m'),c('td','h**2/D','s',r't_D')],
 'El flujo positivo va hacia la concentración menor. Duplicar el espesor divide el flujo estacionario por dos y multiplica la escala temporal por cuatro.',
 r'Comprobar el balance de entrada y salida de especie y las unidades de flujo frente a caudal másico.',
 'No es la ley de transporte de masa total de una mezcla concentrada con contraflujo significativo.')

P(14,'Película que cae por un plano inclinado','Intermedio',
 r'Un líquido forma una película uniforme sobre un plano inclinado. Determine perfil, velocidad máxima, caudal por anchura, tensión en pared y Reynolds definido mediante $q/\nu$.',
 [d('h',.001,'m','espesor'),d('nu',1e-4,'m**2/s','viscosidad cinemática',r'\nu'),d('rho',900,'kg/m**3','densidad',r'\rho'),d('theta',math.pi/6,'','inclinación en radianes',r'\theta')],
 'Película estacionaria uniforme laminar, gas con esfuerzo tangencial despreciable y superficie plana. Coordenada $y$ normal al plano y origen en la pared.',
 r'u=\frac{g\sin\theta}{\nu}(hy-y^2/2),\quad q=\frac{g\sin\theta\,h^3}{3\nu},\quad\tau_w=\rho gh\sin\theta.',
 [r'El balance longitudinal es $\mu u^{\prime\prime}+\rho g\sin\theta=0$.',r'Imponer no deslizamiento en pared y derivada nula en superficie libre.',r'Integrar el perfil y distinguir el Reynolds $q/\nu$ de convenciones que lo multiplican por cuatro. La presión normal es hidrostática.'],
 [c('q','g*sin(theta)*h**3/(3*nu)','m**2/s'),c('umax','g*sin(theta)*h**2/(2*nu)','m/s',r'u_{max}'),c('tau','rho*g*sin(theta)*h','Pa',r'\tau_w'),c('Re','q/nu','',r'\mathrm{Re}_q'),c('pb','rho*g*cos(theta)*h','Pa',r'p_{pared}-p_{atm}')],
 'La condición libre se aplica al esfuerzo tangencial, no a velocidad nula. La superficie es donde el perfil alcanza su máximo.',
 r'Comprobar $u_{max}=3q/(2h)$ y el balance entre peso longitudinal y esfuerzo en pared por unidad de área.',
 'El Reynolds calculado no prueba ausencia de ondas o inestabilidad de superficie; se está estudiando una solución base.')

P(14,'Presión compatible con un remanso viscoso','Avanzado',
 r'Encuentre la presión que hace al campo $u=ax$, $v=-ay$ solución estacionaria de Navier--Stokes sin fuerzas volumétricas. Evalúe presión, gradientes y disipación en el punto dado.',
 [d('rho',1000,'kg/m**3','densidad',r'\rho'),d('a',.4,'1/s','extensión'),d('x',.3,'m','coordenada x'),d('y',.2,'m','coordenada y'),d('p0',100000,'Pa','presión en origen',r'p_0'),d('mu',.01,'Pa*s','viscosidad',r'\mu')],
 'Campo lineal incompresible newtoniano con viscosidad constante; se busca compatibilidad local sin imponer paredes.',
 r'\nabla^2\boldsymbol u=0,\quad\nabla p=-\rho a^2(x,y,0),\quad p=p_0-\tfrac12\rho a^2(x^2+y^2),\quad\Phi=4\mu a^2.',
 [r'Calcular aceleración convectiva y laplaciano de velocidad.',r'La ecuación de momento fija ambas componentes del gradiente de presión; integrarlas usando el valor en el origen.',r'La fuerza viscosa neta local puede anularse aunque exista deformación y disipación. Distinguir divergencia de esfuerzo de producción de calor.'],
 [c('p','p0-rho*a**2*(x**2+y**2)/2','Pa'),c('px','-rho*a**2*x','Pa/m',r'\partial_xp'),c('py','-rho*a**2*y','Pa/m',r'\partial_yp'),c('phi','4*mu*a**2','W/m**3',r'\Phi')],
 'La coincidencia de una constante de Bernoulli en este campo particular no autoriza a aplicar Bernoulli ideal a cualquier flujo viscoso.',
 r'Sustituir presión y velocidad en las dos ecuaciones de momento: sus residuos deben ser cero.',
 'Un campo lineal no es una solución global alrededor de una pared arbitraria; falta el balance térmico si se desea temperatura.')

P(14,'Arranque impulsivo de una placa','Intermedio',
 r'Una placa infinita arranca instantáneamente con velocidad $U$. Determine velocidad en el líquido, esfuerzo en pared, transporte volumétrico por anchura y escala de penetración al tiempo dado.',
 [d('U',.2,'m/s','velocidad de placa'),d('nu',1e-6,'m**2/s','viscosidad cinemática',r'\nu'),d('rho',1000,'kg/m**3','densidad',r'\rho'),d('y',.001,'m','distancia a placa'),d('t',.5,'s','tiempo desde arranque')],
 'Líquido newtoniano semiinfinito inicialmente en reposo, flujo paralelo sin gradiente de presión y $t>0$.',
 r'u=U\,\operatorname{erfc}\!\left(\frac{y}{2\sqrt{\nu t}}\right),\quad \tau_{xy}(0)=-\frac{\mu U}{\sqrt{\pi\nu t}},\quad q=2U\sqrt{\nu t/\pi}.',
 [r'La variable de semejanza es $y/(2\sqrt{\nu t})$. Aplicar las condiciones en placa, infinito e instante inicial para $y>0$.',r'Derivar la función error complementaria; el signo negativo corresponde a $\partial u/\partial y<0$.',r'Integrar el perfil en el semiespacio. La escala $2\sqrt{\nu t}$ no es un borde exacto del fluido en movimiento.'],
 [c('u','U*erfc(y/(2*sqrt(nu*t)))','m/s'),c('tau','-rho*nu*U/sqrt(pi*nu*t)','Pa',r'\tau_{xy}(0)'),c('q','2*U*sqrt(nu*t/pi)','m**2/s'),c('delta','2*sqrt(nu*t)','m',r'\delta_s')],
 'El esfuerzo diverge al acercarse al instante del salto ideal de velocidad. Un arranque físico de duración finita elimina esa idealización.',
 r'Comprobar el residuo difusivo y el balance $\rho\,dq/dt=-\tau_{xy}(0)$.',
 'No describe una placa finita, un arranque suave ni el efecto de otra pared cercana.')

P(15,'Esfera en régimen reptante: viscosidad inversa','Básico',
 r'Una esfera se arrastra horizontalmente a velocidad constante mediante la fuerza dada. Estime viscosidad con Stokes, compruebe Reynolds y calcule potencia. ¿Qué control adicional aportaría repetir a la mitad de velocidad?',
 [d('F',9.42477796076938e-6,'N','fuerza horizontal sintética'),d('R',.0005,'m','radio'),d('U',.001,'m/s','velocidad'),d('rho',1000,'kg/m**3','densidad',r'\rho')],
 'Esfera rígida aislada con no deslizamiento en un fluido newtoniano; la fuerza horizontal compensa sólo resistencia. Paredes lejanas e inercia despreciable por comprobar.',
 r'F=6\pi\mu RU,\quad\mu=F/(6\pi RU),\quad\mathrm{Re}_D=2\rho RU/\mu,\quad P=FU.',
 [r'Invertir la ley de Stokes y conservar radio frente a diámetro.',r'Calcular Reynolds con la viscosidad inferida, cerrando la comprobación de coherencia.',r'En el modelo la fuerza se reduce a la mitad al reducir la velocidad a la mitad; verificarlo con otra medida pondría a prueba linealidad, sin demostrar todas las hipótesis.'],
 [c('mu','F/(6*pi*R*U)','Pa*s',r'\mu'),c('Re','2*rho*R*U/mu','',r'\mathrm{Re}_D'),c('power','F*U','W',r'P'),c('Fhalf','F/2','N',r'F(U/2)')],
 'El Reynolds pequeño obtenido es consistente con la aproximación reptante. No elimina por sí mismo errores por paredes o por no newtonianidad.',
 r'Comprobar $F/(\mu RU)=6\pi$ y positividad de la potencia disipada.',
 'Los datos son académicos. No se confunde este arrastre horizontal con una caída terminal que exige incluir peso y flotación.')

P(15,'Estimación del error hidrostático','Intermedio',
 r'En un flujo somero, estime la razón entre aceleración vertical y gravedad usando las escalas dadas. Compare presión hidrostática y corrección vertical de inercia.',
 [d('L',1000,'m','escala horizontal'),d('H',10,'m','escala vertical'),d('U',2,'m/s','velocidad horizontal'),d('rho',1000,'kg/m**3','densidad',r'\rho')],
 r'Incompresibilidad y variación horizontal en escala advectiva $L/U$; velocidad vertical estimada $W\sim UH/L$. Sin oscilaciones verticales rápidas.',
 r'\varepsilon=H/L,\quad \mathrm{Fr}=U/\sqrt{gH},\quad a_z/g\sim\mathrm{Fr}^2\varepsilon^2,\quad p_h\sim\rho gH,\quad\delta p\sim\rho U^2\varepsilon^2.',
 [r'Estimar $W$ mediante continuidad, sin suponer que es igual a la velocidad horizontal.',r'Escalar $DW/Dt$ con el tiempo advectivo para obtener $U^2H/L^2$.',r'Integrar el orden de la corrección de gradiente vertical a lo largo de $H$ y compararlo con la presión hidrostática.'],
 [c('eps','H/L','',r'\varepsilon'),c('Fr','U/sqrt(g*H)','',r'\mathrm{Fr}'),c('ratio','Fr**2*eps**2','',r'a_z/g\ \mathrm{(escala)}'),c('ph','rho*g*H','Pa',r'p_h'),c('dp','rho*U**2*eps**2','Pa',r'\delta p\ \mathrm{(escala)}')],
 'El resultado es una estimación de escala, no un error calculado de una solución exacta. La hipótesis temporal es esencial.',
 r'La razón $\delta p/p_h$ coincide con $\mathrm{Fr}^2\varepsilon^2$. Una frecuencia impuesta mucho mayor que $U/L$ cambiaría el escalado.',
 'No basta que $H/L$ sea pequeño si hay aceleración vertical rápida, impacto, oleaje corto o saltos.')

P(15,'Reynolds pequeño con inercia no estacionaria','Avanzado',
 r'Un flujo de baja velocidad está forzado en un tiempo muy corto. Calcule Reynolds, Strouhal y su producto para decidir qué términos inerciales pueden despreciarse. Estime la escala viscosa de presión.',
 [d('rho',1000,'kg/m**3','densidad',r'\rho'),d('mu',1,'Pa*s','viscosidad',r'\mu'),d('L',.001,'m','longitud'),d('U',.0001,'m/s','velocidad'),d('T',.0001,'s','tiempo impuesto')],
 'Fluido newtoniano, longitud espacial $L$ y escala temporal externa $T$ independientes; comparación de términos de Navier--Stokes.',
 r'\mathrm{Re}=\rho UL/\mu,\quad \mathrm{St}=L/(UT),\quad\mathrm{Re}\,\mathrm{St}=\rho L^2/(\mu T),\quad p_\nu=\mu U/L.',
 [r'Comparar inercia convectiva con viscosidad mediante Reynolds.',r'Comparar inercia local con viscosidad: el cociente es Reynolds por Strouhal, no Reynolds solo.',r'La presión viscosa sirve de referencia para escribir la ecuación adimensional; cuando la inercia local domina, puede no ser la presión efectiva dominante.'],
 [c('Re','rho*U*L/mu','',r'\mathrm{Re}'),c('St','L/(U*T)','',r'\mathrm{St}'),c('product','Re*St','',r'\mathrm{Re}\,\mathrm{St}'),c('pressure','mu*U/L','Pa',r'p_\nu')],
 'La convección puede ser despreciable mientras la derivada temporal sigue siendo relevante o dominante. No es lícito imponer Stokes estacionario sólo por velocidad pequeña.',
 r'Comprobar el producto directamente como $L^2/(\nu T)$. Para tiempos largos ese producto disminuye.',
 'El análisis ordena términos; no resuelve un campo sin geometría, condiciones de contorno y forma del forzamiento.')

P(16,'Viento geostrófico y signo del gradiente','Intermedio',
 r'Con el gradiente horizontal de presión y el parámetro de Coriolis dados, determine ambas componentes geostróficas y el número de Rossby usando la escala horizontal indicada.',
 [d('f',1e-4,'1/s','parámetro de Coriolis'),d('rho',1.2,'kg/m**3','densidad',r'\rho'),d('px',.0015,'Pa/m','gradiente hacia x',r'\partial_xp'),d('py',-.0006,'Pa/m','gradiente hacia y',r'\partial_yp'),d('L',2e6,'m','escala horizontal')],
 'Plano local con $f>0$ constante, flujo horizontal de gran escala sin fricción ni aceleración en el balance principal. $x,y,z$ forman una base dextrógira.',
 r'f\boldsymbol e_z\times\boldsymbol u_g=-\nabla_hp/\rho,\quad u_g=-\partial_yp/(\rho f),\quad v_g=\partial_xp/(\rho f).',
 [r'Expandir el producto vectorial: sus componentes son $(-fv_g,fu_g)$.',r'Resolver cada ecuación conservando el signo del gradiente suministrado.',r'Calcular Rossby con el módulo de la velocidad resultante y valorar la coherencia del balance dominante.'],
 [c('ug','-py/(rho*f)','m/s',r'u_g'),c('vg','px/(rho*f)','m/s',r'v_g'),c('speed','sqrt(ug**2+vg**2)','m/s',r'|\boldsymbol u_g|'),c('Ro','speed/(f*L)','',r'\mathrm{Ro}')],
 'La velocidad queda perpendicular al gradiente de presión. Rossby pequeño apoya el balance, sin hacerlo exacto ni garantizarlo cerca de fronteras.',
 r'Comprobar $\boldsymbol u_g\cdot\nabla_hp=0$ y ambas componentes de la ecuación vectorial.',
 'La aproximación falla cerca de $f=0$ y necesita términos adicionales para aceleración, curvatura o fricción relevantes.')

P(16,'Estratificación y oscilación de una parcela','Básico',
 r'Un líquido tiene densidad $\rho(z)=\rho_0(1-\alpha z)$ entre fondo y superficie. Estime frecuencia de flotabilidad, período, velocidad máxima de una parcela desplazada y presión hidrostática en el fondo respecto de la superficie.',
 [d('rho0',1000,'kg/m**3','densidad de referencia en fondo',r'\rho_0'),d('alpha',2e-5,'1/m','gradiente relativo',r'\alpha'),d('H',50,'m','profundidad'),d('xi',3,'m','amplitud pequeña de parcela',r'\xi_0')],
 'Coordenada $z$ positiva hacia arriba desde el fondo; aproximación de Boussinesq, parcela sin mezcla ni difusión y oscilación lineal local.',
 r'N^2=-\frac{g}{\rho_0}\frac{d\rho}{dz}=g\alpha,\quad T_N=2\pi/N,\quad |w|_{max}=N\xi_0,\quad\Delta p=\rho_0g(H-\alpha H^2/2).',
 [r'El gradiente de densidad negativo da $N^2>0$ y restauración estable.',r'Resolver $\ddot\xi+N^2\xi=0$ con desplazamiento inicial y velocidad nula.',r'Integrar la densidad variable en hidrostática en lugar de usar una densidad constante sin indicar la aproximación.'],
 [c('N','sqrt(g*alpha)','1/s'),c('period','2*pi/N','s',r'T_N'),c('wmax','N*xi','m/s',r'|w|_{max}'),c('contrast','alpha*H','',r'\alpha H'),c('dp','rho0*g*(H-alpha*H**2/2)','Pa',r'p_f-p_s')],
 'La pequeña variación relativa de densidad permite Boussinesq en la dinámica. La frecuencia de una onda interna general también depende de su geometría de propagación.',
 r'La presión coincide con la densidad media por $gH$ para este perfil lineal. Al hacer $\alpha\to0$ desaparece la restauración estratificada.',
 'No se confunde el oscilador de parcela con una solución completa de ondas internas ni con una estratificación compresible arbitraria.')

P(16,'Convección térmica: escalas de Boussinesq','Avanzado',
 r'Con las propiedades académicas dadas, calcule difusividades, Prandtl, Grashof y Rayleigh. Compruebe la pequeña variación relativa de densidad y explique por qué Rayleigh por sí solo no fija un umbral universal de inestabilidad.',
 [d('rho',1000,'kg/m**3','densidad',r'\rho'),d('mu',.001,'Pa*s','viscosidad',r'\mu'),d('kt',.6,'W/(m*K)','conductividad',r'k_T'),d('cp',4200,'J/(kg*K)','calor específico',r'c_p'),d('beta',2e-4,'1/K','expansión térmica',r'\beta'),d('dT',5,'K','diferencia térmica',r'\Delta T'),d('L',.01,'m','longitud de referencia')],
 'Propiedades constantes de referencia, expansión lineal de densidad y gravedad uniforme. El enunciado define escalas, sin especificar una cavidad ni condiciones térmicas de contorno.',
 r'\nu=\mu/\rho,\quad \kappa_T=k_T/(\rho c_p),\quad \mathrm{Pr}=\nu/\kappa_T,\quad\mathrm{Gr}=g\beta\Delta TL^3/\nu^2,\quad\mathrm{Ra}=\mathrm{Gr}\,\mathrm{Pr}.',
 [r'Construir las dos difusividades con unidades de área por tiempo.',r'Formar los cocientes y verificar que son adimensionales.',r'La condición $\beta\Delta T\ll1$ apoya una parte de la aproximación Boussinesq. Un umbral crítico requiere geometría y condiciones de contorno concretas.'],
 [c('nu','mu/rho','m**2/s',r'\nu'),c('kappa','kt/(rho*cp)','m**2/s',r'\kappa_T'),c('Pr','nu/kappa','',r'\mathrm{Pr}'),c('Gr','g*beta*dT*L**3/nu**2','',r'\mathrm{Gr}'),c('Ra','Gr*Pr','',r'\mathrm{Ra}'),c('variation','beta*dT','',r'\beta\Delta T')],
 'Rayleigh combina flotabilidad y dos procesos difusivos. No se aplica un valor crítico de una capa ideal a cualquier recinto o calentamiento.',
 r'Comprobar también $\mathrm{Ra}=g\beta\Delta TL^3/(\nu\kappa_T)$ y el límite sin diferencia térmica.',
 'Densidad casi constante no asegura por sí sola todas las hipótesis de Boussinesq ni decide estabilidad sin el problema de contorno.')

def evaluate(case):
    """High-precision arithmetic, separate from the unit and model residual checks."""
    env={row[0]:sp.Float(str(row[1]),35) for row in case['data']}
    env.update(g=sp.Float('9.81',35),pi=sp.pi,sqrt=sp.sqrt,exp=sp.exp,log=sp.log,
               sin=sp.sin,cos=sp.cos,tan=sp.tan,erfc=sp.erfc)
    out=[]
    for key,expression,unit,tex in case['calc']:
        value=sp.sympify(expression,locals=env).evalf(32)
        if not value.is_real:raise ValueError((case['id'],key,value))
        env[key]=value;out.append(dict(symbol=key,expression=expression,unit=unit,tex=tex,value=float(value)))
    return out

def cases():return deepcopy(BANK)
