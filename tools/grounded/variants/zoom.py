# zoom.py uit.png soort:variant [...]  (variant: n=normaal, s=shiny, 1..6) - 4x ingezoomd, om lijnen te controleren
import sys, os
sys.path.insert(0, 'tools/grounded/variants')
from sheet import sprite_with, palettes, ROOT
from PIL import Image
import sheet
sheet.SCALE = 4
out = sys.argv[1]; items = sys.argv[2:]
ims = []
for it in items:
    n, v = it.split(':')
    f = os.path.join(ROOT, 'graphics/pokemon', n)
    pals = palettes(f)
    k = {'n': 0, 's': 1}.get(v)
    pal = pals[k] if k is not None else pals[1 + int(v)]
    ims.append(sprite_with(f, pal))
W = Image.new('RGBA', (260 * len(ims), 260), (200, 200, 190, 255))
for i, im in enumerate(ims):
    W.alpha_composite(im, (i * 260 + 2, 2))
W.save(out)
