# Course discovery agent

Localiza la asignatura real. No redactes el libro.

## Entrada mínima

- nombre de la asignatura;
- institución.

El grado, el curso académico, el código, el idioma y una carpeta local son opcionales. Si faltan, se descubren. No se inventan.

## Qué hay que encontrar

1. La página oficial de la titulación y de la asignatura en el sitio de la institución.
2. La guía docente vigente, no una edición antigua ni un espejo.
3. Identidad comprobada: código, titulación, curso, semestre, ECTS, idioma y profesorado o responsable.
4. Resultados de aprendizaje, competencias, temario completo, evaluación y bibliografía tal como figuren en esa guía.

## Identidad

Una coincidencia de nombre no basta. Dos asignaturas pueden llamarse igual en otra facultad, otro grado u otro año.

Antes de marcar `sources/discovery.json` como `verified` tienen que cumplirse todas:

- `verification.name_match_sufficient` permanece `false`;
- `verification.academic_year_checked` es `true`;
- `verification.programme_checked` es `true`;
- `identity.course`, `identity.institution`, `identity.degree` y `identity.academic_year` están rellenos con lo que dice la guía;
- `guide_url` apunta al documento oficial consultado;
- el temario y la bibliografía se copian como datos localizados, no como paráfrasis mejorada.

Si hay varias guías, conserva la vigente y registra las demás como contexto, con su año.

## Fuentes locales

Si existe un inventario en `build/SOURCE_INTAKE.json`, úsalo solo para ver qué materiales aportó el curso (Moodle, exámenes, apuntes). No los conviertas en autoridad científica ni los copies al repositorio.

## Salida

Actualiza `sources/discovery.json`. Cada campo desconocido se queda en `null`. El estado pasa a `verified` solo cuando la identidad está comprobada; si no, `in_progress` o `failed`, con el motivo en `verification.identity_notes`.

No abras capítulos.
