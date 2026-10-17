# Verificación científica — edición 0.1

**Estado: edición en revisión. La auditoría académica integral NO está superada.**

El libro está alineado con la guía docente 2026/2027 aportada y leída, no solo con una guía de otro curso. Los diez PDF de entrada suman 173 páginas: 149 de documentos oficiales aportados (incluida la guía de cinco páginas) y 24 de material estudiantil privado. No se ha validado criptográficamente la firma de la guía.

## Comprobaciones realizadas

- Studium: 150 problemas vigentes con comprobación de pasos; cuatro niveles, 72 resueltos, 72 de transferencia y seis de simulacro.
- Evaluación adicional con cantidades y unidades y controles de dominio: 509 comprobaciones; 0 fallos pendientes.
- Identidades, derivadas e integrales: 15 comprobaciones simbólicas satisfactorias de 15. Los fallos iniciales por parámetros no declarados se corrigieron y se conservan como historial, no como fallos matemáticos pendientes.
- Residuos seleccionados de conservación: 8 controles, todos satisfactorios; ocho no representan una cobertura exhaustiva de todas las leyes para cada problema.
- Casos completos por estaciones: dos; conservan energía, masa y rotalpía bajo sus hipótesis. Eficiencias resultantes: compresor 0.891732, turbina 0.919450.
- Modelos registrados de ejemplo: 18 con comprobación dimensional. Cuando hay exponentes dependientes de gamma o eficiencia politrópica, se especializan explícitamente esos parámetros para el control de unidades; la fórmula general queda almacenada.
- Práctica de geometría: 48 comprobaciones de extremos, tangentes, espesor normal y finitud; 0 fallos. Se generan 1.452 puntos para cuatro configuraciones y tres radios.
- Figuras de capítulo: 18 fuentes originales TikZ ejecutadas y compiladas por Studium; gráficos calculados identificados como modelos y mapa de operación marcado como esquema. Hay seis pares adicionales de diagramas de enunciado/solución, con respuestas solo en el segundo.

## Límites y hallazgos

La reproducción numérica no se denomina validación física. Las dos evaluaciones numéricas proceden de la misma ecuación declarada y no constituyen dos experimentos ni dos modelos físicos independientes. Los residuos comprueban balances seleccionados en modelos idealizados.

C17-04-P tiene datos de ensayo incompatibles con una compresión adiabática del modelo: el rendimiento calculado supera uno. La solución lo diagnostica expresamente. El control de admisibilidad verifica ese diagnóstico; no acepta un estado físicamente imposible como diseño.

Auditoría integrada de Studium: {'ERROR': 0, 'WARNING': 146, 'REVIEW_REQUIRED': 564, 'INFO': 90}. Cero ERROR en esa herramienta no significa aprobación: siguen las advertencias y la revisión requerida. La fundamentación formal automática de parte de las fórmulas sigue incompleta; consulte studium_equation_report.json y studium_book_quality_audit.json para cada párrafo y registro.

Los fragmentos registrados identifican procedencia y principios. Tener fuentes de dos instituciones no demuestra que ambas respalden cada dato original. Las soluciones son originales y sus números se calculan; no se atribuyen a las fuentes consultadas. Los fragmentos de imágenes leídos no se convierten en fórmulas verificadas automáticamente.

Los primeros registros de cálculo de las tablas por estaciones incluyen 25 comprobaciones débiles de ida y vuelta de formato (valor por uno). Se conservan en el historial por transparencia y se excluyen de los recuentos científicos de este informe. El programa final reproduce fórmulas reales con sus operandos para temperaturas, presiones, remanso relativo y áreas.

## Revisión experta requerida

1. Revisar las hipótesis de las deducciones teóricas y cerrar su fundamentación formal en el registro de ecuaciones.
2. Evaluar la aplicabilidad de las correlaciones docentes de Carter, carga de cascada y difusión para perfiles y regímenes concretos. Los coeficientes no se universalizan.
3. Revisar geometrías Hermite: radios de bordes, autocruces, garganta, apilamiento y comportamiento viscoso. Las comprobaciones realizadas no equivalen a diseño aerodinámico validado.
4. Revisar tensiones combinadas, concentración, fluencia, fatiga y vida. Los admisibles no se toman de curvas históricas sin especificación.
5. Revisar transferencia térmica, presiones de refrigerante, mezcla y balance de caudales de un motor real. Los modelos de pared y caudal mínimo son docentes.
6. Calibrar cualquier mapa o modelo de estabilidad si se pretende usarlo para una máquina; aquí no hay mapas experimentales ni línea de bombeo predicha.
7. Contrastar dificultad y rúbricas de simulacros con el criterio del profesorado. Son originales y no oficiales.
8. Comprobar en el ejemplar el año de la edición india de Hill y Peterson: la guía indica 2010 y la lista editorial consultada 2009 para el mismo ISBN.

## Evidencias

Los JSON conservan entradas, resultados, unidades, estados y límites. El motor Studium no se modificó. Se fijó main 08ef1f42892d6a69ad0bbde8816bc3e18fba26f7, versión 1.0.0a1; no se encontró una publicación estable posterior. Antes de redactar pasaron 85 pruebas básicas. El borrador permanece sin liberar.
