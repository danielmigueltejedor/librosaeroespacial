# Entrega de Mecánica de Vuelo — Studium

Fecha: 19 de octubre de 2026. Edición EN REVISIÓN. Revisión experta independiente pendiente.


Se entregan tres volúmenes editoriales completos (143, 50 y 31 páginas), fuentes LaTeX, 26 figuras originales, 84 ejercicios resueltos, seis simulacros, scripts y XML originales, CSV de ejecuciones reales, bibliografía y cinco auditorías. El manual tiene 23 capítulos y 18 apéndices, incluido formulario y guía de reproducción.

## Evidencia y estado

- Programa ULE 2026/2027 contrastado, ampliación dinámica identificada.
- Python: 44 controles de modelos, ocho simbólicos complementarios, 151 del banco y 158 de talleres/simulacros/CSV, correctos en sus alcances.
- Studium: 1193 párrafos, 84 problemas comprobados y 284 cálculos vigentes; diez derivaciones y cuatro contratos. Borrador nativo compilado de 219 páginas, separado de los tres volúmenes finales.
- Framework probado: 1072 pruebas correctas y dos omitidas. Commit y herramientas en versions.json, sin cambios al repositorio principal.
- JSBSim realmente ejecutado: 44 trims, tres pasos temporales T6, trayectoria XML, crucero y dos autonomías hasta agotamiento.

Los informes nativos mantienen bloqueos y autoridad pendiente. El libro NO está científicamente validado ni liberado por Studium; véanse A–E, LIMITACIONES y la incidencia MATH-001. Las comprobaciones numéricas no equivalen a revisión experta o validación experimental.

## Reproducir y revisar

Empiece por README.md. Los tres principales LaTeX compilan con sus figuras locales sin el material privado. rebuild.sh regenera cálculos, simulaciones y figuras con las dependencias indicadas. La instantánea del framework conserva su licencia y commit; los modelos externos se descargan y verifican por commit.

El ZIP excluye runtime, historial Git, OCR privado, PDF protegidos y archivos administrativos. Conserva los registros nativos, fuentes originales, evidencias, informes y CSV. Un manifiesto SHA-256 permite comprobar los miembros; la integridad del ZIP y la presencia de sus componentes se verifican antes de entrega.

Se descomprimió el paquete en otro directorio: los tres documentos recompilaron con igual número de páginas y texto extraído idéntico. El proyecto Studium trasladado se abrió y su interfaz matemática aceptó una comprobación dimensional. No se volvieron a ejecutar las simulaciones inalteradas para esta prueba de traslado.
