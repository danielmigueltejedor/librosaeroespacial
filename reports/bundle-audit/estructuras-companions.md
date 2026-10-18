# Incorporación de los cuadernos de Estructuras

La revisión inicial entregaba trece volúmenes y había omitido los dos cuadernos independientes de Estructuras. Esta incorporación completa las cinco asignaturas con manual, problemas y simulacros: **quince PDF**.

## Contenido y procedencia

- El cuaderno de problemas reúne los **105 ejercicios existentes del manual**, con sus identificadores públicos, ordenados por los ocho temas. No se cuentan como ejercicios adicionales.
- Los **cuatro simulacros de 150 minutos y diez puntos** seleccionan veinte casos distintos del mismo banco, con los mismos datos. Cubren conjuntamente los ocho temas. Se propone una rúbrica y las soluciones se separan de los enunciados. No son exámenes oficiales ni variantes numéricas inéditas.
- Se conservan los diagramas originales de cargas, reacciones, secciones, elásticas y tensiones disponibles en el manual, con registro de correspondencia y huellas de sus bloques de origen. Los esquemas de torsión y cortante se trazan desde las coordenadas públicas del banco. Los enunciados de los simulacros omiten los diagramas del manual que puedan mostrar resultados resueltos.
- Se hacen autónomas las remisiones a «el ejemplo anterior» cuando el propio enunciado ya contiene los datos necesarios. Se mantiene la corrección de giro frente a desplazamiento en PRB-0225.
- Las sustituciones numéricas largas se separan en auxiliares exactos, locales a cada paso. El generador restaura esas sustituciones y exige equivalencia simbólica con la expresión del banco. Los resultados largos se disponen en varias líneas para conservar la legibilidad.
- Las propiedades y cargas son datos académicos de enunciado. No se les atribuye la condición de valores admisibles de diseño ni de datos experimentales.

## Comprobación y alcance

Se repitieron los **405 controles** sobre los 105 casos, sin fallos. La evidencia está en `estructuras.json`: aritmética con redondeo, reconstrucción de ocho geometrías de cortante y contrastes seleccionados de energía y elasticidad. No se suman veinte verificaciones nuevas por reutilizar esos casos en los simulacros. La correspondencia entre banco, capítulos, selección de simulacros y PDF se registra en `estructuras-companions.json`.

Los dos documentos finales tienen **162 y 51 páginas**, respectivamente, y se compilan a tres pasadas con la plantilla común. La colección completa suma 1812 páginas. Se revisan visualmente portadas, índices, todas las páginas nuevas mediante contactos y páginas completas seleccionadas de sustituciones largas y diagramas; el inventario técnico de todos los volúmenes está en `pdf-checks.json`. Las 38 pruebas existentes del framework pasan. Los otros doce volúmenes conservan los resultados científicos de la pasada anterior; no se atribuye una nueva revisión de cada afirmación.

Se intentaron de nuevo los cuatro gates nativos de Estructuras. Siguen `NOT_CONFIGURED` porque esta importación no tiene `book.toml`; se conserva la salida en `estructuras-native-gates.json`. La compilación portable y el cálculo se documentan por separado. La revisión es del mismo agente autor, sin aprobación académica independiente ni validación experimental.

## Edición y reproducción

```sh
python3 books/estructuras-aeroespaciales/scripts/make_companions.py
python3 scripts/audit-estructuras.py
python3 scripts/build-studium-books.py estructuras-aeroespaciales
python3 scripts/audit-estructuras-companions.py
python3 scripts/audit-studium-pdfs.py
```

El generador necesita SymPy; las comprobaciones usan las dependencias de `requirements-audit.txt`. Los `.tex` de entrada están en `books/estructuras-aeroespaciales/latex/`, el contenido editable en `content/` y las selecciones de examen en `content/exam-selections.json`. La publicación PDF es un archivo de estudio y no un manifiesto de cierre académico.
