#!/usr/bin/env python3
"""Regenerate reviewed procedures; never rewrite their problem banks."""
from pathlib import Path
import subprocess,sys
ROOT=Path(__file__).resolve().parents[1]
SCRIPTS=[
 'scripts/build-flight-solution-methods.py',
 'scripts/revise-fluid-solutions.py',
 'scripts/link-fluid-solutions.py',
 'books/mecanica-fluidos/scripts/make_fluid_books.py',
 'scripts/revise-legacy-solutions.py',
 'books/estructuras-aeroespaciales/scripts/make_companions.py',
 'scripts/revise-native-solutions.py',
 'scripts/revise-materials-manual.py',
 'scripts/complete-rocket-opening.py',
 'scripts/revise-technology-solutions.py',
 'scripts/revise-technology-manual.py',
 'scripts/revise-technology-exams.py',
 'books/mecanica-fluidos/scripts/check_solution_procedures.py',
]
for script in SCRIPTS:
 print(script,flush=True)
 subprocess.run([sys.executable,script],cwd=ROOT,check=True)
