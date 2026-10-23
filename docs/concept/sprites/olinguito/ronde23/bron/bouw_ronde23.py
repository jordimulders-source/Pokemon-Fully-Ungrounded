#!/usr/bin/env python3
"""Ronde 23: alleen de verre voorpoot (onder de kin) opnieuw, met Galar-Linoone's verre voorpoot als skelet.
Basis ronde 22. Zone: x8-23 (y39-54) plus x24 op y44-45; frame 2 = dezelfde poot 1 rij hoger (zoals in 22)."""
from PIL import Image
import os
H = os.path.dirname(os.path.abspath(__file__)); R = os.path.join(H, '..', '..')
base = Image.open(os.path.join(R, 'ronde22', 'anim_front.png'))
# Poot in frame-1-coördinaten: rij y -> (x0, tekst). '.' = transparant, ' ' = niet aanraken.
# 1 zwart, 2 donkerbruin (omlijning lichte kant), 3 schaduwvacht, 4 vacht (licht), 9/a/c klauwen (uit ronde 22).
POOT = {
 40: (16, '..233333'),    # x23 wordt vacht: de poot loopt door in de borst, achter de nabije poot (x24)
 41: (16, '.2433333'),
 42: (16, '.2433333'),
 43: (16, '24333333'),    # x23 was lucht: nu achter de nabije poot weggestopt
 44: (16, '24333331'),    # elleboog achteraan (x23)
 45: (15, '24333331'),
 46: (15, '23333321'),
 47: (15, '2333331'),
 48: (15, '.233331'),     # pols, taps
 49: (12, '..99133331'),
 50: (12, '.9aa91331'),
 51: (12, '9a99a1331'),
 52: (12, '9a9a1111'),
 53: (12, '1911'),
 54: (12, '.1'),
}
ZONE = set()
def teken(im, dy):
    px = im.load()
    for y, (x0, s) in POOT.items():
        for i, c in enumerate(s):
            if c == ' ': continue
            x = x0 + i
            ZONE.add((x, y))
            px[x, y + dy] = 0 if c == '.' else int(c, 16)
out = base.copy()
# oude verre poot weghalen in zijn eigen zone (alleen pixels links van de nabije poot)
OUD = {y: range(8, {40:24,41:24,42:24,43:24,44:25,45:26,46:25,47:24,48:23,49:23,50:22,51:22,52:22,53:23,54:24}[y]) for y in range(40, 55)}
px = out.load()
for f in (0, 1):
    dy = 64 * f - f
    for y, xs in OUD.items():
        for x in xs:
            if base.getpixel((x, y + dy)) in (1, 2, 3, 9, 10, 12):
                # alleen de oude verre-poot/klauwpixels; nabije poot en klauwen liggen rechts van deze grens
                px[x, y + dy] = 0; ZONE.add((x, y))
    teken(out, dy)
out.info['transparency'] = 0
out.save(os.path.join(R, 'ronde23', 'anim_front.png'), transparency=0)
open(os.path.join(R, 'ronde23', 'normal.pal'), 'wb').write(open(os.path.join(R, 'ronde22', 'normal.pal'), 'rb').read())
import json; json.dump(sorted(ZONE), open(os.path.join(H, 'zone.json'), 'w'))
