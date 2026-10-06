# Libros

Cada libro vive en una carpeta estable bajo `books/<slug>/`.

## Convención

- La carpeta representa el libro, no una edición concreta.
- `main` contiene el estado de trabajo más reciente.
- Las ediciones cerradas se conservan como tags/releases o snapshots explícitos.
- No se crean carpetas como `v2`, `v3` o `final-final`.
- La edición visible se define en los metadatos LaTeX del propio libro.

## Catálogo actual

| Slug | Título | Edición |
| --- | --- | --- |
| `estructuras-aeroespaciales` | Estructuras Aeroespaciales — Volumen I | Tercera edición |

Para crear un libro nuevo, parte de `../shared/templates/main.tex` y aplica `../shared/STYLE_GUIDE.md`.
