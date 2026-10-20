#!/usr/bin/env python3
"""Reject stale, missing, or incomplete author visual-review receipts."""
from collections import Counter
from pathlib import Path
import hashlib
import json
import re

R = Path(__file__).resolve().parents[1]
P = R / 'reports/edition-v2/figure-visual-review.json'


def digest(data):
    return hashlib.sha256(data).hexdigest()


def review_inventory(root, review):
    """Compare every current asset and TikZ occurrence with the reviewed inventory.

    TikZ branches are deduplicated for visual review, but every branch copy must
    match. Asset discovery deliberately matches render-figure-atlas.py.
    """
    current_assets = {}
    current_inline = Counter()
    for book in sorted((root / 'books').iterdir()):
        if not book.is_dir():
            continue
        for p in sorted(book.rglob('*.pdf')):
            if 'figures' in str(p.relative_to(book)) and p.name != 'cover-art.pdf':
                current_assets[str(p.relative_to(root))] = digest(p.read_bytes())
        for p in sorted(book.glob('figures/FIG-*/*.png')):
            if not p.with_suffix('.pdf').exists():
                current_assets[str(p.relative_to(root))] = digest(p.read_bytes())
        for p in sorted(book.rglob('*.tex')):
            if 'figures-originales' in p.parts:
                continue
            for block in re.findall(r'\\begin\{tikzpicture\}.*?\\end\{tikzpicture\}', p.read_text(), re.S):
                sha = digest(re.sub(r'\s+', ' ', block).encode())
                current_inline[(book.name, str(p.relative_to(root)), sha)] += 1

    expected_assets = {}
    expected_inline = Counter()
    stale = []
    for row in review['figures']:
        if row['kind'] == 'inline-tikz':
            for occurrence in row['occurrences']:
                expected_inline[(row['book'], occurrence['file'], row['sha256'])] += 1
        else:
            expected_assets[row['source']] = row['sha256']
            if current_assets.get(row['source']) != row['sha256']:
                stale.append(row['id'])

    missing_inline = expected_inline - current_inline
    extra_inline = current_inline - expected_inline
    for row in review['figures']:
        if row['kind'] == 'inline-tikz' and any(
            (row['book'], occurrence['file'], row['sha256']) in missing_inline
            for occurrence in row['occurrences']
        ):
            stale.append(row['id'])
    unreviewed_assets = sorted(set(current_assets) - set(expected_assets))
    errors = bool(stale or extra_inline or unreviewed_assets)
    return dict(
        status='FAILED' if errors else 'PASSED',
        reviewed_figures=len(review['figures']),
        current_unique_figures=len(current_assets) + len({(b, s) for b, _, s in current_inline}),
        stale_reviews=sorted(set(stale)),
        unreviewed_assets=unreviewed_assets,
        unreviewed_inline_occurrences=[dict(book=b, file=f, sha256=s, count=n)
                                      for (b, f, s), n in sorted(extra_inline.items())],
        scope='Complete source/asset inventory and every duplicate occurrence compared with author visual-review receipts. Passing does not perform a new visual inspection or confer independent scientific approval.',
    )


def main():
    report = review_inventory(R, json.loads(P.read_text()))
    (R / 'reports/edition-v2/figure-review-checks.json').write_text(json.dumps(report, indent=2) + '\n')
    print(report['status'], report['reviewed_figures'], 'figure review receipts;',
          len(report['stale_reviews']), 'stale;',
          len(report['unreviewed_assets']) + len(report['unreviewed_inline_occurrences']), 'unreviewed additions')
    if report['status'] != 'PASSED':
        raise SystemExit(1)


if __name__ == '__main__':
    main()
