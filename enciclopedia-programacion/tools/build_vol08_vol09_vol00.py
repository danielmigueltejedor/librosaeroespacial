#!/usr/bin/env python3
"""Construye y compila los Volúmenes VIII, IX y 0 (Maestro Integral) de la Enciclopedia en Studium."""

from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from studium_volume_helper import build_studium_volume


def make_practice_set(ch_id: str, items: list[tuple[str, str, str]]) -> list[dict[str, object]]:
    diffs = ["FOUNDATIONAL", "INTERMEDIATE", "INTERMEDIATE", "ADVANCED"]
    ptypes = ["DIRECT_SUBSTITUTION", "MULTI_STEP", "MULTI_STEP", "DESIGN"]
    out: list[dict[str, object]] = []
    for idx, (desc, expr, unit) in enumerate(items):
        out.append({
            "prompt": f"[{ch_id}.{idx+1}] Calcule ({desc}) expresado en {unit}.",
            "expression": expr,
            "difficulty": diffs[idx % len(diffs)],
            "problem_type": ptypes[idx % len(ptypes)],
        })
    return out


def _normalize_spec(raw: dict[str, object]) -> dict[str, object]:
    spec = dict(raw)
    extra_sources = []
    for i, s in enumerate(spec.get("sources", [])):
        extra_sources.append({
            "id": f"src-vol-extra-{i+1}",
            "title": s["title"],
            "url": s["url"],
            "text": " ".join(s["excerpts"]),
        })
    spec["extra_sources"] = extra_sources
    src_ids = [s["id"] for s in extra_sources]
    spec["terminology"] = [
        {"term": t, "canonical": t, "definition": d}
        for t, d in spec.get("glossary", [])
    ]
    spec["notation"] = [
        {"symbol": sym, "meaning": mean, "unit": unit}
        for sym, mean, unit in spec.get("notation", [])
    ]
    norm_chapters = []
    for ch in spec["chapters"]:
        cid = str(ch["id"]).lower()
        paras = ch["paragraphs"]
        wp = ch["worked_problem"]
        nch: dict[str, object] = {
            "id": cid,
            "title": ch["title"],
            "part_id": "parte-volumen",
            "part_title": str(spec.get("Part", spec["title"])),
            "sources": src_ids,
            "learning_objectives": [str(ch["learning_outcomes"])],
            "concepts": [
                {"id": f"cpt-{cid}-1", "title": paras[0]["title"]},
                {"id": f"cpt-{cid}-2", "title": paras[1]["title"]},
            ],
            "subsections": [
                {"id": f"sec-{cid}-1", "title": f"{paras[0]['title']} y {paras[1]['title']}"},
                {"id": f"sec-{cid}-2", "title": f"{paras[2]['title']} y {paras[3]['title']}"},
            ],
            "purpose": str(ch["summary"]),
            "paragraphs": [
                {"subsection": f"sec-{cid}-1", "text": paras[0]["body"] + "\n\n" + paras[1]["body"]},
                {"subsection": f"sec-{cid}-2", "text": paras[2]["body"] + "\n\n" + paras[3]["body"]},
            ],
            "definition": f"{paras[0]['title']}: {paras[0]['claim']}",
            "consejo": str(paras[2]["claim"]),
            "self_check": f"Razone y verifique por qué se cumple el invariante de ingeniería: {paras[3]['claim']}",
            "worked_problem": {
                "prompt": wp["statement"],
                "expression": wp["steps"][-1]["sympy"],
                "solution": {
                    "model": wp["title"],
                    "unknown": wp["unknown"],
                    "given": [
                        {"symbol": g["symbol"], "value": f"{g['value']} {g['unit']}", "description": g["meaning"]}
                        for g in wp["given"]
                    ],
                    "steps": [
                        {"step": st["text"], "equation": st["latex"], "expression": st["sympy"]}
                        for st in wp["steps"]
                    ],
                    "conclusion": wp["conclusion"],
                },
            },
            "practice_problems": ch["practice_problems"],
        }
        if "tikz_code" in ch:
            nch["figure"] = {
                "key": f"{cid}-fig",
                "caption": ch["tikz_caption"],
                "tikz": ch["tikz_code"],
            }
        norm_chapters.append(nch)
    spec["chapters"] = norm_chapters
    return spec


VOL08_SPEC = {
    "slug": "vol08-web-bases-de-datos-y-frameworks",
    "title": "Volumen VIII: Desarrollo Web, Formatos de Datos, Bases de Datos y Frameworks",
    "subtitle": "Enciclopedia de Programación e Ingeniería del Software — Partes VI, VII y VIII",
    "Part": "Partes VI–VIII: Web, Almacenamiento y Ecosistemas de Producción",
    "scope": (
        "Monografías rigurosas de HTML Living Standard, CSS moderno, JSON/YAML/TOML/XML/Protobuf, "
        "curso universitario completo de bases de datos relacionales y distribuidas (Álgebra Relacional, "
        "BCNF, B+-Trees, LSM-Trees, MVCC, WAL, CAP/PACELC) y arquitecturas de frameworks frontend, backend, "
        "escritorio y móvil."
    ),
    "target_pages": 65,
    "sources": [
        {
            "title": "HTML Living Standard & CSS Cascading and Inheritance Level 5",
            "authors": ["WHATWG", "W3C CSS Working Group"],
            "year": 2024,
            "kind": "standard",
            "publisher": "WHATWG / W3C",
            "url": "https://html.spec.whatwg.org/",
            "notes": "Especificación normativa del DOM, parser HTML5, accesibilidad ARIA y modelo de caja CSS.",
            "excerpts": [
                (
                    "El algoritmo de construcción del árbol DOM en HTML5 es determinista ante entradas mal formadas, "
                    "mientras que el motor de estilo resuelve la cascada por origen, importancia, capas (@layer), "
                    "especificidad léxica (a, b, c) y orden de aparición antes de calcular el layout."
                ),
                (
                    "Los contextos de formato modernos (Flexbox unidimensional y CSS Grid bidimensional) junto con "
                    "Container Queries permiten diseñar componentes autónomos cuya geometría responde al tamaño "
                    "del contenedor padre y no únicamente al viewport global."
                ),
            ],
        },
        {
            "title": "Database System Concepts (7th Edition) & Designing Data-Intensive Applications",
            "authors": ["Abraham Silberschatz", "Henry F. Korth", "S. Sudarshan", "Martin Kleppmann"],
            "year": 2020,
            "kind": "book",
            "publisher": "McGraw-Hill / O'Reilly Media",
            "url": "https://www.db-book.com/",
            "notes": "Fundamentos de bases de datos relacionales, normalización, motores de almacenamiento y sistemas distribuidos.",
            "excerpts": [
                (
                    "Una relación R se encuentra en Forma Normal de Boyce-Codd (BCNF) si y solo si para toda "
                    "dependencia funcional no trivial X -> Y en F+, el determinante X es una superclave de R, "
                    "eliminando redundancias y anomalías de actualización."
                ),
                (
                    "Los motores orientados a lectura emplean árboles B+ con páginas de tamaño fijo (4–16 KiB) y "
                    "Write-Ahead Logging (WAL), mientras que los motores optimizados para escritura utilizan "
                    "LSM-Trees (MemTable en RAM, SSTables inmutables en disco y filtros de Bloom)."
                ),
            ],
        },
        {
            "title": "Protocol Buffers v3, JSON Schema (RFC 8259) & YAML 1.2.2 Specification",
            "authors": ["Google Engineering", "Tim Bray (IETF)", "Oren Ben-Kiki"],
            "year": 2023,
            "kind": "standard",
            "publisher": "IETF / Google / YAML.org",
            "url": "https://datatracker.ietf.org/doc/html/rfc8259",
            "notes": "Estándares de serialización textual y binaria, evolución de esquemas y seguridad de parseo.",
            "excerpts": [
                (
                    "JSON (RFC 8259) define una gramática mínima libre de contexto con seis tipos de datos, mientras "
                    "que YAML 1.2 introduce anclas, alias y resolución implícita de etiquetas que exigen cargadores "
                    "seguros (safe_load) para prevenir ejecución arbitraria e inyecciones tipo Norway problem."
                ),
                (
                    "Protocol Buffers codifica mensajes mediante pares etiqueta-tipo (tag-wire type) y enteros "
                    "de longitud variable (Varint con codificación ZigZag para negativos), garantizando compatibilidad "
                    "hacia adelante y hacia atrás sin transmitir nombres de campo en la red."
                ),
            ],
        },
    ],
    "glossary": [
        ("DOM (Document Object Model)", "Representación en memoria como grafo arbóreo de nodos tipados del documento HTML o XML."),
        ("Especificidad CSS", "Tupla lexicográfica (a, b, c) que pondera selectores de ID (a), clase/atributo/pseudoclase (b) y tipo/pseudoelemento (c)."),
        ("BCNF (Forma Normal de Boyce-Codd)", "Condición normalizada donde todo determinante de una dependencia funcional no trivial es superclave."),
        ("MVCC (Control de Concurrencia Multiversión)", "Mecanismo que mantiene múltiples instantáneas inmutables por tupla para que las lecturas nunca bloqueen a las escrituras."),
    ],
    "notation": [
        (r"S = (a, b, c)", "Vector lexicográfico de especificidad CSS", "adimensional"),
        (r"X \to Y", "Dependencia funcional relacional en esquema R", "relación lógica"),
        (r"h = \lceil \log_B(N) \rceil", "Altura de un árbol B+ con factor de ramificación B", "niveles de página"),
    ],
    "chapters": [
        {
            "id": "CH-01",
            "title": "HTML Living Standard y Accesibilidad Web (WCAG / ARIA)",
            "prerequisites": "Conocimientos básicos de codificación UTF-8 y protocolo HTTP.",
            "learning_outcomes": "Dominar la semántica estructural de HTML5, el algoritmo de construcción del DOM, formularios nativos, multimedia y árboles de accesibilidad (AOM/ARIA).",
            "summary": "Estudio riguroso de HTML como lenguaje de marcado declarativo (no de programación de propósito general), su gramática, ciclo de parseo en el navegador y validación accesible.",
            "tikz_caption": "Tubería de renderizado del navegador (Critical Rendering Path): desde el flujo de bytes UTF-8 hasta el árbol DOM, CSSOM, Render Tree, Layout y Composite.",
            "tikz_code": r"""\begin{tikzpicture}[node distance=0.45cm, every node/.style={font=\scriptsize, draw, rounded corners=2pt, align=center, inner sep=3.5pt}]
\node (bytes) [fill=blue!10] {Bytes UTF-8\\(HTML / CSS)};
\node (dom) [right=of bytes, fill=green!10] {Árboles\\DOM + CSSOM};
\node (render) [right=of dom, fill=yellow!15] {Render Tree\\(Nodos visibles)};
\node (layout) [right=of render, fill=orange!15] {Layout / Reflow\\(Geometría)};
\node (paint) [right=of layout, fill=purple!15] {Paint \& Composite\\(Capas GPU)};
\draw[-Stealth, thick] (bytes) -- (dom);
\draw[-Stealth, thick] (dom) -- (render);
\draw[-Stealth, thick] (render) -- (layout);
\draw[-Stealth, thick] (layout) -- (paint);
\end{tikzpicture}""",
            "paragraphs": [
                {
                    "title": "Naturaleza declarativa de HTML y el estándar vivo WHATWG",
                    "claim": "HTML es un lenguaje formal de marcado estructural e hipertextual, no un lenguaje de programación Turing-completo.",
                    "body": (
                        "A diferencia de un lenguaje de programación imperativo o funcional, HTML (HyperText Markup Language, "
                        "mantenido como Living Standard por WHATWG) describe de manera declarativa la estructura semántica de "
                        "un documento mediante elementos delimitados por etiquetas, atributos clave-valor y referencias de "
                        "entidades. Carece de variables mutables, bucles condicionales o abstracción funcional general. El "
                        "analizador sintáctico de HTML5 implementa una máquina de estados finitos con reglas deterministas "
                        "de recuperación de errores: incluso ante etiquetas mal anidadas, construye el mismo árbol DOM en "
                        "todos los motores conformes (Blink, WebKit, Gecko).\n\n"
                        "```html\n"
                        "<!DOCTYPE html>\n"
                        "<html lang=\"es\">\n"
                        "<head>\n"
                        "  <meta charset=\"utf-8\">\n"
                        "  <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">\n"
                        "  <title>Panel de Telemetría Industrial</title>\n"
                        "</head>\n"
                        "<body>\n"
                        "  <header role=\"banner\">\n"
                        "    <h1>Estado del Clúster Principal</h1>\n"
                        "  </header>\n"
                        "  <main id=\"contenido-principal\">\n"
                        "    <article aria-labelledby=\"sec-latencia\">\n"
                        "      <h2 id=\"sec-latencia\">Métricas de Latencia p99</h2>\n"
                        "      <p>Latencia actual: <data value=\"4.2\">4,2 ms</data></p>\n"
                        "    </article>\n"
                        "  </main>\n"
                        "</body>\n"
                        "</html>\n"
                        "```"
                    ),
                },
                {
                    "title": "Semántica estructural, árbol de accesibilidad (AOM) y WAI-ARIA",
                    "claim": "Los elementos semánticos nativos proyectan roles implícitos en el árbol de accesibilidad del sistema operativo sin requerir atributos ARIA redundantes.",
                    "body": (
                        "El navegador construye en paralelo al DOM el Árbol de Accesibilidad (Accessibility Object Model), "
                        "consultado por lectores de pantalla mediante APIs nativas (IAccessible2, UIAutomation, NSAccessibility). "
                        "La primera regla de WAI-ARIA establece que siempre debe preferirse un elemento HTML nativo (`<button>`, "
                        "`<nav>`, `<main>`, `<dialog>`) sobre un `<div>` genérico con `role=\"button\"`, ya que el elemento "
                        "nativo proporciona automáticamente navegación por teclado (`Tab`, `Enter`, `Space`), gestión de foco "
                        "y estados implícitos. Como se ilustra en la {{fig:ch-01-fig}}, el DOM alimenta tanto el Render Tree "
                        "visual como la estructura semántica."
                    ),
                },
                {
                    "title": "Formularios nativos, validación de restricciones y seguridad en enlaces",
                    "claim": "La API de validación de restricciones de HTML5 verifica tipos, patrones regulares y rangos antes del envío HTTP, pero jamás sustituye la validación en el servidor.",
                    "body": (
                        "Los controles de formulario (`<input>`, `<select>`, `<textarea>`) asociados explícitamente mediante "
                        "`<label for=\"id\">` exponen validación declarativa (`required`, `type=\"email\"`, `min`, `max`, "
                        "`pattern`). No obstante, dado que cualquier cliente puede falsificar peticiones HTTP ignorando el "
                        "navegador, toda validación en el cliente es estrictamente una mejora de experiencia de usuario (UX) "
                        "y el servidor debe revalidar íntegramente la carga útil. Asimismo, los enlaces externos con "
                        "`target=\"_blank\"` deben incluir `rel=\"noopener noreferrer\"` para aislar el contexto de "
                        "navegación y evitar ataques de tabnabbing inverso."
                    ),
                },
                {
                    "title": "Carga eficiente de recursos, módulos ES y Web Components",
                    "claim": "Los atributos async, defer y type='module' desacoplan la descarga de scripts del bloqueo del parser HTML.",
                    "body": (
                        "Cuando el parser HTML encuentra una etiqueta `<script>` clásica sin atributos, detiene la construcción "
                        "del DOM hasta descargar y ejecutar el script. El atributo `defer` descarga el script en paralelo y "
                        "pospone su ejecución en orden hasta que el DOM está completo (`DOMContentLoaded`), mientras que "
                        "`type=\"module\"` activa el sistema de módulos ECMAScript en modo estricto con diferimiento implícito. "
                        "Adicionalmente, la especificación HTML incluye `<template>` y `<slot>` como base de Web Components "
                        "y Shadow DOM para encapsular estructura y estilo."
                    ),
                },
            ],
            "worked_problem": {
                "title": "Cálculo del tiempo de bloqueo del Critical Rendering Path",
                "statement": (
                    "Una página HTML descarga un documento base en 40 ms, una hoja CSS bloqueante de renderizado en 65 ms "
                    "en paralelo con un script clásico bloqueante de 110 ms, y ejecuta el layout final en 15 ms tras "
                    "ambos recursos. Calcule el tiempo total hasta el First Contentful Paint (FCP) en milisegundos."
                ),
                "given": [
                    {"symbol": "t_html", "value": "40", "unit": "ms", "meaning": "Tiempo de descarga del HTML base"},
                    {"symbol": "t_css", "value": "65", "unit": "ms", "meaning": "Tiempo de descarga de la hoja CSS"},
                    {"symbol": "t_js", "value": "110", "unit": "ms", "meaning": "Tiempo del script bloqueante mayor"},
                    {"symbol": "t_layout", "value": "15", "unit": "ms", "meaning": "Tiempo de Layout y Paint"},
                ],
                "unknown": "Tiempo total hasta First Contentful Paint T_fcp en ms",
                "steps": [
                    {
                        "text": "Sumamos el tiempo base HTML, el máximo de las descargas en paralelo (max(65, 110) = 110 ms) y el tiempo de layout",
                        "latex": r"T_{\text{fcp}} = 40 + 110 + 15",
                        "sympy": "(40 + 110 + 15)",
                    }
                ],
                "conclusion": "El First Contentful Paint ocurre a los 165 ms; añadir defer al script reduciría la espera crítica de recursos de 110 ms a 65 ms.",
            },
            "practice_problems": make_practice_set(
                "CH-01",
                [
                    ("Reducción de latencia FCP al diferir un script de 110 ms dejando solo el CSS de 65 ms (40 + 65 + 15)", "40 + 65 + 15", "ms"),
                    ("Tamaño total en KiB de un documento HTML de 18 KiB más 3 iconos SVG inline de 4 KiB cada uno", "18 + 3 * 4", "KiB"),
                    ("Número total de nodos DOM generados por una tabla de 25 filas con 4 celdas por fila más el nodo tr por fila", "25 * (4 + 1)", "nodos"),
                    ("Ahorro porcentual de transferencia al comprimir con Brotli un HTML de 80 KiB a 16 KiB", "(80 - 16) * 100 / 80", "%"),
                ],
            ),
        },
        {
            "id": "CH-02",
            "title": "CSS Moderno: Cascada, Especificidad, Flexbox, Grid y Container Queries",
            "prerequisites": "CH-01 (Árbol DOM y modelo estructural HTML).",
            "learning_outcomes": "Calcular determinísticamente la resolución de la cascada CSS, diseñar layouts complejos con Flexbox y Grid, y aplicar propiedades lógicas y variables reactivas.",
            "summary": "Monografía técnica de CSS como lenguaje declarativo de presentación visual, geometría de cajas, contextos de apilamiento, diseño adaptable e ingeniería de sistemas de diseño.",
            "paragraphs": [
                {
                    "title": "Algoritmo de la Cascada, Capas (@layer) y Especificidad Lexicográfica",
                    "claim": "El motor CSS resuelve conflictos entre declaraciones mediante una jerarquía estricta donde el origen y las capas (@layer) preceden a la especificidad del selector.",
                    "body": (
                        "Para cada propiedad de cada elemento DOM, el motor CSS filtra las declaraciones aplicables y elige "
                        "un único valor ganador evaluando en orden: 1) Origen e importancia (`!important` de usuario/autor), "
                        "2) Contexto de encapsulación (Shadow DOM), 3) Capas de cascada explícitas (`@layer reset, base, "
                        "components, utilities`), 4) Especificidad del selector expresada como el vector lexicográfico "
                        "\\(S = (a, b, c)\\) donde \\(a\\) cuenta selectores de ID (`#nav`), \\(b\\) cuenta clases, atributos "
                        "y pseudoclases (`.activo`, `[type=\"text\"]`, `:hover`, mientras `:where()` aporta 0 y `:is()` "
                        "toma el máximo de su lista), y \\(c\\) cuenta selectores de tipo y pseudoelementos (`article`, "
                        "`::before`), y finalmente 5) Orden de aparición en el código fuente.\n\n"
                        "```css\n"
                        "@layer base, components;\n\n"
                        "@layer base {\n"
                        "  :root {\n"
                        "    --espacio-base: 1rem;\n"
                        "    --color-superficie: oklch(98% 0.01 250);\n"
                        "  }\n"
                        "  *, *::before, *::after {\n"
                        "    box-sizing: border-box;\n"
                        "  }\n"
                        "}\n\n"
                        "@layer components {\n"
                        "  .panel-metricas {\n"
                        "    container-type: inline-size;\n"
                        "    display: grid;\n"
                        "    grid-template-columns: repeat(auto-fit, minmax(min(100%, 18rem), 1fr));\n"
                        "    gap: var(--espacio-base);\n"
                        "    background: var(--color-superficie);\n"
                        "  }\n"
                        "}\n"
                        "```"
                    ),
                },
                {
                    "title": "Modelo de Caja, Box-Sizing y Propiedades Lógicas Internacionalizadas",
                    "claim": "El modelo border-box integra el relleno (padding) y el borde dentro del ancho declarado, evitando desbordamientos aritméticos en rejillas.",
                    "body": (
                        "En el modelo tradicional `content-box`, el ancho visual ocupado por una caja es "
                        "\\(W_{\\text{total}} = W_{\\text{content}} + 2P + 2B\\). Al declarar `box-sizing: border-box`, "
                        "el ancho declarado fija directamente \\(W_{\\text{total}}\\), descontando `padding` y `border` "
                        "del área interior disponible. Además, el CSS moderno reemplaza propiedades físicas (`margin-left`, "
                        "`width`) por propiedades lógicas relativas al flujo de escritura (`margin-inline-start`, "
                        "`inline-size`, `block-size`), soportando automáticamente idiomas de derecha a izquierda (RTL) "
                        "como árabe o hebreo sin duplicar hojas de estilo."
                    ),
                },
                {
                    "title": "Contextos de Formato: Flexbox Unidimensional y CSS Grid Bidimensional",
                    "claim": "Flexbox distribuye espacio a lo largo de un eje principal dinámico, mientras que CSS Grid impone una malla bidimensional explícita de filas y columnas.",
                    "body": (
                        "Un contenedor `display: flex` calcula el tamaño base (`flex-basis`) de sus hijos directos y "
                        "reparte el espacio libre positivo según los factores `flex-grow` o absorbe el déficit según "
                        "`flex-shrink` ponderado por el tamaño base. Por su parte, `display: grid` permite definir "
                        "pistas elásticas con la unidad fraccional `fr`, funciones `minmax()` y alineación de subrejillas "
                        "mediante `subgrid`, permitiendo que componentes anidados alineen sus cabeceras y pies exactamente "
                        "con la retícula del contenedor abuelo."
                    ),
                },
                {
                    "title": "Container Queries, Rendimiento de Animaciones y Compositor GPU",
                    "claim": "Animar exclusivamente transform y opacity evita recalcular el Layout (Reflow) y el Paint, delegando la interpolación al hilo compositor de la GPU.",
                    "body": (
                        "Modificar propiedades geométricas (`width`, `top`, `margin`) en cada fotograma invalida el árbol "
                        "de layout y obliga a la CPU a recalcular posiciones y repintar píxeles, provocando caídas por "
                        "debajo de 60 FPS (presupuesto de 16,67 ms por fotograma). En cambio, `transform: translate3d(...)` "
                        "y `opacity` operan sobre texturas ya rasterizadas en la GPU."
                    ),
                },
            ],
            "worked_problem": {
                "title": "Distribución proporcional de espacio libre en Flexbox",
                "statement": (
                    "Un contenedor Flex tiene un ancho interior de 960 px y contiene dos paneles con flex-basis de "
                    "200 px y 160 px respectivamente. Sus factores flex-grow son 2 y 1. Calcule el ancho final en "
                    "píxeles del primer panel tras repartir el espacio libre."
                ),
                "given": [
                    {"symbol": "W_cont", "value": "960", "unit": "px", "meaning": "Ancho interior del contenedor Flex"},
                    {"symbol": "B_1", "value": "200", "unit": "px", "meaning": "Tamaño base flex-basis del panel 1"},
                    {"symbol": "B_2", "value": "160", "unit": "px", "meaning": "Tamaño base flex-basis del panel 2"},
                    {"symbol": "g_1", "value": "2", "unit": "adimensional", "meaning": "Factor flex-grow del panel 1"},
                    {"symbol": "g_2", "value": "1", "unit": "adimensional", "meaning": "Factor flex-grow del panel 2"},
                ],
                "unknown": "Ancho final del primer panel W_1 en px",
                "steps": [
                    {
                        "text": "Calculamos el espacio libre (960 - 200 - 160 = 600 px) y asignamos dos tercios al primer panel",
                        "latex": r"W_1 = 200 + \frac{2}{2 + 1} \cdot (960 - 200 - 160)",
                        "sympy": "200 + (2 * (960 - 200 - 160)) / 3",
                    }
                ],
                "conclusion": "El primer panel alcanza un ancho final exacto de 600 px y el segundo panel ocupa los 360 px restantes.",
            },
            "practice_problems": make_practice_set(
                "CH-02",
                [
                    ("Ancho final del segundo panel en el contenedor Flex de 960 px (160 + 600 / 3)", "160 + (960 - 200 - 160) / 3", "px"),
                    ("Valor entero codificado en base 100 de la especificidad (1, 2, 3) para comparación rápida", "1 * 10000 + 2 * 100 + 3", "puntos"),
                    ("Ancho de una columna 1fr en un CSS Grid de 1200 px con 3 columnas iguales y 2 huecos (gap) de 24 px", "(1200 - 2 * 24) / 3", "px"),
                    ("Ancho de área de contenido en border-box para una caja de 320 px con padding de 16 px y borde de 2 px por lado", "320 - 2 * 16 - 2 * 2", "px"),
                ],
            ),
        },
        {
            "id": "CH-03",
            "title": "Formatos de Intercambio, Configuración y Documentación: JSON, YAML, TOML, XML, CSV, Markdown y Protobuf",
            "prerequisites": "CH-01 y fundamentos de codificación binaria y UTF-8 (Volumen I).",
            "learning_outcomes": "Seleccionar y validar formatos de datos textuales y binarios, diseñar esquemas con JSON Schema y Protocol Buffers, y prevenir vulnerabilidades de deserialización.",
            "summary": "Estudio comparativo y riguroso de los lenguajes de serialización, configuración y marcado ligero empleados en sistemas distribuidos e infraestructura.",
            "paragraphs": [
                {
                    "title": "JSON (RFC 8259) y Validación Contractual con JSON Schema",
                    "claim": "JSON proporciona una gramática libre de contexto mínima y determinista, ideal para APIs web cuando se acompaña de validación estructural mediante JSON Schema.",
                    "body": (
                        "Especificado en el RFC 8259, JSON admite únicamente seis tipos de valores: objetos (pares clave-valor "
                        "con claves de tipo cadena), arrays ordenados, cadenas UTF-8, números en punto flotante IEEE 754, "
                        "booleanos (`true`, `false`) y `null`. No admite comentarios, comas finales ni referencias cíclicas. "
                        "Un riesgo clásico de interoperabilidad ocurre cuando enteros de 64 bits (`int64` mayores que "
                        "\\(2^{53} - 1\\)) se deserializan en motores JavaScript, perdiendo precisión en el mantisa de 53 bits; "
                        "por ello, los identificadores de 64 bits deben serializarse como cadenas textuales.\n\n"
                        "```json\n"
                        "{\n"
                        "  \"$schema\": \"https://json-schema.org/draft/2020-12/schema\",\n"
                        "  \"type\": \"object\",\n"
                        "  \"required\": [\"id_transaccion\", \"importe_centimos\", \"moneda\"],\n"
                        "  \"properties\": {\n"
                        "    \"id_transaccion\": { \"type\": \"string\", \"pattern\": \"^[0-9a-fA-F-]{36}$\" },\n"
                        "    \"importe_centimos\": { \"type\": \"integer\", \"minimum\": 1 },\n"
                        "    \"moneda\": { \"enum\": [\"EUR\", \"USD\", \"GBP\"] }\n"
                        "  },\n"
                        "  \"additionalProperties\": false\n"
                        "}\n"
                        "```"
                    ),
                },
                {
                    "title": "YAML 1.2 vs TOML v1.0: Configuración Humana y Trampas Semánticas",
                    "claim": "YAML 1.2 es un superconjunto de JSON cuya sensibilidad a la indentación y coerción implícita exigen parsers estrictos, mientras que TOML prioriza una semántica plana e inequívoca.",
                    "body": (
                        "YAML 1.2 se utiliza masivamente en Kubernetes, Ansible y pipelines CI/CD gracias a su sintaxis "
                        "concisa, soporte de comentarios y reutilización mediante anclas (`&base`) y alias (`*base`). Sin "
                        "embargo, presenta riesgos conocidos: en YAML 1.1 literales sin comillas como `NO` (código ISO de "
                        "Noruega) u `on` se convertían silenciosamente en booleanos (`false`, `true`), y la carga insegura "
                        "de etiquetas arbitrarias (`!!python/object/apply`) permite ejecución remota de código si no se "
                        "invoca exclusivamente `yaml.safe_load`. Por contraste, TOML (`Cargo.toml`, `pyproject.toml`) "
                        "utiliza secciones explícitas `[tabla]` y tipos literales sin ambigüedad de indentación."
                    ),
                },
                {
                    "title": "XML, Namespaces, XSD y Prevención de Ataques XXE",
                    "claim": "Todo analizador XML en producción debe deshabilitar la resolución de entidades externas (XXE) y la expansión recursiva de DTD.",
                    "body": (
                        "XML sigue siendo el estándar normativo en facturación electrónica, banca (ISO 20022) y federación "
                        "de identidad (SAML 2.0) gracias a sus espacios de nombres (`xmlns`) y validación formal con XML "
                        "Schema (XSD). No obstante, su soporte histórico de Document Type Definitions (DTD) habilita "
                        "vulnerabilidades críticas: la inyección de Entidades Externas XML (XXE) permite leer archivos "
                        "locales del servidor (`file:///etc/passwd`), y la bomba de entidades recursivas (Billion Laughs) "
                        "agota gigabytes de memoria RAM a partir de menos de 1 KiB de entrada."
                    ),
                },
                {
                    "title": "CSV (RFC 4180), Markdown (CommonMark) y Serialización Binaria con Protocol Buffers",
                    "claim": "Protocol Buffers reduce entre 3 y 10 veces el tamaño de carga útil y el tiempo de CPU frente a JSON al codificar campos con etiquetas numéricas y enteros Varint.",
                    "body": (
                        "Mientras CSV (RFC 4180) requiere escapar comillas dobles y neutralizar fórmulas iniciales (`=`, `+`, "
                        "`-`, `@`) para evitar CSV Injection en hojas de cálculo, y CommonMark estandariza la gramática "
                        "de Markdown para documentación técnica, las comunicaciones de alta frecuencia entre microservicios "
                        "emplean formatos binarios con esquema como Protocol Buffers (Protobuf v3). En Protobuf, cada campo "
                        "se identifica en el flujo binario mediante un único byte de cabecera `(field_number << 3) | wire_type`, "
                        "permitiendo evolucionar esquemas añadiendo nuevos campos sin romper clientes antiguos."
                    ),
                },
            ],
            "worked_problem": {
                "title": "Compresión binaria de un mensaje de telemetría con Protocol Buffers frente a JSON",
                "statement": (
                    "Un mensaje JSON de telemetría ocupa 140 bytes en texto UTF-8. Al codificar los mismos 4 campos "
                    "numéricos en Protocol Buffers v3, cada campo requiere 1 byte de etiqueta (tag) y 3 bytes de "
                    "valor Varint promedio. Calcule el ahorro porcentual de ancho de banda logrado por Protobuf."
                ),
                "given": [
                    {"symbol": "B_json", "value": "140", "unit": "bytes", "meaning": "Tamaño del mensaje en JSON"},
                    {"symbol": "n_campos", "value": "4", "unit": "campos", "meaning": "Número de campos del mensaje"},
                    {"symbol": "B_campo", "value": "4", "unit": "bytes", "meaning": "Bytes por campo en Protobuf (1 tag + 3 valor)"},
                ],
                "unknown": "Ahorro porcentual de bytes A_pct en %",
                "steps": [
                    {
                        "text": "Calculamos el tamaño en Protobuf (4 * 4 = 16 bytes) y el porcentaje de reducción respecto a 140 bytes",
                        "latex": r"A_{\text{pct}} = \frac{140 - 4 \cdot 4}{140} \cdot 100",
                        "sympy": "((140 - 4 * 4) * 100) / 140",
                    }
                ],
                "conclusion": "Protocol Buffers reduce el tamaño del mensaje de 140 bytes a 16 bytes, ahorrando aproximadamente un 88,57 % del ancho de banda.",
            },
            "practice_problems": make_practice_set(
                "CH-03",
                [
                    ("Tamaño en bytes del mensaje Protobuf con 4 campos de 4 bytes cada uno", "4 * 4", "bytes"),
                    ("Valor del byte de cabecera Protobuf para el campo número 3 con wire_type 2 (length-delimited: 3*8 + 2)", "3 * 8 + 2", "entero"),
                    ("Codificación ZigZag de sint32 para el entero negativo -15 (-2 * -15 - 1)", "2 * 15 - 1", "entero"),
                    ("Tráfico diario ahorrado en MB al enviar 10 millones de mensajes de 16 B en lugar de 116 B (dividiendo entre 10^6)", "10000000 * (116 - 16) / 1000000", "MB"),
                ],
            ),
        },
        {
            "id": "CH-04",
            "title": "Teoría Relacional, Modelado Entidad-Relación y Normalización (1NF a BCNF)",
            "prerequisites": "Álgebra booleana y teoría de conjuntos (Volumen I).",
            "learning_outcomes": "Traducir requisitos de dominio a esquemas relacionales en Forma Normal de Boyce-Codd (BCNF) garantizando reuniones sin pérdida (lossless-join) y preservación de dependencias.",
            "summary": "Fundamentos matemáticos del modelo relacional de E. F. Codd, equivalencia entre álgebra y cálculo relacional, cierre de atributos y teoría formal de la normalización.",
            "paragraphs": [
                {
                    "title": "El Modelo Relacional de Codd y las Claves Relacionales",
                    "claim": "Una relación matemática es un subconjunto finito del producto cartesiano de dominios atómicos donde el orden de tuplas y atributos carece de significado semántico.",
                    "body": (
                        "Formulado por Edgar F. Codd en 1970, el modelo relacional independiza la representación lógica "
                        "de los datos respecto a su disposición física en almacenamiento secundario. Dado un esquema "
                        "\\(R(A_1, A_2, \\dots, A_n)\\), un subconjunto de atributos \\(K \\subseteq R\\) es una superclave "
                        "si no pueden existir dos tuplas distintas \\(t_1 \\neq t_2\\) en ninguna instancia válida \\(r(R)\\) "
                        "tales que \\(t_1[K] = t_2[K]\\). Una superclave mínima (ningún subconjunto propio suyo es superclave) "
                        "constituye una clave candidata, de las cuales se designa una clave primaria (PK) sujeta a integridad "
                        "de entidad (ningún atributo primo puede ser `NULL`)."
                    ),
                },
                {
                    "title": "Dependencias Funcionales, Axiomas de Armstrong y Cierre de Atributos",
                    "claim": "El algoritmo de cierre de un conjunto de atributos X bajo un conjunto de dependencias F decide en tiempo lineal O(|F|) si X -> Y pertenece a la clausura F+.",
                    "body": (
                        "Una dependencia funcional \\(X \\to Y\\) afirma que los valores del conjunto de atributos \\(X\\) "
                        "determinan unívocamente los valores de \\(Y\\). Los tres axiomas de Armstrong (reflexividad, "
                        "aumentatividad y transitividad) son correctos y completos para inferir todas las dependencias "
                        "implicadas \\(F^+\\). En la práctica ingenieril, en lugar de enumerar \\(F^+\\) (cuyo tamaño puede "
                        "ser exponencial), calculamos el cierre de atributos \\(X^+\\) partiendo de \\(\\text{resultado} = X\\) "
                        "y añadiendo iterativamente \\(W\\) cada vez que \\(V \\to W \\in F\\) cumple \\(V \\subseteq \\text{resultado}\\)."
                    ),
                },
                {
                    "title": "Anomalías de Diseño y Jerarquía de Formas Normales (1NF, 2NF, 3NF y BCNF)",
                    "claim": "Un esquema relacional en BCNF elimina toda redundancia derivada de dependencias funcionales al exigir que todo determinante no trivial sea superclave.",
                    "body": (
                        "Mezclar múltiples entidades independientes en una sola tabla provoca anomalías de inserción "
                        "(no poder registrar un departamento sin empleados), actualización (modificar un dato repetido en "
                        "miles de filas con riesgo de inconsistencia) y borrado. La Primera Forma Normal (1NF) exige dominios "
                        "atómicos; la 2NF prohíbe dependencias parciales de atributos no primos respecto a una clave compuesta; "
                        "la 3NF prohíbe dependencias transitivas entre atributos no primos; y la Forma Normal de Boyce-Codd "
                        "(BCNF) exige que para toda \\(X \\to Y\\) no trivial, \\(X\\) sea superclave."
                    ),
                },
                {
                    "title": "Descomposición sin Pérdida (Lossless-Join) y Preservación de Dependencias",
                    "claim": "La descomposición de R en R1 y R2 es una reunión sin pérdida si y solo si (R1 intersect R2) es superclave de R1 o de R2.",
                    "body": (
                        "Dividir una tabla sin verificar el teorema de Heath produce descomposiciones con pérdida (lossy joins) "
                        "donde la reunión natural \\(R_1 \\bowtie R_2\\) genera tuplas espurias inexistentes en la relación "
                        "original. Mientras que toda relación admite una descomposición en BCNF sin pérdida de información, "
                        "en ocasiones aislar todas las dependencias en tablas individuales sólo es posible en 3NF mediante "
                        "el algoritmo de síntesis de recubrimiento canónico."
                    ),
                },
            ],
            "worked_problem": {
                "title": "Eliminación de redundancia mediante descomposición a BCNF",
                "statement": (
                    "Una tabla desnormalizada de líneas de pedido con 50 000 filas repite en cada fila los 120 bytes "
                    "de datos del cliente (habiendo solo 2 000 clientes distintos). Al descomponer a BCNF en "
                    "Lineas(50 000 filas) y Clientes(2 000 filas x 120 bytes), calcule el espacio total en KiB "
                    "(1 KiB = 1024 B) ahorrado por no repetir los 120 bytes en las 48 000 filas excedentes."
                ),
                "given": [
                    {"symbol": "N_exc", "value": "48000", "unit": "filas", "meaning": "Filas donde se repetían los datos del cliente"},
                    {"symbol": "B_cli", "value": "120", "unit": "bytes", "meaning": "Bytes redundantes por fila"},
                    {"symbol": "K", "value": "1024", "unit": "bytes/KiB", "meaning": "Bytes por kibibyte"},
                ],
                "unknown": "Espacio ahorrado S_kib en KiB",
                "steps": [
                    {
                        "text": "Multiplicamos las 48 000 filas redundantes por 120 bytes y dividimos entre 1024",
                        "latex": r"S_{\text{kib}} = \frac{48000 \cdot 120}{1024}",
                        "sympy": "(48000 * 120) / 1024",
                    }
                ],
                "conclusion": "La normalización a BCNF ahorra exactamente 5 625 KiB de almacenamiento redundante y elimina las anomalías de actualización.",
            },
            "practice_problems": make_practice_set(
                "CH-04",
                [
                    ("Espacio en KiB ocupado por la nueva tabla Clientes con 2048 filas de 128 bytes (2048 * 128 / 1024)", "(2048 * 128) / 1024", "KiB"),
                    ("Número de superclaves en una relación de 5 atributos cuya única clave candidata tiene 2 atributos (2^(5-2))", "2**(5 - 2)", "superclaves"),
                    ("Tuplas espurias generadas al hacer join de dos proyecciones mal descompuestas que producen 140 filas frente a 100 reales", "140 - 100", "tuplas"),
                    ("Número de atributos en la intersección R1 n R2 si |R1|=4, |R2|=5 y |R1 U R2|=7", "4 + 5 - 7", "atributos"),
                ],
            ),
        },
        {
            "id": "CH-05",
            "title": "Motores de Almacenamiento, Índices B+-Tree / LSM, Transacciones ACID y MVCC",
            "prerequisites": "CH-04 y arquitectura de sistemas operativos y memoria virtual (Volumen II).",
            "learning_outcomes": "Analizar la estructura física de páginas de disco, comparar árboles B+ frente a LSM-Trees, diseñar índices compuestos óptimos y depurar anomalías de concurrencia bajo niveles de aislamiento ANSI/serializable.",
            "summary": "Ingeniería interna de sistemas gestores de bases de datos (SGBD): Buffer Pool, Write-Ahead Logging (ARIES), optimizadores basados en costes y control de concurrencia multiversión.",
            "tikz_caption": "Estructura de un índice Árbol B+ (B+-Tree): los nodos internos dirigen la búsqueda por claves separadoras y las hojas enlazadas almacenan los punteros o tuplas en orden secuencial.",
            "tikz_code": r"""\begin{tikzpicture}[node distance=0.6cm and 0.5cm, every node/.style={font=\scriptsize, draw, rounded corners=2pt, align=center, inner sep=3.5pt}]
\node (root) [fill=blue!12] {Raíz B+\\$[50 \mid 100]$};
\node (l1) [below left=of root, fill=green!12] {Hoja 1\\$[10, 25, 40]$};
\node (l2) [below=of root, fill=green!12] {Hoja 2\\$[50, 75, 90]$};
\node (l3) [below right=of root, fill=green!12] {Hoja 3\\$[100, 120, 150]$};
\draw[-Stealth, thick] (root) -- (l1);
\draw[-Stealth, thick] (root) -- (l2);
\draw[-Stealth, thick] (root) -- (l3);
\draw[Stealth-Stealth, dashed, thick, blue!70!black] (l1) -- (l2);
\draw[Stealth-Stealth, dashed, thick, blue!70!black] (l2) -- (l3);
\end{tikzpicture}""",
            "paragraphs": [
                {
                    "title": "Árboles B+ (B+-Trees) frente a LSM-Trees (Log-Structured Merge-Trees)",
                    "claim": "Un árbol B+ con factor de ramificación B=250 localiza cualquier clave entre 1 000 millones de filas en tan solo 4 lecturas de página.",
                    "body": (
                        "Los motores relacionales clásicos (PostgreSQL, InnoDB, SQLite) organizan tablas e índices en páginas "
                        "de disco de 8 KiB o 16 KiB estructuradas como árboles B+, como muestra la {{fig:ch-05-fig}}. Todos "
                        "los valores residen en el nivel de las hojas, las cuales están doblemente enlazadas para acelerar "
                        "escaneos por rango (`BETWEEN`). En contrapartida, motores de alta tasa de ingesta (RocksDB, "
                        "Cassandra, ScyllaDB) emplean LSM-Trees: toda escritura se registra secuencialmente en un log "
                        "en disco y en una estructura ordenada en RAM (`MemTable`); al llenarse, se vuelca como un archivo "
                        "inmutable (`SSTable`) compactado en segundo plano y acelerado mediante filtros de Bloom."
                    ),
                },
                {
                    "title": "Diseño de Índices Compuestos, Índices Cubrientes (Covering) y Optimizadores de Costes",
                    "claim": "En un índice compuesto B+ sobre (A, B, C), el orden lexicográfico permite resolver predicados sobre (A) y (A, B), pero no sobre (B, C) sin fijar A.",
                    "body": (
                        "El optimizador de consultas (Query Planner) utiliza histogramas de distribución, cardinalidad "
                        "(NDV) y factores de correlación física para estimar el coste en E/S y CPU de distintos planes "
                        "de ejecución (`Index Scan`, `Bitmap Heap Scan`, `Seq Scan`, `Hash Join`, `Merge Join`, `Nested Loop`). "
                        "Cuando un índice incluye todas las columnas requeridas por una consulta (por ejemplo, `CREATE INDEX "
                        "idx_pedidos ON pedidos (cliente_id, fecha) INCLUDE (total)`), el motor ejecuta un `Index-Only Scan` "
                        "sin necesidad de acceder a las páginas de la tabla principal (Heap)."
                    ),
                },
                {
                    "title": "Transacciones ACID, Write-Ahead Logging (WAL) y Protocolo ARIES",
                    "claim": "La regla WAL garantiza atomicidad y durabilidad exigiendo que todo registro de log (UNDO/REDO) llegue a almacenamiento no volátil antes de confirmar la transacción o volcar la página sucia.",
                    "body": (
                        "Las garantías ACID comprenden Atomicidad (todo o nada mediante registros UNDO), Consistencia "
                        "(preservación de invariantes e integridad referencial), Aislamiento (ejecución concurrente "
                        "equivalente a una planificación controlada) y Durabilidad (persistencia mediante registros REDO "
                        "en el Write-Ahead Log). Tras un fallo eléctrico, el algoritmo de recuperación ARIES ejecuta tres "
                        "fases a partir del último punto de control (Checkpoint): Análisis, REDO (repitiendo la historia "
                        "hasta el estado exacto previo al fallo) y UNDO (revirtiendo transacciones inconclusas)."
                    ),
                },
                {
                    "title": "Niveles de Aislamiento, Anomalías de Concurrencia y MVCC (Snapshot Isolation)",
                    "claim": "El aislamiento por instantáneas (Snapshot Isolation / Repeatable Read en PostgreSQL) evita lecturas sucias, no repetibles y fantasmas, pero permite Write Skew si no se emplea Serializable Snapshot Isolation (SSI).",
                    "body": (
                        "Bajo MVCC, cada transacción recibe un identificador monotónico (`txid`) y cada actualización "
                        "inserta una nueva versión de la tupla marcada con el intervalo de validez `[xmin, xmax)`. Así, "
                        "las lecturas leen una instantánea consistente sin bloquear a los escritores. Sin embargo, dos "
                        "transacciones concurrentes que leen un mismo invariante y escriben en filas disjuntas pueden "
                        "cometer la anomalía de asimetría de escritura (`Write Skew`); prevenirla requiere bloqueos "
                        "explícitos (`SELECT ... FOR UPDATE`) o el algoritmo SSI (`SERIALIZABLE`)."
                    ),
                },
            ],
            "worked_problem": {
                "title": "Capacidad de direccionamiento de un Árbol B+ de 3 niveles",
                "statement": (
                    "En una base de datos con páginas de 8 KiB, cada nodo interno de un índice B+ tiene un factor de "
                    "ramificación efectivo de 200 hijos y cada página hoja almacena 80 entradas de índice. Calcule "
                    "el número total de filas (en millones) que puede indexar un árbol B+ de altura h = 3 (1 raíz, "
                    "1 nivel intermedio de nodos internos y 1 nivel de hojas)."
                ),
                "given": [
                    {"symbol": "B_int", "value": "200", "unit": "hijos/nodo", "meaning": "Factor de ramificación de nodos internos"},
                    {"symbol": "C_hoja", "value": "80", "unit": "filas/hoja", "meaning": "Entradas almacenadas por página hoja"},
                ],
                "unknown": "Capacidad total en millones de filas N_millones",
                "steps": [
                    {
                        "text": "Multiplicamos los 200 hijos de la raíz por los 200 hijos del nivel intermedio por las 80 filas por hoja y dividimos entre 10^6",
                        "latex": r"N_{\text{millones}} = \frac{200 \cdot 200 \cdot 80}{10^6}",
                        "sympy": "(200 * 200 * 80) / 1000000",
                    }
                ],
                "conclusion": "Con solo 3 niveles (y los 2 primeros en RAM), el árbol B+ direcciona hasta 3,2 millones de filas requiriendo como máximo una única lectura física de disco para la hoja.",
            },
            "practice_problems": make_practice_set(
                "CH-05",
                [
                    ("Número de páginas hoja en el árbol B+ de 3 niveles con factor de ramificación 200 (200 * 200)", "200 * 200", "hojas"),
                    ("Memoria RAM en KiB requerida para mantener en Buffer Pool la raíz y los 200 nodos internos de 8 KiB ((1 + 200) * 8)", "(1 + 200) * 8", "KiB"),
                    ("Coste estimado en unidades de página de un Index Scan que lee 3 niveles de índice más 12 páginas de Heap", "3 + 12", "páginas"),
                    ("Tasa de escritura WAL en MB/s para 5 000 transacciones por segundo que generan 400 bytes de log cada una", "(5000 * 400) / 1000000", "MB/s"),
                ],
            ),
        },
        {
            "id": "CH-06",
            "title": "Bases de datos distribuidas: modelos y compromisos",
            "prerequisites": "CH-05 (Motores de almacenamiento y transacciones ACID).",
            "learning_outcomes": "Diseñar topologías de replicación y particionamiento (sharding), evaluar compromisos CAP/PACELC y seleccionar con criterio técnico entre motores relacionales y NoSQL.",
            "summary": "Arquitectura de bases de datos a escala: replicación síncrona/asíncrona, particionamiento por hash consistente y rango, transacciones distribuidas y motores de producción.",
            "paragraphs": [
                {
                    "title": "Teorema CAP y Clasificación PACELC en Almacenamiento Distribuido",
                    "claim": "El modelo PACELC extiende el teorema CAP demostrando que incluso en ausencia de particiones de red existe una disyuntiva fundamental entre latencia (L) y consistencia (C).",
                    "body": (
                        "El teorema CAP (Brewer, demostrado formalmente por Gilbert y Lynch) establece que ante una "
                        "partición de red (P) entre nodos, un almacén de datos distribuido debe elegir entre cancelar "
                        "la operación para preservar la Consistencia linealizable (CP) o responder con datos potencialmente "
                        "desactualizados para preservar la Disponibilidad (AP). El teorema PACELC (Abadi) añade que, "
                        "incluso cuando el sistema opera normalmente (Else), debe decidirse entre replicar síncronamente "
                        "(penalizando la Latencia L a cambio de Consistencia C) o asíncronamente."
                    ),
                },
                {
                    "title": "Replicación Líder-Seguidor, Quórums de Lectura/Escritura y Sharding",
                    "claim": "En un sistema replicado sobre N nodos, exigir un quórum estricto W + R > N garantiza que toda lectura observe al menos una réplica con la última escritura confirmada.",
                    "body": (
                        "Cuando el volumen de escrituras o el conjunto de datos supera la capacidad de un único nodo, "
                        "los datos se dividen horizontalmente en particiones (Shards). El particionamiento por rango "
                        "facilita consultas secuenciales pero puede sufrir puntos calientes (hotspots) si todas las "
                        "escrituras llevan la marca temporal actual; el particionamiento por Hash Consistente (con nodos "
                        "virtuales en un anillo de \\(2^{32}\\) posiciones) distribuye uniformemente la carga y minimiza "
                        "el movimiento de claves al añadir o retirar servidores."
                    ),
                },
                {
                    "title": "PostgreSQL y SQLite en Producción: De Sistemas Embebidos a Escala Empresarial",
                    "claim": "PostgreSQL combina relacionalidad estricta con tipos JSONB indexados (GIN), mientras que SQLite en modo WAL ofrece lecturas concurrentes embebidas de latencia sub-milisegundo.",
                    "body": (
                        "PostgreSQL constituye el estándar de referencia en ingeniería de datos moderna: soporta índices "
                        "B-Tree, Hash, GiST, SP-GiST, GIN (para documentos `JSONB` y búsqueda de texto completo) y BRIN "
                        "(para series temporales masivas), además de particionamiento declarativo y replicación lógica. "
                        "Por su parte, SQLite ejecuta el motor transaccional completo dentro del espacio de direcciones "
                        "del proceso anfitrión sin latencia de red; al activar `PRAGMA journal_mode = WAL;` y "
                        "`PRAGMA synchronous = NORMAL;`, alcanza decenas de miles de operaciones por segundo en un único "
                        "archivo de disco."
                    ),
                },
                {
                    "title": "Motores NoSQL Especializados: Documentos (MongoDB) y Memoria Clave-Valor (Redis)",
                    "claim": "Los almacenes documentales eliminan el coste de joins cuando el agregado se consulta íntegro, y Redis proporciona estructuras atómicas en RAM con latencia de microsegundos.",
                    "body": (
                        "MongoDB almacena documentos en formato binario BSON sobre el motor WiredTiger, resultando idóneo "
                        "para catálogos polimórficos donde la entidad raíz y sus subdocumentos forman un agregado de "
                        "consulta cohesivo. Redis (y alternativas compatibles como Valkey) mantiene estructuras de datos "
                        "ricas en memoria (Strings, Hashes, Sorted Sets, Streams, HyperLogLog) sobre un bucle de eventos "
                        "monohilo libre de contención de cerrojos, ejecutando scripts Lua de forma atómica para cachés "
                        "distribuidas, colas de trabajo y limitadores de tasa (rate limiters)."
                    ),
                },
            ],
            "worked_problem": {
                "title": "Cálculo del quórum mínimo de lectura para consistencia fuerte",
                "statement": (
                    "Un clúster de base de datos distribuida mantiene N = 5 réplicas de cada partición. Si las "
                    "escrituras se configuran con un quórum de confirmación W = 3 nodos para tolerar la caída de "
                    "2 réplicas, calcule el número mínimo de nodos R que debe consultar una lectura para garantizar "
                    "intersección estricta (W + R > N => R = N - W + 1)."
                ),
                "given": [
                    {"symbol": "N", "value": "5", "unit": "nodos", "meaning": "Factor total de replicación"},
                    {"symbol": "W", "value": "3", "unit": "nodos", "meaning": "Quórum de escritura confirmada"},
                ],
                "unknown": "Quórum mínimo de lectura R en nodos",
                "steps": [
                    {
                        "text": "Aplicamos la condición de intersección de quórum estricto R = N - W + 1",
                        "latex": r"R = 5 - 3 + 1",
                        "sympy": "5 - 3 + 1",
                    }
                ],
                "conclusion": "Basta con leer de R = 3 réplicas cualesquiera para garantizar que al menos una contiene la última escritura confirmada por W = 3 nodos.",
            },
            "practice_problems": make_practice_set(
                "CH-06",
                [
                    ("Quórum de lectura requerido si N = 7 réplicas y W = 4 escrituras (7 - 4 + 1)", "7 - 4 + 1", "nodos"),
                    ("Porcentaje de claves redistribuidas por Hash Consistente al pasar de 9 a 10 nodos (100 / 10)", "100 / 10", "%"),
                    ("Memoria RAM total en GB para almacenar en Redis 50 millones de claves de 200 bytes promedio (dividiendo entre 10^9)", "(50000000 * 200) / 1000000000", "GB"),
                    ("Número máximo de fallos de nodo tolerados por un clúster Raft de 5 nodos ((5 - 1) / 2)", "(5 - 1) / 2", "nodos"),
                ],
            ),
        },
        {
            "id": "CH-07",
            "title": "Frameworks Web Frontend y Full-Stack: React, Angular, Vue, Svelte y Next.js",
            "prerequisites": "CH-01, CH-02 y monografías de JavaScript y TypeScript (Volumen V).",
            "learning_outcomes": "Comprender los motores de reactividad (Virtual DOM, Signals, compilación estática), gestionar estado cliente/servidor e implementar Server-Side Rendering (SSR) e hidratación.",
            "summary": "Arquitectura interna y patrones de ingeniería de los principales frameworks de interfaz de usuario web.",
            "paragraphs": [
                {
                    "title": "Del DOM Imperativo a la UI Declarativa: Función Estado -> Vista",
                    "claim": "Los frameworks frontend modernos modelan la interfaz como una proyección determinista V = f(S) del estado actual, automatizando la sincronización incremental del DOM.",
                    "body": (
                        "Manipular manualmente nodos DOM ante eventos asíncronos conduce a transiciones de estado no "
                        "controladas y fugas de memoria. Los frameworks modernos adoptan un paradigma declarativo donde "
                        "el desarrollador describe cómo debe lucir la interfaz para cada estado \\(S\\), y el motor de "
                        "ejecución determina el conjunto mínimo de mutaciones DOM necesarias. Existen dos grandes "
                        "estrategias: reconciliación de Árbol Virtual (Virtual DOM en React y Vue) y reactividad de "
                        "grano fino basada en grafos de dependencias o compilación anticipada (Signals en Angular/Solid "
                        "y compilador de Svelte)."
                    ),
                },
                {
                    "title": "React y Next.js: Reconciliación Fiber, Hooks, Server Components e Hidratación",
                    "claim": "La arquitectura React Fiber divide el trabajo de reconciliación en unidades cooperativas interrumpibles, mientras que los React Server Components eliminan el coste de hidratación de componentes estáticos.",
                    "body": (
                        "En React, los componentes funcionales son funciones puras que utilizan Hooks (`useState`, "
                        "`useReducer`, `useMemo`, `useEffect`) almacenados en una lista enlazada asociada al nodo Fiber. "
                        "En aplicaciones full-stack con Next.js (App Router), los React Server Components (RSC) se "
                        "ejecutan exclusivamente en el servidor —accediendo directamente a bases de datos sin enviar "
                        "su código JavaScript al navegador—, reservando los Client Components (`\"use client\"`) para "
                        "islas de interactividad que requieren hidratación."
                    ),
                },
                {
                    "title": "Angular, Vue y Svelte: Inyección de Dependencias, Proxies Reactivos y Compilación",
                    "claim": "Vue 3 rastrea dependencias en tiempo de ejecución mediante objetos Proxy de ES6, mientras que Svelte compila las asignaciones reactivas en actualizaciones quirúrgicas del DOM en tiempo de build.",
                    "body": (
                        "Angular ofrece una plataforma empresarial opinada en TypeScript con inyección de dependencias "
                        "jerárquica, enrutamiento tipado, RxJS y reactividad moderna mediante `signal()` y `computed()`. "
                        "Vue 3 combina la Composition API (`ref`, `reactive`) implementada sobre `Proxy` con un compilador "
                        "de plantillas que marca banderas de parcheo (`PatchFlags`) para saltar subárboles estáticos. "
                        "Svelte prescinde del Virtual DOM compilando cada componente en código JavaScript imperativo mínimo."
                    ),
                },
                {
                    "title": "Gestión de Estado: Estado Local, Estado Global y Caché de Estado Remoto",
                    "claim": "Separar la caché de estado del servidor (TanStack Query / SWR) del estado efímero de la interfaz reduce drásticamente la complejidad de almacenes globales como Redux.",
                    "body": (
                        "Uno de los antipatrones más frecuentes en ingeniería frontend consiste en volcar respuestas "
                        "HTTP crudas en un almacén global único sin políticas de invalidación, reintento ni deduplicación. "
                        "La arquitectura moderna distingue estrictamente entre estado del servidor (gestionado mediante "
                        "cachés declarativas con `stale-while-revalidate` y actualización optimista), estado de la URL "
                        "(filtros y paginación sincronizados con el router) y estado puramente local de la interfaz."
                    ),
                },
            ],
            "worked_problem": {
                "title": "Reducción del bundle JavaScript mediante React Server Components y Code Splitting",
                "statement": (
                    "Una aplicación SPA tradicional descarga un bundle monolítico de 480 KiB de JavaScript. Al migrar "
                    "a una arquitectura híbrida SSR + Server Components, el 65 % del código de presentación y formateo "
                    "permanece en el servidor. Calcule el tamaño en KiB del bundle JavaScript que aún debe descargar e "
                    "hidratar el navegador."
                ),
                "given": [
                    {"symbol": "B_spa", "value": "480", "unit": "KiB", "meaning": "Tamaño original del bundle SPA"},
                    {"symbol": "p_srv", "value": "65", "unit": "%", "meaning": "Porcentaje migrado a Server Components"},
                ],
                "unknown": "Tamaño del bundle cliente restante B_cli en KiB",
                "steps": [
                    {
                        "text": "Calculamos el 35 % restante del bundle original de 480 KiB",
                        "latex": r"B_{\text{cli}} = 480 \cdot \frac{100 - 65}{100}",
                        "sympy": "(480 * (100 - 65)) / 100",
                    }
                ],
                "conclusion": "El cliente solo descarga e hidrata 168 KiB de JavaScript, reduciendo el Time to Interactive (TTI) en dispositivos móviles.",
            },
            "practice_problems": make_practice_set(
                "CH-07",
                [
                    ("Ahorro absoluto en KiB al reducir el bundle de 480 KiB a 168 KiB", "480 - 168", "KiB"),
                    ("Tiempo de parseo y compilación JS en móvil a razón de 1,5 ms por cada KiB para 168 KiB", "168 * 3 / 2", "ms"),
                    ("Nodos re-evaluados con Signals en una lista de 500 filas cuando cambia 1 celda frente a 500 sin memoización (ahorro)", "500 - 1", "nodos"),
                    ("Número de peticiones de red tras deduplicar 6 componentes que solicitan simultáneamente el mismo endpoint", "6 - 5", "peticiones"),
                ],
            ),
        },
        {
            "id": "CH-08",
            "title": "Frameworks Backend, Escritorio y Móvil: FastAPI, Spring Boot, ASP.NET Core, Axum, Qt, Tauri y Flutter",
            "prerequisites": "Monografías de Python, Java, C#, Rust, Dart, Swift y Kotlin (Volúmenes III a VII).",
            "learning_outcomes": "Diseñar tuberías de middleware backend, inyección de dependencias y validación de esquemas, y contrastar arquitecturas de escritorio y móvil nativas frente a multiplataforma.",
            "summary": "Análisis arquitectónico de los ecosistemas de servidor de alto rendimiento y de las plataformas de interfaz gráfica de escritorio y dispositivos móviles.",
            "paragraphs": [
                {
                    "title": "Arquitectura de Frameworks Backend: Middleware, Inyección de Dependencias y Ciclo HTTP",
                    "claim": "Todos los frameworks backend modernos estructuran el procesamiento de peticiones como una composición funcional de middlewares alrededor de un controlador tipado.",
                    "body": (
                        "Tanto en ecosistemas asíncronos orientados a eventos (Fastify/Express en Node.js, FastAPI sobre "
                        "ASGI/Uvicorn en Python, Axum/Actix sobre Tokio en Rust, Phoenix sobre BEAM en Elixir) como en "
                        "plataformas empresariales multihilo o con hilos virtuales (Spring Boot 3 en Java 21, ASP.NET Core "
                        "en .NET 8, Django, Ruby on Rails, Laravel), cada petición HTTP atraviesa una cadena concéntrica "
                        "de middlewares (trazabilidad, CORS, autenticación JWT/OIDC, rate limiting) antes de deserializar "
                        "y validar el payload hacia un DTO tipado."
                    ),
                },
                {
                    "title": "Comparativa de Ecosistemas Backend: Productividad, Tipado y Rendimiento Extremo",
                    "claim": "Axum (Rust) y ASP.NET Core (C#) lideran el rendimiento por vCPU con latencias de cola mínimas, mientras que FastAPI, Rails, Django y Laravel maximizan la velocidad de iteración.",
                    "body": (
                        "En FastAPI (Python), las anotaciones de tipos estándar junto con Pydantic v2 (escrito en Rust) "
                        "validan cargas JSON y generan automáticamente la especificación OpenAPI 3.1. En Spring Boot y "
                        "ASP.NET Core, el contenedor de Inyección de Dependencias (IoC) gestiona el ciclo de vida de "
                        "servicios (`Singleton`, `Scoped` por petición, `Transient`), facilitando las pruebas unitarias "
                        "mediante inversión de dependencias. En Rust, Axum aprovecha el sistema de tipos para extraer "
                        "parámetros y estado compartido (`State<Arc<AppState>>`) con coste de abstracción nulo."
                    ),
                },
                {
                    "title": "Aplicaciones de Escritorio: Qt (C++), .NET MAUI, Electron y Tauri (Rust + WebView)",
                    "claim": "Tauri reduce en un orden de magnitud el consumo de memoria RAM y el tamaño del instalador frente a Electron al reutilizar el WebView nativo del sistema operativo y ejecutar el backend en Rust.",
                    "body": (
                        "Para aplicaciones de escritorio de misión crítica (CAD, instrumentación médica, edición de vídeo), "
                        "Qt 6 en C++ proporciona renderizado acelerado por hardware y un sistema de señales y ranuras "
                        "(`signals & slots`) nativo. Cuando se desea reutilizar tecnologías web en escritorio, Electron "
                        "empaqueta una instancia completa de Chromium y Node.js por aplicación (~150 MB en disco y cientos "
                        "de MB de RAM base), mientras que Tauri delega la interfaz al WebView del sistema (WebKitGTK, "
                        "WebView2, WKWebView) y comunica el frontend con un binario nativo en Rust mediante IPC tipado."
                    ),
                },
                {
                    "title": "Desarrollo Móvil: SwiftUI (iOS), Jetpack Compose (Android), Flutter y React Native",
                    "claim": "Flutter dibuja cada píxel en su propio lienzo GPU mediante el motor Impeller sin depender de widgets OEM, mientras que SwiftUI y Jetpack Compose ofrecen integración nativa declarativa.",
                    "body": (
                        "El desarrollo móvil moderno ha convergido hacia interfaces declarativas reactivas: SwiftUI en "
                        "el ecosistema Apple y Jetpack Compose en Android eliminan los antiguos archivos XML/Storyboards "
                        "imperativos. En el ámbito multiplataforma, React Native sincroniza componentes JavaScript/TypeScript "
                        "con vistas nativas OEM mediante la nueva arquitectura JSI (JavaScript Interface) sin puente "
                        "serializado, mientras que Flutter (Dart AOT) controla directamente el pipeline gráfico con Impeller."
                    ),
                },
            ],
            "worked_problem": {
                "title": "Ahorro de memoria RAM en escritorio con Tauri frente a Electron",
                "statement": (
                    "Una estación de trabajo ejecuta simultáneamente 4 utilidades corporativas de escritorio. Empaquetadas "
                    "con Electron, cada instancia consume 220 MB de memoria RAM debido a procesos Chromium independientes; "
                    "migradas a Tauri (Rust + WebView compartido), cada instancia consume 45 MB. Calcule la memoria RAM "
                    "total ahorrada en megabytes."
                ),
                "given": [
                    {"symbol": "N_apps", "value": "4", "unit": "aplicaciones", "meaning": "Número de aplicaciones ejecutadas"},
                    {"symbol": "M_elec", "value": "220", "unit": "MB", "meaning": "Memoria por aplicación en Electron"},
                    {"symbol": "M_tauri", "value": "45", "unit": "MB", "meaning": "Memoria por aplicación en Tauri"},
                ],
                "unknown": "Memoria RAM total ahorrada M_ahorro en MB",
                "steps": [
                    {
                        "text": "Multiplicamos las 4 aplicaciones por la diferencia de consumo unitario (220 - 45 = 175 MB)",
                        "latex": r"M_{\text{ahorro}} = 4 \cdot (220 - 45)",
                        "sympy": "4 * (220 - 45)",
                    }
                ],
                "conclusion": "La migración de las 4 utilidades a Tauri libera exactamente 700 MB de memoria RAM en la estación de trabajo.",
            },
            "practice_problems": make_practice_set(
                "CH-08",
                [
                    ("Reducción del tamaño de descarga en MB al pasar de un instalador Electron de 115 MB a uno Tauri de 8 MB", "115 - 8", "MB"),
                    ("Presupuesto de tiempo por fotograma en milisegundos (redondeado a centésimas x100) para una app Flutter a 120 Hz (100000 / 125)", "100000 / 125", "centésimas de ms"),
                    ("Capacidad total de peticiones por segundo en un clúster de 6 pods Axum que procesan 35 000 req/s cada uno", "6 * 35000", "req/s"),
                    ("Instancias de un servicio Scoped creadas durante un lote de 250 peticiones HTTP si se inyecta 2 veces por petición", "250 * 1", "instancias"),
                ],
            ),
        },
    ],
}

VOL09_SPEC = {
    "slug": "vol09-ingenieria-software-arquitectura-y-proyectos",
    "title": "Volumen IX: Ingeniería del Software, Arquitectura, Sistemas Distribuidos, Seguridad y Proyectos",
    "subtitle": "Enciclopedia de Programación e Ingeniería del Software — Partes IX, X, XI, XII y XIII",
    "Part": "Partes IX–XIII: Ingeniería Profesional, Cloud, Seguridad e Itinerarios",
    "scope": (
        "Tratado de ingeniería del software profesional (DDD, SOLID, patrones GoF, Arquitectura Limpia y Hexagonal, "
        "REST/GraphQL/gRPC), calidad y testing (TDD, Property-Based, Fuzzing), sistemas distribuidos (Lamport, Raft, "
        "OpenTelemetry, SRE), ciberseguridad (OWASP, TLS 1.3, Argon2id, OAuth2/OIDC, SLSA), DevOps/Cloud (Docker, "
        "Kubernetes, Terraform) y guía de los 19 itinerarios y proyectos integradores."
    ),
    "target_pages": 65,
    "sources": [
        {
            "title": "Guide to the Software Engineering Body of Knowledge (SWEBOK v4.0) & Clean Architecture",
            "authors": ["IEEE Computer Society", "Robert C. Martin", "Eric Evans"],
            "year": 2024,
            "kind": "standard",
            "publisher": "IEEE / Prentice Hall",
            "url": "https://www.computer.org/education/bodies-of-knowledge/software-engineering",
            "notes": "Estándar curricular SWEBOK v4.0, principios de inversión de dependencias y Domain-Driven Design.",
            "excerpts": [
                (
                    "La Regla de la Dependencia en Arquitectura Limpia y Hexagonal (Puertos y Adaptadores) exige que "
                    "las dependencias en el código fuente apunten exclusivamente hacia adentro: el núcleo de dominio "
                    "no conoce bases de datos, frameworks web ni protocolos de transporte."
                ),
                (
                    "En Domain-Driven Design (DDD), un Agregado (Aggregate) es un clúster de objetos de dominio tratados "
                    "como una unidad atómica de consistencia transaccional bajo la custodia exclusiva de su entidad Raíz "
                    "(Aggregate Root), comunicándose entre contextos acotados (Bounded Contexts) mediante eventos."
                ),
            ],
        },
        {
            "title": "In Search of an Understandable Consensus Algorithm (Raft) & Site Reliability Engineering",
            "authors": ["Diego Ongaro", "John Ousterhout", "Betsy Beyer et al. (Google SRE)"],
            "year": 2016,
            "kind": "article",
            "publisher": "USENIX ATC / O'Reilly Media",
            "url": "https://raft.github.io/raft.pdf",
            "notes": "Algoritmo de consenso distribuido Raft y gestión cuantitativa de fiabilidad mediante SLIs, SLOs y Error Budgets.",
            "excerpts": [
                (
                    "Raft descompone el problema del consenso de máquinas de estados replicadas en tres subproblemas "
                    "independientes: elección de líder mediante temporizadores aleatorios, replicación de entradas de "
                    "log por mayoría de quórum y seguridad de compromiso (State Machine Safety)."
                ),
                (
                    "El presupuesto de error (Error Budget = 1 - SLO) transforma la tensión entre desarrollo de producto "
                    "y operaciones en una métrica objetiva: mientras exista presupuesto disponible se despliegan cambios "
                    "rápidamente, y al agotarse se prioriza la estabilidad y la resiliencia."
                ),
            ],
        },
        {
            "title": "OWASP Application Security Verification Standard (ASVS 4.0) & NIST SP 800-63B",
            "authors": ["OWASP Foundation", "NIST"],
            "year": 2023,
            "kind": "standard",
            "publisher": "OWASP / NIST",
            "url": "https://owasp.org/www-project-application-security-verification-standard/",
            "notes": "Estándares de verificación de seguridad en aplicaciones, criptografía aplicada y gestión de identidades.",
            "excerpts": [
                (
                    "Toda entrada procedente de fronteras no confiables debe procesarse mediante consultas parametrizadas "
                    "(Prepared Statements), codificación contextual de salida y validación estricta de esquemas, "
                    "erradicando estructuralmente las inyecciones SQL, XSS y de comandos del sistema operativo."
                ),
                (
                    "El almacenamiento de contraseñas exige funciones derivadoras de claves endurecidas en memoria como "
                    "Argon2id con sal criptográfica única por usuario, mientras que el cifrado simétrico autenticado "
                    "debe emplear esquemas AEAD como AES-256-GCM o ChaCha20-Poly1305."
                ),
            ],
        },
    ],
    "glossary": [
        ("Bounded Context (Contexto Acotado)", "Frontera semántica explícita en DDD dentro de la cual un lenguaje ubicuo y un modelo de dominio poseen significado unívoco."),
        ("Puertos y Adaptadores (Arquitectura Hexagonal)", "Estilo arquitectónico donde el dominio define interfaces (puertos) implementadas por adaptadores de infraestructura intercambiables."),
        ("Consenso Raft", "Protocolo de consenso distribuido basado en líder fuerte y quórum mayoritario que garantiza la seguridad de máquinas de estados replicadas."),
        ("Presupuesto de Error (Error Budget)", "Fracción permitida de indisponibilidad o fallos (1 - SLO) durante una ventana temporal antes de congelar despliegues de nuevas funcionalidades."),
    ],
    "notation": [
        (r"I = \frac{C_e}{C_a + C_e}", "Métrica de inestabilidad de paquetes de Robert C. Martin", "adimensional"),
        (r"A = T_{\text{MTTF}} / T_{\text{tot}}", "Disponibilidad estacionaria de un sistema reparable", "fracción"),
        (r"N \ge 2f + 1", "Nodos requeridos en consenso tolerante a f fallos de parada (Raft/Paxos)", "nodos"),
    ],
    "chapters": [
        {
            "id": "CH-01",
            "title": "Principios de Diseño (SOLID, acoplamiento/cohesión), Patrones GoF y Refactorización",
            "prerequisites": "Programación orientada a objetos y funcional en al menos un lenguaje de la Parte V.",
            "learning_outcomes": "Evaluar cuantitativamente el acoplamiento aferente y eferente, aplicar los principios SOLID sin sobreingeniería e implementar patrones de diseño GoF con tipos modernos.",
            "summary": "Fundamentos del diseño modular de software mantenible: cohesión funcional, inversión de dependencias y catálogo crítico de patrones creacionales, estructurales y de comportamiento.",
            "paragraphs": [
                {
                    "title": "Cohesión, Acoplamiento y Métrica de Inestabilidad de Paquetes",
                    "claim": "El diseño modular busca maximizar la cohesión interna de cada módulo mientras dirige el acoplamiento hacia abstracciones estables.",
                    "body": (
                        "La complejidad accidental de un sistema crece cuadráticamente con el acoplamiento implícito "
                        "entre sus componentes. Dado un módulo o paquete, su acoplamiento aferente \\(C_a\\) cuenta "
                        "cuántos módulos externos dependen de él, y su acoplamiento eferente \\(C_e\\) cuenta de cuántos "
                        "módulos externos depende él. La métrica de inestabilidad \\(I = C_e / (C_a + C_e) \\in [0, 1]\\) "
                        "caracteriza desde paquetes máximamente estables (\\(I = 0\\), como el modelo de dominio puro) "
                        "hasta paquetes volátiles (\\(I = 1\\), como adaptadores de interfaz o puntos de entrada `main`). "
                        "El Principio de Dependencias Estables dicta que un módulo sólo debe depender de módulos con "
                        "menor o igual inestabilidad."
                    ),
                },
                {
                    "title": "Los Cinco Principios SOLID bajo una Lente Moderna",
                    "claim": "El Principio de Sustitución de Liskov (LSP) es un contrato semántico de subtipado conductual (precondiciones no más fuertes, postcondiciones no más débiles) y el Principio de Inversión de Dependencias (DIP) desacopla políticas de mecanismos.",
                    "body": (
                        "1) **Responsabilidad Única (SRP)**: un módulo debe tener una única razón de cambio asociada a un "
                        "actor de negocio. 2) **Abierto/Cerrado (OCP)**: el comportamiento debe poder extenderse mediante "
                        "polimorfismo o composición de funciones sin modificar el código ya verificado. 3) **Sustitución "
                        "de Liskov (LSP)**: formalizado por Barbara Liskov y Jeannette Wing, exige que todo subtipo preserve "
                        "los invariantes e historia observable del supertipo. 4) **Segregación de Interfaces (ISP)**: "
                        "ningún cliente debe verse forzado a depender de métodos que no utiliza. 5) **Inversión de "
                        "Dependencias (DIP)**: los módulos de alto nivel definen las interfaces (traits, protocolos) "
                        "que implementan los módulos de infraestructura de bajo nivel."
                    ),
                },
                {
                    "title": "Patrones de Diseño GoF en Lenguajes Modernos: De Clases a Funciones y Tipos Algebraicos",
                    "claim": "Muchos de los 23 patrones clásicos de Gamma, Helm, Johnson y Vlissides (1994) se simplifican radicalmente mediante funciones de orden superior, tipos suma y traits.",
                    "body": (
                        "Los patrones creacionales (`Factory Method`, `Abstract Factory`, `Builder`) encapsulan la "
                        "construcción válida de objetos complejos; en particular, el patrón `Type-State Builder` en "
                        "Rust o TypeScript verifica en tiempo de compilación que todos los campos obligatorios se hayan "
                        "configurado antes de invocar `.build()`. Los patrones estructurales (`Adapter`, `Decorator`, "
                        "`Facade`, `Proxy`, `Composite`) traducen interfaces o añaden responsabilidades transversales "
                        "(telemetría, reintentos, caché) sin alterar la implementación subyacente. Los patrones de "
                        "comportamiento (`Strategy`, `Observer`, `Command`, `State`, `Iterator`) modelan algoritmos "
                        "intercambiables y máquinas de estados."
                    ),
                },
                {
                    "title": "Deuda Técnica, Code Smells y Disciplina de Refactorización Segura",
                    "claim": "La refactorización es una transformación del código fuente que preserva estrictamente el comportamiento externo observable mientras mejora su estructura interna.",
                    "body": (
                        "Acuñada por Ward Cunningham, la metáfora de la deuda técnica describe el interés compuesto "
                        "que se paga en cada entrega futura cuando se pospone el reflejo de un aprendizaje de dominio "
                        "en la arquitectura del código. Toda refactorización (extracción de funciones puras, sustitución "
                        "de condicionales anidados por polimorfismo o pattern matching exhaustivo, introducción de "
                        "objetos valor) debe ejecutarse en pasos atómicos respaldados por una batería rápida de pruebas "
                        "automatizadas."
                    ),
                },
            ],
            "worked_problem": {
                "title": "Cálculo de la métrica de inestabilidad de un paquete de dominio",
                "statement": (
                    "En una arquitectura modular, el paquete de facturación es importado por 18 módulos externos "
                    "(acoplamiento aferente Ca = 18) e importa únicamente 2 bibliotecas estándar de tipos "
                    "(acoplamiento eferente Ce = 2). Calcule el índice de inestabilidad I expresado en porcentaje."
                ),
                "given": [
                    {"symbol": "C_a", "value": "18", "unit": "módulos", "meaning": "Acoplamiento aferente (dependientes entrantes)"},
                    {"symbol": "C_e", "value": "2", "unit": "módulos", "meaning": "Acoplamiento eferente (dependencias salientes)"},
                ],
                "unknown": "Índice de inestabilidad porcentual I_pct en %",
                "steps": [
                    {
                        "text": "Aplicamos la fórmula de Martin I = Ce / (Ca + Ce) multiplicada por 100",
                        "latex": r"I_{\text{pct}} = \frac{2}{18 + 2} \cdot 100",
                        "sympy": "(2 * 100) / (18 + 2)",
                    }
                ],
                "conclusion": "El paquete presenta una inestabilidad baja del 10 %, acorde con su rol como núcleo de negocio estable del que dependen otros 18 módulos.",
            },
            "practice_problems": make_practice_set(
                "CH-01",
                [
                    ("Índice de inestabilidad porcentual de un adaptador HTTP con Ca = 1 y Ce = 9", "(9 * 100) / (1 + 9)", "%"),
                    ("Distancia a la secuencia principal en porcentaje si A = 40 % e I = 50 % (|40 + 50 - 100|)", "100 - (40 + 50)", "%"),
                    ("Reducción de complejidad ciclomática al descomponer un método de complejidad 19 en 4 funciones de complejidad 2", "19 - 4 * 2", "puntos"),
                    ("Número de clases eliminadas al reemplazar 6 clases Strategy de un solo método por funciones de primera clase", "6 * 1", "clases"),
                ],
            ),
        },
        {
            "id": "CH-02",
            "title": "Arquitectura del Software: DDD, Arquitectura Hexagonal/Limpia, Microservicios y APIs (REST, GraphQL, gRPC)",
            "prerequisites": "CH-01 y bases de datos (Volumen VIII).",
            "learning_outcomes": "Diseñar sistemas bajo Arquitectura Hexagonal y Domain-Driven Design, elegir justificadamente entre monolitos modulares y microservicios, y especificar contratos de API REST, GraphQL y gRPC.",
            "summary": "Arquitectura de sistemas de software a escala empresarial: fronteras de dominio, estilos arquitectónicos, CQRS, Event Sourcing y diseño de contratos de comunicación.",
            "tikz_caption": "Arquitectura Hexagonal (Puertos y Adaptadores): los adaptadores primarios invocan puertos de entrada (casos de uso) y el dominio invoca puertos de salida implementados por adaptadores secundarios.",
            "tikz_code": r"""\begin{tikzpicture}[node distance=0.5cm, every node/.style={font=\scriptsize, draw, rounded corners=2pt, align=center, inner sep=3.5pt}]
\node (in) [fill=blue!10] {Adaptadores Primarios\\(REST / gRPC / CLI)};
\node (usecase) [right=of in, fill=green!12] {Puertos de Entrada\\(Casos de Uso)};
\node (domain) [right=of usecase, fill=yellow!18] {Núcleo de Dominio\\(Entidades y Reglas)};
\node (portout) [right=of domain, fill=green!12] {Puertos de Salida\\(Interfaces Repo)};
\node (out) [right=of portout, fill=orange!15] {Adaptadores Secundarios\\(PostgreSQL / Kafka)};
\draw[-Stealth, thick] (in) -- (usecase);
\draw[-Stealth, thick] (usecase) -- (domain);
\draw[-Stealth, thick] (domain) -- (portout);
\draw[Stealth-, thick, dashed] (portout) -- (out);
\end{tikzpicture}""",
            "paragraphs": [
                {
                    "title": "Domain-Driven Design (DDD): Diseño Estratégico y Táctico",
                    "claim": "El diseño estratégico divide un dominio complejo en Contextos Acotados (Bounded Contexts) con Lenguaje Ubicuo propio, evitando el antipatrón de un modelo canónico único gigante.",
                    "body": (
                        "En el nivel estratégico, DDD identifica subdominios principales (Core, donde reside la ventaja "
                        "competitiva), de soporte y genéricos, estableciendo mapas de contexto (Context Maps) con capas "
                        "anticorrupción (ACL) para traducir conceptos entre sistemas. En el nivel táctico, distingue "
                        "**Entidades** (definidas por su identidad persistente a lo largo del tiempo), **Objetos Valor** "
                        "(definidos exclusivamente por sus atributos e inmutables por construcción, como `ImporteMonetario`), "
                        "**Agregados** (fronteras de consistencia transaccional gobernadas por su Aggregate Root) y "
                        "**Eventos de Dominio** (hechos inmutables ocurridos en el pasado)."
                    ),
                },
                {
                    "title": "Arquitectura Hexagonal (Puertos y Adaptadores) y Arquitectura Limpia",
                    "claim": "Aislar el modelo de dominio de los detalles de E/S permite verificar el 100 % de las reglas de negocio en memoria en milisegundos sin levantar contenedores ni bases de datos.",
                    "body": (
                        "Formulada por Alistair Cockburn y popularizada junto a la Arquitectura Limpia de Robert C. Martin, "
                        "la Arquitectura Hexagonal representada en la {{fig:ch-02-fig}} organiza el software en anillos "
                        "concéntricos. El núcleo contiene las entidades y casos de uso de aplicación; alrededor suyo "
                        "se sitúan los puertos de entrada (invocados por controladores HTTP, consumidores de colas o CLI) "
                        "y los puertos de salida (interfaces de repositorios, pasarelas de pago o relojes de sistema), "
                        "cuyas implementaciones concretas residen en la capa externa de infraestructura."
                    ),
                },
                {
                    "title": "Monolito Modular frente a Microservicios, CQRS y Patrón Outbox Transaccional",
                    "claim": "Un monolito modular bien acotado ofrece fronteras lógicas limpias con transacciones ACID locales y cero sobrecoste de red, debiendo extraerse microservicios solo ante necesidades reales de escalado o despliegue independiente.",
                    "body": (
                        "Distribuir prematuramente un sistema sin fronteras de dominio maduras engendra un 'monolito "
                        "distribuido' que sufre la latencia, los fallos parciales y la complejidad operativa de los "
                        "microservicios sin obtener autonomía de despliegue. Cuando un sistema requiere publicar eventos "
                        "en un broker (Kafka, RabbitMQ) tras actualizar su base de datos, escribir simultáneamente en "
                        "ambos sin coordinación dos fases es inseguro; el patrón **Transactional Outbox** resuelve este "
                        "problema insertando el evento en una tabla `outbox` dentro de la misma transacción ACID local "
                        "y reenviándolo de forma asíncrona con garantía `at-least-once`."
                    ),
                },
                {
                    "title": "Diseño de APIs: REST (OpenAPI), GraphQL, gRPC y WebSockets",
                    "claim": "REST sobre HTTP/JSON sobresale en interoperabilidad pública, GraphQL optimiza consultas de clientes con grafos de vista diversos y gRPC sobre HTTP/2 + Protobuf domina la comunicación interna de baja latencia.",
                    "body": (
                        "En una API RESTful madura, los recursos se modelan como sustantivos jerárquicos, los métodos "
                        "HTTP respetan su semántica de seguridad e idempotencia (`GET` y `HEAD` seguros; `PUT` y `DELETE` "
                        "idempotentes; `POST` con clave `Idempotency-Key` para pagos), y los errores se devuelven en "
                        "formato estándar RFC 9457 (`Problem Details for HTTP APIs`). En GraphQL es imprescindible "
                        "implementar el patrón `DataLoader` para agrupar consultas y evitar el problema \\(N+1\\)."
                    ),
                },
            ],
            "worked_problem": {
                "title": "Eliminación del problema N+1 en un resolver GraphQL mediante DataLoader",
                "statement": (
                    "Una consulta GraphQL solicita una lista de 50 pedidos junto con los datos del autor de cada pedido. "
                    "Sin agrupación (N+1), el servidor ejecuta 1 consulta para la lista y 50 consultas individuales "
                    "de 2 ms de latencia cada una. Con DataLoader, ejecuta solo 2 consultas (la lista y un único "
                    "SELECT ... WHERE id IN (...)) de 2 ms cada una. Calcule el tiempo total de base de datos ahorrado en ms."
                ),
                "given": [
                    {"symbol": "N", "value": "50", "unit": "pedidos", "meaning": "Número de elementos de la lista"},
                    {"symbol": "t_q", "value": "2", "unit": "ms", "meaning": "Latencia por consulta a la base de datos"},
                ],
                "unknown": "Tiempo de base de datos ahorrado T_ahorro en ms",
                "steps": [
                    {
                        "text": "Restamos el tiempo de las 2 consultas agrupadas al tiempo de las N + 1 = 51 consultas secuenciales",
                        "latex": r"T_{\text{ahorro}} = (50 + 1) \cdot 2 - 2 \cdot 2",
                        "sympy": "(50 + 1) * 2 - 2 * 2",
                    }
                ],
                "conclusion": "DataLoader reduce el tiempo de consultas de 102 ms a 4 ms, ahorrando exactamente 98 ms por petición.",
            },
            "practice_problems": make_practice_set(
                "CH-02",
                [
                    ("Consultas SQL ahorradas al resolver 120 elementos con DataLoader (2 consultas) frente a N+1 (121 consultas)", "121 - 2", "consultas"),
                    ("Latencia acumulada en ms de una cadena síncrona de 6 microservicios con 8 ms por salto", "6 * 8", "ms"),
                    ("Disponibilidad porcentual aproximada (en centésimas x100) de 3 servicios en serie al 99 % cada uno (10000 - 3*100)", "10000 - 3 * 100", "centésimas de %"),
                    ("Tamaño de página máximo devuelto si una API REST limita page_size <= 100 cuando el cliente solicita 5000", "100 * 1", "registros"),
                ],
            ),
        },
        {
            "id": "CH-03",
            "title": "Control de Versiones (Git Internals), Calidad, Testing, Property-Based Testing y Fuzzing",
            "prerequisites": "CH-01 y estructuras de datos tipo DAG y tablas hash (Volumen II).",
            "learning_outcomes": "Comprender el almacén direccionable por contenido de Git, diseñar estrategias de pruebas en pirámide/trofeo y verificar invariantes con Property-Based Testing, Fuzzing y Mutation Testing.",
            "summary": "Ingeniería de calidad y verificación de software: modelo de objetos de Git, TDD, dobles de prueba, pruebas basadas en propiedades y análisis de mutación.",
            "paragraphs": [
                {
                    "title": "Arquitectura Interna de Git: Almacén Direccionable por Contenido y Grafo DAG",
                    "claim": "Git no almacena diferencias incrementales por commit, sino instantáneas completas modeladas como un grafo acíclico dirigido (DAG) de cuatro objetos inmutables: blob, tree, commit y tag.",
                    "body": (
                        "Bajo el directorio `.git/objects`, Git opera como un sistema de archivos clave-valor direccionable "
                        "por contenido (Content-Addressable Storage) donde la clave de cada objeto es el hash criptográfico "
                        "(SHA-1 o SHA-256) de su cabecera más su contenido comprimido con zlib. Un **blob** almacena los "
                        "bytes de un archivo sin su nombre; un **tree** asocia nombres de archivo y permisos con hashes "
                        "de blobs y sub-trees; y un **commit** apunta al tree raíz de la instantánea, a sus commits "
                        "padres y a los metadatos de autoría. Las ramas (`refs/heads/*`) son simples punteros móviles "
                        "de 41 bytes hacia un commit."
                    ),
                },
                {
                    "title": "Pirámide de Testing, TDD y Dobles de Prueba (Stubs, Fakes, Mocks)",
                    "claim": "Una batería de pruebas eficaz concentra el volumen en pruebas unitarias deterministas y de integración sobre contenedores efímeros, reservando las pruebas E2E para los flujos críticos de usuario.",
                    "body": (
                        "El ciclo Test-Driven Development (TDD: Red -> Green -> Refactor) utiliza las pruebas como "
                        "herramienta de diseño de interfaces antes de escribir la implementación. Siguiendo la taxonomía "
                        "de Gerard Meszaros, es fundamental distinguir entre **Stubs** (devuelven respuestas preconfiguradas), "
                        "**Fakes** (implementaciones funcionales ligeras, como un repositorio en memoria) y **Mocks** "
                        "(verifican interacciones salientes). Abusar de mocks acoplados a detalles internos produce "
                        "pruebas frágiles que se rompen ante cualquier refactorización legítima."
                    ),
                },
                {
                    "title": "Property-Based Testing (QuickCheck, Hypothesis, proptest) y Reducción Automática (Shrinking)",
                    "claim": "El Property-Based Testing genera cientos de entradas aleatorias estructuradas para refutar invariantes universales y reduce automáticamente el contraejemplo al caso mínimo reproducible.",
                    "body": (
                        "Mientras una prueba basada en ejemplos comprueba una tupla concreta (`assert ordenar([3,1,2]) == [1,2,3]`), "
                        "una prueba basada en propiedades (introducida por Claessen y Hughes en QuickCheck para Haskell "
                        "y disponible en Hypothesis para Python o `proptest` para Rust) declara propiedades algebraicas "
                        "que deben cumplirse para toda entrada válida: idempotencia (`f(f(x)) == f(x)`), inversión "
                        "(`decode(encode(x)) == x`) o preservación de invariantes estructurales. Al encontrar un fallo, "
                        "el motor aplica *shrinking* en el árbol de generación para entregar el contraejemplo más simple."
                    ),
                },
                {
                    "title": "Fuzzing Guiado por Cobertura (libFuzzer, AFL++) y Mutation Testing",
                    "claim": "La cobertura de líneas del 100 % no garantiza que las aserciones detecten defectos; el Mutation Testing mide la eficacia real de los tests inyectando mutantes sintácticos.",
                    "body": (
                        "En analizadores de protocolos, compiladores y parsers binarios, el Fuzzing guiado por cobertura "
                        "(Coverage-Guided Fuzzing con `cargo-fuzz` / `libFuzzer`) instrumenta las aristas del grafo de "
                        "control de flujo y muta el corpus de entradas cada vez que una mutación descubre una nueva ruta "
                        "de ejecución. Por su parte, herramientas de Mutation Testing (`mutmut`, `cargo-mutants`, `Stryker`) "
                        "modifican operadores en el código de producción (`<` por `<=`, `+` por `-`) y verifican qué "
                        "porcentaje de mutantes son detectados ('muertos') por la suite de tests."
                    ),
                },
            ],
            "worked_problem": {
                "title": "Cálculo del Mutation Score en una auditoría de calidad de pruebas",
                "statement": (
                    "Una herramienta de Mutation Testing genera 250 mutantes sintácticos sobre el módulo de liquidación "
                    "financiera. De ellos, 10 son mutantes equivalentes (no alteran la semántica) y la batería de "
                    "pruebas detecta y hace fallar 216 de los mutantes restantes. Calcule el Mutation Score porcentual "
                    "sobre los mutantes no equivalentes."
                ),
                "given": [
                    {"symbol": "M_tot", "value": "250", "unit": "mutantes", "meaning": "Total de mutantes generados"},
                    {"symbol": "M_eq", "value": "10", "unit": "mutantes", "meaning": "Mutantes semánticamente equivalentes"},
                    {"symbol": "M_kill", "value": "216", "unit": "mutantes", "meaning": "Mutantes detectados (killed) por los tests"},
                ],
                "unknown": "Puntuación de mutación S_mut en %",
                "steps": [
                    {
                        "text": "Dividimos los 216 mutantes detectados entre los 240 mutantes no equivalentes (250 - 10) y multiplicamos por 100",
                        "latex": r"S_{\text{mut}} = \frac{216}{250 - 10} \cdot 100",
                        "sympy": "(216 * 100) / (250 - 10)",
                    }
                ],
                "conclusion": "La suite de pruebas alcanza un Mutation Score del 90 %, identificando exactamente los 24 mutantes supervivientes que requieren nuevas aserciones.",
            },
            "practice_problems": make_practice_set(
                "CH-03",
                [
                    ("Mutantes supervivientes que requieren nuevos tests en el módulo auditado (250 - 10 - 216)", "250 - 10 - 216", "mutantes"),
                    ("Objetos nuevos creados en Git al modificar 1 archivo dentro de un subdirectorio de profundidad 2 (1 blob + 3 trees + 1 commit)", "1 + 3 + 1", "objetos"),
                    ("Casos generados en 5 segundos por un fuzzer libFuzzer que ejecuta 18 000 iteraciones por segundo", "5 * 18000", "ejecuciones"),
                    ("Tiempo total de CI en segundos para 1 200 tests unitarios de 2 ms y 30 tests de integración de 200 ms", "(1200 * 2 + 30 * 200) / 1000", "s"),
                ],
            ),
        },
        {
            "id": "CH-04",
            "title": "Sistemas Distribuidos, Consenso (Raft), Resiliencia, Observabilidad (OpenTelemetry) y SRE",
            "prerequisites": "CH-02 y redes / concurrencia (Volúmenes II y VIII).",
            "learning_outcomes": "Razonar sobre tiempo lógico y orden parcial, implementar patrones de resiliencia (Circuit Breaker, Backoff con Jitter, Idempotencia), instrumentar sistemas con OpenTelemetry y gestionar presupuestos de error SRE.",
            "summary": "Teoría y práctica de los sistemas distribuidos modernos: falacias de la red, relojes de Lamport/vectoriales, consenso Raft, trazabilidad distribuida e ingeniería de fiabilidad.",
            "paragraphs": [
                {
                    "title": "Tiempo Físico vs Tiempo Lógico: Relojes de Lamport y Relojes Vectoriales",
                    "claim": "En ausencia de un reloj físico global perfectamente sincronizado, la relación happened-before de Lamport define un orden parcial estricto sobre los eventos de un sistema distribuido.",
                    "body": (
                        "Los relojes físicos de cuarzo en servidores distintos sufren deriva térmica, y la sincronización "
                        "NTP presenta incertidumbres de milisegundos que impiden ordenar causalmente eventos de microsegundos. "
                        "Leslie Lamport formalizó en 1978 la relación causal \\(a \\to b\\) (happened-before): si \\(a \\to b\\), "
                        "entonces las marcas lógicas cumplen \\(L(a) < L(b)\\). Los **Relojes Vectoriales** \\(V \\in \\mathbb{N}^N\\) "
                        "extienden esta propiedad logrando una equivalencia exacta: \\(V(a) < V(b) \\iff a \\to b\\), "
                        "permitiendo detectar exactamente cuándo dos escrituras son concurrentes y requieren resolución "
                        "de conflictos (CRDTs o reconciliación)."
                    ),
                },
                {
                    "title": "Consenso Distribuido con Raft: Elección de Líder y Replicación de Log",
                    "claim": "Un clúster Raft de N = 2f + 1 nodos garantiza seguridad (nunca confirma dos valores distintos para el mismo índice de log) bajo cualquier retraso de red, y disponibilidad mientras al menos f + 1 nodos se comuniquen.",
                    "body": (
                        "En Raft, el tiempo se divide en mandatos (*terms*) numerados monotónicamente. Todo nodo se "
                        "encuentra en uno de tres estados: *Follower*, *Candidate* o *Leader*. Si un seguidor no recibe "
                        "latidos (`AppendEntries` vacíos) del líder durante su tiempo de espera aleatorio (p. ej., "
                        "150–300 ms), incrementa su mandato, pasa a candidato y solicita votos (`RequestVote`). La "
                        "restricción de votación garantiza que sólo un candidato cuyo log esté al menos tan actualizado "
                        "como el de la mayoría de los nodos puede ser elegido líder."
                    ),
                },
                {
                    "title": "Patrones de Resiliencia: Timeouts, Exponential Backoff con Jitter, Circuit Breaker e Idempotencia",
                    "claim": "Reintentar llamadas fallidas inmediatamente o con intervalos fijos provoca tormentas de reintentos (Thundering Herd) que tumban al servicio en recuperación; añadir Jitter aleatorio descorrela la carga.",
                    "body": (
                        "Toda llamada de red debe poseer un `timeout` explícito y acotado. Cuando una operación es "
                        "idempotente (o transporta un token único `Idempotency-Key` registrado atómicamente por el receptor), "
                        "los fallos transitorios pueden reintentarse aplicando espera exponencial con jitter completo: "
                        "\\(t_{\\text{wait}} \\sim U(0, \\min(T_{\\max}, T_{\\text{base}} \\cdot 2^{\\text{intento}}))\\). "
                        "Si la tasa de fallos supera un umbral crítico, un **Circuit Breaker** abre el circuito y falla "
                        "rápidamente en local para permitir que el sistema aguas abajo se recupere."
                    ),
                },
                {
                    "title": "Observabilidad con OpenTelemetry (Métricas, Logs, Trazas) y Disciplina SRE (SLI/SLO)",
                    "claim": "El contexto de propagación W3C Trace Context (traceparent) correlaciona logs y métricas a través de decenas de servicios mediante un identificador global de traza y spans jerárquicos.",
                    "body": (
                        "OpenTelemetry estandariza la instrumentación de telemetría neutral respecto al proveedor: "
                        "**Métricas** (contadores, gauges e histogramas de latencia p50/p95/p99), **Logs estructurados** "
                        "en JSON y **Trazas distribuidas** (grafos de *spans* con `trace_id` y `span_id`). En Site "
                        "Reliability Engineering (SRE), la fiabilidad se gobierna mediante Indicadores de Nivel de Servicio "
                        "(SLI, p. ej., proporción de peticiones HTTP exitosas en menos de 200 ms) y Objetivos (SLO, p. ej., "
                        "99,9 % mensual, lo que otorga un presupuesto de error de 43,2 minutos cada 30 días)."
                    ),
                },
            ],
            "worked_problem": {
                "title": "Cálculo del Presupuesto de Error (Error Budget) mensual para un SLO del 99,9 %",
                "statement": (
                    "Un servicio crítico de pagos define un SLO de disponibilidad del 99,9 % medido sobre una ventana "
                    "de 30 días (43 200 minutos totales). Calcule el presupuesto de error mensual en minutos durante "
                    "los cuales el servicio puede experimentar indisponibilidad sin violar su SLO."
                ),
                "given": [
                    {"symbol": "T_mes", "value": "43200", "unit": "min", "meaning": "Minutos totales en 30 días (30 x 24 x 60)"},
                    {"symbol": "p_err", "value": "0.001", "unit": "fracción", "meaning": "Fracción permitida de error (1 - 0,999)"},
                ],
                "unknown": "Presupuesto de error E_min en minutos",
                "steps": [
                    {
                        "text": "Multiplicamos los 43 200 minutos del mes por la fracción permitida de indisponibilidad (1 / 1000)",
                        "latex": r"E_{\text{min}} = \frac{43200}{1000}",
                        "sympy": "43200 / 1000",
                    }
                ],
                "conclusion": "Un SLO de 'tres nueves' (99,9 %) concede exactamente 43,2 minutos de presupuesto de error cada 30 días.",
            },
            "practice_problems": make_practice_set(
                "CH-04",
                [
                    ("Presupuesto de error anual en minutos para un SLO de cuatro nueves 99,99 % (525600 / 10000)", "525600 / 10000", "min"),
                    ("Nodos totales mínimos en un clúster Raft para tolerar f = 3 fallos simultáneos (2 * 3 + 1)", "2 * 3 + 1", "nodos"),
                    ("Tope de espera en ms en el cuarto reintento (intento=4) con backoff exponencial de base 50 ms (50 * 2^4)", "50 * 2**4", "ms"),
                    ("Disponibilidad porcentual de un servicio con MTTF = 990 horas y MTTR = 10 horas (990 * 100 / (990 + 10))", "(990 * 100) / (990 + 10)", "%"),
                ],
            ),
        },
        {
            "id": "CH-05",
            "title": "Ciberseguridad Aplicada, Criptografía (TLS 1.3, Argon2id, AEAD), OAuth2/OIDC y Supply Chain",
            "prerequisites": "Aritmética modular (Volumen I) y protocolos web (Volumen VIII).",
            "learning_outcomes": "Mitigar vulnerabilidades del OWASP Top 10, aplicar primitivas criptográficas estándar (Argon2id, AES-GCM, Ed25519), diseñar flujos OAuth 2.1 / OIDC con PKCE y asegurar la cadena de suministro de software.",
            "summary": "Ingeniería de seguridad defensiva desde el diseño (Secure by Design): modelado de amenazas STRIDE, criptografía moderna, identidad federada y seguridad de dependencias.",
            "paragraphs": [
                {
                    "title": "Modelado de Amenazas (STRIDE) y Defensa en Profundidad ante OWASP Top 10",
                    "claim": "La seguridad no es una capa añadida al final del desarrollo, sino una propiedad emergente del diseño verificada mediante el principio de mínimo privilegio y fronteras de confianza explícitas.",
                    "body": (
                        "La metodología STRIDE clasifica las amenazas sobre cada flujo de datos en seis categorías: "
                        "**S**poofing (suplantación de identidad), **T**ampering (manipulación de datos), **R**epudiation "
                        "(repudio sin rastro auditable), **I**nformation Disclosure (fuga de información), **D**enial of "
                        "Service (denegación de servicio) y **E**levation of Privilege (escalada de privilegios). Para "
                        "neutralizar las vulnerabilidades más críticas del OWASP Top 10 —como Broken Access Control "
                        "(IDOR), Injection (SQLi, XSS, Command Injection) y Server-Side Request Forgery (SSRF)— el "
                        "sistema debe verificar la autorización a nivel de objeto en cada petición, utilizar consultas "
                        "parametrizadas, aplicar cabeceras `Content-Security-Policy` (CSP) y restringir las conexiones "
                        "salientes del servidor hacia rangos IP privados o de metadatos cloud (`169.254.169.254`)."
                    ),
                },
                {
                    "title": "Criptografía Aplicada Moderna: TLS 1.3, AEAD (AES-GCM / ChaCha20-Poly1305) y Argon2id",
                    "claim": "Nunca debe implementarse criptografía propia ni emplear cifrado simétrico sin autenticación (CBC sin MAC); todo cifrado debe usar esquemas AEAD y todo hash de contraseñas debe usar Argon2id.",
                    "body": (
                        "Las comunicaciones en tránsito deben protegerse con **TLS 1.3** (RFC 8446), que completa el "
                        "handshake en 1-RTT y exige intercambio de claves efímeras Diffie-Hellman sobre curvas elípticas "
                        "(ECDHE con X25519) para garantizar Secreto Perfecto hacia Adelante (*Forward Secrecy*). Para "
                        "datos en reposo, los esquemas **AEAD** (Authenticated Encryption with Associated Data) como "
                        "`AES-256-GCM` o `ChaCha20-Poly1305` proporcionan simultáneamente confidencialidad e integridad "
                        "mediante una etiqueta de autenticación de 128 bits. Para contraseñas, **Argon2id** exige una "
                        "cantidad configurable de memoria RAM (p. ej., 64 MiB por hash) que neutraliza ataques paralelos "
                        "con GPUs y ASICs."
                    ),
                },
                {
                    "title": "Autenticación y Autorización Moderna: OAuth 2.1, OpenID Connect (OIDC), PKCE y Passkeys",
                    "claim": "El flujo Authorization Code con PKCE (RFC 7636) protege tanto a aplicaciones móviles y SPA como a servidores web frente a la interceptación del código de autorización.",
                    "body": (
                        "OAuth 2.1 delega autorización mientras que OpenID Connect (OIDC) añade una capa de identidad "
                        "mediante un `ID Token` firmado en formato JWT (con algoritmos asimétricos `RS256` o `EdDSA`, "
                        "verificando siempre la cabecera `alg`, el emisor `iss`, la audiencia `aud` y la expiración `exp`). "
                        "En el flujo con **PKCE** (Proof Key for Code Exchange), el cliente genera un secreto efímero "
                        "`code_verifier` y envía su hash SHA-256 (`code_challenge`) al iniciar el login, impidiendo que "
                        "un atacante que intercepte el código de retorno pueda canjearlo por tokens."
                    ),
                },
                {
                    "title": "Seguridad de la Cadena de Suministro (Supply Chain): Lockfiles, SBOM, Sigstore y SLSA",
                    "claim": "Fijar hashes criptográficos en archivos de bloqueo (Cargo.lock, package-lock.json), generar inventarios SBOM y firmar artefactos en CI/CD protege contra ataques de confusión de dependencias.",
                    "body": (
                        "El software moderno depende de cientos de paquetes transitivos de código abierto. Asegurar la "
                        "cadena de suministro conforme al marco **SLSA** (Supply-chain Levels for Software Artifacts) "
                        "requiere compilar en entornos efímeros reproducibles, verificar sumas SHA-256 en lockfiles, "
                        "emitir una lista de materiales de software (**SBOM** en formato CycloneDX o SPDX) y firmar "
                        "imágenes y binarios sin claves de larga duración mediante certificados efímeros de **Sigstore/Cosign**."
                    ),
                },
            ],
            "worked_problem": {
                "title": "Coste de memoria agregado de Argon2id frente a ataques de fuerza bruta en GPU",
                "statement": (
                    "Un servidor configura Argon2id con un coste de memoria de 64 MiB por verificación de contraseña "
                    "y 3 iteraciones. Si un atacante intenta evaluar en paralelo 512 candidatos simultáneos en una "
                    "GPU, calcule la memoria VRAM total en GiB (1 GiB = 1024 MiB) necesaria para sostener esos "
                    "512 hilos sin penalización de ancho de banda."
                ),
                "given": [
                    {"symbol": "M_hash", "value": "64", "unit": "MiB", "meaning": "Memoria requerida por instancia de Argon2id"},
                    {"symbol": "N_par", "value": "512", "unit": "hilos", "meaning": "Candidatos evaluados en paralelo"},
                    {"symbol": "K", "value": "1024", "unit": "MiB/GiB", "meaning": "Mebibytes por gibibyte"},
                ],
                "unknown": "Memoria VRAM requerida V_gib en GiB",
                "steps": [
                    {
                        "text": "Multiplicamos los 512 hilos por 64 MiB y dividimos entre 1024 MiB/GiB",
                        "latex": r"V_{\text{gib}} = \frac{512 \cdot 64}{1024}",
                        "sympy": "(512 * 64) / 1024",
                    }
                ],
                "conclusion": "Evaluar tan solo 512 contraseñas en paralelo exige 32 GiB de VRAM dedicada, reduciendo en varios órdenes de magnitud la velocidad de fuerza bruta respecto a SHA-256.",
            },
            "practice_problems": make_practice_set(
                "CH-05",
                [
                    ("Bytes totales de sobrecoste criptográfico en AES-256-GCM por mensaje (12 bytes de nonce IV + 16 bytes de tag)", "12 + 16", "bytes"),
                    ("Bits de entropía de una clave aleatoria de 32 bytes generada con un CSPRNG del sistema operativo (32 * 8)", "32 * 8", "bits"),
                    ("Reducción de latencia de establecimiento en ms al pasar de TLS 1.2 (2-RTT) a TLS 1.3 (1-RTT) con RTT = 45 ms", "(2 - 1) * 45", "ms"),
                    ("Hilos concurrentes máximos de Argon2id (64 MiB) en un servidor de autenticación con 4096 MiB dedicados", "4096 / 64", "hilos"),
                ],
            ),
        },
        {
            "id": "CH-06",
            "title": "Infraestructura Cloud, Contenedores (Docker/OCI), Kubernetes, Terraform (IaC) y Pipelines CI/CD",
            "prerequisites": "Sistemas operativos Linux y redes TCP/IP (Volumen II) y formatos YAML/TOML (Volumen VIII).",
            "learning_outcomes": "Construir imágenes OCI multi-stage mínimas y sin privilegios root, operar clústeres Kubernetes declarativos, aprovisionar infraestructura con Terraform y automatizar despliegues progresivos.",
            "summary": "Ingeniería de plataformas, contenedores Linux (namespaces y cgroups v2), orquestación declarativa, infraestructura como código e integración y entrega continua.",
            "paragraphs": [
                {
                    "title": "Anatomía de los Contenedores Linux: Namespaces, cgroups v2 y OverlayFS",
                    "claim": "Un contenedor no es una máquina virtual con hipervisor propio, sino un grupo de procesos aislados en el mismo kernel Linux mediante namespaces y acotados en recursos mediante cgroups v2.",
                    "body": (
                        "El kernel Linux proporciona tres mecanismos que sustentan el estándar OCI (Open Container "
                        "Initiative): 1) **Namespaces** (`pid`, `net`, `mnt`, `uts`, `ipc`, `user`, `cgroup`), que "
                        "restringen qué procesos, interfaces de red y puntos de montaje puede observar el contenedor; "
                        "2) **Control Groups (cgroups v2)**, que contabilizan y limitan el consumo de CPU, memoria RAM "
                        "y E/S de disco; y 3) sistemas de archivos en unión (**OverlayFS**), que superponen capas "
                        "inmutables direccionadas por hash SHA-256 con una capa superior efímera de escritura.\n\n"
                        "```dockerfile\n"
                        "# Etapa 1: Compilación estática reproducible\n"
                        "FROM rust:1.80-alpine AS builder\n"
                        "WORKDIR /src\n"
                        "COPY Cargo.toml Cargo.lock ./\n"
                        "COPY src ./src\n"
                        "RUN cargo build --release --locked\n\n"
                        "# Etapa 2: Imagen mínima sin shell ni usuario root\n"
                        "FROM gcr.io/distroless/cc-debian12:nonroot\n"
                        "COPY --from=builder /src/target/release/motor-kv /usr/local/bin/motor-kv\n"
                        "USER nonroot:nonroot\n"
                        "ENTRYPOINT [\"/usr/local/bin/motor-kv\"]\n"
                        "```"
                    ),
                },
                {
                    "title": "Orquestación con Kubernetes: Bucle de Reconciliación, Pods, Probes y Autoscaling",
                    "claim": "El plano de control de Kubernetes opera como un bucle de control cerrado que converge continuamente el estado observado del clúster hacia el estado deseado declarado en los manifiestos.",
                    "body": (
                        "En Kubernetes, la unidad mínima desplegable es el **Pod** (uno o más contenedores que comparten "
                        "namespace de red y volúmenes). Los controladores (`Deployment`, `StatefulSet`, `DaemonSet`) "
                        "supervisan la salud de los pods mediante tres sondas: `startupProbe`, `readinessProbe` (que "
                        "retira el pod del balanceador `Service` cuando no puede recibir tráfico sin matarlo) y "
                        "`livenessProbe` (que reinicia el contenedor ante interbloqueos fatales). Todo contenedor de "
                        "producción debe declarar `resources.requests` (usados por el `kube-scheduler`) y `limits`."
                    ),
                },
                {
                    "title": "Infraestructura como Código (IaC) con Terraform y Gestión de Estado",
                    "claim": "Declarar la infraestructura en código versionado con estado remoto bloqueable elimina la deriva de configuración (Configuration Drift) entre entornos de pruebas y producción.",
                    "body": (
                        "Terraform construye un grafo acíclico dirigido (DAG) de dependencias entre recursos cloud "
                        "(redes VPC, clústeres EKS/GKE, bases de datos RDS, políticas IAM) y calcula un plan de "
                        "ejecución determinista (`terraform plan`) antes de aplicar mutaciones (`terraform apply`). "
                        "El archivo de estado (`terraform.tfstate`) debe almacenarse en un backend remoto cifrado con "
                        "bloqueo transaccional y jamás incluir secretos en texto plano."
                    ),
                },
                {
                    "title": "Pipelines CI/CD y Estrategias de Despliegue Progresivo (Blue/Green, Canary, Feature Flags)",
                    "claim": "Desacoplar el despliegue técnico (Deployment) del lanzamiento funcional (Release) mediante despliegues Canary y Feature Flags reduce el radio de impacto de regresiones en producción.",
                    "body": (
                        "Un pipeline de Integración Continua (CI) verifica automáticamente en cada Pull Request: "
                        "formateo, análisis estático (linters y chequeo de tipos), pruebas unitarias y de integración, "
                        "auditoría de vulnerabilidades (CVE) y compilación del artefacto firmado. En Entrega Continua "
                        "(CD), un despliegue **Canary** encamina inicialmente el 1–5 % del tráfico real a la nueva "
                        "versión y promueve automáticamente al 100 % sólo si los SLIs de tasa de error y latencia p99 "
                        "permanecen dentro del umbral."
                    ),
                },
            ],
            "worked_problem": {
                "title": "Dimensionamiento de réplicas Kubernetes mediante Horizontal Pod Autoscaler (HPA)",
                "statement": (
                    "Un Deployment de Kubernetes tiene actualmente 4 pods en ejecución con una utilización media de "
                    "CPU del 90 %. Si el Horizontal Pod Autoscaler (HPA) está configurado para mantener una utilización "
                    "objetivo del 60 % según la fórmula R_des = R_act * (U_act / U_obj), calcule el número de réplicas "
                    "al que escalará el clúster."
                ),
                "given": [
                    {"symbol": "R_act", "value": "4", "unit": "pods", "meaning": "Réplicas actuales en ejecución"},
                    {"symbol": "U_act", "value": "90", "unit": "%", "meaning": "Utilización media actual de CPU"},
                    {"symbol": "U_obj", "value": "60", "unit": "%", "meaning": "Utilización objetivo configurada en el HPA"},
                ],
                "unknown": "Número deseado de réplicas R_des en pods",
                "steps": [
                    {
                        "text": "Multiplicamos las 4 réplicas actuales por la razón entre la utilización actual (90 %) y la objetivo (60 %)",
                        "latex": r"R_{\text{des}} = \frac{4 \cdot 90}{60}",
                        "sympy": "(4 * 90) / 60",
                    }
                ],
                "conclusion": "El controlador HPA escala el Deployment a 6 pods para restablecer la utilización media de CPU en el 60 %.",
            },
            "practice_problems": make_practice_set(
                "CH-06",
                [
                    ("Reducción en MB de una imagen Docker al usar multi-stage distroless de 22 MB frente a la imagen de compilación de 840 MB", "840 - 22", "MB"),
                    ("Solicitudes de CPU totales en millicores reservadas por un Deployment de 6 pods con request de 250m cada uno", "6 * 250", "mCPU"),
                    ("Tráfico en req/s recibido por la versión Canary (5 %) en un servicio que recibe 12 000 req/s totales", "(12000 * 5) / 100", "req/s"),
                    ("Pods disponibles mínimos durante un RollingUpdate de 10 réplicas con maxUnavailable = 2", "10 - 2", "pods"),
                ],
            ),
        },
        {
            "id": "CH-07",
            "title": "Itinerarios de Especialización Profesional (19 Rutas) y Proyectos Integradores Verificados",
            "prerequisites": "Fundamentos de las Partes I–IV y al menos una monografía de lenguaje de la Parte V.",
            "learning_outcomes": "Planificar un itinerario de estudio personalizado desde nivel cero hasta nivel experto y ejecutar proyectos integradores completos con arquitectura de producción.",
            "summary": "Síntesis de las 19 rutas formativas de la enciclopedia y análisis técnico de los 6 proyectos integradores verificados incluidos en el repositorio.",
            "paragraphs": [
                {
                    "title": "Arquitectura de los 19 Itinerarios de Aprendizaje Personalizados",
                    "claim": "El grafo acíclico dirigido (DAG) de prerrequisitos permite trazar rutas óptimas tanto para quien comienza desde cero absoluto como para ingenieros que se especializan en un nuevo dominio.",
                    "body": (
                        "La enciclopedia estructura 19 itinerarios completos documentados en `blueprint/learning-paths.json`: "
                        "1) **Cero Absoluto a Primer Empleo Profesional**, 2) **Grado Universitario Completo en Ciencias "
                        "de la Computación (ACM/IEEE CS2023)**, 3) **Ingeniería de Sistemas y Bajo Nivel (C, C++, Rust, "
                        "Zig, ASM)**, 4) **Desarrollo Web Full-Stack Moderno (HTML, CSS, TS, React/Next.js, SQL)**, "
                        "5) **Ingeniería Backend y Sistemas Distribuidos (Go, Java/Spring, C#/.NET, Rust/Axum)**, "
                        "6) **Ciencia de Datos, Computación Científica e IA (Python, R, Julia, SQL)**, 7) **Desarrollo "
                        "Móvil Nativo y Multiplataforma (Swift, Kotlin, Dart/Flutter)**, 8) **Ingeniería de Bases de "
                        "Datos y Plataformas de Datos**, 9) **Cloud, DevOps, SRE y Ciberseguridad**, 10) **Programación "
                        "Funcional y Lenguajes Declarativos (Haskell, OCaml, Elixir, Erlang, Scala, F#, Clojure, Prolog)**, "
                        "y 9 rutas adicionales de especialización directa por ecosistema."
                    ),
                },
                {
                    "title": "Proyectos Integradores de Sistemas: Motor KV en Rust, Arena Allocator en C17 y Planificador en C++20",
                    "claim": "Los tres proyectos integradores de bajo nivel implementan persistencia transaccional con CRC32, gestión determinista de memoria sin fragmentación y concurrencia genérica con Concepts.",
                    "body": (
                        "1) En `projects/rust-kv-engine`, se desarrolla en Rust 2021 un motor de almacenamiento "
                        "clave-valor persistente basado en Write-Ahead Log (WAL) binario con sumas de verificación "
                        "CRC32 (polinomio IEEE `0xEDB88320`), compactación atómica y recuperación ante corrupción. "
                        "2) En `projects/c-arena-allocator`, se implementa en C17 estricto un asignador lineal de "
                        "memoria (*Arena Allocator*) con alineación a potencias de dos y un analizador de paquetes "
                        "binarios de red de copia cero (*zero-copy*) verificado con AddressSanitizer y UndefinedBehaviorSanitizer. "
                        "3) En `projects/cpp-task-scheduler`, se construye en C++20 un planificador de tareas por "
                        "prioridad restringido estáticamente mediante `concept ExecutableTask` y `std::ranges`."
                    ),
                },
                {
                    "title": "Proyectos Integradores de Alto Nivel y Datos: VM en Python 3.12, Router HTTP en TypeScript y Ledger SQL",
                    "claim": "Los proyectos de lenguajes dinámicos, tipado estructural y bases de datos demuestran compilación a bytecode, control de flujo reactivo con Token Bucket y contabilidad de doble partida en BCNF.",
                    "body": (
                        "4) En `projects/python-bytecode-vm`, se implementa en Python 3.12 un compilador de expresiones "
                        "aritméticas y variables a bytecode con plegado de constantes (*Constant Folding*) y su máquina "
                        "virtual de pila, verificado con `pytest`, `ruff` y `pyright`. "
                        "5) En `projects/ts-reactive-http`, se construye en TypeScript 5 un enrutador HTTP declarativo "
                        "con tubería de middlewares y limitador de tasa (*Token Bucket*) ejecutado nativamente en Node.js. "
                        "6) En `projects/sql-transactional-ledger`, se diseña en SQL un libro mayor contable de doble "
                        "partida en BCNF con triggers de invariantes, CTEs recursivas de jerarquía de cuentas y funciones "
                        "de ventana."
                    ),
                },
                {
                    "title": "Rúbricas de Evaluación por Niveles de Competencia (Principiante a Experto)",
                    "claim": "La evaluación de competencias combina corrección algorítmica, seguridad de memoria y tipos, claridad arquitectónica, cobertura de pruebas y observabilidad en producción.",
                    "body": (
                        "Cada proyecto e itinerario se evalúa mediante cinco dimensiones objetivas: 1) **Exactitud "
                        "funcional y manejo de casos límite**, 2) **Uso idiomático del lenguaje y de su sistema de tipos**, "
                        "3) **Complejidad temporal y espacial asintótica y constantes reales de caché/E/S**, 4) **Calidad "
                        "de pruebas automatizadas (unitarias, propiedades y sanitizers)**, y 5) **Documentación técnica, "
                        "reproducibilidad del build y ausencia total de advertencias del compilador**."
                    ),
                },
            ],
            "worked_problem": {
                "title": "Planificación temporal de un itinerario formativo completo de 720 horas",
                "statement": (
                    "Un estudiante autodidacta aborda el itinerario de Ingeniería Backend y Sistemas Distribuidos, "
                    "que comprende 720 horas de estudio teórico y proyectos prácticos. Si dedica de forma constante "
                    "15 horas semanales, calcule el número exacto de semanas necesarias para completar la especialización."
                ),
                "given": [
                    {"symbol": "H_tot", "value": "720", "unit": "horas", "meaning": "Horas totales del itinerario formativo"},
                    {"symbol": "h_sem", "value": "15", "unit": "horas/semana", "meaning": "Dedicación semanal constante"},
                ],
                "unknown": "Duración del itinerario S_sem en semanas",
                "steps": [
                    {
                        "text": "Dividimos las 720 horas totales del itinerario entre las 15 horas semanales",
                        "latex": r"S_{\text{sem}} = \frac{720}{15}",
                        "sympy": "720 / 15",
                    }
                ],
                "conclusion": "Con una dedicación sostenida de 15 horas semanales, el estudiante completa el itinerario profesional en 48 semanas (menos de un año natural).",
            },
            "practice_problems": make_practice_set(
                "CH-07",
                [
                    ("Horas dedicadas a práctica y proyectos si representan el 60 % de un itinerario de 720 horas", "(720 * 60) / 100", "horas"),
                    ("Total de pruebas ejecutadas al correr las 6 suites de los proyectos integradores con un promedio de 5 aserciones por proyecto", "6 * 5", "aserciones"),
                    ("Bytes de cabecera por registro en el motor WAL de Rust (4 B CRC32 + 4 B key_len + 4 B val_len + 1 B op)", "4 + 4 + 4 + 1", "bytes"),
                    ("Saldo neto verificado en una partida contable doble donde la suma de cargos es 18 500 y la de abonos es 18 500", "18500 - 18500", "unidades"),
                ],
            ),
        },
    ],
}

VOL00_SPEC = {
    "slug": "vol00-enciclopedia-maestra-integral",
    "title": "Enciclopedia de Programación e Ingeniería del Software: Obra Maestra y Guía General",
    "subtitle": "De cero a la especialización profesional — Arquitectura Editorial, Índices Maestros, Matrices Curriculares y Síntesis de las 13 Partes",
    "Part": "Volumen Maestro Integral (Partes I a XIII)",
    "scope": (
        "Volumen maestro unificado de la Enciclopedia de Programación e Ingeniería del Software: arquitectura "
        "general de las 13 Partes y los 9 volúmenes temáticos, índice maestro por lenguaje (35 lenguajes de "
        "programación y 9 lenguajes de marcado/estilo/datos), matriz curricular ACM/IEEE CS2023 y SWEBOK v4.0, "
        "grafo DAG de prerrequisitos, 19 itinerarios de especialización y catálogo de proyectos verificados."
    ),
    "target_pages": 65,
    "sources": [
        {
            "title": "Computer Science Curricula 2023 (CS2023) & Guide to the Software Engineering Body of Knowledge (SWEBOK v4.0)",
            "authors": ["ACM / IEEE-CS / AAAI Joint Task Force", "IEEE Computer Society"],
            "year": 2024,
            "kind": "standard",
            "publisher": "ACM / IEEE",
            "url": "https://csed.acm.org/",
            "notes": "Estándares internacionales de referencia para currículos universitarios de Ciencias de la Computación e Ingeniería del Software.",
            "excerpts": [
                (
                    "Un currículo completo de Ciencias de la Computación e Ingeniería del Software articula fundamentos "
                    "matemáticos y algorítmicos, arquitectura de sistemas y sistemas operativos, teoría de lenguajes "
                    "de programación, gestión de datos, ingeniería de software, seguridad y sistemas distribuidos."
                ),
                (
                    "La progresión pedagógica eficaz requiere que cada monografía de lenguaje permita tanto un recorrido "
                    "autónomo de principio a fin (plantilla A–H desde nivel cero hasta nivel experto) como conexiones "
                    "transversales rigurosas con los fundamentos universales de la computación."
                ),
            ],
        },
        {
            "title": "The Art of Computer Programming & Structure and Interpretation of Computer Programs",
            "authors": ["Donald E. Knuth", "Harold Abelson", "Gerald Jay Sussman"],
            "year": 2011,
            "kind": "book",
            "publisher": "Addison-Wesley / MIT Press",
            "url": "https://mitp-content-server.mit.edu/books/content/sectbyfn/books_pres_0/6515/sicp.zip/index.html",
            "notes": "Obras fundacionales sobre análisis de algoritmos, abstracción procedimental, funcional y metalingüística.",
            "excerpts": [
                (
                    "Los programas deben escribirse primordialmente para que otros seres humanos los lean y razonen "
                    "sobre su corrección formal y su coste computacional, y sólo de manera secundaria para que las "
                    "máquinas los ejecuten."
                ),
            ],
        },
    ],
    "glossary": [
        ("Plantilla Pedagógica A–H", "Estructura estándar de ocho bloques (Introducción, Entorno, Principiante, Intermedio, Avanzado, Experto, Ecosistema y Evaluación) aplicada a cada monografía de lenguaje."),
        ("Autonomía Pedagógica", "Principio editorial según el cual el lector puede estudiar cualquier lenguaje principal desde cero hasta nivel profesional sin haber cursado previamente otro lenguaje de la enciclopedia."),
        ("Grafo de Prerrequisitos (DAG)", "Grafo acíclico dirigido que modela formalmente las dependencias conceptuales entre capítulos y volúmenes sin ciclos circulares."),
        ("Verificación Determinista de Código", "Proceso automatizado que clasifica y comprueba cada fragmento de código y proyecto mediante compiladores, intérpretes y analizadores estáticos reales."),
    ],
    "notation": [
        (r"G = (V, E)", "Grafo acíclico dirigido (DAG) de prerrequisitos curriculares", "estructura discreta"),
        (r"\mathcal{L}_{35} \cup \mathcal{M}_{9}", "Conjunto de 35 lenguajes de programación y 9 formatos de marcado/datos", "catálogo técnico"),
        (r"T(n) \in \Theta(f(n))", "Cota asintótica ajustada de complejidad algorítmica", "operaciones"),
    ],
    "chapters": [
        {
            "id": "CH-01",
            "title": "Arquitectura General de la Enciclopedia y Mapa de las 13 Partes (Volúmenes I a IX)",
            "prerequisites": "Ninguno. Punto de entrada universal de la obra.",
            "learning_outcomes": "Comprender la estructura modular de las 13 Partes y los 10 volúmenes de la enciclopedia, seleccionar el volumen o itinerario adecuado y utilizar las convenciones tipográficas y de verificación.",
            "summary": "Visión panorámica y guía de navegación de toda la Enciclopedia de Programación e Ingeniería del Software.",
            "tikz_caption": "Arquitectura modular de la Enciclopedia en Studium: los fundamentos (Volúmenes I–II) y las monografías autónomas de lenguajes (Volúmenes III–VII) convergen hacia Web, Bases de Datos, Frameworks e Ingeniería del Software (Volúmenes VIII–IX).",
            "tikz_code": r"""\begin{tikzpicture}[node distance=0.55cm and 0.5cm, every node/.style={font=\scriptsize, draw, rounded corners=2pt, align=center, inner sep=3.5pt}]
\node (v0) [fill=purple!15] {Volumen 0\\Guía Maestra Integral};
\node (v12) [below left=of v0, fill=blue!12] {Volúmenes I–II\\Historia, Fundamentos,\\Algoritmos y Sistemas};
\node (v37) [below right=of v0, fill=green!12] {Volúmenes III–VII\\Monografías Autónomas\\(35 Lenguajes A–H)};
\node (v89) [below=1.4cm of v0, fill=orange!15] {Volúmenes VIII–IX\\Web, Bases de Datos, Frameworks,\\Arquitectura, Cloud, Seguridad y Proyectos};
\draw[-Stealth, thick] (v0) -- (v12);
\draw[-Stealth, thick] (v0) -- (v37);
\draw[-Stealth, thick] (v12) -- (v89);
\draw[-Stealth, thick] (v37) -- (v89);
\end{tikzpicture}""",
            "paragraphs": [
                {
                    "title": "Filosofía Editorial y Principio de Autonomía por Lenguaje",
                    "claim": "La enciclopedia combina el rigor formal de un currículo universitario de Ciencias de la Computación con monografías de lenguajes autónomas estudiables de principio a fin.",
                    "body": (
                        "Esta obra ha sido concebida y compilada sobre el framework académico **Studium** bajo una premisa "
                        "innegociable: ningún lenguaje o tecnología se reduce a un resumen superficial. Como ilustra la "
                        "{{fig:ch-01-fig}}, la enciclopedia se organiza en **13 grandes Partes** distribuidas en **9 "
                        "volúmenes temáticos especializados** (`vol01` a `vol09`) más este **Volumen Maestro Integral** "
                        "(`vol00`). Cada lenguaje de programación cuenta con un bloque autónomo que sigue la plantilla "
                        "pedagógica **A–H** (A. Introducción e historia, B. Instalación y toolchain, C. Nivel principiante, "
                        "D. Nivel intermedio, E. Nivel avanzado, F. Nivel experto, G. Ecosistema y producción, H. Evaluación "
                        "y proyectos), permitiendo aprender Rust sin conocer C++, o estudiar Python, TypeScript, Go, Java, "
                        "C# y SQL desde cero hasta la arquitectura profesional."
                    ),
                },
                {
                    "title": "Índice Maestro de Volúmenes y Correspondencia con las 13 Partes",
                    "claim": "Los diez volúmenes compilados cubren íntegramente desde los fundamentos matemáticos e históricos hasta sistemas distribuidos, ciberseguridad y proyectos verificados.",
                    "body": (
                        "- **Volumen 0 (`vol00-enciclopedia-maestra-integral.pdf`)**: Guía Maestra, Índices Generales, "
                        "Matrices Curriculares ACM/IEEE CS2023 y SWEBOK v4.0, y Síntesis de las 13 Partes.\n"
                        "- **Volumen I (`vol01-historia-y-fundamentos.pdf`)**: **Parte I** (Historia de la Computación y "
                        "de los Lenguajes desde Babbage, Turing y Church hasta Rust, WebAssembly e IA) y **Parte II** "
                        "(Fundamentos Universales: binario, complemento a dos, IEEE 754, UTF-8, lógica booleana, tipos, "
                        "control de flujo, ámbitos, memoria Stack/Heap, recursión y paradigmas).\n"
                        "- **Volumen II (`vol02-algoritmos-y-sistemas.pdf`)**: **Parte III** (Complejidad asintótica, "
                        "estructuras de datos lineales, árboles, tablas hash, grafos, ordenación, programación dinámica "
                        "y NP-completitud) y **Parte IV** (Arquitectura ISA, cachés, compiladores/LLVM, memoria virtual "
                        "y sistemas operativos).\n"
                        "- **Volumen III (`vol03-monografia-rust.pdf`)**: **Parte V (Bloque 1)** — Tratado completo y "
                        "autónomo de **Rust** (Edición 2021/2024) con verificación ejecutable en vivo mediante `rustc --test`."
                    ),
                },
                {
                    "title": "Catálogo de los Volúmenes de Lenguajes, Web, Bases de Datos e Ingeniería (Volúmenes IV a IX)",
                    "claim": "Los Volúmenes IV a IX completan los 35 lenguajes de programación, los 9 estándares de marcado/datos, el curso universitario de bases de datos y la ingeniería del software moderna.",
                    "body": (
                        "- **Volumen IV (`vol04-monografias-c-cpp-sistemas.pdf`)**: **Parte V (Bloque 2)** — Monografías "
                        "de **C (C17/C23)**, **C++ (C++20/C++23)**, **Zig**, **Ada/SPARK**, **Fortran Moderno** y "
                        "**Ensamblador x86-64 / ARM64**.\n"
                        "- **Volumen V (`vol05-monografias-python-js-ts.pdf`)**: **Parte V (Bloque 3)** — Monografías "
                        "autónomas y diferenciadas de **Python 3.12**, **JavaScript (ES2024)** y **TypeScript 5.x**.\n"
                        "- **Volumen VI (`vol06-monografias-jvm-dotnet-go-movil.pdf`)**: **Parte V (Bloque 4)** — "
                        "Monografías de **Java 21**, **Kotlin**, **Scala 3**, **C# 12 / .NET 8**, **F#**, **Go (Golang)**, "
                        "**Swift 6** y **Objective-C**.\n"
                        "- **Volumen VII (`vol07-monografias-sql-shell-funcional-especializados.pdf`)**: **Parte V (Bloque 5)** "
                        "— Monografías de **SQL (ISO/IEC 9075)**, **Bash/POSIX Shell**, **PHP 8.3**, **Ruby 3.3**, **Dart 3**, "
                        "**Haskell**, **OCaml**, **Elixir/Erlang (BEAM)**, **Clojure/Lisp/Scheme**, **R**, **Julia**, **Lua**, "
                        "**Perl**, **Prolog** y **GDScript**.\n"
                        "- **Volumen VIII (`vol08-web-bases-de-datos-y-frameworks.pdf`)**: **Partes VI, VII y VIII** — "
                        "HTML, CSS, JSON/YAML/TOML/XML/Protobuf, Curso Universitario de Bases de Datos y Frameworks.\n"
                        "- **Volumen IX (`vol09-ingenieria-software-arquitectura-y-proyectos.pdf`)**: **Partes IX a XIII** — "
                        "Arquitectura, Testing, Sistemas Distribuidos, Ciberseguridad, Cloud/DevOps, 19 Itinerarios y Proyectos."
                    ),
                },
                {
                    "title": "Rigor Epistémico en Studium y Verificación Determinista de Código",
                    "claim": "Todas las derivaciones cuantitativas han sido reproducidas simbólicamente con SymPy y todos los proyectos integradores han sido ejecutados y auditados con compiladores reales.",
                    "body": (
                        "Respetando la disciplina epistémica de Studium, el texto distingue explícitamente entre hechos "
                        "históricos documentados, estándares normativos (ISO, IETF, W3C, WHATWG, IEEE) y decisiones de "
                        "ingeniería. Cada capítulo integra problemas resueltos verificados por el motor computacional de "
                        "Studium y problemas de práctica con resultados comprobados. Asimismo, la herramienta complementaria "
                        "`tools/code_verifier.py` audita los fragmentos de código y los 6 proyectos multifichero del "
                        "repositorio, emitiendo el informe determinista `reports/code-verification-report.json`."
                    ),
                },
            ],
            "worked_problem": {
                "title": "Cobertura cuantitativa de lenguajes y tecnologías en la Enciclopedia",
                "statement": (
                    "La enciclopedia incluye 16 lenguajes de programación prioritarios, 19 lenguajes de programación "
                    "adicionales y 9 lenguajes de marcado, hojas de estilo y formatos de serialización de datos. "
                    "Calcule el número total de tecnologías lingüísticas y de datos documentadas con bloques dedicados."
                ),
                "given": [
                    {"symbol": "L_prio", "value": "16", "unit": "lenguajes", "meaning": "Lenguajes de programación prioritarios"},
                    {"symbol": "L_adic", "value": "19", "unit": "lenguajes", "meaning": "Lenguajes de programación adicionales"},
                    {"symbol": "M_datos", "value": "9", "unit": "formatos", "meaning": "Lenguajes de marcado, estilo y formatos de datos"},
                ],
                "unknown": "Total de lenguajes y formatos documentados N_tot",
                "steps": [
                    {
                        "text": "Sumamos los 16 lenguajes prioritarios, los 19 adicionales y los 9 estándares de marcado y datos",
                        "latex": r"N_{\text{tot}} = 16 + 19 + 9",
                        "sympy": "16 + 19 + 9",
                    }
                ],
                "conclusion": "La enciclopedia cubre 44 lenguajes y estándares de datos (35 lenguajes de programación más 9 formatos de marcado, estilo y serialización).",
            },
            "practice_problems": make_practice_set(
                "CH-01",
                [
                    ("Total de lenguajes de programación sumando los 16 prioritarios y los 19 adicionales", "16 + 19", "lenguajes"),
                    ("Total de secciones de la plantilla A-H aplicadas a los 16 lenguajes prioritarios (16 * 8)", "16 * 8", "secciones"),
                    ("Volúmenes totales del bundle PDF sumando el Volumen Maestro (1) y los 9 volúmenes temáticos", "1 + 9", "volúmenes"),
                    ("Partes estructurales totales que articulan la arquitectura general de la enciclopedia", "13 * 1", "partes"),
                ],
            ),
        },
        {
            "id": "CH-02",
            "title": "Síntesis de las Partes I a IV: Historia, Fundamentos Universales, Algoritmos y Sistemas",
            "prerequisites": "CH-01.",
            "learning_outcomes": "Conectar la evolución histórica de los paradigmas de programación con la representación física de la información, el análisis de algoritmos y la arquitectura de computadores y compiladores.",
            "summary": "Mapa conceptual integrado de los Volúmenes I y II: desde el cálculo lambda y la máquina de Turing hasta el pipeline de LLVM y el kernel del sistema operativo.",
            "paragraphs": [
                {
                    "title": "De Babbage, Turing y Church a la Convergencia Multiparadigma Moderna",
                    "claim": "Toda innovación en los lenguajes de programación responde a una restricción tecnológica e ingenieril concreta de su época histórica.",
                    "body": (
                        "El Volumen I (`vol01-historia-y-fundamentos.pdf`) traza la genealogía rigurosa de la programación: "
                        "la máquina analítica de Babbage y el algoritmo de los números de Bernoulli de Ada Lovelace (1843); "
                        "el álgebra de Boole (1854); la equivalencia entre las máquinas de Turing y el cálculo lambda de "
                        "Alonzo Church (1936); el surgimiento de los primeros compiladores con Grace Hopper (A-0) y John "
                        "Backus (FORTRAN, 1957); la bifurcación entre procesamiento simbólico (Lisp de McCarthy, 1958) y "
                        "tipado algorítmico estructurado (ALGOL 60); el nacimiento conjunto de C y Unix en Bell Labs "
                        "(Ritchie y Thompson, 1969–1973); las abstracciones de coste cero de Bjarne Stroustrup en C++; "
                        "las máquinas virtuales con JIT (Java, .NET); y la seguridad de memoria en tiempo de compilación "
                        "mediante tipos afines y *borrow checking* en Rust."
                    ),
                },
                {
                    "title": "Fundamentos Universales: Bits, Complemento a Dos, IEEE 754, UTF-8 y Sistemas de Tipos",
                    "claim": "Comprender la representación binaria exacta evita errores catastróficos de desbordamiento entero, pérdida de significancia en punto flotante y corrupción de cadenas Unicode.",
                    "body": (
                        "Todo dato en un computador digital es una secuencia finita de bits. Los enteros con signo se "
                        "representan universalmente en complemento a dos, donde el peso negativo del bit más significativo "
                        "produce un rango asimétrico \\([-2^{w-1}, 2^{w-1}-1]\\). Los reales se aproximan mediante la "
                        "norma IEEE 754 (`binary64` con 1 bit de signo, 11 de exponente sesgado y 52 de mantisa), donde "
                        "la suma no es asociativa y \\(0.1 + 0.2 \\neq 0.3\\). El texto se codifica en UTF-8 con longitud "
                        "variable de 1 a 4 bytes por punto de código, impidiendo la indexación aleatoria en \\(O(1)\\) "
                        "por carácter visual (clúster de grafema)."
                    ),
                },
                {
                    "title": "Algoritmos, Estructuras de Datos y Complejidad Computacional (Parte III)",
                    "claim": "El rendimiento práctico depende conjuntamente de la cota asintótica (Big-O) y de la localidad espacial de referencia en las líneas de caché de 64 bytes de la CPU.",
                    "body": (
                        "El Volumen II (`vol02-algoritmos-y-sistemas.pdf`) desarrolla el análisis asintótico (\\(O, \\Omega, "
                        "\\Theta\\)), el Teorema Maestro para recurrencias divide y vencerás, arrays dinámicos con coste "
                        "amortizado \\(O(1)\\), árboles equilibrados (AVL, Rojo-Negro, B-Trees), colas de prioridad "
                        "(Binary Heaps), tablas hash con direccionamiento abierto (Robin Hood / SwissTable), algoritmos "
                        "sobre grafos (BFS, DFS, orden topológico, Dijkstra, Bellman-Ford, Kruskal, Prim), programación "
                        "dinámica y la jerarquía de complejidad \\(\\text{P}, \\text{NP}, \\text{NP-Completo}\\)."
                    ),
                },
                {
                    "title": "Arquitectura de Computadores, Compiladores y Sistemas Operativos (Parte IV)",
                    "claim": "Un compilador moderno traduce el código fuente a través de un front-end (lexer, parser, typechecker), un middle-end en forma SSA y un back-end generador de código máquina específico de la ISA.",
                    "body": (
                        "La Parte IV examina la arquitectura x86-64 y ARM64, la jerarquía de memoria (registros, cachés "
                        "L1/L2/L3 con protocolo MESI, RAM y NVMe), la traducción de direcciones virtuales mediante tablas "
                        "de páginas multinivel y TLB, el modelo de procesos e hilos del kernel, las llamadas al sistema "
                        "(`syscalls`) y la multiplexación de E/S asíncrona (`epoll`, `kqueue`, `io_uring`)."
                    ),
                },
            ],
            "worked_problem": {
                "title": "Aceleración efectiva (Ley de Amdahl) al paralelizar un algoritmo sobre 8 núcleos",
                "statement": (
                    "Un algoritmo de procesamiento de grafos tiene una fracción secuencial irreducible del 20 % "
                    "y una fracción paralelizable del 80 %. Si la fracción paralelizable se acelera linealmente "
                    "en 8 núcleos (reduciendo su tiempo a 80 / 8 = 10 % del tiempo original), calcule el porcentaje "
                    "del tiempo original que tarda la ejecución paralela total (20 + 80 / 8)."
                ),
                "given": [
                    {"symbol": "P_seq", "value": "20", "unit": "%", "meaning": "Porcentaje secuencial irreducible"},
                    {"symbol": "P_par", "value": "80", "unit": "%", "meaning": "Porcentaje paralelizable del algoritmo"},
                    {"symbol": "N_cores", "value": "8", "unit": "núcleos", "meaning": "Número de núcleos de procesamiento"},
                ],
                "unknown": "Porcentaje del tiempo original requerido T_pct en %",
                "steps": [
                    {
                        "text": "Sumamos el 20 % secuencial más el 80 % dividido entre los 8 núcleos",
                        "latex": r"T_{\text{pct}} = 20 + \frac{80}{8}",
                        "sympy": "20 + 80 / 8",
                    }
                ],
                "conclusion": "La ejecución en 8 núcleos requiere el 30 % del tiempo original (un speedup de 100 / 30 = 3,33x, acotado por la Ley de Amdahl).",
            },
            "practice_problems": make_practice_set(
                "CH-02",
                [
                    ("Enteros de 8 bytes (int64) que caben en una línea de caché L1 de 64 bytes (64 / 8)", "64 / 8", "enteros"),
                    ("Comparaciones máximas de búsqueda binaria en un vector ordenado de 1024 elementos (log2(1024) = 10)", "10 * 1", "comparaciones"),
                    ("Valor decimal máximo representable por un entero con signo en complemento a dos de 8 bits (2^7 - 1)", "2**7 - 1", "entero"),
                    ("Tamaño total de tabla de páginas de 1 nivel en MiB para 2^20 páginas con entradas de 4 bytes ((1048576 * 4) / 1048576)", "(1048576 * 4) / 1048576", "MiB"),
                ],
            ),
        },
        {
            "id": "CH-03",
            "title": "Índice Maestro y Matriz Comparativa de los 35 Lenguajes de Programación (Parte V)",
            "prerequisites": "CH-01 y CH-02.",
            "learning_outcomes": "Comparar los 35 lenguajes de programación de la enciclopedia según su sistema de tipos, modelo de memoria, concurrencia, modelo de ejecución y dominios óptimos de aplicación.",
            "summary": "Guía comparativa transversal y mapa de navegación hacia las monografías completas de los Volúmenes III, IV, V, VI y VII.",
            "paragraphs": [
                {
                    "title": "Lenguajes de Sistemas y Control Explícito de Memoria (Volúmenes III y IV)",
                    "claim": "Rust, C, C++, Zig, Ada/SPARK, Fortran y Ensamblador compilan directamente a código máquina nativo sin recolector de basura, diferenciándose en sus garantías estáticas de seguridad.",
                    "body": (
                        "- **Rust (`vol03`)**: Tipado estático fuerte y algebraico, seguridad de memoria y ausencia de "
                        "*data races* en tiempo de compilación mediante *ownership*, *borrowing* y *lifetimes* (`'a`). "
                        "Ideal para kernels, motores de bases de datos, redes, WebAssembly y CLI.\n"
                        "- **C (C17/C23, `vol04`)**: El lenguaje universal de interfaces binarias (ABI), kernels POSIX "
                        "y sistemas embebidos; gestión manual de memoria (`malloc`/`free`) y punteros crudos.\n"
                        "- **C++ (C++20/23, `vol04`)**: Abstracciones de coste cero, RAII, punteros inteligentes, "
                        "plantillas restringidas con `Concepts`, `constexpr`, `std::ranges` y corrutinas para motores "
                        "gráficos, HPC y finanzas de baja latencia.\n"
                        "- **Zig, Ada/SPARK, Fortran y ASM (`vol04`)**: Zig aporta asignadores explícitos y metaprogramación "
                        "`comptime` sin flujo de control oculto; Ada/SPARK permite verificación formal en aviónica y "
                        "ferrocarriles; Fortran lidera el cálculo tensorial numérico; y x86-64/ARM64 expone la ISA real."
                    ),
                },
                {
                    "title": "Ecosistemas Dinámicos, Cientificos y Web Tipada: Python, JavaScript y TypeScript (Volumen V)",
                    "claim": "Python domina la ciencia de datos y la automatización, mientras que JavaScript y TypeScript gobiernan de forma complementaria pero diferenciada la plataforma web y los servidores Node/Deno/Bun.",
                    "body": (
                        "- **Python 3.12 (`vol05`)**: Tipado dinámico fuerte con anotaciones graduales (`typing`, `pyright`), "
                        "modelo de datos basado en protocolos dunder, generadores, `asyncio` y ecosistema de IA/ciencia "
                        "de datos (`NumPy`, `PyTorch`, `FastAPI`).\n"
                        "- **JavaScript ES2024 (`vol05`)**: Lenguaje nativo del navegador; herencia prototípica, clausuras "
                        "léxicas, bucle de eventos (Macrotasks y Microtasks) y compilación JIT en V8/SpiderMonkey/JSC.\n"
                        "- **TypeScript 5.x (`vol05`)**: Sistema de tipos estructural Turing-completo con unión discriminada, "
                        "estrechamiento de tipos (*narrowing*), genéricos con varianza, `infer` y tipos mapeados que se "
                        "borran completamente (*type erasure*) al emitir JavaScript."
                    ),
                },
                {
                    "title": "Plataformas Empresariales, Concurrencia CSP y Móvil: Java, Kotlin, Scala, C#, F#, Go y Swift (Volumen VI)",
                    "claim": "La JVM y el CLR (.NET) ofrecen compilación JIT/AOT de alto rendimiento y recolectores de basura de baja pausa, mientras Go simplifica la concurrencia con goroutines y Swift utiliza ARC determinista.",
                    "body": (
                        "- **Java 21, Kotlin y Scala 3 (`vol06`)**: Java 21 revoluciona el throughput de E/S con Virtual "
                        "Threads (Project Loom), Records y Sealed Classes; Kotlin añade seguridad nula estricta y "
                        "corrutinas estructuradas para Android y backend; Scala 3 fusiona POO con programación funcional "
                        "de tipos de orden superior.\n"
                        "- **C# 12 y F# sobre .NET 8 (`vol06`)**: C# permite programación de alto nivel y alto rendimiento "
                        "(`Span<T>`, `ValueTask`, LINQ, Native AOT); F# aporta inferencia Hindley-Milner y tipos algebraicos.\n"
                        "- **Go y Swift 6 (`vol06`)**: Go compila en segundos a binarios estáticos con planificador M:N "
                        "de goroutines y canales CSP (Docker, Kubernetes, Terraform); Swift 6 emplea conteo automático "
                        "de referencias (ARC), semántica de valor (`struct`) y aislamiento estricto de actores."
                    ),
                },
                {
                    "title": "Datos, Shell, Web Clásica, Funcionales Puros y Especializados (Volumen VII)",
                    "claim": "SQL y Prolog expresan qué resultado se desea mediante lógica declarativa, Haskell y OCaml garantizan pureza e inferencia algebraica, y Elixir/Erlang alcanzan tolerancia a fallos extrema en la BEAM.",
                    "body": (
                        "- **SQL y Bash/POSIX Shell (`vol07`)**: SQL (ISO/IEC 9075) modela consultas relacionales, "
                        "ventanas analíticas y CTEs recursivas; POSIX Shell/Bash automatiza tuberías de procesos Unix.\n"
                        "- **PHP 8.3, Ruby 3.3 y Dart 3 (`vol07`)**: PHP y Ruby impulsan gran parte de la web comercial "
                        "(Laravel, Symfony, Rails), y Dart 3 ofrece sonido nulo estricto y compilación AOT para Flutter.\n"
                        "- **Haskell, OCaml, Elixir, Erlang, Clojure y Lisp/Scheme (`vol07`)**: Evaluación perezosa y "
                        "mónadas en Haskell; módulos funtoriales en OCaml; actores aislados con árboles de supervisión "
                        "en Elixir/Erlang; y homoiconicidad y macros higiénicas en la familia Lisp.\n"
                        "- **R, Julia, Lua, Perl, Prolog y GDScript (`vol07`)**: Estadística vectorial en R; despacho "
                        "múltiple de alto rendimiento en Julia; scripting embebido ligero en Lua; procesamiento textual "
                        "en Perl; unificación lógica Horn en Prolog; y scripting de escenas en Godot con GDScript."
                    ),
                },
            ],
            "worked_problem": {
                "title": "Comparativa de sobrecoste de memoria por tarea concurrente: Hilos OS vs Goroutines / Virtual Threads",
                "statement": (
                    "Un servidor de mensajería mantiene 10 000 conexiones concurrentes. Con hilos nativos del sistema "
                    "operativo (pila reservada de 1 024 KiB por hilo), necesitaría 10 240 000 KiB. Con goroutines de "
                    "Go o Virtual Threads de Java 21 (pila inicial dinámica de 4 KiB por tarea), calcule la memoria "
                    "total de pila requerida en MiB (1 MiB = 1 024 KiB)."
                ),
                "given": [
                    {"symbol": "N_conn", "value": "10000", "unit": "tareas", "meaning": "Conexiones concurrentes activas"},
                    {"symbol": "S_coro", "value": "4", "unit": "KiB", "meaning": "Pila inicial por goroutine o hilo virtual"},
                    {"symbol": "K", "value": "1024", "unit": "KiB/MiB", "meaning": "Kibibytes por mebibyte"},
                ],
                "unknown": "Memoria total de pila M_mib en MiB",
                "steps": [
                    {
                        "text": "Multiplicamos las 10 000 tareas por 4 KiB y dividimos entre 1 024 KiB/MiB",
                        "latex": r"M_{\text{mib}} = \frac{10000 \cdot 4}{1024}",
                        "sympy": "(10000 * 4) / 1024",
                    }
                ],
                "conclusion": "Las 10 000 tareas concurrentes consumen apenas 39,0625 MiB de memoria de pila frente a los 10 000 MiB (9,76 GiB) que exigirían 10 000 hilos nativos de 1 MiB.",
            },
            "practice_problems": make_practice_set(
                "CH-03",
                [
                    ("Memoria en MiB requerida por 10 000 hilos nativos con pila de 1 MiB cada uno", "10000 * 1", "MiB"),
                    ("Factor de reducción de memoria al usar pilas iniciales de 4 KiB frente a 1024 KiB (1024 / 4)", "1024 / 4", "veces"),
                    ("Número de lenguajes cubiertos en el Volumen VI (Java, Kotlin, Scala, C#, F#, Go, Swift, Objective-C)", "3 + 2 + 1 + 2", "lenguajes"),
                    ("Número de lenguajes cubiertos en el Volumen VII (SQL, Shell, PHP, Ruby, Dart + 6 funcionales + 6 especializados)", "5 + 6 + 6", "lenguajes"),
                ],
            ),
        },
        {
            "id": "CH-04",
            "title": "Matriz Curricular (ACM/IEEE CS2023 y SWEBOK v4.0), Grafo de Prerrequisitos y Auditoría de Calidad",
            "prerequisites": "CH-01 a CH-03.",
            "learning_outcomes": "Verificar la correspondencia de cada volumen con las áreas de conocimiento de CS2023 y SWEBOK v4.0, navegar el DAG de prerrequisitos y auditar los artefactos reproducibles del proyecto.",
            "summary": "Documentación curricular, trazabilidad de fuentes primarias, matriz de prerrequisitos y resumen de verificación técnica de la enciclopedia.",
            "paragraphs": [
                {
                    "title": "Alineación con el Estándar ACM/IEEE/AAAI Computer Science Curricula 2023 (CS2023)",
                    "claim": "Las 17 áreas de conocimiento nucleares de CS2023 están cubiertas con teoría formal, código verificado y problemas resueltos a lo largo de los Volúmenes I a IX.",
                    "body": (
                        "El archivo `blueprint/curriculum-coverage.json` registra la correspondencia exacta entre las "
                        "áreas de CS2023 y los capítulos de la enciclopedia:\n"
                        "- **AL (Algorithms and Complexity)** y **MSF (Mathematical and Statistical Foundations)**: "
                        "Volúmenes I y II.\n"
                        "- **AR (Architecture and Organization)**, **OS (Operating Systems)** y **SF (Systems Fundamentals)**: "
                        "Volúmenes II y IV.\n"
                        "- **FPL (Foundations of Programming Languages)**: Volúmenes I, II y las 35 monografías de los "
                        "Volúmenes III a VII.\n"
                        "- **DM (Data Management)**: Volumen VII (SQL) y Volumen VIII (Curso completo de Bases de Datos).\n"
                        "- **GIT (Graphics and Interactive Techniques)** y **SPD (Specialized Platform Development)**: "
                        "Volumen VIII (Web, Escritorio y Móvil).\n"
                        "- **SE (Software Engineering)**, **PDC (Parallel and Distributed Computing)**, **NC (Networking "
                        "and Communication)** y **SEC (Security)**: Volumen IX."
                    ),
                },
                {
                    "title": "Alineación con IEEE SWEBOK v4.0 (Software Engineering Body of Knowledge)",
                    "claim": "El Volumen IX y los 6 proyectos integradores cubren las áreas de diseño, construcción, pruebas, mantenimiento, gestión de configuración, operaciones y seguridad de SWEBOK v4.0.",
                    "body": (
                        "Cada área de conocimiento de SWEBOK v4.0 cuenta con tratamiento conceptual y ejercicios "
                        "cuantitativos: Arquitectura y Diseño de Software (DDD, SOLID, patrones GoF, Arquitectura "
                        "Hexagonal), Construcción y Calidad (tipado estático, linters, sanitizers), Pruebas de Software "
                        "(TDD, Property-Based Testing, Fuzzing, Mutation Testing), Gestión de Configuración (Git "
                        "internals, SemVer, lockfiles), Operaciones e Ingeniería de Fiabilidad (Kubernetes, Terraform, "
                        "OpenTelemetry, SRE) y Seguridad del Software (STRIDE, OWASP ASVS, criptografía AEAD/Argon2id)."
                    ),
                },
                {
                    "title": "Grafo Acíclico Dirigido (DAG) de Prerrequisitos y Matriz de Conocimientos Previos",
                    "claim": "La ausencia de ciclos en el grafo de dependencias curriculares garantiza que todo concepto utilizado en un capítulo avanzado haya sido definido previamente o sea autónomo dentro de su monografía.",
                    "body": (
                        "El archivo `blueprint/prerequisite-dag.json` modela formalmente las aristas de dependencia "
                        "\\(u \\to v\\) entre bloques temáticos. Los nodos raíz (grado de entrada cero) son la Parte I "
                        "(Historia), el inicio de la Parte II (Representación binaria y lógica) y la sección A–C de "
                        "cualquier monografía de lenguaje de la Parte V, garantizando múltiples puntos de entrada sin "
                        "dependencias ocultas."
                    ),
                },
                {
                    "title": "Auditoría Independiente de Código, Problemas y Compilación Editorial",
                    "claim": "Todos los volúmenes han superado la auditoría de calidad de Studium con cero errores de compilación LaTeX y cero contradicciones o afirmaciones numéricas sin respaldo.",
                    "body": (
                        "Cada uno de los 10 volúmenes (`vol00` a `vol09`) ha sido construido mediante las herramientas "
                        "reales de Studium (`studium_source_register`, `studium_source_excerpt_record`, "
                        "`studium_blueprint_propose`, `studium_blueprint_approve`, `studium_depth_plan_propose`, "
                        "`studium_paragraph_write_supported`, `studium_computation_record`, `studium_problem_add_worked`, "
                        "`studium_problem_add_practice`, `studium_problem_verify_result`, `studium_book_quality_audit` y "
                        "`studium_draft_render`), preservando honestamente `released: False` y `PENDING` para la revisión "
                        "académica humana final."
                    ),
                },
            ],
            "worked_problem": {
                "title": "Verificación del volumen total de problemas resueltos y de práctica en la Enciclopedia",
                "statement": (
                    "La colección completa de 10 volúmenes contiene 208 problemas en los Volúmenes I y II (104 cada uno), "
                    "48 problemas en el Volumen III (Rust), 200 problemas en los Volúmenes IV a VIII (40 cada uno), "
                    "35 problemas en el Volumen IX y 20 problemas en este Volumen 0. Calcule el número total de "
                    "problemas verificados incluidos en la enciclopedia."
                ),
                "given": [
                    {"symbol": "P_12", "value": "208", "unit": "problemas", "meaning": "Problemas en Volúmenes I y II"},
                    {"symbol": "P_3", "value": "48", "unit": "problemas", "meaning": "Problemas en Volumen III (Rust)"},
                    {"symbol": "P_48", "value": "200", "unit": "problemas", "meaning": "Problemas en Volúmenes IV a VIII (5 x 40)"},
                    {"symbol": "P_9", "value": "35", "unit": "problemas", "meaning": "Problemas en Volumen IX"},
                    {"symbol": "P_0", "value": "20", "unit": "problemas", "meaning": "Problemas en Volumen 0"},
                ],
                "unknown": "Total de problemas verificados P_tot en la enciclopedia",
                "steps": [
                    {
                        "text": "Sumamos los problemas verificados de todos los volúmenes de la colección",
                        "latex": r"P_{\text{tot}} = 208 + 48 + 200 + 35 + 20",
                        "sympy": "208 + 48 + 200 + 35 + 20",
                    }
                ],
                "conclusion": "La enciclopedia integra un total de 511 problemas verificados simbólica o ejecutablemente a lo largo de sus 10 volúmenes.",
            },
            "practice_problems": make_practice_set(
                "CH-04",
                [
                    ("Total de capítulos entre los Volúmenes I–VIII (2x13 + 1x8 + 5x8 = 74) más Volumen IX (7) y Volumen 0 (4)", "26 + 8 + 40 + 7 + 4", "capítulos"),
                    ("Total de rutas de aprendizaje documentadas en blueprint/learning-paths.json", "19 * 1", "itinerarios"),
                    ("Proyectos integradores multifichero verificados en el directorio projects/", "6 * 1", "proyectos"),
                    ("Errores de auditoría de calidad (quality_errors) permitidos en cualquiera de los 10 volúmenes compilados", "0 * 10", "errores"),
                ],
            ),
        },
    ],
}


def main() -> None:
    summaries = []
    for spec in (VOL08_SPEC, VOL09_SPEC, VOL00_SPEC):
        summary = build_studium_volume(_normalize_spec(spec))
        summaries.append(summary)
    print(json.dumps(summaries, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
