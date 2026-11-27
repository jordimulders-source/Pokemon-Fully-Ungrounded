# Regicosmo r7: eindkeuring (Dragonfly Cave) op r6. Alleen tinten/belijning binnen het bevroren silhouet.
# Draaien vanuit docs/concept/sprites/regicosmo: python3 sprite/r7/bouw.py
import numpy as np, math
from PIL import Image
src = Image.open('sprite/r6/regicosmo_r6.png')
a = np.array(src).copy(); r6 = a.copy()
pal = src.getpalette()[:48]

# 1. Palet: asteroide-glans A (idx 10, 6 px) en beige schaduw E (idx 14) samengevoegd tot één tint
#    (zelfde helderheid 128/129, rel. helderheid per deel blijft gelijk); idx 10 wordt de donkerste Mars-tint.
pal[14*3:14*3+3] = [151, 124, 96]
a[a == 10] = 14
pal[10*3:10*3+3] = [120, 36, 36]        # outline base Mars (model-rand rechtsboven 84,11,10 / 156,48,39)
R = 10

# Delen labelen (8-samenhang) om Mars te vinden
H, W = a.shape
lab = np.zeros_like(a, dtype=int); n = 0
for y in range(H):
    for x in range(W):
        if a[y, x] and not lab[y, x]:
            n += 1; st = [(y, x)]; lab[y, x] = n
            while st:
                cy, cx = st.pop()
                for dy in (-1, 0, 1):
                    for dx in (-1, 0, 1):
                        yy, xx = cy+dy, cx+dx
                        if 0 <= yy < H and 0 <= xx < W and a[yy, xx] and not lab[yy, xx]:
                            lab[yy, xx] = n; st.append((yy, xx))
sizes = [(lab == i).sum() for i in range(1, n+1)]
mars = lab == (1 + int(np.argmax(sizes)))
ys, xs = np.nonzero(mars); cy, cx = (ys.min()+ys.max())/2, (xs.min()+xs.max())/2
print("Mars bbox", xs.min(), xs.max(), ys.min(), ys.max(), "midden", cx, cy)

def rand(y, x):  # buitenrand: 4-buur transparant
    return any(not (0 <= y+dy < H and 0 <= x+dx < W) or a[y+dy, x+dx] == 0
               for dy, dx in ((1,0),(-1,0),(0,1),(0,-1)))

# 2. Mars-omlijning: outline base = donkerste eigen tint (R) behalve aan de meest belichte kant
#    (linksboven, 2 blijft daar outline highlight) en de schaduwkant (zwart blijft).
for y, x in zip(ys, xs):
    if a[y, x] == 2 and rand(y, x):
        ang = math.degrees(math.atan2(-(y-cy), x-cx)) % 360   # 0 = rechts, 90 = boven
        if not (100 <= ang <= 197):
            a[y, x] = R

# 3. Zuidpoolvlek onderaan (modelvlek, blijft op zijn plek) ligt in de schaduwzone: één tint omlaag
#    (model daar mediaan 212,160,141 ~ helderheid 175 = tint 4; donkere rand 182,92,57 ~ tint 3).
for y, x in zip(ys, xs):
    if y >= cy + 14:
        if a[y, x] == 5: a[y, x] = 4
        elif a[y, x] == 4: a[y, x] = 3

# 4. Onderhelft: stap 4 -> 2 (helderheid 169 -> 93) in één keer is te groot; tint 3 als overgang
#    waar de schaduwsikkel (2) aan oranje 4 grenst, alleen rechtsonder (sikkel), niet links.
b = a.copy()
for y, x in zip(ys, xs):
    if a[y, x] == 2 and not rand(y, x) and y > cy + 5:
        ang = math.degrees(math.atan2(-(y-cy), x-cx)) % 360
        if 250 <= ang <= 335 and any(a[y+dy, x+dx] == 4 for dy, dx in ((-1,0),(0,-1),(0,1),(1,0))):
            b[y, x] = 3
a = b

out = Image.fromarray(a.astype(np.uint8), 'P'); out.putpalette(pal + [0]*(768-48))
out.save('sprite/r7/regicosmo_r7.png', transparency=0)
np.save('sprite/r7/r7.npy', a)
print('kleuren gebruikt:', sorted(set(a.flatten().tolist())))
