# A. Auditoría científica

Fecha: 19 de octubre de 2026. Edición EN REVISIÓN. Revisión experta independiente pendiente.

## Alcance y dictamen
Se ha desarrollado una edición docente completa, con modelos explícitos, deducciones, ejemplos y límites. No se declara científicamente validada. La cobertura se contrasta con la guía ULE 2026/2027, código 0710325, consultada completa. El capítulo dinámico es ampliación. La repetición de «Bloque V» en la guía se registra como anomalía editorial y no altera el contenido oficial.

## Revisión por familias
### Ejes y transporte (capítulos 1–3)

Contexto: MIT-3, MIT-4, MIT-14. NED: z abajo; cuerpo x delante, y derecha, z abajo; Cb_n pasiva 3-2-1. Velocidad aire distinta de suelo.

Comprobaciones: V001–V006; T02 ida/vuelta. Límite: Euler singular en cos(theta)=0; viento no uniforme requiere derivada de transporte.

### Fuerzas, polar y eficiencia (capítulos 4)

Contexto: MIT-1; deducción original. q=ρV²/2; V=TAS relativa al aire. CD0,k>0; referencias comunes. Oswald no se identifica siempre con eficiencia de envergadura.

Comprobaciones: V009–V014; controles Oswald y dimensiones. Límite: Polar subsónica docente; límite CLmax; mapa propulsivo no constante por defecto.

### Newton–Euler y simetría (capítulos 5–6)

Contexto: MIT-4, MIT-6. Tensor con entradas -Ixz; masa instantánea y tensor constantes en ecuación angular; marco cuerpo; trim no implica estabilidad.

Comprobaciones: V007–V008; T06 residuos por componente; controles trim. Límite: Sin flujo de momento por combustible; fuerzas N y momentos Nm no se mezclan en una norma sin escala.

### Planeadores (capítulos 7–9)

Contexto: MIT-1; derivación e integración originales. γ negativo en descenso, tasa de caída positiva. L=Wcosγ, D=-Wsinγ. ISA geopotencial y CL declarado para integrales.

Comprobaciones: Raíz exacta vs optimización T08; límites de planeo; cuadratura. Límite: No trasladar óptimo de ángulo pequeño a modelo exacto; viento afecta alcance suelo.

### Reactores (capítulos 10–12)

Contexto: MIT-1 y balances originales. cT en kg/(N s); Wdot=-g cT T. Separar V fija, CL fijo, empuje fijo y vuelo de CL,V fijos.

Comprobaciones: Primitivas simbólicas; ODE/cuadratura; 8 controles adicionales. Límite: ρ y CL fijos implican V variable; CL,V fijos requieren ρ variable y, si asciende, T≠D.

### Ascenso y descenso (capítulos 13)

Contexto: Balance Newton/energía. Exceso de potencia para ascenso pequeño cuasiestacionario. Integrar masa con altura y comprobar exceso positivo.

Comprobaciones: T13 refinamiento de 25 a 12.5 m; barridos. Límite: Vx,Vy requieren optimización y restricciones; techo docente no certificado.

### Viraje (capítulos 14)

Contexto: Balances originales. Viraje coordinado nivelado: n=1/cosφ, radio con TAS; comprobar pérdida, estructura y energía.

Comprobaciones: Identidades geométricas y envolvente T14. Límite: Viraje instantáneo no equivale a sostenido; viento altera trayectoria terrestre.

### Hélices y misión (capítulos 15–16)

Contexto: Balances originales. cP referido a potencia al eje en kg/J; η=TV/Peje; separar cuatro óptimos clásicos.

Comprobaciones: Primitiva de autonomía, ODE y T15 0<η≤1. Límite: η y cP variables invalidan fórmula cerrada; potencia útil no se confunde con potencia al eje.

### Rodadura y fases (capítulos 17–18)

Contexto: Newton y cuadratura originales. Va=Vsuelo+viento de cara; N=W-L; masa explícita; empuje finito a velocidad cero.

Comprobaciones: Cuadratura vs integración temporal, límite coeficiente cuadrático nulo. Límite: Rodadura sola no incluye transición ni obstáculo; no usar P/V singular al arrancar.

### Estabilidad estática (capítulos 19–20)

Contexto: MIT-2, MIT-8. Derivadas con variables retenidas y referencias de momento explícitas; margen estático bajo hipótesis lineales.

Comprobaciones: Punto neutro; residuos trim; r×F. Límite: Cm=0 es equilibrio, Cmα<0 tendencia estática. Efecto cola aislado no prueba estabilidad completa.

### Dinámica, ampliación (capítulos 21)

Contexto: MIT-6, MIT-7, MIT-8. Descriptor E xdot=F x; modos locales; aproximaciones reducidas bajo separación de escalas.

Comprobaciones: Autovalores, exponencial matricial, refinamiento por estado. Límite: Ampliación editorial, no bloque oficial adicional. Modelos numéricos sintéticos sin aeronave identificada.

### Simulación (capítulos 22–23)

Contexto: Código y XML JSBSim fijados. T6 con motor de empuje y direct thruster; sumar cuatro motores B747 y sólo depósitos alimentadores.

Comprobaciones: 44 trims, tres pasos T6, XML, crucero, dos autonomías y balances CSV. Límite: Modelos BETA/ALPHA, sin validación experimental; SAULE sólo procedimiento.

## Correcciones y distinciones materiales
El factor de tabla del motor multiplica empuje y sigue dando fuerza; la potencia física usa TAS. Se corrigió el conteo de cuatro motores B747 y se excluyó un depósito sin alimentación. La lectura del modelo T6 impide atribuirle potencia real al eje de un PT6. En los residuos de trim y convergencia se separaron magnitudes de distintas dimensiones. El ejemplo de hélice usa CP=0.090 para conservar eficiencia dentro del dominio energético. Estos cambios están incorporados en los textos y cálculos vigentes.

Los materiales estudiantiles sólo clasifican familias y dificultad. Dos anclas documentales nativas de un problema no son dos soluciones independientes; las fuentes siguen PENDING. No se han inventado datos de ensayo ni prestaciones certificadas.

## Pendientes reales
Revisión experta de texto y ecuaciones; contrastar modelos de aeronave con datos independientes y sus incertidumbres; refinamiento completo de autonomías; ensayo SAULE; completar trazabilidad semántica por afirmación y auditorías nativas. El libro y los PDF permanecen EN REVISIÓN. Véanse LIMITACIONES.md y los informes nativos sin alterar.
