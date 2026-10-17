# Mecánica de Fluidos — Auditoría científica y matemática, fase 4

**Fecha:** 16 de octubre de 2026.
**Base:** `mecanica-fluidos-edicion-revisada.tex` (archivo de la fase 3, sin la marca «Borrador»).
**Salida:** `mecanica-fluidos-edicion-revisada-fase4.tex`.
**Alcance:** revisión dirigida de fórmulas, singularidades, definiciones físicas y consistencia entre capítulos y apéndices. **No es una comprobación exhaustiva de todas las ecuaciones, prácticas ni resultados numéricos.**

## Correcciones aplicadas

| ID | Localización original, línea aproximada | Tipo | Modificación |
|---|---|---|---|
| F4-01 | Capítulo 7, 4357 | **Afirmación cuantitativa incorrectamente garantizada** | Eliminar la tolerancia del 10 % para todo `Re < 1`. Aclarar el límite asintótico y el término de Oseen (18,75 % de la predicción de Stokes si se extrapola a `Re=1`). |
| F4-02 | Capítulo 7, 4373 | **Inconsistencia de parámetros** | Distinguir eficiencia de envergadura `e_i` del factor empírico de Oswald `e_O` y aportar su relación para una polar de resistencia de perfil cuadrática. |
| F4-03 | Capítulo 7, 4385 | **Hipótesis no explicitada** | Separar velocidad de pérdida verdadera TAS y equivalente EAS; indicar que un cambio de `C_L,max` por Mach/Re puede alterar la conclusión. |
| F4-04 | Capítulo 9, 5640 | **Singularidad matemática** | Para `v_e = v_0` la definición de rendimiento es `0/0`, no 1. El rendimiento **tiende** a 1 al aproximarse `v_e` a `v_0` desde arriba; el empuje tiende a cero. |
| F4-05 | Capítulo 10, 6230 | **Generalización física** | Reynolds por sí solo no decide la transición en cualquier sistema; incluir perturbaciones, geometría y estelas/capas de mezcla. |
| F4-06 | Práctica 6, 11725 | **Inferencia estadística injustificada** | La diferencia del ~0,083 % entre interpolación y correlación cuantifica una discrepancia metodológica, no una incertidumbre experimental estimada. |
| F4-07 | Capítulo 16, 10239 | **Generalización física** | Evitar que la rotación terrestre sea automáticamente irrelevante para **cualquier** flujo de laboratorio o aeronáutico; indicar que depende de las escalas y la duración. |
| F4-08 | Capítulo 9, 5668 | **Coherencia pedagógica** | Actualizar autoficha de propulsión: límite y singularidad 0/0. |
| F4-09 | Capítulo 7, 4371 | **Notación de una ecuación numerada** | Cambiar `e` a `e_i` en resistencia puramente inducida. |
| F4-10 | Capítulo 7, 4375 | **Notación de una ecuación numerada** | Cambiar `e` a `e_O` en la polar ajustada de resistencia total. |
| F4-11 | Capítulo 7 y hoja de fórmulas, 4593 y 12546 | **Coherencia entre teoría y apéndice** | Cambiar `e` a `e_O` en ambas expresiones de la polar total. |

**Total:** 11 correcciones declaradas, 12 sustituciones textuales verificadas (la última aparece en dos posiciones).

## Comprobaciones matemáticas independientes

Con SymPy, script `verificar_fase4_fluidos.py`:

1. **Stokes--Oseen:** `((24/Re)*(1+3Re/16)-(24/Re))/(24/Re)=3Re/16`; en Re=1 el incremento asintótico respecto a Stokes es `3/16=18,75 %`. **No equivale a conocer el error exacto de Stokes** a Re=1.
2. **Rendimiento propulsivo:** `eta = m_dot*(v_e-v_0)*v_0 / [m_dot*(v_e²-v_0²)/2]` se simplifica a `2v_0/(v_e+v_0)` **solo si** `v_e != v_0`. Para `v_e = v_0`, numerador y denominador originales son cero; el límite lateral es uno.
3. **Eficiencias inducida y Oswald:** si `C_D = c_d0 + c_d2*C_L² + C_L²/(pi*AR*e_i)` y `C_D = C_D0+C_L²/(pi*AR*e_O)`, entonces, con el mismo `C_D0=c_d0`, se cumple `1/e_O=1/e_i+pi*AR*c_d2`.
4. **Velocidad de pérdida:** `TAS=sqrt(2W/(rho*S*C_L,max))`; `EAS=TAS*sqrt(rho/rho0)=sqrt(2W/(rho0*S*C_L,max))` sin dependencia explícita de la densidad local si se fija `C_L,max`.
5. **Dos estimadores:** `(48.34-48.30)/48.34 = 0,0827 %` (no es una incertidumbre estadística).

Todos estos controles pasaron.

## Integridad editorial

| Control | Antes | Después |
|---|---:|---:|
| Entornos `equation` | 158 | 158 |
| Etiquetas `\label` | 230 | 230 |
| Comandos `\includegraphics` | 21 | 21 |
| Comandos `\chapter` | 30 | 30 |
| Referencias `\ref`/`\eqref` | 168 | 168 |
| Marca «Borrador» | 0 | 0 |

- El conjunto **exacto de etiquetas** es idéntico.
- `--check` del script de aplicación no escribe nada; `--apply` por defecto crea una salida nueva y aborta si el destino preexistente no coincide.
- El documento de prueba con los fragmentos afectados **compiló con pdfLaTeX**, pero esa compilación de dos páginas **no demuestra que el libro completo compile sin incidencias**. El documento aislado tiene avisos esperados de referencias a capítulos no incluidos.
- **No se ha recompilado el libro completo** en esta fase; conserva las imágenes en tu directorio original del Mac.

## Referencias técnicas consultadas

- *Stokes Flow*, Springer: https://link.springer.com/chapter/10.1007/978-3-031-04683-4_5
- Definición del factor de Oswald y su interpretación en polar: https://atlasofengineering.com/aerospace-engineering/oswald-efficiency-factor/
- NASA NTRS/NACA TR 837, terminología TAS/EAS: https://ntrs.nasa.gov/citations/19930091914
- NTSB, preguntas sobre velocidad de pérdida indicada y verdadera: https://libraryonline.erau.edu/online-full-text/ntsb/aviation-special-studies/AAS72-08.pdf

## Pendientes antes de afirmar que todo es matemáticamente riguroso

- Reproducir computacionalmente los resultados de las **siete prácticas de Mathematica**: `NDSolve`, condiciones de contorno, tolerancias y convergencia, además de posibles expresiones sintácticamente incorrectas de Wolfram Language. **No se ha ejecutado Mathematica en esta fase.**
- Auditar sistemáticamente todos los problemas del apéndice, no solo los ejemplos numéricos seleccionados.
- Comprobar la validez científica de derivaciones en hipótesis límite y su respaldo bibliográfico.
- Revisar visualmente los gráficos en el PDF del proyecto real; la conservación de `\includegraphics` no demuestra que las imágenes sean científicamente correctas.
- Validar que la documentación bibliográfica pendiente no se confunda con aprobación experta.

**Conclusión:** corregidos los nuevos hallazgos **confirmados o razonadamente delimitados**; el libro está mejor, pero no puede declararse probado científicamente de forma exhaustiva.
