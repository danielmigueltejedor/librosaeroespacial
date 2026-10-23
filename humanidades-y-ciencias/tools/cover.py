#!/usr/bin/env python3
"""Compose the shared Studium cover for a project and put it in place of the draft title page."""
from __future__ import annotations

import json
import shutil
import subprocess
import tempfile
from pathlib import Path

from pypdf import PdfReader, PdfWriter

HERE = Path(__file__).resolve().parent.parent
SHARED = HERE.parent / 'shared' / 'latex'


def _tex_escape(text: str) -> str:
    for a, b in (('&', r'\&'), ('%', r'\%'), ('#', r'\#'), ('_', r'\_')):
        text = text.replace(a, b)
    return text


def credit_line(meta: dict) -> str:
    author = _tex_escape(meta['author'])
    return (f"Imagen de portada: {_tex_escape(meta['description'])} {author}, {_tex_escape(meta['licence'])}, "
            f"vía Wikimedia Commons.")


def cover_pdf(slug: str, target: Path) -> Path:
    folder = HERE / slug / 'cover'
    meta = json.loads((folder / 'cover.json').read_text())
    with tempfile.TemporaryDirectory(prefix='.cover-') as temp:
        work = Path(temp)
        photo = work / 'cover.jpg'
        shutil.copyfile(folder / meta['file'], photo)
        tex = work / 'cover.tex'
        tex.write_text('\n'.join([
            r'\documentclass[10pt]{book}',
            r'\newcommand{\studiumsharedroot}{' + SHARED.as_posix() + '}',
            r'\input{' + (SHARED / 'studium-editorial.tex').as_posix() + '}',
            r'\renewcommand{\studiumcoverphoto}{cover.jpg}',
            r'\renewcommand{\studiumcovercollection}{BIBLIOTECA DE HUMANIDADES Y CIENCIAS}',
            r'\renewcommand{\studiumcoverdiscipline}{' + _tex_escape(meta['discipline']) + '}',
            r'\renewcommand{\studiumcoverinstitution}{Studium}',
            r'\renewcommand{\studiumcoveredition}{Primera edición}',
            r'\renewcommand{\studiumcovercredit}{' + credit_line(meta) + '}',
            r'\hypersetup{pdftitle={' + _tex_escape(meta['title'].replace('\\\\', ' ')) + '}}',
            r'\begin{document}',
            r'\studiumcover{' + _tex_escape(meta['title']) + '}{' + _tex_escape(meta['subtitle']) + '}{' + _tex_escape(meta['category']) + '}',
            r'\end{document}', ''
        ]), encoding='utf-8')
        for _ in range(2):
            run = subprocess.run(['pdflatex', '-interaction=nonstopmode', '-halt-on-error', 'cover.tex'], cwd=work,
                                 capture_output=True, text=True, errors='replace', check=False)
            if run.returncode:
                raise RuntimeError(f'{slug}: cover did not compile:\n' + run.stdout[-1500:])
        shutil.copyfile(work / 'cover.pdf', target)
    return target


def replace_title_page(slug: str, book_pdf: Path) -> None:
    """The draft title page is page 1; the cover takes its place so pagination is unchanged."""
    with tempfile.TemporaryDirectory(prefix='.cover-pdf-') as temp:
        cover = cover_pdf(slug, Path(temp) / 'cover.pdf')
        writer = PdfWriter()
        for page in PdfReader(cover).pages[:1]:
            writer.add_page(page)
        reader = PdfReader(book_pdf)
        for page in reader.pages[1:]:
            writer.add_page(page)
        if reader.outline:
            writer.add_outline_item('Portada', 0)
        writer.add_metadata({k: v for k, v in (reader.metadata or {}).items()})
        out = Path(temp) / 'merged.pdf'
        with out.open('wb') as handle:
            writer.write(handle)
        shutil.copyfile(out, book_pdf)
