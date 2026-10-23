"""usage: sg.py file kw1 [kw2 ...]  -> sentences of ws/src/file containing each keyword (case-insens), max 3 per kw"""
import sys, re
from pathlib import Path
t = re.sub(r'\s+', ' ', (Path.home()/'Developer/work/ws/src'/sys.argv[1]).read_text(encoding='utf-8'))
sents = re.split(r'(?<=[.!?])\s+(?=[A-ZÁÉÍÓÚÑ¿¡"«(\[])', t)
for kw in sys.argv[2:]:
    n = 0
    print(f'## {kw}')
    for s in sents:
        if kw.lower() in s.lower() and 25 < len(s) < 420:
            print('  -', s); n += 1
            if n >= 3: break
