# Incidencias de Studium separadas del manuscrito

Commit inspeccionado: `675274202360f717f3b835444e26d0f95d2a3c33`.
No se ha modificado el código del framework ni su repositorio principal.

## MATH-001: falso diagnóstico de contradicción por formas de una matriz simbólica

El informe nativo marca como `contradicted` la relación de cinemática local de
`PAR-0101`, capítulo 3. A la izquierda hay una columna de tres derivadas de
posición; a la derecha, una matriz diagonal 3×3, la transformación Cnb y el vector
de velocidad cuerpo.

La expresión física declara Cnb de 3×3 y velocidad de 3×1. Sin embargo, el lector
de LaTeX interpreta los dos símbolos como escalares al multiplicarlos por la
matriz explícita. Por ello obtiene formas `(3,1)` y `(3,3)` y devuelve
`Outcome(kind='contradiction', detail='the shapes differ')`.

La reproducción exacta, las expresiones interpretadas y las formas se conservan
en `framework-math-issue.json`. La línea de diagnóstico está en
`authoring/latex_calculus.py`, `check_relation`: se trata como contradicción una
diferencia de formas aun cuando la forma de los símbolos no está establecida.

Resultado esperado: representación no comprobable o pendiente cuando no se
conocen los tipos matriciales, en lugar de afirmar una contradicción física.
La relación correcta se conserva en el manuscrito. No se fuerza su aceptación,
no se silencia el informe nativo y no se presenta una auditoría nativa limpia.

## Adaptación de entrada editorial

El primer borrador nativo no compiló porque los enunciados contenían macros
propias de la maquetación editorial, como `SIu` y `vect`. Se normalizaron las
entradas al formato estándar antes de registrarlas de nuevo y se volvieron a
vincular sus cálculos. No se atribuye este fallo de integración a la física del
libro ni a un defecto matemático del framework.

Los registros antiguos se conservan en el historial con su condición de
obsolescencia; los controles vigentes se identifican en
`native-computations.json`. Las fuentes siguen pendientes y no se utiliza la
reproducción aritmética para promoverlas de autoridad.
