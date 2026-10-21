#!/usr/bin/env python3
"""Audit all active literal regions and round-trip escaping fixtures through the actual PDF."""
import hashlib
import json
import re
import shutil
import subprocess
import tempfile
from pathlib import Path

from studium.authoring.languages import book_language, messages
from studium.authoring.literals import code_regions
from studium.authoring.render import _compile, _preamble, emit_prose, find_engine, render_text_run
from studium.storage.records import fold_by_id
ROOT=Path(__file__).resolve().parents[1]
FIXTURES=[
    ('python',r'''path = "C:\\work\\file_name.txt"
pattern = r"\b[a-z_]+\b"
value = "\U0001f980"
text = "áéíóú ñ ü"
operators = "<= >= != == & | ^ ~ % # $ { } [ ] _"
quote = 'single and "double"'
literal = "\\end{lstlisting}"
markers = "(*@ @*) (#@ @#) (|@ @|) [<@ @>]"'''),
    ('javascript',r'''const tpl = `Hello ${user_name}`;
const re = /[a-z_]+\s*/gu;
const ok = left <= right && a !== b;'''),
    ('rust',r'''fn borrow<'a>(xs: &'a [u8]) -> &'a [u8] { xs }
// α β ≤ ≥ ≠''')]


def normalize(text):
    return re.sub(r'\s+','',text)


def main():
    findings=[];regions=0;records=0
    for volume in sorted((ROOT/'volumes').glob('vol*')):
        for relative in ['draft/paragraphs.jsonl','problems/problems.jsonl']:
            for record in fold_by_id(volume/relative):
                texts=[record.get('text',''),record.get('prompt',''),record.get('solution',{}).get('text','')]
                for text in texts:
                    if not text:continue
                    records+=1
                    for region in code_regions(text):
                        regions+=1
                        if region.block and not region.closed:
                            findings.append({'volume':volume.name,'id':record['id'],'issue':'unclosed fence'})
                        if any(ord(c)<32 and c not in '\n\r\t' for c in region.body):
                            findings.append({'volume':volume.name,'id':record['id'],'issue':'control character in literal'})
                    try: emit_prose(text)
                    except ValueError as error:
                        findings.append({'volume':volume.name,'id':record['id'],'issue':str(error)})
    if findings:raise RuntimeError(json.dumps(findings,ensure_ascii=False))
    language=book_language(next((ROOT/'volumes').glob('vol03-*')))
    lines=[*_preamble('Literal fidelity fixture',language,messages(language)),r'\begin{document}',r'\chapter*{Fidelidad del código}']
    for i,(lang,source) in enumerate(FIXTURES):
        lines.extend([f'BEGINFIXTURE{i}',*emit_prose(f'```{lang}\n{source}\n```'),f'ENDFIXTURE{i}'])
    inline=r'a_b%#$&{}^~\path/file <= >= "quoted"'
    lines += ['BEGININLINE',render_text_run('`'+inline+'`'),'ENDINLINE',r'\end{document}']
    emphasis = '**Rust (`vol03`)**: *data races*. **$2\\text{ KiB}$**. **`0` significa éxito**. **`Monad`**.'
    lines[-1:-1] = ['BEGINEMPHASIS', *emit_prose(emphasis), 'ENDEMPHASIS']
    checks=[]
    with tempfile.TemporaryDirectory(prefix='.literal-',dir=ROOT) as temporary:
        tex=Path(temporary)/'literal.tex';tex.write_text('\n'.join(lines))
        ok,detail=_compile(find_engine(),tex,tex.parent)
        if not ok:raise RuntimeError(detail)
        result=subprocess.run(['pdftotext','-enc','UTF-8',str(tex.with_suffix('.pdf')),'-'],capture_output=True,text=True,check=True).stdout
        for i,(_,source) in enumerate(FIXTURES):
            actual=result.split(f'BEGINFIXTURE{i}',1)[1].split(f'ENDFIXTURE{i}',1)[0]
            checks.append({'fixture':i,'matches_without_layout_whitespace':normalize(actual)==normalize(source),'expected':source,'actual':actual.strip()})
        actual=result.split('BEGININLINE',1)[1].split('ENDINLINE',1)[0]
        checks.append({'fixture':'inline','matches_without_layout_whitespace':normalize(actual)==normalize(inline),'expected':inline,'actual':actual.strip()})
        actual=result.split('BEGINEMPHASIS',1)[1].split('ENDEMPHASIS',1)[0]
        expected='Rust (vol03): data races. 2 KiB. 0 significa éxito. Monad.'
        checks.append({'fixture':'emphasis_across_literals_and_math',
                       'matches_without_layout_whitespace':normalize(actual)==normalize(expected),
                       'expected':expected,'actual':actual.strip()})
        log=tex.with_suffix('.log').read_text(errors='replace')
        if 'Overfull' in log or 'Missing character:' in log:raise RuntimeError('Fixture composition failure')
        shutil.copyfile(tex.with_suffix('.pdf'),ROOT/'dist/review/literal-fidelity-specimen.pdf')
    report={'scope':'all active prose/solution literal regions checked for unsupported glyphs, controls and fences; PDF fixture text compared without layout whitespace; exact editable source is shipped separately',
            'records_checked':records,'literal_regions_checked':regions,'issues':findings,'roundtrip':checks,
            'pdf_sha256':hashlib.sha256((ROOT/'dist/review/literal-fidelity-specimen.pdf').read_bytes()).hexdigest()}
    (ROOT/'reports/literal-fidelity.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    if not all(c['matches_without_layout_whitespace'] for c in checks):raise RuntimeError('PDF literal extraction differs; inspect literal-fidelity.json')
    print(f'{regions} literal regions; {len(checks)} PDF round-trips passed')


if __name__=='__main__':main()
