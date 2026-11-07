"""Controle sprite v1: open randen (lichte kleur of niet-omlijning op de buitenrand), losse pixels, alleen-diagonaal
verbonden pixels, tintclusters < 3 px, kleurtelling, pixels buiten de C3-massa. Uitvoer: controle_uitvoer.txt"""
import numpy as np
from PIL import Image
from palet import lees, PAL
R = lees('raster.txt')
massa = np.asarray(Image.open('../bron/bron_kleur_1x.png'))[..., 3] > 0
out = []
def nb8(x, y): return [(x+i, y+j) for i in (-1,0,1) for j in (-1,0,1) if (i or j) and 0 <= x+i < 64 and 0 <= y+j < 64]
def nb4(x, y): return [(x+dx, y+dy) for dx, dy in ((1,0),(-1,0),(0,1),(0,-1)) if 0 <= x+dx < 64 and 0 <= y+dy < 64]
OMLIJN = set('k4')
rand = [(x, y, R[y][x]) for y in range(64) for x in range(64) if R[y][x] not in OMLIJN | {'.'} and any(R[b][a] == '.' for a, b in nb4(x, y))]
BLIKSEM_SELOUT = '1'  # oranje selout aan de lichtkant van de gele bliksem (zoals Picapau goudbruin)
licht = [r for r in rand if r[2] in 'a1yYbwc' and not (r[2] == BLIKSEM_SELOUT and r[1] >= 36 and r[0] <= 24)]
out.append(f'lichte kleur op de buitenrand: {len(licht)} {licht}')
out.append(f'overige niet-omlijning op de rand (selout e/G/g/v/3 toegestaan als gekleurde selout): {len(rand) - len(licht)} {[r for r in rand if r not in licht]}')
los = [(x, y) for y in range(64) for x in range(64) if R[y][x] != '.' and all(R[b][a] == '.' for a, b in
       [(x+i, y+j) for i in (-1,0,1) for j in (-1,0,1) if (i or j) and 0 <= x+i < 64 and 0 <= y+j < 64])]
out.append(f'losse pixels: {len(los)} {los}')
diag = [(x, y) for y in range(64) for x in range(64) if R[y][x] != '.' and all(R[b][a] == '.' for a, b in nb4(x, y))]
out.append(f'alleen diagonaal verbonden: {len(diag)} {diag}')
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
        if len(comp) < 3 and not (c in 'wG' and all(24 <= a <= 27 and 23 <= b <= 26 for a, b in comp)):
            klein.append((c, sorted(comp)))
out.append(f'tintclusters < 3 px (8-verbonden, zonder omlijning k/4 en zonder oog/glans): {len(klein)}')
for c, comp in klein: out.append(f'  {c}: {comp}')
buiten = [(x, y) for y in range(64) for x in range(64) if R[y][x] != '.' and not massa[y, x]]
binnen_leeg = [(x, y) for y in range(64) for x in range(64) if R[y][x] == '.' and massa[y, x]]
out.append(f'pixels buiten de C3-massa: {len(buiten)}; massa leeg gelaten: {len(binnen_leeg)}')
tel = {c: sum(r.count(c) for r in R) for c, _ in PAL}
out.append(f'kleuren gebruikt: {sum(1 for c in tel if tel[c] and c != ".")} + transparant; telling {tel}')
out.append(f'totaal {sum(c != "." for r in R for c in r)} px')
open('controle_uitvoer.txt', 'w').write('\n'.join(out) + '\n'); print('\n'.join(out))
