"""Kolibrie ronde 1: met de hand getekend als tekst-raster (pixel voor pixel).
Elke rij: lijst van (x, tekens). Het script zet alleen deze pixels; geen automatische shading.
Silhouet: ../silhouet/silhouet_v6_1x.png (bevroren)."""
import os
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))

PAL = {  # teken: (index, kleur)
    '.': (0, (152, 208, 160)),   # transparant
    'K': (1, (20, 10, 30)),      # omlijning schaduwkant (violetzwart)
    'k': (2, (40, 26, 56)),      # fluweel donker
    'h': (3, (62, 44, 84)),      # fluweel basis
    'H': (4, (94, 74, 124)),     # fluweel hooglicht
    'v': (5, (82, 42, 124)),     # violet omlijningsbasis
    'w': (6, (116, 66, 172)),    # violet schaduw
    'V': (7, (152, 100, 216)),   # violet basis
    'L': (8, (194, 152, 244)),   # violet hooglicht
    't': (9, (30, 112, 132)),    # blauwgroen donker
    'T': (10, (78, 192, 190)),   # blauwgroen licht
    'm': (11, (150, 132, 202)),  # vleugel lila (half doorschijnend)
    'p': (12, (206, 194, 242)),  # bleek lavendel
    'P': (13, (236, 230, 255)),  # zeer bleek (zielelicht)
    'W': (14, (255, 255, 255)),  # gloed
    'o': (15, (228, 132, 72)),   # warm accent (reserve)
}

R = {
    4: [(34, 'w')],
    5: [(33, 'wPw')],
    6: [(33, 'wPw')],
    7: [(32, 'wPw')],
    8: [(31, 'wPpw')],
    9: [(30, 'vPpv')],
    10: [(30, 'vppv')],
    11: [(29, 'vpmv')],
    12: [(28, 'vpmK'), (48, 'wwmm')],
    13: [(27, 'vpmmK'), (44, 'wwwwPPm')],
    14: [(12, 'P'), (15, 'P'), (26, 'vmmwK'), (41, 'vvwPPwww')],
    15: [(12, 'p'), (14, 'pK'), (26, 'vmwK'), (39, 'vvPPmww')],
    16: [(11, 'KhpK'), (25, 'vwwK'), (36, 'vvvPpmvv')],
    17: [(11, 'Khk'), (16, 'kpP'), (24, 'vwwwK'), (33, 'vvvPppmpv')],
    18: [(11, 'KkhkkK'), (23, 'vwVwK'), (31, 'vvmpPpmppv')],
    19: [(11, 'KkkK'), (22, 'vwVwK'), (28, 'vvvmmppmPpvv')],
    20: [(11, 'KkK'), (21, 'vwwwK'), (26, 'vvTtwmpmpppv')],
    21: [(8, 'kkkkkK'), (20, 'vwwwv'), (25, 'vTtwwmwppmpv')],
    22: [(7, 'kHwVhhkK'), (19, 'vwww'), (23, 'vTtwwwwmmpmpK')],
    23: [(6, 'kHHwVwhhkKKK'), (21, 'vTtwwwwwwwmmpK')],
    24: [(6, 'kHhhhhhhhhkkvvvv'), (22, 'vTtwwwwwwmmK')],
    25: [(5, 'kHhhKKhhhhkwVLLVVw'), (23, 'vtwwwwwwmK')],
    26: [(4, 'KHhhhWKhhhhkwVLLVVw'), (23, 'vtwwwvwwK')],
    27: [(4, 'KhhhhwkhhhkkwVLVVVVw'), (24, 'vwwwwwK')],
    28: [(5, 'KkhhhhhhhkwVVVVVVVVw'), (25, 'vwwwK')],
    29: [(5, 'KkhhhhhhkwVVVVVVVVVw'), (25, 'vwwwK')],
    30: [(6, 'KkhhhhkkwVVVVVVVVVVw'), (26, 'vwK')],
    31: [(6, 'hkKKkkkkwVLLVVVVVVwww'), (27, 'vK')],
    32: [(5, 'hkK'), (10, 'KkkkwVLLLVVVVVVVwwKv')],
    33: [(5, 'hK'), (11, 'KkkkwVVLLVVVVVVVVVwvvvv')],
    34: [(4, 'hkK'), (12, 'KkkkwVVVVVVVVVVVVVLLLLvvv'), (40, 'vvvvvvvvvv')],
    35: [(4, 'hK'), (14, 'KkkwwVVVVVVVVVVVVLLVVVwvvvwVwwK'), (48, 'KKvv')],
    36: [(3, 'hkK'), (15, 'KkwwwwwwVVVVVVVVVwwwwwwwVwwwK'), (51, 'Kvv')],
    37: [(3, 'hK'), (17, 'KKKKKwwwwwwwwwwwwKKKwwvwwwK'), (52, 'Kvv')],
    38: [(2, 'hK'), (22, 'KKKKKKKKKKKK'), (37, 'wwwvwwwwK'), (54, 'v')],
    39: [(2, 'hK'), (38, 'KKvKwvwvK'), (54, 'Kv')],
    40: [(2, 'K'), (39, 'vK'), (46, 'vK'), (55, 'v')],
    41: [(1, 'KK'), (40, 'vK'), (47, 'vK'), (55, 'v')],
    42: [(40, 'vK'), (47, 'vK'), (55, 'Kv')],
    43: [(41, 'vK'), (48, 'vK'), (55, 'Kv')],
    44: [(41, 'vK'), (49, 'v'), (54, 'Kv')],
    45: [(41, 'vK'), (49, 'vK'), (52, 'KKK')],
    46: [(41, 'vK'), (49, 'vKPm')],
    47: [(41, 'vK'), (48, 'vKWp')],
    48: [(41, 'vK'), (47, 'vKPp')],
    49: [(41, 'vK'), (47, 'vKpm')],
    50: [(39, 'vvKK'), (45, 'pmvK')],
    51: [(38, 'vvKKmpPWpK')],
    52: [(38, 'vKKpm')],
    53: [(35, 'mppKkK')],
    54: [(34, 'mPWp')],
    55: [(34, 'mpPm')],
    56: [(34, 'mpm')],
    57: [(35, 'm')],
}


def build():
    im = Image.new('P', (64, 64), 0)
    pal = [0] * 768
    for ch, (i, c) in PAL.items():
        pal[i * 3:i * 3 + 3] = c
    im.putpalette(pal)
    px = im.load()
    for y, segs in R.items():
        for x0, s in segs:
            for i, ch in enumerate(s):
                if ch != ' ':
                    px[x0 + i, y] = PAL[ch][0]
    return im


if __name__ == '__main__':
    im = build()
    im.save(os.path.join(HERE, 'kolibrie.png'), transparency=0)
