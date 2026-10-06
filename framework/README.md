# AeroBooks Framework

AeroBooks es la capa editorial, de reproducibilidad y control de calidad del repositorio **Libros Aeroespacial**.

Su objetivo no es sustituir LaTeX. Su objetivo es convertir la creación de libros académicos a partir de fuentes en un proceso **repetible, auditable y fácil de usar**, tanto para una persona como para una IA.

## Principios

1. **Source-first.** Ningún contenido académico se da por correcto solo porque “suene bien”.
2. **Fail closed.** Si falta evidencia, se declara la laguna; no se inventa.
3. **Trazabilidad.** Las fuentes se registran en `sources/manifest.json` y los claims críticos pueden registrarse en `claims/ledger.jsonl`.
4. **Separación entre fuente e inferencia.** La IA debe distinguir texto respaldado, derivación propia, interpretación y conocimiento externo.
5. **Reproducibilidad.** Metadatos, estilo, fuentes, prompts y quality gates viven en Git.
6. **Ediciones editoriales.** Los libros usan Primera, Segunda, Tercera edición… El framework sí puede usar SemVer porque es software.
7. **Composición común.** Portadas, figuras, cajas, referencias y metadatos siguen un estándar común.
8. **No hay garantía mágica de verdad.** El framework reduce errores mediante disciplina, revisión y automatización; no reemplaza la revisión humana experta.

## Flujo recomendado

```text
fuentes
  ↓
registro en manifest
  ↓
auditoría de fuentes
  ↓
outline
  ↓
redacción con citas / derivaciones
  ↓
claim ledger para afirmaciones críticas
  ↓
revisión científica / histórica / matemática
  ↓
revisión LaTeX y editorial
  ↓
aerobooks check --strict
  ↓
aerobooks build
  ↓
release de una edición
```

## Instalación local

Desde la raíz del repositorio:

```bash
python3 -m pip install -e .
aerobooks doctor
```

## Crear un libro

```bash
aerobooks new aerodinamica \
  --title "Aerodinámica para Ingeniería Aeroespacial" \
  --subtitle "Fundamentos, modelos y problemas resueltos"
```

Después:

```bash
aerobooks ai-pack aerodinamica
aerobooks check aerodinamica
aerobooks build aerodinamica
```

## Comandos

| Comando | Función |
| --- | --- |
| `aerobooks new` | crea un libro desde la plantilla |
| `aerobooks list` | lista libros gestionados |
| `aerobooks sync` | genera metadatos LaTeX desde `book.toml` |
| `aerobooks ai-pack` | genera un contexto canónico para una IA |
| `aerobooks check` | comprueba fuentes, citas, labels, figuras y claims |
| `aerobooks audit` | quality gate estricto + compilación |
| `aerobooks build` | comprueba y compila |
| `aerobooks edition` | cambia la edición editorial |
| `aerobooks doctor` | comprueba dependencias |

## Estructura

```text
framework/
├── aerobooks/             # CLI
├── ai/                    # protocolos para IAs
├── latex/                 # clase y estilo comunes
├── policies/              # reglas de calidad
├── prompts/               # prompts especializados
├── schemas/               # contratos de datos
└── templates/
    └── book/              # scaffold de un libro nuevo
```

## Qué debe leer una IA

Antes de tocar un libro:

1. `AGENTS.md`
2. `framework/ai/AI_AUTHORING_PROTOCOL.md`
3. `framework/ai/SOURCE_POLICY.md`
4. `framework/ai/FACT_CHECK_PROTOCOL.md`
5. `framework/ai/LATEX_PROTOCOL.md`
6. `books/<slug>/book.toml`
7. `books/<slug>/ai/BRIEF.md`
8. `books/<slug>/sources/manifest.json`

La forma más sencilla es generar un paquete único:

```bash
aerobooks ai-pack <slug>
```

que crea `books/<slug>/build/AI_CONTEXT.md`.
