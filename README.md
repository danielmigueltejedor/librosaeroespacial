# Libros Aeroespacial

Repositorio monorepo para los libros universitarios en LaTeX de **Daniel Miguel Tejedor** orientados al Grado en Ingeniería Aeroespacial.

La idea es mantener aquí una base editorial común para que todos los libros compartan portada, tipografía, colores, cajas didácticas, índices, referencias y criterios de edición, mientras cada asignatura conserva su contenido y bibliografía propios.

## Estructura

```text
books/
  estructuras-aeroespaciales/
    main.tex
    references.bib
    chapters/
    appendices/
    style/

shared/
  README.md
  STYLE_GUIDE.md
  templates/
```

## Libros

| Libro | Estado | Edición |
| --- | --- | --- |
| Estructuras Aeroespaciales — Volumen I | En desarrollo | Tercera edición |

## Convención de ediciones

Los libros usan nomenclatura editorial, no versiones de software:

- Primera edición
- Segunda edición
- Tercera edición
- etc.

La rama `main` contiene siempre el estado de trabajo más reciente. Las ediciones publicadas se conservarán mediante Git tags/releases con nombres inequívocos, por ejemplo:

```text
estructuras-aeroespaciales-ed3
aerodinamica-ed4
```

## Estándar editorial

Los elementos que deberían ser comunes a todos los libros se documentan en `shared/`:

- jerarquía de portada;
- paleta y tipografía;
- cajas de definición, intuición, examen y advertencia;
- índices de figuras y cuadros;
- bibliografía con BibLaTeX/Biber;
- índice analítico;
- criterio de numeración de figuras, cuadros y ecuaciones;
- metadatos PDF;
- convenciones de nombres y estructura de carpetas.

Cada libro puede añadir figuras y macros específicas sin romper ese estándar.

## Compilación

Cada libro incluye sus propias instrucciones. Para Estructuras Aeroespaciales:

```bash
cd books/estructuras-aeroespaciales
latexmk -pdf -interaction=nonstopmode main.tex
```

El proyecto usa BibLaTeX/Biber e índice analítico, por lo que `latexmk` es la forma recomendada de compilarlo.

## Filosofía del repositorio

Este repositorio contiene **código fuente LaTeX** y recursos editoriales. Los archivos generados por compilación no se versionan de forma ordinaria; los PDF finales se publicarán como artefactos o releases cuando corresponda.
