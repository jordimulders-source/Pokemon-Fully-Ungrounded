# oog.py: Jordi's oog (20 nov, letterlijk): "je kan voor het oog desnoods 1 zwarte pixel doen omringd door óf 4 óf 6
# rode pixels, omringd door een cirkel aan blauw" · "je hebt precies genoeg ruimte voor mijn oog idee, zonder dat je
# iets anders hoeft te veranderen". Pupil = de zwarte pupilpixel uit de reductie (9,30).
# A = 4 rood (plus), B = 6 rood (3x3 zonder de twee hoeken aan de snavelkant). Ring = 8-buren in blauw (12).
# Alleen pixels in het oog/blauwe vlak veranderen; elke wijziging wordt gelogd.
import numpy as np, sys
from PIL import Image
from palet import PAL
S0 = np.load('auto.npy')
P = (9, 30)                                   # (x, y)
VAR = {'A': [(0, -1), (-1, 0), (1, 0), (0, 1)],
       'B': [(0, -1), (1, -1), (-1, 0), (1, 0), (0, 1), (1, 1)]}
def maak(v):
    S = S0.copy(); x, y = P
    S[y, x] = 1
    rood = [(x + dx, y + dy) for dx, dy in VAR[v]]
    for a, b in rood: S[b, a] = 14
    kern = set(rood) | {P}
    for a, b in kern:
        for dx in (-1, 0, 1):
            for dy in (-1, 0, 1):
                q = (a + dx, b + dy)
                if q not in kern and S[q[1], q[0]] in (12, 14): S[q[1], q[0]] = 12   # lijnrand van het gezicht blijft
    d = np.argwhere(S != S0)
    log = ['(%d,%d) %d->%d' % (c, r, S0[r, c], S[r, c]) for r, c in d]
    return S, log
def bewaar(S, naam):
    im = Image.fromarray(S.astype(np.uint8), 'P'); pal = []
    for c in PAL: pal += list(c)
    im.putpalette(pal + [0] * (768 - len(pal))); im.save(naam, transparency=0)
    return im
if __name__ == '__main__':
    for v in 'AB':
        S, log = maak(v); bewaar(S, 'hoatzin_oog%s.png' % v)
        print(v, len(log), 'px:', ' '.join(log))
