"""usage: run_book.py <spec_module> <chapter_prefix> <id_prefix> [section ...]"""
import sys, importlib
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from engine import *
mod, prefix, idp = sys.argv[1:4]; only = sys.argv[4:]
spec = importlib.import_module(mod).spec
for n in range(1, 20):
    try: m = importlib.import_module(f'{prefix}{n}')
    except ModuleNotFoundError: continue
    sid = f'{idp}-{n:02d}'
    spec['chapters'][sid] = {'paragraphs': m.build(spec), **({'problems': m.problems(spec)} if hasattr(m, 'problems') else {})}
b = Builder(spec)
if not b.state.get('blueprint_done'):
    b.blueprint(); b.state['blueprint_done'] = True; b.save()
b.sources()
for sid in spec['chapters']:
    if only and sid not in only: continue
    b.chapter(sid)
