# AI Workflow — AeroBooks

AeroBooks separa las tareas para evitar que una misma pasada de IA investigue, redacte y se autoapruebe.

## Fase 0 — Intake

**Entrada:** archivos, PDFs, enlaces, temario, instrucciones del usuario.

Herramienta opcional:

```bash
aerobooks-ai intake <slug> --dir <carpeta-de-fuentes>
```

**Salida:**
- inventario con SHA-256;
- lista de fuentes accesibles/inaccesibles;
- alcance solicitado.

No se clasifica autoridad automáticamente.

## Fase 1 — Blueprint + Source audit

Roles:
- `BOOK_BLUEPRINT_ARCHITECT`;
- `SOURCE_AUDITOR`.

Atajo:

```bash
aerobooks-ai bootstrap <slug>
```

**Salida:**
- `ai/BRIEF.md`;
- `sources/manifest.json`;
- `sources/conflicts.jsonl`;
- bibliografía inicial;
- mapa de cobertura;
- lagunas declaradas.

## Fase 2 — Architecture

Rol: `OUTLINE_ARCHITECT`.

**Salida:**
- estructura de partes/capítulos;
- objetivos;
- prerrequisitos;
- chapter specs;
- mapa fuente → capítulo;
- lista de derivaciones;
- figuras;
- banco de problemas previsto.

No se inventa contenido para rellenar una laguna.

## Fase 3 — Authoring

Roles:
- `MASTER_AUTHOR`;
- `EXACT_REPRODUCER`.

Usar preferentemente:

```bash
aerobooks-ai chapter-pack <slug> <chapter-id> author
```

El autor recibe únicamente el contexto relevante del capítulo.

## Fase 4 — Claim extraction + evidence mapping

Roles:
- `CLAIM_EXTRACTOR`;
- `EVIDENCE_MAPPER`.

**Salida:**
- `claims/ledger.jsonl`;
- `evidence/map.jsonl`;
- nuevos conflictos si aparecen.

## Fase 5 — Independent review

Según el perfil de riesgo se ejecutan pasadas independientes:

```text
DERIVATION_AUDITOR
MATHEMATICAL_REVIEWER
UNIT_DIMENSION_REVIEWER
SCIENTIFIC_REVIEWER
HISTORICAL_REVIEWER
FIGURE_REVIEWER
EXERCISE_REVIEWER
CITATION_AUDITOR
PEDAGOGICAL_REVIEWER
COPYRIGHT_REVIEWER
RED_TEAM_REVIEWER
```

Prepara plantillas con:

```bash
aerobooks-ai review-suite <slug>
```

El grado de independencia del revisor debe registrarse.

## Fase 6 — Editorial / LaTeX

Rol: `LATEX_EDITOR`.

Comprueba:
- composición;
- figuras;
- cuadros;
- índices;
- referencias;
- consistencia de colección;
- PDF visual.

## Fase 7 — Machine gates

```bash
aerobooks check <slug> --strict
aerobooks-ai coverage <slug> --strict
aerobooks-ai gate <slug>
aerobooks build <slug>
```

## Fase 8 — Release provenance

```bash
aerobooks-ai release-manifest <slug> --label candidate
aerobooks-ai verify-manifest <slug> candidate
```

## Handoffs

Cada fase deja artefactos en Git o en `build/`, nunca solo un “revisado”.

Esto permite que otra IA o una persona reanude el trabajo sin depender de la memoria de una conversación.
