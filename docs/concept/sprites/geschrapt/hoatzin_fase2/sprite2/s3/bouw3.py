# bouw3.py: s3 = s2-silhouet en -zones, Gen 3-afwerking binnen de modelvormen. Niets getekend:
#  - silhouet = s2 (hoatzin.png van s2), zones/tinten = onderlaag (reductie, zelfde rasterfase)
#  - tinten: modus binnen de zone (geen losse pixels, harde vlakken); verre vleugel een tint donkerder
#  - penlijnen: gekozen modellijnen (skelet op 1024 px, skelet.py) geprojecteerd als doorlopende 1-px-lijn
#  - grenzen tussen onderdelen + buitenlijn (selout aan de lichtkant), kuifpunten blijven bruin
#  - oog = s2 variant B (bevroren)
import numpy as np, os, json
from PIL import Image
from scipy import ndimage as nd
from skimage.morphology import skeletonize
from klassen import ZONE
from palet import PAL, MAP, SELOUT

DX, DY = map(float, open('fase_keuze.txt').read().split())
X0, Y0, s = 97, 125, 833 / 62; OX, OY = 1, 5
CFG = json.load(open('keuze.json'))
K = np.load('onderlaag.npy')
S2 = np.array(Image.open('../s2/hoatzin.png')).astype(int)
mask = S2 > 0
if 'masker_uit' in CFG:                         # pixels die volgens het model buiten de vorm vallen
    for x, y in CFG['masker_uit']: mask[y, x] = False
Z = np.full((64, 64), '', object)
for j, i in zip(*np.where(mask)):
    Z[j, i] = ZONE[K[j, i]] if K[j, i] > 0 else 'vleugel'
# zone van s2-pixels die in de onderlaag leeg/lijn waren: neem de s2-kleur
VAN_S2 = {12: 'blauw', 13: 'blauw', 14: 'oog', 10: 'kuif', 11: 'kuif', 15: 'grijs', 5: 'creme', 6: 'creme', 7: 'krop', 8: 'krop', 9: 'krop'}
for j, i in zip(*np.where(mask)):
    if K[j, i] <= 0 and S2[j, i] in VAN_S2: Z[j, i] = VAN_S2[S2[j, i]]

# zone-correctie naar het model: rood bestaat in het model alleen in het oog, grijs alleen in snavel en poten,
# zodat mengtinten in de kuif (roodbruin met witte streep) niet als oog/grijs tellen
PUP = (9, 30)
for _ in range(2):
    for j, i in zip(*np.where(mask)):
        z = Z[j, i]
        fout = (z == 'oog' and max(abs(i - PUP[0]), abs(j - PUP[1])) > 1) or \
               (z == 'grijs' and j <= 28) or (z == 'creme' and i <= 3 and j <= 36)
        if not fout: continue
        if z == 'creme': Z[j, i] = 'grijs'; continue
        buur = [Z[y, x] for y, x in ((j-1, i), (j+1, i), (j, i-1), (j, i+1), (j-1, i-1), (j-1, i+1), (j+1, i-1), (j+1, i+1))
                if 0 <= y < 64 and 0 <= x < 64 and mask[y, x] and Z[y, x] not in ('oog', 'grijs', '')]
        if buur: Z[j, i] = max(set(buur), key=buur.count)
ZT = {'kuif': 10, 'grijs': 15, 'blauw': 12, 'creme': 5, 'vleugel': 3}

def mcel(x, y):   # modelcoordinaat -> spritepixel
    return int(np.floor((x - X0) / s + OX - DX)), int(np.floor((y - Y0) / s + OY - DY))
def cmodel(i, j):  # midden van spritepixel -> modelcoordinaat
    return X0 + (i - OX + DX + .5) * s, Y0 + (j - OY + DY + .5) * s

# --- tinten -----------------------------------------------------------------------------------
T = np.zeros((64, 64), int)
for j, i in zip(*np.where(mask)):
    T[j, i] = MAP[K[j, i]] if K[j, i] > 0 else S2[j, i]
    if ZONE.get(K[j, i]) != Z[j, i] and Z[j, i] in ZT: T[j, i] = ZT[Z[j, i]]   # gecorrigeerde zone: hoofdtint
# verre vleugel: vleugelzone met modelmidden links van de voorrand van de nabije vleugel en boven het lijf
ver = np.zeros((64, 64), bool)
for j, i in zip(*np.where(mask)):
    x, y = cmodel(i, j)
    if Z[j, i] == 'vleugel' and x < CFG['ver_x'] and y < CFG['ver_y']: ver[j, i] = True
STAP = {2: 3, 3: 4, 4: 4}
for j, i in zip(*np.where(ver)):
    if T[j, i] in STAP: T[j, i] = STAP[T[j, i]]
# modus binnen de zone (3x3, alleen dezelfde zone en zelfde deel), twee keer
deel = np.where(ver, 1, 0) + np.where(Z == 'vleugel', 2, 0)
for _ in range(CFG.get('modus', 2)):
    T2 = T.copy()
    for j, i in zip(*np.where(mask)):
        if Z[j, i] == 'oog': continue
        v = []
        for dj in (-1, 0, 1):
            for di in (-1, 0, 1):
                y, x = j + dj, i + di
                if 0 <= y < 64 and 0 <= x < 64 and mask[y, x] and Z[y, x] == Z[j, i] and deel[y, x] == deel[j, i] and T[y, x] > 1:
                    v.append(T[y, x])
        if v:
            b = np.bincount(v)
            if b[T[j, i]] if T[j, i] < len(b) else 0:
                if b.max() >= 5 and b[T[j, i]] <= 2: T2[j, i] = b.argmax()
            else: T2[j, i] = b.argmax()
    T = T2
# tinteilandjes < 4 px opvullen
for _ in range(2):
    for v in np.unique(T[mask]):
        if v in (1, 14): continue
        lab, n = nd.label(T == v)
        for c in range(1, n + 1):
            m = lab == c
            if m.sum() >= 4: continue
            ring = nd.binary_dilation(m) & ~m & mask
            zz = Z[m][0]
            kand = [T[p] for p in zip(*np.where(ring)) if Z[p] == zz and T[p] > 1 and T[p] != v]
            if kand: T[m] = np.bincount(kand).argmax()

# --- lijnen -----------------------------------------------------------------------------------
lijn = np.zeros((64, 64), bool)
PRI = {'oog': 7, 'blauw': 6, 'grijs': 5, 'kuif': 4, 'creme': 3, 'krop': 2, 'vleugel': 1}
for j, i in zip(*np.where(mask)):
    for dj, di in ((0, 1), (1, 0), (0, -1), (-1, 0)):
        y, x = j + dj, i + di
        if 0 <= y < 64 and 0 <= x < 64 and mask[y, x]:
            a, b = Z[j, i], Z[y, x]
            if a != b and PRI[a] < PRI[b] and not {a, b} <= {'oog', 'blauw'}:
                if {a, b} == {'kuif', 'vleugel'} and CFG.get('kuif_vleugel_lijn_in_kuif'):
                    continue
                lijn[j, i] = True
# geprojecteerde modellijnen
sk = np.load('skelet.npz'); lab = sk['lab']
pad = np.zeros((64, 64), bool)
for p in CFG['paden']:
    ys, xs = np.where(lab == p)
    for x, y in zip(xs, ys):
        i, j = mcel(x, y)
        if 0 <= i < 64 and 0 <= j < 64 and mask[j, i]: pad[j, i] = True
pad = skeletonize(pad)
lijn |= pad
S = T.copy(); S[lijn & mask] = 1
# penranden: de pixel boven elke penlijn krijgt de lichte tint (nabij 2, ver 3), zoals de lichte penrand in het model
for j, i in zip(*np.where(pad)):
    for dj in range(1, CFG.get('pen_rand', 1) + 1):
        y = j - dj
        if y >= 0 and mask[y, i] and Z[y, i] == 'vleugel' and not lijn[y, i]:
            S[y, i] = 3 if ver[y, i] else 2
# kuif: KUIF = 'regel' (hoofdtint, schaduw onder/rechts), 'model' (modeltinten licht/donker), 'as' (skelet = licht)
KM = CFG.get('kuif', 'regel')
AS = np.load('kuifas.npy') > 0
for j, i in zip(*np.where(mask & (Z == 'kuif'))):
    if S[j, i] == 1: continue
    onder = j + 1 > 63 or not mask[j + 1, i] or Z[j + 1, i] != 'kuif' or lijn[j + 1, i]
    rechts = i + 1 > 63 or not mask[j, i + 1] or Z[j, i + 1] != 'kuif' or lijn[j, i + 1]
    if KM == 'regel': S[j, i] = 11 if (onder or rechts) else 10
    elif KM == 'model': S[j, i] = 10 if K[j, i] == 9 else 11
    else: S[j, i] = 10 if AS[j, i] else 11
T = np.where(S > 1, S, T)

# --- buitenlijn -------------------------------------------------------------------------------
tr = ~mask
def tp(y, x): return y < 0 or x < 0 or y > 63 or x > 63 or tr[y, x]
pd = np.pad(tr, 1, constant_values=True)
rand = mask & (pd[:-2, 1:-1] | pd[2:, 1:-1] | pd[1:-1, :-2] | pd[1:-1, 2:])
g = nd.gaussian_filter(mask.astype(float), 1.2)
gy, gx = np.gradient(g)
licht = (gy + gx) / (np.hypot(gx, gy) + 1e-6)
for j, i in zip(*np.where(rand)):
    zz = Z[j, i]
    if zz == 'oog': continue
    buren = sum(not tp(j + a, i + b) for a, b in ((0, 1), (1, 0), (0, -1), (-1, 0)))
    dunH = tp(j, i - 1) and tp(j, i + 1); dunV = tp(j - 1, i) and tp(j + 1, i)
    smal = (tp(j, i - 1) and tp(j, i + 2)) or (tp(j, i + 1) and tp(j, i - 2)) or \
           (tp(j - 1, i) and tp(j + 2, i)) or (tp(j + 1, i) and tp(j - 2, i))
    if zz == 'kuif' and buren <= 1:          # punt van een pluk: bruin houden (donker)
        S[j, i] = 11; continue
    if zz in SELOUT and (dunH or dunV):
        S[j, i] = SELOUT[zz] if zz != 'creme' else T[j, i]; continue
    if zz in SELOUT and smal and licht[j, i] > 0:
        S[j, i] = T[j, i] if T[j, i] > 1 else S[j, i]; continue
    S[j, i] = SELOUT[zz] if (zz in SELOUT and licht[j, i] > 0.35) else 1

# kuifplukken eindigen in bruin: waar de middellijn van een pluk (model) op een zwarte rand valt, wordt die rand
# kuifschaduw (11) in plaats van zwart
for j, i in zip(*np.where(AS & (S == 1))):
    if Z[j, i] in ('kuif', '') or any(Z[y, x] == 'kuif' for y, x in ((j-1, i), (j+1, i), (j, i-1), (j, i+1)) if 0 <= y < 64 and 0 <= x < 64):
        if not any(mask[y, x] and Z[y, x] == 'vleugel' for y, x in ((j-1, i), (j+1, i), (j, i-1), (j, i+1)) if 0 <= y < 64 and 0 <= x < 64):
            S[j, i] = 11

# --- oog B uit s2 (bevroren) --------------------------------------------------------------------
for y in range(28, 33):
    for x in range(7, 12):
        if S2[y, x] in (12, 14) or (x, y) == (9, 30): S[y, x] = S2[y, x]

# --- techniek: dambord / klont / barcode -------------------------------------------------------
def techniek(S):
    for _ in range(3):
        for y in range(63):
            for x in range(63):
                p, q, r, t = S[y, x], S[y, x + 1], S[y + 1, x], S[y + 1, x + 1]
                if p and q and p == t and q == r and p != q:
                    if p == 1: S[y + 1, x] = 1
                    elif q == 1: S[y + 1, x + 1] = 1
                    else: S[y + 1, x] = p
        for y in range(63):
            for x in range(63):
                b = S[y:y + 2, x:x + 2]
                if (b == 1).all() and not rand[y:y + 2, x:x + 2].any():
                    S[y + 1, x + 1] = T[y + 1, x + 1] if T[y + 1, x + 1] > 1 else S[y + 1, x + 1]
        for t in range(2):
            V = S if t == 0 else S.T; V0 = T if t == 0 else T.T
            for i in range(64):
                for j in range(60):
                    v = V[i, j:j + 5]
                    if (v > 0).all() and v[0] == v[2] == v[4] and v[1] == v[3] and v[0] != v[1]:
                        k = j + 1 if v[1] == 1 else j + 2
                        if V[i, k] == 1 and V0[i, k] > 1: V[i, k] = V0[i, k]
    return S
S = techniek(S)
def los_weg(S):
    # losse tintpixels (geen 8-buur met dezelfde tint): meest voorkomende tint van dezelfde zone eromheen
    for _ in range(2):
        for y in range(64):
            for x in range(64):
                v = S[y, x]
                if v < 2 or v == 14 or (Z[y, x] == 'grijs' and v in (5, 6)): continue
                nb8 = [(y + a, x + b) for a in (-1, 0, 1) for b in (-1, 0, 1) if (a or b) and 0 <= y + a < 64 and 0 <= x + b < 64]
                if any(S[p] == v for p in nb8): continue
                kand = [S[p] for p in nb8 if S[p] > 1 and Z[p] == Z[y, x] and S[p] != 14]
                if kand: S[y, x] = np.bincount(kand).argmax()
                elif Z[y, x] != 'grijs':
                    ander = [S[p] for p in nb8 if S[p] > 1 and S[p] != 14]
                    if len(ander) >= 3: S[y, x] = np.bincount(ander).argmax()

    return S
S = los_weg(S)
S = techniek(S)
S = los_weg(S)
S = techniek(S)
np.save('hoatzin.npy', S)
im = Image.fromarray(S.astype(np.uint8), 'P'); pal = []
for c in PAL: pal += list(c)
im.putpalette(pal + [0] * (768 - len(pal))); im.save('hoatzin.png', transparency=0)
im.resize((512, 512), Image.NEAREST).save('hoatzin_8x.png', transparency=0)
with open('normal.pal', 'w') as f:
    f.write('JASC-PAL\r\n0100\r\n16\r\n' + ''.join('%d %d %d\r\n' % tuple(c) for c in PAL))
print('kleuren', len(np.unique(S)), 'pixels', int((S > 0).sum()))
