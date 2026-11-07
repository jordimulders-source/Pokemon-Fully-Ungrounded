"""Controle kleur ronde 1: alpha-diff met het bevroren silhouet (uit de PNG zelf), open randen, losse pixels.
Open rand = randpixel (naast transparant, 4-buren) die geen omlijningskleur is (k, d, m, n)."""
import os
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.dirname(HERE)
SIL = [l.rstrip('\n') for l in open(os.path.join(HERE, '../../../silhouet/ronde1b.txt'))]
im = Image.open(os.path.join(OUT, 'lama.png'))
LET = '.kdsblhqrmnytpuw'
g = [[LET[im.getpixel((x, y))] for x in range(64)] for y in range(64)]
diff = sum((SIL[y][x] == '#') != (g[y][x] != '.') for y in range(64) for x in range(64))
print('mode', im.mode, 'transparency', im.info.get('transparency'), '| pixels', sum(c != '.' for r in g for c in r), '| alpha-diff', diff)
print('kleuren gebruikt:', len({c for r in g for c in r}))
OK = set('kdmn')
def at(x, y): return g[y][x] if 0 <= x < 64 and 0 <= y < 64 else '.'
open_ = [(x, y, g[y][x]) for y in range(64) for x in range(64)
         if g[y][x] != '.' and any(at(x + a, y + b) == '.' for a, b in ((1, 0), (-1, 0), (0, 1), (0, -1))) and g[y][x] not in OK]
print('open randen:', len(open_), open_)
alone = [(x, y, g[y][x]) for y in range(64) for x in range(64) if g[y][x] not in '.k'
         and all(at(x + a, y + b) != g[y][x] for a, b in ((1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (-1, -1), (1, -1), (-1, 1)))]
print('losse pixels (geen buur met dezelfde kleur):', len(alone), alone)
