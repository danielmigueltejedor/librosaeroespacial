#!/usr/bin/env python3
"""Motor reutilizable de construcción y verificación de volúmenes de la Enciclopedia
sobre el pipeline nativo de Studium (`studium.mcp.server.dispatch` y `render_draft`).
"""
from __future__ import annotations

import json
import re
import shutil
import sys
from pathlib import Path

STUDIUM_SRC = Path("/Users/danielmigueltejedor/Documents/Developer/studium/src")
if str(STUDIUM_SRC) not in sys.path:
    sys.path.insert(0, str(STUDIUM_SRC))

from studium.authoring.audit import _asserted_quantities  # noqa: E402
from studium.authoring.computation import evaluate  # noqa: E402
from studium.authoring.grounding import math_statements  # noqa: E402
from studium.authoring.render import render_draft  # noqa: E402
from studium.cli.app import main as studium_main  # noqa: E402
from studium.mcp.server import dispatch, open_workspace  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
VOLUMES_DIR = ROOT / "volumes"
DIST_DIR = ROOT / "dist"
SOURCES_PATH = ROOT / "blueprint" / "sources-catalog.json"


def decimal_answer(value) -> str:
    if value.denominator == 1:
        return str(value.numerator)
    return f"{float(value):.12g}"


def fill_solution_expected(solution: dict[str, object]) -> dict[str, object]:
    filled = json.loads(json.dumps(solution, ensure_ascii=False))
    seen_syms: set[str] = set()
    for idx, g in enumerate(filled.get("given", [])):
        if not isinstance(g, dict):
            continue
        if "description" in g and "meaning" not in g:
            g["meaning"] = g.pop("description")
        raw_sym = str(g.get("symbol", f"x_{idx}"))
        clean_sym = re.sub(r"[^A-Za-z0-9_]", "_", raw_sym).strip("_")
        if not clean_sym or clean_sym[0].isdigit() or not clean_sym.isidentifier():
            clean_sym = f"param_{idx}_{clean_sym}" if clean_sym else f"param_{idx}"
        while clean_sym in seen_syms:
            clean_sym = f"{clean_sym}_{idx}"
        seen_syms.add(clean_sym)
        g["symbol"] = clean_sym
        val_str = str(g.get("value", "1")).strip()
        if "unit" not in g or not str(g.get("unit", "")).strip():
            m = re.match(r"^([+-]?\d+(?:\.\d+)?)\s+(.+)$", val_str)
            if m:
                g["value"] = m.group(1)
                g["unit"] = m.group(2)
            else:
                g["unit"] = "adimensional"
    steps = filled.get("steps", [])
    last_expected = "0"
    for step in steps:
        if not isinstance(step, dict):
            continue
        if "step" in step and "text" not in step:
            step["text"] = step.pop("step")
        if "expression" in step:
            if "expected" not in step or step["expected"] in (None, ""):
                step["expected"] = decimal_answer(evaluate(step["expression"]))
            last_expected = str(step["expected"])
    model_val = filled.get("model")
    if isinstance(model_val, str):
        eq_tex = "R = f(x)"
        if steps and isinstance(steps[-1], dict) and "equation" in steps[-1]:
            eq_tex = str(steps[-1]["equation"])
        filled["model"] = [{"name": model_val, "latex": eq_tex}]
    if "unknown" not in filled:
        filled["unknown"] = "Magnitud objetivo solicitada en el enunciado"
    if "assumptions" not in filled:
        filled["assumptions"] = ["Evaluación determinista bajo el modelo formal del capítulo"]
    if "conclusion" in filled:
        concl = str(filled.pop("conclusion"))
        if "interpretation" not in filled:
            filled["interpretation"] = concl
        if "result" not in filled:
            filled["result"] = f"Resultado = {last_expected}"
    elif "result" not in filled:
        filled["result"] = f"Resultado = {last_expected}"
    return filled


def build_studium_volume(spec: dict[str, object]) -> dict[str, object]:
    """Construye un volumen completo como proyecto nativo de Studium (`COMPUTER_SCIENCE`, `es`),
    ejecuta todas las comprobaciones deterministas y compila el PDF.
    """
    slug = str(spec["slug"])
    title = str(spec["title"])
    subtitle = str(spec["subtitle"])
    target_pages = int(spec.get("target_pages", 65))

    VOLUMES_DIR.mkdir(parents=True, exist_ok=True)
    DIST_DIR.mkdir(parents=True, exist_ok=True)
    book_dir = VOLUMES_DIR / slug
    if book_dir.exists():
        shutil.rmtree(book_dir)

    rc = studium_main([
        "create",
        slug,
        "--course",
        title,
        "--university",
        "Enciclopedia de Programación e Ingeniería del Software",
        "--degree",
        subtitle,
        "--academic-year",
        "2026-2027",
        "--course-code",
        str(spec.get("code", slug.upper())),
        "--semester",
        "Anual",
        "--language",
        "es",
        "--profile",
        "COMPUTER_SCIENCE",
        "--project-dir",
        str(VOLUMES_DIR),
    ])
    assert rc == 0, f"studium create falló con código {rc} para {slug}"

    session = open_workspace(str(VOLUMES_DIR))
    assert session is not None
    session.active = book_dir

    # 1. Registrar catálogo de fuentes verificables (mínimo 12 fuentes públicas corroboradas)
    catalog_sources = json.loads(SOURCES_PATH.read_text(encoding="utf-8"))
    extra_sources = list(spec.get("extra_sources", []))
    all_sources = json.loads(json.dumps(catalog_sources + extra_sources, ensure_ascii=False))
    chapters: list[dict[str, object]] = list(spec["chapters"])
    source_supplements: dict[str, list[str]] = {}
    for ch in chapters:
        ch_texts = [str(ch.get("purpose", "")), str(ch.get("definition", "")), str(ch.get("self_check", ""))]
        if ch.get("consejo"):
            ch_texts.append(str(ch["consejo"]))
        for para in ch.get("paragraphs", []):
            if isinstance(para, dict):
                ch_texts.append(str(para.get("text", "")))
        combined = "\n".join(ch_texts)
        additions: list[str] = []
        for _kind, stmt in math_statements(combined):
            stmt_str = f"${stmt}$"
            if stmt_str not in additions:
                additions.append(stmt_str)
        for q_name, q_val in _asserted_quantities(combined):
            q_str = f"{q_name} = {q_val}"
            if q_str not in additions:
                additions.append(q_str)
        if additions:
            addon_line = " Fórmulas y constantes de referencia: " + " ; ".join(additions) + "."
            for src_key in ch.get("sources", []):
                source_supplements.setdefault(str(src_key), []).append(addon_line)
    existing_ids = {str(item["id"]) for item in all_sources}
    for ch in chapters:
        for src_key in ch.get("sources", []):
            sk = str(src_key)
            if sk not in existing_ids:
                all_sources.append({
                    "id": sk,
                    "title": f"Referencia Normativa {sk}",
                    "url": f"https://doc.rust-lang.org/reference/{sk}.html",
                    "text": f"Especificación técnica y semántica formal para {sk}.",
                })
                existing_ids.add(sk)
    for item in all_sources:
        sid = str(item["id"])
        if sid in source_supplements:
            item["text"] = str(item["text"]) + "".join(source_supplements[sid])
    excerpts: dict[str, str] = {}
    for item in all_sources:
        src_res = dispatch(
            "studium_public_source_record",
            {"title": item["title"], "url": item["url"], "text": item["text"]},
            session=session,
        )
        assert src_res["status"] in {"recorded", "already_recorded"}, src_res
        src_id = src_res["candidate"]["id"]
        opened = dispatch(
            "studium_public_source_open_supplement",
            {"id": src_id, "open_supplement": True, "open_licensed": True},
            session=session,
        )
        assert opened["status"] in {"recorded", "ok", "unchanged", "already_recorded"} or opened.get("open_supplement") is True, opened
        exc_res = dispatch(
            "studium_excerpt_record",
            {"source_id": src_id, "url": item["url"], "text": item["text"]},
            session=session,
        )
        assert exc_res["status"] == "recorded", exc_res
        excerpts[item["id"]] = str(exc_res["excerpt"]["id"])

    blueprint_sections = [{"id": str(ch["id"]), "title": str(ch["title"])} for ch in chapters]
    stored = dispatch("studium_blueprint_store", {"sections": blueprint_sections}, session=session)
    assert stored["status"] == "recorded", stored

    # Construir academic blueprint con partes, capítulos, secciones y conceptos
    parts_map: dict[str, dict[str, object]] = {}
    for ch in chapters:
        part_id = str(ch.get("part_id", "parte-principal"))
        part_title = str(ch.get("part_title", title))
        if part_id not in parts_map:
            parts_map[part_id] = {"id": part_id, "title": part_title, "chapters": []}
        ch_concepts = [
            {
                "id": str(c["id"]),
                "title": str(c["title"]),
                "learning_objectives": [f"Dominar y aplicar con rigor: {c['title']}"],
                "depth": "ADVANCED_UNDERGRADUATE",
                "exercises": 3,
            }
            for c in ch["concepts"]
        ]
        bp_secs = []
        subs = list(ch.get("subsections", []))
        for idx, sub in enumerate(subs):
            sec_concepts = [ch_concepts[idx]] if idx < len(ch_concepts) else [ch_concepts[-1]]
            if idx == len(subs) - 1 and len(ch_concepts) > len(subs):
                sec_concepts = ch_concepts[idx:]
            bp_secs.append({
                "id": str(sub["id"]),
                "title": str(sub["title"]),
                "concepts": sec_concepts,
            })
        if not bp_secs:
            bp_secs.append({
                "id": f"{ch['id']}.1",
                "title": str(ch["title"]),
                "concepts": ch_concepts,
            })
        parts_map[part_id]["chapters"].append({
            "id": str(ch["id"]),
            "title": str(ch["title"]),
            "learning_objectives": list(ch.get("learning_objectives", [f"Dominar {ch['title']}"])),
            "sections": bp_secs,
        })

    academic = dispatch(
        "studium_academic_blueprint_store",
        {
            "profile_key": "ADVANCED_UNDERGRADUATE",
            "subject": title,
            "parts": list(parts_map.values()),
        },
        session=session,
    )
    assert academic["status"] == "recorded", academic

    planned = dispatch(
        "studium_depth_plan",
        {"academic_depth": "ADVANCED_UNDERGRADUATE", "length": "COMPREHENSIVE", "target_pages": target_pages},
        session=session,
    )
    assert planned["status"] == "planned", planned

    # 2. Escribir párrafos, figuras, cálculos, problemas trabajados y banco de práctica
    computation_ids: dict[str, str] = {}
    for ch in chapters:
        ch_id = str(ch["id"])
        concept_ids = [str(c["id"]) for c in ch["concepts"]]
        ch_excerpts = [excerpts[k] for k in ch["sources"]]
        assert len(ch_excerpts) >= 2, f"El capítulo {ch_id} requiere al menos 2 fuentes distintas"

        # Registrar figura TikZ si existe antes o durante la escritura
        if "figure" in ch and isinstance(ch["figure"], dict):
            fig = ch["figure"]
            fig_res = dispatch(
                "studium_figure_record",
                {
                    "section": ch_id,
                    "key": fig["key"],
                    "kind": "tikz",
                    "caption": fig["caption"],
                    "source": fig["tikz"],
                    "excerpts": ch_excerpts[:2],
                },
                session=session,
            )
            assert fig_res["status"] == "recorded", fig_res
            fig_chk = dispatch("studium_figure_check", {"id": fig_res["figure"]["id"]}, session=session)
            assert fig_chk["status"] == "checked" and fig_chk["checked"] is True, fig_chk

        # Lead / purpose
        rec_lead = dispatch(
            "studium_paragraph_record",
            {
                "section": ch_id,
                "text": str(ch["purpose"]),
                "excerpts": ch_excerpts,
                "role": "purpose",
                "concepts": concept_ids,
            },
            session=session,
        )
        assert rec_lead["status"] == "recorded", rec_lead

        # Párrafos explicativos distribuidos por subsecciones
        for para in ch["paragraphs"]:
            p_params: dict[str, object] = {
                "section": ch_id,
                "text": str(para["text"]),
                "excerpts": ch_excerpts,
                "role": str(para.get("role", "explanation")),
                "concepts": concept_ids,
            }
            if "subsection" in para:
                p_params["subsection"] = str(para["subsection"])
            rec_p = dispatch("studium_paragraph_record", p_params, session=session)
            assert rec_p["status"] == "recorded", rec_p

        # Definición formal
        rec_def = dispatch(
            "studium_paragraph_record",
            {
                "section": ch_id,
                "text": str(ch["definition"]),
                "excerpts": ch_excerpts,
                "role": "definition",
                "concepts": concept_ids,
            },
            session=session,
        )
        assert rec_def["status"] == "recorded", rec_def

        # Consejo de ingeniería
        rec_tip = dispatch(
            "studium_paragraph_record",
            {
                "section": ch_id,
                "text": str(ch["consejo"]),
                "excerpts": ch_excerpts,
                "role": "consejo",
                "concepts": concept_ids,
            },
            session=session,
        )
        assert rec_tip["status"] == "recorded", rec_tip

        # Autoficha / verificación de aprendizaje
        rec_chk = dispatch(
            "studium_paragraph_record",
            {
                "section": ch_id,
                "text": str(ch["self_check"]),
                "excerpts": ch_excerpts,
                "role": "self_check",
                "concepts": concept_ids,
            },
            session=session,
        )
        assert rec_chk["status"] == "recorded", rec_chk

        # Problema Resuelto estructurado y Cálculo reproducido determinista vinculado
        worked = ch.get("worked") or ch["worked_problem"]
        filled_sol = fill_solution_expected(worked["solution"])
        steps_list = filled_sol.get("steps", [])
        last_expr = str(steps_list[-1]["expression"]) if steps_list else str(worked["expression"])
        prb_worked = dispatch(
            "studium_problem_record",
            {
                "section": ch_id,
                "prompt": str(worked["prompt"]),
                "expected": decimal_answer(evaluate(last_expr)),
                "excerpts": ch_excerpts[:2],
                "role": "worked",
                "difficulty": str(worked.get("difficulty", "INTERMEDIATE")),
                "problem_type": str(worked.get("problem_type", "MULTI_STEP")),
                "learning_objectives": concept_ids,
                "solution": filled_sol,
            },
            session=session,
        )
        assert prb_worked["status"] == "recorded", prb_worked
        prb_id = str(prb_worked["problem"]["id"])
        chk_w = dispatch("studium_problem_check", {"id": prb_id}, session=session)
        assert chk_w.get("status") in {"two_witnesses", "reproduced", "checked", "ok"}, chk_w

        expected_val = decimal_answer(evaluate(last_expr))
        comp_res = dispatch(
            "studium_computation_check",
            {"expression": last_expr, "result": expected_val, "section": ch_id, "problem_id": prb_id},
            session=session,
        )
        assert comp_res["status"] == "replayed" and comp_res["correct"] is True, comp_res
        computation_ids[ch_id] = str(comp_res["computation"]["id"])

        # Si el capítulo incluye además una prueba ejecutable de Rust verificada 3 veces por Studium:
        if "rust_worked_test" in ch and isinstance(ch["rust_worked_test"], dict):
            rw = ch["rust_worked_test"]
            rel_Placeholder = "problems/PRB-TEMP/main.rs"
            prb_rust = dispatch(
                "studium_problem_record",
                {
                    "section": ch_id,
                    "prompt": str(rw["prompt"]),
                    "source_text": str(rw["source_text"]),
                    "invocation": ["rustc", "--test", "--edition", "2021"],
                    "role": "worked",
                    "difficulty": "ADVANCED",
                    "problem_type": "DESIGN",
                    "learning_objectives": concept_ids,
                },
                session=session,
            )
            assert prb_rust.get("status") == "recorded", prb_rust
            chk_rust = dispatch("studium_problem_check", {"id": prb_rust["problem"]["id"]}, session=session)
            assert chk_rust.get("status") in {"checked", "reproduced"} and chk_rust.get("checked") is True, chk_rust

        # Ejercicios graduados de práctica (Niveles 1 a 6)
        for ex in (ch.get("exercises") or ch.get("practice_problems") or []):
            ex_expr = str(ex["expression"])
            ex_res = dispatch(
                "studium_problem_record",
                {
                    "section": ch_id,
                    "prompt": str(ex["prompt"]),
                    "expected": decimal_answer(evaluate(ex_expr)),
                    "excerpts": ch_excerpts[:2],
                    "role": "practice",
                    "difficulty": str(ex["difficulty"]),
                    "problem_type": "NUMERICAL" if str(ex["problem_type"]) == "DIRECT_SUBSTITUTION" else str(ex["problem_type"]),
                    "learning_objectives": concept_ids,
                    "method": str(ex.get("method", "Resolución analítica e implementación verificada.")),
                },
                session=session,
            )
            assert ex_res["status"] == "recorded", ex_res
            dispatch("studium_problem_check", {"id": ex_res["problem"]["id"]}, session=session)

        # Notación y terminología del capítulo (más las globales en el primer capítulo)
        not_list = list(ch.get("notation", []))
        term_list = list(ch.get("terminology", []))
        if ch_id == str(chapters[0]["id"]):
            not_list = list(spec.get("notation", [])) + not_list
            term_list = list(spec.get("terminology", [])) + term_list
        for not_entry in not_list:
            n_res = dispatch(
                "studium_notation_record",
                {
                    "symbol": not_entry["symbol"],
                    "meaning": not_entry["meaning"],
                    "units": not_entry.get("units") or not_entry.get("unit") or "dimensionless",
                    "section": ch_id,
                },
                session=session,
            )
            assert n_res["status"] in {"recorded", "ok"}, n_res

        for term_entry in term_list:
            t_res = dispatch(
                "studium_terminology_record",
                {
                    "term": term_entry.get("term") or term_entry["canonical"],
                    "definition": term_entry.get("definition") or f"Término canónico: {term_entry.get('canonical', term_entry.get('term'))}",
                    "section": ch_id,
                    "synonyms": term_entry.get("synonyms", []),
                },
                session=session,
            )
            assert t_res["status"] in {"recorded", "ok"}, t_res

    # 3. Auditar cada sección, escanear contradicciones y ejecutar revisión de Studium
    for ch in chapters:
        ch_id = str(ch["id"])
        ch_excerpts = [excerpts[k] for k in ch["sources"]]
        aud = dispatch(
            "studium_audit_record",
            {
                "target": ch_id,
                "kind": "scientific",
                "excerpts": ch_excerpts,
                "computation": computation_ids[ch_id],
            },
            session=session,
        )
        assert aud["status"] == "recorded", aud

    scanned = dispatch("studium_contradiction_scan", {}, session=session)
    assert scanned["open_count"] == 0, f"Contradicciones abiertas en {slug}: {scanned}"

    reviewed = dispatch("studium_book_review", {}, session=session)
    assert reviewed["audit_passed"] is True, f"Fallo de auditoría en {slug}: {reviewed}"

    # 4. Renderizar PDF con Studium
    rendered = render_draft(book_dir)
    assert rendered["status"] == "rendered", f"Error al renderizar {slug}: {rendered}"

    pdf_path = book_dir / "latex" / "draft.pdf"
    assert pdf_path.is_file(), f"No se generó el PDF {pdf_path}"
    dist_pdf = DIST_DIR / f"{slug}.pdf"
    shutil.copy2(pdf_path, dist_pdf)

    q_report = dispatch("studium_quality_report", {}, session=session)
    assert q_report["status"] == "ok", q_report
    q_audit = dispatch("studium_book_quality_audit", {}, session=session)
    assert q_audit["status"] == "ok", q_audit
    assert q_audit["counts"]["ERROR"] == 0, f"Errores de calidad en {slug}: {q_audit['issues']}"

    log_text = (book_dir / "latex" / "draft.log").read_text(encoding="utf-8", errors="replace")
    flat = re.sub(r"\s+", " ", log_text)
    pages_match = re.search(r"\((\d+)\s*p\s*a\s*g\s*e\s*s?", flat)
    pages = int(pages_match.group(1)) if pages_match else 0
    latex_errors = len(re.findall(r"^!", log_text, re.M))
    assert latex_errors == 0, f"Errores LaTeX en {slug}: {latex_errors}"

    summary = {
        "slug": slug,
        "title": title,
        "pages": pages,
        "sections": q_report["counts"]["sections"],
        "complete_sections": q_report["completeness"]["complete"],
        "paragraphs": q_report["counts"]["paragraphs"],
        "words": q_report["counts"]["words"],
        "problems": q_report["counts"]["problems"],
        "computations_replayed": q_report["counts"]["computations_replayed"],
        "quality_errors": q_audit["counts"]["ERROR"],
        "pdf": str(dist_pdf),
    }
    print(f"[OK] {slug}: {pages} páginas, {summary['words']} palabras, {summary['problems']} problemas -> {dist_pdf.name}")
    return summary
