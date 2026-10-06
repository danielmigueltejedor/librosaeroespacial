# Curso mínimo — AeroBooks 0.3

AeroBooks no navega Internet por sí mismo. Con dos datos prepara el contrato, los paquetes y los gates para que un agente con acceso web descubra y registre las fuentes. No hay garantía de infalibilidad: si falta una comprobación, el gate no pasa.

```text
NO SOURCE → RESEARCH
NO EVIDENCE → NO CLAIM
NO VERIFICATION → NO SOLVED EXERCISE
NO INDEPENDENT REVIEW → NO HIGH-RISK PASS
NO COMPLETE COVERAGE → NO CHAPTER
NO GREEN GATES → NO RELEASE
```

Los libros ya creados con AeroBooks 0.2 siguen en ese contrato. El 0.3 empieza con `course.toml` o con `academic.contract = "0.3"`.

## Ejemplo sin fuentes locales

Asignatura: Mecánica de Fluidos. Institución: Universidad de León. No hay carpeta de PDFs.

```bash
aerobooks new-course fluidos \
  --course "Mecánica de Fluidos" \
  --institution "Universidad de León"

aerobooks-ai next fluidos
```

`next` responde `COURSE DISCOVERY REQUIRED`. El libro ya existe, con manifiesto vacío, y el flujo no se detiene por la ausencia de archivos.

```bash
aerobooks-ai course-discovery-pack fluidos
```

El agente abre la web de la Universidad de León, localiza la guía docente vigente del grado correcto y rellena `sources/discovery.json`. Tiene que comprobar titulación y curso académico. El nombre de la asignatura, solo, no verifica la identidad.

Cuando esa ficha está en `verified`:

```bash
aerobooks-ai next fluidos
aerobooks-ai research-pack fluidos
```

El paquete de investigación pide buscar la bibliografía de la guía y fuentes abiertas consultables: libros académicos, material universitario, repositorios, y artículos o preprints identificados como tales. Cada consulta queda en `sources/research-log.jsonl`. Una ficha vista solo en un catálogo se queda en `metadata-only` y no sostiene claims.

La matriz `sources/coverage.json` relaciona cada tema oficial con fuentes, claims, derivaciones, figuras y ejercicios. Los estados son `GAP`, `RESEARCHING`, `SUPPORTED` y `READY`. Un capítulo no se redacta mientras un concepto fundamental esté en `GAP`.

```bash
aerobooks-ai coverage fluidos --strict
aerobooks-ai next fluidos
```

A partir de ahí el orden es:

```text
BLUEPRINT → SPECS → CLAIMS/EVIDENCE → AUTHORING → REVIEW → RELEASE
```

Los paquetes correspondientes son `blueprint-pack`, `chapter-pack`, `derivation-pack`, `exercise-pack` y `release-pack`. Cada uno lleva el prompt y los artefactos de esa fase, no el corpus entero.

Un claim científico de alto riesgo necesita dos fuentes independientes de autoridad suficiente, o una fuente canónica (guía oficial, norma o libro de referencia) más una derivación comprobada, o una excepción explícita: norma oficial, definición oficial o resultado matemático derivado. Dos webs que salen del mismo libro no cuentan como independientes.

Un ejercicio resuelto entra en el ledger con enunciado original, datos, hipótesis, solución, unidades, tolerancia y revisiones matemática, dimensional, independiente y computacional. Si el número no se reproduce, no se publica.

La release exige, además, revisiones en `pass`, cobertura sin `GAP`, derivaciones fundamentales auditadas por alguien distinto del autor, figuras con su ficha física, `aerobooks check --strict`, `aerobooks-ai coverage --strict`, `aerobooks-ai gate` y un PDF compilado.

## Ejemplo con PDFs de Moodle, exámenes o apuntes

```bash
aerobooks new-course fluidos \
  --course "Mecánica de Fluidos" \
  --institution "Universidad de León" \
  --degree "Grado en Ingeniería Aeroespacial" \
  --academic-year "2026-2027" \
  --sources ~/curso/mecanica-fluidos
```

`--sources` inventaría la carpeta en `build/SOURCE_INTAKE.json` y escribe una línea en el research log. No copia los PDF al repositorio y no los acepta como evidencia: siguen en `candidate` y `metadata-only` hasta que se consulte el contenido y se decida su tier.

Esos archivos sirven para ver qué se estudia, qué nomenclatura usa el curso y qué tipo de problema cae en el examen. El material de estudiantes o el examen subido a una plataforma es tier fino `D0`, `D1` o `D2`. No autoriza una ley física ni un enunciado copiado. Los problemas del libro se escriben de nuevo.

La guía oficial se busca igual que en el caso sin archivos. Si el PDF local es esa guía, se registra con checksum, URL o localizador institucional, derechos y `content_access: full` solo después de leerlo.

`aerobooks-ai next` sigue diciendo `COURSE DISCOVERY REQUIRED` hasta que la identidad del curso quede verificada. La carpeta local no sustituye ese paso.
