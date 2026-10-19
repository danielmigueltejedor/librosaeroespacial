"""Registro nativo. Conserva autoridad PENDING y estado de revisión; no fuerza publicación."""
from pathlib import Path
import sys,json,re,hashlib,math,subprocess
R=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(R/'framework/src'))
from studium.mcp.server import dispatch,open_workspace
W=R/'project';B=W/'materiales-mantenimiento-ule';W.mkdir(exist_ok=True)
S=open_workspace(str(W),str(B) if B.exists() else None)
LOG=[]
def call(n,a):
 r=dispatch(n,a,session=S)
 LOG.append({'tool':n,'arguments':a,'result':r})
 (R/'reports/api-progress.json').write_text(json.dumps(LOG,ensure_ascii=False,indent=2,default=str))
 if r.get('status') in ['error','mcp.invalid_input']:raise RuntimeError(str((n,r))[:2000])
 return r
def nm(t):return re.sub(r'(?<!\\)\$([^$]+)\$',lambda m:r'\('+m[1]+r'\)',t)
def setup():
 if not B.exists():
  call('studium_project_create',dict(slug=B.name,course='Materiales y mantenimiento de motores aeroespaciales',university='Universidad de León',degree='Grado en Ingeniería Aeroespacial',language='es',profile='STEM',academic_year='2026/2027',course_code='0710341'))
  ch=[]
  for n in range(1,26):
   txt=(R/'content'/f'c{n:02d}.tex').read_text();title=re.search(r'\\chapter\{([^}]+)\}',txt)[1];ch.append({'id':f'c{n:02d}','title':title})
  call('studium_blueprint_store',{'sections':ch})
  parts=[]
  for pid,title,lo,hi in [('I','Materiales y comportamiento en servicio',1,11),('II','Mantenimiento y aeronavegabilidad',12,24),('III','Taller de integración',25,25)]:
   parts.append({'id':pid,'title':title,'chapters':[{'id':c['id'],'title':c['title'],'learning_objectives':['Comprender fundamentos, hipótesis, evidencia y límites del capítulo.'],'sections':[{'id':c['id']+'.core','title':'Fundamentos y aplicaciones','concepts':[{'id':c['id']+'.concept','title':c['title'],'depth':'UNDERGRADUATE','learning_objectives':['Explicar el modelo y justificar su aplicación.'],'exercises':1}]}]} for c in ch[lo-1:hi]]})
  call('studium_academic_blueprint_store',{'parts':parts,'subject':'Materiales y mantenimiento de motores aeroespaciales','profile_key':'UNDERGRADUATE'})
  call('studium_depth_plan',{'academic_depth':'UNDERGRADUATE','length':'COMPREHENSIVE','exercises_with_solutions':True})
  call('studium_course_document_get',{})
 ids={}
 for row in json.loads((R/'evidence/fuentes-publicas.json').read_text()):
  if row['key'] not in ['MIT-ELAS','MIT-SS','MIT-FRAC','MIT-FAT','MIT-CREEP','MIT-COMP','MIT-LAM','EU1321','EU748','EU1139','EU2026-100','RAD','CSE9','AD2024','FAA-G']:continue
  r=call('studium_public_source_record',{'title':row['title'],'url':row['url'],'kind':'institutional_reference','text':'Fuente consultada; alcance y localizadores en auditoría. Identidad bibliográfica no acredita por sí sola autoridad de cada afirmación.'})
  if 'candidate' not in r:raise RuntimeError(str(r))
  pid=r['candidate']['id']
  # Estos textos son materiales abiertos MIT, textos legislativos oficiales y documentación gubernamental pública.
  call('studium_public_source_open_supplement',{'id':pid,'open_supplement':True,'open_licensed':True})
  txt=(R/'work/texts'/f'{row["key"]}.txt').read_text()
  # Anclas literales de localización, no aprobación semántica de cada párrafo.
  chunks=[]
  for start in [len(txt)//5,len(txt)//2]:
   quote=' '.join(txt[start:].split()[:20]);rr=call('studium_excerpt_record',{'source_id':pid,'url':row['url'],'text':quote})
   if 'excerpt' not in rr:raise RuntimeError(str(rr))
   chunks.append(rr['excerpt']['id'])
  ids[row['key']]={'public':pid,'excerpts':chunks}
 (R/'evidence/studium-ids.json').write_text(json.dumps(ids,ensure_ascii=False,indent=2));print('Fuentes nativas registradas',len(ids),flush=True)
def math_checks():
 import sympy as sp
 import pint
 def quad(f,a,b,epsabs=1e-7,epsrel=1e-12):
  def simp(x,y,fx,fm,fy):return (y-x)*(fx+4*fm+fy)/6
  fa=f(a);fb=f(b);mid=(a+b)/2;fm=f(mid);whole=simp(a,b,fa,fm,fb)
  def rec(x,y,fx,fm,fy,old,tol,depth):
   m=(x+y)/2;lm=(x+m)/2;rm=(m+y)/2;fl=f(lm);fr=f(rm)
   left=simp(x,m,fx,fl,fm);right=simp(m,y,fm,fr,fy);delta=left+right-old
   if depth==0 or abs(delta)<=15*tol:return left+right+delta/15,abs(delta)/15
   v1,e1=rec(x,m,fx,fl,fm,left,tol/2,depth-1);v2,e2=rec(m,y,fm,fr,fy,right,tol/2,depth-1)
   return v1+v2,e1+e2
  return rec(a,b,fa,fm,fb,whole,min(epsabs,abs(whole)*epsrel),30)

 U=pint.UnitRegistry();rows=[]
 banks=json.loads((R/'evidence/problem-bank-editorial.json').read_text())
 exams=json.loads((R/'evidence/exam-bank-editorial.json').read_text())
 tasks=[(p['key'],p['ch'],t) for p in banks for t in p['tests']]
 tasks +=[(e['key']+f'.{i}',2,t) for e in exams for i,q in enumerate(e['questions'],1) for t in q['tests']]
 for key,ch,t in tasks:
  exact=sp.sympify(t['expression'],locals={'pi':sp.pi});got=float(exact.evalf(30));ok=math.isclose(got,t['expected'],rel_tol=1e-10,abs_tol=1e-12)
  row={'key':key,'expression':t['expression'],'expected':t['expected'],'sympy':got,'numeric_pass':ok,'unit':t['unit']}
  if not ok:raise AssertionError(row)
  row['studium']=call('studium_computation_check',{'section':f'c{ch:02d}','expression':t['expression'],'result':format(t['expected'],'.16g')})
  if t.get('symbolic') and t.get('symbol_units'):
   row['studium_dimensions']=call('studium_math_verify',{'kind':'dimensions','section':f'c{ch:02d}','expression':t['symbolic'],'symbol_units':t['symbol_units'],'expected_unit':t['unit']})
   val=eval(t['symbolic'],{'__builtins__':{}},{**{k:1*U(v) for k,v in t['symbol_units'].items()},'pi':math.pi,'sqrt':lambda x:x**.5})
   row['pint_dimensions_pass']=val.check(U(t['unit']).dimensionality)
   if not row['pint_dimensions_pass']:raise AssertionError(row)
  rows.append(row)
  (R/'reports/math-checks.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2,default=str))
 print('Sustituciones contrastadas',len(rows),flush=True)
 checks=[{'kind':'equivalence','left':'F*L/(A*E)','right':'(F/A)/E*L'}, {'kind':'equivalence','left':'(smax-smin)/2+(smax+smin)/2','right':'smax'}, {'kind':'derivative','function':'-2*a**(-1/2)','variable':'a','claimed':'a**(-3/2)','assumptions':{'a':['positive']}}, {'kind':'derivative','function':'log(a)','variable':'a','claimed':'1/a','assumptions':{'a':['positive']}}, {'kind':'equivalence','left':'2*E*(b*t**3/12+b*t*(h/2)**2)','right':'E*b*t*(h**2/2+t**2/6)'}, {'kind':'equivalence','left':'(Cbeta-C0)/(Cbeta-Calpha)+(C0-Calpha)/(Cbeta-Calpha)','right':'1'}, {'kind':'limit','expression':'exp(-lam*t)','variable':'t','point':'0','claimed':'1'}]
 rr=[call('studium_math_verify',v) for v in checks]
 qrows=[]
 for key,ai,af,C,ds,m in [('P16',.001,.006,2e-12,110,3),('P17',.0008,.005,5e-10,90,2),('P18',.0007,.004,1.5e-12,100,3),('S02.2',.0012,.005,1e-12,120,3)]:
  z,err=quad(lambda a:1/(C*(ds*math.sqrt(math.pi*a))**m),ai,af,epsabs=1e-6,epsrel=1e-12)
  closed=math.log(af/ai)/(C*(ds*math.sqrt(math.pi))**m) if m==2 else (af**(1-m/2)-ai**(1-m/2))/((1-m/2)*C*(ds*math.sqrt(math.pi))**m)
  qrows.append({'key':key,'quadrature':z,'closed':closed,'estimated_error':err,'pass':math.isclose(z,closed,rel_tol=1e-11)})
 a=sp.symbols('a',positive=True);m=sp.symbols('m',real=True)
 symbolic={'Paris_power_derivative':str(sp.simplify(sp.diff(a**(1-m/2)/(1-m/2),a)-a**(-m/2))),'Paris_log_derivative':str(sp.simplify(sp.diff(sp.log(a),a)-1/a))}
 (R/'reports/math-model-checks.json').write_text(json.dumps({'studium':rr,'quadrature':qrows,'sympy':symbolic},ensure_ascii=False,indent=2,default=str))
 print('Integrales y modelos contrastados',flush=True)
def content():
 ids=json.loads((R/'evidence/studium-ids.json').read_text());keys={1:'MIT-ELAS',2:'MIT-SS',3:'MIT-FRAC',4:'MIT-FAT',5:'MIT-CREEP',6:'FAA-G',7:'FAA-G',8:'FAA-G',9:'MIT-LAM',10:'CSE9',11:'FAA-G',12:'FAA-G',13:'EU1139',14:'EU1321',15:'EU748',16:'EU1321',17:'EU1321',18:'EU1321',19:'EU1321',20:'EU748',21:'AD2024',22:'CSE9',23:'RAD',24:'FAA-G',25:'EU1321'};records=[]
 for n in range(1,26):
  txt=(R/'content'/f'c{n:02d}.tex').read_text();txt=txt.replace(fr'\input{{content/e{n:02d}.tex}}',(R/'content'/f'e{n:02d}.tex').read_text())
  for j,para in enumerate(re.split(r'\n\s*\n',txt)):
   if not para.strip():continue
   # Almacena el desarrollo entero en LaTeX nativo; los fragmentos son anclas contextuales únicamente.
   result=call('studium_paragraph_record',{'section':f'c{n:02d}','text':nm(para.strip()),'excerpts':ids[keys[n]]['excerpts'],'role':'explanation'})
   records.append({'chapter':n,'paragraph':j,'source_sha256':hashlib.sha256(txt.encode()).hexdigest(),'result':result})
  (R/'evidence/content-imported.json').write_text(json.dumps(records,ensure_ascii=False,indent=2,default=str));print('Capítulo registrado',n,flush=True)
 banks=json.loads((R/'evidence/problem-bank-editorial.json').read_text());probs=[]
 for p in banks:
  first=p['tests'][0];ex=ids[keys[p['ch']]]['excerpts'];steps=[{'text':nm(x)} for x in p['steps']]+[{'text':'Reproducción de la sustitución; no valida la aplicabilidad física.','expression':t['expression'],'expected':format(t['expected'],'.16g'),'unit':t['unit']} for t in p['tests'][1:]+p['tests'][:1]]
  sol={'given':[],'unknown':p['unknown'],'assumptions':[p['hyp']],'model':[{'name':p['model'],'latex':p['eqs'][0],'symbolic':first.get('symbolic') or first['expression']}],'development':p['eqs'],'steps':steps,'result':'Y='+format(first['expected'],'.14g'),'interpretation':nm(p['check']),'limitations':[p['limits']],'mistakes':['Confundir magnitudes, omitir hipótesis o mezclar unidades.']}
  r=call('studium_problem_record',{'section':f"c{p['ch']:02d}",'prompt':p['key']+' '+nm(p['prompt']),'expected':format(first['expected'],'.16g'),'excerpts':ex,'role':'practice','difficulty':'INTERMEDIATE','problem_type':'MULTI_STEP','method':p['model'],'solution':sol})
  ck=call('studium_problem_check',{'id':r['problem']['id']}) if 'problem' in r else None
  probs.append({'key':p['key'],'record':r,'check':ck});(R/'evidence/problems-imported.json').write_text(json.dumps(probs,ensure_ascii=False,indent=2,default=str))
  print(p['key'],r.get('status'),ck.get('status') if ck else '',flush=True)
def extras():
 from native_extras import register_extras
 register_extras(call,R)
def reports():
 for name in ['studium_scientific_contract_report','studium_equation_report','studium_book_quality_audit','studium_quality_report','studium_book_review','studium_section_completeness','studium_book_next','studium_verify']:
  rr=call(name,{'mode':'full'} if name=='studium_verify' else {});(R/'reports'/f'{name}.json').write_text(json.dumps(rr,ensure_ascii=False,indent=2,default=str));print(name,rr.get('status'),flush=True)
if __name__=='__main__':
 try:
  for mode in sys.argv[1:] or ['setup','math_checks','content','reports']:globals()[mode]()
 finally:(R/'reports/api-session.json').write_text(json.dumps(LOG,ensure_ascii=False,indent=2,default=str))
