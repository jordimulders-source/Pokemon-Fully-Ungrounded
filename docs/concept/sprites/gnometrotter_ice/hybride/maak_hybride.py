"""Gnometrotter Ice hybride: basis r3 (zelfde pose) + lijfmateriaal van r1.
Draai: python3 maak_hybride.py  (vanuit deze map)"""
import sys, os
import numpy as np
from PIL import Image
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from knip import *

BASIS = '../r3/gemini_r3_lijf.png'
DONOR = '../r1/gemini_r1.png'

# naam, klasse, kader basis, kader donor, spiegel
# naam, klasse, kader basis, kader donor, spiegel, [kaart-kader donor]
# Het kaart-kader (optioneel) is het donorstuk dat op het basisonderdeel
# geschaald wordt, als het donoronderdeel deels achter de baard zit.
DELEN = [
    ('voorhand',   'roze',  (274, 274, 356, 338), (272, 266, 340, 342), False),
    ('voorarm',    'roze',  (352, 282, 400, 320), (336, 268, 402, 336), False),
    ('achterhand', 'roze',  (672, 300, 754, 374), (666, 298, 748, 388), False),
    ('elleboog',   'roze',  (658, 244, 708, 302), (638, 248, 708, 320), False),
    ('schouder',   'roze',  (560, 204, 672, 280), (582, 220, 662, 292), False),
    ('nek',        'roze',  [(488, 176), (545, 176), (545, 212), (540, 220), (530, 232), (512, 241), (488, 251)],
                            [(530, 200), (640, 200), (640, 300), (530, 300)], False,
                            (548, 228, 610, 280)),
    ('romp',       'roze',  [(452, 262), (486, 252), (512, 241), (530, 232), (540, 220), (545, 212), (545, 176), (640, 176), (665, 210), (665, 270), (690, 300), (690, 345), (452, 345)],
                            [(440, 190), (590, 190), (590, 240), (650, 300), (650, 360), (440, 360)], False,
                            (508, 228, 630, 336)),
    ('voet_links', 'blauw', (378, 441, 505, 490), (385, 446, 515, 488), False),
    ('been_links', 'blauw', [(392, 377), (500, 385), (540, 380), (540, 441), (392, 441)],
                            [(400, 386), (500, 392), (552, 388), (552, 446), (400, 446)], False),
    ('voet_rechts','blauw', (570, 451, 675, 494), (585, 457, 700, 496), False),
    ('been_rechts','blauw', [(540, 380), (600, 364), (650, 352), (680, 352), (680, 451), (540, 451)],
                            [(552, 388), (600, 375), (640, 352), (700, 345), (700, 457), (552, 457)], False),
]


def donkerrand(basis, m, dikte=3):
    """Donkere basispixels die tegen de buitenkant van het masker liggen
    (de omlijning van het basisonderdeel) blijven van de basis."""
    from scipy import ndimage as ndi
    lum = basis.mean(axis=-1)
    donker = lum < 95
    buiten = ndi.binary_dilation(~m, iterations=dikte)
    return donker & buiten


def main(debug=True):
    b = laad(BASIS)
    d = laad(DONOR)
    uit = b.copy()
    mbs = basismaskers(b, DELEN)
    mb_all, md_all = [], []
    for (naam, cls, kb, kd, sp, *kaart), mb in zip(DELEN, mbs):
        md = zonder_omlijning(d, deelmasker(d, cls, kd, sluit=3))
        # alleen echte onderdeelkleur en donkere naden; geen grijze vreemde pixels
        md &= klasse(d, cls, True) | (d.mean(axis=-1) < 110)
        nood = plak(uit, mb, d, md, spiegel=sp, kader_b=bbox(mb),
                    kader_d=kaart[0] if kaart else bbox(md))
        mb_all.append(mb); md_all.append(md)
        print(f'{naam:12s} basis {tuple(map(int, bbox(mb)))} ({mb.sum()} px)  '
              f'donor {tuple(map(int, bbox(md)))} ({md.sum()} px)  noodvulling {nood:.1%}')
    # bewaker: waar het silhouet toch zou veranderen (lichte randpixels), de basis terug
    x = omtrek(b) ^ omtrek(uit)
    print('silhouetbewaker zet basis terug op', int(x.sum()), 'px')
    uit[x] = b[x]
    Image.fromarray(uit.astype(np.uint8)).save('model_hybride.png')
    if debug:
        debug_maskers(b, mb_all, 'debug_maskers_basis.png')
        debug_maskers(d, md_all, 'debug_maskers_donor.png')
    ob, oh = omtrek(b), omtrek(uit)
    print('omtrekverschil silhouet (xor):', int((ob ^ oh).sum()))
    print('verschil niet-witte pixels (xor, incl. binnenglim):', int((nietwit(b) ^ nietwit(uit)).sum()))
    vergelijk([BASIS, 'model_hybride.png', DONOR], 'vergelijk.png')


if __name__ == '__main__':
    main()
