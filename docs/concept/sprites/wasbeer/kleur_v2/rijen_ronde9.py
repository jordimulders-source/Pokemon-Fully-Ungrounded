"""Kleur ronde 9 van de wasbeer: exact reparaties 1-8 uit KEURING_ronde8.md op ronde 8, als (x, y): (oud, nieuw).
Reparatie 1 in twee versies: ronde9 = nabij oog ronder zonder pupil (lijn olinguito/Coathief),
ronde9b = idem met pupil (21,12) f->1 zoals de keuring voorstelt.
Draaien: python3 docs/concept/sprites/wasbeer/kleur_v2/rijen_ronde9.py -> ronde9.txt/.png/.pal, ronde9b.txt/.png + controles."""
import os
import numpy as np
from PIL import Image
from rijen_ronde8 import binnen_los, N4, lees

HERE = os.path.dirname(os.path.abspath(__file__))
PAL_TXT = open(os.path.join(HERE, 'ronde8.pal')).read()
PALET = [tuple(int(v) for v in l.split()) for l in PAL_TXT.split('\n')[3:19]]

R = {
    'R1 nabij oog rond, wallenbalk weg': {(21, 13): ('4', 'f'), (20, 13): ('4', '2'), (22, 13): ('4', '2')},
    'R2 verre oog onderlid': {(13, 13): ('4', '2')},
    'R3 verre oor schaduwrand + sluiten': {(28, 3): ('9', '3'), (28, 4): ('9', '3'), (28, 5): ('9', '3'), (29, 5): ('9', '3'),
                                           (28, 6): ('5', '4'), (29, 6): ('9', '5')},
    'R4 nabij oor als holte': {(16, 2): ('5', '4'), (17, 2): ('5', '4'), (17, 3): ('4', '5')},
    'R5 staartpunt': {(56, 26): ('8', '2'), (56, 28): ('1', '2')},
    'R6 onderarm': {(33, 29): ('4', '2')},
    'R7 slagschaduw achter de kop': {(30, 16): ('6', '5'), (31, 16): ('6', '5'), (30, 17): ('6', '5'), (31, 17): ('6', '5'),
                                     (29, 18): ('6', '5'), (30, 18): ('6', '5')},  # keuring noemde (28-29,18); het 6-vlak staat op (29-30,18),
    'R8 kaak en neus': {(16, 19): ('7', '6'), (17, 19): ('7', '6'), (18, 19): ('7', '6'), (12, 16): ('6', '7'), (13, 17): ('2', '4')},
}
PUPIL = {(21, 12): ('f', '1')}


def pas_toe(g, d, naam):
    for (x, y), (o, c) in d.items():
        assert g[y, x] == int(o, 16), (naam, x, y, format(int(g[y, x]), 'x'))
        g[y, x] = int(c, 16)


def schrijf(g, naam, pal=False):
    open(os.path.join(HERE, naam + '.txt'), 'w').write(
        '\n'.join(''.join('.' if v == 0 else format(v, 'x') for v in r) for r in g) + '\n')
    im = Image.new('P', (64, 64)); im.putpalette(sum(PALET, ())); im.putdata(g.flatten().tolist())
    im.save(os.path.join(HERE, naam + '.png'), transparency=0)
    if pal:
        open(os.path.join(HERE, naam + '.pal'), 'w').write(PAL_TXT)


def controle(g, r8, naam):
    sil = np.array([[c == '#' for c in l.rstrip()] for l in open(os.path.join(HERE, '../silhouet_v2/direct_s1a.txt'))])
    lab = open(os.path.join(HERE, '../silhouet_v2/labels_s1a.txt')).read().split('\n')[1:65]
    ger = [(x, y) for y in range(64) for x in range(64) if g[y, x] != r8[y, x]]
    bev = [(x, y) for x, y in ger if lab[y][x] in 'ZKk' or r8[y, x] in (11, 12, 13) or (x, y) in ((13, 11), (13, 12))
           or (y >= 22 and x < 46 and (r8[y, x] in (8, 9, 10) or g[y, x] in (8, 9, 10)))]
    rand = [(int(x), int(y)) for y, x in zip(*np.nonzero(g))
            if any(not (0 <= y + dy < 64 and 0 <= x + dx < 64) or g[y + dy, x + dx] == 0 for dy, dx in N4)
            and g[y, x] not in (1, 2, 4, 11, 12)]
    l8, l9 = set(binnen_los(r8)), set(binnen_los(g))
    print(f'{naam}: alpha-diff {int(((g > 0) != sil).sum())} | gewijzigd t.o.v. ronde8 {len(ger)} px | bevroren geraakt {bev} '
          f'| open randen {rand} | losse binnenpixels {len(l8)} -> {len(l9)} | nieuw los {sorted(l9 - l8)} | weg {sorted(l8 - l9)}')


def main():
    r8 = lees(os.path.join(HERE, 'ronde8.txt'))
    g = r8.copy()
    for n, d in R.items():
        pas_toe(g, d, n)
    gb = g.copy()
    pas_toe(gb, PUPIL, 'pupil')
    controle(g, r8, 'ronde9 ')
    controle(gb, r8, 'ronde9b')
    schrijf(g, 'ronde9', pal=True)
    schrijf(gb, 'ronde9b')


if __name__ == '__main__':
    main()
