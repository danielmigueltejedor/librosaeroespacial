"""The programming encyclopedia keeps its replayed answers and executed checks."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1] / 'enciclopedia-programacion'


def current(volume: str) -> dict[str, dict]:
    records: dict[str, dict] = {}
    for line in (ROOT / 'volumes' / volume / 'problems/problems.jsonl').read_text(encoding='utf-8').splitlines():
        if line.strip():
            record = json.loads(line)
            records[record['id']] = record
    return records


def test_every_revised_answer_replays_and_keeps_its_history():
    ledger = json.loads((ROOT / 'reports/answer-replay.json').read_text(encoding='utf-8'))
    assert len(ledger['changes']) >= 200
    by_volume: dict[str, dict[str, dict]] = {}
    for change in ledger['changes']:
        records = by_volume.setdefault(change['volume'], current(change['volume']))
        record = records[change['id']]
        assert record['answer_check']['result'] == 'replayed', change
        assert record['revision']['review'] == ledger['review']
        assert record['solution']['steps'][0]['expression']


def test_prompt_corrections_state_why():
    ledger = json.loads((ROOT / 'reports/answer-replay.json').read_text(encoding='utf-8'))
    corrected = [c for c in ledger['changes'] if c['prompt_changed']]
    assert len(corrected) >= 7
    assert all(len(c['reason']) > 40 for c in corrected)


def test_toolchain_checks_all_passed_and_name_their_tools():
    report = json.loads((ROOT / 'reports/answer-verification.json').read_text(encoding='utf-8'))
    assert report['failed'] == 0
    assert len(report['checks']) >= 50
    assert all(check['passed'] for check in report['checks'])
    assert {t.split(':')[0] for t in report['tools']} >= {'rustc', 'clang', 'clang++', 'python3', 'node', 'sqlite3'}
