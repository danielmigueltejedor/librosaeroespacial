# Revisión científica y editorial de la biblioteca STUDIUM

**Estado: cambios implementados y comprobados con alcance parcial; edición académica sin cerrar.** No hay aprobación experta independiente ni release nativo. La PR se prepara como borrador y no se fusiona.

Base real: `danielmigueltejedor/librosaeroespacial`, commit `119bc583b4f525c221f0dc815936fffbb4f770a4`. La copia incluye las incorporaciones de Materiales y Mecánica de Vuelo de main. Se trabajan siete asignaturas, veintiún volúmenes y 151 capítulos de manual; se conservan fuentes, bancos, citas, evidencias y documentos. No se recortan libros para reducir el alcance.

Se corrigen definiciones de polar, alcance temporal de Stokes, generalización del caos de tres cuerpos, estabilidad numérica de raíces de actuaciones y el caso rectilíneo del modelo de viraje. Se añaden explicaciones y un problema resuelto, controles independientes y protección de citas e identificadores.

Se unifican las dos incorporaciones con la plantilla de toda la colección. Se aplica fotografía real NASA a Vuelo y se sustituyen portadas de procedencia sin identificar por fotografías documentadas en Estructuras y Turbomáquinas. Se hacen legibles los registros concatenados en dos anexos. Las portadas conservan una retícula común y créditos comprobables.

El constructor registra entradas efectivas, huellas y resultados por documento; retira salidas antiguas antes de reconstruir y continúa tras un fallo. GitHub Actions cubre las siete asignaturas y ejecuta las comprobaciones científicas, preservación e inspección de páginas.

Los resultados concretos están en BUILD-REPORT.md, MATHEMATICAL-VERIFICATION.md, los registros JSON y los informes temáticos. Las siete guías docentes oficiales 2026/2027 están identificadas con huella y fecha. Se reejecutan las simulaciones JSBSim en una copia separada con el commit fijado, sin sustituir los CSV históricos.

La revisión no valida semánticamente cada ecuación, fuente, figura o competencia. Las limitaciones y bloqueos están enumerados en REMAINING-ISSUES.md. Que todos los PDF compilen y los controles seleccionados pasen no satisface por sí solo la aceptación científica integral.

## Reproducir

```sh
python -m pip install -r requirements-audit.txt
python scripts/build-studium-books.py all
python scripts/audit-library.py
python scripts/audit-studium-pdfs.py --output reports/edition-v2/pdf-checks.json
python scripts/inventory-library.py
python scripts/coverage-library.py
python scripts/audit-library-bibliography.py
python scripts/summarize-library-builds.py
```

La compilación requiere pdfLaTeX con español, Latin Modern, TikZ y tcolorbox. Los JPEG necesarios ya están incluidos. Las descargas fotográficas son opcionales y se registran con procedencia y huellas. Las auditorías históricas no se sobrescriben por las nuevas ejecuciones.


## Ampliación del 19 de octubre: figuras y simulación

Se inspeccionan las 358 representaciones del atlas y se modifican 97 de ellas respecto a la pasada anterior, con 141 controles científicos adicionales. Se corrigen errores confirmados de sentido, escala, potencia y representación; se completa el refinamiento de las dos autonomías con seis trayectorias hasta agotamiento. Se retiran dos portadas antiguas sin permiso identificado. Los límites académicos que siguen abiertos se especifican en REMAINING-ISSUES.md. Esta sigue siendo una integración en borrador, sin merge ni certificación general.
