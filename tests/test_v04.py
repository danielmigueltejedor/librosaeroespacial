from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from framework.aerobooks.exercise_check import dependency_lock, exercise_v04_issues
from framework.aerobooks.research import exercise_issues


def _source() -> dict:
    return {
        "id": "SRC-WHITE",
        "title": "Fluid Mechanics",
        "kind": "textbook",
        "tier": "B",
        "tier_detail": "A3",
        "role": ["theory"],
        "status": "verified",
        "lifecycle": "accepted",
        "content_access": "full",
        "consulted": True,
        "rights": "Cita breve.",
    }


def _derivation() -> dict:
    return {
        "id": "DRV-COUETTE",
        "sources": ["SRC-WHITE"],
        "result": "tau = mu * U / h",
        "status": "audited",
    }


def _verification(sources: dict, derivations: dict, **extra) -> dict:
    item = {
        "author": {"agent": "author-a", "expression": "mu * U / h"},
        "independent": {
            "agent": "reviewer-b",
            "independence": "independent_model",
            "expression": "mu * U / h",
        },
        "defines": "tau",
        "original_equation": "tau * h - mu * U",
        "quantities": {"tau": "Pa", "mu": "Pa*s", "U": "m/s", "h": "m"},
        "bindings_range": {"mu": [0.01, 1.0], "U": [0.2, 4.0], "h": [0.001, 0.02]},
        "limit_cases": [{
            "name": "U=0",
            "bindings": {"mu": 0.4, "U": 0.0, "h": 0.002},
            "expression": "mu * U / h",
            "expected": 0.0,
        }],
        "parametric_cases": 100,
        "seed": 7,
        "tolerance": 1e-9,
        "sources": ["SRC-WHITE"],
        "equations": ["DRV-COUETTE"],
    }
    item["dependency_lock"] = dependency_lock(
        sources, derivations, item["sources"], item["equations"],
    )
    item.update(extra)
    return item


def _exercise(verification: dict) -> dict:
    return {
        "id": "EX-COUETTE",
        "statement": "Halla el esfuerzo en un Couette plano.",
        "origin": "aerobooks",
        "data": {"mu": "0.4 Pa s", "U": "1.5 m/s", "h": "2 mm"},
        "unknowns": ["tau"],
        "hypotheses": ["fluido newtoniano", "flujo laminar desarrollado"],
        "solution": "tau = mu U / h",
        "result": "300 Pa",
        "units": "Pa",
        "numerical_tolerance": 1e-9,
        "checks": [{"expected": 300.0, "actual": 300.0, "tolerance": 1e-9}],
        "reviewer": "reviewer-b",
        "status": "published",
        "reviews": {
            "mathematical": "pass",
            "units": "pass",
            "independent_solution": "pass",
            "computational": "pass",
        },
        "computational": {"applicable": True, "tool": "aerobooks"},
        "verification": verification,
    }


class ExerciseGateV04Tests(unittest.TestCase):
    def setUp(self) -> None:
        self.sources = {"SRC-WHITE": _source()}
        self.derivations = {"DRV-COUETTE": _derivation()}

    def test_couette_passes_the_eight_checks(self) -> None:
        row = _exercise(_verification(self.sources, self.derivations))
        self.assertEqual(exercise_v04_issues(row, self.sources, self.derivations), [])

    def test_rubber_stamp_is_not_enough(self) -> None:
        missing = dict(_exercise({}))
        missing.pop("verification")
        self.assertIn(
            "no basta",
            " ".join(item["message"] for item in exercise_v04_issues(missing, self.sources, self.derivations)),
        )
        stamped = _exercise({
            "independent": {"agent": "reviewer-b", "agrees": True},
        })
        self.assertIn(
            "visto bueno",
            " ".join(item["message"] for item in exercise_v04_issues(stamped, self.sources, self.derivations)),
        )

    def test_same_agent_and_wrong_units_fail(self) -> None:
        verification = _verification(
            self.sources,
            self.derivations,
            independent={
                "agent": "author-a",
                "independence": "same_model_new_pass",
                "expression": "mu * U / h",
            },
            quantities={"tau": "m", "mu": "Pa*s", "U": "m/s", "h": "m"},
        )
        messages = " ".join(
            item["message"]
            for item in exercise_v04_issues(_exercise(verification), self.sources, self.derivations)
        )
        self.assertIn("no es independiente", messages)
        self.assertIn("unidades", messages)

    def test_limit_and_parametric_count(self) -> None:
        verification = _verification(self.sources, self.derivations, parametric_cases=99, limit_cases=[])
        messages = " ".join(
            item["message"]
            for item in exercise_v04_issues(_exercise(verification), self.sources, self.derivations)
        )
        self.assertIn("100 casos", messages)
        self.assertIn("casos límite", messages)

    def test_student_notes_cannot_back_the_equation(self) -> None:
        notes = dict(self.sources["SRC-WHITE"], tier="D", tier_detail="D2")
        sources = {"SRC-WHITE": notes}
        verification = _verification(sources, self.derivations)
        messages = " ".join(
            item["message"] for item in exercise_v04_issues(_exercise(verification), sources, self.derivations)
        )
        self.assertIn("no puede respaldar", messages)

    def test_changed_dependency_reopens_the_exercise(self) -> None:
        verification = _verification(self.sources, self.derivations)
        changed = dict(self.sources["SRC-WHITE"], title="Fluid Mechanics, otra edición")
        messages = " ".join(
            item["message"]
            for item in exercise_v04_issues(
                _exercise(verification),
                {"SRC-WHITE": changed},
                self.derivations,
            )
        )
        self.assertIn("ha cambiado desde la revisión", messages)

    def test_ledger_accepts_a_complete_exercise(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            verification = _verification(self.sources, self.derivations)
            (root / "sources").mkdir()
            (root / "sources" / "manifest.json").write_text(
                json.dumps({"sources": [_source()]}), encoding="utf-8",
            )
            (root / "derivations").mkdir()
            with (root / "derivations" / "ledger.jsonl").open("w", encoding="utf-8") as fh:
                fh.write(json.dumps(_derivation()) + "\n")
            (root / "exercises").mkdir()
            with (root / "exercises" / "ledger.jsonl").open("w", encoding="utf-8") as fh:
                fh.write(json.dumps(_exercise(verification)) + "\n")
            self.assertEqual(exercise_issues(root), [])


if __name__ == "__main__":
    unittest.main()
