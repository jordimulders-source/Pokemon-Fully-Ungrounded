"""leg.py spec.txt [uit.txt]: legt een handraster ("y: x=pixels", alleen de gewijzigde stukken) over ../kleur_r2/raster.txt.
Weigert alpha-wijzigingen en wijzigingen aan de ogen. Alleen raster->raster; het inkleuren zelf is handwerk in de spec."""
import sys, os
H = os.path.dirname(os.path.abspath(__file__)); K = os.path.dirname(H)
R = [list(l.rstrip('\n')) for l in open(os.path.join(K, '..', 'kleur_r2', 'raster.txt'))][:64]
OGEN = {(10, 55), (10, 56), (16, 55), (17, 55), (16, 56), (17, 56)}
n = 0
for l in open(sys.argv[1]):
    if l.startswith('#') or not l.strip(): continue
    y, rest = l.split(':', 1); y = int(y)
    for t in rest.split():
        x0, s = t.split('='); x0 = int(x0)
        for k, c in enumerate(s):
            x = x0 + k
            assert R[y][x] != '.' and c != '.', f'alpha geraakt op {(x, y)}'
            assert (x, y) not in OGEN, f'oog geraakt op {(x, y)}'
            if R[y][x] != c: n += 1
            R[y][x] = c
uit = sys.argv[2] if len(sys.argv) > 2 else os.path.join(K, 'raster.txt')
open(uit, 'w').write('\n'.join(''.join(r) for r in R) + '\n'); print('gewijzigde pixels:', n)
