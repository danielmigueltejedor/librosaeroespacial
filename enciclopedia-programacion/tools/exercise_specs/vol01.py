"""Programming exercises of volume 1 (history and foundations). Each reference program runs with the real interpreter."""

EXERCISES = [
    # ---- capítulo 1: computabilidad
    dict(ch=1, lang='python', level='INTERMEDIATE',
         prompt='Escribe `run_tm(rules, tape, state, halt)` que simule una máquina de Turing: `rules` es un diccionario `(estado, símbolo) -> (nuevo_estado, símbolo_escrito, movimiento)` con movimiento `"L"` o `"R"`, la cinta es una cadena y el símbolo en blanco es `"_"`. Devuelve la cinta final (sin blancos de los extremos) al llegar al estado `halt`. Comprueba una máquina que suma 1 a un número binario.',
         code='''def run_tm(rules, tape, state, halt, max_steps=10_000):
    cells = dict(enumerate(tape))
    head = len(tape) - 1
    for _ in range(max_steps):
        if state == halt:
            low, high = min(cells), max(cells)
            return "".join(cells.get(i, "_") for i in range(low, high + 1)).strip("_")
        symbol = cells.get(head, "_")
        state, write, move = rules[(state, symbol)]
        cells[head] = write
        head += 1 if move == "R" else -1
    raise RuntimeError("la maquina no se detiene")''',
         harness='''increment = {
    ("carry", "1"): ("carry", "0", "L"),
    ("carry", "0"): ("done", "1", "L"),
    ("carry", "_"): ("done", "1", "L"),
}
assert run_tm(increment, "1011", "carry", "done") == "1100"
assert run_tm(increment, "111", "carry", "done") == "1000"
assert run_tm(increment, "0", "carry", "done") == "1"
assert run_tm(increment, "", "carry", "done") == "1"
try:
    run_tm({("a", "_"): ("a", "_", "R")}, "", "a", "stop", max_steps=50)
except RuntimeError:
    print("OK")''',
         tests=['`1011` más 1 es `1100`', '`111` más 1 es `1000`', 'una máquina que no se detiene lanza `RuntimeError` en lugar de colgarse'],
         why='Una máquina de Turing es un conjunto de reglas, una cinta y un cabezal; con eso se puede expresar cualquier algoritmo. El límite de pasos es imprescindible: decidir si una máquina cualquiera se detiene es imposible (problema de la parada), así que un simulador no puede saberlo de antemano.'),
    dict(ch=1, lang='python', level='INTERMEDIATE',
         prompt='Implementa los numerales de Church solo con funciones (sin enteros en la representación): `church(n)`, `to_int(c)`, `succ`, `add`, `mul` y `power`. Comprueba `add(church(2), church(3))`, `mul` y `power`.',
         code='''def church(n):
    def numeral(f):
        def apply(x):
            for _ in range(n):
                x = f(x)
            return x
        return apply
    return numeral


def to_int(c):
    return c(lambda k: k + 1)(0)


succ = lambda n: lambda f: lambda x: f(n(f)(x))
add = lambda m, n: lambda f: lambda x: m(f)(n(f)(x))
mul = lambda m, n: lambda f: m(n(f))
power = lambda m, n: n(m)''',
         harness='''two, three = church(2), church(3)
assert to_int(church(0)) == 0
assert to_int(succ(two)) == 3
assert to_int(add(two, three)) == 5
assert to_int(mul(two, three)) == 6
assert to_int(power(two, three)) == 8
assert to_int(power(three, church(0))) == 1
assert to_int(mul(church(0), three)) == 0
print("OK")''',
         tests=['`succ(2)` es 3', '`add(2, 3)` es 5', '`mul(2, 3)` es 6', '`power(2, 3)` es 8', 'cualquier número elevado a 0 es 1'],
         why='En el cálculo lambda un número es "aplicar una función n veces". Con eso se definen la suma, el producto y la potencia sin tipos primitivos: es la prueba de que la abstracción y la aplicación de funciones bastan para calcular.'),
    dict(ch=1, lang='python', level='FOUNDATIONAL',
         prompt='Escribe `equivalent(expr_a, expr_b, variables)` que decida si dos expresiones booleanas (cadenas Python con `and`, `or`, `not`) son equivalentes probando las `2**n` asignaciones de verdad. Comprueba las leyes de De Morgan, la absorción y un par que no es equivalente.',
         code='''from itertools import product


def equivalent(expr_a, expr_b, variables):
    for values in product([False, True], repeat=len(variables)):
        env = dict(zip(variables, values))
        if eval(expr_a, {}, env) != eval(expr_b, {}, env):
            return False
    return True''',
         harness='''assert equivalent("not (a and b)", "(not a) or (not b)", ["a", "b"])
assert equivalent("not (a or b)", "(not a) and (not b)", ["a", "b"])
assert equivalent("a or (a and b)", "a", ["a", "b"])
assert equivalent("a and (b or c)", "(a and b) or (a and c)", ["a", "b", "c"])
assert not equivalent("a and b", "a or b", ["a", "b"])
assert not equivalent("not (a and b)", "(not a) and (not b)", ["a", "b"])
print("OK")''',
         tests=['De Morgan para la conjunción y la disyunción', 'ley de absorción', 'distributividad con tres variables', '`a and b` no equivale a `a or b`'],
         why='Con `n` variables hay `2^n` combinaciones, así que la comprobación exhaustiva es una demostración válida para pocas variables y un método inviable para muchas. Es la razón de que decidir la satisfacibilidad de una fórmula sea el problema NP-completo clásico.'),
    # ---- capítulo 2: primeros ordenadores y compiladores
    dict(ch=2, lang='python', level='INTERMEDIATE',
         prompt='Escribe un ensamblador y una máquina mínimos: `assemble(text)` convierte líneas como `LOAD 5`, `ADD 3`, `JNZ etiqueta` y `etiqueta:` en una lista de instrucciones, y `run(program)` las ejecuta sobre un acumulador y devuelve su valor final al llegar a `HALT`. Escribe con ellas un programa que cuente de 5 a 0. Comprueba también `LOAD 2`, `ADD 3`.',
         code='''def assemble(text):
    labels, lines = {}, []
    for raw in text.splitlines():
        line = raw.split(";")[0].strip()
        if not line:
            continue
        if line.endswith(":"):
            labels[line[:-1]] = len(lines)
        else:
            lines.append(line.split())
    program = []
    for op, *args in lines:
        arg = args[0] if args else None
        if arg is not None and arg in labels:
            arg = labels[arg]
        elif arg is not None:
            arg = int(arg)
        program.append((op, arg))
    return program


def run(program, max_steps=100_000):
    acc, pc = 0, 0
    for _ in range(max_steps):
        op, arg = program[pc]
        pc += 1
        if op == "LOAD":
            acc = arg
        elif op == "ADD":
            acc += arg
        elif op == "JNZ":
            if acc != 0:
                pc = arg
        elif op == "HALT":
            return acc
        else:
            raise ValueError(f"instruccion desconocida: {op}")
    raise RuntimeError("demasiados pasos")''',
         harness='''assert run(assemble("LOAD 2\\nADD 3\\nHALT")) == 5
countdown = """
    LOAD 5
loop:
    ADD -1      ; resta 1
    JNZ loop
    HALT
"""
assert assemble(countdown)[2] == ("JNZ", 1)
assert run(assemble(countdown)) == 0
try:
    run(assemble("LOAD 1\\nloop:\\nJNZ loop"), max_steps=100)
except RuntimeError:
    pass
else:
    raise AssertionError("bucle infinito")
try:
    run(assemble("BOOM 1"))
except ValueError:
    print("OK")''',
         tests=['`LOAD 2`, `ADD 3`, `HALT` da 5', 'la cuenta atrás termina en 0', 'la etiqueta `loop` se traduce a la posición de su instrucción', 'un bucle infinito lanza `RuntimeError`', 'una instrucción desconocida lanza `ValueError`'],
         why='Un ensamblador traduce nombres simbólicos a direcciones: así los saltos usan etiquetas en lugar de números de línea. La máquina ejecuta el ciclo de buscar, decodificar y ejecutar; el contador de programa avanza salvo que un salto lo cambie.'),
    dict(ch=2, lang='python', level='INTERMEDIATE',
         prompt='Escribe un compilador de expresiones aritméticas a una máquina de pila: `compile_expr(text)` devuelve la lista de instrucciones (`("PUSH", n)`, `("ADD",)`, `("SUB",)`, `("MUL",)`, `("DIV",)`) respetando la precedencia y los paréntesis (algoritmo de las vías de tren), y `execute(code)` las ejecuta. Comprueba `2 + 3 * 4`, `(2 + 3) * 4` y `10 - 4 - 3`.',
         code='''import re

PRECEDENCE = {"+": 1, "-": 1, "*": 2, "/": 2}
OPS = {"+": "ADD", "-": "SUB", "*": "MUL", "/": "DIV"}


def compile_expr(text):
    out, stack = [], []
    for token in re.findall(r"\\d+|[-+*/()]", text):
        if token.isdigit():
            out.append(("PUSH", int(token)))
        elif token in PRECEDENCE:
            while stack and stack[-1] in PRECEDENCE and PRECEDENCE[stack[-1]] >= PRECEDENCE[token]:
                out.append((OPS[stack.pop()],))
            stack.append(token)
        elif token == "(":
            stack.append(token)
        else:
            while stack[-1] != "(":
                out.append((OPS[stack.pop()],))
            stack.pop()
    while stack:
        out.append((OPS[stack.pop()],))
    return out


def execute(code):
    stack = []
    for op, *arg in code:
        if op == "PUSH":
            stack.append(arg[0])
            continue
        b, a = stack.pop(), stack.pop()
        stack.append({"ADD": a + b, "SUB": a - b, "MUL": a * b, "DIV": a // b if b else 0}[op])
    return stack[0]''',
         harness='''assert execute(compile_expr("2 + 3 * 4")) == 14
assert execute(compile_expr("(2 + 3) * 4")) == 20
assert execute(compile_expr("10 - 4 - 3")) == 3
assert execute(compile_expr("100 / 5 / 4")) == 5
assert compile_expr("2 + 3 * 4") == [("PUSH", 2), ("PUSH", 3), ("PUSH", 4), ("MUL",), ("ADD",)]
assert execute(compile_expr("((7))")) == 7
print("OK")''',
         tests=['`2 + 3 * 4` es 14', '`(2 + 3) * 4` es 20', '`10 - 4 - 3` es 3 (asociatividad por la izquierda)', 'la salida respeta la precedencia'],
         why='La notación postfija no necesita paréntesis ni reglas de precedencia al ejecutarse: cada operador toma los dos valores superiores de la pila. El algoritmo de las vías de tren retiene los operadores de menor precedencia hasta que llegan los de mayor, y usar `>=` hace que la resta se asocie por la izquierda.'),
    dict(ch=2, lang='python', level='ADVANCED',
         prompt='Escribe un intérprete mínimo de Lisp: `parse(text)` convierte una expresión S en listas anidadas y `evaluate(expr, env=None)` soporta números, `+ - * /`, `if`, `define`, `lambda` y llamadas. Comprueba `(+ 1 (* 2 3))`, una función recursiva `fact` y que una clausura recuerda su entorno.',
         code='''import operator


def parse(text):
    tokens = text.replace("(", " ( ").replace(")", " ) ").split()

    def read(pos):
        token = tokens[pos]
        if token == "(":
            items, pos = [], pos + 1
            while tokens[pos] != ")":
                item, pos = read(pos)
                items.append(item)
            return items, pos + 1
        try:
            return int(token), pos + 1
        except ValueError:
            return token, pos + 1

    return read(0)[0]


def evaluate(expr, env=None):
    env = env if env is not None else {"+": operator.add, "-": operator.sub, "*": operator.mul, "/": operator.floordiv, "<": operator.lt, "=": operator.eq}
    if isinstance(expr, str):
        return env[expr]
    if isinstance(expr, int):
        return expr
    head = expr[0]
    if head == "if":
        return evaluate(expr[2] if evaluate(expr[1], env) else expr[3], env)
    if head == "define":
        env[expr[1]] = evaluate(expr[2], env)
        return None
    if head == "lambda":
        params, body = expr[1], expr[2]
        return lambda *args: evaluate(body, {**env, **dict(zip(params, args))})
    function = evaluate(head, env)
    return function(*[evaluate(arg, env) for arg in expr[1:]])''',
         harness='''assert parse("(+ 1 (* 2 3))") == ["+", 1, ["*", 2, 3]]
assert evaluate(parse("(+ 1 (* 2 3))")) == 7
env = {"+": lambda a, b: a + b, "*": lambda a, b: a * b, "-": lambda a, b: a - b, "<": lambda a, b: a < b, "=": lambda a, b: a == b}
evaluate(parse("(define fact (lambda (n) (if (< n 2) 1 (* n (fact (- n 1))))))"), env)
assert evaluate(parse("(fact 5)"), env) == 120
evaluate(parse("(define make-adder (lambda (n) (lambda (x) (+ x n))))"), env)
evaluate(parse("(define add5 (make-adder 5))"), env)
assert evaluate(parse("(add5 10)"), env) == 15
assert evaluate(parse("(if (= 1 2) 10 20)"), env) == 20
print("OK")''',
         tests=['`(+ 1 (* 2 3))` es 7', '`(fact 5)` es 120 con una función recursiva', 'una clausura recuerda su entorno (`add5`)', '`if` solo evalúa la rama elegida'],
         why='Lisp representa el código como datos: una expresión es una lista, y el intérprete es una función recursiva sobre listas. El entorno de una `lambda` se captura al crearla (clausura), de modo que `add5` recuerda que `n` vale 5. El diccionario de entorno compartido permite que `fact` se vea a sí misma al llamarse.'),
    # ---- capítulo 3: paradigmas y era moderna
    dict(ch=3, lang='python', level='INTERMEDIATE',
         prompt='Implementa un almacén de contenido direccionable al estilo de Git: `Store` con `put(data: bytes) -> str` (devuelve el SHA-1 en hexadecimal), `get(key)` y `__len__`. Guardar dos veces el mismo contenido no debe duplicarlo, y `get` debe verificar la integridad (si el contenido guardado no coincide con su clave, lanza `ValueError`). Comprueba deduplicación e integridad.',
         code='''import hashlib


class Store:
    def __init__(self):
        self._objects = {}

    def put(self, data):
        key = hashlib.sha1(data).hexdigest()
        self._objects.setdefault(key, data)
        return key

    def get(self, key):
        data = self._objects[key]
        if hashlib.sha1(data).hexdigest() != key:
            raise ValueError("objeto corrupto")
        return data

    def __len__(self):
        return len(self._objects)''',
         harness='''store = Store()
a = store.put(b"hola")
b = store.put(b"hola")
c = store.put(b"adios")
assert a == b != c
assert len(store) == 2
assert store.get(a) == b"hola"
assert a == "99800b85d3383e3a2fb45eb7d0066a4879a9dad0"
store._objects[a] = b"manipulado"
try:
    store.get(a)
except ValueError:
    print("OK")''',
         tests=['el mismo contenido da la misma clave y no se duplica', 'contenidos distintos dan claves distintas', 'la clave de `"hola"` es la esperada', 'un objeto manipulado se detecta al leerlo'],
         why='Cuando el nombre de un objeto es el hash de su contenido, la deduplicación sale gratis y la integridad se puede comprobar siempre: es la idea sobre la que se construyen Git, Docker y las cadenas de bloques. Cambiar un byte cambia la clave.'),
    dict(ch=3, lang='python', level='INTERMEDIATE',
         prompt='Escribe un planificador cooperativo con generadores: `run_tasks(tasks)` recibe una lista de generadores, ejecuta cada uno hasta su siguiente `yield` por turnos (round-robin) y devuelve el orden en que se produjeron los valores cedidos. Comprueba el entrelazado de tres tareas con distinto número de pasos.',
         code='''from collections import deque


def run_tasks(tasks):
    queue = deque(tasks)
    order = []
    while queue:
        task = queue.popleft()
        try:
            order.append(next(task))
        except StopIteration:
            continue
        queue.append(task)
    return order''',
         harness='''def task(name, steps):
    for i in range(steps):
        yield f"{name}{i}"

assert run_tasks([task("a", 2), task("b", 3), task("c", 1)]) == ["a0", "b0", "c0", "a1", "b1", "b2"]
assert run_tasks([]) == []
assert run_tasks([task("x", 0)]) == []
print("OK")''',
         tests=['las tareas se entrelazan por turnos', 'una tarea que termina sale de la cola', 'sin tareas o con una tarea vacía el resultado es vacío'],
         why='En la concurrencia cooperativa cada tarea decide cuándo ceder el control con `yield`; no hay interrupciones, así que no hacen falta cerrojos entre pasos. Es el modelo de `asyncio`. Su límite es que una tarea que no cede bloquea a todas las demás.'),
    dict(ch=3, lang='python', level='FOUNDATIONAL',
         prompt='Escribe el mismo contador de dos formas, para comparar estilos: una clase `CounterObj` con estado interno y una función `make_counter()` que devuelva una clausura. Comprueba que se comportan igual, que dos instancias son independientes y que el estado de la clausura no es accesible desde fuera como atributo.',
         code='''class CounterObj:
    def __init__(self):
        self._count = 0

    def increment(self):
        self._count += 1
        return self._count


def make_counter():
    count = 0

    def increment():
        nonlocal count
        count += 1
        return count

    return increment''',
         harness='''obj, fn = CounterObj(), make_counter()
assert [obj.increment() for _ in range(3)] == [fn() for _ in range(3)] == [1, 2, 3]
other_obj, other_fn = CounterObj(), make_counter()
assert other_obj.increment() == other_fn() == 1
assert obj.increment() == 4 and fn() == 4
assert not hasattr(fn, "count")
assert fn.__closure__ is not None and len(fn.__closure__) == 1
print("OK")''',
         tests=['objeto y clausura producen `1, 2, 3`', 'dos instancias son independientes', 'el estado de la clausura no es un atributo de la función'],
         why='Un objeto es datos con comportamiento y una clausura es comportamiento con datos: ambos encapsulan estado. La clase permite varios métodos y herencia; la clausura es más ligera cuando solo hay una operación. Son dos caras del mismo concepto.'),
    # ---- capítulo 4: representación binaria
    dict(ch=4, lang='python', level='FOUNDATIONAL',
         prompt='Escribe `to_twos(n, bits)` que devuelva la representación en complemento a dos de `n` como cadena de `bits` dígitos (lanza `ValueError` si no cabe) y `from_twos(text)` que haga la inversa. Comprueba `-1` y `-128` con 8 bits, `127` y el rechazo de `128`.',
         code='''def to_twos(n, bits):
    if not -(1 << (bits - 1)) <= n < (1 << (bits - 1)):
        raise ValueError("no cabe en ese numero de bits")
    return format(n & ((1 << bits) - 1), f"0{bits}b")


def from_twos(text):
    value = int(text, 2)
    if text[0] == "1":
        value -= 1 << len(text)
    return value''',
         harness='''assert to_twos(-1, 8) == "11111111"
assert to_twos(-128, 8) == "10000000"
assert to_twos(127, 8) == "01111111"
assert to_twos(5, 4) == "0101"
assert from_twos("11111111") == -1
assert from_twos("10000000") == -128
assert from_twos("0101") == 5
for n in range(-8, 8):
    assert from_twos(to_twos(n, 4)) == n
for bad in (128, -129):
    try:
        to_twos(bad, 8)
    except ValueError:
        continue
    raise AssertionError(bad)
print("OK")''',
         tests=['`-1` en 8 bits es `11111111`', '`-128` es `10000000`', '`127` es `01111111`', 'la ida y vuelta se conserva para todos los valores de 4 bits', '`128` y `-129` no caben en 8 bits'],
         why='En complemento a dos el bit más alto vale `-2^(n-1)`, de modo que suma y resta funcionan con el mismo circuito. El rango de `n` bits es asimétrico: de `-2^(n-1)` a `2^(n-1) - 1`, por eso `-128` cabe en 8 bits y `128` no.'),
    dict(ch=4, lang='python', level='INTERMEDIATE',
         prompt='Escribe `float_parts(x)` que descomponga un `float` de 64 bits en signo, exponente sin sesgo y mantisa (usando `struct`), y `from_parts(sign, exponent, mantissa)` que lo reconstruya para números normales. Escribe además `almost_equal(a, b, tol)` y comprueba que `0.1 + 0.2 != 0.3` pero son casi iguales.',
         code='''import struct


def float_parts(x):
    bits = struct.unpack(">Q", struct.pack(">d", x))[0]
    sign = bits >> 63
    exponent = ((bits >> 52) & 0x7FF) - 1023
    mantissa = bits & ((1 << 52) - 1)
    return sign, exponent, mantissa


def from_parts(sign, exponent, mantissa):
    bits = (sign << 63) | ((exponent + 1023) << 52) | mantissa
    return struct.unpack(">d", struct.pack(">Q", bits))[0]


def almost_equal(a, b, tol=1e-9):
    return abs(a - b) <= tol * max(1.0, abs(a), abs(b))''',
         harness='''assert float_parts(1.0) == (0, 0, 0)
assert float_parts(-2.0) == (1, 1, 0)
assert float_parts(0.5) == (0, -1, 0)
assert float_parts(1.5) == (0, 0, 1 << 51)
for x in (0.1, -3.75, 1e300, 12345.678):
    assert from_parts(*float_parts(x)) == x
assert 0.1 + 0.2 != 0.3
assert almost_equal(0.1 + 0.2, 0.3)
assert not almost_equal(1.0, 1.001)
print("OK")''',
         tests=['`1.0` tiene signo 0, exponente 0 y mantisa 0', '`-2.0` tiene signo 1 y exponente 1', '`1.5` tiene la mantisa `1 << 51`', 'la reconstrucción devuelve exactamente el mismo número', '`0.1 + 0.2` no es igual a `0.3` pero sí casi igual'],
         why='Un `double` guarda un signo, un exponente con sesgo de 1023 y 52 bits de mantisa con un 1 implícito. Casi ningún decimal como 0,1 tiene representación exacta en binario, por eso la comparación de reales debe hacerse con una tolerancia, nunca con `==`.'),
    dict(ch=4, lang='python', level='INTERMEDIATE',
         prompt='Escribe `utf8_encode(codepoint)` que codifique un punto de código Unicode en bytes UTF-8 sin usar `str.encode` (1 a 4 bytes; lanza `ValueError` si está fuera de rango o es un sustituto). Comprueba la letra `A`, la `ñ`, el signo del euro y un emoji de carita contra la biblioteca estándar.',
         code='''def utf8_encode(cp):
    if cp < 0 or cp > 0x10FFFF or 0xD800 <= cp <= 0xDFFF:
        raise ValueError("punto de codigo invalido")
    if cp < 0x80:
        return bytes([cp])
    if cp < 0x800:
        return bytes([0xC0 | cp >> 6, 0x80 | cp & 0x3F])
    if cp < 0x10000:
        return bytes([0xE0 | cp >> 12, 0x80 | (cp >> 6) & 0x3F, 0x80 | cp & 0x3F])
    return bytes([0xF0 | cp >> 18, 0x80 | (cp >> 12) & 0x3F, 0x80 | (cp >> 6) & 0x3F, 0x80 | cp & 0x3F])''',
         harness='''for ch in ("A", "\\u00f1", "\\u20ac", "\\U0001F600", "\\u0000", "\\U0010FFFF"):
    assert utf8_encode(ord(ch)) == ch.encode("utf-8"), ch
assert len(utf8_encode(0x7F)) == 1 and len(utf8_encode(0x80)) == 2
assert len(utf8_encode(0x7FF)) == 2 and len(utf8_encode(0x800)) == 3
assert len(utf8_encode(0xFFFF)) == 3 and len(utf8_encode(0x10000)) == 4
for bad in (-1, 0x110000, 0xD800):
    try:
        utf8_encode(bad)
    except ValueError:
        continue
    raise AssertionError(bad)
print("OK")''',
         tests=['`A`, `ñ`, el signo del euro y un emoji coinciden con la biblioteca estándar', 'los límites 0x7F/0x80, 0x7FF/0x800 y 0xFFFF/0x10000 cambian la longitud', 'fuera de rango y sustitutos lanzan `ValueError`'],
         why='UTF-8 usa de 1 a 4 bytes: el primer byte indica la longitud y los demás empiezan por `10`. Es compatible con ASCII y se puede resincronizar tras un error. Los puntos entre `D800` y `DFFF` son sustitutos de UTF-16 y no son caracteres válidos.'),
    # ---- capítulo 5: lógica y matemática discreta
    dict(ch=5, lang='python', level='INTERMEDIATE',
         prompt='Escribe `solve_sat(clauses, n)` que busque por fuerza bruta una asignación que satisfaga una fórmula en forma normal conjuntiva (cada cláusula es una lista de enteros no nulos, con signo negativo para la negación) con `n` variables, y devuelva un diccionario o `None`. Comprueba una fórmula satisfacible y otra insatisfacible.',
         code='''from itertools import product


def solve_sat(clauses, n):
    for values in product([False, True], repeat=n):
        assignment = {i + 1: values[i] for i in range(n)}
        if all(any(assignment[abs(lit)] == (lit > 0) for lit in clause) for clause in clauses):
            return assignment
    return None''',
         harness='''sat = [[1, 2], [-1, 3], [-2, -3]]
solution = solve_sat(sat, 3)
assert solution is not None
assert all(any(solution[abs(l)] == (l > 0) for l in c) for c in sat)
assert solve_sat([[1], [-1]], 1) is None
assert solve_sat([], 2) is not None
assert solve_sat([[]], 1) is None
print("OK")''',
         tests=['una fórmula satisfacible devuelve una asignación válida', '`x` y `no x` es insatisfacible', 'sin cláusulas toda asignación sirve', 'una cláusula vacía es insatisfacible'],
         why='Una cláusula se cumple si alguno de sus literales es verdadero, y la fórmula si se cumplen todas. La búsqueda exhaustiva recorre `2^n` asignaciones; los solucionadores reales (DPLL, CDCL) podan el espacio, pero en el peor caso siguen siendo exponenciales.'),
    dict(ch=5, lang='python', level='FOUNDATIONAL',
         prompt='Escribe `pascal_row(n)` que construya la fila `n` del triángulo de Pascal sumando la fila anterior, y `choose(n, k)` que use esa fila. Comprueba contra `math.comb` hasta `n = 20`, que la suma de cada fila es `2**n` y los casos `choose(5, 7)` y `choose(0, 0)`.',
         code='''def pascal_row(n):
    row = [1]
    for _ in range(n):
        row = [1] + [a + b for a, b in zip(row, row[1:])] + [1]
    return row


def choose(n, k):
    if k < 0 or k > n:
        return 0
    return pascal_row(n)[k]''',
         harness='''import math

for n in range(0, 21):
    row = pascal_row(n)
    assert row == [math.comb(n, k) for k in range(n + 1)]
    assert sum(row) == 2 ** n
assert choose(5, 7) == 0 and choose(0, 0) == 1 and choose(5, -1) == 0
assert choose(10, 3) == 120
print("OK")''',
         tests=['las filas coinciden con `math.comb` hasta `n = 20`', 'cada fila suma `2^n`', '`choose(5, 7)` es 0', '`choose(0, 0)` es 1', '`choose(10, 3)` es 120'],
         why='Cada número del triángulo es la suma de los dos que tiene encima, y cuenta las formas de elegir `k` de `n` elementos. Que cada fila sume `2^n` refleja que el número de subconjuntos de un conjunto de `n` elementos es `2^n`.'),
    dict(ch=5, lang='python', level='INTERMEDIATE',
         prompt='Escribe `power_set(items)` que devuelva todos los subconjuntos de una lista (como listas, ordenados por tamaño y luego por orden de aparición) y `is_subset(a, b)` sin usar `<=` de conjuntos. Comprueba `{1,2,3}` (8 subconjuntos), el vacío y la inclusión.',
         code='''from itertools import combinations


def power_set(items):
    return [list(c) for size in range(len(items) + 1) for c in combinations(items, size)]


def is_subset(a, b):
    return all(x in b for x in a)''',
         harness='''subsets = power_set([1, 2, 3])
assert len(subsets) == 8
assert subsets == [[], [1], [2], [3], [1, 2], [1, 3], [2, 3], [1, 2, 3]]
assert power_set([]) == [[]]
assert len(power_set(list(range(10)))) == 2 ** 10
assert is_subset([1, 2], [1, 2, 3]) and is_subset([], [])
assert not is_subset([4], [1, 2, 3])
print("OK")''',
         tests=['`{1, 2, 3}` tiene 8 subconjuntos en orden por tamaño', 'el conjunto vacío tiene un subconjunto: él mismo', 'un conjunto de 10 elementos tiene 1024 subconjuntos', 'la inclusión se comprueba elemento a elemento'],
         why='Cada elemento está o no en un subconjunto, así que hay `2^n`. El conjunto de las partes crece exponencialmente, por eso generar todos los subconjuntos solo es práctico para conjuntos pequeños.'),
    # ---- capítulo 6: arquitectura de CPU y memoria
    dict(ch=6, lang='python', level='ADVANCED',
         prompt='Escribe un simulador de CPU con registros `R0`..`R3` y memoria: `execute(program)` con instrucciones `("MOV", reg, valor)`, `("ADD", dst, src)`, `("MUL", dst, src)`, `("DEC", reg)`, `("JNZ", reg, destino)` y `("HALT",)`. Escribe con ellas el cálculo de 5! y devuelve el valor de `R1`. Comprueba el resultado y que `R0` termina en 0.',
         code='''def execute(program, max_steps=10_000):
    regs = {"R0": 0, "R1": 0, "R2": 0, "R3": 0}
    pc = 0
    for _ in range(max_steps):
        op, *args = program[pc]
        pc += 1
        if op == "MOV":
            regs[args[0]] = args[1]
        elif op == "ADD":
            regs[args[0]] += regs[args[1]]
        elif op == "MUL":
            regs[args[0]] *= regs[args[1]]
        elif op == "DEC":
            regs[args[0]] -= 1
        elif op == "JNZ":
            if regs[args[0]] != 0:
                pc = args[1]
        elif op == "HALT":
            return regs
        else:
            raise ValueError(op)
    raise RuntimeError("no termina")''',
         harness='''factorial = [
    ("MOV", "R0", 5),
    ("MOV", "R1", 1),
    ("MUL", "R1", "R0"),
    ("DEC", "R0"),
    ("JNZ", "R0", 2),
    ("HALT",),
]
regs = execute(factorial)
assert regs["R1"] == 120 and regs["R0"] == 0
assert execute([("MOV", "R2", 7), ("HALT",)])["R2"] == 7
try:
    execute([("MOV", "R0", 1), ("JNZ", "R0", 0)], max_steps=50)
except RuntimeError:
    print("OK")''',
         tests=['el programa calcula 5! = 120 en `R1`', '`R0` termina en 0', '`MOV` carga un valor', 'un bucle infinito lanza `RuntimeError`'],
         why='Una CPU repite buscar la instrucción apuntada por el contador de programa, decodificarla y ejecutarla. Los saltos condicionales y los registros bastan para escribir bucles y calcular cualquier función computable; el factorial multiplica el acumulador por un contador que decrece hasta cero.'),
    dict(ch=6, lang='python', level='ADVANCED',
         prompt='Escribe `simulate_cache(addresses, lines, line_size)` que simule una caché de correspondencia directa (cada dirección va a la línea `(dirección // line_size) % lines`) y devuelva `(aciertos, fallos)`. Comprueba que recorrer un array en orden tiene muchos más aciertos que saltar con un paso del tamaño de la caché.',
         code='''def simulate_cache(addresses, lines, line_size):
    tags = [None] * lines
    hits = misses = 0
    for address in addresses:
        block = address // line_size
        index = block % lines
        if tags[index] == block:
            hits += 1
        else:
            misses += 1
            tags[index] = block
    return hits, misses''',
         harness='''sequential = list(range(0, 1024))
hits, misses = simulate_cache(sequential, lines=8, line_size=64)
assert (hits, misses) == (1024 - 16, 16)
strided = [(i * 512) % (8 * 512 * 4) for i in range(1024)]
h2, m2 = simulate_cache(strided, lines=8, line_size=64)
assert h2 == 0 and m2 == 1024
assert simulate_cache([], 4, 16) == (0, 0)
assert simulate_cache([0, 0, 0], 4, 16) == (2, 1)
print("OK")''',
         tests=['recorrer 1024 direcciones en orden con líneas de 64 da 16 fallos y 1008 aciertos', 'un paso igual al tamaño de la caché da 0 aciertos', 'sin accesos no hay aciertos ni fallos', 'repetir una dirección acierta'],
         why='Una línea de caché trae un bloque contiguo: el primer acceso a cada bloque falla y los siguientes aciertan (localidad espacial). Un paso que lleva todas las direcciones a la misma línea provoca conflictos continuos, que es el motivo de que el orden de recorrido de una matriz importe tanto.'),
    dict(ch=6, lang='python', level='FOUNDATIONAL',
         prompt='Escribe `to_bytes_manual(n, size, byteorder)` que convierta un entero sin signo a bytes en orden `"little"` o `"big"` sin usar `int.to_bytes`, y `from_bytes_manual(data, byteorder)`. Comprueba `0x12345678` en ambos órdenes contra la biblioteca estándar.',
         code='''def to_bytes_manual(n, size, byteorder):
    if n < 0 or n >= 1 << (8 * size):
        raise OverflowError("no cabe")
    little = [(n >> (8 * i)) & 0xFF for i in range(size)]
    return bytes(little if byteorder == "little" else reversed(little))


def from_bytes_manual(data, byteorder):
    ordered = data if byteorder == "little" else data[::-1]
    return sum(b << (8 * i) for i, b in enumerate(ordered))''',
         harness='''n = 0x12345678
assert to_bytes_manual(n, 4, "little") == b"\\x78\\x56\\x34\\x12" == n.to_bytes(4, "little")
assert to_bytes_manual(n, 4, "big") == b"\\x12\\x34\\x56\\x78" == n.to_bytes(4, "big")
for value in (0, 1, 255, 256, 65535, 2 ** 32 - 1):
    for order in ("little", "big"):
        assert from_bytes_manual(to_bytes_manual(value, 4, order), order) == value
try:
    to_bytes_manual(256, 1, "little")
except OverflowError:
    print("OK")''',
         tests=['`0x12345678` en little-endian es `78 56 34 12`', 'en big-endian es `12 34 56 78`', 'la ida y vuelta se conserva', 'un valor que no cabe lanza `OverflowError`'],
         why='El orden de bytes decide qué byte va en la dirección más baja. Un protocolo de red usa big-endian por convención, y casi todas las CPUs actuales usan little-endian internamente, por lo que hay que convertir al intercambiar datos binarios.'),
    # ---- capítulo 7: tipos, ámbito, errores
    dict(ch=7, lang='python', level='ADVANCED',
         prompt='Escribe un comprobador de tipos para un lenguaje de expresiones con enteros, booleanos y `if`: `type_of(expr, env)` donde una expresión es `("int", n)`, `("bool", b)`, `("var", nombre)`, `("add", a, b)`, `("eq", a, b)` o `("if", c, a, b)`. Debe lanzar `TypeError` si se suma un booleano, se compara un entero con un booleano, la condición no es booleana o las ramas tienen tipos distintos.',
         code='''def type_of(expr, env=None):
    env = env or {}
    tag = expr[0]
    if tag == "int":
        return "int"
    if tag == "bool":
        return "bool"
    if tag == "var":
        return env[expr[1]]
    if tag == "add":
        if type_of(expr[1], env) != "int" or type_of(expr[2], env) != "int":
            raise TypeError("add necesita enteros")
        return "int"
    if tag == "eq":
        if type_of(expr[1], env) != type_of(expr[2], env):
            raise TypeError("eq necesita el mismo tipo")
        return "bool"
    if tag == "if":
        if type_of(expr[1], env) != "bool":
            raise TypeError("la condicion debe ser bool")
        a, b = type_of(expr[2], env), type_of(expr[3], env)
        if a != b:
            raise TypeError("las ramas tienen tipos distintos")
        return a
    raise TypeError(f"expresion desconocida: {tag}")''',
         harness='''assert type_of(("add", ("int", 1), ("int", 2))) == "int"
assert type_of(("eq", ("int", 1), ("int", 2))) == "bool"
assert type_of(("if", ("bool", True), ("int", 1), ("int", 2))) == "int"
assert type_of(("add", ("var", "x"), ("int", 1)), {"x": "int"}) == "int"
bad = [
    ("add", ("bool", True), ("int", 1)),
    ("eq", ("int", 1), ("bool", True)),
    ("if", ("int", 1), ("int", 1), ("int", 2)),
    ("if", ("bool", True), ("int", 1), ("bool", False)),
    ("nada",),
]
for expr in bad:
    try:
        type_of(expr)
    except TypeError:
        continue
    raise AssertionError(expr)
print("OK")''',
         tests=['las expresiones bien tipadas devuelven su tipo', 'sumar un booleano es un error de tipos', 'comparar un entero con un booleano es un error', 'una condición entera es un error', 'ramas de tipos distintos son un error'],
         why='Un sistema de tipos rechaza programas antes de ejecutarlos asignando un tipo a cada expresión y comprobando que las operaciones se aplican a tipos compatibles. Es un análisis estático: demuestra la ausencia de ciertos errores sin necesidad de probar todas las ejecuciones.'),
    dict(ch=7, lang='python', level='INTERMEDIATE',
         prompt='Escribe un intérprete de entornos encadenados: `Env(parent)` con `define`, `get` y `set`, y `lookup` que busque en el entorno actual y suba al padre (ámbito léxico). Comprueba el sombreado de variables, que `set` modifica la variable de un entorno exterior, y que una clausura captura su entorno de definición, no el de llamada.',
         code='''class Env:
    def __init__(self, parent=None):
        self.vars = {}
        self.parent = parent

    def define(self, name, value):
        self.vars[name] = value

    def get(self, name):
        env = self
        while env is not None:
            if name in env.vars:
                return env.vars[name]
            env = env.parent
        raise NameError(name)

    def set(self, name, value):
        env = self
        while env is not None:
            if name in env.vars:
                env.vars[name] = value
                return
            env = env.parent
        raise NameError(name)''',
         harness='''globals_ = Env()
globals_.define("x", 1)
inner = Env(globals_)
inner.define("x", 2)
assert inner.get("x") == 2 and globals_.get("x") == 1
inner2 = Env(globals_)
inner2.set("x", 10)
assert globals_.get("x") == 10
def make_closure():
    local = Env(globals_)
    local.define("y", 5)
    return lambda: local.get("y") + local.get("x")
closure = make_closure()
caller = Env()
caller.define("x", 1000)
assert closure() == 15
for name in ("z",):
    try:
        globals_.get(name)
    except NameError:
        pass
    else:
        raise AssertionError(name)
print("OK")''',
         tests=['una variable local sombrea a la global', '`set` modifica la variable del entorno exterior', 'la clausura usa el entorno donde se definió', 'una variable inexistente lanza `NameError`'],
         why='En el ámbito léxico, el significado de un nombre se decide por dónde está escrito el código, no por quién lo llama. Cada entorno apunta a su padre, y la búsqueda sube por la cadena. Una clausura es una función más una referencia a su entorno.'),
    dict(ch=7, lang='python', level='INTERMEDIATE',
         prompt='Implementa un tipo `Result` con `Ok(value)` y `Err(error)` y los métodos `map`, `and_then` y `unwrap_or`, para encadenar operaciones sin excepciones. Escribe con él `parse_int(text)` y `reciprocal(n)` y encadénalos: `parse_int("4").and_then(reciprocal)` es `Ok(0.25)`; `"x"` y `"0"` dan `Err`.',
         code='''class Result:
    def __init__(self, ok, value):
        self.ok, self.value = ok, value

    def map(self, fn):
        return Result(True, fn(self.value)) if self.ok else self

    def and_then(self, fn):
        return fn(self.value) if self.ok else self

    def unwrap_or(self, default):
        return self.value if self.ok else default

    def __eq__(self, other):
        return (self.ok, self.value) == (other.ok, other.value)


def Ok(value):
    return Result(True, value)


def Err(error):
    return Result(False, error)


def parse_int(text):
    try:
        return Ok(int(text))
    except ValueError:
        return Err(f"no es un entero: {text!r}")


def reciprocal(n):
    return Err("division por cero") if n == 0 else Ok(1 / n)''',
         harness='''assert parse_int("4").and_then(reciprocal) == Ok(0.25)
assert parse_int("x").and_then(reciprocal) == Err("no es un entero: 'x'")
assert parse_int("0").and_then(reciprocal) == Err("division por cero")
assert parse_int("4").map(lambda n: n * 2) == Ok(8)
assert parse_int("x").map(lambda n: n * 2).unwrap_or(-1) == -1
assert parse_int("8").and_then(reciprocal).unwrap_or(-1) == 0.125
print("OK")''',
         tests=['`"4"` encadenado con `reciprocal` da `Ok(0.25)`', 'un texto no numérico da `Err`', 'dividir entre cero da `Err`', '`map` transforma solo los valores correctos', '`unwrap_or` devuelve el valor por defecto ante un error'],
         why='En lugar de lanzar excepciones, la función devuelve un valor que dice si salió bien. `and_then` solo ejecuta el siguiente paso si el anterior fue correcto, de modo que el primer error se propaga sin comprobaciones intermedias. El error pasa a formar parte del tipo.'),
    # ---- capítulo 8: los paradigmas
    dict(ch=8, lang='python', level='FOUNDATIONAL',
         prompt='Resuelve el mismo problema, la suma de los cuadrados de los pares de una lista, en cuatro estilos: `imperative(xs)` con bucle y acumulador, `functional(xs)` con `filter`, `map` y `sum`, `object_oriented(xs)` con una clase `Summer` que acumule estado, y `recursive(xs)` sin bucles ni comprensiones. Comprueba que los cuatro coinciden y que no modifican la entrada.',
         code='''from functools import reduce


def imperative(xs):
    total = 0
    for x in xs:
        if x % 2 == 0:
            total += x * x
    return total


def functional(xs):
    return sum(map(lambda x: x * x, filter(lambda x: x % 2 == 0, xs)))


class Summer:
    def __init__(self):
        self.total = 0

    def feed(self, x):
        if x % 2 == 0:
            self.total += x * x
        return self


def object_oriented(xs):
    return reduce(lambda s, x: s.feed(x), xs, Summer()).total


def recursive(xs):
    if not xs:
        return 0
    head, rest = xs[0], xs[1:]
    return (head * head if head % 2 == 0 else 0) + recursive(rest)''',
         harness='''data = [1, 2, 3, 4, 5, 6, -2, 0]
copy = list(data)
expected = 4 + 16 + 36 + 4 + 0
for fn in (imperative, functional, object_oriented, recursive):
    assert fn(data) == expected, fn.__name__
assert data == copy
for fn in (imperative, functional, object_oriented, recursive):
    assert fn([]) == 0 and fn([1, 3]) == 0
print("OK")''',
         tests=['los cuatro estilos dan 60 para `[1, 2, 3, 4, 5, 6, -2, 0]`', 'la entrada no se modifica', 'una lista vacía o sin pares da 0'],
         why='Cada paradigma organiza el mismo cálculo de forma distinta: el imperativo modifica un acumulador, el funcional compone funciones sin estado, el orientado a objetos encapsula el estado y el recursivo expresa la repetición como definición. Ninguno es mejor en general; cada uno hace más natural un tipo de problema.'),
    dict(ch=8, lang='python', level='INTERMEDIATE',
         prompt='Escribe `evaluate(expr)` para expresiones con tipos algebraicos de datos usando `match` estructural de Python: `("num", n)`, `("add", a, b)`, `("mul", a, b)`, `("neg", a)` y `("div", a, b)`, donde dividir entre cero lanza `ZeroDivisionError`. Comprueba los cinco casos y un error.',
         code='''def evaluate(expr):
    match expr:
        case ("num", n):
            return n
        case ("add", a, b):
            return evaluate(a) + evaluate(b)
        case ("mul", a, b):
            return evaluate(a) * evaluate(b)
        case ("neg", a):
            return -evaluate(a)
        case ("div", a, b):
            return evaluate(a) / evaluate(b)
        case _:
            raise ValueError(f"expresion desconocida: {expr!r}")''',
         harness='''assert evaluate(("num", 7)) == 7
assert evaluate(("add", ("num", 2), ("mul", ("num", 3), ("num", 4)))) == 14
assert evaluate(("neg", ("add", ("num", 1), ("num", 2)))) == -3
assert evaluate(("div", ("num", 1), ("num", 4))) == 0.25
try:
    evaluate(("div", ("num", 1), ("num", 0)))
except ZeroDivisionError:
    pass
else:
    raise AssertionError("division")
try:
    evaluate(("pow", ("num", 2)))
except ValueError:
    print("OK")''',
         tests=['`num`, `add`, `mul`, `neg` y `div` se evalúan', 'las expresiones anidadas se evalúan en profundidad', 'dividir entre cero lanza `ZeroDivisionError`', 'una forma desconocida lanza `ValueError`'],
         why='El ajuste de patrones descompone un dato según su forma y es el estilo natural de los lenguajes funcionales para recorrer árboles. Un `case _` final convierte las formas no previstas en un error explícito en lugar de devolver `None` en silencio.'),
    dict(ch=8, lang='python', level='ADVANCED',
         prompt='Compara dos modelos de concurrencia resolviendo "sumar los cuadrados de 1..N con 4 productores": `with_threads_and_queue(n)` con hilos y una cola compartida (`queue.Queue`) y `with_processes_free_functions(n)` que reparta rangos a `ThreadPoolExecutor` mediante funciones puras sin estado compartido. Comprueba que ambos dan la fórmula `n(n+1)(2n+1)/6`.',
         code='''import queue
import threading
from concurrent.futures import ThreadPoolExecutor


def with_threads_and_queue(n, workers=4):
    results = queue.Queue()

    def producer(start, stop):
        results.put(sum(i * i for i in range(start, stop)))

    step = -(-n // workers)
    threads = [threading.Thread(target=producer, args=(1 + i * step, min(n, (i + 1) * step) + 1)) for i in range(workers)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    total = 0
    while not results.empty():
        total += results.get()
    return total


def partial(bounds):
    start, stop = bounds
    return sum(i * i for i in range(start, stop))


def with_processes_free_functions(n, workers=4):
    step = -(-n // workers)
    ranges = [(1 + i * step, min(n, (i + 1) * step) + 1) for i in range(workers)]
    with ThreadPoolExecutor(max_workers=workers) as pool:
        return sum(pool.map(partial, ranges))''',
         harness='''for n in (1, 10, 1000, 12345):
    formula = n * (n + 1) * (2 * n + 1) // 6
    assert with_threads_and_queue(n) == formula, n
    assert with_processes_free_functions(n) == formula, n
assert with_threads_and_queue(3, workers=8) == 14
assert with_processes_free_functions(3, workers=8) == 14
print("OK")''',
         tests=['los dos modelos coinciden con la fórmula para `n = 1, 10, 1000, 12345`', 'con más trabajadores que elementos sigue siendo correcto'],
         why='Con hilos y cola, los productores se comunican mediante una estructura compartida sincronizada; con funciones puras, cada tarea recibe sus datos y devuelve un resultado, sin estado compartido, lo que elimina por construcción las carreras de datos. Es la diferencia entre comunicar compartiendo memoria y compartir comunicando.'),
]
