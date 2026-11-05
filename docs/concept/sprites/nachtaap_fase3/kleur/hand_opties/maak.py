"""Healerhand-opties A-D (5 nov). Basis ronde3. Per optie een handraster (x5..22); de gloed wordt eromheen
gelegd (band 10 linksboven / 11 rechtsonder, rand 12), alleen binnen het oude hand+gloedvak (+-2 px).
Kin, lijf en polsbont blijven 0 px diff (zie bewerkbaar masker E)."""
import os, sys
import numpy as np
from PIL import Image
H = os.path.dirname(os.path.abspath(__file__))
src = Image.open(os.path.join(H, '../ronde3/nachtaap_fase3.png')); A0 = np.array(src); PAL = src.getpalette()
C = {'3': 3, '4': 4, 'k': 1, 'o': 2, 'W': 15, 'l': 13, 'm': 14, 'a': 10, 'b': 11, 'c': 12, '_': 0}
X0 = 1
# bewerkbaar masker: oude hand + gloed, kin/lijf/polsbont uitgesloten
E = np.zeros_like(A0, bool)
for y in range(46, 63):
    for x in range(4, 24):
        v = A0[y, x]
        if v in (0, 10, 11, 12, 13, 14, 15): E[y, x] = True
        elif v in (1, 2) and 47 <= y <= 60 and 6 <= x <= 21: E[y, x] = True
E[44:48, 4:13] = False                     # kin
E[59:62, 18:22] &= ~np.isin(A0[59:62, 18:22], (1, 3, 4))   # polsbont
E[46:48, 20:24] = False                    # lijf rechtsboven

# groter vak (Jordi: "suggesties uitwerken hoe dat te fixen"): hand mag naar links/onder groeien, polsbont schuift mee
EG = E.copy()
for y in range(46, 64):
    for x in range(1, 24):
        v = A0[y, x]
        if v in (0, 10, 11, 12, 13, 14, 15): EG[y, x] = True
EG[59:62, 18:22] = True                    # oud polsbont mag verschuiven
EG[44:48, 1:13] = False; EG[46:48, 20:24] = False

def bouw(raster, extra=None, groot=False):
    global E
    E0 = E
    if groot: E = EG
    try: return _bouw(raster, extra, groot)
    finally: E = E0

def _bouw(raster, extra, groot):
    a = A0.copy()
    hand = np.zeros_like(E)
    vast = {}
    for y, rij in raster.items():
        for i, ch in enumerate(rij):
            x = X0 + i
            if ch in 'koWlmabc_34':
                if not E[y, x]: raise SystemExit(f'pixel buiten E: {x},{y} {ch}')
                vast[(y, x)] = C[ch]
                if ch in 'koWlm34': hand[y, x] = True
    # gloed: gaten tussen de toppen dicht (band 10), band 1 px, rand 1 px (rond)
    def dil(m, r):
        o = m.copy()
        for dy in range(-r, r + 1):
            for dx in range(-r, r + 1):
                if dx * dx + dy * dy > r * r + (1 if r > 1 else 1): continue
                o |= np.roll(np.roll(m, dy, 0), dx, 1)
        return o
    pols = np.zeros_like(E)
    if not groot: pols[59:62, 18:22] = np.isin(A0[59:62, 18:22], (1, 3, 4))
    basis = hand | pols
    b1 = dil(basis, 1); b2 = dil(basis, 2)
    for y in range(44, 64):
        for x in range(1, 26):
            if not E[y, x]: continue
            if (y, x) in vast: a[y, x] = vast[(y, x)]; continue
            if b1[y, x]:
                rb = hand[y, x - 1] or hand[y - 1, x] or hand[y - 1, x - 1] or pols[y - 1, x] or pols[y, x - 1]
                lt = hand[y, x + 1] or hand[y, x + 2] or (y < 63 and (hand[y + 1, x] or hand[y + 1, x + 1])) or (y < 62 and hand[y + 2, x])
                a[y, x] = 11 if (rb and not lt) or y >= 59 else 10
            elif b2[y, x]: a[y, x] = 12
            else: a[y, x] = 0
    # gaten tussen gloed en lijf/kop dicht, open banden krijgen de rand
    for _ in range(3):
        for y in range(44, 64):
            for x in range(1, 26):
                if E[y, x] and a[y, x] == 0 and 0 < x < 63 and y < 63 and (y, x) not in vast:
                    if (a[y, x - 1] and a[y, x + 1]) or (a[y - 1, x] and (y == 63 or a[y + 1, x])):
                        a[y, x] = 12
    for y in range(44, 64):
        for x in range(1, 26):
            if E[y, x] and a[y, x] in (10, 11) and (y, x) not in vast:
                if y == 63 or 0 in (a[y, x - 1], a[y, x + 1], a[y - 1, x], a[y + 1, x]): a[y, x] = 12
    for y in range(48, 64):                # rand ook waar de gloed tegen het lijf ligt (zoals ronde 3)
        for x in range(20, 24):
            if E[y, x] and (y, x) not in vast and a[y, x] in (10, 11) and not E[y, x + 1] and A0[y, x + 1] not in (0,):
                a[y, x] = 12
    if extra: extra(a)
    return a

def controle(a, naam, groot=False):
    d = (a != A0)
    buiten = d & ~(EG if groot else E)
    ys, xs = np.nonzero(d)
    print(naam, 'diff', int(d.sum()), 'buiten E', int(buiten.sum()), 'vak x%d-%d y%d-%d' % (xs.min(), xs.max(), ys.min(), ys.max()))
    # open randen: hand/gloedkleur naast transparant moet rand (1,2,12) zijn
    fout = []
    for y in range(64):
        for x in range(64):
            if a[y, x] in (10, 11, 13, 14, 15):
                for dy, dx in ((0, 1), (0, -1), (1, 0), (-1, 0)):
                    yy, xx = y + dy, x + dx
                    if not (0 <= yy < 64 and 0 <= xx < 64) or a[yy, xx] == 0: fout.append((x, y))
    print('  open randen:', fout)

def save(a, naam):
    im = Image.fromarray(a, 'P'); im.putpalette(PAL); im.save(os.path.join(H, naam), transparency=0)

OPTIES = {}

def ras(segs):
    """segs: {y: [(x, 'tekens'), ...]} -> raster vanaf X0"""
    R = {}
    for y, lst in segs.items():
        r = ['.'] * 24
        for x, s in lst:
            for i, ch in enumerate(s): r[x - X0 + i] = ch
        R[y] = ''.join(r)
    return R
