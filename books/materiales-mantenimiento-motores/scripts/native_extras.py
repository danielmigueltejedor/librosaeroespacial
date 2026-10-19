from pathlib import Path
import json

def register_extras(call,R):
 guide=(R/'work/texts/GUIA2026-raw.txt').read_text()
 call('studium_course_document_record',{'title':'Guía docente oficial ULE 0710341, 2026-2027','url':'https://guiadocenteapi.unileon.es/syllabuses/downloadPdf/2026-2027/0710341','text':guide})
 call('studium_course_recorded',{})
 ids=json.loads((R/'evidence/studium-ids.json').read_text())
 specs=[('c02','Elongación axial',r'\Delta L=FL/(AE)','F*L/(A*E)',{'F':'N','L':'m','A':'m^2','E':'Pa'},'m',[r'\sigma=F/A',r'\varepsilon=\sigma/E',r'\Delta L=\varepsilon L']),('c03','Grieta crítica con Y constante',r'a_c=(K_c/(Y\sigma))^2/\pi','(K/(Y*sigma))**2/pi',{'K':'Pa*m^0.5','Y':'dimensionless','sigma':'Pa'},'m',[r'K_c=Y\sigma\sqrt{\pi a_c}',r'K_c^2=Y^2\sigma^2\pi a_c',r'a_c=K_c^2/(\pi Y^2\sigma^2)']),('c04','Paris con exponente tres',r'N=2(a_i^{-1/2}-a_f^{-1/2})/[C(Y\Delta\sigma\sqrt\pi)^3]','2*(ai**(-0.5)-af**(-0.5))/(C*(Y*ds*sqrt(pi))**3)',{'ai':'m','af':'m','C':'1/(Pa^3*m^0.5)','Y':'dimensionless','ds':'Pa'},'dimensionless',[r'dN=da/[C(Y\Delta\sigma\sqrt{\pi a})^3]',r'N=[C(Y\Delta\sigma\sqrt\pi)^3]^{-1}\int_{a_i}^{a_f}a^{-3/2}\,da',r'N=2(a_i^{-1/2}-a_f^{-1/2})/[C(Y\Delta\sigma\sqrt\pi)^3]']),('c05','Relajación de tensión',r'\dot\sigma=-E\dot\varepsilon_c','-E*epsdot',{'E':'Pa','epsdot':'1/s'},'Pa/s',[r'\varepsilon_{tot}=\sigma/E+\varepsilon_c',r'0=\dot\sigma/E+\dot\varepsilon_c',r'\dot\sigma=-E\dot\varepsilon_c']),('c09','Rigidez sándwich ideal',r'EI=2E[bt^3/12+bt(h/2)^2]','2*E*(b*t**3/12+b*t*(h/2)**2)',{'E':'Pa','b':'m','t':'m','h':'m'},'N*m^2',[r'I_{cara}=bt^3/12+bt(h/2)^2',r'I=2I_{cara}',r'EI=2E[bt^3/12+bt(h/2)^2]'])]
 rows=[]
 for ch,name,eq,sym,units,unit,steps in specs:
  source='MIT-ELAS' if ch=='c02' else 'MIT-FRAC' if ch=='c03' else 'MIT-FAT' if ch=='c04' else 'MIT-CREEP' if ch=='c05' else 'MIT-COMP'
  r=call('studium_derivation_record',{'section':ch,'name':name,'equation':eq,'symbolic':sym,'variables':units,'assumptions':['Hipótesis específicas desarrolladas en el capítulo: modelo idealizado y datos compatibles.'],'governing_principles':['Equilibrio, compatibilidad o integración de la ley constitutiva indicada.'],'steps':['Paso '+str(i+1) for i in range(len(steps))],'steps_latex':steps,'boundary_conditions':['Condiciones del capítulo y del ejercicio particular.'],'applicability':['Dominio del modelo académico.'],'limitations':['Dimensiones correctas no prueban adecuación física ni autorización real.'],'references':{'excerpts':ids[source]['excerpts']}})
  ck=call('studium_derivation_check',{'id':r['derivation']['id'],'dimensions':{'expression':sym,'symbol_units':units,'expected_unit':unit}}) if 'derivation' in r else None
  rows.append({'name':name,'record':r,'check':ck})
 (R/'evidence/derivations.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2,default=str))
 # Código autocontenido del modelo de figura; registros pendientes de comprobación nativa.
 src=(R/'scripts/figures.py').read_text();src=src[:src.index("(R/'evidence/figures.json')")]
 src=src.replace("R=Path(__file__).resolve().parents[1]","R=Path('.')")
 a=src.index('def save(');b=src.index('def flow(',a)
 src=src[:a]+'''def save(key,fig,scope):
 fig.tight_layout()
 if key==TARGET:fig.savefig('figure.pdf')
 plt.close(fig)
'''+src[b:]
 rows=[];coverage=json.loads((R/'reports/coverage.json').read_text());mapping={x['key']:x['chapter'] for x in coverage['figures']}
 for fig in json.loads((R/'evidence/figures.json').read_text()):
  ch=mapping[fig['key']];source='MIT-ELAS' if ch<12 else 'EU1321'
  r=call('studium_figure_record',{'section':f'c{ch:02d}','key':fig['key'],'caption':fig['scope'],'kind':'python','source':'TARGET='+repr(fig['key'])+'\n'+src,'excerpts':ids[source]['excerpts']})
  rows.append({'key':fig['key'],'record':r,'check':'PENDIENTE de ejecución nativa aislada; PDF/PNG generados por scripts/figures.py e inspeccionados visualmente.'})
 (R/'evidence/figures-imported.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2,default=str))
 print('Guía, derivaciones y figuras registradas',flush=True)
