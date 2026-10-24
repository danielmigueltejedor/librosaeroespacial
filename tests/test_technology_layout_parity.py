"""The compiled Technology chapters must match their editable scientific source."""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1] / "books/tecnologia-aeroespacial"
SECTION = re.compile(
    r"\\refstepcounter\{section\}\\addcontentsline\{toc\}\{section\}"
    r"\{\\protect\\numberline\{\\thesection\}(.+)\}"
)
SOLUTION = re.compile(r"\\input\{\.\./solutions/generated/M\d\d-\d+\.tex\}")


def _normalize_layout(text, chapter):
    lines = []
    for line in text.splitlines():
        section = SECTION.fullmatch(line)
        if section:
            lines.append(r"\section{" + section.group(1) + "}")
            continue
        if (line.startswith(r"\begin{studiumworked}{")
                or line == r"\end{studiumworked}"
                or line == r"\studiumchaptercheck"
                or SOLUTION.fullmatch(line)):
            continue
        # These two paragraphs were deliberately re-typeset as display math.
        if (chapter == 11 and line.startswith(r"\paragraph{7. Ecuaciones simbólicas.}")
                or chapter == 15 and line.startswith(r"\paragraph{9. Sustitución.}")):
            continue
        lines.append(line)
    return [line for line in lines if line.strip()]


def _normalize_source(text, chapter):
    lines = text.splitlines()
    if chapter == 11:
        lines = [line for line in lines if not line.startswith(
            r"\paragraph{7. Ecuaciones simbólicas.}")]
    if chapter == 15:
        lines = [line for line in lines if not line.startswith(
            r"\paragraph{9. Sustitución.}")]
    return [line for line in lines if line.strip()]


def test_compiled_chapters_preserve_scientific_source():
    source = sorted((ROOT / "content").glob("c[0-9][0-9].tex"))
    layout = sorted((ROOT / "content-layout").glob("c[0-9][0-9].tex"))
    assert len(source) == 25
    assert [p.name for p in source] == [p.name for p in layout]
    for src, dst in zip(source, layout):
        number = int(src.stem[1:])
        original = src.read_text(encoding="utf-8")
        compiled = dst.read_text(encoding="utf-8")
        assert _normalize_source(original, number) == _normalize_layout(compiled, number), (
            f"{dst} differs from {src} beyond expected solution/layout wrappers"
        )
        assert r"\studiumchaptercheck" in compiled
        assert SECTION.search(compiled) or "\\refstepcounter{section}" in compiled


def test_layout_solution_includes_exist():
    for layout in (ROOT / "content-layout").glob("c[0-9][0-9].tex"):
        for solution in SOLUTION.findall(layout.read_text(encoding="utf-8")):
            relative = solution[len(r"\input{"):-1]
            assert (layout.parent / relative).is_file(), (layout, solution)
