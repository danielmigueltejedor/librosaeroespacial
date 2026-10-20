"""Regression checks for the turbomachinery notation cleanup."""
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANUAL = ROOT / "books/turbomaquinas/publication/turbomaquinas-ule-2026.tex"


class TurbomachineryNotationTests(unittest.TestCase):
    def test_model_equation_boxes_do_not_leak_internal_identifiers(self):
        text = MANUAL.read_text()
        forbidden = ["\\mathit{uu}", "\\mathit{gam}", "\\mathit{pz}", "\\mathit{wt3}",
                     "\\mathit{Pow}", "\\mathit{dTz}", "mathcalR", "Ctheta"]
        for code in range(1, 19):
            label = f"\\label{{eq:EC-C{code:02d}}}"
            self.assertIn(label, text)
            begin = text.rfind(r"\begin{equation}", 0, text.index(label))
            end = text.index(r"\end{equation}", text.index(label)) + len(r"\end{equation}")
            box = text[begin:end]
            for token in forbidden:
                self.assertNotIn(token, box, f"{token} still present in {label}")

    def test_notation_table_uses_mathcal_r_and_forced_vortex_row(self):
        text = MANUAL.read_text()
        self.assertIn(r"$\mathcal R$", text)
        self.assertIn(r"$k_f$", text)
        self.assertIn(r"\mathrm{s^{-1}}", text)

    def test_formula_chapter_warns_about_identifier_collision(self):
        text = MANUAL.read_text()
        self.assertIn("Advertencia de notación", text)
        self.assertIn("dos magnitudes distintas", text)

    def test_flight_covers_use_distinct_photo_files(self):
        for name, expected in [("main.tex", "cover-manual.jpg"),
                               ("problemas.tex", "cover-problemas.jpg"),
                               ("simulacros.tex", "cover-simulacros.jpg")]:
            text = (ROOT / "books/mecanica-vuelo" / name).read_text()
            self.assertIn(f"assets/{expected}", text, name)
        meta = json.loads((ROOT / "books/mecanica-vuelo/assets/cover-photo.json").read_text())
        self.assertEqual(len(meta["volumes"]), 3)
        photos = {v["output"] for v in meta["volumes"]}
        self.assertEqual(photos, {"assets/cover-manual.jpg", "assets/cover-problemas.jpg",
                                  "assets/cover-simulacros.jpg"})
        for volume in meta["volumes"]:
            self.assertTrue(volume["license"].startswith("PD-USGov-NASA"))
            self.assertTrue(volume["consulted_on"])
