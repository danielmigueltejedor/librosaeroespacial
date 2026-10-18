# Revisión del bundle Studium — 18 de octubre de 2026

Se revisaron las cinco asignaturas y sus trece volúmenes. Se añadieron los dos cuadernos de Fluidos y se corrigieron los fallos reproducibles descritos a continuación. La compilación, el cálculo y la revisión visual se distinguen de una aprobación académica independiente, que no se atribuye a esta entrega.

## Nuevos cuadernos de Fluidos

- 48 problemas resueltos: tres por cada uno de los 16 capítulos teóricos, con datos, incógnitas, hipótesis, ecuaciones, desarrollo, resultados, interpretación, comprobaciones y límites.
- Siete talleres originales con código Wolfram ejecutado realmente. Retoman modelos del banco; no se cuentan como siete familias físicas adicionales.
- Cuatro simulacros de 150 minutos y diez puntos, con cinco problemas cada uno, rúbrica y soluciones separadas. Las veinte variantes cubren conjuntamente los 16 capítulos y usan parámetros distintos de los problemas resueltos.
- Datos hipotéticos originales y esquemas vectoriales propios. No se reproducen exámenes oficiales, medidas experimentales ni documentos privados. Fuentes y clasificación en `books/mecanica-fluidos/bibliography/exercise-sources.json`.

## Fallos corregidos

| ID | Hallazgo y corrección |
| --- | --- |
| MF-TIPO-01 | El manual dejaba activo `footnotesize` tras notas sin agrupar. Se eliminaron 87 etiquetas genéricas y se agruparon las dos notas dimensionales restantes; el texto conserva la tipografía común. |
| TRAZA-01 | Se retiraron 87 etiquetas de Fluidos y 58 de Estructuras que afirmaban una verificación independiente sin delimitar su evidencia. Las comprobaciones reales y sus límites quedan en los informes. No se eliminaron ecuaciones. |
| TUR-RESP-01 | C03-01 pedía temperatura total real de salida pero sólo desarrollaba incremento isentrópico y trabajo. Se añadió el resultado de temperatura y su balance energético. |
| TUR-RESP-02 | C16-01 pedía ambas componentes de salida del difusor, pero faltaba el resultado radial. Se añadió con su comprobación de continuidad. |
| TUR-RESP-03 | C18-01 pedía velocidad periférica, pero sólo mostraba remolino y ángulos. Se añadió `U=Omega r` y se reconstruyó el triángulo relativo. |
| TUR-ALCANCE | Las tres correcciones anteriores se aplican a las variantes R/P: seis ejercicios, presentes tanto en el manual como en el cuaderno de problemas, doce lugares de publicación. Los resultados principales previos se conservan. |
| STR-ROT-01 | Un desarrollo de giro por trabajos virtuales titulaba su suma «desplazamiento». Se corrigió a «giro», conservando valor y radianes. |
| MC-REPRO-01 | Faltaba `cea-case.json`, necesario para reproducir el banco de Motores Cohete. Se ejecutaron de nuevo los seis equilibrios TP con CEA y se incorporó su resultado público. Se repitieron también seis diferencias finitas de entalpía. |
| INDICE-01 | Se amplió el espacio reservado al número de capítulo en el índice común para separar correctamente los números de dos cifras del título. |
| BUILD-01 | La comprobación de recursos no examinaba `lstinputlisting`. Ahora comprueba que los talleres existan y permanezcan dentro del libro. Se añadieron tres regresiones. El control final también rechaza labels duplicados. |
| MF-PAG-01 | En las primeras maquetas nuevas algunos cierres o comienzos de ejercicio quedaban aislados. Se compactaron las síntesis y se mantuvieron juntos los enunciados y sus datos en los simulacros. |

## Comprobaciones ejecutadas y cobertura

| Asignatura | Controles de esta pasada | Alcance y límites |
| --- | --- | --- |
| Estructuras | 405 controles satisfactorios sobre 105 ejercicios | Aritmética con tolerancias de redondeo; integración de paredes y booms; centros de cortadura y máximos de tensión reconstruidos en ocho geometrías; contrastes seleccionados de energía y elasticidad. Las unidades escritas junto a un resultado no se cuentan por sí solas como una verificación dimensional. |
| Fluidos | 329 controles del banco nuevo y sus veinte variantes; 14 de fase 5 y 25 de fase 6 | Evaluación dimensional con Pint frente a SymPy, ecuaciones diferenciales, condiciones de pared, cuadraturas, balances y límites seleccionados. No se presenta como comprobación exhaustiva de cada afirmación del manual. |
| Fluidos, talleres | Siete scripts ejecutados con Wolfram Language | Se conservan versión, salida y hash. El primer ajuste de integración de W02 no alcanzaba su tolerancia; se limitó el paso y se repitió sin relajar el umbral. |
| Motores Cohete | 269 controles, seis equilibrios TP y seis contrastes de derivada de entalpía | Conservación, dominios, aritmética, modelos ideales y reproducibilidad del caso CEA. La derivada usa el mismo código y base CEA; no es validación externa de esa base ni prestación experimental de un motor. |
| Tecnología Aeroespacial | 53 controles y 30 rutas alternativas con dimensiones | Modelos de atmósfera, medidas, aerodinámica, actuaciones, órbita y potencia. Se comprobó que las soluciones de sus simulacros están en el cuaderno de problemas, tal como indican los enunciados. |
| Turbomáquinas | 674 controles sobre 150 casos | Unidades, resultados del banco, dominios e identidades seleccionadas; presencia y balances de las magnitudes completadas. C17-04-P sigue siendo un ejercicio deliberado de diagnóstico con rendimiento imposible, no una máquina aceptada. |

Los trece documentos se compilaron a tres pasadas con las advertencias de desbordamiento, referencias, citas, caracteres y labels duplicados tratadas como fallos. El inventario final de páginas y SHA-256 está en `pdf-checks.json`. Se examinaron automáticamente todas las páginas y se revisaron visualmente las páginas nuevas, aperturas de capítulos, portadas, páginas densas y correcciones seleccionadas. La revisión visual es del mismo agente autor, sin atribuirle independencia.

`math-preservation.json` compara los cuatro manuscritos corregidos con el commit de partida: no desaparece ningún bloque matemático previo. Las adiciones de Turbomáquinas completan las respuestas indicadas.

Las 38 pruebas del framework y del compilador portable pasaron. Los gates nativos de AeroBooks se intentaron en los cinco proyectos; siguen sin estar configurados por tratarse de importaciones sin `book.toml`. Se conserva ese resultado como `NOT_CONFIGURED`, sin convertirlo en aprobado.

## Reproducir

La compilación normal necesita Python 3.11+ y TeX Live:

```sh
python3 scripts/build-studium-books.py all --check
python3 scripts/build-studium-books.py all
python3 -m unittest discover -s tests -v
```

Los controles científicos adicionales necesitan Python 3.12+ con las versiones de `requirements-audit.txt`. CEA 3.3.4 y Wolfram Language son requisitos separados para sus respectivos cálculos:

```sh
python scripts/audit-estructuras.py
python scripts/audit-turbomaquinas.py
python books/mecanica-fluidos/scripts/check_fluid_bank.py
python books/mecanica-fluidos/scripts/verificaciones_simbolicas_fase5.py
python books/mecanica-fluidos/scripts/verificaciones_simbolicas_fase6.py
python books/motores-cohete/scripts/cea_case.py
python books/motores-cohete/scripts/cea_derivative_check.py
python books/motores-cohete/scripts/check_science.py
python books/tecnologia-aeroespacial/scripts/check_science.py
python books/tecnologia-aeroespacial/scripts/check_bank.py
python scripts/audit-studium-pdfs.py
wolframscript -file books/mecanica-fluidos/workshops/w01.wl
```

Para los talleres, repetir el último comando con `w02.wl` a `w07.wl`. El banco y las fórmulas originales de Estructuras y Turbomáquinas se conservan en JSON público para que estos controles no dependan de un servidor, registros privados ni rutas del equipo del autor.

## Pendientes que no se cierran por cálculo automático

Continúan los alcances y pendientes académicos recogidos en cada libro: corroboración localizada de toda la teoría, aplicabilidad de correlaciones y modelos de materiales, geometrías y condiciones reales, y revisión experta independiente. No se declara validación experimental ni certificación para diseño. La entrega es un archivo de estudio con fuentes editables y controles reproducibles, no un release manifest académico.
