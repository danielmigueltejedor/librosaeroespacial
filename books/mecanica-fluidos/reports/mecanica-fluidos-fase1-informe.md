# Mecánica de Fluidos — Correcciones científicas, fase 1

**Fuente:** `draft(2).tex` proporcionado por el usuario.
**Resultado:** `mecanica-fluidos-correcciones-cientificas-fase1.tex`.
**Alcance:** rectificación de hallazgos identificados en la revisión preliminar; **no es una auditoría científica exhaustiva de las 16 unidades y los apéndices**.

## Resumen ejecutivo

Se introdujeron 20 cambios locales en líneas originales del LaTeX. No se alteraron las fórmulas numéricas, datos de los ejercicios, etiquetas LaTeX, diagramas ni orden del documento. Se ha mantenido el ejercicio del campo de corriente porque sus resultados cinemáticos son correctos, pero su interpretación física se ha corregido en capítulos 12 y 14 y en la práctica 3 de Mathematica.

## Hallazgos y tratamiento

| Ámbito | Líneas de origen | Modificación | Naturaleza |
|---|---|---|---|
| Resistencia aerodinámica | 4197, 4415 | La viscosidad explica fricción y condiciona la resistencia de presión por separación, pero no explica universalmente resistencia inducida o de onda. Se actualiza la autoficha. | Generalización física |
| Entrada en pérdida y Reynolds | 4367 | La variación de `c_l,max` y del ángulo de pérdida con Reynolds depende de perfil, transición, rugosidad, Mach y rango de operación. | Generalización física |
| Función de corriente / fuerza neta | 7698, 7700, 7710, 7716, 8004 | Se distingue el cálculo cinemático de `rho*a` de la existencia de una solución física de Navier–Stokes. Se conserva `a=(42,84) m/s²` y `rho*a=(42000,84000) N/m³`. | Incompatibilidad de hipótesis |
| Fuerza neta y presión, capítulo 14 | 8925, 8927 | Se elimina la afirmación incorrecta de que la presión compensa casi toda la inercia del campo prescrito; se incluye la condición de integrabilidad del gradiente de presión. | **Hallazgo crítico** |
| Flujo no viscoso vs irrotacional | 9716 | Flujo de viscosidad despreciable no implica vorticidad nula en general. | Generalización física |
| Espesor de capa límite | 9720, 10018 | Se diferencia la escala `sqrt(nu*L/U)` del espesor `delta_99` de Blasius; se reformula el ejercicio de práctica. | Interpretación de fórmula |
| Stokes no estacionario | 9728, 9730, 9749, 9754 | Se explicita la condición `L²/(nu*T) << 1` para despreciar la inercia temporal; se matiza reversibilidad. | Falta de hipótesis |
| Boussinesq | 10041 | Se compara densidad exacta isobárica frente a linealización de Boussinesq; se identifica una variación de 9,375 % y una discrepancia de 10,34 % en `g'`. | Alcance de aproximación |
| Práctica Mathematica 3 | 11018, 11089 | Se separa validación de derivadas y operaciones de validación dinámica del campo. | Coherencia entre capítulos |

### Comprobación simbólica de capítulos 12 y 14

Con `psi = K(x²y + 2xy²)` y el convenio `(u,v)=(psi_y,-psi_x)`, SymPy reproduce:

- `u = K(x² + 4xy)`; `v = -K(2xy + 2y²)`.
- `div(u,v)=0`.
- `a = 2K²(x²+2xy+4y²)(x,y)`.
- `laplace(u,v) = (2K,-4K)`.

Si se supone un flujo estacionario, incompresible y newtoniano con densidad/viscosidad constantes, sin fuerzas de volumen, Navier–Stokes exigiría

`grad(p) = mu*laplace(u) - rho*a`.

El rotacional perpendicular del lado derecho, que debe ser cero para un gradiente escalar, es:

`curl_z[mu*laplace(u)-rho*a] = 4*rho*K²*(x²+3xy-y²)`.

Con `(x,y,K,rho)=(1,2,1,1000)` vale **12 000 N/m⁴**, no cero. Por tanto, el campo **no es una solución dinámica de ese modelo** en un entorno del punto, aunque sus cálculos cinemáticos y la fuerza *requerida* `rho*a` sí son correctos.

### Comprobaciones numéricas de capítulos 15 y 16

- Capa límite: `sqrt(1.4607e-5*2/70)=0.0006460208 m = 0.646 mm` (escala; **no** `delta_99`).
- Blasius, hipotético flujo laminar sobre placa plana: `delta_99≈5*escala=3.230 mm`.
- Reynolds de cuerda: `70*2/(1.4607e-5)≈9.584·10^6`.
- Boussinesq, gas ideal isobárico a 290 K + 30 K: `g'_exacta=9.81*30/320=0.9196875 m/s²`.
- Aproximación lineal: `g'_Boussinesq=9.81*30/290=1.0148276 m/s²`.
- Diferencia relativa a la magnitud exacta: `10.3448 %`.

## Validación técnica realizada

1. Validación de todas las 20 coincidencias de texto originales (una y solo una), con cancelación de la operación cuando cambia el archivo base.
2. Conservación de los recuentos de identificadores de ecuación de las zonas modificadas.
3. Comprobaciones algebraicas y numéricas independientes con **SymPy y Python**, sin depender de los verificadores de Studium.
4. Compilación **de humo** en `pdflatex` de todas las líneas modificadas en un documento autónomo: **exit 0**, ningún error fatal ni desbordamiento horizontal. Las advertencias sobre referencias cruzadas de este documento de prueba son esperables porque no incluye las etiquetas del libro.
5. **No se ha compilado el libro completo en este entorno**: el LaTeX original hace referencia a recursos `../figures/FIG-...` que no estaban incluidos en el archivo adjunto. Para compilar el libro en el proyecto original deben conservarse los directorios de figuras.

## Pendiente

- Auditoría exhaustiva del resto de derivaciones, ejercicios y prácticas (no cubierta por esta fase).
- Verificación externa de hipótesis y convenciones de signos en fenómenos de transporte y dinámica.
- Compilación integral y revisión visual del PDF con las figuras y tipografías del proyecto original.
- Sincronización de correcciones con las fuentes de generación de libros, para que no desaparezcan al regenerar un capítulo: **esto requiere trabajo posterior en el generador / una nueva PR; el LaTeX corregido no altera Studium**.

## Fuentes de referencia para el contraste físico

- NASA Glenn Research Center, «What is Drag?»: https://www1.grc.nasa.gov/beginners-guide-to-aeronautics/what-is-drag/
- NASA Technical Reports Server, relación de Blasius `delta ≈ 5 sqrt(nu*x/U)`: https://ntrs.nasa.gov/api/citations/19820014335/downloads/19820014335.pdf

Estas fuentes sirven como contraste de conceptos específicos; **no se han utilizado para declarar verificadas automáticamente todas las demás afirmaciones del libro**.
