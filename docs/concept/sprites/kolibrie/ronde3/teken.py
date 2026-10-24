"""Kolibrie ronde 3: met de hand getekend als tekst-raster (pixel voor pixel) op silhouet_v6_groot_1x.png.
Elke rij: lijst van (x, tekens); '.' = niets zetten. Het script zet alleen deze pixels."""
import os
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))

PAL = {  # teken: (index, kleur)
    '.': (0, (152, 208, 160)),   # transparant
    'K': (1, (16, 8, 26)),       # omlijning schaduwkant
    'k': (2, (42, 30, 60)),      # fluweel donker
    'h': (3, (68, 52, 96)),      # fluweel basis
    'H': (4, (118, 116, 176)),   # koel randlicht (selout lichtkant fluweel)
    'v': (5, (80, 46, 118)),     # violet omlijningsbasis
    'w': (6, (100, 58, 146)),    # violet schaduw
    'V': (7, (134, 84, 198)),    # violet basis (verzadiging 0,58)
    'L': (8, (178, 138, 230)),   # violet hooglicht
    'T': (9, (62, 148, 160)),    # blauwgroene glans
    'U': (10, (126, 206, 198)),  # blauwgroene glans licht
    'g': (11, (104, 94, 148)),   # vleugelrand en pennen
    'm': (12, (166, 156, 212)),  # vleugel midden / rand vlammetjes
    'p': (13, (212, 206, 240)),  # bleek lavendel
    'P': (14, (240, 238, 255)),  # zeer bleek
    'W': (15, (255, 255, 255)),  # kern / oogglans
}

R = {
    1: [(38, 'g')],
    2: [(37, 'gPg')],
    3: [(37, 'gPg')],
    4: [(36, 'gPpg')],
    5: [(35, 'gPpg')],
    6: [(34, 'gPmg')],
    7: [(34, 'gpmg')],
    8: [(33, 'gpmg')],
    9: [(32, 'gPpmg')],
    10: [(31, 'gppmg'), (54, 'gggg')],
    11: [(30, 'gpmmg'), (50, 'ggggPgg')],
    12: [(13, 'Pp'), (30, 'gpmmg'), (47, 'gggPPggg')],
    13: [(13, 'pv'), (16, 'P'), (29, 'gmmgK'), (44, 'gggpPPgg')],
    14: [(12, 'Vv'), (15, 'pv'), (28, 'gmgmK'), (42, 'ggppPmgg')],
    15: [(12, 'VvVv'), (19, 'pP'), (27, 'gmgmK'), (39, 'gggppPmmg')],
    16: [(12, 'VKv'), (16, 'vVVv'), (26, 'HhhkkK'), (36, 'gggppPmmmgg')],
    17: [(12, 'vKvVvK'), (25, 'HhhkkK'), (34, 'ggmmmpmmpPg')],
    18: [(12, 'KvvK'), (24, 'HhkkkK'), (31, 'HggmmmggmppPg')],
    19: [(12, 'KkK'), (23, 'HhkkkkK'), (30, 'Hhmmmggmmppgg')],
    20: [(8, 'HHHHhhk'), (22, 'HkkkK'), (27, 'HHHhhgggmmmmmg')],
    21: [(7, 'HhhhhhhhH'), (21, 'HkkK'), (25, 'HHhhhkkmmmmmmmg')],
    22: [(6, 'HhhhhhhhhhHH'), (22, 'kK'), (24, 'Hhhhhhhhhmmmggg')],
    23: [(6, 'Hhhhhhhhhhhh' + 'Hvvvkk' + 'k' + 'hhhhhhhhh' + 'ggmg')],
    24: [(5, 'H' + 'h' * 9 + 'hk' + 'wTUUTwww' + 'khhhhhkkkhkK')],
    25: [(5, 'Hhhhh' + 'KK' + 'hhhk' + 'wVTUUTTTTh' + 'khhhkhhhkK')],
    26: [(4, 'Hhhhhh' + 'WK' + 'hhk' + 'wVLVVVTTThh' + 'khhhhhhkK')],
    27: [(4, 'Hhhhhh' + 'kw' + 'hhk' + 'wVLLVVVVVwww' + 'khhhhkK')],
    28: [(5, 'Hhhhhhhhkw' + 'VLLVVVVVVV' + 'www' + 'khhhkK')],
    29: [(5, 'Hkhhhhhkw' + 'VVLVVVVVVVVV' + 'ww' + 'khhkK')],
    30: [(6, 'Hkhhhkw' + 'VVVLV' + 'V' * 9 + 'ww' + 'kkK')],
    31: [(6, 'khkkkww' + 'V' * 15 + 'ww' + 'kK')],
    32: [(6, 'khKKKkww' + 'V' * 15 + 'ww' + 'K')],
    33: [(5, 'HhK'), (11, 'Kkww' + 'V' * 16 + 'wvvvv')],
    34: [(5, 'HhK'), (13, 'Kkww' + 'V' * 15 + 'LLLL'), (36, 'vvv.........vvvvvv..........')],
    35: [(5, 'HK'), (14, 'Kkww' + 'V' * 18), (36, 'LLVvvv.vvvvvVwLVVVvvv.......')],
    36: [(4, 'HK'), (16, 'Kkwww' + 'V' * 15), (36, 'VVVVwwwVLVVVv.wwwwVLVvv.....')],
    37: [(4, 'HK'), (17, 'Kwwww' + 'V' * 10 + 'wwww'), (36, 'wwwwwwwwwVVKKv....wwwwVv....')],
    38: [(3, 'HK'), (19, 'KKK' + 'wwwVVVVVVVwwww'), (36, 'wwKKKKwwwwVVLK........vVw...')],
    39: [(3, 'HK'), (22, 'KKKK' + 'wwwwwww' + 'KKK'), (36, 'KK....wwKwwVVLK........vVw..')],
    40: [(2, 'HK'), (26, 'KKKKKKK'), (36, '......vVwKKKKvVw.......vVw..')],
    41: [(2, 'HK'), (36, '......vVw.....vVw.......vVw.')],
    42: [(1, 'HK'), (36, '.......vVw.....vVw.......gmg')],
    43: [(36, '........vVw.....vVw......gmg')],
    44: [(36, '........vVw......gmg....gmg.')],
    45: [(36, '.........vVw......gmg....pm.')],
    46: [(36, '..........gmg.....gmg...pm..')],
    47: [(36, '..........gmg....gmg.m.pm...')],
    48: [(36, '..........gmg....pm.mPmm....')],
    49: [(36, '.........mpm.....pm.mPpm....')],
    50: [(36, '.........mpm....pm..mWm.....')],
    51: [(36, '.........mpm....pm...mm.....')],
    52: [(36, '........mpm.m....pm.........')],
    53: [(36, '.......pm..mPm.pm...........')],
    54: [(36, '......pm..mpWPm.............')],
    55: [(36, '......pm..mmmm..............')],
    56: [(36, '..m..pm.....................')],
    57: [(36, '.mPmp.......................')],
    58: [(36, '.mpPm.......................')],
    59: [(36, '.mpPpm......................')],
    60: [(36, '.mPWPm......................')],
    61: [(36, '..mmm.......................')],
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
            assert x0 + len(s) <= 64, (y, x0, len(s))
            if x0 == 36 and y >= 34:
                assert len(s) == 28, (y, len(s))
            for i, ch in enumerate(s):
                if ch != '.':
                    px[x0 + i, y] = PAL[ch][0]
    return im


# Variant "lint" (buiten het silhouet, voor Jordi): zelfde kop, lijf, vleugels en franje;
# de drie slierten als brede linten (4 px: lichtrand, hooglichtstreep, kern, schaduwrand), met de hand getypt.
CLEAR = {33: 47, 34: 47, 35: 47, 36: 50, 37: 50, 38: 50, 39: 51, 40: 42}  # rij: vanaf x leeg (rij >= 41: vanaf 36)
LINT = {
    33: [(49, 'vvvvv')],
    34: [(47, 'vvLLLLLvv')],
    35: [(46, 'vLVwVVVVLvv')],
    36: [(50, 'wwwwVVLv')],
    37: [(54, 'wwVLv')],
    38: [(52, 'm'), (56, 'wVLv')],
    39: [(51, 'mPm'), (57, 'wVLv')],
    40: [(42, 'vLw'), (45, 'KKKK'), (49, 'vLw'), (51, 'mpPm'), (57, 'gmpg')],
    41: [(43, 'vLw'), (49, 'vLw'), (51, 'mWPm'), (57, 'gmpg')],
    42: [(43, 'vLw'), (49, 'vLw'), (51, 'mppm'), (56, 'gmpg')],
    43: [(44, 'vLw'), (49, 'vLw'), (52, 'mpppm')],
    44: [(44, 'vLw'), (50, 'gmg'), (53, 'mmm')],
    45: [(45, 'gmg'), (51, 'gmg')],
    46: [(46, 'gmg'), (52, 'gmpg')],
    47: [(47, 'gmg'), (54, 'mpm')],
    48: [(48, 'gmg'), (55, 'mpm')],
    49: [(49, 'mpm'), (56, 'pm'), (58, 'mm')],
    50: [(50, 'mpm'), (57, 'mPPm')],
    51: [(51, 'mpm'), (57, 'mPWPpm')],
    52: [(52, 'pmm'), (57, 'mppm')],
    53: [(52, 'mPPm'), (58, 'mm')],
    54: [(52, 'mPWPpm')],
    55: [(52, 'mppm')],
    56: [(53, 'mm')],
}


def build_lint():
    im = build()
    px = im.load()
    for y in range(33, 64):
        x0 = CLEAR.get(y, 36 if y >= 41 else 64)
        for x in range(x0, 64):
            px[x, y] = 0
    for y, segs in LINT.items():
        for x0, t in segs:
            for i, ch in enumerate(t):
                if ch != '.':
                    px[x0 + i, y] = PAL[ch][0]
    return im


if __name__ == '__main__':
    build().save(os.path.join(HERE, 'kolibrie.png'), transparency=0)
    build_lint().save(os.path.join(HERE, 'kolibrie_variant_lint.png'), transparency=0)
