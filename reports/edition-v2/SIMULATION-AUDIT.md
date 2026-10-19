# Auditoría ampliada de JSBSim

Se repitieron los tres experimentos publicados con JSBSim 1.3.3 y el modelo oficial fijado al commit `66f7fafc07fe13e7ede9db20873030fed2881713`. Los recibos actuales registran fuente, versión, salida y huellas en `simulation-runs.json`; las ejecuciones se realizan en una copia aislada.

Se confirmó un error en el cálculo del empuje máximo: cambiar la orden de gas y llamar solo a `get_steady_state()` dejaba el sistema de mandos y las entradas del motor en el estado de trim anterior. En la prueba a CAS 155 kt y 5000 ft, el empuje permanecía aproximadamente en 557 lbf, en lugar de consultar el motor a plena potencia. Se actualiza ahora el ejecutivo con la integración del avión suspendida y luego se estabiliza el motor: en ese estado se obtienen aproximadamente 1896 lbf. Se comprueban gas efectivo igual a uno, N1 de plena potencia y conservación de TAS, altura y tiempo durante la consulta. La malla completa tiene 44 puntos y alimenta la figura corregida. El CSV anterior permanece expresamente en `simulations/results/historical/`.

Se completó el refinamiento de las dos autonomías hasta agotar el combustible accesible con pasos de 0,1, 0,05 y 0,025 segundos, con idéntico modelo y ley de control. `audit-endurance-convergence.py` produce seis trayectorias completas y `endurance-convergence.json` registra resultados y criterios.

| Combustible inicial | dt=0,1 s | dt=0,05 s | dt=0,025 s |
|---|---:|---:|---:|
| 28 000 lbm | 4113,000 s | 4112,950 s | 4112,950 s |
| 36 000 lbm | 5264,400 s | 5264,400 s | 5264,375 s |

La diferencia entre los dos pasos menores no supera 0,0251 s. El instante de cruce del umbral está cuantizado al paso; no se estima un orden de convergencia a partir de diferencias de ese tamaño. Se conservan la deriva de altitud y las limitaciones del ajuste analítico equivalente. La convergencia verifica el experimento numérico definido, no el consumo de una aeronave real ni una autonomía certificada. La validación experimental sigue pendiente.
