# Libros

Cada libro conserva una carpeta estable bajo `books/<slug>/`. Los proyectos originales AeroBooks y las importaciones de Studium conviven sin sobrescribir sus fuentes ni sus estados de auditoría.

| Libro | Carpeta | Compilador |
| --- | --- | --- |
| Estructuras Aeroespaciales | [estructuras-aeroespaciales](estructuras-aeroespaciales/) | `aerobooks build estructuras-aeroespaciales` |
| Mecánica de Fluidos | [mecanica-fluidos](mecanica-fluidos/) | `aerobooks build mecanica-fluidos` |
| Turbomáquinas | [turbomaquinas](turbomaquinas/) | `python3 scripts/build-studium-books.py turbomaquinas` |
| Tecnología Aeroespacial | [tecnologia-aeroespacial](tecnologia-aeroespacial/) | `python3 scripts/build-studium-books.py tecnologia-aeroespacial` |
| Motores Cohete | [motores-cohete](motores-cohete/) | `python3 scripts/build-studium-books.py motores-cohete` |

Cada importación Studium contiene tres volúmenes: manual, problemas resueltos y simulacros. Los comandos se ejecutan desde la raíz del repositorio. Los PDF generados no se versionan como fuentes; sus entregas se guardan en Releases y las recompilaciones en los artefactos de GitHub Actions.

No se crean carpetas `v2`, `final-final` ni copias de trabajo privadas. Las fuentes y recursos editables se versionan directamente. La integración académica de las importaciones en AeroBooks queda explícitamente pendiente; no se fabrica un `book.toml`, un ledger ni aprobaciones para simularla.
