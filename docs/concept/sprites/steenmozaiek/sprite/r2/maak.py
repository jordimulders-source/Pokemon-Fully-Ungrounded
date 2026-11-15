# r2: scriptreductie -> kop (j11-24) uit kop.py + handreparaties -> r1-reparaties onder de kop -> losse voegpixels weg
import sys, numpy as np
OUT = sys.argv[1]  # vóór kop.py: die zet sys.argv om
assert OUT.endswith('.txt')
exec(open('kop.py').read().split("if __name__")[0])
rows = [list(l.rstrip('\n')) for l in open('scriptreductie.txt')]
base = [r[:] for r in rows]
# 1. kop: meerderheidstint van het model, lichtste tint bij gelijkspel, geen voegen in de kop
for j in range(11, 25):
    for i in range(3, 25):
        if rows[j][i] in '.k': continue
        v = kopcel(j, i)
        if v: rows[j][i] = v
# 2. met de hand in de kop (zelfde metingen als r1, zie ../r1/edits.py)
H = [
 (15, 8, 'c', 'lichtste lila (was als tandwit gelezen)'), (16, 7, 'c', 'idem'),
 (15, 14, 'g', 'oogglans x29 y31'), (15, 15, 'k', 'oog'), (15, 16, 'k', 'oog'),
 (16, 14, 'k', 'oog'), (16, 15, 'k', 'oog'), (16, 16, 'k', 'oog'),
 (16, 12, 'b', 'lila naast het oog, model bs/rr'), (16, 13, 'c', 'lila naast het oog, model cs/rs'),
 (17, 15, 'c', 'lila onder het oog (oog vrij in het lila; model ##/ss)'), (17, 14, 'R', 'rood stuk, model r#/Rr'),
 (17, 6, 'g', 'glans op de zwarte neus, model x12-14 y34-35'),
 (21, 7, 'w', 'basis linker hoektand'), (21, 8, 'k', 'lippenlijn'), (21, 9, 'k', 'lippenlijn'), (21, 10, 'k', 'lippenlijn'), (21, 11, 'k', 'lippenlijn'),
 (22, 6, 'w', 'linker hoektand'), (22, 10, 'w', 'rechter hoektand'), (22, 11, 'w', 'rechter hoektand'), (22, 13, 'r', 'muil'),
 (23, 10, 'w', 'rechter hoektand'), (23, 11, 'w', 'rechter hoektand'),
 (24, 10, 'r', 'muil'), (24, 11, 'c', 'punt rechter hoektand'),
]
for j, i, c, _ in H: rows[j][i] = c
# 3. r1-reparaties onder de kop (muil, onderkaak, staartpunt, voorpoot, achterpoot)
sys.path.insert(0, '.')
from edits import E
for j, i, c, _ in E:
    if j >= 25 or i >= 44: rows[j][i] = c
# 4. losse voegpixels (geen andere lijn/zwart als 4-buur) nemen de buurtint aan
SEAM = 'dq'; DARK = 'dqkxg.'
for it in range(2):
    for j in range(1, 65):
        for i in range(1, 65):
            if rows[j][i] not in SEAM or j <= 24 and i < 25: continue
            nb = [rows[j-1][i], rows[j+1][i], rows[j][i-1], rows[j][i+1]]
            if any(n in 'dqkx' for n in nb): continue
            fill = [n for n in nb if n not in DARK]
            if fill: rows[j][i] = max(set(fill), key=fill.count)
open(OUT, 'w').write(''.join(''.join(r) + '\n' for r in rows))
print('gewijzigd t.o.v. scriptreductie:', sum(a != b for ra, rb in zip(base, rows) for a, b in zip(ra, rb)))
