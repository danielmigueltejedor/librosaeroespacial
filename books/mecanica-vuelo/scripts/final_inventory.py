"""Inventario íntegro de ecuaciones, con evidencia nativa y fuentes editoriales."""
from pathlib import Path
import sys,json,re,hashlib
from collections import Counter
R=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(R/'framework/src'))
from studium.mcp.server import dispatch,open_workspace
session=open_workspace(str(R/'project'),str(R/'project/mecanica-vuelo-ule'))
rows=[];offset=0
while True:
    answer=dispatch('studium_equation_report',dict(offset=offset,limit=500),session=session)
    rows.extend(answer['equations'])
    offset=answer.get('next_offset')
    if offset is None:break
    print('ecuaciones',len(rows),flush=True)
(R/'evidence/equation-inventory-native.json').write_text(json.dumps(dict(total=len(rows),by_status=dict(Counter(r['status'] for r in rows)),equations=rows,note='Estados del lector nativo; ver MATH-001. No aprobación humana.'),ensure_ascii=False,indent=2))
editorial=[]
for path in sorted((R/'content').glob('*.tex')):
    text=path.read_text()
    for i,m in enumerate(re.finditer(r'\\\[(.*?)\\\]|\\begin\{(equation\*?|align\*?|gather\*?)\}(.*?)\\end\{\2\}',text,re.S),1):
        editorial.append(dict(file=str(path.relative_to(R)),line=text[:m.start()].count('\n')+1,index=i,latex=m.group(1) or m.group(3),expert_review='PENDING',note='Inventario de bloques; puede contener varias relaciones. No implica prueba automática.'))
(R/'evidence/equation-inventory-editorial.json').write_text(json.dumps(editorial,ensure_ascii=False,indent=2))
files=[*R.glob('*.tex'),*(R/'content').glob('*.tex'),*(R/'latex').glob('*.tex')]
(R/'evidence/editorial-source-sha256.json').write_text(json.dumps({str(p.relative_to(R)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(files)},indent=2))
print('Inventario final:',len(rows),'nativas;',len(editorial),'bloques editoriales',flush=True)
