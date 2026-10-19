# Libros

Cada libro conserva una carpeta estable bajo `books/<slug>/`. Las cinco carpetas contienen las ediciones actuales de Studium. Las antiguas ediciones AeroBooks de Estructuras y Fluidos permanecen en el historial de Git.

| Libro | Carpeta | Compilador |
| --- | --- | --- |
| Teoría de Estructuras (segunda edición completa, v3) | [estructuras-aeroespaciales](estructuras-aeroespaciales/) | `python3 scripts/build-studium-books.py estructuras-aeroespaciales` |
| Mecánica de Fluidos (revisión fase 6) | [mecanica-fluidos](mecanica-fluidos/) | `python3 scripts/build-studium-books.py mecanica-fluidos` |
| Turbomáquinas | [turbomaquinas](turbomaquinas/) | `python3 scripts/build-studium-books.py turbomaquinas` |
| Tecnología Aeroespacial | [tecnologia-aeroespacial](tecnologia-aeroespacial/) | `python3 scripts/build-studium-books.py tecnologia-aeroespacial` |
| Motores Cohete | [motores-cohete](motores-cohete/) | `python3 scripts/build-studium-books.py motores-cohete` |

Las cinco colecciones contienen manual, problemas resueltos y simulacros: quince PDF en total. Estructuras reúne los 105 ejercicios de su manual y cuatro simulacros de entrenamiento por selección de veinte casos del mismo banco. Fluidos añade 48 problemas resueltos, siete talleres y cuatro simulacros originales. Los comandos se ejecutan desde la raíz del repositorio. Los PDF generados no se versionan como fuentes; sus entregas se guardan en Releases y las recompilaciones en los artefactos de GitHub Actions.

No se crean carpetas `v2`, `final-final` ni copias de trabajo privadas. Las fuentes y recursos editables se versionan directamente. La integración académica de las importaciones en AeroBooks queda explícitamente pendiente; no se fabrica un `book.toml`, un ledger ni aprobaciones para simularla.

## Importación en curso: Mecánica de Vuelo

La nueva asignatura se está preparando en la rama `import/mecanica-vuelo`; sus tres volúmenes y recursos editoriales se incorporarán antes de completar la importación. No se fusionará esta rama sin las fuentes y las figuras.

## Importación en curso: Materiales y Mantenimiento de Motores Aeroespaciales

La rama `import/materiales-mantenimiento-motores` prepara una sexta asignatura con manual, cuaderno de problemas y simulacros. La importación completa está pendiente de añadir los fuentes y recursos desde el ZIP saneado; no fusionar hasta superar la compilación y revisar los derechos. El libro conserva la calificación editorial **EN REVISIÓN**, sin aprobación académica independiente.
