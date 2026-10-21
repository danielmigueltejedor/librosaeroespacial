# Corrección de formato de la revisión 3

Se corrige el formateador de Studium para que la negrita y la cursiva abarquen código en línea, fórmulas e identificadores. El ejemplo de la guía Rust/vol03 y los casos de Go, Kotlin, Swift, Bash y Haskell ya no imprimen sus delimitadores Markdown. Las iniciales resaltadas de STRIDE también conservan su formato.

La integral mantiene 364 páginas, 75 capítulos y 332 actividades; sus 539 enlaces internos se comprueban tras regenerarla. Se revisan 827 textos activos y 2718 regiones literales. Cinco fixtures extraídos de un PDF real comprueban los literales y el formato mixto. Las únicas tres líneas de la integral que conservan dobles asteriscos son operadores válidos de Python: dos exponentes y unos argumentos por palabra clave.

Se inspeccionan visualmente las páginas indicadas en prose-formatting-review.json. Las pruebas del repositorio de libros pasan: 87 pruebas y siete subtests. Las pruebas específicas del formateador y matemáticas pasan: 53 casos. El CI de la corrección de Studium está en https://github.com/danielmigueltejedor/studium/pull/82 y ejecuta la suite completa en Python 3.11 y 3.12.

Esta revisión cambia la presentación y añade controles de formato. No altera el código de los ejercicios, sus datos científicos ni los estados de revisión bibliográfica o académica. Los 21 PDF de ingeniería se reutilizan con sus hashes y procedencia de la revisión 2; únicamente se regeneran los PDF de programación. Los informes anteriores conservan el alcance de sus respectivas pasadas.
