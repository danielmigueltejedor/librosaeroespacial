"""Finite, source-generated streamlines; no huge off-page TikZ plot paths."""
from pathlib import Path
import hashlib,json,re
import numpy as np
from scipy.optimize import brentq
R=Path(__file__).resolve().parents[1]
x=np.linspace(-4.5,4.5,101);curves=[]
lines=[r'\begin{tikzpicture}',r'% studium:potential-cylinder-v2',r'\fill[gray!35] (0,0) circle (1);',r'\draw[thick] (0,0) circle (1);',r'\draw[blue,thick,->] (-4.5,0) -- (-1,0);',r'\draw[blue,thick,->] (1,0) -- (4.5,0);']
for psi in [.2,.5,1.,1.6,2.4]:
 y=np.array([brentq(lambda yy:yy*(1-1/(xx*xx+yy*yy))-psi,max(1e-10,np.sqrt(max(0,1-xx*xx))),psi+2,xtol=1e-13) for xx in x]);res=y*(1-1/(x*x+y*y))-psi
 assert np.max(abs(res))<1e-10 and np.min(x*x+y*y)>1
 curves.append(dict(psi=psi,max_streamfunction_residual=float(np.max(abs(res))),minimum_radius=float(np.min(np.hypot(x,y)))))
 for sign in [1,-1]:lines.append(r'\draw[blue,smooth] plot coordinates {'+' '.join(f'({xx:.5f},{sign*yy:.5f})' for xx,yy in zip(x,y))+'};')
lines += [r'\draw[->,thick] (-4.4,3.05) -- (-3.2,3.05) node[right]{$U$};',r'\end{tikzpicture}'];block='\n'.join(lines)
p=R/'latex/manual.tex';s=p.read_text()
def replace(m):
 b=m[0];return block if '% studium:potential-cylinder-v2' in b or r'\clip (-4.7,-2.9)' in b else b
new=re.sub(r'\\begin\{tikzpicture\}.*?\\end\{tikzpicture\}',replace,s,flags=re.S);p.write_text(new)
(R/'evidence/cylinder-streamlines.json').write_text(json.dumps(dict(classification='derived',model='Uniform incompressible irrotational flow past cylinder: psi/U=y(1-a²/r²), a=1. Streamlines on both sides; uniform stream along positive x; no penetration.',curves=curves,inline_source_sha256=hashlib.sha256(block.encode()).hexdigest()),indent=2)+'\n')
