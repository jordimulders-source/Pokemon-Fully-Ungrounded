"""Controle: lichte kleur op de buitenrand, losse pixels, tintclusters < 3 px, pixels buiten/binnen het bevroren silhouet,
en welke r5-details letterlijk zijn overgenomen. Uitvoer: controle_uitvoer.txt"""
import numpy as np
from PIL import Image
R = [l.rstrip('\n') for l in open('raster.txt')][:64]
R5 = [l.rstrip('\n') for l in open('../../kleur_r5/raster.txt')][:64]
sil = np.asarray(Image.open('../../silhouet/silhouet_b1_1x.png'))[..., 3] > 0
lab = [l.rstrip('\n') for l in open('../bron/bron_labels.txt') if not l.startswith('#')]
LICHT = set('123hwcl')       # mag niet tegen transparant
out = []
def nb4(x, y):
    return [(x+dx, y+dy) for dx, dy in ((1,0),(-1,0),(0,1),(0,-1)) if 0 <= x+dx < 64 and 0 <= y+dy < 64]
rand = [(x, y, R[y][x]) for y in range(64) for x in range(64) if R[y][x] in LICHT and any(R[b][a] == '.' for a, b in nb4(x, y))]
out.append(f'lichte kleur op de buitenrand (open rand): {len(rand)} {rand}')
los = [(x, y) for y in range(64) for x in range(64) if R[y][x] != '.' and all(R[b][a] == '.' for a, b in
       [(x+i, y+j) for i in (-1,0,1) for j in (-1,0,1) if (i or j) and 0 <= x+i < 64 and 0 <= y+j < 64])]
out.append(f'losse pixels: {len(los)} {los}')
seen = set(); klein = []
for y in range(64):
    for x in range(64):
        c = R[y][x]
        if c in '.k' or (x, y) in seen: continue
        st = [(x, y)]; comp = []; seen.add((x, y))
        while st:
            p = st.pop(); comp.append(p)
            for q in nb4(*p):
                if q not in seen and R[q[1]][q[0]] == c: seen.add(q); st.append(q)
        if len(comp) < 3: klein.append((c, comp))
uitz = [k for k in klein if k[0] in 'wG' or all(18 <= y <= 21 and 25 <= x <= 28 for x, y in k[1])]
out.append(f'tintclusters < 3 px: {len(klein)} (waarvan oog/glans/donkergrijs {len(uitz)})')
for c, comp in klein:
    if (c, comp) not in uitz: out.append(f'  {c}: {comp}')
buiten = [(x, y, lab[y][x]) for y in range(64) for x in range(64) if R[y][x] != '.' and not sil[y, x]]
binnen = [(x, y, lab[y][x]) for y in range(64) for x in range(64) if R[y][x] == '.' and sil[y, x]]
out.append(f'pixels BUITEN het silhouet: {len(buiten)} (x, y, renderlabel) {buiten}')
out.append(f'silhouetpixels LEEG gelaten: {len(binnen)} {binnen}')
zones = {'kuiftoppen r3-8': (0, 3, 64, 9), 'oog x25-28 r18-21': (25, 18, 29, 22), 'wang x23-28 r23-26': (23, 23, 29, 27),
         'schubben x35-41 r27-33': (35, 27, 42, 34)}
for n, (x0, y0, x1, y1) in zones.items():
    d = sum(R[y][x] != R5[y][x] for y in range(y0, y1) for x in range(x0, x1))
    out.append(f'diff met r5 in {n}: {d} px')
out.append(f'totaal {sum(c != "." for r in R for c in r)} px; kleuren gebruikt: {"".join(sorted(set("".join(R)) - {"."}))}')
open('controle_uitvoer.txt', 'w').write('\n'.join(out) + '\n'); print('\n'.join(out))
