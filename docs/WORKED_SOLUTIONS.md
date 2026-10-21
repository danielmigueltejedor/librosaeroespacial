# Soluciones para comparar procedimientos

Cada solución debe justificar qué modelo se elige y por qué; declarar las
condiciones iniciales y los convenios; despejar primero las incógnitas en orden;
sustituir los datos mostrando las operaciones intermedias y sus unidades; y
comprobar el resultado mediante otro balance, un límite o una reconstrucción.
Una igualdad con el resultado final no sustituye esos pasos. Si existen rutas
alternativas equivalentes, hay que explicar cómo comparar sus resultados.

En una raíz, optimización, integral o integración temporal se muestran también
la función, el dominio, el criterio de parada y valores intermedios. Cuando se
emplea una aproximación numérica, una prueba de refinamiento describe su alcance;
repetir un literal almacenado no verifica el algoritmo.

## Fuentes y regeneración

Las rutas originales se encuentran en `books/*/solutions/`. Las tablas de datos,
hipótesis y desarrollos preexistentes permanecen en sus bancos públicos. El
historial de Fluidos se conserva en `solutions/source-cases.json`; sus hashes
permiten detectar cambios accidentales del enunciado.

Después de regenerar fuentes desde un banco anterior, ejecutar
`python scripts/refresh-reviewed-solutions.py` con las dependencias de
`requirements-audit.txt`. Coordina los revisores de soluciones, el generador de
métodos de vuelo y los revisores de manuales y simulacros. `scripts/link-fluid-solutions.py` enlaza las dieciséis
respuestas duplicadas con el desarrollo completo del capítulo. No se deben usar
esos índices de respuestas como sustituto de una resolución.

Las pruebas `tests/test_solution_procedures.py` comprueban el encadenamiento del
avión, las sustituciones visibles, la conservación de figuras y la inclusión de
los desarrollos. `books/mecanica-fluidos/scripts/check_solution_procedures.py`
revisa dimensiones de las 370 operaciones escalares redactadas. Su alcance no
incluye probar que un modelo represente una máquina real.

Compilar de nuevo los 21 PDF de ingeniería mediante
`python scripts/build-studium-books.py`. El informe de cada PDF registra los
archivos de entrada realmente leídos y sus SHA-256. El paquete de publicación
se crea después con `scripts/package-release-bundle.py`; sus 32 PDF se organizan
por asignatura o tema. Los controles técnicos no conceden aprobación académica.
