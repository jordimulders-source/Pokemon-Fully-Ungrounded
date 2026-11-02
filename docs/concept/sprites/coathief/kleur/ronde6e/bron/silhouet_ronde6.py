"""Silhouet ronde 6 = ronde 5 + 2 px: de manchet van de opgetilde poot loopt, zoals de omlijning van de onderlaag,
via (26,55) en (26,56) in een ruime boog naar de onderkant (24-26,56). Jordi's krabbel gaf de richting;
de onderlaag is de maatstaf (geen extra pixels op (32,48-49) en (25,57): daar ligt de onderlaaglijn niet)."""
import os
H = os.path.dirname(os.path.abspath(__file__)); S = os.path.join(H, '../../../silhouet')
sil = [list(l.rstrip('\n')) for l in open(os.path.join(S, 'ronde5.txt')) if l.strip()]
ERBIJ = [(26, 55), (26, 56)]
for x, y in ERBIJ:
    assert sil[y][x] == '.'; sil[y][x] = '#'
open(os.path.join(S, 'ronde6.txt'), 'w').write('\n'.join(''.join(r) for r in sil) + '\n')
print('ronde6.txt:', sum(r.count('#') for r in sil), 'px (+%d)' % len(ERBIJ))
