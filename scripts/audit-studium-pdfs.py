"""Audit every generated page; visual review remains a separate declared step."""
from pathlib import Path
import json,hashlib,re,unicodedata,argparse
from collections import Counter
import pymupdf
ROOT=Path(__file__).resolve().parents[1]
parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('--output',type=Path,default=ROOT/'reports/bundle-audit/pdf-checks.json')
args=parser.parse_args()
volumes=[]
for registry in sorted((ROOT/'books').glob('*/studium-import.json')):
    config=json.loads(registry.read_text());slug=registry.parent.name
    for item in config['documents']:
        pdf=ROOT/'dist/studium'/slug/item['output'];doc=pymupdf.open(pdf)
        problems=[];font=Counter();alltext=[]
        for n,page in enumerate(doc):
            text=page.get_text();alltext.append(text)
            if '\ufffd' in text:problems.append(f'page {n+1}: Unicode replacement character')
            if not text.strip():problems.append(f'page {n+1}: empty page')
            for w in page.get_text('words'):
                if w[0]<-1 or w[1]<-1 or w[2]>page.rect.width+1 or w[3]>page.rect.height+1:
                    problems.append(f'page {n+1}: text outside media box: {w[4]}')
            for b in page.get_text('dict')['blocks']:
                for line in b.get('lines',[]):
                    for span in line['spans']:
                        if len(span['text'])>25:font[round(span['size'],1)]+=len(span['text'])
            for link in page.get_links():
                if link['kind']==pymupdf.LINK_GOTO and not 0<=link['page']<len(doc):problems.append(f'page {n+1}: invalid internal destination')
        cover=unicodedata.normalize('NFKD',alltext[0]).encode('ascii','ignore').decode().lower()
        if 'studium' not in cover:problems.append('missing collection identity on cover')
        if 'en revision' in cover or 'borrador' in cover:problems.append('obsolete cover status')
        log=(pdf.parent/Path(item['source']).stem/Path(item['source']).with_suffix('.log')).read_text(errors='replace')
        if re.search(r'Overfull \\[hv]box|undefined references|undefined citations|multiply[- ]defined|Missing character:|Undefined control sequence',log):problems.append('final composition log failed')
        volumes.append(dict(slug=slug,volume=item['title'],file=str(pdf.relative_to(ROOT)),pages=len(doc),sha256=hashlib.sha256(pdf.read_bytes()).hexdigest(),bookmarks=len(doc.get_toc()),text_spans_by_size=font.most_common(5),issues=problems))
report=dict(status='PASSED' if all(not v['issues'] for v in volumes) else 'FAILED',volumes=len(volumes),pages=sum(v['pages'] for v in volumes),scope='Every page: text bounds, empty pages, replacement glyphs, internal destinations, cover status; final LaTeX warnings. Does not establish scientific correctness or replace visual inspection.',documents=volumes)
args.output.parent.mkdir(parents=True,exist_ok=True)
args.output.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(report['status'],report['volumes'],'volumes;',report['pages'],'pages')
for v in volumes:
    if v['issues']:print(v['file'],v['issues'][:10])
raise SystemExit(report['status']!='PASSED')
