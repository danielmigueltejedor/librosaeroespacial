#!/usr/bin/env python3
"""Generate the master blueprint, curriculum coverage matrix, prerequisite DAG,
19 personalized learning paths, and normative sources catalog for the
Enciclopedia de Programación e Ingeniería del Software.
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BLUEPRINT_DIR = ROOT / "blueprint"

SOURCES_CATALOG = [
    {
        "id": "src-turing-1936",
        "title": "Alan M. Turing — On Computable Numbers, with an Application to the Entscheidungsproblem (1936)",
        "url": "https://www.cs.virginia.edu/~robins/Turing_Paper_1936.pdf",
        "license": "Public Domain / Historical Primary Source",
        "version": "1936",
        "authority": "PRIMARY_SPECIFICATION",
        "text": "The 'computable' numbers may be described briefly as the real numbers whose expressions as a decimal are calculable by finite means. It is possible to invent a single machine which can be used to compute any computable sequence."
    },
    {
        "id": "src-von-neumann-1945",
        "title": "John von Neumann — First Draft of a Report on the EDVAC (1945)",
        "url": "https://web.mit.edu/STS.035/www/PDFs/edvac.pdf",
        "license": "Public Domain",
        "version": "1945",
        "authority": "PRIMARY_SPECIFICATION",
        "text": "An automatic computing system is a device with which certain instructions can be given, and which will then carry out these instructions automatically. The device requires a central arithmetic part, a central control part, a memory that stores both instructions and numerical data, and input and output organs."
    },
    {
        "id": "src-ieee-754",
        "title": "IEEE Standard for Floating-Point Arithmetic (IEEE 754-2019) / Wikipedia Summary",
        "url": "https://en.wikipedia.org/wiki/IEEE_754",
        "license": "CC BY-SA 4.0",
        "version": "IEEE 754-2019",
        "authority": "NORMATIVE_STANDARD",
        "text": "The IEEE Standard for Floating-Point Arithmetic (IEEE 754) is a technical standard for floating-point computation which defines arithmetic formats, interchange formats, rounding rules, operations, and exception handling including binary32 and binary64."
    },
    {
        "id": "src-unicode-utf8",
        "title": "RFC 3629 — UTF-8, a transformation format of ISO 10646 (IETF Standard)",
        "url": "https://datatracker.ietf.org/doc/html/rfc3629",
        "license": "IETF Trust / Public Standard",
        "version": "RFC 3629 (STD 63)",
        "authority": "NORMATIVE_STANDARD",
        "text": "UTF-8 encodes UCS characters as a varying number of octets, where the number of octets, and the value of each, depend on the integer value assigned to the character in ISO/IEC 10646. US-ASCII values do not appear otherwise in a UTF-8 encoded character stream."
    },
    {
        "id": "src-acm-cs2023",
        "title": "ACM / IEEE-CS / AAAI Computer Science Curricula 2023 (CS2023)",
        "url": "https://csed.acm.org/",
        "license": "Open Curriculum Standard",
        "version": "CS2023",
        "authority": "CURRICULUM_AUTHORITY",
        "text": "CS2023 organizes computer science knowledge into core areas including Algorithms and Complexity, Architecture and Organization, Discrete Structures, Foundations of Programming Languages, Operating Systems, Parallel and Distributed Computing, Software Development Fundamentals, Software Engineering, and Security."
    },
    {
        "id": "src-mit-6006",
        "title": "MIT OpenCourseWare 6.006 — Introduction to Algorithms",
        "url": "https://ocw.mit.edu/courses/6-006-introduction-to-algorithms-spring-2020/",
        "license": "CC BY-NC-SA 4.0",
        "version": "Spring 2020",
        "authority": "UNIVERSITY_COURSE",
        "text": "An introduction to mathematical modeling of computational problems, as well as common algorithms, algorithmic paradigms, and data structures used to solve these problems, emphasizing the relationship between algorithms and programming and basic performance measures and analysis techniques."
    },
    {
        "id": "src-rust-book",
        "title": "The Rust Programming Language (Klabnik & Nichols — Official Rust Documentation)",
        "url": "https://doc.rust-lang.org/book/",
        "license": "MIT / Apache-2.0",
        "version": "Rust 2021 / 1.98",
        "authority": "OFFICIAL_DOCUMENTATION",
        "text": "Ownership is Rust's most unique feature and has deep implications for the rest of the language. It enables Rust to make memory safety guarantees without needing a garbage collector: each value in Rust has an owner, there can only be one owner at a time, and when the owner goes out of scope, the value will be dropped."
    },
    {
        "id": "src-rust-reference",
        "title": "The Rust Reference — Memory Model, Type System, Lifetimes, and Unsafe Rust",
        "url": "https://doc.rust-lang.org/reference/",
        "license": "MIT / Apache-2.0",
        "version": "Rust 1.98",
        "authority": "PRIMARY_SPECIFICATION",
        "text": "At any given time, you can have either one mutable reference or any number of immutable references, and references must always be valid. Unsafe Rust unlocks five actions: dereferencing raw pointers, calling unsafe functions, accessing mutable statics, implementing unsafe traits, and accessing union fields."
    },
    {
        "id": "src-rustonomicon",
        "title": "The Rustonomicon — The Dark Arts of Unsafe Rust",
        "url": "https://doc.rust-lang.org/nomicon/",
        "license": "MIT / Apache-2.0",
        "version": "Rust 1.98",
        "authority": "OFFICIAL_DOCUMENTATION",
        "text": "Safe Rust is a sound language: no matter what, Safe Rust cannot cause Undefined Behavior. Unsafe Rust is the exact same language with the same semantics, except that the programmer assumes responsibility for upholding the compiler's aliasing, alignment, initialization, and lifetime invariants."
    },
    {
        "id": "src-c-standard",
        "title": "C Programming Language Reference (ISO/IEC 9899 C17/C23 — cppreference)",
        "url": "https://en.cppreference.com/w/c",
        "license": "CC BY-SA 3.0",
        "version": "ISO/IEC 9899:2018 (C17) / C23",
        "authority": "TECHNICAL_REFERENCE",
        "text": "Objects in C have storage duration (automatic, static, thread, or allocated), scope, linkage, and effective type. Dereferencing an invalid, null, or misaligned pointer, signed integer overflow, or violating strict aliasing rules results in undefined behavior."
    },
    {
        "id": "src-cpp-standard",
        "title": "C++ Reference (ISO/IEC 14882 C++20/C++23 — cppreference)",
        "url": "https://en.cppreference.com/w/cpp",
        "license": "CC BY-SA 3.0",
        "version": "ISO/IEC 14882:2020 (C++20) / C++23",
        "authority": "TECHNICAL_REFERENCE",
        "text": "Resource Acquisition Is Initialization (RAII) binds the life cycle of a resource that must be acquired before use to the lifetime of an object. C++20 introduces Concepts for constraining templates, Ranges for composable algorithms, Coroutines, and Modules."
    },
    {
        "id": "src-python-docs",
        "title": "The Python Language Reference & Standard Library Documentation (Python 3.12–3.14)",
        "url": "https://docs.python.org/3/reference/index.html",
        "license": "PSF License v2 / Zero-Clause BSD",
        "version": "Python 3.12–3.14",
        "authority": "OFFICIAL_DOCUMENTATION",
        "text": "Objects are Python's abstraction for data. All data in a Python program is represented by objects or by relations between objects. Every object has an identity, a type, and a value. Special method names (__init__, __iter__, __enter__, __exit__, __get__) define the Python data model protocols."
    },
    {
        "id": "src-ecmascript-spec",
        "title": "ECMA-262 — ECMAScript 2024 Language Specification",
        "url": "https://tc39.es/ecma262/",
        "license": "BSD-3-Clause / Ecma International",
        "version": "ECMAScript 2024 (15th Edition)",
        "authority": "PRIMARY_SPECIFICATION",
        "text": "An ECMAScript agent consists of execution contexts, an execution context stack, a running execution context, a set of job queues (macrotask and microtask queues), and a heap of objects linked through prototype chains and lexical environments."
    },
    {
        "id": "src-typescript-handbook",
        "title": "The TypeScript Handbook — Structural Typing, Narrowing, and Type Manipulation",
        "url": "https://www.typescriptlang.org/docs/handbook/intro.html",
        "license": "CC BY 4.0 / Apache-2.0",
        "version": "TypeScript 5.x",
        "authority": "OFFICIAL_DOCUMENTATION",
        "text": "One of TypeScript's core principles is that type checking focuses on the shape that values have, sometimes called duck typing or structural subtyping. TypeScript's type system is erased completely at compile time and introduces zero runtime overhead."
    },
    {
        "id": "src-dotnet-csharp",
        "title": "Microsoft .NET & C# Language Specification (ECMA-334 / .NET 8 & 9)",
        "url": "https://learn.microsoft.com/en-us/dotnet/csharp/",
        "license": "CC BY 4.0",
        "version": "C# 12 / .NET 8",
        "authority": "OFFICIAL_DOCUMENTATION",
        "text": "C# is a modern, object-oriented, and type-safe programming language running on the Common Language Runtime (CLR), unifying value types (structs, Span<T>) and reference types (classes, records), generics without type erasure, LINQ, and task-based asynchronous programming."
    },
    {
        "id": "src-java-jls",
        "title": "The Java Language Specification & JVM Specification (Java SE 21 LTS)",
        "url": "https://docs.oracle.com/javase/specs/jls/se21/html/index.html",
        "license": "Specification Reference",
        "version": "Java SE 21 LTS",
        "authority": "PRIMARY_SPECIFICATION",
        "text": "The Java Virtual Machine executes class files using class loaders, a bytecode verifier, an interpreter, a Just-In-Time compiler, and automatic garbage collection under the Java Memory Model (JMM) happens-before relation, complemented in Java 21 by lightweight Virtual Threads."
    },
    {
        "id": "src-go-spec",
        "title": "The Go Programming Language Specification & Memory Model",
        "url": "https://go.dev/ref/spec",
        "license": "CC BY 4.0 / BSD-3-Clause",
        "version": "Go 1.22+",
        "authority": "PRIMARY_SPECIFICATION",
        "text": "Go is a general-purpose systems language designed with structural interfaces, explicit error values, garbage collection, and CSP-inspired concurrency via lightweight goroutines multiplexed onto OS threads and typed communication channels."
    },
    {
        "id": "src-kotlin-docs",
        "title": "Kotlin Language Documentation & Coroutines Guide (Kotlin 2.0)",
        "url": "https://kotlinlang.org/docs/home.html",
        "license": "Apache-2.0",
        "version": "Kotlin 2.0",
        "authority": "OFFICIAL_DOCUMENTATION",
        "text": "Kotlin enforces null safety in its type system by distinguishing nullable and non-null references at compile time, and provides structured concurrency through suspend functions, CoroutineScope, Dispatchers, and cold asynchronous Flows."
    },
    {
        "id": "src-swift-book",
        "title": "The Swift Programming Language (Swift 6.0 Official Book)",
        "url": "https://docs.swift.org/swift-book/documentation/the-swift-programming-language/",
        "license": "Apache-2.0 / CC BY 4.0",
        "version": "Swift 6.0",
        "authority": "OFFICIAL_DOCUMENTATION",
        "text": "Swift combines protocol-oriented programming, copy-on-write value types, deterministic memory management via Automatic Reference Counting (ARC), and compile-time data-race safety using Sendable types and actor isolation."
    },
    {
        "id": "src-codd-relational",
        "title": "E. F. Codd — A Relational Model of Data for Large Shared Data Banks (1970) & PostgreSQL Docs",
        "url": "https://www.postgresql.org/docs/current/",
        "license": "PostgreSQL License",
        "version": "PostgreSQL 17 / SQL:2023",
        "authority": "OFFICIAL_DOCUMENTATION",
        "text": "The relational model represents all data as mathematical n-ary relations manipulated through relational algebra and declarative SQL queries. PostgreSQL implements Multi-Version Concurrency Control (MVCC), Write-Ahead Logging (WAL), and cost-based query optimization."
    },
    {
        "id": "src-sqlite-docs",
        "title": "SQLite 3.54 Transactional SQL Database Engine Documentation",
        "url": "https://www.sqlite.org/docs.html",
        "license": "Public Domain",
        "version": "SQLite 3.54.0",
        "authority": "OFFICIAL_DOCUMENTATION",
        "text": "SQLite is a self-contained, serverless, zero-configuration, transactional SQL database engine in the public domain that implements B-tree storage, ACID transactions via rollback journals or Write-Ahead Logging, CTEs, and window functions."
    },
    {
        "id": "src-posix-bash",
        "title": "GNU Bash Reference Manual & IEEE Std 1003.1 POSIX Shell Specification",
        "url": "https://www.gnu.org/software/bash/manual/bash.html",
        "license": "GFDL / POSIX Standard",
        "version": "Bash 5.2 / POSIX.1-2017",
        "authority": "OFFICIAL_DOCUMENTATION",
        "text": "The shell is a command language interpreter that executes commands read from standard input or a file, performing parameter expansion, command substitution, arithmetic expansion, word splitting, pathname expansion, and redirection across pipelines."
    },
    {
        "id": "src-whatwg-html",
        "title": "WHATWG HTML Living Standard & W3C CSS Specifications",
        "url": "https://html.spec.whatwg.org/multipage/",
        "license": "CC BY 4.0",
        "version": "Living Standard (2026)",
        "authority": "PRIMARY_SPECIFICATION",
        "text": "HTML defines the semantic structure and Document Object Model (DOM) of web documents, while CSS defines the cascade, specificity, inheritance, box model, Flexbox, Grid, and responsive container queries for visual and accessible presentation."
    },
    {
        "id": "src-rfc8259-json",
        "title": "RFC 8259 — The JavaScript Object Notation (JSON) Data Interchange Format & YAML 1.2.2",
        "url": "https://datatracker.ietf.org/doc/html/rfc8259",
        "license": "IETF Trust / Public Standard",
        "version": "RFC 8259 (STD 90) & YAML 1.2.2",
        "authority": "NORMATIVE_STANDARD",
        "text": "JSON is a lightweight, text-based, language-independent data interchange format defining six structural tokens, strings, numbers, booleans, null, objects, and arrays encoded in UTF-8. YAML 1.2 is a strict superset of JSON adding anchors, aliases, and multi-document streams."
    },
    {
        "id": "src-swebok-v4",
        "title": "IEEE Computer Society — Guide to the Software Engineering Body of Knowledge (SWEBOK v4.0)",
        "url": "https://www.computer.org/education/bodies-of-knowledge/software-engineering",
        "license": "IEEE Reference Standard",
        "version": "SWEBOK v4.0",
        "authority": "CURRICULUM_AUTHORITY",
        "text": "Software engineering encompasses systematic, disciplined, quantifiable approaches to software requirements, domain modeling, software architecture, clean and hexagonal design, automated verification and testing, CI/CD, observability, security by design, and long-term maintenance."
    }
]

MASTER_BLUEPRINT = {
    "title": "ENCICLOPEDIA DE PROGRAMACIÓN E INGENIERÍA DEL SOFTWARE — De cero a la especialización profesional",
    "version": "1.0.0",
    "language": "es",
    "framework": "Studium 1.0.0a1 (profile: COMPUTER_SCIENCE)",
    "parts": [
        {
            "part_id": "PARTE-I",
            "title": "PARTE I. Historia de la Informática y la Programación",
            "volume": "vol01-historia-y-fundamentos",
            "chapters": [
                "cap01-antecedentes-y-computabilidad",
                "cap02-primeros-ordenadores-y-compiladores",
                "cap03-paradigmas-sistemas-y-era-moderna"
            ]
        },
        {
            "part_id": "PARTE-II",
            "title": "PARTE II. Fundamentos Universales de Programación y Matemáticas Discretas",
            "volume": "vol01-historia-y-fundamentos",
            "chapters": [
                "cap04-representacion-binaria-ieee754-utf8",
                "cap05-logica-algebra-booleana-matematica-discreta",
                "cap06-arquitectura-cpu-memoria-compilacion",
                "cap07-sistemas-de-tipos-control-ambito-errores",
                "cap08-los-doce-paradigmas-de-programacion"
            ]
        },
        {
            "part_id": "PARTE-III",
            "title": "PARTE III. Algoritmos, Estructuras de Datos y Teoría de la Computación",
            "volume": "vol02-algoritmos-y-sistemas",
            "chapters": [
                "cap01-complejidad-asintotica-recurrencias-amortizado",
                "cap02-busqueda-ordenacion-cotas-inferiores",
                "cap03-divide-venceras-voraces-programacion-dinamica",
                "cap04-grafos-arboles-equilibrados-hashing",
                "cap05-estructuras-persistentes-probabilisticas-paralelos"
            ]
        },
        {
            "part_id": "PARTE-IV",
            "title": "PARTE IV. Sistemas Informáticos, Compiladores, Memoria y Sistemas Operativos",
            "volume": "vol02-algoritmos-y-sistemas",
            "chapters": [
                "cap06-jerarquia-memoria-caches-abi-enlazado",
                "cap07-compiladores-lexing-parsing-ssa-codegen",
                "cap08-sistemas-operativos-procesos-memoria-virtual-io"
            ]
        },
        {
            "part_id": "PARTE-V-RUST",
            "title": "PARTE V (Volumen 3). Monografía Completa de Referencia: Rust",
            "volume": "vol03-monografia-rust",
            "chapters": [
                "cap01-rust-introduccion-filosofia-toolchain-cargo",
                "cap02-rust-principiante-sintaxis-tipos-control-colecciones",
                "cap03-rust-ownership-borrowing-lifetimes-memoria",
                "cap04-rust-intermedio-enums-traits-generics-errores-testing",
                "cap05-rust-avanzado-closures-iteradores-smart-pointers-interior-mutability",
                "cap06-rust-concurrencia-send-sync-async-tokio-pinning",
                "cap07-rust-experto-unsafe-ffi-macros-layout-wasm-embedded",
                "cap08-rust-ecosistema-arquitectura-proyectos-evaluacion"
            ]
        },
        {
            "part_id": "PARTE-V-SISTEMAS",
            "title": "PARTE V (Volumen 4). Monografías de Programación de Sistemas: C, C++, Zig, Ensamblador, Ada y Fortran",
            "volume": "vol04-monografias-c-cpp-sistemas",
            "chapters": [
                "cap01-c-fundamentos-tipos-control-toolchain-posix",
                "cap02-c-punteros-memoria-structs-alineamiento-preprocesador",
                "cap03-c-avanzado-experto-ub-abi-sockets-sanitizers-proyectos",
                "cap04-cpp-moderno-raii-move-semantics-smart-pointers",
                "cap05-cpp-templates-concepts-stl-ranges-metaprogramacion",
                "cap06-cpp-concurrencia-coroutines-modules-hpc-proyectos",
                "cap07-zig-monografia-allocators-comptime-interoperabilidad",
                "cap08-ensamblador-arm64-x86-ada-fortran-sistemas-criticos"
            ]
        },
        {
            "part_id": "PARTE-V-ALTO-NIVEL",
            "title": "PARTE V (Volumen 5). Monografías de Python, JavaScript y TypeScript",
            "volume": "vol05-monografias-python-js-ts",
            "chapters": [
                "cap01-python-fundamentos-modelo-objetos-tipado-packaging",
                "cap02-python-intermedio-iteradores-decoradores-context-descriptores-metaclasses",
                "cap03-python-avanzado-experto-cpython-gil-asyncio-ciencia-datos-proyectos",
                "cap04-javascript-ecmascript-motor-closures-prototipos-this",
                "cap05-javascript-event-loop-promises-async-dom-nodejs-seguridad",
                "cap06-typescript-tipado-estructural-uniones-narrowing-generics",
                "cap07-typescript-avanzado-conditional-mapped-types-arquitectura",
                "cap08-integracion-ecosistema-py-js-ts-testing-proyectos"
            ]
        },
        {
            "part_id": "PARTE-V-PLATAFORMAS",
            "title": "PARTE V (Volumen 6). Monografías de C#, Java, Go, Kotlin y Swift",
            "volume": "vol06-monografias-jvm-dotnet-go-movil",
            "chapters": [
                "cap01-csharp-dotnet-clr-tipos-linq-generics",
                "cap02-csharp-async-span-gc-efcore-aspnet-proyectos",
                "cap03-java-jvm-memoria-generics-colecciones-concurrencia",
                "cap04-java-virtual-threads-records-spring-arquitectura-proyectos",
                "cap05-go-fundamentos-interfaces-modulos-errores-testing",
                "cap06-go-goroutines-channels-context-runtime-servicios-proyectos",
                "cap07-kotlin-null-safety-coroutines-flow-interoperabilidad-android",
                "cap08-swift-value-semantics-protocolos-arc-actors-swiftui-proyectos"
            ]
        },
        {
            "part_id": "PARTE-V-DECLARATIVOS-FUNCIONALES",
            "title": "PARTE V (Volumen 7). Monografías de SQL, Bash/POSIX, PHP, Ruby, Dart, Funcionales y Científicos",
            "volume": "vol07-monografias-sql-shell-funcional-especializados",
            "chapters": [
                "cap01-sql-lenguaje-declarativo-relacional-joins-cte-window",
                "cap02-bash-posix-shell-expansiones-pipelines-traps-portabilidad",
                "cap03-php-moderno-tipado-composer-arquitectura-web",
                "cap04-ruby-modelo-objetos-bloques-metaprogramacion-rails",
                "cap05-dart-isolates-async-tipado-flutter",
                "cap06-funcionales-estaticos-haskell-ocaml-fsharp-scala",
                "cap07-funcionales-concurrentes-elixir-erlang-clojure-lisp-scheme",
                "cap08-cientificos-y-dominio-julia-r-lua-perl-prolog-gdscript"
            ]
        },
        {
            "part_id": "PARTE-VI-VII-VIII",
            "title": "PARTES VI, VII y VIII (Volumen 8). Web, Formatos de Datos, Curso Completo de Bases de Datos y Frameworks",
            "volume": "vol08-web-bases-de-datos-y-frameworks",
            "chapters": [
                "cap01-html-living-standard-semantica-dom-accesibilidad-seo",
                "cap02-css-cascada-especificidad-box-model-flexbox-grid-container-queries",
                "cap03-formatos-datos-json-schema-yaml-toml-xml-markdown-csv-protobuf",
                "cap04-bases-datos-modelo-relacional-algebra-er-normalizacion-bcnf",
                "cap05-bases-datos-indices-btree-planificadores-transacciones-acid-mvcc",
                "cap06-bases-datos-distribuidas-postgresql-sqlite-nosql-laboratorios",
                "cap07-frameworks-frontend-react-nextjs-vue-angular-svelte-arquitectura",
                "cap08-frameworks-backend-escritorio-movil-fastapi-django-spring-tauri-flutter"
            ]
        },
        {
            "part_id": "PARTE-IX-X-XI-XII-XIII",
            "title": "PARTES IX–XIII (Volumen 9). Ingeniería del Software, Sistemas Distribuidos, Cloud/DevOps, Seguridad, Proyectos y Evaluación",
            "volume": "vol09-ingenieria-software-arquitectura-y-proyectos",
            "chapters": [
                "cap01-requisitos-ddd-cohesion-acoplamiento-solid-patrones",
                "cap02-arquitectura-limpia-hexagonal-monolitos-microservicios-eventos",
                "cap03-apis-rest-graphql-grpc-git-interno-code-review-refactoring",
                "cap04-testing-unitario-integracion-e2e-propiedades-fuzzing-mutacion",
                "cap05-sistemas-distribuidos-consenso-observabilidad-sre-incidentes",
                "cap06-seguridad-por-diseno-criptografia-oauth-supply-chain-licencias",
                "cap07-linux-contenedores-docker-kubernetes-iac-cloud-cicd",
                "cap08-proyectos-integradores-evaluacion-competencias-soluciones"
            ]
        }
    ]
}

LEARNING_PATHS = [
    {
        "id": "ruta-01-desde-cero",
        "title": "1. Programación desde Cero hasta Autonomía Técnica",
        "prerequisites": ["Ninguno (aritmética elemental y manejo básico de archivos)"],
        "recommended_order": [
            "vol01-historia-y-fundamentos:cap01..cap08",
            "vol05-monografias-python-js-ts:cap01..cap02",
            "vol02-algoritmos-y-sistemas:cap01..cap02",
            "vol07-monografias-sql-shell-funcional-especializados:cap01..cap02",
            "vol09-ingenieria-software-arquitectura-y-proyectos:cap03..cap04"
        ],
        "essential_projects": ["Calculadora y evaluador de expresiones con AST", "Gestor CLI con persistencia JSON/SQLite y suite pytest"],
        "target_competencies": ["Competencia inicial", "Competencia intermedia"],
        "evaluations": ["Autoevaluaciones de Parte II", "Banco de problemas Niveles 1–3 de Python y Algoritmos"],
        "next_specializations": ["Ingeniería de software generalista", "Desarrollo Backend", "Ciencia de Datos"]
    },
    {
        "id": "ruta-02-ingenieria-generalista",
        "title": "2. Ingeniería del Software Generalista",
        "prerequisites": ["Fundamentos computacionales (Vol. 1)"],
        "recommended_order": [
            "vol01-historia-y-fundamentos:cap04..cap08",
            "vol02-algoritmos-y-sistemas:cap01..cap08",
            "vol03-monografia-rust:cap01..cap05",
            "vol05-monografias-python-js-ts:cap01..cap07",
            "vol08-web-bases-de-datos-y-frameworks:cap04..cap06",
            "vol09-ingenieria-software-arquitectura-y-proyectos:cap01..cap08"
        ],
        "essential_projects": ["Motor KV transaccional con WAL", "API REST Hexagonal con PostgreSQL/SQLite y CI/CD"],
        "target_competencies": ["Competencia profesional", "Competencia experta"],
        "evaluations": ["Auditorías de arquitectura", "Pruebas basadas en propiedades y mutación"],
        "next_specializations": ["Arquitectura de sistemas distribuidos", "Programación de sistemas"]
    },
    {
        "id": "ruta-03-sistemas",
        "title": "3. Programación de Sistemas y Bajo Nivel",
        "prerequisites": ["Representación binaria y arquitectura CPU/memoria (Vol. 1 Cap. 4 y 6)"],
        "recommended_order": [
            "vol02-algoritmos-y-sistemas:cap06..cap08",
            "vol04-monografias-c-cpp-sistemas:cap01..cap08",
            "vol03-monografia-rust:cap01..cap08"
        ],
        "essential_projects": ["Asignador Arena en C17 verificado con ASan/UBSan", "Servidor TCP asíncrono y motor KV en Rust"],
        "target_competencies": ["Competencia avanzada", "Competencia experta"],
        "evaluations": ["Auditoría de memoria sin UB", "Diseño de FFI con ABI C estable"],
        "next_specializations": ["Sistemas embebidos", "Compiladores", "Software de alto rendimiento (HPC)"]
    },
    {
        "id": "ruta-04-web-frontend",
        "title": "4. Desarrollo Web Frontend y Sistemas de Diseño",
        "prerequisites": ["Fundamentos de programación (Vol. 1)"],
        "recommended_order": [
            "vol08-web-bases-de-datos-y-frameworks:cap01..cap03",
            "vol05-monografias-python-js-ts:cap04..cap07",
            "vol08-web-bases-de-datos-y-frameworks:cap07"
        ],
        "essential_projects": ["Sistema de diseño accesible WCAG 2.2 con CSS Grid/Container Queries", "Aplicación SPA/SSR en TypeScript estricto"],
        "target_competencies": ["Competencia profesional"],
        "evaluations": ["Auditoría de accesibilidad DOM/ARIA", "Tipado estructural avanzado en TypeScript"],
        "next_specializations": ["Desarrollo Full Stack", "Aplicaciones de escritorio con Tauri"]
    },
    {
        "id": "ruta-05-backend",
        "title": "5. Desarrollo Backend y Diseño de APIs",
        "prerequisites": ["Fundamentos de programación y redes básicas"],
        "recommended_order": [
            "vol05-monografias-python-js-ts:cap01..cap03",
            "vol06-monografias-jvm-dotnet-go-movil:cap01..cap06",
            "vol08-web-bases-de-datos-y-frameworks:cap04..cap06",
            "vol08-web-bases-de-datos-y-frameworks:cap08",
            "vol09-ingenieria-software-arquitectura-y-proyectos:cap01..cap06"
        ],
        "essential_projects": ["Servicio HTTP concurrente con idempotencia, autenticación OAuth2/JWT y SQL transaccional"],
        "target_competencies": ["Competencia profesional", "Competencia experta"],
        "evaluations": ["Diseño de esquemas normalizados BCNF", "Análisis de aislamiento MVCC y concurrencia"],
        "next_specializations": ["Sistemas distribuidos", "Plataformas Cloud y DevOps"]
    },
    {
        "id": "ruta-06-full-stack",
        "title": "6. Desarrollo Full Stack End-to-End",
        "prerequisites": ["Fundamentos de programación (Vol. 1)"],
        "recommended_order": [
            "vol08-web-bases-de-datos-y-frameworks:cap01..cap08",
            "vol05-monografias-python-js-ts:cap04..cap08",
            "vol09-ingenieria-software-arquitectura-y-proyectos:cap01..cap08"
        ],
        "essential_projects": ["Plataforma web full-stack con contratos OpenAPI/JSON Schema, base de datos relacional y tests E2E"],
        "target_competencies": ["Competencia profesional"],
        "evaluations": ["Integración continua y seguridad web (CSP/CSRF/XSS)"],
        "next_specializations": ["Arquitectura de software", "Ingeniería de producto"]
    },
    {
        "id": "ruta-07-movil",
        "title": "7. Desarrollo Móvil Nativo y Multiplataforma (iOS, Android, Flutter)",
        "prerequisites": ["Fundamentos de tipos y concurrencia asíncrona"],
        "recommended_order": [
            "vol06-monografias-jvm-dotnet-go-movil:cap07..cap08",
            "vol07-monografias-sql-shell-funcional-especializados:cap05",
            "vol08-web-bases-de-datos-y-frameworks:cap08"
        ],
        "essential_projects": ["Aplicación móvil offline-first con SQLite local, coroutines/actors y UI declarativa"],
        "target_competencies": ["Competencia profesional"],
        "evaluations": ["Gestión de memoria ARC sin ciclos de retención", "Concurrencia estructurada en Kotlin y Swift 6"],
        "next_specializations": ["Sistemas embebidos y BLE", "Arquitectura cliente-servidor"]
    },
    {
        "id": "ruta-08-escritorio",
        "title": "8. Desarrollo de Aplicaciones de Escritorio Multiplataforma",
        "prerequisites": ["Programación modular y sistemas operativos"],
        "recommended_order": [
            "vol03-monografia-rust:cap01..cap06",
            "vol04-monografias-c-cpp-sistemas:cap04..cap06",
            "vol06-monografias-jvm-dotnet-go-movil:cap01..cap02",
            "vol08-web-bases-de-datos-y-frameworks:cap08"
        ],
        "essential_projects": ["Aplicación nativa con Tauri (Rust + TypeScript) o Qt/C++ con IPC seguro"],
        "target_competencies": ["Competencia profesional"],
        "evaluations": ["Separación de hilos de UI y workers de E/S"],
        "next_specializations": ["Herramientas CAD/CAE", "Audio/Vídeo en tiempo real"]
    },
    {
        "id": "ruta-09-ingenieria-datos",
        "title": "9. Ingeniería de Datos y Almacenamiento a Gran Escala",
        "prerequisites": ["Algoritmos (Vol. 2) y SQL (Vol. 7 Cap. 1)"],
        "recommended_order": [
            "vol07-monografias-sql-shell-funcional-especializados:cap01",
            "vol08-web-bases-de-datos-y-frameworks:cap03..cap06",
            "vol05-monografias-python-js-ts:cap01..cap03",
            "vol07-monografias-sql-shell-funcional-especializados:cap06",
            "vol09-ingenieria-software-arquitectura-y-proyectos:cap05"
        ],
        "essential_projects": ["Pipeline ETL idempotente con particionado, validación de esquemas y almacenamiento columnar"],
        "target_competencies": ["Competencia profesional", "Competencia experta"],
        "evaluations": ["Optimización de planes de ejecución SQL y diseño de índices B+ y LSM"],
        "next_specializations": ["Sistemas distribuidos", "Arquitectura de bases de datos"]
    },
    {
        "id": "ruta-10-ciencia-datos",
        "title": "10. Ciencia de Datos y Análisis Estadístico Reproducible",
        "prerequisites": ["Matemáticas discretas y probabilidad (Vol. 1 Cap. 5)"],
        "recommended_order": [
            "vol05-monografias-python-js-ts:cap01..cap03",
            "vol07-monografias-sql-shell-funcional-especializados:cap01",
            "vol07-monografias-sql-shell-funcional-especializados:cap08"
        ],
        "essential_projects": ["Laboratorio reproducible de análisis estadístico y visualización en Python y R"],
        "target_competencies": ["Competencia intermedia", "Competencia avanzada"],
        "evaluations": ["Vectorización numérica y control de sesgos de muestreo"],
        "next_specializations": ["Machine Learning", "Computación científica"]
    },
    {
        "id": "ruta-11-computacion-cientifica",
        "title": "11. Computación Científica y Métodos Numéricos",
        "prerequisites": ["IEEE 754 (Vol. 1 Cap. 4) y complejidad algorítmica (Vol. 2)"],
        "recommended_order": [
            "vol01-historia-y-fundamentos:cap04",
            "vol04-monografias-c-cpp-sistemas:cap05..cap08",
            "vol05-monografias-python-js-ts:cap03",
            "vol07-monografias-sql-shell-funcional-especializados:cap08"
        ],
        "essential_projects": ["Solver numérico matricial y de EDOs en Python/Julia/Fortran/C++ con control de error de redondeo"],
        "target_competencies": ["Competencia avanzada", "Competencia experta"],
        "evaluations": ["Análisis de condicionamiento y estabilidad numérica IEEE 754"],
        "next_specializations": ["Software de alto rendimiento (HPC)", "Simulación física"]
    },
    {
        "id": "ruta-12-ia-ml",
        "title": "12. Inteligencia Artificial, Sistemas de Inferencia y Machine Learning",
        "prerequisites": ["Algoritmos, grafos, probabilidad y Python avanzado"],
        "recommended_order": [
            "vol02-algoritmos-y-sistemas:cap01..cap05",
            "vol05-monografias-python-js-ts:cap01..cap03",
            "vol04-monografias-c-cpp-sistemas:cap04..cap06",
            "vol09-ingenieria-software-arquitectura-y-proyectos:cap04..cap07"
        ],
        "essential_projects": ["Motor de diferenciación automática (autograd) y servicio de inferencia instrumentado"],
        "target_competencies": ["Competencia avanzada", "Competencia profesional"],
        "evaluations": ["Verificación de gradientes por diferencias finitas y determinismo de semillas"],
        "next_specializations": ["Compiladores de ML", "MLOps y sistemas distribuidos"]
    },
    {
        "id": "ruta-13-videojuegos",
        "title": "13. Arquitectura de Motores y Desarrollo de Videojuegos",
        "prerequisites": ["Álgebra lineal, memoria contigua y bucle de eventos"],
        "recommended_order": [
            "vol04-monografias-c-cpp-sistemas:cap04..cap06",
            "vol06-monografias-jvm-dotnet-go-movil:cap01..cap02",
            "vol03-monografia-rust:cap01..cap07",
            "vol07-monografias-sql-shell-funcional-especializados:cap08"
        ],
        "essential_projects": ["Arquitectura Entity-Component-System (ECS) orientada a caché con presupuesto de frame de 16.6 ms"],
        "target_competencies": ["Competencia avanzada"],
        "evaluations": ["Diseño orientado a datos (SoA vs AoS) y determinismo de simulación física"],
        "next_specializations": ["Gráficos por computador", "Motores de simulación en tiempo real"]
    },
    {
        "id": "ruta-14-embebidos",
        "title": "14. Programación Embebida, Bare-Metal y Sistemas de Tiempo Real",
        "prerequisites": ["Representación binaria, registros MMIO y arquitectura ARM64/C"],
        "recommended_order": [
            "vol01-historia-y-fundamentos:cap04..cap06",
            "vol04-monografias-c-cpp-sistemas:cap01..cap03",
            "vol04-monografias-c-cpp-sistemas:cap07..cap08",
            "vol03-monografia-rust:cap07"
        ],
        "essential_projects": ["Firmware sin asignación dinámica (no_std / C estático) con máquina de estados determinista"],
        "target_competencies": ["Competencia avanzada", "Competencia experta"],
        "evaluations": ["Uso de volatile/MMIO, presupuesto estático de pila y ausencia de heap"],
        "next_specializations": ["Sistemas críticos (Ada/SPARK)", "RTOS y aviónica"]
    },
    {
        "id": "ruta-15-seguridad",
        "title": "15. Seguridad Informática, Criptografía Aplicada y Auditoría de Código",
        "prerequisites": ["Sistemas operativos, memoria en C y redes"],
        "recommended_order": [
            "vol04-monografias-c-cpp-sistemas:cap02..cap03",
            "vol03-monografia-rust:cap03..cap07",
            "vol05-monografias-python-js-ts:cap05",
            "vol09-ingenieria-software-arquitectura-y-proyectos:cap04..cap06"
        ],
        "essential_projects": ["Auditoría con sanitizers/fuzzing y sistema de autenticación con Argon2id, Ed25519 y AES-GCM"],
        "target_competencies": ["Competencia avanzada", "Competencia experta"],
        "evaluations": ["Modelado de amenazas STRIDE y mitigación de vulnerabilidades de memoria yyección"],
        "next_specializations": ["Seguridad de compiladores", "Criptografía de protocolos"]
    },
    {
        "id": "ruta-16-devops-cloud",
        "title": "16. Ingeniería de Plataformas, DevOps, Contenedores y Cloud",
        "prerequisites": ["Sistemas operativos Linux y Bash/POSIX shell"],
        "recommended_order": [
            "vol02-algoritmos-y-sistemas:cap08",
            "vol07-monografias-sql-shell-funcional-especializados:cap02",
            "vol08-web-bases-de-datos-y-frameworks:cap03",
            "vol06-monografias-jvm-dotnet-go-movil:cap05..cap06",
            "vol09-ingenieria-software-arquitectura-y-proyectos:cap05..cap07"
        ],
        "essential_projects": ["Pipeline CI/CD reproducible, contenedorización multi-stage y observabilidad OpenTelemetry"],
        "target_competencies": ["Competencia profesional", "Competencia experta"],
        "evaluations": ["Aislamiento de namespaces/cgroups, validación YAML/JSON Schema y SLOs"],
        "next_specializations": ["Ingeniería de fiabilidad de sitios (SRE)", "Seguridad de supply chain"]
    },
    {
        "id": "ruta-17-bases-datos",
        "title": "17. Especialista en Motores y Arquitectura de Bases de Datos",
        "prerequisites": ["Árboles B+, hashing y almacenamiento en disco (Vol. 2 Cap. 4 y 8)"],
        "recommended_order": [
            "vol02-algoritmos-y-sistemas:cap04..cap08",
            "vol07-monografias-sql-shell-funcional-especializados:cap01",
            "vol08-web-bases-de-datos-y-frameworks:cap04..cap06"
        ],
        "essential_projects": ["Motor de almacenamiento clave-valor con Write-Ahead Log (WAL), índice en memoria y compactación"],
        "target_competencies": ["Competencia experta"],
        "evaluations": ["Demostración de seriabilidad, recuperación ARIES y optimización de consultas"],
        "next_specializations": ["Motores de almacenamiento distribuido", "Sistemas OLAP columnares"]
    },
    {
        "id": "ruta-18-compiladores",
        "title": "18. Diseño de Lenguajes de Programación, Compiladores y Runtimes",
        "prerequisites": ["Autómatas, grafos, árboles y sistemas de tipos"],
        "recommended_order": [
            "vol01-historia-y-fundamentos:cap07..cap08",
            "vol02-algoritmos-y-sistemas:cap06..cap07",
            "vol03-monografia-rust:cap01..cap07",
            "vol07-monografias-sql-shell-funcional-especializados:cap06..cap07"
        ],
        "essential_projects": ["Lexer, parser Pratt, inferidor de tipos Hindley-Milner y máquina virtual de bytecode verificada"],
        "target_competencies": ["Competencia experta"],
        "evaluations": ["Transformación a forma SSA, análisis de liveness y corrección semántica"],
        "next_specializations": ["Optimización en LLVM/MLIR", "Diseño de máquinas virtuales JIT"]
    },
    {
        "id": "ruta-19-hpc",
        "title": "19. Software de Alto Rendimiento (HPC), Concurrencia y Baja Latencia",
        "prerequisites": ["Jerarquía de cachés, modelo de memoria y perfilado"],
        "recommended_order": [
            "vol02-algoritmos-y-sistemas:cap05..cap06",
            "vol03-monografia-rust:cap05..cap07",
            "vol04-monografias-c-cpp-sistemas:cap04..cap08"
        ],
        "essential_projects": ["Planificador concurrente lock-free / work-stealing y benchmark estadístico de latencia p99"],
        "target_competencies": ["Competencia experta"],
        "evaluations": ["Alineamiento a líneas de caché (64 B), ordenamiento de memoria atómica y Roofline model"],
        "next_specializations": ["Cálculo distribuido MPI/GPU", "Sistemas financieros y aeroespaciales de baja latencia"]
    }
]

CURRICULUM_COVERAGE = {
    "reference_frameworks": [
        "ACM/IEEE-CS/AAAI Computer Science Curricula 2023 (CS2023)",
        "IEEE Computer Society SWEBOK v4.0",
        "MIT 6.006 / 6.031 / 6.172 / 6.824 & CMU 15-213 / 15-445"
    ],
    "matrix": [
        {"area": "CS2023-SDF: Software Development Fundamentals", "volumes": ["vol01-historia-y-fundamentos", "vol03-monografia-rust", "vol05-monografias-python-js-ts"], "status": "COMPLETE"},
        {"area": "CS2023-DM: Discrete Structures & Formal Logic", "volumes": ["vol01-historia-y-fundamentos", "vol02-algoritmos-y-sistemas"], "status": "COMPLETE"},
        {"area": "CS2023-AL: Algorithms and Complexity", "volumes": ["vol02-algoritmos-y-sistemas"], "status": "COMPLETE"},
        {"area": "CS2023-AR & SF: Architecture and Systems Fundamentals", "volumes": ["vol01-historia-y-fundamentos", "vol02-algoritmos-y-sistemas", "vol04-monografias-c-cpp-sistemas"], "status": "COMPLETE"},
        {"area": "CS2023-OS: Operating Systems", "volumes": ["vol02-algoritmos-y-sistemas", "vol04-monografias-c-cpp-sistemas"], "status": "COMPLETE"},
        {"area": "CS2023-FPL: Foundations of Programming Languages & Compilers", "volumes": ["vol01-historia-y-fundamentos", "vol02-algoritmos-y-sistemas", "vol03-monografia-rust", "vol04-monografias-c-cpp-sistemas", "vol05-monografias-python-js-ts", "vol06-monografias-jvm-dotnet-go-movil", "vol07-monografias-sql-shell-funcional-especializados"], "status": "COMPLETE"},
        {"area": "CS2023-IM: Information Management & Databases", "volumes": ["vol07-monografias-sql-shell-funcional-especializados", "vol08-web-bases-de-datos-y-frameworks"], "status": "COMPLETE"},
        {"area": "CS2023-PDC: Parallel and Distributed Computing", "volumes": ["vol02-algoritmos-y-sistemas", "vol03-monografia-rust", "vol06-monografias-jvm-dotnet-go-movil", "vol09-ingenieria-software-arquitectura-y-proyectos"], "status": "COMPLETE"},
        {"area": "CS2023-SE & SWEBOK v4.0: Software Engineering & Architecture", "volumes": ["vol08-web-bases-de-datos-y-frameworks", "vol09-ingenieria-software-arquitectura-y-proyectos"], "status": "COMPLETE"},
        {"area": "CS2023-SEC: Software & Systems Security", "volumes": ["vol03-monografia-rust", "vol04-monografias-c-cpp-sistemas", "vol05-monografias-python-js-ts", "vol09-ingenieria-software-arquitectura-y-proyectos"], "status": "COMPLETE"}
    ],
    "languages_covered": {
        "priority_16": [
            "Rust", "C", "C++", "C#", "Python", "JavaScript", "TypeScript", "Java",
            "Go", "Kotlin", "Swift", "PHP", "Ruby", "Dart", "SQL", "Bash / POSIX Shell"
        ],
        "additional_19": [
            "Scala", "R", "Julia", "Lua", "Zig", "Elixir", "Erlang", "Haskell",
            "F#", "OCaml", "Clojure", "Lisp / Scheme", "Fortran", "Ada", "Perl",
            "Objective-C", "Assembly (ARM64 aarch64 & x86-64)", "Prolog", "GDScript"
        ],
        "web_markup_styles_data_9": [
            "HTML Living Standard", "CSS3 / Modern CSS", "JSON & JSON Schema", "YAML 1.2",
            "TOML", "XML", "Markdown", "CSV", "Protocol Buffers"
        ]
    }
}

PREREQUISITE_DAG = {
    "description": "Directed Acyclic Graph (DAG) of conceptual prerequisites. Note: every language monograph in Part V is pedagogically autonomous and includes self-contained explanations so a reader can start directly in any language monograph.",
    "edges": [
        {"from": "vol01-historia-y-fundamentos:cap04-representacion-binaria-ieee754-utf8", "to": "vol02-algoritmos-y-sistemas:cap06-jerarquia-memoria-caches-abi-enlazado"},
        {"from": "vol01-historia-y-fundamentos:cap05-logica-algebra-booleana-matematica-discreta", "to": "vol02-algoritmos-y-sistemas:cap01-complejidad-asintotica-recurrencias-amortizado"},
        {"from": "vol02-algoritmos-y-sistemas:cap01-complejidad-asintotica-recurrencias-amortizado", "to": "vol02-algoritmos-y-sistemas:cap02-busqueda-ordenacion-cotas-inferiores"},
        {"from": "vol02-algoritmos-y-sistemas:cap02-busqueda-ordenacion-cotas-inferiores", "to": "vol02-algoritmos-y-sistemas:cap03-divide-venceras-voraces-programacion-dinamica"},
        {"from": "vol02-algoritmos-y-sistemas:cap03-divide-venceras-voraces-programacion-dinamica", "to": "vol02-algoritmos-y-sistemas:cap04-grafos-arboles-equilibrados-hashing"},
        {"from": "vol02-algoritmos-y-sistemas:cap04-grafos-arboles-equilibrados-hashing", "to": "vol08-web-bases-de-datos-y-frameworks:cap05-bases-datos-indices-btree-planificadores-transacciones-acid-mvcc"},
        {"from": "vol03-monografia-rust:cap01-rust-introduccion-filosofia-toolchain-cargo", "to": "vol03-monografia-rust:cap02-rust-principiante-sintaxis-tipos-control-colecciones"},
        {"from": "vol03-monografia-rust:cap02-rust-principiante-sintaxis-tipos-control-colecciones", "to": "vol03-monografia-rust:cap03-rust-ownership-borrowing-lifetimes-memoria"},
        {"from": "vol03-monografia-rust:cap03-rust-ownership-borrowing-lifetimes-memoria", "to": "vol03-monografia-rust:cap04-rust-intermedio-enums-traits-generics-errores-testing"},
        {"from": "vol03-monografia-rust:cap04-rust-intermedio-enums-traits-generics-errores-testing", "to": "vol03-monografia-rust:cap05-rust-avanzado-closures-iteradores-smart-pointers-interior-mutability"},
        {"from": "vol03-monografia-rust:cap05-rust-avanzado-closures-iteradores-smart-pointers-interior-mutability", "to": "vol03-monografia-rust:cap06-rust-concurrencia-send-sync-async-tokio-pinning"},
        {"from": "vol03-monografia-rust:cap06-rust-concurrencia-send-sync-async-tokio-pinning", "to": "vol03-monografia-rust:cap07-rust-experto-unsafe-ffi-macros-layout-wasm-embedded"},
        {"from": "vol03-monografia-rust:cap07-rust-experto-unsafe-ffi-macros-layout-wasm-embedded", "to": "vol03-monografia-rust:cap08-rust-ecosistema-arquitectura-proyectos-evaluacion"}
    ]
}

def main() -> None:
    BLUEPRINT_DIR.mkdir(parents=True, exist_ok=True)
    (BLUEPRINT_DIR / "sources-catalog.json").write_text(
        json.dumps(SOURCES_CATALOG, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    (BLUEPRINT_DIR / "master-blueprint.json").write_text(
        json.dumps(MASTER_BLUEPRINT, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    (BLUEPRINT_DIR / "learning-paths.json").write_text(
        json.dumps(LEARNING_PATHS, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    (BLUEPRINT_DIR / "curriculum-coverage.json").write_text(
        json.dumps(CURRICULUM_COVERAGE, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    (BLUEPRINT_DIR / "prerequisite-dag.json").write_text(
        json.dumps(PREREQUISITE_DAG, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print("Generated 5 master blueprint & curriculum JSON artifacts in", BLUEPRINT_DIR)

if __name__ == "__main__":
    main()
