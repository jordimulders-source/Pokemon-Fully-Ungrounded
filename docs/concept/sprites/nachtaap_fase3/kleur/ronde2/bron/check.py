# Controle ronde 2: alpha-diff, bevroren zones, open randen, losse pixels.
import os
H = os.path.dirname(os.path.abspath(__file__))
a = open(os.path.join(H, 'basis_1s.txt')).read().split('\n')[:64]
b = open(os.path.join(H, 'ronde2.txt')).read().split('\n')[:64]
N4 = ((1, 0), (-1, 0), (0, 1), (0, -1))
def at(g, y, x): return g[y][x] if 0 <= y < 64 and 0 <= x < 64 else '.'
alpha = [(y, x) for y in range(64) for x in range(64) if (a[y][x] == '.') != (b[y][x] == '.')]
print('alpha-diff:', len(alpha), alpha)
# bevroren: gezicht/ogen/snuit (6-9, A-C), maan + neus/oogglans (D/E/F boven rij 47), gloed (A/B/C),
# zwart binnen het gezicht (rij 35-46, kol 4-13), staart (kol >= 49 rij 22-41, plus kol 45-48 rij 22-34), voet onderbeen (7)
frozen = []
for y in range(64):
    for x in range(64):
        c = a[y][x]
        f = c in '6789ABC' or (c in 'DEF' and y <= 46) \
            or (c == '1' and 35 <= y <= 46 and 4 <= x <= 13) \
            or (22 <= y <= 41 and x >= 49) or (22 <= y <= 34 and 45 <= x <= 48)
        if f: frozen.append((y, x))
fd = [(y, x, a[y][x], b[y][x]) for y, x in frozen if a[y][x] != b[y][x]]
print('bevroren pixels:', len(frozen), 'diff:', len(fd), fd)
# handomtrek: handpixels (D/E/F/1/2 in rij 46-60, kol 6-21) met een 8-buur in de gloed of transparant
omtrek = []
for y in range(46, 61):
    for x in range(6, 22):
        if a[y][x] in 'DEF12':
            if any(at(a, y + dy, x + dx) in '.ABC' for dy in (-1, 0, 1) for dx in (-1, 0, 1)):
                omtrek.append((y, x))
od = [(y, x, a[y][x], b[y][x]) for y, x in omtrek if a[y][x] != b[y][x]]
print('handomtrek:', len(omtrek), 'diff:', len(od), od)
# open randen: vacht/palm-binnentint naast transparant
open_ = [(y, x, b[y][x]) for y in range(64) for x in range(64)
         if b[y][x] in '345DEF' and any(at(b, y + dy, x + dx) == '.' for dy, dx in N4)]
print('open randen:', len(open_), open_)
# losse pixels: vachttint (3/4/5) waarvan geen enkele 4-buur dezelfde index heeft
losse = [(y, x, b[y][x]) for y in range(64) for x in range(64)
         if b[y][x] in '345' and all(at(b, y + dy, x + dx) != b[y][x] for dy, dx in N4)]
print('losse vachtpixels:', len(losse), losse)
lp = [(y, x, b[y][x]) for y in range(46, 61) for x in range(6, 22)
      if b[y][x] in 'DEF' and all(at(b, y + dy, x + dx) != b[y][x] for dy, dx in N4)]
print('losse palmpixels:', len(lp), lp)
ch = sum(1 for y in range(64) for x in range(64) if a[y][x] != b[y][x])
print('gewijzigde pixels t.o.v. 1s:', ch)
from collections import Counter
print('telling:', sorted(Counter(''.join(b)).items()))
