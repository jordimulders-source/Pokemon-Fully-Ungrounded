"""Kleur ronde 10 van de wasbeer: alleen de neus (zone x 3-11, y 13-20 mag ook in het silhouet veranderen; Jordi:
"de neus is nog steeds een raar uit stekend streepje"). Ronde neusknop zoals in de render: donker 2, glans 7 linksboven,
omlijning 1 aan de buitenkant (links/onder), 4 als zachte onderrand naar de crème kin, crème snuit erboven/erachter.
Op ronde9 -> ronde10 en op ronde9b -> ronde10b. Draaien: python3 docs/concept/sprites/wasbeer/kleur_v2/rijen_ronde10.py"""
import os
import numpy as np
from PIL import Image
from rijen_ronde8 import binnen_los, N4, lees

HERE = os.path.dirname(os.path.abspath(__file__))
PAL_TXT = open(os.path.join(HERE, 'ronde9.pal')).read()
PALET = [tuple(int(v) for v in l.split()) for l in PAL_TXT.split('\n')[3:19]]
ZONES = {'neus': (3, 11, 13, 20), 'staart': (44, 58, 15, 33)}  # x0, x1, y0, y1 (incl.): hier mag het silhouet veranderen
# (x, y): (oud, nieuw); '.' = transparant
NEUS = {
    (10, 16): ('.', '1'), (11, 16): ('2', '7'), (12, 16): ('7', '2'), (13, 16): ('2', '2'),
    (9, 17): ('.', '1'), (10, 17): ('1', '2'), (11, 17): ('2', '2'), (12, 17): ('2', '2'), (13, 17): ('4', '4'),
    (10, 18): ('.', '1'), (11, 18): ('1', '2'), (12, 18): ('9', '4'),
}

# Nabije klauw (Jordi: "de bovenkant van de binnenste klauw moet nog iets meer belijning"):
# donkere selout 4 langs de bovenrand van de hand (op de lijfrij erboven), hoek 5; klauwvorm en crème blijven.
KLAUW = {(22, 25): ('6', '5'), (23, 25): ('6', '4'), (24, 25): ('6', '4'), (25, 25): ('6', '4'), (26, 25): ('6', '4'),
         (27, 25): ('6', '4'), (28, 25): ('6', '4')}
# Staartpunt (Jordi: "de staart idd, die vertaalt niet helemaal lekker vanuit het 3d model"): de punt krult terug
# met lucht in de bocht (x 51-52, y 24-29, open naar linksonder); koepel met lichte boog 5/4 linksboven die langs de
# hangende punt doorloopt; schacht rechts met ring (boven/onder als boog), eigen omlijning langs de spleet.
# Rijen x 47-58, '.' = transparant.
STAART = [
    (18, "......11...."),
    (19, "...1445421.."),
    (20, "..145542221."),
    (21, ".1455422221."),
    (22, ".14542222221"),
    (23, ".15421229921"),
    (24, ".1541.19a981"),
    (25, ".1541.199881"),
    (26, ".1421.182281"),
    (27, ".141..122221"),
    (28, "..11..122221"),
    (29, "....1422221."),
]


def maak(bron, naam, pal):
    g = lees(os.path.join(HERE, bron + '.txt'))
    oud = g.copy()
    for (x, y), (o, c) in NEUS.items():
        assert g[y, x] == (0 if o == '.' else int(o, 16)), (x, y)
        g[y, x] = 0 if c == '.' else int(c, 16)
    for (x, y), (o, c) in KLAUW.items():
        assert g[y, x] == int(o, 16), ('klauw', x, y)
        g[y, x] = int(c, 16)
    for y, r in STAART:
        for i, c in enumerate(r):
            g[y, 47 + i] = 0 if c == '.' else int(c, 16)
    sil = np.array([[c == '#' for c in l.rstrip()] for l in open(os.path.join(HERE, '../silhouet_v2/direct_s1a.txt'))])
    def zone(x, y):
        return next((n for n, (x0, x1, y0, y1) in ZONES.items() if x0 <= x <= x1 and y0 <= y <= y1), None)
    diff = [(x, y) for y in range(64) for x in range(64) if (g[y, x] > 0) != sil[y, x]]
    perzone = {n: [(x, y, 'erbij' if g[y, x] else 'weg') for x, y in diff if zone(x, y) == n] for n in ZONES}
    buiten = [(x, y) for x, y in diff if zone(x, y) is None]
    lab = open(os.path.join(HERE, '../silhouet_v2/labels_s1a.txt')).read().split('\n')[1:65]
    kleur = [(x, y) for y in range(64) for x in range(64) if g[y, x] != oud[y, x] and zone(x, y) is None
             and not (x <= 13 and 13 <= y <= 20) and (x, y) not in KLAUW]
    bev = [(x, y) for y in range(64) for x in range(64) if g[y, x] != oud[y, x] and (lab[y][x] in 'ZKk' or oud[y, x] in (11, 12, 13))]
    rand = [(int(x), int(y)) for y, x in zip(*np.nonzero(g))
            if any(not (0 <= y + dy < 64 and 0 <= x + dx < 64) or g[y + dy, x + dx] == 0 for dy, dx in N4)
            and g[y, x] not in (1, 2, 4, 11, 12)]
    print(f'{naam}: silhouet per zone {perzone} | silhouet buiten zones {buiten} | kleur anders buiten neus/staart/klauwrand {kleur} | bevroren (klauw/buidel) geraakt {bev} | open randen {rand} '
          f'| gewijzigd {int((g != oud).sum())} px | losse binnenpixels {len(binnen_los(oud))} -> {len(binnen_los(g))}')
    open(os.path.join(HERE, naam + '.txt'), 'w').write(
        '\n'.join(''.join('.' if v == 0 else format(v, 'x') for v in r) for r in g) + '\n')
    im = Image.new('P', (64, 64)); im.putpalette(sum(PALET, ())); im.putdata(g.flatten().tolist())
    im.save(os.path.join(HERE, naam + '.png'), transparency=0)
    if pal:
        open(os.path.join(HERE, naam + '.pal'), 'w').write(PAL_TXT)


if __name__ == '__main__':
    maak('ronde9', 'ronde10', True)
    maak('ronde9b', 'ronde10b', False)
