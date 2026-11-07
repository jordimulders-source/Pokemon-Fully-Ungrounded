"""Controle van ../coathief.png: alpha-diff met het bevroren silhouet, open randen per kleurgroep, losse pixels."""
import os
from PIL import Image
H = os.path.dirname(os.path.abspath(__file__))
im = Image.open(os.path.join(H, '../coathief.png'))
assert im.mode == 'P' and im.size == (64, 64)
from bouw import ORDER
px = im.load(); g = [[ORDER[px[x, y]] for x in range(64)] for y in range(64)]
sil = [l.rstrip('\n') for l in open(os.path.join(H, '../../../silhouet/ronde1.txt')) if l.strip()]
diff = [(x, y) for y in range(64) for x in range(64) if (g[y][x] != '.') != (sil[y][x] == '#')]
print('pixels', sum(c != '.' for r in g for c in r), '| silhouet', sum(r.count('#') for r in sil), '| alpha-diff', len(diff))
print('kleuren gebruikt:', len({c for r in g for c in r} - {'.'}), '| transparency =', im.info.get('transparency'))
GROEP = {'d': 'b', 'b': 'b', 'l': 'b', 'h': 'b', 'k': 'k', 'm': 'z', 'z': 'z', 'y': 'z', 'Y': 'z',
         'n': 'c', 'x': 'c', 'c': 'c', 'w': 'c', 'r': 'o', 'i': 'o'}
OK = {'b': 'dk', 'z': 'mk', 'c': 'xk', 'k': 'k', 'o': ''}
# klauwen (1-2 px breed): schaduwtint n aan de buitenrand mag (geen c/w) - keuring ronde 2
KLAUW = lambda x, y: y >= 56 and x <= 23
N4 = ((1, 0), (-1, 0), (0, 1), (0, -1))
def t(x, y): return not (0 <= x < 64 and 0 <= y < 64) or g[y][x] == '.'
open_ = [(x, y, g[y][x]) for y in range(64) for x in range(64) if g[y][x] != '.'
         and any(t(x + a, y + b) for a, b in N4) and g[y][x] not in OK[GROEP[g[y][x]]] and not (KLAUW(x, y) and g[y][x] == 'n')]
print('open randen:', len(open_), open_)
los = [(x, y) for y in range(64) for x in range(64) if g[y][x] != '.' and all(t(x + a, y + b) for a, b in N4)]
print('losse pixels (zonder buren):', len(los), los)
