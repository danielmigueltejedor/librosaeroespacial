import urllib.parse
def S(lang, title, file, label=None, host=None):
    host = host or f'{lang}.wikipedia.org'
    path = urllib.parse.quote(title.replace(' ', '_'), safe="_()',-")
    return dict(title=f'{label or title} — Wikipedia ({lang})' if 'wikipedia' in host else f'{label or title} — Wikisource ({lang})', url=f'https://{host}/wiki/' + path, file=file)
SOURCES = {
 'es_reyes': S('es','Reyes Católicos','es_Reyes_Cat_licos.txt'),
 'en_catolicos': S('en','Catholic Monarchs of Spain','en_Catholic_Monarchs.txt'),
 'es_granada': S('es','Guerra de Granada','es_Guerra_de_Granada.txt'),
 'en_granada': S('en','Granada War','en_Granada_War.txt'),
 'es_edicto': S('es','Edicto de Granada','es_Decreto_de_la_Alhambra.txt'),
 'en_alhambra': S('en','Alhambra Decree','en_Alhambra_Decree.txt'),
 'es_inquisicion': S('es','Inquisición española','es_Inquisici_n_espa_ola.txt'),
 'en_inquisition': S('en','Spanish Inquisition','en_Spanish_Inquisition.txt'),
 'ws_capitulaciones': S('es','Capitulaciones de Santa Fe','ws_es_Capitulaciones_de_Santa_Fe.txt', host='es.wikisource.org'),
 'es_tordesillas': S('es','Tratado de Tordesillas','es_Tratado_de_Tordesillas.txt'),
 'en_tordesillas': S('en','Treaty of Tordesillas','en_Treaty_of_Tordesillas.txt'),
 'es_carlos1': S('es','Carlos I de España','es_Carlos_I_de_Espa_a.txt'),
 'en_carlos5': S('en','Charles V, Holy Roman Emperor','en_Charles_V_Holy_Roman_Emperor.txt'),
 'es_comunidades': S('es','Guerra de las Comunidades de Castilla','es_Guerra_de_las_Comunidades_de_Castilla.txt'),
 'en_comuneros': S('en','Revolt of the Comuneros','en_Revolt_of_the_Comuneros.txt'),
 'es_felipe2': S('es','Felipe II de España','es_Felipe_II_de_Espa_a.txt'),
 'en_felipe2': S('en','Philip II of Spain','en_Philip_II_of_Spain.txt'),
 'es_lepanto': S('es','Batalla de Lepanto','es_Batalla_de_Lepanto.txt'),
 'en_lepanto': S('en','Battle of Lepanto','en_Battle_of_Lepanto.txt'),
 'es_armada': S('es','Armada Invencible','es_Armada_Invencible.txt'),
 'en_armada': S('en','Spanish Armada','en_Spanish_Armada.txt'),
 'es_casa': S('es','Casa de la Contratación de Indias','es_Casa_de_Contrataci_n_de_Indias.txt'),
 'en_casa': S('en','Casa de Contratación','en_Casa_de_Contrataci_n.txt'),
 'es_consejo_indias': S('es','Consejo de Indias','es_Consejo_de_Indias.txt'),
 'en_consejo_indias': S('en','Council of the Indies','en_Council_of_the_Indies.txt'),
 'es_imperio': S('es','Imperio español','es_Imperio_espa_ol.txt'),
 'en_imperio': S('en','Spanish Empire','en_Spanish_Empire.txt'),
 'es_moriscos': S('es','Expulsión de los moriscos','es_Expulsi_n_de_los_moriscos.txt'),
 'en_moriscos': S('en','Expulsion of the Moriscos','en_Expulsion_of_the_Moriscos.txt'),
 'es_olivares': S('es','Conde-duque de Olivares','es_Gaspar_de_Guzm_n_conde_duque_de_Olivares.txt'),
 'en_olivares': S('en','Gaspar de Guzmán, Count-Duke of Olivares','en_Gaspar_de_Guzm_n_Count_Duke_of_Olivares.txt'),
 'es_pirineos': S('es','Tratado de los Pirineos','es_Paz_de_los_Pirineos.txt'),
 'en_pirineos': S('en','Treaty of the Pyrenees','en_Peace_of_the_Pyrenees.txt'),
 'es_carlos2': S('es','Carlos II de España','es_Carlos_II_de_Espa_a.txt'),
 'en_carlos2': S('en','Charles II of Spain','en_Charles_II_of_Spain.txt'),
 'es_sucesion': S('es','Guerra de sucesión española','es_Guerra_de_sucesi_n_espa_ola.txt'),
 'en_sucesion': S('en','War of the Spanish Succession','en_War_of_the_Spanish_Succession.txt'),
 'es_nueva_planta': S('es','Decretos de Nueva Planta','es_Decretos_de_Nueva_Planta.txt'),
 'en_nueva_planta': S('en','Nueva Planta decrees','en_Nueva_Planta_decrees.txt'),
 'es_utrecht': S('es','Tratado de Utrecht','es_Tratado_de_Utrecht.txt'),
 'en_utrecht': S('en','Peace of Utrecht','en_Treaty_of_Utrecht.txt'),
}
BLUEPRINT = [
 ('hist-01', 'Los Reyes Católicos: unión dinástica, Granada y 1492'),
 ('hist-02', 'Carlos I: Comunidades e Imperio'),
 ('hist-03', 'Felipe II: guerras, finanzas y Armada'),
 ('hist-04', 'El Imperio americano y su administración'),
 ('hist-05', 'Los Austrias del siglo XVII: moriscos, Olivares y declive'),
 ('hist-06', 'La Guerra de Sucesión y la Nueva Planta'),
]
CHAPTERS = {}
spec = dict(book='historia-moderna-espana', sources=SOURCES, blueprint=BLUEPRINT, chapters=CHAPTERS, audit_kind='historical')
