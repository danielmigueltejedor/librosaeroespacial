#!/usr/bin/env python3
"""Read-only corpus inventory; counts are not academic or curricular approval."""
from __future__ import annotations

import hashlib
import base64
import json
import re
from collections import Counter
from pathlib import Path

from pypdf import PdfReader
from studium.authoring.literals import code_regions, mask_code
from studium.storage.records import fold_by_id

ROOT = Path(__file__).resolve().parents[1]


def inventory(root: Path = ROOT) -> dict:
    volumes = []
    prompts: dict[str, list[str]] = {}
    for volume in sorted((root / 'volumes').glob('vol*')):
        records = fold_by_id(volume / 'draft/paragraphs.jsonl')
        problems = fold_by_id(volume / 'problems/problems.jsonl')
        excerpts = fold_by_id(volume / 'bibliography/excerpts.jsonl')
        sources = fold_by_id(volume / 'bibliography/public.jsonl')
        pdf = root / 'dist/review' / (volume.name + '.pdf')
        generated = root / 'dist/review' / volume.name
        reader = PdfReader(pdf) if pdf.exists() else None
        pages = [p.extract_text() or '' for p in reader.pages] if reader else []
        labels = reader.page_labels if reader else []
        # latex source markers identify actual record regions, while PDF text
        # occurrence pages may also include audit appendices; keep them distinct.
        texpath = generated / 'draft.tex'
        tex = texpath.read_text() if texpath.exists() else ''
        logpath = generated / 'draft.log'
        log = logpath.read_text(errors='replace') if logpath.exists() else ''
        chapter_pages = {}
        tocpath = generated / 'draft.toc'
        toc = tocpath.read_text() if tocpath.exists() else ''
        for match in re.finditer(r'\\contentsline \{chapter\}\{(.*?)\}\{([^}]+)\}', toc):
            chapter_pages[match[1]] = match[2]
        chapter_ids = re.findall(r'\\label\{chap:([^}]+)\}', tex)
        starts = {}
        toc_pages = {int(n): page for page, n in re.findall(r'\}\{([^{}]+)\}\{chapter\.(\d+)\}', toc)}
        for number, identifier in enumerate(chapter_ids, 1):
            printed = toc_pages.get(number)
            if printed in labels:
                starts[identifier] = {'printed_page': printed, 'pdf_page': labels.index(printed) + 1}
        source_lines = {}
        for number, line in enumerate(tex.splitlines(), 1):
            if line.startswith('% studium:record '):
                record_id = json.loads(base64.b64decode(line.split()[-1]))['id']
                source_lines.setdefault(record_id, number)
        chapters = {}
        for record in records:
            section = record['section']
            chapter = chapters.setdefault(section, {'prose_words': 0, 'records': [], 'code_blocks': 0, 'review_status': 'PENDING_TECHNICAL_AND_PEDAGOGICAL_REVIEW', 'chapter_start': starts.get(section)})
            text = record['text']
            chapter['prose_words'] += len(re.findall(r'\b\w+\b', mask_code(text)))
            chapter['code_blocks'] += sum(r.block for r in code_regions(text))
            chapter['records'].append({'id': record['id'], 'source': str((volume / 'draft/paragraphs.jsonl').relative_to(root)),
                                       'text_sha256': hashlib.sha256(text.encode()).hexdigest(), 'excerpts': record.get('excerpts', []), 'generated_tex_line': source_lines.get(record['id']),
                                       'pdf_id_occurrence_pages': [i for i, t in enumerate(pages, 1) if record['id'] in t]})
        exercise_inventory = []
        for problem in problems:
            ident = volume.name + ':' + problem['id']
            key = re.sub(r'\s+', ' ', problem.get('prompt', '')).strip().lower()
            prompts.setdefault(key, []).append(ident)
            exercise_inventory.append({'id': problem['id'], 'section': problem.get('section'), 'kind': problem.get('kind'),
                                       'declared_problem_type': problem.get('problem_type'), 'correct': problem.get('correct'),
                                       'source': str((volume / 'problems/problems.jsonl').relative_to(root)), 'has_structured_solution': bool(problem.get('solution')), 'has_rust_source': problem.get('kind') == 'rust',
                                       'method_scope': 'Rust test replay' if problem.get('kind') == 'rust' else 'See learning-verification.json for the route-specific programming cases' if problem.get('kind') == 'programming' else 'numeric/excerpt check; not a programming test',
                                       'pedagogical_classification': 'manual_review_required'})
        volumes.append({'slug': volume.name, 'pdf_pages': len(pages) if pages else None, 'chapters': chapters,
                        'toc_chapter_page_labels': chapter_pages, 'sections_in_tex': len(re.findall(r'\\section\{', tex)),
                        'subsections_in_tex': len(re.findall(r'\\subsection\{', tex)),
                        'problems': exercise_inventory, 'problem_kinds': dict(Counter(p.get('kind', 'missing') for p in problems)),
                        'figures': len(fold_by_id(volume / 'figures/figures.jsonl')), 'sources': len(sources), 'excerpts': len(excerpts),
                        'source_review_pending': sum(r.get('provenance_status') in {'client_summary_unverified','client_text_unverified'} for r in excerpts),
                        'sources_inventory': [{k: r.get(k) for k in ('id','title','url','classification')} for r in sources],
                        'excerpts_inventory': [{k: r.get(k) for k in ('id','source_id','url','text_sha256','provenance_status')} for r in excerpts],
                        'active_synthetic_sources': [r['id'] for r in sources if 'Referencia Normativa' in str(r)],
                        'active_contaminated_excerpts': [r['id'] for r in excerpts if 'Fórmulas y constantes de referencia:' in str(r)],
                        'active_synthetic_urls': [r['id'] for r in sources if re.search(r'/vol-ref-\d+$', str(r.get('url', '')))],
                        'latex': {'overfull': log.count('Overfull'), 'underfull': log.count('Underfull'),
                                  'undefined': len(re.findall(r'(?:Reference|Citation).*undefined', log)),
                                  'missing_glyphs': log.count('Missing character:'), 'fatal_errors': len(re.findall(r'^!', log, re.M))}})
    return {'schema_version': 1, 'academic_approval': False, 'curricular_coverage': 'NOT_ESTABLISHED',
            'page_mapping_scope': 'PDF id occurrence pages may refer to audit appendices; printed chapter labels are separately read from TOC.',
            'volumes': volumes, 'duplicate_exact_prompts': [ids for key, ids in prompts.items() if key and len(ids) > 1],
            'totals': {'volumes': len(volumes), 'chapters': sum(len(v['chapters']) for v in volumes),
                       'problems': sum(len(v['problems']) for v in volumes), 'pages': sum(v['pdf_pages'] or 0 for v in volumes)}}


if __name__ == '__main__':
    report = inventory()
    (ROOT / 'reports/current-inventory.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps(report['totals']))
