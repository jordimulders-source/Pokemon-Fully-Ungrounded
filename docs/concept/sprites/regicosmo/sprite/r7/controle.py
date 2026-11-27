# Controle r7 t.o.v. r6: alpha-diff, gewijzigde pixels per deel, afwisseling zwart/niet-zwart langs elke buitenrand.
import numpy as np, math
from PIL import Image
r6 = np.array(Image.open('sprite/r6/regicosmo_r6.png')); r7 = np.array(Image.open('sprite/r7/regicosmo_r7.png'))
print('alpha-diff (pixels waar transparantie verschilt):', int(((r6 == 0) != (r7 == 0)).sum()))
H, W = r7.shape; lab = np.zeros((H, W), int); n = 0
for y in range(H):
    for x in range(W):
        if r7[y, x] and not lab[y, x]:
            n += 1; st = [(y, x)]; lab[y, x] = n
            while st:
                cy, cx = st.pop()
                for dy in (-1, 0, 1):
                    for dx in (-1, 0, 1):
                        yy, xx = cy+dy, cx+dx
                        if 0 <= yy < H and 0 <= xx < W and r7[yy, xx] and not lab[yy, xx]:
                            lab[yy, xx] = n; st.append((yy, xx))
naam = {}
for i in range(1, n+1):
    ys, xs = np.nonzero(lab == i); c = ((xs.min()+xs.max())/2, (ys.min()+ys.max())/2)
    if len(ys) > 500: k = 'Mars'
    elif c[0] < 12 and c[1] < 37: k = 'ijsplaneet'
    elif c[0] < 12: k = 'asteroide'
    elif c[0] > 44 and c[1] < 37: k = 'Saturnus'
    elif c[0] > 44: k = 'maan'
    elif c[0] < 28: k = 'voet blauw'
    else: k = 'voet beige'
    naam[i] = k
    ch = int(((r6 != r7) & (lab == i)).sum())
    # zwart/niet-zwart-wisselingen langs de buitenrand (op hoek gesorteerd)
    rp = [(y, x) for y, x in zip(ys, xs) if any(not (0 <= y+dy < H and 0 <= x+dx < W) or r7[y+dy, x+dx] == 0 for dy, dx in ((1,0),(-1,0),(0,1),(0,-1)))]
    rp.sort(key=lambda p: math.atan2(-(p[0]-c[1]), p[1]-c[0]))
    seq = [r7[p] == 1 for p in rp]
    sw = sum(seq[j] != seq[j-1] for j in range(len(seq)))
    print(f'{k:11s} px {len(ys):4d}  gewijzigd {ch:3d}  wissels zwart<->kleur langs rand: {sw}')
d = r6 != r7
from collections import Counter
print('overgangen (r6->r7):', Counter(zip(r6[d].tolist(), r7[d].tolist())))
print('totaal gewijzigd:', int(d.sum()))
