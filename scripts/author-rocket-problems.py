#!/usr/bin/env python3
"""Sustituye P13 a P18 y P25 a P30 de Motores Cohete por problemas distintos entre sí.

Antes eran seis variantes del mismo problema con cifras casi iguales. Cada nueva
entrada declara datos, modelo, operaciones (calculadas con solution_steps.py),
interpretación y límites. Aritmética de ejercicios originales, sin revisión académica.
"""
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from solution_steps import numeric_steps, number  # noqa: E402

BOOK = ROOT / 'books/motores-cohete'
LEVEL = ['Básico', 'Básico', 'Intermedio', 'Intermedio', 'Avanzado', 'De examen']
G0 = '9.80665'
P = {}


def spec(key, title, statement, data, unknown, hypotheses, model, equations, development, steps,
         results, interpretation, check, limits):
    P[key] = dict(title=title, statement=statement, data=data, unknown=unknown, hypotheses=hypotheses,
                  model=model, equations=equations, development=development, steps=steps,
                  results=results, interpretation=interpretation, check=check, limits=limits)


# ------------------------------------------------------------------ sólidos
spec('P13', 'Presión de cámara en equilibrio de un grano',
 r'Un grano de propulsante sólido tiene densidad $1750\,\mathrm{kg/m^3}$ y velocidad de regresión $8.0\,\mathrm{mm/s}$ a $6.9\,\mathrm{MPa}$, con exponente $n=0.35$. La velocidad característica es $c^*=1520\,\mathrm{m/s}$, el área de garganta $0.0030\,\mathrm{m^2}$ y el área de combustión $0.72\,\mathrm{m^2}$. Calcule la presión de cámara de equilibrio, la velocidad de regresión y el gasto, comprobando éste por las dos vías.',
 r'Densidad: $1750\,\mathrm{kg/m^3}$; $r_{ref}=8.0\,\mathrm{mm/s}$ a $p_{ref}=6.9\,\mathrm{MPa}$; $n=0.35$; $c^*=1520\,\mathrm{m/s}$; $A_t=0.0030\,\mathrm{m^2}$; $A_b=0.72\,\mathrm{m^2}$.',
 r'Presión de cámara, velocidad de regresión y gasto.',
 r'Régimen cuasiestacionario y descarga ahogada; ley de Saint-Robert con coeficiente constante; $c^*$ constante y sin erosión.',
 r'Equilibrio entre masa generada y masa descargada.',
 [r'\rho_pA_br_{ref}(p_c/p_{ref})^n=p_cA_t/c^*',
  r'K_n=A_b/A_t,\quad p_c=p_{ref}\left[\rho_pr_{ref}c^*K_n/p_{ref}\right]^{1/(1-n)}',
  r'r=r_{ref}(p_c/p_{ref})^n,\quad \dot m=\rho_pA_br=p_cA_t/c^*'],
 [r'Se calcula $K_n=%(Kn)s$ y el parámetro $\rho_pr_{ref}c^*K_n/p_{ref}=%(w)s$.',
  r'Se eleva a $1/(1-n)$ para obtener $p_c=%(pc)s\,\mathrm{Pa}$.',
  r'La velocidad es $r=%(r)s\,\mathrm{m/s}$ y el gasto generado $\rho_pA_br=%(m1)s\,\mathrm{kg/s}$, igual al descargado $p_cA_t/c^*=%(m2)s\,\mathrm{kg/s}$.'],
 [('Kn', '.72/.0030', '', 'Cociente de áreas de combustión y garganta.'),
  ('w', '1750*.008*1520*Kn/6.9e6', '', 'Parámetro adimensional del equilibrio.'),
  ('pc', '6.9e6*w**(1/(1-.35))', 'Pa', 'Presión de cámara de equilibrio.'),
  ('r', '.008*(pc/6.9e6)**.35', 'm/s', 'Velocidad de regresión a esa presión.'),
  ('m1', '1750*.72*r', 'kg/s', 'Gasto generado por la superficie.'),
  ('m2', 'pc*.0030/1520', 'kg/s', 'Gasto descargado por la garganta.')],
 r'$p_c=%(pc)s\,\mathrm{Pa}$; $r=%(r)s\,\mathrm{m/s}$; $\dot m=%(m1)s\,\mathrm{kg/s}$.',
 r'La presión queda por debajo de la de referencia porque $K_n$ es menor que el valor que daría $6.9\,\mathrm{MPa}$; con $n<1$ el equilibrio es estable frente a pequeñas perturbaciones de presión.',
 r'Los dos gastos coinciden. Si $n\geq1$ no existe equilibrio estable, y para $K_n$ mayor sube la presión.',
 r'No se incluyen el transitorio de encendido, la erosión de la garganta ni la variación del exponente con la presión. Un $n$ local no garantiza estabilidad acústica.')

spec('P14', 'Grano de combustión frontal: duración, impulso y velocidad ideal',
 r'Un grano cilíndrico de combustión frontal tiene $1.10\,\mathrm m$ de longitud, $0.30\,\mathrm m$ de diámetro y densidad $1780\,\mathrm{kg/m^3}$ y arde a $7.2\,\mathrm{mm/s}$ constante. El motor entrega $I_{sp}=240\,\mathrm s$. La masa inerte del vehículo con la carga útil es $90\,\mathrm{kg}$. Calcule duración, gasto, empuje, impulso total y velocidad ideal.',
 r'$L=1.10\,\mathrm m$; $D=0.30\,\mathrm m$; $\rho_p=1780\,\mathrm{kg/m^3}$; $r=7.2\,\mathrm{mm/s}$; $I_{sp}=240\,\mathrm s$; masa inerte $90\,\mathrm{kg}$.',
 r'Duración, gasto, empuje, impulso total y $\Delta v$.',
 r'Combustión frontal con superficie constante; empuje y $I_{sp}$ constantes; sin fuerzas externas.',
 r'Grano neutro y ecuación del cohete.',
 [r'A_b=\pi D^2/4,\quad t_b=L/r,\quad \dot m=\rho_pA_br',
  r'F=I_{sp}g_0\dot m,\quad I=Ft_b=I_{sp}g_0m_p',
  r'\Delta v=I_{sp}g_0\ln\frac{m_p+m_i}{m_i}'],
 [r'La superficie es $A_b=%(Ab)s\,\mathrm{m^2}$ y la duración $t_b=%(tb)s\,\mathrm s$.',
  r'El gasto es $%(md)s\,\mathrm{kg/s}$ y el empuje $%(F)s\,\mathrm N$, con propulsante $m_p=%(mp)s\,\mathrm{kg}$.',
  r'El impulso es $%(I)s\,\mathrm{N\,s}$ y la velocidad ideal $%(dv)s\,\mathrm{m/s}$.'],
 [('Ab', 'pi*.30**2/4', 'm**2', 'Superficie de combustión constante.'),
  ('tb', '1.10/.0072', 's', 'Duración del quemado.'),
  ('md', '1780*Ab*.0072', 'kg/s', 'Gasto másico.'),
  ('F', '240*9.80665*md', 'N', 'Empuje con impulso específico dado.'),
  ('mp', '1780*Ab*1.10', 'kg', 'Masa de propulsante.'),
  ('I', 'F*tb', 'N*s', 'Impulso total.'),
  ('Ispc', 'I/(mp*9.80665)', 's', 'Comprobación del impulso específico.'),
  ('dv', '240*9.80665*log((mp+90)/90)', 'm/s', 'Velocidad ideal de la ecuación del cohete.')],
 r'$t_b=%(tb)s\,\mathrm s$; $\dot m=%(md)s\,\mathrm{kg/s}$; $F=%(F)s\,\mathrm N$; $I=%(I)s\,\mathrm{N\,s}$; $\Delta v=%(dv)s\,\mathrm{m/s}$.',
 r'Un grano frontal da empuje constante, pero su longitud limita la duración a $L/r$; para empujes mayores se necesita más superficie, con perforación interior.',
 r'$I/(m_pg_0)$ recupera $I_{sp}=240\,\mathrm s$. La velocidad ideal es una cota: no incluye gravedad, resistencia ni la masa de la carcasa que se consume.',
 r'Se desprecian el transitorio, la erosión y la variación de $I_{sp}$ con la presión; la velocidad de regresión se toma constante.')

spec('P15', 'Perforación cilíndrica: presión al inicio y al final',
 r'Un grano de combustión interior tiene longitud $1.4\,\mathrm m$ y radio de perforación que crece de $0.040\,\mathrm m$ a $0.090\,\mathrm m$. La garganta es $0.0016\,\mathrm{m^2}$, el propulsante $1750\,\mathrm{kg/m^3}$, $r_{ref}=6.0\,\mathrm{mm/s}$ a $5\,\mathrm{MPa}$, $n=0.30$ y $c^*=1500\,\mathrm{m/s}$. Calcule la presión de cámara al inicio y al final, su cociente y el cociente de empujes con $C_F$ constante.',
 r'$L=1.4\,\mathrm m$; $r_{p,i}=0.040\,\mathrm m$; $r_{p,f}=0.090\,\mathrm m$; $A_t=0.0016\,\mathrm{m^2}$; $\rho_p=1750\,\mathrm{kg/m^3}$; $r_{ref}=6.0\,\mathrm{mm/s}$ a $5\,\mathrm{MPa}$; $n=0.30$; $c^*=1500\,\mathrm{m/s}$.',
 r'Presiones inicial y final, cociente y cociente de empujes.',
 r'Equilibrio cuasiestacionario en cada instante; $A_b=2\pi r_pL$ (solo la perforación); $C_F$ y $c^*$ constantes; sin erosión.',
 r'Equilibrio con área de combustión variable.',
 [r'A_b=2\pi r_pL,\quad K_n=A_b/A_t',
  r'p_c=p_{ref}\left[\rho_pr_{ref}c^*K_n/p_{ref}\right]^{1/(1-n)}',
  r'F\propto p_c\ \text{con}\ C_F\ \text{y}\ A_t\ \text{constantes}'],
 [r'Con $K_n=%(Kni)s$ al inicio y $%(Knf)s$ al final se obtienen $p_{c,i}=%(pci)s\,\mathrm{Pa}$ y $p_{c,f}=%(pcf)s\,\mathrm{Pa}$.',
  r'El cociente es $p_{c,f}/p_{c,i}=%(rp)s$, igual a $(r_{p,f}/r_{p,i})^{1/(1-n)}$ por la proporcionalidad de $K_n$ con $r_p$: $%(rp2)s$.',
  r'Con $C_F$ y $A_t$ fijos, el empuje crece en el mismo factor.'],
 [('Kni', '2*pi*.040*1.4/.0016', '', 'Cociente de áreas al inicio.'),
  ('Knf', '2*pi*.090*1.4/.0016', '', 'Cociente de áreas al final.'),
  ('wi', '1750*.006*1500*Kni/5e6', '', 'Parámetro adimensional inicial.'),
  ('wf', '1750*.006*1500*Knf/5e6', '', 'Parámetro adimensional final.'),
  ('pci', '5e6*wi**(1/(1-.30))', 'Pa', 'Presión inicial.'),
  ('pcf', '5e6*wf**(1/(1-.30))', 'Pa', 'Presión final.'),
  ('rp', 'pcf/pci', '', 'Cociente de presiones.'),
  ('rp2', '(.090/.040)**(1/(1-.30))', '', 'Comprobación por la proporcionalidad de Kn con el radio.')],
 r'$p_{c,i}=%(pci)s\,\mathrm{Pa}$; $p_{c,f}=%(pcf)s\,\mathrm{Pa}$; $p_{c,f}/p_{c,i}=F_f/F_i=%(rp)s$.',
 r'La perforación cilíndrica es progresiva: la superficie crece y la presión y el empuje aumentan con el tiempo; la envolvente estructural debe dimensionarse para la presión final, no la inicial.',
 r'Los dos cocientes coinciden. Para $r_p$ constante se recupera el cociente 1.',
 r'No se consideran la erosión por flujo cruzado en el conducto, el cambio de $c^*$ con la presión ni la velocidad de regresión transitoria.')

spec('P16', 'Sensibilidad de la presión a la temperatura del grano',
 r'Un propulsante tiene sensibilidad de la velocidad de regresión a la temperatura $\sigma_p=0.0020\,\mathrm{K^{-1}}$ y exponente $n=0.35$. Calcule la sensibilidad de presión $\pi_K$ y los cocientes de presión y de empuje para un grano $+35\,\mathrm K$ y $-20\,\mathrm K$ respecto a la referencia.',
 r'$\sigma_p=0.0020\,\mathrm{K^{-1}}$; $n=0.35$; $\Delta T=+35\,\mathrm K$ y $-20\,\mathrm K$.',
 r'$\pi_K$ y cocientes $p_c/p_{c,ref}$ y $F/F_{ref}$.',
 r'Sensibilidades constantes en el intervalo; $K_n$ y $C_F$ constantes; empuje proporcional a la presión de cámara.',
 r'Sensibilidad exponencial de la presión a la temperatura.',
 [r'\pi_K=\sigma_p/(1-n)',
  r'p_c/p_{c,ref}=e^{\pi_K\Delta T}',
  r'F/F_{ref}=p_c/p_{c,ref}'],
 [r'La sensibilidad de presión es $\pi_K=%(pik)s\,\mathrm{K^{-1}}$.',
  r'Para $+35\,\mathrm K$, el cociente es $%(hot)s$; para $-20\,\mathrm K$, $%(cold)s$.',
  r'El empuje cambia en el mismo factor.'],
 [('pik', '.0020/(1-.35)', '1/K', 'Sensibilidad de presión a la temperatura.'),
  ('hot', 'exp(pik*35)', '', 'Cociente de presiones con grano caliente.'),
  ('cold', 'exp(-pik*20)', '', 'Cociente de presiones con grano frío.'),
  ('spread', 'hot/cold', '', 'Cociente entre los extremos.')],
 r'$\pi_K=%(pik)s\,\mathrm{K^{-1}}$; $p_c/p_{c,ref}=%(hot)s$ ($+35\,\mathrm K$) y $%(cold)s$ ($-20\,\mathrm K$).',
 r'Un grano caliente eleva la presión y el empuje, y exige un diseño estructural para el extremo caliente, mientras que uno frío reduce el empuje y puede dar un quemado más largo; la relación entre extremos es $%(spread)s$.',
 r'Para $\Delta T=0$ el cociente es 1. El aumento de presión por $1\,\mathrm K$ es $\pi_K\approx0.3\,\%%$.',
 r'La sensibilidad no es exactamente constante, ni la presión es la única variable afectada: cambian también el tiempo de quemado y la distribución de tensiones del grano.')

spec('P17', 'Fracción másica y velocidad ideal de un motor sólido',
 r'Un motor sólido tiene $420\,\mathrm{kg}$ de propulsante, $70\,\mathrm{kg}$ de masa inerte del motor y soporta una carga útil de $110\,\mathrm{kg}$. Entrega $I_{sp}=245\,\mathrm s$. Calcule la fracción másica de propulsante del motor, la razón de masas, la velocidad ideal y cómo cambia si el $I_{sp}$ real es el $97\,\%$ del nominal.',
 r'$m_p=420\,\mathrm{kg}$; $m_i=70\,\mathrm{kg}$; $m_{pl}=110\,\mathrm{kg}$; $I_{sp}=245\,\mathrm s$.',
 r'Fracción másica, razón de masas, $\Delta v$ ideal y con $I_{sp}$ reducido.',
 r'Impulso específico constante; sin gravedad ni resistencia; la carga útil permanece unida al final.',
 r'Ecuación del cohete de una sola etapa.',
 [r'\zeta=m_p/(m_p+m_i),\quad \mathcal R=\frac{m_p+m_i+m_{pl}}{m_i+m_{pl}}',
  r'\Delta v=I_{sp}g_0\ln\mathcal R'],
 [r'La fracción másica del motor es $\zeta=%(zeta)s$ y la razón de masas $\mathcal R=%(R)s$.',
  r'La velocidad ideal es $%(dv)s\,\mathrm{m/s}$ y con el $97\,\%%$ de $I_{sp}$ es $%(dv2)s\,\mathrm{m/s}$.'],
 [('zeta', '420/(420+70)', '', 'Fracción másica del motor.'),
  ('R', '(420+70+110)/(70+110)', '', 'Razón de masas con carga útil.'),
  ('dv', '245*9.80665*log(R)', 'm/s', 'Velocidad ideal nominal.'),
  ('dv2', '.97*245*9.80665*log(R)', 'm/s', 'Velocidad ideal con impulso específico reducido.'),
  ('loss', 'dv-dv2', 'm/s', 'Pérdida por la reducción de impulso específico.')],
 r'$\zeta=%(zeta)s$; $\mathcal R=%(R)s$; $\Delta v=%(dv)s\,\mathrm{m/s}$; con $97\,\%%$ de $I_{sp}$, $%(dv2)s\,\mathrm{m/s}$ (pérdida $%(loss)s\,\mathrm{m/s}$).',
 r'Una reducción del $3\,\%%$ en el impulso específico produce la misma reducción relativa en $\Delta v$; reducir la masa inerte del motor mejoraría la razón de masas.',
 r'Sin carga útil $\mathcal R$ sería $(420+70)/70$ y la velocidad mayor. La razón de masas es mayor que 1.',
 r'La velocidad real se reduce por gravedad, resistencia y orientación del empuje; esta es una cota ideal.')

spec('P18', 'Garganta que se erosiona durante el quemado',
 r'En un motor sólido el área de combustión se mantiene y la garganta crece por erosión de $0.00160$ a $0.00176\,\mathrm{m^2}$, un $10\,\%$ más. El exponente es $n=0.32$. Con $C_F$ constante, calcule el cociente de presiones, de empujes y de gastos entre el final y el inicio, y la pérdida relativa de empuje.',
 r'$A_{t,i}=0.00160\,\mathrm{m^2}$; $A_{t,f}=0.00176\,\mathrm{m^2}$; $n=0.32$; $A_b$, $c^*$ y $C_F$ constantes.',
 r'Cocientes de presión, empuje y gasto, y pérdida relativa de empuje.',
 r'Cuasiestacionario y descarga ahogada; $A_b$ y propiedades constantes; $C_F$ constante.',
 r'Equilibrio de generación y descarga con garganta variable.',
 [r'K_n=A_b/A_t,\quad p_c\propto K_n^{1/(1-n)}',
  r'p_f/p_i=(A_{t,i}/A_{t,f})^{1/(1-n)}',
  r'F\propto p_cA_t,\quad \dot m\propto p_cA_t'],
 [r'El cociente de áreas de garganta es $%(tau)s$.',
  r'La presión se reduce en $%(pr)s$.',
  r'El empuje y el gasto varían en $%(fr)s$, es decir, una pérdida del $%(loss)s\,\%%$.'],
 [('tau', '.00176/.00160', '', 'Cociente de áreas de garganta.'),
  ('pr', '(1/tau)**(1/(1-.32))', '', 'Cociente de presiones final e inicial.'),
  ('fr', 'pr*tau', '', 'Cociente de empuje y de gasto con CF constante.'),
  ('loss', '(1-fr)*100', '', 'Pérdida relativa de empuje en por ciento.')],
 r'$p_f/p_i=%(pr)s$; $F_f/F_i=\dot m_f/\dot m_i=%(fr)s$; pérdida de empuje $%(loss)s\,\%%$.',
 r'Aumentar la garganta reduce la presión más que proporcionalmente, porque $1/(1-n)>1$, y el empuje baja aunque la garganta sea mayor: $F=C_Fp_cA_t$ y la caída de $p_c$ domina.',
 r'Para $A_{t,f}=A_{t,i}$ los cocientes valen 1. El gasto y el empuje cambian igual porque $C_F$ y $c^*$ son constantes.',
 r'La erosión real de la garganta no es uniforme, cambia $C_F$ y $c^*$ efectivos y depende del material; el modelo da solo la tendencia.')

# ------------------------------------------------------------------ eléctricos
spec('P25', 'Propulsor iónico: haz, empuje e impulso específico',
 r'Un propulsor iónico de xenón (masa iónica $131.293\,\mathrm u$) acelera iones simples con una tensión efectiva de $1100\,\mathrm V$ y una corriente de haz de $0.45\,\mathrm A$. El factor de divergencia del haz es $0.97$ y la utilización de masa $0.88$. Calcule la velocidad de los iones, el gasto de iones, el empuje, el gasto total de propulsante, el $I_{sp}$ y la potencia del haz.',
 r'$m_i=131.293\,\mathrm u$; $V=1100\,\mathrm V$; $I_b=0.45\,\mathrm A$; divergencia $0.97$; utilización $0.88$.',
 r'Velocidad, gasto, empuje, $I_{sp}$ y potencia del haz.',
 r'Iones simples con carga $e$ y partida del reposo; haz monoenergético; neutros sin empuje.',
 r'Energía cinética de iones acelerados.',
 [r'v=\sqrt{2eV/m_i},\quad \dot m_i=I_bm_i/e',
  r'F=\lambda\dot m_iv,\quad \dot m=\dot m_i/\eta_m',
  r'I_{sp}=F/(\dot mg_0),\quad P_b=I_bV'],
 [r'La velocidad es $v=%(v)s\,\mathrm{m/s}$ y el gasto de iones $%(mi)s\,\mathrm{kg/s}$.',
  r'El empuje es $F=%(F)s\,\mathrm N$ y el gasto total $%(md)s\,\mathrm{kg/s}$, con $I_{sp}=%(isp)s\,\mathrm s$.',
  r'La potencia del haz es $%(Pb)s\,\mathrm W$.'],
 [('mion', '131.293*1.66053906892e-27', 'kg', 'Masa de un ion.'),
  ('v', 'sqrt(2*1.602176634e-19*1100/mion)', 'm/s', 'Velocidad tras la aceleración.'),
  ('mi', '.45*mion/1.602176634e-19', 'kg/s', 'Gasto de iones.'),
  ('F', '.97*mi*v', 'N', 'Empuje con divergencia del haz.'),
  ('md', 'mi/.88', 'kg/s', 'Gasto total con utilización de masa.'),
  ('isp', 'F/(md*9.80665)', 's', 'Impulso específico.'),
  ('Pb', '.45*1100', 'W', 'Potencia del haz.'),
  ('eta', 'F**2/(2*md*Pb)', '', 'Rendimiento de empuje respecto a la potencia del haz.')],
 r'$v=%(v)s\,\mathrm{m/s}$; $F=%(F)s\,\mathrm N$; $\dot m=%(md)s\,\mathrm{kg/s}$; $I_{sp}=%(isp)s\,\mathrm s$; $P_b=%(Pb)s\,\mathrm W$.',
 r'El empuje es de unas decenas de milinewtons con velocidades de escape de decenas de kilómetros por segundo: alto $I_{sp}$, bajo empuje.',
 r'La relación $F^2/(2\dot mP_b)=%(eta)s$ resume divergencia y utilización de masa. El orden de magnitud del empuje es el habitual de un propulsor iónico de unos 500 W de haz.',
 r'No se incluyen iones con doble carga, la potencia de neutralizador, las pérdidas de ionización ni la erosión de rejillas.')

spec('P26', 'Propulsor Hall: empuje, caudal y propulsante consumido',
 r'Un propulsor Hall recibe $1500\,\mathrm W$ con rendimiento total $0.50$ y $I_{sp}=1600\,\mathrm s$. Funciona 30 días seguidos. Calcule la velocidad de escape, el empuje, el gasto y la masa de propulsante consumida, y el empuje si se duplica el $I_{sp}$ con la misma potencia y rendimiento.',
 r'$P=1500\,\mathrm W$; $\eta=0.50$; $I_{sp}=1600\,\mathrm s$; duración 30 días.',
 r'$v_e$, $F$, $\dot m$, masa consumida y empuje con $2I_{sp}$.',
 r'Rendimiento total constante; escape axial uniforme con velocidad $I_{sp}g_0$; potencia constante.',
 r'Potencia del chorro y empuje.',
 [r'v_e=I_{sp}g_0,\quad F=2\eta P/v_e,\quad \dot m=F/v_e',
  r'm_p=\dot mt'],
 [r'La velocidad de escape es $%(ve)s\,\mathrm{m/s}$ y el empuje $%(F)s\,\mathrm N$.',
  r'El gasto es $%(md)s\,\mathrm{kg/s}$ y en $%(t)s\,\mathrm s$ se consumen $%(mp)s\,\mathrm{kg}$.',
  r'Con $2I_{sp}$, el empuje es $%(F2)s\,\mathrm N$, la mitad.'],
 [('ve', '1600*9.80665', 'm/s', 'Velocidad de escape equivalente.'),
  ('F', '2*.50*1500/ve', 'N', 'Empuje con potencia de chorro fija.'),
  ('md', 'F/ve', 'kg/s', 'Gasto másico.'),
  ('t', '30*86400', 's', 'Duración en segundos.'),
  ('mp', 'md*t', 'kg', 'Propulsante consumido.'),
  ('F2', '2*.50*1500/(2*ve)', 'N', 'Empuje con el doble de impulso específico.')],
 r'$v_e=%(ve)s\,\mathrm{m/s}$; $F=%(F)s\,\mathrm N$; $\dot m=%(md)s\,\mathrm{kg/s}$; $m_p=%(mp)s\,\mathrm{kg}$; $F_2=%(F2)s\,\mathrm N$.',
 r'Con potencia fija, el empuje es inversamente proporcional al impulso específico: más $I_{sp}$ ahorra propulsante pero da menos empuje y obliga a tiempos de maniobra mayores.',
 r'$F/(\dot mg_0)$ reproduce $I_{sp}=1600\,\mathrm s$. Con $\eta=0$ el empuje sería nulo.',
 r'El rendimiento real varía con el punto de funcionamiento; no se incluyen la divergencia, la utilización de masa ni las pérdidas del cátodo.')

spec('P27', 'Transferencia de baja empuje entre órbitas circulares',
 r'Un satélite de $600\,\mathrm{kg}$ debe pasar de una órbita circular de $400\,\mathrm{km}$ de altitud a otra de $800\,\mathrm{km}$ en el mismo plano con un propulsor eléctrico de empuje constante $0.045\,\mathrm N$ y velocidad de escape $15000\,\mathrm{m/s}$. Calcule el $\Delta v$ de la espiral, el tiempo de maniobra y la masa de propulsante. Use $\mu=3.986004418\times10^{14}\,\mathrm{m^3/s^2}$ y $R_T=6378\,\mathrm{km}$.',
 r'$m_0=600\,\mathrm{kg}$; altitudes $400$ y $800\,\mathrm{km}$; $F=0.045\,\mathrm N$; $v_e=15000\,\mathrm{m/s}$; $\mu$ y $R_T$ dados.',
 r'$\Delta v$, tiempo y masa de propulsante.',
 r'Espiral coplanar con empuje tangencial; $\Delta v=|v_1-v_2|$ de las velocidades circulares; empuje constante con masa variable.',
 r'Velocidades circulares y ecuación del cohete con empuje constante.',
 [r'v_c=\sqrt{\mu/r},\quad \Delta v=v_{c1}-v_{c2}',
  r'm_p=m_0[1-e^{-\Delta v/v_e}],\quad t=m_pv_e/F'],
 [r'Las velocidades circulares son $%(v1)s\,\mathrm{m/s}$ y $%(v2)s\,\mathrm{m/s}$, de modo que $\Delta v=%(dv)s\,\mathrm{m/s}$.',
  r'La masa de propulsante es $%(mp)s\,\mathrm{kg}$ y el tiempo $%(t)s\,\mathrm s$, unos $%(dias)s$ días.'],
 [('r1', '(6378+400)*1000', 'm', 'Radio de la órbita inicial.'),
  ('r2', '(6378+800)*1000', 'm', 'Radio de la órbita final.'),
  ('v1', 'sqrt(3.986004418e14/r1)', 'm/s', 'Velocidad circular inicial.'),
  ('v2', 'sqrt(3.986004418e14/r2)', 'm/s', 'Velocidad circular final.'),
  ('dv', 'v1-v2', 'm/s', 'Incremento de velocidad de la espiral.'),
  ('mp', '600*(1-exp(-dv/15000))', 'kg', 'Masa de propulsante.'),
  ('t', 'mp*15000/.045', 's', 'Tiempo con gasto de propulsante constante.'),
  ('dias', 't/86400', 'd', 'Tiempo en días.')],
 r'$\Delta v=%(dv)s\,\mathrm{m/s}$; $m_p=%(mp)s\,\mathrm{kg}$; $t=%(t)s\,\mathrm s$ ($%(dias)s$ días).',
 r'El $\Delta v$ es casi el mismo que el de una transferencia de dos impulsos, pero la espiral tarda semanas; la baja aceleración hace útil el alto $I_{sp}$.',
 r'$m_p\,v_e/F$ y $m_0\Delta v/F$ dan prácticamente el mismo tiempo porque $\Delta v/v_e\ll1$.',
 r'Se ignoran los eclipses, el empuje no tangencial, la resistencia atmosférica a $400\,\mathrm{km}$, los cambios de empuje con la potencia y el $J_2$.')

spec('P28', 'Potencia solar disponible y empuje con la distancia al Sol',
 r'Un panel solar entrega $2.4\,\mathrm{kW}$ a $1\,\mathrm{UA}$ y su potencia varía con el inverso del cuadrado de la distancia. Alimenta un propulsor de rendimiento $0.55$ e $I_{sp}=3000\,\mathrm s$. Calcule el empuje a $1\,\mathrm{UA}$ y a $1.5\,\mathrm{UA}$, y el cociente entre ambos.',
 r'$P_1=2.4\,\mathrm{kW}$ a $1\,\mathrm{UA}$; distancias $1$ y $1.5\,\mathrm{UA}$; $\eta=0.55$; $I_{sp}=3000\,\mathrm s$.',
 r'Potencias, empujes y su cociente.',
 r'Potencia $\propto1/d^2$; rendimiento e $I_{sp}$ constantes; toda la potencia se dedica al propulsor.',
 r'Empuje proporcional a la potencia con velocidad de escape fija.',
 [r'P(d)=P_1/d^2,\quad v_e=I_{sp}g_0',
  r'F=2\eta P/v_e'],
 [r'A $1.5\,\mathrm{UA}$ la potencia es $%(P2)s\,\mathrm W$.',
  r'Los empujes son $%(F1)s\,\mathrm N$ y $%(F2)s\,\mathrm N$, cociente $%(q)s$, que coincide con $1/d^2$.'],
 [('ve', '3000*9.80665', 'm/s', 'Velocidad de escape.'),
  ('P2', '2400/1.5**2', 'W', 'Potencia disponible a 1.5 UA.'),
  ('F1', '2*.55*2400/ve', 'N', 'Empuje a 1 UA.'),
  ('F2', '2*.55*P2/ve', 'N', 'Empuje a 1.5 UA.'),
  ('q', 'F2/F1', '', 'Cociente de empujes.')],
 r'$F_1=%(F1)s\,\mathrm N$; $F_2=%(F2)s\,\mathrm N$; $F_2/F_1=%(q)s$.',
 r'A mayor distancia solar el empuje cae como $1/d^2$, de modo que las maniobras se alargan; una misión al exterior del sistema solar requiere otra fuente de energía o una velocidad de escape menor.',
 r'El cociente de empujes iguala el de potencias. Con $d=1$ ambos empujes coinciden.',
 r'No se incluye la degradación de los paneles, la potencia que consumen los demás sistemas ni la variación de $\eta$ con la potencia.')

spec('P29', 'Velocidad de escape que maximiza la carga útil',
 r'Un vehículo con $\Delta v=2000\,\mathrm{m/s}$ usa un sistema eléctrico de masa específica $\alpha=25\,\mathrm{kg/kW}$, rendimiento $0.60$ y tiempo de empuje $2\times10^7\,\mathrm s$. La masa de la planta de potencia es $\alpha P$, con $P=\dot mv_e^2/(2\eta)$. Para velocidades de escape de $10$, $20$, $30$ y $40\,\mathrm{km/s}$, calcule la fracción de masa inicial que es propulsante y la de la planta, y la fracción de carga útil resultante.',
 r'$\Delta v=2000\,\mathrm{m/s}$; $\alpha=25\,\mathrm{kg/kW}$; $\eta=0.60$; $t=2\times10^7\,\mathrm s$; $v_e=10$, $20$, $30$, $40\,\mathrm{km/s}$.',
 r'Fracciones de propulsante, de planta y de carga útil para cada $v_e$.',
 r'Empuje constante durante $t$; potencia constante; la masa de la planta es proporcional a la potencia; sin otras masas.',
 r'Compromiso entre masa de propulsante y masa de la planta de potencia.',
 [r'm_p/m_0=1-e^{-\Delta v/v_e}',
  r'P=m_pv_e^2/(2\eta t),\quad m_{pot}/m_0=\alpha P/m_0=(\alpha v_e^2/(2\eta t))(m_p/m_0)',
  r'm_{pl}/m_0=1-m_p/m_0-m_{pot}/m_0'],
 [r'Las fracciones de propulsante para $v_e=10$, $20$, $30$ y $40\,\mathrm{km/s}$ son $%(mp10)s$, $%(mp20)s$, $%(mp30)s$ y $%(mp40)s$; las de la planta, $%(po10)s$, $%(po20)s$, $%(po30)s$ y $%(po40)s$. Las fracciones de carga útil son $%(pl10)s$, $%(pl20)s$, $%(pl30)s$ y $%(pl40)s$.',
  r'El máximo de las cuatro es el de $%(best)s\,\mathrm{km/s}$; hay un óptimo de $v_e$ entre un extremo con demasiado propulsante y otro con demasiada planta.'],
 [('a', '.025/(2*.60*2e7)', '', 'Coeficiente de la planta por unidad de velocidad al cuadrado.'),
  ('mp10', '1-exp(-2000/10000)', '', 'Fracción de propulsante con 10 km/s.'),
  ('mp20', '1-exp(-2000/20000)', '', 'Fracción de propulsante con 20 km/s.'),
  ('mp30', '1-exp(-2000/30000)', '', 'Fracción de propulsante con 30 km/s.'),
  ('mp40', '1-exp(-2000/40000)', '', 'Fracción de propulsante con 40 km/s.'),
  ('po10', 'mp10*a*10000**2', '', 'Fracción de planta de potencia con 10 km/s.'),
  ('po20', 'mp20*a*20000**2', '', 'Fracción de planta de potencia con 20 km/s.'),
  ('po30', 'mp30*a*30000**2', '', 'Fracción de planta de potencia con 30 km/s.'),
  ('po40', 'mp40*a*40000**2', '', 'Fracción de planta de potencia con 40 km/s.'),
  ('pl10', '1-mp10*(1+a*10000**2)', '', 'Fracción de carga útil con 10 km/s.'),
  ('pl20', '1-mp20*(1+a*20000**2)', '', 'Fracción de carga útil con 20 km/s.'),
  ('pl30', '1-mp30*(1+a*30000**2)', '', 'Fracción de carga útil con 30 km/s.'),
  ('pl40', '1-mp40*(1+a*40000**2)', '', 'Fracción de carga útil con 40 km/s.')],
 r'Fracción de carga útil: $%(pl10)s$ ($10$), $%(pl20)s$ ($20$), $%(pl30)s$ ($30$), $%(pl40)s$ ($40\,\mathrm{km/s}$).',
 r'Por debajo del óptimo se gasta demasiado propulsante y por encima domina la masa de la planta de potencia. La velocidad de escape óptima crece con el tiempo de empuje disponible y disminuye con la masa específica de la planta.',
 r'La suma de las fracciones vale 1 en cada caso. La planta se hace despreciable cuando $v_e\to0$ y el propulsante se hace despreciable cuando $v_e\to\infty$.',
 r'La masa de la planta se toma proporcional a la potencia; no incluye estructura, propulsante no utilizable ni la variación del rendimiento con $v_e$.')

spec('P30', 'Maniobra orbital eléctrica completa: de la potencia al delta-v',
 r'Un satélite de $450\,\mathrm{kg}$ dispone de $1.2\,\mathrm{kW}$ para propulsión, con rendimiento $0.60$ y escape de $18000\,\mathrm{m/s}$. Funciona durante $40$ días seguidos. Calcule el empuje, el gasto, el propulsante consumido, la masa final, el $\Delta v$ ideal y compárelo con el $\Delta v$ de $216\,\mathrm{m/s}$ que exige una espiral entre dos órbitas dadas.',
 r'$m_0=450\,\mathrm{kg}$; $P=1.2\,\mathrm{kW}$; $\eta=0.60$; $v_e=18000\,\mathrm{m/s}$; $t=40$ días; $\Delta v_{req}=216\,\mathrm{m/s}$.',
 r'$F$, $\dot m$, $m_p$, $m_f$, $\Delta v$ y margen frente al requerido.',
 r'Potencia, rendimiento y escape constantes; sin fuerzas externas; masa consumida menor que $m_0$.',
 r'Potencia de chorro, empuje y ecuación del cohete.',
 [r'F=2\eta P/v_e,\quad \dot m=F/v_e,\quad m_p=\dot mt',
  r'\Delta v=v_e\ln[m_0/(m_0-m_p)]'],
 [r'El empuje es $%(F)s\,\mathrm N$ y el gasto $%(md)s\,\mathrm{kg/s}$.',
  r'En $%(t)s\,\mathrm s$ se consumen $%(mp)s\,\mathrm{kg}$, quedan $%(mf)s\,\mathrm{kg}$ y el $\Delta v$ es $%(dv)s\,\mathrm{m/s}$.',
  r'El margen sobre los $216\,\mathrm{m/s}$ es de $%(margin)s\,\mathrm{m/s}$.'],
 [('F', '2*.60*1200/18000', 'N', 'Empuje de potencia de chorro.'),
  ('md', 'F/18000', 'kg/s', 'Gasto másico.'),
  ('t', '40*86400', 's', 'Duración en segundos.'),
  ('mp', 'md*t', 'kg', 'Propulsante consumido.'),
  ('mf', '450-mp', 'kg', 'Masa final.'),
  ('dv', '18000*log(450/mf)', 'm/s', 'Incremento de velocidad ideal.'),
  ('margin', 'dv-216', 'm/s', 'Margen sobre el delta-v requerido.'),
  ('approx', 'F*t/450', 'm/s', 'Aproximación impulso entre masa inicial.')],
 r'$F=%(F)s\,\mathrm N$; $m_p=%(mp)s\,\mathrm{kg}$; $\Delta v=%(dv)s\,\mathrm{m/s}$; margen $%(margin)s\,\mathrm{m/s}$.',
 r'Un empuje de decenas de milinewtons sostenido 40 días da más que el $\Delta v$ requerido, a costa de un tiempo de maniobra largo; la aproximación $Ft/m_0=%(approx)s\,\mathrm{m/s}$ queda algo por debajo porque ignora la reducción de masa.',
 r'La masa final es positiva y el margen es positivo. Con $P=0$ no hay empuje.',
 r'No se incluyen eclipses, la potencia de los demás sistemas ni el empuje fuera de la dirección tangencial.')


def block(key, d):
    keynum = int(key[1:])
    level = LEVEL[(keynum - 13) % 6 if keynum < 25 else (keynum - 25) % 6]
    rows = [dict(target=k, expression=e, unit=u, why=w) for k, e, u, w in d['steps']]
    body, checks = numeric_steps(rows)
    values = {c['target']: number(c['value'], 6) for c in checks}
    if key == 'P29':
        pls = {10: values['pl10'], 20: values['pl20'], 30: values['pl30'], 40: values['pl40']}
        best = max(pls, key=lambda k: float(pls[k]))
        values['best'] = str(best)
    (BOOK / 'solutions/generated' / f'{key}.tex').write_text(body + '\n')
    # El texto en LaTeX usa %% para un porcentaje literal; formatear con los valores.
    fill = lambda s: s % values
    development = '\n'.join(r'\item ' + fill(x) for x in d['development'])
    equations = '\n'.join(r'\[' + e + r'\]' for e in d['equations'])
    return (f'\\section{{{key}. {d["title"]}}}\n'
            f'\\begin{{studiumworked}}{{{key}. {d["title"]} · {level}}}\n'
            f'\\textbf{{Enunciado.}} {d["statement"]}\n\n'
            f'\\textbf{{Datos.}} {d["data"]}\n\n'
            f'\\textbf{{Incógnitas.}} {d["unknown"]}\n\n'
            f'\\textbf{{Hipótesis.}} {d["hypotheses"]}\n\n'
            f'\\textbf{{Modelo físico.}} {d["model"]}\n{equations}\n'
            f'\\textbf{{Desarrollo.}}\n\\begin{{enumerate}}\n{development}\n\\end{{enumerate}}\n'
            f'\\textbf{{Operaciones para contrastar el cálculo.}}\n\\input{{../solutions/generated/{key}.tex}}\n'
            f'\\textbf{{Resultados.}} {fill(d["results"])}\n\n'
            f'\\textbf{{Interpretación.}} {fill(d["interpretation"])}\n\n'
            f'\\textbf{{Comprobación.}} {fill(d["check"])}\n\n'
            f'\\textbf{{Límites.}} {fill(d["limits"])}\n'
            f'\\end{{studiumworked}}\n'), checks


def main() -> None:
    path = BOOK / 'latex/problemas.tex'
    text = path.read_text()
    reports = []
    for key, d in P.items():
        new, checks = block(key, d)
        reports.append(dict(problem=key, steps=checks))
        pattern = re.compile(r'\\section\{' + key + r'\. .*?(?=\\section\{P\d+\.|\\clearpage|\\end\{document\}|\\chapter)', re.S)
        if not pattern.search(text):
            raise SystemExit(f'No se encuentra el bloque de {key}')
        text = pattern.sub(lambda m: new, text, count=1)
    path.write_text(text)
    import json
    (BOOK / 'reports/problem-rewrite-procedures.json').write_text(json.dumps(
        dict(scope='Original numeric exercise data and authored derivations; no independent approval',
             records=reports), ensure_ascii=False, indent=2) + '\n')
    print('problemas reescritos:', ', '.join(P))


if __name__ == '__main__':
    main()
