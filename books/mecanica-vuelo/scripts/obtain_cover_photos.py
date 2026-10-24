#!/usr/bin/env python3
"""Reproduce the three NASA covers from credited, checksum-pinned originals."""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
from io import BytesIO
import json
from pathlib import Path
from urllib.request import Request, urlopen

try:
    from PIL import Image, ImageOps
except ImportError as exc:
    raise SystemExit("Instala Pillow: python3 -m pip install Pillow") from exc

ASSETS = Path(__file__).resolve().parents[1] / "assets"
MANIFEST = ASSETS / "cover-photo.json"


def original_bytes(photo: dict, source_dir: Path | None) -> bytes:
    if source_dir is not None:
        data = (source_dir / (photo["photo_id"] + ".jpg")).read_bytes()
    else:
        request = Request(photo["original_url"], headers={
            "User-Agent": "LibrosStudium-cover-reproducer/1.0 (educational edition)"
        })
        with urlopen(request, timeout=40) as response:
            data = response.read(16 * 1024 * 1024 + 1)
    if not 50_000 < len(data) <= 16 * 1024 * 1024:
        raise ValueError(f"Unexpected source size: {photo['photo_id']}")
    actual = hashlib.sha256(data).hexdigest()
    if actual != photo["original_sha256"]:
        raise ValueError(
            f"Source checksum changed for {photo['photo_id']}: {actual}. "
            "Check the NASA source and update provenance through a reviewed change."
        )
    return data


def create_cover(photo: dict, data: bytes) -> bytes:
    with Image.open(BytesIO(data)) as image:
        image.verify()
    with Image.open(BytesIO(data)) as image:
        if list(image.size) != photo["original_dimensions"]:
            raise ValueError(f"Source dimensions changed: {photo['photo_id']}")
        image = image.convert("RGB")
        image = ImageOps.fit(
            image, (1800, 1500), method=Image.Resampling.LANCZOS,
            centering=(0.5, 0.5),
        )
        out = BytesIO()
        image.save(out, format="JPEG", quality=93, optimize=True,
                   progressive=True, subsampling=0)
        return out.getvalue()


def cover_credit(photo: dict) -> str:
    lines = [
        rf"\noindent\textbf{{Imagen de portada.}} Fotografía {photo['author']},",
        f"{photo['description']}, ID {photo['photo_id']}. Fuente: "
        + rf"\href{{{photo['source']}}}{{Wikimedia Commons}}.",
        "Dominio público en Estados Unidos (autoría NASA); reutilización educativa conforme a "
        + r"\href{https://www.nasa.gov/nasa-brand-center/images-and-media/}{las condiciones NASA}. "
        + "Recorte proporcional y remuestreo a 1800 por 1500 píxeles; "
        + "sin alteración generativa del contenido. "
        + f"Consulta: {photo['consulted_on']}. No implica respaldo institucional.",
    ]
    return "\n".join(lines) + "\n"


def regenerate(source_dir: Path | None = None) -> None:
    record = json.loads(MANIFEST.read_text(encoding="utf-8"))
    volumes = record["volumes"]
    if {v["volume"] for v in volumes} != {"main", "problemas", "simulacros"}:
        raise ValueError("Expected three distinct, documented cover photographs")

    # Validate every original before modifying ANY published asset.
    generated = []
    for photo in volumes:
        source = original_bytes(photo, source_dir)
        cover = create_cover(photo, source)
        updated = dict(photo)
        updated["output_sha256"] = hashlib.sha256(cover).hexdigest()
        updated["consulted_on"] = datetime.now(timezone.utc).date().isoformat()
        # Manifest destinations are relative to the book root: assets/cover-*.jpg.
        destination = ASSETS.parent / updated["output"]
        if destination.parent != ASSETS or destination.suffix.lower() != ".jpg":
            raise ValueError("Unsafe cover output path")
        generated.append((updated, destination, cover))

    for photo, destination, cover in generated:
        destination.write_bytes(cover)
        credit_path = ASSETS / ("cover-credit-" + (
            "manual" if photo["volume"] == "main" else photo["volume"]
        ) + ".tex")
        credit_path.write_text(cover_credit(photo), encoding="utf-8")
    record["volumes"] = [photo for photo, _, _ in generated]
    MANIFEST.write_text(json.dumps(record, ensure_ascii=False, indent=2) + "\n",
                        encoding="utf-8")
    print("Tres portadas reproducidas con originales NASA y SHA-256 verificados.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--source-dir", type=Path,
        help="Offline directory with PHOTO_ID.jpg originals, verified by SHA-256"
    )
    regenerate(parser.parse_args().source_dir)
