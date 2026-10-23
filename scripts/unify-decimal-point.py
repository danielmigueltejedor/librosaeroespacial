#!/usr/bin/env python3
"""Escribe los decimales con punto en los libros de ingeniería de la colección.

Las fuentes de Fluidos, Estructuras, Tecnología, Materiales y Turbomáquinas mezclaban
`9{,}81`, `9,81` y `9.81`. El resto de la colección usa punto, y el punto es la
convención mayoritaria en los problemas resueltos, así que se unifica en punto.

Reglas, que nunca tocan coordenadas de TikZ, listados ni identificadores:
1. `1{,}5` pasa a `1.5` en todo el texto (es la forma de coma decimal en modo matemático).
2. Fuera de matemáticas, TikZ y listados, una coma decimal seguida de una unidad, un
   decimal con cero entero o un decimal de al menos dos cifras (no tres) pasa a punto.
Uso: `python3 scripts/unify-decimal-point.py [--dry-run] LIBRO...`
"""
from pathlib import Path
import argparse
import re

ROOT = Path(__file__).resolve().parents[1]
SKIP_DIRS = {'figures', 'figures-originales', 'practice', 'latex-build', 'build', 'dist'}

MASK = re.compile(r'''
    \\begin\{(?P<env>tikzpicture|pgfpicture|axis|tikzcd|verbatim|lstlisting|minted|equation\*?|align\*?|gather\*?|multline\*?|eqnarray\*?|displaymath|math)\}.*?\\end\{(?P=env)\}
  | \\\[.*?\\\]
  | \\\(.*?\\\)
  | \$\$.*?\$\$
  | \$[^$\n]*\$
  | \\(?:label|ref|eqref|cref|autoref|hyperref|cite|citep|citet|input|include|includegraphics|url|href|lstinputlisting|pageref|nameref)(?:\[[^\]]*\])?\{[^}]*\}
  | \\(?:newcommand|renewcommand|def|setlength|vspace|hspace|pgfmathsetmacro|foreach)\b[^\n]*
''', re.S | re.X)

UNIT = r'(?:\\,|~|\\ |\s)?(?:mm|cm|km|m|kg|g|N|kN|MN|MPa|GPa|kPa|hPa|mPa|Pa|K|s|ms|rad|°|\\%|%|W|kW|MW|J|kJ|MJ|V|A|Hz|kHz|rpm|h|min|veces|puntos|mol|kmol|L|l|ml|mL|dB|grados|µm|μm|nm|ppm|Mach|segundos|metros)(?![A-Za-z])'
RULES = [
    re.compile(r'(?<![\w.,/{\[])(\d+),(\d+)(?=' + UNIT + ')'),
    re.compile(r'(?<![\w.,/{\[])(\d+),(\d+)(?=\s*(?:·|\\cdot|\\times|\\textsuperscript))'),
    re.compile(r'(?<![\w.,/{\[])(0),(\d+)(?![\d,]|\.\d)'),
    re.compile(r'(?<![\w.,/{\[])(\d+),(\d{2}|\d{4,})(?![\d,]|\.\d)'),
]
MATH_START = ('$', '\\(', '\\[', '\\begin{equation', '\\begin{align', '\\begin{gather', '\\begin{multline', '\\begin{displaymath')
MATH_RULE = re.compile(r'((?:=|\\approx|\\pm|\\leq?|\\geq?|<|>|\\sim)\s*[+-]?)(\d+),(\d+)(?![\d,])')
WORD_RULE = re.compile(r'(\b(?:y|a|e|o|de|por|entre|es|vale|con|hasta|unos|casi|del|al)\s)(\d+),(\d+)(?![\d,]|\.\d)')
BRACE = re.compile(r'(\d)\{,\}(\d)')


TIKZ = re.compile(r'\\begin\{tikzpicture\}.*?\\end\{tikzpicture\}', re.S)


def transform(text: str) -> str:
    # Las figuras con recibo de revisión visual (audit-figure-review.py) no se tocan.
    figures: list[str] = []
    text = TIKZ.sub(lambda m: figures.append(m.group(0)) or f'\x01{len(figures) - 1}\x01', text)
    text = BRACE.sub(r'\1.\2', text)
    holders: list[str] = []

    def hold(match: re.Match) -> str:
        holders.append(match.group(0))
        return f'\x00{len(holders) - 1}\x00'

    out_lines = []
    for line in text.split('\n'):
        out_lines.append(line)
    masked = MASK.sub(hold, '\n'.join(out_lines))
    parts = []
    for line in masked.split('\n'):
        match = re.search(r'(?<!\\)%', line)
        code, comment = (line[:match.start()], line[match.start():]) if match else (line, '')
        for rule in RULES:
            code = rule.sub(r'\1.\2', code)
        code = WORD_RULE.sub(r'\1\2.\3', code)
        parts.append(code + comment)
    masked = '\n'.join(parts)
    def restore(match: re.Match) -> str:
        part = holders[int(match.group(1))]
        if part.startswith(MATH_START):
            part = MATH_RULE.sub(r'\1\2.\3', part)
        return part
    text = re.sub(r'\x00(\d+)\x00', restore, masked)
    return re.sub(r'\x01(\d+)\x01', lambda m: figures[int(m.group(1))], text)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('books', nargs='+')
    parser.add_argument('--dry-run', action='store_true')
    args = parser.parse_args()
    changed = 0
    for book in args.books:
        for path in sorted((ROOT / 'books' / book).rglob('*.tex')):
            if SKIP_DIRS & set(path.relative_to(ROOT / 'books' / book).parts):
                continue
            old = path.read_text(encoding='utf-8')
            new = transform(old)
            if new != old:
                changed += 1
                if not args.dry_run:
                    path.write_text(new, encoding='utf-8')
                diff = sum(1 for a, b in zip(old.split('\n'), new.split('\n')) if a != b)
                print(f'{path.relative_to(ROOT)}: {diff} líneas')
    print('archivos cambiados:', changed)


if __name__ == '__main__':
    main()
