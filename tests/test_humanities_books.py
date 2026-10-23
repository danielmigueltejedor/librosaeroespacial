"""The Studium projects in humanidades-y-ciencias keep their evidence intact."""
import json
import tomllib
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
FOLDER = ROOT / 'humanidades-y-ciencias'
EXPECTED = {
    'literatura-espanola': ('HUMANITIES', 13),
    'historia-moderna-espana': ('HUMANITIES', 12),
    'biologia-celular-molecular': ('LIFE_SCIENCES', 12),
}


def fold(path: Path) -> dict[str, dict]:
    records: dict[str, dict] = {}
    for line in path.read_text(encoding='utf-8').splitlines():
        if line.strip():
            record = json.loads(line)
            records[record['id']] = record
    return records


def test_the_three_projects_are_present():
    assert {p.parent.name for p in FOLDER.glob('*/project.toml')} == set(EXPECTED)


@pytest.mark.parametrize('slug', sorted(EXPECTED))
def test_project_declares_its_profile_and_language(slug):
    config = tomllib.loads((FOLDER / slug / 'project.toml').read_text(encoding='utf-8'))
    assert config['course']['kind'] == 'topic'
    assert config['course']['language'] == 'es'
    assert config['course']['domain_profile'] == EXPECTED[slug][0]


@pytest.mark.parametrize('slug', sorted(EXPECTED))
def test_every_chapter_has_cited_audited_paragraphs_and_witnessed_exercises(slug):
    project = FOLDER / slug
    sections = json.loads((project / 'blueprint/outline.jsonl').read_text(encoding='utf-8').splitlines()[-1])['sections']
    assert len(sections) == EXPECTED[slug][1]
    paragraphs = {k: v for k, v in fold(project / 'draft/paragraphs.jsonl').items() if not v.get('deleted')}
    audits = [json.loads(line) for line in (project / 'draft/audits.jsonl').read_text(encoding='utf-8').splitlines() if line.strip()]
    audited = {a['target']: a for a in audits if a.get('target_kind') == 'paragraph'}
    problems = {k: v for k, v in fold(project / 'problems/problems.jsonl').items() if not v.get('deleted')}
    for section in sections:
        mine = [p for p in paragraphs.values() if p['section'] == section['id']]
        assert len(mine) >= 10, section['id']
        for paragraph in mine:
            assert len(paragraph['excerpts']) >= 2, paragraph['id']
            audit = audited.get(paragraph['id'])
            assert audit is not None, paragraph['id']
            assert audit['evidence']['excerpts_result'] == 'two_witnesses'
            assert audit['binding']['passages'][paragraph['id']] == paragraph['text_sha256'], paragraph['id']
        exercises = [p for p in problems.values() if p['section'] == section['id']]
        assert len(exercises) >= 5, section['id']
        assert sum(1 for p in exercises if p.get('role') == 'worked') >= 1, section['id']
        assert all(p['status'] == 'two_witnesses' for p in exercises), section['id']


@pytest.mark.parametrize('slug', sorted(EXPECTED))
def test_excerpts_come_from_recorded_public_sources(slug):
    project = FOLDER / slug
    sources = {json.loads(line)['id'] for line in (project / 'bibliography/public.jsonl').read_text(encoding='utf-8').splitlines() if line.strip()}
    for line in (project / 'bibliography/excerpts.jsonl').read_text(encoding='utf-8').splitlines():
        record = json.loads(line)
        if record.get('source_id'):
            assert record['source_id'] in sources
            assert record['url'].startswith('https://')


def test_no_private_or_machine_specific_paths_are_stored():
    for path in FOLDER.rglob('*'):
        if path.is_file() and path.suffix in {'.py', '.jsonl', '.toml', '.json', '.md'}:
            assert '/Users/' not in path.read_text(encoding='utf-8', errors='ignore'), path


@pytest.mark.parametrize('slug', sorted(EXPECTED))
def test_image_figures_keep_author_licence_page_and_file(slug):
    project = FOLDER / slug
    figures = {k: v for k, v in fold(project / 'figures/figures.jsonl').items() if not v.get('deleted')}
    images = [f for f in figures.values() if f['kind'] == 'image']
    assert len(images) >= 15
    for record in images:
        image = record['image']
        assert image['author'] and image['url'].startswith('https://commons.wikimedia.org/'), record['id']
        assert image['license'].lower().startswith(('public domain', 'cc0', 'cc by')), (record['id'], image['license'])
        assert (project / record['output']).is_file(), record['id']
        assert image['bytes'] < 400_000, record['id']


@pytest.mark.parametrize('slug', sorted(EXPECTED))
def test_cover_photograph_keeps_author_licence_source_and_hash(slug):
    import hashlib
    folder = FOLDER / slug / 'cover'
    cover = json.loads((folder / 'cover.json').read_text(encoding='utf-8'))
    assert cover['author'] and cover['description'] and cover['short_title']
    assert cover['source_page'].startswith('https://commons.wikimedia.org/wiki/File:')
    assert cover['licence'].lower().startswith(('public domain', 'cc0', 'cc by'))
    data = (folder / cover['file']).read_bytes()
    assert hashlib.sha256(data).hexdigest() == cover['sha256']
    assert len(data) < 2_500_000
