# Omlijningsronde r6 -> r7 (Dragonfly Cave-gids r. 80-170 / 340-470): outline base per onderdeel in de eigen
# donkerste tint, zwart alleen als outline shadow aan de schaduwkant (licht linksboven). Alleen zwarte pixels
# (index 1) worden omgetint; geen pixel verplaatst, silhouet en palet gelijk. Draaien vanuit eindkeuring_r6/:
#   python3 omlijning.py
import numpy as np
from PIL import Image

SRC = '../sprite/r6/'
ZWART = 1
# paletindices r6: 2-5 lijf (wit..donkerlavendel), 6-8 gewrichten/antennes, 9-12 panelen, 13-14 lens (teal)
DEEL = {2: 'lijf', 3: 'lijf', 4: 'lijf', 5: 'lijf', 6: 'gew', 7: 'gew', 8: 'gew',
        9: 'paneel', 10: 'paneel', 11: 'paneel', 12: 'paneel', 13: 'oog', 14: 'oog'}
BASIS = {'lijf': 5, 'gew': 8, 'paneel': 9}          # donkerste eigen tint = outline base
# dieptevolgorde (hoog = vooraan): gewrichten > groot paneel ~ lijf > klein paneel
def diepte(deel, x):
    if deel == 'gew': return 4
    if deel == 'paneel': return 3 if x >= 28 else 1   # groot paneel ligt vóór het lijf, het kleine erachter
    return 2
# lens (het gezicht): ringen en pupil blijven zoals ze zijn
OOG_C, OOG_R = (19.0, 34.5), 6.6

def plan(a):
    H, W = a.shape
    nieuw = {}
    for y in range(H):
        for x in range(W):
            if a[y, x] != ZWART: continue
            if (x - OOG_C[0]) ** 2 + (y - OOG_C[1]) ** 2 <= OOG_R ** 2: continue
            buren = []
            for r in (1, 2):
                for dy in range(-r, r + 1):
                    for dx in range(-r, r + 1):
                        xx, yy = x + dx, y + dy
                        if (dx or dy) and 0 <= xx < W and 0 <= yy < H and a[yy, xx] in DEEL and DEEL[a[yy, xx]] != 'oog':
                            buren.append((dx, dy, DEEL[a[yy, xx]], xx))
                if buren: break
            if not buren: continue
            voor = max(buren, key=lambda b: diepte(b[2], b[3]))
            deel = voor[2]
            # normaal = van het voorste onderdeel naar de lijnpixel
            nx = -sum(b[0] for b in buren if b[2] == deel and diepte(b[2], b[3]) == diepte(deel, voor[3]))
            ny = -sum(b[1] for b in buren if b[2] == deel and diepte(b[2], b[3]) == diepte(deel, voor[3]))
            d = nx + ny
            licht = d < 0 or (d == 0 and ny < 0)
            if licht:
                nieuw[(x, y)] = BASIS[deel]
    # handmatig zwart gehouden (benoemd): geen zwart/gekleurd om en om op één rand
    for xy in ZWART_HOUDEN: nieuw.pop(xy, None)
    nieuw.update(EIGEN_TINT)
    return nieuw

ZWART_HOUDEN = [
    (54, 32),                      # rechterrand groot paneel: schaduwkant, rest van die rand is zwart
    (28, 47), (28, 48),            # begin onderrand groot paneel (linksonder): rest van die rand is zwart
    (27, 30), (28, 30),            # rechterrand van de paarse lensring-band: schaduwkant, lijn erboven/eronder zwart
    (14, 42), (15, 42), (15, 41),  # linksonder lenshuis: zwarte boog linksmidden -> onder (Popplio-regel)
    (13, 38), (13, 39), (14, 38), (11, 36),
    (13, 29), (13, 30),            # buitenrand lenshuis linksboven: lens (gezicht) blijft zoals r6
    (29, 33), (29, 37),            # brugpixels: anders breekt de 1 px naadlijn rechts van de lensring
]
# eindkeuring (losse pixels / om-en-om op één rand): zelfde tint als de rest van die rand
EIGEN_TINT = {
    (47, 16): 9,                   # linkerbovenhoek groot paneel (was losse 8)
    (45, 19): 9,                   # linkerrand groot paneel onder de arm (was losse zwarte tussen 9'en)
    (36, 17): 8,                   # bovenrand bij rechter gewricht/arm (was losse 5 tussen 8'en)
}

def schrijf(src, dst, nieuw):
    im = Image.open(src); a = np.array(im)
    for (x, y), v in nieuw.items(): a[y, x] = v
    out = Image.fromarray(a, 'P'); out.putpalette(im.getpalette())
    out.save(dst, transparency=0)
    return a

if __name__ == '__main__':
    a = np.array(Image.open(SRC + 'sprite.png')); b = np.array(Image.open(SRC + 'oog_b.png'))
    nieuw = plan(a)
    verschil = set(zip(*np.nonzero(a != b)[::-1]))
    assert not (set(nieuw) & verschil), 'omlijning raakt de oogvariant'
    for naam in ('sprite.png', 'oog_b.png'):
        r = schrijf(SRC + naam, 'r7/' + naam, nieuw)
        o = np.array(Image.open(SRC + naam))
        assert ((r == 0) == (o == 0)).all(), 'silhouet veranderd'
        assert set(zip(*np.nonzero(r != o)[::-1])) == set(nieuw)
        assert all(o[y, x] == ZWART for (x, y) in nieuw)
    from collections import Counter
    print(len(nieuw), 'zwarte pixels omgetint:', Counter(nieuw.values()))
    print('zwart r6 %d -> r7 %d' % ((a == 1).sum(), (a == 1).sum() - len(nieuw)))
