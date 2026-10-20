#!/usr/bin/env python3
"""Versioned, append-only repair of known synthetic evidence (migration 1)."""
from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

from studium.storage.locking import project_lock
from studium.storage.records import append_jsonl, fold_by_id

ROOT = Path(__file__).resolve().parents[1]
SUFFIX = ' Fórmulas y constantes de referencia: '
MIGRATION = 'programming-evidence-integrity-1'


def repair_volume(volume: Path) -> list[dict]:
    changes = []
    with project_lock(volume):
        sources = volume / 'bibliography/public.jsonl'
        excerpts = volume / 'bibliography/excerpts.jsonl'
        fake_ids = {r['id'] for r in fold_by_id(sources) if str(r.get('title', '')).startswith('Referencia Normativa ')}
        for path in (sources, excerpts):
            for record in fold_by_id(path):
                fake = record.get('id') in fake_ids or record.get('source_id') in fake_ids
                text = str(record.get('text', ''))
                synthetic_url = bool(re.search(r'/vol-ref-\d+$', str(record.get('url', ''))))
                if not fake and SUFFIX not in text and not synthetic_url:
                    continue
                revised = dict(record)
                revised['integrity_migration'] = MIGRATION
                revised['classification'] = 'PENDING'
                if synthetic_url:
                    revised['integrity_previous_url'] = record['url']
                    revised['url'] = re.sub(r'/vol-ref-\d+$', '', str(record['url']))
                revised['integrity_previous_text_sha256'] = hashlib.sha256(text.encode()).hexdigest()
                if fake:
                    revised['deleted'] = True
                    revised['integrity_reason'] = 'Generator fabricated title, URL and excerpt; withdrawn from active evidence.'
                else:
                    revised['text'] = text.split(SUFFIX, 1)[0]
                    revised['text_sha256'] = hashlib.sha256(revised['text'].encode()).hexdigest()
                    revised['provenance_status'] = 'client_summary_unverified'
                    revised['integrity_reason'] = 'Removed manuscript-derived additions; remaining client text still requires source comparison.'
                append_jsonl(path, revised)
                changes.append({'volume': volume.name, 'file': str(path.relative_to(volume)), 'id': record['id'],
                                'action': 'withdrawn' if fake else 'synthetic_url_and_or_additions_removed', 'reason': revised['integrity_reason']})
    return changes


def main() -> None:
    changes = []
    for volume in sorted((ROOT / 'volumes').glob('vol*')):
        changes.extend(repair_volume(volume))
    report = ROOT / 'reports/evidence-integrity-migration.json'
    # An idempotent re-run must not erase the original repair ledger.
    previous = json.loads(report.read_text())['changes'] if report.exists() else []
    report.write_text(json.dumps({'migration': MIGRATION, 'changes': previous + changes,
                                 'remaining_semantic_source_review': 'required'}, ensure_ascii=False, indent=2) + '\n')
    print(f'{len(changes)} new evidence revisions; previous journal records preserved')


if __name__ == '__main__':
    main()
