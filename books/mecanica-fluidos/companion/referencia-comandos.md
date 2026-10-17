# Referencia rápida de Wolfram Language para las prácticas

Sintaxis: los argumentos van entre corchetes `f[x]`, las listas entre llaves `{a, b}`, las funciones internas
empiezan por mayúscula (`Sin`, `Exp`, `Pi`, `E`, `I`). `;` al final suprime la salida. `%` es el último resultado.

| Necesito… | Orden | Ejemplo de las prácticas |
|---|---|---|
| Asignar un valor ya calculado | `x = expr` | `g0 = 9.80665` (P1) |
| Definir una función o un valor que se recalcula | `f[x_] := expr` | `pres[z_] := p0 (temp[z]/T0)^(-g0/(lapse R))` (P1) |
| Borrar definiciones | `ClearAll["Global`*"]` | primera línea de cada guion |
| Sustituir valores | `expr /. {a -> 1, b -> 2}` | `vel /. pt` (P3) |
| Derivar | `D[f, x]`, `D[f, {x, 2}]`, `f'[x]` | `D[psi, y]` (P3) |
| Integrar | `Integrate[f, {x, a, b}]`, `NIntegrate` | `NIntegrate[dens[z], {z, 0, 11000}]` (P1) |
| Simplificar con hipótesis | `Simplify[expr, cond]`, `Factor` | `Simplify[..., 0 < z < 11000]` (P1) |
| Resolver ecuaciones | `Solve[eq, x]`, `FindRoot[eq, {x, x0}]` | `FindRoot[pres[z] == p0/2, {z, 5000}]` (P1) |
| Límite | `Limit[expr, x -> Infinity]` | par del cilindro aislado (P5) |
| EDO exacta | `DSolve`, `DSolveValue` | Couette con gradiente (P5) |
| EDO / EDP numérica | `NDSolve`, `NDSolveValue` | proyectil con resistencia (P2), arranque de Couette (P7) |
| Detener la integración en un suceso | `WhenEvent[cond, accion]` | impacto del proyectil (P2) |
| Cálculo vectorial | `Grad`, `Div`, `Curl`, `Laplacian` | aceleración y vorticidad (P3) |
| Gráficas | `Plot`, `ParametricPlot`, `LogLogPlot`, `ListPlot` | atmósfera (P1), ajuste (P6) |
| Campos | `StreamPlot`, `VectorPlot`, `ContourPlot` | líneas de corriente (P3) |
| Exploración interactiva | `Manipulate[expr, {par, min, max}]` | gradiente térmico (P1) |
| Ajuste de datos | `FindFit[datos, modelo, pars, var]` | correlación Re–Ar (P6) |
| Álgebra lineal | `MatrixRank`, `NullSpace`, `.` (producto) | matriz dimensional (P6) |
| Unidades | `Quantity`, `UnitSimplify`, `DimensionalCombinations` | números adimensionales (P6) |
| Exportar | `Export["f.png", Rasterize[g, Background -> White]]` | todas las figuras |

Comprobaciones que deben acompañar a todo cálculo: dimensiones (P6), caso límite conocido (P2, P5),
ley de conservación (energía en P2, disipación en P5), comparación exacta–numérica (P4, P5, P7).
