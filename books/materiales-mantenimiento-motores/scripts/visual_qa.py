from pathlib import Path
import json
import pymupdf as fitz
from PIL import Image,ImageDraw
R=Path(__file__).resolve().parents[1];O=R/'work/qa';O.mkdir(exist_ok=True)
meta=[]
for stem in ['main','problemas','simulacros']:
 d=fitz.open(R/'build'/f'{stem}.pdf');thumbs=[]
 for n,page in enumerate(d):
  pm=page.get_pixmap(matrix=fitz.Matrix(.6,.6),alpha=False);im=Image.frombytes('RGB',[pm.width,pm.height],pm.samples);im.save(O/f'{stem}-{n+1:03d}.png')
  canvas=Image.new('RGB',(220,330),'#dddddd');im.thumbnail((212,305));canvas.paste(im,((220-im.width)//2,3));ImageDraw.Draw(canvas).text((8,313),f'{stem} | PDF {n+1}',fill='black');thumbs.append(canvas)
 for start in range(0,len(thumbs),24):
  group=thumbs[start:start+24];sheet=Image.new('RGB',(6*220,((len(group)+5)//6)*330),'#bbbbbb')
  for j,im in enumerate(group):sheet.paste(im,((j%6)*220,(j//6)*330))
  sheet.save(O/f'{stem}-contact-{start//24+1}.png')
 meta.append({'document':stem,'pages':len(d),'raster_image_instances':sum(len(p.get_images()) for p in d),'text_characters':sum(len(p.get_text()) for p in d)})
 print(stem,len(d),'páginas',flush=True)
# Todas las figuras originales en un panel.
files=sorted((R/'figures').glob('*.png'));tiles=[]
for p in files:
 im=Image.open(p).convert('RGB');im.thumbnail((420,220));c=Image.new('RGB',(440,260),'white');c.paste(im,((440-im.width)//2,0));ImageDraw.Draw(c).text((10,235),p.stem,fill='black');tiles.append(c)
sheet=Image.new('RGB',(440*3,260*((len(tiles)+2)//3)),'#bbbbbb')
for j,im in enumerate(tiles):sheet.paste(im,((j%3)*440,(j//3)*260))
sheet.save(O/'figuras-contacto.png')
(R/'reports/pdf-structure.json').write_text(json.dumps(meta,ensure_ascii=False,indent=2))
