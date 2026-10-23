# Informe de trazabilidad

Fecha de la edición: 17 de octubre de 2026. Estado: EN REVISIÓN.

La referencia académica es la guía oficial de Tecnología Aeroespacial, código 0710312, curso 2026/2027, Universidad de León. Se consultó el PDF firmado de siete páginas y su representación pública en JSON; se conservan URL, fecha, huella y datos en `evidence/public-sources.json` y `evidence/guia-consultada.json`. La guía corresponde a segundo curso, primer semestre, 6 ECTS y 150 horas (60 presenciales y 90 de trabajo autónomo). Examen escrito: 85 %; prácticas: 15 %. La realización del trabajo práctico es obligatoria para optar a la evaluación. No se inventa un umbral numérico de aprobado cuando la guía permite mínimos sin fijarlos aquí.

Los 25 capítulos son una organización editorial de los trece temas de la guía, no títulos oficiales. La correspondencia es:

| Tema de la guía | Desarrollo editorial |
|---|---|
| 1. Historia aeronáutica y espacial | 1–2 |
| 2. Atmósfera y meteorología | 3–5 |
| 3. Mecánica de fluidos | 6–8 |
| 4. Aerodinámica | 9–10 |
| 5. Mecánica del vuelo | 11–12 |
| 6. Estructuras | 16 |
| 7. Materiales | 17 |
| 8. Sistemas | 21–25 |
| 9. Motores de explosión | 18 |
| 10. Reacción y cohetes | 19–20 |
| 11. Aeropuertos | 13 |
| 12. Ayudas a la navegación | 14 |
| 13. Tecnología espacial | 15 |

## Fuentes y alcance real

Se inventariaron los cinco PDF docentes TAE y dos exámenes anteriores facilitados: nombre, páginas, caracteres extraídos y SHA-256 constan en `evidence/input-inventory.json`. TAE0 fija contexto y evaluación; TAE1 orienta la historia; TAE2, la atmósfera y meteorología; TAE3, los fundamentos de fluidos; el documento de ISA y globos orienta competencias de cálculo. Los exámenes se analizaron para identificar geometría alar, polar, equilibrio, actuaciones y relaciones atmosféricas. No se presuponen correctas sus soluciones ni se reproducen sus páginas, figuras o enunciados.

Los ejemplos, el banco P01–P30 y los ocho simulacros son nuevos (los simulacros 4 a 8 se generan con `scripts/author-technology-extra-exams.py`; sus cifras son aritmética reproducida de datos docentes, sin aprobación académica independiente). Los originales privados y sus extracciones extensas no se redistribuyen en el paquete de entrega; sus huellas permiten cotejarlos con los archivos del usuario.

Fuentes públicas descargadas y consultadas con alcance parcial, salvo la guía de siete páginas:

- **U.S. Standard Atmosphere 1976**: bases, constantes, definiciones de altura y tramos. La comprobación visual documentada abarca páginas PDF 18–20, 23–24 y 26 (paginación impresa 2–4, 7–8 y 10); no se afirma lectura integral de sus 243 páginas. Véase también `reports/fuentes-fundamentos.md`.
- **NASA Beginner’s Guide to Aeronautics**: páginas temáticas sobre sustentación, resistencia, relaciones isentrópicas, choque normal y cohetes, además de recursos históricos y orbitales identificados en la bibliografía. Contraste de hipótesis y ecuaciones concretas; no aprobación automática de toda una fuente.
- **FAA Pilot’s Handbook of Aeronautical Knowledge, FAA-H-8083-25C**: consulta temática sobre aerodinámica, vuelo, meteorología y sistemas. Se descargó el manual completo, pero no se declara una lectura de todas sus páginas.
- **FAA Airframe, FAA-H-8083-31B**: consulta temática de estructuras, materiales y sistemas hidráulicos, eléctricos, combustible y protección. El archivo tiene 1052 páginas; descarga y disponibilidad no equivalen a lectura completa.
- **FAA Powerplant, FAA-H-8083-32B**: se descargó únicamente el capítulo 1, 61 páginas. No se presenta como consulta del volumen completo.
- **Alderliesten**: se consultó la ficha bibliográfica pública. Una ficha confirma datos de la obra, no todas sus afirmaciones técnicas.
- **Leishman y demás libros recomendados**: recomendación bibliográfica; no consulta íntegra. El acceso intentado a Leishman devolvió 403. La bibliografía separa expresamente consulta y recomendación.

Las fuentes están identificadas por claves en `latex/bibliografia.tex`; las URL y huellas de las descargas aparecen en `evidence/public-sources.json`. Las 25 citas locales EVD constituyen anclas temáticas del material docente, no evidencia suficiente de cada ecuación de un capítulo. Permanecen pendientes de revisión semántica.

## Discrepancias conservadas

1. **TAE3, página 17**: las cuatro desigualdades de presión de la tabla inferior no concuerdan con el modelo subsónico/supersónico y convergente/divergente. Se aplica `dp=-rho*u*du` junto con `(M²-1)*du/u=dA/A`. Los dibujos superiores son coherentes; la discrepancia no se extiende a toda la página.
2. **Masa y peso**: cuando un dato se expresa en kg se interpreta como masa; el peso se calcula en N con la gravedad indicada.
3. **Altitudes**: el tratamiento introductorio de los apuntes se amplía distinguiendo altura geométrica, geopotencial, elipsoidal y referencias operacionales.
4. **Composición atmosférica**: un porcentaje histórico de CO₂ no se ofrece como observación de 2026.
5. **NASA Ideal Rocket Equation**: la página consultada contiene una agrupación dimensionalmente inconsistente para la velocidad equivalente. Se conserva la evidencia HTML y se utiliza `v_eq=v_e+A_e*(p_e-p_a)/mdot`. El capítulo 20 y una prueba dimensional explican la corrección.
6. La relación geométrica de retraso del cono de Mach no se clasifica como error: exige su condición de dominio temporal, explicitada en el libro.

## Recursos visuales e identidad

Las 27 figuras didácticas se generaron con programas originales; sus datos, modelos y límites están en `evidence/figures.json`. La foto provisional de portada es de NASA, lanzamiento STS-1 de Columbia, crédito EC81-15508 / S81-30459; URL y huella en `evidence/cover-image.json`. Se acredita en el manual. No se incorporó ninguna página o imagen del libro de Turbomáquinas: sólo se tomó como referencia visual de la colección.

Las rutas `sources/local` en los registros nativos señalan los originales privados de la sesión. El ZIP conserva sus registros, pero no los originales. La compilación editorial funciona con las figuras incluidas y no necesita esos documentos. Una auditoría nativa que compruebe la vigencia física de las fuentes puede requerir restaurarlos y registrar sus rutas.
