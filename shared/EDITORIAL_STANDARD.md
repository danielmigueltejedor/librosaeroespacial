# Norma común de la colección Studium

Los once volúmenes de las cinco asignaturas cargan `shared/latex/studium-editorial.tex` y `studium-cover.tex`. Las reglas visuales se editan una sola vez. Cada proyecto conserva únicamente su fotografía, crédito, título y edición en `editorial-config.tex`.

## Composición

- A4, cuerpo de 10 puntos, Latin Modern, márgenes de 25 mm, encabezado de 14 puntos.
- Igual jerarquía y espaciado de capítulos, secciones y subsecciones. El índice general llega a las secciones; la numeración del texto incluye subsecciones.
- Párrafos con sangría de 1,5 em y separación de 3 puntos. Listas, leyendas, encabezados y numeración de páginas compartidos.
- Portada con cabecera blanca, ventana fotográfica, bloque azul y texto vectorial. El tipo de volumen distingue manual, problemas y simulacros.
- Definiciones y desarrollos en azul; consejos en verde; problemas resueltos en naranja; síntesis y autoevaluación en violeta.

## Organización de los volúmenes

1. Portada.
2. Cómo utilizar este volumen, con instrucciones según sea manual, problemas o simulacros, seguido en la misma página por créditos y alcance editorial, incluida la procedencia de la fotografía.
3. Presentación y alcance específico de la asignatura, cuando exista en el manuscrito.
4. Índice general y, en los manuales, índice de figuras.
5. Texto de estudio o entrenamiento.
6. Anexos y bibliografía existentes.

## Organización de los capítulos

Los 103 capítulos principales de los manuales abren con **Orientación del capítulo** y cierran con **Comprobación final**. Se conservan las secciones técnicas de cada disciplina, sus deducciones, ejemplos y ejercicios. Las antiguas «Autofichas» se llaman **Autoevaluación** y se sitúan al final del capítulo. Cuando ya existe un resumen, se presenta como **Síntesis del capítulo**; no se fabrica un resumen científico para los capítulos que no lo tenían.

Los recuadros de deducciones se llaman **Desarrollos del modelo** y los de ejercicios **Ejercicios propuestos**. Los problemas del cuaderno de Turbomáquinas usan la misma familia de recuadros que los otros cuadernos. Los niveles de dificultad y los tipos de ejercicio se presentan en español.

Los anexos equivalentes comparten nombres: **Notación y unidades**, **Formulario y condiciones de uso**, **Soluciones de los ejercicios** y **Plan de estudio**. Los anexos especializados conservan sus títulos y su contenido.

## Conservación del contenido

Esta revisión modifica presentación, nombres editoriales y ubicación de preguntas de repaso. No añade una aprobación académica. Se comparan las expresiones matemáticas y los identificadores de problemas y referencias con el estado anterior; las preguntas movidas conservan su texto. La compilación exige ausencia de referencias indefinidas y desbordamientos. La inspección visual incluye portadas, índices, aperturas, cierres y páginas de problemas extensos.

## Editar y compilar

Desde la raíz:

```sh
python3 scripts/build-studium-books.py all --check
python3 scripts/build-studium-books.py all
```

Los recursos compartidos están declarados en cada `studium-import.json`; el compilador solo permite dependencias comunes registradas bajo `shared/latex/`. Los PDF se generan en `dist/studium/<libro>/`.
