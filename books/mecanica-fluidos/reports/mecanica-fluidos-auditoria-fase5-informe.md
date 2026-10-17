# Mecánica de Fluidos — Auditoría científica fase 5

**Base:** `mecanica-fluidos-edicion-revisada-fase4.tex`. **Salida:** `mecanica-fluidos-edicion-revisada-fase5.tex`.
**SHA-256 base:** `b7ca7bfc6510e2488d11a3560ce8d3b4db5bb2cf8628d21fedfd59d62f3e695c`.

## Alcance real

Revisión dirigida de hipótesis matemáticas y modelos de los capítulos 1, 5, 6, 9, 10 y 14 y de la práctica 7. No constituye comprobación exhaustiva de las 158 ecuaciones ni ejecución de Mathematica.

## Correcciones

| ID | Localización | Incidencia y reparación |
|---|---|---|
| F5-01 | C01, potencia constante | Se añade dominio $V>0$ a $F_t=P/V$, singular en reposo. |
| F5-02 | C01, dinámica | Se elimina «sea cual sea la velocidad inicial», falso para $V=0$ en el modelo ideal, y se justifica la estabilidad por $d(P/V-Mg\sin\varphi-k_DV^2)/dV=-P/V^2-2k_DV<0$ para $V>0$. Se advierte la necesidad de una ley de tracción limitada para modelar el arranque. |
| F5-03 | C05, centro de presiones | Se explicita la fórmula para superficie inclinada $h_{cp}=h_c+I_G\sin^2\theta/(h_c A)$ en profundidades verticales; se distingue de $s_{cp}=s_c+I_G/(s_c A)$ para longitudes sobre el plano. |
| F5-04 | C10, deducción de semejanza | Se corrige $U_{c2}=U_{c1}d_1/d_2$ (solo si $\nu_1=\nu_2$) por $U_{c2}=U_{c1}(\nu_2/\nu_1)(d_1/d_2)$, consistente con el resultado general posterior. |

## Comprobaciones independientes

Se han ejecutado **14 pruebas simbólicas con SymPy**:

- ✅ C01 potencia constante en dos velocidades
- ✅ C01 derivada aceleracion y monotonia
- ✅ C05 centro presiones vertical desde plano inclinado
- ✅ C06 Couette-Poiseuille segunda derivada
- ✅ C06 perfil cumplimiento placa fija
- ✅ C06 perfil cumplimiento placa movil
- ✅ C06 Hagen Poiseuille caudal
- ✅ C14 Taylor Green Navier Stokes x
- ✅ C14 Taylor Green Navier Stokes y
- ✅ C14 Taylor Green divergencia
- ✅ C10 semejanza Reynolds general
- ✅ C09 limite de Betz valor
- ✅ C09 limite de Betz punto estacionario
- ✅ M07 tension aproximada primer modo al 99%

Son pruebas de casos concretos, no una certificación científica del libro completo.

## Integridad

- Ecuaciones numeradas: 158 conservadas.
- Etiquetas `\label`: 230 conservadas.
- Capítulos `\chapter`: 30 conservados.
- Inclusiones gráficas `\includegraphics`: 21 conservadas.
- Contenido académico fuera de los cuatro pasajes: intacto.
- «Borrador»: no aparece en el `.tex` resultante.
- **PDF completo no compilado** aquí: la fuente contiene rutas a figuras que residen en el proyecto del Mac.

## Pendientes relevantes

1. Las 158 ecuaciones están inventariadas en JSON; quedan pendientes verificaciones individuales no cubiertas por los casos concretos de esta fase.
2. No se han ejecutado los siete cuadernos de Mathematica ni sus llamadas `NDSolve`.
3. Continúa pendiente una comprobación exhaustiva de unidades, modelos y resultados de todos los problemas.
4. Los estados bibliográficos `PENDING` no cambian.
5. Compilar en el proyecto original y revisar advertencias y composición gráfica.

## Compilación local posterior

```bash
BOOK="$HOME/Developer/studium-eval/ule-fluid-mechanics-book-02-r1"
LATEX="$BOOK/workspace/mecanica-fluidos-ule/latex"
cd "$LATEX"
latexmk -pdf -interaction=nonstopmode -halt-on-error -file-line-error -pdflatex='pdflatex -no-shell-escape %O %S' mecanica-fluidos-edicion-revisada-fase5.tex
mkdir -p "$BOOK/output"
cp mecanica-fluidos-edicion-revisada-fase5.pdf "$BOOK/output/"
```
