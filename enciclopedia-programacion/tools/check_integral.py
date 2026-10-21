from pathlib import Path
from pypdf import PdfReader
import json
root=Path(__file__).resolve().parents[1];reports=json.load(open(root/'dist/review/build-summary.json'));final=PdfReader(root/'dist/review/ENCICLOPEDIA_COMPLETA_INTEGRAL.pdf');offset=0;checks=[]
for report in reports:
 slug=report['slug'];reader=PdfReader(root/'dist/review'/f'{slug}.pdf');checked=0;original_count=0;final_count=0
 for i,page in enumerate(reader.pages):
  original_count+=len(page.get('/Annots',[]));final_count+=len(final.pages[offset+i].get('/Annots',[]))
  for annotation in page.get('/Annots',[]):
   annotation=annotation.get_object();action=annotation.get('/A',{});destination=action.get('/D') if action.get('/S')=='/GoTo' else annotation.get('/Dest')
   if isinstance(destination,str) and destination in reader.named_destinations:
    expected=offset+reader.get_destination_page_number(reader.named_destinations[destination]);name=slug+':'+destination
    assert name in final.named_destinations,(slug,name)
    observed=final.get_destination_page_number(final.named_destinations[name]);assert expected==observed,(name,expected,observed)
    checked+=1
 assert original_count==final_count,(slug,original_count,final_count)
 checks.append({'volume':slug,'pdf_offset':offset,'pages':len(reader.pages),'named_internal_links_checked':checked,'original_annotations':original_count,'integral_annotations':final_count})
 offset+=len(reader.pages)
assert offset==len(final.pages)
(root/'reports/integral-navigation.json').write_text(json.dumps({'status':'CHECKS_PASSED','total_pages':offset,'volumes':checks,'scope':'All named internal annotation destinations compared to their source-volume page plus integral offset; annotation counts preserved. This is not academic verification.'},indent=2)+'\n')
print('Navigation checked:',sum(c['named_internal_links_checked'] for c in checks),'internal links,',offset,'pages')
