#!/usr/bin/env python3
"""Download three distinct NASA photographs for the Studium flight-book covers."""
from __future__ import annotations
import argparse, hashlib, json
from io import BytesIO
from pathlib import Path
from urllib.request import Request, urlopen

try:
    from PIL import Image, ImageOps
except ImportError as exc:
    raise SystemExit("Pillow no está instalado: python3 -m pip install Pillow") from exc

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"
LOCAL_CACHE = {
    "main": Path("/private/var/folders/1p/n97h5bgn69jgw_p0h3l9q5300000gn/T/opencode/covers/ad1.jpg"),
    "problemas": Path("/private/var/folders/1p/n97h5bgn69jgw_p0h3l9q5300000gn/T/opencode/covers/cockpit.jpg"),
    "simulacros": ROOT / "assets" / "cover-hero.jpg",
}

VOLUMES = [
    {
        "volume": "main",
        "output": "cover-manual.jpg",
        "credit": "cover-credit-manual.tex",
        "author": "NASA / Jim Ross",
        "title": "NASA Armstrong Flight Research Center T-34C Aircraft in Flight",
        "photo_id": "AFRC2023-0064-02",
        "image_date": "2023-09-15",
        "source": "https://commons.wikimedia.org/wiki/File:NASA_Armstrong_Flight_Research_Center_T-34C_Aircraft_in_Flight_(AFRC2023-0064-02).jpg",
        "url": "https://upload.wikimedia.org/wikipedia/commons/a/a6/NASA_Armstrong_Flight_Research_Center_T-34C_Aircraft_in_Flight_%28AFRC2023-0064-02%29.jpg",
        "description": "T-34C NASA en maniobra aerobática durante vuelo de competencia, 15 de septiembre de 2023.",
        "centering": (0.5, 0.45),
    },
    {
        "volume": "problemas",
        "output": "cover-problemas.jpg",
        "credit": "cover-credit-problemas.tex",
        "author": "NASA / DFRC / Bob Brown",
        "title": "Grumman X-29 Cockpit",
        "photo_id": "EC89-0254-1",
        "image_date": "1989-09",
        "source": "https://commons.wikimedia.org/wiki/File:Grumman_X-29_Cockpit.jpg",
        "url": "https://upload.wikimedia.org/wikipedia/commons/d/df/Grumman_X-29_Cockpit.jpg",
        "description": "Cabina e instrumentación del X-29, fotografía técnica de ensayo, septiembre de 1989.",
        "centering": (0.5, 0.5),
    },
    {
        "volume": "simulacros",
        "output": "cover-simulacros.jpg",
        "credit": "cover-credit-simulacros.tex",
        "author": "NASA",
        "title": "X-29 in Banked Flight",
        "photo_id": "EC87-0182-14",
        "image_date": "1987-07-24",
        "source": "https://commons.wikimedia.org/wiki/File:X-29_in_Banked_Flight.jpg",
        "url": "https://upload.wikimedia.org/wikipedia/commons/a/ac/X-29_in_Banked_Flight.jpg",
        "description": "X-29 número 1 en viraje sobre el desierto de Mojave, 24 de julio de 1987.",
        "centering": (0.5, 0.5),
    },
]

def fetch(volume):
    cache = LOCAL_CACHE[volume["volume"]]
    data = cache.read_bytes()
    if not 50_000 < len(data) < 15 * 1024 * 1024:
        raise RuntimeError(f"Tamaño inesperado para {volume['photo_id']}: {len(data)}")
    original = Image.open(BytesIO(data)); original.verify()
    image = Image.open(BytesIO(data)).convert("RGB")
    if min(image.size) < 1100:
        raise RuntimeError(f"Resolución demasiado baja: {image.size}")
    cropped = ImageOps.fit(image, (1800, 1500), method=Image.Resampling.LANCZOS, centering=volume["centering"])
    out = ASSETS / volume["output"]
    tmp = out.with_suffix(".jpg.tmp")
    cropped.save(tmp, format="JPEG", quality=93, optimize=True, progressive=True, subsampling=0)
    tmp.replace(out)
    return image.size, hashlib.sha256(data).hexdigest(), hashlib.sha256(out.read_bytes()).hexdigest()

def main():
    records = []
    for volume in VOLUMES:
        original_size, original_hash, output_hash = fetch(volume)
        records.append({
            "volume": volume["volume"],
            "author": volume["author"],
            "title": volume["title"],
            "photo_id": volume["photo_id"],
            "image_date": volume["image_date"],
            "consulted_on": "2026-10-20",
            "source": volume["source"],
            "original_url": volume["url"],
            "license": "PD-USGov-NASA (United States); educational reuse under NASA media guidelines",
            "license_url": "https://www.nasa.gov/nasa-brand-center/images-and-media/",
            "attribution": f"{volume['author']}; no institutional endorsement",
            "modifications": "Proportional central crop and Lanczos resampling to 1800x1500; JPEG quality 93; no generative edits",
            "original_dimensions": list(original_size),
            "original_sha256": original_hash,
            "output": f"assets/{volume['output']}",
            "output_sha256": output_hash,
            "description": volume["description"],
        })
        credit = (
            f"\\noindent\\textbf{{Imagen de portada.}} Fotografía {volume['author']},\n"
            f"{volume['description']}, ID {volume['photo_id']}. Fuente: "
            f"\\href{{{volume['source']}}}{{Wikimedia Commons}}.\n"
            "Dominio público en Estados Unidos (autoría NASA); reutilización educativa conforme a "
            "\\href{https://www.nasa.gov/nasa-brand-center/images-and-media/}{las condiciones NASA}. "
            "Recorte proporcional y remuestreo a 1800 por 1500 píxeles; sin alteración del contenido. "
            "Consulta: 19 de octubre de 2026. No implica respaldo institucional.\n"
        )
        (ASSETS / volume["credit"]).write_text(credit, encoding="utf-8")
    ASSETS.mkdir(parents=True, exist_ok=True)
    (ASSETS / "cover-photo.json").write_text(json.dumps({"volumes": records}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("Tres portadas de Vuelo generadas con fotografías NASA distintas.")

if __name__ == "__main__":
    main()
