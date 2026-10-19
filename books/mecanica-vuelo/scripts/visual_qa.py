from pathlib import Path
import json,re
import pymupdf as fitz
from PIL import Image,ImageOps,ImageDraw
R=Path(__file__).resolve().parents[1]
out=R/'work/qa';out.mkdir(parents=True,exist_ok=True)
report=[]
for name in ['main','problemas','simulacros']:
    doc=fitz.open(R/f'{name}.pdf');texts=[];outside=[]
    for i,p in enumerate(doc):
        text=p.get_text();texts.append(text)
        if i:
            for x0,y0,x1,y1,word,*_ in p.get_text('words'):
                if x0<28 or x1>p.rect.width-28 or y0<15 or y1>p.rect.height-12:
                    outside.append(dict(page=i+1,bbox=[x0,y0,x1,y1],word=word))
    alltext='\n'.join(texts);(out/f'{name}-text.txt').write_text(alltext)
    flags={p:len(re.findall(p,alltext)) for p in [r'\?\?',r'PAR-\d+',r'PRB-\d+',r'EVD-\d+',r'CLM-\d+',r'\{U\+[0-9A-F]+\}',r'(?i)undefined',r'\bTODO\b']}
    log=(R/f'{name}.log').read_text(errors='replace')
    logs={key:len(re.findall(p,log)) for key,p in dict(overfull=r'Overfull \\[hv]box',undefined_reference=r'Reference .+ undefined',undefined_control=r'Undefined control sequence',missing_character=r'Missing character',latex_error=r'! LaTeX Error').items()}
    report.append(dict(document=name,pages=len(doc),characters=len(alltext),text_flags=flags,log_flags=logs,outside_text=outside))
    for start in range(0,len(doc),20):
        contact=Image.new('RGB',(1100,2000),'#dce1e7');draw=ImageDraw.Draw(contact)
        for j,i in enumerate(range(start,min(start+20,len(doc)))):
            pix=doc[i].get_pixmap(matrix=fitz.Matrix(.42,.42),alpha=False)
            im=Image.frombytes('RGB',[pix.width,pix.height],pix.samples)
            im.thumbnail((260,370));x=(j%4)*275+(275-im.width)//2;y=(j//4)*400
            contact.paste(im,(x,y));draw.text((j%4*275+12,y+375),f'{name} {i+1}',fill='black')
        contact.save(out/f'{name}-contact-{start//20+1}.jpg',quality=85)
    selections={'main':[0,3,13,27,43,64,79,95,111,126,len(doc)-5], 'problemas':[0,5,12,23,35,42,len(doc)-1], 'simulacros':[0,5,12,18,25,len(doc)-1]}[name]
    for i in selections:
        if i<len(doc):doc[i].get_pixmap(matrix=fitz.Matrix(1.3,1.3),alpha=False).save(out/f'{name}-{i+1}.png')
(R/'reports/editorial-automated-checks.json').write_text(json.dumps(report,ensure_ascii=False,indent=2))
print([(r['document'],r['pages'],r['log_flags'],r['text_flags'],len(r['outside_text'])) for r in report])
