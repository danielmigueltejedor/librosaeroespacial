#!/usr/bin/env python3
"""Report code evidence honestly; execution requires explicit --trusted."""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import sys
import tempfile
from collections import Counter
from pathlib import Path

from studium.authoring.literals import code_regions
from studium.storage.records import fold_by_id
from studium.verification.programs import CodeArtifact, _run, verify_program

ROOT = Path(__file__).resolve().parents[1]


def verify_snippet(language: str, code: str, snippet_id: str, *, trusted: bool = False) -> dict:
    kind = language.lower()
    aliases = {'py': 'python', 'rs': 'rust', 'js': 'javascript', 'ts': 'typescript', 'c++': 'cpp'}
    kind = aliases.get(kind, kind)
    mode = 'syntax'
    if trusted and kind == 'rust':
        mode = 'test' if '#[test]' in code else 'compile'
    elif trusted and kind in {'c', 'cpp'}:
        mode = 'compile'
    partial = bool(re.search(r'(?m)^\s*(?://|#|/\*)\s*PARTIAL\b', code))
    result = verify_program(CodeArtifact(kind, code, mode=mode, partial=partial), trusted=trusted)
    if kind in {'text', 'plaintext', 'output', 'terminal', 'console', 'error', 'pseudo', 'pseudocode'}:
        result.update(classification='LITERAL_OR_PSEUDOCODE', passed=None,
                      detail='Literal illustration; no language execution claimed.')
    for command in result.get('commands', []):
        invocation = command['command']
        invocation[0] = '${WORKSPACE}/program' if Path(invocation[0]).name == 'program' else Path(invocation[0]).name
    result['id'] = snippet_id
    # Discard disposable workspace locations; commands remain reproducible recipes.
    return json.loads(re.sub(r'/[^"\n]*studium-code-[^/"\n]+', '${WORKSPACE}', json.dumps(result)))


def verify_projects(*, trusted: bool = False) -> list[dict]:
    recipes = {
        'rust-kv-engine': [['cargo', 'test', '--quiet']],
        'c-arena-allocator': [['cc', '-std=c17', '-Wall', '-Wextra', '-Werror', '-fsanitize=address,undefined', 'arena.c', 'test_arena.c', '-o', 'tests'], ['./tests']],
        'cpp-task-scheduler': [['c++', '-std=c++20', '-Wall', '-Wextra', '-Werror', '-fsanitize=address,undefined', 'test_scheduler.cpp', '-o', 'tests'], ['./tests']],
        'python-bytecode-vm': [[sys.executable, '-m', 'pytest', '-q', 'test_vm.py']],
        'ts-reactive-http': [['node', '--test', 'test_router.ts']],
        'sql-transactional-ledger': [[sys.executable, 'verify_ledger.py']],
    }
    results = []
    for slug, commands in recipes.items():
        original = ROOT / 'projects' / slug
        inputs = {str(p.relative_to(original)): hashlib.sha256(p.read_bytes()).hexdigest()
                  for p in sorted(original.rglob('*')) if p.is_file() and not {'target', '__pycache__', '.pytest_cache'} & set(p.parts)}
        result = {'project': slug, 'inputs': inputs, 'classification': 'ISOLATION_REQUIRED', 'passed': None, 'commands': [], 'tool_versions': {}}
        if not trusted:
            results.append(result)
            continue
        with tempfile.TemporaryDirectory(prefix='studium-project-') as temp:
            stage = Path(temp) / slug
            shutil.copytree(original, stage, ignore=shutil.ignore_patterns('target', '__pycache__', '.pytest_cache'))
            outcome = []
            for command in commands:
                executable = shutil.which(command[0]) if not command[0].startswith('./') else str(stage / command[0][2:])
                if executable is None:
                    result['classification'] = 'PENDING_TOOLCHAIN'
                    break
                if not command[0].startswith('./'):
                    version = _run([executable, '--version'], stage, 5)
                    result['tool_versions'][Path(executable).name] = str(version['stdout'] or version['stderr']).splitlines()[:1]
                run = _run([executable, *command[1:]], stage, 60)
                run['command'][0] = '${WORKSPACE}/tests' if Path(run['command'][0]).name == 'tests' else Path(run['command'][0]).name
                outcome.append(run)
                result['commands'] = outcome
                if run['returncode'] != 0 or run['timed_out'] or run['truncated']:
                    result.update(classification='FAILED', passed=False)
                    break
            else:
                result.update(classification='PROJECT_TEST_COMMAND_PASSED', passed=True,
                              scope='Fixed project-specific regression suite; finite tests do not prove correctness. TypeScript is executed, not typechecked.')
            rendered = json.dumps(result, ensure_ascii=False).replace(str(stage), '${WORKSPACE}').replace(sys.executable, '${PYTHON}')
            results.append(json.loads(rendered))
    return results


def verify_all_volumes(*, trusted: bool = False) -> dict:
    snippets = []
    for volume in sorted((ROOT / 'volumes').glob('vol*')):
        for paragraph in fold_by_id(volume / 'draft/paragraphs.jsonl'):
            for index, region in enumerate(code_regions(str(paragraph.get('text', ''))), 1):
                if region.block:
                    result = verify_snippet(region.language, region.body, f"{volume.name}:{paragraph['id']}:{index}", trusted=trusted)
                    result['section'] = paragraph.get('section')
                    snippets.append(result)
        for problem in fold_by_id(volume / 'problems/problems.jsonl'):
            if problem.get('kind') == 'rust':
                snippets.append(verify_snippet('rust', problem['source_text'], f"{volume.name}:{problem['id']}", trusted=trusted))
    projects = verify_projects(trusted=trusted)
    failed = sum(r['passed'] is False for r in snippets + projects)
    pending = sum(r['passed'] is None for r in snippets + projects)
    report = {'schema_version': 2, 'status': 'FAILED' if failed else 'INCOMPLETE' if pending else 'CHECKS_PASSED',
              'semantic_review': 'required', 'trusted_execution': trusted, 'snippets_total': len(snippets),
              'counts_by_classification': dict(Counter(r['classification'] for r in snippets)),
              'failed_count': failed, 'pending_count': pending, 'projects': projects, 'snippets': snippets}
    (ROOT / 'reports/code-verification-current.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
    return report


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--trusted', action='store_true', help='Opt in only after reviewing exact author-owned source hashes; otherwise use external isolation')
    args = parser.parse_args()
    report = verify_all_volumes(trusted=args.trusted)
    print(json.dumps({k: v for k, v in report.items() if k not in {'projects', 'snippets'}}, indent=2))
    raise SystemExit(1 if report['failed_count'] else 2 if report['pending_count'] else 0)


if __name__ == '__main__':
    main()
