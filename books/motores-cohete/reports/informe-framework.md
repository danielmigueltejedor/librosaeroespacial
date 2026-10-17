# Studium utilizado e incidencias

Commit exacto: `8bed8a52900d994e683cce7f37b565cd6caa4b15`. Main clonado en el proyecto independiente. Se revisaron releases, PR abiertas y PR integradas; las respuestas de GitHub están en evidencia. No se modificó el repositorio principal.

La batería ejecutada terminó con **1053 passed, 2 skipped**; las dos omisiones corresponden a idiomas LaTeX no instalados. Se enumeraron **91 herramientas MCP** y se utilizaron las interfaces reales para proyecto, blueprint, fuentes, párrafos, problemas, cálculo, dimensiones, derivaciones, notación, contratos, figuras y auditorías.

Resumen nativo final (las cifras describen registros, no aprobación científica):

```json
{
  "sections": 28,
  "sections_with_prose": 28,
  "paragraphs": 195,
  "paragraphs_audited": 0,
  "words": 25630,
  "sources": 38,
  "excerpts_used": 18,
  "excerpts_stored": 18,
  "problems": 77,
  "problems_checked": 77,
  "computations_replayed": 183,
  "derivations": 7,
  "figures": 30,
  "figures_checked": 30,
  "figures_planned": 28,
  "figure_references": 30,
  "figures_uncited": 0,
  "notation_entries": 10,
  "notation_symbols": 10,
  "terminology_entries": 0,
  "audits": 0,
  "reviews": 1,
  "open_contradictions": 0
}
```

Estado de la revisión nativa: bloqueada por auditorías pendientes; `released=false`. Exportación nativa de diagnóstico: `rendered`. Los PDF de entrega se componen con el manuscrito y los registros mediante el adaptador tipográfico del proyecto; no se parchea el framework.

[Incidencia #76](https://github.com/danielmigueltejedor/studium/issues/76): falso positivo con capacidad calorífica variable. Se incluye reproducción mínima. Las adaptaciones de importación conservan `aligned`, delimitadores matemáticos explícitos y referencias de figuras para evitar pérdidas de estructura al pasar de LaTeX a registros.
