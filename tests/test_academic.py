from __future__ import annotations

import unittest

from framework.aerobooks.academic import (
    ACADEMIC_TOOL_VERSION,
    REVIEW_PROMPTS,
    _coverage,
    _evidence_entries,
    _claim_map,
)
from framework.aerobooks.cli import book_dir, framework_dir


class AeroBooksAcademicTests(unittest.TestCase):
    def test_academic_tool_has_version(self) -> None:
        self.assertRegex(ACADEMIC_TOOL_VERSION, r"^\d+\.\d+\.\d+$")

    def test_all_review_prompts_exist(self) -> None:
        prompts = framework_dir() / "prompts"
        missing = [
            filename
            for filename in REVIEW_PROMPTS.values()
            if not (prompts / filename).exists()
        ]
        self.assertEqual(missing, [])

    def test_structures_coverage_has_no_issues(self) -> None:
        root = book_dir("estructuras-aeroespaciales")
        report = _coverage(root)
        self.assertEqual(
            report["issues"],
            [],
            msg="; ".join(
                f"{item['code']}: {item['message']}"
                for item in report["issues"]
            ),
        )

    def test_high_risk_claims_have_verified_evidence(self) -> None:
        root = book_dir("estructuras-aeroespaciales")
        claims = _claim_map(root)
        evidence = _evidence_entries(root)
        by_claim = {}
        for item in evidence:
            if item.get("claim"):
                by_claim.setdefault(item["claim"], []).append(item)

        missing = []
        for cid, claim in claims.items():
            if (
                claim.get("risk") == "high"
                and claim.get("status") in {"verified", "derived"}
                and not any(
                    ev.get("status") == "verified"
                    for ev in by_claim.get(cid, [])
                )
            ):
                missing.append(cid)

        self.assertEqual(missing, [])


if __name__ == "__main__":
    unittest.main()
