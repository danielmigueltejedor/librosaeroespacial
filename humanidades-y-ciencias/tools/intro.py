"""usage: intro.py file [n=8] [skip=0]  -> numbered sentences of ws/src/file (sentences 25..420 chars)"""
import sys, re
from pathlib import Path
t = re.sub(r'\s+', ' ', (Path.home()/'Developer/work/ws/src'/sys.argv[1]).read_text(encoding='utf-8'))
t = re.sub(r'==+ ([^=]+?) ==+', r'. [§ \1]. ', t)
sents = [s for s in re.split(r'(?<=[.!?])\s+(?=[A-ZÁÉÍÓÚÑ¿¡"«(\[])', t) if 25 < len(s) < 420]
n = int(sys.argv[2]) if len(sys.argv) > 2 else 8
k = int(sys.argv[3]) if len(sys.argv) > 3 else 0
for i, s in enumerate(sents[k:k+n], k): print(f'{i}: {s}')
