"""Bouwt raster.txt uit rijen_r7.txt (met de hand geschreven: 'y x: tekst [tekst] x: tekst'; spaties in de tekst zijn
alleen voor de leesbaarheid) en meet de alpha-diff tegen silhouet r2."""
g = [['.'] * 64 for _ in range(64)]
for l in open('rijen_r7.txt'):
    p = l.split()
    if not p: continue
    y = int(p[0]); x = None
    for t in p[1:]:
        if t.endswith(':'): x = int(t[:-1]); continue
        for c in t: g[y][x] = c; x += 1
open('raster.txt', 'w').write('\n'.join(''.join(r) for r in g) + '\n')
s = [l.rstrip('\n') for l in open('../kleur_r6/raster.txt')][:64]
bad = [(x, y) for y in range(64) for x in range(64) if (s[y][x] != '.') != (g[y][x] != '.')]
print('alpha-diff', len(bad), sorted(bad, key=lambda p: (p[1], p[0])))
