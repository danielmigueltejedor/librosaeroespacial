"""Programming exercises of volume 2 (algorithms and systems). Each reference program runs with a real compiler or interpreter."""

EXERCISES = [
    # ---- capítulo 1: complejidad
    dict(ch=1, lang='python', level='INTERMEDIATE',
         prompt='Escribe `master_theorem(a, b, d)` para la recurrencia `T(n) = a T(n/b) + Theta(n^d)` (con `a >= 1`, `b > 1`, `d >= 0`) que devuelva `"n^d"`, `"n^d log n"` o `"n^log_b(a)"` según el caso del teorema maestro. Comprueba la ordenación por mezcla (2, 2, 1), la búsqueda binaria (1, 2, 0), Karatsuba (3, 2, 1) y Strassen (7, 2, 2).',
         code='''import math


def master_theorem(a, b, d):
    critical = math.log(a, b)
    if math.isclose(d, critical):
        return f"n^{d:g} log n"
    if d > critical:
        return f"n^{d:g}"
    return f"n^{critical:.3f}"''',
         harness='''assert master_theorem(2, 2, 1) == "n^1 log n"
assert master_theorem(1, 2, 0) == "n^0 log n"
assert master_theorem(3, 2, 1) == "n^1.585"
assert master_theorem(7, 2, 2) == "n^2.807"
assert master_theorem(1, 2, 1) == "n^1"
assert master_theorem(4, 2, 1) == "n^2.000"
assert master_theorem(8, 2, 3) == "n^3 log n"
print("OK")''',
         tests=['ordenación por mezcla da `n log n`', 'búsqueda binaria da `log n`', 'Karatsuba da `n^1.585`', 'Strassen da `n^2.807`', 'el caso en que domina el trabajo de la raíz da `n^d`'],
         why='Se compara el trabajo de combinar, `n^d`, con el número de hojas del árbol de recursión, `n^log_b(a)`: si empatan hay un nivel de cada tamaño y sale un factor logarítmico; si domina uno de los dos, ese determina el resultado. El teorema solo se aplica a subproblemas del mismo tamaño y coste de combinación polinómico.'),
    dict(ch=1, lang='python', level='INTERMEDIATE',
         prompt='Escribe `linear_search_steps(items, key)` y `binary_search_steps(items, key)` que devuelvan el número de comparaciones realizadas. Comprueba que en una lista de `2**k` elementos ordenados, el peor caso lineal es `n` y el binario no pasa de `k + 1`, y que el crecimiento de ambos con `n` coincide con O(n) y O(log n).',
         code='''def linear_search_steps(items, key):
    steps = 0
    for item in items:
        steps += 1
        if item == key:
            break
    return steps


def binary_search_steps(items, key):
    lo, hi, steps = 0, len(items) - 1, 0
    while lo <= hi:
        steps += 1
        mid = lo + (hi - lo) // 2
        if items[mid] == key:
            break
        if items[mid] < key:
            lo = mid + 1
        else:
            hi = mid - 1
    return steps''',
         harness='''for k in range(4, 17):
    n = 2 ** k
    data = list(range(n))
    assert linear_search_steps(data, n - 1) == n
    assert linear_search_steps(data, -5) == n
    worst = max(binary_search_steps(data, key) for key in (0, n - 1, n // 2, n // 3, -1, n + 5))
    assert worst <= k + 1, (k, worst)
assert binary_search_steps(list(range(2 ** 16)), 12345) <= 17
small, large = binary_search_steps(list(range(2 ** 8)), -1), binary_search_steps(list(range(2 ** 16)), -1)
assert large - small == 8
print("OK")''',
         tests=['el peor caso lineal es `n` comparaciones', 'el binario no pasa de `k + 1` comparaciones para `2^k` elementos', 'multiplicar `n` por 256 solo añade 8 comparaciones al binario'],
         why='Medir operaciones, no segundos, da una cifra independiente de la máquina. La búsqueda binaria descarta la mitad en cada paso, así que necesita `log2(n) + 1` comparaciones como mucho: duplicar los datos añade una sola comparación. Calcular el punto medio como `lo + (hi - lo) // 2` evita el desbordamiento en lenguajes con enteros de tamaño fijo.'),
    dict(ch=1, lang='python', level='INTERMEDIATE',
         prompt='Escribe una clase `DynamicArray` que simule un vector dinámico con duplicación de capacidad y cuente cuántos elementos se copian en total al redimensionar (`copies`). Comprueba que tras `n` inserciones `copies < 2 * n`, es decir, que el coste amortizado por inserción es constante.',
         code='''class DynamicArray:
    def __init__(self):
        self.capacity = 1
        self.size = 0
        self.data = [None]
        self.copies = 0

    def append(self, value):
        if self.size == self.capacity:
            self.capacity *= 2
            new = [None] * self.capacity
            for i in range(self.size):
                new[i] = self.data[i]
                self.copies += 1
            self.data = new
        self.data[self.size] = value
        self.size += 1''',
         harness='''for n in (1, 2, 10, 1000, 100_000):
    array = DynamicArray()
    for i in range(n):
        array.append(i)
    assert array.size == n and array.data[:n] == list(range(n))
    assert array.copies < 2 * n, (n, array.copies)
single = DynamicArray()
for i in range(1025):
    single.append(i)
assert single.copies == 2047
print("OK")''',
         tests=['las copias totales son menores que `2n`', 'el contenido se conserva tras los redimensionados', 'con 1025 inserciones se copian 2047 elementos en total'],
         why='Una inserción suelta puede costar O(n) cuando hay que copiar, pero ocurre cada vez menos: las copias forman la serie `1 + 2 + 4 + ... < 2n`. Por eso el coste amortizado por inserción es constante. Crecer una cantidad fija en lugar de duplicar daría coste cuadrático.'),
    # ---- capítulo 2: búsqueda y ordenación
    dict(ch=2, lang='c', level='INTERMEDIATE',
         prompt='Escribe en C `int mid(int lo, int hi)` que calcule el punto medio de dos índices no negativos sin desbordar `int`, y `int binary_search(const int *a, int n, int key)` que devuelva la posición o -1. Comprueba que `(lo + hi) / 2` desbordaría con `lo = hi = INT_MAX - 1` y que `mid` no, y la búsqueda en varios casos.',
         code='''int mid(int lo, int hi) {
    return lo + (hi - lo) / 2;
}

int binary_search(const int *a, int n, int key) {
    int lo = 0, hi = n - 1;
    while (lo <= hi) {
        int m = mid(lo, hi);
        if (a[m] == key) return m;
        if (a[m] < key) lo = m + 1;
        else hi = m - 1;
    }
    return -1;
}''',
         harness='''#include <limits.h>
#include <stdio.h>

int main(void) {
    int big = INT_MAX - 1;
    if (mid(big, big) != big) return 1;
    long naive = ((long)big + big) / 2;
    if (naive != big) return 2;
    if (mid(0, INT_MAX) != INT_MAX / 2) return 3;
    int a[] = {1, 3, 5, 7, 9, 11};
    if (binary_search(a, 6, 7) != 3 || binary_search(a, 6, 1) != 0 || binary_search(a, 6, 11) != 5) return 4;
    if (binary_search(a, 6, 4) != -1 || binary_search(a, 0, 4) != -1 || binary_search(a, 1, 1) != 0) return 5;
    puts("OK");
    return 0;
}''',
         tests=['`mid(INT_MAX - 1, INT_MAX - 1)` no desborda', '`mid(0, INT_MAX)` es `INT_MAX / 2`', 'se encuentran el primero, el último y uno intermedio', 'un elemento ausente o un array vacío devuelve -1'],
         why='La suma `lo + hi` puede superar `INT_MAX` aunque ambos índices sean válidos, y el desbordamiento de enteros con signo es comportamiento indefinido en C. Este error estuvo décadas en bibliotecas estándar. `lo + (hi - lo) / 2` solo resta dos valores no negativos, que nunca desborda.'),
    dict(ch=2, lang='python', level='INTERMEDIATE',
         prompt='Escribe `count_inversions(items)` que devuelva el número de pares `i < j` con `items[i] > items[j]` en tiempo O(n log n) modificando la ordenación por mezcla. Comprueba contra la versión cuadrática en listas aleatorias y los casos ordenado y en orden inverso.',
         code='''def count_inversions(items):
    def sort(xs):
        if len(xs) <= 1:
            return xs, 0
        mid = len(xs) // 2
        left, a = sort(xs[:mid])
        right, b = sort(xs[mid:])
        merged, count, i, j = [], a + b, 0, 0
        while i < len(left) and j < len(right):
            if left[i] <= right[j]:
                merged.append(left[i])
                i += 1
            else:
                merged.append(right[j])
                count += len(left) - i
                j += 1
        merged.extend(left[i:])
        merged.extend(right[j:])
        return merged, count

    return sort(list(items))[1]''',
         harness='''import random

def brute(xs):
    return sum(1 for i in range(len(xs)) for j in range(i + 1, len(xs)) if xs[i] > xs[j])

rng = random.Random(3)
for _ in range(200):
    xs = [rng.randint(0, 20) for _ in range(rng.randint(0, 30))]
    assert count_inversions(xs) == brute(xs), xs
assert count_inversions(list(range(100))) == 0
assert count_inversions(list(range(100, 0, -1))) == 100 * 99 // 2
assert count_inversions([2, 1, 2, 1]) == 3
big = list(range(20000, 0, -1))
assert count_inversions(big) == 20000 * 19999 // 2
print("OK")''',
         tests=['coincide con la versión cuadrática en 200 listas aleatorias', 'una lista ordenada tiene 0 inversiones', 'una lista en orden inverso tiene `n(n-1)/2`', 'procesa 20 000 elementos sin problemas de tiempo'],
         why='Al mezclar dos mitades ordenadas, cada vez que se toma un elemento de la derecha antes que los que quedan en la izquierda se descubren tantas inversiones como elementos restantes tenga la izquierda. Así se cuentan todas sin compararlas por pares, en O(n log n). Se usa `<=` al mezclar para no contar los iguales.'),
    dict(ch=2, lang='python', level='INTERMEDIATE',
         prompt='Escribe `insertion_sort(items, key=None, check=None)` que ordene una copia y, tras cada iteración del bucle externo, llame a `check(prefijo_ordenado, indice)` si se le pasa, de modo que se pueda comprobar el invariante "los primeros `i + 1` elementos están ordenados". Comprueba el invariante en cada paso, la estabilidad con `key`, y que no modifica la entrada.',
         code='''def insertion_sort(items, key=None, check=None):
    key = key or (lambda x: x)
    result = list(items)
    for i in range(1, len(result)):
        current = result[i]
        j = i - 1
        while j >= 0 and key(result[j]) > key(current):
            result[j + 1] = result[j]
            j -= 1
        result[j + 1] = current
        if check:
            check(result[: i + 1], i)
    return result''',
         harness='''import random

seen = []
def invariant(prefix, i):
    assert all(prefix[k] <= prefix[k + 1] for k in range(len(prefix) - 1)), (prefix, i)
    seen.append(i)

rng = random.Random(5)
data = [rng.randint(0, 50) for _ in range(40)]
copy = list(data)
assert insertion_sort(data, check=invariant) == sorted(data)
assert data == copy and seen == list(range(1, 40))
pairs = [(2, "a"), (1, "b"), (2, "c"), (1, "d")]
assert insertion_sort(pairs, key=lambda p: p[0]) == [(1, "b"), (1, "d"), (2, "a"), (2, "c")]
assert insertion_sort([]) == [] and insertion_sort([7]) == [7]
print("OK")''',
         tests=['tras cada iteración el prefijo está ordenado', 'el resultado coincide con `sorted`', 'la entrada no se modifica', 'la ordenación es estable (los iguales conservan su orden)', 'una lista vacía o de un elemento no falla'],
         why='Un invariante de bucle es una propiedad que se cumple antes y después de cada iteración; demostrarlo, junto con la condición de salida, prueba la corrección. Aquí: tras la iteración `i`, los `i + 1` primeros elementos están ordenados. Desplazar solo mientras el anterior sea estrictamente mayor garantiza la estabilidad.'),
    # ---- capítulo 3: dividir y vencer, voraces, programación dinámica
    dict(ch=3, lang='python', level='INTERMEDIATE',
         prompt='Escribe `knapsack(items, capacity)` para la mochila 0/1 con programación dinámica, donde cada objeto es `(peso, valor)`, y que devuelva `(valor_máximo, índices_elegidos)`. Comprueba un caso conocido y contra fuerza bruta en instancias pequeñas aleatorias.',
         code='''def knapsack(items, capacity):
    n = len(items)
    best = [[0] * (capacity + 1) for _ in range(n + 1)]
    for i, (weight, value) in enumerate(items, 1):
        for c in range(capacity + 1):
            best[i][c] = best[i - 1][c]
            if weight <= c:
                best[i][c] = max(best[i][c], best[i - 1][c - weight] + value)
    chosen, c = [], capacity
    for i in range(n, 0, -1):
        if best[i][c] != best[i - 1][c]:
            chosen.append(i - 1)
            c -= items[i - 1][0]
    return best[n][capacity], sorted(chosen)''',
         harness='''from itertools import combinations
import random

value, chosen = knapsack([(1, 1), (3, 4), (4, 5), (5, 7)], 7)
assert value == 9 and chosen == [1, 2]
assert knapsack([], 10) == (0, [])
assert knapsack([(5, 10)], 4) == (0, [])
rng = random.Random(11)
for _ in range(100):
    items = [(rng.randint(1, 6), rng.randint(1, 9)) for _ in range(rng.randint(0, 8))]
    cap = rng.randint(0, 15)
    brute = max((sum(items[i][1] for i in c) for r in range(len(items) + 1) for c in combinations(range(len(items)), r)
                 if sum(items[i][0] for i in c) <= cap), default=0)
    got, picks = knapsack(items, cap)
    assert got == brute and sum(items[i][1] for i in picks) == got and sum(items[i][0] for i in picks) <= cap
print("OK")''',
         tests=['el caso `(1,1), (3,4), (4,5), (5,7)` con capacidad 7 da 9 con los objetos 1 y 2', 'sin objetos el valor es 0', 'un objeto que no cabe no se elige', 'coincide con la fuerza bruta en 100 instancias aleatorias'],
         why='`best[i][c]` es el mejor valor con los `i` primeros objetos y capacidad `c`: o no se toma el objeto, o se toma y se usa la solución del subproblema con menos capacidad. Recorrer la tabla hacia atrás reconstruye qué objetos se eligieron. El coste es O(n·C), pseudo-polinómico: sigue siendo NP-completo en general.'),
    dict(ch=3, lang='python', level='INTERMEDIATE',
         prompt='Escribe `lcs(a, b)` que devuelva la subsecuencia común más larga de dos cadenas con programación dinámica y reconstrucción de la solución. Comprueba `"ABCBDAB"` y `"BDCABA"` (longitud 4), cadenas sin elementos comunes y la cadena vacía.',
         code='''def lcs(a, b):
    table = [[0] * (len(b) + 1) for _ in range(len(a) + 1)]
    for i in range(len(a) - 1, -1, -1):
        for j in range(len(b) - 1, -1, -1):
            if a[i] == b[j]:
                table[i][j] = 1 + table[i + 1][j + 1]
            else:
                table[i][j] = max(table[i + 1][j], table[i][j + 1])
    result, i, j = [], 0, 0
    while i < len(a) and j < len(b):
        if a[i] == b[j]:
            result.append(a[i])
            i += 1
            j += 1
        elif table[i + 1][j] >= table[i][j + 1]:
            i += 1
        else:
            j += 1
    return "".join(result)''',
         harness='''def is_subsequence(s, t):
    it = iter(t)
    return all(ch in it for ch in s)

x = lcs("ABCBDAB", "BDCABA")
assert len(x) == 4 and is_subsequence(x, "ABCBDAB") and is_subsequence(x, "BDCABA")
assert lcs("abc", "xyz") == "" and lcs("", "abc") == "" and lcs("abc", "") == ""
assert lcs("abc", "abc") == "abc"
assert lcs("AGGTAB", "GXTXAYB") == "GTAB"
print("OK")''',
         tests=['`"ABCBDAB"` y `"BDCABA"` tienen una subsecuencia común de longitud 4', 'sin elementos comunes devuelve la cadena vacía', 'dos cadenas iguales devuelven la cadena completa', '`"AGGTAB"` y `"GXTXAYB"` dan `"GTAB"`'],
         why='La tabla guarda la longitud de la mejor subsecuencia de cada par de sufijos; si los primeros caracteres coinciden se avanza en ambas, y si no, se descarta uno de los dos. Hay varias subsecuencias de la misma longitud, por eso la prueba comprueba la longitud y que sea subsecuencia de ambas.'),
    dict(ch=3, lang='python', level='INTERMEDIATE',
         prompt='Escribe `max_intervals(intervals)` que, con el algoritmo voraz de elegir siempre el intervalo que termina antes, devuelva el máximo conjunto de intervalos `(inicio, fin)` sin solapes (un intervalo que empieza donde otro termina no se solapa). Comprueba contra fuerza bruta en casos pequeños aleatorios.',
         code='''def max_intervals(intervals):
    chosen, last_end = [], float("-inf")
    for start, end in sorted(intervals, key=lambda iv: (iv[1], iv[0])):
        if start >= last_end:
            chosen.append((start, end))
            last_end = end
    return chosen''',
         harness='''from itertools import combinations
import random

assert max_intervals([(1, 3), (2, 5), (4, 6), (6, 8)]) == [(1, 3), (4, 6), (6, 8)]
assert max_intervals([]) == []
def compatible(ivs):
    ivs = sorted(ivs)
    return all(ivs[i][1] <= ivs[i + 1][0] for i in range(len(ivs) - 1))
rng = random.Random(8)
for _ in range(150):
    ivs = []
    for _ in range(rng.randint(0, 9)):
        s = rng.randint(0, 20)
        ivs.append((s, s + rng.randint(1, 6)))
    best = max((len(c) for r in range(len(ivs) + 1) for c in combinations(ivs, r) if compatible(c)), default=0)
    got = max_intervals(ivs)
    assert len(got) == best and compatible(got)
print("OK")''',
         tests=['`(1,3), (2,5), (4,6), (6,8)` da 3 intervalos', 'sin intervalos devuelve vacío', 'coincide en tamaño con la fuerza bruta en 150 casos', 'el resultado no tiene solapes'],
         why='Elegir el intervalo que termina antes deja el máximo espacio para los siguientes: es una elección voraz que se demuestra óptima por intercambio (cualquier solución puede cambiar su primer intervalo por ese sin perder tamaño). Ordenar por inicio, en cambio, no es correcto.'),
    dict(ch=3, lang='python', level='INTERMEDIATE',
         prompt='Escribe `count_queens(n)` que cuente las soluciones del problema de las `n` reinas con vuelta atrás, podando las ramas con conflictos. Comprueba los valores conocidos de 1 a 8 reinas (1, 0, 0, 2, 10, 4, 40, 92).',
         code='''def count_queens(n):
    def place(row, cols, diag1, diag2):
        if row == n:
            return 1
        total = 0
        for col in range(n):
            if col in cols or row + col in diag1 or row - col in diag2:
                continue
            total += place(row + 1, cols | {col}, diag1 | {row + col}, diag2 | {row - col})
        return total

    return place(0, frozenset(), frozenset(), frozenset())''',
         harness='''assert [count_queens(n) for n in range(1, 9)] == [1, 0, 0, 2, 10, 4, 40, 92]
assert count_queens(0) == 1
print("OK")''',
         tests=['de 1 a 8 reinas hay `1, 0, 0, 2, 10, 4, 40, 92` soluciones', '0 reinas tienen una solución trivial'],
         why='La vuelta atrás construye la solución fila a fila y abandona una rama en cuanto aparece un conflicto, en lugar de generar las `n^n` colocaciones. Las columnas y las dos diagonales ocupadas se guardan en conjuntos para comprobar los conflictos en tiempo constante.'),
    # ---- capítulo 4: grafos
    dict(ch=4, lang='python', level='FOUNDATIONAL',
         prompt='Escribe `shortest_path(graph, start, goal)` con una búsqueda en anchura sobre un grafo no ponderado (diccionario de nodo a lista de vecinos) que devuelva el camino más corto como lista de nodos o `None` si no hay camino. Comprueba un grafo con dos caminos, un nodo aislado y el caso inicio igual a destino.',
         code='''from collections import deque


def shortest_path(graph, start, goal):
    parent = {start: None}
    queue = deque([start])
    while queue:
        node = queue.popleft()
        if node == goal:
            path = []
            while node is not None:
                path.append(node)
                node = parent[node]
            return path[::-1]
        for neighbour in graph.get(node, []):
            if neighbour not in parent:
                parent[neighbour] = node
                queue.append(neighbour)
    return None''',
         harness='''graph = {"a": ["b", "c"], "b": ["d"], "c": ["d", "e"], "d": ["f"], "e": ["f"], "f": [], "z": []}
assert shortest_path(graph, "a", "f") in (["a", "b", "d", "f"], ["a", "c", "d", "f"], ["a", "c", "e", "f"])
assert len(shortest_path(graph, "a", "f")) == 4
assert shortest_path(graph, "a", "a") == ["a"]
assert shortest_path(graph, "a", "z") is None
assert shortest_path(graph, "f", "a") is None
print("OK")''',
         tests=['el camino de `a` a `f` tiene 4 nodos', 'el camino de un nodo a sí mismo es él mismo', 'un nodo inalcanzable devuelve `None`', 'no se recorre un grafo dirigido al revés'],
         why='La búsqueda en anchura visita los nodos por distancia creciente, así que la primera vez que alcanza el destino lo hace por un camino con el menor número de aristas. El diccionario de padres sirve a la vez de conjunto de visitados y para reconstruir el camino.'),
    dict(ch=4, lang='python', level='INTERMEDIATE',
         prompt='Escribe `dijkstra(graph, source)` con una cola de prioridad (`heapq`) sobre un grafo ponderado (nodo a lista de `(vecino, peso)`) y que devuelva las distancias mínimas desde el origen (los inalcanzables no aparecen). Comprueba contra Bellman-Ford en grafos aleatorios y un caso con un camino indirecto más corto.',
         code='''import heapq


def dijkstra(graph, source):
    dist = {source: 0}
    heap = [(0, source)]
    while heap:
        d, node = heapq.heappop(heap)
        if d > dist.get(node, float("inf")):
            continue
        for neighbour, weight in graph.get(node, []):
            candidate = d + weight
            if candidate < dist.get(neighbour, float("inf")):
                dist[neighbour] = candidate
                heapq.heappush(heap, (candidate, neighbour))
    return dist''',
         harness='''import random

graph = {"a": [("b", 10), ("c", 3)], "c": [("b", 4), ("d", 8)], "b": [("d", 2)], "d": [], "x": [("a", 1)]}
assert dijkstra(graph, "a") == {"a": 0, "c": 3, "b": 7, "d": 9}

def bellman_ford(graph, source):
    dist = {source: 0}
    for _ in range(len(graph) + 1):
        for u, edges in graph.items():
            for v, w in edges:
                if u in dist and dist[u] + w < dist.get(v, float("inf")):
                    dist[v] = dist[u] + w
    return dist

rng = random.Random(2)
for _ in range(100):
    n = rng.randint(2, 9)
    g = {i: [(rng.randrange(n), rng.randint(1, 9)) for _ in range(rng.randint(0, 3))] for i in range(n)}
    assert dijkstra(g, 0) == bellman_ford(g, 0), g
print("OK")''',
         tests=['el camino indirecto `a, c, b` (7) gana al directo (10)', 'los nodos inalcanzables no aparecen', 'coincide con Bellman-Ford en 100 grafos aleatorios'],
         why='Dijkstra extrae siempre el nodo con menor distancia provisional; con pesos no negativos, esa distancia ya es definitiva. Las entradas obsoletas del montículo se ignoran con `d > dist[node]` en lugar de borrarlas. Con pesos negativos el algoritmo deja de ser correcto y hace falta Bellman-Ford.'),
    dict(ch=4, lang='python', level='INTERMEDIATE',
         prompt='Escribe `kruskal(n, edges)` que calcule un árbol de expansión mínimo con la estructura unión-búsqueda (con compresión de caminos), donde `edges` son tuplas `(peso, u, v)` sobre los nodos `0..n-1`. Devuelve `(peso_total, aristas)` o `None` si el grafo no es conexo. Comprueba un caso conocido, uno desconexo y el peso contra Prim.',
         code='''def kruskal(n, edges):
    parent = list(range(n))

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    total, chosen = 0, []
    for weight, u, v in sorted(edges):
        ru, rv = find(u), find(v)
        if ru != rv:
            parent[ru] = rv
            total += weight
            chosen.append((weight, u, v))
    return (total, chosen) if len(chosen) == n - 1 else None''',
         harness='''import heapq
import random

edges = [(7, 0, 1), (5, 0, 3), (8, 1, 2), (9, 1, 3), (7, 1, 4), (5, 2, 4), (15, 3, 4), (6, 3, 5), (8, 4, 5), (9, 4, 6), (11, 5, 6)]
total, chosen = kruskal(7, edges)
assert total == 39 and len(chosen) == 6
assert kruskal(4, [(1, 0, 1), (2, 2, 3)]) is None
assert kruskal(1, []) == (0, [])

def prim(n, edges):
    adj = {i: [] for i in range(n)}
    for w, u, v in edges:
        adj[u].append((w, v)); adj[v].append((w, u))
    seen, heap, total = set(), [(0, 0)], 0
    while heap:
        w, u = heapq.heappop(heap)
        if u in seen:
            continue
        seen.add(u); total += w
        for item in adj[u]:
            heapq.heappush(heap, item)
    return total if len(seen) == n else None

rng = random.Random(9)
for _ in range(100):
    n = rng.randint(2, 8)
    es = [(rng.randint(1, 9), rng.randrange(n), rng.randrange(n)) for _ in range(rng.randint(1, 16))]
    k, p = kruskal(n, es), prim(n, es)
    assert (k[0] if k else None) == p
print("OK")''',
         tests=['el caso clásico de 7 nodos da peso 39 con 6 aristas', 'un grafo no conexo devuelve `None`', 'un único nodo da peso 0', 'el peso coincide con Prim en 100 grafos aleatorios'],
         why='Kruskal ordena las aristas y añade cada una si no cierra un ciclo, lo que se comprueba con unión-búsqueda en tiempo casi constante. Es correcto porque la arista más barata que cruza un corte pertenece a algún árbol mínimo. Un grafo conexo con `n` nodos produce exactamente `n - 1` aristas.'),
    dict(ch=4, lang='python', level='INTERMEDIATE',
         prompt='Escribe `topological_order(graph)` que devuelva un orden topológico de un grafo dirigido acíclico (algoritmo de Kahn) o lance `ValueError` si hay un ciclo. Comprueba que cada arista respeta el orden en grafos aleatorios acíclicos y que un ciclo se detecta.',
         code='''from collections import deque


def topological_order(graph):
    indegree = {node: 0 for node in graph}
    for node, targets in graph.items():
        for t in targets:
            indegree[t] = indegree.get(t, 0) + 1
    queue = deque(sorted(n for n, d in indegree.items() if d == 0))
    order = []
    while queue:
        node = queue.popleft()
        order.append(node)
        for t in graph.get(node, []):
            indegree[t] -= 1
            if indegree[t] == 0:
                queue.append(t)
    if len(order) != len(indegree):
        raise ValueError("el grafo tiene un ciclo")
    return order''',
         harness='''import random

order = topological_order({"shirt": ["tie", "belt"], "tie": ["jacket"], "pants": ["belt", "shoes"], "belt": ["jacket"], "shoes": [], "jacket": [], "socks": ["shoes"]})
position = {n: i for i, n in enumerate(order)}
for u, vs in {"shirt": ["tie", "belt"], "tie": ["jacket"], "pants": ["belt", "shoes"], "belt": ["jacket"], "socks": ["shoes"]}.items():
    assert all(position[u] < position[v] for v in vs)
rng = random.Random(4)
for _ in range(100):
    n = rng.randint(1, 10)
    g = {i: [j for j in range(i + 1, n) if rng.random() < 0.3] for i in range(n)}
    order = topological_order(g)
    pos = {x: i for i, x in enumerate(order)}
    assert sorted(order) == list(range(n))
    assert all(pos[u] < pos[v] for u, vs in g.items() for v in vs)
try:
    topological_order({"a": ["b"], "b": ["c"], "c": ["a"]})
except ValueError:
    print("OK")''',
         tests=['en el ejemplo de la ropa cada prenda va antes de las que dependen de ella', 'en 100 grafos aleatorios acíclicos todas las aristas respetan el orden', 'un ciclo lanza `ValueError`'],
         why='El algoritmo de Kahn retira repetidamente los nodos sin dependencias pendientes. Si al final quedan nodos sin retirar, todos están en un ciclo o dependen de uno, y no existe orden posible. Es la base de gestores de dependencias y sistemas de construcción.'),
    # ---- capítulo 5: estructuras persistentes y probabilísticas
    dict(ch=5, lang='python', level='INTERMEDIATE',
         prompt='Implementa una pila persistente `PStack` inmutable con `push(x)` y `pop()` que devuelvan pilas nuevas compartiendo estructura con la anterior (lista enlazada). Comprueba que las versiones anteriores siguen intactas, que `push` es O(1) (el nodo anterior es el mismo objeto) y que `pop` de una pila vacía lanza `IndexError`.',
         code='''class PStack:
    __slots__ = ("head", "tail", "size")

    def __init__(self, head=None, tail=None, size=0):
        self.head, self.tail, self.size = head, tail, size

    def push(self, value):
        return PStack(value, self, self.size + 1)

    def pop(self):
        if self.size == 0:
            raise IndexError("pila vacia")
        return self.head, self.tail

    def to_list(self):
        out, node = [], self
        while node.size:
            out.append(node.head)
            node = node.tail
        return out''',
         harness='''empty = PStack()
s1 = empty.push(1)
s2 = s1.push(2)
s3 = s1.push(3)
assert s2.to_list() == [2, 1] and s3.to_list() == [3, 1] and s1.to_list() == [1]
assert s2.tail is s1 and s3.tail is s1
top, rest = s2.pop()
assert top == 2 and rest is s1
assert empty.to_list() == [] and empty.size == 0
try:
    empty.pop()
except IndexError:
    print("OK")''',
         tests=['`s2` y `s3` parten de `s1` sin modificarlo', 'la versión anterior comparte el mismo nodo (`s2.tail is s1`)', '`pop` devuelve el elemento y la pila restante', '`pop` en una pila vacía lanza `IndexError`'],
         why='En una estructura persistente cada operación devuelve una versión nueva y las anteriores siguen siendo válidas. Compartir los nodos comunes hace que insertar cueste lo mismo que en la versión mutable y que las versiones coexistan sin copiar nada. Es la base de los árboles de Clojure y de Git.'),
    dict(ch=5, lang='python', level='ADVANCED',
         prompt='Implementa un filtro de Bloom `Bloom(bits, hashes)` con `add` y `__contains__` (derivando las posiciones de `hashlib.sha256` con una sal por función). Comprueba que no tiene falsos negativos, mide su tasa de falsos positivos con 1000 elementos en 10 000 bits y 5 funciones y compárala con la teoría `(1 - e^{-kn/m})^k`.',
         code='''import hashlib


class Bloom:
    def __init__(self, bits, hashes):
        self.bits = bits
        self.hashes = hashes
        self.array = bytearray(bits)

    def _positions(self, item):
        for i in range(self.hashes):
            digest = hashlib.sha256(f"{i}:{item}".encode()).digest()
            yield int.from_bytes(digest[:8], "big") % self.bits

    def add(self, item):
        for position in self._positions(item):
            self.array[position] = 1

    def __contains__(self, item):
        return all(self.array[position] for position in self._positions(item))''',
         harness='''import math

bloom = Bloom(10_000, 5)
members = [f"socio{i}" for i in range(1000)]
for m in members:
    bloom.add(m)
assert all(m in bloom for m in members)
outsiders = [f"extra{i}" for i in range(20_000)]
rate = sum(1 for x in outsiders if x in bloom) / len(outsiders)
theory = (1 - math.exp(-5 * 1000 / 10_000)) ** 5
assert abs(rate - theory) < 0.01, (rate, theory)
assert 0.005 < rate < 0.05
assert "algo" not in Bloom(100, 3)
print("OK")''',
         tests=['no hay falsos negativos', 'la tasa de falsos positivos coincide con la teórica dentro de un punto porcentual', 'un filtro vacío no contiene nada'],
         why='Un filtro de Bloom responde "seguro que no" o "probablemente sí" con muy poca memoria. Nunca olvida un elemento añadido, pero puede equivocarse al decir que sí. La tasa de error depende de los bits por elemento y del número de funciones, y no se puede eliminar un elemento sin una variante con contadores.'),
    dict(ch=5, lang='python', level='ADVANCED',
         prompt='Implementa un `CountMin(width, depth)` (sketch de recuento mínimo) con `add(item, count=1)` y `estimate(item)`. Comprueba que nunca subestima (la estimación es mayor o igual que el recuento real) y que con un flujo sesgado los elementos frecuentes se estiman con poco error.',
         code='''import hashlib


class CountMin:
    def __init__(self, width, depth):
        self.width, self.depth = width, depth
        self.table = [[0] * width for _ in range(depth)]

    def _cells(self, item):
        for row in range(self.depth):
            digest = hashlib.blake2b(f"{row}:{item}".encode(), digest_size=8).digest()
            yield row, int.from_bytes(digest, "big") % self.width

    def add(self, item, count=1):
        for row, col in self._cells(item):
            self.table[row][col] += count

    def estimate(self, item):
        return min(self.table[row][col] for row, col in self._cells(item))''',
         harness='''import random
from collections import Counter

rng = random.Random(6)
stream = [f"x{min(int(rng.paretovariate(1.2)), 500)}" for _ in range(20_000)]
truth = Counter(stream)
cm = CountMin(width=500, depth=5)
for item in stream:
    cm.add(item)
assert all(cm.estimate(k) >= v for k, v in truth.items())
top = [k for k, _ in truth.most_common(5)]
for k in top:
    assert cm.estimate(k) - truth[k] <= 0.02 * len(stream), (k, cm.estimate(k), truth[k])
assert CountMin(10, 2).estimate("nunca") == 0
print("OK")''',
         tests=['la estimación nunca es menor que el recuento real', 'los cinco elementos más frecuentes se estiman con un error menor del 2 % del flujo', 'un elemento no visto en un sketch vacío se estima en 0'],
         why='Cada elemento incrementa una celda por fila y la estimación toma el mínimo entre filas: las colisiones solo suman, así que el mínimo es la menos contaminada y nunca queda por debajo del recuento real. Ocupa una cantidad fija de memoria sin importar cuántos elementos distintos haya.'),
    # ---- capítulo 6: memoria, cachés, ABI
    dict(ch=6, lang='c', level='INTERMEDIATE',
         prompt='En C, define dos estructuras con los mismos campos (`char a; double b; char c; int d;`) en dos órdenes distintos, una desordenada y otra ordenada de mayor a menor alineamiento. Comprueba con `sizeof` y `offsetof` que la segunda ocupa menos y que cada campo está alineado a su tamaño. Escribe `size_t align_up(size_t value, size_t align)`.',
         code='''#include <stddef.h>

struct Unordered {
    char a;
    double b;
    char c;
    int d;
};

struct Ordered {
    double b;
    int d;
    char a;
    char c;
};

size_t align_up(size_t value, size_t align) {
    return (value + align - 1) & ~(align - 1);
}''',
         harness='''#include <stdio.h>

int main(void) {
    if (sizeof(struct Unordered) != 24) return 1;
    if (sizeof(struct Ordered) != 16) return 2;
    if (offsetof(struct Unordered, b) % _Alignof(double) != 0) return 3;
    if (offsetof(struct Unordered, d) % _Alignof(int) != 0) return 4;
    if (offsetof(struct Ordered, d) != 8 || offsetof(struct Ordered, a) != 12) return 5;
    if (align_up(13, 8) != 16 || align_up(16, 8) != 16 || align_up(0, 64) != 0 || align_up(1, 64) != 64) return 6;
    puts("OK");
    return 0;
}''',
         tests=['la estructura desordenada ocupa 24 bytes', 'la ordenada ocupa 16', 'cada campo está alineado a su tamaño', '`align_up(13, 8)` es 16 y `align_up(16, 8)` es 16'],
         why='Cada campo debe empezar en una dirección múltiplo de su alineamiento, y el compilador rellena con huecos. Ordenar los campos de mayor a menor alineamiento elimina casi todo el relleno: aquí, de 24 a 16 bytes. `align_up` solo funciona con alineamientos que sean potencia de dos.'),
    dict(ch=6, lang='python', level='INTERMEDIATE',
         prompt='Escribe `traversal_misses(rows, cols, order, line_size, lines)` que simule una caché de correspondencia directa y cuente los fallos al recorrer una matriz de enteros de 8 bytes guardada por filas, en orden de filas (`"row"`) o de columnas (`"col"`). Comprueba que el recorrido por columnas produce muchos más fallos.',
         code='''def traversal_misses(rows, cols, order, line_size, lines):
    tags = [None] * lines
    misses = 0
    indices = ((r, c) for r in range(rows) for c in range(cols)) if order == "row" else ((r, c) for c in range(cols) for r in range(rows))
    for r, c in indices:
        address = (r * cols + c) * 8
        block = address // line_size
        index = block % lines
        if tags[index] != block:
            misses += 1
            tags[index] = block
    return misses''',
         harness='''by_rows = traversal_misses(64, 64, "row", line_size=64, lines=32)
by_cols = traversal_misses(64, 64, "col", line_size=64, lines=32)
assert by_rows == 64 * 64 * 8 // 64
assert by_cols > 7 * by_rows
assert traversal_misses(1, 1, "row", 64, 4) == 1
print("OK")''',
         tests=['el recorrido por filas falla una vez por cada línea de 64 bytes (512 fallos)', 'el recorrido por columnas falla muchas más veces', 'una matriz de un elemento falla una vez'],
         why='Una matriz guardada por filas tiene contiguos los elementos de la misma fila. Recorrerla por filas aprovecha cada línea de caché entera (ocho enteros de 8 bytes); por columnas, cada acceso salta una fila entera y las líneas se desalojan antes de reutilizarse. El orden del recorrido puede cambiar el tiempo de un bucle varias veces sin tocar el algoritmo.'),
    dict(ch=6, lang='rust', level='INTERMEDIATE',
         prompt='En Rust, declara `#[repr(C)] struct Header { tag: u8, length: u32, flags: u16 }` y escribe `fn layout() -> (usize, usize, [usize; 3])` que devuelva su tamaño, su alineamiento y los desplazamientos de los tres campos (con `std::mem::offset_of!`). Comprueba los valores y que es compatible con la ABI de C comparando con una estructura equivalente declarada en C mediante `extern "C"`.',
         code='''use std::mem::{align_of, offset_of, size_of};

#[repr(C)]
struct Header {
    tag: u8,
    length: u32,
    flags: u16,
}

fn layout() -> (usize, usize, [usize; 3]) {
    (
        size_of::<Header>(),
        align_of::<Header>(),
        [offset_of!(Header, tag), offset_of!(Header, length), offset_of!(Header, flags)],
    )
}''',
         harness='''fn main() {
    let (size, align, offsets) = layout();
    assert_eq!(align, 4);
    assert_eq!(offsets, [0, 4, 8]);
    assert_eq!(size, 12);
    #[repr(C)]
    struct Packed {
        length: u32,
        flags: u16,
        tag: u8,
    }
    assert_eq!(size_of::<Packed>(), 8);
    println!("OK");
}''',
         tests=['el alineamiento es 4', 'los campos están en los desplazamientos 0, 4 y 8', 'el tamaño es 12', 'reordenar los campos reduce el tamaño a 8'],
         why='`repr(C)` fija el orden de los campos como en C para poder compartir la estructura con otro lenguaje: el relleno se inserta como en un compilador de C. Sin él, Rust puede reordenar los campos para ahorrar espacio. El tamaño es múltiplo del alineamiento mayor para que los arrays de la estructura sigan alineados.'),
    # ---- capítulo 7: compiladores
    dict(ch=7, lang='python', level='INTERMEDIATE',
         prompt='Escribe `tokenize(text)` que convierta una expresión aritmética en una lista de tokens `(tipo, valor)` con los tipos `"NUM"`, `"IDENT"`, `"OP"` (`+ - * / ^`), `"LPAREN"` y `"RPAREN"`, ignorando los espacios y aceptando decimales. Lanza `SyntaxError` ante un carácter inesperado. Comprueba una expresión y los errores.',
         code='''import re

TOKEN_SPEC = [
    ("NUM", r"\\d+(?:\\.\\d+)?"),
    ("IDENT", r"[A-Za-z_]\\w*"),
    ("OP", r"[-+*/^]"),
    ("LPAREN", r"\\("),
    ("RPAREN", r"\\)"),
    ("SKIP", r"\\s+"),
    ("BAD", r"."),
]
PATTERN = re.compile("|".join(f"(?P<{name}>{regex})" for name, regex in TOKEN_SPEC))


def tokenize(text):
    tokens = []
    for match in PATTERN.finditer(text):
        kind, value = match.lastgroup, match.group()
        if kind == "SKIP":
            continue
        if kind == "BAD":
            raise SyntaxError(f"caracter inesperado {value!r} en la posicion {match.start()}")
        tokens.append((kind, float(value) if kind == "NUM" and "." in value else int(value) if kind == "NUM" else value))
    return tokens''',
         harness='''assert tokenize("3 + 4.5*(x - 2)") == [("NUM", 3), ("OP", "+"), ("NUM", 4.5), ("OP", "*"), ("LPAREN", "("), ("IDENT", "x"), ("OP", "-"), ("NUM", 2), ("RPAREN", ")")]
assert tokenize("") == []
assert tokenize("  a_1 ^2 ") == [("IDENT", "a_1"), ("OP", "^"), ("NUM", 2)]
for bad in ("3 $ 4", "a # b"):
    try:
        tokenize(bad)
    except SyntaxError:
        continue
    raise AssertionError(bad)
print("OK")''',
         tests=['`3 + 4.5*(x - 2)` produce 9 tokens', 'una cadena vacía produce una lista vacía', 'los espacios se ignoran y los identificadores admiten guion bajo y dígitos', 'un carácter inesperado lanza `SyntaxError` con su posición'],
         why='El analizador léxico agrupa los caracteres en unidades con significado. Una expresión regular con alternativas con nombre prueba las posibilidades en orden y `lastgroup` dice cuál coincidió; la alternativa final `BAD` captura cualquier carácter para dar un error claro en lugar de omitirlo en silencio.'),
    dict(ch=7, lang='python', level='ADVANCED',
         prompt='Escribe `parse(tokens)` con un analizador sintáctico de descenso recursivo que construya el árbol sintáctico de una expresión con `+ -` (asociativos por la izquierda), `* /` (también) y `^` (asociativo por la derecha), paréntesis y negación unaria. El árbol usa tuplas `("num", n)`, `("bin", op, izq, der)` y `("neg", e)`. Escribe `evaluate(tree)`. Comprueba precedencias y asociatividad.',
         code='''def parse(tokens):
    pos = 0

    def peek():
        return tokens[pos] if pos < len(tokens) else (None, None)

    def take():
        nonlocal pos
        pos += 1
        return tokens[pos - 1]

    def expr():
        node = term()
        while peek() in (("OP", "+"), ("OP", "-")):
            node = ("bin", take()[1], node, term())
        return node

    def term():
        node = unary()
        while peek() in (("OP", "*"), ("OP", "/")):
            node = ("bin", take()[1], node, unary())
        return node

    def unary():
        if peek() == ("OP", "-"):
            take()
            return ("neg", unary())
        return power()

    def power():
        base = atom()
        if peek() == ("OP", "^"):
            take()
            return ("bin", "^", base, unary())
        return base

    def atom():
        kind, value = peek()
        if kind == "NUM":
            take()
            return ("num", value)
        if kind == "LPAREN":
            take()
            node = expr()
            if peek()[0] != "RPAREN":
                raise SyntaxError("falta )")
            take()
            return node
        raise SyntaxError(f"token inesperado {value!r}")

    tree = expr()
    if pos != len(tokens):
        raise SyntaxError("sobran tokens")
    return tree


def evaluate(tree):
    kind = tree[0]
    if kind == "num":
        return tree[1]
    if kind == "neg":
        return -evaluate(tree[1])
    _, op, left, right = tree
    a, b = evaluate(left), evaluate(right)
    return {"+": a + b, "-": a - b, "*": a * b, "/": a / b, "^": a ** b}[op]''',
         harness='''import re

def toks(text):
    out = []
    for m in re.finditer(r"\\d+|[-+*/^()]", text):
        s = m.group()
        out.append(("NUM", int(s)) if s.isdigit() else ("LPAREN", s) if s == "(" else ("RPAREN", s) if s == ")" else ("OP", s))
    return out

def calc(text):
    return evaluate(parse(toks(text)))

assert calc("2 + 3 * 4") == 14
assert calc("(2 + 3) * 4") == 20
assert calc("10 - 4 - 3") == 3
assert calc("100 / 5 / 4") == 5
assert calc("2 ^ 3 ^ 2") == 512
assert calc("-2 ^ 2") == -4
assert calc("2 * -3") == -6
assert parse(toks("1 + 2 * 3")) == ("bin", "+", ("num", 1), ("bin", "*", ("num", 2), ("num", 3)))
for bad in ("1 +", "(1", "1 2", ")"):
    try:
        calc(bad)
    except SyntaxError:
        continue
    raise AssertionError(bad)
print("OK")''',
         tests=['`2 + 3 * 4` es 14', 'la resta y la división se asocian por la izquierda', '`2 ^ 3 ^ 2` es 512 (potencia asociativa por la derecha)', '`-2 ^ 2` es -4', 'las expresiones incompletas lanzan `SyntaxError`'],
         why='Cada nivel de precedencia es una función que llama al siguiente nivel, de menor a mayor precedencia. Los operadores asociativos por la izquierda se resuelven con un bucle; la potencia, con una llamada recursiva a la derecha. Esa estructura es la gramática escrita en código.'),
    dict(ch=7, lang='python', level='INTERMEDIATE',
         prompt='Escribe `fold_constants(tree)` que simplifique un árbol de expresión (`("num", n)`, `("var", nombre)`, `("bin", op, izq, der)`) evaluando los subárboles que solo contienen números y aplicando las identidades `x + 0`, `x * 1`, `x * 0` y `x - x` cuando proceda. Comprueba que no cambia el valor con variables sustituidas.',
         code='''def fold_constants(tree):
    if tree[0] != "bin":
        return tree
    _, op, left, right = tree
    left, right = fold_constants(left), fold_constants(right)
    if left[0] == "num" and right[0] == "num":
        a, b = left[1], right[1]
        return ("num", {"+": a + b, "-": a - b, "*": a * b}[op])
    if op == "+" and right == ("num", 0):
        return left
    if op == "+" and left == ("num", 0):
        return right
    if op == "*" and (right == ("num", 1)):
        return left
    if op == "*" and (left == ("num", 1)):
        return right
    if op == "*" and (left == ("num", 0) or right == ("num", 0)):
        return ("num", 0)
    if op == "-" and left == right:
        return ("num", 0)
    return ("bin", op, left, right)''',
         harness='''import random

def value(tree, env):
    if tree[0] == "num":
        return tree[1]
    if tree[0] == "var":
        return env[tree[1]]
    _, op, l, r = tree
    a, b = value(l, env), value(r, env)
    return {"+": a + b, "-": a - b, "*": a * b}[op]

x = ("var", "x")
assert fold_constants(("bin", "+", ("bin", "*", ("num", 2), ("num", 3)), ("num", 4))) == ("num", 10)
assert fold_constants(("bin", "+", x, ("num", 0))) == x
assert fold_constants(("bin", "*", ("num", 1), x)) == x
assert fold_constants(("bin", "*", x, ("bin", "-", ("num", 2), ("num", 2)))) == ("num", 0)
assert fold_constants(("bin", "-", x, x)) == ("num", 0)
rng = random.Random(1)
def gen(depth):
    if depth == 0 or rng.random() < 0.3:
        return ("num", rng.randint(0, 3)) if rng.random() < 0.6 else ("var", rng.choice("xy"))
    return ("bin", rng.choice("+-*"), gen(depth - 1), gen(depth - 1))
for _ in range(300):
    t = gen(4)
    env = {"x": rng.randint(-5, 5), "y": rng.randint(-5, 5)}
    assert value(fold_constants(t), env) == value(t, env), t
print("OK")''',
         tests=['`2 * 3 + 4` se pliega a 10', '`x + 0` y `1 * x` se simplifican a `x`', '`x * (2 - 2)` da 0', '`x - x` da 0', 'el valor no cambia en 300 expresiones aleatorias'],
         why='Evaluar en compilación lo que ya se conoce ahorra trabajo en ejecución. La prueba esencial para cualquier optimización es que conserve el significado: aquí se comprueba comparando el valor del árbol original y del optimizado con muchas sustituciones aleatorias.'),
    # ---- capítulo 8: sistemas operativos
    dict(ch=8, lang='python', level='INTERMEDIATE',
         prompt='Escribe `round_robin(processes, quantum)` que simule un planificador de turnos rotatorios. Cada proceso es `(nombre, llegada, ráfaga)`. Devuelve un diccionario nombre a `(finalización, tiempo_de_retorno, espera)`. Comprueba un ejemplo de tres procesos con quantum 2 y que un quantum muy grande equivale a FIFO.',
         code='''from collections import deque


def round_robin(processes, quantum):
    pending = sorted(processes, key=lambda p: (p[1], p[0]))
    remaining = {name: burst for name, _, burst in processes}
    arrival = {name: arr for name, arr, _ in processes}
    queue, time, done, i = deque(), 0, {}, 0
    while len(done) < len(processes):
        while i < len(pending) and pending[i][1] <= time:
            queue.append(pending[i][0])
            i += 1
        if not queue:
            time = pending[i][1]
            continue
        name = queue.popleft()
        run = min(quantum, remaining[name])
        time += run
        remaining[name] -= run
        while i < len(pending) and pending[i][1] <= time:
            queue.append(pending[i][0])
            i += 1
        if remaining[name] > 0:
            queue.append(name)
        else:
            burst = next(b for n, _, b in processes if n == name)
            turnaround = time - arrival[name]
            done[name] = (time, turnaround, turnaround - burst)
    return done''',
         harness='''result = round_robin([("A", 0, 5), ("B", 1, 3), ("C", 2, 1)], quantum=2)
assert result == {"C": (5, 3, 2), "B": (8, 7, 4), "A": (9, 9, 4)}
fifo = round_robin([("A", 0, 5), ("B", 1, 3), ("C", 2, 1)], quantum=100)
assert fifo == {"A": (5, 5, 0), "B": (8, 7, 4), "C": (9, 7, 6)}
assert round_robin([("X", 10, 3)], 2) == {"X": (13, 3, 0)}
assert round_robin([], 2) == {}
print("OK")''',
         tests=['con quantum 2 los tiempos de finalización son `C=5, B=8, A=9`', 'con un quantum enorme se comporta como FIFO', 'un proceso que llega tarde espera con la CPU libre', 'sin procesos devuelve un diccionario vacío'],
         why='Cada proceso recibe la CPU durante un quantum y, si no termina, vuelve al final de la cola. Un quantum pequeño mejora la respuesta pero aumenta los cambios de contexto; uno enorme degenera en FIFO. Los procesos que llegan mientras otro se ejecuta entran en la cola antes de que este vuelva a ella.'),
    dict(ch=8, lang='python', level='INTERMEDIATE',
         prompt='Escribe `page_faults(refs, frames, policy)` que cuente los fallos de página con las políticas `"FIFO"` y `"LRU"`. Comprueba la secuencia clásica `1 2 3 4 1 2 5 1 2 3 4 5` con 3 y 4 marcos: con FIFO hay 9 fallos con 3 marcos y 10 con 4 (anomalía de Belady), mientras que LRU no la sufre.',
         code='''from collections import OrderedDict, deque


def page_faults(refs, frames, policy):
    faults = 0
    if policy == "FIFO":
        memory, order = set(), deque()
        for page in refs:
            if page not in memory:
                faults += 1
                if len(memory) == frames:
                    memory.remove(order.popleft())
                memory.add(page)
                order.append(page)
    elif policy == "LRU":
        memory = OrderedDict()
        for page in refs:
            if page in memory:
                memory.move_to_end(page)
            else:
                faults += 1
                if len(memory) == frames:
                    memory.popitem(last=False)
                memory[page] = True
    else:
        raise ValueError(policy)
    return faults''',
         harness='''refs = [1, 2, 3, 4, 1, 2, 5, 1, 2, 3, 4, 5]
assert page_faults(refs, 3, "FIFO") == 9
assert page_faults(refs, 4, "FIFO") == 10
assert page_faults(refs, 3, "LRU") == 10
assert page_faults(refs, 4, "LRU") == 8
assert page_faults(refs, 5, "LRU") == 5 and page_faults(refs, 5, "FIFO") == 5
lru = [page_faults(refs, f, "LRU") for f in range(1, 7)]
assert all(a >= b for a, b in zip(lru, lru[1:]))
assert page_faults([], 3, "LRU") == 0
print("OK")''',
         tests=['FIFO con 3 marcos tiene 9 fallos y con 4 marcos 10 (anomalía de Belady)', 'LRU con 4 marcos tiene 8 fallos', 'LRU nunca empeora al aumentar los marcos', 'sin referencias no hay fallos'],
         why='FIFO expulsa la página más antigua sin mirar si se usa, y por eso tener más memoria puede empeorarlo. LRU pertenece a los algoritmos de pila: el conjunto residente con `n` marcos siempre está contenido en el de `n + 1`, de modo que no sufre la anomalía.'),
    dict(ch=8, lang='python', level='ADVANCED',
         prompt='Implementa un búfer acotado `BoundedBuffer(capacity)` con `put(item)` que bloquee si está lleno y `get()` que bloquee si está vacío, usando `threading.Condition`. Comprueba con 3 productores y 3 consumidores que se entregan todos los elementos exactamente una vez, que nunca se supera la capacidad y que el orden por productor se conserva.',
         code='''import threading
from collections import deque


class BoundedBuffer:
    def __init__(self, capacity):
        self.capacity = capacity
        self.items = deque()
        self.max_seen = 0
        self.cond = threading.Condition()

    def put(self, item):
        with self.cond:
            while len(self.items) >= self.capacity:
                self.cond.wait()
            self.items.append(item)
            self.max_seen = max(self.max_seen, len(self.items))
            self.cond.notify_all()

    def get(self):
        with self.cond:
            while not self.items:
                self.cond.wait()
            item = self.items.popleft()
            self.cond.notify_all()
            return item''',
         harness='''import threading

buf = BoundedBuffer(4)
per = 200
received = []
lock = threading.Lock()

def producer(pid):
    for i in range(per):
        buf.put((pid, i))

def consumer():
    for _ in range(per):
        item = buf.get()
        with lock:
            received.append(item)

threads = [threading.Thread(target=producer, args=(p,)) for p in range(3)] + [threading.Thread(target=consumer) for _ in range(3)]
for t in threads:
    t.start()
for t in threads:
    t.join(timeout=20)
assert not any(t.is_alive() for t in threads), "bloqueo"
assert sorted(received) == sorted((p, i) for p in range(3) for i in range(per))
assert buf.max_seen <= 4
for pid in range(3):
    seq = [i for p, i in received if p == pid]
    assert seq == sorted(seq)
print("OK")''',
         tests=['se entregan los 600 elementos exactamente una vez', 'el búfer nunca supera su capacidad', 'el orden de cada productor se conserva', 'no hay interbloqueo'],
         why='La variable de condición permite esperar sin gastar CPU hasta que cambie el estado. La espera va dentro de un `while`, no de un `if`, porque al despertar hay que volver a comprobar la condición: otro hilo pudo haber vaciado el hueco antes. `notify_all` evita que se despierte a un hilo equivocado.'),
    dict(ch=8, lang='python', level='ADVANCED',
         prompt='Escribe un asignador de memoria de primer ajuste `FirstFit(size)` con `alloc(n)` (devuelve el desplazamiento o `None`) y `free(offset)` que fusione bloques libres adyacentes. Comprueba la fragmentación externa: tras liberar bloques alternos, una petición grande falla aunque haya memoria libre suficiente en total; tras liberar los vecinos, se fusionan y la petición funciona.',
         code='''class FirstFit:
    def __init__(self, size):
        self.free_blocks = [(0, size)]
        self.used = {}

    def alloc(self, n):
        for i, (start, length) in enumerate(self.free_blocks):
            if length >= n:
                if length == n:
                    self.free_blocks.pop(i)
                else:
                    self.free_blocks[i] = (start + n, length - n)
                self.used[start] = n
                return start
        return None

    def free(self, offset):
        length = self.used.pop(offset)
        self.free_blocks.append((offset, length))
        self.free_blocks.sort()
        merged = []
        for start, size in self.free_blocks:
            if merged and merged[-1][0] + merged[-1][1] == start:
                merged[-1] = (merged[-1][0], merged[-1][1] + size)
            else:
                merged.append((start, size))
        self.free_blocks = merged''',
         harness='''mem = FirstFit(100)
blocks = [mem.alloc(10) for _ in range(10)]
assert blocks == list(range(0, 100, 10)) and mem.alloc(1) is None
for offset in blocks[::2]:
    mem.free(offset)
assert sum(l for _, l in mem.free_blocks) == 50
assert mem.alloc(20) is None
mem.free(blocks[1])
assert mem.free_blocks[0] == (0, 30)
assert mem.alloc(20) == 0
assert mem.alloc(10) == 20
for offset in list(mem.used):
    mem.free(offset)
assert mem.free_blocks == [(0, 100)]
print("OK")''',
         tests=['se reparten 10 bloques de 10 contiguos', 'tras liberar los alternos hay 50 libres pero una petición de 20 falla', 'liberar un vecino fusiona los huecos y la petición funciona', 'al liberarlo todo queda un único bloque de 100'],
         why='La fragmentación externa deja memoria libre en trozos demasiado pequeños para servir peticiones grandes. Fusionar bloques adyacentes al liberar es la defensa más barata. Primer ajuste es rápido pero tiende a llenar de restos pequeños el principio; mejor ajuste y otros esquemas cambian la rapidez por el aprovechamiento.'),
]
