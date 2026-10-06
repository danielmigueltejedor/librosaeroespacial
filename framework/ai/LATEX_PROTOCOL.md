# LaTeX Protocol

## Objetivo

Mantener una salida editorial coherente, accesible y compilable.

## Reglas

- No redefinir colores o cajas dentro de capítulos.
- No hardcodear el nombre del autor en el contenido.
- No hardcodear la edición fuera de los metadatos.
- Toda figura relevante debe tener `\caption{}` y `\label{}`.
- Todo cuadro relevante debe tener caption y label.
- Usar `\cref{}` para referencias cruzadas.
- No escribir números de figura a mano.
- Usar `siunitx` para magnitudes cuando sea razonable.
- No mezclar convenciones de notación sin explicarlas.
- Evitar diagramas TikZ decorativos que no aporten información.
- Las figuras técnicas deben ser legibles en escala de impresión.
- No usar espacios manuales para “arreglar” maquetación si existe una solución estructural.
- No silenciar warnings graves de LaTeX.

## Portadas

La portada es infraestructura compartida. Cada libro define metadatos y una figura técnica, no copia una portada entera.

## Compilación

La secuencia recomendada es:

```bash
aerobooks build <slug>
```

El quality gate estricto es:

```bash
aerobooks audit <slug>
```

## Errores bloqueantes

- referencias rotas;
- citas inexistentes;
- labels duplicados;
- archivos requeridos ausentes;
- manifest de fuentes inválido;
- claims verificados con fuentes inexistentes;
- fallo de compilación.
