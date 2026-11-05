"""Derde pas (met de hand gekozen pixels): losse vachtpixels opruimen en de omlijning van het achterwerk boven (r30-33) en de rugrand
rechts naar d (overgang zwart -> omlijningsbasis), zodat zwart <= 10% blijft."""
import os
HERE = os.path.dirname(os.path.abspath(__file__))
FIX = {(18, 21): ('b', 's'), (51, 27): ('b', 'l'), (46, 32): ('b', 'l'), (27, 33): ('b', 'l'), (29, 33): ('s', 'b'), (29, 41): ('b', 'l'),
       (31, 25): ('k', 'd'), (51, 34): ('k', 'd'), (51, 30): ('k', 'd'), (52, 31): ('k', 'd'), (53, 32): ('k', 'd'), (53, 33): ('k', 'd')}
L = open(os.path.join(HERE, 'raster.txt')).read().split('\n')
for i, l in enumerate(L):
    p = l.split()
    if len(p) == 3 and p[0].isdigit():
        y, x0, s = int(p[0]), int(p[1]), list(p[2])
        for j in range(len(s)):
            if (x0 + j, y) in FIX:
                a, b = FIX.pop((x0 + j, y)); assert s[j] == a, ((x0 + j, y), s[j], a); s[j] = b
        L[i] = f'{y} {x0} {"".join(s)}'
assert not FIX, FIX
open(os.path.join(HERE, 'raster.txt'), 'w').write('\n'.join(L)); print('ok')
