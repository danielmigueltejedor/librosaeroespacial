# Teoría de Estructuras

Segunda edición completa, a partir del manuscrito v3 completo, de 270 páginas antes de la revisión de maquetación. La copia de clase de 140 páginas tenía un salto en el contenido; se recupera el manuscrito completo con la portada fotográfica actual. Las ediciones antiguas permanecen en el historial de Git.

## Editar y compilar

Los textos editables están en `latex/manual.tex`, `latex/problemas.tex` y `latex/simulacros.tex`. Las figuras TikZ están incluidas en el texto; los recursos externos están en `figures/` o junto al documento. La portada conserva el diseño Studium.

Desde la raíz del repositorio:

```sh
python3 scripts/build-studium-books.py estructuras-aeroespaciales --check
python3 scripts/build-studium-books.py estructuras-aeroespaciales
```

Requiere Python 3.11+ y pdfLaTeX/TeX Live. El PDF se genera en `dist/studium/estructuras-aeroespaciales/estructuras-aeroespaciales-manual.pdf`.

Se archivan fuentes preexistentes para poder editarlas y recompilarlas. No se incluyen apuntes, escaneos ni exámenes privados. No se atribuye una nueva revisión científica ni se convierten automáticamente los registros al contrato académico AeroBooks. `studium-import.json` registra el origen exacto y las adaptaciones de importación.

## Maquetación común de la colección

Los quince volúmenes comparten `shared/latex/studium-editorial.tex` y `studium-cover.tex`, desde la raíz del repositorio. Las opciones específicas están en `latex/editorial-config.tex`. Consulta `shared/EDITORIAL_STANDARD.md` para el orden común de páginas, apartados y recuadros.

## Cuadernos de entrenamiento

- **Problemas**: 105 ejercicios del manual, reorganizados en ocho capítulos y publicados por separado con datos, hipótesis, modelos, cálculo, resultados, límites y errores frecuentes. No se cuentan como ejercicios adicionales al manual.
- **Simulacros**: cuatro pruebas propuestas de 150 minutos y diez puntos, con cinco casos cada una, rúbrica y soluciones en una segunda parte. Seleccionan veinte ejercicios del banco, con los mismos datos; no son exámenes oficiales ni variantes inéditas. Cubren conjuntamente los ocho temas.
- Los ocho casos avanzados de cortante incluyen esquemas de nudos, sentido de flujo y coordenadas generados desde la geometría del banco.

Los contenidos editables están en `content/`. Para regenerarlos desde el banco público, con SymPy instalado:

```sh
python3 books/estructuras-aeroespaciales/scripts/make_companions.py
```

Los tres PDF se producen con el mismo comando de compilación indicado arriba. La evidencia de cálculo está en `reports/bundle-audit/estructuras.json`; el alcance específico de esta incorporación, en `reports/bundle-audit/estructuras-companions.md`. Las propiedades de material son datos académicos de enunciado, sin atribuirles certificación para diseño.
