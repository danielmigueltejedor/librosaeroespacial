from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from framework.aerobooks.cli import (
    citation_keys,
    edition_name,
    label_keys,
    latex_escape,
    ref_keys,
    static_check,
    inspect_latex_log,
)


class AeroBooksUnitTests(unittest.TestCase):
    def test_edition_names(self) -> None:
        self.assertEqual(edition_name(1), "Primera edición")
        self.assertEqual(edition_name(3), "Tercera edición")
        self.assertEqual(edition_name(10), "Décima edición")

    def test_latex_escape(self) -> None:
        self.assertEqual(
            latex_escape("A&B_100%"),
            r"A\&B\_100\%",
        )

    def test_citation_parser(self) -> None:
        tex = r"""
        Texto \autocite{alpha,beta}.
        Otro \textcite{gamma}.
        """
        self.assertEqual(citation_keys(tex), {"alpha", "beta", "gamma"})

    def test_label_reference_parser(self) -> None:
        tex = r"""
        \label{fig:a}
        Véase \cref{fig:a} y \eqref{eq:b}.
        \label{eq:b}
        """
        self.assertEqual(set(label_keys(tex)), {"fig:a", "eq:b"})
        self.assertEqual(ref_keys(tex), {"fig:a", "eq:b"})

    def test_latex_log_inspection(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "main.log"
            path.write_text(
                "Overfull \\hbox (2.0pt too wide)\n"
                "LaTeX Warning: There were undefined references.\n",
                encoding="utf-8",
            )
            findings = inspect_latex_log(path)
            codes = {f.code for f in findings}
            self.assertIn("PDF002", codes)
            self.assertIn("PDF004", codes)

    def test_structures_book_passes_strict_static_gate(self) -> None:
        report = static_check("estructuras-aeroespaciales", strict=True)
        self.assertEqual(
            report.errors,
            [],
            msg="Errores: " + "; ".join(f"{f.code}: {f.message}" for f in report.errors),
        )
        self.assertEqual(
            report.warnings,
            [],
            msg="Avisos: " + "; ".join(f"{f.code}: {f.message}" for f in report.warnings),
        )


if __name__ == "__main__":
    unittest.main()
