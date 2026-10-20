"""Rebuilding must preserve authoring and fail before publishing conflicts."""
import importlib.util
import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
TOOLS = ROOT / 'enciclopedia-programacion/tools'
sys.path.insert(0, str(TOOLS))
import build_collection as pipeline
import repair_evidence


def test_regeneration_refuses_existing_journals_without_touching_them(tmp_path, monkeypatch):
    monkeypatch.setattr(pipeline, 'VOLUMES', tmp_path)
    slug = 'vol03-test'
    (tmp_path / slug).mkdir()
    correction = tmp_path / slug / 'manual-correction.txt'
    correction.write_text('keep my editorial correction')
    with pytest.raises(FileExistsError):
        pipeline.generate_new_volume({'slug': slug}, lambda _: pytest.fail('must not generate'))
    assert correction.read_text() == 'keep my editorial correction'


def test_path_traversal_and_symlinks_are_refused(tmp_path, monkeypatch):
    monkeypatch.setattr(pipeline, 'VOLUMES', tmp_path)
    for slug in ('../escape', '/absolute', 'vol00-x/../../escape'):
        with pytest.raises(ValueError):
            pipeline.volume_path(slug)
    (tmp_path / 'vol00-x').symlink_to(tmp_path)
    with pytest.raises(ValueError):
        pipeline.volume_path('vol00-x')


def test_failed_compile_preserves_manual_changes_and_previous_pdf(tmp_path, monkeypatch):
    from studium.authoring import render
    volumes = tmp_path / 'volumes'
    volume = volumes / 'vol00-test'
    volume.mkdir(parents=True)
    (tmp_path / 'build-config.json').write_text('{"source_date_epoch": 0}')
    (volume / 'project.toml').write_text('author = "editor"')
    (volume / 'paragraphs.jsonl').write_text('manual revision')
    dist = tmp_path / 'dist'
    (dist / 'review').mkdir(parents=True)
    pdf = dist / 'review/vol00-test.pdf'
    pdf.write_bytes(b'previous valid artifact')
    monkeypatch.setattr(pipeline, 'ROOT', tmp_path)
    monkeypatch.setattr(pipeline, 'VOLUMES', volumes)
    monkeypatch.setattr(pipeline, 'DIST', dist)
    before = pipeline.fingerprints(volume)
    monkeypatch.setattr(render, 'render_draft', lambda *a, **k: {'status': 'render.compile_failed'})
    with pytest.raises(RuntimeError):
        pipeline.compile_volume('vol00-test')
    assert pipeline.fingerprints(volume) == before
    assert pdf.read_bytes() == b'previous valid artifact'
    assert not list(tmp_path.glob('.build-*'))


def test_evidence_repair_is_append_only_and_idempotent(tmp_path):
    from studium.storage.records import fold_by_id
    (tmp_path / '.studium').mkdir()
    bib = tmp_path / 'bibliography'
    bib.mkdir()
    original = {'id': 'source-1', 'title': 'Referencia Normativa missing', 'url': 'https://invalid.example/missing'}
    (bib / 'public.jsonl').write_text(json.dumps(original) + '\n')
    (bib / 'excerpts.jsonl').write_text(json.dumps({'id': 'EVD-1', 'source_id': 'source-1', 'text': 'invented'}) + '\n')
    assert len(repair_evidence.repair_volume(tmp_path)) == 2
    assert (bib / 'public.jsonl').read_text().startswith(json.dumps(original))
    assert fold_by_id(bib / 'public.jsonl') == []
    before = (bib / 'excerpts.jsonl').read_bytes()
    assert repair_evidence.repair_volume(tmp_path) == []
    assert (bib / 'excerpts.jsonl').read_bytes() == before


def test_missing_sources_never_create_synthetic_references(tmp_path, monkeypatch):
    import studium_volume_helper as helper
    catalog = tmp_path / 'sources.json'
    catalog.write_text('[]')
    monkeypatch.setattr(helper, 'SOURCES_PATH', catalog)
    monkeypatch.setattr(helper, 'VOLUMES_DIR', tmp_path / 'volumes')
    with pytest.raises(ValueError, match='Unresolved sources'):
        helper._generate_studium_volume({'slug': 'vol00-test', 'title': 'Test', 'subtitle': 'Test', 'chapters': [{'sources': ['unknown']}]})
    assert not (tmp_path / 'volumes').exists()


def test_normalization_preserves_real_urls():
    spec = importlib.util.spec_from_file_location('last_volumes', TOOLS / 'build_vol08_vol09_vol00.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    normalized = module._normalize_spec(module.VOL00_SPEC)
    assert [s['url'] for s in normalized['extra_sources']] == [s['url'] for s in module.VOL00_SPEC['sources']]


def test_integral_keeps_each_volumes_named_toc_destinations():
    from io import BytesIO
    from pypdf import PdfReader, PdfWriter
    from pypdf.generic import ArrayObject, DictionaryObject, NameObject, TextStringObject, NumberObject
    from pdf_assembly import namespace_destinations
    merged = PdfWriter()
    for number in range(2):
        writer = PdfWriter()
        writer.add_blank_page(width=100, height=100)
        writer.add_blank_page(width=100, height=100)
        writer.add_named_destination('chapter.1', 1)
        annotation = DictionaryObject({NameObject('/Type'): NameObject('/Annot'), NameObject('/Subtype'): NameObject('/Link'),
            NameObject('/Rect'): ArrayObject([NumberObject(n) for n in (0,0,10,10)]),
            NameObject('/A'): DictionaryObject({NameObject('/S'): NameObject('/GoTo'), NameObject('/D'): TextStringObject('chapter.1')})})
        writer.pages[0][NameObject('/Annots')] = ArrayObject([writer._add_object(annotation)])
        stream = BytesIO(); writer.write(stream)
        reader = PdfReader(stream)
        reader = namespace_destinations(reader, f'vol{number}')
        merged.append(reader)
    output = BytesIO(); merged.write(output)
    result = PdfReader(output)
    for number in range(2):
        name = result.pages[number * 2]['/Annots'][0].get_object()['/A']['/D']
        assert name == f'vol{number}:chapter.1'
        assert result.get_destination_page_number(result.named_destinations[name]) == number * 2 + 1


def test_new_generation_refuses_content_free_exercise_templates(tmp_path, monkeypatch):
    import studium_volume_helper as helper
    catalog = tmp_path / "sources.json"
    catalog.write_text("[]")
    monkeypatch.setattr(helper, "SOURCES_PATH", catalog)
    monkeypatch.setattr(helper, "VOLUMES_DIR", tmp_path / "volumes")
    with pytest.raises(ValueError, match="concrete technical scenario"):
        helper._generate_studium_volume({"slug": "vol00-test", "title": "Test", "subtitle": "Test",
            "chapters": [{"sources": [], "exercises": [{"prompt": "analice el escenario técnico número 1"}]}]})
    assert not (tmp_path / "volumes").exists()
