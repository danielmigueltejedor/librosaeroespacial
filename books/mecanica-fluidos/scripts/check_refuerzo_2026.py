#!/usr/bin/env python3
"""Pruebas numéricas e integridad del refuerzo bibliográfico 2026.

No certifica toda la edición ni reemplaza una auditoría independiente.
Solo usa la biblioteca estándar de Python.
"""
from __future__ import annotations

import json
import math
from pathlib import Path

BOOK = Path(__file__).resolve().parents[1]


def near(actual: float, expected: float, tol: float = 1e-9) -> None:
    assert math.isclose(actual, expected, rel_tol=tol, abs_tol=tol), (
        actual,
        expected,
    )


def test_hydrostatics() -> None:
    rho, g, b, H, h0 = 1000.0, 9.81, 1.2, 1.5, 0.6
    A, hc = b * H, h0 + H / 2.0
    Ig = b * H**3 / 12.0
    force = rho * g * A * hc
    hcp = hc + Ig / (A * hc)
    near(force, 23838.3)
    near(hcp, 1.4888888888888889)
    assert hc < hcp < h0 + H
    # Límite: placa con borde superior en la superficie libre
    near(H / 2 + (b * H**3 / 12) / (b * H * H / 2), 2 * H / 3)


def test_couette_poiseuille() -> None:
    h, U, mu, G = 0.002, 0.4, 0.020, -8000.0
    P = G * h * h / (2.0 * mu * U)
    q = U * h / 2.0 + G * h**3 / (12.0 * mu)
    tau_0, tau_h = mu * U / h + G * h / 2, mu * U / h - G * h / 2
    near(P, -2.0)
    near(q, 0.00013333333333333334)
    near(tau_0, -4.0)
    near(tau_h, 12.0)
    u = lambda y: U * y / h + G * y * (h - y) / (2.0 * mu)
    near(u(0.0), 0.0)
    near(u(h), U)
    near(u(0.001), 0.0)
    assert u(0.0005) < 0 < u(0.0015)
    # q > 0 iff P > -3 ; wall flow reverses iff P < -1
    assert -3.0 < P < -1.0


def test_pitot() -> None:
    dp, rho = 240.0, 1.20
    speed = math.sqrt(2 * dp / rho)
    near(speed, 20.0)
    near(math.sqrt(2 * (4 * dp) / rho), 2 * speed)
    bound = 0.5 * (2.0 / dp + 0.02 / rho)
    near(bound, 0.0125)


def test_extensional_flow() -> None:
    a, rho, mu = 2.0, 1000.0, 0.001
    x, y = 0.20, 0.10
    # u = (a*x, -a*y, 0): div=0, Laplacian=0.
    div = a - a
    adv = (a * a * x, a * a * y)
    pressure_offset = -rho * a * a * (x * x + y * y) / 2
    grad_p = (-rho * a * a * x, -rho * a * a * y)
    near(div, 0.0)
    near(pressure_offset, -100.0)
    near(2 * mu * a, 0.004)
    for acceleration, pressure_gradient in zip(adv, grad_p):
        near(rho * acceleration, -pressure_gradient)


def test_references() -> None:
    data = json.loads(
        (BOOK / "bibliography/revision-2026-bibliografia.json").read_text(
            encoding="utf-8"
        )
    )
    assert len(data["sources"]) == 5
    assert data["academic_guide"]["guide_contents_verified"] is True
    guide = json.loads(
        (BOOK / "bibliography/guia-docente-ule-2026-2027.json").read_text(
            encoding="utf-8"
        )
    )
    assert guide["syllabus_verified"] is True
    assert len(guide["topics"]) == 6
    manual = (BOOK / "latex/manual.tex").read_text(encoding="utf-8")
    refs = [source["id"] for source in data["sources"]]
    for key in refs:
        assert manual.count(r"\bibitem{" + key + "}") == 1, key
    contents = []
    for entry in data["new_derived_checks"]:
        relative = entry["manuscript"]
        fragment = BOOK / relative
        assert fragment.is_file(), fragment
        assert (
            manual.count(r"\input{../" + relative + "}") == 1
        ), relative
        contents.append(fragment.read_text(encoding="utf-8"))
    for key in refs:
        assert any(r"\cite{" + key + "}" in txt for txt in contents) or (
            r"\cite{" + key + "}" in manual
        )
    assert len(set(refs)) == len(refs)


if __name__ == "__main__":
    for test in (
        test_hydrostatics,
        test_couette_poiseuille,
        test_pitot,
        test_extensional_flow,
        test_references,
    ):
        test()
        print("OK", test.__name__)
