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
