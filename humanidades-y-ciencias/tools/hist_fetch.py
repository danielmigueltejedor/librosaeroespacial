import sys; sys.path.insert(0,'.')
from wp import wp
import time
ES=['Reyes Católicos','Guerra de Granada','Decreto de la Alhambra','Tratado de Tordesillas','Carlos I de España','Guerra de las Comunidades de Castilla','Felipe II de España','Batalla de Lepanto','Armada Invencible','Casa de Contratación','Expulsión de los moriscos','Gaspar de Guzmán, conde-duque de Olivares','Paz de los Pirineos','Carlos II de España','Guerra de sucesión española','Decretos de Nueva Planta','Imperio español','Inquisición española']
EN=['Catholic Monarchs','Granada War','Alhambra Decree','Treaty of Tordesillas','Charles V, Holy Roman Emperor','Revolt of the Comuneros','Philip II of Spain','Battle of Lepanto','Spanish Armada','House of Trade of the Indies','Expulsion of the Moriscos','Gaspar de Guzmán, Count-Duke of Olivares','Peace of the Pyrenees','Charles II of Spain','War of the Spanish Succession','Nueva Planta decrees','Spanish Empire','Spanish Inquisition']
for lang,L in (('es',ES),('en',EN)):
    for t in L:
        try: print(wp(lang,t))
        except Exception as e: print('ERR',lang,t,e)
        time.sleep(1.5)
