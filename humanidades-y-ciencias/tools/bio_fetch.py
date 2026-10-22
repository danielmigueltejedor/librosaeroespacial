import sys; sys.path.insert(0,'.')
from wp import wp
import time
ES=['Célula','Membrana celular','Respiración celular','ADN','Replicación del ADN','Código genético','Principio de Hardy-Weinberg','Leyes de Mendel']
EN=['Cell (biology)','Cell membrane','Cellular respiration','DNA','DNA replication','Genetic code','Hardy–Weinberg principle','Mendelian inheritance']
for lang,L in (('es',ES),('en',EN)):
    for t in L:
        try: print(wp(lang,t))
        except Exception as e: print('ERR',lang,t,e)
        time.sleep(1.5)
