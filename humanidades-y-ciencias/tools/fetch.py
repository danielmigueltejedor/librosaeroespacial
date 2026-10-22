import subprocess,re,sys,html
from html.parser import HTMLParser
from pathlib import Path
import os
OUT=Path(os.environ.get('STUDIUM_WS', Path.home()/'studium-ws'))/'src'
class P(HTMLParser):
    def __init__(s): super().__init__(); s.out=[]; s.skip=0
    def handle_starttag(s,t,a):
        if t in('script','style','noscript','nav','footer','header'): s.skip+=1
        if t in('p','br','div','li','h1','h2','h3','h4','tr','dd','dt'): s.out.append('\n')
    def handle_endtag(s,t):
        if t in('script','style','noscript','nav','footer','header'): s.skip=max(0,s.skip-1)
        if t in('p','div','li','h1','h2','h3','h4','tr'): s.out.append('\n')
    def handle_data(s,d):
        if not s.skip: s.out.append(d)
def fetch(url,key):
    r=subprocess.run(['curl','-sL','--max-time','40','-A','studium-research/1.0 (contact: see repository)',url],capture_output=True).stdout.decode('utf-8','replace')
    p=P(); p.feed(r)
    t=html.unescape(''.join(p.out)); t=re.sub(r'[ \t​]+',' ',t); t=re.sub(r'\n\s*\n+','\n',t)
    f=OUT/f'{key}.txt'; f.write_text(t,encoding='utf-8'); return f,len(t)
if __name__=='__main__':
    print(fetch(sys.argv[1],sys.argv[2]))
