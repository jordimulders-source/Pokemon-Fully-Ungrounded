"""Controles: alpha-diff tegen silhouet r2, open randen (niet-omlijningskleur naast transparant), losse pixels
(een kleur die geen enkele 4-buur van dezelfde kleur heeft, behalve bewuste accenten), kleurgebruik."""
from collections import Counter
g = [l.rstrip('\n') for l in open('raster.txt')][:64]
s = [l.rstrip('\n') for l in open('../silhouet_r2/silhouet.txt')][:64]
print('alpha-diff tegen silhouet r2:', sum((s[y][x] == '#') != (g[y][x] != '.') for y in range(64) for x in range(64)))
RAND = set('123') | set('CDA')   # omlijning: 1/2/3 (lila), snavel A, mondhoek C/D (gele rand van de gaap)
open_r = []
for y in range(64):
    for x in range(64):
        c = g[y][x]
        if c == '.': continue
        nb = [g[y + dy][x + dx] if 0 <= y + dy < 64 and 0 <= x + dx < 64 else '.' for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))]
        if '.' in nb and c not in RAND: open_r.append((x, y, c))
print('open randen:', open_r)
los = []
for y in range(64):
    for x in range(64):
        c = g[y][x]
        if c == '.': continue
        nb = [g[y + dy][x + dx] if 0 <= y + dy < 64 and 0 <= x + dx < 64 else '.' for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (-1, -1), (1, -1), (-1, 1))]
        if c not in nb: los.append((x, y, c))
print('losse pixels (geen buur in dezelfde kleur, 8-buren):', los)
print('kleurgebruik:', sorted(Counter(c for r in g for c in r if c != '.').items()))
