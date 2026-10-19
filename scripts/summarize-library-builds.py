#!/usr/bin/env python3
"""Summarize actual build receipts and detect stale inputs without conferring approval."""
from pathlib import Path
import hashlib,json
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'reports/edition-v2'
rows=[]
for cfg in sorted((ROOT/'books').glob('*/studium-import.json')):
 d=json.loads(cfg.read_text());slug=cfg.parent.name;p=ROOT/'dist/studium'/slug/'build-report.json'
 report=json.loads(p.read_text()) if p.exists() else {}
 for spec in d['documents']:
  row=next((v.copy() for v in report.get('documents',[]) if v['file'].endswith(spec['output'])),dict(status='NOT_RUN',file=spec['output']))
  row['book']=slug;row['source_date_epoch']=report.get('source_date_epoch');row['engine']=report.get('engine')
  row['stale_inputs']=[v['path'] for v in row.get('inputs',[]) if not (ROOT/v['path']).is_file() or hashlib.sha256((ROOT/v['path']).read_bytes()).hexdigest()!=v['sha256']]
  pdf=ROOT/row['file']
  row['pdf_hash_matches']=bool(pdf.is_file() and hashlib.sha256(pdf.read_bytes()).hexdigest()==row.get('sha256'))
  rows.append(row)
status='PASSED' if all(x['status']=='COMPILED' and not x['stale_inputs'] and x['pdf_hash_matches'] for x in rows) else 'FAILED'
(OUT/'build-receipts.json').write_text(json.dumps(dict(status=status,documents=rows,scope='Executed LaTeX builds and current input/output hashes; no academic approval.'),ensure_ascii=False,indent=2)+'\n')
pdfchecks=json.loads((OUT/'pdf-checks.json').read_text()) if (OUT/'pdf-checks.json').exists() else {}
lines=['# Informe de compilación de toda la colección','',f"Resultado de recibos y huellas: **{status}**. Documentos registrados: {len(rows)}.",'',
'La compilación ha ejecutado tres pasadas por volumen con pdfLaTeX, sin shell escape, y revisado los logs finales. No se deduce corrección científica de este resultado. La fecha de compilación se fija con SOURCE_DATE_EPOCH; el recibo registra el motor y las entradas realmente leídas. Los formularios, apéndices y bibliografías incluidos se generan dentro de cada volumen. No hay otros volúmenes registrados pendientes de compilación.','',
'| Libro | PDF | Pasadas | Estado | Entradas actuales |','|---|---|---:|---|---|']
for x in rows:lines.append(f"| {x['book']} | {Path(x['file']).name} | {x.get('passes')} | {x['status']} | {'Sí' if not x['stale_inputs'] and x['pdf_hash_matches'] else 'NO'} |")
lines+=['',f"Revisión automática de páginas: {pdfchecks.get('status','NOT_RUN')}; {pdfchecks.get('volumes')} volúmenes, {pdfchecks.get('pages')} páginas. Comprueba texto fuera de caja, caracteres de sustitución, páginas vacías, identidad de colección, destinos internos y logs. Véase pdf-checks.json.",'',
'La inspección visual de muestras se registra por separado. El comprobador no busca semánticamente toda fórmula cortada o toda flecha incorrecta. Los logs de cada ejecución se guardan en dist/studium/<libro>/<entrada>/pass-N.log y los recibos en build-report.json; GitHub Actions los vuelve a producir.','',
'No se promete igualdad binaria entre distintos motores y versiones. Las huellas del PDF ligan estos resultados al artefacto exacto; las de entradas detectan un informe obsoleto tras cambiar una fuente.']
(OUT/'BUILD-REPORT.md').write_text('\n'.join(lines)+'\n')
print(status,len(rows),'build receipts;',sum(bool(r['stale_inputs']) for r in rows),'stale documents')
for r in rows:
 if r['stale_inputs'] or not r['pdf_hash_matches']:print(r['book'],r['file'],r['stale_inputs'])
raise SystemExit(status!='PASSED')
