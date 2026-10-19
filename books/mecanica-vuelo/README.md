# Mecánica de Vuelo — Studium

Edición de estudio independiente para el Grado en Ingeniería Aeroespacial de la Universidad de León. Incluye el **manual universitario**, un **cuaderno de problemas** y **simulacros con soluciones**.

## Compilar desde la raíz del monorepo

```sh
python3 scripts/build-studium-books.py mecanica-vuelo --check
python3 scripts/build-studium-books.py mecanica-vuelo
```

El proyecto LaTeX se encuentra en la raíz de esta carpeta (`main.tex`, `problemas.tex`, `simulacros.tex`); el diseño propio está en `latex/preamble.tex`. Los recursos fotográficos y el logo auténtico están en `assets/`, y las figuras PDF de contenido, en `figures/`. Los resultados se publican en `dist/studium/mecanica-vuelo/` y no se versionan como fuentes.

**Portadas:** tres volúmenes con la misma imagen aeronáutica de generación digital y logotipo original Studium reducido. La imagen **no** representa una aeronave real identificada; ver `assets/COVER-IMAGE.md` para los créditos.

No se incluyen fuentes privadas, escaneos o exámenes originales de estudiantes. Los registros científicos proceden de la edición Studium importada y no constituyen revisión académica independiente ni aval de la Universidad. La adaptación posterior al sistema editorial compartido de AeroBooks queda pendiente.
