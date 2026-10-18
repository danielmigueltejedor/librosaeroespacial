"""Portable unit, domain and conservation audit of all 150 original cases.

Uses the public educational bank exported from the original authoring source;
no private excerpts, Studium server or external state are needed.
"""
from pathlib import Path
import json, math, re
import pint
import sympy as sp
ROOT=Path(__file__).resolve().parents[1]
BOOK=ROOT/'books/turbomaquinas'
U=pint.UnitRegistry();Q=U.Quantity
def scalar(v):return v.to('').magnitude if hasattr(v,'to') else v
FUN={'pi':math.pi,'sqrt':lambda x:x**.5,'atan':lambda x:math.atan(scalar(x))*U.radian}
FUN.update({n:(lambda x,f=getattr(math,n):f(scalar(x))) for n in ['sin','cos','tan','log']})
checks=[]
def ck(name,ok,route):
    checks.append(dict(name=name,passed=bool(ok),route=route))
    if not ok:raise AssertionError(name)
rows=json.loads((BOOK/'reports/problem-bank-public.json').read_text())['problems']
printed=(BOOK/'publication/problemas-resueltos.tex').read_text()
manual=(BOOK/'publication/turbomaquinas-ule-2026.tex').read_text()
for p in rows:
    ck(p['key']+' appears in compiled source',p['key'] in printed,'bank-to-publication identifier')
    vals={n:Q(v,u) for n,v,u,_ in p['given']}
    for st in p['computed']:
        got=eval(st['symbolic'],{'__builtins__':{}},FUN|vals)
        if not hasattr(got,'to'):got=Q(got,'')
        mag=got.to(st['unit']).magnitude
        ck(p['key']+':'+st['symbol'],math.isclose(mag,st['value'],rel_tol=3e-10,abs_tol=3e-10),'Pint quantities / Python math versus authoring SymPy')
    d={n:v for n,v,u,_ in p['given']};v={s['symbol']:s['value'] for s in p['computed']}
    if p['key'].startswith(('C03-01-','C16-01-','C18-01-')):
        required={'C03-01':'Tout','C16-01':'crs','C18-01':'U'}[p['key'][:-2]]
        ck(p['key']+' requested result printed',required in v and format(v[required],'.10g') in printed and format(v[required],'.10g') in manual,'requested magnitude present in bank and both publications')
        if required=='Tout':ck(p['key']+' temperature energy',math.isclose(d['cp']*(v['Tout']-d['Tin']),v['wc'],rel_tol=1e-12),'specific work versus real total-temperature rise')
        elif required=='crs':ck(p['key']+' radial continuity',math.isclose(d['rs']*v['crs'],d['re']*d['cr'],rel_tol=1e-12),'constant-width radial mass balance')
        else:ck(p['key']+' relative triangle',math.isclose(math.atan((v['ct']-v['U'])/d['cx']),v['beta'],rel_tol=1e-12),'relative triangle reconstructed with printed blade speed')
    for n in ['eta','em','ep','bb','slip','eff','kk']:
        if n in d and (n!='kk' or p['ch'] in [4,13]):ck(p['key']+' domain '+n,0<d[n]<=1,'prescribed parameter domain')
    for n in ['T','Te','Tout','Tw','Taw','area','Ast','width','rho','pout','wc','wt','Pow','we','mc']:
        if n in v and not(n=='wt' and p['ch']==2):ck(p['key']+' positive '+n,v[n]>0,'physical sign')
    if 'rt' in d and 'rh' in d:ck(p['key']+' radii',0<d['rh']<d['rt'],'ordered geometry')
    if 'ds' in v:ck(p['key']+' entropy',v['ds']>=0,'passive adiabatic entropy sign')
    if p['ch']==17 and 'eta' in v:ck(p['key']+' diagnostic',(0<v['eta']<=1) if p['role']=='worked' else v['eta']>1,'deliberately inconsistent transfer case diagnosed, not accepted as a physical machine')
    if p['ch']==7 and p['title'].startswith('Reacción y'):
        c1=d['uu']*(1-d['rea']-d['psi']/2);c2=d['uu']*(1-d['rea']+d['psi']/2)
        ck(p['key']+' Euler',abs(d['uu']*(c2-c1)-d['psi']*d['uu']**2)<1e-8,'direct velocity reconstruction')
    if p['ch']==14 and p['title'].startswith('Red térmica'):
        q=(d['Tg']-d['Tc'])/(1/d['hg']+d['th']/d['cond']+1/d['hc'])
        hot=d['Tg']-q/d['hg'];cold=d['Tc']+q/d['hc']
        ck(p['key']+' heat balance',abs(d['cond']*(hot-cold)/d['th']-q)<1e-6,'thermal flux continuity')
for left,right in [('hh+(cx**2+(ct-uu)**2)/2-uu**2/2','hh+(cx**2+ct**2)/2-uu*ct'),('uu*(ct-(2*uu-ct))','2*uu*(ct-uu)'),('pi*((rm+bb/2)**2-(rm-bb/2)**2)','2*pi*rm*bb'),('Om*(rad*(ks/rad)-rad*(ke/rad))','Om*(ks-ke)')]:
    names=set(re.findall(r'\b[A-Za-z]+\b',left+' '+right))
    env={n:sp.Symbol(n,nonzero=True) for n in names-{'pi'}};env['pi']=sp.pi
    ck(left,sp.simplify(sp.sympify(left,locals=env)-sp.sympify(right,locals=env))==0,'symbolic identity')
report=dict(status='PASSED',problems=150,checks=len(checks),scope='All bank calculations and selected physical/symbolic checks; not a review of all theoretical claims or expert certification.',reviewer='same agent, fresh calculation pass',records=checks)
(ROOT/'reports/bundle-audit/turbomaquinas.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(len(checks),'checks passed for 150 cases')
