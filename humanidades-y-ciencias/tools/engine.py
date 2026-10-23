"""Spec-driven book builder over Studium's MCP dispatcher."""
import json, hashlib, re, sys, importlib
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from stu import call, WS
SRC = WS/'src'

def norm(s): return re.sub(r'\s+', ' ', s).strip()

class Builder:
    def __init__(self, spec):
        self.spec = spec; self.book = spec['book']
        self.sf = WS/f'{self.book}.state.json'
        self.state = json.loads(self.sf.read_text()) if self.sf.exists() else {'sources':{}, 'excerpts':{}, 'paragraphs':{}, 'audits':{}, 'problems':{}}
        self.texts = {}
    def save(self): self.sf.write_text(json.dumps(self.state, ensure_ascii=False, indent=1))
    def text(self, key):
        if key not in self.texts:
            self.texts[key] = norm((SRC/self.spec['sources'][key]['file']).read_text(encoding='utf-8'))
        return self.texts[key]
    def sources(self):
        have = {s['url']: s['id'] for s in call(self.book, 'studium_public_source_list').get('records', [])}
        for key, s in self.spec['sources'].items():
            if s['url'] in have: self.state['sources'][key] = have[s['url']]; continue
            r = call(self.book, 'studium_public_source_record', title=s['title'], url=s['url'], authors=s.get('authors','Colaboradores de Wikipedia'), year=s.get('year', 2026), kind=s.get('kind','encyclopedia'))
            if r.get('status') != 'recorded': print('SRC FAIL', key, r); continue
            self.state['sources'][key] = r['candidate']['id']
        self.save()
    def excerpt(self, key, quote):
        q = norm(quote)
        if q not in self.text(key): raise ValueError(f'quote not verbatim in {key}: {q[:90]}')
        h = hashlib.sha1((key+'|'+q).encode()).hexdigest()[:12]
        if h in self.state['excerpts']: return self.state['excerpts'][h]
        r = call(self.book, 'studium_excerpt_record', source_id=self.state['sources'][key], url=self.spec['sources'][key]['url'], text=q)
        if r.get('status') != 'recorded': raise RuntimeError(f'excerpt fail {r}')
        self.state['excerpts'][h] = r['excerpt']['id']; self.state.setdefault('exsrc', {})[r['excerpt']['id']] = self.state['sources'][key]; self.save(); return r['excerpt']['id']
    def blueprint(self):
        r = call(self.book, 'studium_blueprint_store', sections=[{'id': i, 'title': t} for i, t in self.spec['blueprint']])
        print('blueprint', r.get('status'), r.get('message',''))
    def paragraph(self, section, idx, p):
        pid_key = f'{section}:{idx}'
        ex = [self.excerpt(k, q) for k, q in p['quotes']]
        args = dict(section=section, text=p['text'], excerpts=ex, role=p.get('role', 'explanation'))
        old = self.state['paragraphs'].get(pid_key)
        if old and old['text'] == p['text'] and old['ex'] == ex and old.get('role') == args['role']: return old['id']
        if old:
            r = call(self.book, 'studium_paragraph_replace', id=old['id'], text=p['text'], excerpts=ex, role=args['role'])
            ok = r.get('status') in ('replaced', 'recorded', 'ok')
            pid = old['id']
        else:
            r = call(self.book, 'studium_paragraph_record', **args)
            ok = r.get('status') == 'recorded'
            pid = (r.get('paragraph') or {}).get('id')
        if not ok or not pid: raise RuntimeError(f'paragraph fail {pid_key}: {json.dumps(r, ensure_ascii=False)[:600]}')
        self.state['paragraphs'][pid_key] = {'id': pid, 'text': p['text'], 'ex': ex, 'role': args['role']}; self.save()
        return pid
    def excerpt_source(self, eid):
        return self.state.get('exsrc', {}).get(eid, eid)
    def audit(self, pid, kind, ex, text=''):
        k = f'{pid}'
        sig = [ex, hashlib.sha1(text.encode()).hexdigest()[:10]]
        if self.state['audits'].get(k) == sig: return
        pick, seen = [], set()
        for e in ex:
            sid = self.excerpt_source(e)
            if sid not in seen: seen.add(sid); pick.append(e)
        r = call(self.book, 'studium_audit_record', target=pid, kind=kind, excerpts=pick[:2])
        if r.get('status') not in ('recorded', 'ok', 'audited'): raise RuntimeError(f'audit fail {pid}: {json.dumps(r, ensure_ascii=False)[:500]}')
        self.state['audits'][k] = sig; self.save()
    def chapter(self, section):
        ch = self.spec['chapters'][section]
        for i, p in enumerate(ch['paragraphs']):
            pid = self.paragraph(section, i, p)
            if p.get('audit', True):
                ex = self.state['paragraphs'][f'{section}:{i}']['ex']
                if len({k for k, _ in p['quotes']}) >= 2: self.audit(pid, self.spec.get('audit_kind', 'historical'), ex, p['text'])
                else: print('  WARN needs 2 sources for audit:', section, i)
        print('chapter', section, 'paragraphs', len(ch['paragraphs']))

_T = {}
def span(spec, key, a, b=None):
    """Verbatim slice of source `key` from phrase `a` to the end of phrase `b` (or of `a`)."""
    if key not in _T: _T[key] = norm((SRC/spec['sources'][key]['file']).read_text(encoding='utf-8'))
    a = norm(a); b = norm(b) if b else b
    t = _T[key]; i = t.find(a)
    if i < 0: raise ValueError(f'anchor not found in {key}: {a[:60]}')
    j = i + len(a)
    if b:
        k = t.find(b, i)
        if k < 0: raise ValueError(f'end anchor not found in {key}: {b[:60]}')
        j = k + len(b)
    return (key, t[i:j])

def _problem(self, section, pr, idx=0):
    key = f'{section}:{idx}'
    h = hashlib.sha1(json.dumps(pr, ensure_ascii=False, sort_keys=True).encode()).hexdigest()
    old = self.state['problems'].get(key)
    if old and old['hash'] == h: return old['id']
    if old: call(self.book, 'studium_problem_remove', id=old['id'])
    args = {k: v for k, v in pr.items() if k != 'quotes'}
    if 'quotes' in pr: args['excerpts'] = [self.excerpt(k, q) for k, q in pr['quotes']]
    r = call(self.book, 'studium_problem_record', section=section, **args)
    if r.get('status') not in ('recorded',) or 'problem' not in r: raise RuntimeError(f'problem fail {key}: {json.dumps(r, ensure_ascii=False)[:800]}')
    self.state['problems'][key] = {'id': r['problem']['id'], 'hash': h}; self.save()
    return r['problem']['id']
Builder.problem = _problem

# ---------------------------------------------------------------- v2
import commons

def S(lang, title, file, label=None, host=None):
    import urllib.parse
    host = host or f'{lang}.wikipedia.org'
    path = urllib.parse.quote(title.replace(' ', '_'), safe="_()',-")
    name = 'Wikisource' if 'wikisource' in host else 'Wikipedia'
    return dict(title=f'{label or title} — {name} ({lang})', url=f'https://{host}/wiki/' + path, file=file)

def _ids(self, quotes):
    return [self.excerpt(k, q) for k, q in quotes]
Builder.ids = _ids

def _translate(self, obj):
    """Replace every 'quotes': [(source key, verbatim text)] of an exercise by stored excerpt ids."""
    if isinstance(obj, dict):
        out = {}
        for k, v in obj.items():
            if k == 'quotes': out['excerpts'] = self.ids(v)
            else: out[k] = self.translate(v)
        return out
    if isinstance(obj, list): return [self.translate(x) for x in obj]
    return obj
Builder.translate = _translate

def _exercise_args(self, ex):
    args = {k: v for k, v in ex.items() if k != 'source'}
    src = ex.get('source')
    if src:
        s = dict(src); key = s.pop('key'); lines = s.pop('lines', None); quote = s.pop('quote', None)
        text = '\n'.join(lines) if lines else quote
        args['source'] = dict(excerpt=self.excerpt(key, text), quote=text, **s)
    if 'quotes' in args:  # numeric problem: quotes is the pair of witnesses
        args['excerpts'] = self.ids(args.pop('quotes'))
    for k in ('answer', 'solution'):
        if k in args: args[k] = self.translate(args[k])
    return args
Builder.exercise_args = _exercise_args

def _put_exercise(self, section, key, ex):
    h = hashlib.sha1(json.dumps(ex, ensure_ascii=False, sort_keys=True, default=str).encode()).hexdigest()
    old = self.state['problems'].get(key)
    if old and old['hash'] == h: return old['id']
    if old: call(self.book, 'studium_problem_remove', id=old['id'])
    r = call(self.book, 'studium_problem_record', section=section, **self.exercise_args(ex))
    if r.get('status') != 'recorded' or 'problem' not in r:
        raise RuntimeError(f'exercise fail {key}: {json.dumps(r, ensure_ascii=False)[:900]}')
    if ex.get('problem_type') and r['problem'].get('status') != 'two_witnesses':
        print('  WARN exercise not witnessed (needs two different sources):', key)
    self.state['problems'][key] = {'id': r['problem']['id'], 'hash': h}; self.save()
    return r['problem']['id']
Builder.put_exercise = _put_exercise

def _put_figure(self, section, fig):
    key = f"{section}:fig:{fig['key']}"
    pre = r'\tikzset{every node/.append style={align=center}}' + '\n' if (fig['kind'] == 'tikz' and '\\\\' in fig['source'] and 'every node' not in fig['source']) else ''
    h = hashlib.sha1((json.dumps(fig, ensure_ascii=False, sort_keys=True, default=str) + pre + ('|img640' if fig['kind'] == 'image' else '')).encode()).hexdigest()
    st = self.state.setdefault('figures', {})
    old = st.get(key)
    if old and old['hash'] == h: return old['id']
    if old: call(self.book, 'studium_figure_remove', id=old['id'])
    args = dict(section=section, caption=fig['caption'], key=fig['key'], kind=fig['kind'], excerpts=self.ids(fig['quotes']))
    if fig['kind'] == 'image':
        args['image'] = commons.download(fig['commons'], self.book, fig['key'], width=fig.get('width', 900))
    else:
        args['source'] = pre + fig['source']
    r = call(self.book, 'studium_figure_record', **args)
    if r.get('status') != 'recorded': raise RuntimeError(f'figure fail {key}: {json.dumps(r, ensure_ascii=False)[:900]}')
    fid = r['figure']['id']
    c = call(self.book, 'studium_figure_check', id=fid)
    if c.get('status') != 'checked': raise RuntimeError(f'figure not checked {key}: {json.dumps(c, ensure_ascii=False)[:900]}')
    st[key] = {'id': fid, 'hash': h}; self.save()
    return fid
Builder.put_figure = _put_figure

def _migrate_slots(self, section):
    """Renumber stored paragraph keys of a section to consecutive creation-order slots 0..n-1."""
    keys = [k for k in self.state['paragraphs'] if k.startswith(section + ':')]
    nums = sorted(int(k.split(':')[1]) for k in keys)
    if nums == list(range(len(nums))): return
    old = {n: self.state['paragraphs'].pop(f'{section}:{n}') for n in nums}
    for new, n in enumerate(nums): self.state['paragraphs'][f'{section}:{new}'] = old[n]
    self.save()
Builder.migrate_slots = _migrate_slots

def _chapter2(self, section):
    ch = self.spec['chapters'][section]
    self.migrate_slots(section)
    final = ch.get('final') or (ch['paragraphs'] + ch.get('extend', []))
    for k, p in enumerate(final): self._para(section, k, p)
    for fig in ch.get('figures', []): self.put_figure(section, fig)
    keep = set()
    for i, pr in enumerate(ch.get('problems', [])):
        keep.add(f'{section}:{i}'); self.put_exercise(section, f'{section}:{i}', pr)
    for i, ex in enumerate(ch.get('exercises', [])):
        keep.add(f'{section}:x{i}'); self.put_exercise(section, f'{section}:x{i}', ex)
    for key in [k for k in self.state['problems'] if k.startswith(section + ':') and k not in keep]:
        call(self.book, 'studium_problem_remove', id=self.state['problems'][key]['id']); del self.state['problems'][key]; self.save()
    n = len(final)
    print('chapter', section, 'paragraphs', n, 'figures', len(ch.get('figures', [])), 'exercises', len(ch.get('exercises', [])) + len(ch.get('problems', [])))

def _para(self, section, idx, p):
    pid = self.paragraph(section, idx, p)
    if p.get('audit', True):
        ex = self.state['paragraphs'][f'{section}:{idx}']['ex']
        if len({k for k, _ in p['quotes']}) >= 2: self.audit(pid, self.spec.get('audit_kind', 'historical'), ex, p['text'])
        else: print('  WARN needs 2 sources for audit:', section, idx)
Builder._para = _para
Builder.chapter = _chapter2
