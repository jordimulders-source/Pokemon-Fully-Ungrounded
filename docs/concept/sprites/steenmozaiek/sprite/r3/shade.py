# r3 shading: per mozaiekstuk een tint lichter aan de lichtkant van de lichaamsvorm (licht linksboven),
# een tint donkerder aan de schaduwkant, als sikkel die de ronding volgt. Stukken, voegen, zwart en silhouet blijven.
# gebruik: python3 shade.py basis.png uit.png [sigma] [hi] [lo]
import sys, numpy as np
from PIL import Image
from scipy import ndimage as nd
IN, UIT = sys.argv[1], sys.argv[2]
SIG = float(sys.argv[3]) if len(sys.argv) > 3 else 2.5
HI = float(sys.argv[4]) if len(sys.argv) > 4 else 0.55
LO = float(sys.argv[5]) if len(sys.argv) > 5 else 0.25
CAP = float(sys.argv[6]) if len(sys.argv) > 6 else 12.0
im = Image.open(IN); a = np.array(im); pal = im.getpalette()
GRP = {6: 'B', 7: 'B', 8: 'B', 9: 'R', 10: 'R', 11: 'R', 12: 'C', 13: 'C', 14: 'C'}
TONES = {'B': [6, 7, 8], 'R': [9, 10, 11], 'C': [12, 13, 14]}
body = a > 0
# hoogteveld: afstand tot de rand, gladgemaakt -> normaal -> licht linksboven
dist = nd.distance_transform_edt(body)
h = nd.gaussian_filter(np.minimum(dist, CAP), SIG)
gy, gx = np.gradient(h)
n = np.dstack([-gx, -gy, np.full_like(h, 0.35)]); n /= np.linalg.norm(n, axis=2, keepdims=True)
L = np.array([-1.0, -1.0, 0.9]); L /= np.linalg.norm(L)
s = n @ L
fillpx = np.isin(a, list(GRP))
qh, ql = np.quantile(s[fillpx], [1 - HI, LO])  # HI/LO = aandeel licht/schaduw
off = np.zeros(a.shape, int); off[s > qh] = 1; off[s < ql] = -1
# uitzonderingen: muil en tanden (x<=15, 24<=y<=36), het oog met rand, verre poten altijd schaduw
ys, xs = np.mgrid[0:64, 0:64]
keep = ((xs <= 15) & (ys >= 24) & (ys <= 36)) | ((xs >= 10) & (xs <= 16) & (ys >= 17) & (ys <= 21))
far = ((xs >= 22) & (xs <= 30) & (ys >= 49)) | ((xs >= 33) & (xs <= 44) & (ys >= 43))
off[far] = -1
neck = (xs >= 14) & (xs <= 22) & (ys >= 31) & (ys <= 37)   # onderkant nek, onder de kaak: schaduw
off[neck] = -1
out = a.copy()
for g, T in TONES.items():
    m = np.isin(a, T) & ~keep
    lab, k = nd.label(m)
    for t in range(1, k + 1):
        mt = lab == t
        v, c = np.unique(a[mt], return_counts=True)
        base = T.index(v[np.argmax(c)])
        new = np.clip(base + off[mt], 0, 2)
        out[mt] = np.array(T)[new]
        # ontkorrelen binnen het stuk: clusters < 3 px nemen de meest voorkomende buurtint
        for it in range(2):
            for tn in T:
                l2, k2 = nd.label(mt & (out == tn))
                for q in range(1, k2 + 1):
                    mq = l2 == q
                    if mq.sum() >= 3: continue
                    ring = nd.binary_dilation(mq) & mt & ~mq
                    if ring.any():
                        vv, cc = np.unique(out[ring], return_counts=True); out[mq] = vv[np.argmax(cc)]
o = Image.fromarray(out.astype(np.uint8), 'P'); o.putpalette(pal); o.info['transparency'] = 0; o.save(UIT, transparency=0)
o.convert('RGBA').resize((512, 512), Image.NEAREST).save(UIT.replace('.png', '_8x.png'))
print(UIT, 'gewijzigd', int((out != a).sum()), 'alpha-diff', int(((out > 0) != body).sum()),
      'helderheid basis %.1f -> %.1f' % tuple((np.array(pal[:48]).reshape(16, 3)[x[x > 0]] @ [0.299, 0.587, 0.114]).mean() for x in (a, out)),
      'licht/donker-verdeling', [(int(t), int((out == t).sum())) for t in range(6, 15)])
