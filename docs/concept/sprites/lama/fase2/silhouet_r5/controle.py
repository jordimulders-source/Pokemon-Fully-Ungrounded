"""Controles silhouet ronde 5 t.o.v. direct.txt (bron). Draaien: python3 controle.py [ronde3.txt]"""
import os, sys
import numpy as np

def edt(mask):  # afstand van elke pixel tot de dichtstbijzijnde False-pixel (brute force, 64x64)
    zy, zx = np.nonzero(~mask); out = np.zeros(mask.shape)
    for y, x in zip(*np.nonzero(mask)): out[y, x] = np.sqrt(((zy - y) ** 2 + (zx - x) ** 2).min())
    return out
def label(mask):
    lab = np.zeros(mask.shape, int); n = 0
    for y, x in zip(*np.nonzero(mask)):
        if lab[y, x]: continue
        n += 1; st = [(y, x)]; lab[y, x] = n
        while st:
            a, b = st.pop()
            for da in (-1, 0, 1):
                for db in (-1, 0, 1):
                    c, d = a + da, b + db
                    if 0 <= c < mask.shape[0] and 0 <= d < mask.shape[1] and mask[c, d] and not lab[c, d]: lab[c, d] = n; st.append((c, d))
    return lab, n
HERE = os.path.dirname(os.path.abspath(__file__))
def load(p): return np.array([[c == '#' for c in l.rstrip('\n')] for l in open(os.path.join(HERE, p)) if l.strip()])
S = load(sys.argv[1] if len(sys.argv) > 1 else 'ronde5.txt'); D = load('direct.txt')
ZONES = {  # (y0, y1, x0, x1) inclusief; volgorde = voorrang
 '1 kop': (0, 20, 0, 63), '2 hals': (21, 27, 0, 28), '5 halsband': (28, 31, 0, 24),
 '3 lijf+staart+aguayo': (21, 43, 0, 63), '4 poten (+buikboog y44)': (44, 63, 0, 63)}
zid = np.full(S.shape, '', object)
for n, (y0, y1, x0, x1) in reversed(list(ZONES.items())): zid[y0:y1+1, x0:x1+1] = n
ys, xs = np.nonzero(S); h = ys.max() - ys.min() + 1
print(f'px {S.sum()} (bron {D.sum()}, fase 1 = 1019), box {xs.max()-xs.min()+1}x{h}, y{ys.min()}-{ys.max()}')
dD = edt(~D); dDin = edt(D)
print('zone            +px  -px  max afstand nieuw px tot bron / weg px tot rand')
for n in ZONES:
    m = zid == n; add = S & ~D & m; rem = D & ~S & m
    print(f'{n:26s} {add.sum():4d} {rem.sum():4d}   {dD[add].max() if add.any() else 0:.1f} / {dDin[rem].max() if rem.any() else 0:.1f}')
print('buiten zones:', int(((S ^ D) & (zid == '')).sum()))
lab, n = label(S); print('componenten', n)
Pp = np.pad(S, 1).astype(int); nb = sum(Pp[1+a:65+a, 1+b:65+b] for a in (-1,0,1) for b in (-1,0,1)) - S
print('losse px (<=1 buur)', int((S & (nb <= 1)).sum()))
bl, _ = label(~np.pad(S, 1)); holes = (bl[1:-1, 1:-1] != bl[0, 0]) & ~S; print('gaten', int(holes.sum()))
# rechte randen: verticale (links/rechts) en horizontale runs van rand-pixels >= 4
def runs(edge, axis):
    out = []
    E = edge if axis == 0 else edge.T
    for i in range(E.shape[1]):
        col = E[:, i]; j = 0
        while j < len(col):
            if col[j]:
                k = j
                while k < len(col) and col[k]: k += 1
                if k - j >= 4: out.append((i, j, k - 1))
                j = k
            else: j += 1
    return out
P = np.pad(S, 1)
L = S & ~P[1:-1, :-2]; R = S & ~P[1:-1, 2:]; T = S & ~P[:-2, 1:-1]; B = S & ~P[2:, 1:-1]
print('rechte verticale randen >=4 (x, y0-y1):')
for nm, E in (('links', L), ('rechts', R)):
    for x, a, b in runs(E, 0): print(f'  {nm} x{x} y{a}-{b} ({b-a+1}) zone {zid[a, x]}')
print('rechte horizontale randen >=4 (y, x0-x1):')
for nm, E in (('boven', T), ('onder', B)):
    for y, a, b in runs(E, 1): print(f'  {nm} y{y} x{a}-{b} ({b-a+1}) zone {zid[y, a]}')
# poten: segmenten per rij y45+
print('poten (rij: segmenten breedte / lucht):')
for y in range(44, 63):
    row = S[y]; seg = []; x = 0
    while x < 64:
        if row[x]:
            k = x
            while k < 64 and row[k]: k += 1
            seg.append((x, k - 1)); x = k
        else: x += 1
    print(f'  y{y}: ' + '  '.join(f'{a}-{b}({b-a+1})' for a, b in seg) + '   lucht ' + ','.join(str(seg[i+1][0]-seg[i][1]-1) for i in range(len(seg)-1)))
kop = S[:21]; print(f'kop incl. oren y{ys.min()}-20: {21-ys.min()}/{h} = {(21-ys.min())/h:.0%} van de hoogte, {kop.sum()} px = {kop.sum()/S.sum():.0%} van het oppervlak')
