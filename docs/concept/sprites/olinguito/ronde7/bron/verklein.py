"""Stap 1 pixel-over: modeltekening uitsnijden en verkleinen (NEAREST, 'jagged' zoals de gids zegt),
dan per pixel de dichtstbijzijnde vlakke kleur van de modeltekening als letter. Alleen referentie."""
import sys
from PIL import Image
src, box, h, out = sys.argv[1], tuple(map(int, sys.argv[2].split(','))), int(sys.argv[3]), sys.argv[4]
cols = eval(sys.argv[5])  # {'letter': (r,g,b)}
im = Image.open(src).convert('RGB').crop(box)
w = round(im.width * h / im.height)
sm = im.resize((w, h), Image.BOX)
lines = []
for y in range(h):
    row = ''
    for x in range(w):
        p = sm.getpixel((x, y))
        best = min(cols, key=lambda k: sum((a - b) ** 2 for a, b in zip(cols[k], p)))
        row += best
    lines.append(row)
open(out, 'w').write('\n'.join(lines) + '\n')
print(w, h)
print('\n'.join('%2d %s' % (i, l) for i, l in enumerate(lines)))
