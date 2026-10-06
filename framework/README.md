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
| `aerobooks status` | resume fuentes, claims, conflictos y capítulos |
| `aerobooks source-add` | registra una fuente sin editar JSON a mano |
| `aerobooks claim-add` | registra un claim crítico |
| `aerobooks ai-pack` | genera un contexto canónico para una IA |
| `aerobooks review-pack` | genera contexto especializado para un revisor IA |
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

## Capa académica v0.2

AeroBooks separa ahora el tooling editorial del tooling de evidencia.

El CLI principal sigue siendo:

```bash
aerobooks ...
```

La capa académica se invoca con:

```bash
aerobooks-ai ...
```

### Chapter specs

Cada capítulo importante puede tener un contrato machine-readable:

```text
books/<slug>/specs/CH-01.json
```

Ese contrato fija:
- alcance;
- objetivos;
- prerrequisitos;
- fuentes autorizadas;
- claims;
- derivaciones;
- figuras;
- ejercicios;
- estado editorial.

### Evidence map

```text
books/<slug>/evidence/map.jsonl
```

Conecta:

```text
capítulo → claim → evidencia → source ID + locator
```

Esto permite que una IA reproduzca la procedencia de una ecuación, fecha o afirmación crítica sin depender de memoria conversacional.

### Paquetes de capítulo para IAs

```bash
aerobooks-ai chapter-pack estructuras-aeroespaciales CH-01-FUNDAMENTOS author
aerobooks-ai chapter-pack estructuras-aeroespaciales CH-01-FUNDAMENTOS red-team
```

El paquete contiene únicamente:
- reglas globales;
- protocolo académico;
- spec del capítulo;
- fuentes relevantes;
- claims relevantes;
- evidence map;
- manuscrito actual;
- prompt del rol.

Esto reduce ruido de contexto y hace más reproducible el trabajo de una IA.

### Revisiones independientes

```bash
aerobooks-ai review-template <slug> \
  --id REV-SCI-001 \
  --role scientific \
  --scope CH-01
```

Los informes registran también el grado de independencia del revisor:
- mismo modelo, nueva pasada;
- modelo independiente;
- humano;
- híbrido.

### Academic gate

```bash
aerobooks-ai coverage <slug> --strict
aerobooks-ai gate <slug>
```

El gate bloquea una edición si quedan, entre otros:
- claims críticos pendientes;
- conflictos sin resolver;
- chapter specs no preparados;
- revisiones obligatorias ausentes;
- revisiones con errores/blockers.

### Release reproducible

```bash
aerobooks-ai release-manifest <slug> --label ed4-candidate
aerobooks-ai verify-manifest <slug> ed4-candidate
```

El manifest guarda SHA-256 del manuscrito y de las reglas del framework que afectan a la edición. Sirve para demostrar que una edición candidata corresponde exactamente a un estado concreto del proyecto.

## Modelo de calidad

AeroBooks no promete una IA infalible. Una herramienta seria no puede garantizar ausencia absoluta de errores. En su lugar aplica defensa en profundidad:

```text
fuentes
  ↓
manifest
  ↓
chapter spec
  ↓
claim ledger
  ↓
evidence map
  ↓
autoría
  ↓
revisión matemática / científica / histórica
  ↓
red team
  ↓
quality gates
  ↓
build + inspección visual
  ↓
release manifest
```

La filosofía es que un error crítico tenga que atravesar varias barreras independientes antes de llegar a una edición publicada.
