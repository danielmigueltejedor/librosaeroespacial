# Informe de compilación — edición v3

La compilación completa de los 21 volúmenes se delega a la CI del repositorio (`.github/workflows/studium-books.yml`), que ejecuta `python3 scripts/build-studium-books.py all` y las pruebas. No se declara aquí una compilación completa ejecutada localmente.

Cambios que afectan a la compilación:
- `books/turbomaquinas/publication/turbomaquinas-ule-2026.tex`: 18 ecuaciones modelo reescritas y una sección de formulario rehecha.
- `books/mecanica-vuelo/main.tex`, `problemas.tex`, `simulacros.tex`: fotografías de portada distintas.

Pruebas locales ejecutadas:
- `python3 -m unittest tests.test_turbomachinery_notation` → 4 OK.
- `scripts/verify-turbomachinery-headlines.py` → 5/5 OK.
