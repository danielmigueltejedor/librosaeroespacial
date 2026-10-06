from __future__ import annotations

import json
import tempfile
import tomllib
import unittest
from pathlib import Path

from framework.aerobooks.academic import ACADEMIC_TOOL_VERSION, _coverage
from framework.aerobooks.cli import FRAMEWORK_VERSION, book_dir, load_book, static_check
from framework.aerobooks.research import (
    assess_authority,
    authoring_block_reason,
    claim_corroboration_issues,
    contract_version,
    create_course,
    derivation_issues,
    doi_shape_ok,
    exercise_issues,
    figure_issues,
    isbn_checksum_ok,
    numeric_reproducible,
    resolve_book_config,
    source_policy_issues,
    v03_coverage_issues,
    v03_next_messages,
    validate_global_config,
    write_pack,
)


def _write_json(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def _append(path: Path, item: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(item, ensure_ascii=False) + "\n")


def _source(sid: str, **extra) -> dict:
    item = {
        "id": sid,
        "title": sid,
        "kind": "textbook",
        "tier": "A",
        "tier_detail": "A3",
        "role": ["theory"],
        "status": "verified",
        "lifecycle": "accepted",
        "content_access": "full",
        "consulted": True,
        "rights": "Cita breve.",
        "discovery_log": "LOG-1",
        "metadata_origin": "verified",
        "publisher": "Academic Press",
        "published": "2020",
    }
    item.update(extra)
    return item


def _verify_discovery(root: Path) -> None:
    path = root / "sources" / "discovery.json"
    record = json.loads(path.read_text(encoding="utf-8"))
    record["status"] = "verified"
    record["guide_url"] = "https://www.unileon.es/guia-docente/mecanica-de-fluidos"
    record["identity"]["degree"] = "Grado en Ingeniería Aeroespacial"
    record["identity"]["academic_year"] = "2026-2027"
    record["identity"]["code"] = "0710311"
    record["verification"]["name_match_sufficient"] = False
    record["verification"]["academic_year_checked"] = True
    record["verification"]["programme_checked"] = True
    _write_json(path, record)


def _log(root: Path) -> None:
    _append(root / "sources" / "research-log.jsonl", {
        "id": "LOG-1",
        "query": "guía docente Mecánica de Fluidos Universidad de León 2026",
        "date": "2026-10-07",
        "agent": "test",
        "candidates": ["SRC-A", "SRC-B"],
        "accepted": ["SRC-A", "SRC-B"],
        "rejected": [],
        "reason": "Identidad de curso comprobada y obras abiertas consultadas.",
    })


class AeroBooksV03Tests(unittest.TestCase):
    def test_versions(self) -> None:
        self.assertEqual(FRAMEWORK_VERSION, "0.3.0")
        self.assertEqual(ACADEMIC_TOOL_VERSION, "0.3.0")

    def test_global_config_and_book_override(self) -> None:
        issues = validate_global_config({"author": {"name": ""}})
        self.assertTrue(issues)
        merged = resolve_book_config(
            {"author": {"name": "Autora del libro"}, "book": {"title": "Local"}},
            {
                "author": {"name": "Global"},
                "institution": {"name": "Universidad de León"},
                "editorial": {"units": "SI"},
            },
        )
        self.assertEqual(merged["author"]["name"], "Autora del libro")
        self.assertEqual(merged["institution"]["name"], "Universidad de León")
        self.assertEqual(merged["editorial"]["units"], "SI")
        self.assertEqual(merged["book"]["title"], "Local")

        _root, config = load_book("mecanica-fluidos")
        self.assertEqual(config["book"]["title"], "Mecánica de Fluidos")
        self.assertEqual(config["author"]["name"], "Daniel Miguel Tejedor")
        self.assertEqual(config["editorial"]["units"], "SI")
        self.assertNotEqual(config.get("academic", {}).get("contract"), "0.3")

    def test_existing_books_stay_on_v02(self) -> None:
        for slug in ("mecanica-fluidos", "estructuras-aeroespaciales"):
            root = book_dir(slug)
            self.assertEqual(contract_version(root), "0.2")
            report = _coverage(root)
            self.assertEqual(
                [item for item in report["issues"] if item["code"].startswith("V03")],
                [],
            )
        structures = static_check("estructuras-aeroespaciales", strict=True)
        self.assertTrue(structures.ok(strict=True), msg=str(structures.findings))

    def test_new_course_without_local_sources(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = create_course(
                slug="fluidos",
                course="Mecánica de Fluidos",
                institution="Universidad de León",
                dest=Path(tmp) / "fluidos",
            )
            manifest = json.loads((root / "sources" / "manifest.json").read_text(encoding="utf-8"))
            self.assertEqual(manifest["sources"], [])
            discovery = json.loads((root / "sources" / "discovery.json").read_text(encoding="utf-8"))
            self.assertEqual(discovery["status"], "required")
            self.assertFalse(discovery["verification"]["name_match_sufficient"])
            with (root / "course.toml").open("rb") as fh:
                course = tomllib.load(fh)
            self.assertEqual(course["mode"], "source-discovery")
            self.assertEqual(course["sources"], "")
            messages = v03_next_messages(root, "fluidos")
            self.assertIn("COURSE DISCOVERY REQUIRED", messages)
            codes = {item["code"] for item in v03_coverage_issues(root)}
            self.assertEqual(codes, {"V03DIS"})

    def test_new_course_with_local_sources_does_not_accept_them(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            library = base / "moodle"
            library.mkdir()
            (library / "examen.md").write_text("enunciado local\n", encoding="utf-8")
            root = create_course(
                slug="fluidos",
                course="Mecánica de Fluidos",
                institution="Universidad de León",
                dest=base / "fluidos",
                degree="Grado en Ingeniería Aeroespacial",
                academic_year="2026-2027",
                sources=library,
            )
            intake = json.loads((root / "build" / "SOURCE_INTAKE.json").read_text(encoding="utf-8"))
            self.assertEqual(len(intake["files"]), 1)
            self.assertEqual(intake["files"][0]["lifecycle"], "candidate")
            self.assertEqual(intake["files"][0]["content_access"], "metadata-only")
            self.assertFalse((root / "sources" / "examen.md").exists())
            log = (root / "sources" / "research-log.jsonl").read_text(encoding="utf-8")
            self.assertIn("examen.md", log)
            self.assertIn("COURSE DISCOVERY REQUIRED", v03_next_messages(root, "fluidos"))

    def test_authority_profile_is_not_a_verdict(self) -> None:
        profile = assess_authority(_source("SRC-A", tier_detail="A2", peer_reviewed=True))
        self.assertIsNone(profile["corroboration"])
        self.assertIn("reasons", profile)
        self.assertNotIn("verdict", profile)
        self.assertGreaterEqual(profile["authority"], 0)
        preprint = assess_authority(_source(
            "SRC-P", tier="C", tier_detail="C0", kind="preprint", peer_reviewed=False,
        ))
        self.assertEqual(preprint["editorial_process"], 0)
        self.assertIn("Preprint", preprint["reasons"]["editorial_process"])

    def test_corroboration_false_independence_and_d_sources(self) -> None:
        shared = [
            _source("SRC-1", origin_id="WHITE"),
            _source("SRC-2", origin_id="WHITE", tier="B", tier_detail="B0"),
        ]
        claim = {
            "id": "CLM-1",
            "type": "scientific",
            "risk": "high",
            "status": "verified",
            "sources": ["SRC-1", "SRC-2"],
        }
        messages = " ".join(
            item["message"] for item in claim_corroboration_issues(claim, {s["id"]: s for s in shared})
        )
        self.assertIn("no son independientes", messages)

        independent = [
            _source("SRC-1"),
            _source("SRC-2", tier="B", tier_detail="B0", kind="notes"),
        ]
        self.assertEqual(
            claim_corroboration_issues(claim, {s["id"]: s for s in independent}),
            [],
        )

        notes = [
            _source("D1", tier="D", tier_detail="D2"),
            _source("D2", tier="D", tier_detail="D1"),
        ]
        d_claim = dict(claim, sources=["D1", "D2"])
        d_messages = " ".join(
            item["message"] for item in claim_corroboration_issues(d_claim, {s["id"]: s for s in notes})
        )
        self.assertIn("solo en fuentes D/E", d_messages)

        derived = {
            "id": "CLM-M",
            "type": "mathematical",
            "risk": "high",
            "status": "derived",
            "sources": [],
            "derivation": "De div v = 0 se sigue la forma integral por el teorema de Gauss.",
        }
        self.assertEqual(claim_corroboration_issues(derived, {}), [])

        canonical = {
            "id": "CLM-C",
            "type": "scientific",
            "risk": "high",
            "status": "derived",
            "sources": ["SRC-1"],
            "derivation": "Proyección de Euler estacionario a lo largo de una línea de corriente.",
        }
        self.assertEqual(
            claim_corroboration_issues(canonical, {"SRC-1": _source("SRC-1", tier_detail="A0")}),
            [],
        )

    def test_source_gates_for_access_identifiers_and_preprints(self) -> None:
        self.assertTrue(isbn_checksum_ok("978-0-306-40615-7"))
        self.assertFalse(isbn_checksum_ok("978-0-306-40615-8"))
        self.assertTrue(doi_shape_ok("10.1017/9781009026307"))
        self.assertFalse(doi_shape_ok("doi-pendiente"))

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "course.toml").write_text("schema_version = 1\n", encoding="utf-8")
            _write_json(root / "sources" / "manifest.json", {"sources": [
                _source("SRC-BAD", metadata_origin="invented", isbn="978-0-306-40615-8"),
                _source(
                    "SRC-PRE",
                    tier="C",
                    tier_detail="C0",
                    kind="preprint",
                    peer_reviewed=True,
                    peer_review_status="preprint",
                ),
                _source("SRC-SNIP", content_access="snippet", consulted=False, lifecycle="candidate"),
            ]})
            _append(root / "evidence" / "map.jsonl", {
                "id": "EV-1",
                "source": "SRC-SNIP",
                "support": "direct",
                "status": "verified",
            })
            codes = {item["code"] for item in source_policy_issues(root)}
            text = " ".join(item["message"] for item in source_policy_issues(root))
            self.assertIn("V03SRC", codes)
            self.assertIn("inventados", text)
            self.assertIn("ISBN", text)
            self.assertIn("preprint", text)
            self.assertIn("sin acceso al contenido", text)

    def test_coverage_gap_blocks_authoring(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = create_course(
                slug="fluidos",
                course="Mecánica de Fluidos",
                institution="Universidad de León",
                dest=Path(tmp) / "fluidos",
            )
            _verify_discovery(root)
            _log(root)
            _write_json(root / "sources" / "manifest.json", {"sources": [
                _source("SRC-A"),
                _source("SRC-B", tier="B", tier_detail="B1"),
            ]})
            _write_json(root / "sources" / "coverage.json", {"schema_version": 1, "topics": [{
                "id": "T-NS",
                "title": "Navier-Stokes",
                "chapter": "CH-NS",
                "fundamental": True,
                "sources": ["SRC-A"],
                "claims": [],
                "derivations": [],
                "figures": [],
                "exercises": [],
                "status": "GAP",
            }]})
            _write_json(root / "specs" / "CH-NS.json", {
                "id": "CH-NS",
                "title": "Navier-Stokes",
                "status": "planned",
                "path": "chapters/ns.tex",
            })
            self.assertTrue(any(item["code"] == "V03GAP" for item in v03_coverage_issues(root)))
            self.assertIn(
                "CHAPTER BLOCKED",
                authoring_block_reason(root, {"id": "CH-NS", "status": "planned"}, "author") or "",
            )
            self.assertIn("COVERAGE GAP", v03_next_messages(root, "fluidos"))

    def test_derivation_and_exercise_and_figure_gates(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            _append(root / "derivations" / "ledger.jsonl", {
                "id": "DRV-1",
                "fundamental": True,
                "status": "pending",
                "dimensional_status": "fail",
                "starting_assumptions": ["fluido incompresible"],
                "starting_equations": ["div v = 0"],
                "steps": ["integrar"],
                "result": "Q = integral",
                "sources": [],
                "dimensional_analysis": "m^3/s",
                "conditions": ["régimen permanente"],
                "limit_cases": ["v = 0"],
                "reviewer": "",
            })
            drv = " ".join(item["message"] for item in derivation_issues(root))
            self.assertIn("no auditada", drv)
            self.assertIn("error dimensional", drv)

            _append(root / "exercises" / "ledger.jsonl", {
                "id": "EX-1",
                "statement": "Calcula el caudal.",
                "origin": "copied-exam",
                "data": {"R": "1 cm"},
                "unknowns": ["Q"],
                "hypotheses": ["laminar"],
                "solution": "Poiseuille",
                "result": "1.0",
                "units": "m^3/s",
                "numerical_tolerance": 1e-6,
                "checks": [{"expected": 1.0, "actual": 2.0, "tolerance": 1e-6}],
                "reviewer": "revisor",
                "status": "published",
                "reviews": {},
                "computational": {"applicable": True},
            })
            ex = " ".join(item["message"] for item in exercise_issues(root))
            self.assertIn("original", ex)
            self.assertIn("fuera de tolerancia", ex)
            self.assertIn("verificación computacional", ex)
            self.assertFalse(numeric_reproducible(1.0, 2.0, 1e-6))
            self.assertTrue(numeric_reproducible(1.0, 1.0000001, 1e-6))

            _write_json(root / "specs" / "CH.json", {
                "id": "CH",
                "status": "ready",
                "figures": ["FIG-1"],
            })
            _append(root / "figures" / "ledger.jsonl", {
                "id": "FIG-1",
                "status": "fail",
                "checks": {"direction": "fail"},
            })
            fig = " ".join(item["message"] for item in figure_issues(root))
            self.assertIn("físicamente errónea", fig)
            self.assertIn("direction", fig)

    def test_research_pack_is_small(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = create_course(
                slug="fluidos",
                course="Mecánica de Fluidos",
                institution="Universidad de León",
                dest=Path(tmp) / "fluidos",
            )
            pack = write_pack(root, "course-discovery", "fluidos")
            text = pack.read_text(encoding="utf-8")
            self.assertIn("COURSE DISCOVERY", text.upper())
            self.assertNotIn("\\chapter", text)
            self.assertTrue(pack.name.endswith("COURSE_DISCOVERY_PACK.md"))

    def test_supported_topic_moves_to_blueprint(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = create_course(
                slug="fluidos",
                course="Mecánica de Fluidos",
                institution="Universidad de León",
                dest=Path(tmp) / "fluidos",
            )
            _verify_discovery(root)
            _log(root)
            _write_json(root / "sources" / "manifest.json", {"sources": [_source("SRC-A")]})
            _write_json(root / "sources" / "coverage.json", {"schema_version": 1, "topics": [{
                "id": "T-1",
                "title": "Continuo",
                "fundamental": True,
                "sources": ["SRC-A"],
                "claims": [],
                "derivations": [],
                "figures": [],
                "exercises": [],
                "status": "SUPPORTED",
            }]})
            self.assertEqual(v03_coverage_issues(root), [])
            self.assertIn("BLUEPRINT REQUIRED", v03_next_messages(root, "fluidos"))


if __name__ == "__main__":
    unittest.main()
