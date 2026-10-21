"""Render the public 105-case bank as editable companion books.

The four training papers select twenty existing cases, not new variants or
official exams. No private authoring stores or downloaded sources are read.
"""
from pathlib import Path
import json
import re
import difflib
import hashlib
import sympy as sp
from sympy.parsing.sympy_parser import parse_expr

BOOK = Path(__file__).resolve().parents[1]
ROOT = BOOK.parents[1]
BANK = ROOT / 'reports/bundle-audit/structures-problem-bank.json'
import sys
sys.path.insert(0,str(ROOT/'scripts'))
from solution_steps import numeric_steps
REASONING=json.loads((BOOK/'solutions/reasoning.json').read_text())
CHAPTERS = [
    'Introducción: rigidez y masa', 'Tensión y deformación',
    'Modelo monodimensional', 'Esfuerzo axil y momento flector',
    'Momento torsor', 'Esfuerzo cortante',
    'Energía elástica de deformación', 'Elasticidad tridimensional',
]
CHECKS = [
    'Reconstruye el área desde la rigidez axial y comprueba la masa con la densidad; compara a igual rigidez y longitud.',
    'Distingue tensión, deformación y desplazamiento. Comprueba el signo de la contracción transversal y la definición de cortadura ingenieril.',
    'Verifica las tres ecuaciones de equilibrio, los saltos de cortante y momento y las condiciones de cada apoyo o rótula.',
    'Fija los ejes centroidales y el signo del axil y del flector. Comprueba la posición del eje neutro y la fibra extrema.',
    'Distingue secciones abiertas y cerradas: la constante torsional de tiras abiertas no es el momento polar. En multiceldas, exige equilibrio y giro compatible.',
    'Conserva el sentido del recorrido de cada pared y distingue flujo de cortante y tensión. Si la carga no pasa por el centro de cortadura, incluye el torsor adicional.',
    'Aplica fuerza virtual para flecha y momento virtual para giro. Mantén las cargas auxiliares hasta después de derivar y separa los tramos de distinta rigidez.',
    'Incluye la tercera tensión principal al evaluar Tresca y von Mises. Comprueba los invariantes antes y después de girar los ejes.',
]
PAPERS = [
    ['PRB-0148','PRB-0151','PRB-0190','PRB-0208','PRB-0232'],
    ['PRB-0152','PRB-0202','PRB-0123','PRB-0225','PRB-0239'],
    ['PRB-0150','PRB-0192','PRB-0165','PRB-0224','PRB-0236'],
    ['PRB-0153','PRB-0207','PRB-0212','PRB-0216','PRB-0175'],
]
ORIGINAL_FIGURES = {}
TITLES = {
    200:'Sección en T y flexión simple', 201:'Sección abierta no simétrica',
    202:'Flexión desviada de un rectángulo',203:'Cajón rectangular y eje neutro',
    204:'T invertida bajo flector negativo',205:'Doble T de alas desiguales',
    206:'Angular y centroide',207:'Flexión compuesta con compresión',
    208:'Cajón cerrado de espesor uniforme',209:'Cajón de espesores distintos',
    210:'Cajón bicelular asimétrico',211:'Perfil abierto en U',
    212:'Cajón cerrado cuadrado',213:'Cajón bicelular simétrico',
    214:'Angular abierto en torsión',215:'Cajón bicelular y pared común',
    216:'C abierto y centro de cortadura',217:'Perfil abierto en Z',
    218:'Cajón unicelular no uniforme',219:'Cajón idealizado con larguerillos',
    220:'Sección abierta en T',221:'Angular con dos cortantes',
    222:'Cortante en un cajón bicelular',223:'C abierta idealizada con larguerillos',
}

def collect_manual_figures(bank):
    """Keep published load, section, elastic-curve and Mohr drawings with cases."""
    source=(BOOK/'latex/manual.tex').read_text()
    def norm(s):
        s=s.replace(r'\(','').replace(r'\)','').replace('$','').replace('{','').replace('}','')
        s=re.sub(r'\\([A-Za-z]+)',r'\1',s)
        return re.sub(r'\W+','',s.lower())
    bindings=[];seen=set()
    for m in re.finditer(re.escape(r'\noindent\textbf{Enunciado}'),source):
        prompt_text=source[m.end():].lstrip().split('\n\n')[0]
        scores=sorted((difflib.SequenceMatcher(None,norm(prompt_text),norm(p['prompt'])).ratio(),p['id']) for p in bank)
        score,id=scores[-1];assert score>.84 and id not in seen,(score,id)
        seen.add(id)
        p=next(p for p in bank if p['id']==id)
        if p['ch'] not in ['c03','c04','c07','c08']:continue
        a=source.rfind(r'\begin{tcolorbox}',0,m.start());depth=0;b=None
        for token in re.finditer(r'\\(begin|end)\{tcolorbox\}',source[a:]):
            depth+=1 if token[1]=='begin' else -1
            if depth==0:b=a+token.end();break
        assert b
        block=source[a:b];data_pos=block.find(r'\noindent\textbf{Datos}')
        drawings=[]
        for match in re.finditer(r'\\noindent\\begin\{minipage\}\{\\linewidth\}.*?\\end\{minipage\}',block,re.S):
            if r'\begin{tikzpicture}' not in match[0]:continue
            drawings.append((match.start()<data_pos,match[0]))
        if drawings:
            ORIGINAL_FIGURES[id]=drawings
            bindings.append(dict(problem=id,figures=len(drawings),prompt_match=score,source_sha256=hashlib.sha256(block.encode()).hexdigest()))
    assert len(seen)==105
    (BOOK/'content/manual-figure-bindings.json').write_text(json.dumps(bindings,indent=2)+'\n')

def manual_figures(p, statement):
    return '\n\n'.join(r'\par\medskip'+s+r'\par\medskip' for before,s in ORIGINAL_FIGURES.get(p['id'],[]) if before==statement)

def text(s):
    """Escape prose outside inline mathematics, keeping authored TeX intact."""
    s=str(s).replace('Conservar el signo del flector del ejemplo anterior.',
                     'Arrastrar el signo del flector de otro caso sin comprobarlo.')
    chunks = re.split(r'(\$[^$]*\$)', str(s))
    for i in range(0, len(chunks), 2):
        t = chunks[i].replace('−','-').replace('×',r'\ensuremath{\times}')
        t = t.replace('√',r'\ensuremath{\sqrt{\vphantom{3}}}').replace('≈',r'\ensuremath{\approx}')
        t = t.replace('²',r'\textsuperscript{2}').replace('³',r'\textsuperscript{3}')
        t = t.replace('τ',r'\ensuremath{\tau}').replace('Σ',r'\ensuremath{\Sigma}')
        t = re.sub(r'\^(-?\d+)', lambda m: r'\textsuperscript{'+m[1]+'}', t)
        t = re.sub(r'(?<!\\)_',r'\_',t)
        chunks[i] = t
    return ''.join(chunks)

def unit(s):
    if not s or s == '1': return ''
    if s == 'deg': return r'{}^{\circ}'
    return r'\,\mathrm{'+s.replace(' ',r'\,')+'}'

def number(s):
    s = str(s)
    if 'e' in s.lower():
        a,b=s.lower().split('e'); return a+r'\times10^{'+str(int(b))+'}'
    return s

def mathtex(s):
    return '\n'.join(line for line in s.splitlines() if line.strip())

def result_tex(s):
    s=mathtex(s)
    if len(s)>150 and r'\begin' not in s:
        parts=re.split(r'[,;]?\s*\\(?:qquad|quad)\s*',s)
        if len(parts)>1:return r'\begin{gathered}'+r'\\'.join(parts)+r'\end{gathered}'
    return s

def numerical_lines(expression, expected, units):
    """Show long numerical substitutions through exact named intermediate steps."""
    expr=parse_expr(expression,evaluate=False)
    definitions=[]
    def split(node, force=False):
        if not force and len(sp.latex(node))<=150:return node
        args=[]
        for arg in node.args:
            args.append(split(arg,True) if arg.args and len(sp.latex(arg))>45 else arg)
        short=node.func(*args,evaluate=False) if node.args else node
        name=sp.Symbol('a_{'+str(len(definitions)+1)+'}')
        definitions.append((name,short))
        return name
    short=split(expr)
    restored=short
    for name,value in reversed(definitions):restored=restored.xreplace({name:value})
    assert sp.simplify(restored-expr)==0, expression
    out=[sp.latex(a)+'='+sp.latex(b) for a,b in definitions]
    out.append(sp.latex(short)+r'\approx '+number(expected)+unit(units))
    return out

def symbol(s):
    names={'rho':r'\rho','nu':r'\nu','epsilon_a':r'\varepsilon_a'}
    if s in names: return names[s]
    s=re.sub(r'^(sigma|tau|theta|epsilon|phi)(?=_|$)',lambda m:'\\'+m[0],s)
    if '_' in s:
        a,b=s.split('_',1);s=a+'_{'+b.replace('_',r'\,')+'}'
    return s

def table(p, local=False):
    env='tabular'
    out=[r'\par\medskip\noindent\begin{'+env+r'}{@{}p{.18\linewidth}p{.26\linewidth}p{.48\linewidth}@{}}',
         r'\toprule Símbolo & Valor y unidad & Significado\\\midrule']
    for d in p['solution']['given']:
        out.append('$'+symbol(d['symbol'])+'$ & $'+number(d['value'])+unit(d['unit'])+'$ & '+text(d['meaning'])+r'\\')
    return '\n'.join(out+[r'\bottomrule\end{'+env+r'}\par\medskip'])

def prompt(p):
    s=p['prompt']
    s=s.replace('Repita el cálculo del ejemplo para un tirante','Considere un tirante')
    s=s.replace('con la misma rigidez axial','con rigidez axial')
    s=s.replace('La barra del ejemplo anterior','Una barra')
    s=s.replace('El árbol tubular del ejemplo','Un árbol tubular')
    s=s.replace('En el perfil en C del ejemplo','En un perfil en C')
    s=s.replace('4√3',r'$4\sqrt{3}$').replace('mm4',r'mm$^4$')
    return text(s)

def diagram(p):
    g=p.get('thin_wall_geometry')
    if not g:return ''
    pts=g['nodes'];xs=[v[0] for v in pts.values()];ys=[v[1] for v in pts.values()]
    scale=min(4.5/(max(xs)-min(xs)),3/(max(ys)-min(ys)))
    out=[r'\par\medskip\noindent\begin{minipage}{\linewidth}\centering',r'\begin{tikzpicture}[>=Stealth]']
    for name,(z,y) in pts.items():
        x=(z-min(xs))*scale;yy=-(y-min(ys))*scale
        out.append(f'\\coordinate ({name}) at ({x:.5f},{yy:.5f});')
        out.append(r'\fill ('+name+r') circle (1.5pt) node[above right,font=\small]{'+name+'};')
    for i,w in enumerate(g['walls'],1):
        out.append(r'\draw[->,very thick,studiumBlue] ('+w['from']+') -- ('+w['to']+r') node[midway,fill=white,font=\small]{$t_'+str(i)+'$};')
    out += [r'\draw[->] (-1,.3)--(-.2,.3) node[above]{$z$};',
            r'\draw[->] (-1,.3)--(-1,-.5) node[left]{$y$};',r'\end{tikzpicture}',
            r'\par\small Nudos $(z,y)$ en mm: '+ '; '.join('$'+n+'=('+str(v[0])+','+str(v[1])+')$' for n,v in pts.items())+'.',
            r'\par\small Flechas: sentido positivo de $q(s)$; $s=0$ en el nudo inicial de cada pared.']
    if g.get('booms'):
        out.append(r'\par\small Larguerillos: '+ '; '.join('$A_{'+b['at']+'}='+str(b['area'])+r'\,\mathrm{mm^2}$' for b in g['booms'])+'.')
    if g.get('cells'):
        out.append(r'\par\small Recorridos de célula: '+ '; '.join('$'+r'\to '.join(c)+'$' for c in g['cells'])+'.')
    out += [r'\par\normalsize\end{minipage}\par\medskip']
    return '\n'.join(out)

def items(title, rows):
    if not rows:return ''
    return r'\textbf{'+title+r'.}\begin{itemize}'+'\n'.join(r'\item '+text(x) for x in rows)+r'\end{itemize}'

def worked(p, exam=False, closing=None):
    s=p['solution']; title=p['id']+' · '+text(TITLES.get(int(p['id'].split('-')[1]),s['unknown'].capitalize()))
    out=[r'\Needspace{.3\textheight}',r'\begin{studiumworked}{'+p['id']+'}',r'\section{'+title+'}',
         r'\textbf{Enunciado.} '+prompt(p),table(p),diagram(p),manual_figures(p,True),
         items('Hipótesis',s['assumptions']),r'\textbf{Modelo y desarrollo.}']
    for m in s['model']:
        out += [text(m['name'])+r'.\[\fitmath{'+mathtex(m['latex'])+r'}\]']
    development=[x.replace('Comprobación independiente por Castigliano','Contraste por Castigliano') for x in s.get('development',[])]
    if p['id'] in REASONING:out.append(r'\textbf{Elección del procedimiento.} '+REASONING[p['id']])
    out += [items('Procedimiento',development),r'\textbf{Cálculo de los pasos.}']
    rows=[dict(target=f'y_{i}',expression=step.get('expression'),equation=step.get('equation'),expected=step.get('expected'),unit=step.get('unit',''),why=text(step['text'])+'.') for i,step in enumerate(s['steps'],1)]
    calculated,_=numeric_steps(rows)
    out.append(calculated)
    out += [manual_figures(p,False),r'\textbf{Resultado e interpretación.}\[\fitmath{'+result_tex(s['result'])+r'}\]',text(s['interpretation']),
            r'\par\textbf{Comprobación.} '+(CHECKS[int(p['ch'][1:])-1] if exam else 'Recalcula los pasos con unidades coherentes y aplica el control específico indicado en la orientación del capítulo.'),
            r'\par\noindent\begin{minipage}{\linewidth}' if closing else '',
            items('Límites',s['limitations']),items('Errores frecuentes',s['mistakes'])]
    if closing:
        out += [r'\begin{tcolorbox}[studiumcheck,breakable=false,title={Síntesis y comprobación}]'+closing+r'\end{tcolorbox}',r'\end{minipage}']
    out += [r'\end{studiumworked}']
    return '\n\n'.join(x for x in out if x)

FRONT=r'''\chapter*{Presentación y convenios}\addcontentsline{toc}{chapter}{Presentación y convenios}
Estos cuadernos acompañan al manual de Teoría de Estructuras de Studium y siguen sus ocho temas. Se reúne el banco de \textbf{105 ejercicios del manual} en un volumen separado, con sus identificadores públicos y soluciones. No se presentan como 105 ejercicios adicionales ni como preguntas oficiales.

Los valores de módulos, densidades, límites y cargas son \textbf{datos académicos de los enunciados}. Incluso cuando se usa el nombre de una aleación, no constituyen valores admisibles certificados de diseño. Cada conclusión se condiciona a las hipótesis indicadas.

La tensión normal es positiva a tracción. En las secciones de pared delgada se usan $z$ a la derecha e $y$ hacia abajo, con flujos firmados según las flechas del esquema. Los resultados de resistencia no incluyen automáticamente pandeo, fatiga, uniones o concentraciones de tensiones.

En cada cálculo conserva una combinación coherente de unidades: $\mathrm{N,mm,MPa}$, con $1\,\mathrm{MPa}=1\,\mathrm{N/mm^2}$, o bien unidades SI. Convierte $\mathrm{kN}$, $\mathrm{GPa}$ y metros antes de sustituir. La energía $\mathrm{N\,mm}$ equivale a $10^{-3}\,\mathrm{J}$; un giro se expresa en radianes. Las expresiones numéricas usan las unidades convertidas del modelo, que pueden diferir de las de la tabla. Los dígitos impresos conservan el redondeo del banco y no representan precisión experimental.
'''
BACK=r'''\backmatter
\chapter*{Procedencia y comprobaciones}\addcontentsline{toc}{chapter}{Procedencia y comprobaciones}
La fuente de estos cuadernos es el banco público de ejercicios originales del manual de Teoría de Estructuras de esta colección, segunda edición completa. Se conserva en \path{reports/bundle-audit/structures-problem-bank.json}, dentro del repositorio \url{https://github.com/danielmigueltejedor/librosaeroespacial}. Los enunciados se han hecho autónomos retirando remisiones como «el ejemplo anterior» cuando los datos ya estaban presentes. Los esquemas de pared delgada se trazan desde las coordenadas del banco y sus flechas fijan el recorrido de las leyes de flujo.

Las ecuaciones y resultados son derivados de los modelos escritos; sus interpretaciones son condicionales. El informe reproducible registra 405 controles sobre los 105 casos, incluyendo aritmética con redondeo, ocho geometrías de cortante y contrastes seleccionados de energía y elasticidad. Los simulacros seleccionan veinte de esos mismos casos, sin atribuirles variantes numéricas ni comprobaciones independientes adicionales.

Revisión y maquetación: 18 de octubre de 2026. Las comprobaciones las realizó el mismo agente autor en una pasada de cálculo distinta. No se atribuye revisión académica independiente ni validación experimental. La bibliografía de teoría y sus condiciones de uso se conservan en el manual; este cuaderno no incorpora nuevas fuentes teóricas ni sustituye la lectura del modelo.
'''

def shell(kind,subtitle,body):
    return r'''\documentclass[10pt,a4paper,openany]{book}
\input{../../../shared/latex/studium-editorial.tex}
\usepackage{needspace}
\input{editorial-config.tex}
\renewcommand{\studiumvolumetype}{'''+kind+r'''}
\hypersetup{pdftitle={Teoría de Estructuras - '''+subtitle+r'''}}
\begin{document}
\studiumcover{TEORÍA\\DE ESTRUCTURAS}{'''+subtitle+'}{'+('PROBLEMAS RESUELTOS' if kind=='problemas' else 'SIMULACROS')+r'''}
\frontmatter
\studiumreadingguide
'''+FRONT+body+BACK+r'\end{document}'+'\n'

def write():
    bank=json.loads(BANK.read_text())['problems']; lookup={p['id']:p for p in bank}
    assert len(bank)==105 and len(set(sum(PAPERS,[])))==20
    assert {lookup[i]['ch'] for i in sum(PAPERS,[])}=={f'c{i:02d}' for i in range(1,9)}
    (BOOK/'content').mkdir(exist_ok=True)
    collect_manual_figures(bank)
    parts=[]
    for i,title in enumerate(CHAPTERS,1):
        group=sorted((p for p in bank if p['ch']==f'c{i:02d}'),key=lambda p:p['id'])
        parts += [r'\chapter{'+title+'}',r'\objetivos{'+CHECKS[i-1]+'}']
        parts += [worked(p,closing=CHECKS[i-1] if j==len(group)-1 else None) for j,p in enumerate(group)]
    (BOOK/'content/problem-solutions.tex').write_text('\n\n'.join(parts)+'\n')
    (BOOK/'latex/problemas.tex').write_text(shell('problemas','105 problemas resueltos',r'\tableofcontents\mainmatter\input{../content/problem-solutions.tex}'+'\n'))
    parts=[r'''\noindent Cuatro simulacros de \textbf{150 minutos y diez puntos}. Son selecciones de entrenamiento del banco de problemas, con los mismos datos, no exámenes oficiales ni variantes inéditas. Los cuatro cubren conjuntamente los ocho temas; cada prueba combina cinco casos de varios capítulos. Las soluciones aparecen en la segunda parte.
\tableofcontents\mainmatter\part{Enunciados}
''']
    for i,ids in enumerate(PAPERS,1):
        parts += [r'\chapter{Simulacro '+str(i)+'}',r'\objetivos{Trabaja sin consultar las soluciones; reserva 25 minutos por problema y 25 minutos para comprobaciones.}',
                  r'Calculadora y una hoja propia de fórmulas permitidas. Cada problema vale 2 puntos: hipótesis y planteamiento, 0.5; desarrollo, 0.75; resultado con unidades, 0.5; comprobación e interpretación, 0.25. Penaliza un error arrastrado una sola vez si el procedimiento posterior es coherente. El tiempo y la rúbrica son propuestas de entrenamiento.']
        for j,id in enumerate(ids,1):
            p=lookup[id]
            # Manual drawings can contain solved reactions or stress values;
            # only the new unsolved node/geometry diagrams belong in the papers.
            parts += [r'\par\medskip\noindent\begin{minipage}{\linewidth}',r'\section{Problema '+str(j)+r' · 2 puntos}',prompt(p),table(p,True),diagram(p),
                      r'\par\textbf{Hipótesis de trabajo.} '+text('; '.join(p['solution']['assumptions']))+'.',r'\par\textit{Entrega: modelo, desarrollo, unidades y una comprobación. Caso del banco: '+id+r'.}\end{minipage}\par\medskip']
        parts += [r'\resumen{Antes de entregar, revisa equilibrio, apoyos, signos, unidades y condiciones de validez. Distingue giro, flecha, flujo y tensión.}']
    parts += [r'\part{Soluciones razonadas}']
    for i,ids in enumerate(PAPERS,1):
        parts += [r'\chapter{Soluciones del simulacro '+str(i)+'}',r'\objetivos{Contrasta primero el modelo y después las cifras; aplica la rúbrica del enunciado.}']
        parts += [worked(lookup[id],True) for id in ids]
    (BOOK/'content/exam-papers-and-solutions.tex').write_text('\n\n'.join(parts)+'\n')
    (BOOK/'latex/simulacros.tex').write_text(shell('simulacros','Cuatro simulacros de entrenamiento y soluciones',r'\input{../content/exam-papers-and-solutions.tex}'+'\n'))
    (BOOK/'content/exam-selections.json').write_text(json.dumps({'source':str(BANK.relative_to(ROOT)),'kind':'selections, same case data, not new variants','duration_minutes':150,'points':10,'papers':PAPERS},indent=2)+'\n')
    print('Rendered 105 solutions and four training papers selecting twenty cases')

if __name__=='__main__':write()
