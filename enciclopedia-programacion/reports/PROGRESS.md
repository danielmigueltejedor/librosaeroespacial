# Estado persistente de la revisión — 20 de octubre de 2026

## Estado de entrega

Hito implementado y comprobable, **sin aprobación académica**. La misión completa
no está terminada. La revisión individual de los 75 capítulos, de las 299 actividades activas y de su suficiencia curricular permanece abierta. No hay release
manifest ni fusión en main.

Referencias reproducibles iniciales:
- Librosaeroespacial: `63fe34a23d4f8beb65a92c09d99123d52cec39c8`.
- Studium: `ebf953dedbd9c483f9651ff93b2a66135db2dc80` (main remoto al iniciar).
- Studium requerido por esta edición: `42ddba1ceb422573ead05020975076f3e9b4cb1b`,
  [PR #79](https://github.com/danielmigueltejedor/studium/pull/79).

## Depuración solicitada: solo material de lectura pertinente

Se quita la hoja de fórmulas vacía de los diez volúmenes. También se omiten la
notación con unidades heredadas, la auditoría interna, el plan de trabajo y los
prefacios genéricos repetidos. Los informes de control permanecen separados.
La guía no contiene ejercicios de inventario ni apéndice vacío; los volúmenes
I y II conservan sus desarrollos resueltos dentro de los capítulos, sin duplicarlos
al final. Las monografías conservan las respuestas a su práctica independiente.

Se retiran 212 actividades: 192 plantillas aritméticas sin escenario y 20
actividades de inventario de la guía. Los registros originales se conservan
mediante revisiones con los mismos identificadores. Quedan 299 actividades
activas (291 numéricas, 8 pruebas Rust), distribuidas en los mismos 75 capítulos.
La retirada no completa los bancos de práctica que ahora necesitan desarrollo.

Se corrigen 38 registros iniciales y dos enunciados relacionados con el WAL; se acortan los
títulos de la guía y se eliminan de 11 títulos las promesas de cuatro proyectos
inexistentes. Las correcciones incluyen las garantías de unsafe, memcpy,
representación de clases valor Kotlin, gestión ARC, strict_types de PHP, índices
SQL, cascada CSS, durabilidad SQLite y datos sensibles del estado Terraform.
Los seis laboratorios se describen según sus archivos reales: el WAL Rust está
en memoria, la cola C++ es FIFO y el módulo TypeScript no es un servidor HTTP.
Las referencias primarias consultadas se registran sin fabricar extractos ni
promoverlas a aprobación independiente.

`reader-cleanup.json` documenta las retiradas y correcciones. Los controles de
los diez volúmenes se encuentran en `reader-edition-checks.json`: no aparecen
capítulos automáticos sobrantes, se comprueban las huellas canónicas de párrafos (41 metadatos reparados) y se repiten
87 pasos aritméticos almacenados. Esto no demuestra la corrección semántica de
cada actividad. La revisión independiente de fuentes, profundidad y soluciones
continúa pendiente. Los 61 fragmentos conservan 22 pendientes o ilustraciones;
las seis suites de proyectos pasan y no hay fallos en las comprobaciones ejecutadas.

## Diagnóstico y correcciones implementadas

La reproducción inicial genera 459 páginas, 75 capítulos y 46 desbordamientos.
Los 511 problemas vigentes son 503 registros numéricos y 8 pruebas Rust; la frase
«511 problemas de programación verificados» queda retirada. El verificador
anterior recorría revisiones históricas sin plegarlas, empleaba versiones y
rutas locales rígidas y equiparaba inspecciones superficiales con validación.

Se identificaron 63 extractos contaminados con afirmaciones del propio
manuscrito. La reparación añade 142 revisiones de evidencia: 72 retiradas
(36 registros bibliográficos y sus 36 extractos, correspondientes a 20 títulos
sintéticos repetidos entre volúmenes) y 70 reparaciones de texto/URL. Las URLs
`/vol-ref-N` también eran sintéticas. Los registros originales se conservan en
los diarios; ningún identificador se reinicia. Los 258 extractos activos quedan
explícitamente pendientes de comparación semántica con su fuente. No se afirma
que el texto restante del catálogo sea una cita auténtica.

El generador deja de borrar volúmenes o completar referencias inexistentes.
Compilar y generar un proyecto nuevo son operaciones distintas. Los proyectos
existentes se corrigen append-only; aún no existe un actualizador semántico
universal de blueprints. Una generación nueva requiere citas abiertas con
localizador, fecha y evidencia de licencia; no puede convertir los resúmenes
anteriores en extractos auténticos.

Studium separa código de matemáticas, añade adaptadores con estados precisos,
contratos de ejercicios sin unidades físicas obligatorias y copias explícitas
de revisión. No ejecuta código ajeno por defecto. La ejecución propia autorizada
lleva límites; no se presenta como sandbox. Los contratos matemáticos siguen
existiendo. El esquema completo de programación en CLI/MCP sigue pendiente.

La edición utiliza diez fotografías distintas con autor, licencia, URL,
resolución y huella en `assets/covers/manifest.json`. Comparte portada y tipografía
con la colección, declarando obra independiente. Los campos aeroespaciales siguen
siendo los valores predeterminados compatibles de la portada general.

Se amplían dos desarrollos sobre préstamos Rust y el compilador educativo
Python. Se corrigen garantías absolutas sobre Rust, reproducibilidad mediante
Cargo.lock, un ejemplo C sin cabeceras y el alcance del WAL en memoria. En los
laboratorios se corrigen reutilización/aceptación de nodos AST/signos en Python,
retroceso del reloj/números inválidos en TypeScript, límites de arena C y overflow
C++. Las seis recetas de pruebas de proyectos se ejecutan satisfactoriamente.
No se atribuye durabilidad en disco al WAL ni un servidor HTTP al limitador.

## Verificación medida

- Studium: **1094 pruebas pasan, 2 omitidas** (paquetes TeX catalán/gallego ausentes).
- Ruff: pasa. Pyright: cero errores con el intérprete del entorno de pruebas.
- Librosaeroespacial: **75 pruebas pasan, 7 subtests pasan**, incluida preservación
  de correcciones y destinos de índices en la unión de PDF.
- Seis proyectos: `PROJECT_TEST_COMMAND_PASSED`; estas pruebas finitas no son
  una certificación de corrección general.
- Fragmentos vigentes: **61**; clasificaciones:
  `{"SYNTAX_VALIDATED": 14, "COMPILED": 17, "TESTS_PASSED": 8, "UNVERIFIED": 21, "LITERAL_OR_PSEUDOCODE": 1}`.
- Fallos de comprobaciones ejecutadas: **0**. Pendientes o
  ilustraciones no verificadas: **22**. Estado global de código:
  `INCOMPLETE`, nunca «verificación completa».
- Integral: **343 páginas**; se comprueban los
  **529 enlaces internos nombrados**
  contra su página original más el desplazamiento. Se preservan las anotaciones.
- El manual de Mecánica de Fluidos recompilado conserva sus **316 páginas** y
  texto extraído idéntico. Los siete adaptadores superan la comprobación de
  recursos compartidos. Esto es compatibilidad, no nueva aprobación científica.
- La reconstrucción repetida de Rust en directorios temporales diferentes
  conserva las huellas de autoría/recursos compartidos y los bytes del PDF.
  Ver `reproducibility.json`. No se afirma identidad entre plataformas/toolchains.

| Volumen | Páginas de revisión | Overfull | Underfull registrados |
| --- | ---: | ---: | ---: |
| vol00 | 12 | 0 | 1 |
| vol01 | 32 | 0 | 1 |
| vol02 | 32 | 0 | 0 |
| vol03 | 42 | 0 | 4 |
| vol04 | 39 | 0 | 4 |
| vol05 | 38 | 0 | 5 |
| vol06 | 39 | 0 | 3 |
| vol07 | 40 | 0 | 2 |
| vol08 | 36 | 0 | 1 |
| vol09 | 33 | 0 | 1 |

No hay referencias/citas indefinidas, caracteres ausentes ni errores graves de
LaTeX en estas compilaciones. Los PDF se generan como artefactos y no se añaden
a Git. La fecha de compilación está fijada en `build-config.json`; el manifest
incluye autoría, fotografías y plantillas compartidas.

## Reproducción desde un clon limpio y CI

En la entrega anterior a esta depuración se clonó el commit `a7d8d096322b196c677f3c76ed7f8c28b4b43699` en otro directorio y
se crea un entorno Python 3.12 vacío. Studium se instala desde su commit público
de GitHub, sin PYTHONPATH ni un clon hermano. Los diez volúmenes y la edición
integral se reconstruyen con **bytes idénticos** y huellas de entrada iguales;
Git quedó limpio en aquel clon. Esa prueba corresponde a la edición anterior; no se atribuye identidad binaria de clon limpio a esta depuración. Ver `clean-clone-reproduction.json`. El entorno
resuelto se conserva en `requirements-constraints.txt`.

La CI de la entrega anterior de Studium pasó en Python 3.11 y 3.12. Para el nuevo commit se registran los resultados locales anteriores; al consultar sus checks no había nuevas ejecuciones. La CI del nuevo cambio del libro se comprueba por separado. Ninguno de estos controles constituye revisión académica.

## Inspección visual y límites

Se inspeccionan las muestras renderizadas de los diez volúmenes, sus portadas,
índices, aperturas, ejercicios, respuestas y bibliografía. La matriz
`visual-review/matrix.json` enumera las páginas y declara al revisor: el mismo
modelo en una pasada visual, **no una revisión académica independiente**.
Se conservan antes/después de la portada Rust y muestras de código.
El specimen de seis páginas cubre dieciséis lenguajes/configuraciones,
terminal/salida/error y un listado de 182 líneas que ocupa varias páginas.
Son fixtures de representación; no se presentan como programas ejecutados.

Persisten páginas escasas al final de capítulos/apéndices. Muchos temas solo
tienen introducciones; mejorar la composición no resuelve esa falta de
profundidad. Los recuadros y el vocabulario editorial heredados requieren otra
pasada. El backend pdfLaTeX no ofrece fidelidad Unicode universal; ese requisito
sigue abierto. El resaltado/metadatos de todos los lenguajes, el ciclo completo
de proyectos multifichero y sus gates específicos tampoco están completos.

Los gates nativos `aerobooks check`, `aerobooks-ai coverage` y `gate` no certifican
estos volúmenes importados: requieren el contrato nativo `book.toml`. Se intentan
y no se declaran aprobados. Se emplea el constructor de importaciones para la
muestra STEM y el pipeline de Studium para la enciclopedia, sin migraciones
académicas destructivas.

## Hitos y continuación

| Fase | Estado real |
| --- | --- |
| A | Reproducción e inventario completos; auditoría profunda de contenido pendiente. |
| B | Correcciones y regresiones generales implementadas; modelo/CLI/MCP completo pendiente. |
| C | Portadas y adaptación compartida implementadas; refinamiento interior aún abierto. |
| D | Ampliaciones y correcciones focalizadas; no se ha revisado exhaustivamente todo el corpus. |
| E | Seis suites ejecutadas y cuatro proyectos corregidos; clasificación pedagógica individual pendiente. |
| F | Compilación temporal y publicación controlada; no existe regeneración destructiva de autoría. |
| G | Muestras y specimen inspeccionados; no se acredita cada página ni Unicode universal. |
| H | Pruebas, composición, preservación y navegación comprobadas; fuentes/cobertura siguen pendientes. |
| I | Dos PR independientes en borrador; sin merge ni declaración de edición final. |

Siguiente trabajo: comparar los 258 extractos activos con originales abiertos;
reclasificar y revisar cada actividad; desarrollar monografías con objetivos,
ejemplos, soluciones justificadas y tests; extender el modelo informático por
CLI/MCP y el backend Unicode; obtener revisión independiente antes de publicar.
