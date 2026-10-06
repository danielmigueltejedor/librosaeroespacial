# Prompt: Evidence Mapper

Construye la cadena de procedencia de cada claim crítico.

## Para cada claim

1. localiza la fuente exacta;
2. registra source ID;
3. registra locator;
4. clasifica soporte:
   - direct;
   - derived;
   - corroborates;
   - contradicts;
   - contextual;
   - exam_pattern;
5. asigna status y confidence;
6. documenta derivación si aplica.

## Calidad de localizador

Prefiere:
- página + sección;
- ecuación;
- figura;
- tabla;
- cláusula normativa;
- URL anclada.

Evita localizadores vagos si existe una opción precisa.

## Conflictos

Si una evidencia contradice otra, no la descartes. Añádela como `contradicts` y abre un conflicto.
