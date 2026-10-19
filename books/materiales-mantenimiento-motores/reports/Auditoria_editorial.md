# Auditoría editorial

Fecha: 18 de octubre de 2026. Edición íntegra de estudio EN REVISIÓN.

## Diseño y referencias

Se inspeccionaron las portadas y páginas interiores localizadas de Fluidos, Estructuras, Turbomáquinas, Tecnología Aeroespacial y Motores Cohete. El registro referencias-diseno.json identifica las rutas y huellas. Se mantiene el diseño final de la colección: A4, margen 25 mm, Latin Modern 10 pt, jerarquía serif, cabeceras alternas, ecuaciones/figuras/cuadros por capítulo y cajas azules, ocres, violetas y verdes. La referencia fotográfica de portada procede de las ediciones finales; la copia de Estructuras localizada conserva portada de borrador y no se toma como portada final.

La fotografía GEnx de Olivier Cleynen está en los tres documentos con encuadre proporcional, crédito y licencia CC BY-SA 3.0. Se conserva el original y el crédito de su adaptación de encuadre.

## Documentos completos

Manual: 108 páginas PDF, 25 capítulos, 23 figuras originales, cuatro apéndices, bibliografía y referencias recomendadas. Cuaderno: 39 páginas PDF, 35 problemas originales y 16 casos con resolución. Simulacros: 20 páginas PDF, seis pruebas y 24 preguntas, con soluciones en parte separada. Los números incluyen portadas, índices y aperturas. La extensión orientativa 300–450 no se usa como cuota: no se añaden hojas de relleno.

Los 35 problemas imprimen enunciado, datos, incógnitas, modelo, hipótesis, ecuaciones, desarrollo algebraico, sustitución, resultado, unidades, interpretación, verificación y limitaciones. Los casos conservan documentación disponible, fecha, norma, análisis, resultado académico y límites. Los seis simulacros tienen puntuación y tiempos didácticos explícitos.

## Comprobaciones

Los tres PDF compilan con latexmk/pdfLaTeX, sin Overfull, referencias indefinidas ni advertencias TeX en los registros finales. Se revisaron portadas, índices, capítulos, fórmulas, cuadros y apéndices. Se renderizaron todas las páginas y se examinaron sus paneles de contacto; se inspeccionaron ampliaciones de ecuaciones, problemas, figuras y los últimos cambios. Se corrigieron recortes de cajas de flujo, etiquetas largas, espacios en los bancos de texto y finales aislados. Las aperturas de parte son deliberadas; no se fuerzan páginas pares vacías.

Una copia limpia del proyecto recompiló los tres documentos con el mismo texto extraído y el mismo número de páginas, sin desbordamientos. El resultado se conserva en reproducibility.json y registros de cada compilación. La comprobación de reproducción es de texto y estructura, no de igualdad binaria de PDF con fechas/identificadores de generación. El compilador integrado se comprobó adicionalmente; una ejecución quedó stale-project por cambios concurrentes del entorno y se repitió sobre los archivos estables.

## Entrega y límites

Se incluyen fuentes LaTeX, figuras vectoriales y PNG, bancos editables, scripts, proyecto Studium, commit fijado, cuatro auditorías, matriz de cobertura, inventario de ecuaciones y registro de verificaciones. No se redistribuyen archivos privados protegidos de entrada ni entornos de ejecución. Las fuentes públicas se documentan con URL y huella. El ZIP mantiene el estado EN REVISIÓN y los bloqueos nativos, sin declarar auditoría experta independiente ni autorización de mantenimiento.
