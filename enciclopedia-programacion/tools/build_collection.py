#!/usr/bin/env python3
"""Compile versioned authoring records transactionally; never regenerate them."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VOLUMES = ROOT / 'volumes'
DIST = ROOT / 'dist'


def volume_path(slug: str) -> Path:
    if not re.fullmatch(r'vol\d{2}-[a-z0-9-]+', slug):
        raise ValueError('Invalid volume slug')
    path = VOLUMES / slug
    if path.is_symlink():
        raise ValueError('Symlinked authoring roots are not supported')
    return path


def fingerprints(root: Path) -> dict[str, str]:
    return {str(p.relative_to(root)): hashlib.sha256(p.read_bytes()).hexdigest()
            for p in sorted(root.rglob('*')) if p.is_file() and p.relative_to(root).parts[0] != 'latex'
            and '__pycache__' not in p.parts}


def common_fingerprints() -> dict[str, str]:
    paths = [p for base in (ROOT / 'assets', ROOT.parent / 'shared/latex') for p in base.rglob('*') if p.is_file()]
    return {str(p.relative_to(ROOT.parent)): hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(paths)}


def atomic_copy(source: Path, target: Path) -> None:
    target.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(dir=target.parent, prefix='.' + target.name, delete=False) as handle:
        temporary = Path(handle.name)
    try:
        shutil.copyfile(source, temporary)
        os.replace(temporary, target)
    finally:
        temporary.unlink(missing_ok=True)


def compile_volume(slug: str, *, review_copy: bool = False) -> dict[str, object]:
    from pypdf import PdfReader
    from studium.authoring.render import render_draft

    source = volume_path(slug)
    if not (source / 'project.toml').is_file():
        raise FileNotFoundError(f'No authored volume: {slug}')
    if any(p.is_symlink() for p in source.rglob('*')):
        raise ValueError('Symlinks are not supported in authoring projects')
    before = fingerprints(source)
    shared_before = common_fingerprints()
    # Same directory depth as volumes/<slug>, so all versioned relative inputs
    # resolve identically. Only the temporary candidate is modified by Studium.
    with tempfile.TemporaryDirectory(prefix='.build-', dir=ROOT) as temp:
        stage = Path(temp) / slug
        shutil.copytree(source, stage, ignore=shutil.ignore_patterns('latex', '__pycache__'))
        epoch = json.loads((ROOT / 'build-config.json').read_text())['source_date_epoch']
        previous_epoch = os.environ.get('SOURCE_DATE_EPOCH')
        previous_force = os.environ.get('FORCE_SOURCE_DATE')
        try:
            os.environ['SOURCE_DATE_EPOCH'] = str(epoch)
            os.environ['FORCE_SOURCE_DATE'] = '1'
            rendered = render_draft(stage, include_unsupported=review_copy)
        finally:
            for key, value in [('SOURCE_DATE_EPOCH', previous_epoch), ('FORCE_SOURCE_DATE', previous_force)]:
                if value is None:
                    os.environ.pop(key, None)
                else:
                    os.environ[key] = value
        if rendered.get('status') != 'rendered':
            for diagnostic in (stage / 'latex').glob('*.log'):
                atomic_copy(diagnostic, DIST / 'review/failures' / slug / diagnostic.name)
            raise RuntimeError(f'{slug}: {rendered}')
        pdf = stage / 'latex/draft.pdf'
        log = (stage / 'latex/draft.log').read_text(errors='replace')
        fatal = re.findall(r'^!.*|Overfull \\[hv]box[^\n]*|Missing character:.*|(?:Reference|Citation) [^\n]*undefined', log, re.M)
        if fatal:
            raise RuntimeError(f'{slug}: composition errors: {fatal[:10]}')
        if fingerprints(source) != before or common_fingerprints() != shared_before:
            raise RuntimeError('Authoring changed during compilation; previous outputs preserved')
        pages = len(PdfReader(pdf).pages)
        report = {'slug': slug, 'status': 'review_copy' if review_copy else 'compiled', 'pages': pages,
                  'overfull_boxes': log.count('Overfull'), 'underfull_boxes': log.count('Underfull'),
                  'academic_approval': False, 'review_copy': review_copy, 'authoring_unchanged': True,
                  'inputs': before, 'shared_inputs': shared_before, 'pdf_sha256': hashlib.sha256(pdf.read_bytes()).hexdigest()}
        # Review copies have their own directory and never replace release artifacts.
        target = DIST / 'review' / f'{slug}.pdf'
        atomic_copy(pdf, target)
        for suffix in ('tex', 'toc', 'log', 'quality.json', 'quality.md'):
            artifact = stage / 'latex' / ('draft.' + suffix)
            if artifact.is_file():
                atomic_copy(artifact, DIST / 'review' / slug / artifact.name)
        (DIST / 'review' / slug / 'build.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
        return report


def generate_new_volume(spec: dict, generator) -> dict:
    """Create only a previously absent project; failures leave no partial target."""
    import studium_volume_helper as helper

    slug = str(spec['slug'])
    target = volume_path(slug)
    if target.exists():
        raise FileExistsError('Existing records must be revised append-only, never regenerated')
    old_volumes, old_dist = helper.VOLUMES_DIR, helper.DIST_DIR
    with tempfile.TemporaryDirectory(prefix='.generate-', dir=ROOT) as temp:
        try:
            helper.VOLUMES_DIR = Path(temp) / 'volumes'
            helper.DIST_DIR = Path(temp) / 'dist'
            result = generator(spec)
            if target.exists():
                raise FileExistsError('Volume appeared during generation; publication refused')
            candidate = helper.VOLUMES_DIR / slug
            target.parent.mkdir(parents=True, exist_ok=True)
            candidate.rename(target)
            return result
        finally:
            helper.VOLUMES_DIR, helper.DIST_DIR = old_volumes, old_dist


def build_all(*, review_copy: bool = False) -> list[dict]:
    reports = [compile_volume(p.name, review_copy=review_copy) for p in sorted(VOLUMES.glob('vol*')) if p.is_dir()]
    assemble_integral(reports)
    (DIST / 'review/build-summary.json').write_text(json.dumps(reports, ensure_ascii=False, indent=2) + '\n')
    return reports


def assemble_integral(reports: list[dict]) -> None:
    from pypdf import PdfReader, PdfWriter
    from pdf_assembly import namespace_destinations

    with tempfile.TemporaryDirectory(prefix='.integral-', dir=ROOT) as temp:
        candidate = Path(temp) / 'integral.pdf'
        writer = PdfWriter()
        for report in reports:
            if fingerprints(volume_path(report['slug'])) != report['inputs'] or common_fingerprints() != report.get('shared_inputs', {}):
                raise RuntimeError('Authoring or shared assets changed; rebuild volumes before assembling')
            pdf = DIST / 'review' / (report['slug'] + '.pdf')
            if hashlib.sha256(pdf.read_bytes()).hexdigest() != report['pdf_sha256']:
                raise RuntimeError('Volume PDF differs from the build manifest')
            reader = PdfReader(pdf)
            reader = namespace_destinations(reader, report['slug'])
            writer.append(reader, outline_item=report['slug'])
        writer.write(candidate)
        final = PdfReader(candidate)
        if len(final.pages) != sum(r['pages'] for r in reports):
            raise RuntimeError('Integral page count does not match its volumes')
        atomic_copy(candidate, DIST / 'review/ENCICLOPEDIA_COMPLETA_INTEGRAL.pdf')



def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('volume', help='volume slug or all')
    parser.add_argument('--review-copy', action='store_true', help='Include unsupported drafts with a visible evidence warning')
    parser.add_argument('--merge-only', action='store_true', help='Assemble already verified volume artifacts')
    args = parser.parse_args()
    if args.merge_only:
        reports = json.loads((DIST / 'review/build-summary.json').read_text())
        assemble_integral(reports)
        return
    reports = build_all(review_copy=args.review_copy) if args.volume == 'all' else [compile_volume(args.volume, review_copy=args.review_copy)]
    print(json.dumps([{k: v for k, v in r.items() if k != 'inputs'} for r in reports], ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
