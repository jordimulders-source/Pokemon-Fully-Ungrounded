"""Silhouet ronde 5 = ronde 4 + 5 px verdikking van de voorpoten in de onderlaag-verhouding (Jordi: "in het origineel
zijn de voorpoten ook ietsje dikker"). Schrijft silhouet/ronde5.txt en een overlay op de onderlaag."""
import os
from PIL import Image, ImageDraw
H = os.path.dirname(os.path.abspath(__file__)); S = os.path.join(H, '../../../silhouet')
sil = [list(l.rstrip('\n')) for l in open(os.path.join(S, 'ronde4.txt')) if l.strip()]
ERBIJ = [(26, 54),   # manchet opgetilde poot: ronder naar rechts (inkeping/lucht begint nu op y 55)
         (25, 56),   # manchet: ronde onderkant rechts
         (32, 54),   # staande poot: bovenkant 1 px breder onder de curve
         (31, 58),   # staande poot: pols 5 px i.p.v. 4
         (31, 59)]   # staande poot: enkel
for x, y in ERBIJ:
    assert sil[y][x] == '.'; sil[y][x] = '#'
open(os.path.join(S, 'ronde5.txt'), 'w').write('\n'.join(''.join(r) for r in sil) + '\n')
print('ronde5.txt:', sum(r.count('#') for r in sil), 'px (+%d)' % len(ERBIJ))
u = Image.open(os.path.join(S, 'onderlaag_b1c_256.png')).convert('RGBA')
ov = u.copy(); d = ImageDraw.Draw(ov, 'RGBA')
for y in range(64):
    for x in range(64):
        if sil[y][x] == '#':
            d.rectangle([x * 4, y * 4, x * 4 + 3, y * 4 + 3], fill=(255, 0, 0, 255) if (x, y) in ERBIJ else (40, 32, 44, 110))
z = ov.crop((48, 176, 144, 256)).resize((96 * 4, 80 * 4), Image.NEAREST)
W = Image.new('RGBA', (256 + 10 + z.width, max(256, z.height)), (236, 236, 230, 255))
W.alpha_composite(ov, (0, 0)); W.alpha_composite(z, (266, 0))
W.save(os.path.join(S, 'overlay_ronde5.png'))
