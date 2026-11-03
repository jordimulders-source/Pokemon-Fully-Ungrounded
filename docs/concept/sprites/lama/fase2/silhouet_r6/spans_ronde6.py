"""Silhouet lama fase 2, ronde 6: het hele silhouet overgetrokken van het goedgekeurde poppetje (fase2_r4('F_pas', head_yaw=55),
camera bron.py) op de 50%-dekkingsgrens (dekkingskaart: ../silhouet_r5/kop_dekking.py -> kop_alpha.npy).
Kop y0-21 letterlijk uit ronde 5f. Rijen 22-63 met de hand per rij op de 50%-grens gezet; afwijkingen (alleen korrels, max 1 px)
staan als commentaar bij de rij. Draaien: python3 spans_ronde6.py  ->  ronde6.txt, ronde6_1x.png"""
import os
import numpy as np
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__))
SPANS = {
    # --- kop (ronde 5f, letterlijk) ---
    1: [(21, 22)],
    2: [(17, 18), (21, 23)],
    3: [(17, 18), (22, 23)],
    4: [(16, 18), (22, 24)],
    5: [(16, 18), (22, 24)],
    6: [(16, 18), (22, 24)],
    7: [(17, 18), (22, 24)],
    8: [(17, 18), (22, 24)],
    9: [(17, 19), (22, 23)],
    10: [(17, 23)],
    11: [(16, 23)],
    12: [(15, 24)],
    13: [(14, 25)],
    14: [(13, 25)],
    15: [(12, 25)],
    16: [(12, 24)],
    17: [(13, 24)],
    18: [(13, 24)],
    19: [(14, 24)],
    20: [(16, 24)],
    21: [(16, 25)],
    # --- hals ---
    22: [(16, 25)],
    23: [(16, 25)],
    24: [(16, 25), (47, 50)],                      # staartpluim begint
    25: [(16, 25), (29, 37), (43, 50)],            # x46 (40%) gevuld: inkeping tussen rug en staart
    26: [(16, 25), (28, 51)],                      # x39 (40%) gevuld: inkeping in de aguayo-rand
    # --- lijf ---
    27: [(16, 51)],
    28: [(15, 51)],
    29: [(14, 51)],
    30: [(14, 50)],
    31: [(14, 50)],
    32: [(14, 50)],
    33: [(14, 50)],
    34: [(14, 50)],
    35: [(14, 50)],
    36: [(14, 50)],
    37: [(14, 50)],
    38: [(13, 50)],
    39: [(13, 50)],
    40: [(13, 49)],
    41: [(14, 48)],
    42: [(15, 34), (37, 47)],
    43: [(19, 27), (30, 33), (41, 47)],            # x38-39 (50%) weg: los stukje met 1-px inkeping x40
    # --- poten: voorpoten (nabij 18-22, ver 24-27), achterpoten samen 42-49 zoals het model ---
    44: [(19, 27), (42, 47)],
    45: [(19, 27), (42, 48)],
    46: [(19, 27), (43, 48)],
    47: [(18, 27), (43, 48)],
    48: [(18, 27), (44, 48)],                      # x23 (30%) gevuld: 1-px inkeping, opening begint op y49
    49: [(18, 21), (24, 27), (44, 48)],
    50: [(18, 21), (24, 27), (44, 48)],
    51: [(18, 21), (24, 27), (44, 48)],
    52: [(17, 21), (24, 27), (44, 49)],
    53: [(17, 20), (24, 27), (44, 49)],
    54: [(17, 20), (24, 27), (44, 49)],
    55: [(17, 20), (24, 28), (44, 49)],
    56: [(16, 20), (24, 28), (44, 49)],
    57: [(15, 20), (23, 28), (44, 49)],
    58: [(15, 20), (23, 29), (44, 49)],            # x22 (70%) weg: 1-px inkeping x21
    59: [(14, 29), (44, 48)],
    60: [(14, 28), (44, 47)],                      # x43 (50%) weg: uitsteeksel
    61: [(14, 20), (24, 27), (44, 46)],            # x13 (70%) weg: uitsteeksel; x44 en x46 (40%) erbij: hoef i.p.v. 1 px
    62: [(14, 19)],
}
S = np.zeros((64, 64), bool)
for y, sp in SPANS.items():
    for a, b in sp: S[y, a:b + 1] = True
open(os.path.join(HERE, 'ronde6.txt'), 'w').write('\n'.join(''.join('#' if v else '.' for v in r) for r in S) + '\n')
img = Image.new('P', (64, 64), 0); img.putpalette([255, 255, 255, 0, 0, 0] + [0] * 762)
img.putdata([1 if v else 0 for v in S.flatten()]); img.save(os.path.join(HERE, 'ronde6_1x.png'), transparency=0)
print(int(S.sum()), 'px')
