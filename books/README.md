# Libros

Cada asignatura conserva una carpeta estable bajo `books/<slug>/`. La colección actual contiene siete asignaturas y veintiún volúmenes Studium. Las antiguas ediciones AeroBooks de Estructuras y Fluidos permanecen en el historial de Git.

| Libro | Carpeta | Compilador |
| --- | --- | --- |
| Teoría de Estructuras | [estructuras-aeroespaciales](estructuras-aeroespaciales/) | `python3 scripts/build-studium-books.py estructuras-aeroespaciales` |
| Mecánica de Fluidos | [mecanica-fluidos](mecanica-fluidos/) | `python3 scripts/build-studium-books.py mecanica-fluidos` |
| Turbomáquinas | [turbomaquinas](turbomaquinas/) | `python3 scripts/build-studium-books.py turbomaquinas` |
| Tecnología Aeroespacial | [tecnologia-aeroespacial](tecnologia-aeroespacial/) | `python3 scripts/build-studium-books.py tecnologia-aeroespacial` |
| Motores Cohete | [motores-cohete](motores-cohete/) | `python3 scripts/build-studium-books.py motores-cohete` |
| Mecánica de Vuelo | [mecanica-vuelo](mecanica-vuelo/) | `python3 scripts/build-studium-books.py mecanica-vuelo` |
| Materiales y Mantenimiento de Motores Aeroespaciales | [materiales-mantenimiento-motores](materiales-mantenimiento-motores/) | `python3 scripts/build-studium-books.py materiales-mantenimiento-motores` |

Cada asignatura tiene manual, cuaderno de problemas y simulacros. Los comandos se ejecutan desde la raíz del repositorio. Los PDF generados no se versionan como fuentes; sus entregas se guardan en Releases y las recompilaciones en los artefactos de GitHub Actions.

No se crean carpetas `v2`, `final-final` ni copias de trabajo privadas. Las fuentes y recursos editables se versionan directamente. La integración académica de las importaciones en AeroBooks queda explícitamente pendiente; no se fabrica un `book.toml`, un ledger ni aprobaciones para simularla. Los libros conservan el estado **EN REVISIÓN** y no se declaran científicamente certificados.

## Fotografías de portada de Mecánica de Vuelo

Los tres volúmenes de Vuelo usan fotografías NASA distintas con la misma plantilla: NASA AD-1 en vuelo para el manual, cabina del X-29 para problemas y X-29 en viraje para simulacros. Procedencia y licencias en `assets/cover-photo.json` y `assets/COVER-IMAGE.md`.
