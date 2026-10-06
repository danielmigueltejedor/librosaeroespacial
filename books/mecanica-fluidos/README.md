# Mecánica de Fluidos

Libro gestionado por AeroBooks.

## Primeros pasos

1. Completa `book.toml`.
2. Completa `ai/BRIEF.md`: es el blueprint que define exactamente qué libro quieres.
3. Registra todas las fuentes en `sources/manifest.json`.
4. Añade bibliografía real en `references.bib`.
5. Inicializa la capa académica:

```bash
aerobooks-ai init mecanica-fluidos
```

6. Audita las fuentes y crea chapter specs antes de redactar:

```bash
aerobooks-ai chapter-spec mecanica-fluidos \
  --id CH-01 \
  --title "Introducción" \
  --path chapters/01-introduction.tex \
  --status planned
```

7. Genera contexto para IA:

```bash
aerobooks ai-pack mecanica-fluidos
```

Para un capítulo concreto es preferible:

```bash
aerobooks-ai chapter-pack mecanica-fluidos CH-01 author
```

8. Mantén `claims/ledger.jsonl` y `evidence/map.jsonl`.

9. Comprueba:

```bash
aerobooks check mecanica-fluidos --strict
aerobooks-ai coverage mecanica-fluidos --strict
```

10. Antes de publicar una edición:

```bash
aerobooks-ai gate mecanica-fluidos
aerobooks build mecanica-fluidos
aerobooks-ai release-manifest mecanica-fluidos --label candidate
```

## Regla fundamental

No redactes contenido material antes de auditar las fuentes.

Una IA puede equivocarse incluso con un buen prompt. AeroBooks usa trazabilidad, revisiones independientes y gates para que los errores sean detectables y no dependan de confiar en una sola pasada del modelo.
