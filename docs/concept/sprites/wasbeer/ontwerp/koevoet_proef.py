"""Proef: zijn koevoetklauwen leesbaar op Gen 3-formaat? Hangende voorpoot (onderarm + hand) met
drie klauwvarianten, 1x en 8x, naast de klauw van Coathief op dezelfde schaal.
Draaien vanuit de repo-root: python3 docs/concept/sprites/wasbeer/ontwerp/koevoet_proef.py"""
import os
from PIL import Image, ImageDraw
HERE = os.path.dirname(os.path.abspath(__file__))
P = {'.': None, 'o': (24, 18, 16), 'd': (52, 44, 44), 'm': (74, 64, 62), 'l': (98, 88, 84),
     'c': (238, 228, 204), 'k': (196, 178, 150), 's': (150, 130, 108)}
# onderarm van boven naar beneden, hand, dan klauwen. c = licht, k = midden, s = schaduw, o = lijn
ARM = """
..oooooo...
.ommmmlo...
.ommmmlo...
.odmmmlo...
.odmmmlo...
.odmmmlo...
.oddmmmlo..
.oddmmmlo..
.odddmmmo..
ooddddmmoo.
""".strip('\n').split('\n')
VARS = {
 'A koevoet (2 klauwen\nnaast elkaar = gespleten\nkop, J-bocht)': """
....ockoco.
....ockoco.
....ockoco.
....ockoco.
....ockoco.
....ockoco.
...ockoco..
..ockoco...
.ocko.o....
.oco.......
..o........
""",
 'B koevoet (1 klauw,\nspleet in de punt)': """
....okco...
....okco...
....okco...
....okco...
....okco...
....okco...
...okco....
..okco.....
.okoko.....
.oco.o.....
..o........
""",
 'C Coathief-klauw\n(ter vergelijking)': """
.ocko.ocko.
.ocko.ocko.
..ocko.ocko
...oko..oko
....oo...oo
""",
}
cells = []
for name, claw in VARS.items():
    rows = ARM + claw.strip('\n').split('\n')
    w = max(len(r) for r in rows)
    im = Image.new('RGBA', (w, len(rows)), (0, 0, 0, 0))
    for y, r in enumerate(rows):
        for x, ch in enumerate(r):
            if P.get(ch):
                im.putpixel((x, y), P[ch] + (255,))
    cells.append((name, im))
W, H = 3 * 150 + 40, 260
sheet = Image.new('RGB', (W, H), (236, 234, 228))
d = ImageDraw.Draw(sheet)
for i, (name, im) in enumerate(cells):
    x0 = 20 + i * 150
    big = im.resize((im.width * 8, im.height * 8), Image.NEAREST)
    sheet.paste(big, (x0, 50), big)
    sheet.paste(im, (x0 + 100, 50), im)
    d.multiline_text((x0, 4), name, fill=(30, 30, 30))
sheet.save(os.path.join(HERE, 'koevoet_proef.png'))
