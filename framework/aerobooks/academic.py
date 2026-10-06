from __future__ import annotations

import argparse
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable

from .cli import FRAMEWORK_VERSION, book_dir, framework_dir, load_book, repo_root


ACADEMIC_TOOL_VERSION = "0.2.0"

REVIEW_PROMPTS = {
    "source": "SOURCE_AUDITOR.md",
    "outline": "OUTLINE_ARCHITECT.md",
    "author": "MASTER_AUTHOR.md",
    "exact": "EXACT_REPRODUCER.md",
    "scientific": "SCIENTIFIC_REVIEWER.md",
    "mathematical": "MATHEMATICAL_REVIEWER.md",
    "historical": "HISTORICAL_REVIEWER.md",
    "citation": "CITATION_AUDITOR.md",
    "latex": "LATEX_EDITOR.md",
    "release": "RELEASE_REVIEWER.md",
    "red-team": "RED_TEAM_REVIEWER.md",
    "derivation": "DERIVATION_AUDITOR.md",
    "exercise": "EXERCISE_AUTHOR.md",
    "exercise-review": "EXERCISE_REVIEWER.md",
    "figure": "FIGURE_REVIEWER.md",
    "pedagogy": "PEDAGOGICAL_REVIEWER.md",
    "copyright": "COPYRIGHT_REVIEWER.md",
    "units": "UNIT_DIMENSION_REVIEWER.md",
    "conflict": "CONFLICT_RESOLVER.md",
    "blueprint": "BOOK_BLUEPRINT_ARCHITECT.md",
    "claim": "CLAIM_EXTRACTOR.md",
    "evidence": "EVIDENCE_MAPPER.md",
    "agent": "AEROBOOKS_AGENT.md",
}

DEFAULT_REQUIRED_REVIEWS = [
    "source",
    "scientific",
    "citation",
    "latex",
    "pedagogy",
    "copyright",
    "red-team",
    "release",
]

SOURCE_STATUSES = {"verified", "provided", "pending", "rejected"}
CLAIM_STATUSES = {"verified", "derived", "pending", "rejected"}
EVIDENCE_SUPPORT = {
    "direct",
    "derived",
    "corroborates",
    "contradicts",
    "contextual",
    "exam_pattern",
}
EVIDENCE_STATUS = {"verified", "pending", "rejected"}
CHAPTER_STATUS = {"planned", "draft", "review", "ready"}
REVIEW_STATUS = {"pending", "pass", "pass_with_changes", "fail"}


def _load_json(path: Path, default):
    if not path.exists():
        return default
    return json.loads(path.read_text(encoding="utf-8"))


def _read_jsonl(path: Path) -> list[dict]:
    if not path.exists():
        return []
    out: list[dict] = []
    for lineno, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        try:
            item = json.loads(line)
        except json.JSONDecodeError as exc:
            raise SystemExit(f"{path}:{lineno}: JSON inválido: {exc}") from exc
        if not isinstance(item, dict):
            raise SystemExit(f"{path}:{lineno}: cada entrada debe ser un objeto JSON.")
        out.append(item)
    return out


def _append_jsonl(path: Path, item: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(item, ensure_ascii=False, sort_keys=False) + "\n")


def _write_json(path: Path, data: dict | list) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(data, ensure_ascii=False, indent=2, sort_keys=False) + "\n",
        encoding="utf-8",
    )


def _manifest(root: Path) -> dict:
    return _load_json(
        root / "sources" / "manifest.json",
        {"schema_version": 1, "book": root.name, "sources": []},
    )


def _source_map(root: Path) -> dict[str, dict]:
    return {
        item.get("id"): item
        for item in _manifest(root).get("sources", [])
        if item.get("id")
    }


def _claim_map(root: Path) -> dict[str, dict]:
    return {
        item.get("id"): item
        for item in _read_jsonl(root / "claims" / "ledger.jsonl")
        if item.get("id")
    }


def _evidence_entries(root: Path) -> list[dict]:
    return _read_jsonl(root / "evidence" / "map.jsonl")


def _chapter_specs(root: Path) -> list[dict]:
    directory = root / "specs"
    if not directory.exists():
        return []
    specs = []
    for path in sorted(directory.glob("*.json")):
        try:
            item = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            raise SystemExit(f"{path}: JSON inválido: {exc}") from exc
        item["_file"] = str(path.relative_to(root))
        specs.append(item)
    return specs


def _conflicts(root: Path) -> list[dict]:
    return _read_jsonl(root / "sources" / "conflicts.jsonl")


def _reviews(root: Path) -> list[dict]:
    directory = root / "reviews"
    if not directory.exists():
        return []
    reports = []
    for path in sorted(directory.glob("*.json")):
        try:
            item = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            raise SystemExit(f"{path}: JSON inválido: {exc}") from exc
        item["_file"] = str(path.relative_to(root))
        reports.append(item)
    return reports


def _ensure_scaffold(root: Path) -> None:
    directories = [
        root / "specs",
        root / "evidence",
        root / "reviews",
        root / "release",
        root / "build" / "ai",
    ]
    for directory in directories:
        directory.mkdir(parents=True, exist_ok=True)

    evidence = root / "evidence" / "map.jsonl"
    if not evidence.exists():
        evidence.write_text("", encoding="utf-8")

    for directory, text in (
        (
            root / "specs",
            "# Chapter specs\n\nCada capítulo puede tener un contrato JSON validable por AeroBooks.\n",
        ),
        (
            root / "evidence",
            "# Evidence map\n\nEl mapa enlaza claims, fuentes, localizadores y capítulos.\n",
        ),
        (
            root / "release",
            "# Release provenance\n\nAquí se guardan manifests reproducibles de cada edición candidata.\n",
        ),
    ):
        readme = directory / "README.md"
        if not readme.exists():
            readme.write_text(text, encoding="utf-8")


def cmd_init(args: argparse.Namespace) -> int:
    root, _ = load_book(args.slug)
    _ensure_scaffold(root)
    print(f"✓ Capa académica inicializada en {root.relative_to(repo_root())}")
    return 0


def cmd_bootstrap(args: argparse.Namespace) -> int:
    root, config = load_book(args.slug)
    _ensure_scaffold(root)

    files = [
        repo_root() / "AGENTS.md",
        framework_dir() / "prompts" / "AEROBOOKS_AGENT.md",
        framework_dir() / "prompts" / "BOOK_BLUEPRINT_ARCHITECT.md",
        framework_dir() / "prompts" / "SOURCE_AUDITOR.md",
        framework_dir() / "prompts" / "OUTLINE_ARCHITECT.md",
        framework_dir() / "ai" / "BOOK_BLUEPRINT_PROTOCOL.md",
        framework_dir() / "ai" / "RESEARCH_PROTOCOL.md",
        framework_dir() / "ai" / "SOURCE_POLICY.md",
        framework_dir() / "ai" / "PROVENANCE_PROTOCOL.md",
        root / "ai" / "BRIEF.md",
        root / "sources" / "manifest.json",
        root / "sources" / "conflicts.jsonl",
    ]

    chunks = [
        f"# AeroBooks Bootstrap Pack — {config.get('book', {}).get('title', args.slug)}",
        "",
        "Este paquete sirve para iniciar o reconstruir un libro a partir de fuentes.",
        "No redactes capítulos todavía. Primero completa blueprint, source audit, conflictos y chapter specs.",
        "",
    ]
    for path in files:
        if path.exists():
            try:
                label = str(path.relative_to(repo_root()))
            except ValueError:
                label = path.name
            chunks += [
                f"## {label}",
                "",
                path.read_text(encoding="utf-8").rstrip(),
                "",
            ]

    chunks += [
        "## SALIDA OBLIGATORIA DE LA FASE DE BOOTSTRAP",
        "",
        "1. ai/BRIEF.md completo;",
        "2. sources/manifest.json auditado;",
        "3. sources/conflicts.jsonl actualizado;",
        "4. mapa de cobertura del temario;",
        "5. chapter specs para el contenido que se vaya a redactar;",
        "6. lista explícita de lagunas que NO deben rellenarse todavía;",
        "",
        "Después de eso puede comenzar la autoría por chapter-pack.",
        "",
    ]

    output = (
        Path(args.output)
        if args.output
        else root / "build" / "ai" / "BOOTSTRAP.md"
    )
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text("\n".join(chunks), encoding="utf-8")
    print(f"✓ Bootstrap pack: {output}")
    return 0


def cmd_chapter_spec(args: argparse.Namespace) -> int:
    root, _ = load_book(args.slug)
    _ensure_scaffold(root)

    sources = _source_map(root)
    claims = _claim_map(root)

    unknown_sources = [sid for sid in args.source if sid not in sources]
    unknown_claims = [cid for cid in args.claim if cid not in claims]
    if unknown_sources:
        raise SystemExit("Fuentes desconocidas: " + ", ".join(unknown_sources))
    if unknown_claims:
        raise SystemExit("Claims desconocidos: " + ", ".join(unknown_claims))

    manuscript = root / args.path
    if not manuscript.exists() and not args.allow_missing:
        raise SystemExit(
            f"No existe {manuscript}. Usa --allow-missing si el capítulo todavía está planificado."
        )

    item = {
        "schema_version": 1,
        "id": args.id,
        "title": args.title,
        "path": args.path,
        "status": args.status,
        "objectives": args.objective or [],
        "prerequisites": args.prerequisite or [],
        "sources": args.source or [],
        "claims": args.claim or [],
        "derivations": args.derivation or [],
        "figures": args.figure or [],
        "exercises": args.exercise or [],
        "historical_scope": bool(args.historical_scope),
        "notes": args.notes,
    }
    path = root / "specs" / f"{args.id}.json"
    if path.exists() and not args.force:
        raise SystemExit(f"Ya existe {path}. Usa --force para reemplazarlo.")
    _write_json(path, item)
    print(f"✓ Chapter spec: {path.relative_to(repo_root())}")
    return 0


def cmd_evidence_add(args: argparse.Namespace) -> int:
    root, _ = load_book(args.slug)
    _ensure_scaffold(root)

    sources = _source_map(root)
    claims = _claim_map(root)
    specs = {item.get("id"): item for item in _chapter_specs(root)}

    existing = _evidence_entries(root)
    if any(item.get("id") == args.id for item in existing):
        raise SystemExit(f"Ya existe una evidencia con id {args.id}")

    if args.chapter not in specs:
        raise SystemExit(f"Chapter spec desconocido: {args.chapter}")
    if args.claim and args.claim not in claims:
        raise SystemExit(f"Claim desconocido: {args.claim}")
    if args.source and args.source not in sources:
        raise SystemExit(f"Fuente desconocida: {args.source}")
    if args.support != "derived" and not args.source:
        raise SystemExit("La evidencia no derivada debe indicar --source.")
    if args.support == "derived" and not (args.derivation or args.notes):
        raise SystemExit("Una evidencia derivada debe documentar --derivation o --notes.")

    item = {
        "schema_version": 1,
        "id": args.id,
        "chapter": args.chapter,
        "claim": args.claim,
        "source": args.source,
        "locator": args.locator,
        "support": args.support,
        "status": args.status,
        "confidence": args.confidence,
        "derivation": args.derivation,
        "notes": args.notes,
    }
    _append_jsonl(root / "evidence" / "map.jsonl", item)
    print(f"✓ Evidencia añadida: {args.id}")
    return 0


def _coverage(root: Path) -> dict:
    sources = _source_map(root)
    claims = _claim_map(root)
    specs = _chapter_specs(root)
    evidence = _evidence_entries(root)
    conflicts = _conflicts(root)

    issues: list[dict] = []
    spec_ids = {s.get("id") for s in specs if s.get("id")}
    evidence_by_claim: dict[str, list[dict]] = {}
    evidence_by_chapter: dict[str, list[dict]] = {}

    for item in evidence:
        if item.get("claim"):
            evidence_by_claim.setdefault(item["claim"], []).append(item)
        if item.get("chapter"):
            evidence_by_chapter.setdefault(item["chapter"], []).append(item)

        if item.get("chapter") not in spec_ids:
            issues.append({
                "severity": "error",
                "code": "EVD001",
                "message": f"{item.get('id')}: chapter desconocido {item.get('chapter')}",
            })
        if item.get("claim") and item.get("claim") not in claims:
            issues.append({
                "severity": "error",
                "code": "EVD002",
                "message": f"{item.get('id')}: claim desconocido {item.get('claim')}",
            })
        if item.get("source") and item.get("source") not in sources:
            issues.append({
                "severity": "error",
                "code": "EVD003",
                "message": f"{item.get('id')}: source desconocida {item.get('source')}",
            })
        if item.get("support") not in EVIDENCE_SUPPORT:
            issues.append({
                "severity": "error",
                "code": "EVD004",
                "message": f"{item.get('id')}: support inválido {item.get('support')}",
            })
        if item.get("status") not in EVIDENCE_STATUS:
            issues.append({
                "severity": "error",
                "code": "EVD005",
                "message": f"{item.get('id')}: status inválido {item.get('status')}",
            })

    for spec in specs:
        sid = spec.get("id", "?")
        if spec.get("status") not in CHAPTER_STATUS:
            issues.append({
                "severity": "error",
                "code": "CHP001",
                "message": f"{sid}: status inválido {spec.get('status')}",
            })

        manuscript = root / str(spec.get("path", ""))
        if not manuscript.exists():
            issues.append({
                "severity": "warning",
                "code": "CHP002",
                "message": f"{sid}: manuscrito no existe: {spec.get('path')}",
            })

        for source_id in spec.get("sources", []):
            if source_id not in sources:
                issues.append({
                    "severity": "error",
                    "code": "CHP003",
                    "message": f"{sid}: fuente desconocida {source_id}",
                })

        for claim_id in spec.get("claims", []):
            if claim_id not in claims:
                issues.append({
                    "severity": "error",
                    "code": "CHP004",
                    "message": f"{sid}: claim desconocido {claim_id}",
                })

    for cid, claim in claims.items():
        if claim.get("risk") == "high" and claim.get("status") in {"verified", "derived"}:
            verified_evidence = [
                e for e in evidence_by_claim.get(cid, [])
                if e.get("status") == "verified"
            ]
            if not verified_evidence:
                issues.append({
                    "severity": "warning",
                    "code": "EVD006",
                    "message": f"{cid}: claim de alto riesgo sin entrada de evidencia verificada.",
                })

    unresolved_conflicts = [
        c for c in conflicts
        if c.get("status", "open") not in {"resolved", "accepted_difference", "closed"}
    ]
    for conflict in unresolved_conflicts:
        issues.append({
            "severity": "warning",
            "code": "CNF001",
            "message": f"Conflicto sin resolver: {conflict.get('id', '(sin id)')}",
        })

    source_usage = {sid: 0 for sid in sources}
    for spec in specs:
        for sid in spec.get("sources", []):
            if sid in source_usage:
                source_usage[sid] += 1
    for item in evidence:
        sid = item.get("source")
        if sid in source_usage:
            source_usage[sid] += 1

    unused_verified = [
        sid for sid, count in source_usage.items()
        if count == 0 and sources[sid].get("status") == "verified"
    ]

    return {
        "book": root.name,
        "chapters": len(specs),
        "sources": len(sources),
        "claims": len(claims),
        "evidence": len(evidence),
        "unresolved_conflicts": len(unresolved_conflicts),
        "unused_verified_sources": unused_verified,
        "issues": issues,
    }


def cmd_coverage(args: argparse.Namespace) -> int:
    root, _ = load_book(args.slug)
    report = _coverage(root)
    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        print(f"AeroBooks Academic Coverage — {args.slug}")
        print(f"  capítulos:  {report['chapters']}")
        print(f"  fuentes:    {report['sources']}")
        print(f"  claims:     {report['claims']}")
        print(f"  evidencias: {report['evidence']}")
        print(f"  conflictos abiertos: {report['unresolved_conflicts']}")
        for issue in report["issues"]:
            icon = "✗" if issue["severity"] == "error" else "!"
            print(f"{icon} {issue['code']}: {issue['message']}")
        if report["unused_verified_sources"]:
            print("· Fuentes verificadas aún no mapeadas: " + ", ".join(report["unused_verified_sources"]))

    errors = any(i["severity"] == "error" for i in report["issues"])
    warnings = any(i["severity"] == "warning" for i in report["issues"])
    return 1 if errors or (args.strict and warnings) else 0


def _prompt_for(role: str) -> str:
    name = REVIEW_PROMPTS.get(role)
    if not name:
        raise SystemExit(f"Rol desconocido '{role}'.")
    path = framework_dir() / "prompts" / name
    if not path.exists():
        raise SystemExit(f"No existe el prompt {path}.")
    return path.read_text(encoding="utf-8")


def _protocol_bundle() -> list[Path]:
    names = [
        "AI_AUTHORING_PROTOCOL.md",
        "AI_WORKFLOW.md",
        "AI_ORCHESTRATION.md",
        "BOOK_BLUEPRINT_PROTOCOL.md",
        "QUALITY_RUBRIC.md",
        "SOURCE_POLICY.md",
        "FACT_CHECK_PROTOCOL.md",
        "RESEARCH_PROTOCOL.md",
        "PROVENANCE_PROTOCOL.md",
        "DERIVATION_PROTOCOL.md",
        "EXERCISE_PROTOCOL.md",
        "FIGURE_PROTOCOL.md",
        "UNCERTAINTY_PROTOCOL.md",
        "RELEASE_GATE.md",
    ]
    return [framework_dir() / "ai" / name for name in names]


def cmd_chapter_pack(args: argparse.Namespace) -> int:
    root, config = load_book(args.slug)
    specs = {item.get("id"): item for item in _chapter_specs(root)}
    if args.chapter not in specs:
        raise SystemExit(
            f"No existe spec '{args.chapter}'. Crea uno con aerobooks-ai chapter-spec."
        )
    spec = specs[args.chapter]

    sources = _source_map(root)
    claims = _claim_map(root)
    evidence = _evidence_entries(root)

    selected_sources = {
        sid: sources[sid]
        for sid in spec.get("sources", [])
        if sid in sources
    }
    selected_claims = {
        cid: claims[cid]
        for cid in spec.get("claims", [])
        if cid in claims
    }
    selected_evidence = [
        item for item in evidence if item.get("chapter") == args.chapter
    ]

    manuscript_path = root / spec.get("path", "")
    manuscript = manuscript_path.read_text(encoding="utf-8") if manuscript_path.exists() else ""

    chunks = [
        f"# AeroBooks Chapter Pack — {args.chapter}",
        "",
        f"Libro: {config.get('book', {}).get('title', args.slug)}",
        f"Rol: {args.role}",
        "",
        "## REGLA DE EJECUCIÓN",
        "",
        "Trabaja únicamente dentro del alcance de este chapter spec. "
        "No rellenes lagunas con conocimiento implícito. "
        "Si necesitas una fuente nueva y el modo de investigación lo permite, "
        "regístrala antes de usarla.",
        "",
        "## ROL",
        "",
        _prompt_for(args.role).rstrip(),
        "",
    ]

    agents = repo_root() / "AGENTS.md"
    if agents.exists():
        chunks += ["## CONTRATO GLOBAL", "", agents.read_text(encoding="utf-8").rstrip(), ""]

    for path in _protocol_bundle():
        if path.exists():
            chunks += [f"## {path.name}", "", path.read_text(encoding="utf-8").rstrip(), ""]

    chunks += [
        "## BOOK.TOML",
        "",
        (root / "book.toml").read_text(encoding="utf-8").rstrip(),
        "",
        "## CHAPTER SPEC",
        "",
        json.dumps(spec, ensure_ascii=False, indent=2),
        "",
        "## FUENTES AUTORIZADAS PARA ESTE CAPÍTULO",
        "",
        json.dumps(selected_sources, ensure_ascii=False, indent=2),
        "",
        "## CLAIMS DEL CAPÍTULO",
        "",
        json.dumps(selected_claims, ensure_ascii=False, indent=2),
        "",
        "## EVIDENCE MAP DEL CAPÍTULO",
        "",
        json.dumps(selected_evidence, ensure_ascii=False, indent=2),
        "",
        "## MANUSCRITO ACTUAL",
        "",
        manuscript.rstrip() if manuscript else "(todavía no existe)",
        "",
        "## CONTRATO DE CIERRE",
        "",
        "Antes de terminar: enumera cambios, claims afectados, nuevas fuentes, "
        "conflictos, comprobaciones independientes y cualquier incertidumbre pendiente. "
        "No declares PASS sobre tu propio trabajo.",
        "",
    ]

    output = (
        Path(args.output)
        if args.output
        else root / "build" / "ai" / f"{args.chapter}-{args.role}.md"
    )
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text("\n".join(chunks), encoding="utf-8")
    print(f"✓ Chapter pack: {output}")
    return 0


def cmd_review_template(args: argparse.Namespace) -> int:
    root, _ = load_book(args.slug)
    _ensure_scaffold(root)
    if args.role not in REVIEW_PROMPTS:
        raise SystemExit(f"Rol desconocido: {args.role}")

    path = root / "reviews" / f"{args.id}.json"
    if path.exists() and not args.force:
        raise SystemExit(f"Ya existe {path}. Usa --force para reemplazar.")

    report = {
        "schema_version": 1,
        "review_id": args.id,
        "review_type": args.role,
        "book": args.slug,
        "scope": args.scope,
        "status": "pending",
        "reviewer": args.reviewer,
        "independence": args.independence,
        "checked": [],
        "findings": [],
        "claims_checked": [],
        "sources_consulted": [],
        "tests_reperformed": [],
        "residual_uncertainty": [],
    }
    _write_json(path, report)
    print(f"✓ Review template: {path.relative_to(repo_root())}")
    return 0


def _required_reviews(root: Path, config: dict, claims: dict[str, dict]) -> list[str]:
    academic = config.get("academic", {})
    required = list(
        dict.fromkeys(academic.get("required_reviews") or DEFAULT_REQUIRED_REVIEWS)
    )
    specs = _chapter_specs(root)

    def ensure(role: str) -> None:
        if role not in required:
            required.append(role)

    has_math = any(
        item.get("type") in {"mathematical", "numerical", "derived_result"}
        and item.get("status") != "rejected"
        for item in claims.values()
    )
    has_science_numbers = any(
        item.get("type") in {"scientific", "mathematical", "numerical", "derived_result"}
        and item.get("status") != "rejected"
        for item in claims.values()
    )
    has_history = any(
        item.get("type") in {"historical", "biographical"}
        and item.get("status") != "rejected"
        for item in claims.values()
    ) or any(spec.get("historical_scope") for spec in specs)
    has_derivations = any(spec.get("derivations") for spec in specs)
    has_figures = any(spec.get("figures") for spec in specs)
    has_exercises = any(spec.get("exercises") for spec in specs)

    if has_math or has_derivations:
        ensure("mathematical")
    if has_science_numbers or has_derivations:
        ensure("units")
    if academic.get("require_historical_when_claims", True) and has_history:
        ensure("historical")
    if has_derivations:
        ensure("derivation")
    if has_figures:
        ensure("figure")
    if has_exercises:
        ensure("exercise-review")

    return required


def _review_gate(root: Path, config: dict) -> dict:
    claims = _claim_map(root)
    reports = _reviews(root)
    required = _required_reviews(root, config, claims)

    latest: dict[str, dict] = {}
    for report in reports:
        role = report.get("review_type")
        if role:
            latest[role] = report

    issues = []
    for role in required:
        report = latest.get(role)
        if not report:
            issues.append({
                "severity": "error",
                "code": "REV001",
                "message": f"Falta revisión obligatoria: {role}",
            })
            continue
        if report.get("status") != "pass":
            issues.append({
                "severity": "error",
                "code": "REV002",
                "message": f"Revisión {role} no está en pass: {report.get('status')}",
            })
        if any(
            finding.get("severity") in {"error", "blocker"}
            for finding in report.get("findings", [])
        ):
            issues.append({
                "severity": "error",
                "code": "REV003",
                "message": f"Revisión {role} conserva errores/blockers.",
            })

    return {
        "required": required,
        "available": sorted(latest),
        "issues": issues,
    }


def cmd_review_suite(args: argparse.Namespace) -> int:
    root, config = load_book(args.slug)
    _ensure_scaffold(root)
    claims = _claim_map(root)
    required = _required_reviews(root, config, claims)
    existing = {
        item.get("review_type")
        for item in _reviews(root)
        if item.get("review_type")
    }

    created = []
    skipped = []
    for role in required:
        if role in existing and not args.force:
            skipped.append(role)
            continue

        safe = role.upper().replace("-", "_")
        path = root / "reviews" / f"REV-{safe}-001.json"
        if path.exists() and not args.force:
            skipped.append(role)
            continue

        report = {
            "schema_version": 1,
            "review_id": f"REV-{safe}-001",
            "review_type": role,
            "book": args.slug,
            "scope": "book",
            "status": "pending",
            "reviewer": "independent-reviewer",
            "independence": args.independence,
            "checked": [],
            "findings": [],
            "claims_checked": [],
            "sources_consulted": [],
            "tests_reperformed": [],
            "residual_uncertainty": [],
        }
        _write_json(path, report)
        created.append(role)

    print("✓ Review suite preparada.")
    if created:
        print("  creadas: " + ", ".join(created))
    if skipped:
        print("  ya existentes: " + ", ".join(skipped))
    print("  Rellena cada informe usando su review-pack/chapter-pack correspondiente.")
    return 0


def cmd_gate(args: argparse.Namespace) -> int:
    root, config = load_book(args.slug)
    coverage = _coverage(root)
    review_gate = _review_gate(root, config)
    issues = list(coverage["issues"]) + list(review_gate["issues"])

    for spec in _chapter_specs(root):
        if spec.get("status") != "ready":
            issues.append({
                "severity": "error",
                "code": "GATE001",
                "message": f"{spec.get('id')}: capítulo no está ready ({spec.get('status')}).",
            })

    pending_claims = [
        cid for cid, item in _claim_map(root).items()
        if item.get("risk") == "high" and item.get("status") == "pending"
    ]
    if pending_claims:
        issues.append({
            "severity": "error",
            "code": "GATE002",
            "message": "Claims de alto riesgo pendientes: " + ", ".join(pending_claims),
        })

    if coverage["unresolved_conflicts"]:
        issues.append({
            "severity": "error",
            "code": "GATE003",
            "message": f"Quedan {coverage['unresolved_conflicts']} conflicto(s) sin resolver.",
        })

    payload = {
        "book": args.slug,
        "framework_version": FRAMEWORK_VERSION,
        "academic_tool_version": ACADEMIC_TOOL_VERSION,
        "coverage": coverage,
        "reviews": review_gate,
        "issues": issues,
        "pass": not any(i["severity"] == "error" for i in issues),
    }

    if args.json:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    else:
        print(f"AeroBooks Academic Gate — {args.slug}")
        print("Revisiones requeridas: " + ", ".join(review_gate["required"]))
        if not issues:
            print("✓ Academic gate superado.")
        else:
            for issue in issues:
                icon = "✗" if issue["severity"] == "error" else "!"
                print(f"{icon} {issue['code']}: {issue['message']}")
            print("✓ PASS" if payload["pass"] else "✗ FAIL")

    return 0 if payload["pass"] else 1


def _hash_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _release_files(root: Path) -> list[Path]:
    allowed = {".tex", ".bib", ".toml", ".json", ".jsonl", ".md", ".sty", ".cls"}
    files: list[Path] = []

    for path in root.rglob("*"):
        if not path.is_file():
            continue
        rel = path.relative_to(root)
        if rel.parts and rel.parts[0] in {"build", "release", "generated"}:
            continue
        if path.suffix.lower() in allowed:
            files.append(path)

    for base in (
        framework_dir() / "latex",
        framework_dir() / "ai",
        framework_dir() / "prompts",
        framework_dir() / "policies",
    ):
        if not base.exists():
            continue
        for path in base.rglob("*"):
            if path.is_file() and path.suffix.lower() in allowed:
                files.append(path)

    agents = repo_root() / "AGENTS.md"
    if agents.exists():
        files.append(agents)
    return sorted(set(files))


def _relative_release_path(root: Path, path: Path) -> str:
    try:
        return "book/" + str(path.relative_to(root))
    except ValueError:
        return "repo/" + str(path.relative_to(repo_root()))


def cmd_release_manifest(args: argparse.Namespace) -> int:
    root, config = load_book(args.slug)
    _ensure_scaffold(root)
    records = []
    for path in _release_files(root):
        records.append({
            "path": _relative_release_path(root, path),
            "sha256": _hash_file(path),
            "bytes": path.stat().st_size,
        })

    tree_digest = hashlib.sha256(
        "\n".join(f"{r['path']}:{r['sha256']}" for r in records).encode("utf-8")
    ).hexdigest()

    payload = {
        "schema_version": 1,
        "book": args.slug,
        "title": config.get("book", {}).get("title"),
        "edition_number": config.get("book", {}).get("edition_number"),
        "edition_name": config.get("book", {}).get("edition_name"),
        "framework_version": FRAMEWORK_VERSION,
        "academic_tool_version": ACADEMIC_TOOL_VERSION,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "tree_sha256": tree_digest,
        "files": records,
    }

    label = args.label or "candidate"
    path = root / "release" / f"{label}.manifest.json"
    _write_json(path, payload)
    print(f"✓ Release manifest: {path.relative_to(repo_root())}")
    print(f"  tree_sha256={tree_digest}")
    return 0


def cmd_verify_manifest(args: argparse.Namespace) -> int:
    root, _ = load_book(args.slug)
    path = root / "release" / f"{args.label}.manifest.json"
    if not path.exists():
        raise SystemExit(f"No existe {path}")

    data = json.loads(path.read_text(encoding="utf-8"))
    mismatches = []

    for record in data.get("files", []):
        label = record["path"]
        if label.startswith("book/"):
            file_path = root / label.removeprefix("book/")
        elif label.startswith("repo/"):
            file_path = repo_root() / label.removeprefix("repo/")
        else:
            mismatches.append(f"Ruta desconocida en manifest: {label}")
            continue

        if not file_path.exists():
            mismatches.append(f"Falta: {label}")
            continue
        digest = _hash_file(file_path)
        if digest != record.get("sha256"):
            mismatches.append(f"Cambió: {label}")

    if mismatches:
        print("✗ Release manifest NO reproducible:")
        for item in mismatches:
            print(f"  - {item}")
        return 1

    current = []
    for file_path in _release_files(root):
        current.append({
            "path": _relative_release_path(root, file_path),
            "sha256": _hash_file(file_path),
        })
    digest = hashlib.sha256(
        "\n".join(f"{r['path']}:{r['sha256']}" for r in current).encode("utf-8")
    ).hexdigest()

    if digest != data.get("tree_sha256"):
        print("✗ El conjunto actual de archivos no coincide con el manifest.")
        print(f"  esperado: {data.get('tree_sha256')}")
        print(f"  actual:   {digest}")
        return 1

    print(f"✓ Manifest verificado: {path.relative_to(repo_root())}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="aerobooks-ai",
        description=(
            "Capa de trazabilidad, evidencia, revisión independiente y "
            "reproducibilidad académica de AeroBooks."
        ),
    )
    parser.add_argument("--version", action="version", version=ACADEMIC_TOOL_VERSION)
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("init", help="Inicializar specs/evidence/reviews/release de un libro.")
    p.add_argument("slug")
    p.set_defaults(func=cmd_init)

    p = sub.add_parser("bootstrap", help="Generar el paquete inicial para crear un libro desde sus fuentes.")
    p.add_argument("slug")
    p.add_argument("--output")
    p.set_defaults(func=cmd_bootstrap)

    p = sub.add_parser("chapter-spec", help="Crear o reemplazar el contrato de un capítulo.")
    p.add_argument("slug")
    p.add_argument("--id", required=True)
    p.add_argument("--title", required=True)
    p.add_argument("--path", required=True)
    p.add_argument("--status", choices=sorted(CHAPTER_STATUS), default="planned")
    p.add_argument("--objective", action="append", default=[])
    p.add_argument("--prerequisite", action="append", default=[])
    p.add_argument("--source", action="append", default=[])
    p.add_argument("--claim", action="append", default=[])
    p.add_argument("--derivation", action="append", default=[])
    p.add_argument("--figure", action="append", default=[])
    p.add_argument("--exercise", action="append", default=[])
    p.add_argument("--historical-scope", action="store_true")
    p.add_argument("--notes")
    p.add_argument("--allow-missing", action="store_true")
    p.add_argument("--force", action="store_true")
    p.set_defaults(func=cmd_chapter_spec)

    p = sub.add_parser("evidence-add", help="Añadir evidencia localizada a un claim/capítulo.")
    p.add_argument("slug")
    p.add_argument("--id", required=True)
    p.add_argument("--chapter", required=True)
    p.add_argument("--claim")
    p.add_argument("--source")
    p.add_argument("--locator")
    p.add_argument("--support", choices=sorted(EVIDENCE_SUPPORT), required=True)
    p.add_argument("--status", choices=sorted(EVIDENCE_STATUS), default="pending")
    p.add_argument("--confidence", choices=["low", "medium", "high"], default="high")
    p.add_argument("--derivation")
    p.add_argument("--notes")
    p.set_defaults(func=cmd_evidence_add)

    p = sub.add_parser("coverage", help="Auditar cobertura fuente→capítulo→claim→evidencia.")
    p.add_argument("slug")
    p.add_argument("--strict", action="store_true")
    p.add_argument("--json", action="store_true")
    p.set_defaults(func=cmd_coverage)

    p = sub.add_parser("chapter-pack", help="Crear contexto mínimo y exacto para una IA.")
    p.add_argument("slug")
    p.add_argument("chapter")
    p.add_argument("role", choices=sorted(REVIEW_PROMPTS))
    p.add_argument("--output")
    p.set_defaults(func=cmd_chapter_pack)

    p = sub.add_parser("review-template", help="Crear informe de revisión machine-readable.")
    p.add_argument("slug")
    p.add_argument("--id", required=True)
    p.add_argument("--role", choices=sorted(REVIEW_PROMPTS), required=True)
    p.add_argument("--scope", default="book")
    p.add_argument("--reviewer", default="independent-reviewer")
    p.add_argument(
        "--independence",
        choices=["same_model_new_pass", "independent_model", "human", "hybrid"],
        default="same_model_new_pass",
    )
    p.add_argument("--force", action="store_true")
    p.set_defaults(func=cmd_review_template)

    p = sub.add_parser("review-suite", help="Crear plantillas para todas las revisiones exigidas por el riesgo del libro.")
    p.add_argument("slug")
    p.add_argument(
        "--independence",
        choices=["same_model_new_pass", "independent_model", "human", "hybrid"],
        default="same_model_new_pass",
    )
    p.add_argument("--force", action="store_true")
    p.set_defaults(func=cmd_review_suite)

    p = sub.add_parser("gate", help="Puerta académica: cobertura + claims + reviews + conflictos.")
    p.add_argument("slug")
    p.add_argument("--json", action="store_true")
    p.set_defaults(func=cmd_gate)

    p = sub.add_parser("release-manifest", help="Congelar hashes reproducibles de una edición candidata.")
    p.add_argument("slug")
    p.add_argument("--label")
    p.set_defaults(func=cmd_release_manifest)

    p = sub.add_parser("verify-manifest", help="Verificar que una edición coincide byte a byte con su manifest.")
    p.add_argument("slug")
    p.add_argument("label")
    p.set_defaults(func=cmd_verify_manifest)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return int(args.func(args))


if __name__ == "__main__":
    raise SystemExit(main())
