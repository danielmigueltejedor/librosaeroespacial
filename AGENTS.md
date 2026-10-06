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
