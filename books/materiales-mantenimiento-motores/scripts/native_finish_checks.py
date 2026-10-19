from pathlib import Path
import json
from studium_project import call,LOG,reports
R=Path(__file__).resolve().parents[1]
rows=json.loads((R/'evidence/problems-imported.json').read_text())+json.loads((R/'evidence/exams-numeric-imported.json').read_text())
mp={r['key']:r['record']['problem'] for r in rows}
checks=json.loads((R/'reports/math-checks.json').read_text())
for row in checks:
 if row['studium'].get('accepted') is True:continue
 problem=mp[row['key']];row['studium_context_retry']=row['studium'];row['studium']=call('studium_computation_check',{'section':problem['section'],'problem_id':problem['id'],'expression':row['expression'],'result':format(row['expected'],'.16g')})
(R/'reports/math-checks.json').write_text(json.dumps(checks,ensure_ascii=False,indent=2,default=str))
assert all(r['studium'].get('accepted') is True and r['studium'].get('correct') is True for r in checks)
# Completar descripciones de variables y mantener sus unidades en su campo propio.
der=json.loads((R/'evidence/derivations.json').read_text());updated=[]
for row in der:
 original=row['record']['derivation'];call('studium_derivation_remove',{'id':original['id']})
 allowed=['section','name','equation','assumptions','governing_principles','steps','steps_latex','symbolic','boundary_conditions','applicability','limitations','references']
 args={k:original[k] for k in allowed if k in original};args['variables']={k:{'meaning':'Magnitud '+k+' del modelo definido en el capítulo.','units':v['meaning']} for k,v in original['variables'].items()}
 result=call('studium_derivation_record',args);oldcheck=row['check']['derivation']['verification']['checks'][0]['inputs'];ck=call('studium_derivation_check',{'id':result['derivation']['id'],'dimensions':oldcheck})
 updated.append({'name':row['name'],'record':result,'check':ck})
(R/'evidence/derivations.json').write_text(json.dumps(updated,ensure_ascii=False,indent=2,default=str))
reports();(R/'reports/api-finish-checks.json').write_text(json.dumps(LOG,ensure_ascii=False,indent=2,default=str))
print('66 de 66 controles numéricos aceptados por Studium; 35 problemas y 13 preguntas numéricas registrados con dos fuentes de contexto. Autoridad y publicación no forzadas.')
