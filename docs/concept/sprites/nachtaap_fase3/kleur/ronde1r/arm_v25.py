"""Ronde 1q (Claude, 5 nov): 1p + Jordi's tweede krabbel ('niet helemaal wat ik bedoelde, maar nu zijn we er bijna, als je nu nog een soort vorm kan maken zoals ik hier aangelijnd heb dan zijn we er'): onderrand van de arm volgt zijn boog van de pols naar de schouder; alles eronder lucht. Eerder: Jordi's krabbel ("zie mijn getekende lijnen, zou zoiets kunnen?"): de arm is een volle,
brede mouw van de vuist naar de schouder. Bovenrand begint hoog aan de rechterkant van de vuist en loopt schuin omlaag naar
de schouder; onderrand begint direct onder de vuist en volgt de kruin (spleet van 1 px). Basis ronde 1j (vuist, kop, lijf).
Shading als buis: lichtband boven, basis, schaduw onder; omlijning 1 aan de schaduwkant, 2 aan de lichtkant."""
import os
import numpy as np
from PIL import Image, ImageDraw
H = os.path.dirname(os.path.abspath(__file__))
src = Image.open(os.path.join(H, '../ronde1j/nachtaap_fase3.png')); a = np.array(src); pal = src.getpalette(); oud = a.copy()
def kop(x, y): return y >= 27 and x <= 13 + (y - 27)
SPLEET = {(14, 27), (15, 28), (16, 29), (17, 30), (18, 31)}
# omtrek van de mouw (64-px coördinaten, pixelranden): uit Jordi's lijnen
# Jordi: "maak het wel netter" / "en geen diagonale lijn, natuurlijke vorm" -> vloeiende krommes (Catmull-Rom):
# bovenrand bol (onderarmspier), onderrand zacht hol langs de kruin
def glad(pts, n=12):
    p = [np.array(q, float) for q in pts]; p = [p[0]] + p + [p[-1]]; out = []
    for i in range(1, len(p) - 2):
        a0, a1, a2, a3 = p[i - 1], p[i], p[i + 1], p[i + 2]
        for t in np.linspace(0, 1, n, endpoint=False):
            out.append(0.5 * (2 * a1 + (-a0 + a2) * t + (2 * a0 - 5 * a1 + 4 * a2 - a3) * t * t + (-a0 + 3 * a1 - 3 * a2 + a3) * t ** 3))
    out.append(p[-2]); return [tuple(q) for q in out]
BOVEN = glad([(11.0, 18.6), (14.0, 18.9), (17.5, 19.9), (20.3, 21.9), (22.2, 24.6), (23.8, 27.6), (25.6, 30.4), (27.0, 31.6)])
# Jordi's boog (krabbel 2, omgerekend naar 64 px): (10.2,22.2) -> (14.1,24.0) -> (17.2,26.3) -> (19.5,30.8)
ONDER = glad([(21.0, 32.6), (19.62, 32.08), (18.85, 31.4), (15.25, 27.28), (13.65, 26.42), (12.07, 25.5), (10.12, 23.57), (9.6, 21.6)])   # 25% van 1p naar Jordi's boog
K = 8
im = Image.new('L', (64 * K, 64 * K), 0); ImageDraw.Draw(im).polygon([(x * K, y * K) for x, y in BOVEN + ONDER], fill=255)
mouw = np.asarray(im).reshape(64, K, 64, K).mean((1, 3)) >= 127
# doorsnede-coördinaat voor de shading: afstand tot de bovenrand t.o.v. de breedte (as van vuist naar schouder)
P0, P1 = np.array([11.0, 21.0]), np.array([22.0, 30.5]); d = (P1 - P0) / np.linalg.norm(P1 - P0); n = np.array([d[1], -d[0]])  # n wijst naar boven-rechts
zone = np.zeros((64, 64), bool); zone[19:33, 9:28] = True
for y in range(64):
    for x in range(64):
        if kop(x, y) or a[y, x] in (6, 7, 8, 9, 10, 11, 12, 13, 14, 15): zone[y, x] = False
# oude arm in het vak weg (vuist boven rij 21 en lijf rechts-onder blijven)
for y, x in zip(*np.nonzero(zone)):
    if y >= 21 and x >= 9 and not (y >= 31 and x >= 21) and y < 32: a[y, x] = 0
sel = mouw & zone
proj = {}
for y, x in zip(*np.nonzero(sel)):
    proj[(y, x)] = (x + 0.5 - P0[0]) * n[0] + (y + 0.5 - P0[1]) * n[1]
lo, hi = min(proj.values()), max(proj.values())
for (y, x), p in proj.items():
    t = (hi - p) / (hi - lo)          # 0 = bovenrand (licht), 1 = onderrand (schaduw)
    a[y, x] = 5 if t < 0.3 else (4 if t < 0.7 else 3)
for (x, y) in SPLEET: a[y, x] = 0
for y, x in zip(*np.nonzero(sel)):
    if (x, y) in SPLEET: continue
    if any(a[y + dy, x + dx] == 0 for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))):
        t = (hi - proj[(y, x)]) / (hi - lo); a[y, x] = 2 if t > 0.5 else 1
# rug/schouder buiten de mouw terug uit 1j; vuist-arm-naad dicht; onderrand bij de kruin rustig
for y in range(19, 33):
    for x in range(23, 28):
        if a[y, x] == 0 and not sel[y, x] and oud[y, x] != 0: a[y, x] = oud[y, x]
a[21, 9] = 3; a[22, 9] = 1; a[26, 13] = 0; a[32, 22] = 4; a[31, 19] = 2
im = Image.fromarray(a, 'P'); im.putpalette(pal); im.save(os.path.join(H, 'v25.png'), transparency=0)
print('gewijzigd t.o.v. 1j:', int((a != oud).sum()))
op = [(x, y) for y in range(64) for x in range(64) if a[y, x] in (3, 4, 5) and any(
    0 <= y + dy < 64 and 0 <= x + dx < 64 and a[y + dy, x + dx] == 0 for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)))]
print('open randen', op)
