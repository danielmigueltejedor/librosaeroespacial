# Mecánica de Fluidos — fase 3, correcciones científicas y edición revisada

**Base:** `mecanica-fluidos-correcciones-cientificas-fase2.tex`, 2026-10-16.
**Salidas:** `mecanica-fluidos-correcciones-cientificas-fase3.tex` (con la marca de borrador) y `mecanica-fluidos-edicion-revisada.tex` (sin ella).
**Alcance:** revisión dirigida y reparaciones comprobables en capítulo 12 y práctica 7. **No supone un arbitraje científico completo de las 289 páginas del PDF anterior.**

## Hallazgos y acciones

| ID | Localización en fase 2 | Tipo | Corrección |
|---|---|---|---|
| F3-01a | C12, ~7696 | Error de alcance físico | El tubo de Pitot no queda inutilizado universalmente a Mach supersónico; la conversión de presión requiere incluir la compresión y el choque normal precedente. Se aclara que la fórmula incompresible no sirve directamente. |
| F3-01b | C12, ~7721 | Precisión en definición | La toma frontal supersónica mide presión de estancamiento aguas abajo del choque, no directamente la presión total de la corriente libre. |
| F3-02 | C12, ~7733 | Inconsistencia interna | La síntesis de Bernoulli decía cuatro hipótesis frente a cinco en el texto: añade la ausencia de trabajo de máquinas y la excepción de campo irrotacional. |
| F3-03 | Práctica 7, ~11949–11959 | Defecto matemático-pedagógico | El problema resuelto consistía únicamente en `(0.010)**2/1.0e-6`; ahora incluye enunciado físico, ecuación de difusión, escala temporal y cálculo con unidades de **100 s**. |
| F3-04 | Apéndice de cálculos, ~18886 | Notación matemática | Se reemplaza una operación Python sin unidades por \(t_\nu=h^2/\nu=100\,\mathrm{s}\). |
| F3-05a | Práctica 7, ~11835 | Atribución no justificada | El cruce al 99 % de esfuerzo calculado con serie es \(53{,}6832\,\mathrm{s}\), frente a \(55{,}1\,\mathrm{s}\) comunicado para el cálculo numérico. La diferencia exige convergencia; no es prueba de la corrección de NDSolve. |
| F3-05b | Apéndice de soluciones, ~18438 | Explicación cuantitativa | Para el tiempo comunicado 55,1 s, la serie predice \(\tau/\tau_{est}\approx0{,}991305\), diferencia de **0,1305 puntos porcentuales** sobre el umbral. Se evita atribuir categóricamente ese error a un único mecanismo. |
| F3-06 | Práctica 7, ~11849 | Inferencia numérica | Una malla espacial convergente no prueba por sí sola que el error residual provenga de tolerancias temporales o discontinuidades. Se solicita estudio separado de convergencia. |

## Cálculos reproducidos

- \(t_\nu=0{,}010^2/10^{-6}=100\,\mathrm{s}\).
- \(t_{99}=\frac{0{,}010^2}{\pi^2 10^{-6}}\ln(200)=53{,}6831786891\,\mathrm{s}\).
- Serie en \(t=55{,}1\,\mathrm{s}\): \(1+2\sum_{n\ge1}(-1)^n\exp[-n^2\pi^2 \nu t/h^2]\approx0{,}9913049808\). Desviación respecto a 0,99: 0,0013049808 (0,130498 puntos porcentuales).
- Comprobación matemática independiente del ejemplo de la función de corriente \(\psi=K(x^2y+2xy^2)\): las aceleraciones son compatibles con su cinemática, pero \(\nabla\times(\mu\nabla^2\mathbf u-\rho\mathbf a)\) tiene componente \(4\rho K^2(x^2+3xy-y^2)\), no nula. Esta incompatibilidad ya se abordó en fase 1; se ha comprobado que permanece la aclaración.
- Se evaluaron numéricamente **63 expresiones aritméticas interpretables del apéndice**, comparando el valor declarado con el recalculado en SymPy; **0** tuvieron error relativo superior a 0,5 %. Este control **no** verifica su modelo físico, unidades ni la totalidad de las derivaciones. Una expresión no fue interpretable automáticamente.

## Integridad y validación

| Control | Resultado |
|---|---|
| Ecuaciones numeradas (`equation`) | 158 antes y después |
| Etiquetas LaTeX (`\\label`) | 230 antes y después |
| Inclusiones gráficas | 22 antes y después |
| Sustituciones dirigidas | 8, con coincidencia exacta única |
| Compilación de fragmentos científicos nuevos con pdfLaTeX | Correcta (2 páginas de prueba) |
| Marcas `Borrador` en el archivo de auditoría | 2 (conservadas) |
| Marcas `Borrador` en la edición revisada | 0 |
| Compilación íntegra de la edición revisada | Pendiente en el proyecto original, donde están las imágenes |

## Limitaciones explícitas

1. El apéndice conserva operaciones auxiliares en sintaxis textual Python; la auditoría corrige el caso de la práctica 7, pero **no** convierte automáticamente todas esas expresiones a LaTeX (podría cambiar su semántica o maquetación).
2. La edición sigue mostrando la advertencia bibliográfica de **157 fuentes PENDING** registrada en su propio apéndice. Eliminar «Borrador» es **una decisión editorial**, no una recategorización de esas fuentes.
3. No se ejecutó Mathematica 15 ni se reprodujeron directamente sus resultados de `NDSolve`. Las cifras comunicadas por el texto se presentan como tales y se han limitado las conclusiones que se pueden extraer de ellas.
4. Las 158 ecuaciones no han sido contrastadas todas, una a una, con demostración y fuente externa. No afirmamos un texto científicamente libre de errores; no hay prueba automática universal para ello.
5. No se dispone aquí del árbol `figures/` ni de la portada original. La compilación íntegra debe ejecutarse en el Mac, usando el script incluido y los recursos del proyecto original.

## Compilar sin «Borrador» en macOS

Copiar `mecanica-fluidos-edicion-revisada.tex` y `compilar_mecanica_fluidos_edicion_revisada.sh` a un lugar accesible y ejecutar:

```bash
BOOK="$HOME/Developer/studium-eval/ule-fluid-mechanics-book-02-r1"
LATEX="$BOOK/workspace/mecanica-fluidos-ule/latex"
# Copiar el .tex al LATEX si aún no está allí.
BOOK="$BOOK" bash compilar_mecanica_fluidos_edicion_revisada.sh
```

El PDF aparecerá en `~/Developer/studium-eval/ule-fluid-mechanics-book-02-r1/output/mecanica-fluidos-edicion-revisada.pdf` si todas las comprobaciones pasan. El LaTeX de fase 2 y los PDFs anteriores quedan intactos.
