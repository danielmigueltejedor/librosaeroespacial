# Source Policy

## Jerarquía de fuentes

Los tiers `A`–`E` siguen vigentes. AeroBooks 0.3 añade un código fino en `tier_detail`. La letra inicial es el tier grueso (`E` se queda en `E`).

| Código | Clase |
| --- | --- |
| A0 | asignatura oficial |
| A1 | norma o documento de una administración |
| A2 | peer-reviewed |
| A3 | libro académico canónico |
| B0 | libro académico abierto |
| B1 | material universitario oficial |
| B2 | repositorio institucional |
| C0 | preprint |
| C1 | documentación técnica reconocible |
| D0 | material informal de curso |
| D1 | examen |
| D2 | apuntes de estudiantes |
| E | rechazado o no verificable |

Un preprint (`C0`) no se marca como peer-reviewed.

### Tier A — primaria / oficial
Ejemplos:
- normativa oficial;
- documentación institucional;
- paper original;
- manual del fabricante;
- guía docente oficial;
- datos de una agencia o archivo oficial.

Uso: autoridad principal cuando sea pertinente.

### Tier B — autoridad académica
Ejemplos:
- textbook reconocido;
- handbook;
- estándar técnico;
- review peer-reviewed;
- monografía académica.

Uso: base para teoría consolidada y contexto.

### Tier C — material académico abierto
Ejemplos:
- MIT OCW;
- TU Delft OCW;
- notas universitarias institucionales;
- repositorios docentes.

Uso: explicación, contraste y ejercicios.

### Tier D — material de estudiantes / archivo de examen
Ejemplos:
- Wuolah;
- resúmenes de estudiantes;
- correcciones no oficiales.

Uso: estilo de examen, terminología local, pistas de énfasis. No elevar automáticamente a autoridad científica.

### Tier E — secundaria general
Ejemplos:
- prensa generalista;
- blogs;
- webs divulgativas;
- foros.

Uso: descubrimiento o contexto. Las afirmaciones técnicas centrales deben verificarse con tiers superiores.

## Reglas de corroboración

- Un claim científico central debe tener una fuente A/B/C o una derivación reproducible.
- Un claim histórico central debe tener preferentemente A/B y no basarse solo en una fuente E.
- Una cifra precisa debe conservar unidad, contexto y fuente.
- Una fecha precisa debe poder trazarse.
- Una “primera vez”, “único”, “siempre”, “nunca” o superlativo histórico requiere especial cautela.
- Una fuente D puede describir un examen, pero no convertir una solución no oficial en ley física.
- Si una fuente de menor tier contradice a una superior, se registra el conflicto antes de decidir.

## Acceso real

En el contrato 0.3 una ficha distingue `candidate`, `accepted` y `rejected`, y el acceso al contenido: `full`, `snippet` o `metadata-only`.

Solo `accepted` + `full` + `consulted: true` puede sostener un claim. Un snippet, un resultado de buscador o una ficha de catálogo no se convierten en evidencia.

## Estado de una fuente

- `verified`: identidad y uso comprobados;
- `provided`: entregada por el usuario, todavía no auditada por completo;
- `pending`: descubierta pero no validada;
- `rejected`: no debe usarse como evidencia.

## Derechos

Registrar cuando sea posible:
- licencia;
- disponibilidad abierta;
- restricciones de reproducción;
- si solo debe citarse/parafrasearse.

El framework no asume que “encontrado en Internet” significa “libre”.
