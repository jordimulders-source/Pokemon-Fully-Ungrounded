"""Maakt de sprites voor de act-kaart van The Spire (graphics/grounded/spire/*.png, 32x32, eigen palet).
Gebruikt dezelfde bronnen als de goedgekeurde mockup (mockups.py, versie 4)."""
import os, sys
from PIL import Image, ImageDraw
sys.argv = [sys.argv[0], '/tmp']
import mockups as M

OUT = os.path.join(M.ROOT, 'graphics/grounded/spire')
os.makedirs(OUT, exist_ok=True)


def save_indexed(im, name):
    """RGBA → 16-kleuren-PNG, index 0 = transparant."""
    canvas = Image.new('RGBA', (32, 32), (0, 0, 0, 0))
    canvas.paste(im, ((32 - im.width) // 2, (32 - im.height) // 2), im)
    # halfdoorzichtige gloed (aura) wordt een lichte, dekkende rand
    px = canvas.load()
    for y in range(32):
        for x in range(32):
            r, g, b, a = px[x, y]
            if 24 <= a < 128:
                px[x, y] = ((r + 255) // 2, (g + 255) // 2, (b + 200) // 2, 255)
    colors = []
    for px in canvas.get_flattened_data() if hasattr(canvas, 'get_flattened_data') else canvas.getdata():
        if px[3] >= 128 and px[:3] not in colors:
            colors.append(px[:3])
    if len(colors) > 15:
        q = canvas.convert('RGB').quantize(15)
        pal = q.getpalette()[:45]
        colors = [tuple(pal[i:i + 3]) for i in range(0, 45, 3)]
    out = Image.new('P', (32, 32), 0)
    pal = [(255, 0, 255)] + colors + [(0, 0, 0)] * (15 - len(colors))
    out.putpalette([c for rgb in pal for c in rgb])
    for y in range(32):
        for x in range(32):
            px = canvas.getpixel((x, y))
            if px[3] < 128:
                continue
            best = min(range(1, len(colors) + 1), key=lambda i: sum((a - b) ** 2 for a, b in zip(pal[i], px[:3])))
            out.putpixel((x, y), best)
    out.save(os.path.join(OUT, name + '.png'))
    print(name, len(colors), 'kleuren')


icons = M.node_icons3()
for kind in ('fight', 'elite', 'rest', 'shop', 'event'):
    save_indexed(icons[kind], 'node_' + kind)

# cursor: rode hoekhaken (Town Map-cursor), 24x24 binnen 32x32
cur = Image.new('RGBA', (24, 24), (0, 0, 0, 0))
d = ImageDraw.Draw(cur)
for (ox, oy, sx, sy) in ((0, 0, 1, 1), (23, 0, -1, 1), (0, 23, 1, -1), (23, 23, -1, -1)):
    for t in range(2):
        d.line((ox, oy + t * sy, ox + 5 * sx, oy + t * sy), fill=(248, 72, 40, 255))
        d.line((ox + t * sx, oy, ox + t * sx, oy + 5 * sy), fill=(248, 72, 40, 255))
save_indexed(cur, 'cursor')
