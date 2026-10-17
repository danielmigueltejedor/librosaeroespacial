# Correcciones de Studium detectadas al crear Motores Cohete

PR: https://github.com/danielmigueltejedor/studium/pull/77

Commit: 4bc67695b462143dab649420a7337bec053c9b23, basado en main 8bed8a52900d994e683cce7f37b565cd6caa4b15.

## Correcciones

- Evita interpretar una derivada escrita como `dh/dT` como el producto `h*T` y utilizarla como premisa.
- Conserva argumentos de funciones griegos, con subíndices o números con signo. Una definición escalar no se convierte en función por suposición.
- Los números entre delimitadores matemáticos de dólar, como `$1.08$`, se componen como matemáticas y no consumen el delimitador de la siguiente fórmula. Los precios sin pareja o separados por comas/espacios se conservan como texto.

La integral de entalpía de la incidencia #76 ahora requiere revisión cuando el lector no puede interpretarla con certeza. No se declara una demostración ni una contradicción inventada. Las integrales explícitas con un resultado realmente incorrecto siguen fallando.

## Comprobaciones ejecutadas

- 16 fallos reproducidos con main: 13 de cálculo simbólico y tres de edición matemática.
- 19 nuevas regresiones superadas con las correcciones.
- Batería completa desde una exportación limpia con los seis archivos modificados idénticos al commit: 1072 pruebas superadas, dos omitidas por paquetes LaTeX de catalán y gallego ausentes; cobertura 80,59 %.
- Ruff y Pyright satisfactorios; Pyright informa cero errores y cero advertencias.
- Párrafo real PAR-0015 de Motores Cohete: lectura sin modificar el proyecto, con resultado `not_machine_checkable`, revisión humana requerida y sin evidencia simbólica inventada.

No se modifica el código fijado dentro de los paquetes antiguos ni se cambia su estado científico. La corrección está publicada como PR; no se ha fusionado por esta tarea. El importador y su error al eliminar envolturas `aligned` ya estaban corregidos en el proyecto editorial y no se atribuyen al framework.

Tecnología Aeroespacial: retiradas las etiquetas «En revisión» de los tres PDF editoriales, actualizados los editables y los tres archivos de la carpeta Clase/TAE.
