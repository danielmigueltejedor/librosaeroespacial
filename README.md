# Libros Aeroespacial

Repositorio monorepo para los libros universitarios en LaTeX de **Daniel Miguel Tejedor** orientados al Grado en Ingeniería Aeroespacial.

La idea es mantener aquí una base editorial común para que todos los libros compartan portada, tipografía, colores, cajas didácticas, índices, referencias y criterios de edición, mientras cada asignatura conserva su contenido y bibliografía propios.

## Estructura

```text
books/
  README.md
  estructuras-aeroespaciales/
    main.tex
    references.bib
    CHANGELOG.md
    chapters/
    appendices/
    style/

shared/
  README.md
  STYLE_GUIDE.md
  templates/
    main.tex
    cover.tex

scripts/
  build-book.sh
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

## Estándar editorial común

Los elementos compartidos se documentan en `shared/`.

La portada de la colección está centralizada en:

```text
shared/templates/cover.tex
```

Cada libro define únicamente sus metadatos y una figura técnica propia mediante `\BookCoverGraphic`. De esta forma se puede cambiar la composición general de las portadas de toda la colección desde un único archivo sin perder la identidad técnica de cada asignatura.

El estándar común fija además:

- jerarquía de portada;
- paleta y tipografía;
- cajas de definición, intuición, examen y advertencia;
- índices de figuras y cuadros;
- bibliografía con BibLaTeX/Biber;
- índice analítico;
- criterio de numeración de figuras, cuadros y ecuaciones;
- metadatos PDF;
- convenciones de nombres y estructura de carpetas.

## Compilación

Para compilar el libro por defecto:

```bash
make book
```

Para indicar otro libro:

```bash
make book BOOK=slug-del-libro
```

O directamente:

```bash
bash scripts/build-book.sh estructuras-aeroespaciales
```

El proyecto usa BibLaTeX/Biber e índice analítico, por lo que `latexmk` es la forma recomendada de compilarlo.

## Filosofía del repositorio

Este repositorio contiene **código fuente LaTeX** y recursos editoriales. Los archivos generados por compilación no se versionan de forma ordinaria; los PDF finales se publicarán como artefactos o releases cuando corresponda.
