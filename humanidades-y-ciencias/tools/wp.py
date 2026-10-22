import json,sys,urllib.parse,subprocess,re
from pathlib import Path
import os
OUT=Path(os.environ.get('STUDIUM_WS', Path.home()/'studium-ws'))/'src'
def wp(lang,title):
    u=f'https://{lang}.wikipedia.org/w/api.php?action=query&prop=extracts&explaintext=1&format=json&redirects=1&titles='+urllib.parse.quote(title)
    import time
    for k in range(6):
        r=subprocess.run(['curl','-sL','--max-time','30','-A','studium-research/1.0 (contact: see repository)',u],capture_output=True,text=True).stdout
        if r.startswith('{'): break
        time.sleep(15)
    d=json.loads(r); p=list(d['query']['pages'].values())[0]
    t=p.get('extract','')
    f=OUT/f'{lang}_{re.sub(r"[^A-Za-z0-9]+","_",title)}.txt'
    f.write_text(t,encoding='utf-8'); return f,len(t),p.get('title')
if __name__=='__main__':
    lang=sys.argv[1]
    for t in sys.argv[2:]:
        print(wp(lang,t))
