"""Ronde 1o (Claude, 5 nov): vuistarm schoon getekend als sprite (Jordi: "je bent niet aan het kijken naar wat er goed
passend uit ziet he"). Route uit het model (onderarm recht omlaag uit de vuist, elleboog links op de kruin, bovenarm schuin
naar de schouder); vorm zoals Gen 3 (Medicham/Machamp): twee buizen van gelijke dikte (5 px) met een ronde elleboog, de
onderarm groeit uit de vuist (geen rand ertussen), licht linksboven, spleet van 1 px langs de kop (Jordi: "pixellijn ruimte
is prima"). Basis ronde 1j (vuist, kop, lijf)."""
import os
import numpy as np
from PIL import Image
H = os.path.dirname(os.path.abspath(__file__))
src = Image.open(os.path.join(H, '../ronde1j/nachtaap_fase3.png')); a = np.array(src); pal = src.getpalette(); oud = a.copy()
def kop(x, y): return y >= 27 and x <= 13 + (y - 27)
SPLEET = {(14, 27), (15, 28), (16, 29), (17, 30), (18, 31)}
BUIZEN = [  # (begin, eind, straal, lichtrichting in de doorsnede)
    ((11.0, 19.5), (11.2, 25.0), 2.6),      # onderarm: uit de vuist recht omlaag naar de elleboog
    ((11.6, 25.2), (21.0, 31.2), 2.6)]      # bovenarm: van de elleboog schuin naar de schouder
K = 8
ys, xs = np.mgrid[0:64 * K, 0:64 * K] / K
best_t = np.full(ys.shape, 9.0); inside = np.zeros(ys.shape, bool)
for (x0, y0), (x1, y1), r in BUIZEN:
    d = np.array([x1 - x0, y1 - y0]); L = np.linalg.norm(d); d /= L; n = np.array([-d[1], d[0]])
    if n[0] + n[1] > 0: n = -n            # normaal wijst naar linksboven (lichtkant)
    px, py = xs - x0, ys - y0
    s = np.clip(px * d[0] + py * d[1], 0, L)
    qx, qy = px - s * d[0], py - s * d[1]
    dist = np.hypot(qx, qy)
    t = -(qx * n[0] + qy * n[1]) / r      # -1 = lichtkant, +1 = schaduwkant
    m = dist <= r
    beter = m & (dist / r < np.abs(best_t))
    best_t = np.where(beter, t, best_t); inside |= m
cov = inside.reshape(64, K, 64, K).mean((1, 3)); T = best_t.reshape(64, K, 64, K).mean((1, 3))
arm = cov >= 0.5
zone = np.zeros((64, 64), bool); zone[21:33, 6:24] = True
for y in range(64):
    for x in range(64):
        if kop(x, y) or a[y, x] in (6, 7, 8, 9, 10, 11, 12, 13, 14, 15): zone[y, x] = False
for (x, y) in SPLEET: zone[y, x] = False
# oude arm weg (alles in de zone dat geen lijf is: rij 31-32 rechts van x20 = lijf, blijft)
for y, x in zip(*np.nonzero(zone)):
    if not (y >= 31 and x >= 21) and not (y >= 32): a[y, x] = 0
for (x, y) in SPLEET: a[y, x] = 0
for y, x in zip(*np.nonzero(arm & zone)):
    t = T[y, x]; a[y, x] = 5 if t < -0.3 else (4 if t < 0.35 else 3)
# omlijning: armpixel naast lege ruimte (of naast de kop via de spleet) -> 2 aan de lichtkant, 1 aan de schaduwkant
rand = []
for y, x in zip(*np.nonzero(arm & zone)):
    if any(a[y + dy, x + dx] == 0 for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))): rand.append((y, x))
for y, x in rand: a[y, x] = 2 if T[y, x] < 0 else 1
im = Image.fromarray(a, 'P'); im.putpalette(pal); im.save(os.path.join(H, 'nachtaap_fase3.png'), transparency=0)
d = np.argwhere(a != oud); print('gewijzigd t.o.v. 1j:', len(d))
op = [(x, y) for y in range(64) for x in range(64) if a[y, x] in (3, 4, 5) and any(
    0 <= y + dy < 64 and 0 <= x + dx < 64 and a[y + dy, x + dx] == 0 for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)))]
print('open randen', op)
