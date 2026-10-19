# Auditoría matemática

Fecha: 18 de octubre de 2026. Alcance: reproducción aritmética, álgebra/dimensiones de modelos seleccionados y revisión de hipótesis; no validación física experimental.

## Comprobaciones completadas

- 66/66 sustituciones de los problemas y preguntas numéricas de simulacros contrastadas con SymPy a 30 cifras y aceptadas por Studium mediante reproducción del cálculo. Tolerancia de comparación 1e-10 relativa y 1e-12 absoluta.
- 24 controles adicionales de los ejemplos numéricos del manual y taller, todos reproducidos con SymPy. Los ejemplos cualitativos se revisan conceptualmente, no se disfrazan como operaciones numéricas.
- 14/14 controles dimensionales de expresiones de ejercicios, con Studium y contraste Pint.
- 5/5 derivaciones registradas y comprobadas dimensionalmente: elongación, tamaño crítico, Paris m=3, relajación y sándwich.
- 7/7 identidades, derivadas o límites aceptados en la comprobación simbólica final, incluido límite exponencial tras declarar símbolos.
- Cuatro integraciones independientes por Simpson adaptativo (P16, P17, P18 y S02.2), coincidentes con soluciones cerradas. Se registran estimaciones de error. SymPy contrasta también primitivas de potencia y logaritmo.

Los 35 problemas y 13 preguntas numéricas de simulacros se almacenan en Studium con dos fuentes de contexto distintas; el resultado de su verificación nativa es two_witnesses. Esa denominación indica contexto de evidencias y reproducción, no revisión física por dos personas ni autoridad científica automática. Las cifras de los enunciados son originales y ficticias, no proceden de esas citas.

## Errores de integración corregidos

Los primeros controles de aritmética entera fueron rechazados por falta de contexto de ejercicio; se vincularon al paso exacto del problema registrado. Un primer enlace usó una sección distinta y fue rechazado; se corrigió la sección. El primer límite no declaró lambda y quedó FAILED; la repetición con símbolos declarados fue aceptada. Los registros conservan esos intentos, sin presentarlos como éxitos. Los primeros registros con dos fragmentos de una misma fuente no bastaban para dos fuentes; se sustituyeron por referencias de contexto distintas y se repitió el control.

## Revisión física y unidades

Se revisan explícitamente a frente a 2a, KI frente a KIC, máximo frente a rango, unidad de C de Paris, horas frente a segundos, temperatura absoluta, tensión de calibración de Larson–Miller y significado de los contadores. Las comprobaciones cubren todos los problemas mediante al menos una sustitución; no todas las igualdades del manual disponen de una prueba automática individual. Las unidades que no se automatizan se razonan en el desarrollo y sus modelos.

## Limitaciones

Repetir una operación no demuestra datos auténticos, ley constitutiva adecuada, espectro representativo, condición de ensayo, POD ni aprobación de un intervalo. No se calculan extensiones reales de vida. La revisión experta independiente sigue pendiente. Registro detallado: math-checks.json, manual-math-checks.json, math-model-checks.json, evidence/derivations.json y API final.
