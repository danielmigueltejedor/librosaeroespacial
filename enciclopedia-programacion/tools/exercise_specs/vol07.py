"""Programming exercises of volume 7 (SQL, shell, PHP, Ruby, Haskell, OCaml, Elixir, Clojure, Scala, Julia, R, Lua, Perl, Prolog).

Each reference program runs with the real interpreter, compiler or database engine."""

SALES = '''CREATE TABLE sales(region TEXT, seller TEXT, amount INTEGER);
INSERT INTO sales VALUES
 ('norte','ana',100),('norte','luis',300),('norte','eva',200),
 ('sur','mar',50),('sur','pau',70),('este','tom',90);'''

EXERCISES = [
    # ---- capítulo 1: SQL
    dict(ch=1, lang='sql', level='INTERMEDIATE',
         prompt='Con la tabla `sales(region, seller, amount)`, escribe una consulta que devuelva, para cada región, los dos vendedores con mayor importe (columnas `region`, `seller`, `amount`), usando una función de ventana. Comprueba el resultado con los datos de ejemplo.',
         code='''SELECT region, seller, amount
FROM (
    SELECT region, seller, amount,
           ROW_NUMBER() OVER (PARTITION BY region ORDER BY amount DESC, seller) AS rn
    FROM sales
)
WHERE rn <= 2''',
         harness=SALES + '''
CREATE VIEW answer AS
{{code}};
SELECT CASE WHEN (SELECT group_concat(region || ':' || seller || ':' || amount, ',') FROM (SELECT * FROM answer ORDER BY region, amount DESC)) =
  'este:tom:90,norte:luis:300,norte:eva:200,sur:pau:70,sur:mar:50' THEN 'OK' ELSE 'FAIL' END;''',
         tests=['`norte` devuelve `luis` (300) y `eva` (200)', '`sur` devuelve `pau` (70) y `mar` (50)', '`este` solo tiene un vendedor y lo devuelve'],
         why='`ROW_NUMBER() OVER (PARTITION BY ...)` numera las filas dentro de cada grupo según el orden indicado, sin colapsarlas como haría `GROUP BY`. Filtrar por `rn <= 2` en una consulta exterior conserva los dos primeros de cada región. El desempate por `seller` hace el resultado determinista.'),
    dict(ch=1, lang='sql', level='INTERMEDIATE',
         prompt='Con `employee(id, name, boss_id)`, escribe con una CTE recursiva una consulta que devuelva, para cada empleado, su nombre y su profundidad en la jerarquía (el jefe sin superior tiene profundidad 0), ordenada por profundidad y nombre. Comprueba con una jerarquía de cuatro niveles.',
         code='''WITH RECURSIVE tree(id, name, depth) AS (
    SELECT id, name, 0 FROM employee WHERE boss_id IS NULL
    UNION ALL
    SELECT e.id, e.name, t.depth + 1
    FROM employee e JOIN tree t ON e.boss_id = t.id
)
SELECT name, depth FROM tree ORDER BY depth, name''',
         harness='''CREATE TABLE employee(id INTEGER, name TEXT, boss_id INTEGER);
INSERT INTO employee VALUES (1,'jefa',NULL),(2,'bea',1),(3,'carl',1),(4,'dani',2),(5,'eli',4);
CREATE VIEW answer AS
{{code}};
SELECT CASE WHEN (SELECT group_concat(name || depth, ',') FROM answer) = 'jefa0,bea1,carl1,dani2,eli3' THEN 'OK' ELSE 'FAIL' END;''',
         tests=['la jefa tiene profundidad 0', 'bea y carl tienen profundidad 1', 'dani 2 y eli 3', 'el resultado está ordenado por profundidad y nombre'],
         why='La parte inicial de la CTE toma las raíces y la parte recursiva añade los hijos de las filas ya encontradas hasta que no aparecen filas nuevas. `UNION ALL` evita eliminar duplicados en cada iteración; si los datos tuvieran un ciclo, la consulta no terminaría sin un límite de profundidad.'),
    dict(ch=1, lang='sql', level='INTERMEDIATE',
         prompt='Con `customer(id, name)` y `orders(customer_id, total)`, escribe una consulta que devuelva el nombre de cada cliente y la suma de sus pedidos, mostrando 0 para los que no han comprado nada (no `NULL`). Comprueba que incluye a los clientes sin pedidos.',
         code='''SELECT c.name, COALESCE(SUM(o.total), 0) AS spent
FROM customer c
LEFT JOIN orders o ON o.customer_id = c.id
GROUP BY c.id, c.name
ORDER BY c.name''',
         harness='''CREATE TABLE customer(id INTEGER, name TEXT);
CREATE TABLE orders(customer_id INTEGER, total INTEGER);
INSERT INTO customer VALUES (1,'ana'),(2,'bruno'),(3,'carla');
INSERT INTO orders VALUES (1,10),(1,15),(3,40);
CREATE VIEW answer AS
{{code}};
SELECT CASE WHEN (SELECT group_concat(name || '=' || spent, ',') FROM answer) = 'ana=25,bruno=0,carla=40' THEN 'OK' ELSE 'FAIL' END;''',
         tests=['`ana` suma 25', '`bruno`, sin pedidos, aparece con 0', '`carla` suma 40'],
         why='Un `JOIN` interno descartaría a los clientes sin pedidos; `LEFT JOIN` los conserva con columnas `NULL`. `SUM` de ningún valor es `NULL`, y `COALESCE` lo convierte en 0. Es el caso típico de lógica trivaluada: un `NULL` no es igual a nada, ni siquiera a otro `NULL`.'),
    # ---- capítulo 2: Bash
    dict(ch=2, lang='bash', level='INTERMEDIATE',
         prompt='Escribe en Bash la función `count_matches PATRON FICHERO` que imprima cuántas líneas del fichero contienen el patrón (como cadena fija, no como expresión regular) y devuelva 2 si el fichero no existe. Debe funcionar con nombres que contengan espacios. Comprueba con un fichero temporal.',
         code='''count_matches() {
    local pattern=$1 file=$2
    if [[ ! -f $file ]]; then
        return 2
    fi
    grep -c -F -- "$pattern" "$file" || true
}''',
         harness='''set -euo pipefail
{{code}}

dir=$(mktemp -d)
trap 'rm -rf "$dir"' EXIT
file="$dir/mi fichero.txt"
printf 'uno\\ndos uno\\ntres\\na.b\\n' > "$file"
[[ $(count_matches uno "$file") == 2 ]]
[[ $(count_matches 'a.b' "$file") == 1 ]]
[[ $(count_matches zzz "$file") == 0 ]]
set +e
count_matches uno "$dir/no existe" > /dev/null
status=$?
set -e
[[ $status == 2 ]]
echo OK''',
         tests=['`uno` aparece en 2 líneas', 'el patrón `a.b` se busca literalmente', 'un patrón ausente da 0', 'un fichero inexistente devuelve 2', 'funciona con espacios en el nombre'],
         why='Las comillas dobles evitan que el shell parta el nombre por espacios. `-F` trata el patrón como texto, no como expresión regular, y `--` impide que un patrón que empiece por `-` se tome por una opción. `grep -c` devuelve 1 cuando no hay coincidencias: con `set -e` eso abortaría el guion, por eso se neutraliza con `|| true`.'),
    dict(ch=2, lang='bash', level='INTERMEDIATE',
         prompt='Escribe en Bash la función `with_temp_file` que cree un fichero temporal, ejecute en él el comando que recibe como argumentos (el nombre se pasa como último argumento) y lo borre siempre al terminar, incluso si el comando falla; debe devolver el código de salida del comando. Comprueba que el fichero desaparece en ambos casos.',
         code='''with_temp_file() {
    local tmp status
    tmp=$(mktemp)
    trap 'rm -f "$tmp"' RETURN
    "$@" "$tmp"
    status=$?
    last_tmp=$tmp
    return "$status"
}''',
         harness='''{{code}}

with_temp_file test -f
[[ $? == 0 && ! -e $last_tmp ]]
with_temp_file bash -c 'echo datos > "$1"; exit 7' _
[[ $? == 7 && ! -e $last_tmp ]]
with_temp_file false
[[ $? == 1 && ! -e $last_tmp ]]
echo OK''',
         tests=['el comando `test -f` ve un fichero que existe y devuelve 0', 'un comando que sale con 7 devuelve 7', 'en todos los casos el fichero temporal se borra'],
         why='`trap ... RETURN` se ejecuta al volver de la función, falle o no el comando, así que la limpieza no depende de que el código llegue al final. Guardar `$?` justo después de la llamada evita perder el código de salida.'),
    dict(ch=2, lang='bash', level='ADVANCED',
         prompt='Escribe en Bash `parse_opts` que procese `-v` (activa `verbose`), `-n NOMBRE` (guarda el nombre) y deje en el array `rest` los argumentos restantes, con `getopts`. Debe devolver 1 ante una opción desconocida. Comprueba `-v -n ana a b`, ningún argumento y una opción inválida.',
         code='''parse_opts() {
    verbose=0
    name=
    rest=()
    local opt OPTIND=1
    while getopts ":vn:" opt; do
        case $opt in
            v) verbose=1 ;;
            n) name=$OPTARG ;;
            *) return 1 ;;
        esac
    done
    shift $((OPTIND - 1))
    rest=("$@")
}''',
         harness='''{{code}}

parse_opts -v -n ana a b
[[ $verbose == 1 && $name == ana && ${#rest[@]} == 2 && ${rest[0]} == a && ${rest[1]} == b ]]
parse_opts
[[ $verbose == 0 && -z $name && ${#rest[@]} == 0 ]]
parse_opts -n "con espacios" "x y"
[[ $name == "con espacios" && ${rest[0]} == "x y" ]]
if parse_opts -z; then exit 1; fi
echo OK''',
         tests=['`-v -n ana a b` activa verbose, guarda `ana` y deja `a b`', 'sin argumentos todo queda por defecto', 'los valores con espacios se conservan', 'una opción desconocida devuelve 1'],
         why='`getopts` recorre las opciones y deja en `OPTIND` la posición del primer argumento no opcional; `shift` descarta lo ya procesado. Reiniciar `OPTIND` al entrar permite llamar a la función varias veces en el mismo shell.'),
    # ---- capítulo 3: PHP y Ruby
    dict(ch=3, lang='php', level='FOUNDATIONAL',
         prompt='Escribe en PHP `function slugify(string $text): string` que convierta un texto en un identificador para URL: minúsculas, letras y números, y guiones en lugar de cualquier otro grupo de caracteres, sin guiones al principio ni al final. Comprueba `"Hola, Mundo!"`, `"  PHP 8.3  "` y la cadena vacía.',
         code='''function slugify(string $text): string
{
    $slug = strtolower($text);
    $slug = preg_replace('/[^a-z0-9]+/', '-', $slug);
    return trim($slug, '-');
}''',
         harness='''<?php
declare(strict_types=1);

{{code}}

assert(slugify("Hola, Mundo!") === "hola-mundo");
assert(slugify("  PHP 8.3  ") === "php-8-3");
assert(slugify("") === "");
assert(slugify("---a---b---") === "a-b");
echo "OK\\n";''',
         tests=['`"Hola, Mundo!"` da `"hola-mundo"`', '`"  PHP 8.3  "` da `"php-8-3"`', 'la cadena vacía da `""`', 'los guiones repetidos se colapsan'],
         why='La expresión regular `[^a-z0-9]+` sustituye cada grupo de caracteres no alfanuméricos por un guion, y `trim` quita los de los extremos. `strict_types` hace que PHP rechace tipos incorrectos en lugar de convertirlos en silencio.'),
    dict(ch=3, lang='php', level='INTERMEDIATE',
         prompt='Define en PHP 8.3 el enumerado `Status: string` (`Draft = "draft"`, `Published = "published"`) con el método `label()`, y la clase `final readonly class Post` con `title` y `status`, un método `publish(): Post` que devuelva una copia publicada (sin modificar el original) y `Status::from`/`tryFrom` para leer un texto. Comprueba la inmutabilidad.',
         code='''enum Status: string
{
    case Draft = 'draft';
    case Published = 'published';

    public function label(): string
    {
        return match ($this) {
            self::Draft => 'Borrador',
            self::Published => 'Publicado',
        };
    }
}

final readonly class Post
{
    public function __construct(public string $title, public Status $status = Status::Draft) {}

    public function publish(): Post
    {
        return new Post($this->title, Status::Published);
    }
}''',
         harness='''<?php
declare(strict_types=1);

{{code}}

$post = new Post("Hola");
$published = $post->publish();
assert($post->status === Status::Draft);
assert($published->status === Status::Published);
assert($published->status->label() === "Publicado");
assert(Status::from("draft") === Status::Draft);
assert(Status::tryFrom("otro") === null);
try {
    $post->title = "Cambio";
    assert(false);
} catch (Error $e) {
    assert(str_contains($e->getMessage(), "readonly"));
}
echo "OK\\n";''',
         tests=['`publish()` no modifica el original', 'la copia tiene estado `Published` y etiqueta `Publicado`', '`Status::from("draft")` devuelve `Draft` y `tryFrom("otro")` devuelve `null`', 'asignar a una propiedad `readonly` lanza `Error`'],
         why='Un enumerado respaldado convierte un conjunto de cadenas válidas en un tipo: `from` lanza una excepción con un valor desconocido y `tryFrom` devuelve `null`. Una clase `readonly` no permite modificar sus propiedades tras la construcción, así que cada cambio crea un objeto nuevo.'),
    dict(ch=3, lang='ruby', level='INTERMEDIATE',
         prompt='Escribe en Ruby `group_anagrams(words)` que agrupe las palabras que son anagramas entre sí y devuelva un array de grupos, cada uno ordenado alfabéticamente y todos ordenados por su primer elemento. Usa `group_by`. Comprueba `["listen", "silent", "enlist", "google", "gogole", "cat"]`.',
         code='''def group_anagrams(words)
  words.group_by { |w| w.chars.sort.join }.values.map(&:sort).sort_by(&:first)
end''',
         harness='''{{code}}

result = group_anagrams(%w[listen silent enlist google gogole cat])
raise "grupos" unless result == [%w[cat], %w[enlist listen silent], %w[gogole google]]
raise "vacio" unless group_anagrams([]) == []
raise "una" unless group_anagrams(%w[a]) == [%w[a]]
puts "OK"''',
         tests=['`listen`, `silent` y `enlist` forman un grupo', '`google` y `gogole` forman otro', '`cat` queda solo', 'una lista vacía da `[]`'],
         why='Dos palabras son anagramas si tienen las mismas letras, así que sus letras ordenadas son una clave común. `group_by` agrupa por esa clave y `values` devuelve los grupos; los `map(&:sort)` y `sort_by` dan un orden determinista.'),
    # ---- capítulo 4: Haskell
    dict(ch=4, lang='haskell', level='FOUNDATIONAL',
         prompt='Escribe `safeDiv :: Int -> Int -> Maybe Int` que devuelva `Nothing` al dividir entre cero, y `calc :: Int -> Int -> Int -> Maybe Int` que calcule `(a / b) / c` encadenando con `>>=`. Comprueba `calc 100 5 2 == Just 10` y los dos casos de división por cero.',
         code='''safeDiv :: Int -> Int -> Maybe Int
safeDiv _ 0 = Nothing
safeDiv a b = Just (a `div` b)

calc :: Int -> Int -> Int -> Maybe Int
calc a b c = safeDiv a b >>= \\q -> safeDiv q c''',
         harness='''{{code}}

main :: IO ()
main = do
  let checks =
        [ calc 100 5 2 == Just 10
        , calc 1 0 2 == Nothing
        , calc 10 2 0 == Nothing
        , safeDiv (-7) 2 == Just (-4)
        ]
  if and checks then putStrLn "OK" else putStrLn "FAIL"''',
         tests=['`calc 100 5 2` es `Just 10`', 'dividir entre cero al principio da `Nothing`', 'dividir entre cero al final da `Nothing`', '`div` redondea hacia menos infinito'],
         why='`>>=` pasa el valor de un `Maybe` a la siguiente función solo si existe; si algún paso devuelve `Nothing`, el resto no se ejecuta. El fallo se propaga sin comprobaciones manuales y queda reflejado en el tipo.'),
    dict(ch=4, lang='haskell', level='INTERMEDIATE',
         prompt='Escribe `primes :: [Int]`, la lista infinita de números primos usando la criba de Eratóstenes de forma perezosa, y `takePrimes :: Int -> [Int]`. Comprueba los diez primeros y que el primo número 100 es 541.',
         code='''primes :: [Int]
primes = sieve [2 ..]
  where
    sieve (p : xs) = p : sieve [x | x <- xs, x `mod` p /= 0]
    sieve [] = []

takePrimes :: Int -> [Int]
takePrimes n = take n primes''',
         harness='''{{code}}

main :: IO ()
main = do
  let ok1 = takePrimes 10 == [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
      ok2 = primes !! 99 == 541
      ok3 = null (takePrimes 0)
  if ok1 && ok2 && ok3 then putStrLn "OK" else putStrLn "FAIL"''',
         tests=['los diez primeros son `2, 3, 5, 7, 11, 13, 17, 19, 23, 29`', 'el primo número 100 es 541', '`takePrimes 0` es vacía'],
         why='La evaluación perezosa calcula cada elemento solo cuando se necesita, de modo que una lista infinita es utilizable. Esta criba es elegante pero poco eficiente (filtra por cada primo anterior), una versión de producción usaría una criba con estructuras mutables o un montículo.'),
    dict(ch=4, lang='haskell', level='ADVANCED',
         prompt='Define `data Tree a = Leaf | Node (Tree a) a (Tree a)` con `insert :: Ord a => a -> Tree a -> Tree a`, `toList :: Tree a -> [a]` (recorrido en orden) e `instance Functor Tree`. Comprueba que insertar `[5,2,8,1,9,3]` y recorrer da la lista ordenada, y que `fmap (*2)` duplica cada valor.',
         code='''data Tree a = Leaf | Node (Tree a) a (Tree a)

insert :: Ord a => a -> Tree a -> Tree a
insert x Leaf = Node Leaf x Leaf
insert x t@(Node l v r)
  | x < v = Node (insert x l) v r
  | x > v = Node l v (insert x r)
  | otherwise = t

toList :: Tree a -> [a]
toList Leaf = []
toList (Node l v r) = toList l ++ [v] ++ toList r

instance Functor Tree where
  fmap _ Leaf = Leaf
  fmap f (Node l v r) = Node (fmap f l) (f v) (fmap f r)''',
         harness='''{{code}}

main :: IO ()
main = do
  let t = foldr insert Leaf [5, 2, 8, 1, 9, 3, 2 :: Int]
      ok1 = toList t == [1, 2, 3, 5, 8, 9]
      ok2 = toList (fmap (* 2) t) == [2, 4, 6, 10, 16, 18]
      ok3 = null (toList (Leaf :: Tree Int))
  if ok1 && ok2 && ok3 then putStrLn "OK" else putStrLn "FAIL"''',
         tests=['insertar y recorrer da la lista ordenada y sin duplicados', '`fmap (*2)` duplica cada valor conservando el orden', 'el árbol vacío da lista vacía'],
         why='Un tipo algebraico describe el árbol y las funciones recursivas siguen su forma. La instancia de `Functor` transforma los valores sin cambiar la estructura. Como `insert` ignora los duplicados (`otherwise = t`), el árbol representa un conjunto.'),
    # ---- capítulo 5: OCaml
    dict(ch=5, lang='ocaml', level='INTERMEDIATE',
         prompt='Define el tipo `type expr = Num of int | Add of expr * expr | Mul of expr * expr | Neg of expr` y `eval : expr -> int` y `to_string : expr -> string` (`"(2 + 3) * 4"` se escribe con paréntesis solo alrededor de sumas dentro de productos). Comprueba ambos.',
         code='''type expr = Num of int | Add of expr * expr | Mul of expr * expr | Neg of expr

let rec eval = function
  | Num n -> n
  | Add (a, b) -> eval a + eval b
  | Mul (a, b) -> eval a * eval b
  | Neg a -> - (eval a)

let rec to_string = function
  | Num n -> string_of_int n
  | Add (a, b) -> to_string a ^ " + " ^ to_string b
  | Mul (a, b) ->
      let wrap e = match e with Add _ -> "(" ^ to_string e ^ ")" | _ -> to_string e in
      wrap a ^ " * " ^ wrap b
  | Neg a -> "-" ^ (match a with Num _ -> to_string a | _ -> "(" ^ to_string a ^ ")")''',
         harness='''{{code}}

let () =
  let e = Mul (Add (Num 2, Num 3), Num 4) in
  assert (eval e = 20);
  assert (to_string e = "(2 + 3) * 4");
  assert (eval (Neg (Add (Num 1, Num 2))) = -3);
  assert (to_string (Neg (Add (Num 1, Num 2))) = "-(1 + 2)");
  assert (to_string (Add (Num 1, Mul (Num 2, Num 3))) = "1 + 2 * 3");
  print_endline "OK"''',
         tests=['`(2 + 3) * 4` vale 20 y se escribe con paréntesis', 'la negación de una suma lleva paréntesis', 'un producto dentro de una suma no los necesita'],
         why='Los tipos suma y el ajuste de patrones permiten escribir cada operación como un caso. El compilador avisa si falta alguna variante. Los paréntesis solo son necesarios cuando una suma queda dentro de un producto o de una negación.'),
    dict(ch=5, lang='ocaml', level='ADVANCED',
         prompt='Escribe un functor `Counter` que, dado un módulo con tipo `t`, `compare` y `to_string`, devuelva un módulo con `add : t -> t list -> (t * int) list` ... en concreto `count : t list -> (t * int) list` que cuente ocurrencias ordenadas por `compare`. Instáncialo para enteros y para cadenas.',
         code='''module type KEY = sig
  type t
  val compare : t -> t -> int
end

module Counter (K : KEY) = struct
  let count (items : K.t list) : (K.t * int) list =
    let sorted = List.sort K.compare items in
    let rec go acc = function
      | [] -> List.rev acc
      | x :: rest -> (
          match acc with
          | (y, n) :: tl when K.compare x y = 0 -> go ((y, n + 1) :: tl) rest
          | _ -> go ((x, 1) :: acc) rest)
    in
    go [] sorted
end''',
         harness='''{{code}}

module IntCounter = Counter (struct type t = int let compare = compare end)
module StrCounter = Counter (String)

let () =
  assert (IntCounter.count [3; 1; 3; 2; 1; 3] = [(1, 2); (2, 1); (3, 3)]);
  assert (StrCounter.count ["b"; "a"; "b"] = [("a", 1); ("b", 2)]);
  assert (IntCounter.count [] = []);
  print_endline "OK"''',
         tests=['cuenta `[3;1;3;2;1;3]` como `[(1,2);(2,1);(3,3)]`', 'funciona para cadenas con el módulo `String`', 'una lista vacía da una lista vacía'],
         why='Un functor es una función de módulos a módulos: el mismo código de conteo sirve para cualquier tipo con una comparación. Aquí se instancia con un módulo anónimo para enteros y con `String`, que ya tiene `t` y `compare`.'),
    dict(ch=5, lang='ocaml', level='INTERMEDIATE',
         prompt='Escribe `safe_assoc : (string * int) list -> string -> int option` y una función `total : (string * int) list -> string list -> int option` que sume los valores de las claves pedidas y devuelva `None` si falta alguna, usando `Option.bind` o `match`. Comprueba aciertos y fallos.',
         code='''let safe_assoc table key = List.assoc_opt key table

let total table keys =
  List.fold_left
    (fun acc key ->
      match (acc, safe_assoc table key) with
      | Some sum, Some v -> Some (sum + v)
      | _ -> None)
    (Some 0) keys''',
         harness='''{{code}}

let () =
  let table = [("a", 1); ("b", 2); ("c", 3)] in
  assert (total table ["a"; "c"] = Some 4);
  assert (total table ["a"; "z"] = None);
  assert (total table [] = Some 0);
  assert (safe_assoc table "b" = Some 2);
  print_endline "OK"''',
         tests=['`["a"; "c"]` suma 4', 'una clave ausente da `None`', 'una lista de claves vacía suma 0'],
         why='`option` hace explícita la posible ausencia, sin valores nulos. El pliegue acumula un `option`: en cuanto aparece un `None`, el resultado final es `None` y no se pueden confundir ausencias con ceros.'),
    # ---- capítulo 6: Elixir, Clojure, Scala
    dict(ch=6, lang='elixir', level='FOUNDATIONAL',
         prompt='Escribe en Elixir el módulo `Fib` con `fib/1` usando ajuste de patrones y guardas (`n >= 0`) y `first/1` que devuelva los `n` primeros números con `Stream.unfold`. `fib/1` con un negativo debe lanzar `FunctionClauseError`. Comprueba `fib(10) == 55` y los 8 primeros.',
         code='''defmodule Fib do
  def fib(0), do: 0
  def fib(1), do: 1
  def fib(n) when is_integer(n) and n > 1, do: fib(n - 1) + fib(n - 2)

  def first(n) do
    {0, 1}
    |> Stream.unfold(fn {a, b} -> {a, {b, a + b}} end)
    |> Enum.take(n)
  end
end''',
         harness='''{{code}}

true = Fib.fib(10) == 55
true = Fib.first(8) == [0, 1, 1, 2, 3, 5, 8, 13]
true = Fib.first(0) == []
try do
  Fib.fib(-1)
  raise "debe fallar"
rescue
  FunctionClauseError -> :ok
end
IO.puts("OK")''',
         tests=['`fib(10)` es 55', '`first(8)` es `[0, 1, 1, 2, 3, 5, 8, 13]`', '`first(0)` es vacía', '`fib(-1)` lanza `FunctionClauseError`'],
         why='Elixir elige la cláusula cuyo patrón y guarda coinciden; si ninguna coincide, lanza `FunctionClauseError`, lo que documenta el dominio de la función. `Stream.unfold` genera la secuencia de forma perezosa a partir de un estado.'),
    dict(ch=6, lang='elixir', level='ADVANCED',
         prompt='Escribe un `GenServer` llamado `Counter` con `start_link/1`, `increment/1` (asíncrono con `cast`), `value/1` (síncrono con `call`) y comprueba con 100 procesos que incrementan concurrentemente que el valor final es exacto, gracias a que el proceso serializa los mensajes.',
         code='''defmodule Counter do
  use GenServer

  def start_link(initial \\\\ 0), do: GenServer.start_link(__MODULE__, initial)
  def increment(pid), do: GenServer.cast(pid, :increment)
  def value(pid), do: GenServer.call(pid, :value)

  @impl true
  def init(initial), do: {:ok, initial}

  @impl true
  def handle_cast(:increment, count), do: {:noreply, count + 1}

  @impl true
  def handle_call(:value, _from, count), do: {:reply, count, count}
end''',
         harness='''{{code}}

{:ok, pid} = Counter.start_link()
1..100
|> Enum.map(fn _ -> Task.async(fn -> Enum.each(1..50, fn _ -> Counter.increment(pid) end) end) end)
|> Enum.each(&Task.await/1)
true = Counter.value(pid) == 5000
{:ok, other} = Counter.start_link(10)
Counter.increment(other)
true = Counter.value(other) == 11
true = Counter.value(pid) == 5000
IO.puts("OK")''',
         tests=['100 procesos con 50 incrementos dan 5000', 'un contador iniciado en 10 llega a 11', 'los contadores son independientes'],
         why='Un proceso procesa un mensaje cada vez, así que el estado del contador no necesita cerrojos: las peticiones se serializan en su buzón. `cast` no espera respuesta y `call` sí; como los mensajes de un mismo remitente llegan en orden, `value` ve los incrementos anteriores.'),
    dict(ch=6, lang='clojure', level='INTERMEDIATE',
         prompt='Escribe en Clojure `word-freq` que reciba una cadena y devuelva un mapa de palabra (en minúsculas) a frecuencia usando `re-seq`, `frequencies` y la macro de hilo `->>`. Comprueba `"a b A c b a"` y la cadena vacía.',
         code='''(defn word-freq [text]
  (->> (re-seq #"[\\p{L}\\p{N}]+" text)
       (map #(.toLowerCase ^String %))
       frequencies))''',
         harness='''{{code}}

(assert (= (word-freq "a b A c b a") {"a" 3 "b" 2 "c" 1}))
(assert (= (word-freq "") {}))
(assert (= (word-freq "Hola, hola... adios!") {"hola" 2 "adios" 1}))
(println "OK")''',
         tests=['`"a b A c b a"` da `{"a" 3, "b" 2, "c" 1}`', 'la cadena vacía da un mapa vacío', 'ignora la puntuación'],
         why='`->>` coloca el resultado de cada paso como último argumento del siguiente, lo que permite leer el flujo de arriba abajo. Los datos de Clojure son inmutables: cada función devuelve un valor nuevo y no modifica la entrada.'),
    dict(ch=6, lang='scala', level='INTERMEDIATE',
         prompt='En Scala 3, define `enum Json` con `JNum(Double)`, `JStr(String)`, `JArr(List[Json])` y `JBool(Boolean)`, y `def render(j: Json): String` con ajuste de patrones exhaustivo. Comprueba `JArr(List(JNum(1), JStr("a"), JBool(true)))` y el array vacío.',
         code='''enum Json:
  case JNum(value: Double)
  case JStr(value: String)
  case JArr(items: List[Json])
  case JBool(value: Boolean)

def render(j: Json): String = j match
  case Json.JNum(v) => if v == v.toLong then v.toLong.toString else v.toString
  case Json.JStr(s) => "\\"" + s + "\\""
  case Json.JBool(b) => b.toString
  case Json.JArr(items) => items.map(render).mkString("[", ",", "]")''',
         harness='''{{code}}

@main def run(): Unit =
  import Json.*
  assert(render(JArr(List(JNum(1), JStr("a"), JBool(true)))) == "[1,\\"a\\",true]")
  assert(render(JArr(Nil)) == "[]")
  assert(render(JNum(2.5)) == "2.5")
  assert(render(JArr(List(JArr(List(JNum(1)))))) == "[[1]]")
  println("OK")''',
         tests=['`[1,"a",true]` se escribe correctamente', 'el array vacío es `[]`', 'un decimal conserva su parte fraccionaria', 'los arrays anidados se escriben recursivamente'],
         why='Un `enum` de Scala 3 es un tipo suma, y el `match` sobre él es exhaustivo: el compilador avisa si falta un caso. La recursión sigue la estructura del dato.'),
    # ---- capítulo 7: Julia y R
    dict(ch=7, lang='julia', level='INTERMEDIATE',
         prompt='En Julia, define `abstract type Shape end`, `struct Circle <: Shape; r::Float64; end`, `struct Rect <: Shape; w::Float64; h::Float64; end` y el método `area` por despacho múltiple, y `collide(a::Shape, b::Shape)` con métodos distintos para (círculo, círculo), (rectángulo, rectángulo) y el caso mixto. Comprueba el despacho.',
         code='''abstract type Shape end
struct Circle <: Shape
    r::Float64
end
struct Rect <: Shape
    w::Float64
    h::Float64
end

area(c::Circle) = pi * c.r^2
area(r::Rect) = r.w * r.h

collide(a::Circle, b::Circle) = "circulo-circulo"
collide(a::Rect, b::Rect) = "rect-rect"
collide(a::Shape, b::Shape) = "mixto"''',
         harness='''{{code}}

using Test
@test area(Circle(1.0)) ≈ pi
@test area(Rect(3.0, 4.0)) == 12.0
@test collide(Circle(1.0), Circle(2.0)) == "circulo-circulo"
@test collide(Rect(1.0, 1.0), Rect(2.0, 2.0)) == "rect-rect"
@test collide(Circle(1.0), Rect(1.0, 1.0)) == "mixto"
@test collide(Rect(1.0, 1.0), Circle(1.0)) == "mixto"
println("OK")''',
         tests=['el área de un círculo de radio 1 es `pi`', 'el área de un rectángulo 3 por 4 es 12', '`collide` elige el método según los tipos de ambos argumentos', 'el caso mixto cae en el método más general'],
         why='En Julia el método ejecutado depende de los tipos de todos los argumentos (despacho múltiple), no solo del primero. Si hay varios aplicables, se elige el más específico; `collide(::Shape, ::Shape)` es el de respaldo. El compilador especializa cada método para los tipos concretos.'),
    dict(ch=7, lang='julia', level='INTERMEDIATE',
         prompt='Escribe en Julia `moving_average(x, k)` que devuelva el vector de medias móviles de ventana `k` (longitud `length(x) - k + 1`) y que sea estable en tipos: para entradas `Float64` debe devolver un `Vector{Float64}`. Lanza `ArgumentError` si `k < 1` o `k > length(x)`. Comprueba con `@inferred`.',
         code='''function moving_average(x::AbstractVector{T}, k::Integer) where {T<:Real}
    (k < 1 || k > length(x)) && throw(ArgumentError("ventana invalida"))
    out = Vector{float(T)}(undef, length(x) - k + 1)
    s = sum(@view x[1:k])
    out[1] = s / k
    for i in 2:length(out)
        s += x[i + k - 1] - x[i - 1]
        out[i] = s / k
    end
    return out
end''',
         harness='''{{code}}

using Test
@test @inferred(moving_average([1.0, 2.0, 3.0, 4.0, 5.0], 3)) == [2.0, 3.0, 4.0]
@test moving_average([1, 2, 3, 4], 2) == [1.5, 2.5, 3.5]
@test moving_average([5.0], 1) == [5.0]
@test_throws ArgumentError moving_average([1.0, 2.0], 3)
@test_throws ArgumentError moving_average([1.0, 2.0], 0)
println("OK")''',
         tests=['`[1,2,3,4,5]` con ventana 3 da `[2,3,4]`', 'con enteros devuelve reales', 'una ventana igual a la longitud devuelve un elemento', 'una ventana mayor o menor que 1 lanza `ArgumentError`', '`@inferred` confirma que el tipo del resultado se conoce en compilación'],
         why='Actualizar la suma deslizante en lugar de recalcularla da coste lineal. Que el tipo del resultado dependa solo de los tipos de entrada (`float(T)`) es lo que permite al compilador generar código rápido, y `@inferred` lo comprueba.'),
    dict(ch=7, lang='r', level='INTERMEDIATE',
         prompt='Escribe en R `normalize(x)` que devuelva el vector escalado a media 0 y desviación típica 1 (vectorizado, sin bucles) y que devuelva ceros si la desviación es 0. Escribe también `count_missing(df)` que cuente los `NA` por columna de un `data.frame`. Comprueba ambas.',
         code='''normalize <- function(x) {
  s <- sd(x, na.rm = TRUE)
  if (is.na(s) || s == 0) {
    return(rep(0, length(x)))
  }
  (x - mean(x, na.rm = TRUE)) / s
}

count_missing <- function(df) {
  vapply(df, function(col) sum(is.na(col)), integer(1))
}''',
         harness='''{{code}}

z <- normalize(c(2, 4, 6, 8))
stopifnot(abs(mean(z)) < 1e-12, abs(sd(z) - 1) < 1e-12)
stopifnot(all(normalize(c(5, 5, 5)) == 0))
df <- data.frame(a = c(1, NA, 3), b = c(NA, NA, "x"), c = 1:3)
cm <- count_missing(df)
stopifnot(identical(unname(cm), c(1L, 2L, 0L)), identical(names(cm), c("a", "b", "c")))
cat("OK\\n")''',
         tests=['el resultado tiene media 0 y desviación 1', 'un vector constante da ceros', '`count_missing` cuenta 1, 2 y 0 `NA` por columna', 'conserva los nombres de columna'],
         why='Las operaciones de R son vectoriales: `(x - media) / s` se aplica a todo el vector a la vez. `vapply` exige declarar el tipo del resultado, lo que lo hace más seguro que `sapply`, que puede devolver estructuras distintas según los datos.'),
    # ---- capítulo 8: Lua, Perl, Prolog, Objective-C
    dict(ch=8, lang='lua', level='INTERMEDIATE',
         prompt='Escribe en Lua una "clase" `Vector2D` con metatablas: `Vector2D.new(x, y)`, el método `magnitude_sq()`, la suma con `__add`, la igualdad con `__eq` y `tostring` con `__tostring`. Comprueba `Vector2D.new(6, 8):magnitude_sq() == 100`.',
         code='''local Vector2D = {}
Vector2D.__index = Vector2D

function Vector2D.new(x, y)
  return setmetatable({ x = x, y = y }, Vector2D)
end

function Vector2D:magnitude_sq()
  return self.x * self.x + self.y * self.y
end

Vector2D.__add = function(a, b) return Vector2D.new(a.x + b.x, a.y + b.y) end
Vector2D.__eq = function(a, b) return a.x == b.x and a.y == b.y end
Vector2D.__tostring = function(v) return "(" .. v.x .. ", " .. v.y .. ")" end''',
         harness='''{{code}}

local v = Vector2D.new(6, 8)
assert(v:magnitude_sq() == 100)
assert(v + Vector2D.new(1, 1) == Vector2D.new(7, 9))
assert(tostring(Vector2D.new(1, 2)) == "(1, 2)")
assert(v ~= Vector2D.new(0, 0))
print("OK")''',
         tests=['`(6, 8)` tiene magnitud al cuadrado 100', 'la suma de vectores funciona', '`tostring` da `"(1, 2)"`', 'la igualdad compara por valor'],
         why='Una metatabla define el comportamiento de una tabla ante operadores y accesos. `__index` apunta a la propia clase para que los métodos se encuentren, y `__add`, `__eq` y `__tostring` conectan el objeto con `+`, `==` y `tostring`. Lua no tiene clases: esto es un patrón sobre tablas.'),
    dict(ch=8, lang='perl', level='INTERMEDIATE',
         prompt='Escribe en Perl `word_freq($texto)` que devuelva una referencia a un hash de palabra (en minúsculas) a frecuencia, extrayendo las palabras con una expresión regular, y `top_word(\\%freq)` que devuelva la más frecuente (la primera alfabéticamente si hay empate). Comprueba con `"a b A c b a"`.',
         code='''use strict;
use warnings;

sub word_freq {
    my ($text) = @_;
    my %freq;
    $freq{lc $1}++ while $text =~ /(\\w+)/g;
    return \\%freq;
}

sub top_word {
    my ($freq) = @_;
    my ($best) = sort { $freq->{$b} <=> $freq->{$a} || $a cmp $b } keys %$freq;
    return $best;
}''',
         harness='''{{code}}

my $f = word_freq("a b A c b a");
die "frecuencias" unless $f->{a} == 3 && $f->{b} == 2 && $f->{c} == 1 && keys(%$f) == 3;
die "top" unless top_word($f) eq "a";
die "empate" unless top_word({ x => 1, b => 1 }) eq "b";
die "vacio" unless keys(%{ word_freq("") }) == 0;
print "OK\\n";''',
         tests=['`"a b A c b a"` da `a=3, b=2, c=1`', 'la palabra más frecuente es `a`', 'un empate se resuelve alfabéticamente', 'la cadena vacía da un hash vacío'],
         why='`while $text =~ /(\\w+)/g` recorre todas las coincidencias; `$1` es el grupo capturado. `use strict` y `use warnings` convierten errores comunes (variables sin declarar) en fallos visibles. La ordenación compuesta con `||` usa el segundo criterio solo si el primero empata.'),
    dict(ch=8, lang='prolog', level='INTERMEDIATE',
         prompt='En Prolog, define los hechos `parent(Padre, Hijo)` para `tom-bob, tom-liz, bob-ann, bob-pat, pat-jim` y la regla recursiva `ancestor(A, D)`. Escribe también `descendants(A, Lista)` con `findall`. Comprueba `ancestor(tom, jim)`, que `ancestor(ann, tom)` falla y la lista de descendientes de `bob`.',
         code='''parent(tom, bob).
parent(tom, liz).
parent(bob, ann).
parent(bob, pat).
parent(pat, jim).

ancestor(A, D) :- parent(A, D).
ancestor(A, D) :- parent(A, X), ancestor(X, D).

descendants(A, List) :- findall(D, ancestor(A, D), Unsorted), sort(Unsorted, List).''',
         harness='''{{code}}

:- initialization(main).
main :-
    ( ancestor(tom, jim) -> true ; halt(1) ),
    ( \\+ ancestor(ann, tom) -> true ; halt(2) ),
    descendants(bob, L), ( L == [ann, jim, pat] -> true ; halt(3) ),
    descendants(jim, E), ( E == [] -> true ; halt(4) ),
    format("OK~n"), halt(0).''',
         tests=['`ancestor(tom, jim)` es verdadero', '`ancestor(ann, tom)` falla', 'los descendientes de `bob` son `[ann, jim, pat]`', '`jim` no tiene descendientes'],
         why='Prolog resuelve consultas buscando por retroceso las cláusulas que unifican. La regla recursiva tiene un caso base (padre directo) y uno recursivo. `findall` reúne todas las soluciones y `sort` las ordena sin duplicados; sin él, el orden depende del orden de los hechos.'),
    dict(ch=8, lang='objc', level='ADVANCED',
         prompt='En Objective-C define la clase `Account` con la propiedad `balance` (`NSInteger`, solo lectura desde fuera), `deposit:` y `withdraw:` (devuelve `NO` y no cambia nada si el saldo no alcanza). Comprueba con ARC un depósito, una retirada válida y una excesiva.',
         code='''#import <Foundation/Foundation.h>

@interface Account : NSObject
@property(nonatomic, readonly) NSInteger balance;
- (void)deposit:(NSInteger)amount;
- (BOOL)withdraw:(NSInteger)amount;
@end

@implementation Account {
    NSInteger _balance;
}
- (NSInteger)balance { return _balance; }
- (void)deposit:(NSInteger)amount { _balance += amount; }
- (BOOL)withdraw:(NSInteger)amount {
    if (amount > _balance) {
        return NO;
    }
    _balance -= amount;
    return YES;
}
@end''',
         harness='''{{code}}

int main(void) {
    @autoreleasepool {
        Account *a = [[Account alloc] init];
        [a deposit:100];
        if (![a withdraw:30] || a.balance != 70) return 1;
        if ([a withdraw:500] || a.balance != 70) return 2;
        NSLog(@"saldo %ld", (long)a.balance);
    }
    printf("OK\\n");
    return 0;
}''',
         tests=['depositar 100 y retirar 30 deja 70', 'una retirada de 500 devuelve `NO` y no cambia el saldo'],
         why='Con ARC el compilador inserta las llamadas de retención y liberación; el programador no las escribe. Una propiedad `readonly` solo expone el getter, y la variable de instancia `_balance` se modifica dentro de la clase.'),
]
