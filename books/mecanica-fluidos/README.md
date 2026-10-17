# Mecánica de Fluidos

Revisión científica fase 6 del manual de 290 páginas. Incluye las últimas correcciones locales, posteriores a la copia de clase. Los informes conservan el alcance y los pendientes de cada fase.

## Editar y compilar

El texto editable está en `latex/manual.tex`. Las figuras TikZ están incluidas en el texto; los recursos externos están en `figures/` o junto al documento. La portada conserva el diseño Studium.

Desde la raíz del repositorio:

```sh
python3 scripts/build-studium-books.py mecanica-fluidos --check
python3 scripts/build-studium-books.py mecanica-fluidos
```

Requiere Python 3.11+ y pdfLaTeX/TeX Live. El PDF se genera en `dist/studium/mecanica-fluidos/mecanica-fluidos-manual.pdf`.

Se archivan fuentes preexistentes para poder editarlas y recompilarlas. No se incluyen apuntes, escaneos ni exámenes privados. No se atribuye una nueva revisión científica ni se convierten automáticamente los registros al contrato académico AeroBooks. `studium-import.json` registra el origen exacto y las adaptaciones de importación.
