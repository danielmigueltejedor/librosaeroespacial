# Exercise Protocol

Los problemas son contenido académico, no decoración.

## AeroBooks 0.4

Publicar un ejercicio no es «la IA lo resolvió y otro agente dijo que está bien». Hace falta, y el gate lo ejecuta de nuevo:

- la solución del autor;
- una solución independiente recalculada;
- unidades coherentes;
- cumplimiento de la ecuación original;
- casos límite;
- 100 casos paramétricos con semilla;
- fuentes que respaldan esas ecuaciones;
- un candado de dependencias que falla si la fuente o la derivación cambian después.

El contrato está en `verification` dentro de `exercises/ledger.jsonl`. Lo comprueba `framework/aerobooks/exercise_check.py`.

## Ledger de soluciones

Un ejercicio que se publica en el contrato 0.3 se registra en `exercises/ledger.jsonl` con enunciado original (`origin: aerobooks`), datos, incógnitas, hipótesis, solución, resultado, unidades, tolerancia si el resultado es numérico, comprobaciones y revisor. Tiene que pasar revisión matemática, de unidades, una solución independiente y la verificación computacional de `COMPUTATIONAL_VERIFIER.md` cuando haya álgebra o números. Si no pasa, se queda en `draft` y no entra en la release.

## Origen

Cada ejercicio debe ser uno de:
- `source-derived`: inspirado en una fuente registrada;
- `exam-pattern`: reproduce el tipo de razonamiento de un examen, no su texto;
- `original`: creado pedagógicamente.

No copiar de forma sustitutiva enunciados o soluciones protegidas.

## Diseño

Un ejercicio debe tener datos suficientes y no ambiguos. Si requiere hipótesis, deben declararse.

## Solución de calidad

Cuando proceda:
1. datos;
2. qué se pide;
3. modelo;
4. hipótesis;
5. estrategia;
6. desarrollo;
7. resultado;
8. unidades;
9. comprobación independiente;
10. interpretación;
11. errores frecuentes;
12. método rápido de examen.

## Validación numérica

La solución debe recalcularse desde cero. Para problemas complejos puede usarse una segunda vía:
- equilibrio global frente a equilibrio local;
- derivada/integral inversa;
- cálculo simbólico frente a numérico;
- balance dimensional;
- caso límite.

## Datos inventados

Pueden crearse datos pedagógicos, pero deben producir:
- magnitudes físicas razonables;
- números manejables cuando el objetivo no sea aritmético;
- ninguna falsa atribución a una fuente.

## Banco de problemas

Los identificadores deben ser estables para poder rastrear correcciones entre ediciones.
