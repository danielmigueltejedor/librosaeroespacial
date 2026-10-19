"""Compatibilidad del adaptador, derivaciones y contratos nativos explícitos."""
import json,sys
from pathlib import Path
from native_import import call,standard,nm,refs,R,problems
def compatibility(rebuild_problems=True):
    rows=json.loads((R/'evidence/native-paragraphs.json').read_text());edits=[]
    first=set()
    for row in rows:
        original=row['result'].get('paragraph',{})
        if not original:continue
        text=original['text'];fixed=standard(text);ch=row['chapter'];concept=False
        if ch not in first and len(text)>100 and not text.lstrip().startswith('\\'):
            first.add(ch);concept=True
        if fixed!=text or concept:
            args=dict(id=original['id'],text=fixed,excerpts=original['excerpts'],role=original.get('role','explanation'))
            if concept:args.update(concepts=[f'c{ch:02}.model'],subsection=f'c{ch:02}.core')
            rr=call('studium_paragraph_replace',args);edits.append(rr)
    (R/'reports/native-compatibility-edits.json').write_text(json.dumps(edits,ensure_ascii=False,indent=2,default=str))
    if not rebuild_problems:return
    old=json.loads((R/'evidence/native-problems.json').read_text())
    for row in old:call('studium_problem_remove',dict(id=row['record']['problem']['id']))
    # Se registra otra revisión sin macros editoriales; los controles se vuelven a vincular.
    problems()
def paragraphs_only():
    compatibility(False)
def derivations():
    D=[
     (4,'Resistencia nivelada',r'D=\frac12\rho SC_{D0}V^2+\frac{2kW^2}{\rho SV^2}', 'rho*S*CD0*V**2/2+2*k*W**2/(rho*S*V**2)',{'rho':'kg/m^3','S':'m^2','CD0':'1','V':'m/s','k':'1','W':'N'},'N',['L=W; polar parabólica; rho y parámetros definidos.']),
     (4,'Potencia de empuje',r'P=DV','D*V',{'D':'N','V':'m/s'},'W',['Empuje o resistencia paralelos a velocidad aérea.']),
     (10,'Gasto másico de reactor',r'\dot m_f=c_TT','cT*T',{'cT':'kg/(N*s)','T':'N'},'kg/s',['cT referido a masa por empuje y tiempo.']),
     (15,'Gasto másico por potencia',r'\dot m_f=c_PP_{eje}','cP*P',{'cP':'kg/J','P':'W'},'kg/s',['cP referido a potencia al eje.']),
     (12,'Escala temporal de Breguet',r'E=\frac{C_L}{g_0c_TC_D}\ln(W_i/W_f)','CL/(g*cT*CD)*log(Wi/Wf)',{'CL':'1','CD':'1','g':'m/s^2','cT':'kg/(N*s)','Wi':'N','Wf':'N'},'s',['CL, polar y consumo constantes; Wi>Wf>0; T=D.']),
     (16,'Alcance ideal de hélice',r'R=\frac{\eta_pC_L}{g_0c_PC_D}\ln(W_i/W_f)','eta*CL/(g*cP*CD)*log(Wi/Wf)',{'eta':'1','CL':'1','CD':'1','g':'m/s^2','cP':'kg/J','Wi':'N','Wf':'N'},'m',['CL, eta y cP constantes; vuelo horizontal y Wi>Wf>0.']),
     (13,'Tasa por exceso de potencia',r'c=(P_d-P_n)/W','(Pd-Pn)/W',{'Pd':'W','Pn':'W','W':'N'},'m/s',['Velocidad constante y ángulo pequeño para evaluar L≈W.']),
     (14,'Radio de viraje nivelado',r'R=V^2/(g_0\tan\phi)','V**2/(g*tan(phi))',{'V':'m/s','g':'m/s^2','phi':'radian'},'m',['Viraje nivelado coordinado, sin viento, phi distinto de cero y menor de 90 grados.']),
     (17,'Distancia de rodadura',r's=V^2/(2a)','V**2/(2*a)',{'V':'m/s','a':'m/s^2'},'m',['Sólo aceleración constante desde reposo; no reemplaza la cuadratura variable.']),
     (19,'Margen y derivada estática',r'C_{m\alpha}=-a(h_n-h)','-a*(hn-h)',{'a':'1/radian','hn':'1','h':'1'},'1/radian',['Mando fijo, pendiente de sustentación positiva y modelo lineal declarado.'])]
    out=[]
    for ch,name,eq,symbolic,variables,unit,assumptions in D:
        rr=call('studium_derivation_record',dict(section=f'c{ch:02}',name=name,equation=eq,symbolic=symbolic,variables={k:dict(meaning='Magnitud '+k+' definida en el capítulo correspondiente.',units=v) for k,v in variables.items()},assumptions=assumptions,governing_principles=['Balances y definiciones explícitos del capítulo.'],steps=['Partir del balance y sustituir las relaciones declaradas antes de evaluar.'],steps_latex=[eq],references=dict(excerpts=refs(ch)),applicability=assumptions,limitations=['La comprobación dimensional no demuestra hipótesis ni modelo; revisión experta pendiente.']))
        ck=call('studium_derivation_check',dict(id=rr['derivation']['id'],dimensions=dict(expression=symbolic,symbol_units=variables,expected_unit=unit)))
        out.append(dict(record=rr,check=ck))
    (R/'reports/native-derivations.json').write_text(json.dumps(out,ensure_ascii=False,indent=2,default=str))
def contracts():
    claims=[
     (4,'La resistencia de la polar nivelada se expresa como AV²+B/V² con las hipótesis definidas.',{'A':'N*s^2/m^2','B':'N*m^2/s^2','V':'m/s'}, {'A':'2','B':'3','V':'4'}, 'A*V**2+B/V**2','N'),
     (10,'El gasto másico del reactor es cT por empuje; la definición de cT es másica.',{'cT':'kg/(N*s)','T':'N'},{'cT':'0.000017','T':'10000'},'cT*T','kg/s'),
     (15,'La potencia útil de hélice es eta por potencia al eje en el régimen de definición.',{'eta':'1','P':'W'},{'eta':'0.8','P':'200000'},'eta*P','W'),
     (13,'La tasa de ascenso aproximada por potencia excedente exige la ley de velocidad declarada.',{'Pd':'W','Pn':'W','W':'N'},{'Pd':'300000','Pn':'200000','W':'50000'},'(Pd-Pn)/W','m/s')]
    out=[]
    for ch,text,units,bindings,expression,expected in claims:
        rr=call('studium_claim_record',dict(section=f'c{ch:02}',text=text,excerpts=refs(ch)))
        claim=rr['claim']['id']
        contract=dict(variables={**units,'Y':expected},bindings=bindings,assumptions=[dict(id='positive_denominator',left='V' if 'V' in bindings else 'W' if 'W' in bindings else 'T' if 'T' in bindings else 'P',relation='gt',right='0')],equations=[dict(id='expression_definition',left='Y',right=expression)],representations=[dict(record=claim,role='theory',requires=['positive_denominator'],checks=[dict(kind='dimensions',expression=expression,expected_unit=expected),dict(kind='defined',expression=expression)])])
        # La definición Y se usa sólo como etiqueta de ecuación; las pruebas anteriores operan la expresión.
        cr=call('studium_scientific_contract_record',dict(claim_id=claim,contract=contract,origin='generator'))
        out.append(dict(claim=rr,contract=cr))
    (R/'reports/native-contracts-recorded.json').write_text(json.dumps(out,ensure_ascii=False,indent=2,default=str))
def notation():
    for symbol,meaning,unit in [('V','Módulo de velocidad relativa al aire, TAS.','m/s'),('m','Masa total instantánea del avión.','kg'),('W','Peso mg0 del avión.','N'),('c_T','Consumo específico másico por empuje.','kg/(N*s)'),('c_P','Consumo específico másico por potencia al eje.','kg/J'),('q_\\infty','Presión dinámica de referencia.','Pa'),('I_{xz}','Integral xz dm; entra con signo negativo en tensor.','kg*m^2')]:
        call('studium_notation_record',dict(section='c01',symbol=symbol,meaning=meaning,units=unit))
if __name__=='__main__':
    for mode in sys.argv[1:]:globals()[mode]()
