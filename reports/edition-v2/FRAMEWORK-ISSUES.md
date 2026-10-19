# Studium: compatibilidad y límites observados

Repositorio inspeccionado: https://github.com/danielmigueltejedor/studium . Commit de main consultado: `675274202360f717f3b835444e26d0f95d2a3c33`, versión declarada `1.0.0a1`. No hay releases publicadas ni PR abiertas en la consulta. Están integradas, entre otras, las PR 77 (notación termodinámica y spans numéricos), 75 (redacción trazable y figuras Python), 74 (potencias de unidades y ejercicios multicapítulo), 73 (contratos bajo hipótesis) y 72 (auditoría y publicación de borradores).

Las importaciones conservan sus commits originales cuando los registran; no se asigna un commit inventado a Fluidos o Estructuras. Vuelo registra el commit actual en su expediente original. El inventario mantiene esta distinción. No se regeneran manuscritos a partir de un framework que no conserva toda su edición manual.

Se ejecutaron verify --full, quality-audit y scientific-contract report sobre una copia del proyecto nativo importado de Materiales. La verificación termina con código 2 y etapas no implementadas; el informe de calidad termina con código 0 porque produce diagnóstico, sin declarar que la edición esté lista. El informe de contratos tiene cero claims anotados y declara scientific_validity=not_established. No se confunde un informe vacío con aprobación.

La ausencia de implementaciones de corpus_sufficient, blueprint_accepted, authoring_complete, verification_passed, reviews_current y release es un límite observado del flujo, no una aprobación que esta tarea pueda inventar. El motor no ejecuta los cuadernos Mathematica ni establece convergencia global de JSBSim. Los estados y pruebas externos de la colección quedan separados.

No se ha modificado el repositorio principal de Studium. Esta incidencia documental queda en el repositorio de libros para evaluar una migración futura, sin abrir ni fusionar cambios en el framework desde esta tarea.
