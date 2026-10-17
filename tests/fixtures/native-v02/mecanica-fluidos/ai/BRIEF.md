# Brief del libro

Este archivo es el **blueprint editorial y académico** del libro. Una IA no debe cambiar estas decisiones sin una instrucción explícita.

## Identidad

- **Título:** Mecánica de Fluidos
- **Subtítulo:** Fundamentos, modelización y resolución de problemas
- **Volumen:** Volumen I. Fundamentos
- **Autor:** Daniel Miguel Tejedor
- **Idioma:** español
- **Edición actual:** Primera edición
- **Fecha editorial:** Octubre de 2026
- **Contexto:** Grado en Ingeniería Aeroespacial, Universidad de León, asignatura Mecánica de Fluidos, código 0710311, plan 2018, segundo curso, primer semestre, 6 ECTS, guía docente firmada 2026/2027.

## Misión

Este libro enseña la Mecánica de Fluidos de la asignatura 0710311 desde los prerrequisitos de primer curso hasta un nivel con el que el estudiante pueda plantear, derivar y comprobar los modelos del programa. No es un resumen de apuntes. Cada resultado central muestra sus hipótesis, el camino matemático, el significado físico, los límites y un uso en un problema original.

Debe servir a la vez para aprender la materia, entender los mecanismos, repetir las derivaciones, resolver problemas, preparar el examen de la Universidad de León y consultar después las ecuaciones con sus condiciones de validez. La guía docente vigente manda sobre el alcance. Las lecturas de esa guía orientan el nivel. Las derivaciones del propio libro son la evidencia de los resultados matemáticos. El material de estudiantes solo informa del énfasis y de la nomenclatura, y nunca autoriza una fórmula.

## Audiencia

- curso / nivel: segundo curso del Grado en Ingeniería Aeroespacial de la Universidad de León, primer semestre, 6 ECTS. El texto también debe poder leerse como manual de consulta al terminar la asignatura.
- conocimientos previos: álgebra lineal y geometría, cálculo diferencial e integral, fundamentos físicos, ampliación de física, métodos numéricos y estadísticos, e informática, que son las materias que la guía recomienda haber cursado. Se usa también, en paralelo, Métodos matemáticos en ingeniería.
- profundidad matemática: cálculo vectorial en coordenadas cartesianas y cilíndricas, teoremas de Gauss y Stokes, ecuaciones diferenciales ordinarias lineales de segundo orden, y el álgebra del teorema Pi. No se exige análisis funcional ni existencia de soluciones débiles de Navier–Stokes.
- profundidad científica: modelo del continuo, fluidos newtonianos incompresibles, hidrostática, balances integrales, Navier–Stokes con viscosidad constante, soluciones exactas laminares, Bernoulli con hipótesis explícitas, semejanza, y las aproximaciones de Stokes, Boussinesq y equilibrio geostrófico al nivel de la guía. La turbulencia se trata por el número de Reynolds y por sus consecuencias en coeficientes, no con un cierre estadístico.
- perfil de examen: la guía 2026/2027 exige un examen escrito final, 70 por ciento, con mínimo de 5 sobre 10, y ejercicios presenciales de clase, 30 por ciento, con uso de modelos y simulación. El examen ordinario 2025/2026, anterior a esta guía, muestra problemas simbólicos que combinan balance de fuerzas, función de corriente, una solución viscosa y semejanza. Ese documento no se copia.
- tiempo de estudio esperado: del orden de las horas de la guía, 6 ECTS, con lectura activa y resolución de problemas. No se convierte esa cifra en un calendario hora a hora.

## Alcance

### Incluye

El temario firmado de 2026/2027, reordenado para estudiar. La correspondencia es:

| Tema de la guía | Capítulos |
| --- | --- |
| 1. Mecánica clásica, sistemas de referencia, trabajo-energía, lagrangiana, introducción al caos | 2 |
| 2. Continuo, fluido, descripciones, visualización, incompresibilidad, laminar y turbulento | 1 y 4 |
| 3. Estática, flujos externos e internos, Couette, Poiseuille, oscilaciones, aerogeneradores, motores a reacción | 5, 8 y 11 |
| 4. Semejanza, Reynolds, coeficientes, Darcy–Weisbach, Buckingham | 10 y 11 |
| 5. Operadores, teoremas, Reynolds, continuidad, función de corriente, vorticidad, Bernoulli, difusión, tensor de esfuerzos, ley newtoniana | 3, 4, 6, 7 y 9 |
| 6. Conservación, Euler, Navier–Stokes, forma adimensional, Stokes, aproximación hidrostática, Boussinesq, giro y geostrofía | 6, 8 y 12 |

### No incluye todavía

- cohetes y ecuación de masa variable: estaban en las guías 2022/2023 y 2024/2025 y en apuntes de estudiante, y no están en la guía firmada 2026/2027;
- tabla de la atmósfera ISA y comparación numérica de planetas: aparecen en apuntes Tier D y no en la guía vigente;
- dinámica de gases compresible, ondas de choque y toberas supersónicas, que corresponden a otras asignaturas del plan;
- capa límite con ecuaciones de Prandtl y métodos integrales, más allá de nombrar el régimen de Reynolds alto;
- cierre de turbulencia, CFD y el libro de Anderson de 1995, que la guía lista pero que este volumen no desarrolla;
- termodinámica aplicada más allá de la energía mecánica del fluido y de las leyes de Fourier y Fick al nivel en que la guía las nombra.

### Futuras ediciones

- un volumen de aerodinámica y flujo compresible alineado con la asignatura de Aerodinámica;
- capa límite y una introducción honesta a la turbulencia media;
- más problemas de simulación con el papel que la guía da a las prácticas informáticas.

## Criterios de aceptación

Una edición no se considera terminada únicamente porque compile.

- los seis temas de la guía 2026/2027 están cubiertos y el mapa tema–capítulo es explícito;
- cada ecuación central declara hipótesis, dimensiones y un caso límite;
- los claims de riesgo alto están en el ledger, tienen evidencia verificada y un `\claimref` en el manuscrito;
- las derivaciones de continuidad, cantidad de movimiento, Navier–Stokes incompresible, Bernoulli, Couette, Poiseuille, cilindro giratorio, Darcy laminar y el máximo del disco actuador están escritas con los pasos;
- los ejercicios son originales, graduados y con comprobación;
- hay índice de figuras, índice de cuadros, notación e índice analítico;
- no se reproduce el examen ni los apuntes Wuolah;
- `aerobooks check --strict`, `coverage --strict`, el academic gate y la compilación pasan;
- el PDF se ha inspeccionado, no solo compilado.

## Autoridad y convenciones

Orden si hay conflicto de contenido científico o de alcance:

1. Guía docente firmada 2026/2027 de la asignatura 0710311.
2. Ficha oficial del plan 2026/2027 para datos de identificación.
3. Derivaciones reproducibles de este libro, con hipótesis escritas.
4. Lecturas de la propia guía (Taylor, Shaughnessy, Tritton, White, Kundu, Powers, Boas, Strogatz), sin inventar páginas no consultadas.
5. Guías ULE de cursos anteriores, solo para documentar cambios de programa.
6. Material Wuolah, solo para énfasis, nomenclatura y tipo de examen.

Convenciones que no se cambian sin autorización:

- sistema internacional: metro, kilogramo, segundo, kelvin, newton, pascal, julio, vatio;
- velocidad \(\vect{v}=(u,v,w)\); presión \(p\); densidad \(\rho\); viscosidad dinámica \(\mu\); viscosidad cinemática \(\nu=\mu/\rho\);
- eje \(z\) hacia arriba y \(\vect{g}=-g\vect{e}_z\), salvo que un problema declare otro eje;
- tracción de Cauchy: la fuerza por unidad de área ejercida sobre el material, en el lado hacia el que apunta \(\vect{n}\), es \(\mat{\sigma}\vect{n}\);
- función de corriente bidimensional incompresible: \(u=\partial\psi/\partial y\), \(v=-\partial\psi/\partial x\);
- fluido ideal significa no viscoso. No significa, por sí solo, incompresible;
- estacionario significa \(\partial/\partial t=0\). No implica aceleración material nula;
- derivada material \(D/Dt=\partial/\partial t+\vect{v}\cdot\nabla\);
- el número de Reynolds es \(\mathrm{Re}=\rho V L/\mu\), y la longitud \(L\) se declara en cada problema;
- el coeficiente de resistencia y el de sustentación usan \( \tfrac12\rho V^2 A \);
- el factor de Darcy–Weisbach se define de modo que la pérdida de carga sea \(f (L/D) V^2/(2g)\);
- cifras de un problema son datos del enunciado, no propiedades universales medidas;
- referencias en autor-año;
- identidad visual de AeroBooks;
- los problemas del libro son originales.

## Política ante conflictos

- Si los apuntes y una derivación discrepan, se registra el conflicto, se conserva la derivación con hipótesis y no se cita el apunte como prueba.
- Si dos guías oficiales discrepan en bibliografía o en el temario, manda la guía firmada 2026/2027. La diferencia queda en `sources/conflicts.jsonl`.
- Si un examen contradice la teoría, el examen describe una convocatoria; no modifica una ley. No se copia el enunciado.
- Si la discrepancia es solo de nombre o de signo, se traduce al convenio de este brief y se dice la traducción una vez.
- No se elige en silencio entre Tritton 1988 y Tritton 2011, ni entre White 2015 y White 2016: la ficha vigente fija el año bibliográfico y la nota declara la otra fecha.
- Un hueco sin fuente ni derivación se deja como pendiente o se omite. No se rellena con una cifra plausible.

## Política para IA

- no rellenar lagunas;
- separar fuente, derivación e interpretación;
- añadir fuentes externas al manifiesto;
- registrar conflictos;
- revisar claims de alto riesgo;
- mantener evidence map;
- usar chapter specs;
- no autoaprobar el propio texto;
- ejecutar quality gates antes de cerrar cambios;
- no subir los PDF de Wuolah al repositorio;
- no reconstruir apuntes ni exámenes protegidos.

## Perfil didáctico

- intuición antes del formalismo cuando el concepto lo permite, sin saltarse las hipótesis;
- derivaciones con los pasos que cambian el resultado;
- ejercicios graduados: básico, intermedio, tipo examen y una aplicación aeroespacial;
- errores frecuentes sacados de fallos de razonamiento, no copiados como lista de un apunte;
- comprobación dimensional, de signos, de condiciones de contorno y de casos límite;
- cada capítulo declara qué tema oficial cubre;
- autoevaluación breve al final de cada capítulo.

## Perfil visual

- densidad de página: texto continuo de manual, con cajas solo cuando separan una definición, un riesgo o un ejemplo;
- estilo de figuras: TikZ, paleta AeroBooks, vectores con sentido comprobado, sin decoración;
- uso de color: azul para la geometría principal, naranja para datos o cargas, verde para una comprobación;
- nivel de tablas/cajas: cuadros de hipótesis y de convenio; pocas cajas por sección;
- restricciones de portada: la portada común del framework, con la figura técnica del libro.

## Reglas de copyright / uso de fuentes

- la guía docente puede citarse y parafrasearse en lo necesario para fijar el programa y la evaluación;
- los libros de la bibliografía se nombran como lecturas; no se transcriben;
- los vídeos del profesor y las conferencias de Lewin no se transcriben;
- los PDF de Wuolah no entran en el repositorio, no se reformulan párrafo a párrafo y no suministran enunciados;
- los problemas y las figuras de este libro son originales;
- una cita textual, si hiciera falta, sería breve y atribuida. Esta edición no necesita citas textuales de obras protegidas.

## Quality gate

Antes de cerrar una edición:

- source audit de la guía 2026/2027 y de la bibliografía listada;
- conflictos cerrados o aceptados de forma explícita;
- chapter specs;
- evidence map;
- claim ledger sin claims críticos pendientes;
- revisiones independientes declaradas;
- red-team;
- compilación;
- inspección visual del PDF;
- changelog de la edición;
- release manifest verificado.

## Decisiones de esta edición

- El orden pedagógico no copia el orden de los apuntes ni el de la guía. La guía estudia casos antes del formalismo; el libro construye primero el lenguaje y luego los casos, y el apéndice de auditoría explica el mapa.
- Lorenz se introduce como el sistema de tres ecuaciones ordinarias nombrado en la guía. No se afirma un conjunto de parámetros numéricos porque no se ha abierto la página correspondiente de Lorenz (1963) ni de Strogatz (2018).
- Anderson (1995) permanece en la bibliografía registrada y fuera del desarrollo.
- Las propiedades físicas que un problema necesite se dan en el enunciado.
