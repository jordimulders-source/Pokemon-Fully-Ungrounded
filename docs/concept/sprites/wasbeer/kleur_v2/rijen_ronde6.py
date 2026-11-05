"""Kleur ronde 6 van de wasbeer (S1a), alleen de KOP (y 0-20, x 10-33): opnieuw met de hand per rij, minder korrel
(rustige vlakken, gebogen banden), neus apart (eigen tint 4 met glans 7, crème rand 9 tussen neus en masker; geen oker 8 in de kop),
wenkbrauw als boog over het nabije oog. Oog (lid, iris, glans), masker (2 lobben met brug), buidel en lijf: ronde 5.
Draaien: python3 docs/concept/sprites/wasbeer/kleur_v2/rijen_ronde6.py -> ronde6.txt, ronde6.png, ronde6.pal + controle."""
import os
import numpy as np
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, '../../../../..')
PALET = [tuple(int(v) for v in l.split()) for l in open(os.path.join(HERE, 'ronde5.pal')).read().split('\n')[3:19]]

KOP = {  # y: [(x-start, indices)]
 1: [(14, '4aaaa4'), (25, '444')],
 2: [(13, '4aaaa91'), (25, '4aa1')],
 3: [(12, '4aaa99991'), (24, '4aa991')],
 4: [(12, '49999444441'), (24, '4a9991')],
 5: [(12, '44333337777441997 71'.replace(' ', ''))],
 6: [(12, '4333337777666619771')],
 7: [(12, '4777766666666655541')],
 8: [(12, '12aa6666aaaaa666 51'.replace(' ', ''))],
 9: [(11, '12222666a22222a9651')],
 10: [(11, '1222244211112296651')],
 11: [(10, '122e222222aee2266651')],
 12: [(10, '122f222222fff2266551')],
 13: [(10, '12222222222222266551')],
 14: [(11, '12222aaaa22226666551')],
 15: [(11, '1299aaaaa22266665555')],
 16: [(11, '1744aaaaaa9976655556')],
 17: [(10, '1444aaaa9977766655556655')],
 18: [(11, '1199977776666655556655')],
 19: [(11, '11777777666666655555555')],
 20: [(13, '114444444')],
}


def lees(p):
    return np.array([[0 if c == '.' else int(c, 16) for c in l.rstrip()] for l in open(p)])


def los(g, y0, y1, x0=0, x1=64):
    n = 0
    for y in range(y0, y1):
        for x in range(x0, x1):
            v = g[y, x]
            if v == 0:
                continue
            if not any(g[y + dy, x + dx] == v for dy in (-1, 0, 1) for dx in (-1, 0, 1)
                       if (dy or dx) and 0 <= y + dy < 64 and 0 <= x + dx < 64):
                n += 1
    return n


def gen3(n):
    return np.array(Image.open(os.path.join(ROOT, f'graphics/pokemon/{n}/anim_front.png')))[:64, :64]


def main():
    g = lees(os.path.join(HERE, 'ronde5.txt')); r5 = g.copy()
    for y, segs in KOP.items():
        for x0, s in segs:
            for i, c in enumerate(s):
                assert g[y, x0 + i] != 0, ('buiten silhouet', x0 + i, y)
                g[y, x0 + i] = int(c, 16)
    sil = np.array([[c == '#' for c in l.rstrip()] for l in open(os.path.join(HERE, '../silhouet_v2/direct_s1a.txt'))])
    print('alpha-diff met direct_s1a:', int(((g > 0) != sil).sum()), '| gewijzigd t.o.v. ronde5:', int((g != r5).sum()),
          'px, buiten de kop (y > 20):', int((g[21:] != r5[21:]).sum()))
    open(os.path.join(HERE, 'ronde6.txt'), 'w').write('\n'.join(''.join('.' if v == 0 else format(v, 'x') for v in r) for r in g) + '\n')
    im = Image.new('P', (64, 64)); im.putpalette(sum(PALET, ())); im.putdata(g.flatten().tolist())
    im.save(os.path.join(HERE, 'ronde6.png'), transparency=0)
    open(os.path.join(HERE, 'ronde6.pal'), 'w').write(open(os.path.join(HERE, 'ronde5.pal')).read())
    rand = [(int(x), int(y)) for y, x in zip(*np.nonzero(g))
            if any(not (0 <= y + dy < 64 and 0 <= x + dx < 64) or g[y + dy, x + dx] == 0 for dy, dx in ((0, 1), (0, -1), (1, 0), (-1, 0)))
            and g[y, x] not in (1, 2, 4, 11, 12)]
    print('randpixels niet 1/2/4/b/c:', rand)
    print('losse pixels in de kop (geen 8-buur met dezelfde index): ronde5', los(r5, 0, 21, 9, 34), '| ronde6', los(g, 0, 21, 9, 34))
    for n, box in (('zigzagoon', (26, 50, 4, 30)), ('linoone', (24, 46, 2, 28)), ('teddiursa', (8, 32, 22, 48)), ('zangoose', (6, 30, 14, 36))):
        a = gen3(n); y0, y1, x0, x1 = box
        print(f'  {n} kop (y {y0}-{y1}, x {x0}-{x1}):', los(a, y0, y1, x0, x1), 'losse pixels')


if __name__ == '__main__':
    main()
