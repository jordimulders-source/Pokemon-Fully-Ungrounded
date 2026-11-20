# reduceer.py: kale reductie van MODEL.png naar 64x64 (oppervlakgewogen).
# Per modelpixel een klasse (dichtstbijzijnde modeltint). Per spritepixel:
#   alpha = aandeel figuur; klasse = dominante tint van de VLAKpixels (zwarte lijnen en de
#   anti-aliasrand van 3 px naar de achtergrond tellen niet mee); per tint het aandeel van de cel.
# Uit: onderlaag.npy (klassekaart, 0 = geen), frac.npy (64x64xK aandeel per klasse), alpha.npy,
#      onderlaag.png (alpha >= 0.45, kale reductie), onderlaag_8x.png
import numpy as np
from PIL import Image
from scipy import ndimage as nd
from klassen import MODELTINT

M = '../../MODEL.png'
a = np.array(Image.open(M).convert('RGB')).astype(int)
w = a.min(2) >= 248
lab, n = nd.label(w)
sz = nd.sum(w, lab, range(1, n + 1))
bg = np.isin(lab, [i + 1 for i in range(n) if sz[i] >= 50])   # buiten + lucht tussen vleugel en kop
fig = ~bg
kern = nd.binary_erosion(fig, iterations=3)
ys, xs = np.where(fig)
X0, X1, Y0, Y1 = xs.min(), xs.max() + 1, ys.min(), ys.max() + 1
BREED = 62
s = (X1 - X0) / BREED
HOOG = int(np.ceil((Y1 - Y0) / s))
ox = (64 - BREED) // 2          # kolom 1..62
oy = 63 - HOOG                  # onderkant op rij 62
print('schaal', round(s, 3), 'hoogte', HOOG, 'bbox', X0, X1, Y0, Y1)

T = np.array(MODELTINT, float)
d = ((a[:, :, None, :] - T[None, None]) ** 2).sum(-1)
kl = d.argmin(-1)
kl[a.max(2) <= 22] = 0
kl[~fig] = -1
np.save('modelklas.npy', kl)
K = len(MODELTINT)

klas = np.zeros((64, 64), int); frac = np.zeros((64, 64, K)); alpha = np.zeros((64, 64))
for j in range(64):
    for i in range(64):
        x0 = X0 + (i - ox) * s; y0 = Y0 + (j - oy) * s
        xa, xb, ya, yb = int(round(x0)), int(round(x0 + s)), int(round(y0)), int(round(y0 + s))
        if xb <= 0 or yb <= 0 or xa >= 1024 or ya >= 1024: continue
        xa, ya = max(xa, 0), max(ya, 0)
        f = fig[ya:yb, xa:xb]
        if f.size == 0: continue
        alpha[j, i] = f.mean()
        if not f.any(): continue
        k = kl[ya:yb, xa:xb]
        frac[j, i] = np.bincount(k[f], minlength=K) / f.size
        kk = k[kern[ya:yb, xa:xb]]
        kk = kk[kk > 0]
        if kk.size == 0:
            kk = k[f]; kk = kk[kk > 0]
        klas[j, i] = np.bincount(kk, minlength=K).argmax() if kk.size else 0
np.save('alpha.npy', alpha); np.save('frac.npy', frac); np.save('onderlaag.npy', klas)
img = np.zeros((64, 64, 4), np.uint8)
for j in range(64):
    for i in range(64):
        if alpha[j, i] >= 0.45:
            img[j, i] = (*MODELTINT[klas[j, i]], 255)
Image.fromarray(img).save('onderlaag.png')
Image.fromarray(img).resize((512, 512), Image.NEAREST).save('onderlaag_8x.png')
print('pixels', int((alpha >= 0.45).sum()))
