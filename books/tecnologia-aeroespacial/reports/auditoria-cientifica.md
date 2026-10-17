# Auditoría científica y estado de revisión

**EN REVISIÓN. No existe aprobación académica humana ni liberación científica.**

Este informe separa cuatro estados: **VERIFICADO**, comprobación concreta bajo hipótesis y alcance definidos; **REPRODUCIDO**, cálculo o compilación repetidos; **PENDIENTE DE REVISIÓN**, soporte o evaluación todavía incompletos; **ERROR DETECTADO**, discrepancia registrada y corregida o limitación pendiente. Una compilación satisfactoria no prueba la validez científica del texto.

## Verificaciones realizadas

Se ejecutaron 53 comprobaciones con resultado satisfactorio (`scientific-tests.json`). Incluyen derivadas y límites de la atmósfera por capas, límite isotermo, mínimos de resistencia y potencia, diferencias entre eficiencia de envergadura y Oswald, límite de Pitot a baja compresibilidad, integral del cohete, energía orbital, análisis dimensional con Pint, continuidad ISA, comparación tabulada a 11 km, integración hidrostática por ODE, rechazo de estados fuera de dominio, inversión de Pitot, raíces empuje-resistencia y envolvente del cono de Mach. También se comprueban los cuatro óptimos de alcance/autonomía, unidades del consumo y un balance diferencial de Breguet. Un caso deliberadamente incorrecto reproduce el error de agrupación de la página NASA y debe ser rechazado.

Los 30 problemas P01–P30 tienen comprobación dimensional y una segunda ruta numérica o de balance, con tolerancia relativa inferior a 1e-7 (`bank-crosschecks.json`). Son rutas alternativas dentro del mismo modelo, no validación experimental de una aeronave. Los capítulos cuentan además con comprobaciones concretas conservadas en `comprobaciones-fundamentos.json`, `comprobaciones-aerovuelo.json` y `comprobaciones-tecnologias.json`.

## Evidencia real en Studium

Se registraron los 25 capítulos, fuentes, extractos, problemas, operaciones, notación y figuras mediante su API/MCP. Se compiló también su borrador nativo. No se modificó el código del framework para forzar estados favorables.

La última revisión nativa declara:

- Estado: **blocked**; `released=false`; aprobación humana no registrada.
- Auditoría de calidad: 0 ERROR, 422 WARNING, 1013 REVIEW_REQUIRED y 27 INFO.
- Afirmaciones de ecuaciones: 960; verificadas por el informe nativo: 7; no comprobables automáticamente: 318; sin soporte suficiente: 631; contradichas o fallidas: 0.
- Ecuaciones importantes sin resolver en esa auditoría: 233.
- Contratos científicos nativos aceptados: **0**. La cobertura no se presenta como completa.

`studium_equation_report.json` es una primera página de resultados de un inventario de 1210 expresiones de varias clases; no debe confundirse ese total con las 960 afirmaciones usadas por la puerta de revisión. Su campo `next_offset` señala que hay más páginas. El inventario editorial de entornos equation/align se conserva además en `evidence/equation-inventory.json`, con estado de revisión pendiente, sin asignarles verificación masiva.

De 30 operaciones adicionales registradas, 28 se reprodujeron nativamente y dos quedaron sin anclaje suficiente por las reglas de procedencia de enteros pequeños. Las 30 soluciones estructuradas conservan sus resultados aritméticos; cuatro modelos con exponentes simbólicos no pasan la comprobación dimensional nativa por una limitación del motor. Las dimensiones completas se comprobaron por separado con Pint. Los modelos angulares P07 y P27 se corrigieron para operar en radianes y convertir después a grados; los registros anteriores se archivaron, sin ocultar la corrección.

Las 27 figuras se generaron externamente y se revisaron visualmente. El ejecutor protegido de Studium no pudo reproducir su cadena de importación de Matplotlib: su estado nativo permanece pendiente. No se debilitó esa protección.

## Errores corregidos y límites abiertos

Las discrepancias docentes y de NASA figuran en `trazabilidad.md` y en el propio manual. Se corrigió un fallo de nuestro adaptador que había eliminado envolturas `align`; no era un error del framework. Se corrigieron los dos modelos angulares y los textos de pies de figura que atribuían al dibujo información no representada.

La revisión semántica de todos los extractos, el soporte exacto de cada afirmación, las hipótesis de cada transformación no ensayada y la revisión académica integral siguen pendientes. La auditoría nativa también señala profundidad insuficiente en varios capítulos bajo sus umbrales y ausencia de auditorías de párrafo. Esas incidencias están conservadas; no se eliminan para publicar el borrador.

## Reproducibilidad y uso de esta edición

Los tres PDF editoriales se recompilaron desde una copia separada de sus fuentes. Coinciden el número de páginas y el texto extraído de cada documento (`reproducibility.json`). La prueba usa las mismas dependencias instaladas: no es una instalación limpia ni una validación científica. El framework pasó 982 pruebas y omitió dos por ausencia de paquetes LaTeX de catalán y gallego. Esto caracteriza la instalación del software, no certifica el manual.

La edición sirve como borrador de estudio y revisión, con errores detectados documentados y comprobaciones localizadas. No se presenta como edición científicamente liberada.
