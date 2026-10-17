# Estructuras Aeroespaciales — Volumen I

**Autor:** Daniel Miguel Tejedor  
**Edición actual:** Tercera edición — octubre de 2026  
**Framework:** AeroBooks

## Alcance

Volumen dedicado a los conceptos básicos y al modelo monodimensional de Teoría de Estructuras:

- fundamentos de estructuras aeronáuticas;
- sólidos rígidos y deformables;
- tensión y deformación;
- leyes de comportamiento;
- cargas y vinculaciones;
- esfuerzos internos;
- equilibrio estático y elástico;
- leyes de esfuerzos;
- problemas resueltos y preparación de examen.

## Fuente canónica de metadatos

```text
book.toml
```

No cambies autor, edición, fecha o título directamente en LaTeX. Sincroniza con:

```bash
aerobooks sync estructuras-aeroespaciales
```

## Contexto para IA

El brief específico está en:

```text
ai/BRIEF.md
```

Las fuentes y claims se gestionan en:

```text
sources/manifest.json
sources/conflicts.jsonl
claims/ledger.jsonl
```

Para crear un paquete único de contexto:

```bash
aerobooks ai-pack estructuras-aeroespaciales
```

## Trazabilidad académica

La Tercera edición sirve también como implementación de referencia de AeroBooks 0.2:

```text
specs/                 contratos de capítulos
evidence/map.jsonl     claim → evidencia → fuente/localizador
claims/ledger.jsonl    afirmaciones críticas
sources/manifest.json  universo de fuentes
reviews/               revisiones independientes
release/               manifests reproducibles
```

Para saber cuál es el siguiente paso:

```bash
aerobooks-ai next estructuras-aeroespaciales
```

Para revisar la cobertura:

```bash
aerobooks-ai coverage estructuras-aeroespaciales --strict
```

Cuando llegue la revisión de la edición:

```bash
aerobooks-ai review-suite estructuras-aeroespaciales
```

El framework añadirá automáticamente revisiones de matemáticas, unidades, derivaciones, figuras y ejercicios porque este libro contiene esos tipos de contenido.

## Comprobación

```bash
aerobooks check estructuras-aeroespaciales --strict
```

## Compilación

Desde la raíz del repositorio:

```bash
aerobooks build estructuras-aeroespaciales
```

o:

```bash
make book BOOK=estructuras-aeroespaciales
```

La clase, portada, cajas y estilo base proceden de `framework/latex/`.

## Ediciones

La carpeta no se duplica por edición. `main` contiene la edición en desarrollo y los estados publicados se conservan mediante snapshots/tags/releases.

```text
estructuras-aeroespaciales-ed3
estructuras-aeroespaciales-ed4
...
```
