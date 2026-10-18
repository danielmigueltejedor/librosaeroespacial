# Motores Cohete

Proyecto LaTeX de la colección Studium, importado el 17 de octubre de 2026. Incluye manual, problemas resueltos y simulacros. Comparte la maquetación común de la colección y conserva sus informes; la importación no equivale a una revisión académica ni a una migración al contrato AeroBooks.

## Editar y compilar

Desde la raíz del repositorio:

```sh
python3 scripts/build-studium-books.py motores-cohete
```

Los PDF se crean en `dist/studium/motores-cohete/`. Para comprobar los archivos antes de compilar:

```sh
python3 scripts/build-studium-books.py motores-cohete --check
```

Entradas de los tres volúmenes:

- `latex/manual.tex`: Manual.
- `latex/problemas.tex`: Problemas resueltos.
- `latex/simulacros.tex`: Simulacros.

El manual compila los capítulos `latex/c01.tex` a `latex/c28.tex`. Los casos desarrollados están en `latex/M01.tex` a `latex/M28.tex`. `content/` conserva el material de origen y los anexos y soluciones que se incluyen explícitamente. Las figuras utilizadas están en `figures/`.

No hacen falta los originales de apuntes ni los exámenes privados para editar o compilar. Se han excluido esos materiales y los registros de extractos. Los informes conservan el alcance de las comprobaciones y los pendientes existentes. `studium-import.json` registra procedencia y archivos de entrada.

Los comandos `aerobooks check/build` pertenecen a los libros con `book.toml`; este proyecto usa el compilador de importaciones anterior. Una migración académica a AeroBooks requiere trasladar explícitamente fuentes, claims y revisiones, sin asignar aprobaciones automáticamente.

## Maquetación común de la colección

Los trece volúmenes comparten `shared/latex/studium-editorial.tex` y `studium-cover.tex`, desde la raíz del repositorio. Las opciones específicas están en `latex/editorial-config.tex`. Consulta `shared/EDITORIAL_STANDARD.md` para el orden común de páginas, apartados y recuadros.
