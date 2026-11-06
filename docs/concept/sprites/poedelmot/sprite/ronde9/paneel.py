"""Ronde 9: paneel.png = schets over ronde 8, schets over ronde 9, ronde 9 los (alle drie 8x, onderkant y30-62 vergroot
in het tweede vak hieronder op 16x)."""
import os
from PIL import Image, ImageDraw, ImageFont
from overlay import over
HERE = os.path.dirname(os.path.abspath(__file__))
F = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 16)
r8 = os.path.join(HERE, '../ronde8/anim_front.png'); r9 = os.path.join(HERE, 'anim_front.png')
los = Image.open(r9).crop((0, 0, 64, 64)).convert('RGB').resize((512, 512), Image.NEAREST)
items = [('schets over ronde 8 (8x)', over(r8)), ('schets over ronde 9 (8x)', over(r9)), ('ronde 9 los (8x)', los)]
onder = [('16x onderkant: schets over ronde 9', over(r9, 16).crop((0, 36 * 16, 52 * 16, 61 * 16))),
         ('16x onderkant: ronde 9 los', Image.open(r9).crop((0, 36, 52, 61)).convert('RGB').resize((52 * 16, 25 * 16), Image.NEAREST))]
W = max(sum(i.width + 10 for _, i in items), sum(i.width + 10 for _, i in onder)) + 10
H = 512 + 30 + 400 + 40
P = Image.new('RGB', (W, H), (236, 236, 240)); d = ImageDraw.Draw(P); x = 10
for t, i in items: d.text((x, 6), t, fill=(0, 0, 0), font=F); P.paste(i, (x, 28)); x += i.width + 10
x = 10
for t, i in onder: d.text((x, 548), t, fill=(0, 0, 0), font=F); P.paste(i, (x, 570)); x += i.width + 10
P.save(os.path.join(HERE, 'paneel.png'))
