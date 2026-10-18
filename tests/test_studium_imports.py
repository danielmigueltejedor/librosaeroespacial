"""Shared editorial inputs must be explicit and remain inside the repository."""
import importlib.util
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

MODULE = Path(__file__).resolve().parents[1] / "scripts/build-studium-books.py"
SPEC = importlib.util.spec_from_file_location("studium_builder", MODULE)
builder = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(builder)


class StudiumDependencyTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.book = self.root / "books/example"
        (self.book / "latex").mkdir(parents=True)
        self.shared = self.root / "shared/latex/common.tex"
        self.shared.parent.mkdir(parents=True)
        self.shared.write_text("% common rules\n")
        (self.book / "latex/manual.tex").write_text(
            "\\input{../../../shared/latex/common.tex}\n"
        )
        self.config = {
            "workdir": "latex",
            "documents": [{"source": "manual.tex", "output": "manual.pdf"}],
            "shared_resources": ["shared/latex/common.tex"],
        }
        self.patch = patch.object(builder, "ROOT", self.root)
        self.patch.start()
        self.addCleanup(self.patch.stop)

    def test_declared_shared_input_is_portable(self):
        builder.check(self.book, self.config)

    def test_undeclared_shared_input_is_rejected(self):
        self.config["shared_resources"] = []
        with self.assertRaisesRegex(ValueError, "fuera del libro"):
            builder.check(self.book, self.config)

    def test_declared_resource_cannot_escape_shared_latex(self):
        self.config["shared_resources"] = ["shared/latex/../../secret.tex"]
        with self.assertRaisesRegex(ValueError, "fuera de shared/latex"):
            builder.check(self.book, self.config)

    def test_shared_input_cannot_open_an_undeclared_neighbour(self):
        (self.shared.parent / "other.tex").write_text("% not registered\n")
        self.shared.write_text("\\input{../../../shared/latex/other.tex}\n")
        with self.assertRaisesRegex(ValueError, "fuera del libro"):
            builder.check(self.book, self.config)

    def test_shared_resource_cannot_be_a_symlink(self):
        target = self.shared.with_name("target.tex")
        self.shared.rename(target)
        self.shared.symlink_to(target.name)
        with self.assertRaisesRegex(ValueError, "enlazado"):
            builder.check(self.book, self.config)

    def test_missing_workshop_listing_is_rejected(self):
        (self.book / "latex/manual.tex").write_text("\\lstinputlisting{../workshops/w01.wl}\n")
        with self.assertRaisesRegex(ValueError, "Dependencia ausente"):
            builder.check(self.book, self.config)

    def test_listing_cannot_escape_the_book(self):
        (self.book / "latex/manual.tex").write_text("\\lstinputlisting{../../../secret.wl}\n")
        with self.assertRaisesRegex(ValueError, "fuera del libro"):
            builder.check(self.book, self.config)

    def test_existing_workshop_listing_is_portable(self):
        (self.book / "workshops").mkdir()
        (self.book / "workshops/w01.wl").write_text("Print[1 + 1];\n")
        (self.book / "latex/manual.tex").write_text("\\lstinputlisting{../workshops/w01.wl}\n")
        builder.check(self.book, self.config)
