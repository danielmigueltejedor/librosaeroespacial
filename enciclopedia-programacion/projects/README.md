# Laboratorios reproducibles

Estos seis proyectos son laboratorios pequeños. No son productos listos para
producción ni acreditan por sí solos un nivel profesional. Las herramientas y
salidas observadas se registran en `reports/code-verification-current.json`.

| Proyecto | Ejecutar desde su directorio | Propiedad observada y límites |
| --- | --- | --- |
| rust-kv-engine | `cargo test` | CRC, reconstrucción desde bytes y escritores concurrentes. El WAL vive en memoria: no hay archivo persistente ni durabilidad ante caídas. |
| c-arena-allocator | `cc -std=c17 -Wall -Wextra -Werror -fsanitize=address,undefined arena.c test_arena.c -o tests` y `./tests` | Alineación, límites y parser de una trama. El llamador debe aportar memoria viva y capacidad correcta. |
| cpp-task-scheduler | `c++ -std=c++20 -Wall -Wextra -Werror -fsanitize=address,undefined test_scheduler.cpp -o tests` y `./tests` | Cola limitada y suma por rangos con detección de overflow. No es un planificador de tareas completo; falta evaluar contención y equidad. |
| python-bytecode-vm | `python -m pytest -q test_vm.py` | Compilación de un subconjunto aritmético, rechazo de nodos desconocidos y errores de ejecución. No implementa Python ni es un sandbox. |
| ts-reactive-http | `node --test test_router.ts` | Validación y limitador de tokens. El ejemplo no inicia un servidor HTTP y no acota el mapa de clientes. Node no sustituye a `tsc`. |
| sql-transactional-ledger | `python verify_ledger.py` | Consultas contables en SQLite en memoria. La comprobación encuentra asientos desequilibrados; el esquema por sí solo no los prohíbe ni es una implementación contable normativa. |

El verificador copia cada proyecto a un directorio temporal, registra huellas y
usa comandos fijos con límites. Para programas ajenos, utilizar un contenedor o
VM de aislamiento externo.

## Progresión de trabajo

1. Reproduce la suite y explica una invariante antes de leer la implementación.
2. Añade un caso límite que falle en una versión defectuosa.
3. Implementa la corrección y comprueba también el comportamiento válido anterior.
4. Documenta qué propiedad no verifica la suite.
5. Amplía un laboratorio con una especificación concreta: persistencia real del
   WAL, cierre/cancelación de la cola, validación previa del bytecode, expiración
   de clientes en el limitador o rechazo de transacciones si no cuadran.

La ampliación debe incluir pruebas y límites propios. Cambiar el nombre de un
laboratorio a «proyecto experto» no aumenta su alcance.
