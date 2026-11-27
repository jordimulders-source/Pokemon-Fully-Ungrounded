# Kale reductie: natief Gemini-raster (100x100, pitch 10,24) -> sprite op schaal S.
# Per spritepixel: oppervlakgewogen dekking van de natieve cellen.
#  - dekking niet-wit >= ALFA -> ondoorzichtig
#  - aandeel lijncellen (zwart) >= LIJN -> lijn (index 1)
#  - anders: gewogen gemiddelde van de vulcellen -> dichtstbijzijnde paletkleur
# Geen handwerk; uitvoer = onderlaag (kaal_<S>.png + .npy met indices).
import sys, numpy as np
from PIL import Image
D = __file__.rsplit('/', 1)[0]
S = float(sys.argv[1]) if len(sys.argv) > 1 else 0.6
LIJN = float(sys.argv[2]) if len(sys.argv) > 2 else 0.30
FX = float(sys.argv[3]) if len(sys.argv) > 3 else 0.0   # fase-verschuiving in natieve cellen
FY = float(sys.argv[4]) if len(sys.argv) > 4 else 0.0
TAG = sys.argv[5] if len(sys.argv) > 5 else str(S)
ALFA = 0.45
from palet import PAL

n = np.load(D + '/nat.npy').astype(float)
som = n.sum(2)
wit = som >= 720
# wit dat niet met de achtergrond verbonden is = oogwit (model), krijgt eigen kleur
from collections import deque
buiten = np.zeros_like(wit); q = deque([(0, 0)]); buiten[0, 0] = True
while q:
    y, x = q.popleft()
    for yy, xx in ((y+1,x),(y-1,x),(y,x+1),(y,x-1)):
        if 0 <= yy < 100 and 0 <= xx < 100 and wit[yy, xx] and not buiten[yy, xx]:
            buiten[yy, xx] = True; q.append((yy, xx))
oogwit = wit & ~buiten
n[oogwit] = (250, 250, 245)
wit = buiten
lijn = som < 150

# bbox van het model op het natieve raster
ys, xs = np.where(~wit)
x0, x1, y0, y1 = xs.min(), xs.max() + 1, ys.min(), ys.max() + 1
W = int(np.ceil((x1 - x0) * S)); H = int(np.ceil((y1 - y0) * S))
x0 -= FX; y0 -= FY
if FX: W += 1
if FY: H += 1

def gewichten(a0, a1):
    # natieve cellen die [a0,a1) overlappen, met overlap
    out = []
    for c in range(int(np.floor(a0)), int(np.ceil(a1))):
        o = min(a1, c + 1) - max(a0, c)
        if o > 1e-9: out.append((c, o))
    return out

idx = np.zeros((H, W), int)
pal = np.array(PAL, float)
for j in range(H):
    wy = gewichten(y0 + j / S, y0 + (j + 1) / S)
    for i in range(W):
        wx = gewichten(x0 + i / S, x0 + (i + 1) / S)
        tot = 0; nw = 0; ln = 0; col = np.zeros(3); cw = 0
        for (yy, a) in wy:
            for (xx, b) in wx:
                w = a * b; tot += w
                if yy >= 100 or xx >= 100 or wit[yy, xx]: continue
                nw += w
                if lijn[yy, xx]: ln += w
                else: col += w * n[yy, xx]; cw += w
        if nw / tot < ALFA: continue
        if ln / tot >= LIJN or cw == 0: idx[j, i] = 1; continue
        c = col / cw
        d = ((pal[2:] - c) ** 2).sum(1)
        idx[j, i] = 2 + int(d.argmin())

# centreren op 64x64, voeten op de onderrand-marge
out = np.zeros((64, 64), int)
ox = (64 - int(np.ceil(85*S))) // 2; oy = 64 - int(np.ceil(52*S)) - 4
if FY: oy -= 1
if FX: ox -= 1
out[oy:oy + H, ox:ox + W] = idx
np.save(D + f'/{"fase/" if TAG!=str(S) else ""}kaal_{TAG}.npy', out)
im = Image.fromarray(out.astype('uint8'), 'P')
flat = [0, 0, 0] * 16
for k, c in enumerate(PAL): flat[3*k:3*k+3] = c
im.putpalette(flat)
im.save(D + f'/{"fase/" if TAG!=str(S) else ""}kaal_{TAG}.png', transparency=0)
print('maat', W, 'x', H, 'px', (out > 0).sum())
