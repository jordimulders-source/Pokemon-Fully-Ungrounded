"""Controle sprite r3: lichte kleur op de buitenrand (open randen), losse pixels, alleen-diagonaal verbonden pixels,
tintclusters < 3 px (8-verbonden; omlijning k/4 en oog/glans uitgezonderd), kleurtelling, afwijking van de r5-massa.
Uitvoer: controle_uitvoer.txt. Draaien: python3.11 controle.py"""
import numpy as np
from PIL import Image
from palet import lees, PAL
R = lees('raster.txt')
massa = np.asarray(Image.open('bron/bron_kleur_1x.png'))[..., 3] > 0
out = []
def nb8(x, y): return [(x+i, y+j) for i in (-1,0,1) for j in (-1,0,1) if (i or j) and 0 <= x+i < 64 and 0 <= y+j < 64]
def nb4(x, y): return [(x+dx, y+dy) for dx, dy in ((1,0),(-1,0),(0,1),(0,-1)) if 0 <= x+dx < 64 and 0 <= y+dy < 64]
LICHT = set('a b 1 y w c 2'.split())
OOG = [(x, y) for x in range(20, 24) for y in range(5, 9)] + [(14, 6), (15, 5), (15, 6), (15, 7)]
rand = [(x, y, R[y][x]) for y in range(64) for x in range(64) if R[y][x] != '.' and any(R[b][a] == '.' for a, b in nb4(x, y)) or
        (R[y][x] != '.' and (x in (0, 63) or y in (0, 63)))]
licht = [r for r in rand if r[2] in LICHT and r[2] != '2']
out.append(f'lichte kleur (a/b/1/y/w/c) op de buitenrand: {len(licht)} {licht}')
sel = {}
for r in rand:
    if r[2] not in 'k': sel[r[2]] = sel.get(r[2], 0) + 1
out.append(f'gekleurde selout op de rand (telling per kleur, k = zwart niet geteld): {sel}')
los = [(x, y) for y in range(64) for x in range(64) if R[y][x] != '.' and all(R[b][a] == '.' for a, b in nb8(x, y))]
out.append(f'losse pixels: {len(los)} {los}')
diag = [(x, y) for y in range(64) for x in range(64) if R[y][x] != '.' and all(R[b][a] == '.' for a, b in nb4(x, y))]
out.append(f'alleen diagonaal verbonden (1px-lijnen van oor en haak tellen hier mee): {len(diag)} {diag}')
seen = set(); klein = []
for y in range(64):
    for x in range(64):
        c = R[y][x]
        if c in '.k4' or (x, y) in seen: continue
        st = [(x, y)]; comp = []; seen.add((x, y))
        while st:
            p = st.pop(); comp.append(p)
            for q in nb8(*p):
                if q not in seen and R[q[1]][q[0]] == c: seen.add(q); st.append(q)
        if len(comp) < 3 and not all(p in OOG for p in comp): klein.append((c, sorted(comp)))
out.append(f'tintclusters < 3 px (8-verbonden, zonder omlijning k/4 en zonder oog/glans): {len(klein)}')
for c, comp in klein: out.append(f'  {c}: {comp}')
buiten = sum(1 for y in range(64) for x in range(64) if R[y][x] != '.' and not massa[y, x])
leeg = sum(1 for y in range(64) for x in range(64) if R[y][x] == '.' and massa[y, x])
out.append(f'afwijking van de R2-massa (info; bewust: buik, bliksem, snavel, verre vleugel): {buiten} px extra, {leeg} px weggelaten')
tel = {c: sum(r.count(c) for r in R) for c, _ in PAL}
out.append(f'kleuren gebruikt: {sum(1 for c in tel if tel[c] and c != ".")} + transparant; telling {tel}')
out.append(f'totaal {sum(c != "." for r in R for c in r)} px')
open('controle_uitvoer.txt', 'w').write('\n'.join(out) + '\n'); print('\n'.join(out))
