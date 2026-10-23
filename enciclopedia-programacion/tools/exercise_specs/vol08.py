"""Programming exercises of volume 8 (web, databases and frameworks). Each reference program runs with a real interpreter."""

EXERCISES = [
    # ---- capítulo 1: HTML y accesibilidad
    dict(ch=1, lang='python', level='FOUNDATIONAL',
         prompt='Escribe `images_without_alt(html)` que use `html.parser.HTMLParser` y devuelva la lista de valores `src` de las imágenes `<img>` que no tienen atributo `alt`. Una imagen decorativa con `alt=""` es correcta y no debe aparecer. Comprueba con un documento con tres imágenes.',
         code='''from html.parser import HTMLParser


class _ImgAudit(HTMLParser):
    def __init__(self):
        super().__init__()
        self.missing = []

    def handle_starttag(self, tag, attrs):
        if tag == "img":
            attributes = dict(attrs)
            if "alt" not in attributes:
                self.missing.append(attributes.get("src", ""))


def images_without_alt(html):
    parser = _ImgAudit()
    parser.feed(html)
    return parser.missing''',
         harness='''doc = '<p><img src="a.png" alt="Logo"><img src="b.png"><img src="c.png" alt=""></p><IMG SRC="d.png">'
assert images_without_alt(doc) == ["b.png", "d.png"]
assert images_without_alt("<p>sin imagenes</p>") == []
assert images_without_alt('<img src="x.png" alt="ok">') == []
print("OK")''',
         tests=['`b.png` sin `alt` aparece en el resultado', '`alt=""` (decorativa) no aparece', 'un documento sin imágenes da lista vacía', 'las etiquetas en mayúsculas también se reconocen'],
         why='El atributo `alt` es la alternativa textual para lectores de pantalla. Su ausencia es un error, pero un `alt` vacío es una declaración legítima de que la imagen es decorativa. `HTMLParser` normaliza los nombres de etiqueta y atributo a minúsculas, así que `IMG` y `SRC` se tratan igual.'),
    dict(ch=1, lang='python', level='INTERMEDIATE',
         prompt='Escribe `heading_problems(html)` que devuelva una lista de mensajes si la jerarquía de encabezados `<h1>`..`<h6>` es incorrecta: debe haber exactamente un `h1`, y un encabezado no puede saltar más de un nivel respecto al anterior (de `h2` a `h4`, por ejemplo). Devuelve `[]` si es correcta. Comprueba un documento correcto y varios incorrectos.',
         code='''import re


def heading_problems(html):
    levels = [int(m.group(1)) for m in re.finditer(r"<h([1-6])[\\s>]", html, re.IGNORECASE)]
    problems = []
    if levels.count(1) != 1:
        problems.append(f"debe haber exactamente un h1, hay {levels.count(1)}")
    previous = 0
    for level in levels:
        if level > previous + 1 and previous != 0:
            problems.append(f"salto de h{previous} a h{level}")
        previous = level
    return problems''',
         harness='''good = "<h1>T</h1><h2>A</h2><h3>A1</h3><h2>B</h2>"
assert heading_problems(good) == []
assert heading_problems("<h1>T</h1><h2>A</h2><h4>X</h4>") == ["salto de h2 a h4"]
assert heading_problems("<h2>A</h2>") == ["debe haber exactamente un h1, hay 0"]
assert len(heading_problems("<h1>A</h1><h1>B</h1>")) == 1
assert heading_problems("<h1>A</h1><h3>B</h3>") == ["salto de h1 a h3"]
print("OK")''',
         tests=['un documento bien jerarquizado da `[]`', '`h2` seguido de `h4` es un salto', 'sin `h1` es un error', 'dos `h1` es un error', 'bajar de nivel (de `h3` a `h2`) no es un error'],
         why='Los lectores de pantalla permiten navegar por encabezados, por lo que los saltos de nivel desorientan. Subir de nivel solo puede hacerse de uno en uno, mientras que bajar a cualquier nivel superior es válido. Esta comprobación con expresión regular basta para el ejercicio; un auditor real analizaría el árbol del documento.'),
    dict(ch=1, lang='js', level='INTERMEDIATE',
         prompt='Escribe en JavaScript `unlabeledInputs(fields)` que reciba una lista de objetos `{ id, label }` (donde `label` es el `for` del `<label>` asociado o `null`) y de campos `{ id, type }`, y devuelva los `id` de los campos de texto, correo o contraseña que no tienen etiqueta asociada. Comprueba con tres campos.',
         code='''function unlabeledInputs(inputs, labels) {
  const labelled = new Set(labels.map((l) => l.forId));
  const needsLabel = new Set(["text", "email", "password", "search", "tel", "url"]);
  return inputs.filter((i) => needsLabel.has(i.type) && !labelled.has(i.id)).map((i) => i.id);
}''',
         harness='''const assert = require("node:assert");
const inputs = [
  { id: "nombre", type: "text" },
  { id: "clave", type: "password" },
  { id: "oculto", type: "hidden" },
  { id: "enviar", type: "submit" },
  { id: "correo", type: "email" },
];
const labels = [{ forId: "nombre" }];
assert.deepStrictEqual(unlabeledInputs(inputs, labels), ["clave", "correo"]);
assert.deepStrictEqual(unlabeledInputs([], []), []);
console.log("OK");''',
         tests=['`clave` y `correo` no tienen etiqueta', 'los campos `hidden` y `submit` no la necesitan', 'sin campos el resultado es vacío'],
         why='Un campo de formulario sin `<label for>` no tiene nombre accesible: un lector de pantalla solo dice "cuadro de edición". Los tipos `hidden`, `submit` y similares no necesitan etiqueta porque no los rellena el usuario o ya tienen su texto.'),
    # ---- capítulo 2: CSS
    dict(ch=2, lang='python', level='INTERMEDIATE',
         prompt='Escribe `specificity(selector)` que devuelva la tupla `(ids, clases_atributos_pseudoclases, elementos)` de un selector CSS simple (sin `:not`, `:is` ni combinadores complejos; `>` y `+` y espacios separan compuestos), y `winner(selectors)` que devuelva el selector con mayor especificidad (el último gana en empate). Comprueba `#a .b p`, `.a.b`, `p::before` y `a:hover`.',
         code='''import re


def specificity(selector):
    s = re.sub(r"\\[[^\\]]*\\]", " [] ", selector)
    ids = len(re.findall(r"#[\\w-]+", s))
    classes = len(re.findall(r"\\.[\\w-]+", s)) + s.count("[]") + len(re.findall(r"(?<!:):[\\w-]+", s))
    elements = len(re.findall(r"(?:(?<=^)|(?<=[\\s>+~]))[a-zA-Z][\\w-]*", s)) + len(re.findall(r"::[\\w-]+", s))
    return (ids, classes, elements)


def winner(selectors):
    best = None
    for selector in selectors:
        if best is None or specificity(selector) >= specificity(best):
            best = selector
    return best''',
         harness='''assert specificity("#a .b p") == (1, 1, 1)
assert specificity(".a.b") == (0, 2, 0)
assert specificity("p::before") == (0, 0, 2)
assert specificity("a:hover") == (0, 1, 1)
assert specificity("input[type=text]") == (0, 1, 1)
assert specificity("ul > li + li") == (0, 0, 3)
assert specificity("*") == (0, 0, 0)
assert winner([".a", "#x", "p p p"]) == "#x"
assert winner([".a", ".b"]) == ".b"
assert (1, 0, 0) > (0, 99, 99)
print("OK")''',
         tests=['`#a .b p` da `(1, 1, 1)`', '`.a.b` da `(0, 2, 0)`', 'un pseudoelemento cuenta como elemento y una pseudoclase como clase', 'un atributo cuenta como clase', 'un identificador gana a cualquier número de clases', 'el último gana en empate'],
         why='La especificidad se compara por tuplas, componente a componente: un solo id supera a cualquier número de clases. Contar mal `::before` (elemento) y `:hover` (clase) es un error frecuente. En un empate decide el orden en la hoja de estilos, por eso `winner` prefiere el último.'),
    dict(ch=2, lang='python', level='INTERMEDIATE',
         prompt='Escribe `flex_widths(container, items)` que calcule el ancho final de cada elemento de un contenedor Flex de una línea. Cada ítem es `(basis, grow, shrink)`. Si la suma de bases es menor que el contenedor, el espacio libre se reparte según `grow`; si es mayor, el exceso se reparte según `shrink * basis`. Comprueba tres ítems de bases 160, 100 y 100 en 960 px con `grow = 1` (el primero mide 360).',
         code='''def flex_widths(container, items):
    total_basis = sum(basis for basis, _, _ in items)
    free = container - total_basis
    if free >= 0:
        total_grow = sum(grow for _, grow, _ in items)
        if total_grow == 0:
            return [float(basis) for basis, _, _ in items]
        return [basis + free * grow / total_grow for basis, grow, _ in items]
    weights = [shrink * basis for basis, _, shrink in items]
    total = sum(weights)
    if total == 0:
        return [float(basis) for basis, _, _ in items]
    return [basis + free * weight / total for (basis, _, _), weight in zip(items, weights)]''',
         harness='''assert flex_widths(960, [(160, 1, 1), (100, 1, 1), (100, 1, 1)]) == [360, 300, 300]
assert flex_widths(500, [(100, 0, 1), (100, 0, 1)]) == [100, 100]
assert flex_widths(300, [(200, 0, 1), (200, 0, 1)]) == [150, 150]
shrunk = flex_widths(300, [(300, 0, 1), (100, 0, 1)])
assert abs(sum(shrunk) - 300) < 1e-9 and abs(shrunk[0] - 225) < 1e-9
assert flex_widths(100, []) == []
print("OK")''',
         tests=['bases 160, 100, 100 en 960 px con `grow = 1` dan 360, 300, 300', 'con `grow = 0` los elementos conservan su base', 'dos bases iguales que no caben se reducen por igual', 'la reducción es proporcional a `shrink * basis` y suma el contenedor', 'sin elementos devuelve lista vacía'],
         why='`flex-grow` reparte el espacio libre en proporción a su factor, mientras que `flex-shrink` reparte el exceso ponderando por la base, de modo que los elementos grandes ceden más. Es el algoritmo simplificado de la especificación, sin tener en cuenta tamaños mínimos ni máximos.'),
    dict(ch=2, lang='python', level='INTERMEDIATE',
         prompt='Escribe `grid_columns(width, columns, gap)` que calcule el ancho de cada columna `1fr` de un CSS Grid con `columns` columnas iguales y huecos de `gap` píxeles entre ellas, y `grid_track_positions(width, columns, gap)` que devuelva la coordenada de inicio de cada columna. Comprueba un contenedor de 1200 px con 3 columnas y hueco de 24 px (384 px cada una).',
         code='''def grid_columns(width, columns, gap):
    if columns < 1:
        raise ValueError("columns debe ser al menos 1")
    return (width - gap * (columns - 1)) / columns


def grid_track_positions(width, columns, gap):
    size = grid_columns(width, columns, gap)
    return [i * (size + gap) for i in range(columns)]''',
         harness='''assert grid_columns(1200, 3, 24) == 384
assert grid_track_positions(1200, 3, 24) == [0, 408, 816]
assert grid_columns(100, 1, 50) == 100
assert grid_columns(100, 4, 0) == 25
last = grid_track_positions(1200, 3, 24)[-1] + grid_columns(1200, 3, 24)
assert last == 1200
try:
    grid_columns(100, 0, 10)
except ValueError:
    print("OK")''',
         tests=['1200 px con 3 columnas y hueco de 24 px da 384 px por columna', 'las columnas empiezan en 0, 408 y 816', 'una columna ocupa todo el ancho', 'la última columna termina exactamente en el ancho del contenedor', '0 columnas lanza `ValueError`'],
         why='Los huecos no son columnas: hay `n - 1` entre `n` columnas, y se descuentan antes de repartir. La comprobación final, que la última columna termine en el borde del contenedor, valida los dos cálculos a la vez.'),
    # ---- capítulo 3: formatos
    dict(ch=3, lang='python', level='INTERMEDIATE',
         prompt='Escribe `encode_varint(n)` y `decode_varint(data)` para el formato de enteros de Protocol Buffers (7 bits por byte, bit alto de continuación, orden little-endian), y `zigzag(n)` / `unzigzag(u)` para enteros con signo de 32 bits. Comprueba `300 -> b"\\xac\\x02"`, `zigzag(-15) == 29` y la ida y vuelta.',
         code='''def encode_varint(n):
    if n < 0:
        raise ValueError("solo no negativos")
    out = bytearray()
    while True:
        byte = n & 0x7F
        n >>= 7
        if n:
            out.append(byte | 0x80)
        else:
            out.append(byte)
            return bytes(out)


def decode_varint(data):
    result = 0
    for shift, byte in enumerate(data):
        result |= (byte & 0x7F) << (7 * shift)
        if not byte & 0x80:
            return result, shift + 1
    raise ValueError("varint truncado")


def zigzag(n):
    return ((n << 1) ^ (n >> 31)) & 0xFFFFFFFF


def unzigzag(u):
    return (u >> 1) ^ -(u & 1)''',
         harness='''assert encode_varint(0) == b"\\x00"
assert encode_varint(1) == b"\\x01"
assert encode_varint(300) == b"\\xac\\x02"
assert decode_varint(b"\\xac\\x02") == (300, 2)
assert decode_varint(b"\\x96\\x01\\xff") == (150, 2)
assert zigzag(0) == 0 and zigzag(-1) == 1 and zigzag(1) == 2 and zigzag(-15) == 29
for n in (0, 1, 127, 128, 16383, 16384, 2**31 - 1):
    assert decode_varint(encode_varint(n))[0] == n
for n in (-2**31, -15, -1, 0, 7, 2**31 - 1):
    assert unzigzag(zigzag(n)) == n
try:
    decode_varint(b"\\x80")
except ValueError:
    print("OK")''',
         tests=['`300` se codifica como `ac 02`', '`decode_varint` devuelve el valor y los bytes consumidos', '`zigzag(-15)` es 29', 'la ida y vuelta se conserva para valores límite', 'un varint truncado lanza `ValueError`'],
         why='Cada byte aporta 7 bits y el bit alto indica que sigue otro byte, así que los números pequeños ocupan poco. ZigZag intercala positivos y negativos (`0, -1, 1, -2, ...`) para que los negativos pequeños tampoco ocupen diez bytes, como ocurriría con el complemento a dos.'),
    dict(ch=3, lang='python', level='INTERMEDIATE',
         prompt='Escribe `csv_to_json(text)` que lea un CSV con cabecera (con el módulo `csv`, respetando comillas y comas dentro de campos) y devuelva un JSON con una lista de objetos, convirtiendo a entero o real los valores numéricos y dejando el resto como texto. Comprueba un CSV con una coma dentro de un campo entre comillas.',
         code='''import csv
import io
import json


def _convert(value):
    for cast in (int, float):
        try:
            return cast(value)
        except ValueError:
            pass
    return value


def csv_to_json(text):
    rows = csv.DictReader(io.StringIO(text))
    data = [{key: _convert(value) for key, value in row.items()} for row in rows]
    return json.dumps(data, ensure_ascii=False)''',
         harness='''text = 'nombre,edad,nota\\n"Pérez, Ana",31,8.5\\nLuis,40,7\\n'
result = json.loads(csv_to_json(text))
assert result == [{"nombre": "Pérez, Ana", "edad": 31, "nota": 8.5}, {"nombre": "Luis", "edad": 40, "nota": 7}]
assert isinstance(result[1]["nota"], int)
assert csv_to_json("a,b\\n") == "[]"
print("OK")''',
         tests=['una coma dentro de comillas no separa el campo', 'los enteros y los reales se convierten', 'el texto se conserva', 'un CSV solo con cabecera da `[]`'],
         why='Dividir por comas a mano rompe con campos entre comillas; el módulo `csv` implementa las reglas de RFC 4180. La conversión intenta `int` antes que `float` para conservar el tipo más estricto, y deja el texto como está.'),
    dict(ch=3, lang='python', level='ADVANCED',
         prompt='Escribe `merge_config(*layers)` que combine capas de configuración (diccionarios anidados, la última prevalece) con fusión profunda: dos diccionarios se fusionan recursivamente y cualquier otro valor se sustituye. No debe modificar las capas de entrada. Después, `load_toml(text)` con `tomllib`. Comprueba con valores por defecto, un fichero TOML y variables de entorno simuladas.',
         code='''import tomllib


def merge_config(*layers):
    merged = {}
    for layer in layers:
        for key, value in layer.items():
            if isinstance(value, dict) and isinstance(merged.get(key), dict):
                merged[key] = merge_config(merged[key], value)
            elif isinstance(value, dict):
                merged[key] = merge_config(value)
            else:
                merged[key] = value
    return merged


def load_toml(text):
    return tomllib.loads(text)''',
         harness='''defaults = {"server": {"host": "localhost", "port": 8000}, "debug": False, "tags": ["a"]}
file_layer = load_toml('[server]\\nport = 9000\\n[db]\\nurl = "sqlite://x"\\n')
env_layer = {"debug": True, "tags": ["b", "c"]}
config = merge_config(defaults, file_layer, env_layer)
assert config == {"server": {"host": "localhost", "port": 9000}, "debug": True, "tags": ["b", "c"], "db": {"url": "sqlite://x"}}
assert defaults["server"]["port"] == 8000 and defaults["tags"] == ["a"]
config["server"]["host"] = "otro"
assert defaults["server"]["host"] == "localhost"
assert merge_config() == {}
print("OK")''',
         tests=['las capas se fusionan en profundidad con prioridad a la última', 'las listas se sustituyen, no se concatenan', 'las capas de entrada no se modifican', 'modificar el resultado no afecta a las capas', 'sin capas el resultado es `{}`'],
         why='Una fusión superficial pisaría `server` entero al leer solo el puerto. La profunda recorre los diccionarios anidados. Copiar también los diccionarios que solo aparecen en una capa evita que el resultado comparta estructuras con las entradas.'),
    # ---- capítulo 4: teoría relacional
    dict(ch=4, lang='python', level='INTERMEDIATE',
         prompt='Escribe `closure(attrs, fds)` que calcule el cierre de un conjunto de atributos respecto a un conjunto de dependencias funcionales (cada una es un par `(izquierda, derecha)` de conjuntos), y `is_superkey(attrs, relation, fds)`. Comprueba con `R(A,B,C,D)`, `A->B`, `B->C`: el cierre de `{A}` es `{A,B,C}` y `{A,D}` es superclave.',
         code='''def closure(attrs, fds):
    result = set(attrs)
    changed = True
    while changed:
        changed = False
        for left, right in fds:
            if set(left) <= result and not set(right) <= result:
                result |= set(right)
                changed = True
    return result


def is_superkey(attrs, relation, fds):
    return closure(attrs, fds) >= set(relation)''',
         harness='''fds = [({"A"}, {"B"}), ({"B"}, {"C"})]
relation = {"A", "B", "C", "D"}
assert closure({"A"}, fds) == {"A", "B", "C"}
assert closure({"D"}, fds) == {"D"}
assert closure({"B"}, fds) == {"B", "C"}
assert is_superkey({"A", "D"}, relation, fds)
assert not is_superkey({"A"}, relation, fds)
assert closure(set(), fds) == set()
print("OK")''',
         tests=['el cierre de `{A}` es `{A, B, C}`', 'el cierre de `{D}` es `{D}`', '`{A, D}` es superclave', '`{A}` no lo es', 'el cierre del conjunto vacío es vacío'],
         why='El algoritmo añade al conjunto los atributos que determinan las dependencias cuyo lado izquierdo ya está contenido, hasta que ninguna añade nada nuevo. Un conjunto es superclave si su cierre contiene todos los atributos de la relación.'),
    dict(ch=4, lang='python', level='ADVANCED',
         prompt='Escribe `candidate_keys(relation, fds)` que devuelva todas las claves candidatas (superclaves mínimas) como lista de conjuntos ordenados, y `bcnf_violations(relation, fds)` que devuelva las dependencias cuyo lado izquierdo no es superclave. Comprueba con `R(A,B,C)`, `A->B`, `B->C` (clave `{A}`, viola BCNF `B->C`).',
         code='''from itertools import combinations


def closure(attrs, fds):
    result = set(attrs)
    changed = True
    while changed:
        changed = False
        for left, right in fds:
            if set(left) <= result and not set(right) <= result:
                result |= set(right)
                changed = True
    return result


def candidate_keys(relation, fds):
    relation = sorted(relation)
    keys = []
    for size in range(1, len(relation) + 1):
        for combo in combinations(relation, size):
            if any(set(k) <= set(combo) for k in keys):
                continue
            if closure(combo, fds) >= set(relation):
                keys.append(combo)
    return [set(k) for k in keys]


def bcnf_violations(relation, fds):
    full = set(relation)
    return [(l, r) for l, r in fds if not set(r) <= set(l) and closure(l, fds) < full]''',
         harness='''fds = [({"A"}, {"B"}), ({"B"}, {"C"})]
assert candidate_keys({"A", "B", "C"}, fds) == [{"A"}]
assert bcnf_violations({"A", "B", "C"}, fds) == [({"B"}, {"C"})]
fds2 = [({"A", "B"}, {"C"}), ({"C"}, {"A"})]
keys = candidate_keys({"A", "B", "C"}, fds2)
assert sorted(sorted(k) for k in keys) == [["A", "B"], ["B", "C"]]
assert bcnf_violations({"A", "B", "C"}, fds2) == [({"C"}, {"A"})]
assert candidate_keys({"X", "Y"}, []) == [{"X", "Y"}]
print("OK")''',
         tests=['`R(A,B,C)` con `A->B`, `B->C` tiene como única clave `{A}`', '`B->C` viola BCNF', 'con `AB->C` y `C->A` las claves son `{A,B}` y `{B,C}`', 'sin dependencias la única clave es toda la relación'],
         why='Se prueban los subconjuntos por tamaño creciente y se descartan los que contienen una clave ya encontrada, de modo que solo quedan las mínimas. Una dependencia viola BCNF si no es trivial y su lado izquierdo no es superclave. Con muchos atributos el método es exponencial: es válido para esquemas pequeños.'),
    dict(ch=4, lang='sql', level='INTERMEDIATE',
         prompt='Dada una tabla `enrol(student, course, teacher)` con la dependencia `course -> teacher`, escribe una consulta que encuentre los cursos que violan esa dependencia (cursos con más de un profesor distinto). Comprueba con datos que contienen un curso inconsistente.',
         code='''SELECT course, COUNT(DISTINCT teacher) AS teachers
FROM enrol
GROUP BY course
HAVING COUNT(DISTINCT teacher) > 1''',
         harness='''CREATE TABLE enrol(student TEXT, course TEXT, teacher TEXT);
INSERT INTO enrol VALUES ('a','bd','ruiz'),('b','bd','ruiz'),('c','so','paz'),('d','so','lara'),('e','so','paz');
CREATE VIEW answer AS
{{code}};
SELECT CASE WHEN (SELECT group_concat(course || ':' || teachers) FROM answer) = 'so:2' THEN 'OK' ELSE 'FAIL' END;''',
         tests=['`bd` tiene un solo profesor y no aparece', '`so` tiene dos profesores y aparece con 2'],
         why='Comprobar una dependencia funcional en los datos equivale a buscar grupos con más de un valor distinto en el lado derecho. Esto detecta violaciones en los datos actuales, pero no demuestra que la dependencia sea una regla del dominio.'),
    # ---- capítulo 5: almacenamiento y transacciones
    dict(ch=5, lang='python', level='INTERMEDIATE',
         prompt='Escribe `merge_runs(newer, older)` que combine dos ejecuciones ordenadas de un árbol LSM (listas de pares `(clave, valor)` ordenadas por clave, donde `valor` puede ser `None` como lápida de borrado) y devuelva la ejecución compactada: gana la más reciente, y las lápidas se eliminan. Comprueba con claves repetidas y borradas.',
         code='''def merge_runs(newer, older):
    merged = {}
    for key, value in older:
        merged[key] = value
    for key, value in newer:
        merged[key] = value
    return [(k, merged[k]) for k in sorted(merged) if merged[k] is not None]''',
         harness='''older = [("a", 1), ("b", 2), ("c", 3)]
newer = [("b", None), ("c", 30), ("d", 4)]
assert merge_runs(newer, older) == [("a", 1), ("c", 30), ("d", 4)]
assert merge_runs([], older) == older
assert merge_runs([("a", None)], [("a", 1)]) == []
assert merge_runs([], []) == []
print("OK")''',
         tests=['`b` borrada desaparece', '`c` toma el valor nuevo', '`d` se añade', 'una ejecución nueva vacía conserva la antigua', 'una lápida sobre la única clave deja la ejecución vacía'],
         why='En un LSM las escrituras van a ejecuciones ordenadas e inmutables, y una lectura mira primero la más reciente. Una lápida es el valor de un borrado, que hay que conservar hasta compactar con todas las ejecuciones más antiguas; aquí se elimina porque `older` es la más antigua.'),
    dict(ch=5, lang='python', level='ADVANCED',
         prompt='Implementa la clase `MVCCStore` con `begin()` (devuelve un identificador de transacción), `read(tx, key)`, `write(tx, key, value)` y `commit(tx)`. Cada transacción ve una instantánea: solo las escrituras confirmadas antes de su inicio. Dos transacciones que escriben la misma clave entran en conflicto: el segundo `commit` debe lanzar `ConflictError`. Comprueba aislamiento y conflicto.',
         code='''class ConflictError(Exception):
    pass


class MVCCStore:
    def __init__(self):
        self.versions = {}
        self.clock = 0
        self.txs = {}

    def begin(self):
        tx = len(self.txs) + 1
        self.txs[tx] = {"start": self.clock, "writes": {}}
        return tx

    def read(self, tx, key):
        state = self.txs[tx]
        if key in state["writes"]:
            return state["writes"][key]
        visible = [(ts, v) for ts, v in self.versions.get(key, []) if ts <= state["start"]]
        return visible[-1][1] if visible else None

    def write(self, tx, key, value):
        self.txs[tx]["writes"][key] = value

    def commit(self, tx):
        state = self.txs[tx]
        for key in state["writes"]:
            versions = self.versions.get(key, [])
            if versions and versions[-1][0] > state["start"]:
                raise ConflictError(key)
        self.clock += 1
        for key, value in state["writes"].items():
            self.versions.setdefault(key, []).append((self.clock, value))''',
         harness='''store = MVCCStore()
t0 = store.begin()
store.write(t0, "x", 1)
store.commit(t0)
t1, t2 = store.begin(), store.begin()
store.write(t1, "x", 10)
assert store.read(t1, "x") == 10
assert store.read(t2, "x") == 1
store.commit(t1)
assert store.read(t2, "x") == 1
assert store.read(store.begin(), "x") == 10
store.write(t2, "x", 20)
try:
    store.commit(t2)
except ConflictError:
    pass
else:
    raise AssertionError("debe haber conflicto")
t4 = store.begin()
store.write(t4, "y", 5)
store.commit(t4)
assert store.read(store.begin(), "y") == 5
print("OK")''',
         tests=['cada transacción lee su instantánea', 'una transacción lee sus propias escrituras', 'una confirmación posterior no cambia lo que ve una transacción abierta', 'dos escrituras concurrentes sobre la misma clave producen `ConflictError`', 'escribir claves distintas no entra en conflicto'],
         why='MVCC guarda varias versiones de cada clave con una marca de tiempo de confirmación. Cada transacción lee las versiones anteriores a su inicio, de modo que las lecturas no bloquean ni son bloqueadas. El conflicto "el primero que confirma gana" detecta las actualizaciones perdidas.'),
    dict(ch=5, lang='python', level='ADVANCED',
         prompt='Escribe un registro de escritura anticipada: `class Wal` con `append(op)` que escriba líneas `"clave=valor"` en una lista de texto (simulando el disco) y `recover(lines)` que reconstruya el diccionario ignorando una última línea incompleta por un corte (sin `\\n` final). Comprueba una recuperación normal y una con la última línea truncada.',
         code='''class Wal:
    def __init__(self):
        self.disk = ""

    def append(self, key, value):
        self.disk += f"{key}={value}\\n"

    def crash(self, keep):
        self.disk = self.disk[:keep]

    @staticmethod
    def recover(disk):
        state = {}
        for line in disk.split("\\n")[:-1]:
            if "=" not in line:
                continue
            key, value = line.split("=", 1)
            state[key] = value
        return state''',
         harness='''wal = Wal()
wal.append("a", "1")
wal.append("b", "2")
wal.append("a", "3")
assert Wal.recover(wal.disk) == {"a": "3", "b": "2"}
wal.crash(len(wal.disk) - 2)
assert Wal.recover(wal.disk) == {"a": "1", "b": "2"}
assert Wal.recover("") == {}
assert Wal.recover("x=1\\nsin-final") == {"x": "1"}
print("OK")''',
         tests=['la recuperación normal devuelve el último valor de cada clave', 'una última línea truncada se ignora', 'un registro vacío da un estado vacío', 'una línea sin salto de línea final no se aplica'],
         why='Una operación solo se considera durable cuando su línea está completa (termina en salto de línea). Tras un fallo, la recuperación aplica en orden las líneas completas y descarta la cola parcial, de modo que el estado resultante es el de la última operación confirmada.'),
    # ---- capítulo 6: distribuidos
    dict(ch=6, lang='python', level='INTERMEDIATE',
         prompt='Implementa `HashRing` con hash consistente: `add(node)`, `remove(node)` y `lookup(key)` (nodo responsable), usando 100 puntos virtuales por nodo y `hashlib.md5`. Comprueba que al añadir un décimo nodo a nueve solo cambia de responsable una fracción de las claves cercana a 1/10 y que quitarlo restituye la asignación original.',
         code='''import bisect
import hashlib


def _hash(text):
    return int(hashlib.md5(text.encode()).hexdigest(), 16)


class HashRing:
    def __init__(self, replicas=100):
        self.replicas = replicas
        self.points = []
        self.owner = {}

    def add(self, node):
        for i in range(self.replicas):
            point = _hash(f"{node}#{i}")
            bisect.insort(self.points, point)
            self.owner[point] = node

    def remove(self, node):
        for i in range(self.replicas):
            point = _hash(f"{node}#{i}")
            self.points.remove(point)
            del self.owner[point]

    def lookup(self, key):
        index = bisect.bisect(self.points, _hash(key)) % len(self.points)
        return self.owner[self.points[index]]''',
         harness='''ring = HashRing()
for n in range(9):
    ring.add(f"nodo{n}")
keys = [f"clave{i}" for i in range(5000)]
before = {k: ring.lookup(k) for k in keys}
ring.add("nodo9")
moved = sum(1 for k in keys if ring.lookup(k) != before[k])
assert 0.04 < moved / len(keys) < 0.18, moved / len(keys)
assert all(ring.lookup(k) == "nodo9" for k in keys if ring.lookup(k) != before[k])
ring.remove("nodo9")
assert all(ring.lookup(k) == before[k] for k in keys)
print("OK")''',
         tests=['añadir un décimo nodo mueve alrededor del 10 % de las claves', 'las claves que cambian de dueño pasan al nodo nuevo', 'quitar el nodo restituye la asignación original'],
         why='Cada nodo ocupa muchos puntos del anillo y una clave pertenece al primer punto que la sigue. Al añadir un nodo solo le corresponden las claves de sus nuevos puntos, aproximadamente 1/10 del total. Con un reparto por módulo se movería casi todo.'),
    dict(ch=6, lang='python', level='INTERMEDIATE',
         prompt='Escribe `compare(a, b)` para relojes vectoriales (diccionarios nodo a contador) que devuelva `"before"`, `"after"`, `"equal"` o `"concurrent"`, y `merge(a, b)` que devuelva el máximo componente a componente. Comprueba los cuatro casos.',
         code='''def compare(a, b):
    nodes = set(a) | set(b)
    le = all(a.get(n, 0) <= b.get(n, 0) for n in nodes)
    ge = all(a.get(n, 0) >= b.get(n, 0) for n in nodes)
    if le and ge:
        return "equal"
    if le:
        return "before"
    if ge:
        return "after"
    return "concurrent"


def merge(a, b):
    return {n: max(a.get(n, 0), b.get(n, 0)) for n in set(a) | set(b)}''',
         harness='''assert compare({"a": 1}, {"a": 2}) == "before"
assert compare({"a": 2, "b": 1}, {"a": 1}) == "after"
assert compare({"a": 1}, {"a": 1, "b": 0}) == "equal"
assert compare({"a": 2, "b": 0}, {"a": 1, "b": 1}) == "concurrent"
assert merge({"a": 2, "b": 0}, {"a": 1, "b": 1, "c": 5}) == {"a": 2, "b": 1, "c": 5}
assert compare({}, {}) == "equal"
print("OK")''',
         tests=['`{a:1}` es anterior a `{a:2}`', '`{a:2,b:1}` es posterior a `{a:1}`', 'un contador ausente equivale a 0', 'dos relojes que cada uno supera al otro en un nodo son concurrentes', '`merge` toma el máximo de cada componente'],
         why='Un reloj vectorial registra cuántos eventos ha visto cada nodo. Un evento precede a otro si todos sus contadores son menores o iguales; si ninguno domina al otro, los eventos son concurrentes y hay que resolver el conflicto. No se pueden ordenar con un solo reloj de pared.'),
    dict(ch=6, lang='python', level='ADVANCED',
         prompt='Simula una base replicada con `N` réplicas: `class Cluster` con `write(key, value, w, down)` que escribe en `w` réplicas disponibles (con una versión creciente) y `read(key, r, down)` que consulta `r` réplicas disponibles y devuelve el valor de mayor versión. Si no hay suficientes réplicas, lanza `Unavailable`. Comprueba que con `R + W > N` una lectura siempre ve la última escritura aunque falle alguna réplica.',
         code='''class Unavailable(Exception):
    pass


class Cluster:
    def __init__(self, n):
        self.n = n
        self.replicas = [dict() for _ in range(n)]
        self.version = 0

    def write(self, key, value, w, down=()):
        up = [i for i in range(self.n) if i not in down]
        if len(up) < w:
            raise Unavailable("faltan replicas para escribir")
        self.version += 1
        for i in up[:w]:
            self.replicas[i][key] = (self.version, value)

    def read(self, key, r, down=()):
        up = [i for i in range(self.n) if i not in down]
        if len(up) < r:
            raise Unavailable("faltan replicas para leer")
        found = [self.replicas[i][key] for i in up[-r:] if key in self.replicas[i]]
        return max(found)[1] if found else None''',
         harness='''c = Cluster(5)
c.write("k", "v1", w=3)
c.write("k", "v2", w=3, down=(0,))
for down in [(), (1,), (4,), (0, 1)]:
    assert c.read("k", r=3, down=down) == "v2", down
try:
    c.write("k", "x", w=3, down=(0, 1, 2))
except Unavailable:
    pass
else:
    raise AssertionError("debe ser no disponible")
try:
    c.read("k", r=3, down=(0, 1, 2))
except Unavailable:
    pass
else:
    raise AssertionError("lectura no disponible")
assert c.read("zzz", r=3) is None
print("OK")''',
         tests=['con `R + W > N` las lecturas ven siempre la última escritura aunque falten réplicas', 'sin réplicas suficientes la escritura lanza `Unavailable`', 'sin réplicas suficientes la lectura lanza `Unavailable`', 'una clave inexistente devuelve `None`'],
         why='Si el conjunto de lectura y el de escritura suman más que `N`, comparten al menos una réplica, que tiene la versión más reciente. Aquí `3 + 3 > 5`. El coste es disponibilidad: si faltan réplicas para completar el quórum, la operación no puede hacerse.'),
    # ---- capítulo 7: frontend
    dict(ch=7, lang='js', level='INTERMEDIATE',
         prompt='Escribe `diff(oldNode, newNode)` para un DOM virtual sencillo, donde un nodo es una cadena o `{ tag, props, children }`. Debe devolver una lista de parches `{ type: "REPLACE"|"PROPS"|"TEXT"|"ADD"|"REMOVE", path, ... }` mínima: no replicar un subárbol si solo cambia una propiedad. Comprueba cambio de texto, de propiedad, de etiqueta y adición/eliminación de hijos.',
         code='''function diff(oldNode, newNode, path = []) {
  if (oldNode === undefined) return [{ type: "ADD", path }];
  if (newNode === undefined) return [{ type: "REMOVE", path }];
  if (typeof oldNode === "string" || typeof newNode === "string") {
    return oldNode === newNode ? [] : [{ type: "TEXT", path, text: newNode }];
  }
  if (oldNode.tag !== newNode.tag) return [{ type: "REPLACE", path }];
  const patches = [];
  const keys = new Set([...Object.keys(oldNode.props || {}), ...Object.keys(newNode.props || {})]);
  for (const key of keys) {
    if ((oldNode.props || {})[key] !== (newNode.props || {})[key]) {
      patches.push({ type: "PROPS", path, key, value: (newNode.props || {})[key] });
    }
  }
  const count = Math.max(oldNode.children.length, newNode.children.length);
  for (let i = 0; i < count; i++) {
    patches.push(...diff(oldNode.children[i], newNode.children[i], [...path, i]));
  }
  return patches;
}''',
         harness='''const assert = require("node:assert");
const h = (tag, props, ...children) => ({ tag, props, children });
const a = h("ul", { class: "x" }, h("li", {}, "uno"), h("li", {}, "dos"));
assert.deepStrictEqual(diff(a, a), []);
assert.deepStrictEqual(diff(a, h("ul", { class: "y" }, h("li", {}, "uno"), h("li", {}, "dos"))), [{ type: "PROPS", path: [], key: "class", value: "y" }]);
assert.deepStrictEqual(diff(a, h("ul", { class: "x" }, h("li", {}, "uno"), h("li", {}, "tres"))), [{ type: "TEXT", path: [1, 0], text: "tres" }]);
assert.deepStrictEqual(diff(a, h("ol", { class: "x" }, h("li", {}, "uno"), h("li", {}, "dos"))), [{ type: "REPLACE", path: [] }]);
assert.deepStrictEqual(diff(a, h("ul", { class: "x" }, h("li", {}, "uno"))), [{ type: "REMOVE", path: [1] }]);
assert.deepStrictEqual(diff(h("ul", {}), h("ul", {}, h("li", {}))), [{ type: "ADD", path: [0] }]);
console.log("OK");''',
         tests=['dos árboles iguales no producen parches', 'un cambio de clase produce solo un parche de propiedad', 'un cambio de texto afecta solo a ese hijo', 'una etiqueta distinta reemplaza el subárbol', 'quitar o añadir hijos produce `REMOVE` o `ADD`'],
         why='Comparar el árbol anterior y el nuevo permite aplicar al DOM real solo lo que cambió, que es lo caro. Comparar nodo a nodo, en lugar de buscar el mínimo exacto, hace el algoritmo lineal; para listas largas se añaden claves (`key`) que identifican cada elemento.'),
    dict(ch=7, lang='js', level='ADVANCED',
         prompt='Implementa `signal(initial)`, `effect(fn)` y `computed(fn)` mínimos para reactividad por señales: una señal devuelve `[get, set]`; un `effect` se reejecuta cuando cambia una señal que leyó; `computed` devuelve un `get` memoizado. Comprueba con un contador: cambiar `a` reejecuta el efecto, cambiar a un valor igual no, y `computed` no recalcula si sus dependencias no cambian.',
         code='''let current = null;

function signal(initial) {
  let value = initial;
  const subscribers = new Set();
  const get = () => {
    if (current) subscribers.add(current);
    return value;
  };
  const set = (next) => {
    if (Object.is(next, value)) return;
    value = next;
    [...subscribers].forEach((run) => run());
  };
  return [get, set];
}

function effect(fn) {
  const run = () => {
    const previous = current;
    current = run;
    try {
      fn();
    } finally {
      current = previous;
    }
  };
  run();
}

function computed(fn) {
  const [get, set] = signal(undefined);
  effect(() => set(fn()));
  return get;
}''',
         harness='''const assert = require("node:assert");
const [a, setA] = signal(1);
const [b, setB] = signal(10);
let runs = 0;
let computeRuns = 0;
const sum = computed(() => { computeRuns += 1; return a() + b(); });
const seen = [];
effect(() => { runs += 1; seen.push(sum()); });
assert.deepStrictEqual(seen, [11]);
setA(2);
assert.deepStrictEqual(seen, [11, 12]);
setA(2);
assert.strictEqual(runs, 2);
setB(20);
assert.deepStrictEqual(seen, [11, 12, 22]);
assert.strictEqual(computeRuns, 3);
console.log("OK");''',
         tests=['el efecto se ejecuta al crearse', 'cambiar una señal reejecuta lo que depende de ella', 'asignar el mismo valor no reejecuta nada', '`computed` solo recalcula cuando cambia una dependencia'],
         why='Una señal recuerda quién la leyó mientras había un efecto en ejecución y lo avisa al cambiar. Eso da reactividad de grano fino: solo se reejecuta lo que depende del valor, sin comparar árboles. `Object.is` evita avisos cuando el valor no cambia.'),
    dict(ch=7, lang='js', level='INTERMEDIATE',
         prompt='Escribe `createStore(reducer, initial)` al estilo Redux, con `getState()`, `dispatch(action)` y `subscribe(listener)` (que devuelve una función para darse de baja). El estado no se modifica: el reductor devuelve uno nuevo. Comprueba un reductor de contador, la suscripción y la baja.',
         code='''function createStore(reducer, initial) {
  let state = initial;
  const listeners = new Set();
  return {
    getState: () => state,
    dispatch(action) {
      state = reducer(state, action);
      listeners.forEach((l) => l());
      return action;
    },
    subscribe(listener) {
      listeners.add(listener);
      return () => listeners.delete(listener);
    },
  };
}''',
         harness='''const assert = require("node:assert");
const reducer = (state, action) => {
  switch (action.type) {
    case "inc": return { ...state, count: state.count + 1 };
    case "add": return { ...state, count: state.count + action.n };
    default: return state;
  }
};
const store = createStore(reducer, { count: 0 });
const before = store.getState();
const calls = [];
const off = store.subscribe(() => calls.push(store.getState().count));
store.dispatch({ type: "inc" });
store.dispatch({ type: "add", n: 5 });
assert.strictEqual(store.getState().count, 6);
assert.strictEqual(before.count, 0);
off();
store.dispatch({ type: "inc" });
assert.deepStrictEqual(calls, [1, 6]);
store.dispatch({ type: "otro" });
assert.strictEqual(store.getState().count, 7);
console.log("OK");''',
         tests=['`inc` y `add` suman al estado', 'el estado anterior no se modifica', 'el suscriptor se llama tras cada acción', 'tras darse de baja ya no se le llama', 'una acción desconocida conserva el estado'],
         why='Un reductor es una función pura `(estado, acción)` a un estado nuevo; devolver un objeto nuevo permite detectar cambios por identidad y recuperar estados anteriores. El almacén solo coordina: guarda el estado, aplica el reductor y avisa a los suscriptores.'),
    # ---- capítulo 8: backend
    dict(ch=8, lang='python', level='INTERMEDIATE',
         prompt='Escribe `make_token(payload, secret)` y `verify_token(token, secret)` para un token firmado al estilo JWT con `hmac` y `hashlib.sha256`: `base64url(payload JSON).base64url(firma)`. `verify_token` debe devolver el payload o `None` si la firma no coincide, usando comparación en tiempo constante (`hmac.compare_digest`). Comprueba un token válido, uno manipulado y una clave incorrecta.',
         code='''import base64
import hashlib
import hmac
import json


def _b64(data):
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode()


def _unb64(text):
    return base64.urlsafe_b64decode(text + "=" * (-len(text) % 4))


def make_token(payload, secret):
    body = _b64(json.dumps(payload, sort_keys=True).encode())
    signature = hmac.new(secret.encode(), body.encode(), hashlib.sha256).digest()
    return f"{body}.{_b64(signature)}"


def verify_token(token, secret):
    try:
        body, signature = token.split(".")
        expected = hmac.new(secret.encode(), body.encode(), hashlib.sha256).digest()
        if not hmac.compare_digest(expected, _unb64(signature)):
            return None
        return json.loads(_unb64(body))
    except (ValueError, TypeError):
        return None''',
         harness='''token = make_token({"user": "ana", "admin": False}, "secreto")
assert verify_token(token, "secreto") == {"admin": False, "user": "ana"}
body, sig = token.split(".")
forged = make_token({"user": "ana", "admin": True}, "otra").split(".")[0] + "." + sig
assert verify_token(forged, "secreto") is None
assert verify_token(token, "incorrecta") is None
assert verify_token("basura", "secreto") is None
assert verify_token(token + "x", "secreto") is None
print("OK")''',
         tests=['un token válido devuelve su payload', 'un payload manipulado con la firma original se rechaza', 'una clave incorrecta se rechaza', 'texto sin formato devuelve `None`'],
         why='La firma HMAC prueba que el contenido no se modificó sin conocer la clave; no lo cifra, así que el payload es legible. `compare_digest` evita revelar, por el tiempo que tarda, cuántos bytes coinciden. Un servicio real también debe comprobar la caducidad del token.'),
    dict(ch=8, lang='python', level='INTERMEDIATE',
         prompt='Escribe `TokenBucket(capacity, rate)` con `allow(now)` que devuelva si se admite una petición en el instante `now` (segundos): el cubo se rellena a `rate` fichas por segundo hasta `capacity` y cada petición consume una. Comprueba la ráfaga inicial, el rechazo y la recuperación con el tiempo. Pasa el reloj como parámetro para que sea comprobable.',
         code='''class TokenBucket:
    def __init__(self, capacity, rate):
        self.capacity = capacity
        self.rate = rate
        self.tokens = float(capacity)
        self.last = None

    def allow(self, now):
        if self.last is not None:
            self.tokens = min(self.capacity, self.tokens + (now - self.last) * self.rate)
        self.last = now
        if self.tokens >= 1:
            self.tokens -= 1
            return True
        return False''',
         harness='''bucket = TokenBucket(capacity=3, rate=1.0)
assert [bucket.allow(0) for _ in range(5)] == [True, True, True, False, False]
assert bucket.allow(0.5) is False
assert bucket.allow(1.0) is True
assert bucket.allow(1.0) is False
assert [bucket.allow(100) for _ in range(4)] == [True, True, True, False]
print("OK")''',
         tests=['una ráfaga inicial admite `capacity` peticiones', 'la siguiente se rechaza', 'tras 1 s se recupera una ficha', 'el cubo nunca supera su capacidad'],
         why='El cubo permite ráfagas de hasta `capacity` peticiones y una tasa sostenida de `rate` por segundo. Recibir el tiempo como argumento, en lugar de leer el reloj, hace la clase determinista y fácil de probar.'),
    dict(ch=8, lang='python', level='ADVANCED',
         prompt='Escribe un pequeño servidor HTTP con `http.server` en un hilo: `GET /items/<id>` devuelve JSON con el elemento (404 si no existe) y `POST /items` crea uno con el cuerpo JSON (400 si el JSON es inválido), devolviendo 201. Comprueba con `urllib` los cuatro casos contra un puerto libre.',
         code='''import json
from http.server import BaseHTTPRequestHandler, HTTPServer

ITEMS = {1: {"id": 1, "name": "uno"}}


class Handler(BaseHTTPRequestHandler):
    def _send(self, status, body):
        data = json.dumps(body).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self):
        parts = self.path.strip("/").split("/")
        if len(parts) == 2 and parts[0] == "items" and parts[1].isdigit() and int(parts[1]) in ITEMS:
            self._send(200, ITEMS[int(parts[1])])
        else:
            self._send(404, {"error": "no encontrado"})

    def do_POST(self):
        length = int(self.headers.get("Content-Length", 0))
        try:
            item = json.loads(self.rfile.read(length))
            if not isinstance(item, dict) or "name" not in item:
                raise ValueError("falta name")
        except ValueError:
            self._send(400, {"error": "json invalido"})
            return
        new_id = max(ITEMS) + 1
        ITEMS[new_id] = {"id": new_id, "name": item["name"]}
        self._send(201, ITEMS[new_id])

    def log_message(self, *args):
        pass''',
         harness='''import threading
import urllib.error
import urllib.request

server = HTTPServer(("127.0.0.1", 0), Handler)
threading.Thread(target=server.serve_forever, daemon=True).start()
base = f"http://127.0.0.1:{server.server_port}"


def call(method, path, body=None):
    request = urllib.request.Request(base + path, data=body, method=method)
    try:
        with urllib.request.urlopen(request) as response:
            return response.status, json.loads(response.read())
    except urllib.error.HTTPError as error:
        return error.code, json.loads(error.read())


assert call("GET", "/items/1") == (200, {"id": 1, "name": "uno"})
assert call("GET", "/items/9")[0] == 404
assert call("POST", "/items", b'{"name": "dos"}') == (201, {"id": 2, "name": "dos"})
assert call("GET", "/items/2")[1]["name"] == "dos"
assert call("POST", "/items", b"no es json")[0] == 400
assert call("POST", "/items", b'{"otro": 1}')[0] == 400
server.shutdown()
print("OK")''',
         tests=['`GET /items/1` devuelve 200 con el elemento', 'un elemento inexistente devuelve 404', '`POST` con JSON válido devuelve 201 y el nuevo elemento', 'el elemento creado se puede leer', 'JSON inválido o sin `name` devuelve 400'],
         why='Cada código de estado dice al cliente qué ha pasado sin que tenga que leer el cuerpo: 200 correcto, 201 creado, 400 petición mal formada, 404 no existe. Validar la entrada antes de modificar el estado evita crear elementos a medias. Se usa el puerto 0 para que el sistema asigne uno libre.'),
]
