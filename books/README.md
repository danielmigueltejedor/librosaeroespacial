# Libros

Cada libro conserva una carpeta estable bajo `books/<slug>/`. Las cinco carpetas contienen las ediciones actuales de Studium. Las antiguas ediciones AeroBooks de Estructuras y Fluidos permanecen en el historial de Git.

| Libro | Carpeta | Compilador |
| --- | --- | --- |
| Teoría de Estructuras (segunda edición completa, v3) | [estructuras-aeroespaciales](estructuras-aeroespaciales/) | `python3 scripts/build-studium-books.py estructuras-aeroespaciales` |
| Mecánica de Fluidos (revisión fase 6) | [mecanica-fluidos](mecanica-fluidos/) | `python3 scripts/build-studium-books.py mecanica-fluidos` |
| Turbomáquinas | [turbomaquinas](turbomaquinas/) | `python3 scripts/build-studium-books.py turbomaquinas` |
| Tecnología Aeroespacial | [tecnologia-aeroespacial](tecnologia-aeroespacial/) | `python3 scripts/build-studium-books.py tecnologia-aeroespacial` |
| Motores Cohete | [motores-cohete](motores-cohete/) | `python3 scripts/build-studium-books.py motores-cohete` |

Estructuras y Fluidos contienen un manual cada uno. Las otras tres colecciones contienen manual, problemas resueltos y simulacros: once PDF en total. Los comandos se ejecutan desde la raíz del repositorio. Los PDF generados no se versionan como fuentes; sus entregas se guardan en Releases y las recompilaciones en los artefactos de GitHub Actions.

No se crean carpetas `v2`, `final-final` ni copias de trabajo privadas. Las fuentes y recursos editables se versionan directamente. La integración académica de las importaciones en AeroBooks queda explícitamente pendiente; no se fabrica un `book.toml`, un ledger ni aprobaciones para simularla.
