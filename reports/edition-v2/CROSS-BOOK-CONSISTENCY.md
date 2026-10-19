# Coherencia transversal

| Concepto | Documentos | Comprobación ejecutada | Resultado y límite |
|---|---|---|---|
| Atmósfera | Tecnología y Vuelo | Dos implementaciones a 0, 2.5, 11, 15 y 20 km geopotenciales | Coinciden T, p, rho y sonido; no contraste meteorológico |
| Polar y resistencia | Fluidos, Tecnología y Vuelo | Óptimo total simbólico y evaluación a tres velocidades | K total distinto de contribución inducida; corrección de dos definiciones en Fluidos |
| Masa frente a peso | Tecnología y Vuelo | Conversión explícita W=m g antes de comparar fuerzas | Coincidencia numérica; no se unifica notación por sustitución mecánica |
| Energía y potencia | Fluidos, Tecnología, Vuelo y Cohete | Potencia de tracción y balances; singularidad P/V | El modelo necesita V>0 y un cierre distinto para arrancar |
| Trabajo de turbomáquina | Turbomáquinas y Cohete | Omega por cambio de momento angular; balance de tobera | Trabajo hacia el fluido y potencia extraída llevan signos distintos por convenio |
| Elasticidad y fractura | Estructuras y Materiales | Solución de viga, Castigliano, unidades y ley de Paris | Son comprobaciones de modelos diferentes, no equivalencia de vida y desplazamiento |
| Referencias | Fluidos y Vuelo | Rotación NED→cuerpo y balance de aceleración | No mezclar componentes de sistemas distintos |

Las comprobaciones se localizan por IDs `CROSS-*`, `A-*`, `F-*`, `I-*`, `STRUCT-*`, `TURBO-*` y `ROCKET-*` en `independent-verification.json`. En Tecnología se distingue consumo másico por empuje de consumo por peso; en Vuelo el consumo `cT` se expresa por masa. No se cambia una fórmula que utiliza otra definición sin convertir también las unidades.

No se ha hecho una demostración semántica de coherencia de cada frase, figura o aplicación de los siete manuales. El registro de cobertura no cierra esa revisión. Las contradicciones confirmadas y corregidas se distinguen de las áreas pendientes.


## Ampliación: figuras y auditorías pendientes

La pasada de figuras usa las mismas relaciones L cos(phi)=W, L=W cos(gamma), D=−W sin(gamma), presión normal desde el agua hacia la pared y flujo que suma el cortante. Mohr declara su ordenada y distingue máximo xy de máximo 3D. Cohete distingue potencia de energía; las gráficas de vuelo separan kN y kW.
