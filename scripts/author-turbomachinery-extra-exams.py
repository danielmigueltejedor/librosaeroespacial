#!/usr/bin/env python3
"""Genera los simulacros adicionales C, D y E de Turbomáquinas (enunciados, soluciones y operaciones)."""
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
import extra_exam_lib as lib  # noqa: E402

BOOK = ROOT / 'books/turbomaquinas'


def main() -> None:
    done = lib.render(
        BOOK,
        files=dict(statements='publication/simulacros-adicionales.tex',
                   solutions='publication/soluciones-simulacros-adicionales.tex'),
        section=r'\section{Simulacro {N}}', input_prefix='../',
        report='reports/exam-solution-procedures-extra.json',
        statement_marker='', solution_marker='',
        solutions_head='\\chapter{Soluciones de los simulacros adicionales C a E}\nLas cifras se calculan con las operaciones mostradas; son aritmética reproducida de datos docentes, sin aprobación académica independiente.\n\n')
    lib.include_once(BOOK / 'publication/simulacros-originales.tex', r'\input{simulacros-adicionales.tex}', r'\end{document}')
    lib.include_once(BOOK / 'publication/problemas-resueltos.tex', r'\input{soluciones-simulacros-adicionales.tex}', r'\begin{thebibliography}')
    print('simulacros adicionales', done)


if __name__ == '__main__':
    main()
