"""Completa contexto de ejercicios y registra controles sin alterar autoridad ni publicación."""
import sys,json,math
from pathlib import Path
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'scripts'))
from studium_project import call,nm,LOG
ids=json.loads((R/'evidence/studium-ids.json').read_text())
P=json.loads((R/'evidence/problem-bank-editorial.json').read_text())
# Dos fuentes de contexto distintas, no dos citas repetidas de la misma fuente.
def sources(ch):
 if ch==2:return ['MIT-ELAS','MIT-SS']
 if ch in [3,4]:return ['MIT-FRAC','MIT-FAT']
 if ch==5:return ['MIT-CREEP','FAA-G']
 if ch==9:return ['MIT-COMP','MIT-LAM']
 if ch in [6,10,11]:return ['FAA-G','MIT-ELAS']
 if ch==1:return ['MIT-ELAS','FAA-G']
 return ['EU1321','FAA-G']
old=json.loads((R/'evidence/problems-imported.json').read_text());new=[];mapping={}
for row in old:call('studium_problem_remove',{'id':row['record']['problem']['id']})
for p in P:
 first=p['tests'][0];ex=[ids[k]['excerpts'][0] for k in sources(p['ch'])]
 steps=[{'text':nm(x)} for x in p['steps']]+[{'text':'Sustitución de valores originales del ejercicio, no una afirmación de propiedades reales.','expression':t['expression'],'expected':format(t['expected'],'.16g'),'unit':t['unit']} for t in p['tests'][1:]+p['tests'][:1]]
 sol={'given':[],'unknown':p['unknown'],'assumptions':[p['hyp']],'model':[{'name':p['model'],'latex':p['eqs'][0],'symbolic':first.get('symbolic') or first['expression']}],'development':p['eqs'],'steps':steps,'result':'Y='+format(first['expected'],'.14g'),'interpretation':nm(p['check']),'limitations':[p['limits']],'mistakes':['Mezclar unidades, convenciones o dominios de modelo.']}
 r=call('studium_problem_record',{'section':f"c{p['ch']:02d}",'prompt':p['key']+' '+nm(p['prompt']),'expected':format(first['expected'],'.16g'),'excerpts':ex,'role':'practice','difficulty':'INTERMEDIATE','problem_type':'MULTI_STEP','method':p['model'],'solution':sol})
 ck=call('studium_problem_check',{'id':r['problem']['id']});new.append({'key':p['key'],'record':r,'check':ck});mapping[p['key']]=r['problem']['id']
(R/'evidence/problems-imported.json').write_text(json.dumps(new,ensure_ascii=False,indent=2,default=str))
examrows=[]
for e in json.loads((R/'evidence/exam-bank-editorial.json').read_text()):
 for i,q in enumerate(e['questions'],1):
  key=e['key']+f'.{i}';ch=17 if e['key']=='S03' else 25 if e['key']=='S04' else 24 if e['key']=='S05' and i==2 else 4 if e['key']=='S02' and i==2 else 2
  if not q['tests']:continue
  ex=[ids[k]['excerpts'][0] for k in sources(ch)];first=q['tests'][0]
  steps=[{'text':nm(q['solution'])}]+[{'text':'Control del cálculo ficticio del simulacro.','expression':t['expression'],'expected':format(t['expected'],'.16g'),'unit':t['unit']} for t in q['tests'][1:]+q['tests'][:1]]
  sol={'given':[],'unknown':'Magnitudes del enunciado.','assumptions':['Las hipótesis físicas y los datos ficticios aparecen en el enunciado.'],'model':[{'name':'Modelo explícito del simulacro','latex':'Y='+format(first['expected'],'.12g')}],'development':[],'steps':steps,'result':'Y='+format(first['expected'],'.12g'),'interpretation':'La solución conserva unidades y límites de alcance.','limitations':['No es evaluación oficial ni autorización.']}
  r=call('studium_problem_record',{'section':f'c{ch:02d}','prompt':key+' '+nm(q['prompt']),'expected':format(first['expected'],'.16g'),'excerpts':ex,'role':'practice','difficulty':'EXAM_LEVEL','problem_type':'MULTI_STEP','method':'Desarrollo razonado del simulacro original.','solution':sol})
  if 'problem' not in r:raise RuntimeError(str(r))
  ck=call('studium_problem_check',{'id':r['problem']['id']});examrows.append({'key':key,'record':r,'check':ck});mapping[key]=r['problem']['id']
(R/'evidence/exams-numeric-imported.json').write_text(json.dumps(examrows,ensure_ascii=False,indent=2,default=str))
checks=json.loads((R/'reports/math-checks.json').read_text())
for row in checks:
 row['studium_previous']=row['studium']
 row['studium']=call('studium_computation_check',{'section':row['studium'].get('computation',{}).get('section','c02'),'problem_id':mapping[row['key']],'expression':row['expression'],'result':format(row['expected'],'.16g')})
(R/'reports/math-checks.json').write_text(json.dumps(checks,ensure_ascii=False,indent=2,default=str))
r=call('studium_math_verify',{'kind':'limit','expression':'exp(-lam*t)','variable':'t','point':'0','claimed':'1','symbols':['lam','t'],'assumptions':{'lam':['positive'],'t':['real']}})
m=json.loads((R/'reports/math-model-checks.json').read_text());m['limit_retry']=r;(R/'reports/math-model-checks.json').write_text(json.dumps(m,ensure_ascii=False,indent=2,default=str))
# Comprobaciones de todos los ejemplos numéricos del manual y del taller.
manual=[('M01-A','2800/280e6',1e-5),('M01-B','4500/600e6',7.5e-6),('M01-ahorro','1-(4500/600e6)/(2800/280e6)',.25),('M02-VM','sqrt(120**2-120*40+40**2+3*30**2)',math.sqrt(13900)),('M02-ratio','240/sqrt(13900)',240/math.sqrt(13900)),('M03-K','180*sqrt(pi*.002)',180*math.sqrt(math.pi*.002)),('M03-ac','(32/180)**2/pi',(32/180)**2/math.pi),('M04-D','2000/100000+500/20000',.045),('M04-bloques','1/.045',1/.045),('M05-tasa','exp(-250000/8.314462618*(1/950-1/900))',5.802957862286402),('M05-deformacion','2e-8*100*3600',.0072),('M06-oxido','sqrt(4e-16*100*3600)',12e-6),('M09-EL','.6*230+.4*3',139.2),('M09-ET','1/(.6/230+.4/3)',1/(.6/230+.4/3)),('M12-A','800/804',800/804),('M12-espera','800/824',800/824),('M17','2400+500-2810',90),('M22','400/(12000/60)',2),('M24-a','4/20000',.0002),('M24-b','6/60000',.0001),('M25-T01','2400+500-2810',90),('M25-T02','1750+300-1980',70),('M25-T03','2400-1980',420),('M25-evento','2000+300',2300)]
import sympy as sp
rows=[]
for key,expr,expected in manual:
 got=float(sp.sympify(expr).evalf(30));ok=math.isclose(got,expected,rel_tol=1e-10,abs_tol=1e-12);assert ok,(key,got,expected)
 rows.append({'key':key,'expression':expr,'expected':expected,'sympy':got,'pass':ok,'scope':'Reproducción aritmética; modelo y datos ficticios del capítulo.'})
(R/'reports/manual-math-checks.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2))
from studium_project import reports
reports()
(R/'reports/api-finalize.json').write_text(json.dumps(LOG,ensure_ascii=False,indent=2,default=str))
print('Problemas:',len(new),'Simulacros numéricos:',len(examrows),'Controles:',len(checks),'Manual:',len(rows),flush=True)
print('Replays aceptados',sum(r['studium'].get('accepted') is True for r in checks),'de',len(checks),flush=True)
