# MATMO — auditoría inicial de materiales de examen (24-10-2026)

**Alcance de esta contribución.** Se examinaron las dos entregas PDF aportadas en la conversación (ejercicios de materiales de 10 páginas; preguntas de teoría de 17 páginas), se inventariaron ambos ZIP de mantenimiento, se examinó el programa de la asignatura y se contrastaron conceptos con documentación abierta. Esto **no** es un cotejo exhaustivo de todas las páginas de los PDF regulatorios (más de 500 páginas acumuladas) ni una revisión académica independiente. Las preguntas del complemento son originales, no transcripciones.

## Materiales recibidos; no redistribuir
- `wuolah-premium-Ejercicios-materiales.pdf` (10 pp): ejercicios de fractura y tamaño crítico de grieta, concentración de tensiones, vida a fatiga y curvas S--N, integración de Paris, y álabe en fluencia por carga centrífuga.
- `wuolah-premium-preguntas-de-teoria.pdf` (17 pp): test y notas de materiales, algunas respuestas erróneas o excesivamente generalizadas. Es **fuente de temas y estilo de examen, no autoridad científica**.
- `Mantenimiento-MATMO-1-temas.zip`: presentación de la asignatura, introducción, marco normativo civil y militar, Parte 21/CS, programa de mantenimiento, HTML resumen y BOE-A-2022-21487.
- `Mantenimiento-MATMO-2-ARC-normativa-ADs.zip`: presentación ARC, copias históricas de 748/2012, 1321/2014 y 2018/1139, más ocho ficheros Excel de listados de AD por modelo de aeronave (CESSNA, TB, PA-28).
- Guía docente ULE 2026-2027, asignatura 0710341, 4.º curso, 6 ECTS: https://www.unileon.es/estudiantes/oferta-academica/grados/grado-en-ingenieria-aeroespacial/plan-estudios?cursoa=2026&id=0710341&te=G y https://guiadocenteapi.unileon.es/syllabuses/downloadPdf/2026-2027/0710341 . El repositorio contiene previamente `reports/Contraste_guia_docente.md`.

## Errores o generalizaciones problemáticas en los apuntes de alumnos

| Tema en apuntes | Juicio | Corrección para estudiar |
|---|---|---|
| Aleación 8090 identificada como níquel | Incorrecto | 8090 es aluminio-litio. Fuente: NIST, Aluminum and Aluminum Alloys (Davis), y ASM Handbook Vol. 2. |
| Temperatura < 200 °C excluye los metales | Incorrecto | La temperatura no permite descartar universalmente materiales metálicos; combinar requisitos térmicos y mecánicos. |
| La matriz nunca soporta carga en compuestos | Incorrecto | Transfiere esfuerzos, soporta cargas en determinadas direcciones y protege el refuerzo. La fracción de carga depende del modelo. |
| Los termoestables serían tipo de termoplástico | Incorrecto | Son familias distintas; curado/reticulación frente a fusión-reprocesado. |
| Aleaciones de aluminio por moldeo nunca reciben tratamiento térmico | Incorrecto | Existen aleaciones de fundición tratadas por solución y envejecimiento, por ejemplo 356.0-T6 (SAE AMS4260H). |
| Fluencia en monocristal únicamente por difusión | Incorrecto | Puede operar fluencia de dislocaciones; se suprimen efectos de borde de grano, no todos los mecanismos. |
| GLARE siempre de bajo módulo | Generalización insegura | Respuesta direccional dependiente de orientación y secuencia de capas; comparar contra referencia definida. |
| Una técnica NDI única para medir cualquier grieta de 5 mm | Indeterminado sin contexto | Debe conocerse material, orientación, geometría, accesibilidad, resolución, POD y procedimiento cualificado. |
| Fenólicas únicas capaces de cumplir requisitos de fuego de interiores | Generalización | Debe evaluarse sistema, formulación y certificación del producto; no solo resina aislada. |
| FCC nunca puede presentar fractura frágil transgranular | Generalización insegura | Mecanismo depende de material, microestructura, ambiente, temperatura, carga y condiciones; evitar absolutos. |
| Todas las aeronaves comparten estructura idéntica de piel y superficies de control | Incorrecto | Las selecciones reales dependen de modelo, misión, zona y configuración. |
| BOE-A-2022-21487 como base de la normativa militar de aeronavegabilidad | Incorrecto | Es convocatoria de personal: no sustituye RD 866/2015 y normativa militar aplicable. |

## Correspondencia de los nuevos materiales con el temario

- Banco de teoría, T01–T20: materiales, microestructura, propiedades, fractura, fatiga, fluencia, compuestos e inspección — principalmente capítulos 1–11.
- Banco de teoría, T21–T36: AD, Parte 21, Parte 145/66/147, CAMO, ARC, documentación, mantenimiento y tendencias de motor — principalmente capítulos 12–24.
- Problemas PE01–PE06: cálculo de fractura, fatiga, Paris, Norton, tensión térmica y ultrasonidos.
- Problemas PE07–PE08: vencimientos de tareas, fiabilidad y decisión documental.

## Controles y límites
- Cálculo de PE01–PE08 contrastado de manera independiente con Python; resultados numéricos y unidades principales registrados en las soluciones.
- Los ejercicios son **académicos**; no autorizan mantenimiento, prórrogas, inspecciones ni límites de vida reales.
- La información regulatoria debe cotejarse con el texto oficial de la fecha del examen y del caso; separar publicación, vigencia y aplicabilidad.
- La compilación del volumen completo, la inspección gráfica de todas sus páginas y la revisión experta independiente quedan pendientes. No marcar `RELEASED`.

## Fuentes abiertas verificables
1. Universidad de León, ficha 0710341 (curso 2026-2027): https://www.unileon.es/estudiantes/oferta-academica/grados/grado-en-ingenieria-aeroespacial/plan-estudios?cursoa=2026&id=0710341&te=G
2. MIT OpenCourseWare, Roylance, Mechanics of Materials: https://ocw.mit.edu/courses/3-11-mechanics-of-materials-fall-1999/pages/modules/
3. FAA, Aviation Maintenance Technician Handbooks General/Airframe/Powerplant (2023): https://www.faa.gov/regulations_policies/handbooks_manuals/aviation
4. EASA, Reglamento (UE) 1321/2014, Continuing Airworthiness: https://www.easa.europa.eu/en/regulations/continuing-airworthiness
5. EASA, CS-E Engines, Amendment 9 (25-09-2026): https://www.easa.europa.eu/en/document-library/certification-specifications/group/cs-e-engines
6. NIST, Aluminum and Aluminum Alloys (Davis): https://materialsdata.nist.gov/bitstream/handle/11115/173/Aluminum%20and%20Aluminum%20Alloys%20Davis.pdf
7. SAE AMS4260H, A356.0-T6 castings heat treated: https://saemobilus.sae.org/standards/ams4260h-aluminum-alloy-investment-castings-70si-032mg-3560-t6-solution-precipitation-heat-treated
8. Revisión de microestructuras de titanio (acceso abierto): https://pmc.ncbi.nlm.nih.gov/articles/PMC10780041/

## Pendientes prioritarios antes del 29-10-2026
1. Verificar los porcentajes y formato concretos del examen con indicaciones docentes recientes; la guía da evaluación general, no asegura formato de la prueba inmediata.
2. Completar contraste lámina a lámina de los dos ZIP y cuestionarios derivados con evidencias por página, de forma que la cobertura se pueda demostrar, no prometer al 100 %.
3. Añadir más casos de respuesta abierta sobre licencias, Parte M/ML, ARC y aplicabilidad de AD con cambios de legislación 2026.
4. Compilar los tres PDF del proyecto, revisar sumarios, numeración, saltos y soluciones, ejecutar tests del repositorio.
