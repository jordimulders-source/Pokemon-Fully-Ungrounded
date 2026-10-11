"""Celebi-intro (src/data/legend_intros_cheap2.h): vier Gold/Silver/Crystal-plekken als 160x144-uitsneden in vier tinten.
Gebruik: python3 tools/grounded/celebi_gsc.py <cachemap>
Haalt de echte kaarten uit pret/pokecrystal (maps/*.blk, data/tilesets/*_metatiles.bin, gfx/tilesets/*.png) naar
<cachemap>, rendert ze (tile-id >= 0x80 = tile - 0x20 uit de png, VRAM-bank 1), knipt de uitsneden en ontdubbelt de
tiles (ook gespiegeld). Schrijft graphics/battle_transitions/legend_celebi_gsc.png (kleur 1-4 = tint wit..zwart) en
legend_celebi_gsc_maps.bin (4 x 20 x 18 tilemap-items: LCC_TILE + tile, spiegelbits, BG-palet 14)."""
import sys, os, urllib.request
import numpy as np
from PIL import Image

REPO = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
CACHE = sys.argv[1]
SRC = 'https://raw.githubusercontent.com/pret/pokecrystal/master/'
BASE = 256  # LCC_TILE
# naam: (kaart, tileset, breedte in blokken, uitsnede linksboven in pixels)
SCENES = [
    ('NewBarkTown', 'johto', 10, 64, 0),          # Elms lab en het huis van de speler
    ('GoldenrodCity', 'johto_modern', 20, 40, 56),  # de Radio Tower
    ('EcruteakCity', 'johto', 20, 480, 0),        # de Tin Tower
    ('IlexForest', 'forest', 15, 56, 296),        # het schrijn
]


def fetch(path):
    dst = os.path.join(CACHE, path.replace('/', '__'))
    if not os.path.exists(dst):
        os.makedirs(CACHE, exist_ok=True)
        urllib.request.urlretrieve(SRC + path, dst)
    return dst


def tileset(ts):
    a = np.array(Image.open(fetch('gfx/tilesets/%s.png' % ts)).convert('L'))
    sh = (3 - a.astype(np.int32) * 4 // 256).astype(np.uint8)   # 255 -> 0 (wit) .. 0 -> 3 (zwart)
    return [sh[y:y + 8, x:x + 8] for y in range(0, a.shape[0], 8) for x in range(0, a.shape[1], 8)]


def render(blk, ts, w):
    b = open(fetch('maps/%s.blk' % blk), 'rb').read()
    meta = open(fetch('data/tilesets/%s_metatiles.bin' % ts), 'rb').read()
    tl = tileset(ts)
    img = np.zeros((len(b) // w * 32, w * 32), np.uint8)
    for i, m in enumerate(b):
        for k in range(16):
            t = meta[m * 16 + k]
            t = t if t < 0x80 else t - 0x20
            y, x = (i // w) * 32 + (k // 4) * 8, (i % w) * 32 + (k % 4) * 8
            img[y:y + 8, x:x + 8] = tl[t] if t < len(tl) else 0
    return img


uniq, keys, maps = [np.zeros((8, 8), np.uint8)], {}, []
for blk, ts, w, x0, y0 in SCENES:
    crop = render(blk, ts, w)[y0:y0 + 144, x0:x0 + 160]
    assert crop.shape == (144, 160), blk
    for ty in range(18):
        for tx in range(20):
            t = crop[ty * 8:ty * 8 + 8, tx * 8:tx * 8 + 8]
            for fl, v in ((0, t), (1, t[:, ::-1]), (2, t[::-1, :]), (3, t[::-1, ::-1])):
                if v.tobytes() in keys:
                    hit = (keys[v.tobytes()], fl)
                    break
            else:
                keys[t.tobytes()] = len(uniq)
                hit = (len(uniq), 0)
                uniq.append(t.copy())
            maps.append((BASE + hit[0]) | (hit[1] << 10) | (14 << 12))
sheet = np.zeros(((len(uniq) + 15) // 16 * 8, 128), np.uint8)
for i, t in enumerate(uniq):
    sheet[(i // 16) * 8:(i // 16) * 8 + 8, (i % 16) * 8:(i % 16) * 8 + 8] = (t + 1) if i else 0
pal = [(0, 0, 0), (232, 248, 168), (152, 200, 80), (72, 128, 64), (24, 56, 32)] + [(0, 0, 0)] * 11
im = Image.fromarray(sheet, 'P')
im.putpalette([c for rgb in pal for c in rgb])
d = os.path.join(REPO, 'graphics/battle_transitions')
im.save(os.path.join(d, 'legend_celebi_gsc.png'))
open(os.path.join(d, 'legend_celebi_gsc_maps.bin'), 'wb').write(b''.join(v.to_bytes(2, 'little') for v in maps))
print('unieke tiles:', len(uniq))
