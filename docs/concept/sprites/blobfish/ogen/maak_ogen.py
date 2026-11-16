"""Oogvarianten blobfish fase 1 (op r5A/r5B). Alleen oogpixels + directe buren veranderen.
Zones: nabij oog x18-21,y44-47; ver oog x9-11,y40-43 (+ (8,43)); buitenlijn en alpha bevroren."""
from PIL import Image, ImageDraw
import os
H = os.path.dirname(os.path.abspath(__file__))
R5 = os.path.join(H, '..', 'sprite_r5')
# W=13 wit, G=12 lichtgrijs, K=1 zwart, R=2 lijnrood, 4=lijftint donker, .=ongewijzigd
SYM = {'W': 13, 'G': 12, 'K': 1, 'R': 2, '4': 4}
NZ = (18, 44)  # nabij: 4 kolommen x18..21, 4 rijen y44..47
FZ = (8, 40)   # ver:   4 kolommen x8..11,  4 rijen y40..43
V = {
 1: ('huidig (r5): 2x2, glans linksboven, pupil rechtsboven, wit sikkeltje onder',
     ['....', '.GK.', '.GG.', '.RR.'],
     ['....', '.GK.', '.GG.', '....']),
 2: ('zoals het model: wit oog 2x2, zwarte pupil rechtsboven, lijnrode rand rondom',
     ['.RR.', 'RWKR', 'RWWR', '.RR.'],
     ['....', '.WKR', '.WWR', '.RR.']),
 3: ('groot rond oog 3x3 (Magikarp-stijl): wit, 1 zwarte pupil midden, rand rechts/onder',
     ['WWWR', 'WKWR', 'WWWR', 'RRR4'],
     ['..WR', '.WKR', '.WWR', '.RR.']),
 4: ('zwart kraaloog 2x2 met 1 witte glanspixel linksboven',
     ['4444', '4WK4', '4KK4', '4RR4'],
     ['....', '.WK4', '.KK4', '.44.']),
 5: ('derpy scheel: wit oog 2x3 (ver 2x2), pupillen omhoog naar elkaar toe',
     ['4KWR', '4WWR', '4WWR', '4RR4'],
     ['....', '.WKR', '.WWR', '.RR.']),
 6: ('breder wit oog 3x2, pupil rechtsboven, lijnrood ooglid onder',
     ['4444', 'WWKR', 'WWWR', 'RRR4'],
     ['....', '.WWK', '.WWW', '.RRR']),
 7: ('extra: blije dichte ogen (boogjes ^ ^), zwart',
     ['4444', '4KK4', 'K44K', '4444'],
     ['....', '.KK4', '.44K', '.44.']),
}
def patch(im, z, pat):
    x0, y0 = z
    for dy, row in enumerate(pat):
        for dx, ch in enumerate(row):
            if ch != '.':
                im.putpixel((x0 + dx, y0 + dy), SYM[ch])
ZONE = {(x, y) for x in range(18, 22) for y in range(44, 48)} | {(x, y) for x in range(8, 12) for y in range(40, 44)}
OUT = {}
for ab in 'AB':
    base = Image.open(os.path.join(R5, f'blobfish_r5{ab}.png'))
    for n, (desc, near, far) in V.items():
        im = base.copy()
        patch(im, NZ, near); patch(im, FZ, far)
        diff = [(x, y) for x in range(64) for y in range(64) if im.getpixel((x, y)) != base.getpixel((x, y))]
        assert all(p in ZONE for p in diff), (n, ab, [p for p in diff if p not in ZONE])
        for x in range(64):
            for y in range(64):
                assert (im.getpixel((x, y)) == 0) == (base.getpixel((x, y)) == 0)  # alpha bevroren
        # buitenlijn (opake pixel met transparante buur) onveranderd
        for (x, y) in diff:
            nb = [(x+1,y),(x-1,y),(x,y+1),(x,y-1)]
            assert not any(base.getpixel(q) == 0 for q in nb), ('buitenlijn', n, x, y)
        im.save(os.path.join(H, f'ogen_v{n}_{ab}.png'), transparency=0)
        OUT[(n, ab)] = (im, sorted(diff, key=lambda p: (p[1], p[0])))
        print(f'v{n}{ab}: {len(diff)} px gewijzigd, alles binnen oogzone, alpha/buitenlijn bevroren')
# notities
PAL = {1: 'zwart', 2: 'lijnrood', 4: 'lijf donker', 6: 'lijf midden', 7: 'lijf licht', 12: 'lichtgrijs', 13: 'wit'}
base = Image.open(os.path.join(R5, 'blobfish_r5A.png'))
with open(os.path.join(H, 'NOTITIES.md'), 'w') as f:
    f.write('# Blobfish fase 1: oogvarianten (op r5)\n\n')
    f.write('Jordi: "probeer een aantal verschillende ogen uit en laat me zien". Basis `sprite_r5/blobfish_r5A.png` en `_r5B.png`; '
            'per variant A en B (zelfde pixels, B = lichtronde). Alleen oog + directe buren (nabij x18-21/y44-47, ver x8-11/y40-43); '
            'alpha, buitenlijn en de rest pixeldiff 0 (asserts in `maak_ogen.py`). Kleuren: bestaande indexen 1 zwart, 2 lijnrood, 4 lijf, 12 lichtgrijs, 13 wit. '
            'Vel: `ogen_vel.png`.\n\n')
    for n, (desc, _, _) in V.items():
        im, diff = OUT[(n, 'A')]
        f.write(f'## v{n}: {desc}\n')
        if not diff:
            f.write('- geen wijziging (referentie)\n\n'); continue
        f.write(f'- {len(diff)} px: ' + ', '.join(f'({x},{y}) {PAL[base.getpixel((x,y))]}→{PAL[im.getpixel((x,y))]}' for x, y in diff) + '\n\n')
# vel
BG = (214, 222, 214)
rowh = 236; W = 1000
vel = Image.new('RGB', (W, rowh * len(V) + 10), (250, 250, 250))
d = ImageDraw.Draw(vel)
for i, (n, (desc, _, _)) in enumerate(V.items()):
    y0 = 5 + i * rowh
    d.text((8, y0), f'v{n}', fill=(0, 0, 0))
    d.text((40, y0), desc, fill=(40, 40, 40))
    x = 8
    for ab in 'AB':
        im = OUT[(n, ab)][0].convert('RGBA')
        crop = im.crop((4, 33, 30, 56)).resize((26 * 8, 23 * 8), Image.NEAREST)
        tile = Image.new('RGB', crop.size, BG); tile.paste(crop, (0, 0), crop)
        vel.paste(tile, (x, y0 + 18)); d.text((x, y0 + 18 + crop.size[1] + 2), f'{ab} 8x', fill=(0, 0, 0)); x += crop.size[0] + 12
    for ab in 'AB':
        im = OUT[(n, ab)][0].convert('RGBA')
        for s in (1, 2):
            sp = im.resize((64 * s, 64 * s), Image.NEAREST)
            for bg in (BG, (36, 40, 48)) if s == 1 else (BG,):
                tile = Image.new('RGB', sp.size, bg); tile.paste(sp, (0, 0), sp)
                vel.paste(tile, (x, y0 + 18)); 
                d.text((x, y0 + 18 + sp.size[1] + 2), f'{ab} {s}x', fill=(0, 0, 0))
                x += sp.size[0] + 6
        x += 6
vel.save(os.path.join(H, 'ogen_vel.png'))
