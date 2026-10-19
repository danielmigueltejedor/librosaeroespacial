# B. Auditoría matemática

Fecha: 19 de octubre de 2026. Edición EN REVISIÓN. Revisión experta independiente pendiente.

## Evidencia ejecutada
`model-checks.json`: 44 controles correctos de 44. Incluye ortogonalidad, determinantes y dirección de matrices; Jacobiano de Euler y gravedad; términos de inercia cruzada y trabajo giroscópico; óptimos de polar; primitivas, Oswald, dimensiones, límites e integraciones. `additional-symbolic-checks.json`: ocho identidades correctas de ocho, entre ellas ramas a empuje fijo, trim lineal, mínimo descenso exacto y norma de cuaterniones.

Studium conserva nueve comprobaciones iniciales (seis simbólicas y tres dimensionales), diez derivaciones con unidades y cuatro contratos de afirmación. La comprobación dimensional de una derivación no certifica su desarrollo ni la correspondencia con el párrafo. Los 284 cálculos vigentes ligados a 84 problemas son sustituciones reproducidas, con historial anterior obsoleto conservado.

## Inventario y correspondencia
`equation-inventory-native.json` contiene todas las relaciones que reconoce Studium en los párrafos, paginadas hasta el final. `equation-inventory-editorial.json` identifica archivo, línea y bloque matemático de la composición LaTeX, incluidas soluciones y apéndices. No se consideran equivalentes un bloque LaTeX, una ecuación reconocida y una prueba: un bloque puede tener varias relaciones; una relación reconocida puede no ser procesable.

`model-family-register.json` declara hipótesis, singularidades y pruebas por familia. Las fórmulas individuales sin prueba ligada permanecen pendientes aunque pertenezcan a una familia comprobada.

## Diagnóstico nativo conservado
{
  "symbolically_verified": 2,
  "dimensionally_verified": 3,
  "numerically_reproduced": 1,
  "source_supported": 0,
  "follows_from_stated_premises": 2,
  "derived_steps_unchecked": 0,
  "numerically_ambiguous": 0,
  "not_machine_checkable": 244,
  "unsupported": 413,
  "contradicted": 1,
  "verification_failed": 0,
  "definition": 0,
  "approximation": 115,
  "value_or_condition": 224
}

El informe nativo reconoce 1005 relaciones y 666 afirmaciones. Sólo seis afirmaciones figuran verificadas según su vinculación exacta; no se extrapola el resultado a todas las ecuaciones. Persiste MATH-001: el lector interpreta símbolos matriciales como escalares y diagnostica formas 3×1 frente a 3×3 en una ecuación cinemática correcta. La reproducción y la incidencia están separadas en `framework-math-issue.json` y `framework-issues.md`. No se modifica la ecuación física ni se silencia el bloqueo.

## Signos, dimensiones y restricciones
Se usa Ixz con signo negativo dentro del tensor; peso W=mg; consumos másicos diferenciados de ponderales; ángulos en radianes para derivar y evaluar. Se revisaron límites de Euler, pérdida, empuje y potencia, determinante de trim, masa final positiva, dominio de raíces y denominadores. Las expresiones de ascenso aproximado y dinámica reducida llevan sus hipótesis. La auditoría no equivale a revisión experta completa de todas las deducciones.
