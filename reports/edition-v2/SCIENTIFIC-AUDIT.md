# Auditoría científica y correcciones

Fecha: 19 de octubre de 2026. Base: `119bc583b4f525c221f0dc815936fffbb4f770a4`.

Se implementan correcciones en las fuentes, modelos y materiales de estudio; las pruebas se conservan en `independent-verification.json`. El inventario incluye los siete manuales, pero la revisión científica no es exhaustiva. Los estados históricos de fuentes y ecuaciones no se convierten en nuevas aprobaciones. El revisor es el mismo modelo en una nueva pasada de cálculo, sin revisión experta independiente.

| ID | Gravedad | Libro | Error confirmado | Corrección y prueba |
|---|---|---|---|---|
| SCI-001 | HIGH | mecanica-fluidos | K aparecía como factor de resistencia inducida a pesar de que la teoría reconoce contribuciones de perfil. | Se denomina coeficiente cuadrático total; se conserva el valor numérico. Prueba: A-polar-stationarity; A-Oswald-distinction. |
| SCI-002 | HIGH | mecanica-fluidos | Re pequeño se usaba para descartar toda la inercia sin condición temporal. | Se distingue convección de aceleración local y se añade un problema resuelto de difusión oscilatoria. Prueba: D-unsteady-Stokes-PDE; D-Re-does-not-bound-time. |
| SCI-003 | MEDIUM | mecanica-fluidos | Se atribuía caos a la mayoría de condiciones sin definir una medida y se generalizaba la evolución de Lorenz. | Se retira la generalización; se incorpora una referencia primaria y una comprobación independiente de movimiento regular. Prueba: FLUID-three-body-regular-motion; fuente arXiv math/0011268. |
| NUM-001 | MEDIUM | tecnologia-aeroespacial | La resta T-sqrt(T²-4AB) puede perder todas las cifras de la raíz inferior. | Racionalización, discriminante escalado y dominio finito positivo; ejemplo que distingue prueba numérica de avión físicamente realizable. Prueba: TECH-stable-lower-speed; TECH-thrust-domain-*; referencia Decimal de 70 cifras. |
| NUM-002 | LOW | mecanica-vuelo | El código dividía por cero para alabeo cero, aunque el manual explica el límite rectilíneo. | Se devuelve radio infinito, tasa nula y n=1; se rechazan rapidez o alabeo inválidos. Prueba: I-zero-bank-limit. |

`confirmed-issues.json` contiene para cada incidencia archivo, ubicación, evidencia, corrección, prueba y estado final, incluidos problemas editoriales y de compilación. No se ha detectado un error en una ecuación solo porque Studium no pueda procesarla.

Los casos históricos A–I se ejercitan con optimización de polar, integrabilidad de presión, semejanza con viscosidades distintas, difusión oscilatoria, singularidades de rendimiento y potencia, balance energético, centro de presión inclinado y rotaciones pasivas. Las pruebas no pretenden revisar todas sus aplicaciones en todos los ejercicios. J se comprueba de forma específica en los simulacros de Estructuras; K mediante conservación de citas e identificadores; L con logs y páginas de los PDF.
