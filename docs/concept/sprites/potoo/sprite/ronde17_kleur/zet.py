"""Zet een rondebestand (segmenten met de hand) om naar raster.txt en controleert de omtrek tegen basis_85.txt.
Gebruik: python3 zet.py r1.py raster.txt"""
import sys, runpy
R = runpy.run_path(sys.argv[1])['R']
B = [l.rstrip('\n') for l in open('basis_85.txt')][:64]
G = [['.']*64 for _ in range(64)]
for y, segs in R.items():
    for x, s in segs:
        for i, c in enumerate(s): G[y][x+i] = c
out = [''.join(r) for r in G]
fout = [(x, y, B[y][x], out[y][x]) for y in range(64) for x in range(64) if (B[y][x] == '.') != (out[y][x] == '.')]
print('alpha-diff met basis:', len(fout), fout[:20])
open(sys.argv[2], 'w').write('\n'.join(out) + '\n')
