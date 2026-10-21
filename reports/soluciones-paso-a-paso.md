# Soluciones paso a paso — edición en revisión

Se amplían los procedimientos de las siete asignaturas: Mecánica de Fluidos,
Estructuras Aeroespaciales, Turbomáquinas, Mecánica de Vuelo, Materiales y
Mantenimiento, Motores Cohete y Tecnología Aeroespacial. Se conservan los
enunciados y figuras; las comprobaciones registran el alcance y la procedencia.

El problema del avión explica por qué se calcula primero la aceleración desde
la fuerza neta, después se integra para obtener tiempo y finalmente espacio.
Obtiene a = 15/7 m/s², t = 35 s y s = 1312,5 m. Lo contrasta con energía y
velocidad media, y muestra cómo detectar el error de usar la velocidad final
durante toda la carrera. Los índices de respuestas enlazan con los desarrollos.

| Asignatura | Desarrollo de esta revisión |
|---|---|
| Fluidos | 128 rutas del manual; operaciones completas en cuaderno y 20 variantes de simulacro; 370 operaciones con dimensiones comprobadas |
| Estructuras | 105 rutas compartidas entre manual y cuaderno; las 20 selecciones de simulacro conservan ese desarrollo |
| Turbomáquinas | 150 rutas con datos sustituidos y todas las operaciones, compartidas entre manual y cuaderno |
| Mecánica de Vuelo | 84 casos de bancos, talleres y simulacros; métodos específicos con matrices, bisección, integrales, refinamiento y trazas temporales; ejemplo del tensor desarrollado |
| Materiales y Mantenimiento | 11 ejemplos numéricos del manual y 48 casos numéricos del cuaderno y simulacros; se mantienen los razonamientos cualitativos |
| Motores Cohete | 28 ejemplos del manual, 36 problemas y 15 casos de simulacro con operaciones visibles |
| Tecnología Aeroespacial | 29 ejemplos de manual, 30 problemas y desarrollo numérico de los tres simulacros |

Se muestran las expresiones tal como están escritas, sin simplificar constantes
antes de la sustitución. El resultado se calcula; una respuesta esperada no se
copia para simular un cálculo correcto. Los valores internos conservan precisión
antes de redondear para lectura. Las operaciones escalares no sustituyen la
justificación física, las hipótesis ni el análisis de validez.

Se recompilan los 21 PDF de ingeniería. Sus informes vinculan los archivos
realmente leídos y sus SHA-256. El control exige 943 inclusiones de procedimientos
en los PDF previstos: este número incluye rutas compartidas y no equivale a
943 problemas distintos. No hay ausencias en ese control. Se conservan las
etiquetas y dibujos de las fuentes revisadas; se revisan visualmente páginas
seleccionadas y sus continuaciones, no todas las páginas.

Pruebas: 85 y siete subtests del repositorio de libros; 329 controles del banco
de Fluidos; cero discrepancias relevantes con los valores históricos en los
registros numéricos reproducidos de bancos nativos y heredados. Los controles
no prueban por sí solos que los modelos representen máquinas reales.

Studium ya no oculta el desarrollo cuando un ejercicio carece de figuras. La
PR #81 supera CI en Python 3.11 y 3.12 con 1113 pruebas por versión y una
omitida por un idioma TeX no instalado; Ruff y Pyright pasan.
https://github.com/danielmigueltejedor/studium/pull/81

La programación conserva su edición de 364 páginas, diez volúmenes y 75
capítulos. Once rutas iniciales y 33 ejercicios de programación tienen ejemplos
y referencias ejecutados con herramientas reales. Los 332 ejercicios activos
no son 332 programas verificados. Siguen pendientes la ampliación de rutas en
64 capítulos, partes ilustrativas del inventario genérico y la revisión técnica
y bibliográfica independiente. Véanse los informes de programación.

El paquete completo contiene 32 PDF distribuidos en ocho temas. El inventario
interior registra hashes, páginas y procedencia. Esta entrega es una revisión
del mismo modelo autor, sin autoaprobación ni cierre académico independiente.

La pasada ampliada reproduce los 16 grupos de controles existentes y todos pasan.
Las 2461 páginas de ingeniería pasan el control automático de límites de texto,
páginas vacías, caracteres de sustitución, destinos internos y composición. Esta
comprobación no es una revisión visual de cada página. La auditoría bibliográfica
localiza 350 registros de ingeniería y mantiene 211 pendientes de revisión
documental; no se convierten en referencias verificadas.

Se corrige la etiqueta de un giro que aparecía como desplazamiento en Estructuras.
El turborreactor distingue el rendimiento solicitado sin combustible (0,5882)
del contraste que lo conserva coherentemente (0,5940), y no deduce un consumo
sin disponer de un modelo térmico. La política de publicación distingue su
primera instalación de una política previamente instalada que haya desaparecido.
