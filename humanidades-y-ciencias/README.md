# Humanidades y ciencias de la vida

Tres libros escritos con Studium para comprobar cómo se comporta el framework
fuera de la ingeniería. Son **ediciones de revisión**: ninguna tiene aprobación
académica ni se declara científicamente certificada.

| Libro | Perfil Studium | Capítulos | Párrafos citados | Palabras | Fuentes | Figuras | Ejercicios | Páginas |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| [Literatura española: de la Edad Media al siglo XX](literatura-espanola/) | `HUMANITIES` | 13 | 337 | 36 000 | 218 | 86 | 90 | 188 |
| [Historia moderna de España: de los Reyes Católicos a la Guerra de Sucesión](historia-moderna-espana/) | `HUMANITIES` | 12 | 304 | 30 700 | 143 | 59 | 68 | 139 |
| [Biología celular y molecular](biologia-celular-molecular/) | `LIFE_SCIENCES` | 12 | 260 | 25 800 | 253 | 103 | 94 | 198 |

Cada disciplina tiene sus propios tipos de ejercicio (Studium elige el tipo
según el perfil del libro):

- **Literatura**: comentario de texto, análisis literario, cronologías y preguntas de desarrollo, con un fragmento citado de Wikisource.
- **Historia**: preguntas de desarrollo, comentario de fuente, cronologías, análisis de causas y consecuencias y comparaciones. Ningún ejercicio numérico.
- **Biología**: problemas numéricos propios de la biología (Nernst, Michaelis-Menten, Hardy-Weinberg, estequiometría de la fotosíntesis, PCR, χ²), más explicación de mecanismos, interpretación de datos, diseño experimental y análisis de causas.

Las figuras son diagramas TikZ con extractos que los respaldan e imágenes con
licencia abierta (dominio público, CC0, CC BY o CC BY-SA) tomadas de Wikimedia
Commons; el autor, la licencia y el enlace figuran bajo cada imagen y en la
lista de créditos de cada libro. Las imágenes se guardan reducidas (640 px). Cada figura se coloca justo después del párrafo que la explica: el párrafo la cita con una referencia y Studium dibuja la figura a continuación; `tools/place_figs.py` elige el párrafo y deja ajustes manuales en `OVERRIDES`.

## Cómo se escribieron

- Cada párrafo cita al menos dos extractos literales de fuentes distintas y
  tiene una auditoría registrada (`two_witnesses`). Eso comprueba que el
  párrafo está respaldado por dos textos; no comprueba que las fuentes sean
  correctas.
- Cada capítulo tiene un ejercicio resuelto y varios ejercicios propuestos
  con solución modelo; la respuesta de cada ejercicio cita extractos de al menos dos fuentes distintas. Varios sirven para comprobar la coherencia entre fuentes
  (por ejemplo, 350 000 moriscos expulsados frente a una población de 325 000,
  o «19 veces» frente a «15 veces» de eficiencia aeróbica).
- Cuando dos fuentes discrepan (el título de Reyes Católicos, 1494 o 1496; el
  número de bancarrotas de Felipe II; el rendimiento de ATP por glucosa) el
  libro lo dice, cita las dos y no elige sin criterio.
- Fuentes: Wikipedia en español e inglés (CC BY-SA, citada con enlace en la
  bibliografía de cada libro), el glosario del NHGRI (biología) y el texto
  original de las Capitulaciones de Santa Fe en Wikisource (historia). Todas
  se leyeron de páginas abiertas; ninguna fuente privada se subió.
- **OpenStax Biology 2e se descartó**: su página prohíbe ingerir el libro en
  sistemas de IA sin permiso escrito, así que no se usó ni se cita.
- La entrada «Célula» de Wikipedia en español tenía palabras corrompidas
  («célular», «biohazard») cuando se obtuvo; solo se citaron frases intactas y
  se añadió «Teoría celular» como fuente de apoyo.

## Reproducir

Cada carpeta es un proyecto Studium completo (extractos, párrafos, auditorías,
problemas). `tools/` contiene el código que lo generó: `engine.py` conduce el
dispatcher MCP de Studium, `*_spec.py` define fuentes y esquema, `*_ch*.py`
define los capítulos y `*_fetch.py` descarga los textos fuente. Los extractos
quedan guardados en el proyecto, así que el libro no depende de volver a
descargar las páginas.

```sh
python -m pip install -r humanidades-y-ciencias/requirements.txt
python humanidades-y-ciencias/tools/build_books.py            # los tres
python humanidades-y-ciencias/tools/build_books.py biologia-celular-molecular
```

Los PDF se generan en `dist/humanidades-y-ciencias/` y no se versionan, igual
que el resto de la colección. El catálogo `release-bundle.json` los incluye.

## Portadas

Cada libro lleva la portada compartida de la biblioteca con una fotografía de
licencia abierta, igual que los manuales de ingeniería. La fotografía, su autor,
licencia, página de origen y huella están en `<libro>/cover/cover.json`; la
compilación no necesita red. Para regenerarlas: `python humanidades-y-ciencias/tools/fetch_covers.py`.

| Libro | Imagen | Licencia |
|---|---|---|
| Literatura española | Don Quijote y Sancho Panza, monumento a Cervantes (Madrid), foto de José María Mateos | CC BY 2.0 |
| Historia moderna de España | Velázquez, *La rendición de Breda* (Museo del Prado) | Dominio público |
| Biología celular y molecular | Células endoteliales con núcleos, mitocondrias y actina, foto de Erin Rod | CC BY 4.0 |

La portada ocupa el lugar de la portada provisional, así que la paginación no cambia.
El pie de página muestra el título del libro. El estado de las fuentes sigue
documentado en el apéndice «Auditoría de fuentes» y en «Límites conocidos».

## Límites conocidos

- Las fuentes son enciclopédicas y de divulgación. Un libro que se use para
  estudiar necesita contraste con manuales y fuentes primarias; la revisión
  académica sigue pendiente.
- Los ejercicios son una propuesta de práctica con respuesta modelo respaldada
  por fuentes, no el modelo de un examen oficial. Las respuestas de comentario
  y desarrollo son una lectura posible, no la única.
- Los datos de algunos ejercicios son ilustrativos y así se dice en el
  enunciado (por ejemplo, un cruce de 160 plantas o un gel de PCR).
- Hay discrepancias entre fuentes que los libros señalan y no resuelven (por
  ejemplo, el año del descubrimiento del aparato de Golgi, 1889 o 1898, o el
  porcentaje de genomas bacterianos con CRISPR, 40 % o 50 %).
- Studium no detecta contradicciones entre dos frases en prosa; las
  discrepancias entre fuentes de estos libros se marcaron a mano.
