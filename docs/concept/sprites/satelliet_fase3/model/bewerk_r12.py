# r12 (Jordi, 25 nov): "rechtse oog is nog niet netjes, het oog zou ook iets groter moeten zijn vanwege de pose,
# plus ik zie daar gekke zwarte pixels, je kan het niet zomaar kopieren".
# Vanuit r11; alleen het rechter zij-oog opnieuw, gebouwd uit het GROTE voorste oog:
#  - schaal = hoogte rechter zijbol / hoogte voorste oogbol (24/42), vlakgewogen reductie per klasse
#    (ring / iris / pupil+rand), kleur = dichtstbijzijnde kleur uit het palet van het voorste oog (geen nieuwe kleuren);
#  - plaats: zelfde relatieve positie in de bol als het voorste oog in zijn bol, niet tegen de kraagomlijning;
#  - oude r11-oog eerst terug naar eigen bolkleuren (per kolom de dichtstbijzijnde bolpixel boven/onder).
# Coordinaten = r10/r11-beeld (x_r9 = X - 21, y_r9 = Y + 15).
from PIL import Image
import numpy as np

R = np.asarray(Image.open('r11_natief.png').convert('RGB')).astype(int)
H, W = R.shape[:2]
out = R.copy()

def cls(c):
    r, g, b = c; l = (r + g + b) / 3
    if g > r + 20 and b > r + 10: return 'T'
    if r > g + 25 and b > g + 25 and l > 60: return 'P'
    if l < 60: return 'o'
    if l > 235 and max(c) - min(c) < 20: return '.'
    if l > 150: return 'w'
    return '-'
def ell(x, y, cx, cy, rx, ry): return ((x - cx) / rx) ** 2 + ((y - cy) / ry) ** 2 <= 1

# ---------------------------------------------------------------- maten
FRONT_BULB_H = 148 - 107 + 1      # voorste oogbol, rij 107..148
RIGHT_BULB_H = 103 - 80 + 1       # rechter zijbol, rij 80..103
FE = (44, 119, 65, 142)           # voorste oog incl. ring en donkere buitenrand (x0,y0,x1,y1)
FB = (41, 107, 82, 148)           # voorste bol
RB = (175, 80, 200, 103)          # rechter bol (vanaf de kraagomlijning)
s = RIGHT_BULB_H / FRONT_BULB_H

# bronmasker voorste oog: ring, iris, pupil, donkere ringrand (geen bolvulling, geen wit)
fcx, fcy = (FE[0] + FE[2]) / 2, (FE[1] + FE[3]) / 2
frx, fry = (FE[2] - FE[0]) / 2 + 0.6, (FE[3] - FE[1]) / 2 + 0.6
src = {}
for y in range(FE[1], FE[3] + 1):
    for x in range(FE[0], FE[2] + 1):
        if ell(x, y, fcx, fcy, frx, fry) and cls(R[y, x]) in 'TPo-':
            src[(x, y)] = R[y, x]
palette = np.array(sorted({tuple(c) for c in src.values()}))

tw = int(round((FE[2] - FE[0] + 1) * s)); th = int(round((FE[3] - FE[1] + 1) * s))
# klasse per bronpixel: ring / iris / donker
def k(c):
    q = cls(c)
    return {'T': 'T', 'P': 'P', 'o': 'o', '-': 'o'}[q]
eye = {}
for j in range(th):
    for i in range(tw):
        x0 = FE[0] + i / s; x1 = FE[0] + (i + 1) / s
        y0 = FE[1] + j / s; y1 = FE[1] + (j + 1) / s
        acc = {}; tot = 0.0
        for y in range(int(np.floor(y0)), int(np.ceil(y1))):
            for x in range(int(np.floor(x0)), int(np.ceil(x1))):
                a = (min(x + 1, x1) - max(x, x0)) * (min(y + 1, y1) - max(y, y0))
                if a <= 0: continue
                tot += a
                if (x, y) in src:
                    c = src[(x, y)]; kk = k(c)
                    acc.setdefault(kk, [0.0, np.zeros(3)]); acc[kk][0] += a; acc[kk][1] += a * c
        cover = sum(v[0] for v in acc.values())
        if cover < 0.5 * tot: continue                    # vooral bol: geen oogpixel
        kk = max(acc, key=lambda q: acc[q][0])
        mean = acc[kk][1] / acc[kk][0]
        eye[(i, j)] = palette[np.argmin(((palette - mean) ** 2).sum(1))]

# ---------------------------------------------------------------- per pixel opschonen
def klass(c): return k(c)
# (1) losse donkere pixels in de iris (niet aan pupil of ring-buitenrand vast) -> iris uit de buren
changed = True
while changed:
    changed = False
    for (i, j), c in list(eye.items()):
        if klass(c) != 'o': continue
        nb = [eye.get((i + dx, j + dy)) for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))]
        outer = any(v is None for v in nb)                # buitenrand van de ring mag donker
        darkn = sum(1 for v in nb if v is not None and klass(v) == 'o')
        if not outer and darkn == 0:
            t = [v for v in nb if v is not None and klass(v) == 'T']
            if t: eye[(i, j)] = t[0]; changed = True

# ---------------------------------------------------------------- plaats in de rechterbol
rel_x = (fcx - FB[0]) / (FB[2] - FB[0]); rel_y = (fcy - FB[1]) / (FB[3] - FB[1])
cx = RB[0] + rel_x * (RB[2] - RB[0]); cy = RB[1] + rel_y * (RB[3] - RB[1])
ox = int(round(cx - (tw - 1) / 2)); oy = int(round(cy - (th - 1) / 2))
ox = max(ox, 178)                     # kraagomlijning (x 175-176) niet raken: minstens 1 px bol ertussen
print('schaal %.3f  oog %dx%d  plaats x %d..%d  y %d..%d' % (s, tw, th, ox, ox + tw - 1, oy, oy + th - 1))

# ---------------------------------------------------------------- oude r11-oog weg: eigen bolkleuren
OLD = {(x, y) for y in range(84, 100) for x in range(177, 194) if cls(R[y, x]) in 'TPo-'
       and ell(x, y, 185, 91.5, 7.2, 6.6)}
def is_fill(x, y): return (x, y) not in OLD and cls(R[y, x]) in 'w.' and x >= 177
for (x, y) in OLD:
    best = None
    for d in range(1, 12):
        for yy in (y - d, y + d):
            if 0 <= yy < H and is_fill(x, yy): best = (x, yy); break
        if best: break
    if best is None:
        cands = [(xx, yy) for xx in range(177, 200) for yy in range(80, 104) if is_fill(xx, yy)]
        best = min(cands, key=lambda q: (q[0] - x) ** 2 + (q[1] - y) ** 2)
    out[y, x] = R[best[1], best[0]]

for (i, j), c in eye.items(): out[oy + j, ox + i] = c

# resten van het r9-oog (onderrand van de oude ring, r9 x167..180 y100..114 = hier x188..201 y85..99) die in r11
# bleven staan: donker/paars/turkoois binnen de bol, niet aan de buitenrand -> eigen bolkleur uit dezelfde kolom
newp = {(ox + i, oy + j) for (i, j) in eye}
def bgp(x, y): return np.all(out[y, x] >= 250)
for y in range(84, 102):
    for x in range(186, 203):
        if (x, y) in newp or not ell(x, y, 194.5, 92.5, 8.0, 8.8): continue
        if cls(out[y, x]) not in 'TPo-': continue
        if any(bgp(x + dx, y + dy) for dx in (-1, 0, 1) for dy in (-1, 0, 1)): continue   # bolomlijning
        best = None
        for d in range(1, 12):
            for yy in (y - d, y + d):
                if (x, yy) not in newp and cls(out[yy, x]) in 'w.' and not bgp(x, yy): best = yy; break
            if best: break
        if best: out[y, x] = out[best, x]; print('rest weg', (x, y))

# ---------------------------------------------------------------- controle
newp = {(ox + i, oy + j) for (i, j) in eye}
wit = [p for p in newp if out[p[1], p[0]].sum() / 3 > 190]
touch = [p for p in newp if p[0] <= 176]
print('oogpixels', len(newp), 'wit', len(wit), 'raakt kraag', len(touch))
def diam(pts):
    xs = [p[0] for p in pts]; ys = [p[1] for p in pts]; return max(xs) - min(xs) + 1, max(ys) - min(ys) + 1
print('voorste oog (b x h):', diam(src), ' rechts:', diam(newp))

im = Image.fromarray(out.astype('uint8')); im.save('r12_natief.png')
im.resize((W * 8, H * 8), Image.NEAREST).save('r12_natief_8x.png')
r11 = Image.fromarray(R.astype('uint8'))
a = r11.crop((172, 76, 204, 106)); b = im.crop((172, 76, 204, 106)); f = im.crop((38, 104, 86, 152))
S = 8
sh = Image.new('RGB', (32 * S * 2 + 48 * S + 32, 48 * S), 'white')
sh.paste(a.resize((32 * S, 30 * S), Image.NEAREST), (0, 0))
sh.paste(b.resize((32 * S, 30 * S), Image.NEAREST), (32 * S + 16, 0))
sh.paste(f.resize((48 * S, 48 * S), Image.NEAREST), (64 * S + 32, 0))
sh.save('r12_rechteroog.png')
