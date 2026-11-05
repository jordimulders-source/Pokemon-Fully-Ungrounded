"""Kleur ronde 7 van de wasbeer (S1a), alleen de kop: exact R1-R5 uit KEURING_ronde6.md, als (x, y): (oud, nieuw).
Draaien: python3 docs/concept/sprites/wasbeer/kleur_v2/rijen_ronde7.py -> ronde7.txt, ronde7.png, ronde7.pal + controle."""
import os, sys
import numpy as np
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from rijen_ronde6 import los, lees  # noqa: E402
PALET = [tuple(int(v) for v in l.split()) for l in open(os.path.join(HERE, 'ronde6.pal')).read().split('\n')[3:19]]
R = {'R1 wenkbrauw als sikkel': {(21, 7): ('6', 'a'), (22, 7): ('6', 'a'), (23, 7): ('6', 'a'), (24, 9): ('2', 'a')},
     'R2': {(12, 15): ('2', '9')}, 'R3': {(12, 18): ('1', '9')}, 'R4': {(24, 13): ('2', '6')},
     'R5': {(17, 13): ('2', 'a'), (18, 13): ('2', 'a')}}


def main():
    g = lees(os.path.join(HERE, 'ronde6.txt')); r6 = g.copy()
    for n, d in R.items():
        for (x, y), (o, c) in d.items():
            assert g[y, x] == int(o, 16), (n, x, y)
            g[y, x] = int(c, 16)
    sil = np.array([[c == '#' for c in l.rstrip()] for l in open(os.path.join(HERE, '../silhouet_v2/direct_s1a.txt'))])
    print('alpha-diff:', int(((g > 0) != sil).sum()), '| gewijzigd t.o.v. ronde6:', int((g != r6).sum()), 'px')
    open(os.path.join(HERE, 'ronde7.txt'), 'w').write('\n'.join(''.join('.' if v == 0 else format(v, 'x') for v in r) for r in g) + '\n')
    im = Image.new('P', (64, 64)); im.putpalette(sum(PALET, ())); im.putdata(g.flatten().tolist())
    im.save(os.path.join(HERE, 'ronde7.png'), transparency=0)
    open(os.path.join(HERE, 'ronde7.pal'), 'w').write(open(os.path.join(HERE, 'ronde6.pal')).read())
    rand = [(int(x), int(y)) for y, x in zip(*np.nonzero(g))
            if any(not (0 <= y + dy < 64 and 0 <= x + dx < 64) or g[y + dy, x + dx] == 0 for dy, dx in ((0, 1), (0, -1), (1, 0), (-1, 0)))
            and g[y, x] not in (1, 2, 4, 11, 12)]
    print('randpixels niet 1/2/4/b/c:', rand)
    print('losse pixels in de kop: ronde6', los(r6, 0, 21, 9, 34), '| ronde7', los(g, 0, 21, 9, 34))


if __name__ == '__main__':
    main()
