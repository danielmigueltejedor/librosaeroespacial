# Incidencias y límites de Studium, sin cambios en su código

Revisión examinada: 08ef1f42892d6a69ad0bbde8816bc3e18fba26f7.

1. El formateador de unidades no acepta `1/s` ni exponentes fraccionarios como `K^0.5`. Se usaron `s^-1` y un paso equivalente con el cuadrado del factor crítico. Se mantuvo la dimensión original en los cálculos de gasto.
2. El verificador dimensional exige exponentes numéricos literales; una potencia dependiente de gamma se devuelve como incompleta incluso si gamma es adimensional. Se conservaron los resultados nativos y se añadieron controles con cantidades y especialización explícita de parámetros.
3. La heurística del renderizador interpreta líneas cortas de prosa que preceden a una fórmula como títulos de sección y escapa sus delimitadores matemáticos. La capa editorial compara con la estructura real y restaura esas líneas como prosa.
4. El apéndice nativo repite números de ejercicio por capítulo sin agrupar siempre las soluciones mediante su identificador completo. La capa editorial agrupa por capítulo y conserva las claves Cxx-yy-P; elimina resúmenes redundantes de los ejemplos resueltos.
5. En la API de derivadas e integrales es obligatorio declarar símbolos adicionales. Los intentos iniciales que omitieron esa declaración fallaron; se corrigieron las llamadas, no el motor. No se registra como defecto del framework.
6. Los niveles y tipos de problemas se muestran como enums en el render nativo. La capa editorial usa rótulos españoles para lectores.

La auditoría general queda bloqueada por fundamentación y revisión pendientes. No se han rellenado auditorías con opiniones del autor para simular una aprobación. No se publicaron cambios, issues ni mensajes externos durante esta tarea.
