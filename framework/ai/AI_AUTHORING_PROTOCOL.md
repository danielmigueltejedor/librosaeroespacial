# AI Authoring Protocol

## Objetivo

Producir un libro académico que sea didáctico y elegante sin sacrificar trazabilidad ni precisión.

## Secuencia obligatoria

### 1. Ingesta
Antes de redactar:
- identifica todas las fuentes disponibles;
- asigna a cada una un ID;
- registra tipo, autoridad, fecha, alcance, derechos y citation key;
- detecta qué partes del temario sí y no están cubiertas.

### 2. Auditoría
Crea o actualiza:
- `sources/manifest.json`;
- `sources/conflicts.jsonl` cuando existan discrepancias;
- `claims/ledger.jsonl` para afirmaciones de alto riesgo o especialmente importantes.

### 3. Outline
El esquema del libro debe derivarse del temario real y de las fuentes, no de una plantilla genérica.

Cada capítulo debe declarar:
- objetivos;
- prerrequisitos;
- fuentes principales;
- conceptos;
- derivaciones;
- ejemplos;
- ejercicios;
- errores frecuentes;
- checklist.

### 4. Redacción
Usa este patrón:

```text
intuición
→ definición rigurosa
→ hipótesis
→ derivación
→ interpretación física
→ ejemplo
→ error típico
→ ejercicio
→ comprobación
```

No es obligatorio usar todos los pasos en cada sección, pero no elimines hipótesis o condiciones de validez para hacer el texto “más sencillo”.

### 4.5. Trazabilidad de claims críticos

Cuando un claim de riesgo alto esté registrado en `claims/ledger.jsonl`, enlázalo desde el LaTeX con:

```latex
\claimref{CLM-001}
```

La macro es invisible en el PDF, pero permite que AeroBooks compruebe que el claim auditado está realmente conectado con el texto que pretende respaldar.

No uses `\claimref` como sustituto de una cita bibliográfica visible cuando el lector necesite la referencia.

### 5. Problemas
Un problema resuelto de calidad debe incluir, cuando corresponda:
- datos;
- qué se pide;
- diagrama/modelo;
- hipótesis;
- estrategia;
- desarrollo;
- unidades;
- comprobaciones;
- interpretación;
- errores habituales;
- método rápido de examen.

Los valores deben ser coherentes y, si son inventados para un ejercicio original, debe indicarse que el ejercicio es original.

### 6. Revisión
Separar la revisión en pasadas:
- científica/matemática;
- histórica/factual;
- bibliográfica;
- editorial;
- LaTeX/visual.

Una IA no debe “revisarse” únicamente con una relectura superficial: debe contrastar claims con sus evidencias.

## Modos de investigación

El libro puede declarar uno de estos modos en `book.toml`:

- `source_lock`: solo se utilizan fuentes proporcionadas;
- `source_plus_verify`: se puede consultar fuera para verificar;
- `source_plus_research`: se puede ampliar con nuevas fuentes de calidad.

Toda fuente externa usada de forma material debe añadirse al manifiesto y a la bibliografía.
