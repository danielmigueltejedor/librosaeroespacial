"""Programming exercises of volume 9 (software engineering, architecture and projects). Each reference program runs with a real interpreter."""

EXERCISES = [
    # ---- capítulo 1: diseño, patrones y refactorización
    dict(ch=1, lang='python', level='INTERMEDIATE',
         prompt='Escribe `cyclomatic(source)` que calcule la complejidad ciclomática de cada función de un código Python con el módulo `ast`: devuelve un diccionario de nombre de función a 1 más el número de puntos de decisión (`if` y `elif`, `for`, `while`, `except`, expresiones condicionales, cada operador booleano `and`/`or` y cada `if` de una comprensión). Comprueba una función simple y una con varias ramas.',
         code='''import ast


class _Decisions(ast.NodeVisitor):
    def __init__(self):
        self.count = 0

    def visit_If(self, node):
        self.count += 1
        self.generic_visit(node)

    visit_For = visit_While = visit_ExceptHandler = visit_IfExp = visit_If

    def visit_BoolOp(self, node):
        self.count += len(node.values) - 1
        self.generic_visit(node)

    def visit_comprehension(self, node):
        self.count += len(node.ifs)
        self.generic_visit(node)


def cyclomatic(source):
    result = {}
    for node in ast.walk(ast.parse(source)):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            visitor = _Decisions()
            for child in node.body:
                visitor.visit(child)
            result[node.name] = 1 + visitor.count
    return result''',
         harness='''src = """
def simple(x):
    return x + 1

def branches(a, b):
    if a and b:
        return 1
    elif a or b:
        return 2
    for i in range(3):
        if i:
            continue
    return [x for x in range(5) if x % 2]
"""
result = cyclomatic(src)
assert result["simple"] == 1
assert result["branches"] == 1 + 1 + 1 + 1 + 1 + 1 + 1 + 1
print("OK")''',
         tests=['una función sin decisiones tiene complejidad 1', 'cada `if`, `elif`, `for`, operador booleano y `if` de comprensión suma 1', 'la función `branches` tiene complejidad 8'],
         why='La complejidad ciclomática es el número de caminos independientes: 1 más las decisiones. Dividir una función no elimina decisiones, las reparte; por eso una refactorización reduce la complejidad máxima por función, no la total. `ast` permite medirla sin ejecutar el código.'),
    dict(ch=1, lang='python', level='FOUNDATIONAL',
         prompt='Implementa el patrón Estrategia con funciones de primera clase, sin una clase por estrategia: `price(base, strategy)` donde `strategy` es una función `precio -> precio`, y las estrategias `no_discount`, `percent(p)` (devuelve una función) y `bulk(min_units, off)`. Comprueba precios con tres estrategias y que `percent` valida su rango.',
         code='''def no_discount(total):
    return total


def percent(p):
    if not 0 <= p <= 100:
        raise ValueError("porcentaje fuera de rango")
    return lambda total: total * (100 - p) / 100


def bulk(min_units, off):
    return lambda total, units=1: total - off if units >= min_units else total


def price(base, strategy):
    return strategy(base)''',
         harness='''assert price(200, no_discount) == 200
assert price(200, percent(25)) == 150
assert price(80, percent(0)) == 80
assert bulk(10, 5)(100, units=10) == 95
assert bulk(10, 5)(100, units=3) == 100
try:
    percent(120)
except ValueError:
    pass
else:
    raise AssertionError("debe validar")
print("OK")''',
         tests=['`no_discount` no cambia el precio', '`percent(25)` rebaja un 25 %', '`bulk` solo aplica a partir del mínimo de unidades', '`percent(120)` lanza `ValueError`'],
         why='Cuando una estrategia solo tiene un método, una función hace el mismo trabajo que una clase y sin ceremonia. Las funciones que devuelven funciones (clausuras) permiten parametrizarlas. Una jerarquía de clases tendría sentido si cada estrategia necesitase estado o varios métodos.'),
    dict(ch=1, lang='python', level='INTERMEDIATE',
         prompt='Escribe una clase `EventBus` con `subscribe(topic, handler)` que devuelva una función de baja, `publish(topic, payload)` que llame a los suscriptores en orden de alta y devuelva cuántos se llamaron, y que un manejador que lance una excepción no impida que se llame a los demás (se registra en `bus.errors`). Comprueba orden, baja y aislamiento de fallos.',
         code='''class EventBus:
    def __init__(self):
        self._handlers = {}
        self.errors = []

    def subscribe(self, topic, handler):
        self._handlers.setdefault(topic, []).append(handler)
        return lambda: self._handlers[topic].remove(handler)

    def publish(self, topic, payload):
        called = 0
        for handler in list(self._handlers.get(topic, [])):
            try:
                handler(payload)
                called += 1
            except Exception as error:
                self.errors.append(error)
        return called''',
         harness='''bus = EventBus()
log = []
off_a = bus.subscribe("t", lambda p: log.append(("a", p)))
def failing(p):
    raise RuntimeError("falla")
bus.subscribe("t", failing)
bus.subscribe("t", lambda p: log.append(("c", p)))
assert bus.publish("t", 1) == 2
assert log == [("a", 1), ("c", 1)] and len(bus.errors) == 1
off_a()
assert bus.publish("t", 2) == 1
assert log[-1] == ("c", 2)
assert bus.publish("otro", 0) == 0
print("OK")''',
         tests=['los suscriptores se llaman en orden de alta', 'un manejador que falla no impide los demás', 'tras la baja ya no se llama al manejador', 'un tema sin suscriptores devuelve 0'],
         why='El patrón Observador desacopla a quien emite de quien reacciona. Copiar la lista antes de recorrerla permite que un manejador se dé de baja sin alterar el recorrido, y aislar los errores impide que un suscriptor defectuoso bloquee a los demás.'),
    # ---- capítulo 2: arquitectura
    dict(ch=2, lang='python', level='INTERMEDIATE',
         prompt='Con arquitectura hexagonal, escribe `OrderService(payments, clock)` cuyo método `place(order_id, amount)` use el puerto `payments.charge(amount)` y registre la hora con `clock()`. Si el cobro falla (lanza `PaymentError`), el pedido queda `"rejected"`; si no, `"paid"`. Comprueba el servicio con adaptadores falsos, sin red ni reloj real.',
         code='''class PaymentError(Exception):
    pass


class OrderService:
    def __init__(self, payments, clock):
        self.payments = payments
        self.clock = clock
        self.orders = {}

    def place(self, order_id, amount):
        try:
            self.payments.charge(amount)
            status = "paid"
        except PaymentError:
            status = "rejected"
        self.orders[order_id] = {"amount": amount, "status": status, "at": self.clock()}
        return status''',
         harness='''class FakePayments:
    def __init__(self, limit):
        self.limit = limit
        self.charged = []

    def charge(self, amount):
        if amount > self.limit:
            raise PaymentError("sin fondos")
        self.charged.append(amount)


payments = FakePayments(limit=100)
service = OrderService(payments, clock=lambda: 1234)
assert service.place("A", 50) == "paid"
assert service.place("B", 500) == "rejected"
assert payments.charged == [50]
assert service.orders["A"] == {"amount": 50, "status": "paid", "at": 1234}
assert service.orders["B"]["status"] == "rejected"
print("OK")''',
         tests=['un cobro dentro del límite deja el pedido `paid`', 'un cobro rechazado deja el pedido `rejected`', 'solo se cobra el pedido aceptado', 'la hora procede del reloj inyectado'],
         why='El servicio de dominio solo conoce los puertos (`charge`, `clock`), no sus implementaciones. Eso permite probarlo con adaptadores falsos rápidos y deterministas y cambiar la pasarela de pago sin tocar la lógica de negocio.'),
    dict(ch=2, lang='python', level='INTERMEDIATE',
         prompt='Define el objeto de valor `Money(amount_cents, currency)` inmutable (`dataclass(frozen=True)`) con suma que exige la misma divisa (si no, `ValueError`), multiplicación por entero y `__str__` (`"12.50 EUR"`). Comprueba igualdad por valor, inmutabilidad y el rechazo de sumar divisas distintas.',
         code='''from dataclasses import dataclass


@dataclass(frozen=True)
class Money:
    amount_cents: int
    currency: str

    def __add__(self, other):
        if self.currency != other.currency:
            raise ValueError("divisas distintas")
        return Money(self.amount_cents + other.amount_cents, self.currency)

    def __mul__(self, factor):
        return Money(self.amount_cents * factor, self.currency)

    def __str__(self):
        return f"{self.amount_cents // 100}.{abs(self.amount_cents) % 100:02d} {self.currency}"''',
         harness='''a = Money(1250, "EUR")
assert a + Money(50, "EUR") == Money(1300, "EUR")
assert a * 2 == Money(2500, "EUR")
assert str(a) == "12.50 EUR"
assert Money(5, "EUR") == Money(5, "EUR")
assert len({Money(5, "EUR"), Money(5, "EUR")}) == 1
try:
    a + Money(1, "USD")
except ValueError:
    pass
else:
    raise AssertionError("divisas")
try:
    a.amount_cents = 1
except Exception as error:
    assert type(error).__name__ == "FrozenInstanceError"
else:
    raise AssertionError("inmutable")
print("OK")''',
         tests=['sumar dos importes de la misma divisa funciona', 'multiplicar por un entero funciona', '`str` da `"12.50 EUR"`', 'dos valores iguales son iguales y comparten hash', 'sumar divisas distintas lanza `ValueError`', 'asignar a un campo lanza `FrozenInstanceError`'],
         why='Un objeto de valor se define por sus atributos, no por su identidad, y no cambia. Guardar el dinero en céntimos enteros evita errores de redondeo de la coma flotante, y exigir la misma divisa impide sumar manzanas con naranjas.'),
    dict(ch=2, lang='python', level='ADVANCED',
         prompt='Reproduce el problema N+1 y su solución: `class Db` cuenta las consultas. Escribe `authors_naive(db, book_ids)` (una consulta por libro) y `authors_batched(db, book_ids)` (una sola consulta con `IN`), que devuelven lo mismo. Comprueba con 20 libros que la versión ingenua hace 21 consultas y la agrupada 2, y que el resultado coincide.',
         code='''class Db:
    def __init__(self, books, authors):
        self.books = books
        self.authors = authors
        self.queries = 0

    def books_by_ids(self, ids):
        self.queries += 1
        return [self.books[i] for i in ids]

    def author_by_id(self, author_id):
        self.queries += 1
        return self.authors[author_id]

    def authors_by_ids(self, ids):
        self.queries += 1
        return {i: self.authors[i] for i in ids}


def authors_naive(db, book_ids):
    books = db.books_by_ids(book_ids)
    return [db.author_by_id(b["author_id"]) for b in books]


def authors_batched(db, book_ids):
    books = db.books_by_ids(book_ids)
    wanted = {b["author_id"] for b in books}
    found = db.authors_by_ids(wanted)
    return [found[b["author_id"]] for b in books]''',
         harness='''authors = {i: f"autor{i}" for i in range(5)}
books = {i: {"id": i, "author_id": i % 5} for i in range(20)}
db1, db2 = Db(books, authors), Db(books, authors)
ids = list(range(20))
naive = authors_naive(db1, ids)
batched = authors_batched(db2, ids)
assert naive == batched
assert db1.queries == 21
assert db2.queries == 2
print("OK")''',
         tests=['las dos versiones devuelven la misma lista de autores', 'la ingenua hace 21 consultas (1 + 20)', 'la agrupada hace 2'],
         why='Por cada libro la versión ingenua consulta a su autor, de modo que el número de consultas crece con el tamaño de la lista. Agrupar los identificadores en una sola consulta con `IN` lo reduce a dos, sin importar la longitud, que es lo que hacen DataLoader y las cargas ansiosas de los ORM.'),
    # ---- capítulo 3: control de versiones, calidad, pruebas
    dict(ch=3, lang='python', level='INTERMEDIATE',
         prompt='Escribe `git_blob_hash(content: bytes) -> str` que calcule el identificador SHA-1 que Git daría a un blob: SHA-1 de `b"blob <longitud>\\0" + contenido`. Compruébalo contra el propio comando `git hash-object` y con el blob vacío, cuyo identificador empieza por `e69de29`.',
         code='''import hashlib


def git_blob_hash(content):
    header = f"blob {len(content)}\\0".encode()
    return hashlib.sha1(header + content).hexdigest()''',
         harness='''import subprocess

assert git_blob_hash(b"") == "e69de29bb2d1d6434b8b29ae775ad8c2e48c5391"
for data in (b"hola\\n", b"x" * 1000, "acci\\u00f3n".encode()):
    real = subprocess.run(["git", "hash-object", "--stdin"], input=data, capture_output=True, check=True).stdout.decode().strip()
    assert git_blob_hash(data) == real, data
print("OK")''',
         tests=['el blob vacío es `e69de29...`', 'coincide con `git hash-object` para tres contenidos distintos'],
         why='Git es un sistema de contenido direccionable: el nombre de un objeto es el hash de su contenido más una cabecera con el tipo y el tamaño. Por eso dos ficheros idénticos comparten objeto y cualquier cambio produce otro nombre.'),
    dict(ch=3, lang='python', level='INTERMEDIATE',
         prompt='Escribe `check_property(prop, gen, runs, seed)` que ejecute una propiedad sobre `runs` entradas aleatorias y, si falla, devuelva el primer contraejemplo reducido (por ejemplo, la lista más corta que sigue fallando, eliminando elementos). Comprueba con la propiedad correcta `sorted(sorted(x)) == sorted(x)` y con la errónea "la suma de una lista es menor que 100".',
         code='''import random


def shrink(prop, value):
    changed = True
    while changed and len(value) > 0:
        changed = False
        for i in range(len(value)):
            smaller = value[:i] + value[i + 1:]
            if not prop(smaller):
                value = smaller
                changed = True
                break
    return value


def check_property(prop, gen, runs, seed):
    rng = random.Random(seed)
    for _ in range(runs):
        value = gen(rng)
        if not prop(value):
            return shrink(prop, value)
    return None''',
         harness='''def gen_list(rng):
    return [rng.randint(-50, 50) for _ in range(rng.randint(0, 20))]

assert check_property(lambda x: sorted(sorted(x)) == sorted(x), gen_list, 200, seed=1) is None
counter = check_property(lambda x: sum(x) < 100, lambda r: [r.randint(0, 60) for _ in range(r.randint(0, 10))], 500, seed=7)
assert counter is not None and sum(counter) >= 100
assert len(counter) <= 3
assert all(sum(counter[:i] + counter[i + 1:]) < 100 for i in range(len(counter)))
print("OK")''',
         tests=['una propiedad verdadera no encuentra contraejemplos', 'una falsa devuelve un contraejemplo', 'el contraejemplo está reducido: quitar cualquier elemento hace que la propiedad se cumpla'],
         why='Las pruebas basadas en propiedades generan muchas entradas y comprueban una afirmación general. Fijar la semilla hace el resultado reproducible. Reducir el contraejemplo a su mínimo facilita ver la causa: un fallo con una lista de dos elementos se entiende mejor que con una de veinte.'),
    dict(ch=3, lang='python', level='ADVANCED',
         prompt='Escribe una prueba de mutación mínima: `mutants(source)` que genere versiones del código sustituyendo un operador (`+` por `-`, `<` por `<=`, `==` por `!=`, `and` por `or`) cada vez, y `mutation_score(source, tests)` que ejecute las pruebas contra cada mutante y devuelva `(muertos, total)`. Comprueba que una batería débil deja supervivientes y una fuerte los mata.',
         code='''import ast

SWAPS = {ast.Add: ast.Sub, ast.Lt: ast.LtE, ast.Eq: ast.NotEq, ast.And: ast.Or}


def mutants(source):
    tree = ast.parse(source)
    sites = [n for n in ast.walk(tree) if isinstance(n, (ast.BinOp, ast.Compare, ast.BoolOp))]
    for index in range(len(sites)):
        copy = ast.parse(source)
        site = [n for n in ast.walk(copy) if isinstance(n, (ast.BinOp, ast.Compare, ast.BoolOp))][index]
        if isinstance(site, ast.BinOp) and type(site.op) in SWAPS:
            site.op = SWAPS[type(site.op)]()
        elif isinstance(site, ast.BoolOp) and type(site.op) in SWAPS:
            site.op = SWAPS[type(site.op)]()
        elif isinstance(site, ast.Compare) and type(site.ops[0]) in SWAPS:
            site.ops[0] = SWAPS[type(site.ops[0])]()
        else:
            continue
        yield ast.unparse(ast.fix_missing_locations(copy))


def mutation_score(source, tests):
    killed = total = 0
    for mutant in mutants(source):
        total += 1
        namespace = {}
        exec(mutant, namespace)
        try:
            tests(namespace)
        except AssertionError:
            killed += 1
    return killed, total''',
         harness='''src = """
def clamp_sum(a, b, limit):
    total = a + b
    if total < limit and total == total:
        return total
    return limit
"""
def weak(ns):
    assert ns["clamp_sum"](1, 2, 10) == 3

def strong(ns):
    f = ns["clamp_sum"]
    assert f(1, 2, 10) == 3
    assert f(8, 5, 10) == 10
    assert f(5, 5, 10) == 10
    assert f(0, 0, 10) == 0

weak_killed, total = mutation_score(src, weak)
strong_killed, total2 = mutation_score(src, strong)
assert total == total2 == 4
assert weak_killed < strong_killed
assert strong_killed >= 3
print("OK")''',
         tests=['se generan 4 mutantes del código', 'la batería débil mata menos mutantes que la fuerte', 'la fuerte mata al menos 3 de los 4'],
         why='Un mutante es una copia con un defecto introducido a propósito. Si las pruebas pasan con el mutante, no comprueban ese comportamiento. La puntuación de mutación mide la capacidad de detección de las pruebas, algo que la cobertura de líneas no mide: ejecutar una línea no es comprobar su resultado. Algunos mutantes son equivalentes (`total == total`) y no se pueden matar.'),
    # ---- capítulo 4: sistemas distribuidos
    dict(ch=4, lang='python', level='INTERMEDIATE',
         prompt='Escribe `backoff_delays(base, cap, attempts, rng)` que devuelva la lista de esperas de un reintento con retroceso exponencial y jitter completo: la espera `k` es un número aleatorio uniforme entre 0 y `min(cap, base * 2**k)`. Comprueba que cada espera respeta su techo, que no se supera `cap` y que con la misma semilla el resultado se repite.',
         code='''def backoff_delays(base, cap, attempts, rng):
    return [rng.uniform(0, min(cap, base * 2 ** k)) for k in range(attempts)]''',
         harness='''import random

delays = backoff_delays(0.1, 5.0, 8, random.Random(42))
assert len(delays) == 8
for k, d in enumerate(delays):
    assert 0 <= d <= min(5.0, 0.1 * 2 ** k), (k, d)
assert max(delays) <= 5.0
assert delays == backoff_delays(0.1, 5.0, 8, random.Random(42))
assert backoff_delays(1, 10, 0, random.Random(1)) == []
print("OK")''',
         tests=['hay una espera por intento', 'cada espera `k` es menor o igual que `min(cap, base * 2^k)`', 'ninguna supera el tope', 'la misma semilla repite el resultado', 'cero intentos da lista vacía'],
         why='El retroceso exponencial reduce la presión sobre un servicio saturado y el jitter evita que todos los clientes reintenten a la vez ("efecto manada"). Pasar el generador aleatorio como parámetro hace la función determinista para las pruebas.'),
    dict(ch=4, lang='python', level='INTERMEDIATE',
         prompt='Implementa `CircuitBreaker(threshold, reset_after, clock)` con `call(fn)`: tras `threshold` fallos seguidos se abre y lanza `CircuitOpen` sin llamar a `fn`; pasado `reset_after` segundos permite una llamada de prueba (semiabierto) y se cierra si tiene éxito o se reabre si falla. Comprueba los estados con un reloj controlado.',
         code='''class CircuitOpen(Exception):
    pass


class CircuitBreaker:
    def __init__(self, threshold, reset_after, clock):
        self.threshold = threshold
        self.reset_after = reset_after
        self.clock = clock
        self.failures = 0
        self.opened_at = None

    def call(self, fn):
        if self.opened_at is not None:
            if self.clock() - self.opened_at < self.reset_after:
                raise CircuitOpen("circuito abierto")
        try:
            result = fn()
        except Exception:
            self.failures += 1
            if self.failures >= self.threshold or self.opened_at is not None:
                self.opened_at = self.clock()
            raise
        self.failures = 0
        self.opened_at = None
        return result''',
         harness='''now = [0.0]
breaker = CircuitBreaker(2, 10, lambda: now[0])
calls = []

def boom():
    calls.append(1)
    raise RuntimeError("falla")

for _ in range(2):
    try:
        breaker.call(boom)
    except RuntimeError:
        pass
try:
    breaker.call(boom)
except CircuitOpen:
    pass
else:
    raise AssertionError("debe estar abierto")
assert len(calls) == 2
now[0] = 11
assert breaker.call(lambda: "ok") == "ok"
assert breaker.opened_at is None
now[0] = 12
for _ in range(2):
    try:
        breaker.call(boom)
    except RuntimeError:
        pass
now[0] = 25
try:
    breaker.call(boom)
except RuntimeError:
    pass
try:
    breaker.call(lambda: "x")
except CircuitOpen:
    print("OK")''',
         tests=['tras 2 fallos el circuito se abre y no llama a la función', 'pasado el tiempo una llamada de prueba con éxito lo cierra', 'una llamada de prueba que falla lo reabre'],
         why='Un cortacircuitos evita seguir llamando a un servicio que está fallando, lo que da tiempo a recuperarse y libera recursos del cliente. El estado semiabierto prueba con una sola llamada antes de volver a la normalidad.'),
    dict(ch=4, lang='python', level='ADVANCED',
         prompt='Escribe `grant_vote(state, request)` para la elección de líder de Raft. `state` es `{"term", "voted_for", "last_log_term", "last_log_index"}` y `request` es `{"term", "candidate", "last_log_term", "last_log_index"}`. Devuelve `(concedido, nuevo_estado)`: se concede si el término del candidato no es menor, no se ha votado a otro en ese término y su registro está al menos tan actualizado. Comprueba las reglas.',
         code='''def grant_vote(state, request):
    new = dict(state)
    if request["term"] < state["term"]:
        return False, new
    if request["term"] > state["term"]:
        new["term"] = request["term"]
        new["voted_for"] = None
    up_to_date = (request["last_log_term"], request["last_log_index"]) >= (state["last_log_term"], state["last_log_index"])
    if new["voted_for"] in (None, request["candidate"]) and up_to_date:
        new["voted_for"] = request["candidate"]
        return True, new
    return False, new''',
         harness='''base = {"term": 3, "voted_for": None, "last_log_term": 2, "last_log_index": 5}
ok, st = grant_vote(base, {"term": 3, "candidate": "B", "last_log_term": 2, "last_log_index": 5})
assert ok and st["voted_for"] == "B"
ok, _ = grant_vote(st, {"term": 3, "candidate": "C", "last_log_term": 2, "last_log_index": 9})
assert not ok
ok, _ = grant_vote(st, {"term": 3, "candidate": "B", "last_log_term": 2, "last_log_index": 5})
assert ok
ok, _ = grant_vote(base, {"term": 2, "candidate": "D", "last_log_term": 9, "last_log_index": 99})
assert not ok
ok, _ = grant_vote(base, {"term": 4, "candidate": "E", "last_log_term": 1, "last_log_index": 99})
assert not ok
ok, st = grant_vote(base, {"term": 4, "candidate": "F", "last_log_term": 3, "last_log_index": 1})
assert ok and st["term"] == 4 and st["voted_for"] == "F"
assert base["voted_for"] is None
print("OK")''',
         tests=['se vota a un candidato con el registro al día', 'no se vota a un segundo candidato en el mismo término', 'se puede repetir el voto al mismo candidato', 'un término anterior se rechaza', 'un candidato con el registro menos actualizado se rechaza aunque tenga mayor término', 'el estado original no se modifica'],
         why='Cada nodo vota como mucho una vez por término, y solo a candidatos cuyo registro sea al menos tan actualizado como el suyo, comparando primero el término de la última entrada y luego el índice. Esa regla impide que un nodo que ha perdido entradas confirmadas llegue a ser líder.'),
    # ---- capítulo 5: seguridad
    dict(ch=5, lang='python', level='INTERMEDIATE',
         prompt='Escribe `hash_password(password)` y `verify_password(password, stored)` con `hashlib.scrypt` o `hashlib.pbkdf2_hmac`, sal aleatoria de `secrets.token_bytes` y comparación en tiempo constante. El formato guardado debe incluir parámetros, sal y hash. Comprueba que dos hashes de la misma clave difieren, que la verificación funciona y que una clave incorrecta falla.',
         code='''import base64
import hashlib
import hmac
import secrets


def hash_password(password, iterations=200_000):
    salt = secrets.token_bytes(16)
    digest = hashlib.pbkdf2_hmac("sha256", password.encode(), salt, iterations)
    b64 = lambda data: base64.b64encode(data).decode()
    return f"pbkdf2_sha256${iterations}${b64(salt)}${b64(digest)}"


def verify_password(password, stored):
    try:
        scheme, iterations, salt, digest = stored.split("$")
        if scheme != "pbkdf2_sha256":
            return False
        candidate = hashlib.pbkdf2_hmac("sha256", password.encode(), base64.b64decode(salt), int(iterations))
        return hmac.compare_digest(candidate, base64.b64decode(digest))
    except (ValueError, TypeError):
        return False''',
         harness='''a = hash_password("correcto")
b = hash_password("correcto")
assert a != b
assert verify_password("correcto", a)
assert verify_password("correcto", b)
assert not verify_password("incorrecto", a)
assert not verify_password("correcto", "basura")
assert not verify_password("correcto", a.replace("pbkdf2_sha256", "md5"))
assert a.startswith("pbkdf2_sha256$200000$")
print("OK")''',
         tests=['dos hashes de la misma clave son distintos (sal aleatoria)', 'la clave correcta verifica', 'una clave incorrecta no verifica', 'un formato inválido devuelve `False`'],
         why='Una función de derivación lenta y con sal obliga a un atacante a trabajar por contraseña y por usuario. Guardar los parámetros con el hash permite aumentar las iteraciones en el futuro y seguir verificando los antiguos. Nunca se debe usar un hash rápido como SHA-256 solo.'),
    dict(ch=5, lang='python', level='FOUNDATIONAL',
         prompt='Escribe `find_user(conn, name)` con una consulta parametrizada de `sqlite3` que no sea vulnerable a inyección SQL. Comprueba que `"ana"` devuelve su fila y que la entrada maliciosa `"x\' OR \'1\'=\'1"` no devuelve ninguna fila, frente a una versión con formato de cadenas que sí la devolvería.',
         code='''def find_user(conn, name):
    return conn.execute("SELECT id, name FROM users WHERE name = ?", (name,)).fetchall()''',
         harness='''import sqlite3

conn = sqlite3.connect(":memory:")
conn.execute("CREATE TABLE users(id INTEGER, name TEXT)")
conn.executemany("INSERT INTO users VALUES (?, ?)", [(1, "ana"), (2, "luis")])
assert find_user(conn, "ana") == [(1, "ana")]
attack = "x' OR '1'='1"
assert find_user(conn, attack) == []
vulnerable = conn.execute(f"SELECT id, name FROM users WHERE name = '{attack}'").fetchall()
assert len(vulnerable) == 2
print("OK")''',
         tests=['`"ana"` devuelve su fila', 'la entrada maliciosa no devuelve filas con la consulta parametrizada', 'la versión con formato de cadenas devuelve todas las filas (demuestra la vulnerabilidad)'],
         why='Con parámetros, el motor recibe la consulta y los datos por separado y nunca interpreta los datos como SQL. Construir la consulta concatenando texto permite que la entrada cambie su estructura, que es la inyección SQL.'),
    dict(ch=5, lang='python', level='INTERMEDIATE',
         prompt='Escribe `safe_join(base, user_path)` que combine una ruta base con una ruta aportada por el usuario y lance `ValueError` si el resultado se sale del directorio base (por ejemplo con `..` o una ruta absoluta), usando `pathlib`. Comprueba rutas válidas y varios intentos de salto de directorio.',
         code='''from pathlib import Path


def safe_join(base, user_path):
    base_path = Path(base).resolve()
    target = (base_path / user_path).resolve()
    if base_path != target and base_path not in target.parents:
        raise ValueError("ruta fuera del directorio base")
    return target''',
         harness='''import tempfile
from pathlib import Path

with tempfile.TemporaryDirectory() as tmp:
    base = Path(tmp).resolve()
    assert safe_join(base, "a/b.txt") == base / "a" / "b.txt"
    assert safe_join(base, "a/../c.txt") == base / "c.txt"
    for bad in ["../secreto", "a/../../secreto", "/etc/passwd", "..", "a/../.."]:
        try:
            safe_join(base, bad)
        except ValueError:
            continue
        raise AssertionError(bad)
    assert safe_join(base, ".") == base
print("OK")''',
         tests=['`a/b.txt` queda dentro de la base', '`a/../c.txt` se normaliza y queda dentro', '`../secreto`, `/etc/passwd`, `..` y similares lanzan `ValueError`', 'la propia base es válida'],
         why='Hay que resolver la ruta final (eliminando `..` y enlaces simbólicos) antes de comprobar que sigue dentro de la base; comprobar el texto de la ruta de entrada no basta. Una ruta absoluta sustituye a la base al unir con `/`, por eso se comprueba el resultado.'),
    # ---- capítulo 6: infraestructura
    dict(ch=6, lang='python', level='INTERMEDIATE',
         prompt='Escribe `lint_deployment(manifest)` que reciba un diccionario con un Deployment de Kubernetes y devuelva la lista de problemas: imagen con etiqueta `latest` o sin etiqueta, contenedor sin `resources.limits`, contenedor que se ejecuta como root (`securityContext.runAsNonRoot` distinto de `True`) y menos de 2 réplicas. Devuelve `[]` si todo está bien.',
         code='''def lint_deployment(manifest):
    problems = []
    spec = manifest.get("spec", {})
    if spec.get("replicas", 1) < 2:
        problems.append("menos de 2 replicas")
    for c in spec.get("template", {}).get("spec", {}).get("containers", []):
        name = c.get("name", "?")
        image = c.get("image", "")
        tag = image.rsplit(":", 1)[1] if ":" in image.rsplit("/", 1)[-1] else ""
        if tag in ("", "latest"):
            problems.append(f"{name}: imagen sin version fija")
        if "limits" not in c.get("resources", {}):
            problems.append(f"{name}: sin resources.limits")
        if c.get("securityContext", {}).get("runAsNonRoot") is not True:
            problems.append(f"{name}: puede ejecutarse como root")
    return problems''',
         harness='''good = {"spec": {"replicas": 3, "template": {"spec": {"containers": [
    {"name": "web", "image": "registry.local/web:1.4.2", "resources": {"limits": {"cpu": "500m"}},
     "securityContext": {"runAsNonRoot": True}}]}}}}
assert lint_deployment(good) == []
bad = {"spec": {"replicas": 1, "template": {"spec": {"containers": [{"name": "app", "image": "nginx"}]}}}}
assert lint_deployment(bad) == ["menos de 2 replicas", "app: imagen sin version fija", "app: sin resources.limits", "app: puede ejecutarse como root"]
latest = {"spec": {"replicas": 2, "template": {"spec": {"containers": [
    {"name": "a", "image": "x/y:latest", "resources": {"limits": {}}, "securityContext": {"runAsNonRoot": True}}]}}}}
assert lint_deployment(latest) == ["a: imagen sin version fija"]
assert lint_deployment({}) == ["menos de 2 replicas"]
print("OK")''',
         tests=['un despliegue correcto no da problemas', 'un despliegue con cuatro defectos da los cuatro mensajes', 'la etiqueta `latest` se detecta', 'una imagen de un registro con puerto no se confunde con una etiqueta'],
         why='Fijar la versión de la imagen hace los despliegues reproducibles; los límites de recursos evitan que un contenedor agote el nodo; ejecutar sin root reduce el daño de una intrusión; y al menos dos réplicas permiten actualizar sin cortar el servicio. Son reglas de política, no garantías de seguridad.'),
    dict(ch=6, lang='python', level='ADVANCED',
         prompt='Escribe `rolling_update(replicas, max_surge, max_unavailable)` que simule una actualización gradual de Kubernetes y devuelva la lista de pasos `(nuevas, antiguas)`. En cada paso se pueden crear hasta `max_surge` pods nuevos por encima de `replicas` y retirar antiguos sin que los disponibles bajen de `replicas - max_unavailable`. Comprueba que nunca hay menos disponibles de lo permitido ni más pods de `replicas + max_surge`, y que termina en `(replicas, 0)`.',
         code='''def rolling_update(replicas, max_surge, max_unavailable):
    new, old = 0, replicas
    steps = [(new, old)]
    while old > 0 or new < replicas:
        # Crear pods nuevos sin pasar del techo de pods totales.
        new += min(replicas - new, replicas + max_surge - (new + old))
        # Retirar antiguos sin bajar del minimo de pods disponibles.
        old -= min(old, new + old - (replicas - max_unavailable))
        steps.append((new, old))
        if len(steps) > 1000:
            raise RuntimeError("la actualizacion no progresa")
    return steps''',
         harness='''for replicas, surge, unavailable in [(10, 2, 2), (4, 1, 0), (6, 0, 1), (1, 1, 0), (5, 3, 3)]:
    steps = rolling_update(replicas, surge, unavailable)
    assert steps[0] == (0, replicas) and steps[-1] == (replicas, 0)
    for new, old in steps:
        assert new + old <= replicas + surge, (replicas, surge, unavailable, new, old)
        assert new + old >= replicas - unavailable, (replicas, surge, unavailable, new, old)
        assert new >= 0 and old >= 0
    assert all(b[0] >= a[0] and b[1] <= a[1] for a, b in zip(steps, steps[1:]))
print("OK")''',
         tests=['empieza en `(0, replicas)` y termina en `(replicas, 0)`', 'nunca hay más de `replicas + max_surge` pods', 'nunca hay menos de `replicas - max_unavailable` disponibles', 'los pods nuevos solo aumentan y los antiguos solo disminuyen', 'probado con cinco configuraciones'],
         why='La actualización alterna crear pods nuevos, limitado por `max_surge`, y retirar antiguos, limitado por `max_unavailable`. Si ambos fuesen 0 el proceso no podría avanzar. La prueba comprueba las dos invariantes en cada paso, que es lo que garantiza que el servicio no se interrumpe.'),
    dict(ch=6, lang='python', level='INTERMEDIATE',
         prompt='Escribe `lint_dockerfile(text)` que devuelva los problemas de un Dockerfile: `FROM` sin etiqueta fija o con `latest`, ausencia de `USER` no root antes del último `CMD`/`ENTRYPOINT`, `RUN apt-get install` sin `--no-install-recommends` y `ADD` cuando bastaría `COPY` (origen que no es una URL ni un `.tar`). Comprueba un fichero correcto y otro con defectos.',
         code='''import re


def lint_dockerfile(text):
    problems = []
    lines = [l.strip() for l in text.splitlines() if l.strip() and not l.strip().startswith("#")]
    user = None
    for number, line in enumerate(lines, 1):
        keyword, _, rest = line.partition(" ")
        keyword = keyword.upper()
        if keyword == "FROM":
            image = rest.split()[0]
            tag = image.rsplit(":", 1)[1] if ":" in image.rsplit("/", 1)[-1] else ""
            if tag in ("", "latest"):
                problems.append(f"linea {number}: FROM sin version fija")
        elif keyword == "USER":
            user = rest.strip()
        elif keyword == "RUN" and "apt-get install" in rest and "--no-install-recommends" not in rest:
            problems.append(f"linea {number}: falta --no-install-recommends")
        elif keyword == "ADD":
            source = rest.split()[0]
            if not (re.match(r"https?://", source) or source.endswith((".tar", ".tar.gz", ".tgz"))):
                problems.append(f"linea {number}: usa COPY en lugar de ADD")
    if user in (None, "root", "0"):
        problems.append("falta USER no root")
    return problems''',
         harness='''good = """
FROM python:3.12-slim
RUN apt-get update && apt-get install -y --no-install-recommends curl
COPY app /app
USER 1000
CMD ["python", "/app/main.py"]
"""
assert lint_dockerfile(good) == []
bad = """
FROM ubuntu
ADD app /app
RUN apt-get install -y curl
CMD ["/app/run"]
"""
assert lint_dockerfile(bad) == [
    "linea 1: FROM sin version fija",
    "linea 2: usa COPY en lugar de ADD",
    "linea 3: falta --no-install-recommends",
    "falta USER no root",
]
assert lint_dockerfile("FROM x:1\\nADD https://e.com/a.tgz /a\\nUSER app") == []
assert lint_dockerfile("FROM debian:latest\\nUSER root") == ["linea 1: FROM sin version fija", "falta USER no root"]
print("OK")''',
         tests=['un Dockerfile correcto no da problemas', 'un Dockerfile con cuatro defectos los da todos con su línea', '`ADD` de una URL o un `.tgz` es válido', '`USER root` cuenta como ausencia de usuario no root'],
         why='Una imagen reproducible fija la versión base; un contenedor no debe ejecutarse como root; evitar paquetes recomendados reduce tamaño y superficie; y `COPY` es más predecible que `ADD`, que además descomprime y descarga. Son reglas de higiene que se pueden comprobar automáticamente en la integración continua.'),
    # ---- capítulo 7: proyectos integradores
    dict(ch=7, lang='python', level='ADVANCED',
         prompt='Proyecto: un almacén clave-valor persistente `KV(path)` con `put`, `get`, `delete`, registro en un fichero de líneas JSON, recuperación al abrir (ignorando una última línea truncada) y `compact()` que reescriba el fichero con solo el estado vivo. Comprueba persistencia entre aperturas, borrados, corte a medias y compactación.',
         code='''import json
import os


class KV:
    def __init__(self, path):
        self.path = path
        self.data = {}
        if os.path.exists(path):
            with open(path, encoding="utf-8") as handle:
                for line in handle:
                    if not line.endswith("\\n"):
                        break
                    record = json.loads(line)
                    if record["op"] == "put":
                        self.data[record["k"]] = record["v"]
                    else:
                        self.data.pop(record["k"], None)

    def _append(self, record):
        with open(self.path, "a", encoding="utf-8") as handle:
            handle.write(json.dumps(record) + "\\n")

    def put(self, key, value):
        self._append({"op": "put", "k": key, "v": value})
        self.data[key] = value

    def get(self, key, default=None):
        return self.data.get(key, default)

    def delete(self, key):
        self._append({"op": "del", "k": key})
        self.data.pop(key, None)

    def compact(self):
        tmp = self.path + ".tmp"
        with open(tmp, "w", encoding="utf-8") as handle:
            for key, value in self.data.items():
                handle.write(json.dumps({"op": "put", "k": key, "v": value}) + "\\n")
        os.replace(tmp, self.path)''',
         harness='''import os
import tempfile

with tempfile.TemporaryDirectory() as tmp:
    path = os.path.join(tmp, "kv.log")
    kv = KV(path)
    kv.put("a", 1)
    kv.put("b", [1, 2])
    kv.put("a", 3)
    kv.delete("b")
    assert kv.get("a") == 3 and kv.get("b") is None
    reopened = KV(path)
    assert reopened.data == {"a": 3}
    size_before = os.path.getsize(path)
    reopened.compact()
    assert os.path.getsize(path) < size_before
    assert KV(path).data == {"a": 3}
    with open(path, "a", encoding="utf-8") as handle:
        handle.write('{"op": "put", "k": "z", "v"')
    assert KV(path).data == {"a": 3}
print("OK")''',
         tests=['los datos persisten al reabrir', 'un borrado persiste', 'la compactación reduce el tamaño y conserva el estado', 'una última línea truncada se ignora'],
         why='Un registro de solo añadir es simple y robusto: cada operación es una línea completa. Al abrir se reproduce el registro; una línea sin salto final indica un corte durante la escritura y se descarta. `os.replace` hace la sustitución atómica al compactar.'),
    dict(ch=7, lang='python', level='INTERMEDIATE',
         prompt='Proyecto: una aplicación de línea de comandos con `argparse`. Escribe `build_parser()` con subcomandos `add TEXTO`, `done ID` y `list [--all]`, y `run(argv, store)` que ejecute el subcomando sobre una lista de tareas y devuelva el texto que se imprimiría. Comprueba añadir, completar, listar y los errores (identificador inexistente).',
         code='''import argparse


def build_parser():
    parser = argparse.ArgumentParser(prog="todo")
    sub = parser.add_subparsers(dest="command", required=True)
    add = sub.add_parser("add")
    add.add_argument("text")
    done = sub.add_parser("done")
    done.add_argument("id", type=int)
    listing = sub.add_parser("list")
    listing.add_argument("--all", action="store_true")
    return parser


def run(argv, store):
    args = build_parser().parse_args(argv)
    if args.command == "add":
        store.append({"id": len(store) + 1, "text": args.text, "done": False})
        return f"anadida {len(store)}"
    if args.command == "done":
        for task in store:
            if task["id"] == args.id:
                task["done"] = True
                return f"hecha {args.id}"
        return f"error: no existe {args.id}"
    lines = [f"{t['id']}. [{'x' if t['done'] else ' '}] {t['text']}" for t in store if args.all or not t["done"]]
    return "\\n".join(lines)''',
         harness='''store = []
assert run(["add", "comprar pan"], store) == "anadida 1"
assert run(["add", "llamar"], store) == "anadida 2"
assert run(["list"], store) == "1. [ ] comprar pan\\n2. [ ] llamar"
assert run(["done", "1"], store) == "hecha 1"
assert run(["list"], store) == "2. [ ] llamar"
assert run(["list", "--all"], store) == "1. [x] comprar pan\\n2. [ ] llamar"
assert run(["done", "9"], store) == "error: no existe 9"
for bad in (["borrar"], ["done", "x"], []):
    try:
        run(bad, [])
    except SystemExit as exit_:
        assert exit_.code == 2
    else:
        raise AssertionError(bad)
print("OK")''',
         tests=['`add` anade tareas con identificador creciente', '`list` muestra solo las pendientes y `list --all` todas', '`done` marca como hecha', 'un identificador inexistente da un mensaje de error', 'un subcomando desconocido o un argumento no numérico sale con código 2'],
         why='Separar el análisis de argumentos (`build_parser`) de la lógica (`run`) permite probar la aplicación sin lanzar procesos. `argparse` valida los tipos y termina con código 2 ante un uso incorrecto, como hacen las herramientas estándar.'),
    dict(ch=7, lang='python', level='ADVANCED',
         prompt='Proyecto: un libro contable por partida doble con registro de eventos. `Ledger` con `post(entries)` (lista de `(cuenta, débito, crédito)` que debe sumar lo mismo en débito y crédito, si no `ValueError` sin cambiar nada), `balance(account)` y `replay(events)` que reconstruya el libro desde el registro. Comprueba el cuadre, el rechazo de un asiento descuadrado y la reconstrucción.',
         code='''class Ledger:
    def __init__(self):
        self.events = []
        self.balances = {}

    def post(self, entries):
        debit = sum(d for _, d, _ in entries)
        credit = sum(c for _, _, c in entries)
        if debit != credit or debit == 0:
            raise ValueError("asiento descuadrado")
        self.events.append(list(entries))
        for account, d, c in entries:
            self.balances[account] = self.balances.get(account, 0) + d - c

    def balance(self, account):
        return self.balances.get(account, 0)

    @staticmethod
    def replay(events):
        ledger = Ledger()
        for entries in events:
            ledger.post(entries)
        return ledger''',
         harness='''ledger = Ledger()
ledger.post([("caja", 100, 0), ("capital", 0, 100)])
ledger.post([("compras", 30, 0), ("caja", 0, 30)])
assert ledger.balance("caja") == 70
assert ledger.balance("compras") == 30
assert ledger.balance("capital") == -100
assert sum(ledger.balances.values()) == 0
before = dict(ledger.balances)
try:
    ledger.post([("caja", 10, 0), ("capital", 0, 5)])
except ValueError:
    pass
else:
    raise AssertionError("debe rechazar")
assert ledger.balances == before and len(ledger.events) == 2
rebuilt = Ledger.replay(ledger.events)
assert rebuilt.balances == ledger.balances
try:
    ledger.post([])
except ValueError:
    print("OK")''',
         tests=['los saldos reflejan los asientos', 'la suma de todos los saldos es 0', 'un asiento descuadrado se rechaza sin cambiar nada', 'reproducir el registro reconstruye los saldos', 'un asiento vacío se rechaza'],
         why='En la partida doble cada asiento suma lo mismo en el debe y en el haber, así que la suma de todos los saldos es siempre 0: es un invariante que detecta errores. Guardar los eventos y derivar el estado (event sourcing) permite auditar y reconstruir el libro.'),
]
