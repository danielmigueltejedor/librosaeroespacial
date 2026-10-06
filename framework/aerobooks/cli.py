from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import textwrap
from dataclasses import dataclass, field
from datetime import date
from pathlib import Path
from typing import Iterable

try:
    import tomllib
except ModuleNotFoundError as exc:
    raise SystemExit("AeroBooks requiere Python 3.11 o superior.") from exc

FRAMEWORK_NAME = "AeroBooks"
FRAMEWORK_VERSION = "0.1.0"
TEXT_EXTENSIONS = {".tex", ".md", ".toml", ".json", ".bib", ".txt", ".yml", ".yaml"}

EDITION_NAMES = {
    1: "Primera edición",
    2: "Segunda edición",
    3: "Tercera edición",
    4: "Cuarta edición",
    5: "Quinta edición",
    6: "Sexta edición",
    7: "Séptima edición",
    8: "Octava edición",
    9: "Novena edición",
    10: "Décima edición",
    11: "Undécima edición",
    12: "Duodécima edición",
    13: "Decimotercera edición",
    14: "Decimocuarta edición",
    15: "Decimoquinta edición",
    16: "Decimosexta edición",
    17: "Decimoséptima edición",
    18: "Decimoctava edición",
    19: "Decimonovena edición",
    20: "Vigésima edición",
}

MONTHS_ES = {
    1: "Enero", 2: "Febrero", 3: "Marzo", 4: "Abril",
    5: "Mayo", 6: "Junio", 7: "Julio", 8: "Agosto",
    9: "Septiembre", 10: "Octubre", 11: "Noviembre", 12: "Diciembre",
}


@dataclass
class Finding:
    level: str
    code: str
    message: str
    path: str | None = None

    def as_dict(self) -> dict:
        return {
            "level": self.level,
            "code": self.code,
            "message": self.message,
            "path": self.path,
        }


@dataclass
class Report:
    book: str
    findings: list[Finding] = field(default_factory=list)

    def add(self, level: str, code: str, message: str, path: Path | str | None = None) -> None:
        self.findings.append(
            Finding(level, code, message, str(path) if path is not None else None)
        )

    @property
    def errors(self) -> list[Finding]:
        return [f for f in self.findings if f.level == "error"]

    @property
    def warnings(self) -> list[Finding]:
        return [f for f in self.findings if f.level == "warning"]

    def ok(self, strict: bool = False) -> bool:
        return not self.errors and (not strict or not self.warnings)

    def as_dict(self) -> dict:
        return {
            "book": self.book,
            "ok": self.ok(),
            "errors": len(self.errors),
            "warnings": len(self.warnings),
            "findings": [f.as_dict() for f in self.findings],
        }


def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def book_dir(slug: str) -> Path:
    return repo_root() / "books" / slug


def framework_dir() -> Path:
    return repo_root() / "framework"


def load_toml(path: Path) -> dict:
    with path.open("rb") as fh:
        return tomllib.load(fh)


def load_book(slug: str) -> tuple[Path, dict]:
    root = book_dir(slug)
    config = root / "book.toml"
    if not config.exists():
        raise SystemExit(
            f"No existe {config}. Migra el libro al framework o usa 'aerobooks new'."
        )
    return root, load_toml(config)


def current_spanish_date() -> str:
    today = date.today()
    return f"{MONTHS_ES[today.month]} de {today.year}"


def edition_name(number: int) -> str:
    return EDITION_NAMES.get(number, f"{number}.ª edición")


def latex_escape(value: str) -> str:
    replacements = {"&": r"\&", "%": r"\%", "#": r"\#", "_": r"\_"}
    return "".join(replacements.get(ch, ch) for ch in value)


def write_metadata(root: Path, config: dict) -> Path:
    meta = config.get("book", {})
    author = config.get("author", {})
    institution = config.get("institution", {})

    required = [
        "title", "subtitle", "volume", "volume_title",
        "edition_name", "date",
    ]
    missing = [key for key in required if not meta.get(key)]
    if missing:
        raise SystemExit(
            "Faltan metadatos obligatorios en book.toml: " + ", ".join(missing)
        )

    generated = root / "generated"
    generated.mkdir(exist_ok=True)
    path = generated / "metadata.tex"

    title_display = meta.get("title_display_tex") or latex_escape(meta["title"])
    title_short = meta.get("title_short") or meta["title"]

    content = textwrap.dedent(
        rf"""
        % AUTO-GENERADO POR AEROBOOKS. NO EDITAR A MANO.
        \newcommand{{\BookTitle}}{{{latex_escape(meta["title"])}}}
        \newcommand{{\BookTitleShort}}{{{latex_escape(title_short)}}}
        \newcommand{{\BookTitleDisplay}}{{{title_display}}}
        \newcommand{{\BookSubtitle}}{{{latex_escape(meta["subtitle"])}}}
        \newcommand{{\BookVolume}}{{{latex_escape(meta["volume"])}}}
        \newcommand{{\BookVolumeSubtitle}}{{{latex_escape(meta["volume_title"])}}}
        \newcommand{{\BookAuthor}}{{{latex_escape(author.get("name", ""))}}}
        \newcommand{{\BookEdition}}{{{latex_escape(meta["edition_name"])}}}
        \newcommand{{\BookDate}}{{{latex_escape(meta["date"])}}}
        \newcommand{{\BookProgramme}}{{{latex_escape(institution.get("programme", ""))}}}
        \newcommand{{\BookInstitution}}{{{latex_escape(institution.get("name", ""))}}}
        \newcommand{{\BookLegalNotice}}{{{latex_escape(meta.get("legal_notice", "Edición de estudio independiente."))}}}
        """
    ).lstrip()
    path.write_text(content, encoding="utf-8")
    return path


def copy_template(slug: str, title: str, subtitle: str, author: str) -> Path:
    target = book_dir(slug)
    if target.exists():
        raise SystemExit(f"Ya existe {target}")

    template = framework_dir() / "templates" / "book"
    if not template.exists():
        raise SystemExit(f"No existe la plantilla {template}")

    shutil.copytree(template, target)

    tokens = {
        "{{SLUG}}": slug,
        "{{TITLE}}": title,
        "{{SUBTITLE}}": subtitle,
        "{{AUTHOR}}": author,
        "{{DATE}}": current_spanish_date(),
    }

    for path in target.rglob("*"):
        if path.is_file() and path.suffix.lower() in TEXT_EXTENSIONS:
            text = path.read_text(encoding="utf-8")
            for key, value in tokens.items():
                text = text.replace(key, value)
            path.write_text(text, encoding="utf-8")

    config = load_toml(target / "book.toml")
    write_metadata(target, config)
    return target


def iter_tex(root: Path) -> Iterable[Path]:
    yield from sorted(p for p in root.rglob("*.tex") if "generated" not in p.parts)


def read_all_tex(root: Path) -> str:
    chunks = []
    for path in iter_tex(root):
        try:
            chunks.append(path.read_text(encoding="utf-8"))
        except UnicodeDecodeError:
            continue
    return "\n".join(chunks)


def bib_keys(path: Path) -> set[str]:
    if not path.exists():
        return set()
    text = path.read_text(encoding="utf-8")
    return set(re.findall(r"@\w+\s*\{\s*([^,\s]+)\s*,", text))


def citation_keys(tex: str) -> set[str]:
    pattern = re.compile(
        r"\\(?:auto|text|paren|foot|smart|super)?cite\*?(?:\[[^\]]*\]){0,2}\{([^}]+)\}"
    )
    keys: set[str] = set()
    for match in pattern.finditer(tex):
        keys.update(k.strip() for k in match.group(1).split(",") if k.strip())
    return keys


def label_keys(tex: str) -> list[str]:
    return re.findall(r"\\label\{([^}]+)\}", tex)


def ref_keys(tex: str) -> set[str]:
    keys: set[str] = set()
    for match in re.finditer(r"\\(?:c|C|page|eq)?ref\{([^}]+)\}", tex):
        keys.update(k.strip() for k in match.group(1).split(",") if k.strip())
    return keys


def load_source_manifest(root: Path, report: Report) -> tuple[dict, set[str]]:
    path = root / "sources" / "manifest.json"
    if not path.exists():
        report.add("error", "SRC001", "Falta sources/manifest.json", path)
        return {}, set()

    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        report.add("error", "SRC002", f"JSON inválido: {exc}", path)
        return {}, set()

    seen: set[str] = set()
    valid_tiers = {"A", "B", "C", "D", "E"}
    for index, source in enumerate(data.get("sources", []), 1):
        sid = source.get("id")
        if not sid:
            report.add("error", "SRC003", f"Fuente #{index} sin id", path)
            continue
        if sid in seen:
            report.add("error", "SRC004", f"ID de fuente duplicado: {sid}", path)
        seen.add(sid)

        for field_name in ("title", "kind", "tier", "role", "status"):
            if not source.get(field_name):
                report.add(
                    "error", "SRC005",
                    f"{sid}: falta el campo obligatorio '{field_name}'", path
                )

        tier = source.get("tier")
        if tier and tier not in valid_tiers:
            report.add("error", "SRC006", f"{sid}: tier desconocido '{tier}'", path)

        if source.get("status") not in {"verified", "provided", "pending", "rejected"}:
            report.add(
                "warning", "SRC007",
                f"{sid}: status debería ser verified/provided/pending/rejected", path
            )

    return data, seen


def check_claim_ledger(root: Path, source_ids: set[str], report: Report) -> None:
    path = root / "claims" / "ledger.jsonl"
    if not path.exists():
        report.add("warning", "CLM001", "No existe claims/ledger.jsonl", path)
        return

    seen: set[str] = set()
    for lineno, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        try:
            item = json.loads(line)
        except json.JSONDecodeError as exc:
            report.add("error", "CLM002", f"Línea {lineno}: JSON inválido: {exc}", path)
            continue

        cid = item.get("id")
        if not cid:
            report.add("error", "CLM003", f"Línea {lineno}: claim sin id", path)
            continue
        if cid in seen:
            report.add("error", "CLM004", f"Claim duplicado: {cid}", path)
        seen.add(cid)

        if not item.get("claim"):
            report.add("error", "CLM005", f"{cid}: falta claim", path)

        status = item.get("status")
        if status not in {"verified", "derived", "pending", "rejected"}:
            report.add("warning", "CLM006", f"{cid}: status no reconocido '{status}'", path)

        sources = item.get("sources", [])
        if status == "verified" and not sources:
            report.add("error", "CLM007", f"{cid}: claim verificado sin fuentes", path)

        unknown = [sid for sid in sources if sid not in source_ids]
        if unknown:
            report.add(
                "error", "CLM008",
                f"{cid}: fuentes no declaradas en manifest: {', '.join(unknown)}", path
            )

        if item.get("risk") == "high" and status == "verified":
            if not sources and not item.get("derivation"):
                report.add(
                    "error", "CLM009",
                    f"{cid}: claim de alto riesgo sin fuente ni derivación", path
                )


def check_figures_and_tables(tex: str, report: Report) -> None:
    for env, prefix in (("figure", "FIG"), ("table", "TAB")):
        pattern = re.compile(
            rf"\\begin\{{{env}\}}(?:\[[^\]]*\])?(.*?)\\end\{{{env}\}}",
            re.DOTALL,
        )
        for i, match in enumerate(pattern.finditer(tex), 1):
            body = match.group(1)
            if r"\caption" not in body:
                report.add("warning", f"{prefix}001", f"{env} #{i} sin caption")
            if r"\label" not in body:
                report.add("warning", f"{prefix}002", f"{env} #{i} sin label")


def static_check(slug: str, strict: bool = False) -> Report:
    root, config = load_book(slug)
    report = Report(slug)

    required = [
        root / "main.tex",
        root / "references.bib",
        root / "book.toml",
        root / "sources" / "manifest.json",
        root / "ai" / "BRIEF.md",
    ]
    for path in required:
        if not path.exists():
            report.add("error", "FS001", "Archivo obligatorio ausente", path)

    meta = config.get("book", {})
    if meta.get("slug") and meta.get("slug") != slug:
        report.add(
            "error", "META000",
            f"book.slug='{meta.get('slug')}' no coincide con la carpeta '{slug}'",
            root / "book.toml",
        )

    for field_name in (
        "title", "subtitle", "edition_number", "edition_name",
        "date", "language",
    ):
        if not meta.get(field_name):
            report.add("error", "META001", f"Falta book.{field_name}", root / "book.toml")

    number = meta.get("edition_number")
    name = meta.get("edition_name")
    if isinstance(number, int) and name and name != edition_name(number):
        report.add(
            "warning", "META002",
            f"edition_name='{name}' no coincide con edition_number={number} "
            f"('{edition_name(number)}')",
            root / "book.toml",
        )

    tex = read_all_tex(root)
    bib = bib_keys(root / "references.bib")

    used_citations = citation_keys(tex)
    for key in sorted(used_citations - bib):
        report.add("error", "BIB001", f"Cita sin entrada BibLaTeX: {key}")

    labels = label_keys(tex)
    duplicate_labels = sorted({key for key in labels if labels.count(key) > 1})
    for key in duplicate_labels:
        report.add("error", "TEX001", f"Label duplicado: {key}")

    references = ref_keys(tex)
    for key in sorted(references - set(labels)):
        report.add("error", "TEX002", f"Referencia a label inexistente: {key}")

    for marker in ("TODO", "FIXME", "XXX", "[CITATION NEEDED]", "[SOURCE NEEDED]"):
        if marker in tex:
            report.add("warning", "TEX003", f"Marcador pendiente encontrado: {marker}")

    check_figures_and_tables(tex, report)

    manifest, source_ids = load_source_manifest(root, report)
    if manifest.get("book") and manifest.get("book") != slug:
        report.add(
            "error", "SRC000",
            f"manifest.book='{manifest.get('book')}' no coincide con '{slug}'",
            root / "sources" / "manifest.json",
        )

    for source in manifest.get("sources", []):
        key = source.get("citation_key")
        if key and key not in bib:
            report.add(
                "error", "SRC008",
                f"{source.get('id', '?')}: citation_key '{key}' no existe en references.bib",
                root / "sources" / "manifest.json",
            )

    policy = config.get("quality", {})
    claims_path = root / "claims" / "ledger.jsonl"
    if policy.get("require_claim_ledger", False) and not claims_path.exists():
        report.add("error", "CLM000", "Se exige claim ledger y no existe.", claims_path)

    conflicts_path = root / "sources" / "conflicts.jsonl"
    ai_policy = config.get("ai", {})
    if ai_policy.get("record_conflicts", False) and not conflicts_path.exists():
        report.add(
            "error", "SRC009",
            "La política exige registrar conflictos y falta sources/conflicts.jsonl.",
            conflicts_path,
        )

    check_claim_ledger(root, source_ids, report)

    if policy.get("require_list_of_figures", False) and r"\listoffigures" not in tex:
        report.add("error", "QA002", "Se exige índice de figuras y main.tex no lo incluye.")
    if policy.get("require_list_of_tables", False) and r"\listoftables" not in tex:
        report.add("error", "QA003", "Se exige índice de cuadros y main.tex no lo incluye.")

    author_name = config.get("author", {}).get("name")
    if author_name:
        for path in list((root / "chapters").rglob("*.tex")) + list((root / "appendices").rglob("*.tex")):
            if path.exists() and author_name in path.read_text(encoding="utf-8"):
                report.add(
                    "warning", "ED001",
                    "El nombre del autor aparece dentro del contenido; debería limitarse a portada/créditos/metadatos.",
                    path,
                )

    generated = root / "generated" / "metadata.tex"
    if not generated.exists():
        report.add(
            "warning", "META003",
            "Falta generated/metadata.tex; ejecuta 'aerobooks sync'.",
            generated,
        )

    if policy.get("require_source_audit", False):
        audit = root / "appendices" / "source-audit.tex"
        if not audit.exists():
            report.add("error", "QA001", "Se exige auditoría de fuentes y no existe.", audit)

    return report


def print_report(report: Report, strict: bool = False, json_output: bool = False) -> None:
    if json_output:
        payload = report.as_dict()
        payload["strict_ok"] = report.ok(strict=strict)
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return

    icon = {"error": "✗", "warning": "!", "info": "·"}
    for finding in report.findings:
        location = f" [{finding.path}]" if finding.path else ""
        print(
            f"{icon.get(finding.level, '·')} {finding.level.upper():7} "
            f"{finding.code}: {finding.message}{location}"
        )

    print()
    print(
        f"{report.book}: {len(report.errors)} error(es), "
        f"{len(report.warnings)} aviso(s)"
    )
    if report.ok(strict=strict):
        print("✓ Quality gate superado.")
    else:
        print("✗ Quality gate NO superado.")


def texinputs_env(root: Path) -> dict[str, str]:
    env = os.environ.copy()
    paths = [
        str(repo_root() / "framework" / "latex") + "//",
        str(repo_root() / "shared") + "//",
        str(root) + "//",
    ]
    current = env.get("TEXINPUTS", "")
    env["TEXINPUTS"] = os.pathsep.join(paths + ([current] if current else [""]))
    return env


def run_build(slug: str, halt_on_error: bool = True) -> int:
    root, config = load_book(slug)
    write_metadata(root, config)
    latex = config.get("latex", {})
    entry = latex.get("entrypoint", "main.tex")

    if shutil.which("latexmk") is None:
        print("No se encuentra 'latexmk'. Ejecuta 'aerobooks doctor'.", file=sys.stderr)
        return 127

    cmd = ["latexmk", "-pdf", "-interaction=nonstopmode"]
    if halt_on_error:
        cmd.append("-halt-on-error")
    cmd.append(entry)

    print(f"→ Compilando {slug}: {' '.join(cmd)}")
    return subprocess.call(cmd, cwd=root, env=texinputs_env(root))


def make_ai_pack(slug: str, output: Path | None = None) -> Path:
    root, config = load_book(slug)
    manifest_path = root / "sources" / "manifest.json"
    brief_path = root / "ai" / "BRIEF.md"
    claims_path = root / "claims" / "ledger.jsonl"

    sections: list[tuple[str, str]] = []

    sections.append((
        "INSTRUCCIÓN DE USO",
        (
            "Este archivo es un paquete de contexto generado por AeroBooks. "
            "La IA debe obedecer el contrato del proyecto, después el brief del libro "
            "y finalmente las fuentes. Si falta evidencia, debe declarar la laguna; "
            "no debe inventar datos, citas, fechas, autores, resultados ni bibliografía."
        ),
    ))

    protocol_files = [
        framework_dir() / "ai" / "AI_AUTHORING_PROTOCOL.md",
        framework_dir() / "ai" / "AI_WORKFLOW.md",
        framework_dir() / "ai" / "SOURCE_POLICY.md",
        framework_dir() / "ai" / "FACT_CHECK_PROTOCOL.md",
        framework_dir() / "ai" / "LATEX_PROTOCOL.md",
        framework_dir() / "ai" / "RELEASE_GATE.md",
        repo_root() / "shared" / "STYLE_GUIDE.md",
    ]
    for path in protocol_files:
        if path.exists():
            sections.append((path.name, path.read_text(encoding="utf-8")))

    for path in (
        framework_dir() / "prompts" / "MASTER_AUTHOR.md",
        framework_dir() / "prompts" / "EXACT_REPRODUCER.md",
    ):
        if path.exists():
            sections.append((path.name, path.read_text(encoding="utf-8")))

    sections.append(("BOOK.TOML", (root / "book.toml").read_text(encoding="utf-8")))

    if brief_path.exists():
        sections.append(("BRIEF DEL LIBRO", brief_path.read_text(encoding="utf-8")))

    if manifest_path.exists():
        sections.append(("MANIFIESTO DE FUENTES", manifest_path.read_text(encoding="utf-8")))

    if claims_path.exists():
        sections.append(("LEDGER DE CLAIMS", claims_path.read_text(encoding="utf-8")))

    chapters = "\n".join(
        f"- {p.relative_to(root)}" for p in sorted((root / "chapters").rglob("*.tex"))
    )
    sections.append(("MAPA DE CAPÍTULOS", chapters or "(sin capítulos)"))

    text = [
        f"# AeroBooks AI Context — {config.get('book', {}).get('title', slug)}",
        "",
        f"Generado por {FRAMEWORK_NAME} {FRAMEWORK_VERSION}.",
        "",
    ]
    for title, body in sections:
        text += [f"## {title}", "", body.rstrip(), ""]

    if output is None:
        output = root / "build" / "AI_CONTEXT.md"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text("\n".join(text), encoding="utf-8")
    return output


REVIEW_PROMPTS = {
    "author": "MASTER_AUTHOR.md",
    "source": "SOURCE_AUDITOR.md",
    "outline": "OUTLINE_ARCHITECT.md",
    "scientific": "SCIENTIFIC_REVIEWER.md",
    "historical": "HISTORICAL_REVIEWER.md",
    "mathematical": "MATHEMATICAL_REVIEWER.md",
    "citation": "CITATION_AUDITOR.md",
    "latex": "LATEX_EDITOR.md",
    "release": "RELEASE_REVIEWER.md",
    "exact": "EXACT_REPRODUCER.md",
}


def make_review_pack(slug: str, role: str, output: Path | None = None) -> Path:
    if role not in REVIEW_PROMPTS:
        raise SystemExit(
            f"Rol desconocido '{role}'. Roles: {', '.join(sorted(REVIEW_PROMPTS))}"
        )

    ai_context = make_ai_pack(slug)
    prompt_path = framework_dir() / "prompts" / REVIEW_PROMPTS[role]
    if not prompt_path.exists():
        raise SystemExit(f"No existe el prompt {prompt_path}")

    root, config = load_book(slug)
    if output is None:
        output = root / "build" / "reviews" / f"{role.upper()}_CONTEXT.md"
    output.parent.mkdir(parents=True, exist_ok=True)

    content = [
        f"# AeroBooks Review Pack — {role}",
        "",
        f"Libro: {config.get('book', {}).get('title', slug)}",
        "",
        "## ROL ESPECIALIZADO",
        "",
        prompt_path.read_text(encoding="utf-8").rstrip(),
        "",
        "## CONTEXTO CANÓNICO",
        "",
        ai_context.read_text(encoding="utf-8").rstrip(),
        "",
        "## CONTRATO DE SALIDA",
        "",
        "Cuando el rol sea de revisión, devuelve findings concretos. "
        "Si produces JSON, usa framework/schemas/review-report.schema.json. "
        "No declares PASS si quedan blockers o claims críticos pendientes.",
        "",
    ]
    output.write_text("\n".join(content), encoding="utf-8")
    return output


def replace_toml_scalar(path: Path, section: str, key: str, value: str | int) -> None:
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    current = None
    replaced = False
    serialized = str(value) if isinstance(value, int) else json.dumps(value, ensure_ascii=False)

    for i, line in enumerate(lines):
        section_match = re.match(r"\s*\[([^\]]+)\]\s*$", line)
        if section_match:
            current = section_match.group(1)
            continue
        if current == section and re.match(rf"\s*{re.escape(key)}\s*=", line):
            lines[i] = f"{key} = {serialized}"
            replaced = True
            break

    if not replaced:
        raise SystemExit(f"No se encontró [{section}] {key} en {path}")

    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def set_edition(slug: str, number: int, date_label: str | None) -> None:
    root, _ = load_book(slug)
    path = root / "book.toml"
    replace_toml_scalar(path, "book", "edition_number", number)
    replace_toml_scalar(path, "book", "edition_name", edition_name(number))
    replace_toml_scalar(path, "book", "date", date_label or current_spanish_date())
    config = load_toml(path)
    generated = write_metadata(root, config)
    print(f"✓ {slug}: {edition_name(number)}")
    print(f"✓ Metadatos sincronizados en {generated.relative_to(repo_root())}")


def doctor() -> int:
    tools = {
        "python": sys.executable,
        "latexmk": shutil.which("latexmk"),
        "biber": shutil.which("biber"),
        "makeindex": shutil.which("makeindex"),
        "git": shutil.which("git"),
    }
    ok = True
    print(f"{FRAMEWORK_NAME} {FRAMEWORK_VERSION}")
    print(f"Python {sys.version.split()[0]}")
    for name, value in tools.items():
        if value:
            print(f"✓ {name}: {value}")
        else:
            print(f"✗ {name}: no encontrado")
            if name in {"latexmk", "biber", "makeindex"}:
                ok = False
    return 0 if ok else 1


def list_books(json_output: bool = False) -> int:
    books = []
    root = repo_root() / "books"
    for config_path in sorted(root.glob("*/book.toml")):
        try:
            config = load_toml(config_path)
        except Exception as exc:
            books.append({"slug": config_path.parent.name, "error": str(exc)})
            continue
        meta = config.get("book", {})
        books.append({
            "slug": config_path.parent.name,
            "title": meta.get("title", ""),
            "edition": meta.get("edition_name", ""),
            "status": meta.get("status", ""),
        })

    if json_output:
        print(json.dumps(books, ensure_ascii=False, indent=2))
    else:
        if not books:
            print("No hay libros migrados a AeroBooks.")
            return 0
        width = max(len(b["slug"]) for b in books)
        for book in books:
            print(
                f"{book['slug']:<{width}}  "
                f"{book.get('edition', ''):<20}  "
                f"{book.get('status', ''):<12}  "
                f"{book.get('title', '')}"
            )
    return 0


def cmd_new(args: argparse.Namespace) -> int:
    target = copy_template(args.slug, args.title, args.subtitle, args.author)
    print(f"✓ Libro creado: {target.relative_to(repo_root())}")
    print(f"  Siguiente paso: aerobooks ai-pack {args.slug}")
    return 0


def cmd_sync(args: argparse.Namespace) -> int:
    root, config = load_book(args.slug)
    path = write_metadata(root, config)
    print(f"✓ {path.relative_to(repo_root())}")
    return 0


def cmd_check(args: argparse.Namespace) -> int:
    report = static_check(args.slug, strict=args.strict)
    print_report(report, strict=args.strict, json_output=args.json)
    return 0 if report.ok(strict=args.strict) else 1


def cmd_audit(args: argparse.Namespace) -> int:
    report = static_check(args.slug, strict=True)
    print_report(report, strict=True, json_output=False)
    if not report.ok(strict=True):
        return 1
    if args.no_build:
        return 0
    return run_build(args.slug)


def cmd_build(args: argparse.Namespace) -> int:
    if not args.skip_check:
        report = static_check(args.slug, strict=False)
        print_report(report, strict=False, json_output=False)
        if report.errors:
            return 1
    return run_build(args.slug)


def cmd_ai_pack(args: argparse.Namespace) -> int:
    output = Path(args.output) if args.output else None
    path = make_ai_pack(args.slug, output=output)
    print(f"✓ AI context: {path}")
    return 0


def cmd_review_pack(args: argparse.Namespace) -> int:
    output = Path(args.output) if args.output else None
    path = make_review_pack(args.slug, args.role, output=output)
    print(f"✓ Review context: {path}")
    return 0


def cmd_edition(args: argparse.Namespace) -> int:
    set_edition(args.slug, args.number, args.date)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="aerobooks",
        description="Framework editorial reproducible para libros académicos en LaTeX.",
    )
    parser.add_argument("--version", action="version", version=FRAMEWORK_VERSION)
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("new", help="Crear un libro desde la plantilla estándar.")
    p.add_argument("slug")
    p.add_argument("--title", required=True)
    p.add_argument("--subtitle", default="Manual académico")
    p.add_argument("--author", default="Daniel Miguel Tejedor")
    p.set_defaults(func=cmd_new)

    p = sub.add_parser("list", help="Listar libros gestionados por AeroBooks.")
    p.add_argument("--json", action="store_true")
    p.set_defaults(func=lambda args: list_books(args.json))

    p = sub.add_parser("sync", help="Generar metadatos LaTeX desde book.toml.")
    p.add_argument("slug")
    p.set_defaults(func=cmd_sync)

    p = sub.add_parser("check", help="Ejecutar comprobaciones estáticas.")
    p.add_argument("slug")
    p.add_argument("--strict", action="store_true")
    p.add_argument("--json", action="store_true")
    p.set_defaults(func=cmd_check)

    p = sub.add_parser("build", help="Comprobar y compilar un libro.")
    p.add_argument("slug")
    p.add_argument("--skip-check", action="store_true")
    p.set_defaults(func=cmd_build)

    p = sub.add_parser("audit", help="Quality gate estricto y compilación.")
    p.add_argument("slug")
    p.add_argument("--no-build", action="store_true")
    p.set_defaults(func=cmd_audit)

    p = sub.add_parser("ai-pack", help="Generar contexto canónico para una IA.")
    p.add_argument("slug")
    p.add_argument("--output")
    p.set_defaults(func=cmd_ai_pack)

    p = sub.add_parser("review-pack", help="Generar contexto especializado para una IA revisora.")
    p.add_argument("slug")
    p.add_argument(
        "role",
        choices=sorted(REVIEW_PROMPTS),
        help="Rol: author/source/outline/scientific/historical/mathematical/citation/latex/release/exact",
    )
    p.add_argument("--output")
    p.set_defaults(func=cmd_review_pack)

    p = sub.add_parser("edition", help="Cambiar la edición editorial del libro.")
    p.add_argument("slug")
    p.add_argument("number", type=int)
    p.add_argument("--date")
    p.set_defaults(func=cmd_edition)

    p = sub.add_parser("doctor", help="Comprobar dependencias locales.")
    p.set_defaults(func=lambda args: doctor())

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return int(args.func(args))


if __name__ == "__main__":
    raise SystemExit(main())
