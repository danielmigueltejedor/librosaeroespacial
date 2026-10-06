# AeroBooks LaTeX layer

Esta carpeta contiene la identidad visual y estructural común de la colección.

## Archivos

- `aerobook.cls`: clase base. Extiende `book`.
- `aerobook-core.sty`: tipografía, geometría, cajas, referencias, bibliografía, índices, paleta y utilidades.
- `aerobook-cover.tex`: composición de portada y página de edición.
- `aerobook-diagrams.sty`: estilos y primitivas TikZ comunes para vigas, apoyos, cargas, reacciones y cotas.

## Cómo se resuelve la clase

El comando `aerobooks build` añade `framework/latex//` a `TEXINPUTS`, por lo que un libro puede usar:

```latex
\documentclass{aerobook}
```

sin copiar el framework dentro de cada carpeta.

## Responsabilidad del libro

Cada libro define:
- metadatos mediante `book.toml`;
- figura técnica de portada;
- contenido;
- bibliografía;
- fuentes;
- claims.

No debe duplicar:
- paleta;
- cajas;
- portada;
- estilos de capítulo;
- configuración de BibLaTeX;
- configuración de índices.

## Compatibilidad

La capa común conserva algunos alias de las primeras ediciones para que los libros existentes puedan migrarse sin reescribir todo el contenido de una vez.

## Diagramas técnicos

Para evitar que cada libro dibuje apoyos, cargas o vigas con estilos distintos, usa las primitivas de `aerobook-diagrams.sty` siempre que encajen con la figura.

Ejemplo:

```latex
\begin{tikzpicture}
  \AeroBeam{0}{0}{6}{0}
  \AeroPinSupport{0.5}{0}
  \AeroRollerSupport{5.5}{0}
  \AeroDownLoad{3}{0}{1.5}{$P$}
\end{tikzpicture}
```

## Dependencias TeX en CI

El workflow instala explícitamente `latexmk`, `biber`, `texlive-latex-extra`, `texlive-bibtex-extra`, `texlive-science`, `texlive-lang-spanish` y Latin Modern para que la compilación sea reproducible en GitHub Actions.
