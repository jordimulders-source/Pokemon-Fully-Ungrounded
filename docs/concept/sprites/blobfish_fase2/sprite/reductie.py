# Kale reductie model_natief (92x68) -> 1,5x kleiner (oppervlak-middeling). Lijnen: aandeel zwarte modelcellen per spritepixel.
# Uitvoer: kaal_rgb.npy (gemiddelde vulkleur), alpha.npy (dekking), lijnfrac.npy, lijnkleur.npy
import sys; from PIL import Image; import numpy as np
F = 1.5; phx, phy = [float(v) for v in (sys.argv[1:3] if len(sys.argv) > 2 else (0, 0))]
a = np.asarray(Image.open('model_natief.png').convert('RGBA')).astype(float)
al = a[..., 3] > 0; rgb = a[..., :3]; lum = rgb @ [0.299, 0.587, 0.114]
ln = al & (rgb.max(2) < 70)   # zwarte modellijn (zelfde als v<0.25 in stapel_kleur)
lab = np.load('label_natief.npy')
yy, xx = np.where(al); x0, y0 = xx.min() - phx, yy.min() - phy
W = int(np.ceil((xx.max() + 1 - x0) / F)); H = int(np.ceil((yy.max() + 1 - y0) / F))
def ov(lo, hi, n):  # overlap van [lo,hi) met cel n
    return max(0., min(hi, n + 1) - max(lo, n))
C = np.zeros((H, W, 3)); LB = np.zeros((H, W, 3)); A = np.zeros((H, W)); L = np.zeros((H, W)); LC = np.zeros((H, W, 3))
for j in range(H):
    for i in range(W):
        sx, sy = x0 + i * F, y0 + j * F; tw = 0; cw = 0; c = np.zeros(3); lw = 0; lc = np.zeros(3); lmin = 999
        for y in range(int(np.floor(sy)), int(np.ceil(sy + F))):
            for x in range(int(np.floor(sx)), int(np.ceil(sx + F))):
                w = ov(sx, sx + F, x) * ov(sy, sy + F, y)
                if w <= 0: continue
                tw += w
                if not (0 <= y < a.shape[0] and 0 <= x < a.shape[1]) or not al[y, x]: continue
                cw += w
                LB[j, i, lab[y, x]] += w
                if ln[y, x]:
                    lw += w
                    if lum[y, x] < lmin: lmin = lum[y, x]; lc = rgb[y, x]
                else: c += w * rgb[y, x]
        A[j, i] = cw / tw; L[j, i] = lw / tw; LC[j, i] = lc
        C[j, i] = c / (cw - lw) if cw - lw > 1e-6 else lc
# lijncentra: elke zwarte modelcel kleurt precies de spritepixel waar haar middelpunt in valt (dunne lijnen blijven 1 px en doorlopend)
LM = np.zeros((H, W), bool)
for y, x in zip(*np.where(ln)):
    i, j = int((x + 0.5 - x0) // F), int((y + 0.5 - y0) // F)
    if 0 <= i < W and 0 <= j < H: LM[j, i] = True
np.save('lijncentra.npy', LM)
# donkere binnenlijnen van het lijf (donker oudroze, geen zwart): zelfde middelpunt-regel -> tweede lijnkaart
ln2 = al & ~ln & (lab == 0) & (lum < 80)
LM2 = np.zeros((H, W), bool)
for y, x in zip(*np.where(ln2)):
    i, j = int((x + 0.5 - x0) // F), int((y + 0.5 - y0) // F)
    if 0 <= i < W and 0 <= j < H: LM2[j, i] = True
np.save('lijncentra2.npy', LM2 & ~LM)
np.save('kaal_rgb.npy', C); np.save('label.npy', LB.argmax(2)); np.save('alpha.npy', A); np.save('lijnfrac.npy', L); np.save('lijnkleur.npy', LC)
print('maat', W, H)
