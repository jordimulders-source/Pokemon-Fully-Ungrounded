# r18 op r17. Coordinator na r17: de "paarse lijn boven het hoofd" is in het model de bovenrand van het kleine (verre) paneel,
# die achter de kap doorloopt tot achter het grote gewricht, met daaronder pas een dunne lila rand en dan het wit.
# Daarnaast panelen en gewrichten opnieuw inkleuren vanuit het model (Jordi: "kleurtinten, lijnen, schaduw is nog niet goed").
# Draaien vanuit deze map: python3 toon.py && python3 vul.py && python3 bouw_r18.py && python3 vel_r18.py
import numpy as np
from PIL import Image
from collections import Counter
im0 = Image.open('../r17/sprite.png'); r17 = np.array(im0).astype(int); a = r17.copy()
r16 = np.array(Image.open('../r16/sprite.png')).astype(int)
pal = np.array(im0.getpalette()[:48]).reshape(16, 3)
V = np.load('vul_L.npy')          # vultoon van de panelen (model, zonder raster/lijnen, 3x3-venster)
H = '0123456789ABCDEF'
def put(x, y, s):
    for i, c in enumerate(s):
        if c != '-': a[y, x + i] = 0 if c == '.' else H.index(c)
N4 = ((-1, 0), (1, 0), (0, -1), (0, 1))

# ---------- paneelpalet (model: boven vul 82-87, onder 52-57, raster licht ±160 / donker ±105)
pal[9] = (44, 34, 84)      # donkere vul (schaduwdeel) + omlijning lichtkant
pal[10] = (84, 76, 150)    # lichte vul (bovendeel)
pal[11] = (112, 104, 182)  # glansband + raster in het schaduwdeel
pal[12] = (170, 158, 222)  # raster/kader in het lichte deel

# ---------- 1. bovenrand klein paneel achter de kap (gemeten per kolom in het model, 1024; zie verslag)
# model: buitenlijn rij 17 x19-24; paneelrand (paars) rij 18 x19-23 en rij 19 x20-22 (rechts loopt de rand 2 rijen dik naar beneden);
# navy binnen (19,19); dunne lila rand diagonaal (26,17)(25,17)(25,18)(24,18)(23,19)(22,20) met donkerder lila eronder (26,18)(24,19);
# kapcontour tegen het paneel (21,20) in de contourtint 5 zoals de rest van die contour.
put(19, 17, '999999')
put(25, 17, '66')
put(19, 18, 'BBBBB667')
a[18, 27] = 8                       # r17 overschreef hier per ongeluk de omlijning van de bol (r16 = 8)
put(19, 19, 'ABBB67')
put(19, 20, 'BB56')

# ---------- 2. groot paneel
seen = np.zeros((64, 64), bool); st = [(25, 55)]; seen[25, 55] = True; comp = []
while st:
    y, x = st.pop(); comp.append((y, x))
    for dy, dx in N4:
        ny, nx = y + dy, x + dx
        if 0 <= ny < 64 and 0 <= nx < 64 and not seen[ny, nx] and r17[ny, nx] in (9, 10, 11, 12): seen[ny, nx] = True; st.append((ny, nx))
P = seen.copy()
for y in range(33, 64):           # paars kader onderaan/rechtsonder (r17: 7/8) hoort bij het paneel (knop naast de lens niet)
    for x in range(29 if y >= 38 else 37, 64):
        if r17[y, x] in (7, 8) and any(P[y + dy, x + dx] for dy, dx in N4): P[y, x] = True
ROL = np.zeros((64, 64), int)    # 1 = vul, 2 = raster/kader
for y, x in zip(*np.nonzero(P)):
    v = r17[y, x]
    if any(r17[y + dy, x + dx] == 0 for dy, dx in N4) and v in (1, 9): continue      # buitenlijn blijft
    if v == 9 and V[y, x] >= 70: continue                                             # 9 in het lichte deel = omlijning (tegen antenne/lijf)
    licht = V[y, x] >= 70
    raster = v == 12 or v in (7, 8) or (v in (10, 11) and not licht)
    if v in (7, 8) and y >= 37:
        a[y, x] = 11; ROL[y, x] = 2            # kader in het schaduwdeel
    elif raster:
        a[y, x] = 12 if licht else 11; ROL[y, x] = 2
    else:
        a[y, x] = (11 if (y >= 30 and x <= 50) else 10) if licht else 9; ROL[y, x] = 1

# ---------- 3. klein paneel (achter): donkerder dan het grote; kader en raster in A (donker navy-paars), vul 9.
# Daarmee is ook de doorlopende bovenrand achter de kap (punt 1) een donkere navy-paarse band, zoals in het model.
seen = np.zeros((64, 64), bool); st = [(35, 5)]; seen[35, 5] = True
while st:
    y, x = st.pop()
    if a[y, x] == 10 and 20 <= y <= 24 and 11 <= x <= 17 and r17[y, x] == 10: a[y, x] = 9   # lichte vlek in r17; model vul 45-54
    elif a[y, x] == 11: a[y, x] = 10
    for dy, dx in N4:
        ny, nx = y + dy, x + dx
        if 0 <= ny < 64 and 0 <= nx < 26 and not seen[ny, nx] and a[ny, nx] in (9, 10, 11): seen[ny, nx] = True; st.append((ny, nx))

a[20, 16] = 10                      # losse 9 in de kaderband

# ---------- 4. gewrichten als bol: hooglicht linksboven, schaduw rechtsonder (r17 had hun glans per ongeluk als lijftint omgekleurd)
a[17, 29] = 3                                            # bol: glans (r16)
a[20, 38] = 3                                            # klein gewricht rechts: glans linksboven (r16); 6/7/8 naar rechtsonder staan al
put(32, 33, '636'); put(32, 34, '667'); put(32, 35, '677'); put(32, 36, '778'); put(32, 37, '88')   # knop naast de lens

# ---------- 5. lila onderschaduw: in het model iets lichter rechtsboven (naar de witte banden en het paneel); 4 daar, 5 de rest
for y in range(38, 43):
    for x in range(27, 33):
        if a[y, x] == 5 and r17[y, x] == 5 and not any(a[y + dy, x + dx] == 0 for dy, dx in N4): a[y, x] = 4

# ---------- opschonen: paneelvul-vlakjes < 3 px naar de meest voorkomende vulbuur
def clusters(arr, vals):
    seen = np.zeros_like(arr, bool); out = []
    for y in range(64):
        for x in range(64):
            if seen[y, x] or arr[y, x] not in vals: continue
            v = arr[y, x]; st = [(y, x)]; seen[y, x] = True; cl = []
            while st:
                cy, cx = st.pop(); cl.append((cy, cx))
                for dy, dx in N4:
                    ny, nx = cy + dy, cx + dx
                    if 0 <= ny < 64 and 0 <= nx < 64 and not seen[ny, nx] and arr[ny, nx] == v: seen[ny, nx] = True; st.append((ny, nx))
            out.append((v, cl))
    return out
for v, cl in clusters(a, {9, 10, 11}):
    if len(cl) >= 3: continue
    for y, x in cl:
        if ROL[y, x] != 1: continue
        c = Counter(a[y + dy, x + dx] for dy, dx in N4 if ROL[y + dy, x + dx] == 1 and a[y + dy, x + dx] != v)
        if c: a[y, x] = c.most_common(1)[0][0]

def sla(arr, naam):
    im = Image.fromarray(arr.astype('uint8'), 'P'); im.putpalette([int(v) for v in pal.flatten()] + [0] * (768 - 48))
    im.save(naam, transparency=0)
    b = Image.new('RGBA', (64, 64), (255, 255, 255, 255)); m = np.array(im.convert('RGBA')); m[arr == 0, 3] = 0; b.alpha_composite(Image.fromarray(m))
    b.convert('RGB').resize((512, 512), Image.NEAREST).save(naam.replace('.png', '_8x.png'))
if __name__ == '__main__':
    sla(a, 'sprite.png'); np.save('r18.npy', a)
    H2 = '.123456789ABCDEF'
    print('   ' + ''.join(str(x % 10) for x in range(64)))
    for y in range(12, 56): print('%2d ' % y + ''.join(H2[v] for v in a[y]))
    print('silhouet-diff t.o.v. r16:', int(((a == 0) != (r16 == 0)).sum()), ' gewijzigd t.o.v. r17:', int((a != r17).sum()), ' kleuren:', len(np.unique(a)))
