"""vergelijk10.py <soortmap> : compare.png met ronde 9 en ronde 10 (frame 1 en 2), 1x en 3x."""
import sys, os
from PIL import Image, ImageDraw
d = sys.argv[1]
items = []
for r in ('ronde9', 'ronde10'):
    for f in (0, 1):
        items.append(('%s f%d' % (r.replace('ronde', 'ronde '), f + 1), os.path.join(d, r, 'anim_front.png'), f))
BG = (232, 232, 224)
W = 64 * 3 + 12
cv = Image.new('RGB', (W * len(items), 64 + 64 * 3 + 24), BG)
dr = ImageDraw.Draw(cv)
for i, (n, p, f) in enumerate(items):
    idx = Image.open(p).crop((0, 64 * f, 64, 64 * f + 64))
    im = idx.convert('RGB')
    px, ip = im.load(), idx.load()
    for y in range(64):
        for x in range(64):
            if ip[x, y] == 0:
                px[x, y] = BG
    x0 = i * W
    cv.paste(im, (x0 + 70, 2))
    cv.paste(im.resize((192, 192), Image.NEAREST), (x0 + 6, 68))
    dr.text((x0 + 8, 262), n, fill=(40, 40, 40))
cv.save(os.path.join(d, 'ronde10/compare.png'))
