# Enciclopedia de Programación e Ingeniería del Software

**Edición de estudio en revisión. No es una biblioteca completa ni una edición
aprobada académicamente.** La revisión conserva la colección de diez volúmenes
(vol00 es su guía, no la edición integral), identifica defectos de la generación
anterior y mejora el framework, la presentación y varios ejemplos/proyectos.

La afirmación anterior de «511 problemas verificados» queda retirada. El estado
inicial contiene 503 problemas numéricos y 8 pruebas Rust. Los controles de
aritmética, diversidad bibliográfica y compilación no validan una implementación
ni la suficiencia de su explicación. La revisión curricular de los 75 capítulos
sigue abierta; los recuentos de palabras no la sustituyen.

## Aprender mediante práctica

La edición incorpora once recorridos iniciales: Python, JavaScript, TypeScript,
Rust, C, C++, Java, C#, Go, SQL y Bash. Cada uno contiene un primer programa,
contrato de entrada, traza explicada, errores frecuentes y tres ejercicios con
soluciones separadas. Los ejemplos impresos y las referencias completas se
ejecutan con herramientas reales; los resultados están en
`reports/learning-verification.json` y el código editable en `learning/`.
La guía del volumen 0 indica el orden recomendado y los prerrequisitos.

[Descarga de la colección completa organizada por temas](https://github.com/danielmigueltejedor/librosstudium/releases/tag/librosstudium-aprendizaje-2026-10-21-r2).
La revisión curricular independiente de los 75 capítulos sigue pendiente;
estos recorridos no certifican los capítulos avanzados ni los demás lenguajes.

## Edición de lectura depurada

Se elimina la hoja de fórmulas vacía y los apéndices de notación, auditoría interna
y plan de trabajo automático. La portada ya incluye orientación y alcance, por
lo que se omiten los prefacios genéricos repetidos. Se mantienen capítulos,
actividades útiles, soluciones de práctica, bibliografía y créditos. La guía y
los dos primeros volúmenes no duplican en un apéndice los desarrollos ya resueltos.

Se retiran mediante revisiones, conservando su historial, 192 ejercicios de
plantilla sin escenario técnico y 20 ejercicios de inventario del volumen guía.
Con los 33 ejercicios nuevos quedan 332 actividades activas: 291 numéricas,
8 pruebas Rust y 33 de programación. No se presentan como 332 programas
verificados. Las correcciones focalizadas están registradas
en `reports/reader-cleanup.json`; los controles de toda la colección, en
`reports/reader-edition-checks.json`.

Cada `project.toml` selecciona explícitamente las secciones de lectura mediante
`[render]`. Los libros STEM sin esa configuración conservan sus apéndices.

## Ejercicios: programas que escribir (2026-10-23)

Los ejercicios de cálculo aritmético se han retirado (la revisión conserva su
historial) y los volúmenes 1 a 9 piden ahora **programas**: 218 ejercicios con
enunciado, solución de referencia, casos comprobados y una breve explicación de
por qué funciona. Cada solución de referencia se ejecuta con sus pruebas antes de
registrarse, con toolchains reales: Rust, C, C++, Zig, ensamblador AArch64,
Fortran, Python, JavaScript, TypeScript, Java, Go, C#, Kotlin, Swift, SQL, Bash,
PHP, Ruby, Haskell, OCaml, Elixir, Clojure, Scala, Julia, R, Lua, Perl, Prolog y
Objective-C. Faltan Ada, Dart y GDScript por no disponer de su toolchain.

- `tools/exercise_specs/volNN.py`: enunciados, soluciones y pruebas.
- `tools/exercises.py verify|record|retire`: ejecuta, registra como contrato de
  programación de Studium y retira los ejercicios numéricos.
- `reports/exercise-verification.json`: versión de cada herramienta, huella del
  programa y salida observada. Un acierto significa que la solución cumple los
  casos indicados en esa versión; no es una aprobación del volumen.
- Los enunciados que el primer intento de comprobación dejó mal (un `take` sobre
  `filter` en C++20, el quantum de la BEAM, un mensaje Protobuf sin etiqueta, la
  complejidad ciclomática de una refactorización) ya no existen: sus
  ejercicios se sustituyeron por programas.

Pendiente: el segundo extracto que citaban los ejercicios antiguos de los
volúmenes 3 a 7 era texto inventado que la migración de integridad retiró, y
44 de los 50 párrafos de cada uno de esos volúmenes carecen de extractos
verificados. Siguen abiertos: es el motivo de la nota «REVISIÓN DE FUENTES
PENDIENTE» de esos volúmenes.

## Resultados y estado

- `reports/baseline-inventory.json`: referencia Git, inventario y recompilación
  original de los diez volúmenes: 459 páginas, 75 capítulos y 46 desbordamientos.
- `reports/evidence-integrity-migration.json`: reparaciones append-only de
  referencias inventadas, URLs sintéticas y texto añadido a extractos.
- `reports/current-inventory.json`: inventario vigente, problemas, capítulos,
  fuentes, ubicación por identificadores y defectos de composición.
- `reports/code-verification-current.json`: comprobaciones vigentes con huellas,
  herramientas observadas, salidas y alcance. Un estado pendiente impide declarar
  completa la verificación; no se transforma en éxito.
- `reports/PROGRESS.md`: hitos comprobados, limitaciones y trabajo pendiente.

Los informes `MASTER-AUDIT-REPORT.md`, `master-audit-summary.json` y
`code-verification.json` describen la entrega anterior y están superados. Se
conservan como evidencia histórica, con un aviso de alcance.

## Instalación reproducible

Python 3.12 (Studium admite Python >=3.11). Crear un entorno e instalar:

```sh
python3.12 -m venv .venv
. .venv/bin/activate
python -m pip install -r enciclopedia-programacion/requirements.txt
```

La versión exacta de Studium queda fijada a un commit en ese archivo. No depende
de un directorio privado ni de un clon hermano. Para desarrollar contra otro
clon de Studium, instalar explícitamente ese clon en el entorno con `pip install
/ruta/elegida/studium`; no cambiar el generador para introducir rutas personales.

LaTeX: pdfLaTeX o Tectonic; con TeX Live instalar `latex-base`, `latex-extra`,
`latex-recommended`, `fonts-recommended`, `lang-spanish`, Latin Modern y TikZ.
En Debian/Ubuntu esos nombres llevan el prefijo `texlive-`, salvo `lmodern`.
Los paquetes `upquote` y `accsupp` preservan comillas y el texto Unicode literal.
Poppler permite renderizar las páginas para revisión visual y comprobar el texto extraído.

Compiladores opcionales en PATH: Rust/rustc y Cargo, C17, C++20, Node.js 24 y
TypeScript 5.9.3 (`tsc`). Los proyectos Python necesitan pytest; SQLite procede
del módulo estándar Python. Los recorridos iniciales también usan Java/JDK 11,
.NET SDK 8, Go y Bash; la configuración reproducible está en el flujo
`programming-review.yml`. Su versión real se registra. La ausencia de una
herramienta deja un pendiente, nunca una comprobación ficticia.

## Compilar sin regenerar la autoría

```sh
python enciclopedia-programacion/tools/build_collection.py vol03-monografia-rust --review-copy
python enciclopedia-programacion/tools/build_collection.py all --review-copy
python enciclopedia-programacion/tools/audit_collection.py
python enciclopedia-programacion/tools/check_integral.py
```

Las salidas están en `enciclopedia-programacion/dist/review/`, incluido
`ENCICLOPEDIA_COMPLETA_INTEGRAL.pdf`. Se construyen en directorios temporales y
se publican con reemplazos controlados. La compilación comprueba las huellas de
entrada y no escribe en los diarios, las revisiones o los identificadores del
volumen. `build-config.json` fija la fecha de construcción. Los nuevos PDF son
artefactos locales/CI; no se añaden binarios PDF a Git.

`--review-copy` incluye explícitamente manuscritos cuya evidencia está bloqueada
y diagramas TikZ pendientes, con avisos visibles. No cambia su estado académico.
Sin esa opción, Studium conserva sus filtros habituales y rechaza un volumen
incompleto. Los underfull quedan registrados; los desbordamientos, referencias indefinidas,
caracteres ausentes y errores de LaTeX impiden publicar la copia.

La generación de un volumen nuevo es una operación diferente en
`build_studium_volume(..., operation="generate")`. Se rechaza si el volumen ya
existe o faltan identificadores/citas auténticas. Los resúmenes del catálogo
anterior están marcados como texto no contrastado y no pueden convertirse en
extractos de fuente mediante la generación. Una fuente nueva requiere
`text_origin="opened_source_quote"`, `locator`, `retrieved_on`,
`license_verified=true` y `license_evidence_url`, registrados tras abrir el
original y comprobar sus condiciones. Esta procedencia no constituye aprobación
de las afirmaciones del manuscrito. **Todavía no hay un actualizador
semántico general de blueprints**: las correcciones existentes se versionan como
revisiones append-only con los mismos identificadores. Se evita reemplazarlas
por una nueva generación que perdería su trazabilidad.

## Verificar código y proyectos

```sh
# Inventario y análisis sin autorizar ejecución de programas externos:
python enciclopedia-programacion/tools/code_verifier.py
# Solo tras revisar los hashes de programas propios, o dentro de un entorno aislado:
python enciclopedia-programacion/tools/code_verifier.py --trusted
python -m pytest tests/test_programming_pipeline.py
```

El verificador no ejecuta comandos procedentes de fuentes. Usa adaptadores de
Studium y recetas fijas para los seis proyectos. `--trusted` autoriza ejecución
local de los programas revisados: los límites temporales/de salida y el
directorio temporal **no son un sandbox de seguridad**. Para código no confiable
se requiere un contenedor/VM externo. El código pendiente de adaptador o de
comprobación de resultados permanece pendiente. El comando sale con 1 si hay
fallos, con 2 si hay pendientes y con 0 solo si las comprobaciones solicitadas
pasan sin pendientes.

## Diseño y contenidos

La portada utiliza `shared/latex/studium-cover.tex`, con los valores antiguos de
Ingeniería Aeroespacial/Universidad de León como predeterminados compatibles.
La enciclopedia declara su propia colección y condición de obra independiente.
La jerarquía de títulos y cabeceras se comparte mediante
`shared/latex/studium-typography.tex`. Las diez fotografías, sus licencias y
transformaciones están en `assets/covers/manifest.json`.

Se han añadido desarrollos originales sobre préstamos en Rust y el compilador
educativo Python en `content/revisions/`, incorporados al manuscrito mediante
revisiones de los mismos párrafos. El resto de los capítulos todavía necesita
ampliación y revisión individual. Estos cambios no justifican llamar «experto» a
un ejemplo breve ni cerrar itinerarios autónomos de lenguajes completos.

## Auditoría de práctica y caracteres

```sh
python enciclopedia-programacion/tools/verify_learning.py --trusted
python enciclopedia-programacion/tools/audit_learning.py
python enciclopedia-programacion/tools/check_literal_fidelity.py
```

Usar `--trusted` únicamente tras revisar estas fuentes propias. El comprobador
registra casos finitos, versiones, salidas y hashes; no ejecuta código arbitrario
con aislamiento. El control de caracteres recorre los literales activos y
compara fixtures extraídos del PDF, excluyendo espacios de maquetación. El
archivo editable conserva la indentación exacta. Un carácter literal sin soporte
provoca un diagnóstico explícito en vez de sustituirlo silenciosamente.

La auditoría `reports/pedagogical-audit.json` inventaría los 75 capítulos y
separa los once recorridos incorporados del material que requiere ampliación
y revisión independiente.
