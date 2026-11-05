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
# Jordi: "wel wat beter, maar de vingers zijn wel erg recht" + "en de tint mag meer zilver, lijkt nog steeds een handschoen"
# -> vingers als waaier, per pixel uitgeschreven; lijnen tussen de vingers in middengrijs zilver (s = index 14, zoals Mr. Mime),
#    alleen de buitenomlijning donker; palet 13/14 koeler zilver (zie onder).
C2 = {'.': 10, 'o': 2, 'k': 1, 'W': 15, 'l': 13, 's': 14}
WAAIER = {   # x 7..21 ; rij 47 x7-11 = kin (blijft)
 47: "......oo.......",
 48: ".....oWlo..oo..",
 49: "..oo.olso.oWlo.",
 50: ".oWlo.lso.olso.",
 51: ".olsoolssolsooo",
 52: "..olssllsslsoWk",
 53: "..ollsllslsslsk",
}
for y, rij in WAAIER.items():
    for i, ch in enumerate(rij):
        x = 7 + i
        if y == 47 and x <= 11: continue
        if ch == '.' and a[y, x] not in HANDGLOED: continue
        a[y, x] = C2[ch]
# zilver (Jordi: "de tint mag meer zilver"): koeler, minder lila; 14 = middengrijs voor de vingerlijnen/palmschaduw
ZILVER = {13: (222, 226, 236), 14: (146, 154, 174)}
for i, rgb in ZILVER.items(): pal[i * 3:i * 3 + 3] = list(rgb)
im = Image.fromarray(a, 'P'); im.putpalette(pal); im.save(os.path.join(H, 'nachtaap_fase3.png'), transparency=0)
print('gewijzigd t.o.v. 1s:', int((a != oud).sum()))
