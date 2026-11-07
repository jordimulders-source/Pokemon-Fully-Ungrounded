"""Bouwt r8 (kapgrens zoals r7b) en de varianten hoger/lager, meet de alpha-diff tegen r7b en bewijst dat het oog bevroren is."""
import palet
def lees(fn):
    g = [['.'] * 64 for _ in range(64)]
    for l in open(fn):
        p = l.split()
        if not p: continue
        y = int(p[0]); x = None
        for t in p[1:]:
            if t.endswith(':'): x = int(t[:-1]); continue
            for c in t: g[y][x] = c; x += 1
    return [''.join(r) for r in g]
r7b = [l.rstrip('\n') for l in open('../kleur_r7/raster_r7b.txt')][:64]
OOG = [(x, y) for y in range(14, 19) for x in range(21, 26) if (x, y) not in ((21, 14), (25, 14), (21, 18), (25, 18))]
for naam, fn, uit in (('r8', 'rijen_r8.txt', 'raster.txt'), ('hoger', 'rijen_r8_hoger.txt', 'raster_hoger.txt'), ('lager', 'rijen_r8_lager.txt', 'raster_lager.txt')):
    g = lees(fn); open(uit, 'w').write('\n'.join(g) + '\n')
    png = 'kolibrie_pre.png' if naam == 'r8' else f'kolibrie_pre_{naam}.png'
    palet.build(uit, png)
    alpha = [(x, y) for y in range(64) for x in range(64) if (r7b[y][x] != '.') != (g[y][x] != '.')]
    oog = sum(r7b[y][x] != g[y][x] for x, y in OOG)
    print(naam, 'alpha-diff tegen r7b', len(alpha), alpha, '| oogpixels anders dan r7b:', oog, '| px', sum(c != '.' for r in g for c in r))
