# r2 = r1 + benoemde reparaties van Claude (ronde 2). Alleen gemeten op het model (meet.py), lijnen en silhouet van r1 blijven.
#  1. kop/nek (x<=21, y 39..53): vulpixels opnieuw uit het model met MEERDERHEID van de modelcellen
#     (i.p.v. het gemiddelde dat modder gaf) -> crème/tan snuit en kaak, lichtste plaattinten in de nek.
#     Oog = Sandshrew-oog (Gen 3, anim_front_gba) 1-op-1 overgenomen, kern 4x3 (kolom 19-22, rij 28-30), op de modelplek.
#  2. poten (y>=53): meerderheid + lichte tenen waar >=30% van de pixel lichte modelcellen (>=140) zijn.
#  3. staart (x>=42): meerderheid + lichte segmentbovenkanten waar >=30% lichte modelcellen (>=135) zijn.
# Randpixels (buitenlijn/selout) en lijnpixels van r1 worden niet aangeraakt.
import sys, numpy as np
from PIL import Image
D = __file__.rsplit('/', 1)[0]; sys.path.insert(0, D)
from palet import PAL
import meet
PAL = list(PAL) + [(52, 48, 45)]
r1 = np.load(D + '/r1.npy'); a = r1.copy(); H, W = a.shape
log = {}

def rand(y, x):
    return any(not (0 <= yy < H and 0 <= xx < W) or a[yy, xx] == 0 for yy, xx in ((y-1, x), (y+1, x), (y, x-1), (y, x+1)))

def zet(y, x, v, waarom):
    if a[y, x] != v:
        log.setdefault(waarom, []).append((x, y, int(a[y, x]), v)); a[y, x] = v

VUL = [2, 3, 4, 5, 6, 7, 8, 9, 10]
GRIJS = [2, 3, 4, 5, 6, 7]
for y in range(H):
    for x in range(W):
        v = r1[y, x]
        if v in (0, 1, 12) or rand(y, x): continue
        if x <= 21 and 39 <= y <= 53:
            m, _ = meet.meerderheid(x, y, PAL, VUL)
            if m: zet(y, x, m, '1 kop/nek meerderheid')
        elif x >= 42 and y <= 52:
            m, _ = meet.meerderheid(x, y, PAL, GRIJS)
            if m: zet(y, x, m, '3 staart meerderheid')
            if meet.licht(x, y, 135) >= 0.30: zet(y, x, 7, '3 staart licht segment')
        elif y >= 53:
            m, _ = meet.meerderheid(x, y, PAL, GRIJS)
            if m: zet(y, x, m, '2 poten meerderheid')
            if meet.licht(x, y, 140) >= 0.30: zet(y, x, 7, '2 tenen licht')

# Oog: Sandshrew anim_front_gba, kolom 19-22 x rij 28-30 (f=zwart, c=wit, e=donkergrijs), 1-op-1, wit op de modelglans (12,48)
SAND = ['fecf', 'ffcc', 'fffe']
MAP = {'f': 1, 'c': 11, 'e': 5}
for j, rij in enumerate(SAND):
    for i, ch in enumerate(rij):
        zet(47 + j, 10 + i, MAP[ch], '1 oog Sandshrew')

np.save(D + '/r2.npy', a)
im = Image.fromarray(a.astype('uint8'), 'P'); flat = [0, 0, 0] * 16
for k, c in enumerate(PAL): flat[3*k:3*k+3] = c
im.putpalette(flat); im.save(D + '/r2.png', transparency=0)
rgb = Image.open(D + '/r2.png').convert('RGBA'); bg = Image.new('RGBA', rgb.size, (255, 255, 255, 255)); bg.alpha_composite(rgb)
bg.resize((512, 512), Image.NEAREST).save(D + '/r2_8x.png')
kaal = np.load(D + '/kaal_0.6.npy')
print('t.o.v. r1:', (a != r1).sum(), ' t.o.v. kaal:', (a != kaal).sum(), ' kleuren', len(set(a.flatten())))
for k in sorted(log): print(f'  {k:28s} {len(log[k])}')
