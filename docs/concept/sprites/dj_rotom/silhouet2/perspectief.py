"""DJ Rotom silhouet 2: het 3/4-perspectief van de bron sterker maken (2D-vervorming van de bron zelf).
Nabij (rechts) groter, veraf (links) kleiner en iets smaller; boven- en onderlijn kantelen rond 62% van de hoogte.
Gebruik: python3 perspectief.py <bron> <uitmap> k1 k2 ..."""
import sys
from PIL import Image
import numpy as np
bron, uit, ks = sys.argv[1], sys.argv[2], [float(k) for k in sys.argv[3:]]
im = Image.open(bron).convert('RGBA')
a = np.array(im)[..., 3]; ys, xs = np.where(a > 128)
src = np.array(im.crop((xs.min(), ys.min(), xs.max() + 1, ys.max() + 1))).astype(float)
h, w = src.shape[:2]
for k in ks:
    # horizontaal: projectieve 1D-kaart, links samengedrukt, rechts uitgerekt
    A = 1 + k                                          # horizontaal milder: de kop blijft breed
    f = lambda u: u * A / (1 + (A - 1) * u)            # bron u -> doel t (f'(0)=A>1?) -> omgekeerd gebruiken
    # doel t -> bron u (inverse van f): links in het doel = minder bron-breedte per px? we willen links smal: doel = f^-1
    finv = lambda t: t / (A - (A - 1) * t)             # inverse van f
    # links smal in doel: doel t = finv(u) heeft afgeleide 1/A links -> smal. Dus bron u = f(t).
    sc = lambda u: (1 - k) + 2 * k * u                 # hoogteschaal per bron-kolom
    YA = 0.62                                          # vast punt (fractie van boven): boven- en onderlijn kantelen mee
    H = int(h * (1 + k)) + 2
    T = np.linspace(0, 1, w)
    U = f(T)                                           # bronkolom voor elke doelkolom
    out = np.zeros((H, w, 4))
    Y = np.arange(H)[:, None]
    for X in range(w):
        u = U[X]; s = sc(u)
        sx = min(w - 1, int(round(u * (w - 1))))
        ay_d = YA * (H - 1); ay_s = YA * (h - 1)
        sy = ay_s + (Y[:, 0] - ay_d) / s                 # rond het vaste punt
        ok = (sy >= 0) & (sy <= h - 1)
        out[ok, X] = src[np.round(sy[ok]).astype(int), sx]
    Image.fromarray(out.astype('uint8'), 'RGBA').save(f'{uit}/bron_k{k:.2f}.png')
    print(k, w, H)
