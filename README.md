# Libros Aeroespacial

Repositorio monorepo para libros universitarios en LaTeX de **Daniel Miguel Tejedor**, orientados al Grado en Ingeniería Aeroespacial.

La colección está construida sobre **AeroBooks**, un framework editorial y de control de calidad diseñado para que crear, revisar y mantener libros académicos a partir de fuentes sea sencillo, reproducible y compatible con flujos de trabajo asistidos por IA.

## AeroBooks

AeroBooks aporta tres capas:

```text
fuentes + reglas académicas
          ↓
     AeroBooks
   ┌──────┼─────────┐
   ↓      ↓         ↓
 LaTeX    IA      quality gates
   ↓      ↓         ↓
        libros auditables
```

No pretende “hacer infalible” a una IA. Pretende obligarla a trabajar con un proceso donde los errores sean más difíciles de introducir y más fáciles de detectar.

Incluye:

- clase LaTeX común;
- portada estándar;
- metadatos canónicos en `book.toml`;
- manifiesto de fuentes;
- jerarquía de autoridad A–E;
- ledger de claims críticos;
- registro de conflictos entre fuentes;
- protocolos científicos, matemáticos, históricos y editoriales;
- prompts especializados para IAs;
- contexto canónico generado para cada libro;
- validación de citas, labels, figuras, cuadros y fuentes;
- quality gates;
- CLI para crear, auditar y compilar libros;
- GitHub Actions.

Documentación completa:

```text
framework/README.md
AGENTS.md
```

## Estructura

```text
.
├── AGENTS.md
├── pyproject.toml
├── Makefile
│
├── framework/
│   ├── aerobooks/             # CLI
│   ├── ai/                    # protocolos y contratos para IAs
│   ├── latex/                 # aerobook.cls + estilo
│   ├── policies/              # política de calidad
│   ├── prompts/               # revisores y autor académico
│   ├── schemas/               # contratos machine-readable
│   └── templates/book/        # plantilla de libro nuevo
│
├── books/
│   └── estructuras-aeroespaciales/
│       ├── book.toml
│       ├── main.tex
│       ├── references.bib
│       ├── ai/
│       ├── sources/
│       ├── claims/
│       ├── chapters/
│       ├── appendices/
│       └── generated/
│
├── shared/                    # compatibilidad / guía editorial histórica
└── scripts/
```

## Instalación

Requiere Python 3.11+ y una instalación LaTeX con `latexmk`, Biber y MakeIndex.

```bash
python3 -m pip install -e .
aerobooks doctor
```

## Crear un libro nuevo

```bash
aerobooks new aerodinamica \
  --title "Aerodinámica para Ingeniería Aeroespacial" \
  --subtitle "Fundamentos, modelos y problemas resueltos"
```

AeroBooks genera:

```text
book.toml
main.tex
references.bib
ai/BRIEF.md
sources/manifest.json
sources/conflicts.jsonl
claims/ledger.jsonl
chapters/
appendices/
figures/
generated/
```

Antes de redactar teoría:

```bash
aerobooks ai-pack aerodinamica
```

Esto crea un único contexto para la IA con:
- contrato académico;
- política de fuentes;
- protocolo de fact-checking;
- reglas LaTeX;
- prompt maestro;
- brief del libro;
- manifest;
- claims.

## Comandos principales

```bash
aerobooks list
aerobooks new <slug> --title "..." --subtitle "..."
aerobooks sync <slug>
aerobooks ai-pack <slug>
aerobooks check <slug>
aerobooks check <slug> --strict
aerobooks build <slug>
aerobooks audit <slug>
aerobooks edition <slug> 4
aerobooks doctor
```

También:

```bash
make book BOOK=estructuras-aeroespaciales
make check BOOK=estructuras-aeroespaciales
make audit BOOK=estructuras-aeroespaciales
make ai-pack BOOK=estructuras-aeroespaciales
```

## Flujo académico recomendado

```text
1. recopilar fuentes
2. manifestarlas
3. auditar autoridad / fecha / derechos
4. detectar conflictos
5. construir outline
6. redactar
7. registrar claims críticos
8. revisión científica
9. revisión matemática
10. revisión histórica/factual
11. revisión editorial/LaTeX
12. aerobooks check --strict
13. compilación
14. inspección visual
15. changelog + edición
```

## Política para IAs

Cualquier IA que trabaje en el repositorio debe leer `AGENTS.md`.

Principios centrales:

- no inventar bibliografía ni hechos;
- no rellenar lagunas silenciosamente;
- distinguir evidencia, derivación e interpretación;
- registrar nuevas fuentes;
- registrar conflictos;
- comprobar unidades, signos y condiciones de validez;
- no elevar material de estudiantes a autoridad científica;
- no ocultar incertidumbre histórica;
- no declarar una edición “perfecta” sin quality gate.

## Libros

| Libro | Estado | Edición |
| --- | --- | --- |
| Estructuras Aeroespaciales — Volumen I | Activo | Tercera edición |

## Ediciones

Los **libros** usan nomenclatura editorial:

- Primera edición
- Segunda edición
- Tercera edición
- etc.

El software AeroBooks sí puede usar versionado técnico.

La rama `main` contiene el estado de trabajo más reciente. Las ediciones cerradas se conservan mediante snapshots/tags/releases, por ejemplo:

```text
estructuras-aeroespaciales-ed3
aerodinamica-ed2
```

## PDFs

El repositorio principal guarda código fuente y recursos editoriales. Los PDFs finales deben publicarse como releases o artefactos para no mezclar archivos generados con las fuentes.
