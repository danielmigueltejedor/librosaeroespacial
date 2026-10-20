#!/usr/bin/env python3
"""Construcción completa de los Volúmenes 4 y 5 de la Enciclopedia:
- vol04-monografias-c-cpp-sistemas (Parte V — Monografías Completas de C, C++, Zig, Ensamblador ARM64/x86-64, Ada y Fortran)
- vol05-monografias-python-js-ts (Parte V — Monografías Completas de Python 3.12+, JavaScript ES2024+ y TypeScript 5.x)
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from studium_volume_helper import ROOT, build_studium_volume  # noqa: E402

VOL04_SPEC: dict[str, object] = {
    "slug": "vol04-monografias-c-cpp-sistemas",
    "code": "ENC-VOL04",
    "title": "Volumen IV: Monografías de Lenguajes de Sistemas — C, C++, Zig, Ensamblador, Ada y Fortran",
    "subtitle": "Parte V (Bloques A–H): Memoria manual, RAII, metaprogramación con Concepts, ABI de bajo nivel y cómputo científico",
    "target_pages": 68,
    "terminology": [
        {"term": "comportamiento indefinido (Undefined Behavior)", "canonical": "comportamiento indefinido (Undefined Behavior)", "forbidden": ["error impredecible libre"]},
        {"term": "adquisición de recursos es inicialización (RAII)", "canonical": "RAII (Resource Acquisition Is Initialization)", "forbidden": ["limpieza diferida"]},
        {"term": "alias estricto (strict aliasing)", "canonical": "alias estricto (strict aliasing)", "forbidden": ["solapamiento libre de punteros"]},
    ],
    "notation": [
        {"symbol": r"\text{sizeof}(T)", "meaning": "Tamaño en bytes de un objeto o tipo completo en C/C++", "unit": "B"},
        {"symbol": r"\text{alignof}(T)", "meaning": "Requisito de alineamiento de dirección en C11/C23 y C++11/C++20", "unit": "B"},
        {"symbol": r"p + k", "meaning": "Aritmética de punteros escalada por k * sizeof(*p) bytes", "unit": "dirección"},
    ],
    "chapters": [
        {
            "id": "cap01-c-fundamentos-modelo-compilacion-tipos-principiante",
            "title": "Monografía de C (I — Bloques A, B y C): Historia, modelo de traducción ISO C17/C23, toolchain y nivel principiante",
            "part_id": "parte-v-monografia-c",
            "part_title": "Monografía Autónoma de C (ISO/IEC 9899:2018 / C23)",
            "sources": ["src-iso-c17", "src-bryant-ohallaron"],
            "learning_objectives": [
                "Comprender la evolución histórica de C desde UNIX en Bell Labs (Dennis Ritchie, 1972) hasta los estándares ANSI C89, C99, C11, C17 y C23.",
                "Dominar las 8 fases de traducción del estándar ISO C, el preprocesador, la compilación separada por unidades de traducción y el enlazado ELF/Mach-O.",
                "Utilizar con precisión los tipos enteros de anchura exacta (<stdint.h>), promociones enteras, operadores bit a bit y estructuras de control.",
            ],
            "concepts": [
                {"id": "cpt-c-translation-phases", "title": "Unidades de traducción, preprocesado, compilación con GCC/Clang y enlazado estático/dinámico"},
                {"id": "cpt-c-stdint-promotions", "title": "Tipos de anchura fija (<stdint.h>), conversiones aritméticas usuales y comportamiento indefinido en desbordamiento con signo"},
            ],
            "subsections": [
                {"id": "sec-v4-1-1", "title": "Bloques A y B: Historia de C, modelo de máquina abstracta, GCC/Clang, CMake y flags de diagnóstico"},
                {"id": "sec-v4-1-2", "title": "Bloque C: Tipos fundamentales, <stdint.h>, promociones aritméticas, operadores y control de flujo"},
            ],
            "figure": {
                "key": "fig-c-translation-pipeline",
                "caption": "Tubería clásica de compilación separada en C: el preprocesador expande directivas sobre cada unidad de traducción (.i), el compilador emite código ensamblador (.s), el ensamblador genera objetos reubicables (.o) y el enlazador resuelve símbolos externos.",
                "tikz": r"""\begin{tikzpicture}[node distance=1.6cm, >=stealth, thick, font=\small]
\node[draw=blue!70!black, fill=blue!8, rounded corners, minimum width=2.2cm, minimum height=0.9cm, align=center] (src) {\texttt{arena.c}\\+\,\texttt{arena.h}};
\node[draw=blue!70!black, fill=blue!8, rounded corners, minimum width=2.3cm, minimum height=0.9cm, align=center, right=0.5cm of src] (cpp) {Preprocesador\\(\texttt{cc -E} $\to$ \texttt{.i})};
\node[draw=orange!75!black, fill=orange!12, rounded corners, minimum width=2.3cm, minimum height=0.9cm, align=center, right=0.5cm of cpp] (cc1) {Compilador\\(\texttt{cc -S} $\to$ \texttt{.s})};
\node[draw=teal!70!black, fill=teal!10, rounded corners, minimum width=2.3cm, minimum height=0.9cm, align=center, right=0.5cm of cc1] (as) {Ensamblador\\(\texttt{as} $\to$ \texttt{.o})};
\node[draw=green!60!black, fill=green!10, rounded corners, minimum width=2.2cm, minimum height=0.9cm, align=center, right=0.5cm of as] (ld) {Enlazador\\(\texttt{ld} $\to$ Binario)};
\draw[->] (src) -- (cpp);
\draw[->] (cpp) -- (cc1);
\draw[->] (cc1) -- (as);
\draw[->] (as) -- (ld);
\end{tikzpicture}""",
            },
            "purpose": (
                "Este capítulo inicia la monografía autónoma del lenguaje C (Bloques A, B y C). C es la lingua franca de los "
                "sistemas operativos (Linux, Windows NT, XNU/macOS), los motores de bases de datos (PostgreSQL, SQLite, Redis), "
                "los intérpretes de lenguajes (CPython, Lua) y los sistemas empotrados. El lector aprenderá a programar en C "
                "moderno (C17/C23) desde cero con disciplina de tipos y herramientas de verificación rigurosas."
            ),
            "paragraphs": [
                {
                    "subsection": "sec-v4-1-1",
                    "text": (
                        "Creado por Dennis Ritchie entre 1969 y 1973 en los Laboratorios Bell para reescribir el núcleo de UNIX "
                        "(originalmente en ensamblador PDP-11), C fue estandarizado por ANSI en 1989 (C89/C90) y por ISO en las "
                        "revisiones C99 (que introdujo `<stdint.h>`, `<stdbool.h>`, inicializadores designados y el calificador "
                        "`restrict`), C11 (modelo de memoria multihilo y `_Atomic`), C17 y C23 (`nullptr`, `constexpr`, `typeof`, "
                        "`<stdckdint.h>`). Como muestra la Figura \\ref{fig:fig-c-translation-pipeline}, cada fichero `.c` junto "
                        "con las cabeceras `.h` incluidas por `#include` constituye una *unidad de traducción* independiente. En "
                        "ingeniería profesional, ningún programa en C debe compilarse sin activar las banderas estrictas de diagnóstico "
                        "y los sanitizadores dinámicos: `clang -std=c17 -O2 -Wall -Wextra -Wpedantic -Werror -Wshadow -Wconversion "
                        "-fsanitize=address,undefined`."
                    ),
                },
                {
                    "subsection": "sec-v4-1-2",
                    "text": (
                        "Dado que el estándar C solo fija anchuras mínimas para `short`, `int`, `long` y `long long`, el código de "
                        "sistemas portable utiliza siempre los tipos de anchura exacta de `<stdint.h>`: `uint8_t`, `uint16_t`, "
                        "`uint32_t`, `uint64_t`, `int32_t`, `int64_t`, además de `size_t` (para tamaños y conteos de objetos en "
                        "memoria) y `ptrdiff_t` (para diferencias entre punteros). Una regla crítica de la máquina abstracta de C "
                        "es la asimetría entre enteros sin signo y con signo: mientras que los enteros sin signo (`uint32_t`, `size_t`) "
                        "operan por definición en aritmética modular $\\bmod 2^w$, el desbordamiento de un entero **con signo** "
                        "(`int32_t`) constituye **comportamiento indefinido** (*Undefined Behavior*, UB), lo que autoriza al "
                        "optimizador a asumir que jamás ocurre y a eliminar comprobaciones ingenuas a posteriori como `if (a + b < a)`. "
                        "Por ello, el desbordamiento con signo debe prevenirse **antes** de ejecutar la suma:\n"
                        "```c\n"
                        "#include <stdint.h>\n"
                        "#include <stdbool.h>\n\n"
                        "bool safe_add_i32(int32_t a, int32_t b, int32_t *out) {\n"
                        "    if ((b > 0 && a > INT32_MAX - b) || (b < 0 && a < INT32_MIN - b)) {\n"
                        "        return false;\n"
                        "    }\n"
                        "    *out = a + b;\n"
                        "    return true;\n"
                        "}\n"
                        "```\n"
                        "En C23, la cabecera estándar `<stdckdint.h>` estandariza esta operación mediante la primitiva intrínseca "
                        "`ckd_add(out, a, b)`."
                    ),
                },
            ],
            "definition": (
                "Comportamiento Indefinido (Undefined Behavior, ISO C17 §3.4.3): uso de una construcción no portable o de datos "
                "erróneos para los cuales el estándar internacional no impone requisito alguno, permitiendo que el compilador "
                "optimice bajo la premisa axiomática de que dicha situación es inalcanzable."
            ),
            "consejo": (
                "Incluye siempre guardas de inclusión (`#ifndef MODULO_H` / `#define MODULO_H` / `#endif`) en todas tus cabeceras "
                "`.h` y nunca declares variables globales con definición en una cabecera sin `extern`."
            ),
            "self_check": (
                "¿Por qué comparar un índice `int i = -1` con `size_t n = 10` mediante `if (i < n)` evalúa a `false` en C debido "
                "a las conversiones aritméticas usuales?"
            ),
            "derivation": {
                "title": "Conversión implícita de entero negativo con signo a sin signo módulo 2^w",
                "assumptions": ["En conversión de int con valor -x (x > 0) a un tipo sin signo de w bits, ISO C suma 2^w"],
                "steps": [
                    {"equation": r"U(-x) = 2^w - x", "justification": "Semántica estándar ISO C §6.3.1.3 de conversión a entero sin signo módulo 2^w"},
                    {"equation": r"U(-1) = 2^w - 1", "justification": "El valor -1 se convierte en el valor máximo representable UINT_MAX"},
                ],
                "Verify": {"left": "2**w - 1", "right": "-1 + 2**w"},
            },
            "worked_problem": {
                "prompt": (
                    "En una arquitectura de 32 bits para enteros `uint32_t` ($w = 32$, módulo $2^{32} = 4294967296$), un entero "
                    "con signo con valor $-100$ se convierte implícitamente a `uint32_t` durante una comparación. Calcula el valor "
                    "numérico exacto que toma tras la conversión según la regla $2^{32} - 100$."
                ),
                "expression": "2**32 - 100",
                "solution": {
                    "model": "Conversión a entero sin signo módulo 2^32 (ISO C §6.3.1.3)",
                    "given": [
                        {"symbol": "w", "value": "32 bits", "description": "Anchura en bits de uint32_t"},
                        {"symbol": "x", "value": "-100", "description": "Valor con signo original"},
                    ],
                    "steps": [
                        {"step": "Sumamos 2^32 al valor negativo -100", "equation": r"U = 2^{32} - 100", "expression": "2**32 - 100"},
                    ],
                    "conclusion": "El valor resultante en uint32_t es 4 294 967 196, razón por la cual `-Wsign-conversion` es indispensable.",
                },
            },
            "practice_problems": [
                {"prompt": "Calcula el valor en `uint16_t` ($w = 16$) resultante de convertir $-1$ a sin signo ($2^{16} - 1$).", "expression": "2**16 - 1", "difficulty": "FOUNDATIONAL", "problem_type": "DIRECT_SUBSTITUTION"},
                {"prompt": "Un registro de control de 8 bits activa los bits 0, 3 y 7 ($2^0 + 2^3 + 2^7$). ¿Cuál es el valor decimal de la máscara `uint8_t`?", "expression": "1 + 8 + 128", "difficulty": "FOUNDATIONAL", "problem_type": "DIRECT_SUBSTITUTION"},
                {"prompt": "¿Cuántos bytes ocupa en total una estructura con 4 campos `uint32_t` y 2 campos `uint64_t` perfectamente alineados ($4 \\times 4 + 2 \\times 8$)?", "expression": "4 * 4 + 2 * 8", "difficulty": "INTERMEDIATE", "problem_type": "MULTI_STEP"},
                {"prompt": "Si compilamos un proyecto en C formado por 18 unidades de traducción `.c` y solo modificamos un fichero `.c`, ¿cuántas unidades de traducción evita recompilar `make`/`ninja`?", "expression": "18 - 1", "difficulty": "INTERMEDIATE", "problem_type": "DESIGN"},
            ],
        },
        {
            "id": "cap02-c-punteros-memoria-dinamica-estructuras-aliasing",
            "title": "Monografía de C (II — Bloques D y E): Punteros, aritmética de direcciones, memoria dinámica, structs y strict aliasing",
            "part_id": "parte-v-monografia-c",
            "part_title": "Monografía Autónoma de C (ISO/IEC 9899:2018 / C23)",
            "sources": ["src-iso-c17", "src-bryant-ohallaron"],
            "learning_objectives": [
                "Dominar la semántica de punteros, el decaimiento de arrays a punteros, punteros a funciones y la aritmética escalada de direcciones.",
                "Gestionar el ciclo de vida en el montículo con malloc, calloc, realloc y free, y construir asignadores lineales de región (Arena Allocators).",
                "Aplicar la regla de alias estricto (strict aliasing), el calificador restrict y la lectura binaria segura mediante memcpy.",
            ],
            "concepts": [
                {"id": "cpt-c-pointers-arenas", "title": "Aritmética de punteros, decaimiento de arrays, punteros a funciones y asignadores por arena"},
                {"id": "cpt-c-strict-aliasing-restrict", "title": "Regla del tipo efectivo (strict aliasing), calificador restrict y deserialización segura con memcpy"},
            ],
            "subsections": [
                {"id": "sec-v4-2-1", "title": "Bloque D: Punteros, arrays, cadenas terminadas en NUL, structs, unions y memoria dinámica"},
                {"id": "sec-v4-2-2", "title": "Bloque E: Punteros a función, calificador restrict, strict aliasing y asignadores de región (Arena)"},
            ],
            "purpose": (
                "Este capítulo desarrolla los niveles intermedio y avanzado de C (Bloques D y E). Aquí desentrañamos la relación "
                "exacta entre arrays y punteros, la representación en memoria de estructuras y uniones, los riesgos de `malloc`/`free` "
                "individuales y por qué el patrón de ingeniería de sistemas por excelencia en C es el asignador por región (*Arena Allocator*)."
            ),
            "paragraphs": [
                {
                    "subsection": "sec-v4-2-1",
                    "text": (
                        "En C, un puntero `T *p` almacena la dirección virtual de un objeto de tipo `T`. La aritmética de punteros está "
                        "escalada automáticamente por el tamaño del tipo apuntado: si `p` tiene dirección base $A$, la expresión `p + k` "
                        "(y su equivalente por definición `&(p[k])`) evalúa a la dirección $A + k \\cdot \\text{sizeof}(T)$. El estándar "
                        "ISO C permite formar y comparar un puntero únicamente dentro del mismo array asignado o exactamente una posición "
                        "más allá del último elemento (`p + N`, denominado *one-past-the-end*), aunque desreferenciar `p + N` es "
                        "comportamiento indefinido. Las cadenas en C son secuencias de bytes terminadas por el carácter nulo `'\\0'` "
                        "(`0x00`); calcular `strlen(s)` cuesta $O(n)$ porque debe recorrer los bytes hasta hallar el centinela, y usar "
                        "funciones no acotadas permite desbordar el búfer si no se pasa explícitamente la capacidad máxima del destino."
                    ),
                },
                {
                    "subsection": "sec-v4-2-2",
                    "text": (
                        "La regla de *alias estricto* (*strict aliasing*, ISO C17 §6.5 p7) estipula que un objeto en memoria solo "
                        "puede ser accedido a través de un lvalue de tipo compatible con su tipo efectivo o a través de un puntero "
                        "a carácter (`unsigned char *` o `char *`). Por tanto, convertir un `uint8_t *buf` arbitrario mediante "
                        "`*(uint32_t *)buf` viola tanto el alias estricto como potencialmente el alineamiento de hardware; la forma "
                        "conforme al estándar —que GCC y Clang compilan a una única instrucción máquina `mov` sin llamada real a "
                        "función— consiste en usar `memcpy(&val, buf, sizeof(val))`. Asimismo, el calificador `restrict` en "
                        "`void saxpy(size_t n, float a, const float *restrict x, float *restrict y)` promete al compilador que las "
                        "regiones apuntadas por `x` e `y` no se solapan, habilitando la vectorización SIMD automática:\n"
                        "```c\n"
                        "#include <stddef.h>\n"
                        "#include <stdint.h>\n\n"
                        "void vector_scale_add(size_t n, float alpha, const float *restrict x, float *restrict y) {\n"
                        "    for (size_t i = 0; i < n; ++i) {\n"
                        "        y[i] += alpha * x[i];\n"
                        "    }\n"
                        "}\n"
                        "```\n"
                        "En sistemas de alto rendimiento (compiladores, servidores HTTP, videojuegos), en lugar de invocar miles de "
                        "veces `malloc` y `free`, se reserva un bloque contiguo y se sirve memoria alineada incrementando un desplazamiento "
                        "(`Arena Allocator`), liberando toda la región en $O(1)$ al finalizar la petición o fase."
                    ),
                },
            ],
            "definition": (
                "Regla de Alias Estricto (Strict Aliasing, ISO C17 §6.5): restricción semántica que prohíbe acceder a un valor "
                "almacenado mediante un puntero de un tipo distinto no relacionado (salvo tipos de carácter `unsigned char`), "
                "permitiendo al compilador mantener valores en registros sin recargarlos desde memoria tras escrituras a otros tipos."
            ),
            "consejo": (
                "Para reinterpretar los bits de un `float` como `uint32_t` o leer enteros de un paquete de red en C, utiliza "
                "siempre `memcpy(&destino, &origen, sizeof(destino))`: es 100 % seguro frente a strict aliasing y alineamiento, "
                "y el compilador lo optimiza a una sola instrucción de registro."
            ),
            "self_check": (
                "¿Por qué tras ejecutar `free(ptr)` en C es una buena práctica defensiva asignar `ptr = NULL` si el puntero "
                "permanece aún en ámbito?"
            ),
            "derivation": {
                "title": "Alineamiento hacia arriba a potencia de dos en un asignador Arena",
                "assumptions": ["Sea offset la posición actual y align una potencia de dos (align = 2^k)"],
                "steps": [
                    {"equation": r"\text{pad} = (\text{align} - (\text{offset} \bmod \text{align})) \bmod \text{align}", "justification": "Bytes necesarios para alcanzar el siguiente múltiplo exacto de align"},
                    {"equation": r"\text{aligned} = \text{offset} + \text{pad}", "justification": "Nueva posición inicial garantizada como múltiplo de align"},
                ],
                "Verify": {"left": "offset + pad", "right": "pad + offset"},
            },
            "worked_problem": {
                "prompt": (
                    "En el asignador por región `projects/c-arena-allocator`, el desplazamiento actual del búfer es `offset = 19` bytes "
                    "y se solicita reservar una estructura de $40\\text{ B}$ con requisito de alineamiento `align = 8` bytes. "
                    "El asignador avanza primero `offset` al siguiente múltiplo de 8 (sumando $5\\text{ B}$ de relleno hasta $24$) "
                    "y luego suma los $40\\text{ B}$ del objeto. Calcula el nuevo valor exacto de `offset` tras la asignación."
                ),
                "expression": "(19 + 5) + 40",
                "solution": {
                    "model": "Avance de puntero con alineamiento en Arena Allocator",
                    "given": [
                        {"symbol": "offset_0", "value": "19 B", "description": "Desplazamiento actual antes de la reserva"},
                        {"symbol": "pad", "value": "5 B", "description": "Relleno para alcanzar el múltiplo de 8 (24 B)"},
                        {"symbol": "size", "value": "40 B", "description": "Tamaño del bloque solicitado"},
                    ],
                    "steps": [
                        {"step": "Alineamos 19 + 5 = 24 y sumamos los 40 bytes del bloque", "equation": r"\text{offset}_1 = (19 + 5) + 40", "expression": "(19 + 5) + 40"},
                    ],
                    "conclusion": "El desplazamiento final de la arena queda en 64 bytes.",
                },
            },
            "practice_problems": [
                {"prompt": "Si un puntero `uint64_t *p` apunta a la dirección decimal 4096, ¿a qué dirección decimal apunta `p + 5` sabiendo que `sizeof(uint64_t) = 8`?", "expression": "4096 + 5 * 8", "difficulty": "FOUNDATIONAL", "problem_type": "DIRECT_SUBSTITUTION"},
                {"prompt": "Una cadena en C contiene 31 caracteres visibles más su byte terminador `'\\0'`. ¿Cuántos bytes mínimos debe reservar `malloc`?", "expression": "31 + 1", "difficulty": "FOUNDATIONAL", "problem_type": "DIRECT_SUBSTITUTION"},
                {"prompt": "En una arena con capacidad total de 4096 bytes, se reservan 12 nodos de 64 bytes ya alineados. ¿Cuántos bytes libres quedan en la arena?", "expression": "4096 - 12 * 64", "difficulty": "INTERMEDIATE", "problem_type": "MULTI_STEP"},
                {"prompt": "Si un paquete binario de telemetría tiene 8 bytes de cabecera y transporta 16 muestras `int16_t` (2 bytes cada una), ¿cuántos bytes mide el paquete completo?", "expression": "8 + 16 * 2", "difficulty": "INTERMEDIATE", "problem_type": "DESIGN"},
            ],
        },
        {
            "id": "cap03-c-experto-atomicos-posix-sanitizers-ecosistema-proyectos",
            "title": "Monografía de C (III — Bloques F, G y H): Concurrencia C11/POSIX, Sanitizers, Ecosistema y Proyectos",
            "part_id": "parte-v-monografia-c",
            "part_title": "Monografía Autónoma de C (ISO/IEC 9899:2018 / C23)",
            "sources": ["src-iso-c17", "src-posix-2017"],
            "learning_objectives": [
                "Programar concurrencia segura en C mediante <stdatomic.h>, pthreads, descriptores de fichero POSIX y mmap.",
                "Integrar AddressSanitizer (ASan), UndefinedBehaviorSanitizer (UBSan), ThreadSanitizer (TSan) y analizadores estáticos en CMake/Meson.",
                "Auditar y extender el proyecto completo `projects/c-arena-allocator` junto con los 4 proyectos integradores en C.",
            ],
            "concepts": [
                {"id": "cpt-c-stdatomic-posix", "title": "Operaciones atómicas C11 (<stdatomic.h>), hilos POSIX (pthreads) y E/S no bloqueante"},
                {"id": "cpt-c-sanitizers-projects", "title": "Verificación dinámica con ASan/UBSan/TSan, construcción con CMake y proyectos de sistemas en C"},
            ],
            "subsections": [
                {"id": "sec-v4-3-1", "title": "Bloque F: Concurrencia C11 (<stdatomic.h>), pthreads, llamadas POSIX y programación defensiva"},
                {"id": "sec-v4-3-2", "title": "Bloques G y H: Ecosistema (CMake, Meson, pkg-config, Sanitizers) y los 4 proyectos en C"},
            ],
            "purpose": (
                "Este capítulo cierra la monografía de C abordando el nivel experto (Bloque F), el ecosistema de construcción "
                "y auditoría (Bloque G) y los proyectos prácticos (Bloque H), incluyendo la verificación real del proyecto "
                "`projects/c-arena-allocator` compilado con `clang -std=c17 -fsanitize=address,undefined`."
            ),
            "paragraphs": [
                {
                    "subsection": "sec-v4-3-1",
                    "text": (
                        "Un error histórico frecuente en C consiste en emplear el calificador `volatile` creyendo que proporciona "
                        "sincronización entre hilos. En el estándar ISO C, `volatile` únicamente instruye al compilador para no omitir "
                        "ni reordenar lecturas/escrituras respecto a registros de hardware mapeados en memoria (MMIO) o manejadores "
                        "de señales (`sig_atomic_t`), pero **no** garantiza atomicidad ni emite barreras de coherencia de caché entre "
                        "núcleos de CPU. Para concurrencia multihilo real, C11 introdujo `<stdatomic.h>` (`_Atomic uint64_t`, "
                        "`atomic_fetch_add_explicit`, `memory_order_acquire`, `memory_order_release`). En sistemas UNIX/POSIX "
                        "(IEEE Std 1003.1), la gestión de recursos que pueden fallar en cascada dentro de una misma función se "
                        "estructura idiomáticamente mediante el patrón de limpieza centralizada con etiquetas `goto cleanup:`:\n"
                        "```c\n"
                        "int process_file_buffer(size_t bytes) {\n"
                        "    int rc = -1;\n"
                        "    uint8_t *buf_a = malloc(bytes);\n"
                        "    if (!buf_a) goto fail_a;\n"
                        "    uint8_t *buf_b = malloc(bytes);\n"
                        "    if (!buf_b) goto fail_b;\n"
                        "    rc = 0; // operación exitosa\n"
                        "    free(buf_b);\n"
                        "fail_b:\n"
                        "    free(buf_a);\n"
                        "fail_a:\n"
                        "    return rc;\n"
                        "}\n"
                        "```\n"
                        "Este patrón asegura un único camino determinista de liberación en orden inverso de adquisición sin duplicar llamadas a `free`."
                    ),
                },
                {
                    "subsection": "sec-v4-3-2",
                    "text": (
                        "El ecosistema moderno de C se apoya en generadores de sistemas de construcción como `CMake` y `Meson` sobre "
                        "el ejecutor `Ninja`, el sistema de metadatos de bibliotecas `pkg-config`, pruebas unitarias ligeras y, de "
                        "forma obligatoria en integración continua, la tríada de sanitizadores de compilador: `AddressSanitizer` "
                        "(detecta desbordamientos en pila/montículo/globales y *use-after-free* con una sobrecarga media inferior "
                        "a $2\\times$), `UndefinedBehaviorSanitizer` (detecta desbordamientos con signo, desplazamientos ilegales "
                        "y punteros nulos o desalineados) y `ThreadSanitizer` (detecta carreras de datos). Los cuatro proyectos del "
                        "bloque en C son: (1) una utilidad CLI compatible con POSIX (`wc`/`sha256`) usando E/S por bloques; (2) el "
                        "asignador por arena y analizador de paquetes binarios con checksum `projects/c-arena-allocator`; (3) una "
                        "tabla hash abierta genérica con sondeo lineal y factor de carga controlado; y (4) un servidor TCP multicliente "
                        "no bloqueante basado en multiplexación de descriptores."
                    ),
                },
            ],
            "definition": (
                "Memoria sombra en AddressSanitizer (ASan Shadow Memory): técnica de instrumentación de compilador donde cada "
                "bloque alineado de 8 bytes de la memoria de aplicación se proyecta mediante `(addr >> 3) + Offset` sobre 1 byte "
                "de memoria sombra que codifica si dichos 8 bytes son direccionables o pertenecen a una zona roja (*redzone*) envenenada."
            ),
            "consejo": (
                "Nunca utilices `volatile` como sustituto de `<stdatomic.h>` o `pthread_mutex_t`: una carrera de datos sobre una "
                "variable `volatile` no atómica sigue siendo comportamiento indefinido según ISO C11/C17."
            ),
            "self_check": (
                "¿Por qué el patrón `goto cleanup;` hacia adelante al final de una función en C mejora la seguridad de liberación "
                "de recursos frente a tener múltiples sentencias `return` dispersas que olvidan liberar descriptores previos?"
            ),
            "derivation": {
                "title": "Relación de escala 8:1 de la memoria sombra en AddressSanitizer (ASan)",
                "assumptions": ["Cada 8 bytes de memoria de aplicación se codifican en 1 byte de memoria sombra (shadow memory)"],
                "steps": [
                    {"equation": r"M_{\text{shadow}} = \frac{M_{\text{app}}}{8}", "justification": "Desplazamiento bit a bit addr >> 3 que comprime 8 bytes de estado en 1 byte sombra"},
                    {"equation": r"M_{\text{total}} = M_{\text{app}} + \frac{M_{\text{app}}}{8} = \frac{9}{8} M_{\text{app}}", "justification": "Suma de memoria de datos más tabla sombra"},
                ],
                "Verify": {"left": "M_app + M_app / 8", "right": "9 * M_app / 8"},
            },
            "worked_problem": {
                "prompt": (
                    "Cuando un programa en C se compila con `-fsanitize=address` (AddressSanitizer), cada $8\\text{ B}$ de memoria "
                    "de aplicación requieren $1\\text{ B}$ de memoria sombra (*shadow memory*), más zonas rojas (*redzones*) de "
                    "$32\\text{ B}$ alrededor de cada asignación. Si una aplicación reserva $N = 1000$ bloques de $64\\text{ B}$ "
                    "cada uno (con $32\\text{ B}$ de zona roja por bloque), calcula cuántos bytes suman los bloques más sus zonas "
                    "rojas más la memoria sombra correspondiente ($1/8$ del total)."
                ),
                "expression": "(1000 * (64 + 32)) * 9 / 8",
                "solution": {
                    "model": "Consumo de memoria bajo instrumentación AddressSanitizer (ASan)",
                    "given": [
                        {"symbol": "N", "value": "1000", "description": "Número de bloques asignados"},
                        {"symbol": "S_bloque", "value": "64 B", "description": "Tamaño útil de cada bloque"},
                        {"symbol": "S_redzone", "value": "32 B", "description": "Zona roja envenenada por bloque"},
                    ],
                    "steps": [
                        {"step": "Sumamos bloque + redzone (96000 B) y multiplicamos por 9/8 para incluir el byte sombra por cada 8 B", "equation": r"M = 1000 \cdot (64 + 32) \cdot \frac{9}{8}", "expression": "(1000 * (64 + 32)) * 9 / 8"},
                    ],
                    "conclusion": "El conjunto instrumentado ocupa 108 000 bytes (96 000 B de bloques con redzones y 12 000 B de memoria sombra).",
                },
            },
            "practice_problems": [
                {"prompt": "En AddressSanitizer, ¿cuántos bytes de memoria sombra corresponden a 64 000 bytes de memoria de aplicación ($64000 / 8$)?", "expression": "64000 / 8", "difficulty": "FOUNDATIONAL", "problem_type": "DIRECT_SUBSTITUTION"},
                {"prompt": "En `projects/c-arena-allocator`, la cabecera de telemetría suma los campos `magic` (10), `version` (2), `flags` (3) y `payload_len` (25). ¿Cuál es el valor del checksum esperado?", "expression": "10 + 2 + 3 + 25", "difficulty": "FOUNDATIONAL", "problem_type": "DIRECT_SUBSTITUTION"},
                {"prompt": "Una función en C adquiere secuencialmente 5 recursos y falla al intentar adquirir el cuarto. ¿Cuántos recursos ya adquiridos debe liberar la cascada `goto cleanup` antes de retornar?", "expression": "4 - 1", "difficulty": "INTERMEDIATE", "problem_type": "MULTI_STEP"},
                {"prompt": "Un anillo de descriptores E/S tiene capacidad para 256 entradas de 16 bytes cada una. ¿Cuántos bytes mide el anillo completo mapeado en memoria?", "expression": "256 * 16", "difficulty": "INTERMEDIATE", "problem_type": "DESIGN"},
            ],
        },
        {
            "id": "cap04-cpp-fundamentos-raii-move-semantics-smart-pointers",
            "title": "Monografía de C++ (I — Bloques A–D): De C++98 a C++20/23, RAII, Semántica de Movimiento y Punteros Inteligentes",
            "part_id": "parte-v-monografia-cpp",
            "part_title": "Monografía Autónoma de C++ (ISO/IEC 14882:2020 / C++23)",
            "sources": ["src-iso-cpp20", "src-bryant-ohallaron"],
            "learning_objectives": [
                "Comprender la filosofía de C++ moderno (Bjarne Stroustrup): tipos definidos por el usuario con coste cero y determinismo RAII.",
                "Aplicar la Regla de Cero, la Regla de Cinco, categorías de valores (lvalue, prvalue, xvalue) y semántica de movimiento (std::move).",
                "Gestionar recursos dinámicos sin fugas mediante std::unique_ptr, std::shared_ptr, std::weak_ptr, std::span y std::string_view.",
            ],
            "concepts": [
                {"id": "cpt-cpp-raii-rule-of-five", "title": "Invariantes de clase, destructores deterministas RAII, Regla de Cero/Cinco y referencias rvalue (T&&)"},
                {"id": "cpt-cpp-smart-pointers-spans", "title": "Propiedad exclusiva (std::unique_ptr), compartida (std::shared_ptr) y vistas sin propiedad (std::span, std::string_view)"},
            ],
            "subsections": [
                {"id": "sec-v4-4-1", "title": "Bloques A–C: Evolución C++11/14/17/20/23, toolchain, referencias, sobrecarga, constexpr y RAII"},
                {"id": "sec-v4-4-2", "title": "Bloque D: Categorías de valores (lvalue/rvalue), Regla de Cero/Cinco, std::unique_ptr y std::span"},
            ],
            "purpose": (
                "Este capítulo inicia la monografía autónoma de C++ moderno (ISO C++20 / C++23). Lejos de tratar a C++ como "
                "«C con clases y `new`/`delete` manuales», enseñamos desde el primer día el paradigma moderno: propiedad "
                "automática determinista mediante RAII, vistas no propietarias (`std::string_view`, `std::span`), evaluación "
                "en tiempo de compilación (`constexpr`/`consteval`) y semántica de movimiento."
            ),
            "paragraphs": [
                {
                    "subsection": "sec-v4-4-1",
                    "text": (
                        "Diseñado por Bjarne Stroustrup desde 1979 y estandarizado por ISO en 1998, C++ experimentó una profunda "
                        "modernización con C++11 (semántica de movimiento, lambdas, `auto`, `constexpr`, `std::unique_ptr`, modelo "
                        "de memoria multihilo), C++14, C++17 (`std::optional`, `std::variant`, `std::string_view`, `if constexpr`) "
                        "y C++20/C++23 (`concepts`, `std::ranges`, corrutinas, módulos, `std::span`, `std::expected`). El pilar "
                        "arquitectónico de C++ es **RAII** (*Resource Acquisition Is Initialization*): todo recurso (memoria del "
                        "montículo, socket, fichero, cerrojo `std::scoped_lock`) se vincula al ciclo de vida de un objeto alojado "
                        "en la pila cuyo constructor establece la invariante y cuyo destructor `~T()` libera infaliblemente el recurso "
                        "al salir del ámbito, incluso si se desenrolla la pila (*stack unwinding*) por el lanzamiento de una excepción."
                    ),
                },
                {
                    "subsection": "sec-v4-4-2",
                    "text": (
                        "C++11 clasificó toda expresión según su identidad y movibilidad en `lvalue` (tiene identidad persistente), "
                        "`xvalue` (*expiring value*, tiene identidad pero sus recursos pueden ser robados) y `prvalue` (temporal puro). "
                        "La **Regla de Cero** establece que las clases de lógica de negocio no deben escribir destructores, constructores "
                        "de copia ni de movimiento manuales, sino componer miembros RAII (`std::vector`, `std::string`, `std::unique_ptr`). "
                        "Si una clase gestiona directamente un manejador crudo del sistema, aplica la **Regla de Cinco**: definir "
                        "explícitamente destructor, constructor de copia, asignación por copia, constructor de movimiento (`noexcept`) "
                        "y asignación por movimiento (`noexcept`):\n"
                        "```cpp\n"
                        "#include <memory>\n"
                        "#include <span>\n"
                        "#include <numeric>\n\n"
                        "// std::span<const double> observa cualquier array, std::vector o std::array sin copiar:\n"
                        "constexpr double sum_window(std::span<const double> samples) noexcept {\n"
                        "    double acc = 0.0;\n"
                        "    for (double v : samples) { acc += v; }\n"
                        "    return acc;\n"
                        "}\n"
                        "```\n"
                        "Es fundamental marcar los constructores de movimiento como `noexcept`: `std::vector` solo mueve sus elementos "
                        "durante una realojación si el constructor de movimiento promete `noexcept`; de lo contrario, cae de vuelta a "
                        "copiar cada elemento para preservar la garantía fuerte frente a excepciones (*strong exception safety guarantee*)."
                    ),
                },
            ],
            "definition": (
                "Garantía fuerte frente a excepciones (Strong Exception Safety Guarantee): propiedad de una operación en C++ "
                "según la cual, si la operación termina lanzando una excepción, el estado observable del programa permanece "
                "idéntico al que tenía antes de iniciar la operación (semántica commit-or-rollback)."
            ),
            "consejo": (
                "En C++20/C++23, no escribas jamás `new` ni `delete` desnudos en código de aplicación: utiliza `std::make_unique<T>(...)` "
                "para propiedad única (cuyo tamaño y coste en ensamblador son idénticos a un puntero crudo `T*`) y pasa vistas "
                "`std::span<const T>` o `std::string_view` cuando una función no necesite adquirir propiedad."
            ),
            "self_check": (
                "¿Por qué `std::vector<T>::push_back` se ve obligado a copiar en lugar de mover los elementos existentes al "
                "duplicar su capacidad si el constructor de movimiento `T(T&&)` no está declarado como `noexcept`?"
            ),
            "derivation": {
                "title": "Optimización de Cadena Corta (Small String Optimization, SSO) en std::string",
                "assumptions": ["En arquitecturas de 64 bits (cabecera de 24 B o 32 B), std::string almacena cadenas cortas directamente dentro del propio objeto en la pila sin llamar al asignador del montículo"],
                "steps": [
                    {"equation": r"A_{\text{heap}}(L) = 0 \quad \text{para } L \le L_{\text{SSO}}", "justification": "Cuando la longitud L no supera el umbral SSO (típicamente 15 o 22 bytes), los caracteres viven dentro de los 24 B del objeto en pila"},
                    {"equation": r"M_{\text{stack}} = 3 W = 24\text{ B}", "justification": "Tamaño fijo del objeto std::string en pila en implementaciones de 3 palabras (libc++ / libstdc++)"},
                ],
                "Verify": {"left": "3 * 8", "right": "24"},
            },
            "worked_problem": {
                "prompt": (
                    "En una implementación estándar de C++ de 64 bits donde `sizeof(std::string) = 24` bytes y la optimización de "
                    "cadena corta (*Small String Optimization*, SSO) almacena en línea cadenas de hasta $22\\text{ B}$ sin alojar "
                    "en el montículo, un programa crea un `std::vector<std::string>` con $N = 5000$ identificadores cortos de "
                    "$12\\text{ B}$ cada uno. Calcula cuántos bytes totales ocupan los 5000 objetos `std::string` dentro del búfer "
                    "contiguo del vector (sabiendo que realizan $0$ alojamientos adicionales fuera del vector)."
                ),
                "expression": "5000 * 24",
                "solution": {
                    "model": "Huella de memoria con Small String Optimization (SSO) en C++",
                    "given": [
                        {"symbol": "N", "value": "5000", "description": "Número de cadenas cortas de 12 B (<= 22 B SSO)"},
                        {"symbol": "S_str", "value": "24 B", "description": "Tamaño de cada objeto std::string en 64 bits"},
                    ],
                    "steps": [
                        {"step": "Multiplicamos las 5000 instancias por 24 B (sin alojamientos externos gracias a SSO)", "equation": r"M = 5000 \cdot 24", "expression": "5000 * 24"},
                    ],
                    "conclusion": "Los 5000 identificadores se almacenan contiguamente en 120 000 bytes con cero llamadas individuales al montículo por cadena.",
                },
            },
            "practice_problems": [
                {"prompt": "¿Cuántos bytes ocupa `std::unique_ptr<double>` con deleción por defecto en una arquitectura de 64 bits?", "expression": "8", "difficulty": "FOUNDATIONAL", "problem_type": "DIRECT_SUBSTITUTION"},
                {"prompt": "Un `std::span<const int>` en C++20 con extensión dinámica almacena un puntero (8 B) y una longitud `size_t` (8 B). ¿Cuántos bytes ocupa en la pila?", "expression": "8 + 8", "difficulty": "FOUNDATIONAL", "problem_type": "DIRECT_SUBSTITUTION"},
                {"prompt": "Un `std::vector<int>` duplica su capacidad geométricamente desde 16 hasta 1024 elementos (`sizeof(int) = 4`). ¿Cuántos bytes reserva el búfer final de 1024 enteros?", "expression": "1024 * 4", "difficulty": "INTERMEDIATE", "problem_type": "MULTI_STEP"},
                {"prompt": "Un bloque de control de `std::make_shared<T>` combina en una única reserva de montículo los dos contadores atómicos (16 B) más el objeto `T` de 48 B. ¿Cuántos bytes mide esa única reserva?", "expression": "16 + 48", "difficulty": "INTERMEDIATE", "problem_type": "DESIGN"},
            ],
        },
        {
            "id": "cap05-cpp-templates-concepts-ranges-concurrencia-proyectos",
            "title": "Monografía de C++ (II — Bloques E–H): Plantillas, Concepts C++20, std::ranges, Concurrencia, Corrutinas y Proyectos",
            "part_id": "parte-v-monografia-cpp",
            "part_title": "Monografía Autónoma de C++ (ISO/IEC 14882:2020 / C++23)",
            "sources": ["src-iso-cpp20", "src-cormen-clrs"],
            "learning_objectives": [
                "Escribir código genérico restringido semánticamente mediante C++20 Concepts (`requires`), plantillas variádicas y `if constexpr`.",
                "Componer tuberías perezosas de vistas con `std::ranges` y `std::views` evitando copias intermedias.",
                "Dominar la concurrencia en C++20 (`std::jthread`, `std::stop_token`, `std::atomic`, `std::latch`), el ecosistema CMake/Conan/vcpkg y el proyecto `projects/cpp-task-scheduler`.",
            ],
            "concepts": [
                {"id": "cpt-cpp20-concepts-ranges", "title": "Restricciones de tipos con Concepts (requires), metaprogramación constexpr y vistas perezosas std::ranges"},
                {"id": "cpt-cpp20-concurrency-projects", "title": "Concurrencia cooperativa con std::jthread, corrutinas C++20 y arquitectura de projects/cpp-task-scheduler"},
            ],
            "subsections": [
                {"id": "sec-v4-5-1", "title": "Bloques E y F: Plantillas, C++20 Concepts, std::ranges, std::jthread y corrutinas"},
                {"id": "sec-v4-5-2", "title": "Bloques G y H: Ecosistema CMake/vcpkg/Conan/Clang-Tidy y los 4 proyectos (incluyendo cpp-task-scheduler)"},
            ],
            "purpose": (
                "Este capítulo completa la monografía de C++ desarrollando los Bloques E, F, G y H: desde la programación "
                "genérica con `concept`s y `std::ranges` hasta la concurrencia cooperativa con `std::jthread` y la verificación "
                "del planificador de tareas `projects/cpp-task-scheduler`."
            ),
            "paragraphs": [
                {
                    "subsection": "sec-v4-5-1",
                    "text": (
                        "Históricamente, las plantillas (*templates*) en C++ dependían de SFINAE (*Substitution Failure Is Not An Error*), "
                        "produciendo diagnósticos de compilación crípticos cuando un tipo no cumplía una operación interna. C++20 resolvió "
                        "este problema introduciendo **Concepts**: predicados en tiempo de compilación que especifican formalmente los "
                        "requisitos sintácticos y semánticos de un parámetro de plantilla. En nuestro proyecto verificado `projects/cpp-task-scheduler`, "
                        "el concepto `ExecutableTask` exige que cualquier tipo de tarea proporcione `id()`, `priority()` convertible a "
                        "`int` y `execute()` convertible a `int64_t`:\n"
                        "```cpp\n"
                        "#include <concepts>\n"
                        "#include <cstdint>\n\n"
                        "template <typename T>\n"
                        "concept ExecutableTask = requires(const T& t) {\n"
                        "    { t.id() } -> std::convertible_to<uint32_t>;\n"
                        "    { t.priority() } -> std::convertible_to<int>;\n"
                        "    { t.execute() } -> std::convertible_to<int64_t>;\n"
                        "};\n"
                        "```\n"
                        "Junto con los conceptos, la biblioteca `<ranges>` permite encadenar vistas perezosas mediante el operador tubería "
                        "`|`, como `tasks | std::views::filter(...) | std::views::transform(...)`, y `<thread>` incorpora `std::jthread`, "
                        "que se une automáticamente (`join()`) en su destructor e integra cancelación cooperativa mediante `std::stop_token`."
                    ),
                },
                {
                    "subsection": "sec-v4-5-2",
                    "text": (
                        "En el Bloque G (Ecosistema), los proyectos profesionales de C++ se estructuran mediante `CMake` moderno basado "
                        "en objetivos (`target_link_libraries`, `target_compile_features(tgt PUBLIC cxx_std_20)`), gestores de paquetes "
                        "`vcpkg` o `Conan 2`, pruebas con `GoogleTest` o `Catch2`, benchmarking con `Google Benchmark` y auditoría "
                        "estática continua con `clang-tidy` (perfiles `cppcoreguidelines-*`, `modernize-*`, `bugprone-*`). En el Bloque H, "
                        "además de una biblioteca de álgebra lineal estática `constexpr`, un motor de eventos con `std::variant` y un "
                        "servidor de red asíncrono, el lector cuenta con el proyecto completo `projects/cpp-task-scheduler`, que implementa "
                        "una cola de prioridad determinista `TaskScheduler<Task>` verificada con `clang++ -std=c++20 -fsanitize=address,undefined`."
                    ),
                },
            ],
            "definition": (
                "Concepto en C++20 (`concept`): predicado nombrado evaluado en tiempo de compilación que restringe el conjunto "
                "de argumentos de plantilla aceptados por una función o clase genérica y participa en la resolución de sobrecarga "
                "por subsunción lógica."
            ),
            "consejo": (
                "Sustituye `std::thread` por `std::jthread` en todo código C++20 nuevo: si una función lanza una excepción antes "
                "de llamar a `.join()` sobre un `std::thread` convencional, su destructor invoca `std::terminate()` abortando el proceso."
            ),
            "self_check": (
                "¿Cómo decide el compilador de C++20 qué sobrecarga de plantilla es más específica cuando dos funciones restringidas "
                "por `concept`s distintos son válidas para un mismo tipo (regla de subsunción)?"
            ),
            "derivation": {
                "title": "Cálculo del coste acumulado ponderado en el planificador cpp-task-scheduler",
                "assumptions": ["En cpp-task-scheduler, cada tarea con prioridad >= min_priority aporta base_cost * priority"],
                "steps": [
                    {"equation": r"C_i = \text{base\_cost}_i \cdot p_i", "justification": "Método execute() de ComputeTask en scheduler.hpp"},
                    {"equation": r"C_{\text{total}} = \sum_{p_i \ge p_{\min}} \text{base\_cost}_i \cdot p_i", "justification": "Reducción del pipeline std::views::filter y std::views::transform"},
                ],
                "Verify": {"left": "c1 * p1 + c2 * p2", "right": "p1 * c1 + p2 * c2"},
            },
            "worked_problem": {
                "prompt": (
                    "En el proyecto `projects/cpp-task-scheduler`, se encolan cuatro tareas `(id, prioridad, base_cost)`: "
                    "`(1, 2, 10)`, `(2, 9, 10)`, `(3, 5, 20)` y `(4, 9, 15)`. Si se ejecuta `execute_filtered(5)` (que filtra "
                    "las tareas con `priority >= 5` y suma `base_cost * priority` de cada una), calcula el resultado exacto devuelto."
                ),
                "expression": "9 * 10 + 9 * 15 + 5 * 20",
                "solution": {
                    "model": "Filtrado y reducción en cpp-task-scheduler con std::views",
                    "given": [
                        {"symbol": "T_2", "value": "prioridad 9, coste 10", "description": "Aporta 9 * 10 = 90"},
                        {"symbol": "T_4", "value": "prioridad 9, coste 15", "description": "Aporta 9 * 15 = 135"},
                        {"symbol": "T_3", "value": "prioridad 5, coste 20", "description": "Aporta 5 * 20 = 100"},
                    ],
                    "steps": [
                        {"step": "Descartamos la tarea 1 (prioridad 2 < 5) y sumamos los productos de las tres restantes", "equation": r"R = 9 \cdot 10 + 9 \cdot 15 + 5 \cdot 20", "expression": "9 * 10 + 9 * 15 + 5 * 20"},
                    ],
                    "conclusion": "El planificador devuelve exactamente 325, coincidiendo con el test ejecutable de `projects/cpp-task-scheduler`.",
                },
            },
            "practice_problems": [
                {"prompt": "En `cpp-task-scheduler`, ¿qué valor devuelve `ComputeTask{10, 7, 12}.execute()` ($12 \\times 7$)?", "expression": "12 * 7", "difficulty": "FOUNDATIONAL", "problem_type": "DIRECT_SUBSTITUTION"},
                {"prompt": "Una plantilla variádica `sum_all(10, 20, 30, 40)` utiliza una expresión pliegue (*fold expression* `(args + ...)`). ¿Cuál es el resultado evaluado en `constexpr`?", "expression": "10 + 20 + 30 + 40", "difficulty": "FOUNDATIONAL", "problem_type": "DIRECT_SUBSTITUTION"},
                {"prompt": "Un `std::variant<int, double, std::array<char, 32>>` almacena la alternativa mayor (32 B) más un índice alineado a 8 B. ¿Cuántos bytes ocupa la instancia?", "expression": "32 + 8", "difficulty": "INTERMEDIATE", "problem_type": "MULTI_STEP"},
                {"prompt": "Si una vista `std::views::iota(1, 1001) | std::views::filter(...) | std::views::take(5)` detiene la evaluación al encontrar los primeros 5 pares ($2, 4, 6, 8, 10$), ¿cuántos enteros del rango $[1, 1000]$ llegaron a inspeccionarse?", "expression": "10", "difficulty": "INTERMEDIATE", "problem_type": "DESIGN"},
            ],
        },
        {
            "id": "cap06-monografia-zig-asignadores-comptime-interoperabilidad-c",
            "title": "Monografía de Zig (Bloques A–H): Asignadores explícitos, metaprogramación comptime, uniones de error y toolchain C",
            "part_id": "parte-v-zig-asm-ada-fortran",
            "part_title": "Monografías Especializadas de Sistemas: Zig, Ensamblador, Ada y Fortran",
            "sources": ["src-iso-c17", "src-bryant-ohallaron"],
            "learning_objectives": [
                "Comprender los principios de diseño de Zig: ausencia de flujo de control oculto, ausencia de asignaciones implícitas de montículo y ausencia de preprocesador.",
                "Programar con uniones de error (`!T`), limpieza diferida determinista (`defer` y `errdefer`), rebanadas con longitud y asignadores explícitos (`std.mem.Allocator`).",
                "Utilizar `comptime` para tipos genéricos y evaluación en tiempo de compilación, e integrar cabeceras C con `@cImport`.",
            ],
            "concepts": [
                {"id": "cpt-zig-allocators-errdefer", "title": "Inyección explícita de std.mem.Allocator, uniones de error (!T) y limpieza con defer/errdefer"},
                {"id": "cpt-zig-comptime-c-interop", "title": "Generación de tipos en comptime sin lenguaje de macros separado y compilación cruzada C/Zig"},
            ],
            "subsections": [
                {"id": "sec-v4-6-1", "title": "Bloques A–D: Filosofía de Zig, toolchain integrada, tipos, rebanadas, uniones de error y defer/errdefer"},
                {"id": "sec-v4-6-2", "title": "Bloques E–H: Asignadores explícitos (Arena, FixedBuffer, GPA), comptime, FFI con C y proyectos"},
            ],
            "purpose": (
                "Este capítulo presenta la monografía completa de **Zig** siguiendo los bloques A–H. Creado por Andrew Kelley, "
                "Zig se concibe como un sucesor moderno y transparente de C donde ninguna expresión oculta llamadas a funciones "
                "ni reservas de memoria, los tipos son valores de primera clase en tiempo de compilación (`comptime`) y el "
                "propio binario `zig` incluye un compilador C/C++ de compilación cruzada basado en Clang/LLVM."
            ),
            "paragraphs": [
                {
                    "subsection": "sec-v4-6-1",
                    "text": (
                        "Zig se rige por tres mandamientos de ingeniería de sistemas: (1) sin flujo de control oculto (no hay sobrecarga "
                        "de operadores, ni constructores/destructores implícitos, ni excepciones); (2) sin asignaciones de memoria ocultas "
                        "(toda función de la biblioteca estándar que necesita alojar en el montículo recibe explícitamente un parámetro "
                        "`allocator: std.mem.Allocator`); y (3) sin preprocesador de macros textuales. Para gestionar recursos y errores "
                        "con precisión quirúrgica, Zig combina tipos de unión de error (`AllocError![]u8`) con las palabras clave `try`, "
                        "`catch`, `defer` (que se ejecuta al salir del bloque actual) y `errdefer` (que se ejecuta **únicamente** si el "
                        "bloque actual retorna con un error):\n"
                        "```zig\n"
                        "const std = @import(\"std\");\n\n"
                        "pub fn allocateInitializedRing(allocator: std.mem.Allocator, n: usize) ![]u64 {\n"
                        "    const buf = try allocator.alloc(u64, n);\n"
                        "    errdefer allocator.free(buf);\n"
                        "    for (buf, 0..) |*slot, idx| {\n"
                        "        slot.* = @as(u64, @intCast(idx)) * 10;\n"
                        "    }\n"
                        "    return buf;\n"
                        "}\n"
                        "```\n"
                        "Si cualquier paso posterior dentro de la función fallara y retornara un error mediante `try`, `errdefer` "
                        "libera automáticamente `buf` sin necesidad de etiquetas `goto`."
                    ),
                },
                {
                    "subsection": "sec-v4-6-2",
                    "text": (
                        "En lugar de plantillas o macros, el polimorfismo paramétrico en Zig consiste en funciones ordinarias que "
                        "aceptan argumentos `comptime T: type` y devuelven un `type` (`fn BoundedQueue(comptime T: type, comptime cap: usize) type`). "
                        "Gracias a que los asignadores se pasan como valores de interfaz `std.mem.Allocator`, el mismo contenedor "
                        "`std.ArrayList(T)` puede ejecutarse sobre el asignador detector de fugas `std.testing.allocator` durante "
                        "`zig test`, sobre un `std.heap.ArenaAllocator` por petición HTTP, o sobre un `std.heap.FixedBufferAllocator` "
                        "respaldado por un array estático en la pila sin tocar jamás el sistema operativo."
                    ),
                },
            ],
            "definition": (
                "Limpieza condicional de error (`errdefer` en Zig): sentencia registrada en la pila léxica del bloque actual "
                "cuya expresión asociada se ejecuta si y solo si la función abandona dicho ámbito devolviendo un valor de error "
                "de su unión de retorno `!T`."
            ),
            "consejo": (
                "En todas tus pruebas unitarias de Zig (`test \"...\" { ... }`), pasa siempre `std.testing.allocator` a las estructuras "
                "bajo prueba: el arnés de pruebas hará fallar automáticamente el test si queda un solo byte sin liberar o si ocurre doble liberación."
            ),
            "self_check": (
                "¿Qué ventaja arquitectónica aporta que `std.ArrayList` en Zig reciba un `Allocator` explícito en lugar de invocar "
                "un asignador global fijo como `std::vector` por defecto en C++ o `Vec<T>` en Rust estable?"
            ),
            "derivation": {
                "title": "Capacidad máxima de objetos en un FixedBufferAllocator de Zig",
                "assumptions": ["Un búfer estático de B bytes aloja objetos ya alineados de tamaño S_obj sin metadatos por objeto"],
                "steps": [
                    {"equation": r"N_{\max} = \lfloor B / S_{\text{obj}} \rfloor", "justification": "El asignador lineal avanza el índice end_index en S_obj bytes por cada reserva"},
                    {"equation": r"B_{\text{rem}} = B - N_{\max} \cdot S_{\text{obj}}", "justification": "Bytes sobrantes insuficientes para una instancia adicional"},
                ],
                "Verify": {"left": "B - (B - B_rem)", "right": "B_rem"},
            },
            "worked_problem": {
                "prompt": (
                    "En un microservicio escrito en Zig, cada petición HTTP utiliza un `std.heap.FixedBufferAllocator` respaldado por "
                    "un array en pila de $B = 16384\\text{ B}$ ($16\\text{ KiB}$). Si el manejador aloja una cabecera parseada de "
                    "$512\\text{ B}$ y $N = 60$ cabeceras clave-valor de $128\\text{ B}$ cada una, calcula cuántos bytes quedan "
                    "disponibles en el `FixedBufferAllocator` antes de que devuelva `error.OutOfMemory`."
                ),
                "expression": "16384 - (512 + 60 * 128)",
                "solution": {
                    "model": "Contabilidad lineal en FixedBufferAllocator de Zig",
                    "given": [
                        {"symbol": "B", "value": "16384 B", "description": "Capacidad total del búfer estático en pila"},
                        {"symbol": "S_hdr", "value": "512 B", "description": "Reserva inicial para el descriptor de petición"},
                        {"symbol": "N, S_kv", "value": "60, 128 B", "description": "60 pares clave-valor de 128 B"},
                    ],
                    "steps": [
                        {"step": "Restamos los 512 B y los 60 * 128 = 7680 B a la capacidad total de 16384 B", "equation": r"B_{\text{libre}} = 16384 - (512 + 60 \cdot 128)", "expression": "16384 - (512 + 60 * 128)"},
                    ],
                    "conclusion": "Quedan exactamente 8192 bytes (8 KiB) libres en el búfer de la petición.",
                },
            },
            "practice_problems": [
                {"prompt": "Una rebanada `[]const u32` en Zig de 64 bits consta de un puntero `[*]const u32` (8 B) y una longitud `usize` (8 B). ¿Cuántos bytes ocupa?", "expression": "8 + 8", "difficulty": "FOUNDATIONAL", "problem_type": "DIRECT_SUBSTITUTION"},
                {"prompt": "En Zig, el tipo entero de anchura arbitraria `u12` se aloja en memoria ocupando el siguiente número entero de bytes potencia de dos (`@sizeOf(u12)`). ¿Cuántos bytes ocupa en memoria?", "expression": "2", "difficulty": "FOUNDATIONAL", "problem_type": "DIRECT_SUBSTITUTION"},
                {"prompt": "Un `packed struct` de Zig contiene campos `u3`, `u5`, `u16` y `u8` empaquetados al bit exacto. ¿Cuántos bytes ocupa `(3 + 5 + 16 + 8) / 8`?", "expression": "(3 + 5 + 16 + 8) / 8", "difficulty": "INTERMEDIATE", "problem_type": "MULTI_STEP"},
                {"prompt": "Si una función con 4 reservas secuenciales protegidas cada una por `errdefer` falla en la cuarta reserva, ¿cuántos bloques previos son liberados automáticamente por los `errdefer` ya registrados?", "expression": "3", "difficulty": "INTERMEDIATE", "problem_type": "DESIGN"},
            ],
        },
        {
            "id": "cap07-monografia-ensamblador-arm64-x86-64-abi-simd",
            "title": "Monografía de Ensamblador ARM64 (AArch64) y x86-64 (Bloques A–H): Registros, ABI, Pila y SIMD",
            "part_id": "parte-v-zig-asm-ada-fortran",
            "part_title": "Monografías Especializadas de Sistemas: Zig, Ensamblador, Ada y Fortran",
            "sources": ["src-bryant-ohallaron", "src-patterson-hennessy"],
            "learning_objectives": [
                "Distinguir la arquitectura RISC de carga/almacenamiento AArch64 (ARM64) frente a la arquitectura CISC de longitud variable x86-64.",
                "Dominar las convenciones de llamada ABI System V AMD64 (`rdi, rsi, rdx, rcx, r8, r9` y retorno en `rax`) y AAPCS64 (`x0–x7` y retorno en `x0`).",
                "Analizar el prólogo y epílogo de marcos de pila, el alineamiento obligatorio de 16 bytes del puntero de pila (`sp`/`rsp`) e instrucciones vectoriales SIMD.",
            ],
            "concepts": [
                {"id": "cpt-asm-registers-abi", "title": "Banco de registros, registros preservados por llamador vs llamado y convenciones System V x86-64 y AAPCS64 ARM64"},
                {"id": "cpt-asm-stack-frame-simd", "title": "Alineamiento de 16 bytes del puntero de pila, puntero de marco (fp/rbp) y registros vectoriales NEON/AVX2"},
            ],
            "subsections": [
                {"id": "sec-v4-7-1", "title": "Bloques A–D: Arquitectura de registros x86-64 y ARM64 (AArch64), modos de direccionamiento y saltos"},
                {"id": "sec-v4-7-2", "title": "Bloques E–H: Convenciones ABI (System V y AAPCS64), alineamiento de pila, SIMD (NEON/AVX) e inspección con objdump"},
            ],
            "figure": {
                "key": "fig-abi-calling-conventions",
                "caption": "Comparativa de paso de los primeros 6 argumentos enteros/punteros y valor de retorno entre la ABI System V x86-64 y la ABI AAPCS64 (ARM64).",
                "tikz": r"""\begin{tikzpicture}[node distance=1.4cm, >=stealth, thick, font=\small]
\node[draw=blue!70!black, fill=blue!8, rounded corners, minimum width=5.6cm, minimum height=1.8cm, align=center] (x86) {\textbf{System V AMD64 (x86-64)}\\Args 1--6: \texttt{rdi, rsi, rdx, rcx, r8, r9}\\Retorno: \texttt{rax} (\texttt{rdx})\\Callee-saved: \texttt{rbx, rbp, r12--r15}};
\node[draw=teal!70!black, fill=teal!10, rounded corners, minimum width=5.6cm, minimum height=1.8cm, align=center, right=0.8cm of x86] (arm) {\textbf{AAPCS64 (ARM64 / AArch64)}\\Args 1--8: \texttt{x0, x1, x2, x3, x4, x5, x6, x7}\\Retorno: \texttt{x0} (\texttt{x1})\\Callee-saved: \texttt{x19--x28, x29(fp), x30(lr)}};
\end{tikzpicture}""",
            },
            "purpose": (
                "Todo ingeniero de sistemas debe ser capaz de leer el código ensamblador emitido por el compilador (`clang -S -O2` "
                "u `objdump -d`), diagnosticar volcados de pila y escribir rutinas críticas vectorizadas o cambios de contexto de "
                "sistema operativo. Este capítulo ofrece el bloque completo A–H para las dos arquitecturas dominantes de 64 bits: "
                "**x86-64 (AMD64)** y **ARM64 (AArch64)**."
            ),
            "paragraphs": [
                {
                    "subsection": "sec-v4-7-1",
                    "text": (
                        "En **x86-64**, la CPU dispone de 16 registros de propósito general de 64 bits (`rax`, `rbx`, `rcx`, `rdx`, "
                        "`rsi`, `rdi`, `rbp`, `rsp`, `r8`–`r15`) e instrucciones de longitud variable (de 1 a 15 bytes) que permiten "
                        "combinar acceso a memoria y operación aritmética en una sola instrucción. En **ARM64 (AArch64)**, la arquitectura "
                        "es estrictamente *load/store* con instrucciones de anchura fija de 32 bits (4 bytes) y 31 registros de propósito "
                        "general de 64 bits (`x0`–`x30`, con sus mitades inferiores de 32 bits `w0`–`w30`), más el registro cero `xzr` "
                        "y el puntero de pila `sp`. En ARM64, las operaciones aritméticas operan exclusivamente entre registros; la "
                        "memoria solo se toca mediante instrucciones de carga y almacenamiento como `ldr`, `str`, `ldp` (cargar par de "
                        "registros) y `stp` (almacenar par de registros)."
                    ),
                },
                {
                    "subsection": "sec-v4-7-2",
                    "text": (
                        "Para que módulos compilados por distintos lenguajes (C, C++, Rust, Zig) puedan invocarse entre sí, deben "
                        "respetar la **ABI** (*Application Binary Interface*) de la plataforma. Como resume la Figura \\ref{fig:fig-abi-calling-conventions}, "
                        "en la ABI System V x86-64 (Linux, macOS, BSD) los primeros 6 argumentos enteros o punteros se pasan en "
                        "`rdi`, `rsi`, `rdx`, `rcx`, `r8`, `r9`, mientras que en AAPCS64 (ARM64) los primeros 8 se pasan en `x0`–`x7`. "
                        "En ambas arquitecturas, el puntero de pila (`rsp` o `sp`) debe mantenerse alineado a un múltiplo de **16 bytes** "
                        "en el punto de llamada a cualquier función (`call` o `bl`). Compare la misma función `uint64_t fma_u64(uint64_t a, uint64_t b, uint64_t c)` "
                        "que calcula $a \\cdot b + c$ en ambas arquitecturas:\n"
                        "```nasm\n"
                        "; System V x86-64 (a=rdi, b=rsi, c=rdx -> retorno en rax):\n"
                        "fma_u64_x86:\n"
                        "    mov     rax, rdi\n"
                        "    imul    rax, rsi\n"
                        "    add     rax, rdx\n"
                        "    ret\n\n"
                        "; AAPCS64 ARM64 (a=x0, b=x1, c=x2 -> retorno en x0, una sola instrucción madd):\n"
                        "fma_u64_arm64:\n"
                        "    madd    x0, x0, x1, x2   ; x0 = (x0 * x1) + x2\n"
                        "    ret\n"
                        "```\n"
                        "En ARM64, el prólogo estándar de una función no hoja guarda el puntero de marco `x29` (`fp`) y el registro de "
                        "enlace `x30` (`lr`) reservando un múltiplo de 16 bytes en una sola instrucción con pre-indexación: "
                        "`stp x29, x30, [sp, #-16]!`."
                    ),
                },
            ],
            "definition": (
                "Registros preservados por el llamado (Callee-saved registers): subconjunto de registros de la CPU (`rbx, rbp, r12–r15` "
                "en System V x86-64; `x19–x28, x29, x30` en AAPCS64) cuyo valor original debe ser restaurado por cualquier subrutina "
                "antes de ejecutar `ret` si dicha subrutina decide modificarlos."
            ),
            "consejo": (
                "En lugar de escribir funciones enteras en ensamblador manual que dificultan las optimizaciones del compilador, "
                "prefiere funciones intrínsecas SIMD (`<arm_neon.h>` o `<immintrin.h>`) y verifica el ensamblador generado con "
                "`clang -O3 -S`."
            ),
            "self_check": (
                "¿Por qué en x86-64 al entrar en el cuerpo de una función tras ejecutar la instrucción `call` (que empuja 8 bytes "
                "de dirección de retorno en la pila), el registro `rsp` tiene un valor congruente con 8 módulo 16 y requiere "
                "restar $8 + 16k$ bytes antes de hacer otro `call`?"
            ),
            "derivation": {
                "title": "Alineamiento de marco de pila a múltiplo de 16 bytes en ARM64 y x86-64",
                "assumptions": ["La ABI exige que el tamaño de reserva del marco de pila S_frame sea múltiplo exacto de 16 bytes"],
                "steps": [
                    {"equation": r"S_{\text{raw}} = S_{\text{saved\_regs}} + S_{\text{locals}}", "justification": "Suma de registros callee-saved guardados más variables locales en pila"},
                    {"equation": r"S_{\text{frame}} = 16 \cdot \lceil S_{\text{raw}} / 16 \rceil", "justification": "Redondeo hacia arriba al siguiente múltiplo de 16 bytes exigido por la ABI"},
                ],
                "Verify": {"left": "S_saved_regs + S_locals", "right": "S_locals + S_saved_regs"},
            },
            "worked_problem": {
                "prompt": (
                    "Una función en ensamblador ARM64 guarda en la pila el par `(x29, x30)` ($16\\text{ B}$), dos registros "
                    "preservados `(x19, x20)` ($16\\text{ B}$) y necesita alojar un búfer local de $36\\text{ B}$. Como el "
                    "hardware AArch64 exige que el puntero de pila `sp` permanezca siempre alineado a múltiplo de $16\\text{ B}$ "
                    "(redondeando los $36\\text{ B}$ locales hacia arriba a $48\\text{ B}$), calcula cuántos bytes totales "
                    "resta al registro `sp` el prólogo de la función."
                ),
                "expression": "16 + 16 + 48",
                "solution": {
                    "model": "Cálculo del tamaño de marco de pila alineado a 16 bytes en AAPCS64",
                    "given": [
                        {"symbol": "S_fplr", "value": "16 B", "description": "Par de registros (x29, x30)"},
                        {"symbol": "S_callee", "value": "16 B", "description": "Par de registros preservados (x19, x20)"},
                        {"symbol": "S_local_aligned", "value": "48 B", "description": "36 B redondeados al siguiente múltiplo de 16 B"},
                    ],
                    "steps": [
                        {"step": "Sumamos los tres bloques alineados a 16 bytes", "equation": r"S_{\text{frame}} = 16 + 16 + 48", "expression": "16 + 16 + 48"},
                    ],
                    "conclusion": "El prólogo reserva exactamente 80 bytes (múltiplo exacto de 16: 5 * 16 = 80 B) en la pila.",
                },
            },
            "practice_problems": [
                {"prompt": "En ARM64, cada instrucción máquina tiene una anchura fija de 32 bits (4 bytes). ¿Cuántos bytes ocupan en la sección `.text` una secuencia de 250 instrucciones?", "expression": "250 * 4", "difficulty": "FOUNDATIONAL", "problem_type": "DIRECT_SUBSTITUTION"},
                {"prompt": "Un registro vectorial NEON de 128 bits en ARM64 (`v0.4s`) procesa enteros o flotantes de 32 bits en paralelo. ¿Cuántos elementos de 32 bits opera por instrucción?", "expression": "128 / 32", "difficulty": "FOUNDATIONAL", "problem_type": "DIRECT_SUBSTITUTION"},
                {"prompt": "Una función en System V x86-64 recibe 9 argumentos enteros de 64 bits. Sabiendo que los primeros 6 van en registros y el resto se pasa por la pila (8 B cada uno), ¿cuántos bytes ocupan en la pila los argumentos restantes?", "expression": "(9 - 6) * 8", "difficulty": "INTERMEDIATE", "problem_type": "MULTI_STEP"},
                {"prompt": "Un bucle procesa un array de 4096 flotantes `f32` utilizando instrucciones AVX-512 (16 flotantes `f32` por registro de 512 bits). ¿Cuántas iteraciones vectoriales ejecuta el bucle?", "expression": "4096 / 16", "difficulty": "INTERMEDIATE", "problem_type": "DESIGN"},
            ],
        },
        {
            "id": "cap08-monografias-ada-spark-tiempo-real-y-fortran-cientifico",
            "title": "Monografías de Ada/SPARK (Sistemas Críticos) y Fortran Moderno (Cómputo Científico HPC) (Bloques A–H)",
            "part_id": "parte-v-zig-asm-ada-fortran",
            "part_title": "Monografías Especializadas de Sistemas: Zig, Ensamblador, Ada y Fortran",
            "sources": ["src-ieee-754", "src-knuth-taocp"],
            "learning_objectives": [
                "Diseñar tipos escalares con rangos restringidos, contratos ejecutables (`Pre`, `Post`, `Type_Invariant`) y tareas críticas bajo el perfil Ravenscar en Ada 2022 y SPARK.",
                "Comprender cómo el demostrador formal GNATprove en SPARK demuestra estáticamente la ausencia de errores en tiempo de ejecución (AoRTE).",
                "Programar cálculo numérico de alto rendimiento en Fortran 2018/2023 mediante operaciones matriciales intrínsecas, `intent(in/out)`, módulos y paralelismo Coarray.",
            ],
            "concepts": [
                {"id": "cpt-ada-spark-ravenscar", "title": "Tipos de rango fuerte, programación por contrato en Ada 2022/SPARK y concurrencia determinista Ravenscar"},
                {"id": "cpt-fortran-arrays-coarrays", "title": "Semántica de arrays sin alias por defecto en Fortran 2018/2023, orden por columnas y paralelismo PGAS Coarray"},
            ],
            "subsections": [
                {"id": "sec-v4-8-1", "title": "Monografía de Ada 2022 y SPARK (Bloques A–H): Tipado fuerte de dominio, contratos y sistemas críticos"},
                {"id": "sec-v4-8-2", "title": "Monografía de Fortran 2018/2023 (Bloques A–H): Arrays multidimensionales, vectorización y Coarrays"},
            ],
            "purpose": (
                "Este capítulo cierra el Volumen IV con las monografías completas de dos lenguajes insustituibles en sus dominios "
                "de alta exigencia: **Ada 2022 / SPARK** en aviónica (DO-178C Nivel A), ferrocarriles y espacio, y **Fortran 2018/2023** "
                "en supercomputación (HPC), dinámica de fluidos computacional (CFD) y predicción meteorológica."
            ),
            "paragraphs": [
                {
                    "subsection": "sec-v4-8-1",
                    "text": (
                        "Encargado por el Departamento de Defensa de EE. UU. (Jean Ichbiah, 1980; revisiones ISO Ada 95, 2005, 2012 y 2022), "
                        "**Ada** fue diseñado para sistemas embebidos de misión crítica donde un defecto de software puede costar vidas "
                        "humanas. En Ada, el ingeniero no declara variables como meros `int`, sino que define tipos nominalmente distintos "
                        "con su rango físico exacto: `type Altitude_Meters is range -500 .. 50_000;` y `type Velocity_Knots is range 0 .. 2_500;`. "
                        "Sumar una altitud con una velocidad es un error de compilación inmediato, y asignar un valor fuera de rango lanza "
                        "`Constraint_Error`. En el subconjunto formalmente verificable **SPARK**, los aspectos `Pre`, `Post` y `Global` "
                        "se traducen en obligaciones de prueba matemática descargadas por solucionadores SMT (`Z3`, `Alt-Ergo`) mediante "
                        "`gnatprove`, demostrando la ausencia total de desbordamientos o divisiones por cero antes de compilar:\n"
                        "```ada\n"
                        "package Flight_Envelope with SPARK_Mode is\n"
                        "   type Altitude_M is range 0 .. 20_000;\n"
                        "   function Safe_Climb (Current : Altitude_M; Delta_H : Altitude_M) return Altitude_M\n"
                        "     with Pre  => Integer (Current) + Integer (Delta_H) <= 20_000,\n"
                        "          Post => Safe_Climb'Result = Current + Delta_H;\n"
                        "end Flight_Envelope;\n"
                        "```\n"
                        "Para concurrencia de tiempo real duro, el perfil **Ravenscar** restringe las tareas (`task`) y los objetos "
                        "protegidos (`protected object`) al protocolo de techo de prioridad inmediata (*Immediate Ceiling Priority Protocol*), "
                        "garantizando ausencia matemática de interbloqueos (*deadlocks*) y acotación estática del tiempo de respuesta."
                    ),
                },
                {
                    "subsection": "sec-v4-8-2",
                    "text": (
                        "Por su parte, **Fortran** (John Backus, IBM, 1957; modernizado radicalmente en Fortran 90/95, 2003, 2008, "
                        "2018 y 2023) sigue siendo el estándar de oro en supercomputación científica por dos razones técnicas: primero, "
                        "los arrays multidimensionales son ciudadanos de primera clase almacenados en **orden mayor por columnas** "
                        "(*column-major*, donde `A(i, j)` es contiguo en memoria al variar el primer índice `i`); segundo, el estándar "
                        "Fortran garantiza por defecto que los argumentos `intent(in)` e `intent(inout)` de una subrutina `pure` **no "
                        "presentan alias entre sí** (a menos que tengan el atributo `pointer` o `target`), lo que permite a compiladores "
                        "como `gfortran`, `ifx` o `nvfortran` vectorizar bucles matriciales con una agresividad superior a la de C sin "
                        "`restrict`:\n"
                        "```fortran\n"
                        "module numerics_mod\n"
                        "  use, intrinsic :: iso_fortran_env, only: dp => real64\n"
                        "  implicit none\n"
                        "contains\n"
                        "  pure subroutine laplacian_1d(u, d2u, inv_dx2)\n"
                        "    real(dp), intent(in)  :: u(:), inv_dx2\n"
                        "    real(dp), intent(out) :: d2u(:)\n"
                        "    integer :: n\n"
                        "    n = size(u)\n"
                        "    d2u(1) = 0.0_dp\n"
                        "    d2u(2:n-1) = (u(1:n-2) - 2.0_dp * u(2:n-1) + u(3:n)) * inv_dx2\n"
                        "    d2u(n) = 0.0_dp\n"
                        "  end subroutine laplacian_1d\n"
                        "end module numerics_mod\n"
                        "```\n"
                        "Además, Fortran 2008/2018 incorpora paralelismo de memoria distribuida directamente en la sintaxis del lenguaje "
                        "mediante **Coarrays** (`real(dp) :: field(1000)[*]`), donde la notación entre corchetes `[imagen]` realiza "
                        "transferencias RDMA de un solo lado entre nodos de un clúster sin llamadas verbosas a MPI."
                    ),
                },
            ],
            "definition": (
                "Orden mayor por columnas (Column-Major Order en Fortran): disposición lineal en memoria de un array bidimensional "
                "$A(1..M, 1..N)$ según la cual el elemento $A(i, j)$ (con índices basados en 1) se ubica en el desplazamiento "
                "lineal $(j - 1) \\cdot M + (i - 1)$, haciendo contiguos los elementos de una misma columna."
            ),
            "consejo": (
                "En Fortran moderno, comienza siempre todo módulo y programa con `implicit none` e importa `real64` (`dp`) e "
                "`int64` desde el módulo estándar `iso_fortran_env`; al anidar bucles sobre `A(i, j)`, sitúa siempre el índice "
                "`i` en el bucle más interno y `j` en el externo para recorrer la memoria secuencialmente."
            ),
            "self_check": (
                "¿Por qué intercambiar el orden de los bucles `do i = 1, M; do j = 1, N` sobre `A(i, j)` en Fortran degrada "
                "severamente la tasa de aciertos de caché L1 respecto a `do j = 1, N; do i = 1, M`?"
            ),
            "derivation": {
                "title": "Índice lineal en orden por columnas (Column-Major) de Fortran",
                "assumptions": ["Una matriz Fortran A(1..M, 1..N) indexada desde 1 con elementos de tamaño S bytes a partir de la dirección base B_0"],
                "steps": [
                    {"equation": r"k(i, j) = (j - 1) \cdot M + (i - 1)", "justification": "Cada columna completa anterior (j - 1) contiene M elementos contiguos"},
                    {"equation": r"\text{Addr}(i, j) = B_0 + S \cdot ((j - 1) \cdot M + (i - 1))", "justification": "Escalamiento por el tamaño S en bytes de cada elemento real(real64)"},
                ],
                "Verify": {"left": "(j - 1) * M + (i - 1)", "right": "j * M - M + i - 1"},
            },
            "worked_problem": {
                "prompt": (
                    "En un programa Fortran 2018, una matriz `real(real64) :: A(100, 200)` ($M = 100$ filas, $N = 200$ columnas, "
                    "$S = 8\\text{ B}$ por elemento) está almacenada en orden mayor por columnas a partir del desplazamiento base $0$. "
                    "Calcula el desplazamiento exacto en bytes del elemento `A(25, 4)` usando la fórmula $8 \\cdot ((4 - 1) \\cdot 100 + (25 - 1))$."
                ),
                "expression": "8 * ((4 - 1) * 100 + (25 - 1))",
                "solution": {
                    "model": "Direccionamiento Column-Major en Fortran",
                    "given": [
                        {"symbol": "M", "value": "100", "description": "Número de filas por columna"},
                        {"symbol": "i, j", "value": "25, 4", "description": "Fila 25, columna 4 (base 1)"},
                        {"symbol": "S", "value": "8 B", "description": "Tamaño de real(real64)"},
                    ],
                    "steps": [
                        {"step": "Calculamos el índice lineal (3 * 100 + 24 = 324) y multiplicamos por 8 bytes", "equation": r"\text{Offset} = 8 \cdot ((4 - 1) \cdot 100 + (25 - 1))", "expression": "8 * ((4 - 1) * 100 + (25 - 1))"},
                    ],
                    "conclusion": "El elemento A(25, 4) se encuentra exactamente a 2592 bytes del inicio de la matriz.",
                },
            },
            "practice_problems": [
                {"prompt": "En Ada, el tipo `type Percent is range 0 .. 100;` comprende desde 0 hasta 100 ambos inclusive. ¿Cuántos valores distintos pertenecen al tipo (`Percent'Last - Percent'First + 1`)?", "expression": "100 - 0 + 1", "difficulty": "FOUNDATIONAL", "problem_type": "DIRECT_SUBSTITUTION"},
                {"prompt": "En Fortran, una rebanada vectorial `u(2:n-1)` para $n = 1002$ evalúa los puntos interiores de una malla 1D. ¿Cuántos puntos interiores actualiza la sentencia?", "expression": "(1002 - 1) - 2 + 1", "difficulty": "FOUNDATIONAL", "problem_type": "DIRECT_SUBSTITUTION"},
                {"prompt": "Un programa Coarray Fortran se ejecuta en 16 imágenes (`num_images() = 16`) y cada imagen aloja una malla local de $50000$ flotantes `real64` (8 B). ¿Cuántos bytes suman las mallas de las 16 imágenes?", "expression": "16 * 50000 * 8", "difficulty": "INTERMEDIATE", "problem_type": "MULTI_STEP"},
                {"prompt": "En un sistema de tiempo real Ada Ravenscar con periodo de marco mayor $T = 100\\text{ ms}$, tres tareas periódicas consumen $15\\text{ ms}$, $22\\text{ ms}$ y $18\\text{ ms}$ por cada $100\\text{ ms}$. ¿Cuál es el porcentaje entero de utilización total de CPU?", "expression": "15 + 22 + 18", "difficulty": "INTERMEDIATE", "problem_type": "DESIGN"},
            ],
        },
    ],
}

VOL05_SPEC: dict[str, object] = {
    "slug": "vol05-monografias-python-js-ts",
    "code": "ENC-VOL05",
    "title": "Volumen V: Monografías de Python, JavaScript y TypeScript",
    "subtitle": "Parte V (Bloques A–H): De cero a máquinas virtuales de bytecode, asincronía, Event Loop V8 y sistemas de tipos estructurales",
    "target_pages": 68,
    "terminology": [
        {"term": "tipado estructural (structural typing)", "canonical": "tipado estructural (structural typing)", "forbidden": ["tipado nominal débil"]},
        {"term": "bucle de eventos (Event Loop)", "canonical": "bucle de eventos (Event Loop)", "forbidden": ["hilo rotatorio"]},
        {"term": "protocolo descriptor (descriptor protocol)", "canonical": "protocolo descriptor (descriptor protocol)", "forbidden": ["getter oculto"]},
    ],
    "notation": [
        {"symbol": r"\text{refcnt}(o)", "meaning": "Contador de referencias de un PyObject en CPython", "unit": "referencias"},
        {"symbol": r"T \text{ extends } U ? X : Y", "meaning": "Tipo condicional distributivo en el sistema de tipos de TypeScript", "unit": "tipo"},
        {"symbol": r"\tau_{\text{micro}}, \tau_{\text{macro}}", "meaning": "Colas de microtareas (Promises) y macrotareas (timers/I/O) del Event Loop", "unit": "tareas"},
    ],
    "chapters": [
        {
            "id": "cap01-python-fundamentos-modelo-objetos-nivel-principiante",
            "title": "Monografía de Python (I — Bloques A, B y C): Historia, CPython, Entorno (uv/venv) y Nivel Principiante",
            "part_id": "parte-v-monografia-python",
            "part_title": "Monografía Autónoma de Python (Python 3.12 – 3.14)",
            "sources": ["src-python-ref", "src-unicode-15"],
            "learning_objectives": [
                "Comprender la historia de Python (Guido van Rossum, 1991), la transición Python 2 a 3 y el modelo de ejecución de bytecode de CPython (incluyendo el compilador especializador PEP 659 y el modo free-threaded PEP 703).",
                "Configurar entornos reproducibles conforme a PEP 517/518/621 (`pyproject.toml`, `venv`, `uv`, `ruff`, `pyright`, `pytest`).",
                "Dominar la semántica de nombres vinculados a objetos (`PyObject`), mutabilidad vs inmutabilidad, tipos básicos y estructuras de datos nativas (`list`, `tuple`, `dict`, `set`).",
            ],
            "concepts": [
                {"id": "cpt-py-object-model-bytecode", "title": "Modelo de referencias a PyObject, conteo de referencias + GC cíclico y compilación a bytecode CPython"},
                {"id": "cpt-py-collections-comprehensions", "title": "Complejidad algorítmica de list, dict (tablas hash compactas) y set, comprensiones y coincidencia estructural match/case"},
            ],
            "subsections": [
                {"id": "sec-v5-1-1", "title": "Bloques A y B: Historia, máquina virtual CPython, GIL / Free-Threading y toolchain moderna (uv, ruff, pyright)"},
                {"id": "sec-v5-1-2", "title": "Bloque C: Modelo de nombres y objetos, tipos nativos, colecciones, comprensiones y control de flujo (match/case)"},
            ],
            "figure": {
                "key": "fig-cpython-object-layout",
                "caption": "Diferencia semántica fundamental en Python: las variables no son cajas con tipo fijo, sino etiquetas en un diccionario de espacio de nombres que apuntan a estructuras PyObject en el montículo con cabecera ob_refcnt y ob_type.",
                "tikz": r"""\begin{tikzpicture}[node distance=1.8cm, >=stealth, thick, font=\small]
\node[draw=blue!70!black, fill=blue!8, rounded corners, minimum width=2.8cm, minimum height=1.2cm, align=center] (ns) {Marco Léxico\\(\texttt{locals()})\\\texttt{"a"} $\bullet$\quad \texttt{"b"} $\bullet$};
\node[draw=orange!75!black, fill=orange!12, rounded corners, minimum width=4.6cm, minimum height=1.4cm, align=center, right=1.8cm of ns] (obj) {\texttt{PyLongObject} en Montículo\\\texttt{ob\_refcnt = 2}\\\texttt{ob\_type = \&PyLong\_Type}\\\texttt{ob\_digit = 42}};
\draw[->] (ns.15) -- (obj.165);
\draw[->] (ns.345) -- (obj.195);
\end{tikzpicture}""",
            },
            "purpose": (
                "Este capítulo inaugura la monografía autónoma de **Python** (Bloques A, B y C). Python es simultáneamente el "
                "lenguaje hegemónico en ciencia de datos, inteligencia artificial y automatización, y un lenguaje de ingeniería "
                "de software de primer orden para backends web y herramientas de infraestructura. El lector aprenderá su modelo "
                "exacto de ejecución bajo el capó de CPython."
            ),
            "paragraphs": [
                {
                    "subsection": "sec-v5-1-1",
                    "text": (
                        "Creado por Guido van Rossum en el CWI de Ámsterdam y publicado en 1991, Python ejecuta el código fuente "
                        "compilándolo primero a un árbol de sintaxis abstracta (AST) y seguidamente a código de bytes (*bytecode*, "
                        "inspeccionable con el módulo estándar `dis`) interpretado por una máquina virtual de pila en CPython. Cada "
                        "valor en Python —incluidos los enteros y las propias clases— es una estructura `PyObject` en el montículo "
                        "que almacena como mínimo su contador de referencias (`ob_refcnt`, 8 bytes en 64 bits) y un puntero a su "
                        "descriptor de tipo (`ob_type`, 8 bytes), como ilustra la Figura \\ref{fig:fig-cpython-object-layout}. La "
                        "gestión de memoria combina liberación inmediata cuando `ob_refcnt` cae a cero con un recolector generacional "
                        "detector de ciclos. Históricamente, CPython protegió el estado del intérprete con el cerrojo global **GIL** "
                        "(*Global Interpreter Lock*), pero a partir de Python 3.13/3.14 (PEP 703) incorpora soporte para compilaciones "
                        "*free-threaded* sin GIL basadas en conteo de referencias sesgado (*biased reference counting*). Todo proyecto "
                        "moderno de Python se configura mediante un único fichero declarativo `pyproject.toml` (PEP 621), gestionado "
                        "con `uv` o `pip` sobre `venv`, formateado y auditado con `ruff`, verificado estáticamente con `pyright` o "
                        "`mypy` y probado con `pytest`."
                    ),
                },
                {
                    "subsection": "sec-v5-1-2",
                    "text": (
                        "En Python, la sentencia `a = [1, 2, 3]; b = a` **no** copia la lista: vincula ambos nombres al mismo objeto "
                        "`PyListObject` incrementando su `ob_refcnt` a 2. La distinción entre tipos inmutables (`int` de precisión "
                        "arbitraria, `float` IEEE 754, `str` Unicode, `bytes`, `tuple`, `frozenset`) y mutables (`list`, `dict`, "
                        "`set`, `bytearray`) determina qué objetos son *hashables* y pueden actuar como claves de un diccionario. "
                        "Desde Python 3.6/3.7, `dict` se implementa como una tabla hash compacta que preserva por especificación el "
                        "orden de inserción separando un array denso de índices hash de la tabla contigua de entradas `(hash, key_ptr, val_ptr)`. "
                        "Asimismo, Python 3.10+ incorpora coincidencia estructural de patrones (`match`/`case`, PEP 634):\n"
                        "```python\n"
                        "def evaluate_ast_node(node: tuple) -> int:\n"
                        "    match node:\n"
                        "        case (\"lit\", int(v)):\n"
                        "            return v\n"
                        "        case (\"add\", left, right):\n"
                        "            return evaluate_ast_node(left) + evaluate_ast_node(right)\n"
                        "        case (\"mul\", left, right):\n"
                        "            return evaluate_ast_node(left) * evaluate_ast_node(right)\n"
                        "        case _:\n"
                        "            raise ValueError(f\"Nodo AST desconocido: {node!r}\")\n"
                        "```\n"
                        "Un escollo clásico que todo programador debe evitar desde el primer día es emplear argumentos por defecto "
                        "mutables en definiciones de función (`def append_item(x, target=[]):`), ya que la expresión por defecto se "
                        "evalúa una única vez al ejecutar la sentencia `def`, compartiendo la misma lista entre todas las llamadas; "
                        "el patrón correcto es `def append_item(x, target: list | None = None):`."
                    ),
                },
            ],
            "definition": (
                "Vinculación de nombres en Python (Name Binding): asociación en una tabla de símbolos (`locals()`, `globals()`) "
                "entre un identificador y la dirección de un `PyObject` en el montículo; el tipo pertenece exclusivamente al "
                "objeto referenciado y nunca a la variable léxica."
            ),
            "consejo": (
                "Utiliza siempre `is None` e `is not None` para comprobar identidad frente al singleton `None`, y reserva `==` "
                "para comparar igualdad de valor (`__eq__`)."
            ),
            "self_check": (
                "¿Por qué una tupla `(1, [2, 3])` lanza `TypeError: unhashable type: 'list'` al intentar usarla como clave de un "
                "`dict` a pesar de que el contenedor exterior es un `tuple` inmutable?"
            ),
            "derivation": {
                "title": "Ahorro de memoria de la tabla hash compacta de dict en Python 3.6+",
                "assumptions": ["Una tabla con K ranuras (potencia de dos) y N entradas activas almacena K índices de b bytes más N entradas de 24 bytes (hash, key, value) en lugar de K * 24 bytes"],
                "steps": [
                    {"equation": r"M_{\text{legacy}} = 24 \cdot K", "justification": "En el diseño clásico previo a Python 3.6, las K ranuras completas de 24 B se reservaban aunque estuvieran vacías"},
                    {"equation": r"M_{\text{compact}} = b \cdot K + 24 \cdot N", "justification": "La tabla de índices ocupa solo b bytes por ranura (1 B si K <= 128) más las N entradas de 24 B"},
                ],
                "Verify": {"left": "24 * K - (b * K + 24 * N)", "right": "(24 - b) * K - 24 * N"},
            },
            "worked_problem": {
                "prompt": (
                    "En CPython de 64 bits, cada entrada de un diccionario almacena tres palabras de $8\\text{ B}$ (`me_hash`, "
                    "`me_key`, `me_value` = $24\\text{ B}$). Para una tabla con $K = 128$ ranuras en el índice ($1\\text{ B}$ por "
                    "ranura en `dk_indices`) y capacidad para $N = 85$ entradas en `dk_entries`, calcula cuántos bytes ahorra el "
                    "diseño de diccionario compacto ($128 \\cdot 1 + 85 \\cdot 24$) frente al diseño disperso antiguo ($128 \\cdot 24$)."
                ),
                "expression": "(128 * 24) - (128 * 1 + 85 * 24)",
                "solution": {
                    "model": "Ahorro de memoria del diccionario compacto de CPython (Raymond Hettinger)",
                    "given": [
                        {"symbol": "K", "value": "128 ranuras", "description": "Tamaño del array de índices hash (1 B por índice)"},
                        {"symbol": "N", "value": "85 entradas", "description": "Capacidad densa de entradas (2/3 de K)"},
                        {"symbol": "S_entry", "value": "24 B", "description": "Tamaño de cada entrada (hash, key, value)"},
                    ],
                    "steps": [
                        {"step": "Restamos el tamaño compacto (2168 B) al tamaño antiguo (3072 B)", "equation": r"\Delta M = 128 \cdot 24 - (128 \cdot 1 + 85 \cdot 24)", "expression": "(128 * 24) - (128 * 1 + 85 * 24)"},
                    ],
                    "conclusion": "El diccionario compacto ahorra 904 bytes (casi un 30 % menos de memoria) y acelera la iteración al recorrer un array contiguo.",
                },
            },
            "practice_problems": [
                {"prompt": "En CPython de 64 bits, la cabecera base `PyObject` contiene `ob_refcnt` (8 B) y `ob_type` (8 B). ¿Cuántos bytes mide esta cabecera mínima?", "expression": "8 + 8", "difficulty": "FOUNDATIONAL", "problem_type": "DIRECT_SUBSTITUTION"},
                {"prompt": "Una lista `PyListObject` mantiene un array de punteros `PyObject*` (8 B cada uno). Si su capacidad reservada es de 64 elementos, ¿cuántos bytes ocupa ese array de punteros?", "expression": "64 * 8", "difficulty": "FOUNDATIONAL", "problem_type": "DIRECT_SUBSTITUTION"},
                {"prompt": "¿Cuál es la suma de los cuadrados impares evaluada por `sum(x * x for x in range(1, 10, 2))` ($1^2 + 3^2 + 5^2 + 7^2 + 9^2$)?", "expression": "1 + 9 + 25 + 49 + 81", "difficulty": "INTERMEDIATE", "problem_type": "MULTI_STEP"},
                {"prompt": "En el proyecto `projects/python-bytecode-vm`, la función compila y evalúa `(x + 4) * (y - 2) + (10 if x < y else 20)` para $x = 6, y = 9$. ¿Cuál es el resultado entero devuelto?", "expression": "(6 + 4) * (9 - 2) + 10", "difficulty": "INTERMEDIATE", "problem_type": "DESIGN"},
            ],
        },
        {
            "id": "cap02-python-intermedio-avanzado-modelo-datos-tipado-iteradores",
            "title": "Monografía de Python (II — Bloques D y E): Modelo de Datos (__dunder__), Typing Estático, Decoradores, Generadores y Context Managers",
            "part_id": "parte-v-monografia-python",
            "part_title": "Monografía Autónoma de Python (Python 3.12 – 3.14)",
            "sources": ["src-python-ref", "src-gamma-gof"],
            "learning_objectives": [
                "Dominar el Data Model de Python (`__repr__`, `__eq__`, `__hash__`, `__len__`, `__getitem__`, `__enter__`/`__exit__`, `__slots__`).",
                "Diseñar jerarquías limpias con `@dataclass(frozen=True, slots=True)`, protocolos estructurales (`typing.Protocol`) y genéricos de Python 3.12 (PEP 695).",
                "Construir clausuras, decoradores con `functools.wraps`, generadores perezosos (`yield`, `yield from`) y gestores de contexto (`contextlib`).",
            ],
            "concepts": [
                {"id": "cpt-py-datamodel-slots-protocols", "title": "Protocolos del modelo de datos (__dunder__), optimización __slots__, dataclasses y typing.Protocol"},
                {"id": "cpt-py-generators-decorators-ctx", "title": "Evaluación perezosa con generadores, clausuras/decoradores y gestión determinista con with"},
            ],
            "subsections": [
                {"id": "sec-v5-2-1", "title": "Bloque D: POO en Python, Data Model (__dunder__), @dataclass, __slots__ y sistema de tipos (PEP 484 / PEP 695)"},
                {"id": "sec-v5-2-2", "title": "Bloque E: Clausuras, decoradores, iteradores, generadores (yield) y gestores de contexto (with)"},
            ],
            "purpose": (
                "Este capítulo cubre los Bloques D y E de Python. La verdadera fluidez en Python consiste en comprender que "
                "la sintaxis del lenguaje (`len(x)`, `x[i]`, `for v in x`, `with ctx:`, `a + b`) se traduce directamente en "
                "invocaciones a métodos especiales del **Modelo de Datos** (`__len__`, `__getitem__`, `__iter__`, `__enter__`/`__exit__`, `__add__`)."
            ),
            "paragraphs": [
                {
                    "subsection": "sec-v5-2-1",
                    "text": (
                        "Por defecto, cada instancia de una clase definida por el usuario almacena sus atributos en un diccionario "
                        "dinámico `__dict__`, lo que aporta flexibilidad pero añade más de $100\\text{ B}$ de sobrecoste por objeto. "
                        "Cuando se instancian millones de objetos de dominio o nodos del AST (como en nuestro proyecto `projects/python-bytecode-vm`), "
                        "declarar `@dataclass(frozen=True, slots=True)` genera automáticamente `__init__`, `__repr__`, `__eq__`, `__hash__` "
                        "y reemplaza `__dict__` por un descriptor compacto de ranuras fijas (`__slots__`). Asimismo, Python 3.12 (PEP 695) "
                        "simplifica la sintaxis de clases y funciones genéricas y de `typing.Protocol` (subtipado estructural o *static duck typing*):\n"
                        "```python\n"
                        "from dataclasses import dataclass\n"
                        "from typing import Protocol\n\n"
                        "class Measurable(Protocol):\n"
                        "    def byte_size(self) -> int: ...\n\n"
                        "@dataclass(frozen=True, slots=True)\n"
                        "class TelemetryFrame:\n"
                        "    sensor_id: int\n"
                        "    payload: bytes\n"
                        "    def byte_size(self) -> int:\n"
                        "        return 8 + len(self.payload)\n\n"
                        "def total_footprint[T: Measurable](items: list[T]) -> int:\n"
                        "    return sum(item.byte_size() for item in items)\n"
                        "```\n"
                        "Observa que `TelemetryFrame` satisface `Measurable` estructuralmente para `pyright`/`mypy` sin necesidad de "
                        "heredar nominalmente de `Measurable`."
                    ),
                },
                {
                    "subsection": "sec-v5-2-2",
                    "text": (
                        "Un **generador** es cualquier función cuyo cuerpo contiene la palabra clave `yield`. Al llamarla, no ejecuta "
                        "su cuerpo inmediatamente, sino que devuelve un objeto iterador que suspende y reanuda su marco de ejecución "
                        "(`PyGenObject`) en cada llamada a `next()`, manteniendo un consumo de memoria $O(1)$ independientemente de si "
                        "la secuencia subyacente tiene miles de millones de registros. Por su parte, los **gestores de contexto** "
                        "implementan el protocolo `__enter__` / `__exit__(exc_type, exc_val, exc_tb)` (o se escriben de forma concisa "
                        "con `@contextlib.contextmanager` y un único `yield` dentro de un bloque `try ... finally:`), garantizando la "
                        "liberación determinista de ficheros, conexiones de red, cerrojos `threading.Lock` y transacciones de base de datos."
                    ),
                },
            ],
            "definition": (
                "Protocolo Descriptor en Python: mecanismo fundamental del modelo de objetos según el cual cualquier atributo de "
                "clase que defina `__get__`, `__set__` o `__delete__` intercepta el acceso a atributos en las instancias, sirviendo "
                "de base para métodos ligados, `@property`, `@classmethod`, `@staticmethod` y `__slots__`."
            ),
            "consejo": (
                "Usa siempre `@dataclass(slots=True)` en clases de datos de alto volumen: reduce el consumo de memoria entre un "
                "40 % y un 60 % y acelera el acceso a atributos al sustituir búsquedas hash en `__dict__` por desplazamientos directos en C."
            ),
            "self_check": (
                "¿Qué diferencia existe en el protocolo descriptor entre un *data descriptor* (define `__get__` y `__set__`) "
                "y un *non-data descriptor* (solo define `__get__`) frente a una entrada con el mismo nombre en ` instance.__dict__`?"
            ),
            "derivation": {
                "title": "Ahorro de memoria por instancia al usar __slots__ frente a __dict__ en CPython",
                "assumptions": ["Una instancia con k atributos ocupa S_slots bytes con __slots__ frente a S_slots + S_dict bytes con diccionario por instancia"],
                "steps": [
                    {"equation": r"S_{\text{slots}} = 16 + 8 k", "justification": "Cabecera PyObject (16 B) más k punteros de 8 B a los atributos"},
                    {"equation": r"\Delta M(N) = N \cdot S_{\text{dict}}", "justification": "Ahorro total en N instancias al suprimir el diccionario __dict__ de tamaño S_dict por objeto"},
                ],
                "Verify": {"left": "N * (16 + 8 * k + S_dict) - N * (16 + 8 * k)", "right": "N * S_dict"},
            },
            "worked_problem": {
                "prompt": (
                    "En una aplicación de procesamiento de grafos en CPython de 64 bits, una clase `Edge` con $k = 3$ atributos "
                    "ocupa $16 + 3 \\times 8 = 40\\text{ B}$ cuando se declara con `__slots__`, mientras que sin `__slots__` cada "
                    "instancia aloja además un `__dict__` que añade $112\\text{ B}$ por objeto ($152\\text{ B}$ en total). Calcula "
                    "cuántos megabytes exactos (dividiendo entre $10^6$) se ahorran al instanciar $N = 1000000$ de aristas con `__slots__`."
                ),
                "expression": "(1000000 * (152 - 40)) / 1000000",
                "solution": {
                    "model": "Ahorro de RAM con __slots__ en millones de instancias en CPython",
                    "given": [
                        {"symbol": "N", "value": "1000000", "description": "Un millón de instancias de Edge"},
                        {"symbol": "S_con_dict", "value": "152 B", "description": "Tamaño por instancia con __dict__"},
                        {"symbol": "S_con_slots", "value": "40 B", "description": "Tamaño por instancia con __slots__"},
                    ],
                    "steps": [
                        {"step": "Multiplicamos el millón de instancias por los 112 B ahorrados y dividimos entre 10^6", "equation": r"\Delta M_{\text{MB}} = \frac{10^6 \cdot (152 - 40)}{10^6}", "expression": "(1000000 * (152 - 40)) / 1000000"},
                    ],
                    "conclusion": "El uso de __slots__ ahorra exactamente 112 MB de memoria RAM.",
                },
            },
            "practice_problems": [
                {"prompt": "En CPython de 64 bits, ¿cuántos bytes ocupa una instancia con `__slots__` de 4 atributos (16 B de cabecera más $4 \\times 8$ B)?", "expression": "16 + 4 * 8", "difficulty": "FOUNDATIONAL", "problem_type": "DIRECT_SUBSTITUTION"},
                {"prompt": "Un generador perezoso produce bloques de 4096 bytes uno a uno para procesar un fichero de 10 GiB. ¿Cuántos bloques mantiene simultáneamente en RAM?", "expression": "1", "difficulty": "FOUNDATIONAL", "problem_type": "DIRECT_SUBSTITUTION"},
                {"prompt": "En una jerarquía con herencia múltiple `class D(B, C)` donde `B(A)` y `C(A)` heredan de `A(object)`, ¿cuántas clases aparecen en la tupla de orden de resolución de métodos `D.__mro__` (`D, B, C, A, object`)?", "expression": "5", "difficulty": "INTERMEDIATE", "problem_type": "MULTI_STEP"},
                {"prompt": "Un decorador `@lru_cache(maxsize=256)` recibe 1000 consultas sobre un conjunto de solo 200 claves distintas. ¿Cuántas veces se ejecuta realmente la función subyacente?", "expression": "200", "difficulty": "INTERMEDIATE", "problem_type": "DESIGN"},
            ],
        },
        {
            "id": "cap03-python-experto-asyncio-concurrencia-metaclases-packaging-proyectos",
            "title": "Monografía de Python (III — Bloques F, G y H): Asyncio, Concurrencia, Metaprogramación, Packaging y Proyectos",
            "part_id": "parte-v-monografia-python",
            "part_title": "Monografía Autónoma de Python (Python 3.12 – 3.14)",
            "sources": ["src-python-ref", "src-kleppmann-ddia"],
            "learning_objectives": [
                "Dominar la concurrencia asíncrona con `asyncio` (`TaskGroup`, `gather`, corrutinas nativas `async def`/`await`) y distinguir cuándo usar `multiprocessing` o `concurrent.futures`.",
                "Aplicar metaprogramación limpia con `__init_subclass__`, metaclases, el módulo `ast` y extensiones nativas C/Rust (`PyO3`/`maturin`, `ctypes`).",
                "Empaquetar y publicar distribuciones Wheel/sdist y estudiar el proyecto completo verificado `projects/python-bytecode-vm`.",
            ],
            "concepts": [
                {"id": "cpt-py-asyncio-taskgroups", "title": "Concurrencia estructurada en asyncio (TaskGroup), multiprocessing y extensiones nativas PyO3"},
                {"id": "cpt-py-ast-vm-packaging", "title": "Compilación del árbol sintáctico (módulo ast), máquina virtual de pila y empaquetado PEP 621"},
            ],
            "subsections": [
                {"id": "sec-v5-3-1", "title": "Bloque F: Asincronía con asyncio.TaskGroup, multiprocesamiento, metaclases y compilación AST"},
                {"id": "sec-v5-3-2", "title": "Bloques G y H: Ecosistema industrial (FastAPI, Pydantic, SQLAlchemy, Pytest) y los 4 proyectos (python-bytecode-vm)"},
            ],
            "purpose": (
                "Este capítulo completa la monografía de Python abordando el Nivel Experto (Bloque F), el Ecosistema (Bloque G) "
                "y los Proyectos (Bloque H), analizando en detalle el compilador AST y la máquina virtual de código de bytes "
                "`projects/python-bytecode-vm`."
            ),
            "paragraphs": [
                {
                    "subsection": "sec-v5-3-1",
                    "text": (
                        "En Python, la elección del modelo de concurrencia depende de la naturaleza del cuello de botella: para "
                        "operaciones limitadas por E/S de red o disco (*I/O-bound*) con miles de conexiones, `asyncio` ejecuta "
                        "corrutinas cooperativas sobre un único hilo respaldado por `epoll`/`kqueue`/`iocp`. Python 3.11+ introdujo "
                        "**concurrencia estructurada** mediante `async with asyncio.TaskGroup() as tg:`: si cualquiera de las tareas "
                        "hijas lanza una excepción no capturada, el `TaskGroup` cancela automáticamente todas las tareas hermanas y "
                        "propaga un `ExceptionGroup` manejable con `except*`. Para cargas intensivas de CPU (*CPU-bound*), se emplea "
                        "`concurrent.futures.ProcessPoolExecutor`, compilación sin GIL (PEP 703) o núcleos vectorizados en Rust/C "
                        "mediante `PyO3`, `NumPy` o `PyTorch`. En metaprogramación, el módulo estándar `ast` permite inspeccionar, "
                        "transformar y compilar árboles sintácticos de forma segura sin usar `eval()` arbitrario, técnica demostrada "
                        "en nuestro proyecto verificado `projects/python-bytecode-vm`:\n"
                        "```python\n"
                        "import ast\n\n"
                        "def count_binary_ops(expr_source: str) -> int:\n"
                        "    tree = ast.parse(expr_source, mode=\"eval\")\n"
                        "    return sum(1 for node in ast.walk(tree) if isinstance(node, ast.BinOp))\n"
                        "```\n"
                        "Para registrar subclases o validar esquemas de clase en el momento de su creación, Python 3.6+ ofrece el "
                        "gancho ligero `__init_subclass__(cls, **kwargs)`, evitando en el 95 % de los casos la complejidad de definir "
                        "una metaclase personalizada que herede de `type`."
                    ),
                },
                {
                    "subsection": "sec-v5-3-2",
                    "text": (
                        "El ecosistema profesional de Python (Bloque G) destaca por cuatro pilares: (1) desarrollo web y APIs con "
                        "`FastAPI` (ASGI asíncrono), `Django` y validación de esquemas en Rust con `Pydantic v2`; (2) persistencia "
                        "y migraciones con `SQLAlchemy 2.0` y `Alembic`; (3) ingeniería de datos y cálculo científico con `NumPy`, "
                        "`SciPy`, `Pandas` y `Polars`; y (4) calidad y empaquetado con `pytest` (fixtures, parametrización), "
                        "`Hypothesis` (property-based testing), `ruff`, `pyright` y construcción de paquetes `.whl` con `hatchling` "
                        "o `maturin`. En el Bloque H, el lector desarrolla cuatro proyectos completos: un gestor CLI de tareas con "
                        "persistencia SQLite, un cliente/servidor HTTP asíncrono con reintentos exponenciales, un pipeline de validación "
                        "de datos y la máquina virtual de pila `projects/python-bytecode-vm`, verificada al 100 % con `pytest`, `ruff` y `pyright`."
                    ),
                },
            ],
            "definition": (
                "Concurrencia estructurada (`asyncio.TaskGroup`): abstracción de control de flujo concurrente que garantiza que "
                "el tiempo de vida de todas las tareas asíncronas lanzadas dentro de un bloque léxico `async with` está acotado "
                "por dicho bloque, sin dejar tareas huérfanas ejecutándose en segundo plano tras salir del ámbito."
            ),
            "consejo": (
                "Nunca llames a funciones bloqueantes síncronas (`time.sleep`, `requests.get`, lectura síncrona de disco) dentro "
                "de una función `async def`: bloquearás todo el bucle de eventos de `asyncio` congelando el resto de tareas concurrentes; "
                "utiliza `await asyncio.sleep(...)`, `httpx.AsyncClient` o `await asyncio.to_thread(...)`."
            ),
            "self_check": (
                "¿Por qué en `projects/python-bytecode-vm` un salto condicional `JMP_IF_FALSE` necesita parchar (*backpatch*) su "
                "índice de destino después de haber emitido las instrucciones de la rama verdadera?"
            ),
            "derivation": {
                "title": "Aceleración de E/S concurrente con asyncio.TaskGroup frente a ejecución secuencial",
                "assumptions": ["N peticiones de red independientes con latencia individual L_i y sobrecoste local despreciable"],
                "steps": [
                    {"equation": r"T_{\text{seq}} = \sum_{i=1}^{N} L_i = N \cdot \bar{L}", "justification": "La ejecución síncrona secuencial espera a que termine cada petición antes de iniciar la siguiente"},
                    {"equation": r"T_{\text{async}} \approx \max_{1 \le i \le N} L_i", "justification": "En asyncio las N esperas de red se solapan en el reactor epoll/kqueue"},
                ],
                "Verify": {"left": "N * L_avg - L_max", "right": "-L_max + N * L_avg"},
            },
            "worked_problem": {
                "prompt": (
                    "Un agregador de microservicios en Python debe consultar $N = 20$ endpoints HTTP independientes, cada uno con "
                    "una latencia de red de $L = 150\\text{ ms}$ y $1\\text{ ms}$ de procesamiento de CPU local en el bucle de eventos. "
                    "Calcula cuántos milisegundos se ahorran al ejecutarlos concurrentemente con `asyncio.TaskGroup` ($150 + 20 \\times 1 = 170\\text{ ms}$) "
                    "frente a ejecutarlos secuencialmente de forma síncrona ($20 \\times (150 + 1) = 3020\\text{ ms}$)."
                ),
                "expression": "20 * (150 + 1) - (150 + 20 * 1)",
                "solution": {
                    "model": "Solapamiento de latencia de E/S en el bucle de eventos de asyncio",
                    "given": [
                        {"symbol": "N", "value": "20", "description": "Número de peticiones HTTP"},
                        {"symbol": "L", "value": "150 ms", "description": "Latencia de red por petición"},
                        {"symbol": "t_cpu", "value": "1 ms", "description": "Tiempo de CPU por respuesta"},
                    ],
                    "steps": [
                        {"step": "Restamos el tiempo concurrente (170 ms) al tiempo secuencial (3020 ms)", "equation": r"\Delta T = 20 \cdot 151 - (150 + 20)", "expression": "20 * (150 + 1) - (150 + 20 * 1)"},
                    ],
                    "conclusion": "La ejecución concurrente con asyncio ahorra 2850 ms, reduciendo el tiempo de respuesta total de 3.02 s a 0.17 s.",
                },
            },
            "practice_problems": [
                {"prompt": "En `projects/python-bytecode-vm`, la expresión `2 * 3 + 4 * 5` emite 4 instrucciones `LOAD_CONST` y 3 instrucciones binarias (`MUL`, `MUL`, `ADD`). ¿Cuántas instrucciones totales contiene el bloque compilado?", "expression": "4 + 3", "difficulty": "FOUNDATIONAL", "problem_type": "DIRECT_SUBSTITUTION"},
                {"prompt": "Al evaluar `2 * 3 + 4 * 5` en una máquina de pila, ¿cuál es la altura máxima (número máximo de operandos apilados simultáneamente) que alcanza la pila?", "expression": "3", "difficulty": "FOUNDATIONAL", "problem_type": "DIRECT_SUBSTITUTION"},
                {"prompt": "Un pool de 8 procesos (`ProcessPoolExecutor(max_workers=8)`) ejecuta 40 tareas de CPU de 2 segundos cada una. ¿Cuántos segundos tarda en completar las 40 tareas ideales ($40 / 8 \\times 2$)?", "expression": "(40 / 8) * 2", "difficulty": "INTERMEDIATE", "problem_type": "MULTI_STEP"},
                {"prompt": "Una política de reintentos con retroceso exponencial (`backoff`) espera $100 \\cdot 2^k\\text{ ms}$ para $k = 0, 1, 2, 3$. ¿Cuántos milisegundos totales habrá esperado acumulados tras esos 4 reintentos?", "expression": "100 * (1 + 2 + 4 + 8)", "difficulty": "INTERMEDIATE", "problem_type": "DESIGN"},
            ],
        },
        {
            "id": "cap04-javascript-fundamentos-closures-prototipos-nivel-intermedio",
            "title": "Monografía de JavaScript (I — Bloques A–D): Historia, Motor V8, Ámbitos, Clausuras, Prototipos y Módulos ESM",
            "part_id": "parte-v-monografia-js-ts",
            "part_title": "Monografías Autónomas de JavaScript (ES2024+) y TypeScript (5.x)",
            "sources": ["src-ecmascript-2024", "src-mdn-html-css"],
            "learning_objectives": [
                "Comprender la evolución de ECMAScript (ES3, ES5, ES6/ES2015 hasta ES2024+) y la arquitectura JIT multipaso (Ignition + Sparkplug + Maglev + TurboFan en V8).",
                "Dominar los tipos primitivos (`number` IEEE 754, `bigint`, `string`, `symbol`), la igualdad estricta (`===`), ámbitos léxicos (`let`/`const` y Temporal Dead Zone) y clausuras.",
                "Explicar con rigor la delegación prototípica (`[[Prototype]]`, `Object.create`, sintaxis `class`), la vinculación dinámica de `this` y el sistema de módulos estándar ESM (`import`/`export`).",
            ],
            "concepts": [
                {"id": "cpt-js-v8-hidden-classes", "title": "Compilación JIT adaptativa, clases ocultas (Shapes/Maps), Inline Caches y semántica de tipos en ECMAScript"},
                {"id": "cpt-js-closures-prototypes-esm", "title": "Entornos léxicos, clausuras, cadena de prototipos [[Prototype]], enlace de this y módulos estáticos ESM"},
            ],
            "subsections": [
                {"id": "sec-v5-4-1", "title": "Bloques A–C: Historia de ECMAScript, motores JIT (V8), tipos, coerción vs ===, let/const y funciones"},
                {"id": "sec-v5-4-2", "title": "Bloque D: Clausuras, delegación por prototipos, clases, desestructuración y módulos ES (ESM vs CommonJS)"},
            ],
            "purpose": (
                "Este capítulo inicia la monografía autónoma de **JavaScript (ECMAScript 2024+)**, diferenciándolo con rigor "
                "de TypeScript. JavaScript es el único lenguaje nativo universal de los navegadores web y, a través de motores "
                "como V8 (Node.js, Deno) y JavaScriptCore (Bun), un entorno de servidor de altísima velocidad cuando se comprende "
                "cómo optimiza el compilador JIT sus estructuras dinámicas."
            ),
            "paragraphs": [
                {
                    "subsection": "sec-v5-4-1",
                    "text": (
                        "Creado por Brendan Eich en Netscape en 1995 y estandarizado por Ecma International bajo la especificación "
                        "**ECMA-262**, JavaScript experimentó su transformación decisiva en ES6 (ES2015) con la introducción de "
                        "`let`/`const`, funciones flecha, clases, promesas, generadores, `Map`/`Set`, `Symbol` y módulos nativos ESM. "
                        "En los motores modernos como V8, el código fuente no se interpreta línea a línea: se compila a bytecode "
                        "(*Ignition*) y las funciones calientes se optimizan a código máquina nativo (*TurboFan*) asociando a cada "
                        "objeto una **clase oculta** (*Hidden Class* o *Shape/Map*). Si todas las instancias de un punto se inicializan "
                        "con las mismas propiedades en el mismo orden (`{ x, y }`), comparten la misma Shape y los accesos `pt.x` se "
                        "resuelven en una sola instrucción mediante *Inline Caching* (monomórfico). En cuanto a los tipos primitivos, "
                        "`number` es un flotante IEEE 754 de doble precisión cuyos enteros exactos llegan hasta `Number.MAX_SAFE_INTEGER` "
                        "($2^{53} - 1 = 9007199254740991$), mientras que `BigInt` (`42n`) representa enteros de precisión arbitraria. "
                        "En código profesional se utiliza siempre la igualdad estricta `===` y `!==` (que no realiza coerción implícita "
                        "de tipos) o `Object.is(a, b)` (que distingue `+0` de `-0` y evalúa `Object.is(NaN, NaN)` a `true`)."
                    ),
                },
                {
                    "subsection": "sec-v5-4-2",
                    "text": (
                        "A diferencia de los lenguajes basados en clases estáticas, el modelo de objetos de JavaScript se fundamenta "
                        "en la **delegación prototípica**: cada objeto posee un enlace interno `[[Prototype]]` (accesible mediante "
                        "`Object.getPrototypeOf(obj)`). Cuando se lee una propiedad `obj.metodo`, si no existe como propiedad propia "
                        "(`Object.hasOwn(obj, 'metodo')`), el motor asciende por la cadena de prototipos hasta encontrarla o llegar a "
                        "`null`. La sintaxis `class` de ES2015/ES2022 (incluyendo campos privados reales `#saldo` verificados por la "
                        "gramática) se construye limpiamente sobre este mecanismo:\n"
                        "```javascript\n"
                        "export class TokenBucket {\n"
                        "  #capacity;\n"
                        "  #tokens;\n"
                        "  constructor(capacity) {\n"
                        "    this.#capacity = capacity;\n"
                        "    this.#tokens = capacity;\n"
                        "  }\n"
                        "  tryConsume(amount = 1) {\n"
                        "    if (amount <= 0 || this.#tokens < amount) return false;\n"
                        "    this.#tokens -= amount;\n"
                        "    return true;\n"
                        "  }\n"
                        "  get available() { return this.#tokens; }\n"
                        "}\n"
                        "```\n"
                        "Asimismo, mientras que las funciones tradicionales determinan el valor de `this` dinámicamente según el sitio "
                        "de llamada (`obj.fn()`, `fn.call(ctx)`), las funciones flecha (`() => ...`) carecen de `this` propio y lo "
                        "capturan léxicamente del ámbito circundante."
                    ),
                },
            ],
            "definition": (
                "Zona Muerta Temporal (Temporal Dead Zone, TDZ en ECMAScript): intervalo de ejecución desde la entrada al bloque "
                "léxico hasta la evaluación de la declaración `let` o `const` de una variable, durante el cual cualquier intento "
                "de leer o escribir dicha variable lanza determinísticamente un `ReferenceError`."
            ),
            "consejo": (
                "Para preservar el polimorfismo monomórfico en las *Inline Caches* de V8, inicializa siempre todas las propiedades "
                "de un objeto en su constructor en el mismo orden y evita eliminar propiedades dinámicamente con `delete obj.prop`."
            ),
            "self_check": (
                "¿Por qué en JavaScript `0.1 + 0.2 === 0.3` evalúa a `false` y cómo deben representarse importes monetarios "
                "exactos usando `BigInt` en céntimos?"
            ),
            "derivation": {
                "title": "Límite de enteros seguros (MAX_SAFE_INTEGER) en el tipo Number de JavaScript",
                "assumptions": ["El tipo Number de ECMAScript es un binario64 IEEE 754 con 52 bits explícitos de mantisa más 1 bit implícito (p = 53 bits)"],
                "steps": [
                    {"equation": r"N_{\text{safe}} = 2^{53} - 1", "justification": "Mayor entero tal que N y N + 1 son ambos representables sin redondeo en 53 bits de significando"},
                    {"equation": r"2^{53} + 1 \mapsto 2^{53}", "justification": "En 2^53 el espaciado entre números representables (ULP) pasa a ser 2, perdiendo los impares"},
                ],
                "Verify": {"left": "2**53 - 1", "right": "9007199254740991"},
            },
            "worked_problem": {
                "prompt": (
                    "En el motor V8 con compresión de punteros (*Pointer Compression*), cada referencia a propiedad en un objeto "
                    "de forma fija (*Fast Properties / In-object properties*) ocupa $4\\text{ B}$ en lugar de $8\\text{ B}$, más "
                    "una cabecera de objeto de $12\\text{ B}$ (`map`, `properties`, `elements` comprimidos). Calcula cuántos bytes "
                    "ahorran $N = 10000$ objetos con $k = 5$ propiedades en línea bajo compresión de punteros ($12 + 5 \\times 4 = 32\\text{ B}$ "
                    "por objeto) frente a punteros de 64 bits sin comprimir ($24 + 5 \\times 8 = 64\\text{ B}$ por objeto)."
                ),
                "expression": "10000 * ((24 + 5 * 8) - (12 + 5 * 4))",
                "solution": {
                    "model": "Ahorro de montículo mediante Pointer Compression en el motor V8",
                    "given": [
                        {"symbol": "N", "value": "10000", "description": "Número de objetos instanciados"},
                        {"symbol": "S_64", "value": "64 B", "description": "Tamaño por objeto con punteros de 8 B (24 + 40)"},
                        {"symbol": "S_comp", "value": "32 B", "description": "Tamaño por objeto con punteros comprimidos de 4 B (12 + 20)"},
                    ],
                    "steps": [
                        {"step": "Multiplicamos los 10000 objetos por los 32 B ahorrados en cada uno", "equation": r"\Delta M = 10000 \cdot (64 - 32)", "expression": "10000 * ((24 + 5 * 8) - (12 + 5 * 4))"},
                    ],
                    "conclusion": "La compresión de punteros de V8 reduce el consumo a la mitad exacta, ahorrando 320 000 bytes.",
                },
            },
            "practice_problems": [
                {"prompt": "En V8 con punteros comprimidos de 4 bytes, ¿cuántos bytes ocupa la cabecera de 3 campos (`map`, `properties`, `elements`) de un objeto JS ($3 \\times 4$)?", "expression": "3 * 4", "difficulty": "FOUNDATIONAL", "problem_type": "DIRECT_SUBSTITUTION"},
                {"prompt": "Un `ArrayBuffer(1024)` se observa mediante un `Float64Array` (8 bytes por elemento). ¿Cuántos elementos `length` tiene la vista tipada?", "expression": "1024 / 8", "difficulty": "FOUNDATIONAL", "problem_type": "DIRECT_SUBSTITUTION"},
                {"prompt": "Si una cadena de prototipos tiene 4 niveles (`instancia -> SubClase.prototype -> Base.prototype -> Object.prototype -> null`) y se busca una propiedad inexistente, ¿cuántos eslabones de objeto se inspeccionan antes de llegar a `null`?", "expression": "4", "difficulty": "INTERMEDIATE", "problem_type": "MULTI_STEP"},
                {"prompt": "En `TokenBucket` con capacidad inicial de 100 tokens, se procesan 7 peticiones que consumen 12 tokens cada una. ¿Cuántos tokens quedan disponibles?", "expression": "100 - 7 * 12", "difficulty": "INTERMEDIATE", "problem_type": "DESIGN"},
            ],
        },
        {
            "id": "cap05-javascript-avanzado-event-loop-promesas-web-node-proyectos",
            "title": "Monografía de JavaScript (II — Bloques E–H): Event Loop, Microtareas, Promises, Async/Await, Streams, Node.js y Proyectos",
            "part_id": "parte-v-monografia-js-ts",
            "part_title": "Monografías Autónomas de JavaScript (ES2024+) y TypeScript (5.x)",
            "sources": ["src-ecmascript-2024", "src-mdn-html-css"],
            "learning_objectives": [
                "Trazar con exactitud el orden de ejecución entre la pila síncrona, la cola de microtareas (Promises, queueMicrotask) y la cola de macrotareas (setTimeout, I/O).",
                "Dominar los combinadores concurrentes de Promesas (`Promise.all`, `Promise.allSettled`, `Promise.race`, `Promise.any`), `AbortController`, generadores asíncronos (`for await...of`) y Web/Node Streams.",
                "Gestionar fugas de memoria en el recolector generacional (Orinoco), usar `WeakMap`/`WeakRef`, `Worker Threads` y desarrollar los 4 proyectos en JavaScript.",
            ],
            "concepts": [
                {"id": "cpt-js-event-loop-microtasks", "title": "Arquitectura del Event Loop, prioridad de vaciado exhaustivo de microtareas sobre macrotareas y async/await"},
                {"id": "cpt-js-streams-workers-gc", "title": "Contrapresión (backpressure) en Streams, paralelismo con Worker Threads + SharedArrayBuffer y prevención de fugas"},
            ],
            "subsections": [
                {"id": "sec-v5-5-1", "title": "Bloques E y F: Event Loop, cola de microtareas vs macrotareas, Promises, async/await, Streams y Workers"},
                {"id": "sec-v5-5-2", "title": "Bloques G y H: Ecosistema (Node.js, Deno, Bun, npm/pnpm, Vitest, ESLint) y los 4 proyectos en JavaScript"},
            ],
            "figure": {
                "key": "fig-js-event-loop-queues",
                "caption": "Ciclo determinista del Event Loop: tras vaciar la pila de llamadas síncrona (Call Stack), el motor drena exhaustivamente TODas las microtareas encoladas (incluidas las añadidas por otras microtareas) antes de tomar una única macrotarea.",
                "tikz": r"""\begin{tikzpicture}[node distance=1.6cm, >=stealth, thick, font=\small]
\node[draw=blue!70!black, fill=blue!8, rounded corners, minimum width=3.2cm, minimum height=1.0cm, align=center] (stack) {1. Call Stack\\(Código Síncrono)};
\node[draw=orange!75!black, fill=orange!12, rounded corners, minimum width=3.8cm, minimum height=1.0cm, align=center, right=1.0cm of stack] (micro) {2. Cola de Microtareas\\(\texttt{Promise.then}, \texttt{await})\\¡Vaciado hasta 0!};
\node[draw=teal!70!black, fill=teal!10, rounded corners, minimum width=3.6cm, minimum height=1.0cm, align=center, right=1.0cm of micro] (macro) {3. Cola de Macrotareas\\(\texttt{setTimeout}, I/O)\\(1 tarea por vuelta)};
\draw[->] (stack) -- (micro);
\draw[->] (micro) -- (macro);
\draw[->] (macro.south) -- ++(0,-0.6) -| (stack.south);
\end{tikzpicture}""",
            },
            "purpose": (
                "Este capítulo completa la monografía de JavaScript cubriendo los Bloques E, F, G y H: el funcionamiento exacto "
                "del **Event Loop**, la diferencia crítica entre microtareas y macrotareas, el manejo de contrapresión (*backpressure*) "
                "en flujos de datos y el paralelismo real mediante `Worker`s."
            ),
            "paragraphs": [
                {
                    "subsection": "sec-v5-5-1",
                    "text": (
                        "El modelo de concurrencia de JavaScript se basa en un hilo principal con ejecución hasta completitud "
                        "(*run-to-completion*) gobernado por el **Event Loop**. Como muestra la Figura \\ref{fig:fig-js-event-loop-queues}, "
                        "existen dos colas con semánticas de vaciado radicalmente distintas: la **cola de microtareas** (*Jobs* en "
                        "ECMA-262: continuaciones `.then/.catch/.finally` de `Promise`, código posterior a un `await` y `queueMicrotask`) "
                        "y la **cola de tareas o macrotareas** (`setTimeout`, `setInterval`, eventos del DOM, callbacks de red/disco en "
                        "`libuv`). Regla fundamental: cada vez que el *Call Stack* queda vacío, el motor ejecuta **todas** las microtareas "
                        "pendientes hasta dejar la cola de microtareas completamente vacía antes de procesar la siguiente macrotarea o "
                        "repintar la interfaz:\n"
                        "```javascript\n"
                        "// Orden determinista de salida: [1, 4, 3, 2]\n"
                        "export function traceEventLoopOrder() {\n"
                        "  const log = [];\n"
                        "  log.push(1);\n"
                        "  setTimeout(() => log.push(2), 0);               // Macrotarea\n"
                        "  Promise.resolve().then(() => log.push(3));      // Microtarea\n"
                        "  log.push(4);\n"
                        "  return log;\n"
                        "}\n"
                        "```\n"
                        "Por consiguiente, un bucle recursivo infinito de `queueMicrotask` o `Promise.resolve().then(...)` hambrea por "
                        "completo las macrotareas de E/S y congela el proceso aunque nunca bloquee mediante un `while(true)` síncrono."
                    ),
                },
                {
                    "subsection": "sec-v5-5-2",
                    "text": (
                        "En el Nivel Experto (Bloque F), cuando se procesan ficheros o respuestas HTTP de varios gigabytes en Node.js "
                        "o la Web API, cargar todo el cuerpo en un `Buffer` agota el montículo de V8; en su lugar se utilizan "
                        "`ReadableStream` / `WritableStream` con `pipeline()`, que regulan automáticamente la velocidad del productor "
                        "según la capacidad del consumidor (*backpressure*). Para cómputo intensivo de CPU (criptografía, compresión, "
                        "procesamiento de imágenes), se emplean `Worker Threads` (Node.js) o `Web Workers` (navegador) comunicados "
                        "por paso de mensajes (`Structured Clone`), transferencia de propiedad de coste cero (`ArrayBuffer` transferibles) "
                        "o memoria compartida sincronizada con `SharedArrayBuffer` y `Atomics`. El Bloque G cubre la gestión de paquetes "
                        "con `pnpm`/`npm`, `package.json` (`exports` condicionales ESM), `ESLint`, `Prettier` y `Vitest` / `node --test`, "
                        "y el Bloque H presenta cuatro proyectos completos en JavaScript puro (motor de plantillas reactivo sin dependencias, "
                        "planificador de colas asíncrono con límite de concurrencia `p-limit`, procesador de logs por streams y servidor HTTP REST)."
                    ),
                },
            ],
            "definition": (
                "Contrapresión (Backpressure en Streams): mecanismo de control de flujo mediante el cual un consumidor lento "
                "señala al productor asíncrono que su búfer interno ha alcanzado la marca de agua alta (`highWaterMark`), "
                "pausando la lectura de la fuente subyacente hasta que el búfer se drena."
            ),
            "consejo": (
                "Cuando lances múltiples operaciones asíncronas independientes entre sí dentro de una función `async`, no escribas "
                "`const a = await fetchA(); const b = await fetchB();` en serie: lánzalas en paralelo con `const [a, b] = await Promise.all([fetchA(), fetchB()]);`."
            ),
            "self_check": (
                "¿Qué diferencia existe entre `Promise.all`, `Promise.allSettled`, `Promise.race` y `Promise.any` cuando una de "
                "las promesas de entrada se rechaza con un error?"
            ),
            "derivation": {
                "title": "Tiempo de ejecución de un limitador de concurrencia asíncrono (Pool de k workers)",
                "assumptions": ["N tareas asíncronas de duración uniforme D ejecutadas con un máximo de k promesas en vuelo simultáneamente"],
                "steps": [
                    {"equation": r"B_{\text{waves}} = \lceil N / k \rceil", "justification": "Las N tareas se completan en N/k oleadas de k tareas en paralelo"},
                    {"equation": r"T_{\text{total}} = \lceil N / k \rceil \cdot D", "justification": "Cada oleada de k promesas concurrentes tarda D milisegundos"},
                ],
                "Verify": {"left": "(N / k) * D", "right": "D * (N / k)"},
            },
            "worked_problem": {
                "prompt": (
                    "Un descargador asíncrono en Node.js debe procesar $N = 120$ ficheros remotos con un limitador de concurrencia "
                    "que mantiene exactamente $k = 15$ promesas en vuelo simultáneamente para no saturar el servidor de origen. "
                    "Si cada descarga tarda $D = 200\\text{ ms}$, calcula el tiempo total en milisegundos necesario para completar "
                    "las 120 descargas ($(120 / 15) \\times 200$)."
                ),
                "expression": "(120 / 15) * 200",
                "solution": {
                    "model": "Tiempo de finalización con concurrencia acotada (Semaphore / Pool de Promesas)",
                    "given": [
                        {"symbol": "N", "value": "120", "description": "Total de tareas asíncronas"},
                        {"symbol": "k", "value": "15", "description": "Concurrencia máxima permitida"},
                        {"symbol": "D", "value": "200 ms", "description": "Duración de cada descarga"},
                    ],
                    "steps": [
                        {"step": "Dividimos las 120 tareas en 8 oleadas de 15 y multiplicamos por 200 ms", "equation": r"T = \frac{120}{15} \cdot 200", "expression": "(120 / 15) * 200"},
                    ],
                    "conclusion": "Las 120 descargas finalizan en 1600 ms (1.6 segundos) manteniendo el uso de sockets acotado en 15.",
                },
            },
            "practice_problems": [
                {"prompt": "En un turno del Event Loop se encolan 3 macrotareas (`setTimeout`) y 5 microtareas (`Promise.then`). ¿Cuántas microtareas se ejecutan antes de que comience la primera macrotarea?", "expression": "5", "difficulty": "FOUNDATIONAL", "problem_type": "DIRECT_SUBSTITUTION"},
                {"prompt": "Un `ReadableStream` con `highWaterMark = 65536` bytes (64 KiB) contiene actualmente 49 152 bytes sin consumir. ¿Cuántos bytes más puede aceptar antes de activar la señal de contrapresión?", "expression": "65536 - 49152", "difficulty": "FOUNDATIONAL", "problem_type": "DIRECT_SUBSTITUTION"},
                {"prompt": "Si 3 promesas independientes tardan 120 ms, 350 ms y 210 ms respectivamente, ¿en cuántos milisegundos se resuelve `Promise.all` de las tres?", "expression": "350", "difficulty": "INTERMEDIATE", "problem_type": "MULTI_STEP"},
                {"prompt": "En el problema anterior, si en lugar de `Promise.all` se ejecutaran secuencialmente con tres `await` uno tras otro, ¿cuántos milisegundos adicionales tardaría la operación ($120 + 350 + 210 - 350$)?", "expression": "120 + 350 + 210 - 350", "difficulty": "INTERMEDIATE", "problem_type": "DESIGN"},
            ],
        },
        {
            "id": "cap06-typescript-fundamentos-sistema-tipos-estructural-uniones",
            "title": "Monografía de TypeScript (I — Bloques A–D): Relación con JS, Borrado de Tipos, Tipado Estructural y Uniones Discriminadas",
            "part_id": "parte-v-monografia-js-ts",
            "part_title": "Monografías Autónomas de JavaScript (ES2024+) y TypeScript (5.x)",
            "sources": ["src-typescript-handbook", "src-pierce-tapl"],
            "learning_objectives": [
                "Comprender con exactitud la relación entre TypeScript y JavaScript: superconjunto sintáctico tipado con borrado completo de tipos (type erasure) en tiempo de ejecución.",
                "Configurar `tsconfig.json` con máxima rigurosidad (`strict: true`, `noUncheckedIndexedAccess: true`, `exactOptionalPropertyTypes: true`, `verbatimModuleSyntax: true`).",
                "Dominar el subtipado estructural, tipos unión e intersección (`|`, `&`), estrechamiento de flujo de control (*control-flow narrowing*), `unknown` vs `any` vs `never` y uniones discriminadas.",
            ],
            "concepts": [
                {"id": "cpt-ts-structural-erasure", "title": "Subtipado estructural, borrado de tipos (type erasure), tsconfig estricto y celosía top/bottom (unknown, never)"},
                {"id": "cpt-ts-discriminated-narrowing", "title": "Uniones discriminadas algebraicas, estrechamiento de tipos por flujo de control y comprobación exhaustiva con never"},
            ],
            "subsections": [
                {"id": "sec-v5-6-1", "title": "Bloques A–C: Filosofía de TypeScript, borrado de tipos, tsconfig.json estricto y primitivos (unknown, never)"},
                {"id": "sec-v5-6-2", "title": "Bloque D: Tipado estructural, interfaces vs type aliases, estrechamiento (narrowing) y uniones discriminadas"},
            ],
            "purpose": (
                "Este capítulo inicia la monografía diferenciada de **TypeScript (5.x)** (Bloques A, B, C y D). Explicamos "
                "con rigor matemático cómo su sistema de tipos estructural modela toda la flexibilidad dinámica de JavaScript "
                "mediante tipos algebraicos y análisis de flujo de control, y por qué el **borrado de tipos** (*type erasure*) "
                "exige combinar tipos estáticos con validadores en las fronteras de red."
            ),
            "paragraphs": [
                {
                    "subsection": "sec-v5-6-1",
                    "text": (
                        "Creado por Anders Hejlsberg en Microsoft y publicado en 2012, TypeScript es un superconjunto sintáctico "
                        "estáticamente tipado de ECMAScript. Su principio arquitectónico fundamental es el **borrado de tipos** "
                        "(*type erasure*): una vez que el comprobador de tipos (`tsc`) verifica la ausencia de errores estáticos, "
                        "todas las anotaciones de tipos, interfaces, alias `type` y parámetros genéricos desaparecen por completo al "
                        "emitir JavaScript (o al ejecutar directamente el fichero `.ts` mediante `node --experimental-strip-types` en "
                        "Node.js 22+/24+). En consecuencia, las anotaciones de TypeScript tienen **coste cero** en tiempo de ejecución, "
                        "pero tampoco realizan validaciones automáticas sobre un JSON recibido de la red (`JSON.parse` devuelve datos "
                        "cuya forma real debe verificarse en tiempo de ejecución antes de estrechar su tipo). En teoría de tipos, "
                        "`unknown` es el tipo superior seguro (*top type*: acepta cualquier valor pero prohíbe operar sobre él sin "
                        "estrecharlo primero), `never` es el tipo inferior vacío (*bottom type*, conjunto $\\emptyset$: habita las "
                        "funciones que nunca retornan y las ramas inalcanzables), mientras que `any` desactiva el sistema de tipos "
                        "y debe prohibirse mediante `@typescript-eslint/no-explicit-any`."
                    ),
                },
                {
                    "subsection": "sec-v5-6-2",
                    "text": (
                        "A diferencia de Java o C#, TypeScript utiliza **subtipado estructural** (*structural subtyping*): un tipo "
                        "$S$ es subtipo de $T$ ($S <: T$) si y solo si $S$ posee al menos todas las propiedades requeridas por $T$ con "
                        "tipos compatibles, sin importar cómo se declararon sus nombres. La herramienta de modelado de dominio más "
                        "potente de TypeScript es la **unión discriminada** (*discriminated union*): una unión de tipos objeto que "
                        "comparten una propiedad literal discriminante común (como `kind` o `ok`). Como se implementa en nuestro "
                        "proyecto verificado `projects/ts-reactive-http`, el compilador estrecha (*narrows*) automáticamente el tipo "
                        "en cada rama condicional y verifica la exhaustividad asignando el caso residual al tipo vacío `never`:\n"
                        "```typescript\n"
                        "export type DomainEvent =\n"
                        "  | { readonly kind: \"created\"; readonly id: string; readonly timestamp: number }\n"
                        "  | { readonly kind: \"paid\"; readonly id: string; readonly amountCents: number }\n"
                        "  | { readonly kind: \"cancelled\"; readonly id: string; readonly reason: string };\n\n"
                        "export function formatEventSummary(ev: DomainEvent): string {\n"
                        "  switch (ev.kind) {\n"
                        "    case \"created\":   return `Created ${ev.id} at ${ev.timestamp}`;\n"
                        "    case \"paid\":      return `Paid ${ev.id}: ${ev.amountCents} cents`;\n"
                        "    case \"cancelled\": return `Cancelled ${ev.id}: ${ev.reason}`;\n"
                        "    default: {\n"
                        "      const _exhaustive: never = ev;\n"
                        "      return _exhaustive;\n"
                        "    }\n"
                        "  }\n"
                        "}\n"
                        "```\n"
                        "Si en el futuro un ingeniero añade una cuarta variante a `DomainEvent`, el bloque `default` fallará en "
                        "compilación porque la nueva variante no es asignable a `never`."
                    ),
                },
            ],
            "definition": (
                "Subtipado Estructural por Anchura y Profundidad: relación de subtipado $S <: T$ en la que un registro "
                "$S = \\{ l_i : S_i \\}_{i \\in I}$ es subtipo de $T = \\{ l_j : T_j \\}_{j \\in J}$ si el conjunto de etiquetas "
                "de $T$ está contenido en el de $S$ ($J \\subseteq I$, anchura) y para cada $j \\in J$ inmutable se cumple $S_j <: T_j$ (profundidad)."
            ),
            "consejo": (
                "Activa siempre en `tsconfig.json` tanto `\"strict\": true` como `\"noUncheckedIndexedAccess\": true`: sin esta "
                "última opción, indexar un array `arr[i]` o un diccionario `dict[k]` se tipa como `T` en lugar de `T | undefined`, "
                "ocultando posibles accesos fuera de límites."
            ),
            "self_check": (
                "¿Por qué TypeScript aplica una comprobación adicional de *propiedades en exceso* (*excess property checking*) "
                "cuando se pasa un literal de objeto directamente a una función, pero la omite si ese mismo objeto se guarda "
                "primero en una variable intermedia?"
            ),
            "derivation": {
                "title": "Cardinalidad de tipos algebraicos suma y producto en TypeScript",
                "assumptions": ["Un tipo unión disjunta A | B suma cardinalidades; una tupla o interfaz { a: A; b: B } las multiplica"],
                "steps": [
                    {"equation": r"|A \cup B| = |A| + |B|", "justification": "Cardinalidad de una unión discriminada disjunta"},
                    {"equation": r"|A \times B| = |A| \cdot |B|", "justification": "Cardinalidad de un tipo producto { a: A, b: B }"},
                ],
                "Verify": {"left": "A_card * B_card + C_card", "right": "C_card + B_card * A_card"},
            },
            "worked_problem": {
                "prompt": (
                    "En un módulo de pagos en TypeScript, un estado mal modelado con banderas opcionales independientes "
                    "`{ status: 'idle' | 'loading' | 'success' | 'error'; isRetry: boolean; hasCache: boolean; isOffline: boolean }` "
                    "tiene $4 \\times 2 \\times 2 \\times 2 = 32$ combinaciones posibles. Al refactorizarlo en una unión discriminada "
                    "exacta donde solo existen $9$ estados válidos de dominio, ¿cuántos estados inválidos se vuelven estáticamente "
                    "irrepresentables en compilación?"
                ),
                "expression": "(4 * 2 * 2 * 2) - 9",
                "solution": {
                    "model": "Reducción de cardinalidad de estados mediante uniones discriminadas en TypeScript",
                    "given": [
                        {"symbol": "C_prod", "value": "32", "description": "Estados del tipo producto cartesiano (4 * 2^3)"},
                        {"symbol": "C_suma", "value": "9", "description": "Estados legítimos de la unión discriminada"},
                    ],
                    "steps": [
                        {"step": "Restamos los 9 estados legítimos a las 32 combinaciones del producto cartesiano", "equation": r"\Delta C = 4 \cdot 2^3 - 9", "expression": "(4 * 2 * 2 * 2) - 9"},
                    ],
                    "conclusion": "Se eliminan de raíz 23 estados imposibles o incoherentes sin escribir una sola prueba adicional.",
                },
            },
            "practice_problems": [
                {"prompt": "Un tipo literal unión `type HttpMethod = 'GET' | 'POST' | 'PUT' | 'DELETE' | 'PATCH'` se combina en una tupla `[HttpMethod, boolean]`. ¿Cuántos valores distintos habitan esa tupla ($5 \\times 2$)?", "expression": "5 * 2", "difficulty": "FOUNDATIONAL", "problem_type": "DIRECT_SUBSTITUTION"},
                {"prompt": "¿Cuántos bytes adicionales ocupa en el fichero `.js` emitido por `tsc` una interfaz `interface UserProfile` de 45 líneas tras el borrado de tipos?", "expression": "0", "difficulty": "FOUNDATIONAL", "problem_type": "DIRECT_SUBSTITUTION"},
                {"prompt": "Una unión discriminada tiene 6 variantes y un `switch` cubre actualmente 4 de ellas. ¿Cuántas variantes quedan en el tipo estrechado de la variable al llegar a la rama `default`?", "expression": "6 - 4", "difficulty": "INTERMEDIATE", "problem_type": "MULTI_STEP"},
                {"prompt": "En `projects/ts-reactive-http`, el limitador de tasa se inicializa con capacidad 3 y se envían 4 peticiones válidas seguidas. ¿Cuántas respuestas retornan con código HTTP `201` antes de que salte el código `429`?", "expression": "3", "difficulty": "INTERMEDIATE", "problem_type": "DESIGN"},
            ],
        },
        {
            "id": "cap07-typescript-avanzado-experto-mapped-conditional-infer-proyectos",
            "title": "Monografía de TypeScript (II — Bloques E–H): Programación a Nivel de Tipos (Mapped, Conditional, infer, Template Literals) y Proyectos",
            "part_id": "parte-v-monografia-js-ts",
            "part_title": "Monografías Autónomas de JavaScript (ES2024+) y TypeScript (5.x)",
            "sources": ["src-typescript-handbook", "src-pierce-tapl"],
            "learning_objectives": [
                "Dominar los operadores avanzados del sistema de tipos de TypeScript: `keyof`, `typeof`, tipos indexados `T[K]`, predicados de tipo (`x is T`), funciones de aserción (`asserts x is T`) y el operador `satisfies`.",
                "Construir transformaciones a nivel de tipos mediante Mapped Types (`{ [K in keyof T]: ... }`), Conditional Types (`T extends U ? X : Y`), inferencia estructural (`infer R`) y Template Literal Types.",
                "Integrar validación de fronteras en tiempo de ejecución (Zod / TypeBox) y auditar el proyecto completo `projects/ts-reactive-http`.",
            ],
            "concepts": [
                {"id": "cpt-ts-type-level-programming", "title": "Tipos mapeados, tipos condicionales distributivos, palabra clave infer, Template Literal Types y operador satisfies"},
                {"id": "cpt-ts-variance-zod-projects", "title": "Varianza explícita (in/out), tipos nominales simulados (Branded Types), validación de esquemas y projects/ts-reactive-http"},
            ],
            "subsections": [
                {"id": "sec-v5-7-1", "title": "Bloques E y F: Generics, keyof, Mapped Types, Conditional Types, infer, Template Literals, satisfies y Branded Types"},
                {"id": "sec-v5-7-2", "title": "Bloques G y H: Ecosistema (Zod, tRPC, Vite, tsx, Vitest) y los 4 proyectos (incluyendo ts-reactive-http)"},
            ],
            "purpose": (
                "Este capítulo lleva al lector a los niveles Avanzado y Experto de TypeScript (Bloques E, F, G y H). El sistema "
                "de tipos de TypeScript constituye por sí mismo un lenguaje funcional puro que se evalúa en tiempo de compilación "
                "sobre conjuntos de tipos, permitiendo calcular tipos de retorno, rutas tipadas y esquemas recursivos."
            ),
            "paragraphs": [
                {
                    "subsection": "sec-v5-7-1",
                    "text": (
                        "La programación a nivel de tipos en TypeScript se apoya en cuatro primitivas composicionales: (1) el operador "
                        "de consulta de claves `keyof T` y el acceso indexado `T[K]`; (2) los **tipos mapeados** (`{ readonly [K in keyof T as ...]: ... }`), "
                        "sobre los que se construyen utilidades estándar como `Partial<T>`, `Required<T>`, `Readonly<T>`, `Pick<T, K>` "
                        "y `Record<K, V>`; (3) los **tipos condicionales** `T extends U ? X : Y`, que se distribuyen automáticamente "
                        "sobre uniones cuando `T` es un parámetro de tipo desnudo y permiten extraer tipos internos mediante `infer` "
                        "(como `type AwaitedValue<T> = T extends Promise<infer U> ? AwaitedValue<U> : T`); y (4) los **Template Literal "
                        "Types**, que calculan productos cartesianos de cadenas en compilación. Además, TypeScript 4.9+ introdujo el "
                        "operador `satisfies`, que valida que una expresión cumpla un contrato `T` **sin ensanchar** (*widening*) su "
                        "tipo literal inferido, y para los casos donde el tipado estructural resulta demasiado permisivo (por ejemplo, "
                        "evitar pasar un `UserId` donde se espera un `OrderId`, siendo ambos `string`), se emplean **Branded Types**:\n"
                        "```typescript\n"
                        "declare const __brand: unique symbol;\n"
                        "export type Brand<T, B extends string> = T & { readonly [__brand]: B };\n\n"
                        "export type UserId  = Brand<string, \"UserId\">;\n"
                        "export type OrderId = Brand<string, \"OrderId\">;\n"
                        "export type DeepReadonly<T> = {\n"
                        "  readonly [K in keyof T]: T[K] extends object ? DeepReadonly<T[K]> : T[K];\n"
                        "};\n"
                        "```\n"
                        "Con `Brand<string, \"UserId\">`, la marca fantasma `unique symbol` existe únicamente en el comprobador de "
                        "tipos y se borra por completo en ejecución, proporcionando seguridad nominal con coste cero."
                    ),
                },
                {
                    "subsection": "sec-v5-7-2",
                    "text": (
                        "En el Bloque G (Ecosistema), la práctica estándar de la industria combina TypeScript con validadores de "
                        "esquema en las fronteras de entrada/salida (como `Zod` o `Valibot`, donde `type Payload = z.infer<typeof PayloadSchema>` "
                        "deriva el tipo estático directamente del validador de ejecución para que jamás diverjan), comunicación "
                        "extremo a extremo con seguridad de tipos (`tRPC`, OpenAPI/GraphQL codegen), empaquetadores rápidos (`Vite`, "
                        "`esbuild`, `tsup`) y ejecución directa en Node.js (`node --experimental-strip-types` o `tsx`). En el Bloque H, "
                        "junto con un cliente HTTP tipado por rutas, un motor de máquinas de estados finitos (`StateMachine<S, E>`) y "
                        "un bus de eventos tipado, estudiamos el proyecto completo `projects/ts-reactive-http`, verificado con "
                        "`node --experimental-strip-types --test`."
                    ),
                },
            ],
            "definition": (
                "Distributividad de Tipos Condicionales en TypeScript: propiedad según la cual, para un tipo condicional "
                "`type F<T> = T extends U ? X : Y` donde `T` es un parámetro genérico desnudo, instanciar `F<A | B>` se distribuye "
                "automáticamente como `F<A> | F<B>` (pudiendo desactivarse escribiendo `[T] extends [U] ? X : Y`)."
            ),
            "consejo": (
                "Utiliza el operador `satisfies` para diccionarios de configuración y tablas de rutas: `const routes = { ... } satisfies Record<string, RouteConfig>` "
                "comprueba cada entrada contra `RouteConfig` pero conserva las claves literales exactas en `keyof typeof routes`."
            ),
            "self_check": (
                "¿Por qué `Exclude<'a' | 'b' | 'c', 'a'>` devuelve `'b' | 'c'` gracias a la distributividad de `T extends U ? never : T` "
                "y por qué `never` actúa como el elemento neutro de la unión (`T | never = T`)?"
            ),
            "derivation": {
                "title": "Expansión combinatoria de Template Literal Types en TypeScript",
                "assumptions": ["Un tipo plantilla `${A}-${B}-${C}` donde A, B y C son uniones de literales de cadena genera el producto cartesiano de sus miembros"],
                "steps": [
                    {"equation": r"|T_{\text{tpl}}| = |A| \cdot |B| \cdot |C|", "justification": "Cada combinación de un literal de A, uno de B y uno de C forma un tipo literal distinto en la unión resultante"},
                    {"equation": r"|T_{\text{tpl}}| \le 100000", "justification": "El compilador tsc impone un límite de seguridad de 100 000 miembros en una unión generada por plantilla"},
                ],
                "Verify": {"left": "A_n * B_n * C_n", "right": "C_n * B_n * A_n"},
            },
            "worked_problem": {
                "prompt": (
                    "En un sistema de diseño tipado en TypeScript, se define el tipo de clases utilitarias mediante Template Literal Types: "
                    "`type SpacingUtility = `${Direction}-${Axis}-${Scale}``, donde `Direction` tiene $2$ miembros (`'m' | 'p'`), "
                    "`Axis` tiene $7$ miembros (`'t' | 'b' | 'l' | 'r' | 'x' | 'y' | 'a'`) y `Scale` tiene $12$ miembros (`'0'` a `'11'`). "
                    "Calcula cuántos tipos literales de cadena exactos genera el compilador en la unión `SpacingUtility`."
                ),
                "expression": "2 * 7 * 12",
                "solution": {
                    "model": "Producto cartesiano en Template Literal Types de TypeScript",
                    "given": [
                        {"symbol": "|Direction|", "value": "2", "description": "Margen o padding ('m' | 'p')"},
                        {"symbol": "|Axis|", "value": "7", "description": "Ejes direccionales"},
                        {"symbol": "|Scale|", "value": "12", "description": "Niveles de la escala espacial"},
                    ],
                    "steps": [
                        {"step": "Multiplicamos las cardinalidades de las tres uniones literales", "equation": r"|U| = 2 \cdot 7 \cdot 12", "expression": "2 * 7 * 12"},
                    ],
                    "conclusion": "El compilador genera y autocompleta exactamente 168 literales de cadena válidos en tiempo de compilación.",
                },
            },
            "practice_problems": [
                {"prompt": "Una interfaz `Config` tiene 8 propiedades obligatorias. Si se aplica `Pick<Config, 'host' | 'port' | 'tls'>`, ¿cuántas propiedades tiene el tipo resultante?", "expression": "3", "difficulty": "FOUNDATIONAL", "problem_type": "DIRECT_SUBSTITUTION"},
                {"prompt": "En el problema anterior, si en su lugar se aplica `Omit<Config, 'host' | 'port' | 'tls'>`, ¿cuántas propiedades conserva el tipo resultante?", "expression": "8 - 3", "difficulty": "FOUNDATIONAL", "problem_type": "DIRECT_SUBSTITUTION"},
                {"prompt": "Un Template Literal Type `${'http' | 'https'}://${'api' | 'auth' | 'cdn'}.ejemplo.es/${'v1' | 'v2'}` expande todas las rutas válidas. ¿Cuántos literales de URL compone la unión?", "expression": "2 * 3 * 2", "difficulty": "INTERMEDIATE", "problem_type": "MULTI_STEP"},
                {"prompt": "En `projects/ts-reactive-http`, cada lectura de telemetría se redondea con `Math.round(v * 100) / 100`. Para el vector `[12.5, 7.25, 10.25]`, ¿cuál es el valor exacto de la suma?", "expression": "12.5 + 7.25 + 10.25", "difficulty": "INTERMEDIATE", "problem_type": "DESIGN"},
            ],
        },
        {
            "id": "cap08-interoperabilidad-comparativa-arquitectura-python-js-ts",
            "title": "Arquitectura Comparada, Interoperabilidad (FFI, WebAssembly, REST/JSON) y Rúbrica de Python, JavaScript y TypeScript",
            "part_id": "parte-v-monografia-js-ts",
            "part_title": "Monografías Autónomas de JavaScript (ES2024+) y TypeScript (5.x)",
            "sources": ["src-python-ref", "src-typescript-handbook"],
            "learning_objectives": [
                "Comparar rigurosamente los modelos de ejecución, sistemas de tipos, concurrencia y ecosistemas de Python, JavaScript y TypeScript.",
                "Diseñar contratos de interoperabilidad entre backends en Python (FastAPI/Pydantic) y clientes/servidores en TypeScript mediante esquemas OpenAPI 3.1 y JSON Schema.",
                "Superar la evaluación integradora del Volumen V resolviendo problemas de rendimiento, tipado y concurrencia en los tres lenguajes.",
            ],
            "concepts": [
                {"id": "cpt-v5-comparative-runtime", "title": "Comparativa de máquinas virtuales (CPython vs V8), sistemas de tipos (PEP 484/695 vs TS) y modelos asíncronos"},
                {"id": "cpt-v5-contract-first-interop", "title": "Sincronización de esquemas entre Pydantic (Python) y Zod/TypeScript mediante OpenAPI y JSON Schema"},
            ],
            "subsections": [
                {"id": "sec-v5-8-1", "title": "Comparativa profunda de ejecución, memoria, concurrencia y sistemas de tipos (Python vs JS vs TS)"},
                {"id": "sec-v5-8-2", "title": "Arquitectura políglota: contratos OpenAPI/JSON Schema entre Python y TypeScript y evaluación global"},
            ],
            "purpose": (
                "Este capítulo de síntesis compara con rigor científico los tres lenguajes del Volumen V y muestra cómo "
                "combinarlos en arquitecturas reales de producción (por ejemplo, un frontend y pasarela API en TypeScript "
                "comunicándose con un motor de cálculo científico o de aprendizaje automático en Python)."
            ),
            "paragraphs": [
                {
                    "subsection": "sec-v5-8-1",
                    "text": (
                        "Aunque Python y JavaScript comparten tipado dinámico en tiempo de ejecución y gestión automática de memoria, "
                        "sus decisiones de diseño divergen en aspectos esenciales. Primero, en **semántica numérica y de tipos**: "
                        "Python posee enteros de precisión arbitraria (`int`) y distingue estrictamente entre tipos sin coerción "
                        "implícita entre cadenas y números (`\"5\" + 1` lanza `TypeError`), mientras que JavaScript unifica números "
                        "en `Number` (IEEE 754) + `BigInt` y realiza coerciones implícitas si no se usa `===` o TypeScript. Segundo, "
                        "en **modelo de objetos**: Python se basa en clases reales donde incluso las metaclases son objetos (`type`), "
                        "mientras que JavaScript se basa en delegación de prototipos (`[[Prototype]]`). Tercero, en **asincronía**: "
                        "en JavaScript una `Promise` es *ansiosa* (*eager*, comienza a ejecutarse en el instante en que se construye "
                        "y el Event Loop está siempre activo por defecto), mientras que una corrutina `async def` en Python es "
                        "estrictamente *perezosa* hasta que es agendada o esperada dentro de `asyncio.run(...)`."
                    ),
                },
                {
                    "subsection": "sec-v5-8-2",
                    "text": (
                        "Tanto el sistema de anotaciones de Python (`typing`, PEP 484/695) como TypeScript aplican borrado de tipos "
                        "en tiempo de ejecución (*type erasure*). Sin embargo, dado que en Python las anotaciones pueden conservarse "
                        "opcionalmente en el diccionario `__annotations__` de la clase o función, bibliotecas como `Pydantic` y "
                        "`FastAPI` inspeccionan dichas anotaciones al arrancar el proceso para compilar validadores en Rust y emitir "
                        "automáticamente un documento **OpenAPI 3.1 / JSON Schema**. A partir de ese único contrato normativo, el "
                        "equipo de TypeScript genera sus tipos estáticos y clientes HTTP sin duplicar definiciones manualmente, "
                        "garantizando consistencia matemática entre ambos extremos del sistema distribuido."
                    ),
                },
            ],
            "definition": (
                "Ejecución ansiosa frente a perezosa de tareas asíncronas (Eager Promises vs Lazy Coroutines): en ECMAScript "
                "el ejecutor de `new Promise(fn)` se invoca síncronamente al instanciarse, mientras que en Python (y Rust) "
                "invocar una función `async` devuelve un objeto corrutina inerte hasta que el bucle de eventos lo impulsa."
            ),
            "consejo": (
                "En arquitecturas políglotas Python + TypeScript, utiliza el esquema OpenAPI exportado por FastAPI/Pydantic "
                "o definiciones Protobuf como única fuente de verdad en el pipeline de CI para detectar rupturas de contrato antes de desplegar."
            ),
            "self_check": (
                "¿Por qué llamar a una función `async def f()` en Python sin anteponer `await` ni `asyncio.create_task(f())` "
                "no ejecuta ni una sola línea del cuerpo de `f` y emite un `RuntimeWarning: coroutine 'f' was never awaited`?"
            ),
            "derivation": {
                "title": "Ahorro de ancho de banda en serialización binaria frente a JSON textual entre servicios",
                "assumptions": ["Un lote de N registros ocupa N * S_json bytes en JSON UTF-8 frente a N * S_bin bytes en formato binario compacto"],
                "steps": [
                    {"equation": r"B_{\text{saved}} = N \cdot (S_{\text{json}} - S_{\text{bin}})", "justification": "Reducción por registro al eliminar nombres de claves repetidos y formateo decimal ASCII"},
                    {"equation": r"R_{\text{comp}} = \frac{S_{\text{json}}}{S_{\text{bin}}}", "justification": "Factor de compresión de representación de carga útil"},
                ],
                "Verify": {"left": "N * S_json - N * S_bin", "right": "N * (S_json - S_bin)"},
            },
            "worked_problem": {
                "prompt": (
                    "Una pasarela en TypeScript envía lotes de $N = 5000$ eventos de telemetría a un servicio de análisis en Python. "
                    "En formato JSON textual cada objeto `{ \"sensorId\": ..., \"timestamp\": ..., \"value\": ... }` ocupa en promedio "
                    "$S_{\\text{json}} = 76\\text{ B}$, mientras que codificado en binario compacto ocupa $S_{\\text{bin}} = 20\\text{ B}$. "
                    "Calcula cuántos kilobytes (dividiendo entre 1000) se ahorran por cada lote transmitido."
                ),
                "expression": "(5000 * (76 - 20)) / 1000",
                "solution": {
                    "model": "Ahorro de tráfico de red entre representación JSON y binaria",
                    "given": [
                        {"symbol": "N", "value": "5000", "description": "Eventos por lote"},
                        {"symbol": "S_json", "value": "76 B", "description": "Tamaño medio en JSON UTF-8"},
                        {"symbol": "S_bin", "value": "20 B", "description": "Tamaño en binario compacto"},
                    ],
                    "steps": [
                        {"step": "Multiplicamos los 5000 eventos por los 56 B ahorrados y dividimos entre 1000 B/kB", "equation": r"\Delta B_{\text{kB}} = \frac{5000 \cdot (76 - 20)}{1000}", "expression": "(5000 * (76 - 20)) / 1000"},
                    ],
                    "conclusion": "Se ahorran 280 kB por lote (pasando de 380 kB a 100 kB).",
                },
            },
            "practice_problems": [
                {"prompt": "Un contrato OpenAPI define 18 endpoints REST y cada endpoint especifica 3 esquemas (petición, respuesta 200 y error 400). ¿Cuántos esquemas genera automáticamente el generador de tipos de TypeScript ($18 \\times 3$)?", "expression": "18 * 3", "difficulty": "FOUNDATIONAL", "problem_type": "DIRECT_SUBSTITUTION"},
                {"prompt": "Si una respuesta JSON de 120 000 bytes se comprime con Brotli a un 25 % de su tamaño original ($120000 / 4$), ¿cuántos bytes se transmiten por la red?", "expression": "120000 / 4", "difficulty": "FOUNDATIONAL", "problem_type": "DIRECT_SUBSTITUTION"},
                {"prompt": "Un servicio en Python delega un cálculo matricial a una extensión compilada en Rust (`PyO3`) reduciendo el tiempo por petición de 45 ms a 3 ms. Para 200 peticiones secuenciales, ¿cuántos milisegundos totales se ahorran?", "expression": "200 * (45 - 3)", "difficulty": "INTERMEDIATE", "problem_type": "MULTI_STEP"},
                {"prompt": "Una aplicación web carga un módulo WebAssembly de 180 KiB y un bundle TypeScript/JS de 95 KiB. ¿Cuántos KiB totales descarga el cliente en el arranque inicial?", "expression": "180 + 95", "difficulty": "INTERMEDIATE", "problem_type": "DESIGN"},
            ],
        },
    ],
}


def main() -> None:
    s4 = build_studium_volume(VOL04_SPEC)
    s5 = build_studium_volume(VOL05_SPEC)
    report_path = ROOT / "reports" / "vol04-vol05-build.json"
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(json.dumps([s4, s5], indent=2, ensure_ascii=False), encoding="utf-8")


if __name__ == "__main__":
    main()
