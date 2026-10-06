"""AeroBooks 0.3 research contracts.

The framework does not browse the web. It gives an agent with web access
a reproducible path: discovery, source audit, coverage, derivations,
exercises and fail-closed gates. Books without contract 0.3 keep the
0.2 checks.
"""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path
from typing import Iterable

try:
    import tomllib
except ModuleNotFoundError as exc:  # pragma: no cover
    raise SystemExit("AeroBooks requiere Python 3.11 o superior.") from exc


CONTRACT_V03 = "0.3"
CONTRACT_V02 = "0.2"

TIER_DETAILS = {
    "A0": "official-course",
    "A1": "official-standard",
    "A2": "peer-reviewed",
    "A3": "canonical-academic-book",
    "B0": "open-academic-book",
    "B1": "official-university-material",
    "B2": "institutional-repository",
    "C0": "preprint",
    "C1": "reputable-technical",
    "D0": "informal-course-material",
    "D1": "exam",
    "D2": "student-notes",
    "E": "rejected-unverifiable",
}

COARSE_TIERS = {"A", "B", "C", "D", "E"}
CANONICAL_DETAILS = {"A0", "A1", "A3"}
SUFFICIENT_COARSE = {"A", "B"}
LOW_COARSE = {"D", "E"}
LIFECYCLES = {"candidate", "accepted", "rejected"}
CONTENT_ACCESS = {"full", "snippet", "metadata-only"}
COVERAGE_STATUS = {"GAP", "RESEARCHING", "SUPPORTED", "READY"}
AUTHORING_STATUS = {"SUPPORTED", "READY"}
INDEPENDENT_REVIEW = {"independent_model", "human", "hybrid"}
GLOBAL_SECTIONS = (
    "author",
    "institution",
    "program",
    "editorial",
    "pedagogy",
    "research",
    "quality",
    "copyright",
)
BRIEF_HEADINGS = (
    "## Misión",
    "## Alcance",
    "## Criterios de aceptación",
    "## Autoridad y convenciones",
    "## Política ante conflictos",
    "## Perfil didáctico",
    "## Perfil visual",
    "## Quality gate",
)
BRIEF_PLACEHOLDER = "Describe en 3–6 frases"
FIGURE_CHECKS = (
    "direction",
    "sign",
    "vectors",
    "axes",
    "units",
    "boundary_conditions",
    "conceptual_scale",
    "text_consistency",
)
PACK_SPECS = {
    "course-discovery": (
        "COURSE_DISCOVERY_PACK.md",
        "COURSE_DISCOVERY_AGENT.md",
        ("course.toml", "sources/discovery.json"),
    ),
    "research": (
        "RESEARCH_PACK.md",
        "LITERATURE_RESEARCHER.md",
        (
            "course.toml",
            "sources/discovery.json",
            "sources/manifest.json",
            "sources/coverage.json",
            "sources/research-log.jsonl",
        ),
    ),
    "source-audit": (
        "SOURCE_AUDIT_PACK.md",
        "SOURCE_AUDITOR.md",
        ("sources/manifest.json", "sources/research-log.jsonl", "sources/conflicts.jsonl"),
    ),
    "blueprint": (
        "BLUEPRINT_PACK.md",
        "BOOK_BLUEPRINT_ARCHITECT.md",
        ("course.toml", "sources/discovery.json", "sources/coverage.json", "ai/BRIEF.md"),
    ),
    "derivation": (
        "DERIVATION_PACK.md",
        "DERIVATION_AUDITOR.md",
        ("derivations/ledger.jsonl",),
    ),
    "exercise": (
        "EXERCISE_PACK.md",
        "COMPUTATIONAL_VERIFIER.md",
        ("exercises/ledger.jsonl",),
    ),
    "release": (
        "RELEASE_PACK.md",
        "RELEASE_REVIEWER.md",
        ("sources/coverage.json", "sources/conflicts.jsonl"),
    ),
}


def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def framework_dir() -> Path:
    return repo_root() / "framework"


def global_config_path() -> Path:
    return repo_root() / "aerobooks.toml"


def load_toml(path: Path) -> dict:
    with path.open("rb") as fh:
        return tomllib.load(fh)


def deep_merge(base: dict, override: dict) -> dict:
    """Override wins. Nested tables merge. Lists and scalars are replaced."""
    merged = dict(base)
    for key, value in override.items():
        current = merged.get(key)
        if isinstance(current, dict) and isinstance(value, dict):
            merged[key] = deep_merge(current, value)
        else:
            merged[key] = value
    return merged


def load_global_config(path: Path | None = None) -> dict:
    target = path or global_config_path()
    if not target.exists():
        return {}
    data = load_toml(target)
    issues = validate_global_config(data)
    if issues:
        raise SystemExit("aerobooks.toml inválido: " + "; ".join(issues))
    return data


def validate_global_config(data: dict) -> list[str]:
    issues = []
    if not isinstance(data, dict):
        return ["la configuración global debe ser una tabla TOML"]
    for section in GLOBAL_SECTIONS:
        if section not in data or not isinstance(data[section], dict):
            issues.append(f"falta la sección [{section}]")
    author = data.get("author") if isinstance(data.get("author"), dict) else {}
    institution = data.get("institution") if isinstance(data.get("institution"), dict) else {}
    if not str(author.get("name", "")).strip():
        issues.append("author.name vacío")
    if not str(institution.get("name", "")).strip():
        issues.append("institution.name vacío")
    return issues


def resolve_book_config(book: dict, global_config: dict | None = None) -> dict:
    base = load_global_config() if global_config is None else global_config
    return deep_merge(base, book)


def _read_json(path: Path, default):
    if not path.exists():
        return default
    return json.loads(path.read_text(encoding="utf-8"))


def _write_json(path: Path, data: dict | list) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def _read_jsonl(path: Path) -> list[dict]:
    if not path.exists():
        return []
    rows = []
    for lineno, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        text = line.strip()
        if not text or text.startswith("#"):
            continue
        try:
            item = json.loads(text)
        except json.JSONDecodeError as exc:
            raise SystemExit(f"{path}:{lineno}: JSON inválido: {exc}") from exc
        if isinstance(item, dict):
            rows.append(item)
    return rows


def contract_version(root: Path, config: dict | None = None) -> str:
    if (root / "course.toml").exists():
        return CONTRACT_V03
    if config is None and (root / "book.toml").exists():
        config = load_toml(root / "book.toml")
    academic = (config or {}).get("academic") or {}
    if str(academic.get("contract", "")) == CONTRACT_V03:
        return CONTRACT_V03
    return CONTRACT_V02


def coarse_tier(source: dict) -> str | None:
    detail = source.get("tier_detail")
    if detail:
        if detail not in TIER_DETAILS:
            return None
        return "E" if detail == "E" else detail[0]
    tier = source.get("tier")
    return tier if tier in COARSE_TIERS else None


def issue(code: str, message: str, severity: str = "error") -> dict:
    return {"severity": severity, "code": code, "message": message}


def isbn_checksum_ok(value: str) -> bool:
    digits = re.sub(r"[^0-9Xx]", "", value or "")
    if len(digits) == 13 and digits.isdigit():
        total = sum(int(ch) * (1 if i % 2 == 0 else 3) for i, ch in enumerate(digits))
        return total % 10 == 0
    if len(digits) == 10 and re.fullmatch(r"\d{9}[\dXx]", digits):
        total = 0
        for i, ch in enumerate(digits):
            number = 10 if ch in "Xx" else int(ch)
            total += number * (10 - i)
        return total % 11 == 0
    return False


def doi_shape_ok(value: str) -> bool:
    return bool(re.fullmatch(r"10\.\d{4,9}/\S+", value or ""))


def assess_authority(source: dict, *, currency_year: int | None = None) -> dict:
    """Reproducible profile. Corroboration stays null: it is a claim-level check."""
    detail = source.get("tier_detail")
    tier = coarse_tier(source)
    reasons: dict[str, str] = {}

    if detail in {"A0", "A1"} or (tier == "A" and not detail):
        authority = 3
        reasons["authority"] = "Fuente oficial o de curso."
    elif detail in {"A2", "A3"} or tier == "A":
        authority = 3
        reasons["authority"] = "Literatura académica canónica o revisada."
    elif detail in {"B0", "B1", "B2"} or tier == "B":
        authority = 2
        reasons["authority"] = "Material académico abierto o universitario."
    elif detail == "C1" or tier == "C":
        authority = 1
        reasons["authority"] = "Material técnico o docente, no norma ni revisión formal."
    elif detail == "C0":
        authority = 1
        reasons["authority"] = "Preprint: todavía no es literatura revisada."
    else:
        authority = 0
        reasons["authority"] = "Material informal, de examen o no verificable."

    peer = bool(source.get("peer_reviewed"))
    preprint = detail == "C0" or source.get("kind") == "preprint" or source.get("peer_review_status") == "preprint"
    if peer and not preprint:
        editorial = 3
        reasons["editorial_process"] = "Marcado como peer-reviewed y no como preprint."
    elif detail in {"A0", "A1"} or (tier == "A" and not detail):
        editorial = 3
        reasons["editorial_process"] = "Documento oficial; el proceso no es el de una revista."
    elif detail in {"A3", "B0"} or tier == "B":
        editorial = 2
        reasons["editorial_process"] = "Libro o material universitario con edición, sin dictamen de revista."
    elif preprint:
        editorial = 0
        reasons["editorial_process"] = "Preprint o equivalente: no cuenta como revisión por pares."
    else:
        editorial = 0
        reasons["editorial_process"] = "Sin proceso editorial declarado."

    if "direct_relevance" in source and source.get("direct_relevance") is not None:
        relevance = int(source["direct_relevance"])
        reasons["direct_relevance"] = source.get("relevance_reason") or "Relevancia declarada en la ficha."
    else:
        relevance = None
        reasons["direct_relevance"] = "No evaluada en la ficha; no se inventa."

    published = source.get("published") or source.get("year")
    year = None
    if isinstance(published, int):
        year = published
    elif isinstance(published, str) and re.search(r"\d{4}", published):
        year = int(re.search(r"\d{4}", published).group(0))
    if source.get("currency_relevant") and year and currency_year:
        delta = abs(currency_year - year)
        currency = 3 if delta <= 2 else 2 if delta <= 6 else 1
        reasons["currency"] = f"Año {year} frente a la referencia {currency_year}."
    elif source.get("currency_relevant"):
        currency = None
        reasons["currency"] = "Importa la actualidad, pero no hay año utilizable."
    else:
        currency = None
        reasons["currency"] = "La actualidad no es el criterio de esta fuente."

    access = source.get("content_access")
    if access == "full":
        access_score = 3
        reasons["content_access"] = "Contenido consultado, no solo un snippet."
    elif access == "snippet":
        access_score = 1
        reasons["content_access"] = "Solo snippet o referencia indirecta: no vale como evidencia."
    elif access == "metadata-only":
        access_score = 0
        reasons["content_access"] = "Solo metadatos."
    else:
        access_score = None
        reasons["content_access"] = "Acceso no declarado."

    if source.get("origin_id") or source.get("derived_from"):
        independence = 1
        reasons["independence"] = "Comparte origen o deriva de otra ficha; no suma como fuente independiente."
    else:
        independence = 3
        reasons["independence"] = "No declara un original compartido."

    reasons["corroboration"] = "La corroboración se decide al nivel del claim, no de la ficha."
    return {
        "authority": authority,
        "editorial_process": editorial,
        "direct_relevance": relevance,
        "corroboration": None,
        "currency": currency,
        "content_access": access_score,
        "independence": independence,
        "reasons": reasons,
    }


def _family_roots(sources: Iterable[dict]) -> dict[str, str]:
    parent: dict[str, str] = {}

    def find(node: str) -> str:
        parent.setdefault(node, node)
        while parent[node] != node:
            parent[node] = parent[parent[node]]
            node = parent[node]
        return node

    def union(left: str, right: str) -> None:
        root_left, root_right = find(left), find(right)
        if root_left != root_right:
            parent[root_right] = root_left

    for source in sources:
        sid = source.get("id")
        if not sid:
            continue
        union(sid, sid)
        origin = source.get("origin_id")
        if origin:
            union(sid, f"origin:{origin}")
        for upstream in source.get("derived_from") or []:
            union(sid, str(upstream))
    return {sid: find(sid) for sid in parent if not sid.startswith("origin:")}


def independent_groups(sources: list[dict]) -> list[list[dict]]:
    roots = _family_roots(sources)
    groups: dict[str, list[dict]] = {}
    for source in sources:
        sid = source.get("id")
        if not sid:
            continue
        groups.setdefault(roots.get(sid, sid), []).append(source)
    return list(groups.values())


def _is_low_tier(source: dict) -> bool:
    detail = source.get("tier_detail")
    if detail in TIER_DETAILS and (detail == "E" or detail.startswith("D")):
        return True
    return coarse_tier(source) in LOW_COARSE


def _is_sufficient(source: dict) -> bool:
    if source.get("lifecycle") not in {None, "accepted"}:
        return False
    if source.get("status") == "rejected":
        return False
    if source.get("lifecycle") == "accepted":
        if source.get("consulted") is not True or source.get("content_access") != "full":
            return False
    elif source.get("content_access") not in {None, "full"}:
        return False
    elif source.get("consulted") is False:
        return False
    if _is_low_tier(source):
        return False
    detail = source.get("tier_detail")
    if detail:
        return detail[0] in SUFFICIENT_COARSE
    return coarse_tier(source) in SUFFICIENT_COARSE


def _is_canonical(source: dict) -> bool:
    if not _is_sufficient(source):
        return False
    detail = source.get("tier_detail")
    if detail:
        return detail in CANONICAL_DETAILS
    return coarse_tier(source) == "A"


def claim_corroboration_issues(claim: dict, sources: dict[str, dict]) -> list[dict]:
    if claim.get("risk") != "high" or claim.get("status") in {"pending", "rejected"}:
        return []
    cid = claim.get("id", "?")
    linked = [sources[sid] for sid in claim.get("sources") or [] if sid in sources]
    missing = [sid for sid in claim.get("sources") or [] if sid not in sources]
    issues = []
    for sid in missing:
        issues.append(issue("V03CLM", f"{cid}: fuente desconocida {sid}"))
    if linked and all(_is_low_tier(source) for source in linked):
        issues.append(issue(
            "V03CLM",
            f"{cid}: claim de alto riesgo apoyado solo en fuentes D/E.",
        ))
        return issues

    sufficient = [source for source in linked if _is_sufficient(source)]
    groups = independent_groups(sufficient)
    exception = claim.get("corroboration_exception")
    claim_type = claim.get("type")
    derivation = (claim.get("derivation") or "").strip()

    if len(groups) >= 2:
        return issues
    if len(groups) == 1 and len(sufficient) >= 2 and len(groups) < 2:
        issues.append(issue(
            "V03CLM",
            f"{cid}: las fuentes suficientes comparten origen y no son independientes.",
        ))
        return issues

    canonical = [source for source in sufficient if _is_canonical(source)]
    if canonical and derivation and claim.get("status") == "derived":
        return issues
    if exception == "official_norm" or claim_type == "regulatory":
        if any(
            source.get("tier_detail") == "A1" or coarse_tier(source) == "A"
            for source in sufficient
        ):
            return issues
    if exception == "official_definition" or (
        claim_type == "definition" and any(_is_canonical(source) for source in sufficient)
    ):
        if sufficient:
            return issues
    if exception == "derived_mathematical" or (
        claim_type in {"mathematical", "derived_result"} and derivation and claim.get("status") == "derived"
    ):
        return issues

    issues.append(issue(
        "V03CLM",
        f"{cid}: el claim de alto riesgo no tiene dos fuentes independientes, "
        "ni una fuente canónica con derivación comprobada, ni una excepción justificada.",
    ))
    return issues


def discovery_record(root: Path) -> dict:
    return _read_json(root / "sources" / "discovery.json", {})


def discovery_complete(record: dict) -> bool:
    if record.get("status") != "verified":
        return False
    identity = record.get("identity") or {}
    verification = record.get("verification") or {}
    if verification.get("name_match_sufficient") is not False:
        return False
    if not verification.get("academic_year_checked") or not verification.get("programme_checked"):
        return False
    if not identity.get("course") or not identity.get("institution"):
        return False
    if not identity.get("academic_year") or not identity.get("degree"):
        return False
    if not record.get("guide_url"):
        return False
    return True


def _manifest_sources(root: Path) -> list[dict]:
    data = _read_json(root / "sources" / "manifest.json", {"sources": []})
    return list(data.get("sources") or [])


def _accepted_content_sources(root: Path) -> list[dict]:
    found = []
    for source in _manifest_sources(root):
        if source.get("lifecycle") == "rejected" or source.get("status") == "rejected":
            continue
        if source.get("lifecycle") not in {None, "accepted"} and source.get("status") != "verified":
            continue
        access = source.get("content_access")
        if access in {"snippet", "metadata-only"}:
            continue
        if source.get("lifecycle") == "accepted" or source.get("status") == "verified":
            if access in {None, "full"}:
                found.append(source)
    return found


def source_policy_issues(root: Path) -> list[dict]:
    issues = []
    log_ids = {row.get("id") for row in _read_jsonl(root / "sources" / "research-log.jsonl")}
    for source in _manifest_sources(root):
        sid = source.get("id", "?")
        detail = source.get("tier_detail")
        if detail and detail not in TIER_DETAILS:
            issues.append(issue("V03SRC", f"{sid}: tier_detail desconocido {detail}"))
        elif detail and source.get("tier") and coarse_tier(source) != source.get("tier"):
            issues.append(issue(
                "V03SRC",
                f"{sid}: tier {source.get('tier')} no coincide con tier_detail {detail}",
            ))
        lifecycle = source.get("lifecycle")
        if lifecycle and lifecycle not in LIFECYCLES:
            issues.append(issue("V03SRC", f"{sid}: lifecycle inválido"))
        access = source.get("content_access")
        if access and access not in CONTENT_ACCESS:
            issues.append(issue("V03SRC", f"{sid}: content_access inválido"))
        if source.get("metadata_origin") == "invented":
            issues.append(issue("V03SRC", f"{sid}: metadatos marcados como inventados"))
        preprint = detail == "C0" or source.get("kind") == "preprint" or source.get("peer_review_status") == "preprint"
        if preprint and source.get("peer_reviewed") is True:
            issues.append(issue("V03SRC", f"{sid}: un preprint no puede presentarse como peer-reviewed"))
        if lifecycle == "accepted":
            if source.get("consulted") is not True:
                issues.append(issue("V03SRC", f"{sid}: fuente aceptada sin consulta real del contenido"))
            if access != "full":
                issues.append(issue("V03SRC", f"{sid}: fuente aceptada sin acceso efectivo al contenido"))
            if source.get("doi") and not (source.get("doi_verified") is True and doi_shape_ok(source["doi"])):
                issues.append(issue("V03SRC", f"{sid}: DOI ausente de verificación o con forma inválida"))
            if source.get("doi") and source.get("doi_verified") is True and not source.get("doi_check_method"):
                issues.append(issue("V03SRC", f"{sid}: DOI marcado verificado sin método (crossref, editor o ficha)"))
            if source.get("isbn"):
                if not isbn_checksum_ok(str(source["isbn"])):
                    issues.append(issue("V03SRC", f"{sid}: ISBN no supera el dígito de control"))
                elif source.get("isbn_verified") is not True:
                    issues.append(issue("V03SRC", f"{sid}: ISBN no verificado"))
            if not source.get("rights"):
                issues.append(issue("V03SRC", f"{sid}: fuente aceptada sin nota de derechos"))
            log_id = source.get("discovery_log")
            if not log_id or log_id not in log_ids:
                issues.append(issue("V03LOG", f"{sid}: la aceptación no apunta a una entrada del research log"))
            if source.get("copyright_status") == "violation":
                issues.append(issue("V03CPY", f"{sid}: violación de copyright registrada"))
    for evidence in _read_jsonl(root / "evidence" / "map.jsonl"):
        source_id = evidence.get("source")
        if not source_id:
            continue
        source = next((item for item in _manifest_sources(root) if item.get("id") == source_id), None)
        if not source:
            continue
        access = source.get("content_access")
        if access in {"snippet", "metadata-only"} or source.get("consulted") is False:
            issues.append(issue(
                "V03SRC",
                f"{evidence.get('id', '?')}: la evidencia usa {source_id} sin acceso al contenido completo",
            ))
    return issues


def coverage_matrix(root: Path) -> dict:
    return _read_json(root / "sources" / "coverage.json", {"schema_version": 1, "topics": []})


def coverage_gap_issues(root: Path) -> list[dict]:
    data = coverage_matrix(root)
    topics = data.get("topics") or []
    issues = []
    if not topics:
        issues.append(issue(
            "V03GAP",
            "sources/coverage.json no relaciona todavía el temario oficial.",
        ))
        return issues
    specs = _chapter_specs(root)
    by_chapter: dict[str, list[dict]] = {}
    for topic in topics:
        status = topic.get("status")
        tid = topic.get("id", "?")
        if status not in COVERAGE_STATUS:
            issues.append(issue("V03GAP", f"{tid}: estado de cobertura inválido"))
            continue
        chapter = topic.get("chapter")
        if chapter:
            by_chapter.setdefault(chapter, []).append(topic)
        fundamental = topic.get("fundamental", True)
        if fundamental and status == "GAP":
            issues.append(issue("V03GAP", f"{tid}: concepto fundamental en GAP"))
    for spec in specs:
        sid = spec.get("id")
        topics_for = by_chapter.get(sid, [])
        if spec.get("status") in {"draft", "review", "ready"} and not topics_for:
            issues.append(issue("V03GAP", f"{sid}: capítulo sin fila en la matriz de cobertura"))
        for topic in topics_for:
            if topic.get("fundamental", True) and topic.get("status") not in AUTHORING_STATUS:
                if spec.get("status") in {"draft", "review", "ready"}:
                    issues.append(issue(
                        "V03GAP",
                        f"{spec.get('id')}: no puede avanzarse con {topic.get('id')} en {topic.get('status')}",
                    ))
    return issues


def _chapter_specs(root: Path) -> list[dict]:
    directory = root / "specs"
    if not directory.exists():
        return []
    specs = []
    for path in sorted(directory.glob("*.json")):
        try:
            specs.append(json.loads(path.read_text(encoding="utf-8")))
        except json.JSONDecodeError:
            continue
    return specs


def derivation_issues(root: Path) -> list[dict]:
    issues = []
    for row in _read_jsonl(root / "derivations" / "ledger.jsonl"):
        did = row.get("id", "?")
        if row.get("dimensional_status") == "fail":
            issues.append(issue("V03DIM", f"{did}: error dimensional"))
        if not row.get("fundamental"):
            continue
        if row.get("status") != "audited":
            issues.append(issue("V03DRV", f"{did}: derivación fundamental no auditada"))
            continue
        if row.get("independence") not in INDEPENDENT_REVIEW:
            issues.append(issue("V03DRV", f"{did}: la revisión no es independiente"))
        if not str(row.get("reviewer") or "").strip():
            issues.append(issue("V03DRV", f"{did}: falta revisor"))
        for field_name in (
            "starting_assumptions",
            "starting_equations",
            "steps",
            "result",
            "dimensional_analysis",
            "conditions",
            "limit_cases",
        ):
            if row.get(field_name) in (None, "", []):
                issues.append(issue("V03DRV", f"{did}: falta {field_name}"))
    return issues


def numeric_reproducible(expected: float, actual: float, tolerance: float) -> bool:
    return abs(float(expected) - float(actual)) <= float(tolerance)


def exercise_issues(root: Path) -> list[dict]:
    issues = []
    rows = {row.get("id"): row for row in _read_jsonl(root / "exercises" / "ledger.jsonl")}
    for eid, row in rows.items():
        if row.get("status") not in {"solved", "published"}:
            continue
        if row.get("origin") != "aerobooks":
            issues.append(issue("V03EX", f"{eid}: el enunciado resuelto no está marcado como original de AeroBooks"))
        for field_name in ("statement", "solution", "result", "units", "reviewer"):
            if not str(row.get(field_name) or "").strip():
                issues.append(issue("V03EX", f"{eid}: falta {field_name}"))
        reviews = row.get("reviews") or {}
        for review_name in ("mathematical", "units", "independent_solution"):
            if reviews.get(review_name) != "pass":
                issues.append(issue("V03EX", f"{eid}: falta review {review_name} en pass"))
        computational = row.get("computational") or {}
        applicable = computational.get("applicable", True)
        if applicable:
            if reviews.get("computational") != "pass":
                issues.append(issue("V03EX", f"{eid}: falta verificación computacional"))
            if not computational.get("tool") and not computational.get("script"):
                issues.append(issue("V03EX", f"{eid}: la verificación computacional no declara herramienta ni script"))
        elif reviews.get("computational") != "not_applicable" or not computational.get("reason"):
            issues.append(issue("V03EX", f"{eid}: computational no aplicable sin motivo"))
        tolerance = row.get("numerical_tolerance")
        for check in row.get("checks") or []:
            if not isinstance(check, dict):
                continue
            if {"expected", "actual", "tolerance"} <= set(check):
                if not numeric_reproducible(check["expected"], check["actual"], check["tolerance"]):
                    issues.append(issue("V03EX", f"{eid}: resultado numérico fuera de tolerancia"))
            elif check.get("kind") == "numeric":
                issues.append(issue("V03EX", f"{eid}: comprobación numérica incompleta"))
        if tolerance is not None and row.get("result") and not any(
            isinstance(check, dict) and "expected" in check for check in row.get("checks") or []
        ):
            issues.append(issue("V03EX", f"{eid}: hay tolerancia pero no hay una comprobación numérica reproducible"))
        for case in computational.get("random_cases") or []:
            if not isinstance(case, dict) or "seed" not in case or "tolerance" not in case:
                issues.append(issue("V03EX", f"{eid}: caso aleatorio sin semilla o tolerancia"))
    ready_ids = set()
    for spec in _chapter_specs(root):
        if spec.get("status") == "ready":
            ready_ids.update(spec.get("exercises") or [])
    for eid in sorted(ready_ids):
        row = rows.get(eid)
        if not row or row.get("status") not in {"solved", "published"}:
            issues.append(issue("V03EX", f"{eid}: ejercicio de un capítulo ready sin solución verificada"))
    return issues


def figure_issues(root: Path) -> list[dict]:
    issues = []
    rows = {row.get("id"): row for row in _read_jsonl(root / "figures" / "ledger.jsonl")}
    needed = set()
    for spec in _chapter_specs(root):
        if spec.get("status") in {"review", "ready"}:
            needed.update(spec.get("figures") or [])
    for topic in coverage_matrix(root).get("topics") or []:
        if topic.get("status") == "READY":
            needed.update(topic.get("figures") or [])
    for fid in sorted(needed):
        row = rows.get(fid)
        if not row:
            issues.append(issue("V03FIG", f"{fid}: figura científica sin ficha de revisión"))
            continue
        checks = row.get("checks") or {}
        for name in FIGURE_CHECKS:
            if checks.get(name) != "pass":
                issues.append(issue("V03FIG", f"{fid}: comprobación '{name}' no está en pass"))
        if row.get("status") == "fail":
            issues.append(issue("V03FIG", f"{fid}: figura marcada como físicamente errónea"))
    return issues


def claim_policy_issues(root: Path) -> list[dict]:
    sources = {item.get("id"): item for item in _manifest_sources(root) if item.get("id")}
    issues = []
    ledger = root / "claims" / "ledger.jsonl"
    if not ledger.exists():
        return issues
    for claim in _read_jsonl(ledger):
        issues.extend(claim_corroboration_issues(claim, sources))
    return issues


def v03_coverage_issues(root: Path, config: dict | None = None) -> list[dict]:
    if contract_version(root, config) != CONTRACT_V03:
        return []
    record = discovery_record(root)
    if not discovery_complete(record):
        return [issue(
            "V03DIS",
            "COURSE DISCOVERY REQUIRED: la guía oficial vigente no está verificada "
            "(titulación, curso académico e identidad; el nombre no basta).",
        )]
    issues = []
    if not _accepted_content_sources(root):
        issues.append(issue(
            "V03SRC",
            "No hay fuentes aceptadas con acceso al contenido. La investigación sigue abierta.",
        ))
    issues.extend(source_policy_issues(root))
    issues.extend(coverage_gap_issues(root))
    issues.extend(claim_policy_issues(root))
    issues.extend(derivation_issues(root))
    issues.extend(exercise_issues(root))
    issues.extend(figure_issues(root))
    return issues


def build_issue(root: Path) -> dict | None:
    logs = [root / "main.log", *root.glob("*.log")]
    existing = [path for path in logs if path.exists() and path.is_file()]
    if not existing:
        return issue("V03BLD", "No hay compilación registrada (falta main.log con PDF generado).")
    text = existing[0].read_text(encoding="utf-8", errors="ignore")
    if "Emergency stop" in text or "Fatal error" in text:
        return issue("V03BLD", "La última compilación contiene un error fatal.")
    if "Output written" not in text:
        return issue("V03BLD", "El log de LaTeX no registra un PDF escrito.")
    return None


def v03_gate_issues(root: Path, config: dict | None = None) -> list[dict]:
    if contract_version(root, config) != CONTRACT_V03:
        return []
    issues = list(v03_coverage_issues(root, config))
    codes = {item["code"] for item in issues}
    if "V03DIS" not in codes:
        build = build_issue(root)
        if build:
            issues.append(build)
    return issues


def brief_ready(root: Path) -> bool:
    path = root / "ai" / "BRIEF.md"
    if not path.exists():
        return False
    text = path.read_text(encoding="utf-8")
    if any(heading not in text for heading in BRIEF_HEADINGS):
        return False
    if BRIEF_PLACEHOLDER in text:
        return False
    return True


def authoring_block_reason(root: Path, spec: dict, role: str) -> str | None:
    if role != "author" or contract_version(root) != CONTRACT_V03:
        return None
    if not discovery_complete(discovery_record(root)):
        return "CHAPTER BLOCKED: COURSE DISCOVERY REQUIRED"
    chapter_id = spec.get("id")
    topics = [
        topic for topic in coverage_matrix(root).get("topics") or []
        if topic.get("chapter") == chapter_id
    ]
    if not topics:
        return f"CHAPTER BLOCKED: {chapter_id} no está en sources/coverage.json"
    blocked = [
        topic for topic in topics
        if topic.get("fundamental", True) and topic.get("status") not in AUTHORING_STATUS
    ]
    if blocked:
        listed = ", ".join(f"{topic.get('id')}={topic.get('status')}" for topic in blocked)
        return f"CHAPTER BLOCKED: cobertura insuficiente ({listed})"
    return None


def v03_next_messages(root: Path, slug: str) -> list[str]:
    if not discovery_complete(discovery_record(root)):
        return [
            "COURSE DISCOVERY REQUIRED",
            "  Una coincidencia de nombre no identifica la asignatura.",
            "  Hay que verificar la guía oficial vigente, la titulación y el curso académico.",
            f"  Genera el paquete: aerobooks-ai course-discovery-pack {slug}",
        ]
    if not _accepted_content_sources(root):
        return [
            "RESEARCH REQUIRED",
            "  No hay fuentes aceptadas con el contenido realmente consultado.",
            f"  Genera el paquete: aerobooks-ai research-pack {slug}",
        ]
    gaps = [
        topic for topic in coverage_matrix(root).get("topics") or []
        if topic.get("fundamental", True) and topic.get("status") == "GAP"
    ]
    if not coverage_matrix(root).get("topics") or gaps:
        return [
            "COVERAGE GAP",
            "  El temario oficial todavía tiene conceptos fundamentales sin soporte.",
            f"  Completa sources/coverage.json y ejecuta: aerobooks-ai coverage {slug} --strict",
        ]
    if not brief_ready(root):
        return [
            "BLUEPRINT REQUIRED",
            f"  Genera el paquete: aerobooks-ai blueprint-pack {slug}",
        ]
    specs = _chapter_specs(root)
    if not specs:
        return [
            "SPECS REQUIRED",
            f"  Crea los chapter specs: aerobooks-ai chapter-spec {slug} ...",
        ]
    unfinished = [spec for spec in specs if spec.get("status") in {"planned", "draft"}]
    if unfinished:
        spec = unfinished[0]
        blocked = authoring_block_reason(root, spec, "author")
        if blocked:
            return [blocked, f"  Tema aún no SUPPORTED para {spec.get('id')}."]
        return [
            f"AUTHORING: {spec.get('id')} — {spec.get('title', '')}".rstrip(),
            f"  aerobooks-ai chapter-pack {slug} {spec.get('id')} author",
        ]
    in_review = [spec for spec in specs if spec.get("status") == "review"]
    if in_review:
        return [
            "REVIEW REQUIRED",
            f"  aerobooks-ai review-suite {slug}",
            f"  aerobooks-ai chapter-pack {slug} {in_review[0].get('id')} red-team",
        ]
    return [
        "RELEASE GATE",
        f"  aerobooks check {slug} --strict",
        f"  aerobooks-ai coverage {slug} --strict",
        f"  aerobooks-ai gate {slug}",
        f"  aerobooks build {slug}",
        f"  aerobooks-ai release-pack {slug}",
    ]


def _toml_string(value: str) -> str:
    return json.dumps(value, ensure_ascii=False)


def _ensure_toml_key(path: Path, section: str, key: str, value: str) -> None:
    lines = path.read_text(encoding="utf-8").splitlines()
    current = None
    serialized = value if re.fullmatch(r"-?\d+", value) else _toml_string(value)
    for index, line in enumerate(lines):
        header = re.match(r"\s*\[([^\]]+)\]\s*$", line)
        if header:
            if current == section:
                lines.insert(index, f"{key} = {serialized}")
                path.write_text("\n".join(lines) + "\n", encoding="utf-8")
                return
            current = header.group(1)
            continue
        if current == section and re.match(rf"\s*{re.escape(key)}\s*=", line):
            lines[index] = f"{key} = {serialized}"
            path.write_text("\n".join(lines) + "\n", encoding="utf-8")
            return
    if current == section:
        lines.append(f"{key} = {serialized}")
        path.write_text("\n".join(lines) + "\n", encoding="utf-8")
        return
    raise SystemExit(f"No existe la sección [{section}] en {path}")


def inventory_local_sources(directory: Path) -> list[dict]:
    allowed = {
        ".pdf", ".docx", ".pptx", ".xlsx", ".xls", ".csv",
        ".tex", ".md", ".txt", ".html", ".htm", ".epub",
    }
    records = []
    for path in sorted(directory.rglob("*")):
        if not path.is_file() or path.suffix.lower() not in allowed:
            continue
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        records.append({
            "filename": path.name,
            "relative_path": str(path.relative_to(directory)),
            "extension": path.suffix.lower(),
            "bytes": path.stat().st_size,
            "sha256": digest,
            "classification": "candidate",
            "lifecycle": "candidate",
            "content_access": "metadata-only",
            "notes": "Inventariado. El contenido no se ha auditado ni copiado al repositorio.",
        })
    return records


def create_course(
    *,
    slug: str,
    course: str,
    institution: str,
    dest: Path,
    degree: str | None = None,
    academic_year: str | None = None,
    code: str | None = None,
    language: str | None = None,
    sources: Path | None = None,
    author: str | None = None,
) -> Path:
    if not course.strip() or not institution.strip():
        raise SystemExit("new-course exige asignatura e institución.")
    global_config = load_global_config()
    author_name = author or global_config.get("author", {}).get("name") or "Daniel Miguel Tejedor"
    subtitle = global_config.get("editorial", {}).get("subtitle") or "Manual académico"
    programme = degree or global_config.get("program", {}).get("name") or ""
    lang = language or global_config.get("program", {}).get("language") or "es"

    from .cli import copy_template, load_toml, write_metadata

    root = copy_template(slug, course, subtitle, author_name, dest=dest)
    book_toml = root / "book.toml"
    _ensure_toml_key(book_toml, "institution", "name", institution)
    if programme:
        _ensure_toml_key(book_toml, "institution", "programme", programme)
    _ensure_toml_key(book_toml, "book", "language", lang)
    _ensure_toml_key(book_toml, "academic", "contract", CONTRACT_V03)
    mode = "intake" if sources else "source-discovery"
    if mode == "source-discovery":
        _ensure_toml_key(book_toml, "ai", "research_mode", "source_discovery")

    course_toml = "\n".join([
        f"schema_version = 1",
        f"slug = {_toml_string(slug)}",
        f"course = {_toml_string(course)}",
        f"institution = {_toml_string(institution)}",
        f"degree = {_toml_string(degree or '')}",
        f"academic_year = {_toml_string(academic_year or '')}",
        f"code = {_toml_string(code or '')}",
        f"language = {_toml_string(lang)}",
        f"sources = {_toml_string(str(sources) if sources else '')}",
        f"mode = {_toml_string(mode)}",
        "",
    ])
    (root / "course.toml").write_text(course_toml, encoding="utf-8")

    _write_json(root / "sources" / "discovery.json", {
        "schema_version": 1,
        "status": "required",
        "identity": {
            "course": course,
            "institution": institution,
            "degree": degree,
            "academic_year": academic_year,
            "code": code,
            "year_of_study": None,
            "semester": None,
            "ects": None,
            "language": lang,
        },
        "official_url": None,
        "guide_url": None,
        "verification": {
            "name_match_sufficient": False,
            "academic_year_checked": False,
            "programme_checked": False,
            "identity_notes": "El nombre de la asignatura no basta. Hay que localizar la guía oficial vigente.",
        },
        "faculty": [],
        "competences": [],
        "outcomes": [],
        "syllabus": [],
        "assessment": None,
        "bibliography": [],
    })
    _write_json(root / "sources" / "coverage.json", {"schema_version": 1, "topics": []})
    for relative in (
        root / "sources" / "research-log.jsonl",
        root / "derivations" / "ledger.jsonl",
        root / "exercises" / "ledger.jsonl",
        root / "figures" / "ledger.jsonl",
    ):
        relative.parent.mkdir(parents=True, exist_ok=True)
        if not relative.exists():
            relative.write_text("", encoding="utf-8")

    if sources:
        directory = sources.expanduser().resolve()
        if not directory.exists() or not directory.is_dir():
            raise SystemExit(f"No existe el directorio de fuentes: {directory}")
        records = inventory_local_sources(directory)
        _write_json(root / "build" / "SOURCE_INTAKE.json", {
            "schema_version": 1,
            "book": slug,
            "source_directory_name": directory.name,
            "files": records,
            "warning": (
                "Inventario local. No clasifica autoridad ni derechos y no copia los archivos. "
                "Cada candidato sigue en lifecycle=candidate y content_access=metadata-only "
                "hasta que alguien consulte el contenido."
            ),
        })
        log = {
            "id": "LOG-INTAKE-001",
            "query": f"local intake {directory.name}",
            "date": "local",
            "agent": "aerobooks-new-course",
            "candidates": [item["relative_path"] for item in records],
            "accepted": [],
            "rejected": [],
            "reason": "Inventario de archivos locales. Ninguno queda aceptado como evidencia.",
        }
        with (root / "sources" / "research-log.jsonl").open("a", encoding="utf-8") as fh:
            fh.write(json.dumps(log, ensure_ascii=False) + "\n")

    write_metadata(root, load_toml(book_toml))
    return root


def write_pack(root: Path, kind: str, slug: str, output: Path | None = None) -> Path:
    if kind not in PACK_SPECS:
        raise SystemExit(f"Paquete desconocido: {kind}")
    filename, prompt_name, relatives = PACK_SPECS[kind]
    prompt = framework_dir() / "prompts" / prompt_name
    if not prompt.exists():
        raise SystemExit(f"No existe el prompt {prompt}")
    chunks = [
        f"# AeroBooks {kind} pack — {slug}",
        "",
        "Este paquete contiene solo el contrato de esta fase.",
        "No uses conocimiento no registrado como evidencia.",
        "No trates un snippet, un resultado de buscador o una ficha bibliográfica como si hubieras leído la obra.",
        "",
        f"## {prompt_name}",
        "",
        prompt.read_text(encoding="utf-8").rstrip(),
        "",
    ]
    for relative in relatives:
        path = root / relative
        chunks.append(f"## {relative}")
        chunks.append("")
        if path.exists():
            chunks.append(path.read_text(encoding="utf-8").rstrip() or "(vacío)")
        else:
            chunks.append("(todavía no existe)")
        chunks.append("")
    chunks += [
        "## SALIDA",
        "",
        "Actualiza únicamente los artefactos de esta fase.",
        "Deja por escrito qué consultaste, qué aceptaste, qué rechazaste y por qué.",
        "Si falta acceso al contenido, la fuente se queda en metadata-only o candidate.",
        "",
    ]
    target = output or (root / "build" / "ai" / filename)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text("\n".join(chunks), encoding="utf-8")
    return target
