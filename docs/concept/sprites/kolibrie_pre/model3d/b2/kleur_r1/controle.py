"""Controle kleur r1: alpha-diff met silhouet r1, randkleuren (open randen), losse pixels."""
import os, numpy as np
from PIL import Image
D = os.path.dirname(os.path.abspath(__file__))
sil = np.array([[c == '#' for c in r] for r in open(os.path.join(D, '..', 'silhouet_r1', 'silhouet.txt')).read().split()])
a = np.array(Image.open(os.path.join(D, 'kolibrie_pre.png')))
R = [l.rstrip('\n') for l in open(os.path.join(D, 'raster.txt'))][:64]
m = a != 0
print('alpha-diff met silhouet r1:', int((m ^ sil).sum()), '| px', int(m.sum()), '| kleuren', sorted(set(''.join(R)) - {'.'}))
p = np.pad(m, 1)
rand = m & ~(p[:-2, 1:-1] & p[2:, 1:-1] & p[1:-1, :-2] & p[1:-1, 2:])
CH = '.123456789ABCDEF'
OK_RAND = set('12') | set('3')          # 3 = gekleurde selout op de lichte borstrand
DUN = set('FDCA')                       # pseudo-omlijning op dunne delen (snavel 2 px, pootjes)
open_r = [(x, y, R[y][x]) for y in range(64) for x in range(64) if rand[y, x] and R[y][x] not in OK_RAND | DUN]
print('open randen:', open_r or 'geen')
print('dunne delen met pseudo-omlijning:', sorted({R[y][x] for y in range(64) for x in range(64) if rand[y, x] and R[y][x] in DUN}))
los = []
for y in range(64):
    for x in range(64):
        c = R[y][x]
        if c == '.': continue
        nb = [R[y+dy][x+dx] for dy, dx in ((-1,0),(1,0),(0,-1),(0,1),(-1,-1),(-1,1),(1,-1),(1,1))]
        if c not in nb: los.append((x, y, c))
print('losse pixels (geen buur, ook diagonaal, met dezelfde kleur):', los or 'geen')
