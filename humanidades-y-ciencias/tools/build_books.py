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
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent
ROOT = HERE.parent
DIST = ROOT / 'dist' / 'humanidades-y-ciencias'


def projects() -> list[str]:
    return sorted(p.parent.name for p in HERE.glob('*/project.toml'))


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
        log = (stage / 'latex/draft.log').read_text(errors='replace')
        fatal = re.findall(r'^!.*|Missing character:.*|(?:Reference|Citation) [^\n]*undefined', log, re.M)
        if fatal:
            raise RuntimeError(f'{slug}: composition errors: {fatal[:10]}')
        pdf = stage / 'latex/draft.pdf'
        DIST.mkdir(parents=True, exist_ok=True)
        target = DIST / f'{slug}.pdf'
        shutil.copyfile(pdf, target)
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
