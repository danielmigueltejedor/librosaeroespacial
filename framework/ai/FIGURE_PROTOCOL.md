# Figure Protocol

Una figura técnica forma parte del argumento académico.

## Requisitos

- debe explicar algo;
- proporciones coherentes;
- ejes, signos y unidades cuando sean necesarios;
- flechas y grosores consistentes;
- caption informativa;
- label estable;
- referencia en el texto;
- ausencia de información engañosa.

## Ficha de revisión

Toda figura científica que un capítulo 0.3 da por lista tiene una entrada en `figures/ledger.jsonl`. La revisión deja en `pass` el sentido, el signo, los vectores, los ejes, las unidades, las condiciones de contorno, la escala conceptual y la coherencia con el texto. `status: fail` es un blocker.

## Diagramas físicos

Comprobar:
- orientación;
- sentido de fuerzas/momentos;
- sistema de referencia;
- apoyos;
- magnitudes;
- escala cuando se afirme que es a escala.

Si no es a escala y eso puede inducir a error, indicarlo.

## Gráficas

Comprobar:
- variable de cada eje;
- unidades;
- dominio;
- ley representada;
- puntos singulares;
- tendencia;
- coherencia con la ecuación.

## TikZ

Preferir macros del framework frente a estilos improvisados. Un libro no debe introducir nuevos colores/grosores si existe ya un equivalente.

## Revisión

El revisor de figuras debe comparar la figura con la teoría, no solo con criterios estéticos.
