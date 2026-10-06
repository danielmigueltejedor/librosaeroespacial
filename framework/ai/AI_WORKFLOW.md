# AI Workflow — AeroBooks

AeroBooks separa las tareas de una IA para evitar que el mismo pase mezcle investigación, redacción y autoaprobación.

## Fase 0 — Intake

**Entrada:** archivos, PDFs, enlaces, temario, instrucciones del usuario.

**Salida:**
- lista de fuentes;
- fuentes aún inaccesibles;
- alcance solicitado;
- preguntas abiertas.

No se redacta el libro.

## Fase 1 — Source audit

Rol: `SOURCE_AUDITOR`.

**Salida:**
- `sources/manifest.json`;
- `sources/conflicts.jsonl`;
- bibliografía inicial;
- mapa de cobertura: qué parte del temario cubre cada fuente.

## Fase 2 — Architecture

Rol: `OUTLINE_ARCHITECT`.

**Salida:**
- estructura de partes/capítulos;
- objetivos;
- prerrequisitos;
- mapa fuente → capítulo;
- lista de derivaciones;
- lista de figuras;
- banco de problemas previsto;
- lagunas.

No se inventa contenido para rellenar una laguna.

## Fase 3 — Authoring

Rol: `MASTER_AUTHOR` + `EXACT_REPRODUCER`.

Produce el contenido respetando:
- brief;
- notación;
- estilo;
- fuentes;
- rights;
- claim ledger.

## Fase 4 — Claim extraction

Extrae claims de alto riesgo:
- fórmulas;
- cifras;
- fechas;
- atribuciones;
- propiedades;
- afirmaciones absolutas;
- conclusiones que alteran el resultado.

Actualiza `claims/ledger.jsonl`.

## Fase 5 — Independent review

Ejecuta revisiones separadas:

```text
MATHEMATICAL_REVIEWER
SCIENTIFIC_REVIEWER
HISTORICAL_REVIEWER
SOURCE_AUDITOR / citation audit
```

Un revisor no debe asumir que el autor ya comprobó algo.

## Fase 6 — Editorial / LaTeX

Rol: `LATEX_EDITOR`.

Comprueba:
- composición;
- figuras;
- tablas;
- índices;
- referencias;
- consistencia de colección;
- PDF visual.

## Fase 7 — Machine gate

```bash
aerobooks check <slug> --strict
aerobooks build <slug>
```

## Fase 8 — Release review

Rol: `RELEASE_REVIEWER`.

Solo después se considera una edición candidata a publicación.

## Handoffs

Cada fase debe dejar artefactos, no solo una frase tipo “revisado”:

- auditoría → manifest/conflicts;
- arquitectura → outline;
- autoría → .tex;
- revisión → review report;
- fact-check → ledger;
- release → changelog + gate report.

Esto permite que otra IA o una persona reanude el trabajo sin depender de memoria conversacional.
