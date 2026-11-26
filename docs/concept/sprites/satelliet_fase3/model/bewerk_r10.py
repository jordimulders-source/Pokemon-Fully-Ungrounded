# r10: reparaties op het r9-model (Jordi, 25 nov; zie ../SPEC.md onderaan).
# Werkt in het ECHTE natieve raster van gemini/r9.png: pitch 5,12 px (200x200, natief200.py).
# Het 99-px raster (pitch 10,24) is elke tweede cel en verliest de paneelrasterlijnen.
# Alles met bestaande pixels: verschuiven, cellen herhalen/weghalen, kopieren, spiegelen.
from PIL import Image
import numpy as np, sys

SRC = 'r9_natief200.png'
old = np.asarray(Image.open(SRC).convert('RGB')).astype(int)
H0, W0 = old.shape[:2]
PADL, PADR, PADT, PADB = 40, 20, 0, 0          # canvas groter: LF links, tweeling rechts
H, W = H0 + PADT + PADB, W0 + PADL + PADR
WHITE = np.array([255, 255, 255])

def lum(c): return (c[0] + c[1] + c[2]) / 3
def is_white(c): return lum(c) > 235 and max(c) - min(c) < 20

def O(x, y):
    """oud pixel in r9-coordinaten (wit buiten het beeld)"""
    if 0 <= x < W0 and 0 <= y < H0: return old[y, x].copy()
    return WHITE.copy()

def new_canvas():
    a = np.full((H, W, 3), 255, int)
    a[PADT:PADT + H0, PADL:PADL + W0] = old
    return a

class Img:
    def __init__(self): self.a = new_canvas()
    def g(self, x, y):
        X, Y = x + PADL, y + PADT
        if 0 <= X < W and 0 <= Y < H: return self.a[Y, X].copy()
        return WHITE.copy()
    def s(self, x, y, c):
        X, Y = x + PADL, y + PADT
        if 0 <= X < W and 0 <= Y < H: self.a[Y, X] = c
    def coords(self):
        for Y in range(H):
            for X in range(W): yield X - PADL, Y - PADT

def bg_of(im):
    """achtergrond = vanaf de rand bereikbaar wit (dus niet de bijna witte glans op de bollen)"""
    a = im.a; h, w = a.shape[:2]
    seen = np.zeros((h, w), bool); st = [(0, 0), (w - 1, 0), (0, h - 1), (w - 1, h - 1)]
    while st:
        x, y = st.pop()
        if not (0 <= x < w and 0 <= y < h) or seen[y, x]: continue
        if not is_white(a[y, x]): continue
        seen[y, x] = True
        st += [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]
    return lambda x, y: 0 <= x + PADL < w and 0 <= y + PADT < h and seen[y + PADT, x + PADL]

# ---------------------------------------------------------------- 1. RF (rechtsvoor) 5 -> 4 vakken
# dwarslijnen // kapjes, richting (-12,15): f = 15x + 12y.  Celperiode D = (11,4) (autocorrelatie).
# Knip midden in vak 4 en schuif vak 5 + eindkap een periode terug: vak 4 verdwijnt.
def rf_top(x): return 140 + (x - 101) / 3.0          # bovenrand RF (omlijning ligt op deze lijn)
RF_D = (11, 4)
def f_rf(x, y): return 15 * x + 12 * y
RF_CUT = f_rf(116, 155)          # midden van vak 4 (tussen dwarslijnen x+y~260 en ~276)

def step_rf(im):
    src = Img(); src.a = im.a.copy()
    for x, y in list(im.coords()):
        if not (100 <= x <= 145 and 140 <= y <= 175): continue
        if y < rf_top(x) - 0.6: continue                 # boven RF (mast): niet aanraken
        if f_rf(x, y) < RF_CUT: continue
        sx, sy = x + RF_D[0], y + RF_D[1]
        c = O(sx, sy)
        if sy < rf_top(sx) - 0.6: c = WHITE.copy()      # bron boven RF = geen paneel
        im.s(x, y, c)

# ---------------------------------------------------------------- 2. mast onder 2 -> 3 vakken
# mastkolom x 101..115; dwarslijnen // (1,1): f = y - x.  Kap boven f~8, dwarslijn f~22, eindkap f~33.
# Een periode (0,13) herhalen vanaf f=29: eindkap komt op f~46 en valt achter RF.
M_P = 13
def step_mast(im):
    for x in range(101, 116):
        for y in range(120, 175):
            if y >= rf_top(x) - 0.6: continue           # RF ligt ervoor
            if y - x < 29: continue
            sy = y - M_P
            im.s(x, y, O(x, sy))

# ---------------------------------------------------------------- 3. LF (linksvoor) 3 -> 4 vakken + staafje
# LF hoort achter de grote bol (verre paneel). Kapjes // (-16,9): f = 9x + 16y.
# Oud: verre kap f~1888, dwarslijnen f~2036 en ~2188, daarna liep vak 3 half achter bol/ring (f~2290) = "lijkt 3".
# Periode DL=(10,4) (f +154).  Nieuw:
#  (a) hele paneel langs de as naar buiten: S=(-8,-3) (f -120), zodat het vrij van de bol ligt en er plek is voor een staafje;
#  (b) aan de verre kant een periode erbij (knip midden in vak 1);
#  (c) vak 4 (half verborgen in r9) periodiek uit vak 3 aangevuld; nabije kap = waar de volgende dwarslijn valt (f~2220),
#      met daarachter een pixel omlijning (zoals de verre kap);
#  (d) staafje van RF gekopieerd (zelfde asrichting), achter de bol; bolrand gesloten waar het paneel hem bedekte.
DL = (10, 4)
def f_lf(x, y): return 9 * x + 16 * y
LF_CUT = 1888 + 77            # midden vak 1 (oud)
S_LF = (-8, -3)
LF_NEAR = 2220                # nieuwe nabije kap
LF_LAST = 2188                # laatste goede dwarslijn (oud)
OUTLINE_DARK = np.array([28, 24, 48])      # paneelomlijning (r9, bijv. (24,128))
BULB_EDGE = np.array([103, 102, 125])      # bolomlijning lichte kant (r9, (24,130))

def lf_old_mask(x, y):
    if not (0 <= x <= 44 and 106 <= y <= 128): return False
    c = O(x, y)
    if lum(c) >= 150: return False
    if x >= 23 and y >= 129: return False
    return True

def bulb_mask_old(x, y):
    """lichte vulling van de grote oogbol rond LF"""
    if not (18 <= x <= 47 and 118 <= y <= 135): return False
    c = O(x, y)
    if c[0] > c[1] + 25 and c[2] > c[1] + 25: return False      # paarse ring hoort er niet bij
    return lum(c) >= 150 and not is_white(c)

LF_TOP = lambda x: 109 + (x - 16) / 3.0           # bovenrand oud
LF_BOT = lambda x: 119 + (x - 2) * 10 / 24.0      # onderrand oud
def lf_inside_old(x, y):
    return LF_TOP(x) - 1.2 <= y <= LF_BOT(x) + 1.2 and f_lf(x, y) >= 1888 - 20

def lf_src(px, py):
    if f_lf(px, py) > LF_NEAR + 6: return None
    qx, qy = px - S_LF[0], py - S_LF[1]
    if f_lf(qx, qy) < LF_CUT: qx, qy = qx + DL[0], qy + DL[1]
    if f_lf(qx, qy) > LF_LAST + 6: qx, qy = qx - DL[0], qy - DL[1]     # vak 4 uit vak 3
    if not lf_inside_old(qx, qy): return None
    for k in range(3):
        sx, sy = qx - k * DL[0], qy - k * DL[1]
        if lf_old_mask(sx, sy): return O(sx, sy)
    return None

def step_lf(im):
    for x in range(0, 45):
        for y in range(106, 129):
            if lf_old_mask(x, y): im.s(x, y, WHITE)
    panel = set()
    for x in range(-40, 45):
        for y in range(95, 132):
            if bulb_mask_old(x, y): continue
            c = lf_src(x, y)
            if c is None: continue
            im.s(x, y, c); panel.add((x, y))
    bg = bg_of(im)
    # omlijning achter de nabije kap
    for (x, y) in list(panel):
        for dx, dy in ((1, 0), (0, 1)):
            n = (x + dx, y + dy)
            if n in panel or f_lf(*n) <= LF_NEAR or f_lf(*n) > LF_NEAR + 18: continue
            if bg(*n): im.s(n[0], n[1], OUTLINE_DARK)
    # bolrand sluiten: wit pixel direct boven bolvulling
    edge = {}
    for x in range(20, 46):
        for y in range(115, 132):
            if bulb_mask_old(x, y) and not bulb_mask_old(x, y - 1) and is_white(im.g(x, y - 1)):
                im.s(x, y - 1, BULB_EDGE); edge[x] = y - 1; break
    # kuiltjes in de rand (bijna witte glans van de bol telde als achtergrond): rand 1 omhoog, bolvulling eronder
    for x in sorted(edge):
        lft = [edge[k] for k in (x - 2, x - 1) if k in edge]
        rgt = [edge[k] for k in (x + 1, x + 2) if k in edge]
        if lft and rgt and edge[x] > min(lft) and edge[x] > min(rgt):
            y = edge[x]
            im.s(x, y, im.g(x, y + 1)); im.s(x, y - 1, BULB_EDGE); edge[x] = y - 1
    # staafje: RF-staafje (r9 x67..75, y136..141) verschoven naar de zichtbare ringrand boven de bol, alleen op wit
    T = (38 - 68, 117 - 137)     # linkereind tegen de nabije kap, rechtereind in de ring
    bg = bg_of(im)
    for y in range(136, 142):
        for x in range(67, 76):
            c = O(x, y)
            if is_white(c) or lum(c) > 200: continue
            tx, ty = x + T[0], y + T[1]
            if bg(tx, ty): im.s(tx, ty, c)
    # gaatjes in het staafje (lichte bronpixels) dicht met de buurkleur links
    for y in range(136 + T[1], 142 + T[1]):
        for x in range(66 + T[0], 76 + T[0]):
            if is_white(im.g(x, y)) and not is_white(im.g(x - 1, y)) and not is_white(im.g(x + 1, y)):
                im.s(x, y, im.g(x - 1, y))

# ---------------------------------------------------------------- 4. tweeling van het paneel linksboven (BL)
# BL: kapjes // (-14,10): f = 10x + 14y; linkerkap f=1200 ((64,40)-(50,50)), rechterkap f=1940, 4 vakken,
# periode (13,4) (f +186). Het stuk achter de mast (x 102..111) wordt aangevuld: kapzone uit de linkerkap
# (+4 vakken = (53,15)), de rest uit het vak ernaast. De tweeling = dit volledige paneel verschoven (licht blijft
# gelijk), op de plek van Jordi's rode schets maar iets hoger, tegen de achterarm; alleen op wit, dus achter
# achterarm, rechter zijarm en oogbol. Staafje = het BL-staafje (r9 x111..124, y60..66) verschoven.
def f_bl(x, y): return 10 * x + 14 * y
BL_TOP = lambda x: 40 + (x - 64) * 15 / 53.0
BL_BOT = lambda x: 50 + (x - 50) * 15 / 53.0
MAST_X = (102, 111)
def bl_in_poly(x, y):
    return BL_TOP(x) - 1.5 <= y <= BL_BOT(x) + 1.5 and 1185 <= f_bl(x, y) <= 1955
def bl_vis(x, y):
    if not bl_in_poly(x, y) or MAST_X[0] <= x <= MAST_X[1]: return False
    c = O(x, y)
    return not is_white(c) and lum(c) < 160
def bl_full(x, y):
    if not bl_in_poly(x, y): return None
    if bl_vis(x, y): return O(x, y)
    if not (MAST_X[0] <= x <= MAST_X[1]): return None
    if f_bl(x, y) >= 1940 - 16:
        sx, sy = x - 53, y - 15
        if bl_vis(sx, sy): return O(sx, sy)
        return None
    for k in (1, 2):
        sx, sy = x - 13 * k, y - 4 * k
        if bl_vis(sx, sy): return O(sx, sy)
    return None

TWIN_T = (89, 38)
def step_twin(im):
    bg = bg_of(im)
    for x in range(48, 120):
        for y in range(36, 70):
            c = bl_full(x, y)
            if c is None: continue
            tx, ty = x + TWIN_T[0], y + TWIN_T[1]
            if bg(tx, ty): im.s(tx, ty, c)
    # staafje: rechtereind (124,65) op 40% van de linkerkap van de tweeling
    P = (64 - 0.4 * 14 + TWIN_T[0], 40 + 0.4 * 10 + TWIN_T[1])
    RT = (round(P[0] - 124), round(P[1] - 65))
    for x in range(112, 125):
        for y in range(60, 67):
            c = O(x, y)
            if is_white(c) or lum(c) > 200: continue
            if f_bl(x, y) <= 1955: continue                 # alleen staafje, niet het paneel
            tx, ty = x + RT[0], y + RT[1]
            if bg(tx, ty): im.s(tx, ty, c)

# ---------------------------------------------------------------- 5. ogen: binnen de paarse ring alleen iris + pupil
def cls(c):
    r, g, b = c; l = (r + g + b) / 3
    if g > r + 20 and b > r + 10: return 'T'
    if r > g + 25 and b > g + 25 and l > 60: return 'P'
    if l < 60: return 'o'
    if l > 150: return 'w'
    return '-'

def clean_eye(im, box, seed, ell):
    x0, y0, x1, y1 = box
    ecx, ecy, erx, ery = ell
    reg, todo = set(), [seed]
    while todo:
        p = todo.pop()
        if p in reg: continue
        x, y = p
        if not (x0 <= x <= x1 and y0 <= y <= y1): continue
        if ((x - ecx) / erx) ** 2 + ((y - ecy) / ery) ** 2 > 1: continue
        if cls(im.g(x, y)) == 'P': continue
        reg.add(p)
        todo += [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]
    glans = lambda c: lum(c) > 190                     # witte en bijna witte (glans)pixels
    teal = {p: im.g(*p) for p in reg if cls(im.g(*p)) == 'T' and not glans(im.g(*p))}
    fix = [p for p in reg if cls(im.g(*p)) == 'w' or glans(im.g(*p))]
    # dichtstbijzijnde iriskleur (bestaande pixels), van buiten naar binnen niets verzinnen
    out = {}
    for (x, y) in fix:
        best = min(teal, key=lambda q: (q[0] - x) ** 2 + (q[1] - y) ** 2)
        out[(x, y)] = teal[best]
    for p, c in out.items(): im.s(p[0], p[1], c)
    return len(reg), len(fix)

def step_eyes(im):
    print('groot oog', clean_eye(im, (24, 134, 44, 158), (32, 146), (32.5, 146.5, 8.0, 8.8)))
    print('rechteroog', clean_eye(im, (166, 100, 181, 116), (174, 108), (174.0, 108.0, 4.8, 6.3)))

# ---------------------------------------------------------------- 6. linkeroog, twee varianten
LEFT_EYE_BOX = (41, 71, 53, 89)

def left_eye_pixels():
    """pixels van het huidige linkeroog (ring, iris, pupil, glans, omlijning links)"""
    x0, y0, x1, y1 = LEFT_EYE_BOX
    reg = set()
    for x in range(x0, x1 + 1):
        for y in range(y0, y1 + 1):
            c = O(x, y)
            k = cls(c)
            if k in 'TP': reg.add((x, y))
    # alles binnen de ring (pupil, glans, donkere randjes) erbij
    for y in range(y0, y1 + 1):
        xs = [x for (x, yy) in reg if yy == y]
        if xs:
            for x in range(min(xs), max(xs) + 1): reg.add((x, y))
    return reg

def variant_b(im):
    """oog kijkt langs de linkerarm naar links-achter: smalle staande ellips op de linkerrand.
    Bron: het (opgeschoonde) rechteroog, gespiegeld, kolommen/rijen geschrapt (niets getekend)."""
    cols = [179, 178, 177, 175, 174, 172, 170, 168]        # gespiegeld: omlijning links, dikke ring rechts
    rows = [r for r in range(100, 116) if r not in (103, 112)]
    src = Img(); src.a = im.a.copy()
    eye = {}
    for j, ry in enumerate(rows):
        for i, rx in enumerate(cols):
            c = src.g(rx, ry)
            if cls(c) in 'TPo-': eye[(i, j)] = c
    # oude ooggebied naar bolvulling (dichtstbijzijnde bolpixel uit r9)
    oldeye = left_eye_pixels()
    bulb = [(x, y) for x in range(40, 60) for y in range(66, 92)
            if (x, y) not in oldeye and cls(O(x, y)) in 'w' and not is_white(O(x, y))]
    ox, oy = 43, 80 - len(rows) // 2
    neweye = {(ox + i, oy + j): c for (i, j), c in eye.items()}
    for (x, y) in oldeye:
        if (x, y) in neweye: continue
        if x <= 43:                                   # linker silhouet: wit buiten de bol
            im.s(x, y, WHITE); continue
        b = min(bulb, key=lambda q: (q[0] - x) ** 2 + (q[1] - y) ** 2)
        im.s(x, y, O(*b))
    for (x, y), c in neweye.items(): im.s(x, y, c)
    return neweye

def variant_a(im):
    """rechter zijbol + oog gespiegeld naar links, iets kleiner (rijen 26->24 geschrapt)."""
    src = Img(); src.a = im.a.copy()
    K, cy_d, cy_s = 222, 79.5, 105.5
    for x in range(38, 58):
        for y in range(64, 95):
            sx = K - x
            sy = int(round(cy_s + (y - cy_d) * 26 / 24.0))
            in_eye = ((sx - 174) / 4.8) ** 2 + ((sy - 108) / 6.3) ** 2 <= 1
            c = src.g(sx, sy) if (in_eye or not is_white(O(sx, sy))) else WHITE.copy()   # alleen de r9-bol (niet de tweeling)
            d = im.g(x, y)
            if is_white(c) and is_white(d): continue
            im.s(x, y, c)

# ---------------------------------------------------------------- run
# ---------------------------------------------------------------- afronden
def background_white(a):
    """achtergrond (vanaf de rand bereikbaar bijna-wit) puur wit; de bolglans blijft zoals hij is"""
    h, w = a.shape[:2]
    seen = np.zeros((h, w), bool); st = [(0, 0), (w - 1, 0), (0, h - 1), (w - 1, h - 1)]
    while st:
        x, y = st.pop()
        if not (0 <= x < w and 0 <= y < h) or seen[y, x]: continue
        if not is_white(a[y, x]): continue
        seen[y, x] = True; a[y, x] = 255
        st += [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]
    return seen

def strays(a, bg, region=None):
    h, w = a.shape[:2]; out = []
    for y in range(1, h - 1):
        for x in range(1, w - 1):
            if bg[y, x]: continue
            n = int((~bg[y - 1:y + 2, x - 1:x + 2]).sum()) - 1
            if n <= 1: out.append((x - PADL, y - PADT))
    return out

def finish(im, changed):
    a = im.a
    bg = background_white(a)
    for (x, y) in strays(a, bg):
        if (x, y) in changed or any((x + dx, y + dy) in changed for dx in (-1, 0, 1) for dy in (-1, 0, 1)):
            im.s(x, y, WHITE)
    bg = background_white(a)
    return bg

def changed_set(a):
    ref = new_canvas()
    d = np.abs(a - ref).sum(2) > 0
    ys, xs = np.where(d)
    return {(x - PADL, y - PADT) for x, y in zip(xs, ys)}

def crop_box(arrs, m=3):
    xs0, ys0, xs1, ys1 = [], [], [], []
    for a in arrs:
        nb = ~(np.all(a >= 250, axis=2))
        ys, xs = np.where(nb)
        xs0.append(xs.min()); xs1.append(xs.max()); ys0.append(ys.min()); ys1.append(ys.max())
    return max(0, min(xs0) - m), max(0, min(ys0) - m), min(W, max(xs1) + m + 1), min(H, max(ys1) + m + 1)

def save(a, name, box):
    x0, y0, x1, y1 = box
    im = Image.fromarray(a[y0:y1, x0:x1].astype('uint8'))
    im.save(name + '.png')
    im.resize((im.width * 8, im.height * 8), Image.NEAREST).save(name + '_8x.png')
    return im

if __name__ == '__main__':
    im = Img()
    step_rf(im)
    step_mast(im)
    step_lf(im)
    step_twin(im)
    step_eyes(im)
    ima = Img(); ima.a = im.a.copy()
    variant_b(im)
    variant_a(ima)
    for x_ in (im, ima): finish(x_, changed_set(x_.a))
    r9 = Img(); background_white(r9.a)
    box = crop_box([im.a, ima.a, r9.a])
    b = save(im.a, 'r10_natief', box)
    a_ = save(ima.a, 'r10a_natief', box)
    x0, y0, x1, y1 = box
    o = Image.fromarray(r9.a[y0:y1, x0:x1].astype('uint8'))
    w, h = o.size; S = 8; gap = 16
    sheet = Image.new('RGB', (w * S * 2 + gap, h * S), 'white')
    sheet.paste(o.resize((w * S, h * S), Image.NEAREST), (0, 0))
    sheet.paste(b.resize((w * S, h * S), Image.NEAREST), (w * S + gap, 0))
    sheet.save('r10_vs_r9.png')
    print('canvas', b.size, 'crop', box, '(r9-coordinaten: x', x0 - PADL, '..', x1 - PADL, ', y', y0 - PADT, '..', y1 - PADT, ')')
    bg = background_white(im.a.copy())
    print('losse pixels over (b):', strays(im.a, bg)[:40])
