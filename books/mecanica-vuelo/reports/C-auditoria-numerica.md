# C. Auditoría numérica

Fecha: 19 de octubre de 2026. Edición EN REVISIÓN. Revisión experta independiente pendiente.

## Pruebas y alcance
- 44/44 controles de modelos, 8/8 simbólicos adicionales.
- 151/151 controles del banco, con reproducción de sustituciones y cruces seleccionados con cuadratura, ODE, autovalores y barridos.
- 158/158 controles de talleres, simulacros y CSV. Incluyen residuos por componente de trim; ida/vuelta de rotación; mínimo exacto por raíz y optimización; refinamiento de ascenso y balances de combustible.
- 284 sustituciones vigentes aceptadas por Studium. Varias pruebas comparten ecuaciones o entradas; no se suman como testigos científicos independientes.

Los resultados completos con tolerancias y alcance están en los JSON correspondientes y en `verification-register.json`. No se han cambiado tolerancias para ocultar fallos. Se conservan scripts ejecutables.

## Experimentos realmente ejecutados
JSBSim 1.3.3; modelos en commit `66f7fafc07fe13e7ede9db20873030fed2881713`. Se guardan entradas, huellas XML, propiedades, CSV, condición de terminación y resultados.

1. T6: 44 trims sin fallo en dos masas (5600, 5850 lbm) y alturas (5000, 9000 ft), 115–215 kt CAS. EAS y TAS se leen de la salida; no se equiparan automáticamente. Ascenso por exceso de potencia desde trim horizontal: aproximación, no trim de ascenso exacto.
2. T6 libre, 60 s, dt=0.1/0.05/0.025 s: las diferencias sucesivas finales de TAS y altura disminuyen. Para el par fino son menores que 1e-4 m/s y 1e-3 m. No se calcula un orden global formal.
3. XML originales: 1200 pasos de 0.05 s realmente ejecutados; CSV de 61 muestras.
4. B747: crucero de 1800 s con control docente, masa y gasto variables. Los errores de seguimiento se conservan; no se afirma altura perfectamente constante.
5. B747: dos autonomías hasta agotar depósitos alimentadores. La comparación equivalente ajusta la misma procedencia y no es validación independiente.

Combustible inicial 12700.586360 kg; autonomía simulada 4113.000 s; gasto inicial congelado 4003.098950 s; polar equivalente 4105.333000 s; error máximo de altura 58.253 m.

Combustible inicial 16329.325320 kg; autonomía simulada 5264.400 s; gasto inicial congelado 5146.841508 s; polar equivalente 5313.604539 s; error máximo de altura 74.633 m.

## Integridad y pendientes
Cuatro CSV de trayectorias tienen tiempo estrictamente creciente, números finitos y diferencia entre integral de gasto y consumo de depósitos inferior al 2% fijado para la salida muestreada. Esto es tolerancia de auditoría numérica, no precisión de fabricante. El último paso de agotamiento y el transitorio inicial están identificados. Los dos casos de autonomía usan dt=0.1 s y NO tienen estudio completo de refinamiento temporal; sigue pendiente.

Los modelos ALPHA/BETA contienen estimaciones; el control es docente. No hay ensayo físico SAULE ni medición de vuelo real. Los datos sintéticos se identifican como tales. La instalación y las pruebas del framework arrojaron 1072 correctas y dos omitidas por paquetes de idioma ausentes, sin modificar su código.
