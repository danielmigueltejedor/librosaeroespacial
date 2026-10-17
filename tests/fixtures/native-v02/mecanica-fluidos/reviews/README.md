# Review reports

Guarda aquí informes materialmente relevantes para una edición.

Roles recomendados:

- source;
- outline;
- scientific;
- mathematical;
- historical;
- citation;
- latex;
- release.

Genera el contexto de un revisor con:

```bash
aerobooks review-pack <slug> scientific
aerobooks review-pack <slug> mathematical
aerobooks review-pack <slug> historical
aerobooks review-pack <slug> citation
aerobooks review-pack <slug> latex
aerobooks review-pack <slug> release
```

Los contextos generados van a `build/reviews/` y no se versionan. Los informes finales que justifiquen una edición sí pueden guardarse aquí.
