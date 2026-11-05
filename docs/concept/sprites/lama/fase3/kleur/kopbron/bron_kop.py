"""Kop-overtrekbron fase 3 (5 nov). Jordi: "probeer het hoofd na te maken zoals in het model, nu ben je gewoon weer dingen aan
het verzinnen" + eerder "maak het hoofd maar wat groter dan het silhouet". Het model (poppetje W3, pose C2) met alleen de kop
(kop, oren, bombín, pony, vlechten) KOPK x groter, op dezelfde schaal/positie als silhouet ronde 2 (lijf valt precies samen).
Uitvoer: kop_overtrekvel.png (links render, rechts per spritepixel de meerderheidskleur + lijnen, raster met coördinaten),
kop_labels.txt (onderdeel per pixel), kop_lijnen.txt ('#' = omlijning in het model), kop_kleur_64.png (bemonsterd, géén sprite).
Draaien vanuit de repo-root: python3 docs/concept/sprites/lama/fase3/kleur/kopbron/bron_kop.py"""
import os, sys, math
import numpy as np
from PIL import Image, ImageDraw, ImageFont
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '../../../ontwerp'))
import pop3d_lama as L, fase3_r4 as F4
P = L.P
KOPK, YAW, PITCH = 1.25, 45, 8
X0, X1, Y0, Y1 = 8, 36, 0, 26          # kopzone in spritepixels
L.set_vacht('bont (foto 4)'); L.COL['lid'] = L.COL['head']; L.COL['lip'] = '#C9A982'; F4.HEAD_YAW = 18
W3 = dict(breed=1.26, nr=7, legk=1.85)
m = F4.fase3_r4('Y', **W3)
Rc = P.rot_x(math.radians(PITCH)) @ P.rot_y(math.radians(YAW))
pts = np.array([Rc @ c for c, r, R0, g in m.parts]); rs = np.array([r.max() for c, r, R0, g in m.parts])
x0, x1, y0, y1 = (pts[:, 0] - rs).min(), (pts[:, 0] + rs).max(), (pts[:, 1] - rs).min(), (pts[:, 1] + rs).max()
fill = 0.99; scale = L.R * fill / max(x1 - x0, y1 - y0)
c = ((x0 + x1) / 2, (y0 + y1) / 2 + (1 - fill) * L.R / scale * 0.5)      # = bron.py ronde 2
a0, a1 = m.kop_range
kop = m.parts[a0:a1]
# pivot: de oorpunten (hoogste punt van de kop in beeld): de bovenkant blijft op zijn plek (rij 1, zoals silhouet ronde 2),
# de kop groeit naar voren en omlaag over de bovenkant van de hals. Uniform geschaald: vormen van het model blijven gelijk.
KOPK = float(sys.argv[1]) if len(sys.argv) > 1 else KOPK
hi = max(range(len(kop)), key=lambda i: (Rc @ kop[i][0])[1] + kop[i][1].max())
piv = kop[hi][0] + np.linalg.inv(Rc) @ np.array((0, kop[hi][1].max(), 0))
m.parts[a0:a1] = [(piv + KOPK * (cc - piv), r * KOPK, R0, g) for cc, r, R0, g in kop]
zbuf, gid, nrm, groups = L.render(m, YAW, PITCH, scale, c)
und, a = L.shade(zbuf, gid, nrm, groups, out=L.R)
rgb = np.array(und); k = L.R // 64
lijn = np.all(rgb == L.LINE, -1) & (gid >= 0)
kopg = {'head', 'ear', 'eye', 'glint', 'lid', 'lip', 'nose', 'hat', 'hatband', 'pony', 'braid', 'tassel', 'gold'}
lab = np.full((64, 64), '.', object); col = np.full((64, 64, 3), 255, np.uint8); lin = np.zeros((64, 64), bool)
for y in range(64):
    for x in range(64):
        blk = gid[y*k:(y+1)*k, x*k:(x+1)*k]; cov = (blk >= 0).mean()
        if cov < 0.5: continue
        vals, cnt = np.unique(blk[blk >= 0], return_counts=True); g = groups[vals[cnt.argmax()]]
        lab[y, x] = g
        lin[y, x] = lijn[y*k:(y+1)*k, x*k:(x+1)*k].mean() > 0.35
        pix = rgb[y*k:(y+1)*k, x*k:(x+1)*k][blk == vals[cnt.argmax()]]
        col[y, x] = pix.mean(0)
        if lin[y, x]: col[y, x] = L.LINE
SUF = '' if len(sys.argv) < 3 else sys.argv[2]
Image.fromarray(col).save(os.path.join(HERE, f'kop_kleur_64{SUF}.png'))
afk = {'head': 'K', 'ear': 'O', 'eye': 'E', 'glint': 'g', 'lid': 'D', 'lip': 'l', 'nose': 'n', 'hat': 'H', 'hatband': 'B',
       'pony': 'p', 'braid': 'V', 'tassel': 'T', 'gold': 'G', 'neck': 'N', '.': '.'}
with open(os.path.join(HERE, f'kop_labels{SUF}.txt'), 'w') as f:
    f.write('# kopzone x%d-%d y%d-%d; K kop, O oor, E oog, g glans, D ooglid, l onderlip, n neusgat, H bombín, B hoedband, p pony, V vlecht, T tullma, G gouden ring, N hals, x = ander (lijf/kleding), . leeg\n' % (X0, X1 - 1, Y0, Y1 - 1))
    f.write('     ' + ''.join(str(x % 10) for x in range(X0, X1)) + '\n')
    for y in range(Y0, Y1):
        f.write(f'y{y:02d}  ' + ''.join(afk.get(lab[y, x], 'x') for x in range(X0, X1)) + '\n')
with open(os.path.join(HERE, f'kop_lijnen{SUF}.txt'), 'w') as f:
    f.write('     ' + ''.join(str(x % 10) for x in range(X0, X1)) + '\n')
    for y in range(Y0, Y1):
        f.write(f'y{y:02d}  ' + ''.join('#' if lin[y, x] else ('o' if lab[y, x] != '.' else '.') for x in range(X0, X1)) + '\n')
# overtrekvel: links render (8 px per spritepixel), rechts bemonsterde kleur, beide met raster en coördinaten
S = 16; W, H = (X1 - X0) * S, (Y1 - Y0) * S
F = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 10)
links = Image.fromarray(rgb[Y0*k:Y1*k, X0*k:X1*k]).resize((W, H), Image.LANCZOS)
rechts = Image.fromarray(col[Y0:Y1, X0:X1]).resize((W, H), Image.NEAREST)
vel = Image.new('RGB', (W * 2 + 3 * 24, H + 40), 'white'); d = ImageDraw.Draw(vel)
for i, im in enumerate((links, rechts)):
    ox = 24 + i * (W + 24); vel.paste(im, (ox, 24)); dd = ImageDraw.Draw(vel)
    for x in range(X1 - X0 + 1):
        dd.line([(ox + x * S, 24), (ox + x * S, 24 + H)], fill=(150, 150, 220) if (x + X0) % 5 else (60, 60, 200))
        if x < X1 - X0 and (x + X0) % 2 == 0: dd.text((ox + x * S + 2, 10), str(x + X0), font=F, fill=(60, 60, 60))
    for y in range(Y1 - Y0 + 1):
        dd.line([(ox, 24 + y * S), (ox + W, 24 + y * S)], fill=(150, 150, 220) if (y + Y0) % 5 else (60, 60, 200))
        if y < Y1 - Y0: dd.text((ox - 20, 24 + y * S + 3), str(y + Y0), font=F, fill=(60, 60, 60))
vel.save(os.path.join(HERE, f'kop_overtrekvel{SUF}.png'))
ys, xs = np.nonzero(lab != '.')
print('kop ×', KOPK, '| bovenste rij', ys.min(), '| kopzone-pixels', int(sum(lab[y, x] in kopg for y in range(64) for x in range(64))))
