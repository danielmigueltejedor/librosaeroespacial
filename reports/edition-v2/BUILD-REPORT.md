# Informe de compilación de toda la colección

Resultado de recibos y huellas: **PASSED**. Documentos registrados: 21.

La compilación ha ejecutado tres pasadas por volumen con pdfLaTeX, sin shell escape, y revisado los logs finales. No se deduce corrección científica de este resultado. La fecha de compilación se fija con SOURCE_DATE_EPOCH; el recibo registra el motor y las entradas realmente leídas. Los formularios, apéndices y bibliografías incluidos se generan dentro de cada volumen. No hay otros volúmenes registrados pendientes de compilación.

| Libro | PDF | Pasadas | Estado | Entradas actuales |
|---|---|---:|---|---|
| estructuras-aeroespaciales | estructuras-aeroespaciales-manual.pdf | 3 | COMPILED | Sí |
| estructuras-aeroespaciales | estructuras-aeroespaciales-problemas.pdf | 3 | COMPILED | Sí |
| estructuras-aeroespaciales | estructuras-aeroespaciales-simulacros.pdf | 3 | COMPILED | Sí |
| materiales-mantenimiento-motores | materiales-mantenimiento-motores-manual.pdf | 3 | COMPILED | Sí |
| materiales-mantenimiento-motores | materiales-mantenimiento-motores-problemas.pdf | 3 | COMPILED | Sí |
| materiales-mantenimiento-motores | materiales-mantenimiento-motores-simulacros.pdf | 3 | COMPILED | Sí |
| mecanica-fluidos | mecanica-fluidos-manual.pdf | 3 | COMPILED | Sí |
| mecanica-fluidos | mecanica-fluidos-problemas.pdf | 3 | COMPILED | Sí |
| mecanica-fluidos | mecanica-fluidos-simulacros.pdf | 3 | COMPILED | Sí |
| mecanica-vuelo | mecanica-vuelo-manual.pdf | 3 | COMPILED | Sí |
| mecanica-vuelo | mecanica-vuelo-problemas.pdf | 3 | COMPILED | Sí |
| mecanica-vuelo | mecanica-vuelo-simulacros.pdf | 3 | COMPILED | Sí |
| motores-cohete | motores-cohete-manual.pdf | 3 | COMPILED | Sí |
| motores-cohete | motores-cohete-problemas.pdf | 3 | COMPILED | Sí |
| motores-cohete | motores-cohete-simulacros.pdf | 3 | COMPILED | Sí |
| tecnologia-aeroespacial | tecnologia-aeroespacial-manual.pdf | 3 | COMPILED | Sí |
| tecnologia-aeroespacial | tecnologia-aeroespacial-problemas.pdf | 3 | COMPILED | Sí |
| tecnologia-aeroespacial | tecnologia-aeroespacial-simulacros.pdf | 3 | COMPILED | Sí |
| turbomaquinas | turbomaquinas-manual.pdf | 3 | COMPILED | Sí |
| turbomaquinas | turbomaquinas-problemas.pdf | 3 | COMPILED | Sí |
| turbomaquinas | turbomaquinas-simulacros.pdf | 3 | COMPILED | Sí |

Revisión automática de páginas: PASSED; 21 volúmenes, 2212 páginas. Comprueba texto fuera de caja, caracteres de sustitución, páginas vacías, identidad de colección, destinos internos y logs. Véase pdf-checks.json.

La inspección visual de muestras se registra por separado. El comprobador no busca semánticamente toda fórmula cortada o toda flecha incorrecta. Los logs de cada ejecución se guardan en dist/studium/<libro>/<entrada>/pass-N.log y los recibos en build-report.json; GitHub Actions los vuelve a producir.

No se promete igualdad binaria entre distintos motores y versiones. Las huellas del PDF ligan estos resultados al artefacto exacto; las de entradas detectan un informe obsoleto tras cambiar una fuente.
