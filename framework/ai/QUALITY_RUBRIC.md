# AeroBooks Quality Rubric

AeroBooks no usa una puntuación única para declarar que un libro es “perfecto”. Una media puede ocultar un error crítico.

La calidad se evalúa por dimensiones y por blockers.

## Dimensiones

### Q1 — Exactitud factual
- hechos;
- fechas;
- atribuciones;
- definiciones;
- cifras.

### Q2 — Exactitud científica
- hipótesis;
- leyes;
- dominio de validez;
- interpretación física;
- nomenclatura.

### Q3 — Exactitud matemática
- álgebra;
- derivaciones;
- signos;
- condiciones de contorno;
- cálculo numérico.

### Q4 — Evidencia
- fuente adecuada;
- cita suficiente;
- localizador;
- corroboración;
- conflictos.

### Q5 — Pedagogía
- prerrequisitos;
- secuencia;
- intuición;
- ejemplos;
- ejercicios;
- feedback.

### Q6 — Reproducibilidad
- metadatos;
- source manifest;
- claim ledger;
- evidence map;
- chapter specs;
- release manifest.

### Q7 — Editorial
- estructura;
- consistencia;
- figuras;
- cuadros;
- índices;
- referencias cruzadas.

### Q8 — Legal/editorial source use
- atribución;
- derechos;
- parafraseo;
- uso responsable de material protegido.

## Blockers

Bloquean una edición:
- claim de alto riesgo pendiente;
- derivación central no verificada;
- conflicto material sin resolver;
- cita inventada;
- fuente inexistente;
- error dimensional;
- figura científicamente falsa;
- revisión obligatoria ausente;
- error de compilación;
- referencia rota relevante.

## Defensa en profundidad

Ningún gate promete que el libro sea infalible. El contrato 0.3 corta el avance cuando falta una capa:

- sin fuente consultada, toca investigar;
- sin evidencia, no hay claim;
- sin verificación, no se publica el ejercicio resuelto;
- sin revisión independiente, no pasa un resultado de alto riesgo;
- con un tema fundamental en `GAP`, no se redacta el capítulo;
- con un gate en rojo, no hay release.

Una puntuación de autoridad describe la ficha. No absuelve ni condena un enunciado por sí sola.

## Regla de aprobación

Una edición es candidata cuando:
- no quedan blockers;
- los gates automáticos pasan;
- las revisiones obligatorias están en `pass`;
- el PDF se ha inspeccionado visualmente;
- las incertidumbres residuales están declaradas.
