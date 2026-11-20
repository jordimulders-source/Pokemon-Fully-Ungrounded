# check.py [png]: dambord (2x2 a/b/b/a), om-en-om op de buitenrand (lijn en selout wisselen 3x achter elkaar langs de rand),
# zwarte klonten (2x2 blok lijnkleur 1 dat niet aan de achtergrond grenst = binnenklont)
import sys, numpy as np; from PIL import Image
a = np.array(Image.open(sys.argv[1] if len(sys.argv) > 1 else 'hoatzin.png')).astype(int)
H, W = a.shape
dam = []
for y in range(H-1):
    for x in range(W-1):
        p, q, r, s = a[y,x], a[y,x+1], a[y+1,x], a[y+1,x+1]
        if p and q and p == s and q == r and p != q: dam.append((x, y, p, q))
bg = a == 0
rand = (a > 0) & (np.pad(bg, 1, constant_values=True)[1:-1, :-2] | np.pad(bg, 1, constant_values=True)[1:-1, 2:] |
                  np.pad(bg, 1, constant_values=True)[:-2, 1:-1] | np.pad(bg, 1, constant_values=True)[2:, 1:-1])
# om-en-om: op randpixels, rij of kolom met patroon 1,x,1,x (x != 1, x selout) over 4 opeenvolgende randpixels
oeo = []
for y in range(H):
    for x in range(W-3):
        v = a[y, x:x+4]; r_ = rand[y, x:x+4]
        if r_.all() and v[0] == v[2] == 1 and v[1] == v[3] and v[1] not in (0, 1): oeo.append((x, y, 'rij'))
for x in range(W):
    for y in range(H-3):
        v = a[y:y+4, x]; r_ = rand[y:y+4, x]
        if r_.all() and v[0] == v[2] == 1 and v[1] == v[3] and v[1] not in (0, 1): oeo.append((x, y, 'kol'))
klont = []
for y in range(H-1):
    for x in range(W-1):
        b = a[y:y+2, x:x+2]
        if (b == 1).all() and not rand[y:y+2, x:x+2].any(): klont.append((x, y))
print('dambord', len(dam), dam[:20]); print('om-en-om', len(oeo), oeo[:20]); print('zwarte klonten (binnen)', len(klont), klont[:20])
