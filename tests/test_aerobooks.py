from __future__ import annotations

import unittest

from framework.aerobooks.cli import (
    citation_keys,
    edition_name,
    label_keys,
    latex_escape,
    ref_keys,
    static_check,
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
