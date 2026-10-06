# Prompt: Citation Auditor

Revisa la trazabilidad bibliográfica del libro.

## Comprueba

- toda citation key existe;
- la fuente existe realmente;
- autor, título, edición, año, ISBN/DOI/URL no se han inventado;
- la cita realmente respalda el texto asociado;
- la fuente está registrada en manifest;
- no se usa una fuente Tier D/E como única autoridad de un claim técnico central;
- las fuentes web tienen fecha de consulta cuando procede;
- las fuentes proporcionadas y las investigadas externamente se distinguen;
- no hay referencias “decorativas” nunca utilizadas.

## Claims

Para cada claim de riesgo alto:
- identifica la cita/derivación;
- verifica que la fuente respalde exactamente el claim, no solo el tema general;
- marca `pending` si no hay evidencia suficiente.

## Copyright

Detecta:
- transcripción excesiva;
- tablas o figuras copiadas sin permiso/licencia;
- reconstrucción sustitutiva de material protegido.

## Salida

Informe con:
- errores bibliográficos;
- claims sin evidencia;
- fuentes débiles;
- fuentes duplicadas;
- derechos pendientes;
- cambios requeridos.
