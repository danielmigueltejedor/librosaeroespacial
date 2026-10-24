# MATMO — ampliación avanzada del manual y cuadernos (24-10-2026)

**Línea base:** release `librosstudium-2026-10-24-r2`, código en `main` anterior a esta rama.  
**Propósito:** ampliar la capacidad de estudiar y resolver preguntas difíciles, evitando contenido repetitivo sin aporte pedagógico.  
**Estado:** propuesta, no release aprobada; pendiente evaluación académica independiente.

## Inventario de cambios

| Documento | Refuerzo nuevo | Riesgo y validación |
|---|---|---|
| Manual | `content/profundizacion-aplicada.tex`: derivaciones y ejemplos multiaxiales, fractura, Paris, Basquin/Miner, materiales compuestos, END y mantenimiento; tres diagramas TikZ originales | Se comprueban valores numéricos mediante pruebas unitarias. Son modelos idealizados. |
| Manual | Nuevas secciones en c02, c06, c12, c13, c15, c22, c24 y c25, anteriormente fuera del refuerzo específico de la r2 | Se distingue ciencia de materiales, diagnóstico, evidencia documental y derecho aplicable. |
| Problemas | `content/problemas-avanzados-resueltos.tex`: PA01--PA06, con datos, ecuaciones, soluciones y comprobación | Ejemplos ficticios; ninguna propiedad constituye un admisible certificado. |
| Simulacros | `content/simulacros-avanzados-teoria-enunciados.tex` y `-soluciones.tex`: AT01--AT12, casos originales con rúbrica | Respuestas modelo condicionales; no son preguntas oficiales. |

## Correspondencia pedagógica con MATMO

- **Materiales:** respuesta multiaxial, tenacidad y crecimiento, curvas de fatiga y Miner, fluencia y corrosión, módulo de compuestos y selección por rigidez/resistencia, capacidad END y probabilidad de inspección.
- **Mantenimiento:** funcionalidad, consecuencias y eficacia de tareas, reparto de competencias OACI/EASA/AESA/FAA, certificados de tipo/instalación, normas de personal y organizaciones, ARC, AD, AMP, LLP, parámetros del motor, fiabilidad condicional y datos trazables.
- **Integración:** paso desde un indicio hasta técnica de inspección, aplicabilidad, decisión y documento de cierre, con ilustración propia.

El contraste de cobertura general y el reparto de evaluación provienen del informe previo `reports/Contraste_guia_docente.md` y del material docente inventariado en `reports/auditoria-fuentes-preexamen-2026-10-24.md`. La ampliación no representa una revisión línea por línea de los materiales privados.

## Derivaciones y valores que deben verificarse por código

1. **Von Mises:** plano $\sigma_x=120$, $\sigma_y=-40$, $\tau_{xy}=30\ \mathrm{MPa}$; principales 125.440 y -45.440 MPa, equivalente 153.297 MPa.
2. **Paris $m=2$:** $Y=1.05$, $\Delta\sigma=80$ MPa, $C=10^{-11}$ en unidades coherentes y $a_i=1$ mm, $a_f=4$ mm; 6.254 millones de ciclos.
3. **Compuesto:** $V_f=0.55$, $E_f=200$ GPa, $E_m=3$ GPa; $E_L=111.35$ GPa y $E_T^{\mathrm{ideal}}=6.547$ GPa; densidad 1530 kg/m3.
4. **Bayes sobre END:** prevalencia ficticia 5 %, POD 90 %, falso positivo 2 %; posterior de defecto tras negativo 0.534 %.
5. **Selección de barra:** límite de elongación gobierna en ambas alternativas, masas ideales 0.1500 y 0.15341 kg.
6. **Weibull:** $\beta=2$, $\eta=1500$ h; $R(1000)=0.64118$; supervivencia condicional de 1000 a 1100 h 0.91089.

Estas comprobaciones solo respaldan la aritmética y ciertas propiedades del manuscrito, no la validez física de cada modelo fuera de sus hipótesis.

## Fuentes abiertas y jerarquía

1. Guía docente oficial de la ULE 2026-2027, asignatura 0710341: https://guiadocenteapi.unileon.es/syllabuses/downloadPdf/2026-2027/0710341
2. MIT OpenCourseWare (Roylance), mecánica y propiedades de materiales: https://ocw.mit.edu/courses/3-11-mechanics-of-materials-fall-1999/pages/modules/
3. FAA Aviation Maintenance Technician Handbook General (edición 2023): https://www.faa.gov/regulations_policies/handbooks_manuals/aviation
4. EASA, Reglamento UE 1321/2014 y estado de reglas vigentes: https://www.easa.europa.eu/en/regulations/continuing-airworthiness
5. EASA, FAQ Airworthiness Review sobre hallazgos abiertos y anticipación de la extensión de ARC (FAQ 19050): https://www.easa.europa.eu/en/the-agency/faqs/airworthiness-review

**Precaución normativa:** la fecha de una FAQ no sustituye el reglamento; las afirmaciones aplicadas a una aeronave real requieren artículo, ámbito y fecha de aplicación, incluidas modificaciones y regímenes transitorios. Las copias antiguas de los ZIP son referencias históricas, no fuente suficiente de vigencia actual.

## Pendientes para revisión experta

- Ejecutar CI completo para los tres PDF de MATMO y la colección, inspeccionar especialmente los tres diagramas nuevos.
- Revisar de forma humana los enunciados normativos a la luz del régimen de cada aeronave y los artículos vigentes.
- Confrontar a nivel de concepto las nuevas derivaciones con la bibliografía abierta y las correcciones docentes; no se atribuye lectura de bibliografía privada no disponible.
- Mantener la release r2 intacta y no publicar la ampliación hasta completar controles y revisión.
