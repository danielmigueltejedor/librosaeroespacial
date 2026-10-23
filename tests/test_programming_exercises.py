"""The programming encyclopedia asks for programs, and every reference program was run."""
import importlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1] / 'enciclopedia-programacion'
sys.path.insert(0, str(ROOT / 'tools'))
VOLUMES = sorted(p.name for p in (ROOT / 'volumes').glob('vol0[1-9]*'))


def current(volume: str) -> dict[str, dict]:
    records: dict[str, dict] = {}
    for line in (ROOT / 'volumes' / volume / 'problems/problems.jsonl').read_text(encoding='utf-8').splitlines():
        if line.strip():
            record = json.loads(line)
            records[record['id']] = record
    return records


def test_every_exercise_has_a_passing_run_and_a_stored_contract():
    report = {r['key']: r for r in json.loads((ROOT / 'reports/exercise-verification.json').read_text(encoding='utf-8'))['results']}
    ledger = json.loads((ROOT / 'reports/exercise-records.json').read_text(encoding='utf-8'))
    total = 0
    for volume in VOLUMES:
        module = importlib.import_module(f'exercise_specs.{volume.split("-")[0]}')
        records = current(volume)
        for index, spec in enumerate(module.EXERCISES, 1):
            key = f'{volume.split("-")[0]}-{spec["ch"]:02d}-{index:03d}'
            assert report[key]['passed'], key
            stored = records[ledger[key]['id']]
            assert stored.get('kind') == 'programming' and not stored.get('deleted'), key
            assert spec['code'].isascii(), key
            assert len(spec['tests']) >= 1, key
            total += 1
    assert total >= 200


def test_no_arithmetic_exercise_is_left_in_the_volumes():
    for volume in VOLUMES:
        numeric = [r['id'] for r in current(volume).values() if r.get('kind') == 'numeric' and not r.get('deleted')]
        assert numeric == [], (volume, numeric)


def test_toolchains_are_named_in_the_report():
    report = json.loads((ROOT / 'reports/exercise-verification.json').read_text(encoding='utf-8'))
    assert report['failed'] == 0
    tools = {r['lang']: r['tool'] for r in report['results'] if 'tool' in r}
    assert {'rust', 'python', 'c', 'cpp', 'go', 'java', 'swift', 'kotlin', 'csharp', 'sql'} <= set(tools)
    assert all(version and version != 'unknown' for version in tools.values())
