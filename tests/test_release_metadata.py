"""The stable edition is dated and every delivered byte has a recorded digest."""
import hashlib
import importlib.util
import json
from datetime import datetime, timezone
from pathlib import Path
import zipfile

import pytest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location(
    "release_metadata", ROOT / "scripts/prepare-release-metadata.py"
)
metadata = importlib.util.module_from_spec(spec)
spec.loader.exec_module(metadata)


def _fixture(tmp_path):
    bundle = tmp_path / "LibrosStudium-bundle-completo.zip"
    inventory = {
        "pdf_count": 1,
        "files": [{"archive": "engineering/manual.pdf", "sha256": "example"}],
        "topics": ["engineering"],
    }
    with zipfile.ZipFile(bundle, "w") as archive:
        archive.writestr("INVENTARIO.json", json.dumps(inventory))
        archive.writestr("engineering/manual.pdf", b"%PDF-test")
    source = tmp_path / "LibrosStudium-fuentes-v1.2.3.tar.gz"
    source.write_bytes(b"example source archive")
    return bundle, source


@pytest.mark.parametrize("invalid", [
    "v1.2.3-rc.1", "v1.2", "v01.2.3", "v1.02.3", "1.2.3",
    "v1.2.3+dirty", "v1.2.3;echo-bad",
])
def test_only_stable_semver_tags_are_publishable(invalid):
    with pytest.raises(ValueError, match="Stable tags"):
        metadata.validate_tag(invalid)


def test_release_date_commit_and_asset_checksums(tmp_path):
    bundle, source = _fixture(tmp_path)
    commit = "a" * 40
    record = metadata.prepare(
        "v1.2.3", commit, bundle, source, tmp_path / "release",
        datetime(2026, 10, 24, 15, 20, tzinfo=timezone.utc),
    )
    assert record["title"] == "Edición 24/10/2026"
    assert record["commit_sha"] == commit
    assert record["pdf_count"] == 1
    assert record["academic_certification"] is False
    notes = (tmp_path / "release/NOTAS-EDICION.md").read_text()
    assert commit in notes and "SHA-256" in notes
    assert hashlib.sha256(bundle.read_bytes()).hexdigest() in notes
    for line in (tmp_path / "release/SHA256SUMS.txt").read_text().splitlines():
        checksum, name = line.split("  ", 1)
        assert hashlib.sha256((tmp_path / "release" / name).read_bytes()).hexdigest() == checksum if name not in {bundle.name,source.name} else hashlib.sha256((tmp_path / name).read_bytes()).hexdigest() == checksum


def test_reject_invalid_sha_or_bundle(tmp_path):
    bundle, source = _fixture(tmp_path)
    with pytest.raises(ValueError, match="40-character"):
        metadata.prepare("v1.2.3", "invalid", bundle, source, tmp_path / "release")
    bundle.write_bytes(b"not a zip")
    with pytest.raises(ValueError, match="valid bundle ZIP"):
        metadata.prepare("v1.2.3", "a" * 40, bundle, source, tmp_path / "release")
