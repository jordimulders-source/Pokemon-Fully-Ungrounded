"""Pootstudie ronde 2 (Jordi 6 nov: "kijk ook naar andere pokemon sprites van niet insecten hiervoor"):
Gen 3-viervoeters, frame 1 op 8x, met een raster per 8 px. Schrijft studie_poten.png."""
import os
from PIL import Image, ImageDraw, ImageFont
HERE = os.path.dirname(os.path.abspath(__file__))
G = os.path.join(HERE, '../../../../../../graphics/pokemon/')
NAMEN = ['teddiursa', 'skitty', 'eevee', 'vulpix', 'growlithe', 'ponyta', 'absol', 'mightyena']
F = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 20)
def pal(p):
    L = open(p).read().split('\n'); return [tuple(map(int, L[3 + i].split())) for i in range(int(L[2]))]
def laad(n):
    d = G + n + '/'; f = d + ('anim_front.png' if os.path.exists(d + 'anim_front.png') else 'front.png')
    im = Image.open(f); P = pal(d + 'normal.pal'); a = im.load(); o = Image.new('RGB', (64, 64), (236, 236, 240)); q = o.load()
    for y in range(64):
        for x in range(64):
            if a[x, y]: q[x, y] = P[a[x, y]]
    return o
Z = 8; V = Image.new('RGB', (4 * 64 * Z, 2 * 64 * Z), (236, 236, 240)); d = ImageDraw.Draw(V)
for i, n in enumerate(NAMEN):
    x0, y0 = (i % 4) * 64 * Z, (i // 4) * 64 * Z
    V.paste(laad(n).resize((64 * Z, 64 * Z), Image.NEAREST), (x0, y0))
    for k in range(0, 65, 8):
        d.line([(x0 + k * Z, y0), (x0 + k * Z, y0 + 64 * Z)], fill=(200, 200, 210)); d.line([(x0, y0 + k * Z), (x0 + 64 * Z, y0 + k * Z)], fill=(200, 200, 210))
    d.rectangle([x0, y0, x0 + 64 * Z - 1, y0 + 64 * Z - 1], outline=(120, 120, 140), width=2)
    d.text((x0 + 8, y0 + 6), n, fill=(0, 0, 0), font=F)
V.save(os.path.join(HERE, 'studie_poten.png'))
