"""Numeric and editorial regression checks for MATMO advanced study materials.

These checks confirm arithmetic and inclusion, NOT the validity of physical
assumptions, accepted inspection intervals or the legal applicability of a rule.
"""
from __future__ import annotations

import math
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MATMO = ROOT / "books" / "materiales-mantenimiento-motores"
CONTENT = MATMO / "content"


class TestMATMOAdvanced(unittest.TestCase):
    def test_multiaxial_stress(self) -> None:
        sx, sy, tau = 120.0, -40.0, 30.0
        center = (sx + sy) / 2.0
        radius = math.hypot((sx - sy) / 2.0, tau)
        von_mises = math.sqrt(sx**2 - sx * sy + sy**2 + 3 * tau**2)
        self.assertAlmostEqual(center + radius, 125.440037, places=5)
        self.assertAlmostEqual(center - radius, -45.440037, places=5)
        self.assertAlmostEqual(von_mises, 153.297097, places=5)
        self.assertAlmostEqual(center * 2, sx + sy, places=8)

    def test_paris_m2_integration(self) -> None:
        y, stress_range, c = 1.05, 80.0, 1e-11
        ai, af = .001, .004
        cycles = math.log(af / ai) / (c * math.pi * (y * stress_range) ** 2)
        self.assertAlmostEqual(cycles, 6253843.541742, places=3)
        self.assertGreater(cycles, 0)

    def test_fibre_mixture(self) -> None:
        vf, ef, em = .55, 200.0, 3.0
        longitudinal = vf * ef + (1 - vf) * em
        transversal = 1 / (vf / ef + (1 - vf) / em)
        density = vf * 1800.0 + (1 - vf) * 1200.0
        self.assertAlmostEqual(longitudinal, 111.35, places=4)
        self.assertAlmostEqual(transversal, 6.5466448445, places=7)
        self.assertAlmostEqual(density, 1530.0, places=5)
        self.assertLess(transversal, longitudinal)

    def test_inspection_negative_bayes(self) -> None:
        prevalence = .05
        detection = .90
        false_positive = .02
        posterior = (prevalence * (1 - detection)) / (
            prevalence * (1 - detection) + (1 - prevalence) * (1 - false_positive)
        )
        self.assertAlmostEqual(posterior, .00534188034188, places=11)
        self.assertGreater(posterior, 0)

    def test_strength_and_stiffness_design(self) -> None:
        force, length, extension = 15000.0, .5, .001
        def design(e: float, rho: float, admissible: float) -> tuple[float, float]:
            area = max(force / admissible, force * length / (e * extension))
            return area * 1e6, rho * length * area
        area_a, mass_a = design(70e9, 2800, 200e6)
        area_b, mass_b = design(110e9, 4500, 600e6)
        self.assertAlmostEqual(area_a, 107.1428571429, places=7)
        self.assertAlmostEqual(mass_a, .15, places=10)
        self.assertAlmostEqual(area_b, 68.1818181818, places=7)
        self.assertAlmostEqual(mass_b, .153409090909, places=10)
        self.assertLess(mass_a, mass_b)

    def test_weibull_conditional_reliability(self) -> None:
        def reliability(t: float) -> float:
            return math.exp(-(t / 1500) ** 2)
        self.assertAlmostEqual(reliability(1000), .64118038843, places=10)
        self.assertAlmostEqual(reliability(1100) / reliability(1000),
                               .910889819746, places=10)
        self.assertNotAlmostEqual(reliability(100), .910889819746, places=2)

    def test_new_sources_are_used_once(self) -> None:
        inputs = (
            ("main.tex", ("profundizacion-aplicada",)),
            ("problemas.tex", ("problemas-avanzados-resueltos",)),
            ("simulacros.tex", (
                "simulacros-avanzados-teoria-enunciados",
                "simulacros-avanzados-teoria-soluciones",
            )),
        )
        for filename, modules in inputs:
            doc = (MATMO / filename).read_text(encoding="utf-8")
            for module in modules:
                with self.subTest(doc=filename, module=module):
                    self.assertEqual(doc.count(r"\input{content/" + module + ".tex}"), 1)
                    self.assertTrue((CONTENT / (module + ".tex")).is_file())

    def test_advanced_questions_have_matched_solutions(self) -> None:
        pattern = r"\\section\*\{(AT\d\d)\."
        statements = (CONTENT / "simulacros-avanzados-teoria-enunciados.tex").read_text()
        answers = (CONTENT / "simulacros-avanzados-teoria-soluciones.tex").read_text()
        a = re.findall(pattern, statements)
        b = re.findall(pattern, answers)
        self.assertEqual(a, [f"AT{i:02d}" for i in range(1, 13)])
        self.assertEqual(a, b)

    def test_advanced_problems_and_figures(self) -> None:
        problems = (CONTENT / "problemas-avanzados-resueltos.tex").read_text()
        theory = (CONTENT / "profundizacion-aplicada.tex").read_text()
        ids = re.findall(r"\\section\{(PA\d\d)\.", problems)
        self.assertEqual(ids, [f"PA{i:02d}" for i in range(1, 7)])
        self.assertEqual(theory.count(r"\begin{figure}"), 3)
        self.assertEqual(theory.count(r"\end{figure}"), 3)
        self.assertEqual(theory.count(r"\begin{tikzpicture}"), 3)
        self.assertEqual(theory.count(r"\end{tikzpicture}"), 3)


if __name__ == "__main__":
    unittest.main()
