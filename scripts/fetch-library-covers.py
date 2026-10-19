#!/usr/bin/env python3
"""Reproduce the two licensed replacement photos; compilation never needs the network."""
from pathlib import Path
import hashlib,json
from io import BytesIO
from urllib.request import Request,urlopen
from PIL import Image
ROOT=Path(__file__).resolve().parents[1]
for slug in ['estructuras-aeroespaciales','turbomaquinas']:
 folder=ROOT/'books'/slug;meta=json.loads((folder/'cover-photo.json').read_text())
 with urlopen(Request(meta['original_url'],headers={'User-Agent':'Mozilla/5.0 Studium academic library'}),timeout=60) as response:data=response.read(50_000_001)
 if len(data)>50_000_000:raise ValueError('Unexpected download size')
 expected=meta.get('original_sha256',meta['sha256'])
 if hashlib.sha256(data).hexdigest()!=expected:raise ValueError('Remote photo changed; inspect source and license before updating')
 if slug=='estructuras-aeroespaciales':
  im=Image.open(BytesIO(data)).convert('RGB');im.thumbnail((3000,3000),Image.Resampling.LANCZOS)
  output=BytesIO();im.save(output,format='JPEG',quality=94,optimize=True,subsampling=0);data=output.getvalue()
  if hashlib.sha256(data).hexdigest()!=meta['sha256']:
   raise ValueError('Image codec differs from recorded derivative; preserve existing cover and review the new encoding separately')
 target=folder/meta['file'];temp=target.with_suffix('.jpg.tmp');temp.write_bytes(data);temp.replace(target)
 print(slug,hashlib.sha256(data).hexdigest())
