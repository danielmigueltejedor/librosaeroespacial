# Auditoría editorial

Los veintiún volúmenes usan `shared/latex/studium-editorial.tex` y `studium-cover.tex`. Vuelo y Materiales conservan únicamente sus adaptadores de disciplina. Se comparten A4, Latin Modern, márgenes, jerarquía, encabezados, recuadros, numeración y retícula de portada.

Las portadas emplean fotografía, franja blanca, título vectorial, categoría, Universidad de León, titulación, año y edición. El título largo de Materiales usa 26/29 puntos dentro de la misma retícula. Se corrige el sistema de coordenadas de portada a puntos PDF (`bp`). Las imágenes mantienen proporción; no se estiran. Las tres portadas de Vuelo comparten exactamente plantilla y fotografía NASA X-29.

Los originales de Estructuras y Turbomáquinas se localizaron en `figures/cover.jpeg` y sus configuraciones editoriales antes de intervenir. Su procedencia seguía pendiente, por lo que las portadas actuales incorporan fotografías documentadas. Los originales históricos se conservan.

Los anexos de auditoría de Estructuras y Fluidos separan sus registros con párrafos reales. Se aclara que los estados importados son históricos; la existencia de dos documentos no demuestra apoyo semántico. Se conservan identificadores, citas, enunciados, figuras y contenido científico previo salvo las correcciones documentadas.

Los logs se revisan tras tres pasadas efectivas. `pdf-checks.json` revisa todas las páginas en busca de glifos de sustitución, texto fuera de caja, destinos internos inválidos y páginas vacías. `visual-samples.json` identifica páginas renderizadas; su aprobación solo se registra tras mirar las imágenes. Se revisan muestras de portadas, índices, capítulos, matemáticas, figuras, problemas, apéndices, bibliografía y cierre, cuando existen.

La inspección es por muestreo. No acredita cada ángulo, flecha o escala de todas las figuras. Se conservan casos heredados de `fitmath`; esta revisión no afirma que se hayan sustituido todos por divisiones automáticas de ecuaciones largas.
