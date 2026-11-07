"""Kleur ronde 5 van de wasbeer (S1a): ronde4.txt + de 8 reparaties uit KEURING_ronde4.md (alleen kleur, binnen het silhouet).
Elke reparatie als expliciete pixel (x, y): (oud, nieuw); het script controleert dat 'oud' klopt.
Draaien: python3 docs/concept/sprites/wasbeer/kleur_v2/rijen_ronde5.py -> ronde5.txt, ronde5.png, ronde5.pal + controle."""
import os
import numpy as np
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__))
PALET = [tuple(int(v) for v in l.split()) for l in open(os.path.join(HERE, 'ronde4.pal')).read().split('\n')[3:19]]
PALET[8] = (184, 146, 96)      # 8. crème-schaduw echt oker (verschilt nu van vacht 7)


def zet(oud, nieuw, *pts):
    return {p: (oud, nieuw) for p in pts}


Z = {
    # 1. nabije hand: handrug a -> 9 behalve één glans (24,26); slagschaduw 8 onder de klauwpunten
    '1 nabije hand': {**zet('a', '9', (25, 26), (26, 26), (27, 26), (23, 27), (24, 27), (25, 27), (26, 27), (22, 28), (25, 28)),
                      **zet('9', '8', (21, 34), (24, 34), (21, 35), (22, 35), (23, 35), (24, 35), (25, 35), (26, 35)),
                      (27, 35): ('8', '7')},
    # 2. nabije onderarm: bovenkant als lichtkant 4, elleboog 4
    '2 onderarm': zet('2', '4', (28, 29), (29, 29), (30, 29), (31, 29), (28, 30), (29, 30), (33, 29)),
    # 3. bovenarm: eigen hooglicht 3 (waar nu 7: x 31 op y 21-22, x 32 op y 23-24)
    '3 bovenarm': zet('7', '3', (31, 21), (31, 22), (32, 23), (32, 24)),
    # 4. staarthaak: lichte ring over de bocht, schacht naast de binnenlijn 5 voor contrast
    '4 staarthaak': {(51, 20): ('8', '9'), (52, 20): ('4', 'a'), (53, 20): ('4', '9'), (54, 20): ('2', '8'), (55, 20): ('2', '8'),
                     (51, 21): ('4', '9'), (52, 21): ('2', '9'), (53, 21): ('2', '8'), (54, 21): ('2', '8'),
                     **zet('4', '5', (52, 23), (52, 24), (52, 25), (52, 26), (52, 27))},
    # 5. zakmond 2 rijen diep aan de schouderkant
    '5 zakmond': zet('d', '2', (36, 20), (37, 20)),
    # 6. verre dij: lichtrand 6 langs de bovenkant ((19,43) is randpixel -> (20,43))
    '6 verre dij': zet('5', '6', (22, 40), (23, 40), (24, 40), (21, 41), (22, 41), (23, 41), (20, 42), (21, 42), (20, 43)),
    # 7. romp: hooglicht 7 als boog verder het lijf in (alleen waar nu 6)
    '7 romp': zet('6', '7', (20, 23), (21, 23), (20, 24), (21, 24), (19, 25), (20, 25), (21, 25), (19, 26), (20, 26), (21, 26),
                  (19, 27), (20, 27)),
}


def lees(p):
    return np.array([[0 if c == '.' else int(c, 16) for c in l.rstrip()] for l in open(p)])


def main():
    g = lees(os.path.join(HERE, 'ronde4.txt')); r4 = g.copy()
    for n, d in Z.items():
        for (x, y), (o, c) in d.items():
            assert g[y, x] == int(o, 16), (n, x, y, 'is', format(g[y, x], 'x'), 'niet', o)
            g[y, x] = int(c, 16)
        print(f'zone {n}: {len(d)} px')
    sil = np.array([[c == '#' for c in l.rstrip()] for l in open(os.path.join(HERE, '../silhouet_v2/direct_s1a.txt'))])
    print('alpha-diff met direct_s1a:', int(((g > 0) != sil).sum()), '| totaal gewijzigd t.o.v. ronde4:', int((g != r4).sum()), 'px + palet 8')
    open(os.path.join(HERE, 'ronde5.txt'), 'w').write('\n'.join(''.join('.' if v == 0 else format(v, 'x') for v in r) for r in g) + '\n')
    im = Image.new('P', (64, 64)); im.putpalette(sum(PALET, ())); im.putdata(g.flatten().tolist())
    im.save(os.path.join(HERE, 'ronde5.png'), transparency=0)
    open(os.path.join(HERE, 'ronde5.pal'), 'w').write('JASC-PAL\n0100\n16\n' + ''.join(f'{r} {gg} {b}\n' for r, gg, b in PALET))
    rand = [(int(x), int(y)) for y, x in zip(*np.nonzero(g))
            if any(not (0 <= y + dy < 64 and 0 <= x + dx < 64) or g[y + dy, x + dx] == 0 for dy, dx in ((0, 1), (0, -1), (1, 0), (-1, 0)))
            and g[y, x] not in (1, 2, 4, 11, 12)]
    print('randpixels niet 1/2/4/b/c:', rand)


if __name__ == '__main__':
    main()
