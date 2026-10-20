# Revisión científica y editorial — edición v3

Fecha: 20 de octubre de 2026. Base real: `danielmigueltejedor/librosaeroespacial`, commit `7b20e20` (main tras la PR #3). Rama de trabajo: `improvement/aerospace-library-scientific-editorial-v3`.

## Cambios implementados en esta pasada

1. **Notación de turbomáquinas.** Las 18 ecuaciones modelo del manual de Turbomáquinas mostraban identificadores internos de SymPy (`uu`, `gam`, `pz`, `wt3`, `Pow`, `dTz`, `mathcalR`). Se han reescrito con la notación del apéndice. El formulario se ha rehecho con las mismas relaciones y una advertencia de notación. La tabla de símbolos corrige `$mathcalR$`, `$K_v$`, `$\phi$`, `$\psi_c$` y `$\psi_t$`, y añade la fila de $k_f$ para el vórtice forzado. Se han corregido 25 referencias textuales a `Ctheta` y 11 a `wt3` en los tres volúmenes.
2. **Portadas de Mecánica de Vuelo.** Los tres volúmenes usan ahora fotografías NASA distintas y documentadas: T-34C en maniobra para el manual, cabina del X-29 para problemas y X-29 en viraje para simulacros. La plantilla común se mantiene.
3. **Documentación obsoleta.** `books/README.md` describe ahora las siete asignaturas y veintiún volúmenes.
4. **Convenciones transversales.** Nuevo `shared/CROSS_BOOK_CONVENTIONS.md`.
5. **Pruebas y verificación.** `tests/test_turbomachinery_notation.py` y `scripts/verify-turbomachinery-headlines.py`.

## Lo que esta pasada no cierra

- No se ha revalidado semánticamente cada ecuación, figura o competencia. Los pendientes de `REMAINING-ISSUES.md` de la edición v2 siguen vigentes.
- La revisión sigue siendo del mismo modelo en una pasada nueva; no hay revisión experta independiente.
- No se ha ejecutado una compilación completa de los 21 volúmenes en esta pasada; la CI la ejecutará.

## Estado

Cambios implementados y comprobados parcialmente. No se declara certificación científica.
