# Estándar editorial compartido

La infraestructura compartida de la colección vive ahora en **AeroBooks**:

```text
framework/latex/
framework/ai/
framework/prompts/
framework/policies/
framework/templates/
```

Esta carpeta `shared/` se conserva únicamente para documentación editorial de alto nivel que no pertenece a un libro concreto.

La guía visual y editorial histórica sigue en:

```text
shared/STYLE_GUIDE.md
```

La implementación canónica de portada, tipografía, cajas, figuras, bibliografía e índices está en `framework/latex/`.

No copies estilos desde ediciones antiguas a nuevos libros: usa `\documentclass{aerobook}` y la plantilla de `framework/templates/book/`.
