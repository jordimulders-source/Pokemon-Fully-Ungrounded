# Rendert alle bestaande tilesets als overzichtsvellen (metatiles 16x16, 8 per rij, zoals in Porymap)
# naar tilesets/bestaand/{primary,secondary}/<naam>.png. Secondaries worden getekend met een primary waarmee
# ze in layouts.json echt gebruikt worden (hun metatiles verwijzen ook naar tegels uit de primary).
import json, os, re, struct, sys
import numpy as np
from PIL import Image

ROOT = 'data/tilesets'
OUT = 'tilesets/bestaand'
PER_ROW = 8

def tsname(sym):
    return re.sub(r'(?<!^)(?=[A-Z])', '_', sym.replace('gTileset_', '')).lower()

def load(dirn):
    base = dirn
    if os.path.exists(dirn + '/BASE'):
        base = os.path.join(os.path.dirname(dirn), open(dirn + '/BASE').read().strip())
    tdir = base
    if os.path.exists(dirn + '/TILES'):
        tdir = os.path.join(os.path.dirname(dirn), open(dirn + '/TILES').read().strip())
    tp = tdir + '/tiles.4bpp'
    if not os.path.exists(tp):
        return None
    tiles = np.frombuffer(open(tp, 'rb').read(), np.uint8)
    nt = len(tiles) // 32
    lo, hi = tiles & 15, tiles >> 4
    pix = np.stack([lo, hi], -1).reshape(nt, 8, 8)
    mts = np.frombuffer(open(base + '/metatiles.bin', 'rb').read(), '<u2').reshape(-1, 8)
    pals = np.zeros((16, 16, 3), np.uint8)
    for i in range(16):
        f = f'{dirn}/palettes/{i:02}.pal'
        if os.path.exists(f):
            lines = open(f).read().split('\n')[3:19]
            pals[i] = [tuple(map(int, l.split())) for l in lines]
    return pix, mts, pals

def render(mts, tile_of, pals):
    n = len(mts)
    rows = (n + PER_ROW - 1) // PER_ROW
    img = np.full((rows * 16, PER_ROW * 16, 3), 40, np.uint8)
    for m in range(n):
        ox, oy = (m % PER_ROW) * 16, (m // PER_ROW) * 16
        for layer in range(2):
            for k in range(4):
                e = int(mts[m, layer * 4 + k])
                t, hf, vf, pn = e & 0x3FF, (e >> 10) & 1, (e >> 11) & 1, (e >> 12) & 15
                tp = tile_of(t)
                if hf: tp = tp[:, ::-1]
                if vf: tp = tp[::-1, :]
                blk = img[oy + (k // 2) * 8: oy + (k // 2) * 8 + 8, ox + (k % 2) * 8: ox + (k % 2) * 8 + 8]
                col = pals[pn][tp]
                mask = tp != 0 if layer else np.ones_like(tp, bool)
                blk[mask] = col[mask]
    return Image.fromarray(img).resize((PER_ROW * 32, rows * 32), Image.NEAREST)

layouts = json.load(open('data/layouts/layouts.json'))['layouts']
pairs = {}
for L in layouts:
    if 'primary_tileset' in L:
        pairs.setdefault(tsname(L['secondary_tileset']), tsname(L['primary_tileset']))

os.makedirs(OUT + '/primary', exist_ok=True)
os.makedirs(OUT + '/secondary', exist_ok=True)
cache = {}
def get(kind, name):
    key = (kind, name)
    if key not in cache:
        cache[key] = load(f'{ROOT}/{kind}/{name}')
    return cache[key]

done = 0
for name in sorted(os.listdir(ROOT + '/primary')):
    d = get('primary', name)
    if not d: continue
    pix, mts, pals = d
    tile_of = lambda t, pix=pix: pix[t] if t < len(pix) else np.zeros((8, 8), np.uint8)
    render(mts, tile_of, pals).save(f'{OUT}/primary/{name}.png'); done += 1
for name in sorted(os.listdir(ROOT + '/secondary')):
    d = get('secondary', name)
    if not d: continue
    spix, smts, spals = d
    prim = get('primary', pairs.get(name, 'general')) or get('primary', 'general')
    ppix, _, ppals = prim
    pals = np.concatenate([ppals[:6], spals[6:]])
    def tile_of(t, ppix=ppix, spix=spix):
        if t < 512:
            return ppix[t] if t < len(ppix) else np.zeros((8, 8), np.uint8)
        t -= 512
        return spix[t] if t < len(spix) else np.zeros((8, 8), np.uint8)
    render(smts, tile_of, pals).save(f'{OUT}/secondary/{name}.png'); done += 1
print(done, 'tilesets')
