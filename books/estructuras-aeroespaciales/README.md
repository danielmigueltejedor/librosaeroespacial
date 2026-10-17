# Teoría de Estructuras

Segunda edición completa, a partir del manuscrito v3 de 270 páginas. La copia de clase de 140 páginas tenía un salto en el contenido; se recupera el manuscrito completo con la portada fotográfica actual. Las ediciones antiguas permanecen en el historial de Git.

## Editar y compilar

El texto editable está en `latex/manual.tex`. Las figuras TikZ están incluidas en el texto; los recursos externos están en `figures/` o junto al documento. La portada conserva el diseño Studium.

Desde la raíz del repositorio:

```sh
python3 scripts/build-studium-books.py estructuras-aeroespaciales --check
python3 scripts/build-studium-books.py estructuras-aeroespaciales
```

Requiere Python 3.11+ y pdfLaTeX/TeX Live. El PDF se genera en `dist/studium/estructuras-aeroespaciales/estructuras-aeroespaciales-manual.pdf`.

Se archivan fuentes preexistentes para poder editarlas y recompilarlas. No se incluyen apuntes, escaneos ni exámenes privados. No se atribuye una nueva revisión científica ni se convierten automáticamente los registros al contrato académico AeroBooks. `studium-import.json` registra el origen exacto y las adaptaciones de importación.
