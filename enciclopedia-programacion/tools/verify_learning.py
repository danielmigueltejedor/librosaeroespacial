#!/usr/bin/env python3
"""Run reviewed teaching programs with real tools and exact output or SQL row oracles."""
from __future__ import annotations
import argparse
import hashlib
import json
import os
import shutil
import sqlite3
import subprocess
import sys
import tempfile
from pathlib import Path

from studium.authoring.literals import code_regions
from studium.authoring.problems import problem_result_current
from studium.storage.records import fold_by_id
ROOT = Path(__file__).resolve().parents[1]
LEARNING = ROOT/'learning'


def execute(command: list[str], cwd: Path, *, expected: str | None = None) -> dict:
    env = os.environ.copy()
    env.update({'DOTNET_CLI_TELEMETRY_OPTOUT':'1','DOTNET_NOLOGO':'1','DOTNET_SKIP_FIRST_TIME_EXPERIENCE':'1','GOTOOLCHAIN':'local'})
    result = subprocess.run(command,cwd=cwd,env=env,text=True,capture_output=True,timeout=120)
    record = {'command':command,'returncode':result.returncode,'stdout':result.stdout,'stderr':result.stderr}
    if result.returncode != 0 or (expected is not None and result.stdout != expected):
        raise RuntimeError(json.dumps(record,ensure_ascii=False))
    return record


def required(name: str, variable: str | None = None) -> str:
    result = os.environ.get(variable or '') or shutil.which(name)
    if not result:
        raise RuntimeError(f'Missing tool: {name}; no verification claimed')
    return str(Path(result).absolute())


def main() -> int:
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--trusted', action='store_true', help='Execute this reviewed repository code; not an isolation boundary')
    args=parser.parse_args()
    if not args.trusted:
        parser.error('Execution requires --trusted after source review')
    units=json.loads((LEARNING/'units.json').read_text())
    versions={}
    report={'scope':'same-model authored examples; finite test cases only; no independent academic approval',
            'files':{str(p.relative_to(LEARNING)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(LEARNING.rglob('*')) if p.is_file()},'units':[]}
    with tempfile.TemporaryDirectory(prefix='.learning-run-',dir=ROOT) as temporary:
        stage=Path(temporary)
        for unit in units:
            key=unit['key'];folder=stage/key
            shutil.copytree(LEARNING/key,folder)
            current={p['id']:p for p in fold_by_id(ROOT/'volumes'/unit['slug']/'problems/problems.jsonl')}
            for identifier in unit['exercise_ids']:
                p=current[identifier]
                if not problem_result_current(ROOT/'volumes'/unit['slug'],p):
                    raise RuntimeError('Stale programming contract: '+identifier)
                source=LEARNING/p['reference_source'].removeprefix('learning/')
                if hashlib.sha256(source.read_bytes()).hexdigest()!=p['reference_sha256']:
                    raise RuntimeError('Stale exercise source: '+identifier)
                for region in code_regions(p['solution']['text']):
                    if region.block:
                        candidates=list((LEARNING/key).glob('*.sql')) if key=='sql' else [source]
                        if not any(region.body.strip() in x.read_text() for x in candidates):
                            raise RuntimeError('Printed solution differs from executable source: '+identifier)
            paragraphs={p['id']:p for p in fold_by_id(ROOT/'volumes'/unit['slug']/'draft/paragraphs.jsonl')}
            if unit['example'] not in paragraphs[unit['paragraph_id']]['text']:
                raise RuntimeError('Printed lesson differs from executable example')
            runs=[]
            if key=='sql':
                db=sqlite3.connect(':memory:')
                db.executescript((folder/'schema.sql').read_text())
                example_rows=db.execute(unit['example']).fetchall()
                assert example_rows==[(1,200),(2,300)],example_rows
                runs.append({'scope':'printed introductory example','actual_rows':example_rows})
                for i,expected in enumerate([[(1,300),(2,300)],[(1,2),(2,1),(3,0)],[(2,),(3,)]],1):
                    query=(folder/f'ex{i}.sql').read_text();actual=db.execute(query).fetchall()
                    assert actual==expected,(query,actual,expected)
                    runs.append({'query_file':f'ex{i}.sql','expected_rows':expected,'actual_rows':actual})
                db.execute('DELETE FROM orders')
                for i,expected in enumerate([[],[(1,0),(2,0),(3,0)],[]],1):
                    assert db.execute((folder/f'ex{i}.sql').read_text()).fetchall()==expected
                versions[key]=sqlite3.sqlite_version
            else:
                tools={'python':(sys.executable,['--version']), 'javascript':(required('node'),['--version']),
                       'typescript':(required('tsc'),['--version']), 'rust':(required('rustc'),['--version']),
                       'c':(required('cc'),['--version']), 'cpp':(required('c++'),['--version']),
                       'java':(required('javac'),['-version']), 'csharp':(required('dotnet','DOTNET_BIN'),['--version']),
                       'go':(required('go','GO_BIN'),['version']), 'bash':(required('bash'),['--version'])}
                tool,versionargs=tools[key]
                version=subprocess.run([tool,*versionargs],cwd=folder,capture_output=True,text=True,timeout=30)
                if version.returncode:raise RuntimeError('Unable to identify tool '+key)
                versions[key]=(version.stdout+version.stderr).strip()
                if key=='python':commands=[[tool,'main.py']]
                elif key=='javascript':commands=[[tool,'main.js']]
                elif key=='typescript':commands=[[tool,'--project','tsconfig.json'],[required('node'),'build/main.js']]
                elif key=='rust':commands=[[tool,'--edition=2021','main.rs','-o','app'],[str(folder/'app')]]
                elif key in {'c','cpp'}:commands=[[tool,'-std='+('c11' if key=='c' else 'c++20'),'-Wall','-Wextra','-Werror','main.'+('c' if key=='c' else 'cpp'),'-o','app'],[str(folder/'app')]]
                elif key=='java':commands=[[tool,'Main.java'],[required('java'),'Main']]
                elif key=='csharp':commands=[[tool,'build','Learning.csproj','--verbosity','quiet'],[tool,str(folder/'bin/Debug/net8.0/Learning.dll')]]
                elif key=='go':commands=[[tool,'run','main.go']]
                else:commands=[[tool,'test.sh']]
                for i,command in enumerate(commands):
                    runs.append(execute(command,folder,expected=f'{key}: OK\n' if i==len(commands)-1 else None))
                # Execute the exact small example printed before the exercises,
                # independently of the larger reference implementation.
                example=folder/'example'
                example.mkdir()
                filename={'python':'main.py','javascript':'main.js','typescript':'main.ts','rust':'main.rs','c':'main.c','cpp':'main.cpp','java':'Main.java','csharp':'Program.cs','go':'main.go','bash':'test.sh'}[key]
                (example/filename).write_text(unit['example']+'\n')
                for config in ['Learning.csproj','tsconfig.json']:
                    if (folder/config).exists(): shutil.copyfile(folder/config,example/config)
                for i,command in enumerate(commands):
                    example_command=[str(example/part.relative_to(folder)) if (part:=Path(arg)).is_absolute() and part.is_relative_to(folder) else arg for arg in command]
                    runs.append({'scope':'printed introductory example',**execute(example_command,example,expected=unit['example_stdout'] if i==len(commands)-1 else None)})

            report['units'].append({'language':unit['title'],'key':key,'status':'CASES_PASSED','exercise_ids':unit['exercise_ids'],'runs':runs})
            print(key+': CASES_PASSED',flush=True)
    report['tool_versions']=versions
    report['unit_count']=len(units)
    report['exercise_count']=sum(len(u['exercise_ids']) for u in units)
    report['verifier_sha256']=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    serialized=json.dumps(report,ensure_ascii=False,indent=2).replace(str(stage),'${WORKSPACE}').replace(sys.executable,'${PYTHON}')
    (ROOT/'reports/learning-verification.json').write_text(serialized+'\n')
    return 0


if __name__=='__main__':
    raise SystemExit(main())
