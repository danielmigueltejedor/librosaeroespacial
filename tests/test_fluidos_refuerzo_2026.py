"""Verifica en CI los cálculos y anclajes del refuerzo bibliográfico de Fluidos."""

from __future__ import annotations

import subprocess
import sys
import unittest
from pathlib import Path


class FluidBibliography2026Checks(unittest.TestCase):
    def test_source_review_derivations_and_integration(self):
        repo = Path(__file__).resolve().parents[1]
        script = repo / "books/mecanica-fluidos/scripts/check_refuerzo_2026.py"
        result = subprocess.run(
            [sys.executable, str(script)],
            cwd=repo,
            capture_output=True,
            text=True,
            timeout=30,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual(result.stdout.count("OK test_"), 5)


if __name__ == "__main__":
    unittest.main()
