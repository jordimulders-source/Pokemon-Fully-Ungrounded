"""Maakt schetsen.png (uit schetsen.txt) en compare.png (alpaca naast 5 echte Gen 3-sprites, 1x en 3x).
Gebruik: python3 vergelijk.py <repo-root>
"""
import sys, os
from PIL import Image, ImageDraw

root = sys.argv[1]
r8 = os.path.join(root, 'docs/concept/sprites/alpaca/ronde8')
BG = (152, 208, 160, 255)

# schetsen
kleur = {'w': (240, 230, 206), 'f': (222, 164, 106), 'g': (222, 92, 70), 'o': (40, 32, 40), 'k': (120, 72, 50)}
blokken, cur = [], None
for regel in open(os.path.join(r8, 'bron/schetsen.txt'), encoding='utf-8'):
    regel = regel.rstrip('\n')
    if regel.startswith('#'):
        if regel[1:2] in 'ABC' or regel.startswith('# A'):
            cur = []
            blokken.append(cur)
        continue
    if cur is not None and regel:
        cur.append(regel)
S = 6
sch = Image.new('RGBA', (len(blokken) * 34 * S, 34 * S), BG)
d = ImageDraw.Draw(sch)
for i, b in enumerate(blokken):
    for y, rij in enumerate(b):
        for x, c in enumerate(rij):
            if c in kleur:
                d.rectangle([i * 34 * S + x * S, S + y * S, i * 34 * S + x * S + S - 1, S + y * S + S - 1], fill=kleur[c])
    d.text((i * 34 * S + 4, 4), 'ABC'[i], fill=(0, 0, 0))
sch.save(os.path.join(r8, 'schetsen.png'))

# vergelijking
namen = ['mareep', 'eevee', 'torchic', 'cyndaquil', 'skitty']
ims = [Image.open(os.path.join(r8, 'anim_front.png')).convert('RGBA').crop((0, 0, 64, 64))]
for n in namen:
    ims.append(Image.open(os.path.join(root, 'graphics/pokemon', n, 'anim_front_gba.png')).convert('RGBA').crop((0, 0, 64, 64)))
out = Image.new('RGBA', (len(ims) * 192, 64 + 192 + 8), BG)
for i, im in enumerate(ims):
    out.paste(im, (i * 192 + 64, 0), im)
    big = im.resize((192, 192), Image.NEAREST)
    out.paste(big, (i * 192, 72), big)
out.save(os.path.join(r8, 'compare.png'))
