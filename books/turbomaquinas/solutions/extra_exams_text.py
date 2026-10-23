"""Enunciados y criterios de los simulacros adicionales C, D y E de Turbomáquinas."""
LABEL = {1: 'C', 2: 'D', 3: 'E'}
STATEMENTS, STRATEGY, SOLUTION = {}, {}, {}

STATEMENTS[1] = r'''\chapter{Simulacro C: compresión axial y radial}
\noindent\textbf{Condiciones.} 120 minutos orientativos. Declare convenios, hipótesis y unidades; el sentido positivo de las velocidades tangenciales es el de la velocidad periférica $U$. Gas perfecto con $c_p=1005\,\mathrm{J/(kg\,K)}$ y $\gamma=1.4$. Propuesta original, sin carácter oficial.
\section{Cuestiones razonadas (2 puntos)}
Explique por qué el trabajo de Euler de un escalón no depende de la eficiencia y sí lo hace la razón de presiones. Indique qué mide el cociente de velocidades relativas $W_2/W_1$ y por qué se limita en un rotor de compresor. Explique por qué el deslizamiento reduce el trabajo de un rodete radial.
\section{Escalón de compresor axial (4 puntos)}
Un escalón trabaja al radio medio con $T_{01}=288.15\,\mathrm K$, $p_{01}=101325\,\mathrm{Pa}$, $U=250\,\mathrm{m/s}$, $C_x=160\,\mathrm{m/s}$ constante, remolino absoluto $C_{\theta1}=70\,\mathrm{m/s}$ a la entrada del rotor y $C_{\theta2}=180\,\mathrm{m/s}$ a la salida. El rendimiento total-total es $0.88$ y el caudal $20\,\mathrm{kg/s}$.
\begin{enumerate}[label=\alph*)]
\item Calcule el trabajo específico, el aumento de temperatura total, la razón de presiones y la presión total de salida. (1.5)
\item Calcule la potencia absorbida y la reacción del escalón. (1.0)
\item Calcule las velocidades relativas, los ángulos relativos y el cociente de velocidades relativas; comente su valor. (1.5)
\end{enumerate}
\section{Rodete centrífugo (4 puntos)}
Un rodete de $0.30\,\mathrm m$ de diámetro gira a $36000\,\mathrm{min^{-1}}$ sin prerrotación y con deslizamiento $0.85$. La temperatura total de entrada es $300\,\mathrm K$ y el rendimiento total-total $0.80$.
\begin{enumerate}[label=\alph*)]
\item Calcule la velocidad periférica de salida y el remolino absoluto de salida. (1.0)
\item Calcule el trabajo específico, el aumento de temperatura total y la razón de presiones. (1.5)
\item Calcule el Mach periférico y la potencia para $1.2\,\mathrm{kg/s}$; discuta qué límites de diseño aparecen. (1.5)
\end{enumerate}
'''
STRATEGY[1] = r'Se aplica la ecuación de Euler con radio constante en el escalón axial y con $C_{\theta1}=0$ en el rodete. La razón de presiones sale del rendimiento total-total; la reacción, de la cinemática con $C_x$ constante.'
def _s1(v):
    return (
r'''\textbf{Cuestiones.} El trabajo de Euler es el cambio del flujo de momento angular y solo depende de la cinemática, $w=U\,\Delta C_\theta$; la eficiencia determina qué parte de ese trabajo se convierte en aumento de presión total y qué parte se pierde como entropía, de modo que a igual $w$ una eficiencia menor da menor razón de presiones. El cociente $W_2/W_1$ mide la desaceleración relativa en el rotor y es un indicador de difusión: por debajo de unos $0.7$ el riesgo de desprendimiento aumenta, aunque el umbral depende del perfil y no se universaliza. El deslizamiento reduce el remolino de salida porque el flujo no sigue el álabe, con lo que cae $C_{\theta2}$ y el trabajo.

\textbf{Escalón axial.} $w=U(C_{\theta2}-C_{\theta1})=%(w)s\,\mathrm{J/kg}$ y $\Delta T_0=%(dT0)s\,\mathrm K$, de modo que $T_{02}=%(T02)s\,\mathrm K$. La razón de presiones es $%(pr)s$ y $p_{02}=%(p02)s\,\mathrm{Pa}$. La potencia es $\dot m w=%(P)s\,\mathrm W$ y la reacción $1-(C_{\theta1}+C_{\theta2})/(2U)=%(R)s$. Las velocidades relativas son $W_1=%(W1)s\,\mathrm{m/s}$ y $W_2=%(W2)s\,\mathrm{m/s}$, con ángulos $%(b1)s^\circ$ y $%(b2)s^\circ$ respecto al eje. El cociente $W_2/W_1=%(DH)s$ está justo por encima de $0.72$, valor que suele citarse como límite para evitar difusión excesiva; se trata de un criterio orientativo.

\textbf{Rodete.} $U_2=%(U2)s\,\mathrm{m/s}$ y $C_{\theta2}=\sigma U_2=%(Cth2r)s\,\mathrm{m/s}$. El trabajo es $w=U_2C_{\theta2}=%(wr)s\,\mathrm{J/kg}$ y $\Delta T_0=%(dT0r)s\,\mathrm K$, con razón de presiones $%(prr)s$. El Mach periférico es $U_2/a_{01}=%(Mu)s$ con $a_{01}=%(a01)s\,\mathrm{m/s}$, y la potencia con $1.2\,\mathrm{kg/s}$ es $%(Pr)s\,\mathrm W$. Un Mach periférico supersónico obliga a vigilar el choque en el difusor, y la tensión del rodete limita la velocidad periférica; ninguno de los dos efectos entra en este cálculo ideal.''' % v)
SOLUTION[1] = _s1

STATEMENTS[2] = r'''\chapter{Simulacro D: turbina axial, pala y refrigeración}
\noindent\textbf{Condiciones.} 120 minutos orientativos. Declare convenios, hipótesis y unidades. Gas caliente con $c_p=1150\,\mathrm{J/(kg\,K)}$ y $\gamma=1.33$. Propuesta original, sin carácter oficial.
\section{Cuestiones razonadas (2 puntos)}
Defina coeficiente de carga y de flujo y explique cómo condicionan el diseño del escalón. Explique por qué la reacción de una turbina se define con la caída de entalpía estática del rotor y qué hipótesis hace falta para igualar el trabajo con la caída del escalón. Indique por qué la tensión centrífuga de una pala no depende de la forma de la sección en el modelo de barra uniforme.
\section{Escalón de turbina con descarga axial (4 puntos)}
Un escalón repetitivo trabaja al radio medio con $T_{01}=1400\,\mathrm K$, $U=320\,\mathrm{m/s}$ y $C_x=200\,\mathrm{m/s}$ constante. El remolino a la salida del estator es $C_{\theta2}=384\,\mathrm{m/s}$ y el escalón descarga axialmente. El rendimiento total-total es $0.90$.
\begin{enumerate}[label=\alph*)]
\item Calcule el trabajo específico, los coeficientes de carga y de flujo y la caída de temperatura total. (1.5)
\item Calcule la razón de expansión total-total y el ángulo absoluto de entrada al rotor. (1.0)
\item Calcule las velocidades relativas al cuadrado a la entrada y a la salida del rotor y la reacción. (1.5)
\end{enumerate}
\section{Pala y pared refrigerada (4 puntos)}
Una pala de acero de densidad $8200\,\mathrm{kg/m^3}$ gira a $9000\,\mathrm{min^{-1}}$ con cubo a $0.35\,\mathrm m$ y punta a $0.45\,\mathrm m$. Se adopta una tensión admisible docente de $400\,\mathrm{MPa}$. La pared de la pala tiene $1.5\,\mathrm{mm}$ de espesor y conductividad $25\,\mathrm{W/(m\,K)}$; el gas exterior ($T_{aw}=1500\,\mathrm K$, $h_g=1800\,\mathrm{W/(m^2\,K)}$) y el refrigerante ($700\,\mathrm K$, $h_c=2500\,\mathrm{W/(m^2\,K)}$) dan una red estacionaria unidimensional.
\begin{enumerate}[label=\alph*)]
\item Calcule la tensión centrífuga de barra uniforme, la velocidad en la punta y el coeficiente de seguridad. (1.5)
\item Calcule el flujo de calor, la temperatura de la pared caliente y la diferencia de temperatura a través de la pared. (1.5)
\item Calcule la tensión térmica con restricción total uniaxial, con $E=190\,\mathrm{GPa}$ y $\alpha=14\times10^{-6}\,\mathrm{K^{-1}}$, e indique qué fenómenos deja fuera. (1.0)
\end{enumerate}
'''
STRATEGY[2] = r'El escalón repetitivo con descarga axial se resuelve con Euler; la reacción sale de la caída estática del rotor entre el trabajo, con radio constante. La pala se trata como barra uniforme sometida a fuerza centrífuga y la pared como una red térmica de tres resistencias en serie.'
def _s2(v):
    return (
r'''\textbf{Cuestiones.} El coeficiente de carga $\psi=w/U^2$ mide el trabajo extraído por unidad de energía cinética periférica y el de flujo $\phi=C_x/U$ el caudal axial adimensional; juntos fijan los ángulos de los triángulos y, con ellos, la difusión y las pérdidas. La reacción es el cociente de la caída de entalpía estática del rotor entre la del escalón; con radio constante y rotor adiabático la caída estática del rotor es $(W_3^2-W_2^2)/2$, y en un escalón repetitivo ($C_3=C_1$) la caída del escalón coincide con el trabajo. En una barra uniforme la tensión en la raíz es el peso centrífugo del material por encima de ella dividido por el área, y el área se cancela.

\textbf{Escalón.} $w=UC_{\theta2}=%(w)s\,\mathrm{J/kg}$, $\psi=%(psi)s$, $\phi=%(phi)s$ y $\Delta T_0=%(dT0)s\,\mathrm K$. La razón de expansión es $%(pr)s$ y el ángulo absoluto de entrada al rotor es $%(a2)s^\circ$. Las velocidades relativas al cuadrado son $W_2^2=%(W2sq)s\,\mathrm{m^2/s^2}$ y $W_3^2=%(W3sq)s\,\mathrm{m^2/s^2}$, y la reacción es $(W_3^2-W_2^2)/(2w)=%(R)s$.

\textbf{Pala.} $\sigma=\rho\omega^2(r_t^2-r_h^2)/2=%(sig)s\,\mathrm{Pa}$ con $U_t=%(Ut)s\,\mathrm{m/s}$, de modo que el coeficiente de seguridad frente a $400\,\mathrm{MPa}$ es $%(SF)s$. La red térmica tiene $R=%(Rt)s\,\mathrm{m^2K/W}$, un flujo $q=%(q)s\,\mathrm{W/m^2}$, una pared caliente a $%(Twh)s\,\mathrm K$ y una diferencia de temperatura de $%(dTw)s\,\mathrm K$ a través de la pared. La tensión térmica con restricción total es $E\alpha\Delta T=%(sth)s\,\mathrm{Pa}$. El modelo deja fuera la concentración de tensiones en la raíz, la fluencia a esa temperatura, la fatiga, la película de refrigeración y el gradiente térmico bidimensional en el borde de ataque.''' % v)
SOLUTION[2] = _s2

STATEMENTS[3] = r'''\chapter{Simulacro E: fuera de diseño y acoplamiento}
\noindent\textbf{Condiciones.} 120 minutos orientativos. Declare convenios, hipótesis y unidades. Temperatura y presión de referencia $288.15\,\mathrm K$ y $101325\,\mathrm{Pa}$. Propuesta original, sin carácter oficial.
\section{Cuestiones razonadas (2 puntos)}
Explique qué representa el régimen corregido y bajo qué hipótesis dos puntos con el mismo régimen y caudal corregidos tienen la misma razón de presiones. Indique por qué un margen de bombeo no puede deducirse solo de los datos de un punto de funcionamiento. Explique por qué la potencia de la turbina de un generador de gas debe igualar la del compresor más las pérdidas mecánicas.
\section{Corrección de un punto de ensayo (4 puntos)}
Un compresor se ensaya con $T_{in}=250\,\mathrm K$ y $p_{in}=70000\,\mathrm{Pa}$. Mide un caudal de $14\,\mathrm{kg/s}$ a $10200\,\mathrm{min^{-1}}$.
\begin{enumerate}[label=\alph*)]
\item Calcule el régimen y el caudal corregidos. (2.0)
\item Determine el régimen físico y el caudal físico del punto equivalente con $T=320\,\mathrm K$ y $p=101325\,\mathrm{Pa}$. (1.5)
\item Indique qué hipótesis de semejanza se usan. (0.5)
\end{enumerate}
\section{Generador de gas (4 puntos)}
El compresor de un generador de gas mueve $22\,\mathrm{kg/s}$ con un aumento de temperatura total de $240\,\mathrm K$ ($c_p=1005\,\mathrm{J/(kg\,K)}$). La turbina recibe $(1+0.02-0.05)$ veces ese caudal (combustible $2\,\%$, sangrado $5\,\%$), con $c_p=1150\,\mathrm{J/(kg\,K)}$, $\gamma=1.33$, rendimiento mecánico $0.99$, rendimiento total-total $0.88$ y temperatura total de entrada $1450\,\mathrm K$.
\begin{enumerate}[label=\alph*)]
\item Calcule la potencia del compresor. (1.0)
\item Calcule la caída de temperatura total de la turbina. (1.5)
\item Calcule la razón de expansión total-total e indique tres efectos que el modelo omite. (1.5)
\end{enumerate}
'''
STRATEGY[3] = r'La corrección usa los cocientes $\theta=T/T_{ref}$ y $\delta=p/p_{ref}$: $N/\sqrt\theta$ y $\dot m\sqrt\theta/\delta$. El acoplamiento iguala la potencia del compresor con la de la turbina multiplicada por el rendimiento mecánico, y la razón de expansión sale de la caída de temperatura con el rendimiento total-total.'
def _s3(v):
    return (
r'''\textbf{Cuestiones.} El régimen corregido $N/\sqrt\theta$ y el caudal corregido $\dot m\sqrt\theta/\delta$ agrupan los efectos de la temperatura y la presión de entrada si el gas es el mismo, el número de Reynolds es comparable y la cinemática es semejante; entonces la razón de presiones y el rendimiento son iguales. Un margen de bombeo es una distancia a la línea de bombeo del mapa, y esa línea solo se conoce con datos experimentales del compresor completo. La turbina entrega la potencia que absorbe el compresor y los auxiliares, más las pérdidas mecánicas, porque comparten eje: si hubiera un exceso, el régimen aumentaría.

\textbf{Corrección.} $\theta=%(th)s$ y $\delta=%(de)s$. El régimen corregido es $%(Nc)s\,\mathrm{min^{-1}}$ y el caudal corregido $%(mc)s\,\mathrm{kg/s}$. Para $T=320\,\mathrm K$ y $p=101325\,\mathrm{Pa}$, $\theta=%(th2)s$ y $\delta=1$: el régimen físico es $%(N2)s\,\mathrm{min^{-1}}$ y el caudal físico $%(m2)s\,\mathrm{kg/s}$. Se supone el mismo gas, número de Reynolds comparable y la misma cinemática; no se corrige por holguras ni por cambios de $\gamma$.

\textbf{Generador de gas.} La potencia del compresor es $%(Pc)s\,\mathrm W$. El caudal de turbina es $%(mt)s\,\mathrm{kg/s}$ y la caída de temperatura total necesaria, $\Delta T_{0t}=P_c/(\eta_m\dot m_tc_{p})=%(dTt)s\,\mathrm K$. Con $\eta_t=0.88$ y $T_{04}=1450\,\mathrm K$ la razón de expansión total-total es $%(prt)s$. El modelo omite el aire de refrigeración reinyectado, la variación de $c_p$ con la temperatura y la potencia de los auxiliares.''' % v)
SOLUTION[3] = _s3
