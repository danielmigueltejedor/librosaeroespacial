#!/usr/bin/env python3
"""Run real toolchains against the language-specific claims behind stored answers.

    python tools/verify_answers.py

Each check is a small program written independently of the formula used in the
replay: it asks the compiler, interpreter or database for the quantity itself
(size_of, sizeof, MemoryLayout, window functions, exit codes, git objects).
The report keeps tool versions, source hashes and outputs. A passing check shows
that one claim holds on this machine and toolchain; it is not an approval.
"""
from __future__ import annotations

import hashlib
import json
import shutil
import subprocess
import sys
import tempfile
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / 'reports/answer-verification.json'

RUST = r'''
use std::fmt::Display;
use std::mem::size_of;
use std::num::{NonZeroU32, NonZeroU64};
use std::rc::Rc;
use std::sync::atomic::{AtomicU64, Ordering};
use std::sync::Arc;
use std::thread;
#[repr(C)] struct BadLayoutC { a: u8, b: u64, c: u8 }
struct GoodLayoutRust { a: u8, b: u64, c: u8 }
fn main() {
    println!("vol03/PRB-0004 {}", size_of::<Vec<f64>>());
    println!("vol03/PRB-0005 {}", size_of::<&dyn Display>());
    println!("vol03/PRB-0011 {}", size_of::<[u64; 32]>());
    println!("vol03/PRB-0018 {}", size_of::<String>());
    println!("vol03/PRB-0025 {}", size_of::<Option<Box<u64>>>());
    println!("vol03/PRB-0026 {}", size_of::<[Option<NonZeroU32>; 1000]>());
    println!("vol03/PRB-0028 {}", 64 / size_of::<Option<NonZeroU64>>());
    println!("vol03/PRB-0046 {}", size_of::<BadLayoutC>());
    println!("vol03/PRB-0047 {}", size_of::<GoodLayoutRust>());
    println!("vol03/PRB-0012 {}", "abcdefgh\u{3b1}\u{3b2}\u{3b3}\u{3b4}\u{1f600}\u{1f601}".len());
    println!("vol03/PRB-0013 {}", 250u8.wrapping_add(15));
    let mut v: Vec<i32> = Vec::with_capacity(128);
    for i in 0..50 { v.push(i); }
    println!("vol03/PRB-0014 {}", (v.capacity() - v.len()) * size_of::<i32>());
    let big = vec![0u8; 1024];
    let mut copy = big.clone();
    let (_, right) = copy.split_at_mut(300);
    println!("vol03/PRB-0019 {}", right.len());
    println!("vol03/PRB-0032 {}", (1..=10).filter(|x| x % 2 == 0).map(|x| x * x).sum::<i32>());
    let original = Rc::new(5);
    let clones: Vec<Rc<i32>> = (0..4).map(|_| Rc::clone(&original)).collect();
    let _weak: Vec<_> = (0..3).map(|_| Rc::downgrade(&original)).collect();
    let mut clones = clones;
    clones.truncate(2);
    println!("vol03/PRB-0034 {}", Rc::strong_count(&original));
    let counter = Arc::new(AtomicU64::new(0));
    let handles: Vec<_> = (0..4).map(|_| { let c = Arc::clone(&counter); thread::spawn(move || { for _ in 0..25_000 { c.fetch_add(1, Ordering::Relaxed); } }) }).collect();
    for h in handles { h.join().unwrap(); }
    println!("vol03/PRB-0039 {}", counter.load(Ordering::Relaxed));
    let data = vec![0u8; 10_000];
    println!("vol03/PRB-0040 {}", data.chunks(1250).count());
}
'''
RUST_EXPECTED = '''vol03/PRB-0004 24
vol03/PRB-0005 16
vol03/PRB-0011 256
vol03/PRB-0018 24
vol03/PRB-0025 8
vol03/PRB-0026 4000
vol03/PRB-0028 8
vol03/PRB-0046 24
vol03/PRB-0047 16
vol03/PRB-0012 24
vol03/PRB-0013 9
vol03/PRB-0014 312
vol03/PRB-0019 724
vol03/PRB-0032 220
vol03/PRB-0034 3
vol03/PRB-0039 100000
vol03/PRB-0040 8'''

C = r'''
#include <stdint.h>
#include <stdio.h>
struct S { uint32_t a, b, c, d; uint64_t e, f; };
int main(void) {
    uint16_t m = (uint16_t)-1;
    uint8_t mask = (1u << 0) | (1u << 3) | (1u << 7);
    uint64_t *p = (uint64_t *)4096;
    printf("vol04/PRB-0003 %u\n", (unsigned)m);
    printf("vol04/PRB-0004 %u\n", (unsigned)mask);
    printf("vol04/PRB-0005 %zu\n", sizeof(struct S));
    printf("vol04/PRB-0009 %lu\n", (unsigned long)(uintptr_t)(p + 5));
    return 0;
}
'''
C_EXPECTED = '''vol04/PRB-0003 65535
vol04/PRB-0004 137
vol04/PRB-0005 32
vol04/PRB-0009 4136'''

CPP = r'''
#include <array>
#include <cstdio>
#include <memory>
#include <ranges>
#include <span>
#include <variant>
template <class... T> constexpr auto sum_all(T... args) { return (args + ...); }
int main() {
    int inspected = 0;
    auto evens = std::views::iota(1, 1001)
        | std::views::transform([&](int x) { if (x > inspected) inspected = x; return x; })
        | std::views::filter([](int x) { return x % 2 == 0; })
        | std::views::take(5);
    for (int x : evens) { (void)x; }
    std::printf("vol04/PRB-0021 %zu\n", sizeof(std::unique_ptr<double>));
    std::printf("vol04/PRB-0022 %zu\n", sizeof(std::span<const int>));
    std::printf("vol04/PRB-0028 %d\n", sum_all(10, 20, 30, 40));
    std::printf("vol04/PRB-0029 %zu\n", sizeof(std::variant<int, double, std::array<char, 32>>));
    std::printf("vol04/PRB-0030 %d\n", inspected);
}
'''
CPP_EXPECTED = '''vol04/PRB-0021 8
vol04/PRB-0022 16
vol04/PRB-0028 100
vol04/PRB-0029 40
vol04/PRB-0030 12'''

SWIFT = r'''
protocol P1 {}
protocol P2 {}
protocol P3 {}
struct Inline { var a: Int; var b: Int; var c: Int }
struct Boxed { var a: Int; var b: Int; var c: Int; var d: Int }
extension Inline: P1 {}
extension Boxed: P1 {}
final class Obj { var x = 0 }
print("vol06/PRB-0047", MemoryLayout<any P1 & P2 & P3>.size)
print("vol06/PRB-0027", MemoryLayout<[Int]>.size)
let a = Array(repeating: 1, count: 50_000)
var b = a
let same = a.withUnsafeBufferPointer { x in b.withUnsafeBufferPointer { y in x.baseAddress == y.baseAddress } }
print("vol06/PRB-0046", same ? 0 : 50_000)
'''
SWIFT_EXPECTED = '''vol06/PRB-0047 56
vol06/PRB-0027 8
vol06/PRB-0046 0'''

PYTHON = r'''
import functools, sys
print("vol05/PRB-0005", sum(x * x for x in range(1, 10, 2)))
x, y = 6, 9
print("vol05/PRB-0006", (x + 4) * (y - 2) + (10 if x < y else 20))
class A: pass
class B(A): pass
class C(A): pass
class D(B, C): pass
print("vol05/PRB-0011", len(D.__mro__))
calls = 0
@functools.lru_cache(maxsize=256)
def f(k):
    global calls
    calls += 1
    return k
for i in range(1000):
    f(i % 200)
print("vol05/PRB-0012", calls)
print("vol05/PRB-0003", sys.getsizeof(object()))
print("vol05/PRB-0042", round(sum(round(v * 100) / 100 for v in [12.5, 7.25, 10.25]), 2))
print("vol05/PRB-0018", sum(100 * 2 ** k for k in range(4)))
n = -15
print("vol08/PRB-0017", ((n << 1) ^ (n >> 31)) & 0xFFFFFFFF)
print("vol08/PRB-0016", (3 << 3) | 2)
print("vol08/PRB-0010", 1 * 100 ** 2 + 2 * 100 + 3)
print("vol07/PRB-0012", oct(0o666 & ~0o027)[2:])
print("vol09/PRB-0003", round(9 / (1 + 9) * 100))
print("vol07/PRB-0027", (85 - 1) // 2)
'''
PYTHON_EXPECTED = '''vol05/PRB-0005 165
vol05/PRB-0006 80
vol05/PRB-0011 5
vol05/PRB-0012 200
vol05/PRB-0003 16
vol05/PRB-0042 30.0
vol05/PRB-0018 1500
vol08/PRB-0017 29
vol08/PRB-0016 26
vol08/PRB-0010 10203
vol07/PRB-0012 640
vol09/PRB-0003 90
vol07/PRB-0027 42'''

NODE = r'''
console.log('vol05/PRB-0022', new Float64Array(new ArrayBuffer(1024)).length);
const order = [];
setTimeout(() => { order.push('macro'); console.log('vol05/PRB-0027', order.filter(x => x === 'micro').length); }, 0);
for (let i = 0; i < 5; i++) Promise.resolve().then(() => order.push('micro'));
class Base {} class Sub extends Base {}
let links = 0; let o = new Sub();
while (o !== null) { links++; o = Object.getPrototypeOf(o); }
console.log('vol05/PRB-0023', links);
'''
NODE_EXPECTED = '''vol05/PRB-0022 128
vol05/PRB-0023 4
vol05/PRB-0027 5'''

RUBY = "puts 'vol07/PRB-0016 ' + (1..10).select(&:even?).map { |x| x * 3 }.sum.to_s"
RUBY_EXPECTED = 'vol07/PRB-0016 90'

SQL = '''
CREATE TABLE s(v INTEGER); INSERT INTO s VALUES (100),(90),(90),(80);
SELECT 'vol07/PRB-0003 ' || rk FROM (SELECT v, RANK() OVER (ORDER BY v DESC) rk FROM s) WHERE v = 80;
SELECT 'vol07/PRB-0004 ' || rk FROM (SELECT v, DENSE_RANK() OVER (ORDER BY v DESC) rk FROM s) WHERE v = 80;
WITH RECURSIVE a(n) AS (SELECT 1 UNION ALL SELECT n + 1 FROM a WHERE n < 120), b(n) AS (SELECT 1 UNION ALL SELECT n + 1 FROM b WHERE n < 365)
SELECT 'vol07/PRB-0005 ' || COUNT(*) FROM a CROSS JOIN b;
WITH RECURSIVE n(i) AS (SELECT 1 UNION ALL SELECT i + 1 FROM n WHERE i < 1000)
SELECT 'vol07/PRB-0006 ' || i FROM n ORDER BY i LIMIT 1 OFFSET 400;
'''
SQL_EXPECTED = '''vol07/PRB-0003 4
vol07/PRB-0004 3
vol07/PRB-0005 43800
vol07/PRB-0006 401'''

BASH = r'''
bash -c 'kill -INT $$' ; echo "vol07/PRB-0009 $?"
bash -c 'kill -TERM $$' ; echo "vol07/PRB-0010 $?"
echo "vol07/PRB-0011 $(seq 600 | xargs -n 50 echo | wc -l | tr -d ' ')"
(umask 027; touch f; echo "vol07/PRB-0012b $(stat -f %Lp f 2>/dev/null || stat -c %a f)")
'''
BASH_EXPECTED = '''vol07/PRB-0009 130
vol07/PRB-0010 143
vol07/PRB-0011 12
vol07/PRB-0012b 640'''

FORTRAN = '''
program t
  implicit none
  integer, parameter :: n = 1002
  real :: u(n)
  u = 0.0
  print '(A,I0)', 'vol04/PRB-0046 ', size(u(2:n-1))
end program t
'''
FORTRAN_EXPECTED = 'vol04/PRB-0046 1000'

LUA = "print('vol07/PRB-0045 ' .. (6^2 + 8^2))"
LUA_EXPECTED = 'vol07/PRB-0045 100.0'

GIT = r'''
set -e
git init -q repo && cd repo
git config user.email a@b.c && git config user.name t
mkdir -p a/b && echo one > a/b/f.txt && echo top > top.txt
git add . && git commit -q -m first
before=$(git count-objects -v | awk '/^count:/{print $2}')
echo two > a/b/f.txt && git add . && git commit -q -m second
after=$(git count-objects -v | awk '/^count:/{print $2}')
echo "vol09/PRB-0016 $((after - before))"
'''
GIT_EXPECTED = 'vol09/PRB-0016 5'


def run(argv: list[str], cwd: Path, stdin: str | None = None) -> str:
    done = subprocess.run(argv, cwd=cwd, input=stdin, capture_output=True, text=True, timeout=300, check=False)
    return (done.stdout + (f'\n[stderr] {done.stderr.strip()}' if done.returncode and done.stderr else '')).strip()


def version(argv: list[str]) -> str:
    done = subprocess.run(argv, capture_output=True, text=True, check=False)
    return (done.stdout or done.stderr).strip().splitlines()[0]


def checks(work: Path) -> list[dict]:
    jobs = []

    def add(tool, versioncmd, source, expected, build=None, ext='txt', command=None):
        path = work / f'{tool}.{ext}'
        path.write_text(source)
        jobs.append(dict(tool=tool, version=version(versioncmd), source=source, expected=expected, path=path, build=build, command=command))

    add('rustc', ['rustc', '--version'], RUST, RUST_EXPECTED, build=['rustc', '--edition', '2021', '-O', 'rustc.rs', '-o', 'rustc_bin'], ext='rs', command=['./rustc_bin'])
    add('clang', ['clang', '--version'], C, C_EXPECTED, build=['clang', '-std=c11', 'clang.c', '-o', 'clang_bin'], ext='c', command=['./clang_bin'])
    add('clang++', ['clang++', '--version'], CPP, CPP_EXPECTED, build=['clang++', '-std=c++20', 'clang++.cpp', '-o', 'cpp_bin'], ext='cpp', command=['./cpp_bin'])
    add('swiftc', ['swiftc', '--version'], SWIFT, SWIFT_EXPECTED, build=['swiftc', '-O', 'swiftc.swift', '-o', 'swift_bin'], ext='swift', command=['./swift_bin'])
    add('python3', ['python3', '--version'], PYTHON, PYTHON_EXPECTED, ext='py', command=['python3', 'python3.py'])
    add('node', ['node', '--version'], NODE, NODE_EXPECTED, ext='js', command=['node', 'node.js'])
    add('ruby', ['ruby', '--version'], RUBY, RUBY_EXPECTED, ext='rb', command=['ruby', 'ruby.rb'])
    add('sqlite3', ['sqlite3', '--version'], SQL, SQL_EXPECTED, ext='sql', command=['sqlite3', ':memory:', '.read sqlite3.sql'])
    add('bash', ['bash', '--version'], BASH, BASH_EXPECTED, ext='sh', command=['bash', 'bash.sh'])
    add('gfortran', ['gfortran', '--version'], FORTRAN, FORTRAN_EXPECTED, build=['gfortran', 'gfortran.f90', '-o', 'f_bin'], ext='f90', command=['./f_bin'])
    add('lua', ['lua', '-v'], LUA, LUA_EXPECTED, ext='lua', command=['lua', 'lua.lua'])
    add('git', ['git', '--version'], GIT, GIT_EXPECTED, ext='sh', command=['bash', 'git.sh'])
    return jobs


def main() -> int:
    results = []
    with tempfile.TemporaryDirectory(prefix='.verify-') as temp:
        work = Path(temp)
        for job in checks(work):
            if job['build']:
                built = subprocess.run(job['build'], cwd=work, capture_output=True, text=True, check=False)
                if built.returncode:
                    output = '[build failed] ' + (built.stderr or built.stdout)[-800:]
                else:
                    output = run(job['command'], work)
            else:
                output = run(job['command'], work)
            got = [line.strip() for line in output.splitlines() if line.strip()]
            want = [line.strip() for line in job['expected'].splitlines() if line.strip()]
            for line in want:
                results.append({'check': line.split()[0], 'tool': job['tool'], 'version': job['version'],
                                'expected': line.split(' ', 1)[1], 'observed': next((g.split(' ', 1)[1] for g in got if g.split(' ')[0] == line.split()[0]), None),
                                'passed': line in got, 'source_sha256': hashlib.sha256(job['source'].encode()).hexdigest()})
            if any(not r['passed'] for r in results if r['tool'] == job['tool']):
                results.append({'check': f"{job['tool']}-output", 'tool': job['tool'], 'passed': False, 'output': output[-1500:]})
    failed = [r for r in results if not r['passed']]
    REPORT.write_text(json.dumps({
        'date': date.today().isoformat(),
        'scope': 'Each check asks the real toolchain for the quantity behind a stored answer. A pass confirms the claim on these tool versions; it is not an academic approval.',
        'tools': sorted({f"{r['tool']}: {r['version']}" for r in results if 'version' in r}),
        'checks': results, 'failed': len(failed)}, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({'checks': len(results), 'failed': len(failed)}))
    for r in failed:
        print('FAIL', r['check'], r.get('expected'), r.get('observed'), r.get('output', '')[:600], file=sys.stderr)
    return 1 if failed else 0


if __name__ == '__main__':
    if shutil.which('git') is None:
        raise SystemExit('git is required')
    raise SystemExit(main())
