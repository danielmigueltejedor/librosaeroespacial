# STUDIUM — Materiales y mantenimiento de motores aeroespaciales

Edición completa de estudio, 2026. Estado: **EN REVISIÓN**. Fecha normativa de referencia: 18 de octubre de 2026. Contexto: Grado en Ingeniería Aeroespacial, Universidad de León. No es publicación oficial de la ULE ni de las autoridades citadas.

## Documentos

- `main.tex`: manual de 25 capítulos, 23 figuras originales, ejemplos, preguntas de comprensión con respuesta, fórmulas, glosario y bibliografía.
- `problemas.tex`: 35 problemas originales resueltos y 16 casos académicos de mantenimiento.
- `simulacros.tex`: diez pruebas originales (cuatro de materiales, tres de mantenimiento y tres combinadas), con 40 preguntas y soluciones separadas; S07 a S10 se generan con `scripts/author-materials-extra-exams.py`.

En este repositorio los PDF compilados no se versionan: el compilador del monorepo los genera en `dist/studium/materiales-mantenimiento-motores/`. Los datos de ejercicios y del taller AULA-01 son ficticios. No son instrucciones aprobadas, autorizaciones, límites certificados ni un trabajo evaluable presentado como realización personal de un estudiante.

## Editar y compilar

Se puede abrir esta carpeta en el editor LaTeX de Codex, con `main.tex` como documento principal. También puede usarse una instalación de TeX Live con `latexmk` y pdfLaTeX:

```sh
bash scripts/build.sh
```

Los resultados aparecen en `build/`. El diseño utiliza A4, márgenes de 25 mm, Latin Modern 10 pt y los colores y portada de la colección. El preámbulo común es `latex/preamble.tex`. Cada capítulo principal `cNN.tex` incorpora su desarrollo complementario `eNN.tex`; ambos se editan juntos. No se necesita Python para compilar: las figuras vectoriales están incluidas.

La compilación independiente desde una copia limpia ha dado texto y número de páginas idénticos para los tres documentos. Véase `reports/reproducibility.json`. El compilador integrado también confirmó compilación correcta del manual completo.

## Figuras y bancos de ejercicios

`figures/` contiene PDF vectoriales, PNG y la foto de portada con su licencia. `scripts/figures.py` reconstruye los 23 modelos originales. Curvas y escalas son sintéticas, sin propiedades certificadas de motores reales. Para regenerar figuras o comprobaciones, crear un entorno Python 3.12 e instalar `requirements.txt`.

Los bancos originales están en `scripts/problem_bank.py`, `case_bank.py` y `exam_bank.py`. La normalización editorial está en `scripts/montar_libros.py`, y el desarrollo algebraico explícito de cada problema en `problem_development.py`. `scripts/build_companions.py` reconstruye los dos cuadernos LaTeX. Los archivos `evidence/*-editorial.json` identifican exactamente la versión de datos y textos impresa.

## Proyecto Studium y verificación

El framework de Studium se referencia mediante el commit de `STUDIUM_COMMIT.txt` y no se duplica en el monorepo. El proyecto nativo está en `project/materiales-mantenimiento-ule`; puede abrirse con esa ruta usando una instalación compatible del framework en el commit registrado. La salida editorial de los tres documentos está en los LaTeX de raíz; algunos scripts de auditoría histórica necesitan fuentes externas que no se redistribuyen. Los JSON de casos y simulacros completos se conservan como materiales complementarios junto al proyecto.

Los registros incluyen 66 controles numéricos de los cuadernos, 24 controles de ejemplos del manual, 14 comprobaciones dimensionales de ejercicios, cinco de derivaciones, siete comprobaciones simbólicas y cuatro cuadraturas de Paris. No equivalen a validación física de los datos ficticios. Se conservan intentos rechazados y sus correcciones. `reports/Registro_verificaciones.csv` y los JSON detallan el alcance real.

El estado de autoridad de las fuentes y los bloqueos de auditoría nativa **no se han forzado**. La revisión nativa del libro devuelve `blocked` y el gate no libera la obra: faltan auditorías semánticas individuales, revisión independiente y otras condiciones. Ello no impide compilar una edición completa de estudio rotulada en revisión. No se declara `RELEASED`.

La primera ejecución del framework dio 1070 aprobadas, 2 omitidas y 2 fallidas por importación en subprocesos. Un reintento previo no terminó. Tras corregir el entorno de dependencias y las rutas, las dos pruebas afectadas pasaron en una ejecución dirigida (2/2, 2,41 s). Se conservan todos los registros: no se presenta como una segunda ejecución completa. El uso directo de la API y las comprobaciones del libro también se ejecutaron.

Para reconstruir registros desde cero, hacerlo en **otra copia**, retirando de esa copia `project/`; no ejecutar `setup` sobre el proyecto existente. Reobtener primero las fuentes públicas y extraer sus PDF a `work/texts/` con pdftotext (la guía también en modo `-raw` como `GUIA2026-raw.txt`). El orden de reconstrucción en una copia nueva es: `studium_project.py setup math_checks content extras reports`, `native_finalize.py`, `native_finish_checks.py`. Los scripts de integración registran entradas y no son una operación idempotente. El proyecto entregado ya contiene esos registros y no necesita reimportación para consultar o editar LaTeX.

## Fuentes, normativa y límites

La guía oficial ULE 2026–2027 se recuperó íntegra y se contrastó (cinco páginas). Sus datos de evaluación global se distinguen de porcentajes parciales de diapositivas. Las fuentes consultadas, históricas, recomendadas y pendientes se identifican por separado. Los libros no obtenidos íntegramente se citan solo por metadatos o como recomendaciones.

`reports/Registro_normativo.csv` contiene 36 fichas con versión, disposición, ámbito, consulta y URL. Se usaron las consolidaciones de 1321/2014 (7-08-2026), 748/2012 (22-02-2026), 2018/1139 (2-08-2026), el acto 2026/100, CS-E enmienda 9 y el RAD 866/2015. No se declara una lista exhaustiva actual de AD. El estado de sustitución/cancelación de FAA AD 2024-14-03 sigue pendiente; su publicación original solo acredita el dato histórico. C08 deja pendiente la disposición operacional concreta de MEL por falta de escenario completo.

Las copias protegidas de los cinco archivos de entrada y las descargas públicas voluminosas no se redistribuyen. `evidence/inventario-entrada.json` conserva identificación/huellas y `fuentes-publicas.json` las URL y el alcance. `scripts/fetch_public_sources.py` permite volver a descargar las fuentes públicas; no valida su vigencia futura ni evita que cambie una respuesta.

## Informes y taller

En `reports/`: auditorías científica, matemática, normativa y editorial; contraste de guía; inspección del framework; matriz de cobertura; inventario de 170 expresiones/ecuaciones; registro de verificaciones; registros nativos y compilaciones. Los bloqueos y pendientes son parte de la entrega.

`templates/AULA-01_control_ficticio.csv` es una tabla de referencia del capítulo 25, sin fórmulas ejecutadas de una aplicación. Sirve para reconstruir y probar un modelo propio. Las celdas vacías no son cero. No es un AMP aprobado ni una herramienta para uso operacional.

Fotografía: Olivier Cleynen, detalle del núcleo GEnx (2011), Wikimedia Commons, CC BY-SA 3.0. Se conserva el crédito, original y licencia de su encuadre. Véase `figures/LICENCIA-PORTADA.md`.

## Integración en Libros Aeroespacial

Esta carpeta se incorpora a `books/materiales-mantenimiento-motores/` como fuentes Studium editables, **sin simular que haya pasado los controles científicos de AeroBooks**. Mantiene el preámbulo y la portada de la edición original. `studium-import.json` registra los documentos y la procedencia.

Desde la raíz del monorepo:

```sh
python3 scripts/build-studium-books.py materiales-mantenimiento-motores --check
python3 scripts/build-studium-books.py materiales-mantenimiento-motores
```

La fotografía de portada es de Olivier Cleynen (CC BY-SA 3.0), con créditos en `figures/LICENCIA-PORTADA.md`. Se conserva `EN REVISIÓN`: la auditoría y revisión independiente no han aprobado esta edición. `sources/README.md` explica las fuentes excluidas de la versión pública.
