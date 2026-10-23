#!/usr/bin/env python3
"""Genera los simulacros S07 a S10 de Materiales y Mantenimiento (decimales con punto)."""
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
import extra_exam_lib as lib  # noqa: E402

BOOK = ROOT / 'books/materiales-mantenimiento-motores'


def main() -> None:
    done = lib.render(
        BOOK,
        files=dict(statements='content/simulacros-extra-enunciados.tex',
                   solutions='content/simulacros-extra-soluciones.tex'),
        section=r'\chapter{Soluciones de {N}}', input_prefix='',
        report='reports/exam-solution-procedures-extra.json')
    lib.include_once(BOOK / 'simulacros.tex', r'\input{content/simulacros-extra-enunciados.tex}',
                     r'\part{Soluciones y criterios de corrección}')
    lib.include_once(BOOK / 'simulacros.tex', r'\input{content/simulacros-extra-soluciones.tex}', r'\backmatter')
    print('simulacros adicionales', done)


if __name__ == '__main__':
    main()
