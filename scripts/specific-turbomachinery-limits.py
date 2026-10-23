#!/usr/bin/env python3
"""Sustituye la limitación genérica de cada problema de Turbomáquinas por otra propia del modelo.

Cada entrada dice qué fenómeno real omite la hipótesis del modelo y qué haría
falta para tratarlo. Es una redacción docente, sin aprobación académica independiente.
"""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
FILE = ROOT / 'books/turbomaquinas/publication/problemas-resueltos.tex'
GENERIC = r'\item Modelo educativo; la aplicabilidad a una máquina real requiere revisión experta.'

LIMITS = {
'Estado estático desde remanso': [
  r'Con $\gamma$ constante se desprecia la variación del calor específico con la temperatura; a la temperatura de una turbina el error en $\rho$ no es despreciable.',
  r'El Mach es el medio de la estación; una capa límite gruesa o un perfil radial cambian la presión estática local.'],
'Difusor adiabático': [
  r'Se supone pérdida de remanso nula o dada; una separación real aumenta esa pérdida y limita la recuperación de presión.',
  r'El flujo es uniforme a la salida; las distorsiones aguas abajo no se modelan.'],
'Entropía en fila fija': [
  r'El aumento de entropía se atribuye a la fila completa sin separar pérdidas de perfil, de borde de salida y secundarias.',
  r'No se incluyen fugas ni mezcla con otros flujos, que añaden entropía.'],
'Anillo con remolino': [
  r'Se promedia en el anillo; la velocidad axial real varía con el radio y las estelas de la fila anterior.',
  r'Con bloqueo despreciable el área efectiva se sobrestima si las capas límite de cubo y carcasa son gruesas.'],
'Par de un compresor': [
  r'El par se obtiene del flujo de momento angular de los cortes elegidos; no incluye fricción de disco ni fugas, que consumen par adicional.',
  r'Con radio constante y flujo uniforme se pierden los efectos radiales de un escalón de gran altura de pala.'],
'Triángulo y referencia relativa': [
  r'El triángulo es el del radio de referencia; en raíz y punta cambian $U$, $C_x$ y los ángulos relativos.',
  r'No hay variaciones circunferenciales: estelas y choques locales se promedian.'],
'Euler con radios distintos': [
  r'Los radios medios representan el flujo de momento angular solo si la distribución radial es suave; con grandes gradientes habría que integrar por franjas.',
  r'El resultado es el trabajo ideal de Euler: no descuenta fugas, calor intercambiado ni pérdidas por fricción de disco.'],
'Comprobación de rotalpía': [
  r'La conservación de rotalpía exige flujo estacionario y adiabático en la referencia móvil; se rompe con refrigeración o sangrado de aire.',
  r'La comprobación verifica la coherencia del balance del modelo, no la exactitud de las medidas.'],
'Compresión total-total': [
  r'El rendimiento total-total no separa las pérdidas de cada escalón ni la contribución de las fugas.',
  r'Con $\gamma$ constante se subestima el trabajo cuando el aire se calienta mucho a lo largo de la compresión.'],
'Expansión total-total': [
  r'Se supone expansión sin sangrado ni refrigeración; el aire de refrigeración real modifica el gasto, la temperatura de entrada al rotor y el trabajo.',
  r'El gas es perfecto con $\gamma$ constante, aunque los productos de combustión cambian de composición y de calor específico.'],
'Conversión politrópica': [
  r'La eficiencia politrópica se toma constante a lo largo del proceso; la de un escalón real varía con el punto de funcionamiento.',
  r'La conversión a eficiencia isentrópica depende de la razón de presiones y de $\gamma$ constante.'],
'Corrección de caudal': [
  r'La corrección por $T_0$ y $p_0$ supone el mismo gas, el mismo número de Reynolds y cinemática semejante; no sirve lejos del punto de diseño o con Reynolds muy distinto.',
  r'No incluye efectos de Mach compresible distintos de la semejanza declarada.'],
'Acción ideal': [
  r'Una turbina de acción pura tiene reacción nula y radio y componente axial constantes, algo que el espesor de la pala y las pérdidas no permiten alcanzar.',
  r'El resultado es una cota superior de trabajo con pérdidas nulas.'],
'Óptimo de utilización': [
  r'El óptimo cinemático es el del triángulo ideal; las pérdidas, el Mach y la fricción desplazan el óptimo de una máquina real.',
  r'Se fija la velocidad y la orientación de entrada; en una máquina real varían con el punto de funcionamiento.'],
'Rotor con reducción de velocidad relativa': [
  r'El factor $k$ y la dirección relativa son datos del modelo, no resultado de las pérdidas del canal del rotor.',
  r'Con radio constante se ignora que la velocidad periférica cambia entre entrada y salida si el flujo no es axial.'],
'Carga de cascada de turbina': [
  r'Los ángulos algebraicos describen el flujo medio; la desviación real depende de la solidez, del espesor y del número de Mach.',
  r'La densidad y la velocidad axial constantes no se mantienen en una expansión con gran caída de entalpía.'],
'Triángulos desde carga y reacción': [
  r'Los triángulos se obtienen para igualar energía cinética en los extremos del escalón; en el primero y en el último escalón de una máquina eso rara vez ocurre.',
  r'Un único radio de referencia no describe la torsión de la pala.'],
'Reacción general no repetitiva': [
  r'La reacción general no repetitiva se usa en un solo escalón; la comparación con otros escalones exigiría cerrar los triángulos de cada fila.',
  r'La hipótesis de radio constante para Euler deja de valer en escalones con cambio importante de radio.'],
'Presión de descarga de turbina': [
  r'Sin refrigeración ni sangrado el modelo no incluye las pérdidas por fuga ni por espacios en punta.',
  r'Se supone la misma eficiencia en todo el escalón; en realidad varía con el Mach y la carga.'],
'Descarga axial y potencia': [
  r'El escalón repetitivo asume que la descarga de un escalón es la entrada del siguiente, lo que no se cumple en el primero ni en el último.',
  r'La potencia es la del eje antes de pérdidas mecánicas; la eficiencia mecánica se aplica aparte y es un dato del modelo.'],
'Área crítica': [
  r'La garganta ideal es unidimensional e isentrópica; una capa límite o una distorsión reducen el área efectiva y el gasto.',
  r'El resultado es la garganta de diseño; fuera de ese punto el bloqueo depende de las condiciones corriente abajo.'],
'Cociente crítico': [
  r'Una tobera convergente ideal conecta un depósito con el exterior sin pérdidas; las toberas reales tienen coeficiente de descarga menor que la unidad.',
  r'El cociente crítico depende de $\gamma$ constante.'],
'Reparto entero de escalones': [
  r'Dividir el trabajo por igual entre escalones con igual $U$ simplifica el diseño pero ignora que las primeras filas de un compresor suelen cargarse menos.',
  r'El número de escalones es entero; el redondeo cambia el trabajo por escalón respecto al valor ideal.'],
'Caudal de garganta oblicua': [
  r'El caudal se calcula en un corte axial con densidad y velocidad uniformes; en una garganta oblicua real el flujo no es uniforme.',
  r'El área proyectada no incluye el bloqueo de las capas límite.'],
'Trabajo y presión del escalón': [
  r'La eficiencia global del escalón se toma constante; no se distingue entre rotor y estator.',
  r'Con gas perfecto constante la razón de presiones sale distinta de la real si el calentamiento es grande.'],
'Reacción y remolinos': [
  r'La condición $C_3^2=C_1^2$ define un escalón repetitivo; no vale para escalones de entrada o de salida.',
  r'Un radio y una velocidad axial constantes no describen un escalón con gran relación cubo-punta.'],
'Mach relativo': [
  r'El Mach relativo local debe compararse con el crítico del perfil; este problema no incluye ese límite.',
  r'El gas se supone perfecto con $\gamma$ constante.'],
'Cierre de reacción por entalpías': [
  r'El cierre por entalpías es un balance del modelo; no sustituye una medida de las condiciones de entrada y salida del escalón.',
  r'Con $C_x$ constante la reacción por entalpías coincide con la cinemática solo si no hay pérdidas.'],
'Indicador de difusión': [
  r'El factor de difusión es un indicador empírico del capítulo, definido en la referencia relativa; no predice el desprendimiento de la capa límite.',
  r'Los umbrales habituales dependen del perfil y del Reynolds y no se universalizan.'],
'Solidez mínima del modelo': [
  r'La solidez mínima sale de un criterio de difusión prescrito; el valor real también depende de pérdidas, espesor y Mach.',
  r'El criterio no garantiza una pérdida concreta ni la ausencia de desprendimiento.'],
'Número entero y solidez real': [
  r'La solidez real aparece al redondear el número de álabes a un entero; la fila se supone uniforme en el radio de referencia, aunque la cuerda cambie con el radio.',
  r'El espaciado y el número de álabes también se fijan por criterios vibratorios y de fabricación que este problema no considera.'],
'Incidencia y desviación algebraicas': [
  r'La incidencia y la desviación se tratan como diferencias de ángulos algebraicos con el mismo sentido positivo; su signo debe comprobarse en cada caso.',
  r'La desviación real depende de la curvatura, la solidez y el Mach; aquí es un dato.'],
'Compresión de varios escalones': [
  r'La eficiencia politrópica constante y el gas perfecto son aproximaciones; la eficiencia real varía a lo largo del compresor.',
  r'Sin sangrado, el gasto es el mismo en todos los escalones, lo que no ocurre en un compresor con sangrados.'],
'Altura de anillo con bloqueo': [
  r'El flujo se supone uniforme en el área restante después del bloqueo; el bloqueo real cambia a lo largo de la máquina.',
  r'La altura de anillo calculada es la efectiva, no la geométrica.'],
'Trabajo por escalón y razón de presión': [
  r'La razón de presiones del escalón sale de gas perfecto constante y escalón adiabático; no incluye fugas ni sangrados.',
  r'El trabajo por escalón es un valor medio: las filas de entrada y de salida pueden trabajar a otro nivel.'],
'Acoplamiento de eje con caudales distintos': [
  r'El trabajo del compresor ya excluye las pérdidas de transmisión y la eficiencia mecánica se aplica una vez al lado de la turbina; contar la pérdida dos veces o no contarla cambia el resultado.',
  r'Los caudales distintos de compresor y turbina suponen un sangrado o una inyección que se tratan solo como datos.'],
'Incidencia durante variación de caudal': [
  r'Se supone velocidad axial positiva, sin prerrotación y con el metal fijo; con prerrotación variable o álabes de geometría variable el cambio de incidencia sería distinto.',
  r'La incidencia sola no indica cuándo se pierde la capacidad de difusión de la fila.'],
'Margen de caudal definido': [
  r'El margen se define con caudales corregidos a las mismas referencias; si las referencias cambian, el margen no es comparable.',
  r'No hay mapa experimental ni línea de bombeo predicha: el margen es una definición, no una predicción de estabilidad.'],
'Corrección de velocidad': [
  r'La corrección por temperatura de entrada supone el mismo gas y semejanza cinemática; no vale con grandes cambios de Reynolds o de Mach.',
  r'El radio es fijo; con deformación centrífuga o variación de la holgura el radio efectivo cambia.'],
'Estabilidad lineal del modelo ampliado': [
  r'La linealización es local en torno a un punto de equilibrio; no predice la amplitud ni el ciclo límite de una inestabilidad real.',
  r'El modelo pedagógico no tiene retardo ni acoplamiento con el sistema de conductos, que en una máquina real alteran el umbral de estabilidad.'],
'Presión de vórtice libre': [
  r'El equilibrio radial simple supone flujo axisimétrico y densidad constante; con altos números de Mach la densidad varía con el radio.',
  r'Se desprecia la curvatura de las líneas de corriente en el plano meridional.'],
'Trabajo uniforme con vórtice libre': [
  r'El vórtice libre da trabajo uniforme solo en el modelo ideal con líneas de corriente cilíndricas; la torsión de pala resultante puede ser excesiva para una relación cubo-punta pequeña.',
  r'No hay pérdidas distribuidas ni efectos secundarios en cubo y carcasa.'],
'Reacción hacia la raíz': [
  r'El criterio reducido solo vale para radio y $C_x$ constantes en un escalón repetitivo; en cubos pequeños la reacción puede hacerse negativa.',
  r'No indica si el Mach relativo o la difusión se vuelven críticos en la raíz.'],
'Vórtice forzado admisible': [
  r'El equilibrio radial simple con $h_0$ y $s$ uniformes es una idealización; las capas límite y las pérdidas crean gradientes de entropía radiales.',
  r'El valor admisible es el del modelo y no incluye otros límites estructurales o de Mach.'],
'Torsión de entrada de rotor': [
  r'Sin prerrotación, con $C_x$ uniforme e incidencia cero se obtiene un ángulo ideal; la incidencia óptima real no es cero.',
  r'La torsión necesaria puede exceder lo que permiten los criterios de fabricación y de esfuerzos.'],
'Cuerda y proyección': [
  r'La proyección con calado menor de noventa grados en módulo es un cálculo geométrico; no incluye espesor ni el efecto del número de álabes.',
  r'Los ángulos se miden respecto al eje elegido y no son los del flujo.'],
'Línea de Hermite': [
  r'La línea media es una función $y(x)$ monótona con cuatro condiciones de contorno; no garantiza un perfil aerodinámicamente óptimo.',
  r'Las comprobaciones de curvatura y de autocruces no sustituyen un análisis de flujo viscoso.'],
'Desplazamiento normal por espesor': [
  r'El espesor se aplica por desplazamiento normal local; con curvatura grande aparecen autocruces cerca del borde.',
  r'No se incluye el redondeo de bordes ni los límites de fabricación.'],
'Tracción centrífuga uniforme': [
  r'La barra radial uniforme y homogénea deja fuera la variación de sección, la plataforma y la raíz de sujeción.',
  r'La tensión nominal no incluye concentración de tensiones, fluencia ni vida a fatiga; los admisibles se toman como dato.'],
'Pala estrechada': [
  r'El área lineal positiva en el intervalo es un modelo geométrico; sin carga aerodinámica ni térmica no da la tensión real.',
  r'La integral de tensión centrífuga ignora el cambio de material por temperatura.'],
'Flexión nominal y tracción': [
  r'Viga elástica lineal con sección equivalente; no se incluyen la torsión, los acoplamientos ni la plasticidad local.',
  r'La carga aerodinámica se toma como dato; la distribución real depende del perfil y de la incidencia.'],
'Frecuencia del voladizo educativo': [
  r'Una viga uniforme de Euler-Bernoulli sin rotación ni amortiguamiento da solo la primera frecuencia nominal; la rigidización centrífuga y el acoplamiento torsional la modifican.',
  r'El resultado no sustituye un análisis modal ni un diagrama de Campbell.'],
'Red térmica de pared': [
  r'La red estacionaria unidimensional con coeficientes constantes no incluye radiación ni conducción lateral; en el borde de ataque el flujo de calor es bidimensional.',
  r'Los coeficientes de transferencia son datos, no resultado de un cálculo de capa límite.'],
'Caudal energético de refrigeración': [
  r'El balance supone que todo el calor extraído lo absorbe el refrigerante con $c_p$ constante; no se modelan la mezcla ni las pérdidas de presión del circuito.',
  r'El caudal de refrigeración mínimo del modelo es una cota inferior ideal.'],
'Película y recuperación': [
  r'La efectividad y el coeficiente son datos para una misma geometría y un mismo punto; cambian con el soplado y la posición de las perforaciones.',
  r'La película se supone completamente adherida; en la realidad se desprende y se mezcla.'],
'Restricción térmica uniaxial': [
  r'La restricción total uniaxial y la elasticidad lineal dan la tensión máxima térmica; se ignora la relajación por fluencia y la plasticidad.',
  r'Un gradiente térmico real genera tensiones multiaxiales que no se calculan aquí.'],
'Rodete radial con deslizamiento': [
  r'El deslizamiento se aplica sobre una salida ideal radial sin prerrotación; el factor depende del número de álabes y del ángulo de salida.',
  r'No se incluyen pérdidas por fricción de disco, recirculación ni fugas.'],
'Curvatura hacia atrás': [
  r'El factor de deslizamiento prescrito es positivo; su dependencia con el número de álabes y el caudal no se modela.',
  r'Con curvatura hacia atrás, el trabajo cae con el caudal; aquí solo se evalúa un punto.'],
'Inductor y Mach de punta': [
  r'La velocidad axial uniforme y la ausencia de prerrotación omiten la distorsión de la entrada; el Mach relativo de punta depende de la capa límite en la carcasa.',
  r'No se evalúa el límite de cavitación o de bloqueo sónico.'],
'Prerrotación y trabajo': [
  r'Euler con valores medios compatibles supone una distribución uniforme; la prerrotación real varía en la altura de la entrada.',
  r'El efecto de la prerrotación sobre el Mach relativo y la incidencia no se evalúa.'],
'Difusor sin álabes ideal': [
  r'Un difusor ideal sin par con ancho y densidad constantes subestima las pérdidas por fricción y por mezcla.',
  r'La velocidad radial supone flujo axisimétrico y la distorsión de la salida del rodete no se modela.'],
'Recuperación con pérdida prescrita': [
  r'El modelo incompresible con pérdida prescrita es válido a Mach bajo; a Mach alto la densidad cambia.',
  r'La pérdida se define con la velocidad de entrada y es un dato, no un resultado.'],
'Ancho del paso cilíndrico': [
  r'El paso cilíndrico uniforme con bloqueo explícito supone una distribución uniforme del flujo en el ancho.',
  r'El valor de bloqueo es un dato y varía con el punto de funcionamiento.'],
'Estado estático de descarga': [
  r'Las componentes ortogonales de la velocidad suponen un flujo sin gradiente circunferencial a la descarga.',
  r'Con $\gamma$ constante y gas perfecto, la temperatura estática estimada se aparta del valor real si hay gran calentamiento.'],
'Velocidad exigida por trabajo': [
  r'Con salida radial, sin prerrotación y deslizamiento constante, la velocidad periférica exigida es un valor mínimo ideal.',
  r'La velocidad real también debe respetar límites de tensión y de Mach.'],
'Presión y sensibilidad de eficiencia': [
  r'El trabajo se fija y la presión sale de la eficiencia; sin refrigeración el modelo no incluye pérdidas de calor.',
  r'La sensibilidad es local: grandes cambios de eficiencia exigirían recalcular el punto de trabajo.'],
'Pendiente cinemática con caudal': [
  r'La pendiente cinemática supone densidad, ancho, deslizamiento, radio y giro fijos; si cambian con el caudal la pendiente real difiere.',
  r'No hay prerrotación: con prerrotación variable la curva cambia.'],
'Balance inverso de rendimiento': [
  r'El rendimiento inverso sale de mediciones medias representativas; el error de medida de temperatura o de presión afecta directamente al resultado.',
  r'Sin calor externo y con gas perfecto constante, el balance no detecta fugas.'],
'Rotor compresor a radio elegido': [
  r'El vórtice libre por estación y la incidencia prescrita dan ángulos de un radio; la distribución radial completa requiere varias estaciones.',
  r'El resultado es geométrico y no valida el comportamiento aerodinámico del perfil.'],
'Estator compresor y orientación de salida': [
  r'Las velocidades absolutas son prescritas y la desviación es un dato; la desviación real depende de la solidez y el Mach.',
  r'No hay verificación de pérdidas ni de difusión del estator.'],
'Estator turbina y calado educativo': [
  r'La línea media de Hermite educativa con $x$ monótona es geométrica; no incluye pérdidas ni el efecto del espesor sobre el flujo.',
  r'El calado calculado es el del modelo, no un valor de diseño validado.'],
'Rotor turbina y espesor por radio': [
  r'El vórtice libre y el espesor normal local son un modelo geométrico por radio; no incluye el efecto del espesor sobre el flujo ni los límites de fabricación.',
  r'No se evalúa la tensión ni la frecuencia propia de la pala resultante.'],
'Cierre de compresor axial': [
  r'El escalón adiabático con gas perfecto, radio medio y $C_x$ constantes cierra el balance del modelo, no un compresor real con fugas y sangrados.',
  r'La razón de presiones obtenida es la del escalón ideal con la eficiencia dada.'],
'Turbina con descarga axial': [
  r'Un escalón repetitivo con descarga axial supone igual radio y $C_x$ y ninguna refrigeración; el primer escalón real recibe un flujo no axial.',
  r'La potencia calculada es la de eje antes de pérdidas mecánicas.'],
'Distribución radial y tracción': [
  r'La reacción reducida es válida para un escalón repetitivo y una pala mecánica uniforme; en un cubo pequeño la torsión resultante puede ser excesiva.',
  r'La tensión de tracción es la nominal; no incluye concentraciones, fluencia ni fatiga.'],
'Rodete radial y prestación': [
  r'Con salida radial ideal antes del deslizamiento y sin prerrotación el modelo da una cota superior del trabajo.',
  r'La prestación calculada no incluye fricción de disco, recirculación ni fugas.'],
'Cascada y elección entera': [
  r'El indicador de difusión definido en referencia relativa decide la solidez; al elegir un número entero de álabes cambia el valor real.',
  r'El criterio no garantiza la ausencia de desprendimiento.'],
'Balance térmico integrado': [
  r'La red estacionaria unidimensional con propiedades constantes y sin radiación no representa un gradiente térmico bidimensional en el borde de ataque.',
  r'Los coeficientes de transferencia y la efectividad de la película son datos del problema.'],
}


def main() -> None:
    text = FILE.read_text()
    blocks = re.split(r'(?=\\begin\{studiumworked\})', text)
    out, changed, missing = [blocks[0]], 0, []
    for block in blocks[1:]:
        title = re.search(r'Modelo físico\}\s*\\noindent\\textit\{([^}]*)\}', block)
        head = re.match(r'\\begin\{studiumworked\}\{([^}]*)\}', block)
        key = title.group(1) if title else None
        if key is not None:
            key = re.sub(r'^[A-Z]\d+ \\\(\\cdot\\\) ', '', key)
        if GENERIC in block:
            if key in LIMITS:
                block = block.replace(GENERIC, '\n'.join(r'\item ' + b for b in LIMITS[key]), 1)
                changed += 1
            else:
                missing.append((head.group(1) if head else '?', key))
        out.append(block)
    FILE.write_text(''.join(out))
    print('limitaciones reescritas:', changed, 'sin entrada:', missing[:5])


if __name__ == '__main__':
    main()
