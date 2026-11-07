"""Ronde 1n (Claude, 5 nov): vuist + pols + arm in één stuk uit het model (Jordi: "nee we stoppen niet met de arm, de arm
moet goed"). Bron: silhouet/onderlaag_256.png (model in hetzelfde vak), per 64-pixel gemiddeld. Omlijning waar het model
zijn lijn heeft (paarsig: R >= G-4), vacht 5/4/3 op helderheid. Kop, maan, rug en rest = ronde 1j; spleet van 1 px langs de
kop zoals 1k. Daarna met de hand opgeschoond (zie HAND)."""
import os
import numpy as np
from PIL import Image
H = os.path.dirname(os.path.abspath(__file__))
src = Image.open(os.path.join(H, '../ronde1j/nachtaap_fase3.png')); a = np.array(src); pal = src.getpalette(); oud = a.copy()
M = np.array(Image.open(os.path.join(H, '../../silhouet/onderlaag_256.png')).convert('RGBA')).astype(float)
al = M[..., 3] / 255; w = al.reshape(64, 4, 64, 4); A = w.mean((1, 3))
C = (M[..., :3] * al[..., None]).reshape(64, 4, 64, 4, 3).sum((1, 3)) / np.maximum(w.sum((1, 3)), 1e-6)[..., None]
lum = C.mean(2); lijn = (C[..., 0] - C[..., 1]) > -4
def kop_sprite(x, y): return y >= 27 and x <= 13 + (y - 27)
SPLEET = [(14, 27), (15, 28), (16, 29), (17, 30), (18, 31)]
# vak van vuist + arm in de sprite: rij 13-31, x 0-22 (rechts daarvan rug/been: blijft)
zone = np.zeros((64, 64), bool); zone[13:32, 0:23] = True
for y in range(13, 32):
    for x in range(0, 23):
        if kop_sprite(x, y) or (y >= 30 and x >= 21): zone[y, x] = False
for y, x in zip(*np.nonzero(zone)):
    if a[y, x] in (13, 14, 15, 6, 7, 8, 9, 10, 11, 12): zone[y, x] = False   # maan/gezicht/gloed nooit
# armvorm uit het model
for y, x in zip(*np.nonzero(zone)):
    if A[y, x] < 0.5: a[y, x] = 0; continue
    if lijn[y, x]: a[y, x] = 1
    else: a[y, x] = 5 if lum[y, x] >= 125 else (4 if lum[y, x] >= 95 else (3 if lum[y, x] >= 72 else 2))
for x, y in SPLEET: a[y, x] = 0
# omlijning gesloten: vacht naast transparant wordt rand; lichtkant (links/onder) 2, schaduwkant (rechts/boven) 1
for y, x in zip(*np.nonzero(zone)):
    if a[y, x] in (3, 4, 5):
        n = {(dx, dy): a[y + dy, x + dx] == 0 for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)) if 0 <= y + dy < 64 and 0 <= x + dx < 64}
        if n.get((0, -1)) or n.get((1, 0)): a[y, x] = 1
        elif n.get((0, 1)) or n.get((-1, 0)): a[y, x] = 2
HAND = {}   # handmatige opschoning per pixel: (x, y): index (ingevuld na het bekijken)
for (x, y), c in HAND.items(): a[y, x] = c
im = Image.fromarray(a, 'P'); im.putpalette(pal); im.save(os.path.join(H, 'nachtaap_fase3.png'), transparency=0)
d = np.argwhere(a != oud); print('gewijzigd t.o.v. 1j:', len(d), 'px, rijen', min(d[:, 0]), '-', max(d[:, 0]))
op = [(x, y) for y in range(64) for x in range(64) if a[y, x] in (3, 4, 5) and any(
    0 <= y + dy < 64 and 0 <= x + dx < 64 and a[y + dy, x + dx] == 0 for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)))]
print('open randen', op)
