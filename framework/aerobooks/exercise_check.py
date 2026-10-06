"""AeroBooks 0.4 exercise gate.

A solved exercise is not accepted because one model wrote it and another
said it looked fine. The framework reruns the independent expression,
the units, the original equation, the limit cases and 100 parametric
draws, and it rejects the result if a cited source or derivation changed
after the review.
"""

from __future__ import annotations

import ast
import hashlib
import json
import operator
import random
from typing import Iterable

PARAMETRIC_CASES = 100
INDEPENDENT = {"independent_model", "human", "hybrid"}
BASE_UNITS = {
    "1": {},
    "kg": {"M": 1},
    "m": {"L": 1},
    "s": {"T": 1},
    "N": {"M": 1, "L": 1, "T": -2},
    "Pa": {"M": 1, "L": -1, "T": -2},
    "J": {"M": 1, "L": 2, "T": -2},
    "W": {"M": 1, "L": 2, "T": -3},
}
BINOPS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
}
UNARY = {ast.UAdd: operator.pos, ast.USub: operator.neg}


def issue(code: str, message: str) -> dict:
    return {"severity": "error", "code": code, "message": message}


def fingerprint(payload: dict) -> str:
    blob = json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(blob.encode("utf-8")).hexdigest()


def dependency_lock(sources: dict[str, dict], derivations: dict[str, dict], cited_sources: Iterable[str], cited_equations: Iterable[str]) -> dict:
    return {
        "sources": {sid: fingerprint(sources[sid]) for sid in cited_sources},
        "equations": {did: fingerprint(derivations[did]) for did in cited_equations},
    }


def eval_arith(expression: str, env: dict[str, float]) -> float:
    tree = ast.parse(expression, mode="eval")

    def walk(node: ast.AST) -> float:
        if isinstance(node, ast.Expression):
            return walk(node.body)
        if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
            return float(node.value)
        if isinstance(node, ast.Name):
            if node.id not in env:
                raise ValueError(f"variable libre {node.id}")
            return float(env[node.id])
        if isinstance(node, ast.UnaryOp) and type(node.op) in UNARY:
            return UNARY[type(node.op)](walk(node.operand))
        if isinstance(node, ast.BinOp) and type(node.op) in BINOPS:
            return BINOPS[type(node.op)](walk(node.left), walk(node.right))
        raise ValueError("expresión no aritmética")

    return walk(tree)


def _add_dim(left: dict[str, int], right: dict[str, int], scale: int = 1) -> dict[str, int]:
    keys = set(left) | set(right)
    out = {}
    for key in keys:
        value = left.get(key, 0) + scale * right.get(key, 0)
        if value:
            out[key] = value
    return out


def parse_unit(text: str) -> dict[str, int]:
    raw = text.replace("·", "*").replace(" ", "")
    if raw in {"", "1", "-"}:
        return {}
    if raw.count("/") > 1:
        raise ValueError(f"unidad ambigua {text}")
    if "/" in raw:
        num, den = raw.split("/", 1)
        return _add_dim(_parse_product(num), _parse_product(den), scale=-1)
    return _parse_product(raw)


def _parse_product(text: str) -> dict[str, int]:
    dim: dict[str, int] = {}
    if not text:
        return dim
    for part in text.split("*"):
        if "^" in part:
            name, power_text = part.split("^", 1)
            power = int(power_text)
        else:
            name, power = part, 1
        if name not in BASE_UNITS:
            raise ValueError(f"unidad desconocida {name}")
        dim = _add_dim(dim, BASE_UNITS[name], scale=power)
    return dim


def _dim_walk(node: ast.AST, quantities: dict[str, str]) -> dict[str, int]:
    if isinstance(node, ast.Expression):
        return _dim_walk(node.body, quantities)
    if isinstance(node, ast.Constant):
        return {}
    if isinstance(node, ast.Name):
        if node.id not in quantities:
            raise ValueError(f"{node.id} no tiene unidad")
        return parse_unit(quantities[node.id])
    if isinstance(node, ast.UnaryOp):
        return _dim_walk(node.operand, quantities)
    if isinstance(node, ast.BinOp) and isinstance(node.op, (ast.Add, ast.Sub)):
        left = _dim_walk(node.left, quantities)
        right = _dim_walk(node.right, quantities)
        if left != right:
            raise ValueError("suma de dimensiones distintas")
        return left
    if isinstance(node, ast.BinOp) and isinstance(node.op, ast.Mult):
        return _add_dim(_dim_walk(node.left, quantities), _dim_walk(node.right, quantities))
    if isinstance(node, ast.BinOp) and isinstance(node.op, ast.Div):
        return _add_dim(
            _dim_walk(node.left, quantities),
            _dim_walk(node.right, quantities),
            scale=-1,
        )
    if isinstance(node, ast.BinOp) and isinstance(node.op, ast.Pow):
        if not isinstance(node.right, ast.Constant) or not isinstance(node.right.value, int):
            raise ValueError("exponente no entero")
        base = _dim_walk(node.left, quantities)
        return {key: value * node.right.value for key, value in base.items() if value}
    raise ValueError("expresión dimensional no permitida")


def expression_dimensions(expression: str, quantities: dict[str, str]) -> dict[str, int]:
    return _dim_walk(ast.parse(expression, mode="eval"), quantities)


def _low_tier(source: dict) -> bool:
    detail = str(source.get("tier_detail") or "")
    tier = source.get("tier")
    return tier in {"D", "E"} or detail == "E" or detail.startswith("D")


def _sample(rng: random.Random, ranges: dict) -> dict[str, float]:
    env = {}
    for name, bounds in ranges.items():
        if not isinstance(bounds, (list, tuple)) or len(bounds) != 2:
            raise ValueError(f"rango inválido para {name}")
        low, high = float(bounds[0]), float(bounds[1])
        if low >= high:
            raise ValueError(f"rango vacío para {name}")
        env[name] = rng.uniform(low, high)
    return env


def exercise_v04_issues(row: dict, sources: dict[str, dict], derivations: dict[str, dict]) -> list[dict]:
    eid = row.get("id", "?")
    if row.get("status") not in {"solved", "published"}:
        return []
    verification = row.get("verification")
    if not isinstance(verification, dict):
        return [issue(
            "V04EX",
            f"{eid}: no basta con que otro agente diga que está bien. "
            "Falta la verificación 0.4: solución propia, solución independiente, "
            "unidades, ecuaciones originales, casos límite, 100 casos paramétricos, "
            "fuentes y dependencias congeladas.",
        )]

    issues: list[dict] = []
    author = verification.get("author") or {}
    independent = verification.get("independent") or {}
    author_agent = str(author.get("agent") or "").strip()
    independent_agent = str(independent.get("agent") or "").strip()
    author_expr = str(author.get("expression") or "").strip()
    independent_expr = str(independent.get("expression") or "").strip()
    if not author_agent or not author_expr:
        issues.append(issue("V04EX", f"{eid}: falta la solución calculada por el autor"))
    if (
        not independent_agent
        or not independent_expr
        or independent.get("independence") not in INDEPENDENT
        or independent_agent == author_agent
    ):
        issues.append(issue(
            "V04EX",
            f"{eid}: la segunda solución no es independiente; un visto bueno no sustituye el recálculo",
        ))

    quantities = verification.get("quantities") or {}
    defines = verification.get("defines")
    original = str(verification.get("original_equation") or "").strip()
    if not original or not defines or not isinstance(quantities, dict):
        issues.append(issue("V04EX", f"{eid}: faltan la ecuación original y las unidades de cada magnitud"))
    else:
        try:
            expression_dimensions(original, quantities)
            solved_dim = expression_dimensions(author_expr, quantities) if author_expr else {}
            if defines not in quantities or solved_dim != parse_unit(quantities[defines]):
                issues.append(issue("V04EX", f"{eid}: las unidades de la solución no coinciden con {defines}"))
        except (ValueError, SyntaxError, ZeroDivisionError) as exc:
            issues.append(issue("V04EX", f"{eid}: unidades incoherentes ({exc})"))

    tolerance = verification.get("tolerance")
    ranges = verification.get("bindings_range") or {}
    seed = verification.get("seed")
    count = verification.get("parametric_cases")
    limits = verification.get("limit_cases") or []
    if not isinstance(limits, list) or not limits:
        issues.append(issue("V04EX", f"{eid}: no hay casos límite recalculados"))
    if count != PARAMETRIC_CASES or not isinstance(seed, int) or not isinstance(tolerance, (int, float)):
        issues.append(issue("V04EX", f"{eid}: hacen falta 100 casos paramétricos con semilla y tolerancia"))
        return _with_source_and_lock(eid, verification, sources, derivations, issues)

    if author_expr and independent_expr and original and defines and isinstance(ranges, dict):
        try:
            _run_cases(
                eid,
                author_expr,
                independent_expr,
                original,
                defines,
                ranges,
                limits,
                int(seed),
                float(tolerance),
                issues,
            )
        except (ValueError, SyntaxError, ZeroDivisionError, TypeError) as exc:
            issues.append(issue("V04EX", f"{eid}: no se pudieron ejecutar los casos ({exc})"))

    return _with_source_and_lock(eid, verification, sources, derivations, issues)


def _run_cases(eid, author_expr, independent_expr, original, defines, ranges, limits, seed, tolerance, issues) -> None:
    parametric_fail = 0
    independent_fail = 0
    rng = random.Random(seed)
    for _ in range(PARAMETRIC_CASES):
        env = _sample(rng, ranges)
        author_value = eval_arith(author_expr, env)
        other_value = eval_arith(independent_expr, env)
        if abs(author_value - other_value) > tolerance:
            independent_fail += 1
        env[defines] = author_value
        residual = eval_arith(original, env)
        if abs(residual) > tolerance:
            parametric_fail += 1
    if independent_fail:
        issues.append(issue(
            "V04EX",
            f"{eid}: la solución independiente no coincide en {independent_fail} de {PARAMETRIC_CASES} casos",
        ))
    if parametric_fail:
        issues.append(issue(
            "V04EX",
            f"{eid}: la ecuación original no se cumple en {parametric_fail} de {PARAMETRIC_CASES} casos",
        ))

    for case in limits:
        if not isinstance(case, dict):
            issues.append(issue("V04EX", f"{eid}: caso límite ilegible"))
            continue
        name = case.get("name", "?")
        bindings = dict(case.get("bindings") or {})
        expression = case.get("expression") or author_expr
        if "expected" not in case:
            issues.append(issue("V04EX", f"{eid}: el caso límite {name} no tiene valor esperado"))
            continue
        got = eval_arith(expression, bindings)
        if abs(got - float(case["expected"])) > tolerance:
            issues.append(issue("V04EX", f"{eid}: el caso límite {name} no se cumple"))
            continue
        bindings[defines] = got
        residual = eval_arith(original, bindings)
        if abs(residual) > tolerance:
            issues.append(issue("V04EX", f"{eid}: el caso límite {name} no satisface la ecuación original"))


def _with_source_and_lock(eid, verification, sources, derivations, issues) -> list[dict]:
    cited_sources = list(verification.get("sources") or [])
    cited_equations = list(verification.get("equations") or [])
    if not cited_sources or not cited_equations:
        issues.append(issue("V04EX", f"{eid}: las ecuaciones usadas no declaran fuentes"))
    else:
        for sid in cited_sources:
            source = sources.get(sid)
            if not source:
                issues.append(issue("V04EX", f"{eid}: la fuente {sid} no está en el manifiesto"))
            elif _low_tier(source):
                issues.append(issue("V04EX", f"{eid}: {sid} no puede respaldar la ecuación"))
        for did in cited_equations:
            derivation = derivations.get(did)
            if not derivation:
                issues.append(issue("V04EX", f"{eid}: la ecuación {did} no está en el ledger de derivaciones"))
                continue
            backing = set(derivation.get("sources") or [])
            if not backing.intersection(cited_sources):
                issues.append(issue("V04EX", f"{eid}: {did} no está respaldada por las fuentes citadas"))

    lock = verification.get("dependency_lock")
    if not isinstance(lock, dict):
        issues.append(issue("V04EX", f"{eid}: no hay dependencias congeladas desde la revisión"))
        return issues
    try:
        current = dependency_lock(sources, derivations, cited_sources, cited_equations)
    except KeyError as exc:
        issues.append(issue("V04EX", f"{eid}: la dependencia {exc} ya no está disponible"))
        return issues
    if current != {"sources": lock.get("sources") or {}, "equations": lock.get("equations") or {}}:
        issues.append(issue("V04EX", f"{eid}: una dependencia ha cambiado desde la revisión"))
    return issues
