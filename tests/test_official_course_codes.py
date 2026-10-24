"""A release report must use the official ULE identity of each subject."""
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
LABELS = {
    "estructuras-aeroespaciales": "Teoría de Estructuras",
    "mecanica-fluidos": "Mecánica de Fluidos",
    "turbomaquinas": "Turbomáquinas",
    "tecnologia-aeroespacial": "Tecnología Aeroespacial",
    "motores-cohete": "Motores Cohete",
    "mecanica-vuelo": "Mecánica de Vuelo",
    "materiales-mantenimiento-motores": "Materiales y Mantenimiento",
}


def test_version_four_inventory_course_codes_are_official():
    guides = json.loads((ROOT / "reports/edition-v2/official-guides.json").read_text())
    summary = (ROOT / "reports/edition-v4/AUDIT-SUMMARY.md").read_text()
    assert len(guides) == len(LABELS)
    for guide in guides:
        label = re.escape(LABELS[guide["book"]])
        code = re.escape(guide["code"])
        expected = rf"^\| \*\*{label}\*\* \(`{code}`\) \|"
        assert re.search(expected, summary, re.MULTILINE), (
            f"Incorrect course code for {guide['book']}: expected {guide['code']}"
        )
