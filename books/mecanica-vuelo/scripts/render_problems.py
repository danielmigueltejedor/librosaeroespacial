from pathlib import Path
import json,re
import sympy as sp
R=Path(__file__).resolve().parents[1]
P=json.loads((R/'evidence/problem-bank.json').read_text())
units={'dimensionless':'','kg/s':r'\mathrm{kg\,s^{-1}}','kg':r'\mathrm{kg}','N':r'\mathrm N','N*m':r'\mathrm{N\,m}','Pa':r'\mathrm{Pa}','W':r'\mathrm W','m':r'\mathrm m','s':r'\mathrm s','m/s':r'\mathrm{m\,s^{-1}}','m/s^2':r'\mathrm{m\,s^{-2}}','kg/m^3':r'\mathrm{kg\,m^{-3}}','degree':r'{}^\circ','radian':r'\mathrm{rad}','1/radian':r'\mathrm{rad^{-1}}','1/s':r'\mathrm{s^{-1}}','1/s^2':r'\mathrm{s^{-2}}'}
levels={'BASIC':'Básico','INTERMEDIATE':'Intermedio','ADVANCED':'Avanzado','EXAM_LEVEL':'Nivel de examen'}
def num(value):
    x=format(value,'.7g')
    if 'e' in x:
        a,b=x.split('e');return a+r'\times10^{'+str(int(b))+'}'
    return x
def prose(t):
    t=t.replace("\u2011","-")
    for old,new in [('CL^(3/2)/CD',r'$C_L^{3/2}/C_D$'),('CL^(-1/2)',r'$C_L^{-1/2}$'),('W^(-3/2)',r'$W^{-3/2}$'),('W^(3/2)',r'$W^{3/2}$'),('n^(3/2)',r'$n^{3/2}$')]:t=t.replace(old,new)
    t=t.replace('0.2<=CL<=1.6',r'$0.2\leq C_L\leq1.6$').replace('(mg)^2',r'$ (mg_0)^2 $').replace('phi=theta=0',r'$\phi=\theta=0$')
    pieces=re.split(r'(\$[^$]*\$)',t)
    for i in range(0,len(pieces),2):
        z=pieces[i]
        # Etiquetas de variables en la explicación: mantenerlas en modo matemático.
        def subscript(m):
            token=m[0];head,*tail=token.split('_')
            return '$'+head+'_{'+','.join(tail)+'}$'
        z=re.sub(r'\b[A-Za-z]+(?:_[A-Za-z0-9]+)+\b',subscript,z)
        z=re.sub(r'(?<![$\\])\b([A-Za-z]+)\^([A-Za-z0-9]+)',lambda m:'$'+m[1]+'^{'+m[2]+'}$',z)
        pieces[i]=z
    return ''.join(pieces)
def solution(p,include_prompt=True):
    out=[]
    if include_prompt:
        out+=[r'\section{'+p['key']+' · '+p['title']+'}',r'\noindent\textbf{Nivel:} '+levels[p['level']]+'.',r'\apartado{1. Enunciado}{'+prose(p['prompt'])+'}']
    fields=[('2. Datos',p['data']),('3. Incógnitas',p['unknown']),('4. Sistema de referencia',p['frame']),('5. Hipótesis físicas',p['hyp']),('6. Modelo matemático',p['model'])]
    out += [r'\apartado{'+k+'}{'+prose(v)+'}' for k,v in fields]
    out += [r'\apartado{7. Ecuaciones simbólicas}{Se parte de los balances y definiciones siguientes.}']
    for eq in p['eqs']:out += [r'\begin{equation}'+eq+r'\end{equation}']
    out += [r'\apartado{8. Desarrollo algebraico}{Las operaciones se realizan en este orden, conservando las condiciones del modelo.}',r'\begin{enumerate}']
    out += [r'\item '+prose(x) for x in p['steps']]
    out += [r'\end{enumerate}',r'\apartado{9. Sustitución numérica}{Se usan las magnitudes del apartado de datos en SI; los ángulos se convierten a radianes antes de evaluar funciones trigonométricas. Las densidades indicadas como ISA se obtienen de la capa correspondiente.}']
    short=0
    for t in p['tests']:
        if len(t['expression'])<60 and short<3:
            tex=sp.latex(sp.sympify(t['expression'],evaluate=False))
            out += [r'\noindent '+prose(t['name'])+r':\quad $'+tex+r'\simeq '+num(t['expected'])+r'\,'+units[t['unit']]+r'$.\par']
            short+=1
    if not short:out += ['La evaluación conserva los parámetros intermedios sin redondear. El registro de cálculo del proyecto incluye la sustitución completa que reproduce cada valor de la tabla siguiente.']
    out += [r'\apartado{10. Resultados con unidades}{Los resultados pertenecen al modelo y al intervalo de datos declarados.}',r'\begin{center}\begin{tabular}{lr}\toprule Magnitud&Resultado\\\midrule']
    for t in p['tests']:out += [prose(t['name'])+' & $'+num(t['expected'])+r'\,'+units[t['unit']]+r'$\\']
    out += [r'\bottomrule\end{tabular}\end{center}',r'\apartado{11. Interpretación}{'+prose(p['interpretation'])+'}',r'\apartado{12. Comprobación independiente y alcance}{'+prose(p['independent'])+'}',r'\apartado{13. Limitaciones}{'+prose(p['limits'])+'}']
    out += [r'\par\smallskip\noindent{\footnotesize\textit{Datos y solución originales. Las sustituciones registradas se reproducen con SymPy y Studium; eso no establece validación experimental ni revisión experta.}}']
    return '\n\n'.join(out)+'\n'

body=[]
for level in levels:
    body += [r'\chapter{'+levels[level]+'}']
    body += [solution(p) for p in P if p['level']==level]
(R/'content/problems.tex').write_text('\n\n'.join(body))
(R/'problemas.tex').write_text(r'''\input{latex/preamble}
\hypersetup{pdftitle={Problemas resueltos de Mecánica de Vuelo},pdfauthor={Studium}}
\begin{document}
\portada{CUADERNO DE PROBLEMAS}{PROBLEMAS RESUELTOS\\DE MECÁNICA DE VUELO}{Colección original · Fundamentos, actuaciones y estabilidad}
\frontmatter
\chapter*{Cómo usar la colección}
Esta colección contiene 43 problemas originales con datos docentes. Se distribuye en niveles básico, intermedio, avanzado y de examen. Cada solución declara sistema de referencia, hipótesis, ecuaciones, desarrollo, resultados, comprobación y límites. Los ejercicios no son exámenes oficiales ni soluciones de las prácticas evaluables facilitadas.

La comprobación propuesta puede utilizar un balance, un límite, una cuadratura o un método numérico distinto. Cuando una magnitud procede de una raíz u optimización, reproducir su literal no verifica el algoritmo: se conserva esa distinción en el registro. La revisión experta independiente permanece pendiente.
\input{assets/cover-credit.tex}
\tableofcontents
\mainmatter
\input{content/problems}
\end{document}
''')
print('Cuaderno redactado:',len(P))
