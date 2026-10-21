#!/usr/bin/env python3
"""Connect the duplicate answer keys to the complete chapter derivations."""
from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[1];BOOK=ROOT/'books/mecanica-fluidos'
p=BOOK/'latex/manual.tex';text=p.read_text();split=text.index(r'\chapter{Soluciones de los ejercicios}')
for row in json.loads((BOOK/'solutions/source-cases.json').read_text())[:16]:
 key=f'mf-{row["index"]:03}';token=r'\input{../solutions/generated/'+key+'.tex}';label=r'\phantomsection\label{solution:'+key+'}'
 if label not in text:text=text.replace(token,label+'\n'+token,1)
 a=text.find(row['Enunciado'].strip(),split)
 if a<0:raise ValueError(row['index'])
 b=text.index(r'\noindent\textbf{Respuesta}',a)
 link=(r'\noindent La resolución completa, con la deducción y las operaciones intermedias, está en el '
       +r'\hyperref[solution:'+key+r']{problema resuelto del capítulo correspondiente}, página~'
       +r'\pageref{solution:'+key+r'}.\par\medskip'+'\n')
 if link not in text[a:b]:text=text[:b]+link+text[b:]
p.write_text(text)
