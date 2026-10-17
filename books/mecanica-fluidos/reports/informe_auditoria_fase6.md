# Mecánica de Fluidos — Fase 6: auditoría matemática dirigida

**Base:** `mecanica-fluidos-edicion-revisada-fase5.tex` (SHA-256 `b3f64374f2ee322c30793f11db10c0d6ffdb6b22cda251656aeb558b9ff98045`).
**Salida:** `mecanica-fluidos-edicion-revisada-fase6.tex`.
**Fecha de auditoría:** 2026-10-16.

## Hallazgo científico confirmado: máximo de L/D e interpretación de la resistencia inducida

El capítulo 7 distinguía ya correctamente `e_i` (eficiencia de envergadura) de `e_O` (factor de Oswald), pero seguía afirmando en teoría, autoficha, deducción y solución que el máximo de `L/D` se alcanza necesariamente cuando la resistencia *inducida* iguala a la resistencia *parásita*.

La polar parabólica efectiva es

\[C_D=C_{D0}+K C_L^2,\quad K=\frac{1}{\pi e_O\mathcal A}.\]

Su máximo cumple

\[\frac{d}{dC_L}\frac{C_L}{C_{D0}+KC_L^2}=0\iff KC_L^2=C_{D0}.\]

Pero el coeficiente cuadrático total puede ser

\[K=\frac{1}{\pi e_i\mathcal A}+c_{d,2}.\]

Así, `K C_L²` combina resistencia inducida con dependencia de perfil cuadrática. **La igualdad matemática es con el término cuadrático total, no necesariamente con la resistencia inducida aislada**. Solo pueden identificarse ambos cuando `c_{d,2}=0` en la parametrización considerada.

**Contraejemplo independiente:** con `C_D0=0.018`, `e_i=0.9`, `AR=9.5`, `c_d2=0.004` resulta `K_i=0.03722922645`, `K=0.04122922645`, `C_L*=0.66074466`, `K C_L*² = 0.018`, pero `C_D,i = K_i C_L*² ≈ 0.016253666` y el término cuadrático adicional es `≈0.001746334`. Es imposible que `C_D,i = C_D0` en este caso. Se han conservado los valores del ejercicio con **e_O**: no tenemos datos para separar `e_i` de `c_{d,2}` en ese ejemplo.

### Cinco pasajes corregidos

| Identificador | Localización aproximada de fase 5 | Cambio |
|---|---|---|
| F6-01 | C07 explicación de la polar | Se sustituye la falsa igualdad general por `K C_L²=C_D0` y se explicita la condición `c_d2=0`. |
| F6-02 | C07 autoficha | Se pregunta por la identidad correcta y su dominio de validez. |
| F6-03 | C07 deducción, hipótesis | Se deja de identificar automáticamente el término cuadrático con resistencia inducida. |
| F6-04 | C07 deducción, pasos | Se precisa la interpretación de la condición de estacionariedad. |
| F6-05 | C07 apéndice de soluciones | Se cambia la explicación física, conservando K, CL* y L/D máximos originales. |

## 25 comprobaciones simbólicas independientes (20 etiquetas de ecuaciones)

El script `verificaciones_simbolicas_fase6.py` ha ejecutado **25/25 pruebas** sobre expresiones seleccionadas. Incluye: derivación y óptimo de polar parabólica, separación inducida/perfil, esquiador en dos pendientes, coast-down, perfil Couette–Poiseuille y contornos, caudal plano y de tubo, oscilación del tubo en U, rendimiento propulsivo (incluido límite), exponentes de Buckingham, traza no estacionaria, presión atmosférica isoterma, vorticidad fuera de eje, flujo de película viscosa, depósito vaciándose, Venturi, modos de la serie de Couette y balance geostrófico.

**Cobertura real de esta fase:** 20 de las 158 etiquetas aparecen en alguna prueba exacta seleccionada; **138 no tienen comprobación simbólica nueva en fase 6**. Esto no significa que las 20 ecuaciones estén certificadas científicamente bajo cualquier hipótesis, ni resta valor a las verificaciones de fases anteriores. El JSON asocia cada una con la identidad efectivamente ensayada; ninguna recibe el estado `VERIFIED`.

## Integridad y límites

- **158** entornos `equation`, **230** etiquetas, **21** `includegraphics`, **30** capítulos LaTeX y **168** referencias encontradas: idénticos a fase 5 y en el mismo orden.
- Solo se han modificado los **cinco pasajes anteriores** mediante sustitución exacta; la igualdad `K C_L²=C_D0` y todos los resultados numéricos permanecen.
- No aparece «Borrador» en el LaTeX, conforme a la decisión editorial de fases anteriores.
- El libro **no** se ha compilado en PDF durante fase 6. Los recursos gráficos están en el proyecto del Mac.
- **No** se ha ejecutado Mathematica ni se ha afirmado reproducir sus resultados `NDSolve`.
- No se han contrastado en esta fase todos los problemas, derivaciones, notas bibliográficas o hipótesis físicas de las 158 ecuaciones. Sigue habiendo fuentes `PENDING`.

## Reproducción en macOS

Los scripts se ejecutan desde el directorio `latex`, con el LaTeX de fase 5 presente:

```bash
LATEX="$HOME/Developer/studium-eval/ule-fluid-mechanics-book-02-r1/workspace/mecanica-fluidos-ule/latex"
cd "$LATEX"
python3 aplicar_fase6_fluidos.py --check
python3 aplicar_fase6_fluidos.py --apply
python3 verificar_fase6_fluidos.py
"$HOME/.venvs/studium-dev/bin/python" verificaciones_simbolicas_fase6.py --json verificaciones_fase6_local.json
```

El archivo F5 no se sobrescribe. Si ya existe F6, solo se acepta si coincide exactamente. Se aborta cuando el SHA-256 de F5 o alguna de las cinco coincidencias es distinta. La compilación del libro completo debe hacerse por separado y revisando logs y figuras. **Ninguna prueba certifica que el libro esté completamente libre de errores.**
