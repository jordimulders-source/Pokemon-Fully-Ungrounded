# bouw.py ronde 18 (vanaf sprite_r17): meer en hardere belijning zoals Kangaskhan (Gen 3 GBA) en onze best belijnde sprites.
# Jordi: "de lijnen mogen ook iets harder, iets donkerder, kijk naar kangaskhan en ivm daarmee hoe weinig belijnd onze sprite is"
#        · "zelfs het buikvlak bijv" · "er zit iets tussen zwart en heel licht nog he"
#        · "dundragoon doet dat het beste van alle sprites die we gemaakt hebben, princadee en zapacha ook"
# Lijnverhouding gemeten (L lijn / L basisvlak): Kangaskhan 64/164=0,39; Zapacha 85/190=0,45; Dundragoon geel 109/218=0,50,
#   blauw 73/148=0,49. Buitenlijn bij allen bijna zwart.  -> bruin b: L 51 / d 147 = 0,35 (iets harder, Jordi "iets donkerder");
#   creme-lijn D: L 121 / C 236 = 0,51 (gouden lijn, zoals Dundragoons gele vlak).
# Plek van elke nieuwe lijn: model r10_k8 geprojecteerd op het spriteraster met de MINIMUM-luminantie per spritepixel
#   (model_min.npy); een lijn in het model (L < 75) binnen bruine vacht wordt een b-lijn. Geen nieuwe vormen, silhouet gelijk.
# Draaien vanuit docs/concept/sprites/bibarel_evo:  python3 sprite_r18/bouw.py
import numpy as np
from PIL import Image, ImageDraw
from scipy import ndimage
R = '/home/user/Pokemon-Fully-Ungrounded/'
ch = '.KbcdfSCeLMogWwD'; I = {c: i for i, c in enumerate(ch)}
im17 = Image.open('sprite_r17/sprite.png'); PAL17 = np.array(im17.getpalette()[:48]).reshape(16, 3).astype('uint8')
a = np.asarray(im17).astype(int); o = a.copy()
H, Wd = a.shape

# ---- model-minimum op het spriteraster (zelfde mapping als keuring_r15/proj.py)
def model_min():
    MK = np.asarray(Image.open('model/r10_k8.png').convert('RGB')).astype(float) @ [.299, .587, .114]
    s_ = 64 / 90; mn = np.full((64, 64), 255.)
    for y in range(64):
        for x in range(64):
            x0, x1 = x / s_, (x + 1) / s_; y0, y1 = 9 + (y - 6) / s_, 9 + (y + 1 - 6) / s_
            v = [MK[yy, xx] for yy in range(int(np.floor(y0)), int(np.ceil(y1))) for xx in range(int(np.floor(x0)), int(np.ceil(x1)))
                 if 0 <= yy < 99 and 0 <= xx < 99 and min(xx + 1, x1) - max(xx, x0) > .15 and min(yy + 1, y1) - max(yy, y0) > .15]
            if v: mn[y, x] = min(v)
    return mn
mn = model_min(); np.save('sprite_r18/model_min.npy', mn)

FUR = [I[c] for c in 'fdc']; CR = [I[c] for c in 'CMS']
N4 = ((1, 0), (-1, 0), (0, 1), (0, -1)); N8 = [(dx, dy) for dx in (-1, 0, 1) for dy in (-1, 0, 1) if dx or dy]
inb = lambda x, y: 0 <= x < 64 and 0 <= y < 64

# ---- 1. bruine binnenlijnen uit het model (romp/armen/benen; kop, gezicht, potlood, staart niet: rij >= 27, alleen vacht)
ster = np.isin(a, FUR) & (mn < 75); ster[:27] = False
lab, n = ndimage.label(ster | (a == I['b']), structure=np.ones((3, 3)))
nieuw = np.zeros_like(ster)
for k in range(1, n + 1):
    m = lab == k
    if m.sum() >= 3: nieuw |= m & ster
o[nieuw] = I['b']
# dunnen: een nieuwe lijnpixel met >= 3 lijnburen die weg kan zonder de lijn te breken, gaat terug naar vacht (1 px, taps)
lijn = lambda: np.isin(o, [I['b'], I['K']])
veranderd = True
while veranderd:
    veranderd = False
    for y, x in sorted(map(tuple, np.argwhere(nieuw & (o == I['b'])))):
        L = lijn(); nb = sum(L[y + dy, x + dx] for dx, dy in N8 if inb(x + dx, y + dy))
        if nb < 3: continue
        L2 = L.copy(); L2[y, x] = False
        sub = L2[max(0, y - 1):y + 2, max(0, x - 1):x + 2]
        if ndimage.label(sub, structure=np.ones((3, 3)))[1] == 1:
            o[y, x] = a[y, x]; nieuw[y, x] = False; veranderd = True
# schaduwtint naast de lijn (zoals Kangaskhan: D naast E): rechts/onder van een nieuwe lijnpixel f->d, d->c
schaduw = {}
for y, x in map(tuple, np.argwhere(nieuw & (o == I['b']))):
    for dx, dy in ((1, 0), (0, 1)):
        X, Y = x + dx, y + dy
        if inb(X, Y) and not nieuw[Y, X] and o[Y, X] in (I['f'], I['d']):
            schaduw[(X, Y)] = I['d'] if o[Y, X] == I['f'] else I['c']
for (X, Y), v in schaduw.items(): o[Y, X] = v

# 1b. handmatig na eigen controle op 8x (alleen binnen de modellijnen hierboven):
#   kraagonderrand doorlopend maken (gaten (29,32) en (31,32) tussen twee b-stukken), spoortje (28,33) terug;
#   schouderlijn rechts doorlopend: gat (44,35) dicht, dubbele pixel (44,36) terug; broekrand links: vachtsliver (22,49) wordt lijn.
for (x, y) in [(29, 32), (31, 32), (44, 35), (22, 49)]: o[y, x] = I['b']; nieuw[y, x] = True
for (x, y) in [(28, 33), (44, 36)]: o[y, x] = a[y, x]; nieuw[y, x] = False
for (x, y) in [(29, 33), (31, 33)]:
    if o[y, x] == I['c'] and a[y, x] == I['d']: o[y, x] = I['d']  # schaduw van het teruggezette spoortje

# ---- 2. losse korte b-stukjes (< 3 px, binnenin, niet aan een lijn) in de romp weghalen -> meest voorkomende vachtbuur
lab, n = ndimage.label(o == I['b'], structure=np.ones((3, 3)))
weg = []
for k in range(1, n + 1):
    m = lab == k
    pts = list(map(tuple, np.argwhere(m)))
    if len(pts) >= 3 or min(p[0] for p in pts) < 27: continue
    if any(inb(x + dx, y + dy) and o[y + dy, x + dx] in (I['K'], I['e'], I['L'], 0) for y, x in pts for dx, dy in N8): continue
    for y, x in pts:
        buren = [o[y + dy, x + dx] for dx, dy in N8 if inb(x + dx, y + dy) and o[y + dy, x + dx] in FUR]
        if buren: o[y, x] = max(set(buren), key=buren.count); weg.append((x, y))

# ---- 3. creme-vlak (borststuk, bandjes, broek) belijnd met een gouden lijn D, binnen het vlak, waar het nog geen lijn heeft
D_px = []
for y in range(27, 64):
    for x in range(14, 64):
        if a[y, x] not in CR: continue
        kanten = [(dx, dy) for dx, dy in N4 if inb(x + dx, y + dy) and o[y + dy, x + dx] in FUR]
        if y < 35: kanten = [k for k in kanten if k in ((1, 0), (0, 1))]  # smalle bandjes: alleen schaduwkant
        if kanten: D_px.append((x, y))
for x, y in D_px: o[y, x] = I['D']
# oogrand gebruikte D (gezicht): naar d, kleur blijft nagenoeg gelijk (176,136,80 -> 192,136,80); vorm ongewijzigd
for y, x in map(tuple, np.argwhere((a == I['D']))):
    if 14 <= y <= 18 and x >= 18: o[y, x] = I['d']

# ---- 4. palet
PAL = PAL17.copy()
PAL[I['b']] = (80, 44, 16)    # was (88,52,20) L59 -> L51
PAL[I['D']] = (160, 116, 48)  # was (176,136,80) L141 -> L121: gouden creme-lijn

def save(idx, pad, z=None):
    im = Image.new('P', (64, 64)); im.putpalette(PAL.ravel().tolist() + [0] * 3 * 240)
    im.putdata(idx.astype('uint8').ravel().tolist()); im.save(pad, transparency=0)
    if z: Image.fromarray(PAL[idx]).resize((64 * z, 64 * z), Image.NEAREST).save(pad.replace('.png', f'_{z}x.png'))
save(o, 'sprite_r18/sprite.png', 8)

# ---- bewijs
diff = o != a
print('nieuwe b-lijnpixels:', int((diff & (o == I['b'])).sum()), '| schaduw naast lijn:', len(schaduw),
      '| losse stukjes weg:', weg, '| creme-lijn D:', len(D_px), '| totaal gewijzigd:', int(diff.sum()))
assert ((o > 0) == (a > 0)).all(), 'silhouet'
assert not (diff & np.isin(a, [I[c] for c in 'ogWweLK'])).any(), 'gezicht/staart/potloodkern/buitenlijn aangeraakt'
assert not diff[:14].any(), 'kop boven rij 14'
pot = np.zeros_like(diff); pot[15:27, :14] = True; assert not (diff & pot).any(), 'potlood'

# ---- vel: r18 | r17 | Kangaskhan 4x en 8x ; 1x licht/donker ; + Dundragoon/Princadee/Zapacha 4x
def jasc(p):
    L = open(p).read().split('\n'); n = int(L[2]); return np.array([[int(v) for v in L[3 + i].split()] for i in range(n)], dtype='uint8')
BG = (152, 208, 160)
def rgb(idx, pal, bg=BG):
    t = np.zeros((64, 64, 3), 'uint8'); t[:] = bg; m = idx > 0; t[m] = pal[idx[m]]; return Image.fromarray(t)
def rgba(p, bg=BG):
    im = Image.open(R + p).convert('RGBA').crop((0, 0, 64, 64)); b = Image.new('RGBA', (64, 64), bg + (255,)); b.alpha_composite(im); return b.convert('RGB')
ka = np.asarray(Image.open(R + 'graphics/pokemon/kangaskhan/anim_front_gba.png'))[:64].astype(int)
kp = jasc(R + 'graphics/pokemon/kangaskhan/normal_gba.pal')
items = [('r18', lambda bg=BG: rgb(o, PAL, bg)), ('r17', lambda bg=BG: rgb(a, PAL17, bg)), ('Kangaskhan Gen 3 (GBA)', lambda bg=BG: rgb(ka, kp, bg))]
extra = [('Dundragoon', 'docs/concept/sprites/dundragoon/af/dundragoon.png'), ('Princadee', 'docs/concept/sprites/awki/af/awki.png'),
         ('Zapacha', 'docs/concept/sprites/viscacha/af/viscacha.png')]
V = Image.new('RGB', (3 * 522 + 10, 22 + 256 + 34 + 512 + 34 + 64 + 34 + 256 + 10), 'white'); d = ImageDraw.Draw(V)
for i, (t, f) in enumerate(items):
    V.paste(f().resize((256, 256), Image.NEAREST), (10 + i * 266, 22)); d.text((10 + i * 266, 6), t + ' 4x', fill='black')
y = 22 + 256 + 34
for i, (t, f) in enumerate(items):
    V.paste(f().resize((512, 512), Image.NEAREST), (10 + i * 522, y)); d.text((10 + i * 522, y - 14), t + ' 8x', fill='black')
y += 512 + 34
d.text((10, y - 14), '1x licht / donker: r18 r17 Kangaskhan', fill='black')
for j, bg in enumerate([(248, 248, 248), (24, 24, 32)]):
    for i, (t, f) in enumerate(items): V.paste(f(bg), (10 + j * 240 + i * 70, y))
y += 64 + 34
d.text((10, y - 14), 'onze best belijnde (Jordi): Dundragoon | Princadee | Zapacha 4x', fill='black')
for i, (t, p) in enumerate(extra): V.paste(rgba(p).resize((256, 256), Image.NEAREST), (10 + i * 266, y))
V.save('sprite_r18/vel.png')
