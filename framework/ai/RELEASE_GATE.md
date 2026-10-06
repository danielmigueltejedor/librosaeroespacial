# Release Gate

Una edición no debe considerarse cerrada hasta pasar estas puertas.

## G1 — Alcance
- temario explícito;
- lagunas declaradas;
- edición y fecha correctas;
- no hay capítulos “rellenados” sin fuente.

## G2 — Fuentes
- manifest actualizado;
- bibliografía resoluble;
- fuentes externas añadidas;
- conflictos documentados;
- derechos/restricciones razonablemente identificados.

## G3 — Exactitud
- claims críticos revisados;
- derivaciones comprobadas;
- unidades consistentes;
- fechas y atribuciones verificadas;
- no quedan marcadores `[SOURCE NEEDED]`.

## G4 — Didáctica
- objetivos;
- prerrequisitos;
- ejemplos;
- problemas;
- comprobaciones;
- errores frecuentes.

## G5 — Editorial
- portada estándar;
- índices;
- figuras y cuadros;
- referencias cruzadas;
- autor sin repetición innecesaria;
- nomenclatura editorial de edición.

## G6 — Técnica
- `aerobooks check <slug> --strict`;
- compilación limpia;
- sin referencias rotas;
- sin overfull relevantes;
- PDF inspeccionado visualmente.

## G7 — Publicación
- changelog;
- snapshot/tag de la edición;
- PDF final como release/artifact;
- rama main preparada para la edición siguiente.
