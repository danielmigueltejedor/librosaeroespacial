# Mecánica de Vuelo — Studium

Importación de la asignatura de la Universidad de León en preparación. Los volúmenes son **manual**, **problemas resueltos** y **simulacros y soluciones**.

El paquete completo de fuentes, imágenes, diagramas y scripts está preparado como `Mecanica_de_Vuelo_fuentes_para_librosaeroespacial.zip`. Hay que incorporarlo a esta carpeta antes de fusionar la rama.

Después de subir las fuentes:

```sh
python3 scripts/build-studium-books.py mecanica-vuelo --check
python3 scripts/build-studium-books.py mecanica-vuelo
```

La imagen de portada es una ilustración digital original, no una fotografía documental. El logotipo oficial de Studium se utiliza a 185 bp de ancho.
