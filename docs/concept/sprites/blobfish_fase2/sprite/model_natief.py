# Model op het NATIEVE raster van r5 (99x99, pitch 10,24): r5 natief + 2 lagen eronder volgens lagen/stapel_kleur.py
# (band = puddingvoet y 672-820 op 1024-schaal = natieve rijen 65-76; telkens 6% breder via kolommen dupliceren (NEAREST),
#  gecentreerd op x=512, 64 px (6,25 natieve rij) lager; omkleuring = kleur() uit stapel_kleur.py, zwarte lijn blijft).
import sys, colorsys; from PIL import Image; import numpy as np
SH = [int(a) for a in (sys.argv[1:3] if len(sys.argv) > 2 else (6, 12))]
a = np.array(Image.open('natief_r5.png').convert('RGBA'))
a[(a[..., :3].astype(int).sum(2) >= 720)] = (0, 0, 0, 0)
P = 8                                   # marge links/rechts
full = np.zeros((99 + 16, 99 + 2 * P, 4), 'uint8'); full[:99, P:P + 99] = a
band = a[65:77].copy()
def kleur(b, tint, verz, helder):       # 1-op-1 uit lagen/stapel_kleur.py
    rgb = b[..., :3] / 255.0; o = b.copy()
    h, s, v = np.vectorize(colorsys.rgb_to_hsv)(rgb[..., 0], rgb[..., 1], rgb[..., 2])
    lijn = v < 0.25
    s2 = np.clip(s * verz + 0.15, 0, 1); v2 = v * helder
    r, g, bb = np.vectorize(colorsys.hsv_to_rgb)(np.full_like(h, tint / 360), s2, v2)
    nieuw = (np.dstack([r, g, bb]) * 255).astype(np.uint8)
    o[..., :3] = np.where(lijn[..., None], b[..., :3], nieuw)
    return o
K = [(355, 1.5, 0.85), (340, 1.6, 0.68)]
canvas = Image.new('RGBA', (full.shape[1], full.shape[0]), (0, 0, 0, 0))
for i in (2, 1):
    b = Image.fromarray(kleur(band, *K[i - 1])); w = round(99 * 1.06 ** i)
    b = b.resize((w, b.height), Image.NEAREST)
    canvas.alpha_composite(b, (P + (99 - w) // 2, 65 + SH[i - 1]))
canvas.alpha_composite(Image.fromarray(full), (0, 0))
canvas.save('model_natief.png')
lab = np.zeros(full.shape[:2], 'uint8')            # 0 lijf, 1 rode laag, 2 bordeaux laag (zichtbaar deel)
for i in (2, 1):
    w = round(99 * 1.06 ** i); x0 = P + (99 - w) // 2
    m = np.array(Image.fromarray(band[..., 3]).resize((w, band.shape[0]), Image.NEAREST)) > 0
    sub = lab[65 + SH[i-1]:65 + SH[i-1] + band.shape[0], x0:x0 + w]; sub[m] = i
lab[full[..., 3] > 0] = 0
np.save('label_natief.npy', lab)
m = np.array(canvas)[..., 3] > 0; yy, xx = np.where(m)
print('maat', xx.max() - xx.min() + 1, yy.max() - yy.min() + 1, 'bbox', xx.min(), xx.max(), yy.min(), yy.max())
w = Image.new('RGBA', canvas.size, (255, 255, 255, 255)); w.alpha_composite(canvas)
w.convert('RGB').resize((canvas.width * 8, canvas.height * 8), Image.NEAREST).save('model_natief_8x.png')
