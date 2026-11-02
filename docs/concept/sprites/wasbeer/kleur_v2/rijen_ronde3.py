"""Kleur ronde 3 van de wasbeer (S1a): ronde2.txt + de punten uit KEURING_ronde1.md die in ronde 2 nog niet slaagden,
met de hand als expliciete pixels (x, y): index, per zone. Palet = ronde 2.
Draaien: python3 docs/concept/sprites/wasbeer/kleur_v2/rijen_ronde3.py -> ronde3.txt, ronde3.png, ronde3.pal + controle."""
import os
import numpy as np
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__))
PALET = [tuple(int(v) for v in l.split()) for l in open(os.path.join(HERE, 'ronde2.pal')).read().split('\n')[3:19]]


def rij(y, x0, s):
    return {(x0 + i, y): c for i, c in enumerate(s)}


Z = {}
# Nabije klauw: 2 klauwen (x 22-23 en 25-26), elk links 9 (licht) / rechts 8 (schaduw), bovenkant a,
# donkere omlijning 1 aan de schaduwkant (rechts x 27, onder y 34), inkeping 1 alleen bij de punt (24, 32-33).
Z['nabije klauw'] = {**rij(26, 23, '9aaaa8'), **rij(27, 22, '9aaaa98'), **rij(28, 22, 'a99a98'),
                     **rij(29, 22, '98898'), (27, 29): '1', **rij(30, 22, '98898'), (27, 30): '1',
                     **rij(31, 22, '98898'), (27, 31): '1', **rij(32, 22, '98198'), (27, 32): '4',
                     **rij(33, 22, '98198'), **rij(34, 22, '11911')}
# Nabije onderarm (donkere buis: glans 4 boven, 2 midden, 1 onder) + bovenarm in vachtgrijs vanuit de schouder
# (omlijning 4 voor, 7 licht, 6 basis, 5 schaduw, kernschaduw 4 naar de rug).
Z['onderarm'] = {**rij(26, 29, '4444'), **rij(27, 29, '4444'), **rij(28, 28, '244422'), **rij(29, 28, '222222'),
                 **rij(30, 28, '222222'), (34, 30): '1', **rij(31, 28, '22222'), (33, 31): '1', (34, 31): '1',
                 **rij(32, 28, '12222'), (33, 32): '1'}
Z['bovenarm'] = {**rij(21, 30, '47654'), **rij(22, 30, '47654'), **rij(23, 31, '47654'), **rij(24, 31, '47654'),
                 **rij(25, 32, '4764'), **rij(26, 33, '4764'), **rij(27, 33, '4764'), **rij(28, 34, '654'),
                 **rij(29, 34, '5554'), **rij(30, 35, '554'), **rij(31, 35, '554'), **rij(32, 34, '55554'),
                 **rij(33, 34, '555455')}
# Buidel: zakmond als opening (3 breed, 2 hoog: 1 boven, 2 onder) met lichte bovenlip d en lichte onderlip d;
# plooi = lichte rug d linksboven + schaduw b rechtsonder (vouw, geen lijn).
Z['buidel'] = {**rij(16, 33, '1bdbb1'), **rij(17, 34, 'bddd1'), **rij(18, 34, 'bd1111'), **rij(19, 34, 'b12221c1'),
               **rij(20, 35, 'bdddccd1'), **rij(21, 35, 'bddccccb1'),
               **rij(25, 36, 'bddbccccbb1'), **rij(26, 37, 'bcdbcccbb1'), **rij(27, 37, 'bccdbccbb1'),
               **rij(28, 37, 'bcccdbcbb1'), **rij(29, 38, 'bcccdbbb1')}
# Staart: haakkop met licht (4/8) op de bovenkant en kernschaduw 1 aan de rechterkant; ringen gebogen (midden hoger
# dan de randen) met licht links (a/9) en schaduw rechts (8).
Z['staart'] = {**rij(19, 50, '1448841'), **rij(20, 49, '14844221'), **rij(21, 49, '14422211'),
               **rij(22, 49, '142222211'), **rij(23, 48, '1411222211'), **rij(24, 48, '1442222211'),
               **rij(25, 48, '1442222211'), **rij(26, 48, '1442222211'), **rij(27, 48, '1422222211'),
               **rij(28, 49, '142222211'), **rij(29, 49, '122222211'),
               **rij(30, 50, '129a9821'), **rij(31, 50, '49a99881'), **rij(32, 50, '49999881'),
               **rij(33, 49, '498222881'), **rij(34, 48, '142222221'), **rij(35, 48, '142222211'),
               **rij(36, 47, '1422222221'), **rij(37, 46, '1429992221'), **rij(38, 45, '12a99998221')}
# Volume: groter hooglicht op kop en schouder/borst, kernschaduw 4 aan de schaduwkant van de kop
Z['volume'] = {**rij(5, 14, '33333'), **rij(6, 14, '3333'), **rij(7, 13, '777'),
               **rij(9, 27, '54'), **rij(10, 27, '54'), **rij(11, 27, '54'), **rij(12, 27, '54'), **rij(13, 27, '54'),
               **rij(21, 16, '33333'), **rij(22, 16, '33337'), **rij(23, 16, '3377'), **rij(24, 16, '377'),
               **rij(25, 16, '37')}
# Oogkas: geen wal meer onder het nabije oog (terug naar masker 2)
Z['oog'] = {(20, 13): '2', (21, 13): '2', (22, 13): '2', (23, 11): '2', (23, 12): '2'}


def lees(p):
    return np.array([[0 if c == '.' else int(c, 16) for c in l.rstrip()] for l in open(p)])


def main():
    g = lees(os.path.join(HERE, 'ronde2.txt')); r2 = g.copy()
    for n, d in Z.items():
        for (x, y), c in d.items():
            assert g[y, x] != 0, ('buiten silhouet', n, x, y)
            g[y, x] = int(c, 16)
    sil = np.array([[c == '#' for c in l.rstrip()] for l in open(os.path.join(HERE, '../silhouet_v2/direct_s1a.txt'))])
    print('alpha-diff met direct_s1a:', int(((g > 0) != sil).sum()), '| gewijzigd t.o.v. ronde2:', int((g != r2).sum()), 'px')
    open(os.path.join(HERE, 'ronde3.txt'), 'w').write('\n'.join(''.join('.' if v == 0 else format(v, 'x') for v in r) for r in g) + '\n')
    im = Image.new('P', (64, 64)); im.putpalette(sum(PALET, ())); im.putdata(g.flatten().tolist())
    im.save(os.path.join(HERE, 'ronde3.png'), transparency=0)
    open(os.path.join(HERE, 'ronde3.pal'), 'w').write(open(os.path.join(HERE, 'ronde2.pal')).read())
    rand = [(int(x), int(y), format(g[y, x], 'x')) for y, x in zip(*np.nonzero(g))
            if any(not (0 <= y + dy < 64 and 0 <= x + dx < 64) or g[y + dy, x + dx] == 0 for dy, dx in ((0, 1), (0, -1), (1, 0), (-1, 0)))
            and g[y, x] not in (1, 2, 4, 11, 12)]
    print('randpixels niet 1/2/4/b/c:', rand)


if __name__ == '__main__':
    main()
