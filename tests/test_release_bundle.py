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


def _run_real_policy_stage(root, review):
    import os, subprocess, textwrap
    workflow=(Path(__file__).resolve().parents[1]/'.github/workflows/release-bundle-guard.yml').read_text()
    stage=workflow.split('      - name: Detect installed default-branch policy\n',1)[1].split('      - uses:',1)[0]
    shell=textwrap.dedent(stage.split('        run: |\n',1)[1])
    output=root/'policy-output';output.write_text('')
    subprocess.run(['bash','-e','-c',shell],cwd=root,env=os.environ|{'GITHUB_OUTPUT':str(output),'REVIEW_RELEASE':str(review).lower()},check=True,capture_output=True)
    return output.read_text().strip()=='enabled=true'


def _policy_git(root,*args):
    import subprocess
    subprocess.run(['git','-c','user.name=Policy fixture','-c','user.email=fixture@example.invalid',*args],cwd=root,check=True,capture_output=True)


def test_uninstalled_policy_only_defers_review_releases(tmp_path):
    _policy_git(tmp_path,'init','-q')
    _policy_git(tmp_path,'commit','--allow-empty','-qm','Initial fixture')
    assert not _run_real_policy_stage(tmp_path,True)
    assert _run_real_policy_stage(tmp_path,False)


def test_deleted_installed_policy_does_not_disable_the_guard(tmp_path):
    _policy_git(tmp_path,'init','-q')
    (tmp_path/'scripts').mkdir()
    files=[tmp_path/'release-bundle.json',tmp_path/'scripts/package-release-bundle.py']
    for p in files:p.write_text('fixture')
    _policy_git(tmp_path,'add','.')
    _policy_git(tmp_path,'commit','-qm','Install fixture policy')
    assert _run_real_policy_stage(tmp_path,True)
    for p in files:p.unlink()
    _policy_git(tmp_path,'commit','-am','Remove fixture policy','-q')
    assert _run_real_policy_stage(tmp_path,True)


def test_incomplete_policy_fails_closed_even_during_first_install(tmp_path):
    _policy_git(tmp_path,'init','-q')
    _policy_git(tmp_path,'commit','--allow-empty','-qm','Initial fixture')
    (tmp_path/'release-bundle.json').write_text('{}')
    assert _run_real_policy_stage(tmp_path,True)
