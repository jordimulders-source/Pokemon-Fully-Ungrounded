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
ZONE = (3, 11, 13, 20)  # x0, x1, y0, y1 (incl.) waar het silhouet mag veranderen
# (x, y): (oud, nieuw); '.' = transparant
NEUS = {
    (10, 16): ('.', '1'), (11, 16): ('2', '7'), (12, 16): ('7', '2'), (13, 16): ('2', '2'),
    (9, 17): ('.', '1'), (10, 17): ('1', '2'), (11, 17): ('2', '2'), (12, 17): ('2', '2'), (13, 17): ('4', '4'),
    (10, 18): ('.', '1'), (11, 18): ('1', '2'), (12, 18): ('9', '4'),
}


def maak(bron, naam, pal):
    g = lees(os.path.join(HERE, bron + '.txt'))
    oud = g.copy()
    for (x, y), (o, c) in NEUS.items():
        assert g[y, x] == (0 if o == '.' else int(o, 16)), (x, y)
        g[y, x] = 0 if c == '.' else int(c, 16)
    sil = np.array([[c == '#' for c in l.rstrip()] for l in open(os.path.join(HERE, '../silhouet_v2/direct_s1a.txt'))])
    x0, x1, y0, y1 = ZONE
    diff = [(x, y) for y in range(64) for x in range(64) if (g[y, x] > 0) != sil[y, x]]
    buiten = [(x, y) for x, y in diff if not (x0 <= x <= x1 and y0 <= y <= y1)]
    kleur = [(x, y) for y in range(64) for x in range(64) if g[y, x] != oud[y, x] and not (x0 <= x <= x1 + 2 and y0 <= y <= y1)]
    rand = [(int(x), int(y)) for y, x in zip(*np.nonzero(g))
            if any(not (0 <= y + dy < 64 and 0 <= x + dx < 64) or g[y + dy, x + dx] == 0 for dy, dx in N4)
            and g[y, x] not in (1, 2, 4, 11, 12)]
    print(f'{naam}: silhouet anders {diff} | buiten zone {buiten} | kleur anders buiten neus {kleur} | open randen {rand} '
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
