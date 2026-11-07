"""Sprite r2: reparaties op v1 (../raster.txt), alleen de benoemde punten 1-6 van de coördinator.
Massa/omtrek van v1 bevroren behalve zone KOP (punt 1: kop, oren, snavel) en zone STROOK (punt 4); bij punt 6
(bliksem- en pootranden) verandert de omtrek ook een paar px, gemeld door diff.py.
Gebruik: python3.11 teken_r2.py  -> raster.txt"""
import math
V1 = [list(l.rstrip('\n')) for l in open('raster_v1.txt')][:64]
P1 = [l.rstrip('\n') for l in open('../onderdelen.txt')][:64]
R = [r[:] for r in V1]
IN = lambda x, y: 0 <= x < 64 and 0 <= y < 64
def nb4(x, y): return [(x+dx, y+dy) for dx, dy in ((1,0),(-1,0),(0,1),(0,-1)) if IN(x+dx, y+dy)]

# ---------- onderdelenkaart van v1 (na het handwerk) ----------
DEEL = [['.'] * 64 for _ in range(64)]
for y in range(64):
    for x in range(64):
        if V1[y][x] == '.': continue
        p = P1[y][x]
        if y <= 18 and x <= 32 and p in 'UIFSK.': p = 'U'
        elif p == '.': p = 'L'
        if p in 'ZT' and x < 24 and y < 59: p = 'Z'
        DEEL[y][x] = p
for y in range(51, 57):
    for x in range(19, 34):
        if V1[y][x] in 'gG' or (V1[y][x] == 'k' and P1[y][x] == 'P'): DEEL[y][x] = 'P'

# ---------- punt 1: kop als eigen ronde vorm (ellips), ook ronder aan de achterkant ----------
KX, KY, KRX, KRY = 19.5, 26.2, 9.2, 8.4
def in_kop(x, y): return ((x - KX) / KRX) ** 2 + ((y - KY) / KRY) ** 2 <= 1.0
ZONE_KOP = {(x, y) for y in range(6, 36) for x in range(2, 32)}
ZONE_STROOK = {(x, y) for y in range(17, 36) for x in range(26, 38)}
KOP = {(x, y) for (x, y) in ZONE_KOP if in_kop(x, y)}
# alles in de kopzone dat kop/oor/snavel was, eerst weg (wordt opnieuw getekend)
for (x, y) in ZONE_KOP:
    if DEEL[y][x] in 'KUNWOI': R[y][x] = '.'; DEEL[y][x] = '.'
for (x, y) in KOP: DEEL[y][x] = 'K'
# wat in v1 kop/hals was en nu buiten de ronde kop valt (onder de kop, rij 27+): borst/hals = lijf
for (x, y) in ZONE_KOP:
    if y >= 27 and DEEL[y][x] == '.' and V1[y][x] != '.' and P1[y][x] in 'KWO': DEEL[y][x] = 'L'

# ---------- punt 4: de strook achter de kop (verre vleugel) lichter ----------
for (x, y) in ZONE_STROOK:
    if DEEL[y][x] == 'F': DEEL[y][x] = 'F'   # blijft verre vleugel, maar met lichte tinten (zie kleuring)

# ---------- kleuring met volume: lichtpunt linksboven, tint naar afstand (cirkels = vloeiende sikkels) ----------
def tint(d, drie, s=0.86): return drie[0] if d < 0.45 else (drie[1] if d < s else drie[2])
# kop
for (x, y) in KOP:
    d = math.hypot((x - (KX - 3.6)) / (KRX * 1.15), (y - (KY - 3.6)) / (KRY * 1.15))
    R[y][x] = tint(d, '123')
# lijf + buik: één bol lijf; de buik is een ellips (vloeiende grens), zelfde lichtpunt
LIJF = [(x, y) for y in range(64) for x in range(64) if DEEL[y][x] in 'LB' and not in_kop(x, y)]
bx = [x for x, y in LIJF if DEEL[y][x] == 'B']; by = [y for x, y in LIJF if DEEL[y][x] == 'B']
BCX, BCY = sum(bx) / len(bx), sum(by) / len(by)
LCX, LCY = 24.5, 41.5     # middelpunt lijf (uit de massa)
for (x, y) in LIJF:
    buik = ((x - (BCX - 0.5)) / 6.6) ** 2 + ((y - (BCY - 0.5)) / 9.6) ** 2 <= 1.0
    DEEL[y][x] = 'B' if buik else 'L'
    d = math.hypot((x - (LCX - 6)) / 17.0, (y - (LCY - 7)) / 17.0)
    R[y][x] = tint(d, 'abe' if buik else '123', 1.0)   # sikkel smaller: alleen de rand rechtsonder in schaduw
# nabije vleugel: voorrand licht (3), basis v, schaduw (4) alleen onder en rechts
VL = [(x, y) for y in range(64) for x in range(64) if DEEL[y][x] in 'VS' and x >= 29]
for (x, y) in VL:
    d = math.hypot((x - 38) / 22.0, (y - 9) / 26.0)
    R[y][x] = '3' if d < 0.42 else ('v' if d < 1.05 else '4')
    DEEL[y][x] = 'V'
# verre vleugel: v, voorrand 3, geen zwarte vlek (punt 4)
for y in range(64):
    for x in range(64):
        if DEEL[y][x] == 'F':
            R[y][x] = '3' if (x + y) < 50 else 'v'

# ---------- punt 3: veerranden (3 ronde veren) en ronde, onregelmatige stippen ----------
for a, b in [((50, 10), (47, 13)), ((51, 25), (47, 27)), ((49, 33), (46, 31))]:
    n = max(abs(b[0] - a[0]), abs(b[1] - a[1]))
    for i in range(n + 1):
        x = round(a[0] + (b[0] - a[0]) * i / n); y = round(a[1] + (b[1] - a[1]) * i / n)
        if DEEL[y][x] == 'V' and i < n: R[y][x] = '4'
S2 = ['aa', 'aa']; S3 = ['aa.', 'aaa', '.aa']; S3b = ['.aa', 'aaa', 'aa.']   # één tint, zoals Picapau
STIPPEN = [((40, 11), S3), ((46, 9), S2), ((44, 16), S3b), ((51, 12), S3), ((39, 21), S3), ((47, 21), S3),
           ((53, 18), S2), ((41, 28), S3b), ((49, 28), S3), ((35, 26), S2)]
for (sx, sy), sj in STIPPEN:
    for j, r in enumerate(sj):
        for i, c in enumerate(r):
            if c != '.' and DEEL[sy + j][sx + i] == 'V': R[sy + j][sx + i] = c
for (sx, sy) in [(31, 17)]:   # één stip op de verre vleugel, in de basis-tint (verder weg)
    for j, r in enumerate(S2):
        for i, c in enumerate(r):
            if DEEL[sy + j][sx + i] == 'F': R[sy + j][sx + i] = 'b'

# ---------- punt 1: oren als veerkuif, smal aan de voet, krul aan de punt ----------
OOR = ['..kkk',          # rij 9, x vanaf 9
       '.k122k',
       'k1kk12k',
       'k2k.k12k',
       '.kk.k412k',
       '....41b2k',
       '....41bb2k',
       '....41bb2k',
       '.....41b2k',
       '.....412k']
KL = {(9 + x, 9 + y): c for y, r in enumerate(OOR) for x, c in enumerate(r) if c != '.'}
# voet doortrekken tot op de ronde kop
SP = {(41 - x, y): {'1': '2', '2': '1'}.get(c, c) for (x, y), c in KL.items()}
for kl in (KL, SP):           # elke kolom van de onderste rij doortrekken tot hij op de ronde kop staat
    for (x, y), c in [(p, c) for p, c in kl.items() if p[1] == 18]:
        yy = 19
        while not in_kop(x, yy) and yy < 24: kl[(x, yy)] = c; yy += 1
def omlijn(kl):
    m = set(kl); out = {}
    for (x, y) in m:
        leeg = [(a, b) for a, b in nb4(x, y) if (a, b) not in m and not in_kop(a, b)]
        if leeg: out[(x, y)] = '4' if all(a < x or b < y for a, b in leeg) else 'k'
        else: out[(x, y)] = kl[(x, y)]
    return out
for kl in (KL, SP):
    for (x, y), c in omlijn(kl).items():
        if (x, y) not in KOP: R[y][x] = c; DEEL[y][x] = 'U'
# krul in één tint (dunne lijn)
for (x, y) in list(KL) + list(SP):
    if y <= 13 and R[y][x] in '12': R[y][x] = '2'

# ---------- punt 1: snavel zoals Picapau (g/a/G, donkere punt, schaduw onder), punt naar links ----------
SNAVEL = {28: (9, 'gggk'), 29: (7, 'ggaaag'), 30: (5, 'Gggaaaag'), 31: (4, 'GGgggggGG'), 32: (5, 'kGGGGGGk'), 33: (7, 'kkkkk')}
for y, (x0, s) in SNAVEL.items():
    for i, c in enumerate(s):
        x = x0 + i
        if not in_kop(x, y): R[y][x] = c; DEEL[y][x] = 'N'
# ---------- punt 5: wang met twee tinten ----------
for y, (x0, s) in {30: (22, 'ccc'), 31: (21, 'ccccC'), 32: (21, 'cccCC'), 33: (22, 'CCC')}.items():
    for i, c in enumerate(s): R[y][x0 + i] = c
# oog (pixel voor pixel Picapau, ongewijzigd t.o.v. v1)
for y, r in {23: '.kk.', 24: 'Gwkk', 25: 'kkGk', 26: '.kk.'}.items():
    for i, c in enumerate(r):
        if c != '.': R[y][24 + i] = c

# ---------- omlijning van kop en lijf: zelfde helft = zelfde soort lijn (geen om-en-om) ----------
def rand(cel, cx, cy, selout):
    x, y = cel
    leeg = [(a, b) for a, b in nb4(x, y) if R[b][a] == '.']
    if not leeg: return None
    return selout if (x - cx) + (y - cy) * 1.1 < 0 else 'k'
for (x, y) in KOP:
    if R[y][x] in 'kGw' and 23 <= y <= 26: continue
    r = rand((x, y), KX, KY, '4')
    if r: R[y][x] = r
    elif any(DEEL[b][a] in 'VFLB' for a, b in nb4(x, y)) and not (21 <= x <= 25 and 30 <= y <= 33):
        R[y][x] = '4'                                   # binnenlijn: de kop valt over lijf en vleugel
for (x, y) in LIJF:
    r = rand((x, y), LCX, LCY, 'e' if DEEL[y][x] == 'B' else '4')
    if r: R[y][x] = r
for (x, y) in VL:
    r = rand((x, y), 44, 20, '4')
    if r: R[y][x] = r

# ---------- punt 6: bliksem met regelmatige randen, pootjes met 2+2 tenen ----------
# bliksem: het masker van v1 blijft (omtrek bevroren; de linkerrand is al precies 1:1, rechts 1-2-1-2 regelmatig);
# opnieuw gekleurd: y licht + 1 schaduw (Y is vervallen voor de wangschaduw), zwarte rand rechts/onder, oranje links
BL = {(x, y) for y in range(36, 60) for x in range(0, 24) if V1[y][x] in 'y1Yk' and (P1[y][x] in 'ZT' or V1[y][x] in 'yY')}
for (x, y) in BL:
    rij = [a for a, b in BL if b == y]
    leeg = [(a, b) for a, b in nb4(x, y) if (a, b) not in BL and R[b][a] == '.']
    if len(rij) == 1 or x == max(rij): R[y][x] = 'k'
    elif x == min(rij): R[y][x] = '1'
    elif any(b > y for a, b in leeg): R[y][x] = 'k'
    elif leeg: R[y][x] = '1' if x <= (min(rij) + max(rij)) / 2 else 'k'
    else: R[y][x] = 'y' if (x - min(rij)) < 0.55 * (max(rij) - min(rij)) or y < 47 else '1'
    DEEL[y][x] = 'Z'
for y in range(51, 57):
    for x in range(19, 34):
        if DEEL[y][x] == 'P': R[y][x] = '.'
POOT = {52: [(23, 'gGk'), (29, 'GGk')],          # nabij: g/G, ver: alleen G (schaduwtint), hoger
        53: [(23, 'gGk'), (29, 'GGk')],
        54: [(20, 'kggGGgk'), (27, 'kGGGGk')],    # tenen: 2 naar voren (links), 2 naar achteren (rechts)
        55: [(20, 'gk'), (22, 'gk'), (25, 'Gk'), (27, 'Gk'), (31, 'Gk')]}
for y, delen in POOT.items():
    for x0, s in delen:
        for i, c in enumerate(s):
            if R[y][x0 + i] == '.' or c != '.': R[y][x0 + i] = c

# ---------- afwerking ----------
# restjes v1 boven de kop (geen oor, kop of verre vleugel meer) weg
for (x, y) in ZONE_KOP:
    if y <= 21 and DEEL[y][x] in 'L.' and not in_kop(x, y) and R[y][x] != '.': R[y][x] = '.'
# gaatjes van 1 px tussen ronde kop en verre vleugel dicht (verre vleugel v)
for (x, y) in ZONE_STROOK:
    if R[y][x] == '.' and V1[y][x] != '.' and sum(R[b][a] != '.' for a, b in nb4(x, y)) >= 3: R[y][x] = 'v'
# snavelvoet: de pixel naast de kop donker (G), zoals Picapau
for y in range(28, 33):
    xs = [x for x in range(2, 16) if DEEL[y][x] == 'N' and R[y][x] in 'ga']
    if xs: R[y][max(xs)] = 'G' if y >= 30 else 'g'
# alpha bevroren buiten de zones: wat in v1 dicht was en nu leeg is, vullen met de tint van de buren
ZONE6 = {(x, y) for y in range(51, 57) for x in range(18, 34)}
for y in range(64):
    for x in range(64):
        if V1[y][x] != '.' and R[y][x] == '.' and (x, y) not in ZONE_KOP | ZONE_STROOK | ZONE6:
            bur = [R[b][a] for a, b in nb4(x, y) if R[b][a] not in '.k']
            R[y][x] = max(set(bur), key=bur.count) if bur else 'k'
# verre vleugel: blootgekomen bovenrand (door de verlaagde top) selout 4; losse restpixels
for y in range(14, 21):
    for x in range(27, 34):
        if R[y][x] in 'v3' and any(R[b][a] == '.' for a, b in nb4(x, y)): R[y][x] = '4'
for (x, y), c in {(15, 34): 'a', (25, 54): 'G', (18, 58): 'k'}.items(): R[y][x] = c
open('raster.txt', 'w').write('\n'.join(''.join(r) for r in R) + '\n')
print('ok')
