# bouw6.py: s6 = s5 + afwerking. NIETS GETEKEND: silhouet = s5 (alleen losse ruispixels eruit), oog bevroren.
#  1. palet: elke kleurgroep 3 tinten (kleurtoon model, alleen helderheid); vleugelpalet lichter/gespreid (R2)
#  2. kuif, snavel/poten, creme, krop: omlijning (zwart aan schaduwkant, eigen donkerste tint aan lichtkant)
#     + licht linksboven / sikkel rechtsonder per onderdeel
#  3. handreparaties (R3-R6) uit hand.json
import numpy as np, json
from PIL import Image
PAL = [(255, 255, 255), (16, 14, 24),
       (112, 114, 166), (70, 72, 118), (48, 46, 80),        # 2-4 blauwzwart licht/midden/schaduw (R2)
       (244, 236, 212), (198, 194, 176), (144, 142, 134),   # 5-7 creme licht/midden/schaduw; 6/7 ook grijs licht/midden
       (196, 60, 52),                                       # 8 oog rood (bevroren)
       (184, 136, 188), (146, 96, 148), (98, 58, 104),      # 9-11 krop
       (178, 108, 70), (146, 80, 54), (106, 48, 34),        # 12-14 kuif licht / midden / schaduw
       (110, 150, 194)]                                     # 15 gezicht blauw
S5 = np.array(Image.open('../s5/hoatzin.png')).astype(int)
OUD = {0: 0, 1: 1, 2: 2, 3: 3, 4: 4, 5: 5, 6: 6, 7: 9, 8: 10, 9: 11, 10: 13, 11: 14, 12: 15, 13: 7, 14: 8, 15: 6}
A = np.vectorize(OUD.get)(S5)
H = json.load(open('hand.json'))
for x, y in H['weg']: A[y, x] = 0
OOG = {(x, y) for y in range(27, 33) for x in range(4, 13) if S5[y, x] in (12, 14) or (x, y) == (9, 30)}
# groepen (op s5-index + plaats)
G = np.full((64, 64), '', object)
for y in range(64):
    for x in range(64):
        o = S5[y, x]
        if A[y, x] == 0 or (x, y) in OOG: continue
        if o in (10, 11): G[y, x] = 'kuif'
        elif o in (13, 15) or (o == 6 and (y >= 50 or x <= 12 and y >= 34)): G[y, x] = 'grijs'
        elif o in (5, 6): G[y, x] = 'creme'
        elif o in (7, 8, 9): G[y, x] = 'krop'
for x, y, g in H.get('groep', []): G[y, x] = g
for y in range(49, 64):
    for x in range(64):
        if G[y, x] == 'grijs': G[y, x] = 'poot'
TINT = {'kuif': (12, 13, 14), 'grijs': (6, 7, 1), 'poot': (6, 7, 7), 'creme': (5, 6, 7), 'krop': (9, 10, 11)}
BASIS = {'poot': 7, 'kuif': 13, 'grijs': 7, 'creme': 5, 'krop': 10}
def binnen(x, y): return 0 <= x < 64 and 0 <= y < 64
def uit(x, y, g, dx, dy, n):          # stappen tot de vorm g verlaten wordt in richting (dx,dy)
    for k in range(1, n + 1):
        if not binnen(x + k*dx, y + k*dy) or G[y + k*dy, x + k*dx] != g: return k
    return n + 1
B = A.copy()
for y in range(64):
    for x in range(64):
        g = G[y, x]
        if not g: continue
        L, M, D = TINT[g]
        lucht = {d for d, (dx, dy) in {'r': (1, 0), 'o': (0, 1), 'l': (-1, 0), 'b': (0, -1)}.items()
                 if not binnen(x + dx, y + dy) or A[y + dy, x + dx] == 0}
        # dikte van het onderdeel in de richting van de lucht (dunne delen: geen eigen lijn, wel donkere tint)
        dik = {'r': uit(x, y, g, -1, 0, 3), 'l': uit(x, y, g, 1, 0, 3), 'o': uit(x, y, g, 0, -1, 3), 'b': uit(x, y, g, 0, 1, 3)}
        if any(dik[d] >= 2 for d in lucht & {'r', 'o'}) and not {'l', 'r'} <= lucht: B[y, x] = 1   # schaduwkant: zwart
        elif any(dik[d] >= 3 for d in lucht & {'l', 'b'}): B[y, x] = D                            # lichtkant: selout
        elif lucht & {'r', 'o'}: B[y, x] = D
        elif lucht: B[y, x] = L if g == 'poot' else M
        else:
            br = min(uit(x, y, g, 1, 0, 3), uit(x, y, g, 0, 1, 3), uit(x, y, g, 1, 1, 3))
            tl = min(uit(x, y, g, -1, 0, 3), uit(x, y, g, 0, -1, 3), uit(x, y, g, -1, -1, 3))
            B[y, x] = D if br <= 1 else L if tl <= (2 if g == "krop" else 1) else BASIS[g]
# R3: verre vleugel (x15-28, y7-19): losse lichte 2-pixels -> vlak 4, behalve de bovenrand (<= 2 px onder de lucht)
for y in range(7, 20):
    for x in range(15, 29):
        if B[y, x] == 2 and not any(y - k >= 0 and B[y - k, x] == 0 for k in (1, 2, 3)): B[y, x] = 4
# R4: nabije vleugel (x40-60, y5-22): zwarte binnenpixels die op een andere zwarte binnenpixel staan (2 px dikke
#     penlijn) -> pentint van de buur eronder; zo blijft per penscheiding 1 px
def lucht4(x, y): return any(B[y + b, x + a] == 0 for a, b in ((1, 0), (-1, 0), (0, 1), (0, -1)))
for y in range(6, 22):
    for x in range(40, 60):
        if B[y, x] == 1 and B[y - 1, x] == 1 and not lucht4(x, y) and not lucht4(x, y - 1) and B[y + 1, x] in (2, 3, 4):
            B[y, x] = B[y + 1, x]
# R6: lijf (3-vlak, x27-45, y33-48): sikkel 4 langs rechter-/ondercontour (2 px), lichte band 2 langs de linkerrand
R6 = B.copy()
for y in range(33, 49):
    for x in range(27, 46):
        if R6[y, x] != 3: continue
        if any(R6[y + b, x + a] in (0, 1) for a, b in ((1, 0), (2, 0), (0, 1), (0, 2), (1, 1))): B[y, x] = 4
        elif x <= 33 and any(R6[y, x - k] == 1 for k in (1, 2)): B[y, x] = 2
# krop: cel-shading van het model overnemen (modeltint 6/7/8 -> 9/10/11) voor binnenpixels
K = np.load('../s5/onderlaag.npy')
for y in range(64):
    for x in range(64):
        if G[y, x] == 'krop' and B[y, x] in (9, 10, 11) and K[y, x] in (6, 7, 8) and \
           not any(A[y + b, x + a] == 0 for a, b in ((1, 0), (-1, 0), (0, 1), (0, -1))):
            B[y, x] = {6: 9, 7: 10, 8: 11}[K[y, x]]
for x, y, v in H['px']: B[y, x] = v
# dambord in de vleugels/het lijf (1-px diagonale penlijn op een vlak): de pixel linksboven van de stap wordt de
# lichte penrand (een tint lichter); is die al de lichtste, dan de pixel rechtsonder een tint donkerder
for _ in range(3):
    for y in range(63):
        for x in range(63):
            p, q, r, t = B[y, x], B[y, x + 1], B[y + 1, x], B[y + 1, x + 1]
            if not (p and q and p == t and q == r and p != q): continue
            if {p, q} <= {1, 2, 3, 4}:
                if q == 1: B[y, x] = p - 1 if p > 2 else p; B[y + 1, x + 1] = 3 if p == 2 else B[y + 1, x + 1]
                elif p == 1: B[y, x + 1] = q - 1 if q > 2 else q; B[y + 1, x] = 3 if q == 2 else B[y + 1, x]
                else: B[y + 1, x + 1] = q
im = Image.fromarray(B.astype(np.uint8), 'P'); flat = [c for p in PAL for c in p]; im.putpalette(flat); im.save('hoatzin.png', transparency=0)
im.convert('RGB').resize((512, 512), Image.NEAREST).save('hoatzin_8x.png')
with open('normal.pal', 'w') as f: f.write('JASC-PAL\r\n0100\r\n16\r\n' + ''.join('%d %d %d\r\n' % p for p in PAL))
np.save('groep.npy', G.astype(str))
# bewijs: silhouet gelijk aan s5 behalve 'weg'; oog ongewijzigd
z5, z6 = S5 > 0, B > 0
print('silhouet anders:', sorted((int(x), int(y)) for y, x in zip(*np.where(z5 != z6))))
print('oog anders:', [p for p in OOG if PAL[B[p[1], p[0]]] != [(255,)*3, (16, 14, 24)][0] and B[p[1], p[0]] != {12: 15, 14: 8}.get(S5[p[1], p[0]], 1)])
