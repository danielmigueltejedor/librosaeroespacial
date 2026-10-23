"""Wikimedia Commons helper: find open-licensed pictures and download them with their credit.

usage:
  python commons.py search "Reyes Católicos retrato" [limit]
  python commons.py info "File:Nombre.jpg"
Only pictures whose licence is public domain, CC0, CC BY or CC BY-SA are offered.
"""
import hashlib
import html
import json
import re
import subprocess
import sys
import time
import urllib.parse
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
API = 'https://commons.wikimedia.org/w/api.php'
UA = 'studium-research/1.0 (contact: danielmigueltejedor@icloud.com)'
CACHE = Path.home() / 'Developer/work/ws/commons'
CACHE.mkdir(parents=True, exist_ok=True)

from studium.authoring.figure_images import normalise_license  # noqa: E402


def _get(url, binary=False, tries=5):
    for k in range(tries):
        r = subprocess.run(['curl', '-sL', '--max-time', '60', '-A', UA, url], capture_output=True)
        out = r.stdout
        if binary:
            if out[:2] in (b'\xff\xd8', b'\x89P'):
                return out
        else:
            text = out.decode('utf-8', 'replace')
            if text.startswith('{'):
                return text
        time.sleep(4 + 6 * k)
    raise RuntimeError('fetch failed: ' + url)


def _clean(value):
    value = re.sub(r'<[^>]+>', '', value or '')
    return re.sub(r'\s+', ' ', html.unescape(value)).strip()


def info(title, width=900):
    if not title.startswith('File:'):
        title = 'File:' + title
    q = {'action': 'query', 'titles': title, 'prop': 'imageinfo', 'format': 'json',
         'iiprop': 'url|extmetadata|size|mime', 'iiurlwidth': str(width)}
    d = json.loads(_get(API + '?' + urllib.parse.urlencode(q)))
    page = list(d['query']['pages'].values())[0]
    if 'imageinfo' not in page:
        return None
    ii = page['imageinfo'][0]
    md = ii.get('extmetadata', {})
    val = lambda k: _clean(md.get(k, {}).get('value', ''))
    lic = val('LicenseShortName') or val('UsageTerms')
    norm = normalise_license(lic)
    return dict(title=page['title'], page=ii['descriptionurl'], thumb=ii.get('thumburl') or ii['url'], mime=ii['mime'],
                width=ii['width'], height=ii['height'], license_raw=lic, license=norm[0] if norm else None,
                artist=val('Artist'), credit=val('Credit'), object_name=val('ObjectName'), date=val('DateTimeOriginal'),
                description=val('ImageDescription')[:200], restrictions=val('Restrictions'))


def search(query, limit=10):
    q = {'action': 'query', 'list': 'search', 'srnamespace': '6', 'srsearch': query, 'srlimit': str(limit), 'format': 'json'}
    d = json.loads(_get(API + '?' + urllib.parse.urlencode(q)))
    rows = []
    for hit in d['query']['search']:
        i = info(hit['title'])
        if i and i['mime'] in ('image/jpeg', 'image/png', 'image/svg+xml', 'image/tiff', 'image/gif') and i['license']:
            rows.append(i)
    return rows


def download(title, book, key, width=900, max_bytes=700_000):
    """Save the picture under <book>/figures/incoming/<key>.<ext>; return the image object for studium_figure_record."""
    i = info(title, width)
    if i is None:
        raise ValueError('not on Commons: ' + title)
    if not i['license']:
        raise ValueError(f"licence not allowed for {title}: {i['license_raw']}")
    if i['mime'] not in ('image/jpeg', 'image/png', 'image/svg+xml', 'image/gif', 'image/tiff'):
        raise ValueError('not a picture: ' + i['mime'])
    w = width
    while True:
        j = info(title, w)
        key_hash = hashlib.sha1(f"{j['thumb']}".encode()).hexdigest()[:10]
        cached = CACHE / f'{key_hash}.bin'
        if not cached.exists():
            cached.write_bytes(_get(j['thumb'], binary=True))
        data = cached.read_bytes()
        if len(data) <= max_bytes or w <= 500:
            break
        w = int(w * 0.8)
    if len(data) > 110_000:
        import io
        from PIL import Image
        im = Image.open(io.BytesIO(data))
        if im.width > 640:
            im = im.resize((640, round(im.height * 640 / im.width)), Image.LANCZOS)
        if im.mode in ('RGBA', 'LA', 'P'):
            bg = Image.new('RGB', im.size, (255, 255, 255))
            im = im.convert('RGBA'); bg.paste(im, mask=im.split()[-1]); im = bg
        else:
            im = im.convert('RGB')
        buf = io.BytesIO(); im.save(buf, 'JPEG', quality=72, optimize=True, progressive=True)
        data = buf.getvalue()
    ext = 'jpg' if data[:2] == b'\xff\xd8' else 'png'
    root = Path.home() / 'Developer/work/ws' / book / book
    out = root / 'figures' / 'incoming' / f'{key}.{ext}'
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_bytes(data)
    author = i['artist'] or i['credit'] or 'Anónimo'
    if len(author) > 300:
        author = author[:297] + '...'
    return dict(path=f'figures/incoming/{key}.{ext}', url=i['page'], title=i['title'].removeprefix('File:').rsplit('.', 1)[0][:300],
                author=author, license=i['license_raw'])


if __name__ == '__main__':
    cmd = sys.argv[1]
    if cmd == 'search':
        for r in search(sys.argv[2], int(sys.argv[3]) if len(sys.argv) > 3 else 10):
            print(f"{r['title']} | {r['license']} | {r['width']}x{r['height']} | {r['artist'][:50]} | {r['description'][:90]}")
    elif cmd == 'info':
        print(json.dumps(info(sys.argv[2]), ensure_ascii=False, indent=1))
