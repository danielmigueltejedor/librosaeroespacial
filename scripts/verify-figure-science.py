#!/usr/bin/env python3
"""Source-bound invariants for corrected scientific diagrams, not expert approval."""
from pathlib import Path
import csv,hashlib,json,math,re
import numpy as np
import sympy as sp
R=Path(__file__).resolve().parents[1];rows=[]
def check(key,source,passed,evidence):
 rows.append(dict(id=key,source=source,passed=bool(passed),classification='derived',evidence=evidence))
def text(p):return (R/p).read_text()
# Independent tensor eigenproblem and affine source-coordinate checks for every unique Mohr drawing.
seen=set()
for path in (R/'books/estructuras-aeroespaciales').rglob('*.tex'):
 for block in re.findall(r'\\begin\{tikzpicture\}.*?\\end\{tikzpicture\}',path.read_text(),re.S):
  if '% studium:mohrpoint' not in block:continue
  h=hashlib.sha256(block.encode()).hexdigest()
  if h in seen:continue
  seen.add(h);source=str(path.relative_to(R));pts=re.findall(r'% studium:mohrpoint (P[xy]) sigma=([-\d.e]+) tau=([-\d.e]+) scale=([-\d.e]+) offset=([-\d.e]+)\n\\fill\[[^\n]*?\] \(([-\d.e]+),([-\d.e]+)\)',block)
  circles=re.findall(r'% studium:circle centre=([-\d.e]+) radius=([-\d.e]+) scale=([-\d.e]+) offset=([-\d.e]+)\n\\draw\[[^\n]*?\] \(([-\d.e]+),0\) circle \(([-\d.e]+)\)',block)
  check('mohr-source-parsed-'+h[:8],source,len(pts)==2 and len(circles)==3,'Two stress points and three circles bound directly to rendered coordinates.')
  if len(pts)!=2 or len(circles)!=3:continue
  sx,tau,k,C=map(float,pts[0][1:5]);sy=float(pts[1][1]);eig=np.linalg.eigvalsh([[sx,-tau],[-tau,sy]]);rad=(eig[1]-eig[0])/2
  check('mohr-eigen-'+h[:8],source,abs(float(circles[0][0])-(sx+sy)/2)<1e-10 and abs(float(circles[0][1])-rad)<1e-10,{'eigenvalues_MPa':eig.tolist()})
  for name,v,t,k,off,x,y in pts:
   v,t,k,off,x,y=map(float,[v,t,k,off,x,y]);check(f'mohr-{name}-geometry-'+h[:8],source,max(abs(x-(v-off)*k),abs(y-t*k))<6e-6,'One isotropic affine scale for both axes; stress point lies on the physical circle.')
  for i,(c,r,k,off,x,rp) in enumerate(circles):
   c,r,k,off,x,rp=map(float,[c,r,k,off,x,rp]);check(f'mohr-circle-{i}-geometry-'+h[:8],source,abs(x-(c-off)*k)<6e-6 and abs(rp-r*k)<6e-6,'Actual TikZ centre and radius agree with MPa metadata.')
  theta=.5*math.atan2(-2*tau,sx-sy);rot=np.array([[math.cos(theta),math.sin(theta)],[-math.sin(theta),math.cos(theta)]]);T=rot@np.array([[sx,-tau],[-tau,sy]])@rot.T
  check('mohr-angle-'+h[:8],source,abs(T[0,1])<1e-10 and abs(T[0,0]-eig[1])<1e-10,'Principal rotation annihilates transformed shear and selects the larger in-plane eigenvalue.')
# Resultants and their first moments, independently integrated.
x,L,q=sp.symbols('x L q',positive=True)
check('uniform-resultant','books/estructuras-aeroespaciales/latex/manual.tex',sp.integrate(q,(x,0,L))==q*L and sp.integrate(x*q,(x,0,L))/(q*L)==L/2,'Uniform load qL at L/2.')
check('triangle-resultant','books/estructuras-aeroespaciales/latex/manual.tex',sp.integrate(q*x/L,(x,0,L))==q*L/2 and sp.integrate(x*q*x/L,(x,0,L))/(q*L/2)==2*L/3,'Increasing triangle resultant qL/2 at 2L/3 from its zero end.')
s=text('books/estructuras-aeroespaciales/latex/manual.tex');check('rendered-load-signs','books/estructuras-aeroespaciales/latex/manual.tex','(2,-0.1) -- (2,-0.9)' in s and '(2.667,-0.1) -- (2.667,-0.9)' in s,'Actual red arrows point down, like the distributed loads.')
B,y,V=sp.symbols('B y V',positive=True);flow=V*B*y/(4*B*y*y)
check('two-web-shear-resultant','books/estructuras-aeroespaciales/latex/manual.tex',sp.simplify(2*flow*2*y-V)==0 and '(0,3) -- (0,1.5)' in s and '(0,1.5) -- (0,0.1)' in s,'Both webs sum to V; equal lever arms give zero torsional moment about the symmetry plane.')
h,rho,g,b=sp.symbols('h rho g b',positive=True);F=sp.integrate(rho*g*h*b,(h,0,L));depth=sp.simplify(sp.integrate(h*rho*g*h*b,(h,0,L))/F)
fl=text('books/mecanica-fluidos/latex/manual.tex');check('hydrostatic-wall-force','books/mecanica-fluidos/latex/manual.tex',depth==2*L/3 and '(0.05,\\y) -- ({2.4*(3-\\y)/3},\\y)' in fl,'Pressure and resultant on the wall point away from water at left; application depth 2H/3.')
phi=math.radians(35);W=2*math.cos(phi);Lift=np.array([2*math.sin(phi),W]);wing=np.array([1,-math.tan(phi)])
check('turn-force-and-angle','books/mecanica-vuelo/scripts/figures.py',abs(Lift@wing)<1e-12 and abs(Lift[1]-W)<1e-12 and "ax.set_aspect('equal')" in text('books/mecanica-vuelo/scripts/figures.py'),'Banked wing perpendicular to lift; vertical lift balances weight; isotropic plotting scale.')
gamma=-.12;Vunit=np.array([math.cos(gamma),math.sin(gamma)]);Lunit=np.array([-math.sin(gamma),math.cos(gamma)]);net=1.8*math.cos(gamma)*Lunit+1.8*math.sin(gamma)*Vunit+np.array([0,-1.8])
check('glide-force-balance','books/mecanica-vuelo/scripts/figures.py',np.linalg.norm(net)<1e-12,'L=W cos(gamma), D=−W sin(gamma); exact vector closure for steady glide.')
# Recomputed full-throttle evidence must hold the airplane fixed at each trimmed point.
csvpath='books/mecanica-vuelo/simulations/results/t6-trim-grid.csv';data=list(csv.DictReader((R/csvpath).open()))
check('jsbsim-full-throttle-grid',csvpath,len(data)==44 and all(float(v['max_throttle_position'])==1 and float(v['max_engine_n1'])>=99.99 and v['held_airframe']=='True' and float(v['max_thrust_N'])>float(v['thrust_N']) for v in data),'44 trims; full FCS throttle, N1, held kinematics/time, available thrust above trim thrust.')
for i,v in enumerate(data):
 excess=(float(v['max_thrust_N'])-float(v['drag_N']))*float(v['TAS_m_s'])/(float(v['mass_kg'])*9.80665)
 check(f'jsbsim-available-power-{i:02}',csvpath,math.isclose(excess,float(v['excess_power_approx_m_s']),rel_tol=1e-12),'Power/weight relation independently recomputed from published CSV columns.')
# Actual saved render hashes bind practice checks to assets.
p=R/'books/mecanica-fluidos/evidence/practice-figure-redraws.json';redraw=json.loads(p.read_text())
for a in redraw['figures']:
 check('practice-'+a['id'],'books/mecanica-fluidos/'+a['file'],all(a['checks'].values()) and hashlib.sha256((p.parents[1]/a['file']).read_bytes()).hexdigest()==a['sha256'],a['checks'])
# Every flow-table value must remain visible, including rational-position extrema.
from fractions import Fraction
flows_seen=set()
for path in (R/'books/estructuras-aeroespaciales').rglob('*.tex'):
 for block in re.findall(r'\\begin\{tikzpicture\}.*?\\end\{tikzpicture\}',path.read_text(),re.S):
  if '% studium:flow' not in block:continue
  h=hashlib.sha256(block.encode()).hexdigest()
  if h in flows_seen:continue
  flows_seen.add(h)
  vals=re.findall(r'% studium:qlabel \S+ s=([-\d./]+) value=([-\d.]+)',block)
  constants=re.findall(r'% studium:qconstant \S+ value=([-\d.]+)',block)
  ok=all(f'{float(Fraction(pos)):.2f}\\mapsto {float(val):.2f}' in block for pos,val in vals) and all(f'|q|={float(v):.2f}' in block for v in constants)
  check('flow-table-values-'+h[:8],str(path.relative_to(R)),ok,'All retained endpoint and interior-extremum metadata agree with the visible panel table, including rational s positions.')
cyl=json.loads((R/'books/mecanica-fluidos/evidence/cylinder-streamlines.json').read_text())
check('potential-cylinder-streamlines','books/mecanica-fluidos/latex/manual.tex',all(c['max_streamfunction_residual']<1e-10 and c['minimum_radius']>1 for c in cyl['curves']),'Five finite positive streamlines and symmetric negative partners satisfy psi/U=y(1−1/r²), with r>1 everywhere; impermeable circular boundary.')
report=dict(status='PASSED' if all(r['passed'] for r in rows) else 'FAILED',checks=len(rows),mohr_drawings=len(seen),reviewer='Same authoring model; no independent approval',scope='Corrected force directions, moment/pressure integrals, tensor invariants, actual drawing coordinates, practice model checks and full-throttle data. Does not certify all equations in the collection.',records=rows)
(R/'reports/edition-v2/figure-science-checks.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(report['status'],len(rows),'figure science checks;',len(seen),'Mohr diagrams')
for r in rows:
 if not r['passed']:print(r)
raise SystemExit(report['status']!='PASSED')
