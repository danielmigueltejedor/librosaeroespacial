"""Cover provenance should remain consistent and reproducible on clean machines."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FLIGHT = ROOT / "books/mecanica-vuelo"


def test_cover_manifest_matches_editorial_description():
    metadata = json.loads((FLIGHT / "assets/cover-photo.json").read_text())
    photos = {p["volume"]: p for p in metadata["volumes"]}
    assert set(photos) == {"main", "problemas", "simulacros"}
    assert photos["main"]["photo_id"] == "EC81-15846"
    assert "AD-1" in photos["main"]["title"]
    for photo in photos.values():
        assert len(photo["original_sha256"]) == 64
        assert len(photo["output_sha256"]) == 64
        assert photo["original_url"].startswith("https://")
        assert (FLIGHT / photo["output"]).is_file()
    assert "AD-1" in (FLIGHT / "README.md").read_text()
    assert "AD-1" in (ROOT / "books/README.md").read_text()


def test_cover_regenerator_has_no_author_specific_absolute_cache():
    script = (FLIGHT / "scripts/obtain_cover_photos.py").read_text()
    assert "LOCAL_CACHE" not in script
    assert "/private/var/folders" not in script
    assert "/Users/" not in script
    assert 'photo["original_sha256"]' in script
    assert 'photo["original_url"]' in script
