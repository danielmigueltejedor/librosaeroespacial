import urllib.parse
def S(lang, title, file, label=None):
    path = urllib.parse.quote(title.replace(' ', '_'), safe="_()',-")
    return dict(title=f'{label or title} — Wikipedia ({lang})', url=f'https://{lang}.wikipedia.org/wiki/' + path, file=file)
def N(slug, label, file):
    return dict(title=f'{label} — NHGRI Talking Glossary', url=f'https://www.genome.gov/genetics-glossary/{slug}', file=file, kind='glossary', authors='National Human Genome Research Institute')
SOURCES = {
 'es_celula': S('es','Célula','es_C_lula.txt'),
 'es_teoria_celular': S('es','Teoría celular','es_Teor_a_celular.txt'),
 'en_cell': S('en','Cell (biology)','en_Cell_biology_.txt'),
 'nhgri_cell': N('Cell','Cell','nhgri_Cell.txt'),
 'es_membrana': S('es','Membrana celular','es_Membrana_celular.txt'),
 'en_membrane': S('en','Cell membrane','en_Cell_membrane.txt'),
 'es_bomba': S('es','Bomba de sodio-potasio','es_Bomba_de_sodio_potasio.txt'),
 'en_pump': S('en','Na+/K+-ATPase','en_Na_K_ATPase.txt'),
 'es_nernst': S('es','Ecuación de Nernst','es_Ecuaci_n_de_Nernst.txt'),
 'en_nernst': S('en','Nernst equation','en_Nernst_equation.txt'),
 'es_respiracion': S('es','Respiración celular','es_Respiraci_n_celular.txt'),
 'en_respiration': S('en','Cellular respiration','en_Cellular_respiration.txt'),
 'es_atp': S('es','Adenosín trifosfato','es_Adenos_n_trifosfato.txt'),
 'en_atp': S('en','Adenosine triphosphate','en_Adenosine_triphosphate.txt'),
 'es_mitocondria': S('es','Mitocondria','es_Mitocondria.txt'),
 'en_mitochondrion': S('en','Mitochondrion','en_Mitochondrion.txt'),
 'nhgri_mito': N('Mitochondria','Mitochondria','nhgri_Mitochondria.txt'),
 'es_adn': S('es','ADN','es_ADN.txt'),
 'en_dna': S('en','DNA','en_DNA.txt'),
 'es_replicacion': S('es','Replicación del ADN','es_Replicaci_n_del_ADN.txt'),
 'en_replication': S('en','DNA replication','en_DNA_replication.txt'),
 'nhgri_replication': N('DNA-Replication','DNA Replication','nhgri_DNA_Replication.txt'),
 'es_cromosoma': S('es','Cromosoma','es_Cromosoma.txt'),
 'en_chromosome': S('en','Chromosome','en_Chromosome.txt'),
 'nhgri_chromosome': N('Chromosome','Chromosome','nhgri_Chromosome.txt'),
 'es_codigo': S('es','Código genético','es_C_digo_gen_tico.txt'),
 'en_code': S('en','Genetic code','en_Genetic_code.txt'),
 'nhgri_codon': N('Codon','Codon','nhgri_Codon.txt'),
 'nhgri_code': N('Genetic-Code','Genetic Code','nhgri_Genetic_Code.txt'),
 'nhgri_translation': N('Translation','Translation','nhgri_Translation.txt'),
 'nhgri_transcription': N('Transcription','Transcription','nhgri_Transcription.txt'),
 'es_mendel': S('es','Leyes de Mendel','es_Leyes_de_Mendel.txt'),
 'en_mendel': S('en','Mendelian inheritance','en_Mendelian_inheritance.txt'),
 'es_hw': S('es','Principio de Hardy-Weinberg','es_Principio_de_Hardy_Weinberg.txt'),
 'en_hw': S('en','Hardy–Weinberg principle','en_Hardy_Weinberg_principle.txt'),
 'nhgri_allele': N('Allele','Allele','nhgri_Allele.txt'),
 'nhgri_dominant': N('Dominant','Dominant Traits and Alleles','nhgri_Dominant.txt'),
 'nhgri_recessive': N('Recessive','Recessive Traits and Alleles','nhgri_Recessive.txt'),
}
BLUEPRINT = [
 ('bio-01', 'La célula como unidad de la vida'),
 ('bio-02', 'La membrana plasmática y el transporte de iones'),
 ('bio-03', 'Energía celular: ATP, mitocondrias y respiración'),
 ('bio-04', 'El ADN y su replicación'),
 ('bio-05', 'El código genético y la síntesis de proteínas'),
 ('bio-06', 'Herencia mendeliana y genética de poblaciones'),
 ('bio-07', 'Ciclo celular, mitosis, meiosis y cáncer'),
 ('bio-08', 'Regulación de la expresión génica y epigenética'),
 ('bio-09', 'Mutación, selección natural y evolución'),
 ('bio-10', 'Fotosíntesis'),
 ('bio-11', 'Biotecnología: PCR, clonación y CRISPR'),
 ('bio-12', 'Taller de diseño experimental y análisis de datos'),
]
CHAPTERS = {}
spec = dict(book='biologia-celular-molecular', sources=SOURCES, blueprint=BLUEPRINT, chapters=CHAPTERS, audit_kind='scientific')
