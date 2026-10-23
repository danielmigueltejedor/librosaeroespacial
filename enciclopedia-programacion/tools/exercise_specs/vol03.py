"""Programming exercises of volume 3 (Rust). Every reference program runs with rustc before it is recorded."""

L = 'rust'

EXERCISES = [
    # ---- capítulo 1: modelo de compilación y tipos
    dict(ch=1, lang=L, level='FOUNDATIONAL',
         prompt='Escribe `fn size_report() -> (usize, usize, usize)` que devuelva, con `std::mem::size_of`, los tamaños en bytes de `&u64`, `&[u64]` y `Vec<u64>` en este orden. No escribas los números a mano: deja que el compilador los diga. En una arquitectura de 64 bits debes obtener `(8, 16, 24)`.',
         code='''use std::mem::size_of;

fn size_report() -> (usize, usize, usize) {
    (size_of::<&u64>(), size_of::<&[u64]>(), size_of::<Vec<u64>>())
}''',
         harness='''fn main() {
    let (thin, wide, vec) = size_report();
    assert_eq!(thin, size_of::<usize>());
    assert_eq!(wide, 2 * thin);
    assert_eq!(vec, 3 * thin);
    println!("OK");
}''',
         tests=['`&u64` ocupa una palabra', '`&[u64]` ocupa dos palabras (puntero y longitud)', '`Vec<u64>` ocupa tres palabras (puntero, longitud y capacidad)'],
         why='`size_of` se evalúa en tiempo de compilación para el tipo indicado, así que el resultado depende de la plataforma y no de los datos. La referencia a un valor es un puntero; la referencia a una rebanada es un puntero ancho con longitud; un `Vec` guarda además la capacidad. Los elementos de un `Vec` viven en el montículo y no cuentan en estos tamaños.'),
    dict(ch=1, lang=L, level='FOUNDATIONAL',
         prompt='Escribe `fn classify(n: i64) -> &\'static str` que devuelva `"negativo"`, `"cero"` o `"positivo"` usando una sola expresión `match` con guardas. Comprueba `-5`, `0` y `42`.',
         code='''fn classify(n: i64) -> &'static str {
    match n {
        x if x < 0 => "negativo",
        0 => "cero",
        _ => "positivo",
    }
}''',
         harness='''fn main() {
    assert_eq!(classify(-5), "negativo");
    assert_eq!(classify(0), "cero");
    assert_eq!(classify(42), "positivo");
    assert_eq!(classify(i64::MIN), "negativo");
    println!("OK");
}''',
         tests=['`-5` devuelve `"negativo"`', '`0` devuelve `"cero"`', '`42` devuelve `"positivo"`', '`i64::MIN` es negativo'],
         why='En Rust `match` es una expresión: su valor es el de la rama elegida y el compilador exige que cubra todos los casos. La guarda `x if x < 0` captura los negativos, el patrón `0` el cero y `_` el resto.'),
    dict(ch=1, lang=L, kind='debugging', level='INTERMEDIATE',
         prompt='Depuración. Esta función entra en pánico con una lista vacía porque divide entre cero en coma flotante y devuelve `NaN` con otras entradas problemáticas:\n\n```rust\nfn mean(values: &[f64]) -> f64 {\n    values.iter().sum::<f64>() / values.len() as f64\n}\n```\n\nCorrige el contrato: `fn mean(values: &[f64]) -> Option<f64>` debe devolver `None` si no hay datos. Comprueba `[1.0, 2.0, 6.0] -> Some(3.0)` y `[] -> None`.',
         code='''fn mean(values: &[f64]) -> Option<f64> {
    if values.is_empty() {
        return None;
    }
    Some(values.iter().sum::<f64>() / values.len() as f64)
}''',
         harness='''fn main() {
    assert_eq!(mean(&[1.0, 2.0, 6.0]), Some(3.0));
    assert_eq!(mean(&[]), None);
    assert_eq!(mean(&[-4.0, -2.0]), Some(-3.0));
    println!("OK");
}''',
         tests=['`[1.0, 2.0, 6.0]` devuelve `Some(3.0)`', 'la lista vacía devuelve `None`', 'los negativos se promedian bien'],
         why='La media de cero mediciones no existe, y el tipo debe decirlo: `Option<f64>` obliga a quien llama a tratar la ausencia. Devolver `NaN` esconde el problema y lo propaga a cálculos posteriores.'),
    # ---- capítulo 2: toolchain y primeros programas
    dict(ch=2, lang=L, level='FOUNDATIONAL',
         prompt='Escribe `fn parse_pair(text: &str) -> Result<(i32, i32), String>` que lea `"3,4"` y devuelva `Ok((3, 4))`. Ignora los espacios alrededor de cada número. Si falta la coma o un número no es válido, devuelve `Err` con un mensaje. Comprueba `"3,4"`, `" -2 , 7 "`, `"3"` y `"a,1"`.',
         code='''fn parse_pair(text: &str) -> Result<(i32, i32), String> {
    let (left, right) = text.split_once(',').ok_or("falta la coma")?;
    let a = left.trim().parse::<i32>().map_err(|e| format!("izquierda: {e}"))?;
    let b = right.trim().parse::<i32>().map_err(|e| format!("derecha: {e}"))?;
    Ok((a, b))
}''',
         harness='''fn main() {
    assert_eq!(parse_pair("3,4"), Ok((3, 4)));
    assert_eq!(parse_pair(" -2 , 7 "), Ok((-2, 7)));
    assert!(parse_pair("3").is_err());
    assert!(parse_pair("a,1").is_err());
    assert!(parse_pair("1,").is_err());
    println!("OK");
}''',
         tests=['`"3,4"` devuelve `Ok((3, 4))`', '`" -2 , 7 "` devuelve `Ok((-2, 7))`', '`"3"` sin coma es error', '`"a,1"` es error', '`"1,"` es error'],
         why='`split_once` devuelve `Option`; `ok_or` lo convierte en `Result` y el operador `?` propaga el error sin escribir `match`. Cada `parse` transforma su error en un mensaje que dice qué lado falló.'),
    dict(ch=2, lang=L, level='INTERMEDIATE',
         prompt='Escribe `fn collatz_steps(n: u64) -> u32` que cuente cuántos pasos necesita la sucesión de Collatz (si es par, dividir entre 2; si es impar, multiplicar por 3 y sumar 1) para llegar a 1. Comprueba `1 -> 0`, `6 -> 8` y `27 -> 111`.',
         code='''fn collatz_steps(mut n: u64) -> u32 {
    let mut steps = 0;
    while n != 1 {
        n = if n % 2 == 0 { n / 2 } else { 3 * n + 1 };
        steps += 1;
    }
    steps
}''',
         harness='''fn main() {
    assert_eq!(collatz_steps(1), 0);
    assert_eq!(collatz_steps(6), 8);
    assert_eq!(collatz_steps(27), 111);
    assert_eq!(collatz_steps(97), 118);
    println!("OK");
}''',
         tests=['`1` necesita 0 pasos', '`6` necesita 8 pasos', '`27` necesita 111 pasos', '`97` necesita 118 pasos'],
         why='El parámetro `mut n` es una copia local que el bucle puede modificar sin afectar a quien llama. La condición `n != 1` termina para todos los valores probados; que termine para todo `n` es la conjetura de Collatz y sigue sin demostrarse, así que una entrada `0` no está dentro del contrato.'),
    dict(ch=2, lang=L, level='INTERMEDIATE',
         prompt='Escribe `fn is_palindrome(text: &str) -> bool` que ignore mayúsculas y todo lo que no sea una letra o un dígito. Comprueba `"Anita lava la tina"`, `"A man, a plan, a canal: Panama"`, `"rust"` y la cadena vacía.',
         code='''fn is_palindrome(text: &str) -> bool {
    let clean: Vec<char> = text
        .chars()
        .filter(|c| c.is_alphanumeric())
        .flat_map(|c| c.to_lowercase())
        .collect();
    clean.iter().eq(clean.iter().rev())
}''',
         harness='''fn main() {
    assert!(is_palindrome("Anita lava la tina"));
    assert!(is_palindrome("A man, a plan, a canal: Panama"));
    assert!(!is_palindrome("rust"));
    assert!(is_palindrome(""));
    println!("OK");
}''',
         tests=['"Anita lava la tina" es palíndromo', '"A man, a plan, a canal: Panama" es palíndromo', '"rust" no lo es', 'la cadena vacía es palíndromo'],
         why='Se filtran los caracteres alfanuméricos y se pasan a minúscula antes de comparar la secuencia con su inversa. Trabajar con `char` y no con bytes evita errores con letras acentuadas.'),
    # ---- capítulo 3: ownership, borrowing, lifetimes
    dict(ch=3, lang=L, level='FOUNDATIONAL',
         prompt='Escribe `fn longest<\'a>(a: &\'a str, b: &\'a str) -> &\'a str` que devuelva la cadena más larga (la primera si empatan). Explica con tus palabras por qué hace falta la anotación de vida `\'a`. Comprueba `"abc"` y `"de"`, y un empate.',
         code='''fn longest<'a>(a: &'a str, b: &'a str) -> &'a str {
    if b.len() > a.len() { b } else { a }
}''',
         harness='''fn main() {
    assert_eq!(longest("abc", "de"), "abc");
    assert_eq!(longest("x", "yz"), "yz");
    assert_eq!(longest("ab", "cd"), "ab");
    let outer = String::from("larga");
    let result;
    {
        let inner = String::from("c");
        result = longest(outer.as_str(), inner.as_str()).len();
    }
    assert_eq!(result, 5);
    println!("OK");
}''',
         tests=['`"abc"` frente a `"de"` devuelve `"abc"`', '`"x"` frente a `"yz"` devuelve `"yz"`', 'un empate devuelve el primero', 'el resultado se usa antes de que acabe la vida de `inner`'],
         why='El compilador no sabe si la referencia devuelta apunta a `a` o a `b`, así que la firma declara que el resultado vive como mucho tanto como la menos duradera de las dos. Si se usara fuera de ese alcance, el programa no compilaría.'),
    dict(ch=3, lang=L, level='INTERMEDIATE',
         prompt='Escribe `fn first_word(s: &str) -> &str` que devuelva la primera palabra (hasta el primer espacio) sin copiar texto: debe devolver una rebanada del original. Comprueba `"hola mundo"`, `"uno"` y `""`.',
         code='''fn first_word(s: &str) -> &str {
    match s.find(' ') {
        Some(index) => &s[..index],
        None => s,
    }
}''',
         harness='''fn main() {
    assert_eq!(first_word("hola mundo"), "hola");
    assert_eq!(first_word("uno"), "uno");
    assert_eq!(first_word(""), "");
    let text = String::from("rust en serio");
    let word = first_word(&text);
    assert_eq!(word.as_ptr(), text.as_ptr());
    println!("OK");
}''',
         tests=['`"hola mundo"` devuelve `"hola"`', '`"uno"` sin espacios se devuelve entero', 'la cadena vacía devuelve la vacía', 'el resultado apunta al mismo búfer que la entrada'],
         why='Una rebanada `&str` es un puntero y una longitud sobre el texto original; no reserva memoria. La prueba del puntero demuestra que no hubo copia. Gracias a la elisión de vidas, la firma no necesita anotaciones.'),
    dict(ch=3, lang=L, level='INTERMEDIATE',
         prompt='Escribe `fn dedup_adjacent(v: &mut Vec<i32>)` que elimine, in situ, los elementos iguales consecutivos de `v`. Comprueba `[1, 1, 2, 2, 2, 3, 1, 1] -> [1, 2, 3, 1]`, la lista vacía y una sin repeticiones. No se permite crear otro vector.',
         code='''fn dedup_adjacent(v: &mut Vec<i32>) {
    let mut write = 0;
    for read in 0..v.len() {
        if write == 0 || v[read] != v[write - 1] {
            v[write] = v[read];
            write += 1;
        }
    }
    v.truncate(write);
}''',
         harness='''fn main() {
    let mut a = vec![1, 1, 2, 2, 2, 3, 1, 1];
    dedup_adjacent(&mut a);
    assert_eq!(a, vec![1, 2, 3, 1]);
    let mut b: Vec<i32> = vec![];
    dedup_adjacent(&mut b);
    assert!(b.is_empty());
    let mut c = vec![4, 5, 6];
    dedup_adjacent(&mut c);
    assert_eq!(c, vec![4, 5, 6]);
    println!("OK");
}''',
         tests=['`[1, 1, 2, 2, 2, 3, 1, 1]` queda `[1, 2, 3, 1]`', 'la lista vacía no cambia', 'sin repeticiones no cambia'],
         why='La referencia mutable `&mut Vec<i32>` es exclusiva: mientras exista, nadie más puede leer ni escribir `v`. Dos índices recorren la lista, uno que lee y otro que escribe, y `truncate` descarta la cola sobrante.'),
    # ---- capítulo 4: tipos algebraicos, traits, genéricos, errores
    dict(ch=4, lang=L, level='FOUNDATIONAL',
         prompt='Define `enum Shape { Circle(f64), Rect(f64, f64) }` y un método `area(&self) -> f64`. Comprueba que un círculo de radio 1 tiene área `PI` y que un rectángulo 3 por 4 tiene área 12.',
         code='''use std::f64::consts::PI;

enum Shape {
    Circle(f64),
    Rect(f64, f64),
}

impl Shape {
    fn area(&self) -> f64 {
        match self {
            Shape::Circle(r) => PI * r * r,
            Shape::Rect(w, h) => w * h,
        }
    }
}''',
         harness='''fn main() {
    assert!((Shape::Circle(1.0).area() - PI).abs() < 1e-12);
    assert_eq!(Shape::Rect(3.0, 4.0).area(), 12.0);
    assert_eq!(Shape::Rect(0.0, 9.0).area(), 0.0);
    println!("OK");
}''',
         tests=['círculo de radio 1 tiene área `PI`', 'rectángulo 3 por 4 tiene área 12', 'rectángulo degenerado tiene área 0'],
         why='Un `enum` es un tipo suma: un valor es exactamente una de sus variantes. `match` debe cubrirlas todas, de modo que añadir una variante nueva rompe la compilación en cada `match` que no la trate.'),
    dict(ch=4, lang=L, level='INTERMEDIATE',
         prompt='Define el rasgo `trait Describe { fn describe(&self) -> String; }`, impleméntalo para `i32` (`"entero 5"`) y para `String` (`"texto hola"`), y escribe la función genérica `fn describe_all<T: Describe>(items: &[T]) -> Vec<String>`. Comprueba con una lista de enteros y una de cadenas.',
         code='''trait Describe {
    fn describe(&self) -> String;
}

impl Describe for i32 {
    fn describe(&self) -> String {
        format!("entero {self}")
    }
}

impl Describe for String {
    fn describe(&self) -> String {
        format!("texto {self}")
    }
}

fn describe_all<T: Describe>(items: &[T]) -> Vec<String> {
    items.iter().map(|item| item.describe()).collect()
}''',
         harness='''fn main() {
    assert_eq!(describe_all(&[5, -1]), vec!["entero 5", "entero -1"]);
    assert_eq!(describe_all(&[String::from("hola")]), vec!["texto hola"]);
    let empty: [i32; 0] = [];
    assert!(describe_all(&empty).is_empty());
    println!("OK");
}''',
         tests=['`[5, -1]` produce `["entero 5", "entero -1"]`', '`["hola"]` produce `["texto hola"]`', 'una lista vacía produce una lista vacía'],
         why='El límite `T: Describe` permite llamar a `describe` dentro de la función genérica. El compilador genera una versión para cada tipo concreto (monomorfización), de modo que no hay coste de despacho en ejecución.'),
    dict(ch=4, lang=L, level='ADVANCED',
         prompt='Define este tipo de error y escribe una función con la firma indicada:\n\n```rust\nenum AgeError { Empty, NotANumber, OutOfRange(u32) }\nfn parse_age(text: &str) -> Result<u8, AgeError>\n```\n\nUna cadena vacía (tras recortar) es `Empty`, un texto no numérico es `NotANumber` y un valor mayor que 150 es `OutOfRange(valor)`. Usa `?` y una conversión `From<std::num::ParseIntError>`. Comprueba `"42"`, `""`, `"abc"`, `"200"` y `"-3"`.',
         code='''use std::num::ParseIntError;

#[derive(Debug, PartialEq)]
enum AgeError {
    Empty,
    NotANumber,
    OutOfRange(u32),
}

impl From<ParseIntError> for AgeError {
    fn from(_: ParseIntError) -> Self {
        AgeError::NotANumber
    }
}

fn parse_age(text: &str) -> Result<u8, AgeError> {
    let text = text.trim();
    if text.is_empty() {
        return Err(AgeError::Empty);
    }
    let value: u32 = text.parse()?;
    if value > 150 {
        return Err(AgeError::OutOfRange(value));
    }
    Ok(value as u8)
}''',
         harness='''fn main() {
    assert_eq!(parse_age("42"), Ok(42));
    assert_eq!(parse_age("  7 "), Ok(7));
    assert_eq!(parse_age(""), Err(AgeError::Empty));
    assert_eq!(parse_age("abc"), Err(AgeError::NotANumber));
    assert_eq!(parse_age("200"), Err(AgeError::OutOfRange(200)));
    assert_eq!(parse_age("-3"), Err(AgeError::NotANumber));
    println!("OK");
}''',
         tests=['`"42"` devuelve `Ok(42)`', 'la cadena vacía devuelve `Empty`', '`"abc"` devuelve `NotANumber`', '`"200"` devuelve `OutOfRange(200)`', '`"-3"` no es un `u32` válido y devuelve `NotANumber`'],
         why='El operador `?` convierte el error de `parse` en `AgeError` mediante `From`, así que la función conserva una sola clase de error. Analizar como `u32` rechaza los negativos y permite informar del valor fuera de rango antes de reducirlo a `u8`.'),
    # ---- capítulo 5: closures, iteradores, punteros inteligentes
    dict(ch=5, lang=L, level='FOUNDATIONAL',
         prompt='Escribe `fn make_counter() -> impl FnMut() -> u32` que devuelva una clausura que cuente `1, 2, 3, ...` cada vez que se llama. Dos contadores creados por separado deben ser independientes.',
         code='''fn make_counter() -> impl FnMut() -> u32 {
    let mut count = 0;
    move || {
        count += 1;
        count
    }
}''',
         harness='''fn main() {
    let mut a = make_counter();
    let mut b = make_counter();
    assert_eq!((a(), a(), a()), (1, 2, 3));
    assert_eq!(b(), 1);
    assert_eq!(a(), 4);
    println!("OK");
}''',
         tests=['las tres primeras llamadas dan `1, 2, 3`', 'un segundo contador empieza en 1', 'el primero sigue en 4'],
         why='`move` transfiere `count` a la clausura, que lo conserva entre llamadas. Como la clausura modifica su estado, implementa `FnMut` y debe declararse `mut` para llamarla.'),
    dict(ch=5, lang=L, level='INTERMEDIATE',
         prompt='Escribe `fn top_words(text: &str, n: usize) -> Vec<(String, usize)>` que cuente las palabras (en minúscula, separadas por espacios y signos de puntuación) y devuelva las `n` más frecuentes, de mayor a menor frecuencia y, en caso de empate, en orden alfabético. Usa un `HashMap` y la cadena de iteradores. Comprueba con `"a b a c b a"` y `n = 2`.',
         code='''use std::collections::HashMap;

fn top_words(text: &str, n: usize) -> Vec<(String, usize)> {
    let mut counts: HashMap<String, usize> = HashMap::new();
    for word in text
        .split(|c: char| !c.is_alphanumeric())
        .filter(|w| !w.is_empty())
    {
        *counts.entry(word.to_lowercase()).or_insert(0) += 1;
    }
    let mut pairs: Vec<(String, usize)> = counts.into_iter().collect();
    pairs.sort_by(|a, b| b.1.cmp(&a.1).then_with(|| a.0.cmp(&b.0)));
    pairs.truncate(n);
    pairs
}''',
         harness='''fn main() {
    assert_eq!(
        top_words("a b a c b a", 2),
        vec![("a".to_string(), 3), ("b".to_string(), 2)]
    );
    assert_eq!(
        top_words("Hola, hola. ADIÓS adiós, hola!", 5),
        vec![("hola".to_string(), 3), ("adiós".to_string(), 2)]
    );
    assert!(top_words("", 3).is_empty());
    assert_eq!(top_words("x y", 0), vec![]);
    println!("OK");
}''',
         tests=['`"a b a c b a"` con `n = 2` devuelve `[("a", 3), ("b", 2)]`', 'ignora mayúsculas y puntuación', 'el texto vacío devuelve lista vacía', '`n = 0` devuelve lista vacía'],
         why='`entry(...).or_insert(0)` evita buscar dos veces. `HashMap` no garantiza el orden de recorrido, así que el resultado se ordena de forma explícita: primero por frecuencia descendente y después por palabra, para que la salida sea determinista.'),
    dict(ch=5, lang=L, level='ADVANCED',
         prompt='Dos manejadores comparten una cuenta. Escribe `fn transfer(from: &Rc<RefCell<i64>>, to: &Rc<RefCell<i64>>, amount: i64) -> Result<(), String>` que mueva `amount` de una cuenta a otra y devuelva `Err` sin modificar nada si el saldo de origen no alcanza. Comprueba con dos cuentas compartidas por `Rc::clone`.',
         code='''use std::cell::RefCell;
use std::rc::Rc;

fn transfer(from: &Rc<RefCell<i64>>, to: &Rc<RefCell<i64>>, amount: i64) -> Result<(), String> {
    if *from.borrow() < amount {
        return Err(format!("saldo insuficiente: {} < {amount}", from.borrow()));
    }
    *from.borrow_mut() -= amount;
    *to.borrow_mut() += amount;
    Ok(())
}''',
         harness='''fn main() {
    let a = Rc::new(RefCell::new(100));
    let b = Rc::new(RefCell::new(5));
    let a2 = Rc::clone(&a);
    assert!(transfer(&a, &b, 30).is_ok());
    assert_eq!((*a2.borrow(), *b.borrow()), (70, 35));
    assert!(transfer(&b, &a, 500).is_err());
    assert_eq!((*a.borrow(), *b.borrow()), (70, 35));
    assert_eq!(Rc::strong_count(&a), 2);
    println!("OK");
}''',
         tests=['transferir 30 deja `(70, 35)`', 'una transferencia mayor que el saldo falla', 'tras el fallo los saldos no cambian', 'el contador de referencias sigue en 2'],
         why='`Rc` permite varios propietarios y `RefCell` traslada la comprobación de préstamos a la ejecución: dos `borrow_mut` simultáneos sobre la misma celda producirían un pánico. Por eso se comprueba el saldo antes de pedir el préstamo mutable.'),
    # ---- capítulo 6: concurrencia
    dict(ch=6, lang=L, level='FOUNDATIONAL',
         prompt='Escribe `fn parallel_sum(values: &[u64], parts: usize) -> u64` que reparta `values` en `parts` fragmentos y sume cada uno en un hilo con `std::thread::scope`, sin clonar el vector. Comprueba que el resultado coincide con la suma secuencial para `1..=1000` con 1, 4 y 7 partes.',
         code='''use std::thread;

fn parallel_sum(values: &[u64], parts: usize) -> u64 {
    let size = values.len().div_ceil(parts.max(1)).max(1);
    thread::scope(|scope| {
        let handles: Vec<_> = values
            .chunks(size)
            .map(|chunk| scope.spawn(move || chunk.iter().sum::<u64>()))
            .collect();
        handles.into_iter().map(|h| h.join().unwrap()).sum()
    })
}''',
         harness='''fn main() {
    let data: Vec<u64> = (1..=1000).collect();
    for parts in [1, 4, 7] {
        assert_eq!(parallel_sum(&data, parts), 500_500);
    }
    assert_eq!(parallel_sum(&[], 3), 0);
    println!("OK");
}''',
         tests=['`1..=1000` con 1, 4 y 7 partes suma 500500', 'la lista vacía suma 0'],
         why='`thread::scope` garantiza que los hilos terminan antes de salir del alcance, de modo que pueden tomar prestadas rebanadas de `values` sin `Arc` ni copias. Cada hilo devuelve su suma parcial y el hilo principal las acumula.'),
    dict(ch=6, lang=L, level='INTERMEDIATE',
         prompt='Escribe `fn squares_via_channel(n: u32) -> Vec<u32>`: un hilo productor envía los cuadrados de `1..=n` por un canal `mpsc` y el hilo principal los recoge. Cuando el productor termina, el bucle de recepción debe acabar solo. Comprueba `n = 5` y `n = 0`.',
         code='''use std::sync::mpsc;
use std::thread;

fn squares_via_channel(n: u32) -> Vec<u32> {
    let (tx, rx) = mpsc::channel();
    let producer = thread::spawn(move || {
        for i in 1..=n {
            tx.send(i * i).unwrap();
        }
    });
    let result: Vec<u32> = rx.iter().collect();
    producer.join().unwrap();
    result
}''',
         harness='''fn main() {
    assert_eq!(squares_via_channel(5), vec![1, 4, 9, 16, 25]);
    assert!(squares_via_channel(0).is_empty());
    assert_eq!(squares_via_channel(1000).len(), 1000);
    println!("OK");
}''',
         tests=['`n = 5` devuelve `[1, 4, 9, 16, 25]`', '`n = 0` devuelve lista vacía', '`n = 1000` devuelve 1000 elementos'],
         why='`move` lleva `tx` al hilo productor. Cuando ese hilo termina, el emisor se destruye, el canal se cierra y `rx.iter()` deja de bloquear. Si el hilo principal conservara otro emisor, el bucle no terminaría nunca.'),
    dict(ch=6, lang=L, level='ADVANCED',
         prompt='Escribe `fn count_with_threads(threads: usize, per_thread: usize) -> usize` que lance `threads` hilos y que cada uno incremente `per_thread` veces un contador compartido con `Arc<Mutex<usize>>`. El valor final debe ser exactamente `threads * per_thread`. Comprueba 8 hilos con 10 000 incrementos.',
         code='''use std::sync::{Arc, Mutex};
use std::thread;

fn count_with_threads(threads: usize, per_thread: usize) -> usize {
    let counter = Arc::new(Mutex::new(0usize));
    let handles: Vec<_> = (0..threads)
        .map(|_| {
            let counter = Arc::clone(&counter);
            thread::spawn(move || {
                for _ in 0..per_thread {
                    *counter.lock().unwrap() += 1;
                }
            })
        })
        .collect();
    for handle in handles {
        handle.join().unwrap();
    }
    let total = *counter.lock().unwrap();
    total
}''',
         harness='''fn main() {
    assert_eq!(count_with_threads(8, 10_000), 80_000);
    assert_eq!(count_with_threads(1, 5), 5);
    assert_eq!(count_with_threads(0, 5), 0);
    println!("OK");
}''',
         tests=['8 hilos con 10 000 incrementos dan 80 000', '1 hilo con 5 incrementos da 5', '0 hilos dan 0'],
         why='`Arc` permite que varios hilos sean propietarios del mismo `Mutex`, y `lock` devuelve una guardia que libera el cerrojo al destruirse. Sin la exclusión mutua, dos hilos podrían leer el mismo valor y perder un incremento.'),
    # ---- capítulo 7: unsafe, FFI, macros
    dict(ch=7, lang=L, level='INTERMEDIATE',
         prompt='Escribe `unsafe fn swap_raw(a: *mut i32, b: *mut i32)` que intercambie dos enteros mediante punteros crudos, y una envoltura segura `fn swap(a: &mut i32, b: &mut i32)` que la use. Documenta en un comentario `// SAFETY:` por qué la llamada es válida. Comprueba el intercambio.',
         code='''unsafe fn swap_raw(a: *mut i32, b: *mut i32) {
    let tmp = unsafe { *a };
    unsafe {
        *a = *b;
        *b = tmp;
    }
}

fn swap(a: &mut i32, b: &mut i32) {
    // SAFETY: dos referencias mutables son validas, estan alineadas y no se solapan.
    unsafe { swap_raw(a, b) }
}''',
         harness='''fn main() {
    let (mut x, mut y) = (1, 2);
    swap(&mut x, &mut y);
    assert_eq!((x, y), (2, 1));
    swap(&mut x, &mut y);
    assert_eq!((x, y), (1, 2));
    println!("OK");
}''',
         tests=['`(1, 2)` pasa a `(2, 1)`', 'intercambiar dos veces devuelve el original'],
         why='El contrato de `swap_raw` es que ambos punteros sean válidos para leer y escribir y no se solapen; el compilador no puede comprobarlo, de ahí `unsafe`. La envoltura segura convierte ese contrato en un invariante de tipos: dos `&mut` distintos siempre lo cumplen.'),
    dict(ch=7, lang=L, level='INTERMEDIATE',
         prompt='Escribe la macro `max_of!` que acepte uno o más argumentos y devuelva el mayor, por ejemplo `max_of!(3, 9, 4) == 9`, usando `macro_rules!` y recursión. Comprueba con enteros y con números reales.',
         code='''macro_rules! max_of {
    ($x:expr) => ($x);
    ($x:expr, $($rest:expr),+) => {{
        let a = $x;
        let b = max_of!($($rest),+);
        if a > b { a } else { b }
    }};
}''',
         harness='''fn main() {
    assert_eq!(max_of!(7), 7);
    assert_eq!(max_of!(3, 9, 4), 9);
    assert_eq!(max_of!(1.5, -2.0), 1.5);
    assert_eq!(max_of!(2, 2, 2), 2);
    println!("OK");
}''',
         tests=['un argumento devuelve el mismo', '`max_of!(3, 9, 4)` es 9', 'funciona con `f64`', 'los iguales devuelven ese valor'],
         why='Una macro declarativa reconoce patrones sobre los fragmentos de sintaxis. La primera regla es el caso base; la segunda evalúa el primer argumento una sola vez y se llama a sí misma con el resto. Las llaves dobles crean un bloque que puede usarse como expresión.'),
    dict(ch=7, lang=L, level='ADVANCED',
         prompt='Declara con `extern "C"` la función `strlen` de la biblioteca de C y escribe `fn c_strlen(text: &std::ffi::CStr) -> usize` que la llame de forma segura. Comprueba `"hola"`, la cadena vacía y una cadena con texto UTF-8 (`"año"` mide 4 bytes).',
         code='''use std::ffi::{c_char, CStr};

unsafe extern "C" {
    fn strlen(s: *const c_char) -> usize;
}

fn c_strlen(text: &CStr) -> usize {
    // SAFETY: CStr garantiza un puntero valido terminado en cero.
    unsafe { strlen(text.as_ptr()) }
}''',
         harness='''use std::ffi::CString;

fn main() {
    assert_eq!(c_strlen(c"hola"), 4);
    assert_eq!(c_strlen(c""), 0);
    let utf8 = CString::new("año").unwrap();
    assert_eq!(c_strlen(&utf8), 4);
    assert_eq!(c_strlen(&utf8), "año".len());
    println!("OK");
}''',
         tests=['`"hola"` mide 4', 'la cadena vacía mide 0', '`"año"` mide 4 bytes en UTF-8'],
         why='Una función de C no tiene garantías de Rust, así que su declaración es `unsafe`. El tipo `CStr` asegura que el texto termina en cero y no contiene ceros intermedios, que es justo la precondición de `strlen`; la envoltura expone una interfaz segura. `strlen` cuenta bytes, no caracteres.'),
    # ---- capítulo 8: ecosistema y proyecto
    dict(ch=8, lang=L, level='INTERMEDIATE',
         prompt='Del motor `rust-kv-engine`: escribe `fn encode_record(key: &[u8], value: &[u8]) -> Vec<u8>` y `fn decode_record(buf: &[u8]) -> Option<(&[u8], &[u8], usize)>`. El formato es longitud de clave (`u32` little-endian), longitud de valor (`u32` little-endian), clave y valor. `decode_record` devuelve clave, valor y bytes consumidos, o `None` si el búfer está truncado. Comprueba la ida y vuelta y un búfer cortado.',
         code='''fn encode_record(key: &[u8], value: &[u8]) -> Vec<u8> {
    let mut out = Vec::with_capacity(8 + key.len() + value.len());
    out.extend_from_slice(&(key.len() as u32).to_le_bytes());
    out.extend_from_slice(&(value.len() as u32).to_le_bytes());
    out.extend_from_slice(key);
    out.extend_from_slice(value);
    out
}

fn decode_record(buf: &[u8]) -> Option<(&[u8], &[u8], usize)> {
    let key_len = u32::from_le_bytes(buf.get(0..4)?.try_into().ok()?) as usize;
    let value_len = u32::from_le_bytes(buf.get(4..8)?.try_into().ok()?) as usize;
    let key = buf.get(8..8 + key_len)?;
    let value = buf.get(8 + key_len..8 + key_len + value_len)?;
    Some((key, value, 8 + key_len + value_len))
}''',
         harness='''fn main() {
    let bytes = encode_record(b"clave", b"valor");
    assert_eq!(bytes.len(), 8 + 5 + 5);
    let (k, v, used) = decode_record(&bytes).unwrap();
    assert_eq!((k, v, used), (&b"clave"[..], &b"valor"[..], bytes.len()));
    assert!(decode_record(&bytes[..bytes.len() - 1]).is_none());
    assert!(decode_record(&bytes[..3]).is_none());
    let two = [encode_record(b"a", b""), encode_record(b"b", b"2")].concat();
    let (_, _, first) = decode_record(&two).unwrap();
    assert_eq!(decode_record(&two[first..]).unwrap().0, b"b");
    println!("OK");
}''',
         tests=['la ida y vuelta recupera clave y valor', 'la longitud codificada es 8 más clave más valor', 'un búfer truncado devuelve `None`', 'dos registros seguidos se leen uno tras otro'],
         why='`get` devuelve `None` en lugar de entrar en pánico cuando el rango no existe, así que un registro cortado por un fallo se detecta sin `unsafe`. Devolver los bytes consumidos permite recorrer un fichero con registros consecutivos.'),
    dict(ch=8, lang=L, level='INTERMEDIATE',
         prompt='Escribe `fn compact(log: &[(&str, Option<&str>)]) -> BTreeMap<String, String>` que reproduzca un registro de escrituras: `Some(valor)` asigna y `None` borra la clave. Debe quedar el último valor de cada clave viva. Comprueba un registro con asignaciones repetidas y un borrado.',
         code='''use std::collections::BTreeMap;

fn compact(log: &[(&str, Option<&str>)]) -> BTreeMap<String, String> {
    let mut state = BTreeMap::new();
    for (key, value) in log {
        match value {
            Some(v) => {
                state.insert(key.to_string(), v.to_string());
            }
            None => {
                state.remove(*key);
            }
        }
    }
    state
}''',
         harness='''fn main() {
    let log = [("a", Some("1")), ("b", Some("2")), ("a", Some("3")), ("b", None), ("c", Some("9"))];
    let state = compact(&log);
    let pairs: Vec<(&str, &str)> = state.iter().map(|(k, v)| (k.as_str(), v.as_str())).collect();
    assert_eq!(pairs, vec![("a", "3"), ("c", "9")]);
    assert!(compact(&[]).is_empty());
    assert!(compact(&[("x", None)]).is_empty());
    println!("OK");
}''',
         tests=['el último valor de `a` es `3`', '`b` queda borrada', '`c` se conserva', 'borrar una clave que no existe no falla'],
         why='Reproducir el registro en orden y aplicar cada operación reconstruye el estado; la compactación de un motor real escribe ese estado en un fichero nuevo y descarta el anterior. `BTreeMap` mantiene las claves ordenadas, lo que da una salida determinista.'),
    dict(ch=8, lang=L, level='ADVANCED',
         prompt='Escribe un `struct Lru` de capacidad fija con `fn new(capacity: usize) -> Lru`, `fn get(&mut self, key: &str) -> Option<i32>` y `fn put(&mut self, key: &str, value: i32)`. Al insertar con la caché llena se expulsa la clave usada hace más tiempo; `get` cuenta como uso. Comprueba una secuencia que expulse la clave correcta.',
         code='''use std::collections::HashMap;

struct Lru {
    capacity: usize,
    tick: u64,
    items: HashMap<String, (i32, u64)>,
}

impl Lru {
    fn new(capacity: usize) -> Lru {
        Lru { capacity, tick: 0, items: HashMap::new() }
    }

    fn get(&mut self, key: &str) -> Option<i32> {
        self.tick += 1;
        let tick = self.tick;
        self.items.get_mut(key).map(|entry| {
            entry.1 = tick;
            entry.0
        })
    }

    fn put(&mut self, key: &str, value: i32) {
        self.tick += 1;
        if !self.items.contains_key(key) && self.items.len() == self.capacity {
            if let Some(oldest) = self.items.iter().min_by_key(|(_, (_, used))| *used).map(|(k, _)| k.clone()) {
                self.items.remove(&oldest);
            }
        }
        if self.capacity > 0 {
            self.items.insert(key.to_string(), (value, self.tick));
        }
    }
}''',
         harness='''fn main() {
    let mut cache = Lru::new(2);
    cache.put("a", 1);
    cache.put("b", 2);
    assert_eq!(cache.get("a"), Some(1));
    cache.put("c", 3);
    assert_eq!(cache.get("b"), None);
    assert_eq!(cache.get("a"), Some(1));
    assert_eq!(cache.get("c"), Some(3));
    cache.put("c", 30);
    assert_eq!(cache.get("c"), Some(30));
    let mut none = Lru::new(0);
    none.put("x", 1);
    assert_eq!(none.get("x"), None);
    println!("OK");
}''',
         tests=['tras usar `a`, insertar `c` expulsa `b`', '`a` y `c` siguen presentes', 'actualizar una clave existente no expulsa nada', 'una capacidad cero no guarda nada'],
         why='Cada acceso marca la entrada con un contador creciente y la expulsión busca la marca más baja. La búsqueda lineal cuesta O(n); una implementación de producción usaría una lista enlazada para obtener O(1), pero la versión simple es fácil de verificar.'),
]
