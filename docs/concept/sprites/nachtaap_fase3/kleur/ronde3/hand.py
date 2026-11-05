"""Ronde 3 (Claude, 5 nov): healerhand per pixel uitgeschreven. Vorm: Jordi's Sugimori-Drowzee ("deze": open hand, gespreide
vingers als waaier, ronde toppen, duim apart). Opbouw: Gen 3 Mr. Mime (open hand op deze maat: vingers 2 px, scheidingslijn
in middentoon, toppen op verschillende hoogte zodat er lucht tussen zit, zwart alleen aan de schaduwkant, palm licht).
Basis ronde 1s; gloed blijft eromheen (binnenste gloedband vult de ruimte tussen de toppen)."""
import os
import numpy as np
from PIL import Image
H = os.path.dirname(os.path.abspath(__file__))
src = Image.open(os.path.join(H, '../ronde1s/nachtaap_fase3.png')); a = np.array(src); pal = src.getpalette(); oud = a.copy()
C = {'.': 10, 'o': 2, 'k': 1, 'W': 15, 'l': 13, 'm': 14}
X0 = 7
RASTER = {   # x 7..21
 47: "......oo.......",
 48: ".....oWloo.....",
 49: "...oooWloWlo...",
 50: "..oWloWloWlooo.",
 51: "..oWlollolmoWlk",
 52: "..olmolmolmolmk",
 53: "..olmolmolmolmk",
 54: "..ollmllmlmmmmk",
 55: ".oolWWllllmmmmk",
 56: "oWloWllllmmmmmk",
 57: "ollloWllmmmmmok",
 58: ".oommllmmmmmoo.",
}
HANDGLOED = {1, 2, 10, 11, 13, 14, 15}
for y, rij in RASTER.items():
    for i, ch in enumerate(rij):
        x = X0 + i
        if y == 47 and x <= 11: continue                 # kin blijft
        if ch == '.' and a[y, x] not in HANDGLOED: continue
        a[y, x] = C[ch]
im = Image.fromarray(a, 'P'); im.putpalette(pal); im.save(os.path.join(H, 'nachtaap_fase3.png'), transparency=0)
print('gewijzigd t.o.v. 1s:', int((a != oud).sum()))
