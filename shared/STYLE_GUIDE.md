# Guía editorial de Libros Aeroespacial

## 1. Ediciones

Usar siempre nomenclatura editorial:

```text
Primera edición
Segunda edición
Tercera edición
...
```

No mostrar números tipo `2.0.0` o `v3.1` en portada.

## 2. Portada

Orden recomendado:

1. volumen;
2. título;
3. subtítulo;
4. nombre o subtítulo del volumen;
5. figura técnica;
6. autor;
7. edición y fecha;
8. titulación/universidad cuando proceda.

El autor no debe repetirse en encabezados ni en páginas interiores: basta con portada, créditos y metadatos PDF.

## 3. Índices

Todos los libros deben incluir, cuando existan elementos suficientes:

- índice general;
- índice de figuras;
- índice de cuadros;
- lista de símbolos;
- índice analítico.

## 4. Figuras

Las figuras deben:

- aportar información;
- tener proporciones limpias;
- usar grosores y flechas coherentes;
- incluir `\caption{}` y `\label{}`;
- poder citarse con `\cref{}`;
- evitar decoración innecesaria.

## 5. Cuadros

Usar “Cuadro” como nombre editorial de las tablas.

Cada cuadro relevante debe tener caption y label.

## 6. Cajas didácticas

Conservar una familia pequeña y consistente:

- definición;
- resultado;
- intuición física;
- ejemplo;
- problema;
- solución;
- tip de estudio/examen;
- advertencia;
- clave de examen.

## 7. Bibliografía

Usar BibLaTeX + Biber.

Separar cuando resulte útil:

- fuentes de la asignatura;
- exámenes/material de terceros;
- recursos abiertos;
- bibliografía complementaria.

## 8. Historial

La rama `main` representa la edición en desarrollo.

Las ediciones cerradas deben etiquetarse de forma inequívoca, por ejemplo:

```text
estructuras-aeroespaciales-ed3
```

Los PDF finales deben publicarse como releases/artefactos, no mezclarse con el código fuente ordinario.
