"""Gnometrotter Grass hybride: basis r4 (zelfde pose) + lijfmateriaal van r1
(handen gewisseld). Alleen knippen, schalen, spiegelen en plakken binnen de
maskers van de basis; niets getekend. Draai: python3 maak_hybride.py"""
import sys, os
import numpy as np
from PIL import Image
os.chdir(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, '.')
from knip import *

BASIS = '../r4/gemini_r4_lijf.png'
DONOR = '../r1/gemini_r1_handen_gewisseld.png'

# naam, klasse, kader basis, kader donor, opties
#   kaart: het donorstuk dat op het basisonderdeel komt (anders bbox donormasker)
#   tegel: vaste schaal (donorpixels per basispixel = 1/tegel), gespiegeld herhaald
#   spiegel: horizontaal spiegelen
DELEN = [
    ('voorhand',   'roze',  (272, 268, 358, 340), (266, 292, 352, 362), {'kaart': (271, 298, 346, 338)}),
    # de voorarm van de donor zit achter de hand/baard: de geribbelde
    # bovenarm van de achterste arm (ligt ook horizontaal) is de donor
    ('voorarm',    'roze',  (350, 262, 402, 322), (585, 183, 695, 265), {'kaart': (600, 200, 680, 255)}),
    ('achterhand', 'roze',  (672, 300, 756, 378), (678, 292, 772, 378), {}),
    ('elleboog',   'roze',  (656, 246, 710, 314), (660, 215, 752, 300), {}),
    ('schouder',   'roze',  (572, 200, 668, 276), (585, 183, 695, 265), {}),
    # neus (x 395-460, y 160-215) hoort er niet bij
    ('romp',       'roze',  [(462, 160), (600, 160), (668, 240), (668, 348), (380, 348), (380, 235), (462, 222)],
                            [(530, 255), (645, 255), (645, 326), (530, 326)],
                            {'kaart': (561, 278, 632, 295), 'tegel': 1.0}),
    ('voet_links', 'blauw', (372, 437, 505, 484), (380, 372, 560, 482), {'kaart': (425, 430, 502, 478)}),
    ('been_links', 'blauw', [(390, 360), (545, 360), (545, 437), (390, 437)],
                            [(372, 370), (560, 380), (560, 482), (372, 482)], {'kaart': (382, 380, 505, 452)}),
    ('voet_rechts','blauw', (572, 448, 668, 494), (580, 466, 692, 502), {}),
    ('been_rechts','blauw', [(545, 345), (680, 345), (680, 448), (545, 448)],
                            [(560, 345), (695, 345), (695, 468), (560, 468)], {}),
]


def main(debug=True):
    b = laad(BASIS)
    d = laad(DONOR)
    uit = b.copy()
    mbs = basismaskers(b, DELEN, donker=80, gat=900, binnennaad=4)
    mb_all, md_all = [], []
    for (naam, cls, kb, kd, opt), mb in zip(DELEN, mbs):
        md = zonder_omlijning(d, deelmasker(d, cls, kd, sluit=3))
        md &= klasse(d, cls, True) | (d.mean(axis=-1) < 110)
        if opt.get('zonder_zwart'):
            # pikzwarte donorlijnen (lum < 45) zijn omlijning tussen losse
            # donorstukken; in de basisvorm worden het losse strepen
            md &= d.mean(axis=-1) >= 45
        nood = plak(uit, mb, d, md, spiegel=opt.get('spiegel', False), kader_b=bbox(mb),
                    kader_d=opt.get('kaart') or bbox(md), tegel=opt.get('tegel'))
        mb_all.append(mb); md_all.append(md)
        print(f'{naam:12s} basis {tuple(map(int, bbox(mb)))} ({mb.sum()} px)  '
              f'donor {tuple(map(int, opt.get("kaart") or bbox(md)))} ({md.sum()} px)  noodvulling {nood:.1%}')
    x = omtrek(b) ^ omtrek(uit)
    print('silhouetbewaker zet basis terug op', int(x.sum()), 'px')
    uit[x] = b[x]
    Image.fromarray(uit.astype(np.uint8)).save('model_hybride.png')
    if debug:
        debug_maskers(b, mb_all, 'debug_maskers_basis.png')
        debug_maskers(d, md_all, 'debug_maskers_donor.png')
    print('omtrekverschil silhouet (xor):', int((omtrek(b) ^ omtrek(uit)).sum()))
    print('verschil niet-witte pixels (xor, incl. binnenglim):', int((nietwit(b) ^ nietwit(uit)).sum()))
    vergelijk([BASIS, 'model_hybride.png', DONOR], 'vergelijk.png')


if __name__ == '__main__':
    main()
