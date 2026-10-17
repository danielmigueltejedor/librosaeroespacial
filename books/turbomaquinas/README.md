# Turbomáquinas

Proyecto LaTeX de la colección Studium, importado el 17 de octubre de 2026. Incluye manual, problemas resueltos y simulacros. Conserva su composición propia y sus informes; la importación no equivale a una revisión académica ni a una migración al contrato AeroBooks.

## Editar y compilar

Desde la raíz del repositorio:

```sh
python3 scripts/build-studium-books.py turbomaquinas
```

Los PDF se crean en `dist/studium/turbomaquinas/`. Para comprobar los archivos antes de compilar:

```sh
python3 scripts/build-studium-books.py turbomaquinas --check
```

Entradas de los tres volúmenes:

- `publication/turbomaquinas-ule-2026.tex`: Manual.
- `publication/problemas-resueltos.tex`: Problemas resueltos.
- `publication/simulacros-originales.tex`: Simulacros.

Los tres `.tex` de `publication/` son documentos completos y editables. La portada se define en `publication/cover.tex`; la fotografía está en `figures/cover.jpeg`. Los esquemas del cuerpo están incluidos como TikZ. `practice/` conserva las geometrías originales y sus coordenadas.

No hacen falta los originales de apuntes ni los exámenes privados para editar o compilar. Se han excluido esos materiales y los registros de extractos. Los informes conservan el alcance de las comprobaciones y los pendientes existentes. `studium-import.json` registra procedencia y archivos de entrada.

Los comandos `aerobooks check/build` pertenecen a los libros con `book.toml`; este proyecto usa el compilador de importaciones anterior. Una migración académica a AeroBooks requiere trasladar explícitamente fuentes, claims y revisiones, sin asignar aprobaciones automáticamente.
