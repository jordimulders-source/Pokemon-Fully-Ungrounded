"""Kleur ronde 2 van de wasbeer (S1a): ronde1.txt + reparaties uit KEURING_ronde1.md (punten 1-10), met de hand per zone.
Stap 0: paletindex 3 (72,63,58) ging op in 4 (niet te onderscheiden); index 3 is nu hooglicht-grijs (176,168,156).
Crème selout = c (120,103,84). Elke reparatie staat als expliciete pixel (x, y): index.
Draaien: python3 docs/concept/sprites/wasbeer/kleur_v2/rijen_ronde2.py -> ronde2.txt, ronde2.png, ronde2.pal + controle."""
import os
import numpy as np
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__))

PALET = [(152, 208, 160), (22, 16, 16), (44, 37, 35), (176, 168, 156),
         (74, 68, 63), (96, 89, 81), (118, 110, 100), (146, 138, 126),
         (158, 147, 128), (204, 194, 172), (238, 233, 222),
         (86, 72, 58), (120, 103, 84), (150, 131, 106),
         (100, 34, 24), (168, 72, 46)]


def rij(y, x0, s):
    return {(x0 + i, y): c for i, c in enumerate(s)}


Z = {}
# 6. selout op de lichtkant van oren en kop (was 1)
Z['oren/kop selout'] = {(31, 15): '4', **rij(0, 15, '4441'), (14, 1): '4', (19, 1): '4', (25, 1): '4', (26, 1): '4', (27, 1): '4',
                        (13, 2): '4', (25, 2): '4', (12, 3): '4', (24, 3): '4', (12, 4): '4', (24, 4): '4'}
# 5. hooglicht op de kop (bol, linksboven)
Z['kop hooglicht'] = {**rij(5, 15, '333'), **rij(6, 14, '33')}
# 2. masker: twee lobben met brug, wenkbrauwboog, lobonderkant rond, oogkas, verre oog 1 px naar binnen
Z['masker'] = {(18, 9): 'a', (16, 10): '4', (17, 10): '4', (16, 12): '2', (16, 13): '2',
               (19, 14): 'a', (24, 14): '6', (23, 15): '6', (24, 15): '6', (18, 14): 'a', (25, 12): '6', (25, 13): '6'}
Z['ogen'] = {(19, 10): '1', (20, 13): '4', (21, 13): '4', (22, 13): '4', (23, 11): '4', (23, 12): '4', (22, 12): 'f',
             (12, 10): '2', (12, 11): '2', (13, 11): 'e', (13, 12): 'f'}
Z['snuit'] = {(22, 17): '8'}
# 5. romp: hooglichtboog schouder/borst, gebogen 6/5-grens, kernschaduw + bovenarm (4) langs de rug
Z['romp'] = {**rij(21, 17, '333'), **rij(22, 16, '33'), (16, 23): '3',
             (28, 23): '6', (28, 24): '6', (29, 24): '6', (28, 25): '6', (29, 25): '6',
             (33, 22): '4', (33, 23): '4', (33, 24): '4', (33, 25): '4',
             (35, 28): '4', (36, 29): '4', (36, 30): '4', (36, 31): '4', (37, 32): '4'}
# 4. buidelnaad: grijze 4 naast b -> 5 (één grens), onderkant loopt over in de rug
Z['naad'] = {(33, 17): '5', (33, 18): '5', (33, 19): '5', (33, 20): '5', (34, 20): '5', (34, 21): '5',
             (34, 22): '5', (34, 23): '5', (35, 23): '5', (34, 24): '5', (35, 24): '5', (34, 25): '5', (35, 25): '5',
             (36, 26): '5', (36, 27): '5', (36, 28): '5', (37, 29): '5', (37, 30): '5', (37, 31): '5', (38, 32): '5',
             (38, 33): '5', (39, 33): '5', (39, 34): '5', (40, 34): '5', (40, 35): '5', (41, 35): 'b'}
# 4. buidel: zakmond (gebogen spleet 1 van (35,18) naar (39,20), lichte lip d erboven, b eronder) + één plooi b met lichte rug d
Z['buidel'] = {**rij(16, 33, '1bdbb1'), **rij(17, 34, 'bddd1'),
               **rij(18, 34, 'b11dd1'), **rij(19, 34, 'bbc11db1'), **rij(20, 35, 'cddb1cd1'),
               (38, 25): 'b', (39, 26): 'b', (40, 27): 'b', (41, 28): 'b', (42, 29): 'b',
               (39, 25): 'd', (40, 26): 'd', (41, 27): 'd', (42, 28): 'd'}
# 3. nabije klauw: klauwen tegen elkaar (inkeping alleen y 32-33), crème strook links -> grijs, 2 punten
Z['nabije klauw'] = {(24, 30): '9', (24, 31): '9',
                     **rij(28, 15, '7776665'), **rij(29, 15, '7666665'), **rij(30, 17, '66665'), **rij(31, 18, '6665'),
                     **rij(32, 19, '665'), **rij(33, 19, '465'), (20, 34): '4'}
# 8. nabije onderarm als buis (licht boven 5, midden 4, onder 2, rand 1) + bovenarm (zie romp, x 33)
Z['nabije onderarm'] = {**rij(26, 29, '44444'), **rij(27, 29, '5555'), (33, 27): '4',
                        **rij(28, 28, '55554'), (33, 28): '4', **rij(29, 28, '44444'), **rij(30, 27, '24444221'),
                        (28, 33): '4'}
# 3. verre klauw: crème selout c aan de lichtkant (open rand dicht), schaduw 8 onderaan, hooglicht 9 boven
Z['verre klauw'] = {(10, 34): 'c', (11, 34): '1', (9, 35): 'c', **rij(36, 8, 'c9999881'), **rij(37, 8, 'c998881'),
                    **rij(38, 8, 'c98881'), **rij(39, 7, 'c98881'), **rij(40, 7, 'c98881'), **rij(41, 7, 'c81881'),
                    **rij(42, 6, 'c81'), **rij(42, 10, 'c81'), **rij(43, 6, 'c81'), **rij(43, 10, 'c1'),
                    **rij(44, 6, 'c1'), **rij(44, 10, 'c1'), (17, 30): '6'}
# 5. nabije dij: hooglicht 7 linksboven, schaduwhalvemaan 5 onderaan; 6: (28,45) zwart -> 4
Z['nabije dij'] = {**rij(36, 31, '7777'), **rij(37, 31, '7777'), **rij(38, 31, '777'), **rij(39, 32, '77'),
                   **rij(45, 32, '5555'), **rij(46, 31, '55555'), (28, 45): '4'}
# 7. staart: lichte vierkant weg, lichte rand langs de haak, schaduwlijn onder de punt, gebogen ringen, randen dicht
Z['staart'] = {**rij(19, 53, '88'), **rij(20, 49, '1488842'), **rij(23, 49, '411222222'), **rij(24, 53, '2222'),
               **rij(25, 53, '2222'), **rij(26, 54, '222'), (50, 31): '2', (56, 31): '2', (50, 32): '4', (49, 33): '4',
               (50, 34): '8', (47, 38): '2', (44, 39): '4'}


def main():
    g = np.array([[0 if c == '.' else int(c, 16) for c in l.rstrip()] for l in open(os.path.join(HERE, 'ronde1.txt'))])
    g[g == 3] = 4                                    # stap 0
    gezien = {}
    for n, d in Z.items():
        for (x, y), c in d.items():
            assert g[y, x] != 0, ('buiten silhouet', n, x, y)
            gezien[(x, y)] = n
            g[y, x] = int(c, 16)
    r1 = np.array([[0 if c == '.' else int(c, 16) for c in l.rstrip()] for l in open(os.path.join(HERE, 'ronde1.txt'))])
    sil = np.array([[c == '#' for c in l.rstrip()] for l in open(os.path.join(HERE, '../silhouet_v2/direct_s1a.txt'))])
    print('alpha-diff met direct_s1a:', int(((g > 0) != sil).sum()))
    print('gewijzigd t.o.v. ronde1 (excl. 3->4):', int(((g != r1) & ~(r1 == 3)).sum()), 'px; per zone:',
          {n: len(d) for n, d in Z.items()})
    open(os.path.join(HERE, 'ronde2.txt'), 'w').write('\n'.join(''.join('.' if v == 0 else format(v, 'x') for v in r) for r in g) + '\n')
    im = Image.new('P', (64, 64)); im.putpalette(sum(PALET, ())); im.putdata(g.flatten().tolist())
    im.save(os.path.join(HERE, 'ronde2.png'), transparency=0)
    open(os.path.join(HERE, 'ronde2.pal'), 'w').write('JASC-PAL\n0100\n16\n' + ''.join(f'{r} {gg} {b}\n' for r, gg, b in PALET))
    # open randen: pixel naast transparant moet omlijning (1), donker (2), selout (4, c) of schaduw (8 alleen in de staart/klauwpunt) zijn
    rand = []
    for y, x in zip(*np.nonzero(g)):
        if any(not (0 <= y + dy < 64 and 0 <= x + dx < 64) or g[y + dy, x + dx] == 0 for dy, dx in ((0, 1), (0, -1), (1, 0), (-1, 0))):
            if g[y, x] not in (1, 2, 4, 11, 12):
                rand.append((int(x), int(y), format(g[y, x], 'x')))
    print('randpixels niet 1/2/4/b/c:', rand)
    # losse pixels: geen enkele buur (8-buren) met dezelfde index, buiten omlijning 1
    los = []
    for y, x in zip(*np.nonzero(g)):
        if g[y, x] == 1: continue
        if not any(g[y + dy, x + dx] == g[y, x] for dy in (-1, 0, 1) for dx in (-1, 0, 1) if (dy or dx) and 0 <= y + dy < 64 and 0 <= x + dx < 64):
            los.append((int(x), int(y), format(g[y, x], 'x')))
    print('losse pixels (8-buren):', los)


if __name__ == '__main__':
    main()
