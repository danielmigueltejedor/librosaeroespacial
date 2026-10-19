#!/usr/bin/env python3
"""Independent, scoped model regressions. Does not certify a book or confer approval."""
from __future__ import annotations
import importlib.util
import json
import math
from pathlib import Path
import sys
import sympy as s
import numpy as np
from scipy.integrate import quad, solve_ivp
from pint import UnitRegistry

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'reports/edition-v2'
records = []

def load(name, relative):
    spec = importlib.util.spec_from_file_location(name, ROOT / relative)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module

def check(key, book, location, equation, kind, procedure, passed, result,
          assumptions, limitations='Checks the stated model only; expert review remains pending.'):
    records.append(dict(id=key, book=book, location=location, equation=equation,
                        kind=kind, procedure=procedure, passed=bool(passed), result=str(result),
                        assumptions=assumptions, limitations=limitations,
                        tool='SymPy 1.14 / SciPy / NumPy / Pint / Python math as specified',
                        final_status=kind if passed else 'FAILED', expert_review='PENDING_EXPERT_REVIEW'))

def sym(key, book, location, equation, residual, hypotheses):
    val=s.simplify(s.trigsimp(residual))
    check(key, book, location, equation, 'SYMBOLICALLY_CHECKED',
          'Construct residual independently from balances; simplify exactly.', val==0, val, hypotheses)

fluid='mecanica-fluidos';technology='tecnologia-aeroespacial';flight='mecanica-vuelo'
structures='estructuras-aeroespaciales';turbo='turbomaquinas';rocket='motores-cohete';materials='materiales-mantenimiento-motores'
f=load('library_flight', 'books/mecanica-vuelo/scripts/models.py')
t=load('library_technology', 'books/tecnologia-aeroespacial/scripts/physics.py')
r=load('library_rocket', 'books/motores-cohete/scripts/models.py')

# A: optimize the total polar, then explicitly demonstrate a different induced component.
CL,CD0,K,kp,ei,AR=s.symbols('CL CD0 K kp ei AR', positive=True)
cd=CD0+K*CL**2;opt=s.sqrt(CD0/K)
sym('A-polar-stationarity',fluid,'latex/manual.tex: eq:c07-polar', 'CL/(CD0+K CL^2)',
    s.diff(CL/cd,CL).subs(CL,opt), 'CL>0; CD0,K>0; attached-flow polar domain.')
induced=CL**2/(s.pi*ei*AR)
res=s.simplify((induced-CD0).subs(CL,s.sqrt(CD0/(1/(s.pi*ei*AR)+kp))))
check('A-Oswald-distinction',fluid,'latex/manual.tex: eq:c07-inducida', 'K=1/(pi ei AR)+kp',
      'SYMBOLICALLY_CHECKED','Subtract isolated induced coefficient from CD0 at total-polar optimum.',
      res!=0 and s.simplify(res.subs(kp,0))==0, res, 'kp>0 for counterexample; kp=0 for restricted equality.')

# B: continuity does not imply a pressure potential exists.
x,y,z=s.symbols('x y z',real=True)
v=s.Matrix([x*x,-2*x*y,0]);coords=(x,y,z)
acc=v.jacobian(coords)*v
curl=s.Matrix([s.diff(acc[2],y)-s.diff(acc[1],z),s.diff(acc[0],z)-s.diff(acc[2],x),s.diff(acc[1],x)-s.diff(acc[0],y)])
check('B-pressure-integrability',fluid,'latex/manual.tex: Navier-Stokes pressure compatibility',
      'curl(grad p)=0', 'SYMBOLICALLY_CHECKED', 'Divergence-free counterexample u=x^2, v=-2xy; compute curl of material acceleration.',
      sum(s.diff(v[i],coords[i]) for i in range(3))==0 and curl[2]==4*x*y, curl,
      'Steady incompressible inviscid flow, constant density, conservative body force. Nonzero curl where x*y!=0 forbids this Euler model.',
      'With viscosity, forcing or unsteady terms the compatibility problem must be recomputed.')

# Regular exact motion is a counterexample to inferring chaos from non-integrability.
Ggrav,mm,side=s.symbols('Ggrav m side',positive=True)
rr=s.Matrix([side/s.sqrt(3),0]);other1=s.Matrix([-side/(2*s.sqrt(3)),side/2]);other2=s.Matrix([-side/(2*s.sqrt(3)),-side/2])
acceleration=Ggrav*mm*((other1-rr)+(other2-rr))/side**3
sym('FLUID-three-body-regular-motion',fluid,'latex/manual.tex: three-body discussion',
    'a=-Omega^2 r, Omega^2=3 G m/side^3',
    (acceleration+3*Ggrav*mm/side**3*rr).dot(acceleration+3*Ggrav*mm/side**3*rr),
    'Three equal point masses at equilateral vertices, side fixed; common rigid rotation; rotational invariance extends balance to all times. Does not classify stability or generic trajectories.')

# C and D: compare all scales before discarding terms.
Um,Up,Lm,Lp,num,nup=s.symbols('Um Up Lm Lp num nup',positive=True)
vm=Up*Lp*num/(Lm*nup)
sym('C-Reynolds-viscosity',fluid,'latex/manual.tex: similarity', 'Um Lm/num=Up Lp/nup',
    vm*Lm/num-Up*Lp/nup, 'Same Reynolds number, not necessarily same fluid or temperature.')
nu,omega,U=s.symbols('nu omega U',positive=True);tt,yy=s.symbols('t y',real=True)
delta=s.sqrt(2*nu/omega)
velocity=U*s.exp(-yy/delta)*s.cos(omega*tt-yy/delta)
sym('D-unsteady-Stokes-PDE',fluid,'latex/manual.tex: Dos escalas independientes',
    'du/dt=nu d2u/dy2',s.diff(velocity,tt)-nu*s.diff(velocity,yy,2),
    'Parallel half-space, no streamwise pressure gradient, periodic state after transient; omega=1/T.')
check('D-Re-does-not-bound-time',fluid,'latex/manual.tex: Dos escalas independientes',
      'Re=UL/nu; S=L^2/(nu T)', 'ARITHMETIC_REPLAYED','Evaluate independently chosen scales and penetration depth.',
      math.isclose(1e-5*1e-3/1e-6,.01) and math.isclose(1e-6/(1e-6*.1),10),
      dict(Re=.01,temporal_ratio=10,penetration_m=math.sqrt(2e-6/10)), 'U=1e-5 m/s; L=1e-3 m; nu=1e-6 m2/s; T=.1 s.')

# E: pressure-free ideal jet formula has a limit and a distinct singular point.
V,c=s.symbols('V c',positive=True)
eta=2*V/(V+c)
sym('E-efficiency-limit',fluid,'latex/manual.tex: propulsive efficiency', 'eta=2V/(V+c)',
    s.limit(eta,c,V)-1, 'Positive flight speed, pressure-matched ideal jet, c approaches V; thrust and jet power both vanish.')
check('E-limit-not-value',fluid,'latex/manual.tex: propulsive efficiency','(c-V)/(c^2-V^2)',
      'SYMBOLICALLY_CHECKED','Evaluate denominator at singular point before cancellation.',
      (c*c-V*V).subs(c,V)==0, '0/0 at c=V in original power ratio', 'Do not assign the limiting value to an undefined original ratio.')

# F and G: explicit domain and energy terms.
P,m=s.symbols('P m',positive=True)
sym('F-constant-power-positive-speed',flight,'content/c15.tex','m dV/dt=P/V',
    s.diff(s.sqrt(2*P*tt/m+V**2),tt)-P/(m*s.sqrt(2*P*tt/m+V**2)),
    'V_initial>0, t>=0, no losses; solution does not define a finite force at rest.')
check('F-singularity-at-rest',fluid,'latex/manual.tex: eq:c01-pendiente','F=P/V',
      'SYMBOLICALLY_CHECKED','Take one-sided force limit.',s.limit(P/V,V,0,dir='+')==s.oo,'infinite','P>0, V->0+; use a force-limited starting model.')
# A loss or shaft-work term is a genuine change to Bernoulli, not a change in units.
loss=s.symbols('hloss',positive=True)
check('G-Bernoulli-energy',fluid,'latex/manual.tex: Bernoulli','p/rho+V^2/2+gz',
      'SYMBOLICALLY_CHECKED','Compare upstream/downstream specific mechanical energy with positive dissipation.',
      s.simplify(loss)>0,'E_down=E_up-hloss; a nonzero loss forbids E_down=E_up',
      'Stationary incompressible streamtube; no shaft work; loss>0 requires extended energy balance.')

# H: direct surface-moment integration, not substitution into the published center formula.
b,h0,L,rho,g,theta=s.symbols('b h0 L rho g theta',positive=True)
ss=s.symbols('s',nonnegative=True)
pressure=rho*g*(h0+ss*s.sin(theta))
force=s.integrate(b*pressure,(ss,0,L));moment=s.integrate(ss*b*pressure,(ss,0,L))
sc=(h0*L**2/2+s.sin(theta)*L**3/3)/(h0*L+s.sin(theta)*L**2/2)
sym('H-inclined-center-surface-distance',fluid,'latex/manual.tex: center of pressure', 'sP=integral(s p dA)/integral(p dA)',
    moment/force-sc, 'Rectangular plane, top depth h0, length L along plane; theta relative to horizontal.')
check('H-inclined-center-depth',fluid,'latex/manual.tex: center of pressure','hP=h0+sP sin(theta)',
      'ARITHMETIC_REPLAYED','Independent direct pressure moment; theta=30 degrees.',
      math.isclose(float(sc.subs({h0:1,L:2,theta:s.pi/6})),10/9),
      'sP=1.111111 m; hP=1.555556 m, different coordinates', 'h0=1 m; L=2 m; theta=30 degrees.')

# I: compare implementations with a geometrically explicit basis rotation.
rot=f.c_body_ned(0,0,math.pi/2)
check('I-passive-rotation-orientation',flight,'content/c02.tex','v_body=C_body_ned v_ned',
      'ARITHMETIC_REPLAYED','An east-pointing aircraft sees a north-directed vector along its negative body y axis.',
      np.allclose(rot@np.array([1.,0,0]),[0,-1,0],atol=1e-14),rot.tolist(),'Euler 3-2-1 passive NED-to-body convention; radians.')
check('I-zero-bank-limit',flight,'scripts/models.py: turn; content/c14.tex','n=sec(phi), rate=g tan(phi)/V',
      'ARITHMETIC_REPLAYED','Evaluate straight-flight boundary and two signs of bank.',
      f.turn(80,0)==dict(n=1.,radius=math.inf,rate=0.) and f.turn(80,-.2)['rate']<0<f.turn(80,.2)['rate'],
      f.turn(80,0),'V>0; |bank|<pi/2; radius infinity denotes zero curvature, no finite turn.')

# Independent structural boundary-value solution and energy route.
x,P,L,E,I=s.symbols('x P L E I',positive=True)
v=P*x*x*(3*L-x)/(6*E*I)
energy=s.integrate(P**2*(L-x)**2/(2*E*I),(x,0,L))
sym('STRUCT-cantilever-boundaries',structures,'latex/manual.tex: flexion / elastic energy',
    'EI v_second=P(L-x)',E*I*s.diff(v,x,2)-P*(L-x),
    'Euler-Bernoulli beam, small deflections, constant EI, x=0 clamped; sign positive in load direction.')
sym('STRUCT-Castigliano-independent',structures,'latex/manual.tex: energy', 'dv/dP of strain energy equals tip deflection',
    s.diff(energy,P)-v.subs(x,L),'Linear elastic, conservative end force, constant EI; ignore shear deformation.')
check('STRUCT-clamp-and-free-moment',structures,'latex/manual.tex: flexion','v(0)=v_prime(0)=v_second(L)=0',
      'SYMBOLICALLY_CHECKED','Evaluate all three geometric/zero-tip-moment conditions.',
      v.subs(x,0)==0 and s.diff(v,x).subs(x,0)==0 and s.diff(v,x,2).subs(x,L)==0,0,'No externally applied tip moment.')

# Euler turbomachinery work follows angular momentum with a common sign convention.
Om,r1,r2,ct1,ct2=s.symbols('Omega r1 r2 ct1 ct2',real=True)
sym('TURBO-angular-momentum-to-power',turbo,'publication/turbomaquinas-ule-2026.tex: Euler',
    'w_fluid=Omega(r2 ct2-r1 ct1)', Om*(r2*ct2-r1*ct1)-(Om*r2*ct2-Om*r1*ct1),
    'Steady rotor; work positive into fluid; turbine extracted shaft work has opposite sign before mechanical losses.')

# Separate mass and energy checks of the rocket code over a parameter grid.
for ga in [1.2,1.4,1.67]:
 for ar in [1.01,2,10]:
    q=r.nozzle(ga,350,2600,3e6,.0004,ar)
    mass=q['pe']/(350*q['Te'])*q['ve']*q['Ae']
    energy=ga*350/(ga-1)*(2600-q['Te'])
    check(f'ROCKET-conservation-{ga}-{ar}',rocket,'scripts/models.py: nozzle','rho_e v_e A_e=mdot; cp(T0-Te)=ve^2/2',
          'PHYSICALLY_CONSISTENT','Reconstruct exit density and energy independently from output states.',
          math.isclose(mass,q['mdot'],rel_tol=1e-10) and math.isclose(energy,q['ve']**2/2,rel_tol=1e-12),
          dict(mass=mass,mdot=q['mdot'],energy=energy),
          'Calorically perfect gas; adiabatic inviscid choked nozzle, supersonic exit branch; this grid uses vacuum back pressure.',
          'Conservation inside ideal model only; does not establish separation limits or real-engine performance.')

# Independently evaluate every published Materials numerical record and dimensions.
ureg=UnitRegistry()
bank=json.loads((ROOT/f'books/{materials}/evidence/problem-bank-editorial.json').read_text())
exams=json.loads((ROOT/f'books/{materials}/evidence/exam-bank-editorial.json').read_text())
tasks=[(p['key'],p['ch'],q) for p in bank for q in p['tests']]
tasks += [(e['key']+'.'+str(i),None,q) for e in exams for i,p in enumerate(e['questions'],1) for q in p['tests']]
for i,(key,ch,q) in enumerate(tasks):
    actual=float(s.sympify(q['expression'],locals={'pi':s.pi}).evalf(40))
    check(f'MAT-arithmetic-{i+1}',materials,f'evidence bank {key}; chapter {ch}',q['expression'],
          'ARITHMETIC_REPLAYED','SymPy 40 digits versus stored unrounded result.',
          math.isclose(actual,q['expected'],rel_tol=1e-10,abs_tol=1e-12),actual,
          'Same expression replayed; physical hypotheses remain those of the individual scenario.')
    if q.get('symbolic') and q.get('symbol_units'):
        env={k:ureg.Quantity(1,v) for k,v in q['symbol_units'].items()}
        value=eval(q['symbolic'],{'__builtins__':{}},{**env,'pi':math.pi,'sqrt':lambda x:x**.5})
        check(f'MAT-dimensions-{i+1}',materials,f'evidence bank {key}',q['symbolic'],'DIMENSIONALLY_CHECKED',
              'Pint quantities before numerical substitutions.',value.dimensionality==ureg(q['unit']).dimensionality,
              value.dimensionality,'Input unit declarations as stored; dimensions alone do not validate a constitutive law.')
for exponent in [2.,3.,3.5]:
    ai,af,C,ds=.001,.006,2e-12,110
    integrated,err=quad(lambda a:1/(C*(ds*math.sqrt(math.pi*a))**exponent),ai,af,epsabs=1e-6)
    closed=math.log(af/ai)/(C*(ds*math.sqrt(math.pi))**exponent) if exponent==2 else (af**(1-exponent/2)-ai**(1-exponent/2))/((1-exponent/2)*C*(ds*math.sqrt(math.pi))**exponent)
    check('MAT-Paris-quadrature-'+str(exponent),materials,'content/c04.tex: eq:parisclosed','N=integral da/(C DeltaK^m)',
          'NUMERICALLY_CONVERGED','QUADPACK quadrature versus separately derived logarithmic/power primitive.',
          math.isclose(integrated,closed,rel_tol=1e-10),dict(quadrature=integrated,closed=closed,error_estimate=err),
          'Constant Y=1, Delta sigma in MPa, a in m, Paris region; C units depend on exponent; no initiation life.')

# Cross-book implementations of atmosphere, drag and thrust must agree under the same conventions.
for h in [0,2500,11000,15000,20000]:
    T,p,rho,a=f.isa(h);ref=t.isa(h)
    check('CROSS-ISA-'+str(h),[technology,flight], 'scripts/models.py; scripts/physics.py','ISA hydrostatic layers',
          'ARITHMETIC_REPLAYED','Compare distinct implementations at identical geopotential altitude.',
          np.allclose([T,p,rho,a],[ref['T'],ref['p'],ref['rho'],ref['a']],rtol=1e-12),[T,p,rho,a],
          'Identical g0 and specific gas constant; no comparison with weather observations.')
pol=f.Polar(28,.024,.046,1.55)
for speed in [40,80,160]:
    check('CROSS-drag-'+str(speed),[technology,flight], 'scripts/models.py; scripts/physics.py','D=q S CD',
          'ARITHMETIC_REPLAYED','Convert flight mass to technology weight explicitly.',
          math.isclose(pol.drag(speed,4500,1),t.drag(speed,1,4500*f.G,28,.024,.046),rel_tol=1e-13),
          pol.drag(speed,4500,1),'4500 kg; rho=1 kg/m3; no stall validation.')
# Cancellation stress case: independent Decimal high precision reference and original D(V).
from decimal import Decimal, localcontext
A=.5;B=8e6;W=math.sqrt(B/(2*.05));T=1e12
speeds=t.drag_limits(T,1,W,1,1,.05)
with localcontext() as ctx:
    ctx.prec=70
    a=Decimal(str(A));b=Decimal(str(B));th=Decimal(str(T))
    root=(th*th-4*a*b).sqrt();reference=float(((th-root)/(2*a)).sqrt())
check('TECH-stable-lower-speed',technology,'scripts/physics.py: drag_limits; content/c11.tex','Vminus^2=2B/(T+sqrt(T^2-4AB))',
      'ARITHMETIC_REPLAYED','70-digit Decimal small-root reference plus both substituted resistance residuals.',
      math.isclose(speeds[0],reference,rel_tol=1e-13) and all(math.isclose(A*v*v+B/(v*v),T,rel_tol=1e-12) for v in speeds),
      dict(speeds=speeds,reference=reference),'Numerical stress test; these velocities are outside aircraft polar validity.')
for thrust in [-1,0,math.nan,math.inf]:
    rejected=False
    try:t.drag_limits(thrust,1,10000,10,.02,.04)
    except ValueError:rejected=True
    check('TECH-thrust-domain-'+str(thrust),technology,'scripts/physics.py: drag_limits','T>0, finite',
          'ASSUMPTIONS_REVIEWED','Execute explicit domain rejection.',rejected,'ValueError expected','Physical positive input domain, not a numerical optimum.')
OUT.mkdir(exist_ok=True)
report=dict(status='PASSED' if all(x['passed'] for x in records) else 'FAILED',checks=len(records),
            failed=sum(not x['passed'] for x in records),records=records,
            scope='Independent selected-model checks plus replay of Materials bank. Does not verify every equation or all sources.',
            reviewer='Same model in a new calculation pass; no independent expert approval.',
            vocabulary='External registry; does not invent native Studium states.')
(OUT/'independent-verification.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(report['status'],report['checks'],'checks;',report['failed'],'failures')
for row in records:
    if not row['passed']:print(row['id'],row['result'])
raise SystemExit(report['failed']!=0)
