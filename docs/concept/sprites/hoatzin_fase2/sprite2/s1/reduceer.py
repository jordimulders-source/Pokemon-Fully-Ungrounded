# reduceer.py: kale reductie van MODEL.png naar 64x64 (oppervlakgewogen).
# Per modelpixel een klasse (dichtstbijzijnde modeltint); per spritepixel:
#   alpha = aandeel figuur; zone/toon = dominante klasse van de VLAKpixels (lijnen tellen niet mee);
#   lijnaandeel apart bewaard (voor binnenlijnen).
# Uit: onderlaag.npy (klassekaart, 0 = transparant), lijn.npy (lijnaandeel), alpha.npy, onderlaag.png
import numpy as np
from PIL import Image
from scipy import ndimage as nd
from klassen import MODELTINT, NAMEN

M = '../../MODEL.png'
a = np.array(Image.open(M).convert('RGB')).astype(int)
w = a.min(2) >= 248
lab, n = nd.label(w)
sz = nd.sum(w, lab, range(1, n + 1))
bg = np.isin(lab, [i + 1 for i in range(n) if sz[i] >= 50])   # buiten + lucht tussen vleugel en kop
fig = ~bg
ys, xs = np.where(fig)
X0, X1, Y0, Y1 = xs.min(), xs.max() + 1, ys.min(), ys.max() + 1
BREED = 62
s = (X1 - X0) / BREED
HOOG = int(np.ceil((Y1 - Y0) / s))
ox = (64 - BREED) // 2          # kolom 1..62
oy = 63 - HOOG                  # onderkant op rij 62
print('schaal', round(s, 3), 'hoogte', HOOG, 'bbox', X0, X1, Y0, Y1)

# klasse per modelpixel
T = np.array(MODELTINT, float)                       # K x 3, index 0 = lijn
d = ((a[:, :, None, :] - T[None, None]) ** 2).sum(-1)
kl = d.argmin(-1)                                     # 0 = lijn
kl[a.max(2) <= 22] = 0
K = len(MODELTINT)

klas = np.zeros((64, 64), int); lijn = np.zeros((64, 64)); alpha = np.zeros((64, 64))
for j in range(64):
    for i in range(64):
        x0 = X0 + (i - ox) * s; y0 = Y0 + (j - oy) * s
        xa, xb, ya, yb = int(round(x0)), int(round(x0 + s)), int(round(y0)), int(round(y0 + s))
        if xb <= 0 or yb <= 0 or xa >= 1024 or ya >= 1024: continue
        xa, ya = max(xa, 0), max(ya, 0)
        f = fig[ya:yb, xa:xb]
        if f.size == 0: continue
        alpha[j, i] = f.mean()
        if alpha[j, i] < 0.12: continue
        k = kl[ya:yb, xa:xb][f]
        lijn[j, i] = (k == 0).mean()
        v = np.bincount(k[k > 0], minlength=K)
        klas[j, i] = v.argmax() if v.sum() else 0
        if v.sum() == 0: klas[j, i] = -1                    # puur lijn
np.save('alpha.npy', alpha); np.save('lijn.npy', lijn); np.save('onderlaag.npy', klas)
img = np.zeros((64, 64, 4), np.uint8)
for j in range(64):
    for i in range(64):
        if alpha[j, i] >= 0.45:
            c = MODELTINT[klas[j, i]] if klas[j, i] > 0 else MODELTINT[0]
            img[j, i] = (*c, 255)
Image.fromarray(img).save('onderlaag.png')
Image.fromarray(img).resize((512, 512), Image.NEAREST).save('onderlaag_8x.png')
print('pixels', int((alpha >= 0.45).sum()), 'pure lijn', int((klas == -1).sum()))
