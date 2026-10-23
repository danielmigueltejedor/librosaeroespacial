"""Enunciados y criterios de los simulacros 4 a 8 (texto en LaTeX).

Las cifras de `SOLUTION[n]` se obtienen de `extra_exams_steps.STEPS[n]`.
"""

COMMON = (r'Tiempo sugerido: {t} minutos. Puntuación: 10 puntos. Se permite una calculadora. '
          r'Esta propuesta no describe las condiciones oficiales de examen. {extra}')

STATEMENTS = {}
STRATEGY = {}
SOLUTION = {}

# ---------------------------------------------------------------- simulacro 4
STATEMENTS[4] = r'''\chapter{Simulacro 4: compresibilidad, ondas de choque y perfiles}
\caja{Condiciones editoriales}{Tiempo sugerido: 110 minutos. Puntuación: 10 puntos. Se permite una calculadora. Esta propuesta no describe las condiciones oficiales de examen. Use ISA con altitud geopotencial, $g_0=9.80665\,\mathrm{m/s^2}$, $R_a=287.05287\,\mathrm{J/(kg\,K)}$ y $\gamma=1.4$.}
\section{Cuestiones razonadas: 2 puntos}
Explique por qué a través de un choque normal estacionario aumenta la entropía y disminuye la presión total mientras la temperatura total se conserva. Distinga el ángulo de Mach del ángulo de un choque oblicuo e indique cuándo coinciden. Justifique por qué la corrección de Prandtl-Glauert no sirve en régimen supersónico ni en las cercanías de $M=1$. Reparta la respuesta en tres explicaciones breves con sus hipótesis. (0.7 + 0.7 + 0.6)
\section{Pitot en vuelo supersónico: 3 puntos}
Una aeronave de investigación vuela en ISA a $H=12000\,\mathrm m$ con $M=2.0$. Se supone gas perfecto, un choque normal desprendido frente a la toma de un tubo Pitot y desaceleración isentrópica posterior hasta la toma.
\begin{enumerate}[label=\alph*)]
\item Calcule $p$, $T$, $\rho$, la velocidad del sonido y la velocidad de vuelo. (0.8)
\item Obtenga el Mach tras el choque y los cocientes de presión, densidad y temperatura estáticas a través de él, además de $p_{t2}/p_{t1}$. (1.2)
\item Calcule la presión de remanso $p_{t2}$ que mediría el Pitot. Si un observador aplicase por error la fórmula subsónica a $p_{t2}$ y $p$, ¿qué Mach leería? Interprete la diferencia. (1.0)
\end{enumerate}
\section{Cuña y choque oblicuo: 3 puntos}
Una corriente de aire con $M_1=2.5$ incide sobre una cuña que produce un choque oblicuo unido de ángulo $\beta=40^\circ$.
\begin{enumerate}[label=\alph*)]
\item Determine el ángulo de desviación $\theta$ de la cuña mediante la relación $\theta$-$\beta$-$M$. (1.0)
\item Calcule los cocientes de presión, densidad y temperatura estáticas a través del choque. (1.0)
\item Obtenga el Mach tras el choque, compruebe que sigue siendo supersónico y explique por qué no existe solución con choque unido si $\theta$ supera un máximo que depende de $M_1$. (1.0)
\end{enumerate}
\section{Perfil y compresibilidad: 2 puntos}
Un perfil de cuerda $c=1.8\,\mathrm m$ vuela a $H=3000\,\mathrm m$ en ISA con $M=0.6$. Use teoría de perfil delgado con pendiente $2\pi\,\mathrm{rad^{-1}}$, $\alpha=4^\circ$ y $\alpha_{L0}=-1.5^\circ$. La viscosidad sigue la ley de Sutherland: $\mu=1.716\times10^{-5}(T/273.15)^{3/2}(273.15+110.4)/(T+110.4)$.
\begin{enumerate}[label=\alph*)]
\item Calcule velocidad de vuelo, densidad y número de Reynolds. (1.0)
\item Obtenga $C_l$ incompresible y con corrección de Prandtl-Glauert; comente su validez. (1.0)
\end{enumerate}
'''
STRATEGY[4] = (r'La atmósfera ISA da el estado antes del choque. Para el choque normal se usan las relaciones de Rankine-Hugoniot en función de $M_1$; la presión de remanso medida por un Pitot supersónico sigue la fórmula de Rayleigh. En el choque oblicuo, la relación $\theta$-$\beta$-$M$ da la desviación y las relaciones normales se aplican a $M_1\sin\beta$. En el perfil se usa $\rho Vc/\mu$ y la corrección lineal subsónica.')
def _s4(v, f):
    return (
r'''\textbf{Cuestiones.} Un choque es un proceso irreversible: la entropía aumenta y la presión total cae, mientras que la temperatura total se conserva porque el flujo es adiabático y no hay trabajo. Solo es posible un salto de supersónico a subsónico, nunca el contrario. El ángulo de Mach $\mu=\arcsin(1/M)$ corresponde a perturbaciones infinitesimales; un choque oblicuo de intensidad finita tiene $\beta>\mu$, y ambos coinciden solo en el límite de desviación nula. La corrección de Prandtl-Glauert procede de linealizar flujo subsónico con perturbaciones pequeñas; diverge en $M\to1$, donde aparecen regiones supersónicas locales y choques, y en supersónico la teoría lineal es la de Ackeret, con otra forma.

\textbf{Pitot.} A $12000\,\mathrm m$ la capa es isoterma con $T=%(T11)s\,\mathrm K$. Se obtiene $p=%(p1)s\,\mathrm{Pa}$, $\rho=%(rho1)s\,\mathrm{kg/m^3}$, $a=%(a1)s\,\mathrm{m/s}$ y $V=%(V1)s\,\mathrm{m/s}$. Con $M_1=2$, el choque normal da $M_2=%(M2)s$, $p_2/p_1=%(pr)s$, $\rho_2/\rho_1=%(rr)s$, $T_2/T_1=%(Tr)s$ y $p_{t2}/p_{t1}=%(ptr)s$. El Pitot mide $p_{t2}=%(pt2)s\,\mathrm{Pa}$. Con la fórmula subsónica se leería $M=%(Mfalse)s$ en lugar de $2$: el error es grande porque esa fórmula supone compresión isentrópica completa y aquí hay una pérdida de presión total en el choque desprendido.

\textbf{Cuña.} La relación $\tan\theta=2\cot\beta\,(M_1^2\sin^2\beta-1)/[M_1^2(\gamma+\cos2\beta)+2]$ da $\theta=%(thetadeg)s^\circ$. La componente normal es $M_{n1}=%(Mn1)s$, con $p_2/p_1=%(pr2)s$, $\rho_2/\rho_1=%(rr2)s$ y $T_2/T_1=%(Tr2)s$. Tras el choque, $M_{n2}=%(Mn2)s$ y $M_2=M_{n2}/\sin(\beta-\theta)=%(Mo2)s$, todavía supersónico: es un choque débil. Para cada $M_1$ existe una desviación máxima; por encima de ella el choque se desprende y pasa a ser curvo.

\textbf{Perfil.} A $3000\,\mathrm m$, $T=%(Tc)s\,\mathrm K$, $\rho=%(rhoc)s\,\mathrm{kg/m^3}$ y $a=%(ac)s\,\mathrm{m/s}$, de modo que $V=%(Vc)s\,\mathrm{m/s}$. Con $\mu=%(muc)s\,\mathrm{Pa\,s}$ resulta $Re=%(Re)s$. El coeficiente incompresible es $C_l=2\pi(\alpha-\alpha_{L0})=%(Cl0)s$; con $\beta_{PG}=\sqrt{1-M^2}=%(bPG)s$ se obtiene $C_l=%(Clc)s$. La corrección es razonable a $M=0.6$ si el perfil es delgado y la incidencia pequeña, y deja de serlo cerca del Mach crítico.''' % f)
SOLUTION[4] = _s4

# ---------------------------------------------------------------- simulacro 5
STATEMENTS[5] = r'''\chapter{Simulacro 5: motores de explosión, de reacción y cohete}
\caja{Condiciones editoriales}{Tiempo sugerido: 120 minutos. Puntuación: 10 puntos. Se permite una calculadora. Esta propuesta no describe las condiciones oficiales de examen. Salvo indicación, use $\gamma=1.4$ y $R_a=287.05287\,\mathrm{J/(kg\,K)}$ con calores específicos constantes. $g_0=9.80665\,\mathrm{m/s^2}$.}
\section{Cuestiones razonadas: 2 puntos}
Explique por qué el rendimiento térmico del ciclo Otto ideal depende solo de la relación de compresión y por qué no puede aumentarse indefinidamente en un motor real. Justifique por qué un turborreactor tiene mayor rendimiento propulsivo cuanto más se acerca la velocidad de salida a la de vuelo y qué se pierde a cambio. Defina impulso específico e indique por qué el valor en vacío es mayor que a nivel del mar para una misma tobera. (0.7 + 0.7 + 0.6)
\section{Ciclo Otto ideal: 2.5 puntos}
Un motor de encendido por chispa admite aire a $T_1=300\,\mathrm K$ y $p_1=95\,\mathrm{kPa}$, con relación de compresión $r=9$. El aporte de calor a volumen constante es $q=1.2\,\mathrm{MJ/kg}$.
\begin{enumerate}[label=\alph*)]
\item Calcule temperatura y presión al final de la compresión isentrópica. (0.8)
\item Calcule temperatura y presión tras el aporte de calor y la temperatura al final de la expansión. (0.9)
\item Determine el rendimiento térmico, el trabajo neto específico y compruebe el balance de calor cedido de dos formas. (0.8)
\end{enumerate}
\section{Turborreactor con tobera adaptada: 2.5 puntos}
Un turborreactor ingiere $45\,\mathrm{kg/s}$ de aire en vuelo a $220\,\mathrm{m/s}$. El dosado másico es $f=0.015$ y los gases salen a $620\,\mathrm{m/s}$ con la presión ambiente.
\begin{enumerate}[label=\alph*)]
\item Calcule el empuje. (1.0)
\item Obtenga la potencia propulsiva, el incremento de energía cinética de la corriente y el rendimiento propulsivo. (1.0)
\item Calcule el consumo específico de empuje en $\mathrm{kg/(N\,s)}$ y en $\mathrm{kg/(N\,h)}$. (0.5)
\end{enumerate}
\section{Tobera de un motor cohete: 3 puntos}
La cámara de un motor cohete está a $p_c=5\,\mathrm{MPa}$ y $T_c=3400\,\mathrm K$. Los gases tienen $\gamma=1.2$ y $R=380\,\mathrm{J/(kg\,K)}$. La garganta tiene $A_t=0.04\,\mathrm{m^2}$ y la tobera se diseña para $p_e=60\,\mathrm{kPa}$. Flujo isentrópico unidimensional.
\begin{enumerate}[label=\alph*)]
\item Calcule el gasto másico, la temperatura y la velocidad de salida. (1.0)
\item Obtenga el área de salida, la relación de expansión y el Mach de salida. (1.0)
\item Calcule el empuje al nivel del mar ($p_a=101325\,\mathrm{Pa}$) y en vacío, y los impulsos específicos correspondientes. Indique el régimen de funcionamiento de la tobera al nivel del mar. (1.0)
\end{enumerate}
'''
STRATEGY[5] = (r'En el ciclo Otto se encadenan las dos isentrópicas con el aporte a volumen constante. En el turborreactor se aplica la cantidad de movimiento con tobera adaptada, de modo que no hay término de presión. En la tobera de cohete se usan el gasto crítico, la velocidad de salida isentrópica y la continuidad para el área de salida; el empuje añade el término de presión $(p_e-p_a)A_e$.')
def _s5(v, f):
    return (
r'''\textbf{Cuestiones.} En el ciclo Otto ideal el calor cedido y el aportado son a volumen constante entre las mismas temperaturas límite, y las dos adiabáticas fijan $T_2/T_1=r^{\gamma-1}$; el rendimiento es $1-r^{1-\gamma}$ y no depende del calor aportado. En un motor real la relación está limitada por la detonación del combustible, por pérdidas de calor y por el aumento de tensiones mecánicas. En un turborreactor el rendimiento propulsivo $2V_0/(V_e+V_0)$ aumenta al acercarse $V_e$ a $V_0$, pero el empuje $\dot m(V_e-V_0)$ disminuye si no crece el gasto. El impulso específico mide empuje por unidad de peso de propulsante consumido; en vacío desaparece el término $-p_aA_e$, que resta empuje a nivel del mar.

\textbf{Otto.} Con $r=9$, $T_2=T_1r^{0.4}=%(T2)s\,\mathrm K$ y $p_2=p_1r^{1.4}=%(p2)s\,\mathrm{Pa}$. Con $c_v=R_a/(\gamma-1)=%(cv)s\,\mathrm{J/(kg\,K)}$, el aporte de calor lleva a $T_3=T_2+q/c_v=%(T3)s\,\mathrm K$ y $p_3=p_2T_3/T_2=%(p3)s\,\mathrm{Pa}$. La expansión termina en $T_4=T_3/r^{0.4}=%(T4)s\,\mathrm K$. El rendimiento es $\eta=1-r^{-0.4}=%(eta)s$, el trabajo $w=\eta q=%(w)s\,\mathrm{J/kg}$ y el calor cedido $q-w=%(qout)s\,\mathrm{J/kg}$, que coincide con $c_v(T_4-T_1)=%(qout2)s\,\mathrm{J/kg}$.

\textbf{Turborreactor.} El empuje es $F=\dot m[(1+f)V_e-V_0]=%(F)s\,\mathrm N$. La potencia propulsiva es $FV_0=%(Pu)s\,\mathrm W$ y el incremento de energía cinética $%(dKE)s\,\mathrm W$, por lo que $\eta_p=%(etap)s$. El consumo es $\mathrm{TSFC}=f\dot m/F=%(TSFC)s\,\mathrm{kg/(N\,s)}=%(TSFCh)s\,\mathrm{kg/(N\,h)}$. Es un modelo docente: no considera presión de salida distinta de la ambiente ni sangrados.

\textbf{Cohete.} El gasto crítico es $\dot m=p_cA_t\sqrt{\gamma/(RT_c)}\,[2/(\gamma+1)]^{(\gamma+1)/[2(\gamma-1)]}=%(mdotc)s\,\mathrm{kg/s}$. A la salida, $T_e=T_c(p_e/p_c)^{(\gamma-1)/\gamma}=%(Te)s\,\mathrm K$ y $V_e=%(Vex)s\,\mathrm{m/s}$, con $\rho_e=%(rhoe)s\,\mathrm{kg/m^3}$ y $A_e=\dot m/(\rho_eV_e)=%(Ae)s\,\mathrm{m^2}$. La relación de expansión es $%(eps)s$ y $M_e=%(Mex)s$. El empuje es $F_{sl}=\dot mV_e+(p_e-p_a)A_e=%(Fsl)s\,\mathrm N$ al nivel del mar y $F_{vac}=\dot mV_e+p_eA_e=%(Fvac)s\,\mathrm N$ en vacío, con $I_{sp}=%(Ispsl)s\,\mathrm s$ y $%(Ispvac)s\,\mathrm s$. Como $p_e<p_a$, la tobera está sobreexpandida al nivel del mar; con $p_e/p_a\approx0.59$ no cabe esperar desprendimiento de la capa límite, que suele aparecer con cocientes mucho menores, pero conviene comprobarlo.''' % f)
SOLUTION[5] = _s5

# ---------------------------------------------------------------- simulacro 6
STATEMENTS[6] = r'''\chapter{Simulacro 6: estructuras, materiales y cargas de vuelo}
\caja{Condiciones editoriales}{Tiempo sugerido: 120 minutos. Puntuación: 10 puntos. Se permite una calculadora. Esta propuesta no describe las condiciones oficiales de examen. Los datos de material son docentes: $E=70\,\mathrm{GPa}$ y límite elástico $\sigma_y=300\,\mathrm{MPa}$. Use ISA, $g_0=9.80665\,\mathrm{m/s^2}$ y $R_a=287.05287\,\mathrm{J/(kg\,K)}$.}
\section{Cuestiones razonadas: 2 puntos}
Explique por qué en un recipiente cilíndrico de pared delgada la tensión circunferencial es el doble que la longitudinal. Indique cuándo es válida la fórmula de Euler para una columna y qué ocurre con la carga crítica si se duplica la longitud o se empotran ambos extremos. Defina la velocidad de maniobra y explique qué protege. (0.7 + 0.7 + 0.6)
\section{Fuselaje presurizado: 3 puntos}
Un fuselaje cilíndrico de radio $r=1.9\,\mathrm m$ y espesor $t=1.6\,\mathrm{mm}$ mantiene una altitud de cabina de $2400\,\mathrm m$ mientras la aeronave cruza a $11000\,\mathrm m$ (ISA para ambas).
\begin{enumerate}[label=\alph*)]
\item Calcule las presiones de cabina y exterior y su diferencia. (0.8)
\item Obtenga las tensiones circunferencial y longitudinal, la tensión equivalente de von Mises y el coeficiente de seguridad estático. (1.2)
\item Explique por qué ese coeficiente no garantiza la vida a fatiga ni la tolerancia al daño. (1.0)
\end{enumerate}
\section{Pandeo de una barra tubular: 2.5 puntos}
Una barra tubular biarticulada de diámetro exterior $40\,\mathrm{mm}$, interior $36\,\mathrm{mm}$ y longitud $1.2\,\mathrm m$ trabaja a compresión.
\begin{enumerate}[label=\alph*)]
\item Calcule momento de inercia, área y carga crítica de Euler. (1.0)
\item Obtenga la esbeltez, compruebe la validez de Euler con la esbeltez límite $\pi\sqrt{E/\sigma_y}$ y determine si gobierna el pandeo o la fluencia. (1.0)
\item Indique cómo cambia la carga crítica con empotramiento doble. (0.5)
\end{enumerate}
\section{Maniobra y ráfaga: 2.5 puntos}
Una aeronave ligera de $W=11800\,\mathrm N$ y $S=16\,\mathrm{m^2}$ tiene $C_{L\max}=1.5$. Se toma $\rho_0=1.225\,\mathrm{kg/m^3}$ y un factor de carga límite $n_{\max}=3.8$.
\begin{enumerate}[label=\alph*)]
\item Calcule la velocidad de pérdida con $n=1$ y la velocidad de maniobra. (1.0)
\item Para una ráfaga discreta de $7.6\,\mathrm{m/s}$ a una velocidad equivalente de $45\,\mathrm{m/s}$ y pendiente de sustentación $5.0\,\mathrm{rad^{-1}}$, calcule el incremento y el factor de carga resultante, sin factor de atenuación. (1.0)
\item Compare con el límite e indique dos simplificaciones del modelo. (0.5)
\end{enumerate}
'''
STRATEGY[6] = (r'La presión de cabina y la exterior salen de ISA; el recipiente delgado se resuelve con equilibrio de fuerzas en cada dirección. La barra se estudia con Euler y se compara con la carga de fluencia. La maniobra sigue $n=(V/V_s)^2$ y la ráfaga discreta se aproxima con $\Delta n=\rho_0U_{de}Va/(2W/S)$.')
def _s6(v, f):
    return (
r'''\textbf{Cuestiones.} Un corte longitudinal soporta la presión sobre el área $2rL$ con dos secciones resistentes $2tL$, de donde $\sigma_\theta=pr/t$; un corte transversal soporta $p\pi r^2$ con sección $2\pi rt$, de donde $\sigma_x=pr/(2t)$. La fórmula de Euler es válida si la esbeltez supera la límite $\pi\sqrt{E/\sigma_y}$; al duplicar la longitud la carga crítica se divide por cuatro, y con empotramiento doble se multiplica por cuatro (longitud efectiva $L/2$). La velocidad de maniobra es la mayor a la que un mando brusco completo no supera el factor de carga límite: $V_A=V_s\sqrt{n_{\max}}$.

\textbf{Fuselaje.} A $2400\,\mathrm m$ la temperatura es $%(Tcab)s\,\mathrm K$ y $p_{cab}=%(pcab)s\,\mathrm{Pa}$. A $11000\,\mathrm m$ la presión es $%(pext)s\,\mathrm{Pa}$, de modo que $\Delta p=%(dp)s\,\mathrm{Pa}$. Resulta $\sigma_\theta=%(sth)s\,\mathrm{Pa}$, $\sigma_x=%(sx)s\,\mathrm{Pa}$ y $\sigma_{vM}=%(svm)s\,\mathrm{Pa}$, con un coeficiente de seguridad estático $\sigma_y/\sigma_{vM}=%(SF)s$. Ese valor no cubre la fatiga por ciclos de presurización, ni grietas, ni concentraciones en ventanas y uniones; para ello se analiza la vida con curvas $S$-$N$ y la propagación de grietas con criterio de tolerancia al daño.

\textbf{Pandeo.} $I=%(I)s\,\mathrm{m^4}$, $A=%(A)s\,\mathrm{m^2}$ y $P_{cr}=\pi^2EI/L^2=%(Pcr)s\,\mathrm N$. El radio de giro es $%(rg)s\,\mathrm m$ y la esbeltez $%(lam)s$, mayor que la límite $%(lamc)s$, de modo que Euler es aplicable. La carga de fluencia es $%(Py)s\,\mathrm N$, mayor que $P_{cr}$, así que gobierna el pandeo. Con empotramiento doble la carga crítica sería cuatro veces mayor.

\textbf{Maniobra y ráfaga.} $V_s=\sqrt{2W/(\rho_0SC_{L\max})}=%(Vs)s\,\mathrm{m/s}$ y $V_A=V_s\sqrt{3.8}=%(VA)s\,\mathrm{m/s}$. El incremento por ráfaga es $\Delta n=\rho_0U_{de}Va/(2W/S)=%(dn)s$ y el factor resultante $%(nR)s$, inferior a $3.8$. El modelo ignora el factor de atenuación de ráfaga y la respuesta dinámica del ala, y supone sustentación lineal con la incidencia.''' % f)
SOLUTION[6] = _s6

# ---------------------------------------------------------------- simulacro 7
STATEMENTS[7] = r'''\chapter{Simulacro 7: navegación, ortodrómica y actuaciones de pista}
\caja{Condiciones editoriales}{Tiempo sugerido: 110 minutos. Puntuación: 10 puntos. Se permite una calculadora. Esta propuesta no describe las condiciones oficiales de examen. Tierra esférica de radio $6371\,\mathrm{km}$; ISA con altitud geopotencial, $g_0=9.80665\,\mathrm{m/s^2}$, $R_a=287.05287\,\mathrm{J/(kg\,K)}$.}
\section{Cuestiones razonadas: 2 puntos}
Distinga velocidad verdadera, velocidad respecto al suelo y velocidad indicada. Explique por qué una ruta ortodrómica no mantiene un rumbo constante y cuándo conviene la loxodrómica. Justifique por qué un aeródromo elevado en un día cálido alarga el recorrido de despegue. (0.7 + 0.7 + 0.6)
\section{Triángulo de vientos: 3 puntos}
Una aeronave de $\mathrm{TAS}=75\,\mathrm{m/s}$ debe seguir una derrota $090^\circ$. El viento sopla de $030^\circ$ con $15\,\mathrm{m/s}$.
\begin{enumerate}[label=\alph*)]
\item Calcule las componentes longitudinal y transversal del viento respecto a la derrota. (0.8)
\item Determine el ángulo de corrección de deriva, el rumbo a volar y la velocidad respecto al suelo. (1.4)
\item Calcule el tiempo de un tramo de $180\,\mathrm{km}$. (0.8)
\end{enumerate}
\section{Distancia y rumbo inicial ortodrómicos: 2.5 puntos}
Entre dos aeropuertos de coordenadas redondeadas $40.47^\circ\mathrm N,\,3.56^\circ\mathrm W$ y $41.30^\circ\mathrm N,\,2.08^\circ\mathrm E$.
\begin{enumerate}[label=\alph*)]
\item Calcule el ángulo central por la fórmula haversine y la distancia ortodrómica. (1.5)
\item Obtenga el rumbo inicial y explique su variación a lo largo de la ruta. (1.0)
\end{enumerate}
\section{Recorrido de despegue: 2.5 puntos}
Una aeronave ligera de $W=15000\,\mathrm N$, $S=16\,\mathrm{m^2}$ y $C_{L\max}=1.6$ despega con empuje estático constante $3200\,\mathrm N$ al nivel del mar ($\rho_0=1.225\,\mathrm{kg/m^3}$), con coeficiente de rodadura $\mu=0.03$. Se modela una aceleración media constante $a=g_0(T/W-\mu)$, sin resistencia aerodinámica, y la velocidad de despegue es $1.2V_s$.
\begin{enumerate}[label=\alph*)]
\item Calcule el recorrido al nivel del mar. (0.8)
\item Repítalo en un aeródromo a $2000\,\mathrm m$ ISA con temperatura ISA$+20\,\mathrm K$, suponiendo que el empuje es proporcional a la densidad. (1.2)
\item Compare ambos resultados e indique tres efectos que el modelo omite. (0.5)
\end{enumerate}
'''
STRATEGY[7] = (r'El triángulo de vientos se resuelve proyectando el viento sobre la derrota; la corrección de deriva sale del seno del ángulo transversal. La distancia ortodrómica usa la fórmula haversine y el rumbo inicial la ecuación de rumbo esférico. El despegue se reduce a movimiento uniformemente acelerado hasta $V_{LOF}=1.2V_s$ con la densidad de cada caso.')
def _s7(v, f):
    return (
r'''\textbf{Cuestiones.} La velocidad indicada es la que mide el anemómetro a partir de la presión dinámica; la verdadera la corrige por densidad, y la velocidad respecto al suelo suma el viento a la verdadera. En una esfera, la ruta más corta es un arco de círculo máximo, que corta a los meridianos con ángulos distintos, de modo que el rumbo varía; la loxodrómica mantiene rumbo constante y se usa en tramos cortos o cerca del ecuador. Con densidad menor aumentan la velocidad de pérdida y de despegue y disminuyen el empuje disponible, por lo que se alarga el recorrido.

\textbf{Vientos.} El viento de $030^\circ$ forma $60^\circ$ con la derrota. La componente transversal es $%(cross)s\,\mathrm{m/s}$ y la longitudinal, de cara, $%(head)s\,\mathrm{m/s}$. La corrección de deriva es $\mathrm{WCA}=\arcsin(\mathrm{cross}/\mathrm{TAS})=%(WCAdeg)s^\circ$; el viento llega por la izquierda de la derrota y empuja hacia la derecha, de modo que el rumbo es $090^\circ-%(WCAdeg)s^\circ\approx080.0^\circ$. La velocidad respecto al suelo es $\mathrm{GS}=\mathrm{TAS}\cos\mathrm{WCA}-\mathrm{head}=%(GS)s\,\mathrm{m/s}$ y el tramo de $180\,\mathrm{km}$ dura $%(tmin)s\,\mathrm{min}$.

\textbf{Ortodrómica.} Con haversine, $%(hav)s$ es la haversine del ángulo central, que vale $%(cang)s\,\mathrm{rad}$, y la distancia $%(dist)s\,\mathrm{km}$. El rumbo inicial es $\arctan(\mathrm{by}/\mathrm{bx})=%(brg)s^\circ$; como el denominador es positivo no hace falta corregir el cuadrante. El rumbo cambia a lo largo de la ruta porque los meridianos convergen hacia el polo.

\textbf{Despegue.} Al nivel del mar, $V_s=%(Vs1)s\,\mathrm{m/s}$, $V_{LOF}=%(Vlof1)s\,\mathrm{m/s}$, $a=%(a1)s\,\mathrm{m/s^2}$ y el recorrido es $%(s1)s\,\mathrm m$. A $2000\,\mathrm m$ con ISA$+20$, $T=%(Thot)s\,\mathrm K$, $p=%(p2k)s\,\mathrm{Pa}$ y $\rho=%(rhoh)s\,\mathrm{kg/m^3}$; entonces $V_s=%(Vs2)s\,\mathrm{m/s}$, $V_{LOF}=%(Vlof2)s\,\mathrm{m/s}$, $T=%(T2)s\,\mathrm N$, $a=%(a2)s\,\mathrm{m/s^2}$ y el recorrido es $%(s2)s\,\mathrm m$, es decir $%(ratio)s$ veces el anterior. El modelo omite la resistencia aerodinámica y la sustentación durante la rodadura, el viento, la pendiente de pista y la variación real del empuje con la velocidad.''' % f)
SOLUTION[7] = _s7

# ---------------------------------------------------------------- simulacro 8
STATEMENTS[8] = r'''\chapter{Simulacro 8: sistemas hidráulicos, eléctricos y alcance}
\caja{Condiciones editoriales}{Tiempo sugerido: 110 minutos. Puntuación: 10 puntos. Se permite una calculadora. Esta propuesta no describe las condiciones oficiales de examen. Datos educativos; no representan una aeronave ni un componente certificados. $g_0=9.80665\,\mathrm{m/s^2}$.}
\section{Cuestiones razonadas: 2 puntos}
Explique por qué un actuador hidráulico de doble efecto con vástago de un solo lado desarrolla menos fuerza y más velocidad en retracción que en extensión. Distinga la capacidad nominal de una batería de la energía realmente utilizable. Justifique por qué la ecuación de Breguet supone cociente $L/D$ y consumo específico constantes y qué ocurre si no lo son. (0.7 + 0.7 + 0.6)
\section{Actuador hidráulico: 3 puntos}
Un actuador de doble efecto tiene pistón de $50\,\mathrm{mm}$ de diámetro y vástago de $25\,\mathrm{mm}$. El sistema trabaja a $21\,\mathrm{MPa}$ y el caudal disponible es $1.0\times10^{-3}\,\mathrm{m^3/s}$.
\begin{enumerate}[label=\alph*)]
\item Calcule la fuerza máxima en extensión y en retracción. (0.8)
\item Calcule las velocidades de extensión y de retracción con ese caudal. (0.7)
\item Con una carga de $30\,\mathrm{kN}$ en extensión, calcule potencia hidráulica, potencia útil y potencia disipada; la potencia de entrada de una bomba de rendimiento $0.85$; y la tasa de calentamiento si $18\,\mathrm{kg}$ de fluido ($c=1900\,\mathrm{J/(kg\,K)}$) absorben el calor sin enfriamiento. (1.5)
\end{enumerate}
\section{Batería y cableado: 2.5 puntos}
Una batería de $24\,\mathrm V$ y $40\,\mathrm{Ah}$ alimenta una carga de $15\,\mathrm A$ continuos mediante un cable de cobre ($\rho_{Cu}=1.72\times10^{-8}\,\Omega\,\mathrm m$) de $6\,\mathrm{mm^2}$ y $12\,\mathrm m$ de longitud total de ida y vuelta.
\begin{enumerate}[label=\alph*)]
\item Calcule la autonomía si solo es utilizable el $80\,\%$ de la capacidad. (0.8)
\item Calcule la resistencia del cable, la caída de tensión y la pérdida por efecto Joule. (1.2)
\item Indique la tensión en la carga y la caída relativa. (0.5)
\end{enumerate}
\section{Alcance y autonomía de Breguet: 2.5 puntos}
Una aeronave a reacción vuela a $230\,\mathrm{m/s}$ con $L/D=16$ y consumo específico $1.7\times10^{-5}\,\mathrm{kg/(N\,s)}$. La razón entre pesos inicial y final es $1.25$.
\begin{enumerate}[label=\alph*)]
\item Calcule el alcance de Breguet. (1.2)
\item Calcule la autonomía. (0.8)
\item Obtenga la fracción de combustible respecto al peso inicial e indique dos condiciones que la ecuación supone. (0.5)
\end{enumerate}
'''
STRATEGY[8] = (r'En el actuador se aplican $F=pA$ y $v=Q/A$ con el área útil de cada cámara; las potencias salen del balance hidráulico. La batería se trata como reserva energética utilizable y el cable como una resistencia en serie. El alcance sigue la integración de Breguet para reactor con $L/D$ y consumo constantes.')
def _s8(v, f):
    return (
r'''\textbf{Cuestiones.} En retracción el aceite actúa sobre el área anular, pistón menos vástago: la misma presión da menos fuerza y el mismo caudal da más velocidad. La capacidad nominal es la corriente por hora a un régimen de descarga y temperatura concretos; la utilizable es menor por profundidad de descarga, envejecimiento y temperatura. La ecuación de Breguet integra $dW/W$ suponiendo $V$, $L/D$ y consumo constantes; si cambian con la masa o la altitud hay que integrar por tramos o usar una variante con ascenso escalonado.

\textbf{Actuador.} Las áreas son $A_p=%(Ap)s\,\mathrm{m^2}$ y $A_r=%(Ar)s\,\mathrm{m^2}$. Las fuerzas son $F_{ext}=%(Fext)s\,\mathrm N$ y $F_{ret}=%(Fret)s\,\mathrm N$. Con el caudal dado, $v_{ext}=%(vext)s\,\mathrm{m/s}$ y $v_{ret}=%(vret)s\,\mathrm{m/s}$. Con $30\,\mathrm{kN}$ de carga, que es inferior a $F_{ext}$, la potencia hidráulica es $%(Ph)s\,\mathrm W$, la útil $%(Pu)s\,\mathrm W$ y la disipada $%(loss)s\,\mathrm W$ en válvulas y fugas. La bomba toma $%(Pin)s\,\mathrm W$. Sin enfriamiento, el fluido se calienta a $%(dTdt)s\,\mathrm{K/s}$, es decir, unos $10\,\mathrm K$ por minuto, lo que justifica un intercambiador de calor.

\textbf{Batería.} La autonomía es $0.8\cdot40/15=%(t)s\,\mathrm h$. El cable tiene $R=\rho L/A=%(R)s\,\Omega$, con caída $%(dV)s\,\mathrm V$ y pérdida $%(Ploss)s\,\mathrm W$. La tensión en la carga es $%(Vload)s\,\mathrm V$ si se toman $24\,\mathrm V$ en bornes de la batería, una caída del $%(frac)s\,\%%$.

\textbf{Breguet.} Con $c_w=c\,g_0=%(cw)s\,\mathrm{s^{-1}}$, el alcance es $R=(V/c_w)(L/D)\ln(W_0/W_1)=%(Rbr)s\,\mathrm m\approx4926\,\mathrm{km}$ y la autonomía $E=%(Eh)s\,\mathrm h$. La fracción de combustible es $1-W_1/W_0=%(ff)s$. La ecuación supone empuje igual a resistencia, vuelo horizontal y velocidad y consumo constantes, y no incluye reservas, ascenso ni descenso.''' % f)
SOLUTION[8] = _s8
