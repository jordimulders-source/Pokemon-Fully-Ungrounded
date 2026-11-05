"""Controle r4: bevroren delen (diff 0 met r3), palet, open randen, losse pixels, tintclusters < 3 px,
pixels buiten het bevroren silhouet. Uitvoer: controle_uitvoer.txt"""
import numpy as np
from PIL import Image
R = [l.rstrip('\n') for l in open('raster.txt')][:64]
R3 = [l.rstrip('\n') for l in open('../kleur_r3/raster.txt')][:64]
sil = np.asarray(Image.open('../../silhouet/silhouet_b1_1x.png'))[..., 3] > 0
out = []
def nb4(x, y):
    return [(x+dx, y+dy) for dx, dy in ((1,0),(-1,0),(0,1),(0,-1)) if 0 <= x+dx < 64 and 0 <= y+dy < 64]
# 1. bevroren delen
zones = {
 'oog (x24-27, r18-21)': {(x, y) for y in range(18, 22) for x in range(24, 28)},
 'wang (alle c/C van r3)': {(x, y) for y in range(64) for x in range(64) if R3[y][x] in 'cC'},
 'vleugelstippen (h/l/g in de vleugel van r3, x>=33 r25-36)': {(x, y) for y in range(25, 37) for x in range(33, 64) if R3[y][x] in 'hlg'},
 'staart (x>=44, r46-63)': {(x, y) for y in range(46, 64) for x in range(44, 64)},
}
for n, z in zones.items():
    d = [(x, y) for x, y in sorted(z) if R[y][x] != R3[y][x]]
    out.append(f'diff met r3, bevroren {n}: {len(z)} px, verschil {len(d)} {d}')
nieuw_cC = [(x, y) for y in range(64) for x in range(64) if R[y][x] in 'cC' and R3[y][x] not in 'cC']
out.append(f'nieuwe wangpixels buiten de r3-wang: {len(nieuw_cC)}')
p3 = open('../kleur_r3/normal.pal').read(); p4 = open('normal.pal').read()
out.append(f'palet gelijk aan r3: {p3 == p4}')
# 2. open randen: elke kleur behalve omlijning (k, 4, G, d) naast transparant
OMLIJN = set('k4Gd')
rand = [(x, y, R[y][x]) for y in range(64) for x in range(64) if R[y][x] not in OMLIJN | {'.'} and any(R[b][a] == '.' for a, b in nb4(x, y))]
licht = [r for r in rand if r[2] in '12hwcl']
out.append(f'lichte kleur op de buitenrand: {len(licht)} {licht}')
out.append(f'overige niet-omlijningskleur op de rand (dunne delen: snavel, poten, tenen = pseudo-omlijning; staart r3): {len(rand) - len(licht)} {[r for r in rand if r not in licht]}')
los = [(x, y) for y in range(64) for x in range(64) if R[y][x] != '.' and all(R[b][a] == '.' for a, b in
       [(x+i, y+j) for i in (-1,0,1) for j in (-1,0,1) if (i or j) and 0 <= x+i < 64 and 0 <= y+j < 64])]
out.append(f'losse pixels: {len(los)} {los}')
diag = [(x, y) for y in range(64) for x in range(64) if R[y][x] != '.' and all(R[b][a] == '.' for a, b in nb4(x, y))]
out.append(f'pixels alleen diagonaal verbonden: {len(diag)} {diag}')
# 3. tintclusters < 3 px (k/4/d/G = lijnen, niet geteld)
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
bev = set().union(*zones.values())
eigen = [(c, k) for c, k in klein if not all(p in bev for p in k)]
out.append(f'tintclusters < 3 px: {len(klein)}, waarvan in bevroren delen (oog/stippen/staart/wang) {len(klein) - len(eigen)}; in r4-werk {len(eigen)}:')
for c, comp in eigen: out.append(f'  {c}: {comp}')
# 4. buiten het silhouet
buiten = [(x, y) for y in range(64) for x in range(64) if R[y][x] != '.' and not sil[y, x]]
def afstand(x, y):
    return min(max(abs(x-a), abs(y-b)) for b in range(64) for a in range(64) if sil[b, a])
ver = [(x, y, afstand(x, y)) for x, y in buiten]
out.append(f'pixels BUITEN het silhouet: {len(buiten)}, max afstand {max(v[2] for v in ver) if ver else 0} px (eis <= 2); > 2: {[v for v in ver if v[2] > 2]}')
def zone(x, y):
    if y <= 11: return 'kuif'
    if x >= 37 and y <= 24: return 'achterkuif-lobben'
    if x <= 22 and y <= 24: return 'snavel/verre oog'
    if y <= 28: return 'kop'
    if y <= 44: return 'borst/buik (bol)'
    return 'poten/tenen'
from collections import Counter
cnt = Counter(zone(x, y) for x, y in buiten)
out.append('  per onderdeel: ' + ', '.join(f'{k} {v}' for k, v in cnt.items()))
out.append(f'  lijst: {buiten}')
leeg = [(x, y) for y in range(64) for x in range(64) if R[y][x] == '.' and sil[y, x]]
out.append(f'silhouetpixels LEEG gelaten: {len(leeg)} {leeg}')
alle = sum(R[y][x] != R3[y][x] for y in range(64) for x in range(64))
out.append(f'gewijzigd t.o.v. r3: {alle} px; totaal {sum(c != "." for r in R for c in r)} px; kleuren: {"".join(sorted(set("".join(R)) - {"."}))}')
geel = sorted(set(c for r in R for c in r if c in '123')); out.append(f'tinten geel: {geel} + selout 4')
open('controle_uitvoer.txt', 'w').write('\n'.join(out) + '\n'); print('\n'.join(out))
