from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'scripts'))
from solution_steps import numeric_steps
book=ROOT/'books/motores-cohete'
rows={
'M01':[('FA','2*600/3000','N','Despejar empuje de potencia cinética: F=2P/v.'),('mA','2*600/3000**2','kg/s','Del balance de energía, caudal es 2P/v al cuadrado.'),('IA','FA*120','N*s','Integrar empuje constante durante el intervalo.'),('FB','2*600/18000','N','Repetir el balance de momento y energía con la segunda velocidad.'),('mB','2*600/18000**2','kg/s','Calcular el segundo caudal.'),('IB','FB*120','N*s','Impulso del segundo caso.')],
'M02':[('Fk','2.40*2500','N','Contribución cinética del caudal.'),('Fp90','(45000-90000)*.012','N','Presión residual en el primer ambiente.'),('F90','Fk+Fp90','N','Sumar contribuciones del mismo balance.'),('c90','F90/2.40','m/s','Velocidad efectiva incluye presión.'),('Isp90','c90/9.80665','s','Pasar a impulso específico convencional.'),('Fv','Fk+45000*.012','N','En vacío se resta presión ambiente cero.'),('cv','Fv/2.40','m/s','Velocidad efectiva de vacío.'),('Ispv','cv/9.80665','s','Impulso específico de vacío.')]
}
for key,r in rows.items():
 body,_=numeric_steps([dict(target=k,expression=e,unit=u,why=w) for k,e,u,w in r])
 (book/'solutions/generated'/(key+'.tex')).write_text(r'\textbf{Operaciones para comparar ambos casos.}'+'\n'+body+'\n')
 f=book/'latex'/('c01.tex' if key=='M01' else 'c02.tex');s=f.read_text();a=s.index(r'\begin{studiumworked}{'+key);b=s.index(r'\end{studiumworked}',a);token=r'\input{../solutions/generated/'+key+'.tex}'
 if token not in s[a:b]:s=s[:b]+token+'\n'+s[b:]
 f.write_text(s)
