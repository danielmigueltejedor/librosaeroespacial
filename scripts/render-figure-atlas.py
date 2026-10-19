from pathlib import Path
import re,hashlib,json,subprocess,concurrent.futures as cf
import pymupdf
from PIL import Image,ImageDraw
R=Path(__file__).resolve().parents[1];D=R/'dist/figure-audit';D.mkdir(parents=True,exist_ok=True)
records=[]
# Asset figures are vector or raster representations used by these imports; alternate formats are deduplicated.
for book in sorted((R/'books').iterdir()):
 if not book.is_dir():continue
 for p in sorted(book.rglob('*')):
  if p.suffix!='.pdf' or 'figures' not in str(p.relative_to(book)) or p.name=='cover-art.pdf':continue
  records.append(dict(book=book.name,kind='pdf-asset',source=str(p.relative_to(R)),id=f'{book.name}/{p.relative_to(book)}',sha256=hashlib.sha256(p.read_bytes()).hexdigest()))
 for p in sorted(book.glob('figures/FIG-*/*.png')):
  if p.with_suffix('.pdf').exists():continue
  records.append(dict(book=book.name,kind='raster-asset',source=str(p.relative_to(R)),id=f'{book.name}/{p.relative_to(book)}',sha256=hashlib.sha256(p.read_bytes()).hexdigest()))
 seen={}
 for p in sorted(book.rglob('*.tex')):
  if 'figures-originales' in p.parts:continue
  text=p.read_text()
  for m in re.finditer(r'\\begin\{tikzpicture\}.*?\\end\{tikzpicture\}',text,re.S):
   block=m[0];h=hashlib.sha256(re.sub(r'\s+',' ',block).encode()).hexdigest()
   loc=dict(file=str(p.relative_to(R)),line=text.count('\n',0,m.start())+1)
   if h in seen:seen[h]['occurrences'].append(loc);continue
   idx=len(seen)+1;key=f'{book.name}-tikz-{idx:03d}';target=D/(key+'.tex')
   after=text[m.end():m.end()+1800];before=text[max(0,m.start()-1000):m.start()]
   row=dict(book=book.name,kind='inline-tikz',id=key,sha256=h,source=loc['file'],line=loc['line'],occurrences=[loc],context_after=after,context_before=before,code=block,render=str(target.with_suffix('.pdf').relative_to(R)))
   seen[h]=row;records.append(row)
   header=r'''\documentclass{article}\usepackage[paperwidth=40cm,paperheight=40cm,margin=1cm]{geometry}\usepackage{tikz}\pagestyle{empty}
\usepackage[utf8]{inputenc}\usepackage[T1]{fontenc}\usepackage{lmodern,amsmath,amssymb,mathtools}
\usepackage[spanish,es-nodecimaldot]{babel}
\AtBeginDocument{\spanishdeactivate{"~<>}}
\usetikzlibrary{arrows.meta,calc,positioning,patterns,decorations.pathreplacing,angles,quotes}
\definecolor{studiumInk}{HTML}{142C40}\definecolor{studiumBlue}{RGB}{24,74,130}\definecolor{studiumCyan}{RGB}{0,184,205}
\definecolor{studiumLight}{RGB}{232,240,250}
\newcommand{\SIu}[1]{\,\mathrm{#1}}
\begin{document}
'''
   target.write_text(header+r'\setbox0=\hbox{'+block+r'}'+r'\pdfpagewidth=\dimexpr\wd0+16pt\relax\pdfpageheight=\dimexpr\ht0+\dp0+16pt\relax\hoffset=-1in\voffset=-1in\shipout\vbox{\kern8pt\hbox{\kern8pt\box0\kern8pt}\kern8pt}'+r'\end{document}')
jsonpath=D/'source-register.json';jsonpath.write_text(json.dumps(records,ensure_ascii=False,indent=2)+'\n')
print('Registered',len(records),'figures;',sum(r['kind']=='inline-tikz' for r in records),'TikZ',flush=True)
def compile_one(row):
 if row['kind']!='inline-tikz':return
 p=R/row['render'];
 stamp=p.with_suffix('.source-sha256')
 if p.exists() and stamp.exists() and stamp.read_text()=='tight-page-v2:'+row['sha256']:return
 res=subprocess.run(['pdflatex','-no-shell-escape','-halt-on-error','-interaction=batchmode','-output-directory='+str(D),str(p.with_suffix('.tex'))],cwd=R,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
 if res.returncode:return row['id']
 stamp.write_text('tight-page-v2:'+row['sha256'])
with cf.ThreadPoolExecutor(max_workers=4) as pool:
 fails=[v for v in pool.map(compile_one,records) if v]
print('Compile failures',fails,flush=True)
if fails:raise SystemExit('Standalone figure compilation failed')
# Six figures per sheet, with source identifiers; preserve aspect ratio.
for book in sorted(set(r['book'] for r in records)):
 rr=[r for r in records if r['book']==book]
 for start in range(0,len(rr),6):
  batch=rr[start:start+6];sheet=Image.new('RGB',(1800,1650),'#e3e8ee');draw=ImageDraw.Draw(sheet)
  for j,row in enumerate(batch):
   p=R/row.get('render',row['source']);x=j%2*900;y=j//2*550
   if p.suffix=='.pdf' and p.exists():
    doc=pymupdf.open(p);page=doc[0];clip=page.rect
    scale=min(868/clip.width,485/clip.height);pix=page.get_pixmap(matrix=pymupdf.Matrix(scale,scale),clip=clip,alpha=False);im=Image.frombytes('RGB',(pix.width,pix.height),pix.samples)
   elif p.suffix=='.png':im=Image.open(p).convert('RGB');im.thumbnail((868,485))
   else:draw.text((x+12,y+80),'RENDER ERROR',fill='red');continue
   sheet.paste(im,(x+(900-im.width)//2,y+55+(485-im.height)//2));draw.text((x+10,y+10),row['id'].replace(book+'/',''),fill='black');draw.text((x+10,y+28),row['source'][-105:]+(f":{row['line']}" if 'line' in row else ''),fill='black')
   row['atlas']=f'{book}-{start//6+1:02d}.jpg';row['atlas_slot']=j+1
  sheet.save(D/f'{book}-{start//6+1:02d}.jpg',quality=94)
jsonpath.write_text(json.dumps(records,ensure_ascii=False,indent=2)+'\n')
print('Atlas sheets ready',flush=True)
