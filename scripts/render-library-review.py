from pathlib import Path
import json,unicodedata,re,hashlib
import pymupdf
from PIL import Image,ImageDraw
r=Path(__file__).resolve().parents[1];dest=r/'dist/visual-review';dest.mkdir(parents=True,exist_ok=True);records=[]
def norm(x):return ''.join(c for c in unicodedata.normalize('NFD',x).lower() if not unicodedata.combining(c))
for cfg in sorted((r/'books').glob('*/studium-import.json')):
 data=json.loads(cfg.read_text())
 for spec in data['documents']:
  pdf=r/'dist/studium'/cfg.parent.name/spec['output'];d=pymupdf.open(pdf);texts=[norm(p.get_text()) for p in d];toc=d.get_toc()
  selected={'cover':0,'contents':next((i for i,t in enumerate(texts) if i and ('indice' in t[:160] or 'indice general' in t[:200])),min(3,len(d)-1)),
   'chapter':next((i for i,t in enumerate(texts) if i>4 and re.search(r'(?:^|\n)capitulo\s+1(?:\n|[ .])',t[:250])),min(14,len(d)-1)),
   'equations':max(range(1,max(2,int(len(d)*.8))),key=lambda i:sum(texts[i].count(x) for x in ['=','∂','∫','ρ','σ'])),
   'figure_or_frontmatter':next((i for i,t in enumerate(texts) if i>6 and re.search(r'figura\s+\d+(?:\.\d+)?[.:]',t)),1),
   'worked':next((i for i,t in enumerate(texts) if i>5 and ('hipotesis' in t and ('resultado' in t or 'sustitucion' in t))),min(14,len(d)-1)),
   'appendix_or_solutions':next((row[2]-1 for row in toc if any(x in norm(row[1]) for x in ['apendice','formulario','notacion y unidades','soluciones de'])),max(1,len(d)-5)),
   'bibliography_or_last':next((i for i,t in enumerate(texts) if i>len(d)//2 and re.search(r'(?:^|\n)(?:bibliografia(?:\s+y[^\n]*)?|fuentes realmente consultadas)\n',t[:350])),len(d)-1),'last_page':len(d)-1}
  w,h=598,868;sheet=Image.new('RGB',(w*2,h*5),'#dce2e8');draw=ImageDraw.Draw(sheet)
  for j,(kind,i) in enumerate(selected.items()):
   pix=d[i].get_pixmap(matrix=pymupdf.Matrix(1,1),alpha=False);im=Image.frombytes('RGB',[pix.width,pix.height],pix.samples)
   sheet.paste(im,(j%2*w,j//2*h+22));draw.text((j%2*w+8,j//2*h+4),f'{kind} | page {i+1}/{len(d)}',fill='black')
  target=dest/(pdf.stem+'.jpg');sheet.save(target,quality=92)
  records.append(dict(document=spec['output'],pdf=str(pdf.relative_to(r)),pages=len(d),sample={k:v+1 for k,v in selected.items()},sheet=str(target.relative_to(r)),pdf_sha256=hashlib.sha256(pdf.read_bytes()).hexdigest(),review_status='RENDERED_NOT_YET_REVIEWED'))
  print(target.name,flush=True)
(r/'reports/edition-v2/visual-samples.json').write_text(json.dumps(records,ensure_ascii=False,indent=2)+'\n')
