"""Reobtiene las fuentes públicas del registro, sin atribuirles vigencia ni autoridad automática."""
from pathlib import Path
import json,urllib.request,hashlib
R=Path(__file__).resolve().parents[1]
for row in json.loads((R/'evidence/fuentes-publicas.json').read_text()):
 if row.get('usable_content') is False:continue
 target=R/row['path'];target.parent.mkdir(parents=True,exist_ok=True)
 if target.exists():print('Conservado',row['key']);continue
 try:
  with urllib.request.urlopen(row['url'],timeout=60) as response:data=response.read()
  target.write_bytes(data);print(row['key'],'coincide con huella original:',hashlib.sha256(data).hexdigest()==row['sha256'])
 except Exception as exc:print(row['key'],'no recuperada:',exc)
