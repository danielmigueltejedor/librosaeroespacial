# Convenciones transversales de la colección STUDIUM

Este documento fija las convenciones que se repiten en las siete asignaturas. No sustituye los apéndices de notación de cada libro; los completa y evita que un símbolo se copie entre asignaturas sin convertir unidades.

## Magnitudes con nombres colisionantes

| Símbolo | Significado en el libro | Unidad | No confundir con |
|---|---|---|---|
| $K_v$ | constante de vórtice libre, $rC_\theta$ | $\mathrm{m^2\,s^{-1}}$ | $k_f$, coeficiente de vórtice forzado, en $\mathrm{s^{-1}}$ |
| $\eta_p$ | eficiencia politrópica de compresor o turbina | adimensional | rendimiento propulsivo de hélice, $\eta_p$ en actuaciones |
| $c_T$, $c_m$ | consumo específico másico por empuje | $\mathrm{kg\,N^{-1}\,s^{-1}}$ | consumo ponderal $\tilde c_T=g_0 c_T$, en $\mathrm{s^{-1}}$ |
| $C_D$, $K$ | coeficiente de arrastre y pendiente cuadrática total de la polar | adimensional | $k_{\mathrm{perfil}}$ y contribución inducida aislada |
| $e_i$, $e_O$ | eficiencia de envergadura y factor de Oswald de la polar total | adimensional | no intercambiables cuando $k_{\mathrm{perfil}}\neq 0$ |

## Signos y sistemas de referencia

- Los ángulos de Euler usan el orden declarado en cada capítulo; no se trasladan matrices entre libros sin comprobar ejes, sentido y orden.
- En turbomáquinas, $w_f$ es positivo en compresor y $w_t$ positivo en turbina; no se mezclan con el signo de la potencia de eje.
- En mecánica de vuelo, $Z_b$ positivo es hacia abajo; la sustentación positiva no coincide con $Z_b$ positivo.
- La eficiencia propulsiva ideal $\eta=2V/(V+c)$ tiene límite 1, pero su valor no se asigna en la singularidad $c=V$.

## Modelos con singularidades

- $F=P/V$ no se aplica desde $V=0$; se necesita una ley de tracción finita en el arranque.
- El centro de presión diverge cuando $C_L\to 0$ con momento finito; se usa el centro aerodinámico y un momento.
- La raíz inferior de actuaciones debe calcularse de forma estable, no por resta directa.

## Normativa

Las referencias EASA/FAA/AESA se verifican en su texto vigente en la fecha de consulta. Las publicaciones originales no demuestran por sí solas el estado vigente. Se registran fecha y fuente en cada libro.

## Separador decimal

Los libros de ingeniería escriben los decimales con punto (`9.81`, `0.5882`), tanto en prosa como en modo matemático: era la forma de la inmensa mayoría de los problemas resueltos y mezclarla con `9{,}81` dentro del mismo libro era la inconsistencia señalada en la auditoría del 22 de octubre de 2026. `scripts/unify-decimal-point.py` convierte `1{,}5` y las comas decimales de la prosa con unidad; no toca los bloques `tikzpicture` (tienen recibo de revisión visual) ni listados. Al añadir contenido, usa punto.
