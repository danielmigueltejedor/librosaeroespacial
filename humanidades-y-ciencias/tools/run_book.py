"""usage: run_book.py <spec_module> <chapter_prefix> <id_prefix> [section ...]
Chapter modules <prefix>N may define: build(spec) base paragraphs, extend(spec) more paragraphs,
figures(spec), exercises(spec), problems(spec) (numeric, legacy), SOURCES (extra sources)."""
import sys, importlib, json
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from engine import *
mod, prefix, idp = sys.argv[1:4]; only = sys.argv[4:]
spec = importlib.import_module(mod).spec
order = list(spec.get('chapter_ids', []))
mods = {}
for n in range(1, 40):
    try: m = importlib.import_module(f'{prefix}{n}')
    except ModuleNotFoundError: continue
    mods[n] = m
    spec['sources'].update(getattr(m, 'SOURCES', {}))
for n, m in mods.items():
    sid = f'{idp}-{n:02d}'
    base = m.build(spec) if hasattr(m, 'build') else []
    for i, title in getattr(m, 'HEADS', {}).items():
        if not base[i]['text'].startswith(title + '\n'): base[i]['text'] = title + '\n' + base[i]['text']
    ch = {'paragraphs': base}
    for name, key in (('extend', 'extend'), ('figures', 'figures'), ('exercises', 'exercises'), ('problems', 'problems')):
        if hasattr(m, name): ch[key] = getattr(m, name)(spec)
    if hasattr(m, 'ORDER'):
        ext = ch.get('extend', [])
        ch['final'] = [base[int(o[1:])] if o[0] == 'b' else ext[int(o[1:])] for o in m.ORDER]
        assert len(ch['final']) == len(base) + len(ext) and len(set(m.ORDER)) == len(m.ORDER), 'ORDER must use every paragraph once'
    spec['chapters'][sid] = ch
b = Builder(spec)
b.blueprint(); b.save()
b.sources()
for sid in spec['chapters']:
    if only and sid not in only: continue
    b.chapter(sid)
