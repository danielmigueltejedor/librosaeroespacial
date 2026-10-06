# Prompt: Claim Extractor

Extrae del manuscrito únicamente afirmaciones cuya falsedad afectaría materialmente al libro.

## Prioridad alta

- ecuaciones centrales;
- constantes;
- resultados numéricos;
- fechas;
- atribuciones;
- definiciones;
- límites de validez;
- propiedades de materiales;
- convenciones del curso;
- afirmaciones de examen;
- superlativos y absolutos.

## Atomización

Cada claim debe poder evaluarse como una sola proposición.

Malo:
> “El acero es dúctil, resistente y se usa mucho.”

Mejor:
- “El material X se modela como dúctil en el contexto Y.”
- “La propiedad Z tiene el valor … bajo …”

## Salida

Propón entradas para `claims/ledger.jsonl`:
- id;
- claim;
- type;
- risk;
- status;
- source IDs;
- derivation;
- scope;
- notes.

No marques `verified` solo porque el texto parezca correcto.
