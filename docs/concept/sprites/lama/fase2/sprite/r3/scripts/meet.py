# Llamauler r3: meting van het model per spritepixel (geen tekenwerk).
# Model: gemini/poten/model_v3.png (1024², wit). Raster: 62 rijen van y 28 t/m 1003 -> s = 15,74 modelpx per spritepixel,
# rij 2..63 in de 64x64; kolommen gecentreerd op het midden van de modelinhoud.
# Gebruik: from meet import M  (M.cel(x,y) -> dict met dekking, klassen, gem. helderheid, gem. kleur per klasse)
import os, numpy as np
from PIL import Image
HIER = os.path.dirname(os.path.abspath(__file__))
FASE2 = os.path.abspath(os.path.join(HIER, '../../..'))
MODEL = os.path.join(FASE2, 'gemini/poten/model_v3.png')

a = np.asarray(Image.open(MODEL).convert('RGB')).astype(int).copy()
R, G, B = a[..., 0], a[..., 1], a[..., 2]
bg = a.min(2) >= 235

# naad van het plakwerk (model_v3.py plakt de voorpoten op y 815): witte spleet van een paar modelpx tussen wol en poot.
# Technisch dicht: een witte pixel met binnen 6 px erboven én eronder model krijgt de kleur van de pixel erboven.
H, W = bg.shape
naad = np.zeros_like(bg)
for y in range(780, 850):
    for d in range(1, 7):
        up = ~bg[y - d]
        for e in range(1, 7):
            if y + e >= H: break
            naad[y] |= bg[y] & up & ~bg[y + e]
ys, xs = np.nonzero(naad)
for y, x in sorted(zip(ys, xs)):
    a[y, x] = a[y - 1, x]
bg = a.min(2) >= 235
R, G, B = a[..., 0], a[..., 1], a[..., 2]
L = a.mean(2)

red = (R - G > 55) & (G - B < 25) & ~bg
yel = (G - B > 100) & (R > 170) & ~bg
grn = (G > R + 10) & ~bg & ~yel
blu = (B > R + 30) & ~bg
gry = (abs(R - G) < 16) & (abs(G - B) < 16) & (L < 140) & ~bg
brn = ~(bg | red | yel | grn | blu | gry)
yy, xx = np.mgrid[:H, :W]
ver = ((xx >= 735) & (yy >= 815)) | ((xx >= 395) & (xx < 500) & (yy >= 812) & (yy < 900))   # verre poten
KL = dict(red=red, yel=yel, grn=grn, blu=blu, gry=gry, fur=brn & ~ver, ver=brn & ver)

S = (1003 - 28 + 1) / 62.0
OY = 28 - 2 * S
fx = np.nonzero(~bg.all(0))[0]
OX = (fx.min() + fx.max() + 1) / 2 - 32 * S


def blok(x, y):
    xa, xb = int(round(OX + x * S)), int(round(OX + (x + 1) * S))
    ya, yb = int(round(OY + y * S)), int(round(OY + (y + 1) * S))
    return max(ya, 0), min(yb, H), max(xa, 0), min(xb, W)


def cel(x, y):
    ya, yb, xa, xb = blok(x, y)
    if yb <= ya or xb <= xa:
        return None
    sl = (slice(ya, yb), slice(xa, xb)); n = (yb - ya) * (xb - xa)
    fg = ~bg[sl]
    r = dict(dek=fg.sum() / n, n={k: int(v[sl].sum()) for k, v in KL.items()})
    r['lum'] = L[sl][fg].mean() if fg.any() else 255
    r['lmin'] = L[sl][fg].min() if fg.any() else 255
    r['rgb'] = {k: a[sl][v[sl]] for k, v in KL.items()}
    return r


if __name__ == '__main__':
    import sys
    X0, X1, Y0, Y1 = map(int, sys.argv[1:5])
    print('S=%.3f OX=%.1f OY=%.1f' % (S, OX, OY))
    print('    ' + ''.join('%8d' % x for x in range(X0, X1)))
    for y in range(Y0, Y1):
        row = []
        for x in range(X0, X1):
            c = cel(x, y)
            row.append('       .' if c is None or c['dek'] < .45 else '%4d/%3d' % (c['lum'], c['lmin']))
        print('%3d ' % y + ''.join(row))


# ---- binnenlijnen van het model (wol + verre poot, helderheid < 100), zonder de buitenlijn (binnen 9 px van wit)
def _bijwit(r=9):
    m = bg.copy(); acc = bg.copy()
    for _ in range(r):
        n = acc.copy()
        n[1:] |= acc[:-1]; n[:-1] |= acc[1:]; n[:, 1:] |= acc[:, :-1]; n[:, :-1] |= acc[:, 1:]
        acc = n
    return acc
BIJWIT = _bijwit()
LIJNPX = (KL['fur'] | KL['ver']) & (L < 100) & ~BIJWIT


def lijnfrac(x, y):
    ya, yb, xa, xb = blok(x, y)
    if yb <= ya or xb <= xa: return 0.0, 0
    sub = LIJNPX[ya:yb, xa:xb]; f = sub.mean()
    if sub.sum() < 3: return f, 0
    yy_, xx_ = np.nonzero(sub)
    cov = np.cov(np.vstack([xx_, yy_])) if len(xx_) > 2 else np.eye(2)
    w, v = np.linalg.eigh(cov); d = v[:, 1]          # lijnrichting (grootste eigenvector)
    ang = (np.degrees(np.arctan2(d[1], d[0])) + 180) % 180
    # loodrechte buurrichting: 0=horizontaal lijn -> buren boven/onder, 1=diag /, 2=verticaal, 3=diag \
    q = int(((ang + 22.5) % 180) // 45)
    return f, q
