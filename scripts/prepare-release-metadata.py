#!/usr/bin/env python3
"""Prepare reproducible release metadata, release notes and asset checksums."""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re
import zipfile

STABLE_TAG = re.compile(r"v(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\Z")
COMMIT_SHA = re.compile(r"[0-9a-f]{40}\Z")
DISCLAIMER = (
    "Edición de estudio independiente. La publicación estable del paquete "
    "acredita integridad de los ficheros, no una certificación científica "
    "ni la aprobación de la Universidad de León."
)


def validate_tag(tag: str) -> str:
    if not STABLE_TAG.fullmatch(tag):
        raise ValueError("Stable tags must use vMAJOR.MINOR.PATCH (for example v1.0.0)")
    return tag


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def prepare(tag: str, commit: str, bundle: Path, source: Path,
            output_dir: Path, published_at: datetime | None = None) -> dict:
    validate_tag(tag)
    if not COMMIT_SHA.fullmatch(commit):
        raise ValueError("A full 40-character commit SHA is required")
    if not bundle.is_file() or not source.is_file():
        raise ValueError("The complete PDF bundle and source archive are required")
    if not zipfile.is_zipfile(bundle):
        raise ValueError("Not a valid bundle ZIP")
    with zipfile.ZipFile(bundle) as archive:
        inventory = json.loads(archive.read("INVENTARIO.json"))
    if inventory["pdf_count"] != len(inventory["files"]):
        raise ValueError("Incomplete bundle manifest")
    if not inventory["pdf_count"]:
        raise ValueError("Empty release bundle")

    now = published_at or datetime.now(timezone.utc)
    if now.tzinfo is None:
        raise ValueError("Publication time must be timezone-aware")
    now = now.astimezone(timezone.utc)
    date = now.strftime("%d/%m/%Y")
    title = f"Edición {date}"
    assets = {
        bundle.name: {"sha256": sha256_file(bundle), "bytes": bundle.stat().st_size},
        source.name: {"sha256": sha256_file(source), "bytes": source.stat().st_size},
    }
    record = {
        "schema_version": 1,
        "tag": tag,
        "title": title,
        "published_at_utc": now.isoformat(timespec="seconds"),
        "commit_sha": commit,
        "pdf_count": inventory["pdf_count"],
        "topics": inventory["topics"],
        "assets": assets,
        "academic_certification": False,
        "notice": DISCLAIMER,
    }
    output_dir.mkdir(parents=True, exist_ok=True)
    release_json = output_dir / "RELEASE.json"
    release_json.write_text(json.dumps(record, ensure_ascii=False, indent=2) + "\n",
                            encoding="utf-8")
    notes = [
        f"# {title}", "",
        f"**Versión:** `{tag}`",
        f"**Fecha de publicación (UTC):** {date}",
        f"**Commit de origen (Git SHA):** `{commit}`", "",
        f"**Contenido:** {inventory['pdf_count']} PDF en el ZIP completo; "
        "manuales, problemas, simulacros y demás colecciones registradas.",
        "Las carpetas están organizadas por asignatura/tema. `INVENTARIO.json` "
        "detalla el SHA-256 de cada PDF.", "",
        "## Archivos e integridad", "",
    ]
    for name, data in assets.items():
        notes.append(f"- `{name}` — SHA-256: `{data['sha256']}`")
    notes += [
        "", "`SHA256SUMS.txt` permite verificar las descargas. "
        "`RELEASE.json` conserva la fecha UTC, el commit, los nombres y hashes.",
        "GitHub también ofrece automáticamente **Source code (zip)** y "
        "**Source code (tar.gz)** del tag.", "",
        "## Estado académico", "", DISCLAIMER, "",
    ]
    notes_file = output_dir / "NOTAS-EDICION.md"
    notes_file.write_text("\n".join(notes), encoding="utf-8")
    checksummed = [bundle, source, release_json, notes_file]
    checksum = output_dir / "SHA256SUMS.txt"
    checksum.write_text("".join(f"{sha256_file(p)}  {p.name}\n" for p in checksummed),
                        encoding="utf-8")
    return record


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--tag", required=True)
    parser.add_argument("--commit", required=True)
    parser.add_argument("--bundle", type=Path, required=True)
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--github-output", type=Path)
    args = parser.parse_args()
    record = prepare(args.tag, args.commit, args.bundle, args.source, args.output_dir)
    if args.github_output:
        with args.github_output.open("a", encoding="utf-8") as output:
            output.write(f"title={record['title']}\n")
    print(json.dumps({"title": record["title"], "tag": record["tag"],
                      "pdf_count": record["pdf_count"], "commit": record["commit_sha"]},
                     ensure_ascii=False))


if __name__ == "__main__":
    main()
