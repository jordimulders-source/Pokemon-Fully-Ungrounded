"""Controle r2: lichte kleur op de buitenrand, losse pixels, tintclusters < 3 px, pixels buiten/binnen het bevroren silhouet,
en welke r5-details letterlijk zijn overgenomen. Uitvoer: controle_uitvoer.txt"""
import numpy as np
from PIL import Image
R = [l.rstrip('\n') for l in open('raster.txt')][:64]
R1 = [l.rstrip('\n') for l in open('../kleur_r1/raster.txt')][:64]
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
# bevroren delen (masker op kleur_r1): diff moet 0 zijn
def masker(naam):
    m = set()
    if naam == 'kuiftoppen':
        m = {(x, y) for y in range(3, 9) for x in range(64)}
    elif naam == 'oog':
        m = {(x, y) for y in range(18, 22) for x in range(25, 29)}
    elif naam == 'wang':
        m = {(x, y) for y in range(64) for x in range(64) if R1[y][x] in 'cC'}
    elif naam == 'vleugel+schubben':   # per rij vanaf de eerste vleugelpixel (d) rechts van x33 tot het eind
        for y in range(24, 46):
            xs = [x for x in range(33, 64) if R1[y][x] == 'd']
            if xs: m |= {(x, y) for x in range(xs[0], 64)}
    elif naam == 'staart':
        m = {(x, y) for y in range(45, 64) for x in range(44, 64)}
    return m
for n in ['kuiftoppen', 'oog', 'wang', 'vleugel+schubben', 'staart']:
    d = [(x, y) for x, y in sorted(masker(n)) if R[y][x] != R1[y][x]]
    out.append(f'diff met r1, bevroren {n} ({len(masker(n))} px): {len(d)} {d}')
alle = [(x, y, R1[y][x], R[y][x]) for y in range(64) for x in range(64) if R[y][x] != R1[y][x]]
out.append(f'gewijzigd t.o.v. r1: {len(alle)} px (snavel, kop-/borst-/buiklicht, voetjes, kuifpunten)')
out.append(f'totaal {sum(c != "." for r in R for c in r)} px; kleuren gebruikt: {"".join(sorted(set("".join(R)) - {"."}))}')
open('controle_uitvoer.txt', 'w').write('\n'.join(out) + '\n'); print('\n'.join(out))
