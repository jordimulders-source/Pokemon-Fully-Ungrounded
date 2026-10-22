"""compare.png (en thumbnails.png) voor ronde 2 van de nachtaap.
python3 compose.py <ronde2-map>
Ronde 1 en 2 naast Abra, Espurr, Oranguru, Natu, Elgyem, Hatenna en de Hoenn-starters,
vergroot (3x) en op 1x, plus de silhouettest (zwart, 1x en 2x)."""
import sys, os
import numpy as np
from PIL import Image, ImageDraw
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '../../../../../../tools/concept/sprites'))
import spritelib as L

d = sys.argv[1]
r1 = os.path.join(d, '..', 'anim_front.png')
r2 = os.path.join(d, 'anim_front.png')


def own(path, k):
    a, pal = L.load_png(path)
    return L.rgb_img(a[64 * k:64 * (k + 1)], pal)


def ref(sp):
    for w in ('new', 'gba'):     # in-game versie: zo ziet de speler ze naast de onze
        try:
            fr, pal = L.load_front(sp, w); return L.rgb_img(fr[0], pal)
        except Exception:
            pass


items = [('ronde 1 f1', own(r1, 0)), ('ronde 1 f2', own(r1, 1)),
         ('RONDE 2 f1', own(r2, 0)), ('RONDE 2 f2', own(r2, 1))]
for sp in ['abra', 'espurr', 'oranguru', 'natu', 'elgyem', 'hatenna', 'munna',
           'treecko', 'torchic', 'mudkip']:
    items.append((sp, ref(sp)))


def sil(im):
    a = np.array(im); a[a[..., 3] > 0, :3] = (24, 24, 24); return Image.fromarray(a)


Z = 3; T = 64 * Z; PER = 7; BG = (250, 249, 244)
rows = (len(items) + PER - 1) // PER
W = PER * (T + 6) + 10
H = 20 + rows * (T + 16) + 30 + 70 + 30 + 140 + 10
sheet = Image.new('RGB', (W, H), BG); dr = ImageDraw.Draw(sheet)
dr.text((6, 4), 'Nachtaap fase 1, ronde 2 ("Maanogen") naast Psychic-referenties en de Hoenn-starters (in-game sprites)', fill=(0, 0, 0))
y = 20
for i, (n, im) in enumerate(items):
    if i and i % PER == 0: y += T + 16
    x = 6 + (i % PER) * (T + 6)
    t = L.checker_bg(T, T, 4 * Z); t.alpha_composite(L.scaled(im, Z))
    sheet.paste(t.convert('RGB'), (x, y + 12))
    dr.text((x + 2, y), n, fill=(150, 20, 60) if n.startswith('RONDE') else (0, 0, 0))
y += T + 16 + 8
dr.text((6, y), '1x (echte grootte)', fill=(0, 0, 0)); y += 12
for i, (n, im) in enumerate(items):
    t = Image.new('RGBA', (64, 64), BG + (255,)); t.alpha_composite(im)
    sheet.paste(t.convert('RGB'), (6 + i * 66, y))
y += 70 + 8
dr.text((6, y), 'silhouettest: 1x en 2x', fill=(0, 0, 0)); y += 12
for i, (n, im) in enumerate(items):
    t = Image.new('RGBA', (64, 64), BG + (255,)); t.alpha_composite(sil(im))
    sheet.paste(t.convert('RGB'), (6 + i * 66, y))
y += 68
for i, (n, im) in enumerate(items[:7]):
    t = Image.new('RGBA', (128, 128), BG + (255,)); t.alpha_composite(L.scaled(sil(im), 2))
    sheet.paste(t.convert('RGB'), (6 + i * 132, y))
sheet = sheet.crop((0, 0, W, y + 132))
sheet.save(os.path.join(d, 'compare.png'))
print('compare.png', sheet.size)
