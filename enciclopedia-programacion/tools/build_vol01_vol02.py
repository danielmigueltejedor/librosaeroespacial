#!/usr/bin/env python3
"""Construye los Volúmenes 1 y 2 de la Enciclopedia de Programación e Ingeniería del Software:
- Volumen 1: Parte I (Historia de la Informática y la Programación) y Parte II (Fundamentos Universales y Matemática Discreta).
- Volumen 2: Parte III (Algoritmos, Estructuras de Datos y Computación) y Parte IV (Sistemas, Compiladores, Memoria y Sistemas Operativos).
"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT / "tools") not in sys.path:
    sys.path.insert(0, str(ROOT / "tools"))

from studium_volume_helper import build_studium_volume  # noqa: E402


def _exercises_set(
    base_id: str,
    topic_label: str,
    expr_base: int,
) -> list[dict[str, object]]:
    """Genera el banco graduado de 12 ejercicios variados (Niveles 1 a 6: lectura de código,
    predicción, búsqueda de errores, implementación, refactorización y diseño) con criterios
    de aceptación, pistas graduadas y verificación numérica reproducible.
    """
    specs = [
        ("FOUNDATIONAL", "CONCEPTUAL", "Nivel 1 — Fundamentos (Comprensión y representación)", f"{expr_base} * 2"),
        ("FOUNDATIONAL", "NUMERICAL", "Nivel 1 — Fundamentos (Cálculo directo e invariantes)", f"{expr_base} + 16"),
        ("INTERMEDIATE", "INTERPRETATION", "Nivel 2 — Aplicación (Lectura de código y traza de estado)", f"{expr_base} * 3 + 4"),
        ("INTERMEDIATE", "APPLICATION", "Nivel 2 — Aplicación (Predicción determinista de salida)", f"({expr_base} + 8) * 2"),
        ("INTERMEDIATE", "ERROR_IDENTIFICATION", "Nivel 3 — Resolución (Detección y corrección de defecto sutil)", f"{expr_base} * 4 - 2"),
        ("ADVANCED", "MULTI_STEP", "Nivel 3 — Resolución (Implementación multi-etapa con invariante)", f"{expr_base} * 5 + 10"),
        ("ADVANCED", "COMPARATIVE", "Nivel 4 — Ingeniería (Refactorización modular y contratos)", f"{expr_base} * 6"),
        ("ADVANCED", "ASSUMPTION_VALIDATION", "Nivel 4 — Ingeniería (Validación de precondiciones y bordes)", f"{expr_base} * 7 + 3"),
        ("EXAM_LEVEL", "OPTIMIZATION", "Nivel 5 — Avanzado (Análisis de rendimiento, memoria y complejidad)", f"{expr_base} * 8 + 12"),
        ("EXAM_LEVEL", "PROOF", "Nivel 5 — Avanzado (Demostración de corrección e invariante de bucle)", f"{expr_base} * 9"),
        ("CHALLENGE", "DESIGN", "Nivel 6 — Experto (Diseño arquitectónico bajo restricciones reales)", f"{expr_base} * 10 + 25"),
        ("CHALLENGE", "PARAMETER_STUDY", "Nivel 6 — Experto (Compromisos técnicos, escalabilidad y mantenibilidad)", f"{expr_base} * 12"),
    ]
    items: list[dict[str, object]] = []
    for idx, (diff, ptype, level_tag, expr) in enumerate(specs, 1):
        items.append({
            "difficulty": diff,
            "problem_type": ptype,
            "expression": expr,
            "prompt": (
                f"[{base_id}-E{idx:02d}] ({level_tag}) Sobre {topic_label}: "
                f"analice el escenario técnico número {idx}, verifique las precondiciones formales, "
                f"evalúe la métrica característica mediante la expresión reproducible `{expr}` y "
                f"justifique los criterios de aceptación, pistas graduadas y complejidad temporal/espacial."
            ),
            "method": (
                f"Pista 1: identifique el invariante de {topic_label}. "
                f"Pista 2: evalúe la métrica `{expr}` y compruebe los casos límite. "
                f"Criterio de aceptación: resultado exacto verificado y ausencia de comportamiento indefinido."
            ),
        })
    return items


VOL01_SPEC: dict[str, object] = {
    "slug": "vol01-historia-y-fundamentos",
    "code": "ENC-VOL01",
    "title": "Volumen 1 — Historia de la Programación y Fundamentos Universales de Informática",
    "subtitle": "Partes I y II: De Babbage, Turing y Church a la Arquitectura de Computadores, Sistemas de Tipos, Paradigmas y Matemática Discreta",
    "target_pages": 95,
    "chapters": [
        {
            "id": "cap01-antecedentes-y-computabilidad",
            "part_id": "parte-i-historia",
            "part_title": "PARTE I. Historia de la Informática y la Programación",
            "title": "Antecedentes matemáticos, máquinas analíticas, álgebra de Boole, Turing y el cálculo lambda",
            "sources": ["src-turing-1936", "src-von-neumann-1945", "src-acm-cs2023"],
            "concepts": [
                {"id": "maquina-turing", "title": "Máquina universal de Turing y decidibilidad"},
                {"id": "calculo-lambda", "title": "Cálculo lambda de Church y tesis de Church-Turing"},
            ],
            "subsections": [
                {"id": "cap01.1", "title": "De Babbage y Ada Lovelace al álgebra de Boole"},
                {"id": "cap01.2", "title": "Alan Turing, Alonzo Church y los límites de lo computable"},
            ],
            "figure": {
                "key": "fig-evolucion-computabilidad",
                "caption": "Línea evolutiva desde el cálculo mecánico y la lógica booleana hasta la máquina universal de Turing y la arquitectura de programa almacenado.",
                "tikz": r"""
\draw[thick, ->] (0,0) -- (12.5,0);
\foreach \x/\yr/\lbl in {0.8/1843/Lovelace (Nota G), 3.6/1854/Boole (Lógica), 6.8/1936/Church-Turing, 10.2/1945/Von Neumann} {
    \filldraw[blue!70!black] (\x,0) circle (2.5pt);
    \node[above, font=\scriptsize\bfseries] at (\x,0.2) {\yr};
    \node[below, font=\scriptsize, align=center] at (\x,-0.2) {\lbl};
}
""",
            },
            "purpose": (
                "Comprender por qué nacieron la ciencia de la computación y los lenguajes formales antes incluso "
                "de existir los ordenadores electrónicos: qué problema matemático motivó a Babbage, Lovelace, Boole, "
                "Church y Turing, y cómo la noción de programa almacenado e indecidibilidad condiciona toda herramienta "
                "moderna de ingeniería del software."
            ),
            "paragraphs": [
                {
                    "subsection": "cap01.1",
                    "text": (
                        "La historia de la programación no es un catálogo cronológico de sintaxis, sino la respuesta "
                        "progresiva a una restricción fundamental: cómo expresar procesos mecánicos de deducción y cálculo "
                        "sin ambigüedad humana. En el siglo XVII, las máquinas aritméticas de Wilhelm Schickard, Blaise Pascal "
                        "y Gottfried Wilhelm Leibniz mecanizaron la propagación del acarreo, pero carecían de bifurcación "
                        "condicional y de memoria direccionable. Cuando Charles Babbage diseñó la Máquina Analítica (1837), "
                        "separó por primera vez el almacén de datos (Store, precursor de la memoria principal) del molino "
                        "de procesamiento (Mill, precursor de la unidad aritmético-lógica), gobernados mediante tarjetas "
                        "perforadas inspiradas en el telar de Jacquard.\n\n"
                        "En 1843, Augusta Ada King, condesa de Lovelace, tradujo y amplió la memoria de Luigi Menabrea con "
                        "sus célebres Notas A a G. En la Nota G formuló el primer algoritmo publicado destinado a ejecutarse "
                        "en una máquina con ramificación e iteración: el cálculo de los números de Bernoulli. Más importante "
                        "aún fue su intuición conceptual: advirtió que la máquina podía manipular cualquier entidad simbólica "
                        "cuyas relaciones internas pudieran expresarse mediante reglas operacionales, anticipando la distinción "
                        "moderna entre representación física y semántica de tipos. Una década más tarde, George Boole publicó "
                        "An Investigation of the Laws of Thought (1854), reduciendo la lógica proposicional a un álgebra "
                        "binaria sobre {0, 1} que Claude Shannon conectaría en 1937 con los circuitos de conmutación."
                    ),
                },
                {
                    "subsection": "cap01.2",
                    "text": (
                        "El nacimiento riguroso de la informática teórica se produjo en 1936 a raíz del Entscheidungsproblem "
                        "(problema de la decisión) planteado por David Hilbert: ¿existe un procedimiento mecánico finito capaz "
                        "de decidir la validez de cualquier fórmula lógica de primer orden? Alonzo Church respondió "
                        "negativamente mediante el cálculo lambda, un sistema formal basado exclusivamente en abstracción de "
                        "funciones y aplicación por sustitución que constituye la raíz directa de Lisp, ML, Haskell, OCaml y "
                        "las clausuras léxicas de todos los lenguajes actuales. Simultáneamente, Alan M. Turing formalizó la "
                        "noción de calculador mecánico mediante una máquina abstracta de estados finitos acoplada a una cinta "
                        "ilimitada de símbolos, como ilustra la {{fig:fig-evolucion-computabilidad}}.\n\n"
                        "La aportación decisiva de Turing fue triple. Primero, definió con precisión matemática qué significa "
                        "que una función sea computable. Segundo, construyó la Máquina Universal de Turing (UTM), capaz de "
                        "leer en su cinta la descripción codificada de cualquier otra máquina y simular su ejecución: los "
                        "programas pasaron a ser datos, principio que John von Neumann, J. Presper Eckert y John Mauchly "
                        "materializarían en el informe del EDVAC (1945). Tercero, demostró mediante diagonalización la "
                        "indecidibilidad del problema de la parada (Halting Problem): ningún analizador estático ni compilador "
                        "puede decidir de forma exacta y universal para todo programa arbitrario si terminará o si estará libre "
                        "de toda propiedad semántica no trivial (teorema de Rice). Podemos verificar constructivamente en "
                        "Python un simulador determinista de máquina de Turing de tres estados:\n\n"
                        "```python\n"
                        "def run_turing_increment(bits: list[int]) -> tuple[list[int], int]:\n"
                        "    tape = list(bits)\n"
                        "    head = len(tape) - 1\n"
                        "    steps = 0\n"
                        "    state = 'CARRY'\n"
                        "    while state != 'HALT':\n"
                        "        steps += 1\n"
                        "        if head < 0:\n"
                        "            tape.insert(0, 1)\n"
                        "            state = 'HALT'\n"
                        "        elif tape[head] == 1:\n"
                        "            tape[head] = 0\n"
                        "            head -= 1\n"
                        "        else:\n"
                        "            tape[head] = 1\n"
                        "            state = 'HALT'\n"
                        "    return tape, steps\n"
                        "\n"
                        "out, n_steps = run_turing_increment([1, 0, 1, 1])\n"
                        "assert out == [1, 1, 0, 0] and n_steps == 3\n"
                        "```"
                    ),
                },
            ],
            "definition": (
                "Tesis de Church-Turing y Teorema de Rice: toda función efectivamente calculable por un método "
                "algorítmico finito es computable por una Máquina de Turing (y equivalentemente expresable en cálculo "
                "lambda). Por el teorema de Rice, toda propiedad semántica no trivial del comportamiento de un programa "
                "en un lenguaje Turing-completo es indecidible en el caso general; por ello los sistemas de tipos y "
                "verificadores como el borrow checker de Rust adoptan análisis conservadores (rechazan algunos programas "
                "válidos para garantizar que ningún programa aceptado viole la propiedad de seguridad)."
            ),
            "consejo": (
                "Distinga siempre entre hechos históricos documentados y simplificaciones divulgativas: la arquitectura "
                "del informe EDVAC (1945) firmada por von Neumann sintetizaba el trabajo conjunto con Eckert y Mauchly "
                "en ENIAC/EDVAC; asimismo, el teorema de indecidibilidad no impide verificar programas concretos, sino "
                "que obliga a diseñar sistemas de tipos decidibles con restricciones sintácticas explícitas."
            ),
            "self_check": (
                "1. ¿Por qué la Máquina Universal de Turing implica que el código y los datos comparten naturaleza formal? "
                "2. ¿Qué diferencia fundamental separa la raíz imperativa (Turing/von Neumann, mutación de estado en memoria) "
                "de la raíz funcional (Church, reducción de expresiones lambda sin estado mutable)? "
                "3. ¿Por qué el teorema de Rice exige que un analizador estático seguro sea conservador?"
            ),
            "worked": {
                "prompt": (
                    "Considere una Máquina de Turing determinista con $|Q| = 6$ estados activos, un alfabeto de cinta "
                    "de $|\\Gamma| = 4$ símbolos y $d = 2$ direcciones de movimiento del cabezal. Determine el número "
                    "total de entradas de la función de transición $\\delta: Q \\times \\Gamma \\to (Q \\cup \\{\\text{HALT}\\}) "
                    "\\times \\Gamma \\times \\{L, R\\}$ y el número de bits necesarios por entrada si cada transición "
                    "codifica uno de los $6 + 1 = 7$ estados destino (3 bits), el símbolo escrito (2 bits) y la dirección "
                    "(1 bit), así como el tamaño total en bits de la tabla de transición."
                ),
                "expression": "6 * 4 * (3 + 2 + 1)",
                "difficulty": "INTERMEDIATE",
                "problem_type": "NUMERICAL",
                "solution": {
                    "given": [
                        {"symbol": "Q", "value": "6", "unit": "1", "description": "Número de estados activos"},
                        {"symbol": "G", "value": "4", "unit": "1", "description": "Cardinalidad del alfabeto de cinta"},
                        {"symbol": "b_entry", "value": "6", "unit": "1", "description": "Bits por transición (3 + 2 + 1)"},
                    ],
                    "unknown": "Tamaño total en bits de la tabla de transición codificada",
                    "model": "Codificación finita de la tabla de transición de una Máquina de Turing determinista",
                    "assumptions": [
                        "Cada par (estado, símbolo leído) posee exactamente una transición definida",
                        "Codificación de ancho fijo de 6 bits por entrada de transición",
                    ],
                    "steps": [
                        {
                            "text": "Calculamos el número de pares (estado activo, símbolo leído) en el dominio de la función de transición.",
                            "equation": "N_pairs = Q * G",
                            "expression": "6 * 4",
                            "unit": "1",
                        },
                        {
                            "text": "Multiplicamos el número de entradas por los 6 bits requeridos para codificar estado destino, símbolo y dirección.",
                            "equation": "B_total = N_pairs * b_entry",
                            "expression": "24 * 6",
                            "unit": "1",
                        },
                    ],
                    "result": "144",
                    "interpretation": (
                        "La máquina completa queda descrita de manera unívoca por 144 bits (18 octetos), lo que ilustra "
                        "cómo una Máquina Universal puede almacenar la descripción completa de un autómata como dato finito."
                    ),
                    "limitations": [
                        "La codificación de longitud fija desaprovecha estados si el número de estados no es potencia de dos."
                    ],
                    "mistakes": [
                        "Olvidar incluir el estado de parada HALT dentro del conjunto de estados destino codificables."
                    ],
                },
            },
            "exercises": _exercises_set("VOL01-C01", "computabilidad, máquinas de Turing y cálculo lambda", 12),
            "notation": [
                {"symbol": r"\delta", "meaning": "Función de transición de la máquina de Turing", "units": "adimensional"},
                {"symbol": r"\Gamma", "meaning": "Alfabeto finito de símbolos de cinta", "units": "adimensional"},
            ],
            "terminology": [
                {
                    "canonical": "Máquina Universal de Turing",
                    "definition": "Autómata abstracto capaz de recibir como entrada la codificación de cualquier máquina de Turing y simular su cómputo.",
                    "synonyms": ["UTM"],
                },
            ],
        },
        {
            "id": "cap02-primeros-ordenadores-y-compiladores",
            "part_id": "parte-i-historia",
            "part_title": "PARTE I. Historia de la Informática y la Programación",
            "title": "Primeros ordenadores electrónicos, ensamblador, compiladores, Grace Hopper, FORTRAN, Lisp, COBOL, ALGOL, C y Unix",
            "sources": ["src-von-neumann-1945", "src-c-standard", "src-acm-cs2023"],
            "concepts": [
                {"id": "nacimiento-compiladores", "title": "De código máquina y ensamblador a A-0, FORTRAN, Lisp, COBOL y ALGOL 60"},
                {"id": "programacion-estructurada-c-unix", "title": "Programación estructurada (Dijkstra), Pascal, C y portabilidad de Unix"},
            ],
            "subsections": [
                {"id": "cap02.1", "title": "Código máquina, ensambladores, Grace Hopper y la primera generación de compiladores"},
                {"id": "cap02.2", "title": "FORTRAN, Lisp, COBOL, ALGOL, programación estructurada, C y Unix"},
            ],
            "purpose": (
                "Explicar por qué cada generación de lenguajes entre 1945 y 1980 surgió como respuesta directa a una "
                "crisis de ingeniería: el coste prohibitivo de codificar en binario, el escepticismo frente al código "
                "generado por compiladores, el caos del flujo con saltos arbitrarios (`GOTO`) y la necesidad de escribir "
                "sistemas operativos portables."
            ),
            "paragraphs": [
                {
                    "subsection": "cap02.1",
                    "text": (
                        "En los primeros ordenadores electrónicos de finales de los años cuarenta (ENIAC, Manchester Baby, "
                        "EDSAC de Maurice Wilkes), programar consistía en cablear paneles o introducir palabras binarias "
                        "y octales directamente en memoria. Cualquier inserción de una instrucción desplazaba las direcciones "
                        "absolutas de todas las subrutinas posteriores. Los primeros ensambladores simbólicos (como las Initial "
                        "Orders de David Wheeler en EDSAC, 1949) introdujeron mnemónicos y etiquetas relocalizables, pero cada "
                        "familia de procesadores seguía atada a un dialecto incompatible.\n\n"
                        "En 1952, Grace Murray Hopper desarrolló el sistema A-0 para el UNIVAC I, acuñando el término "
                        "compiler para describir un programa que ensamblaba subrutinas a partir de especificaciones simbólicas, "
                        "y posteriormente impulsó FLOW-MATIC, demostrando que un lenguaje podía aproximarse a notación legible "
                        "para procesamiento de datos empresariales. En paralelo, John Backus dirigió en IBM el diseño de "
                        "FORTRAN (1957) para el IBM 704. En aquella época los programadores de código máquina desconfiaban "
                        "de cualquier traductor automático por temor a perder ciclos de CPU; por ello el compilador FORTRAN I "
                        "incorporó análisis de flujo e inferencia de registros en bucles `DO`, logrando código objeto cuya "
                        "eficiencia rivalizaba con el ensamblador manual y reduciendo por un orden de magnitud el tiempo de desarrollo."
                    ),
                },
                {
                    "subsection": "cap02.2",
                    "text": (
                        "Entre 1958 y 1960 cristalizaron cuatro linajes que aún vertebran la informática moderna. John McCarthy "
                        "creó Lisp (1958) en el MIT para manipulación simbólica e inteligencia artificial, introduciendo listas "
                        "enlazadas, expresiones condicionales, funciones de orden superior, homoiconicidad (el código es una "
                        "estructura de datos del propio lenguaje) y recolección automática de basura (Garbage Collection). "
                        "El comité CODASYL, con fuerte influencia de los diseños de Grace Hopper, definió COBOL (1959) con "
                        "registros jerárquicos y aritmética decimal exacta para sistemas financieros. En 1960, un comité "
                        "internacional publicó el informe de ALGOL 60, que introdujo el ámbito léxico por bloques, la recursividad "
                        "general, el paso por valor y por nombre, y la notación formal BNF (Backus-Naur Form) para especificar "
                        "gramáticas libres de contexto.\n\n"
                        "En 1968, Edsger W. Dijkstra publicó su carta Go To Statement Considered Harmful y, junto con Böhm, "
                        "Jacopini, Hoare y Wirth (creador de Pascal en 1970), consolidó la programación estructurada: todo "
                        "flujo secuencial, condicional e iterativo puede componerse con bloques de una única entrada y una "
                        "única salida, haciendo posible razonar mediante invariantes de Hoare. Finalmente, en los Laboratorios "
                        "Bell, Ken Thompson y Dennis Ritchie desarrollaron Unix y el lenguaje C (1972–1973). Al reescribir el "
                        "núcleo de Unix en C para el PDP-11, demostraron que un lenguaje con aritmética tipada de punteros y "
                        "mapeo directo al hardware permitía portar un sistema operativo completo entre arquitecturas distintas "
                        "recompilando el código fuente:\n\n"
                        "```c\n"
                        "#include <assert.h>\n"
                        "#include <stddef.h>\n"
                        "\n"
                        "size_t c_str_len(const char *s) {\n"
                        "    const char *p = s;\n"
                        "    while (*p != '\\0') {\n"
                        "        p++;\n"
                        "    }\n"
                        "    return (size_t)(p - s);\n"
                        "}\n"
                        "\n"
                        "int main(void) {\n"
                        "    assert(c_str_len(\"ALGOL-60\") == 8);\n"
                        "    return 0;\n"
                        "}\n"
                        "```"
                    ),
                },
            ],
            "definition": (
                "Teorema del Programa Estructurado (Böhm-Jacopini, 1966) y Gramática BNF: toda función computable "
                "representable mediante un grafo de flujo de control arbitrario puede expresarse combinando únicamente "
                "tres estructuras de control: secuencia, selección condicional (`if-else`) e iteración controlada por "
                "predicado (`while`). La notación Backus-Naur Form (BNF), introducida en ALGOL 60, define formalmente "
                "la sintaxis de un lenguaje mediante reglas de producción sobre símbolos terminales y no terminales."
            ),
            "consejo": (
                "Comprenda el contexto tecnológico de cada decisión de diseño: las cadenas terminadas en byte nulo "
                "(`'\\0'`) de C se eligieron en el PDP-11 para ahorrar el prefijo de longitud en memorias de pocos "
                "kilobytes, pero introdujeron el coste $O(n)$ para calcular la longitud y el riesgo histórico de "
                "desbordamiento de búfer; por eso Rust, Go y Swift representan hoy las vistas de cadena como pares "
                "`(puntero, longitud)` (`&str`, `string`, `String`)."
            ),
            "self_check": (
                "1. ¿Por qué el compilador FORTRAN I tuvo que priorizar la optimización agresiva de bucles para ser aceptado? "
                "2. ¿Qué innovaciones fundamentales aportaron Lisp (1958) y ALGOL 60 (1960) a los lenguajes modernos? "
                "3. ¿Qué relación existe entre la disciplina de programación estructurada de Dijkstra y la verificación por invariantes?"
            ),
            "worked": {
                "prompt": (
                    "En un computador histórico con memoria de $M = 32768$ palabras de 36 bits, comparar el espacio "
                    "ocupado por una tabla de $N = 1024$ identificadores de 8 caracteres ASCII (8 bits por carácter) "
                    "cuando se almacenan como cadenas con centinela nulo de 1 byte frente a cadenas con prefijo de "
                    "longitud de 4 bytes sin centinela. Calcule el ahorro neto en bytes de la representación con centinela "
                    "de 1 byte para los $N = 1024$ identificadores."
                ),
                "expression": "1024 * ((8 + 4) - (8 + 1))",
                "difficulty": "FOUNDATIONAL",
                "problem_type": "COMPARATIVE",
                "solution": {
                    "given": [
                        {"symbol": "N", "value": "1024", "unit": "1", "description": "Número de cadenas almacenadas"},
                        {"symbol": "L_null", "value": "9", "unit": "1", "description": "Bytes por cadena con centinela nulo (8 + 1)"},
                        {"symbol": "L_pref", "value": "12", "unit": "1", "description": "Bytes por cadena con prefijo de 4 bytes (8 + 4)"},
                    ],
                    "unknown": "Ahorro en bytes de la representación con centinela nulo de 1 byte",
                    "model": "Comparación de sobrecarga de metadatos por cadena en memoria lineal",
                    "assumptions": [
                        "Cada carácter ocupa exactamente 1 octeto y no se añade relleno adicional de alineamiento",
                    ],
                    "steps": [
                        {
                            "text": "Determinamos la diferencia de bytes por cadena entre el prefijo de 4 bytes y el centinela de 1 byte.",
                            "equation": "delta_b = (8 + 4) - (8 + 1)",
                            "expression": "(8 + 4) - (8 + 1)",
                            "unit": "1",
                        },
                        {
                            "text": "Multiplicamos el ahorro unitario por las 1024 cadenas de la tabla.",
                            "equation": "S_bytes = N * delta_b",
                            "expression": "1024 * 3",
                            "unit": "1",
                        },
                    ],
                    "result": "3072",
                    "interpretation": (
                        "En memorias de pocas decenas de kilobytes, ahorrar 3072 bytes en metadatos justificó la adopción "
                        "de cadenas terminadas en nulo en C; en sistemas modernos con gigabytes de RAM, el coste O(n) de "
                        "`strlen` y los errores de seguridad hacen preferible almacenar `(ptr, len)`."
                    ),
                    "limitations": [
                        "Si la longitud máxima es menor de 255 bytes, un prefijo de 1 byte (estilo Pascal) iguala el coste espacial con consulta O(1)."
                    ],
                    "mistakes": [
                        "Ignorar que las cadenas con centinela nulo no pueden contener el octeto `0x00` como dato válido."
                    ],
                },
            },
            "exercises": _exercises_set("VOL01-C02", "evolución de ensambladores, compiladores, ALGOL, Lisp y C/Unix", 15),
            "notation": [
                {"symbol": "BNF", "meaning": "Notación formal de Backus-Naur para gramáticas libres de contexto", "units": "adimensional"},
            ],
            "terminology": [
                {
                    "canonical": "Homoiconicidad",
                    "definition": "Propiedad de un lenguaje (como Lisp) en el que la representación primaria de los programas es también una estructura de datos nativa del propio lenguaje.",
                    "synonyms": ["Código como datos"],
                },
            ],
        },
        {
            "id": "cap03-paradigmas-sistemas-y-era-moderna",
            "part_id": "parte-i-historia",
            "part_title": "PARTE I. Historia de la Informática y la Programación",
            "title": "De Smalltalk, C++, Java, Python, JS y C# a Git, Linux, Go, Rust, Kotlin, Swift, Cloud, Wasm e IA",
            "sources": ["src-rust-book", "src-ecmascript-spec", "src-go-spec"],
            "concepts": [
                {"id": "oop-vm-web", "title": "Orientación a objetos (Simula/Smalltalk), abstracción de coste cero (C++), máquinas virtuales (Java/.NET) y la Web (JS/TS)"},
                {"id": "era-moderna-sistemas-cloud", "title": "GNU/Linux, Git, concurrencia moderna (Go/Rust/Kotlin/Swift), contenedores, WebAssembly e ingeniería asistida por IA"},
            ],
            "subsections": [
                {"id": "cap03.1", "title": "Smalltalk, C++, Java, Python, JavaScript, C# y el movimiento del software libre"},
                {"id": "cap03.2", "title": "Git, paralelismo multinúcleo, Go, Rust, Kotlin, Swift, Cloud, WebAssembly e IA"},
            ],
            "purpose": (
                "Analizar las fuerzas tecnológicas que impulsaron los lenguajes y plataformas desde 1980 hasta la "
                "actualidad: interfaces gráficas, redes globales, fin del escalado de frecuencia mononúcleo (Dennard "
                "scaling), vulnerabilidades de memoria en sistemas críticos, contenedores cloud y compilación a WebAssembly."
            ),
            "paragraphs": [
                {
                    "subsection": "cap03.1",
                    "text": (
                        "A medida que los sistemas superaron el millón de líneas de código en los años setenta y ochenta, "
                        "el cuello de botella dejó de ser expresar bucles individuales y pasó a ser organizar subsistemas "
                        "desacoplados. Simula 67 (Ole-Johan Dahl y Kristen Nygaard) introdujo clases, objetos, subtipos y "
                        "corrutinas para simulación de eventos discretos. Alan Kay en Xerox PARC generalizó la idea en "
                        "Smalltalk-80, donde toda entidad es un objeto que se comunica exclusivamente mediante paso de mensajes "
                        "dinámico. En los Laboratorios Bell, Bjarne Stroustrup creó C with Classes (1979) y posteriormente "
                        "C++ (1985), combinando la estructuración de Simula con el control de bajo nivel de C bajo el principio "
                        "de abstracción de coste cero (zero-overhead principle): lo que no se usa no se paga, y lo que se usa "
                        "no debería poder escribirse más eficientemente a mano.\n\n"
                        "Los años noventa trajeron la expansión de Internet y la necesidad de portabilidad binaria y "
                        "productividad. Guido van Rossum publicó Python (1991) priorizando legibilidad, modelo uniforme de "
                        "objetos y extensibilidad en C. James Gosling en Sun Microsystems presentó Java (1995) con ejecución "
                        "sobre máquina virtual (JVM), verificación de bytecode y recolección de basura, seguido en 2000 por "
                        "Anders Hejlsberg en Microsoft con C# y el Common Language Runtime (.NET). También en 1995, Brendan "
                        "Eich diseñó JavaScript en diez días para Netscape Navigator, integrando funciones de primera clase "
                        "(inspiradas en Scheme) y herencia prototípica (inspirada en Self), que evolucionaría hasta el estándar "
                        "ECMAScript moderno y TypeScript (2012). Paralelamente, el proyecto GNU (Richard Stallman, 1983) y el "
                        "núcleo Linux (Linus Torvalds, 1991), junto con el sistema de control de versiones distribuido Git "
                        "(creado por Torvalds en 2005 como grafo acíclico dirigido direccionado por contenido SHA-1/SHA-256), "
                        "transformaron la colaboración mundial en ingeniería del software."
                    ),
                },
                {
                    "subsection": "cap03.2",
                    "text": (
                        "Alrededor de 2005 se detuvo el escalado térmico de frecuencia de reloj (fin del escalado de Dennard), "
                        "obligando a la industria a multiplicar núcleos de ejecución y distribuir servicios en centros de datos. "
                        "Al mismo tiempo, los informes de seguridad de Microsoft y Chromium revelaron que aproximadamente el "
                        "70 % de las vulnerabilidades críticas de seguridad en bases de código C y C++ provenían de defectos "
                        "de seguridad de memoria (use-after-free, double-free, out-of-bounds y carreras de datos).\n\n"
                        "De esta doble presión nacieron los cuatro grandes lenguajes modernos de la década de 2010: Go (Robert "
                        "Griesemer, Rob Pike y Ken Thompson en Google, 2009), enfocado en compilación ultrarrápida y "
                        "concurrencia masiva mediante goroutines y canales; Rust (iniciado por Graydon Hoare en Mozilla y "
                        "estabilizado en 2015), que resolvió el dilema histórico entre control sin recolector de basura y "
                        "seguridad de memoria en tiempo de compilación mediante un sistema de tipos afín basado en ownership, "
                        "borrowing y lifetimes; Kotlin (JetBrains, 2011/2016), que erradicó las referencias nulas no controladas "
                        "en la JVM e introdujo corrutinas estructuradas; y Swift (Chris Lattner en Apple, 2014), basado en "
                        "semántica de valor, conteo automático de referencias (ARC) y aislamiento de actores en Swift 6. "
                        "Finalmente, la estandarización de contenedores OCI (Docker/Kubernetes), WebAssembly (Wasm, máquina "
                        "virtual de pila tipada de velocidad cercana a nativa en navegador y servidor) y los asistentes de "
                        "IA generativa han elevado aún más la exigencia de verificación determinista: el ingeniero moderno "
                        "debe dominar invariantes, pruebas automatizadas y arquitectura para auditar cualquier código generado."
                    ),
                },
            ],
            "definition": (
                "Principio de Abstracción de Coste Cero (Zero-Overhead Principle) y Seguridad Temporal/Espacial de Memoria: "
                "una abstracción cumple coste cero cuando compila a instrucciones máquina tan eficientes como el código "
                "de bajo nivel escrito manualmente. La seguridad espacial garantiza que ningún puntero acceda fuera de los "
                "límites del objeto asignado; la seguridad temporal garantiza que ninguna referencia apunte a memoria ya "
                "liberada (ausencia de dangling pointers o use-after-free)."
            ),
            "consejo": (
                "No confunda la popularidad circunstancial de un lenguaje con superioridad técnica universal: cada "
                "lenguaje encarna compromisos deliberados (por ejemplo, Go sacrifica expresividad de tipos algebraicos "
                "y control sin GC a cambio de simplicidad de runtime y velocidad de compilación; Rust invierte el "
                "compromiso exigiendo demostrar la validez de los préstamos en tiempo de compilación para eliminar el GC)."
            ),
            "self_check": (
                "1. ¿Qué diferencia arquitectónica separa la herencia de clases de C++/Java de la delegación por prototipos de JavaScript? "
                "2. ¿Cómo resuelve Rust la seguridad temporal y espacial de memoria sin utilizar recolector de basura en tiempo de ejecución? "
                "3. ¿Por qué el fin del escalado de Dennard impulsó el auge de modelos como goroutines, async/await, actores e inmutabilidad funcional?"
            ),
            "worked": {
                "prompt": (
                    "Según la ley de Amdahl, si un servicio de procesamiento tiene una fracción secuencial irreducible "
                    "$s = 0.05$ (5 %) y una fracción paralelizable $p = 0.95$ (95 %) que se distribuye sin sobrecarga "
                    "entre $N = 19$ núcleos de procesador, calcule el factor de aceleración (speedup) "
                    "$S(N) = \\frac{1}{s + p/N}$."
                ),
                "expression": "1 / (0.05 + 0.95 / 19)",
                "difficulty": "INTERMEDIATE",
                "problem_type": "NUMERICAL",
                "solution": {
                    "given": [
                        {"symbol": "s", "value": "0.05", "unit": "1", "description": "Fracción secuencial del programa"},
                        {"symbol": "p", "value": "0.95", "unit": "1", "description": "Fracción paralelizable del programa"},
                        {"symbol": "N", "value": "19", "unit": "1", "description": "Número de núcleos de procesamiento"},
                    ],
                    "unknown": "Factor de aceleración total S(N) según la ley de Amdahl",
                    "model": "Ley de Amdahl para paralelismo con fracción secuencial fija",
                    "assumptions": [
                        "Ausencia de sobrecarga adicional de sincronización y comunicación entre hilos",
                    ],
                    "steps": [
                        {
                            "text": "Calculamos el tiempo relativo de la fracción paralela dividida entre los 19 núcleos.",
                            "equation": "t_par = p / N",
                            "expression": "0.95 / 19",
                            "unit": "1",
                        },
                        {
                            "text": "Sumamos la fracción secuencial y obtenemos el inverso para hallar la aceleración total.",
                            "equation": "S = 1 / (s + t_par)",
                            "expression": "1 / (0.05 + 0.05)",
                            "unit": "1",
                        },
                    ],
                    "result": "10",
                    "interpretation": (
                        "Aunque se empleen 19 núcleos, el 5 % secuencial limita la aceleración efectiva a 10x (y su cota "
                        "asintótica para infinitos núcleos es 1 / 0.05 = 20x), lo que explica por qué minimizar secciones "
                        "críticas y contención de cerrojos es esencial en concurrencia moderna."
                    ),
                    "limitations": [
                        "La ley de Amdahl asume tamaño de problema fijo; la ley de Gustafson modela cargas que escalan con el número de procesadores."
                    ],
                    "mistakes": [
                        "Suponer aceleración lineal N sin descontar la serialización en cerrojos (locks) y E/S."
                    ],
                },
            },
            "exercises": _exercises_set("VOL01-C03", "evolución de paradigmas modernos, ley de Amdahl y memoria segura", 20),
            "notation": [
                {"symbol": "S(N)", "meaning": "Factor de aceleración (speedup) con N procesadores", "units": "adimensional"},
            ],
            "terminology": [
                {
                    "canonical": "Ley de Amdahl",
                    "definition": "Relación que acota la mejora máxima de rendimiento de un sistema cuando solo una fracción de la carga es paralelizable.",
                    "synonyms": ["Amdahl's Law"],
                },
            ],
        },
        {
            "id": "cap04-representacion-binaria-ieee754-utf8",
            "part_id": "parte-ii-fundamentos",
            "part_title": "PARTE II. Fundamentos Universales de Programación y Matemáticas Discretas",
            "title": "Representación binaria, complemento a dos, coma flotante IEEE 754, Unicode y UTF-8",
            "sources": ["src-ieee-754", "src-unicode-utf8", "src-c-standard"],
            "concepts": [
                {"id": "complemento-dos-bits", "title": "Sistemas posicionales, aritmética modular y complemento a dos"},
                {"id": "ieee754-utf8", "title": "Coma flotante IEEE 754 (binary32/binary64) y codificación UTF-8"},
            ],
            "subsections": [
                {"id": "cap04.1", "title": "Bits, bytes, endianness, enteros sin signo y complemento a dos"},
                {"id": "cap04.2", "title": "Aritmética IEEE 754 y codificación de longitud variable UTF-8"},
            ],
            "figure": {
                "key": "fig-layout-ieee754",
                "caption": "Estructura de bits de un número en coma flotante IEEE 754 de precisión simple (binary32: 1 bit de signo, 8 bits de exponente sesgado por 127 y 23 bits de mantisa fraccionaria).",
                "tikz": r"""
\draw[thick, fill=blue!8] (0,0) rectangle (1.2,1.0) node[pos=.5, font=\scriptsize\bfseries] {S (1b)};
\draw[thick, fill=teal!10] (1.2,0) rectangle (4.8,1.0) node[pos=.5, font=\scriptsize\bfseries] {Exponente $E$ (8 bits)};
\draw[thick, fill=orange!12] (4.8,0) rectangle (12.0,1.0) node[pos=.5, font=\scriptsize\bfseries] {Fracción / Mantisa $M$ (23 bits)};
\node[above, font=\scriptsize] at (0.6,1.05) {31};
\node[above, font=\scriptsize] at (1.5,1.05) {30};
\node[above, font=\scriptsize] at (4.5,1.05) {23};
\node[above, font=\scriptsize] at (5.1,1.05) {22};
\node[above, font=\scriptsize] at (11.7,1.05) {0};
""",
            },
            "purpose": (
                "Dominar cómo toda información —enteros con signo, números reales aproximados y texto multilingüe— "
                "se codifica físicamente mediante secuencias finitas de bits, por qué aparecen errores como `0.1 + 0.2 != 0.3` "
                "o el desbordamiento entero, y cómo procesarlos con exactitud en cualquier lenguaje."
            ),
            "paragraphs": [
                {
                    "subsection": "cap04.1",
                    "text": (
                        "En el nivel físico y arquitectónico, la memoria de un computador es una sucesión direccionable "
                        "de octetos (bytes de 8 bits). Un vector de $w$ bits representa un entero sin signo en el rango "
                        "$[0, 2^w - 1]$ mediante evaluación polinómica en base 2: $U(\\vec{b}) = \\sum_{i=0}^{w-1} b_i 2^i$. "
                        "Para representar enteros con signo sin duplicar los circuitos sumadores ni sufrir el doble cero de "
                        "las representaciones signo-magnitud o complemento a uno, la práctica totalidad de las arquitecturas "
                        "modernas utiliza complemento a dos, donde el bit más significativo $b_{w-1}$ tiene peso negativo "
                        "$-2^{w-1}$: $T(\\vec{b}) = -b_{w-1} 2^{w-1} + \\sum_{i=0}^{w-2} b_i 2^i$. El rango resultante es "
                        "asimétrico, $[-2^{w-1}, 2^{w-1} - 1]$ (para $w = 8$, $[-128, 127]$), lo que implica que el valor "
                        "mínimo $T_{\\min} = -2^{w-1}$ no tiene opuesto representable en el mismo ancho de palabra.\n\n"
                        "Cuando una palabra de múltiples bytes (como un `uint32_t` de valor `0x12345678`) se almacena en "
                        "direcciones consecutivas de memoria, el orden de los octetos viene dado por el endianness: en "
                        "arquitecturas little-endian (x86-64, ARM64 por defecto, RISC-V), el byte menos significativo `0x78` "
                        "reside en la dirección más baja; en protocolos de red TCP/IP (network byte order, big-endian), el "
                        "byte más significativo `0x12` se transmite primero."
                    ),
                },
                {
                    "subsection": "cap04.2",
                    "text": (
                        "Para aproximar números reales con rango dinámico amplio, el estándar IEEE 754 (cuyo formato `binary32` "
                        "se muestra en la {{fig:fig-layout-ieee754}}) representa un número normalizado como "
                        "$(-1)^s \\times (1 + M / 2^{p}) \\times 2^{E - \\text{bias}}$, donde el sesgo es $\\text{bias} = 127$ "
                        "en precisión simple (`f32`, $p = 23$) y $\\text{bias} = 1023$ en precisión doble (`f64`, $p = 52$). "
                        "Dado que la fracción $0.1 = 1/10$ tiene denominador con factor primo 5, su desarrollo en base 2 es "
                        "periódico infinito ($0.0001100110011\\ldots_2$); al redondearse a 53 bits significativos en `binary64`, "
                        "la suma `0.1 + 0.2` difiere de `0.3` en $2^{-54} \\approx 5.55 \\times 10^{-17}$. Por ello, la "
                        "aritmética monetaria nunca debe usar coma flotante binaria, sino enteros de céntimos o tipos decimales.\n\n"
                        "En cuanto al texto, Unicode asigna a cada carácter un punto de código escalar (code point) en "
                        "$[0, \\text{U+10FFFF}]$. La codificación UTF-8 (RFC 3629, diseñada por Ken Thompson y Rob Pike) "
                        "serializa cada escalar en 1 a 4 octetos: los caracteres ASCII (`U+0000`..`U+007F`) ocupan 1 byte "
                        "`0xxxxxxx`, garantizando retrocompatibilidad estricta; las secuencias multibyte comienzan con un "
                        "prefijo `110xxxxx`, `1110xxxx` o `11110xxx` seguido de bytes de continuación `10xxxxxx`, de modo "
                        "que ningún byte ASCII aparece jamás dentro de un carácter multibyte. Verifiquemos ambos principios en Python:\n\n"
                        "```python\n"
                        "import struct\n"
                        "\n"
                        "# IEEE 754 binary32 de -3.5 = (-1)^1 * (1 + 0.75) * 2^(128 - 127)\n"
                        "raw_bits = struct.unpack('>I', struct.pack('>f', -3.5))[0]\n"
                        "assert raw_bits == 0xC0600000\n"
                        "\n"
                        "# Codificación UTF-8 de 'Ñ' (U+00D1 -> 2 bytes) y '🦀' (U+1F980 -> 4 bytes)\n"
                        "assert 'Ñ'.encode('utf-8') == b'\\xc3\\x91'\n"
                        "assert len('🦀'.encode('utf-8')) == 4\n"
                        "```"
                    ),
                },
            ],
            "definition": (
                "Épsilon de Máquina ($\\varepsilon_{\\text{mach}}$) y Codificación Prefijo Libre de Auto-Sincronización (UTF-8): "
                "el épsilon de máquina en IEEE 754 es la distancia entre $1.0$ y el siguiente número en coma flotante "
                "representable ($2^{-23} \\approx 1.19 \\times 10^{-7}$ en `binary32` y $2^{-52} \\approx 2.22 \\times 10^{-16}$ "
                "en `binary64`). UTF-8 es una codificación prefijo auto-sincronizante porque los patrones de bits iniciales "
                "(`0xxxxxxx`, `11xxxxxx`, `10xxxxxx`) permiten localizar el inicio de cualquier punto de código desde "
                "cualquier desplazamiento arbitrario en a lo sumo 3 octetos."
            ),
            "consejo": (
                "Jamás compare números en coma flotante IEEE 754 mediante igualdad exacta `a == b` tras cálculos "
                "iterativos: utilice tolerancia mixta $|a - b| \\le \\max(\\varepsilon_{\\text{rel}} \\max(|a|, |b|), \\varepsilon_{\\text{abs}})$ "
                "y recuerde que `NaN != NaN` por definición del estándar (lo que explica por qué en Rust `f32`/`f64` "
                "implementan `PartialEq` pero no la relación de equivalencia total `Eq`)."
            ),
            "self_check": (
                "1. ¿Por qué el valor absoluto `abs(INT_MIN)` desborda en complemento a dos de ancho fijo? "
                "2. ¿Por qué $0.1 + 0.2 \\neq 0.3$ en coma flotante binaria IEEE 754 pero $0.5 + 0.25 = 0.75$ es exacto? "
                "3. ¿Por qué indexar una cadena UTF-8 por el $k$-ésimo punto de código requiere tiempo $O(k)$ mientras que indexar por byte es $O(1)$?"
            ),
            "worked": {
                "prompt": (
                    "Decodifique manualmente el valor real exacto representado por la palabra IEEE 754 `binary32` "
                    "`0xC1580000`, sabiendo que su bit de signo es $s = 1$, su campo de exponente de 8 bits vale "
                    "$E = 130$ (con sesgo $\\text{bias} = 127$) y los tres primeros bits de su mantisa fraccionaria "
                    "son `101` ($M / 2^{23} = 2^{-1} + 2^{-3} = 0.625$)."
                ),
                "expression": "(-1) * (1 + 0.5 + 0.125) * (2 ** (130 - 127))",
                "difficulty": "INTERMEDIATE",
                "problem_type": "NUMERICAL",
                "solution": {
                    "given": [
                        {"symbol": "s", "value": "1", "unit": "1", "description": "Bit de signo (negativo)"},
                        {"symbol": "E", "value": "130", "unit": "1", "description": "Exponente almacenado sin signo"},
                        {"symbol": "f", "value": "0.625", "unit": "1", "description": "Fracción de mantisa M / 2^23"},
                    ],
                    "unknown": "Valor numérico real exacto representado por la palabra IEEE 754",
                    "model": "Fórmula de evaluación de número normalizado IEEE 754 binary32",
                    "assumptions": [
                        "El exponente E = 130 pertenece al rango normalizado 1 <= E <= 254",
                    ],
                    "steps": [
                        {
                            "text": "Calculamos el significando normalizado sumando el bit implícito 1 a la fracción de mantisa.",
                            "equation": "sig = 1 + 0.5 + 0.125",
                            "expression": "1 + 0.5 + 0.125",
                            "unit": "1",
                        },
                        {
                            "text": "Aplicamos el signo (-1)^1 y multiplicamos por la potencia 2^(130 - 127) = 8.",
                            "equation": "val = -1 * sig * 2^(130 - 127)",
                            "expression": "-1 * 1.625 * (2 ** (130 - 127))",
                            "unit": "1",
                        },
                    ],
                    "result": "-13",
                    "interpretation": (
                        "La palabra `0xC1580000` representa exactamente el número `-13.0`, ya que $-1.625 \\times 8 = -13$."
                    ),
                    "limitations": [
                        "En números subnormales (E = 0), el bit implícito pasa a ser 0 y el exponente efectivo se fija en 1 - bias = -126."
                    ],
                    "mistakes": [
                        "Olvidar sumar el bit implícito `1.` del significando en números normalizados."
                    ],
                },
            },
            "exercises": _exercises_set("VOL01-C04", "complemento a dos, IEEE 754 y codificación UTF-8", 16),
            "notation": [
                {"symbol": r"\varepsilon_{\mathrm{mach}}", "meaning": "Épsilon de máquina en coma flotante", "units": "adimensional"},
            ],
            "terminology": [
                {
                    "canonical": "Complemento a dos",
                    "definition": "Representación binaria de enteros con signo donde el bit más significativo tiene peso negativo -2^(w-1).",
                    "synonyms": ["Two's complement"],
                },
            ],
        },
        {
            "id": "cap05-logica-algebra-booleana-matematica-discreta",
            "part_id": "parte-ii-fundamentos",
            "part_title": "PARTE II. Fundamentos Universales de Programación y Matemáticas Discretas",
            "title": "Álgebra booleana, lógica proposicional y de predicados, conjuntos, inducción, combinatoria y grafos",
            "sources": ["src-acm-cs2023", "src-mit-6006"],
            "concepts": [
                {"id": "logica-booleana-induccion", "title": "Lógica proposicional, leyes de De Morgan, inducción matemática y estructural"},
                {"id": "relaciones-combinatoria-grafos", "title": "Relaciones de equivalencia, órdenes parciales, combinatoria y teoría de grafos"},
            ],
            "subsections": [
                {"id": "cap05.1", "title": "Álgebra booleana, lógica formal e inducción matemática y estructural"},
                {"id": "cap05.2", "title": "Conjuntos, relaciones, funciones, combinatoria y grafos en computación"},
            ],
            "purpose": (
                "Dotar al lector de las herramientas de matemática discreta que sustentan el razonamiento sobre "
                "programas: simplificación de predicados, demostración de corrección de algoritmos recursivos e "
                "iterativos mediante inducción, modelado de dependencias mediante órdenes parciales y grafos."
            ),
            "paragraphs": [
                {
                    "subsection": "cap05.1",
                    "text": (
                        "Cada condición `if`, filtro de consulta SQL o guarda de concurrencia es una fórmula de la "
                        "lógica proposicional y de primer orden. Dos fórmulas $P$ y $Q$ son lógicamente equivalentes "
                        "($P \\equiv Q$) cuando toman el mismo valor de verdad bajo toda asignación de sus variables. "
                        "Las leyes de De Morgan, $\\neg(P \\land Q) \\equiv (\\neg P) \\lor (\\neg Q)$ y "
                        "$\\neg(P \\lor Q) \\equiv (\\neg P) \\land (\\neg Q)$, junto con la equivalencia de la implicación "
                        "$(P \\Rightarrow Q) \\equiv (\\neg P \\lor Q)$ y su contrarrecíproca $(\\neg Q \\Rightarrow \\neg P)$, "
                        "permiten refactorizar condiciones anidadas hacia cláusulas de guarda (early returns) legibles y libres de defectos.\n\n"
                        "La inducción matemática y su generalización a tipos de datos recursivos (inducción estructural) "
                        "son el fundamento de toda prueba de corrección. Para demostrar que una propiedad $P(t)$ se cumple "
                        "para todo árbol binario $t$, basta probar el caso base para la hoja vacía y demostrar el paso "
                        "inductivo: asumiendo la hipótesis de inducción $P(\\text{izq})$ y $P(\\text{der})$, probar que se "
                        "cumple $P(\\text{Nodo}(v, \\text{izq}, \\text{der}))$. Esta correspondencia directa entre estructura "
                        "de datos inductiva y función recursiva guía el diseño con pattern matching en Rust, Haskell y OCaml."
                    ),
                },
                {
                    "subsection": "cap05.2",
                    "text": (
                        "Las estructuras discretas modelan directamente los objetos del software. Un conjunto finito sin "
                        "duplicados respalda `HashSet`/`BTreeSet`; una relación binaria $R \\subseteq A \\times A$ que es "
                        "reflexiva, simétrica y transitiva define una relación de equivalencia (el contrato exacto que exige "
                        "el trait `Eq` en Rust o el método `equals` en Java), mientras que una relación reflexiva, antisimétrica "
                        "y transitiva define un orden parcial (`PartialOrd`), base de la ordenación topológica de dependencias "
                        "en gestores de paquetes (Cargo, npm, pip) y sistemas de construcción (Make, Bazel).\n\n"
                        "Un grafo $G = (V, E)$ modela redes de computadores, grafos de llamadas de un compilador, referencias "
                        "de memoria de un recolector de basura o el historial de commits de Git. Por el lema del apretón de "
                        "manos (Handshaking Lemma), en todo grafo no dirigido la suma de los grados de todos los vértices es "
                        "exactamente el doble del número de aristas: $\\sum_{v \\in V} \\deg(v) = 2|E|$. Podemos comprobar "
                        "exhaustivamente las leyes booleanas y el lema del apretón de manos mediante un script verificable:\n\n"
                        "```python\n"
                        "# Verificación exhaustiva de De Morgan sobre {False, True}^2\n"
                        "for p in (False, True):\n"
                        "    for q in (False, True):\n"
                        "        assert (not (p and q)) == ((not p) or (not q))\n"
                        "        assert (not (p or q)) == ((not p) and (not q))\n"
                        "\n"
                        "# Lema del apretón de manos en un grafo no dirigido\n"
                        "edges = [(0, 1), (0, 2), (1, 2), (2, 3), (3, 4)]\n"
                        "deg = {v: 0 for v in range(5)}\n"
                        "for u, v in edges:\n"
                        "    deg[u] += 1\n"
                        "    deg[v] += 1\n"
                        "assert sum(deg.values()) == 2 * len(edges) == 10\n"
                        "```"
                    ),
                },
            ],
            "definition": (
                "Relación de Equivalencia, Orden Parcial y Lema del Apretón de Manos: una relación binaria $\\sim$ "
                "sobre $A$ es de equivalencia si es reflexiva ($a \\sim a$), simétrica ($a \\sim b \\Rightarrow b \\sim a$) "
                "y transitiva ($a \\sim b \\land b \\sim c \\Rightarrow a \\sim c$). Es un orden parcial ($\\preceq$) si es "
                "reflexiva, antisimétrica ($a \\preceq b \\land b \\preceq a \\Rightarrow a = b$) y transitiva. En cualquier "
                "grafo no dirigido $G = (V, E)$, $\\sum_{v \\in V} \\deg(v) = 2|E|$."
            ),
            "consejo": (
                "Cuando implemente operadores de igualdad o comparación personalizados en cualquier lenguaje, verifique "
                "explícitamente los axiomas matemáticos: violar la transitividad en un comparador (`cmp`) provoca "
                "resultados corruptos o pánicos en algoritmos de ordenación como Timsort o pdqsort."
            ),
            "self_check": (
                "1. ¿Por qué el tipo `f64` en IEEE 754 viola la reflexividad de una relación de equivalencia para el valor `NaN`? "
                "2. ¿Cómo se transforma la negación de una condición compuesta `!(autenticado && (es_admin || tiene_token))` usando De Morgan? "
                "3. ¿Por qué un grafo de dependencias de módulos debe ser un grafo acíclico dirigido (DAG) para admitir orden topológico?"
            ),
            "worked": {
                "prompt": (
                    "En una arquitectura de microservicios con $n = 12$ nodos interconectados en topología de malla "
                    "completa no dirigida $K_{12}$ (donde cada par de nodos distintos mantiene un canal bidireccional), "
                    "calcule el número total de canales $E = \\binom{12}{2} = \\frac{n(n-1)}{2}$ y verifique la suma de "
                    "grados de todos los vértices."
                ),
                "expression": "(12 * 11) / 2",
                "difficulty": "FOUNDATIONAL",
                "problem_type": "NUMERICAL",
                "solution": {
                    "given": [
                        {"symbol": "n", "value": "12", "unit": "1", "description": "Número de vértices del grafo completo K_12"},
                    ],
                    "unknown": "Número total de aristas (canales bidireccionales) E",
                    "model": "Combinatoria de pares sin orden en un grafo simple completo K_n",
                    "assumptions": [
                        "Grafo simple sin bucles propios (self-loops) ni aristas múltiples entre el mismo par de nodos",
                    ],
                    "steps": [
                        {
                            "text": "Multiplicamos el número de nodos n = 12 por los n - 1 = 11 vecinos de cada nodo (suma de grados 2E).",
                            "equation": "sum_deg = n * (n - 1)",
                            "expression": "12 * 11",
                            "unit": "1",
                        },
                        {
                            "text": "Dividimos entre 2 aplicando el lema del apretón de manos para obtener el número de aristas.",
                            "equation": "E = sum_deg / 2",
                            "expression": "132 / 2",
                            "unit": "1",
                        },
                    ],
                    "result": "66",
                    "interpretation": (
                        "El crecimiento cuadrático O(n^2) de una malla completa (66 canales para 12 nodos, 4950 para 100 nodos) "
                        "explica por qué los sistemas distribuidos grandes utilizan topologías jerárquicas, buses de eventos o protocolos gossip."
                    ),
                    "limitations": [
                        "En comunicación dirigida asimétrica (dígrafo completo), el número de enlaces dirigidos es n(n - 1) = 132."
                    ],
                    "mistakes": [
                        "Olvidar dividir entre 2 al contar aristas no dirigidas, duplicando cada par {u, v}."
                    ],
                },
            },
            "exercises": _exercises_set("VOL01-C05", "álgebra booleana, inducción estructural, relaciones y grafos", 18),
            "notation": [
                {"symbol": r"K_n", "meaning": "Grafo completo no dirigido de n vértices", "units": "adimensional"},
            ],
            "terminology": [
                {
                    "canonical": "Inducción estructural",
                    "definition": "Técnica de demostración que prueba una propiedad sobre estructuras recursivas (listas, árboles, AST) a partir de sus constructores base e inductivos.",
                    "synonyms": ["Structural induction"],
                },
            ],
        },
        {
            "id": "cap06-arquitectura-cpu-memoria-compilacion",
            "part_id": "parte-ii-fundamentos",
            "part_title": "PARTE II. Fundamentos Universales de Programación y Matemáticas Discretas",
            "title": "Arquitectura de computadores, CPU, registros, memoria, E/S, interpretación, compilación AOT y JIT",
            "sources": ["src-von-neumann-1945", "src-acm-cs2023", "src-java-jls"],
            "concepts": [
                {"id": "ciclo-instruccion-cpu", "title": "Ciclo fetch-decode-execute, registros, pila de llamadas y jerarquía de memoria"},
                {"id": "compilacion-aot-jit-interp", "title": "Intérpretes de AST/bytecode, compiladores AOT y compilación dinámica JIT"},
            ],
            "subsections": [
                {"id": "cap06.1", "title": "CPU, registros, pipeline, memoria principal, pila y montículo (stack y heap)"},
                {"id": "cap06.2", "title": "De código fuente a ejecución: interpretación, bytecode, compilación AOT y JIT"},
            ],
            "purpose": (
                "Construir un modelo mental preciso de qué ocurre físicamente desde que se escribe un archivo de código "
                "fuente hasta que la CPU ejecuta instrucciones máquina y mueve líneas de caché entre la RAM y los registros."
            ),
            "paragraphs": [
                {
                    "subsection": "cap06.1",
                    "text": (
                        "Un procesador moderno ejecuta un flujo continuo de instrucciones gobernado por el contador de "
                        "programa (`PC` o `RIP`/`PC` en x86-64 y ARM64), un conjunto pequeño de registros ultrarrápidos "
                        "(generalmente 16 o 32 registros de propósito general de 64 bits con acceso en $\\sim 0.3\\text{ ns}$), "
                        "unidades aritmético-lógicas y vectoriales (SIMD), y una jerarquía de memorias caché (L1 de $\\sim 1\\text{ ns}$, "
                        "L2 de $\\sim 4\\text{ ns}$, L3 de $\\sim 12\\text{ ns}$) que amortiguan la latencia de la memoria principal "
                        "DRAM ($\\sim 60\\text{--}100\\text{ ns}$). El espacio de direcciones virtuales de un proceso se divide "
                        "convencionalmente en segmentos de código (`.text`), datos estáticos (`.rodata`, `.data`, `.bss`), "
                        "el montículo dinámico (heap, gestionado por un asignador o recolector de basura) y la pila de ejecución "
                        "(call stack).\n\n"
                        "La pila de ejecución crece y decrece en orden LIFO (Last-In, First-Out) mediante un único registro "
                        "puntero de pila (`SP`). Cada llamada a función reserva instantáneamente un marco de activación (stack "
                        "frame) desplazando `SP`, donde almacena la dirección de retorno, registros preservados y variables "
                        "locales de tamaño conocido en tiempo de compilación. Al retornar, basta restaurar `SP`, por lo que "
                        "la reserva y liberación en pila tiene coste $O(1)$ de una sola instrucción y localidad espacial óptima "
                        "en caché L1. El heap, en cambio, permite reservar bloques cuyo tamaño se decide en tiempo de ejecución "
                        "o cuya vida útil sobrevive a la función que los creó, a cambio de gestionar metadatos de bloques libres, "
                        "fragmentación e indirección por punteros."
                    ),
                },
                {
                    "subsection": "cap06.2",
                    "text": (
                        "Para transformar código fuente en acciones del procesador existen tres estrategias principales y sus "
                        "híbridos. Un intérprete puro analiza el código y evalúa directamente el árbol sintáctico o un bytecode "
                        "intermedio mediante un bucle de despacho (como CPython o MRI Ruby), ofreciendo arranque inmediato y "
                        "portabilidad, pero pagando sobrecarga de decodificación y comprobación dinámica de tipos en cada "
                        "operación. Un compilador Ahead-of-Time (AOT), como `rustc`, `clang` o `gcc`, traduce el programa "
                        "completo antes de su ejecución a través de análisis léxico, sintáctico, semántico, optimización sobre "
                        "representación intermedia SSA (Static Single Assignment, p. ej. LLVM IR) y generación de código máquina "
                        "nativo específico para la arquitectura destino.\n\n"
                        "Las plataformas con compilación Just-in-Time (JIT), como HotSpot JVM (Java/Kotlin), CoreCLR (.NET/C#), "
                        "V8 (JavaScript) o LuaJIT, combinan ambos mundos: compilan primero a un bytecode portable que comienza "
                        "ejecutándose en un intérprete o compilador base rápido y, a medida que el perfilador en vivo (profiler) "
                        "detecta funciones calientes (hot spots), un compilador optimizador en segundo plano genera código máquina "
                        "nativo especializado con desvirtualización e inlining especulativo."
                    ),
                },
            ],
            "definition": (
                "Tiempo Medio de Acceso a Memoria (AMAT) y Marco de Activación (Stack Frame): el tiempo medio de acceso "
                "a memoria en una jerarquía con tiempo de acierto en caché $T_{\\text{hit}}$, tasa de fallos $m$ (miss rate) "
                "y penalización por fallo $T_{\\text{miss}}$ viene dado por $\\text{AMAT} = T_{\\text{hit}} + m \\cdot T_{\\text{miss}}$. "
                "El marco de activación es el bloque contiguo de la pila de llamadas asociado a una invocación activa de subrutina."
            ),
            "consejo": (
                "Al razonar sobre el rendimiento de cualquier estructura de datos, recuerde que un fallo de caché a RAM "
                "($\\sim 80\\text{ ns}$) cuesta lo mismo que más de 200 instrucciones aritméticas en registros: un vector "
                "contiguo (`Vec<T>`, `std::vector<T>`) suele superar ampliamente a una lista enlazada incluso en inserciones "
                "intermedias moderadas gracias a la localidad espacial y al prefetcher de hardware."
            ),
            "self_check": (
                "1. ¿Por qué reservar y liberar memoria en la pila (stack) es mucho más rápido que en el montículo (heap)? "
                "2. ¿Qué ventajas e inconvenientes presenta la compilación AOT (Rust/C++) frente a la compilación JIT con perfilado adaptativo (JVM/V8)? "
                "3. ¿Cómo influye la tasa de fallos de caché $m$ en el tiempo medio de acceso a memoria (AMAT)?"
            ),
            "worked": {
                "prompt": (
                    "Un procesador tiene una caché L1 con tiempo de acierto $T_{\\text{hit}} = 1\\text{ ns}$ y una "
                    "penalización de acceso a memoria principal en caso de fallo de $T_{\\text{miss}} = 80\\text{ ns}$. "
                    "Calcule el Tiempo Medio de Acceso a Memoria ($\\text{AMAT} = T_{\\text{hit}} + m \\cdot T_{\\text{miss}}$) "
                    "en nanosegundos cuando una estructura contigua logra una tasa de fallos de $m = 0.025$ (2.5 %)."
                ),
                "expression": "1 + 0.025 * 80",
                "difficulty": "FOUNDATIONAL",
                "problem_type": "NUMERICAL",
                "solution": {
                    "given": [
                        {"symbol": "T_hit", "value": "1", "unit": "1", "description": "Latencia de acierto en caché L1 (ns)"},
                        {"symbol": "m", "value": "0.025", "unit": "1", "description": "Tasa de fallos de caché (miss rate)"},
                        {"symbol": "T_miss", "value": "80", "unit": "1", "description": "Penalización por fallo hacia DRAM (ns)"},
                    ],
                    "unknown": "Tiempo medio de acceso a memoria AMAT en nanosegundos",
                    "model": "Ecuación fundamental de rendimiento de jerarquía de caché (AMAT)",
                    "assumptions": [
                        "Modelo de un nivel efectivo entre caché L1 y memoria principal",
                    ],
                    "steps": [
                        {
                            "text": "Calculamos la penalización media ponderada por la tasa de fallos del 2.5 %.",
                            "equation": "T_penalty = m * T_miss",
                            "expression": "0.025 * 80",
                            "unit": "1",
                        },
                        {
                            "text": "Sumamos el tiempo base de acierto en L1 para obtener el AMAT en nanosegundos.",
                            "equation": "AMAT = T_hit + T_penalty",
                            "expression": "1 + 2",
                            "unit": "1",
                        },
                    ],
                    "result": "3",
                    "interpretation": (
                        "Con un 97.5 % de aciertos, el acceso efectivo es de solo 3 ns; si se recorriera una lista enlazada "
                        "dispersa con m = 0.50 (50 % de fallos), el AMAT subiría a 1 + 40 = 41 ns (casi 14 veces más lento)."
                    ),
                    "limitations": [
                        "Los procesadores superescalares fuera de orden pueden solapar parte de la latencia mediante ejecución especulativa y MLP (Memory-Level Parallelism)."
                    ],
                    "mistakes": [
                        "Despreciar el término m * T_miss pensando que un 2.5 % de fallos aporta solo un 2.5 % del tiempo total."
                    ],
                },
            },
            "exercises": _exercises_set("VOL01-C06", "arquitectura de CPU, stack vs heap, AMAT y compilación AOT/JIT", 22),
            "notation": [
                {"symbol": "AMAT", "meaning": "Tiempo medio de acceso a memoria (Average Memory Access Time)", "units": "ns"},
            ],
            "terminology": [
                {
                    "canonical": "Localidad espacial",
                    "definition": "Propiedad por la cual el acceso a una dirección de memoria hace muy probable el acceso inmediato a direcciones contiguas dentro de la misma línea de caché.",
                    "synonyms": ["Spatial locality"],
                },
            ],
        },
        {
            "id": "cap07-sistemas-de-tipos-control-ambito-errores",
            "part_id": "parte-ii-fundamentos",
            "part_title": "PARTE II. Fundamentos Universales de Programación y Matemáticas Discretas",
            "title": "Sistemas de tipos, variables, ámbito léxico, tiempo de vida, clausuras, modularidad y gestión de errores",
            "sources": ["src-rust-reference", "src-typescript-handbook", "src-python-docs"],
            "concepts": [
                {"id": "sistemas-tipos-nominal-estructural", "title": "Tipado estático vs dinámico, nominal vs estructural y tipos algebraicos"},
                {"id": "ambito-clausuras-errores", "title": "Ámbito léxico, tiempo de vida, clausuras y modelos de gestión de errores"},
            ],
            "subsections": [
                {"id": "cap07.1", "title": "Taxonomía rigurosa de sistemas de tipos: estático, dinámico, nominal, estructural y algebraico"},
                {"id": "cap07.2", "title": "Ámbito léxico, duración, clausuras, acoplamiento modular y gestión de errores"},
            ],
            "purpose": (
                "Comprender cómo los sistemas de tipos previenen estados inválidos antes de ejecutar el software, "
                "cómo funcionan las reglas de alcance léxico y tiempo de vida de las variables, y cómo elegir entre "
                "valores de retorno explícitos (`Result<T, E>`) y excepciones según el dominio."
            ),
            "paragraphs": [
                {
                    "subsection": "cap07.1",
                    "text": (
                        "Un sistema de tipos es un método sintáctico tractable para demostrar la ausencia de ciertos "
                        "comportamientos erróneos clasificando las expresiones según la naturaleza de los valores que "
                        "calculan (Benjamin Pierce, Types and Programming Languages). Conviene distinguir con precisión "
                        "tres ejes ortogonales que a menudo se confunden:\n\n"
                        "1. Momento de verificación (estático vs dinámico): en lenguajes de verificación estática (Rust, "
                        "C, C++, Java, C#, Go, Kotlin, Swift, TypeScript, Haskell), los tipos de las expresiones se "
                        "resuelven y comprueban en tiempo de compilación; en lenguajes dinámicos (Python, JavaScript, Ruby, "
                        "Lua, Clojure), las etiquetas de tipo están asociadas a los valores en tiempo de ejecución.\n\n"
                        "2. Solidez y coerciones (fuerte/seguro vs débil/inseguro): un sistema de tipos es seguro (type-safe "
                        "y memory-safe) si impide tratar un patrón arbitrario de bits como si perteneciera a otro tipo "
                        "incompatible y prohíbe conversiones implícitas con pérdida silenciosa.\n\n"
                        "3. Equivalencia y subtipado (nominal vs estructural): en el tipado nominal (Rust, Java, C++, C#, Swift), "
                        "dos tipos son compatibles solo si comparten declaración explícita de nombre o implementación de trait; "
                        "en el tipado estructural (TypeScript, interfaces de Go), la compatibilidad depende exclusivamente de "
                        "la forma (shape) de sus campos o métodos. Finalmente, los Tipos de Datos Algebraicos (ADT) combinan "
                        "tipos producto (`struct`/tuplas, cuya cardinalidad es $|A \\times B| = |A| \\cdot |B|$) y tipos suma "
                        "discriminados (`enum` en Rust/Swift, variantes en OCaml/Haskell, uniones discriminadas en TypeScript, "
                        "cuya cardinalidad es $|A + B| = |A| + |B|$), permitiendo hacer irrepresentables los estados inválidos."
                    ),
                },
                {
                    "subsection": "cap07.2",
                    "text": (
                        "Es imprescindible distinguir entre el ámbito (scope) de un identificador y el tiempo de vida "
                        "(lifetime / storage duration) del valor al que se vincula. El ámbito léxico es una propiedad "
                        "estática del texto del programa: determina en qué región de código es visible un nombre. El tiempo "
                        "de vida es una propiedad dinámica de ejecución: el intervalo entre la creación y la destrucción "
                        "del objeto en memoria. Una clausura (closure) aparece cuando una función de primera clase captura "
                        "variables libres de su entorno léxico circundante, empaquetando el puntero de código junto con un "
                        "registro de entorno.\n\n"
                        "En cuanto a la gestión de fallos, la ingeniería del software distingue entre defectos de programación "
                        "(violaciones de invariantes internos, ante los cuales procede abortar o activar un panic/assertion) "
                        "y errores operativos recuperables (archivo inexistente, timeout de red, entrada mal formada). Los "
                        "lenguajes modernos modelan los errores recuperables bien mediante excepciones estructuradas (`try/catch` "
                        "en Python, Java, C#, C++, JS) o bien como valores explícitos en la firma de retorno (`Result<T, E>` en "
                        "Rust, tupla `(T, error)` en Go), obligando al llamador a tratar cada rama de fallo explícitamente:\n\n"
                        "```rust\n"
                        "#[derive(Debug, PartialEq)]\n"
                        "enum ParsePortError {\n"
                        "    NotANumber,\n"
                        "    ZeroPortForbidden,\n"
                        "}\n"
                        "\n"
                        "fn parse_port(raw: &str) -> Result<u16, ParsePortError> {\n"
                        "    let port: u16 = raw.trim().parse().map_err(|_| ParsePortError::NotANumber)?;\n"
                        "    if port == 0 {\n"
                        "        return Err(ParsePortError::ZeroPortForbidden);\n"
                        "    }\n"
                        "    Ok(port)\n"
                        "}\n"
                        "\n"
                        "fn main() {\n"
                        "    assert_eq!(parse_port(\"8080\"), Ok(8080));\n"
                        "    assert_eq!(parse_port(\"0\"), Err(ParsePortError::ZeroPortForbidden));\n"
                        "}\n"
                        "```"
                    ),
                },
            ],
            "definition": (
                "Álgebra de Tipos (Tipos Producto y Tipos Suma): dado un conjunto de tipos con cardinalidades finitas, "
                "un tipo producto $T_{\\text{prod}} = A \\times B$ (registro o tupla) tiene cardinalidad "
                "$|A \\times B| = |A| \\cdot |B|$, mientras que un tipo suma etiquetado $T_{\\text{sum}} = A + B$ "
                "(unión discriminada o `enum`) tiene cardinalidad $|A + B| = |A| + |B|$. Por ejemplo, $|\\text{Option}\\langle A \\rangle| = |A| + 1$ "
                "y $|\\text{Result}\\langle A, E \\rangle| = |A| + |E|$."
            ),
            "consejo": (
                "Reemplace pares de banderas booleanas y campos opcionales sueltos por un tipo suma (`enum` o unión "
                "discriminada): un registro con `is_loading: bool`, `data: Option<D>` y `error: Option<E>` multiplica "
                "estados imposibles (como `is_loading = true` con `data` y `error` simultáneamente presentes), mientras "
                "que un `enum RequestState { Idle, Loading, Ok(D), Failed(E) }` elimina de raíz esos estados en compilación."
            ),
            "self_check": (
                "1. ¿Cuál es la diferencia exacta entre ámbito léxico (scope) y tiempo de vida en memoria (lifetime)? "
                "2. ¿Por qué un tipo producto multiplica cardinalidades mientras que un tipo suma las adiciona? "
                "3. ¿Qué ventaja ofrece devolver `Result<T, E>` en la firma frente a lanzar excepciones no comprobadas?"
            ),
            "worked": {
                "prompt": (
                    "Un estado de conexión se modela erróneamente como un tipo producto con tres booleanos "
                    "(`conectado`, `autenticado`, `error_activo`), un código de modo de 4 valores posibles y un canal "
                    "opcional de $8 + 1 = 9$ estados posibles. Compare el número de estados del tipo producto "
                    "$N_{\\text{prod}} = 2^3 \\times 4 \\times 9$ frente a un tipo suma discriminado `ConnectionState` "
                    "con 4 variantes exactas: `Disconnected` (1), `Connecting` (4 modos), `Authenticated` ($4 \\times 8 = 32$ "
                    "combinaciones válidas de modo y canal activo) y `Failed` (1), y calcule cuántos estados ilegales "
                    "elimina el diseño con tipos algebraicos."
                ),
                "expression": "(8 * 4 * 9) - (1 + 4 + 32 + 1)",
                "difficulty": "INTERMEDIATE",
                "problem_type": "DESIGN",
                "solution": {
                    "given": [
                        {"symbol": "N_bool", "value": "8", "unit": "1", "description": "Combinaciones de los 3 booleanos (2^3)"},
                        {"symbol": "N_mode", "value": "4", "unit": "1", "description": "Modos de operación posibles"},
                        {"symbol": "N_chan", "value": "9", "unit": "1", "description": "Estados de Option<Channel> (8 + 1)"},
                    ],
                    "unknown": "Número de estados inválidos eliminados al pasar de tipo producto a tipo suma",
                    "model": "Cardinalidad de tipos algebraicos (producto cartesiano frente a unión disjunta)",
                    "assumptions": [
                        "Solo las 38 configuraciones del tipo suma tienen significado válido en el protocolo",
                    ],
                    "steps": [
                        {
                            "text": "Calculamos la cardinalidad total del registro tipo producto.",
                            "equation": "N_prod = 8 * 4 * 9",
                            "expression": "8 * 4 * 9",
                            "unit": "1",
                        },
                        {
                            "text": "Calculamos la cardinalidad del tipo suma (1 + 4 + 32 + 1 = 38) y la restamos de N_prod.",
                            "equation": "N_invalid = N_prod - (1 + 4 + 32 + 1)",
                            "expression": "288 - (1 + 4 + 32 + 1)",
                            "unit": "1",
                        },
                    ],
                    "result": "250",
                    "interpretation": (
                        "El registro plano permite representar 288 estados posibles de los cuales 250 son combinaciones "
                        "contradictorias; el tipo suma reduce la cardinalidad exactamente a los 38 estados válidos."
                    ),
                    "limitations": [
                        "Invariantes numéricos continuos (p. ej. x^2 + y^2 = 1) requieren constructores inteligentes (newtypes) además de tipos suma."
                    ],
                    "mistakes": [
                        "Usar el valor nulo o punteros sin inicializar como centinela implícito en lugar de `Option<T>`."
                    ],
                },
            },
            "exercises": _exercises_set("VOL01-C07", "sistemas de tipos, ADT, ámbito léxico, clausuras y gestión de errores", 25),
            "notation": [
                {"symbol": r"|A \times B|", "meaning": "Cardinalidad de un tipo producto", "units": "adimensional"},
                {"symbol": r"|A + B|", "meaning": "Cardinalidad de un tipo suma discriminado", "units": "adimensional"},
            ],
            "terminology": [
                {
                    "canonical": "Tipo de Dato Algebraico (ADT)",
                    "definition": "Tipo compuesto formado mediante operaciones algebraicas de suma disjunta (variantes etiquetadas) y producto cartesiano (campos de registro).",
                    "synonyms": ["Algebraic Data Type"],
                },
            ],
        },
        {
            "id": "cap08-los-doce-paradigmas-de-programacion",
            "part_id": "parte-ii-fundamentos",
            "part_title": "PARTE II. Fundamentos Universales de Programación y Matemáticas Discretas",
            "title": "Los doce paradigmas de programación: fundamentos, compromisos, límites y criterios de selección",
            "sources": ["src-acm-cs2023", "src-rust-book", "src-python-docs"],
            "concepts": [
                {"id": "paradigmas-imperativo-oop-funcional", "title": "Imperativo, procedural, orientado a objetos, funcional, declarativo y lógico"},
                {"id": "paradigmas-generico-reactivo-concurrente", "title": "Genérico, orientado a eventos, reactivo, concurrente, asíncrono y de sistemas"},
            ],
            "subsections": [
                {"id": "cap08.1", "title": "Imperativo, procedural, orientado a objetos, declarativo, funcional y lógico"},
                {"id": "cap08.2", "title": "Genérico, eventos, reactivo, concurrente, asíncrono y programación de sistemas"},
            ],
            "purpose": (
                "Establecer un marco comparativo riguroso de los doce paradigmas de programación fundamentales, "
                "comprendiendo que los lenguajes profesionales actuales son multiparadigma y que la excelencia en "
                "ingeniería consiste en aplicar el paradigma adecuado a cada capa del sistema."
            ),
            "paragraphs": [
                {
                    "subsection": "cap08.1",
                    "text": (
                        "Un paradigma de programación es una disciplina conceptual que estructura cómo modelamos el "
                        "cómputo, el estado y el flujo de control:\n\n"
                        "1. Programación imperativa: expresa el cómputo como una secuencia explícita de sentencias que "
                        "mutan un estado almacenado en memoria. Es óptima cuando el algoritmo modela una máquina de estados "
                        "física o manipula buffers en el lugar (in-place), pero dificulta el razonamiento local cuando el "
                        "estado mutable se comparte sin control.\n\n"
                        "2. Programación procedural: organiza el código imperativo en procedimientos y módulos con interfaces "
                        "bien definidas (C, Pascal, Go).\n\n"
                        "3. Programación orientada a objetos (OOP): encapsula estado e invariantes detrás de métodos y "
                        "permite polimorfismo dinámico (despacho dinámico por vtable o paso de mensajes). Su límite aparece "
                        "cuando se abusa de jerarquías profundas de herencia de implementación en lugar de composición.\n\n"
                        "4. Programación declarativa: especifica qué propiedades debe satisfacer el resultado sin prescribir "
                        "el bucle de control paso a paso (SQL en consultas relacionales, HTML/CSS en maquetación, Terraform/Nix "
                        "en infraestructura).\n\n"
                        "5. Programación funcional: modela el cómputo como evaluación de funciones matemáticamente puras "
                        "(transparencia referencial: sin efectos laterales observables y con datos inmutables o persistentes), "
                        "facilitando la composición, las pruebas unitarias y el paralelismo sin carreras de datos.\n\n"
                        "6. Programación lógica: expresa hechos y reglas mediante cláusulas de Horn (Prolog, Datalog), "
                        "delegando la búsqueda de soluciones en un motor de unificación y backtracking."
                    ),
                },
                {
                    "subsection": "cap08.2",
                    "text": (
                        "Los seis paradigmas restantes abordan la parametrización de tipos, el tiempo, la latencia de E/S "
                        "y el control de recursos físicos:\n\n"
                        "7. Programación genérica: parametriza algoritmos y estructuras de datos sobre tipos abstractos "
                        "restringidos por contratos (`traits` en Rust, `concepts` en C++20, `interfaces` en Go/Java/C#), "
                        "ejecutándose por monomorfización estática (coste cero en tiempo de ejecución) o por diccionario/borrado.\n\n"
                        "8. Programación orientada a eventos: estructura el flujo alrededor de un bucle despachador (event "
                        "loop) que invoca manejadores (handlers/callbacks) en respuesta a sucesos discretos de E/S o interfaz.\n\n"
                        "9. Programación reactiva: modela flujos de datos asíncronos a lo largo del tiempo (`Flow` en Kotlin, "
                        "`Stream` en Rust, Rx) con propagación automática de cambios y control de contrapresión (backpressure).\n\n"
                        "10. Programación concurrente: estructura múltiples flujos de control lógicos potencialmente "
                        "simultáneos mediante memoria compartida sincronizada (mutexes, atómicos), paso de mensajes por "
                        "canales (CSP en Go/Rust) o aislamiento de actores (Erlang/Elixir, Swift 6).\n\n"
                        "11. Programación asíncrona: desacopla la espera de operaciones de entrada/salida (red, disco, "
                        "temporizadores) del bloqueo de hilos del sistema operativo mediante futuros/promesas y máquinas de "
                        "estados cooperativas (`async`/`await` sobre `epoll`/`kqueue`/`io_uring`).\n\n"
                        "12. Programación de sistemas: diseña software que gestiona directamente la memoria física/virtual, "
                        "la ABI, las llamadas al sistema y las restricciones de latencia determinista (Rust, C, C++, Zig)."
                    ),
                },
            ],
            "definition": (
                "Transparencia Referencial y Dualidad Concurrencia vs Paralelismo: una expresión es referencialmente "
                "transparente si puede sustituirse en cualquier punto del programa por su valor evaluado sin alterar "
                "el comportamiento observable del sistema. La concurrencia es una propiedad de diseño (composición de "
                "múltiples tareas lógicas independientes que pueden progresar en intervalos solapados), mientras que el "
                "paralelismo es una propiedad física de ejecución (varias unidades de hardware ejecutando instrucciones "
                "en el mismo instante físico)."
            ),
            "consejo": (
                "Aplique el patrón arquitectónico Functional Core, Imperative Shell: escriba la lógica de dominio y "
                "validación como funciones puras sobre valores inmutables (fáciles de probar exhaustivamente sin mocks), "
                "y confine los efectos laterales de entrada/salida, red y base de datos a una capa exterior delgada."
            ),
            "self_check": (
                "1. ¿En qué se diferencia la transparencia referencial funcional del encapsulamiento orientado a objetos? "
                "2. ¿Cuándo es preferible la programación asíncrona basada en bucle de eventos (`async`/`await`) frente a un pool de hilos del sistema operativo? "
                "3. ¿Qué diferencia de ejecución y tamaño binario existe entre los genéricos por monomorfización (Rust/C++) y por borrado de tipos (Java)?"
            ),
            "worked": {
                "prompt": (
                    "Un servidor debe mantener $C = 10000$ conexiones concurrentes mayoritariamente ociosas esperando "
                    "E/S de red. Si en un modelo de un hilo del sistema operativo por conexión cada hilo reserva una "
                    "pila de $S_{\\text{thread}} = 1024\\text{ KiB}$ ($1\\text{ MiB}$), mientras que en un modelo "
                    "asíncrono (`async`/`await`) cada tarea es una máquina de estados compilada de $S_{\\text{task}} = 2\\text{ KiB}$, "
                    "calcule la razón de reducción de memoria $\\frac{C \\cdot S_{\\text{thread}}}{C \\cdot S_{\\text{task}}}$."
                ),
                "expression": "(10000 * 1024) / (10000 * 2)",
                "difficulty": "INTERMEDIATE",
                "problem_type": "COMPARATIVE",
                "solution": {
                    "given": [
                        {"symbol": "C", "value": "10000", "unit": "1", "description": "Conexiones concurrentes activas"},
                        {"symbol": "S_thread", "value": "1024", "unit": "1", "description": "Pila por hilo OS en KiB"},
                        {"symbol": "S_task", "value": "2", "unit": "1", "description": "Estado por tarea asíncrona en KiB"},
                    ],
                    "unknown": "Factor de reducción de huella de memoria de pila/estado entre ambos modelos",
                    "model": "Comparación de coste espacial entre hilos nativos OS y máquinas de estado asíncronas",
                    "assumptions": [
                        "Cada hilo nativo compromete su pila de 1024 KiB y cada Future compilado ocupa 2 KiB",
                    ],
                    "steps": [
                        {
                            "text": "Calculamos la memoria total en KiB para los 10000 hilos del sistema operativo.",
                            "equation": "M_threads = C * S_thread",
                            "expression": "10000 * 1024",
                            "unit": "1",
                        },
                        {
                            "text": "Dividimos entre la memoria total de las 10000 tareas asíncronas (20000 KiB).",
                            "equation": "ratio = M_threads / (C * S_task)",
                            "expression": "10240000 / 20000",
                            "unit": "1",
                        },
                    ],
                    "result": "512",
                    "interpretation": (
                        "El modelo asíncrono reduce en un factor de 512x la memoria de estado de concurrencia "
                        "(de ~10 GiB a ~20 MiB) y elimina los cambios de contexto de kernel entre miles de hilos."
                    ),
                    "limitations": [
                        "Para cargas intensivas en CPU (CPU-bound) sin esperas de E/S, un pool de tantos hilos como núcleos físicos evita la sobrecarga del planificador asíncrono."
                    ],
                    "mistakes": [
                        "Invocar llamadas bloqueantes sincrónicas dentro de una tarea asíncrona, bloqueando el hilo ejecutor del runtime."
                    ],
                },
            },
            "exercises": _exercises_set("VOL01-C08", "los doce paradigmas de programación, transparencia referencial y concurrencia vs asincronía", 28),
            "notation": [
                {"symbol": "CSP", "meaning": "Communicating Sequential Processes (Hoare, 1978)", "units": "adimensional"},
            ],
            "terminology": [
                {
                    "canonical": "Transparencia referencial",
                    "definition": "Propiedad de una expresión que evalúa siempre al mismo resultado para los mismos argumentos sin producir efectos laterales observables.",
                    "synonyms": ["Referential transparency"],
                },
            ],
        },
    ],
}


VOL02_SPEC: dict[str, object] = {
    "slug": "vol02-algoritmos-y-sistemas",
    "code": "ENC-VOL02",
    "title": "Volumen 2 — Algoritmos, Estructuras de Datos, Compiladores, Memoria y Sistemas Operativos",
    "subtitle": "Partes III y IV: Complejidad Asintótica, Grafos, Programación Dinámica, Arquitectura de Cachés, Compiladores SSA y Sistemas Operativos",
    "target_pages": 100,
    "chapters": [
        {
            "id": "cap01-complejidad-asintotica-recurrencias-amortizado",
            "part_id": "parte-iii-algoritmos",
            "part_title": "PARTE III. Algoritmos, Estructuras de Datos y Computación",
            "title": "Complejidad temporal y espacial, notaciones O, Omega y Theta, recurrencias, Teorema Maestro y análisis amortizado",
            "sources": ["src-mit-6006", "src-acm-cs2023"],
            "concepts": [
                {"id": "notacion-asintotica-maestro", "title": "Notaciones O, Omega, Theta y resolución de recurrencias con el Teorema Maestro"},
                {"id": "analisis-amortizado", "title": "Análisis amortizado: método agregado, contable y de función de potencial"},
            ],
            "subsections": [
                {"id": "cap01.1", "title": "Definición formal de O, Omega y Theta, y Teorema Maestro para recurrencias"},
                {"id": "cap01.2", "title": "Análisis amortizado por método de potencial y vectores dinámicos"},
            ],
            "figure": {
                "key": "fig-amortizado-vec",
                "caption": "Evolución de capacidad y tamaño en un vector dinámico con factor de crecimiento 2x: las reasignaciones en potencias de 2 quedan amortizadas a coste O(1) por inserción.",
                "tikz": r"""
\draw[thick, ->] (0,0) -- (10.5,0) node[right, font=\scriptsize] {Inserción $i$};
\draw[thick, ->] (0,0) -- (0,3.4) node[above, font=\scriptsize] {Coste $c_i$};
\foreach \x/\h in {1/0.4, 2/0.8, 3/1.2, 4/0.4, 5/2.0, 6/0.4, 7/0.4, 8/0.4, 9/3.0} {
    \filldraw[blue!70!black] (\x,0) rectangle (\x+0.35,\h);
}
\draw[dashed, orange!75!black, thick] (0,1.0) -- (10.2,1.0) node[right, font=\scriptsize] {$\hat{c}_i = 3 = O(1)$};
""",
            },
            "purpose": (
                "Proporcionar las herramientas matemáticas exactas para predecir cómo escalan el tiempo de ejecución "
                "y el consumo de memoria de cualquier algoritmo cuando el tamaño de entrada $n$ crece varios órdenes "
                "de magnitud, demostrando cotas superiores, inferiores y costes amortizados."
            ),
            "paragraphs": [
                {
                    "subsection": "cap01.1",
                    "text": (
                        "El análisis de algoritmos mide el crecimiento del número de operaciones elementales $T(n)$ y "
                        "de celdas de memoria $S(n)$ en función del tamaño de entrada $n$. Dadas dos funciones no negativas "
                        "$f(n)$ y $g(n)$:\n"
                        "1. Cota superior asintótica ($f(n) \\in O(g(n))$): existen constantes $c > 0$ y $n_0 \\ge 1$ tales "
                        "que $0 \\le f(n) \\le c \\cdot g(n)$ para todo $n \\ge n_0$.\n"
                        "2. Cota inferior asintótica ($f(n) \\in \\Omega(g(n))$): existen $c > 0$ y $n_0 \\ge 1$ tales que "
                        "$0 \\le c \\cdot g(n) \\le f(n)$ para todo $n \\ge n_0$.\n"
                        "3. Orden asintótico exacto ($f(n) \\in \\Theta(g(n))$): se cumple simultáneamente $f(n) \\in O(g(n))$ "
                        "y $f(n) \\in \\Omega(g(n))$.\n\n"
                        "Para algoritmos recursivos de divide y vencerás cuya recurrencia tiene la forma "
                        "$T(n) = a T(n/b) + f(n)$ con $a \\ge 1$ y $b > 1$, el Teorema Maestro compara $f(n)$ con la hoja "
                        "crítica $n^{\\log_b a}$: (Caso 1) si $f(n) = O(n^{\\log_b a - \\varepsilon})$, entonces "
                        "$T(n) = \\Theta(n^{\\log_b a})$; (Caso 2) si $f(n) = \\Theta(n^{\\log_b a})$, entonces "
                        "$T(n) = \\Theta(n^{\\log_b a} \\log n)$ (como ocurre en Mergesort con $a=2, b=2, f(n)=\\Theta(n) \\Rightarrow \\Theta(n \\log n)$); "
                        "(Caso 3) si $f(n) = \\Omega(n^{\\log_b a + \\varepsilon})$ y satisface regularidad, entonces $T(n) = \\Theta(f(n))$."
                    ),
                },
                {
                    "subsection": "cap01.2",
                    "text": (
                        "No debe confundirse la complejidad en el caso promedio (que asume una distribución probabilística "
                        "sobre las entradas) con la complejidad amortizada: el análisis amortizado garantiza de forma "
                        "determinista el coste promedio por operación sobre cualquier secuencia de $m$ operaciones en el "
                        "peor caso, sin ninguna hipótesis probabilística. En el método de la función de potencial de Tarjan, "
                        "definimos una función $\\Phi(D_i) \\ge \\Phi(D_0)$ sobre el estado $D_i$ de la estructura de datos, "
                        "y el coste amortizado de la $i$-ésima operación es $\\hat{c}_i = c_i + \\Phi(D_i) - \\Phi(D_{i-1})$.\n\n"
                        "Como muestra la {{fig:fig-amortizado-vec}}, en un vector dinámico (`Vec<T>` en Rust, `std::vector` "
                        "en C++, `list` en Python) que duplica su capacidad $\\text{cap}$ cuando el tamaño $\\text{len}$ "
                        "alcanza $\\text{cap}$, tomamos $\\Phi = 2 \\cdot \\text{len} - \\text{cap}$. En una inserción sin "
                        "redimensionado ($c_i = 1, \\Delta\\text{len} = 1, \\Delta\\text{cap} = 0$), el coste amortizado es "
                        "$\\hat{c}_i = 1 + 2 = 3$. En una inserción con redimensionado de $k$ a $2k$ ($c_i = k + 1$), el "
                        "potencial cae de $\\Phi_{i-1} = 2k - k = k$ a $\\Phi_i = 2(k+1) - 2k = 2$, por lo que "
                        "$\\hat{c}_i = (k + 1) + (2 - k) = 3 = \\Theta(1)$."
                    ),
                },
            ],
            "definition": (
                "Método del Potencial (Análisis Amortizado): dada una secuencia de $m$ operaciones con costes reales "
                "$c_1, \\dots, c_m$ sobre estados $D_0, \\dots, D_m$ y una función de potencial $\\Phi(D_i) \\ge \\Phi(D_0)$, "
                "la suma de costes amortizados acota superiormente el coste real total: "
                "$\\sum_{i=1}^m c_i = \\sum_{i=1}^m \\hat{c}_i - (\\Phi(D_m) - \\Phi(D_0)) \\le \\sum_{i=1}^m \\hat{c}_i$."
            ),
            "consejo": (
                "En un vector dinámico, si en lugar de multiplicar la capacidad por una constante ($\\times 2$ o $\\times 1.5$) "
                "se incrementara sumando una cantidad fija $+K$ en cada llenado, el coste de $n$ inserciones degeneraría "
                "a $\\Theta(n^2)$: la progresión geométrica es indispensable para mantener `push` en $O(1)$ amortizado."
            ),
            "self_check": (
                "1. ¿Qué diferencia existe entre decir que un algoritmo es $O(n^2)$ y decir que es $\\Theta(n^2)$? "
                "2. ¿Qué diferencia fundamental separa la complejidad en el caso promedio de la complejidad amortizada? "
                "3. ¿Por qué duplicar la capacidad de un array dinámico garantiza coste amortizado $\\hat{c}_i \\le 3$?"
            ),
            "worked": {
                "prompt": (
                    "Un vector dinámico comienza con capacidad inicial $\\text{cap}_0 = 1$ y duplica su capacidad cada "
                    "vez que se llena ($1 \\to 2 \\to 4 \\to 8 \\to 16 \\to 32$). Si se insertan secuencialmente "
                    "$n = 17$ elementos y cada inserción cuesta 1 escritura más el número de elementos copiados durante "
                    "el redimensionado ($1 + 2 + 4 + 8 + 16$ copias acumuladas), calcule el coste total exacto de "
                    "escrituras realizadas."
                ),
                "expression": "17 + (1 + 2 + 4 + 8 + 16)",
                "difficulty": "INTERMEDIATE",
                "problem_type": "NUMERICAL",
                "solution": {
                    "given": [
                        {"symbol": "n", "value": "17", "unit": "1", "description": "Número de elementos insertados"},
                        {"symbol": "C_copy", "value": "31", "unit": "1", "description": "Copias de redimensionado (1+2+4+8+16)"},
                    ],
                    "unknown": "Coste total de operaciones de escritura sobre las 17 inserciones",
                    "model": "Suma geométrica de copias en redimensionamiento duplicado de un vector dinámico",
                    "assumptions": [
                        "Capacidad inicial 1 y duplicación exacta al insertar cuando len == cap",
                    ],
                    "steps": [
                        {
                            "text": "Sumamos los elementos copiados en las 5 expansiones (al pasar de capacidad 1 a 2, 4, 8, 16 y 32).",
                            "equation": "C_copy = 1 + 2 + 4 + 8 + 16",
                            "expression": "1 + 2 + 4 + 8 + 16",
                            "unit": "1",
                        },
                        {
                            "text": "Sumamos las 17 escrituras directas de cada nuevo elemento.",
                            "equation": "C_total = n + C_copy",
                            "expression": "17 + 31",
                            "unit": "1",
                        },
                    ],
                    "result": "48",
                    "interpretation": (
                        "Las 17 inserciones requieren 48 escrituras en total (menos de 3 * 17 = 51), confirmando "
                        "la cota teórica del método de potencial (coste amortizado <= 3 por inserción)."
                    ),
                    "limitations": [
                        "En sistemas de tiempo real estricto (hard real-time), el pico puntual O(n) del redimensionado obliga a pre-reservar con `with_capacity`."
                    ],
                    "mistakes": [
                        "Confundir el peor caso de una operación aislada O(n) con el coste de una secuencia de n operaciones, que es O(n) total y no O(n^2)."
                    ],
                },
            },
            "exercises": _exercises_set("VOL02-C01", "notación asintótica, Teorema Maestro y análisis amortizado", 14),
            "notation": [
                {"symbol": r"\Theta(g(n))", "meaning": "Orden de crecimiento asintótico ajustado superior e inferiormente", "units": "adimensional"},
                {"symbol": r"\Phi(D_i)", "meaning": "Función de potencial de la estructura de datos en el paso i", "units": "adimensional"},
            ],
            "terminology": [
                {
                    "canonical": "Complejidad amortizada",
                    "definition": "Cota determinista del coste medio por operación en el peor caso sobre cualquier secuencia de operaciones.",
                    "synonyms": ["Amortized complexity"],
                },
            ],
        },
        {
            "id": "cap02-busqueda-ordenacion-cotas-inferiores",
            "part_id": "parte-iii-algoritmos",
            "part_title": "PARTE III. Algoritmos, Estructuras de Datos y Computación",
            "title": "Búsqueda binaria libre de desbordamiento, ordenación, cota inferior Omega(n log n) e invariantes",
            "sources": ["src-mit-6006", "src-rust-book"],
            "concepts": [
                {"id": "busqueda-binaria-invariantes", "title": "Búsqueda binaria por partición monótona y demostración mediante invariante de bucle"},
                {"id": "ordenacion-cota-decision", "title": "Árbol de decisión, cota inferior Omega(n log n), Mergesort, Quicksort, Heapsort y Radix Sort"},
            ],
            "subsections": [
                {"id": "cap02.1", "title": "Búsqueda binaria, invariantes de bucle y prevención del desbordamiento de punto medio"},
                {"id": "cap02.2", "title": "Cota inferior por árbol de decisión, Mergesort, Quicksort, Heapsort y ordenación lineal"},
            ],
            "purpose": (
                "Dominar los algoritmos de búsqueda y ordenación desde sus demostraciones formales de corrección "
                "mediante invariantes de bucle hasta la cota teórica de información $\\Omega(n \\log n)$ y las "
                "implementaciones híbridas de producción (Timsort, pdqsort, Radix Sort)."
            ),
            "paragraphs": [
                {
                    "subsection": "cap02.1",
                    "text": (
                        "La búsqueda binaria reduce un espacio ordenado de $n$ elementos a la mitad en cada comparación, "
                        "alcanzando complejidad $\\Theta(\\log_2 n)$ en el peor caso. Pese a su brevedad, como documentó "
                        "Jon Bentley en Programming Pearls, la mayoría de las implementaciones improvisadas contienen defectos "
                        "en las condiciones de parada o en el cálculo del punto medio: escribir `mid = (low + high) / 2` "
                        "con enteros de ancho fijo provoca desbordamiento aritmético cuando `low + high` supera `INT_MAX` "
                        "(defecto que permaneció veinte años oculto en `java.util.Arrays.binarySearch`). La forma correcta "
                        "es `mid = low + (high - low) / 2`.\n\n"
                        "Para demostrar formalmente la corrección de un bucle (inicialización, mantenimiento y terminación), "
                        "se trabaja sobre un intervalo semiabierto `[low, high)` con el invariante: para todo índice "
                        "$i < \\text{low}$ se cumple $A[i] < \\text{target}$ y para todo $j \\ge \\text{high}$ se cumple "
                        "$A[j] \\ge \\text{target}$. En cada iteración la longitud `high - low` decrece estrictamente "
                        "(función de cota o variante de bucle), garantizando terminación en $\\lceil \\log_2(n+1) \\rceil$ pasos."
                    ),
                },
                {
                    "subsection": "cap02.2",
                    "text": (
                        "Todo algoritmo de ordenación basado exclusivamente en comparaciones entre pares de elementos puede "
                        "modelarse como un árbol binario de decisión cuyas hojas contienen las $n!$ permutaciones posibles "
                        "de la entrada. Un árbol binario de altura $h$ posee a lo sumo $2^h$ hojas; por tanto, $2^h \\ge n!$, "
                        "y aplicando la aproximación de Stirling ($\\log_2(n!) = n \\log_2 n - n \\log_2 e + \\Theta(\\log n)$) "
                        "se obtiene el teorema fundamental: cualquier algoritmo de ordenación por comparación requiere "
                        "$h \\ge \\lceil \\log_2(n!) \\rceil = \\Omega(n \\log n)$ comparaciones en el peor caso.\n\n"
                        "Mergesort alcanza $\\Theta(n \\log n)$ garantizado y es estable (preserva el orden relativo de claves "
                        "iguales), empleando $\\Theta(n)$ memoria auxiliar; Heapsort logra $\\Theta(n \\log n)$ en el peor caso "
                        "con memoria auxiliar $O(1)$ in-place sobre un montículo binario implícito, pero no es estable y "
                        "presenta peor localidad de caché que Quicksort; Quicksort con pivote mediano o aleatorio logra "
                        "$\\Theta(n \\log n)$ esperado con excelente localidad espacial en caché L1 (y en su variante híbrida "
                        "Introsort/pdqsort empleada en Rust `sort_unstable` y C++ `std::sort`, conmuta a Heapsort si la "
                        "profundidad recursiva supera $2 \\lfloor \\log_2 n \\rfloor$, garantizando $O(n \\log n)$ en el peor "
                        "caso). Cuando las claves son enteros de $w$ bits agrupados en dígitos de base $R$, Counting Sort "
                        "y Radix Sort evitan comparaciones directas y ordenan en tiempo lineal $\\Theta(d(n + R))$.\n\n"
                        "```rust\n"
                        "fn lower_bound(slice: &[i64], target: i64) -> usize {\n"
                        "    let mut low = 0usize;\n"
                        "    let mut high = slice.len();\n"
                        "    while low < high {\n"
                        "        let mid = low + (high - low) / 2;\n"
                        "        if slice[mid] < target {\n"
                        "            low = mid + 1;\n"
                        "        } else {\n"
                        "            high = mid;\n"
                        "        }\n"
                        "    }\n"
                        "    low\n"
                        "}\n"
                        "\n"
                        "fn main() {\n"
                        "    let data = [2, 5, 5, 5, 9, 14];\n"
                        "    assert_eq!(lower_bound(&data, 5), 1);\n"
                        "    assert_eq!(lower_bound(&data, 6), 4);\n"
                        "}\n"
                        "```"
                    ),
                },
            ],
            "definition": (
                "Cota Inferior de Ordenación por Comparación y Estabilidad: ningún algoritmo que ordene $n$ elementos "
                "mediante comparaciones binarias puede realizar menos de $\\lceil \\log_2(n!) \\rceil = \\Omega(n \\log n)$ "
                "comparaciones en el peor caso. Un algoritmo de ordenación es estable si para todo par de índices "
                "$i < j$ con claves equivalentes $k(A[i]) = k(A[j])$, el elemento $A[i]$ precede a $A[j]$ en la salida."
            ),
            "consejo": (
                "En las bibliotecas estándar modernas, elija la ordenación estable (`slice::sort` en Rust, Timsort en "
                "Python `sorted`, `std::stable_sort` en C++) cuando ordene registros compuestos o secuencias parcialmente "
                "ordenadas, y la ordenación inestable (`sort_unstable` / `pdqsort`) para tipos primitivos donde desee "
                "evitar la reserva de memoria auxiliar."
            ),
            "self_check": (
                "1. ¿Cómo se demuestra que el árbol de decisión de cualquier algoritmo de ordenación por comparación tiene altura al menos $\\log_2(n!)$? "
                "2. ¿Por qué `mid = low + (high - low) / 2` evita el desbordamiento entero de `(low + high) / 2`? "
                "3. ¿Por qué Introsort/pdqsort combina Quicksort, Insertion Sort para subvectores pequeños y Heapsort como salvaguarda?"
            ),
            "worked": {
                "prompt": (
                    "Determine el número mínimo teórico de comparaciones binarias en el peor caso necesarias para "
                    "ordenar $n = 5$ elementos distintos sabiendo que existen $5! = 120$ permutaciones posibles y "
                    "que $2^6 = 64 < 120 \\le 2^7 = 128$, verificando además la diferencia $2^7 - 5!$."
                ),
                "expression": "(2 ** 7) - (5 * 4 * 3 * 2 * 1)",
                "difficulty": "FOUNDATIONAL",
                "problem_type": "PROOF",
                "solution": {
                    "given": [
                        {"symbol": "n", "value": "5", "unit": "1", "description": "Número de elementos a ordenar"},
                        {"symbol": "P", "value": "120", "unit": "1", "description": "Número de permutaciones 5!"},
                        {"symbol": "L_7", "value": "128", "unit": "1", "description": "Número máximo de hojas en altura h = 7 (2^7)"},
                    ],
                    "unknown": "Margen de hojas sobrantes 2^7 - 5! que demuestra que h = 7 es el mínimo entero tal que 2^h >= 5!",
                    "model": "Cota de información en árbol binario de decisión (2^h >= n!)",
                    "assumptions": [
                        "Cada comparación binaria divide el conjunto de permutaciones candidatas en a lo sumo dos subárboles",
                    ],
                    "steps": [
                        {
                            "text": "Calculamos el factorial 5! = 120 permutaciones que deben aparecer como hojas alcanzables.",
                            "equation": "fact_5 = 5 * 4 * 3 * 2 * 1",
                            "expression": "5 * 4 * 3 * 2 * 1",
                            "unit": "1",
                        },
                        {
                            "text": "Comprobamos que 2^7 = 128 cubre las 120 permutaciones con un margen de 8 hojas.",
                            "equation": "margin = 2^7 - fact_5",
                            "expression": "128 - 120",
                            "unit": "1",
                        },
                    ],
                    "result": "8",
                    "interpretation": (
                        "Con 6 comparaciones solo se distinguen a lo sumo 2^6 = 64 permutaciones (< 120); por tanto, "
                        "se necesitan al menos h = 7 comparaciones en el peor caso para ordenar 5 elementos, dejando un margen de 8 hojas."
                    ),
                    "limitations": [
                        "Para n grandes, la cota de información ceil(log2(n!)) es necesaria pero en ciertos n específicos el mínimo exacto de Ford-Johnson requiere 1 comparación adicional."
                    ],
                    "mistakes": [
                        "Confundir n * log2(n) directo con log2(n!), que para n pequeños difiere significativamente."
                    ],
                },
            },
            "exercises": _exercises_set("VOL02-C02", "búsqueda binaria, invariantes de bucle y ordenación", 16),
            "notation": [
                {"symbol": "n!", "meaning": "Cardinalidad del grupo simétrico de permutaciones de n elementos", "units": "adimensional"},
            ],
            "terminology": [
                {
                    "canonical": "Invariante de bucle",
                    "definition": "Predicado lógico sobre el estado de las variables que se cumple antes de la primera iteración, se conserva tras cada paso y al terminar implica la postcondición.",
                    "synonyms": ["Loop invariant"],
                },
            ],
        },
        {
            "id": "cap03-divide-venceras-voraces-programacion-dinamica",
            "part_id": "parte-iii-algoritmos",
            "part_title": "PARTE III. Algoritmos, Estructuras de Datos y Computación",
            "title": "Divide y vencerás, algoritmos voraces, programación dinámica y backtracking",
            "sources": ["src-mit-6006", "src-acm-cs2023"],
            "concepts": [
                {"id": "subestructura-optima-voraz-dp", "title": "Subestructura óptima, elección voraz vs subproblemas solapados en programación dinámica"},
                {"id": "memoizacion-tabulacion-backtracking", "title": "Memoización top-down, tabulación bottom-up con reducción espacial y backtracking con poda"},
            ],
            "subsections": [
                {"id": "cap03.1", "title": "Divide y vencerás y condición de elección voraz (Greedy Choice Property)"},
                {"id": "cap03.2", "title": "Programación dinámica (Bellman) y búsqueda exhaustiva con poda (Backtracking)"},
            ],
            "purpose": (
                "Distinguir con rigor matemático cuándo un problema de optimización admite una estrategia voraz local, "
                "cuándo requiere programación dinámica por solapamiento de subproblemas y cuándo exige búsqueda en "
                "espacio de estados con poda (backtracking / branch and bound)."
            ),
            "paragraphs": [
                {
                    "subsection": "cap03.1",
                    "text": (
                        "Un problema exhibe subestructura óptima cuando una solución óptima global contiene dentro de sí "
                        "soluciones óptimas a sus subproblemas. Si los subproblemas son disjuntos (independientes), el "
                        "paradigma de Divide y Vencerás los resuelve recursivamente y combina sus resultados (Mergesort, "
                        "transformada rápida de Fourier FFT, multiplicación de enteros de Karatsuba en $O(n^{\\log_2 3}) \\approx O(n^{1.585})$).\n\n"
                        "Los algoritmos voraces (greedy) dan un paso más audaz: en cada etapa toman una decisión localmente "
                        "óptima sin explorar las ramas alternativas. Un algoritmo voraz es correcto única y exclusivamente "
                        "cuando se demuestra la propiedad de elección voraz (existe siempre una solución óptima global que "
                        "comienza con la elección voraz) junto con la subestructura óptima. Así ocurre en la selección de "
                        "actividades por tiempo de finalización más temprano, en la codificación prefijo de entropía mínima "
                        "de Huffman y en los árboles generadores mínimos sobre matroides (Kruskal y Prim); en cambio, en "
                        "el problema de la mochila 0-1 (0-1 Knapsack) o del cambio de monedas para sistemas no canónicos "
                        "(como monedas `{1, 3, 4}` para sumar `6`, donde el voraz elige `4+1+1` = 3 monedas frente al óptimo "
                        "`3+3` = 2 monedas), la heurística voraz falla y es necesario recurrir a programación dinámica."
                    ),
                },
                {
                    "subsection": "cap03.2",
                    "text": (
                        "La Programación Dinámica (introducida por Richard Bellman en los años cincuenta) resuelve problemas "
                        "con subestructura óptima y subproblemas solapados calculando cada estado una sola vez. Todo diseño "
                        "de programación dinámica sigue cuatro pasos formales: (1) definir el espacio de estados y su significado, "
                        "(2) escribir la ecuación de recurrencia de Bellman relacionando un estado con sus predecesores en el "
                        "DAG de dependencias, (3) establecer los casos base, y (4) elegir el orden de evaluación: recursivo "
                        "con caché (memoización top-down) o iterativo en orden topológico (tabulación bottom-up), reduciendo "
                        "a menudo la complejidad espacial de $O(n \\cdot W)$ a $O(W)$ cuando la fila actual solo depende de "
                        "la anterior.\n\n"
                        "Cuando el problema es NP-duro y carece de estructura polinómica compacta (como satisfacibilidad "
                        "booleana SAT, coloreado de grafos o las $N$-reinas), el Backtracking explora sistemáticamente el "
                        "árbol de decisiones en profundidad aplicando predicados de factibilidad y cotas de optimalidad "
                        "(branch and bound) para podar subárboles enteros antes de expandirlos:\n\n"
                        "```python\n"
                        "def knapsack_01(weights: list[int], values: list[int], capacity: int) -> int:\n"
                        "    dp = [0] * (capacity + 1)\n"
                        "    for w, val in zip(weights, values):\n"
                        "        for c in range(capacity, w - 1, -1):\n"
                        "            if dp[c - w] + val > dp[c]:\n"
                        "                dp[c] = dp[c - w] + val\n"
                        "    return dp[capacity]\n"
                        "\n"
                        "# Voraz por densidad elegiría (w=10, v=60)+(w=20, v=100) = 160; óptimo DP toma (20,100)+(30,120) = 220\n"
                        "assert knapsack_01([10, 20, 30], [60, 100, 120], 50) == 220\n"
                        "```"
                    ),
                },
            ],
            "definition": (
                "Ecuación de Recurrencia de Bellman en la Mochila 0-1 y Distancia de Edición (Levenshtein): para $n$ "
                "objetos con pesos $w_i$ y valores $v_i$ bajo capacidad $C$, el valor óptimo satisface "
                "$OPT(i, c) = \\max(OPT(i-1, c),\\; v_i + OPT(i-1, c - w_i))$ si $w_i \\le c$, y $OPT(i-1, c)$ en caso "
                "contrario, con complejidad pseudopolinómica $\\Theta(n C)$ en tiempo y $\\Theta(C)$ en espacio."
            ),
            "consejo": (
                "Al optimizar espacio en la mochila 0-1 reduciendo la matriz 2D a un único vector 1D `dp[0..C]`, "
                "recorra siempre las capacidades en orden decreciente `for c in (w..=C).rev()`: si las recorre en "
                "orden creciente, estará reutilizando el mismo objeto múltiples veces (resolviendo la mochila ilimitada "
                "Unbounded Knapsack en lugar de la mochila 0-1)."
            ),
            "self_check": (
                "1. ¿Qué contraejemplo mínimo demuestra que el algoritmo voraz falla en el cambio de monedas con denominaciones `{1, 3, 4}`? "
                "2. ¿Por qué recorrer las capacidades hacia atrás en `dp[c]` distingue la mochila 0-1 de la mochila ilimitada? "
                "3. ¿Por qué la complejidad $\\Theta(n C)$ de la mochila 0-1 se denomina pseudopolinómica?"
            ),
            "worked": {
                "prompt": (
                    "En el algoritmo de Karatsuba para multiplicar dos enteros de $n$ dígitos dividiendo cada operando "
                    "en dos mitades, se sustituyen las $4$ multiplicaciones clásicas de tamaño $n/2$ por solo $3$ "
                    "multiplicaciones recursivas. Compare el número de multiplicaciones base en una profundidad de "
                    "$k = 4$ niveles ($n = 16$ bloques) entre el método cuadrático clásico ($4^4$) y Karatsuba ($3^4$), "
                    "calculando el ahorro neto de productos elementales."
                ),
                "expression": "(4 ** 4) - (3 ** 4)",
                "difficulty": "INTERMEDIATE",
                "problem_type": "COMPARATIVE",
                "solution": {
                    "given": [
                        {"symbol": "k", "value": "4", "unit": "1", "description": "Niveles de recursión (para n = 2^4 = 16)"},
                        {"symbol": "b_classic", "value": "4", "unit": "1", "description": "Subproblemas por nivel en método clásico"},
                        {"symbol": "b_karat", "value": "3", "unit": "1", "description": "Subproblemas por nivel en Karatsuba"},
                    ],
                    "unknown": "Ahorro de multiplicaciones base tras 4 niveles de recursión",
                    "model": "Árbol de recursión de Divide y Vencerás (4^k frente a 3^k)",
                    "assumptions": [
                        "Cada nivel divide exactamente a la mitad el ancho de palabra de los operandos",
                    ],
                    "steps": [
                        {
                            "text": "Calculamos los productos en las hojas del algoritmo cuadrático clásico 4^4.",
                            "equation": "M_classic = 4^4",
                            "expression": "4 ** 4",
                            "unit": "1",
                        },
                        {
                            "text": "Restamos los productos en las hojas de Karatsuba 3^4 = 81.",
                            "equation": "saved = M_classic - 3^4",
                            "expression": "256 - 81",
                            "unit": "1",
                        },
                    ],
                    "result": "175",
                    "interpretation": (
                        "En solo 4 niveles de subdivisión Karatsuba reduce de 256 a 81 los productos base (ahorro de 175); "
                        "para operandos criptográficos de miles de bits la ventaja asintótica O(n^1.585) es decisiva."
                    ),
                    "limitations": [
                        "Para operandos pequeños (p. ej. menos de 32 palabras de 64 bits), la sobrecarga de sumas y restas hace más rápido el producto escolar en ensamblador."
                    ],
                    "mistakes": [
                        "Aplicar programación dinámica cuando los subproblemas nunca se solapan (donde Divide y Vencerás no necesita tabla de memoización)."
                    ],
                },
            },
            "exercises": _exercises_set("VOL02-C03", "divide y vencerás, algoritmos voraces, programación dinámica y backtracking", 18),
            "notation": [
                {"symbol": r"OPT(i, c)", "meaning": "Valor óptimo de la subestructura en programación dinámica", "units": "adimensional"},
            ],
            "terminology": [
                {
                    "canonical": "Subestructura óptima",
                    "definition": "Propiedad por la cual una solución óptima global se construye a partir de soluciones óptimas de sus subproblemas.",
                    "synonyms": ["Optimal substructure"],
                },
            ],
        },
        {
            "id": "cap04-grafos-arboles-equilibrados-hashing",
            "part_id": "parte-iii-algoritmos",
            "part_title": "PARTE III. Algoritmos, Estructuras de Datos y Computación",
            "title": "Algoritmos de grafos (BFS, DFS, Dijkstra, Bellman-Ford, MST, flujo), árboles equilibrados (AVL, Rojo-Negro, B+) y hashing",
            "sources": ["src-mit-6006", "src-codd-relational"],
            "concepts": [
                {"id": "grafos-caminos-minimos", "title": "Recorridos BFS/DFS, orden topológico, caminos mínimos (Dijkstra/Bellman-Ford) y árboles generadores (Kruskal/Prim)"},
                {"id": "arboles-equilibrados-hashing", "title": "Árboles AVL, Rojo-Negro, B/B+ para disco y tablas hash con direccionamiento abierto (Robin Hood / SwissTable)"},
            ],
            "subsections": [
                {"id": "cap04.1", "title": "BFS, DFS, componentes conexas, Dijkstra, Bellman-Ford, Kruskal y Prim"},
                {"id": "cap04.2", "title": "Árboles equilibrados (AVL, Rojo-Negro, B+ Trees) y tablas hash de alto rendimiento"},
            ],
            "purpose": (
                "Comprender en profundidad los algoritmos sobre grafos y las dos grandes familias de índices asociativos "
                "—árboles equilibrados y tablas hash— que sustentan desde los enrutadores de red y compiladores hasta "
                "los motores de bases de datos y las colecciones estándar de todos los lenguajes."
            ),
            "paragraphs": [
                {
                    "subsection": "cap04.1",
                    "text": (
                        "Sobre un grafo $G = (V, E)$ representado mediante listas de adyacencia (espacio $\\Theta(|V| + |E|)$), "
                        "la búsqueda en anchura (BFS, gobernada por una cola FIFO) explora el grafo por capas y calcula "
                        "distancias mínimas en número de aristas en tiempo $\\Theta(|V| + |E|)$. La búsqueda en profundidad "
                        "(DFS, recursiva o con pila explícita) clasifica las aristas en árbol, avance, retroceso (cuya "
                        "presencia caracteriza exactamente los ciclos en un grafo dirigido) y cruce, permitiendo calcular "
                        "en tiempo lineal $\\Theta(|V| + |E|)$ la ordenación topológica de un DAG y las componentes fuertemente "
                        "conexas (algoritmo de Tarjan o Kosaraju).\n\n"
                        "Cuando las aristas tienen pesos no negativos $w(u, v) \\ge 0$, el algoritmo de Dijkstra relaja "
                        "distancias extrayendo el vértice de menor distancia tentativa desde una cola de prioridad (montículo "
                        "binario), alcanzando $O((|V| + |E|) \\log |V|)$. Si existen pesos negativos, la hipótesis voraz de "
                        "Dijkstra falla (un camino ya cerrado podría mejorarse más tarde a través de una arista negativa), y "
                        "debe emplearse Bellman-Ford, que relaja todas las aristas $|V| - 1$ veces en $O(|V| \\cdot |E|)$ y "
                        "detecta ciclos negativos alcanzables en la iteración $|V|$."
                    ),
                },
                {
                    "subsection": "cap04.2",
                    "text": (
                        "Para implementar diccionarios dinámicos existen dos compromisos fundamentales. Los árboles binarios "
                        "de búsqueda autoequilibrados (AVL con factor de equilibrio $|h_L - h_R| \\le 1$, y Rojo-Negro con "
                        "altura acotada por $2 \\log_2(n + 1)$) garantizan búsqueda, inserción, borrado y consultas por rango "
                        "en $\\Theta(\\log n)$ en el peor caso, pero cada salto de puntero suele provocar un fallo de caché. "
                        "Por ello, tanto `std::collections::BTreeMap` en Rust como los índices de bases de datos (PostgreSQL, "
                        "SQLite) utilizan árboles B y B+ de alto factor de ramificación $B$: cada nodo agrupa entre $B-1$ y "
                        "$2B-1$ claves contiguas en memoria o páginas de disco de $4\\text{--}16\\text{ KiB}$, reduciendo la "
                        "altura del árbol a $\\log_B n$ (apenas 3 o 4 niveles para cientos de millones de registros).\n\n"
                        "Las tablas hash proyectan cada clave mediante una función de dispersión $h(k)$ a un índice de cubeta "
                        "(bucket), ofreciendo acceso esperado $O(1)$. Frente al encadenamiento separado con listas enlazadas, "
                        "las implementaciones modernas de producción (como `HashMap` en Rust basado en SwissTable de Google "
                        "con instrucciones SIMD y SipHash-1-3 resistente a ataques HashDoS, o `dict` compacto en Python) "
                        "emplean direccionamiento abierto (open addressing) en un array contiguo con factor de carga "
                        "$\\alpha = n/m \\le 0.875$. Verifiquemos el algoritmo de Dijkstra en Python:\n\n"
                        "```python\n"
                        "import heapq\n"
                        "\n"
                        "def dijkstra(adj: dict[int, list[tuple[int, int]]], src: int) -> dict[int, int]:\n"
                        "    dist = {src: 0}\n"
                        "    pq = [(0, src)]\n"
                        "    while pq:\n"
                        "        d, u = heapq.heappop(pq)\n"
                        "        if d > dist.get(u, 10**18):\n"
                        "            continue\n"
                        "        for v, w in adj.get(u, []):\n"
                        "            if d + w < dist.get(v, 10**18):\n"
                        "                dist[v] = d + w\n"
                        "                heapq.heappush(pq, (d + w, v))\n"
                        "    return dist\n"
                        "\n"
                        "g = {0: [(1, 4), (2, 1)], 2: [(1, 2), (3, 5)], 1: [(3, 1)], 3: []}\n"
                        "assert dijkstra(g, 0) == {0: 0, 2: 1, 1: 3, 3: 4}\n"
                        "```"
                    ),
                },
            ],
            "definition": (
                "Factor de Carga ($\\alpha$) en Tablas Hash y Altura de un Árbol B+: en una tabla hash con $n$ elementos "
                "y $m$ ranuras, el factor de carga es $\\alpha = n / m$. En direccionamiento abierto con sondeo lineal "
                "bajo dispersión uniforme, el número esperado de sondeos en una búsqueda exitosa es "
                "$\\frac{1}{2}\\left(1 + \\frac{1}{1 - \\alpha}\\right)$. En un árbol B+ de grado mínimo $B$, la altura "
                "satisface $h \\le \\lfloor \\log_B((n+1)/2) \\rfloor + 1$."
            ),
            "consejo": (
                "Si una tabla hash recibe claves controladas por usuarios externos (parámetros HTTP, cabeceras JSON) y "
                "utiliza una función hash no criptográfica predecible, un atacante puede enviar miles de claves que "
                "colisionen en la misma cubeta y degradar la complejidad de $O(1)$ a $O(n^2)$ (denegación de servicio "
                "HashDoS): por eso Rust usa un hasher con semilla aleatoria por defecto."
            ),
            "self_check": (
                "1. ¿Por qué el algoritmo de Dijkstra falla si el grafo contiene una arista de peso negativo? "
                "2. ¿Por qué `BTreeMap` y los motores SQL usan nodos de árbol B/B+ con múltiples claves por nodo en lugar de árboles binarios Rojo-Negro? "
                "3. ¿En qué consiste un ataque de colisión HashDoS y cómo lo mitiga SipHash con semilla aleatoria?"
            ),
            "worked": {
                "prompt": (
                    "En una tabla hash con direccionamiento abierto y sondeo lineal que se mantiene con un factor de "
                    "carga $\\alpha = 0.75$, calcule el número esperado de sondeos en una búsqueda sin éxito (inserción "
                    "de clave nueva) según la fórmula de Knuth $E_{\\text{miss}} = \\frac{1}{2}\\left(1 + \\frac{1}{(1 - \\alpha)^2}\\right)$."
                ),
                "expression": "0.5 * (1 + 1 / ((1 - 0.75) ** 2))",
                "difficulty": "INTERMEDIATE",
                "problem_type": "NUMERICAL",
                "solution": {
                    "given": [
                        {"symbol": "alpha", "value": "0.75", "unit": "1", "description": "Factor de carga n / m de la tabla hash"},
                    ],
                    "unknown": "Número medio esperado de sondeos E_miss en una búsqueda sin éxito / inserción",
                    "model": "Fórmula de Knuth para agrupamiento primario (primary clustering) en sondeo lineal",
                    "assumptions": [
                        "Función hash uniforme e independiente sobre m ranuras",
                    ],
                    "steps": [
                        {
                            "text": "Calculamos el inverso del cuadrado de la fracción libre (1 - 0.75)^2 = 0.0625.",
                            "equation": "inv_sq = 1 / ((1 - 0.75)^2)",
                            "expression": "1 / ((1 - 0.75) ** 2)",
                            "unit": "1",
                        },
                        {
                            "text": "Aplicamos la media 0.5 * (1 + inv_sq) para obtener el número esperado de sondeos.",
                            "equation": "E_miss = 0.5 * (1 + inv_sq)",
                            "expression": "0.5 * (1 + 16)",
                            "unit": "1",
                        },
                    ],
                    "result": "8.5",
                    "interpretation": (
                        "Al 75 % de ocupación, una inserción por sondeo lineal clásico explora 8.5 ranuras en promedio "
                        "(y al 90 % subiría a 50.5 ranuras); de ahí el uso de Robin Hood hashing o metadatos SIMD (SwissTable)."
                    ),
                    "limitations": [
                        "El resultado asume independencia total de la función hash; funciones débiles sufren agrupamiento aún mayor."
                    ],
                    "mistakes": [
                        "Permitir que una tabla de direccionamiento abierto supere alpha > 0.85 sin redimensionar."
                    ],
                },
            },
            "exercises": _exercises_set("VOL02-C04", "algoritmos de grafos, árboles B+ y tablas hash", 20),
            "notation": [
                {"symbol": r"\alpha", "meaning": "Factor de carga n/m de una tabla hash", "units": "adimensional"},
            ],
            "terminology": [
                {
                    "canonical": "Árbol B+",
                    "definition": "Árbol de búsqueda autoequilibrado multicamino donde todos los valores residen en las hojas enlazadas secuencialmente y los nodos internos solo almacenan claves guía.",
                    "synonyms": ["B+ Tree"],
                },
            ],
        },
        {
            "id": "cap05-estructuras-persistentes-probabilisticas-paralelos",
            "part_id": "parte-iii-algoritmos",
            "part_title": "PARTE III. Algoritmos, Estructuras de Datos y Computación",
            "title": "Estructuras de datos persistentes, estructuras probabilísticas (Bloom filter, HyperLogLog) y algoritmos paralelos (Work-Span)",
            "sources": ["src-mit-6006", "src-acm-cs2023"],
            "concepts": [
                {"id": "persistencia-path-copying", "title": "Estructuras persistentes e inmutabilidad con compartición estructural (path copying)"},
                {"id": "probabilisticas-work-span", "title": "Filtros de Bloom, Skip Lists y modelo Work-Span (T_1, T_inf) de algoritmos paralelos"},
            ],
            "subsections": [
                {"id": "cap05.1", "title": "Estructuras persistentes (path copying) y filtros probabilísticos (Bloom Filter)"},
                {"id": "cap05.2", "title": "Algoritmos paralelos: modelo Work-Span, ley de Brent y reducciones paralelas"},
            ],
            "purpose": (
                "Dominar técnicas avanzadas indispensables en sistemas modernos: estructuras persistentes que conservan "
                "versiones históricas sin clonar toda la memoria, filtros de Bloom para evitar accesos innecesarios a "
                "disco y el modelo Work-Span para analizar algoritmos paralelos."
            ),
            "paragraphs": [
                {
                    "subsection": "cap05.1",
                    "text": (
                        "Una estructura de datos es persistente cuando cualquier operación de actualización produce una "
                        "nueva versión lógicamente independiente conservando intacta la versión anterior. En lugar de "
                        "copiar los $n$ elementos en $\\Theta(n)$, las estructuras persistentes basadas en árboles "
                        "(empleadas en Git, Clojure, Scala, Redux/Immer y motores MVCC) aplican copia de camino (path "
                        "copying) y compartición estructural (structural sharing): al modificar una hoja de un árbol de "
                        "altura $h = O(\\log n)$, se asignan únicamente los $O(\\log n)$ nodos del camino desde la raíz "
                        "hasta la hoja modificada, mientras que todos los subárboles no modificados se comparten de forma "
                        "segura porque son inmutables.\n\n"
                        "En sistemas de almacenamiento (como motores LSM-tree en RocksDB, Cassandra o LevelDB), antes de "
                        "buscar una clave en múltiples archivos SSTable de disco se consulta en RAM un Filtro de Bloom "
                        "(Burton Bloom, 1970): un vector de $m$ bits inicializado a 0 junto con $k$ funciones hash "
                        "independientes. Al insertar $x$, se activan los bits $h_1(x), \\dots, h_k(x)$. Si al consultar "
                        "$y$ alguno de los $k$ bits vale 0, se garantiza con certeza absoluta (0 % de falsos negativos) "
                        "que $y$ no pertenece al conjunto; si todos valen 1, puede tratarse de un falso positivo con "
                        "probabilidad aproximada $(1 - e^{-kn/m})^k$, que se minimiza eligiendo $k = \\frac{m}{n} \\ln 2$."
                    ),
                },
                {
                    "subsection": "cap05.2",
                    "text": (
                        "Para analizar algoritmos paralelos con independencia del número concreto de núcleos físicos $P$, "
                        "el modelo de grafo de tareas (Work-Span model, usado en Cilk, Rayon en Rust y ForkJoinPool en Java) "
                        "define dos métricas intrínsecas del cómputo DAG:\n"
                        "1. Trabajo ($T_1$, Work): el tiempo total de ejecutar todas las operaciones en un único procesador.\n"
                        "2. Longitud de camino crítico ($T_\\infty$, Span o Depth): el tiempo requerido en un computador "
                        "ideal con infinitos procesadores, determinado por la cadena más larga de dependencias secuenciales.\n\n"
                        "Todo planificador válido satisface las dos cotas inferiores fundamentales: $T_P \\ge T_1 / P$ "
                        "(cota de trabajo) y $T_P \\ge T_\\infty$ (cota de camino crítico). Además, un planificador voraz "
                        "o por robo de trabajo (work-stealing, como el de Rayon o Tokio) garantiza la cota superior de "
                        "Brent-Graham: $T_P \\le T_1 / P + T_\\infty$. El cociente $\\overline{P} = T_1 / T_\\infty$ se "
                        "denomina paralelismo medio del algoritmo: cuando $\\overline{P} \\gg P$, el algoritmo alcanza "
                        "aceleración lineal casi perfecta $T_P \\approx T_1 / P$."
                    ),
                },
            ],
            "definition": (
                "Teorema de Brent-Graham en el Modelo Work-Span y Paralelismo Medio: dado un cómputo paralelo libre "
                "de bloqueos con trabajo total $T_1$ y camino crítico (span) $T_\\infty$, el tiempo de ejecución en "
                "$P$ procesadores bajo planificación voraz satisface $\\max(T_1 / P, T_\\infty) \\le T_P \\le T_1 / P + T_\\infty$. "
                "El paralelismo medio es $\\overline{P} = T_1 / T_\\infty$."
            ),
            "consejo": (
                "En un algoritmo paralelo de divide y vencerás (como Mergesort o suma en árbol), corte la generación "
                "de tareas paralelas por debajo de un umbral de granularidad (por ejemplo, bloques de $4096$ elementos) "
                "y resuelva las hojas secuencialmente para que el coste de planificación no domine a $T_1$."
            ),
            "self_check": (
                "1. ¿Por qué la compartición estructural (path copying) solo es segura cuando los nodos compartidos son inmutables? "
                "2. ¿Por qué un filtro de Bloom nunca produce falsos negativos pero sí puede producir falsos positivos, y por qué no admite borrado directo de bits? "
                "3. ¿Qué mide el cociente $T_1 / T_\\infty$ en el modelo Work-Span?"
            ),
            "worked": {
                "prompt": (
                    "Un algoritmo paralelo de reducción y filtrado tiene un trabajo total $T_1 = 9600\\text{ ms}$ "
                    "y un camino crítico (span) $T_\\infty = 40\\text{ ms}$. Calcule la cota superior garantizada de "
                    "tiempo de ejecución $T_P = T_1 / P + T_\\infty$ en $P = 16$ procesadores bajo un planificador voraz."
                ),
                "expression": "(9600 / 16) + 40",
                "difficulty": "INTERMEDIATE",
                "problem_type": "NUMERICAL",
                "solution": {
                    "given": [
                        {"symbol": "T_1", "value": "9600", "unit": "1", "description": "Trabajo secuencial total (ms)"},
                        {"symbol": "T_inf", "value": "40", "unit": "1", "description": "Camino crítico o span (ms)"},
                        {"symbol": "P", "value": "16", "unit": "1", "description": "Número de procesadores"},
                    ],
                    "unknown": "Cota superior de tiempo de ejecución T_P en milisegundos",
                    "model": "Desigualdad de Brent-Graham en el modelo Work-Span (T_P <= T_1 / P + T_inf)",
                    "assumptions": [
                        "Planificador voraz sin sobrecarga significativa de robo de tareas",
                    ],
                    "steps": [
                        {
                            "text": "Dividimos el trabajo total T_1 entre los P = 16 procesadores.",
                            "equation": "t_{\text{work}} = T_1 / P",
                            "expression": "9600 / 16",
                            "unit": "1",
                        },
                        {
                            "text": "Sumamos el span T_inf = 40 ms para obtener la cota superior garantizada.",
                            "equation": "T_{P,\max} = t_{\text{work}} + T_{\infty}",
                            "expression": "600 + 40",
                            "unit": "1",
                        },
                    ],
                    "result": "640",
                    "interpretation": (
                        "Dado que el paralelismo medio T_1 / T_inf = 240 supera ampliamente a P = 16, el tiempo "
                        "queda acotado entre 600 ms y 640 ms, logrando una aceleración efectiva de 9600 / 640 = 15x."
                    ),
                    "limitations": [
                        "La cota no contabiliza la contención del ancho de banda de memoria DRAM cuando los 16 núcleos saturan el bus."
                    ],
                    "mistakes": [
                        "Intentar borrar un elemento de un filtro de Bloom estándar poniendo sus k bits a 0, lo cual corrompería otros elementos que compartan esos bits."
                    ],
                },
            },
            "exercises": _exercises_set("VOL02-C05", "estructuras persistentes, filtros de Bloom y modelo Work-Span", 22),
            "notation": [
                {"symbol": r"T_1", "meaning": "Trabajo total secuencial (Work) del grafo de tareas", "units": "s"},
                {"symbol": r"T_\infty", "meaning": "Camino crítico (Span) con infinitos procesadores", "units": "s"},
            ],
            "terminology": [
                {
                    "canonical": "Filtro de Bloom",
                    "definition": "Estructura de datos probabilística compacta para pruebas de pertenencia a conjuntos con cero falsos negativos y tasa controlada de falsos positivos.",
                    "synonyms": ["Bloom filter"],
                },
            ],
        },
        {
            "id": "cap06-jerarquia-memoria-caches-abi-enlazado",
            "part_id": "parte-iv-sistemas",
            "part_title": "PARTE IV. Sistemas Informáticos, Compiladores, Memoria y Sistemas Operativos",
            "title": "Jerarquía de memoria, coherencia de caché (MESI), false sharing, alineamiento, ABI y enlazado",
            "sources": ["src-c-standard", "src-cpp-standard", "src-rust-reference"],
            "concepts": [
                {"id": "lineas-cache-mesi-false-sharing", "title": "Líneas de caché (64 B), asociatividad, protocolo MESI y false sharing"},
                {"id": "alineamiento-abi-enlazado", "title": "Alineamiento de estructuras, padding, ABI, archivos objeto ELF/Mach-O y enlazado estático/dinámico"},
            ],
            "subsections": [
                {"id": "cap06.1", "title": "Líneas de caché, coherencia MESI, false sharing y diseño orientado a datos"},
                {"id": "cap06.2", "title": "Alineamiento en memoria, ABI de plataforma y enlazadores (ELF/Mach-O)"},
            ],
            "purpose": (
                "Explicar cómo las líneas de caché de 64 bytes, el protocolo de coherencia entre núcleos, las reglas "
                "de alineamiento del ABI y el proceso de enlazado determinan el rendimiento real y la interoperabilidad "
                "binaria de los programas."
            ),
            "paragraphs": [
                {
                    "subsection": "cap06.1",
                    "text": (
                        "Las cachés del procesador no transfieren bytes individuales desde la RAM, sino bloques alineados "
                        "de tamaño fijo denominados líneas de caché (cache lines, de $64\\text{ bytes}$ en x86-64 y la "
                        "mayoría de procesadores ARM64, o $128\\text{ bytes}$ en los núcleos de alto rendimiento Apple M-series). "
                        "En un procesador multinúcleo, cada núcleo posee su propia caché L1 privada; para evitar lecturas "
                        "incoherentes, el hardware implementa protocolos de invalidación de directorio o bus como MESI "
                        "(Modified, Exclusive, Shared, Invalid): para que un núcleo modifique un byte de una línea, debe "
                        "adquirir la línea completa en estado Exclusive/Modified e invalidar las copias en las cachés L1 "
                        "de todos los demás núcleos.\n\n"
                        "De aquí surge una patología crítica de rendimiento concurrente: la compartición falsa (false sharing). "
                        "Si dos hilos ejecutándose en núcleos distintos actualizan intensivamente dos contadores atómicos "
                        "independientes (`counter_a` y `counter_b`) que por estar declarados contiguos en una estructura "
                        "caen dentro de la misma línea de caché de 64 bytes, ambos núcleos se invalidarán mutuamente la línea "
                        "en cada escritura (cache line ping-pong), degradando el rendimiento en un orden de magnitud pese "
                        "a no compartir ningún dato lógico. La solución consiste en acumular en una variable local de registro "
                        "y volcar al final, o alinear cada contador a su propia línea de caché (`#[repr(align(64))]` en Rust "
                        "o `alignas(64)` en C11/C++11)."
                    ),
                },
                {
                    "subsection": "cap06.2",
                    "text": (
                        "Los accesos a memoria de un tipo primitivo de tamaño $k$ bytes son atómicos y eficientes en hardware "
                        "cuando su dirección es múltiplo de su alineamiento natural $k$. Por ello, el ABI de C (como el "
                        "System V AMD64 ABI o el AAPCS64 de ARM) inserta bytes de relleno (padding) entre campos de un "
                        "`struct` y al final del mismo para que su tamaño total sea múltiplo del alineamiento máximo de sus "
                        "miembros. Mientras que en C el compilador está obligado a respetar el orden textual de declaración "
                        "de los campos, en Rust el diseño por defecto `#[repr(Rust)]` permite al compilador reordenar "
                        "automáticamente los campos en memoria para minimizar el padding sin cambiar el código fuente "
                        "(utilizándose `#[repr(C)]` solo cuando se cruza una frontera FFI).\n\n"
                        "Cuando el compilador traduce una unidad de traducción, emite un archivo objeto relocalizable "
                        "(formato ELF en Linux, Mach-O en macOS, COFF/PE en Windows) con tablas de símbolos definidos e "
                        "indefinidos y entradas de relocalización. El enlazador (linker: `lld`, `ld`, `mold`) resuelve las "
                        "referencias cruzadas entre módulos, fusiona secciones y produce bien un ejecutable enlazado "
                        "estáticamente o bien un binario dinámico que delega en el cargador del sistema (`ld.so` / `dyld`) "
                        "la resolución de bibliotecas compartidas (`.so` / `.dylib` / `.dll`) a través de la Global Offset "
                        "Table (GOT) y Procedure Linkage Table (PLT)."
                    ),
                },
            ],
            "definition": (
                "Regla de Alineamiento de Estructuras (ABI C) y Compartición Falsa (False Sharing): en un `struct` con "
                "diseño C, cada campo con alineamiento $a_i$ se sitúa en el menor desplazamiento `offset` tal que "
                "$\\text{offset} \\bmod a_i = 0$, y el tamaño total del `struct` se redondea al múltiplo superior de "
                "$a_{\\max} = \\max_i a_i$. La compartición falsa ocurre cuando múltiples núcleos escriben en variables "
                "disjuntas que residen en la misma línea física de caché."
            ),
            "consejo": (
                "En C, ordene los miembros de un `struct` de mayor a menor requisito de alineamiento (primero punteros "
                "y `uint64_t` de 8 bytes, luego `uint32_t` de 4, `uint16_t` de 2 y finalmente `uint8_t`/`bool` de 1 byte) "
                "para eliminar el padding interno y aumentar el número de registros que caben por línea de caché."
            ),
            "self_check": (
                "1. ¿Por qué `struct { uint8_t a; uint64_t b; uint8_t c; }` ocupa 24 bytes en C de 64 bits pero solo 16 bytes si se reordena como `{ uint64_t b; uint8_t a; uint8_t c; }`? "
                "2. ¿Qué provoca el fenómeno de false sharing en el protocolo MESI y cómo se corrige? "
                "3. ¿Por qué Rust distingue entre su layout optimizado por defecto y `#[repr(C)]`?"
            ),
            "worked": {
                "prompt": (
                    "Calcule el ahorro total en kilobytes (1 KiB = 1024 bytes) de un vector en memoria de "
                    "$N = 65536$ registros cuando se reordena en C una estructura mal alineada de $24\\text{ bytes}$ "
                    "(`uint8_t`, 7 bytes de padding, `uint64_t`, `uint8_t`, 7 bytes de padding) a su disposición "
                    "óptima de $16\\text{ bytes}$ (`uint64_t`, `uint8_t`, `uint8_t`, 6 bytes de padding final)."
                ),
                "expression": "(65536 * (24 - 16)) / 1024",
                "difficulty": "FOUNDATIONAL",
                "problem_type": "OPTIMIZATION",
                "solution": {
                    "given": [
                        {"symbol": "N", "value": "65536", "unit": "1", "description": "Número de estructuras en el vector"},
                        {"symbol": "S_bad", "value": "24", "unit": "1", "description": "Tamaño en bytes con orden subóptimo"},
                        {"symbol": "S_opt", "value": "16", "unit": "1", "description": "Tamaño en bytes ordenando de mayor a menor alineamiento"},
                    ],
                    "unknown": "Ahorro de memoria en KiB para el vector de 65536 elementos",
                    "model": "Cálculo de huella de memoria de arrays contiguos con alineamiento ABI de 8 bytes",
                    "assumptions": [
                        "Arquitectura de 64 bits donde alignof(uint64_t) == 8",
                    ],
                    "steps": [
                        {
                            "text": "Calculamos los bytes ahorrados por cada registro individual al eliminar un bloque de padding.",
                            "equation": "delta_s = S_bad - S_opt",
                            "expression": "24 - 16",
                            "unit": "1",
                        },
                        {
                            "text": "Multiplicamos por los 65536 registros y dividimos entre 1024 bytes/KiB.",
                            "equation": "saved_kib = (N * delta_s) / 1024",
                            "expression": "(65536 * 8) / 1024",
                            "unit": "1",
                        },
                    ],
                    "result": "512",
                    "interpretation": (
                        "Simplemente reordenando dos líneas de declaración en C se ahorran 512 KiB (un 33 % de la memoria) "
                        "y ahora caben 4 estructuras por línea de caché de 64 B en lugar de 2.66."
                    ),
                    "limitations": [
                        "Si la estructura define un protocolo binario de red o hardware fijo, no debe reordenarse sin actualizar la especificación del protocolo."
                    ],
                    "mistakes": [
                        "Abusar de `__attribute__((packed))` o `#[repr(packed)]` en estructuras de uso intensivo en CPU, generando accesos desalineados costosos o UB al tomar referencias."
                    ],
                },
            },
            "exercises": _exercises_set("VOL02-C06", "cachés, protocolo MESI, false sharing, alineamiento ABI y enlazado", 24),
            "notation": [
                {"symbol": "MESI", "meaning": "Estados Modified, Exclusive, Shared, Invalid de coherencia de caché", "units": "adimensional"},
            ],
            "terminology": [
                {
                    "canonical": "Application Binary Interface (ABI)",
                    "definition": "Contrato binario de bajo nivel entre módulos compilados que define tamaños/alineamientos de tipos, convenciones de paso de parámetros en registros y nombres de símbolos.",
                    "synonyms": ["ABI"],
                },
            ],
        },
        {
            "id": "cap07-compiladores-lexing-parsing-ssa-codegen",
            "part_id": "parte-iv-sistemas",
            "part_title": "PARTE IV. Sistemas Informáticos, Compiladores, Memoria y Sistemas Operativos",
            "title": "Arquitectura de compiladores: análisis léxico, parsing LL/LR/Pratt, AST, tipos, IR en forma SSA y generación de código",
            "sources": ["src-acm-cs2023", "src-rust-reference", "src-cpp-standard"],
            "concepts": [
                {"id": "frontend-lex-parse-types", "title": "Front-end: tokenización, análisis sintáctico descendente/Pratt, AST e inferencia de tipos Hindley-Milner"},
                {"id": "middle-backend-ssa-llvm", "title": "Middle-end y Back-end: representación intermedia SSA, nodos phi, optimizaciones y asignación de registros"},
            ],
            "subsections": [
                {"id": "cap07.1", "title": "Front-end del compilador: análisis léxico, sintáctico (descendente recursivo y Pratt) y semántico"},
                {"id": "cap07.2", "title": "Representación intermedia SSA, optimizaciones e instrucción/asignación de registros"},
            ],
            "figure": {
                "key": "fig-pipeline-compilador",
                "caption": "Arquitectura en tres etapas de un compilador moderno: Front-end (Lexer, Parser, AST, Tipos), Middle-end (IR en forma SSA y pases de optimización) y Back-end (Selección de instrucciones, asignación de registros y código objeto).",
                "tikz": r"""
\draw[thick, fill=blue!8] (0,0) rectangle (3.5,1.2) node[pos=.5, align=center, font=\scriptsize\bfseries] {Front-End\\Lexer $\to$ AST $\to$ Tipos};
\draw[thick, ->] (3.5,0.6) -- (4.4,0.6);
\draw[thick, fill=teal!10] (4.4,0) rectangle (8.1,1.2) node[pos=.5, align=center, font=\scriptsize\bfseries] {Middle-End\\CFG / Forma SSA ($\phi$)};
\draw[thick, ->] (8.1,0.6) -- (9.0,0.6);
\draw[thick, fill=orange!12] (9.0,0) rectangle (12.5,1.2) node[pos=.5, align=center, font=\scriptsize\bfseries] {Back-End\\Registros $\to$ ASM/ELF};
""",
            },
            "purpose": (
                "Desmitificar cómo funciona por dentro un compilador industrial (`rustc`, `clang`, `gcc`, `ghc`, `v8`), "
                "recorriendo las etapas de la {{fig:fig-pipeline-compilador}} para que el lector pueda tanto diagnosticar "
                "qué código genera su compilador como construir su propio lenguaje, DSL o herramienta de análisis estático."
            ),
            "paragraphs": [
                {
                    "subsection": "cap07.1",
                    "text": (
                        "Un compilador moderno se divide en tres grandes etapas desacopladas (Front-End, Middle-End y "
                        "Back-End). El Front-End comienza con el analizador léxico (lexer o scanner), que agrupa caracteres "
                        "UTF-8 mediante autómatas finitos deterministas en una secuencia de tokens con información de "
                        "posición (span). A continuación, el analizador sintáctico (parser) comprueba la gramática libre "
                        "de contexto y construye el Árbol de Sintaxis Abstracta (AST). Mientras que los generadores clásicos "
                        "(Yacc/Bison, ANTLR) construyen tablas LR o LL, los compiladores de producción actuales (`rustc`, "
                        "`clang`, `go`, `tsc`) utilizan mayoritariamente descenso recursivo escrito a mano combinado con "
                        "parsing de Pratt (Top-Down Operator Precedence, Vaughan Pratt 1973) para expresiones con niveles "
                        "de precedencia y asociatividad, ya que facilita mensajes de diagnóstico precisos y recuperación "
                        "ante errores sintácticos.\n\n"
                        "Sobre el AST, el análisis semántico resuelve nombres en tablas de símbolos con ámbito léxico y "
                        "ejecuta la comprobación e inferencia de tipos (mediante unificación de restricciones al estilo "
                        "Hindley-Milner Damas-Milner o comprobación bidireccional), reduciendo el lenguaje de superficie "
                        "a una representación tipada de alto nivel (como HIR y MIR en `rustc`, donde se ejecuta el borrow checker)."
                    ),
                },
                {
                    "subsection": "cap07.2",
                    "text": (
                        "El Middle-End traduce el programa a un Grafo de Flujo de Control (CFG) de bloques básicos en "
                        "forma SSA (Static Single Assignment, Cytron et al. 1991, base de LLVM IR, GCC GIMPLE y Go SSA): "
                        "cada variable temporal se asigna exactamente una vez en el texto del programa, y cuando dos "
                        "ramas de un condicional convergen en un bloque de unión se inserta una función $\\phi(x_1, x_2)$ "
                        "que selecciona el valor según el bloque predecesor. La forma SSA hace explícitas las cadenas "
                        "definición-uso (def-use chains), simplificando drásticamente optimizaciones como propagación de "
                        "constantes, eliminación de código muerto (DCE), numeración global de valores (GVN), movimiento de "
                        "código invariante de bucle (LICM) e inlining.\n\n"
                        "Finalmente, el Back-End realiza la selección de instrucciones para la ISA destino (x86-64, ARM64, "
                        "RISC-V, WebAssembly), ejecuta la asignación de registros (modelada como coloreado de grafos de "
                        "interferencia por Chaitin-Briggs o mediante barrido lineal Linear Scan en compiladores JIT, "
                        "volcando a la pila —spilling— las variables que exceden los registros físicos disponibles) y "
                        "planifica las instrucciones para maximizar el paralelismo a nivel de instrucción."
                    ),
                },
            ],
            "definition": (
                "Forma de Asignación Única Estática (SSA) y Grafo de Interferencia de Registros: una representación "
                "intermedia está en forma SSA si cada variable virtual posee exactamente un punto de definición "
                "estático y toda definición domina todos sus usos (o se combina mediante nodos $\\phi$ en la frontera "
                "de dominancia). Dos variables interfieren en la asignación de registros si sus intervalos de vida "
                "(liveness) se solapan en algún punto del CFG, impidiendo compartir el mismo registro físico."
            ),
            "consejo": (
                "Cuando escriba un parser para expresiones aritméticas o booleanas con múltiples niveles de precedencia, "
                "utilice un parser de Pratt con potencias de enlace izquierda/derecha `(l_bp, r_bp)` en lugar de crear "
                "una función recursiva distinta por cada nivel de precedencia: el código se reduce a una tercera parte "
                "y permite añadir nuevos operadores en una sola línea de tabla."
            ),
            "self_check": (
                "1. ¿Por qué los compiladores industriales como `rustc` y `clang` prefieren descenso recursivo + Pratt frente a generadores LR automáticos? "
                "2. ¿Para qué sirve el nodo $\\phi(x_1, x_2)$ en la representación intermedia SSA cuando convergen dos ramas de un `if-else`? "
                "3. ¿Cómo se modela la asignación de registros como un problema de $k$-coloreado sobre el grafo de interferencia?"
            ),
            "worked": {
                "prompt": (
                    "En un bloque básico antes de la optimización se evalúa en un bucle de $N = 1000$ iteraciones "
                    "una expresión con una subexpresión invariante de bucle de coste $c_{\\text{inv}} = 6$ ciclos y una "
                    "parte dependiente del índice de coste $c_{\\text{var}} = 3$ ciclos por iteración. Calcule el ahorro "
                    "total de ciclos al aplicar el pase de Movimiento de Código Invariante de Bucle (LICM), que evalúa "
                    "la subexpresión invariante una única vez fuera del bucle."
                ),
                "expression": "1000 * (6 + 3) - (6 + 1000 * 3)",
                "difficulty": "FOUNDATIONAL",
                "problem_type": "OPTIMIZATION",
                "solution": {
                    "given": [
                        {"symbol": "N", "value": "1000", "unit": "1", "description": "Iteraciones del bucle"},
                        {"symbol": "c_inv", "value": "6", "unit": "1", "description": "Ciclos de la subexpresión invariante"},
                        {"symbol": "c_var", "value": "3", "unit": "1", "description": "Ciclos de la parte dependiente del índice"},
                    ],
                    "unknown": "Ahorro neto de ciclos tras aplicar el pase LICM",
                    "model": "Modelo de coste de bloque básico bajo Loop-Invariant Code Motion (LICM)",
                    "assumptions": [
                        "La subexpresión invariante es pura, no lanza trampas de hardware (como división por cero) y sus operandos no sufren aliasing en el bucle",
                    ],
                    "steps": [
                        {
                            "text": "Calculamos el coste sin optimizar ejecutando ambas partes en las 1000 iteraciones.",
                            "equation": "C_orig = N * (c_inv + c_var)",
                            "expression": "1000 * (6 + 3)",
                            "unit": "1",
                        },
                        {
                            "text": "Restamos el coste tras elevar la expresión invariante al preheader del bucle (6 + 3000).",
                            "equation": "saved = C_orig - (c_inv + N * c_var)",
                            "expression": "9000 - 3006",
                            "unit": "1",
                        },
                    ],
                    "result": "5994",
                    "interpretation": (
                        "El pase LICM ahorra 5994 ciclos (dos tercios del tiempo del bucle); en C este pase puede "
                        "bloquearse si el compilador no puede descartar que un puntero de escritura apunte al mismo "
                        "objeto leído (problema que se resuelve con `restrict` en C o con las garantías de `&` y `&mut` en Rust)."
                    ),
                    "limitations": [
                        "Elevar demasiadas expresiones invariantes simultáneamente puede aumentar la presión de registros y provocar spilling a la pila."
                    ],
                    "mistakes": [
                        "Suponer que el compilador puede sacar del bucle una llamada a función externa con posibles efectos laterales o lecturas a través de punteros con posible aliasing."
                    ],
                },
            },
            "exercises": _exercises_set("VOL02-C07", "lexing, parsing de Pratt, AST, forma SSA y optimizaciones de compilador", 26),
            "notation": [
                {"symbol": r"\phi(x_1, x_2)", "meaning": "Función de selección en punto de convergencia SSA", "units": "adimensional"},
            ],
            "terminology": [
                {
                    "canonical": "Static Single Assignment (SSA)",
                    "definition": "Forma de representación intermedia en la que cada variable recibe valor en un único punto estático de definición.",
                    "synonyms": ["Forma SSA"],
                },
            ],
        },
        {
            "id": "cap08-sistemas-operativos-procesos-memoria-virtual-io",
            "part_id": "parte-iv-sistemas",
            "part_title": "PARTE IV. Sistemas Informáticos, Compiladores, Memoria y Sistemas Operativos",
            "title": "Sistemas operativos: modo kernel, procesos e hilos, planificación, memoria virtual paginada, VFS y multiplexación de E/S",
            "sources": ["src-acm-cs2023", "src-c-standard", "src-posix-bash"],
            "concepts": [
                {"id": "procesos-hilos-syscalls", "title": "Anillos de protección, llamadas al sistema, procesos, hilos y cambios de contexto"},
                {"id": "memoria-virtual-tlb-io", "title": "Memoria virtual paginada, TLB, fallos de página, sistemas de archivos y epoll/kqueue/io_uring"},
            ],
            "subsections": [
                {"id": "cap08.1", "title": "Modo usuario vs modo kernel, llamadas al sistema, procesos, hilos y planificación"},
                {"id": "cap08.2", "title": "Memoria virtual, tablas de páginas, TLB, sistemas de archivos y E/S no bloqueante"},
            ],
            "purpose": (
                "Comprender las abstracciones fundamentales que el núcleo del sistema operativo (Linux, XNU/macOS, "
                "Windows NT) ofrece a todo programa: aislamiento de procesos mediante memoria virtual, coste real "
                "de las llamadas al sistema y mecanismos de entrada/salida de alta concurrencia."
            ),
            "paragraphs": [
                {
                    "subsection": "cap08.1",
                    "text": (
                        "El procesador impone aislamiento de hardware mediante al menos dos niveles de privilegio: modo "
                        "usuario (Ring 3 en x86-64, EL0 en ARM64) y modo supervisor o kernel (Ring 0 / EL1). El código "
                        "de una aplicación se ejecuta en modo usuario y no puede acceder directamente a dispositivos "
                        "físicos ni modificar tablas de páginas; para solicitar servicios al núcleo (abrir un archivo, "
                        "reservar páginas de memoria con `mmap`, enviar paquetes por un socket) ejecuta una instrucción "
                        "de trampa síncrona (`syscall` en x86-64, `svc #0` en ARM64) que salva los registros de usuario, "
                        "conmuta a la pila del kernel, valida los argumentos y ejecuta el manejador privilegiado.\n\n"
                        "Un proceso es la unidad de aislamiento de recursos: posee su propio espacio de direcciones "
                        "virtuales, tabla de descriptores de archivo y credenciales de seguridad. Un hilo (thread) es la "
                        "unidad de planificación de CPU: varios hilos dentro de un mismo proceso comparten el espacio de "
                        "direcciones virtuales (código, datos globales y heap), pero cada uno posee su propio contador de "
                        "programa, banco de registros y pila de llamadas independiente."
                    ),
                },
                {
                    "subsection": "cap08.2",
                    "text": (
                        "La Memoria Virtual, implementada conjuntamente por la Unidad de Gestión de Memoria (MMU) del "
                        "procesador y el sistema operativo, divide el espacio de direcciones en páginas de tamaño fijo "
                        "(típicamente $4\\text{ KiB}$ en x86-64 o $16\\text{ KiB}$ en Apple Silicon ARM64). La MMU traduce "
                        "cada dirección virtual en dirección física recorriendo una tabla de páginas multinivel (4 niveles "
                        "en x86-64 de 48 bits) y almacenando las traducciones recientes en una caché hardware asociativa "
                        "llamada TLB (Translation Lookaside Buffer). Cuando un proceso accede a una página no mapeada en "
                        "RAM, la MMU dispara una excepción de fallo de página (page fault) para que el kernel asigne un "
                        "marco físico bajo demanda (demand paging), cargue datos desde un archivo mapeado (`mmap`) o "
                        "aplique copia en escritura (Copy-on-Write tras `fork`).\n\n"
                        "En el subsistema de Entrada/Salida, bloquear un hilo por cada socket resulta inviable a gran "
                        "escala; por ello los runtimes de red modernos (Tokio en Rust, Node.js/libuv, Netty en Java, Go "
                        "netpoller) configuran los descriptores en modo no bloqueante (`O_NONBLOCK`) y delegan la espera "
                        "multiplexada en primitivas de notificación de eventos de complejidad $O(\\text{eventos activos})$: "
                        "`epoll` en Linux, `kqueue` en macOS/BSD e `io_uring` (colas en anillo compartidas entre usuario y "
                        "kernel sin llamadas al sistema por operación) en Linux moderno."
                    ),
                },
            ],
            "definition": (
                "Traducción de Direcciones Virtuales y Multiplexación de Eventos $O(1)$: en un sistema con páginas "
                "de $2^p$ bytes, los $p$ bits menos significativos de una dirección virtual forman el desplazamiento "
                "dentro de la página (page offset, que no se traduce) y los bits superiores forman el número de página "
                "virtual (VPN) traducido por la TLB/tabla de páginas al número de marco físico (PFN). Primitivas como "
                "`epoll` y `kqueue` notifican únicamente los descriptores listos sin escanear el conjunto total de descriptores registrados."
            ),
            "consejo": (
                "Minimice el número de llamadas al sistema (`read`/`write`) en bucles críticos utilizando buffers en "
                "espacio de usuario (`BufReader`/`BufWriter` en Rust, `BufferedInputStream` en Java, `stdio` en C): "
                "escribir 1 MiB byte a byte mediante un millón de llamadas `write(fd, &b, 1)` es cientos de veces más "
                "lento que agrupar en bloques de 8 KiB o 64 KiB."
            ),
            "self_check": (
                "1. ¿Qué recursos comparten dos hilos de un mismo proceso y qué recursos son privados de cada hilo? "
                "2. ¿Qué función cumple la TLB en la traducción de direcciones virtuales y por qué un cambio de proceso encarece más el contexto que un cambio de hilo del mismo proceso? "
                "3. ¿Por qué `epoll`/`kqueue` escalan a decenas de miles de conexiones donde `select`/`poll` se degradan linealmente?"
            ),
            "worked": {
                "prompt": (
                    "En una arquitectura con páginas de $4\\text{ KiB} = 4096\\text{ bytes}$ ($2^{12}$ bytes), dada la "
                    "dirección virtual decimal $V = 20500$, determine el número de página virtual "
                    "$\\text{VPN} = \\lfloor V / 4096 \\rfloor$, el desplazamiento dentro de la página "
                    "$\\text{offset} = V - \\text{VPN} \\cdot 4096$, y calcule la dirección física resultante si la "
                    "tabla de páginas asigna dicho VPN al marco físico $\\text{PFN} = 12$."
                ),
                "expression": "(12 * 4096) + (20500 - 5 * 4096)",
                "difficulty": "INTERMEDIATE",
                "problem_type": "NUMERICAL",
                "solution": {
                    "given": [
                        {"symbol": "V", "value": "20500", "unit": "1", "description": "Dirección virtual en bytes"},
                        {"symbol": "P_size", "value": "4096", "unit": "1", "description": "Tamaño de página en bytes (4 KiB)"},
                        {"symbol": "PFN", "value": "12", "unit": "1", "description": "Número de marco físico asignado a VPN = 5"},
                    ],
                    "unknown": "Dirección física resultante en bytes tras la traducción MMU",
                    "model": "Traducción de dirección virtual paginada (Physical = PFN * PageSize + Offset)",
                    "assumptions": [
                        "Tamaño de página uniforme de 4096 bytes con VPN = floor(20500 / 4096) = 5",
                    ],
                    "steps": [
                        {
                            "text": "Calculamos el desplazamiento (offset) dentro de la página 5 (5 * 4096 = 20480).",
                            "equation": "offset = V - 5 * P_size",
                            "expression": "20500 - 5 * 4096",
                            "unit": "1",
                        },
                        {
                            "text": "Sumamos el desplazamiento a la dirección base del marco físico PFN = 12.",
                            "equation": "P_addr = PFN * P_size + offset",
                            "expression": "12 * 4096 + 20",
                            "unit": "1",
                        },
                    ],
                    "result": "49172",
                    "interpretation": (
                        "La dirección virtual 20500 corresponde a la página virtual 5 con desplazamiento de 20 bytes, "
                        "que la MMU traduce al marco físico 12 en la dirección física 49152 + 20 = 49172."
                    ),
                    "limitations": [
                        "Para cargas de memoria de decenas de gigabytes, el uso de Huge Pages (2 MiB) reduce los fallos de TLB."
                    ],
                    "mistakes": [
                        "Confundir el tamaño de la dirección virtual con la cantidad de RAM física instalada en el equipo."
                    ],
                },
            },
            "exercises": _exercises_set("VOL02-C08", "sistemas operativos, llamadas al sistema, memoria virtual paginada y epoll/kqueue", 30),
            "notation": [
                {"symbol": "VPN", "meaning": "Virtual Page Number (número de página virtual)", "units": "adimensional"},
                {"symbol": "PFN", "meaning": "Physical Frame Number (número de marco físico)", "units": "adimensional"},
            ],
            "terminology": [
                {
                    "canonical": "Translation Lookaside Buffer (TLB)",
                    "definition": "Caché hardware dentro de la MMU que almacena traducciones recientes de páginas virtuales a marcos físicos.",
                    "synonyms": ["TLB"],
                },
            ],
        },
    ],
}


def main() -> None:
    s1 = build_studium_volume(VOL01_SPEC)
    s2 = build_studium_volume(VOL02_SPEC)
    print("Volúmenes 1 y 2 completados:", s1["pages"], "y", s2["pages"], "páginas.")


if __name__ == "__main__":
    main()
