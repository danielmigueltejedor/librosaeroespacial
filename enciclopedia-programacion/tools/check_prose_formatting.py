#!/usr/bin/env python3
"""Detect leaked bold markers in active prose; code and mathematics stay literal."""
import json
from pathlib import Path

from studium.authoring.render import _explicit_spans, _formula_spans, _split_blocks, render_text_run
from studium.storage.records import fold_by_id

ROOT = Path(__file__).resolve().parents[1]


def leaked_markers(text):
    findings = []
    for kind, payload, _ in _split_blocks(text):
        if kind != 'text':
            continue
        explicit = _explicit_spans(payload)
        spans = [(a, b) for a, b, _ in explicit]
        spans += [(a, b) for a, b in _formula_spans(payload, explicit)
                  if not payload[a:b].strip().startswith('*') and not payload[a:b].strip().endswith('*')]
        # A nonempty placeholder preserves emphasis that surrounds a literal.
        # Its contents cannot be mistaken for markup (e.g. Python **kwargs).
        for start, end in sorted(spans, reverse=True):
            payload = payload[:start] + 'PROTECTED' + payload[end:]
        rendered = render_text_run(payload)
        if '**' in rendered:
            findings.append(rendered)
    return findings


def audit(root=ROOT):
    checked = 0
    findings = []
    for volume in sorted((root / 'volumes').glob('vol*')):
        for relative in ('draft/paragraphs.jsonl', 'problems/problems.jsonl'):
            for record in fold_by_id(volume / relative):
                for field, text in (
                    ('text', record.get('text', '')),
                    ('prompt', record.get('prompt', '')),
                    ('solution.text', record.get('solution', {}).get('text', '')),
                ):
                    if not text:
                        continue
                    checked += 1
                    for fragment in leaked_markers(text):
                        findings.append({'volume': volume.name, 'id': record['id'],
                                         'field': field, 'rendered': fragment})
    return {'scope': 'Active paragraph, prompt and solution text; fenced/inline code and math excluded. '
                     'Checks rendering, not academic content.',
            'texts_checked': checked, 'issues': findings}


if __name__ == '__main__':
    report = audit()
    (ROOT / 'reports/prose-formatting.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
    if report['issues']:
        raise SystemExit(json.dumps(report['issues'], ensure_ascii=False))
    print(f"{report['texts_checked']} active texts: no leaked bold markers outside code/math")
