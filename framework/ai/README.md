# Herramientas para IAs

Esta carpeta define el comportamiento esperado de una IA que escriba o revise libros del repositorio.

## Capas

### Contrato de autoría
`AI_AUTHORING_PROTOCOL.md`

Define el proceso completo de ingesta, auditoría, outline, redacción y revisión.

### Política de fuentes
`SOURCE_POLICY.md`

Define jerarquía A–E, corroboración y restricciones de uso.

### Fact checking
`FACT_CHECK_PROTOCOL.md`

Define cómo verificar claims científicos, matemáticos, históricos y numéricos.

### LaTeX
`LATEX_PROTOCOL.md`

Impide que cada IA improvise estilos o rompa la identidad editorial.

### Release
`RELEASE_GATE.md`

Define cuándo una edición puede considerarse cerrada.

## Plantillas

`templates/` incluye tarjetas para documentar fuentes, claims, conflictos e informes de revisión.

## Contexto canónico

Para evitar que una IA reciba instrucciones parciales:

```bash
aerobooks ai-pack <slug>
```

genera un único `AI_CONTEXT.md` con protocolos, brief, manifest y ledger.

## Evidencia y reproducibilidad

AeroBooks v0.2 añade:

- `BOOK_BLUEPRINT_PROTOCOL.md`: captura exacta de la intención del libro;
- `RESEARCH_PROTOCOL.md`: investigación externa trazable;
- `PROVENANCE_PROTOCOL.md`: cadena claim → evidencia → fuente;
- `DERIVATION_PROTOCOL.md`: reproducción matemática independiente;
- `EXERCISE_PROTOCOL.md`: diseño y validación de problemas;
- `FIGURE_PROTOCOL.md`: control científico de figuras;
- `UNCERTAINTY_PROTOCOL.md`: lenguaje y estados de incertidumbre;
- `AI_ORCHESTRATION.md`: separación de roles;
- `QUALITY_RUBRIC.md`: blockers y dimensiones de calidad.

Para tareas acotadas por capítulo usa `aerobooks-ai chapter-pack`. Es preferible a proporcionar a la IA un contexto masivo no filtrado.
