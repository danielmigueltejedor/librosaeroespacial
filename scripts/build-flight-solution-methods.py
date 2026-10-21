from pathlib import Path
import sys,json,math
import numpy as np
import sympy as sp
from scipy.integrate import quad,solve_ivp
from scipy.linalg import expm
ROOT=Path(__file__).resolve().parents[1];BOOK=ROOT/'books/mecanica-vuelo'
sys.path.insert(0,str(ROOT/'scripts'));from solution_steps import number,mathlines,numeric_steps
sys.path.insert(0,str(BOOK/'scripts'));import models
FOLDER=BOOK/'solutions/methods';FOLDER.mkdir(parents=True,exist_ok=True)
records=[]
def save(key,text,data=None):
 (FOLDER/(key+'.tex')).write_text(text+'\n');records.append(dict(key=key,calculations=data or []))
def calc(rows,values=None):return numeric_steps([dict(target=k,expression=e,unit=u,why=w) for k,e,u,w in rows],values)
def table(headers,rows):
 return '\n'.join([r'\begin{center}\begin{tabular}{'+'r'*len(headers)+'}',r'\toprule '+' & '.join(headers)+r'\\\midrule',*[ ' & '.join('$'+number(x)+'$' if isinstance(x,(float,int,np.floating)) else x for x in row)+r'\\' for row in rows],r'\bottomrule\end{tabular}\end{center}'])
def bisection(key,f,a,b,tex,unit='',tail=''):
 assert f(a)*f(b)<0;rows=[]
 for i in range(35):
  mid=(a+b)/2;v=f(mid)
  if i in [0,1,2,3,7,15,23,34]:rows.append([i+1,a,b,mid,v])
  if f(a)*v<=0:b=mid
  else:a=mid
 text=r'\textbf{Resolución numérica que puede reproducirse.} '+tex+r' Se elige un intervalo con cambio de signo. En cada paso $c=(a+b)/2$ y se conserva la mitad que mantiene signos opuestos. El ancho final acota el error en la raíz, bajo continuidad.'+'\n'+table(['Paso','$a$','$b$','$c$','$f(c)$'],rows)+'\n'+r'El resultado queda en $['+number(a,10)+','+number(b,10)+']'+r'\,'+unit+r'$. '+tail
 save(key,text,[dict(a=a,b=b,residual=f((a+b)/2))]);return (a+b)/2

def rotations(key,angles,vector):
 C=models.c_body_ned(*np.radians(angles));v=np.array(vector);result=C@v
 syms=r'C_{bn}=\begin{bmatrix}c_\theta c_\psi&c_\theta s_\psi&-s_\theta\\s_\phi s_\theta c_\psi-c_\phi s_\psi&s_\phi s_\theta s_\psi+c_\phi c_\psi&s_\phi c_\theta\\c_\phi s_\theta c_\psi+s_\phi s_\psi&c_\phi s_\theta s_\psi-s_\phi c_\psi&c_\phi c_\theta\end{bmatrix}'
 text=r'\textbf{Construcción de la matriz y producto por filas.} Se convierte cada ángulo a radianes y se escribe $c_\phi=\cos\phi$, $s_\phi=\sin\phi$, y análogamente para los otros ángulos. Multiplicar las rotaciones pasivas en orden 3--2--1 da:'+mathlines(syms)
 for j in range(3):
  line='+'.join('('+number(C[j,k],9)+')('+str(vector[k])+')' for k in range(3))
  text+=mathlines(['u','v','w'][j]+'='+line+r'\approx'+number(result[j])+r'\,\mathrm{m/s}')
 text+=r'La inversa es la transpuesta: multiplicar $C_{bn}^T$ por el vector obtenido recupera las tres componentes NED. Las normas coinciden: $V='+number(np.linalg.norm(v))+r'\,\mathrm{m/s}$. Para incidencia se usa $\alpha=\operatorname{atan2}(w,u)$; el argumento de $w/u$ por sí solo pierde el cuadrante.'
 save(key,text,[dict(matrix=C.tolist(),body=result.tolist(),back=(C.T@result).tolist())])
rotations('T02',[18,9,32],[96,8,-5]);rotations('S01.1',[12,6,25],[82,-4,-3])
def dynamics(key,Ixx,Iyy,Izz,Ixz,omega,M):
 I=np.array([[Ixx,0,-Ixz],[0,Iyy,0],[-Ixz,0,Izz]],float);o=np.array(omega);M=np.array(M);H=I@o;c=np.cross(o,H);rhs=M-c;a=np.linalg.solve(I,rhs);d=Ixx*Izz-Ixz**2
 text=r'\textbf{Momento angular, producto vectorial y sistema de ecuaciones.} Primero se calculan las tres filas de $\boldsymbol H=I\boldsymbol\omega$. Las entradas $xz$ y $zx$ son negativas con el convenio del enunciado.'
 text+=mathlines(r'\boldsymbol H='+sp.latex(sp.Matrix(H))+r'\,\mathrm{kg\,m^2/s}')
 for j in range(3):
  terms='+'.join('('+number(I[j,k])+')('+number(o[k])+')' for k in range(3) if I[j,k])
  text+=mathlines('H_{'+str(j+1)+'}='+terms+r'\approx'+number(H[j])+r'\,\mathrm{kg\,m^2/s}')
 for j,(k,l) in enumerate([(1,2),(2,0),(0,1)]):
  text+=mathlines('c_{'+str(j+1)+'}=('+number(o[k])+')('+number(H[l])+')-('+number(o[l])+')('+number(H[k])+r')\approx'+number(c[j])+r'\,\mathrm{N\,m}')

 text+=r'El producto giroscópico se desarrolla como $(qH_z-rH_y,\ rH_x-pH_z,\ pH_y-qH_x)$; su valor es:'
 text+=mathlines(r'\boldsymbol\omega\times\boldsymbol H='+sp.latex(sp.Matrix(c))+r'\,\mathrm{N\,m}')
 text+=r'Se resta de los momentos aplicados, obteniendo el segundo miembro $\boldsymbol b=\boldsymbol M-\boldsymbol\omega\times\boldsymbol H$.'
 text+=mathlines(r'\boldsymbol b='+sp.latex(sp.Matrix(rhs))+r'\,\mathrm{N\,m}')
 text+=r'La ecuación de $y$ queda desacoplada: $\dot q=b_y/I_{yy}$. Para $x,z$, eliminar la otra aceleración en el sistema $I_{xx}\dot p-I_{xz}\dot r=b_x$, $-I_{xz}\dot p+I_{zz}\dot r=b_z$ da:'
 text+=mathlines(r'\dot p=\frac{I_{zz}b_x+I_{xz}b_z}{I_{xx}I_{zz}-I_{xz}^2},\qquad\dot r=\frac{I_{xz}b_x+I_{xx}b_z}{I_{xx}I_{zz}-I_{xz}^2}')
 text+=mathlines(r'(\dot p,\dot q,\dot r)='+sp.latex(sp.Matrix(a).T)+r'\,\mathrm{s^{-2}}')
 text+=r'Para comprobar, multiplicar el vector de aceleraciones por $I$ y sumar el término giroscópico recupera $\boldsymbol M$. El trabajo giroscópico se anula por perpendicularidad; la tasa de energía es $\boldsymbol\omega\cdot\boldsymbol M='+number(o@M)+r'\,\mathrm W$.'
 save(key,text,[dict(H=H.tolist(),cross=c.tolist(),rhs=rhs.tolist(),determinant=d,acceleration=a.tolist(),residual=(I@a+c-M).tolist())])
dynamics('T05',9800,14800,19200,760,[.13,.05,-.09],[600,-380,420]);dynamics('S05.1',11000,16500,21000,850,[.10,.06,-.08],[700,-450,380])
dynamics('manual-c05',8500,13000,17000,620,[.12,-.08,.15],[950,-500,340])
# The trim's moment equation eliminates elevator; tangential force eliminates T.
m,rho,S,V=2450,1.04,26,66;W=m*models.G;qS=.5*rho*V*V*S
def trim(a):
 de=(.045-.72*a)/1.08;CL=.24+5.2*a+.28*de;D=qS*(.026+.046*CL*CL)
 return qS*CL+D*math.tan(a)-W
bisection('T06',trim,0,.2,r'La ecuación de momento se despeja como $\delta=(0.045-0.72\alpha)/1.08$. El equilibrio tangencial da $T=D/\cos\alpha$. Sustituir ambos en el vertical reduce tres incógnitas a una: $f(\alpha)=qSC_L(\alpha)+D(\alpha)\tan\alpha-mg_0=0$, con $qS='+number(qS)+r'\,\mathrm N$, $C_L=0.24+5.2\alpha+0.28\delta$ y $D=qS(0.026+0.046C_L^2)$.',r'\mathrm{rad}',r'Después se recuperan $\delta$ y $T$ con las dos relaciones despejadas, se comprueban sus límites y se sustituyen en los tres residuos. No se impone $L=W$ porque el empuje tiene componente vertical.')
# Exact glide rates and one-dimensional optimizations.
polar=models.Polar(16.2,.014,.032,1.55);mass=455;rho=1.05
f=lambda cl:4*polar.k*cl**2-2*polar.k*polar.cd(cl)**2-3*polar.cd(cl)
bisection('T08',f,.3,1.55,r'El descenso exacto es $s=\sqrt{2W/(\rho S)}C_D(C_L^2+C_D^2)^{-3/4}$. Derivar su logaritmo y usar $C_D\prime=2kC_L$ lleva a $4kC_L^2-2kC_D^2-3C_D=0$. Se busca esa raíz; además se comparan los valores de descenso en ambos extremos del intervalo.','',r'Una raíz de derivada no basta por sí sola: el signo cambia de negativo a positivo para el descenso y el mínimo queda por debajo de los extremos. La fórmula tendida $\sqrt{3C_{D0}/k}$ omite términos de $C_D^2$.')
polar=models.Polar(16.8,.013,.030,1.6)
def G(cl):
 z=models.glide_exact(polar,460,1.02,cl);return (z['horizontal']-10)/z['sink']
def dg(cl):return (G(cl+1e-5)-G(cl-1e-5))/(2e-5)
opt=bisection('P36',dg,.2,1.6,r'Para cada $C_L$ se calcula $C_D=0.013+0.030C_L^2$, $\delta=\arctan(C_D/C_L)$, $V=\sqrt{2mg_0\cos\delta/(\rho SC_L)}$, $s=V\sin\delta$ y $G=(V\cos\delta-10)/s$. Se busca un cero de la derivada de $G$, aproximada aquí por diferencia centrada con incremento $10^{-5}$; esa aproximación de derivada se refina al contrastar el resultado.','',r'Comparar también $G(0.2)$ y $G(1.6)$. El máximo en calma usa $C_L=\sqrt{0.013/0.030}$ y no maximiza necesariamente el avance terrestre con viento.')
with (FOLDER/'P36.tex').open('a') as f:f.write(table(['$C_L$','$G$'],[[.2,G(.2)],[opt,G(opt)],[1.6,G(1.6)]]))
# Altitude inversion includes the layer boundary explicitly.
Dmin=2*6200*models.G*math.sqrt(.023*.043);rhotarget=1.225*(Dmin/18000)**(1/.8)
bisection('P19',lambda h:models.isa(h)[2]-rhotarget,11000,20000,r'Calcular $W=6200g_0$. La mínima resistencia es $D_{min}=2W\sqrt{0.023\cdot0.043}$. Su valor es $D_{min}='+number(Dmin)+r'\,\mathrm N$. La ley de empuje da $\sigma=(D_{min}/18000)^{1/0.8}$ y $\rho_{obj}='+number(rhotarget)+r'\,\mathrm{kg/m^3}$. Evaluar densidad en 11 km identifica la capa isoterma; allí $T=216.65$ K y $\rho(h)=\rho_{11}\exp[-g_0(h-11000)/(RT)]$. Se resuelve $f(h)=\rho(h)-\rho_{obj}=0$.',r'\mathrm m',r'En esta capa también se puede despejar directamente $h=11000-(RT/g_0)\ln(\rho_{obj}/\rho_{11})$. Sustituir esa altura en la ley de empuje debe recuperar $D_{min}$.')
# Closed-form glide time in a lapse-rate layer, plus intermediate nodes.
def glide(key,m,S,cd,k,hi,hf,wind,cl=None,bank=None):
 p=models.Polar(S,cd,k);cl=cl or p.cl_ld();CD=p.cd(cl);delta=math.atan(CD/cl);nexp=models.G/(models.R*.0065)-1;z=nexp/2
 K=math.sqrt(2*m*models.G*math.cos(delta)/(S*cl))*math.sin(delta)
 pref=math.sqrt(1.225)*288.15/(.0065*K*(z+1))
 E=pref*((1-.0065*hf/288.15)**(z+1)-(1-.0065*hi/288.15)**(z+1))
 result=models.glide_integral(p,m,hi,hf,cl,wind)
 assert math.isclose(E,result['time'],rel_tol=2e-7),(key,E,result)
 text=r'\textbf{Integral de tiempo desarrollada.} Calcular $C_D=C_{D0}+kC_L^2$ y $\delta=\arctan(C_D/C_L)$. Del equilibrio exacto, $V(h)=\sqrt{2mg_0\cos\delta/[\rho(h)SC_L]}$ y $s(h)=V(h)\sin\delta$. Definir $K=\sqrt{2mg_0\cos\delta/(SC_L)}\sin\delta$ da $s=K/\sqrt\rho$. En la troposfera, $\rho=\rho_0(1-\beta h/T_0)^a$, con $a=g_0/(R\beta)-1$.'
 text+=mathlines(r'E=\frac{\sqrt{\rho_0}}{K}\int_{h_f}^{h_i}(1-\beta h/T_0)^{a/2}dh=\frac{\sqrt{\rho_0}T_0}{K\beta(1+a/2)}\left[(1-\beta h_f/T_0)^{1+a/2}-(1-\beta h_i/T_0)^{1+a/2}\right]')
 text+=r'Los parámetros intermedios son $C_L='+number(cl)+r'$, $C_D='+number(CD)+r'$, $\delta='+number(delta)+r'\,\mathrm{rad}$ y $a='+number(nexp)+r'$. La evaluación por alturas permite contrastar el integrando:'
 rows=[]
 for h in np.linspace(hf,hi,5):
  T,pr,rho,asound=models.isa(float(h));g=models.glide_exact(p,m,rho,cl);rows.append([float(h),rho,g['V'],g['sink'],1/g['sink']])
 text+=table(['$h$ (m)','$\rho$','$V$ (m/s)','$s$ (m/s)','$1/s$ (s/m)'],rows)
 text+=mathlines(r'E\approx'+number(E)+r'\,\mathrm s,\qquad R_a=(h_i-h_f)\frac{C_L}{C_D}\approx'+number(result['air_range'])+r'\,\mathrm m')
 text+=mathlines(r'R_g=R_a+U E\approx'+number(result['ground_range'])+r'\,\mathrm m')
 if bank is not None:
  factor=math.cos(math.radians(bank))**1.5
  text+=r'En el modelo helicoidal tendido del enunciado, $n=1/\cos\phi$ y $E_n/E_1=n^{-3/2}='+number(factor)+r'$. Por tanto $E_n='+number(E*factor)+r'\,\mathrm s$. Este escalado añade la aproximación de viraje tendido al cálculo recto anterior.'
 save(key,text,[dict(CL=cl,CD=CD,delta=delta,time=E,range_air=result['air_range'],range_ground=result['ground_range'])])
glide('T09',455,16.2,.014,.032,3100,350,9)
glide('S01.2',490,17.6,.0132,.0305,3400,600,-6)
glide('P35',475,17.1,.014,.032,2800,500,0,math.sqrt(3*.014/.032),28)
# Analytic state transition for the particular two-state matrix.
A=np.array([[-.7,1],[-3.8,-1.1]]);B=A+.9*np.eye(2);wd=math.sqrt(3.76);x=math.exp(-.9*12)*(np.eye(2)*math.cos(wd*12)+B*math.sin(wd*12)/wd)@np.array([.04,0])
text=r'\textbf{Exponencial desarrollada para esta matriz.} El polinomio característico es $\lambda^2+1.8\lambda+4.57=0$, de donde $\lambda=-0.9\pm i\sqrt{3.76}$. Escribir $A=-0.9I+B$ da $B=\bigl(\begin{smallmatrix}0.2&1\\-3.8&-0.2\end{smallmatrix}\bigr)$ y verificar por multiplicación $B^2=-3.76I$. Agrupar términos pares e impares de la serie exponencial produce:'
text+=mathlines(r'e^{At}=e^{-0.9t}\left[I\cos(\sqrt{3.76}t)+\frac{B}{\sqrt{3.76}}\sin(\sqrt{3.76}t)\right]')
text+=mathlines(r'\alpha(t)=0.04e^{-0.9t}\left[\cos(\sqrt{3.76}t)+\frac{0.2}{\sqrt{3.76}}\sin(\sqrt{3.76}t)\right]')
text+=mathlines(r'q(t)=-\frac{0.152}{\sqrt{3.76}}e^{-0.9t}\sin(\sqrt{3.76}t)')
text+=r'Sustituir $t=12$ s da $\alpha='+number(x[0])+r'\,\mathrm{rad}$ y $q='+number(x[1])+r'\,\mathrm{s^{-1}}$. Para contrastar con integración, se usa el mismo estado inicial y se controla cada componente por separado; una diferencia entre algoritmos no es validación experimental.'
save('T21',text,[dict(state=x.tolist())])
(BOOK/'evidence/solution-method-calculations.json').write_text(json.dumps(records,ensure_ascii=False,indent=2)+'\n')
print(len(records),'method-specific derivations and traces')
# Ground roll: show the integrand, intermediate forces and convergence.
def ground(key,m,S,rho,T,mu,cl,cd0,k,vgf,wind=0,brake=False,delay=0):
 CD=cd0+k*cl*cl;g=models.G
 a0=(mu*g if brake else T/m-mu*g)
 a2=rho*S*(CD-mu*cl)/(2*m) if brake else rho*S*(mu*cl-CD)/(2*m)
 def acc(v):return a0+a2*(v+wind)**2
 def simpson(n,mode):
  dx=vgf/n
  def f(v):return (v if mode=='s' else 1)/acc(v)
  return dx/3*(f(0)+f(vgf)+sum((4 if i%2 else 2)*f(i*dx) for i in range(1,n)))
 rows=[]
 for v in np.linspace(0,vgf,5):
  va=v+wind;q=.5*rho*va*va;L=q*S*cl;D=q*S*CD;N=m*g-L
  assert N>=0 and acc(v)>0
  rows.append([float(v),va,D,mu*N,acc(v)])
 method=r'b(V_g)' if brake else r'a(V_g)'
 text=r'\textbf{De fuerzas a aceleración y a distancia.} Se calcula primero $C_D=C_{D0}+kC_L^2='+number(CD)+r'$. Para cada velocidad terrestre, $V_a=V_g+U$, $q=\rho V_a^2/2$, $L=qSC_L$ y $N=mg_0-L$; la fuerza de rueda utiliza esa reacción normal, no todo el peso.'
 text+=r' En frenado se define $b=-\dot V_g>0$ y $b=[D+\mu_bN]/m$.' if brake else r' El balance horizontal es $ma=T-D-\mu_rN$.'
 text+=mathlines(method+'='+number(a0,10)+'+('+number(a2,10)+r')(V_g+'+number(wind)+r')^2\quad[\mathrm{m/s^2}]')
 text+=table(['$V_g$','$V_a$','$D$ (N)',r'$\mu N$ (N)','$'+method+'$'],rows)
 text+=r'Como $ds/dt=V_g$ y $dV_g/dt$ es la aceleración con signo, se cambia la variable de integración. Con aceleración o desaceleración positiva en los límites elegidos:'
 text+=mathlines(r's=\int_0^{V_{g,f}}\frac{V_g}{'+method+r'}dV_g,\qquad t=\int_0^{V_{g,f}}\frac{1}{'+method+r'}dV_g')
 text+=r'Para reproducir el cálculo a mano o con una hoja, Simpson compuesto usa un número par $n$ de intervalos, $h=V_{g,f}/n$ y $I\simeq(h/3)[f_0+f_n+4\sum_{i\ impar}f_i+2\sum_{i\ par,\ interior}f_i]$. Se aplica una vez con $f=V_g/'+method+r'$ y otra con $f=1/'+method+r'$. El refinamiento da:'
 convergence=[[n,simpson(n,'s'),simpson(n,'t')] for n in [4,8,16,32,64]]
 text+=table(['$n$','$s$ (m)','$t$ (s)'],convergence)
 if wind==0 and a2!=0:
  exact=math.log((a0+a2*vgf**2)/a0)/(2*a2)
  text+=mathlines(r's=\frac{1}{2a_2}\ln\!\left(\frac{a_0+a_2V_f^2}{a_0}\right)\approx'+number(exact)+r'\,\mathrm m')
  text+=r'La primitiva sale de sustituir $u=a_0+a_2V^2$, $du=2a_2VdV$. Si $a_2\to0$, el límite es $V_f^2/(2a_0)$.'
 if delay:text+=r'La fase de demora se añade después: $s_d=28(1.2)=33.6$ m; el total terrestre es $s_b+s_d='+number(simpson(64,'s')+delay)+r'\,\mathrm m$.'
 save(key,text,[dict(a0=a0,a2=a2,samples=rows,convergence=convergence)])
ground('P25',1620,19,1.225,5200,.028,.62,.034,.052,34)
ground('P26',1620,19,1.225,0,.32,.18,.034,.052,31,brake=True)
ground('T17',1680,20.2,1.2,5400,.03,.63,.034,.051,29,5)
# Add the calm comparison to the same solution with its own final speed.
ground('T17-calm',1680,20.2,1.2,5400,.03,.63,.034,.051,34)
with (FOLDER/'T17.tex').open('a') as f:f.write('\n'+r'\textbf{Contraste en calma.}\input{solutions/methods/T17-calm.tex}'+'\n')
ground('T18',1680,20.2,1.2,0,.31,.17,.034,.051,30,brake=True)
ground('S04.1',1720,20,1.17,5500,.03,.60,.033,.050,32,5)
ground('S04.2',1720,20,1.17,0,.29,.16,.033,.050,29,brake=True,delay=33.6)
# Scalar bookkeeping previously represented only by literals.
for key,vals in [('P27',(5.2,4,.21,.94,.32,.25,3.4,.08,.38)),('T19',(5,4.3,.20,.93,.33,.25,3.3,.09,None))]:
 aw,at,sr,eta,eps,hac,ht,cf,h=vals
 rows=[('Kt',f'{eta}*{sr}*{at}*(1-{eps})','','La pendiente efectiva de cola incluye área, presión dinámica relativa y estela.'),('atot',f'{aw}+Kt','','Sumar las contribuciones a la sustentación total.'),('hn',f'({aw}*{hac}+Kt*{ht}-{cf})/atot','','Imponer pendiente de momento nula y despejar la posición de CG.')]
 rows += [('SM',f'hn-{h}','','Restar el CG al punto neutro.'),('Cm','-atot*SM','1/rad','Comprobar signo de la pendiente restauradora.')] if h is not None else [('hmax','hn-.08','','Restar el margen mínimo exigido al punto neutro.'),('Cm','-atot*.08','1/rad','Comprobar la pendiente en el límite de CG.')]
 body,checks=calc(rows)
 save(key,r'\textbf{Despeje del punto neutro.} La pendiente directa es $C_{m\alpha}=a_w(h-h_{ac})-K_t(h_t-h)+C_{m\alpha,f}$. Agrupar términos en $h$ deja $(a_w+K_t)h-a_wh_{ac}-K_th_t+C_{m\alpha,f}$. Igualar a cero produce la expresión de $h_n$; conservar $K_t$ en el denominador es necesario porque la cola también sustenta.'+body,checks)
# Airspeed calibration from the actual atmospheric state.
T,p,rho,a=models.isa(6000);T0,p0,rho0,a0=models.isa(0)
body,checks=calc([('Ma','170/a','','Dividir TAS por sonido local.'),('EAS','170*sqrt(rho/rho0)','m/s','Igualar presión dinámica a la referencia de densidad.'),('qc','p*((1+.2*Ma**2)**3.5-1)','Pa','Calcular presión de impacto isentrópica, diferente de presión dinámica.'),('CAS','a0*sqrt(5*((1+qc/p0)**(2/7)-1))','m/s','Invertir la calibración isentrópica de nivel del mar.')],dict(a=a,rho=rho,rho0=1.225,p=p,p0=101325,a0=a0))
save('P38',r'\textbf{Estado, presión de impacto y calibración.} En 6000 m ISA, $T='+number(T)+r'\,\mathrm K$, $p='+number(p)+r'\,\mathrm{Pa}$, $\rho='+number(rho)+r'\,\mathrm{kg/m^3}$ y $a=\sqrt{1.4RT}='+number(a)+r'\,\mathrm{m/s}$. Para el sonido de referencia se usa $a_0=\sqrt{1.4R(288.15)}='+number(a0)+r'\,\mathrm{m/s}$. La relación $1+q_c/p=(1+0.2M^2)^{3.5}$ se despeja con potencia $2/7$, resta uno y raíz positiva.'+body,checks)
# Trace the experiment's differences using recorded endpoints, not new data.
xr=json.loads((BOOK/'reports/xml-run.json').read_text());z=xr['final'];a=xr['initial'];rows=[]
for label,e,u,why in [('dh',f'{z["h_m"]}-{a["h_m"]}','m','Restar altura inicial a final de la misma columna.'),('dV',f'{z["TAS_m_s"]}-{a["TAS_m_s"]}','m/s','Restar velocidades verdaderas de la misma columna.'),('fuel',f'{a["fuel_kg"]}-{z["fuel_kg"]}','kg','Consumo positivo: masa de combustible inicial menos final.')]:rows.append((label,e,u,why))
body,checks=calc(rows);save('T22',r'\textbf{Lectura y resta de estados.} Estos son los extremos conservados en el registro de la ejecución original. Las restas comprueban la lectura; no se ha vuelto a ejecutar aquí el simulador ni se atribuye al modelo fidelidad experimental.'+body,checks)
cv=json.loads((BOOK/'reports/jsbsim-results.json').read_text())['convergence'];v=[c['TAS_m_s'] for c in cv]
body,checks=calc([('d1',f'abs({v[0]}-{v[1]})','m/s','Diferencia entre los dos primeros pasos temporales.'),('d2',f'abs({v[1]}-{v[2]})','m/s','Diferencia entre los dos pasos menores.'),('pobs','log(d1/d2)/log(2)','','Calcular el indicador de orden solo tras comprobar diferencias no nulas.')]);save('T23',r'\textbf{Refinamiento del caso registrado.} Se comparan las mismas columnas TAS al mismo tiempo final. Conservar sus cifras antes de restar evita que el redondeo domine las diferencias. El cociente de diferencias no demuestra un orden universal del simulador.'+body,checks)
# Compare a fixed-TAS jet integral with the mistaken fixed-efficiency law.
pol=models.Polar(38,.022,.046);rho=models.isa(6000)[2];cl=pol.cl_ld();V=pol.speed(7000,rho,cl)
rows=[('CLi','sqrt(.022/.046)','','Obtener CL inicial de mínima resistencia.'),('V',f'sqrt(2*7000*9.80665/({rho}*38*CLi))','m/s','Fijar la TAS inicial que se mantendrá durante toda la fase.'),('A',f'.5*{rho}*V**2*38*.022','N','Coeficiente constante de resistencia a esa TAS.'),('B',f'2*.046/({rho}*V**2*38)','1/N','Coeficiente que multiplica al peso al cuadrado.'),('Eexact','(atan(7000*9.80665*sqrt(B/A))-atan(5700*9.80665*sqrt(B/A)))/(9.80665*1.7e-5*sqrt(A*B))','s','Evaluar la primitiva arcotangente entre peso final e inicial.'),('LD','CLi/(.022+.046*CLi**2)','','Obtener eficiencia inicial para la aproximación distinta.'),('Eapprox','LD/(9.80665*1.7e-5)*log(7000/5700)','s','Evaluar la hipótesis artificial de eficiencia fija por separado.'),('error','Eapprox/Eexact-1','','Comparar los dos tiempos.')]
body,checks=calc(rows);save('P37',r'\textbf{Por qué aparece una arcotangente.} Con TAS constante, $D=A+BW^2$ y $dW/dt=-g_0c_TD$. Separar da $dt=-dW/[g_0c_T(A+BW^2)]$. La sustitución $u=W\sqrt{B/A}$ convierte la integral en $du/(1+u^2)$, cuya primitiva es $\arctan u$. No se conserva la eficiencia al consumir masa.'+body,checks)
# Print all numerical state traces generated in this pass.
(BOOK/'evidence/solution-method-calculations.json').write_text(json.dumps(records,ensure_ascii=False,indent=2)+'\n')
print(len(records),'method-specific derivations and traces total')
# Simple scalar stages formerly reduced to a literal in the printed solutions.
def scalar_method(key,text,rows,values=None):
 body,checks=calc(rows,values);save(key,r'\textbf{Desarrollo de las magnitudes intermedias.} '+text+body,checks)
scalar_method('T04',r'Con TAS y densidad fijas, $qS$ permanece constante. El peso cambia y obliga a cambiar $C_L=W/(qS)$. Por tanto el término parásito permanece fijo y el término cuadrático disminuye como el cuadrado de la masa.',[
('qS','.5*.92*98**2*29','N','Calcular la fuerza de referencia constante.'),('CLi','5100*9.80665/qS','','Equilibrio con masa inicial.'),('CLf','4590*9.80665/qS','','Equilibrio con masa final.'),('Di','qS*(.024+.047*CLi**2)','N','Resistencia inicial de la polar.'),('Df','qS*(.024+.047*CLf**2)','N','Resistencia final.'),('reduction','1-Df/Di','','Comparar fuerzas completas, no solo el término cuadrático.')])
scalar_method('T07',r'De $D=W\sin\delta$ y $L=W\cos\delta$, dividir da $\tan\delta=C_D/C_L$. La sustentación exacta usa el coseno; el descenso usa el seno. La aproximación tendida sustituye ambos factores por sus límites de ángulo pequeño.',[
('CD','.014+.032*.78**2','','Calcular la polar al CL impuesto.'),('delta','atan(CD/.78)','rad','Obtener ángulo de descenso positivo.'),('Vexact','sqrt(2*455*9.80665*cos(delta)/(1.05*16.2*.78))','m/s','Conservar coseno en el equilibrio normal.'),('sexact','Vexact*sin(delta)','m/s','Proyectar la velocidad sobre la vertical.'),('Vapprox','sqrt(2*455*9.80665/(1.05*16.2*.78))','m/s','Aplicar solo en esta ruta el equilibrio aproximado L=W.'),('sapprox','Vapprox*CD/.78','m/s','Sustituir seno por tangente en la aproximación.'),('relative','sapprox/sexact-1','','Cuantificar el error en descenso.')])
scalar_method('P39',r'La fórmula cuadrática para $\lambda^2-0.24\lambda+2.25=0$ da parte real $0.24/2$ y parte imaginaria $\sqrt{2.25-(0.24/2)^2}$. La envolvente es $e^{0.12t}$, de modo que duplicarla exige $0.12t=\ln2$.',[
('realpart','.24/2','1/s','El signo de la parte real es positivo.'),('wd','sqrt(2.25-(.24/2)**2)','1/s','Separar la oscilación de su envolvente creciente.'),('t2','log(2)/(.24/2)','s','Despejar el tiempo de duplicación.')])
# Jet mission integrals: derive the coefficient hidden by the name K_m.
JET=r'De $dm/dt=-c_TD=-c_Tmg_0/(L/D)$, separar variables da $E=(L/D)\ln(m_i/m_f)/(g_0c_T)$. Con CL fijo, $V=\sqrt{2g_0m/(\rho SC_L)}$; sustituir en $dx=Vdt$ deja integrar $m^{-1/2}$, cuya primitiva es $2\sqrt m$. Por eso $R=K_m(\sqrt{m_i}-\sqrt{m_f})$, con $K_m=2(L/D)\sqrt{2g_0/(\rho SC_L)}/(g_0c_T)$.'
rho7=models.isa(7000)[2]
scalar_method('T12',JET+r' Para reactor a CL constante, máximo alcance se obtiene maximizando $\sqrt{C_L}/C_D$, que da $C_L=\sqrt{C_{D0}/(3k)}$. Despejar la masa inicial requiere primero $\sqrt{m_i}=\sqrt{m_f}+R/K_m$ y después elevar al cuadrado.',[
('CL','sqrt(.024/(3*.044))','','Elegir el óptimo de alcance de reactor.'),('CD','.024+.044*CL**2','','Evaluar resistencia adimensional.'),('LD','CL/CD','','Obtener eficiencia de esa condición.'),('Km',f'2*LD/(9.80665*1.7e-5)*sqrt(2*9.80665/({rho7}*42*CL))','m/kg**.5','Calcular el coeficiente completo de la integral.'),('mi','(sqrt(6500)+1400000/Km)**2','kg','Cerrar el alcance prescrito antes de estimar combustible.'),('fuel','mi-6500','kg','Restar masa final que ya incluye reserva.'),('Vi',f'sqrt(2*mi*9.80665/({rho7}*42*CL))','m/s','Comprobar velocidad inicial.'),('Vf',f'sqrt(2*6500*9.80665/({rho7}*42*CL))','m/s','Comprobar velocidad final.')])
rho65=models.isa(6500)[2];CL=math.sqrt(.024/.044);LD=CL/(.024+.044*CL**2);mA=11400*math.exp(-models.G*1.68e-5*2700/LD)
scalar_method('S02.1',JET+r' Aquí se fija duración y se invierte la integral de tiempo: $m_f=m_i\exp[-g_0c_TE/(L/D)]$. Para autonomía de reactor se maximiza $L/D$ y se usa $C_L=\sqrt{C_{D0}/k}$.',[
('CL','sqrt(.024/.044)','','Óptimo de autonomía del reactor.'),('LD','CL/(.024+.044*CL**2)','','Eficiencia correspondiente.'),('mf','11400*exp(-9.80665*1.68e-5*2700/LD)','kg','Invertir el logaritmo de la ley temporal.'),('Km',f'2*LD/(9.80665*1.68e-5)*sqrt(2*9.80665/({rho65}*52*CL))','m/kg**.5','Evaluar el coeficiente de distancia.'),('R','Km*(sqrt(11400)-sqrt(mf))','m','Integrar la velocidad que disminuye con la masa.'),('Vi',f'sqrt(2*11400*9.80665/({rho65}*52*CL))','m/s','Velocidad inicial.'),('Vf',f'sqrt(2*mf*9.80665/({rho65}*52*CL))','m/s','Velocidad final.')])
scalar_method('S02.2',r'Al cambiar a TAS fija, la resistencia pasa a $D=A+BW^2$, con $A=qSC_{D0}$ y $B=k/(qS)$. Separar la ecuación de consumo y sustituir $u=W\sqrt{B/A}$ produce la primitiva arcotangente; la masa de enlace es la calculada en la fase anterior.',[
('A',f'.5*{rho65}*175**2*52*.024','N','Término parásito a TAS fija.'),('B',f'2*.044/({rho65}*175**2*52)','1/N','Coeficiente del peso al cuadrado.'),('E',f'(atan({mA}*9.80665*sqrt(B/A))-atan(9300*9.80665*sqrt(B/A)))/(9.80665*1.68e-5*sqrt(A*B))','s','Evaluar la diferencia de primitivas.'),('R','175*E','m','En esta fase sí es válida distancia igual a TAS constante por tiempo.'),('fuel',f'{mA}-9300','kg','Cerrar consumo de la segunda fase.')])
scalar_method('S02.3',r'La factibilidad por sustentación se contrasta con $C_{L,max}$; la de motor compara la resistencia de ese mismo estado con el empuje disponible. Ninguna de las dos verifica por sí sola el trim de momentos.',[
('qS',f'.5*{rho65}*175**2*52','N','Fuerza de referencia de la fase a TAS fija.'),('CL',f'{mA}*9.80665/qS','','Sustentación requerida por la masa de enlace.'),('D','qS*(.024+.044*CL**2)','N','Resistencia y empuje requerido.'),('margin','10500-D','N','Margen local de empuje disponible.')])
PROP=r'Para hélice, $P_e=DV/\eta_p=mg_0V/[\eta_p(L/D)]$ y $dm/dt=-c_PP_e$. Introducir $V=\sqrt{2g_0m/(\rho SC_L)}$ deja $dt=-(\eta_p L/D)/(g_0c_P)\sqrt{\rho SC_L/(2g_0)}m^{-3/2}dm$. Integrar usa la primitiva $-2m^{-1/2}$ para tiempo; en distancia, $dx=Vdt$ deja $dm/m$ y un logaritmo.'
def prop_rows(mi,mf,rho,S,cd0,k,eta,cp,clname,expr):
 return [(clname,expr,'','Elegir el CL según el objetivo de la ley.'),(clname+'CD',f'{cd0}+{k}*{clname}**2','','Evaluar la polar.'),(clname+'LD',f'{clname}/{clname}CD','','Calcular eficiencia.'),(clname+'R',f'{eta}*{clname}LD/(9.80665*{cp})*log({mi}/{mf})','m','Evaluar la integral de distancia.'),(clname+'E',f'2*{eta}*{clname}LD/(9.80665*{cp})*sqrt({rho}*{S}*{clname}/(2*9.80665))*(1/sqrt({mf})-1/sqrt({mi}))','s','Evaluar la integral de tiempo con ambas masas.')]
scalar_method('T16',PROP+r' El consumo se convierte: $c_P=0.295/(3.6\times10^6)$ kg/J. Se comparan $C_{L,R}=\sqrt{C_{D0}/k}$ y $C_{L,E}=\sqrt{3C_{D0}/k}$ bajo las mismas masas y altitud.',prop_rows(1850,1510,models.isa(2000)[2],19.4,.026,.047,.8,.295/3.6e6,'CLR','sqrt(.026/.047)')+prop_rows(1850,1510,models.isa(2000)[2],19.4,.026,.047,.8,.295/3.6e6,'CLE','sqrt(3*.026/.047)'))
scalar_method('S03.2',PROP+r' La fase previa consume $0.30(230)(7/60)=8.05$ kg, por lo que comienza con $2171.95$ kg. La masa final suma masa seca y reserva: $1760+60=1820$ kg. La reserva no se quema en esta fase.',prop_rows(2171.95,1820,models.isa(2200)[2],21.4,.028,.049,.78,.30/3.6e6,'CL','sqrt(.028/.049)'))
scalar_method('S03.3',r'Con la aproximación indicada $L\simeq W$, obtener primero CL y resistencia de la polar. La potencia útil disponible es rendimiento por potencia al eje; solo su exceso respecto a $DV$ puede transformarse en altura.',[
('qS','.5*1.02*59**2*21.4','N','Formar fuerza de referencia.'),('CL','2100*9.80665/qS','','Imponer sustentación aproximada igual a peso.'),('D','qS*(.028+.049*CL**2)','N','Calcular resistencia.'),('Pn','D*59','W','Potencia aerodinámica necesaria.'),('Pd','.78*230000','W','Convertir potencia al eje en potencia útil.'),('ROC','(Pd-Pn)/(2100*9.80665)','m/s','El exceso de potencia se divide por peso, no por masa.')])
scalar_method('S04.3',r'El punto neutro se obtiene de $0=a_w(h_n-h_{ac})-K_t(h_t-h_n)+C_{m\alpha,f}$. Agrupar $h_n$ da el denominador $a_w+K_t$; después se calcula el margen y la pendiente estática.',[
('Kt','.9*.18*4.2*(1-.35)','','Pendiente efectiva de la cola.'),('hn','(5.1*.25+Kt*3.1-.06)/(5.1+Kt)','','Resolver el equilibrio de pendiente nula.'),('SM','hn-.35','','Distancia del CG al punto neutro.'),('Cm','-(5.1+Kt)*SM','1/rad','Comprobar tendencia restauradora; la estabilidad dinámica requiere además amortiguamiento y autovalores.')])
# Explicit limits for the horizontal envelope.
rho=models.isa(7000)[2];a=models.isa(7000)[3]
scalar_method('T11',r'Con $D=AV^2+B/V^2$, imponer $D=T$ y multiplicar por $V^2$ produce una cuadrática en $y=V^2$: $Ay^2-Ty+B=0$. Una raíz existe si $T^2-4AB\ge0$. La raíz baja se calcula como $V_-^2=2B/[T+\sqrt{T^2-4AB}]$ para evitar restar dos números próximos. Después se intersecta el intervalo de motor con pérdida y Mach.',[
('A',f'.5*{rho}*42*.024','kg/m','Coeficiente que multiplica V al cuadrado.'),('B',f'2*.044*(7600*9.80665)**2/({rho}*42)','N*m**2/s**2','Coeficiente del término inverso.'),('disc','10000**2-4*A*B','N**2','Comprobar discriminante no negativo.'),('Vlo','sqrt(2*B/(10000+sqrt(disc)))','m/s','Raíz baja estable.'),('Vhi','sqrt((10000+sqrt(disc))/(2*A))','m/s','Raíz alta.'),('Vstall',f'sqrt(2*7600*9.80665/({rho}*42*1.5))','m/s','Límite de sustentación.'),('VMach',f'.62*{a}','m/s','Límite por velocidad del sonido local.')])
with (FOLDER/'T11.tex').open('a') as f:f.write(r'\par El límite inferior es el mayor entre raíz baja y pérdida; el superior, el menor entre raíz alta y límite de Mach. Comparar ambos extremos determina si la intersección está vacía.'+'\n')
(BOOK/'evidence/solution-method-calculations.json').write_text(json.dumps(records,ensure_ascii=False,indent=2)+'\n')
print(len(records),'method-specific derivations and traces total')
# Integrating coupled mass and time: a reproducible hand calculation step.
pol=models.Polar(31,.025,.047);V=90;ct=1.8e-5
def climb(h,y):
 m=y[0];rho=models.isa(h)[2];T=9500*(rho/1.225)**.8;D=pol.drag(V,m,rho);c=(T-D)*V/(m*models.G)
 assert c>0
 return np.array([-ct*T/c,1/c,V/c])
def rk4(dh):
 h=1200.;y=np.array([5300.,0.,0.]);trace=[(h,*y)];first=[]
 while h<4200-1e-9:
  k1=climb(h,y);k2=climb(h+dh/2,y+dh*k1/2);k3=climb(h+dh/2,y+dh*k2/2);k4=climb(h+dh,y+dh*k3)
  if not first:first=[k1.tolist(),k2.tolist(),k3.tolist(),k4.tolist()]
  y=y+dh*(k1+2*k2+2*k3+k4)/6;h+=dh;trace.append((h,*y))
 return y,trace,first
convergence=[]
for dh in [250,125,62.5]:
 y,trace,first=rk4(dh);convergence.append([dh,*y])
y,trace,first=rk4(125)
text=r'\textbf{Integración de masa, tiempo y avance, sin congelar el peso.} Se toma altura como variable independiente porque el ascenso es monótono. En cada etapa, obtener $\rho(h)$, $T(h)=9500[\rho(h)/1.225]^{0.8}$, $qS=\rho(h)V^2S/2$, $C_L=mg_0/(qS)$, $D=qS(0.025+0.047C_L^2)$ y $c=(T-D)V/(mg_0)$. Comprobar $c>0$ antes de dividir.'
text+=mathlines(r'\frac{d}{dh}\begin{pmatrix}m\\t\\x\end{pmatrix}=\boldsymbol f(h,\boldsymbol y)=\begin{pmatrix}-c_TT/c\\1/c\\V/c\end{pmatrix},\qquad\boldsymbol y(1200)=\begin{pmatrix}5300\\0\\0\end{pmatrix}')
text+=r'Un paso de Runge--Kutta de cuarto orden de altura $\Delta h$ usa $k_1=f(h,y)$, $k_2=f(h+\Delta h/2,y+\Delta hk_1/2)$, $k_3=f(h+\Delta h/2,y+\Delta hk_2/2)$ y $k_4=f(h+\Delta h,y+\Delta hk_3)$. La actualización es $y_{nuevo}=y+\Delta h(k_1+2k_2+2k_3+k_4)/6$. Para el primer paso de 125 m, las tres componentes de cada pendiente son:'
text+=table(['Etapa','$dm/dh$','$dt/dh$','$dx/dh$'],[[i+1,*k] for i,k in enumerate(first)])
text+=r'Aplicar la suma ponderada produce el primer estado y repetirla da la evolución siguiente:'
text+=table(['$h$ (m)','$m$ (kg)','$t$ (s)','$x$ (m)'],[trace[i] for i in [0,1,6,12,18,24]])
text+=r'La comprobación de refinamiento mantiene el mismo problema y reduce el paso de altura:'
text+=table([r'$\Delta h$ (m)','$m_f$ (kg)','$t_f$ (s)','$x_f$ (m)'],convergence)
text+=r'El combustible es $5300-m_f='+number(5300-y[0])+r'\,\mathrm{kg}$. En esta aproximación, $x_f=90t_f$ ofrece un contraste adicional. Conservar $L\simeq W$ y $\dot x\simeq V$ es parte del modelo impuesto, no de la precisión del integrador.'
save('T13',text,[dict(convergence=convergence,first_step=first,trajectory=trace)])
# Locate the active frontier of a grid optimum, not just its final literal.
pol=models.Polar(30,.024,.046,1.6);W=4500*models.G;A=.5*30*.024;B=2*.046*W*W/30
lo=pol.stall(4500,1)*1.001;vs=np.linspace(lo,180,20001)
def turnrow(v):
 nT=math.sqrt(max(0,(7200-A*v*v)*v*v/B));nL=.5*v*v*30*1.6/W;n=min(nT,nL,3)
 rad=v*v/(models.G*math.sqrt(n*n-1)) if n>1 else float('inf')
 return [float(v),nT,nL,n,rad]
allrows=[turnrow(v) for v in vs];idx=min(range(len(vs)),key=lambda i:allrows[i][-1]);selected=[allrows[i] for i in range(max(0,idx-2),min(len(vs),idx+3))]
text=r'\textbf{Barrido y frontera activa.} Partir de $W=4500g_0$, $A=\rho SC_{D0}/2$ y $B=2kW^2/(\rho S)$. En viraje, $C_L=nW/(qS)$ y $D=AV^2+Bn^2/V^2$. Imponer $D\le T$ y despejar $n$ da $n_T$; imponer $C_L\le C_{L,max}$ da $n_L$. Para cada velocidad se elige $n=\min(n_T,n_L,3)$ y solo se calcula radio finito si $n>1$.'
text+=mathlines(r'A='+number(A)+r',\qquad B='+number(B)+r',\qquad V_{stall}='+number(pol.stall(4500,1))+r'\,\mathrm{m/s}')
text+=r'La rejilla usa 20001 puntos igualmente espaciados desde $1.001V_{stall}$ hasta 180 m/s. El factor 1.001 evita la singularidad de radio en la frontera $n=1$; no es un margen certificado. Las filas próximas al menor radio son:'
text+=table(['$V$','$n_T$','$n_L$','$n$','$R$ (m)'],selected)
text+=r'En cada fila puede verse qué límite fija $n$. El menor radio de esta rejilla es $'+number(allrows[idx][-1])+r'\,\mathrm m$ a $V='+number(vs[idx])+r'\,\mathrm{m/s}$. La cifra se debe informar como resultado de rejilla y contrastarse refinando alrededor de la intersección de restricciones, no como un óptimo continuo demostrado.'
save('T14',text,[dict(A=A,B=B,grid_step=float(vs[1]-vs[0]),selected=selected)])
(BOOK/'evidence/solution-method-calculations.json').write_text(json.dumps(records,ensure_ascii=False,indent=2)+'\n')
print(len(records),'method-specific derivations and traces total')
scalar_method('P21',r'Con $D=AV^2+Bn^2/V^2$, el empuje disponible limita la carga a $n_T=\sqrt{(T-AV^2)V^2/B}$. La sustentación la limita a $n_L=qSC_{L,max}/W$. El valor estructural 3.2 es un dato del enunciado, no un cálculo; se elige el menor de los tres límites.',[
('W','6200*9.80665','N','Peso del estado.'),('qS',f'.5*{models.isa(5000)[2]}*110**2*34','N','Fuerza de referencia local.'),('A',f'.5*{models.isa(5000)[2]}*34*.023','kg/m','Coeficiente parásito.'),('B',f'2*.043*W**2/({models.isa(5000)[2]}*34)','N*m**2/s**2','Coeficiente cuadrático de carga.'),('nT','sqrt((8200-A*110**2)*110**2/B)','','Carga que agota el margen de empuje.'),('nL','qS*1.6/W','','Carga que alcanza CL máximo.')])
with (FOLDER/'P21.tex').open('a') as f:f.write(r'\par Comparar $n_T\simeq2.120$, $n_L\simeq3.985$ y el dato $3.2$: el límite activo es el empuje y la carga sostenida máxima del modelo es aproximadamente 2.120.'+'\n')
scalar_method('P30',r'El determinante característico de una matriz dos por dos es $\lambda^2-\operatorname{tr}(A)\lambda+\det A$. La traza fija dos veces la parte real y el determinante fija $\omega_n^2$; solo después se obtiene el amortiguamiento.',[
('trace','-.6-1.4','1/s','Sumar la diagonal.'),('det','(-.6)*(-1.4)-1*(-3.5)','1/s**2','Restar productos diagonales cruzados.'),('real','trace/2','1/s','Parte real de los dos autovalores conjugados.'),('wn','sqrt(det)','1/s','Frecuencia natural.'),('wd','sqrt(det-real**2)','1/s','Frecuencia amortiguada.'),('zeta','-real/wn','','Factor de amortiguamiento positivo.'),('period','2*pi/wd','s','Pasar pulsación amortiguada a periodo.')])
# The underlying dataset retains more digits than the displayed prompt.
c=json.loads((BOOK/'reports/endurance-results.json').read_text())['cases'][0]
scalar_method('S06.1',r'Los tres tiempos son resultados conservados de una simulación y dos aproximaciones. Para compararlos se adopta como denominador el tiempo simulado, sin interpretar esa referencia como verdad experimental. Un error negativo significa que la aproximación predice menor duración.',[
('ec',f'{c["constant_initial_flow_time_s"]}/{c["simulated_time_s"]}-1','','Dividir el tiempo de gasto congelado por el simulado y restar uno.'),('eeq',f'{c["equivalent_polar_time_s"]}/{c["simulated_time_s"]}-1','','Repetir con el modelo equivalente.')])
(BOOK/'evidence/solution-method-calculations.json').write_text(json.dumps(records,ensure_ascii=False,indent=2)+'\n')
print(len(records),'method-specific derivations and traces total')
