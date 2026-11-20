# lijnen.py: modellijnen naar het spriteraster. Cel = lijn als er in het midden (60%) van de cel
# genoeg zwarte modelpixels liggen. Uit: modellijn.npy (aandeel lijn in het celmidden)
import numpy as np
DX, DY = map(float, open('fase.txt').read().split())
kl = np.load('modelklas.npy')
X0, Y0, s = 97, 125, 833 / 62; ox, oy = 1, 5
L = np.zeros((64, 64))
for j in range(64):
    for i in range(64):
        cx = X0 + (i - ox + .5 + DX) * s; cy = Y0 + (j - oy + .5 + DY) * s; h = s * .3
        xa, xb, ya, yb = int(cx - h), int(cx + h) + 1, int(cy - h), int(cy + h) + 1
        if xb <= 0 or yb <= 0 or xa >= 1024 or ya >= 1024: continue
        c = kl[max(ya, 0):yb, max(xa, 0):xb]
        L[j, i] = (c == 0).mean()
np.save('modellijn.npy', L)
