#!/usr/bin/env python3
"""Fail closed on catalog gaps; assemble and reopen a complete subject-organized ZIP."""
from __future__ import annotations
import argparse
import hashlib
import io
import json
import os
import tempfile
import zipfile
from pathlib import Path, PurePosixPath

ROOT = Path(__file__).resolve().parents[1]


def catalog(root: Path) -> list[dict]:
    entries = json.loads((root / 'release-bundle.json').read_text())['entries']
    required = set()
    for spec_path in (root / 'books').glob('*/studium-import.json'):
        spec = json.loads(spec_path.read_text())
        required.update(f'dist/studium/{spec_path.parent.name}/{d["output"]}' for d in spec['documents'])
    required.update(f'enciclopedia-programacion/dist/review/{v.name}.pdf'
                    for v in (root / 'enciclopedia-programacion/volumes').glob('vol*') if v.is_dir())
    required.add('enciclopedia-programacion/dist/review/ENCICLOPEDIA_COMPLETA_INTEGRAL.pdf')
    required.update(f'dist/humanidades-y-ciencias/{p.parent.name}.pdf'
                    for p in (root / 'humanidades-y-ciencias').glob('*/project.toml'))
    topics = {e['topic'] for e in entries}
    for folder in (root / 'books').iterdir():
        if folder.is_dir() and (folder/'book.toml').is_file() and folder.name not in topics:
            raise ValueError('Unregistered subject: update bundle catalog and build recipe')
    sources = [e['source'] for e in entries]
    archives = [e['archive'] for e in entries]
    if set(sources) != required or len(set(sources)) != len(sources):
        raise ValueError('Catalog does not match all registered books and programming volumes')
    if len(set(archives)) != len(archives):
        raise ValueError('Duplicate archive paths')
    for e in entries:
        for key in ('source', 'archive'):
            p = PurePosixPath(e[key])
            if p.is_absolute() or '..' in p.parts or '\\' in e[key]:
                raise ValueError('Unsafe bundle path')
        if PurePosixPath(e['archive']).parts[0] != e['topic'] or len(PurePosixPath(e['archive']).parts) < 2:
            raise ValueError('Books must be grouped under their topic')
    return entries


def package(root: Path, output: Path, provenance: Path | None = None) -> dict:
    from pypdf import PdfReader
    entries = catalog(root)
    origin = json.loads(provenance.read_text()) if provenance else {}
    records = []
    for e in entries:
        p = root / e['source']
        if p.is_symlink() or not p.resolve().is_relative_to(root.resolve()) or not p.is_file():
            raise ValueError(f'Missing or unsafe PDF: {e["source"]}')
        content = p.read_bytes()
        if not content.startswith(b'%PDF-'):
            raise ValueError(f'Invalid PDF: {p}')
        reader = PdfReader(p, strict=True)
        if reader.is_encrypted or not len(reader.pages):
            raise ValueError(f'Empty or encrypted PDF: {p}')
        records.append({**e, 'sha256': hashlib.sha256(content).hexdigest(), 'bytes': len(content),
                        'pages': len(reader.pages), 'origin': origin.get(e['source'], {'type':'local-build'})})
    manifest = {'schema_version': 1, 'scope': 'delivery inventory; no academic approval implied',
                'pdf_count': len(records), 'topics': sorted({e['topic'] for e in entries}), 'files': records}
    output.parent.mkdir(parents=True, exist_ok=True)
    handle, name = tempfile.mkstemp(prefix='.bundle-', suffix='.zip', dir=output.parent)
    os.close(handle)
    temporary = Path(name)
    try:
        with zipfile.ZipFile(temporary, 'w', zipfile.ZIP_DEFLATED, compresslevel=6) as z:
            for e in records:
                data = (root / e['source']).read_bytes()
                if hashlib.sha256(data).hexdigest() != e['sha256']:
                    raise ValueError('PDF changed during packaging')
                info = zipfile.ZipInfo(e['archive'], (2026, 1, 1, 0, 0, 0))
                info.compress_type = zipfile.ZIP_DEFLATED
                info.external_attr = 0o100644 << 16
                z.writestr(info, data)
            z.writestr('INVENTARIO.json', json.dumps(manifest, ensure_ascii=False, indent=2)+'\n')
            z.writestr('LEEME.txt', 'Libros Studium\nPDF organizados por asignatura o tema.\nINVENTARIO.json documenta contenido, hashes y procedencia.\nLa inclusion no equivale a aprobacion academica; se conservan los avisos de cada libro.\n')
        verify(temporary, entries)
        os.replace(temporary, output)
    finally:
        temporary.unlink(missing_ok=True)
    return manifest


def verify(path: Path, entries: list[dict]) -> dict:
    from pypdf import PdfReader
    from pypdf.errors import PdfReadError
    with zipfile.ZipFile(path) as z:
        if z.testzip():
            raise ValueError('ZIP integrity failure')
        expected = {e['archive'] for e in entries}
        if len(z.namelist()) != len(set(z.namelist())) or set(z.namelist()) != expected | {'INVENTARIO.json','LEEME.txt'}:
            raise ValueError('Missing, duplicate or unexpected bundle members')
        manifest = json.loads(z.read('INVENTARIO.json'))
        files = manifest['files']
        if len(files) != len(entries) or {e['archive'] for e in files} != expected:
            raise ValueError('Incomplete inventory')
        by_archive = {e['archive']: e for e in entries}
        if set(manifest['topics']) != {e['topic'] for e in entries}:
            raise ValueError('Incorrect subject inventory')
        for e in files:
            if any(e[key] != by_archive[e['archive']][key] for key in ('source', 'topic')):
                raise ValueError('Incorrect PDF catalog mapping')
            data = z.read(e['archive'])
            if hashlib.sha256(data).hexdigest() != e['sha256'] or len(data) != e['bytes']:
                raise ValueError('PDF checksum mismatch')
            if not data.startswith(b'%PDF-'):
                raise ValueError('Invalid PDF member')
            try:
                reader = PdfReader(io.BytesIO(data), strict=True)
                if reader.is_encrypted or len(reader.pages) != e['pages'] or not len(reader.pages):
                    raise ValueError('Invalid PDF page inventory')
            except PdfReadError as error:
                raise ValueError('Invalid PDF member') from error
        if manifest['pdf_count'] != len(entries):
            raise ValueError('Incorrect count')
        return manifest


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=ROOT)
    parser.add_argument('--output', type=Path, default=ROOT/'dist/release/LibrosStudium-bundle-completo.zip')
    parser.add_argument('--provenance', type=Path)
    parser.add_argument('--verify-only', action='store_true')
    args = parser.parse_args()
    result = verify(args.output, catalog(args.root)) if args.verify_only else package(args.root, args.output, args.provenance)
    print(json.dumps({'pdf_count': result['pdf_count'], 'topics': result['topics'], 'zip': str(args.output)}))
