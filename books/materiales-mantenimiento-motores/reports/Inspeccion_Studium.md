# Inspección e integración de Studium

Commit utilizado: `675274202360f717f3b835444e26d0f95d2a3c33`. Rama main consultada; no se modificó código del framework. Proyecto nativo en `project/materiales-mantenimiento-ule`.

Se revisaron documentación de arquitectura, investigación y verificación, esquemas MCP y cambios recientes de redacción científica, unidades, comprobación y conservación de matemáticas. La integración usa API dispatch/open_workspace del commit fijado. Los registros nativos y resultados reales están en evidence y reports; no se fuerza estado RELEASED ni autoridad de fuentes.

## Pruebas del framework

Ejecución completa registrada: 1070 pasaron, 2 se omitieron por paquetes TeX catalán/gallego ausentes y 2 fallaron al iniciar procesos que no localizaron el módulo studium. El reintento dirigido con PYTHONPATH absoluto se interrumpió tras 1032,56 s sin completar pruebas. El resultado del reintento final se documenta más abajo; no se convierte el intento interrumpido en éxito. El código original permanece intacto.

Un primer intento de comprobación matemática del libro falló al importar SciPy por TimeoutError de lectura de archivos. Se conserva el registro. La cuadratura se reemplaza por Simpson adaptativo autónomo, sin requerir SciPy. Los resultados finales, si se completan, se documentan aparte; esta incidencia no se oculta.

La importación nativa utiliza fragmentos literales como anclas de localización. No se afirma que cada ancla sostenga semánticamente cada frase. Fuentes públicas quedan con su estado real; bibliografía, licencia y autoridad son aspectos diferentes. Las auditorías nativas pueden devolver bloqueos y pendientes, que no se reinterpretan como aprobación. La salida editorial LaTeX se conserva junto al proyecto.

## Reintento final resuelto

Se instaló el conjunto mínimo de dependencias fuera de la carpeta sincronizada que provocaba esperas de lectura y se fijó PYTHONPATH absoluto. Las dos pruebas afectadas pasaron: 2 passed in 2.41s, en framework-targeted-final.log. No se repitió toda la batería: el resultado conjunto se describe como 1070 aprobadas en ejecución inicial, dos adicionales aprobadas en reintento dirigido y dos omisiones por paquetes TeX ausentes. El código del framework sigue intacto.
