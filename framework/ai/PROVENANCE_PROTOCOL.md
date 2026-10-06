# Provenance Protocol

AeroBooks trata la procedencia como parte del contenido académico.

## Cadena deseada

```text
frase / ecuación / dato
        ↓
claim ID
        ↓
evidence ID
        ↓
source ID + locator
        ↓
fuente registrada
```

No todos los párrafos necesitan un claim ID, pero todo contenido de alto riesgo debe poder reconstruirse mediante esta cadena.

## Tipos de procedencia

### Direct
La fuente afirma sustancialmente el mismo hecho.

### Derived
El resultado se obtiene de forma reproducible a partir de ecuaciones o datos declarados.

### Corroborates
Una fuente independiente confirma un claim ya respaldado.

### Contradicts
La fuente entra en conflicto con otra evidencia. Debe registrarse.

### Contextual
La fuente aporta contexto, no prueba directa.

### Exam pattern
La fuente solo informa sobre estilo, formato o tipo de ejercicio de examen.

## Localizadores

Siempre que sea posible usar un localizador preciso:
- página;
- sección;
- ecuación;
- figura;
- tabla;
- capítulo;
- URL anclada;
- identificador normativo.

“Está en el libro X” no es suficiente para un claim crítico cuando puede darse una ubicación mejor.

## Derivaciones

Una derivación debe especificar:
- hipótesis;
- ecuación de partida;
- pasos esenciales;
- condiciones de contorno;
- unidades;
- verificación independiente.

## Conflictos

No se borra la evidencia discrepante. Se registra en `sources/conflicts.jsonl` y se documenta la resolución.

## Regla de edición

Cuando cambie una fuente o una derivación que respalda un claim crítico, ese claim debe volver a revisión.
