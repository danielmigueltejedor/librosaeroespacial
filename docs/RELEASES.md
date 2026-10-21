# Publicaciones de Libros Studium

Toda nueva publicación, incluso una revisión de un único libro, debe adjuntar
`LibrosStudium-bundle-completo.zip`. No basta con el ZIP automático de GitHub
(código fuente) ni con un paquete parcial de una asignatura.

El catálogo `release-bundle.json` contiene todos los documentos registrados:
manual, problemas y simulacros de cada asignatura, los diez volúmenes de
programación y su edición integral. Al añadir una asignatura se debe actualizar
el catálogo; la comprobación compara ambos inventarios y rechaza omisiones.

El ZIP contiene una subcarpeta por asignatura o tema. `programacion/volumenes/`
agrupa las monografías y `programacion/Enciclopedia-integral.pdf` la colección
unida. `INVENTARIO.json` conserva páginas, tamaño, SHA-256 y procedencia de cada
PDF. Es un inventario de entrega, no un cierre o aprobación académica.

Usar el flujo **Publish complete library bundle**, indicando una etiqueta nueva.
Compila toda la colección, comprueba y reabre el ZIP, crea una publicación en
borrador, sube el paquete completo y solo entonces publica. Ante un error no se
publica. Las ediciones de programación siguen marcadas como revisión.

Para preparar una entrega manual:

```sh
python scripts/build-studium-books.py all
python enciclopedia-programacion/tools/build_collection.py all --review-copy
python scripts/package-release-bundle.py
python scripts/package-release-bundle.py --verify-only
```

No publicar solo archivos sueltos. Si se reutilizan PDF ya publicados, el
argumento `--provenance` debe identificar su etiqueta y hash; no atribuirlos a una
compilación nueva. Las ediciones históricas conservan su contenido original.
El administrador puede publicar manualmente fuera de GitHub Actions; esta
política no sustituye las restricciones de acceso de GitHub.

El guard `release-bundle-guard.yml` revisa también las publicaciones manuales:
si no puede descargar y validar el paquete completo contra el catálogo vigente,
devuelve la publicación a borrador y deja el trabajo en error. La política y el verificador deben
fusionarse en la rama predeterminada para que el guard aplique sus comprobaciones. Las publicaciones
creadas por el token de Actions no disparan otro flujo; el publicador comprueba
por sí mismo el ZIP descargado antes de publicar.

El evento de publicación puede cargar un workflow desde la etiqueta antes de
que la PR esté fusionada. Por eso el guard detecta si la política aún no ha
existido en la historia de la rama predeterminada: únicamente en esa primera
instalación omite su actuación para una edición en revisión. El publicador
sigue comprobando el ZIP descargado. Si la política ya existió y desaparece
o queda incompleta, el control sigue siendo obligatorio y falla de forma
visible. Se comprueba esa diferencia con repositorios Git temporales.
