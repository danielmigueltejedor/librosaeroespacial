# AGENTS.md — Contrato de trabajo para IAs

Este repositorio contiene libros académicos. Una IA que modifique contenido debe tratar la exactitud como un requisito de compilación, no como una preferencia.

## Orden de autoridad

1. Petición explícita del usuario para la tarea actual.
2. `books/<slug>/ai/BRIEF.md`.
3. Fuentes registradas en `books/<slug>/sources/manifest.json`.
4. Protocolos de `framework/ai/`.
5. Estándar editorial de `shared/STYLE_GUIDE.md`.
6. Conocimiento general del modelo, únicamente cuando el modo de investigación del libro lo permita y siempre identificado.

## Regla fundamental

**No inventes nunca una afirmación para completar un hueco.**

Si una fuente no respalda un dato:
- busca una fuente permitida si la tarea autoriza investigación;
- registra la nueva fuente;
- o marca el punto como pendiente.

Nunca fabriques:
- autores;
- títulos;
- DOI;
- ISBN;
- páginas;
- fechas;
- normas;
- resultados experimentales;
- citas;
- constantes;
- cifras;
- preguntas de examen;
- atribuciones históricas.

## Tipos de contenido

Toda afirmación importante debe poder clasificarse como:

- **source-backed**: respaldada directamente por una fuente;
- **derived**: obtenida mediante una derivación reproducible;
- **interpretation**: interpretación explícita de material respaldado;
- **external-research**: obtenida fuera de las fuentes iniciales y añadida al manifiesto;
- **pending**: todavía no verificada.

No mezcles esas categorías silenciosamente.

## Conflictos entre fuentes

Si dos fuentes discrepan:
1. no elijas una en silencio;
2. registra el conflicto;
3. identifica autoridad, fecha, edición y contexto;
4. explica cuál se adopta y por qué;
5. conserva el convenio del curso cuando el libro sea de una asignatura y el conflicto sea meramente notacional.

## Matemáticas y ciencia

Para resultados derivados:
- muestra hipótesis;
- conserva unidades;
- comprueba dimensiones;
- comprueba signos;
- prueba casos límite cuando sea útil;
- diferencia aproximación y igualdad;
- no presentes como teorema una regla empírica.

## Historia y cronología

Para fechas, atribuciones, biografías o “primero en…”:
- prioriza fuentes primarias o institucionales;
- exige una fecha concreta cuando el dato sea central;
- evita afirmaciones absolutas si la historiografía es discutida;
- registra discrepancias.

## Exámenes y material de estudiantes

Fuentes tipo Wuolah, apuntes de estudiantes o correcciones no oficiales:
- pueden indicar estilo, dificultad o tipos de ejercicios;
- no tienen prioridad sobre material oficial o bibliografía técnica;
- no deben convertirse en autoridad científica por defecto;
- no deben reproducirse de forma sustitutiva si existen restricciones de derechos.

## Copyright

Parafrasea y sintetiza. No reconstruyas libros o apuntes protegidos de forma sustitutiva. Las citas textuales deben ser breves, necesarias y correctamente atribuidas.

## Antes de cerrar una tarea

Ejecuta o deja listo para ejecutar:

```bash
aerobooks check <slug> --strict
```

y, si has tocado LaTeX:

```bash
aerobooks build <slug>
```

No declares que un libro está “perfecto” si no se ha pasado el quality gate correspondiente.

## Workflow de capítulo

Cuando exista `specs/<chapter-id>.json`, la IA debe trabajar dentro de ese contrato.

Flujo preferido:

```bash
aerobooks-ai chapter-pack <slug> <chapter-id> <role>
```

El paquete de capítulo es preferible a cargar todo el repositorio indiscriminadamente.

Para claims de alto riesgo:
- registrar el claim;
- registrar al menos una evidencia localizada o una derivación;
- enlazarlo desde el manuscrito cuando la política lo exija;
- someterlo a una revisión independiente.

## Independencia de revisión

El autor no puede autoaprobar una edición.

Una revisión debe declarar si la hizo:
- el mismo modelo en una pasada nueva;
- un modelo independiente;
- una persona;
- un flujo híbrido.

Para claims centrales, prioriza una revisión más independiente cuando sea posible.

## Cierre académico

Además del gate LaTeX, ejecutar:

```bash
aerobooks-ai coverage <slug> --strict
aerobooks-ai gate <slug>
```

No crear un release manifest hasta que el estado académico esté suficientemente maduro.

## AeroBooks 0.3

Un curso nuevo puede empezar solo con la asignatura y la institución. Las fuentes locales son opcionales. Si no están, el siguiente paso es descubrirlas: `aerobooks-ai next` lo dice con `COURSE DISCOVERY REQUIRED`. El procedimiento está en `framework/ai/MINIMAL_COURSE_WORKFLOW.md`.

Los libros ya existentes siguen en el contrato 0.2. No se les aplica la matriz de cobertura ni el ledger de ejercicios nuevos.

El sistema no es infalible. Corta el paso cuando falta la capa correspondiente: sin fuente no hay investigación cerrada, sin evidencia no hay claim, sin verificación no hay ejercicio publicado, sin revisión independiente no pasa un resultado de alto riesgo, sin cobertura no hay capítulo, y sin gates en verde no hay release.
