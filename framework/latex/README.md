# AeroBooks LaTeX layer

Esta carpeta contiene la identidad visual y estructural común de la colección.

## Archivos

- `aerobook.cls`: clase base. Extiende `book`.
- `aerobook-core.sty`: tipografía, geometría, cajas, referencias, bibliografía, índices, paleta y utilidades.
- `aerobook-cover.tex`: composición de portada y página de edición.

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
