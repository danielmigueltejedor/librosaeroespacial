#!/usr/bin/env python3
"""Programming exercises of the encyclopedia: verify them with real toolchains, record them, retire calculations.

    python tools/exercises.py verify [vol03 vol04 ...]   # run every reference program with its tests
    python tools/exercises.py record vol03               # store the verified exercises as Studium contracts
    python tools/exercises.py retire vol03               # withdraw the numeric (arithmetic) exercises

Each exercise lives in ``tools/exercise_specs/<vol>.py``: a prompt that asks for a program, the
reference solution that the book prints, and a test driver that is not printed. The driver must print
``OK`` (or the exact ``expect`` text). ``verify`` writes tool versions, source hashes and the observed
output to ``reports/exercise-verification.json``. A passing run means the reference solution meets
the stated cases on that toolchain; it is not an academic approval.
"""
from __future__ import annotations

import hashlib
import importlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(__file__).resolve().parent))
REPORT = ROOT / 'reports/exercise-verification.json'
LEDGER = ROOT / 'reports/exercise-records.json'

PY = shutil.which('python3.14') or shutil.which('python3.13') or shutil.which('python3.12') or 'python3'

JAVA = '/opt/homebrew/opt/openjdk/bin/java' if Path('/opt/homebrew/opt/openjdk/bin/java').exists() else 'java'

# language -> (file name, build command or None, run command, version command, fence tag)
LANGS = {
    'rust': ('main.rs', ['rustc', '--edition', '2021', '-O', 'main.rs', '-o', 'prog'], ['./prog'], ['rustc', '--version'], 'rust'),
    'c': ('main.c', ['clang', '-std=c11', '-Wall', '-Werror', 'main.c', '-o', 'prog'], ['./prog'], ['clang', '--version'], 'c'),
    'cpp': ('main.cpp', ['clang++', '-std=c++20', '-Wall', '-Werror', 'main.cpp', '-o', 'prog'], ['./prog'], ['clang++', '--version'], 'cpp'),
    'python': ('main.py', None, [PY, 'main.py'], [PY, '--version'], 'python'),
    'js': ('main.js', None, ['node', 'main.js'], ['node', '--version'], 'javascript'),
    'ts': ('main.ts', None, ['node', '--disable-warning=ExperimentalWarning', 'main.ts'], ['node', '--version'], 'typescript'),
    'java': ('Main.java', None, [JAVA, 'Main.java'], [JAVA, '-version'], 'java'),
    'go': ('main.go', None, ['go', 'run', 'main.go'], ['go', 'version'], 'go'),
    'swift': ('main.swift', ['swiftc', '-O', 'main.swift', '-o', 'prog'], ['./prog'], ['swiftc', '--version'], 'swift'),
    'ruby': ('main.rb', None, ['ruby', 'main.rb'], ['ruby', '--version'], 'ruby'),
    'lua': ('main.lua', None, ['lua', 'main.lua'], ['lua', '-v'], 'lua'),
    'perl': ('main.pl', None, ['perl', 'main.pl'], ['perl', '-v'], 'perl'),
    'php': ('main.php', None, ['php', '-d', 'zend.assertions=1', 'main.php'], ['php', '--version'], 'php'),
    'bash': ('main.sh', None, ['bash', 'main.sh'], ['bash', '--version'], 'bash'),
    'sql': ('main.sql', None, ['sqlite3', ':memory:', '.read main.sql'], ['sqlite3', '--version'], 'sql'),
    'haskell': ('main.hs', None, ['runghc', 'main.hs'], ['ghc', '--version'], 'haskell'),
    'ocaml': ('main.ml', None, ['ocaml', 'main.ml'], ['ocaml', '-version'], 'ocaml'),
    'elixir': ('main.exs', None, ['elixir', 'main.exs'], ['elixir', '--version'], 'elixir'),
    'zig': ('main.zig', None, ['zig', 'run', 'main.zig'], ['zig', 'version'], 'zig'),
    'kotlin': ('main.kt', ['kotlinc', 'main.kt', '-include-runtime', '-d', 'prog.jar'], ['java', '-jar', 'prog.jar'], ['kotlinc', '-version'], 'kotlin'),
    'prolog': ('main.pl', None, ['swipl', '-q', '-f', 'main.pl', '-t', 'halt'], ['swipl', '--version'], 'prolog'),
    'fortran': ('main.f90', ['gfortran', 'main.f90', '-o', 'prog'], ['./prog'], ['gfortran', '--version'], 'fortran'),
    'objc': ('main.m', ['clang', '-fobjc-arc', '-framework', 'Foundation', 'main.m', '-o', 'prog'], ['./prog'], ['clang', '--version'], 'objectivec'),
    'asm-arm64': ('main.s', ['clang', '-arch', 'arm64', 'main.s', 'driver.c', '-o', 'prog'], ['./prog'], ['clang', '--version'], 'asm'),
    'csharp': ('main.cs', None, ['dotnet', 'run', 'main.cs'], ['dotnet', '--version'], 'csharp'),
    'julia': ('main.jl', None, ['julia', 'main.jl'], ['julia', '--version'], 'julia'),
    'r': ('main.R', None, ['Rscript', 'main.R'], ['Rscript', '--version'], 'r'),
    'scala': ('main.scala', None, ['scala', 'run', 'main.scala', '--server=false'], ['scala', '--version'], 'scala'),
    'clojure': ('main.clj', None, ['clojure', '-M', 'main.clj'], ['clojure', '--version'], 'clojure'),
    'ts-types': ('main.ts', None, ['tsc', '--noEmit', '--strict', '--target', 'ES2022', '--lib', 'ES2022', 'main.ts'], ['tsc', '--version'], 'typescript'),
    'zig-test': ('main.zig', None, ['zig', 'test', 'main.zig'], ['zig', 'version'], 'zig'),
}


def program(spec: dict) -> str:
    code, harness = spec['code'].rstrip('\n'), spec['harness'].rstrip('\n')
    return harness.replace('{{code}}', code) + '\n' if '{{code}}' in harness else code + '\n' + harness + '\n'


def specs(volume: str) -> list[dict]:
    try:
        module = importlib.import_module(f'exercise_specs.{volume.split("-")[0]}')
    except ModuleNotFoundError:
        return []
    out = []
    for index, spec in enumerate(module.EXERCISES, 1):
        entry = dict(spec)
        entry.setdefault('key', f'{volume.split("-")[0]}-{entry["ch"]:02d}-{index:03d}')
        entry.setdefault('expect', 'OK')
        entry.setdefault('kind', 'implementation')
        out.append(entry)
    keys = [e['key'] for e in out]
    assert len(keys) == len(set(keys)), 'duplicate exercise keys'
    return out


def version(argv: list[str]) -> str:
    done = subprocess.run(argv, capture_output=True, text=True, check=False)
    text = (done.stdout or done.stderr).strip().splitlines()
    first = text[0] if text else 'unknown'
    if argv[0] == 'sqlite3':
        return 'SQLite ' + first.split()[0]
    return ' '.join(first.split()[:6])


def run_one(spec: dict, work: Path) -> dict:
    name, build, command, version_cmd, _ = LANGS[spec['lang']]
    folder = work / spec['key']
    folder.mkdir()
    source = program(spec)
    if spec['lang'] == 'asm-arm64':
        (folder / 'driver.c').write_text(spec['harness'], encoding='utf-8')
        source = spec['code'] + '\n' + spec['harness']
        (folder / name).write_text(spec['code'].rstrip('\n') + '\n', encoding='utf-8')
    else:
        (folder / name).write_text(source, encoding='utf-8')
    if build:
        built = subprocess.run(build, cwd=folder, capture_output=True, text=True, check=False, timeout=300)
        if built.returncode:
            return {'key': spec['key'], 'passed': False, 'stage': 'build', 'output': (built.stderr or built.stdout)[-1200:]}
    env = {**os.environ, 'DOTNET_NOLOGO': '1', 'DOTNET_CLI_TELEMETRY_OPTOUT': '1', 'GOTOOLCHAIN': 'local', 'JULIA_PKG_OFFLINE': 'true'}
    done = subprocess.run(command, cwd=folder, capture_output=True, text=True, check=False, timeout=240, env=env)
    out = done.stdout.strip()
    return {'key': spec['key'], 'lang': spec['lang'], 'tool': version(version_cmd), 'passed': done.returncode == 0 and out == spec['expect'].strip(),
            'observed': out[-300:], 'stderr': done.stderr.strip()[-400:] if done.returncode else '',
            'source_sha256': hashlib.sha256(source.encode()).hexdigest()}


def verify(volumes: list[str]) -> int:
    results = []
    previous = json.loads(REPORT.read_text())['results'] if REPORT.exists() else []
    with tempfile.TemporaryDirectory(prefix='.exercises-') as temp:
        for volume in volumes:
            for spec in specs(volume):
                if spec['lang'] not in LANGS or shutil.which(LANGS[spec['lang']][2][0] if spec['lang'] in ('haskell',) else LANGS[spec['lang']][3][0]) is None:
                    results.append({'key': spec['key'], 'passed': False, 'stage': 'tool', 'output': f"missing tool for {spec['lang']}"})
                    continue
                result = run_one(spec, Path(temp))
                results.append(result)
                print(('ok  ' if result['passed'] else 'FAIL'), spec['key'], spec['lang'], '' if result['passed'] else (result.get('output') or result.get('observed') or result.get('stderr', ''))[:300])
    touched = {r['key'].split('-')[0] for r in results}
    kept = [r for r in previous if r['key'].split('-')[0] not in touched]
    allr = kept + results
    REPORT.write_text(json.dumps({
        'date': date.today().isoformat(),
        'scope': 'Each reference program was compiled or interpreted and run with its test driver. A pass shows that the program meets the stated cases on that toolchain; it is not an academic approval.',
        'failed': sum(1 for r in allr if not r['passed']), 'results': allr}, ensure_ascii=False, indent=1) + '\n')
    failed = [r for r in results if not r['passed']]
    print(json.dumps({'run': len(results), 'failed': len(failed)}))
    return 1 if failed else 0


def solution_text(spec: dict, tool: str = '') -> str:
    fence = LANGS[spec['lang']][4]
    cases = '; '.join(spec['tests'])
    ran = f' con {tool}' if tool else ''
    return (f"{spec['why'].strip()}\n\n```{fence}\n{spec['code'].strip()}\n```\n\n"
            f"Casos comprobados al ejecutarla{ran}: {cases}. Una prueba aprobada no cubre entradas fuera del contrato.")


def section_ids(volume: str) -> dict[int, str]:
    root = ROOT / 'volumes' / volume
    last = {}
    for line in (root / 'blueprint/academic.jsonl').read_text().splitlines():
        if line.strip():
            record = json.loads(line)
            last[record.get('id')] = record
    chapters = [c['id'] for part in list(last.values())[-1]['parts'] for c in part['chapters']]
    return {i: c for i, c in enumerate(chapters, 1)}


def record(volumes: list[str]) -> None:
    from studium.authoring import problems
    ledger = json.loads(LEDGER.read_text()) if LEDGER.exists() else {}
    report = {r['key']: r for r in json.loads(REPORT.read_text())['results']}
    for volume in volumes:
        root = ROOT / 'volumes' / volume
        sections = section_ids(volume)
        for spec in specs(volume):
            if not report.get(spec['key'], {}).get('passed'):
                raise SystemExit(f"{spec['key']}: no passing verification; refusing to record")
            digest = hashlib.sha256(json.dumps([spec, report[spec['key']].get('tool', '')], sort_keys=True, ensure_ascii=False).encode()).hexdigest()
            old = ledger.get(spec['key'])
            if old and old['sha256'] == digest:
                continue
            if old:
                problems.remove_problem(root, old['id'])
            contract = {'kind': spec['kind'], 'language': LANGS[spec['lang']][4], 'solution': solution_text(spec, report[spec['key']].get('tool', '')), 'tests': spec['tests'], 'rubric': []}
            out = problems.record_problem(root, section=sections[spec['ch']], prompt=spec['prompt'], role='practice',
                                          difficulty=spec['level'], problem_type='APPLICATION', programming=contract)
            if out.get('status') != 'recorded':
                raise SystemExit(f"{spec['key']}: {json.dumps(out, ensure_ascii=False)[:500]}")
            ledger[spec['key']] = {'id': out['problem']['id'], 'sha256': digest, 'volume': volume}
            LEDGER.write_text(json.dumps(ledger, ensure_ascii=False, indent=1) + '\n')
        print(volume, 'recorded', sum(1 for v in ledger.values() if v['volume'] == volume))


def retire(volumes: list[str]) -> None:
    from studium.authoring import problems
    from studium.storage.records import fold_by_id
    for volume in volumes:
        root = ROOT / 'volumes' / volume
        gone = []
        for rec in fold_by_id(root / 'problems/problems.jsonl'):
            if rec.get('deleted') or rec.get('kind') != 'numeric':
                continue
            out = problems.remove_problem(root, rec['id'])
            gone.append(rec['id'])
            assert out.get('status') in ('removed', 'ok', 'deleted'), out
        print(volume, 'retired numeric exercises:', len(gone))


def main() -> int:
    command, *volumes = sys.argv[1:] or ['verify']
    names = [p.name for p in sorted((ROOT / 'volumes').glob('vol*'))]
    chosen = [n for n in names if not volumes or n.split('-')[0] in volumes or n in volumes]
    if command == 'verify':
        return verify(chosen)
    if command == 'record':
        record(chosen)
    elif command == 'retire':
        retire(chosen)
    else:
        raise SystemExit(__doc__)
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
