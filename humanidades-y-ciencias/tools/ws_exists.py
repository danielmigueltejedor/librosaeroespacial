import sys, json, urllib.parse, subprocess
def exists(titles, host='es.wikisource.org'):
    out = {}
    for i in range(0, len(titles), 40):
        chunk = titles[i:i+40]
        u = f'https://{host}/w/api.php?action=query&format=json&redirects=1&titles=' + urllib.parse.quote('|'.join(chunk))
        r = subprocess.run(['curl','-sL','--max-time','40','-A','studium-research/1.0',u],capture_output=True,text=True).stdout
        d = json.loads(r)['query']
        norm = {n['from']: n['to'] for n in d.get('normalized', [])}
        red = {n['from']: n['to'] for n in d.get('redirects', [])}
        pages = {p['title']: ('missing' not in p) for p in d['pages'].values()}
        for t in chunk:
            x = norm.get(t, t); x = red.get(x, x)
            out[t] = pages.get(x, False)
    return out
if __name__ == '__main__':
    ts = [l.strip() for l in sys.stdin if l.strip()]
    for t, ok in exists(ts).items(): print('OK ' if ok else '-- ', t)
