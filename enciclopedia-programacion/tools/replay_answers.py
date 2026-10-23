#!/usr/bin/env python3
"""Give the unchecked numeric answers of a volume a replayable solution (append-only revision).

    python tools/replay_answers.py vol03-monografia-rust [--dry-run]

Each entry of ``tools/answer_specs/<vol>.py`` states the data, the formula and the
reasoning. The formula is evaluated with the data, the value must equal the stored
answer, and the record is revised, never overwritten: the previous record stays in
the history. A replay reproduces the arithmetic; it does not validate the model.
"""
from __future__ import annotations

import argparse
import importlib
import json
import re
import sys
from pathlib import Path

from studium.authoring import problems
from studium.authoring.computation import agrees, evaluate
from studium.storage.locking import project_lock
from studium.storage.records import append_jsonl, fold_by_id

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(__file__).resolve().parent))
REVIEW = 'answer-replay-2026-10-23'


def substitute(formula: str, given: list[tuple]) -> str:
    text = formula
    for symbol, value, *_ in sorted(given, key=lambda item: -len(item[0])):
        text = re.sub(rf'\b{re.escape(symbol)}\b', f'({value})' if str(value).startswith('-') else str(value), text)
    return text


def latex_of(formula: str) -> str:
    text = re.sub(r'\*\*\s*(\d+)', r'^{\1}', formula)
    text = text.replace('*', r'\cdot')
    return re.sub(r'\s+', ' ', text).strip()


def solution_for(record: dict, spec: tuple) -> dict:
    given, formula, unit, step, conclusion = spec[:5]
    expression = substitute(formula, given)
    value = evaluate(expression)
    expected = record['expected']
    if not agrees(str(expected), value):
        raise ValueError(f"{record['id']}: the formula gives {value}, the stored answer is {expected}")
    return {
        'given': [{'symbol': s, 'value': str(v), 'unit': u or 'adimensional', 'meaning': m} for s, v, u, m in given],
        'unknown': 'Magnitud pedida en el enunciado',
        'steps': [{'text': step, 'equation': f'r = {latex_of(formula)}', 'expression': expression,
                   'expected': str(expected), 'unit': unit or 'adimensional'}],
        'result': f'Resultado = {expected}' + (f' {unit}' if unit else '') + f'. {conclusion}',
        'interpretation': conclusion,
        'assumptions': ['Los datos son los del enunciado; el modelo es el del capítulo.'],
    }


def revise(volume: Path, dry_run: bool, only: set[str] | None = None) -> list[dict]:
    module = importlib.import_module(f'answer_specs.{volume.name.split("-")[0]}')
    changes = []
    current = {r['id']: r for r in fold_by_id(volume / 'problems/problems.jsonl') if not r.get('deleted')}
    for identifier, spec in sorted(module.SPECS.items()):
        if only and identifier not in only:
            continue
        record = current[identifier]
        fix = spec[5] if len(spec) > 5 else {}
        revised = dict(record)
        for key in ('prompt', 'expected'):
            if key in fix:
                revised[key] = fix[key]
        revised['solution'] = problems._solution(solution_for(revised, spec))[0]
        if revised['solution'] is None:
            raise ValueError(f'{identifier}: the solution was rejected')
        for stale in ('answer_check', 'step_checks'):
            revised.pop(stale, None)
        revised['revision'] = {'review': REVIEW, 'reason': fix.get('reason', 'Replayable solution added; arithmetic reproduced.')}
        problems._stamp_inputs(volume, revised)
        changes.append({'volume': volume.name, 'id': identifier, 'prompt_changed': 'prompt' in fix,
                        'reason': revised['revision']['reason']})
        if not dry_run:
            with project_lock(volume):
                append_jsonl(volume / 'problems/problems.jsonl', revised)
            outcome = problems.check_problem(volume, identifier)
            replay = (outcome.get('answer_check') or {}).get('result')
            if replay != 'replayed':
                raise RuntimeError(f'{identifier}: replay is {replay}')
    return changes


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('volume')
    parser.add_argument('--dry-run', action='store_true')
    parser.add_argument('--only', nargs='*', help='revise only these problem ids')
    args = parser.parse_args()
    volume = ROOT / 'volumes' / args.volume
    changes = revise(volume, args.dry_run, set(args.only) if args.only else None)
    print(json.dumps({'volume': args.volume, 'revised': len(changes), 'dry_run': args.dry_run}))
    if not args.dry_run:
        ledger = ROOT / 'reports/answer-replay.json'
        previous = json.loads(ledger.read_text())['changes'] if ledger.exists() else []
        previous = [c for c in previous if c['volume'] != args.volume or (args.only and c['id'] not in args.only)]
        ledger.write_text(json.dumps({
            'review': REVIEW,
            'reviewer': 'same model, separate pass; not independent academic approval',
            'scope': 'Arithmetic of each stated answer is reproduced from its stated data. This does not validate the model or the language semantics.',
            'changes': previous + changes}, ensure_ascii=False, indent=2) + '\n')


if __name__ == '__main__':
    main()
