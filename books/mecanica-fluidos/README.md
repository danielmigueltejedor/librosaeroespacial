# Mecánica de Fluidos

Revisión científica fase 6 del manuscrito de 290 páginas anterior a la revisión de maquetación. Incluye las últimas correcciones locales, posteriores a la copia de clase. Los informes conservan el alcance y los pendientes de cada fase.

## Editar y compilar

El texto editable está en `latex/manual.tex`. Las figuras TikZ están incluidas en el texto; los recursos externos están en `figures/` o junto al documento. La portada conserva el diseño Studium.

Desde la raíz del repositorio:

```sh
python3 scripts/build-studium-books.py mecanica-fluidos --check
python3 scripts/build-studium-books.py mecanica-fluidos
```

Requiere Python 3.11+ y pdfLaTeX/TeX Live. El PDF se genera en `dist/studium/mecanica-fluidos/mecanica-fluidos-manual.pdf`.

Se archivan fuentes preexistentes para poder editarlas y recompilarlas. No se incluyen apuntes, escaneos ni exámenes privados. No se atribuye una nueva revisión científica ni se convierten automáticamente los registros al contrato académico AeroBooks. `studium-import.json` registra el origen exacto y las adaptaciones de importación.

## Maquetación común de la colección

Los quince volúmenes comparten `shared/latex/studium-editorial.tex` y `studium-cover.tex`, desde la raíz del repositorio. Las opciones específicas están en `latex/editorial-config.tex`. Consulta `shared/EDITORIAL_STANDARD.md` para el orden común de páginas, apartados y recuadros.

## Cuadernos originales de Fluidos

`latex/problemas.tex` contiene 48 problemas resueltos (tres por cada uno de los 16 capítulos) y siete talleres Wolfram. `latex/simulacros.tex` reúne cuatro simulacros de 150 minutos con cinco problemas cada uno, rúbrica y soluciones separadas. Son datos hipotéticos originales, no exámenes oficiales.

Los textos editables están en `content/`. El banco autoral está en `scripts/fluid_bank.py`; se regenera con `scripts/make_fluid_books.py` y `scripts/make_fluid_workshops.py` usando Python con SymPy. La compilación normal usa los LaTeX ya generados y no requiere esas dependencias. Para conservar una edición manual de `content/`, no ejecutes el generador encima sin trasladar antes los cambios al banco.

`check_fluid_bank.py` requiere SymPy, Pint y SciPy. Contrasta todos los resultados del banco y las variantes, más residuos de modelos seleccionados. `workshops/w01.wl` a `w07.wl` se ejecutaron con Wolfram Language 15. Los resultados se guardan en `reports/`; no constituyen aprobación científica independiente.
