"""Enunciados y criterios de los simulacros S07 a S10 (decimales con coma)."""
LABEL = {1: 'S07', 2: 'S08', 3: 'S09', 4: 'S10'}
STATEMENTS, STRATEGY, SOLUTION = {}, {}, {}

STATEMENTS[1] = r'''\chapter{S07. Materiales III: tensiones, fluencia, difusión e inspección}
\noindent\textbf{Tiempo orientativo: 100 minutos. Cuatro preguntas; 10 puntos.}
\section*{1. Estado plano de tensiones (2,5 puntos)}
Un punto de una chapa ficticia soporta $\sigma_x=120\,\mathrm{MPa}$, $\sigma_y=-40\,\mathrm{MPa}$ y $\tau_{xy}=60\,\mathrm{MPa}$. Calcule las tensiones principales, la tensión tangencial máxima en el plano, la orientación del plano principal mayor y la tensión equivalente de von Mises. Con un límite elástico docente de $350\,\mathrm{MPa}$, indique el coeficiente de seguridad y qué no cubre.

\section*{2. Parámetro de Larson-Miller (2,5 puntos)}
Una pieza ficticia rompe a 100 h a 1000 K y se adopta $C=20$ con el tiempo en horas. Calcule el parámetro y el tiempo de rotura a 1050 K con la misma tensión. Explique dos límites del método.

\section*{3. Profundidad de cementación (2,5 puntos)}
El carbono difunde en austenita con $D_0=2{,}3\times10^{-5}\,\mathrm{m^2/s}$ y $Q=148\,\mathrm{kJ/mol}$. Calcule $D$ a 1223 K y la profundidad característica $\sqrt{Dt}$ tras 4 h, con $R=8{,}314462618\,\mathrm{J/(mol\,K)}$. Explique por qué no es un perfil de dureza.

\section*{4. Ultrasonidos por pulso-eco (2,5 puntos)}
Con $v=6300\,\mathrm{m/s}$ en aluminio, calcule el tiempo de ida y vuelta en una pared de 25 mm y la profundidad de un eco recibido a $4{,}76\,\mu\mathrm s$. Calcule la diferencia en dB entre dos ecos con razón de amplitudes 3 y explique por qué una amplitud no determina el tamaño de la discontinuidad.
'''
STRATEGY[1] = r'Se emplean el círculo de Mohr, la forma de Larson-Miller con logaritmo decimal, la ley de Arrhenius para el coeficiente de difusión y la relación entre tiempo de vuelo y profundidad $d=vt/2$.'
def _s1(v):
    return (
r'''\section{1. Estado plano de tensiones}
El centro del círculo de Mohr es $(\sigma_x+\sigma_y)/2=%(c)s\,\mathrm{MPa}$ y su radio $%(rad)s\,\mathrm{MPa}$. Las tensiones principales son $\sigma_1=%(s1)s\,\mathrm{MPa}$ y $\sigma_2=%(s2)s\,\mathrm{MPa}$, la tangencial máxima en el plano $%(tmax)s\,\mathrm{MPa}$ y el plano principal mayor forma $%(th)s^\circ$ con el eje $x$. La tensión de von Mises es $\sqrt{\sigma_1^2-\sigma_1\sigma_2+\sigma_2^2}=%(svm)s\,\mathrm{MPa}$ y el coeficiente de seguridad estático $350/%(svm)s=%(SF)s$. No cubre fatiga, concentraciones de tensión, tensiones residuales ni inestabilidad.

\section{2. Parámetro de Larson-Miller}
$P=T(C+\log_{10}t)=%(LMP)s\,\mathrm K$. Con el mismo $P$ a $1050\,\mathrm K$, $t=10^{P/T-C}=%(t2)s\,\mathrm h$. El método supone que el mecanismo de fluencia no cambia con la temperatura y que $C$ es constante para el material, y no sustituye ensayos del lote y de la condición de servicio; la sensibilidad a la temperatura es grande: $50\,\mathrm K$ más reducen el tiempo de rotura más de diez veces.

\section{3. Profundidad de cementación}
$D=D_0e^{-Q/(RT)}=%(D)s\,\mathrm{m^2/s}$. Con $t=14400\,\mathrm s$, $\sqrt{Dt}=%(x)s\,\mathrm m$, es decir, unos $0{,}4\,\mathrm{mm}$. Es una escala de penetración del carbono; el perfil de dureza depende además de la concentración superficial, el temple y la transformación martensítica, y la profundidad de capa efectiva se define con un umbral de dureza.

\section{4. Ultrasonidos por pulso-eco}
$t=2d/v=%(tf)s\,\mu\mathrm s$ para $25\,\mathrm{mm}$. El eco a $4{,}76\,\mu\mathrm s$ está a $vt/2=%(de)s\,\mathrm{mm}$. La razón de amplitudes 3 equivale a $20\log_{10}3=%(dB)s\,\mathrm{dB}$. La amplitud depende de la orientación, la rugosidad, el acoplamiento y la atenuación además del tamaño, de modo que no determina por sí sola el tamaño del defecto; para dimensionar se usan bloques de calibración y procedimientos cualificados.''' % v)
SOLUTION[1] = _s1

STATEMENTS[2] = r'''\chapter{S08. Materiales IV: fatiga, daño acumulado, compuestos y fractura}
\noindent\textbf{Tiempo orientativo: 110 minutos. Cuatro preguntas; 10 puntos.}
\section*{1. Curva de Basquin (2,5 puntos)}
Un material ficticio cumple $\sigma_a=\sigma_f'(2N_f)^b$ con $\sigma_f'=900\,\mathrm{MPa}$ y $b=-0{,}09$. Calcule los ciclos hasta rotura para $\sigma_a=300\,\mathrm{MPa}$ y explique dos límites de la ecuación.

\section*{2. Regla de Miner (2,5 puntos)}
Un bloque de carga contiene $2\times10^4$ ciclos de una amplitud con vida $10^5$, $5\times10^4$ de otra con vida $5\times10^5$ y $10^5$ de una tercera con vida $2\times10^6$. Calcule el daño por bloque y los bloques hasta $D=1$. Explique por qué esa predicción no garantiza una vida segura.

\section*{3. Lámina unidireccional (2,5 puntos)}
Una lámina tiene $V_f=0{,}55$, $E_f=200\,\mathrm{GPa}$, $E_m=4\,\mathrm{GPa}$, $\rho_f=1800\,\mathrm{kg/m^3}$ y $\rho_m=1200\,\mathrm{kg/m^3}$. Calcule $E_L$, $E_T$ por el modelo de Reuss, la densidad y el módulo longitudinal específico. Explique por qué la diferencia entre $E_L$ y $E_T$ obliga a laminar en varias orientaciones.

\section*{4. Resistencia residual (2,5 puntos)}
Una placa con grieta superficial tiene $K_{IC}=40\,\mathrm{MPa\sqrt m}$ y $Y=1{,}12$. Calcule la tensión de fallo para semilongitudes de 4 mm y 8 mm, y el tamaño crítico a $250\,\mathrm{MPa}$. Explique la utilidad de la curva de resistencia residual.
'''
STRATEGY[2] = r'Se invierte la ecuación de Basquin, se suman fracciones de vida (Miner), se aplican las reglas de mezclas en paralelo y en serie y se usa $K_I=Y\sigma\sqrt{\pi a}$ igualada a $K_{IC}$.'
def _s2(v):
    return (
r'''\section{1. Curva de Basquin}
Despejando, $2N_f=(\sigma_a/\sigma_f')^{1/b}=%(N2)s$ y $N_f=%(Nf)s$ ciclos. La ecuación describe la región de vida alta con amplitud constante; no incluye tensión media, entallas, acabado superficial, tamaño ni ambiente, y no es válida cerca de la rotura estática ni con plasticidad importante.

\section{2. Regla de Miner}
Los daños parciales son $%(d1)s$, $%(d2)s$ y $%(d3)s$, de modo que $D=%(Dm)s$ por bloque y el fallo se predice tras $1/D=%(nb)s$ bloques. La regla es lineal e independiente del orden; en la práctica el orden de aplicación importa y $D$ en el fallo oscila notablemente respecto a la unidad, por lo que se emplea con factores de dispersión.

\section{3. Lámina unidireccional}
$E_L=V_fE_f+(1-V_f)E_m=%(EL)s\,\mathrm{GPa}$, $E_T=1/(V_f/E_f+(1-V_f)/E_m)=%(ET)s\,\mathrm{GPa}$, $\rho=%(rho)s\,\mathrm{kg/m^3}$ y $E_L/\rho=%(ELesp)s\,\mathrm{J/kg}$. La rigidez en la dirección de la fibra es más de diez veces la transversal, que depende de la matriz; por eso un laminado se compone con orientaciones distintas para dar propiedades útiles en varias direcciones.

\section{4. Resistencia residual}
$\sigma_c=K_{IC}/(Y\sqrt{\pi a})$ da $%(sc1)s\,\mathrm{MPa}$ con $4\,\mathrm{mm}$ y $%(sc2)s\,\mathrm{MPa}$ con $8\,\mathrm{mm}$. A $250\,\mathrm{MPa}$ el tamaño crítico es $a_c=%(ac)s\,\mathrm{mm}$. La curva de resistencia residual muestra cuánta carga soporta una pieza dañada según el tamaño de grieta y permite fijar el tamaño detectable y los intervalos de inspección; en este problema se supone una tenacidad constante y una geometría con $Y$ fijo.''' % v)
SOLUTION[2] = _s2

STATEMENTS[3] = r'''\chapter{S09. Mantenimiento III: contadores, vida límite, fiabilidad y tendencia}
\noindent\textbf{Tiempo orientativo: 90 minutos. Cuatro preguntas; 10 puntos.}
Todos los datos son ficticios y las reglas de intervalo se dan en el enunciado; no corresponden a ningún programa aprobado.
\section*{1. Intervalo con dos contadores (2,5 puntos)}
Una tarea ficticia se repite cada 200 FH o 12 meses, lo que ocurra antes. Se realizó el 2 de marzo de 2026 a 3100 FH. El 8 de octubre de 2026 la aeronave tiene 3250 FH y vuela una media de 6 FH al día. Calcule el margen de cada contador y señale cuál gobierna.

\section*{2. Pieza de vida limitada (2,5 puntos)}
Una pieza tiene vida límite de 20000 ciclos y acumula 17450; se suman 5 ciclos al día. El plazo de aprovisionamiento es de 90 días. Calcule los ciclos y días restantes y cuántos días quedan hasta el último momento para pedir el repuesto.

\section*{3. Fiabilidad básica (2,5 puntos)}
Se registraron 6 retiradas no programadas de un componente en 18000 FH. Con tasa constante, calcule la tasa de retirada, el tiempo medio entre retiradas, la probabilidad de no retirada en 500 FH y las retiradas esperadas al mes en una flota de 12 aeronaves con 40 FH cada una. Explique la hipótesis de tasa constante.

\section*{4. Tendencia de un parámetro de motor (2,5 puntos)}
El margen de temperatura de gases de escape de un motor ficticio es 38 K y desciende linealmente $0{,}9\,\mathrm K$ cada 100 FH. Se define una alerta a 15 K. Calcule las horas y los días de uso (6 FH al día) hasta la alerta y explique dos limitaciones de la extrapolación lineal.
'''
STRATEGY[3] = r'Se calculan márgenes en cada contador y se compara el tiempo de uso; la fiabilidad usa una tasa constante $\lambda=n/T$ y $R=e^{-\lambda t}$, y la tendencia se extrapola linealmente.'
def _s3(v):
    return (
r'''\section{1. Intervalo con dos contadores}
Han transcurrido $%(dias)s$ días desde el 2 de marzo, de modo que el margen de calendario es $365-%(dias)s=%(mcal)s$ días. El margen en horas es $3100+200-3250=%(mh)s\,\mathrm{FH}$, equivalente a $%(dh)s$ días de uso: gobierna el contador de horas. Las reglas reales de tolerancia, uso de «lo que ocurra antes» y registro de la ejecución son las del programa aplicable, no las de este ejercicio.

\section{2. Pieza de vida limitada}
Restan $%(rest)s$ ciclos, es decir $%(dias_vida)s$ días de uso. El plazo de aprovisionamiento consume $450$ ciclos, así que el último momento para pedir es dentro de $%(pedido)s$ días. El cálculo supone un uso uniforme; con variaciones de ciclos por día conviene recalcular y mantener un margen de seguridad logístico.

\section{3. Fiabilidad básica}
$\lambda=6/18000=%(lam)s\,\mathrm{FH^{-1}}$ y $\mathrm{MTBUR}=%(mtbur)s\,\mathrm{FH}$. La probabilidad de no retirada en $500\,\mathrm{FH}$ es $e^{-\lambda t}=%(R)s$. La flota acumula $480\,\mathrm{FH}$ al mes, con $%(flota)s$ retiradas esperadas al mes. La tasa constante equivale a una distribución exponencial y no describe desgaste ni mortalidad infantil; con muy pocos sucesos la incertidumbre es grande.

\section{4. Tendencia de un parámetro de motor}
Hasta la alerta faltan $(38-15)/0{,}9\cdot100=%(egt)s\,\mathrm{FH}$, es decir, $%(degt)s$ días de uso. La extrapolación lineal supone una pendiente constante, y el deterioro real puede acelerarse; además, el parámetro depende de la corrección por condiciones ambientales y de la calidad de los datos, por lo que se compara con los límites y la acción definidos por el fabricante.''' % v)
SOLUTION[3] = _s3

STATEMENTS[4] = r'''\chapter{S10. Combinada: fluencia, tensión térmica, corrosión y propagación}
\noindent\textbf{Tiempo orientativo: 110 minutos. Cuatro preguntas; 10 puntos.}
\section*{1. Fluencia de Norton (2,5 puntos)}
Una pieza ficticia tiene velocidad de fluencia estacionaria $10^{-8}\,\mathrm{s^{-1}}$ a 150 MPa y 1000 K, con exponente $n=5$. Calcule el cociente de velocidades al subir la tensión a 180 MPa, la velocidad nueva y el tiempo hasta 1 \% de deformación en ambos casos, a temperatura constante. Indique qué fase de fluencia no se representa.

\section*{2. Tensión térmica (2,5 puntos)}
Una barra con $E=200\,\mathrm{GPa}$ y $\alpha=13\times10^{-6}\,\mathrm{K^{-1}}$ sufre un calentamiento de 250 K con coacción total. Calcule la deformación libre, la tensión con coacción total y con coacción del 50 \%. Compare con un límite elástico docente de $400\,\mathrm{MPa}$.

\section*{3. Velocidad de corrosión (2,5 puntos)}
En un ensayo ficticio, una probeta de aluminio ($2{,}7\,\mathrm{g/cm^3}$, $25\,\mathrm{cm^2}$) pierde $0{,}84\,\mathrm g$ en 480 h. Calcule la velocidad de penetración en mm/año y explique por qué no puede extrapolarse sin más al servicio.

\section*{4. Propagación de grieta (2,5 puntos)}
Integre la ley de Paris con $C=3\times10^{-12}$ (m/ciclo, $\Delta K$ en $\mathrm{MPa\sqrt m}$), $m=3$, $Y=1{,}12$ y $\Delta\sigma=90\,\mathrm{MPa}$ entre semilongitudes de 2 mm y 9 mm. Indique dos hipótesis.
'''
STRATEGY[4] = r'Se usa la ley de Norton $\dot\varepsilon\propto\sigma^n$, la deformación térmica $\alpha\Delta T$, la penetración como pérdida de masa entre densidad, área y tiempo, y la integral cerrada de Paris para $m=3$.'
def _s4(v):
    return (
r'''\section{1. Fluencia de Norton}
El cociente es $(180/150)^5=%(rt)s$ y la velocidad nueva $%(e1)s\,\mathrm{s^{-1}}$. El tiempo hasta $1\,\%%$ es $%(t0)s\,\mathrm h$ con $150\,\mathrm{MPa}$ y $%(t1)s\,\mathrm h$ con $180\,\mathrm{MPa}$. El modelo describe solo la fluencia secundaria: no incluye la primaria ni la terciaria, que acorta la vida real.

\section{2. Tensión térmica}
La deformación libre es $\alpha\Delta T=%(eps)s$, la tensión con coacción total $E\alpha\Delta T=%(sth)s\,\mathrm{MPa}$ y con coacción del $50\,\%%$ $%(sth2)s\,\mathrm{MPa}$. La primera supera el límite elástico docente de $400\,\mathrm{MPa}$, de modo que habría plastificación y el cálculo elástico deja de valer; en la segunda se queda por debajo, aunque sin margen para ciclos repetidos.

\section{3. Velocidad de corrosión}
La penetración es $\Delta m/(\rho At)=%(v)s\,\mathrm{mm/año}$ sobre una probeta uniforme. No se extrapola porque el ensayo acelerado puede tener otro mecanismo, la corrosión real es localizada (picaduras, exfoliación, fisuración) y depende de la protección, el ambiente y el tiempo de humectación.

\section{4. Propagación de grieta}
Para $m=3$, $N=2(a_i^{-1/2}-a_f^{-1/2})/[C(Y\Delta\sigma\sqrt\pi)^3]=%(Np)s$ ciclos. Se supone región de Paris, amplitud constante y $Y$ constante; el cálculo omite el umbral, la zona de rotura rápida, la plasticidad en punta, el cierre de grieta y los efectos del ambiente, y no sustituye un análisis de tolerancia al daño con datos verificados.''' % v)
SOLUTION[4] = _s4
