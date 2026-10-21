"""Generate editable LaTeX from original academic cases; never contacts an authoring API."""
from pathlib import Path
from copy import deepcopy
import json, math
from fluid_bank import cases, evaluate, CHAPTERS
ROOT=Path(__file__).resolve().parents[1]
import sys
sys.path.insert(0,str(ROOT.parents[1]/"scripts"))
from solution_steps import numeric_steps

# Twenty new parameter sets. Families are reused explicitly, never counted as
# twenty additional independent physical models.
SETS=[
 [(2,{'m':30,'k':.6,'v0':10,'t':4}),(10,{'a':.8,'x':.25,'y':.15}),(13,{'b':1,'L':1.8,'h0':.3,'theta':math.pi/4}),(17,{'R':.0012,'L':1,'Q':1.5e-6}),(46,{'px':.0012,'py':-.00048,'L':1.8e6})],
 [(3,{'m':.06,'b':.15,'t':.9}),(15,{'b':.45,'h':.22,'L':1,'rs':650}),(23,{'U':.15,'f':3,'y':.0008}),(25,{'Q':.015,'D':.035,'p':100000,'theta':math.pi/2}),(30,{'V':.8,'L':3,'D':.012})],
 [(7,{'F':4.2,'A':.14,'U':.5,'h':.0015}),(19,{'W':5000,'S':14,'cd0':.028,'K':.052}),(33,{'C':.004,'K':.008,'r1':.12,'r2':.24}),(34,{'At':1,'Ao':.0005,'h0':2.5,'h1':.8}),(37,{'a':1.5,'b':4,'p':1500})],
 [(5,{'m':3,'k':120,'b':6,'x0':.04,'t':1}),(45,{'T':.0002,'U':.0002,'L':.0012}),(27,{'V':24,'U':6,'A':.0008}),(42,{'U':.3,'t':.8,'y':.0012}),(48,{'dT':4,'L':.012})]
]
def exams():
    bank=cases();out=[]
    for i,group in enumerate(SETS,1):
        rows=[]
        for j,(num,values) in enumerate(group,1):
            p=deepcopy(bank[num-1]);p['family']=p['id'];p['id']=f'MF-S{i}-{j}'
            for d in p['data']:
                if d[0] in values:d[1]=values[d[0]]
            rows.append(p)
        out.append(rows)
    return out

UNITS={'':'1','kg/m**3':r'\mathrm{kg/m^3}','m/s**2':r'\mathrm{m/s^2}','m**2/s':r'\mathrm{m^2/s}','m**3/s':r'\mathrm{m^3/s}','1/s':r'\mathrm{s^{-1}}','1/s**2':r'\mathrm{s^{-2}}','m**2':r'\mathrm{m^2}','m**3':r'\mathrm{m^3}','W/m**2':r'\mathrm{W/m^2}','W/m**3':r'\mathrm{W/m^3}','kg/(m**2*s)':r'\mathrm{kg/(m^2\,s)}','W/(m*K)':r'\mathrm{W/(m\,K)}','J/(kg*K)':r'\mathrm{J/(kg\,K)}','1/K':r'\mathrm{K^{-1}}','1/m':r'\mathrm{m^{-1}}'}
def unit(u):return UNITS.get(u,r'\mathrm{'+u.replace('*',r'\,')+'}')
def num(v):
    if v==0:return '0'
    s=f'{v:.6g}'
    if 'e' in s:
        m,e=s.split('e');return m+r'\times10^{'+str(int(e))+'}'
    return s
def table(p,local=False):
    env='tabular' if local else 'longtable'
    lines=[r'\begin{'+env+r'}{@{}p{.15\linewidth}p{.23\linewidth}p{.54\linewidth}@{}}',r'\toprule Símbolo & Valor SI & Significado\\\midrule'+('' if local else r'\endhead')]
    for k,v,u,label,tex in p['data']:
        un='' if not u else r'\,'+unit(u)
        lines.append('$'+tex+'$ & $'+num(v)+un+'$ & '+label+r'\\')
    return '\n'.join(lines+[r'\bottomrule\end{'+env+'}'])

DIAGRAMS={
13:r'''\begin{tikzpicture}[scale=.85,>=Stealth]
\fill[studiumLight] (-1,0)--(0,0)--(0,-.6)--(2,-2.5)--(2,-3)--(-1,-3)--cycle;
\draw[blue,thick] (-1,0)--(0,0) node[above right]{superficie libre};
\draw[thick] (0,0)--(0,-.6);
\draw[very thick] (0,-.6)--(2,-2.5);
\fill (0,-.6) circle(2pt) node[left]{bisagra};
\draw[->,thick] (.2,-1.7)--(1.15,-.7) node[right]{$F$};
\draw[<->] (2.6,-.6)--(2.6,-2.5) node[midway,right]{$L\sin\theta$};
\draw[dashed] (0,-.6)--(2.7,-.6);
\node at (1.4,-3.5){Esquema: distancias sobre el panel y profundidad son distintas.};
\end{tikzpicture}''',
16:r'''\begin{tikzpicture}[>=Stealth]
\draw[very thick] (0,0)--(5,0);\draw[very thick] (0,2)--(5,2);
\draw[->] (4.2,2.2)--(5.3,2.2) node[right]{$U$};
\draw[->] (.2,.2)--(.2,1.8) node[left]{$y$};
\draw[studiumBlue,thick,domain=0:2,samples=50] plot ({1.3+1.2*\x+.15*\x*(2-\x)},\x);
\draw[<->] (5.5,0)--(5.5,2) node[midway,right]{$h$};
\node at (2.5,-.45){Pared fija};\node at (2.5,2.7){Perfil combinado, esquema sin escala};
\end{tikzpicture}''',
25:r'''\begin{tikzpicture}[>=Stealth]
\draw[thick] (-2,-.3)--(0,-.3)--(1.5,1.2);
\draw[thick] (-2,.3)--(-.2,.3)--(1.1,1.6);
\draw[->,very thick,studiumBlue] (-2,0)--(-.8,0) node[above]{$V_1$};
\draw[->,very thick,studiumBlue] (.6,.9)--(1.6,1.9) node[right]{$V_2$};
\draw[->] (2.3,-.2)--(3.3,-.2) node[right]{$x$};
\draw[->] (2.3,-.2)--(2.3,.8) node[above]{$y$};
\node at (-1,-.7){entrada con $p_g>0$};\node at (.7,2.2){salida atmosférica};
\end{tikzpicture}''',
33:r'''\begin{tikzpicture}[>=Stealth]
\fill[studiumLight,even odd rule] (0,0) circle(1.7) (0,0) circle(.7);
\draw (0,0) circle(1.7);\draw (0,0) circle(.7);
\draw[->] (.7,0)--(1.6,0) node[midway,above]{$u_r$};
\draw[->] (0,1.2)--(-.7,1.2) node[above]{$u_\theta$};
\node at (0,-2.2){El origen queda fuera del dominio anular.};
\end{tikzpicture}''',
42:r'''\begin{tikzpicture}[x=1cm,y=.45cm,>=Stealth]
\draw[very thick] (0,0)--(5,0);\draw[->] (4,-.35)--(5,-.35) node[right]{$U$};
\draw[->] (.5,0)--(.5,2.5) node[above]{$y$};
\draw[thick,studiumBlue] (3,0) .. controls (1.2,.6) and (1,1.5) .. (1,2.3);
\draw[->] (1,.35)--(2.2,.35);\draw[->] (1,.8)--(1.6,.8);\draw[->] (1,1.3)--(1.2,1.3);
\node at (3.3,2){$u\to0$ cuando $y\to\infty$};
\end{tikzpicture}''',
46:r'''\begin{tikzpicture}[>=Stealth]
\draw[->] (0,0)--(3,0) node[right]{$x$};\draw[->] (0,0)--(0,2.5) node[above]{$y$};
\draw[->,very thick,studiumBlue] (0,0)--(.8,2) node[right]{$\boldsymbol u_g$};
\draw[->,very thick] (0,0)--(2,-.8) node[right]{$\nabla_h p$};
\node at (3,2){$f>0$};
\end{tikzpicture}'''
}
def diagram(p):
    n=int(p.get('family',p['id']).split('P')[-1]) if '-P' in p.get('family',p['id']) else 0
    if n not in DIAGRAMS:return ''
    return '\n'+r'\begin{figure}[htbp]\centering'+DIAGRAMS[n]+r'\caption{'+p['title']+r'. Esquema original de apoyo, sin escala.}\label{fig:mf-p'+str(n)+r'}\end{figure}'+'\n'
def worked(p,exam=False):
    unknowns=r',\ '.join(row[3] for row in p['calc'])
    out=[r'\Needspace{.30\textheight}\section{'+p['id']+'. '+p['title']+'}',r'\begin{studiumworked}{'+p['id']+' · '+p['level']+'}',r'\textbf{Enunciado.} '+p['question'],table(p),r'\textbf{Incógnitas.} Se calculan $'+unknowns+r'$ y se interpreta el resultado bajo las hipótesis indicadas.',r'\textbf{Hipótesis.} '+p['hypotheses'],r'\textbf{Modelo y ecuaciones.}',r'\[\fitmath{'+p['model']+r'}\]',r'\textbf{Desarrollo.}\begin{enumerate}']
    out += [r'\item '+s for s in p['steps']]
    out += [r'\end{enumerate}',r'\textbf{Cálculo de cada magnitud.}']
    calculation_rows=[dict(target=k,expression=e,unit=u,why=r'Obtener $'+tex+r'$ con la relación del modelo y los valores anteriores.') for k,e,u,tex in p['calc']]
    calculated,_=numeric_steps(calculation_rows,dict(g=9.81,**{k:v for k,v,*_ in p['data']}))
    out += [calculated,r'\textbf{Resultados.}\begin{itemize}']
    for r in evaluate(p):
        un='' if not r['unit'] else r'\,'+unit(r['unit'])
        out.append(r'\item $'+r['tex']+'='+num(r['value'])+un+'$.')
    out += [r'\end{itemize}',r'\textbf{Interpretación.} '+p['interpretation'],r'\textbf{Comprobación.} '+p['check'],r'\textbf{Límites.} '+p['limits'],r'\end{studiumworked}']
    if not exam:out.append(diagram(p))
    return '\n\n'.join(out)

SOURCES=r'''\chapter*{Referencias y procedencia}\addcontentsline{toc}{chapter}{Referencias y procedencia}
Los enunciados, datos y esquemas de este volumen son originales. Los números son \textbf{datos hipotéticos de aprendizaje}, no resultados de ensayo ni preguntas oficiales. Las soluciones se clasifican como resultados derivados de los modelos escritos, y sus conclusiones físicas como interpretaciones condicionadas a esas hipótesis.

El manual de Mecánica de Fluidos de esta colección fija el recorrido de 16 capítulos. Para contrastar las ecuaciones y sus condiciones de aplicación se consultaron las siguientes fuentes abiertas de sus autores o instituciones, sin reproducir sus ejercicios:
\begin{itemize}
\item David Tong, \emph{Lectures on Fluid Mechanics}, University of Cambridge, notas del autor. Continuidad, esfuerzos viscosos, soluciones paralelas, flujo potencial y fluidos estratificados. \url{https://www.damtp.cam.ac.uk/user/tong/fluids/fluids.pdf}.
\item Dick K. P. Yue, \emph{Marine Hydrodynamics}, MIT OpenCourseWare, primavera de 2005. Lecciones 4 (esfuerzos, Navier--Stokes y contorno) y 16 (escalas y soluciones viscosas). \url{https://ocw.mit.edu/courses/2-20-marine-hydrodynamics-13-021-spring-2005/pages/lecture-notes/}.
\item Richard Lindzen, \emph{Dynamics of the Atmosphere}, MIT OpenCourseWare, primavera de 2008, capítulo 6, ecuaciones de movimiento, coordenadas giratorias, hidrostática y geostrofía. \url{https://ocw.mit.edu/courses/12-810-dynamics-of-the-atmosphere-spring-2008/resources/chapter_6/}.
\end{itemize}
Consulta de fuentes: 18 de octubre de 2026. No se atribuye aval a estas instituciones. El repositorio conserva un registro de procedencia, las expresiones de cálculo y las comprobaciones ejecutadas. La coincidencia aritmética, las dimensiones y los residuos de modelos seleccionados no constituyen validación experimental ni aprobación científica independiente.
'''
FRONT=r'''\chapter*{Presentación y convenios}\addcontentsline{toc}{chapter}{Presentación y convenios}
Estos cuadernos acompañan al manual de Mecánica de Fluidos de Studium y mantienen su orden de 16 capítulos. Se adopta $g=9.81\,\mathrm{m/s^2}$ en todos los casos que requieren gravedad. Se emplean unidades SI; los ángulos numéricos son radianes y las presiones son manométricas o absolutas según se indica. Los dígitos de las soluciones facilitan reproducir los cálculos, sin representar precisión experimental.

Antes de sustituir números, dibuja el sistema, fija ejes y frontera y escribe las hipótesis. En balances vectoriales, distingue la fuerza sobre el líquido de la fuerza sobre el sólido. En problemas de semejanza, diferencia las escalas de convección y variación temporal. Un valor adimensional sólo apoya las hipótesis concretas que compara.

La comprobación de cada ejercicio propone una ruta de contraste. Los informes del repositorio distinguen las comprobaciones efectivamente ejecutadas de los controles sugeridos al estudiante. Los niveles de dificultad son editoriales.
'''
def shell(kind,subtitle,body):
    return r'''\documentclass[10pt,a4paper,openany]{book}
\input{../../../shared/latex/studium-editorial.tex}
\usepackage{needspace}
\input{editorial-config.tex}
\renewcommand{\studiumvolumetype}{'''+kind+r'''}
\hypersetup{pdftitle={Mecánica de Fluidos — '''+subtitle+r'''}}
\begin{document}
\studiumcover{MECÁNICA DE FLUIDOS}{'''+subtitle+'}{'+('PROBLEMAS RESUELTOS' if kind=='problemas' else 'SIMULACROS')+r'''}
\frontmatter
\studiumreadingguide
'''+FRONT+body+r'''
\backmatter
'''+SOURCES+r'''
\end{document}
'''

def write():
    bank=cases();parts=[]
    chapter_checks=[
      'Distingue fuerza, potencia y energía; comprueba cómo cambia cada una al variar la velocidad.',
      'Separa un efecto local de rotación, una ecuación de movimiento y una conclusión de estabilidad local.',
      'Comprueba por separado la hipótesis newtoniana, la variación de densidad y la validez del continuo.',
      'Reconstruye la aceleración material sin omitir su parte convectiva ni confundir trayectoria y giro local.',
      'Verifica brazos de momento, signo de las presiones y criterio de estabilidad de flotación.',
      'Recupera condiciones de pared y contrasta caudal, esfuerzo y potencia sin intercambiar radio y diámetro.',
      'Diferencia mínima resistencia, mínima potencia y un ajuste empírico; comprueba qué incluye el coeficiente cuadrático.',
      'Separa frecuencia angular y frecuencia cíclica, amplitud y valor instantáneo, tiempo difusivo y período.',
      'Fija la frontera, usa la velocidad relativa donde corresponde y comprueba fuerza y potencia por balances distintos.',
      'Escribe los convenios de los coeficientes y distingue semejanza dimensional de una ley física medida.',
      'Comprueba el dominio de aplicación de Gauss y Stokes, especialmente cuando se excluye una singularidad.',
      'Verifica continuidad, referencias de presión y condiciones necesarias para aplicar Bernoulli.',
      'Distingue tracción y esfuerzo, flujo y caudal, y comprueba que la disipación no sea negativa.',
      'Sustituye el campo en la ecuación diferencial y en sus condiciones de contorno antes de evaluar números.',
      'Compara por separado inercia local y convectiva; declara la escala temporal empleada.',
      'Comprueba signos de Coriolis y estratificación; no deduzcas un umbral universal sin geometría y contorno.',
    ]
    for ch,title in enumerate(CHAPTERS,1):
        rows=[p for p in bank if p['ch']==ch]
        parts += [r'\chapter{'+title+'}',r'\objetivos{Aplicar los modelos del capítulo '+str(ch)+r' del manual; separar hipótesis, cálculo e interpretación. Los tres ejercicios abordan situaciones distintas.}']
        parts += [worked(p) for p in rows]
        parts += [r'\begin{tcolorbox}[studiumcheck,breakable=false,title={Síntesis y comprobación}]Modelos trabajados: '+ '; '.join(p['title'].lower() for p in rows)+r'.\par\textbf{Antes de continuar.} '+chapter_checks[ch-1]+r'\end{tcolorbox}']
    (ROOT/'content/problem-solutions.tex').write_text('\n\n'.join(parts)+'\n')
    problem_intro=r'''\noindent Este volumen contiene \textbf{48 problemas resueltos}, tres por capítulo, y \textbf{siete talleres de cálculo}. Los talleres retoman modelos del banco para enseñar verificación, unidades, integración y convergencia; no se cuentan como siete familias físicas adicionales.
\tableofcontents
\listoffigures
\mainmatter
\part{Problemas resueltos}
\input{../content/problem-solutions.tex}
\part{Talleres de cálculo reproducible}
\input{../content/computational-workshops.tex}
'''
    (ROOT/'latex/problemas.tex').write_text(shell('problemas','Problemas resueltos y talleres de cálculo',problem_intro))
    enunciados=[r'''\noindent Cuatro simulacros originales de \textbf{150 minutos}, con cinco problemas de dos puntos cada uno. Tiempo y puntuación son propuestas de entrenamiento. Las veinte variantes reutilizan familias del banco con datos distintos. Las soluciones están reunidas en la segunda parte, para permitir trabajar sin verlas.
\tableofcontents
\mainmatter
\part{Enunciados}
''']
    for i,group in enumerate(exams(),1):
        enunciados += [r'\chapter{Simulacro '+str(i)+'}',r'\objetivos{Resolver cinco situaciones de temas diferentes en 150 minutos. Reserva unos 25 minutos por problema y 25 minutos para comprobar.}',r'''Calculadora científica y una hoja de fórmulas propia permitidas. No se necesita ordenador. Cada problema vale 2 puntos: planteamiento e hipótesis, 0.5; ecuaciones y desarrollo, 0.75; resultados con unidades, 0.5; interpretación o comprobación, 0.25. Un error aritmético arrastrado se penaliza una sola vez si el procedimiento posterior es coherente.
''']
        for j,p in enumerate(group,1):
            enunciados += [r'\par\medskip\noindent\begin{minipage}{\linewidth}',r'\section{Problema '+str(j)+r' · 2 puntos}',p['question'],table(p,local=True),r'\par\medskip\textbf{Condiciones del modelo.} '+p['hypotheses'],r'\par\textit{Entrega: ecuaciones justificadas, resultados con unidades y una comprobación física o matemática.}',r'\end{minipage}\par\medskip']
        enunciados.append(r'\resumen{Antes de entregar, comprueba signos de las fuerzas, definición de cada número adimensional y carácter absoluto o manométrico de la presión.}')
    enunciados.append(r'\part{Soluciones razonadas}')
    for i,group in enumerate(exams(),1):
        enunciados += [r'\chapter{Soluciones del simulacro '+str(i)+'}',r'\objetivos{Comparar el planteamiento antes de consultar los resultados. La rúbrica valora el modelo, no sólo la cifra final.}']
        enunciados += [worked(p,True) for p in group]
        enunciados.append(r'\studiumchaptercheck')
    (ROOT/'content/exam-papers-and-solutions.tex').write_text('\n\n'.join(enunciados)+'\n')
    (ROOT/'latex/simulacros.tex').write_text(shell('simulacros','Cuatro simulacros originales y soluciones',r'\input{../content/exam-papers-and-solutions.tex}'))
    out=dict(provenance='Original hypothetical educational data; derived models; no official exams',gravity_m_s2=9.81,problems=bank,exams=exams())
    (ROOT/'content/fluid-bank.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
    print('48 worked cases and 20 exam variants rendered')
if __name__=='__main__':write()
