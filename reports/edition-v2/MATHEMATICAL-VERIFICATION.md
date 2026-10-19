# Verificación matemática reproducible

La batería nueva ejecutó **125 controles**, con 0 fallos. El registro por control contiene identificador, asignatura, localizador, ecuación, procedimiento, resultado, hipótesis, límites, herramienta y estado. La batería recorre modelos seleccionados de las siete disciplinas y todas las sustituciones del banco editorial de Materiales.

- `ARITHMETIC_REPLAYED`: se vuelve a evaluar una expresión o comparar algoritmos numéricos; no prueba la hipótesis física.
- `SYMBOLICALLY_CHECKED`: se simplifica un residuo exacto bajo condiciones declaradas.
- `DIMENSIONALLY_CHECKED`: Pint compara dimensiones antes de sustituir cantidades.
- `ASSUMPTIONS_REVIEWED`: se ejercita un dominio de entrada, sin afirmar que un experimento real lo satisfaga.
- `PHYSICALLY_CONSISTENT`: balances seleccionados dentro del modelo ideal declarado.
- `NUMERICALLY_CONVERGED`: contraste concreto entre cuadratura y primitiva; no convergencia global de todas las simulaciones.
- `PENDING_EXPERT_REVIEW`: permanece para todos los controles; no hay aprobación académica independiente.

Estos son estados externos. Studium mantiene su vocabulario nativo, entre otros `SYMBOLICALLY_VERIFIED`, `DIMENSIONALLY_VERIFIED`, `MODEL_CONSISTENT_UNDER_ASSUMPTIONS` y revisión experta pendiente. No se añade un estado nativo universal VERIFIED.

La raíz inferior de actuaciones se compara con Decimal de 70 cifras y con la sustitución de ambas velocidades en la resistencia. El flujo oscilatorio se introduce como solución y se sustituye en su EDP; el centro de presión se obtiene integrando fuerza y momento. La viga en voladizo se contrasta mediante condiciones de contorno y energía. Las toberas se contrastan mediante flujos de masa y energía; no basta con repetir un número del libro.

Se ejecutan además las auditorías anteriores mediante `audit-library.py`; resultados y límites por tarea en `audit-runs.json`. Los controles de Estructuras (405), Turbomáquinas (674), banco de Fluidos (329), Motores Cohete (269) y Vuelo conservan su alcance original. No se suman como si fueran pruebas científicas independientes de todas las afirmaciones.

El registro `equation-register.json` localiza los bloques matemáticos de los documentos, incluidos apéndices y soluciones. Los bloques aún sin una vinculación semántica individual permanecen pendientes. Localizar un bloque o un label no equivale a verificarlo.

```sh
python -m pip install -r requirements-audit.txt
python scripts/audit-library.py
```


## Ampliación: figuras y auditorías pendientes

La ampliación añade 141 controles de figuras ligados a sus fuentes, además de los 125 controles seleccionados anteriores: tensor y geometría de Mohr, balances y momentos, series/condiciones de contorno, tablas y 44 estados de plena potencia. Las seis trayectorias de agotamiento usan tres pasos. Los resultados detallados están en figure-science-checks.json y endurance-convergence.json.
