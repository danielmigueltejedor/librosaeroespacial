"""Regression checks for review coverage, including duplicated TeX branches."""
import importlib.util
from pathlib import Path
import tempfile
import unittest

SPEC = importlib.util.spec_from_file_location('figure_review', Path(__file__).resolve().parents[1] / 'scripts/audit-figure-review.py')
AUDIT = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(AUDIT)


class FigureReviewTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.book = self.root / 'books/example'
        (self.book / 'figures').mkdir(parents=True)
        self.block = r'\begin{tikzpicture}\draw (0,0)--(1,1);\end{tikzpicture}'
        self.tex = self.book / 'manual.tex'
        self.tex.write_text('\n'.join([self.block] * 4))
        self.asset = self.book / 'figures/graph.pdf'
        self.asset.write_bytes(b'original figure bytes')
        self.review = {'figures': [
            dict(id='example-tikz-001', book='example', kind='inline-tikz', source='books/example/manual.tex', sha256=AUDIT.digest(self.block.encode()), occurrences=[dict(file='books/example/manual.tex', line=i) for i in range(1, 5)]),
            dict(id='example/figures/graph.pdf', book='example', kind='pdf-asset', source='books/example/figures/graph.pdf', sha256=AUDIT.digest(self.asset.read_bytes())),
        ]}

    def test_complete_inventory_passes(self):
        result = AUDIT.review_inventory(self.root, self.review)
        self.assertEqual(result['status'], 'PASSED')
        self.assertEqual(result['current_unique_figures'], 2)

    def test_one_changed_branch_cannot_hide_behind_three_original_copies(self):
        self.tex.write_text(self.block.replace('(1,1)', '(1,2)') + '\n' + '\n'.join([self.block] * 3))
        result = AUDIT.review_inventory(self.root, self.review)
        self.assertEqual(result['status'], 'FAILED')
        self.assertIn('example-tikz-001', result['stale_reviews'])
        self.assertEqual(result['unreviewed_inline_occurrences'][0]['count'], 1)

    def test_new_figure_requires_review(self):
        (self.book / 'figures/new.pdf').write_bytes(b'new figure')
        result = AUDIT.review_inventory(self.root, self.review)
        self.assertEqual(result['status'], 'FAILED')
        self.assertEqual(result['unreviewed_assets'], ['books/example/figures/new.pdf'])

    def test_deleted_asset_invalidates_its_receipt(self):
        self.asset.unlink()
        result = AUDIT.review_inventory(self.root, self.review)
        self.assertEqual(result['status'], 'FAILED')
        self.assertIn('example/figures/graph.pdf', result['stale_reviews'])
