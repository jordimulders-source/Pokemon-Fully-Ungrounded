"""Controle r5: bevroren delen (diff 0 met r4), kop rechts t.o.v. r2 (alleen de lijn-pixels + naad), open randen,
losse pixels, tintclusters < 3 px, pixels buiten het silhouet. Uitvoer: controle_uitvoer.txt"""
import numpy as np
from PIL import Image
R = [l.rstrip('\n') for l in open('raster.txt')][:64]
R4 = [l.rstrip('\n') for l in open('../kleur_r4/raster.txt')][:64]
R2 = [l.rstrip('\n') for l in open('../kleur_r2/raster.txt')][:64]
sil = np.asarray(Image.open('../../silhouet/silhouet_b1_1x.png'))[..., 3] > 0
out = []
def nb4(x, y):
    return [(x+dx, y+dy) for dx, dy in ((1,0),(-1,0),(0,1),(0,-1)) if 0 <= x+dx < 64 and 0 <= y+dy < 64]
KOPR = set()
for y in range(3, 12): KOPR |= {(x, y) for x in range(64)}
KOPR |= {(x, 12) for x in range(25, 64)}
for y in range(13, 25): KOPR |= {(x, y) for x in range(29, 64)}
omtrek = set()
for y in range(29, 46):
    xs = [x for x in range(64) if R4[y][x] != '.']; omtrek.add((xs[0], y))
zones = {
 'oog (x24-27, r18-21)': {(x, y) for y in range(18, 22) for x in range(24, 28)},
 'wang (c/C van r4)': {(x, y) for y in range(64) for x in range(64) if R4[y][x] in 'cC'},
 'snavel + verre oog (x13-23, r16-24)': {(x, y) for y in range(16, 25) for x in range(13, 24)},
 'kop links van het oog (x<=28 r13-28 behalve snavel)': {(x, y) for y in range(13, 29) for x in range(13, 29) if not (x <= 23 and 16 <= y <= 24) and (x, y) not in KOPR} - {(28, 14), (27, 15), (28, 15)},
 'borstomtrek (eerste pixel per rij r29-45)': omtrek,
 'vleugel (alle d/b/h/l/g rechts van x33, r25-46 in r4)': {(x, y) for y in range(25, 46) for x in range(33, 64) if R4[y][x] in 'dbhlgk' and x >= 33},
 'staart (x>=44, r46-63)': {(x, y) for y in range(46, 64) for x in range(44, 64)},
}
for n, z in zones.items():
    d = [(x, y) for x, y in sorted(z) if R[y][x] != R4[y][x]]
    out.append(f'diff met r4, bevroren {n}: {len(z)} px, verschil {len(d)} {d}')
d2 = [(x, y, R2[y][x], R[y][x]) for x, y in sorted(KOPR, key=lambda p: (p[1], p[0])) if R[y][x] != R2[y][x]]
out.append(f'kop rechts (zone r3-24, uit r2): verschil met r2 {len(d2)} px (x, y, r2 -> r5): {d2}')
out.append(f'  (wangpixels in de zone blijven r4; naad met r4-voorhoofd: (28,14) (27,15) (28,15) -> 1, buiten de zone)')
out.append(f'palet gelijk aan r4: {open("../kleur_r4/normal.pal").read() == open("normal.pal").read()}')
OMLIJN = set('k4Gd')
rand = [(x, y, R[y][x]) for y in range(64) for x in range(64) if R[y][x] not in OMLIJN | {'.'} and any(R[b][a] == '.' for a, b in nb4(x, y))]
licht = [r for r in rand if r[2] in '12hwcl']
out.append(f'lichte kleur op de buitenrand: {len(licht)} {licht}')
out.append(f'overige niet-omlijningskleur op de rand: {len(rand) - len(licht)} {[r for r in rand if r not in licht]}')
los = [(x, y) for y in range(64) for x in range(64) if R[y][x] != '.' and all(R[b][a] == '.' for a, b in
       [(x+i, y+j) for i in (-1,0,1) for j in (-1,0,1) if (i or j) and 0 <= x+i < 64 and 0 <= y+j < 64])]
out.append(f'losse pixels: {len(los)} {los}')
diag = [(x, y) for y in range(64) for x in range(64) if R[y][x] != '.' and all(R[b][a] == '.' for a, b in nb4(x, y))]
out.append(f'pixels alleen diagonaal verbonden: {len(diag)} {diag}')
seen = set(); klein = []
for y in range(64):
    for x in range(64):
        c = R[y][x]
        if c in '.k4dG' or (x, y) in seen: continue
        st = [(x, y)]; comp = []; seen.add((x, y))
        while st:
            p = st.pop(); comp.append(p)
            for q in nb4(*p):
                if q not in seen and R[q[1]][q[0]] == c: seen.add(q); st.append(q)
        if len(comp) < 3: klein.append((c, comp))
out.append(f'tintclusters < 3 px: {len(klein)}')
for c, comp in klein:
    waar = 'kop rechts (r2)' if all(p in KOPR for p in comp) else ('bevroren' if any(all(p in z for p in comp) for z in zones.values()) else 'r5-werk')
    out.append(f'  {c}: {comp}  [{waar}]')
buiten = [(x, y) for y in range(64) for x in range(64) if R[y][x] != '.' and not sil[y, x]]
def afstand(x, y):
    return min(max(abs(x-a), abs(y-b)) for b in range(64) for a in range(64) if sil[b, a])
ver = [(x, y, afstand(x, y)) for x, y in buiten]
out.append(f'pixels BUITEN het silhouet: {len(buiten)}, max afstand {max(v[2] for v in ver)} px; > 2: {[v for v in ver if v[2] > 2]}')
out.append(f'  lijst: {buiten}')
alle = sum(R[y][x] != R4[y][x] for y in range(64) for x in range(64))
out.append(f'gewijzigd t.o.v. r4: {alle} px; totaal {sum(c != "." for r in R for c in r)} px; kleuren: {"".join(sorted(set("".join(R)) - {"."}))}')
open('controle_uitvoer.txt', 'w').write('\n'.join(out) + '\n'); print('\n'.join(out))
