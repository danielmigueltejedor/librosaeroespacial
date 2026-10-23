"""Programming exercises of volume 4 (C, C++, Zig, assembly, Fortran). Each reference program runs with a real compiler."""

EXERCISES = [
    # ---- capítulo 1: C, tipos y traducción
    dict(ch=1, lang='c', level='FOUNDATIONAL',
         prompt='Escribe `uint8_t make_mask(const int *bits, size_t n)` que devuelva un byte con activos los bits cuyas posiciones (0 a 7) están en `bits`. Ignora las posiciones fuera de rango. Comprueba que `{0, 3, 7}` da 137 (`0x89`) y que la lista vacía da 0.',
         code='''#include <stddef.h>
#include <stdint.h>

uint8_t make_mask(const int *bits, size_t n) {
    uint8_t mask = 0;
    for (size_t i = 0; i < n; i++) {
        if (bits[i] >= 0 && bits[i] < 8) {
            mask = (uint8_t)(mask | (1u << bits[i]));
        }
    }
    return mask;
}''',
         harness='''#include <stdio.h>

int main(void) {
    int a[] = {0, 3, 7};
    int b[] = {1, 1, 9, -2};
    if (make_mask(a, 3) != 137) return 1;
    if (make_mask(b, 4) != 2) return 2;
    if (make_mask(a, 0) != 0) return 3;
    puts("OK");
    return 0;
}''',
         tests=['`{0, 3, 7}` da 137', 'las posiciones repetidas y fuera de rango no cambian el resultado', 'la lista vacía da 0'],
         why='`1u << bits[i]` construye el bit, y el `or` lo activa sin tocar los demás. El resultado se convierte explícitamente a `uint8_t` porque la expresión se promueve a `unsigned int`. Desplazar por 8 o más sería comportamiento indefinido, por eso se comprueba el rango antes.'),
    dict(ch=1, lang='c', level='INTERMEDIATE',
         prompt='Escribe `int checked_add(int a, int b, int *out)` que guarde en `*out` la suma y devuelva 1, o devuelva 0 sin tocar `*out` si la suma desbordaría `int`. El desbordamiento de enteros con signo es comportamiento indefinido, así que debes comprobarlo antes de sumar, sin recurrir a extensiones del compilador. Comprueba `INT_MAX + 1`, `INT_MIN + -1` y casos normales.',
         code='''#include <limits.h>

int checked_add(int a, int b, int *out) {
    if ((b > 0 && a > INT_MAX - b) || (b < 0 && a < INT_MIN - b)) {
        return 0;
    }
    *out = a + b;
    return 1;
}''',
         harness='''#include <stdio.h>

int main(void) {
    int r = 7;
    if (!checked_add(2, 3, &r) || r != 5) return 1;
    if (!checked_add(INT_MAX, 0, &r) || r != INT_MAX) return 2;
    r = 99;
    if (checked_add(INT_MAX, 1, &r) || r != 99) return 3;
    if (checked_add(INT_MIN, -1, &r) || r != 99) return 4;
    if (!checked_add(INT_MIN, INT_MAX, &r) || r != -1) return 5;
    puts("OK");
    return 0;
}''',
         tests=['`2 + 3` devuelve 1 y escribe 5', '`INT_MAX + 0` es válido', '`INT_MAX + 1` devuelve 0 y no modifica la salida', '`INT_MIN + -1` devuelve 0', '`INT_MIN + INT_MAX` da -1'],
         why='La comprobación se reescribe para que nunca se ejecute la suma que desbordaría: `a > INT_MAX - b` equivale a `a + b > INT_MAX` sin salirse del rango. Solo después de comprobar se realiza la suma.'),
    dict(ch=1, lang='c', kind='debugging', level='INTERMEDIATE',
         prompt='Depuración. Esta función copia mal cuando el origen no cabe: no deja terminador y escribe un byte de más.\n\n```c\nvoid copy_bounded(char *dst, size_t cap, const char *src) {\n    for (size_t i = 0; i <= cap; i++) dst[i] = src[i];\n}\n```\n\nCorrígela: debe copiar como máximo `cap - 1` caracteres y terminar `dst` siempre con `\'\\0\'` si `cap > 0`. Comprueba un origen corto, uno largo y `cap == 1`.',
         code='''#include <stddef.h>

void copy_bounded(char *dst, size_t cap, const char *src) {
    if (cap == 0) {
        return;
    }
    size_t i = 0;
    while (i + 1 < cap && src[i] != '\\0') {
        dst[i] = src[i];
        i++;
    }
    dst[i] = '\\0';
}''',
         harness='''#include <stdio.h>
#include <string.h>

int main(void) {
    char buf[8];
    memset(buf, 'x', sizeof buf);
    copy_bounded(buf, 8, "hola");
    if (strcmp(buf, "hola") != 0) return 1;
    copy_bounded(buf, 4, "abcdefgh");
    if (strcmp(buf, "abc") != 0) return 2;
    copy_bounded(buf, 1, "zzz");
    if (buf[0] != '\\0') return 3;
    memset(buf, 'x', sizeof buf);
    copy_bounded(buf, 0, "zzz");
    if (buf[0] != 'x') return 4;
    puts("OK");
    return 0;
}''',
         tests=['"hola" cabe en 8 bytes y queda terminado', '"abcdefgh" en 4 bytes queda como "abc"', 'con `cap == 1` solo se escribe el terminador', 'con `cap == 0` no se escribe nada'],
         why='El bucle original usaba `<=` y escribía `cap + 1` bytes, además de copiar sin comprobar el final del origen. La versión correcta reserva siempre el último byte para el terminador, la regla que debe cumplir toda función que escriba en un búfer de tamaño dado.'),
    # ---- capítulo 2: punteros y memoria dinámica
    dict(ch=2, lang='c', level='FOUNDATIONAL',
         prompt='Escribe `int *dup_array(const int *src, size_t n)` que reserve memoria con `malloc`, copie `n` enteros y devuelva el nuevo array, o `NULL` si `n` es 0 o si falla la reserva. Comprueba que la copia es independiente del original y que la reserva se libera.',
         code='''#include <stdlib.h>
#include <string.h>

int *dup_array(const int *src, size_t n) {
    if (n == 0) {
        return NULL;
    }
    int *copy = malloc(n * sizeof *copy);
    if (copy == NULL) {
        return NULL;
    }
    memcpy(copy, src, n * sizeof *copy);
    return copy;
}''',
         harness='''#include <stdio.h>

int main(void) {
    int a[] = {1, 2, 3, 4};
    int *b = dup_array(a, 4);
    if (b == NULL || b == a) return 1;
    a[0] = 99;
    if (b[0] != 1 || b[3] != 4) return 2;
    free(b);
    if (dup_array(a, 0) != NULL) return 3;
    puts("OK");
    return 0;
}''',
         tests=['la copia tiene los mismos valores', 'modificar el original no cambia la copia', '`n == 0` devuelve `NULL`', 'la reserva se libera con `free`'],
         why='`sizeof *copy` calcula el tamaño a partir de la variable y no del tipo, así que no queda desactualizado si cambia el tipo. Quien llama es responsable de liberar el resultado: el contrato de propiedad debe estar documentado junto a la función.'),
    dict(ch=2, lang='c', level='INTERMEDIATE',
         prompt='Implementa un asignador de arena: `typedef struct { unsigned char *base; size_t cap, used; } Arena;` y `void *arena_alloc(Arena *a, size_t size, size_t align)`, que devuelva memoria alineada a `align` (potencia de dos) o `NULL` si no cabe. Comprueba que las direcciones están alineadas, que no se solapan y que al agotarse devuelve `NULL`.',
         code='''#include <stddef.h>
#include <stdint.h>

typedef struct {
    unsigned char *base;
    size_t cap, used;
} Arena;

void *arena_alloc(Arena *a, size_t size, size_t align) {
    uintptr_t start = (uintptr_t)a->base + a->used;
    uintptr_t aligned = (start + (align - 1)) & ~(uintptr_t)(align - 1);
    size_t offset = (size_t)(aligned - (uintptr_t)a->base);
    if (offset > a->cap || size > a->cap - offset) {
        return NULL;
    }
    a->used = offset + size;
    return a->base + offset;
}''',
         harness='''#include <stdio.h>

int main(void) {
    _Alignas(64) unsigned char storage[256];
    Arena arena = {storage, sizeof storage, 0};
    unsigned char *a = arena_alloc(&arena, 3, 1);
    unsigned char *b = arena_alloc(&arena, 8, 8);
    unsigned char *c = arena_alloc(&arena, 16, 16);
    if (!a || !b || !c) return 1;
    if (((uintptr_t)b % 8) != 0 || ((uintptr_t)c % 16) != 0) return 2;
    if (b < a + 3 || c < b + 8) return 3;
    if (arena_alloc(&arena, 1000, 1) != NULL) return 4;
    if (arena.used > arena.cap) return 5;
    if (arena_alloc(&arena, arena.cap - arena.used, 1) == NULL) return 6;
    if (arena_alloc(&arena, 1, 1) != NULL) return 7;
    puts("OK");
    return 0;
}''',
         tests=['cada reserva respeta su alineamiento', 'las reservas no se solapan', 'una petición mayor que el espacio libre devuelve `NULL`', 'se puede consumir exactamente todo el espacio restante'],
         why='El redondeo `(x + align - 1) & ~(align - 1)` solo vale cuando `align` es potencia de dos. Se comprueba el espacio con restas sobre `size_t` para no desbordar. Una arena no libera elementos sueltos: se descarta entera reiniciando `used`.'),
    dict(ch=2, lang='c', level='INTERMEDIATE',
         prompt='Dada `typedef struct Node { int value; struct Node *next; } Node;`, escribe `Node *reverse(Node *head)` que invierta la lista enlazada in situ, sin reservar memoria, y devuelva la nueva cabeza. Comprueba una lista de tres nodos, una de uno y la lista vacía.',
         code='''typedef struct Node {
    int value;
    struct Node *next;
} Node;

Node *reverse(Node *head) {
    Node *previous = 0;
    while (head != 0) {
        Node *next = head->next;
        head->next = previous;
        previous = head;
        head = next;
    }
    return previous;
}''',
         harness='''#include <stdio.h>

int main(void) {
    Node c = {3, 0}, b = {2, &c}, a = {1, &b};
    Node *head = reverse(&a);
    if (head != &c || head->next != &b || head->next->next != &a || a.next != 0) return 1;
    Node solo = {9, 0};
    if (reverse(&solo) != &solo) return 2;
    if (reverse(0) != 0) return 3;
    puts("OK");
    return 0;
}''',
         tests=['`1 -> 2 -> 3` pasa a `3 -> 2 -> 1`', 'una lista de un nodo no cambia', 'la lista vacía devuelve `NULL`'],
         why='Tres punteros recorren la lista: el nodo actual, el siguiente guardado antes de romper el enlace y el anterior. Guardar `next` primero es lo que evita perder el resto de la lista.'),
    # ---- capítulo 3: concurrencia y recursos
    dict(ch=3, lang='c', level='INTERMEDIATE',
         prompt='Escribe `long run_counter(int threads, int per_thread)` que lance `threads` hilos POSIX y que cada uno incremente `per_thread` veces un contador global protegido con `pthread_mutex_t`. Debe devolver `threads * per_thread`. Comprueba 8 hilos con 10 000 incrementos.',
         code='''#include <pthread.h>

static long counter;
static pthread_mutex_t lock = PTHREAD_MUTEX_INITIALIZER;

static void *work(void *arg) {
    int n = *(int *)arg;
    for (int i = 0; i < n; i++) {
        pthread_mutex_lock(&lock);
        counter++;
        pthread_mutex_unlock(&lock);
    }
    return 0;
}

long run_counter(int threads, int per_thread) {
    pthread_t ids[64];
    counter = 0;
    for (int i = 0; i < threads; i++) {
        pthread_create(&ids[i], 0, work, &per_thread);
    }
    for (int i = 0; i < threads; i++) {
        pthread_join(ids[i], 0);
    }
    return counter;
}''',
         harness='''#include <stdio.h>

int main(void) {
    if (run_counter(8, 10000) != 80000) return 1;
    if (run_counter(1, 5) != 5) return 2;
    if (run_counter(0, 5) != 0) return 3;
    puts("OK");
    return 0;
}''',
         tests=['8 hilos con 10 000 incrementos dan 80 000', '1 hilo con 5 da 5', '0 hilos dan 0'],
         why='`counter++` son tres operaciones (leer, sumar, escribir) y dos hilos pueden entrelazarlas y perder una. El cerrojo hace que cada incremento sea indivisible respecto a los demás. Los hilos se unen con `pthread_join` antes de leer el resultado.'),
    dict(ch=3, lang='c', level='ADVANCED',
         prompt='Escribe `int open_all(int fail_at)` que adquiera en orden tres recursos con `malloc` (A, B y C) y, si la adquisición número `fail_at` (1, 2 o 3) falla (se simula con un parámetro; 0 significa que no falla), libere con la cascada `goto cleanup` solo los ya adquiridos, en orden inverso, y devuelva -1. Si todo va bien, libera los tres y devuelve 0. Comprueba mediante contadores globales que cada recurso adquirido se libera exactamente una vez.',
         code='''#include <stdlib.h>

int acquired, released;

static void *take(int number, int fail_at) {
    if (number == fail_at) {
        return NULL;
    }
    acquired++;
    return malloc(16);
}

static void give(void *p) {
    released++;
    free(p);
}

int open_all(int fail_at) {
    int status = -1;
    void *a = NULL, *b = NULL, *c = NULL;
    a = take(1, fail_at);
    if (a == NULL) goto cleanup;
    b = take(2, fail_at);
    if (b == NULL) goto cleanup;
    c = take(3, fail_at);
    if (c == NULL) goto cleanup;
    status = 0;
cleanup:
    if (c) give(c);
    if (b) give(b);
    if (a) give(a);
    return status;
}''',
         harness='''#include <stdio.h>

int main(void) {
    int codes[] = {0, 1, 2, 3};
    int expected_status[] = {0, -1, -1, -1};
    int expected_acquired[] = {3, 0, 1, 2};
    for (int i = 0; i < 4; i++) {
        acquired = released = 0;
        if (open_all(codes[i]) != expected_status[i]) return 1;
        if (acquired != expected_acquired[i] || released != acquired) return 2;
    }
    puts("OK");
    return 0;
}''',
         tests=['sin fallos se adquieren y liberan 3 recursos y devuelve 0', 'si falla el primero no se libera nada', 'si falla el segundo se libera solo el primero', 'si falla el tercero se liberan los dos primeros', 'en todos los casos liberados es igual a adquiridos'],
         why='Todos los punteros se inicializan a `NULL`, de modo que la etiqueta `cleanup` puede ejecutarse desde cualquier punto y liberar solo lo adquirido. El orden inverso respeta las dependencias entre recursos. Es el patrón habitual de gestión de errores en C sin excepciones.'),
    dict(ch=3, lang='c', level='ADVANCED',
         prompt='Escribe `int atomic_total(int threads, int per_thread)` que use `_Atomic int` de C11 y `atomic_fetch_add` para que varios hilos incrementen un contador compartido sin cerrojo. Comprueba 4 hilos con 25 000 incrementos cada uno.',
         code='''#include <pthread.h>
#include <stdatomic.h>

static atomic_int total;

static void *work(void *arg) {
    int n = *(int *)arg;
    for (int i = 0; i < n; i++) {
        atomic_fetch_add_explicit(&total, 1, memory_order_relaxed);
    }
    return 0;
}

int atomic_total(int threads, int per_thread) {
    pthread_t ids[64];
    atomic_store(&total, 0);
    for (int i = 0; i < threads; i++) {
        pthread_create(&ids[i], 0, work, &per_thread);
    }
    for (int i = 0; i < threads; i++) {
        pthread_join(ids[i], 0);
    }
    return atomic_load(&total);
}''',
         harness='''#include <stdio.h>

int main(void) {
    if (atomic_total(4, 25000) != 100000) return 1;
    if (atomic_total(2, 0) != 0) return 2;
    puts("OK");
    return 0;
}''',
         tests=['4 hilos con 25 000 incrementos dan 100 000', 'con 0 incrementos el total es 0'],
         why='`atomic_fetch_add` hace la lectura, la suma y la escritura como una sola operación indivisible. Con `memory_order_relaxed` solo se garantiza la atomicidad del contador, no ningún orden respecto a otras variables, que es suficiente para una cuenta cuyo valor se lee tras `pthread_join`.'),
    # ---- capítulo 4: C++ RAII y movimiento
    dict(ch=4, lang='cpp', level='FOUNDATIONAL',
         prompt='Escribe la clase `ScopeLog` que, en el constructor, añada `"entra <nombre>"` a un `std::vector<std::string>&` y, en el destructor, `"sale <nombre>"`. Comprueba con bloques anidados que el orden de salida es el inverso al de entrada.',
         code='''#include <string>
#include <vector>

class ScopeLog {
public:
    ScopeLog(std::vector<std::string>& log, std::string name)
        : log_(log), name_(std::move(name)) {
        log_.push_back("entra " + name_);
    }
    ~ScopeLog() { log_.push_back("sale " + name_); }
    ScopeLog(const ScopeLog&) = delete;
    ScopeLog& operator=(const ScopeLog&) = delete;

private:
    std::vector<std::string>& log_;
    std::string name_;
};''',
         harness='''#include <cstdio>

int main() {
    std::vector<std::string> log;
    {
        ScopeLog a(log, "a");
        {
            ScopeLog b(log, "b");
        }
    }
    const std::vector<std::string> expected{"entra a", "entra b", "sale b", "sale a"};
    if (log != expected) return 1;
    std::puts("OK");
    return 0;
}''',
         tests=['el registro es `entra a, entra b, sale b, sale a`', 'el destructor se ejecuta al salir de cada bloque'],
         why='RAII liga la vida de un recurso a la de un objeto: el destructor se ejecuta siempre al salir del alcance, incluso con excepciones. Se prohíbe copiar el guardián para que cada entrada tenga exactamente una salida.'),
    dict(ch=4, lang='cpp', level='INTERMEDIATE',
         prompt='Escribe `class Buffer` que posea un array dinámico de `int` (`std::size_t size()`, `int& operator[](std::size_t)`), con constructor `Buffer(std::size_t n)`, **sin copia** y con **movimiento**: tras mover, el origen queda vacío (`size() == 0`). Comprueba que mover transfiere el contenido sin copiarlo y que el origen queda utilizable.',
         code='''#include <cstddef>
#include <utility>

class Buffer {
public:
    explicit Buffer(std::size_t n) : size_(n), data_(new int[n]()) {}
    ~Buffer() { delete[] data_; }
    Buffer(const Buffer&) = delete;
    Buffer& operator=(const Buffer&) = delete;
    Buffer(Buffer&& other) noexcept
        : size_(std::exchange(other.size_, 0)), data_(std::exchange(other.data_, nullptr)) {}
    Buffer& operator=(Buffer&& other) noexcept {
        if (this != &other) {
            delete[] data_;
            size_ = std::exchange(other.size_, 0);
            data_ = std::exchange(other.data_, nullptr);
        }
        return *this;
    }
    std::size_t size() const { return size_; }
    int& operator[](std::size_t i) { return data_[i]; }

private:
    std::size_t size_;
    int* data_;
};''',
         harness='''#include <cstdio>
#include <type_traits>

int main() {
    static_assert(!std::is_copy_constructible_v<Buffer>);
    static_assert(std::is_nothrow_move_constructible_v<Buffer>);
    Buffer a(4);
    a[2] = 42;
    int* raw = &a[0];
    Buffer b(std::move(a));
    if (b.size() != 4 || b[2] != 42 || &b[0] != raw) return 1;
    if (a.size() != 0) return 2;
    Buffer c(1);
    c = std::move(b);
    if (c.size() != 4 || b.size() != 0) return 3;
    std::puts("OK");
    return 0;
}''',
         tests=['el constructor de copia está prohibido', 'mover conserva el contenido y la dirección del búfer', 'el origen queda con tamaño 0', 'la asignación por movimiento libera el búfer anterior'],
         why='`std::exchange` toma el valor y deja uno neutro en el origen en una sola expresión. Marcar los movimientos `noexcept` permite que contenedores como `std::vector` los usen al crecer en lugar de copiar. Tener destructor propio obliga a definir o prohibir copia y movimiento: es la regla de los cinco.'),
    dict(ch=4, lang='cpp', level='INTERMEDIATE',
         prompt='Escribe `std::vector<long> counts_after()` que cree un `std::shared_ptr<int>`, lo copie en un segundo `shared_ptr`, cree un `std::weak_ptr` y devuelva en este orden `use_count()` tras crear el primero, tras copiarlo, tras crear el `weak_ptr` y tras destruir la copia (dentro de un bloque). Después de liberar todos los propietarios, `weak_ptr::expired()` debe ser verdadero. Comprueba `{1, 2, 2, 1}`.',
         code='''#include <memory>
#include <vector>

std::vector<long> counts_after(bool& expired_at_end) {
    std::vector<long> counts;
    std::weak_ptr<int> weak;
    {
        auto first = std::make_shared<int>(7);
        counts.push_back(first.use_count());
        {
            auto second = first;
            counts.push_back(first.use_count());
            weak = first;
            counts.push_back(first.use_count());
        }
        counts.push_back(first.use_count());
    }
    expired_at_end = weak.expired();
    return counts;
}''',
         harness='''#include <cstdio>

int main() {
    bool expired = false;
    const std::vector<long> expected{1, 2, 2, 1};
    if (counts_after(expired) != expected) return 1;
    if (!expired) return 2;
    std::puts("OK");
    return 0;
}''',
         tests=['`use_count` sigue `1, 2, 2, 1`', 'crear un `weak_ptr` no aumenta `use_count`', 'tras liberar todos los propietarios el `weak_ptr` ha expirado'],
         why='`shared_ptr` cuenta propietarios; `weak_ptr` observa sin poseer, así que no mantiene vivo el objeto ni cuenta. Es la herramienta para romper ciclos y para cachés que no deben alargar la vida de lo que guardan.'),
    # ---- capítulo 5: plantillas, conceptos y rangos
    dict(ch=5, lang='cpp', level='INTERMEDIATE',
         prompt='Escribe la plantilla variádica `template <std::integral... T> constexpr auto sum_all(T... values)` con una expresión pliegue. Comprueba en tiempo de compilación (`static_assert`) que `sum_all(10, 20, 30, 40) == 100` y que `sum_all()` devuelve 0. Comprueba también que el concepto rechaza un `double`.',
         code='''#include <concepts>

template <std::integral... T>
constexpr auto sum_all(T... values) {
    return (0 + ... + values);
}''',
         harness='''#include <cstdio>
#include <type_traits>

template <class... T>
concept CanSum = requires(T... v) { sum_all(v...); };

static_assert(sum_all(10, 20, 30, 40) == 100);
static_assert(sum_all() == 0);
static_assert(sum_all(1, 2L, 3u) == 6);
static_assert(CanSum<int, int>);
static_assert(!CanSum<double>);

int main() {
    std::puts("OK");
    return 0;
}''',
         tests=['`sum_all(10, 20, 30, 40)` es 100 en tiempo de compilación', '`sum_all()` es 0', 'mezcla de tipos enteros', '`double` no satisface el concepto'],
         why='La expresión pliegue `(0 + ... + values)` expande el paquete en una cadena de sumas, con 0 como valor inicial para que el paquete vacío sea válido. El concepto `std::integral` convierte el error de usar un `double` en un mensaje claro de la restricción incumplida.'),
    dict(ch=5, lang='cpp', level='INTERMEDIATE',
         prompt='Escribe `std::vector<int> first_even_squares(int n)` con `std::views`: los cuadrados de los `n` primeros números pares positivos. No bucles manuales. Comprueba `n = 4 -> {4, 16, 36, 64}` y `n = 0`.',
         code='''#include <ranges>
#include <vector>

std::vector<int> first_even_squares(int n) {
    auto view = std::views::iota(1)
        | std::views::filter([](int x) { return x % 2 == 0; })
        | std::views::transform([](int x) { return x * x; })
        | std::views::take(n)
        | std::views::common;
    return {view.begin(), view.end()};
}''',
         harness='''#include <cstdio>

int main() {
    const std::vector<int> expected{4, 16, 36, 64};
    if (first_even_squares(4) != expected) return 1;
    if (!first_even_squares(0).empty()) return 2;
    if (first_even_squares(1) != std::vector<int>{4}) return 3;
    std::puts("OK");
    return 0;
}''',
         tests=['`n = 4` devuelve `{4, 16, 36, 64}`', '`n = 0` devuelve vector vacío', '`n = 1` devuelve `{4}`'],
         why='`iota(1)` es una secuencia infinita y perezosa: solo se calculan los elementos que `take` consume. Cada adaptador compone una vista sin crear contenedores intermedios; `common` hace que el inicio y el fin tengan el mismo tipo para poder construir el vector de una vez.'),
    dict(ch=5, lang='cpp', level='ADVANCED',
         prompt='Escribe `template <class T> class Stack` con `push(T)`, `T pop()` y `bool empty() const`, de forma que `pop` en una pila vacía lance `std::out_of_range`. Comprueba con `int` y con `std::string`, el orden LIFO y la excepción.',
         code='''#include <stdexcept>
#include <utility>
#include <vector>

template <class T>
class Stack {
public:
    void push(T value) { items_.push_back(std::move(value)); }
    T pop() {
        if (items_.empty()) {
            throw std::out_of_range("pila vacia");
        }
        T top = std::move(items_.back());
        items_.pop_back();
        return top;
    }
    bool empty() const { return items_.empty(); }

private:
    std::vector<T> items_;
};''',
         harness='''#include <cstdio>
#include <string>

int main() {
    Stack<int> s;
    s.push(1);
    s.push(2);
    if (s.pop() != 2 || s.pop() != 1 || !s.empty()) return 1;
    bool thrown = false;
    try {
        s.pop();
    } catch (const std::out_of_range&) {
        thrown = true;
    }
    if (!thrown) return 2;
    Stack<std::string> t;
    t.push("a");
    t.push("b");
    if (t.pop() != "b") return 3;
    std::puts("OK");
    return 0;
}''',
         tests=['`push(1)`, `push(2)` y dos `pop` devuelven 2 y 1', '`pop` en pila vacía lanza `std::out_of_range`', 'funciona con `std::string`'],
         why='La plantilla se instancia para cada tipo. `pop` devuelve por valor tras mover el elemento, lo que da garantía básica ante excepciones: si el movimiento fallase, el estado interno no queda a medias porque el elemento se retira después.'),
    # ---- capítulo 6: Zig
    dict(ch=6, lang='zig-test', level='FOUNDATIONAL', expect='',
         prompt='Escribe en Zig `fn fibonacci(n: u32) u64` iterativa y comprueba con `test` y `std.testing` que `fibonacci(0) == 0`, `fibonacci(1) == 1` y `fibonacci(50) == 12586269025`.',
         code='''const std = @import("std");

fn fibonacci(n: u32) u64 {
    var a: u64 = 0;
    var b: u64 = 1;
    var i: u32 = 0;
    while (i < n) : (i += 1) {
        const next = a + b;
        a = b;
        b = next;
    }
    return a;
}''',
         harness='''test "fibonacci" {
    try std.testing.expectEqual(@as(u64, 0), fibonacci(0));
    try std.testing.expectEqual(@as(u64, 1), fibonacci(1));
    try std.testing.expectEqual(@as(u64, 12586269025), fibonacci(50));
}''',
         tests=['`fibonacci(0)` es 0', '`fibonacci(1)` es 1', '`fibonacci(50)` es 12586269025'],
         why='Zig no tiene asignaciones ocultas ni flujo de control implícito: el bucle `while` con la expresión de continuación `: (i += 1)` es explícito. Un desbordamiento de `u64` sería un error detectable en las compilaciones de depuración; `fibonacci(93)` ya no cabe.'),
    dict(ch=6, lang='zig-test', level='INTERMEDIATE', expect='',
         prompt='Escribe en Zig `fn joinWords(allocator: std.mem.Allocator, words: []const []const u8) ![]u8` que una las palabras con un espacio y devuelva memoria reservada con el asignador recibido. Comprueba con `std.testing.allocator`, que detecta fugas, que `{"a", "bc"}` da `"a bc"` y que la lista vacía da `""`.',
         code='''const std = @import("std");

fn joinWords(allocator: std.mem.Allocator, words: []const []const u8) ![]u8 {
    var total: usize = 0;
    for (words) |w| total += w.len;
    if (words.len > 1) total += words.len - 1;
    const out = try allocator.alloc(u8, total);
    var pos: usize = 0;
    for (words, 0..) |w, i| {
        if (i > 0) {
            out[pos] = ' ';
            pos += 1;
        }
        @memcpy(out[pos .. pos + w.len], w);
        pos += w.len;
    }
    return out;
}''',
         harness='''test "joinWords" {
    const a = std.testing.allocator;
    const joined = try joinWords(a, &.{ "a", "bc" });
    defer a.free(joined);
    try std.testing.expectEqualStrings("a bc", joined);
    const empty = try joinWords(a, &.{});
    defer a.free(empty);
    try std.testing.expectEqualStrings("", empty);
}''',
         tests=['`{"a", "bc"}` da `"a bc"`', 'la lista vacía da la cadena vacía', 'el asignador de pruebas no detecta fugas'],
         why='En Zig el asignador es un parámetro explícito: quien llama decide de dónde sale la memoria y quién la libera. `defer` libera al salir del bloque, y `std.testing.allocator` falla la prueba si algo no se libera.'),
    dict(ch=6, lang='zig-test', level='INTERMEDIATE', expect='',
         prompt='Escribe en Zig una función `comptime` `fn tableSquares(comptime n: usize) [n]u32` que calcule en tiempo de compilación la tabla de cuadrados de `0` a `n - 1`. Comprueba con `comptime` que `tableSquares(5)` es `{0, 1, 4, 9, 16}`.',
         code='''const std = @import("std");

fn tableSquares(comptime n: usize) [n]u32 {
    var table: [n]u32 = undefined;
    for (&table, 0..) |*slot, i| {
        slot.* = @intCast(i * i);
    }
    return table;
}''',
         harness='''test "tableSquares" {
    const t = comptime tableSquares(5);
    try std.testing.expectEqualSlices(u32, &.{ 0, 1, 4, 9, 16 }, &t);
}''',
         tests=['`tableSquares(5)` es `{0, 1, 4, 9, 16}` evaluada en compilación'],
         why='El parámetro `comptime n` forma parte del tipo del resultado: `[5]u32` y `[8]u32` son tipos distintos. El bucle se ejecuta durante la compilación, de modo que la tabla ya está calculada en el binario sin coste en ejecución.'),
    # ---- capítulo 7: ensamblador AArch64
    dict(ch=7, lang='asm-arm64', level='INTERMEDIATE',
         prompt='Escribe en ensamblador AArch64 (convención de llamada de Apple, símbolo con guion bajo) la función `long sum_to(long n)` que devuelva `1 + 2 + ... + n` con un bucle y `0` si `n <= 0`. El argumento llega en `x0` y el resultado sale en `x0`. Comprueba `0`, `1`, `10` y `100` desde un programa en C.',
         code='''    .text
    .globl _sum_to
    .p2align 2
_sum_to:
    mov x1, #0
1:  cmp x0, #1
    b.lt 2f
    add x1, x1, x0
    sub x0, x0, #1
    b 1b
2:  mov x0, x1
    ret''',
         harness='''#include <stdio.h>

long sum_to(long n);

int main(void) {
    if (sum_to(0) != 0 || sum_to(-5) != 0) return 1;
    if (sum_to(1) != 1 || sum_to(10) != 55 || sum_to(100) != 5050) return 2;
    puts("OK");
    return 0;
}''',
         tests=['`sum_to(0)` y los negativos devuelven 0', '`sum_to(1)` es 1', '`sum_to(10)` es 55', '`sum_to(100)` es 5050'],
         why='La función no necesita pila: usa solo `x0` y `x1`, que son registros que quien llama no espera conservados. El bucle suma `n` al acumulador y decrece `n` hasta que deja de ser mayor o igual que 1. `ret` salta a la dirección guardada en `x30`.'),
    dict(ch=7, lang='asm-arm64', level='INTERMEDIATE',
         prompt='Escribe en ensamblador AArch64 la función `unsigned long my_strlen(const char *s)` que cuente bytes hasta el terminador `0`. Comprueba cadenas de longitud 0, 1 y 11 desde C.',
         code='''    .text
    .globl _my_strlen
    .p2align 2
_my_strlen:
    mov x1, x0
1:  ldrb w2, [x1], #1
    cbnz w2, 1b
    sub x0, x1, x0
    sub x0, x0, #1
    ret''',
         harness='''#include <stdio.h>
#include <string.h>

unsigned long my_strlen(const char *s);

int main(void) {
    const char *cases[] = {"", "a", "hola mundo"};
    for (int i = 0; i < 3; i++) {
        if (my_strlen(cases[i]) != strlen(cases[i])) return 1;
    }
    puts("OK");
    return 0;
}''',
         tests=['la cadena vacía mide 0', '`"a"` mide 1', '`"hola mundo"` mide 10', 'coincide con `strlen` de la biblioteca'],
         why='`ldrb w2, [x1], #1` carga un byte y avanza el puntero una posición (direccionamiento posindexado). Al salir, `x1` apunta un byte después del terminador, por eso se resta 1 a la diferencia con el inicio.'),
    dict(ch=7, lang='asm-arm64', level='ADVANCED',
         prompt='Escribe en ensamblador AArch64 `int dot(const int *a, const int *b, long n)` que devuelva el producto escalar de dos arrays de `int` de longitud `n`. Comprueba `{1, 2, 3} . {4, 5, 6} = 32`, un array vacío y valores negativos.',
         code='''    .text
    .globl _dot
    .p2align 2
_dot:
    mov w3, #0
1:  cbz x2, 2f
    ldr w4, [x0], #4
    ldr w5, [x1], #4
    madd w3, w4, w5, w3
    sub x2, x2, #1
    b 1b
2:  mov w0, w3
    ret''',
         harness='''#include <stdio.h>

int dot(const int *a, const int *b, long n);

int main(void) {
    int a[] = {1, 2, 3}, b[] = {4, 5, 6};
    if (dot(a, b, 3) != 32) return 1;
    if (dot(a, b, 0) != 0) return 2;
    int c[] = {-1, 2}, d[] = {3, -4};
    if (dot(c, d, 2) != -11) return 3;
    puts("OK");
    return 0;
}''',
         tests=['`{1, 2, 3}` por `{4, 5, 6}` da 32', 'una longitud 0 da 0', 'los valores negativos se tratan con signo'],
         why='`madd w3, w4, w5, w3` multiplica y acumula en una sola instrucción. Se usan registros `w` de 32 bits porque el tipo es `int`; el contador `n` es un `long` en `x2`. La función no usa la pila ni registros que deba conservar.'),
    # ---- capítulo 8: Fortran científico
    dict(ch=8, lang='fortran', level='FOUNDATIONAL',
         prompt='Escribe en Fortran moderno `pure function interior_sum(u) result(s)` que reciba un vector real `u(:)` y devuelva la suma de los puntos interiores `u(2:n-1)`, usando secciones de arrays. Comprueba `[1, 2, 3, 4]` (suma 5), un vector de tres elementos y uno de dos (suma 0).',
         code='''pure function interior_sum(u) result(s)
    real, intent(in) :: u(:)
    real :: s
    if (size(u) < 3) then
        s = 0.0
    else
        s = sum(u(2:size(u) - 1))
    end if
end function interior_sum''',
         harness='''program main
    implicit none
    interface
        pure function interior_sum(u) result(s)
            real, intent(in) :: u(:)
            real :: s
        end function interior_sum
    end interface
    if (abs(interior_sum([1.0, 2.0, 3.0, 4.0]) - 5.0) > 1e-6) stop 1
    if (abs(interior_sum([1.0, 7.0, 3.0]) - 7.0) > 1e-6) stop 2
    if (interior_sum([1.0, 2.0]) /= 0.0) stop 3
    print '(A)', 'OK'
end program main

{{code}}''',
         tests=['`[1, 2, 3, 4]` suma 5', '`[1, 7, 3]` suma 7', 'un vector de dos elementos suma 0'],
         why='`u(2:size(u)-1)` es una sección de array: se expresa sobre el vector entero, sin bucle ni índices explícitos, y el compilador puede vectorizarlo. `pure` declara que la función no tiene efectos laterales, requisito para usarla en contextos paralelos.'),
    dict(ch=8, lang='fortran', level='INTERMEDIATE',
         prompt='Escribe en Fortran `function laplacian_1d(u) result(d)` que devuelva un vector con la segunda diferencia `u(i-1) - 2 u(i) + u(i+1)` en los puntos interiores y `0` en los extremos. Comprueba que para `u = [0, 1, 4, 9, 16]` (`x**2`) el interior vale 2.',
         code='''function laplacian_1d(u) result(d)
    real, intent(in) :: u(:)
    real :: d(size(u))
    integer :: n
    n = size(u)
    d = 0.0
    if (n >= 3) then
        d(2:n-1) = u(1:n-2) - 2.0 * u(2:n-1) + u(3:n)
    end if
end function laplacian_1d''',
         harness='''program main
    implicit none
    interface
        function laplacian_1d(u) result(d)
            real, intent(in) :: u(:)
            real :: d(size(u))
        end function laplacian_1d
    end interface
    real :: d(5)
    d = laplacian_1d([0.0, 1.0, 4.0, 9.0, 16.0])
    if (any(abs(d(2:4) - 2.0) > 1e-6)) stop 1
    if (d(1) /= 0.0 .or. d(5) /= 0.0) stop 2
    if (any(laplacian_1d([1.0, 2.0]) /= 0.0)) stop 3
    print '(A)', 'OK'
end program main

{{code}}''',
         tests=['para `x**2` el interior vale 2', 'los extremos valen 0', 'un vector de dos elementos devuelve ceros'],
         why='La asignación de una expresión de arrays se evalúa elemento a elemento como si se hiciera a la vez, así que la diferencia finita se escribe sin bucle. La segunda derivada de x al cuadrado es 2, que es lo que se comprueba.'),
    dict(ch=8, lang='fortran', level='ADVANCED',
         prompt='Escribe en Fortran `subroutine matmul2(a, b, c)` que multiplique dos matrices reales con bucles (sin usar `matmul`) y deje el resultado en `c`, comprobando que las dimensiones son compatibles (si no, `c` se rellena de ceros). Comprueba `[[1,2],[3,4]] x [[5,6],[7,8]] = [[19,22],[43,50]]` y que coincide con el intrínseco `matmul` en un caso rectangular.',
         code='''subroutine matmul2(a, b, c)
    real, intent(in) :: a(:, :), b(:, :)
    real, intent(out) :: c(:, :)
    integer :: i, j, k
    c = 0.0
    if (size(a, 2) /= size(b, 1)) return
    if (size(c, 1) /= size(a, 1) .or. size(c, 2) /= size(b, 2)) return
    do j = 1, size(b, 2)
        do k = 1, size(a, 2)
            do i = 1, size(a, 1)
                c(i, j) = c(i, j) + a(i, k) * b(k, j)
            end do
        end do
    end do
end subroutine matmul2''',
         harness='''program main
    implicit none
    interface
        subroutine matmul2(a, b, c)
            real, intent(in) :: a(:, :), b(:, :)
            real, intent(out) :: c(:, :)
        end subroutine matmul2
    end interface
    real :: a(2, 2), b(2, 2), c(2, 2), r(2, 3), s(3, 2), p(2, 2), q(2, 2)
    a = reshape([1.0, 3.0, 2.0, 4.0], [2, 2])
    b = reshape([5.0, 7.0, 6.0, 8.0], [2, 2])
    call matmul2(a, b, c)
    if (any(abs(c - reshape([19.0, 43.0, 22.0, 50.0], [2, 2])) > 1e-5)) stop 1
    r = reshape([1.0, 2.0, 3.0, 4.0, 5.0, 6.0], [2, 3])
    s = reshape([1.0, -1.0, 0.5, 2.0, 3.0, 1.0], [3, 2])
    call matmul2(r, s, p)
    q = matmul(r, s)
    if (any(abs(p - q) > 1e-5)) stop 2
    call matmul2(r, r, p)
    if (any(p /= 0.0)) stop 3
    print '(A)', 'OK'
end program main

{{code}}''',
         tests=['`[[1,2],[3,4]] x [[5,6],[7,8]]` da `[[19,22],[43,50]]`', 'coincide con `matmul` en un caso rectangular', 'dimensiones incompatibles dejan ceros'],
         why='Fortran guarda las matrices por columnas, así que el bucle más interno recorre las filas (`i`) para acceder a memoria contigua. Se comprueba el resultado con el intrínseco `matmul` como oráculo independiente.'),
]
