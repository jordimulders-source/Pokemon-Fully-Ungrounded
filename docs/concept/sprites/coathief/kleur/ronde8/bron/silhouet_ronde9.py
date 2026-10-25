"""Silhouet ronde 9: het silhouet volgt de overgetrokken sprite (ronde 8). Buiten de voorpootzone gelijk aan ronde 8;
binnen x 10-34, y 50-63 komt het uit de pixel-over van de onderlaag. Schrijft silhouet/ronde9.txt."""
import os, sys
H = os.path.dirname(os.path.abspath(__file__)); S = os.path.join(H, '../../../silhouet'); sys.path.insert(0, H)
import bouw
g, f = bouw.lees()
for ln in open(os.path.join(H, 'reparaties.txt')):
    ln = ln.split('#')[0].strip()
    if not ln: continue
    y, x0, px = ln.split(); y = int(y); x0 = int(x0)
    for i, ch in enumerate(px): g[y][x0 + i] = ch
oud = [l.rstrip('\n') for l in open(os.path.join(S, 'ronde8.txt')) if l.strip()]
new = [''.join('#' if g[y][x] != '.' else '.' for x in range(64)) for y in range(64)]
buiten = [(x, y) for y in range(64) for x in range(64) if (oud[y][x] != new[y][x]) and not (10 <= x <= 34 and 50 <= y <= 63)]
assert not buiten, buiten
erbij = sum(1 for y in range(64) for x in range(64) if new[y][x] == '#' and oud[y][x] != '#')
eraf = sum(1 for y in range(64) for x in range(64) if new[y][x] != '#' and oud[y][x] == '#')
open(os.path.join(S, 'ronde9.txt'), 'w').write('\n'.join(new) + '\n')
print('ronde9.txt: %d px (+%d, -%d ten opzichte van ronde8)' % (sum(r.count('#') for r in new), erbij, eraf))
