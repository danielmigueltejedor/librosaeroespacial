#!/bin/sh
set -eu
cd "$(dirname "$0")/.."
if [ ! -x work/runtime/bin/python ]; then
  mkdir -p work
  python3.12 -m venv work/runtime
  work/runtime/bin/python -m pip install -r requirements.txt
fi
if [ ! -d simulations/jsbsim-upstream/.git ]; then
  git clone --depth 1 --branch v1.3.3 https://github.com/JSBSim-Team/jsbsim.git simulations/jsbsim-upstream
fi
task_jsbsim_commit=$(git -C simulations/jsbsim-upstream rev-parse HEAD)
test "$task_jsbsim_commit" = 66f7fafc07fe13e7ede9db20873030fed2881713
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1
work/runtime/bin/python scripts/verify_models.py
work/runtime/bin/python scripts/additional_checks.py
work/runtime/bin/python scripts/run_jsbsim.py > reports/jsbsim-run.log 2>&1
work/runtime/bin/python scripts/run_xml.py > reports/xml-run.log 2>&1
work/runtime/bin/python scripts/run_endurance.py > reports/endurance-run.log 2>&1
work/runtime/bin/python scripts/problem_bank.py
work/runtime/bin/python scripts/render_problems.py
work/runtime/bin/python scripts/exams.py
work/runtime/bin/python scripts/workshops.py
work/runtime/bin/python scripts/source_registry.py
work/runtime/bin/python scripts/figures.py
work/runtime/bin/python scripts/validate_problem_bank.py
work/runtime/bin/python scripts/validate_all_cases.py
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
latexmk -pdf -interaction=nonstopmode -halt-on-error problemas.tex
latexmk -pdf -interaction=nonstopmode -halt-on-error simulacros.tex
work/runtime/bin/python scripts/visual_qa.py
work/runtime/bin/python scripts/final_inventory.py
work/runtime/bin/python scripts/write_final_audits.py
printf '%s\n' 'Reconstrucción terminada. Consulte informes y límites de validación.'
