"""Compact builder for numeric (NUMERICAL) biology exercises in the Studium solution format."""
def num(role, prompt, expected, quotes, method, given, unknown, model, assumptions, development, steps, result, interpretation, limitations, mistakes, difficulty=None):
    d = dict(role=role, problem_type='NUMERICAL', prompt=prompt, expected=expected, quotes=quotes, method=method,
             solution=dict(given=[dict(symbol=s, value=v, unit=u, meaning=m) for s, v, u, m in given], unknown=unknown,
                           model=[dict(name=n, latex=l, symbolic=sy) for n, l, sy in model],
                           assumptions=assumptions, development=development,
                           steps=[dict(text=t, equation=e, expression=x, expected=ev, unit=u) for t, e, x, ev, u in steps],
                           result=result, interpretation=interpretation, limitations=limitations, mistakes=mistakes))
    if difficulty: d['difficulty'] = difficulty
    return d
