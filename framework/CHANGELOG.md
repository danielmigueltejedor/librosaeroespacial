# AeroBooks Framework — Changelog

AeroBooks es software, por lo que su versión técnica es independiente de las ediciones editoriales de los libros.

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
