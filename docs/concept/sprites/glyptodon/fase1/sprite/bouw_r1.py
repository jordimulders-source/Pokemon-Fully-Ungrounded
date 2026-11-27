# r1 = kale reductie (kaal_0.6, natief raster x0,6, lijn bij >=30% zwart) + alleen technische stappen.
# Elke stap logt hoeveel pixels hij verandert (diff t.o.v. kaal), per zone.
import numpy as np
from PIL import Image
import sys
D = __file__.rsplit('/', 1)[0]
sys.path.insert(0, D)
from palet import PAL

PAL = list(PAL) + [(52, 48, 45)]   # 12 = binnenlijn grijs (donkerste eigen tint, geen zwart)
BL = 12
kaal = np.load(D + '/kaal_0.6.npy')
a = kaal.copy()
H, W = a.shape
GRIJS = {2, 3, 4, 5, 6, 7, BL}
BAND = {8, 9, 10}
log = []

def buren4(y, x):
    for yy, xx in ((y-1, x), (y+1, x), (y, x-1), (y, x+1)):
        if 0 <= yy < H and 0 <= xx < W: yield yy, xx, a[yy, xx]
        else: yield yy, xx, 0

def zone(y, x):
    if x <= 21 and y >= 38: return 'kop/nek'
    if x >= 42: return 'staart'
    if y >= 52: return 'poten'
    return 'schild/romp'

def zet(y, x, v, waarom):
    if a[y, x] != v:
        log.append((zone(y, x), waarom, (x, y), int(a[y, x]), v)); a[y, x] = v

# 1. Oog: modelpixel (20,57) is wit (glans) in een zwart oog; op x0,6 valt hij in spritepixel (12,48)
#    en verdwijnt in de middeling. Terugzetten op de modelplek (onderhoek van de pupil).
zet(48, 12, 11, 'oogglans uit model (natief 20,57)')

# 2. Binnenlijnen: zwarte lijnpixels die niet aan de buitenkant grenzen en alleen grijs (zelfde materiaal)
#    scheiden -> donkerste eigen tint (binnenlijn, SPRITE_KERN). Lijnen tussen grijs en band, en rond het oog, blijven zwart.
oog = {(11, 48), (12, 47), (13, 47), (11, 47)}
nieuw = []
for y in range(H):
    for x in range(W):
        if kaal[y, x] != 1 or (x, y) in oog: continue
        b = [v for _, _, v in buren4(y, x)]
        if 0 in b: continue
        b8 = [kaal[yy, xx] for yy in range(y-1, y+2) for xx in range(x-1, x+2) if (yy, xx) != (y, x)]
        if 0 in b8: continue
        vul = [v for v in b8 if v not in (1, BL)]
        if vul and all(v in GRIJS for v in vul):
            nieuw.append((y, x))
for y, x in nieuw: zet(y, x, BL, 'binnenlijn grijs-in-grijs -> donkere eigen tint')

# 3. Buitenlijn: elke pixel aan de rand die geen lijn is krijgt een lijn.
#    Lichtkant (transparant boven/links) -> gekleurde selout (donkerste tint van het eigen materiaal),
#    schaduwkant (transparant rechts/onder) -> zwart. Bestaande donkerste tinten aan de lichtkant blijven.
rand = []
for y in range(H):
    for x in range(W):
        v = a[y, x]
        if v == 0 or v == 1: continue
        t = [(yy - y, xx - x) for yy, xx, w in buren4(y, x) if w == 0]
        if not t: continue
        schaduw = any(d in ((0, 1), (1, 0)) for d in t)
        if schaduw: rand.append((y, x, 1, 'buitenlijn schaduwkant zwart'))
        else:
            sel = 8 if v in BAND else (5 if v in (5, 6, 7) else 2)
            if v not in (2, 5, 8, BL): rand.append((y, x, sel, 'buitenlijn lichtkant selout'))
for y, x, v, w in rand: zet(y, x, v, w)

np.save(D + '/r1.npy', a)
im = Image.fromarray(a.astype('uint8'), 'P')
flat = [0, 0, 0] * 16
for k, c in enumerate(PAL): flat[3*k:3*k+3] = c
im.putpalette(flat); im.save(D + '/r1.png', transparency=0)
rgb = Image.open(D + '/r1.png').convert('RGBA')
bg = Image.new('RGBA', rgb.size, (255, 255, 255, 255)); bg.alpha_composite(rgb)
bg.resize((512, 512), Image.NEAREST).save(D + '/r1_8x.png')

from collections import Counter
print('pixels', (a > 0).sum(), 'kleuren', len(set(a.flatten())) , 'afwijkend van kaal', (a != kaal).sum())
c = Counter((z, w) for z, w, *_ in log)
for k, v in sorted(c.items()): print(f'  {k[0]:12s} {v:4d}  {k[1]}')
