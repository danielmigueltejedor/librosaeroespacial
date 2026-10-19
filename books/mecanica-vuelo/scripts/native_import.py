"""Registra el manuscrito completo y los problemas, sin certificar sus fuentes."""
from pathlib import Path
import json,re,hashlib
from studium_project import call,LOG,R
ids=json.loads((R/'evidence/studium-ids.json').read_text())
def nm(t):return re.sub(r'(?<!\\)\$([^$]+)\$',lambda m:r'\('+m[1]+r'\)',t)
def arguments(text,start,n):
    vals=[];pos=start
    for _ in range(n):
        while pos<len(text) and text[pos].isspace():pos+=1
        if pos>=len(text):raise ValueError('Fin de argumento')
        if text[pos]!='{':
            # TeX permite un token sin llaves: por ejemplo, la unidad m.
            if text[pos]=='\\':
                token=re.match(r'\\[A-Za-z]+',text[pos:])[0]
            else:token=text[pos]
            vals.append(token);pos+=len(token);continue
        depth=1;beg=pos+1;pos+=1
        while pos<len(text) and depth:
            if text[pos]=='{' and text[pos-1]!='\\':depth+=1
            elif text[pos]=='}' and text[pos-1]!='\\':depth-=1
            pos+=1
        vals.append(text[beg:pos-1])
    return vals,pos
def expand(t):
    return re.sub(r'\\input\{([^}]+)\}',lambda m:expand((R/(m[1]+('' if m[1].endswith('.tex') else '.tex'))).read_text()),t)
def standard(t):
    t=t.replace('\u2011','-')
    commands={'SIu':1,'texttt':1,'vect':1,'dd':0,'apartado':2,'objetivos':1,'hipotesis':1,'verifica':1,'resumen':1,'fuentes':1,'repaso':2,'caso':2,'caja':2,'consejo':2,'errorcomun':1,'ilustra':2,'figura':2}
    pat=re.compile(r'\\('+'|'.join(commands)+r')(?![A-Za-z])')
    pos=0;out=[]
    while (m:=pat.search(t,pos)):
        out.append(t[pos:m.start()]);name=m[1];n=commands[name]
        if not n:out.append(r'\mathrm{d}');pos=m.end();continue
        vals,pos=arguments(t,m.end(),n)
        vals=[standard(x) for x in vals]
        if name=='SIu':v=r'\,\mathrm{'+vals[0]+'}'
        elif name=='texttt':v='`'+vals[0].replace(r'\_', '_')+'`'
        elif name=='vect':v=r'\boldsymbol{'+vals[0]+'}'
        elif name in ['ilustra','figura']:v='Figura original en la edición maquetada: '+vals[1]
        elif n==2:v=r'\textbf{'+vals[0]+'}. '+vals[1]
        else:v=vals[0]
        out.append(v)
    out.append(t[pos:]);return ''.join(out)
def refs(ch):
    k=('MIT-3' if ch<=3 else 'MIT-4' if ch<=6 else 'MIT-1' if ch<=18 else 'MIT-2' if ch==19 else 'MIT-8' if ch==20 else 'MIT-6' if ch==21 else 'JSBSIM')
    other='JSBSIM' if k!='JSBSIM' else 'MIT-4'
    return [ids[k]['excerpt'],ids[other]['excerpt']]
def paragraphs():
    rows=[]
    for n in range(1,24):
        original=expand((R/'content'/f'c{n:02}.tex').read_text())
        txt=standard(original)
        txt=re.sub(r'\\chapter\{[^{}]+\}(?:\\label\{[^{}]+\})?','',txt)
        for j,para in enumerate(re.split(r'\n\s*\n',txt)):
            if not para.strip():continue
            rr=call('studium_paragraph_record',dict(section=f'c{n:02}',text=nm(para.strip()),excerpts=refs(n),role='explanation'))
            rows.append(dict(chapter=n,paragraph=j,result=rr))
        (R/'evidence/native-paragraphs.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2,default=str))
        print('Capítulo nativo:',n,flush=True)
    (R/'evidence/native-content-sha256.json').write_text(json.dumps({str(p.relative_to(R)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted((R/'content').glob('*.tex'))},indent=2))
def problems():
    bank=json.loads((R/'evidence/problem-bank.json').read_text());exam=json.loads((R/'evidence/exam-bank.json').read_text());manual=json.loads((R/'evidence/manual-workshops.json').read_text())
    allp=bank+manual+[q for e in exam for q in e['questions']]
    rows=[];computations=[]
    for p in allp:
        ch=p['ch'] if p['key'].startswith(('P','T')) else (3 if p['key'].startswith('S01') else 12 if p['key'].startswith('S02') else 16 if p['key'].startswith('S03') else 17 if p['key'].startswith('S04') else 21 if p['key'].startswith('S05') else 23)
        t0=p['tests'][0];ex=refs(ch)
        steps=[dict(text=nm(standard(s))) for s in p['steps']]
        steps += [dict(text='Sustitución aritmética de datos originales del caso. No valida aplicabilidad.',expression=t['expression'],expected=format(t['expected'],'.12g'),unit=t['unit']) for t in p['tests'][1:]+p['tests'][:1]]
        sol=dict(given=[],unknown=p['unknown'],assumptions=[p['hyp'],p['frame']],model=[dict(name=p['model'],latex=standard(p['eqs'][0]),symbolic=t0['expression'])],development=[standard(x) for x in p['eqs']],steps=steps,result='Y='+format(t0['expected'],'.12g'),interpretation=nm(p['interpretation']+' '+p['independent']),limitations=[p['limits'],'Las dos citas son anclas de contexto de fuentes distintas; no contienen los resultados originales ni constituyen dos soluciones independientes.'],mistakes=['Confundir unidades, sistemas de referencia o leyes de vuelo.'])
        rr=call('studium_problem_record',dict(section=f'c{ch:02}',prompt=p['key']+' '+nm(standard(p['prompt'])),expected=format(t0['expected'],'.12g'),excerpts=ex,role='worked' if p['key'].startswith('T') else 'practice',difficulty='FOUNDATIONAL' if p['level']=='BASIC' else p['level'],problem_type='MULTI_STEP',method=p['model'],solution=sol))
        if 'problem' not in rr:raise RuntimeError(str(rr))
        pid=rr['problem']['id'];ck=call('studium_problem_check',dict(id=pid))
        rows.append(dict(key=p['key'],record=rr,check=ck))
        for t in p['tests']:
            co=call('studium_computation_check',dict(section=f'c{ch:02}',problem_id=pid,expression=t['expression'],result=format(t['expected'],'.12g')))
            computations.append(dict(key=p['key'],name=t['name'],result=co))
        (R/'evidence/native-problems.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2,default=str))
        (R/'reports/native-computations.json').write_text(json.dumps(computations,ensure_ascii=False,indent=2,default=str))
        print('Problema nativo:',p['key'],flush=True)
    print('Problemas nativos:',len(rows),'controles:',len(computations),flush=True)
def figures():
    rows=[]
    source=r'''\draw[->] (-2,0)--(2,0) node[right] {$x_w$};
\draw[->] (0,1.5)--(0,-1.5) node[below] {$z_w$};
\draw[->,thick,blue] (0,0)--(1.3,0) node[above] {$V$};
\draw[->,thick] (0,0)--(-1,0) node[above] {$D$};
\draw[->,thick] (0,0)--(0,1.1) node[right] {$L$};'''
    rr=call('studium_figure_record',dict(section='c07',caption='Esquema original de direcciones en ejes viento; magnitudes de flechas ilustrativas.',kind='tikz',source=source,excerpts=refs(7),key='fuerzas-viento-nativo'))
    ck=call('studium_figure_check',dict(id=rr['figure']['id']));rows.append(dict(record=rr,check=ck))
    source='''import matplotlib\nmatplotlib.use("Agg")\nimport matplotlib.pyplot as plt\nimport numpy as np\nx=np.linspace(0.05,1.5,200)\nplt.plot(x,0.024+0.046*x*x)\nplt.xlabel("Coeficiente de sustentacion")\nplt.ylabel("Coeficiente de resistencia")\nplt.tight_layout()\nplt.savefig("figure.pdf")\n'''
    rr=call('studium_figure_record',dict(section='c04',caption='Polar parabólica docente original; parámetros definidos como ejemplo, sin identificación experimental.',kind='python',source=source,excerpts=refs(4),key='polar-nativa'))
    ck=call('studium_figure_check',dict(id=rr['figure']['id']));rows.append(dict(record=rr,check=ck))
    (R/'reports/native-figures.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2,default=str))
def reports():
    for name in ['studium_scientific_contract_report','studium_equation_report','studium_book_quality_audit','studium_quality_report','studium_book_review','studium_section_completeness','studium_book_next','studium_verify']:
        rr=call(name,dict(mode='full') if name=='studium_verify' else {})
        (R/'reports'/f'{name}.json').write_text(json.dumps(rr,ensure_ascii=False,indent=2,default=str))
        print(name,rr.get('status'),flush=True)
def render():
    rr=call('studium_render',{})
    (R/'reports/native-render.json').write_text(json.dumps(rr,ensure_ascii=False,indent=2,default=str));print(rr,flush=True)
if __name__=='__main__':
    import sys
    for mode in sys.argv[1:]:globals()[mode]()
