# Estructuras Aeroespaciales — Volumen I

**Autor:** Daniel Miguel Tejedor  
**Edición actual:** Tercera edición — octubre de 2026

## Alcance

Volumen dedicado a los conceptos básicos y al modelo monodimensional de Teoría de Estructuras:

- fundamentos de estructuras aeronáuticas;
- sólidos rígidos y deformables;
- tensión y deformación;
- leyes de comportamiento;
- cargas y vinculaciones;
- esfuerzos internos;
- equilibrio estático y elástico;
- leyes de esfuerzos;
- problemas resueltos y preparación de examen.

## Compilación

Desde esta carpeta:

```bash
latexmk -pdf -interaction=nonstopmode main.tex
```

El proyecto utiliza BibLaTeX/Biber e índice analítico. `latexmk` ejecuta las etapas necesarias.

## Ediciones

La fuente de esta carpeta representa siempre la edición en desarrollo más reciente. Las ediciones publicadas se conservarán con tags/releases del repositorio, no duplicando carpetas completas.

Convención sugerida:

```text
estructuras-aeroespaciales-ed3
estructuras-aeroespaciales-ed4
...
```

## Estilo editorial

Esta edición es la referencia inicial para el estándar visual documentado en `../../shared/STYLE_GUIDE.md`.

En futuras revisiones se irá trasladando al estándar compartido cualquier elemento reutilizable de portada, cajas, tipografía y composición.
