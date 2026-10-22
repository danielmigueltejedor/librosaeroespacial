"""The Studium projects in humanidades-y-ciencias keep their evidence intact."""
import json
import tomllib
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
FOLDER = ROOT / 'humanidades-y-ciencias'
EXPECTED = {
    'literatura-espanola': ('HUMANITIES', 7),
    'historia-moderna-espana': ('HUMANITIES', 6),
    'biologia-celular-molecular': ('LIFE_SCIENCES', 6),
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
def test_every_chapter_has_cited_audited_paragraphs_and_a_two_witness_problem(slug):
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
        worked = [p for p in problems.values() if p['section'] == section['id']]
        assert len(worked) == 1, section['id']
        assert worked[0]['status'] == 'two_witnesses'


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
