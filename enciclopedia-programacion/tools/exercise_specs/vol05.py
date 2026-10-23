"""Programming exercises of volume 5 (Python, JavaScript, TypeScript). Each reference program runs with the real interpreter or compiler."""

EXERCISES = [
    # ---- capítulo 1: Python, fundamentos
    dict(ch=1, lang='python', level='FOUNDATIONAL',
         prompt='Escribe `chunk(items, size)` que divida una lista en trozos consecutivos de longitud `size` (el último puede ser más corto) y devuelva una lista de listas, sin modificar la original. Si `size < 1` debe lanzar `ValueError`. Comprueba `chunk([1,2,3,4,5], 2) == [[1,2],[3,4],[5]]`, la lista vacía y el error.',
         code='''def chunk(items, size):
    if size < 1:
        raise ValueError("size debe ser al menos 1")
    return [items[i:i + size] for i in range(0, len(items), size)]''',
         harness='''original = [1, 2, 3, 4, 5]
assert chunk(original, 2) == [[1, 2], [3, 4], [5]]
assert original == [1, 2, 3, 4, 5]
assert chunk([], 3) == []
assert chunk([1, 2], 5) == [[1, 2]]
try:
    chunk([1], 0)
except ValueError:
    pass
else:
    raise AssertionError("debe lanzar ValueError")
print("OK")''',
         tests=['`chunk([1,2,3,4,5], 2)` da `[[1,2],[3,4],[5]]`', 'la lista original no cambia', 'la lista vacía da `[]`', '`size = 0` lanza `ValueError`'],
         why='Una rebanada `items[i:i + size]` crea una lista nueva, así que la original no se toca, y no falla si se pasa del final. Validar `size` antes de usarlo evita un `range` con paso cero, que lanzaría un error menos claro.'),
    dict(ch=1, lang='python', level='INTERMEDIATE',
         prompt='Escribe `is_balanced(text)` que compruebe si los paréntesis `()`, corchetes `[]` y llaves `{}` de una cadena están bien emparejados y anidados, ignorando los demás caracteres. Comprueba `"{[()]}"`, `"([)]"`, `"(("` y la cadena vacía.',
         code='''def is_balanced(text):
    pairs = {")": "(", "]": "[", "}": "{"}
    stack = []
    for char in text:
        if char in "([{":
            stack.append(char)
        elif char in pairs:
            if not stack or stack.pop() != pairs[char]:
                return False
    return not stack''',
         harness='''assert is_balanced("{[()]}")
assert not is_balanced("([)]")
assert not is_balanced("((")
assert not is_balanced(")")
assert is_balanced("")
assert is_balanced("def f(x): return [x, {1: (2)}]")
print("OK")''',
         tests=['`"{[()]}"` está equilibrada', '`"([)]"` no lo está', '`"(("` no lo está', 'un cierre sin apertura falla', 'la cadena vacía es válida'],
         why='Una pila recuerda las aperturas pendientes: cada cierre debe corresponder a la última apertura. Al final la pila debe estar vacía; si no, queda alguna apertura sin cerrar.'),
    dict(ch=1, lang='python', kind='debugging', level='INTERMEDIATE',
         prompt='Depuración. Esta función acumula entre llamadas porque el valor por defecto mutable se crea una sola vez:\n\n```python\ndef add_tag(tag, tags=[]):\n    tags.append(tag)\n    return tags\n```\n\nCorrígela para que cada llamada sin `tags` empiece con una lista nueva y vacía. Comprueba que dos llamadas independientes no comparten estado y que una lista pasada explícitamente se amplía.',
         code='''def add_tag(tag, tags=None):
    if tags is None:
        tags = []
    tags.append(tag)
    return tags''',
         harness='''assert add_tag("a") == ["a"]
assert add_tag("b") == ["b"]
mine = ["x"]
assert add_tag("y", mine) is mine
assert mine == ["x", "y"]
print("OK")''',
         tests=['`add_tag("a")` y luego `add_tag("b")` devuelven `["a"]` y `["b"]`', 'una lista pasada se modifica y se devuelve la misma'],
         why='Los valores por defecto se evalúan al definir la función, no en cada llamada, así que una lista literal en la firma se comparte entre todas. El centinela `None` y la creación dentro del cuerpo dan una lista nueva en cada ejecución.'),
    # ---- capítulo 2: modelo de datos, tipado, iteradores
    dict(ch=2, lang='python', level='INTERMEDIATE',
         prompt='Escribe la clase `Vector2` con `x` e `y`, que soporte suma (`+`), multiplicación por escalar (`*`, también `2 * v`), igualdad, `repr` legible, iteración (`x, y = v`) y `abs(v)` como módulo. Comprueba las operaciones y que `Vector2(3, 4)` tiene módulo 5.',
         code='''import math


class Vector2:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        return Vector2(self.x + other.x, self.y + other.y)

    def __mul__(self, k):
        return Vector2(self.x * k, self.y * k)

    __rmul__ = __mul__

    def __eq__(self, other):
        return isinstance(other, Vector2) and (self.x, self.y) == (other.x, other.y)

    def __hash__(self):
        return hash((self.x, self.y))

    def __iter__(self):
        yield self.x
        yield self.y

    def __abs__(self):
        return math.hypot(self.x, self.y)

    def __repr__(self):
        return f"Vector2({self.x!r}, {self.y!r})"''',
         harness='''a, b = Vector2(1, 2), Vector2(3, 4)
assert a + b == Vector2(4, 6)
assert a * 3 == 3 * a == Vector2(3, 6)
assert abs(b) == 5
x, y = b
assert (x, y) == (3, 4)
assert repr(a) == "Vector2(1, 2)"
assert {a, Vector2(1, 2)} == {a}
assert a != "no soy un vector"
print("OK")''',
         tests=['`Vector2(1, 2) + Vector2(3, 4)` es `Vector2(4, 6)`', '`a * 3` y `3 * a` coinciden', '`abs(Vector2(3, 4))` es 5', 'se puede desempaquetar', '`repr` es legible', 'es utilizable en conjuntos'],
         why='Los métodos especiales conectan la clase con la sintaxis del lenguaje: `__add__` con `+`, `__rmul__` con el escalar a la izquierda, `__iter__` con el desempaquetado. Si se define `__eq__`, conviene definir también `__hash__` coherente para poder usar el objeto en conjuntos y claves de diccionario.'),
    dict(ch=2, lang='python', level='INTERMEDIATE',
         prompt='Escribe un generador `fibonacci()` infinito y una función `take(n, iterable)` que devuelva una lista con los `n` primeros elementos de cualquier iterable sin consumir más de los necesarios. Comprueba los diez primeros números de Fibonacci y que `take` funciona con un generador que cuenta cuántos elementos produjo.',
         code='''from itertools import islice


def fibonacci():
    a, b = 0, 1
    while True:
        yield a
        a, b = b, a + b


def take(n, iterable):
    return list(islice(iterable, n))''',
         harness='''assert take(10, fibonacci()) == [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]
assert take(0, fibonacci()) == []
produced = []


def counted():
    for i in range(100):
        produced.append(i)
        yield i


assert take(3, counted()) == [0, 1, 2]
assert len(produced) == 3
print("OK")''',
         tests=['los diez primeros son `0, 1, 1, 2, 3, 5, 8, 13, 21, 34`', '`take(0, ...)` devuelve lista vacía', 'solo se produce lo necesario'],
         why='Un generador calcula cada valor cuando se le pide y recuerda su estado entre `yield`. `islice` se detiene tras `n` elementos sin leer el siguiente, por eso la secuencia infinita no cuelga el programa.'),
    dict(ch=2, lang='python', level='ADVANCED',
         prompt='Escribe el decorador `counted_cache(func)` que memorice los resultados por argumentos posicionales hashables y exponga `func.calls` (veces que se ejecutó realmente la función) y `func.hits` (veces que se respondió desde la caché). Conserva el nombre y la documentación de la función con `functools.wraps`. Comprueba con una función de Fibonacci recursiva.',
         code='''import functools


def counted_cache(func):
    cache = {}

    @functools.wraps(func)
    def wrapper(*args):
        if args in cache:
            wrapper.hits += 1
            return cache[args]
        wrapper.calls += 1
        result = func(*args)
        cache[args] = result
        return result

    wrapper.calls = 0
    wrapper.hits = 0
    return wrapper''',
         harness='''@counted_cache
def fib(n):
    """Fibonacci recursivo."""
    return n if n < 2 else fib(n - 1) + fib(n - 2)


assert fib(30) == 832040
assert fib.calls == 31
assert fib.hits == 28
assert fib.__name__ == "fib" and fib.__doc__ == "Fibonacci recursivo."
assert fib(30) == 832040 and fib.calls == 31
print("OK")''',
         tests=['`fib(30)` es 832040', 'la función se ejecuta 31 veces', 'hay 28 aciertos de caché', 'se conservan nombre y documentación', 'una segunda llamada no ejecuta la función'],
         why='Un decorador es una función que recibe una función y devuelve otra. El contador `calls` demuestra el efecto: sin memoización `fib(30)` necesitaría más de un millón de llamadas, con ella solo 31. `functools.wraps` copia nombre y documentación para que la envoltura sea transparente.'),
    # ---- capítulo 3: asyncio, concurrencia, metaprogramación
    dict(ch=3, lang='python', level='INTERMEDIATE',
         prompt='Escribe la corrutina `fetch_all(delays)` que lance una tarea por cada retraso en segundos (`await asyncio.sleep(d)`) y devuelva, en el orden de la entrada, la lista `["ok:<d>", ...]`. Las tareas deben ejecutarse a la vez: con retrasos `[0.2, 0.2, 0.2]` el total debe ser mucho menor que 0,6 s. Comprueba el orden y el tiempo.',
         code='''import asyncio


async def fetch_one(delay):
    await asyncio.sleep(delay)
    return f"ok:{delay}"


async def fetch_all(delays):
    return await asyncio.gather(*(fetch_one(d) for d in delays))''',
         harness='''import time

start = time.perf_counter()
result = asyncio.run(fetch_all([0.2, 0.2, 0.2]))
elapsed = time.perf_counter() - start
assert result == ["ok:0.2", "ok:0.2", "ok:0.2"]
assert elapsed < 0.5, elapsed
assert asyncio.run(fetch_all([0.05, 0.01])) == ["ok:0.05", "ok:0.01"]
assert asyncio.run(fetch_all([])) == []
print("OK")''',
         tests=['el resultado conserva el orden de la entrada', 'tres esperas de 0,2 s tardan menos de 0,5 s', 'una lista vacía devuelve lista vacía'],
         why='`asyncio.gather` programa todas las corrutinas en el mismo bucle de eventos; mientras una espera, otra avanza. El resultado conserva el orden de los argumentos aunque terminen en otro orden. Es concurrencia cooperativa: ayuda con esperas de red, no con cálculo intensivo.'),
    dict(ch=3, lang='python', level='INTERMEDIATE',
         prompt='Escribe `parallel_squares(values, workers)` que calcule los cuadrados con `concurrent.futures.ThreadPoolExecutor` y devuelva la lista en el mismo orden que la entrada. Escribe también `count_failures(values)` que, usando `submit` y `Future.exception()`, cuente cuántos valores negativos fallaron al llamar a `math.sqrt`. Comprueba ambos.',
         code='''import math
from concurrent.futures import ThreadPoolExecutor


def parallel_squares(values, workers):
    with ThreadPoolExecutor(max_workers=workers) as pool:
        return list(pool.map(lambda v: v * v, values))


def count_failures(values):
    with ThreadPoolExecutor(max_workers=2) as pool:
        futures = [pool.submit(math.sqrt, v) for v in values]
    return sum(1 for f in futures if f.exception() is not None)''',
         harness='''assert parallel_squares([1, 2, 3, 4], 3) == [1, 4, 9, 16]
assert parallel_squares([], 2) == []
assert count_failures([4, -1, 9, -4, 0]) == 2
assert count_failures([]) == 0
print("OK")''',
         tests=['`[1, 2, 3, 4]` da `[1, 4, 9, 16]` en orden', 'una entrada vacía da lista vacía', 'dos negativos fallan en `sqrt`', 'sin valores no hay fallos'],
         why='`pool.map` devuelve los resultados en el orden de la entrada. Una excepción dentro de una tarea no se propaga hasta que se consulta el `Future`; `exception()` la devuelve sin lanzarla, y la salida del bloque `with` espera a que terminen todas.'),
    dict(ch=3, lang='python', level='ADVANCED',
         prompt='Escribe una clase base `Plugin` que registre automáticamente cada subclase en `Plugin.registry` (diccionario nombre a clase) usando `__init_subclass__`, sin metaclase. El nombre por defecto es el de la clase en minúsculas y puede cambiarse con `class A(Plugin, name="x")`. Comprueba el registro y que dos plugins con el mismo nombre lanzan `ValueError`.',
         code='''class Plugin:
    registry = {}

    def __init_subclass__(cls, name=None, **kwargs):
        super().__init_subclass__(**kwargs)
        key = name or cls.__name__.lower()
        if key in Plugin.registry:
            raise ValueError(f"plugin duplicado: {key}")
        Plugin.registry[key] = cls''',
         harness='''class Csv(Plugin):
    pass


class JsonPlugin(Plugin, name="json"):
    pass


assert Plugin.registry == {"csv": Csv, "json": JsonPlugin}
try:
    class Another(Plugin, name="csv"):
        pass
except ValueError:
    pass
else:
    raise AssertionError("debe rechazar el duplicado")
assert len(Plugin.registry) == 2
print("OK")''',
         tests=['`Csv` se registra como `"csv"`', 'el nombre se puede cambiar con `name="json"`', 'un nombre repetido lanza `ValueError`', 'el registro no cambia tras el error'],
         why='`__init_subclass__` se invoca cuando se define una subclase, así que permite registros y validaciones sin metaclases. El error se lanza antes de insertar en el registro, de modo que un duplicado no deja el estado a medias.'),
    # ---- capítulo 4: JavaScript, cierres y prototipos
    dict(ch=4, lang='js', level='FOUNDATIONAL',
         prompt='Escribe `makeCounter(start = 0)` que devuelva un objeto con `increment()`, `decrement()` y `value()`, cuyo estado sea privado (no accesible como propiedad). Dos contadores deben ser independientes. Comprueba las operaciones y que no existe `counter.count`.',
         code='''function makeCounter(start = 0) {
  let count = start;
  return {
    increment() { count += 1; return count; },
    decrement() { count -= 1; return count; },
    value() { return count; },
  };
}''',
         harness='''const assert = require("node:assert");
const a = makeCounter();
const b = makeCounter(10);
a.increment(); a.increment(); b.decrement();
assert.strictEqual(a.value(), 2);
assert.strictEqual(b.value(), 9);
assert.strictEqual(a.count, undefined);
assert.deepStrictEqual(Object.keys(a).sort(), ["decrement", "increment", "value"]);
console.log("OK");''',
         tests=['dos incrementos dejan el contador en 2', 'el segundo contador es independiente', 'no existe la propiedad `count`'],
         why='Una clausura conserva las variables de la función exterior aunque esta haya terminado. `count` solo es accesible desde los tres métodos devueltos, que es la forma clásica de tener estado privado antes de los campos `#privados`.'),
    dict(ch=4, lang='js', level='INTERMEDIATE',
         prompt='Escribe `memoize(fn)` que guarde en un `Map` los resultados de `fn` según sus argumentos (usa `JSON.stringify(args)` como clave) y no vuelva a llamar a `fn` con los mismos argumentos. Comprueba con un contador de llamadas que `memoize` evita el recálculo.',
         code='''function memoize(fn) {
  const cache = new Map();
  return function (...args) {
    const key = JSON.stringify(args);
    if (!cache.has(key)) {
      cache.set(key, fn.apply(this, args));
    }
    return cache.get(key);
  };
}''',
         harness='''const assert = require("node:assert");
let calls = 0;
const slowSquare = (n) => { calls += 1; return n * n; };
const fast = memoize(slowSquare);
assert.strictEqual(fast(9), 81);
assert.strictEqual(fast(9), 81);
assert.strictEqual(fast(3), 9);
assert.strictEqual(calls, 2);
const sum = memoize((a, b) => { calls += 1; return a + b; });
assert.strictEqual(sum(1, 2), 3);
assert.strictEqual(sum(1, 2), 3);
assert.strictEqual(sum(2, 1), 3);
assert.strictEqual(calls, 4);
console.log("OK");''',
         tests=['`fast(9)` dos veces ejecuta la función una vez', 'argumentos distintos se calculan por separado', 'varios argumentos forman una sola clave', '`sum(2, 1)` es otra clave que `sum(1, 2)`'],
         why='La clausura guarda el `Map`. Usar `cache.has` y no comprobar el valor devuelto permite cachear resultados falsos como `0` o `undefined`. Serializar con JSON funciona para argumentos simples; no distingue objetos con ciclos ni funciones.'),
    dict(ch=4, lang='js', level='INTERMEDIATE',
         prompt='Construye una cadena de prototipos sin usar `class`: `Animal` con el método `describe()` que devuelva `"<nombre> hace <sonido>"`, y `Dog` que herede de `Animal` mediante `Object.create` y añada `fetch()`. Comprueba `instanceof`, que `describe` se hereda y que se encuentra en el prototipo y no en la instancia.',
         code='''function Animal(name, sound) {
  this.name = name;
  this.sound = sound;
}
Animal.prototype.describe = function () {
  return `${this.name} hace ${this.sound}`;
};

function Dog(name) {
  Animal.call(this, name, "guau");
}
Dog.prototype = Object.create(Animal.prototype);
Dog.prototype.constructor = Dog;
Dog.prototype.fetch = function () {
  return `${this.name} trae la pelota`;
};''',
         harness='''const assert = require("node:assert");
const rex = new Dog("Rex");
assert.strictEqual(rex.describe(), "Rex hace guau");
assert.strictEqual(rex.fetch(), "Rex trae la pelota");
assert.ok(rex instanceof Dog && rex instanceof Animal);
assert.strictEqual(Object.hasOwn(rex, "describe"), false);
assert.strictEqual(Object.getPrototypeOf(Object.getPrototypeOf(rex)), Animal.prototype);
assert.strictEqual(new Animal("Gato", "miau").fetch, undefined);
console.log("OK");''',
         tests=['`describe` devuelve `"Rex hace guau"`', '`fetch` solo existe en `Dog`', '`rex` es instancia de `Dog` y de `Animal`', '`describe` no es propiedad propia de la instancia'],
         why='La búsqueda de una propiedad sube por la cadena de prototipos hasta encontrarla: `rex`, `Dog.prototype`, `Animal.prototype`. `Object.create` enlaza los prototipos sin ejecutar el constructor padre; por eso `Dog` llama explícitamente a `Animal.call(this, ...)`.'),
    # ---- capítulo 5: event loop, promesas, Node
    dict(ch=5, lang='js', level='INTERMEDIATE',
         prompt='Escribe `eventOrder()` que devuelva una promesa con el orden real en que se ejecutan estas cuatro marcas: código síncrono (`"sync"`), una microtarea con `Promise.resolve().then` (`"micro"`), un `setTimeout(..., 0)` (`"macro"`) y una segunda microtarea encadenada desde la primera (`"micro2"`). Debes obtener `["sync", "micro", "micro2", "macro"]` y explicar por qué.',
         code='''function eventOrder() {
  const order = [];
  return new Promise((resolve) => {
    setTimeout(() => {
      order.push("macro");
      resolve(order);
    }, 0);
    Promise.resolve()
      .then(() => {
        order.push("micro");
      })
      .then(() => {
        order.push("micro2");
      });
    order.push("sync");
  });
}''',
         harness='''const assert = require("node:assert");
eventOrder().then((order) => {
  assert.deepStrictEqual(order, ["sync", "micro", "micro2", "macro"]);
  console.log("OK");
});''',
         tests=['el orden es `sync`, `micro`, `micro2`, `macro`'],
         why='El bucle de eventos ejecuta primero el código síncrono, luego vacía por completo la cola de microtareas (incluidas las que se encadenan) y solo después toma la siguiente macrotarea, como un temporizador. Por eso `micro2` precede a un `setTimeout` de 0 ms.'),
    dict(ch=5, lang='js', level='INTERMEDIATE',
         prompt='Escribe `async function retry(fn, times)` que ejecute `fn` (que devuelve una promesa) y, si falla, lo reintente hasta `times` intentos en total; devuelve el primer resultado correcto o lanza el último error. Comprueba una función que falla dos veces y luego acierta, y otra que siempre falla.',
         code='''async function retry(fn, times) {
  let lastError;
  for (let attempt = 1; attempt <= times; attempt++) {
    try {
      return await fn(attempt);
    } catch (error) {
      lastError = error;
    }
  }
  throw lastError;
}''',
         harness='''const assert = require("node:assert");
(async () => {
  let calls = 0;
  const flaky = async () => {
    calls += 1;
    if (calls < 3) throw new Error("falla " + calls);
    return "listo";
  };
  assert.strictEqual(await retry(flaky, 5), "listo");
  assert.strictEqual(calls, 3);
  let tries = 0;
  const broken = async () => { tries += 1; throw new Error("siempre " + tries); };
  await assert.rejects(retry(broken, 3), /siempre 3/);
  assert.strictEqual(tries, 3);
  assert.strictEqual(await retry(async (n) => n, 1), 1);
  console.log("OK");
})();''',
         tests=['falla dos veces y acierta a la tercera', 'una función que siempre falla lanza el último error tras 3 intentos', 'un acierto inmediato no reintenta'],
         why='`await` dentro de `try` convierte el rechazo de la promesa en una excepción que `catch` puede tratar. Se conserva el último error para que quien llama vea la causa real. En producción conviene añadir una espera creciente entre intentos.'),
    dict(ch=5, lang='js', level='ADVANCED',
         prompt='Escribe `async function allSettledSummary(promises)` que espere a todas las promesas aunque algunas fallen y devuelva `{ ok: [...valores], failed: [...mensajes de error] }` conservando el orden. Usa `Promise.allSettled`. Comprueba una mezcla de éxitos y fallos.',
         code='''async function allSettledSummary(promises) {
  const results = await Promise.allSettled(promises);
  const summary = { ok: [], failed: [] };
  for (const r of results) {
    if (r.status === "fulfilled") summary.ok.push(r.value);
    else summary.failed.push(String(r.reason.message ?? r.reason));
  }
  return summary;
}''',
         harness='''const assert = require("node:assert");
const wait = (ms, v) => new Promise((r) => setTimeout(() => r(v), ms));
const boom = (ms, msg) => new Promise((_, rej) => setTimeout(() => rej(new Error(msg)), ms));
(async () => {
  const summary = await allSettledSummary([wait(20, "a"), boom(5, "x"), wait(1, "c"), boom(10, "y")]);
  assert.deepStrictEqual(summary, { ok: ["a", "c"], failed: ["x", "y"] });
  assert.deepStrictEqual(await allSettledSummary([]), { ok: [], failed: [] });
  console.log("OK");
})();''',
         tests=['éxitos y fallos se separan conservando su orden', 'una lista vacía devuelve dos listas vacías'],
         why='`Promise.all` se rechaza en cuanto una promesa falla; `allSettled` espera a todas y describe cada resultado. Es la herramienta correcta cuando los fallos parciales son aceptables y se quiere informar de cada uno.'),
    # ---- capítulo 6: TypeScript
    dict(ch=6, lang='ts', level='FOUNDATIONAL',
         prompt='Define la unión discriminada `Shape` (`{ kind: "circle"; r: number } | { kind: "rect"; w: number; h: number }`) y `area(shape: Shape): number` con un `switch` que cubra todos los casos y use `never` para comprobar la exhaustividad. Comprueba círculo y rectángulo.',
         code='''type Shape =
  | { kind: "circle"; r: number }
  | { kind: "rect"; w: number; h: number };

function area(shape: Shape): number {
  switch (shape.kind) {
    case "circle":
      return Math.PI * shape.r ** 2;
    case "rect":
      return shape.w * shape.h;
    default: {
      const unreachable: never = shape;
      return unreachable;
    }
  }
}''',
         harness='''import assert from "node:assert";
assert.ok(Math.abs(area({ kind: "circle", r: 1 }) - Math.PI) < 1e-12);
assert.strictEqual(area({ kind: "rect", w: 3, h: 4 }), 12);
console.log("OK");''',
         tests=['un círculo de radio 1 tiene área `PI`', 'un rectángulo 3 por 4 tiene área 12', 'añadir una variante sin tratarla da error de compilación'],
         why='El campo `kind` discrimina la unión: dentro de cada `case`, TypeScript estrecha el tipo y permite acceder a `r` o a `w` y `h`. La asignación a `never` en `default` falla en compilación si falta una variante, de modo que añadir una sin tratarla se detecta al compilar.'),
    dict(ch=6, lang='ts', level='INTERMEDIATE',
         prompt='Escribe la función genérica `groupBy<T, K extends string | number>(items: T[], key: (item: T) => K): Record<K, T[]>` que agrupe los elementos por la clave calculada. Comprueba con números agrupados por paridad y con objetos agrupados por su categoría.',
         code='''function groupBy<T, K extends string | number>(items: T[], key: (item: T) => K): Record<K, T[]> {
  const result = {} as Record<K, T[]>;
  for (const item of items) {
    const k = key(item);
    (result[k] ??= []).push(item);
  }
  return result;
}''',
         harness='''import assert from "node:assert";
const byParity = groupBy([1, 2, 3, 4, 5], (n) => (n % 2 === 0 ? "even" : "odd"));
assert.deepStrictEqual(byParity, { odd: [1, 3, 5], even: [2, 4] });
const items = [{ name: "a", cat: "x" }, { name: "b", cat: "y" }, { name: "c", cat: "x" }];
const byCat = groupBy(items, (i) => i.cat);
assert.deepStrictEqual(byCat.x.map((i) => i.name), ["a", "c"]);
assert.deepStrictEqual(groupBy([], (n: number) => n), {});
console.log("OK");''',
         tests=['los números se agrupan por paridad', 'los objetos se agrupan por categoría', 'una lista vacía da un objeto vacío'],
         why='Los parámetros de tipo `T` y `K` se infieren de los argumentos, por lo que `byParity` se tipa como `Record<"even" | "odd", number[]>` sin anotaciones. `??=` crea la lista solo si no existía. Un tipo `K` limitado a `string | number` garantiza que pueda usarse como clave.'),
    dict(ch=6, lang='ts', level='INTERMEDIATE',
         prompt='Escribe la guarda de tipo `isNonEmptyString(value: unknown): value is string` y `function lengths(values: unknown[]): number[]` que devuelva la longitud de las cadenas no vacías ignorando todo lo demás, usando la guarda para que el compilador estreche el tipo. Comprueba una lista con mezcla de tipos.',
         code='''function isNonEmptyString(value: unknown): value is string {
  return typeof value === "string" && value.length > 0;
}

function lengths(values: unknown[]): number[] {
  return values.filter(isNonEmptyString).map((s) => s.length);
}''',
         harness='''import assert from "node:assert";
assert.deepStrictEqual(lengths(["ab", 3, "", null, "xyz", undefined, {}]), [2, 3]);
assert.deepStrictEqual(lengths([]), []);
assert.strictEqual(isNonEmptyString(""), false);
console.log("OK");''',
         tests=['`["ab", 3, "", null, "xyz", ...]` da `[2, 3]`', 'una lista vacía da vacía', 'la cadena vacía no pasa la guarda'],
         why='El predicado `value is string` indica al compilador que, si la función devuelve `true`, el argumento es una cadena. `filter` con una guarda produce `string[]`, de modo que `s.length` es válido sin conversiones.'),
    # ---- capítulo 7: TypeScript avanzado (el compilador es la prueba)
    dict(ch=7, lang='ts-types', expect='', level='INTERMEDIATE',
         prompt='Escribe el tipo mapeado `Mutable<T>` que quite el modificador `readonly` de todas las propiedades de `T`. Demuéstralo con tipos: asigna una propiedad de un objeto de tipo `Mutable<Readonly<{ a: number }>>` y comprueba con el tipo `Equal` que el resultado coincide con `{ a: number }`.',
         code='''type Mutable<T> = { -readonly [K in keyof T]: T[K] };''',
         harness='''type Equal<A, B> = (<T>() => T extends A ? 1 : 2) extends (<T>() => T extends B ? 1 : 2) ? true : false;
type Expect<T extends true> = T;

type Frozen = Readonly<{ a: number; b: string }>;
type Test1 = Expect<Equal<Mutable<Frozen>, { a: number; b: string }>>;
type Test2 = Expect<Equal<Mutable<{ readonly x?: boolean }>, { x?: boolean }>>;

const m: Mutable<Frozen> = { a: 1, b: "x" };
m.a = 2;
export type { Test1, Test2 };''',
         tests=['`Mutable<Readonly<{a: number; b: string}>>` equivale a `{a: number; b: string}`', 'conserva las propiedades opcionales', 'permite asignar a una propiedad antes de solo lectura'],
         why='`-readonly` en un tipo mapeado elimina el modificador, igual que `-?` elimina la opcionalidad. La prueba es del propio compilador: si `Mutable` fuese incorrecto, `Expect<Equal<...>>` fallaría al compilar.'),
    dict(ch=7, lang='ts-types', expect='', level='ADVANCED',
         prompt='Escribe el tipo condicional `ElementOf<T>` que dé el tipo de los elementos de un array (`ElementOf<string[]>` es `string`) y, si `T` no es un array, el propio `T`. Después, `Awaited2<T>` que desenvuelva una `Promise` (una sola capa) con `infer`. Comprueba ambos con `Equal`.',
         code='''type ElementOf<T> = T extends readonly (infer U)[] ? U : T;
type Awaited2<T> = T extends Promise<infer U> ? U : T;''',
         harness='''type Equal<A, B> = (<T>() => T extends A ? 1 : 2) extends (<T>() => T extends B ? 1 : 2) ? true : false;
type Expect<T extends true> = T;

type T1 = Expect<Equal<ElementOf<string[]>, string>>;
type T2 = Expect<Equal<ElementOf<readonly [1, 2]>, 1 | 2>>;
type T3 = Expect<Equal<ElementOf<number>, number>>;
type T4 = Expect<Equal<Awaited2<Promise<boolean>>, boolean>>;
type T5 = Expect<Equal<Awaited2<string>, string>>;
export type { T1, T2, T3, T4, T5 };''',
         tests=['`ElementOf<string[]>` es `string`', '`ElementOf<readonly [1, 2]>` es `1 | 2`', '`ElementOf<number>` es `number`', '`Awaited2<Promise<boolean>>` es `boolean`', '`Awaited2<string>` es `string`'],
         why='`infer U` captura el tipo que aparece en esa posición cuando el patrón coincide. Los tipos condicionales se distribuyen sobre uniones, de modo que `ElementOf<string[] | number[]>` sería `string | number`.'),
    dict(ch=7, lang='ts-types', expect='', level='ADVANCED',
         prompt='Con tipos literales de plantilla, escribe `EventName<T extends string>` que convierta `"click"` en `"onClick"` (prefijo `on` y primera letra en mayúscula, con `Capitalize`) y funcione sobre uniones: `EventName<"click" | "hover">` es `"onClick" | "onHover"`. Comprueba con `Equal`.',
         code='''type EventName<T extends string> = `on${Capitalize<T>}`;''',
         harness='''type Equal<A, B> = (<T>() => T extends A ? 1 : 2) extends (<T>() => T extends B ? 1 : 2) ? true : false;
type Expect<T extends true> = T;

type T1 = Expect<Equal<EventName<"click">, "onClick">>;
type T2 = Expect<Equal<EventName<"click" | "hover">, "onClick" | "onHover">>;
type T3 = Expect<Equal<EventName<"a">, "onA">>;
// @ts-expect-error: un número no es una cadena
type T4 = EventName<5>;
export type { T1, T2, T3, T4 };''',
         tests=['`EventName<"click">` es `"onClick"`', 'funciona sobre una unión', 'un número no cumple la restricción'],
         why='Un tipo literal de plantilla construye cadenas a nivel de tipos, y al aplicarse a una unión produce una unión con cada combinación. `Capitalize` es uno de los tipos intrínsecos de cadenas del compilador. `@ts-expect-error` falla si la línea siguiente no tuviera error, lo que comprueba la restricción.'),
    # ---- capítulo 8: interoperabilidad
    dict(ch=8, lang='python', level='INTERMEDIATE',
         prompt='Escribe `to_wire(record)` y `from_wire(text)` para intercambiar datos con JavaScript: `to_wire` serializa un diccionario a JSON compacto con claves ordenadas y sin escapar los caracteres no ASCII, y `from_wire` lo recupera. Comprueba la ida y vuelta con tildes y con un número grande.',
         code='''import json


def to_wire(record):
    return json.dumps(record, sort_keys=True, ensure_ascii=False, separators=(",", ":"))


def from_wire(text):
    return json.loads(text)''',
         harness='''record = {"nombre": "Ángel", "edad": 31, "tags": ["año", "ñu"], "n": 9007199254740993}
text = to_wire(record)
assert text == '{"edad":31,"n":9007199254740993,"nombre":"Ángel","tags":["año","ñu"]}'
assert from_wire(text) == record
assert to_wire({}) == "{}"
print("OK")''',
         tests=['las claves salen ordenadas y sin espacios', 'las tildes no se escapan', 'la ida y vuelta devuelve el original', 'un entero mayor que 2^53 se conserva en Python'],
         why='Fijar el orden de las claves y los separadores hace que la salida sea determinista, lo que facilita firmas y comparaciones. Los enteros mayores que `2^53` se conservan en Python, pero un `JSON.parse` en JavaScript los redondearía: conviene transmitirlos como cadenas.'),
    dict(ch=8, lang='js', level='INTERMEDIATE',
         prompt='Escribe `parseWire(text)` en JavaScript que lea el JSON producido por el ejercicio anterior y compruebe que `n` (un entero grande) se transmite como cadena para no perder precisión: si `n` llega como número mayor que `Number.MAX_SAFE_INTEGER`, debe lanzar `RangeError`. Comprueba un mensaje correcto y uno que perdería precisión.',
         code='''function parseWire(text) {
  const data = JSON.parse(text);
  if (typeof data.n === "number" && !Number.isSafeInteger(data.n)) {
    throw new RangeError("entero fuera del rango seguro: transmitelo como cadena");
  }
  return data;
}''',
         harness='''const assert = require("node:assert");
assert.deepStrictEqual(parseWire('{"n":"9007199254740993","x":1}'), { n: "9007199254740993", x: 1 });
assert.strictEqual(parseWire('{"n":42}').n, 42);
assert.throws(() => parseWire('{"n":9007199254740993}'), RangeError);
assert.strictEqual(9007199254740993, 9007199254740992);
console.log("OK");''',
         tests=['un `n` como cadena se acepta', 'un `n` pequeño como número se acepta', 'un `n` que no es entero seguro lanza `RangeError`', 'JavaScript redondea 2^53 + 1'],
         why='Los números de JavaScript son dobles IEEE 754, y solo representan exactamente los enteros hasta `2^53 - 1`. `Number.isSafeInteger` detecta los que ya se han redondeado al leer el JSON, algo que no se puede arreglar a posteriori.'),
    dict(ch=8, lang='ts', level='ADVANCED',
         prompt='Escribe `parseUser(data: unknown): User | null` que valide en tiempo de ejecución un objeto recibido de fuera (`{ name: string; age: number }` con `age` entero entre 0 y 150) y devuelva `null` si no cumple, sin lanzar excepciones. Comprueba un objeto válido y varios inválidos: `null`, texto, edad negativa, edad no entera y nombre ausente.',
         code='''interface User {
  name: string;
  age: number;
}

function parseUser(data: unknown): User | null {
  if (typeof data !== "object" || data === null) return null;
  const { name, age } = data as Record<string, unknown>;
  if (typeof name !== "string" || name.length === 0) return null;
  if (typeof age !== "number" || !Number.isInteger(age) || age < 0 || age > 150) return null;
  return { name, age };
}''',
         harness='''import assert from "node:assert";
assert.deepStrictEqual(parseUser({ name: "Ana", age: 31, extra: true }), { name: "Ana", age: 31 });
for (const bad of [null, "texto", 5, { name: "Ana", age: -1 }, { name: "Ana", age: 3.5 }, { age: 4 }, { name: "", age: 4 }, { name: "Ana", age: "31" }]) {
  assert.strictEqual(parseUser(bad), null);
}
console.log("OK");''',
         tests=['un objeto válido se devuelve sin los campos extra', '`null`, un texto y un número devuelven `null`', 'edad negativa o no entera devuelve `null`', 'falta el nombre o está vacío devuelve `null`'],
         why='Los tipos de TypeScript se borran al compilar, así que los datos que vienen de fuera (red, ficheros) llegan como `unknown` y hay que validarlos en ejecución. La función estrecha el tipo paso a paso y devuelve un `User` construido, no el objeto original, para no dejar pasar campos inesperados.'),
]
