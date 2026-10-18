# Libros Aeroespacial

Repositorio monorepo para libros universitarios en LaTeX de **Daniel Miguel Tejedor**, orientados al Grado en Ingeniería Aeroespacial.

[Los cinco libros y sus fuentes](books/) · [Descargar la colección PDF actualizada](https://github.com/danielmigueltejedor/librosaeroespacial/releases/tag/studium-fluidos-auditoria-2026-10-18) · [Auditoría de los trece volúmenes](reports/bundle-audit/README.md) · [Norma común de maquetación](shared/EDITORIAL_STANDARD.md)

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
│   └── <libro>/
│       ├── studium-import.json # procedencia y documentos editables
│       ├── README.md
│       ├── latex/             # o publication/, según el proyecto
│       └── figures/           # recursos necesarios para recompilar
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

## Curso con solo la asignatura

AeroBooks 0.3 no exige PDFs de partida. Con la asignatura y la institución deja el libro listo para que un agente con web busque la guía oficial y la bibliografía. El ejemplo completo, con y sin carpeta de Moodle, está en `framework/ai/MINIMAL_COURSE_WORKFLOW.md`.

```bash
aerobooks new-course fluidos \
  --course "Mecánica de Fluidos" \
  --institution "Universidad de León"

aerobooks-ai next fluidos
```

La primera respuesta es `COURSE DISCOVERY REQUIRED`. El marco no navega solo: entrega el paquete `aerobooks-ai course-discovery-pack` y no acepta una fuente que nadie haya abierto.

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
aerobooks status <slug>
aerobooks source-add <slug> --id SRC-001 --title "..." --kind textbook --tier B --role theory
aerobooks claim-add <slug> --id CLM-001 --claim "..." --type scientific --risk high --source SRC-001
aerobooks ai-pack <slug>
aerobooks review-pack <slug> scientific
aerobooks review-pack <slug> mathematical
aerobooks review-pack <slug> historical
aerobooks review-pack <slug> citation
aerobooks review-pack <slug> latex
aerobooks check <slug>
aerobooks check <slug> --strict
aerobooks build <slug>
aerobooks audit <slug>
aerobooks edition <slug> 4
aerobooks doctor
```

`make book` y `make check` seleccionan el compilador correspondiente al proyecto:

```bash
make book BOOK=estructuras-aeroespaciales
make check BOOK=estructuras-aeroespaciales
```

Los paquetes de IA y la auditoría AeroBooks requieren un libro nativo con `book.toml`, como el creado en el ejemplo anterior:

```bash
make audit BOOK=aerodinamica
make ai-pack BOOK=aerodinamica
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

| Libro | Proyecto | Edición |
| --- | --- | --- |
| [Teoría de Estructuras](books/estructuras-aeroespaciales/) | Studium importado | Segunda edición completa, manuscrito v3 |
| [Mecánica de Fluidos](books/mecanica-fluidos/) | Studium importado | Portada I edición, revisión científica fase 6 |
| [Turbomáquinas](books/turbomaquinas/) | Studium importado | Primera edición |
| [Tecnología Aeroespacial](books/tecnologia-aeroespacial/) | Studium importado | Primera edición |
| [Motores Cohete](books/motores-cohete/) | Studium importado | Primera edición |


## Editar los libros importados de Studium

Los cinco libros conservan sus fuentes y su diseño Studium. Estructuras contiene su manual; Fluidos, Turbomáquinas, Tecnología Aeroespacial y Motores Cohete incluyen **manual, problemas y simulacros**. Se guardan también los recursos necesarios para recompilar. No se incluyen los apuntes, escaneos ni exámenes privados utilizados como referencia.

Las antiguas ediciones AeroBooks de Estructuras y Fluidos se han sustituido por sus manuscritos actuales y permanecen recuperables en el historial de Git. Estructuras recupera el manuscrito completo: la copia de clase tenía un salto de la página impresa 98 a la 230. Fluidos incorpora las correcciones hasta la fase 6. La paginación cambia con la maquetación común; los informes registran el tamaño de los PDF actuales.

```bash
python3 scripts/build-studium-books.py all --check
python3 scripts/build-studium-books.py estructuras-aeroespaciales
python3 scripts/build-studium-books.py mecanica-fluidos
python3 scripts/build-studium-books.py motores-cohete
python3 scripts/build-studium-books.py tecnologia-aeroespacial
python3 scripts/build-studium-books.py turbomaquinas
```

Requieren Python 3.11+ y pdfLaTeX (TeX Live con español, Latin Modern, TikZ y tcolorbox). Los trece PDF se generan bajo `dist/studium/`. GitHub Actions también los compila y publica en el artefacto **studium-pdfs**. Las entregas PDF de la importación se conservan en [Releases](https://github.com/danielmigueltejedor/librosaeroespacial/releases).

Consulta el README de cada libro para saber qué `.tex` editar. La maquetación de los trece volúmenes se controla en [`shared/EDITORIAL_STANDARD.md`](shared/EDITORIAL_STANDARD.md) y `shared/latex/`: una sola plantilla para portadas, capítulos, recuadros y páginas iniciales. Fluidos y Motores Cohete usan fotografías NASA de mayor resolución, con procedencia en sus archivos `cover-photo.json`.

Estos proyectos existentes están archivados como importaciones; sus registros académicos no se convierten automáticamente al contrato AeroBooks y no se asignan aprobaciones. Para ellos se usa el compilador anterior, y para los libros nativos se mantiene `aerobooks build`.

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

## Flujo de máxima calidad para IA

Para trabajo serio sobre un capítulo:

```bash
aerobooks-ai chapter-spec <slug> ...
aerobooks-ai evidence-add <slug> ...
aerobooks-ai chapter-pack <slug> <chapter-id> author
```

Después de redactar, generar revisiones independientes:

```bash
aerobooks-ai chapter-pack <slug> <chapter-id> derivation
aerobooks-ai chapter-pack <slug> <chapter-id> scientific
aerobooks-ai chapter-pack <slug> <chapter-id> red-team
aerobooks-ai chapter-pack <slug> <chapter-id> figure
```

Antes de una edición candidata:

```bash
aerobooks check <slug> --strict
aerobooks-ai coverage <slug> --strict
aerobooks-ai gate <slug>
aerobooks build <slug>
aerobooks-ai release-manifest <slug> --label candidate
```

Los protocolos se encuentran en `framework/ai/` y son parte del producto: especifican cómo investigar, derivar, diseñar ejercicios, tratar incertidumbre, revisar figuras y mantener procedencia.

## Atajo para iniciar un libro con IA

Después de `aerobooks new`, genera un único paquete de arranque:

```bash
aerobooks-ai bootstrap <slug>
```

Ese paquete obliga a la IA a completar primero el blueprint, la auditoría de fuentes, los conflictos y la arquitectura antes de redactar.

Cuando el manuscrito esté maduro, prepara todas las revisiones que el perfil de riesgo del libro exige:

```bash
aerobooks-ai review-suite <slug>
```

AeroBooks calcula dinámicamente si además hacen falta revisiones de matemáticas, unidades, derivaciones, figuras, ejercicios o historia a partir de los claims y chapter specs.
