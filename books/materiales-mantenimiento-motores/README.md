# Materiales y Mantenimiento de Motores Aeroespaciales

**Estado de esta rama: importación pendiente de fuentes.**

El proyecto Studium completo ha sido depurado para excluir copias privadas de apuntes y normativa, caches y dependencias vendorizadas. Las fuentes editables y los recursos deben colocarse aquí a partir de `Materiales_Mantenimiento_Motores_para_librosaeroespacial.zip`.

Una vez añadidos los archivos, desde la raíz del repositorio:

```bash
python3 scripts/build-studium-books.py materiales-mantenimiento-motores --check
python3 scripts/build-studium-books.py materiales-mantenimiento-motores
```

Se esperan tres volúmenes (manual: 108 páginas; problemas: 39; simulacros: 20) según la compilación local. Publicar los PDF en artefactos o releases, no versionarlos. El proyecto está **EN REVISIÓN**; el gate de auditoría del framework no ha aprobado su publicación académica.
