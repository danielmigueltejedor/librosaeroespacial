from pathlib import Path
import sys,re,json
R=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(R/'scripts'))
from problem_bank import P
from case_bank import CASES
from exam_bank import EXAMS
# Corrección editorial de espacios sin tocar expresiones de prueba ni comandos matemáticos.
fix={
'esmenorque':'es menor que','recuperaríaamplitud':'recuperaría amplitud','alminimo':'al mínimo','recupera36':'recupera 36','ligamento,carga':'ligamento, carga','retardosniiniciación':'retardos ni iniciación','Ncrece':'N crece','reducirDeltaSigma':'reducir el rango de tensión','exponente2':'exponente 2','denominador1':'denominador 1','contiene1/a':'contiene 1/a','eslogaritmo':'es logaritmo','cocientea_f/a_iesadimensional':'cociente entre tamaños es adimensional','Siaf=ai,log1=0yN=0':'Si los tamaños final e inicial coinciden, el logaritmo y la vida de propagación son cero','del40%':'del 40%','factor0,4no':'factor 0,4 no','es0,4':'es 0,4','durante20h':'durante 20 h','permanencia20h':'permanencia 20 h','MismoQ,n':'Mismos Q y n','gradosCelsius':'grados Celsius','t2con':'t2 con','recuperaP':'recupera P','conservandoC':'conservando C','ensayo900K':'ensayo a 900 K','deformación0,0007':'deformación 0,0007','sumar0,0005+2e−8·35000se recupera0,0012':'sumar las contribuciones elástica y de fluencia se recupera la deformación límite','ConVf=0se':'Con fracción de fibra cero se','panelniotros':'panel ni otros','longitudinaly':'longitudinal y','problemaP23':'problema P23','comparacióncon':'comparación con','espesor2t':'espesor 2t','hcomo':'h como','carascontiguas':'caras contiguas','para2x':'para 2x','xesespesor':'x es espesor','a1000h':'a 1000 h','recuperakp':'recupera la constante parabólica','Profundidadd':'Profundidad d','total47,2mm':'total de 47,2 mm','por5900m/s':'por 5900 m/s','recupera8µs':'recupera 8 microsegundos','defectoniPOD':'defecto ni la probabilidad de detección','ydelta2':'y su valor a la frecuencia nueva','usan100000Hz':'usan 100000 Hz','a400kHz':'a 400 kHz','detecciónni':'detección ni','de100horas':'de 100 horas','R(0)=1y':'R(0)=1 y','tpara':'t para','programadoniotras':'programado ni otras','entre0y1':'entre cero y uno','sobrevivir200horas':'sobrevivir 200 horas','alcanzado500sin':'alcanzado 500 sin','usa700y500horas':'usa 700 y 500 horas','beta=1la':'beta igual a uno, la','del95%para':'del 95% para','nivel0,95':'nivel 0,95','SustituirlambdaUTda−ln0,05y la probabilidad de ceroeventoses0,05':'Sustituir el límite en la probabilidad de cero eventos devuelve 0,05','individualni':'individual ni','yorden':'y orden','giro160Hz':'giro de 160 Hz','orden3':'orden 3','Multiplicarordenporfrecuencia':'Multiplicar orden por frecuencia','recupera480Hz':'recupera 480 Hz','desalineaciónni':'desalineación ni','delmodelo':'del modelo','kg/m³y650MPa':'kg/m³ y 650 MPa','uniónni':'unión ni','fabricacióno':'fabricación o',
'nohay':'no hay','aplicabilidadjurisdiccional':'aplicabilidad jurisdiccional','estadovigenteDRSporcomprobar':'estado vigente en DRS por comprobar','publicaciónoriginal':'publicación original','trataun':'trata un','depilotoautomático':'de piloto automático','datosdecomponentes':'datos de componentes','decomponentes':'de componentes','devidaaplicables':'de vida aplicables','tratarvacío':'tratar vacío','yse':'y se','ylos':'y los','intervalosyfechasnuméricosinventados':'intervalos y fechas numéricos inventados','parael':'para el','porjornada':'por jornada','sealcanzaríael':'se alcanzaría el','deoperación':'de operación','elcalendario':'el calendario','ylafecha':'y la fecha','delritmo':'del ritmo','deutilización':'de utilización','seconvierte':'se convierte','jornadasautomáticamente':'jornadas automáticamente','díasnaturales':'días naturales','unaprevisión':'una previsión','seacumulan':'se acumulan','octubrese':'octubre se','yfecha':'y fecha',
'referenciaALSsupuestas':'referencia ALS supuestas','deMEL':'de MEL','yMELaplicable':'y MEL aplicable','yMELreales':'y MEL reales','MAWAcomo':'MAWA como','EARde':'EAR de','ARCde':'ARC de','datosy':'datos y','modificaciónycondiciones':'modificación y condiciones','contrastaP/N':'contrasta P/N','STCni':'STC ni','ySTC':'y STC','deENDdel':'de END del','delcapítulo':'del capítulo','yP/N':'y P/N','identidadP/NyS/Nconfirmada':'identidad P/N y S/N confirmada','cadaAD':'cada AD',
'°Cno':' °C no','950a1000Ksin':'950 a 1000 K sin','M/MLy':'M/ML y','AOCni':'AOC ni','identificarP/N':'identificar P/N','aIPC':'a IPC','AMMyCMM':'AMM y CMM','IP Cayuda':'IPC ayuda','IPCayuda':'IPC ayuda','AMMaporta':'AMM aporta','CMMtrata':'CMM trata','CRSde':'CRS de','ARCregistra':'ARC registra','CRScertifica':'CRS certifica','CRSycertificado':'CRS y certificado','conM.A.':'con M.A.','en145.A.':'en 145.A.','pero145.A.':'pero 145.A.','archivoBOE':'archivo BOE','queEMAR':'que EMAR','EMARson':'EMAR son','MAWAno':'MAWA no','consultaRD':'consulta RD','Para$':'Para $','ADy':'AD y','yAMOC':'y AMOC','delSBno':'del SB no','tieneForm':'tiene Form','Form1no':'Form 1 no','correlaciónLarson':'correlación Larson','Millercon':'Miller con','deMFELyParisse':'de MFEL y Paris se','Calculea_c':'Calcule el tamaño crítico','académicoN/3':'académico N/3','unaAD':'una AD','unSB':'un SB','unaMEL':'una MEL','reglamentaria,':'reglamentaria,','a900Krompe':'a 900 K rompe','a940Ky':'a 940 K y'
}
def cleanplain(s):
 for a,b in sorted(fix.items(),key=lambda x:-len(x[0])):s=s.replace(a,b)
 s=re.sub(r'(?<=[a-záéíóúñ])(?=[A-ZÁÉÍÓÚÑ])',' ',s)
 s=re.sub(r'(?<=[a-záéíóúñ])(?=\d)',' ',s)
 s=re.sub(r'(?<=\d)(?=[A-Za-záéíóúñ])',' ',s)
 s=re.sub(r'(?<=[,;:])(?=[A-Za-záéíóúñ])',' ',s)
 s=re.sub(r'(?<=[^\d]),(?=\d)',', ',s)
 s=re.sub(r'\b(AD|RD|Form|Parte|ARC|STC|LLP)(?=\d)',r'\1 ',s)
 s=s.replace('−', '-').replace('–','--').replace('—','---').replace('√',' raíz de ').replace('µ','micro').replace('⁻¹',r'\(^{-1}\)').replace('³',r'\(^{3}\)').replace('²',r'\(^{2}\)').replace('%',r'\%').replace('°C',r'$^\circ\mathrm C$')
 s=re.sub(r'(?<=\d)h\b',' h',s)
 return s
# Conservar todo lo que sea matemático o comando; normalizar únicamente el texto.
def clean(s):
 parts=re.split(r'(\$[^$]*\$|\\\[.*?\\\]|\\\(.*?\\\)|\\[a-zA-Z]+(?:\{[^{}]*\})?)',s,flags=re.S)
 out=''.join(p if (p.startswith('$') or p.startswith('\\')) else cleanplain(p) for p in parts)
 out=re.sub(r'([a-záéíóúñ])(?=\$)',r'\1 ',out)
 out=re.sub(r'(\$)(?=[a-záéíóúñ])',r'\1 ',out)
 out=re.sub(r'([0-9]+(?:\.[0-9]+)?)e([+-]?[0-9]+)',lambda m:m[1]+r'\times10^{'+str(int(m[2]))+'}',out)
 return out
def walk(x):
 if isinstance(x,str):return clean(x)
 if isinstance(x,list):return [walk(v) for v in x]
 if isinstance(x,dict):return {k:(v if k in ['tests','key','ch','date'] else walk(v)) for k,v in x.items()}
 return x
P=walk(P);C=walk(CASES);E=walk(EXAMS)
by={p['key']:p for p in P}
by['P08']['unknown']=r'$a_c$, $2a_c$ y tensión crítica para $a_i$.'
by['P08']['check']=r'Sustituir $a_c$ en $K_I$ recupera $36\,\mathrm{MPa\sqrt m}$. Duplicar tensión reduce el tamaño crítico a un cuarto si $Y$ permanece constante.'
by['P09']['unknown']=r'Dimensión $2{,}5(K/\sigma_y)^2$ y comparación con espesor.'
by['P12']['model']=r'Basquin con $\sigma_a=AN^b$, usando ciclos y no reversiones.'
by['P12']['check']=r'Sustituir $10^4$ y $10^6$ ciclos recupera 400 y 220 MPa. La vida objetivo queda entre ambas.'
by['P13']['unknown']=r'Número de ciclos $n_2$.'
by['P13']['check']=r'La suma $0{,}15+25500/30000$ es uno y $n_2<N_2$.'
by['P15']['unknown']=r'$K_{max}$, $K_{min}$, $\Delta K$ y $R$.'
by['P15']['check']=r'$K_{min}/K_{max}=R$ y $K_{max}-K_{min}=\Delta K$. La intensidad máxima queda por debajo de la tenacidad supuesta en el modelo.'
by['P15']['limits']=r'Un $\Delta K$ positivo no garantiza validez de Paris: se necesita dominio de crecimiento, umbral, razón de carga y condiciones. La comparación estática no excluye propagación.'
by['P21']['unknown']=r'Tiempo $t_2$ y parámetro $P$.'
by['P23']['unknown']=r'$E_L$, $\rho$ y $E_L/\rho$.'
by['P24']['unknown']=r'$E_T$ en la idealización.'
by['P26']['check']=r'$x^2/t$ recupera $k_p$. El tiempo crece con el cuadrado del espesor en esta ley.'
by['P28']['check']=r'La ley de escala $f^{-1/2}$ ofrece una comprobación independiente.'
by['P29']['unknown']=r'$\lambda$, MTBF y $R(100)$.'
by['P31']['unknown']=r'$R(t_0+\Delta t)/R(t_0)$.'
by['P32']['unknown']=r'Límite superior $\lambda_U$.'

# Formas tipográficas de símbolos que también aparecen en la prosa.
for p in P:
 p['check']=p['check'].replace('a^(−3/2)',r'$a^{-3/2}$').replace('a^(-3/2)',r'$a^{-3/2}$').replace('f^(-1/2)',r'$f^{-1/2}$')
# Guardar exactamente la versión editorial que se imprime para auditarla.
for name,data in [('problem-bank',P),('case-bank',C),('exam-bank',E)]:
 (R/'evidence'/f'{name}-editorial.json').write_text(json.dumps(data,ensure_ascii=False,indent=2))
if __name__=='__main__':print('Bancos editoriales preparados:',len(P),len(C),len(E))
