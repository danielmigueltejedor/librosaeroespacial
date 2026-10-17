# Mecánica de Fluidos — Auditoría científica y matemática, fase 2

**Fecha:** 2026-10-16
**Fuente:** `mecanica-fluidos-correcciones-cientificas-fase1.tex` (289 páginas compiladas por el usuario)
**Resultado:** `mecanica-fluidos-correcciones-cientificas-fase2.tex`
**Alcance:** comprobación dirigida de la coherencia de modelos, hipótesis y parámetros seleccionados; **no es una certificación exhaustiva** de todas las derivaciones y ejercicios. La compilación íntegra de fase 2 se realizará cuando concluya la auditoría científica del libro.

## Resumen de cambios

| ID | Capítulo / ubicación en LaTeX de fase 1 | Clasificación | Problema | Corrección |
|---|---|---|---|---|
| F2-01 | C1 y apéndice de soluciones, líneas originales 1073 y 12683 | Ambigüedad física **que altera el resultado** | La velocidad de lanzamiento de la herramienta no especificaba marco de referencia. Si los 1,5 m/s son respecto a la estación, la respuesta del libro es 0,375 m/s; si son respecto al astronauta, sería 0,300 m/s. | El enunciado indica explícitamente «respecto a la estación» y se conserva la respuesta correcta bajo esa hipótesis. Dos lugares corregidos. |
| F2-02 | C9, línea 5654 | Sobregeneralización física | El límite de Betz de 16/27 se enunciaba como un máximo para cualquier turbina en flujo abierto «con independencia de su diseño», sin suficientes precisiones sobre modelo y referencia de potencia. | Se delimita el caso de disco actuador ideal, flujo libre estacionario y el área usada como referencia; se mencionan difusores, confinamiento y operación no estacionaria como modelos distintos. |
| F2-03 | C10, línea 6226 | Hipótesis omitidas | Una única curva de resistencia de esfera frente a Re se declaraba válida para «cualquier fluido, tamaño y velocidad». | Se restringe explícitamente la semejanza a las variables consideradas, sin efectos dominantes de Mach, rugosidad, rarefacción, cavitación, etc. |
| F2-04 | C10, línea 6647 | Interpretación de semejanza | El túnel igualaba Reynolds pero se presentaba Mach 0,24 frente a 0,21 como aproximadamente igual sin cuantificar la discrepancia. | Se indica que Mach **no coincide** y que la diferencia relativa es 14,286 %; se distingue la aproximación incompresible de la semejanza dinámica exacta. |
| F2-05 | C15, línea 9728 | Afirmación cuantitativa injustificada | Ley de Stokes descrita como válida con error del orden del 10 % hasta Re≈1. | Se retira la tolerancia garantizada; se incluye la corrección asintótica de Oseen, que añade 18,75 % sobre Stokes cuando se extrapola a Re=1. Se advierte que no es una cota rigurosa del error. |

## Cálculos independientes

### Astronauta y herramienta

Para un sistema aislado inicialmente en reposo, en el marco de la estación:

\[m_a v_a + m_h v_h = 0.\]

Si `v_h = 1.5 m/s` **respecto a la estación**: `|v_a| = 20 × 1.5 / 80 = 0.375 m/s`.

Si `v_h - v_a = 1.5 m/s` **respecto al astronauta**: `|v_a| = 20 × 1.5 / (80 + 20) = 0.300 m/s`.

Los valores distintos verifican que la precisión del enunciado es importante para un estudiante.

### Betz

`C_P(a) = 4 a (1-a)^2`, `a=1/3`: `C_P=16/27`. Se conserva la derivación original. El cambio afecta al **alcance** de la afirmación.

### Túnel

Con velocidad del sonido de 340 m/s: `Ma_m = 80/340 ≈ 0.235294`; `Ma_p = 70/340 ≈ 0.205882`; diferencia relativa al prototipo: `(80-70)/70 = 14.285714 %`.

La presión del túnel no iguala Mach al conservar la temperatura: modifica la densidad y por tanto Re, pero aproximadamente no la velocidad local del sonido de un gas ideal a esa T.

### Esfera a Reynolds bajo

La solución de Stokes predice `C_D=24/Re`; la primera corrección de Oseen predice `C_D ≈ (24/Re)(1+3 Re/16)`. A `Re=1`, la adición de primer orden vale `18.75 %` de la predicción Stokes. **No implica conocer el error real exacto a Re=1 ni garantiza que la aproximación truncada siga siendo precisa allí**.

## Integridad y pruebas realizadas

- Se verificaron los recuentos y ubicaciones exactos de los cinco cambios: **6 pasajes** en total.
- Original y fase 2 conservan **158 entornos `equation`**, sus etiquetas, capítulos, secciones, figuras TikZ y estructuras de ejercicios.
- Se conservaron los datos, las soluciones numéricas y el texto «Borrador».
- Las comprobaciones algebraicas y numéricas descritas se reprodujeron con SymPy y Python.
- Los seis fragmentos modificados se compilaron en un **documento de prueba aislado con pdfLaTeX (2 pasadas, sin errores)**.
- **No se ha compilado el libro completo de fase 2**; faltan revisar los demás problemas y disponer de todos los recursos gráficos originales en el entorno de evaluación.

## Referencias técnicas independientes

- *Stokes Flow*, Springer (ecuación para coeficiente de Oseen, `C_D=24/Re (1+3 Re/16)`): https://doi.org/10.1007/978-3-031-04683-4_5
- Dabiri, J. O. (2020), «Theoretical framework to surpass the Betz limit using unsteady fluid mechanics», *Physical Review Fluids*, 5, 022501: https://doi.org/10.1103/PhysRevFluids.5.022501
- Bontempo y Manna (2020), «On the potential of the ideal diffuser augmented wind turbine», *Energy Conversion and Management*: https://doi.org/10.1016/j.enconman.2020.112794

Estas fuentes se utilizan exclusivamente para los puntos concretos citados; no se asignan etiquetas `VERIFIED` al resto del libro ni se modifican registros de Studium.

## Pendientes para declarar terminado el libro

1. Revisar sistemáticamente las derivaciones numeradas del resto de los 16 capítulos, incluyendo hipótesis y límites de validez.
2. Revisar las soluciones del apéndice: enunciados, datos, unidades, respuestas, valores redondeados y explicaciones.
3. Revisar las siete prácticas de Mathematica: ecuaciones, discretización, condiciones de contorno y resultados numéricos.
4. Contrastar en bibliografía académica los modelos y afirmaciones pendientes.
5. Compilar finalmente la edición revisada en el proyecto original, revisar PDF y retirar «Borrador» **solo tras completar la auditoría**.
