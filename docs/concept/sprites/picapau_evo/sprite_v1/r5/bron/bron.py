"""Overtrekbron uit de R3-render (r7pose) (methode Picapau sprite v2): per spritepixel (1) de kleur uit R5_8x (gemiddelde van het
8x8-blok, alpha-drempel als C3_1x), (2) het onderdeel (meerderheid uit labels.png), (3) de toon (0-3) uit wit.png.
Uitvoer: bron_kleur_1x/8x.png, bron_labels.txt, bron_toon.txt, toonkaart_1x/8x.png, overtrekvel.png. Draaien: python3.11 bron.py"""
import numpy as np
from PIL import Image, ImageDraw
kl = np.asarray(Image.open('../../../blender/r7pose/R3_8x.png').convert('RGBA')).astype(float)
lb = np.asarray(Image.open('labels.png').convert('RGBA')).astype(float)
wt = np.asarray(Image.open('wit.png').convert('RGBA')).astype(float)
# labelkleuren: 0 -> 0, 0.5 (lineair) -> 188 (sRGB), 1 -> 255
def s(v): return {0: 0, 0.5: 188, 1: 255}[v]
LABEL = dict(L=('lijf', (1, 0.5, 0)), B=('buik', (1, 1, 0.5)), K=('kop', (1, 0, 0.5)), W=('wang', (1, 0, 0)), U=('oor', (0.5, 0, 0)),
             I=('oor binnen', (1, 0.5, 0.5)), N=('snavel', (0, 1, 1)), M=('mond', (0.5, 0.5, 0.5)), V=('vleugel nabij', (0, 0.5, 0)),
             F=('vleugel ver', (0, 0, 0.5)), H=('pennen nabij', (0.5, 0.5, 0)), J=('pennen ver', (0, 0.5, 0.5)), S=('stip', (0.5, 1, 0.5)),
             T=('staartschacht', (0.5, 0, 1)), X=('steunstaart', (1, 0, 1)), Z=('bliksem', (1, 1, 0)), O=('oog', (0, 0, 1)),
             P=('poot', (1, 1, 1)), Q=('klauw', (0, 0, 0)))
keys = list(LABEL); cols = np.array([[s(c) for c in LABEL[k][1]] for k in keys], float)
kleur = np.zeros((64, 64, 4), np.uint8); lab = [['.'] * 64 for _ in range(64)]; toon = [['.'] * 64 for _ in range(64)]
lum = np.zeros((64, 64))
for y in range(64):
    for x in range(64):
        k = kl[y*8:y*8+8, x*8:x*8+8].reshape(-1, 4); a = k[:, 3] >= 128
        if k[:, 3].mean() >= 128:
            kleur[y, x, :3] = k[a, :3].mean(0); kleur[y, x, 3] = 255
        l = lb[y*8:y*8+8, x*8:x*8+8].reshape(-1, 4); la = l[:, 3] > 128
        if la.sum() >= 12:
            d = ((l[la, None, :3] - cols[None]) ** 2).sum(-1).argmin(1)
            lab[y][x] = keys[np.bincount(d, minlength=len(keys)).argmax()]
        w = wt[y*8:y*8+8, x*8:x*8+8].reshape(-1, 4); wa = w[:, 3] > 128
        if wa.sum(): lum[y, x] = w[wa, :3].mean()
vals = lum[kleur[..., 3] > 0]; grens = np.percentile(vals, [20, 50, 80])
for y in range(64):
    for x in range(64):
        if kleur[y, x, 3]: toon[y][x] = str(int((lum[y, x] > grens).sum()))   # 0 donker .. 3 licht
kop = '# onderdeel per spritepixel uit R5 (' + ', '.join(f'{k}={v[0]}' for k, v in LABEL.items()) + ')\n'
open('bron_labels.txt', 'w').write(kop + '\n'.join(''.join(r) for r in lab) + '\n')
open('bron_toon.txt', 'w').write('# toon uit de witte render: 0 donker .. 3 licht\n' + '\n'.join(''.join(r) for r in toon) + '\n')
Image.fromarray(kleur).save('bron_kleur_1x.png'); Image.fromarray(kleur).resize((512, 512), Image.NEAREST).save('bron_kleur_8x.png')
tk = np.zeros((64, 64, 4), np.uint8)
for y in range(64):
    for x in range(64):
        if toon[y][x] != '.': g = [70, 130, 190, 245][int(toon[y][x])]; tk[y, x] = (g, g, g, 255)
Image.fromarray(tk).save('toonkaart_1x.png'); Image.fromarray(tk).resize((512, 512), Image.NEAREST).save('toonkaart_8x.png')
Z = 8; W = 64 * Z
v = Image.new('RGBA', (W * 2 + 60, W + 40), (230, 230, 230, 255)); d = ImageDraw.Draw(v)
v.alpha_composite(Image.open('../../../blender/r7pose/R3_8x.png').convert('RGBA'), (30, 30))
v.alpha_composite(Image.fromarray(kleur).resize((W, W), Image.NEAREST), (W + 50, 30))
for i in range(0, 65, 4):
    for ox in (30, W + 50):
        d.line([(ox + i * Z, 30), (ox + i * Z, 30 + W)], fill=(150, 150, 150)); d.line([(ox, 30 + i * Z), (ox + W, 30 + i * Z)], fill=(150, 150, 150))
    if i < 64: d.text((W + 50 + i * Z + 1, 18), str(i), fill=(0, 0, 0)); d.text((W + 34, 30 + i * Z), str(i), fill=(0, 0, 0))
v.save('overtrekvel.png')
print('onderdelen:', {LABEL[k][0]: sum(r.count(k) for r in lab) for k in keys})
print('px', int((kleur[..., 3] > 0).sum()))
