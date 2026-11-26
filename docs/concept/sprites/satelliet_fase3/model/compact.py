# compact (Jordi, 25 nov): de sprite is "heel erg blurry" ... "dat die het vak niet vult".
# Model r13b (model_gekozen.png, 231x159) compacter maken ZONDER te tekenen:
#  - hele paneelvakken weghalen: knip midden in een vak en schuif het eindstuk (eindkap) een of twee
#    periodes terug langs de eigen paneelrichting (zoals bewerk_r10 step_rf);
#  - waar een korter paneel iets vrijgeeft wat erachter zat (onderste mast achter RF): de mast uit zijn eigen
#    periode (13 px verticaal) en zijn r9-eindkap (langs de kap zelf doorgekopieerd);
#  - canvas bijsnijden.
# Romp, bollen, ogen blijven pixel voor pixel gelijk (gecontroleerd met een diffmasker).
# Panelen schuiven naar de buis bleek niet te kunnen: LF raakt de grote bol al, de tweeling zit al achter de arm,
# RF zou de mast vrijgeven zonder iets te winnen.
# Coordinaten: model X = r9 x + 21, Y = r9 y - 15 (r9 = r9_natief200.png, zie bewerk_r13 CROP).
from PIL import Image
import numpy as np

M0 = np.asarray(Image.open('model_gekozen.png').convert('RGB')).astype(int)
R9 = np.asarray(Image.open('r9_natief200.png').convert('RGB')).astype(int)
H, W = M0.shape[:2]
WH = np.array([255, 255, 255])

def is_white(c): return c.sum() / 3 > 235 and c.max() - c.min() < 20
def O(x, y):
    if 0 <= x < R9.shape[1] and 0 <= y < R9.shape[0]: return R9[y, x].copy()
    return WH.copy()
def white_at(a, X, Y): return not (0 <= X < W and 0 <= Y < H) or is_white(a[Y, X])

# r9-RF-bovenrand (bewerk_r10.rf_top) en zichtbaarheid in r9
def rf_top9(x): return 140 + (x - 101) / 3.0
def vis9(x, y): return y < rf_top9(x) - 0.6
def rf_topM(X): return rf_top9(X - 21) - 15

# ---------------------------------------------------------------- panelen
# (naam, f-vector, periode naar de verre kant, Delta f, kant van de verre kap, knip c = midden van het
#  eindvak, masker)
def mask_lf(X, Y, f): return X <= 62 and 84 <= Y <= 117 and f < 2120
def mask_bl(X, Y, f):
    top = 25 + (X - 85) * 15 / 53.0; bot = 35 + (X - 71) * 15 / 53.0
    return X <= 121 and top - 2 <= Y <= bot + 2 and f < 1700
def mask_rf(X, Y, f): return 95 <= X <= 156 and Y >= rf_topM(X) - 0.6 and Y <= 158 and f >= 3100
TWIN = None
def mask_tw(X, Y, f): return TWIN[Y, X]

PANELS = {
    #        f = a*X + b*Y   Dfar        verre kap laag/hoog   c (midden eindvak)
    'LF':   ((9, 16),        (-10, -4),  'low',                1637, mask_lf),
    'BL':   ((10, 14),       (-13, -4),  'low',                1295, mask_bl),
    'RF':   ((15, 12),       (11, 4),    'high',               3716, mask_rf),
    'TW':   ((10, 14),       (13, 4),    'high',               3191, mask_tw),
}

def twin_mask():
    """tweeling = pixels die in r9 achtergrond waren en nu niet (zoals bewerk_r13), rechts van de achterarm"""
    m = np.zeros((H, W), bool)
    for Y in range(40, 105):
        for X in range(150, W):
            x, y = X - 21, Y + 15
            if is_white(O(x, y)) and not is_white(M0[Y, X]): m[Y, X] = True
    return m

def shrink(a, name, k, under=None, free=None):
    """k vakken uit het paneel: alles voorbij de knip c schuift k periodes naar de buis.
    under(X,Y) -> kleur of None: wat er achter het paneel zit als het vrijkomt (anders wit).
    free(X,Y): mag het nieuwe paneel hier schilderen (standaard: alleen waar het paneel zelf of wit was)."""
    (fa, fb), (dx, dy), side, c, mask = PANELS[name]
    f = lambda X, Y: fa * X + fb * Y
    s = 1 if side == 'low' else -1                       # s*f stijgt naar de buis
    dfar = s * f(dx, dy)                                  # negatief: verre kant
    src = a.copy(); out = a.copy()
    region = lambda X, Y: s * f(X, Y) < s * c - k * dfar  # = s*c + k*|D|
    panel = np.zeros((H, W), bool)
    for Y in range(H):
        for X in range(W):
            if mask(X, Y, f(X, Y)) and not is_white(src[Y, X]): panel[Y, X] = True
    # 1. oud eindstuk weg
    for Y in range(H):
        for X in range(W):
            if panel[Y, X] and region(X, Y):
                u = under(X, Y) if under else None
                out[Y, X] = u if u is not None else WH
    # 2. eindstuk k periodes dichter bij de buis
    n = 0
    for Y in range(H):
        for X in range(W):
            if not region(X, Y): continue
            sx, sy = X + k * dx, Y + k * dy
            if not (0 <= sx < W and 0 <= sy < H) or not panel[sy, sx]: continue
            if s * f(sx, sy) >= s * c: continue
            ok = panel[Y, X] or is_white(src[Y, X]) or (free and free(X, Y))
            if ok: out[Y, X] = src[sy, sx]; n += 1
    return out

# ---------------------------------------------------------------- onderste mast (achter RF)
def mast_in_col(x): return not is_white(O(x, x + 20))          # kolom hoort bij de mast (r9 x 102..114)

def ml9(x, y, n, memo):
    """onderste mast met n vakken (2 = r9, 3 = model) in r9-coordinaten, onbedekt; None = geen mast"""
    key = (x, y)
    if key in memo: return memo[key]
    r = None
    if 101 <= x <= 115 and mast_in_col(x):
        f = y - x; sh = 13 * (n - 2)                             # extra vak = 13 px verticaal
        capf = 33 + sh
        if f < 29 and vis9(x, y):
            c = O(x, y); r = None if is_white(c) else c
        elif f <= capf - 1:                                      # binnenkant: periode terug tot zichtbaar
            yy = y - sh if f >= 29 else y
            while not (vis9(x, yy) and yy - x <= 32): yy -= 13
            c = O(x, yy); r = None if is_white(c) else c
        elif f <= capf + 1:                                      # eindkap (r9 f 33..34)
            yy = y - sh
            if vis9(x, yy):
                c = O(x, yy); r = None if is_white(c) else c
            else:
                r = ml9(x - 1, y - 1, n, memo)                   # kap langs zichzelf doorkopieren
    memo[key] = r
    return r

def mast_layer(n):
    memo = {}
    def u(X, Y):
        if Y < rf_topM(X) - 0.6: return None                     # zichtbaar deel: uit het model
        return ml9(X - 21, Y + 15, n, memo)
    return u, memo

def mast_lower_to_2(a):
    """B: onderste mast terug naar 2 vakken = r9-origineel (bewerk_r10 step_mast terugdraaien)"""
    out = a.copy(); memo = {}
    for X in range(122, 137):
        for Y in range(90, H):
            x, y = X - 21, Y + 15
            if y - x < 29 or Y >= rf_topM(X) - 0.6: continue
            c = ml9(x, y, 2, memo)
            out[Y, X] = c if c is not None else WH
    return out

def mast_upper(a, k):
    """bovenste mast k vakken korter: knip midden vak 1 (f=Y-X=-113), topkap 13k omlaag"""
    out = a.copy(); c = -113
    for X in range(118, 137):
        for Y in range(0, 34):
            if Y - X >= c + 13 * k: continue
            sy = Y - 13 * k
            v = a[sy, X] if sy >= 0 and sy - X < c else WH
            out[Y, X] = v
    return out

# ---------------------------------------------------------------- opruimen, meten
def background(a):
    h, w = a.shape[:2]; seen = np.zeros((h, w), bool)
    st = [(0, 0), (w - 1, 0), (0, h - 1), (w - 1, h - 1)]
    while st:
        x, y = st.pop()
        if not (0 <= x < w and 0 <= y < h) or seen[y, x] or not is_white(a[y, x]): continue
        seen[y, x] = True; st += [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]
    return seen

def clean(a):
    a = a.copy(); bg = background(a)
    a[bg] = 255
    # losse pixels (0-1 buren) die door het knippen overbleven
    changed = np.any(a != M0, axis=2)
    for _ in range(2):
        bg = background(a)
        for y in range(1, H - 1):
            for x in range(1, W - 1):
                if bg[y, x] or not changed[max(0, y - 1):y + 2, max(0, x - 1):x + 2].any(): continue
                if int((~bg[y - 1:y + 2, x - 1:x + 2]).sum()) - 1 <= 1: a[y, x] = 255
    return a

def bbox(a):
    nb = ~np.all(a >= 250, axis=2); ys, xs = np.where(nb)
    return xs.min(), ys.min(), xs.max(), ys.max()

def variant(front, back, mast):
    a = M0.copy()
    global TWIN
    TWIN = twin_mask()
    kf, kb, km = 4 - front, 4 - back, 3 - mast
    if km:
        a = mast_upper(a, km)
        a = mast_lower_to_2(a)
    n = 3 - km
    if kf:
        a = shrink(a, 'LF', kf)
        under, _ = mast_layer(n)
        a = shrink(a, 'RF', kf, under=under, free=lambda X, Y: under(X, Y) is not None)
    if kb:
        a = shrink(a, 'BL', kb)
        a = shrink(a, 'TW', kb)
    return clean(a)

def save(a, name, m=3):
    x0, y0, x1, y1 = bbox(a)
    box = (max(0, x0 - m), max(0, y0 - m), min(W, x1 + m + 1), min(H, y1 + m + 1))
    im = Image.fromarray(a[box[1]:box[3], box[0]:box[2]].astype('uint8'))
    im.save(name + '.png'); im.resize((im.width * 8, im.height * 8), Image.NEAREST).save(name + '_8x.png')
    return im, (x1 - x0 + 1, y1 - y0 + 1), box

# grote oog: paarse ring rond (32..36, 131) in het model
def eye_size(a):
    from collections import deque
    def P(c): r, g, b = c; return r > g + 25 and b > g + 25 and c.sum() / 3 > 60
    def T(c): r, g, b = c; return g > r + 20 and b > r + 10
    xs, ys = [], []
    for Y in range(115, 150):
        for X in range(40, 80):
            c = a[Y, X]
            if (P(c) or T(c)) and ((X - 55) ** 2 + (Y - 131) ** 2) < 15 ** 2: xs.append(X); ys.append(Y)
    return max(xs) - min(xs) + 1, max(ys) - min(ys) + 1

def enclosed_bg(a, seed=(118, 115), thr=253):
    """ingesloten achtergrond: de witte driehoek tussen hoofdarm, onderste mast en RF (zuiver wit)"""
    w = np.all(a >= thr, axis=2); seen = np.zeros((H, W), bool); st = [seed]
    while st:
        x, y = st.pop()
        if not (0 <= x < W and 0 <= y < H) or seen[y, x] or not w[y, x]: continue
        seen[y, x] = True; st += [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]
    return seen

def to64(a):
    """content (zonder marge) LANCZOS naar het 64-vak; achtergrond (ook de ingesloten driehoek) transparant"""
    bg = background(a) | enclosed_bg(a)
    rgba = np.dstack([a, np.where(bg, 0, 255)]).astype('uint8')
    I = Image.fromarray(rgba, 'RGBA')
    nb = np.where(~bg); y0, y1, x0, x1 = nb[0].min(), nb[0].max(), nb[1].min(), nb[1].max()
    I = I.crop((x0, y0, x1 + 1, y1 + 1))
    w, h = I.size; s = min(64 / w, 64 / h)
    r = I.resize((max(1, round(w * s)), max(1, round(h * s))), Image.LANCZOS)
    ar = np.asarray(r).copy(); ar[..., 3] = np.where(ar[..., 3] >= 128, 255, 0)
    return Image.fromarray(ar, 'RGBA'), s

if __name__ == '__main__':
    eye0 = eye_size(M0)
    res = [('r13b', M0, Image.fromarray(M0.astype('uint8')))]
    for nm, fr, bk, ms in (('A', 3, 3, 3), ('B', 3, 3, 2), ('C', 2, 2, 3)):
        a = variant(fr, bk, ms)
        im, (cw, ch), box = save(a, 'compact_%s_natief' % nm)
        res.append((nm, a, im))
    rows = []
    for nm, a, im in res:
        x0, y0, x1, y1 = bbox(a); cw, ch = x1 - x0 + 1, y1 - y0 + 1
        ew, eh = eye_size(a)
        sw, sh = 64 / cw, 64 / ch; s = min(sw, sh)
        print('%-5s canvas %s  inhoud %dx%d  verhouding %.2f  64/b=%.3f (hoogte %.1f)  64/h=%.3f (breedte %.1f)  '
              '-> %s begrenst, %dx%d op 64  oog %dx%d -> %.1fx%.1f px'
              % (nm, im.size, cw, ch, cw / ch, sw, ch * sw, sh, cw * sh, 'breedte' if sw < sh else 'hoogte',
                 round(cw * s), round(ch * s), ew, eh, ew * s, eh * s))
    # vel: r13b | A | B | C, elk in een lichtgrijs 64-vak, 6x
    S, gap = 6, 12
    sheet = Image.new('RGB', (4 * 64 * S + 5 * gap, 64 * S + 2 * gap), 'white')
    for i, (nm, a, im) in enumerate(res):
        r, s = to64(a)
        vak = Image.new('RGBA', (64, 64), (210, 210, 210, 255))
        vak.alpha_composite(r, ((64 - r.width) // 2, (64 - r.height) // 2))
        sheet.paste(vak.convert('RGB').resize((64 * S, 64 * S), Image.NEAREST), (gap + i * (64 * S + gap), gap))
    sheet.save('compact_varianten.png')
    # bewijs: romp/bollen/ogen ongewijzigd -> diff buiten paneel- en mastzones
    for nm, a, im in res[1:]:
        d = np.any(a != M0, axis=2); ys, xs = np.where(d)
        Image.fromarray(np.where(d, 0, 255).astype('uint8')).save('compact_%s_diff.png' % nm)
        print(nm, 'gewijzigde pixels', d.sum())
