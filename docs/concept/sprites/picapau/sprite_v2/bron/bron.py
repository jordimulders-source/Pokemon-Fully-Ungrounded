"""Overtrekbron uit het goedgekeurde B1-model (lama-fase-3-methode): per spritepixel
(1) de kleur uit de render (gemiddelde van het 8x8-blok), (2) het onderdeel (meerderheid uit B1/labels.png),
(3) de toon uit de witte render (licht/schaduw). Uitvoer: bron_kleur_8x.png, bron_labels.txt, overtrekvel.png."""
import numpy as np
from PIL import Image, ImageDraw
B = '../../blender/B1/'
kl = np.asarray(Image.open(B + 'b1.png').convert('RGBA')).astype(float)
lb = np.asarray(Image.open(B + 'labels.png').convert('RGBA')).astype(float)
LBL = {'Y': (255, 255, 0), 'V': (0, 255, 0), 'S': (255, 0, 255), 'R': (255, 0, 0), 'K': (0, 0, 0),
       'N': (0, 255, 255), 'O': (0, 0, 255), 'P': (255, 255, 255)}
NAAM = dict(Y='geel lijf/kop', V='vleugel', S='staart', R='wang', K='kuiftop', N='snavel', O='oog+glans', P='poot/klauw')
keys = list(LBL); cols = np.array([LBL[k] for k in keys], float)
kleur = np.zeros((64, 64, 4), np.uint8); lab = [['.'] * 64 for _ in range(64)]
for y in range(64):
    for x in range(64):
        k = kl[y*8:y*8+8, x*8:x*8+8].reshape(-1, 4); a = k[:, 3] > 128
        l = lb[y*8:y*8+8, x*8:x*8+8].reshape(-1, 4); la = l[:, 3] > 128
        if a.sum() >= 20:
            kleur[y, x, :3] = k[a, :3].mean(0); kleur[y, x, 3] = 255
        if la.sum() >= 12:   # ook dunne delen (snavel, klauw) die minder dan de helft van het blok vullen
            d = ((l[la, None, :3] - cols[None]) ** 2).sum(-1).argmin(1)
            lab[y][x] = keys[np.bincount(d, minlength=len(keys)).argmax()]
open('bron_labels.txt', 'w').write('# onderdeel per spritepixel uit B1 (' + ', '.join(f'{k}={v}' for k, v in NAAM.items()) + ')\n' + '\n'.join(''.join(r) for r in lab) + '\n')
Image.fromarray(kleur).resize((512, 512), Image.NEAREST).save('bron_kleur_8x.png')
Image.fromarray(kleur).save('bron_kleur_1x.png')
# overtrekvel: render | bron 8x met raster en coördinaten
Z = 8; W = 64 * Z
v = Image.new('RGBA', (W * 2 + 60, W + 40), (230, 230, 230, 255)); d = ImageDraw.Draw(v)
r = Image.open(B + 'b1.png').convert('RGBA'); v.alpha_composite(r, (30, 30))
v.alpha_composite(Image.fromarray(kleur).resize((W, W), Image.NEAREST), (W + 50, 30))
for i in range(0, 65, 4):
    for ox in (30, W + 50):
        d.line([(ox + i * Z, 30), (ox + i * Z, 30 + W)], fill=(150, 150, 150)); d.line([(ox, 30 + i * Z), (ox + W, 30 + i * Z)], fill=(150, 150, 150))
    if i < 64: d.text((W + 50 + i * Z + 1, 18), str(i), fill=(0, 0, 0)); d.text((W + 52 - 18 + 0, 30 + i * Z), str(i), fill=(0, 0, 0))
v.save('overtrekvel.png')
print('onderdelen:', {k: sum(r.count(k) for r in lab) for k in keys})
