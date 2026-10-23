# Informe editorial

La maquetación se rehízo tomando como referencia visual el volumen de Turbomáquinas aportado por el usuario. Se aplicó a los tres documentos: A4, márgenes de 25 mm, Latin Modern de 10 puntos, títulos negros, cabeceras clásicas con número de página y sección, pies de figura en negrita y ejemplos resueltos en recuadros crema con título ocre. La portada usa fotografía a sangre, una banda superior clara y una zona inferior azul oscuro con acentos turquesa. No se copió contenido de ese volumen.

La fotografía de NASA es provisional, está acreditada y puede sustituirse por la imagen que facilite el usuario. La etiqueta editorial de revisión se retiró por petición del usuario; esta decisión no cambia las comprobaciones registradas. Los archivos `latex/preamble.tex` y `scripts/house_style.py` conservan la identidad visual; `content-layout` se deriva de `content` y no sustituye a la fuente científica. El adaptador reúne ecuaciones consecutivas y coloca la puntuación dentro de ellas para evitar signos aislados.

La entrega contiene:

| Documento | Páginas A4 | Contenido |
|---|---:|---|
| Manual | 164 | 25 capítulos en diez partes, apéndices y bibliografía |
| Problemas | 38 | P01–P30 y soluciones de los ocho simulacros |
| Simulacros | 7 | Tres enunciados originales, sin las soluciones del cuaderno |

El manual incluye 29 casos desarrollados, 107 ejercicios propuestos con orientación de respuesta y 27 figuras originales. El proyecto nativo estima alrededor de 51 000 palabras. El objetivo orientativo de 300–450 páginas **no se alcanza** en esta maquetación compacta. No se añadieron páginas vacías o duplicaciones para simularlo. La profundidad de varios capítulos sigue siendo un aspecto a valorar en la revisión académica; la presencia de todos los temas no la resuelve por sí sola.

Los tres PDF se compilaron en tres pasadas. Los controles finales dan cero referencias indefinidas, cero marcadores `??`, cero desbordamientos horizontales, cero advertencias de caracteres ausentes y cero destinos duplicados. Todas las páginas tienen tamaño A4. Los resultados completos y SHA-256 figuran en `final-quality.json`.

Se rasterizaron y revisaron portada, páginas de texto, derivaciones, tablas, figuras, ejemplos, apéndices y simulacros. La selección de páginas está en `evidence/visual-review-selection.json`. Es una inspección representativa, no una lectura académica exhaustiva de cada página. La revisión gráfica y la compilación no cambian el estado científico del libro.

La compilación trasladada reproduce paginación y texto de los tres archivos, usando las dependencias ya instaladas. Los fuentes LaTeX y gráficos necesarios se incluyen. Los originales privados de apuntes y exámenes quedan excluidos del paquete.
