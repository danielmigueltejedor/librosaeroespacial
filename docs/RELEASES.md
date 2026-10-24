# Publicación de ediciones de Libros Studium

## Versionado estable y fecha

**Una release estable se publica desde un tag `vMAJOR.MINOR.PATCH`** que apunte a
un commit ya fusionado en `main` (por ejemplo, `v1.0.0`). El workflow
`.github/workflows/release-bundle.yml` se activa automáticamente al enviar
un tag estable. También puede relanzarse manualmente indicando **ese mismo
tag ya existente**, sin publicar una versión distinta por accidente.

La release se titula **Edición DD/MM/AAAA**: día, mes y año UTC en que se
preparó la publicación del bundle, no una fecha ficticia introducida en el
nombre del tag. La versión se indica dentro de las notas y del manifiesto
`RELEASE.json`. Las etiquetas `-rc`, `-beta` o `-alpha` **no publican
automáticamente una edición estable**.

Comandos de ejemplo, **solo cuando la nueva versión esté lista**:

```bash
git switch main
git pull --ff-only origin main
git tag -a v1.0.0 -m "Primera edición estable del bundle Studium"
git push origin v1.0.0
```

El workflow impide publicar si faltan PDFs o fallan las verificaciones, y
no publica etiquetas de ramas que no estén integradas en `main`.
No se crea una release estable hasta que se ha validado el contenido concreto
del tag.

## Contenido obligatorio de CADA release

- `LibrosStudium-bundle-completo.zip`: todos los PDF registrados, agrupados
  por asignatura o tema.
- `LibrosStudium-fuentes-vX.Y.Z.tar.gz`: instantánea del código fuente del
  commit etiquetado, producida con `git archive` (no incluye archivos
  ignorados, secretos ni PDFs generados).
- `SHA256SUMS.txt`: digests SHA-256 verificables del ZIP completo, archivo
  de fuentes y metadatos.
- `RELEASE.json`: fecha y hora UTC, tag, SHA Git completo, número de
  PDF, temas y SHA-256 de los archivos.
- `NOTAS-EDICION.md`: notas de la release con el commit y los SHA-256.

GitHub muestra además sus propios **Source code (zip)** y
**Source code (tar.gz)** del commit etiquetado. Esos enlaces automáticos
son adicionales al archivo de fuentes con hash explícito.

El catálogo `release-bundle.json` contiene los manuales, cuadernos de
problemas y simulacros aeroespaciales, la colección de programación, y los
libros de humanidades y ciencias. El empaquetador compara el catálogo con
todos los proyectos de origen y exige que aparezcan todos los PDF.
Al añadir un libro hay que actualizar el catálogo y el proceso de compilación.

El ZIP contiene `INVENTARIO.json` con los hashes SHA-256 individuales,
tamaños y páginas de los PDF. **Un SHA demuestra identidad de bytes; no
certifica la exactitud científica de la edición**.

## Etapas y garantías

1. Validación de formato del tag, de su SHA Git y de su procedencia desde `main`.
2. Ejecución de tests, reconstrucción de los PDF y auditorías técnicas.
3. Compilación y verificación del ZIP completo contra `release-bundle.json`.
4. Creación del archivo de fuentes, `RELEASE.json`, notas y hashes.
5. Creación de release como **draft** y subida de todos los activos.
6. Descarga de los activos desde GitHub, `sha256sum --check` y segunda
   verificación del contenido del ZIP.
7. Promoción a release **estable y pública** solo tras superar todos los pasos.

Si una ejecución falla antes de publicar, no se anuncia una versión estable.
Una ejecución interrumpida con un draft puede relanzarse con el mismo tag;
el workflow sustituye sus activos tras reconstruirlos y revalidarlos.
Una release ya publicada **no se sobreescribe automáticamente**.

El guard `.github/workflows/release-bundle-guard.yml` revisa publicaciones
manuales. Las releases creadas con `GITHUB_TOKEN` no disparan necesariamente
un nuevo workflow, por lo que el publicador ya ejecuta las mismas
comprobaciones antes de dar publicidad al draft.

Para verificar localmente un ZIP ya compilado:

```bash
python scripts/package-release-bundle.py --verify-only
cd dist/release
sha256sum --check SHA256SUMS.txt
```

Para reconstruir la entrega hacen falta el entorno de compilación,
las dependencias de Python y LaTeX y los tres pipelines de ingeniería,
programación y humanidades.

## Estado editorial

Una versión **estable del bundle** significa que se ha empaquetado y
verificado correctamente el conjunto de archivos; **no implica** que todos
los libros hayan superado una revisión experta independiente. Los contenidos
que todavía estén `EN REVISIÓN` conservarán ese estado y no se presentan
como certificados por la ULE. Los informes de evidencia y las limitaciones
científicas no se sustituyen por un número de versión.
