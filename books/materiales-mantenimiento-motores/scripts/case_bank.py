"""Casos originales de estudio. No autorizaciones ni expedientes reales."""
from pathlib import Path
import json
R=Path(__file__).resolve().parents[1]
CASES=[]
def case(key,title,situation,docs,norm,analysis,result,limits):CASES.append(dict(key=key,title=title,situation=situation,docs=docs,date='18 de octubre de 2026',norm=norm,analysis=analysis,result=result,limits=limits))
case('C01','Elegir Parte M o Parte ML','Se comparan dos aviones ficticios no complejos de2200kg. El primero se usa privadamente; el segundo figura en el AOC de una compañía aérea con licencia del Reglamento1008/2008.','Datos académicos de masa,complejidad,matrícula y tipo de operación. No hay programa ni certificado real.','1321/2014,artículo3.1–3.3,consolidación7agosto2026.',
 'Se comprueban ámbito,características y operación. La masa coincide con una categoría de3.2,pero el segundo párrafo introduce la condición de AOC y compañía con licencia. La respuesta debe mencionar ambas condiciones,no solo masa.',
 'Bajo las hipótesis del caso,el primero se analiza por Parte ML y el segundo por Parte M. No se deduce de ello automáticamente quién puede mantenerlo o qué organización necesita:esas preguntas requieren su propio análisis.',
 'La conclusión depende de que los datos ficticios de complejidad,operación y ámbito estén completos; no clasifica ninguna aeronave real.')
case('C02','Revisión de manual y configuración','Una orden de trabajo académica utilizó una revisión de un manual que no corresponde al estado de modificación de la pieza. La tarea aparece marcada como terminada.','Orden,identidad de componente,registro de modificación y dos revisiones de datos ficticios.','1321/2014,145.A.45 y145.A.50;748/2012,21.A.7.',
 'Se identifica qué instrucción era aplicable,qué diferencias técnicas existen y qué se realizó realmente. Se documenta la discrepancia,se evita tratar la casilla de cierre como prueba suficiente y se remite la evaluación al procedimiento competente. Se estudia la causa de selección de la copia incorrecta.',
 'El estado académico es pendiente de evaluación y corrección documentada. Cambiar la referencia escrita sin evaluar el trabajo no acredita conformidad.',
 'Sin datos de mantenimiento no se prescribe repetir un paso,desmontar ni liberar el componente.')
case('C03','CRS y ARC','Tras una tarea ficticia se ha emitido un CRS. El propietario piensa que con ello empieza automáticamente un nuevo periodo de ARC.','Certificado de tarea,fecha de ARC y configuración académicos.','1321/2014,145.A.50 yM.A.901–903,consolidación20260807.',
 'Se separa la certificación del mantenimiento ordenado de la revisión de aeronavegabilidad. Se identifican organización,privilegios y documentos requeridos para cada proceso. El CRS se incorpora como evidencia pertinente,pero no se transforma en ARC.',
 'No hay renovación automática del ARC por el solo CRS. Debe analizarse el proceso de revisión y sus condiciones.',
 'No se determina la validez de un ARC real ni se presupone que una revisión ya esté completada.')
case('C04','Graduado y personal certificador','Una persona ficticia posee un grado universitario y ha cursado materiales y mantenimiento. Se le pide firmar un CRS de tareas en aeronave.','Título académico y experiencia de laboratorio,pero sin licencia,habilitación ni autorización acreditadas.','1321/2014,66.A.20,.25,.30,.45 y145.A.35.',
 'Se identifica tarea y régimen. Se comprueban licencia,categoría,limitaciones,habilitación,experiencia y autorización organizativa. Los posibles créditos o rutas para titulados se estudian en su disposición concreta,no se inventa equivalencia total.',
 'Con la documentación dada no se demuestra capacidad reglamentaria para emitir ese CRS. Se produce un mapa de requisitos pendientes,sin atribuir una denegación administrativa al ejercicio.',
 'La formación académica puede ser relevante; el caso no evalúa un expediente personal real ni sustituye a la autoridad.')
case('C05','Una hoja de AD no es una búsqueda completa','Un estudiante recibe la hoja aportada de TB20 y concluye que todas las AD del motor están incluidas porque hay una columna de modelo.','Hoja histórica proporcionada,con identificadores,asuntos y estadoCurrent de la exportación.','748/2012,21.A.3B;1321/2014,M.A.303; fuente original de cadaAD.',
 'Se revisan objeto y clasificación. La hoja se organiza por modelos de aeronave y no demuestra exhaustividad para motor,hélice y componentes. Se identifica cada producto instalado y se consulta la autoridad y base pertinentes con fecha de corte.',
 'Se conserva la hoja como índice de candidatos y queda pendiente una búsqueda por productos y componentes. No se declara cumplida una flota a partir de la exportación.',
 'La obra no aporta una lista actualizada completa de AD para ningún modelo real.')
case('C06','Vida de una pieza trasladada','Un componente LLP ficticio pasa de un motor a otro. Su historial anterior suma1650ciclos y la vida académica total es2200. El segundo motor tiene900ciclos propios.','Tarjeta de pieza e instalación ficticias; identidadP/NyS/Nconfirmada.',
 '1321/2014,M.A.305 y reglas de control de vida aplicables al producto; límite numérico creado para el ejercicio.',
 'Se conserva el total de la pieza. Los900ciclos del receptor no reemplazan ni reinician el contador del LLP. Si se asume que desde instalarlo se añaden40ciclos de la definición aplicable,el total de la pieza pasa a1690.',
 'Margen inicial550ciclos; tras40nuevos,margen510. Se documenta instalación y acumulación por eventos.',
 'La definición real de ciclo y las posibles reglas de contabilización deben proceder de datos aplicables. El límite2200es ficticio.')
case('C07','Modificar un intervalo del programa','Un indicador de fiabilidad mejora y se propone ampliar por decisión interna un intervalo que procede de una limitación de aeronavegabilidad.','Gráfico académico de eventos,lista de tareas y referenciaALSsupuestas.','1321/2014,M.A.302(d)–(h);datos de limitaciones aplicables.',
 'Se rastrea la fuente de la tarea y el tipo de obligación. La mejoría estadística no elimina una limitación ni sustituye el proceso de modificación y aprobación que corresponda. Se comprueba que el indicador mide el modo de fallo relevante.',
 'No se autoriza una ampliación por la sola tendencia. La propuesta se mantiene como estudio pendiente de la vía técnica y reglamentaria aplicable.',
 'No se emite una regla universal de escalado ni una tolerancia numérica.')
case('C08','MEL y datos de reparación','Un equipo ficticio presenta una anomalía. Un estudiante busca un procedimiento de reparación en la MEL y afirma que cualquier elemento listado puede quedar diferido.','Extracto académico deMEL,configuración y descripción incompleta del fallo.','Régimen operacional yMELaplicable;1321/2014,M.A.403;datos de mantenimiento. No se fija una disposición operacional concreta sin el escenario completo.',
 'Se distingue autorización de despacho bajo condiciones de la instrucción técnica de reparación. Se comprueban sistema exacto,fallo,condiciones,procedimientos y límites del documento aplicable. Una entrada de MEL no cubre automáticamente cualquier fallo de ese sistema.',
 'Se requiere completar datos y usar el procedimiento correspondiente. No puede cerrarse la reparación con la MEL ni diferirse por simple semejanza del nombre.',
 'La norma operacional yMELreales no se han proporcionado; esa parte queda expresamente pendiente.')
case('C09','Reconocimiento civil–militar','Un taller civil propone ejecutar y certificar una tarea en una aeronave militar derivada de un tipo civil porque dispone de experiencia con el modelo.','Certificado civil de organización y solicitud militar ficticios,sin documento de reconocimiento.','2018/1139,artículo2;RD866/2015;marco militar y reconocimiento aplicables;EDA/MAWAcomo contexto de armonización.',
 'Se identifica autoridad militar,configuración,datos de tarea y alcance de aprobación o reconocimiento. La similitud técnica no demuestra validez jurídica de la aprobación para esa tarea militar.',
 'La aceptación y certificación quedan pendientes de comprobar el marco aplicable. Se separa capacidad técnica potencial de autorización.',
 'No se asume reconocimiento automático de licencias u organizaciones por existir EMAR.')
case('C10','Fecha de aplicación de una modificación','Un resumen de2025describe revisiónARC. En octubre2026se pretende utilizarlo sin consultar cambios posteriores.','EARde septiembre2025,consolidación1321/2014deagosto2026 yReglamento2026/100 descargados.',
 '2026/100,artículo4;1321/2014,M.A.901–903.',
 'Se compara fecha documental,entrada en vigor y aplicación. El artículo4fija aplicación general desde7agosto2026y excepciones concretas. Se lee el punto de la consolidación actual en lugar de conservar automáticamente numeración antigua.',
 'La explicación académica se actualiza aM.A.901yM.A.903vigentes en la fecha de corte; el resumen2025queda como referencia histórica parcial.',
 'El caso no demuestra que todo el contenido de cualquierEAR2025sea obsoleto:se analiza la disposición concreta.')
case('C11','Daño fuera de límites de un manual','Una indicación ficticia está fuera de los límites de reparación de la instrucción disponible. El material propuesto como parche tiene mayor resistencia nominal.','Identidad y medida de daño académicas,extracto de datos y ficha nominal sin base de reparación.','1321/2014,M.A.304 y145.A.45;748/2012,Parte21según ruta de diseño de reparación.',
 'Se conserva la discrepancia y se solicita el dato de reparación adecuado o la evaluación correspondiente. Se consideran geometría,fatiga,corrosión,uniones y compatibilidad. Mayor resistencia nominal no demuestra equivalencia ni conformidad.',
 'La documentación proporcionada no permite definir ni autorizar la reparación. Se entrega una lista concreta de información necesaria.',
 'No se propone material,espesor,adhesivo ni proceso para una pieza real.')
case('C12','Inspección sin indicaciones','Un informe ficticio de penetrantes no encuentra indicaciones y se concluye que no existen defectos internos ni riesgo de fatiga.','Informe de penetrantes con superficie y cobertura definidas; sin otra inspección.','Datos de inspección y criterios del producto; fundamentos deENDdel capítulo11.',
 'Se identifica la capacidad del método:discontinuidades abiertas a una superficie compatible. Se comprueba cobertura y sensibilidad. Una grieta interna o una orientación no examinada no se excluye por este resultado.',
 'La conclusión se limita a la inspección ejecutada y sus condiciones. No se afirma ausencia de todo daño ni vida infinita.',
 'La selección de técnicas adicionales y aceptación real requiere los datos y autoridad técnica aplicables.')
case('C13','Repuesto con documento pero sin compatibilidad','Un componente ficticio tiene documento de liberación,pero no se ha demostrado que su configuración sea elegible para la instalación prevista.','Documento de liberación,IPCde la aeronave y registro de modificación incompleto.',
 '1321/2014,145.A.42,.45 y.50;datos de elegibilidad/configuración del producto.',
 'Se verifica identidad,estado,alcance del documento y compatibilidad con la instalación. Se contrastaP/N,modificaciónycondiciones. El documento de componente no se transforma en aprobación de cualquier instalación.',
 'La instalación queda pendiente de demostrar elegibilidad. La existencia del documento no completa el análisis de configuración.',
 'No se declara defectuoso el componente por falta de datos; se distingue estado físico de evidencia de elegibilidad.')
case('C14','Aplicabilidad de la AD2024-14-03','Una aeronave ficticia coincide con un modelo de la tabla de la ADoriginal,pero no consta si incorpora el piloto automático definido.','Hoja histórica aportada y publicaciónFAAoriginal2024-15529; nohay expedienteSTCni equipo confirmado.',
 'FAA AD2024-14-03,apartados(a),(c),(g)y(i)en publicaciónoriginal;aplicabilidadjurisdiccional yestadovigenteDRSporcomprobar.',
 'Se confirma efectividad histórica20agosto2024y la combinación modelo/instalación definida. Antes de calcular plazo se busca evidencia de equipo ySTC. También se comprueba si la directiva ha sido sustituida o modificada en la fecha de análisis.',
 'Estado:pendiente de configuración y de comprobación actual de sustitución/cancelación. No es un caso cerrado de cumplimiento.',
 'La publicaciónoriginal no prueba por sí sola vigencia actual. El caso no es específico del motor:trataun sistema depilotoautomático.')
case('C15','Un contador desconocido','Se recibe un componente ficticio con identificación legible,pero sin evidencia suficiente de ciclos totales. La hoja de cálculo convierte una celda vacía en cero.','Tarjeta de pieza incompleta y modelo académico de control; límite ficticio de1800ciclos.',
 '1321/2014,M.A.305y reglas decomponentes/control devidaaplicables.',
 'Se corrige el modelo para tratarvacío como dato ausente,se conserva la trazabilidad del hallazgo yse solicita evidencia. Asignar cero fabrica un margen no demostrado.',
 'Estado académico:PENDIENTE DE HISTORIAL. No se calcula un margen positivo acreditado ni se declara condición servible.',
 'La reconstrucción de historial debe seguir el sistema ylos datos aplicables; el ejercicio no describe una vía de regularización real.')
case('C16','Vencimiento simultáneo por uso y calendario','Una tarea ficticia vence cada200horaso6meses,lo primero. Se realizó el30abril2026a1000h. El18octubreseacumulan1190h.','Registro académico de tarea ylectura actual; sin tolerancias autorizadas.',
 'Reglas de programa aplicables;intervalosyfechasnuméricosinventados parael ejercicio.',
 'Se calcula umbral1200h,margen10h,yfecha30octubre2026. Ambos límites se conservan. Con unaprevisión de5hporjornada,sealcanzaríael umbral tras2jornadas deoperación,siempre que no domine antes elcalendario.',
 'La planificación debe considerar10hylafecha30octubre,con evidencia delritmo deutilización. No seconvierte2jornadasautomáticamente en2díasnaturales.',
 'El caso no autoriza extensiones ni interpreta6meses como180días.')

if __name__=='__main__':
 (R/'evidence/case-bank.json').write_text(json.dumps(CASES,ensure_ascii=False,indent=2));print(len(CASES),'casos académicos')
