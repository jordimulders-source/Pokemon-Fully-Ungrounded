# r17: alleen de lila rand bovenop de kap naar het model + tinten opnieuw vanuit de modeltoonkaart (toon.py -> toon_L.npy).
# Jordi over r16: "alleen de paarse lijn boven het hoofd klopt niet helemaal, verder is die een stuk beter.
#                  alleen kleurtinten, lijnen, schaduw is nog niet goed"
# Vorm = r16 (silhouetdiff 0); per pixel wordt alleen de tint binnen dezelfde kleurgroep gekozen, behalve de rand (punt 1).
# Draaien vanuit deze map: python3 toon.py && python3 bouw_r17.py
import numpy as np
from PIL import Image
im0 = Image.open('../r16/sprite.png'); r16 = np.array(im0).astype(int); a = r16.copy()
pal = np.array(im0.getpalette()[:48]).reshape(16, 3)
L = np.load('toon_L.npy')
H = '0123456789ABCDEF'
def put(x, y, s):
    for i, c in enumerate(s):
        if c != '-': a[y, x + i] = 0 if c == '.' else H.index(c)

# ---------- palet: lijframp naar de modeltonen (model: wit 241, lichte schaduw 202,188,209, middentint 182,158,191,
# onderschaduw 143,109,164); wit blijft koel, alleen de onderste twee tinten lopen naar lila.  Stappen L 236/204/166/127.
pal[2] = (236, 235, 242)
pal[3] = (207, 201, 222)
pal[4] = (172, 158, 195)
pal[5] = (138, 114, 165)

BODY = {2, 3, 4, 5, 15}; PANEL = {9, 10, 11, 12}
def buur(y, x):
    return [r16[y + dy, x + dx] for dy, dx in ((-1, 0), (1, 0), (0, -1), (0, 1)) if 0 <= y + dy < 64 and 0 <= x + dx < 64]

# ---------- lijf: tint per pixel uit de modelhelderheid (glans F blijft waar r16 hem had: het hooglicht bovenop de kap)
def lijftint(v):
    return 2 if v >= 215 else 3 if v >= 186 else 4 if v >= 150 else 5
for y in range(64):
    for x in range(64):
        v = r16[y, x]
        if v not in BODY or v == 15: continue
        nb = buur(y, x)
        if v == 5 and any(n == 0 or n in PANEL for n in nb): continue       # 5 als contour (lichtkant): blijft lijn
        if np.hypot(x + .5 - 19, y + .5 - 35) <= 7.0: continue              # lens = oog b (r8), niet het modeloog: tinten blijven
        a[y, x] = lijftint(L[y, x])

# ---------- lila (6/7) binnen de paarse onderdelen: licht/midden uit het model; 8 en zwart (lijnen) blijven
for y in range(64):
    for x in range(64):
        if r16[y, x] in (6, 7) and 12 <= x <= 30 and 25 <= y <= 45:   # lens/voorvlak; antennes, bol en rechtergewricht blijven r16
            a[y, x] = 6 if L[y, x] >= 140 else 7

# ---------- 1. lila rand bovenop de kap (gemeten in het model, sprite_r17/top3.png):
# buitenlijn rij 17 (x19-24), band rij 18: x19-21 midden, x22-26 licht; rij 17 x25-26 licht (de band ligt daar hoger, onder de antennevoet);
# rij 19: x20 midden, x21-22 donker (de donkere onderlijn van de band), wit vanaf x23; rij 20: x19-20 donker (rand loopt over in de kapcontour).
put(25, 17, '66')
put(19, 18, '-77766666')
put(20, 19, '788222')
put(19, 20, '88')
# rechts van de bol: band rij 17-18 (model x33-34 licht, x35 midden)
a[17, 33] = 6; put(33, 18, '667')

# slagschaduw onder de bol (r16, model 204-214) en de grijze rand langs de linkerkapcontour (model 190-200)
put(28, 21, '333')
# langs de linker kapcontour (x14-22, rij 20-25) blijven de r16-tinten: een 3-strook daar loopt evenwijdig aan de contour (banding)
for y in range(20, 26):
    for x in range(14, 23):
        if r16[y, x] in (2, 3, 4) and a[y, x] in (2, 3, 4, 5): a[y, x] = r16[y, x]

# ---------- lijnen: voorvlakrand boven de lens is in het model zwart (L 23-34 op x15-20) en loopt rechts over in middenpaars (x21 L116);
# links buigt hij naar beneden (model (14,27) 48, (15,27) 40)
put(15, 26, '1111117'); put(14, 27, '11')

# ---------- schaduw onder: tussen het wit (3) en de lila onderschaduw (5) zit in r16 een sprong van L 77; terminator in 4
# (alleen vulpixels 5 die aan 3/2 grenzen, onder de lens: rij >= 39)
b = a.copy()
for y in range(39, 48):
    for x in range(10, 36):
        if b[y, x] == 5 and not any(n == 0 or n == 1 for n in [b[y-1, x], b[y+1, x], b[y, x-1], b[y, x+1]]) and \
           any(n in (2, 3) for n in [b[y-1, x], b[y+1, x], b[y, x-1], b[y, x+1]]):
            a[y, x] = 4

put(22, 43, '4'); put(22, 44, '44')   # terminator wit -> lila onder de lens (model (22,43) L151)
VAST = {(43, 22), (44, 22), (44, 23)}
# ---------- technisch opschonen: tintvlakjes < 3 px binnen het lijf naar de meest voorkomende lijfbuur (alleen tint, geen lijnen)
def clusters(arr, vals):
    seen = np.zeros_like(arr, bool); out = []
    for y in range(64):
        for x in range(64):
            if seen[y, x] or arr[y, x] not in vals: continue
            v = arr[y, x]; st = [(y, x)]; seen[y, x] = True; cl = []
            while st:
                cy, cx = st.pop(); cl.append((cy, cx))
                for dy, dx in ((-1, 0), (1, 0), (0, -1), (0, 1)):
                    ny, nx = cy + dy, cx + dx
                    if 0 <= ny < 64 and 0 <= nx < 64 and not seen[ny, nx] and arr[ny, nx] == v: seen[ny, nx] = True; st.append((ny, nx))
            out.append((v, cl))
    return out
from collections import Counter
for ronde in range(3):
    for v, cl in clusters(a, {2, 3, 4}):
        if len(cl) >= 3 or any(p in VAST for p in cl): continue
        for (y, x) in cl:
            if r16[y, x] not in BODY: continue
            c = Counter(a[y + dy, x + dx] for dy, dx in ((-1, 0), (1, 0), (0, -1), (0, 1)) if a[y + dy, x + dx] in (2, 3, 4, 5) and a[y + dy, x + dx] != v)
            if c: a[y, x] = c.most_common(1)[0][0]

def sla(arr, naam):
    im = Image.fromarray(arr.astype('uint8'), 'P'); im.putpalette([int(v) for v in pal.flatten()] + [0] * (768 - 48))
    im.save(naam, transparency=0)
    b = Image.new('RGBA', (64, 64), (255, 255, 255, 255)); m = np.array(im.convert('RGBA')); m[arr == 0, 3] = 0; b.alpha_composite(Image.fromarray(m))
    b.convert('RGB').resize((512, 512), Image.NEAREST).save(naam.replace('.png', '_8x.png'))
if __name__ == '__main__':
    sla(a, 'sprite.png'); np.save('r17.npy', a)
    H2 = '.123456789ABCDEF'
    print('   ' + ''.join(str(x % 10) for x in range(6, 42)))
    for y in range(14, 50): print('%2d ' % y + ''.join(H2[v] for v in a[y, 6:42]))
    print('silhouet-diff:', int(((a == 0) != (r16 == 0)).sum()), ' gewijzigde px:', int((a != r16).sum()), ' kleuren:', len(np.unique(a)))
