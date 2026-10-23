#!/usr/bin/env python3
"""Cambia en los simulacros 2 y 3 de Motores Cohete los problemas S2.2, S2.4, S3.2 y S3.4.

Antes repetían, con otras cifras, el mismo tipo de problema que el simulacro 1.
Reutiliza el formato y las funciones de `author-rocket-problems.py`.
"""
from pathlib import Path
import importlib.util
import json
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
spec_ = importlib.util.spec_from_file_location('rocket_problems', ROOT / 'scripts/author-rocket-problems.py')
rp = importlib.util.module_from_spec(spec_)
spec_.loader.exec_module(rp)
BOOK = rp.BOOK
X = {}


def exam(key, *args):
    rp.P.clear()
    rp.spec(key, *args)
    X[key] = rp.P[key]


exam('S2.2', 'Motor sólido: impulso, masa final y relación empuje-peso',
 r'Un motor sólido quema $260\,\mathrm{kg}$ de propulsante en $38\,\mathrm s$ con $I_{sp}=262\,\mathrm s$. La masa inerte del motor y la carga útil suman $175\,\mathrm{kg}$. Calcule el gasto medio, el empuje medio, el impulso total, la velocidad ideal y la relación empuje-peso en el encendido con la masa inicial.',
 r'$m_p=260\,\mathrm{kg}$; $t_b=38\,\mathrm s$; $I_{sp}=262\,\mathrm s$; masa inerte y carga útil $175\,\mathrm{kg}$.',
 r'Gasto, empuje, impulso, $\Delta v$ y $F/W$.',
 r'Gasto y empuje constantes; $I_{sp}$ constante; sin gravedad ni resistencia en el $\Delta v$.',
 r'Ecuación del cohete y empuje medio.',
 [r'\dot m=m_p/t_b,\quad F=I_{sp}g_0\dot m,\quad I=Ft_b',
  r'\Delta v=I_{sp}g_0\ln\frac{m_p+m_i}{m_i},\quad F/W=F/[(m_p+m_i)g_0]'],
 [r'El gasto es $%(md)s\,\mathrm{kg/s}$ y el empuje $%(F)s\,\mathrm N$; el impulso es $%(I)s\,\mathrm{N\,s}$.',
  r'La velocidad ideal es $%(dv)s\,\mathrm{m/s}$ y la relación empuje-peso inicial $%(tw)s$.'],
 [('md', '260/38', 'kg/s', 'Gasto medio.'),
  ('F', '262*9.80665*md', 'N', 'Empuje medio.'),
  ('I', 'F*38', 'N*s', 'Impulso total.'),
  ('dv', '262*9.80665*log((260+175)/175)', 'm/s', 'Velocidad ideal.'),
  ('tw', 'F/((260+175)*9.80665)', '', 'Relación empuje-peso con la masa inicial.')],
 r'$\dot m=%(md)s\,\mathrm{kg/s}$; $F=%(F)s\,\mathrm N$; $I=%(I)s\,\mathrm{N\,s}$; $\Delta v=%(dv)s\,\mathrm{m/s}$; $F/W=%(tw)s$.',
 r'Una relación empuje-peso mayor que 1 permite despegar en vertical; el valor medio oculta que el empuje real varía con la forma del grano y el peso baja mientras se quema.',
 r'$I/(m_pg_0)$ devuelve $I_{sp}=262\,\mathrm s$. Con $m_p\to0$ la velocidad ideal tiende a 0.',
 r'No se modelan la forma de la curva empuje-tiempo, la gravedad ni la resistencia, que reducen la velocidad real.')

exam('S3.2', 'Presión máxima admisible y radio de perforación límite',
 r'La carcasa de un motor sólido admite una presión máxima de funcionamiento de $8.5\,\mathrm{MPa}$. El grano tiene perforación cilíndrica de $1.2\,\mathrm m$ de longitud, $\rho_p=1760\,\mathrm{kg/m^3}$, $r_{ref}=7.0\,\mathrm{mm/s}$ a $6\,\mathrm{MPa}$, $n=0.33$, $c^*=1480\,\mathrm{m/s}$ y garganta de $0.0014\,\mathrm{m^2}$. Calcule el cociente de áreas máximo y el radio de perforación máximo admisible, y la presión si la perforación llega a $0.10\,\mathrm m$.',
 r'$p_{max}=8.5\,\mathrm{MPa}$; $L=1.2\,\mathrm m$; $\rho_p=1760\,\mathrm{kg/m^3}$; $r_{ref}=7.0\,\mathrm{mm/s}$ a $6\,\mathrm{MPa}$; $n=0.33$; $c^*=1480\,\mathrm{m/s}$; $A_t=0.0014\,\mathrm{m^2}$.',
 r'$K_{n,max}$, $r_{p,max}$ y presión con $r_p=0.10\,\mathrm m$.',
 r'Equilibrio cuasiestacionario; $A_b=2\pi r_pL$; $c^*$ constante; sin erosión.',
 r'Inversión de la presión de equilibrio.',
 [r'p_c=p_{ref}\left[\rho_pr_{ref}c^*K_n/p_{ref}\right]^{1/(1-n)}',
  r'K_{n,max}=\frac{p_{ref}}{\rho_pr_{ref}c^*}\left(\frac{p_{max}}{p_{ref}}\right)^{1-n},\quad r_{p,max}=\frac{K_{n,max}A_t}{2\pi L}'],
 [r'Se obtiene $K_{n,max}=%(Kmax)s$ y $r_{p,max}=%(rpmax)s\,\mathrm m$.',
  r'Para $r_p=0.10\,\mathrm m$, $K_n=%(Kn)s$ y la presión es $%(pc)s\,\mathrm{Pa}$, es decir, $%(frac)s\,\%%$ del máximo.'],
 [('Kmax', '6e6/(1760*.007*1480)*(8.5e6/6e6)**(1-.33)', '', 'Cociente de áreas máximo.'),
  ('rpmax', 'Kmax*.0014/(2*pi*1.2)', 'm', 'Radio máximo de perforación.'),
  ('Kn', '2*pi*.10*1.2/.0014', '', 'Cociente de áreas con perforación de 0.10 m.'),
  ('pc', '6e6*(1760*.007*1480*Kn/6e6)**(1/(1-.33))', 'Pa', 'Presión con ese radio.'),
  ('frac', 'pc/8.5e6*100', '', 'Cociente en por ciento respecto al máximo.')],
 r'$K_{n,max}=%(Kmax)s$; $r_{p,max}=%(rpmax)s\,\mathrm m$; con $r_p=0.10\,\mathrm m$, $p_c=%(pc)s\,\mathrm{Pa}$ ($%(frac)s\,\%%$ del máximo).',
 r'Si la presión supera el máximo con un radio de $0.10\,\mathrm m$, el grano debe diseñarse con menos superficie o una garganta mayor; el resultado muestra hasta dónde puede avanzar la perforación.',
 r'Con $r_p=r_{p,max}$ la presión vuelve a $8.5\,\mathrm{MPa}$. El cociente supera el $100\,\%%$ si $r_p>r_{p,max}$.',
 r'No se añade margen de seguridad estructural ni el aumento transitorio de presión del encendido; el máximo admisible es un dato.')

exam('S2.4', 'Maniobra con propulsor Hall: propulsante y tiempo',
 r'Un satélite de $900\,\mathrm{kg}$ necesita $\Delta v=450\,\mathrm{m/s}$ con un propulsor Hall de $1350\,\mathrm W$, rendimiento $0.55$ e $I_{sp}=1800\,\mathrm s$. Calcule la velocidad de escape, el propulsante necesario, el empuje, el gasto y el tiempo de maniobra con empuje constante.',
 r'$m_0=900\,\mathrm{kg}$; $\Delta v=450\,\mathrm{m/s}$; $P=1350\,\mathrm W$; $\eta=0.55$; $I_{sp}=1800\,\mathrm s$.',
 r'$v_e$, $m_p$, $F$, $\dot m$ y tiempo.',
 r'Potencia, rendimiento e $I_{sp}$ constantes; sin fuerzas externas; empuje en la dirección del movimiento.',
 r'Ecuación del cohete y potencia del chorro.',
 [r'v_e=I_{sp}g_0,\quad m_p=m_0(1-e^{-\Delta v/v_e})',
  r'F=2\eta P/v_e,\quad \dot m=F/v_e,\quad t=m_p/\dot m'],
 [r'La velocidad de escape es $%(ve)s\,\mathrm{m/s}$ y el propulsante $%(mp)s\,\mathrm{kg}$.',
  r'El empuje es $%(F)s\,\mathrm N$, el gasto $%(md)s\,\mathrm{kg/s}$ y el tiempo $%(t)s\,\mathrm s$, es decir, $%(dias)s$ días.'],
 [('ve', '1800*9.80665', 'm/s', 'Velocidad de escape.'),
  ('mp', '900*(1-exp(-450/ve))', 'kg', 'Propulsante por la ecuación del cohete.'),
  ('F', '2*.55*1350/ve', 'N', 'Empuje de potencia de chorro.'),
  ('md', 'F/ve', 'kg/s', 'Gasto.'),
  ('t', 'mp/md', 's', 'Tiempo de maniobra.'),
  ('dias', 't/86400', 'd', 'Tiempo en días.')],
 r'$v_e=%(ve)s\,\mathrm{m/s}$; $m_p=%(mp)s\,\mathrm{kg}$; $F=%(F)s\,\mathrm N$; $t=%(t)s\,\mathrm s$ ($%(dias)s$ días).',
 r'La maniobra consume pocos kilogramos de propulsante pero dura semanas; la solución solo es válida si el satélite puede mantener la potencia disponible durante ese tiempo.',
 r'$F\,t$ dividido entre $m_0$ da una velocidad algo menor que $450\,\mathrm{m/s}$ porque ignora la pérdida de masa.',
 r'No se consideran eclipses, la orientación de los paneles ni el empuje fuera de la dirección del movimiento.')

exam('S3.4', 'Varios propulsores iónicos: empuje, potencia y paneles',
 r'Un remolcador necesita $0.30\,\mathrm N$ de empuje con propulsores iónicos idénticos que, cada uno, consumen $2.5\,\mathrm{kW}$ con rendimiento $0.65$ y escape de $30000\,\mathrm{m/s}$. Calcule el empuje de un propulsor, cuántos hacen falta, la potencia total, el gasto total y el área de panel si la potencia específica es $150\,\mathrm{W/m^2}$.',
 r'$F_{req}=0.30\,\mathrm N$; $P_1=2.5\,\mathrm{kW}$; $\eta=0.65$; $v_e=30000\,\mathrm{m/s}$; $150\,\mathrm{W/m^2}$.',
 r'$F_1$, número de propulsores, $P$ total, gasto y área.',
 r'Propulsores idénticos con empuje aditivo; potencia y rendimiento constantes; toda la potencia va a los propulsores.',
 r'Potencia de chorro por propulsor y suma.',
 [r'F_1=2\eta P_1/v_e,\quad N=\lceil F_{req}/F_1\rceil',
  r'P=NP_1,\quad \dot m=NF_1/v_e,\quad A=P/p_{esp}'],
 [r'Un propulsor da $%(F1)s\,\mathrm N$ y el cociente $F_{req}/F_1=%(nex)s$ obliga a usar $3$ propulsores.',
  r'La potencia total es $%(P)s\,\mathrm W$, el gasto $%(md)s\,\mathrm{kg/s}$ y el panel tiene $%(A)s\,\mathrm{m^2}$.'],
 [('F1', '2*.65*2500/30000', 'N', 'Empuje de un propulsor.'),
  ('nex', '.30/F1', '', 'Número de propulsores necesario sin redondear.'),
  ('F3', '3*F1', 'N', 'Empuje con tres propulsores.'),
  ('P', '3*2500', 'W', 'Potencia total.'),
  ('md', 'F3/30000', 'kg/s', 'Gasto con tres propulsores.'),
  ('A', 'P/150', 'm**2', 'Área de panel.')],
 r'$F_1=%(F1)s\,\mathrm N$; $N=3$; $F=%(F3)s\,\mathrm N$; $P=%(P)s\,\mathrm W$; $A=%(A)s\,\mathrm{m^2}$.',
 r'El número se redondea hacia arriba y el empuje real supera el requerido; con tres propulsores se necesita un panel grande, que domina la masa del sistema.',
 r'El cociente $F_{req}/F_1$ es menor que 3 y mayor que 2, de modo que 3 es el mínimo entero.',
 r'No se incluyen la potencia de los demás sistemas, la degradación del panel ni el funcionamiento a potencia parcial.')


def replace_all() -> None:
    path = BOOK / 'latex/simulacros.tex'
    text = path.read_text()
    reports = []
    for key, d in X.items():
        d_ = d
        keynum = key
        rp.LEVEL_OVERRIDE = 'De examen'
        rows = [dict(target=k, expression=e, unit=u, why=w) for k, e, u, w in d_['steps']]
        body, checks = rp.numeric_steps(rows)
        values = {c['target']: rp.number(c['value'], 6) for c in checks}
        (BOOK / 'solutions/generated' / f'{key}.tex').write_text(body + '\n')
        fill = lambda s: s % values
        development = '\n'.join(r'\item ' + fill(x) for x in d_['development'])
        equations = '\n'.join(r'\[' + e + r'\]' for e in d_['equations'])
        solution = (f'\\section{{{key}. {d_["title"]}}}\n'
                    f'\\begin{{studiumworked}}{{{key}. {d_["title"]} · De examen}}\n'
                    f'\\textbf{{Enunciado.}} {d_["statement"]}\n\n'
                    f'\\textbf{{Datos.}} {d_["data"]}\n\n'
                    f'\\textbf{{Incógnitas.}} {d_["unknown"]}\n\n'
                    f'\\textbf{{Hipótesis.}} {d_["hypotheses"]}\n\n'
                    f'\\textbf{{Modelo físico.}} {d_["model"]}\n{equations}\n'
                    f'\\textbf{{Desarrollo.}}\n\\begin{{enumerate}}\n{development}\n\\end{{enumerate}}\n'
                    f'\\textbf{{Operaciones para contrastar el cálculo.}}\n\\input{{../solutions/generated/{key}.tex}}\n'
                    f'\\textbf{{Resultados.}} {fill(d_["results"])}\n\n'
                    f'\\textbf{{Interpretación.}} {fill(d_["interpretation"])}\n\n'
                    f'\\textbf{{Comprobación.}} {fill(d_["check"])}\n\n'
                    f'\\textbf{{Límites.}} {fill(d_["limits"])}\n'
                    f'\\end{{studiumworked}}\n')
        statement = f'\\section{{{key}. {d_["title"]} · 2 puntos}}\n{d_["statement"]}\n\n'
        k = re.escape(key)
        stm = re.compile(r'\\section\{' + k + r'\. [^\n]*? · 2 puntos\}\n.*?(?=\\section\{)', re.S)
        sol = re.compile(r'\\section\{' + k + r'\. (?:(?!· 2 puntos)[^\n])*\}\n\\begin\{studiumworked\}.*?\\end\{studiumworked\}\n', re.S)
        if not stm.search(text) or not sol.search(text):
            raise SystemExit(f'No se encuentra {key}')
        text = stm.sub(lambda m: statement, text, count=1)
        text = sol.sub(lambda m: solution, text, count=1)
        reports.append(dict(problem=key, steps=checks))
    path.write_text(text)
    (BOOK / 'reports/exam-problem-rewrite-procedures.json').write_text(json.dumps(
        dict(scope='Original numeric exam data and authored derivations; no independent approval',
             records=reports), ensure_ascii=False, indent=2) + '\n')
    print('problemas de simulacro reescritos:', ', '.join(X))


if __name__ == '__main__':
    replace_all()
