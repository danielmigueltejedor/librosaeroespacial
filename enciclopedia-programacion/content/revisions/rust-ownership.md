El préstamo se entiende mejor empezando por una operación que el lector ya conoce: inspeccionar una colección sin consumirla. Una función que recibe `Vec<String>` obtiene la propiedad del vector; cuando devuelve el control, el llamador ya no puede seguir utilizándolo salvo que la función lo devuelva. Una función que recibe `&[String]` obtiene acceso compartido a una secuencia existente. La segunda interfaz expresa una necesidad menor: observar elementos, sin decidir quién libera la colección ni exigir que su almacenamiento proceda de un vector. Elegir la firma constituye parte del diseño, antes de escribir el cuerpo.

No interpretes una referencia como una dirección sin restricciones. La referencia incorpora un contrato de validez y acceso. Mientras un préstamo compartido sigue siendo utilizado, el propietario no puede realizar una modificación que lo invalide. Un préstamo mutable proporciona acceso exclusivo durante su uso. Esto impide que una función observe un elemento después de que otra operación haya realojado el almacenamiento que lo contenía. El compilador comprueba esos usos; no añade un recolector de basura que descubra el problema posteriormente.

En este programa la primera referencia deja de utilizarse antes de la modificación. Las instrucciones se presentan como una unidad de compilación completa y contienen una comprobación del resultado:

```rust
fn main() {
    let mut names = vec![String::from("Ada")];
    let first = &names[0];
    assert_eq!(first, "Ada");
    names.push(String::from("Grace"));
    assert_eq!(names.len(), 2);
}
```

Recorre el programa en orden. La creación del vector establece un propietario. La indexación obtiene un préstamo compartido de su primer elemento. La primera aserción utiliza ese préstamo. La llamada posterior a `push` necesita modificar el vector y podría realojar sus elementos. Como `first` no vuelve a utilizarse, el análisis de préstamos permite esa modificación. El ámbito textual de la variable y la región durante la que el préstamo debe mantenerse no son necesariamente lo mismo.

Como ejercicio de depuración, mueve la primera aserción detrás de `push`. La referencia tendría que seguir siendo válida después de una operación que puede modificar el almacenamiento. El compilador debe rechazar esa versión. El objetivo del ejercicio es explicar el conflicto, no memorizar un número de diagnóstico que puede variar entre versiones. Conserva ambos archivos y registra la versión de `rustc`, el estado de salida y el mensaje observado. La versión que falla intencionadamente no debe etiquetarse como un ejemplo ejecutable correcto.

Hay varias reparaciones con costes diferentes. Puedes terminar de observar el elemento antes de modificar la colección. Puedes conservar su índice y volver a consultar el vector después de la modificación, siempre que la operación no invalide el significado lógico del índice. También puedes clonar la cadena cuando necesites un valor independiente. Clonar introduce una copia y posiblemente una asignación; no es una solución automática a cualquier conflicto. La elección depende de si quieres identidad, posición o una instantánea del contenido.

Los parámetros de tiempo de vida describen relaciones entre referencias. No prolongan la vida de un objeto ni reservan memoria. Si una función devuelve una referencia que proviene de uno de sus argumentos, la firma debe permitir relacionar la validez del resultado con el argumento adecuado. Cuando las reglas de elisión bastan, escribir todos los parámetros explícitamente añade ruido. Cuando hay varias entradas y una salida prestada, piensa primero qué relación puede cumplir la implementación para todas las llamadas permitidas. Una anotación no puede convertir una referencia a una variable local destruida en un resultado válido.

Tampoco debes confundir seguridad de memoria con corrección funcional. Un programa puede respetar todos los préstamos y devolver un resultado incorrecto, entrar en un bucle, filtrar memoria o bloquearse por un protocolo de sincronización defectuoso. Las garantías de las interfaces seguras dependen de que el compilador y las implementaciones `unsafe` de las que dependen sean correctos. Una biblioteca con una abstracción no sólida puede exponer comportamiento indefinido a sus clientes seguros. Esta es la razón de revisar los contratos de seguridad al encapsular punteros o interactuar mediante FFI.

Práctica guiada: escribe una función que reciba una rebanada de cadenas y devuelva la longitud de la primera, o cero si está vacía. Prueba una secuencia vacía, una cadena vacía y dos cadenas de longitudes distintas. Después cambia el resultado a `Option<usize>` y explica qué información conserva esta segunda interfaz. Las longitudes de `String` cuentan bytes UTF-8; si quieres contar valores escalares debes definir otra operación, y ninguno de esos recuentos equivale necesariamente a caracteres percibidos por una persona.

Práctica autónoma: diseña dos interfaces para seleccionar el primer nombre que cumpla un predicado, una que devuelva una referencia y otra que devuelva una cadena propia. Justifica el comportamiento cuando no hay coincidencias, cuándo hace falta una copia y cuánto tiempo puede conservarse el resultado. La solución debe incluir pruebas del caso vacío y del caso sin coincidencias. Revisar la firma, las pruebas y los costes constituye una evaluación más útil que calcular únicamente el número de bytes de un vector.
