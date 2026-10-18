"""Original reproducible Wolfram workshops accompanying existing problem families."""
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
WORKSHOPS=[
('Unidades antes de calcular','MF-P17',
 'Convierte caudal y radio a SI antes de evaluar la caída de presión. Repite el cálculo conservando cantidades con unidades para detectar una confusión entre milímetros y metros.',
 '''q = UnitConvert[Quantity[60, "Milliliters"/"Minutes"], "Meters"^3/"Seconds"];
r = UnitConvert[Quantity[1, "Millimeters"], "Meters"];
mu = Quantity[0.012, "Pascals"*"Seconds"];
len = Quantity[0.8, "Meters"];
dp = UnitConvert[8 mu len q/(Pi r^4), "Pascals"];
value = QuantityMagnitude[dp];
If[Abs[value - 24446.1992589151] > 10^-7, Exit[1]];
Print[ExportString[<|"dp_Pa" -> value|>, "RawJSON"]];''',
 r'$Q=10^{-6}\,\mathrm{m^3/s}$ y $\Delta p\simeq24446.2\,\mathrm{Pa}$. Introducir el radio en milímetros como si fueran metros modifica el resultado por un factor $10^{12}$.',
 'Cambia el radio conservando el caudal. Explica la potencia cuarta. Introduce deliberadamente una unidad incompatible y observa el diagnóstico; no lo conviertas en un valor físico.'),
('Integración temporal de una resistencia cuadrática','MF-P02',
 'Compara un integrador de ecuaciones diferenciales con la solución separada. La coincidencia controla implementación y tolerancias, sin validar la ley de fuerza frente a medidas.',
 '''mass = 24.; drag = 0.8; initial = 8.; final = 6.;
vel = NDSolveValue[{v'[t] == -drag v[t]^2/mass, v[0] == initial}, v, {t, 0, final}, AccuracyGoal -> 11, PrecisionGoal -> 10, MaxStepFraction -> 1/200];
exact[t_] := initial/(1 + drag initial t/mass);
err = Max[Table[Abs[vel[t] - exact[t]], {t, 0, final, final/100}]];
If[err > 10^-7, Exit[1]];
Print[ExportString[<|"velocity_m_s" -> vel[final], "max_error_m_s" -> err|>, "RawJSON"]];''',
 r'$v(6)=3.076923\,\mathrm{m/s}$. El error absoluto en 101 puntos debe quedar por debajo de $10^{-7}\,\mathrm{m/s}$ con la tolerancia propuesta.',
 'Repite con tolerancias más laxas. Compara error de integración con error del modelo. Comprueba el límite de resistencia nula de la solución analítica.'),
('Operadores vectoriales y aceleración','MF-P10',
 'Calcula divergencia, rotacional y aceleración convectiva del campo de remanso sin confundir un campo estacionario con partículas sin aceleración.',
 '''field = {a x, -a y, 0}; coords = {x, y, z};
dv = Div[field, coords]; rot = Curl[field, coords];
acc = Simplify[Table[Sum[field[[j]] D[field[[i]], coords[[j]]], {j, 3}], {i, 3}]];
If[dv =!= 0 || rot =!= {0, 0, 0} || acc =!= {a^2 x, a^2 y, 0}, Exit[1]];
Print[ExportString[<|"divergence" -> dv, "curl" -> rot,
 "acceleration_m_s2" -> N[acc /. {a -> .6, x -> .3, y -> .2}]|>, "RawJSON"]];''',
 r'$\nabla\cdot\boldsymbol u=0$, $\boldsymbol\omega=0$ y $\boldsymbol a=(0.108,0.072,0)\,\mathrm{m/s^2}$ en el punto dado.',
 'Sustituye el campo por una cizalla simple. Explica por qué puede aparecer rotacional sin aceleración. Reconstruye la matriz simétrica y antisimétrica del gradiente.'),
('Depósito: continuidad y evolución de nivel','MF-P34',
 'Integra el nivel hasta el tiempo analítico necesario para alcanzar el nivel final. Evita prolongar el modelo a niveles negativos.',
 '''gravity = 9.81; tank = .8; hole = .0004; cd = .62;
h0 = 2.; h1 = .5;
tf = 2 tank (Sqrt[h0] - Sqrt[h1])/(cd hole Sqrt[2 gravity]);
level = NDSolveValue[{h'[t] == -cd hole Sqrt[2 gravity h[t]]/tank, h[0] == h0}, h, {t, 0, tf}, AccuracyGoal -> 11, PrecisionGoal -> 10];
err = Abs[level[tf] - h1];
If[err > 10^-7, Exit[1]];
Print[ExportString[<|"time_s" -> tf, "terminal_level_m" -> level[tf], "error_m" -> err|>, "RawJSON"]];''',
 r'El nivel final numérico debe coincidir con $0.5\,\mathrm m$ dentro de $10^{-7}\,\mathrm m$. El caudal inicial no permanece constante durante el vaciado.',
 'Duplica la sección del depósito. Repite con otro coeficiente dado y explica el cambio temporal. No interpretes ajustar el coeficiente como una validación sin datos.'),
('Discretización espacial de Poiseuille plano','MF-P16 con pared superior fija',
 'Resuelve la ecuación de contorno mediante una matriz tridiagonal. En este caso el perfil exacto es cuadrático: la segunda diferencia centrada lo reproduce exactamente salvo redondeo.',
 '''gap = .004; visc = .08; grad = 100.; n = 40;
dy = gap/n; grid = Range[1, n - 1] dy;
mat = SparseArray[{Band[{1, 1}] -> -2., Band[{1, 2}] -> 1., Band[{2, 1}] -> 1.}, {n - 1, n - 1}];
profile = LinearSolve[mat, ConstantArray[-grad dy^2/visc, n - 1]];
exact = grad grid (gap - grid)/(2 visc);
err = Max[Abs[profile - exact]];
res = Max[Abs[mat.profile + grad dy^2/visc]];
If[err > 10^-10 || res > 10^-10, Exit[1]];
Print[ExportString[<|"max_error_m_s" -> err, "discrete_residual" -> res|>, "RawJSON"]];''',
 r'El error debe ser próximo al redondeo. Este resultado no mide orden de convergencia: la derivada cuarta de una parábola es cero. El taller 7, de difusión, sí permite observar error espacial no nulo.',
 'Comprueba ambos valores de pared y el máximo central. Añade la contribución lineal de una pared móvil. Distingue residuo discreto de error respecto de la solución continua.'),
('Ajuste de una ley de resistencia sintética','MF-P20',
 'Usa mínimos cuadrados con cuatro puntos construidos de una misma ley. La recuperación exacta de sus parámetros es un control algebraico, no evidencia experimental.',
 '''speeds = {1., 2., 4., 5.};
forces = {0.12, 0.30, 0.84, 1.20};
design = Transpose[{speeds, speeds^2}];
coef = LeastSquares[design, forces];
res = Norm[design.coef - forces];
If[Max[Abs[coef - {.09, .03}]] > 10^-10 || res > 10^-10, Exit[1]];
Print[ExportString[<|"a_kg_s" -> coef[[1]], "b_kg_m" -> coef[[2]], "residual_N" -> res|>, "RawJSON"]];''',
 r'$a=0.09\,\mathrm{kg/s}$ y $b=0.03\,\mathrm{kg/m}$. El residuo casi nulo se debe a que los datos sintéticos obedecen exactamente a la ley propuesta.',
 'Añade una perturbación conocida a una fuerza y compara parámetros y residuos. Reserva un punto para prueba. Sin un modelo de incertidumbre no atribuyas significado estadístico a los decimales.'),
('Difusión: convergencia de la tasa modal','MF-P24',
 'Compara la tasa de decaimiento continua del seno con la tasa de una segunda diferencia centrada. Duplica sucesivamente el número de intervalos y estima el orden de error espacial.',
 '''gap = .01; visc = 10^-5; rate = visc Pi^2/gap^2;
sizes = {20, 40, 80};
rates = Table[4 visc Sin[Pi/(2 n)]^2/(gap/n)^2, {n, sizes}];
errors = N[Abs[rates - rate], 16];
ratios = Most[errors]/Rest[errors];
If[Min[ratios] < 3.98 || Max[ratios] > 4.02, Exit[1]];
Print[ExportString[<|"errors_s_inverse" -> errors, "ratios" -> ratios|>, "RawJSON"]];''',
 r'Las razones de errores se aproximan a cuatro, correspondientes a segundo orden espacial. Esta comparación de tasas no introduce un integrador temporal ni mide su error.',
 'Representa el error frente a la holgura de malla en escala logarítmica. Deduce el orden con una expansión de seno. Diferencia convergencia espacial de estabilidad y convergencia temporal.')
]

def write():
    dest=ROOT/'workshops';dest.mkdir(exist_ok=True)
    tex=[r'''\chapter*{Uso de los talleres}\addcontentsline{toc}{chapter}{Uso de los talleres}
Cada taller incluye objetivo, código, resultado de contraste y trabajo propuesto. Los archivos editables están en \texttt{workshops/}; se ejecutan con Wolfram Language. El material de \texttt{companion/} pertenece a las prácticas anteriores del manual. Los scripts terminan con error si falla su comprobación. El informe del repositorio registra su ejecución real, versión y salida.

Todos los cálculos usan los datos hipotéticos del banco. Un cálculo simbólico o numérico que reproduce una ecuación no demuestra por sí solo que esa ecuación describa un experimento.
''']
    for i,(title,ref,goal,code,result,exercise) in enumerate(WORKSHOPS,1):
        filename=f'w{i:02d}.wl';(dest/filename).write_text('(* Original educational workshop. SI unless Quantity is used. *)\nClearAll["Global`*"];\n'+code+'\n')
        tex += [r'\chapter{'+title+'}',r'\objetivos{'+goal+'}',r'\textbf{Modelo de referencia.} '+ref+r'.\par',r'\section{Procedimiento y código}',r'Antes de ejecutar, escribe las unidades esperadas y el control que decidirá si el cálculo coincide con el modelo.',r'\lstinputlisting{../workshops/'+filename+'}',r'\section{Resultado de contraste}',result,r'\section{Trabajo propuesto}',exercise,r'\studiumchaptercheck']
    (ROOT/'content/computational-workshops.tex').write_text('\n\n'.join(tex)+'\n')
    print('7 original workshops rendered')
if __name__=='__main__':write()
