#!/usr/bin/env python3
"""Reproducible rendering matrix; these are display fixtures, not executed programs."""
import hashlib
import json
import tempfile
from pathlib import Path

from studium.authoring.languages import book_language, messages
from studium.authoring.render import _compile, _preamble, emit_prose, find_engine

ROOT = Path(__file__).resolve().parents[1]
FIXTURES = {
    'rust': "fn choose<'a, T: Ord>(items: &'a [T]) -> Option<&'a T> {\n    items.iter().max()\n}\n",
    'c': '#include <stdint.h>\nuint32_t mask(uint32_t x) { return (x << 2) & 0xffu; }\n',
    'cpp': 'template<class T> auto twice(T x) { return [x] { return x + x; }; }\n',
    'csharp': 'var names = new[] { "Ada", "Grace" };\nvar selected = names.Where(name => name.Length > 3);\n',
    'python': '@decorator\ndef café(data_items):\n    pattern = r"\\b[a-z_]+\\b"\n    return [x for x in data_items if x <= 3]\n',
    'java': 'var names = List.of("Ada", "Grace");\nnames.stream().filter(x -> x.length() > 3).forEach(System.out::println);\n',
    'go': 'func sum(xs []int) int {\n    total := 0\n    for _, x := range xs { total += x }\n    return total\n}\n',
    'javascript': 'const user_name = "Ada";\nconst message = `Hello ${user_name}`;\nconst matches = /[a-z_]+/gu.test(message);\n',
    'typescript': 'type Result<T> = { ok: true; value: T } | { ok: false; error: string };\n',
    'html': '<section aria-label="example"><code>data_items[0]</code></section>\n',
    'css': '.code { display: grid; grid-template-columns: 1fr 2fr; }\n',
    'json': '{"data_items": [1, 2], "enabled": true, "path": "C:\\\\work"}\n',
    'yaml': 'server:\n  ports: [8080, 8443]\n  enabled: true\n',
    'sql': 'SELECT name, COUNT(*) AS total\nFROM events GROUP BY name HAVING COUNT(*) >= 2;\n',
    'bash': 'for file in *.txt; do\n  printf "%s\\n" "$file"\ndone\n',
    'toml': '[tool.example]\nname = "data_items"\nenabled = true\n',
    'terminal': 'python -m pytest -q test_vm.py\n',
    'output': '10 passed\n',
    'error': 'SyntaxError: invalid syntax\n',
}


def main():
    language = book_language(ROOT / 'volumes/vol03-monografia-rust')
    assert language is not None
    lines = [*_preamble('Editorial rendering specimen', language, messages(language)), r'\begin{document}',
             r'\chapter*{Matriz de representación editorial}',
             'Fixtures de presentación. No se afirma ejecución o corrección de los programas parciales.']
    for name, source in FIXTURES.items():
        lines += [r'\section*{' + name + '}']
        lines += emit_prose('```' + name + '\n' + source + '```')
    long_source = '\n'.join(f'    // line {i:03}: preserve data_items[{i}] and indentation' for i in range(1, 181))
    lines += [r'\section*{Listado largo de varias páginas}']
    lines += emit_prose('```rust\nfn main() {\n' + long_source + '\n}\n```')
    lines += [r'\end{document}']
    output = ROOT / 'dist/review'
    output.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='.specimen-', dir=ROOT) as temp:
        tex = Path(temp) / 'specimen.tex'
        tex.write_text('\n'.join(lines))
        compiled, detail = _compile(find_engine(), tex, tex.parent)
        if not compiled:
            raise RuntimeError(detail)
        log = tex.with_suffix('.log').read_text(errors='replace')
        assert 'Overfull' not in log and 'Missing character:' not in log
        (output / 'editorial-specimen.pdf').write_bytes(tex.with_suffix('.pdf').read_bytes())
        report = {'scope': 'rendering only; partial fixtures not executed', 'fixtures': {k: hashlib.sha256(v.encode()).hexdigest() for k,v in FIXTURES.items()},
                  'long_listing_lines': 182, 'overfull': log.count('Overfull'), 'missing_glyphs': log.count('Missing character:')}
        (ROOT / 'reports/editorial-specimen.json').write_text(json.dumps(report,indent=2)+'\n')


if __name__ == '__main__':
    main()
