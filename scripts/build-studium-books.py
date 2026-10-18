#!/usr/bin/env python3
"""Compile existing Studium editions without migrating their academic records."""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def imports() -> dict[str, tuple[Path, dict]]:
    return {
        p.parent.name: (p.parent, json.loads(p.read_text(encoding="utf-8")))
        for p in sorted((ROOT / "books").glob("*/studium-import.json"))
    }


def check(folder: Path, spec: dict) -> None:
    shared = set()
    for resource in spec.get("shared_resources", []):
        raw_path = ROOT / resource
        path = raw_path.resolve()
        if not path.is_relative_to((ROOT / "shared" / "latex").resolve()) or path.suffix != ".tex":
            raise ValueError(f"Recurso compartido fuera de shared/latex: {resource}")
        if not path.is_file() or raw_path.is_symlink():
            raise ValueError(f"Recurso compartido ausente o enlazado: {resource}")
        shared.add(path)
    work = (folder / spec["workdir"]).resolve()
    if not work.is_relative_to(folder.resolve()):
        raise ValueError("El directorio de compilación debe permanecer dentro del libro")
    for doc in spec["documents"]:
        source = (work / doc["source"]).resolve()
        if not source.is_relative_to(work) or not source.is_file():
            raise ValueError(f"Entrada ausente o fuera del libro: {doc['source']}")
        if Path(doc["output"]).name != doc["output"]:
            raise ValueError("El nombre de salida debe ser un archivo simple")
    for p in [*folder.rglob("*"), *shared]:
        if p.is_symlink():
            raise ValueError(f"No se admiten enlaces simbólicos: {p.relative_to(folder)}")
        if p.suffix != ".tex":
            continue
        text = p.read_text(encoding="utf-8")
        for ref in re.findall(r"\\(?:input|include|includegraphics|lstinputlisting)(?:\[[^]]*\])?\{([^}]+)\}", text):
            if "#" in ref or "\\" in ref:
                continue
            if Path(ref).is_absolute():
                raise ValueError(f"Ruta absoluta en {p.relative_to(folder)}: {ref}")
            # t1lmr.fd is a TeX distribution resource, not a manuscript input.
            if ref.endswith(".fd"):
                continue
            # TeX resolves inputs from the compilation directory, including
            # inputs written inside the shared preamble.
            target = (work / ref).resolve()
            if not target.is_relative_to(folder.resolve()) and target not in shared:
                raise ValueError(f"Dependencia fuera del libro: {ref}")
            candidates = [target, target.with_suffix(".tex"), target.with_suffix(".pdf")]
            from_parent = (p.parent / ref).resolve()
            if from_parent.is_relative_to(folder.resolve()) or from_parent in shared:
                candidates += [from_parent, from_parent.with_suffix(".tex"), from_parent.with_suffix(".pdf")]
            # includegraphics also uses the document's graphicspath.
            candidates += [folder / "figures" / ref, folder / "figures" / (ref + ".pdf")]
            if not any(x.is_file() for x in candidates):
                raise ValueError(f"Dependencia ausente en {p.relative_to(folder)}: {ref}")


def build(folder: Path, spec: dict, engine: str) -> list[dict]:
    results = []
    output = ROOT / "dist" / "studium" / folder.name
    output.mkdir(parents=True, exist_ok=True)
    for doc in spec["documents"]:
        source = Path(doc["source"])
        intermediate = output / source.stem
        intermediate.mkdir(exist_ok=True)
        for n in range(1, 4):
            command = [engine, "-no-shell-escape", "-halt-on-error", "-interaction=nonstopmode",
                       "-file-line-error", f"-output-directory={intermediate}", str(source)]
            result = subprocess.run(command, cwd=folder / spec["workdir"],
                                    stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            (intermediate / f"pass-{n}.log").write_bytes(result.stdout)
            if result.returncode:
                raise RuntimeError(f"Falló {folder.name}/{source}; consulta {intermediate}")
        log = (intermediate / source.with_suffix(".log")).read_text(errors="replace")
        if re.search(r"Overfull \\[hv]box|undefined references|undefined citations|multiply[- ]defined|Missing character:|Undefined control sequence", log):
            raise RuntimeError(f"Incidencia de composición en {folder.name}/{source}; consulta {intermediate}")
        pdf = output / doc["output"]
        shutil.copy2(intermediate / source.with_suffix(".pdf"), pdf)
        results.append({"document": doc["title"], "file": str(pdf.relative_to(ROOT)),
                        "sha256": hashlib.sha256(pdf.read_bytes()).hexdigest(), "passes": 3})
        print(f"PDF: {pdf.relative_to(ROOT)}", flush=True)
    (output / "build-report.json").write_text(json.dumps({
        "status": "compiled", "scope": "Composición LaTeX; no aprobación académica",
        "documents": results}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return results


def main() -> None:
    registry = imports()
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("book", choices=["all", *registry], nargs="?", default="all")
    parser.add_argument("--check", action="store_true", help="Comprobar entradas y dependencias sin compilar")
    args = parser.parse_args()
    selected = registry if args.book == "all" else {args.book: registry[args.book]}
    engine = shutil.which("pdflatex")
    if not args.check and engine is None:
        parser.error("Instala pdfLaTeX/TeX Live para compilar")
    for slug, (folder, spec) in selected.items():
        check(folder, spec)
        print(f"Entradas y recursos comprobados: {slug}", flush=True)
        if not args.check:
            build(folder, spec, str(engine))


if __name__ == "__main__":
    main()
