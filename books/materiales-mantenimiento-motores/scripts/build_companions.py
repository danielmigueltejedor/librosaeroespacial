from pathlib import Path
import sys,json,re
R=Path(__file__).resolve().parents[1]
W=Path(__file__).resolve().parent
sys.path.insert(0,str(R/'scripts'))
from montar_libros import P,C,E
from problem_development import D
interpret=[
'La elongación responde a la rigidez axial; la tensión compara fuerza y área, sin verificar todavía cedencia.',
'La compresión impide la expansión libre; una estructura flexible daría otra compatibilidad.',
'El equivalente sirve para comparar cedencia en el modelo declarado, mientras las principales describen planos sin cortante.',
'La geometría de equilibrio explica la razón dos entre tensiones; el equivalente combina ambas.',
'La energía es trabajo recuperable en el modelo elástico y no energía de rotura.',
'El efecto de entalla en fatiga es menor que la concentración elástica para la sensibilidad adoptada.',
'La intensidad resulta inferior a la tenacidad supuesta, con una conclusión estática y condicionada.',
'La longitud crítica total duplica la semilongitud; el defecto inicial requiere su propia tensión crítica.',
'El espesor es insuficiente para el cribado, por lo que la denominación de tenacidad plana no está demostrada.',
'La corrección por anchura eleva intensidad y reduce el tamaño crítico respecto a la placa infinita.',
'La tensión media consume parte del margen del modelo de Goodman; máximo y amplitud deben distinguirse.',
'La interpolación asigna una vida solo dentro del tramo y convención de la curva ajustada.',
'El daño previo consume una fracción de la vida idealizada; la vida restante depende del siguiente nivel.',
'Los bloques acumulan daño linealmente y el fallo idealizado puede caer dentro de un bloque.',
'La intensidad máxima y el rango responden a preguntas físicas distintas: inestabilidad y crecimiento.',
'La vida calculada cubre crecimiento entre tamaños, sin añadir iniciación ni certificar detectabilidad.',
'El exponente dos cambia la primitiva a un logaritmo y requiere mantener unidades del coeficiente.',
'La fracción académica reduce el intervalo respecto a la vida de propagación, sin ser regla reglamentaria.',
'La potencia de tensión amplifica un cambio moderado de carga; el tiempo convierte tasa en deformación.',
'Ambos cambios elevan la tasa del mecanismo asumido; no se deduce por ello una vida de rotura.',
'La exposición más caliente corresponde a menor tiempo bajo la correlación y la misma tensión.',
'La elasticidad ya consume parte del límite; el tiempo usa únicamente la deformación todavía disponible.',
'La fracción de fibra eleva rigidez longitudinal y modifica masa dentro de una idealización sin vacíos.',
'La matriz domina buena parte de la deformación transversal del modelo en serie.',
'Separar caras aumenta inercia, pero el beneficio exige que núcleo y unión mantengan la arquitectura.',
'Duplicar espesor exige cuadruplicar tiempo en la ley parabólica, sin medir directamente metal consumido.',
'El factor dos procede del recorrido de retorno; el eco no caracteriza por sí solo tamaño o aceptación.',
'La mayor frecuencia reduce profundidad pelicular, sin fijar una detección garantizada.',
'La tasa observada y supervivencia son estimaciones condicionadas al modelo y población.',
'La espera logística reduce el cociente de disponibilidad aun manteniendo la reparación activa.',
'La edad cambia la supervivencia condicional con el parámetro de forma adoptado.',
'La ausencia de eventos acota la tasa solo con exposición y un nivel estadístico definido.',
'La orden relaciona el pico con el giro; no identifica por sí sola una causa de vibración.',
'El material más denso puede producir menor masa cuando gobierna resistencia y cambia el área.',
'El reparto de caídas térmicas determina la interfaz dentro de la pared plana idealizada.'
]
def safe(s):
 # Caracteres reservados en prosa; los segmentos matemáticos existentes se conservan.
 parts=re.split(r'(\$[^$]*\$|\\\[.*?\\\]|\\\(.*?\\\))',s,flags=re.S)
 for i,v in enumerate(parts):
  if v.startswith('$') or v.startswith('\\[') or v.startswith('\\('):continue
  v=re.sub(r'(?<!\\)_',r'\\_',v)
  v=re.sub(r'(?<!\\)\^',r'\\textasciicircum{}',v)
  parts[i]=v
 return ''.join(parts)
def a(title,body):return r'\apartado{'+title+'}{'+safe(body)+'}\n'
header=r'''\input{latex/preamble.tex}
\begin{document}\frontmatter
'''
intro=r'''\chapter*{Cómo utilizar este cuaderno}\addcontentsline{toc}{chapter}{Cómo utilizar este cuaderno}
Los datos y situaciones son originales y ficticios, salvo identificación expresa de una publicación oficial. Se conserva la secuencia modelo--hipótesis--desarrollo--resultado--verificación. Una comprobación numérica no valida por sí sola el modelo ni el estado de una aeronave. Las referencias de capítulo corresponden al manual de la colección.

Fecha normativa de referencia: 18 de octubre de 2026, con las versiones y pendientes indicados en el manual y los informes. Las soluciones no constituyen instrucciones aprobadas, programas aprobados ni autorizaciones de mantenimiento. En los casos puede ser correcto concluir que falta evidencia. La publicación histórica de una AD no acredita automáticamente su estado actual.
\bigskip\creditosportada
\tableofcontents\mainmatter
'''
s=header+r'\portada{PROBLEMAS Y CASOS}{PROBLEMAS RESUELTOS\\Y CASOS PRÁCTICOS}{Materiales y mantenimiento de motores aeroespaciales\\35 problemas originales · 16 casos académicos}'+'\n'+intro
for title,chs in [('Mecánica, selección y efectos térmicos',[1,2]),('Fractura y tolerancia al daño',[3]),('Fatiga y propagación',[4]),('Fluencia y exposición térmica',[5]),('Compuestos, degradación, inspección y calor',[6,9,10,11]),('Fiabilidad, disponibilidad y monitorización',[12,22,24])]:
 s+=r'\chapter{'+title+'}\n'
 for p in P:
  if p['ch'] not in chs:continue
  s+=r'\section{'+p['key']+'. '+p['title']+'}'+fr'\label{{prob:{p["key"]}}}'+'\n'
  s+=a('Enunciado',p['prompt'])+a('Datos',p['datos'])+a('Incógnitas',p['unknown'])+a('Modelo físico',p['model'])+a('Hipótesis',p['hyp'])
  s+=r'\apartado{Ecuaciones}{'+'\n'.join(r'\['+v+r'\]' for v in p['eqs'])+'}\n'
  s+=a('Desarrollo algebraico',D[p['key']][0])+a('Sustitución numérica',D[p['key']][1])
  s+=r'\caso{Resultado}{'+p['results']+'}\n'
  units=', '.join(dict.fromkeys(t['unit'] for t in p['tests'])).replace('dimensionless','adimensional')
  s+=a('Unidades','Magnitudes de los controles numéricos: '+r'\texttt{'+units.replace('^',r'\textasciicircum{}')+'}. Las unidades tipográficas del resultado se muestran junto a cada valor; las conversiones se realizan antes de operar.')
  s+=a('Interpretación',interpret[int(p['key'][1:])-1])+a('Verificación',p['check'])+a('Limitaciones',p['limits'])
 s+='\n'
s+=r'\part{Casos de mantenimiento y normativa}\chapter{Situaciones académicas razonadas}'+'\n'
for c in C:
 s+=r'\Needspace{.36\textheight}'+r'\section{'+c['key']+'. '+c['title']+'}\n'
 for title,key in [('Situación inicial','situation'),('Documentación disponible','docs'),('Fecha de referencia','date'),('Normativa y alcance','norm'),('Procedimiento y justificación','analysis'),('Resultado académico','result'),('Limitaciones','limits')]:s+=a(title,c[key])
s+=r'\end{document}'
(R/'problemas.tex').write_text(s)
s=header+r'\portada{AUTOEVALUACIÓN}{SIMULACROS\\DE EXAMEN}{Materiales · Mantenimiento · Evaluación combinada\\Seis pruebas originales con soluciones razonadas}'+'\n'+intro
s+=r'''\chapter*{Reglas de autoevaluación}\addcontentsline{toc}{chapter}{Reglas de autoevaluación}
Cada prueba contiene cuatro preguntas de 2,5 puntos: total 10 puntos. Los tiempos propuestos son orientativos y no describen una convocatoria oficial. En cuestiones numéricas: 1 punto por modelo, hipótesis y planteamiento; 1 por desarrollo, unidades y resultado; 0,5 por verificación e interpretación. En cuestiones de análisis: 1 por identificar ámbito y fuentes; 1 por razonamiento y conclusión; 0,5 por condiciones y límites. Se admiten métodos equivalentes justificados. Un resultado sin desarrollo no obtiene toda la puntuación.

En materiales se permite una hoja propia de fórmulas. En mantenimiento se recomienda trabajar con los textos oficiales de las versiones indicadas para practicar localización, sin depender de memoria de números. Resolver primero los enunciados; las soluciones aparecen en la segunda parte.
\part{Enunciados}
'''
for e in E:
 s+=r'\chapter{'+e['key']+'. '+e['title']+'}\n'+r'\noindent\textbf{Tiempo orientativo: '+str(e['duration'])+' minutos. Cuatro preguntas; 10 puntos.}\n'
 for i,q in enumerate(e['questions'],1):s+=r'\section*{'+str(i)+'. '+q['title']+' (2,5 puntos)}\n'+safe(q['prompt'])+'\n\n'
s+=r'\part{Soluciones y criterios de corrección}'+'\n'
for e in E:
 s+=r'\chapter{Soluciones de '+e['key']+'}\n'
 for i,q in enumerate(e['questions'],1):s+=r'\section{'+str(i)+'. '+q['title']+'}\n'+safe(q['solution'])+'\n\n'
s+=r'\backmatter\chapter*{Cómo corregir el intento}\addcontentsline{toc}{chapter}{Cómo corregir el intento}Comparar primero el modelo, después operaciones y unidades y finalmente interpretación. Registrar el origen del error. En mantenimiento, comprobar versión y hechos del escenario antes de puntuar una conclusión. Una respuesta condicional bien justificada puede ser más precisa que una certeza sin evidencia.\end{document}'
(R/'simulacros.tex').write_text(s)
print('Cuadernos montados:',len(P),'problemas,',len(C),'casos,',len(E),'simulacros')
