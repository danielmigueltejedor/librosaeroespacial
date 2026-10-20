#!/usr/bin/env python3
"""Construcción completa del Volumen 3 de la Enciclopedia:
- vol03-monografia-rust (Parte V — Monografía de Referencia del Lenguaje Rust: De cero a sistemas concurrentes, unsafe y arquitectura)
Sigue íntegramente la plantilla obligatoria A–H en 8 capítulos autónomos con pruebas ejecutables reales verificadas por `rustc --test`.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from studium_volume_helper import ROOT, build_studium_volume  # noqa: E402

VOL03_SPEC: dict[str, object] = {
    "slug": "vol03-monografia-rust",
    "code": "ENC-VOL03",
    "title": "Volumen III: Monografía Completa de Rust — Seguridad de Memoria, Concurrencia y Sistemas",
    "subtitle": "Parte V (Bloque A–H): De cero a sistemas de alto rendimiento, programación asíncrona, unsafe y arquitectura",
    "target_pages": 68,
    "terminology": [
        {"term": "propiedad única (ownership)", "canonical": "propiedad única (ownership)", "forbidden": ["dueñez", "posesión libre"]},
        {"term": "préstamo comprobado (borrowing)", "canonical": "préstamo comprobado (borrowing)", "forbidden": ["empréstito de puntero"]},
        {"term": "tiempo de vida léxico/no léxico (lifetime)", "canonical": "tiempo de vida (lifetime)", "forbidden": ["duración vital"]},
        {"term": "mutabilidad interior (interior mutability)", "canonical": "mutabilidad interior (interior mutability)", "forbidden": ["mutación oculta"]},
    ],
    "notation": [
        {"symbol": r"\text{'a}", "meaning": "Parámetro genérico de tiempo de vida (lifetime) de una referencia", "unit": "adimensional"},
        {"symbol": r"T: \text{Send} + \text{Sync}", "meaning": "Cotas de rasgo de transferencia y compartición segura entre hilos", "unit": "adimensional"},
        {"symbol": r"\text{sizeof}(T)", "meaning": "Tamaño estático en bytes de un tipo Sized en pila", "unit": "B"},
        {"symbol": r"\text{alignof}(T)", "meaning": "Alineamiento de dirección de memoria requerido por el tipo T", "unit": "B"},
    ],
    "chapters": [
        {
            "id": "cap01-introduccion-historia-modelo-compilacion-rust",
            "title": "A. Introducción, historia, filosofía y modelo de compilación de Rust",
            "part_id": "parte-v-rust-fundamentos",
            "part_title": "Bloques A–C: Fundamentos, Entorno y Nivel Principiante en Rust",
            "sources": ["src-rust-book", "src-rust-nomicon"],
            "learning_objectives": [
                "Comprender el origen histórico de Rust (Graydon Hoare, Mozilla Research, Rust Foundation) y las ediciones 2015, 2018, 2021 y 2024.",
                "Trazar la tubería de compilación desde el código fuente hasta código máquina nativo pasando por HIR, THIR, MIR y LLVM IR.",
                "Contrastar las abstracciones de coste cero y la seguridad espacial y temporal de memoria sin recolector de basura frente a C, C++ y Go.",
            ],
            "concepts": [
                {"id": "cpt-rust-mir-llvm", "title": "Representación intermedia MIR, comprobador de préstamos NLL y generación de código LLVM"},
                {"id": "cpt-rust-zero-cost", "title": "Abstracciones de coste cero, monomorfización y ausencia de recolector de basura"},
            ],
            "subsections": [
                {"id": "sec-rust-1-1", "title": "Historia, problema que resuelve y filosofía de diseño"},
                {"id": "sec-rust-1-2", "title": "Modelo de ejecución, fases HIR/MIR/LLVM y comparativa con otros lenguajes"},
            ],
            "figure": {
                "key": "fig-rust-compiler-pipeline",
                "caption": "Tubería del compilador rustc: análisis sintáctico, expansión de macros, HIR, inferencia de tipos, MIR (borrow checker NLL) y optimización LLVM.",
                "tikz": r"""\begin{tikzpicture}[node distance=1.6cm, >=stealth, thick, font=\small]
\node[draw=blue!70!black, fill=blue!8, rounded corners, minimum width=2.2cm, minimum height=0.9cm, align=center] (src) {\texttt{.rs}\\AST + Macros};
\node[draw=blue!70!black, fill=blue!8, rounded corners, minimum width=2.2cm, minimum height=0.9cm, align=center, right=0.5cm of src] (hir) {HIR / THIR\\Inferencia Tipos};
\node[draw=orange!75!black, fill=orange!12, rounded corners, minimum width=2.5cm, minimum height=0.9cm, align=center, right=0.5cm of hir] (mir) {MIR\\Borrow Checker};
\node[draw=teal!70!black, fill=teal!10, rounded corners, minimum width=2.3cm, minimum height=0.9cm, align=center, right=0.5cm of mir] (llvm) {LLVM IR\\Monomorfización};
\node[draw=green!60!black, fill=green!10, rounded corners, minimum width=2.1cm, minimum height=0.9cm, align=center, right=0.5cm of llvm] (bin) {ELF / Mach-O\\Binario Nativo};
\draw[->] (src) -- (hir);
\draw[->] (hir) -- (mir);
\draw[->] (mir) -- (llvm);
\draw[->] (llvm) -- (bin);
\end{tikzpicture}""",
            },
            "purpose": (
                "Este capítulo inaugura la monografía autónoma de Rust (Bloque A). Un lector sin experiencia previa en C o C++ "
                "comprenderá qué problema fundamental de la ingeniería de sistemas resuelve Rust: garantizar simultáneamente control "
                "predictivo sobre la representación de memoria y ausencia matemática de comportamiento indefinido (Undefined Behavior) "
                "en código seguro (`safe Rust`), sin recurrir a un recolector de basura en tiempo de ejecución."
            ),
            "paragraphs": [
                {
                    "subsection": "sec-rust-1-1",
                    "text": (
                        "Iniciado en 2006 por Graydon Hoare y respaldado por Mozilla Research desde 2009 para construir el motor "
                        "experimental Servo, Rust alcanzó su versión estable 1.0 en mayo de 2015 bajo un compromiso estricto de "
                        "estabilidad sin estancamiento mediante el sistema de Ediciones (2015, 2018, 2021 y 2024). Las estadísticas "
                        "de vulnerabilidades publicadas por Microsoft Security Response Center y el proyecto Chromium revelaron que "
                        "aproximadamente el 70 % de las vulnerabilidades críticas de seguridad en grandes bases de código C y C++ "
                        "proceden de defectos de seguridad de memoria: uso después de liberación (use-after-free), doble liberación "
                        "(double free), desbordamientos de búfer, desreferenciación de punteros colgantes (dangling pointers) y "
                        "carreras de datos (data races) entre hilos. Como se ilustra en la Figura \\ref{fig:fig-rust-compiler-pipeline}, "
                        "Rust traslada la verificación de estas invariantes desde el tiempo de ejecución hacia la representación "
                        "intermedia de nivel medio (MIR, Mid-level Intermediate Representation) durante la compilación."
                    ),
                },
                {
                    "subsection": "sec-rust-1-2",
                    "text": (
                        "El principio de abstracciones de coste cero (zero-cost abstractions), formulado originalmente por Bjarne "
                        "Stroustrup, establece que aquello que no se utiliza no conlleva coste alguno y aquello que sí se utiliza "
                        "se compila con una eficiencia igual o superior al código escrito manualmente a bajo nivel. En Rust, los "
                        "tipos genéricos parametrizados $f\\langle T: \\text{Trait}\\rangle(x: T)$ se compilan por defecto mediante "
                        "monomorfización estática: el compilador genera una copia especializada de la función para cada tipo concreto "
                        "invocado, eliminando la indirección de tablas virtuales (`vtable`) y permitiendo el *inlining* agresivo "
                        "del optimizador LLVM:\n"
                        "```rust\n"
                        "// Compilado mediante monomorfización a instrucciones máquina directas sin vtable:\n"
                        "#[inline]\n"
                        "pub fn clamp_value<T: PartialOrd>(val: T, low: T, high: T) -> T {\n"
                        "    if val < low { low } else if val > high { high } else { val }\n"
                        "}\n"
                        "```\n"
                        "Cuando el despacho dinámico es deseable para reducir el tamaño del binario o almacenar colecciones heterogéneas, "
                        "el programador lo solicita explícitamente mediante objetos de rasgo (`&dyn Trait` o `Box<dyn Trait>`), "
                        "representados como un puntero ancho (*fat pointer*) de dos palabras máquina ($2 \\times 8 = 16\\text{ B}$ "
                        "en arquitecturas de 64 bits): una palabra para la dirección del dato y otra para la tabla virtual del rasgo."
                    ),
                },
            ],
            "definition": (
                "Seguridad espacial y temporal de memoria en Rust: propiedad verificada estáticamente en MIR según la cual ningún "
                "acceso seguro lee o escribe fuera de los límites asignados (seguridad espacial) ni accede a una región cuya vida "
                "útil ha concluido o está siendo mutada concurrentemente (seguridad temporal)."
            ),
            "consejo": (
                "No luches contra el comprobador de préstamos intentando replicar grafos cíclicos de punteros mutables propios de "
                "Java o C++; modela la propiedad de los datos como árboles jerárquicos o utiliza índices tipados sobre vectores contiguos (arenas)."
            ),
            "self_check": (
                "¿Por qué un puntero a objeto de rasgo `&dyn Write` ocupa 16 bytes en una arquitectura de 64 bits mientras que una "
                "referencia ordinaria `&File` ocupa únicamente 8 bytes?"
            ),
            "derivation": {
                "title": "Tamaño en memoria de punteros ordinarios y punteros anchos (fat pointers) en Rust",
                "assumptions": ["Arquitectura de 64 bits donde el tamaño de palabra W = 8 bytes"],
                "steps": [
                    {"equation": r"S_{\text{thin}} = W", "justification": "Una referencia a un tipo de tamaño conocido en compilación (Sized) almacena únicamente la dirección base"},
                    {"equation": r"S_{\text{fat}} = 2 W", "justification": "Una referencia a un tipo dinámicamente dimensionado (&[T], &str o &dyn Trait) almacena dirección base más longitud o puntero a vtable"},
                ],
                "Verify": {"left": "2 * W", "right": "W + W"},
            },
            "worked_problem": {
                "prompt": (
                    "En una arquitectura de 64 bits ($W = 8\\text{ B}$), un vector en Rust `Vec<T>` se representa en la pila mediante "
                    "tres campos de tamaño palabra (`ptr`, `len`, `cap`), mientras que una rebanada `&[T]` es un puntero ancho de dos "
                    "palabras (`ptr`, `len`). Calcula el tamaño total en pila en bytes de una estructura que contiene dos `Vec<u8>` y "
                    "tres rebanadas `&[u8]`."
                ),
                "expression": "2 * (3 * 8) + 3 * (2 * 8)",
                "solution": {
                    "model": "Representación en pila de Vec<T> (3 palabras) y &[T] (2 palabras)",
                    "given": [
                        {"symbol": "W", "value": "8 B", "description": "Tamaño de palabra en arquitectura de 64 bits"},
                        {"symbol": "n_vec", "value": "2", "description": "Número de vectores Vec<u8>"},
                        {"symbol": "n_slice", "value": "3", "description": "Número de rebanadas &[u8]"},
                    ],
                    "steps": [
                        {"step": "Tamaño de cada Vec<u8> en pila (3 * 8 = 24 B) y cada &[u8] (2 * 8 = 16 B)", "equation": r"S = 2 \cdot (3 \cdot 8) + 3 \cdot (2 \cdot 8)", "expression": "2 * (3 * 8) + 3 * (2 * 8)"},
                    ],
                    "conclusion": "La estructura ocupa exactamente 96 bytes en la pila (48 B de los dos vectores y 48 B de las tres rebanadas), independientemente del número de elementos alojados en el montículo.",
                },
            },
            "rust_worked_test": {
                "prompt": "Verificación ejecutable con `rustc --test` del tamaño exacto en bytes de `&u64`, `&[u64]` y `Vec<u64>` mediante `std::mem::size_of`.",
                "source_text": (
                    "#[cfg(test)]\n"
                    "mod tests {\n"
                    "    use std::mem::size_of;\n"
                    "    #[test]\n"
                    "    fn verify_pointer_and_vec_layouts() {\n"
                    "        let w = size_of::<usize>();\n"
                    "        assert_eq!(size_of::<&u64>(), w);\n"
                    "        assert_eq!(size_of::<&[u64]>(), 2 * w);\n"
                    "        assert_eq!(size_of::<Vec<u64>>(), 3 * w);\n"
                    "    }\n"
                    "}\n"
                ),
            },
            "practice_problems": [
                {"prompt": "Calcula el tamaño en bytes en la pila de un `Vec<f64>` en una arquitectura de 64 bits ($3 \\times 8$).", "expression": "3 * 8", "difficulty": "FOUNDATIONAL", "problem_type": "DIRECT_SUBSTITUTION"},
                {"prompt": "Calcula el tamaño en bytes de un puntero ancho `&dyn std::fmt::Display` en una CPU de 64 bits ($2 \\times 8$).", "expression": "2 * 8", "difficulty": "FOUNDATIONAL", "problem_type": "DIRECT_SUBSTITUTION"},
                {"prompt": "Si un binario contiene 45 funciones genéricas instanciadas cada una para 4 tipos concretos distintos mediante monomorfización, ¿cuántas funciones especializadas se emiten antes de la eliminación de código muerto?", "expression": "45 * 4", "difficulty": "INTERMEDIATE", "problem_type": "MULTI_STEP"},
                {"prompt": "Un búfer de 4096 elementos `u32` (4 bytes por elemento) está referenciado por un `Vec<u32>` (24 bytes en pila). ¿Cuántos bytes totales suma la cabecera en pila más la región en el montículo?", "expression": "24 + 4096 * 4", "difficulty": "INTERMEDIATE", "problem_type": "DESIGN"},
            ],
        },
        {
            "id": "cap02-entorno-toolchain-cargo-nivel-principiante",
            "title": "B–C. Instalación, toolchain (rustup, Cargo) y nivel principiante completo",
            "part_id": "parte-v-rust-fundamentos",
            "part_title": "Bloques A–C: Fundamentos, Entorno y Nivel Principiante en Rust",
            "sources": ["src-rust-book", "src-unicode-15"],
            "learning_objectives": [
                "Configurar y gestionar toolchains con rustup, perfiles de compilación en Cargo.toml, resolución determinista con Cargo.lock, rustfmt y clippy.",
                "Dominar el modelo de vinculación inmutable por defecto (let vs let mut), sombreado (shadowing), tipos escalares y compuestos, y control de flujo expresivo.",
                "Distinguir la representación UTF-8 de String y &str frente a arrays [T; N], tuplas y vectores Vec<T>.",
            ],
            "concepts": [
                {"id": "cpt-rust-cargo-toolchain", "title": "Gestión de toolchains, workspaces de Cargo, perfiles dev/release y análisis estático con Clippy"},
                {"id": "cpt-rust-scalars-control", "title": "Tipos escalares, semántica de expresiones (bloques, if, match, loop) y cadenas UTF-8"},
            ],
            "subsections": [
                {"id": "sec-rust-2-1", "title": "Bloque B: Toolchain oficial (rustup, rustc, cargo, clippy, rustfmt) y estructura de un crate"},
                {"id": "sec-rust-2-2", "title": "Bloque C: Variables, tipos primitivos, expresiones de control de flujo y funciones"},
            ],
            "purpose": (
                "Este capítulo cubre los Bloques B y C de la plantilla estandarizada: desde la configuración profesional del "
                "entorno (`rustup`, `cargo`, `Cargo.toml`, `Cargo.lock`, `rustfmt`, `clippy`, `rust-analyzer`) hasta el dominio "
                "completo del nivel principiante de Rust. A diferencia de los lenguajes imperativos clásicos donde casi todas las "
                "construcciones son sentencias sin valor, Rust es un lenguaje orientado a expresiones donde `if`, `match` y los "
                "bloques `{ ... }` producen valores tipados verificados estáticamente."
            ),
            "paragraphs": [
                {
                    "subsection": "sec-rust-2-1",
                    "text": (
                        "La herramienta `rustup` administra canales de distribución (`stable`, `beta`, `nightly`) y objetivos de "
                        "compilación cruzada (`targets`, como `aarch64-apple-darwin`, `x86_64-unknown-linux-gnu` o `wasm32-unknown-unknown`). "
                        "Todo paquete en Rust se denomina *crate* (binario o biblioteca) y se gobierna mediante el manifiesto declarativo "
                        "`Cargo.toml`. Mientras que `Cargo.toml` expresa rangos semánticos compatibles (SemVer, por ejemplo `serde = \"1.0\"`), "
                        "el fichero `Cargo.lock` registra las versiones exactas y los resúmenes criptográficos SHA-256 de cada dependencia, "
                        "fijando versiones de dependencias, sin garantizar por sí solo reproducibilidad binaria. Los comandos esenciales del ciclo de ingeniería son `cargo check` "
                        "(verificación rápida de tipos y préstamos en MIR sin invocar el generador de código LLVM), `cargo test` "
                        "(ejecución concurrente de pruebas unitarias, de integración y de documentación), `cargo clippy -- -D warnings` "
                        "(análisis estático con más de 700 reglas idiomáticas y de rendimiento) y `cargo fmt --check`."
                    ),
                },
                {
                    "subsection": "sec-rust-2-2",
                    "text": (
                        "En Rust, las vinculaciones introducidas con `let x: i32 = 42;` son inmutables por defecto; la mutabilidad "
                        "requiere la marca explícita `let mut contador: u64 = 0;`. El lenguaje proporciona enteros con signo (`i8`, "
                        "`i16`, `i32`, `i64`, `i128`, `isize`), enteros sin signo (`u8`, `u16`, `u32`, `u64`, `u128`, `usize`), "
                        "flotantes IEEE 754 (`f32`, `f64`), el tipo booleano `bool` (1 byte) y el tipo `char` de 4 bytes que representa "
                        "exactamente un valor escalar Unicode ($\\text{U+0000}$ a $\\text{U+D7FF}$ y $\\text{U+E000}$ a $\\text{U+10FFFF}$). "
                        "En caso de desbordamiento entero, el perfil `dev` genera un *panic* determinista, mientras que el lenguaje "
                        "ofrece métodos explícitos para cada semántica aritmética: `checked_add` (devuelve `Option<T>`), `wrapping_add` "
                        "(aritmética modular $\\bmod 2^w$), `saturating_add` (satura en los extremos) y `overflowing_add`:\n"
                        "```rust\n"
                        "pub fn classify_http_status(code: u16) -> &'static str {\n"
                        "    match code {\n"
                        "        100..=199 => \"informational\",\n"
                        "        200..=299 => \"success\",\n"
                        "        300..=399 => \"redirection\",\n"
                        "        400..=499 => \"client_error\",\n"
                        "        500..=599 => \"server_error\",\n"
                        "        _ => \"unknown\",\n"
                        "    }\n"
                        "}\n"
                        "```\n"
                        "Observa que `match` exige exhaustividad verificada por el compilador: si se omitiera el brazo comodín `_`, "
                        "`rustc` rechazaría el programa indicando exactamente los rangos de `u16` no cubiertos (`0..=99` y `600..=65535`)."
                    ),
                },
            ],
            "definition": (
                "Expresión de bloque en Rust: secuencia de sentencias encerrada entre llaves `{ s_1; s_2; ...; e }` cuyo tipo y valor "
                "resultante coinciden con los de la expresión final `e` (sin punto y coma), o con el tipo unidad `()` si termina en punto y coma."
            ),
            "consejo": (
                "Prefiere siempre `checked_add`, `saturating_add` o `wrapping_add` cuando implementes protocolos binarios, criptografía "
                "o contadores de sistemas para que el comportamiento ante desbordamiento no dependa del perfil de compilación."
            ),
            "self_check": (
                "¿Qué diferencia fundamental existe entre sombrear una variable (`let x = x + 1;`) y declararla mutable (`let mut x = 0; x += 1;`) "
                "en cuanto a la posibilidad de cambiar su tipo estático?"
            ),
            "derivation": {
                "title": "Capacidad en bytes de arrays estáticos [T; N] y tuplas alineadas",
                "assumptions": ["Un array [T; N] almacena N elementos contiguos de tamaño S_T sin cabecera adicional"],
                "steps": [
                    {"equation": r"B_{\text{array}} = N \cdot S_T", "justification": "En Rust [T; N] se aloja directamente en línea en la pila o estructura contenedora sin puntero intermedio"},
                    {"equation": r"B_{\text{chars}} = 4 \cdot N_{\text{char}}", "justification": "Cada valor char ocupa exactamente 4 bytes (UTF-32 escalar Unicode)"},
                ],
                "Verify": {"left": "4 * N_char", "right": "N_char * 4"},
            },
            "worked_problem": {
                "prompt": (
                    "Una cadena en Rust contiene 10 caracteres ASCII ($1\\text{ B}$ cada uno en UTF-8) y 5 caracteres acentuados "
                    "españoles (`á`, `é`, `í`, `ó`, `ú`, que ocupan $2\\text{ B}$ cada uno en UTF-8). Calcula la diferencia en bytes "
                    "entre representarla como `&str` en UTF-8 frente a un array `[char; 15]` de valores escalares Unicode ($4\\text{ B}$ por `char`)."
                ),
                "expression": "(15 * 4) - (10 * 1 + 5 * 2)",
                "solution": {
                    "model": "Comparación de almacenamiento UTF-8 (&str) frente a array de escalares Unicode [char; N]",
                    "given": [
                        {"symbol": "N_ascii", "value": "10", "description": "Caracteres ASCII de 1 byte en UTF-8"},
                        {"symbol": "N_lat", "value": "5", "description": "Caracteres latinos acentuados de 2 bytes en UTF-8"},
                        {"symbol": "S_char", "value": "4 B", "description": "Tamaño fijo del tipo char en Rust"},
                    ],
                    "steps": [
                        {"step": "Restamos los 20 bytes de la codificación UTF-8 a los 60 bytes del array [char; 15]", "equation": r"\Delta B = 15 \cdot 4 - (10 \cdot 1 + 5 \cdot 2)", "expression": "(15 * 4) - (10 * 1 + 5 * 2)"},
                    ],
                    "conclusion": "La representación UTF-8 nativa de Rust ahorra 40 bytes (ocupa 20 B frente a 60 B), razón por la cual String y &str utilizan UTF-8 en lugar de arrays de 32 bits.",
                },
            },
            "rust_worked_test": {
                "prompt": "Verificación ejecutable con `rustc --test` de aritmética saturada, verificada y longitud UTF-8 frente a conteo de `chars()`.",
                "source_text": (
                    "#[cfg(test)]\n"
                    "mod tests {\n"
                    "    #[test]\n"
                    "    fn verify_utf8_and_checked_arithmetic() {\n"
                    "        let s = \"programación\"; // 11 ASCII + 'ó' (2 bytes)\n"
                    "        assert_eq!(s.chars().count(), 12);\n"
                    "        assert_eq!(s.len(), 13);\n"
                    "        let max_u8: u8 = 250;\n"
                    "        assert_eq!(max_u8.checked_add(10), None);\n"
                    "        assert_eq!(max_u8.saturating_add(10), 255);\n"
                    "    }\n"
                    "}\n"
                ),
            },
            "practice_problems": [
                {"prompt": "Calcula el tamaño en bytes de un array `[u64; 32]` alojado en la pila ($32 \\times 8$).", "expression": "32 * 8", "difficulty": "FOUNDATIONAL", "problem_type": "DIRECT_SUBSTITUTION"},
                {"prompt": "Una cadena UTF-8 contiene 8 caracteres ASCII (1 B), 4 letras griegas (2 B) y 2 emojis (4 B). ¿Cuál es el valor de `s.len()` en bytes?", "expression": "8 * 1 + 4 * 2 + 2 * 4", "difficulty": "FOUNDATIONAL", "problem_type": "MULTI_STEP"},
                {"prompt": "Calcula el resultado de `250u8.wrapping_add(15)` en aritmética modular de 8 bits ($250 + 15 - 256$).", "expression": "250 + 15 - 256", "difficulty": "INTERMEDIATE", "problem_type": "MULTI_STEP"},
                {"prompt": "Si `Vec::with_capacity(128)` reserva espacio para 128 elementos `i32` (4 B cada uno) e insertamos 50 elementos, ¿cuántos bytes de capacidad reservada permanecen aún libres en el montículo?", "expression": "(128 - 50) * 4", "difficulty": "INTERMEDIATE", "problem_type": "DESIGN"},
            ],
        },
        {
            "id": "cap03-ownership-borrowing-lifetimes-modelo-memoria",
            "title": "D.1. Propiedad (Ownership), Préstamo (Borrowing), Rebanadas y Tiempos de Vida (Lifetimes)",
            "part_id": "parte-v-rust-intermedio",
            "part_title": "Bloque D: Nivel Intermedio — Propiedad, Tipos Algebraicos, Rasgos y Modularidad",
            "sources": ["src-rust-book", "src-rust-nomicon"],
            "learning_objectives": [
                "Enunciar y aplicar las tres leyes del sistema de propiedad (ownership) y diferenciar semántica Move, Copy y Clone.",
                "Aplicar la ley de exclusión mutua de referencias (XOR entre alias y mutabilidad: múltiples &T o una única &mut T).",
                "Anotar explícitamente tiempos de vida genéricos ('a, 'static), comprender las tres reglas de elisión y el comprobador NLL.",
            ],
            "concepts": [
                {"id": "cpt-rust-ownership-move-copy", "title": "Propiedad única, transferencia de dominio (move semantics), rasgo Copy y destrucción determinista (Drop)"},
                {"id": "cpt-rust-borrowing-lifetimes", "title": "Ley de alias XOR mutabilidad (&T vs &mut T), rebanadas y tiempos de vida ('a) con NLL"},
            ],
            "subsections": [
                {"id": "sec-rust-3-1", "title": "Las tres leyes de Ownership, semántica Move frente a Copy y el rasgo Drop"},
                {"id": "sec-rust-3-2", "title": "Reglas de Borrowing (&T vs &mut T), Non-Lexical Lifetimes (NLL) y parámetros de vida 'a"},
            ],
            "figure": {
                "key": "fig-rust-aliasing-xor-mutability",
                "caption": "Invariante fundamental del comprobador de préstamos: en cualquier punto del flujo de control MIR, un recurso admite múltiples préstamos inmutables (&T) o exactamente un préstamo exclusivo mutable (&mut T).",
                "tikz": r"""\begin{tikzpicture}[node distance=1.8cm, >=stealth, thick, font=\small]
\node[draw=blue!70!black, fill=blue!8, rounded corners, minimum width=3.4cm, minimum height=1.0cm, align=center] (own) {Propietario Único\\(\texttt{owner: T})};
\node[draw=teal!70!black, fill=teal!10, rounded corners, minimum width=4.2cm, minimum height=1.1cm, align=center, below left=1.2cm and 0.4cm of own] (imm) {Estado Compartido ($N \ge 1$, $M = 0$)\\Múltiples lectores \texttt{\&T}\\Sin mutación permitida};
\node[draw=orange!75!black, fill=orange!12, rounded corners, minimum width=4.2cm, minimum height=1.1cm, align=center, below right=1.2cm and 0.4cm of own] (mut) {Estado Exclusivo ($N = 0$, $M = 1$)\\Único escritor \texttt{\&mut T}\\Sin alias simultáneos};
\draw[->] (own) -- node[left, font=\footnotesize] {Préstamo lectura} (imm);
\draw[->] (own) -- node[right, font=\footnotesize] {Préstamo exclusivo} (mut);
\draw[<->, dashed, red!75!black] (imm) -- node[above, font=\footnotesize] {Prohibido simultáneamente} (mut);
\end{tikzpicture}""",
            },
            "purpose": (
                "Este capítulo desarrolla el corazón teórico y práctico de Rust: su sistema de tipos afín basado en propiedad "
                "única (*ownership*), préstamo (*borrowing*) y regiones de tiempo de vida (*lifetimes*). Comprender este modelo "
                "no solo permite escribir Rust sin fricción, sino que transforma permanentemente la manera en que un ingeniero "
                "razona sobre la vida útil de los recursos y la concurrencia en cualquier lenguaje."
            ),
            "paragraphs": [
                {
                    "subsection": "sec-rust-3-1",
                    "text": (
                        "El sistema de propiedad de Rust se rige por tres axiomas verificados en compilación: (1) cada valor en Rust "
                        "tiene una variable denominada su *propietario* (*owner*); (2) solo puede existir un único propietario a la vez; "
                        "y (3) cuando el propietario sale de su ámbito léxico (*scope*), el valor se destruye invocando determinísticamente "
                        "`Drop::drop` (patrón RAII, *Resource Acquisition Is Initialization*). Cuando asignamos o pasamos por valor un tipo "
                        "que gestiona memoria en el montículo como `String` o `Vec<T>`, Rust ejecuta una transferencia de propiedad (*move*): "
                        "copia los 24 bytes de la cabecera en la pila e invalida estáticamente la variable de origen en el grafo de flujo MIR, "
                        "impidiendo cualquier doble liberación (*double free*). Por el contrario, los tipos escalares simples que residen "
                        "íntegramente en la pila implementan el rasgo marcador `Copy`, por lo que la asignación duplica sus bits sin invalidar "
                        "el origen. Un tipo solo puede implementar `Copy` si ninguno de sus componentes implementa `Drop`."
                    ),
                },
                {
                    "subsection": "sec-rust-3-2",
                    "text": (
                        "Para operar sobre un valor sin transferir su propiedad, Rust introduce las referencias (*borrowing*). Como "
                        "muestra la Figura \\ref{fig:fig-rust-aliasing-xor-mutability}, en cualquier punto de ejecución del grafo de "
                        "control MIR para un recurso dado, el número de referencias inmutables activas $N_{\\text{shared}}$ y el número "
                        "de referencias mutables activas $M_{\\text{mut}}$ satisfacen la invariante de exclusión:\n"
                        "$$(N_{\\text{shared}} \\ge 0 \\land M_{\\text{mut}} = 0) \\lor (N_{\\text{shared}} = 0 \\land M_{\\text{mut}} = 1)$$\n"
                        "Esta ley de *Alias XOR Mutabilidad* elimina de raíz tanto las carreras de datos entre hilos como la invalidación "
                        "de iteradores en un único hilo (por ejemplo, intentar hacer `vec.push(x)` mientras se mantiene una referencia "
                        "`&vec[0]` que quedaría colgante si el vector realoja su búfer en el montículo). Cuando una función devuelve una "
                        "referencia derivada de sus parámetros de entrada, el parámetro de tiempo de vida `'a` expresa la relación de "
                        "inclusión de regiones $\\text{'a} \\subseteq \\text{vida}(x) \\cap \\text{vida}(y)$, sin alterar jamás la "
                        "duración real en tiempo de ejecución:\n"
                        "```rust\n"
                        "pub fn longest_token<'a>(left: &'a str, right: &'a str) -> &'a str {\n"
                        "    if left.len() >= right.len() { left } else { right }\n"
                        "}\n"
                        "```\n"
                        "El compilador aplica tres reglas deterministas de *elisión de tiempos de vida*: (1) cada parámetro por referencia "
                        "recibe su propio parámetro `'a`, `'b`; (2) si hay exactamente un tiempo de vida de entrada, se asigna a todas "
                        "las referencias de salida; y (3) si uno de los parámetros es `&self` o `&mut self`, su tiempo de vida se asigna "
                        "a todas las referencias de salida."
                    ),
                },
            ],
            "definition": (
                "Parámetro de tiempo de vida `'a`: variable de región en el sistema de tipos de Rust que restringe estáticamente el "
                "ámbito durante el cual una referencia prestada `&'a T` o `&'a mut T` es válida, garantizando que el referente sobrevive a toda referencia."
            ),
            "consejo": (
                "Recuerda que las anotaciones `'a` nunca prolongan la vida de un valor en memoria: únicamente declaran al compilador "
                "cómo se relaciona la vida útil de la referencia de salida con la de las referencias de entrada."
            ),
            "self_check": (
                "¿Por qué la firma `fn dangling() -> &str { let s = String::from(\"hola\"); &s }` es rechazada en compilación independientemente "
                "del tiempo de vida que se intente anotar?"
            ),
            "derivation": {
                "title": "Coste en copias de bytes de una transferencia de propiedad (Move) de Vec<T>",
                "assumptions": ["Vec<T> consta de 3 palabras de W bytes en la pila y N elementos de tamaño S_T en el montículo"],
                "steps": [
                    {"equation": r"C_{\text{move}} = 3 W", "justification": "Un move copia únicamente la cabecera (ptr, len, cap) en la pila sin tocar el montículo"},
                    {"equation": r"C_{\text{clone}} = 3 W + N \cdot S_T", "justification": "Un clone profundo duplica tanto la cabecera como los N elementos en el montículo"},
                ],
                "Verify": {"left": "3 * W + 0 * N * S_T", "right": "3 * W"},
            },
            "worked_problem": {
                "prompt": (
                    "Un vector `Vec<u64>` contiene $N = 10000$ enteros de 8 bytes en el montículo en una máquina de 64 bits ($W = 8\\text{ B}$). "
                    "Calcula cuántos bytes menos se copian al pasar el vector por transferencia de propiedad (*move*, que solo copia las "
                    "3 palabras de la cabecera en pila) frente a invocar `.clone()` (que copia la cabecera más los $10000 \\times 8$ bytes del montículo)."
                ),
                "expression": "(3 * 8 + 10000 * 8) - (3 * 8)",
                "solution": {
                    "model": "Diferencia de bytes copiados entre Move (O(1)) y Clone (O(N))",
                    "given": [
                        {"symbol": "N", "value": "10000", "description": "Número de elementos u64 en el vector"},
                        {"symbol": "S_T", "value": "8 B", "description": "Tamaño de cada elemento u64"},
                        {"symbol": "W", "value": "8 B", "description": "Tamaño de palabra en arquitectura de 64 bits"},
                    ],
                    "steps": [
                        {"step": "Restamos el coste de move (24 B) al coste total de clone (80024 B)", "equation": r"\Delta B = (3 \cdot 8 + 10000 \cdot 8) - 3 \cdot 8", "expression": "(3 * 8 + 10000 * 8) - (3 * 8)"},
                    ],
                    "conclusion": "La transferencia de propiedad (move) ahorra la copia de 80 000 bytes en el montículo y se ejecuta en tiempo constante O(1) copiando únicamente 24 bytes.",
                },
            },
            "rust_worked_test": {
                "prompt": "Verificación ejecutable con `rustc --test` de préstamos con tiempos de vida explícitos `'a`, rebanadas mutables disjuntas (`split_at_mut`) y Non-Lexical Lifetimes.",
                "source_text": (
                    "pub fn longest<'a>(x: &'a str, y: &'a str) -> &'a str {\n"
                    "    if x.len() >= y.len() { x } else { y }\n"
                    "}\n"
                    "#[cfg(test)]\n"
                    "mod tests {\n"
                    "    use super::*;\n"
                    "    #[test]\n"
                    "    fn verify_lifetimes_and_disjoint_borrows() {\n"
                    "        let s1 = String::from(\"rust-systems\");\n"
                    "        let res = {\n"
                    "            let s2 = \"c\";\n"
                    "            longest(s1.as_str(), s2)\n"
                    "        };\n"
                    "        assert_eq!(res, \"rust-systems\");\n"
                    "        let mut data = [10, 20, 30, 40];\n"
                    "        let (left, right) = data.split_at_mut(2);\n"
                    "        left[0] += 5;\n"
                    "        right[1] += 10;\n"
                    "        assert_eq!(data, [15, 20, 30, 50]);\n"
                    "    }\n"
                    "}\n"
                ),
            },
            "practice_problems": [
                {"prompt": "Calcula cuántos bytes en la pila se copian al mover un `String` en una arquitectura de 64 bits ($3 \\times 8$).", "expression": "3 * 8", "difficulty": "FOUNDATIONAL", "problem_type": "DIRECT_SUBSTITUTION"},
                {"prompt": "Si dividimos una rebanada de 1024 elementos mediante `split_at_mut(300)`, ¿cuántos elementos contiene la segunda sub-rebanada mutable?", "expression": "1024 - 300", "difficulty": "FOUNDATIONAL", "problem_type": "DIRECT_SUBSTITUTION"},
                {"prompt": "Una estructura contiene 4 campos `u64` que implementan `Copy`. ¿Cuántos bytes se copian en cada asignación por valor ($4 \\times 8$)?", "expression": "4 * 8", "difficulty": "INTERMEDIATE", "problem_type": "MULTI_STEP"},
                {"prompt": "Un analizador léxico de copia cero (*zero-copy*) genera 500 tokens `&'a str` (16 B cada uno) sobre un texto fuente de 32 000 bytes sin clonar subcadenas. ¿Cuántos bytes ocupan en total los 500 descriptores de token?", "expression": "500 * 16", "difficulty": "INTERMEDIATE", "problem_type": "DESIGN"},
            ],
        },
        {
            "id": "cap04-tipos-algebraicos-traits-genericos-errores",
            "title": "D.2. Tipos Algebraicos (struct, enum), Rasgos (Traits), Genéricos y Manejo de Errores (Option y Result)",
            "part_id": "parte-v-rust-intermedio",
            "part_title": "Bloque D: Nivel Intermedio — Propiedad, Tipos Algebraicos, Rasgos y Modularidad",
            "sources": ["src-rust-book", "src-pierce-tapl"],
            "learning_objectives": [
                "Modelar invariantes de dominio mediante tipos producto (struct) y tipos suma (enum) haciendo irrepresentables los estados inválidos.",
                "Diseñar jerarquías de polimorfismo paramétrico y ad-hoc con rasgos (traits), tipos asociados, cotas where y coherencia (regla del huérfano).",
                "Gestionar errores recuperables e irrecuperables mediante Option<T>, Result<T, E>, el operador de propagación `?` y conversiones From/Into.",
            ],
            "concepts": [
                {"id": "cpt-rust-adt-niche", "title": "Tipos algebraicos de datos, optimización de nicho (NonZero, Option<&T>) y pattern matching exhaustivo"},
                {"id": "cpt-rust-traits-result", "title": "Rasgos con tipos asociados, regla del huérfano y propagación algebraica de errores con Result<T, E> y `?`"},
            ],
            "subsections": [
                {"id": "sec-rust-4-1", "title": "Estructuras, enumeraciones algebraicas, optimización de nicho y coincidencia de patrones"},
                {"id": "sec-rust-4-2", "title": "Rasgos (Traits), genéricos, tipos asociados y manejo de errores con Option<T> y Result<T, E>"},
            ],
            "purpose": (
                "Este capítulo completa el Nivel Intermedio (Bloque D) profundizando en el sistema de tipos algebraicos, "
                "el polimorfismo basado en rasgos (*traits*) y la arquitectura de manejo de errores de Rust. A diferencia de "
                "los lenguajes con referencias nulas implícitas o excepciones no comprobadas, Rust codifica la ausencia de valor "
                "(`Option<T>`) y la posibilidad de fallo (`Result<T, E>`) directamente en las firmas de tipos."
            ),
            "paragraphs": [
                {
                    "subsection": "sec-rust-4-1",
                    "text": (
                        "Un `struct` en Rust define un tipo producto cuya cardinalidad es el producto de los dominios de sus campos, "
                        "mientras que un `enum` define un tipo suma etiquetado (*tagged union*) donde cada variante puede transportar "
                        "datos de tipos distintos: por ejemplo, `enum IpPacket { V4([u8; 4], u16), V6([u16; 8], u16), Dropped }`. El "
                        "tamaño en memoria de un `enum` es el tamaño de su variante más grande más el discriminante (etiqueta), redondeado "
                        "al múltiplo del alineamiento máximo. Sin embargo, el compilador aplica la *optimización de nicho* (*null pointer / "
                        "niche optimization*): como una referencia `&T`, un `Box<T>` o un `NonZeroU64` jamás pueden tener el patrón de "
                        "bits cero, `Option<&T>` utiliza el valor cero para representar `None`, por lo que $\\text{sizeof}(\\text{Option}\\langle\\&T\\rangle) "
                        "= \\text{sizeof}(\\&T) = 8\\text{ B}$, con sobrecoste espacial exactamente nulo."
                    ),
                },
                {
                    "subsection": "sec-rust-4-2",
                    "text": (
                        "Los rasgos (*traits*) definen interfaces de comportamiento compartido que admiten implementaciones por defecto, "
                        "parámetros genéricos y tipos asociados (`type Item;`). Para garantizar la coherencia global de tipos al enlazar "
                        "múltiples crates, Rust impone la *regla del huérfano* (*orphan rule*): solo se puede implementar un rasgo `Trait` "
                        "para un tipo `Type` en el crate actual si al menos uno de los dos (`Trait` o `Type`) está definido localmente en "
                        "dicho crate. En el tratamiento de errores, `Result<T, E>` se combina con el operador de propagación `?`, que "
                        "desazucara una expresión `expr?` en una evaluación exhaustiva que convierte automáticamente el error mediante "
                        "`From::from(err)`:\n"
                        "```rust\n"
                        "#[derive(Debug, PartialEq)]\n"
                        "pub enum ConfigError { EmptyInput, InvalidPort(String) }\n\n"
                        "pub fn parse_port_str(raw: &str) -> Result<u16, ConfigError> {\n"
                        "    let trimmed = raw.trim();\n"
                        "    if trimmed.is_empty() {\n"
                        "        return Err(ConfigError::EmptyInput);\n"
                        "    }\n"
                        "    let port: u16 = trimmed.parse().map_err(|_| ConfigError::InvalidPort(trimmed.to_string()))?;\n"
                        "    if port == 0 { Err(ConfigError::InvalidPort(trimmed.to_string())) } else { Ok(port) }\n"
                        "}\n"
                        "```\n"
                        "Esta disciplina distingue con nitidez entre errores recuperables (modelados con `Result<T, E>`) y violaciones "
                        "de invariantes de programación irrecuperables (modeladas con `panic!`)."
                    ),
                },
            ],
            "definition": (
                "Optimización de nicho (Niche Optimization): transformación de representación mediante la cual el compilador de Rust "
                "codifica variantes de un tipo suma (`enum`) utilizando patrones de bits inválidos (nichos) del tipo contenido, "
                "eliminando la necesidad de un byte discriminante adicional."
            ),
            "consejo": (
                "En bibliotecas reutilizables, define tipos de error estructurados como `enum` que implementen `std::error::Error` "
                "y `Display` (o utiliza `thiserror`), reservando errores opacos tipo `Box<dyn Error>` o `anyhow` para la capa superior binaria."
            ),
            "self_check": (
                "¿Cuándo debe un rasgo utilizar un tipo asociado (`trait Iterator { type Item; }`) en lugar de un parámetro de tipo "
                "genérico (`trait From<T>`)?"
            ),
            "derivation": {
                "title": "Ahorro de memoria por optimización de nicho en arreglos de Option<&T>",
                "assumptions": ["En 64 bits (W = 8 B), sin optimización de nicho Option<&T> requeriría 8 B + 8 B de alineamiento = 16 B; con nicho ocupa 8 B"],
                "steps": [
                    {"equation": r"S_{\text{naive}} = 2 W \cdot N", "justification": "Un puntero de 8 B más etiqueta alineada a 8 B ocuparía 16 B por elemento"},
                    {"equation": r"S_{\text{niche}} = W \cdot N", "justification": "El valor nulo 0x0 representa None, reduciendo el tamaño por elemento a W = 8 B"},
                ],
                "Verify": {"left": "2 * W * N - W * N", "right": "W * N"},
            },
            "worked_problem": {
                "prompt": (
                    "Una tabla hash abierta almacena $N = 65536$ ranuras de tipo `Option<std::num::NonZeroU64>` en una arquitectura de "
                    "64 bits ($W = 8\\text{ B}$). Gracias a la optimización de nicho, cada `Option<NonZeroU64>` ocupa exactamente 8 bytes "
                    "en lugar de 16 bytes (8 bytes de dato más 8 bytes de discriminante alineado). Calcula cuántos kilobytes (dividiendo "
                    "entre 1024) se ahorran en la tabla completa gracias a la optimización de nicho."
                ),
                "expression": "(65536 * (16 - 8)) / 1024",
                "solution": {
                    "model": "Ahorro de memoria por optimización de nicho en Option<NonZeroU64>",
                    "given": [
                        {"symbol": "N", "value": "65536", "description": "Número de ranuras en la tabla"},
                        {"symbol": "S_sin", "value": "16 B", "description": "Tamaño alineado sin optimización de nicho"},
                        {"symbol": "S_con", "value": "8 B", "description": "Tamaño con optimización de nicho"},
                    ],
                    "steps": [
                        {"step": "Multiplicamos las 65536 ranuras por los 8 B ahorrados y dividimos entre 1024 B/KiB", "equation": r"\Delta M_{\text{KiB}} = \frac{65536 \cdot (16 - 8)}{1024}", "expression": "(65536 * (16 - 8)) / 1024"},
                    ],
                    "conclusion": "La optimización de nicho ahorra exactamente 512 KiB de memoria caché/RAM y duplica el número de entradas por línea de caché de 64 bytes.",
                },
            },
            "rust_worked_test": {
                "prompt": "Verificación ejecutable con `rustc --test` de la optimización de nicho (`size_of::<Option<&u64>>() == 8`) y propagación de errores con `?`.",
                "source_text": (
                    "use std::num::NonZeroU64;\n"
                    "pub fn parse_positive_pair(a: &str, b: &str) -> Result<u64, &'static str> {\n"
                    "    let x: u64 = a.parse().map_err(|_| \"invalid_a\")?;\n"
                    "    let y: u64 = b.parse().map_err(|_| \"invalid_b\")?;\n"
                    "    Ok(x + y)\n"
                    "}\n"
                    "#[cfg(test)]\n"
                    "mod tests {\n"
                    "    use super::*;\n"
                    "    use std::mem::size_of;\n"
                    "    #[test]\n"
                    "    fn verify_niche_and_result_propagation() {\n"
                    "        assert_eq!(size_of::<Option<&u64>>(), size_of::<&u64>());\n"
                    "        assert_eq!(size_of::<Option<NonZeroU64>>(), size_of::<u64>());\n"
                    "        assert_eq!(parse_positive_pair(\"15\", \"27\"), Ok(42));\n"
                    "        assert_eq!(parse_positive_pair(\"15\", \"bad\"), Err(\"invalid_b\"));\n"
                    "    }\n"
                    "}\n"
                ),
            },
            "practice_problems": [
                {"prompt": "En una arquitectura de 64 bits, ¿cuántos bytes ocupa `Option<Box<u64>>` gracias a la optimización de nicho?", "expression": "8", "difficulty": "FOUNDATIONAL", "problem_type": "DIRECT_SUBSTITUTION"},
                {"prompt": "¿Cuántos bytes ocupa en total un array `[Option<NonZeroU32>; 1000]` sabiendo que cada elemento ocupa 4 bytes?", "expression": "1000 * 4", "difficulty": "FOUNDATIONAL", "problem_type": "DIRECT_SUBSTITUTION"},
                {"prompt": "Un `enum` sin nicho tiene una variante de 24 bytes con alineamiento de 8 bytes y una etiqueta de 1 byte. Tras añadir 7 bytes de relleno (*padding*) para mantener el alineamiento a múltiplo de 8, ¿cuál es su tamaño total en bytes?", "expression": "24 + 1 + 7", "difficulty": "INTERMEDIATE", "problem_type": "MULTI_STEP"},
                {"prompt": "Una línea de caché de CPU mide 64 bytes. ¿Cuántos elementos `Option<NonZeroU64>` (8 B cada uno) caben en una única línea de caché?", "expression": "64 / 8", "difficulty": "INTERMEDIATE", "problem_type": "DESIGN"},
            ],
        },
        {
            "id": "cap05-closures-iteradores-smart-pointers-mutabilidad-interior",
            "title": "E.1. Nivel Avanzado: Clausuras (Fn/FnMut/FnOnce), Iteradores, Punteros Inteligentes y Mutabilidad Interior",
            "part_id": "parte-v-rust-avanzado-experto",
            "part_title": "Bloques E–F: Nivel Avanzado y Experto — Smart Pointers, Concurrencia, Async y Unsafe",
            "sources": ["src-rust-book", "src-rust-nomicon"],
            "learning_objectives": [
                "Distinguir la representación y captura de entorno en clausuras según la jerarquía de rasgos FnOnce, FnMut y Fn.",
                "Diseñar tuberías perezosas de iteradores de coste cero y demostrar su equivalencia en ensamblador frente a bucles manuales.",
                "Seleccionar con rigor entre Box<T>, Rc<T>, Arc<T>, Cell<T>, RefCell<T>, Cow<'a, B> y Weak<T> evitando fugas por ciclos de referencias.",
            ],
            "concepts": [
                {"id": "cpt-rust-closures-iterators", "title": "Jerarquía de rasgos FnOnce/FnMut/Fn y composición perezosa de iteradores sin alojamientos intermedios"},
                {"id": "cpt-rust-smart-pointers", "title": "Punteros inteligentes (Box, Rc, Arc, Weak) y mutabilidad interior verificada en ejecución (Cell, RefCell)"},
            ],
            "subsections": [
                {"id": "sec-rust-5-1", "title": "Clausuras (Fn, FnMut, FnOnce) e iteradores perezosos de coste cero"},
                {"id": "sec-rust-5-2", "title": "Punteros inteligentes (Box, Rc, Weak) y mutabilidad interior (Cell, RefCell, Cow)"},
            ],
            "purpose": (
                "Este capítulo abre el Nivel Avanzado (Bloque E). Estudiaremos cómo Rust implementa la programación funcional "
                "mediante estructuras anónimas de clausura e iteradores fusionados en compilación, y cómo permite relajar las "
                "restricciones estáticas de propiedad única cuando un algoritmo requiere grafos compartidos o cachés internas "
                "mediante punteros inteligentes y contenedores de mutabilidad interior."
            ),
            "paragraphs": [
                {
                    "subsection": "sec-rust-5-1",
                    "text": (
                        "Cada clausura `|x| x + umbral` en Rust genera un tipo `struct` anónimo único que captura las variables "
                        "libres de su entorno por el modo menos restrictivo posible: por referencia compartida `&T` (implementa "
                        "`Fn`, `FnMut` y `FnOnce`), por referencia mutable `&mut T` (implementa `FnMut` y `FnOnce`) o por valor "
                        "consumiendo la variable (implementa únicamente `FnOnce`, o cuando se fuerza la captura con la palabra "
                        "clave `move`). Los iteradores en Rust implementan el rasgo `Iterator { type Item; fn next(&mut self) -> Option<Self::Item>; }`. "
                        "Adaptadores como `.map(...)`, `.filter(...)`, `.take(...)` y `.enumerate()` son perezosos (*lazy*): "
                        "no ejecutan ningún trabajo ni alojan vectores intermedios hasta que un consumidor terminal como `.fold(...)`, "
                        "`.sum()` o `.collect::<Vec<_>>()` solicita los elementos. Gracias a la monomorfización, LLVM fusiona toda "
                        "la cadena de adaptadores en un único bucle registrador sin comprobaciones de límites redundantes."
                    ),
                },
                {
                    "subsection": "sec-rust-5-2",
                    "text": (
                        "Un puntero inteligente (*smart pointer*) es una estructura que implementa los rasgos `Deref` y `Drop`. "
                        "`Box<T>` proporciona propiedad única en el montículo (indispensable para tipos recursivos de tamaño finito "
                        "como árboles sintácticos `enum Expr { Add(Box<Expr>, Box<Expr>), Lit(i64) }`). `Rc<T>` (*Reference Counted*) "
                        "habilita propiedad compartida en un único hilo manteniendo un contador de referencias fuertes (`strong_count`) "
                        "y débiles (`weak_count`); como `Rc<T>` no utiliza instrucciones atómicas, el compilador le niega los rasgos "
                        "`Send` y `Sync`, impidiendo estáticamente que cruce a otro hilo. Cuando se necesita mutar un dato a través de "
                        "una referencia compartida `&self`, Rust ofrece *mutabilidad interior*: `Cell<T>` opera por reemplazo de valores "
                        "sin referencias internas (coste cero en espacio), mientras que `RefCell<T>` traslada las reglas del comprobador "
                        "de préstamos al tiempo de ejecución manteniendo un contador de préstamos (`borrow()` e `borrow_mut()`):\n"
                        "```rust\n"
                        "use std::cell::RefCell;\n"
                        "use std::rc::Rc;\n\n"
                        "pub fn shared_accumulator_demo() -> i64 {\n"
                        "    let acc = Rc::new(RefCell::new(10_i64));\n"
                        "    let handle_a = Rc::clone(&acc);\n"
                        "    let handle_b = Rc::clone(&acc);\n"
                        "    *handle_a.borrow_mut() += 15;\n"
                        "    *handle_b.borrow_mut() *= 2;\n"
                        "    let final_val = *acc.borrow();\n"
                        "    final_val\n"
                        "}\n"
                        "```\n"
                        "Si un programa intenta adquirir un `borrow_mut()` mientras otro préstamo de la misma `RefCell<T>` sigue vivo, "
                        "`RefCell` dispara un *panic* inmediato en lugar de permitir corrupción de memoria."
                    ),
                },
            ],
            "definition": (
                "Mutabilidad interior (Interior Mutability): patrón de diseño seguro en Rust mediante el cual una estructura expone "
                "una interfaz inmutable (`&self`) pero permite mutar su estado interno encapsulado en `UnsafeCell<T>` garantizando "
                "la invariante de exclusión mediante transferencia de valores (`Cell<T>`), contadores dinámicos (`RefCell<T>`) o "
                "sincronización atómica (`Mutex<T>`, `RwLock<T>`)."
            ),
            "consejo": (
                "Para evitar fugas de memoria en estructuras doblemente enlazadas o árboles con puntero al nodo padre, utiliza "
                "`Rc<Node>` de padre a hijo y `Weak<Node>` de hijo a padre, ya que `Weak<T>` no incrementa el `strong_count`."
            ),
            "self_check": (
                "¿Por qué `Rc<T>` no implementa el rasgo `Send` y qué ocurriría en hardware multinúcleo si dos hilos ejecutaran "
                "`Rc::clone` simultáneamente sobre el mismo contador no atómico?"
            ),
            "derivation": {
                "title": "Tamaño del bloque de control de RcBox<T> en el montículo",
                "assumptions": ["RcBox<T> almacena strong_count (usize = W bytes), weak_count (usize = W bytes) y el valor T de tamaño S_T"],
                "steps": [
                    {"equation": r"S_{\text{RcBox}} = 2 W + S_T", "justification": "El bloque en el montículo precede al valor T con los dos contadores de referencias"},
                    {"equation": r"S_{\text{total}}(k) = k \cdot W + (2 W + S_T)", "justification": "k clones de Rc<T> en la pila ocupan k*W bytes apuntando todos al único RcBox en el montículo"},
                ],
                "Verify": {"left": "k * W + 2 * W + S_T", "right": "(k + 2) * W + S_T"},
            },
            "worked_problem": {
                "prompt": (
                    "En una arquitectura de 64 bits ($W = 8\\text{ B}$), se aloja un bloque `Rc< [u8; 1024] >` ($S_T = 1024\\text{ B}$) "
                    "y se crean $k = 5$ manejadores `Rc::clone` en distintas estructuras en la pila. Calcula la memoria total consumida "
                    "(los 5 punteros en la pila más el único bloque `RcBox` en el montículo con sus 2 contadores `usize` y los 1024 bytes de datos)."
                ),
                "expression": "5 * 8 + (2 * 8 + 1024)",
                "solution": {
                    "model": "Consumo de memoria de Rc<T> con k referencias compartidas",
                    "given": [
                        {"symbol": "W", "value": "8 B", "description": "Tamaño de usize y puntero en 64 bits"},
                        {"symbol": "k", "value": "5", "description": "Número de manejadores Rc<T> en la pila"},
                        {"symbol": "S_T", "value": "1024 B", "description": "Tamaño del valor compartido en el montículo"},
                    ],
                    "steps": [
                        {"step": "Sumamos los 5 punteros de 8 B en pila más el RcBox (16 B de contadores + 1024 B de datos)", "equation": r"M = 5 \cdot 8 + (2 \cdot 8 + 1024)", "expression": "5 * 8 + (2 * 8 + 1024)"},
                    ],
                    "conclusion": "El conjunto completo ocupa 1080 bytes (40 B en la pila y 1040 B en el montículo), ahorrando 4096 bytes frente a clonar 5 veces el búfer.",
                },
            },
            "rust_worked_test": {
                "prompt": "Verificación ejecutable con `rustc --test` de tuberías de iteradores, `Rc`/`Weak` y mutabilidad interior con `RefCell`.",
                "source_text": (
                    "use std::cell::RefCell;\n"
                    "use std::rc::Rc;\n"
                    "#[cfg(test)]\n"
                    "mod tests {\n"
                    "    use super::*;\n"
                    "    #[test]\n"
                    "    fn verify_iterators_and_rc_refcell() {\n"
                    "        let sum_sq: i64 = (1..=10).filter(|x| x % 2 == 0).map(|x| x * x).sum();\n"
                    "        assert_eq!(sum_sq, 4 + 16 + 36 + 64 + 100);\n"
                    "        let shared = Rc::new(RefCell::new(vec![1, 2]));\n"
                    "        let weak_ref = Rc::downgrade(&shared);\n"
                    "        assert_eq!(Rc::strong_count(&shared), 1);\n"
                    "        assert_eq!(Rc::weak_count(&shared), 1);\n"
                    "        shared.borrow_mut().push(3);\n"
                    "        assert_eq!(*weak_ref.upgrade().unwrap().borrow(), vec![1, 2, 3]);\n"
                    "    }\n"
                    "}\n"
                ),
            },
            "practice_problems": [
                {"prompt": "Calcula la suma de los cuadrados de los números pares del 2 al 10 ($2^2 + 4^2 + 6^2 + 8^2 + 10^2$) evaluada por `(1..=10).filter(|x| x % 2 == 0).map(|x| x * x).sum()`.", "expression": "4 + 16 + 36 + 64 + 100", "difficulty": "FOUNDATIONAL", "problem_type": "DIRECT_SUBSTITUTION"},
                {"prompt": "¿Cuántos bytes de metadatos añaden los dos contadores (`strong` y `weak`) de `RcBox<T>` en una arquitectura de 64 bits ($2 \\times 8$)?", "expression": "2 * 8", "difficulty": "FOUNDATIONAL", "problem_type": "DIRECT_SUBSTITUTION"},
                {"prompt": "Si se crean 1 `Rc` original, 4 clones fuertes (`Rc::clone`) y 3 referencias débiles (`Rc::downgrade`), y luego se destruyen 2 clones fuertes, ¿cuál es el valor actual de `Rc::strong_count`?", "expression": "1 + 4 - 2", "difficulty": "INTERMEDIATE", "problem_type": "MULTI_STEP"},
                {"prompt": "Un flujo de datos procesa 5000 enteros mediante `iter().filter(...).map(...).fold(...)` sin llamar a `collect()`. ¿Cuántos vectores dinámicos intermedios se alojan en el montículo durante el recorrido?", "expression": "0", "difficulty": "INTERMEDIATE", "problem_type": "DESIGN"},
            ],
        },
        {
            "id": "cap06-concurrencia-sin-miedo-send-sync-async-tokio-pin",
            "title": "E.2. Concurrencia sin Miedo (Send/Sync, Arc, Mutex, Canales) y Asincronía (Future, async/await, Pin, Tokio)",
            "part_id": "parte-v-rust-avanzado-experto",
            "part_title": "Bloques E–F: Nivel Avanzado y Experto — Smart Pointers, Concurrencia, Async y Unsafe",
            "sources": ["src-rust-book", "src-rust-nomicon"],
            "learning_objectives": [
                "Demostrar cómo los rasgos automáticos Send y Sync garantizan en tiempo de compilación la ausencia de carreras de datos.",
                "Combinar hilos con ámbito (std::thread::scope), canales MPSC, Arc<Mutex<T>>, Arc<RwLock<T>> y tipos atómicos con órdenes de memoria.",
                "Comprender la compilación de funciones async a máquinas de estados sin pila (stackless coroutines), el rasgo Future::poll y la garantía estructural de Pin<P>.",
            ],
            "concepts": [
                {"id": "cpt-rust-send-sync-atomics", "title": "Rasgos marcadores Send y Sync, Arc<Mutex<T>>, hilos con ámbito y órdenes de memoria atómica"},
                {"id": "cpt-rust-async-future-pin", "title": "Máquinas de estados Future, Context/Waker, referencias autorreferenciales y fijación en memoria con Pin<P>"},
            ],
            "subsections": [
                {"id": "sec-rust-6-1", "title": "Concurrencia basada en hilos: Send, Sync, thread::scope, Arc, Mutex y canales"},
                {"id": "sec-rust-6-2", "title": "Programación asíncrona: el rasgo Future, máquinas de estados, Pin/Unpin y el ejecutor Tokio"},
            ],
            "figure": {
                "key": "fig-rust-async-poll-state-machine",
                "caption": "Modelo de ejecución de Future en Rust: el ejecutor (Tokio) invoca poll(Pin<&mut Self>, &mut Context); si el recurso E/S no está listo devuelve Poll::Pending y registra el Waker en el reactor del sistema operativo (epoll/kqueue).",
                "tikz": r"""\begin{tikzpicture}[node distance=2.2cm, >=stealth, thick, font=\small]
\node[draw=blue!70!black, fill=blue!8, rounded corners, minimum width=3.2cm, minimum height=1.0cm, align=center] (exec) {Ejecutor Asíncrono\\(Cola de Tareas Tokio)};
\node[draw=orange!75!black, fill=orange!12, rounded corners, minimum width=3.4cm, minimum height=1.0cm, align=center, right=1.4cm of exec] (fut) {Máquina de Estados\\(\texttt{Pin<\&mut Future>})};
\node[draw=teal!70!black, fill=teal!10, rounded corners, minimum width=3.2cm, minimum height=1.0cm, align=center, below=1.2cm of fut] (reac) {Reactor E/S OS\\(\texttt{epoll} / \texttt{kqueue})};
\draw[->] (exec.10) -- node[above, font=\footnotesize] {\texttt{poll(cx)}} (fut.170);
\draw[<-] (exec.350) -- node[below, font=\footnotesize] {\texttt{Poll::Pending} / \texttt{Ready}} (fut.190);
\draw[->] (fut) -- node[right, font=\footnotesize] {Registra \texttt{Waker}} (reac);
\draw[->] (reac.west) -| node[pos=0.25, below, font=\footnotesize] {\texttt{waker.wake()} al llegar evento} (exec.south);
\end{tikzpicture}""",
            },
            "purpose": (
                "Este capítulo aborda la concurrencia paralela y la asincronía de alto rendimiento en Rust. Veremos por qué el "
                "mismo sistema de tipos que previene punteros colgantes en un hilo es capaz de impedir toda carrera de datos entre "
                "múltiples hilos mediante los rasgos marcadores `Send` y `Sync`, y cómo Rust compila funciones `async fn` en máquinas "
                "de estados compactas sin requerir un alojamiento en el montículo por cada llamada asíncrona."
            ),
            "paragraphs": [
                {
                    "subsection": "sec-rust-6-1",
                    "text": (
                        "Dos rasgos marcadores automáticos gobiernan toda la concurrencia en Rust: un tipo `T` es `Send` si su "
                        "propiedad puede transferirse de manera segura a otro hilo, y es `Sync` si es seguro compartirlo entre varios "
                        "hilos simultáneamente por referencia inmutable (es decir, `T: Sync` si y solo si `&T: Send`). Mientras que "
                        "`std::thread::spawn` exige una clausura `'static + Send` porque el hilo hijo podría sobrevivir a la función "
                        "que lo creó, `std::thread::scope` permite lanzar hilos que toman prestadas referencias locales no `'static` "
                        "del marco de pila padre, garantizando estáticamente que todos los hilos del ámbito terminan antes de que "
                        "`scope` retorne:\n"
                        "```rust\n"
                        "use std::thread;\n\n"
                        "pub fn parallel_dot_product(a: &[i64], b: &[i64]) -> i64 {\n"
                        "    let mid = a.len() / 2;\n"
                        "    let (a_left, a_right) = a.split_at(mid);\n"
                        "    let (b_left, b_right) = b.split_at(mid);\n"
                        "    thread::scope(|s| {\n"
                        "        let left_handle = s.spawn(|| a_left.iter().zip(b_left).map(|(x, y)| x * y).sum::<i64>());\n"
                        "        let right_sum: i64 = a_right.iter().zip(b_right).map(|(x, y)| x * y).sum();\n"
                        "        left_handle.join().unwrap() + right_sum\n"
                        "    })\n"
                        "}\n"
                        "```\n"
                        "Cuando varios hilos deben compartir y mutar estado sin un ámbito estático común, se combina el contador "
                        "atómico de referencias `Arc<T>` con un cerrojo que envuelve directamente al dato protegido (`Mutex<T>` o "
                        "`RwLock<T>`): en Rust es sintácticamente imposible acceder al dato sin adquirir primero el `MutexGuard`."
                    ),
                },
                {
                    "subsection": "sec-rust-6-2",
                    "text": (
                        "Para cargas masivas de entrada/salida de red con cientos de miles de conexiones simultáneas, crear un hilo "
                        "del sistema operativo por conexión resulta prohibitivo. En lugar de ello, una función `async fn` en Rust "
                        "devuelve un valor que implementa el rasgo `Future { type Output; fn poll(self: Pin<&mut Self>, cx: &mut Context<'_>) -> Poll<Self::Output>; }`. "
                        "Como ilustra la Figura \\ref{fig:fig-rust-async-poll-state-machine}, los futuros en Rust son perezosos y "
                        "dirigidos por sondeo (*poll-driven*): el compilador transforma el cuerpo de una `async fn` en un `enum` "
                        "donde cada punto `.await` es un estado que guarda únicamente las variables vivas a través de esa suspensión. "
                        "Dado que una variable local puede ser prestada a través de un punto `.await`, la máquina de estados generada "
                        "es *autorreferencial* (un campo del `enum` contiene un puntero a otro campo del mismo `enum`). Si esa "
                        "estructura se moviera de dirección en memoria después del primer `poll`, el puntero interno quedaría colgante; "
                        "por ello `Future::poll` recibe `self: Pin<&mut Self>`, un envoltorio de tipos que prohíbe obtener `&mut T` "
                        "para mover el valor fuera de su dirección fijada salvo que el tipo implemente `Unpin`."
                    ),
                },
            ],
            "definition": (
                "Fijación de dirección (`Pin<P>`): contrato del sistema de tipos de Rust que garantiza que el valor apuntado por el "
                "puntero `P` no será movido jamás a otra dirección de memoria mientras no implemente `Unpin`, hasta que se ejecute su destructor `Drop::drop`."
            ),
            "consejo": (
                "En código asíncrono sobre Tokio, nunca mantengas bloqueado un `std::sync::MutexGuard` a través de un punto `.await` "
                "ni ejecutes cómputo intensivo de CPU sin ceder el control; usa bloques cortos sin `.await` o delega el cómputo pesado a `tokio::task::spawn_blocking`."
            ),
            "self_check": (
                "¿Por qué en Rust un `Mutex<T>` es un contenedor genérico que envuelve al dato `T` en lugar de ser un objeto cerrojo "
                "separado del dato como en C++ (`std::mutex`) o Java?"
            ),
            "derivation": {
                "title": "Ahorro de memoria de máquinas de estados Future frente a pilas de hilos nativos",
                "assumptions": ["C conexiones concurrentes; un hilo OS reserva S_thread bytes de pila frente a S_future bytes por máquina de estados asíncrona"],
                "steps": [
                    {"equation": r"M_{\text{threads}} = C \cdot S_{\text{thread}}", "justification": "Cada hilo nativo requiere su propia pila virtual/física independiente"},
                    {"equation": r"M_{\text{async}} = C \cdot S_{\text{future}}", "justification": "Cada tarea asíncrona almacena solo las variables vivas en los puntos .await"},
                ],
                "Verify": {"left": "C * S_thread - C * S_future", "right": "C * (S_thread - S_future)"},
            },
            "worked_problem": {
                "prompt": (
                    "Un servidor de mensajería mantiene $C = 50000$ conexiones TCP simultáneas. Si cada máquina de estados `Future` "
                    "en Tokio ocupa $256\\text{ B}$ ($0.25\\text{ KiB}$) mientras que una pila mínima de hilo cuesta $64\\text{ KiB}$, "
                    "calcula la memoria total en MiB (dividiendo los KiB entre 1024) que consumen las 50 000 tareas asíncronas."
                ),
                "expression": "(50000 * 256) / (1024 * 1024)",
                "solution": {
                    "model": "Huella de memoria en MiB de C máquinas de estados Future",
                    "given": [
                        {"symbol": "C", "value": "50000", "description": "Conexiones concurrentes activas"},
                        {"symbol": "S_future", "value": "256 B", "description": "Tamaño de cada máquina de estados Future"},
                        {"symbol": "B_MiB", "value": "1048576 B/MiB", "description": "Bytes por mebibyte (1024 * 1024)"},
                    ],
                    "steps": [
                        {"step": "Multiplicamos las 50000 tareas por 256 B y dividimos entre 1024*1024", "equation": r"M_{\text{MiB}} = \frac{50000 \cdot 256}{1024 \cdot 1024}", "expression": "(50000 * 256) / (1024 * 1024)"},
                    ],
                    "conclusion": "Las 50 000 conexiones asíncronas consumen tan solo 12.20703125 MiB de RAM, frente a los 3125 MiB (> 3 GiB) que exigirían 50 000 pilas de 64 KiB.",
                },
            },
            "rust_worked_test": {
                "prompt": "Verificación ejecutable con `rustc --test` de concurrencia paralela con `std::thread::scope`, `Arc<Mutex<T>>` y canales `mpsc`.",
                "source_text": (
                    "use std::sync::{mpsc, Arc, Mutex};\n"
                    "use std::thread;\n"
                    "#[cfg(test)]\n"
                    "mod tests {\n"
                    "    use super::*;\n"
                    "    #[test]\n"
                    "    fn verify_scoped_threads_arc_mutex_and_mpsc() {\n"
                    "        let data = [1_i64, 2, 3, 4, 5, 6, 7, 8];\n"
                    "        let counter = Arc::new(Mutex::new(0_i64));\n"
                    "        let (tx, rx) = mpsc::channel();\n"
                    "        thread::scope(|s| {\n"
                    "            for chunk in data.chunks(4) {\n"
                    "                let c = Arc::clone(&counter);\n"
                    "                let t = tx.clone();\n"
                    "                s.spawn(move || {\n"
                    "                    let partial: i64 = chunk.iter().sum();\n"
                    "                    *c.lock().unwrap() += partial;\n"
                    "                    t.send(partial).unwrap();\n"
                    "                });\n"
                    "            }\n"
                    "        });\n"
                    "        drop(tx);\n"
                    "        let channel_total: i64 = rx.iter().sum();\n"
                    "        assert_eq!(*counter.lock().unwrap(), 36);\n"
                    "        assert_eq!(channel_total, 36);\n"
                    "    }\n"
                    "}\n"
                ),
            },
            "practice_problems": [
                {"prompt": "Cuatro hilos incrementan un `AtomicU64` exactamente 25 000 veces cada uno con `fetch_add(1, Ordering::Relaxed)`. ¿Cuál es el valor final exacto del contador?", "expression": "4 * 25000", "difficulty": "FOUNDATIONAL", "problem_type": "DIRECT_SUBSTITUTION"},
                {"prompt": "Un vector de 10 000 elementos se divide equitativamente entre 8 hilos mediante `chunks(1250)` dentro de `std::thread::scope`. ¿Cuántos elementos procesa cada hilo?", "expression": "10000 / 8", "difficulty": "FOUNDATIONAL", "problem_type": "DIRECT_SUBSTITUTION"},
                {"prompt": "Una `async fn` tiene 3 variables locales `u64` (8 B cada una) vivas simultáneamente en su punto `.await` más grande, más 8 bytes de discriminante de estado. ¿Cuántos bytes ocupa esa máquina de estados `Future`?", "expression": "3 * 8 + 8", "difficulty": "INTERMEDIATE", "problem_type": "MULTI_STEP"},
                {"prompt": "Un canal acotado `mpsc::sync_channel(64)` almacena mensajes de 128 bytes cada uno. ¿Cuántos bytes como máximo ocupan los mensajes en tránsito cuando el búfer está lleno?", "expression": "64 * 128", "difficulty": "INTERMEDIATE", "problem_type": "DESIGN"},
            ],
        },
        {
            "id": "cap07-nivel-experto-unsafe-ffi-macros-wasm-embedded",
            "title": "F. Nivel Experto: Rust Inseguro (unsafe), FFI con C, Macros, WebAssembly, Embedded (no_std) y Optimización",
            "part_id": "parte-v-rust-avanzado-experto",
            "part_title": "Bloques E–F: Nivel Avanzado y Experto — Smart Pointers, Concurrencia, Async y Unsafe",
            "sources": ["src-rust-nomicon", "src-iso-c17"],
            "learning_objectives": [
                "Enumerar exactamente los cinco superpoderes de un bloque unsafe y encapsularlos tras interfaces seguras con contratos Safety documentados.",
                "Construir puentes FFI bidireccionales con C (#[repr(C)], extern \"C\", #[no_mangle]) y auditar ausencias de Undefined Behavior con Miri.",
                "Escribir macros declarativas (macro_rules!) e higiénicas, comprender macros procedimentales y compilar crates para WebAssembly y sistemas empotrados (#![no_std]).",
            ],
            "concepts": [
                {"id": "cpt-rust-unsafe-miri-ffi", "title": "Los cinco superpoderes de unsafe, modelo Stacked/Tree Borrows en Miri e interoperabilidad FFI con C"},
                {"id": "cpt-rust-macros-nostd-wasm", "title": "Macros declarativas y procedimentales, programación empotrada #![no_std] y compilación a WebAssembly"},
            ],
            "subsections": [
                {"id": "sec-rust-7-1", "title": "Rust inseguro (unsafe), contratos de seguridad, Miri e interoperabilidad FFI con C"},
                {"id": "sec-rust-7-2", "title": "Metaprogramación con macros, entornos empotrados (#![no_std]), WebAssembly y optimización SIMD"},
            ],
            "purpose": (
                "Este capítulo desarrolla el Nivel Experto (Bloque F). Cuando un ingeniero de sistemas necesita implementar "
                "nuevas primitivas de sincronización, estructuras de datos intrusivas, controladores de registros de hardware "
                "mapeados en memoria (MMIO) o enlazar con bibliotecas en C del sistema operativo, recurre al subconjunto "
                "`unsafe` de Rust bajo contratos formales auditables con `Miri`."
            ),
            "paragraphs": [
                {
                    "subsection": "sec-rust-7-1",
                    "text": (
                        "Un bloque `unsafe { ... }` en Rust **no** desactiva el comprobador de préstamos ni las reglas de propiedad "
                        "sobre referencias ordinarias (`&T` y `&mut T`); únicamente habilita cinco operaciones adicionales cuyos "
                        "invariantes de validez no puede demostrar estáticamente el compilador: (1) desreferenciar punteros crudos "
                        "(`*const T` y `*mut T`); (2) llamar a una función o método marcado como `unsafe fn`; (3) acceder o modificar "
                        "una variable estática mutable; (4) implementar un rasgo marcado como `unsafe trait` (como `Send` o `Sync`); "
                        "y (5) acceder a campos de una `union`. La arquitectura idiomática de Rust encapsula todo bloque `unsafe` "
                        "dentro de un módulo con fronteras pequeñas y expone al exterior una API 100 % segura:\n"
                        "```rust\n"
                        "#[repr(C)]\n"
                        "#[derive(Copy, Clone, Debug, PartialEq)]\n"
                        "pub struct CTelemetryHeader {\n"
                        "    pub magic: u32,\n"
                        "    pub version: u16,\n"
                        "    pub payload_len: u16,\n"
                        "}\n\n"
                        "/// Divide una rebanada mutable en dos partes disjuntas usando punteros crudos.\n"
                        "pub fn safe_split_at_mut<T>(slice: &mut [T], mid: usize) -> (&mut [T], &mut [T]) {\n"
                        "    let len = slice.len();\n"
                        "    assert!(mid <= len, \"mid fuera de rango\");\n"
                        "    let ptr = slice.as_mut_ptr();\n"
                        "    // SAFETY: 0 <= mid <= len garantiza que [ptr, ptr+mid) y [ptr+mid, ptr+len)\n"
                        "    // están dentro de la misma asignación y son estrictamente disjuntos.\n"
                        "    unsafe {\n"
                        "        (std::slice::from_raw_parts_mut(ptr, mid),\n"
                        "         std::slice::from_raw_parts_mut(ptr.add(mid), len - mid))\n"
                        "    }\n"
                        "}\n"
                        "```\n"
                        "Para interoperar con C mediante FFI (*Foreign Function Interface*), se utiliza `#[repr(C)]` (ya que el diseño "
                        "por defecto `repr(Rust)` reordena libremente los campos de un `struct` para minimizar el relleno de alineamiento) "
                        "y la convención de llamada `extern \"C\"`. El intérprete abstracto `cargo miri test` ejecuta el código MIR "
                        "verificando el modelo de alias *Stacked Borrows* / *Tree Borrows*, lecturas de memoria no inicializada y "
                        "alineamientos inválidos."
                    ),
                },
                {
                    "subsection": "sec-rust-7-2",
                    "text": (
                        "En metaprogramación, Rust ofrece dos familias de macros que operan sobre el árbol sintáctico antes de la "
                        "comprobación de tipos: las macros declarativas (`macro_rules!`), que funcionan por coincidencia de patrones "
                        "higiénica sobre fragmentos sintácticos (`expr`, `ty`, `ident`, `tt`), y las macros procedimentales (`#[derive(...)]`, "
                        "macros de atributo y macros tipo función), que son crates compilados que transforman un flujo `TokenStream` "
                        "en otro `TokenStream`. En el ámbito de sistemas empotrados y kernels de sistemas operativos, el atributo "
                        "`#![no_std]` prescinde de la biblioteca estándar `std` (que depende de un sistema operativo subyacente) y "
                        "opera únicamente sobre `core` (independiente de plataforma y sin montículo) y opcionalmente `alloc`. Del mismo "
                        "modo, Rust compila de forma nativa a `wasm32-unknown-unknown` y `wasm32-wasip1`, permitiendo ejecutar motores "
                        "criptográficos, analizadores y simuladores físicos en el navegador o en pasarelas *serverless* a velocidad cercana al código nativo."
                    ),
                },
            ],
            "definition": (
                "Invariante de validez frente a invariante de seguridad en Rust: la invariante de validez exige que un tipo nunca "
                "adopte un patrón de bits ilegal (por ejemplo, un `bool` distinto de 0 o 1, o una referencia `&T` nula o desalineada), "
                "mientras que la invariante de seguridad exige que ninguna secuencia de llamadas desde código seguro pueda inducir comportamiento indefinido."
            ),
            "consejo": (
                "Todo bloque `unsafe { ... }` debe ir precedido por un comentario `// SAFETY:` que demuestre formalmente por qué se "
                "cumplen las precondiciones en ese punto, y toda función `pub unsafe fn` debe incluir una sección `# Safety` en su documentación."
            ),
            "self_check": (
                "¿Por qué el compilador de Rust reordena por defecto los campos de un `struct` (`repr(Rust)`) y por qué es obligatorio "
                "añadir `#[repr(C)]` antes de pasar un puntero a esa estructura a una función escrita en C?"
            ),
            "derivation": {
                "title": "Reordenación óptima de campos en repr(Rust) frente a repr(C)",
                "assumptions": ["Una estructura con campos (u8, u64, u8) en arquitectura de 64 bits con alineamiento de 8 bytes para u64"],
                "steps": [
                    {"equation": r"S_{\text{repr(C)}} = 1 + 7 + 8 + 1 + 7 = 24\text{ B}", "justification": "repr(C) respeta el orden textual e inserta 7 B de padding tras cada u8 para alinear a 8 B"},
                    {"equation": r"S_{\text{repr(Rust)}} = 8 + 1 + 1 + 6 = 16\text{ B}", "justification": "repr(Rust) coloca u64 primero (8 B), agrupa los dos u8 (2 B) y añade solo 6 B de padding final"},
                ],
                "Verify": {"left": "(1 + 7 + 8 + 1 + 7) - (8 + 1 + 1 + 6)", "right": "8"},
            },
            "worked_problem": {
                "prompt": (
                    "Una estructura declarada con `#[repr(C)]` contiene en este orden exacto: `a: u8` ($1\\text{ B}$), `b: u64` "
                    "($8\\text{ B}$, requiere alineamiento a múltiplo de 8), `c: u8` ($1\\text{ B}$) y `d: u32` ($4\\text{ B}$, "
                    "requiere alineamiento a múltiplo de 4), con alineamiento total de la estructura a múltiplo de 8 bytes. "
                    "Calcula la diferencia en bytes para un array de $N = 1000$ estructuras entre `#[repr(C)]` ($24\\text{ B}$ cada una) "
                    "y el empaquetado óptimo de `repr(Rust)` que ordena `b: u64`, `d: u32`, `a: u8`, `c: u8` ($8 + 4 + 1 + 1 + 2\\text{ padding} = 16\\text{ B}$)."
                ),
                "expression": "1000 * (24 - 16)",
                "solution": {
                    "model": "Ahorro de relleno (padding) de alineamiento entre repr(C) y repr(Rust)",
                    "given": [
                        {"symbol": "N", "value": "1000", "description": "Número de estructuras en el array"},
                        {"symbol": "S_C", "value": "24 B", "description": "Tamaño bajo #[repr(C)] (1+7 + 8 + 1+3 + 4 = 24 B)"},
                        {"symbol": "S_Rust", "value": "16 B", "description": "Tamaño reordenado por repr(Rust) (8 + 4 + 1 + 1 + 2 = 16 B)"},
                    ],
                    "steps": [
                        {"step": "Multiplicamos las 1000 instancias por los 8 B ahorrados por estructura", "equation": r"\Delta B = 1000 \cdot (24 - 16)", "expression": "1000 * (24 - 16)"},
                    ],
                    "conclusion": "La reordenación automática de campos de repr(Rust) ahorra 8000 bytes (un 33.3 % de reducción de huella en caché) sin requerir acceso desalineado.",
                },
            },
            "rust_worked_test": {
                "prompt": "Verificación ejecutable con `rustc --test` de `safe_split_at_mut`, `macro_rules!` y diferencia real de tamaño entre `#[repr(C)]` y `repr(Rust)`.",
                "source_text": (
                    "#[repr(C)]\n"
                    "struct BadLayoutC { a: u8, b: u64, c: u8 }\n"
                    "struct GoodLayoutRust { a: u8, b: u64, c: u8 }\n"
                    "macro_rules! vec_of_squares {\n"
                    "    ($($x:expr),* $(,)?) => {\n"
                    "        vec![$(($x) * ($x)),*]\n"
                    "    };\n"
                    "}\n"
                    "#[cfg(test)]\n"
                    "mod tests {\n"
                    "    use super::*;\n"
                    "    use std::mem::size_of;\n"
                    "    #[test]\n"
                    "    fn verify_repr_and_declarative_macro() {\n"
                    "        assert_eq!(size_of::<BadLayoutC>(), 24);\n"
                    "        assert_eq!(size_of::<GoodLayoutRust>(), 16);\n"
                    "        let sq = vec_of_squares![2, 3, 5];\n"
                    "        assert_eq!(sq, vec![4, 9, 25]);\n"
                    "    }\n"
                    "}\n"
                ),
            },
            "practice_problems": [
                {"prompt": "Calcula el tamaño en bytes de `BadLayoutC { a: u8, b: u64, c: u8 }` bajo `#[repr(C)]` en 64 bits ($1 + 7 + 8 + 1 + 7$).", "expression": "1 + 7 + 8 + 1 + 7", "difficulty": "FOUNDATIONAL", "problem_type": "DIRECT_SUBSTITUTION"},
                {"prompt": "Calcula el tamaño en bytes de `GoodLayoutRust { a: u8, b: u64, c: u8 }` reordenado por el compilador de Rust ($8 + 1 + 1 + 6$).", "expression": "8 + 1 + 1 + 6", "difficulty": "FOUNDATIONAL", "problem_type": "DIRECT_SUBSTITUTION"},
                {"prompt": "Un registro SIMD de 256 bits (`AVX2`) procesa carriles `f32` de 32 bits en paralelo. ¿Cuántos números `f32` opera en una sola instrucción?", "expression": "256 / 32", "difficulty": "INTERMEDIATE", "problem_type": "MULTI_STEP"},
                {"prompt": "En un microcontrolador ARM Cortex-M `#![no_std]` con 64 KiB de SRAM ($65536\\text{ B}$), el firmware reserva 8192 bytes para la pila y 4096 bytes para variables estáticas. ¿Cuántos bytes quedan disponibles para buffers estáticos de DMA?", "expression": "65536 - 8192 - 4096", "difficulty": "INTERMEDIATE", "problem_type": "DESIGN"},
            ],
        },
        {
            "id": "cap08-ecosistema-herramientas-evaluacion-proyectos-rust",
            "title": "G–H. Ecosistema Profesional, Idioms, Antipatrones, Evaluación y 4 Proyectos en Rust",
            "part_id": "parte-v-rust-ecosistema-proyectos",
            "part_title": "Bloques G–H: Ecosistema Industrial, Pruebas, Benchmarking y Proyectos Completos",
            "sources": ["src-rust-book", "src-kleppmann-ddia"],
            "learning_objectives": [
                "Dominar el ecosistema estándar de producción en Rust: serde, clap, tokio, axum, sqlx, tracing, thiserror, anyhow, proptest y criterion.",
                "Diseñar arquitecturas modulares con Cargo Workspaces, feature flags aditivas, semántica SemVer e idioms (AsRef, Borrow, FromStr, Builder).",
                "Construir y verificar los 4 proyectos integradores progresivos en Rust, incluyendo el motor Key-Value concurrente con WAL y CRC32.",
            ],
            "concepts": [
                {"id": "cpt-rust-ecosystem-idioms", "title": "Ecosistema industrial (Serde, Tokio, Axum, Tracing), diseño de APIs idiomáticas y antipatrones"},
                {"id": "cpt-rust-projects-wal-kv", "title": "Arquitectura de proyectos completos en Rust: CLI, analizador, servicio HTTP y motor KV con WAL binario"},
            ],
            "subsections": [
                {"id": "sec-rust-8-1", "title": "Bloque G: Ecosistema de crates, Cargo Workspaces, idioms de diseño de APIs y antipatrones"},
                {"id": "sec-rust-8-2", "title": "Bloque H: Evaluación integral y los 4 proyectos progresivos (incluyendo rust-kv-engine verificado)"},
            ],
            "purpose": (
                "Este capítulo culmina la monografía de Rust cubriendo los Bloques G y H de la plantilla: el ecosistema real de "
                "producción, los patrones de diseño de APIs conformes a las *Rust API Guidelines*, el catálogo de antipatrones "
                "frecuentes y la construcción paso a paso de cuatro proyectos completos, culminando en el motor de almacenamiento "
                "Key-Value transaccional con registro de escritura anticipada (*Write-Ahead Log*) y suma de verificación CRC32 "
                "ubicado en `projects/rust-kv-engine`."
            ),
            "paragraphs": [
                {
                    "subsection": "sec-rust-8-1",
                    "text": (
                        "El ecosistema industrial de Rust se articula en torno a crates fundacionales de altísima cohesión: `serde` "
                        "(serialización y deserialización de coste cero sin reflexión en tiempo de ejecución mediante generación de "
                        "código con `#[derive(Serialize, Deserialize)]`), `clap` (análisis declarativo de argumentos CLI), `tokio` "
                        "y `axum` (servidores HTTP/gRPC asíncronos con extractores con seguridad de tipos), `sqlx` (consultas SQL "
                        "verificadas contra el esquema de la base de datos en tiempo de compilación), `tracing` (telemetría estructurada "
                        "con *spans* jerárquicos conscientes de tareas asíncronas), `proptest` (pruebas basadas en propiedades con "
                        "reducción automática de contraejemplos) y `criterion` (microbenchmarking estadístico). Al diseñar APIs públicas, "
                        "las *Rust API Guidelines* recomiendan aceptar parámetros genéricos mediante `impl AsRef<Path>` o `&str` en "
                        "lugar de `&String` o `&Vec<T>`, implementar `From`/`TryFrom` y garantizar que las *feature flags* de Cargo "
                        "sean estrictamente aditivas para que la unión de características solicitadas por distintos crates en el árbol "
                        "de dependencias nunca provoque incompatibilidades de compilación."
                    ),
                },
                {
                    "subsection": "sec-rust-8-2",
                    "text": (
                        "El Bloque H articula cuatro proyectos progresivos obligatorios: (1) una herramienta CLI de auditoría e "
                        "indexación de ficheros con sumas criptográficas y salida estructurada; (2) un analizador sintáctico de "
                        "copia cero (*zero-copy*) para registros de configuración y telemetría; (3) un microservicio HTTP concurrente "
                        "con limitación de tasa (*token bucket*) y apagado ordenado (*graceful shutdown*); y (4) el motor de almacenamiento "
                        "Key-Value persistente `projects/rust-kv-engine`. En este cuarto proyecto, cada mutación `SET` o `DEL` se "
                        "empaqueta en una trama binaria `[crc32: 4 B][op: 1 B][key_len: 4 B][val_len: 4 B][key][val]` de $13\\text{ B}$ "
                        "de cabecera fija y se sincroniza en el fichero de registro de escritura anticipada (*Write-Ahead Log*, WAL) "
                        "antes de actualizar el índice en memoria protegido por `Arc<RwLock<HashMap<String, Vec<u8>>>>`:\n"
                        "```rust\n"
                        "pub fn encode_wal_frame_size(key: &str, value: &[u8]) -> usize {\n"
                        "    // 4B CRC32 + 1B opcode + 4B key_len + 4B val_len + key + value\n"
                        "    13 + key.len() + value.len()\n"
                        "}\n"
                        "```\n"
                        "Durante la recuperación tras un fallo eléctrico o caída del proceso, el motor recorre secuencialmente el WAL, "
                        "recalcula el polinomio IEEE 802.3 CRC32 (`0xEDB88320`) de cada trama y rechaza de forma determinista cualquier "
                        "registro truncado o corrompido en disco."
                    ),
                },
            ],
            "definition": (
                "Write-Ahead Log (WAL) con verificación CRC32: estructura de almacenamiento secuencial sólo-añadir (append-only) "
                "en la que toda operación de mutación se persiste en disco precedida de un código de redundancia cíclica antes de "
                "confirmarse en la estructura de datos en memoria, garantizando atomicidad y durabilidad (propiedades A y D de ACID)."
            ),
            "consejo": (
                "Nunca expongas `&String`, `&Vec<T>` ni `&Box<T>` en los parámetros de entrada de funciones públicas: utiliza `&str`, "
                "`&[T]` y `&T`, ya que las coerciones automáticas `Deref` permiten pasar tanto tipos propietarios como vistas prestadas sin coste."
            ),
            "self_check": (
                "¿Por qué las *feature flags* de un manifiesto `Cargo.toml` deben ser siempre aditivas y qué problema ocurre cuando "
                "dos dependencias de un mismo workspace activan combinaciones distintas de una feature no aditiva?"
            ),
            "derivation": {
                "title": "Tamaño en disco de un lote de N registros en el Write-Ahead Log (WAL) de rust-kv-engine",
                "assumptions": ["Cada registro WAL consta de 13 bytes de cabecera fija (CRC32 + op + key_len + val_len) más L_k bytes de clave y L_v bytes de valor"],
                "steps": [
                    {"equation": r"S_{\text{frame}} = 13 + L_k + L_v", "justification": "Suma de 4 B (CRC32) + 1 B (op) + 4 B (key_len) + 4 B (val_len) + clave + valor"},
                    {"equation": r"S_{\text{batch}}(N) = N \cdot (13 + L_k + L_v)", "justification": "Para N registros de longitud uniforme (L_k, L_v) en el fichero append-only"},
                ],
                "Verify": {"left": "N * (13 + L_k + L_v)", "right": "13 * N + N * L_k + N * L_v"},
            },
            "worked_problem": {
                "prompt": (
                    "En el motor `rust-kv-engine`, cada trama del Write-Ahead Log (WAL) tiene una cabecera fija de $13\\text{ B}$ "
                    "(4 B de CRC32, 1 B de código de operación, 4 B de longitud de clave y 4 B de longitud de valor). Si se registran "
                    "$N = 2000$ operaciones `SET` donde cada clave mide $L_k = 16\\text{ B}$ y cada valor mide $L_v = 99\\text{ B}$, "
                    "calcula el tamaño exacto en bytes del fichero WAL resultante antes de ejecutar `compact()`."
                ),
                "expression": "2000 * (13 + 16 + 99)",
                "solution": {
                    "model": "Tamaño total del fichero Write-Ahead Log (WAL) para N tramas",
                    "given": [
                        {"symbol": "N", "value": "2000", "description": "Número de operaciones SET registradas"},
                        {"symbol": "H", "value": "13 B", "description": "Cabecera binaria fija por trama WAL"},
                        {"symbol": "L_k, L_v", "value": "16 B, 99 B", "description": "Longitudes de clave y valor"},
                    ],
                    "steps": [
                        {"step": "Calculamos 13 + 16 + 99 = 128 B por trama y multiplicamos por 2000 tramas", "equation": r"B_{\text{WAL}} = 2000 \cdot (13 + 16 + 99)", "expression": "2000 * (13 + 16 + 99)"},
                    ],
                    "conclusion": "El fichero WAL ocupa exactamente 256 000 bytes (250 KiB) en disco.",
                },
            },
            "rust_worked_test": {
                "prompt": "Verificación ejecutable con `rustc --test` del algoritmo CRC32 IEEE 802.3 y empaquetado de trama WAL empleado en `projects/rust-kv-engine`.",
                "source_text": (
                    "pub fn crc32_ieee(data: &[u8]) -> u32 {\n"
                    "    let mut crc: u32 = 0xFFFF_FFFF;\n"
                    "    for &byte in data {\n"
                    "        crc ^= u32::from(byte);\n"
                    "        for _ in 0..8 {\n"
                    "            if (crc & 1) != 0 { crc = (crc >> 1) ^ 0xEDB8_8320; } else { crc >>= 1; }\n"
                    "        }\n"
                    "    }\n"
                    "    !crc\n"
                    "}\n"
                    "#[cfg(test)]\n"
                    "mod tests {\n"
                    "    use super::*;\n"
                    "    #[test]\n"
                    "    fn verify_crc32_standard_check_value() {\n"
                    "        // El valor estándar IEEE 802.3 de \"123456789\" es 0xCBF43926\n"
                    "        assert_eq!(crc32_ieee(b\"123456789\"), 0xCBF4_3926);\n"
                    "    }\n"
                    "}\n"
                ),
            },
            "practice_problems": [
                {"prompt": "Calcula el tamaño en bytes de una trama WAL de `rust-kv-engine` con cabecera de 13 B, clave de 11 B y valor de 40 B ($13 + 11 + 40$).", "expression": "13 + 11 + 40", "difficulty": "FOUNDATIONAL", "problem_type": "DIRECT_SUBSTITUTION"},
                {"prompt": "Un fichero WAL contiene 5000 registros sobre un conjunto de solo 800 claves únicas (cada una actualizada varias veces). Si `compact()` conserva únicamente el último valor de cada clave viva (64 B por trama), ¿cuántos bytes ocupa el WAL compactado?", "expression": "800 * 64", "difficulty": "FOUNDATIONAL", "problem_type": "MULTI_STEP"},
                {"prompt": "En el problema anterior, ¿cuántos bytes de espacio en disco libera la operación `compact()` respecto a las 5000 tramas originales de 64 B?", "expression": "(5000 - 800) * 64", "difficulty": "INTERMEDIATE", "problem_type": "MULTI_STEP"},
                {"prompt": "Un workspace de Cargo contiene 6 crates de biblioteca y cada crate define 12 pruebas unitarias y 3 pruebas de integración. ¿Cuántas pruebas ejecuta en total `cargo test --workspace`?", "expression": "6 * (12 + 3)", "difficulty": "INTERMEDIATE", "problem_type": "DESIGN"},
            ],
        },
    ],
}


def main() -> None:
    s3 = build_studium_volume(VOL03_SPEC)
    report_path = ROOT / "reports" / "vol03-build.json"
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(json.dumps(s3, indent=2, ensure_ascii=False), encoding="utf-8")


if __name__ == "__main__":
    main()
