# Mecánica de Vuelo — Studium

Edición de estudio independiente para el Grado en Ingeniería Aeroespacial de la Universidad de León. Incluye el **manual universitario**, un **cuaderno de problemas** y **simulacros con soluciones**.

## Compilar desde la raíz del monorepo

```sh
python3 scripts/build-studium-books.py mecanica-vuelo --check
python3 scripts/build-studium-books.py mecanica-vuelo
```

El proyecto LaTeX se encuentra en la raíz de esta carpeta (`main.tex`, `problemas.tex`, `simulacros.tex`); la configuración de la disciplina está en `latex/preamble.tex` y la composición común en `shared/latex/`. Los recursos fotográficos y el logo auténtico están en `assets/`, y las figuras PDF de contenido, en `figures/`. Los resultados se publican en `dist/studium/mecanica-vuelo/` y no se versionan como fuentes.

**Portadas:** tres volúmenes con fotografías NASA distintas y la misma plantilla STUDIUM compartida: T-34C en maniobra para el manual, cabina del X-29 para problemas y X-29 en viraje para simulacros. Ver `assets/COVER-IMAGE.md` y `assets/cover-photo.json` para procedencia, licencia, recorte y huellas.

No se incluyen fuentes privadas, escaneos o exámenes originales de estudiantes. Los registros científicos proceden de la edición Studium importada y no constituyen revisión académica independiente ni aval de la Universidad. La plantilla editorial compartida se aplica a los tres documentos; la revisión académica sigue pendiente.
