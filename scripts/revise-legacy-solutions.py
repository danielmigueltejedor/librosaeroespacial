#!/usr/bin/env python3
"""Restore authored reasoning and print all intermediate arithmetic in exports."""
from pathlib import Path
import json,re,difflib,hashlib,sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from solution_steps import numeric_steps, prose_tex

def norm(s):
 s=re.sub(r'\\([A-Za-z]+)',r'\1',s)
 return re.sub(r'\W+','',s.lower())

def replace_development(path, bank, key, prompt, content, relative):
 text=path.read_text();marks=list(re.finditer(re.escape(r'\noindent\textbf{Enunciado}'),text));seen=[]
 for i,m in reversed(list(enumerate(marks))):
  end=marks[i+1].start() if i+1<len(marks) else len(text)
  block=text[m.start():end]
  written=block[len(m[0]):].lstrip().split('\n\n')[0]
  scores=sorted((difflib.SequenceMatcher(None,norm(written),norm(prompt(p))).ratio(),j) for j,p in enumerate(bank))
  score,j=scores[-1]
  exact=[k for k,p in enumerate(bank) if key(p) in written]
  if len(exact)==1:j=exact[0];score=1.0
  if score<.84:raise ValueError((path,score,written[:100]))
  ident=key(bank[j]);seen.append(ident)
  pattern=re.escape(r'\noindent\textbf{Desarrollo}')+r'\s*'+re.escape(r'\begin{enumerate}')+r'.*?'+re.escape(r'\end{enumerate}')
  replacement=r'\noindent\textbf{Desarrollo paso a paso}'+'\n\n'+r'\input{'+relative+'/'+ident+'.tex}\n\n'
  if re.search(pattern,block,re.S):block=re.sub(pattern,lambda m:replacement,block,count=1,flags=re.S)
  else:assert relative+'/'+ident+'.tex' in block,(path,ident)
  text=text[:m.start()]+block+text[end:]
 assert len(seen)==len(set(seen))==len(bank),(path,len(seen))
 path.write_text(text)
 return len(seen)

# These annotations explain the missing connection to the model. They do not
# change numerical data or silently claim independent scientific review.
EXPLAIN={
'PRB-0149':r'La exigencia $k=EA/L$ fija un área distinta para cada material: $A=kL/E$. Luego $m=\rho AL=\rho kL^2/E$. Comparar densidad sola sería incorrecto porque el área cambia.',
'PRB-0150':r'Primero imponer la rigidez $EA/L=k$ y despejar $A=kL/E$; después calcular volumen $AL$ y masa $\rho AL$. La comparación se hace a igual rigidez, no a igual sección.',
'PRB-0125':r'Para el anillo circular delgado, la ley de cortante alcanza un máximo que es dos veces la media $C_y/(2\pi Rt)$. Sustituir esa sección resistente da $\tau_{max}=C_y/(\pi Rt)$.',
'PRB-0126':r'Calcular primero $I_z$ de alma y alas. La ley $q=C_yQ/I_z$ se integra sobre el ala: $F=\int_0^b C_y(th/2)s/I_z\,ds=C_yhtb^2/(4I_z)$. No se multiplica el flujo máximo por toda la anchura.',
'PRB-0127':r'La idealización concentra área axial en cuatro larguerillos: $I_z=\sum B_i y_i^2=4By^2$. Al cruzar un larguerillo, el primer momento cambia en $By$, de modo que el salto de flujo es $\Delta q=C_yBy/I_z$.',
'PRB-0128':r'Integrar los flujos de las alas da un par respecto al alma. Igualar ese par a $C_y e_c$ y usar $I_z=th^2(h+6b)/12$ elimina $t$ y permite despejar $e_c=3b^2/(h+6b)$. La distancia se mide desde el alma.',
'PRB-0129':r'El área de pared es aproximadamente $2\pi Rt$, por lo que la tensión media es $C_y/(2\pi Rt)$. La distribución de cortante del anillo eleva el máximo al doble. No confundir media y máxima.',
'PRB-0141':r'La ecuación característica del bloque plano da media $c=(\sigma_x+\sigma_y)/2$ y radio $R=\sqrt{[(\sigma_x-\sigma_y)/2]^2+\tau_{xy}^2}$. Las dos principales son $c+R$ y $c-R$; se conserva además la principal fuera del plano cuando corresponda.',
'PRB-0142':r'La relación isótropa $E=2G(1+\nu)$ se resuelve dividiendo ambos lados por $2(1+\nu)$. Conservar la unidad del módulo de entrada: dividir por un número adimensional no la modifica.',
'PRB-0144':r'El criterio de Tresca utiliza la mayor diferencia entre las tres principales, incluyendo la nula fuera del plano en tensión plana. Se evalúan todos los pares, se toma su máximo absoluto y se divide el límite uniaxial por ese valor.',
'PRB-0145':r'La deformación volumétrica lineal es la traza: $e=\varepsilon_x+\varepsilon_y+\varepsilon_z$. Sumar las tres leyes de Hooke da $e=(1-2\nu)(\sigma_x+\sigma_y+\sigma_z)/E$. Para tres tensiones iguales, la suma es $3\sigma$.',
'PRB-0147':r'En cortante puro, $\sigma_x=\sigma_y=\sigma_z=0$. En la expresión de von Mises quedan tres veces los cuadrados de cortante; con una sola componente $\sigma_v^2=3\tau^2$. La raíz positiva da $\sqrt3|\tau|$.',
'PRB-0153':r'Calcular primero $G=E/[2(1+\nu)]$ para el material isótropo. La ley de cortante $\tau=G\gamma$ se despeja como $\gamma=\tau/G$. El ángulo de distorsión sale adimensional, aproximadamente en radianes.',
'PRB-0154':r'La tracción es $\boldsymbol t=\boldsymbol\sigma\boldsymbol n$. En tracción uniaxial, proyectar sobre la normal da $\sigma_n=\sigma\cos^2\theta$. Hay dos proyecciones: una forma el vector tracción y otra su componente normal.',
'PRB-0161':r'Con equilibrio y $EI\,v\prime\prime=M(x)$, integrar por tramos e imponer flecha nula en los dos apoyos da para carga uniforme $\delta_C=5qL^4/(384EI)$. Usar $q$ en N/mm cuando $L$ e inercia estén en mm; la flecha resulta en mm.',
'PRB-0162':r'Para el voladizo, $M(x)=-q(L-x)^2/2$ con el convenio adoptado. Integrar $EI\,v\prime\prime=M$ e imponer $v(0)=v\prime(0)=0$ produce módulo de flecha final $qL^4/(8EI)$. El signo físico sigue el sentido de la carga.',
'PRB-0163':r'La ley de flexión es $\sigma=My/I$. En un círculo macizo, $I=\pi d^4/64$ e $y_{max}=d/2$; por tanto $W=I/y_{max}=\pi d^3/32$ y $\sigma_{max}=M/W$.',
'PRB-0164':r'El límite del núcleo exige que la tensión no cambie de signo en ninguna esquina. Con axil excéntrico, $\sigma=N/A\pm Ne_y(h/2)/I_z\pm Ne_z(b/2)/I_y$. Imponer tensión nula en una esquina fija las intersecciones $h/6$ y $b/6$ del rombo.',
'PRB-0168':r'La torsión circular cumple $\tau=Tr/J$. Para sección maciza $J=\pi D^4/32$ y $r_{max}=D/2$; sustituir y cancelar un factor $D$ da $\tau_{max}=16T/(\pi D^3)$.',
'PRB-0169':r'Para anillo cerrado delgado $J_c=2\pi R^3t$. Al abrirlo como tira, $J_a\simeq(2\pi R)t^3/3$. Dividir cancela $2\pi Rt$ y deja $J_c/J_a=3(R/t)^2$. No se usa el momento polar para la sección abierta.',
'PRB-0170':r'Bredt da flujo constante $q=T/(2A_m)$ en una célula cerrada. Como $A_m=\pi R^2$ y $\tau=q/t$, resulta $\tau=T/(2\pi R^2t)$. Las dimensiones son las de tensión.',
'PRB-0171':r'La ley de giro es $\theta=TL/(GJ)$. Despejar $T=GJ\theta/L$ exige convertir el grado a $\pi/180$ rad. En un tubo, $J=\pi(R_o^4-R_i^4)/2$ utiliza radios, no diámetros.',
'PRB-0172':r'Para una tira muy delgada de ancho $a$ y espesor $s$, el módulo torsional aproximado conduce a $\tau_{max}\simeq3T/(as^2)$. Verificar $a/s\gg1$ antes de usar esa aproximación; el espesor entra al cuadrado.',
'PRB-0176':r'Con fuerza final $P$ en un voladizo, $M=P(L-x)$. El giro por trabajo virtual usa momento virtual unidad, de modo que $\phi=\int_0^L M/(EI)dx=PL^2/(2EI)$. La flecha usaría otra ley virtual.',
'PRB-0177':r'Identificar reacciones escalares independientes $r$. Un sólido plano conectado aporta tres ecuaciones independientes de equilibrio. Cuando no hay mecanismos ni restricciones redundantes adicionales, el exceso es $g=r-3$; contar apoyos sin analizar su vínculo puede fallar.',
'PRB-0178':r'Para viga biapoyada con carga uniforme, $M=qx(L-x)/2$. Sustituir en $U=\int M^2/(2EI)dx$ deja $q^2\int_0^Lx^2(L-x)^2dx/(8EI)$. Expandir el polinomio e integrar da $L^5/30$ y finalmente $U=q^2L^5/(240EI)$.',
'PRB-0179':r'Liberar el apoyo redundante y exigir desplazamiento nulo en su posición. En el voladizo base, la carga uniforme da $qL^4/(8EI)$ y la reacción ascendente $X$ da $XL^3/(3EI)$. Igualarlas permite despejar $X=3qL/8$.',
'PRB-0180':r'Las dos leyes triangulares de momento son $M=cx/L$ y $\bar M=dx/L$. Su producto integra $cd\int_0^Lx^2dx/L^2=cdL/3$. No se multiplica simplemente área por ordenada máxima.',
'PRB-0189':r'La inercia respecto al eje horizontal es $I_z=\int_A y^2dA=b\int_{-h/2}^{h/2}y^2dy=bh^3/12$. La dimensión perpendicular al eje es la que aparece al cubo.',
}
records=[]
book=ROOT/'books/estructuras-aeroespaciales';folder=book/'solutions/generated';folder.mkdir(parents=True,exist_ok=True)
bank=json.loads((ROOT/'reports/bundle-audit/structures-problem-bank.json').read_text())['problems']
for p in bank:
 s=p['solution'];steps=[]
 for j,row in enumerate(s['steps'],1):
  steps.append(dict(target=f'y_{j}',expression=row.get('expression'),equation=row.get('equation'),unit=row.get('unit',''),
                    expected=row.get('expected'),why=row['text']+'.'))
 numeric,checks=numeric_steps(steps)
 development=s.get('development',[])
 out=[]
 if p['id'] in EXPLAIN:out.append(r'\noindent\textbf{Por qué se usa este procedimiento.} '+EXPLAIN[p['id']])
 if development:out += [r'\begin{enumerate}',*[r'\item '+prose_tex(x) for x in development],r'\end{enumerate}']
 out += [r'\noindent\textbf{Operaciones y resultados intermedios.}',numeric]
 (folder/(p['id']+'.tex')).write_text('\n\n'.join(out)+'\n')
 # A renderer can print exact equations from the bank as well as their complete
 # substitutions. The public corpus retains original numerical precision.
 records.append(dict(book=book.name,key=p['id'],steps=checks))
replace_development(book/'latex/manual.tex',bank,lambda p:p['id'],lambda p:p['prompt'],None,'../solutions/generated')
# The companion generator shares these authored notes and arithmetic routines.
notes=book/'solutions/reasoning.json';notes.write_text(json.dumps(EXPLAIN,ensure_ascii=False,indent=2)+'\n')

book=ROOT/'books/turbomaquinas';folder=book/'solutions/generated';folder.mkdir(parents=True,exist_ok=True)
bank=json.loads((book/'reports/problem-bank-public.json').read_text())['problems']
for p in bank:
 given={k:v for k,v,*_ in p['given']}
 rows=[dict(target=target,expression=e,unit=u,why=why) for why,e,u,target in p['steps']]
 out,checks=numeric_steps(rows,given)
 (folder/(p['key']+'.tex')).write_text(out+'\n')
 records.append(dict(book=book.name,key=p['key'],steps=checks))
for f in ['turbomaquinas-ule-2026.tex','problemas-resueltos.tex']:
 replace_development(book/'publication'/f,bank,lambda p:p['key'],lambda p:p['prompt'],None,'../solutions/generated')
report=dict(scope='Restore stored reasoning and show every supplied numeric operation; not independent academic approval',reviewer='same authoring model',records=records)
(ROOT/'reports/solution-procedure-legacy.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(len(records),'legacy cases rewritten')
