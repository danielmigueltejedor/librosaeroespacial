# Mecánica de Fluidos — contraste bibliográfico y primera mejora (19-10-2026)

## Alcance y límite de la guía ULE

- Asignatura **0710311**, obligatoria, 2.º curso, 1.er cuatrimestre, 6 ECTS del Grado en Ingeniería Aeroespacial (ULE), curso **2026-2027**.
- Ficha oficial: https://www.unileon.es/estudiantes/oferta-academica/grados/grado-en-ingenieria-aeroespacial/plan-estudios?cursoa=2026&id=0710311&te=G
- Visor oficial de guía: https://visor-guiadocente.unileon.es/snapshots/2026-2027/0710311
- **Limitación verificable:** el visor web no devolvió temario, evaluación y bibliografía completos en contenido legible para esta auditoría. No se presenta un programa reconstruido del manual como si fuera el programa firmado por la universidad; la coincidencia con el curso queda **pendiente de comprobación**.

## Libros aportados (consulta privada, no redistribuida)

1. White, *Fluid Mechanics*, 7.ª ed. (2011), 885 páginas PDF; capítulos 2, 3, 4 y 6 contrastados por sus títulos y pasajes relevantes.
2. Shaughnessy, Katz y Schaffer, *Introduction to Fluid Mechanics* (2005), 1057 páginas PDF; capítulos 10 y 11 consultados.
3. Tritton, *Physical Fluid Dynamics*, 2.ª ed. (1988), 536 páginas PDF; escaneo sin capa textual utilizable para localizar citas. **Pendiente de cotejo por páginas**.
4. Boas, *Mathematical Methods in the Physical Sciences*, 3.ª ed. (2006), 859 páginas PDF; capítulos 6, 8 y 10 identificados por su índice.
5. Taylor, *Classical Mechanics* (2005), 808 páginas PDF; escaneo sin capa textual utilizable. Bibliografía editorial contrastada; **pendiente de cotejo por páginas**.

Metadatos y localizadores verificables: [revision-2026-bibliografia.json](../bibliography/revision-2026-bibliografia.json). Los valores de páginas indican número de páginas del archivo PDF, distinto del folio impreso del libro.

## Inventario previo

El manual no parte de cero: contiene 16 capítulos teóricos, 7 capítulos de prácticas con Mathematica, notación, formulario, soluciones, auditoría y plan de estudio. Hay un cuaderno independiente con 48 problemas y 7 talleres y cuatro simulacros originales. Se conserva la clase editorial compartida de la colección.

**Riesgo académico:** la propia sección histórica de auditoría del manual registra 157 fuentes pendientes. La revisión anterior solo probó selectivamente 20 etiquetas de ecuaciones en su fase 6, sin aprobación científica integral. Añadir esta bibliografía no convierte automáticamente esos 157 estados en “VERIFIED”.

## Cuatro refuerzos incorporados al manual

| Capítulo | Sección añadida | Derivación original | Verificación numérica |
| --- | --- | --- | --- |
| 5 — Estática | Presión y centro de presiones en compuerta | Integración de fuerza y momento | F = 23838,3 N; hcp = 1,48889 m |
| 6 — Flujos laminares | Contraflujo local en Couette–Poiseuille | Condición -3 < P < -1 para caudal neto positivo y velocidad invertida | q = 1,3333e-4 m²/s; tau(0) = -4 Pa |
| 12 — Transporte, continuidad, Bernoulli | Pitot y propagación de sensibilidad | Hipótesis de Bernoulli, diferencial de V | V = 20 m/s; cota lineal relativa 1,25 % |
| 14 — Navier–Stokes | Esfuerzo viscoso no equivale a divergencia viscosa | Solución exacta extensional 2D, divergencia nula y tensiones no nulas | delta p = -100 Pa; tau_xx = +0,004 Pa |

Cada sección expone hipótesis de aplicación, signos, dimensiones, condiciones límite, ejemplo original y ejercicio de autocomprobación. Se han incluido mediante `\\input` en `latex/manual.tex` para conservar la plantilla común, sin replicar problemas protegidos.

## Matriz orientativa de lecturas por temas del MANUAL — no equivale a mapa oficial ULE

| Capítulos | Base recomendada | Naturaleza |
| --- | --- | --- |
| 1–2: mecánica clásica | Taylor; Boas | bases previas |
| 3–4: medio continuo y cinemática | Shaughnessy; White cap. 1 | fundamentos |
| 5: estática de fluidos | White cap. 2 | base |
| 6: Couette y Poiseuille | White cap. 4 y 6; Shaughnessy | base |
| 7–9: flujo externo, oscilaciones y control | White cap. 3 y 7; Tritton (pendiente de cotejo) | aplicación |
| 10: semejanza | White cap. 5 | base |
| 11: cálculo vectorial | Boas cap. 6 | prerrequisito |
| 12–14: balances, esfuerzo y Navier–Stokes | White cap. 3–4; Shaughnessy cap. 11 | base |
| 15–16: adimensionalización y flujos geofísicos | White cap. 5; Tritton (pendiente de cotejo) | ampliación, priorización curricular pendiente |

## Gates antes de publicar nueva edición

- Compilar **manual, problemas y simulacros** con `python3 scripts/build-studium-books.py mecanica-fluidos --check` y luego sin `--check`.
- Ejecutar `python3 books/mecanica-fluidos/scripts/check_refuerzo_2026.py` y `python3 books/mecanica-fluidos/scripts/check_fluid_bank.py` si hay dependencias.
- Inspeccionar cada página de las cuatro nuevas secciones (saltos, etiquetas, tablas, dimensiones).
- Leer la **guía docente completa y firmada** de 2026-2027, y documentar temas obligatorios, prácticas, criterios de examen y prioridades. No confundir el plan del manual con la guía.
- Revisar todas las afirmaciones de alto riesgo; asignar localizador de fuente preciso, derivación reproducible, y revisión independiente. Tritton y Taylor requieren cotejo visual por páginas.
- Mantener los cinco PDF originales **fuera del repositorio**, por derechos de autor.
- No crear un release final ni declarar validación académica completa sin completar los gates.
