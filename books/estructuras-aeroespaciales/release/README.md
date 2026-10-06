# Release provenance

Antes de cerrar una edición:

```bash
aerobooks check estructuras-aeroespaciales --strict
aerobooks-ai coverage estructuras-aeroespaciales --strict
aerobooks-ai gate estructuras-aeroespaciales
aerobooks build estructuras-aeroespaciales
aerobooks-ai release-manifest estructuras-aeroespaciales --label ed3-candidate
```

El manifest SHA-256 permite verificar después el estado exacto del manuscrito y del framework.
