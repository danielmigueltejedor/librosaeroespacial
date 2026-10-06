# AeroBooks Framework — Changelog

AeroBooks es software, por lo que su versión técnica es independiente de las ediciones editoriales de los libros.

## 0.3.0 — octubre de 2026

Un libro puede arrancar con la asignatura y la institución. Las fuentes locales son opcionales.

- `aerobooks.toml` guarda autor, institución, programa, línea editorial, pedagogía, investigación, calidad y copyright. Cada libro sobrescribe lo que necesite.
- `aerobooks new-course` crea el contrato 0.3. Sin carpeta de fuentes sigue en descubrimiento; con `--sources` solo inventaría, no copia ni acepta los archivos.
- `aerobooks-ai next` indica `COURSE DISCOVERY REQUIRED` hasta que la guía oficial esté identificada por titulación y curso, no por el nombre.
- Paquetes pequeños: `course-discovery-pack`, `research-pack`, `source-audit-pack`, `blueprint-pack`, `derivation-pack`, `exercise-pack` y `release-pack`.
- Tiers finos `A0`–`E` junto a los tiers `A`–`E`. Una fuente vista solo como ficha o snippet no entra como evidencia.
- Perfil de autoridad por dimensiones, sin una nota única que decida la verdad.
- Corroboración de claims de alto riesgo, con detección de orígenes compartidos.
- `sources/coverage.json`, `derivations/ledger.jsonl`, `exercises/ledger.jsonl`, `figures/ledger.jsonl` y `sources/research-log.jsonl`.
- Gates que fallan cerrados en el contrato 0.3. Los libros 0.2 no cambian de puerta.

## 0.2.0 — octubre de 2026

Capa académica de alta trazabilidad:

- `aerobooks-ai` como CLI complementario;
- chapter specs machine-readable;
- evidence map claim → source + locator;
- chapter packs de contexto mínimo para IAs;
- nuevos roles: red-team, derivation auditor, figure reviewer, pedagogy, copyright, units, conflict resolver, blueprint architect, claim extractor y evidence mapper;
- protocolos de investigación, procedencia, derivaciones, ejercicios, figuras e incertidumbre;
- quality rubric por dimensiones y blockers;
- revisión independiente con grado de independencia declarado;
- academic gate separado del gate LaTeX;
- release manifests con SHA-256 para reproducibilidad;
- schemas de chapter spec, evidence y release manifest;
- CI de cobertura académica;
- Estructuras Aeroespaciales migrado como implementación de referencia.

## 0.1.0 — octubre de 2026

Primera versión funcional:

- CLI instalable;
- `aerobook.cls`;
- portada y estilo compartidos;
- `book.toml` como metadata canónica;
- scaffold de libros;
- source manifest;
- source tiers A–E;
- conflict ledger;
- critical claim ledger;
- `\claimref{}` para trazabilidad manuscrito → evidencia;
- AI context packs;
- specialized review packs;
- prompts de autor, auditor, revisor científico, matemático, histórico, bibliográfico, LaTeX y release;
- validación de citas y referencias;
- validación de figuras/cuadros;
- strict quality gate;
- unit/integration tests;
- GitHub Actions para calidad y compilación.
