from pathlib import Path
import json,re,hashlib
from studium_project import call,nm,LOG
R=Path(__file__).resolve().parents[1];path=R/'evidence/content-imported.json';rows=json.loads(path.read_text());changes=[]
for n in [2,5,16]:
 txt=(R/'content'/f'c{n:02d}.tex').read_text().replace(fr'\input{{content/e{n:02d}.tex}}',(R/'content'/f'e{n:02d}.tex').read_text())
 parts=re.split(r'\n\s*\n',txt)
 for row in [x for x in rows if x['chapter']==n]:
  para=nm(parts[row['paragraph']].strip());old=row['result']['paragraph']
  if old['text']!=para:
   result=call('studium_paragraph_replace',{'id':old['id'],'text':para,'excerpts':old['excerpts']});row['result']=result;changes.append(old['id'])
  row['source_sha256']=hashlib.sha256(txt.encode()).hexdigest()
path.write_text(json.dumps(rows,ensure_ascii=False,indent=2,default=str));(R/'reports/api-final-content-sync.json').write_text(json.dumps(LOG,ensure_ascii=False,indent=2,default=str));print('Párrafos sincronizados',changes)
