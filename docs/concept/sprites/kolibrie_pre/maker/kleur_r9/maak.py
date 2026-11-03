"""Bouwt r9 uit rijen_r9.txt; meet alpha-diff tegen r7b (totaal en in de bekzone x<=16, y12-21) en bewijst dat het oog bevroren is."""
import palet
g = [['.'] * 64 for _ in range(64)]
for l in open('rijen_r9.txt'):
    p = l.split()
    if not p: continue
    y = int(p[0]); x = None
    for t in p[1:]:
        if t.endswith(':'): x = int(t[:-1]); continue
        for c in t: g[y][x] = c; x += 1
g = [''.join(r) for r in g]
open('raster.txt', 'w').write('\n'.join(g) + '\n')
palet.build('raster.txt', 'kolibrie_pre.png')
r7b = [l.rstrip('\n') for l in open('../kleur_r7/raster_r7b.txt')][:64]
alpha = [(x, y) for y in range(64) for x in range(64) if (r7b[y][x] != '.') != (g[y][x] != '.')]
bek = [(x, y) for x, y in alpha if x <= 16 and 12 <= y <= 21]
OOG = [(x, y) for y in range(14, 19) for x in range(21, 26) if (x, y) not in ((21, 14), (25, 14), (21, 18), (25, 18))]
print('alpha-diff tegen r7b:', len(alpha), alpha)
print('waarvan in de bekzone (x<=16, y12-21):', len(bek), bek)
print('oogpixels anders dan r7b:', sum(r7b[y][x] != g[y][x] for x, y in OOG), '| px', sum(c != '.' for r in g for c in r))
