#!/usr/bin/env python3
"""Viscacha (Zapacha) frame 2: Gemini-bewerking overnemen, snorharen van frame 1 terugzetten.
Uitvoer in deze map. Frame 1 (af/viscacha.png) wordt alleen gelezen."""
import os, hashlib
import numpy as np
from PIL import Image

HIER = os.path.dirname(os.path.abspath(__file__))
F1 = os.path.join(HIER, '..', 'af', 'viscacha.png')
GEM = os.path.join(HIER, '..', 'gemini', 'frame2_ronde1.png')
SNOR = 15
SNOR_SHIFT = (0, -11)   # (dx, dy): snuit in frame 2 zit 11 rijen hoger; dx 0 past exact op Gemini's stompje

h_voor = hashlib.sha256(open(F1, 'rb').read()).hexdigest()
f1 = Image.open(F1)
assert f1.mode == 'P' and f1.size == (64, 64)
pal = f1.getpalette()[:48]
a = np.array(f1)
P = np.array(pal).reshape(16, 3).astype(int)
P[0] = 255  # achtergrond van Gemini is wit

# 1. Overnemen: middelste pixel per 16x16-vak -> dichtstbijzijnde paletkleur
g = np.array(Image.open(GEM).convert('RGB')).astype(int)
assert g.shape == (1024, 1024, 3)
s = g[8::16, 8::16]
ruw = ((s[:, :, None, :] - P[None, None]) ** 2).sum(-1).argmin(-1).astype(np.uint8)

b = ruw.copy()
log = []
def zet(x, y, v, waarom):
    log.append((x, y, int(b[y, x]), v, waarom)); b[y, x] = v

# 2. Zones. Buiten de bewogen zone (kop, voorpoten, wangpluk, borstlijn) is Gemini al
#    pixel voor pixel gelijk aan frame 1; we nemen daar toch expliciet frame 1 over.
beweeg = np.zeros((64, 64), bool)
beweeg[14:53, 0:36] = True        # kop, oren, snuitpluk, wangpluk, voorpoten, borst
vast = ~beweeg
n_vast_verschil = int((b[vast] != a[vast]).sum())
b[vast] = a[vast]

# 3. Snorharen: Gemini's stompje weg (alleen links van de snuit, x<=6),
#    de grijze pixel in de bek (11,25) is tandschaduw uit het model en blijft.
TAND = {(11, 25)}
for y, x in np.argwhere(ruw == SNOR):
    if (x, y) in TAND:
        continue
    assert x <= 6, (x, y)
    zet(x, y, 0, 'Gemini-snorstompje weg')
dx, dy = SNOR_SHIFT
snor1 = [(x, y) for y, x in np.argwhere(a == SNOR)]
for x, y in snor1:
    zet(x + dx, y + dy, SNOR, 'snorhaar frame 1 verplaatst')

# 4. Technische opschoning (vorm en pose bevroren)
#    a. witte vakken aan de buitenrand zijn achtergrond die doorschemert -> 0
for x, y in [(23, 21), (11, 38)]:
    assert b[y, x] == 13
    zet(x, y, 0, 'achtergrondwit aan de rand -> transparant')
#    b. buitenlijn in 'e' (anti-aliasing van Gemini) -> selout 2, zoals frame 1
for x, y in [(12, 21), (13, 21), (25, 21), (9, 24)]:
    assert b[y, x] == 14
    zet(x, y, 2, 'buitenlijn e -> selout 2')

# Controles
assert hashlib.sha256(open(F1, 'rb').read()).hexdigest() == h_voor, 'frame 1 aangeraakt'
assert b.max() <= 15 and set(np.unique(b)) <= set(np.unique(a)) | {13}, 'onbekende index'
assert set(np.unique(b)) <= set(range(16))
snor2 = sorted((int(x), int(y)) for y, x in np.argwhere(b == SNOR) if (x, y) not in TAND)
verwacht = sorted((x + dx, y + dy) for x, y in snor1)
assert len(snor2) == len(snor1) == len(verwacht), (len(snor2), len(snor1))
assert snor2 == verwacht, 'snorharen niet dezelfde vorm'
assert (b[vast] == a[vast]).all()
# buitenrand alleen in lijnkleuren (zoals frame 1: 1, 2, 8, f)
pd = np.pad(b, 1)
rand = (b != 0) & ((pd[:-2, 1:-1] == 0) | (pd[2:, 1:-1] == 0) | (pd[1:-1, :-2] == 0) | (pd[1:-1, 2:] == 0))
assert set(np.unique(b[rand])) <= {1, 2, 8, 15}, set(np.unique(b[rand]))

def pim(arr):
    im = Image.fromarray(arr.astype(np.uint8), 'P'); im.putpalette(pal)
    im.info['transparency'] = 0
    return im

pim(b).save(os.path.join(HIER, 'viscacha_frame2.png'), transparency=0)
pim(ruw).save(os.path.join(HIER, 'gemini64_ruw.png'), transparency=0)
pim(np.vstack([a, b])).save(os.path.join(HIER, 'viscacha_anim_front.png'), transparency=0)

def rgb(arr, k):
    im = pim(arr).convert('RGB'); x = np.array(im); x[arr == 0] = 255
    return Image.fromarray(x).resize((64 * k, 64 * k), Image.NEAREST)
K = 6
vel = Image.new('RGB', (64 * K * 3 + 2 * 12, 64 * K), 'white')
for i, arr in enumerate([a, ruw, b]):
    vel.paste(rgb(arr, K), (i * (64 * K + 12), 0))
vel.save(os.path.join(HIER, 'vel.png'))
fr = [rgb(a, K), rgb(b, K)]
fr[0].save(os.path.join(HIER, 'viscacha_frame2.gif'), save_all=True, append_images=[fr[1]],
           duration=[700, 250], loop=0, disposal=1)

# Verslag
def zone(x, y):
    if (x, y) in TAND: return 'bek'
    return 'kop/voorpoten'
print('vaste zone: Gemini wijkt af van frame 1 op', n_vast_verschil, 'px (overschreven met frame 1)')
print('bewogen zone t.o.v. frame 1:', int((b[beweeg] != a[beweeg]).sum()), 'px anders')
print('afwijkingen van de kale reductie (ruw -> af):', int((b != ruw).sum()), 'px')
from collections import Counter
print(Counter(w for *_, w in log))
with open(os.path.join(HIER, 'wijzigingen.txt'), 'w') as fh:
    for x, y, o, n, w in log:
        fh.write(f'({x},{y}) {o:x} -> {n:x}  {w}\n')
