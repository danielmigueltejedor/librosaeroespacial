"""Importación nativa y trazabilidad sin elevar la autoridad PENDING."""
from pathlib import Path
import sys,json,re,hashlib
R=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(R/'framework/src'))
from studium.mcp.server import dispatch,open_workspace
W=R/'project';B=W/'mecanica-vuelo-ule';W.mkdir(exist_ok=True)
S=open_workspace(str(W),str(B) if B.exists() else None)
LOG=[]
def call(name,args):
    result=dispatch(name,args,session=S)
    LOG.append(dict(tool=name,arguments=args,result=result))
    (R/'reports/studium-api-progress.json').write_text(json.dumps(LOG,ensure_ascii=False,indent=2,default=str))
    if result.get('status') in ['error','mcp.invalid_input']:raise RuntimeError(str((name,result))[:1800])
    return result
def setup():
    if B.exists():raise RuntimeError('El proyecto ya existe: no se regenera ni sobrescribe')
    call('studium_project_create',dict(slug=B.name,course='Mecánica de Vuelo',university='Universidad de León',degree='Grado en Ingeniería Aeroespacial',language='es',profile='STEM',academic_year='2026/2027',course_code='0710325'))
    call('studium_course_document_record',dict(title='Guía docente oficial Mecánica de Vuelo ULE 2026/2027',url='https://guiadocenteapi.unileon.es/syllabuses/downloadPdf/2026-2027/0710325',text=(R/'work/texts/GUIA2026.txt').read_text()))
    chapters=[]
    for i in range(1,24):
        txt=(R/'content'/f'c{i:02}.tex').read_text();title=re.search(r'\\chapter\{([^}]+)\}',txt)[1]
        chapters.append(dict(id=f'c{i:02}',title=title))
    call('studium_blueprint_store',dict(sections=chapters))
    parts=[]
    for title,lo,hi in [('Fundamentos',1,3),('Ecuaciones del movimiento',4,6),('Planeadores',7,9),('Aerorreactores',10,14),('Hélices',15,16),('Operaciones',17,18),('Estabilidad estática y ampliación dinámica',19,21),('Simulación',22,23)]:
        parts.append(dict(id=f'P{lo}',title=title,chapters=[dict(id=c['id'],title=c['title'],learning_objectives=['Derivar, aplicar y comprobar los modelos del capítulo y sus límites.'],sections=[dict(id=c['id']+'.core',title='Fundamentos y aplicaciones',concepts=[dict(id=c['id']+'.model',title=c['title'],depth='UNDERGRADUATE',learning_objectives=['Relacionar hipótesis, ecuaciones, resultados y comprobaciones.'],exercises=2)])]) for c in chapters[lo-1:hi]]))
    call('studium_academic_blueprint_store',dict(parts=parts,subject='Mecánica de Vuelo',profile_key='UNDERGRADUATE'))
    call('studium_depth_plan',dict(academic_depth='UNDERGRADUATE',length='COMPREHENSIVE',exercises_with_solutions=True))
    ids={}
    for row in json.loads((R/'evidence/public-sources-initial.json').read_text()):
        if row['key']=='MIT-17':continue # Identificación/validación avanzada fuera de alcance del texto.
        text=(R/'work/texts'/f'{row["key"]}.txt').read_text()
        ret=call('studium_public_source_record',dict(title=row['title'],url=row['url'],kind='academic_open_notes',text='Notas abiertas consultadas; alcance de lectura en registro bibliográfico. No constituye respaldo automático de cada afirmación.'))
        pid=ret['candidate']['id']
        call('studium_public_source_open_supplement',dict(id=pid,open_supplement=True,open_licensed=True))
        # Una sola ancla literal de veinte palabras por documento; localización, no prueba semántica.
        quote=' '.join(text.split()[15:35])
        ev=call('studium_excerpt_record',dict(source_id=pid,url=row['url'],text=quote))
        ids[row['key']]=dict(public=pid,excerpt=ev['excerpt']['id'])
    src='simulations/jsbsim-upstream/src/models/FGAccelerations.cpp'
    url='https://github.com/JSBSim-Team/jsbsim/blob/v1.3.3/src/models/FGAccelerations.cpp'
    ret=call('studium_public_source_record',dict(title='JSBSim 1.3.3: ecuaciones y modelos, commit 66f7faf',url=url,kind='software_primary_source',text='Código realmente consultado. No valida experimentalmente el modelo ni los ejemplos originales.'))
    pid=ret['candidate']['id'];call('studium_public_source_open_supplement',dict(id=pid,open_supplement=True,open_licensed=True))
    ev=call('studium_excerpt_record',dict(source_id=pid,url=url,text=' '.join((R/src).read_text().split()[15:35])))
    ids['JSBSIM']=dict(public=pid,excerpt=ev['excerpt']['id'])
    (R/'evidence/studium-ids.json').write_text(json.dumps(ids,indent=2))
    print('Proyecto y fuentes nativas creados',flush=True)
def math():
    checks=[dict(kind='equivalence',left='A*V**2+B/V**2',right='(A*V**4+B)/V**2',symbols=['A','B','V']),
      dict(kind='derivative',function='A*V**2+B/V**2',variable='V',claimed='2*A*V-2*B/V**3',symbols=['A','B','V']),
      dict(kind='derivative',function='A*V**3+B/V',variable='V',claimed='3*A*V**2-B/V**2',symbols=['A','B','V']),
      dict(kind='derivative',function='atan(W*sqrt(B/A))/(g*cT*sqrt(A*B))',variable='W',claimed='1/(g*cT*(A+B*W**2))',symbols=['A','B','W','g','cT'],assumptions={k:['positive'] for k in ['A','B','W','g','cT']}),
      dict(kind='equivalence',left='(1/ei+pi*AR*kp)/(pi*AR)',right='1/(pi*AR*ei)+kp',symbols=['ei','AR','kp']),
      dict(kind='limit',expression='log(1+a2*V**2/a0)/(2*a2)',variable='a2',point='0',claimed='V**2/(2*a0)',symbols=['a2','V','a0'],assumptions={'V':['positive'],'a0':['positive']}),
      dict(kind='dimensions',expression='rho*V**2*S',symbol_units={'rho':'kg/m^3','V':'m/s','S':'m^2'},expected_unit='N'),
      dict(kind='dimensions',expression='1/(g*cT)',symbol_units={'g':'m/s^2','cT':'kg/(N*s)'},expected_unit='s'),
      dict(kind='dimensions',expression='1/(g*cP)',symbol_units={'g':'m/s^2','cP':'kg/J'},expected_unit='m')]
    out=[call('studium_math_verify',c) for c in checks]
    (R/'reports/studium-math.json').write_text(json.dumps(out,indent=2,ensure_ascii=False,default=str))
    print('Verificaciones nativas:',len(out),flush=True)
if __name__=='__main__':
    for mode in sys.argv[1:]:globals()[mode]()
