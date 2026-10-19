#!/usr/bin/env python3
"""Inventory registered documents and reachable TeX; no invented counts or approval."""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
import re
import subprocess

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'reports/edition-v2'


def uncomment(text):
    return re.sub(r'(?<!\\)%[^\n]*','',text)


def brace(text,start):
    """Read a balanced TeX argument, including nested math braces."""
    depth=1;i=start
    while i<len(text):
        if text[i]=='{' and (i==0 or text[i-1]!='\\'):depth+=1
        if text[i]=='}' and (i==0 or text[i-1]!='\\'):
            depth-=1
            if depth==0:return text[start:i],i+1
        i+=1
    raise ValueError('Unclosed TeX argument')


def reachable(entry,work,seen=None):
    seen=set() if seen is None else seen
    entry=entry.resolve()
    if entry in seen:return []
    seen.add(entry)
    text=uncomment(entry.read_text())
    # Do not interpret macro bodies as executed scientific content.
    if entry.name in ['preamble.tex','studium-editorial.tex','studium-cover.tex','editorial-config.tex','cover.tex']:
        return [(entry,text)]
    pieces=[];pos=0
    for m in re.finditer(r'\\(?:input|include)\{([^}]+)\}',text):
        pieces.append((entry,text[pos:m.start()]))
        raw=m[1];target=(work/raw).with_suffix('.tex') if not Path(raw).suffix else work/raw
        if not target.exists():target=(entry.parent/raw).with_suffix('.tex') if not Path(raw).suffix else entry.parent/raw
        if '\\' not in raw and '#' not in raw and target.exists() and target.resolve().is_relative_to(ROOT):
            pieces+=reachable(target,work,seen)
        pos=m.end()
    pieces.append((entry,text[pos:]))
    return pieces


def inventory():
    documents=[];equations=[];chapters=[];sources=[]
    for cfg in sorted((ROOT/'books').glob('*/studium-import.json')):
        spec=json.loads(cfg.read_text());folder=cfg.parent;work=folder/spec['workdir'];slug=folder.name
        build_path=ROOT/'dist/studium'/slug/'build-report.json'
        build=json.loads(build_path.read_text()) if build_path.exists() else {}
        for doc in spec['documents']:
            entry=work/doc['source'];segments=reachable(entry,work)
            content=[(p,t) for p,t in segments if p.name not in ['preamble.tex','studium-editorial.tex','studium-cover.tex','editorial-config.tex','cover.tex']]
            alltext='\n'.join(t for p,t in content)
            kind='manual' if doc==spec['documents'][0] else ('problemas' if 'problema' in doc['source'] else 'simulacros')
            chapter='Front matter';appendix=False;chapter_rows=[];display_count=0
            for path,text in content:
                tokens=re.finditer(r'\\appendix\b|\\chapter(\*)?\{|\\begin\{(equation\*?|align\*?|gather\*?|multline\*?|displaymath)\}|\\\[',text)
                for token in tokens:
                    if token[0].startswith('\\appendix'):appendix=True;continue
                    if token[0].startswith('\\chapter'):
                        title,_=brace(text,token.end());chapter=title
                        if token[1] is None:
                            row=dict(book=slug,document=kind,source=str(path.relative_to(ROOT)),title=title,appendix=appendix,
                                     worked_examples=None,proposed_exercises=None,coverage_status='PENDING_SEMANTIC_REVIEW')
                            chapter_rows.append(row);chapters.append(row)
                        continue
                    if token[2]:
                        closing='\\end{'+token[2]+'}';end=text.find(closing,token.end())
                    else:
                        end=text.find('\\]',token.end())
                    if end<0:continue
                    eq=text[token.end():end];display_count+=1
                    equations.append(dict(id=f'{slug}:{kind}:{display_count:04d}',book=slug,document=kind,
                        chapter=chapter,source=str(path.relative_to(ROOT)),equation=eq.strip(),line=(path.read_text()[:path.read_text().find(eq)].count('\n')+1 if eq in path.read_text() else None),labels=re.findall(r'\\label\{([^}]+)\}',eq),
                        statuses=['PENDING_EXPERT_REVIEW'],scope='Located display; not automatically validated or semantically linked to a passing test.'))
                for m in re.finditer(r'\\bibitem(?:\[[^]]*\])?\{([^}]+)\}',text):
                    sources.append(dict(book=slug,document=kind,id=m[1],source=str(path.relative_to(ROOT)),status='PENDING_SOURCE_SUPPORT_REVIEW'))
            report=next((d for d in build.get('documents',[]) if d['file'].endswith(doc['output'])),{})
            pdf=ROOT/'dist/studium'/slug/doc['output'];pages=None
            if pdf.exists():
                import pymupdf
                with pymupdf.open(pdf) as opened:pages=len(opened)
            files=sorted(set(p for p,text in segments))
            documents.append(dict(subject=spec['title'],book=slug,document_type=kind,path=str(entry.relative_to(ROOT)),
                imported_on=spec.get('imported_on'),version=spec.get('origin_edition'),
                chapters=sum(not c['appendix'] for c in chapter_rows),appendices=sum(c['appendix'] for c in chapter_rows),pages=pages,
                display_math_blocks=display_count,
                figure_calls=len(re.findall(r'\\(?:includegraphics(?:\[[^]]*\])?|figura|ilustra|studiumcaption)\{',alltext)),
                problem_count=None,problem_count_note='No unified problem syntax; see original banks and coverage findings. No count inferred from section headings.',
                bibliography_entries=len(re.findall(r'\\bibitem(?:\[[^]]*\])?\{',alltext)),
                build_status=report.get('status',build.get('status','NOT_RUN')),
                verification_status='PARTIAL_MODEL_CHECKS; PENDING_EXPERT_REVIEW',
                dependencies=[dict(path=str(p.relative_to(ROOT)),sha256=hashlib.sha256(p.read_bytes()).hexdigest()) for p in files],
                engine='pdfLaTeX (see actual pass count in build receipt)',generator='scripts/build-studium-books.py; imported TeX retained',
                framework_at_import=spec.get('origin_framework'),pdf=str(pdf.relative_to(ROOT)) if pdf.exists() else None))
    OUT.mkdir(exist_ok=True)
    for name,data in [('inventory',documents),('equation-register',equations),('chapter-register',chapters),('bibliography-locations',sources)]:
        (OUT/(name+'.json')).write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
    rows=['# Inventario real de la colección','',
          'Los recuentos se obtienen de entradas registradas e inclusiones TeX. Los bloques matemáticos son entornos display, no ecuaciones científicas únicas. `null` significa desconocido. Los registros de ecuaciones y bibliografía localizan contenido, sin asignarle aprobación.','',
          '| Asignatura | Volumen | Capítulos | Apéndices | Páginas | Bloques matemáticos | Compilación |',
          '|---|---|---:|---:|---:|---:|---|']
    for d in documents:rows.append(f"| {d['subject']} | {d['document_type']} | {d['chapters']} | {d['appendices']} | {d['pages']} | {d['display_math_blocks']} | {d['build_status']} |")
    rows+=['','El registro JSON contiene rutas, dependencias y huellas, versión cuando existe, bibliografía y límites del recuento. Los formularios y apéndices incluidos se compilan como parte de sus volúmenes; no se han encontrado otras entradas documentales registradas. Las figuras PDF son recursos, no libros independientes.']
    (OUT/'INVENTORY.md').write_text('\n'.join(rows)+'\n')
    print(len(documents),'volumes;',sum(d['chapters'] for d in documents if d['document_type']=='manual'),'manual chapters;',len(equations),'located displays')

if __name__=='__main__':inventory()
