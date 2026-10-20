"""Comprueba que el libro mantiene la correspondencia con la guía ULE 2026-27.

Prueba de integridad estructural; no constituye una aprobación científica.
"""
from __future__ import annotations

import json
import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BOOK = ROOT / "books/mecanica-fluidos"


class ULESyllabusMappingTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.guide = json.loads(
            (BOOK / "bibliography/guia-docente-ule-2026-2027.json").read_text(
                encoding="utf-8"
            )
        )
        cls.manifest = json.loads(
            (BOOK / "bibliography/revision-2026-bibliografia.json").read_text(
                encoding="utf-8"
            )
        )
        cls.manual = (BOOK / "latex/manual.tex").read_text(encoding="utf-8")
        cls.plan = cls.manual.split(r"\chapter{Plan de estudio}", 1)[1].split(
            r"\backmatter", 1
        )[0]

    def test_metadata_and_program(self):
        self.assertEqual(self.guide["course"]["code"], "0710311")
        self.assertEqual(self.guide["course"]["credits_ects"], 6)
        self.assertEqual(len(self.guide["topics"]), 6)
        self.assertTrue(self.guide["syllabus_verified"])
        self.assertTrue(self.manifest["academic_guide"]["guide_contents_verified"])
        self.assertEqual(self.guide["mapping_review_status"].split(";")[0].split("_")[0], "official")

    def test_theory_mapping_matches_manuscript(self):
        ids = [t["id"] for t in self.guide["topics"]]
        self.assertEqual(ids, ["T1", "T2", "T3", "T4", "T5", "T6"])
        mapped_chapters = [n for t in self.guide["topics"] for n in t["chapters"]]
        self.assertEqual(mapped_chapters, list(range(1, 17)))
        part_names = re.findall(r"\\part\{([^}]+)\}", self.manual)
        theory_chapters = re.findall(r"\\chapter\{([^}]+)\}", self.manual)[:16]
        for t in self.guide["topics"]:
            self.assertIn(t["manual_part"], part_names)
            for heading in t["manual_chapter_titles"]:
                self.assertIn(heading, theory_chapters)
        self.assertEqual(len(theory_chapters), 16)

    def test_contact_hours(self):
        m = self.guide["methodologies"]
        kinds = ("informatics", "problem_sessions", "lectures")
        for kind in kinds:
            item = m[kind]
            self.assertEqual(item["contact"] + item["noncontact"], item["total"])
        self.assertEqual(sum(m[k]["contact"] for k in kinds), 60)
        self.assertEqual(sum(m[k]["noncontact"] for k in kinds), 90)
        self.assertEqual(m["total_hours"], 150)

    def test_grading_policy_and_source_edition_difference(self):
        a = self.guide["assessment"]
        self.assertAlmostEqual(
            a["written_exam_weight"] + a["in_class_exercises_weight"], 1.0
        )
        self.assertEqual(a["minimum_written_exam_out_of_10"], 5)
        refs = {
            r["local_source_id"]: r
            for r in self.guide["official_references"]
            if "local_source_id" in r
        }
        self.assertEqual(len(refs), 5)
        self.assertEqual(refs["ref26-white"]["year"], 2016)
        self.assertEqual(refs["ref26-tritton"]["year"], 2011)
        local = {s["id"]: s for s in self.manifest["sources"]}
        self.assertEqual(local["ref26-white"]["year"], 2011)
        self.assertEqual(local["ref26-tritton"]["year"], 1988)

    def test_study_plan_integrity(self):
        self.assertEqual(
            self.manual.count(r"\input{../content/orientacion-guia-ule-2026.tex}"),
            1,
        )
        self.assertNotIn("concepts planned", self.plan)
        self.assertEqual(self.plan.count("Objetivo de comprobación:"), 23)
        self.assertNotIn(r"\subsection*{\checkmark", self.plan)
        source = BOOK / "content/orientacion-guia-ule-2026.tex"
        self.assertTrue(source.is_file())


if __name__ == "__main__":
    unittest.main()
