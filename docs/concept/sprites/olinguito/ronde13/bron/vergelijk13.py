"""vergelijk13.py <repo-root> : ronde13/compare.png.
Rij 1: ronde 12 en 13, frame 1 en 2, 1x en 3x. Rij 2: referenties voor de 3/4-constructie (frame 1)."""
import sys, os
from PIL import Image, ImageDraw
R = sys.argv[1]
O = os.path.join(R, 'docs/concept/sprites/olinguito')
rij1 = []
for r in ('ronde12', 'ronde13'):
    for f in (0, 1):
        rij1.append(('%s f%d' % (r.replace('ronde', 'ronde '), f + 1), os.path.join(O, r, 'anim_front.png'), f))
rij2 = []
for s, n in (('mightyena', 'anim_front_gba'), ('poochyena', 'anim_front_gba'), ('persian', 'anim_front_gba'),
             ):
    rij2.append((s, os.path.join(R, 'graphics/pokemon', s, n + '.png'), 0))
BG = (232, 232, 224)
W = 64 * 3 + 12
H = 64 + 64 * 3 + 24
cv = Image.new('RGB', (W * max(len(rij1), len(rij2)), H * 2), BG)
dr = ImageDraw.Draw(cv)
for j, items in enumerate((rij1, rij2)):
    for i, (n, p, f) in enumerate(items):
        idx = Image.open(p).crop((0, 64 * f, 64, 64 * f + 64))
        im = idx.convert('RGB')
        px, ip = im.load(), idx.load()
        for y in range(64):
            for x in range(64):
                if ip[x, y] == 0:
                    px[x, y] = BG
        x0, y0 = i * W, j * H
        cv.paste(im, (x0 + 70, y0 + 2))
        cv.paste(im.resize((192, 192), Image.NEAREST), (x0 + 6, y0 + 68))
        dr.text((x0 + 8, y0 + 262), n, fill=(40, 40, 40))
cv.save(os.path.join(O, 'ronde13', 'compare.png'))
