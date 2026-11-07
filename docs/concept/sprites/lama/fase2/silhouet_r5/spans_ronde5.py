"""Lama fase 2, silhouet ronde 5: met de hand gezet als spans per rij (x0, x1 inclusief), per zone.
Bron: direct.txt (poppetje ronde 5, pose F 'pas'). Geen automatische vormen: elke rij staat hieronder.
Draaien: python3 spans_ronde5.py -> ronde5.txt + ronde5_1x.png"""
import os
import numpy as np
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__))
R = {}
def put(y, *spans):
    R.setdefault(y, []).extend(spans)

# --- zone 1: kop (oren y1-9, schedel/snuit y10-20) -------------------------------------------
# oren zoals het poppetje: lange banaanoren die in de 3/4-draai van de kop allebei licht naar links hellen;
# nabij oor (links) bijna recht, top iets smaller; ver oor (rechts) met de top naar binnen (banaan). Kwast binnen de oorbreedte.
# (eerste poging: beide als '(' ')' met toppen naar elkaar -> las op 1x als lier/hoorns, verworpen)
for y, s in {1: (17, 18), 2: (16, 18), 3: (16, 18), 4: (16, 19), 5: (16, 19), 6: (16, 19),
             7: (17, 19), 8: (17, 19), 9: (17, 19)}.items(): put(y, s)
for y, s in {1: (21, 22), 2: (21, 23), 3: (22, 24), 4: (22, 25), 5: (22, 25), 6: (22, 25),
             7: (22, 24), 8: (22, 24), 9: (22, 24)}.items(): put(y, s)
# schedel: ronde kruin en rond achterhoofd, stompe ronde snuit naar links-voor, ronde kin (onderlip in de kleur)
for y, s in {10: (16, 24), 11: (15, 25), 12: (14, 25), 13: (13, 26), 14: (12, 26), 15: (11, 26),
             16: (11, 25), 17: (11, 24), 18: (12, 24), 19: (13, 25), 20: (15, 26)}.items(): put(y, s)

# --- zone 2: hals (y21-27): kaarsrecht, één zachte wolboog voor en achter --------------------
for y, s in {21: (16, 26), 22: (16, 27), 23: (15, 27), 24: (15, 27), 25: (15, 27), 26: (15, 27)}.items():
    put(y, s)

# --- zone 3: lijf + staart + aguayo -----------------------------------------------------------
put(26, (30, 38))                                          # aguayo: platte doek, 1 rij boven de rug (geen bult/koffer)
for y, s in {23: (48, 50), 24: (47, 51), 25: (46, 52), 26: (45, 52)}.items(): put(y, s)   # staartpluim
# romp y27-43: links hals/halsband/borstboog, rechts staart/rompboog
LEFT = {27: 15, 28: 14, 29: 14, 30: 14, 31: 15, 32: 15, 33: 14, 34: 13, 35: 13, 36: 12, 37: 12, 38: 12,
        39: 13, 40: 13, 41: 14, 42: 15, 43: 16}
RIGHT = {27: 52, 28: 51, 29: 51, 30: 52, 31: 52, 32: 53, 33: 53, 34: 53, 35: 53, 36: 53, 37: 52, 38: 51,
         39: 51, 40: 52, 41: 52, 42: 53, 43: 53}
for y in LEFT: put(y, (LEFT[y], RIGHT[y]))
# y44: onderkant: voorpoten nog samen (kruis), één buikboog (franje), achterpoten (wolbroek)
put(44, (17, 29), (32, 37), (40, 53)); put(45, (41, 53))   # kruis voorpoten, buikboog, wolbroek achter

# --- zone 4: poten (y45-62), pas in telgang zoals pose F: nabije poten naar voren, verre poten iets naar achteren --
NF = {45: (17, 21), 46: (17, 21), 47: (17, 21), 48: (17, 21), 49: (16, 21), 50: (16, 20), 51: (16, 20),
      52: (16, 20), 53: (15, 19), 54: (15, 19), 55: (15, 19),
      56: (14, 20), 57: (13, 20), 58: (13, 20), 59: (13, 20), 60: (13, 20), 61: (14, 19), 62: (15, 18)}
FF = {45: (24, 29), 46: (24, 29), 47: (25, 29), 48: (25, 29), 49: (25, 29), 50: (26, 30), 51: (26, 30),
      52: (26, 30), 53: (26, 30),
      54: (25, 30), 55: (24, 31), 56: (24, 31), 57: (24, 31), 58: (24, 31), 59: (25, 30), 60: (26, 29)}
NH = {46: (41, 46), 47: (41, 46), 48: (41, 46), 49: (41, 47), 50: (41, 47), 51: (40, 47), 52: (40, 46),
      53: (40, 45), 54: (39, 45), 55: (39, 44), 56: (39, 44), 57: (38, 44), 58: (38, 44),
      59: (37, 44), 60: (37, 44), 61: (38, 43)}
FH = {46: (49, 53), 47: (49, 54), 48: (49, 54), 49: (50, 54), 50: (50, 54), 51: (50, 55), 52: (50, 55),
      53: (51, 55), 54: (51, 55), 55: (51, 55), 56: (51, 55), 57: (49, 54), 58: (49, 54), 59: (50, 53)}
for D in (NF, FF, NH, FH):
    for y, s in D.items(): put(y, s)

S = np.zeros((64, 64), bool)
for y, sp in R.items():
    for a, b in sp: S[y, a:b + 1] = True
if __name__ == '__main__':
    open(os.path.join(HERE, 'ronde5.txt'), 'w').write('\n'.join(''.join('#' if v else '.' for v in r) for r in S) + '\n')
    im = np.zeros((64, 64, 4), np.uint8); im[S] = (0, 0, 0, 255)
    Image.fromarray(im, 'RGBA').save(os.path.join(HERE, 'ronde5_1x.png'))
    ys, xs = np.nonzero(S)
    print('px', S.sum(), 'box', xs.max() - xs.min() + 1, 'x', ys.max() - ys.min() + 1, 'y', ys.min(), ys.max())
