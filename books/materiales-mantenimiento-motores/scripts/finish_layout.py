from pathlib import Path
R=Path(__file__).resolve().parents[1]
p=R/'latex/preamble.tex';s=p.read_text();s=s.replace(r'\usepackage{amsmath,',r'\usepackage{needspace}'+'\n'+r'\usepackage{amsmath,') if r'\usepackage{needspace}' not in s else s;p.write_text(s)
# Evitar finales de capítulo de solo una caja o unas líneas de fuentes.
for n,title in [(5,'Relajación bajo deformación impuesta'),(9,'Sándwich, GLARE y uniones adhesivas'),(11,'Ensayar una propiedad y decidir aceptación'),(23,'Configuración y misión')]:
 p=R/'content'/f'e{n:02d}.tex';s=p.read_text();needle=r'\section{'+title+'}'
 if r'\Needspace' not in s:s=s.replace(needle,r'\Needspace{.48\textheight}'+'\n'+needle)
 p.write_text(s)
# La referencia al manual ya aparece en la introducción; no necesita página propia.
p=R/'work/montar_cuadernos.py';s=p.read_text();s=s.replace(" s+=r'\\section{'+c['key']+'. '+c['title']+'}\\n'"," s+=r'\\Needspace{.36\\textheight}'+r'\\section{'+c['key']+'. '+c['title']+'}\\n'")
a=s.index("s+=r'\\backmatter\\chapter*{Referencia al manual}");b=s.index("(R/'problemas.tex').write_text(s)",a)
s=s[:a]+"s+=r'\\end{document}'\n"+s[b:]
p.write_text(s)
