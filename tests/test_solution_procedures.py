"""Learning regressions: calculations must remain visible and traceable."""
import importlib.util
import json
import math
from pathlib import Path
import sys

import pytest

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from solution_steps import numeric_steps, expression, unit


def test_substitution_is_not_collapsed_into_a_bare_result():
    tex,rows=numeric_steps([
        dict(target='a',expression='F/m',unit='m/s**2',why='Newton'),
        dict(target='t',expression='V/a',unit='s',why='Integrar velocidad'),
    ],dict(F=150000,m=70000,V=75))
    assert '(150000)' in tex and '(70000)' in tex
    assert '(75)' in tex and '35' in tex
    assert math.isclose(rows[0]['value'],15/7)
    assert rows[1]['value']==35


def test_scalar_calculator_rejects_execution_and_undefined_inputs():
    with pytest.raises(ValueError):expression('__import__("os").system("bad")')
    with pytest.raises(ValueError):numeric_steps([dict(expression='missing+1')])
    assert unit('MPa*m**.5')==r'\mathrm{MPa\,m^{.5}}'


def test_plane_route_contains_the_whole_chain_and_independent_energy_check():
    file=ROOT/'books/mecanica-fluidos/solutions/procedures.py'
    spec=importlib.util.spec_from_file_location('fluid_routes',file)
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    route=module.ROUTES[1]
    _,rows=numeric_steps(route['steps'],dict(m=70000,F=150000,V=75))
    v={r['target']:r['value'] for r in rows}
    assert math.isclose(v['a'],150000/70000)
    assert v['t']==35 and v['s']==1312.5
    assert v['W']==v['E']==196875000
    assert 'v_0=0' in route['strategy']
    assert 'integr' in route['steps'][2]['why'].lower()
    assert '2625' in route['check']


def test_every_fluid_solution_has_its_own_reasoning_and_dimensional_check():
    book=ROOT/'books/mecanica-fluidos'
    rows=json.loads((book/'solutions/source-cases.json').read_text())
    source=(book/'latex/manual.tex').read_text()
    assert len(rows)==128
    for row in rows:
        token=f'../solutions/generated/mf-{row["index"]:03}.tex'
        assert source.count(token)==1
        body=(book/'solutions/generated'/f'mf-{row["index"]:03}.tex').read_text()
        assert 'Elección del procedimiento' in body and r'\begin{enumerate}' in body
        assert r'\approx' in body
    dimensions=json.loads((book/'reports/solution-dimensions.json').read_text())
    assert dimensions['passed']==370 and dimensions['failed']==0


def test_numeric_flight_results_have_a_method_instead_of_replaying_literals():
    report=json.loads((ROOT/'reports/solution-procedure-native.json').read_text())
    for row in report['records']:
        if row['book']=='mecanica-vuelo' and row.get('non_scalar_results'):
            assert (ROOT/'books/mecanica-vuelo/solutions/methods'/(row['key']+'.tex')).is_file(),row['key']
    for key,phrase in [('T05','producto'),('T06','mitad'),('T09','Integral'),('T13','Runge'),('T14','rejilla')]:
        text=(ROOT/'books/mecanica-vuelo/solutions/methods'/(key+'.tex')).read_text()
        assert phrase.lower() in text.lower()


def test_detailed_legacy_solutions_preserve_all_original_figure_labels():
    # The fingerprint list is authored once from the pre-revision edition.
    report=json.loads((ROOT/'reports/solution-figure-preservation.json').read_text())
    import re
    for row in report['files']:
        source=(ROOT/row['path']).read_text()
        labels=set(re.findall(r'\\(?:label|studiumcaption)\{(fig:[^}]+)\}',source))
        assert set(row['figure_labels'])<=labels
        assert source.count(r'\begin{tikzpicture}')>=row['tikz_pictures']


def test_every_method_and_solution_is_included_in_the_reader_sources():
    records=json.loads((ROOT/'reports/solution-procedure-native.json').read_text())['records']
    for row in records:
        book=ROOT/'books'/row['book']
        token='solutions/generated/'+row['key']+'.tex'
        sources=[p for p in book.rglob('*.tex') if 'solutions' not in p.parts]
        assert any(token in p.read_text() for p in sources),(row['book'],row['key'])
        if row['book']=='mecanica-vuelo' and row.get('non_scalar_results'):
            assert 'solutions/methods/'+row['key']+'.tex' in (book/'solutions/generated'/(row['key']+'.tex')).read_text()
    technology=ROOT/'books/tecnologia-aeroespacial/content/exam-solutions.tex'
    for n in (1,2,3):
        assert f'solutions/generated/EX{n}.tex' in technology.read_text()
    fluid=(ROOT/'books/mecanica-fluidos/latex/manual.tex').read_text()
    assert fluid.count(r'\hyperref[solution:mf-')==16


def test_isa_substitution_keeps_reference_temperature_and_exponent_operations():
    from solution_steps import scalar_tex
    tex=scalar_tex('101325*(T/288.15)**(9.80665/(287.05287*.0065))',{'T':271.9})
    assert r'\frac{(271.9)}{288.15}' in tex
    assert r'\frac{9.80665}{287.05287\cdot 0.0065}' in tex
    assert '1.181789' not in tex


def test_variable_names_do_not_resolve_to_sympy_library_functions():
    from solution_steps import scalar_tex
    assert r'\mathrm{trace}' in scalar_tex('trace**2-4*det')
    assert scalar_tex('erfc(x)').startswith(r'\operatorname{erfc}')


def test_jet_efficiency_respects_the_requested_negligible_fuel_approximation():
    file=ROOT/'books/mecanica-fluidos/solutions/procedures.py'
    spec=importlib.util.spec_from_file_location('fluid_jet_route',file)
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    _,rows=numeric_steps(module.ROUTES[9]['steps'],dict(ma=50,mf=1,v0=250,ve=600))
    values={r['target']:r['value'] for r in rows}
    assert values['F']==18100 and values['Pu']==4525000
    assert math.isclose(values['etaApprox'],10/17)
    assert values['etap']>values['etaApprox']
    source=(ROOT/'books/mecanica-fluidos/latex/manual.tex').read_text()
    assert r'\eta_p \approx 0{,}594' not in source
    assert source.count(r'\eta_p \approx 0{,}5882')>=2
