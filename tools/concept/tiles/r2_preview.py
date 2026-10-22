"""Hulpje: render een bestaande Hoenn-kaart met de Andes-primary (secondary ongewijzigd) om de omkleuring te
beoordelen. python3 tools/concept/tiles/r2_preview.py <Kaart> <uit.png> [x0 y0 x1 y1]"""
import json, os, struct, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from PIL import Image
from andes_primary import build
from r2lib import load_set
from tilelib import _tsname

m, out = sys.argv[1], sys.argv[2]
pair = build()
d = json.load(open(f'data/maps/{m}/map.json'))
L = [l for l in json.load(open('data/layouts/layouts.json'))['layouts'] if l.get('id') == d['layout']][0]
sec = load_set('secondary', _tsname(L['secondary_tileset']))
w, h = L['width'], L['height']
x0, y0, x1, y1 = (map(int, sys.argv[3:7]) if len(sys.argv) > 6 else (0, 0, w, h))
v = struct.unpack(f'<{w * h}H', open(L['blockdata_filepath'], 'rb').read())
pair.st = list(sec['tiles']); pair.sm = [list(map(int, r)) for r in sec['mts']]
for i in range(6, 13):
    pair.pals[i] = [tuple(int(q) for q in c) for c in sec['pals'][i]]
grid = [[v[y * w + x] & 0x3FF for x in range(x0, x1)] for y in range(y0, y1)]
Image.fromarray(pair.render(grid)).save(out)
