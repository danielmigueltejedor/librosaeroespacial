# AI Orchestration

El objetivo es impedir que una sola pasada de una IA investigue, escriba, se autocorrija y se autoapruebe.

## Roles

### Source auditor
Construye el universo de evidencia.

### Outline architect
Diseña la arquitectura sin inventar contenido.

### Academic author
Redacta únicamente con fuentes/derivaciones autorizadas.

### Derivation auditor
Rehace matemáticas y cálculos.

### Scientific reviewer
Contrasta ciencia, hipótesis y validez.

### Historical reviewer
Contrasta cronología y atribuciones.

### Citation auditor
Comprueba que la cita realmente soporta el texto.

### Figure reviewer
Contrasta figuras con física/matemática.

### Pedagogical reviewer
Comprueba secuencia, carga cognitiva y aprendizaje.

### Red-team reviewer
Busca activamente errores que los demás hayan pasado por alto.

### LaTeX editor
Revisa composición sin alterar silenciosamente contenido científico.

### Release reviewer
Solo evalúa si la edición está lista para cerrarse.

## Independencia

Preferencia, de mayor a menor:
1. revisor humano experto;
2. modelo diferente;
3. nueva sesión/contexto de la misma IA con rol adversarial;
4. auto-relectura del mismo autor.

El nivel de independencia debe registrarse en cada review report.

## Handoff

Cada rol recibe un `chapter-pack` mínimo con:
- contrato;
- chapter spec;
- fuentes permitidas;
- claims;
- evidence map;
- manuscrito actual.

Esto reduce contaminación de contexto y hace más reproducible la salida.

## Prohibición

Ningún rol autor puede declarar su propio texto “aprobado”. La aprobación es una etapa distinta.
