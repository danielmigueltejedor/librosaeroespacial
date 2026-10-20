#!/usr/bin/env python3
"""Replace internal SymPy identifiers in the 18 turbo equation boxes with notation."""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
MANUAL = ROOT / "books/turbomaquinas/publication/turbomaquinas-ule-2026.tex"
FORMULARIO_START = r"\chapter{Formulario y condiciones de uso}"
SOLUCIONES_START = r"\chapter{Soluciones de los ejercicios}"

# New equation for each of the 18 model boxes.  Each must be mathematically
# identical to the corresponding old expression (verified by sympy separately).
NEW_EQUATIONS = {
 "C01": r"\rho=\frac{p_0}{R_g T_0}\left(1+\frac{\gamma-1}{2}\mathrm{Ma}^2\right)^{-\frac{1}{\gamma-1}}",
 "C02": r"\dot W=\Omega\,\dot m\,r\,(C_{\theta s}-C_{\theta e})",
 "C03": r"w_c=\frac{T_{0e}\,c_p}{\eta_{tt}}\left(\pi_c^{\frac{\gamma-1}{\gamma}}-1\right)",
 "C04": r"\Delta T_0=\frac{2\,U\,(C_\theta-U)}{c_p}",
 "C05": r"W_{\theta 3}=U\left(-\frac{\psi}{2}-\mathcal R\right)",
 "C06": r"A^*=\frac{\dot m\,\sqrt{T_{0e}}}{p_{0e}}\left(\frac{2}{\gamma+1}\right)^{-\frac{\gamma+1}{2(\gamma-1)}}\sqrt{\frac{R_g}{\gamma}}",
 "C07": r"\pi_c=\left(1+\frac{\eta_{tt}\,\psi\,U^2}{T_{0e}\,c_p}\right)^{\frac{\gamma}{\gamma-1}}",
 "C08": r"D=\frac{\Delta V_\theta}{2\,\sigma\,V_e}+1-\frac{V_s}{V_e}",
 "C09": r"\dot W=\frac{T_{0e}\,c_p\,\dot m}{\eta_m}\left(\pi_c^{\frac{\gamma-1}{\eta_p\,\gamma}}-1\right)",
 "C10": r"i=-\kappa-\arctan\frac{U}{C_x}",
 "C11": r"\Delta p=\frac{K_v^{\,2}\,\rho}{2}\left(\frac{1}{r_m^2}-\frac{1}{r_t^2}\right)",
 "C12": r"\Delta\beta=\arctan\frac{\Omega\,r_h}{C_x}-\arctan\frac{\Omega\,r_t}{C_x}",
 "C13": r"\sigma_c=\frac{\rho\,\Omega^2}{2}\left(r_t^2-r_h^2\right)",
 "C14": r"T_w=T_{aw}-\frac{T_{aw}-T_c}{h_g\left(\frac1{h_g}+\frac1{h_c}+\frac{t}{k_m}\right)}",
 "C15": r"\Delta T_0=\frac{\sigma_s\,U^2}{c_p}",
 "C16": r"\Delta p=\frac{\rho\,(C_r^2+C_\theta^2)}{2}\left(1-\frac{r_e^2}{r_s^2}\right)",
 "C17": r"r=\frac{1}{\Omega}\sqrt{\frac{w_c}{\sigma_s}}",
 "C18": r"\kappa=-i+\arctan\frac{K_v/r-\Omega\,r}{C_x}",
}

DEFINITIONS = {
 "C01": "Densidad estática a partir de la presión y temperatura totales locales, con frenado isentrópico local. Aquí $p_0$ y $T_0$ son totales; no intercambiarlas con magnitudes estáticas.",
 "C02": "Potencia de eje comunicada al fluido a radio constante. $C_{\\theta s}$ y $C_{\\theta e}$ son componentes tangenciales absolutas; el signo indica compresor o turbina.",
 "C03": "Trabajo específico real de un compresor total-total. $\\eta_{tt}$ es la eficiencia total-total del escalón, distinta de una eficiencia politrópica.",
 "C04": "Descenso de temperatura total en una acción ideal con radio y componente axial constantes. $\\Delta T_0$ es una caída positiva; no equivale a $T_{\\mathrm{salida}}-T_{\\mathrm{entrada}}$.",
 "C05": "Componente relativa tangencial a la salida del rotor. Es $W_{\\theta 3}$, no $C_{\\theta 3}$; el signo depende de $\\psi$ y $\\mathcal R$.",
 "C06": "Área de garganta sónica ideal para gas perfecto con las condiciones de entrada declaradas.",
 "C07": "Relación de presiones totales de un escalón de compresor. $\\psi$ es la carga adimensional y $\\eta_{tt}$ la eficiencia total-total.",
 "C08": "Factor de difusión de Lieblein en la referencia de la fila. $\\Delta V_\\theta$ es el cambio tangencial con el signo usado en el caso; la definición clásica usa su valor absoluto.",
 "C09": "Potencia de eje de una compresión politrópica sin sangrado. $\\eta_p$ es la eficiencia politrópica, no el rendimiento propulsivo de una hélice.",
 "C10": "Incidencia con prerrotación nula. $\\kappa$ es el ángulo metálico de entrada; los ángulos se miden desde el eje hacia el giro positivo.",
 "C11": "Diferencia de presión entre dos radios en un vórtice libre. $K_v=rC_\\theta$ es el identificador del vórtice libre, en $\\mathrm{m^2\\,s^{-1}}$; no es el coeficiente de vórtice forzado, cuya unidad es $\\mathrm{s^{-1}}$.",
 "C12": "Diferencia de ángulo relativo entre raíz y punta con prerrotación nula. El valor es negativo cuando la punta está más inclinada; no equivale al valor absoluto de la torsión geométrica.",
 "C13": "Tensión centrífuga en la raíz de una pala de sección constante. No incluye estrechamiento, flexión ni temperatura.",
 "C14": "Temperatura de la cara caliente en una red térmica unidimensional. La temperatura motriz es la de pared adiabática $T_{aw}$, no una temperatura estática de gas no declarada.",
 "C15": "Aumento de temperatura total con prerrotación nula. $\\sigma_s$ es el factor de deslizamiento, no la solidez.",
 "C16": "Diferencia de presión entre entrada y salida en un flujo radial incompresible, de ancho constante y sin par.",
 "C17": "Radio de salida exigido por un trabajo específico sin prerrotación.",
 "C18": "Ángulo metálico en función de la incidencia, el vórtice libre y la velocidad de giro.",
}

def patch_model_boxes(text):
    for code, new_eq in NEW_EQUATIONS.items():
        label = r"\label{eq:EC-" + code + "}"
        assert label in text, code
        # Replace first equation body preceding the label.
        # find label position
        idx = text.index(label)
        # find preceding \begin{equation}
        begin = text.rfind(r"\begin{equation}", 0, idx)
        assert begin != -1
        end = text.index(r"\end{equation}", idx) + len(r"\end{equation}")
        old_block = text[begin:end]
        # capture leading whitespace
        new_block = r"\begin{equation}" + "\n" + new_eq + "\n" + label + "\n" + r"\end{equation}"
        # preserve the newline after end{equation} by replacement range
        text = text[:begin] + new_block + text[end:]
        # Insert definition after the equation block (only first occurrence per code)
    # Insert definitions after each equation label block
    for code, definition in DEFINITIONS.items():
        label = r"\label{eq:EC-" + code + "}"
        idx = text.index(label)
        end = text.index(r"\end{equation}", idx) + len(r"\end{equation}")
        # avoid duplicate insertion
        if definition not in text[end:end+400]:
            text = text[:end] + "\n\n\\noindent\\textit{Significado.} " + definition + text[end:]
    return text

def main():
    text = MANUAL.read_text()
    text = patch_model_boxes(text)
    # Fix the derived formula that still used the internal identifier.
    text = text.replace(r"\fitmath{\mathit{wt3}=U \left(- \frac{\psi}{2} - \mathcal R\right)}",
                        r"\fitmath{W_{\theta 3}=U \left(- \frac{\psi}{2} - \mathcal R\right)}")
    # Replace the sympy identifiers in the first formula of each model? Already done above.
    MANUAL.write_text(text)
    print("patched model boxes")

if __name__ == "__main__":
    main()
