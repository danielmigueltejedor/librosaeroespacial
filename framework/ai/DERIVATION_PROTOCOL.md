# Derivation Protocol

Toda derivación importante debe poder ser reproducida por una persona o por una IA revisora que no confíe en el resultado anterior.

## Ledger

En el contrato 0.3 cada derivación vive en `derivations/ledger.jsonl`: identificador, hipótesis, ecuaciones de partida, pasos, resultado, fuentes, análisis dimensional, condiciones, casos límite, revisor y estado. Una derivación fundamental queda en `audited` solo con revisor independiente (`independent_model`, `human` o `hybrid`). `dimensional_status: fail` bloquea el gate.

## Contrato mínimo

1. declarar hipótesis;
2. declarar variables y unidades;
3. escribir la ecuación de partida;
4. justificar cada transformación no trivial;
5. conservar signos y orientación;
6. indicar aproximaciones;
7. verificar dimensiones;
8. comprobar condiciones iniciales/de contorno;
9. probar un caso límite o un caso simple cuando sea útil;
10. recalcular el resultado por una ruta independiente si es de alto riesgo.

## Igualdad frente a aproximación

No escribir `=` cuando se usa:
- linealización;
- pequeña perturbación;
- redondeo;
- hipótesis asintótica;
- ajuste empírico.

Usar `\approx`, `\simeq` o explicar explícitamente el error.

## Resultados numéricos

Para cada resultado:
- unidades coherentes;
- cifras significativas razonables;
- orden de magnitud;
- signo físico;
- sensibilidad básica si el resultado depende fuertemente de un dato.

## Revisión independiente

El revisor matemático no debe usar la solución como premisa. Debe volver a resolver desde los datos de entrada.

## Registro

Los resultados de alto riesgo se registran como claim `derived` y su evidencia usa `support=derived`.
