# r14: poten naar Kirlia (Jordi, 26 nov: "doe kirlia maar na idd"), vanaf r12 (niet r13).
# Kirlia (anim_front_gba.png x29-34 y46-57), gemeten: 1 px vulling, tint varieert in de LENGTE:
#   nabije poot d(mid) y46-47, c y48, b(lichtst) y49-56, d y57; linkerlijn e (donker eigen), rechts f (zwart);
#   verre poot een stap donkerder (c/d), lijn e.
# Impala, bestaande grijzen: nabije poten scheen H, heup/knie/hiel/boven de hoef L; verre poten scheen N, gewrichten M.
# Gewrichten per poot = de knikken in de pootvorm (kolomsprong) en de modelplekken (knie nabije voorpoot rij 52-53, model 167-176).
# Stukken van 2-5 rijen (Kirlia-ritme). Alleen vulpixels (M/N/L/H); lijnen (D links, zwart rechts) en hoeven blijven.
import os, json, numpy as np
from PIL import Image
src = Image.open('r12/impala_r12.png'); a0 = np.array(src); a = a0.copy(); pal = src.getpalette()
D, S, M, N, L, H = 2, 3, 4, 5, 6, 7
NM = {1: '0', 2: 'D', 3: 'S', 4: 'M', 5: 'N', 6: 'L', 7: 'H', 8: 'W'}
def seg(*parts):          # (rij_van, rij_tot, tint) -> {rij: tint}
    return {y: t for y0, y1, t in parts for y in range(y0, y1 + 1)}
POTEN = [  # naam, x0, x1, rijen
    ('verre voorpoot', 19, 25, seg((48, 49, M), (50, 51, N), (52, 53, M), (54, 56, N), (57, 58, M))),
    ('nabije voorpoot', 29, 34, seg((48, 49, L), (50, 51, H), (52, 53, L), (54, 58, H), (59, 60, L))),
    ('verre achterpoot', 36, 41, seg((46, 48, M), (49, 51, N), (52, 53, M), (54, 55, N), (56, 56, M))),
    ('nabije achterpoot', 41, 52, seg((46, 48, L), (49, 52, H), (53, 54, L), (55, 56, H), (58, 59, L))),
]
for nm, x0, x1, rows in POTEN:
    for y, t in rows.items():
        for x in range(x0, x1 + 1):
            if a0[y, x] in (M, N, L, H): a[y, x] = t
# ---- bevroren ----
assert ((a0 == 0) == (a == 0)).all(), 'silhouet'
d = a != a0
inpoot = np.zeros_like(d)
for nm, x0, x1, rows in POTEN: inpoot[min(rows):max(rows) + 1, x0:x1 + 1] = True
assert not (d & ~inpoot).any(), 'buiten de poten'
assert not d[21:28, 18:26].any(), 'oog B3'
for _, x, y in json.load(open('extra_r9.json')): assert not d[y + 1, x + 10] and a[y + 1, x + 10] == 1, 'strepen'
wit = [(x, y) for y in range(31, 48) for x in range(18, 30) if a0[y, x] == 8]
assert all(not d[y + j, x + i] for x, y in wit for i in (-1, 0, 1) for j in (-1, 0, 1)), 'witte borst/buik'
assert not (d & (a0 <= 3)).any(), 'lijnen/hoeven'
os.makedirs('r14', exist_ok=True)
im = Image.fromarray(a, 'P'); im.putpalette(pal); im.save('r14/impala_r14.png', transparency=0)
c = np.array(Image.open('r14/impala_r14.png').convert('RGB').convert('RGBA')); c[a == 0, 3] = 0
Image.fromarray(c).resize((512, 512), Image.NEAREST).save('r14/impala_r14_8x.png')
from collections import Counter
cnt = Counter()
with open('r14/wijzigingen.txt', 'w') as f:
    for y, x in zip(*np.nonzero(d)):
        nm = next(p[0] for p in POTEN if p[1] <= x <= p[2] and y in p[3]); cnt[nm] += 1
        f.write('%s (%d,%d) %s->%s\n' % (nm, x, y, NM[a0[y, x]], NM[a[y, x]]))
print(int(d.sum()), 'px', dict(cnt), 'kleuren', len(set(np.unique(a)) - {0}), '+ transparant')
for y in range(44, 64): print('%2d ' % y + ''.join('.' if v == 0 else '.0DSMNLHWA345'[v] for v in a[y, 17:54]))
