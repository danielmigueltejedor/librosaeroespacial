# Humanidades y ciencias de la vida

Tres libros escritos con Studium para comprobar cómo se comporta el framework
fuera de la ingeniería. Son **ediciones de revisión**: ninguna tiene aprobación
académica ni se declara científicamente certificada.

| Libro | Perfil Studium | Capítulos | Párrafos citados | Fuentes | Páginas |
| --- | --- | --- | --- | --- | --- |
| [Literatura española: de la Edad Media al Siglo de Oro](literatura-espanola/) | `HUMANITIES` | 7 | 81 | 29 | 31 |
| [Historia moderna de España: de los Reyes Católicos a la Guerra de Sucesión](historia-moderna-espana/) | `HUMANITIES` | 6 | 82 | 41 | 28 |
| [Biología celular y molecular](biologia-celular-molecular/) | `LIFE_SCIENCES` | 6 | 70 | 38 | 28 |

## Cómo se escribieron

- Cada párrafo cita al menos dos extractos literales de fuentes distintas y
  tiene una auditoría registrada (`two_witnesses`). Eso comprueba que el
  párrafo está respaldado por dos textos; no comprueba que las fuentes sean
  correctas.
- Cada capítulo tiene un problema resuelto numérico con su resultado
  recalculado. Varios sirven para comprobar la coherencia entre fuentes
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

## Límites conocidos

- Las fuentes son enciclopédicas y de divulgación. Un libro que se use para
  estudiar necesita contraste con manuales y fuentes primarias; la revisión
  académica sigue pendiente.
- Los problemas son aritmética y comprobaciones de coherencia, no el modelo de
  problemas de un examen de la materia.
- Studium no detecta contradicciones entre dos frases en prosa; las
  discrepancias entre fuentes de estos libros se marcaron a mano.
