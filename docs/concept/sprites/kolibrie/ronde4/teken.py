"""Kolibrie ronde 4: alleen de staart van ronde3/kolibrie_variant_sleep.png gerepareerd.
Pixel voor pixel met de hand: per rij (x, tekens); '.' = transparant maken, '_' = niet aanraken.
Kop, kuif, lijf en vleugels zijn bevroren (zie check.py)."""
import os, sys
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '../ronde3'))
from teken import PAL  # zelfde palet als ronde 3

BASIS = os.path.join(HERE, '../ronde3/kolibrie_variant_sleep.png')

EDITS = {
    # punt 4 en 5: S1 als boog (bovenrand 5-3-2-1-1), hooglicht een tint terug, schaduwkant donker
    30: [(57, 'gmpmpm')],
    31: [(56, 'gmppmv.')],
    32: [(54, 'ggmmpmv..')],
    33: [(51, 'vvvVVmmmv..')],
    34: [(51, 'VVVVVVwK..')],
    35: [(47, 'VVVVVVVVVwK..')],
    36: [(42, 'v'), (50, 'KKKKKKK.')],
    # punt 3: onderkant staartbasis oplopend in treden van 3 (rij 40 x42-44, rij 39 x45-47, rij 38 x48-50)
    38: [(48, 'KKK')],
    39: [(42, 'K'), (45, 'KKK..')],
    40: [(45, 'KVv..K'), (55, 'gg')],
    # punt 1: schaduwkant S2 en S3 donker (1 in violet, 5 in het bleke deel)
    41: [(45, 'KLv'), (51, 'KKKK')],
    42: [(45, 'K'), (55, 'vv.')],
    43: [(46, 'KK')],
    44: [(48, 'KK')],
    45: [(50, 'KK')],
    46: [(52, 'vv')],
    47: [(54, 'vvmg.')],
    48: [(55, 'vmg')],
    49: [(56, 'vmm.')],
    # punt 2: S2- en S3-vlam liggend: ronde voet aan de sliertkant, één punt naar achteren
    # (B: rij 38-42, C: rij 49-53; niet gekopieerd, C is korter onderaan)
}
VLAM = {
    38: [(58, 'mm.')],
    39: [(57, 'mPPmm')],
    40: [(57, 'mPWPpmm')],
    41: [(57, 'mppmm')],
    42: [(58, 'mm.')],
    50: [(56, 'mPPmm')],
    51: [(56, 'mPWPmmm')],
    52: [(56, 'mppm.')],
    53: [(57, 'mm.')],
}


def build():
    im = Image.open(BASIS).copy()
    px = im.load()
    for tab in (EDITS, VLAM):
        for y, segs in tab.items():
            for x0, t in segs:
                for i, ch in enumerate(t):
                    if ch == '_':
                        continue
                    px[x0 + i, y] = 0 if ch == '.' else PAL[ch][0]
    return im


if __name__ == '__main__':
    build().save(os.path.join(HERE, 'kolibrie.png'), transparency=0)
