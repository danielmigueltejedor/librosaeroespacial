from pathlib import Path
import json,sys,importlib.util,ast,math
import pint
BOOK=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('procedures',BOOK/'solutions/procedures.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
U=pint.UnitRegistry();Q=U.Quantity
rows=json.loads((BOOK/'solutions/source-cases.json').read_text());fail=[];passed=[]
for row in rows:
 n=row['index'];route=m.ROUTES[n]
 try:env={k:Q(v['value'],v['unit']) for k,v in row['given'].items()}
 except Exception as e:fail.append([n,'given',str(e)]);continue
 env.update({k:Q(v,u) for k,(v,u) in route['extra'].items()})
 def scalar(q):return q.to('').magnitude if hasattr(q,'to') else q
 functions={k:(lambda x,fn=getattr(math,k):fn(scalar(x))) for k in ['sin','cos','tan','asin','acos','atan','exp']}
 functions.update(sqrt=lambda x:x**.5,log=lambda x,b=math.e:math.log(scalar(x),scalar(b)),pi=math.pi)
 for step in route['steps']:
  try:
   value=eval(step['expression'],{'__builtins__':{}},env|functions)
   if not hasattr(value,'dimensionality'):value=Q(value,'')
   expected=U.parse_units(step['unit'] or '')
   # Conversion factors are printed explicitly (rpm, hours, degrees). This
   # check assesses dimensions, not an additional application of conversions.
   if value.dimensionality!=expected.dimensionality:raise ValueError(f'{value.dimensionality} != {expected.dimensionality}')
   env[step['target']]=Q(float(value.magnitude),step['unit'] or '')
   passed.append([n,step['target']])
  except Exception as e:
   fail.append([n,step['target'],str(e)]);break
report=dict(scope='Dimensional consistency of the authored scalar steps; explicit numerical conversion factors retained; not model validation or independent approval',passed=len(passed),failed=len(fail),failures=fail)
(BOOK/'reports/solution-dimensions.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(report,ensure_ascii=False))
if fail:raise SystemExit(1)
