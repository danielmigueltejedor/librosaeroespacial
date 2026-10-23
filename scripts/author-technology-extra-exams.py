#!/usr/bin/env python3
"""Genera los simulacros 4 a 8 de Tecnología Aeroespacial con sus operaciones.

Los datos y las operaciones viven en `books/tecnologia-aeroespacial/solutions/
extra_exams_steps.py`; el texto, en `extra_exams_text.py`. Todas las cifras de las
soluciones se calculan aquí con `solution_steps.py` y se escriben en el texto.
Es aritmética reproducida de ejercicios originales, sin aprobación académica.
"""
from pathlib import Path
import json
import sys

ROOT = Path(__file__).resolve().parents[1]
BOOK = ROOT / 'books/tecnologia-aeroespacial'
sys.path.insert(0, str(ROOT / 'scripts'))
sys.path.insert(0, str(BOOK / 'solutions'))
from solution_steps import numeric_steps, number  # noqa: E402
import extra_exams_steps as steps  # noqa: E402
import extra_exams_text as text  # noqa: E402

INCLUDE_STATEMENTS = '\\input{../content/exam-statements-extra.tex}'
INCLUDE_SOLUTIONS = '\\input{../content/exam-solutions-extra.tex}'


def main() -> None:
    statements, solutions, reports = [], [], []
    for n in sorted(steps.STEPS):
        rows = [dict(target=k, expression=e, unit=u, why=w) for k, e, u, w in steps.STEPS[n]]
        body, checks = numeric_steps(rows)
        values = {c['target']: number(c['value'], 6) for c in checks}
        generated = (r'\subsection*{Procedimiento y operaciones del simulacro ' + str(n) + '}\n'
                     + text.STRATEGY[n] + '\n\n' + body + '\n')
        (BOOK / 'solutions/generated' / f'EX{n}.tex').write_text(generated)
        statements.append(text.STATEMENTS[n].rstrip() + '\n')
        solutions.append('\\section{Simulacro ' + str(n) + '}\n' + text.SOLUTION[n](None, values) + '\n\n'
                         + '\\input{../solutions/generated/EX' + str(n) + '.tex}\n')
        reports.append(dict(exam=n, steps=checks))
    (BOOK / 'content/exam-statements-extra.tex').write_text('\n'.join(statements))
    (BOOK / 'content/exam-solutions-extra.tex').write_text('\n'.join(solutions))
    for name, token in (('exam-statements.tex', INCLUDE_STATEMENTS), ('exam-solutions.tex', INCLUDE_SOLUTIONS)):
        path = BOOK / 'content' / name
        current = path.read_text()
        if token not in current:
            path.write_text(current.rstrip('\n') + '\n\n' + token + '\n')
    (BOOK / 'reports/exam-solution-procedures-extra.json').write_text(json.dumps(
        dict(scope='Original numeric exam data and authored derivations; no independent approval',
             records=reports), ensure_ascii=False, indent=2) + '\n')
    print('simulacros', sorted(steps.STEPS), 'escritos')


if __name__ == '__main__':
    main()
