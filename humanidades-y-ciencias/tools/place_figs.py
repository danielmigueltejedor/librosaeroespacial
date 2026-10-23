"""Attach each figure to the paragraph that explains it by adding a {{fig:key}} reference to that paragraph."""
import re

STOP = set('de la el los las un una y o en que se por con para del al es son su sus como más este esta entre sobre'.split())


def words(text):
    return {w for w in re.findall(r'[a-záéíóúñü]{5,}', text.lower()) if w not in STOP}


def quote_set(item):
    return {(k, ' '.join(q.split())) for k, q in item.get('quotes', [])}


OVERRIDES = {
    # biology
    'pasteur-nadar': 16, 'plasmolisis-cebolla': 8, 'axon-mielinico': 17, 'franklin-microscopio': 4, 'modelo-crick-watson': 3,
    'frotis-falciforme': 18, 'falciforme-mutacion': 17, 'hemoglobina-3d': 18, 'morgan': 10, 'ecoli-sem': 3,
    'ingenhousz': 4, 'termociclador': 7, 'jenner': 15, 'pearson': 13,
    # literature
    'alexandre-manuscrito': 7, 'berceo-estatua': 9, 'baroja-retrato': 18, 'dario-retrato': 1, 'azul-primera-edicion': 2,
    'lope-pacheco': 14,
}


def plan(paragraphs, figures):
    """Return {figure key: paragraph index}. Prefer shared evidence quotes, then shared words; spread figures out."""
    scored = []
    for fi, fig in enumerate(figures):
        fq, fw = quote_set(fig), words(fig['caption'] + ' ' + fig['key'].replace('-', ' '))
        for pi, par in enumerate(paragraphs):
            if par.get('role') in ('purpose',) or len(par['text']) < 200:
                continue
            s = 12 * len(fq & quote_set(par)) + len(fw & words(par['text']))
            scored.append((s, -pi, fi, pi))
    scored.sort(reverse=True)
    used_fig, count, placed = set(), {}, {}
    for fi, fig in enumerate(figures):
        if fig['key'] in OVERRIDES and OVERRIDES[fig['key']] < len(paragraphs):
            used_fig.add(fi); count[OVERRIDES[fig['key']]] = count.get(OVERRIDES[fig['key']], 0) + 1; placed[fig['key']] = OVERRIDES[fig['key']]
    for cap in (1, 2, 3):
        for s, _, fi, pi in scored:
            if fi in used_fig or s <= 0 or count.get(pi, 0) >= cap:
                continue
            used_fig.add(fi); count[pi] = count.get(pi, 0) + 1; placed[figures[fi]['key']] = pi
    return placed


def apply(paragraphs, figures, verb='véase'):
    placed = plan(paragraphs, figures)
    out = [dict(p) for p in paragraphs]
    by_par = {}
    for key, pi in placed.items():
        by_par.setdefault(pi, []).append(key)
    for pi, keys in by_par.items():
        refs = ' y '.join('{{fig:%s}}' % k for k in keys) if len(keys) == 2 else ', '.join('{{fig:%s}}' % k for k in keys)
        text = out[pi]['text'].rstrip()
        if any('{{fig:%s}}' % k in text for k in keys):
            continue
        out[pi]['text'] = (text[:-1] + f' ({verb} {refs}).') if text.endswith('.') else text + f' ({verb} {refs})'
    missing = [f['key'] for f in figures if f['key'] not in placed]
    return out, placed, missing
