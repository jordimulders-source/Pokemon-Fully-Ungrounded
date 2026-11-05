"""Kleur ronde 4 van de wasbeer (S1a): ronde3.txt met een warmer palet (Jordi: "1 ja warmer") en meer contrast per
kleurgroep (hue shift: licht warmer/geler, schaduw iets koeler/dieper), plus alleen de staarthaak als haak (Furret/Sentret).
Draaien: python3 docs/concept/sprites/wasbeer/kleur_v2/rijen_ronde4.py -> ronde4.txt, ronde4.png, ronde4.pal + controle."""
import os
import numpy as np
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__))

PALET = [(152, 208, 160),                                          # 0 transparant
         (24, 15, 12), (46, 34, 28),                               # 1 omlijning, 2 masker/onderarm/-been/ring (warm zwart)
         (198, 180, 152),                                          # 3 hooglicht (warm)
         (68, 55, 48), (100, 82, 68), (130, 110, 90), (162, 142, 116),   # 4-7 warm grijsbruin: selout, schaduw, basis, licht
         (172, 150, 118), (214, 198, 166), (244, 236, 218),        # 8-a crème: oker-schaduw, crème, warm wit
         (88, 56, 36), (128, 84, 52), (166, 118, 76),              # b-d buidel: eigen roodbruin (Coathief-familie)
         (110, 36, 24), (178, 78, 46)]                             # e-f iris


def rij(y, x0, s):
    return {(x0 + i, y): c for i, c in enumerate(s)}


# Staarthaak: de terugkrullende punt (x 49-50) los van de schacht met een donkere binnenlijn 1 op x 51 (y 23-28),
# punt en schacht elk met licht 4 links en kernschaduw 1 rechts (Furret/Sentret: elk deel eigen licht/schaduw).
Z = {'staarthaak': {**rij(22, 49, '144222211'), **rij(23, 48, '1421422211'), **rij(24, 48, '1421422211'),
                    **rij(25, 48, '1421422211'), **rij(26, 48, '1421422211'), **rij(27, 48, '1421422211'),
                    **rij(28, 49, '114222211'), **rij(29, 49, '142222211')}}


def lees(p):
    return np.array([[0 if c == '.' else int(c, 16) for c in l.rstrip()] for l in open(p)])


def main():
    g = lees(os.path.join(HERE, 'ronde3.txt')); r3 = g.copy()
    for n, d in Z.items():
        for (x, y), c in d.items():
            assert g[y, x] != 0, ('buiten silhouet', n, x, y)
            g[y, x] = int(c, 16)
    sil = np.array([[c == '#' for c in l.rstrip()] for l in open(os.path.join(HERE, '../silhouet_v2/direct_s1a.txt'))])
    print('alpha-diff met direct_s1a:', int(((g > 0) != sil).sum()), '| pixels gewijzigd t.o.v. ronde3:', int((g != r3).sum()))
    open(os.path.join(HERE, 'ronde4.txt'), 'w').write('\n'.join(''.join('.' if v == 0 else format(v, 'x') for v in r) for r in g) + '\n')
    im = Image.new('P', (64, 64)); im.putpalette(sum(PALET, ())); im.putdata(g.flatten().tolist())
    im.save(os.path.join(HERE, 'ronde4.png'), transparency=0)
    open(os.path.join(HERE, 'ronde4.pal'), 'w').write('JASC-PAL\n0100\n16\n' + ''.join(f'{r} {gg} {b}\n' for r, gg, b in PALET))
    rand = [(int(x), int(y)) for y, x in zip(*np.nonzero(g))
            if any(not (0 <= y + dy < 64 and 0 <= x + dx < 64) or g[y + dy, x + dx] == 0 for dy, dx in ((0, 1), (0, -1), (1, 0), (-1, 0)))
            and g[y, x] not in (1, 2, 4, 11, 12)]
    print('randpixels niet 1/2/4/b/c:', rand)
    luma = lambda c: round(0.3 * c[0] + 0.59 * c[1] + 0.11 * c[2])
    print('luma vacht 4-7 + 3:', [luma(PALET[i]) for i in (4, 5, 6, 7, 3)], '| crème 8,9,a:', [luma(PALET[i]) for i in (8, 9, 10)],
          '| buidel b,c,d:', [luma(PALET[i]) for i in (11, 12, 13)])


if __name__ == '__main__':
    main()
