"""Kolibrie ronde 2: met de hand getekend als tekst-raster (pixel voor pixel) op silhouet_v6_groot_1x.png.
Elke rij: lijst van (x, tekens). Het script zet alleen deze pixels; geen automatische shading."""
import os
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))

PAL = {  # teken: (index, kleur)
    '.': (0, (152, 208, 160)),   # transparant
    'K': (1, (18, 8, 28)),       # omlijning schaduwkant (violetzwart)
    'k': (2, (40, 26, 56)),      # fluweel donker / omlijningsbasis fluweel
    'h': (3, (64, 46, 88)),      # fluweel basis
    'H': (4, (100, 80, 132)),    # fluweel hooglicht
    'v': (5, (72, 16, 112)),     # lijf violet omlijningsbasis
    'w': (6, (106, 30, 166)),    # lijf violet schaduw
    'V': (7, (142, 54, 214)),    # lijf violet basis (diep, verzadigd)
    'L': (8, (186, 116, 246)),   # lijf violet hooglicht
    't': (9, (20, 96, 118)),     # blauwgroen donker
    'T': (10, (52, 166, 172)),   # blauwgroen basis
    'U': (11, (140, 228, 212)),  # blauwgroen hooglicht
    'm': (12, (140, 128, 184)),  # vleugel lila-grijs (halfdoorschijnend)
    'p': (13, (206, 198, 238)),  # bleek lavendel
    'P': (14, (240, 236, 255)),  # zeer bleek (zielelicht)
    'W': (15, (255, 255, 255)),  # kernpixel / oogglans
}

R = {
    1: [(38, 'm')],
    2: [(37, 'mPm')],
    3: [(37, 'mPm')],
    4: [(36, 'mPPm')],
    5: [(35, 'mPph')],
    6: [(34, 'hPph')],
    7: [(34, 'hPph')],
    8: [(33, 'hPph')],
    9: [(32, 'hPpph')],
    10: [(31, 'hppmh'), (54, 'mmmm')],
    11: [(30, 'hpmph'), (50, 'mmmmPPm')],
    12: [(13, 'Pp'), (30, 'hmpmh'), (47, 'mmPPmmmm')],
    13: [(13, 'pv'), (16, 'P'), (29, 'hmmmh'), (44, 'mmmmPPmm')],
    14: [(12, 'Vv'), (15, 'pv'), (28, 'hmhmK'), (42, 'hhmmPPmm')],
    15: [(12, 'VvVv'), (19, 'pP'), (27, 'hmhhK'), (39, 'hhhmmpPPm')],
    16: [(12, 'Vvv'), (16, 'vVVv'), (26, 'kkhhkK'), (36, 'hhhpmmppmhm')],
    17: [(12, 'vVvVvK'), (25, 'khhkkK'), (34, 'hhmmhhppmph')],
    18: [(12, 'KvvK'), (24, 'khhkkK'), (31, 'hhhmhhhmmhhph')],
    19: [(12, 'KkK'), (23, 'kkhkkkK'), (30, 'kmmhhmmmhhmhh')],
    20: [(8, 'kkkkhhK'), (22, 'khkkK'), (27, 'kkkHhhmmmhhmmh')],
    21: [(7, 'kHHwVwhhK'), (21, 'khkK'), (25, 'kkHHhhhhhhmmmmh')],
    22: [(6, 'kHHhwwhhhhKK'), (22, 'kK'), (24, 'kHHhhhhhhhhhmmh')],
    23: [(6, 'kHhhhhhhhhkhtttttk'), (24, 'kHhhhhhhhhhhkK')],
    24: [(5, 'kHhhhhhhhhkktTUUTTtt'), (25, 'kHhhhhhhhhkK')],
    25: [(5, 'kHhhhKKhhhk'), (16, 'tTUUTTTTtt'), (26, 'khhhhhhhkK')],
    26: [(4, 'kHhhhhWKhhhk'), (16, 'tTTTTTTTTt'), (26, 'khhhhhhkK')],
    27: [(4, 'khhhhhwkhhkk'), (16, 'tTTTTTTtttt'), (27, 'khhhhkK')],
    28: [(5, 'khhhhhhhhkk'), (16, 'tTTTttVVVwww'), (28, 'khhhkK')],
    29: [(5, 'kkhhhhhhkk'), (15, 'wVtttVLVVVVww'), (28, 'khhkK')],
    30: [(6, 'kkhhhhkk'), (14, 'wVLLVVVVVVVVVww'), (29, 'kkK')],
    31: [(6, 'khkkkkkk'), (14, 'wVLVVVVVVVVVVVVw'), (30, 'kK')],
    32: [(6, 'khKKKkkkk'), (15, 'wVVVLLVVVVVVVVww'), (31, 'K')],
    33: [(5, 'hkK'), (11, 'KkkkkwVVVLLVVVVVVVVVwvvvv')],
    34: [(5, 'hkK'), (13, 'KkkkwVVVVVVVVVVVVVVLLLL'), (36, 'vvv........vvvvvvv..........')],
    35: [(5, 'hK'), (14, 'KkkwwVVVVVVVVVVVVVVVVL'), (36, 'LLVvvv.vvvvVVVLVVVvvv.......')],
    36: [(4, 'hK'), (16, 'Kkwww' + 'V' * 15), (36, 'VVVVwwVwwwwwKKKKKKVVvvv.....')],
    37: [(4, 'hK'), (17, 'KKwwwwwVVVVVVVVwwww'), (36, 'wwwwwwwwVwwwwK....KKKVvv....')],
    38: [(3, 'hK'), (19, 'KK' + 'w' * 15), (36, 'wwwwwwwwwwVwwK.......KKVv...')],
    39: [(3, 'hK'), (22, 'K' * 14), (36, 'KKKKKKwwwwwwVwK........KVv..')],
    40: [(2, 'hK'), (36, '......KVvKKKKKVv.......KVv..')],
    41: [(2, 'hK'), (36, '......KVv.....KVv.......KVv.')],
    42: [(1, 'KK'), (36, '.......KVv.....KVv......KVv.')],
    43: [(36, '........KVv.....KVv.....KVv.')],
    44: [(36, '........KVv......KVv....KVv.')],
    45: [(36, '.........KVv......KVv...KVv.')],
    46: [(36, '.........KVv......KVv..KVv..')],
    47: [(36, '.........KVv......KVv.KVv...')],
    48: [(36, '.........KVv.....KVKmmpm....')],
    49: [(36, '.........KVv....KVKmpPm.....')],
    50: [(36, '.........KVv....KVKmPWm.....')],
    51: [(36, '.........KVv....KVKwpw......')],
    52: [(36, '........KVv.mmm.KVvw........')],
    53: [(36, '.......KVv.mpPpmVv..........')],
    54: [(36, '......KVv.mpPWpmK...........')],
    55: [(36, '......KVv.wwww..............')],
    56: [(36, '...mmmKVv...................')],
    57: [(36, '..mpPpV.....................')],
    58: [(36, '.mPWPm......................')],
    59: [(36, '.mpPpw......................')],
    60: [(36, '..www.......................')],
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
            assert x0 + len(s) <= 64, (y, x0, s)
            for i, ch in enumerate(s):
                if ch != '.':
                    px[x0 + i, y] = PAL[ch][0]
    return im


if __name__ == '__main__':
    build().save(os.path.join(HERE, 'kolibrie.png'), transparency=0)
