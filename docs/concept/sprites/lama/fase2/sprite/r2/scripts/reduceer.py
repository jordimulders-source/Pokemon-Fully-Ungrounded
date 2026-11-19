# Kale reductie van het model (r4 + poten r12) en de handschoenen van r3 -> onderlaag.png
# Niets getekend: elke spritepixel komt uit zijn blok modelpixels (vlakklasse + gemiddelde toon -> dichtstbijzijnde paletkleur).
# Gebruik (vanuit lama/fase2): python3 sprite/r1/scripts/reduceer.py
import numpy as np
from PIL import Image
import os
HIER = os.path.dirname(os.path.abspath(__file__)); R1 = os.path.dirname(HIER)
FASE2 = os.path.dirname(os.path.dirname(R1))
MODEL = os.path.join(FASE2, 'gemini/poten/r4_poten_r12.png')
HANDS = os.path.join(FASE2, 'gemini/r3/r3_prompt_v3.png')

# ---- palet (index 0 transparant); tonen uit het model, Gen 3-stappen
PAL = [
 (152, 208, 160),  # 0 transparant
 (58, 30, 22),     # 1 omlijning (donkerbruin)
 (138, 82, 50),    # 2 vacht donker / binnenlijn
 (184, 120, 76),   # 3 vacht schaduw
 (218, 160, 104),  # 4 vacht basis
 (236, 192, 140),  # 5 vacht licht
 (250, 228, 196),  # 6 glans / oogwit / nageltjes
 (96, 26, 36),     # 7 rood donker
 (168, 44, 56),    # 8 rood midden
 (222, 78, 76),    # 9 rood licht
 (246, 206, 80),   # 10 geel
 (70, 146, 66),    # 11 groen
 (66, 112, 196),   # 12 blauw
 (70, 68, 76),     # 13 polsband grijs
 (34, 30, 34),     # 14 polsband zwart
]

def klassen(a):
    R, G, B = a[..., 0], a[..., 1], a[..., 2]
    lum = 0.299 * R + 0.587 * G + 0.114 * B
    bg = a.min(axis=2) >= 232
    red = (R - G > 45) & (G - B < 22) & (R > 75) & ~bg
    yel = (R > 200) & (G > 165) & (G - B > 85) & ~bg
    grn = (G > R + 15) & (G > B) & ~bg
    blu = (B > R + 40) & (B > G) & ~bg
    gry = (np.abs(R - G) < 14) & (np.abs(G - B) < 14) & (lum < 110) & ~bg
    drk = (lum < 106) & ~red & ~grn & ~blu & ~bg & ~gry
    fur = ~(bg | red | yel | grn | blu | drk | gry)
    return dict(bg=bg, red=red, yel=yel, grn=grn, blu=blu, drk=drk, gry=gry, fur=fur, lum=lum)

def furtoon(l):
    if l < 125: return 2
    if l < 156: return 3
    if l < 184: return 4
    if l < 214: return 5
    return 6

def roodtoon(l):
    if l < 70: return 7
    if l < 105: return 8
    return 9

def reduceer(a, y0, x0, s, rows, cols, dekking=0.45):
    K = klassen(a)
    out = np.zeros((rows, cols), int)
    for j in range(rows):
        for i in range(cols):
            ya, yb = int(round(y0 + j * s)), int(round(y0 + (j + 1) * s))
            xa, xb = int(round(x0 + i * s)), int(round(x0 + (i + 1) * s))
            if yb <= 0 or xb <= 0 or ya >= a.shape[0] or xa >= a.shape[1]: continue
            ya, xa = max(ya, 0), max(xa, 0)
            sl = (slice(ya, yb), slice(xa, xb)); n = (yb - ya) * (xb - xa)
            fg = (~K['bg'][sl]).sum()
            if fg < dekking * n: continue
            c = {k: K[k][sl].sum() for k in ('red', 'yel', 'grn', 'blu', 'drk', 'gry', 'fur')}
            # lijn: aandeel lijnpixels (modellijn ~5 px dik) in het blok
            if c['drk'] >= LIJNFRAC * n:
                out[j, i] = 1; continue
            acc = {k: c[k] * 1.6 for k in ('yel', 'grn', 'blu')}
            acc['red'] = c['red'] * 1.2; acc['gry'] = c['gry'] * 1.2; acc['fur'] = c['fur']
            k = max(acc, key=acc.get)
            L = K['lum'][sl]
            if k == 'fur': out[j, i] = furtoon(L[K['fur'][sl]].mean())
            elif k == 'red': out[j, i] = roodtoon(L[K['red'][sl]].mean())
            elif k == 'yel': out[j, i] = 10
            elif k == 'grn': out[j, i] = 11
            elif k == 'blu': out[j, i] = 12
            elif k == 'gry': out[j, i] = 14 if L[K['gry'][sl]].mean() < 62 else 13
            else: out[j, i] = 1
    return out

def wit_binnen(out, a, y0, x0, s):
    """gaten in het silhouet (oogwit) vullen met 6"""
    H, W = out.shape; buiten = np.zeros((H, W), bool)
    st = [(y, x) for y in range(H) for x in (0, W - 1)] + [(y, x) for x in range(W) for y in (0, H - 1)]
    while st:
        y, x = st.pop()
        if 0 <= y < H and 0 <= x < W and not buiten[y, x] and out[y, x] == 0:
            buiten[y, x] = True; st += [(y + 1, x), (y - 1, x), (y, x + 1), (y, x - 1)]
    out[(out == 0) & ~buiten] = 6
    return out

LIJNFRAC = 0.20
ROWS, S = 62, (1016 - 28) / 62.0
Y0 = 28.0
COLS = 44
X0 = (191 + 878) / 2 - COLS * S / 2

def save(arr, pad):
    im = Image.fromarray(arr.astype('uint8'), 'P')
    im.putpalette([v for c in PAL for v in c] + [0] * (768 - 3 * len(PAL)))
    im.save(pad, transparency=0)

if __name__ == '__main__':
    a = np.asarray(Image.open(MODEL).convert('RGB')).astype(int)
    body = reduceer(a, Y0, X0, S, ROWS, COLS)
    body = wit_binnen(body, a, Y0, X0, S)
    # handschoenen r3: zelfde schaal; r3-blok verschoven zodat de polsband op de nieuwe voorpoot zit
    h = np.asarray(Image.open(HANDS).convert('RGB')).astype(int)
    # (dy, dx) in modelpixels: r3-voet -> voet van de nieuwe poten (gemeten op polsbandmidden/onderkant)
    VERSCHUIF = {'nabij': (-2, -15), 'ver': (5, 0)}
    VAK = {'nabij': (845, 1005, 215, 392), 'ver': (830, 985, 380, 505)}  # r3: y0,y1,x0,x1
    hand = np.zeros_like(body)
    for naam in ('ver', 'nabij'):
        dy, dx = VERSCHUIF[naam]; ya, yb, xa, xb = VAK[naam]
        hb = np.full_like(h, 255); hb[ya:yb, xa:xb] = h[ya:yb, xa:xb]
        # alleen handschoen: polsband (grijs/zwart), rood, nageltjes onderaan; vacht van het been erboven weg
        K = klassen(hb)
        keep = K['red'] | K['gry'] | (K['drk'])
        yy = np.arange(1024)[:, None]
        keep |= K['fur'] & (yy > (975 if naam == 'nabij' else 955))  # nageltjes
        hb2 = np.full_like(h, 255); hb2[keep] = hb[keep]
        sh = np.full_like(h, 255)
        sh[max(dy, 0):1024 + min(dy, 0), max(dx, 0):1024 + min(dx, 0)] = hb2[max(-dy, 0):1024 - max(dy, 0), max(-dx, 0):1024 - max(dx, 0)]
        r = reduceer(sh, Y0, X0, S, ROWS, COLS, dekking=0.40)
        hand[r > 0] = r[r > 0]
    full = np.zeros((64, 64), int); full2 = np.zeros((64, 64), int)
    ox = (64 - COLS) // 2
    full[1:63, ox:ox + COLS] = body
    comb = body.copy(); comb[hand > 0] = hand[hand > 0]
    full2[1:63, ox:ox + COLS] = comb
    hl = np.zeros((64, 64), int); hl[1:63, ox:ox + COLS] = hand
    save(full, os.path.join(R1, 'onderlaag_zonder_handschoen.png'))
    save(hl, os.path.join(R1, 'handschoenlaag.png'))
    save(full2, os.path.join(R1, 'onderlaag.png'))
    ys, xs = np.nonzero(full2)
    print('box', xs.min(), xs.max(), ys.min(), ys.max(), 'px', (full2 > 0).sum(), 'kleuren', len(set(full2.ravel())) - 1)
