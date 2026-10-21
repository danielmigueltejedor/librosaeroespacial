"""A partial, stale or corrupt library cannot be published by the bundle tool."""
import importlib.util
import json
import zipfile
from pathlib import Path

import pytest
from pypdf import PdfWriter

spec = importlib.util.spec_from_file_location('release_bundle', Path(__file__).parents[1]/'scripts/package-release-bundle.py')
bundle = importlib.util.module_from_spec(spec)
spec.loader.exec_module(bundle)


@pytest.fixture
def collection(tmp_path):
    book = tmp_path/'books/mechanics'
    book.mkdir(parents=True)
    (book/'studium-import.json').write_text(json.dumps({'documents':[{'output':'manual.pdf'}]}))
    (tmp_path/'enciclopedia-programacion/volumes/vol00-guide').mkdir(parents=True)
    entries = [
        {'topic':'mechanics','source':'dist/studium/mechanics/manual.pdf','archive':'mechanics/manual.pdf'},
        {'topic':'programacion','source':'enciclopedia-programacion/dist/review/vol00-guide.pdf','archive':'programacion/volumenes/vol00-guide.pdf'},
        {'topic':'programacion','source':'enciclopedia-programacion/dist/review/ENCICLOPEDIA_COMPLETA_INTEGRAL.pdf','archive':'programacion/Integral.pdf'}]
    for e in entries:
        p = tmp_path/e['source']
        p.parent.mkdir(parents=True, exist_ok=True)
        writer = PdfWriter()
        writer.add_blank_page(width=200,height=200)
        writer.write(p)
    (tmp_path/'release-bundle.json').write_text(json.dumps({'entries':entries}))
    return tmp_path, entries


def test_complete_bundle_is_grouped_and_reopened(collection):
    root, entries = collection
    output = root/'out.zip'
    report = bundle.package(root, output)
    assert report['pdf_count'] == 3
    assert report['topics'] == ['mechanics','programacion']
    assert bundle.verify(output, entries) == report
    with zipfile.ZipFile(output) as z:
        assert set(z.namelist()) == {e['archive'] for e in entries}|{'INVENTARIO.json','LEEME.txt'}


def test_missing_pdf_preserves_previous_delivery(collection):
    root, entries = collection
    out = root/'out.zip'
    bundle.package(root,out)
    previous = out.read_bytes()
    (root/entries[0]['source']).unlink()
    with pytest.raises(ValueError,match='Missing'):
        bundle.package(root,out)
    assert out.read_bytes() == previous


def test_new_book_or_duplicate_destination_cannot_be_omitted(collection):
    root, entries = collection
    (root/'enciclopedia-programacion/volumes/vol01-new').mkdir()
    with pytest.raises(ValueError,match='Catalog'):
        bundle.catalog(root)
    (root/'enciclopedia-programacion/volumes/vol01-new').rmdir()
    entries[1]['archive'] = entries[2]['archive']
    (root/'release-bundle.json').write_text(json.dumps({'entries':entries}))
    with pytest.raises(ValueError,match='Duplicate'):
        bundle.catalog(root)


def test_corrupt_member_is_detected(collection):
    root, entries = collection
    out = root/'out.zip'
    bundle.package(root,out)
    with zipfile.ZipFile(out) as z:
        content = {n:z.read(n) for n in z.namelist()}
    content[entries[0]['archive']] = b'%PDF-tampered'
    with zipfile.ZipFile(out,'w') as z:
        for n,data in content.items():
            z.writestr(n,data)
    with pytest.raises(ValueError,match='checksum'):
        bundle.verify(out,entries)


def test_traversal_is_rejected(collection):
    root, entries = collection
    entries[0]['archive'] = '../manual.pdf'
    (root/'release-bundle.json').write_text(json.dumps({'entries':entries}))
    with pytest.raises(ValueError,match='Unsafe'):
        bundle.catalog(root)


def test_new_aerobooks_subject_without_import_manifest_is_not_silently_omitted(collection):
    root, _ = collection
    folder = root/'books/new-subject'
    folder.mkdir()
    (folder/'book.toml').write_text('title = "New subject"\n')
    with pytest.raises(ValueError, match='Unregistered subject'):
        bundle.catalog(root)


def test_matching_hash_does_not_make_a_placeholder_a_book(collection):
    import hashlib
    root, entries = collection
    out = root/'out.zip'
    bundle.package(root,out)
    with zipfile.ZipFile(out) as z:
        content = {n:z.read(n) for n in z.namelist()}
    name = entries[0]['archive']
    content[name] = b'placeholder'
    inventory = json.loads(content['INVENTARIO.json'])
    record = next(e for e in inventory['files'] if e['archive'] == name)
    record['sha256'] = hashlib.sha256(content[name]).hexdigest()
    record['bytes'] = len(content[name])
    content['INVENTARIO.json'] = json.dumps(inventory).encode()
    with zipfile.ZipFile(out,'w') as z:
        for n,data in content.items():
            z.writestr(n,data)
    with pytest.raises(ValueError,match='Invalid PDF'):
        bundle.verify(out,entries)
