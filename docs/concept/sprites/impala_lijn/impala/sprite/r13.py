# r13: volume in de vier poten (Jordi, 26 nov: "de poten zijn effen vlakken, controleer die opnieuw"), vanaf r12.
# Gemeten (zie r13/rapport.md): het model is per poot vlak (binnenkant 138-146, nabije voorpoot ~200; links/rechts verschil <= 5),
# dus het volume volgt het Gen 3-recept dat in Stantler/Girafarig/Ponyta/Rapidash (_gba) gemeten is:
#   lijn | lichte kolom naast de lichtkant | middentint | (donkere kolom) | zwart; hoef: lichtere pixel links binnen de hoef.
# Per rij, per poot: breedte 1 = middentint; breedte 2 = licht + midden; breedte >= 3 = licht + midden + donker.
# Vlakjes < 3 px (8-verbonden: een 1-px lichtstrook langs de poot telt als een geheel; behalve de hoefglans) gaan terug naar de middentint. Alleen vulpixels; lijnen (zwart/D) en silhouet blijven.
# Variant B (python3 r13.py B): op de schenen van de twee nabije poten wordt de linkerlijn outline highlight S
#   (gids: "Put some of the shadow/outline highlight color on the outlines in the very most highlighted parts").
import os, sys, json, numpy as np
from PIL import Image
VAR = sys.argv[1] if len(sys.argv) > 1 else 'A'
RN = 'r13' if VAR == 'A' else 'r13/variant_B'
src = Image.open('r12/impala_r12.png'); a0 = np.array(src); a = a0.copy(); pal = src.getpalette()
D, S, M, N, L, H = 2, 3, 4, 5, 6, 7
NM = {1: '0', 2: 'D', 3: 'S', 4: 'M', 5: 'N', 6: 'L', 7: 'H', 8: 'W'}
# poot: (naam, x0, x1, y0, y1, licht, midden, donker)
POTEN = [('verre voorpoot', 19, 25, 46, 60, N, M, S),
         ('nabije voorpoot', 29, 34, 48, 63, H, L, N),
         ('verre achterpoot', 36, 41, 46, 58, N, M, S),
         ('nabije achterpoot', 41, 52, 46, 60, L, N, M)]
FILL = {M, N, L, H}
rol = {}   # (x,y) -> (poot, 'licht'/'midden'/'donker')
for nm, x0, x1, y0, y1, li, mi, do in POTEN:
    for y in range(y0, y1 + 1):
        xs = [x for x in range(x0, x1 + 1) if a0[y, x] in FILL]
        runs = []
        for x in xs:
            if runs and x == runs[-1][-1] + 1: runs[-1].append(x)
            else: runs.append([x])
        for r in runs:
            for i, x in enumerate(r):
                k = 'licht' if len(r) >= 2 and i == 0 else 'donker' if len(r) >= 3 and i == len(r) - 1 else 'midden'
                rol[(x, y)] = (nm, k)
                a[y, x] = {'licht': li, 'midden': mi, 'donker': do}[k]
# vlakjes < 3 px van licht/donker terug naar midden
def comp(x, y):
    v = a[y, x]; seen = {(x, y)}; st = [(x, y)]
    while st:
        cx, cy = st.pop()
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (1, -1), (-1, 1), (-1, -1)):
            q = (cx + dx, cy + dy)
            if q not in seen and q in rol and a[q[1], q[0]] == v: seen.add(q); st.append(q)
    return seen
for (x, y), (nm, k) in list(rol.items()):
    if k != 'midden' and len(comp(x, y)) < 3:
        mi = [p for p in POTEN if p[0] == nm][0][6]
        for q in comp(x, y): a[q[1], q[0]] = mi; rol[q] = (nm, 'midden')
# hoefglans nabije voorpoot: model heeft links in de hoef lichtere pixels (lum 80-120 tegen 70); S = 1 stap boven D
for x, y in ((31, 61), (31, 62)): assert a0[y, x] == D; a[y, x] = S
if VAR == 'B':
    for (x, y), (nm, k) in rol.items():
        if nm.startswith('nabije') and a0[y, x - 1] == D and a0[y, x + 1] == 1 and k == 'midden' and a0[y, x - 2] == 0:
            a[y, x - 1] = S
# ---- bevroren ----
assert ((a0 == 0) == (a == 0)).all(), 'silhouet'
d = a != a0
inpoot = np.zeros_like(d)
for nm, x0, x1, y0, y1, *_ in POTEN: inpoot[y0:y1 + 1, x0:x1 + 1] = True
assert not (d & ~inpoot).any(), 'buiten de poten gewijzigd'
assert not d[21:28, 18:26].any()
for _, x, y in json.load(open('extra_r9.json')): assert not d[y + 1, x + 10] and a[y + 1, x + 10] == 1
wit = [(x, y) for y in range(31, 48) for x in range(18, 30) if a0[y, x] == 8]
assert all(not d[y + j, x + i] for x, y in wit for i in (-1, 0, 1) for j in (-1, 0, 1)), 'witte borst/buik'
assert VAR == 'B' or not ((a0 <= 2) & d & (a0 > 0)).sum() - 2, 'lijnen gewijzigd (behalve hoefglans)'
os.makedirs(RN, exist_ok=True)
fn = f'{RN}/impala_r13{"" if VAR == "A" else "_B"}.png'
im = Image.fromarray(a, 'P'); im.putpalette(pal); im.save(fn, transparency=0)
c = np.array(Image.open(fn).convert('RGB').convert('RGBA')); c[a == 0, 3] = 0
Image.fromarray(c).resize((512, 512), Image.NEAREST).save(fn.replace('.png', '_8x.png'))
from collections import Counter
cnt = Counter()
with open(f'{RN}/wijzigingen.txt', 'w') as f:
    for y, x in zip(*np.nonzero(d)):
        nm = next((p[0] for p in POTEN if p[1] <= x <= p[2] and p[3] <= y <= p[4]), '?'); cnt[nm] += 1
        f.write('%s (%d,%d) %s->%s\n' % (nm, x, y, NM[a0[y, x]], NM[a[y, x]]))
print(VAR, int(d.sum()), 'px', dict(cnt), 'kleuren', len(set(np.unique(a)) - {0}), '+ transparant')
for y in range(44, 64): print('%2d ' % y + ''.join('.' if v == 0 else '.0DSMNLHWA345'[v] for v in a[y, 17:54]))
