# r11: (1) dunne lichte rand bovenop het lijf i.p.v. de dikke kraag (model: 1-2 px lila op de bovenrand),
#      (2) oog/lens in drie varianten met een breder wit koepelvlak rechts van de lens (model: lens, wit 1, paars 1, wit 2, donkere lijn).
# Basis: ../r10/sprite.png. Draaien vanuit deze map: python3 bouw_r11.py
import numpy as np
from PIL import Image
im0 = Image.open('../r10/sprite.png'); r10 = np.array(im0).astype(int); pal = im0.getpalette()[:48]
H = '0123456789ABCDEF'
def put(a, x, y, s):
    for i, c in enumerate(s):
        if c == '-': continue
        a[y, x + i] = 0 if c == '.' else H.index(c)

# ================= 1. bovenkant (gemeenschappelijk) =================
basis = r10.copy()
# links van het gewricht: r16 = silhouetrand + antennevoet (blijft), r17 = lila rand 6 (blijft), r18 rand alleen
# bij de paneelhoek 2 px (model: daar 2 rijen), verder lijf; r19 (was de donkere onderlijn) wordt lijf
put(basis, 22, 18, '762222')
put(basis, 22, 19, '322222')
# rechts van het gewricht: r17 silhouetrand (blijft), r18 dunne roze rand, r19 (was onderlijn) wordt lijf
put(basis, 33, 18, '6667')
put(basis, 33, 19, '2233')

# ================= 2. koepel rechts (gemeenschappelijk) =================
# paarse koepelring rechts 1 px (was 2): r30 x25, r31-37 x26, r38-39 x25, r40 x24, r41 x23 ; kleur loopt mee met het licht
RING = {30: [25], 31: [26], 32: [26], 33: [26], 34: [26], 35: [26], 36: [26], 37: [26], 38: [25], 39: [25], 40: [24], 41: [23]}
RINGKLEUR = {30: 6, 31: 6, 32: 6, 33: 7, 34: 7, 35: 7, 36: 7, 37: 7, 38: 8, 39: 8, 40: 8, 41: 8}
# buitenste donkere koepellijn (blijft waar hij is): r29 x26-27, r30 x27-28, r31-32 x28, r33-37 x29, r38-39 x28, r40 x27, r41 x25-27
LIJN = {29: 26, 30: 27, 31: 28, 32: 28, 33: 29, 34: 29, 35: 29, 36: 29, 37: 29, 38: 28, 39: 28, 40: 27, 41: 25}

def toon(x, y, buiten):
    # verloop wit linksboven -> 3/4 rechtsonder, sikkel 5 onderaan (licht van linksboven: t = afstand langs de lichtrichting)
    t = (x - 19) + (y - 35) + (1 if buiten else 0)
    if t <= 5: return 3 if y >= 39 else 2   # onder de lens (schaduwkant) nooit het lichtste wit
    if t <= 8: return 3
    if t <= 11: return 4
    return 5

def koepel(a, lensrechts):
    """lensrechts[y] = x van de zwarte lensrand rechts in rij y. Vult rechts: binnenwit, ring, buitenwit."""
    for y in range(30, 42):
        rx = RING[y][0]
        x0 = lensrechts.get(y, None)
        if x0 is not None:
            for x in range(x0 + 1, rx): a[y, x] = toon(x, y, False)
        a[y, rx] = RINGKLEUR[y]
        for x in range(rx + 1, LIJN[y]): a[y, x] = toon(x, y, True)

def lensrand(a):
    out = {}
    for y in range(29, 42):
        xs = [x for x in range(14, 26) if a[y, x] == 1]
        if xs: out[y] = max(xs)
    return out

# ---------- variant A: lens zoals r10 ----------
A = basis.copy()
LA = {30: 22, 31: 23, 32: 23, 33: 24, 34: 24, 35: 24, 36: 24, 37: 23, 38: 23, 39: 22, 40: 20}
koepel(A, LA)

# ---------- variant B: lens 10x10 (paarse lensring 1 px i.p.v. 2, iris/pupil/glans ongewijzigd, 1 px naar links) ----------
B = basis.copy()
# oud lensvlak (r29-40, x13-24) eerst leeg naar wit; dan de nieuwe lens erin
R10LENS = {29: (17, 20), 30: (15, 22), 31: (14, 23), 32: (14, 23), 33: (13, 24), 34: (13, 24), 35: (13, 24), 36: (13, 24),
           37: (14, 23), 38: (15, 23), 39: (15, 22), 40: (17, 20)}   # zwarte rand + binnenkant van de r10-lens
for y, (x0, x1) in R10LENS.items():
    B[y, x0:x1 + 1] = -1
# r10-binnenkant 1 px naar links: B(x,y) = r10(x+1,y) voor iris + binnenste ringpixel
LENS_B = {  # rij: (zwart links, zwart rechts) ; binnenkant ertussen komt uit r10 (x+1)
    30: [(16, 19)], 31: [(14, 15), (20, 21)], 32: [(14, 14), (21, 21)], 33: [(13, 13), (22, 22)], 34: [(13, 13), (22, 22)],
    35: [(13, 13), (22, 22)], 36: [(13, 13), (22, 22)], 37: [(14, 14), (21, 21)], 38: [(15, 15), (20, 21)], 39: [(16, 19)]}
for y, segs in LENS_B.items():
    for x0, x1 in segs:
        for x in range(x0, x1 + 1): B[y, x] = 1
    if len(segs) == 2:
        for x in range(segs[0][1] + 1, segs[1][0]): B[y, x] = r10[y, x + 1]
# bovenste en onderste ringrij: r31 en r38 uit r10 (x+1) staan er al via de lus; de r10-ringrijen r30 en r39 vervallen
# de vrijgekomen pixels rond de lens (-1): wit volgens het verloop, links/boven zoals de r10-witring daar
for y in range(29, 41):
    for x in range(13, 25):
        if B[y, x] == -1:
            B[y, x] = toon(x, y, False)
LB = {30: 19, 31: 21, 32: 21, 33: 22, 34: 22, 35: 22, 36: 22, 37: 21, 38: 21, 39: 19}
koepel(B, LB)
# onder de lens (r40) liep in r10 de lensrand; nu binnenwit tot aan de ring
for x in range(15, 24):
    if B[40, x] == 1: B[40, x] = toon(x, 40, False)
B[40, 16] = 3   # r10-pixel 4 stond los tussen twee 3-en nu de lensrand erboven weg is

# ---------- variant C: lens even groot, 1 px naar links (met wit + rand links mee) ----------
C = basis.copy()
SEG = {29: (13, 20), 30: (13, 22), 31: (13, 23), 32: (12, 23), 33: (12, 24), 34: (12, 24), 35: (12, 24), 36: (11, 24),
       37: (11, 23), 38: (13, 23), 39: (13, 22), 40: (13, 20), 41: (14, 22)}
for y, (x0, x1) in SEG.items():
    C[y, x0 - 1:x1] = r10[y, x0:x1 + 1]
    C[y, x1] = -1
for y in range(29, 42):
    for x in range(10, 26):
        if C[y, x] == -1: C[y, x] = toon(x, y, False)
C[38, 11] = 1   # 1-px gaatje tussen paneelrand en koepelrand dicht (rand loopt door, zoals r37)
LC = {y: v - 1 for y, v in LA.items()}
koepel(C, LC)

def sla(arr, naam):
    im = Image.fromarray(arr.astype('uint8'), 'P'); im.putpalette(pal + [0] * (768 - len(pal)))
    im.save(naam, transparency=0)
    b = Image.new('RGBA', (64, 64), (255, 255, 255, 255)); rgba = im.convert('RGBA'); m = np.array(rgba); m[arr == 0, 3] = 0; b.alpha_composite(Image.fromarray(m))
    b.convert('RGB').resize((512, 512), Image.NEAREST).save(naam.replace('.png', '_8x.png'))
for nm, arr in (('var_a', A), ('var_b', B), ('var_c', C)):
    assert arr.min() >= 0
    sla(arr, nm + '.png'); np.save(nm + '.npy', arr)
    d = arr != r10
    print(nm, 'afwijkend t.o.v. r10:', d.sum(), ' bovenkant', d[14:21, 18:42].sum(), ' koepel/lens', d[26:46, 8:31].sum(), ' kleuren', len(np.unique(arr)))
