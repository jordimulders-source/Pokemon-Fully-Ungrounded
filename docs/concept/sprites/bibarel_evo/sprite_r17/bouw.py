# bouw.py ronde 17 (vanaf sprite_r16): lijnen en kleurgebruik naar ECHTE Gen 3 (GBA-sprites, *_gba.png + normal_gba.pal).
# Jordi: "ik kan me er toch niet aan ontlenen dat het lijnen en kleurengebruik anders is dan bij andere sprites" · "gen 1 t/m 3 he"
#        · "dat is geen goed vergelijkingsmateriaal, pak er 1 met een buikvlak" -> hoofdreferentie Kangaskhan (Gen 3).
# Studie: ../stijl_gen123/STUDIE.md.  Geen nieuwe vormen, silhouet en bevroren onderdelen ongewijzigd (assert).
# Draaien vanuit docs/concept/sprites/bibarel_evo:  python3 sprite_r17/bouw.py
import numpy as np
from PIL import Image, ImageDraw
R = '/home/user/Pokemon-Fully-Ungrounded/'
ch = '.KbcdfSCeLMogWwD'; I = {c: i for i, c in enumerate(ch)}
im16 = Image.open('sprite_r16/sprite.png'); PAL16 = np.array(im16.getpalette()[:48]).reshape(16, 3).astype('uint8')
r16 = np.asarray(im16).astype(int); o = r16.copy()

# ---- 1. palet (zelfde 15 + transparant; alleen kleuren, geen pixels)
#  bruin: Gen 3-opbouw (Kangaskhan/Ursaring/Teddiursa): tint bijna constant, licht iets geler en minder verzadigd,
#  verzadiging loopt op naar donker; lijnkleur b diep en verzadigd.  creme: warm geel-creme met gouden schaduw
#  (Kangaskhan-buik 255,255,148 / 238,205,106; Teddiursa 255,246,164 / 255,213,123 / 213,172,82), niet grijsbeige.
PAL = PAL16.copy()
NIEUW = {'f': (224, 184, 128), 'd': (192, 136, 80), 'c': (148, 96, 48), 'b': (88, 52, 20),
         'C': (248, 240, 192), 'M': (240, 216, 152), 'S': (216, 180, 112), 'D': (176, 136, 80)}
for k, v in NIEUW.items(): PAL[I[k]] = v

# ---- 2. pixels: alleen omkleuren binnen bestaande vormen
W = {}  # (x,y) -> nieuw teken
def zet(x, y, nieuw, oud=None):
    if oud: assert ch[r16[y, x]] in oud, (x, y, ch[r16[y, x]])
    W[(x, y)] = nieuw
# 2a. kruis: de mengband D tussen creme-schaduw S en bruin (rij 45-54) -> harde grens zoals Kangaskhan:
#     D die aan bruin/hand grenst -> c (bruine schaduw, model is hier donker 138-160), overige D -> S (creme-schaduw).
BRUIN = {I[c] for c in 'dcbfeKL'}
for y in range(45, 55):
    for x in range(30, 44):
        if r16[y, x] == I['D']:
            nb = [r16[y + dy, x + dx] for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))]
            zet(x, y, 'c' if any(n in BRUIN for n in nb) else 'S')
# 2b. rechts naast de broek, onder de arm (rij 35-43): losse d-pixels tussen S en de armlijn = lichte mengrand;
#     model is daar schaduw (145) -> c, zodat creme hard op bruine schaduw stoot.
for y in range(35, 44):
    xs = [x for x in range(36, 48) if r16[y, x] in (I['S'], I['M'])]
    if not xs: continue
    x = max(xs) + 1
    while r16[y, x] == I['d']: zet(x, y, 'c'); x += 1
# 2c. dijlijn rechts: gat in de binnenlijn (38,51) dichten (lijn loopt 38,50 / 38,52-54).
zet(38, 51, 'b', 'd')
# 2d. linkerdij/broek (rij 45-49): broek stoot daar zonder lijn op lichte d; de lijn b (22,50)-(27,54) loopt
#     omhoog door als donkere eigen tint c op de bestaande randpixel (model: lijn rond de broek).
for (x, y) in [(18, 45), (19, 46), (20, 47), (20, 48), (22, 49)]: zet(x, y, 'c', 'd')

for (x, y), n in W.items(): o[y, x] = I[n]

def save(idx, pad, z=None):
    im = Image.new('P', (64, 64)); im.putpalette(PAL.ravel().tolist() + [0] * 3 * 240)
    im.putdata(idx.astype('uint8').ravel().tolist()); im.save(pad, transparency=0)
    if z: Image.fromarray(PAL[idx]).resize((64 * z, 64 * z), Image.NEAREST).save(pad.replace('.png', f'_{z}x.png'))
save(o, 'sprite_r17/sprite.png', 8)

# ---- bewijs
diff = {(int(x), int(y)) for y, x in np.argwhere(o != r16)}
print('pixels omgekleurd:', len(diff), '| silhouet gewijzigd:', int(((o > 0) != (r16 > 0)).sum()))
assert diff == set(W) - {k for k, v in W.items() if I[v] == r16[k[1], k[0]]}
assert ((o > 0) == (r16 > 0)).all()
# bevroren onderdelen (staart o/g/W/w, gezicht/potlood e/L, tanden, ogen K/W rond de kop) onaangeraakt:
assert not any(r16[y, x] in [I[c] for c in 'ogWweLK'] for (x, y) in diff)
assert not any(y < 35 for (x, y) in diff)  # kop, kraag, klep, potlood, armen boven: 0 px
print('per teken:', {k: sum(1 for p in diff if ch[o[p[1], p[0]]] == k) for k in 'bcS'})

# ---- vel
def jasc(p):
    L = open(p).read().split('\n'); n = int(L[2]); return np.array([[int(v) for v in L[3 + i].split()] for i in range(n)], dtype='uint8')
def gen3(n):
    a = np.asarray(Image.open(R + f'graphics/pokemon/{n}/anim_front_gba.png'))[:64].astype(int)
    return a, jasc(R + f'graphics/pokemon/{n}/normal_gba.pal')
BG = (152, 208, 160)
def rgb(a, pal, bg=BG):
    t = np.zeros((64, 64, 3), 'uint8'); t[:] = bg; m = a > 0; t[m] = pal[a[m]]; return Image.fromarray(t)
big = lambda img, z: img.resize((64 * z, 64 * z), Image.NEAREST)
refs = [('kangaskhan', gen3('kangaskhan')), ('ursaring', gen3('ursaring')), ('teddiursa', gen3('teddiursa'))]
V = Image.new('RGB', (3 * 522 + 10, 22 + 256 + 30 + 512 + 30 + 64 + 40), 'white'); d = ImageDraw.Draw(V)
items = [('r17', rgb(o, PAL)), ('r16', rgb(r16, PAL16))] + [(n + ' (Gen 3 GBA)', rgb(*p)) for n, p in refs]
for i, (t, img) in enumerate(items):
    V.paste(big(img, 4), (10 + i * 266, 22)); d.text((10 + i * 266, 6), t + ' 4x', fill='black')
y = 22 + 256 + 30
for i, (t, img) in enumerate(items[:3]):
    V.paste(big(img, 8), (10 + i * 522, y)); d.text((10 + i * 522, y - 14), t + ' 8x', fill='black')
# Kangaskhan 8x rechts afgesneden naast de twee
V2 = V
y2 = y + 512 + 30
d.text((10, y2 - 14), '1x licht / donker: r17 r16 Kangaskhan Ursaring Teddiursa', fill='black')
for j, bg in enumerate([(248, 248, 248), (24, 24, 32)]):
    for i, (t, img) in enumerate(items):
        a, p = (o, PAL) if i == 0 else (r16, PAL16) if i == 1 else refs[i - 2][1]
        V.paste(rgb(a, p, bg), (10 + j * 380 + i * 70, y2))
V.save('sprite_r17/vel.png')
