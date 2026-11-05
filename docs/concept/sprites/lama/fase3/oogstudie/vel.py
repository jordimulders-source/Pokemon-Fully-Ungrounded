"""Oogstudie fase 3 (5 nov). Jordi: "ik ben nog niet tevreden met het oog, het is nu gewoon bijna een zwarte vlek, niet typisch
lui oid, kijk nogmaals naar slakoth, slaking etc". Gen 3-sprites op 3x + uitsnede rond het oog op 12x.
Draaien vanuit de repo-root: python3 docs/concept/sprites/lama/fase3/oogstudie/vel.py"""
import os
import numpy as np
from PIL import Image, ImageDraw, ImageFont
HERE = os.path.dirname(os.path.abspath(__file__))
G = os.path.join(HERE, '../../../../../../graphics/pokemon')
F = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 12)
def frame(n):
    p = Image.open(os.path.join(G, n, 'anim_front.png'))
    p = p if p.mode == 'P' else p.convert('P')
    a = np.array(p)[:64, :64]; rgb = np.array(p.convert('RGB'))[:64, :64]; rgb[a == 0] = 255
    return Image.fromarray(rgb)
# (naam, oog-uitsnede x0,y0,x1,y1) - uitsneden met de hand gezocht rond het oog
NAMEN = ['slakoth', 'vigoroth', 'slaking', 'numel', 'camerupt', 'snorlax', 'girafarig', 'lama3']
im = Image.new('RGB', (12 + 210 * 4, 30 + 2 * (200 + 220)), 'white'); d = ImageDraw.Draw(im)
d.text((12, 8), 'Oogstudie: luie/droge ogen in Gen 3 (boven 3x, onder het oog 12x)', font=F, fill=(30, 30, 30))
for i, n in enumerate(NAMEN):
    if n == 'lama3':
        f = Image.open(os.path.join(HERE, '../kleur/ronde4b/lama3.png')).convert('RGBA'); bg = Image.new('RGBA', f.size, 'white'); bg.alpha_composite(f); f = bg.convert('RGB')
    else:
        f = frame(n)
    x = 12 + 210 * (i % 4); y = 30 + (i // 4) * 420
    im.paste(f.resize((192, 192), Image.NEAREST), (x, y)); d.text((x, y + 194), n, font=F, fill=(60, 60, 60))
    f.save(os.path.join(HERE, f'{n}.png'))
im.save(os.path.join(HERE, 'overzicht.png'))
