#!/usr/bin/env python3
"""vel.py uit.png schaal : finale naast 15 echte fase-1-sprites (Gen 1-3 GBA-origineel, Gen 4+ expansion), op schaal en op 1x."""
import sys, tools as T
from PIL import Image, ImageDraw
sys.path.insert(0, '/home/user/projectgrounded/docs/lessen/vormstudie/tools')
from lib import load
s = int(sys.argv[2])
names = [('FINALE', None), ('ronde23', 'r23'), ('poochyena', 1), ('zigzagoon', 1), ('growlithe', 1), ('eevee', 1), ('vulpix', 1), ('skitty', 1),
         ('meowth', 1), ('sentret', 0), ('shinx', 0), ('purrloin', 0), ('nickit', 0), ('cyndaquil', 1), ('totodile', 1), ('charmander', 1), ('chimchar', 0)]
ims = []
for n, gba in names:
    if n == 'FINALE': im = T.rgba(T.read_png(T.H + '/../anim_front.png', 0))
    elif gba == 'r23': im = T.rgba(T.read_png(T.OL + '/ronde23/anim_front.png', 0))
    else: im = load(n, bool(gba))
    ims.append((n, im))
cols = 6 if s >= 3 else 17
rows = (len(ims) + cols - 1) // cols
W = Image.new('RGB', (cols * 64 * s, rows * (64 * s + 12)), (255, 255, 255)); d = ImageDraw.Draw(W)
for i, (n, im) in enumerate(ims):
    x, y = (i % cols) * 64 * s, (i // cols) * (64 * s + 12)
    bg = Image.new('RGBA', (64, 64), (255, 255, 255, 255)); bg.alpha_composite(im)
    W.paste(bg.resize((64 * s, 64 * s), Image.NEAREST).convert('RGB'), (x, y))
    d.text((x + 2, y + 64 * s), n, fill=(200, 0, 120) if n == 'FINALE' else (0, 0, 0))
W.save(sys.argv[1])
