"""Escribe simulacros adicionales: enunciados, soluciones con cifras calculadas y operaciones.

Cada libro aporta dos módulos en `books/<libro>/solutions/`: `extra_exams_steps.py`
(`STEPS[n]`: filas `(destino, expresión, unidad, motivo)`) y `extra_exams_text.py`
(`STATEMENTS[n]`, `STRATEGY[n]`, `SOLUTION[n](valores)`). Las cifras se calculan con
`solution_steps.py`; es aritmética reproducida de datos docentes, no una revisión.
"""
from pathlib import Path
import json
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from solution_steps import numeric_steps, number  # noqa: E402


def load(book: Path):
    sys.path.insert(0, str(book / 'solutions'))
    for name in ('extra_exams_steps', 'extra_exams_text'):
        sys.modules.pop(name, None)
    import extra_exams_steps as steps  # noqa: E402
    import extra_exams_text as text  # noqa: E402
    return steps, text


def render(book: Path, *, files: dict, section: str, input_prefix: str, report: str,
           statement_marker: str, solution_marker: str, solutions_head: str = '') -> list[int]:
    """files: nombres de salida relativos al libro. section: comando de sección de la solución."""
    steps, text = load(book)
    statements, solutions, reports = [], [], []
    for n in sorted(steps.STEPS):
        rows = [dict(target=k, expression=e, unit=u, why=w) for k, e, u, w in steps.STEPS[n]]
        body, checks = numeric_steps(rows)
        values = {c['target']: number(c['value'], 6) for c in checks}
        generated = (r'\subsection*{Procedimiento y operaciones del simulacro ' + text.LABEL[n] + '}\n'
                     + text.STRATEGY[n] + '\n\n' + body + '\n')
        (book / 'solutions/generated' / f'EX{n}.tex').write_text(generated)
        statements.append(text.STATEMENTS[n].rstrip() + '\n')
        solutions.append(section.replace('{N}', text.LABEL[n]) + '\n' + text.SOLUTION[n](values) + '\n\n'
                         + '\\input{' + input_prefix + 'solutions/generated/EX' + str(n) + '.tex}\n')
        reports.append(dict(exam=n, steps=checks))
    (book / files['statements']).write_text('\n'.join(statements))
    (book / files['solutions']).write_text(solutions_head + '\n'.join(solutions))
    (book / report).write_text(json.dumps(
        dict(scope='Original numeric exam data and authored derivations; no independent approval',
             records=reports), ensure_ascii=False, indent=2) + '\n')
    return sorted(steps.STEPS)


def include_once(path: Path, token: str, before: str | None = None) -> None:
    current = path.read_text()
    if token in current:
        return
    if before and before in current:
        path.write_text(current.replace(before, token + '\n' + before, 1))
    else:
        path.write_text(current.rstrip('\n') + '\n\n' + token + '\n')
