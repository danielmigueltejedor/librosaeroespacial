#!/usr/bin/env python3
"""Download the licensed cover photographs once; compilation never needs the network.

    python humanidades-y-ciencias/tools/fetch_covers.py [slug ...]

Each project keeps cover/cover.jpg (derived from the Commons file) and
cover/cover.json (title, subtitle, credit, licence, source page and hashes).
"""
from __future__ import annotations

import hashlib
import io
import json
import subprocess
import sys
import time
import urllib.parse
from pathlib import Path

from PIL import Image

HERE = Path(__file__).resolve().parent.parent
API = 'https://commons.wikimedia.org/w/api.php'
UA = 'studium-research/1.0 (contact: danielmigueltejedor@icloud.com)'

COVERS = {
    'literatura-espanola': {
        'short_title': 'Literatura española',
        'file': 'Monumento a Cervantes (Madrid) 10n.jpg',
        'title': 'LITERATURA\\\\ESPAÑOLA',
        'subtitle': 'De la Edad Media al Siglo de Oro: textos, géneros y contextos',
        'category': 'MANUAL UNIVERSITARIO',
        'discipline': 'HUMANIDADES · FILOLOGÍA HISPÁNICA',
        'description': 'Don Quijote y Sancho Panza, bronces de Lorenzo Coullaut Valera (1925-1930), monumento a Cervantes, Madrid.',
    },
    'historia-moderna-espana': {
        'short_title': 'Historia moderna de España',
        'file': 'Velázquez - de Breda o Las Lanzas (Museo del Prado, 1634-35)FXD.jpg',
        'title': 'HISTORIA MODERNA\\\\DE ESPAÑA',
        'subtitle': 'De los Reyes Católicos a los Borbones: política, sociedad y fuentes',
        'category': 'MANUAL UNIVERSITARIO',
        'discipline': 'HUMANIDADES · HISTORIA',
        'description': 'Diego Velázquez, La rendición de Breda (Las Lanzas), 1634-1635, Museo del Prado.',
    },
    'biologia-celular-molecular': {
        'short_title': 'Biología celular y molecular',
        'file': 'Bovine Pulmonary Artery Endothelial Cells Fluorescent Image.jpg',
        'title': 'BIOLOGÍA CELULAR\\\\Y MOLECULAR',
        'subtitle': 'Estructura celular, biomoléculas, genes y señalización',
        'category': 'MANUAL UNIVERSITARIO',
        'discipline': 'CIENCIAS DE LA VIDA · BIOLOGÍA',
        'description': 'Células endoteliales de arteria pulmonar bovina: núcleos (azul), mitocondrias (rojo) y filamentos de actina (verde).',
    },
}


def get(url: str, binary: bool = False, tries: int = 6) -> bytes:
    for k in range(tries):
        out = subprocess.run(['curl', '-sL', '--max-time', '90', '-A', UA, url], capture_output=True, check=False).stdout
        if (out[:2] == b'\xff\xd8') if binary else out.startswith(b'{'):
            return out
        time.sleep(5 + 8 * k)
    raise RuntimeError('download failed: ' + url)


def fetch(slug: str) -> dict:
    spec = COVERS[slug]
    query = {'action': 'query', 'titles': 'File:' + spec['file'], 'prop': 'imageinfo', 'format': 'json',
             'iiprop': 'url|extmetadata|size', 'iiurlwidth': '2000'}
    page = next(iter(json.loads(get(API + '?' + urllib.parse.urlencode(query)))['query']['pages'].values()))
    ii = page['imageinfo'][0]
    meta = ii['extmetadata']
    import re
    clean = lambda k: re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', '', meta.get(k, {}).get('value', ''))).strip()
    licence = clean('LicenseShortName')
    if licence not in ('Public domain', 'CC0', 'CC BY 2.0', 'CC BY 4.0', 'CC BY-SA 3.0', 'CC BY-SA 4.0', 'CC BY-SA 2.0'):
        raise ValueError(f'{slug}: licence not allowed: {licence}')
    data = get(ii['thumburl'], binary=True)
    image = Image.open(io.BytesIO(data)).convert('RGB')
    buf = io.BytesIO()
    image.save(buf, 'JPEG', quality=88, optimize=True, progressive=True)
    folder = HERE / slug / 'cover'
    folder.mkdir(parents=True, exist_ok=True)
    (folder / 'cover.jpg').write_bytes(buf.getvalue())
    record = {
        'file': 'cover.jpg',
        'dimensions_px': list(image.size),
        'sha256': hashlib.sha256(buf.getvalue()).hexdigest(),
        'commons_title': 'File:' + spec['file'],
        'source_page': ii['descriptionurl'],
        'original_dimensions_px': [ii['width'], ii['height']],
        'author': clean('Artist') or 'Anónimo',
        'licence': licence,
        'description': spec['description'],
        'consulted_on': time.strftime('%Y-%m-%d'),
        'modifications': 'Reescalado a 2000 px de ancho y recodificado como JPEG; sin retoque de color.',
        'title': spec['title'], 'subtitle': spec['subtitle'], 'category': spec['category'],
        'discipline': spec['discipline'], 'short_title': spec['short_title'],
    }
    (folder / 'cover.json').write_text(json.dumps(record, ensure_ascii=False, indent=2) + '\n')
    return record


if __name__ == '__main__':
    for name in sys.argv[1:] or list(COVERS):
        rec = fetch(name)
        print(name, rec['dimensions_px'], rec['licence'], '|', rec['author'][:60])
        time.sleep(4)
