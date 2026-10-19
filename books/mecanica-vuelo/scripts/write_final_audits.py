"""Consolida resultados existentes. No promueve estados científicos."""
from pathlib import Path
import json,hashlib,re
from collections import Counter
R=Path(__file__).resolve().parents[1]
def read(n):return json.loads((R/'reports'/n).read_text())
def save(n,t):(R/'reports'/n).write_text(t.strip()+'\n')
q=read('studium_quality_report.json');qa=read('editorial-automated-checks.json');end=read('endurance-results.json')
status=q['math_grounding']['by_status'];counts=q['counts']
base='Fecha: 19 de octubre de 2026. Edición EN REVISIÓN. Revisión experta independiente pendiente.\n\n'
families=[
('Ejes y transporte','1–3','MIT-3, MIT-4, MIT-14','NED: z abajo; cuerpo x delante, y derecha, z abajo; Cb_n pasiva 3-2-1. Velocidad aire distinta de suelo.','V001–V006; T02 ida/vuelta','Euler singular en cos(theta)=0; viento no uniforme requiere derivada de transporte.'),
('Fuerzas, polar y eficiencia','4','MIT-1; deducción original','q=ρV²/2; V=TAS relativa al aire. CD0,k>0; referencias comunes. Oswald no se identifica siempre con eficiencia de envergadura.','V009–V014; controles Oswald y dimensiones','Polar subsónica docente; límite CLmax; mapa propulsivo no constante por defecto.'),
('Newton–Euler y simetría','5–6','MIT-4, MIT-6','Tensor con entradas -Ixz; masa instantánea y tensor constantes en ecuación angular; marco cuerpo; trim no implica estabilidad.','V007–V008; T06 residuos por componente; controles trim','Sin flujo de momento por combustible; fuerzas N y momentos Nm no se mezclan en una norma sin escala.'),
('Planeadores','7–9','MIT-1; derivación e integración originales','γ negativo en descenso, tasa de caída positiva. L=Wcosγ, D=-Wsinγ. ISA geopotencial y CL declarado para integrales.','Raíz exacta vs optimización T08; límites de planeo; cuadratura','No trasladar óptimo de ángulo pequeño a modelo exacto; viento afecta alcance suelo.'),
('Reactores','10–12','MIT-1 y balances originales','cT en kg/(N s); Wdot=-g cT T. Separar V fija, CL fijo, empuje fijo y vuelo de CL,V fijos.','Primitivas simbólicas; ODE/cuadratura; 8 controles adicionales','ρ y CL fijos implican V variable; CL,V fijos requieren ρ variable y, si asciende, T≠D.'),
('Ascenso y descenso','13','Balance Newton/energía','Exceso de potencia para ascenso pequeño cuasiestacionario. Integrar masa con altura y comprobar exceso positivo.','T13 refinamiento de 25 a 12.5 m; barridos','Vx,Vy requieren optimización y restricciones; techo docente no certificado.'),
('Viraje','14','Balances originales','Viraje coordinado nivelado: n=1/cosφ, radio con TAS; comprobar pérdida, estructura y energía.','Identidades geométricas y envolvente T14','Viraje instantáneo no equivale a sostenido; viento altera trayectoria terrestre.'),
('Hélices y misión','15–16','Balances originales','cP referido a potencia al eje en kg/J; η=TV/Peje; separar cuatro óptimos clásicos.','Primitiva de autonomía, ODE y T15 0<η≤1','η y cP variables invalidan fórmula cerrada; potencia útil no se confunde con potencia al eje.'),
('Rodadura y fases','17–18','Newton y cuadratura originales','Va=Vsuelo+viento de cara; N=W-L; masa explícita; empuje finito a velocidad cero.','Cuadratura vs integración temporal, límite coeficiente cuadrático nulo','Rodadura sola no incluye transición ni obstáculo; no usar P/V singular al arrancar.'),
('Estabilidad estática','19–20','MIT-2, MIT-8','Derivadas con variables retenidas y referencias de momento explícitas; margen estático bajo hipótesis lineales.','Punto neutro; residuos trim; r×F','Cm=0 es equilibrio, Cmα<0 tendencia estática. Efecto cola aislado no prueba estabilidad completa.'),
('Dinámica, ampliación','21','MIT-6, MIT-7, MIT-8','Descriptor E xdot=F x; modos locales; aproximaciones reducidas bajo separación de escalas.','Autovalores, exponencial matricial, refinamiento por estado','Ampliación editorial, no bloque oficial adicional. Modelos numéricos sintéticos sin aeronave identificada.'),
('Simulación','22–23','Código y XML JSBSim fijados','T6 con motor de empuje y direct thruster; sumar cuatro motores B747 y sólo depósitos alimentadores.','44 trims, tres pasos T6, XML, crucero, dos autonomías y balances CSV','Modelos BETA/ALPHA, sin validación experimental; SAULE sólo procedimiento.')]
(R/'evidence/model-family-register.json').write_text(json.dumps([dict(family=f,chapters=c,documentary_context=s,assumptions=a,checks=v,limitations=l,expert_review='PENDING') for f,c,s,a,v,l in families],ensure_ascii=False,indent=2))
science='# A. Auditoría científica\n\n'+base+'''## Alcance y dictamen
Se ha desarrollado una edición docente completa, con modelos explícitos, deducciones, ejemplos y límites. No se declara científicamente validada. La cobertura se contrasta con la guía ULE 2026/2027, código 0710325, consultada completa. El capítulo dinámico es ampliación. La repetición de «Bloque V» en la guía se registra como anomalía editorial y no altera el contenido oficial.

## Revisión por familias
'''
for f,c,s,a,v,l in families:science+=f'### {f} (capítulos {c})\n\nContexto: {s}. {a}\n\nComprobaciones: {v}. Límite: {l}\n\n'
science+='''## Correcciones y distinciones materiales
El factor de tabla del motor multiplica empuje y sigue dando fuerza; la potencia física usa TAS. Se corrigió el conteo de cuatro motores B747 y se excluyó un depósito sin alimentación. La lectura del modelo T6 impide atribuirle potencia real al eje de un PT6. En los residuos de trim y convergencia se separaron magnitudes de distintas dimensiones. El ejemplo de hélice usa CP=0.090 para conservar eficiencia dentro del dominio energético. Estos cambios están incorporados en los textos y cálculos vigentes.

Los materiales estudiantiles sólo clasifican familias y dificultad. Dos anclas documentales nativas de un problema no son dos soluciones independientes; las fuentes siguen PENDING. No se han inventado datos de ensayo ni prestaciones certificadas.

## Pendientes reales
Revisión experta de texto y ecuaciones; contrastar modelos de aeronave con datos independientes y sus incertidumbres; refinamiento completo de autonomías; ensayo SAULE; completar trazabilidad semántica por afirmación y auditorías nativas. El libro y los PDF permanecen EN REVISIÓN. Véanse LIMITACIONES.md y los informes nativos sin alterar.
'''
save('A-auditoria-cientifica.md',science)
math='# B. Auditoría matemática\n\n'+base+'''## Evidencia ejecutada
`model-checks.json`: 44 controles correctos de 44. Incluye ortogonalidad, determinantes y dirección de matrices; Jacobiano de Euler y gravedad; términos de inercia cruzada y trabajo giroscópico; óptimos de polar; primitivas, Oswald, dimensiones, límites e integraciones. `additional-symbolic-checks.json`: ocho identidades correctas de ocho, entre ellas ramas a empuje fijo, trim lineal, mínimo descenso exacto y norma de cuaterniones.

Studium conserva nueve comprobaciones iniciales (seis simbólicas y tres dimensionales), diez derivaciones con unidades y cuatro contratos de afirmación. La comprobación dimensional de una derivación no certifica su desarrollo ni la correspondencia con el párrafo. Los 284 cálculos vigentes ligados a 84 problemas son sustituciones reproducidas, con historial anterior obsoleto conservado.

## Inventario y correspondencia
`equation-inventory-native.json` contiene todas las relaciones que reconoce Studium en los párrafos, paginadas hasta el final. `equation-inventory-editorial.json` identifica archivo, línea y bloque matemático de la composición LaTeX, incluidas soluciones y apéndices. No se consideran equivalentes un bloque LaTeX, una ecuación reconocida y una prueba: un bloque puede tener varias relaciones; una relación reconocida puede no ser procesable.

`model-family-register.json` declara hipótesis, singularidades y pruebas por familia. Las fórmulas individuales sin prueba ligada permanecen pendientes aunque pertenezcan a una familia comprobada.

## Diagnóstico nativo conservado
'''+json.dumps(status,ensure_ascii=False,indent=2)+'''

El informe nativo reconoce 1005 relaciones y 666 afirmaciones. Sólo seis afirmaciones figuran verificadas según su vinculación exacta; no se extrapola el resultado a todas las ecuaciones. Persiste MATH-001: el lector interpreta símbolos matriciales como escalares y diagnostica formas 3×1 frente a 3×3 en una ecuación cinemática correcta. La reproducción y la incidencia están separadas en `framework-math-issue.json` y `framework-issues.md`. No se modifica la ecuación física ni se silencia el bloqueo.

## Signos, dimensiones y restricciones
Se usa Ixz con signo negativo dentro del tensor; peso W=mg; consumos másicos diferenciados de ponderales; ángulos en radianes para derivar y evaluar. Se revisaron límites de Euler, pérdida, empuje y potencia, determinante de trim, masa final positiva, dominio de raíces y denominadores. Las expresiones de ascenso aproximado y dinámica reducida llevan sus hipótesis. La auditoría no equivale a revisión experta completa de todas las deducciones.
'''
save('B-auditoria-matematica.md',math)
num='# C. Auditoría numérica\n\n'+base+'''## Pruebas y alcance
- 44/44 controles de modelos, 8/8 simbólicos adicionales.
- 151/151 controles del banco, con reproducción de sustituciones y cruces seleccionados con cuadratura, ODE, autovalores y barridos.
- 158/158 controles de talleres, simulacros y CSV. Incluyen residuos por componente de trim; ida/vuelta de rotación; mínimo exacto por raíz y optimización; refinamiento de ascenso y balances de combustible.
- 284 sustituciones vigentes aceptadas por Studium. Varias pruebas comparten ecuaciones o entradas; no se suman como testigos científicos independientes.

Los resultados completos con tolerancias y alcance están en los JSON correspondientes y en `verification-register.json`. No se han cambiado tolerancias para ocultar fallos. Se conservan scripts ejecutables.

## Experimentos realmente ejecutados
JSBSim 1.3.3; modelos en commit `66f7fafc07fe13e7ede9db20873030fed2881713`. Se guardan entradas, huellas XML, propiedades, CSV, condición de terminación y resultados.

1. T6: 44 trims sin fallo en dos masas (5600, 5850 lbm) y alturas (5000, 9000 ft), 115–215 kt CAS. EAS y TAS se leen de la salida; no se equiparan automáticamente. Ascenso por exceso de potencia desde trim horizontal: aproximación, no trim de ascenso exacto.
2. T6 libre, 60 s, dt=0.1/0.05/0.025 s: las diferencias sucesivas finales de TAS y altura disminuyen. Para el par fino son menores que 1e-4 m/s y 1e-3 m. No se calcula un orden global formal.
3. XML originales: 1200 pasos de 0.05 s realmente ejecutados; CSV de 61 muestras.
4. B747: crucero de 1800 s con control docente, masa y gasto variables. Los errores de seguimiento se conservan; no se afirma altura perfectamente constante.
5. B747: dos autonomías hasta agotar depósitos alimentadores. La comparación equivalente ajusta la misma procedencia y no es validación independiente.

'''
for c in end['cases']:
    num+=f"Combustible inicial {c['initial']['fuel_kg']:.6f} kg; autonomía simulada {c['simulated_time_s']:.3f} s; gasto inicial congelado {c['constant_initial_flow_time_s']:.6f} s; polar equivalente {c['equivalent_polar_time_s']:.6f} s; error máximo de altura {c['max_height_error_m']:.3f} m.\n\n"
num+='''## Integridad y pendientes
Cuatro CSV de trayectorias tienen tiempo estrictamente creciente, números finitos y diferencia entre integral de gasto y consumo de depósitos inferior al 2% fijado para la salida muestreada. Esto es tolerancia de auditoría numérica, no precisión de fabricante. El último paso de agotamiento y el transitorio inicial están identificados. Los dos casos de autonomía usan dt=0.1 s y NO tienen estudio completo de refinamiento temporal; sigue pendiente.

Los modelos ALPHA/BETA contienen estimaciones; el control es docente. No hay ensayo físico SAULE ni medición de vuelo real. Los datos sintéticos se identifican como tales. La instalación y las pruebas del framework arrojaron 1072 correctas y dos omitidas por paquetes de idioma ausentes, sin modificar su código.
'''
save('C-auditoria-numerica.md',num)
bib='# D. Auditoría bibliográfica\n\n'+base+'''## Categorías y lectura efectiva
`source-registry.json` conserva 21 fichas: guía oficial, nueve registros MIT (MIT-17 sólo inspección inicial y no respaldo científico), USSA, código JSBSim y nueve libros investigados sólo bibliográficamente. La guía oficial se leyó completa; se indican secciones efectivamente consultadas de MIT, código y atmósfera. No se atribuye lectura completa a las 243 páginas USSA ni a libros de pago.

El proyecto nativo tiene diez fuentes públicas/documentales y diez extractos; su esquema cuenta la guía docente aparte. El registro bibliográfico editorial y los candidatos nativos cumplen funciones distintas. No se añaden fuentes irrelevantes para franquear el umbral nativo de doce. Ninguna autoridad PENDING se eleva automáticamente.

## Material facilitado
Los cuatro archivos se abrieron, inventariaron y clasificaron: ZIP Ágora, formulario, exámenes resueltos y cuaderno de ejercicios/exámenes. Se extrajeron textos y OCR de las páginas escaneadas; se revisaron contactos de todas ellas y páginas representativas completas. `input-review.json` conserva 31 grupos temáticos y el alcance; no declara lectura perfecta de cada línea manuscrita. Se identifican ejes, planeadores, reactores, hélices, rodadura, estabilidad y misiones. Las soluciones manuscritas dudosas no se adoptan como autoridad.

No se redistribuyen los PDF privados, el OCR, sus figuras o documentos administrativos. Sólo se conservan nombres de archivo y huellas de identificación, categorías y notas originales de revisión; no se incluyen datos personales de estudiantes.

## Diferencias bibliográficas registradas
Garceta: segunda edición 2012, ISBN 9788415452010 y 480 páginas según catálogo editorial, sin mezclar otro ISBN UPM. Etkin/Reid: guía 1996 frente a ficha editorial octubre 1995. Roskam: Flight Dynamics no se confunde con Airplane Design I/II de la guía. Carmona: DL2002/ISBN antiguo frente a 14.ª edición 2022. Torenbeek: fecha de guía frente a copyright/reimpresiones de Springer. Phillips: diciembre 2009 frente a catalogaciones 2010. Nelson y Pamadi conservan alcance de metadatos obtenido, sin afirmar páginas no leídas. Raymer 7.ª edición se comprueba en el autor, sin atribuir lectura del libro.

## Uso y límites
Los localizadores junto al texto indican contexto documental; no sustituyen una prueba ni dos soluciones independientes. Las figuras y ejercicios son originales. Se conserva licencia del framework; dependencias externas y modelos se obtienen por el procedimiento de reconstrucción, respetando sus avisos. No se atribuye aprobación a ULE, MIT, NASA, Boeing o fabricantes.
'''
save('D-auditoria-bibliografica.md',bib)
editor='# E. Auditoría editorial\n\n'+base+'''## Composición final
Se adapta la colección Studium ya existente: A4, márgenes 25 mm, familia Latin Modern, jerarquía de títulos, paleta azul/ocre/violeta/verde y cabeceras de revisión. La portada es una ilustración vectorial académica provisional, conforme al último encargo, con retícula y ejes de avión. El texto no lleva identificadores internos nativos.

'''
for row in qa:editor+=f"- {row['document']}: {row['pages']} páginas; errores de compilación, referencias indefinidas, glifos perdidos, desbordamientos y texto fuera de área comprobada: cero.\n"
editor+='''
## Inspección visual
Se renderizaron todas las páginas y se revisaron sus contactos: ocho hojas del manual, tres del banco y dos de simulacros. Se ampliaron páginas representativas de portadas, índices, ecuaciones, gráficos, soluciones, simulación y apéndices; se revisaron de nuevo los cambios finales de bibliografía y rúbrica. No equivale a corrección tipográfica experta línea por línea. Se corrigieron anchura de índice, guiones Unicode, macros de entrada y recuadros que quedaban aislados. La bibliografía se compone a 9 puntos para evitar una página residual y la tabla de estudio se mantiene continua.

Se conservan páginas de apertura de parte deliberadas. No se aumenta el número de páginas con relleno. Los 143+50+31=224 folios PDF se entregan como tres documentos; la extensión orientativa del encargo no se trata como motivo para añadir contenido repetido.

## Contenido de cierre
23 capítulos, 23 talleres, 18 apéndices A–R sin Ñ, formulario condicionado, ISA, guía JSBSim, soluciones razonadas, cobertura y plan. 43 problemas en cuatro niveles y seis simulacros con 18 problemas nuevos, enunciados agrupados antes de soluciones. Figuras vectoriales originales: 26, más portada dibujada. Las soluciones explicitan datos, incógnitas, ejes, hipótesis, modelo, ecuaciones, desarrollo, sustitución, unidades, interpretación, comprobación y límites.

Los controles editoriales detallados están en `editorial-automated-checks.json`. Las miniaturas de trabajo no forman parte de la entrega. La lectura de texto extraído se complementa con inspección visual, porque no detecta sola superposiciones o pérdida de legibilidad.
'''
save('E-auditoria-editorial.md',editor)
save('LIMITACIONES.md','''# Limitaciones y trabajo pendiente

'''+base+'''
1. Revisión científica experta y corrección tipográfica exhaustiva independientes pendientes. La cobertura y las pruebas no convierten el material en libro aprobado por ULE.
2. Fuentes nativas PENDING, trazabilidad semántica parcial y párrafos sin auditoría nativa; Studium conserva COURSE_DISCOVERY, released=false y bloqueos. Las cinco auditorías externas no se hacen pasar por aprobaciones nativas.
3. MATH-001 conserva falso positivo matricial; centenares de relaciones son unsupported o no procesables por el lector. No se infiere que sean correctas por pertenecer a una familia comprobada.
4. Los modelos de polar, consumo y mapas usados en problemas son docentes. Las leyes cerradas requieren sus hipótesis; no extrapolar a envolventes reales sin datos.
5. JSBSim T6 y B747 educativos, sin contraste experimental. T6 usa empuje con direct thruster. SAULE sólo metodología. Autonomías completas sin refinamiento temporal; seguimiento de altura imperfecto y cuantificado.
6. Los libros recomendados se investigaron por metadatos; no se consultó su texto completo. El material manuscrito privado tiene partes inciertas. No se reutilizan sus soluciones como autoridad.
7. Reconstrucción requiere LaTeX, Python3.12, Git, acceso a paquetes/modelos públicos y versiones fijadas. Se preservan CSV para revisión sin red. No se promete igualdad binaria de PDF entre sistemas.
8. El proyecto nativo representa los 23 capítulos y 84 ejercicios; los 18 apéndices se conservan en las fuentes editoriales. Dos figuras nativas comprobadas y 26 figuras editoriales no son el mismo inventario. Los cambios finales de maquetación y bibliografía no se reimportaron al historial nativo; sus huellas se distinguen.
''')
save('INFORME-FINAL.md',f'''# Entrega de Mecánica de Vuelo — Studium

{base}
Se entregan tres volúmenes editoriales completos (143, 50 y 31 páginas), fuentes LaTeX, 26 figuras originales, 84 ejercicios resueltos, seis simulacros, scripts y XML originales, CSV de ejecuciones reales, bibliografía y cinco auditorías. El manual tiene 23 capítulos y 18 apéndices, incluido formulario y guía de reproducción.

## Evidencia y estado

- Programa ULE 2026/2027 contrastado, ampliación dinámica identificada.
- Python: 44 controles de modelos, ocho simbólicos complementarios, 151 del banco y 158 de talleres/simulacros/CSV, correctos en sus alcances.
- Studium: {counts['paragraphs']} párrafos, {counts['problems']} problemas comprobados y {counts['computations_replayed']} cálculos vigentes; diez derivaciones y cuatro contratos. Borrador nativo compilado de 219 páginas, separado de los tres volúmenes finales.
- Framework probado: 1072 pruebas correctas y dos omitidas. Commit y herramientas en versions.json, sin cambios al repositorio principal.
- JSBSim realmente ejecutado: 44 trims, tres pasos temporales T6, trayectoria XML, crucero y dos autonomías hasta agotamiento.

Los informes nativos mantienen bloqueos y autoridad pendiente. El libro NO está científicamente validado ni liberado por Studium; véanse A–E, LIMITACIONES y la incidencia MATH-001. Las comprobaciones numéricas no equivalen a revisión experta o validación experimental.

## Reproducir y revisar

Empiece por README.md. Los tres principales LaTeX compilan con sus figuras locales sin el material privado. rebuild.sh regenera cálculos, simulaciones y figuras con las dependencias indicadas. La instantánea del framework conserva su licencia y commit; los modelos externos se descargan y verifican por commit.

El ZIP excluye runtime, historial Git, OCR privado, PDF protegidos y archivos administrativos. Conserva los registros nativos, fuentes originales, evidencias, informes y CSV. Un manifiesto SHA-256 permite comprobar los miembros; la integridad del ZIP y la presencia de sus componentes se verifican antes de entrega.
''')
register={}
for file in ['model-checks.json','additional-symbolic-checks.json','problem-checks.json','all-cases-checks.json','studium-math.json','native-derivations.json','native-contracts-recorded.json','native-computations.json']:
    p=R/'reports'/file;register[file]=dict(path='reports/'+file,sha256=hashlib.sha256(p.read_bytes()).hexdigest(),scope='Consultar campos de cada registro; pruebas no independientes ni aprobación humana.')
(R/'evidence/verification-register.json').write_text(json.dumps(register,ensure_ascii=False,indent=2))
print('Cinco auditorías, limitaciones e informe de entrega escritos.')
