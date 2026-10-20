# Mecánica de Fluidos

## Revisión bibliográfica 2026-2027 (en curso)

Se han inventariado cinco libros aportados para consulta privada: White (7.ª ed.), Shaughnessy/Katz/Schaffer, Tritton, Boas y Taylor. Los PDF no se incluyen en Git por derechos de autor. El manual añade cuatro secciones de contraste con derivaciones y ejemplos **originales** sobre compuertas, flujo Couette–Poiseuille, sonda Pitot y ecuaciones de Navier–Stokes.

**Guía oficial cotejada:** el PDF firmado de la ULE 2026-2027 (asignatura **0710311**) permite mapear los **seis temas** de la asignatura a los **16 capítulos teóricos** del manual. El examen escrito representa el **70 %** y exige **5/10 como mínimo**; los ejercicios realizados presencialmente durante el curso aportan el **30 %**. Las siete prácticas y cuatro simulacros incluidos en el repositorio son material de estudio propio, no formato oficial confirmado. Esta mejora sigue siendo **parcial**: no certifica las afirmaciones pendientes de fase 6 ni constituye una edición académica cerrada. Consultar [informe de revisión](reports/revision-2026-bibliografia.md), [correspondencia detallada con la guía](bibliography/guia-docente-ule-2026-2027.json) y [manifest bibliográfico](bibliography/revision-2026-bibliografia.json).

Verificar cálculos e integración documental:

```sh
python3 books/mecanica-fluidos/scripts/check_refuerzo_2026.py
```

Para cerrar los cambios es obligatorio compilar los tres volúmenes, inspeccionar las páginas modificadas y auditar la profundidad real de cada subtema frente a la guía ya cotejada. No reclasificar fuentes PENDING por el simple hecho de haber localizado nuevos libros.


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
