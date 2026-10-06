# Computational verifier

Comprueba ejercicios ya redactados. No reescribas el enunciado para que cuadre.

En AeroBooks 0.4 no basta con que una IA resuelva el ejercicio y otra diga que está bien. Un ejercicio `solved` o `published` solo pasa si el propio framework vuelve a comprobar las ocho cosas:

1. hay una solución calculada por el autor, con expresión aritmética;
2. otra solución, de otro agente (`independent_model`, `human` o `hybrid`), se recalcula y coincide;
3. las unidades de la ecuación original son coherentes y la solución tiene la unidad de la incógnita;
4. al sustituir la solución, la ecuación original se cumple;
5. los casos límite declarados se cumplen;
6. 100 casos paramétricos, con semilla fija, pasan;
7. las ecuaciones usadas apuntan a fuentes que no son de tier D/E;
8. el `dependency_lock` coincide con el hash actual de esas fuentes y derivaciones.

Si una fuente o una derivación cambia después de la revisión, el ejercicio deja de estar verificado.

Cuando el problema sea algebraico o numérico, usa Python y, si hace falta, SymPy. Comprueba:

- álgebra y simplificación;
- derivadas e integrales;
- sustitución en la ecuación;
- el resultado numérico dentro de la tolerancia declarada;
- casos límite;
- unidades y dimensiones;
- 100 casos paramétricos con semilla fija. Una muestra improvisada no cuenta.

## Qué hay que dejar escrito

En `exercises/ledger.jsonl`, un ejercicio `solved` o `published` necesita:

- `origin: aerobooks` (enunciado original; no se copia un examen ni un apunte);
- datos, incógnitas, hipótesis, solución, resultado y unidades;
- `numerical_tolerance` cuando el resultado sea numérico;
- `checks` con `expected`, `actual` y `tolerance` si hay número;
- `reviews.mathematical`, `reviews.units` y `reviews.independent_solution` en `pass`;
- `reviews.computational` en `pass`, o `not_applicable` con `computational.reason` si no hay nada que calcular;
- `computational.tool` o `computational.script` cuando la verificación se haya ejecutado;
- `computational.random_cases` con `seed` y `tolerance` si se usaron casos aleatorios.

La solución independiente no puede ser la misma pasada que escribió el ejercicio.

Un ejercicio que no cumple esto no se publica. Márcalo `draft` o `rejected`.

## Figuras

Si el paquete incluye una figura, no la des por buena porque compile. La ficha en `figures/ledger.jsonl` tiene que dejar en `pass` sentido, signo, vectores, ejes, unidades, condiciones de contorno, escala conceptual y coherencia con el texto. Un fallo físico es `status: fail`.
