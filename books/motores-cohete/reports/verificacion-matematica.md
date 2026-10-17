# Verificación matemática

**269 controles superados** con alcance individual registrado en `science-checks.json`. No son una validación experimental ni una revisión académica integral.

- NUMERICALLY_CROSS_CHECKED: 189.
- SYMBOLICALLY_VERIFIED: 5.
- CONSERVATION_CHECK: 44.
- ALGEBRAIC_NUMERIC: 17.
- PHYSICAL_DOMAIN: 7.
- DIMENSION_AND_CONVERSION: 1.
- DOMAIN_REJECTION: 5.
- PROVENANCE_SCOPE: 1.

Se reprodujeron las sustituciones declaradas de 77 casos estructurados, más los casos M01 y M02 escritos en el manuscrito. Las rutas alternativas contrastan continuidad, energía, salto normal, integral vertical y equilibrio dinámico normalizado. No se afirma que se haya probado automáticamente cada frase ni cada ecuación del libro.

El proyecto nativo guarda cálculos ligados a revisiones de los problemas, comprobaciones dimensionales y siete derivaciones. Sus estatus describen método, no verdad física. La falta de dos testigos públicos independientes no se resuelve promoviendo los PDFs descargados a autoridad.

CEA 3.3.4: seis estados TP, conservación elemental y normalización, segunda ejecución idéntica. Se añadió un control de capacidad calorífica por diferencia centrada de entalpía en los seis estados, tolerancia relativa 3e-4, usando el mismo código y base: no es contraste independiente.

El detector nativo conserva un falso positivo de la integral de entalpía; reproducción mínima y comprobación del teorema fundamental en el paquete. [Incidencia #76](https://github.com/danielmigueltejedor/studium/issues/76).
