# Tecnología Aeroespacial

Proyecto LaTeX de la colección Studium, importado el 17 de octubre de 2026. Incluye manual, problemas resueltos y simulacros. Comparte la maquetación común de la colección y conserva sus informes; la importación no equivale a una revisión académica ni a una migración al contrato AeroBooks.

## Editar y compilar

Desde la raíz del repositorio:

```sh
python3 scripts/build-studium-books.py tecnologia-aeroespacial
```

Los PDF se crean en `dist/studium/tecnologia-aeroespacial/`. Para comprobar los archivos antes de compilar:

```sh
python3 scripts/build-studium-books.py tecnologia-aeroespacial --check
```

Entradas de los tres volúmenes:

- `latex/manual.tex`: Manual.
- `latex/problemas.tex`: Problemas resueltos.
- `latex/simulacros.tex`: Simulacros.

La teoría editable está en `content/`; `content-layout/` es la composición usada por el manual cuando existe. Si cambias un capítulo de Tecnología Aeroespacial, actualiza también su copia de composición o conserva su recuadro editorial. Las figuras utilizadas están en `figures/`, con sus originales SVG. La bibliografía figura en los propios archivos LaTeX; los metadatos públicos están en `bibliography/`.

No hacen falta los originales de apuntes ni los exámenes privados para editar o compilar. Se han excluido esos materiales y los registros de extractos. Los informes conservan el alcance de las comprobaciones y los pendientes existentes. `studium-import.json` registra procedencia y archivos de entrada.

Los comandos `aerobooks check/build` pertenecen a los libros con `book.toml`; este proyecto usa el compilador de importaciones anterior. Una migración académica a AeroBooks requiere trasladar explícitamente fuentes, claims y revisiones, sin asignar aprobaciones automáticamente.

## Maquetación común de la colección

Los once volúmenes comparten `shared/latex/studium-editorial.tex` y `studium-cover.tex`, desde la raíz del repositorio. Las opciones específicas están en `latex/editorial-config.tex`. Consulta `shared/EDITORIAL_STANDARD.md` para el orden común de páginas, apartados y recuadros.
