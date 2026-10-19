#!/usr/bin/env python3
"""Download the verified public-domain NASA X-29 image and update Studium covers."""
from __future__ import annotations
import argparse
import hashlib
from io import BytesIO
from pathlib import Path
import subprocess
from urllib.request import Request, urlopen

try:
    from PIL import Image, ImageOps
except ImportError as exc:
    raise SystemExit("Pillow no está instalado: python3 -m pip install Pillow") from exc

ROOT = Path(__file__).resolve().parents[1]
URL = "https://upload.wikimedia.org/wikipedia/commons/a/ac/X-29_in_Banked_Flight.jpg"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--rebuild", action="store_true", help="Recompile all three books with latexmk")
    args = parser.parse_args()
    request = Request(URL, headers={"User-Agent": "Mozilla/5.0 (Studium/educational-book-cover)"})
    try:
        with urlopen(request, timeout=50) as response:
            data = response.read(12 * 1024 * 1024 + 1)
    except Exception as exc:
        raise SystemExit(f"No se ha podido descargar la imagen NASA X-29: {exc}") from exc
    if not 100_000 < len(data) < 12 * 1024 * 1024:
        raise SystemExit("Tamaño inesperado de descarga, no se ha modificado la portada")
    try:
        original = Image.open(BytesIO(data))
        original.verify()
        image = Image.open(BytesIO(data)).convert("RGB")
    except Exception as exc:
        raise SystemExit(f"La descarga no es una imagen válida: {exc}") from exc
    if min(image.size) < 1100:
        raise SystemExit("La imagen tiene una resolución demasiado baja")
    cropped = ImageOps.fit(image, (1800, 1500), method=Image.Resampling.LANCZOS, centering=(0.5, 0.5))
    out = ROOT / "assets" / "cover-hero.jpg"
    tmp = out.with_suffix('.jpg.tmp')
    cropped.save(tmp, format='JPEG', quality=93, optimize=True, progressive=True, subsampling=0)
    tmp.replace(out)
    (ROOT / "assets" / "cover-credit.tex").write_text(
        "\\noindent\\textbf{Imagen de portada.} Fotografía NASA,\n"
        "X-29 número 1 en viraje sobre el desierto de Mojave,\n"
        "24 de julio de 1987, ID EC87-0182-14. Fuente: "
        "\\href{https://commons.wikimedia.org/wiki/File:X-29_in_Banked_Flight.jpg}{Wikimedia Commons}.\n"
        "Dominio público en Estados Unidos (autoría NASA); reutilización educativa conforme a "
        "\\href{https://www.nasa.gov/nasa-brand-center/images-and-media/}{las condiciones NASA}. "
        "Recorte proporcional y remuestreo a 1800 por 1500 píxeles; sin alteración del contenido. "
        "Consulta: 19 de octubre de 2026. No implica respaldo institucional.\n",
        encoding="utf-8",
    )
    import json
    (ROOT / "assets" / "cover-photo.json").write_text(json.dumps(dict(
        author="NASA", title="X-29 in Banked Flight", photo_id="EC87-0182-14",
        image_date="1987-07-24", consulted_on="2026-10-19",
        source="https://commons.wikimedia.org/wiki/File:X-29_in_Banked_Flight.jpg",
        original_url=URL, license="PD-USGov-NASA (United States); educational reuse under NASA media guidelines",
        license_url="https://www.nasa.gov/nasa-brand-center/images-and-media/",
        attribution="NASA; no institutional endorsement",
        modifications="Proportional central crop and Lanczos resampling to 1800x1500; JPEG encoding; no generative edits",
        original_dimensions=list(image.size), original_sha256=hashlib.sha256(data).hexdigest(),
        output_sha256=hashlib.sha256(out.read_bytes()).hexdigest(), output="assets/cover-hero.jpg"
    ), ensure_ascii=False, indent=2)+"\n", encoding="utf-8")
    print(f"Imagen X-29 aplicada: {out}; SHA256 original: {hashlib.sha256(data).hexdigest()}")
    if args.rebuild:
        for tex in ("main.tex", "problemas.tex", "simulacros.tex"):
            subprocess.run(
                ["latexmk", "-pdf", "-interaction=nonstopmode", "-halt-on-error", tex],
                cwd=ROOT,
                check=True,
            )
        print("Tres portadas X-29 compiladas correctamente.")


if __name__ == "__main__":
    main()
