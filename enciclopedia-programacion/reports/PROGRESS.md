# Estado persistente de la revisión — 20 de octubre de 2026

## Estado de entrega

Hito implementado y comprobable, **sin aprobación académica**. La misión completa
no está terminada. La revisión individual de los 75 capítulos, de las 511
actividades y de su suficiencia curricular permanece abierta. No hay release
manifest ni fusión en main.

Referencias reproducibles iniciales:
- Librosaeroespacial: `63fe34a23d4f8beb65a92c09d99123d52cec39c8`.
- Studium: `ebf953dedbd9c483f9651ff93b2a66135db2dc80` (main remoto al iniciar).
- Studium requerido por esta edición: `f5f7bd021a984184c2ac4af202f44f2f771b6f87`,
  [PR #79](https://github.com/danielmigueltejedor/studium/pull/79).

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

- Studium: **1090 pruebas pasan, 2 omitidas** (paquetes TeX catalán/gallego ausentes).
- Ruff: pasa. Pyright: cero errores con el intérprete del entorno de pruebas.
- Librosaeroespacial: **74 pruebas pasan, 7 subtests pasan**, incluida preservación
  de correcciones y destinos de índices en la unión de PDF.
- Seis proyectos: `PROJECT_TEST_COMMAND_PASSED`; estas pruebas finitas no son
  una certificación de corrección general.
- Fragmentos vigentes: **62**; clasificaciones:
  `{"SYNTAX_VALIDATED": 14, "COMPILED": 17, "TESTS_PASSED": 8, "UNVERIFIED": 22, "LITERAL_OR_PSEUDOCODE": 1}`.
- Fallos de comprobaciones ejecutadas: **0**. Pendientes o
  ilustraciones no verificadas: **23**. Estado global de código:
  `INCOMPLETE`, nunca «verificación completa».
- Integral: **486 páginas**; se comprueban los
  **644 enlaces internos nombrados**
  contra su página original más el desplazamiento. Se preservan las anotaciones.
- El manual de Mecánica de Fluidos recompilado conserva sus **316 páginas** y
  texto extraído idéntico. Los siete adaptadores superan la comprobación de
  recursos compartidos. Esto es compatibilidad, no nueva aprobación científica.
- La reconstrucción repetida de Rust en directorios temporales diferentes
  conserva las huellas de autoría/recursos compartidos y los bytes del PDF.
  Ver `reproducibility.json`. No se afirma identidad entre plataformas/toolchains.

| Volumen | Páginas de revisión | Overfull | Underfull registrados |
| --- | ---: | ---: | ---: |
| vol00 | 28 | 0 | 2 |
| vol01 | 65 | 0 | 1 |
| vol02 | 65 | 0 | 1 |
| vol03 | 51 | 0 | 4 |
| vol04 | 48 | 0 | 4 |
| vol05 | 47 | 0 | 5 |
| vol06 | 48 | 0 | 4 |
| vol07 | 49 | 0 | 3 |
| vol08 | 44 | 0 | 1 |
| vol09 | 41 | 0 | 2 |

No hay referencias/citas indefinidas, caracteres ausentes ni errores graves de
LaTeX en estas compilaciones. Los PDF se generan como artefactos y no se añaden
a Git. La fecha de compilación está fijada en `build-config.json`; el manifest
incluye autoría, fotografías y plantillas compartidas.

## Reproducción desde un clon limpio y CI

Se clona el commit `a7d8d096322b196c677f3c76ed7f8c28b4b43699` en otro directorio y
se crea un entorno Python 3.12 vacío. Studium se instala desde su commit público
de GitHub, sin PYTHONPATH ni un clon hermano. Los diez volúmenes y la edición
integral se reconstruyen con **bytes idénticos** y huellas de entrada iguales;
Git queda limpio en el clon. Ver `clean-clone-reproduction.json`. El entorno
resuelto se conserva en `requirements-constraints.txt`.

La CI de Studium PR #79 pasa en Python 3.11 y 3.12, además de la comprobación de
descripción. La CI de la PR del libro se comprueba por separado; estos resultados
no constituyen revisión académica.

## Inspección visual y límites

Se inspeccionan las muestras renderizadas de los diez volúmenes, sus portadas,
índices, aperturas, ejercicios, respuestas, notación y bibliografía. La matriz
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
