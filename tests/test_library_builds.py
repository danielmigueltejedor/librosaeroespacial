"""Regression tests for evidence bound to actual LaTeX runs."""
import importlib.util
import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

spec = importlib.util.spec_from_file_location('library_builder', Path(__file__).resolve().parents[1]/'scripts/build-studium-books.py')
builder = importlib.util.module_from_spec(spec)
spec.loader.exec_module(builder)

class LogGateTests(unittest.TestCase):
    def test_rejects_individual_unresolved_reference_and_citation(self):
        for log in ["LaTeX Warning: Reference `eq:missing' on page 8 undefined on input line 20.",
                    "LaTeX Warning: Citation `missing' on page 1 undefined on input line 2.",
                    "Overfull \\hbox (4.8pt too wide)", "Overfull \\vbox (2.1pt too high)",
                    "LaTeX Warning: Label `eq:one' multiply defined.",
                    "LaTeX Warning: Rerun to get cross-references right.","Missing character: There is no x in font y!"]:
            with self.subTest(log=log):self.assertIsNotNone(builder.COMPOSITION_ERROR.search(log))
    def test_ordinary_information_is_not_a_failure(self):
        self.assertIsNone(builder.COMPOSITION_ERROR.search('Output written on manual.pdf (23 pages).'))

class BuildEvidenceTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup)
        self.root=Path(self.tmp.name).resolve();self.book=self.root/'books/example';self.book.mkdir(parents=True)
        for name in ['manual','problems']:(self.book/f'{name}.tex').write_text('source')
        self.config={'workdir':'.','documents':[{'source':f'{n}.tex','output':f'{n}.pdf','title':n} for n in ['manual','problems']]}
    def test_failed_document_does_not_hide_later_build_or_leave_stale_pdf(self):
        out=self.root/'dist/studium/example';out.mkdir(parents=True)
        (out/'manual.pdf').write_bytes(b'stale')
        def run(command,**kwargs):
            name=Path(command[-1]).stem
            if name=='manual':
                return type('Result',(),{'returncode':1,'stdout':b'error'})()
            directory=out/name
            (directory/f'{name}.pdf').write_bytes(b'fresh PDF')
            (directory/f'{name}.log').write_text('Output written on problems.pdf (1 page).')
            (directory/f'{name}.fls').write_text(f'INPUT {self.book}/problems.tex\n')
            return type('Result',(),{'returncode':0,'stdout':b'ok'})()
        with patch.object(builder,'ROOT',self.root),patch.object(builder.subprocess,'run',side_effect=run),patch.object(builder.subprocess,'check_output',return_value='pdfTeX test\n'),patch.dict(os.environ,{'SOURCE_DATE_EPOCH':'1'}):
            rows=builder.build(self.book,self.config,'pdflatex')
        self.assertEqual([r['status'] for r in rows],['FAILED','COMPILED'])
        self.assertFalse((out/'manual.pdf').exists())
        self.assertEqual(rows[1]['inputs'][0]['path'],'books/example/problems.tex')
        self.assertEqual(len(rows[1]['inputs'][0]['sha256']),64)
        self.assertEqual(rows[1]['passes'],3)
