#!/usr/bin/env python3
"""Construcción completa de los Volúmenes 6 y 7 de la Enciclopedia:
- vol06-monografias-jvm-dotnet-go-movil (Parte V — Monografías Completas de C#, Java, Go, Kotlin y Swift)
- vol07-monografias-sql-shell-funcional-especializados (Parte V — Monografías de SQL, Bash/POSIX, PHP, Ruby, Dart, Haskell, OCaml, F#, Scala, Elixir, Erlang, Clojure, Lisp/Scheme, Julia, R, Lua, Perl, Objective-C, Prolog y GDScript)
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from studium_volume_helper import ROOT, build_studium_volume  # noqa: E402

VOL06_SPEC: dict[str, object] = {
    "slug": "vol06-monografias-jvm-dotnet-go-movil",
    "code": "ENC-VOL06",
    "title": "Volumen VI: Monografías de C#, Java, Go, Kotlin y Swift",
    "subtitle": "Parte V (Bloques A–H): Máquinas virtuales gestionadas (CLR y JVM), concurrencia G-M-P en Go, Coroutines y ARC/Actores",
    "target_pages": 68,
    "terminology": [
        {"term": "hilo virtual (Virtual Thread)", "canonical": "hilo virtual (Virtual Thread)", "forbidden": ["hilo verde pesado"]},
        {"term": "conteo automático de referencias (ARC)", "canonical": "ARC (Automatic Reference Counting)", "forbidden": ["recolector de barrido Swift"]},
        {"term": "planificador M:N (G-M-P)", "canonical": "planificador M:N (G-M-P)", "forbidden": ["planificador 1:1 de goroutines"]},
    ],
    "notation": [
        {"symbol": r"G, M, P", "meaning": "Goroutine, Machine (hilo OS) y Processor (contexto lógico) en el runtime de Go", "unit": "entidades"},
        {"symbol": r"\text{Span}\langle T \rangle", "meaning": "Vista contigua de memoria alojada en pila (ref struct) sin asignación en el montículo en .NET", "unit": "vista"},
        {"symbol": r"\text{ARC}(o)", "meaning": "Contador fuerte/débil/unowned gestionado en compilación en Swift", "unit": "referencias"},
    ],
    "chapters": [
        {
            "id": "cap01-csharp-dotnet-clr-tipos-valor-referencia-linq",
            "title": "Monografía de C# (I — Bloques A–D): Arquitectura .NET/CLR, Tipos Valor vs Referencia, Records, Pattern Matching y LINQ",
            "part_id": "parte-v-csharp-java",
            "part_title": "Monografías de Plataformas Gestionadas: C# (.NET 8/9) y Java (JVM 21 LTS)",
            "sources": ["src-csharp-spec", "src-gamma-gof"],
            "learning_objectives": [
                "Comprender la arquitectura del Common Language Runtime (CLR), el lenguaje intermedio CIL, la compilación JIT (RyuJIT) y Native AOT en .NET 8/9.",
                "Distinguir con precisión semántica y espacial entre tipos por valor (`struct`, `readonly struct`, `ref struct`) y tipos por referencia (`class`, `record`), evitando el boxing involuntario.",
                "Dominar la nulabilidad verificada (`string?`), coincidencia de patrones avanzada y consultas declarativas con LINQ (`IEnumerable<T>` vs `IQueryable<T>`).",
            ],
            "concepts": [
                {"id": "cpt-cs-clr-value-ref-types", "title": "Arquitectura CLR/RyuJIT, distinción struct vs class, boxing/unboxing y reificación de genéricos en .NET"},
                {"id": "cpt-cs-records-linq-iqueryable", "title": "Inmutabilidad estructural con record, pattern matching y árboles de expresión en LINQ"},
            ],
            "subsections": [
                {"id": "sec-v6-1-1", "title": "Bloques A–C: Historia de C# y .NET, CLI (`dotnet`), CIL, tipos valor vs referencia y nulabilidad"},
                {"id": "sec-v6-1-2", "title": "Bloque D: Propiedades, records, interfaces, genéricos reificados, delegados y LINQ"},
            ],
            "purpose": (
                "Este capítulo inicia la monografía autónoma de **C# (.NET 8/9)** (Bloques A, B, C y D). Diseñado por Anders "
                "Hejlsberg, C# combina la ergonomía expresiva de los lenguajes funcionales modernos con un control de bajo nivel "
                "sobre la disposición de memoria (`struct`, `Span<T>`, genéricos reificados en la máquina virtual) único entre "
                "los entornos gestionados."
            ),
            "paragraphs": [
                {
                    "subsection": "sec-v6-1-1",
                    "text": (
                        "En la plataforma **.NET**, el compilador Roslyn (`csc`) traduce el código fuente C# a *Common Intermediate "
                        "Language* (CIL, estándar ECMA-335) almacenado en ensamblados `.dll`. Durante la ejecución, el compilador "
                        "JIT **RyuJIT** traduce los métodos CIL a código máquina nativo aplicando compilación por niveles (*Tiered "
                        "Compilation*) y perfilado dinámico (Dynamic PGO), o bien compila directamente a binario nativo autónomo "
                        "mediante **Native AOT**. Una decisión crucial de ingeniería en C# es la distinción entre **tipos por referencia** "
                        "(`class`, alojados en el montículo gestionado con una cabecera de objeto de 16 bytes en 64 bits) y **tipos "
                        "por valor** (`struct`, alojados en línea en el marco de pila o directamente dentro del array/objeto contenedor "
                        "sin indirección de puntero). Además, a diferencia de la JVM, el CLR **reifica los tipos genéricos**: "
                        "`List<int>` o `Dictionary<long, double>` generan código máquina especializado con arrays planos de valores "
                        "primitivos sin *boxing*."
                    ),
                },
                {
                    "subsection": "sec-v6-1-2",
                    "text": (
                        "C# moderno incorpora tipos de referencia anulables verificados por flujo (`<Nullable>enable</Nullable>`), "
                        "tipos de datos inmutables por valor o referencia (`readonly record struct` y `record class`) con igualdad "
                        "estructural sintetizada y **LINQ** (*Language Integrated Query*). En LINQ es indispensable distinguir entre "
                        "`IEnumerable<T>`, cuyos operadores reciben delegados `Func<T, bool>` evaluados en memoria en el proceso actual, "
                        "e `IQueryable<T>`, cuyos operadores reciben árboles de expresión (`Expression<Func<T, bool>>`) que un proveedor "
                        "como Entity Framework Core inspecciona para traducirlos a consultas SQL ejecutadas en el motor de base de datos:\n"
                        "```csharp\n"
                        "public readonly record struct SensorSample(int SensorId, double Value, long TimestampMs);\n\n"
                        "public static double ComputeHighValueAverage(ReadOnlySpan<SensorSample> samples, double threshold)\n"
                        "{\n"
                        "    double sum = 0.0;\n"
                        "    int count = 0;\n"
                        "    foreach (ref readonly var s in samples)\n"
                        "    {\n"
                        "        if (s.Value >= threshold) { sum += s.Value; count++; }\n"
                        "    }\n"
                        "    return count > 0 ? sum / count : 0.0;\n"
                        "}\n"
                        "```\n"
                        "Observa cómo `foreach (ref readonly var s in samples)` sobre un `ReadOnlySpan<SensorSample>` recorre las "
                        "estructuras contiguas por referencia constante sin realizar ni una sola copia ni alojar un iterador en el montículo."
                    ),
                },
            ],
            "definition": (
                "Reificación de Genéricos en el CLR (.NET): preservación de los argumentos de tipo genérico en los metadatos "
                "CIL y en tiempo de ejecución, permitiendo que el JIT emita representaciones especializadas en memoria para "
                "cada tipo por valor (`struct`) sin encajonamiento (*boxing*)."
            ),
            "consejo": (
                "Cuando declares un `struct` en C#, márcalo como `readonly struct` (o `readonly record struct`) siempre que sea "
                "posible: si pasas un `struct` no `readonly` mediante `in` o lo almacenas en un campo `readonly`, el compilador "
                "se ve obligado a emitir copias defensivas ocultas en cada llamada a método para proteger el original."
            ),
            "self_check": (
                "¿Qué problema grave de rendimiento ocurre en una base de datos de millones de filas si un desarrollador convierte "
                "un `IQueryable<Order>` de EF Core a `IEnumerable<Order>` mediante `.AsEnumerable()` o `.ToList()` **antes** "
                "de aplicar `.Where(...)`?"
            ),
            "derivation": {
                "title": "Ahorro de memoria de un array de struct reificado en C# frente a referencias encajonadas (boxed)",
                "assumptions": ["Un array de N estructuras de tamaño S_val bytes ocupa N * S_val bytes en C#; si fueran objetos por referencia en 64 bits cada uno añadiría 8 B de puntero + 16 B de cabecera de objeto (Object Header + MethodTable)"],
                "steps": [
                    {"equation": r"M_{\text{struct}} = N \cdot S_{\text{val}}", "justification": "Almacenamiento contiguo en línea sin punteros ni cabeceras individuales"},
                    {"equation": r"M_{\text{ref}} = N \cdot (24 + S_{\text{val}})", "justification": "8 B de referencia en el array + 16 B de cabecera en el montículo + campos por cada instancia"},
                ],
                "Verify": {"left": "N * (24 + S_val) - N * S_val", "right": "24 * N"},
            },
            "worked_problem": {
                "prompt": (
                    "En una aplicación financiera en C# sobre .NET de 64 bits, se mantiene un búfer de $N = 100000$ cotizaciones "
                    "donde cada cotización tiene $S_{\\text{val}} = 16\\text{ B}$ de datos (`long Timestamp`, `double Price`). "
                    "Si se modela como `readonly record struct`, el array `Quote[]` ocupa $100000 \\times 16\\text{ B}$. Si se "
                    "modelara como `class`, cada elemento añadiría $8\\text{ B}$ de puntero en el array más $16\\text{ B}$ de "
                    "cabecera de objeto en el montículo ($24\\text{ B}$ extra por instancia). Calcula cuántos kilobytes (dividiendo "
                    "entre 1000) ahorra el diseño con `struct`."
                ),
                "expression": "(100000 * 24) / 1000",
                "solution": {
                    "model": "Ahorro de memoria entre array de struct y array de class en el CLR (.NET)",
                    "given": [
                        {"symbol": "N", "value": "100000", "description": "Número de cotizaciones en el array"},
                        {"symbol": "S_extra", "value": "24 B", "description": "Sobrecoste por instancia de class (8 B ref + 16 B cabecera)"},
                    ],
                    "steps": [
                        {"step": "Multiplicamos las 100000 instancias por 24 B y dividimos entre 1000 B/kB", "equation": r"\Delta M_{\text{kB}} = \frac{100000 \cdot 24}{1000}", "expression": "(100000 * 24) / 1000"},
                    ],
                    "conclusion": "El diseño con readonly record struct ahorra 2400 kB (2.4 MB) y elimina 100 000 nodos del grafo del recolector de basura.",
                },
            },
            "practice_problems": [
                {"prompt": "En .NET de 64 bits, la cabecera de todo objeto por referencia (`class`) consta de `ObjHeader` (8 B) y `MethodTable*` (8 B). ¿Cuántos bytes suma esta cabecera?", "expression": "8 + 8", "difficulty": "FOUNDATIONAL", "problem_type": "DIRECT_SUBSTITUTION"},
                {"prompt": "Un `readonly record struct Point3D(double X, double Y, double Z)` contiene tres `double` de 8 bytes. ¿Cuántos bytes ocupa cada instancia?", "expression": "3 * 8", "difficulty": "FOUNDATIONAL", "problem_type": "DIRECT_SUBSTITUTION"},
                {"prompt": "Una consulta LINQ encadena `.Where(...)` y `.Take(25)` sobre una secuencia perezosa de 10 000 elementos donde se cumple el predicado en 1 de cada 4 elementos. ¿Cuántos elementos evalúa antes de detenerse ($25 \\times 4$)?", "expression": "25 * 4", "difficulty": "INTERMEDIATE", "problem_type": "MULTI_STEP"},
                {"prompt": "El recolector generacional del CLR divide el montículo de objetos pequeños en 3 generaciones (`Gen 0`, `Gen 1`, `Gen 2`). Si `Gen 0` tiene un presupuesto de 4 MiB y `Gen 1` de 2 MiB, ¿cuántos KiB suman las dos generaciones efímeras ($(4 + 2) \\times 1024$)?", "expression": "(4 + 2) * 1024", "difficulty": "INTERMEDIATE", "problem_type": "DESIGN"},
            ],
        },
        {
            "id": "cap02-csharp-avanzado-experto-span-async-valuetask-aspnet-proyectos",
            "title": "Monografía de C# (II — Bloques E–H): Span<T>, Memory<T>, Async/Await, ValueTask, ASP.NET Core y Proyectos",
            "part_id": "parte-v-csharp-java",
            "part_title": "Monografías de Plataformas Gestionadas: C# (.NET 8/9) y Java (JVM 21 LTS)",
            "sources": ["src-csharp-spec", "src-kleppmann-ddia"],
            "learning_objectives": [
                "Programar procesamiento de alto rendimiento sin asignaciones en el montículo usando `Span<T>`, `ReadOnlySpan<T>`, `Memory<T>`, `ArrayPool<T>` y `System.IO.Pipelines`.",
                "Comprender la máquina de estados generada por el compilador para `async`/`await`, cuándo utilizar `ValueTask<T>` frente a `Task<T>` y la propagación de `CancellationToken`.",
                "Dominar el ecosistema empresarial de .NET (ASP.NET Core, inyección de dependencias, EF Core, Dapper, xUnit, BenchmarkDotNet) y los 4 proyectos integradores.",
            ],
            "concepts": [
                {"id": "cpt-cs-span-memory-pipelines", "title": "Seguridad en pila de ref struct (Span<T>), buffers alquilados (ArrayPool<T>) y máquinas de estados ValueTask<T>"},
                {"id": "cpt-cs-aspnet-di-projects", "title": "Ciclos de vida de inyección de dependencias (Transient, Scoped, Singleton) y arquitectura en .NET"},
            ],
            "subsections": [
                {"id": "sec-v6-2-1", "title": "Bloques E y F: Span<T>, ref struct, ArrayPool<T>, máquinas de estados async/await, ValueTask<T> y Channels"},
                {"id": "sec-v6-2-2", "title": "Bloques G y H: Ecosistema (ASP.NET Core, DI, EF Core, xUnit, BenchmarkDotNet) y los 4 proyectos en C#"},
            ],
            "purpose": (
                "Este capítulo completa la monografía de C# cubriendo los niveles Avanzado y Experto (Bloques E y F), el "
                "Ecosistema empresarial (Bloque G) y los Proyectos (Bloque H). Explicamos cómo las primitivas `Span<T>` y "
                "`ValueTask<T>` han situado a ASP.NET Core (Kestrel) entre los servidores web más rápidos del mundo."
            ),
            "paragraphs": [
                {
                    "subsection": "sec-v6-2-1",
                    "text": (
                        "Para permitir el acceso uniforme y sin copias a memoria gestionada (`T[]`), memoria en pila (`stackalloc`) "
                        "y memoria nativa no gestionada, C# 7.2+ introdujo `Span<T>` y `ReadOnlySpan<T>`. Un `Span<T>` se declara "
                        "como `ref struct`, lo que significa que el compilador y el verificador del CLR prohíben estáticamente que "
                        "escape al montículo (no puede ser un campo de una `class`, ni ser encajonado como `object`, ni capturarse "
                        "en una lambda, ni cruzar un punto `await`). En programación asíncrona, cada método `async` es transformado "
                        "por el compilador en una estructura que implementa `IAsyncStateMachine`. Si un método `async Task<T>` "
                        "completa su trabajo de forma asíncrona, aloja un objeto `Task<T>` en el montículo; pero en rutas calientes "
                        "(como lecturas desde caché o sockets con datos ya presentes en el búfer del kernel) donde el 90 % de las "
                        "llamadas se resuelven síncronamente, devolver `ValueTask<T>` (un `readonly struct`) evita por completo "
                        "cualquier asignación en el montículo:\n"
                        "```csharp\n"
                        "using System.Buffers;\n"
                        "using System.Threading;\n"
                        "using System.Threading.Tasks;\n\n"
                        "public sealed class CachedMetricReader\n"
                        "{\n"
                        "    private double? _cached;\n"
                        "    public ValueTask<double> ReadMetricAsync(CancellationToken ct)\n"
                        "    {\n"
                        "        if (_cached is double ready)\n"
                        "            return new ValueTask<double>(ready); // 0 bytes alojados en el montículo\n"
                        "        return new ValueTask<double>(FetchSlowAsync(ct));\n"
                        "    }\n"
                        "    private async Task<double> FetchSlowAsync(CancellationToken ct)\n"
                        "    {\n"
                        "        await Task.Delay(10, ct).ConfigureAwait(false);\n"
                        "        _cached = 42.5;\n"
                        "        return 42.5;\n"
                        "    }\n"
                        "}\n"
                        "```\n"
                        "Recuerda la restricción contractual de `ValueTask<T>`: nunca debe ser esperado (`await`) más de una vez ni "
                        "consumido concurrentemente antes de que complete."
                    ),
                },
                {
                    "subsection": "sec-v6-2-2",
                    "text": (
                        "En el Bloque G (Ecosistema), las aplicaciones .NET modernas se construyen sobre el contenedor de **Inyección "
                        "de Dependencias (DI)** integrado en `Microsoft.Extensions.DependencyInjection`, que distingue tres ciclos "
                        "de vida: `Transient` (una instancia nueva en cada resolución), `Scoped` (una instancia única por ámbito o "
                        "petición HTTP, obligatoria para `DbContext` de Entity Framework Core) y `Singleton` (una única instancia "
                        "segura para hilos durante toda la vida del proceso). Un antipatrón crítico (detectado automáticamente por "
                        "`ValidateScopes = true` en entorno de desarrollo) es la **dependencia cautiva** (*Captive Dependency*): "
                        "inyectar un servicio `Scoped` dentro de un `Singleton`, lo que retiene el servicio `Scoped` indefinidamente "
                        "y provoca accesos concurrentes ilegales a `DbContext`."
                    ),
                },
            ],
            "definition": (
                "Estructura restringida a pila (`ref struct` en C#): tipo por valor cuya ubicación está garantizada estáticamente "
                "por el compilador y el verificador del CLR exclusivamente en la pila de ejecución, permitiendo contener "
                "punteros interiores gestionados (`ref T` en `Span<T>`) seguros frente a compactaciones del recolector de basura."
            ),
            "consejo": (
                "En todos los métodos asíncronos de entrada/salida en C#, acepta siempre un `CancellationToken ct = default` "
                "como último parámetro y pásalo hacia abajo a todas las llamadas de red y base de datos para abortar el trabajo "
                "inmediatamente cuando el cliente HTTP cierra la conexión."
            ),
            "self_check": (
                "¿Por qué un objeto `Span<byte>` no puede ser un campo de una clase ni persistir a través de una expresión `await` "
                "en un método `async`?"
            ),
            "derivation": {
                "title": "Reducción de presión sobre el recolector de basura (Gen 0) usando ValueTask<T> en aciertos de caché",
                "assumptions": ["En R peticiones por segundo con tasa de acierto síncrono h, Task<T> no cacheable aloja S_task bytes por petición mientras que ValueTask<T> aloja 0 bytes en los R * h aciertos"],
                "steps": [
                    {"equation": r"A_{\text{Task}} = R \cdot S_{\text{task}}", "justification": "Asignación de un objeto Task<T> cuando el resultado no es un primitivo pre-cacheado"},
                    {"equation": r"A_{\text{ValueTask}} = R \cdot (1 - h) \cdot S_{\text{task}}", "justification": "ValueTask<T> solo aloja un Task<T> subyacente en la fracción (1 - h) de fallos asíncronos"},
                ],
                "Verify": {"left": "R * S_task - R * (1 - h) * S_task", "right": "R * h * S_task"},
            },
            "worked_problem": {
                "prompt": (
                    "Un servicio de alta frecuencia en ASP.NET Core procesa $R = 50000$ llamadas por segundo donde el $90\\%$ "
                    "($45000$ llamadas/s) se resuelven síncronamente desde memoria local y solo el $10\\%$ ($5000$ llamadas/s) "
                    "requieren E/S asíncrona real. Si cada objeto `Task<Result>` alojado en el montículo mide $S_{\\text{task}} = 72\\text{ B}$, "
                    "calcula cuántos kilobytes por segundo (dividiendo entre 1000) deja de alojar en `Gen 0` el servicio al "
                    "cambiar el tipo de retorno de `Task<Result>` a `ValueTask<Result>`."
                ),
                "expression": "(45000 * 72) / 1000",
                "solution": {
                    "model": "Ahorro de asignaciones en Gen 0 con ValueTask<T> en rutas calientes",
                    "given": [
                        {"symbol": "R_sync", "value": "45000 llamadas/s", "description": "Llamadas resueltas síncronamente por segundo"},
                        {"symbol": "S_task", "value": "72 B", "description": "Tamaño del objeto Task<Result> evitado"},
                    ],
                    "steps": [
                        {"step": "Multiplicamos las 45000 llamadas síncronas por 72 B y dividimos entre 1000 B/kB", "equation": r"\Delta A_{\text{kB/s}} = \frac{45000 \cdot 72}{1000}", "expression": "(45000 * 72) / 1000"},
                    ],
                    "conclusion": "Se evita alojar y recolectar 3240 kB/s (3.24 MB/s) de objetos efímeros en Gen 0.",
                },
            },
            "practice_problems": [
                {"prompt": "En .NET de 64 bits, un `Span<byte>` contiene una referencia interior `ref byte` (8 B) y una longitud `int` alineada a 8 B. ¿Cuántos bytes ocupa en la pila?", "expression": "8 + 8", "difficulty": "FOUNDATIONAL", "problem_type": "DIRECT_SUBSTITUTION"},
                {"prompt": "Si se alquila un búfer con `ArrayPool<byte>.Shared.Rent(4000)`, el pool devuelve un array cuya longitud es la siguiente potencia de dos ($4096$). ¿Cuántos bytes adicionales respecto a los 4000 solicitados tiene el array devuelto?", "expression": "4096 - 4000", "difficulty": "FOUNDATIONAL", "problem_type": "DIRECT_SUBSTITUTION"},
                {"prompt": "Un canal acotado `Channel.CreateBounded<Job>(new BoundedChannelOptions(128))` contiene actualmente 95 trabajos. ¿Cuántos trabajos más pueden escribirse sin suspender al productor?", "expression": "128 - 95", "difficulty": "INTERMEDIATE", "problem_type": "MULTI_STEP"},
                {"prompt": "Un contenedor de inyección de dependencias resuelve por cada petición HTTP 1 servicio `Singleton` (ya creado), 2 servicios `Scoped` y 4 servicios `Transient` (invocados 2 veces cada uno en la petición). ¿Cuántas instancias nuevas se crean durante esa petición ($2 + 4 \\times 2$)?", "expression": "2 + 4 * 2", "difficulty": "INTERMEDIATE", "problem_type": "DESIGN"},
            ],
        },
        {
            "id": "cap03-java-jvm-bytecode-memoria-generics-streams",
            "title": "Monografía de Java (I — Bloques A–D): Arquitectura JVM, Bytecode, Memoria, Records, Sealed Classes, Generics y Streams",
            "part_id": "parte-v-csharp-java",
            "part_title": "Monografías de Plataformas Gestionadas: C# (.NET 8/9) y Java (JVM 21 LTS)",
            "sources": ["src-java-jls21", "src-gamma-gof"],
            "learning_objectives": [
                "Explicar la arquitectura de la Java Virtual Machine (JVM): subsistema ClassLoader, áreas de memoria (Heap, Metaspace, pilas de hilo), intérprete y compiladores JIT C1/C2.",
                "Dominar las innovaciones de Java 17/21 LTS: `record`, `sealed interface`/`permits`, coincidencia de patrones en `switch` y desestructuración de records.",
                "Aplicar genéricos con comodines acotados (principio PECS: Producer Extends, Consumer Super), colecciones (`ArrayList`, `HashMap`, `ConcurrentHashMap`) y la API `Stream<T>`.",
            ],
            "concepts": [
                {"id": "cpt-java-jvm-jit-gc", "title": "Arquitectura HotSpot JVM, compilación escalonada C1/C2 y recolectores G1GC y ZGC Generacional"},
                {"id": "cpt-java-records-sealed-pecs", "title": "Modelado algebraico de datos en Java 21 (records + sealed interfaces), principio PECS y Streams"},
            ],
            "subsections": [
                {"id": "sec-v6-3-1", "title": "Bloques A–C: Evolución hasta Java 21 LTS, arquitectura JVM, JIT C1/C2, G1/ZGC y sintaxis fundamental"},
                {"id": "sec-v6-3-2", "title": "Bloque D: Records, Sealed Classes, Pattern Matching, Genéricos (PECS), Colecciones y Streams API"},
            ],
            "purpose": (
                "Este capítulo inicia la monografía autónoma de **Java (Java 21 LTS)** (Bloques A, B, C y D). Java impulsa la "
                "infraestructura crítica financiera, bancaria y de comercio electrónico a escala planetaria, y con la llegada de "
                "Java 17 y Java 21 LTS ha incorporado tipos algebraicos de datos (`record` + `sealed interface`) e hilos virtuales "
                "que transforman por completo la escritura de código en la JVM."
            ),
            "paragraphs": [
                {
                    "subsection": "sec-v6-3-1",
                    "text": (
                        "Creado por James Gosling en Sun Microsystems en 1995, Java compila los ficheros `.java` mediante `javac` a "
                        "código de bytes de pila (`.class`) independiente de la arquitectura física. En tiempo de ejecución, la máquina "
                        "virtual **HotSpot** aplica compilación escalonada (*Tiered Compilation*): comienza interpretando el bytecode "
                        "(Nivel 0), compila métodos frecuentes con el compilador rápido C1 recolectando perfiles de ejecución (Niveles 1–3) "
                        "y finalmente optimiza el código caliente con el compilador servidor **C2** (Nivel 4), capaz de desvirtualizar "
                        "llamadas polimórficas monomórficas/bimórficas y aplicar análisis de escape (*Escape Analysis*) para alojar "
                        "objetos efímeros en registros o escalarizarlos en la pila. Para la gestión del montículo, Java 21 ofrece "
                        "**G1GC** (recolector regional por defecto) y **Generational ZGC** (`-XX:+UseZGC -XX:+ZGenerational`), un "
                        "recolector concurrente con barreras de punteros coloreados (*colored pointers*) cuyas pausas *Stop-The-World* "
                        "son inferiores a $1\\text{ ms}$ incluso en montículos de varios terabytes."
                    ),
                },
                {
                    "subsection": "sec-v6-3-2",
                    "text": (
                        "Java 17 y Java 21 LTS introdujeron el paradigma de **Programación Orientada a Datos** (*Data-Oriented "
                        "Programming*): la combinación de clases `record` (portadores transparentes e inmutables de datos), interfaces "
                        "selladas (`sealed interface ... permits ...`) y coincidencia de patrones exhaustiva en expresiones `switch` "
                        "con desestructuración:\n"
                        "```java\n"
                        "public sealed interface PaymentResult permits PaymentResult.Approved, PaymentResult.Declined {\n"
                        "    record Approved(String txId, long cents) implements PaymentResult {}\n"
                        "    record Declined(String reason, int retryAfterSec) implements PaymentResult {}\n\n"
                        "    static String describe(PaymentResult res) {\n"
                        "        return switch (res) {\n"
                        "            case Approved(var id, var cents) when cents >= 100_00 -> \"High-value approved: \" + id;\n"
                        "            case Approved(var id, var cents)                      -> \"Approved: \" + id + \" (\" + cents + \")\";\n"
                        "            case Declined(var reason, var wait)                   -> \"Declined (\" + reason + \"), wait \" + wait + \"s\";\n"
                        "        };\n"
                        "    }\n"
                        "}\n"
                        "```\n"
                        "En el sistema de tipos genéricos de Java (implementado con borrado de tipos a `Object` o a su cota superior "
                        "para mantener compatibilidad binaria), la varianza en sitios de uso se rige por la regla **PECS** (*Producer "
                        "Extends, Consumer Super*, formulada por Joshua Bloch): usa `List<? extends T>` cuando solo leas elementos `T` "
                        "de la estructura productora, y `Comparator<? super T>` o `Collection<? super T>` cuando insertes o consumas "
                        "elementos `T`."
                    ),
                },
            ],
            "definition": (
                "Principio PECS (Producer Extends, Consumer Super en Java): regla de varianza en el sitio de uso (*use-site "
                "variance*) según la cual una estructura parametrizada que actúa como productora de valores `T` debe tiparse "
                "de forma covariante (`? extends T`), y una que actúa como consumidora de valores `T` de forma contravariante (`? super T`)."
            ),
            "consejo": (
                "Cuando operes con flujos numéricos en la API de Streams de Java, utiliza siempre las especializaciones "
                "primitivas (`IntStream`, `LongStream`, `DoubleStream` mediante `.mapToLong(...)` o `.mapToDouble(...)`) en "
                "lugar de `Stream<Integer>` o `Stream<Double>` para evitar el encajonamiento (*boxing*) de millones de objetos."
            ),
            "self_check": (
                "¿Por qué en Java `Integer.valueOf(100) == Integer.valueOf(100)` evalúa a `true` (por la caché obligatoria de "
                "`-128` a `127` de la JLS §5.1.7), pero `Integer.valueOf(1000) == Integer.valueOf(1000)` evalúa a `false` y "
                "debe compararse siempre con `.equals()`?"
            ),
            "derivation": {
                "title": "Ahorro de memoria con Compressed OOPs (Ordinary Object Pointers) en la JVM de 64 bits",
                "assumptions": ["Para montículos <= 32 GiB con alineamiento de objetos a 8 bytes (2^3), la JVM almacena referencias en 32 bits (4 bytes) desplazadas 3 bits en lugar de 64 bits (8 bytes)"],
                "steps": [
                    {"equation": r"M_{\text{max\_heap}} = 2^{32} \cdot 8\text{ B} = 32\text{ GiB}", "justification": "Un índice de 32 bits multiplicado por la granularidad de alineamiento de 8 bytes direcciona hasta 32 GiB"},
                    {"equation": r"S_{\text{obj\_header}} = 8\text{ B (Mark Word)} + 4\text{ B (Klass Pointer)} = 12\text{ B}", "justification": "Cabecera compacta de objeto en HotSpot con -XX:+UseCompressedOops"},
                ],
                "Verify": {"left": "8 + 4", "right": "12"},
            },
            "worked_problem": {
                "prompt": (
                    "En la JVM HotSpot de 64 bits con punteros comprimidos activos (`-XX:+UseCompressedOops`), un objeto `Double` "
                    "encajonado (*boxed*) ocupa $24\\text{ B}$ (12 B de cabecera + 8 B del `double` + 4 B de relleno a múltiplo de 8), "
                    "más $4\\text{ B}$ de la referencia en un `ArrayList<Double>` ($28\\text{ B}$ por número), mientras que un array "
                    "primitivo `double[]` o un `DoubleStream` ocupa únicamente $8\\text{ B}$ por número. Calcula cuántos megabytes "
                    "(dividiendo entre $10^6$) se ahorran al almacenar $N = 2000000$ de valores en `double[]` frente a `ArrayList<Double>`."
                ),
                "expression": "(2000000 * (28 - 8)) / 1000000",
                "solution": {
                    "model": "Sobrecoste de memoria por boxing en la JVM frente a tipos primitivos",
                    "given": [
                        {"symbol": "N", "value": "2000000", "description": "Dos millones de números en coma flotante"},
                        {"symbol": "S_boxed", "value": "28 B", "description": "24 B del objeto Double + 4 B de referencia comprimida"},
                        {"symbol": "S_prim", "value": "8 B", "description": "8 B por elemento en double[]"},
                    ],
                    "steps": [
                        {"step": "Multiplicamos los 2 millones de elementos por los 20 B ahorrados y dividimos entre 10^6", "equation": r"\Delta M_{\text{MB}} = \frac{2 \cdot 10^6 \cdot (28 - 8)}{10^6}", "expression": "(2000000 * (28 - 8)) / 1000000"},
                    ],
                    "conclusion": "Usar arrays o flujos primitivos ahorra exactamente 40 MB de montículo y elimina 2 millones de objetos del recolector de basura.",
                },
            },
            "practice_problems": [
                {"prompt": "En la JVM HotSpot con Compressed OOPs, la cabecera de un objeto ordinario mide 8 B (`Mark Word`) más 4 B (`Klass Pointer`). ¿Cuántos bytes mide la cabecera antes de alinear campos?", "expression": "8 + 4", "difficulty": "FOUNDATIONAL", "problem_type": "DIRECT_SUBSTITUTION"},
                {"prompt": "En `HashMap` de Java 8+, cuando un cubo (*bucket*) alcanza el umbral `TREEIFY_THRESHOLD = 8` colisiones (con capacidad de tabla $\\ge 64$), la lista enlazada se transforma en un árbol rojo-negro. Si hay 256 elementos colisionando en ese mismo cubo, ¿cuál es la altura máxima $2 \\log_2(256)$ a comparar frente a los 256 saltos lineales?", "expression": "2 * 8", "difficulty": "FOUNDATIONAL", "problem_type": "MULTI_STEP"},
                {"prompt": "Un `ConcurrentHashMap` redimensiona su tabla de 1024 a 2048 cubos manteniendo el factor de carga en $0.75$. ¿Cuántas entradas admite la nueva tabla antes del siguiente redimensionado ($2048 \\times 3 / 4$)?", "expression": "(2048 * 3) / 4", "difficulty": "INTERMEDIATE", "problem_type": "MULTI_STEP"},
                {"prompt": "Si el tamaño de un montículo de la JVM supera los 32 GiB y desactiva Compressed OOPs, cada referencia pasa de 4 B a 8 B. En un grafo en memoria con 50 millones de referencias, ¿cuántos megabytes ($10^6\\text{ B}$) adicionales consumen las referencias?", "expression": "(50000000 * (8 - 4)) / 1000000", "difficulty": "INTERMEDIATE", "problem_type": "DESIGN"},
            ],
        },
        {
            "id": "cap04-java-avanzado-experto-virtual-threads-jmm-spring-proyectos",
            "title": "Monografía de Java (II — Bloques E–H): Java Memory Model, Virtual Threads (Loom), Foreign Function & Memory API y Proyectos",
            "part_id": "parte-v-csharp-java",
            "part_title": "Monografías de Plataformas Gestionadas: C# (.NET 8/9) y Java (JVM 21 LTS)",
            "sources": ["src-java-jls21", "src-kleppmann-ddia"],
            "learning_objectives": [
                "Dominar el Java Memory Model (JMM, JLS §17.4): la relación de orden parcial *happens-before*, `volatile`, `VarHandle`, `CompletableFuture` y `ReentrantLock`.",
                "Escalar aplicaciones síncronas legibles a millones de tareas concurrentes mediante **Virtual Threads** (JEP 444 en Java 21 LTS) y Concurrencia Estructurada.",
                "Integrar el ecosistema empresarial de Java (Maven, Gradle, JUnit 5, Testcontainers, Spring Boot 3, Micrometer/OpenTelemetry) y construir los 4 proyectos del bloque.",
            ],
            "concepts": [
                {"id": "cpt-java-jmm-virtual-threads", "title": "Relación happens-before del JMM, hilos portadores (carrier threads) y desmontaje de Virtual Threads en E/S"},
                {"id": "cpt-java-ffm-spring-projects", "title": "API Foreign Function & Memory (Panama), ecosistema Spring Boot / Maven / JUnit 5 y proyectos"},
            ],
            "subsections": [
                {"id": "sec-v6-4-1", "title": "Bloques E y F: Java Memory Model, Virtual Threads (Project Loom), StructuredTaskScope y API Panama (FFM)"},
                {"id": "sec-v6-4-2", "title": "Bloques G y H: Ecosistema (Maven, Gradle, JUnit 5, Spring Boot, GraalVM) y los 4 proyectos en Java"},
            ],
            "purpose": (
                "Este capítulo completa la monografía de Java (Bloques E, F, G y H). Analizamos con rigor la innovación más "
                "importante de la JVM en la última década: los **Hilos Virtuales** (*Virtual Threads*, JEP 444 en Java 21 LTS), "
                "que reconcilian el modelo sencillo de un hilo por petición (*thread-per-request*) con la escalabilidad masiva "
                "de la E/S no bloqueante."
            ),
            "paragraphs": [
                {
                    "subsection": "sec-v6-4-1",
                    "text": (
                        "El **Java Memory Model (JMM)** define formalmente cuándo las escrituras de un hilo son visibles para otro "
                        "hilo a través de la relación transitiva *happens-before*: la liberación de un monitor (`synchronized` o "
                        "`Lock.unlock()`) *happens-before* toda adquisición posterior del mismo monitor, y una escritura en un campo "
                        "`volatile` *happens-before* toda lectura posterior de ese campo. En Java 21 LTS, **Project Loom** introdujo "
                        "los **Virtual Threads** (`Thread.ofVirtual().start(...)` o `Executors.newVirtualThreadPerTaskExecutor()`): "
                        "hilos gestionados por la JVM que se montan sobre un pequeño grupo de hilos del sistema operativo (*carrier "
                        "threads* en un `ForkJoinPool`). Cuando el código ejecutado dentro de un hilo virtual realiza una operación "
                        "bloqueante de red o base de datos (como `Socket.read()` o `Thread.sleep()`), el runtime de la JVM **desmonta** "
                        "automáticamente la pila de continuación del hilo virtual hacia el montículo y deja libre al hilo portador del "
                        "sistema operativo para ejecutar otro hilo virtual:\n"
                        "```java\n"
                        "import java.util.concurrent.Executors;\n"
                        "import java.util.stream.IntStream;\n\n"
                        "public final class VirtualThreadDispatcher {\n"
                        "    public static long runConcurrentTasks(int taskCount) throws Exception {\n"
                        "        try (var executor = Executors.newVirtualThreadPerTaskExecutor()) {\n"
                        "            var futures = IntStream.range(0, taskCount)\n"
                        "                .mapToObj(i -> executor.submit(() -> (long) i * 2L))\n"
                        "                .toList();\n"
                        "            long total = 0L;\n"
                        "            for (var f : futures) { total += f.get(); }\n"
                        "            return total;\n"
                        "        }\n"
                        "    }\n"
                        "}\n"
                        "```\n"
                        "Por la Ley de Little ($L = \\lambda \\cdot W$), un servidor ya no está limitado por el número de hilos de "
                        "plataforma ($\\approx 200$–$1000$), sino que puede sostener cientos de miles de peticiones bloqueadas en E/S "
                        "escribiendo código imperativo directo, fácil de depurar y con trazas de pila legibles."
                    ),
                },
                {
                    "subsection": "sec-v6-4-2",
                    "text": (
                        "Asimismo, Java 21/22 reemplaza a JNI y `sun.misc.Unsafe` con la **Foreign Function & Memory API (Project "
                        "Panama)**: `Arena.ofConfined()` y `MemorySegment` permiten gestionar memoria nativa fuera del montículo "
                        "(*off-heap*) con límites espaciales y temporales comprobados determinísticamente. En el Bloque G (Ecosistema), "
                        "estudiamos la gestión declarativa de proyectos con `Maven` (`pom.xml`) y `Gradle` (`build.gradle.kts`), "
                        "pruebas unitarias y de integración con `JUnit 5` y `Testcontainers`, microservicios con `Spring Boot 3` "
                        "(`spring.threads.virtual.enabled=true`) y compilación nativa con `GraalVM Native Image`."
                    ),
                },
            ],
            "definition": (
                "Hilo Virtual en la JVM (Virtual Thread, JEP 444): instancia de `java.lang.Thread` planificada en espacio de "
                "usuario por la máquina virtual sobre un conjunto reducido de hilos portadores del sistema operativo (*carrier "
                "threads*), cuya pila de marcos crece y se encoge dinámicamente en el montículo durante bloqueos de E/S."
            ),
            "consejo": (
                "No reutilices en un pool (`ThreadPool`) los hilos virtuales: los hilos virtuales son baratos y efímeros; "
                "crea uno nuevo por cada tarea con `Executors.newVirtualThreadPerTaskExecutor()` y usa un `Semaphore` cuando "
                "necesites limitar el número de llamadas simultáneas a una base de datos externa."
            ),
            "self_check": (
                "¿Qué es el *anclaje de hilo portador* (*carrier thread pinning*) cuando un hilo virtual se bloquea en E/S "
                "dentro de un bloque `synchronized` tradicional en Java 21 y por qué sustituirlo por `ReentrantLock` evita el anclaje?"
            ),
            "derivation": {
                "title": "Ley de Little aplicada a capacidad de concurrencia en servidores con Virtual Threads",
                "assumptions": ["En estado estacionario, la concurrencia media L es el producto de la tasa de llegadas lambda (req/s) por el tiempo medio de respuesta W (s)"],
                "steps": [
                    {"equation": r"L = \lambda \cdot W", "justification": "Teorema fundamental de colas de John Little"},
                    {"equation": r"\lambda_{\max} = \frac{L_{\max}}{W}", "justification": "Caudal máximo sostenible dado un límite de hilos concurrentes L_max"},
                ],
                "Verify": {"left": "(L_max / W) * W", "right": "L_max"},
            },
            "worked_problem": {
                "prompt": (
                    "Según la Ley de Little ($\\lambda_{\\max} = L_{\\max} / W$), un microservicio donde cada petición pasa "
                    "$W = 0.25\\text{ s}$ esperando respuestas de APIs externas está limitado con hilos tradicionales de plataforma "
                    "a $L_{\\text{plat}} = 400$ hilos (caudal máximo $400 / 0.25 = 1600\\text{ req/s}$). Al migrar a **Virtual Threads** "
                    "en Java 21 soportando $L_{\\text{virt}} = 20000$ hilos virtuales simultáneos con la misma latencia $W = 0.25\\text{ s}$, "
                    "calcula cuántas peticiones por segundo adicionales puede sostener el servidor ($20000 / 0.25 - 400 / 0.25$)."
                ),
                "expression": "(20000 / 0.25) - (400 / 0.25)",
                "solution": {
                    "model": "Incremento de caudal máximo por Ley de Little con Virtual Threads (JEP 444)",
                    "given": [
                        {"symbol": "L_plat", "value": "400 hilos", "description": "Pool clásico de hilos del sistema operativo"},
                        {"symbol": "L_virt", "value": "20000 hilos", "description": "Hilos virtuales simultáneos en Java 21"},
                        {"symbol": "W", "value": "0.25 s", "description": "Tiempo medio de espera de E/S por petición"},
                    ],
                    "steps": [
                        {"step": "Restamos el caudal antiguo (1600 req/s) al nuevo caudal (80000 req/s)", "equation": r"\Delta \lambda = \frac{20000}{0.25} - \frac{400}{0.25}", "expression": "(20000 / 0.25) - (400 / 0.25)"},
                    ],
                    "conclusion": "El servidor incrementa su capacidad en 78 400 peticiones/s (pasando de 1600 req/s a 80 000 req/s).",
                },
            },
            "practice_problems": [
                {"prompt": "Por la Ley de Little ($L = \\lambda \\cdot W$), si un sistema recibe $\\lambda = 2500$ peticiones/s y cada una tarda $W = 0.2$ segundos, ¿cuántas peticiones hay en vuelo simultáneamente en promedio?", "expression": "2500 * 0.2", "difficulty": "FOUNDATIONAL", "problem_type": "DIRECT_SUBSTITUTION"},
                {"prompt": "En una CPU de 16 núcleos lógicos, el `ForkJoinPool` portador de hilos virtuales crea por defecto un hilo portador (*carrier thread*) por núcleo. ¿Cuántos hilos del sistema operativo mantienen activos los hilos virtuales?", "expression": "16", "difficulty": "FOUNDATIONAL", "problem_type": "DIRECT_SUBSTITUTION"},
                {"prompt": "En el código `VirtualThreadDispatcher.runConcurrentTasks(100)`, se suma `i * 2` para $i = 0, 1, \\dots, 99$. ¿Cuál es el valor exacto de la suma ($99 \\times 100$)?", "expression": "99 * 100", "difficulty": "INTERMEDIATE", "problem_type": "MULTI_STEP"},
                {"prompt": "Una `Arena.ofConfined()` de Project Panama reserva 64 segmentos nativos de 4096 bytes cada uno. ¿Cuántos bytes de memoria *off-heap* se liberan determinísticamente al cerrarse el bloque `try-with-resources`?", "expression": "64 * 4096", "difficulty": "INTERMEDIATE", "problem_type": "DESIGN"},
            ],
        },
        {
            "id": "cap05-go-fundamentos-slices-interfaces-errores-genericos",
            "title": "Monografía de Go (I — Bloques A–D): Filosofía, Compilación Estática, Slices, Maps, Interfaces Implícitas y Manejo de Errores",
            "part_id": "parte-v-go-kotlin-swift",
            "part_title": "Monografías de Sistemas Cloud y Móviles: Go, Kotlin y Swift",
            "sources": ["src-go-spec", "src-kleppmann-ddia"],
            "learning_objectives": [
                "Comprender la filosofía de simplicidad ortogonal de Go (Rob Pike, Ken Thompson, Robert Griesemer), su compilador ultrarrápido y el enlazado de binarios estáticos.",
                "Dominar la anatomía en memoria de `slice` (puntero, longitud, capacidad) y `map`, el valor cero útil (*zero value*), composición de `struct` por incrustación (*embedding*) y `defer`.",
                "Diseñar abstracciones desacopladas mediante interfaces satisfechas implícitamente, manejo explícito de errores como valores (`errors.Is`, `errors.As`, `%w`) y genéricos de Go 1.18+.",
            ],
            "concepts": [
                {"id": "cpt-go-slices-structs-defer", "title": "Representación de tres palabras de un slice, valores cero útiles, composición por embedding y semántica de defer"},
                {"id": "cpt-go-interfaces-errors-generics", "title": "Satisfacción estructural implícita de interfaces (iface/eface), envoltura de errores y parámetros de tipo"},
            ],
            "subsections": [
                {"id": "sec-v6-5-1", "title": "Bloques A–C: Filosofía de Go, toolchain integrada (`go`), tipos, valores cero, arrays vs slices y maps"},
                {"id": "sec-v6-5-2", "title": "Bloque D: Métodos, composición de structs, interfaces implícitas, errores como valores y genéricos"},
            ],
            "purpose": (
                "Este capítulo inicia la monografía autónoma de **Go (Golang 1.22+)** (Bloques A, B, C y D). Go es el lenguaje "
                "fundacional de la infraestructura nativa en la nube (Docker, Kubernetes, etcd, Prometheus, Terraform, Caddy). "
                "Estudiaremos por qué su deliberada economía de conceptos produce sistemas distribuidos mantenibles por grandes equipos."
            ),
            "paragraphs": [
                {
                    "subsection": "sec-v6-5-1",
                    "text": (
                        "Diseñado en Google en 2007 por Robert Griesemer, Rob Pike y Ken Thompson, Go nació como respuesta a los "
                        "tiempos de compilación masivos y la complejidad accidental de C++ y Java en servidores multinúcleo. La "
                        "herramienta unificada `go` integra compilación, gestión de módulos (`go.mod` / `go.sum` con selección de "
                        "versión mínima, *Minimal Version Selection*), formateo canónico (`gofmt`), análisis estático (`go vet`), "
                        "pruebas y *fuzzing* nativo (`go test -fuzz`). En Go, toda variable no inicializada explícitamente recibe su "
                        "**valor cero** determinista (`0`, `false`, `\"\"`, `nil`), y los principios de diseño recomiendan que el "
                        "valor cero de una estructura sea inmediatamente utilizable sin constructor (como `var mu sync.Mutex` o "
                        "`var buf bytes.Buffer`). Un `slice` `[]T` es un descriptor de 24 bytes (en 64 bits) formado por un puntero "
                        "al array subyacente, la longitud `len` y la capacidad `cap`. Si dos rebanadas comparten el mismo array "
                        "subyacente y una ejecuta `append` sin superar `cap`, modifica el array compartido; para independizar la "
                        "capacidad al hacer sub-slicing se utiliza la expresión de tres índices `s[low:high:max]`."
                    ),
                },
                {
                    "subsection": "sec-v6-5-2",
                    "text": (
                        "Go prescinde por completo de la herencia de clases y la sustituye por **composición de estructuras** y "
                        "**interfaces satisfechas implícitamente**: un tipo satisface una interfaz como `io.Reader` (`Read(p []byte) (n int, err error)`) "
                        "simplemente implementando sus métodos, sin escribir nunca `implements`. Esto permite definir interfaces "
                        "pequeñas de uno o dos métodos en el paquete consumidor en lugar de acoplarse al paquete proveedor. Asimismo, "
                        "Go trata los errores como valores ordinarios devueltos en la última posición de retorno `(val, error)`, "
                        "encadenados con `fmt.Errorf(\"contexto: %w\", err)` e inspeccionados mediante `errors.Is` y `errors.As`:\n"
                        "```go\n"
                        "package storage\n\n"
                        "import (\n"
                        "    \"errors\"\n"
                        "    \"fmt\"\n"
                        "    \"io\"\n"
                        ")\n\n"
                        "var ErrEmptyPayload = errors.New(\"empty payload\")\n\n"
                        "func ReadExactHeader(r io.Reader, size int) ([]byte, error) {\n"
                        "    if size <= 0 {\n"
                        "        return nil, ErrEmptyPayload\n"
                        "    }\n"
                        "    buf := make([]byte, size)\n"
                        "    if _, err := io.ReadFull(r, buf); err != nil {\n"
                        "        return nil, fmt.Errorf(\"read exact header (%d bytes): %w\", size, err)\n"
                        "    }\n"
                        "    return buf, nil\n"
                        "}\n"
                        "```\n"
                        "Un matiz técnico esencial de las interfaces en Go es su representación interna de dos palabras (`tab` / tipo "
                        "dinámico y `data` / valor dinámico): una interfaz solo es `== nil` si **ambos** punteros internos son nulos; "
                        "asignar un puntero tipado `(*MyError)(nil)` a una variable `var err error` produce una interfaz **no nula** "
                        "(`err != nil`), por lo que las funciones deben devolver siempre el literal `nil` directamente cuando no hay error."
                    ),
                },
            ],
            "definition": (
                "Expresión de rebanada completa (`s[i:j:k]` en Go): operación de sub-slicing que produce una nueva rebanada "
                "con longitud `j - i` y capacidad restringida a `k - i`, forzando que cualquier `append` posterior sobre la "
                "sub-rebanada aloje un nuevo array en lugar de sobrescribir los elementos a partir del índice `k`."
            ),
            "consejo": (
                "Sigue el axioma idiomático de Go: *«Acepta interfaces (pequeñas, como `io.Reader`), devuelve estructuras concretas»*, "
                "y evalúa siempre los argumentos de `defer` teniendo en cuenta que se capturan en el momento en que se ejecuta "
                "la sentencia `defer`, no cuando retorna la función."
            ),
            "self_check": (
                "¿Por qué una función en Go que declara `var p *MyCustomError = nil; return p` como valor de retorno de tipo "
                "`error` hace que el llamador observe `err != nil`?"
            ),
            "derivation": {
                "title": "Longitud y capacidad de una expresión de sub-rebanada de tres índices s[i:j:k] en Go",
                "assumptions": ["Para una rebanada s con 0 <= i <= j <= k <= cap(s)"],
                "steps": [
                    {"equation": r"\text{len}(s[i:j:k]) = j - i", "justification": "Número de elementos visibles en la nueva vista"},
                    {"equation": r"\text{cap}(s[i:j:k]) = k - i", "justification": "Techo máximo del array subyacente accesible desde la nueva vista"},
                ],
                "Verify": {"left": "(k - i) - (j - i)", "right": "k - j"},
            },
            "worked_problem": {
                "prompt": (
                    "En un programa en Go, se crea un slice `base := make([]int64, 100, 200)` (cada `int64` ocupa $8\\text{ B}$) "
                    "y se obtiene la sub-rebanada de tres índices `sub := base[20:60:80]`. Calcula la suma de la longitud `len(sub)` "
                    "($60 - 20$) más la capacidad `cap(sub)` ($80 - 20$) multiplicada por los $8\\text{ B}$ de cada elemento."
                ),
                "expression": "((60 - 20) + (80 - 20)) * 8",
                "solution": {
                    "model": "Cálculo de len y cap en expresiones de rebanada de tres índices s[i:j:k] en Go",
                    "given": [
                        {"symbol": "i", "value": "20", "description": "Índice inicial"},
                        {"symbol": "j", "value": "60", "description": "Índice final de longitud"},
                        {"symbol": "k", "value": "80", "description": "Índice límite de capacidad"},
                    ],
                    "steps": [
                        {"step": "Sumamos len (40) + cap (60) = 100 y multiplicamos por 8 bytes", "equation": r"R = ((60 - 20) + (80 - 20)) \cdot 8", "expression": "((60 - 20) + (80 - 20)) * 8"},
                    ],
                    "conclusion": "La longitud de sub es 40, su capacidad es 60 y la métrica ponderada por 8 bytes es 800.",
                },
            },
            "practice_problems": [
                {"prompt": "En Go de 64 bits, el encabezado de un slice (`SliceHeader`) consta de `Data` (8 B), `Len` (8 B) y `Cap` (8 B). ¿Cuántos bytes ocupa en la pila?", "expression": "8 + 8 + 8", "difficulty": "FOUNDATIONAL", "problem_type": "DIRECT_SUBSTITUTION"},
                {"prompt": "En Go, cada cubo (*bucket* `bmap`) de un `map[K]V` almacena exactamente 8 pares clave-valor. Si un mapa tiene $2^6 = 64$ cubos, ¿cuántos pares clave-valor caben en esos 64 cubos sin cubos de desbordamiento ($64 \\times 8$)?", "expression": "64 * 8", "difficulty": "FOUNDATIONAL", "problem_type": "DIRECT_SUBSTITUTION"},
                {"prompt": "Para la rebanada `s[15:45:50]`, ¿cuántos elementos pueden añadirse con `append` antes de superar la capacidad y forzar la reserva de un nuevo array ($(50 - 15) - (45 - 15)$)?", "expression": "(50 - 15) - (45 - 15)", "difficulty": "INTERMEDIATE", "problem_type": "MULTI_STEP"},
                {"prompt": "Una interfaz `io.Reader` en Go se representa como un par de palabras `(itab*, data*)` de 8 bytes cada una. ¿Cuántos bytes ocupan 500 descriptores de interfaz en un slice `[]io.Reader`?", "expression": "500 * 16", "difficulty": "INTERMEDIATE", "problem_type": "DESIGN"},
            ],
        },
        {
            "id": "cap06-go-avanzado-experto-goroutines-gmp-canales-context-proyectos",
            "title": "Monografía de Go (II — Bloques E–H): Planificador G-M-P, Goroutines, Canales, Context, Perfilado pprof y Proyectos",
            "part_id": "parte-v-go-kotlin-swift",
            "part_title": "Monografías de Sistemas Cloud y Móviles: Go, Kotlin y Swift",
            "sources": ["src-go-spec", "src-kleppmann-ddia"],
            "learning_objectives": [
                "Explicar el funcionamiento interno del planificador M:N con robo de trabajo (*work-stealing*) de Go basado en las entidades G (Goroutine), M (Machine) y P (Processor).",
                "Diseñar patrones concurrentes basados en CSP (Tony Hoare) con canales con y sin búfer, `select`, cancelación jerárquica con `context.Context` y `errgroup.Group`.",
                "Auditar el escape al montículo (`go build -gcflags='-m'`), detectar carreras de datos (`go test -race`), perfilar CPU/memoria con `pprof` y construir los 4 proyectos en Go.",
            ],
            "concepts": [
                {"id": "cpt-go-gmp-scheduler-channels", "title": "Planificador G-M-P con robo de trabajo, pilas iniciales de 2 KiB, canales CSP y multiplexación con select"},
                {"id": "cpt-go-context-pprof-escape", "title": "Cancelación con context.Context, análisis de escape del compilador, detector de carreras y pprof"},
            ],
            "subsections": [
                {"id": "sec-v6-6-1", "title": "Bloques E y F: Planificador G-M-P, goroutines, canales, select, context.Context, sync/errgroup y análisis de escape"},
                {"id": "sec-v6-6-2", "title": "Bloques G y H: Ecosistema (net/http, grpc-go, sqlc, pprof, -race) y los 4 proyectos en Go"},
            ],
            "figure": {
                "key": "fig-go-gmp-scheduler",
                "caption": "Arquitectura del planificador M:N de Go: cada contexto lógico P (GOMAXPROCS) posee una cola local sin cerrojos de Goroutines (G) y se vincula a un hilo del sistema operativo (M) para ejecutar código Go o robar la mitad de la cola de otro P.",
                "tikz": r"""\begin{tikzpicture}[node distance=1.6cm, >=stealth, thick, font=\small]
\node[draw=blue!70!black, fill=blue!8, rounded corners, minimum width=2.8cm, minimum height=0.9cm, align=center] (m1) {Hilo OS $M_1$};
\node[draw=teal!70!black, fill=teal!10, rounded corners, minimum width=2.8cm, minimum height=0.9cm, align=center, below=0.7cm of m1] (p1) {Procesador $P_1$};
\node[draw=orange!75!black, fill=orange!12, rounded corners, minimum width=3.4cm, minimum height=0.9cm, align=center, below=0.7cm of p1] (q1) {Cola Local: $G_1, G_2, G_3$};
\node[draw=blue!70!black, fill=blue!8, rounded corners, minimum width=2.8cm, minimum height=0.9cm, align=center, right=2.2cm of m1] (m2) {Hilo OS $M_2$};
\node[draw=teal!70!black, fill=teal!10, rounded corners, minimum width=2.8cm, minimum height=0.9cm, align=center, below=0.7cm of m2] (p2) {Procesador $P_2$};
\node[draw=orange!75!black, fill=orange!12, rounded corners, minimum width=3.4cm, minimum height=0.9cm, align=center, below=0.7cm of p2] (q2) {Cola Local Vacía};
\draw[->] (m1) -- (p1);
\draw[->] (p1) -- (q1);
\draw[->] (m2) -- (p2);
\draw[->] (p2) -- (q2);
\draw[->, dashed, red!75!black] (q1.east) -- node[above, font=\footnotesize] {Work-Stealing ($50\%$)} (q2.west);
\end{tikzpicture}""",
            },
            "purpose": (
                "Este capítulo completa la monografía de Go (Bloques E, F, G y H). Analizamos el motor de ejecución de Go: "
                "su planificador de **goroutines G-M-P**, los patrones de canales y `context.Context` para evitar fugas de "
                "goroutines, el recolector de basura tricolor concurrente de baja latencia y las herramientas integradas de "
                "diagnóstico de producción (`pprof`, `trace`, `-race`)."
            ),
            "paragraphs": [
                {
                    "subsection": "sec-v6-6-1",
                    "text": (
                        "Una **goroutine** (`go fn()`) es un hilo de ejecución ligero gestionado por el runtime de Go cuya pila "
                        "inicial mide tan solo **$2\\text{ KiB}$** ($2048\\text{ B}$) y crece o decrece dinámicamente según la "
                        "profundidad de llamadas. Como muestra la Figura \\ref{fig:fig-go-gmp-scheduler}, el planificador M:N "
                        "multiplexa $N$ goroutines (`G`) sobre $M$ hilos del sistema operativo (`M`) utilizando hasta `GOMAXPROCS` "
                        "procesadores lógicos (`P`). Cada `P` mantiene una cola local de hasta 256 goroutines ejecutables; cuando "
                        "la cola de un `P` se vacía, intenta robar la mitad de las goroutines de la cola de otro `P` elegido al azar "
                        "(*work-stealing*) o toma trabajo de la cola global. La comunicación entre goroutines sigue el cálculo "
                        "**CSP** (*Communicating Sequential Processes*): *«No compartas memoria para comunicarte; comunícate para "
                        "compartir memoria»*. Para evitar que una goroutine quede bloqueada eternamente intentando enviar en un canal "
                        "cuyo receptor ya ha abandonado la operación (*goroutine leak*), todo ciclo concurrente debe seleccionar "
                        "también sobre `<-ctx.Done()` de un `context.Context`:\n"
                        "```go\n"
                        "package worker\n\n"
                        "import \"context\"\n\n"
                        "func FanOutGenerator(ctx context.Context, items []int, out chan<- int) error {\n"
                        "    for _, v := range items {\n"
                        "        select {\n"
                        "        case <-ctx.Done():\n"
                        "            return ctx.Err()\n"
                        "        case out <- v * 2:\n"
                        "        }\n"
                        "    }\n"
                        "    return nil\n"
                        "}\n"
                        "```\n"
                        "A partir de Go 1.22, las variables de bucle `for i, v := range items` tienen ámbito por iteración en lugar "
                        "de por bucle completo, eliminando el error histórico de capturar la misma variable `v` en múltiples clausuras concurrentes."
                    ),
                },
                {
                    "subsection": "sec-v6-6-2",
                    "text": (
                        "En el Nivel Experto (Bloque F), el compilador de Go decide automáticamente si una variable local se aloja "
                        "en la pila de $2\\text{ KiB}$ de la goroutine o en el montículo gestionado mediante **análisis de escape** "
                        "(*escape analysis*), inspeccionable con `go build -gcflags=\"-m\"`. En el Bloque G y Bloque H, la biblioteca "
                        "estándar de Go es tan completa que permite construir servidores HTTP/2 de producción con enrutamiento por "
                        "patrones (`net/http` en Go 1.22+), observabilidad (`log/slog`, `runtime/pprof`), clientes SQL con pools de "
                        "conexiones (`database/sql`) y pruebas de concurrencia instrumentadas con ThreadSanitizer (`go test -race`). "
                        "Los cuatro proyectos del bloque incluyen un proxy inverso con balanceo *round-robin* y *health checks*, "
                        "un grupo de trabajadores (*worker pool*) con apagado ordenado (`os/signal` + `context.WithTimeout`), un "
                        "limitador de tasa distribuido y un servidor gRPC."
                    ),
                },
            ],
            "definition": (
                "Fuga de Goroutines (Goroutine Leak): defecto de recursos en Go en el que una goroutine queda suspendida "
                "permanentemente en una operación de envío o recepción de canal que ningún otro participante completará jamás, "
                "impidiendo que el recolector de basura libere su pila y las variables referenciadas por ella."
            ),
            "consejo": (
                "Antes de lanzar cualquier `go func() { ... }()`, responde siempre a dos preguntas: (1) ¿bajo qué condición exacta "
                "terminará esta goroutine (por ejemplo, cancelación de `ctx.Done()` o cierre del canal de entrada)? y (2) ¿quién "
                "esperará a que termine (`sync.WaitGroup` o `errgroup.Group`) antes de cerrar el proceso?"
            ),
            "self_check": (
                "¿Qué ocurre exactamente en tiempo de ejecución en Go cuando una goroutine intenta enviar un valor a un canal "
                "cerrado (`close(ch)`) frente a cuando intenta recibir de un canal cerrado?"
            ),
            "derivation": {
                "title": "Robo de trabajo (Work-Stealing) de la mitad de la cola local en el planificador de Go",
                "assumptions": ["Cuando un procesador P_i se queda con 0 goroutines, roba floor(Q_j / 2) goroutines de la cola local de otro procesador P_j"],
                "steps": [
                    {"equation": r"G_{\text{stolen}} = Q_j / 2", "justification": "División equitativa de la cola local víctima para minimizar transferencias futuras"},
                    {"equation": r"G_{\text{rem}} = Q_j - G_{\text{stolen}}", "justification": "Goroutines que permanecen en el procesador víctima P_j"},
                ],
                "Verify": {"left": "Q_j - Q_j / 2", "right": "Q_j / 2"},
            },
            "worked_problem": {
                "prompt": (
                    "Cada goroutine recién creada en Go 1.22 reserva una pila inicial de $S_G = 2\\text{ KiB}$ ($2048\\text{ B}$), "
                    "mientras que un hilo nativo de sistema operativo reserva por defecto una pila de $S_M = 2048\\text{ KiB}$ "
                    "($2\\text{ MiB}$). Si un servidor de telemetría en Go mantiene $N = 100000$ goroutines activas sobre "
                    "$M = 16$ hilos del sistema operativo, calcula cuántos mebibytes totales (dividiendo los KiB entre 1024) "
                    "ocupan las pilas de las 100 000 goroutines más los 16 hilos OS."
                ),
                "expression": "(100000 * 2 + 16 * 2048) / 1024",
                "solution": {
                    "model": "Consumo de memoria de pilas en el modelo M:N de Go",
                    "given": [
                        {"symbol": "N", "value": "100000", "description": "Número de goroutines concurrentes"},
                        {"symbol": "S_G", "value": "2 KiB", "description": "Pila inicial por goroutine"},
                        {"symbol": "M", "value": "16", "description": "Hilos del sistema operativo de 2048 KiB"},
                    ],
                    "steps": [
                        {"step": "Sumamos los KiB de las goroutines (200000 KiB) y de los 16 hilos OS (32768 KiB) y dividimos entre 1024", "equation": r"M_{\text{MiB}} = \frac{100000 \cdot 2 + 16 \cdot 2048}{1024}", "expression": "(100000 * 2 + 16 * 2048) / 1024"},
                    ],
                    "conclusion": "Las 100 000 goroutines más los 16 hilos del sistema operativo consumen tan solo 227.3125 MiB de memoria de pila.",
                },
            },
            "practice_problems": [
                {"prompt": "¿Cuántos bytes mide la pila inicial de una goroutine en Go ($2 \\times 1024$)?", "expression": "2 * 1024", "difficulty": "FOUNDATIONAL", "problem_type": "DIRECT_SUBSTITUTION"},
                {"prompt": "En el planificador de Go, un procesador $P_1$ tiene 180 goroutines en su cola local y un procesador inactivo $P_2$ le roba la mitad. ¿Cuántas goroutines roba $P_2$?", "expression": "180 / 2", "difficulty": "FOUNDATIONAL", "problem_type": "DIRECT_SUBSTITUTION"},
                {"prompt": "Un canal con búfer `ch := make(chan uint64, 512)` almacena elementos de 8 bytes. Si hay 300 elementos encolados en el búfer, ¿cuántos elementos adicionales caben antes de bloquear al emisor?", "expression": "512 - 300", "difficulty": "INTERMEDIATE", "problem_type": "MULTI_STEP"},
                {"prompt": "En el problema anterior, ¿cuántos bytes ocupa el búfer circular completo de 512 elementos `uint64` ($512 \\times 8$)?", "expression": "512 * 8", "difficulty": "INTERMEDIATE", "problem_type": "DESIGN"},
            ],
        },
        {
            "id": "cap07-monografia-kotlin-null-safety-coroutines-flow-kmp",
            "title": "Monografía de Kotlin (Bloques A–H): Null-Safety, Data/Sealed Classes, Extensiones, Coroutines, Flow y Multiplatform",
            "part_id": "parte-v-go-kotlin-swift",
            "part_title": "Monografías de Sistemas Cloud y Móviles: Go, Kotlin y Swift",
            "sources": ["src-kotlin-spec", "src-java-jls21"],
            "learning_objectives": [
                "Dominar el sistema de tipos de Kotlin 2.0 (compilador K2): distinción estricta `T` vs `T?`, smart casts, `data class`, `sealed interface`, `value class` y delegación (`by`).",
                "Escribir código expresivo con funciones de orden superior `inline`, tipos genéricos reificados (`reified T`), funciones de extensión y DSLs con receptores (`T.() -> Unit`).",
                "Construir sistemas concurrentes y reactivos con **Kotlin Coroutines**: funciones `suspend`, transformaciones CPS, `CoroutineScope`, `Dispatchers`, `Structured Concurrency` y `Flow` / `StateFlow`.",
            ],
            "concepts": [
                {"id": "cpt-kt-types-inline-dsl", "title": "Seguridad frente a nulos (T vs T?), clases selladas, funciones inline con reified T y receptores de lambda"},
                {"id": "cpt-kt-coroutines-cps-flow", "title": "Transformación Continuation-Passing Style (CPS) de funciones suspend, concurrencia estructurada y flujos fríos/calientes"},
            ],
            "subsections": [
                {"id": "sec-v6-7-1", "title": "Bloques A–D: Filosofía de Kotlin, interoperabilidad JVM/KMP, null-safety, data/sealed classes y extensiones"},
                {"id": "sec-v6-7-2", "title": "Bloques E–H: Funciones inline/reified, DSLs, Coroutines (suspend, CPS, Flow), ecosistema (Ktor, Compose) y proyectos"},
            ],
            "purpose": (
                "Este capítulo ofrece la monografía completa (Bloques A–H) de **Kotlin (2.0+)**. Desarrollado por JetBrains, "
                "Kotlin es el lenguaje oficial prioritario para el desarrollo en Android, una potencia en microservicios de "
                "servidor sobre la JVM (Spring Boot, Ktor) y un lenguaje multiplataforma nativo (**Kotlin Multiplatform**, KMP)."
            ),
            "paragraphs": [
                {
                    "subsection": "sec-v6-7-1",
                    "text": (
                        "Kotlin resuelve las limitaciones históricas de Java manteniendo una interoperabilidad del 100 % a nivel de "
                        "bytecode. Su sistema de tipos incorpora nulabilidad en la raíz de la jerarquía: `String` no puede almacenar "
                        "`null`, mientras que `String?` exige comprobación explícita mediante el operador de llamada segura `?.`, el "
                        "operador Elvis `?:` o *smart casts* tras verificar `if (x != null)`. Para modelar dominios sin sobrecoste de "
                        "ejecución, `@JvmInline value class UserId(val raw: Long)` envuelve un tipo primitivo en compilación pero se "
                        "emite como un `long` desnudo en el bytecode de la JVM. Asimismo, dado que en Kotlin las funciones de orden "
                        "superior se usan intensivamente, la palabra clave `inline` inserta el cuerpo de la función y el de las lambdas "
                        "recibidas directamente en el sitio de llamada, eliminando la creación de objetos clausura y permitiendo "
                        "preservar el tipo genérico en ejecución con `reified T`."
                    ),
                },
                {
                    "subsection": "sec-v6-7-2",
                    "text": (
                        "La concurrencia en Kotlin se fundamenta en **Coroutines** estructuradas a partir de una única palabra clave "
                        "en el lenguaje: `suspend`. El compilador K2 transforma cada `suspend fun fetch(id: Long): Profile` mediante "
                        "**Continuation-Passing Style (CPS)** en una función que recibe un parámetro adicional oculto `Continuation<Profile>` "
                        "implementado como una máquina de estados sin alojar un hilo por espera:\n"
                        "```kotlin\n"
                        "import kotlinx.coroutines.*\n\n"
                        "data class NodeHealth(val nodeId: Int, val latencyMs: Long)\n\n"
                        "suspend fun aggregateClusterLatency(nodeIds: List<Int>): Long = coroutineScope {\n"
                        "    val deferreds: List<Deferred<Long>> = nodeIds.map { id ->\n"
                        "        async(Dispatchers.Default) {\n"
                        "            // Simulación de consulta paralela por nodo:\n"
                        "            id.toLong() * 5L\n"
                        "        }\n"
                        "    }\n"
                        "    deferreds.awaitAll().sum()\n"
                        "}\n"
                        "```\n"
                        "Dentro de `coroutineScope { ... }`, la concurrencia es estrictamente jerárquica: la función no retorna hasta "
                        "que todas las corrutinas hijas lanzadas con `launch` o `async` han terminado, y si una sola falla con una "
                        "excepción, todas las demás hermanas reciben cancelación cooperativa inmediata. Para secuencias asíncronas de "
                        "múltiples valores, Kotlin distingue entre `Flow<T>` (flujo frío perezoso con contrapresión natural por suspensión) "
                        "y `StateFlow<T>` / `SharedFlow<T>` (flujos calientes observables en arquitecturas reactivas como Jetpack Compose)."
                    ),
                },
            ],
            "definition": (
                "Transformación CPS de funciones `suspend` en Kotlin: reescritura realizada por el compilador en la que toda "
                "función `suspend fun f(a: A): R` se compila en bytecode a `Object f(A a, Continuation<? super R> completion)`, "
                "donde `completion` almacena el índice `label` del estado actual y las variables locales vivas entre puntos de suspensión."
            ),
            "consejo": (
                "Cuando captures excepciones genéricas (`catch (e: Throwable)` o `catch (e: Exception)`) dentro de una corrutina "
                "de Kotlin, **relanza siempre `CancellationException`** (`if (e is CancellationException) throw e`): tragarse "
                "`CancellationException` rompe el mecanismo de cancelación cooperativa de la concurrencia estructurada."
            ),
            "self_check": (
                "¿Qué diferencia de comportamiento ante el fallo de una corrutina hija existe entre `coroutineScope { ... }` "
                "y `supervisorScope { ... }` en Kotlin Coroutines?"
            ),
            "derivation": {
                "title": "Eliminación de asignaciones de objetos clausura mediante funciones inline en Kotlin",
                "assumptions": ["En un bucle de N iteraciones, una lambda no inline que captura variables locales aloja 1 objeto Function en el montículo por iteración; con inline aloja 0 objetos"],
                "steps": [
                    {"equation": r"A_{\text{no\_inline}}(N) = N \cdot S_{\text{lambda}}", "justification": "Una lambda que captura variables del entorno instancia un objeto clausura por llamada"},
                    {"equation": r"A_{\text{inline}}(N) = 0", "justification": "El compilador expande el cuerpo de la lambda directamente en el bytecode del llamador"},
                ],
                "Verify": {"left": "N * S_lambda - 0", "right": "N * S_lambda"},
            },
            "worked_problem": {
                "prompt": (
                    "En una aplicación en Kotlin sobre la JVM, una función de orden superior que captura una variable local del "
                    "entorno se invoca en un bucle caliente $N = 500000$ veces por segundo. Si la función NO está marcada como "
                    "`inline`, cada invocación aloja una instancia de clase anónima de $S_{\\text{lambda}} = 24\\text{ B}$. "
                    "Al marcar la función de orden superior con `inline`, el alojamiento cae a $0\\text{ B}$. Calcula cuántos "
                    "megabytes por segundo (dividiendo entre $10^6$) deja de alojar el bucle gracias a `inline`."
                ),
                "expression": "(500000 * 24) / 1000000",
                "solution": {
                    "model": "Ahorro de montículo mediante expansión inline de lambdas con captura en Kotlin",
                    "given": [
                        {"symbol": "N", "value": "500000", "description": "Invocaciones por segundo"},
                        {"symbol": "S_lambda", "value": "24 B", "description": "Tamaño del objeto clausura capturado"},
                    ],
                    "steps": [
                        {"step": "Multiplicamos las 500000 invocaciones por 24 B y dividimos entre 10^6", "equation": r"\Delta M_{\text{MB/s}} = \frac{500000 \cdot 24}{10^6}", "expression": "(500000 * 24) / 1000000"},
                    ],
                    "conclusion": "La palabra clave inline ahorra exactamente 12 MB/s de asignaciones efímeras en el montículo.",
                },
            },
            "practice_problems": [
                {"prompt": "En la función `aggregateClusterLatency` con `nodeIds = [1, 2, 3, 4, 5]` donde cada nodo devuelve `id * 5`, ¿cuál es la suma total devuelta ($(1 + 2 + 3 + 4 + 5) \\times 5$)?", "expression": "(1 + 2 + 3 + 4 + 5) * 5", "difficulty": "FOUNDATIONAL", "problem_type": "DIRECT_SUBSTITUTION"},
                {"prompt": "Un `@JvmInline value class Meter(val v: Double)` se almacena en un array primitivo de 1000 elementos. ¿Cuántos bytes ocupan los 1000 elementos `double` ($1000 \\times 8$)?", "expression": "1000 * 8", "difficulty": "FOUNDATIONAL", "problem_type": "DIRECT_SUBSTITUTION"},
                {"prompt": "Un `Flow<Int>` emite 60 elementos a razón de 1 elemento cada 10 ms y el colector aplica `.buffer(10)` tardando 25 ms por elemento. ¿Cuántos milisegundos tarda el colector en procesar los 60 elementos ($10 + 60 \\times 25$)?", "expression": "10 + 60 * 25", "difficulty": "INTERMEDIATE", "problem_type": "MULTI_STEP"},
                {"prompt": "Un proyecto Kotlin Multiplatform comparte 14 000 líneas de lógica de dominio en `commonMain` entre Android e iOS, requiriendo solo 1500 líneas específicas en `androidMain` y 1500 en `iosMain`. ¿Cuántas líneas de código duplicado se ahorran respecto a escribir los 14 000 líneas dos veces?", "expression": "14000", "difficulty": "INTERMEDIATE", "problem_type": "DESIGN"},
            ],
        },
        {
            "id": "cap08-monografia-swift-valor-cow-protocolos-arc-actores",
            "title": "Monografía de Swift 6 (Bloques A–H): Semántica de Valor, Copy-on-Write, Protocolos, ARC y Concurrencia con Actores",
            "part_id": "parte-v-go-kotlin-swift",
            "part_title": "Monografías de Sistemas Cloud y Móviles: Go, Kotlin y Swift",
            "sources": ["src-swift-book", "src-pierce-tapl"],
            "learning_objectives": [
                "Comprender la arquitectura del compilador `swiftc` (SIL: Swift Intermediate Language y LLVM), la semántica de valor (`struct`, `enum`) y la optimización Copy-on-Write (CoW).",
                "Diseñar abstracciones con Programación Orientada a Protocolos (`protocol`, tipos asociados, tipos opacos `some P` vs existenciales `any P`).",
                "Dominar la gestión determinista de memoria mediante **ARC** (`strong`, `weak`, `unowned`) y el aislamiento estricto de carreras de datos de **Swift 6** (`async`/`await`, `actor`, `@MainActor`, `Sendable`).",
            ],
            "concepts": [
                {"id": "cpt-swift-value-cow-protocols", "title": "Semántica de valor con Copy-on-Write (isKnownUniquelyReferenced), SIL y tipos opacos some vs existenciales any"},
                {"id": "cpt-swift-arc-actors-sendable", "title": "Conteo automático de referencias (ARC), resolución de ciclos con weak/unowned y aislamiento de actores en Swift 6"},
            ],
            "subsections": [
                {"id": "sec-v6-8-1", "title": "Bloques A–D: Filosofía de Swift, SIL/LLVM, SwiftPM, semántica de valor (struct/enum), Copy-on-Write y protocolos"},
                {"id": "sec-v6-8-2", "title": "Bloques E–H: Gestión de memoria ARC (weak/unowned), concurrencia estricta en Swift 6 (actor, Sendable) y proyectos"},
            ],
            "purpose": (
                "Este capítulo cierra el Volumen VI con la monografía completa (Bloques A–H) de **Swift (6.0+)**. Creado por "
                "Chris Lattner y el equipo de Apple sobre la infraestructura LLVM, Swift es un lenguaje compilado nativamente "
                "sin recolector de basura de trazado que combina semántica de valor profunda, conteo automático de referencias "
                "(**ARC**) y verificación estática de aislamiento de actores en tiempo de compilación."
            ),
            "paragraphs": [
                {
                    "subsection": "sec-v6-8-1",
                    "text": (
                        "A diferencia de Java o Objective-C, en Swift casi todos los tipos fundamentales de la biblioteca estándar "
                        "—incluyendo enteros, flotantes, `String`, `Array<T>`, `Dictionary<K, V>` y `Set<T>`— son **tipos por valor** "
                        "(`struct`), no clases (`class`). Para que pasar un `Array<Double>` de un millón de elementos por valor a "
                        "una función no implique copiar el búfer inmediatamente, las colecciones de Swift implementan **Copy-on-Write (CoW)**: "
                        "al asignar `var b = a`, ambas estructuras comparten el mismo búfer interno en el montículo; solo cuando se "
                        "ejecuta una mutación como `b.append(1.0)`, `Array` comprueba en $O(1)$ mediante `isKnownUniquelyReferenced` "
                        "si el contador de referencias del búfer es mayor que 1 y, únicamente en ese caso, duplica el búfer antes de "
                        "modificarlo. En el diseño con protocolos (`protocol`), Swift 5.7+/6.0 distingue explícitamente entre `some Protocol` "
                        "(tipo opaco conocido estáticamente en compilación, despachado sin coste) y `any Protocol` (contenedor "
                        "existencial dinámico de 5 palabras máquina: 3 palabras de búfer de valor en línea más metadatos de tipo y *witness table*)."
                    ),
                },
                {
                    "subsection": "sec-v6-8-2",
                    "text": (
                        "Para las clases (`class`) y clausuras, Swift gestiona la memoria de forma determinista en tiempo de compilación "
                        "mediante **ARC** (*Automatic Reference Counting*): el compilador inserta llamadas `swift_retain` y `swift_release` "
                        "en la representación intermedia SIL. Como el conteo de referencias no recolecta ciclos aislados, todo ciclo "
                        "entre instancias de clases o clausuras que capturan `self` debe romperse declarando una de las aristas como "
                        "`weak` (opcional `T?` que se pone automáticamente a `nil` al destruirse el objeto) o `unowned` (no opcional, "
                        "cuando ambas vidas útiles están ligadas). Finalmente, **Swift 6** garantiza en tiempo de compilación la "
                        "ausencia de carreras de datos mediante el protocolo marcador `Sendable` y el tipo de referencia **`actor`**, "
                        "que serializa el acceso a su estado mutable interno exigiendo `await` desde cualquier contexto externo:\n"
                        "```swift\n"
                        "public actor TelemetryVault {\n"
                        "    private var readings: [String: Double] = [:]\n"
                        "    public init() {}\n"
                        "    public func record(sensor: String, value: Double) {\n"
                        "        readings[sensor] = value\n"
                        "    }\n"
                        "    public func current(sensor: String) -> Double? {\n"
                        "        return readings[sensor]\n"
                        "    }\n"
                        "}\n"
                        "```\n"
                        "El capítulo concluye con el ecosistema Swift Package Manager (`Package.swift`), `SwiftTesting` (`@Test`, `#expect`), "
                        "`SwiftUI` / `Vapor` en servidor Linux y cuatro proyectos completos en Swift 6."
                    ),
                },
            ],
            "definition": (
                "Aislamiento de Actor (`actor` en Swift): tipo por referencia que protege su estado mutable encapsulado "
                "mediante un ejecutor serie exclusivo, exigiendo estáticamente en tiempo de compilación que cualquier acceso "
                "desde fuera del actor sea asíncrono (`await`) y que los valores transferidos a través de su frontera cumplan `Sendable`."
            ),
            "consejo": (
                "En firmas de funciones en Swift, prefiere siempre `func render(item: some Drawable)` sobre `func render(item: any Drawable)` "
                "salvo que necesites almacenar elementos heterogéneos en un mismo array `[any Drawable]`: `some` permite al "
                "compilador especializar la función y evitar el contenedor existencial."
            ),
            "self_check": (
                "¿Cómo ocurre la *reentrancia de actores* (*actor reentrancy*) en Swift cuando un método de un `actor` ejecuta "
                "un punto de suspensión `await` intermedio, y por qué deben revalidarse las invariantes del actor después del `await`?"
            ),
            "derivation": {
                "title": "Tamaño del contenedor existencial (Existential Container) any Protocol en Swift de 64 bits",
                "assumptions": ["Un contenedor existencial para un protocolo con K tablas de testigos (Protocol Witness Tables) consta de 3 palabras de Value Buffer + 1 palabra de Value Witness Table + K palabras de Protocol Witness Table"],
                "steps": [
                    {"equation": r"S_{\text{exist}}(K) = (3 + 1 + K) \cdot W", "justification": "3 palabras de búfer en línea (24 B), 1 puntero a metadatos/VWT (8 B) y K punteros a PWT (8*K B)"},
                    {"equation": r"S_{\text{exist}}(1) = 5 W = 40\text{ B}", "justification": "Para un único protocolo (K = 1) en arquitectura de 64 bits (W = 8 B)"},
                ],
                "Verify": {"left": "(3 + 1 + 1) * 8", "right": "40"},
            },
            "worked_problem": {
                "prompt": (
                    "En Swift sobre una arquitectura de 64 bits ($W = 8\\text{ B}$), un contenedor existencial `any P` para un "
                    "protocolo ocupa $5 \\times 8 = 40\\text{ B}$ (24 B de búfer de valor en línea, 8 B de *Value Witness Table* "
                    "y 8 B de *Protocol Witness Table*), mientras que un valor concreto `Int64` pasado mediante un genérico "
                    "especializado `some P` ocupa únicamente $8\\text{ B}$. Calcula cuántos bytes ahorra un array de $N = 10000$ "
                    "elementos al usar el tipo especializado `[Int64]` frente a un array existencial `[any P]`."
                ),
                "expression": "10000 * (40 - 8)",
                "solution": {
                    "model": "Sobrecoste espacial de contenedores existenciales (any P) frente a tipos concretos (some P) en Swift",
                    "given": [
                        {"symbol": "N", "value": "10000", "description": "Número de elementos en la colección"},
                        {"symbol": "S_any", "value": "40 B", "description": "Tamaño del contenedor existencial de 5 palabras"},
                        {"symbol": "S_some", "value": "8 B", "description": "Tamaño del tipo concreto especializado"},
                    ],
                    "steps": [
                        {"step": "Multiplicamos los 10000 elementos por los 32 B ahorrados por elemento", "equation": r"\Delta M = 10000 \cdot (40 - 8)", "expression": "10000 * (40 - 8)"},
                    ],
                    "conclusion": "La especialización estática ahorra 320 000 bytes (un 80 % de reducción) y elimina el despacho indirecto por tabla de testigos.",
                },
            },
            "practice_problems": [
                {"prompt": "En Swift de 64 bits ($W = 8\\text{ B}$), el `Value Buffer` interno de un contenedor existencial tiene 3 palabras. ¿Hasta cuántos bytes puede medir un `struct` para caber en línea dentro del contenedor existencial sin alojar en el montículo ($3 \\times 8$)?", "expression": "3 * 8", "difficulty": "FOUNDATIONAL", "problem_type": "DIRECT_SUBSTITUTION"},
                {"prompt": "Si se copia un `Array<Int>` de 50 000 enteros (`var b = a`) y solo se realizan lecturas sobre `a` y `b` sin mutar ninguno de los dos, ¿cuántos elementos se duplican en el montículo gracias a Copy-on-Write?", "expression": "0", "difficulty": "FOUNDATIONAL", "problem_type": "DIRECT_SUBSTITUTION"},
                {"prompt": "Un contenedor existencial para una composición de $K = 3$ protocolos (`any P1 & P2 & P3`) ocupa $(3 + 1 + 3) \\times 8$ bytes en 64 bits. ¿Cuántos bytes mide en total?", "expression": "(3 + 1 + 3) * 8", "difficulty": "INTERMEDIATE", "problem_type": "MULTI_STEP"},
                {"prompt": "En la cabecera de un objeto `class` en Swift de 64 bits, se almacenan el puntero `isa`/metadatos (8 B) y la palabra de contadores ARC (8 B). ¿Cuántos bytes suman las cabeceras de 2000 instancias?", "expression": "2000 * (8 + 8)", "difficulty": "INTERMEDIATE", "problem_type": "DESIGN"},
            ],
        },
    ],
}

VOL07_SPEC: dict[str, object] = {
    "slug": "vol07-monografias-sql-shell-funcional-especializados",
    "code": "ENC-VOL07",
    "title": "Volumen VII: Monografías de SQL, Shell, PHP, Ruby, Dart, Funcionales y Científicos",
    "subtitle": "Parte V (Bloques A–H): Consultas declarativas, automatización UNIX, ecosistemas web/móvil, programación funcional pura, BEAM y cálculo científico",
    "target_pages": 68,
    "terminology": [
        {"term": "expresión de tabla común (CTE)", "canonical": "CTE (Common Table Expression)", "forbidden": ["tabla fantasma suelta"]},
        {"term": "transparencia referencial", "canonical": "transparencia referencial", "forbidden": ["pureza parcial mutable"]},
        {"term": "despacho múltiple (Multiple Dispatch)", "canonical": "despacho múltiple (Multiple Dispatch)", "forbidden": ["sobrecarga simple de receptor"]},
    ],
    "notation": [
        {"symbol": r"\sigma_p(R), \pi_L(R), R \bowtie S", "meaning": "Operadores de selección, proyección y reunión natural del álgebra relacional", "unit": "relación"},
        {"symbol": r"w \text{ OVER } (P, O)", "meaning": "Marco de evaluación de una función de ventana en SQL estándar", "unit": "ventana"},
        {"symbol": r"m \gg= f : M\langle B \rangle", "meaning": "Operador bind (>>=) de una mónada en programación funcional", "unit": "tipo"},
    ],
    "chapters": [
        {
            "id": "cap01-monografia-sql-ddl-dml-cte-ventanas-optimizacion",
            "title": "Monografía de SQL (Bloques A–H): Álgebra Relacional, DDL/DML, Lógica Trivaluada, CTEs Recursivas, Funciones de Ventana y Optimización",
            "part_id": "parte-v-sql-shell-web",
            "part_title": "Monografías de Datos, Automatización de Sistemas y Desarrollo Web/Móvil",
            "sources": ["src-sql-2023", "src-codd-1970"],
            "learning_objectives": [
                "Comprender el fundamento relacional de SQL (E. F. Codd, 1970; estándar ISO/IEC 9075:2023) y el orden lógico exacto de evaluación de una consulta (`FROM -> WHERE -> GROUP BY -> HAVING -> WINDOW -> SELECT -> DISTINCT -> ORDER BY -> LIMIT`).",
                "Dominar la lógica trivaluada de `NULL` (`TRUE`, `FALSE`, `UNKNOWN`), todos los tipos de `JOIN` (incluso `LATERAL`), subconsultas correlacionadas, CTEs recursivas (`WITH RECURSIVE`) y funciones de ventana (`ROW_NUMBER`, `RANK`, `LAG`, `SUM() OVER (...)`).",
                "Interpretar planes de ejecución (`EXPLAIN ANALYZE`), diseñar índices compuestos sargables y verificar el libro mayor financiero `projects/sql-transactional-ledger`.",
            ],
            "concepts": [
                {"id": "cpt-sql-logical-eval-nulls", "title": "Orden lógico de fases de ejecución SQL, lógica trivaluada de NULL y álgebra de reuniones (JOINs)"},
                {"id": "cpt-sql-recursive-cte-windows", "title": "Consultas jerárquicas con WITH RECURSIVE, funciones de ventana analíticas y optimización de consultas"},
            ],
            "subsections": [
                {"id": "sec-v7-1-1", "title": "Bloques A–D: Modelo relacional, DDL con restricciones, orden lógico de SELECT, lógica trivaluada (NULL) y JOINs"},
                {"id": "sec-v7-1-2", "title": "Bloques E–H: CTEs recursivas, funciones de ventana (OVER), transacciones, EXPLAIN y projects/sql-transactional-ledger"},
            ],
            "figure": {
                "key": "fig-sql-logical-execution-order",
                "caption": "Orden lógico de evaluación de una consulta SQL frente al orden léxico de escritura: un alias definido en SELECT no existe aún cuando se evalúan WHERE, GROUP BY o HAVING.",
                "tikz": r"""\begin{tikzpicture}[node distance=1.4cm, >=stealth, thick, font=\small]
\node[draw=blue!70!black, fill=blue!8, rounded corners, minimum width=2.4cm, minimum height=0.8cm, align=center] (from) {1. \texttt{FROM / JOIN}};
\node[draw=blue!70!black, fill=blue!8, rounded corners, minimum width=2.1cm, minimum height=0.8cm, align=center, right=0.35cm of from] (where) {2. \texttt{WHERE}};
\node[draw=teal!70!black, fill=teal!10, rounded corners, minimum width=2.4cm, minimum height=0.8cm, align=center, right=0.35cm of where] (group) {3. \texttt{GROUP BY}};
\node[draw=teal!70!black, fill=teal!10, rounded corners, minimum width=2.1cm, minimum height=0.8cm, align=center, right=0.35cm of group] (having) {4. \texttt{HAVING}};
\node[draw=orange!75!black, fill=orange!12, rounded corners, minimum width=2.5cm, minimum height=0.8cm, align=center, below=0.7cm of from] (win) {5. \texttt{WINDOW}};
\node[draw=orange!75!black, fill=orange!12, rounded corners, minimum width=2.1cm, minimum height=0.8cm, align=center, right=0.35cm of win] (sel) {6. \texttt{SELECT}};
\node[draw=green!60!black, fill=green!10, rounded corners, minimum width=2.4cm, minimum height=0.8cm, align=center, right=0.35cm of sel] (ord) {7. \texttt{ORDER BY}};
\node[draw=green!60!black, fill=green!10, rounded corners, minimum width=2.1cm, minimum height=0.8cm, align=center, right=0.35cm of ord] (lim) {8. \texttt{LIMIT}};
\draw[->] (from) -- (where);
\draw[->] (where) -- (group);
\draw[->] (group) -- (having);
\draw[->] (having.south) -- ++(0,-0.3) -| (win.north);
\draw[->] (win) -- (sel);
\draw[->] (sel) -- (ord);
\draw[->] (ord) -- (lim);
\end{tikzpicture}""",
            },
            "purpose": (
                "Este capítulo desarrolla la monografía completa (Bloques A–H) de **SQL (ISO/IEC 9075:2023)**. SQL no es un "
                "simple lenguaje de consulta superficial, sino un lenguaje declarativo funcional basado en el álgebra y el "
                "cálculo relacional de primer orden (con recursión de punto fijo y funciones analíticas de ventana) que todo "
                "ingeniero de software y datos debe dominar en profundidad."
            ),
            "paragraphs": [
                {
                    "subsection": "sec-v7-1-1",
                    "text": (
                        "Aunque en SQL escribimos léxicamente `SELECT ... FROM ... WHERE ...`, el motor relacional evalúa la "
                        "consulta siguiendo el orden lógico estricto mostrado en la Figura \\ref{fig:fig-sql-logical-execution-order}: "
                        "`FROM` y `JOIN` construyen primero el producto cartesiano filtrado por `ON`; `WHERE` descarta las filas "
                        "cuya condición no evalúa a `TRUE`; `GROUP BY` particiona las filas en grupos; `HAVING` filtra grupos "
                        "agregados; `WINDOW` calcula funciones de ventana; `SELECT` proyecta las columnas y asigna alias; `DISTINCT` "
                        "elimina duplicados; `ORDER BY` ordena el conjunto resultante; y `LIMIT`/`FETCH FIRST` recorta la salida. "
                        "Un escollo clásico proviene de la **lógica trivaluada (3VL)** de `NULL` (`TRUE`, `FALSE`, `UNKNOWN`): "
                        "cualquier comparación ordinaria `col = NULL` o `col <> NULL` produce `UNKNOWN`. Si una subconsulta de "
                        "`WHERE id NOT IN (SELECT parent_id FROM t)` devuelve un solo `NULL`, la expresión `id <> v1 AND id <> NULL` "
                        "evalúa a `UNKNOWN` para todas las filas y la consulta devuelve un conjunto vacío; por ello debe utilizarse "
                        "siempre `WHERE NOT EXISTS (...)` o `IS DISTINCT FROM`."
                    ),
                },
                {
                    "subsection": "sec-v7-1-2",
                    "text": (
                        "En el Nivel Avanzado y Experto (Bloques E y F), las **expresiones de tabla común recursivas** (`WITH RECURSIVE`) "
                        "permiten recorrer árboles jerárquicos y grafos (como el plan contable de nuestro proyecto verificado "
                        "`projects/sql-transactional-ledger`), mientras que las **funciones de ventana** (`OVER (PARTITION BY ... ORDER BY ... ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW)`) "
                        "calculan saldos acumulados, medias móviles y clasificaciones (`ROW_NUMBER`, `RANK`, `DENSE_RANK`, `LAG`, `LEAD`) "
                        "en una sola pasada sin colapsar las filas individuales:\n"
                        "```sql\n"
                        "SELECT\n"
                        "    account_id,\n"
                        "    entry_id,\n"
                        "    debit_cents - credit_cents AS delta_cents,\n"
                        "    SUM(debit_cents - credit_cents) OVER (\n"
                        "        PARTITION BY account_id\n"
                        "        ORDER BY entry_id\n"
                        "        ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW\n"
                        "    ) AS running_balance_cents\n"
                        "FROM journal_lines;\n"
                        "```\n"
                        "Para que el optimizador de costes pueda emplear un índice B+ Tree, los predicados de `WHERE` deben ser "
                        "**sargables** (*Search Argument Able*): aplicar una función sobre la columna indexada (`WHERE YEAR(created_at) = 2026`) "
                        "impide el recorrido por rango del índice y fuerza un escaneo completo de tabla (`Seq Scan`), debiendo "
                        "reescribirse como `WHERE created_at >= '2026-01-01' AND created_at < '2027-01-01'`."
                    ),
                },
            ],
            "definition": (
                "Predicado Sargable en SQL (Search Argument Able): condición de filtro de la forma `columna_indexada OP expresión_constante` "
                "que permite al motor de almacenamiento posicionarse directamente en las páginas hoja de un árbol B+ (`Index Seek / Index Range Scan`) "
                "sin evaluar una transformación fila por fila."
            ),
            "consejo": (
                "En funciones de ventana con `ORDER BY` que calculan acumulados (`SUM(...) OVER (ORDER BY fecha)`), especifica "
                "explícitamente `ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW`: el marco por defecto del estándar SQL cuando "
                "hay `ORDER BY` es `RANGE BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW`, que agrupa de golpe todas las filas empatadas en `fecha`."
            ),
            "self_check": (
                "¿Qué diferencia exacta de numeración producen `ROW_NUMBER()`, `RANK()` y `DENSE_RANK()` ante una secuencia de "
                "puntuaciones `[100, 90, 90, 80]`?"
            ),
            "derivation": {
                "title": "Invariante contable de partida doble en sql-transactional-ledger",
                "assumptions": ["En cada asiento transaccional j, la suma de débitos D_j iguala a la suma de créditos C_j"],
                "steps": [
                    {"equation": r"\sum_{i \in j} D_{j,i} - \sum_{i \in j} C_{j,i} = 0", "justification": "Invariante de balance por asiento individual"},
                    {"equation": r"\sum_{j=1}^{M} \sum_{i \in j} (D_{j,i} - C_{j,i}) = 0", "justification": "El balance global agregado de todo el libro mayor es idénticamente cero"},
                ],
                "Verify": {"left": "(D1 + D2) - (C1 + C2)", "right": "(D1 - C1) + (D2 - C2)"},
            },
            "worked_problem": {
                "prompt": (
                    "En el proyecto `projects/sql-transactional-ledger`, la cuenta de Caja (`account_id = 110`) registra tres "
                    "apuntes sucesivos `(debit_cents, credit_cents)`: `(500000, 0)`, `(125000, 0)` y `(0, 40000)`. Calcula el "
                    "saldo acumulado en céntimos (`running_balance_cents`) que devuelve la función de ventana `SUM(debit_cents - credit_cents) OVER (...)` "
                    "en la tercera fila."
                ),
                "expression": "(500000 - 0) + (125000 - 0) + (0 - 40000)",
                "solution": {
                    "model": "Cálculo de saldo acumulado por función de ventana SQL en sql-transactional-ledger",
                    "given": [
                        {"symbol": "d_1", "value": "500000 centimos", "description": "Aportación inicial de capital"},
                        {"symbol": "d_2", "value": "125000 centimos", "description": "Cobro de factura SaaS"},
                        {"symbol": "c_3", "value": "40000 centimos", "description": "Pago de infraestructura cloud"},
                    ],
                    "steps": [
                        {"step": "Sumamos los tres deltas algebraicos de la partición account_id = 110", "equation": r"B_3 = 500000 + 125000 - 40000", "expression": "(500000 - 0) + (125000 - 0) + (0 - 40000)"},
                    ],
                    "conclusion": "El saldo acumulado en la tercera fila es exactamente 585 000 céntimos (5850.00 EUR), idéntico a la aserción de `verify_ledger.py`.",
                },
            },
            "practice_problems": [
                {"prompt": "Ante las puntuaciones `[100, 90, 90, 80]`, ¿qué valor entero asigna `RANK()` al cuarto elemento (`80`) tras el empate en la posición 2?", "expression": "4", "difficulty": "FOUNDATIONAL", "problem_type": "DIRECT_SUBSTITUTION"},
                {"prompt": "Ante las mismas puntuaciones `[100, 90, 90, 80]`, ¿qué valor entero asigna `DENSE_RANK()` al cuarto elemento (`80`)?", "expression": "3", "difficulty": "FOUNDATIONAL", "problem_type": "DIRECT_SUBSTITUTION"},
                {"prompt": "Un producto cartesiano `CROSS JOIN` entre una tabla de 120 tiendas y una tabla de 365 días del año genera todas las combinaciones `(tienda, día)`. ¿Cuántas filas produce?", "expression": "120 * 365", "difficulty": "INTERMEDIATE", "problem_type": "MULTI_STEP"},
                {"prompt": "Una consulta con paginación `LIMIT 50 OFFSET 400` devuelve la página 9 de resultados. ¿Cuál es el número de orden (base 1) de la primera fila devuelta en esa página ($400 + 1$)?", "expression": "400 + 1", "difficulty": "INTERMEDIATE", "problem_type": "DESIGN"},
            ],
        },
        {
            "id": "cap02-monografia-bash-posix-shell-automatizacion-sistemas",
            "title": "Monografía de Bash y POSIX Shell (Bloques A–H): Tuberías, Redirecciones, Expansiones Seguras, Trap, Herramientas UNIX y Proyectos",
            "part_id": "parte-v-sql-shell-web",
            "part_title": "Monografías de Datos, Automatización de Sistemas y Desarrollo Web/Móvil",
            "sources": ["src-posix-2017", "src-bryant-ohallaron"],
            "learning_objectives": [
                "Distinguir con rigor entre el estándar portable POSIX `sh` (IEEE Std 1003.1) y las extensiones de GNU Bash (`[[ ... ]]`, arrays indexados/asociativos, sustitución de procesos `<(...)`).",
                "Dominar los descriptores de fichero (`0` stdin, `1` stdout, `2` stderr), tuberías (`|`), códigos de salida (`$?`), entrecomillado seguro y expansiones de parámetros (`${var:-def}`, `${var:?err}`).",
                "Escribir scripts de producción robustos con modo estricto (`set -euo pipefail`), limpieza atómica mediante `trap ... EXIT`, integración con `find`/`xargs -0`/`jq`/`awk` y verificación con `shellcheck`.",
            ],
            "concepts": [
                {"id": "cpt-sh-fds-pipes-quoting", "title": "Descriptores de fichero POSIX, redirecciones (2>&1), división de palabras (IFS) y expansiones de parámetros"},
                {"id": "cpt-sh-strict-mode-trap-shellcheck", "title": "Modo estricto (set -euo pipefail), manejadores de señales con trap y análisis estático con ShellCheck"},
            ],
            "subsections": [
                {"id": "sec-v7-2-1", "title": "Bloques A–D: Filosofía UNIX, POSIX sh vs Bash, descriptores de fichero, redirecciones, entrecomillado y expansiones"},
                {"id": "sec-v7-2-2", "title": "Bloques E–H: Modo estricto, arrays, trap de limpieza, herramientas (awk, sed, jq), ShellCheck y 4 proyectos"},
            ],
            "purpose": (
                "Este capítulo presenta la monografía completa (Bloques A–H) de **Bash y POSIX Shell**. Los scripts de shell son "
                "el pegamento universal de los sistemas Linux/macOS, los contenedores Docker y los pipelines de CI/CD. Enseñamos "
                "a escribirlos con rigor de ingeniería de sistemas: inmunes a espacios en nombres de fichero, con limpieza "
                "atómica de directorios temporales y auditados con `shellcheck`."
            ),
            "paragraphs": [
                {
                    "subsection": "sec-v7-2-1",
                    "text": (
                        "En el modelo de procesos POSIX, cada comando hereda tres descriptores de fichero abiertos: `0` (entrada "
                        "estándar), `1` (salida estándar) y `2` (error estándar), y al terminar devuelve un código de estado entero "
                        "entre `0` y `255` donde **`0` significa éxito** (verdadero en `if cmd; then` y en los operadores de cortocircuito "
                        "`cmd1 && cmd2` y `cmd1 || cmd2`) y cualquier valor distinto de cero indica fallo. El orden de las redirecciones "
                        "se evalúa de izquierda a derecha: `cmd > salida.log 2>&1` apunta primero el descriptor `1` a `salida.log` y "
                        "luego duplica el descriptor `2` hacia donde apunta `1` (ambos van al fichero). La causa número uno de fallos "
                        "y vulnerabilidades de inyección en scripts de shell es dejar expansiones sin comillas dobles (`$archivo` en "
                        "lugar de `\"$archivo\"`), lo que dispara la división por palabras (*word splitting* según `IFS`) y la expansión "
                        "de comodines (*pathname expansion* `*`, `?`)."
                    ),
                },
                {
                    "subsection": "sec-v7-2-2",
                    "text": (
                        "Todo script de automatización en Bash debe comenzar configurando el modo estricto (`set -euo pipefail`, que "
                        "aborta ante comandos fallidos, variables no definidas y errores intermedios en una tubería) y registrando "
                        "un manejador `trap` sobre la pseudo-señal `EXIT` para eliminar de forma garantizada los recursos temporales:\n"
                        "```bash\n"
                        "#!/usr/bin/env bash\n"
                        "set -euo pipefail\n"
                        "IFS=$'\\n\\t'\n\n"
                        "readonly WORK_DIR=\"$(mktemp -d)\"\n"
                        "cleanup() {\n"
                        "    rm -rf -- \"$WORK_DIR\"\n"
                        "}\n"
                        "trap cleanup EXIT INT TERM\n\n"
                        "count_non_empty_lines() {\n"
                        "    local target_file=\"${1:?Ruta de fichero obligatoria}\"\n"
                        "    grep -cve '^[[:space:]]*$' -- \"$target_file\"\n"
                        "}\n"
                        "```\n"
                        "Observa el uso de `--` antes de `\"$target_file\"` y `\"$WORK_DIR\"`: indica el fin de las opciones de bandera, "
                        "impidiendo que un fichero cuyo nombre empiece por guion (`-rf`) sea interpretado como una opción por `grep` "
                        "o `rm`. Para procesar listas de ficheros con nombres arbitrarios (incluyendo saltos de línea), se combina "
                        "siempre el delimitador nulo: `find . -type f -name '*.log' -print0 | xargs -0 sha256sum`."
                    ),
                },
            ],
            "definition": (
                "Código de estado de salida por señal en POSIX (`128 + N`): convención del intérprete de comandos según la cual "
                "un proceso terminado de forma abrupta por la señal número $N$ reporta en `$?` el código de salida $128 + N$ "
                "(por ejemplo, `130` para `SIGINT = 2` o `137` para `SIGKILL = 9`)."
            ),
            "consejo": (
                "Integra siempre `shellcheck -S warning script.sh` en tu editor y en CI: detecta al instante variables sin "
                "entrecomillar (SC2086), pérdida de estado de salida al usar `local x=$(cmd)` en una sola línea (SC2155) y "
                "problemas de subshells en tuberías."
            ),
            "self_check": (
                "¿Por qué la línea `local salida=\"$(comando_que_falla)\"` en Bash oculta el código de error de `comando_que_falla` "
                "(porque `local` es un comando builtin cuyo propio código de retorno es `0`) y debe escribirse en dos líneas "
                "separadas (`local salida; salida=\"$(comando_que_falla)\"`)?"
            ),
            "derivation": {
                "title": "Cálculo del código de salida POSIX ($?) ante terminación por señal N",
                "assumptions": ["Cuando un proceso hijo muere por la señal N (1 <= N <= 64), el shell codifica $? = 128 + N"],
                "steps": [
                    {"equation": r"E_{\text{exit}}(N) = 128 + N", "justification": "Bit 7 activado (128) más el número de señal POSIX N"},
                    {"equation": r"N = E_{\text{exit}} - 128", "justification": "Identificación de la señal que mató al proceso a partir del código de retorno"},
                ],
                "Verify": {"left": "(128 + N) - 128", "right": "N"},
            },
            "worked_problem": {
                "prompt": (
                    "Un contenedor en un pipeline de despliegue termina abruptamente con código de salida `$? = 137` tras "
                    "intervenir el *OOM Killer* del kernel Linux (`SIGKILL = 9`), y otro proceso aborta por violación de "
                    "segmento (`SIGSEGV = 11`, código $128 + 11 = 139$). Calcula la suma de los números de las dos señales "
                    "POSIX subyacentes obtenidas restando $128$ a cada código de salida ($(137 - 128) + (139 - 128)$)."
                ),
                "expression": "(137 - 128) + (139 - 128)",
                "solution": {
                    "model": "Decodificación de señales POSIX a partir del código de estado 128 + N",
                    "given": [
                        {"symbol": "E_1", "value": "137", "description": "Código de salida por SIGKILL (128 + 9)"},
                        {"symbol": "E_2", "value": "139", "description": "Código de salida por SIGSEGV (128 + 11)"},
                    ],
                    "steps": [
                        {"step": "Restamos 128 a cada código para recuperar los números de señal 9 y 11 y los sumamos", "equation": r"S = (137 - 128) + (139 - 128)", "expression": "(137 - 128) + (139 - 128)"},
                    ],
                    "conclusion": "Las señales subyacentes son la 9 (SIGKILL) y la 11 (SIGSEGV), cuya suma es 20.",
                },
            },
            "practice_problems": [
                {"prompt": "Un script en ejecución es interrumpido por el usuario pulsando `Ctrl+C` (`SIGINT = 2`). ¿Qué código de salida `$?` reporta el shell ($128 + 2$)?", "expression": "128 + 2", "difficulty": "FOUNDATIONAL", "problem_type": "DIRECT_SUBSTITUTION"},
                {"prompt": "Un proceso recibe la señal de terminación ordenada `SIGTERM = 15` sin capturarla. ¿Cuál es su código de salida ($128 + 15$)?", "expression": "128 + 15", "difficulty": "FOUNDATIONAL", "problem_type": "DIRECT_SUBSTITUTION"},
                {"prompt": "Un comando `xargs -0 -n 50 -P 4` procesa una lista de 600 ficheros pasándolos en lotes de 50 ficheros por invocación. ¿Cuántos procesos hijos lanza en total `xargs` ($600 / 50$)?", "expression": "600 / 50", "difficulty": "INTERMEDIATE", "problem_type": "MULTI_STEP"},
                {"prompt": "Una máscara `umask 027` se resta de los permisos base `666` (octal) para la creación de ficheros regulares ($666 - 27$ en dígito a dígito: $6-0=6$, $6-2=4$, $6-7\\to 0$). ¿Cuál es el permiso octal resultante expresado como entero de tres dígitos?", "expression": "640", "difficulty": "INTERMEDIATE", "problem_type": "DESIGN"},
            ],
        },
        {
            "id": "cap03-monografias-php-ruby-dart-web-movil",
            "title": "Monografías de PHP 8.3+, Ruby 3.3+ y Dart 3.x (Bloques A–H): Motores Zend, YJIT y Compilación AOT/JIT Multiplataforma",
            "part_id": "parte-v-sql-shell-web",
            "part_title": "Monografías de Datos, Automatización de Sistemas y Desarrollo Web/Móvil",
            "sources": ["src-ecmascript-2024", "src-unicode-15"],
            "learning_objectives": [
                "Dominar PHP moderno (8.3+): tipado estricto (`declare(strict_types=1)`), tipos de unión/intersección, `readonly class`, `enum` respaldados, Fibers, OPcache/JIT, Composer, estándares PSR y Laravel/Symfony.",
                "Dominar Ruby (3.3+): modelo de objetos puro, bloques/`Proc`/lambdas, mixins con `Module`, metaprogramación, compilador YJIT, concurrencia con Fibers/Ractors y ecosistema Bundler/RSpec/Rails.",
                "Dominar Dart (3.x): *sound null-safety*, modificadores de clase (`sealed`, `final`, `interface`), coincidencia de patrones, concurrencia por memoria aislada (*Isolates*) y compilación JIT/AOT para Flutter.",
            ],
            "concepts": [
                {"id": "cpt-php8-strict-types-psr", "title": "Tipado estricto en PHP 8.3+, atributos, OPcache/JIT, Composer y arquitectura PSR (Symfony/Laravel)"},
                {"id": "cpt-ruby-blocks-dart-isolates", "title": "Modelo de objetos y bloques en Ruby 3 (YJIT), y sound null-safety con Isolates en Dart 3"},
            ],
            "subsections": [
                {"id": "sec-v7-3-1", "title": "Monografía de PHP 8.3+ (Bloques A–H): Zend Engine, tipado estricto, enums, Composer/PSR y arquitectura web"},
                {"id": "sec-v7-3-2", "title": "Monografías de Ruby 3.3+ y Dart 3.x (Bloques A–H): Bloques/Metaprogramación en Ruby e Isolates/AOT en Dart"},
            ],
            "purpose": (
                "Este capítulo agrupa las monografías completas (Bloques A–H) de tres lenguajes esenciales en el desarrollo "
                "web y móvil de producción: **PHP 8.3+**, **Ruby 3.3+** y **Dart 3.x**."
            ),
            "paragraphs": [
                {
                    "subsection": "sec-v7-3-1",
                    "text": (
                        "**PHP 8.x** ha experimentado una transformación profunda respecto a sus versiones históricas: al encabezar "
                        "cada fichero con `declare(strict_types=1);`, el motor Zend desactiva las coerciones escalares silenciosas "
                        "y verifica contratos de tipos de unión (`int|float`), intersección (`Countable&Iterator`), clases inmutables "
                        "`readonly class`, enumeraciones respaldadas (`enum Status: string`), atributos de metadatos (`#[Route(...)]`) "
                        "y expresiones `match` con comparación estricta (`===`). En producción, **OPcache** mantiene el bytecode "
                        "precompilado en memoria compartida entre trabajadores PHP-FPM (o en servidores persistentes como FrankenPHP / "
                        "RoadRunner), y el gestor de paquetes `Composer` junto con las normas **PSR** (*PHP Standards Recommendations*: "
                        "PSR-4 autoloading, PSR-7 mensajes HTTP, PSR-11 contenedores DI, PSR-15 middlewares) articula los ecosistemas "
                        "de `Symfony` y `Laravel`, verificados estáticamente con `PHPStan` (nivel máximo) y probados con `PHPUnit`."
                    ),
                },
                {
                    "subsection": "sec-v7-3-2",
                    "text": (
                        "En **Ruby 3.3+** (creado por Yukihiro «Matz» Matsumoto), absolutamente todo valor es un objeto y toda operación "
                        "es un envío de mensaje; las clases son abiertas, la herencia múltiple se resuelve linealmente mediante *mixins* "
                        "(`include` e `prepend` de módulos) y cada método puede recibir un bloque anónimo invocado con `yield` o "
                        "convertido en clausura `Proc`. Con el compilador JIT en proceso **YJIT** (escrito en Rust dentro de CRuby), "
                        "las aplicaciones `Ruby on Rails` logran mejoras notables de latencia, mientras que los **Ractors** proporcionan "
                        "paralelismo de actores sin compartir estado mutable. Por su parte, **Dart 3.x** ofrece **nulabilidad sólida** "
                        "(*sound null-safety*: el compilador AOT garantiza que una variable no anulable jamás contiene `null`, optimizando "
                        "el código máquina emitido), clases selladas (`sealed class`) con *pattern matching* exhaustivo y un modelo de "
                        "concurrencia basado en **Isolates** (hebras con montículos de memoria independientes que se comunican por "
                        "puertos de mensajes o transferencia de `TransferableTypedData`), compilando en modo JIT con *stateful hot reload* "
                        "durante el desarrollo y en binario nativo **AOT** para producción en iOS, Android, escritorio y web:\n"
                        "```dart\n"
                        "sealed class ApiResponse<T> {}\n"
                        "final class ApiSuccess<T> extends ApiResponse<T> {\n"
                        "  final T data;\n"
                        "  const ApiSuccess(this.data);\n"
                        "}\n"
                        "final class ApiFailure<T> extends ApiResponse<T> {\n"
                        "  final int statusCode;\n"
                        "  const ApiFailure(this.statusCode);\n"
                        "}\n\n"
                        "String describeResponse<T>(ApiResponse<T> res) => switch (res) {\n"
                        "  ApiSuccess(data: final d)       => 'OK: $d',\n"
                        "  ApiFailure(statusCode: final c) => 'HTTP Error $c',\n"
                        "};\n"
                        "```"
                    ),
                },
            ],
            "definition": (
                "Nulabilidad Sólida (Sound Null-Safety en Dart 3): propiedad del sistema de tipos según la cual, una vez que "
                "el programa compila, es matemáticamente imposible en tiempo de ejecución que una expresión de tipo no anulable "
                "`T` evalúe a `null`, permitiendo al compilador AOT eliminar comprobaciones de puntero nulo."
            ),
            "consejo": (
                "En PHP 8+, incluye siempre `declare(strict_types=1);` en la primera línea de todos tus ficheros `.php` y "
                "utiliza la expresión `match ($valor) { ... }` en lugar de `switch ($valor)`: `match` compara con identidad "
                "estricta (`===`), no requiere `break` y lanza `UnhandledMatchError` si olvidas un caso."
            ),
            "self_check": (
                "¿Qué diferencia exacta existe en Ruby entre una instancia de `Proc.new { return 1 }` y un `lambda` (`-> { return 1 }`) "
                "en cuanto al efecto de `return` y la comprobación del número de argumentos?"
            ),
            "derivation": {
                "title": "Dimensionamiento de trabajadores PHP-FPM (pm.max_children) en función de la RAM disponible",
                "assumptions": ["Sea M_avail la RAM dedicada a PHP-FPM y m_worker el consumo medio de memoria residente (RSS) no compartida por proceso trabajador"],
                "steps": [
                    {"equation": r"N_{\text{workers}} = \lfloor M_{\text{avail}} / m_{\text{worker}} \rfloor", "justification": "Cota máxima de procesos hijo simultáneos sin provocar paginación a disco (swap)"},
                    {"equation": r"M_{\text{used}} = N_{\text{workers}} \cdot m_{\text{worker}}", "justification": "Memoria total reservada por el pool en carga punta"},
                ],
                "Verify": {"left": "N_workers * m_worker", "right": "m_worker * N_workers"},
            },
            "worked_problem": {
                "prompt": (
                    "Un servidor de producción con $8192\\text{ MiB}$ de RAM reserva $2048\\text{ MiB}$ para el sistema operativo "
                    "y el búfer de OPcache/Redis, dejando $M_{\\text{avail}} = 6144\\text{ MiB}$ para el pool de trabajadores "
                    "PHP-FPM. Si cada trabajador consume en carga punta $m_{\\text{worker}} = 48\\text{ MiB}$ de memoria privada, "
                    "calcula el valor óptimo de `pm.max_children` ($6144 / 48$)."
                ),
                "expression": "6144 / 48",
                "solution": {
                    "model": "Dimensionamiento de pm.max_children en PHP-FPM sin agotamiento de RAM",
                    "given": [
                        {"symbol": "M_avail", "value": "6144 MiB", "description": "RAM neta disponible para trabajadores PHP-FPM"},
                        {"symbol": "m_worker", "value": "48 MiB", "description": "Consumo privado RSS por proceso trabajador"},
                    ],
                    "steps": [
                        {"step": "Dividimos la memoria disponible entre el consumo por trabajador", "equation": r"N_{\max} = \frac{6144}{48}", "expression": "6144 / 48"},
                    ],
                    "conclusion": "El servidor puede ejecutar de forma segura hasta 128 trabajadores PHP-FPM concurrentes.",
                },
            },
            "practice_problems": [
                {"prompt": "En Flutter/Dart, para sostener una tasa de refresco de pantalla de $120\\text{ Hz}$, el presupuesto total por fotograma (construcción + diseño + pintado) es $1000 / 120\\text{ ms}$. ¿Cuántos milisegundos caben en 12 fotogramas consecutivos?", "expression": "12 * (1000 / 120)", "difficulty": "FOUNDATIONAL", "problem_type": "DIRECT_SUBSTITUTION"},
                {"prompt": "En Ruby, la expresión `(1..10).select(&:even?).map { |x| x * 3 }.sum` suma el triple de los pares del 2 al 10 ($(2+4+6+8+10) \\times 3$). ¿Cuál es el resultado?", "expression": "(2 + 4 + 6 + 8 + 10) * 3", "difficulty": "FOUNDATIONAL", "problem_type": "DIRECT_SUBSTITUTION"},
                {"prompt": "Si OPcache evita recompilar 85 ficheros PHP por petición HTTP (ahorrando $0.4\\text{ ms}$ por fichero), ¿cuántos milisegundos de CPU ahorra en cada petición ($85 \\times 0.4$)?", "expression": "85 * 0.4", "difficulty": "INTERMEDIATE", "problem_type": "MULTI_STEP"},
                {"prompt": "Un Isolate de fondo en Dart procesa un lote de 400 imágenes en grupos de 25 imágenes devolviendo el progreso al Isolate principal tras cada grupo. ¿Cuántos mensajes de progreso envía?", "expression": "400 / 25", "difficulty": "INTERMEDIATE", "problem_type": "DESIGN"},
            ],
        },
        {
            "id": "cap04-monografia-haskell-funcional-puro-tipos-monadas",
            "title": "Monografía de Haskell (Bloques A–H): Pureza, Evaluación Perezosa, Inferencia Hindley-Milner, Typeclasses y Mónadas",
            "part_id": "parte-v-funcionales-estaticos",
            "part_title": "Monografías de Lenguajes Funcionales Estáticos y Concurrentes (Haskell, OCaml, F#, Scala, BEAM, Lisp)",
            "sources": ["src-pierce-tapl", "src-knuth-taocp"],
            "learning_objectives": [
                "Comprender la transparencia referencial, la evaluación no estricta (perezosa por necesidad, *call-by-need* con *thunks*), la currificación universal y el sistema de tipos Hindley-Milner de GHC.",
                "Diseñar tipos de datos algebraicos (`data`, `newtype`), sinónimos de tipos, polimorfismo de clases de tipos (`Eq`, `Ord`, `Monoid`) y tipos de orden superior (*Higher-Kinded Types*, `* -> *`).",
                "Dominar la jerarquía `Functor` (`fmap`), `Applicative` (`<*>`) y `Monad` (`>>=`, notación `do`), el aislamiento puro de efectos con `IO`, `STM` (*Software Transactional Memory*) y pruebas de propiedades con `QuickCheck`.",
            ],
            "concepts": [
                {"id": "cpt-hs-lazy-hm-typeclasses", "title": "Transparencia referencial, reducción de grafos perezosa (WHNF), inferencia Hindley-Milner y clases de tipos"},
                {"id": "cpt-hs-functor-monad-stm", "title": "Leyes algebraicas de Functor/Applicative/Monad, mónada IO, memoria transaccional STM y QuickCheck"},
            ],
            "subsections": [
                {"id": "sec-v7-4-1", "title": "Bloques A–D: Filosofía pura de Haskell, GHC/Cabal/Stack, currificación, evaluación perezosa, ADTs y Typeclasses"},
                {"id": "sec-v7-4-2", "title": "Bloques E–H: Functor, Applicative, Monad (IO, Reader, State, Either), concurrencia STM, QuickCheck y proyectos"},
            ],
            "purpose": (
                "Este capítulo desarrolla la monografía completa (Bloques A–H) de **Haskell (GHC 9.x)**. Estudiar Haskell "
                "enseña en su forma más pura los conceptos que posteriormente han adoptado Rust (`Trait`, `Option`, `Result`), "
                "Scala, Swift y TypeScript: tipos algebraicos, clases de tipos, composición monádica y pruebas basadas en propiedades."
            ),
            "paragraphs": [
                {
                    "subsection": "sec-v7-4-1",
                    "text": (
                        "En **Haskell**, toda función es matemática y **referencialmente transparente**: para una misma entrada, "
                        "produce siempre la misma salida sin mutar variables globales ni realizar entrada/salida oculta. Todas las "
                        "funciones de varios argumentos están currificadas por defecto (`add :: Int -> Int -> Int` es `Int -> (Int -> Int)`), "
                        "permitiendo la aplicación parcial directa (`map (+10) [1, 2, 3]`). La estrategia de evaluación por defecto es "
                        "no estricta (*lazy evaluation* / *call-by-need*): las expresiones no se evalúan al pasarse como argumento, "
                        "sino que se empaquetan en una suspensión en el montículo denominada **thunk** que se reduce a *Weak Head Normal "
                        "Form* (WHNF) solo cuando la coincidencia de patrones exige conocer su constructor exterior, compartiendo el "
                        "resultado para no recalcularlo. Cuando se acumulan sumas en un pliegue izquierdo, usar `foldl` perezoso "
                        "construye una cadena de $N$ *thunks* `(((0 + x1) + x2) ...)` que desborda la memoria (*space leak*); "
                        "la solución profesional consiste en usar siempre la variante estricta `Data.List.foldl'`."
                    ),
                },
                {
                    "subsection": "sec-v7-4-2",
                    "text": (
                        "Haskell parametriza constructores de tipos de *kind* `* -> *` mediante la jerarquía algebraica `Functor` "
                        "(`fmap :: (a -> b) -> f a -> f b`), `Applicative` (`pure :: a -> f a`, `(<*>) :: f (a -> b) -> f a -> f b`) "
                        "y **`Monad`** (`(>>=) :: m a -> (a -> m b) -> m b`). Toda instancia de `Monad` debe satisfacer las tres "
                        "leyes monádicas: identidad por la izquierda (`return a >>= k == k a`), identidad por la derecha (`m >>= return == m`) "
                        "y asociatividad (`(m >>= k) >>= h == m >>= (\\x -> k x >>= h)`). La notación `do` es azúcar sintáctico directo "
                        "sobre `(>>=)`:\n"
                        "```haskell\n"
                        "module SafeEval (Expr(..), eval) where\n\n"
                        "data Expr = Lit Int | Add Expr Expr | Div Expr Expr\n"
                        "  deriving (Show, Eq)\n\n"
                        "eval :: Expr -> Either String Int\n"
                        "eval (Lit n)     = Right n\n"
                        "eval (Add e1 e2) = do\n"
                        "  v1 <- eval e1\n"
                        "  v2 <- eval e2\n"
                        "  Right (v1 + v2)\n"
                        "eval (Div e1 e2) = do\n"
                        "  v1 <- eval e1\n"
                        "  v2 <- eval e2\n"
                        "  if v2 == 0 then Left \"division by zero\" else Right (div v1 v2)\n"
                        "```\n"
                        "Gracias a que las lecturas y escrituras de estado están controladas por el sistema de tipos, Haskell ofrece "
                        "**Software Transactional Memory (STM)**: transacciones en memoria (`TVar`, `atomically`, `retry`, `orElse`) "
                        "que se componen sin posibilidad de interbloqueos (*deadlocks*), ya que el tipo `STM a` prohíbe estáticamente "
                        "ejecutar efectos `IO` irreversibles dentro de un bloque que podría reintentarse."
                    ),
                },
            ],
            "definition": (
                "Forma Normal Débil a la Cabeza (Weak Head Normal Form, WHNF en Haskell): estado de reducción de una expresión "
                "en el que su capa más externa ya no es un redex (es un constructor de datos como `Just thunk`, un literal primitivo "
                "o una abstracción lambda `\\x -> ...`), aunque sus subexpresiones internas permanezcan sin evaluar."
            ),
            "consejo": (
                "En Haskell de producción, utiliza siempre `newtype` en lugar de `data` cuando envuelvas un único campo con un "
                "solo constructor (`newtype CustomerId = CustomerId Int`): `newtype` garantiza distinción de tipos en compilación "
                "pero se borra por completo en ejecución con cero sobrecoste de puntero."
            ),
            "self_check": (
                "¿Por qué el sistema de tipos de Haskell impide ejecutar `putStrLn \" enviando misil \"` dentro de una transacción "
                "`atomically :: STM a -> IO a` de memoria transaccional por software?"
            ),
            "derivation": {
                "title": "Fusión de listas (Stream/Short-cut Fusion foldr/build) en el optimizador de GHC",
                "assumptions": ["Una cadena map f . map g . filter p sobre N elementos sin fusión aloja 3 listas intermedias de N celdas cons; con la regla foldr/build de GHC aloja 0 celdas intermedias"],
                "steps": [
                    {"equation": r"\text{map } f \circ \text{map } g = \text{map } (f \circ g)", "justification": "Segunda ley de los funtores verificada por las reglas de reescritura de GHC"},
                    {"equation": r"\text{foldr } k \, z \, (\text{build } g) = g \, k \, z", "justification": "Teorema de desforestación de corto circuito (Gill, Launchbury y Peyton Jones)"},
                ],
                "Verify": {"left": "3 * N - 0", "right": "3 * N"},
            },
            "worked_problem": {
                "prompt": (
                    "En GHC de 64 bits, cada celda `(:)` de una lista enlazada `[Int]` en el montículo ocupa $3$ palabras de "
                    "$8\\text{ B}$ ($24\\text{ B}$ por nodo). Una tubería `sum (map (*2) (map (+1) [1..N]))` para $N = 100000$ "
                    "elementos, si se evaluara de forma estricta sin fusión, alojaría $3$ listas de $100000$ celdas ($3 \\times 100000 \\times 24\\text{ B}$). "
                    "Gracias a la fusión `foldr/build` de GHC con `-O2`, las tres listas desaparecen y el bucle se ejecuta en "
                    "registros alojando $0\\text{ B}$ de celdas. Calcula cuántos kilobytes (dividiendo entre 1000) ahorra la desforestación."
                ),
                "expression": "(3 * 100000 * 24) / 1000",
                "solution": {
                    "model": "Ahorro de montículo mediante desforestación foldr/build en GHC",
                    "given": [
                        {"symbol": "k_listas", "value": "3", "description": "Listas intermedias eliminadas"},
                        {"symbol": "N", "value": "100000", "description": "Elementos de la secuencia"},
                        {"symbol": "S_cons", "value": "24 B", "description": "Tamaño de una celda cons en GHC 64 bits"},
                    ],
                    "steps": [
                        {"step": "Multiplicamos 3 * 100000 * 24 B y dividimos entre 1000 B/kB", "equation": r"\Delta M_{\text{kB}} = \frac{3 \cdot 100000 \cdot 24}{1000}", "expression": "(3 * 100000 * 24) / 1000"},
                    ],
                    "conclusion": "La fusión de flujos de GHC evita alojar 7200 kB (7.2 MB) de celdas intermedias.",
                },
            },
            "practice_problems": [
                {"prompt": "En el evaluador monádico `eval (Div (Add (Lit 20) (Lit 22)) (Lit 6))`, ¿qué valor entero `Right v` devuelve la expresión ($(20 + 22) / 6$)?", "expression": "(20 + 22) / 6", "difficulty": "FOUNDATIONAL", "problem_type": "DIRECT_SUBSTITUTION"},
                {"prompt": "`QuickCheck` ejecuta por defecto 100 casos generados aleatoriamente por cada propiedad `prop_*`. Si un módulo define 18 propiedades, ¿cuántos casos de prueba verifica `quickCheck` en total?", "expression": "18 * 100", "difficulty": "FOUNDATIONAL", "problem_type": "DIRECT_SUBSTITUTION"},
                {"prompt": "En la expresión aplicativa `[(+10), (*2), (+100)] <*> [1, 2, 3, 4]`, la instancia `Applicative` de listas aplica cada una de las 3 funciones a cada uno de los 4 valores. ¿Cuántos elementos contiene la lista resultante?", "expression": "3 * 4", "difficulty": "INTERMEDIATE", "problem_type": "MULTI_STEP"},
                {"prompt": "Un `newtype` en Haskell envuelve un `Int64` (8 B). ¿Cuántos bytes de sobrecoste adicional añade el constructor del `newtype` en tiempo de ejecución tras el borrado de GHC?", "expression": "0", "difficulty": "INTERMEDIATE", "problem_type": "DESIGN"},
            ],
        },
        {
            "id": "cap05-monografias-ocaml-fsharp-ml-sistemas-tipos",
            "title": "Monografías de OCaml 5.x y F# (.NET) (Bloques A–H): Módulos de Orden Superior (Functors), Efectos Algebraicos y Expresiones de Computación",
            "part_id": "parte-v-funcionales-estaticos",
            "part_title": "Monografías de Lenguajes Funcionales Estáticos y Concurrentes (Haskell, OCaml, F#, Scala, BEAM, Lisp)",
            "sources": ["src-pierce-tapl", "src-csharp-spec"],
            "learning_objectives": [
                "Dominar la familia ML (Robin Milner): evaluación estricta por valor con inferencia Hindley-Milner completa, tipos algebraicos, coincidencia de patrones y mutabilidad explícita (`ref`, `mutable`).",
                "En OCaml 5.x: programar módulos parametrizados de orden superior (*Functors*), variantes polimórficas, paralelismo nativo con *Domains* y concurrencia mediante manejadores de efectos algebraicos (*Effect Handlers*). ",
                "En F#: dominar el operador tubería (`|>`), unidades de medida estáticas (`[<Measure>]`), proveedores de tipos y expresiones de computación (`async { ... }`, `seq { ... }`).",
            ],
            "concepts": [
                {"id": "cpt-ocaml-functors-effects", "title": "Sistema de módulos y Functors de OCaml, representación de enteros etiquetados (63 bits) y efectos algebraicos en OCaml 5"},
                {"id": "cpt-fsharp-units-computation", "title": "Modelado de dominio funcional en F#, unidades de medida físicas en compilación y expresiones de computación"},
            ],
            "subsections": [
                {"id": "sec-v7-5-1", "title": "Monografía de OCaml 5.x (Bloques A–H): Inferencia ML, Functors de módulos, representación en memoria y efectos algebraicos"},
                {"id": "sec-v7-5-2", "title": "Monografía de F# sobre .NET (Bloques A–H): Tuberías, unidades de medida ([<Measure>]), Computation Expressions y proyectos"},
            ],
            "purpose": (
                "Este capítulo presenta las monografías completas (Bloques A–H) de los dos principales exponentes industriales "
                "de la familia **ML** (*Meta Language*): **OCaml 5.x** (el lenguaje de elección para escribir compiladores, "
                "demostradores de teoremas como Coq/Rocq y sistemas de negociación algorítmica de baja latencia como en Jane Street) "
                "y **F#** (el lenguaje funcional primero del ecosistema .NET)."
            ),
            "paragraphs": [
                {
                    "subsection": "sec-v7-5-1",
                    "text": (
                        "**OCaml** (desarrollado en INRIA por Xavier Leroy y su equipo) combina evaluación estricta predecible, un "
                        "compilador nativo rapidísimo (`ocamlopt`) con un recolector generacional incremental de latencias sub-milisegundo "
                        "y el sistema de módulos más potente de la industria: en OCaml, los módulos (`struct ... end`) tienen tipos "
                        "llamados firmas (`sig ... end`), y un **Functor** es una función a nivel de módulos que recibe un módulo como "
                        "argumento y devuelve un nuevo módulo especializado (por ejemplo, `Map.Make(String)` construye un árbol AVL "
                        "tipado para claves `string`). En cuanto a su representación de bajo nivel en 64 bits, OCaml reserva el bit "
                        "menos significativo de cada palabra como etiqueta del recolector de basura (`1` para enteros inmediatos sin "
                        "puntero `int` de **63 bits**, y `0` para punteros alineados al montículo). Además, **OCaml 5** incorpora "
                        "paralelismo multinúcleo real (`Domain.spawn`) y **manejadores de efectos algebraicos** (*Effect Handlers*), "
                        "que permiten definir planificadores asíncronos como bibliotecas puras sin colorear las funciones con `async`."
                    ),
                },
                {
                    "subsection": "sec-v7-5-2",
                    "text": (
                        "Por su parte, **F#** (diseñado por Don Syme en Microsoft Research) traslada la elegancia de OCaml al CLR de "
                        ".NET. Entre sus innovaciones más notables destacan las **unidades de medida verificadas en compilación** "
                        "(`[<Measure>] type m`, `[<Measure>] type s`, `[<Measure>] type N = kg m / s^2`), que previenen errores "
                        "dimensionales (como el accidente de la sonda Mars Climate Orbiter) y se borran por completo al emitir el "
                        "bytecode CIL con coste cero en tiempo de ejecución:\n"
                        "```fsharp\n"
                        "[<Measure>] type m\n"
                        "[<Measure>] type s\n"
                        "[<Measure>] type kg\n\n"
                        "let kineticEnergy (mass: float<kg>) (velocity: float<m/s>) : float<kg * m^2 / s^2> =\n"
                        "    0.5 * mass * velocity * velocity\n"
                        "```\n"
                        "Asimismo, F# generaliza las mónadas, los generadores y las consultas mediante una construcción sintáctica "
                        "unificada: las **expresiones de computación** (*Computation Expressions*: `seq { yield ... }`, `async { let! x = ... }`, "
                        "`task { ... }`, `result { ... }`)."
                    ),
                },
            ],
            "definition": (
                "Entero etiquetado de 63 bits en OCaml (Tagged Integer): representación en máquina de 64 bits en la que un "
                "entero matemático $n$ se codifica en registro como la palabra $(2n + 1)$ (desplazado 1 bit a la izquierda con "
                "el bit menos significativo fijado a `1`), permitiendo al recolector de basura distinguirlo instantáneamente "
                "de cualquier puntero alineado (cuyo bit 0 es `0`) sin alojar en el montículo."
            ),
            "consejo": (
                "En OCaml, define siempre un fichero de interfaz explícito `.mli` para cada módulo `.ml`: mantener abstractos "
                "los tipos internos en el `.mli` garantiza el encapsulamiento de invariantes y acelera la compilación incremental con `dune`."
            ),
            "self_check": (
                "¿Por qué la codificación de un entero $n$ como $2n + 1$ en OCaml permite que la suma de dos enteros etiquetados "
                "se implemente en ensamblador como `(a + b) - 1` en un solo ciclo de reloj sin desencajonar punteros?"
            ),
            "derivation": {
                "title": "Aritmética directa sobre enteros etiquetados (2n + 1) en el compilador nativo ocamlopt",
                "assumptions": ["En OCaml, el entero n se representa en registro como R(n) = 2*n + 1"],
                "steps": [
                    {"equation": r"R(a) + R(b) - 1 = (2a + 1) + (2b + 1) - 1 = 2(a + b) + 1", "justification": "La suma de las representaciones menos 1 produce exactamente la representación etiquetada R(a + b)"},
                    {"equation": r"R(a + b) = 2(a + b) + 1", "justification": "Invariante de etiqueta del bit 0 conservado sin desplazamientos adicionales"},
                ],
                "Verify": {"left": "(2 * a + 1) + (2 * b + 1) - 1", "right": "2 * (a + b) + 1"},
            },
            "worked_problem": {
                "prompt": (
                    "En el compilador nativo `ocamlopt` de 64 bits, cualquier entero `int` $n$ se almacena en un registro de CPU "
                    "mediante la representación etiquetada $R(n) = 2n + 1$ (con el bit 0 puesto a 1 para indicar al recolector "
                    "de basura que no es un puntero). Calcula el valor decimal exacto de la palabra en registro $R(n)$ para el "
                    "entero de aplicación $n = 1500$."
                ),
                "expression": "2 * 1500 + 1",
                "solution": {
                    "model": "Codificación de enteros inmediatos de 63 bits (2n + 1) en OCaml",
                    "given": [
                        {"symbol": "n", "value": "1500", "description": "Valor entero lógico en el programa OCaml"},
                    ],
                    "steps": [
                        {"step": "Desplazamos 1 bit a la izquierda (multiplicar por 2) y activamos el bit de etiqueta (+1)", "equation": r"R(1500) = 2 \cdot 1500 + 1", "expression": "2 * 1500 + 1"},
                    ],
                    "conclusion": "El registro de CPU almacena el valor impar 3001 (0xBB9), que el recolector identifica en O(1) como un valor inmediato no rastreable.",
                },
            },
            "practice_problems": [
                {"prompt": "En OCaml, si un registro contiene la palabra etiquetada $R(n) = 85$, ¿cuál es el entero lógico $n = (85 - 1) / 2$?", "expression": "(85 - 1) / 2", "difficulty": "FOUNDATIONAL", "problem_type": "DIRECT_SUBSTITUTION"},
                {"prompt": "En F#, la función `kineticEnergy` calcula $0.5 \\cdot m \\cdot v^2$. Para una masa $m = 4\\text{ kg}$ y velocidad $v = 15\\text{ m/s}$, ¿cuántos julios ($\\text{kg}\\cdot\\text{m}^2/\\text{s}^2$) devuelve?", "expression": "0.5 * 4 * 15 * 15", "difficulty": "FOUNDATIONAL", "problem_type": "DIRECT_SUBSTITUTION"},
                {"prompt": "¿Cuántos bytes adicionales ocupa en el ensamblado `.dll` de .NET la anotación de unidades `[<Measure>] type kg` tras la compilación de F#?", "expression": "0", "difficulty": "INTERMEDIATE", "problem_type": "MULTI_STEP"},
                {"prompt": "En OCaml de 64 bits, cada bloque en el montículo tiene 1 palabra de cabecera (8 B) que codifica tamaño, color GC y etiqueta de constructor, seguida de $k$ campos de 8 B. ¿Cuántos bytes ocupa un nodo de árbol binario con 3 campos (`valor`, `izq`, `der`)?", "expression": "8 + 3 * 8", "difficulty": "INTERMEDIATE", "problem_type": "DESIGN"},
            ],
        },
        {
            "id": "cap06-monografias-beam-elixir-erlang-scala3-clojure-lisp",
            "title": "Monografías de Elixir, Erlang/OTP (BEAM), Scala 3, Clojure y Lisp/Scheme (Bloques A–H)",
            "part_id": "parte-v-funcionales-estaticos",
            "part_title": "Monografías de Lenguajes Funcionales Estáticos y Concurrentes (Haskell, OCaml, F#, Scala, BEAM, Lisp)",
            "sources": ["src-pierce-tapl", "src-kleppmann-ddia"],
            "learning_objectives": [
                "Comprender la máquina virtual BEAM (Erlang/Elixir): aislamiento total de memoria por proceso, recolección de basura por proceso, paso de mensajes asíncrono y árboles de supervisión OTP (*let it crash*).",
                "Dominar Elixir (tuberías `|>`, protocolos, macros higiénicas, `GenServer`, `Supervisor`, `Phoenix LiveView`) y Erlang/OTP (coincidencia de patrones binarios, actualización de código en caliente).",
                "Dominar Scala 3 (cálculo DOT, `enum`, `given`/`using`, tipos unión/intersección, ZIO/Cats Effect), Clojure (estructuras persistentes HAMT, átomos/STM, REPL) y Lisp/Scheme (homoiconicidad, S-expressions y macros `defmacro`/`syntax-rules`).",
            ],
            "concepts": [
                {"id": "cpt-beam-erlang-elixir-otp", "title": "Aislamiento de procesos en la máquina virtual BEAM, buzón de mensajes y árboles de supervisión OTP"},
                {"id": "cpt-scala3-clojure-lisp-macros", "title": " Abstracciones contextuales given/using en Scala 3, estructuras persistentes en Clojure y homoiconicidad en Lisp/Scheme"},
            ],
            "subsections": [
                {"id": "sec-v7-6-1", "title": "Monografías de Erlang/OTP y Elixir sobre la BEAM (Bloques A–H): Actores aislados, GenServer y Supervisores"},
                {"id": "sec-v7-6-2", "title": "Monografías de Scala 3, Clojure y Common Lisp / Scheme (Bloques A–H): Tipos dependientes, HAMT y macros"},
            ],
            "figure": {
                "key": "fig-otp-supervision-tree",
                "caption": "Árbol de supervisión OTP en Erlang/Elixir: los supervisores monitorizan procesos trabajadores (GenServer) aislados en memoria y aplican estrategias deterministas de reinicio (one_for_one, rest_for_one, one_for_all).",
                "tikz": r"""\begin{tikzpicture}[node distance=1.4cm, >=stealth, thick, font=\small]
\node[draw=blue!70!black, fill=blue!8, rounded corners, minimum width=3.6cm, minimum height=0.9cm, align=center] (root) {Supervisor Raíz\\(\texttt{:one\_for\_one})};
\node[draw=teal!70!black, fill=teal!10, rounded corners, minimum width=3.2cm, minimum height=0.9cm, align=center, below left=1.1cm and 0.6cm of root] (w1) {\texttt{GenServer}: Telemetría\\(Montículo Aislado)};
\node[draw=orange!75!black, fill=orange!12, rounded corners, minimum width=3.4cm, minimum height=0.9cm, align=center, below right=1.1cm and 0.6cm of root] (sub) {Supervisor de Sesiones\\(\texttt{:DynamicSupervisor})};
\draw[->] (root) -- (w1);
\draw[->] (root) -- (sub);
\end{tikzpicture}""",
            },
            "purpose": (
                "Este capítulo desarrolla las monografías completas (Bloques A–H) de cinco lenguajes fundamentales de la "
                "computación concurrente y funcional: **Erlang/OTP** y **Elixir** (sobre la máquina virtual BEAM), **Scala 3**, "
                "**Clojure** y **Lisp/Scheme**."
            ),
            "paragraphs": [
                {
                    "subsection": "sec-v7-6-1",
                    "text": (
                        "Creado por Joe Armstrong, Robert Virding y Mike Williams en Ericsson para conmutadores telefónicos con una "
                        "disponibilidad del $99.9999999\\%$ (*nueve nueves*), **Erlang** y su compañero moderno **Elixir** (creado por "
                        "José Valim) se ejecutan sobre la máquina virtual **BEAM**. En la BEAM, cada actor (proceso Erlang/Elixir, "
                        "que ocupa apenas $\\approx 2.6\\text{ KiB}$ iniciales) posee su **propio montículo privado inmutable** y su "
                        "propio recolector de basura independiente: no existe memoria mutable compartida ni pausas globales *Stop-The-World* "
                        "que detengan a todo el nodo. La tolerancia a fallos se estructura mediante **OTP** (*Open Telecom Platform*) "
                        "y la filosofía *«Let it crash»*: como ilustra la Figura \\ref{fig:fig-otp-supervision-tree}, cuando un "
                        "proceso trabajador (`GenServer`) encuentra un estado corrupto inesperado, muere limpiamente liberando su "
                        "montículo instantáneamente y su `Supervisor` padre lo reinicia a un estado inicial conocido válido:\n"
                        "```elixir\n"
                        "defmodule TelemetryCounter do\n"
                        "  use GenServer\n\n"
                        "  def start_link(initial \\\\ 0), do: GenServer.start_link(__MODULE__, initial, name: __MODULE__)\n"
                        "  def increment(delta),          do: GenServer.call(__MODULE__, {:inc, delta})\n\n"
                        "  @impl true\n"
                        "  def init(initial), do: {:ok, initial}\n\n"
                        "  @impl true\n"
                        "  def handle_call({:inc, delta}, _from, state) do\n"
                        "    new_state = state + delta\n"
                        "    {:reply, new_state, new_state}\n"
                        "  end\n"
                        "end\n"
                        "```"
                    ),
                },
                {
                    "subsection": "sec-v7-6-2",
                    "text": (
                        "**Scala 3** (Martin Odersky, EPFL) unifica la programación orientada a objetos y funcional sobre el cálculo "
                        "**DOT** (*Dependent Object Types*), reemplazando los antiguos `implicit` sobrecargados de Scala 2 por las "
                        "abstracciones contextuales limpias `given` y `using`, tipos unión (`A | B`) e intersección (`A & B`) y "
                        "enumeraciones algebraicas (`enum`). Por su parte, **Lisp** (John McCarthy, 1958; estandarizado en **Common "
                        "Lisp** y **Scheme** R7RS) y **Clojure** (Rich Hickey, sobre la JVM) se distinguen por la **homoiconicidad** "
                        "(*el código es datos*: el programa se escribe directamente como listas de símbolos o vectores que son el "
                        "propio AST del lenguaje), lo que permite escribir macros sintácticas que transforman el lenguaje desde dentro. "
                        "Clojure aporta además vectores y mapas persistentes inmutables implementados como árboles trie de factor "
                        "de ramificación 32 (**HAMT**, *Hash Array Mapped Trie* con compartición estructural $O(\\log_{32} N)$), "
                        "donde producir una versión modificada de un vector de un millón de elementos copia a lo sumo $\\lceil \\log_{32}(10^6) \\rceil = 4$ "
                        "nodos internos."
                    ),
                },
            ],
            "definition": (
                "Homoiconicidad (Code-as-Data en la familia Lisp): propiedad de un lenguaje cuya representación sintáctica "
                "primaria (S-expressions en Common Lisp/Scheme y EDN en Clojure) coincide directamente con las estructuras "
                "de datos primitivas manipulables por el propio lenguaje, haciendo trivial la metaprogramación por macros."
            ),
            "consejo": (
                "En Erlang y Elixir, evita acumular millones de mensajes sin procesar en el buzón (*mailbox*) de un único "
                "`GenServer` usando `cast` asíncrono sin control: utiliza `GenServer.call` (que aplica contrapresión síncrona "
                "al llamador) o procesadores con demanda controlada como `GenStage` y `Broadway`."
            ),
            "self_check": (
                "¿Por qué en un vector persistente inmutable de Clojure con factor de ramificación $B = 32$, acceder o actualizar "
                "un elemento entre $32^4 = 1048576$ elementos requiere recorrer únicamente 4 niveles de punteros?"
            ),
            "derivation": {
                "title": "Profundidad y copia por compartición estructural (Path Copying) en árboles persistentes de ramificación 32 (Clojure/Scala)",
                "assumptions": ["Un árbol persistente de factor de ramificación B = 32 y profundidad d almacena hasta 32^d elementos"],
                "steps": [
                    {"equation": r"N_{\max}(d) = 32^d = 2^{5d}", "justification": "Cada nivel se indexa con 5 bits de la clave o índice"},
                    {"equation": r"B_{\text{copied}}(d) = d \cdot 32 \cdot W", "justification": "Una actualización inmutable clona únicamente los d nodos de 32 punteros a lo largo del camino desde la raíz"},
                ],
                "Verify": {"left": "32**4", "right": "1048576"},
            },
            "worked_problem": {
                "prompt": (
                    "En el vector persistente inmutable de Clojure y Scala (`Vector`), cada nodo interno contiene $32$ punteros. "
                    "Para un vector con $N = 1048576$ elementos ($32^4$, profundidad $d = 4$ niveles), crear un nuevo vector "
                    "con un elemento actualizado mediante **compartición estructural** (*path copying*) clona únicamente los "
                    "$d = 4$ nodos de $32$ referencias a lo largo del camino modificado, reutilizando todos los demás nodos. "
                    "Calcula cuántas referencias de puntero se copian en esa actualización ($4 \\times 32$)."
                ),
                "expression": "4 * 32",
                "solution": {
                    "model": "Coste de actualización por Path Copying en vectores persistentes de ramificación 32",
                    "given": [
                        {"symbol": "d", "value": "4 niveles", "description": "Profundidad del trie para 32^4 = 1048576 elementos"},
                        {"symbol": "B", "value": "32 punteros", "description": "Factor de ramificación por nodo"},
                    ],
                    "steps": [
                        {"step": "Multiplicamos los 4 niveles modificados por las 32 ranuras de cada nodo", "equation": r"P_{\text{copiados}} = 4 \cdot 32", "expression": "4 * 32"},
                    ],
                    "conclusion": "Actualizar inmutablemente un vector de más de un millón de elementos copia únicamente 128 punteros, compartiendo el 99.99 % de la estructura.",
                },
            },
            "practice_problems": [
                {"prompt": "Un nodo de la máquina virtual BEAM ejecuta 25 000 procesos Elixir aislados, cada uno con un montículo inicial de 3 KiB. ¿Cuántos KiB suman en total esos 25 000 procesos?", "expression": "25000 * 3", "difficulty": "FOUNDATIONAL", "problem_type": "DIRECT_SUBSTITUTION"},
                {"prompt": "En el planificador preventivo de la BEAM, cada proceso dispone de un presupuesto de `2000` reducciones (llamadas a función) antes de ceder la CPU a otro proceso. Si un proceso ejecuta 14 000 llamadas a función, ¿cuántas rodajas de planificación (*context switches*) consume?", "expression": "14000 / 2000", "difficulty": "FOUNDATIONAL", "problem_type": "DIRECT_SUBSTITUTION"},
                {"prompt": "En un árbol persistente de Clojure con factor de ramificación 32, ¿cuántos elementos caben en $d = 3$ niveles ($32^3$)?", "expression": "32**3", "difficulty": "INTERMEDIATE", "problem_type": "MULTI_STEP"},
                {"prompt": "Un supervisor OTP configurado con estrategia `:one_for_all` supervisa 6 procesos trabajadores y uno de ellos falla. ¿Cuántos procesos trabajadores reinicia el supervisor?", "expression": "6", "difficulty": "INTERMEDIATE", "problem_type": "DESIGN"},
            ],
        },
        {
            "id": "cap07-monografias-julia-r-computacion-cientifica-estadistica",
            "title": "Monografías de Julia y R (Bloques A–H): Despacho Múltiple, Especialización JIT LLVM, Vectorización y Ciencia de Datos",
            "part_id": "parte-v-cientificos-embebidos-logicos",
            "part_title": "Monografías de Lenguajes Científicos, Embebidos y Lógicos (Julia, R, Lua, Perl, Objective-C, Prolog, GDScript)",
            "sources": ["src-ieee-754", "src-knuth-taocp"],
            "learning_objectives": [
                "Comprender cómo Julia resuelve el «problema de los dos lenguajes» mediante despacho múltiple (*multiple dispatch*), inferencia de estabilidad de tipos y compilación JIT sobre LLVM.",
                "Dominar en Julia los tipos paramétricos abstractos y concretos, la difusión vectorizada fusionada con punto (`f.(x) .+ g.(y)`), macros metaprogramáticas y álgebra lineal/ecuaciones diferenciales (`DifferentialEquations.jl`).",
                "Dominar R (4.x): vectores atómicos con semántica Copy-on-Modify, factores, matrices, `data.frame` / `tibble` / `data.table`, programación funcional (`purrr`), modelado estadístico (`y ~ x1 + x2`) y visualización con la Gramática de Gráficos (`ggplot2`).",
            ],
            "concepts": [
                {"id": "cpt-julia-multiple-dispatch-stability", "title": "Despacho múltiple simétrico en Julia, estabilidad de tipos (@code_warntype) y fusión de broadcasting con punto"},
                {"id": "cpt-r-vectorization-formulas", "title": "Operaciones vectorizadas en R, semántica Copy-on-Modify, fórmulas estadísticas y ecosistema Tidyverse/data.table"},
            ],
            "subsections": [
                {"id": "sec-v7-7-1", "title": "Monografía de Julia (Bloques A–H): Despacho múltiple, estabilidad de tipos, broadcasting fusionado y HPC"},
                {"id": "sec-v7-7-2", "title": "Monografía de R (Bloques A–H): Vectores, data frames, fórmulas estadísticas, Tidyverse/data.table y Quarto"},
            ],
            "purpose": (
                "Este capítulo desarrolla las monografías completas (Bloques A–H) de los dos lenguajes especializados en "
                "cálculo numérico, simulación física y estadística avanzada: **Julia** y **R**."
            ),
            "paragraphs": [
                {
                    "subsection": "sec-v7-7-1",
                    "text": (
                        "Creado en el MIT por Jeff Bezanson, Stefan Karpinski, Viral B. Shah y Alan Edelman, **Julia** fue diseñado "
                        "para eliminar el «problema de los dos lenguajes» (prototipar en un lenguaje dinámico lento y reescribir en C/Fortran "
                        "para producción). El núcleo semántico de Julia es el **despacho múltiple** (*multiple dispatch*): las funciones "
                        "genéricas seleccionan el método más específico considerando simultáneamente el tipo concreto de **todos** sus "
                        "argumentos, y cuando se invoca un método con una tupla de tipos concretos, el compilador JIT genera código "
                        "máquina LLVM especializado para esa firma exacta. La regla de oro del rendimiento en Julia es la **estabilidad "
                        "de tipos** (*type stability*, verificable con `@code_warntype`): el tipo del valor de retorno de una función "
                        "debe depender exclusivamente de los tipos de sus argumentos y nunca de sus valores en tiempo de ejecución. "
                        "Además, la sintaxis de difusión con punto `y .= a .* x .+ b` fusiona a nivel sintáctico múltiples operaciones "
                        "elementales en un único bucle SIMD en el sitio sin alojar ningún array temporal:\n"
                        "```julia\n"
                        "abstract type DissipationLaw end\n"
                        "struct LinearDrag <: DissipationLaw\n"
                        "    coeff::Float64\n"
                        "end\n\n"
                        "# Despacho múltiple especializado y bucle fusionado sin alojamientos (0 bytes):\n"
                        "function apply_damping!(v::AbstractVector{Float64}, law::LinearDrag, dt::Float64)\n"
                        "    @. v = v * (1.0 - law.coeff * dt)\n"
                        "    return v\n"
                        "end\n"
                        "```"
                    ),
                },
                {
                    "subsection": "sec-v7-7-2",
                    "text": (
                        "Por su parte, **R** (Ross Ihaka y Robert Gentleman, heredero del lenguaje S de John Chambers en Bell Labs) "
                        "es el estándar en bioestadística, econometría y ciencia de datos reproducible. En R no existen escalares "
                        "aislados: el número `42` es un vector numérico de longitud 1, todas las operaciones aritméticas están "
                        "vectorizadas en C/Fortran bajo el capó, los valores faltantes tipados `NA` (*Not Available*) son ciudadanos "
                        "de primera clase y los objetos siguen semántica funcional **Copy-on-Modify**. Asimismo, R posee evaluación "
                        "perezosa de argumentos mediante promesas (*Non-Standard Evaluation*, NSE) y un operador de fórmulas "
                        "simbólicas (`y ~ x1 + x2 + x1:x2`) que construye matrices de diseño para regresión lineal (`lm`), modelos "
                        "lineales generalizados (`glm`) y efectos mixtos."
                    ),
                },
            ],
            "definition": (
                "Estabilidad de Tipos (Type Stability en Julia): propiedad de un método según la cual el compilador puede "
                "inferir un único tipo concreto (no abstracto ni unión abierta `Any`) para su valor de retorno y todas sus "
                "variables internas a partir únicamente de los tipos de los argumentos de entrada."
            ),
            "consejo": (
                "En estructuras `struct` de Julia que van a participar en bucles numéricos intensivos, nunca declares campos "
                "con tipos abstractos (`x::Real` o `v::Vector{Number}`): parametriza siempre la estructura (`struct Particle{T<:Real} x::T end`) "
                "para que el compilador conozca el tamaño exacto del campo y lo aloje en línea sin punteros."
            ),
            "self_check": (
                "¿Por qué en Julia la función `f(x) = x > 0 ? x : 0.0` es inestable en tipos cuando se llama con un `Int64` "
                "(porque una rama devuelve `Int64` y la otra `Float64`), y cómo la corrige `zero(x)`?"
            ),
            "derivation": {
                "title": "Fusión sintáctica de broadcasting (Dot-Call Fusion) en Julia",
                "assumptions": ["Una expresión vectorizada de k operadores sobre vectores de N elementos Float64 (8 B) sin fusión aloja k vectores temporales; con @. e asignación en sitio (.=) aloja 0 bytes"],
                "steps": [
                    {"equation": r"M_{\text{unfused}} = k \cdot 8 N", "justification": "En lenguajes sin fusión de bucles, cada operador binario materializa un vector intermedio de 8*N bytes"},
                    {"equation": r"M_{\text{fused!}} = 0", "justification": "La macro @. reescribe la expresión como Broadcast.materialize! en un único bucle in-place"},
                ],
                "Verify": {"left": "k * 8 * N - 0", "right": "8 * k * N"},
            },
            "worked_problem": {
                "prompt": (
                    "Una expresión vectorial `w = a .* x .+ b .* y .- c` contiene $k = 4$ operaciones binarias sobre vectores "
                    "de $N = 1000000$ de elementos `Float64` ($8\\text{ B}$ cada uno). En un lenguaje sin fusión de expresiones, "
                    "evaluar los 4 operadores materializaría $4$ vectores temporales en memoria ($4 \\times 10^6 \\times 8\\text{ B}$). "
                    "En Julia, al escribir `@. w = a * x + b * y - c` sobre un vector preasignado `w`, la fusión sintáctica aloja "
                    "$0\\text{ B}$. Calcula cuántos megabytes exactos (dividiendo entre $10^6$) ahorra la fusión de Julia."
                ),
                "expression": "(4 * 1000000 * 8) / 1000000",
                "solution": {
                    "model": "Ahorro de asignaciones mediante Loop Fusion de broadcasting en Julia",
                    "given": [
                        {"symbol": "k", "value": "4 operaciones", "description": "Vectores temporales evitados"},
                        {"symbol": "N", "value": "1000000", "description": "Longitud de los vectores Float64"},
                        {"symbol": "S_f64", "value": "8 B", "description": "Tamaño de cada Float64"},
                    ],
                    "steps": [
                        {"step": "Multiplicamos 4 * 10^6 * 8 B y dividimos entre 10^6 B/MB", "equation": r"\Delta M_{\text{MB}} = \frac{4 \cdot 10^6 \cdot 8}{10^6}", "expression": "(4 * 1000000 * 8) / 1000000"},
                    ],
                    "conclusion": "La fusión sintáctica de Julia ahorra 32 MB de asignaciones temporales por evaluación y maximiza la localidad en caché L1/L2.",
                },
            },
            "practice_problems": [
                {"prompt": "En Julia, si una función genérica tiene 4 métodos especializados para el primer argumento y 4 para el segundo (todas las combinaciones de pares), ¿cuántos métodos especializados forman la tabla de despacho ($4 \\times 4$)?", "expression": "4 * 4", "difficulty": "FOUNDATIONAL", "problem_type": "DIRECT_SUBSTITUTION"},
                {"prompt": "En R, un `data.frame` tiene 12 columnas numéricas (`double` de 8 B) y 50 000 filas. ¿Cuántos bytes suman los datos de las 12 columnas ($12 \\times 50000 \\times 8$)?", "expression": "12 * 50000 * 8", "difficulty": "FOUNDATIONAL", "problem_type": "DIRECT_SUBSTITUTION"},
                {"prompt": "En un modelo lineal en R con intercepto y $p = 5$ predictores continuos más todas las interacciones de pares entre los 5 predictores ($5 \\times 4 / 2 = 10$), ¿cuántos coeficientes $\\beta$ estima en total `lm()` ($1 + 5 + 10$)?", "expression": "1 + 5 + 10", "difficulty": "INTERMEDIATE", "problem_type": "MULTI_STEP"},
                {"prompt": "Una validación cruzada de $K = 10$ pliegues (*10-fold CV*) repetida 5 veces evalúa una rejilla de 8 hiperparámetros. ¿Cuántos ajustes del modelo ejecuta en total ($10 \\times 5 \\times 8$)?", "expression": "10 * 5 * 8", "difficulty": "INTERMEDIATE", "problem_type": "DESIGN"},
            ],
        },
        {
            "id": "cap08-monografias-lua-perl-objc-prolog-gdscript",
            "title": "Monografías de Lua 5.4+, Perl 5, Objective-C, Prolog y GDScript (Bloques A–H): Scripting Embebido, Unificación Lógica y Motores",
            "part_id": "parte-v-cientificos-embebidos-logicos",
            "part_title": "Monografías de Lenguajes Científicos, Embebidos y Lógicos (Julia, R, Lua, Perl, Objective-C, Prolog, GDScript)",
            "sources": ["src-iso-c17", "src-knuth-taocp"],
            "learning_objectives": [
                "Dominar Lua (5.4+ / LuaJIT): máquina virtual basada en registros, tablas híbridas (array + hash), metatablas (`__index`, `__newindex`, `__add`), corrutinas asimétricas y la API de pila en C (`lua_State*`).",
                "Comprender Perl 5 (contexto escalar vs lista, expresiones regulares PCRE, CPAN, `use strict; use warnings;`) y Objective-C (paso de mensajes dinámico Smalltalk `objc_msgSend`, categorías y puente con Swift/C).",
                "Dominar Prolog (cláusulas de Horn, resolución SLD, unificación sintáctica de Robinson, retroceso y corte `!`) y GDScript (árbol de escenas de Godot, señales desacopladas y procesado por fotograma `_process`/`_physics_process`).",
            ],
            "concepts": [
                {"id": "cpt-lua-tables-metatables-capi", "title": "Tablas híbridas y metatablas en Lua 5.4, corrutinas cooperativas e integración embebida mediante lua_State"},
                {"id": "cpt-prolog-unification-gdscript", "title": "Unificación de términos y resolución SLD en Prolog, paso de mensajes en Objective-C y arquitectura de escenas en GDScript"},
            ],
            "subsections": [
                {"id": "sec-v7-8-1", "title": "Monografías de Lua 5.4+, Perl 5 y Objective-C (Bloques A–H): Tablas/Metatablas, Regex y objc_msgSend"},
                {"id": "sec-v7-8-2", "title": "Monografías de Prolog y GDScript (Bloques A–H): Unificación lógica (SLD) y programación de motores de videojuegos"},
            ],
            "purpose": (
                "Este capítulo cierra las monografías de lenguajes de la Parte V completando los Bloques A–H para **Lua**, "
                "**Perl**, **Objective-C**, **Prolog** y **GDScript**."
            ),
            "paragraphs": [
                {
                    "subsection": "sec-v7-8-1",
                    "text": (
                        "Diseñado en la PUC-Rio (Roberto Ierusalimschy, Waldemar Celes y Luiz Henrique de Figueiredo), **Lua** es "
                        "el lenguaje de scripting embebido por excelencia en motores de videojuegos, Redis, Nginx/OpenResty y Neovim: "
                        "todo su intérprete ANSI C ocupa menos de $300\\text{ KiB}$ y se ejecuta sobre una máquina virtual basada "
                        "en registros. La única estructura de datos compuesta de Lua es la **tabla**, implementada internamente "
                        "como una estructura híbrida que combina una parte de array denso (indexada desde `1`) y una parte de tabla "
                        "hash; asociando a una tabla una **metatabla** con metamétodos como `__index` y `__call`, se implementan "
                        "sistemas de objetos, proxies y sobrecarga de operadores:\n"
                        "```lua\n"
                        "local Vector2D = {}\n"
                        "Vector2D.__index = Vector2D\n\n"
                        "function Vector2D.new(x, y)\n"
                        "    return setmetatable({ x = x or 0, y = y or 0 }, Vector2D)\n"
                        "end\n\n"
                        "function Vector2D:magnitude_sq()\n"
                        "    return self.x * self.x + self.y * self.y\n"
                        "end\n"
                        "```\n"
                        "En **Perl 5** (Larry Wall), todo módulo moderno comienza con `use v5.36; use strict; use warnings;` y distingue "
                        "por sigilo e invocación entre contexto escalar (`$x`), lista (`@arr`) y tabla asociativa (`%hash`), habiendo "
                        "definido el estándar moderno de expresiones regulares (PCRE). En **Objective-C** (Brad Cox), las llamadas "
                        "`[receiver message:arg]` no se resuelven por desplazamiento de tabla virtual fija como en C++, sino mediante "
                        "el despachador dinámico en tiempo de ejecución `objc_msgSend(receiver, @selector(message:), arg)`, lo que "
                        "permite enviar mensajes a `nil` de forma segura (no-op que devuelve cero) e introspeccionar selectores dinámicamente."
                    ),
                },
                {
                    "subsection": "sec-v7-8-2",
                    "text": (
                        "En el paradigma lógico declarativo, un programa en **Prolog** (Alain Colmerauer y Philippe Roussel, 1972; "
                        "ISO Prolog / SWI-Prolog) consta de una base de conocimientos de **cláusulas de Horn**: hechos (`padre(juan, maria).`) "
                        "y reglas (`ancestro(X, Y) :- padre(X, Z), ancestro(Z, Y).`). Ante una consulta, el motor ejecuta **resolución "
                        "SLD** combinando el algoritmo de **unificación sintáctica de Robinson** (que calcula el unificador general "
                        "máximo, MGU, vinculando variables lógicas en ambos sentidos) con búsqueda en profundidad y retroceso "
                        "(*backtracking*) automático, además de aritmética con restricciones sobre dominios finitos (`use_module(library(clpfd))`). "
                        "Finalmente, **GDScript** (el lenguaje específico de dominio del motor libre **Godot Engine 4.x**) ofrece "
                        "tipado gradual estático (`var speed: float = 250.0`), referencias directas a nodos del árbol de escenas y "
                        "comunicación desacoplada mediante el patrón Observador con señales tipadas (`signal health_changed(new_hp: int)`), "
                        "separando estrictamente el bucle visual (`_process(delta)`) del paso fijo del motor de física (`_physics_process(delta)`)."
                    ),
                },
            ],
            "definition": (
                "Unificador General Máximo (Most General Unifier, MGU en Prolog): sustitución de variables $\\theta$ tal que, "
                "dados dos términos lógicos $s$ y $t$, los hace sintácticamente idénticos ($s\\theta = t\\theta$) y cualquier "
                "otro unificador $\\sigma$ de $s$ y $t$ es una instancia de $\\theta$ ($\\sigma = \\theta\\gamma$)."
            ),
            "consejo": (
                "En GDScript (Godot 4), añade anotaciones de tipos estáticos explícitas (`var vel: Vector2`, `func calc(x: float) -> float:`) "
                "en todos los scripts de física e inteligencia artificial: permite a la máquina virtual de Godot emitir opcodes "
                "tipados directos evitando la resolución dinámica de variantes en cada fotograma."
            ),
            "self_check": (
                "¿Qué diferencia fundamental existe entre la asignación destructiva `x = x + 1` de un lenguaje imperativo "
                "y la unificación `X = Y + 1` frente a la evaluación aritmética `X is Y + 1` en Prolog?"
            ),
            "derivation": {
                "title": "Integración cinemática independiente de la tasa de fotogramas mediante delta time en GDScript",
                "assumptions": ["En un motor de juego que avanza con paso temporal delta = 1 / FPS segundos por fotograma a velocidad v constante"],
                "steps": [
                    {"equation": r"\Delta x_{\text{frame}} = v \cdot \Delta t = \frac{v}{\text{FPS}}", "justification": "Desplazamiento por fotograma proporcional a delta"},
                    {"equation": r"X_{\text{1s}} = \text{FPS} \cdot \left(\frac{v}{\text{FPS}}\right) = v", "justification": "El desplazamiento acumulado tras 1 segundo es exactamente v píxeles/metros sin importar si FPS es 30, 60 o 144"},
                ],
                "Verify": {"left": "FPS * (v / FPS)", "right": "v"},
            },
            "worked_problem": {
                "prompt": (
                    "En la implementación C de las tablas híbridas de Lua 5.4, cuando una tabla almacena claves enteras "
                    "consecutivas `1..N`, se alojan en la parte array (`TValue` de $16\\text{ B}$ por elemento: 8 B de valor "
                    "más 1 B de etiqueta alineado), mientras que en la parte hash cada nodo (`Node`) ocupa $32\\text{ B}$ "
                    "(clave + valor + enlace `next`). Calcula cuántos bytes ahorra una tabla Lua de $N = 4000$ elementos al "
                    "indexarse secuencialmente desde `1` hasta `4000` (parte array de $16\\text{ B}$) frente a usar claves "
                    "dispersas en la parte hash ($32\\text{ B}$ por nodo)."
                ),
                "expression": "4000 * (32 - 16)",
                "solution": {
                    "model": "Ahorro de memoria de la parte Array frente a la parte Hash en tablas híbridas de Lua 5.4",
                    "given": [
                        {"symbol": "N", "value": "4000", "description": "Elementos en la tabla Lua"},
                        {"symbol": "S_hash", "value": "32 B", "description": "Tamaño por nodo en la parte hash"},
                        {"symbol": "S_array", "value": "16 B", "description": "Tamaño por TValue en la parte array"},
                    ],
                    "steps": [
                        {"step": "Multiplicamos los 4000 elementos por los 16 B ahorrados al residir en la parte array", "equation": r"\Delta M = 4000 \cdot (32 - 16)", "expression": "4000 * (32 - 16)"},
                    ],
                    "conclusion": "Usar índices enteros consecutivos desde 1 ahorra 64 000 bytes (la mitad exacta de memoria) y evita el cálculo de hashes.",
                },
            },
            "practice_problems": [
                {"prompt": "En el ejemplo de Lua `Vector2D.new(6, 8):magnitude_sq()`, ¿qué valor devuelve $6^2 + 8^2$?", "expression": "6 * 6 + 8 * 8", "difficulty": "FOUNDATIONAL", "problem_type": "DIRECT_SUBSTITUTION"},
                {"prompt": "En Godot Engine (GDScript), el bucle `_physics_process(delta)` se ejecuta por defecto a una frecuencia fija de 60 tics por segundo. ¿Cuántos pasos de física ejecuta exactamente en 15 segundos ($60 \\times 15$)?", "expression": "60 * 15", "difficulty": "FOUNDATIONAL", "problem_type": "DIRECT_SUBSTITUTION"},
                {"prompt": "Un predicado no determinista en Prolog tiene 3 cláusulas que se ramifican en profundidad $d = 4$ niveles ($3^4$ hojas en el árbol de búsqueda SLD). Si el operador de corte `!` poda 2 de las 3 ramas en la raíz, ¿cuántas hojas se ahorra explorar ($3^4 - 3^3$)?", "expression": "3**4 - 3**3", "difficulty": "INTERMEDIATE", "problem_type": "MULTI_STEP"},
                {"prompt": "En la API de pila en C de Lua (`lua_State`), una función nativa empuja 5 argumentos a la pila, invoca `lua_pcall(L, 4, 2, 0)` (que consume la función más los 4 argumentos y empuja 2 resultados). Si antes de empezar había 3 elementos en la pila, ¿cuántos elementos hay en la pila al terminar ($3 + 2$)?", "expression": "3 + 2", "difficulty": "INTERMEDIATE", "problem_type": "DESIGN"},
            ],
        },
    ],
}


def main() -> None:
    s6 = build_studium_volume(VOL06_SPEC)
    s7 = build_studium_volume(VOL07_SPEC)
    report_path = ROOT / "reports" / "vol06-vol07-build.json"
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(json.dumps([s6, s7], indent=2, ensure_ascii=False), encoding="utf-8")


if __name__ == "__main__":
    main()
