"""Snelle 3D-preview (512 px, basiskleuren + schaduw) om de pose te beoordelen vóór de conversie.
Gebruik: preview.py <model> uit.png [yaw,pitch,headturn ...]"""
import importlib
import os
import sys
import numpy as np
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(HERE, 'models'))
from model3d import camera, bbox, render

mod = importlib.import_module(sys.argv[1])
views = [tuple(float(v) for v in a.split(',')) for a in sys.argv[3:]] or [(mod.SPEC['yaw'], mod.SPEC['pitch'])]
tiles = []
for v in views:
    if len(v) > 2 and hasattr(mod, 'HEAD_TURN'):
        mod.HEAD_TURN = v[2]
    m = mod.build()
    Rc = camera(v[0], v[1], v[3] if len(v) > 3 else 1.0)
    x0, x1, y0, y1 = bbox(m, Rc)
    S = 300
    sc = S * 0.95 / max(x1 - x0, y1 - y0)
    R = render(m, Rc, S, sc, (x0 - (S / sc - (x1 - x0)) / 2, y1 + (S / sc - (y1 - y0)) / 2))
    pal = mod.SPEC['palette']
    img = np.full((S, S, 3), 255, np.uint8)
    L = np.array((-0.6, 0.7, 0.35)); L /= np.linalg.norm(L)
    lit = R['n'] @ L
    for i, mn in enumerate(R['mats']):
        sel = R['mat'] == i
        key = mn + 'b'
        col = np.array(pal.get(key, (200, 0, 200)))
        img[sel] = np.where((lit[sel] > 0)[:, None], col, col * 0.75)
    tiles.append(Image.fromarray(img))
out = Image.new('RGB', (300 * len(tiles), 300), 'white')
for i, t in enumerate(tiles):
    out.paste(t, (i * 300, 0))
out.save(sys.argv[2])
