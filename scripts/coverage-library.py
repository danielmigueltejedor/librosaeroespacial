#!/usr/bin/env python3
"""Locate teaching elements per chapter and map official themes without claiming mastery."""
from pathlib import Path
import importlib.util,json,re
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'reports/edition-v2'
spec=importlib.util.spec_from_file_location('inventory',ROOT/'scripts/inventory-library.py');iv=importlib.util.module_from_spec(spec);spec.loader.exec_module(iv)
MAP={
 'estructuras-aeroespaciales':[(1,8,'Temas 1–8, correspondencia de capítulos')],
 'mecanica-fluidos':[(1,2,'Tema 1: mecánica clásica'),(3,4,'Tema 2: fundamentos'),(5,9,'Tema 3: casos'),(10,10,'Tema 4: similitud'),(11,13,'Tema 5: formalismo'),(14,16,'Tema 6: Navier–Stokes'),(17,23,'Prácticas informáticas: desarrollo editorial')],
 'turbomaquinas':[(1,3,'Bloque I: principios'),(4,6,'Bloque II: turbinas axiales'),(7,10,'Bloque III: compresores axiales'),(11,14,'Bloque IV: estudio tridimensional'),(15,17,'Bloque V: radiales'),(18,19,'Aplicación y entrenamiento editorial')],
 'tecnologia-aeroespacial':[(1,2,'Tema 1: introducción e historia'),(3,5,'Tema 2: atmósfera'),(6,8,'Tema 3: fluidos'),(9,10,'Tema 4: aerodinámica'),(11,12,'Tema 5: actuaciones y estabilidad'),(13,14,'Temas 11–12: aeropuertos y navegación'),(15,15,'Tema 13: espacio'),(16,16,'Tema 6: estructuras'),(17,17,'Tema 7: materiales'),(18,18,'Tema 9: alternativos'),(19,20,'Tema 10: reacción y cohete'),(21,25,'Tema 8: sistemas')],
 'motores-cohete':[(1,4,'Bloque I: fundamentos'),(5,9,'Bloque II: toberas'),(10,13,'Bloque III: sólidos'),(14,20,'Bloque IV: líquidos'),(21,24,'Bloque V: eléctrica'),(25,28,'Bloque VI: vehículos')],
 'materiales-mantenimiento-motores':[(1,11,'Bloque I: materiales'),(12,14,'Bloque II tema 1: marco y técnicas'),(15,15,'Bloque II tema 2: certificación'),(16,17,'Bloque II tema 3: aeronavegabilidad'),(18,21,'Bloque II tema 4: organizaciones y documentación'),(22,25,'Integración y profundización editorial de mantenimiento')],
 'mecanica-vuelo':[(1,3,'Bloque I: introducción y ejes'),(4,6,'Bloque II: ecuaciones'),(7,9,'Bloque III: planeadores'),(10,14,'Bloque IV: aerorreactores'),(15,16,'Bloque de hélices'),(17,18,'Bloque de operaciones'),(19,20,'Estabilidad estática'),(21,21,'Ampliación editorial: estabilidad dinámica'),(22,23,'Prácticas informáticas: desarrollo editorial')],
}
rows=[]
for cfg in sorted((ROOT/'books').glob('*/studium-import.json')):
 d=json.loads(cfg.read_text());slug=cfg.parent.name;work=cfg.parent/d['workdir'];doc=d['documents'][0]
 segments=iv.reachable(work/doc['source'],work);current=None;appendix=False;chapters=[]
 for p,txt in segments:
  if p.name in ['preamble.tex','studium-editorial.tex','studium-cover.tex','editorial-config.tex','cover.tex']:continue
  pos=0
  for m in re.finditer(r'\\appendix\b|\\chapter\{',txt):
   if current is not None:current['text']+=txt[pos:m.start()]
   if m[0].startswith('\\appendix'):appendix=True;current=None;pos=m.end();continue
   title,end=iv.brace(txt,m.end());pos=end
   if not appendix:
    current=dict(book=slug,index=len(chapters)+1,title=title,source=str(p.relative_to(ROOT)),text='');chapters.append(current)
   else:current=None
  if current is not None:current['text']+=txt[pos:]
 companions='\n'.join(t for doc in d['documents'][1:] for p,t in iv.reachable(work/doc['source'],work))
 for c in chapters:
  txt=c.pop('text');c['official_or_editorial_group']=next((title for lo,hi,title in MAP[slug] if lo<=c['index']<=hi),'PENDING_MAPPING')
  c['theory_sections']=re.findall(r'\\(?:sub)?section\{([^}]+)\}',txt)
  c['worked_locations']=re.findall(r'\\(?:caso|begin\{studiumworked\})\{([^}]+)\}',txt)
  c['worked_locations']+=re.findall(r'\\(?:section|noindent\\textbf)\{([^}]*(?:[Pp]roblema resuelto|[Ee]jemplo|[Tt]aller resuelto)[^}]*)\}',txt)
  c['proposed_locations']=re.findall(r'\\(?:sub)?section\{([^}]*(?:[Ee]jercicios|[Aa]utoevaluación|[Pp]reguntas)[^}]*)\}',txt)
  c['proposed_locations']+=['Recuadro Ejercicios propuestos'] if 'Ejercicios propuestos' in txt else []
  c['problem_identifiers']=sorted(set(re.findall(r'\b(?:PRB-\d{4}|C\d{2}-\d{2}-[PRT]|T\d{2}|M\d{2})\b',txt)))
  c['shared_identifiers_in_companions']=[key for key in c['problem_identifiers'] if key in companions]
  c['outcome']='LOCATED_NOT_SEMANTICALLY_APPROVED'
  c['exam_skill_coverage']='PENDING_EXPERT_COMPARISON'
  c['limits']='Literal headings/IDs only; no equivalence of competence inferred from equal identifiers or similar words. Chapters descriptive or normative need no artificial numerical quota.'
  rows.append(c)
(OUT/'coverage-register.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2)+'\n')
print(len(rows),'chapter mappings; semantic exam-to-manual sufficiency remains pending')
