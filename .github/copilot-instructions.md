# GitHub Copilot instructions — AeroBooks

# AeroBooks AI entrypoint

Este repositorio contiene libros académicos y usa un contrato de trabajo estricto.

Antes de modificar contenido:

1. Lee `AGENTS.md`.
2. Lee `framework/ai/AI_WORKFLOW.md`.
3. Lee `books/<slug>/book.toml` y `books/<slug>/ai/BRIEF.md`.
4. Para trabajo inicial usa `aerobooks-ai bootstrap <slug>`.
5. Para un capítulo usa `aerobooks-ai chapter-pack <slug> <chapter-id> <role>`.
6. No inventes fuentes, datos, fórmulas, fechas, autores, DOI, ISBN, citas ni resultados.
7. Registra claims críticos y evidencia localizada.
8. No autoapruebes tu propio texto: separa autoría y revisión.
9. Antes de cerrar ejecuta los gates aplicables.

Prioridad: exactitud y trazabilidad > reproducibilidad > pedagogía > estética > velocidad.


Los pull requests que cambien contenido académico deben describir:
- fuentes añadidas;
- claims afectados;
- evidence entries;
- conflictos;
- revisiones realizadas;
- gates ejecutados.
