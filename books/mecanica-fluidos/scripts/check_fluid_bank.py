"""Reproducible checks; alternate arithmetic is not an independent peer review."""
import json,math
from pathlib import Path
import numpy as np
import pint
import sympy as sp
from scipy.integrate import quad, solve_ivp
from fluid_bank import cases,evaluate

ROOT=Path(__file__).resolve().parents[1]
U=pint.UnitRegistry();Q=U.Quantity
def scalar(q):return q.to('').magnitude if hasattr(q,'to') else q
FUN={'pi':math.pi,'g':Q(9.81,'m/s**2'),'sqrt':lambda x:x**.5}
FUN.update({n:(lambda x,fn=getattr(math,n):fn(scalar(x))) for n in ['sin','cos','tan','exp','log','erfc']})
records=[]
def ck(name,condition,route):
    records.append(dict(name=name,passed=bool(condition),route=route))
    if not condition:raise AssertionError(name)
def same(a,b):return math.isclose(a,b,rel_tol=2e-10,abs_tol=2e-10)

def validate(bank):
    for p in bank:
        env=FUN|{k:Q(v,u or '') for k,v,u,_,_ in p['data']}
        for row in evaluate(p):
            got=eval(row['expression'],{'__builtins__':{}},env)
            if not hasattr(got,'to'):got=Q(got,'')
            value=got.to(row['unit'] or '').magnitude
            ck(p['id']+':'+row['symbol'],same(value,row['value']),'Pint dimensional evaluation / Python math versus SymPy 32-digit arithmetic')
            env[row['symbol']]=got

def model_checks():
    b=cases()
    def val(i):return {r['symbol']:r['value'] for r in evaluate(b[i-1])}
    def data(i):return {r[0]:r[1] for r in b[i-1]['data']}
    t,x,y,nu,h,a,G,mu,U0=sp.symbols('t x y nu h a G mu U',positive=True)
    v0,k,m=sp.symbols('v0 k m',positive=True)
    v=v0/(1+k*v0*t/m);xx=m/k*sp.log(1+k*v0*t/m)
    ck('quadratic drag differential residual',sp.simplify(m*sp.diff(v,t)+k*v*v)==0,'symbolic ODE residual')
    ck('quadratic drag position',sp.simplify(sp.diff(xx,t)-v)==0,'differentiate displacement')
    uu=U0*y/h+G*y*(h-y)/(2*mu)
    ck('Couette-Poiseuille equation',sp.simplify(mu*sp.diff(uu,y,2)+G)==0,'boundary value residual')
    ck('Couette-Poiseuille boundaries',uu.subs(y,0)==0 and sp.simplify(uu.subs(y,h)-U0)==0,'two no-slip boundaries')
    decay=U0*sp.sin(sp.pi*y/h)*sp.exp(-nu*sp.pi**2*t/h**2)
    ck('sine diffusion PDE',sp.simplify(sp.diff(decay,t)-nu*sp.diff(decay,y,2))==0,'PDE residual')
    startup=U0*sp.erfc(y/(2*sp.sqrt(nu*t)))
    ck('impulsive plate PDE',sp.simplify(sp.diff(startup,t)-nu*sp.diff(startup,y,2))==0,'PDE residual')
    ck('stagnation acceleration',sp.simplify(a*x*sp.diff(a*x,x)-a**2*x)==0,'convective differentiation')
    d=data(13);r=val(13)
    force=quad(lambda ss:d['rho']*9.81*d['b']*(d['h0']+ss*math.sin(d['theta'])),0,d['L'])[0]
    moment=quad(lambda ss:d['rho']*9.81*d['b']*ss*(d['h0']+ss*math.sin(d['theta'])),0,d['L'])[0]
    ck('gate force quadrature',same(force,r['F']),'adaptive quadrature of pressure')
    ck('gate moment quadrature',same(moment,r['M']),'adaptive quadrature of moment')
    ck('gate pressure centre',d['L']/2<r['sr']<d['L'],'physical bounds')
    d=data(18);r=val(18)
    integral=quad(lambda rr:d['rho']*(r['aa']*rr+r['bb']/rr)**2/rr,d['Ri'],d['Ro'])[0]
    ck('circular Couette radial pressure',same(integral,r['dp']),'positive radial quadrature versus cancellation-prone closed form')
    ck('floating stability',val(15)['GM']>0 and val(15)['moment']<0,'restoring sign')
    ck('polar quadratic remainder',val(19)['rest']>0,'nonnegative residual quadratic drag')
    ck('minimum power feasibility',val(21)['margin']>0,'supplied lift constraint')
    d=data(26);r=val(26)
    ck('actuator energy',same(r['power'],d['rho']*r['A']*r['ud']*(d['U']**2-r['uw']**2)/2),'far-wake kinetic flux')
    ck('moving jet energy',same(val(27)['power'],val(27)['energy']),'laboratory kinetic flux versus mechanical power')
    ck('Darcy convention',same(val(30)['dp'],val(30)['dp2']),'integrated laminar momentum versus Darcy-Weisbach')
    d=data(34);r=val(34)
    sol=solve_ivp(lambda tt,hh:[-d['Cd']*d['Ao']/d['At']*math.sqrt(2*9.81*max(hh[0],0))],[0,r['time']],[d['h0']],rtol=1e-11,atol=1e-12)
    ck('tank terminal level',abs(sol.y[0,-1]-d['h1'])<1e-9,'numerical time integration versus separated solution')
    th=sp.symbols('theta',real=True)
    ck('cylinder zero pressure drag',sp.integrate((1-4*sp.sin(th)**2)*sp.cos(th),(th,0,2*sp.pi))==0,'pressure-force integration')
    ck('viscous heating balance',same(2*val(38)['qwall'],val(38)['power']),'wall heat extraction versus work')
    ck('small-Re unsteady counterexample',val(45)['Re']<.001 and val(45)['product']>1,'separate local and convective inertia scales')
    d=data(46);r=val(46)
    ck('geostrophic orthogonality',abs(r['ug']*d['px']+r['vg']*d['py'])<1e-14,'pressure gradient dot velocity')
    ck('Boussinesq density variation',val(48)['variation']<.01,'small prescribed density change; not a full validity proof')

if __name__=='__main__':
    from make_fluid_books import exams
    validate(cases());validate([p for exam in exams() for p in exam]);model_checks()
    result=dict(status='PASSED',problems=48,exam_variants=20,checks=len(records),reviewer='same authoring agent; two numerical routes and selected residuals, not independent scientific approval',records=records)
    (ROOT/'reports/fluid-bank-checks.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print(len(records),'checks passed')
