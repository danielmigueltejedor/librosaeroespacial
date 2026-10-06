# Fact Check Protocol

## Objetivo

Revisar afirmaciones verificables con un método explícito. El resultado de una revisión debe poder auditarse.

## Clasificación de claims

- `scientific`
- `mathematical`
- `historical`
- `biographical`
- `numerical`
- `definition`
- `exam_pattern`
- `interpretation`
- `derived_result`

## Riesgo

### Alto
- fórmulas centrales;
- constantes;
- fechas históricas;
- atribuciones;
- límites de seguridad;
- resultados de examen;
- propiedades de materiales;
- afirmaciones absolutas;
- datos que cambian una conclusión.

### Medio
- definiciones;
- comparaciones;
- generalizaciones didácticas.

### Bajo
- transiciones;
- ejemplos puramente ilustrativos identificados como tales.

## Procedimiento

Para cada claim de riesgo alto:

1. Escribe el claim de forma atómica.
2. Identifica qué evidencia lo respaldaría.
3. Comprueba la fuente exacta.
4. Registra el ID de fuente.
5. Si es derivado, registra la derivación o ecuación.
6. Comprueba unidades y orden de magnitud.
7. Busca conflicto con otras fuentes relevantes.
8. Asigna estado:
   - `verified`
   - `derived`
   - `pending`
   - `rejected`

## Matemáticas

Una igualdad derivada debe revisarse:
- algebraicamente;
- dimensionalmente si hay magnitudes físicas;
- con condiciones de contorno cuando existan;
- con un caso simple o límite si aporta información.

## Historia

No conviertas una simplificación docente en una afirmación historiográfica. Distingue:
- fecha de invención;
- fecha de patente;
- primera demostración;
- primera publicación;
- primera aplicación operativa.

Si las fuentes usan criterios diferentes, el texto debe decirlo.

## Enlace con el manuscrito

Los claims de riesgo alto verificados o derivados deben enlazarse desde el LaTeX mediante `\claimref{CLM-...}` cuando la política del libro active `require_claim_links`.

Esto crea una cadena auditable:

```text
frase/ecuación en LaTeX
        ↓
   \claimref
        ↓
claims/ledger.jsonl
        ↓
source IDs / derivación
        ↓
sources/manifest.json
```

## Resultado de revisión

El revisor debe informar:
- claims aceptados;
- claims corregidos;
- claims pendientes;
- conflictos;
- cambios concretos necesarios.

No debe devolver “todo correcto” sin mostrar qué se verificó.
