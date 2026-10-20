# Auditoría científica — edición v3

## Incidencias confirmadas y corregidas en esta pasada

| ID | Gravedad | Libro | Error | Corrección | Prueba |
|---|---|---|---|---|---|
| SCI-TURBO-001 | MEDIUM | turbomaquinas | Las 18 ecuaciones modelo del manual mostraban identificadores internos de SymPy (`uu`, `gam`, `pz`, `wt3`, `Pow`, `dTz`, `mathcalR`) en lugar de la notación declarada en el apéndice. | Reescritura de las 18 ecuaciones con notación del apéndice y una línea de significado. | `tests/test_turbomachinery_notation.py::test_model_equation_boxes_do_not_leak_internal_identifiers`; `scripts/verify-turbomachinery-headlines.py` |
| SCI-TURBO-002 | LOW | turbomaquinas | La tabla de notación renderizaba `$mathcalR$` como texto, usaba `dimensionless` en inglés y no distinguía $K_v$ de $k_f$. | Corrección de la tabla y añadido de la fila $k_f$. | `tests/test_turbomachinery_notation.py::test_notation_table_uses_mathcal_r_and_forced_vortex_row` |
| SCI-TURBO-003 | LOW | turbomaquinas | El encabezado de la red térmica usaba $T_g$ mientras los pasos usaban $T_{aw}$. | El encabezado usa ahora $T_{aw}$, coherente con la derivación. | Inspección de la ecuación C14 |
| ED-VUELO-001 | MEDIUM | mecanica-vuelo | Los tres volúmenes compartían una sola fotografía de portada, en contra del requisito de tres fotografías distintas. | Tres fotografías NASA documentadas por volumen. | `tests/test_turbomachinery_notation.py::test_flight_covers_use_distinct_photo_files` |
| DOC-001 | LOW | colección | `books/README.md` describía cinco asignaturas y quince volúmenes. | Actualizado a siete asignaturas y veintiún volúmenes. | Inspección |

## Casos históricos A–L

Se han comprobado las correcciones acumuladas de la edición v2. No se han detectado recaídas en los textos modificados. Los casos siguen pendientes de revisión semántica completa.
