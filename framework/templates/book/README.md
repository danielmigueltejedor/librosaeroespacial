# {{TITLE}}

Libro gestionado por AeroBooks.

## Primeros pasos

1. Completa `book.toml`.
2. Completa `ai/BRIEF.md`.
3. Registra las fuentes en `sources/manifest.json`.
4. Añade bibliografía real en `references.bib`.
5. Genera el contexto para IA:

```bash
aerobooks ai-pack {{SLUG}}
```

6. Comprueba:

```bash
aerobooks check {{SLUG}}
```

7. Compila:

```bash
aerobooks build {{SLUG}}
```

## Regla

No redactes contenido material antes de auditar las fuentes.
