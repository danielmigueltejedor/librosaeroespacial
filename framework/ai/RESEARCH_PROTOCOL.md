# Research Protocol

Este protocolo gobierna cómo AeroBooks amplía un libro más allá de las fuentes inicialmente proporcionadas.

## Regla central

La investigación externa no se usa para “rellenar” texto. Se usa para resolver una necesidad explícita de evidencia.

Antes de buscar, formula:

1. qué afirmación o laguna se quiere resolver;
2. qué tipo de fuente sería suficiente;
3. qué fecha/edición/contexto importa;
4. qué grado de autoridad necesita el claim.

## Contrato 0.3

La investigación queda en `sources/research-log.jsonl`: consulta, fecha, agente, candidatos, aceptados, rechazados y motivo. La guía de herramientas (Crossref, OpenAlex, repositorios, NASA NTRS, ESA, NIST, sociedades profesionales y preprints) está en `framework/prompts/LITERATURE_RESEARCHER.md`.

Para teoría consolidada se prefieren libros y material universitario. Para el estado del arte, reviews y artículos revisados. Para un resultado concreto, el trabajo primario. Un preprint se etiqueta como preprint.

## Orden de preferencia

1. fuentes primarias y documentación oficial;
2. normas y organismos técnicos;
3. libros y monografías académicas;
4. artículos revisados por pares;
5. OpenCourseWare y repositorios universitarios;
6. material docente;
7. fuentes secundarias generales;
8. foros/blogs solo como pista de descubrimiento.

## Trazabilidad obligatoria

Toda fuente externa usada materialmente debe:
- entrar en `sources/manifest.json`;
- tener `citation_key` cuando se cite;
- declarar localizador/URL/edición;
- declarar status;
- declarar derechos cuando sea relevante;
- quedar asociada a un chapter spec o a una entrada de evidence map.

## No usar snippets como evidencia

Un resultado de búsqueda, resumen automático o snippet no es evidencia final. Debe abrirse y comprobarse la fuente original siempre que sea posible.

## Fechas y ediciones

Para contenidos que cambian con el tiempo:
- registrar fecha de consulta;
- verificar la edición vigente;
- no mezclar ediciones sin avisar.

## Investigación histórica

Distinguir siempre:
- invención;
- patente;
- primera publicación;
- primera demostración;
- primera adopción;
- primer uso operativo.

Los superlativos históricos requieren evidencia especialmente fuerte.

## Resultado

La salida de una fase de investigación debe ser una actualización del manifest/evidence map/conflicts, no solo una respuesta narrativa.
