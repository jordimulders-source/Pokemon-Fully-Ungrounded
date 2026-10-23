"""skelet.py <repo-root> <ronde15-map> <uit.png> [dx dy]
Maakt skelet.png: (1) Poochyena (referentie, frame 1), (2) olinguito ronde 15 zonder romp/achterpoten met
het Poochyena-lijf als rode onderlaag (verschoven dx,dy, niet geschaald), (3) de overtekening (ronde 15)
met de omtrek van de onderlaag als rode stippen erover, (4) het resultaat. Alles 1x en 4x.
"""
import sys, os
from PIL import Image, ImageDraw

R, D, UIT = sys.argv[1], sys.argv[2], sys.argv[3]
dx = int(sys.argv[4]) if len(sys.argv) > 4 else 0
dy = int(sys.argv[5]) if len(sys.argv) > 5 else 5
sys.argv = [sys.argv[0], R, str(dx), str(dy)]
sys.path.insert(0, os.path.join(D, 'bron'))
import onderlaag  # noqa: E402

BG = (152, 208, 160)
S = 4
pooch = Image.open(R + '/graphics/pokemon/poochyena/anim_front.png').convert('RGB').crop((0, 0, 64, 64))
res = Image.open(D + '/anim_front.png').convert('RGB').crop((0, 0, 64, 64))
mask = onderlaag.pixels()

# olinguito zonder romp en achterpoten: lees delen_abs en sla die delen over
B = os.path.join(D, 'bron')
pal = {}
for r in open(os.path.join(B, 'palet.txt'), encoding='utf-8'):
    p = r.split('#')[0].split()
    if p:
        pal[p[0]] = tuple(int(v) for v in p[1:4])
zonder = Image.new('RGB', (64, 64), BG)
skip = False
for r in open(os.path.join(B, 'delen_abs.txt'), encoding='utf-8'):
    r = r.rstrip('\n')
    if r.startswith('## '):
        skip = r.split()[1] in ('lijf', 'been_voor', 'been_achter')
        continue
    r = r.split('#')[0].strip()
    if not r or skip:
        continue
    y, x, px = r.split()
    for i, c in enumerate(px):
        if c != '.':
            zonder.putpixel((int(x) + i, int(y)), pal[c])

onder = zonder.copy()
for (x, y), c in mask.items():
    if onder.getpixel((x, y)) == BG:
        onder.putpixel((x, y), (200, 60, 60) if c == '0' else (240, 150, 150))

over = res.copy()
for (x, y) in mask:
    rand = any((x + a, y + b) not in mask for a, b in ((1, 0), (-1, 0), (0, 1), (0, -1)))
    if rand:
        over.putpixel((x, y), (255, 0, 0))

panelen = [pooch, onder, over, res]
titels = ['Poochyena (referentie)', 'onderlaag (+%d,+%d)' % (dx, dy), 'overtekening + omtrek onderlaag', 'resultaat ronde 15']
W = Image.new('RGB', (len(panelen) * (64 * S + 8) + 8, 64 * S + 64 + 30), (255, 255, 255))
d = ImageDraw.Draw(W)
for i, p in enumerate(panelen):
    x = 8 + i * (64 * S + 8)
    d.text((x, 4), titels[i], fill=(0, 0, 0))
    W.paste(p.resize((64 * S, 64 * S), Image.NEAREST), (x, 18))
    W.paste(p, (x, 64 * S + 24))
W.save(UIT)
