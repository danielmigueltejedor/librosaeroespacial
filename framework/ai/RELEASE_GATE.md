# Release Gate

Una edición no debe considerarse cerrada hasta superar todas las puertas aplicables.

## G0 — Blueprint

- misión explícita;
- audiencia y nivel explícitos;
- alcance y exclusiones;
- criterios de aceptación;
- convenciones que no pueden cambiarse;
- política ante conflictos;
- perfil didáctico/visual.

## G1 — Fuentes

- source intake completado cuando proceda;
- `sources/manifest.json` actualizado;
- bibliografía resoluble;
- fuentes externas registradas;
- autoridad/edición/contexto razonablemente auditados;
- derechos/restricciones documentados;
- ninguna fuente `rejected` usada.

## G2 — Procedencia

- chapter specs presentes;
- claims críticos registrados;
- evidence map actualizado;
- localizadores suficientes;
- conflictos documentados;
- claims de alto riesgo sin estado `pending`.

## G3 — Exactitud

- derivaciones recalculadas;
- ecuaciones dimensionalmente coherentes;
- unidades consistentes;
- signos y convenios revisados;
- fechas y atribuciones verificadas;
- casos límite comprobados cuando aporten evidencia;
- ninguna incertidumbre material ocultada.

## G4 — Didáctica

- prerrequisitos;
- objetivos;
- secuencia lógica;
- ejemplos;
- problemas;
- comprobaciones;
- errores frecuentes;
- autoevaluación;
- dificultad graduada cuando proceda.

## G5 — Figuras y editorial

- portada estándar;
- índices;
- figuras y cuadros con caption/label;
- figuras científicamente correctas;
- referencias cruzadas;
- autor sin repetición innecesaria;
- nomenclatura editorial de edición;
- ausencia de desbordamientos relevantes.

## G6 — Revisión independiente

Debe existir `pass` para todos los roles requeridos por el perfil de riesgo.

AeroBooks puede exigir dinámicamente:
- source;
- scientific;
- mathematical;
- units;
- derivation;
- historical;
- figure;
- exercise-review;
- citation;
- pedagogy;
- copyright;
- latex;
- red-team;
- release.

No basta con que el autor se relea a sí mismo.

## G7 — Machine gates

```bash
aerobooks check <slug> --strict
aerobooks-ai coverage <slug> --strict
aerobooks-ai gate <slug>
aerobooks build <slug>
```

Además:
- sin referencias rotas;
- sin citas indefinidas;
- sin errores de compilación;
- PDF inspeccionado visualmente.

## G8 — Reproducibilidad y publicación

- changelog;
- edition metadata;
- `aerobooks-ai release-manifest`;
- manifest verificado;
- snapshot/tag de la edición;
- PDF final como release/artifact;
- rama principal preparada para la edición siguiente.

## Regla

Un gate puede decir **FAIL** aunque el PDF sea visualmente perfecto. La composición no sustituye la corrección académica.
