"""Programming exercises of volume 6 (C#, Java, Go, Kotlin, Swift). Each reference program runs with the real toolchain."""

EXERCISES = [
    # ---- capítulo 1: C# y .NET
    dict(ch=1, lang='csharp', level='FOUNDATIONAL',
         prompt='Define `readonly record struct Point3D(double X, double Y, double Z)` con el método `double DistanceTo(Point3D other)`. Comprueba la distancia entre `(0, 0, 0)` y `(1, 2, 2)` (3), la igualdad por valor y que `with` crea una copia modificada sin cambiar la original.',
         code='''readonly record struct Point3D(double X, double Y, double Z)
{
    public double DistanceTo(Point3D other)
    {
        double dx = X - other.X, dy = Y - other.Y, dz = Z - other.Z;
        return Math.Sqrt(dx * dx + dy * dy + dz * dz);
    }
}''',
         harness='''var origin = new Point3D(0, 0, 0);
var p = new Point3D(1, 2, 2);
if (Math.Abs(origin.DistanceTo(p) - 3.0) > 1e-12) return 1;
if (p != new Point3D(1, 2, 2)) return 2;
var moved = p with { X = 10 };
if (p.X != 1 || moved.X != 10 || moved.Y != 2) return 3;
if (p.Equals(moved)) return 4;
Console.WriteLine("OK");
return 0;

{{code}}''',
         tests=['la distancia de `(0,0,0)` a `(1,2,2)` es 3', 'dos puntos con las mismas coordenadas son iguales', '`with` no modifica el original', 'puntos distintos no son iguales'],
         why='Un `record struct` es un tipo valor con igualdad por componentes y sintaxis `with` para copias modificadas. `readonly` impide mutarlo y permite al compilador evitar copias defensivas. Como tipo valor, no tiene cabecera de objeto ni asignación en el montículo cuando va en una variable local.'),
    dict(ch=1, lang='csharp', level='INTERMEDIATE',
         prompt='Escribe `static IEnumerable<int> FirstEvenSquares(IEnumerable<int> source, int count)` con LINQ (`Where`, `Select`, `Take`). Debe ser perezosa: con `count = 3` sobre una secuencia infinita debe terminar, y no debe examinar más elementos de los necesarios. Comprueba el resultado y cuántos elementos se examinaron.',
         code='''static IEnumerable<int> FirstEvenSquares(IEnumerable<int> source, int count) =>
    source.Where(n => n % 2 == 0).Select(n => n * n).Take(count);''',
         harness='''int inspected = 0;
IEnumerable<int> Naturals()
{
    for (int i = 1; ; i++) { inspected++; yield return i; }
}
var result = FirstEvenSquares(Naturals(), 3).ToList();
if (!result.SequenceEqual(new[] { 4, 16, 36 })) return 1;
if (inspected != 6) return 2;
if (FirstEvenSquares(new[] { 1, 3, 5 }, 2).Any()) return 3;
Console.WriteLine("OK");
return 0;

{{code}}''',
         tests=['los tres primeros pares al cuadrado son `4, 16, 36`', 'sobre una secuencia infinita termina', 'solo se examinan los 6 primeros números', 'sin pares el resultado es vacío'],
         why='Las consultas LINQ se ejecutan de forma diferida: no hacen nada hasta que se enumera el resultado, y `Take` detiene el recorrido tras el último elemento pedido. En C# el recorrido se detiene sin leer el siguiente elemento, por lo que se examinan exactamente seis números.'),
    dict(ch=1, lang='csharp', kind='debugging', level='INTERMEDIATE',
         prompt='Depuración. Este método intenta incrementar un contador de un `struct`, pero el original no cambia porque se pasa una copia:\n\n```csharp\nstruct Counter { public int Value; }\nstatic void Increment(Counter c) { c.Value++; }\n```\n\nCorrígelo con un parámetro `ref` (`IncrementStruct`) y escribe la versión para `class` (`IncrementBox`); comprueba que el valor del original aumenta. Comprueba también que, con una `class`, el mismo método sin `ref` sí modifica el original, y explica la diferencia.',
         code='''static void IncrementStruct(ref Counter c) => c.Value++;
static void IncrementBox(CounterBox c) => c.Value++;

struct Counter { public int Value; }
class CounterBox { public int Value; }''',
         harness='''var s = new Counter();
IncrementStruct(ref s);
IncrementStruct(ref s);
if (s.Value != 2) return 1;
var box = new CounterBox();
IncrementBox(box);
if (box.Value != 1) return 2;
var copy = s;
copy.Value = 99;
if (s.Value != 2) return 3;
var alias = box;
alias.Value = 99;
if (box.Value != 99) return 4;
Console.WriteLine("OK");
return 0;

{{code}}''',
         tests=['con `ref`, el `struct` original aumenta a 2', 'con una `class`, el método modifica el objeto original', 'copiar un `struct` crea un valor independiente', 'copiar una referencia a una `class` comparte el objeto'],
         why='Un tipo valor se copia al asignarlo o pasarlo, así que el método modificaba su copia. `ref` pasa una referencia a la variable original. Un tipo referencia pasa la referencia por valor: el método y quien llama comparten el mismo objeto.'),
    # ---- capítulo 2: C# avanzado
    dict(ch=2, lang='csharp', level='INTERMEDIATE',
         prompt='Escribe `static int SumSlice(Span<int> data, int start, int length)` que sume un fragmento de `data` sin copiar ni reservar memoria, usando `Slice`. Comprueba con un array, con `stackalloc` y con fragmentos vacíos.',
         code='''static int SumSlice(Span<int> data, int start, int length)
{
    int total = 0;
    foreach (int value in data.Slice(start, length))
    {
        total += value;
    }
    return total;
}''',
         harness='''int[] array = { 1, 2, 3, 4, 5 };
if (SumSlice(array, 1, 3) != 9) return 1;
Span<int> stack = stackalloc int[4];
for (int i = 0; i < stack.Length; i++) stack[i] = i + 10;
if (SumSlice(stack, 0, 4) != 46) return 2;
if (SumSlice(array, 2, 0) != 0) return 3;
SumSlice(array, 1, 2);
try { SumSlice(array, 4, 3); return 4; } catch (ArgumentOutOfRangeException) { }
Console.WriteLine("OK");
return 0;

{{code}}''',
         tests=['`array[1..4]` suma 9', 'funciona con memoria de la pila (`stackalloc`)', 'un fragmento vacío suma 0', 'un rango fuera de límites lanza `ArgumentOutOfRangeException`'],
         why='`Span<T>` es una vista sobre memoria contigua, sea un array, la pila o memoria nativa, y `Slice` crea otra vista sin copiar. Al ser un tipo `ref struct` solo puede vivir en la pila, lo que evita que sobreviva a la memoria que mira.'),
    dict(ch=2, lang='csharp', level='INTERMEDIATE',
         prompt='Escribe `static async Task<int[]> SquaresAsync(int[] values)` que calcule cada cuadrado en una tarea con un retraso de 100 ms (`await Task.Delay`) y espere a todas con `Task.WhenAll`. Las tareas deben ejecutarse a la vez: con 5 valores el total debe ser mucho menor que 500 ms. Comprueba el orden y el tiempo.',
         code='''static async Task<int[]> SquaresAsync(int[] values)
{
    async Task<int> Square(int v)
    {
        await Task.Delay(100);
        return v * v;
    }
    return await Task.WhenAll(values.Select(Square));
}''',
         harness='''var watch = System.Diagnostics.Stopwatch.StartNew();
var result = await SquaresAsync(new[] { 1, 2, 3, 4, 5 });
watch.Stop();
if (!result.SequenceEqual(new[] { 1, 4, 9, 16, 25 })) return 1;
if (watch.ElapsedMilliseconds > 400) return 2;
if ((await SquaresAsync(Array.Empty<int>())).Length != 0) return 3;
Console.WriteLine("OK");
return 0;

{{code}}''',
         tests=['el resultado conserva el orden de la entrada', 'cinco esperas de 100 ms tardan menos de 400 ms', 'una entrada vacía devuelve un array vacío'],
         why='`Select` crea todas las tareas antes de esperar a ninguna; `WhenAll` espera a todas y conserva el orden de los argumentos. Con `await` seguido de otro `await` por cada elemento, las esperas se encadenarían y tardarían 500 ms.'),
    dict(ch=2, lang='csharp', level='ADVANCED',
         prompt='Escribe `static async Task<List<int>> PipelineAsync(int count)` que cree un `Channel<int>` acotado a capacidad 2, con un productor que escriba `1..count` (esperando si el canal está lleno) y un consumidor que lea todo hasta que se cierre y devuelva la lista. Comprueba `count = 10` y `count = 0`.',
         code='''// Requiere: using System.Threading.Channels;
static async Task<List<int>> PipelineAsync(int count)
{
    var channel = Channel.CreateBounded<int>(2);
    var producer = Task.Run(async () =>
    {
        for (int i = 1; i <= count; i++)
        {
            await channel.Writer.WriteAsync(i);
        }
        channel.Writer.Complete();
    });
    var result = new List<int>();
    await foreach (int item in channel.Reader.ReadAllAsync())
    {
        result.Add(item);
    }
    await producer;
    return result;
}''',
         harness='''using System.Threading.Channels;

if (!(await PipelineAsync(10)).SequenceEqual(Enumerable.Range(1, 10))) return 1;
if ((await PipelineAsync(0)).Count != 0) return 2;
if ((await PipelineAsync(1000)).Count != 1000) return 3;
Console.WriteLine("OK");
return 0;

{{code}}''',
         tests=['`count = 10` devuelve `1..10` en orden', '`count = 0` devuelve una lista vacía', '`count = 1000` entrega los 1000 elementos con un canal de capacidad 2'],
         why='Un canal acotado aplica contrapresión: cuando está lleno, `WriteAsync` espera hasta que el consumidor lea. `Complete` avisa al lector de que no habrá más datos, y `ReadAllAsync` termina entonces. Sin él el consumidor esperaría para siempre.'),
    # ---- capítulo 3: Java
    dict(ch=3, lang='java', level='INTERMEDIATE',
         prompt='Define la jerarquía sellada `Expr` con `Num(double)`, `Add(Expr, Expr)` y `Mul(Expr, Expr)` como `record`, y `static double eval(Expr e)` con `switch` de patrones sin rama `default`. Comprueba `(2 + 3) * 4 = 20`.',
         code='''sealed interface Expr permits Num, Add, Mul {}
record Num(double value) implements Expr {}
record Add(Expr left, Expr right) implements Expr {}
record Mul(Expr left, Expr right) implements Expr {}

static double eval(Expr e) {
    return switch (e) {
        case Num n -> n.value();
        case Add a -> eval(a.left()) + eval(a.right());
        case Mul m -> eval(m.left()) * eval(m.right());
    };
}''',
         harness='''public class Main {
    {{code}}

    public static void main(String[] args) {
        Expr e = new Mul(new Add(new Num(2), new Num(3)), new Num(4));
        if (eval(e) != 20.0) throw new AssertionError("20");
        if (eval(new Num(-1.5)) != -1.5) throw new AssertionError("num");
        if (eval(new Add(new Num(0), new Mul(new Num(2), new Num(2)))) != 4.0) throw new AssertionError("anidado");
        System.out.println("OK");
    }
}''',
         tests=['`(2 + 3) * 4` vale 20', 'un número vale él mismo', 'las expresiones anidadas se evalúan en profundidad'],
         why='`sealed` enumera todas las implementaciones posibles, de modo que el `switch` de patrones es exhaustivo sin `default`. Si se añade una variante, el compilador señala cada `switch` que falta por actualizar. Los `record` dan constructor, acceso y igualdad por componentes sin código repetitivo.'),
    dict(ch=3, lang='java', level='INTERMEDIATE',
         prompt='Escribe un método con esta firma:\n\n```java\nstatic Map<Integer, List<String>> groupByLength(List<String> words)\n```\n\nUsa `Collectors.groupingBy` para que agrupe las palabras por longitud, en un `TreeMap` para que el orden sea determinista y conservando el orden de aparición dentro de cada grupo. Comprueba con `["a", "bb", "c", "dd", "eee"]`.',
         code='''static Map<Integer, List<String>> groupByLength(List<String> words) {
    return words.stream().collect(Collectors.groupingBy(String::length, TreeMap::new, Collectors.toList()));
}''',
         harness='''import java.util.*;
import java.util.stream.*;

public class Main {
    {{code}}

    public static void main(String[] args) {
        Map<Integer, List<String>> grouped = groupByLength(List.of("a", "bb", "c", "dd", "eee"));
        if (!grouped.equals(Map.of(1, List.of("a", "c"), 2, List.of("bb", "dd"), 3, List.of("eee")))) throw new AssertionError("grupos");
        if (!new ArrayList<>(grouped.keySet()).equals(List.of(1, 2, 3))) throw new AssertionError("orden");
        if (!groupByLength(List.of()).isEmpty()) throw new AssertionError("vacio");
        System.out.println("OK");
    }
}''',
         tests=['`["a","bb","c","dd","eee"]` se agrupa por longitud 1, 2 y 3', 'las claves salen ordenadas', 'dentro de cada grupo se conserva el orden', 'la lista vacía da un mapa vacío'],
         why='`groupingBy` recibe la función de clasificación, la fábrica del mapa y el colector de cada grupo. Pasar `TreeMap::new` evita depender del orden de un `HashMap`, que no está garantizado.'),
    dict(ch=3, lang='java', level='FOUNDATIONAL',
         prompt='Escribe `static <T extends Comparable<T>> T maxOf(List<T> items)` que devuelva el mayor elemento y lance `NoSuchElementException` si la lista está vacía. Comprueba con enteros y con cadenas.',
         code='''static <T extends Comparable<T>> T maxOf(List<T> items) {
    if (items.isEmpty()) {
        throw new NoSuchElementException("lista vacia");
    }
    T best = items.get(0);
    for (T item : items) {
        if (item.compareTo(best) > 0) {
            best = item;
        }
    }
    return best;
}''',
         harness='''import java.util.*;

public class Main {
    {{code}}

    public static void main(String[] args) {
        if (maxOf(List.of(3, 9, 4)) != 9) throw new AssertionError("enteros");
        if (!maxOf(List.of("pera", "manzana", "uva")).equals("uva")) throw new AssertionError("cadenas");
        if (maxOf(List.of(5)) != 5) throw new AssertionError("uno");
        try {
            maxOf(new ArrayList<Integer>());
            throw new AssertionError("debe lanzar");
        } catch (NoSuchElementException expected) {
        }
        System.out.println("OK");
    }
}''',
         tests=['`[3, 9, 4]` devuelve 9', 'con cadenas devuelve la mayor por orden alfabético', 'una lista de un elemento lo devuelve', 'una lista vacía lanza `NoSuchElementException`'],
         why='El límite `T extends Comparable<T>` garantiza que `compareTo` existe y se puede llamar. Java borra los tipos genéricos en tiempo de ejecución: el límite se comprueba en compilación y el código generado es uno solo para todos los tipos.'),
    # ---- capítulo 4: Java avanzado
    dict(ch=4, lang='java', level='INTERMEDIATE',
         prompt='Escribe `static long sumWithVirtualThreads(int tasks)` que lance `tasks` hilos virtuales con `Executors.newVirtualThreadPerTaskExecutor()`, cada uno devolviendo su índice, y sume los resultados con `Future.get`. Comprueba `tasks = 1000` (suma 499500) y `tasks = 0`.',
         code='''static long sumWithVirtualThreads(int tasks) throws Exception {
    try (var executor = Executors.newVirtualThreadPerTaskExecutor()) {
        List<Future<Integer>> futures = new ArrayList<>();
        for (int i = 0; i < tasks; i++) {
            final int index = i;
            futures.add(executor.submit(() -> index));
        }
        long total = 0;
        for (Future<Integer> future : futures) {
            total += future.get();
        }
        return total;
    }
}''',
         harness='''import java.util.*;
import java.util.concurrent.*;

public class Main {
    {{code}}

    public static void main(String[] args) throws Exception {
        if (sumWithVirtualThreads(1000) != 499500L) throw new AssertionError("1000");
        if (sumWithVirtualThreads(0) != 0L) throw new AssertionError("0");
        if (sumWithVirtualThreads(10_000) != 49_995_000L) throw new AssertionError("10000");
        System.out.println("OK");
    }
}''',
         tests=['1000 tareas suman 499 500', '0 tareas suman 0', '10 000 hilos virtuales suman 49 995 000'],
         why='Un hilo virtual es muy barato: miles pueden convivir sobre pocos hilos del sistema, y se suspenden sin bloquear el hilo portador cuando esperan. El `try` con recursos cierra el ejecutor y espera a que terminen todas las tareas.'),
    dict(ch=4, lang='java', level='INTERMEDIATE',
         prompt='Escribe un método con esta firma:\n\n```java\nstatic Map<String, Integer> parallelCount(List<String> words, int threads)\n```\n\nQue cuente las palabras desde varios hilos usando un `ConcurrentHashMap` y `merge`, sin sincronizar a mano. Comprueba con 4 hilos y una lista grande: el resultado debe ser exacto.',
         code='''static Map<String, Integer> parallelCount(List<String> words, int threads) throws Exception {
    ConcurrentHashMap<String, Integer> counts = new ConcurrentHashMap<>();
    ExecutorService pool = Executors.newFixedThreadPool(threads);
    int chunk = Math.max(1, (words.size() + threads - 1) / threads);
    List<Future<?>> futures = new ArrayList<>();
    for (int start = 0; start < words.size(); start += chunk) {
        List<String> part = words.subList(start, Math.min(words.size(), start + chunk));
        futures.add(pool.submit(() -> part.forEach(w -> counts.merge(w, 1, Integer::sum))));
    }
    for (Future<?> f : futures) {
        f.get();
    }
    pool.shutdown();
    return counts;
}''',
         harness='''import java.util.*;
import java.util.concurrent.*;

public class Main {
    {{code}}

    public static void main(String[] args) throws Exception {
        List<String> words = new ArrayList<>();
        for (int i = 0; i < 40_000; i++) {
            words.add(i % 4 == 0 ? "a" : (i % 4 == 1 ? "b" : "c"));
        }
        Map<String, Integer> counts = parallelCount(words, 4);
        if (counts.get("a") != 10_000 || counts.get("b") != 10_000 || counts.get("c") != 20_000) throw new AssertionError("conteo");
        if (!parallelCount(List.of(), 3).isEmpty()) throw new AssertionError("vacio");
        System.out.println("OK");
    }
}''',
         tests=['40 000 palabras en 4 hilos dan `a=10000, b=10000, c=20000`', 'una lista vacía da un mapa vacío'],
         why='`merge` hace la lectura, la suma y la escritura de forma atómica por clave, de modo que dos hilos no pierden un incremento. Con un `HashMap` normal el resultado sería incorrecto o el programa podría fallar.'),
    dict(ch=4, lang='java', level='ADVANCED',
         prompt='Escribe `static long incrementWithAdder(int threads, int perThread)` que use un `LongAdder` compartido y `threads` hilos que lo incrementen `perThread` veces cada uno, y devuelva `sum()`. Explica por qué `LongAdder` escala mejor que `AtomicLong` con mucha contención. Comprueba 8 hilos con 50 000 incrementos.',
         code='''static long incrementWithAdder(int threads, int perThread) throws InterruptedException {
    LongAdder adder = new LongAdder();
    List<Thread> list = new ArrayList<>();
    for (int t = 0; t < threads; t++) {
        Thread thread = new Thread(() -> {
            for (int i = 0; i < perThread; i++) {
                adder.increment();
            }
        });
        list.add(thread);
        thread.start();
    }
    for (Thread thread : list) {
        thread.join();
    }
    return adder.sum();
}''',
         harness='''import java.util.*;
import java.util.concurrent.atomic.LongAdder;

public class Main {
    {{code}}

    public static void main(String[] args) throws Exception {
        if (incrementWithAdder(8, 50_000) != 400_000L) throw new AssertionError("8x50000");
        if (incrementWithAdder(1, 3) != 3L) throw new AssertionError("1x3");
        if (incrementWithAdder(0, 3) != 0L) throw new AssertionError("0x3");
        System.out.println("OK");
    }
}''',
         tests=['8 hilos con 50 000 incrementos dan 400 000', '1 hilo con 3 da 3', '0 hilos dan 0'],
         why='`LongAdder` reparte los incrementos entre varias celdas y las suma en `sum()`, de modo que los hilos no compiten por una única posición de memoria. `thread.join()` establece una relación happens-before: tras él, `sum()` ve todos los incrementos.'),
    # ---- capítulo 5: Go
    dict(ch=5, lang='go', level='FOUNDATIONAL',
         prompt='Escribe `func Chunk(items []int, size int) [][]int` que divida un slice en trozos de longitud `size` (el último puede ser menor) devolviendo subslices del original, sin copiar. Si `size < 1` debe devolver `nil`. Comprueba el resultado y que los trozos comparten memoria con el original.',
         code='''func Chunk(items []int, size int) [][]int {
	if size < 1 {
		return nil
	}
	var out [][]int
	for start := 0; start < len(items); start += size {
		end := start + size
		if end > len(items) {
			end = len(items)
		}
		out = append(out, items[start:end:end])
	}
	return out
}''',
         harness='''package main

import (
	"fmt"
	"reflect"
)

{{code}}

func main() {
	data := []int{1, 2, 3, 4, 5}
	got := Chunk(data, 2)
	if !reflect.DeepEqual(got, [][]int{{1, 2}, {3, 4}, {5}}) {
		panic("chunks")
	}
	got[0][0] = 99
	if data[0] != 99 {
		panic("comparten memoria")
	}
	if Chunk(data, 0) != nil || len(Chunk(nil, 3)) != 0 {
		panic("bordes")
	}
	fmt.Println("OK")
}''',
         tests=['`[1,2,3,4,5]` con tamaño 2 da `[[1,2],[3,4],[5]]`', 'los trozos comparten memoria con el original', '`size = 0` devuelve `nil`', 'un slice vacío da cero trozos'],
         why='Un slice es un descriptor con puntero, longitud y capacidad; `items[start:end:end]` crea otro sobre el mismo array. Limitar la capacidad con la tercera cota evita que un `append` sobre un trozo pise los datos del siguiente.'),
    dict(ch=5, lang='go', level='INTERMEDIATE',
         prompt='Define la interfaz `Shape` con `Area() float64` y dos tipos que la implementen, `Circle{R}` y `Rect{W, H}`. Escribe `func TotalArea(shapes []Shape) float64`. Comprueba la suma de áreas y que un tipo que no implementa la interfaz no puede añadirse (se comprueba en compilación con una aserción de interfaz).',
         code='''type Shape interface {
	Area() float64
}

type Circle struct{ R float64 }
type Rect struct{ W, H float64 }

func (c Circle) Area() float64 { return math.Pi * c.R * c.R }
func (r Rect) Area() float64   { return r.W * r.H }

var (
	_ Shape = Circle{}
	_ Shape = Rect{}
)

func TotalArea(shapes []Shape) float64 {
	total := 0.0
	for _, s := range shapes {
		total += s.Area()
	}
	return total
}''',
         harness='''package main

import (
	"fmt"
	"math"
)

{{code}}

func main() {
	got := TotalArea([]Shape{Circle{1}, Rect{3, 4}})
	if math.Abs(got-(math.Pi+12)) > 1e-12 {
		panic("total")
	}
	if TotalArea(nil) != 0 {
		panic("vacio")
	}
	fmt.Println("OK")
}''',
         tests=['un círculo de radio 1 y un rectángulo 3 por 4 suman `PI + 12`', 'una lista vacía suma 0'],
         why='En Go las interfaces se satisfacen implícitamente: basta con tener los métodos. Las declaraciones `var _ Shape = Circle{}` fallan al compilar si el tipo deja de cumplir la interfaz, lo que documenta la intención.'),
    dict(ch=5, lang='go', level='INTERMEDIATE',
         prompt='Define `var ErrEmpty = errors.New("vacío")` y `func ParseAge(s string) (int, error)` que devuelva el error `ErrEmpty` (envuelto con `%w` y el texto recibido) si la cadena está vacía, y un error de `strconv` envuelto si no es un número. Comprueba con `errors.Is` y `errors.As`.',
         code='''var ErrEmpty = errors.New("vacio")

func ParseAge(s string) (int, error) {
	if s == "" {
		return 0, fmt.Errorf("parse age %q: %w", s, ErrEmpty)
	}
	n, err := strconv.Atoi(s)
	if err != nil {
		return 0, fmt.Errorf("parse age %q: %w", s, err)
	}
	return n, nil
}''',
         harness='''package main

import (
	"errors"
	"fmt"
	"strconv"
)

{{code}}

func main() {
	if n, err := ParseAge("42"); n != 42 || err != nil {
		panic("valido")
	}
	_, err := ParseAge("")
	if !errors.Is(err, ErrEmpty) {
		panic("vacio")
	}
	_, err = ParseAge("abc")
	var numErr *strconv.NumError
	if !errors.As(err, &numErr) || numErr.Func != "Atoi" || errors.Is(err, ErrEmpty) {
		panic("no numerico")
	}
	fmt.Println("OK")
}''',
         tests=['`"42"` devuelve 42 sin error', 'la cadena vacía devuelve un error que cumple `errors.Is(err, ErrEmpty)`', '`"abc"` devuelve un error del que se puede extraer `*strconv.NumError`'],
         why='`%w` envuelve el error original conservando la cadena de causas. `errors.Is` compara con un valor centinela recorriendo esa cadena y `errors.As` extrae un error de un tipo concreto, de modo que quien llama decide sin analizar el texto del mensaje.'),
    # ---- capítulo 6: Go concurrente
    dict(ch=6, lang='go', level='INTERMEDIATE',
         prompt='Escribe `func SquareAll(nums []int, workers int) []int` que reparta el trabajo entre `workers` goroutines con un canal de tareas y devuelva los cuadrados en el mismo orden que la entrada. Comprueba con 1, 4 y 50 trabajadores y con la lista vacía.',
         code='''func SquareAll(nums []int, workers int) []int {
	if workers < 1 {
		workers = 1
	}
	out := make([]int, len(nums))
	jobs := make(chan int)
	var wg sync.WaitGroup
	for w := 0; w < workers; w++ {
		wg.Add(1)
		go func() {
			defer wg.Done()
			for i := range jobs {
				out[i] = nums[i] * nums[i]
			}
		}()
	}
	for i := range nums {
		jobs <- i
	}
	close(jobs)
	wg.Wait()
	return out
}''',
         harness='''package main

import (
	"fmt"
	"reflect"
	"sync"
)

{{code}}

func main() {
	in := []int{1, 2, 3, 4, 5, 6, 7, 8}
	want := []int{1, 4, 9, 16, 25, 36, 49, 64}
	for _, w := range []int{1, 4, 50} {
		if !reflect.DeepEqual(SquareAll(in, w), want) {
			panic("orden")
		}
	}
	if len(SquareAll(nil, 3)) != 0 {
		panic("vacio")
	}
	fmt.Println("OK")
}''',
         tests=['con 1, 4 y 50 trabajadores el resultado es el mismo y está ordenado', 'una lista vacía devuelve una lista vacía'],
         why='Cada tarea es un índice, y cada goroutine escribe solo en su posición, así que no hay carreras de datos aunque compartan el slice de salida. Cerrar el canal indica a los trabajadores que no habrá más tareas, y `WaitGroup` espera a que acaben.'),
    dict(ch=6, lang='go', level='INTERMEDIATE',
         prompt='Escribe una función con esta firma:\n\n```go\nfunc CountConcurrently(goroutines, perGoroutine int) int\n```\n\nQue use `sync.Mutex` para que varias goroutines incrementen un contador compartido sin perder ninguna actualización. Comprueba 8 goroutines con 10 000 incrementos.',
         code='''func CountConcurrently(goroutines, perGoroutine int) int {
	var mu sync.Mutex
	var wg sync.WaitGroup
	counter := 0
	for g := 0; g < goroutines; g++ {
		wg.Add(1)
		go func() {
			defer wg.Done()
			for i := 0; i < perGoroutine; i++ {
				mu.Lock()
				counter++
				mu.Unlock()
			}
		}()
	}
	wg.Wait()
	return counter
}''',
         harness='''package main

import (
	"fmt"
	"sync"
)

{{code}}

func main() {
	if CountConcurrently(8, 10000) != 80000 {
		panic("8x10000")
	}
	if CountConcurrently(1, 5) != 5 || CountConcurrently(0, 5) != 0 {
		panic("bordes")
	}
	fmt.Println("OK")
}''',
         tests=['8 goroutines con 10 000 incrementos dan 80 000', '1 goroutine con 5 da 5', '0 goroutines dan 0'],
         why='`counter++` no es atómico, así que sin el cerrojo dos goroutines pueden leer el mismo valor y perder un incremento. `wg.Wait()` garantiza que todas han terminado antes de leer el contador.'),
    dict(ch=6, lang='go', level='ADVANCED',
         prompt='Escribe `func Slow(ctx context.Context, d time.Duration) error` que espere `d` o hasta que `ctx` se cancele, devolviendo `ctx.Err()` en ese caso. Comprueba con un contexto con plazo de 50 ms: una espera de 10 ms termina bien y una de 2 s devuelve `context.DeadlineExceeded` mucho antes de los 2 s.',
         code='''func Slow(ctx context.Context, d time.Duration) error {
	timer := time.NewTimer(d)
	defer timer.Stop()
	select {
	case <-timer.C:
		return nil
	case <-ctx.Done():
		return ctx.Err()
	}
}''',
         harness='''package main

import (
	"context"
	"errors"
	"fmt"
	"time"
)

{{code}}

func main() {
	ctx, cancel := context.WithTimeout(context.Background(), 50*time.Millisecond)
	defer cancel()
	if err := Slow(ctx, 10*time.Millisecond); err != nil {
		panic("corta")
	}
	start := time.Now()
	err := Slow(ctx, 2*time.Second)
	if !errors.Is(err, context.DeadlineExceeded) || time.Since(start) > 500*time.Millisecond {
		panic("larga")
	}
	cancelled, stop := context.WithCancel(context.Background())
	stop()
	if !errors.Is(Slow(cancelled, time.Second), context.Canceled) {
		panic("cancelado")
	}
	fmt.Println("OK")
}''',
         tests=['una espera de 10 ms con plazo de 50 ms termina sin error', 'una espera de 2 s devuelve `DeadlineExceeded` en menos de 0,5 s', 'un contexto cancelado devuelve `Canceled`'],
         why='`select` espera a la primera de varias operaciones de canal. El contexto es la forma estándar de propagar cancelaciones y plazos por todas las llamadas de una petición. Detener el temporizador con `defer` libera sus recursos si se sale antes.'),
    # ---- capítulo 7: Kotlin
    dict(ch=7, lang='kotlin', level='FOUNDATIONAL',
         prompt='Escribe `fun totalLength(words: List<String?>): Int` que sume las longitudes de las cadenas no nulas sin usar `!!`. Comprueba `["ab", null, "cde"]` (5), la lista vacía y una lista solo de nulos.',
         code='''fun totalLength(words: List<String?>): Int = words.sumOf { it?.length ?: 0 }''',
         harness='''{{code}}

fun main() {
    check(totalLength(listOf("ab", null, "cde")) == 5)
    check(totalLength(emptyList()) == 0)
    check(totalLength(listOf(null, null)) == 0)
    println("OK")
}''',
         tests=['`["ab", null, "cde"]` suma 5', 'la lista vacía suma 0', 'una lista de nulos suma 0'],
         why='El tipo `String?` obliga a decidir qué hacer con la ausencia. `?.` evita la llamada si el valor es nulo y `?:` aporta un valor alternativo, de modo que no hace falta el operador `!!`, que lanzaría una excepción.'),
    dict(ch=7, lang='kotlin', level='INTERMEDIATE',
         prompt='Define `sealed interface Result` con `data class Ok(val value: Int)` y `data class Err(val message: String)`, y `fun safeDivide(a: Int, b: Int): Result`. Escribe `fun describe(r: Result): String` con `when` exhaustivo (sin `else`) que devuelva `"ok: <valor>"` o `"error: <mensaje>"`. Comprueba `10 / 2`, `1 / 0` y la igualdad de `data class`.',
         code='''sealed interface Result
data class Ok(val value: Int) : Result
data class Err(val message: String) : Result

fun safeDivide(a: Int, b: Int): Result =
    if (b == 0) Err("division por cero") else Ok(a / b)

fun describe(r: Result): String = when (r) {
    is Ok -> "ok: ${r.value}"
    is Err -> "error: ${r.message}"
}''',
         harness='''{{code}}

fun main() {
    check(describe(safeDivide(10, 2)) == "ok: 5")
    check(describe(safeDivide(1, 0)) == "error: division por cero")
    check(safeDivide(9, 3) == Ok(3))
    check(Ok(1).copy(value = 2) == Ok(2))
    println("OK")
}''',
         tests=['`10 / 2` se describe como `ok: 5`', '`1 / 0` se describe como `error: division por cero`', 'las `data class` se comparan por valor', '`copy` crea una copia modificada'],
         why='`sealed` hace que el `when` sea exhaustivo sin `else`. Las `data class` generan igualdad, `copy` y `toString` según su constructor. Devolver un `Result` en lugar de lanzar una excepción hace explícito el fallo en el tipo.'),
    dict(ch=7, lang='kotlin', level='INTERMEDIATE',
         prompt='Escribe la función de extensión `fun <T> List<T>.secondOrNull(): T?` que devuelva el segundo elemento o `null`, y la extensión `fun String.wordCount(): Int` que cuente las palabras separadas por espacios en blanco. Comprueba ambas, incluyendo la lista de un elemento y la cadena vacía.',
         code='''fun <T> List<T>.secondOrNull(): T? = if (size >= 2) this[1] else null

fun String.wordCount(): Int = trim().split(Regex("\\\\s+")).count { it.isNotEmpty() }''',
         harness='''{{code}}

fun main() {
    check(listOf(1, 2, 3).secondOrNull() == 2)
    check(listOf("solo").secondOrNull() == null)
    check(emptyList<Int>().secondOrNull() == null)
    check("  hola   mundo kotlin ".wordCount() == 3)
    check("".wordCount() == 0)
    println("OK")
}''',
         tests=['`[1, 2, 3].secondOrNull()` es 2', 'una lista de un elemento devuelve `null`', '`"  hola   mundo kotlin "` tiene 3 palabras', 'la cadena vacía tiene 0 palabras'],
         why='Una extensión añade funciones a un tipo existente sin heredar ni modificarlo: se resuelven de forma estática. `secondOrNull` devuelve `T?` para que la ausencia sea parte del tipo, igual que `firstOrNull` de la biblioteca estándar.'),
    # ---- capítulo 8: Swift
    dict(ch=8, lang='swift', level='INTERMEDIATE',
         prompt='Define `struct Stack<Element>` con `push`, `pop` (devuelve `Element?`) y `count`, usando `mutating` donde haga falta. Comprueba la semántica de valor: copiar una pila y modificar la copia no cambia la original.',
         code='''struct Stack<Element> {
    private var items: [Element] = []
    var count: Int { items.count }
    mutating func push(_ item: Element) { items.append(item) }
    mutating func pop() -> Element? { items.popLast() }
}''',
         harness='''{{code}}

var a = Stack<Int>()
a.push(1)
a.push(2)
var b = a
b.push(3)
precondition(a.count == 2 && b.count == 3, "copia independiente")
precondition(b.pop() == 3 && b.pop() == 2 && b.pop() == 1 && b.pop() == nil, "orden LIFO")
precondition(a.pop() == 2, "la original sigue intacta")
print("OK")''',
         tests=['`push` y `pop` respetan el orden LIFO', 'la copia es independiente de la original', '`pop` en una pila vacía devuelve `nil`'],
         why='Un `struct` se copia al asignarlo; la copia diferida (copy-on-write) de `Array` evita duplicar los elementos hasta que uno de los dos se modifica. `mutating` marca los métodos que cambian el valor, y por eso no se pueden llamar sobre una constante.'),
    dict(ch=8, lang='swift', level='INTERMEDIATE',
         prompt='Define el protocolo `Describable` con `var name: String { get }` y una extensión que añada `func describe() -> String` (`"<nombre> (descripción)"`). Implementa el protocolo en dos tipos y escribe `func names<T: Describable>(_ items: [T]) -> [String]`. Comprueba la implementación por defecto y que un tipo puede sobrescribirla.',
         code='''protocol Describable {
    var name: String { get }
    func describe() -> String
}

extension Describable {
    func describe() -> String { "\\(name) (descripcion)" }
}

struct Cat: Describable { let name: String }
struct Robot: Describable {
    let name: String
    func describe() -> String { "robot \\(name)" }
}

func names<T: Describable>(_ items: [T]) -> [String] { items.map { $0.name } }''',
         harness='''{{code}}

precondition(Cat(name: "Tom").describe() == "Tom (descripcion)")
precondition(Robot(name: "R2").describe() == "robot R2")
precondition(names([Cat(name: "a"), Cat(name: "b")]) == ["a", "b"])
precondition(names([Robot]()) == [])
let anyItems: [any Describable] = [Cat(name: "x"), Robot(name: "y")]
precondition(anyItems.map { $0.describe() } == ["x (descripcion)", "robot y"])
print("OK")''',
         tests=['`Cat` usa la descripción por defecto', '`Robot` la sobrescribe', '`names` devuelve los nombres', 'una colección heterogénea `[any Describable]` despacha dinámicamente'],
         why='Una extensión de protocolo ofrece una implementación por defecto. Como `describe` también es requisito del protocolo, la llamada a través de `any Describable` usa la versión del tipo concreto; si no fuese requisito, se usaría la de la extensión, un error clásico.'),
    dict(ch=8, lang='swift', level='ADVANCED',
         prompt='Escribe `actor Counter` con `increment()` y `value`, y una función asíncrona `func countConcurrently(tasks: Int, each: Int) async -> Int` que lance `tasks` tareas que incrementen `each` veces el contador del actor. Comprueba 8 tareas con 1 000 incrementos: el resultado debe ser exacto sin cerrojos explícitos.',
         code='''actor Counter {
    private var count = 0
    func increment() { count += 1 }
    var value: Int { count }
}

func countConcurrently(tasks: Int, each: Int) async -> Int {
    let counter = Counter()
    await withTaskGroup(of: Void.self) { group in
        for _ in 0..<tasks {
            group.addTask {
                for _ in 0..<each {
                    await counter.increment()
                }
            }
        }
    }
    return await counter.value
}''',
         harness='''{{code}}

let total = await countConcurrently(tasks: 8, each: 1000)
precondition(total == 8000, "8x1000")
let none = await countConcurrently(tasks: 0, each: 5)
precondition(none == 0, "sin tareas")
print("OK")''',
         tests=['8 tareas con 1 000 incrementos dan 8 000', '0 tareas dan 0'],
         why='Un `actor` serializa el acceso a su estado: solo una tarea ejecuta código suyo a la vez, y las llamadas desde fuera usan `await`. El compilador impide así las carreras de datos sobre `count` sin escribir cerrojos.'),
]
