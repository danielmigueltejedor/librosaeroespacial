# Libros Studium — revisión de aprendizaje

El repositorio pasa a llamarse **librosstudium**. El paquete
`LibrosStudium-bundle-completo.zip` contiene **32 PDF**, en ocho carpetas por
asignatura o tema: siete asignaturas con 21 PDF y programación con diez
volúmenes más su integral. El inventario interior identifica cada archivo,
páginas, SHA-256 y procedencia. Los 21 PDF de ingeniería se han recompilado
para esta entrega. El control de sus entradas comprueba los hashes del
manuscrito y que los procedimientos requeridos se incluyan realmente en cada
PDF previsto. Véase también `reports/soluciones-paso-a-paso.md`.

La nueva integral de programación tiene **364 páginas y 75 capítulos**.
Se conservan las retiradas de la hoja de fórmulas, notación y apéndices internos
innecesarios. Añade once recorridos iniciales: Python, JavaScript, TypeScript,
Rust, C, C++, Java, C#, Go, SQL y Bash. Cada recorrido incluye un programa
pequeño, contrato de entrada, traza explicada, errores frecuentes y tres
problemas progresivos con soluciones separadas. La guía explica cómo empezar.
Quedan 332 actividades activas: 291 numéricas, 8 pruebas Rust y 33 de programación;
ese recuento no significa 332 programas verificados.

Los once ejemplos introductorios impresos y las referencias de sus soluciones
se ejecutan con compiladores o intérpretes reales; también se comprueban las
consultas SQL con datos normales y vacíos. El código editable y la configuración
mínima están en `learning/` dentro del paquete de programación. Las pruebas
cubren casos finitos, no todas las entradas posibles.

Se revisan 2718 regiones literales activas y cuatro fixtures de texto
extraído del PDF: comillas, barras, operadores, tildes, letras griegas, regex,
plantillas y colisiones de delimitadores. Cero incidencias en esos controles.
La comparación excluye espacios introducidos por la maquetación: para conservar
indentación exacta se entregan también los archivos fuente. Se corrige la copia
del signo distinto, la sustitución silenciosa de un emoji por una etiqueta U+ y
los saltos de línea escapados de dos ejemplos de C/C++. Ninguna comprobación
pretende garantizar cualquier carácter Unicode fuera del corpus revisado.

Toda la colección compila sin desbordamientos, caracteres ausentes, referencias
indefinidas ni errores graves; se comprueban 539 enlaces internos de la integral
y se reproducen 87 pasos aritméticos almacenados. La revisión visual muestrea
portadas, índices, aperturas, código, actividades, soluciones y bibliografía;
no certifica todas las páginas ni constituye revisión independiente.

Studium corrige los contratos de programación, los bloques que comenzaban un
párrafo, el texto Unicode del PDF, los listados largos en recuadros, la selección
de secciones de lectura y los títulos del solucionario. También conserva el
desarrollo de las soluciones aunque no tengan figuras y muestra el resultado
calculado, sin copiar una respuesta esperada incorrecta. En GitHub pasan 1113
pruebas con Python 3.11 y otras 1113 con Python 3.12; cada trabajo omite una
prueba de idioma alemán TeX no instalado. Ruff y Pyright pasan. El repositorio
de libros supera 86 pruebas y siete subtests.

El inventario genérico de código mantiene 83 fragmentos, cero fallos y
37 entradas pendientes o ilustrativas. Algunos ejemplos nuevos se verifican mediante
el comprobador específico de los recorridos aunque no tengan adaptador genérico.
Las seis suites de proyectos existentes pasan. No se convierten estados
pendientes en éxitos ni se aprueba académicamente una solución por haberla guardado.

La auditoría pedagógica inventaría los 75 capítulos: once tienen un nuevo
recorrido de entrada y 64 requieren establecer o ampliar ese recorrido. Sigue
pendiente la revisión técnica y bibliográfica independiente de los capítulos
y de los 258 extractos originales. Se incorporan referencias oficiales nuevas
sin inventar citas textuales. Esta es una **edición en revisión**, no un cierre
académico ni una promesa de dominio de todos los lenguajes.

Las publicaciones futuras se preparan con un flujo que construye el bundle
completo y lo descarga para verificarlo antes de publicar. Otro guard revisa
publicaciones manuales y devuelve a borrador las que no puedan validarse.
Ambos se activan al fusionar la PR del libro; no se ha fusionado automáticamente.

Cambios para revisión:
- Studium: https://github.com/danielmigueltejedor/studium/pull/81
- Libros y publicación: https://github.com/danielmigueltejedor/librosstudium/pull/8

En las siete asignaturas se han ampliado las operaciones y deducciones de los
bancos de problemas, manuales y solucionarios. Fluidos desarrolla primero
aceleración, después tiempo y finalmente espacio; muestra también el contraste
con trabajo y energía. Las 370 operaciones redactadas de su manual pasan el
control dimensional. Los métodos numéricos de vuelo añaden intervalos,
iteraciones, filas de matrices y pruebas de refinamiento, según el caso.
Son controles técnicos y una revisión del mismo modelo; la revisión académica
independiente sigue pendiente.

Versión de Studium fijada: `a7801896d8973218b9e5d1c9b456f22048ef7851`.
