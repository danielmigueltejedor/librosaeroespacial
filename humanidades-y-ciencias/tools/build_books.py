#!/usr/bin/env python3
"""Compile the Studium projects of this folder into review PDFs under dist/.

    python humanidades-y-ciencias/tools/build_books.py [slug ...]

The authored project is never modified: it is copied to a temporary directory
and rendered there. The result is a review copy, not an approved edition.
"""
from __future__ import annotations

import hashlib
import json
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

HERE = Path(__file__).resolve().parent.parent
ROOT = HERE.parent
DIST = ROOT / 'dist' / 'humanidades-y-ciencias'


def projects() -> list[str]:
    return sorted(p.parent.name for p in HERE.glob('*/project.toml'))


def retitle_footer(stage: Path, source: Path) -> None:
    """Running footer shows the book title instead of the draft badge; the pages stay where they were."""
    cover = source / 'cover' / 'cover.json'
    if not cover.is_file():
        return
    title = json.loads(cover.read_text())['short_title']
    tex = stage / 'latex' / 'draft.tex'
    text = tex.read_text()
    text = re.sub(r'(\\fancyfoot\[C\]\{\\small )Borrador\}', lambda m: m.group(1) + title + '}', text)
    tex.write_text(text)
    for _ in range(2):
        run = subprocess.run(['pdflatex', '-interaction=nonstopmode', '-halt-on-error', 'draft.tex'], cwd=tex.parent,
                             capture_output=True, text=True, errors='replace', check=False)
        if run.returncode:
            raise RuntimeError('footer recompilation failed:\n' + run.stdout[-1500:])


def build(slug: str) -> dict[str, object]:
    from studium.authoring.render import render_draft

    source = HERE / slug
    if not (source / 'project.toml').is_file():
        raise FileNotFoundError(f'No Studium project: {slug}')
    if any(p.is_symlink() for p in source.rglob('*')):
        raise ValueError('Symlinks are not supported in authoring projects')
    with tempfile.TemporaryDirectory(prefix='.build-', dir=HERE) as temp:
        stage = Path(temp) / slug
        shutil.copytree(source, stage, ignore=shutil.ignore_patterns('latex', '__pycache__'))
        rendered = render_draft(stage)
        if rendered.get('status') != 'rendered':
            raise RuntimeError(f'{slug}: {rendered.get("status")}: {rendered.get("message")}')
        retitle_footer(stage, source)
        log = (stage / 'latex/draft.log').read_text(errors='replace')
        fatal = re.findall(r'^!.*|Missing character:.*|(?:Reference|Citation) [^\n]*undefined', log, re.M)
        if fatal:
            raise RuntimeError(f'{slug}: composition errors: {fatal[:10]}')
        pdf = stage / 'latex/draft.pdf'
        DIST.mkdir(parents=True, exist_ok=True)
        target = DIST / f'{slug}.pdf'
        shutil.copyfile(pdf, target)
        if (source / 'cover' / 'cover.json').is_file():
            from cover import replace_title_page
            replace_title_page(slug, target)
        report = {
            'slug': slug,
            'status': 'review_copy',
            'academic_approval': False,
            'overfull_boxes': log.count('Overfull'),
            'pdf_sha256': hashlib.sha256(target.read_bytes()).hexdigest(),
        }
        (DIST / f'{slug}.build.json').write_text(json.dumps(report, indent=2) + '\n')
        return report


def main(argv: list[str]) -> int:
    wanted = argv or projects()
    for slug in wanted:
        print(json.dumps(build(slug), ensure_ascii=False))
    return 0


if __name__ == '__main__':
    raise SystemExit(main(sys.argv[1:]))
